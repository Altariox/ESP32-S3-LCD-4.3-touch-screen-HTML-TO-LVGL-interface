#!/usr/bin/env python3
"""Generate LVGL image assets from SVG logos.

- Input: data/logos/*.svg
- Output: src/generated/ui_assets.c + ui_assets.h

This keeps the build self-contained by using system tools already present on many Linux distros:
- rsvg-convert (librsvg) to rasterize SVG -> PNG
- ImageMagick (magick) to export raw RGBA bytes

The output format matches LVGL v8 "TRUE_COLOR_ALPHA" with project LV_COLOR_DEPTH.
This project uses LV_COLOR_DEPTH=16, so each pixel is: RGB565 (2 bytes, little-endian) + alpha (1 byte).
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
LOGOS_DIR = DATA_DIR / "logos"
OUTPUT_DIR = PROJECT_DIR / "src" / "generated"
LV_CONF_PATH = PROJECT_DIR / "lib" / "lv_conf.h"

# Desired icon size (px)
ICON_SIZE = 96


@dataclass(frozen=True)
class Asset:
    symbol: str
    svg_path: Path


def _require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(
            f"Required tool '{name}' not found in PATH. "
            f"Install it (e.g., apt install librsvg2-bin imagemagick) and retry."
        )
    return path


def _read_lv_color_depth(lv_conf_path: Path) -> int:
    if not lv_conf_path.exists():
        return 16

    content = lv_conf_path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"^\s*#define\s+LV_COLOR_DEPTH\s+(\d+)\s*$", content, flags=re.MULTILINE)
    if not m:
        return 16
    return int(m.group(1))


def _sanitize_symbol(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9_]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        raise ValueError("Empty symbol name")
    if name[0].isdigit():
        name = "img_" + name
    return name


def _run(cmd: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=False)


def _svg_to_png(svg: Path, png: Path, size: int) -> None:
    raise RuntimeError("_svg_to_png is deprecated; use _to_png")


def _looks_like_svg(path: Path) -> bool:
    try:
        head = path.read_bytes()[:256]
    except Exception:
        return False

    # UTF-8 BOM + '<'
    if head.startswith(b"\xef\xbb\xbf<"):
        return True
    if head.lstrip().startswith(b"<"):
        return True
    return b"<svg" in head.lower() or b"<?xml" in head.lower()


def _to_png(input_path: Path, png: Path, size: int) -> None:
    """Convert an input logo (SVG/PNG/JPG/...) into a square PNG with alpha."""

    svg_candidate = _looks_like_svg(input_path)

    # 1) If it is really SVG, try rsvg-convert first (fast, reliable for proper SVG).
    if svg_candidate:
        rsvg = shutil.which("rsvg-convert")
        if rsvg:
            cmd = [rsvg, "-w", str(size), "-h", str(size), "-o", str(png), str(input_path)]
            proc = _run(cmd)
            if proc.returncode == 0 and png.exists() and png.stat().st_size > 0:
                return

    # 2) Try ImageMagick for everything (also covers raster files with wrong extensions).
    magick = shutil.which("magick")
    if magick:
        # -resize keeps aspect ratio, -extent makes it square with transparent padding.
        cmd = [
            magick,
            str(input_path),
            "-alpha",
            "on",
            "-background",
            "none",
            "-resize",
            f"{size}x{size}",
            "-gravity",
            "center",
            "-extent",
            f"{size}x{size}",
            f"png32:{png}",
        ]
        proc = _run(cmd)
        if proc.returncode == 0 and png.exists() and png.stat().st_size > 0:
            return

    # 3) If it still looks like SVG, try Inkscape as a last resort.
    if svg_candidate:
        inkscape = shutil.which("inkscape")
        if inkscape:
            cmd = [
                inkscape,
                str(input_path),
                "--export-type=png",
                f"--export-filename={png}",
                f"--export-width={size}",
                f"--export-height={size}",
                "--export-background-opacity=0",
            ]
            proc = _run(cmd)
            if proc.returncode == 0 and png.exists() and png.stat().st_size > 0:
                return

    raise RuntimeError(
        f"Failed to rasterize {input_path.name}. "
        "If it's an SVG, it may be invalid; if it's a raster, it may be corrupted."
    )


def _png_to_rgba_bytes(png: Path) -> bytes:
    magick = _require_tool("magick")
    # Export raw RGBA bytes to stdout.
    cmd = [magick, str(png), "-depth", "8", "rgba:-"]
    proc = _run(cmd)
    if proc.returncode != 0:
        stderr = (proc.stderr or b"").decode("utf-8", errors="replace")
        raise RuntimeError(f"ImageMagick failed for {png.name}:\n{stderr}")
    return proc.stdout or b""


def _rgba_to_lvgl_true_color_alpha(rgba: bytes, *, width: int, height: int, color_depth: int) -> bytes:
    expected = width * height * 4
    if len(rgba) != expected:
        raise RuntimeError(f"Unexpected RGBA length: got {len(rgba)} bytes, expected {expected}")

    if color_depth != 16:
        raise RuntimeError(
            f"Unsupported LV_COLOR_DEPTH={color_depth} for asset generator. "
            "This project is configured for 16 (RGB565)."
        )

    out = bytearray(width * height * 3)
    o = 0
    for i in range(0, len(rgba), 4):
        r = rgba[i + 0]
        g = rgba[i + 1]
        b = rgba[i + 2]
        a = rgba[i + 3]

        rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        out[o + 0] = rgb565 & 0xFF
        out[o + 1] = (rgb565 >> 8) & 0xFF
        out[o + 2] = a
        o += 3

    return bytes(out)


def _format_c_bytes(data: bytes, *, cols: int = 12) -> str:
    # Hex bytes like 0x12,0xAB,... with line breaks.
    parts = [f"0x{b:02X}" for b in data]
    lines = []
    for i in range(0, len(parts), cols):
        lines.append("  " + ",".join(parts[i : i + cols]))
    return ",\n".join(lines)


def _discover_assets(logos_dir: Path) -> list[Asset]:
    # Fixed mapping: symbol name -> search needle in filename
    mapping = {
        "discord": "discord",
        "firefox": "firefox",
        "prusa": "prusa",
        "prismlauncher": "prismlauncher",
        "vscode": "vscode",
        "terminal": "terminal",
    }

    # Find SVGs by partial filename match.
    svgs = list(logos_dir.glob("*.svg"))
    if not svgs:
        raise RuntimeError(f"No SVG files found in {logos_dir}")

    def find_svg(needle: str) -> Path:
        needle_l = needle.lower()
        for p in svgs:
            if needle_l in p.name.lower():
                return p
        raise RuntimeError(
            f"Could not find an SVG matching '{needle}' in {logos_dir}. "
            f"Available: {[p.name for p in svgs]}"
        )

    chosen = {
        "discord": find_svg("discord"),
        "firefox": find_svg("firefox"),
        "prusa": find_svg("prusa"),
        "prismlauncher": find_svg("prismlauncher"),
        "vscode": find_svg("vscode"),
        "terminal": find_svg("terminal"),
    }

    assets: list[Asset] = []
    for key in mapping:
        symbol = f"ui_img_{_sanitize_symbol(mapping[key])}"
        assets.append(Asset(symbol=symbol, svg_path=chosen[key]))
    return assets


def generate() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    color_depth = _read_lv_color_depth(LV_CONF_PATH)

    assets = _discover_assets(LOGOS_DIR)

    h_lines: list[str] = []
    c_lines: list[str] = []

    h_lines.append("// Auto-generated assets (SVG -> LVGL)")
    h_lines.append("// Do not edit manually!")
    h_lines.append("")
    h_lines.append("#pragma once")
    h_lines.append("")
    h_lines.append('#include "lvgl.h"')
    h_lines.append("")

    c_lines.append("// Auto-generated assets (SVG -> LVGL)")
    c_lines.append("// Do not edit manually!")
    c_lines.append("")
    c_lines.append('#include "ui_assets.h"')
    c_lines.append("")
    c_lines.append("#ifndef LV_ATTRIBUTE_MEM_ALIGN")
    c_lines.append("#define LV_ATTRIBUTE_MEM_ALIGN")
    c_lines.append("#endif")
    c_lines.append("")

    with tempfile.TemporaryDirectory(prefix="ui_assets_") as tmp:
        tmpdir = Path(tmp)

        for asset in assets:
            png = tmpdir / f"{asset.symbol}.png"
            _to_png(asset.svg_path, png, ICON_SIZE)
            rgba = _png_to_rgba_bytes(png)
            lv_bytes = _rgba_to_lvgl_true_color_alpha(
                rgba, width=ICON_SIZE, height=ICON_SIZE, color_depth=color_depth
            )

            map_name = f"{asset.symbol}_map"
            h_lines.append(f"extern const lv_img_dsc_t {asset.symbol};")

            c_lines.append(f"static const LV_ATTRIBUTE_MEM_ALIGN uint8_t {map_name}[] = {{")
            c_lines.append(_format_c_bytes(lv_bytes))
            c_lines.append("};")
            c_lines.append("")
            c_lines.append(f"const lv_img_dsc_t {asset.symbol} = {{")
            c_lines.append("  .header.cf = LV_IMG_CF_TRUE_COLOR_ALPHA,")
            c_lines.append("  .header.always_zero = 0,")
            c_lines.append("  .header.reserved = 0,")
            c_lines.append(f"  .header.w = {ICON_SIZE},")
            c_lines.append(f"  .header.h = {ICON_SIZE},")
            c_lines.append(f"  .data_size = {ICON_SIZE * ICON_SIZE} * LV_IMG_PX_SIZE_ALPHA_BYTE,")
            c_lines.append(f"  .data = {map_name},")
            c_lines.append("};")
            c_lines.append("")

    (OUTPUT_DIR / "ui_assets.h").write_text("\n".join(h_lines) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "ui_assets.c").write_text("\n".join(c_lines) + "\n", encoding="utf-8")


def main() -> int:
    try:
        generate()
        print(f"Generated UI assets in: {OUTPUT_DIR}")
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

ENV_NAME="${PIO_ENV:-esp32s3box}"
UPLOAD_PORT="${PIO_PORT:-}"

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Error: missing command '$1'" >&2
    exit 1
  fi
}

need_cmd python3
need_cmd platformio

echo "==> [1/3] Generating LVGL image assets from data/logos (SVG)"
python3 scripts/generate_ui_assets.py

echo "==> [2/3] Generating LVGL UI from data/ (HTML/CSS/JS)"
python3 scripts/html_to_lvgl.py

echo "==> [3/3] Uploading firmware via PlatformIO"
cmd=(platformio run -e "$ENV_NAME" --target upload)
if [[ -n "$UPLOAD_PORT" ]]; then
  cmd+=(--upload-port "$UPLOAD_PORT")
fi
"${cmd[@]}"

echo "Done."

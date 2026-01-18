#!/usr/bin/env python3
"""
PlatformIO Pre-Build Script
Runs HTML to LVGL converter before compilation
"""

import subprocess
import sys
from pathlib import Path

Import("env")

project_dir = Path(env["PROJECT_DIR"])
script_path = project_dir / "scripts" / "html_to_lvgl.py"

def run_html_converter(source, target, env):
    print("\n" + "=" * 50)
    print("Running HTML to LVGL Converter...")
    print("=" * 50)
    
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(project_dir),
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    if result.returncode != 0:
        print("ERROR: HTML conversion failed!")
        env.Exit(1)
    
    print("=" * 50 + "\n")

# Run before building
env.AddPreAction("buildprog", run_html_converter)

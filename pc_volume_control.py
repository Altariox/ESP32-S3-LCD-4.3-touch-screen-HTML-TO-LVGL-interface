#!/usr/bin/env python3
"""pc_volume_control.py

ESP32 serial command listener.

- Volume control demo (VOL_UP / VOL_DOWN)
- Stream-deck style app launcher (APP_*)
"""

import serial
import subprocess
import sys
import time
import shutil

# Configuration
SERIAL_PORT = "/dev/ttyACM0"  # Adjust if needed
BAUD_RATE = 115200
VOLUME_STEP = 5  # % per click
MAX_VOLUME = 100
MIN_VOLUME = 0

def get_current_volume():
    """Get current volume percentage using pactl"""
    try:
        result = subprocess.run(
            ["pactl", "get-sink-volume", "@DEFAULT_SINK@"],
            capture_output=True, text=True, check=True
        )
        # Output like: "Volume: front-left: 65536 / 100% / 0.00 dB, ..."
        import re
        match = re.search(r'(\d+)%', result.stdout)
        if match:
            return int(match.group(1))
    except Exception:
        pass
    return 50  # Default if can't read

def set_volume(delta):
    """Adjust volume using pactl (PulseAudio), capped at 0-100%"""
    try:
        current = get_current_volume()
        new_volume = current + delta
        
        # Clamp to 0-100%
        new_volume = max(MIN_VOLUME, min(MAX_VOLUME, new_volume))
        
        if new_volume == current:
            print(f"Volume already at {current}%")
            return
        
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{new_volume}%"], check=True)
        direction = "+" if delta > 0 else "-"
        print(f"Volume {direction}: {current}% -> {new_volume}%")
    except FileNotFoundError:
        # Try amixer as fallback
        try:
            if delta > 0:
                subprocess.run(["amixer", "set", "Master", f"{delta}%+"], check=True)
            else:
                subprocess.run(["amixer", "set", "Master", f"{-delta}%-"], check=True)
        except Exception as e:
            print(f"Error adjusting volume: {e}")


def _launch_first_available(candidates: list[list[str]]) -> bool:
    """Try a list of commands; launch first one available."""
    for argv in candidates:
        if not argv:
            continue
        exe = argv[0]
        if shutil.which(exe) is None:
            continue
        try:
            subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            return True
        except Exception:
            continue
    return False


def launch_app(command: str) -> None:
    """Launch an application based on a serial command."""
    mapping: dict[str, list[list[str]]] = {
        "APP_DISCORD": [["discord"], ["discord-canary"], ["discord-ptb"]],
        "APP_BRAVE": [["brave-browser"], ["brave"]],
        "APP_PRUSA_SLICER": [["prusa-slicer"], ["PrusaSlicer"]],
        "APP_PRISM_LAUNCHER": [["prismlauncher"], ["PrismLauncher"]],
        "APP_VSCODE": [["code"], ["codium"], ["vscodium"]],
        "APP_TERMINAL": [
            ["x-terminal-emulator"],
            ["gnome-terminal"],
            ["konsole"],
            ["xfce4-terminal"],
            ["kitty"],
            ["alacritty"],
            ["wezterm"],
            ["tilix"],
        ],
    }

    candidates = mapping.get(command)
    if not candidates:
        print(f"Unknown APP command: {command}")
        return

    ok = _launch_first_available(candidates)
    if ok:
        print(f"Launched: {command}")
    else:
        print(
            f"Could not launch {command}. Install the app or edit the mapping in this script."
        )


def _is_probably_command(line: str) -> bool:
    # Ignore touch debug lines like: "Touch point: x 123, y 456"
    if not line:
        return False
    if line.startswith("Touch point"):
        return False
    # Only accept tokens we define (avoid spamming on random logs)
    if " " in line:
        return False
    if len(line) > 64:
        return False
    return True

def main():
    print("=" * 50)
    print("ESP32 Serial Controller (Volume + Stream Deck)")
    print("=" * 50)
    print(f"Connecting to {SERIAL_PORT}...")
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"✓ Connected to {SERIAL_PORT}")
        print("Listening for commands... (Ctrl+C to quit)")
        print("-" * 50)
        
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line and _is_probably_command(line):
                    print(f"Received: {line}")

                    if line == "VOL_UP":
                        set_volume(VOLUME_STEP)
                    elif line == "VOL_DOWN":
                        set_volume(-VOLUME_STEP)
                    elif line.startswith("APP_"):
                        launch_app(line)
                    else:
                        print(f"Unknown command: {line}")
            
            time.sleep(0.01)
            
    except serial.SerialException as e:
        print(f"Error: Could not open {SERIAL_PORT}")
        print(f"Details: {e}")
        print("\nTry:")
        print("  1. Check if ESP32 is connected")
        print("  2. Run: ls /dev/ttyACM*")
        print("  3. Update SERIAL_PORT in this script")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nStopped.")
        ser.close()

if __name__ == "__main__":
    main()

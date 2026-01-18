#!/usr/bin/env python3
"""
ESP32 Volume Controller
Listens to serial commands from ESP32 and adjusts PC volume
"""

import serial
import subprocess
import sys
import time

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
            print(f"🔇 Volume already at {current}%")
            return
        
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{new_volume}%"], check=True)
        print(f"{'🔊' if delta > 0 else '🔉'} Volume: {current}% → {new_volume}%")
    except FileNotFoundError:
        # Try amixer as fallback
        try:
            if delta > 0:
                subprocess.run(["amixer", "set", "Master", f"{delta}%+"], check=True)
            else:
                subprocess.run(["amixer", "set", "Master", f"{-delta}%-"], check=True)
        except Exception as e:
            print(f"Error adjusting volume: {e}")

def main():
    print("=" * 50)
    print("ESP32 Volume Controller")
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
                if line:
                    print(f"Received: {line}")
                    
                    if line == "VOL_UP":
                        set_volume(VOLUME_STEP)
                    elif line == "VOL_DOWN":
                        set_volume(-VOLUME_STEP)
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

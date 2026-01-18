#!/usr/bin/env python3
"""
PC App Launcher - Receives commands from ESP32 Stream Deck via USB Serial
and launches the corresponding applications on Linux.
"""

import subprocess
import serial
import serial.tools.list_ports
import sys
import time

# App commands mapping - matches the button names in the UI
APP_COMMANDS = {
    "APP_DISCORD": ["discord"],
    "APP_BRAVE": ["brave-browser"],
    "APP_PRUSA_SLICER": ["prusa-slicer"],
    "APP_PRISM_LAUNCHER": ["prismlauncher"],
    "APP_VSCODE": ["code"],
    "APP_TERMINAL": ["gnome-terminal"],
}

# Alternative commands if primary fails
APP_ALTERNATIVES = {
    "APP_BRAVE": ["brave", "brave-browser-stable", "flatpak run com.brave.Browser"],
    "APP_PRUSA_SLICER": ["PrusaSlicer", "flatpak run com.prusa3d.PrusaSlicer"],
    "APP_VSCODE": ["codium", "code-oss", "flatpak run com.visualstudio.code"],
    "APP_TERMINAL": ["konsole", "xfce4-terminal", "alacritty", "kitty", "xterm"],
}


def find_esp32_port():
    """Find the ESP32 serial port."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # ESP32-S3 typically shows up as ttyACM* or ttyUSB*
        if "ACM" in port.device or "USB" in port.device:
            # Check for ESP32 identifiers
            desc = (port.description or "").lower()
            if "esp" in desc or "cp210" in desc or "ch340" in desc or "usb" in desc:
                return port.device
        # Also check by VID/PID for ESP32-S3 native USB
        if port.vid == 0x303a:  # Espressif VID
            return port.device
    
    # Fallback: return first ACM port
    for port in ports:
        if "ACM" in port.device:
            return port.device
    
    return None


def launch_app(cmd_name):
    """Launch an application by command name."""
    if cmd_name not in APP_COMMANDS:
        print(f"Unknown command: {cmd_name}")
        return False
    
    # Try primary command
    cmd = APP_COMMANDS[cmd_name]
    try:
        subprocess.Popen(cmd, start_new_session=True, 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Launched: {' '.join(cmd)}")
        return True
    except FileNotFoundError:
        pass
    
    # Try alternatives
    if cmd_name in APP_ALTERNATIVES:
        for alt in APP_ALTERNATIVES[cmd_name]:
            try:
                if isinstance(alt, str):
                    alt = alt.split()
                subprocess.Popen(alt, start_new_session=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"Launched (alternative): {' '.join(alt)}")
                return True
            except FileNotFoundError:
                continue
    
    print(f"Could not find executable for: {cmd_name}")
    return False


def main():
    print("=" * 50)
    print("ESP32 Stream Deck - PC App Launcher")
    print("=" * 50)
    
    # Find ESP32 port
    port = find_esp32_port()
    if not port:
        print("ERROR: Could not find ESP32 serial port!")
        print("Available ports:")
        for p in serial.tools.list_ports.comports():
            print(f"  {p.device}: {p.description}")
        sys.exit(1)
    
    print(f"Connecting to ESP32 on {port}...")
    
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"Connected! Listening for commands...")
        print("-" * 50)
        
        while True:
            try:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(f"Received: {line}")
                    
                    # Check for app launch commands
                    if line.startswith("APP_"):
                        launch_app(line)
                    elif line.startswith("BTN_"):
                        # Map button presses to app commands
                        btn_map = {
                            "BTN_DISCORD": "APP_DISCORD",
                            "BTN_BRAVE": "APP_BRAVE",
                            "BTN_PRUSA": "APP_PRUSA_SLICER",
                            "BTN_PRISM": "APP_PRISM_LAUNCHER",
                            "BTN_VSCODE": "APP_VSCODE",
                            "BTN_TERMINAL": "APP_TERMINAL",
                        }
                        if line in btn_map:
                            launch_app(btn_map[line])
                            
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                print("Attempting to reconnect...")
                time.sleep(2)
                ser.close()
                ser = serial.Serial(port, 115200, timeout=1)
                
    except KeyboardInterrupt:
        print("\nExiting...")
    except serial.SerialException as e:
        print(f"Could not open serial port: {e}")
        sys.exit(1)
    finally:
        if 'ser' in locals():
            ser.close()


if __name__ == "__main__":
    main()

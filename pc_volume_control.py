#!/usr/bin/env python3
"""pc_volume_control.py

ESP32 serial command listener + time/weather sender.

- Volume control (VOL_UP / VOL_DOWN / VOL_MUTE)
- Stream-deck style app launcher (APP_*)
- Sends time & weather data to ESP32
"""

import serial
import subprocess
import sys
import time
import shutil
import threading
import requests
from datetime import datetime
import locale

# Configuration
SERIAL_PORT = "/dev/ttyACM0"  # Adjust if needed
BAUD_RATE = 115200
VOLUME_STEP = 5  # % per click
MAX_VOLUME = 100
MIN_VOLUME = 0

# Weather config - Open-Meteo API (free, no API key needed)
# Grenoble coordinates (change to your location)
LATITUDE = 45.1885
LONGITUDE = 5.7245
WEATHER_UPDATE_INTERVAL = 300  # seconds (5 min)
TIME_UPDATE_INTERVAL = 1  # seconds

# Set French locale for date formatting
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except:
    pass  # Use default if French locale not available

# Global serial connection
ser = None
last_weather = {"temp": "--", "humidity": "--", "wind": "--", "description": "..."}


def get_current_volume():
    """Get current volume percentage using pactl"""
    try:
        result = subprocess.run(
            ["pactl", "get-sink-volume", "@DEFAULT_SINK@"],
            capture_output=True, text=True, check=True
        )
        import re
        match = re.search(r'(\d+)%', result.stdout)
        if match:
            return int(match.group(1))
    except Exception:
        pass
    return 50


def set_volume(delta):
    """Adjust volume using pactl (PulseAudio), capped at 0-100%"""
    try:
        current = get_current_volume()
        new_volume = current + delta
        new_volume = max(MIN_VOLUME, min(MAX_VOLUME, new_volume))
        
        if new_volume == current:
            print(f"Volume already at {current}%")
            return
        
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{new_volume}%"], check=True)
        direction = "+" if delta > 0 else "-"
        print(f"Volume {direction}: {current}% -> {new_volume}%")
    except FileNotFoundError:
        try:
            if delta > 0:
                subprocess.run(["amixer", "set", "Master", f"{delta}%+"], check=True)
            else:
                subprocess.run(["amixer", "set", "Master", f"{-delta}%-"], check=True)
        except Exception as e:
            print(f"Error adjusting volume: {e}")


def toggle_mute():
    """Toggle mute state using pactl"""
    try:
        subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"], check=True)
        print("Mute toggled")
    except FileNotFoundError:
        try:
            subprocess.run(["amixer", "set", "Master", "toggle"], check=True)
        except Exception as e:
            print(f"Error toggling mute: {e}")


def _launch_first_available(candidates):
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


def launch_app(command):
    """Launch an application based on a serial command."""
    mapping = {
        "APP_LIBREOFFICE": [["libreoffice"], ["soffice"]],
        "APP_FIREFOX": [["firefox"], ["firefox-esr"]],
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
        print(f"Could not launch {command}.")


def weather_code_to_text(code):
    """Convert WMO weather code to French description"""
    codes = {
        0: "Ciel degage",
        1: "Peu nuageux",
        2: "Partiellement nuageux",
        3: "Couvert",
        45: "Brouillard",
        48: "Brouillard givrant",
        51: "Bruine legere",
        53: "Bruine",
        55: "Bruine forte",
        61: "Pluie legere",
        63: "Pluie",
        65: "Pluie forte",
        71: "Neige legere",
        73: "Neige",
        75: "Neige forte",
        80: "Averses",
        81: "Averses fortes",
        82: "Averses violentes",
        95: "Orage",
        96: "Orage + grele",
        99: "Orage violent",
    }
    return codes.get(code, "Inconnu")


def fetch_weather():
    """Fetch weather from Open-Meteo API"""
    global last_weather
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        current = data.get("current", {})
        temp = current.get("temperature_2m", "--")
        humidity = current.get("relative_humidity_2m", "--")
        wind = current.get("wind_speed_10m", "--")
        weather_code = current.get("weather_code", 0)
        
        last_weather = {
            "temp": int(temp) if temp != "--" else "--",
            "humidity": int(humidity) if humidity != "--" else "--",
            "wind": int(wind) if wind != "--" else "--",
            "description": weather_code_to_text(weather_code)
        }
        print(f"Weather updated: {last_weather['temp']}°C, {last_weather['description']}")
    except Exception as e:
        print(f"Weather fetch error: {e}")


def send_to_esp(data):
    """Send data to ESP32 via serial"""
    global ser
    if ser and ser.is_open:
        try:
            ser.write(f"{data}\n".encode())
        except Exception as e:
            print(f"Serial write error: {e}")


def time_sender_thread():
    """Thread that sends time updates to ESP32"""
    while True:
        try:
            now = datetime.now()
            time_str = now.strftime("%H:%M")
            
            # French date format
            day_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            month_names = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", 
                          "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
            
            day_name = day_names[now.weekday()]
            month_name = month_names[now.month - 1]
            date_str = f"{day_name} {now.day} {month_name} {now.year}"
            
            send_to_esp(f"TIME:{time_str}")
            send_to_esp(f"DATE:{date_str}")
            
        except Exception as e:
            print(f"Time sender error: {e}")
        
        time.sleep(TIME_UPDATE_INTERVAL)


def weather_sender_thread():
    """Thread that fetches and sends weather updates"""
    while True:
        fetch_weather()
        
        send_to_esp(f"TEMP:{last_weather['temp']}")
        send_to_esp(f"WEATHER:{last_weather['description']}")
        send_to_esp(f"HUMIDITY:{last_weather['humidity']}%")
        send_to_esp(f"WIND:{last_weather['wind']} km/h")
        
        time.sleep(WEATHER_UPDATE_INTERVAL)


def _is_probably_command(line):
    if not line:
        return False
    if line.startswith("Touch point"):
        return False
    if " " in line:
        return False
    if len(line) > 64:
        return False
    return True


def main():
    global ser
    
    print("=" * 50)
    print("ESP32 Serial Controller (Volume + Weather)")
    print("=" * 50)
    print(f"Connecting to {SERIAL_PORT}...")
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"✓ Connected to {SERIAL_PORT}")
        
        # Start background threads for time and weather
        time_thread = threading.Thread(target=time_sender_thread, daemon=True)
        weather_thread = threading.Thread(target=weather_sender_thread, daemon=True)
        time_thread.start()
        weather_thread.start()
        
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
                    elif line == "VOL_MUTE":
                        toggle_mute()
                    elif line.startswith("APP_"):
                        launch_app(line)
                    else:
                        print(f"Unknown command: {line}")
            
            time.sleep(0.01)
            
    except serial.SerialException as e:
        print(f"Error: Could not open {SERIAL_PORT}")
        print(f"Details: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nStopped.")
        if ser:
            ser.close()


if __name__ == "__main__":
    main()

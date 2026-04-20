#!/usr/bin/env python3
import serial, subprocess, sys, time, shutil, threading, requests
from serial.tools import list_ports
from datetime import datetime

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200
VOLUME_STEP = 5
MAX_VOLUME, MIN_VOLUME = 100, 0
LATITUDE, LONGITUDE = 45.1885, 5.7245
WEATHER_UPDATE_INTERVAL = 300
TIME_UPDATE_INTERVAL = 1
RECONNECT_INTERVAL = 2

ser = None
serial_lock = threading.Lock()
last_weather = {"temp": "--", "humidity": "--", "wind": "--", "description": "..."}

# Precompile regex
import re
_volume_re = re.compile(r'(\d+)%')

def get_current_volume():
    try:
        out = subprocess.run(["pactl", "get-sink-volume", "@DEFAULT_SINK@"],
                             capture_output=True, text=True, check=True).stdout
        m = _volume_re.search(out)
        return int(m.group(1)) if m else 50
    except Exception:
        return 50

def set_volume(delta):
    try:
        current = get_current_volume()
        new_volume = max(MIN_VOLUME, min(MAX_VOLUME, current + delta))
        if new_volume != current:
            subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{new_volume}%"], check=True)
    except FileNotFoundError:
        cmd = ["amixer", "set", "Master", f"{abs(delta)}%{'+' if delta>0 else '-'}"]
        subprocess.run(cmd, check=True)

def toggle_mute():
    try:
        subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"], check=True)
    except FileNotFoundError:
        subprocess.run(["amixer", "set", "Master", "toggle"], check=True)

def _launch_first_available(candidates):
    for argv in candidates:
        if argv and shutil.which(argv[0]):
            subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            return True
    return False

def launch_app(command):
    mapping = {
        "APP_LIBREOFFICE": [["libreoffice"], ["soffice"]],
        "APP_FIREFOX": [["firefox"], ["firefox-esr"]],
        "APP_PRUSA_SLICER": [["prusa-slicer"], ["PrusaSlicer"]],
        "APP_PRISM_LAUNCHER": [["prismlauncher"], ["PrismLauncher"]],
        "APP_VSCODE": [["code"], ["codium"], ["vscodium"]],
        "APP_TERMINAL": [["x-terminal-emulator"], ["gnome-terminal"], ["konsole"], ["xfce4-terminal"],
                         ["kitty"], ["alacritty"], ["wezterm"], ["tilix"]],
    }
    _launch_first_available(mapping.get(command, []))

def weather_code_to_text(code):
    return {
        0:"Ciel degage",1:"Peu nuageux",2:"Partiellement nuageux",3:"Couvert",
        45:"Brouillard",48:"Brouillard givrant",51:"Bruine legere",53:"Bruine",55:"Bruine forte",
        61:"Pluie legere",63:"Pluie",65:"Pluie forte",71:"Neige legere",73:"Neige",75:"Neige forte",
        80:"Averses",81:"Averses fortes",82:"Averses violentes",95:"Orage",96:"Orage + grele",99:"Orage violent"
    }.get(code,"Inconnu")

def fetch_weather():
    global last_weather
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
        data = requests.get(url, timeout=10).json().get("current", {})
        last_weather = {
            "temp": int(data.get("temperature_2m","--")) if data.get("temperature_2m") else "--",
            "humidity": int(data.get("relative_humidity_2m","--")) if data.get("relative_humidity_2m") else "--",
            "wind": int(data.get("wind_speed_10m","--")) if data.get("wind_speed_10m") else "--",
            "description": weather_code_to_text(data.get("weather_code",0))
        }
    except:
        pass

def _find_serial_port(preferred=SERIAL_PORT):
    ports = [p.device for p in list_ports.comports()]
    if preferred in ports:
        return preferred
    for p in ports:
        if p.startswith("/dev/ttyACM") or p.startswith("/dev/ttyUSB"):
            return p
    return None

def _connect_serial_if_available():
    global ser
    port = _find_serial_port()
    if not port:
        return False

    try:
        candidate = serial.Serial(port, BAUD_RATE, timeout=1)
    except serial.SerialException:
        return False

    with serial_lock:
        if ser and ser.is_open:
            try:
                ser.close()
            except serial.SerialException:
                pass
        ser = candidate
    return True

def _disconnect_serial():
    global ser
    with serial_lock:
        if ser:
            try:
                ser.close()
            except serial.SerialException:
                pass
        ser = None

def send_to_esp(data):
    with serial_lock:
        if ser and ser.is_open:
            try:
                ser.write(f"{data}\n".encode())
            except serial.SerialException:
                pass

def time_sender_thread():
    while True:
        now = datetime.now()
        send_to_esp(f"TIME:{now:%H:%M}")
        send_to_esp(f"DATE:{now:%A} {now.day} {now:%B} {now.year}")
        time.sleep(TIME_UPDATE_INTERVAL)

def weather_sender_thread():
    while True:
        fetch_weather()
        send_to_esp(f"TEMP:{last_weather['temp']}")
        send_to_esp(f"WEATHER:{last_weather['description']}")
        send_to_esp(f"HUMIDITY:{last_weather['humidity']}%")
        send_to_esp(f"WIND:{last_weather['wind']} km/h")
        time.sleep(WEATHER_UPDATE_INTERVAL)

def _is_command(line):
    return line and not line.startswith("Touch point") and " " not in line and len(line)<=64

def main():
    connected = False
    try:
        threading.Thread(target=time_sender_thread, daemon=True).start()
        threading.Thread(target=weather_sender_thread, daemon=True).start()

        while True:
            if not connected:
                connected = _connect_serial_if_available()
                if not connected:
                    time.sleep(RECONNECT_INTERVAL)
                    continue

            try:
                with serial_lock:
                    current_ser = ser

                if current_ser and current_ser.is_open and current_ser.in_waiting:
                    line = current_ser.readline().decode('utf-8', errors='ignore').strip()
                    if _is_command(line):
                        if line=="VOL_UP": set_volume(VOLUME_STEP)
                        elif line=="VOL_DOWN": set_volume(-VOLUME_STEP)
                        elif line=="VOL_MUTE": toggle_mute()
                        elif line.startswith("APP_"): launch_app(line)
            except (serial.SerialException, OSError):
                _disconnect_serial()
                connected = False

            time.sleep(0.05)  # plus léger que 0.01
    except KeyboardInterrupt:
        _disconnect_serial()
        sys.exit(0)

if __name__=="__main__":
    main()

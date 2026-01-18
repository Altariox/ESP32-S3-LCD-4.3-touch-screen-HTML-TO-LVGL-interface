# ESP32‑S3 Touch LCD 4.3" (Waveshare) — Stream Deck + Dashboard

Langues: **Français** | **English**

---

## Français

### Description

Ce dépôt contient un projet **PlatformIO (Arduino)** pour la carte **Waveshare ESP32‑S3 Touch LCD 4.3" (800×480)** avec **LVGL v8.3.x**.

Objectif: pouvoir décrire l'interface en **HTML/CSS/JS très simple**, puis la **traduire automatiquement en LVGL C** au moment du build.

### Fonctionnalités

**2 pages avec navigation par swipe horizontal:**

#### Page 1 — Stream Deck (6 boutons)
Lance des applications sur le PC:
- LibreOffice
- Firefox
- Prusa Slicer
- Prism Launcher
- VS Code
- Terminal

#### Page 2 — Dashboard
Affiche en temps réel:
- **Horloge** (police 48px)
- **Date** complète
- **Contrôle du volume** (Vol+, Mute, Vol-)
- **Météo** (température, description, humidité, vent) via Open-Meteo API

Les données sont envoyées depuis le PC via série.

### Structure

```
data/
├── index.html          # Interface HTML (2 pages)
├── style.css           # Styles CSS
├── script.js           # Actions JS
└── logos/              # Icônes SVG des apps

scripts/
├── html_to_lvgl.py     # Convertisseur HTML→LVGL
└── generate_ui_assets.py  # Générateur SVG→LVGL

src/
├── main.cpp            # Firmware ESP32
└── generated/          # Code LVGL auto-généré

pc_volume_control.py    # Script PC (volume + météo + heure)
start.sh                # Build complet
```

### Prérequis

- PlatformIO (VS Code) ou CLI `platformio`
- Python 3 + `pyserial`, `requests`, `pulsectl`
- Pour les icônes: `rsvg-convert` (librsvg) ou ImageMagick
- Applications: LibreOffice, Firefox, Prusa Slicer, Prism Launcher, VS Code, Terminal

### Installation

```bash
# Dépendances Python
pip install pyserial requests pulsectl

# Arch Linux
sudo pacman -S python-pyserial python-requests python-pulsectl
```

### Build & Flash

```bash
./start.sh
```

Ce script:
1. Génère les assets LVGL depuis les SVG
2. Convertit HTML/CSS/JS en code LVGL C
3. Compile et flashe le firmware

### Lancer le contrôleur PC

```bash
python3 pc_volume_control.py
```

Le script:
- Écoute les commandes série (apps, volume)
- Envoie l'heure toutes les secondes
- Envoie la météo toutes les 5 minutes (Grenoble par défaut)

### Personnalisation

#### Changer les applications
1. Modifier `data/index.html` (boutons)
2. Modifier `data/style.css` (couleurs, positions)
3. Modifier `data/script.js` (commandes)
4. Ajouter les logos SVG dans `data/logos/`
5. Mettre à jour `pc_volume_control.py`

#### Changer la localisation météo
Dans `pc_volume_control.py`, modifier les coordonnées:
```python
LATITUDE = 45.1885   # Grenoble
LONGITUDE = 5.7245
```

---

## English

### Overview

This repository is a **PlatformIO (Arduino)** project for the **Waveshare ESP32‑S3 Touch LCD 4.3" (800×480)** using **LVGL v8.3.x**.

Goal: describe a simple UI using **HTML/CSS/JS**, then **auto‑convert it to LVGL C** at build time.

### Features

**2 pages with horizontal swipe navigation:**

#### Page 1 — Stream Deck (6 buttons)
Launch PC applications:
- LibreOffice
- Firefox
- Prusa Slicer
- Prism Launcher
- VS Code
- Terminal

#### Page 2 — Dashboard
Real-time display:
- **Clock** (48px font)
- **Full date**
- **Volume controls** (Vol+, Mute, Vol-)
- **Weather** (temperature, description, humidity, wind) via Open-Meteo API

Data is sent from PC via serial.

### Structure

```
data/
├── index.html          # HTML UI (2 pages)
├── style.css           # CSS styles
├── script.js           # JS actions
└── logos/              # SVG app icons

scripts/
├── html_to_lvgl.py     # HTML→LVGL converter
└── generate_ui_assets.py  # SVG→LVGL generator

src/
├── main.cpp            # ESP32 firmware
└── generated/          # Auto-generated LVGL code

pc_volume_control.py    # PC script (volume + weather + time)
start.sh                # Full build
```

### Requirements

- PlatformIO (VS Code) or `platformio` CLI
- Python 3 + `pyserial`, `requests`, `pulsectl`
- For icons: `rsvg-convert` (librsvg) or ImageMagick
- Apps: LibreOffice, Firefox, Prusa Slicer, Prism Launcher, VS Code, Terminal

### Installation

```bash
# Python dependencies
pip install pyserial requests pulsectl

# Arch Linux
sudo pacman -S python-pyserial python-requests python-pulsectl
```

### Build & Flash

```bash
./start.sh
```

This script:
1. Generates LVGL assets from SVGs
2. Converts HTML/CSS/JS to LVGL C code
3. Compiles and uploads the firmware

### Run PC controller

```bash
python3 pc_volume_control.py
```

The script:
- Listens for serial commands (apps, volume)
- Sends time every second
- Sends weather every 5 minutes (Grenoble by default)

### Customization

#### Change applications
1. Edit `data/index.html` (buttons)
2. Edit `data/style.css` (colors, positions)
3. Edit `data/script.js` (commands)
4. Add SVG logos in `data/logos/`
5. Update `pc_volume_control.py`

#### Change weather location
In `pc_volume_control.py`, modify coordinates:
```python
LATITUDE = 45.1885   # Grenoble
LONGITUDE = 5.7245
```

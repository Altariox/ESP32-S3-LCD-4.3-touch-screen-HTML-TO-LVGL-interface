# ESP32‑S3 Touch LCD 4.3" (Waveshare) — Stream Deck + Contrôle PC

Langues: **Français** | **English** | **Español**

---

## Français

### Description

Ce dépôt contient un projet **PlatformIO (Arduino)** pour la carte **Waveshare ESP32‑S3 Touch LCD 4.3" (800×480)** avec **LVGL v8.3.x**.

Objectif: pouvoir décrire l'interface en **HTML/CSS/JS très simple**, puis la **traduire automatiquement en LVGL C** au moment du build.

**Stream Deck inclus**: une interface avec **6 boutons tactiles** pour lancer des applications sur le PC:
- Discord
- Firefox
- Prusa Slicer
- Prism Launcher
- VS Code
- Terminal

Les boutons envoient des commandes série (`APP_DISCORD`, `APP_FIREFOX`, etc.) vers le PC. Un script Python écoute et lance les applications correspondantes.

### Structure

- Interface "web": [data/index.html](data/index.html), [data/style.css](data/style.css), [data/script.js](data/script.js)
- Logos SVG: [data/logos/](data/logos/)
- Convertisseur HTML→LVGL: [scripts/html_to_lvgl.py](scripts/html_to_lvgl.py)
- Générateur d'assets (SVG→LVGL): [scripts/generate_ui_assets.py](scripts/generate_ui_assets.py)
- Généré automatiquement: [src/generated/](src/generated/)
- Firmware principal: [src/main.cpp](src/main.cpp)
- Lanceur d'apps côté PC: [pc_volume_control.py](pc_volume_control.py)

### Prérequis

- PlatformIO (VS Code) ou CLI `platformio`
- Python 3 + `pyserial` (sur Arch: `sudo pacman -S python-pyserial`)
- Pour les icônes: `rsvg-convert` (librsvg) ou ImageMagick (`magick`) ou Inkscape
- Applications à lancer: Discord, Firefox, Prusa Slicer, Prism Launcher, VS Code, Terminal

### Build & Flash

1. Brancher la carte en USB
2. Vérifier le port (`ls /dev/ttyACM*`)
3. Lancer le build complet:

```bash
./start.sh
```

Ce script:
1. Génère les assets LVGL depuis les SVG
2. Convertit HTML/CSS/JS en code LVGL C
3. Compile et flashe le firmware

### Lancer le lanceur d'apps PC

1. Fermer le moniteur série PlatformIO (sinon le port peut être "busy")
2. Lancer:

```bash
python3 pc_volume_control.py
```

3. Appuyer sur les boutons sur l'écran tactile pour lancer les apps!

### Personnalisation

Pour changer les applications:
1. Modifier [data/index.html](data/index.html) (boutons)
2. Modifier [data/style.css](data/style.css) (couleurs, positions)
3. Modifier [data/script.js](data/script.js) (commandes envoyées)
4. Ajouter les logos SVG dans [data/logos/](data/logos/)
5. Mettre à jour [scripts/generate_ui_assets.py](scripts/generate_ui_assets.py) (mapping des icônes)
6. Mettre à jour [pc_volume_control.py](pc_volume_control.py) (commandes → exécutables)

---

## English

### Overview

This repository is a **PlatformIO (Arduino)** project for the **Waveshare ESP32‑S3 Touch LCD 4.3" (800×480)** using **LVGL v8.3.x**.

Goal: describe a very simple UI using **HTML/CSS/JS**, then **auto‑convert it to LVGL C** at build time.

**Stream Deck included**: a 6-button touch interface to launch PC applications:
- Discord
- Firefox
- Prusa Slicer
- Prism Launcher
- VS Code
- Terminal

Buttons send serial commands (`APP_DISCORD`, `APP_FIREFOX`, etc.) to the PC. A Python script listens and launches the corresponding applications.

### Key paths

- "Web" UI: [data/index.html](data/index.html), [data/style.css](data/style.css), [data/script.js](data/script.js)
- SVG logos: [data/logos/](data/logos/)
- HTML→LVGL converter: [scripts/html_to_lvgl.py](scripts/html_to_lvgl.py)
- Asset generator (SVG→LVGL): [scripts/generate_ui_assets.py](scripts/generate_ui_assets.py)
- Generated output: [src/generated/](src/generated/)
- Firmware entry: [src/main.cpp](src/main.cpp)
- PC app launcher: [pc_volume_control.py](pc_volume_control.py)

### Requirements

- PlatformIO (VS Code) or `platformio` CLI
- Python 3 + `pyserial` (Arch: `sudo pacman -S python-pyserial`)
- For icons: `rsvg-convert` (librsvg) or ImageMagick (`magick`) or Inkscape
- Apps to launch: Discord, Firefox, Prusa Slicer, Prism Launcher, VS Code, Terminal

### Build & Upload

1. Plug the board via USB
2. Check the device path (`ls /dev/ttyACM*`)
3. Run the full build:

```bash
./start.sh
```

This script:
1. Generates LVGL assets from SVGs
2. Converts HTML/CSS/JS to LVGL C code
3. Compiles and uploads the firmware

### Run PC app launcher

1. Close PlatformIO serial monitor (otherwise the port may be busy)
2. Run:

```bash
python3 pc_volume_control.py
```

3. Tap buttons on the touch screen to launch apps!

---

## Español

### Descripción

Este repositorio contiene un proyecto **PlatformIO (Arduino)** para la **Waveshare ESP32‑S3 Touch LCD 4.3" (800×480)** con **LVGL v8.3.x**.

Objetivo: definir una interfaz simple con **HTML/CSS/JS** y **convertirla automáticamente a LVGL C** durante el build.

**Stream Deck incluido**: interfaz táctil con **6 botones** para lanzar aplicaciones en el PC:
- Discord
- Firefox
- Prusa Slicer
- Prism Launcher
- VS Code
- Terminal

Los botones envían comandos serie (`APP_DISCORD`, `APP_FIREFOX`, etc.) al PC. Un script Python escucha y lanza las aplicaciones correspondientes.

### Rutas importantes

- UI "web": [data/index.html](data/index.html), [data/style.css](data/style.css), [data/script.js](data/script.js)
- Logos SVG: [data/logos/](data/logos/)
- Convertidor HTML→LVGL: [scripts/html_to_lvgl.py](scripts/html_to_lvgl.py)
- Generador de assets: [scripts/generate_ui_assets.py](scripts/generate_ui_assets.py)
- Archivos generados: [src/generated/](src/generated/)
- Firmware principal: [src/main.cpp](src/main.cpp)
- Lanzador de apps (PC): [pc_volume_control.py](pc_volume_control.py)

### Compilar y flashear

1. Conecta la placa por USB
2. Verifica el puerto (`ls /dev/ttyACM*`)
3. Ejecuta el build completo:

```bash
./start.sh
```

### Ejecutar el lanzador en el PC

1. Cierra el monitor serie de PlatformIO
2. Ejecuta:

```bash
python3 pc_volume_control.py
```

3. ¡Pulsa los botones en la pantalla táctil para lanzar las apps!

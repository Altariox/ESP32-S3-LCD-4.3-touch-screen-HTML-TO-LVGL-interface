# ESP32‑S3 Touch LCD 4.3" (Waveshare) — UI “Web” → LVGL + Contrôle de volume PC

Langues: **Français** | **English** | **Español**

---

## Français

### Description

Ce dépôt contient un projet **PlatformIO (Arduino)** pour la carte **Waveshare ESP32‑S3 Touch LCD 4.3" (800×480)** avec **LVGL v8.3.x**.

Objectif: pouvoir décrire l’interface en **HTML/CSS/JS très simple**, puis la **traduire automatiquement en LVGL C** au moment du build.

Démo incluse: une interface minimaliste avec deux boutons **“+”** et **“-”** sur l’écran tactile qui envoient des commandes série (`VOL_UP` / `VOL_DOWN`) vers le PC.

Sur le PC, un script Python écoute le port série et ajuste le volume (Linux / PipeWire / PulseAudio via `pactl`). Le volume est **borné entre 0% et 100%**.

### Structure

- Interface “web”: [data/index.html](data/index.html), [data/style.css](data/style.css), [data/script.js](data/script.js)
- Convertisseur HTML→LVGL: [scripts/html_to_lvgl.py](scripts/html_to_lvgl.py)
- Généré automatiquement: [src/generated/ui_generated.c](src/generated/ui_generated.c) et [src/generated/ui_generated.h](src/generated/ui_generated.h)
- Firmware principal: [src/main.cpp](src/main.cpp)
- Contrôle volume côté PC: [pc_volume_control.py](pc_volume_control.py)

### Prérequis

- PlatformIO (VS Code) ou CLI `platformio`
- Linux: `pactl` (PipeWire/PulseAudio). Optionnel: `amixer` en fallback
- Python 3 + `pyserial` (sur Arch: `sudo pacman -S python-pyserial`)

### Build & Flash

1. Brancher la carte en USB
2. Vérifier le port (`ls /dev/ttyACM*`) et mettre à jour `upload_port` / `monitor_port` dans [platformio.ini](platformio.ini)
3. Compiler + flasher:

	- `platformio run --target upload`

Le script [scripts/pre_build.py](scripts/pre_build.py) lance automatiquement la conversion HTML→LVGL avant compilation.

Alternative (recommandé): utiliser [start.sh](start.sh) pour **générer l’UI** puis **uploader** en une seule commande:

	- `./start.sh`

Options:

	- `PIO_ENV=esp32s3box ./start.sh`
	- `PIO_PORT=/dev/ttyACM0 ./start.sh`

### Lancer le contrôle volume PC

1. Fermer le moniteur série PlatformIO (sinon le port peut être “busy”)
2. Lancer:

	- `python3 pc_volume_control.py`

3. Toucher **+** / **-** sur l’écran.

### Notes / Dépannage

- Si le port change (ex: `/dev/ttyACM0` ↔ `/dev/ttyACM1`), il faut mettre à jour [platformio.ini](platformio.ini) et/ou [pc_volume_control.py](pc_volume_control.py).
- Les grosses polices LVGL sont activées dans [lib/lv_conf.h](lib/lv_conf.h) (Montserrat 48) pour que “+ / -” soient lisibles.
- Ce dépôt embarque des bibliothèques tierces dans [lib/](lib/) avec leurs fichiers de licence respectifs.

---

## English

### Overview

This repository is a **PlatformIO (Arduino)** project for the **Waveshare ESP32‑S3 Touch LCD 4.3" (800×480)** using **LVGL v8.3.x**.

Goal: describe a very simple UI using **HTML/CSS/JS**, then **auto‑convert it to LVGL C** at build time.

Included demo: two big touch buttons **“+”** and **“-”** that send serial commands (`VOL_UP` / `VOL_DOWN`) to the host PC.

On the PC side, a Python script listens on the serial port and adjusts the system volume (Linux / PipeWire / PulseAudio via `pactl`). Volume is **clamped to 0–100%**.

### Key paths

- “Web” UI: [data/index.html](data/index.html), [data/style.css](data/style.css), [data/script.js](data/script.js)
- HTML→LVGL converter: [scripts/html_to_lvgl.py](scripts/html_to_lvgl.py)
- Generated output: [src/generated/ui_generated.c](src/generated/ui_generated.c), [src/generated/ui_generated.h](src/generated/ui_generated.h)
- Firmware entry: [src/main.cpp](src/main.cpp)
- PC volume controller: [pc_volume_control.py](pc_volume_control.py)

### Requirements

- PlatformIO (VS Code) or `platformio` CLI
- Linux: `pactl` (PipeWire/PulseAudio). Optional fallback: `amixer`
- Python 3 + `pyserial` (Arch: `sudo pacman -S python-pyserial`)

### Build & Upload

1. Plug the board via USB
2. Check the device path (`ls /dev/ttyACM*`) and update `upload_port` / `monitor_port` in [platformio.ini](platformio.ini)
3. Upload:

	- `platformio run --target upload`

[scripts/pre_build.py](scripts/pre_build.py) runs the HTML→LVGL conversion before compilation.

Alternative (recommended): use [start.sh](start.sh) to **regenerate the UI** and **upload** in one shot:

	- `./start.sh`

Options:

	- `PIO_ENV=esp32s3box ./start.sh`
	- `PIO_PORT=/dev/ttyACM0 ./start.sh`

### Run PC listener

1. Close PlatformIO serial monitor (otherwise the port may be busy)
2. Run:

	- `python3 pc_volume_control.py`

3. Tap **+** / **-** on the display.

---

## Español

### Descripción

Este repositorio contiene un proyecto **PlatformIO (Arduino)** para la **Waveshare ESP32‑S3 Touch LCD 4.3" (800×480)** con **LVGL v8.3.x**.

Objetivo: definir una interfaz simple con **HTML/CSS/JS** y **convertirla automáticamente a LVGL C** durante el build.

Demo incluida: dos botones táctiles grandes **“+”** y **“-”** que envían comandos por serie (`VOL_UP` / `VOL_DOWN`) al PC.

En el PC, un script Python escucha el puerto serie y ajusta el volumen (Linux / PipeWire / PulseAudio con `pactl`). El volumen queda **limitado a 0–100%**.

### Rutas importantes

- UI “web”: [data/index.html](data/index.html), [data/style.css](data/style.css), [data/script.js](data/script.js)
- Convertidor HTML→LVGL: [scripts/html_to_lvgl.py](scripts/html_to_lvgl.py)
- Archivos generados: [src/generated/ui_generated.c](src/generated/ui_generated.c), [src/generated/ui_generated.h](src/generated/ui_generated.h)
- Firmware principal: [src/main.cpp](src/main.cpp)
- Control de volumen (PC): [pc_volume_control.py](pc_volume_control.py)

### Compilar y flashear

1. Conecta la placa por USB
2. Verifica el puerto (`ls /dev/ttyACM*`) y actualiza `upload_port` / `monitor_port` en [platformio.ini](platformio.ini)
3. Subir firmware:

	- `platformio run --target upload`

Alternativa (recomendado): usa [start.sh](start.sh) para **regenerar la UI** y **subir** el firmware en un solo comando:

	- `./start.sh`

Opciones:

	- `PIO_ENV=esp32s3box ./start.sh`
	- `PIO_PORT=/dev/ttyACM0 ./start.sh`

### Ejecutar el script en el PC

1. Cierra el monitor serie de PlatformIO (si no, el puerto puede estar ocupado)
2. Ejecuta:

	- `python3 pc_volume_control.py`

3. Pulsa **+** / **-** en la pantalla.

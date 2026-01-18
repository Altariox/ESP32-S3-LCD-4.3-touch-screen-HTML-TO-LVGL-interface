// Stream Deck - Page 1: Apps, Page 2: Info + Volume

// ========== PAGE 1: APP LAUNCHERS ==========
function openLibreOffice() {
    serialSend("APP_LIBREOFFICE");
}

function openFirefox() {
    serialSend("APP_FIREFOX");
}

function openPrusaSlicer() {
    serialSend("APP_PRUSA_SLICER");
}

function openPrismLauncher() {
    serialSend("APP_PRISM_LAUNCHER");
}

function openVSCode() {
    serialSend("APP_VSCODE");
}

function openTerminal() {
    serialSend("APP_TERMINAL");
}

// ========== PAGE 2: VOLUME CONTROLS ==========
function volUp() {
    serialSend("VOL_UP");
}

function volDown() {
    serialSend("VOL_DOWN");
}

function toggleMute() {
    serialSend("VOL_MUTE");
}

function init() {
    // Ready
}

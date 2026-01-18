// Stream Deck - sends serial commands to PC

function openDiscord() {
    serialSend("APP_DISCORD");
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

function init() {
    // Ready
}

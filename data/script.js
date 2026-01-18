// Stream Deck - sends serial commands to PC

function openDiscord() {
    serialSend("APP_DISCORD");
}

function openBrave() {
    serialSend("APP_BRAVE");
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

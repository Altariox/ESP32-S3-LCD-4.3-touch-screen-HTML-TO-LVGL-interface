// Volume Control - sends serial commands to PC

function volumeUp() {
    serialSend("VOL_UP");
}

function volumeDown() {
    serialSend("VOL_DOWN");
}

function init() {
    // Ready
}

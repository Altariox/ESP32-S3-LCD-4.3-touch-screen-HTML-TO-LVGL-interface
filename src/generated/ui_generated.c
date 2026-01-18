// Auto-generated from HTML/CSS/JS
// Do not edit manually!

#include "ui_generated.h"
#include <stdio.h>
#include <string.h>

// UI Elements
static lv_obj_t* ui_title;
static lv_obj_t* ui_elem_7;
static lv_obj_t* ui_btn_discord;
static lv_obj_t* ui_btn_brave;
static lv_obj_t* ui_btn_prusa;
static lv_obj_t* ui_btn_prism;
static lv_obj_t* ui_btn_vscode;
static lv_obj_t* ui_btn_terminal;

// Function prototypes
static void openDiscord(void);
static void openBrave(void);
static void openPrusaSlicer(void);
static void openPrismLauncher(void);
static void openVSCode(void);
static void openTerminal(void);
static void init(void);

// Event handlers
static void event_btn_discord(lv_event_t* e) {
    openDiscord();
}
static void event_btn_brave(lv_event_t* e) {
    openBrave();
}
static void event_btn_prusa(lv_event_t* e) {
    openPrusaSlicer();
}
static void event_btn_prism(lv_event_t* e) {
    openPrismLauncher();
}
static void event_btn_vscode(lv_event_t* e) {
    openVSCode();
}
static void event_btn_terminal(lv_event_t* e) {
    openTerminal();
}

// Converted JS functions
static void openDiscord(void) {
    serial_send("APP_DISCORD");
}

static void openBrave(void) {
    serial_send("APP_BRAVE");
}

static void openPrusaSlicer(void) {
    serial_send("APP_PRUSA_SLICER");
}

static void openPrismLauncher(void) {
    serial_send("APP_PRISM_LAUNCHER");
}

static void openVSCode(void) {
    serial_send("APP_VSCODE");
}

static void openTerminal(void) {
    serial_send("APP_TERMINAL");
}

static void init(void) {
    // Ready
}

void ui_generated_init(lv_obj_t* parent) {
    // Set screen background
    lv_obj_set_style_bg_color(parent, lv_color_hex(0x0A0A0F), 0);

    // label#title
    ui_title = lv_label_create(parent);
    lv_label_set_text(ui_title, "Stream Deck");
    lv_obj_align(ui_title, LV_ALIGN_TOP_MID, 0, 40);
    lv_obj_set_style_text_color(ui_title, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_text_font(ui_title, &lv_font_montserrat_30, 0);

    // div#elem_7
    ui_elem_7 = lv_obj_create(parent);
    lv_obj_clear_flag(ui_elem_7, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_width(ui_elem_7, 740);
    lv_obj_set_height(ui_elem_7, 340);
    lv_obj_align(ui_elem_7, LV_ALIGN_TOP_MID, 0, 100);
    lv_obj_set_style_bg_color(ui_elem_7, lv_color_hex(0x0A0A0F), 0);
    lv_obj_set_style_bg_opa(ui_elem_7, LV_OPA_COVER, 0);
    lv_obj_set_style_pad_all(ui_elem_7, 20, 0);

    // button#btn-discord
    ui_btn_discord = lv_btn_create(ui_elem_7);
    lv_obj_t* ui_btn_discord_label = lv_label_create(ui_btn_discord);
    lv_label_set_text(ui_btn_discord_label, "Discord");
    lv_obj_center(ui_btn_discord_label);
    lv_obj_add_event_cb(ui_btn_discord, event_btn_discord, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_discord, 340);
    lv_obj_set_height(ui_btn_discord, 90);
    lv_obj_set_pos(ui_btn_discord, 20, 20);
    lv_obj_set_style_bg_color(ui_btn_discord, lv_color_hex(0x5865F2), 0);
    lv_obj_set_style_bg_opa(ui_btn_discord, LV_OPA_COVER, 0);
    lv_obj_set_style_text_color(ui_btn_discord, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_text_color(ui_btn_discord_label, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_radius(ui_btn_discord, 24, 0);
    lv_obj_set_style_text_font(ui_btn_discord, &lv_font_montserrat_30, 0);
    lv_obj_set_style_text_font(ui_btn_discord_label, &lv_font_montserrat_30, 0);

    // button#btn-brave
    ui_btn_brave = lv_btn_create(ui_elem_7);
    lv_obj_t* ui_btn_brave_label = lv_label_create(ui_btn_brave);
    lv_label_set_text(ui_btn_brave_label, "Brave");
    lv_obj_center(ui_btn_brave_label);
    lv_obj_add_event_cb(ui_btn_brave, event_btn_brave, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_brave, 340);
    lv_obj_set_height(ui_btn_brave, 90);
    lv_obj_set_pos(ui_btn_brave, 380, 20);
    lv_obj_set_style_bg_color(ui_btn_brave, lv_color_hex(0xFB542B), 0);
    lv_obj_set_style_bg_opa(ui_btn_brave, LV_OPA_COVER, 0);
    lv_obj_set_style_text_color(ui_btn_brave, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_text_color(ui_btn_brave_label, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_radius(ui_btn_brave, 24, 0);
    lv_obj_set_style_text_font(ui_btn_brave, &lv_font_montserrat_30, 0);
    lv_obj_set_style_text_font(ui_btn_brave_label, &lv_font_montserrat_30, 0);

    // button#btn-prusa
    ui_btn_prusa = lv_btn_create(ui_elem_7);
    lv_obj_t* ui_btn_prusa_label = lv_label_create(ui_btn_prusa);
    lv_label_set_text(ui_btn_prusa_label, "PrusaSlicer");
    lv_obj_center(ui_btn_prusa_label);
    lv_obj_add_event_cb(ui_btn_prusa, event_btn_prusa, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_prusa, 340);
    lv_obj_set_height(ui_btn_prusa, 90);
    lv_obj_set_pos(ui_btn_prusa, 20, 130);
    lv_obj_set_style_bg_color(ui_btn_prusa, lv_color_hex(0xFF7F2A), 0);
    lv_obj_set_style_bg_opa(ui_btn_prusa, LV_OPA_COVER, 0);
    lv_obj_set_style_text_color(ui_btn_prusa, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_text_color(ui_btn_prusa_label, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_radius(ui_btn_prusa, 24, 0);
    lv_obj_set_style_text_font(ui_btn_prusa, &lv_font_montserrat_30, 0);
    lv_obj_set_style_text_font(ui_btn_prusa_label, &lv_font_montserrat_30, 0);

    // button#btn-prism
    ui_btn_prism = lv_btn_create(ui_elem_7);
    lv_obj_t* ui_btn_prism_label = lv_label_create(ui_btn_prism);
    lv_label_set_text(ui_btn_prism_label, "Prism");
    lv_obj_center(ui_btn_prism_label);
    lv_obj_add_event_cb(ui_btn_prism, event_btn_prism, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_prism, 340);
    lv_obj_set_height(ui_btn_prism, 90);
    lv_obj_set_pos(ui_btn_prism, 380, 130);
    lv_obj_set_style_bg_color(ui_btn_prism, lv_color_hex(0x2ECC71), 0);
    lv_obj_set_style_bg_opa(ui_btn_prism, LV_OPA_COVER, 0);
    lv_obj_set_style_text_color(ui_btn_prism, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_text_color(ui_btn_prism_label, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_radius(ui_btn_prism, 24, 0);
    lv_obj_set_style_text_font(ui_btn_prism, &lv_font_montserrat_30, 0);
    lv_obj_set_style_text_font(ui_btn_prism_label, &lv_font_montserrat_30, 0);

    // button#btn-vscode
    ui_btn_vscode = lv_btn_create(ui_elem_7);
    lv_obj_t* ui_btn_vscode_label = lv_label_create(ui_btn_vscode);
    lv_label_set_text(ui_btn_vscode_label, "VS Code");
    lv_obj_center(ui_btn_vscode_label);
    lv_obj_add_event_cb(ui_btn_vscode, event_btn_vscode, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_vscode, 340);
    lv_obj_set_height(ui_btn_vscode, 90);
    lv_obj_set_pos(ui_btn_vscode, 20, 240);
    lv_obj_set_style_bg_color(ui_btn_vscode, lv_color_hex(0x007ACC), 0);
    lv_obj_set_style_bg_opa(ui_btn_vscode, LV_OPA_COVER, 0);
    lv_obj_set_style_text_color(ui_btn_vscode, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_text_color(ui_btn_vscode_label, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_radius(ui_btn_vscode, 24, 0);
    lv_obj_set_style_text_font(ui_btn_vscode, &lv_font_montserrat_30, 0);
    lv_obj_set_style_text_font(ui_btn_vscode_label, &lv_font_montserrat_30, 0);

    // button#btn-terminal
    ui_btn_terminal = lv_btn_create(ui_elem_7);
    lv_obj_t* ui_btn_terminal_label = lv_label_create(ui_btn_terminal);
    lv_label_set_text(ui_btn_terminal_label, "Terminal");
    lv_obj_center(ui_btn_terminal_label);
    lv_obj_add_event_cb(ui_btn_terminal, event_btn_terminal, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_terminal, 340);
    lv_obj_set_height(ui_btn_terminal, 90);
    lv_obj_set_pos(ui_btn_terminal, 380, 240);
    lv_obj_set_style_bg_color(ui_btn_terminal, lv_color_hex(0x111827), 0);
    lv_obj_set_style_bg_opa(ui_btn_terminal, LV_OPA_COVER, 0);
    lv_obj_set_style_text_color(ui_btn_terminal, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_text_color(ui_btn_terminal_label, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_radius(ui_btn_terminal, 24, 0);
    lv_obj_set_style_text_font(ui_btn_terminal, &lv_font_montserrat_30, 0);
    lv_obj_set_style_text_font(ui_btn_terminal_label, &lv_font_montserrat_30, 0);

    // Call init function
    init();
}
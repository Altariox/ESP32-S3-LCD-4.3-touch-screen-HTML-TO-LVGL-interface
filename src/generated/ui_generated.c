// Auto-generated from HTML/CSS/JS
// Do not edit manually!

#include "ui_generated.h"
#include "ui_assets.h"
#include <stdio.h>
#include <string.h>

// UI Elements
static lv_obj_t* ui_elem_6;
static lv_obj_t* ui_btn_discord;
static lv_obj_t* ui_elem_8;
static lv_obj_t* ui_btn_firefox;
static lv_obj_t* ui_elem_10;
static lv_obj_t* ui_btn_prusa;
static lv_obj_t* ui_elem_12;
static lv_obj_t* ui_btn_prism;
static lv_obj_t* ui_elem_14;
static lv_obj_t* ui_btn_vscode;
static lv_obj_t* ui_elem_16;
static lv_obj_t* ui_btn_terminal;
static lv_obj_t* ui_elem_18;

// Function prototypes
static void openDiscord(void);
static void openFirefox(void);
static void openPrusaSlicer(void);
static void openPrismLauncher(void);
static void openVSCode(void);
static void openTerminal(void);
static void init(void);

// Event handlers
static void event_btn_discord(lv_event_t* e) {
    openDiscord();
}
static void event_btn_firefox(lv_event_t* e) {
    openFirefox();
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

static void openFirefox(void) {
    serial_send("APP_FIREFOX");
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
    lv_obj_set_style_bg_color(parent, lv_color_hex(0x1A1A2E), 0);

    // div#elem_6
    ui_elem_6 = lv_obj_create(parent);
    lv_obj_clear_flag(ui_elem_6, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_width(ui_elem_6, 780);
    lv_obj_set_height(ui_elem_6, 460);
    lv_obj_center(ui_elem_6);
    lv_obj_set_style_bg_color(ui_elem_6, lv_color_hex(0x1A1A2E), 0);
    lv_obj_set_style_bg_opa(ui_elem_6, LV_OPA_COVER, 0);
    lv_obj_set_style_pad_all(ui_elem_6, 0, 0);

    // button#btn-discord
    ui_btn_discord = lv_btn_create(ui_elem_6);
    lv_obj_add_event_cb(ui_btn_discord, event_btn_discord, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_discord, 240);
    lv_obj_set_height(ui_btn_discord, 200);
    lv_obj_set_pos(ui_btn_discord, 20, 20);
    lv_obj_set_style_bg_color(ui_btn_discord, lv_color_hex(0x5865F2), 0);
    lv_obj_set_style_bg_opa(ui_btn_discord, LV_OPA_COVER, 0);
    lv_obj_set_style_radius(ui_btn_discord, 24, 0);
    lv_obj_set_style_pad_all(ui_btn_discord, 0, 0);

    // img#elem_8
    ui_elem_8 = lv_img_create(ui_btn_discord);
    lv_img_set_src(ui_elem_8, &ui_img_discord);
    lv_obj_center(ui_elem_8);

    // button#btn-firefox
    ui_btn_firefox = lv_btn_create(ui_elem_6);
    lv_obj_add_event_cb(ui_btn_firefox, event_btn_firefox, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_firefox, 240);
    lv_obj_set_height(ui_btn_firefox, 200);
    lv_obj_set_pos(ui_btn_firefox, 270, 20);
    lv_obj_set_style_bg_color(ui_btn_firefox, lv_color_hex(0xFF7139), 0);
    lv_obj_set_style_bg_opa(ui_btn_firefox, LV_OPA_COVER, 0);
    lv_obj_set_style_radius(ui_btn_firefox, 24, 0);
    lv_obj_set_style_pad_all(ui_btn_firefox, 0, 0);

    // img#elem_10
    ui_elem_10 = lv_img_create(ui_btn_firefox);
    lv_img_set_src(ui_elem_10, &ui_img_firefox);
    lv_obj_center(ui_elem_10);

    // button#btn-prusa
    ui_btn_prusa = lv_btn_create(ui_elem_6);
    lv_obj_add_event_cb(ui_btn_prusa, event_btn_prusa, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_prusa, 240);
    lv_obj_set_height(ui_btn_prusa, 200);
    lv_obj_set_pos(ui_btn_prusa, 520, 20);
    lv_obj_set_style_bg_color(ui_btn_prusa, lv_color_hex(0x585858), 0);
    lv_obj_set_style_bg_opa(ui_btn_prusa, LV_OPA_COVER, 0);
    lv_obj_set_style_radius(ui_btn_prusa, 24, 0);
    lv_obj_set_style_pad_all(ui_btn_prusa, 0, 0);

    // img#elem_12
    ui_elem_12 = lv_img_create(ui_btn_prusa);
    lv_img_set_src(ui_elem_12, &ui_img_prusa);
    lv_obj_center(ui_elem_12);

    // button#btn-prism
    ui_btn_prism = lv_btn_create(ui_elem_6);
    lv_obj_add_event_cb(ui_btn_prism, event_btn_prism, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_prism, 240);
    lv_obj_set_height(ui_btn_prism, 200);
    lv_obj_set_pos(ui_btn_prism, 20, 240);
    lv_obj_set_style_bg_color(ui_btn_prism, lv_color_hex(0x2ECC71), 0);
    lv_obj_set_style_bg_opa(ui_btn_prism, LV_OPA_COVER, 0);
    lv_obj_set_style_radius(ui_btn_prism, 24, 0);
    lv_obj_set_style_pad_all(ui_btn_prism, 0, 0);

    // img#elem_14
    ui_elem_14 = lv_img_create(ui_btn_prism);
    lv_img_set_src(ui_elem_14, &ui_img_prismlauncher);
    lv_obj_center(ui_elem_14);

    // button#btn-vscode
    ui_btn_vscode = lv_btn_create(ui_elem_6);
    lv_obj_add_event_cb(ui_btn_vscode, event_btn_vscode, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_vscode, 240);
    lv_obj_set_height(ui_btn_vscode, 200);
    lv_obj_set_pos(ui_btn_vscode, 270, 240);
    lv_obj_set_style_bg_color(ui_btn_vscode, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_bg_opa(ui_btn_vscode, LV_OPA_COVER, 0);
    lv_obj_set_style_radius(ui_btn_vscode, 24, 0);
    lv_obj_set_style_pad_all(ui_btn_vscode, 0, 0);

    // img#elem_16
    ui_elem_16 = lv_img_create(ui_btn_vscode);
    lv_img_set_src(ui_elem_16, &ui_img_vscode);
    lv_obj_center(ui_elem_16);

    // button#btn-terminal
    ui_btn_terminal = lv_btn_create(ui_elem_6);
    lv_obj_add_event_cb(ui_btn_terminal, event_btn_terminal, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_terminal, 240);
    lv_obj_set_height(ui_btn_terminal, 200);
    lv_obj_set_pos(ui_btn_terminal, 520, 240);
    lv_obj_set_style_bg_color(ui_btn_terminal, lv_color_hex(0x2C3E50), 0);
    lv_obj_set_style_bg_opa(ui_btn_terminal, LV_OPA_COVER, 0);
    lv_obj_set_style_radius(ui_btn_terminal, 24, 0);
    lv_obj_set_style_pad_all(ui_btn_terminal, 0, 0);

    // img#elem_18
    ui_elem_18 = lv_img_create(ui_btn_terminal);
    lv_img_set_src(ui_elem_18, &ui_img_terminal);
    lv_obj_center(ui_elem_18);

    // Call init function
    init();
}
// Auto-generated from HTML/CSS/JS
// Do not edit manually!

#include "ui_generated.h"
#include "ui_assets.h"
#include <stdio.h>
#include <string.h>

// UI Elements
static lv_obj_t* ui_elem_6;
static lv_obj_t* ui_btn_libreoffice;
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
static lv_obj_t* ui_elem_20;
static lv_obj_t* ui_elem_21;
static lv_obj_t* ui_btn_vol_up;
static lv_obj_t* ui_vol_up_icon;
static lv_obj_t* ui_vol_up_text;
static lv_obj_t* ui_btn_mute;
static lv_obj_t* ui_mute_icon;
static lv_obj_t* ui_mute_text;
static lv_obj_t* ui_btn_vol_down;
static lv_obj_t* ui_vol_down_icon;
static lv_obj_t* ui_vol_down_text;
lv_obj_t* ui_time_display = NULL;
lv_obj_t* ui_date_display = NULL;
static lv_obj_t* ui_elem_33;
lv_obj_t* ui_temp_value = NULL;
static lv_obj_t* ui_temp_unit;
lv_obj_t* ui_weather_desc = NULL;
lv_obj_t* ui_humidity = NULL;
lv_obj_t* ui_wind = NULL;

// Function prototypes
static void openLibreOffice(void);
static void openFirefox(void);
static void openPrusaSlicer(void);
static void openPrismLauncher(void);
static void openVSCode(void);
static void openTerminal(void);
static void volUp(void);
static void volDown(void);
static void toggleMute(void);
static void init(void);

// Event handlers
static void event_btn_libreoffice(lv_event_t* e) {
    openLibreOffice();
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
static void event_btn_vol_up(lv_event_t* e) {
    volUp();
}
static void event_btn_mute(lv_event_t* e) {
    toggleMute();
}
static void event_btn_vol_down(lv_event_t* e) {
    volDown();
}

// Converted JS functions
static void openLibreOffice(void) {
    serial_send("APP_LIBREOFFICE");
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

static void volUp(void) {
    serial_send("VOL_UP");
}

static void volDown(void) {
    serial_send("VOL_DOWN");
}

static void toggleMute(void) {
    serial_send("VOL_MUTE");
}

static void init(void) {
    // Ready
}

void ui_generated_init(lv_obj_t* parent) {
    // Create tileview for swipeable pages
    static lv_obj_t* tileview;
    tileview = lv_tileview_create(parent);
    lv_obj_set_size(tileview, 800, 480);
    lv_obj_set_style_bg_opa(tileview, LV_OPA_TRANSP, 0);

    // Tile 0: page-apps
    static lv_obj_t* tile_page_apps;
    tile_page_apps = lv_tileview_add_tile(tileview, 0, 0, LV_DIR_HOR);
    lv_obj_set_style_bg_color(tile_page_apps, lv_color_hex(0x1A1A2E), 0);
    lv_obj_set_style_bg_opa(tile_page_apps, LV_OPA_COVER, 0);

    // Tile 1: page-info
    static lv_obj_t* tile_page_info;
    tile_page_info = lv_tileview_add_tile(tileview, 1, 0, LV_DIR_HOR);
    lv_obj_set_style_bg_color(tile_page_info, lv_color_hex(0x0D0D12), 0);
    lv_obj_set_style_bg_opa(tile_page_info, LV_OPA_COVER, 0);

    // div#elem_6
    ui_elem_6 = lv_obj_create(tile_page_apps);
    lv_obj_clear_flag(ui_elem_6, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_width(ui_elem_6, 780);
    lv_obj_set_height(ui_elem_6, 460);
    lv_obj_center(ui_elem_6);
    lv_obj_set_style_bg_color(ui_elem_6, lv_color_hex(0x1A1A2E), 0);
    lv_obj_set_style_bg_opa(ui_elem_6, LV_OPA_COVER, 0);
    lv_obj_set_style_pad_all(ui_elem_6, 0, 0);

    // button#btn-libreoffice
    ui_btn_libreoffice = lv_btn_create(ui_elem_6);
    lv_obj_add_event_cb(ui_btn_libreoffice, event_btn_libreoffice, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_libreoffice, 240);
    lv_obj_set_height(ui_btn_libreoffice, 200);
    lv_obj_set_pos(ui_btn_libreoffice, 20, 20);
    lv_obj_set_style_bg_color(ui_btn_libreoffice, lv_color_hex(0x18A303), 0);
    lv_obj_set_style_bg_opa(ui_btn_libreoffice, LV_OPA_COVER, 0);
    lv_obj_set_style_radius(ui_btn_libreoffice, 24, 0);
    lv_obj_set_style_pad_all(ui_btn_libreoffice, 0, 0);

    // img#elem_8
    ui_elem_8 = lv_img_create(ui_btn_libreoffice);
    lv_img_set_src(ui_elem_8, &ui_img_libreoffice);
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
    lv_obj_set_style_bg_color(ui_btn_vscode, lv_color_hex(0x1E1E1E), 0);
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

    // div#elem_20
    ui_elem_20 = lv_obj_create(tile_page_info);
    lv_obj_clear_flag(ui_elem_20, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_width(ui_elem_20, 800);
    lv_obj_set_height(ui_elem_20, 480);
    lv_obj_set_pos(ui_elem_20, 0, 0);
    lv_obj_set_style_bg_color(ui_elem_20, lv_color_hex(0x0D0D12), 0);
    lv_obj_set_style_bg_opa(ui_elem_20, LV_OPA_COVER, 0);
    lv_obj_set_style_pad_all(ui_elem_20, 0, 0);

    // div#elem_21
    ui_elem_21 = lv_obj_create(ui_elem_20);
    lv_obj_clear_flag(ui_elem_21, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_width(ui_elem_21, 120);
    lv_obj_set_height(ui_elem_21, 450);
    lv_obj_set_pos(ui_elem_21, 10, 15);
    lv_obj_set_style_bg_color(ui_elem_21, lv_color_hex(0x1A1A22), 0);
    lv_obj_set_style_bg_opa(ui_elem_21, LV_OPA_COVER, 0);
    lv_obj_set_style_radius(ui_elem_21, 20, 0);
    lv_obj_set_style_pad_all(ui_elem_21, 0, 0);

    // button#btn-vol-up
    ui_btn_vol_up = lv_btn_create(ui_elem_21);
    lv_obj_add_event_cb(ui_btn_vol_up, event_btn_vol_up, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_vol_up, 100);
    lv_obj_set_height(ui_btn_vol_up, 100);
    lv_obj_set_pos(ui_btn_vol_up, 10, 15);
    lv_obj_set_style_bg_color(ui_btn_vol_up, lv_color_hex(0x252530), 0);
    lv_obj_set_style_bg_opa(ui_btn_vol_up, LV_OPA_COVER, 0);
    lv_obj_set_style_radius(ui_btn_vol_up, 50, 0);
    lv_obj_set_style_pad_all(ui_btn_vol_up, 0, 0);

    // label#vol-up-icon
    ui_vol_up_icon = lv_label_create(ui_btn_vol_up);
    lv_label_set_text(ui_vol_up_icon, "+");
    lv_obj_center(ui_vol_up_icon);
    lv_obj_set_style_text_color(ui_vol_up_icon, lv_color_hex(0x3498DB), 0);
    lv_obj_set_style_text_font(ui_vol_up_icon, &lv_font_montserrat_44, 0);

    // label#vol-up-text
    ui_vol_up_text = lv_label_create(ui_elem_21);
    lv_label_set_text(ui_vol_up_text, "Vol+");
    lv_obj_align(ui_vol_up_text, LV_ALIGN_TOP_MID, 0, 125);
    lv_obj_set_style_text_color(ui_vol_up_text, lv_color_hex(0x666666), 0);
    lv_obj_set_style_text_font(ui_vol_up_text, &lv_font_montserrat_14, 0);

    // button#btn-mute
    ui_btn_mute = lv_btn_create(ui_elem_21);
    lv_obj_add_event_cb(ui_btn_mute, event_btn_mute, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_mute, 100);
    lv_obj_set_height(ui_btn_mute, 100);
    lv_obj_set_pos(ui_btn_mute, 10, 165);
    lv_obj_set_style_bg_color(ui_btn_mute, lv_color_hex(0x252530), 0);
    lv_obj_set_style_bg_opa(ui_btn_mute, LV_OPA_COVER, 0);
    lv_obj_set_style_radius(ui_btn_mute, 20, 0);
    lv_obj_set_style_pad_all(ui_btn_mute, 0, 0);

    // label#mute-icon
    ui_mute_icon = lv_label_create(ui_btn_mute);
    lv_label_set_text(ui_mute_icon, "M");
    lv_obj_center(ui_mute_icon);
    lv_obj_set_style_text_color(ui_mute_icon, lv_color_hex(0xE74C3C), 0);
    lv_obj_set_style_text_font(ui_mute_icon, &lv_font_montserrat_40, 0);

    // label#mute-text
    ui_mute_text = lv_label_create(ui_elem_21);
    lv_label_set_text(ui_mute_text, "Mute");
    lv_obj_align(ui_mute_text, LV_ALIGN_TOP_MID, 0, 275);
    lv_obj_set_style_text_color(ui_mute_text, lv_color_hex(0x666666), 0);
    lv_obj_set_style_text_font(ui_mute_text, &lv_font_montserrat_14, 0);

    // button#btn-vol-down
    ui_btn_vol_down = lv_btn_create(ui_elem_21);
    lv_obj_add_event_cb(ui_btn_vol_down, event_btn_vol_down, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_vol_down, 100);
    lv_obj_set_height(ui_btn_vol_down, 100);
    lv_obj_set_pos(ui_btn_vol_down, 10, 315);
    lv_obj_set_style_bg_color(ui_btn_vol_down, lv_color_hex(0x252530), 0);
    lv_obj_set_style_bg_opa(ui_btn_vol_down, LV_OPA_COVER, 0);
    lv_obj_set_style_radius(ui_btn_vol_down, 50, 0);
    lv_obj_set_style_pad_all(ui_btn_vol_down, 0, 0);

    // label#vol-down-icon
    ui_vol_down_icon = lv_label_create(ui_btn_vol_down);
    lv_label_set_text(ui_vol_down_icon, "-");
    lv_obj_center(ui_vol_down_icon);
    lv_obj_set_style_text_color(ui_vol_down_icon, lv_color_hex(0x3498DB), 0);
    lv_obj_set_style_text_font(ui_vol_down_icon, &lv_font_montserrat_44, 0);

    // label#vol-down-text
    ui_vol_down_text = lv_label_create(ui_elem_21);
    lv_label_set_text(ui_vol_down_text, "Vol-");
    lv_obj_align(ui_vol_down_text, LV_ALIGN_TOP_MID, 0, 420);
    lv_obj_set_style_text_color(ui_vol_down_text, lv_color_hex(0x666666), 0);
    lv_obj_set_style_text_font(ui_vol_down_text, &lv_font_montserrat_14, 0);

    // label#time-display
    ui_time_display = lv_label_create(ui_elem_20);
    lv_label_set_text(ui_time_display, "10:45");
    lv_obj_set_pos(ui_time_display, 400, 150);
    lv_obj_set_style_text_color(ui_time_display, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_text_font(ui_time_display, &lv_font_montserrat_44, 0);

    // label#date-display
    ui_date_display = lv_label_create(ui_elem_20);
    lv_label_set_text(ui_date_display, "Samedi 18 Janvier 2026");
    lv_obj_set_pos(ui_date_display, 250, 240);
    lv_obj_set_style_text_color(ui_date_display, lv_color_hex(0x4ECDC4), 0);
    lv_obj_set_style_text_font(ui_date_display, &lv_font_montserrat_40, 0);

    // div#elem_33
    ui_elem_33 = lv_obj_create(ui_elem_20);
    lv_obj_clear_flag(ui_elem_33, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_width(ui_elem_33, 650);
    lv_obj_set_height(ui_elem_33, 90);
    lv_obj_set_pos(ui_elem_33, 140, 380);
    lv_obj_set_style_bg_color(ui_elem_33, lv_color_hex(0x1A1A22), 0);
    lv_obj_set_style_bg_opa(ui_elem_33, LV_OPA_COVER, 0);
    lv_obj_set_style_radius(ui_elem_33, 20, 0);
    lv_obj_set_style_pad_all(ui_elem_33, 0, 0);

    // label#temp-value
    ui_temp_value = lv_label_create(ui_elem_33);
    lv_label_set_text(ui_temp_value, "21");
    lv_obj_align(ui_temp_value, LV_ALIGN_LEFT_MID, 30, 0);
    lv_obj_set_style_text_color(ui_temp_value, lv_color_hex(0xE74C3C), 0);
    lv_obj_set_style_text_font(ui_temp_value, &lv_font_montserrat_44, 0);

    // label#temp-unit
    ui_temp_unit = lv_label_create(ui_elem_33);
    lv_label_set_text(ui_temp_unit, "C");
    lv_obj_set_pos(ui_temp_unit, 100, 15);
    lv_obj_set_style_text_color(ui_temp_unit, lv_color_hex(0xE74C3C), 0);
    lv_obj_set_style_text_font(ui_temp_unit, &lv_font_montserrat_30, 0);

    // label#weather-desc
    ui_weather_desc = lv_label_create(ui_elem_33);
    lv_label_set_text(ui_weather_desc, "Nuageux");
    lv_obj_align(ui_weather_desc, LV_ALIGN_LEFT_MID, 160, 0);
    lv_obj_set_style_text_color(ui_weather_desc, lv_color_hex(0xAAAAAA), 0);
    lv_obj_set_style_text_font(ui_weather_desc, &lv_font_montserrat_30, 0);

    // label#humidity
    ui_humidity = lv_label_create(ui_elem_33);
    lv_label_set_text(ui_humidity, "55%");
    lv_obj_align(ui_humidity, LV_ALIGN_LEFT_MID, 380, 0);
    lv_obj_set_style_text_color(ui_humidity, lv_color_hex(0x3498DB), 0);
    lv_obj_set_style_text_font(ui_humidity, &lv_font_montserrat_30, 0);

    // label#wind
    ui_wind = lv_label_create(ui_elem_33);
    lv_label_set_text(ui_wind, "15 km/h");
    lv_obj_align(ui_wind, LV_ALIGN_LEFT_MID, 510, 0);
    lv_obj_set_style_text_color(ui_wind, lv_color_hex(0xAAAAAA), 0);
    lv_obj_set_style_text_font(ui_wind, &lv_font_montserrat_30, 0);

    // Call init function
    init();
}
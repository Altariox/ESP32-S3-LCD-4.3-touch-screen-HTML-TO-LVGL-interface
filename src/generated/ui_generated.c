// Auto-generated from HTML/CSS/JS
// Do not edit manually!

#include "ui_generated.h"
#include <stdio.h>
#include <string.h>

// UI Elements
static lv_obj_t* ui_title;
static lv_obj_t* ui_elem_7;
static lv_obj_t* ui_btn_minus;
static lv_obj_t* ui_btn_plus;

// Function prototypes
static void volumeUp(void);
static void volumeDown(void);
static void init(void);

// Event handlers
static void event_btn_minus(lv_event_t* e) {
    volumeDown();
}
static void event_btn_plus(lv_event_t* e) {
    volumeUp();
}

// Converted JS functions
static void volumeUp(void) {
    serial_send("VOL_UP");
}

static void volumeDown(void) {
    serial_send("VOL_DOWN");
}

static void init(void) {
    // Ready
}

void ui_generated_init(lv_obj_t* parent) {
    // Set screen background
    lv_obj_set_style_bg_color(parent, lv_color_hex(0x0A0A0F), 0);

    // label#title
    ui_title = lv_label_create(parent);
    lv_label_set_text(ui_title, "Volume");
    lv_obj_align(ui_title, LV_ALIGN_TOP_MID, 0, 40);
    lv_obj_set_style_text_color(ui_title, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_text_font(ui_title, &lv_font_montserrat_30, 0);

    // div#elem_7
    ui_elem_7 = lv_obj_create(parent);
    lv_obj_clear_flag(ui_elem_7, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_width(ui_elem_7, 720);
    lv_obj_set_height(ui_elem_7, 260);
    lv_obj_center(ui_elem_7);
    lv_obj_set_style_bg_color(ui_elem_7, lv_color_hex(0x0A0A0F), 0);
    lv_obj_set_style_bg_opa(ui_elem_7, LV_OPA_COVER, 0);
    lv_obj_set_style_pad_all(ui_elem_7, 20, 0);

    // button#btn-minus
    ui_btn_minus = lv_btn_create(ui_elem_7);
    lv_obj_t* ui_btn_minus_label = lv_label_create(ui_btn_minus);
    lv_label_set_text(ui_btn_minus_label, "-");
    lv_obj_center(ui_btn_minus_label);
    lv_obj_add_event_cb(ui_btn_minus, event_btn_minus, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_minus, 280);
    lv_obj_set_height(ui_btn_minus, 200);
    lv_obj_align(ui_btn_minus, LV_ALIGN_LEFT_MID, 40, 0);
    lv_obj_set_style_bg_color(ui_btn_minus, lv_color_hex(0xE74C3C), 0);
    lv_obj_set_style_bg_opa(ui_btn_minus, LV_OPA_COVER, 0);
    lv_obj_set_style_text_color(ui_btn_minus, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_text_color(ui_btn_minus_label, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_radius(ui_btn_minus, 32, 0);
    lv_obj_set_style_text_font(ui_btn_minus, &lv_font_montserrat_48, 0);
    lv_obj_set_style_text_font(ui_btn_minus_label, &lv_font_montserrat_48, 0);

    // button#btn-plus
    ui_btn_plus = lv_btn_create(ui_elem_7);
    lv_obj_t* ui_btn_plus_label = lv_label_create(ui_btn_plus);
    lv_label_set_text(ui_btn_plus_label, "+");
    lv_obj_center(ui_btn_plus_label);
    lv_obj_add_event_cb(ui_btn_plus, event_btn_plus, LV_EVENT_CLICKED, NULL);
    lv_obj_set_width(ui_btn_plus, 280);
    lv_obj_set_height(ui_btn_plus, 200);
    lv_obj_align(ui_btn_plus, LV_ALIGN_LEFT_MID, 400, 0);
    lv_obj_set_style_bg_color(ui_btn_plus, lv_color_hex(0x27AE60), 0);
    lv_obj_set_style_bg_opa(ui_btn_plus, LV_OPA_COVER, 0);
    lv_obj_set_style_text_color(ui_btn_plus, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_text_color(ui_btn_plus_label, lv_color_hex(0xFFFFFF), 0);
    lv_obj_set_style_radius(ui_btn_plus, 32, 0);
    lv_obj_set_style_text_font(ui_btn_plus, &lv_font_montserrat_48, 0);
    lv_obj_set_style_text_font(ui_btn_plus_label, &lv_font_montserrat_48, 0);

    // Call init function
    init();
}
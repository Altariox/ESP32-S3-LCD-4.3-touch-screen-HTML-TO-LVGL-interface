// Auto-generated from HTML/CSS/JS
// Do not edit manually!

#ifndef UI_GENERATED_H
#define UI_GENERATED_H

#include "lvgl.h"

#ifdef __cplusplus
extern "C" {
#endif

// Extern function implemented in main.cpp for serial communication
extern void serial_send(const char* message);

// Dynamic labels accessible from main.cpp for updates
extern lv_obj_t* ui_time_display;
extern lv_obj_t* ui_date_display;
extern lv_obj_t* ui_temp_value;
extern lv_obj_t* ui_weather_desc;
extern lv_obj_t* ui_humidity;
extern lv_obj_t* ui_wind;

void ui_generated_init(lv_obj_t* parent);

#ifdef __cplusplus
}
#endif

#endif // UI_GENERATED_H

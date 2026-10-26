#pragma once
#include "main_flash_layout.h"

// Steno V3: RP2040-Plus 16 MB. Matrix cathodes on rows; columns pulled up.
// Keep Uni v4's 0..27 physical indexes and BOOTSEL=28 for its base script.
// The two additional far-left switches use indexes 29 and 30.
#define JAVELIN_USE_EMBEDDED_STENO 1
#define JAVELIN_USE_USER_DICTIONARY 1
#define JAVELIN_USB_MILLIAMPS 500
#define JAVELIN_DEBOUNCE_MS 10
#define JAVELIN_BUTTON_MATRIX 1
#define BOOTSEL_BUTTON_INDEX 28
#define JAVELIN_RGB 1
#define JAVELIN_RGB_PIN 22
#define JAVELIN_RGB_COUNT 8

constexpr uint8_t ROW_PINS[] = {0, 1, 2, 3, 4};
constexpr uint8_t COLUMN_PINS[] = {5, 6, 7, 8, 9, 10};
constexpr int8_t KEY_MAP[5][16] = {
  {29, 0, 1, 2, 3, 4},
  {30, 11, 12, 13, 14, 15},
  {5, 6, 7, 8, 9, 10},
  {16, 17, 18, 19, 20, 21},
  {22, 23, 24, 25, 26, 27},
};
const size_t BUTTON_COUNT = 31;
#define JAVELIN_SCRIPT_CONFIGURATION R"STENO({"n":"Steno V3","s":[],"k":[{"x":1,"y":0},{"x":2,"y":0},{"x":3,"y":0},{"x":4,"y":0},{"x":5,"y":0},{"x":8,"y":0},{"x":9,"y":0},{"x":10,"y":0},{"x":11,"y":0},{"x":12,"y":0},{"x":13,"y":0},{"x":1,"y":1},{"x":2,"y":1},{"x":3,"y":1},{"x":4,"y":1},{"x":5,"y":1},{"x":8,"y":1},{"x":9,"y":1},{"x":10,"y":1},{"x":11,"y":1},{"x":12,"y":1},{"x":13,"y":1},{"x":3,"y":3},{"x":4,"y":3},{"x":5,"y":3},{"x":8,"y":3},{"x":9,"y":3},{"x":10,"y":3},{"x":13.5,"y":3.5,"s":0.5},{"x":0,"y":0},{"x":0,"y":1}]})STENO"

const char *const MANUFACTURER_NAME = "Steno V3";
const char *const PRODUCT_NAME = "Steno V3 (Javelin)";
const int VENDOR_ID = 0xFEED;

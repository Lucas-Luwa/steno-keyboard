"""Run on the keyboard in MicroPython, for example using Thonny's Run button.

Steno V3: Waveshare RP2040-Plus 16 MB, GP22, eight WS2812B LEDs.
Requires the assembled controller, fuse, buffer, R3, capacitors and LED chain.
Switches and keyboard diodes are not required for this LED-only test.
"""

from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

LED_PIN = 22
LED_REFERENCES = ("LED17", "LED16", "LED15", "LED14",
                  "LED13", "LED12", "LED8", "LED28")
LEVEL = 16  # Dim test level, out of 255; no full-brightness white.
COLORS = (("red", (LEVEL, 0, 0)),
          ("green", (0, LEVEL, 0)),
          ("blue", (0, 0, LEVEL)))

pixels = NeoPixel(Pin(LED_PIN, Pin.OUT, value=0), len(LED_REFERENCES))


def show_all(color):
    pixels.fill(color)
    pixels.write()
    sleep_ms(10)  # Allow the LEDs to latch before another update.


try:
    show_all((0, 0, 0))
    sleep_ms(300)
    print("LED test: GP22, eight pixels, low brightness.")
    for name, color in COLORS:
        print("All eight LEDs:", name)
        show_all(color)
        sleep_ms(1500)
        show_all((0, 0, 0))
        sleep_ms(250)

    for name, color in COLORS:
        for index, reference in enumerate(LED_REFERENCES):
            pixels.fill((0, 0, 0))
            pixels[index] = color
            pixels.write()
            print("Index", index, reference, name)
            sleep_ms(600)
    print("Test complete. All LEDs will turn off. Run again to repeat.")
finally:
    # Also attempt to turn the LEDs off if you interrupt the test with Ctrl+C.
    show_all((0, 0, 0))

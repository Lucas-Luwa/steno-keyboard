# Physical LED test results

Date: October 25, 2026. Hardware: V3 keyboard with Waveshare RP2040-Plus 16 MB, GP22/buffer/330 Ω data path and eight WS2812B LEDs. Firmware: MicroPython 1.29.0.

| Session | Requested level | Result |
| --- | --- | --- |
| Initial RGB and individual chase | 16/255 | Completed; builder visually confirmed all eight LEDs showed red, green and blue, with none dark. |
| Complete base showcase | Normal animations 64/255; sweeps 1–255 | All 134 cues completed without a reported controller error; final all-off write completed. |
| Fast/fade extension | 128/255 | All 35 cues completed; no limited frames; final all-off write completed. |
| Same fast/fade extension | 255/255 | All 35 cues completed; no limited frames; final all-off write completed. |
| Half-output comparison replay | 128/255 | All 35 cues completed again; no limited frames; final all-off write completed. |

The base showcase's limiter reduced 57 frames, all in the lavender brightness sweep/ramps. Its estimated channel-current peak was 320 mA. The fast extension estimated a peak of approximately 160.63 mA at 128 and 320 mA at 255. These are calculations from commanded RGB values, not readings from a meter. Requested 255 output was not reduced in the fast-extension session.

The builder reported that 50% and 100% appeared similar. The software records confirm different level overrides, 128 versus 255; actual luminance was not measured. Raw PWM settings are not proportional to perceived brightness.

The RGB/chase run visually confirmed all eight LEDs. The later sessions record controller execution and LED-off writes; individual animation frames were not independently inspected.

These results cover the MicroPython diagnostics. The [Javelin lighting script](../javelin/README.md#onboard-lighting) is a separate implementation.

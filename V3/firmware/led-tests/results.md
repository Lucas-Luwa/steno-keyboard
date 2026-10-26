# Physical LED test results

Date: October 25, 2026. Hardware: Steno V3 with Waveshare RP2040-Plus 16 MB, GP22/buffer/330 Ω data path and eight WS2812B LEDs. Firmware: MicroPython 1.29.0. Results are for the assembled prototype, not a production qualification.

| Session | Requested level | Result |
| --- | --- | --- |
| Initial RGB and individual chase | 16/255 | Completed; builder visually confirmed all eight LEDs showed red, green and blue, with none dark. |
| Complete base showcase | Normal animations 64/255; sweeps 1–255 | All 134 cues completed without a reported controller error; final all-off write completed. |
| Fast/fade extension | 128/255 | All 35 cues completed; no limited frames; final all-off write completed. |
| Same fast/fade extension | 255/255 | All 35 cues completed; no limited frames; final all-off write completed. |
| Half-output comparison replay | 128/255 | All 35 cues completed again; no limited frames; final all-off write completed. |

The base showcase's limiter reduced 57 frames, all in the lavender brightness sweep/ramps. Its estimated channel-current peak was 320 mA. The fast extension estimated a peak of approximately 160.63 mA at 128 and 320 mA at 255. These are calculations from commanded RGB values, not readings from a meter. Requested 255 output was not reduced in the fast-extension session.

The builder reported that 50% and 100% appeared similar. The software records confirm different level overrides, 128 versus 255; actual luminance was not measured. Raw PWM settings are not proportional to perceived brightness.

The later 134/35-cue sessions establish successful controller execution and LED-off writes. They were not an independent camera inspection of every rendered frame. The initial RGB/chase visual confirmation demonstrates a functional power/data chain through all eight LEDs at that test level. It does not individually certify every capacitor, measure the buffer waveform, prove a fuse trip characteristic or establish every USB port's current capacity.

The controller successfully compiled and ran both renderers. An unsupported string-title method found during the first attempt was removed before the successful showcase. Simulated frame, mapping, interruption/error cleanup and fake-serial checks were also completed before live use. Raw session logs and development checks are retained outside the repository.

No real-audio/FFT or Javelin lighting implementation was tested. Javelin replaces MicroPython, so these demos need a separate port or script implementation there. The saved diagnostic programs remain available for reuse.

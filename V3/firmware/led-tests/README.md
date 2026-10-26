# LED tests and visual patterns

Run these diagnostics on the **Waveshare RP2040-Plus 16 MB with MicroPython**, before installing Javelin or when troubleshooting the RGB chain. They drive GP22 and eight WS2812Bs; switches are not needed. The scripts are diagnostic programs, not Javelin firmware.

The initial RGB test was visually confirmed on the assembled board. The 134-cue showcase and 35-cue extension subsequently ran at the levels recorded in [results.md](results.md).

## Hardware and LED order

`GP22 → U1 buffer → R3 (330 Ω) → eight WS2812Bs`

The LED supply passes through F1. Nine 100 nF capacitors provide local bypassing for the eight LEDs and buffer. The tested order is left to right, four LEDs per half:

| Position | Pixel index | Reference |
| --- | ---: | --- |
| 1 | 0 | LED17 |
| 2 | 1 | LED16 |
| 3 | 2 | LED15 |
| 4 | 3 | LED14 |
| 5 | 4 | LED13 |
| 6 | 5 | LED12 |
| 7 | 6 | LED8 |
| 8 | 7 | LED28 |

## Choose a test

| File | Purpose |
| --- | --- |
| [steno-led-test.py](steno-led-test.py) | Initial all-pixel RGB and individual RGB chase at 16/255; finishes off. |
| [steno-led-showcase.py](steno-led-showcase.py) | 134 labelled demos: mapping, 22 colours, brightness comparisons, motion, symmetry, textures, synthetic beats, detail comparisons and flashes. |
| [steno-led-energy.py](steno-led-energy.py) | Optional 35-cue extension: fades, rapid stripes/chases, random colours, synthetic rhythms and flashes. Load it through the launcher after the base renderer. |
| [run.py](run.py) | Computer-side launcher: explicit USB port selection, labels, logs, level/speed selection and stopping. |

The full base catalogue takes about 18:53. The fast extension takes about 3:49. See [catalogue.md](catalogue.md) for IDs and [energy-catalogue.md](energy-catalogue.md) for the extra 35 cues.

## Install MicroPython and run the first test

1. Disconnect USB before soldering. Inspect orientation and joints, and check for a persistent supply-to-ground short before powering a new assembly.
2. If the board contains Javelin dictionaries/settings you need, export them before replacing firmware. MicroPython is a separate firmware, not an application running inside Javelin.
3. Use the **16 MiB Flash** firmware from the [official Waveshare RP2040-Plus download page](https://micropython.org/download/WAVESHARE_RP2040_PLUS/). The completed sessions used MicroPython 1.29.0.
4. Hold BOOTSEL while connecting USB, then copy the UF2 to `RPI-RP2`. Its disappearance after flashing is normal. If the correct MicroPython firmware is already installed, connect normally without BOOTSEL.
5. In [Thonny](https://thonny.org/), select the Raspberry Pi Pico/MicroPython interpreter and the correct serial port. Open `steno-led-test.py` and Run. Do not copy Python scripts to the BOOTSEL drive.
6. Verify every LED shows red, green and blue, then the individual chase. The script finishes by sending an all-off frame.

## Run labelled sections from a computer

With Python installed, open a terminal in this directory and install the pinned launcher dependencies:

```powershell
py -m pip install -r requirements.txt
py run.py --list
py run.py --section colors --prepare-only
```

Find the board's current serial port in Device Manager or Thonny. Substitute that port below; `COM4` is only an example. Close other programs holding the port.

```powershell
py run.py --port COM4 --section colors
py run.py --port COM4 --section motion --level 128
py run.py --port COM4 --energy --level 128
py run.py --port COM4 --energy --level 255
py run.py --port COM4 --energy --pattern energy-out-24 --level 128 --repeat 3
py run.py --port COM4 --all
```

The port must identify a MicroPython RP2040 (VID 0x2E8A, PID 0x1020). Add `--serial YOUR_SERIAL` to require a particular board identity. Nothing flashes automatically or installs a startup program. Program payloads, session markers and logs are under this directory's ignored `work/` folder.

Use Ctrl+C in the running terminal, or `py run.py --stop` in a second terminal. The launcher sends an interrupt and waits for the renderer's LED-off cleanup. `py run.py --status` reports the current cue. The device turns LEDs off on completion, interruption or a caught error; communication-error recovery attempts all-off while the link survives. Unplugging USB removes power. A stale session marker after a forcibly terminated process needs review before another run.

## Brightness, colour and speed

The first test uses **16/255 (6.3% raw channel level)**. Normal showcase animations use **64/255 (25.1%)**. The extension defaults to **128/255 (50.2%)**; `--level 255` requests full output. Fades and trails vary below the chosen peak. These are digital channel settings, not perceived-brightness percentages.

Brightness sweeps use 1, 2, 4, 8, 16, 24, 32, 48, 64, 96, 128, 160, 192, 224 and 255. Base brightness/flash cues retain fixed labelled levels and reject a level override. The fast extension allows the requested override, including its flashes. White is excluded; the base showcase includes non-white pastels.

Every rendered frame retains an estimated **320 mA light-producing-channel limit**, based on 20 mA per full channel. Demanding frames are scaled down and counted in the summary. Adding a 100 mA planning reserve gives approximately 420 mA; actual USB current, fuse rating and port allocation were not measured. The BOM fuse is the design value; the builder reported possibly fitting a 750 mA part, which remains unconfirmed. Do not treat the software limiter as hardware protection or the fuse as a USB power allocation.

Playback speed can be selected from 0.25 to 4. It also changes labelled BPM/flash rates relative to their speed-1 values. Fast-motion rates are animation targets, not measured timing guarantees. Flash demos include rapid 8/12/16 Hz changes; the base flash section has a five-second dark countdown. Other beat and random-colour effects also contain abrupt changes.

## Scope of these demos

Beat/BPM and bass/mid/treble examples are synthetic. They do not capture laptop audio, run an FFT, detect real beats or integrate with Javelin. The four-zone/eight-pixel A/B groups physical neighbours into pairs; it cannot reproduce sixteen physical LEDs. Increasing the LED count requires reviewing power and bypassing as well as changing software.

See the [firmware guide](../README.md) for the separate Javelin configuration and the [build guide](../../build-guide.md) for assembly.

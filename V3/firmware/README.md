# Javelin hardware configuration

The keyboard uses [Javelin firmware with Lapwing dictionaries](javelin/README.md) and onboard lighting. This guide covers the controller, switch matrix and RGB connections used by the firmware. The separate [MicroPython diagnostics](led-tests/README.md) check the LED chain before loading Javelin.

## LED diagnostics

The [LED test guide](led-tests/README.md) covers RGB/chase checks, color and brightness patterns, and fade animations. These diagnostics drive GP22 without scanning the switch matrix. See the [test results](led-tests/results.md) for the recorded runs.

## Controller and pins

| Function | Configuration |
|---|---|
| Controller | Waveshare RP2040-Plus-16MB |
| Matrix rows | GP0, GP1, GP2, GP3, GP4 |
| Matrix columns | GP5, GP6, GP7, GP8, GP9, GP10 |
| Scan direction | Select cathode rows low; read columns with pull-ups; unselected rows inactive |
| RGB data | GP22 |
| RGB count | 8 |

## Electrical matrix

| Row / column | GP5 | GP6 | GP7 | GP8 | GP9 | GP10 |
|---|---|---|---|---|---|---|
| GP0 | SW1 | SW2 | SW3 | SW4 | SW5 | SW6 |
| GP1 | SW7 | SW8 | SW9 | SW10 | SW11 | SW12 |
| GP2 | SW13 | SW14 | SW15 | SW16 | SW17 | SW18 |
| GP3 | SW31 | SW32 | SW33 | SW34 | SW35 | SW36 |
| GP4 | SW25 | SW26 | SW27 | SW28 | SW29 | SW30 |

Map each electrical position to its steno action or auxiliary key in the firmware. [key-matrix.csv](../hardware/key-matrix.csv) provides the diode reference and PCB coordinates for each switch; [pinout.csv](../hardware/pinout.csv) provides physical controller pad numbers.

## RGB LEDs

Configure the serial order as **LED17 → LED16 → LED15 → LED14 → LED13 → LED12 → LED8 → LED28**. The first index is zero.

Set a brightness cap for normal operation and startup effects. Account for both the controller and LEDs in the USB current budget.

## Building and flashing

Use the [custom Javelin build instructions](javelin/README.md#reproduce-the-build) with the matrix, GPIO assignments and LED order above. The packager combines the custom hardware binary, 31-button script and dictionary/data image into one UF2; a hardware-only image does not include the dictionaries.

## Custom Javelin build

The [Javelin/Lapwing configuration](javelin/README.md) defines the base and Fn key layouts, dictionary preset and onboard lighting. Its guide includes the hardware header, key script and build instructions for this PCB.

The Lapwing preset includes Emily's Symbols, Javelin-compatible modifiers, number support and Jeff's Phrasing. See the [dictionary preset](javelin/README.md#dictionary-preset) for the enabled dictionaries and settings.

[Onboard lighting](javelin/README.md#onboard-lighting) includes brightness controls, bouncing wave, breathing colors, glowing coals, color drift and long-rest pulses. Key activity turns the LEDs green; the selected idle effect resumes after five minutes without typing. The lighting guide explains the selectors and color palettes.

The [key layout](javelin/README.md#physical-layout) covers steno keys, navigation, modifiers and lighting controls on the Fn layer.

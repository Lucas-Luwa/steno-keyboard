# Javelin hardware configuration

This directory contains [runnable MicroPython LED diagnostics](led-tests/README.md) and the hardware configuration reference for the separate custom Javelin build. The diagnostics have run on the physical prototype; the custom Javelin build is now installed and its configuration/dictionary lookups have passed on-device checks. The configuration below defines the controller, matrix and RGB connections.

## LED diagnostics

The [LED test guide](led-tests/README.md) covers the initial RGB/chase test, 134-cue colour/brightness showcase and 35-cue fast/fade extension. [Recorded prototype results](led-tests/results.md) distinguish observed execution and visual confirmation from estimated current. Normal connection, execution and stop commands are included; the scripts drive GP22 without scanning the switch matrix.

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

1. Use [javelin-steno-pico](https://github.com/jthlim/javelin-steno-pico) and its [custom-hardware guide](https://github.com/jthlim/javelin-steno-pico#using-javelin-steno-pico-with-your-own-hardware).
2. Set the controller, matrix scan direction, key actions and RGB parameters above in the hardware configuration.
3. Prepare the complete dictionary/data image and custom hardware binary, then combine them offline with the matching 31-button script as described in the [reproducible build guide](javelin/README.md). Flash only the combined custom UF2 to this PCB. A hardware-only image does not supply dictionary data or reuse a MicroPython filesystem.
4. Enter the controller's BOOTSEL mode, connect it over USB and copy the UF2 to the bootloader drive.
5. Exercise every key, simultaneous chords, releases, USB reconnect and the RGB chain before closing the case.

Use the same key assignments in your firmware configuration and stenography software.

## Custom Javelin build

The installed initial setup is Lapwing with the compatible dictionary stack documented in the [Lapwing Javelin guide](https://lapwing.aerick.ca/Appendix-C.html): core Lapwing dictionaries, Emily's Symbols, Javelin-compatible Emily/Abby modifiers, number support and Jeff's Phrasing. Jeff's Modifiers is disabled in that documented setup. The movement and Jeff’s Numbers dictionaries are included but initially disabled; Lapwing’s number dictionary is active. The [custom hardware build and Lapwing preset](javelin/README.md) now include the matrix header, 31-button script, key layout and reproducible image packaging. Offline checks, installation, USB enumeration, configuration and dictionary lookups passed. The first physical word sequence also passed.

The LED diagnostics remain separate from the final Javelin effects. Their audio events are simulated; live laptop audio input, on-device FFT and beat-reactive firmware are future software work.

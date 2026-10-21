# Javelin hardware configuration

Use these parameters to configure Javelin for Steno V3. The firmware source/code update will be added in this directory. The configuration reference below defines the controller, matrix and RGB connections.

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
3. Build the UF2 using the toolchain instructions for the chosen upstream revision.
4. Enter the controller's BOOTSEL mode, connect it over USB and copy the UF2 to the bootloader drive.
5. Exercise every key, simultaneous chords, releases, USB reconnect and the RGB chain before closing the case.

Use the same key assignments in your firmware configuration and stenography software.

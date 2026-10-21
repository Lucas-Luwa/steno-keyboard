# Electronics

Open [`StenoV3.kicad_pro`](StenoV3.kicad_pro) in KiCad 10 with the standard symbol, footprint and 3D libraries installed.

## Circuit specifications

| Item | Specification |
|---|---|
| Controller | Waveshare RP2040-Plus-16MB |
| Switch matrix | 30 positions, 5 rows × 6 columns |
| Switches | Kailh Choc V1 |
| Row pins | GP0–GP4, connected to diode cathodes |
| Column pins | GP5–GP10, connected to switch sides |
| LED data | GP22 → U1 → R3 (330 Ω) → LEDs |
| RGB LEDs | Eight 5 × 5 mm WS2812B LEDs in a serial chain |
| Bypass capacitors | Nine × 100 nF, 0805 |
| Mounting holes | Eight × 2.2 mm for M2 screws |
| PCB | Two copper layers, 1.6 mm thickness; approximately 252 × 68 mm |

A1 uses the generic `RaspberryPi_Pico` symbol, footprint and 3D model. Fit the Waveshare module with its USB-C connector aligned to the case opening.

## Parts and connections

- [Bill of materials](bom.csv): component quantities, references, schematic values, footprints and package notes.
- [Controller pinout](pinout.csv): GPIO functions and physical module pad numbers.
- [Electrical key matrix](key-matrix.csv): each switch, its diode and its PCB position.
- [LED chain](led-chain.csv): zero-based LED order, beginning at R3.

Use the matrix's row/column coordinates when assigning firmware key actions. Electrical matrix positions are independent of physical keyboard rows.

## Component packages

| Reference | Part / package | Schematic label |
|---|---|---|
| A1 | Waveshare RP2040-Plus-16MB, castellated Pico-compatible module | `RaspberryPi_Pico` |
| D2–D45, populated positions listed in BOM | 1N4148-family switching diode, **SOD-323**; e.g. 1N4148WS | `1N4148W` |
| LED8–LED28, populated positions listed in BOM | WS2812B, **5 × 5 mm four-pin** | `WS2812C` |
| U1 | Single buffer, **SOT-23-5**; see buffer options below | `74AHCT1G125` |
| F1 | MF_MSMF050-2 resettable fuse, **1812** | `MF_MSMF050-2` |

The component/package column identifies the assembly part; the schematic-label column connects it to the names in the design files. Match the package to the footprint when ordering. For the diode's package and cathode marking, see the [1N4148WS datasheet](https://www.diodes.com/datasheet/download/1N4148WS.pdf).

## LED buffer

The PCB's U1 connections are:

| Pin | PCB connection |
|---|---|
| 1 | Ground |
| 2 | GP22 input |
| 3 | Ground |
| 4 | R3 → first LED DIN |
| 5 | Fused USB 5 V |

The SOT-23-5 options are **74AHCT1G125** and **SN74LV1T34DBVR**. Pin 1 grounds the AHCT buffer's active-low enable; the LV1T34 leaves pin 1 internally unconnected. Both use pins 2–5 for input, ground, output and supply. Use the DBV/SOT-23-5 package. See the [74AHCT1G125](https://www.ti.com/lit/ds/symlink/sn74ahct1g125.pdf) and [SN74LV1T34](https://www.ti.com/lit/ds/symlink/sn74lv1t34.pdf) pin tables.

## Matrix and RGB configuration

Scan GP0–GP4 as cathode rows, selecting one row low at a time and reading GP5–GP10 with pull-ups. Leave unselected rows inactive.

The RGB chain is **LED17 → LED16 → LED15 → LED14 → LED13 → LED12 → LED8 → LED28**. Apply a firmware brightness cap to the complete chain, including startup effects, and keep total keyboard current within the USB supply budget.

## Libraries and models

The custom Choc footprint is under `libraries/`; the footprint table uses a project-relative path. Switch and fuse models are under `models/`. Standard models use `${KICAD10_3DMODEL_DIR}`. The board has no display.

Continue with the [build guide](../build-guide.md) or [firmware configuration](../firmware/README.md).

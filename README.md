# Steno

A custom 30-key stenography keyboard with a Waveshare RP2040-Plus 16 MB controller, Kailh Choc V1 switches, eight RGB LEDs, and a 3D-printed case with a removable travel cap.

**[V3](V3/) is the latest version.** Earlier electronics designs and base meshes are in [archive/](archive/README.md).

![Steno PCB](V3/images/pcb-front.png)

## Start here

| What you need | Open |
|---|---|
| Assembly instructions | [Build guide](V3/build-guide.md) |
| Schematic, PCB and parts | [Electronics](V3/hardware/README.md) · [KiCad project](V3/hardware/StenoV3.kicad_pro) · [BOM](V3/hardware/bom.csv) |
| Editable CAD, STL models and printer jobs | [Mechanical guide](V3/mechanical/README.md) |
| Gerbers and drill files | [Fabrication guide](V3/manufacturing/README.md) · [Fabrication ZIP](V3/manufacturing/StenoV3-Gerbers.zip) |
| Javelin hardware configuration | [Firmware guide](V3/firmware/README.md) |
| Switch-library credits and licenses | [Reference assets](third_party/README.md) |

## Design files

The [mechanical guide](V3/mechanical/README.md) covers the editable base, protective cap, heat-set-insert coupon, keycap references and keyboard assemblies. There are **20 SolidWorks part files and 12 assembly files**, plus STEP references and printable meshes.

For printing, start with [`case-bottom.stl`](V3/mechanical/stl/case-bottom.stl), [`travel-cap.stl`](V3/mechanical/stl/travel-cap.stl) and [`insert-test-coupon.stl`](V3/mechanical/stl/insert-test-coupon.stl). Printer jobs for A1, P1S and P2S are grouped under [`print-jobs/`](V3/mechanical/print-jobs/).

The [electronics guide](V3/hardware/README.md) explains component packages, the five-row/six-column matrix and the RGB chain. GPIO assignments, switch/diode positions and LED order are also available as CSV tables alongside the KiCad project.

## Repository layout

```text
steno/
├── README.md
├── V3/
│   ├── build-guide.md
│   ├── hardware/        # KiCad project, BOM, pinout and matrix
│   ├── mechanical/
│   │   ├── solidworks/ # Editable parts and assemblies
│   │   ├── step/       # Neutral CAD references
│   │   ├── stl/        # Three current printable models
│   │   └── print-jobs/ # A1, P1S and P2S jobs
│   ├── manufacturing/ # Fabrication ZIP and individual Gerbers/drills
│   ├── firmware/       # Javelin hardware configuration
│   └── images/         # Board diagrams and project images
├── archive/            # Earlier electronics versions and base meshes
└── third_party/        # Reference-asset credits and license texts
```

## Photos and code

The design files, printable models and build documentation are available here. Photos of the physical parts and the firmware source/code update are the remaining additions. Project images belong in [`V3/images/`](V3/images/), and the code update belongs in [`V3/firmware/`](V3/firmware/README.md).

## Credits

[Javelin](https://github.com/jthlim/javelin-steno-pico) by its contributors. Kailh Choc switch footprint and models from [keyswitch-kicad-library](https://github.com/perigoso/keyswitch-kicad-library). See [third_party/](third_party/README.md) for the bundled notices.

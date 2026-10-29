# Steno

A custom 30-key stenography keyboard with a Waveshare RP2040-Plus 16 MB controller, Kailh Choc V1 switches, eight RGB LEDs, and a 3D-printed case with a removable travel cap.

**[V3](V3/) is the latest version.** Earlier electronics designs and case exports are in [archive/](archive/README.md).

![Assembled Steno keyboard with aqua keycaps and a pink printed base](V3/images/keyboard-assembled.jpg)

## Start here

| What you need | Open |
|---|---|
| Assembly instructions | [Build guide](V3/build-guide.md) |
| Schematic, PCB and parts | [Electronics](V3/hardware/README.md) · [KiCad project](V3/hardware/StenoV3.kicad_pro) · [BOM](V3/hardware/bom.csv) |
| Editable CAD, STL models and printer jobs | [Mechanical guide](V3/mechanical/README.md) |
| Gerbers and drill files | [Fabrication guide](V3/manufacturing/README.md) · [Fabrication ZIP](V3/manufacturing/StenoV3-Gerbers.zip) |
| Javelin configuration and LED diagnostics | [Firmware guide](V3/firmware/README.md) |
| LED diagnostics and test results | [LED test guide](V3/firmware/led-tests/README.md) · [Results](V3/firmware/led-tests/results.md) |
| Switch-library credits and licenses | [Reference assets](third_party/README.md) |

## Onboard lighting

Steno uses [Javelin/Lapwing](V3/firmware/javelin/README.md) for onboard stenography. The lighting runs on the controller, with selectable idle patterns, brightness controls and a green typing indicator.

<a href="V3/images/videos/onboard-lighting-demo.mp4">
  <img src="V3/images/onboard-lighting-demo-poster.jpg" alt="Onboard lighting on the assembled keyboard" width="320">
</a>

[Watch the lighting demo](V3/images/videos/onboard-lighting-demo.mp4).

See the [lighting controls and color palettes](V3/firmware/javelin/README.md#onboard-lighting), or the separate [bare-board LED diagnostics](V3/firmware/led-tests/README.md).

## Design files

The [mechanical guide](V3/mechanical/README.md) covers the base, travel cap, insert coupon, LED jig references and keyboard assemblies.

For printing, start with [`case-bottom.stl`](V3/mechanical/stl/case-bottom.stl), [`travel-cap.stl`](V3/mechanical/stl/travel-cap.stl) and [`insert-test-coupon.stl`](V3/mechanical/stl/insert-test-coupon.stl). The [SV06/OrcaSlicer profile](V3/mechanical/README.md#sv06-slicing-settings) covers PLA settings and diagonal bed placement. Slice the current travel cap from its STL. Bambu-specific base and insert-coupon printer jobs for A1, P1S and P2S are grouped under [`print-jobs/`](V3/mechanical/print-jobs/).

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
│   │   ├── stl/        # Case, coupon and LED jig reference meshes
│   │   └── print-jobs/ # A1, P1S and P2S base/coupon jobs
│   ├── manufacturing/ # Fabrication ZIP and individual Gerbers/drills
│   ├── firmware/       # Javelin hardware configuration and LED diagnostics
│   └── images/         # Build photos, diagrams and videos
├── archive/            # Earlier electronics versions and case exports
└── third_party/        # Reference-asset credits and license texts
```

## Credits

[Javelin](https://github.com/jthlim/javelin-steno-pico) by its contributors. Kailh Choc switch footprint and models from [keyswitch-kicad-library](https://github.com/perigoso/keyswitch-kicad-library). See [third_party/](third_party/README.md) for the bundled notices.

## License

See [LICENSE.md](LICENSE.md) for hardware, software, documentation and third-party license terms.

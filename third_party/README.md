# Credits and reference assets

## Switch footprint and models

The Kailh Choc V1 footprint and WRL/STP models are from [perigoso/keyswitch-kicad-library](https://github.com/perigoso/keyswitch-kicad-library), maintained by Rafael Silva and contributors. The library's MIT and CC-BY-SA license texts are included under [`keyswitch-kicad-library/`](keyswitch-kicad-library/).

The footprint uses a project-relative model path. Standard KiCad symbols, footprints and models are supplied by the KiCad installation.

## Firmware

[Javelin](https://github.com/jthlim/javelin-steno) and its [Pico bindings](https://github.com/jthlim/javelin-steno-pico), by Jeffrey Lim and contributors, provide the firmware platform. Their upstream **PolyForm Noncommercial 1.0.0** terms remain applicable to their code and any adapted upstream portions. A [license copy](javelin/LICENSE.txt) is included from the engine revision used in the [build guide](../V3/firmware/javelin/README.md#reproduce-the-build).

The project's MIT grant applies to original project code and contributions; it does not relicense the Javelin engine, Pico bindings, upstream compiler, dictionary data or adapted upstream portions. Follow their respective source notices and license terms when building and distributing combined firmware.

## Reference geometry

The mechanical directories include controller, switch, keycap, PCB and discrete-component models for positioning the electronics and designing the enclosure. Keep these reference components with the assemblies that use them.

## Original project materials

See [LICENSE.md](../LICENSE.md) for the licenses covering original hardware designs, project code and documentation. Imported reference models and library assets keep their original terms, including reference geometry embedded in assemblies.

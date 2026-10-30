# Steno project licensing

Copyright © 2026 Steno project.

## Build, modify and share

You are welcome to build your own Steno keyboard, study the designs, make changes and share improvements. The original project materials are licensed as follows, subject to the third-party exceptions below:

| Original project material | License |
|---|---|
| Electronics designs and associated fabrication exports in `V3/hardware/` and `V3/manufacturing/`, and original earlier electronics designs in `archive/` | [CERN-OHL-P-2.0](LICENSES/CERN-OHL-P-2.0.txt) |
| Original case and jig designs, their native CAD, STEP/STL exports and print jobs, including archived versions | [CERN-OHL-P-2.0](LICENSES/CERN-OHL-P-2.0.txt) |
| Original project software, diagnostic scripts, build/packaging tools and original contributions to firmware configuration and scripts | [MIT](LICENSES/MIT.txt) |
| Original guide text, photographs and explanatory illustrations | [CC BY 4.0](LICENSES/CC-BY-4.0.txt) |

These are permissive grants: the covered original work may be reused, modified and distributed, including commercially, under the applicable terms. Preserve the applicable copyright, attribution and license notices. Hardware modifications distributed under CERN-OHL-P must also identify their changes as that license requires. You do not have to publish your own improvements under these permissive licenses.

## Third-party exceptions

These grants apply only to rights held by this project's authors. Existing third-party notices and licenses continue to apply to imported material and adapted portions; their inclusion here does not relicense them.

- **Javelin:** the Javelin engine, Pico bindings and any upstream-derived portions retain their upstream **PolyForm Noncommercial 1.0.0** terms. The MIT grant covers original project contributions only and does not grant additional rights to the underlying Javelin software. A [license copy](third_party/javelin/LICENSE.txt) and [source references](third_party/README.md#firmware) are provided. Combined firmware must comply with all applicable upstream terms.
- **Switch footprint and models:** the bundled keyswitch-kicad-library assets retain their [MIT and CC-BY-SA notices](third_party/README.md#switch-footprint-and-models), including where used in design files.
- **Reference geometry and libraries:** imported controller, switch, keycap, PCB and component reference models, plus standard KiCad library material, are not relicensed as original case designs. Follow their source notices and license terms. The same boundary applies to reference bodies embedded in native CAD or STEP assemblies.
- **Dependencies and dictionaries:** upstream compiler/runtime dependencies, dictionary content and other external data retain their own terms. Project configuration and packaging instructions do not change those terms.

The complete license texts govern. Materials are supplied without the warranties disclaimed in those licenses. See the [reference-asset guide](third_party/README.md) for credits and upstream sources.

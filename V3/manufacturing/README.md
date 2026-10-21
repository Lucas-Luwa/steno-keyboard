# PCB fabrication

Download [`StenoV3-Gerbers.zip`](StenoV3-Gerbers.zip) for a fabricator. The same Gerber, drill and job files are available individually under [`gerbers/`](gerbers/).

## Package contents

| Files | Function |
|---|---|
| `StenoV3-F_Cu.gtl`, `StenoV3-B_Cu.gbl` | Front and back copper |
| `StenoV3-F_Mask.gts`, `StenoV3-B_Mask.gbs` | Front and back solder mask |
| `StenoV3-F_Silkscreen.gto`, `StenoV3-B_Silkscreen.gbo` | Front and back silkscreen |
| `StenoV3-Edge_Cuts.gm1` | Board outline |
| `StenoV3-PTH.drl` | Plated holes |
| `StenoV3-NPTH.drl` | Non-plated holes |
| `StenoV3-job.gbrjob` | Gerber job metadata |

The ZIP and individual files contain the same V3 board package. It uses two copper layers and a nominal **1.6 mm** PCB thickness. Solder-paste/stencil layers are excluded.

## Ordering

Upload the ZIP as one PCB design and select bare-board fabrication. Use a two-layer FR-4 stackup, 1.6 mm thickness and 1 oz outer copper. Select the board color, finish and quantity for your build. PCB assembly and stencil services are separate from this package.

Inspect the fabricator's preview with plated and non-plated holes visible. Use the [electronics guide and BOM](../hardware/README.md) for component selection and the [build guide](../build-guide.md) for hand assembly.

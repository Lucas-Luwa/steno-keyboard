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

The PCB was fabricated by **AIVON**. The Gerber package can also be used with another fabricator offering the board specifications below.

Fabrication specification: **two-layer FR-4, 1.6 mm thickness and 1 oz outer copper**. The package is for bare-board fabrication and includes separate plated and non-plated drill files; stencil layers are not included.

Component packages are listed in the [electronics guide and BOM](../hardware/README.md); assembly is covered in the [build guide](../build-guide.md).

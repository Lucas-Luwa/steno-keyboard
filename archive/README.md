# Earlier designs

Use [V3](../V3/) and the [main project guide](../README.md) for the current keyboard.

## Electronics

- [`StenoV1/`](StenoV1/): first electronics version.
- [`StenoV2/`](StenoV2/): second electronics version and its fabrication files.

## Earlier base meshes

The [`prints/`](prints/) directory contains these earlier case-base exports:

| File | Size (mm) |
|---|---|
| [BottomCasePARTONLYV1.STL](prints/BottomCasePARTONLYV1.STL) | 254.286 × 70.286 × 6.336 |
| [BottomSTLV1.STL](prints/BottomSTLV1.STL) | 254.286 × 70.286 × 14.090 |
| [BottomSTLV2.STL](prints/BottomSTLV2.STL) | 254.286 × 70.286 × 5.955 |

For the current base, cap and insert coupon, use the [mechanical guide](../V3/mechanical/README.md).

## Previous travel cap

The previous cover mesh is [travel-cap-previous.stl](prints/travel-cap-previous.stl), measuring 254.286 × 87.366 × 20.433 mm. Its native source remains at [TopCaseV3.SLDPRT](../V3/mechanical/solidworks/TopCaseV3.SLDPRT) with the other SolidWorks files to preserve the original assembly references.

The following sliced jobs belong to that previous cover geometry:

| Printer | Previous cap job |
|---|---|
| Bambu A1 | [travel-cap-previous-A1.gcode.3mf](prints/travel-cap-previous-A1.gcode.3mf) |
| Bambu P1S | [travel-cap-previous-P1S.gcode.3mf](prints/travel-cap-previous-P1S.gcode.3mf) |
| Bambu P2S | [travel-cap-previous-P2S.gcode.3mf](prints/travel-cap-previous-P2S.gcode.3mf) |

For the taller cap with the horizontal center hook, use the [current travel-cap guide](../V3/mechanical/README.md#current-travel-cap) and slice its STL.

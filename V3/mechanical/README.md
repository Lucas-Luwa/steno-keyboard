# Mechanical design and printing

This folder contains the case base, protective travel cap, heat-set-insert coupon, full-length and short LED alignment jig references, keycap references and keyboard assemblies. Use native CAD to edit features, STEP for reference geometry, STL to prepare your own prints, or a printer job for the matching setup.

## File formats

| Folder | Contents | Use |
|---|---|---|
| [`solidworks/`](solidworks/) | 23 `.SLDPRT` files and 12 `.SLDASM` files | Edit parts and work with the keyboard assembly |
| [`step/`](step/) | Travel cap, PCB assembly and keycap STEP files | Exchange cap geometry and position references in CAD |
| [`stl/`](stl/) | Base, travel cap, insert coupon and two LED jig references | Slice printable geometry |
| [`print-jobs/`](print-jobs/) | Six base/coupon jobs, grouped by A1/P1S/P2S | Print using a matching printer setup |

Earlier base and cap meshes, plus jobs for the previous cap, are in [`archive/prints/`](../../archive/prints/), described in the [archive guide](../../archive/README.md).

## Editable SolidWorks files

| File | Purpose | Printable model |
|---|---|---|
| `Bottom Prototype.SLDPRT` | Base design with reference geometry | Use the part-only base for printing |
| `BottomCasePARTONLYV1.SLDPRT` | Part-only base | [case-bottom.stl](stl/case-bottom.stl) |
| [travel-cap.SLDPRT](solidworks/travel-cap.SLDPRT) | Current standalone protective travel cap | [travel-cap.stl](stl/travel-cap.stl) |
| `TestPrintHoles.SLDPRT` | Heat-set-insert coupon | [insert-test-coupon.stl](stl/insert-test-coupon.stl) |
| [LEDAlignmentJig.SLDPRT](solidworks/LEDAlignmentJig.SLDPRT) | Full-length jig with eight LED openings; design reference | [led-alignment-jig.stl](stl/led-alignment-jig.stl) |
| [LEDAlignmentJigShort.SLDPRT](solidworks/LEDAlignmentJigShort.SLDPRT) | Short jig with four LED openings; design reference | [led-alignment-jig-short.stl](stl/led-alignment-jig-short.stl) |
| `ChocKeyCap.SLDPRT` | Keycap reference | Reference geometry |
| `StenoFullASMV1.SLDASM` | Keyboard assembly | Assembly reference |
| `StenoFullASMV1SINGLEPART.SLDPRT` | Single-part keyboard reference | Assembly reference |
| `TopCaseV1.SLDPRT`, `TopCaseV2.SLDPRT`, `TopCaseV3.SLDPRT` | Earlier cap iterations; original filenames retained for assembly references | Earlier design references |

The directory also contains PCB, controller, switch, terminal, LED, diode, resistor, capacitor, fuse and buffer-package models used with these assemblies. Files ending in `.step.SLDPRT` or `.step.SLDASM` are native representations of those components.

Keep the SolidWorks files together. If prompted for an external reference, select the corresponding component in `solidworks/` or a STEP reference below. Use SolidWorks Pack and Go when making a separately linked assembly copy or renaming dependencies.

To export a printable part, save the edit and export only its printable body as an STL in **millimeters**. Exclude the PCB, switches and other reference bodies. STL stores a surface mesh, not editable feature history.

## Current travel cap

Use [travel-cap.SLDPRT](solidworks/travel-cap.SLDPRT), [travel-cap.step](step/travel-cap.step) or [travel-cap.stl](stl/travel-cap.stl) for the current cover. These contain only the cap body. The SolidWorks file contains a standalone solid rather than the original sketch/feature history; use direct editing or add features for further changes.

The cap adds **2.54 mm (0.1 inch) of height** over the previous design. The hooks and loops are on the opposite sides from the previous cap, the loops span the taller walls, and the hooks are centered vertically. A horizontal hook sits between the two loops to provide another retaining-band attachment point.

Slice the current STL for your printer. After printing, check clearance above the keycaps and the retaining-band fit with the keyboard installed in its base. The earlier cap's mesh and sliced jobs are in the [archive guide](../../archive/README.md#previous-travel-cap).

## STEP references

- [`travel-cap.step`](step/travel-cap.step): current standalone travel cap for use in other CAD tools.
- [`pcb-assembly.step`](step/pcb-assembly.step): PCB assembly for positioning the electronics inside the case.
- [`Choc_Stem_Choc_Size_Normal.step`](step/Choc_Stem_Choc_Size_Normal.step): keycap reference geometry.

The PCB model uses generic Pico geometry. Fit the Waveshare module with its USB-C socket aligned to the case opening. STEP files provide neutral CAD geometry; use native CAD when its feature history is needed. The current standalone cap is supplied as a solid in both native and STEP formats.

## STL files

STL has no unit field; select **millimeters** in the slicer.

| Model | Size (mm) | Purpose |
|---|---|---|
| [case-bottom.stl](stl/case-bottom.stl) | 254.286 × 70.286 × 6.336 | Keyboard base |
| [travel-cap.stl](stl/travel-cap.stl) | 254.286 × 87.355 × 22.973 | Current protective travel cap |
| [insert-test-coupon.stl](stl/insert-test-coupon.stl) | 6.350 × 48.260 × 5.080 | Insert hole-fit coupon |
| [led-alignment-jig.stl](stl/led-alignment-jig.stl) | 245.447 × 30.873 × 3.175 | Full-length, eight-opening LED jig reference |
| [led-alignment-jig-short.stl](stl/led-alignment-jig-short.stl) | 104.958 × 32.137 × 3.175 | Short, four-opening LED jig reference |

1. Open the mesh and select your printer, nozzle, filament and build plate.
2. Arrange it on the plate and account for any skirt or brim. Use center/arrange for the travel-cap mesh's offset origin.
3. Inspect orientation, walls, blind-hole floors, insert holes and underside pockets in the sliced preview.
4. Print the coupon, establish the insert fit, then print the base and cap.

## LED alignment jig

Two LED alignment jig designs are included: the [full-length jig](stl/led-alignment-jig.stl) has eight LED openings, and the [short jig](stl/led-alignment-jig-short.stl) has four. They were designed to hold LED packages in position while soldering. The intended approach was to tin all four PCB pads, position the LEDs with the jig, and reheat each pad to join the contacts.

**The jig approach did not work as intended during assembly.** Assembly returned to conventional hand soldering without a jig: tin one pad, position and tack the LED, then solder the remaining three contacts. Follow the [LED soldering steps in the build guide](../build-guide.md#solder-the-rgb-leds).

The [full-length SolidWorks part](solidworks/LEDAlignmentJig.SLDPRT), [short SolidWorks part](solidworks/LEDAlignmentJigShort.SLDPRT) and their STL files remain available as design references. Neither jig is required for assembly. The native parts include keyboard reference geometry; export only the jig body when creating a new STL. For inspecting or modifying either mesh in a slicer, use millimeters and drop its broad flat face onto the build plate to remove its Z offset.

## SV06 slicing settings

Use **OrcaSlicer with the standard Sovol SV06 profile and stock Marlin firmware**. The printer has a 220 × 220 × 250 mm build volume. Slice the STL files for this printer; the Bambu jobs below target different machines.

| Setting | Case-printing profile |
|---|---|
| Material / nozzle | Generic PLA, 1.75 mm filament / 0.4 mm nozzle |
| Nozzle / bed temperature | 220°C / 55°C; stay within the filament manufacturer's range |
| Layer height / first layer | 0.12 mm / 0.20 mm |
| Walls / top / bottom layers | 3 / 3 / 3 |
| Infill | 20% Triangles |
| First layer / first-layer infill | 15 / 20 mm/s |
| Outer / inner walls | 25 / 35 mm/s |
| Top surface / sparse infill | 20 / 45 mm/s |
| Small perimeters / gap infill | 15 / 20 mm/s |
| Travel / first-layer travel | 80 / 60 mm/s |
| Normal / outer-wall / top / first-layer acceleration | 500 / 300 / 300 / 300 mm/s² |
| Travel acceleration | 400 mm/s² |
| Brim | Outer only, 5 mm wide, 0.10 mm object gap |
| Travel planning | Avoid crossing walls enabled |

Keep **Emit limits to G-code disabled** in the machine-limit settings. Use the SV06 profile's complete start routine, with homing (`G28`) followed by automatic mesh probing (`G29`) at the start of each print. Set Z offset for your own printer; it is not a transferable project dimension. Tune support placement to the selected part and orientation.

For the current base and cap, **rotate approximately 45° in the XY plane**, center the part and drop it onto the plate. Their rotated mesh footprints are approximately **204 × 204 mm** and **206.5 × 206.5 mm**; a 5 mm outer brim brings these to about **214 × 214 mm** and **216.5 × 216.5 mm**. Check the complete brim, supports and start/purge path against the usable bed area in Preview before printing. These footprints describe the geometry, not a supplied SV06 G-code file.

## Printer jobs

The following pre-sliced jobs are **Bambu-specific alternatives** with their own saved settings. They are not SV06 G-code or the SV06 profile above. Each printer has a base and insert-coupon job. **Slice the current travel-cap STL separately**; the earlier cap jobs are retained in the [archive](../../archive/README.md#previous-travel-cap).

| Printer | Base | Insert coupon |
|---|---|---|
| Bambu A1 | [Base](print-jobs/A1/case-bottom.gcode.3mf) | [Coupon](print-jobs/A1/insert-test-coupon.gcode.3mf) |
| Bambu P1S | [Base](print-jobs/P1S/case-bottom.gcode.3mf) | [Coupon](print-jobs/P1S/insert-test-coupon.gcode.3mf) |
| Bambu P2S | [Base](print-jobs/P2S/case-bottom.gcode.3mf) | [Coupon](print-jobs/P2S/insert-test-coupon.gcode.3mf) |

These `.gcode.3mf` files use the named printer's **Bambu PLA Basic** profile with a **0.4 mm nozzle, textured PEI plate and 0.12 mm layer height**. The saved settings are consistent across the A1, P1S and P2S jobs:

| Part | Wall loops | Infill | Supports |
|---|---:|---|---|
| Base | 5 | 20% gyroid | Automatic tree supports enabled |
| Insert coupon | 3 | 15% gyroid | Automatic tree supports enabled |

Open a job in Bambu Studio and match its printer, nozzle, material and plate to your setup. These settings describe the saved jobs; slicer support generation still depends on the part's geometry and orientation. The current travel cap is also a PLA part; slice its current STL separately. For different hardware or edited geometry, reslice the STL.

## Case hardware and materials

| Item | Specification |
|---|---|
| Printed parts | PLA base, travel cap and insert coupon |
| Mounting screws | Eight **M2 × 5 mm** machine screws |
| Heat-set inserts | Eight **M2 internal thread × 3 mm length × 3.2 mm outside diameter** |
| PCB mounting holes | Eight 2.2 mm clearance holes through the 1.6 mm PCB |
| Cap retention | Rubber bands, routed through the cap anchors and under the keyboard/base |

The 5 mm screw length is measured beneath the head. After passing through the 1.6 mm PCB, approximately 3.4 mm enters the base. Seat each 3 mm insert flush at the PCB seating surface, with clearance below the screw tip. The insert's 3.2 mm outside diameter is not the printed installation-hole size; use the coupon to establish that fit for your inserts, filament and printer.

The cap uses ordinary rubber bands rather than a dedicated strap. Route them so they capture the keyboard/base and pull into a hook recess behind its tip. Assortment sizes vary; choose a band that remains seated with snug tension rather than excessive stretch.

Seat the PCB in the component recesses, fit the inserts and M2 × 5 mm screws, and keep the USB opening and key travel clear. Follow the [build guide](../build-guide.md) for assembly and cap retention.

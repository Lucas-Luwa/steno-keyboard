# Mechanical design and printing

This folder contains the case base, protective travel cap, heat-set-insert coupon, full-length and short LED alignment jig references, keycap references and keyboard assemblies. Use native CAD to edit features, STEP for reference geometry, STL to prepare your own prints, or a printer job for the matching setup.

## File formats

| Folder | Contents | Use |
|---|---|---|
| [`solidworks/`](solidworks/) | 22 `.SLDPRT` files and 12 `.SLDASM` files | Edit parts and work with the keyboard assembly |
| [`step/`](step/) | PCB assembly and keycap STEP references | Position reference geometry in CAD |
| [`stl/`](stl/) | Base, travel cap, insert coupon and two LED jig references | Slice printable geometry |
| [`print-jobs/`](print-jobs/) | Nine jobs, grouped by A1/P1S/P2S | Print using a matching printer setup |

Earlier base meshes are in [`archive/prints/`](../../archive/prints/), described in the [archive guide](../../archive/README.md).

## Editable SolidWorks files

| File | Purpose | Printable model |
|---|---|---|
| `Bottom Prototype.SLDPRT` | Base design with reference geometry | Use the part-only base for printing |
| `BottomCasePARTONLYV1.SLDPRT` | Part-only base | [case-bottom.stl](stl/case-bottom.stl) |
| `TopCaseV3.SLDPRT` | Protective travel cap | [travel-cap.stl](stl/travel-cap.stl) |
| `TestPrintHoles.SLDPRT` | Heat-set-insert coupon | [insert-test-coupon.stl](stl/insert-test-coupon.stl) |
| [LEDAlignmentJig.SLDPRT](solidworks/LEDAlignmentJig.SLDPRT) | Full-length jig with eight LED openings; design reference | [led-alignment-jig.stl](stl/led-alignment-jig.stl) |
| [LEDAlignmentJigShort.SLDPRT](solidworks/LEDAlignmentJigShort.SLDPRT) | Short jig with four LED openings; design reference | [led-alignment-jig-short.stl](stl/led-alignment-jig-short.stl) |
| `ChocKeyCap.SLDPRT` | Keycap reference | Reference geometry |
| `StenoFullASMV1.SLDASM` | Keyboard assembly | Assembly reference |
| `StenoFullASMV1SINGLEPART.SLDPRT` | Single-part keyboard reference | Assembly reference |
| `TopCaseV1.SLDPRT`, `TopCaseV2.SLDPRT` | Earlier cap iterations | Earlier design references |

The directory also contains PCB, controller, switch, terminal, LED, diode, resistor, capacitor, fuse and buffer-package models used with these assemblies. Files ending in `.step.SLDPRT` or `.step.SLDASM` are native representations of those components.

Keep the SolidWorks files together. If prompted for an external reference, select the corresponding component in `solidworks/` or a STEP reference below. Use SolidWorks Pack and Go when making a separately linked assembly copy or renaming dependencies.

To export a printable part, save the edit and export only its printable body as an STL in **millimeters**. Exclude the PCB, switches and other reference bodies. STL stores a surface mesh, not editable feature history.

## STEP references

- [`pcb-assembly.step`](step/pcb-assembly.step): PCB assembly for positioning the electronics inside the case.
- [`Choc_Stem_Choc_Size_Normal.step`](step/Choc_Stem_Choc_Size_Normal.step): keycap reference geometry.

The PCB model uses generic Pico geometry. Fit the Waveshare module with its USB-C socket aligned to the case opening. STEP files provide neutral CAD geometry; use the native part to edit case features and dimensions.

## STL files

STL has no unit field; select **millimeters** in the slicer.

| Model | Size (mm) | Purpose |
|---|---|---|
| [case-bottom.stl](stl/case-bottom.stl) | 254.286 × 70.286 × 6.336 | Keyboard base |
| [travel-cap.stl](stl/travel-cap.stl) | 254.286 × 87.366 × 20.433 | Protective travel cap |
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

## Printer jobs

Each printer has a base, cap and coupon job:

| Printer | Base | Travel cap | Insert coupon |
|---|---|---|---|
| Bambu A1 | [Base](print-jobs/A1/case-bottom.gcode.3mf) | [Cap](print-jobs/A1/travel-cap.gcode.3mf) | [Coupon](print-jobs/A1/insert-test-coupon.gcode.3mf) |
| Bambu P1S | [Base](print-jobs/P1S/case-bottom.gcode.3mf) | [Cap](print-jobs/P1S/travel-cap.gcode.3mf) | [Coupon](print-jobs/P1S/insert-test-coupon.gcode.3mf) |
| Bambu P2S | [Base](print-jobs/P2S/case-bottom.gcode.3mf) | [Cap](print-jobs/P2S/travel-cap.gcode.3mf) | [Coupon](print-jobs/P2S/insert-test-coupon.gcode.3mf) |

These `.gcode.3mf` files contain sliced jobs for the named printer, with a **0.4 mm nozzle, PLA, textured PEI plate and 0.12 mm layer height**. Open a job in Bambu Studio and match its printer, nozzle, material and plate to your setup. For different hardware or edited geometry, reslice the STL.

## Case hardware and assembly

The case uses eight M2 mounting positions and M2 × 3 mm heat-set inserts with nominal 3.2 mm outside diameter. Use the coupon to establish the printed hole fit. The cap uses a hook/anchor arrangement for a retaining band.

Seat the PCB in the component recesses, fit the inserts, select screw lengths for the stack, and keep the USB opening and key travel clear. Follow the [build guide](../build-guide.md) for assembly and cap retention.

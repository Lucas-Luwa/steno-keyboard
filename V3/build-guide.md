# Build Steno V3

This guide covers parts, case printing, soldering, firmware configuration and final assembly.

## 1. Gather the parts

Use the [bill of materials](hardware/bom.csv) for the electronics. The case and assembly materials are:

| Item | Specification |
|---|---|
| Keycaps | 30 Kailh Choc V1-compatible keycaps |
| PCB mounting screws | **Eight M2 × 5 mm machine screws** |
| Heat-set inserts | **Eight M2-thread inserts, 3 mm long and 3.2 mm outside diameter** |
| Printed base, travel cap and insert coupon | **PLA** |
| Cap retention | Rubber bands looped through the cap anchors and under the keyboard/base |
| USB cable | USB-C data cable |

The mounting stack uses the 5 mm screw length measured beneath the head: passing through the 1.6 mm PCB leaves approximately 3.4 mm entering the base. Seat the 3 mm insert flush at the PCB seating surface and keep the screw tip clear of the blind-hole floor. The 3.2 mm insert dimension is its outside diameter, not the installation-hole diameter.

Use the [mechanical guide](mechanical/README.md#case-hardware-and-materials) for the hardware details and [saved print settings](mechanical/README.md#printer-jobs).

Use the component packages in the [electronics guide](hardware/README.md). Its package table connects assembly part names to the schematic labels. The [sourcing note](hardware/README.md#parts-sourcing) identifies AliExpress, AIVON and RobotShop as the suppliers used for the prototype.

## 2. Print the case parts

Open the [STL files](mechanical/README.md#stl-files) in your slicer and select millimeters. For a Sovol SV06, use the [OrcaSlicer PLA settings and diagonal bed placement](mechanical/README.md#sv06-slicing-settings). [Bambu-specific printer jobs](mechanical/README.md#printer-jobs) are supplied for the base and insert coupon; slice the [current travel cap](mechanical/stl/travel-cap.stl) separately. Use G-code generated for your own printer.

Print the insert coupon first. Install an insert into each hole size, allow it to cool and choose the fit that seats flush without bulging, spinning or pulling loose. Apply that hole fit to the base, then print the base and travel cap.

For CAD changes, use the [SolidWorks files](mechanical/README.md#editable-solidworks-files) and export only the printable body. The [current cap part](mechanical/solidworks/travel-cap.SLDPRT) is a standalone solid for direct editing or adding features. Keep reference electronics and switches out of the STL.

## 3. Assemble the electronics

1. Inspect the bare PCB's pads, holes and tracks.
2. Solder the diodes, resistor, capacitors, fuse, LED buffer and LEDs in their marked orientations. Align diode cathodes and LED pin 1 with the footprints.
3. Fit the controller with its USB-C connector at the case opening and solder the castellated pads.
4. Fit and solder the switches, then attach the keycaps.
5. Inspect the joints and remove bridges. With power disconnected, check for a short between the USB supply and ground.

### Solder the RGB LEDs

Use conventional hand soldering, tinning **one pad first** for each LED:

1. With power disconnected, check the LED's orientation against its pinout and the PCB footprint, then apply flux to the pads.
2. Lightly tin one PCB pad.
3. Hold the LED by its sides with tweezers. Reheat the tinned pad and position the LED flat against the board, aligning all four contacts with their pads.
4. Let the first joint cool, then solder the diagonally opposite contact and the remaining two contacts.
5. Inspect all four joints for bridges and unjoined contacts. Use brief heating and keep the iron clear of the LED's plastic body and light-emitting surface.

The [LED alignment jig](mechanical/README.md#led-alignment-jig) was tried with all four pads pre-tinned, but it did not work as intended. Assembly returned to the one-pad-first method above. CAD and STL files for both the full-length and short jigs are retained as design references; printing a jig is not part of the assembly procedure.

Parts on the PCB's underside need the orientation shown from that side. Use the [schematic](images/schematic.svg), [front layout](images/pcb-front.svg) and [back layout](images/pcb-back.svg) while assembling.

## 4. Power and configure the keyboard

Connect over USB and check the controller and supply before enabling the LEDs. The [MicroPython LED tests](firmware/led-tests/README.md) can check the complete RGB chain before switches or Javelin are required; begin with the 16/255 RGB/chase test. The [prototype results](firmware/led-tests/results.md) record the later colour, brightness and pattern sessions.

Then apply the [Javelin hardware configuration](firmware/README.md), build and flash the complete firmware/data setup, and use a limited RGB brightness setting during initial operation. Javelin replaces MicroPython; the Python diagnostic animations are not automatically installed as Javelin effects.

Test every matrix position and its assigned steno or auxiliary action. Exercise simultaneous chords, release timing, all eight LEDs and a USB disconnect/reconnect. Keep total current within the USB supply budget.

## 5. Mount the PCB

Install the heat-set inserts in the base and let them cool. Seat the PCB over the mounting positions, keeping underside components clear of the recess floors. Tighten the M2 screws evenly without bottoming them out or bending the PCB.

Ensure the USB connector is accessible and the cable does not load the controller sideways. Press all keys through their travel and operate multi-key chords with the case fitted.

## 6. Fit the travel cap

Place the [current travel cap](mechanical/README.md#current-travel-cap) over the keyboard with clearance above the keycaps. Route the retaining band through the loops and onto a hook so it captures the keyboard/base, and seat it behind the hook tip. The cap includes two full-height loops, centered side hooks and an additional horizontal hook between the loops; choose the attachment path that holds the cap securely without pressing the keys.

Remove and refit the cap, then tilt and gently jostle the closed assembly to check retention. The keyboard is ready for normal use when the controls, USB connection, LEDs, mounting and cap operate as described.

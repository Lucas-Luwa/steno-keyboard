# Build Steno V3

This guide covers parts, case printing, soldering, firmware configuration and final assembly.

## 1. Gather the parts

Use the [bill of materials](hardware/bom.csv) for the electronics. Add 30 Kailh Choc V1 keycaps, eight M2 mounting screws, eight M2 × 3 mm heat-set inserts with 3.2 mm outside diameter, a retaining band for the cap, and a USB-C data cable. Select screw lengths for the PCB, base and insert stack without bottoming out in the inserts.

Use the component packages in the [electronics guide](hardware/README.md). Its package table connects assembly part names to the schematic labels.

## 2. Print the case parts

Open the [STL files](mechanical/README.md#stl-files) in your slicer, or use a matching [printer job](mechanical/README.md#printer-jobs). Set units to millimeters and select your printer, nozzle, material and build plate.

Print the insert coupon first. Install an insert into each hole size, allow it to cool and choose the fit that seats flush without bulging, spinning or pulling loose. Apply that hole fit to the base, then print the base and travel cap.

For CAD changes, edit the [SolidWorks source](mechanical/README.md#editable-solidworks-files) and export only the printable body. Keep reference electronics and switches out of the STL.

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

Place the cap over the keyboard and route the retaining band between the anchor and hook so it captures the keyboard/base. Seat the band behind the hook tip. Seat the cap on the case with clearance above the keycaps.

Remove and refit the cap, then tilt and gently jostle the closed assembly to check retention. The keyboard is ready for normal use when the controls, USB connection, LEDs, mounting and cap operate as described.

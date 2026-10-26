# Steno V3 Javelin / Lapwing

Prepared 2026-10-25 for the Waveshare RP2040-Plus **16 MB** prototype. The custom hardware firmware and 31-button script compile successfully, and a combined Lapwing UF2 has passed offline image checks. **Installed on the prototype on 2026-10-25.** USB enumeration, custom configuration, all-up trigger, Repeat processing, US Windows Alt host layout, dictionary states, saved script read-back and on-device lookups passed. The builder also confirmed the physical S, T and H-L typing sequence produced “is it hello”. The [MicroPython LED tests](../led-tests/README.md) are separate firmware; their 134-cue showcase and 35-cue extension have already run on the prototype.

## Physical layout

Viewed from the typing side, USB at the top:

```text
Esc  #  T  P  H  *       *  F  P  L  T  D
Tab  S  K  W  R  *       *  R  B  G  S  Z
         #  A  O         E  U  #
```

Esc is SW1 and Tab is SW7. The top S position (SW2) acts as # through the engine key map; the lower S (SW8) remains S. Both outer thumb keys act as #. All four star keys have independent physical indexes. BOOTSEL uses index 28 and enters the ROM bootloader. It is separate from the 30 keyboard switches. [key-matrix.csv](key-matrix.csv) maps each switch to its electrical position and Javelin button index; [layout.json](layout.json) defines the visual geometry embedded in the firmware.

The [hardware header](steno_v3.h) scans GP0–GP4 as cathode rows and GP5–GP10 as pulled-up columns. Eight WS2812B LEDs use GP22. The [button script](steno_v3.jss) enables button-state events and sets all LEDs off at startup. The MicroPython animations and their current limiter are **not ported into this script**. Live laptop audio input and on-device FFT remain future software work.

## Dictionary preset

The official [builder](https://lim.au/#/software/javelin-steno) supplies the dictionary/system/host-layout data. The initial preset follows [Lapwing's Javelin setup](https://lapwing.aerick.ca/Appendix-C.html).

| Priority | Dictionary | Initially enabled |
|---|---|---|
| 1 | Emily's Symbols | Yes |
| 2 | abby-left-hand-modifiers.json | Yes |
| 3 | emily-modifiers.json | Yes |
| 4 | Jeff's Phrasing | Yes |
| 5 | Jeff's Numbers | No |
| 6 | lapwing-javelin-additions.json | Yes |
| 7 | lapwing-semi-modal-movement.json | No |
| 8 | lapwing-commands.json | Yes |
| 9 | lapwing-numbers.json | Yes |
| 10 | lapwing-uk-additions.json | Yes |
| 11 | lapwing-proper-nouns.json | Yes |
| 12 | lapwing-base.json | Yes |

Other options: US Windows Alt host layout, default keyboard protocol, spaces before output, Repeat on, First Up off, Jeff's Modifiers off, Show-Stroke off, reverse lookup tables on. Emily's Symbols uses its normal AO spacing option. The included movement and Jeff's Numbers dictionaries can be enabled later. Windows Alt has limited Unicode coverage; plain English, normal symbols and shortcuts do not require installing Plover. Advanced Unicode can be configured later.

## Reproduce the build

Upstream repositories are distributed under their own licenses, including Javelin's PolyForm Noncommercial license. Consult upstream before commercial use. Dependencies and generated binaries are not vendored here.

| Component | Tested revision/version |
|---|---|
| [javelin-steno-pico](https://github.com/jthlim/javelin-steno-pico) | da5eb7ca467714f9f8caa01f60eff69025082659 |
| [javelin-steno](https://github.com/jthlim/javelin-steno) | e093126aed38e062ce4b646d92ba99a956e0b6d0 |
| [javelin_steno_script](https://github.com/jthlim/javelin_steno_script) | f3a66d46ebf87609d2b9ba45a8af73802fb7805e |
| Pico SDK | 2.3.1, 079c6f39023649b154152db30f1d781e884879bc |
| TinyUSB (SDK submodule) | 86ad6e56c1700e85f1c5678607a762cfe3aa2f47 |
| Arm GNU Toolchain | 15.2.rel1 |
| CMake / Ninja | 4.4.4 / 1.13.2 |
| Dart SDK | 3.13.7 |

1. Clone those revisions, initialize the SDK's TinyUSB submodule, and link or copy the engine into `javelin-steno-pico/javelin` as upstream describes. Copy `steno_v3.h` into `javelin-steno-pico/config/`.
2. Set `PICO_SDK_PATH` and `PICO_TOOLCHAIN_PATH` for the shell, with the compiler and Ninja on PATH. From the Pico bindings checkout:

   ```powershell
   cmake -S . -B build -G Ninja -DJAVELIN_BOARD=steno_v3 -DPICO_BOARD=waveshare_rp2040_plus_16mb -DPICO_PLATFORM=rp2040 -DPICO_NO_PICOTOOL=1 -DCMAKE_BUILD_TYPE=Release
   cmake --build build --parallel 6
   ```

   The hardware binary is `build/javelin-steno-pico.bin`. The tested build uses 230,584 flash bytes and 88,728 RAM bytes. `PICO_NO_PICOTOOL` suppresses the SDK's UF2 conversion; the packager below creates the combined UF2.
3. Copy the official script compiler repository's `lib/` into this directory's `compiler/lib/`. The included minimal pubspec builds the upstream pure Dart compiler without its Flutter editor. From `compiler/`:

   ```powershell
   dart pub get
   dart run bin/compile.dart ../steno_v3.jss ../steno_v3-script.bin
   ```

   This emits a **458-byte JSS4 script for 31 buttons**, including Esc, Tab and BOOTSEL. A stock Uni v4 builder compiles only 29 buttons; using that bytecode unmodified would lose the two extra keys.
4. In the official builder, select The Uni v4 **as a data-image template only**, add the Lapwing bundle, and use the preset above. Under expert options, select top S as # and leave inner # unchecked. Use **Load Script** to load `steno_v3.jss`; loading the file also supplies the matching source storage. Create and download a full firmware image. Do not flash that stock hardware image to this PCB.
5. From this directory, combine the downloaded data with the custom hardware and 31-button script:

   ```powershell
   python package.py --builder path/to/downloaded.uf2 --hardware path/to/javelin-steno-pico.bin --script steno_v3-script.bin --source steno_v3.jss --output steno-v3-javelin-lapwing.uf2
   ```

   The packager validates the RP2040 UF2 family/ranges, reset vector, compiled key handlers, dictionary states and completion timestamp, source storage, and config flags. It replaces the hardware and button bytecode and updates the source-storage CRC. It preserves the builder's system, word list, host layouts and dictionary data. It writes a SHA-256 sidecar and verifies the UF2 round trip. The tested combined file is 13,942,784 bytes; its data fits within the 16 MB flash. The 256 KB user-dictionary area at the end is initialized by Javelin on first boot.

Use the local [first-word typing page](first-words.html) for the initial S, T, H-L and undo exercise.

## Install and check

Installing Javelin replaces the MicroPython runtime. Save any MicroPython files first. With USB disconnected, hold BOOTSEL while connecting a data cable, then release. Copy **the combined custom UF2** to the RPI-RP2 drive and wait for the drive to disconnect and the keyboard to restart. The LEDs start off.

Use the [Javelin web tools](https://lim.au/#/software/javelin-steno) to inspect firmware settings, active dictionaries, key state and paper tape. Keep `steno_v3.jss` available when editing scripts. Check the two auxiliary keys, every steno position, simultaneous chords, complete releases and USB reconnect. Confirm Lapwing words in a disposable text field, undo with *, then test numbers and Emily's Symbols. Successful lookup confirms dictionary data; physical typing still needs its own check. Do not rerun a stock Uni update over the custom hardware configuration.

To return to the saved light demos, reinstall the correct Waveshare RP2040-Plus 16 MB MicroPython firmware and use the [LED test launcher](../led-tests/README.md). Returning to Javelin uses the combined custom UF2 again; export any user dictionary before reinitializing firmware/data.

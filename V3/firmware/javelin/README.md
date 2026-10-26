# Steno V3 Javelin / Lapwing

Prepared 2026-10-25 for the Waveshare RP2040-Plus **16 MB** prototype. The custom hardware firmware and 31-button script compile successfully, and a combined Lapwing UF2 has passed offline image checks. The active v2 layout is described below. **Installed on the prototype on 2026-10-25.** USB enumeration, custom configuration, all-up trigger, Repeat processing, US Windows Alt host layout, dictionary states, saved script read-back and on-device lookups passed. The builder also confirmed the physical S, T and H-L typing sequence produced “is it hello”. The [MicroPython LED tests](../led-tests/README.md) are separate firmware; their 134-cue showcase and 35-cue extension have already run on the prototype.

## Physical layout — v2

Applied 2026-10-25 after the initial layout. Viewed from the typing side, USB at the top:

```text
Tab  S  T  P  H  #       *  F  P  L  T  D
Ent  S  K  W  R  #       *  R  B  G  S  Z
        Fn  A  O         E  U  Bsp
```

SW1 is Tab, SW7 is Enter, both S positions produce left S, both left inner keys are #, the two right inner keys remain *, SW25 is hold-Fn, and SW30 is ordinary Backspace. The four vowel positions stay A O E U. The upper/lower S keys retain separate physical steno identities, so overlapping them does not release the other prematurely. The engine configuration maps S1 to stroke bit 1 (left S). Asterisk remains steno undo; Backspace deletes characters.

Fn is momentary. Holding the outer left thumb key selects:

```text
Esc  --  --  --  -- LED     Home PgUp  Up PgDn End Del
Ent Ctrl Shft Alt Win --      -- Left Down Right Dim Brt
        Fn  --  --          Spc Ins Bsp
```

Each key latches its action when pressed and releases that same action, even if Fn is released first. Release a steno chord before switching layers. Reserved `--` positions do nothing on Fn. The outer right thumb remains Backspace on both layers. LED toggle is Fn + upper-left #; dim/brighten are Fn + right-hand lower S/Z. Lighting starts off and uses steady magenta, with red/blue levels 16–128/255 in steps of 16 and a default of 64. The maximum estimated LED channel current is 160.63 mA for eight LEDs, excluding controller/idle draw; this is a command-based estimate, not a meter reading. Effects/FFT are separate future work.

[key-matrix.csv](key-matrix.csv) maps switch references to Javelin indexes; [layout.json](layout.json) supplies visual geometry. The [hardware header](steno_v3.h) still scans GP0–GP4 cathode rows and GP5–GP10 pulled-up columns; GP22 drives eight LEDs. BOOTSEL stays index 28. This update changed the script, source storage and S1 config byte, not the hardware application or dictionaries.

The compiled 690-byte v2 script passed checks using the upstream Javelin interpreter for every base/Fn position, overlapping S keys, layer release order, modifier chords, LED brightness bounds and all-off cleanup. On-device source read-back, unchanged dictionaries, embedded/all-up mode, startup globals and Lapwing lookups passed. **The builder confirmed the v2 physical checks passed: both S positions output “is”, outer-right-thumb Backspace removes a character, and hold-Fn + the upper far-left key sends Escape.** Other v2 physical layer positions and LED controls have interpreter coverage but were not individually confirmed by this physical check. The initial v1 “is it hello” physical test passed before this change.

The [v1 script](previous/steno_v3-layout-v1.jss) is retained for rollback. Its S1 mapping must be restored to stroke bit 0 (#) when reverting; changing only its script is insufficient. The original complete v1 UF2 and a new complete v2 UF2 are saved with the setup deliverables. Both use the same hardware pins. Export any user dictionary before rebuilding or replacing data.

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

   This emits a **690-byte JSS4 script for 31 buttons**, including both layers and BOOTSEL. A stock Uni v4 builder compiles only 29 buttons; using that bytecode unmodified would lose the two extra keys.
4. In the official builder, select The Uni v4 **as a data-image template only**, add the Lapwing bundle, and use the preset above. The v2 packager sets top S back to S and embeds the supplied custom script/source independently of the template’s layout options. Create and download a full firmware image. Do not flash that stock hardware image to this PCB.
5. From this directory, combine the downloaded data with the custom hardware and 31-button script:

   ```powershell
   python package.py --builder path/to/downloaded.uf2 --hardware path/to/javelin-steno-pico.bin --script steno_v3-script.bin --source steno_v3.jss --output steno-v3-javelin-layout-v2.uf2 --top-s-as-s
   ```

   The packager validates the RP2040 UF2 family/ranges, reset vector, compiled callback table, dictionary states and completion timestamp, source storage, and config flags. It replaces the hardware and button bytecode, sets S1’s stroke mapping, and stores the supplied script source with its matching bytecode CRC. It preserves the builder's system, word list, host layouts and dictionary data. It writes a SHA-256 sidecar and verifies the UF2 round trip. The combined data fits within the 16 MB flash. The 256 KB user-dictionary area at the end is initialized by Javelin on first boot.

Use the local [first-word typing page](first-words.html) for the initial S, T, H-L and undo exercise.

## Install and check

Installing Javelin replaces the MicroPython runtime. Save any MicroPython files first. With USB disconnected, hold BOOTSEL while connecting a data cable, then release. Copy **the combined custom UF2** to the RPI-RP2 drive and wait for the drive to disconnect and the keyboard to restart. The LEDs start off.

Use the [Javelin web tools](https://lim.au/#/software/javelin-steno) to inspect firmware settings, active dictionaries, key state and paper tape. Keep `steno_v3.jss` available when editing scripts. Check the two auxiliary keys, every steno position, simultaneous chords, complete releases and USB reconnect. Confirm Lapwing words in a disposable text field, undo with *, then test numbers and Emily's Symbols. Successful lookup confirms dictionary data; physical typing still needs its own check. Do not rerun a stock Uni update over the custom hardware configuration.

To return to the saved light demos, reinstall the correct Waveshare RP2040-Plus 16 MB MicroPython firmware and use the [LED test launcher](../led-tests/README.md). Returning to Javelin uses the combined custom UF2 again; export any user dictionary before reinitializing firmware/data.

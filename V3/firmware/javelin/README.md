# Steno V3 Javelin / Lapwing

The Waveshare RP2040-Plus **16 MB** prototype runs embedded Javelin/Lapwing with the v2 base key layout and the current **v6.1 ambient-lighting script**. The lighting update was installed on 2026-10-27 in the reserved script/source regions. The C++ hardware application, steno mode, all-up trigger, US Windows Alt host layout, configuration and dictionary list were preserved. Source/bytecode CRC readback passed. The first onboard lighting version also persisted through a device restart with lighting off. The builder previously confirmed that selecting LED 3 starts onboard coals and that the pink selection display is clear. The builder confirmed the slot-1 bouncing wave with fully dark LEDs outside the moving streak. The T-only 20/50/100% brightness selector and matching pink/cyan/amber indicators passed compilation and source/bytecode CRC readback; physical confirmation of the new selector remains pending.

The editable installed source is [`steno_v3.jss`](steno_v3.jss). It compiles to JSS4 bytecode and runs inside Javelin. Existing timers and the PIO/DMA LED driver handle the animations without a PC helper or manual core allocation.

## Physical layout

Viewed from the typing side, USB at the top:

```text
Tab  S  T  P  H  #       *  F  P  L  T  D
Ent  S  K  W  R  #       *  R  B  G  S  Z
        Fn  A  O         E  U  Bsp
```

SW1 is Tab, SW7 is Enter, both S positions produce left S, both left inner keys are #, the two right inner keys remain *, SW25 is hold-Fn, and SW30 is ordinary Backspace. The vowels remain A O E U. The two S keys retain their separate physical steno identities; S1 maps to stroke bit 1 (left S). Asterisk remains steno undo; Backspace deletes characters.

Fn is momentary. Hold the outer-left-thumb key to select:

```text
Esc   -- Brt* Pat* Off* Guard    Home PgUp  Up PgDn End Del
Ent Ctrl Shft Alt Win   --      -- Left Down Right -- --
         Fn   --   --         Spc Ins Bsp
```

`Brt*`, `Pat*` and `Off*` require the upper-left # guard as well as Fn; those keys produce no output by themselves on Fn. Fn + Tab, the upper far-left key, remains Escape. The old magenta toggle and lower-right S/Z dim/brighten functions have been removed. Every other key retains its press-time action and releases that same action even if Fn is released first. Release a steno chord before switching layers.

## Onboard lighting

![Fn and idle-pattern controls](../../images/lighting-controls.png)

**All LEDs start off after every power-up**, with 20% brightness selected. Hold the outer-left-thumb **Fn first**, then use the **upper-left #** together with a top-row left-hand selector. The # and selector can go down together or in either order, provided they overlap.

| Selector | Action |
|---|---|
| T | Open brightness selection at 20%; tap during its blinks to step through 50%, 100%, then 20% again. If off, enable original breathing colors. |
| H | Turn all LEDs off immediately |
| P | Open at LED 1; tap again during selection blinks to advance |

Keep Fn + # held while tapping T. Each new brightness selection opens at **20% / pink**. Additional T taps during its five blinks advance to **50% / cyan**, then **100% / amber**, then wrap to 20%. Each tap restarts the five blinks; let them finish to close the selector. Brightness confirmation always uses LED 1. S no longer controls lighting and remains unused on Fn; ordinary steno S is unchanged. T keeps the active pattern, or enables breathing when lighting was off.

Keep Fn + # held while tapping P. The first tap opens the selector at LED 1 (Bouncing wave), regardless of the pattern that was running. Further P taps during the five selection blinks advance one choice and restart the blinks. When the five blinks finish, that choice takes effect and the selector closes. The next P tap opens at LED 1 again. For example, choosing coals always takes three taps: wave, breathing, coals. Brightness confirmations do not count as an open P-selection window. A held selector does not auto-repeat; release it before tapping again. The command keys produce no text and add no waiting delay to normal typing.

One of the **first five physical LEDs, left to right**, flashes pink at 20%, cyan at 50%, or amber at 100% to identify the choice:

| Pattern indicator | Choice |
|---|---|
| LED 1 (LED17/index 0) | Bouncing wave |
| LED 2 (LED16/index 1) | Original breathing colors |
| LED 3 (LED15/index 2) | Glowing coals |
| LED 4 (LED14/index 3) | Left-to-right color drift |
| LED 5 (LED13/index 4) | Long-rest pulses |

The selection order is **wave → breathing → coals → drift → long-rest pulses → wave**. Each confirmation uses five 200 ms pulses separated by 200 ms off, at the selected brightness. T brightness selection confirms on LED 1. P pattern selection uses the pattern's LED position. Both use pink for 20%, cyan for 50%, and amber for 100%. Opening P closes the T selection window; opening T closes the P selection window. The next tap of the other selector starts at its first choice. H is immediate off without confirmation. Off is no longer a P-selector slot; startup still remains Off.

| Idle pattern | Behavior |
|---|---|
| Bouncing wave | A soft glow about three LEDs wide travels left to right and back with soft fading edges and fully dark LEDs outside the moving streak. At 20% or 50%, each crossing takes 7 seconds with a 1-second rest at each end; at 100%, 11.2 seconds with 1.6-second rests. Motion eases near the ends, and color blends to the next contrasting palette color during the final rest of each round trip. |
| Original breathing | All LEDs show one color at a time. At 20% or 50%, fade in/out for 5 seconds each; at 100%, 8 seconds each. No peak hold, then 3 seconds dark before the next color. |
| Glowing coals | LEDs independently move between nearly dark red embers and brighter orange peaks. Integer smooth curves approximate the accepted PC preview without floating-point trigonometry. Motion is slower at 100%. |
| Left-to-right drift | A contrasting new color enters at the leftmost LED and gradually replaces the old color toward the right. At 20% or 50%, each LED blends for 3 seconds with a 2-second stagger; a transition starts every 22 seconds. At 100%, these times are 1.6 times longer. |
| Long-rest pulses | Whole-board color pulses, fading up/down for 5 seconds each at 20% or 50%, or 8 seconds each at 100%, followed by 10 seconds completely off. |

Breathing and pulses use **red, orange, yellow, green, cyan, blue, purple, pink**. Drift and wave use contrasting saturated colors so their movement is visible.

Typing immediately selects **steady green at the chosen 20%, 50%, or 100% brightness**, for every enabled pattern. Green remains while keys are held and for **five minutes after the last release**, then fades to black over 2 seconds and returns to the selected idle effect. Selecting a pattern starts it after confirmation so it can be seen immediately; typing afterward begins the five-minute hold. `IDLE_DELAY_MS = 300000` controls that delay.

USB suspend/disconnection turns lighting off. Settings are not repeatedly written to flash: power-up returns to Off and 20%, and lighting must be deliberately selected again.

All frames, including per-LED patterns, share a conservative **320 mA estimated LED-current budget** after brightness scaling. This is a calculation, not a measurement; controller and LED idle draw are additional. The firmware declares a 500 mA USB budget. Keep the frame limiter when adding effects.

## Computer compatibility

The board enumerates as a USB keyboard and runs both stenography and lighting onboard. No Python, LedFx, OpenRGB or Plover application is needed on the host. Use a USB data cable and a compatible USB port/adapter. Current output is configured for **US Windows Alt** with a matching US keyboard layout. Basic typing can work on other hosts, but Mac/Linux layouts, Unicode entry and shortcuts may need corresponding host-layout settings; Windows Alt Unicode behavior is not portable to every operating system.

## Configuration and previous versions

[`key-matrix.csv`](key-matrix.csv) maps switch references to Javelin indexes; [`layout.json`](layout.json) supplies visual geometry. The [`hardware header`](steno_v3.h) scans GP0-GP4 cathode rows and GP5-GP10 pulled-up columns; GP22 drives eight LEDs. BOOTSEL remains index 28. The ambient-lighting update changes only the script and stored source, not the hardware application, engine configuration or dictionaries.

The earlier v2 base/Fn layout passed interpreter checks and physical S/Backspace/Fn-Escape checks on 2026-10-25. That coverage is historical and does not replace physical checks of the new lighting controls. The [previous magenta v2 script](previous/steno_v3-layout-v2.jss) is retained for rollback with the same S1 mapping. The [v1 script](previous/steno_v3-layout-v1.jss) requires restoring S1 to stroke bit 0 (#) when reverting; changing only that script is insufficient. Existing complete v1/v2 UF2 files are historical and do not contain the current ambient lighting.

For a keyboard already running this custom hardware build, update only the compiled 31-button script and matching stored source through Javelin's supported script/flash tools. Back up the current script first and retain dictionary/configuration data. A full combined UF2 build below is for reproducing the entire installation; export any user dictionary before replacing full firmware/data.

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

   This emits a **2,580-byte JSS4 script for 31 buttons**, including both layers, onboard ambient lighting and BOOTSEL. A stock Uni v4 builder compiles only 29 buttons; using that bytecode unmodified would lose the two extra keys.
4. In the official builder, select The Uni v4 **as a data-image template only**, add the Lapwing bundle, and use the preset above. The packager sets top S back to S and embeds the supplied custom script/source independently of the template’s layout options. Create and download a full firmware image. Do not flash that stock hardware image to this PCB.
5. From this directory, combine the downloaded data with the custom hardware and 31-button script:

   ```powershell
   python package.py --builder path/to/downloaded.uf2 --hardware path/to/javelin-steno-pico.bin --script steno_v3-script.bin --source steno_v3.jss --output steno-v3-javelin-layout-v2.uf2 --top-s-as-s
   ```

   The packager validates the RP2040 UF2 family/ranges, reset vector, compiled callback table, dictionary states and completion timestamp, source storage, and config flags. It replaces the hardware and button bytecode, sets S1’s stroke mapping, and stores the supplied script source with its matching bytecode CRC. It preserves the builder's system, word list, host layouts and dictionary data. It writes a SHA-256 sidecar and verifies the UF2 round trip. The combined data fits within the 16 MB flash. The 256 KB user-dictionary area at the end is initialized by Javelin on first boot.

Use the local [first-word typing page](first-words.html) for the initial S, T, H-L and undo exercise.

## Install and check

Installing Javelin replaces the MicroPython runtime. Save any MicroPython files first. With USB disconnected, hold BOOTSEL while connecting a data cable, then release. Copy **the combined custom UF2** to the RPI-RP2 drive and wait for the drive to disconnect and the keyboard to restart. The LEDs start off.

Use the [Javelin web tools](https://lim.au/#/software/javelin-steno) to inspect firmware settings, active dictionaries, key state and paper tape. Keep the current `steno_v3.jss` available when editing scripts. Its lighting runs onboard; no PC lighting application is needed. Check the two auxiliary keys, every steno position, simultaneous chords, complete releases and USB reconnect. Confirm Lapwing words in a disposable text field, undo with *, then test numbers and Emily's Symbols. Successful lookup confirms dictionary data; physical typing still needs its own check. Do not rerun a stock Uni update over the custom hardware configuration.

To return to the saved light demos, reinstall the correct Waveshare RP2040-Plus 16 MB MicroPython firmware and use the [LED test launcher](../led-tests/README.md). Returning to Javelin uses the combined custom UF2 again; export any user dictionary before reinitializing firmware/data.

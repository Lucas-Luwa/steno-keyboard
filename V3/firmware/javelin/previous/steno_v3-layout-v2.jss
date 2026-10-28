// Steno V3 layout v2: Tab/Enter, split S, left #, right *, Fn and Backspace.
// Keep the hardware configuration and dictionaries; config keyMap[S1] = SL (1).
// Fn is momentary. Each key keeps its press-time action until physically released.
// LED controls: static magenta, starts off, channel level 16..128 (default 64).
var fnHeld;
var ledEnabled;
var ledLevel;
var held[31];

func showLeds() {
  var level = ledEnabled ? ledLevel : 0;
  setRgb(0, level, 0, level);
  setRgb(1, level, 0, level);
  setRgb(2, level, 0, level);
  setRgb(3, level, 0, level);
  setRgb(4, level, 0, level);
  setRgb(5, level, 0, level);
  setRgb(6, level, 0, level);
  setRgb(7, level, 0, level);
}
func init() {
  fnHeld = 0;
  ledEnabled = 0;
  ledLevel = 64;
  setEnableButtonStates(1);
  showLeds();
}
// Action encoding: 0 = unused; 1..64 = steno key + 1;
// 65..320 = USB scan code + 65; 1000/1001/1002 = LED toggle/dim/brighten.
func pressMapped(button, normal, alternate) {
  var action = fnHeld ? alternate : normal;
  if (action >= 1000) {
    held[button] = 0;
    if (action == 1000) { ledEnabled = !ledEnabled; }
    if (action == 1001 && ledLevel > 16) { ledLevel = ledLevel - 16; }
    if (action == 1002 && ledLevel < 128) { ledLevel = ledLevel + 16; }
    showLeds();
  } else {
    held[button] = action;
    if (action > 0 && action <= 64) { pressStenoKey(action - 1); }
    if (action >= 65) { pressScanCode(action - 65); }
  }
}
func releaseMapped(button) {
  var action = held[button];
  held[button] = 0;
  if (action > 0 && action <= 64) { releaseStenoKey(action - 1); }
  if (action >= 65) { releaseScanCode(action - 65); }
}
func onPress0() { pressMapped(0, SK_S1 + 1, 0); }
func onRelease0() { releaseMapped(0); }
func onPress1() { pressMapped(1, SK_TL + 1, 0); }
func onRelease1() { releaseMapped(1); }
func onPress2() { pressMapped(2, SK_PL + 1, 0); }
func onRelease2() { releaseMapped(2); }
func onPress3() { pressMapped(3, SK_HL + 1, 0); }
func onRelease3() { releaseMapped(3); }
func onPress4() { pressMapped(4, SK_NUM1 + 1, 1000); }
func onRelease4() { releaseMapped(4); }
func onPress5() { pressMapped(5, SK_STAR2 + 1, SC_HOME + 65); }
func onRelease5() { releaseMapped(5); }
func onPress6() { pressMapped(6, SK_FR + 1, SC_PAGE_UP + 65); }
func onRelease6() { releaseMapped(6); }
func onPress7() { pressMapped(7, SK_PR + 1, SC_UP + 65); }
func onRelease7() { releaseMapped(7); }
func onPress8() { pressMapped(8, SK_LR + 1, SC_PAGE_DOWN + 65); }
func onRelease8() { releaseMapped(8); }
func onPress9() { pressMapped(9, SK_TR + 1, SC_END + 65); }
func onRelease9() { releaseMapped(9); }
func onPress10() { pressMapped(10, SK_DR + 1, SC_DELETE + 65); }
func onRelease10() { releaseMapped(10); }
func onPress11() { pressMapped(11, SK_S2 + 1, SC_L_CTRL + 65); }
func onRelease11() { releaseMapped(11); }
func onPress12() { pressMapped(12, SK_KL + 1, SC_L_SHIFT + 65); }
func onRelease12() { releaseMapped(12); }
func onPress13() { pressMapped(13, SK_WL + 1, SC_L_ALT + 65); }
func onRelease13() { releaseMapped(13); }
func onPress14() { pressMapped(14, SK_RL + 1, SC_L_META + 65); }
func onRelease14() { releaseMapped(14); }
func onPress15() { pressMapped(15, SK_NUM2 + 1, 0); }
func onRelease15() { releaseMapped(15); }
func onPress16() { pressMapped(16, SK_STAR4 + 1, 0); }
func onRelease16() { releaseMapped(16); }
func onPress17() { pressMapped(17, SK_RR + 1, SC_LEFT + 65); }
func onRelease17() { releaseMapped(17); }
func onPress18() { pressMapped(18, SK_BR + 1, SC_DOWN + 65); }
func onRelease18() { releaseMapped(18); }
func onPress19() { pressMapped(19, SK_GR + 1, SC_RIGHT + 65); }
func onRelease19() { releaseMapped(19); }
func onPress20() { pressMapped(20, SK_SR + 1, 1001); }
func onRelease20() { releaseMapped(20); }
func onPress21() { pressMapped(21, SK_ZR + 1, 1002); }
func onRelease21() { releaseMapped(21); }
func onPress22() { fnHeld = 1; }
func onRelease22() { fnHeld = 0; }
func onPress23() { pressMapped(23, SK_A + 1, 0); }
func onRelease23() { releaseMapped(23); }
func onPress24() { pressMapped(24, SK_O + 1, 0); }
func onRelease24() { releaseMapped(24); }
func onPress25() { pressMapped(25, SK_E + 1, SC_SPACE + 65); }
func onRelease25() { releaseMapped(25); }
func onPress26() { pressMapped(26, SK_U + 1, SC_INSERT + 65); }
func onRelease26() { releaseMapped(26); }
func onPress27() { pressMapped(27, SC_BACKSPACE + 65, SC_BACKSPACE + 65); }
func onRelease27() { releaseMapped(27); }
func onPress28() { console("launch_bootloader"); }
func onRelease28() {}
func onPress29() { pressMapped(29, SC_TAB + 65, SC_ESC + 65); }
func onRelease29() { releaseMapped(29); }
func onPress30() { pressMapped(30, SC_ENTER + 65, SC_ENTER + 65); }
func onRelease30() { releaseMapped(30); }

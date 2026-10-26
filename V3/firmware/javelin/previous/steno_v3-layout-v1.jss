// Steno V3: 30 switches plus BOOTSEL, embedded Lapwing.
// Top-left steno S1 is remapped to # by the firmware configuration.
// Far-left extra switches: SW1 = Esc; SW7 = Tab.
// Lighting starts off; MicroPython animation tests are separate firmware.
func init() {
  setEnableButtonStates(1);
  setRgb(0, 0, 0, 0);
  setRgb(1, 0, 0, 0);
  setRgb(2, 0, 0, 0);
  setRgb(3, 0, 0, 0);
  setRgb(4, 0, 0, 0);
  setRgb(5, 0, 0, 0);
  setRgb(6, 0, 0, 0);
  setRgb(7, 0, 0, 0);
}

func onPress0() { pressStenoKey(SK_S1); }
func onRelease0() { releaseStenoKey(SK_S1); }
func onPress1() { pressStenoKey(SK_TL); }
func onRelease1() { releaseStenoKey(SK_TL); }
func onPress2() { pressStenoKey(SK_PL); }
func onRelease2() { releaseStenoKey(SK_PL); }
func onPress3() { pressStenoKey(SK_HL); }
func onRelease3() { releaseStenoKey(SK_HL); }
func onPress4() { pressStenoKey(SK_STAR1); }
func onRelease4() { releaseStenoKey(SK_STAR1); }
func onPress5() { pressStenoKey(SK_STAR2); }
func onRelease5() { releaseStenoKey(SK_STAR2); }
func onPress6() { pressStenoKey(SK_FR); }
func onRelease6() { releaseStenoKey(SK_FR); }
func onPress7() { pressStenoKey(SK_PR); }
func onRelease7() { releaseStenoKey(SK_PR); }
func onPress8() { pressStenoKey(SK_LR); }
func onRelease8() { releaseStenoKey(SK_LR); }
func onPress9() { pressStenoKey(SK_TR); }
func onRelease9() { releaseStenoKey(SK_TR); }
func onPress10() { pressStenoKey(SK_DR); }
func onRelease10() { releaseStenoKey(SK_DR); }
func onPress11() { pressStenoKey(SK_S2); }
func onRelease11() { releaseStenoKey(SK_S2); }
func onPress12() { pressStenoKey(SK_KL); }
func onRelease12() { releaseStenoKey(SK_KL); }
func onPress13() { pressStenoKey(SK_WL); }
func onRelease13() { releaseStenoKey(SK_WL); }
func onPress14() { pressStenoKey(SK_RL); }
func onRelease14() { releaseStenoKey(SK_RL); }
func onPress15() { pressStenoKey(SK_STAR3); }
func onRelease15() { releaseStenoKey(SK_STAR3); }
func onPress16() { pressStenoKey(SK_STAR4); }
func onRelease16() { releaseStenoKey(SK_STAR4); }
func onPress17() { pressStenoKey(SK_RR); }
func onRelease17() { releaseStenoKey(SK_RR); }
func onPress18() { pressStenoKey(SK_BR); }
func onRelease18() { releaseStenoKey(SK_BR); }
func onPress19() { pressStenoKey(SK_GR); }
func onRelease19() { releaseStenoKey(SK_GR); }
func onPress20() { pressStenoKey(SK_SR); }
func onRelease20() { releaseStenoKey(SK_SR); }
func onPress21() { pressStenoKey(SK_ZR); }
func onRelease21() { releaseStenoKey(SK_ZR); }
func onPress22() { pressStenoKey(SK_NUM1); }
func onRelease22() { releaseStenoKey(SK_NUM1); }
func onPress23() { pressStenoKey(SK_A); }
func onRelease23() { releaseStenoKey(SK_A); }
func onPress24() { pressStenoKey(SK_O); }
func onRelease24() { releaseStenoKey(SK_O); }
func onPress25() { pressStenoKey(SK_E); }
func onRelease25() { releaseStenoKey(SK_E); }
func onPress26() { pressStenoKey(SK_U); }
func onRelease26() { releaseStenoKey(SK_U); }
func onPress27() { pressStenoKey(SK_NUM2); }
func onRelease27() { releaseStenoKey(SK_NUM2); }
func onPress28() { console("launch_bootloader"); }
func onRelease28() {}
func onPress29() { pressScanCode(SC_ESC); }
func onRelease29() { releaseScanCode(SC_ESC); }
func onPress30() { pressScanCode(SC_TAB); }
func onRelease30() { releaseScanCode(SC_TAB); }

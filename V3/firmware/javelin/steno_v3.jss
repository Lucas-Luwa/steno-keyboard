// Steno V3 layout v6.1: five autonomous idle patterns; original v2 base mapping.
// Fn+# P opens at LED1/Wave; further P taps during confirmation advance.
// LED1=Wave, LED2=Breathing, LED3=Coals, LED4=Drift, LED5=Long-rest pulses.
// Off is Fn+# H; internal pattern 0 remains Off and 5 is Wave.
// T opens at 20%; repeat during its blinks for 50%, 100%, then 20% again.
// T confirms on LED1; P uses the pattern LED. Pink=20%, cyan=50%, amber=100%.
// Fn first; upper-left # and top T/H/P may be pressed in either order/together.
// Five-minute idle delay. No host program is needed for lighting or steno.
const IDLE_DELAY_MS = 300000;
const RETURN_FADE_MS = 2000;
const LIGHT_TIMER_ID = 421;
var fnHeld;
var guardHeld;
var held[31];
var lightMode;
var lightLevel;
var activeCount;
var hasActivity;
var lastActivity;
var idleStart;
var blinkActive;
var blinkStart;
var blinkPhase;
var lastR;
var lastG;
var lastB;
var chordLatched;
var chordTarget;
var idlePattern;
var chosenBrightness;
var pixelR[8];
var pixelG[8];
var pixelB[8];
var sentR[8];
var sentG[8];
var sentB[8];
var selectorActive;
var confirmationColor;
var confirmationLed;
var brightnessSelectorActive;

func smoothLevel(t) var {
  if (t < 0) { return 0; }
  if (t > 1000) { return 1000; }
  return (t*t/1000)*(3000-2*t)/1000;
}

// All frames share the same conservative power budget, including per-LED effects.
func flushFrame() {
  var sum = 0;
  for (var i = 0; i < 8; i += 1) {
    pixelR[i] = pixelR[i]*lightLevel/255;
    pixelG[i] = pixelG[i]*lightLevel/255;
    pixelB[i] = pixelB[i]*lightLevel/255;
    sum += pixelR[i]+pixelG[i]+pixelB[i];
  }
  for (var i = 0; i < 8; i += 1) {
    if (sum > 4080) {
      pixelR[i] = pixelR[i]*4080/sum;
      pixelG[i] = pixelG[i]*4080/sum;
      pixelB[i] = pixelB[i]*4080/sum;
    }
    if (pixelR[i] != sentR[i] || pixelG[i] != sentG[i] || pixelB[i] != sentB[i]) {
      setRgb(i, pixelR[i], pixelG[i], pixelB[i]);
      sentR[i] = pixelR[i]; sentG[i] = pixelG[i]; sentB[i] = pixelB[i];
    }
  }
}

func allLeds(r, g, b) {
  for (var i = 0; i < 8; i += 1) {
    pixelR[i] = r; pixelG[i] = g; pixelB[i] = b;
  }
  flushFrame();
  lastR = pixelR[0]; lastG = pixelG[0]; lastB = pixelB[0];
}

func breathingLeds(elapsed, gap) {
  var fade = lightMode == 100 ? 8000 : 5000;
  var duration = 2*fade + gap;
  var color = (elapsed/duration)%8;
  var phase = elapsed%duration;
  var level = 0;
  if (phase < fade) { level = smoothLevel(phase*1000/fade); }
  else if (phase < 2*fade) { level = 1000-smoothLevel((phase-fade)*1000/fade); }
  var r = 0; var g = 0; var b = 0;
  if (color == 0) { r = 255; }
  if (color == 1) { r = 255; g = 128; }
  if (color == 2) { r = 255; g = 255; }
  if (color == 3) { g = 255; }
  if (color == 4) { g = 255; b = 255; }
  if (color == 5) { b = 255; }
  if (color == 6) { r = 170; b = 255; }
  if (color == 7) { r = 255; b = 128; }
  allLeds(r*level/1000, g*level/1000, b*level/1000);
}

// An integer smooth-wave approximation avoids floating-point trigonometry.
func emberWave(elapsed, period, offset) var {
  var phase = (elapsed%period + period/4 + period*offset/10000)%period;
  if (phase < period/2) { return smoothLevel(phase*2000/period); }
  return 1000-smoothLevel((phase-period/2)*2000/period);
}

func coalsLeds(elapsed) {
  if (lightMode == 100) { elapsed = elapsed/8*5; }
  for (var i = 0; i < 8; i += 1) {
    var a = emberWave(elapsed, 11938+1068*i, (i*3676)%10000);
    var b = emberWave(elapsed, 29531+1948*i, (i*2276)%10000);
    var heat = (820*a+180*b)/1000;
    var glow = 12+988*(heat*heat/1000)/1000;
    var warmth = 12+450*(a*a/1000)/1000;
    pixelR[i] = 255*glow/1000;
    pixelG[i] = pixelR[i]*warmth/1000;
    pixelB[i] = 0;
  }
  flushFrame();
  lastR = -1; lastG = -1; lastB = -1;
}

func driftRed(color) var {
  if (color == 0 || color == 2 || color == 5 || color == 6) { return 255; }
  if (color == 7) { return 150; }
  return 0;
}
func driftGreen(color) var {
  if (color == 1 || color == 4) { return 255; }
  if (color == 2) { return 110; }
  if (color == 6) { return 220; }
  return 0;
}
func driftBlue(color) var {
  if (color == 1 || color == 3 || color == 7) { return 255; }
  if (color == 5) { return 180; }
  return 0;
}
func driftLeds(elapsed) {
  if (lightMode == 100) { elapsed = elapsed/8*5; }
  var old = (elapsed/22000)%8;
  var next = (old+1)%8;
  var phase = elapsed%22000;
  var r0 = driftRed(old); var g0 = driftGreen(old); var b0 = driftBlue(old);
  var r1 = driftRed(next); var g1 = driftGreen(next); var b1 = driftBlue(next);
  for (var i = 0; i < 8; i += 1) {
    var blend = smoothLevel((phase-2000*i)*1000/3000);
    pixelR[i] = (r0*(1000-blend)+r1*blend)/1000;
    pixelG[i] = (g0*(1000-blend)+g1*blend)/1000;
    pixelB[i] = (b0*(1000-blend)+b1*blend)/1000;
  }
  flushFrame();
  lastR = -1; lastG = -1; lastB = -1;
}

// Smooth three-LED glow on black, with eased turns and endpoint rests.
func waveLeds(elapsed) {
  if (lightMode == 100) { elapsed = elapsed/8*5; }
  var phase = elapsed%16000;
  var position = 0;
  if (phase < 7000) { position = 7*smoothLevel(phase*1000/7000); }
  else if (phase < 8000) { position = 7000; }
  else if (phase < 15000) { position = 7000-7*smoothLevel((phase-8000)*1000/7000); }
  // Blend toward the next contrasting color during the final endpoint rest.
  var color = (elapsed/16000)%8;
  var next = (color+1)%8;
  var blend = smoothLevel((phase-15000)*1000/1000);
  var r = (driftRed(color)*(1000-blend)+driftRed(next)*blend)/1000;
  var g = (driftGreen(color)*(1000-blend)+driftGreen(next)*blend)/1000;
  var b = (driftBlue(color)*(1000-blend)+driftBlue(next)*blend)/1000;
  var arrival = smoothLevel(elapsed);
  for (var i = 0; i < 8; i += 1) {
    var distance = i*1000-position;
    if (distance < 0) { distance = -distance; }
    var glow = 1000-smoothLevel(distance*1000/1500);
    glow = glow*arrival/1000;
    pixelR[i] = r*glow/1000;
    pixelG[i] = g*glow/1000;
    pixelB[i] = b*glow/1000;
  }
  flushFrame();
  lastR = -1; lastG = -1; lastB = -1;
}

func idleLeds(elapsed) {
  if (idlePattern == 1) { breathingLeds(elapsed, 3000); }
  if (idlePattern == 2) { coalsLeds(elapsed); }
  if (idlePattern == 3) { driftLeds(elapsed); }
  if (idlePattern == 4) { breathingLeds(elapsed, 10000); }
  if (idlePattern == 5) { waveLeds(elapsed); }
}

func lightTick() {
  var now = getTime();
  if (blinkActive) {
    var elapsed = (now-blinkStart)&0x7fffffff;
    if (elapsed < 2000) {
      var phase = elapsed/200;
      if (phase != blinkPhase) {
        blinkPhase = phase;
        lastR = -1; lastG = -1; lastB = -1;
        allLeds(0, 0, 0);
        if ((phase%2) == 0) {
          // Brightness uses LED1; pattern selection uses its own slot LED.
          var led = confirmationLed;
          var r = confirmationColor == 50 ? 0 : lightLevel;
          var g = confirmationColor == 20 ? 0 : (confirmationColor == 50 ? lightLevel : 128*lightLevel/255);
          var b = confirmationColor == 100 ? 0 : (confirmationColor == 50 ? lightLevel : 128*lightLevel/255);
          setRgb(led, r, g, b);
          sentR[led] = r; sentG[led] = g; sentB[led] = b;
        }
        lastR = -1; lastG = -1; lastB = -1;
      }
      return;
    }
    blinkActive = 0;
    selectorActive = 0;
    brightnessSelectorActive = 0;
    idleStart = now;
  }
  if (!lightMode) { allLeds(0, 0, 0); stopTimer(LIGHT_TIMER_ID); return; }
  if (activeCount > 0) { allLeds(0, 255, 0); return; }
  if (hasActivity) {
    var age = (now-lastActivity)&0x7fffffff;
    if (age <= IDLE_DELAY_MS) { allLeds(0, 255, 0); return; }
    if (age < IDLE_DELAY_MS+RETURN_FADE_MS) {
      var level = 1000-smoothLevel((age-IDLE_DELAY_MS)*1000/RETURN_FADE_MS);
      allLeds(0, 255*level/1000, 0);
      return;
    }
    idleLeds(age-IDLE_DELAY_MS-RETURN_FADE_MS);
    return;
  }
  idleLeds((now-idleStart)&0x7fffffff);
}

func confirmSelection(showPattern) {
  stopTimer(LIGHT_TIMER_ID);
  selectorActive = 0;
  brightnessSelectorActive = 0;
  confirmationColor = chosenBrightness;
  confirmationLed = showPattern ? (idlePattern == 5 ? 0 : idlePattern) : 0;
  lightMode = idlePattern == 0 ? 0 : chosenBrightness;
  lightLevel = (chosenBrightness*255+50)/100;
  allLeds(0, 0, 0);
  hasActivity = activeCount > 0;
  lastActivity = getTime();
  blinkStart = lastActivity;
  blinkPhase = -1; blinkActive = 1;
  lightTick();
  startTimer(LIGHT_TIMER_ID, 33, 1, @{ lightTick(); });
}

func lightsOff() {
  stopTimer(LIGHT_TIMER_ID);
  lightMode = 0; idlePattern = 0; blinkActive = 0; selectorActive = 0;
  brightnessSelectorActive = 0;
  lightLevel = (chosenBrightness*255+50)/100;
  allLeds(0, 0, 0);
}

func brightnessButton() {
  if (brightnessSelectorActive && blinkActive) {
    if (chosenBrightness == 20) { chosenBrightness = 50; }
    else if (chosenBrightness == 50) { chosenBrightness = 100; }
    else { chosenBrightness = 20; }
  }
  else { chosenBrightness = 20; }
  if (idlePattern == 0) { idlePattern = 1; }
  confirmSelection(0);
  brightnessSelectorActive = 1;
}

func patternButton() {
  if (selectorActive && blinkActive) {
    if (idlePattern == 5) { idlePattern = 1; }
    else if (idlePattern == 4) { idlePattern = 5; }
    else { idlePattern += 1; }
  }
  else { idlePattern = 5; }
  confirmSelection(1);
  selectorActive = 1;
}

func init() {
  fnHeld = 0; guardHeld = 0; activeCount = 0; hasActivity = 0;
  chordLatched = 0; chordTarget = -1;
  idlePattern = 0; chosenBrightness = 20; selectorActive = 0;
  brightnessSelectorActive = 0;
  for (var i = 0; i < 8; i += 1) {
    sentR[i] = -1; sentG[i] = -1; sentB[i] = -1;
  }
  setEnableButtonStates(1);
  lightsOff();
  setScript(SCRIPT_ID_CONNECTION_UPDATE, @{
    if (isUsbSuspended() || !isUsbConnected()) { lightsOff(); }
  });
}

func resetLightLatch() {
  if (chordLatched) {
    // A fresh selector press is required; Fn+# may stay held between taps.
    if (!isButtonPressed(chordTarget)) {
      chordLatched = 0; chordTarget = -1;
    }
  }
}

func tryLightChord() {
  if (chordLatched || !fnHeld || !guardHeld) { return; }
  if (!isButtonPressed(22) || !isButtonPressed(4)) { return; }
  var count = 0; var target = -1;
  if (held[1] == 1002 && isButtonPressed(1)) { target = 1; count += 1; }
  if (held[2] == 1004 && isButtonPressed(2)) { target = 2; count += 1; }
  if (held[3] == 1003 && isButtonPressed(3)) { target = 3; count += 1; }
  if (count != 1) { return; }
  chordLatched = 1; chordTarget = target;
  if (target == 1) { brightnessButton(); }
  else if (target == 2) { patternButton(); }
  else { lightsOff(); }
}

// Each key latches its press-time action, preserving Fn release behavior.
func pressMapped(button, normal, alternate) {
  if (fnHeld && button == 4) {
    guardHeld = 1; held[button] = 1000; tryLightChord(); return;
  }
  if (fnHeld) {
    // These were already reserved (no output) on the Fn layer.
    if (button == 0) { held[button] = 1000; return; }
    if (button == 1) { held[button] = 1002; tryLightChord(); return; }
    if (button == 2) { held[button] = 1004; tryLightChord(); return; }
    if (button == 3) { held[button] = 1003; tryLightChord(); return; }
  }
  var action = fnHeld ? alternate : normal;
  held[button] = action;
  if (action > 0) {
    activeCount += 1; hasActivity = 1; lastActivity = getTime();
    if (lightMode && !blinkActive) { allLeds(0, 255, 0); }
  }
  if (action > 0 && action <= 64) { pressStenoKey(action-1); }
  if (action >= 65) { pressScanCode(action-65); }
}

func releaseMapped(button) {
  var action = held[button];
  held[button] = 0;
  if (action >= 1000) {
    if (button == 4) { guardHeld = 0; }
    resetLightLatch(); return;
  }
  if (action > 0 && action <= 64) { releaseStenoKey(action-1); }
  if (action >= 65) { releaseScanCode(action-65); }
  if (action > 0) {
    if (activeCount > 0) { activeCount -= 1; }
    lastActivity = getTime();
  }
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
func onPress20() { pressMapped(20, SK_SR + 1, 0); }
func onRelease20() { releaseMapped(20); }
func onPress21() { pressMapped(21, SK_ZR + 1, 0); }
func onRelease21() { releaseMapped(21); }
func onPress22() { fnHeld = 1; }
func onRelease22() {
  fnHeld = 0; guardHeld = 0;
  // A new Fn session must not inherit a selector pressed before Fn.
  if (held[0] >= 1000) { held[0] = 1000; }
  if (held[1] >= 1000) { held[1] = 1000; }
  if (held[2] >= 1000) { held[2] = 1000; }
  if (held[3] >= 1000) { held[3] = 1000; }
  resetLightLatch();
}
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

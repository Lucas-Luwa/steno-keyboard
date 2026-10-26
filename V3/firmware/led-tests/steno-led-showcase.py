"""Eight-LED visual showcase for Lucas's steno board; MicroPython on RP2040.

GP22 -> buffer -> 330R -> eight WS2812Bs, physically left to right.
No matrix pins, HID events, filesystem writes or audio capture.
Beat effects use synthetic events: this is not an FFT implementation.
"""
from machine import Pin
from neopixel import NeoPixel
from time import ticks_ms, ticks_diff, sleep_ms
import math
import random
import json

LED_PIN = 22
LED_REFERENCES = ('LED17', 'LED16', 'LED15', 'LED14',
                  'LED13', 'LED12', 'LED8', 'LED28')
COUNT = 8
DEFAULT_LEVEL = 64
FRAME_MS = 25
# Estimated light-producing current, not measured USB current or a hardware limit.
CHANNEL_MA = 20
EMITTER_BUDGET_MA = 320
LEVELS = (1, 2, 4, 8, 16, 24, 32, 48, 64, 96, 128, 160, 192, 224, 255)
BLACK = (0, 0, 0)
COLORS = (
    ('red', (255, 0, 0)), ('green', (0, 255, 0)),
    ('blue', (0, 0, 255)), ('yellow', (255, 255, 0)),
    ('cyan', (0, 255, 255)), ('magenta', (255, 0, 255)),
    ('orange', (255, 96, 0)), ('amber', (255, 40, 0)),
    ('lime', (128, 255, 0)), ('emerald', (0, 255, 64)),
    ('teal', (0, 160, 128)), ('sky-blue', (0, 160, 255)),
    ('royal-blue', (48, 0, 255)), ('violet', (128, 0, 255)),
    ('purple', (192, 0, 255)), ('hot-pink', (255, 0, 96)),
    ('rose', (255, 32, 96)), ('coral', (255, 80, 40)),
    ('lavender', (180, 96, 255)), ('pastel-pink', (255, 112, 176)),
    ('ice-blue', (80, 176, 255)), ('warm-purple', (255, 48, 192)),
)
COLOR = dict(COLORS)
PALETTES = {
    'neon': (COLOR['magenta'], COLOR['cyan'], COLOR['violet'], COLOR['orange']),
    'fire': ((12, 0, 0), (160, 0, 0), (255, 48, 0), (255, 176, 0)),
    'ocean': ((0, 0, 24), (0, 24, 160), (0, 160, 192), (0, 255, 128)),
    'aurora': (COLOR['purple'], COLOR['teal'], COLOR['royal-blue'], COLOR['emerald']),
}
CATALOG = []


def cue(ident, section, title, kind, seconds=6, **params):
    CATALOG.append(dict(id=ident, section=section, title=title, kind=kind,
                        seconds=seconds, params=params))


for i, ref in enumerate(LED_REFERENCES):
    cue('map-%02d' % (i + 1), 'mapping', 'Position %d: %s' % (i + 1, ref),
        'position', 2, index=i)
cue('map-left', 'mapping', 'Four left LEDs only', 'bank', 3, bank=0)
cue('map-right', 'mapping', 'Four right LEDs only', 'bank', 3, bank=1)
for name, rgb in COLORS:
    cue('color-' + name, 'colors', name.replace('-', ' '),
        'solid', 3, color=name)
for name in ('red', 'green', 'blue', 'magenta', 'cyan', 'orange', 'lavender'):
    cue('steps-' + name, 'brightness', 'Raw brightness steps: ' + name,
        'steps', len(LEVELS) * 1.5, color=name)
for a, b in ((16, 32), (16, 64), (16, 128), (16, 255), (64, 128), (128, 255)):
    cue('compare-%d-%d' % (a, b), 'brightness', 'Magenta A/B: %d versus %d' % (a, b),
        'compare', 8, a=a, b=b, color='magenta')
for name in ('red', 'magenta', 'lavender'):
    cue('ramp-' + name, 'brightness', 'Continuous raw ramp: ' + name,
        'ramp', 8, color=name, gamma=False)
    cue('gamma-' + name, 'brightness', 'Perceptual-style ramp: ' + name,
        'ramp', 8, color=name, gamma=True)
cue('density-one', 'brightness', 'One LED versus eight at the same channel level',
    'density', 8, color='magenta')

for ident, title, params in (
    ('chase-red', 'One red dot, left to right', dict(color='red')),
    ('chase-blue-back', 'One blue dot, right to left', dict(color='blue', reverse=True)),
    ('chase-rainbow', 'One dot changes hue as it moves', dict(rainbow=True)),
    ('chase-pair', 'Two adjacent moving dots', dict(width=2)),
    ('chase-opposed', 'Two dots move in opposite directions', dict(opposed=True)),
    ('bounce', 'Single dot bounces at the ends', dict(bounce=True)),
    ('scanner', 'Scanner with a soft trail', dict(bounce=True, trail=3)),
    ('comet-short', 'Short comet tail', dict(trail=2)),
    ('comet-long', 'Long comet tail', dict(trail=5)),
    ('chase-fast', 'Fast single-dot chase', dict(rate=7)),
    ('chase-slow', 'Slow single-dot chase', dict(rate=1.5)),
):
    cue(ident, 'motion', title, 'chase', 7, **params)
for ident, title, kind in (
    ('fill-drain', 'Fill then drain the row', 'fill'),
    ('color-wipe', 'Colour wipe across all eight', 'wipe'),
    ('rainbow-conveyor', 'Moving saturated rainbow', 'rainbow'),
    ('gradient-conveyor', 'Moving purple/cyan gradient', 'gradient'),
    ('sine-wave', 'Smooth wave of brightness', 'sine'),
    ('two-waves', 'Two overlapping coloured waves', 'two-waves'),
    ('bouncing-particle', 'Smooth bouncing point with subpixel blending', 'particle'),
    ('random-walk', 'A dot wanders between neighbours', 'walk'),
    ('binary', 'Slow binary count in magenta', 'binary'),
):
    cue(ident, 'motion', title, kind, 8)

for ident, title, kind, params in (
    ('mirror-out', 'Mirrored centre-to-edge dots', 'mirror', dict(inward=False)),
    ('mirror-in', 'Mirrored edge-to-centre dots', 'mirror', dict(inward=True)),
    ('mirror-comet', 'Mirrored centre-out comet trails', 'mirror', dict(trail=True)),
    ('mirror-fill', 'Both halves fill out from the centre', 'mirror-fill', {}),
    ('mirror-breathe', 'Both halves breathe together', 'breathe', {}),
    ('cross-breathe', 'Left and right take turns breathing', 'cross-breathe', {}),
    ('alternate-banks', 'Left/right colour alternation', 'alternate', {}),
    ('split-colors', 'Purple left / cyan right', 'split', {}),
    ('checkerboard', 'Alternating individual LEDs', 'checker', {}),
    ('paired-zones', 'Four two-LED zones', 'zones', {}),
    ('centre-glow', 'Centre glows with a soft falloff', 'centre', {}),
    ('edges-glow', 'Outer edges glow with a soft falloff', 'edges', {}),
):
    cue(ident, 'symmetry', title, kind, 8, **params)

for ident, title, kind, params in (
    ('breathe-purple', 'Slow purple breathing', 'breathe', dict(color='purple')),
    ('breathe-blue', 'Slow blue breathing', 'breathe', dict(color='blue')),
    ('hue-fade', 'All LEDs fade through saturated hues', 'hue', {}),
    ('palette-neon', 'Neon palette transitions', 'palette', dict(palette='neon')),
    ('palette-ocean', 'Ocean palette transitions', 'palette', dict(palette='ocean')),
    ('fire', 'Warm flickering embers', 'texture', dict(palette='fire')),
    ('ocean-shimmer', 'Blue/teal shimmer', 'texture', dict(palette='ocean')),
    ('aurora', 'Slow purple/green aurora', 'texture', dict(palette='aurora')),
    ('sparkle-sparse', 'Sparse coloured sparkles', 'sparkle', dict(density=1)),
    ('sparkle-dense', 'Dense coloured sparkles', 'sparkle', dict(density=3)),
    ('twinkle', 'Soft independent twinkles', 'twinkle', {}),
    ('raindrops', 'Drops appear and fade away', 'drops', {}),
    ('random-colors', 'Random saturated colour per LED', 'random-colors', {}),
    ('noise-flow', 'Flowing multicolour texture', 'noise', {}),
):
    cue(ident, 'textures', title, kind, 10, **params)

for bpm in (60, 90, 120, 150, 180):
    cue('beat-pulse-%d' % bpm, 'beats', 'Synthetic beat pulse: %d BPM' % bpm,
        'beat', 8, bpm=bpm, mode='pulse')
for ident, title, mode in (
    ('beat-alternate', 'Alternate halves on each beat', 'alternate'),
    ('beat-color', 'Choose a saturated colour on each beat', 'color'),
    ('beat-step', 'Advance one LED per beat', 'step'),
    ('beat-mirror', 'Launch a mirrored wave on each beat', 'mirror'),
    ('beat-burst', 'Random spatial burst on each beat', 'burst'),
    ('beat-kick', 'Bass/kick: strong pulse with decay', 'kick'),
    ('beat-snare', 'Snare/backbeat: alternate accented beats', 'snare'),
    ('beat-hats', 'Hi-hat-style eighth-note sparkles', 'hats'),
    ('beat-layered', 'Synthetic kick, snare and hats together', 'layered'),
    ('beat-subdivide', 'Quarter/eighth/sixteenth-note motion', 'subdivide'),
    ('beat-half-double', 'Half-time then double-time feel', 'half-double'),
    ('beat-swing', 'Swinging pairs of light pulses', 'swing'),
    ('beat-tempo-change', 'Tempo ramps from 75 to 165 BPM', 'tempo'),
    ('beat-build-drop', 'Build, brief gap, then a drop', 'drop'),
    ('beat-silence', 'Activity, silence with decay, activity', 'silence'),
    ('beat-pattern-picker', 'Synthetic events choose different patterns', 'picker'),
    ('beat-features', 'Synthetic bass/mid/treble independently shape the LEDs', 'features'),
):
    cue(ident, 'beats', title, 'beat', 12, bpm=120, mode=mode)

for effect in ('chase', 'comet', 'wave', 'sparkle'):
    cue('detail-' + effect, 'detail', 'Four zones versus eight pixels: ' + effect,
        'detail', 12, effect=effect)

for hz in (1, 2, 4, 8, 12, 16):
    cue('flash-%dhz' % hz, 'flashes', 'Labelled magenta flashes: %d Hz' % hz,
        'flash', 5, hz=hz, level=16 if hz >= 8 else 32)
cue('flash-alternating', 'flashes', 'Alternating banks, four changes/second',
    'flash-alternate', 6, level=16)
cue('flash-double', 'flashes', 'Double flash per synthetic beat', 'flash-double', 6, level=16)
cue('flash-triplet', 'flashes', 'Three-flash burst per synthetic beat', 'flash-triplet', 6, level=16)
cue('flash-random', 'flashes', 'Irregular magenta bursts', 'flash-random', 6, level=16)

SECTIONS = ('mapping', 'colors', 'brightness', 'motion', 'symmetry',
            'textures', 'beats', 'detail', 'flashes')


def clamp(x):
    return max(0.0, min(1.0, x))


def scale(color, value):
    return tuple(int(c * clamp(value)) for c in color)


def mix(a, b, value):
    value = clamp(value)
    return tuple(int(a[i] + (b[i] - a[i]) * value) for i in range(3))


def hsv(hue):
    hue = (hue % 1.0) * 6
    sector = int(hue)
    x = int((hue - sector) * 255)
    return ((255, x, 0), (255-x, 255, 0), (0, 255, x),
            (0, 255-x, 255), (x, 0, 255), (255, 0, 255-x))[sector]


def palette(name, value):
    colors = PALETTES[name]
    p = (value % 1.0) * len(colors)
    i = int(p)
    return mix(colors[i], colors[(i + 1) % len(colors)], p - i)


def hash01(index, step):
    return ((index * 374761393 + step * 668265263 + 1447) & 65535) / 65535.0


def triangle(t):
    return 1 - abs((t % 2) - 1)


def blank():
    return [BLACK] * COUNT


def feature_wave(t, x, rate=1):
    return (math.sin(t * rate + x) + 1) * 0.5


def frame_for(item, t, duration, state):
    """Return an eight-pixel 0..255 frame and raw channel-level multiplier."""
    kind, p = item['kind'], item['params']
    frame = blank()
    level = p.get('level', DEFAULT_LEVEL)
    color = COLOR.get(p.get('color', 'magenta'), COLOR['magenta'])
    if kind == 'solid':
        frame = [color] * COUNT
    elif kind == 'position':
        frame[p['index']] = color
    elif kind == 'bank':
        for i in range(p['bank'] * 4, p['bank'] * 4 + 4):
            frame[i] = color
    elif kind == 'steps':
        index = min(len(LEVELS) - 1, int(t / 1.5))
        level = LEVELS[index]
        frame = [color] * COUNT
        if state.get('step') != index:
            state['step'] = index
            print('LEVEL', json.dumps(dict(raw=level, percent=round(level / 255 * 100, 2))))
    elif kind == 'compare':
        side = int(t / 2) % 2
        level = p['b'] if side else p['a']
        frame = [color] * COUNT
        if state.get('step') != int(t / 2):
            state['step'] = int(t / 2)
            print('LEVEL', json.dumps(dict(label='B' if side else 'A', raw=level)))
    elif kind == 'ramp':
        progress = triangle(t / 2)
        if p['gamma']:
            progress = progress ** 2.2
        level = int(progress * 255)
        frame = [color] * COUNT
    elif kind == 'density':
        count = 1 if int(t / 2) % 2 == 0 else 8
        frame = [color if i < count else BLACK for i in range(COUNT)]
    elif kind == 'chase':
        pos = int(t * p.get('rate', 3))
        if p.get('bounce'):
            pos = pos % 14
            pos = pos if pos < 8 else 14 - pos
        else:
            pos %= COUNT
        if p.get('reverse'):
            pos = 7 - pos
        for k in range(p.get('trail', p.get('width', 1))):
            amount = (1 - k / p['trail']) if p.get('trail') else 1
            i = (pos-k) % COUNT
            if p.get('bounce'):
                past = (int(t*p.get('rate', 3))-k) % 14
                i = past if past < 8 else 14-past
            frame[i] = scale(hsv(t / 6) if p.get('rainbow') else color, amount)
        if p.get('opposed'):
            frame[7-pos] = COLOR['cyan']
    elif kind == 'fill':
        n = int(triangle(t * 0.7) * 8.99)
        frame = [color if i < n else BLACK for i in range(COUNT)]
    elif kind == 'wipe':
        cycle = int(t / 2)
        n = int((t / 2 % 1) * 8)
        frame = [hsv((cycle+1)/6) if i <= n else hsv(cycle/6) for i in range(COUNT)]
    elif kind == 'rainbow':
        frame = [hsv(i / COUNT - t / 5) for i in range(COUNT)]
    elif kind == 'gradient':
        frame = [palette('neon', i / COUNT - t / 6) for i in range(COUNT)]
    elif kind in ('sine', 'two-waves'):
        for i in range(COUNT):
            a = feature_wave(t * 2, -i * 0.85)
            frame[i] = scale(color, a)
            if kind == 'two-waves':
                b = feature_wave(t * 1.7, i * 0.85)
                frame[i] = mix(scale(color, a), scale(COLOR['cyan'], b), 0.5)
    elif kind == 'particle':
        pos = triangle(t * 0.65) * 7
        frame = [scale(color, max(0, 1-abs(i-pos))) for i in range(COUNT)]
    elif kind == 'walk':
        step = int(t * 4)
        if state.get('step') != step:
            state['step'] = step
            state['pos'] = max(0, min(7, state.get('pos', 3) + random.choice((-1, 1))))
        frame[state['pos']] = color
    elif kind == 'binary':
        n = int(t * 2) + 1
        frame = [color if n & (1 << i) else BLACK for i in range(COUNT)]
    elif kind in ('mirror', 'mirror-fill'):
        pos = int(t * 3) % 4
        if p.get('inward'):
            pos = 3-pos
        for i in range(4):
            if kind == 'mirror-fill':
                amount = 1 if i <= pos else 0
            elif p.get('trail'):
                amount = max(0, 1 - ((pos-i) % 4) / 3)
            else:
                amount = 1 if i == pos else 0
            frame[3-i] = scale(color, amount)
            frame[4+i] = scale(COLOR['cyan'], amount)
    elif kind == 'breathe':
        frame = [scale(color, (1-math.cos(t * math.pi))/2)] * COUNT
    elif kind == 'cross-breathe':
        a = (1-math.cos(t * math.pi))/2
        frame = [scale(color, a if i < 4 else 1-a) for i in range(COUNT)]
    elif kind == 'alternate':
        bank = int(t * 2) % 2
        frame = [color if i // 4 == bank else COLOR['cyan'] for i in range(COUNT)]
    elif kind == 'split':
        frame = [color if i < 4 else COLOR['cyan'] for i in range(COUNT)]
    elif kind == 'checker':
        frame = [color if (i+int(t*2)) % 2 else COLOR['cyan'] for i in range(COUNT)]
    elif kind == 'zones':
        frame = [hsv((i//2)/4 + t/8) for i in range(COUNT)]
    elif kind in ('centre', 'edges'):
        frame = [scale(color, (1-abs(i-3.5)/4) if kind == 'centre' else abs(i-3.5)/4)
                 for i in range(COUNT)]
    elif kind == 'hue':
        frame = [hsv(t/6)] * COUNT
    elif kind == 'palette':
        frame = [palette(p['palette'], t/6)] * COUNT
    elif kind == 'texture':
        for i in range(COUNT):
            value = 0.5*feature_wave(t*1.3, i*1.7) + 0.5*feature_wave(t*3.1, i*0.7)
            frame[i] = scale(palette(p['palette'], value*0.9), 0.2+0.8*value)
    elif kind == 'sparkle':
        step = int(t * 10)
        for i in range(COUNT):
            if hash01(i, step) < p['density']/8:
                frame[i] = hsv(hash01(i+17, step))
    elif kind == 'twinkle':
        for i in range(COUNT):
            amount = feature_wave(t * (0.6+i*0.17), i*2.1) ** 4
            frame[i] = scale(hsv(i/8+t/30), amount)
    elif kind == 'drops':
        step = int(t * 3)
        age = t * 3 % 1
        frame[int(hash01(5, step)*7.999)] = scale(COLOR['sky-blue'], (1-age)**2)
    elif kind == 'random-colors':
        frame = [hsv(hash01(i, int(t*2))) for i in range(COUNT)]
    elif kind == 'noise':
        frame = [scale(palette('neon', feature_wave(t*0.6, i*1.1)),
                       0.2+0.8*feature_wave(t*1.3, i*2.5)) for i in range(COUNT)]
    elif kind == 'beat':
        mode = p['mode']
        bpm = p['bpm']
        beats = t * bpm / 60
        if mode == 'tempo':
            # Integrated linearly increasing tempo over the cue.
            beats = (75*t + 45*t*t/duration) / 60
        elif mode == 'half-double':
            beats = t if t < duration/2 else duration/2 + (t-duration/2)*4
        elif mode == 'swing':
            pair = t % 1
            beats = int(t)*2 + (pair/0.66 if pair < 0.66 else 1+(pair-0.66)/0.34)
        beat = int(beats)
        phase = beats % 1
        kick = math.exp(-phase*9)
        snare = math.exp(-phase*16) if beat % 2 else 0
        hats = math.exp(-(beats*2 % 1)*18)
        hue = hash01(3, beat)
        if mode == 'picker':
            chosen = ('pulse', 'mirror', 'burst', 'step')[int(beats/4) % 4]
            mode = chosen
        if mode in ('pulse', 'kick', 'tempo', 'half-double', 'swing', 'drop', 'silence'):
            if mode == 'drop':
                if t < duration*0.45:
                    kick *= 0.2 + 0.8*t/(duration*0.45)
                elif t < duration*0.55:
                    kick = 0
                else:
                    kick = math.exp(-((t-duration*0.55)*2 % 1)*8)
            if mode == 'silence' and duration*0.35 < t < duration*0.65:
                kick = 0
            frame = [scale(color, kick)] * COUNT
        elif mode == 'alternate':
            frame = [scale(color if i < 4 else COLOR['cyan'], kick)
                     if i//4 == beat % 2 else BLACK for i in range(COUNT)]
        elif mode == 'color':
            frame = [scale(hsv(hue), kick)] * COUNT
        elif mode == 'step':
            frame[beat % COUNT] = scale(hsv(hue), 0.25+0.75*kick)
        elif mode == 'mirror':
            for i in range(4):
                amount = max(0, 1 - abs(i-phase*4))
                frame[3-i] = scale(color, amount)
                frame[4+i] = scale(COLOR['cyan'], amount)
        elif mode == 'burst':
            frame = [scale(hsv(hue+i/16), kick) if hash01(i, beat) < 0.5 else BLACK
                     for i in range(COUNT)]
        elif mode == 'snare':
            frame = [scale(COLOR['orange'], snare)] * COUNT
        elif mode == 'hats':
            frame[int(beats*2) % COUNT] = scale(COLOR['cyan'], hats)
        elif mode == 'layered':
            for i in range(COUNT):
                if i in (3, 4):
                    frame[i] = scale(COLOR['magenta'], kick)
                elif i in (1, 6):
                    frame[i] = scale(COLOR['orange'], snare)
                else:
                    frame[i] = scale(COLOR['cyan'], hats if i % 4 == int(beats*2) % 4 else 0)
        elif mode == 'subdivide':
            division = (1, 2, 4)[min(2, int(t/(duration/3)))]
            frame[int(beats*division) % COUNT] = color
        elif mode == 'features':
            bass = 0.2+0.8*feature_wave(t*0.9, 0)
            mid = 0.2+0.8*feature_wave(t*0.7, 2)
            high = 0.2+0.8*feature_wave(t*1.7, 4)
            for i in range(COUNT):
                frame[i] = scale(color, kick*bass) if i in (3, 4) else (
                    scale(COLOR['orange'], mid*feature_wave(t*3, i)) if i in (2, 5)
                    else scale(COLOR['cyan'], hats*high))
    elif kind == 'detail':
        grouped = int(t/3) % 2 == 0
        n = 4 if grouped else 8
        small = [BLACK] * n
        effect = p['effect']
        pos = int(t*3) % n
        for i in range(n):
            if effect == 'chase':
                amount = 1 if i == pos else 0
            elif effect == 'comet':
                amount = max(0, 1 - ((pos-i) % n)/3)
            elif effect == 'wave':
                amount = feature_wave(t*2, -i*math.pi*2/n)
            else:
                amount = 1 if hash01(i, int(t*5)) < 1/n else 0
            small[i] = scale(color, amount)
        frame = [small[i//2] if grouped else small[i] for i in range(COUNT)]
        segment = int(t/3)
        if state.get('step') != segment:
            state['step'] = segment
            print('DETAIL', 'four paired zones' if grouped else 'eight independent pixels')
    elif kind == 'flash':
        frame = [color if (t*p['hz']) % 1 < 0.15 else BLACK] * COUNT
    elif kind == 'flash-alternate':
        frame = [color if i//4 == int(t*4) % 2 else BLACK for i in range(COUNT)]
    elif kind in ('flash-double', 'flash-triplet'):
        count = 2 if kind == 'flash-double' else 3
        phase = t % 0.75
        on = any(k*0.11 <= phase < k*0.11+0.035 for k in range(count))
        frame = [color if on else BLACK] * COUNT
    elif kind == 'flash-random':
        frame = [color if hash01(1, int(t*12)) < 0.25 else BLACK] * COUNT
    else:
        raise ValueError('Unknown renderer: ' + kind)
    return frame, level


class Driver:
    def __init__(self):
        self.pixels = NeoPixel(Pin(LED_PIN, Pin.OUT, value=0), COUNT)
        self.peak_ma = 0
        self.limited_frames = 0

    def show(self, frame, level):
        # Keep the existing no-white preference even when interpolating colours.
        result = []
        for color in frame:
            c = [max(0, min(255, int(v))) for v in color]
            high = max(c)
            if high and min(c) > high*0.7:
                c[c.index(min(c))] = int(high*0.7)
            result.append(tuple(int(v*max(0, min(255, level))/255) for v in c))
        estimated = CHANNEL_MA * sum(sum(c) for c in result) / 255
        if estimated > EMITTER_BUDGET_MA:
            ratio = EMITTER_BUDGET_MA/estimated
            result = [tuple(int(v*ratio) for v in c) for c in result]
            self.limited_frames += 1
        actual_estimate = CHANNEL_MA * sum(sum(c) for c in result) / 255
        self.peak_ma = max(self.peak_ma, actual_estimate)
        for i in range(COUNT):
            self.pixels[i] = result[i]
        self.pixels.write()
        return actual_estimate

    def off(self):
        self.pixels.fill(BLACK)
        self.pixels.write()


def select(section=None, pattern=None):
    if section is not None and section not in SECTIONS:
        raise ValueError('Unknown section: ' + str(section))
    if pattern is not None and not any(c['id'] == pattern for c in CATALOG):
        raise ValueError('Unknown pattern: ' + str(pattern))
    chosen = [c for c in CATALOG if (section is None or c['section'] == section)
              and (pattern is None or c['id'] == pattern)]
    if not chosen:
        raise ValueError('No patterns match that selection')
    return chosen


def run(section=None, pattern=None, level=None, speed=1.0, repeat=1):
    chosen = select(section, pattern)
    if level is not None and not 1 <= level <= 255:
        raise ValueError('level must be 1..255')
    if level is not None and any(c['section'] in ('brightness', 'flashes') for c in chosen):
        raise ValueError('Brightness and flash cues use their labelled fixed levels; omit level override')
    if not 0.25 <= speed <= 4 or not 1 <= repeat <= 10:
        raise ValueError('speed must be 0.25..4 and repeat 1..10')
    driver = Driver()
    completed = []
    interrupted = False
    error = None
    active = None
    print('SHOWCASE_READY', json.dumps(dict(count=COUNT, pin=LED_PIN, cues=len(chosen)*repeat,
                                          emitter_budget_ma=EMITTER_BUDGET_MA,
                                          simulated_audio=True, level_override=level)))
    try:
        driver.off()
        sleep_ms(500)
        last_section = None
        for repetition in range(repeat):
            for item in chosen:
                if item['section'] != last_section:
                    print('SECTION', item['section'])
                    if item['section'] == 'flashes':
                        print('FLASH_SECTION_STARTS_IN_5_SECONDS: all LEDs off during countdown.')
                        driver.off()
                        sleep_ms(5000)
                    last_section = item['section']
                active = item['id']
                print('CUE_START', json.dumps(dict(id=active, title=item['title'], section=item['section'],
                                                  seconds=item['seconds']/speed,
                                                  level_override=level, repetition=repetition+1)))
                state = {}
                before_limited = driver.limited_frames
                started = ticks_ms()
                while True:
                    t = ticks_diff(ticks_ms(), started)/1000 * speed
                    if t >= item['seconds']:
                        break
                    frame, cue_level = frame_for(item, t, item['seconds'], state)
                    driver.show(frame, cue_level if level is None else level)
                    sleep_ms(4 if item['section'] == 'flashes' else FRAME_MS)
                driver.off()
                completed.append(active)
                print('CUE_END', json.dumps(dict(id=active, limited_frames=driver.limited_frames-before_limited)))
                active = None
                sleep_ms(350)
    except KeyboardInterrupt:
        interrupted = True
        print('SHOWCASE_INTERRUPTED')
    except Exception as exc:
        error = str(exc)
        raise
    finally:
        driver.off()
        print('SHOWCASE_SUMMARY', json.dumps(dict(completed=completed, active_at_stop=active,
                                                interrupted=interrupted,
                                                error=error,
                                                peak_estimated_emitter_ma=driver.peak_ma,
                                                limited_frames=driver.limited_frames,
                                                note='Visual showcase only; current estimate is not a measurement.')))


if __name__ == '__main__':
    run()

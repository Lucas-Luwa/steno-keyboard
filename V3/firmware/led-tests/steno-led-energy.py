"""Optional fast extension; execute after steno-led-showcase.py in its namespace.
Original catalog and settings are preserved. New cues default to 128/255; the launcher can override this.
"""
_BASE_FRAME_FOR = frame_for
FRAME_MS = 5
ENERGY_START = len(CATALOG)


def energy_cue(ident, title, mode, seconds=6, **params):
    cue(ident, 'energy', title, 'energy', seconds, mode=mode, level=128, **params)


energy_cue('energy-fade-slow', 'Smooth fade in/out: zero to selected peak', 'fade', 8, rate=0.5)
energy_cue('energy-fade-fast', 'Fast fade in/out: two pulses per second', 'fade', rate=2)
energy_cue('energy-attack-decay', 'Sharp attack with a fading tail', 'decay', rate=4)
energy_cue('energy-crossfade', 'Left and right crossfade', 'crossfade', rate=2)
energy_cue('energy-colour-fade', 'Rapid smooth saturated color fades', 'colour-fade', rate=2)
for rate in (12, 24, 40):
    energy_cue('energy-out-%d' % rate, '4+5, 3+6, 2+7, 1+8: %d pair steps/sec' % rate,
               'stripes', rate=rate)
energy_cue('energy-in', 'Outside-in pairs: 24 steps/sec', 'stripes', rate=24, inward=True)
energy_cue('energy-pingpong', 'Center-out then edge-in: 24 steps/sec', 'stripes', rate=24, bounce=True)
energy_cue('energy-fill', 'Pairs rapidly fill out from the center', 'stripes', rate=24, fill=True)
energy_cue('energy-stripe-trails', 'Center-out pairs with fading trails', 'stripes', rate=24, trail=True)
energy_cue('energy-stripe-rainbow', 'Center-out pairs cycle saturated hues', 'stripes', rate=24, hue=True)
energy_cue('energy-stripe-random', 'Center-out pairs change to a random color each sweep', 'stripes', rate=24, random_color=True)
for rate in (16, 32, 64):
    energy_cue('energy-chase-%d' % rate, 'Fast chase: %d LED positions/sec' % rate, 'chase', rate=rate)
energy_cue('energy-scanner', 'Fast bouncing scanner: 40 positions/sec', 'scanner', rate=40)
energy_cue('energy-comets', 'Opposing colored comets: 32 positions/sec', 'comets', rate=32)
energy_cue('energy-opposed', 'Opposing dots: 32 positions/sec', 'opposed', rate=32)
energy_cue('energy-colour-12', 'Whole row switches random colors 12 times/sec', 'random-colour', rate=12)
energy_cue('energy-colour-24', 'Whole row switches random colors 24 times/sec', 'random-colour', rate=24)
energy_cue('energy-random-pixels', 'All pixels change independently 24 times/sec', 'random-pixels', rate=24)
energy_cue('energy-bursts', 'Random colored spatial bursts 16 times/sec', 'bursts', rate=16)
energy_cue('energy-sparkles', 'Rapid isolated colored sparks: 40 updates/sec', 'sparkles', rate=40)
energy_cue('energy-alternate', 'Rapid left/right color alternation', 'alternate', rate=12)
energy_cue('energy-180', '180 BPM sixteenth-note motion', 'rhythm', bpm=180, subdivision=4)
energy_cue('energy-220', '220 BPM sixteenth-note motion', 'rhythm', bpm=220, subdivision=4)
energy_cue('energy-triplets', '200 BPM triplet motion', 'rhythm', bpm=200, subdivision=3)
energy_cue('energy-build-drop', 'Accelerating stripes, dark gap, then colored bursts', 'build-drop', 8)
for rate in (8, 12, 16):
    energy_cue('energy-strobe-%d' % rate, 'Magenta flashes: %d Hz' % rate, 'strobe', rate=rate)
energy_cue('energy-burst-strobe', 'Random-color double/triple flash bursts', 'burst-strobe', rate=4)
energy_cue('energy-mix', 'Rapid pattern switching: stripes/chase/bursts/sparkles', 'mix', 8)
SECTIONS = SECTIONS + ('energy',)
ENERGY_CATALOG = CATALOG[ENERGY_START:]


def energy_hash(index, step):
    # Scramble adjacent positions and steps rather than a linear gradient.
    n = (index*374761393 + step*668265263 + 1447) & 0xffffffff
    n = ((n ^ (n >> 13))*1274126177) & 0xffffffff
    return ((n ^ (n >> 16)) & 65535)/65536.0


def energy_frame(item, t, duration, state):
    p = item['params']
    mode, rate = p['mode'], p.get('rate', 24)
    step, phase = int(t*rate), t*rate % 1
    color, frame = COLOR['magenta'], blank()
    if mode == 'mix':
        mode = ('stripes', 'chase', 'bursts', 'sparkles')[int(t*2) % 4]
    elif mode == 'build-drop':
        if t < 3.5:
            mode, step = 'stripes', int(8*t+4*t*t)
        elif t < 4:
            return frame, 128
        else:
            mode, step, phase = 'bursts', int((t-4)*24), (t-4)*24 % 1
    if mode in ('fade', 'decay', 'crossfade', 'colour-fade'):
        amount = (1-math.cos(t*rate*2*math.pi))/2
        if mode == 'decay':
            amount = math.exp(-phase*7)
        for i in range(COUNT):
            if mode == 'colour-fade':
                frame[i] = hsv(t*rate/6)
            else:
                frame[i] = scale(color if i < 4 or mode != 'crossfade' else COLOR['cyan'],
                                 1-amount if mode == 'crossfade' and i >= 4 else amount)
    elif mode == 'stripes':
        pos = step % 4
        if p.get('bounce'):
            pos = step % 6
            pos = pos if pos < 4 else 6-pos
        if p.get('inward'):
            pos = 3-pos
        if p.get('hue'):
            color = hsv(t*1.2)
        if p.get('random_color'):
            color = hsv(energy_hash(9, step//4))
        for k in range(4):
            amount = (1 if k <= pos else 0) if p.get('fill') else (1 if k == pos else 0)
            if p.get('trail'):
                amount = max(0, 1-(((pos-k) % 4)+phase)/2.5)
            frame[3-k] = frame[4+k] = scale(color, amount)
    elif mode in ('chase', 'scanner', 'comets', 'opposed'):
        if mode == 'scanner':
            for tail in range(3):
                pos = (step-tail) % 14
                pos = pos if pos < 8 else 14-pos
                frame[pos] = scale(color, 1-tail/3)
        else:
            for tail in range(3 if mode == 'comets' else 1):
                pos, amount = (step-tail) % COUNT, 1-tail/3
                frame[pos] = scale(color, amount)
                if mode in ('comets', 'opposed'):
                    frame[7-pos] = scale(COLOR['cyan'], amount)
    elif mode in ('random-colour', 'random-pixels', 'bursts', 'sparkles'):
        if mode == 'random-colour':
            frame = [hsv(energy_hash(1, step))]*COUNT
        elif mode == 'random-pixels':
            frame = [hsv(energy_hash(i, step)) for i in range(COUNT)]
        elif mode == 'bursts':
            frame = [scale(hsv(energy_hash(i+20, step)), (1-phase)**0.5)
                     if energy_hash(i, step) < .55 else BLACK for i in range(COUNT)]
        else:
            frame[int(energy_hash(1, step)*COUNT)] = hsv(energy_hash(3, step))
    elif mode == 'alternate':
        frame = [color if (i//4+step) % 2 else COLOR['cyan'] for i in range(COUNT)]
    elif mode == 'rhythm':
        beats = t*p['bpm']/60
        pos = int(beats*p['subdivision']) % COUNT
        frame = [scale(hsv(i/8+int(beats)/12),
                       1 if i == pos else .18*math.exp(-(beats % 1)*8)) for i in range(COUNT)]
    elif mode == 'strobe':
        frame = [color if phase < .2 else BLACK]*COUNT
    elif mode == 'burst-strobe':
        period = t % .75
        count = 2 if int(t/.75) % 2 == 0 else 3
        on = any(k*.085 <= period < k*.085+.025 for k in range(count))
        frame = [hsv(energy_hash(1, int(t/.75))) if on else BLACK]*COUNT
    else:
        raise ValueError('Unknown energy renderer: '+mode)
    return frame, 128


def frame_for(item, t, duration, state):
    if item['kind'] == 'energy':
        return energy_frame(item, t, duration, state)
    return _BASE_FRAME_FOR(item, t, duration, state)

"""Run labelled LED sections on the known MicroPython controller; never flash.

Uses the mpremote 1.29 transport to stream output and deliver Ctrl-C
on request. --list, --prepare-only, --status and --stop do not open a device.
"""
import argparse
import codecs
from datetime import datetime
import json
import os
from pathlib import Path
import sys
import time
import uuid
from led_showcase_metadata import ROOT, SOURCE, ENERGY_SOURCE, load

TOOLS = ROOT / 'work' / 'led-tools'
SESSION = ROOT / 'work' / 'led-showcase-session.json'
STOP = ROOT / 'work' / 'led-showcase.stop'
SERIAL = None  # Optional user-provided identity check; no personal device ID committed.


class RawOutput:
    """Separate raw-REPL stdout/stderr, including EOF markers in split chunks."""
    def __init__(self, consumer):
        self.phase = 0
        self.consumer = consumer
        self.stderr = bytearray()

    def feed(self, chunk):
        for byte in chunk:
            if self.phase >= 2:
                continue  # A trailing raw prompt is not device output.
            if byte == 4:
                self.phase += 1
            elif self.phase == 0:
                self.consumer(bytes((byte,)))
            else:
                self.stderr.append(byte)


def write_session(value):
    temp = SESSION.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2), encoding='utf-8')
    temp.replace(SESSION)


def main():
    ns = load(energy='--energy' in sys.argv[1:])
    parser = argparse.ArgumentParser()
    parser.add_argument('--energy', action='store_true', help='Include the fast extension (defaults to 128/255)')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--section', choices=ns['SECTIONS'])
    mode.add_argument('--pattern')
    mode.add_argument('--all', action='store_true')
    mode.add_argument('--list', action='store_true')
    mode.add_argument('--status', action='store_true')
    mode.add_argument('--stop', action='store_true')
    parser.add_argument('--port', help='Explicit serial port, e.g. COM4')
    parser.add_argument('--serial', help='Optional expected USB serial number')
    parser.add_argument('--level', type=int)
    parser.add_argument('--speed', type=float, default=1)
    parser.add_argument('--repeat', type=int, default=1)
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    if args.list:
        for section in ns['SECTIONS']:
            entries = ns['select'](section=section)
            print(section, len(entries), 'cues;', round(sum(c['seconds']+.35 for c in entries), 1), 'seconds')
            for c in entries:
                print(' ', c['id'], '|', c['title'])
        return
    if args.status or args.stop:
        if not SESSION.exists():
            print('No active showcase session marker.')
            return
        current = json.loads(SESSION.read_text())
        if args.stop:
            STOP.write_text(current['token'], encoding='utf-8')
            print('Stop requested; the active runner will send Ctrl-C and wait for LED-off cleanup.')
        else:
            print(json.dumps(current, indent=2))
        return
    section = args.section
    if not (section or args.pattern or args.all):
        section = 'energy' if args.energy else 'mapping'
    chosen = ns['select'](section=section, pattern=args.pattern)
    if args.level is not None and not 1 <= args.level <= 255:
        parser.error('--level must be 1..255')
    if args.level is not None and any(c['section'] in ('brightness', 'flashes') for c in chosen):
        parser.error('Brightness/flash cues use fixed labelled levels; omit --level.')
    if not .25 <= args.speed <= 4 or not 1 <= args.repeat <= 10:
        parser.error('--speed must be .25..4 and --repeat 1..10')
    options = dict(section=section, pattern=args.pattern, level=args.level,
                   speed=args.speed, repeat=args.repeat)
    source = SOURCE.read_text(encoding='utf-8')
    if args.energy:
        source += '\n' + ENERGY_SOURCE.read_text(encoding='utf-8')
    payload = ("_led_showcase = {'__name__': 'steno_showcase'}\n"
               + 'exec(' + repr(source) + ', _led_showcase)\n'
               + "_led_showcase['run'](**" + repr(options) + ')\n')
    payload_path = ROOT / 'work' / 'led-showcase-payload.py'
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    compile(payload, str(payload_path), 'exec')
    payload_path.write_text(payload, encoding='utf-8')
    seconds = args.repeat*(sum(c['seconds']/args.speed+.35 for c in chosen)
                          + (5 if any(c['section'] == 'flashes' for c in chosen) else 0))+.5
    print('Selection:', section or args.pattern or 'all', '| Cues:', len(chosen)*args.repeat,
          '| Approx seconds:', round(seconds), flush=True)
    if args.prepare_only:
        print('Payload validated. No serial device opened, no GPIO changed.')
        return
    if not args.port:
        parser.error('--port is required to open a device; use --prepare-only for offline preparation')
    sys.path.insert(0, str(TOOLS))
    from serial.tools import list_ports
    from mpremote.transport_serial import SerialTransport
    ports = [p for p in list_ports.comports()
             if p.device.upper() == args.port.upper() and p.vid == 0x2E8A and p.pid == 0x1020
             and (args.serial is None or p.serial_number == args.serial)]
    if len(ports) != 1:
        raise SystemExit('Expected one MicroPython RP2040 at the selected port; found %d. Connect normally, without BOOTSEL.' % len(ports))
    token = uuid.uuid4().hex
    state = dict(token=token, pid=os.getpid(), port=ports[0].device,
                 started=datetime.now().isoformat(), selection=options, phase='connecting',
                 approximate_seconds=seconds, completed_cues=0)
    folder = ROOT / 'work' / 'led-showcase-logs'
    folder.mkdir(exist_ok=True)
    log_path = folder / (datetime.now().strftime('%Y%m%d-%H%M%S-%f') + '.log')
    state['log'] = str(log_path)
    try:
        with SESSION.open('x', encoding='utf-8') as marker:
            json.dump(state, marker, indent=2)
    except FileExistsError:
        raise SystemExit('A showcase session marker already exists. Use --status or --stop before starting another run.')
    transport = None
    pending = ''
    stop_sent = False
    stop_deadline = None
    with log_path.open('w', encoding='utf-8') as log:
        decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')

        def consume(chunk):
            nonlocal pending
            value = decoder.decode(chunk)
            if not value:
                return
            print(value, end='', flush=True)
            log.write(value)
            log.flush()
            pending += value
            while '\n' in pending:
                line, pending = pending.split('\n', 1)
                if line.startswith('CUE_START '):
                    state.update(phase='running', cue=json.loads(line[10:]))
                    write_session(state)
                elif line.startswith('CUE_END '):
                    state['completed_cues'] += 1
                    write_session(state)
                elif line.startswith('SHOWCASE_SUMMARY '):
                    state['summary'] = json.loads(line[17:])
                    write_session(state)

        try:
            transport = SerialTransport(ports[0].device, timeout=.1)
            transport.enter_raw_repl(soft_reset=True)
            transport.exec_raw_no_follow(payload)
            output = RawOutput(consume)
            deadline = time.monotonic()+seconds+60
            while output.phase < 2:
                try:
                    if not stop_sent and STOP.exists() and STOP.read_text().strip() == token:
                        transport.serial.write(b'\x03')
                        stop_sent = True
                        stop_deadline = time.monotonic()+20
                        state['phase'] = 'stopping'
                        write_session(state)
                    if time.monotonic() > (stop_deadline if stop_sent else deadline):
                        raise TimeoutError('Device did not complete within the expected window.')
                    chunk = transport.serial.read(max(1, transport.serial.in_waiting))
                    if chunk:
                        output.feed(chunk)
                except KeyboardInterrupt:
                    if not stop_sent:
                        transport.serial.write(b'\x03')
                        stop_sent = True
                        stop_deadline = time.monotonic()+20
            if output.stderr:
                error = output.stderr.decode('utf-8', errors='replace')
                print(error, file=sys.stderr)
                log.write(error)
                raise RuntimeError('Device reported an exception; inspect the saved log.')
            if 'summary' not in state:
                raise RuntimeError('No complete showcase summary was received.')
            print('\nLOG:', log_path, flush=True)
        except BaseException:
            if transport is not None:
                # Best effort: interrupt and explicitly send all-off if the link survives.
                try:
                    transport.enter_raw_repl(soft_reset=False)
                    transport.exec("from machine import Pin; from neopixel import NeoPixel; "
                                   "_off=NeoPixel(Pin(22,Pin.OUT,value=0),8); _off.fill((0,0,0)); _off.write()")
                except BaseException:
                    pass
            raise
        finally:
            if transport is not None:
                try:
                    try:
                        transport.exit_raw_repl()
                    finally:
                        transport.close()
                except OSError as exc:
                    print('Serial close notice:', str(exc), file=sys.stderr)
            if SESSION.exists() and json.loads(SESSION.read_text()).get('token') == token:
                SESSION.unlink()
            if STOP.exists() and STOP.read_text().strip() == token:
                STOP.unlink()


if __name__ == '__main__':
    main()

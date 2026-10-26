"""Read the device catalogue without importing hardware modules or opening USB."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'steno-led-showcase.py'
ENERGY_SOURCE = ROOT / 'steno-led-energy.py'


def load(energy=False):
    tree = ast.parse(SOURCE.read_text(encoding='utf-8'))
    tree.body = [node for node in tree.body if not (
        isinstance(node, ast.ImportFrom) and node.module in ('machine', 'neopixel', 'time'))]

    def forbidden(*args, **kwargs):
        raise RuntimeError('Hardware API called while loading metadata')

    namespace = dict(__name__='showcase_metadata', Pin=forbidden, NeoPixel=forbidden)
    exec(compile(tree, str(SOURCE), 'exec'), namespace)
    if energy:
        exec(compile(ENERGY_SOURCE.read_text(encoding='utf-8'), str(ENERGY_SOURCE), 'exec'), namespace)
    return namespace

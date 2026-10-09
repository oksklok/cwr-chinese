"""Generate LOCAL-ONLY wizard PBO overlays; never modify/distribute stock assets.

Only the existing UTF-8 CSV member is replaced. --check never writes.
"""
import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'terrain'))
from build_labels import pbo_parts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('game', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    game = args.game.resolve()
    mod = game / '@zhcn-prototype'
    outputs = {}
    for relative, digest in json.loads((ROOT / 'stock-hashes.json').read_text()).items():
        source = (game / relative).read_bytes()
        if hashlib.sha256(source).hexdigest() != digest:
            raise ValueError(('Unsupported stock wizard PBO', relative))
        headers, terminator, payloads = pbo_parts(source)
        if b'stringtable.utf8.csv' not in payloads:
            raise ValueError(('Missing stock UTF-8 table', relative))
        payloads[b'stringtable.utf8.csv'] = (ROOT / relative.removesuffix('.pbo') / 'stringtable.utf8.csv').read_bytes()
        out = bytearray()
        for name, fields in headers:
            if name is None:
                out.extend(fields)
            else:
                fields = fields.copy()
                if name == b'stringtable.utf8.csv':
                    fields[0] = 0  # Replacement CSV is stored uncompressed.
                    fields[1] = len(payloads[name])
                    fields[4] = len(payloads[name])
                out.extend(name + b'\0' + struct.pack('<5I', *fields))
        out.extend(terminator)
        for name, _ in headers:
            if name is not None:
                out.extend(payloads[name])
        if pbo_parts(bytes(out))[2] != payloads:
            raise ValueError(('Overlay round-trip failed', relative))
        target = mod / relative
        if args.check:
            if target.read_bytes() != out:
                raise ValueError(('Wizard deployment mismatch', relative))
        elif target.exists() and target.read_bytes() != out:
            raise ValueError(('Existing wizard overlay differs; remove only the prior generated overlay first', relative))
        outputs[target] = out
    # Preflight ALL sources/targets before any writes; stock PBOs are read-only.
    if not args.check:
        for target, data in outputs.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    print(f'PASS: {len(outputs)} wizard overlays; stock hashes, only CSV payload changed, deployment equality')


if __name__ == '__main__':
    main()

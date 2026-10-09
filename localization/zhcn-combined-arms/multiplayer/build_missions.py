"""Pack APL-SA authored MP overlays from compatible stock 3.05 missions.

Ready-made adaptations may ship under APL-SA; see DISTRIBUTION.md. --check is read-only.
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


def stock_files(directory):
    files = {}
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():
            raise ValueError(('Unsupported stock symlink', path))
        if path.is_file():
            files[path.relative_to(directory).as_posix()] = path.read_bytes()
    return files


def tree_hash(files):
    digest = hashlib.sha256()
    for name, data in sorted(files.items()):
        digest.update(name.encode('utf-8') + b'\0' + hashlib.sha256(data).digest())
    return digest.hexdigest()


def overlay_payloads(game, name, digest):
    files = stock_files(game / 'MPMissions' / name)
    if not files or tree_hash(files) != digest:
        raise ValueError(('Unsupported stock GOG 3.05 MP mission', name))
    edits = json.loads((ROOT / 'text-references.json').read_text(encoding='utf-8')).get(name, {})
    result = dict(files)
    result['stringtable.utf8.csv'] = (ROOT / 'MPMissions' / name / 'stringtable.utf8.csv').read_bytes()
    for filename, replacements in edits.items():
        data = files[filename]
        for replacement in replacements:
            old, new, key = replacement[:3]
            old, new = old.encode('utf-8'), new.encode('utf-8')
            if data.count(old) != 1:
                raise ValueError(('Text reference no longer matches stock', name, filename, key))
            data = data.replace(old, new)
        result[filename] = data
    return result


def pack(files):
    # Standard uncompressed PBO: stock relative paths/bytes, no invented prefix.
    output = bytearray()
    for name, data in files.items():
        output.extend(name.encode('utf-8') + b'\0' + struct.pack('<5I', 0, 0, 0, 0, len(data)))
    output.extend(b'\0' + bytes(20))
    for data in files.values():
        output.extend(data)
    if pbo_parts(bytes(output))[2] != {k.encode('utf-8'): v for k, v in files.items()}:
        raise ValueError('MP overlay did not round-trip exactly')
    return bytes(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('game', type=Path)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--mod-dir', type=Path)
    args = parser.parse_args()
    game = args.game.resolve()
    mod = args.mod_dir or game / '@zhcn-prototype'
    outputs = {}
    for name, digest in json.loads((ROOT / 'stock-hashes.json').read_text()).items():
        data = pack(overlay_payloads(game, name, digest))
        target = mod / 'MPMissions' / (name + '.pbo')
        if args.check:
            if target.read_bytes() != data:
                raise ValueError(('MP deployment mismatch', name))
        elif target.exists() and target.read_bytes() != data:
            raise ValueError(('Existing overlay differs; remove only the prior generated MP overlay first', name))
        outputs[target] = data
    # Preflight every stock tree and output before writing; originals stay read-only.
    if not args.check:
        for target, data in outputs.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    print(f'PASS: {len(outputs)} authored MP overlays; stock hashes, payload round-trip, deployment equality')


if __name__ == '__main__':
    main()

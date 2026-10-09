"""Generate local-only terrain-label overlays from an untouched GOG 3.05 install.

Only stock name values become $STR references. No commercial config/terrain
payload is shipped with this script. Run --check to verify without writing.
"""
import argparse
import copy
import csv
import hashlib
import struct
from pathlib import Path

PATCH = Path(__file__).resolve().parents[1]
TABLE = PATCH / 'mod/bin/stringtable_terrain.utf8.csv'
INPUTS = {
    'BIN/CONFIG.BIN': 'ad7e33e39b84cca0e4ec0d04b7be97424725b0cf057c56a57ce082e19d0ad876',
    'AddOns/Noe.pbo': 'c98a6c97f21264e20f91e2e7ee024a068a11821361266041ac0c47de4f05cf72',
}


class Config:
    """Stock version-4 ParamFile binary; mirrors ParamFileParse.cpp serialization."""
    def __init__(self, data):
        self.data = data
        self.pos = 8
        self.pool = []
        if data[:8] != b'\0raP\x04\0\0\0':
            raise ValueError('Unsupported config format')
        self.root = self.read_class()
        self.tail = data[self.pos:]  # Preserve serialized evaluator variables.
        if self.encode() != data:
            raise ValueError('Stock config did not round-trip exactly')

    def number(self, fmt):
        value = struct.unpack_from('<' + fmt, self.data, self.pos)[0]
        self.pos += struct.calcsize(fmt)
        return value

    def text(self):
        end = self.data.index(b'\0', self.pos)
        value = self.data[self.pos:end].decode('cp1252')
        self.pos = end + 1
        return value

    def index(self):
        value = shift = 0
        while True:
            b = self.number('B')
            value |= (b & 127) << shift
            if b < 128:
                return value
            shift += 7
            if shift >= 35:
                raise ValueError('Invalid index')

    def pooled(self):
        index = self.index()
        if index == len(self.pool):
            self.pool.append(self.text())
        if index >= len(self.pool):
            raise ValueError('Invalid string pool')
        return self.pool[index]

    def raw(self, kind):
        if kind == 0:
            return self.pooled()
        if kind == 1:
            return self.number('f')
        if kind == 2:
            return self.number('i')
        if kind == 3:
            return self.array()
        raise ValueError(f'Invalid value kind {kind}')

    def array(self):
        return [self.raw(self.number('B')) for _ in range(self.index())]

    def read_class(self):
        name, base = self.pooled(), self.text()
        entries = {}
        for _ in range(self.index()):
            kind = self.number('B')
            if kind == 0:
                child = self.read_class()
                entries[child.pop('_name')] = child
            elif kind == 1:
                value_kind = self.number('B')
                key = self.pooled()
                entries[key] = self.raw(value_kind)
            else:
                if kind != 2:
                    raise ValueError('Invalid entry kind')
                key = self.pooled()
                entries[key] = self.array()
        return dict(_name=name, _base=base, **entries)

    def encode(self):
        out = bytearray(self.data[:8])
        pool = {}

        def index(value):
            while value >= 128:
                out.append((value & 127) | 128)
                value >>= 7
            out.append(value)

        def text(value):
            out.extend(value.encode('cp1252') + b'\0')

        def pooled(value):
            if value in pool:
                index(pool[value])
            else:
                index(len(pool))
                pool[value] = len(pool)
                text(value)

        def raw(value):
            if isinstance(value, str):
                out.append(0)
                pooled(value)
            elif isinstance(value, float):
                out.append(1)
                out.extend(struct.pack('<f', value))
            elif isinstance(value, int):
                out.append(2)
                out.extend(struct.pack('<i', value))
            else:
                if not isinstance(value, list):
                    raise ValueError('Invalid array value')
                out.append(3)
                array(value)

        def array(values):
            index(len(values))
            for value in values:
                raw(value)

        def write_class(name, node):
            pooled(name)
            text(node['_base'])
            entries = [(k, v) for k, v in node.items() if k not in ('_name', '_base')]
            index(len(entries))
            for key, value in entries:
                if isinstance(value, dict):
                    out.append(0)
                    write_class(key, value)
                elif isinstance(value, list):
                    out.append(2)
                    pooled(key)
                    array(value)
                else:
                    out.append(1)
                    # ParamValue writes type before its property name.
                    out.append(0 if isinstance(value, str) else 1 if isinstance(value, float) else 2)
                    pooled(key)
                    if isinstance(value, str):
                        pooled(value)
                    else:
                        out.extend(struct.pack('<f' if isinstance(value, float) else '<i', value))

        write_class(self.root['_name'], self.root)
        out.extend(self.tail)
        return bytes(out)


def pbo_parts(data):
    """Retain stock PBO extension/header fields and opaque member payloads."""
    pos = 0
    headers = []
    while True:
        start = pos
        end = data.index(b'\0', pos)
        name = data[pos:end]
        fields = list(struct.unpack_from('<5I', data, end + 1))
        pos = end + 21
        if not name:
            if fields[0] == 0x56657273:
                while data[pos]:
                    pos = data.index(b'\0', data.index(b'\0', pos) + 1) + 1
                pos += 1
                headers.append((None, data[start:pos]))
                continue
            terminator = data[start:pos]
            break
        headers.append((name, fields))
    payloads = {}
    for name, fields in headers:
        if name is not None:
            payloads[name] = data[pos:pos + fields[4]]
            pos += fields[4]
    if pos != len(data):
        raise ValueError('Unexpected PBO trailer; unsupported input')
    return headers, terminator, payloads


def localized(config, worlds, rows):
    original = copy.deepcopy(config.root)
    expected = copy.deepcopy(original)
    count = 0
    for world in worlds:
        names = config.root['CfgWorlds'][world]['Names']
        ids = {k for k in names if not k.startswith('_')}
        if ids != set(rows[world]):
            raise ValueError((world, 'Incomplete terrain label coverage'))
        for location in ids:
            key, chinese, stock = rows[world][location]
            if names[location]['name'] != stock:
                raise ValueError((world, location, 'Stock label mismatch'))
            names[location]['name'] = '$' + key
            expected['CfgWorlds'][world]['Names'][location]['name'] = '$' + key
            count += 1
    if config.root != expected:
        raise ValueError('Non-name configuration changed')
    result = config.encode()
    reparsed = Config(result)
    if reparsed.root != expected or reparsed.tail != config.tail:
        raise ValueError('Localized config did not round-trip exactly')
    return result, count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('game', type=Path, help='Untouched-stock Remastered directory (campaign CSV patches are fine)')
    parser.add_argument('--check', action='store_true', help='Check generated deployment without writing')
    parser.add_argument('--mod-dir', type=Path)
    args = parser.parse_args()
    game = args.game.resolve()
    mod = args.mod_dir or game / '@zhcn-prototype'
    # The engine prefers config.cpp to config.bin, so our overlay would be ignored.
    bin_dir = mod / 'bin'
    if bin_dir.is_dir():
        for entry in bin_dir.iterdir():
            if entry.name.casefold() == 'config.cpp':
                raise ValueError(f'Conflicting mod bin/{entry.name} exists; leave it untouched and resolve the conflict first')
    if not (mod / 'bin/stringtable.csv').is_file():
        raise ValueError('Deploy the existing Chinese mod first')
    sources = {}
    for relative, digest in INPUTS.items():
        data = (game / relative).read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(('Not stock GOG 3.05', relative))
        sources[relative] = data
    rows = {world: {} for world in ('Eden', 'Abel', 'Noe')}
    with TABLE.open(encoding='utf-8', newline='') as stream:
        table = list(csv.reader(stream, strict=True))
    if not table or table[0] != ['LANGUAGE', 'English', 'French', 'Italian', 'Spanish', 'German', 'Czech', 'Polish', 'Russian', 'ChineseSimplified', 'ChineseTraditional']:
        raise ValueError('Invalid terrain table header')
    for row in table[1:]:
        if len(row) != 11 or not all(row) or len(set(row[1:9])) != 1:
            raise ValueError('Malformed terrain translation')
        prefix, world, location = row[0].split('_', 4)[2:]
        if prefix != 'MAP' or not row[0].startswith('STR_CWRC_MAP_'):
            raise ValueError('Invalid terrain key')
        if location in rows[world]:
            raise ValueError('Duplicate terrain key')
        rows[world][location] = (row[0], row[9], row[1])
    if {w: len(v) for w, v in rows.items()} != {'Eden': 18, 'Abel': 14, 'Noe': 30}:
        raise ValueError('Incomplete terrain table')
    from fontTools.ttLib import TTFont
    chars = {ord(c) for values in rows.values() for _, chinese, _ in values.values() for c in chinese}
    for role in ('title', 'body', 'mono', 'serif', 'hand'):
        font = PATCH / f'font/cwr_{role}.ttf'
        with TTFont(font) as face:
            if chars - set(face.getBestCmap()):
                raise ValueError((font.name, 'Missing terrain glyphs'))
        with TTFont(PATCH / f'font/ChineseTraditional/cwr_{role}.ttf') as face:
            traditional_chars = {ord(c) for row in table[1:] for c in row[10]}
            if traditional_chars - set(face.getBestCmap()):
                raise ValueError((font.name, 'Missing Traditional terrain glyphs'))
    master = Config(sources['BIN/CONFIG.BIN'])
    if set(master.root['CfgWorlds']['Cain']['Names']) != {'_base'}:
        raise ValueError('Kolgujev unexpectedly has names')
    master_bytes, master_count = localized(master, ('Eden', 'Abel'), rows)
    headers, terminator, payloads = pbo_parts(sources['AddOns/Noe.pbo'])
    config_header = next(fields for name, fields in headers if name == b'config.bin')
    if config_header[0] != 0:
        raise ValueError('Unsupported compressed config')
    payloads[b'config.bin'], noe_count = localized(Config(payloads[b'config.bin']), ('Noe',), rows)
    out = bytearray()
    for name, fields in headers:
        if name is None:
            out.extend(fields)
        else:
            fields = fields.copy()
            fields[4] = len(payloads[name])
            out.extend(name + b'\0' + struct.pack('<5I', *fields))
    out.extend(terminator)
    for name, _ in headers:
        if name is not None:
            out.extend(payloads[name])
    _, _, changed_payloads = pbo_parts(bytes(out))
    _, _, stock_payloads = pbo_parts(sources['AddOns/Noe.pbo'])
    if any(changed_payloads[k] != v for k, v in stock_payloads.items() if k != b'config.bin'):
        raise ValueError('Terrain asset changed')
    outputs = {'bin/config.bin': master_bytes, 'AddOns/Noe.pbo': bytes(out),
               'bin/stringtable_terrain.utf8.csv': TABLE.read_bytes()}
    # Preflight every output before writing any of them.
    for relative, data in outputs.items():
        target = mod / relative
        if args.check:
            if target.read_bytes() != data:
                raise ValueError(('Deployment mismatch', relative))
        else:
            # Never replace an unrelated mod artifact; only update our own prior output.
            if target.exists() and relative != 'bin/stringtable_terrain.utf8.csv':
                if relative == 'bin/config.bin':
                    prior = Config(target.read_bytes()).root
                    for w in ('Eden', 'Abel'):
                        for loc, (_, _, stock) in rows[w].items():
                            if not prior['CfgWorlds'][w]['Names'][loc]['name'].startswith('$STR_CWRC_MAP_'):
                                raise ValueError('Unrelated mod config exists')
                            prior['CfgWorlds'][w]['Names'][loc]['name'] = stock
                    if prior != Config(sources['BIN/CONFIG.BIN']).root:
                        raise ValueError('Unrelated mod config exists')
                else:
                    if target.read_bytes() != data:
                        raise ValueError('Unrelated mod Noe.pbo exists')
            if target.exists() and relative == 'bin/stringtable_terrain.utf8.csv':
                with target.open(encoding='utf-8', newline='') as stream:
                    prior_table = list(csv.reader(stream, strict=True))
                if [r[0] for r in prior_table] != [r[0] for r in table]:
                    raise ValueError('Unrelated terrain table exists')
    if not args.check:
        for relative, data in outputs.items():
            target = mod / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    print(f'PASS: {master_count + noe_count} built-in labels; Everon 18, Malden 14, Nogova 30; Kolgujev 0 stock labels')
    print('PASS: exact stock round-trip, only name values changed, positions/IDs/other properties and terrain payloads preserved')
    print('PASS: all five font cmaps; eight stock language columns keep stock labels; stock input hashes unchanged')
    print('PASS: deployment equality' if args.check else 'Generated three LOCAL-ONLY mod files; do not distribute config.bin or Noe.pbo')


if __name__ == '__main__':
    main()

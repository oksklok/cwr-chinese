"""Development export: Chinese-only data + stock-reference recipes, never stock rows.

Requires a restored, verified stock source and compares reconstruction to every
known-good file. GPL-3.0-or-later + Section 7 for code; APL-SA for Chinese text.
"""
import argparse
import csv
import difflib
import io
import json
import shutil
from pathlib import Path

from install_core import PATCH, HEADER, digest, read_stock, stock_globals, csv_bytes, reconstruct, require


def payload_file(file):
    data = file.read_bytes()
    if file.relative_to(PATCH).as_posix() == 'multiplayer/text-references.json':
        recipes = json.loads(data)
        data = (json.dumps({name: {member: [edit[:3] for edit in edits] for member, edits in members.items()}
                           for name, members in recipes.items()}, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    return data


def assemble(output):
    """Assemble safe data from the committed recipe and existing authored assets."""
    require(not output.exists(), 'Choose an absent payload output')
    recipe = Path(__file__).with_name('payload.json').read_bytes()
    manifest = json.loads(recipe)
    # The recipe has keys, Chinese values, references and hashes, not stock columns.
    data = {rel: payload_file(PATCH / rel) for rel in manifest['files']}
    require(all(digest(value) == manifest['files'][rel] for rel, value in data.items()), 'Authored payload asset differs')
    output.mkdir(parents=True)
    (output / 'payload.json').write_bytes(recipe)
    for rel, value in data.items():
        dest = output / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(value)
    print('PASS: Chinese-only payload assembled; ten finished fonts; no commercial game data/client')


def export(game, output, record=False):
    require(not output.exists(), 'Choose an absent payload output')
    original_files = {p.relative_to(game).as_posix(): digest(p.read_bytes())
                      for p in game.rglob('*') if p.is_file()}
    require(not any('/@' in '/' + r or r.startswith('.crwc') for r in original_files), 'Source is not clean')
    # Our independent earlier stock inventories plus reversal hashes certify the restored source.
    backup = PATCH.parents[1] / 'game-local/localization-backup'
    expected = {}
    for section, prefix in [('1985-original', 'Campaigns/1985/'), ('resistance-original', 'Campaigns/resistance/'), ('standalone-original', 'Missions/')]:
        base = backup / section
        for entry in json.loads((base / 'before-hashes.json').read_text(encoding='utf-8-sig')):
            file = Path(entry['Path'])
            try:
                rel = file.relative_to(PATCH.parents[1] / 'game-local/Remastered').as_posix()
            except ValueError:
                continue
            if rel.split('/')[0].startswith('@'):
                continue  # Earlier inventories also recorded our prototype; not original game data.
            expected[rel] = entry['Hash'].lower()
    for section, prefix in [('1985-original', 'Campaigns/1985/'), ('resistance-original', 'Campaigns/resistance/'), ('standalone-original', 'Missions/')]:
        for entry in json.loads((backup / section / 'reversal.json').read_text(encoding='utf-8-sig')):
            rel = prefix + entry['Relative'].replace('\\', '/')
            if entry['Existed']:
                expected[rel] = entry['Hash'].lower()
            else:
                expected.pop(rel, None)
                require(rel not in original_files, f'Originally absent file exists: {rel}')
    ambush = 'Missions/02Infantry.Abel/description.ext'
    expected[ambush] = digest((backup / 'standalone-original/02Infantry.Abel/description.ext').read_bytes())
    require(set(original_files) == set(expected), 'Restored source file inventory differs from verified originals')
    require(all(original_files.get(r) == h for r, h in expected.items()),
            'Restored game does not match original inventories: ' + str([r for r,h in expected.items() if original_files.get(r) != h][:10]))
    globals_ = stock_globals(game)
    # Single canonical fallbacks are either references into installed data or authored GPL runtime labels.
    import sys
    sys.path.insert(0, str(PATCH))
    from validate_ui import RUNTIME_LITERALS
    authored = dict(RUNTIME_LITERALS)
    authored.update({'STR_CWRC_MASTER_DISABLED': 'Operated by disabled',
                     'STR_CWRC_MASTER_OPERATED_BY': 'Operated by %s'})
    candidates = [(r, (game / r).read_bytes()) for r in original_files
                  if r.lower().endswith(('.csv', '.ext', '.html', '.sqm', '.sqs')) or r == 'BIN/CONFIG.BIN']
    cache = {}

    def ref_span(value):
        if value not in cache:
            found = None
            for encoding in ('utf-8', 'cp1252', 'cp1250', 'cp1251'):
                try:
                    raw = value.encode(encoding)
                except UnicodeEncodeError:
                    continue
                if not raw:
                    continue
                for rel, data in candidates:
                    pos = data.find(raw)
                    if pos >= 0:
                        found = ['span', rel, pos, len(raw), encoding]
                        break
                if found:
                    break
            cache[value] = found
        return cache[value]

    records = []
    for table in sorted(PATCH.rglob('*.csv')):
        rows = list(csv.reader(io.StringIO(table.read_text(encoding='utf-8-sig')), strict=True))
        if not rows or 'ChineseTraditional' not in rows[0]:
            continue
        rel = table.relative_to(PATCH).as_posix()
        source = None
        if rel.startswith('campaign/'):
            source = 'Campaigns/' + rel.removeprefix('campaign/')
            if not (game / source).exists():
                source = source.replace('stringtable.utf8.csv', 'stringtable.csv')
        elif rel.startswith('standalone/'):
            source = 'Missions/' + rel.removeprefix('standalone/')
        elif rel.startswith('multiplayer/'):
            source = rel.removeprefix('multiplayer/')
        elif rel.startswith('wizard/'):
            source = [rel.removeprefix('wizard/').removesuffix('/stringtable.utf8.csv') + '.pbo', 'stringtable.utf8.csv']
        elif rel.startswith('mission/'):
            source = 'Campaigns/1985/missions/02combinedarms.eden/stringtable.utf8.csv'
        stock = read_stock(game, source) if source else {}
        translated = []
        for row in rows[1:]:
            key, old = row[0], row[:9]
            reference = None
            if key in stock and stock[key] == old:
                reference = ['row', source, key]
            elif key in globals_ and globals_[key] == old:
                reference = ['global', key]
            elif key.startswith('STR_CWRC_MAP_'):
                _, _, _, world, location = key.split('_', 4)
                reference = ['terrain', world, location]
            elif all(v == '' for v in row[1:9]):
                reference = ['empty']
            else:
                # Text aliases preserve their source's language cells or English-only stock fallback.
                candidates_rows = [(source, k, v) for k,v in stock.items()]
                if key == 'STR_c02n01':
                    other = 'Missions/C02Battlefields.Eden/stringtable.utf8.csv'
                    candidates_rows += [(other,k,v) for k,v in read_stock(game,other).items()]
                for src, k, v in candidates_rows:
                    if v[1:] == old[1:]:
                        reference = ['alias', src, k, False]
                        break
                    if [v[1]] * 8 == old[1:]:
                        reference = ['alias', src, k, True]
                        break
                if reference is None and len(set(row[1:9])) == 1:
                    reference = ref_span(row[1])
                    if reference is None:
                        for file in original_files:
                            for index in (-1, -2):
                                parts = Path(file).parts
                                if len(parts) < abs(index):
                                    continue
                                value = parts[index]
                                for extensions in range(3):
                                    if value == row[1]:
                                        reference = ['identifier', file, index, extensions]
                                        break
                                    value = value.rsplit('.', 1)[0]
                                if reference:
                                    break
                            if reference:
                                break
                    if reference is None and authored.get(key) == row[1]:
                        reference = ['authored', row[1]]
            require(reference is not None, f'No stock/authored fallback provenance: {rel} {key} {row[1:9]}')
            translated.append([key, row[9], row[10], reference])
        records.append({'path': rel, 'header': rows[0], 'rows': translated, 'sha256': digest(table.read_bytes())})
    require(len(records) == 217, 'Incomplete table inventory')
    edits = []
    for rel in ('campaign/1985/description.ext', 'campaign/resistance/description.ext', 'standalone/02Infantry.Abel/description.ext'):
        src = rel.replace('campaign/', 'Campaigns/').replace('standalone/', 'Missions/')
        old = (game / src).read_bytes()
        new = (PATCH / rel).read_bytes()
        ops = []
        for tag, a, b, c, d in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
            if tag != 'equal':
                ops.append([a, b-a, new[c:d].decode('utf-8')])
        # Export only authored inserted reference syntax, not copied stock mission configuration.
        require(all(not text or re_safe(text) for _,_,text in ops), f'Non-reference config payload: {rel} {ops}')
        edits.append({'path': rel, 'source': src, 'operations': ops, 'sha256': digest(new)})
    files = {}
    selected = list((PATCH / 'font').glob('*.ttf')) + list((PATCH / 'font/ChineseTraditional').glob('*.ttf'))
    selected += [PATCH / rel for rel in ('mod/bin/config-extra.cpp', 'mod/bin/stringtable.csv', 'ui/config.cpp',
                 'wizard/stock-hashes.json', 'multiplayer/stock-hashes.json', 'multiplayer/text-references.json',
                 'font/OFL.txt', 'font/NOTICE.md', 'font/ChineseTraditional/NOTICE.md')]
    output.mkdir(parents=True)
    for file in selected:
        rel = file.relative_to(PATCH).as_posix()
        # MP recipes contain small stock needles; remove redundant English/Chinese columns from payload copy.
        data = payload_file(file)
        files[rel] = digest(data)
        dest = output / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    manifest = {'schema': 1, 'codeLicense': 'GPL-3.0-or-later with repository Section 7 terms',
                'contentLicense': 'APL-SA', 'fontLicense': 'OFL-1.1',
                'attribution': 'Original game: Bohemia Interactive. CRWC: new Simplified/Traditional Chinese translations and display-reference adaptations; unofficial, noncommercial patch.',
                'sources': original_files, 'tables': records, 'edits': edits, 'files': files}
    (output / 'payload.json').write_bytes((json.dumps(manifest, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8'))
    with __import__('tempfile').TemporaryDirectory() as temp:
        reconstruct(game, output, Path(temp))
    if record:
        Path(__file__).with_name('payload.json').write_bytes((output / 'payload.json').read_bytes())
    print(f'PASS: {len(records)} exact reconstructed tables; three exact metadata files; {len(original_files)} verified stock inputs')


def re_safe(text):
    return all(c.isalnum() or c in '_$;" =\t\r\n' for c in text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='operation', required=True)
    generate = commands.add_parser('export', help='Development only: verify original inventories and record the recipe')
    generate.add_argument('game', type=Path)
    generate.add_argument('output', type=Path)
    generate.add_argument('--record-manifest', action='store_true')
    package = commands.add_parser('assemble', help='Assemble safe payload from the committed recipe; no game/backup required')
    package.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.operation == 'export':
        export(args.game.resolve(), args.output.resolve(), args.record_manifest)
    else:
        assemble(args.output.resolve())

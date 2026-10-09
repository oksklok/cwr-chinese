"""Validate the 30 authored GOG 3.05 MP translations and local-only mod banks."""
import html
import json
import re
import sys

from fontTools.ttLib import TTFont
from validate_campaign import GAME, PATCH, anchors, digest, placeholders, text_references, CHINESE
from validate_resistance import stock_csv_rows, tags

sys.path.insert(0, str(PATCH / 'multiplayer'))
from build_missions import overlay_payloads, pack, stock_files, tree_hash


def require(condition, *detail):
    if not condition:
        raise ValueError(detail)


def rows(path):
    parsed = stock_csv_rows(path.read_text(encoding='utf-8-sig'), strict=True)
    header = next(r for r in parsed if r and r[0] == 'LANGUAGE')
    values = [r for r in parsed if r and r[0].startswith('STR')]
    require(all(len(r) == len(header) for r in values), 'malformed row', path)
    require(len({r[0] for r in values}) == len(values), 'duplicate key', path)
    return header, values


def main():
    from validate_campaign import check_traditional
    check_traditional(PATCH / 'multiplayer')
    root = PATCH / 'multiplayer'
    hashes = json.loads((root / 'stock-hashes.json').read_text(encoding='utf-8'))
    repairs = json.loads((root / 'text-references.json').read_text(encoding='utf-8'))
    installed = {p.name for p in (GAME / 'MPMissions').iterdir() if p.is_dir() and (p / 'mission.sqm').is_file()}
    translated = {p.parent.name for p in (root / 'MPMissions').glob('*/stringtable.utf8.csv')}
    require(installed == translated == set(hashes) and len(installed) == 30, 'folder coverage')
    count = extra_count = unchanged = 0
    chars = set()
    for name, expected_hash in hashes.items():
        files = stock_files(GAME / 'MPMissions' / name)
        require(tree_hash(files) == expected_hash, 'original stock assets changed', name)
        old_header, old = rows(GAME / 'MPMissions' / name / 'stringtable.utf8.csv')
        new_header, new = rows(root / 'MPMissions' / name / 'stringtable.utf8.csv')
        added = [edit for edits in repairs.get(name, {}).values() for edit in edits]
        require(new_header == old_header[:9] + ['ChineseSimplified', 'ChineseTraditional'] + old_header[9:], 'language columns', name)
        require([r[0] for r in new] == [r[0] for r in old] + [e[2] for e in added], 'exact keys/case/order', name)
        for source, target in zip(old, new):
            key, english, chinese = source[0], source[1], target[CHINESE]
            require(source[:9] == target[:9] and source[9:] == target[11:], 'stock languages/comment changed', name, key)
            for check in (placeholders, text_references, anchors, tags):
                require(check(english) == check(chinese), check.__name__, name, key)
            require(re.findall(r'<[^>]+>', english) == re.findall(r'<[^>]+>', chinese), 'exact HTML tag sequence', name, key)
            require(english.count('\\n') == chinese.count('\\n') and english.count('\n') == chinese.count('\n'), 'line breaks', name, key)
            require(bool(english) == bool(chinese), 'empty value', name, key)
            # Retained stock dead-end scaffolding, codes/models and a semantic
            # callsign are explicit exceptions, not unreviewed English prose.
            plain = re.sub(r'<[^>]*>', '', html.unescape(chinese))
            latin = re.findall(r'[A-Za-z][A-Za-z0-9-]*', plain)
            allowed = {'M1A1', 'M16', 'M16A2', 'AK47', 'AK-47', 'BIS', 'BMP', 'SCUD', 'T55', 'T-55',
                       'T72', 'T-72', 'T80', 'T-80', 'M2', 'M60', 'PK', 'SVD', 'UAZ', 'V3S', 'HK',
                       'RPG', 'LAW', 'HEAT', 'HE', 'NATO', 'AT', 'ZSU', 'ZSU-23-4', 'Swordfish',
                       'Everon', 'Malden', 'Kolgujev', 'Nogova', 'Skalice'}
            require(all(t in allowed or len(t) == 1 or re.fullmatch(r'[A-Za-z]{2}\d{2}|(?:Description(?:Text)?End|DescrTextEnd|PopisTextEnd)\d', t)
                        for t in latin), 'unreviewed Latin prose/token', name, key, latin)
            chars.update(map(ord, html.unescape(chinese)))
        for row, edit in zip(new[len(old):], added):
            source_literal, reference, key = edit[:3]
            if len(edit) == 5:
                english, chinese = edit[3:]
            else:
                require(len(edit) == 3, 'literal recipe shape', name)
                # Distribution-safe recipes omit redundant source/Chinese cells.
                # Recover the original literal from the verified stock needle.
                quoted = re.findall(r'"([^"\r\n]*)"', source_literal)
                require(len(quoted) == 1 or source_literal == 'onLoadMission=Nogovo', 'literal source shape', name, key)
                english = quoted[0] if quoted else source_literal.partition('=')[2]
                chinese = row[CHINESE]
            require(key in reference and row[:10] == [key] + [english] * 8 + [chinese] and row[11:] == ['CRWC localized display literal'], 'literal display repair', name, key)
            chars.update(map(ord, chinese))
        payloads = overlay_payloads(GAME, name, expected_hash)
        require(set(payloads) == set(files), 'commercial member set changed', name)
        for filename in files:
            if filename != 'stringtable.utf8.csv' and filename not in repairs.get(name, {}):
                require(payloads[filename] == files[filename], 'non-text asset changed', name, filename)
                unchanged += 1
        require(pack(payloads) == (GAME / '@zhcn-prototype/MPMissions' / (name + '.pbo')).read_bytes(), 'deployment equality', name)
        count += len(old)
        extra_count += len(added)
    require((count, extra_count) == (1511, 27), 'key totals', count, extra_count)
    for role in ('title', 'body', 'mono', 'serif', 'hand'):
        path = PATCH / f'font/cwr_{role}.ttf'
        with TTFont(path) as font:
            require(not (chars - set(font.getBestCmap()) - {9, 10, 13}), 'missing glyphs', role)
        require(digest(path) == digest(GAME / f'@zhcn-prototype/Fonts/ChineseSimplified/cwr_{role}.ttf'), 'font deployment', role)
    print(f'PASS: 30 authored MP folders; {count} stock keys + {extra_count} literal-display keys; all other language/comment columns unchanged')
    print(f'PASS: exact keys/order, UTF-8, formats/references/HTML/line breaks, five unchanged fonts, stock hashes and deployed banks; {unchanged} non-text members unchanged')


if __name__ == '__main__':
    main()

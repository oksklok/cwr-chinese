"""Focused Resistance checks against the backed-up local GOG 3.05 installation."""
import collections
import csv
import html
import io
import json
import re
import struct
from pathlib import Path

from fontTools.ttLib import TTFont
from validate_campaign import (GAME, PATCH, REPO, anchors, base_globals, digest,
                               placeholders, table, text_references, strip_identity_keys, strip_campaign_labels, global_overrides, HEADER, check_stock_columns, stock_columns, CAMPAIGN_LABELS)

CAMPAIGN = PATCH / 'campaign/resistance'
BACKUP = REPO / 'game-local/localization-backup/resistance-original'
LABELS = {'Resistance': '抵抗力量', 'Chapter I - The Outrage': '第一章——暴行',
          'Chapter II - The War': '第二章——战争', 'Chapter IIII - Revenge': '第三章——复仇'}
ADDONS = ('6G30.pbo', 'kozl.pbo', 'O.pbo', 'O_WP.PBO')
# Two stock references are absent from their tables. Only add text aliases.
REPAIRED_KEYS = {
    'stringtable.utf8.csv': {'STRD_D06n52': 'Enemy base'},
    'missions/x01facetoface.noe/stringtable.utf8.csv': {
        'STRD_Dx02t51': 'US Special Forces Command Post'},
}


def stock_csv_rows(text, strict=False):
    # Stock tables have spaces before opening quotes. CsvReadCell skips those
    # spaces before deciding whether a field is quoted; commas inside stay data.
    return list(csv.reader(io.StringIO(text), skipinitialspace=True, strict=strict))


def addon_globals(with_rows=False):
    """Read only stock add-on CSV members, including their other language columns."""
    values = {}
    for name in sorted(p.name for p in (GAME / 'AddOns').glob('*.pbo')):
        data = (GAME / 'AddOns' / name).read_bytes()
        pos, entries = 0, []
        while True:
            end = data.index(b'\0', pos)
            member = data[pos:end].decode('cp1252')
            pos = end + 1
            method, original, _, _, size = struct.unpack_from('<5I', data, pos)
            pos += 20
            if not member:
                if method == 0x56657273:  # PBO version/properties header
                    while data[pos]:
                        pos = data.index(b'\0', data.index(b'\0', pos) + 1) + 1
                    pos += 1
                    continue
                break
            entries.append((member, method, original, size))
        for member, method, original, size in entries:
            payload = data[pos:pos + size]
            pos += size
            if member.lower() not in ('stringtable.csv', 'stringtable.utf8.csv'):
                continue
            if method:
                assert method == 0x43707273, ('unexpected PBO compression', name)
                # Stock OFP LZSS, matching IO/Streams/SsCompress.cpp; checksum verified.
                ring = bytearray(b' ' * 4078 + b'\0' * 18)
                cursor, flags, offset, out = 4078, 0, 0, bytearray()
                while len(out) < original:
                    flags >>= 1
                    if not flags & 256:
                        flags = payload[offset] | 0xff00
                        offset += 1
                    literal = flags & 1
                    if literal:
                        byte, count = payload[offset], 1
                        offset += 1
                    else:
                        lo, hi = payload[offset:offset + 2]
                        offset += 2
                        distance, count = lo | ((hi & 0xf0) << 4), (hi & 15) + 3
                    for _ in range(count):
                        byte = byte if literal else ring[(cursor - distance) & 4095]
                        out.append(byte)
                        ring[cursor] = byte
                        cursor = (cursor + 1) & 4095
                        if len(out) == original:
                            break
                assert sum(out) & 0xffffffff == struct.unpack_from('<I', payload, offset)[0], name
                payload = bytes(out)
            utf8 = member.lower().endswith('.utf8.csv')
            rows = stock_csv_rows(payload.decode('utf-8-sig' if utf8 else 'latin1').replace('\r\r\n', '\n'))
            header = next((r for r in rows if r and r[0].upper() == 'LANGUAGE'), ['LANGUAGE', 'English'])
            for row in rows:
                if len(row) < 2 or not row[0].startswith('STR'):
                    continue
                translations = {}
                for language, value in zip(header[1:], row[1:]):
                    encoding = 'cp1250' if language.lower() in ('czech', 'polish') else 'cp1251' if language.lower() == 'russian' else 'cp1252'
                    translations[language.title()] = value if utf8 else value.encode('latin1').decode(encoding, errors='replace')
                english = translations.get('English', '')
                values[row[0]] = ([row[0]] + [translations.get(language, english) for language in
                                  ('English', 'French', 'Italian', 'Spanish', 'German', 'Czech', 'Polish', 'Russian')]
                                 if with_rows else english.strip())
    return values


def tags(value):
    # This caption is literal text, not an HTML element.
    return (collections.Counter() if value in ('<Cutscene>', '<过场动画>')
            else collections.Counter(re.findall(r'<[^>]+>', value)))


def main():
    from validate_campaign import check_traditional
    check_traditional(CAMPAIGN)
    installed = GAME / 'Campaigns/resistance'
    folders = {p.name for p in (CAMPAIGN / 'missions').iterdir() if p.is_dir()}
    assert folders == {p.name for p in (installed / 'missions').iterdir() if p.is_dir()}
    assert len(folders) == 39
    base = base_globals()
    overlay = global_overrides()
    chars, count, unresolved = set(), 0, set()
    for key, value in overlay.items():
        assert key in base, ('unknown global key', key)
        assert placeholders(value) == placeholders(base[key]), ('global placeholder', key)
        assert text_references(value) == text_references(base[key]), ('global reference', key)
        chars.update(map(ord, html.unescape(value)))
    shared = table(CAMPAIGN / 'stringtable.utf8.csv', strict=True)
    for path in sorted(CAMPAIGN.rglob('stringtable.utf8.csv')):
        relative = path.relative_to(CAMPAIGN)
        original = BACKUP / relative
        if relative.parent == Path('.'):
            original = BACKUP / 'stringtable.csv'
        old, new = table(original), table(path, strict=True)
        check_stock_columns(path, original)
        repairs = REPAIRED_KEYS.get(relative.as_posix(), {})
        metadata = {}
        if relative == Path('stringtable.utf8.csv'):
            key = 'STR_CWRC_IDENTITY_VIKTOR_CANONICAL'
            canonical = stock_columns(original.read_bytes(), False)['STR_RESISTANCE_IDENTITY_VIKTOR_TROSKA']
            rows = list(csv.reader(io.StringIO(path.read_text(encoding='utf-8')), strict=True))
            row = next(r for r in rows if r[0] == key)
            assert row == [key] + canonical[1:] + [canonical[1], canonical[1]], 'Canonical identity language spellings'
            metadata[key] = canonical[1]
        assert list(new) == list(old) + list(repairs) + list(metadata), ('exact keys/case/order', relative)
        old.update(repairs)
        old.update(metadata)
        for key, value in new.items():
            assert placeholders(value) == placeholders(old[key]), ('placeholder', relative, key)
            assert text_references(value) == text_references(old[key]), ('text reference', relative, key)
            assert anchors(value) == anchors(old[key]), ('HTML attributes', relative, key)
            assert tags(value) == tags(old[key]), ('HTML tags', relative, key)
            assert not re.search(r'\{H\d+\}', value), ('worksheet token', relative, key)
            assert bool(value) == bool(old[key]), ('empty source text', relative, key)
            chars.update(map(ord, html.unescape(value)))
            count += key not in metadata
        available = set(new) | set(shared) | set(base) | set(overlay) | set(CAMPAIGN_LABELS)
        prior = set(old) | set(shared) | set(base)
        for page in (installed / relative.parent).glob('*.utf8.html'):
            refs = {k.upper() for k in re.findall(r'\$(STR\w+)', page.read_text(encoding='utf-8-sig'), re.I)}
            assert not refs - {k.upper() for k in available}, ('missing HTML reference', page)
        for source in (installed / relative.parent).iterdir():
            if source.suffix.lower() not in ('.sqm', '.sqs', '.ext'):
                continue
            text = source.read_bytes().decode('utf-8', errors='replace')
            text = '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith(';'))
            refs = set(re.findall(r'(?:[\x24@]|localize[\s\x22]+)(STR\w+)', text, re.I))
            assert not (refs - available) - (refs - prior), ('new unresolved runtime reference', source)
            unresolved.update((relative.parent.as_posix(), k) for k in refs - available)
        assert path.read_bytes() == (installed / relative).read_bytes(), ('deployment', relative)
    assert count == 1310
    config = strip_identity_keys(strip_campaign_labels((CAMPAIGN / 'description.ext').read_bytes()))
    for english, chinese in LABELS.items():
        assert config.count(('name = "' + english + '";').encode()) == 1
        chars.update(map(ord, chinese))
    assert config == (BACKUP / 'description.ext').read_bytes(), 'Non-display configuration changed'
    assert (CAMPAIGN / 'description.ext').read_bytes() == (installed / 'description.ext').read_bytes()
    for role in ('title', 'body', 'mono', 'serif', 'hand'):
        path = PATCH / f'font/cwr_{role}.ttf'
        with TTFont(path) as font:
            missing = chars - set(font.getBestCmap()) - {9, 10, 13}
        assert not missing, (role, 'missing glyphs', sorted(missing))
        assert digest(path) == digest(GAME / f'@zhcn-prototype/Fonts/ChineseSimplified/cwr_{role}.ttf')
    assert digest(PATCH / 'mod/bin/stringtable.utf8.csv') == digest(GAME / '@zhcn-prototype/bin/stringtable.utf8.csv')
    manifest = json.loads((BACKUP / 'reversal.json').read_text(encoding='utf-8-sig'))
    for entry in manifest:
        if entry['Existed']:
            assert digest(BACKUP / entry['Relative']) == entry['Hash'], ('original backup', entry['Relative'])
    allowed = {(installed / e['Relative']).resolve() for e in manifest}
    allowed.add((GAME / '@zhcn-prototype/bin/stringtable.utf8.csv').resolve())
    # The five verified, byte-identical mod fonts moved to the language-only
    # directory; their old flat paths must now be absent (checked by CWC).
    allowed.update((GAME / f'@zhcn-prototype/Fonts/cwr_{role}.ttf').resolve()
                   for role in ('title', 'body', 'mono', 'serif', 'hand'))
    # Later standalone CSV replacements have their own stricter whole-install
    # baseline. Keep this older baseline strict for every other game file.
    for path in (PATCH / 'standalone').rglob('stringtable.utf8.csv'):
        allowed.add((GAME / 'Missions' / path.relative_to(PATCH / 'standalone')).resolve())
    # The fresh CWC wording pass replaces only these CSVs. Its own validator
    # verifies them; CWC scripts, configuration, audio and all other files
    # remain covered by this pre-Resistance whole-install baseline.
    cwc = PATCH / 'campaign/1985'
    allowed.add((GAME / 'Campaigns/1985/description.ext').resolve())  # Exact display-only diff checked by CWC validator.
    allowed.add((GAME / 'Missions/02Infantry.Abel/description.ext').resolve())  # Checked by standalone validator.
    allowed.update((GAME / 'Campaigns/1985' / p.relative_to(cwc)).resolve()
                   for p in cwc.rglob('stringtable.utf8.csv'))
    before = json.loads((BACKUP / 'before-hashes.json').read_text(encoding='utf-8-sig'))
    unchanged = 0
    for entry in before:
        path = Path(entry['Path'])
        if path.resolve() not in allowed:
            assert digest(path) == entry['Hash'], ('unrelated game file changed', path)
            unchanged += 1
    print(f'PASS: Resistance, {len(folders)} mission/support folders; {count} authored keys + 1 canonical identity metadata key; {len(overlay)} shared globals')
    print(f'PASS: exact keys/order, UTF-8, placeholders, HTML, references, deployment, five unchanged fonts')
    print(f'PASS: {unchanged} other game files unchanged (identity display metadata checked separately; executable, scripts, audio and lip-sync unchanged)')
    print(f'Stock unresolved literal runtime references: {len(unresolved)}: {sorted(unresolved)}')


if __name__ == '__main__':
    main()

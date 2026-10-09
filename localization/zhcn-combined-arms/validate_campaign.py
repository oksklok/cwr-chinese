"""Focused checks against a backed-up GOG 3.05 installation; run from repo root."""
import collections
import csv
import hashlib
import html
import io
import json
import os
import re
from pathlib import Path

from fontTools.ttLib import TTFont

PATCH = Path(os.environ.get('CWRC_TRANSLATION_ROOT', Path(__file__).resolve().parent)).resolve()
REPO = Path(os.environ.get('CWRC_VALIDATION_REPO', Path(__file__).resolve().parent.parents[1])).resolve()
GAME = REPO / 'game-local/Remastered'
BACKUP = REPO / 'game-local/localization-backup/1985-original'
CAMPAIGN = PATCH / 'campaign/1985'
LANGUAGES = ['English', 'French', 'Italian', 'Spanish', 'German', 'Czech', 'Polish', 'Russian']
HEADER = ['LANGUAGE'] + LANGUAGES + ['ChineseSimplified', 'ChineseTraditional']
CHINESE = 9
CAMPAIGN_LABELS = {
    'STR_CWRC_CAMPAIGN_CWC': ('1985 - Cold War Crisis', '1985——冷战危机'),
    'STR_CWRC_CWC_PROLOGUE': ('PROLOGUE', '序章'),
    'STR_CWRC_CWC_PART1': ('Part I - BATTLESTATIONS', '第一章——战斗部署'),
    'STR_CWRC_CWC_PART2': ('Part II - THE EVIL GENERAL', '第二章——邪恶的将军'),
    'STR_CWRC_CWC_PART3': ('Part III - THE ROAD TO WAR', '第三章——战争之路'),
    'STR_CWRC_CWC_PART4': ('Part IV - COUNTDOWN TO ARMAGEDDON', '第四章——末日倒计时'),
    'STR_CWRC_CWC_EPILOGUE': ('EPILOGUE', '尾声'),
    'STR_CWRC_CAMPAIGN_RESISTANCE': ('Resistance', '抵抗力量'),
    'STR_CWRC_RES_PART1': ('Chapter I - The Outrage', '第一章——暴行'),
    'STR_CWRC_RES_PART2': ('Chapter II - The War', '第二章——战争'),
    'STR_CWRC_RES_PART3': ('Chapter IIII - Revenge', '第三章——复仇'),
}
REPAIRED_KEYS = {'00training.abel': {'STRM_00v16a'}, '28killdozer.eden': {'STR_END'}}
GENERATED_GROUP_KEYS = {
    'STR_CFG_GRPNAMES_' + k for k in
    ('ALPHA', 'BRAVO', 'CHARLIE', 'DELTA', 'ECHO', 'FOXTROT', 'GOLF', 'HOTEL',
     'NOVEMBER', 'KILO', 'YANKEE', 'ZULU', 'TWO', 'THREE', 'SIX', 'BUFFALO', 'GUARDIAN', 'CONVOY', 'FOX')
} | {'STR_CFG_GRPCOL_' + k for k in ('BLACK', 'RED', 'GREEN', 'BLUE', 'YELLOW', 'ORANGE', 'PINK')}


def global_overrides():
    values = table(PATCH / 'mod/bin/stringtable.utf8.csv', strict=True)
    path = PATCH / 'mod/bin/stringtable_groups.utf8.csv'
    rows = list(csv.reader(io.StringIO(path.read_bytes().decode('utf-8')), strict=True))
    assert rows[0] == HEADER
    groups = {r[0]: r for r in rows[1:]}
    assert len(groups) == len(rows) - 1 == 26 and set(groups) == GENERATED_GROUP_KEYS
    assert all(len(r) == len(HEADER) and all(r) for r in groups.values())
    stock = list(csv.reader(io.StringIO((GAME / 'BIN/STRINGTABLE.CSV').read_bytes().decode('latin1'))))
    originals = {r[0]: r for r in stock[1:] if r and r[0] in groups}
    for key, row in groups.items():
        for index in range(1, 9):
            encoding = 'cp1250' if index in (6, 7) else 'cp1251' if index == 8 else 'cp1252'
            assert row[index] == originals[key][index].encode('latin1').decode(encoding), ('Stock group column', key, index)
    assert path.read_bytes() == (GAME / '@zhcn-prototype/bin' / path.name).read_bytes(), 'Group deployment'
    assert not set(values) & set(groups), 'Duplicate shared group keys'
    values.update({key: row[CHINESE] for key, row in groups.items()})
    path = PATCH / 'mod/bin/stringtable_ui.utf8.csv'
    rows = list(csv.reader(io.StringIO(path.read_text(encoding='utf-8')), strict=True))
    assert rows[0] == HEADER
    ui = {r[0]: r[CHINESE] for r in rows[1:]}
    assert len(ui) == len(rows) - 1 and all(len(r) == len(HEADER) for r in rows[1:]), 'UI duplicate/malformed rows'
    assert not set(ui) & set(values), 'Duplicate shared UI keys'
    assert path.read_bytes() == (GAME / '@zhcn-prototype/bin' / path.name).read_bytes(), 'UI deployment'
    values.update(ui)
    return values


def generated_names():
    path = PATCH / 'mod/bin/stringtable_generated.utf8.csv'
    rows = list(csv.reader(io.StringIO(path.read_bytes().decode('utf-8')), strict=True))
    assert rows[0] == HEADER
    values = {r[0]: r for r in rows[1:]}
    assert len(values) == len(rows) - 1 == 26, 'Generated-name keys/duplicates'
    assert all(len(r) == len(HEADER) and all(r) and len(set(r[1:9])) == 1 for r in values.values())
    assert values['STR_SINGLE_CATEGORY_RESISTANCE'][1] == 'Resistance'
    assert path.read_bytes() == (GAME / '@zhcn-prototype/bin' / path.name).read_bytes(), 'Generated-name deployment'
    return values


def strip_identity_keys(config):
    """Allow only opt-in display metadata with an exact stock-name fallback."""
    values = generated_names()
    # This stock identity used a localized name property. Keep script/save names
    # canonical while retaining the original key for display in every language.
    config = config.replace(b'\t\tname = $STR_CWRC_IDENTITY_VIKTOR_CANONICAL;\n\t\tnameKey = "STR_RESISTANCE_IDENTITY_VIKTOR_TROSKA";\n',
                            b'\t\tname = $STR_RESISTANCE_IDENTITY_VIKTOR_TROSKA;\n')
    pattern = rb'(\t\tname = "([^"\r\n]+)";\r?\n)\t\tnameKey = "(STR_CWRC_IDENTITY_[A-Z_]+)";\r?\n'

    def remove(match):
        key = match[3].decode('ascii')
        assert key in values and values[key][2] == match[2].decode('ascii'), ('Identity fallback', key)
        return match[1]

    cleaned = re.sub(pattern, remove, config)
    assert b'nameKey' not in cleaned, 'Unexpected identity metadata'
    return cleaned


def strip_campaign_labels(config):
    path = PATCH / 'mod/bin/stringtable_campaigns.utf8.csv'
    rows = list(csv.reader(io.StringIO(path.read_text(encoding='utf-8')), strict=True))
    assert rows[0] == HEADER and len(rows) == 12
    for row in rows[1:]:
        english, chinese = CAMPAIGN_LABELS[row[0]]
        assert row[:10] == [row[0]] + [english] * 8 + [chinese], ('Campaign display metadata', row[0])
        config = re.sub(rb'\t+nameKey = "' + row[0].encode() + rb'";\r?\n', b'', config)
    assert path.read_bytes() == (GAME / '@zhcn-prototype/bin' / path.name).read_bytes()
    return config


def table(path, strict=False):
    data = path.read_bytes()
    try:
        text = data.decode('utf-8-sig')
    except UnicodeDecodeError:
        assert not strict, f'Not UTF-8: {path}'
        # Stock multi-language tables contain other legacy code pages; only
        # their English column is consumed, and localized output is strict UTF-8.
        text = data.decode('cp1252', errors='replace')
    rows = list(csv.reader(io.StringIO(text), strict=strict))
    header = next((r for r in rows if r and r[0] == 'LANGUAGE'), ['LANGUAGE', 'English'])
    column = header.index('ChineseSimplified') if strict and 'ChineseSimplified' in header else 1
    if strict:
        legacy_backup = 'localization-backup' in path.parts and header == ['LANGUAGE', 'English']
        assert rows and (header == HEADER or legacy_backup), (path, 'invalid header')
        assert all(len(row) == len(header) and row[0].upper().startswith('STR')
                   for row in rows[1:]), (path, 'malformed translation row')
    values = {}
    for row in rows:
        if not row or not row[0].upper().startswith('STR'):
            continue
        key = row[0]
        assert len(row) >= 2 and key not in values, (path, key, 'invalid/duplicate row')
        if strict:
            assert len(row) == len(header), (path, key, 'unexpected columns')
            assert '\ufffd' not in row[column], (path, key, 'replacement character')
        values[key] = row[column]
    return values


def stock_columns(data, utf8=True):
    """Stock language cells using CsvReadCell whitespace and legacy French rules."""
    from validate_resistance import stock_csv_rows
    rows = stock_csv_rows(data.decode('utf-8-sig' if utf8 else 'latin1').replace('\r\r\n', '\n'))
    header = next(r for r in rows if r and r[0].upper() == 'LANGUAGE')
    values = {}
    for row in rows:
        if not row or not row[0].upper().startswith('STR'):
            continue
        if not utf8 and len(row) > len(header) and 'French' in header:
            column = header.index('French')
            extra = len(row) - len(header) + 1
            row[column:column + extra] = [','.join(row[column:column + extra])]
        assert len(row) <= len(header), ('Surplus stock columns', row[0])
        cells = dict(zip(header[1:], row[1:]))
        translated = []
        for language in LANGUAGES:
            cell = cells.get(language, '')
            if not utf8:
                encoding = 'cp1250' if language in ('Czech', 'Polish') else 'cp1251' if language == 'Russian' else 'cp1252'
                cell = cell.encode('latin1').decode(encoding, errors='replace')
            translated.append(cell.replace('\r\n', '\n'))
        values[row[0]] = [row[0]] + translated
    return values


def check_stock_columns(path, original):
    source = stock_columns(original.read_bytes(), original.name.endswith('.utf8.csv'))
    rows = list(csv.reader(io.StringIO(path.read_text(encoding='utf-8')), strict=True))
    assert rows[0] == HEADER
    for row in rows[1:]:
        if row[0] in source:
            assert row[:CHINESE] == source[row[0]], ('Stock language cells', path, row[0])


def placeholders(value):
    return collections.Counter(re.findall(r'%(?:\d+(?:\.\d+)?|\.\d+[a-zA-Z]|[a-zA-Z])', value))


def anchors(value):
    return collections.Counter(re.findall(r'(?:href|name)\s*=\s*[\"\']([^\"\']+)[\"\']', value, re.I))


def text_references(value):
    return collections.Counter(re.findall(r'\$STR\w+', value, re.I))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def check_traditional(*roots):
    """Both Chinese columns share protected syntax; TC uses separate font assets."""
    chars = set(map(ord, '简体中文繁體中文'))
    count = 0
    for root in roots:
        for path in sorted(root.rglob('*.csv')):
            rows = list(csv.reader(io.StringIO(path.read_text(encoding='utf-8-sig')), strict=True))
            if not rows or 'ChineseSimplified' not in rows[0]:
                continue
            header = rows[0]
            assert header[:11] == HEADER and len({r[0] for r in rows[1:]}) == len(rows)-1, path
            for row in rows[1:]:
                assert len(row) == len(header), (path, 'malformed bilingual row')
                simplified, traditional = row[9:11]
                assert bool(simplified) == bool(traditional) and '\ufffd' not in traditional, (path, row[0])
                for check in (placeholders, anchors, text_references):
                    assert check(simplified) == check(traditional), (path, row[0], check.__name__)
                assert re.findall(r'</?[A-Za-z][^>]*>', simplified) == re.findall(r'</?[A-Za-z][^>]*>', traditional), (path, row[0], 'HTML')
                for token in ('\\n', '\\r', '\n', '\r'):
                    assert simplified.count(token) == traditional.count(token), (path, row[0], 'breaks')
                if row[0] == 'STR_CWRC_IDENTITY_VIKTOR_CANONICAL':
                    assert traditional == simplified == row[1] == 'Victor Troska', 'Canonical identity was translated'
                chars.update(map(ord, html.unescape(traditional)))
                count += 1
    for role in ('title', 'body', 'mono', 'serif', 'hand'):
        path = PATCH / f'font/ChineseTraditional/cwr_{role}.ttf'
        with TTFont(path) as font:
            assert not chars - set(font.getBestCmap()) - {9, 10, 13}, (role, 'Traditional missing glyphs')
        assert digest(path) == digest(GAME / f'@zhcn-prototype/Fonts/ChineseTraditional/cwr_{role}.ttf'), ('Traditional font deployment', role)
    print(f'PASS: {count} Traditional Chinese cells; protected syntax, canonical identity and five-font deployment/coverage')


def base_globals():
    base = table(GAME / 'BIN/STRINGTABLE.CSV')
    for path in sorted((GAME / 'BIN').glob('STRINGTABLE_*.utf8.csv')):
        base.update(table(path))
    # Resistance equipment includes addon-only keys absent from BIN tables.
    # Read their stock originals so the existing global-key check stays strict.
    from validate_resistance import addon_globals
    for key, value in addon_globals().items():
        base.setdefault(key, value)
    return base


def main():
    check_traditional(CAMPAIGN, PATCH / 'mod/bin', PATCH / 'mission')
    mission_names = {p.name for p in (CAMPAIGN / 'missions').iterdir() if p.is_dir()}
    installed_names = {p.name for p in (GAME / 'Campaigns/1985/missions').iterdir() if p.is_dir()}
    assert mission_names == installed_names, 'Incomplete campaign-folder coverage'
    base = base_globals()
    global_table = global_overrides()
    chars = {ord(c) for row in generated_names().values() for c in row[CHINESE]}
    chars.update(map(ord, '简体中文'))
    for _, chinese in CAMPAIGN_LABELS.values():
        chars.update(map(ord, chinese))
    assert (PATCH / 'mod/bin/config-extra.cpp').read_bytes() == (GAME / '@zhcn-prototype/bin/config-extra.cpp').read_bytes(), 'Language registration deployment'
    for key, value in global_table.items():
        assert key in base, ('unknown global key', key)
        assert placeholders(value) == placeholders(base[key]), ('global placeholder', key)
        assert text_references(value) == text_references(base[key]), ('global text reference', key)
        chars.update(map(ord, html.unescape(value)))
    shared = table(CAMPAIGN / 'stringtable.utf8.csv', strict=True)
    count = 0
    for path in sorted(CAMPAIGN.rglob('stringtable.utf8.csv')):
        relative = path.relative_to(CAMPAIGN)
        original = BACKUP / relative
        if not original.exists():
            original = GAME / 'Campaigns/1985' / relative.with_name('stringtable.csv')
        old, new = table(original), table(path, strict=True)
        check_stock_columns(path, original)
        additions = REPAIRED_KEYS.get(relative.parent.name, set())
        assert set(old) | additions == set(new), ('campaign keys/exact case', relative)
        for key, value in new.items():
            if key in old:
                assert placeholders(value) == placeholders(old[key]), ('campaign placeholder', relative, key)
                assert text_references(value) == text_references(old[key]), ('campaign text reference', relative, key)
                if anchors(old[key]):
                    assert anchors(value) == anchors(old[key]), ('HTML links', relative, key)
            chars.update(map(ord, html.unescape(value)))
            count += 1
        available = set(new) | set(shared) | set(base) | set(global_table) | set(CAMPAIGN_LABELS)
        for page in (GAME / 'Campaigns/1985' / relative.parent).glob('*.utf8.html'):
            # The HTML preview resolver compares keys case-insensitively,
            # unlike runtime LocalizeString. Exact CSV spellings are checked above.
            refs = {s.upper() for s in re.findall(r'\$(STR\w+)', page.read_text(encoding='utf-8-sig'), re.I)}
            assert not refs - {k.upper() for k in available}, ('unresolved HTML', page, refs)
        if relative.parent.name != '1985':
            for source in (GAME / 'Campaigns/1985' / relative.parent).iterdir():
                if source.suffix.lower() not in ('.sqm', '.sqs', '.ext'):
                    continue
                refs = set(re.findall(r'(?:[\x24@]|localize[\s\x22]+)(STR\w+)',
                                      source.read_bytes().decode('utf-8', errors='replace'), re.I))
                # A few stock speech definitions have no text in any original
                # table. Require no new unresolved references, rather than
                # inventing captions for untranscribed voice recordings.
                prior_available = set(old) | set(shared) | set(base)
                assert not (refs - available) - (refs - prior_available), ('new missing runtime key', source)
        assert path.read_bytes() == (GAME / 'Campaigns/1985' / relative).read_bytes(), ('deployment', relative)
    labels = {
        '1985 - Cold War Crisis': '1985——冷战危机',
        'PROLOGUE': '序章', 'Part I - BATTLESTATIONS': '第一章——战斗部署',
        'Part II - THE EVIL GENERAL': '第二章——邪恶的将军',
        'Part III - THE ROAD TO WAR': '第三章——战争之路',
        'Part IV - COUNTDOWN TO ARMAGEDDON': '第四章——末日倒计时', 'EPILOGUE': '尾声',
    }
    config = strip_identity_keys(strip_campaign_labels((CAMPAIGN / 'description.ext').read_bytes()))
    for english, chinese in labels.items():
        config = config.replace(('"' + chinese + '"').encode(), ('"' + english + '"').encode())
    assert config == (BACKUP / 'description.ext').read_bytes(), 'Non-display campaign configuration changed'
    assert (CAMPAIGN / 'description.ext').read_bytes() == (GAME / 'Campaigns/1985/description.ext').read_bytes()
    for role in ('title', 'body', 'mono', 'serif', 'hand'):
        path = PATCH / f'font/cwr_{role}.ttf'
        with TTFont(path) as font:
            missing = chars - set(font.getBestCmap()) - {9, 10, 13}
        assert not missing, (role, 'missing glyphs', sorted(missing))
        assert digest(path) == digest(GAME / f'@zhcn-prototype/Fonts/ChineseSimplified/cwr_{role}.ttf')
        assert not (GAME / f'@zhcn-prototype/Fonts/cwr_{role}.ttf').exists(), 'Global mod font leaks into stock languages'
    for name in ('stringtable.csv', 'stringtable.utf8.csv'):
        assert digest(PATCH / 'mod/bin' / name) == digest(GAME / '@zhcn-prototype/bin' / name)
    assert table(CAMPAIGN / 'missions/02combinedarms.eden/stringtable.utf8.csv') == table(PATCH / 'mission/stringtable.utf8.csv')
    manifest = json.loads((BACKUP / 'reversal.json').read_text(encoding='utf-8-sig'))
    for entry in manifest:
        if entry['Existed']:
            assert digest(BACKUP / entry['Relative']) == entry['Hash'], ('original backup hash', entry['Relative'])
    allowed = {(GAME / 'Campaigns/1985' / entry['Relative']).resolve() for entry in manifest}
    # Only the separate Resistance patch targets are exempt from this older
    # CWC-only baseline. validate_resistance verifies those and all other files.
    resistance = PATCH / 'campaign/resistance'
    allowed.update((GAME / 'Campaigns/resistance' / p.relative_to(resistance)).resolve()
                   for p in resistance.rglob('*') if p.is_file())
    unchanged = 0
    for entry in json.loads((BACKUP / 'before-hashes.json').read_text(encoding='utf-8-sig')):
        path = Path(entry['Path'])
        if path.resolve() not in allowed:
            assert digest(path) == entry['Hash'], ('unrelated installed file changed', path)
            unchanged += 1
    missions = len(list((CAMPAIGN / 'missions').iterdir()))
    print(f'PASS: {missions} mission folders; {count} campaign keys; {len(global_table)} partial global overrides')
    print(f'PASS: references, placeholders, deployment, five-font coverage; {unchanged} other campaign files unchanged')


if __name__ == '__main__':
    main()

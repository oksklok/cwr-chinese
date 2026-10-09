"""Focused stock-column, formatting, font and wizard-overlay checks for GOG 3.05."""
import csv
import html
import io
import json
import re
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from validate_campaign import (GAME, PATCH, anchors, global_overrides, placeholders,
                               text_references, CHINESE, stock_columns, HEADER, check_traditional)
from validate_resistance import addon_globals, stock_csv_rows, tags

LANGUAGES = ['English', 'French', 'Italian', 'Spanish', 'German', 'Czech', 'Polish', 'Russian']
# These four stock option labels contain literal brackets, not HTML markup.
ANGLE_LABELS = {
    'STR_RADIO_UNASSIGNED': ('<Unassigned>', '<未分配>'),
    'STR_NOT_ASSIGNED': ('<Unassigned>', '<未分配>'),
    'STR_MPW_NEW_EDIT': ('<< New - Editor >>', '<< 新建——编辑器 >>'),
    'STR_MPW_NEW_WIZ': ('<< New - Wizard >>', '<< 新建——向导 >>'),
}
RUNTIME_LITERALS = {
    'STR_DISP_OPT_CTL_GAMEPAD_REVERSE_Y': 'Y-axis inversion',
    'STR_CWRC_RESET_CATEGORY_TITLE': 'Reset "%s" bindings?',
    'STR_CWRC_RESET_CATEGORY_BODY': 'All current %s bindings in this category will be replaced with defaults.',
    'STR_CWRC_RESET_CATEGORY_BUTTON': 'Reset',
    'STR_CWRC_MOD_LOAD_FAILED': 'Could not load the selected mod set. Reverted to the previous one.',
    'STR_CWRC_STICK_BUTTON_9': 'Stick Btn. #9',
    'STR_CWRC_STICK_BUTTON_10': 'Stick Btn. #10',
    'STR_CWRC_G36_AUTO': 'G36 Auto',
    'STR_CWRC_SFX_MUSIC': "'Music'",
    **{'STR_CWRC_RTRACK' + suffix.upper(): 'Resistance Track ' + suffix
       for suffix in ('1a', '1b', '2', '3', '4', '5', '6', '7', '8', '9', '10')},
}


def read_rows(path, legacy=False):
    rows = stock_csv_rows(path.read_bytes().decode('latin1' if legacy else 'utf-8-sig'), strict=True)
    if rows and any(r and r[0] == 'LANGUAGE' for r in rows):
        return stock_columns(path.read_bytes(), not legacy)
    result = {}
    for row in rows:
        if len(row) < 2 or not row[0].startswith('STR'):
            continue
        if legacy:
            row = [row[0]] + [v.encode('latin1').decode('cp1250' if i in (6, 7) else 'cp1251' if i == 8 else 'cp1252', errors='replace')
                              for i, v in enumerate(row[1:], 1)]
        result[row[0]] = row[:9]
    return result


def main():
    check_traditional(PATCH / 'wizard', PATCH / 'mod/bin')
    stock = read_rows(GAME / 'BIN/STRINGTABLE.CSV', legacy=True)
    for path in sorted((GAME / 'BIN').glob('STRINGTABLE_*.utf8.csv')):
        stock.update(read_rows(path))
    for key, row in addon_globals(with_rows=True).items():
        stock.setdefault(key, row)
    chars = set()
    # All stock-key shards, including the original 1,101-key partial overlay,
    # now preserve English as well as the other seven shipped languages.
    for name in ('stringtable.utf8.csv', 'stringtable_groups.utf8.csv', 'stringtable_ui.utf8.csv'):
        path = PATCH / 'mod/bin' / name
        cells = list(csv.reader(io.StringIO(path.read_text(encoding='utf-8')), strict=True))
        assert cells[0] == HEADER
        for row in cells[1:]:
            assert row[:CHINESE] == (stock[row[0]] + [''] * 8)[:CHINESE], ('Stock global cells', name, row[0])
            chars.update(map(ord, html.unescape(row[CHINESE])))
        assert path.read_bytes() == (GAME / '@zhcn-prototype/bin' / name).read_bytes()
    path = PATCH / 'mod/bin/stringtable_ui.utf8.csv'
    rows = list(csv.reader(io.StringIO(path.read_text(encoding='utf-8')), strict=True))
    assert rows[0] == HEADER and len({r[0] for r in rows[1:]}) == len(rows) - 1
    for row in rows[1:]:
        assert len(row) == len(HEADER) and row[0] in stock, ('Unknown/malformed UI key', row[0])
        original = stock[row[0]]
        assert row[:CHINESE] == (original + [''] * 8)[:9], ('Stock language columns', row[0])
        chinese = row[CHINESE]
        assert placeholders(chinese) == placeholders(original[1]), ('UI placeholders', row[0])
        assert anchors(chinese) == anchors(original[1]), ('UI anchors', row[0])
        if row[0] in ANGLE_LABELS:
            assert (original[1], chinese) == ANGLE_LABELS[row[0]], ('Literal bracket label', row[0])
        else:
            assert tags(chinese) == tags(original[1]), ('UI HTML tags', row[0])
        assert text_references(chinese) == text_references(original[1]), ('UI references', row[0])
        assert chinese.count('\\n') == original[1].count('\\n'), ('UI literal breaks', row[0])
        assert chinese.count('\n') == original[1].count('\n'), ('UI physical breaks', row[0])
        assert '\ufffd' not in chinese, row[0]
        chars.update(map(ord, html.unescape(chinese)))
    # Opt-in selector/world metadata and documented runtime/config literals.
    path = PATCH / 'mod/bin/stringtable_ui_generated.utf8.csv'
    custom = list(csv.reader(io.StringIO(path.read_text(encoding='utf-8')), strict=True))
    assert custom[0] == HEADER and len(custom) == 58
    assert len({r[0] for r in custom[1:]}) == 57
    assert not {r[0] for r in custom[1:]} & set(global_overrides())
    selectors = set()
    for folder in ('SPTemplates', 'Templates', 'MPMissions'):
        for source in (GAME / folder).iterdir():
            if source.is_dir() or source.suffix.lower() == '.pbo':
                name = source.stem if source.suffix.lower() == '.pbo' else source.name
                identity = name.rsplit('.', 1)[0]
                selectors.add('STR_CWRC_WIZARD_' + identity.upper().replace('-', '_'))
    worlds = {'EDEN': 'Everon', 'ABEL': 'Malden', 'CAIN': 'Kolgujev',
              'NOE': 'Nogova', 'INTRO': 'Desert Island'}
    for row in custom[1:]:
        assert len(row) == len(HEADER) and len(set(row[1:9])) == 1
        if row[0].startswith('STR_CWRC_WIZARD_'):
            assert row[0] in selectors, ('Unknown selector identity', row[0])
        elif row[0].startswith('STR_CWRC_WORLD_'):
            assert row[2] == worlds[row[0].removeprefix('STR_CWRC_WORLD_')]
        elif row[0] in RUNTIME_LITERALS:
            assert row[2] == RUNTIME_LITERALS[row[0]], ('Runtime literal stock fallback', row[0])
        else:
            assert row[0] in ('STR_CWRC_MASTER_DISABLED', 'STR_CWRC_MASTER_OPERATED_BY')
        assert placeholders(row[CHINESE]) == placeholders(row[1])
        chars.update(map(ord, row[CHINESE]))
    assert path.read_bytes() == (GAME / '@zhcn-prototype/bin' / path.name).read_bytes()
    sys.path.insert(0, str(PATCH / 'terrain'))
    from build_labels import Config, pbo_parts
    sys.path.insert(0, str(PATCH / 'ui'))
    from build_addon import payload as ui_payload
    assert (GAME / '@zhcn-prototype/AddOns/cwrc_ui.pbo').read_bytes() == ui_payload()
    config = Config((GAME / 'BIN/CONFIG.BIN').read_bytes()).root
    assert config['CfgSFX']['FunMusicSfx']['name'] == RUNTIME_LITERALS['STR_CWRC_SFX_MUSIC']
    g36 = Config(pbo_parts((GAME / 'AddOns/G36a.pbo').read_bytes())[2][b'config.bin']).root
    assert g36['CfgWeapons']['G36aBase']['FullAuto']['displayName'] == RUNTIME_LITERALS['STR_CWRC_G36_AUTO']
    resistance = Config(pbo_parts((GAME / 'AddOns/O.pbo').read_bytes())[2][b'config.bin']).root
    for suffix in ('1a', '1b', '2', '3', '4', '5', '6', '7', '8', '9', '10'):
        assert resistance['cfgMusic']['RTrack' + suffix]['name'] == RUNTIME_LITERALS['STR_CWRC_RTRACK' + suffix.upper()]
    count = 0
    manifest = json.loads((PATCH / 'wizard/stock-hashes.json').read_text())
    for relative in manifest:
        payload = pbo_parts((GAME / relative).read_bytes())[2][b'stringtable.utf8.csv']
        original = stock_columns(payload)
        path = PATCH / 'wizard' / relative.removesuffix('.pbo') / 'stringtable.utf8.csv'
        translated = list(csv.reader(io.StringIO(path.read_text(encoding='utf-8')), strict=True))
        assert translated[0] == HEADER
        assert [r[0] for r in translated[1:]] == list(original), ('Wizard key/order', relative)
        for row in translated[1:]:
            old = original[row[0]]
            assert len(row) == len(HEADER) and row[:CHINESE] == [v.replace('\r\n', '\n') for v in old[:9]], ('Wizard stock columns', relative, row[0])
            for checker in (placeholders, anchors, text_references, tags):
                assert checker(row[CHINESE]) == checker(old[1]), (checker.__name__, relative, row[0])
            assert row[CHINESE].count('\\n') == old[1].count('\\n'), ('Wizard literal breaks', relative, row[0])
            assert row[CHINESE].count('\n') == old[1].count('\n'), ('Wizard physical breaks', relative, row[0])
            assert '\ufffd' not in row[CHINESE], (relative, row[0])
            chars.update(map(ord, html.unescape(row[CHINESE])))
            count += 1
    for role in ('title', 'body', 'mono', 'serif', 'hand'):
        with TTFont(PATCH / f'font/cwr_{role}.ttf') as font:
            assert not chars - set(font.getBestCmap()) - {9, 10, 13}, ('UI missing glyphs', role)
    print(f'PASS: {len(rows)-1} new stock UI keys, 57 documented custom keys, {len(manifest)} wizard folders / {count} keys')
    print('PASS: stock other-language columns, keys/order, formats, links, references, line breaks, five-font coverage')


if __name__ == '__main__':
    main()

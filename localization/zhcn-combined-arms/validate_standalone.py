"""Focused standalone checks against the backed-up local GOG 3.05 installation."""
import html
import csv
import io
import json
import re
from pathlib import Path

from fontTools.ttLib import TTFont
from validate_campaign import (GAME, PATCH, REPO, anchors, base_globals, digest,
                               placeholders, table, text_references, strip_identity_keys, GENERATED_GROUP_KEYS, global_overrides, check_stock_columns)
from validate_resistance import tags

MISSIONS = PATCH / 'standalone'
INSTALLED = GAME / 'Missions'
BACKUP = REPO / 'game-local/localization-backup/standalone-original'
REPAIRS = {
    'C01Convoy.Eden': {'STRCAMP_r30': 'STRCAMP_c01r30'},
    'Resistance/R01WarCry.Noe': {'STR_c02n01': None},
}


def main():
    from validate_campaign import check_traditional
    check_traditional(MISSIONS)
    originals = {p.relative_to(BACKUP) for p in BACKUP.rglob('stringtable.utf8.csv')}
    translated = {p.relative_to(MISSIONS) for p in MISSIONS.rglob('stringtable.utf8.csv')}
    installed = {p.relative_to(INSTALLED) for p in INSTALLED.rglob('stringtable.utf8.csv')}
    mission_folders = {p.parent.relative_to(INSTALLED) for p in INSTALLED.rglob('mission.sqm')}
    assert originals == translated == installed, 'Incomplete standalone table coverage'
    assert {p.parent for p in translated} == mission_folders, 'Incomplete mission-folder coverage'
    assert len(translated) == 24
    base = base_globals()
    overlay = global_overrides()
    previous = table(BACKUP / 'pre-standalone-global.utf8.csv', strict=True)
    # Roster composition appends this suffix directly to a name. Parentheses
    # repair the observed run-together label.
    assert previous['STR_BRIEF_GROUP_LEADER'] == '小队队长'
    assert overlay['STR_BRIEF_GROUP_LEADER'] == '（小队队长）'
    # Final QA shortened this heading after observing clipping at 1280x900.
    # Keep the exception exact rather than allowing arbitrary wording changes.
    assert previous['STR_BRIEFING'] == '任务简报 (%s, %s %d)'
    assert overlay['STR_BRIEFING'] == '简报（%s，%s %d）'
    # Later spacing QA may change ASCII spaces, but not the wording of prior keys.
    assert all(overlay[k].replace(' ', '') == v.replace(' ', '')
               for k, v in previous.items()
               if k not in {'STR_BRIEF_GROUP_LEADER', 'STR_BRIEFING'}), 'Existing global override wording changed'
    assert set(overlay) - set(previous) == {
        'STR_DISP_SINGLE_TITLE', 'STR_SINGLE_OPEN', 'STR_SINGLE_PLAY', 'STR_SINGLE_RESUME',
        'STR_RADIO', 'STR_RADIO_CUSTOM', 'STR_OBJECTIVE_UPDATED'} | GENERATED_GROUP_KEYS | {
            row[0] for row in csv.reader(io.StringIO((PATCH / 'mod/bin/stringtable_ui.utf8.csv').read_text(
                encoding='utf-8')), strict=True) if row and row[0].startswith('STR')}
    chars, count, unresolved = set(), 0, set()
    for key, value in overlay.items():
        assert key in base, ('unknown global', key)
        assert placeholders(value) == placeholders(base[key]), ('global placeholder', key)
        assert text_references(value) == text_references(base[key]), ('global reference', key)
        chars.update(map(ord, html.unescape(value)))
    for relative in sorted(translated):
        old = table(BACKUP / relative)
        new = table(MISSIONS / relative, strict=True)
        check_stock_columns(MISSIONS / relative, BACKUP / relative)
        repairs = REPAIRS.get(relative.parent.as_posix(), {})
        assert list(new) == list(old) + list(repairs), ('exact keys/case/order', relative)
        for alias, target in repairs.items():
            source = (old[target] if target else table(
                BACKUP / 'C02Battlefields.Eden/stringtable.utf8.csv')[alias])
            old[alias] = source
            assert new[alias] == (new[target] if target else '任务完成'), ('caption alias', relative, alias)
        for key, value in new.items():
            source = old[key]
            assert placeholders(value) == placeholders(source), ('placeholder', relative, key)
            assert text_references(value) == text_references(source), ('reference', relative, key)
            assert anchors(value) == anchors(source), ('HTML attributes', relative, key)
            assert tags(value) == tags(source), ('HTML tags', relative, key)
            assert value.count('\\n') == source.count('\\n'), ('line-break token', relative, key)
            assert bool(value) == bool(source), ('empty source value', relative, key)
            chars.update(map(ord, html.unescape(value)))
            count += 1
        available = set(new) | set(base) | set(overlay)
        prior = set(old) | set(base)
        folder = INSTALLED / relative.parent
        for page in folder.glob('*.utf8.html'):
            refs = {k.upper() for k in re.findall(r'\$(STR\w+)', page.read_text(encoding='utf-8-sig'), re.I)}
            assert not refs - {k.upper() for k in available}, ('missing HTML reference', page)
        for path in folder.rglob('*'):
            if not path.is_file() or path.suffix.lower() not in ('.sqm', '.sqs', '.ext'):
                continue
            text = path.read_bytes().decode('utf-8', errors='replace')
            text = '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith(';'))
            refs = set(re.findall(r'(?:[\x24@]|localize[\s\x22]+)(STR\w+)', text, re.I))
            assert not (refs - available) - (refs - prior), ('new unresolved runtime reference', path)
            unresolved.update((relative.parent.as_posix(), k) for k in refs - available)
        assert (MISSIONS / relative).read_bytes() == (INSTALLED / relative).read_bytes(), ('deployment', relative)
    assert count == 1284  # 1,282 original keys plus two exact-spelling text repairs
    for role in ('title', 'body', 'mono', 'serif', 'hand'):
        path = PATCH / f'font/cwr_{role}.ttf'
        with TTFont(path) as font:
            missing = chars - set(font.getBestCmap()) - {9, 10, 13}
        assert not missing, (role, 'missing glyphs', sorted(missing))
        assert digest(path) == digest(GAME / f'@zhcn-prototype/Fonts/ChineseSimplified/cwr_{role}.ttf')
    assert digest(PATCH / 'mod/bin/stringtable.utf8.csv') == digest(GAME / '@zhcn-prototype/bin/stringtable.utf8.csv')
    manifest = json.loads((BACKUP / 'reversal.json').read_text(encoding='utf-8-sig'))
    assert {Path(e['Relative']) for e in manifest} == translated
    for entry in manifest:
        assert entry['Existed'] and digest(BACKUP / entry['Relative']) == entry['Hash'], ('original backup', entry)
    allowed = {(INSTALLED / p).resolve() for p in translated}
    allowed.add((GAME / '@zhcn-prototype/bin/stringtable.utf8.csv').resolve())
    allowed.update((GAME / f'@zhcn-prototype/Fonts/cwr_{role}.ttf').resolve()
                   for role in ('title', 'body', 'mono', 'serif', 'hand'))
    identity = Path('02Infantry.Abel/description.ext')
    config = (MISSIONS / identity).read_bytes()
    assert config == (INSTALLED / identity).read_bytes(), 'Standalone identity deployment'
    # The stock file has no final newline; apply_patch adds exactly one.
    assert strip_identity_keys(config).removesuffix(b'\n') == (BACKUP / identity).read_bytes(), 'Non-display standalone config changed'
    allowed.add((INSTALLED / identity).resolve())
    # Only CWC's freshly retranslated CSVs supersede this older baseline.
    # validate_campaign checks those; all other campaign files stay protected.
    cwc = PATCH / 'campaign/1985'
    allowed.add((GAME / 'Campaigns/1985/description.ext').resolve())  # Exact display-only diff checked by CWC validator.
    allowed.add((GAME / 'Campaigns/resistance/description.ext').resolve())  # Checked by Resistance validator.
    allowed.update((GAME / 'Campaigns/1985' / p.relative_to(cwc)).resolve()
                   for p in cwc.rglob('stringtable.utf8.csv'))
    # The later cross-campaign unit-designator pass also supersedes Resistance
    # CSV wording. validate_resistance checks those tables and deployment;
    # every non-CSV Resistance file remains protected by this baseline.
    resistance = PATCH / 'campaign/resistance'
    allowed.update((GAME / 'Campaigns/resistance' / p.relative_to(resistance)).resolve()
                   for p in resistance.rglob('stringtable.utf8.csv'))
    before = json.loads((BACKUP / 'before-hashes.json').read_text(encoding='utf-8-sig'))
    stock_config_hash = next(e['Hash'] for e in before if Path(e['Path']).resolve() == (INSTALLED / identity).resolve())
    assert digest(BACKUP / identity) == stock_config_hash, 'Standalone identity backup hash'
    unchanged = 0
    for entry in before:
        path = Path(entry['Path'])
        if path.resolve() not in allowed:
            assert digest(path) == entry['Hash'], ('unrelated game file changed', path)
            unchanged += 1
    print(f'PASS: standalone, {len(translated)} mission folders; {count} keys; {len(overlay) - len(previous)} new globals')
    print('PASS: exact keys/order, UTF-8, placeholders, line-break tokens, HTML, references, deployment, five unchanged fonts')
    print(f'PASS: {unchanged} other game files unchanged (identity display metadata checked separately; executable, scripts, audio and lip-sync unchanged)')
    print(f'Stock unresolved literal runtime references: {len(unresolved)}: {sorted(unresolved)}')


if __name__ == '__main__':
    main()

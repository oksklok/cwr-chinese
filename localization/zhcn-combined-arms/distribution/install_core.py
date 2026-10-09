"""Local-only installation core. No executable or commercial data is bundled.

GPL-3.0-or-later with repository Section 7 terms. Chinese payload: APL-SA;
finished font assets: OFL-1.1. Public binary/installer compliance is separate.
"""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import os
import shutil
import stat
import struct
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

PATCH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PATCH))
from validate_campaign import HEADER, stock_columns
import validate_resistance

MOD = '@zhcn-prototype'
STATE = '.crwc-install'
RETIRED = STATE + '-retired'
# Only these stock add-ons supply referenced global rows. Their other members
# are not reconstruction inputs; table output hashes verify the required rows.
GLOBAL_ADDONS = ('6G30.pbo', 'ABox.pbo', 'Apac.pbo', 'BISCamel.pbo', 'BMP2.pbo',
                 'Bizon.pbo', 'Flags.pbo', 'G36a.pbo', 'Hunter.pbo', 'KOLO.PBO',
                 'LaserGuided.pbo', 'M2A2.pbo', 'MINI.PBO', 'Mm-1.pbo', 'O.pbo',
                 'O_WP.PBO', 'Steyr.pbo', 'XMS.pbo', 'kozl.pbo', 'trab.pbo', 'vulcan.pbo')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def target(root, relative):
    """Reject traversal, Windows aliasing, symlinks and junctions before writes."""
    require(isinstance(relative, str), 'Invalid relative path')
    p = PurePosixPath(relative)
    require(not p.is_absolute() and p.parts and all(
        v not in ('', '.', '..') and ':' not in v and '\\' not in v
        and not any(c in v for c in '<>"|?*\0') and not v.endswith(('.', ' '))
        and v.split('.')[0].upper() not in {'CON', 'PRN', 'AUX', 'NUL',
            *(f'COM{i}' for i in range(1, 10)), *(f'LPT{i}' for i in range(1, 10))}
        for v in p.parts), f'Unsafe path: {relative}')
    path = root.joinpath(*p.parts)
    cursor = root
    for part in p.parts:
        cursor = cursor / part
        require(not reparse(cursor),
                f'Reparse path: {cursor}')
    require(path.resolve().is_relative_to(root.resolve()), f'Out of bounds: {relative}')
    return path


def reparse(path):
    return path.is_symlink() or (path.exists() and bool(
        getattr(path.lstat(), 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 1024)))


def validate_record(game, record):
    require(record.get('schema') == 1 and isinstance(record.get('files'), dict), 'Invalid receipt')
    for rel, item in record['files'].items():
        target(game, rel)
        allowed = (rel.startswith(MOD + '/') or rel in ('crwc-client/PoseidonGame.exe', 'crwc-client/OpenAL32.dll')
                   or (rel.startswith(('Campaigns/1985/', 'Campaigns/resistance/', 'Missions/'))
                       and rel.endswith(('stringtable.utf8.csv', 'description.ext'))))
        require(allowed, f'Unexpected receipt target: {rel}')
        for value in (item['original'], item['installed']):
            require(value is None or (len(value) == 64 and all(c in '0123456789abcdef' for c in value)), 'Invalid receipt hash')
        require(item['installed'] is not None, 'Missing installed hash')


def state_files(state, record):
    """Validate all state contents before retiring or deleting anything."""
    known = {'receipt.json', 'pending.json'}
    # A hard termination can leave atomic_json's exclusively-created staging
    # file. Recognize only bytes (including a truncated prefix) of the precise
    # next journal/receipt; never treat arbitrary state files as disposable.
    updates = []
    if record.get('status') == 'installing':
        written = record['written']
        order = list(record['files'])
        require(written == order[:len(written)], 'Invalid recovery write order')
        updates.append(('pending.tmp', dict(record, written=order[:len(written) + 1])))
        updates.append(('receipt.tmp', {**{k: record[k] for k in ('schema', 'package', 'files')},
                                        'status': 'installed'}))
    else:
        updates.append(('receipt.tmp', dict(record, status='restore-conflicts')))
    for name, update in updates:
        path = target(state, name)
        if path.is_file():
            expected = (json.dumps(update, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
            require(expected.startswith(path.read_bytes()), f'Preserved unrecognized state file: {name}')
            known.add(name)
    known.update('backup/' + rel for rel, item in record['files'].items() if item['original'] is not None)
    actual = {p.relative_to(state).as_posix() for p in state.rglob('*') if p.is_file() or reparse(p)}
    require(not actual - known, f'Preserved unrecognized state files: {sorted(actual - known)}')
    known_dirs = {str(parent) for rel in known for parent in PurePosixPath(rel).parents if str(parent) != '.'}
    actual_dirs = {p.relative_to(state).as_posix() for p in state.rglob('*') if p.is_dir()}
    require(not actual_dirs - known_dirs, f'Preserved unrecognized state directories: {sorted(actual_dirs - known_dirs)}')
    for rel in actual | actual_dirs:
        target(state, rel)
    return actual


def resume_retired(game):
    """Cleanup is resumable even after some backups or the final journal vanished."""
    state = target(game, RETIRED)
    if not state.exists():
        return False
    require(not target(game, STATE).exists(), 'Conflicting active and retired installation state')
    anchor = next((state / name for name in ('receipt.json', 'pending.json')
                   if (state / name).is_file()), None)
    if anchor is None:
        require(not any(state.iterdir()), 'Preserved unrecognized retired state')
        state.rmdir()  # Interruption between deleting the final journal and rmdir.
        return True
    record = json.loads(anchor.read_text())
    validate_record(game, record)
    actual = state_files(state, record)
    # Keep one complete journal until every other file and directory is gone.
    for rel in sorted(actual - {anchor.name}):
        target(state, rel).unlink()
    for directory in sorted((p for p in state.rglob('*') if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        directory.rmdir()
    anchor.unlink()
    state.rmdir()
    return True


def clear_state(game, record):
    """Atomically retire restored state before resumable, bounded deletion."""
    state = target(game, STATE)
    state_files(state, record)
    require(not target(game, RETIRED).exists(), 'Conflicting retired installation state')
    os.rename(state, target(game, RETIRED))
    resume_retired(game)


def csv_bytes(rows):
    stream = io.StringIO(newline='')
    csv.writer(stream, quoting=csv.QUOTE_ALL, lineterminator='\n').writerows(rows)
    return stream.getvalue().encode('utf-8')


def read_stock(game, source):
    if isinstance(source, list):
        sys.path.insert(0, str(PATCH / 'terrain'))
        from build_labels import pbo_parts
        data = pbo_parts(target(game, source[0]).read_bytes())[2][source[1].encode()]
        name = source[1]
    else:
        data = target(game, source).read_bytes()
        name = source
    return stock_columns(data, name.lower().endswith('.utf8.csv'))


def stock_globals(game, sources=None):
    values = read_stock(game, 'BIN/STRINGTABLE.CSV')
    tables = ((game / rel for rel in sources if rel.startswith('BIN/STRINGTABLE_') and rel.endswith('.utf8.csv'))
              if sources is not None else (game / 'BIN').glob('STRINGTABLE_*.utf8.csv'))
    for p in sorted(tables):
        values.update(read_stock(game, p.relative_to(game).as_posix()))
    prior = validate_resistance.GAME
    try:
        validate_resistance.GAME = game
        for k, v in validate_resistance.addon_globals(with_rows=True, names=GLOBAL_ADDONS).items():
            values.setdefault(k, v)
    finally:
        validate_resistance.GAME = prior
    return values


def reconstruct(game, payload, out):
    """Only reconstruct language tables/reference edits; reuse stock CSV rules."""
    manifest = json.loads((payload / 'payload.json').read_text(encoding='utf-8'))
    require(manifest['schema'] == 1, 'Unsupported payload')
    globals_ = stock_globals(game, manifest.get('sources'))
    sources = {}
    for table in manifest['tables']:
        rows = [table['header']]
        for key, sc, tc, reference in table['rows']:
            kind = reference[0]
            if kind == 'row':
                src, old_key = reference[1:]
                tag = json.dumps(src)
                if tag not in sources:
                    sources[tag] = read_stock(game, src)
                cells = sources[tag][old_key][1:]
                extra = []
                if isinstance(src, str) and src.startswith('MPMissions/'):
                    originals = list(csv.reader(io.StringIO(target(game, src).read_text(encoding='utf-8-sig')),
                                                skipinitialspace=True))
                    extra = next(r[9:] for r in originals if r and r[0] == old_key)
            elif kind == 'global':
                cells, extra = globals_[reference[1]][1:], []
            elif kind == 'span':
                file, offset, size, encoding = reference[1:]
                value = target(game, file).read_bytes()[offset:offset+size].decode(encoding)
                cells, extra = [value] * 8, []
            elif kind == 'empty':
                cells, extra = [''] * 8, []
            elif kind == 'authored':
                cells, extra = [reference[1]] * 8, []
            elif kind == 'identifier':
                file, index, extensions = reference[1:]
                value = PurePosixPath(file).parts[index]
                for _ in range(extensions):
                    value = value.rsplit('.', 1)[0]
                cells, extra = [value] * 8, []
            elif kind == 'alias':
                src, old_key, english_only = reference[1:]
                original = read_stock(game, src)[old_key]
                cells, extra = ([original[1]] * 8 if english_only else original[1:]), []
            elif kind == 'terrain':
                sys.path.insert(0, str(PATCH / 'terrain'))
                from build_labels import Config, pbo_parts
                world, location = reference[1:]
                tag = 'terrain:' + ('Noe' if world == 'Noe' else 'master')
                if tag not in sources:
                    data = (target(game, 'BIN/CONFIG.BIN').read_bytes() if world != 'Noe' else
                            pbo_parts(target(game, 'AddOns/Noe.pbo').read_bytes())[2][b'config.bin'])
                    sources[tag] = Config(data).root
                value = sources[tag]['CfgWorlds'][world]['Names'][location]['name']
                cells, extra = [value] * 8, []
            else:
                raise ValueError(f'Unknown stock reference: {kind}')
            if len(table['header']) > 11 and not extra:
                extra = ['CRWC localized display literal']
            rows.append([key] + cells + [sc, tc] + extra)
        data = csv_bytes(rows)
        require(digest(data) == table['sha256'], f'Reconstruction differs: {table["path"]}')
        p = target(out, table['path'])
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    for edit in manifest['edits']:
        data = target(game, edit['source']).read_bytes()
        # Descending offsets preserve all stock bytes except these known insertions/replacements.
        for offset, count, replacement in reversed(edit['operations']):
            data = data[:offset] + replacement.encode('utf-8') + data[offset+count:]
        require(digest(data) == edit['sha256'], f'Metadata differs: {edit["path"]}')
        p = target(out, edit['path'])
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    for rel, expected in manifest['files'].items():
        data = target(payload, rel).read_bytes()
        require(digest(data) == expected, f'Payload file differs: {rel}')
        p = target(out, rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    return manifest


def run_builders(patch, game, check=False):
    """Load each existing builder with its data root redirected to reconstruction."""
    sys.path.insert(0, str(PATCH / 'terrain'))
    for folder, filename in [('terrain', 'build_labels.py'), ('wizard', 'build_templates.py'),
                             ('multiplayer', 'build_missions.py'), ('ui', 'build_addon.py')]:
        file = PATCH / folder / filename
        spec = importlib.util.spec_from_file_location('crwc_builder_' + folder, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if folder == 'terrain':
            module.PATCH = patch
            module.TABLE = patch / 'mod/bin/stringtable_terrain.utf8.csv'
        elif folder in ('wizard', 'multiplayer'):
            module.ROOT = patch / folder
        else:
            module.__file__ = str(patch / folder / filename)
        saved = sys.argv
        try:
            sys.argv = [str(file), str(game)] + (['--check'] if check else [])
            module.main()
        finally:
            sys.argv = saved


def load_payload(payload):
    data = (payload / 'payload.json').read_bytes()
    manifest = json.loads(data)
    require(manifest['schema'] == 1, 'Unsupported payload')
    for rel, expected in manifest['files'].items():
        require(digest(target(payload, rel).read_bytes()) == expected, f'Payload file differs: {rel}')
    # Git/Windows newline normalization must not turn an identical payload into an upgrade.
    canonical = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return manifest, digest(b'CWRC-mod-layout-2\0' + canonical)


def verify_sources(game, manifest, receipt=None):
    tracked = receipt['files'] if receipt else {}
    if 'BIN/CONFIG.BIN' in source_inputs(manifest):
        require(not target(game, 'BIN/config.cpp').exists(),
                'Conflicting base BIN/config.cpp: it overrides the required CONFIG.BIN. Restore the base config or keep that modification in a separate mod.')
    for rel, expected in source_inputs(manifest).items():
        p = target(game, rel)
        if rel in tracked:
            require(digest(p.read_bytes()) == tracked[rel]['installed'], f'User modified installed file: {rel}')
            backup = target(game / STATE / 'backup', rel)
            require(digest(backup.read_bytes()) == expected, f'Original backup differs: {rel}')
        else:
            if rel in {'AddOns/' + name for name in GLOBAL_ADDONS}:
                require(p.is_file(), f'Missing required localization source: {rel}')
                continue
            require(p.is_file() and digest(p.read_bytes()) == expected,
                    f'Incompatible Remastered 3.05 source: {rel}. Restore this required file; unrelated assets/mods need not be removed.')


def verify_game(game):
    exe = target(game, 'PoseidonGame.exe')
    require(exe.is_file(), 'Select Remastered containing the original PoseidonGame.exe')
    data = exe.read_bytes()
    require(len(data) > 64 and data[:2] == b'MZ', 'Original client is not a Windows executable')
    offset = struct.unpack_from('<I', data, 60)[0]
    require(offset + 6 <= len(data) and data[offset:offset+4] == b'PE\0\0'
            and struct.unpack_from('<H', data, offset+4)[0] == 0x8664,
            'Windows x64 Remastered 3.05 is required; original 1.96/1.99 data is unsupported')
    if os.name == 'nt':
        quoted = str(exe).replace("'", "''")
        version = subprocess.check_output(['powershell.exe', '-NoProfile', '-Command',
            f"(Get-Item -LiteralPath '{quoted}').VersionInfo.ProductVersion"], text=True).strip()
        require(version == '3.05', f'Unsupported Remastered version: {version or "missing"}; expected 3.05')


def source_inputs(manifest):
    """The existing recipes need these inputs, not a storefront-wide inventory."""
    if 'tables' not in manifest:  # Small restoration fixtures and legacy receipts.
        return manifest['sources']
    needed = set()
    for table in manifest['tables']:
        for row in table['rows']:
            ref = row[3]
            if ref[0] in ('row', 'alias'):
                needed.add(ref[1][0] if isinstance(ref[1], list) else ref[1])
            elif ref[0] == 'span':
                needed.add(ref[1])
            elif ref[0] == 'terrain':
                needed.add('AddOns/Noe.pbo' if ref[1] == 'Noe' else 'BIN/CONFIG.BIN')
    needed.update(edit['source'] for edit in manifest['edits'])
    needed.update(rel for rel in manifest['sources'] if
                  (rel.startswith('BIN/') and '.csv' in rel.lower()) or
                  rel.startswith(('Templates/', 'SPTemplates/', 'MPMissions/')))
    if any(row[3][0] == 'global' for table in manifest['tables'] for row in table['rows']):
        needed.update('AddOns/' + name for name in GLOBAL_ADDONS)
    return {rel: manifest['sources'][rel] for rel in sorted(needed)}


def check_idle(game):
    if os.name == 'nt':
        # Require no matching executable running, without affecting unrelated games.
        import subprocess
        result = subprocess.run(['powershell.exe', '-NoProfile', '-Command',
            "[Console]::OutputEncoding=[Text.UTF8Encoding]::new($false); "
            "Get-CimInstance Win32_Process -Filter \"Name='PoseidonGame.exe'\" | Select-Object -ExpandProperty ExecutablePath"],
            capture_output=True, text=True, encoding='utf-8', check=True)
        paths = [Path(p.strip()).resolve() for p in result.stdout.splitlines() if p.strip()]
        require(not any(p.is_relative_to(game) for p in paths), 'Close the target game before installation/removal')


def atomic_json(path, value):
    tmp = path.with_suffix('.tmp')
    created = False
    try:
        with tmp.open('x', encoding='utf-8') as stream:
            created = True
            stream.write(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if created and tmp.exists():
            tmp.unlink()


def replace_file(source, dest):
    tmp = dest.with_name(dest.name + '.crwc-tmp')
    # Exclusive creation never truncates a conflicting file between preflight and write.
    created = False
    try:
        with tmp.open('xb') as stream:
            created = True
            with source.open('rb') as original:
                shutil.copyfileobj(original, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, dest)
    finally:
        if created and tmp.exists():
            tmp.unlink()  # This invocation exclusively created it; never delete a pre-existing conflict.


def required_space(game, payload, manifest, client=None):
    """Bound real allocations; the stock staging tree is hardlinked, not copied."""
    sizes = {rel: target(game, rel).stat().st_size for rel in source_inputs(manifest)}
    # Only these banks/configs are reconstructed by the four existing builders.
    banks = sum(size for rel, size in sizes.items() if
                rel in ('AddOns/Noe.pbo', 'BIN/CONFIG.BIN') or
                rel.startswith(('Templates/', 'MPTemplates/', 'MPMissions/')))
    source_text = sum(size for rel, size in sizes.items() if rel.lower().endswith(('.csv', '.ext')))
    # UTF-8 expansion, both Chinese cells, CSV quoting and reference insertions.
    tables = 4 * source_text + 2 * (payload / 'payload.json').stat().st_size
    authored = sum(target(payload, rel).stat().st_size for rel in manifest['files'])
    runtime = sum((client / name).stat().st_size for name in ('PoseidonGame.exe', 'OpenAL32.dll')) if client else 0
    # Reconstructed patch + staged mod + deployed outputs, original text backups,
    # runtime destination and one maximum atomic-replacement temp, plus filesystem slack.
    atomic = max([tables, runtime, authored, *[size for rel, size in sizes.items()
                 if rel in ('AddOns/Noe.pbo', 'BIN/CONFIG.BIN')]], default=0)
    mission_dirs = {PurePosixPath(table['path']).parent.relative_to('standalone').as_posix()
                    for table in manifest.get('tables', []) if table['path'].startswith('standalone/')}
    missions = sum(p.stat().st_size for rel in mission_dirs
                   for p in target(game, 'Missions/' + rel).rglob('*') if p.is_file())
    return 3 * (tables + authored) + 2 * (banks + missions) + source_text + runtime + atomic + 64 * 1024**2


def content_outputs(patch, game, mod):
    """Ordinary mod banks, generated locally from the existing table recipes."""
    sys.path.insert(0, str(PATCH / 'multiplayer'))
    from build_missions import pack
    outputs = {}
    # Campaign banks intentionally prefer loose patch files at their virtual
    # prefix (QFBank::ScanPatchFiles). Stock campaign tables therefore shadow
    # a mod bank. Retain the existing exact-backup replacements for campaigns.
    for name in ('1985', 'resistance'):
        folder = patch / 'campaign' / name
        if folder.exists():
            for f in folder.rglob('*'):
                if f.is_file():
                    outputs['Campaigns/' + name + '/' + f.relative_to(folder).as_posix()] = f
    standalone = patch / 'standalone'
    folders = sorted({f.parent for f in standalone.rglob('stringtable.utf8.csv')})
    for folder in folders:
        relative = folder.relative_to(standalone).as_posix()
        original = target(game, 'Missions/' + relative)
        require((original / 'mission.sqm').is_file(), f'Missing standalone mission: {folder.name}')
        members = {}
        for f in sorted(original.rglob('*')):
            target(game, f.relative_to(game).as_posix())
            if f.is_file():
                members[f.relative_to(original).as_posix()] = f.read_bytes()
        members.update({f.relative_to(folder).as_posix(): f.read_bytes()
                        for f in sorted(folder.rglob('*')) if f.is_file()})
        bank = mod / 'Missions' / (relative + '.pbo')
        bank.parent.mkdir(parents=True, exist_ok=True)
        bank.write_bytes(pack(members))
        outputs[MOD + '/Missions/' + relative + '.pbo'] = bank
    return outputs


def install(game, payload, client=None, fail_after=None):
    require(not reparse(game), 'Invalid game root')
    game = game.resolve()
    require(game.is_dir(), 'Invalid game root')
    check_idle(game)
    verify_game(game)
    resume_retired(game)
    manifest, package = load_payload(payload)
    state = target(game, STATE)
    receipt_path = state / 'receipt.json'
    require(not (state / 'pending.json').exists(), 'Interrupted operation: run recover first')
    receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else None
    if receipt:
        validate_record(game, receipt)
        require(receipt['schema'] == 1 and receipt['package'] == package and receipt['status'] == 'installed',
                'Different/incomplete CWRC installation. Uninstall the existing CWRC first; original backups are retained.')
        for rel, item in receipt['files'].items():
            p = target(game, rel)
            require(p.is_file() and digest(p.read_bytes()) == item['installed'], f'User modified installed file: {rel}')
        if client:
            for name in ('PoseidonGame.exe', 'OpenAL32.dll'):
                rel = 'crwc-client/' + name
                require(rel in receipt['files'] and digest((client / name).read_bytes()) == receipt['files'][rel]['installed'],
                        'Different client runtime; uninstall before changing the local client')
        verify_sources(game, manifest, receipt)
        print('PASS: recognized installation; originals retained; reinstall is an exact no-op')
        return receipt
    require(not state.exists(), f'Unrecognized installation state: {state}')
    print('STEP 10 Verifying required Remastered 3.05 sources', flush=True)
    verify_sources(game, manifest)
    require(not target(game, MOD).exists(), 'Conflicting existing Chinese mod; leave it untouched')
    require(not target(game, 'crwc-client').exists(), 'Conflicting client directory')
    required = required_space(game, payload, manifest, client)
    require(shutil.disk_usage(game).free > required, f'Insufficient staging/backup space: need {required // 1024**2 + 1} MiB free')
    print('STEP 25 Reconstructing translations and local overlays', flush=True)
    # Stage stock reads via hardlinks: builders only read commercial sources and write their mod outputs.
    with tempfile.TemporaryDirectory(prefix='crwc-stage-', dir=game.parent) as temp:
        stage = Path(temp)
        stock = stage / 'game'
        patch = stage / 'patch'
        for rel in source_inputs(manifest):
            p = target(stock, rel)
            p.parent.mkdir(parents=True, exist_ok=True)
            os.link(target(game, rel), p)
        if (game / 'PoseidonGame.exe').exists():
            os.link(target(game, 'PoseidonGame.exe'), stock / 'PoseidonGame.exe')
        reconstruct(stock, payload, patch)
        mod = stock / MOD
        shutil.copytree(patch / 'mod/bin', mod / 'bin')
        for language, source in [('ChineseSimplified', patch / 'font'), ('ChineseTraditional', patch / 'font/ChineseTraditional')]:
            dest = mod / 'Fonts' / language
            dest.mkdir(parents=True)
            for f in source.glob('*.ttf'):
                shutil.copyfile(f, dest / f.name)
            shutil.copyfile(source / 'NOTICE.md', dest / 'NOTICE.md')
            shutil.copyfile(patch / 'font/OFL.txt', dest / 'OFL.txt')
        run_builders(patch, stock)
        run_builders(patch, stock, check=True)
        outputs = {f.relative_to(stock).as_posix(): f for f in mod.rglob('*') if f.is_file()}
        # Standalone discovery uses a full mission bank; campaigns retain the
        # engine's established loose patch precedence and exact restoration.
        outputs.update(content_outputs(patch, game, mod))
        if client:
            # Developer-only local runtime input, never stored in the payload or public bundle here.
            for name in ('PoseidonGame.exe', 'OpenAL32.dll'):
                p = client / name
                require(p.is_file(), f'Missing local client runtime: {p}')
                outputs['crwc-client/' + name] = p
        for rel in outputs:
            p = target(game, rel)
            require(not p.exists() or rel in manifest['sources'], f'Conflicting output: {rel}')
            require(not p.with_name(p.name + '.crwc-tmp').exists(), f'Conflicting temporary output: {rel}')
        # Test write permissions in each existing output parent without changing its contents.
        for parent in {target(game, rel).parent for rel in outputs}:
            while not parent.exists():
                parent = parent.parent
            with tempfile.NamedTemporaryFile(prefix='.crwc-permission-', dir=parent):
                pass
        print('STEP 65 Rechecking sources and preparing exact original backups', flush=True)
        verify_sources(game, manifest)  # Recheck after staging, before the first original replacement.
        check_idle(game)
        # Prepare off to the side: a killed backup copy cannot publish half a state.
        prepared = stage / 'state'
        prepared.mkdir()
        files = {}
        for rel, source in outputs.items():
            dest = target(game, rel)
            existed = dest.exists()
            old_hash = digest(dest.read_bytes()) if existed else None
            if existed:
                backup = target(prepared / 'backup', rel)
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(dest, backup)
                require(digest(backup.read_bytes()) == old_hash, f'Backup mismatch: {rel}')
            files[rel] = {'original': old_hash, 'installed': digest(source.read_bytes())}
        pending = {'schema': 1, 'package': package, 'status': 'installing', 'files': files, 'written': []}
        atomic_json(prepared / 'pending.json', pending)
        require(not state.exists(), 'Conflicting installation state')
        os.rename(prepared, state)  # Same-volume publication; journal/backups arrive together.
        try:
            print('STEP 80 Installing verified outputs', flush=True)
            for rel, source in outputs.items():
                dest = target(game, rel)
                require((digest(dest.read_bytes()) if dest.exists() else None) == files[rel]['original'],
                        f'File changed during install: {rel}')
                dest.parent.mkdir(parents=True, exist_ok=True)
                # Journal before replacement; recovery recognizes either original or installed hash.
                pending['written'].append(rel)
                atomic_json(state / 'pending.json', pending)
                temporary = dest.with_name(dest.name + '.crwc-tmp')
                require(not temporary.exists(), f'Conflicting temporary file: {temporary}')
                replace_file(source, dest)
                if fail_after and len(pending['written']) == fail_after:
                    raise OSError('Injected installation failure')
            for rel, item in files.items():
                require(digest(target(game, rel).read_bytes()) == item['installed'], f'Installed mismatch: {rel}')
            receipt = {k: pending[k] for k in ('schema', 'package', 'files')}
            receipt['status'] = 'installed'
            atomic_json(receipt_path, receipt)
            (state / 'pending.json').unlink()
        except BaseException:
            if (state / 'pending.json').exists():
                recover(game)
            # With no pending journal, commit completed. Retain the installed
            # receipt/backups; only successful restoration may retire them.
            raise
    print(f'STEP 100 Installed {len(files)} files; originals backed up; stock executable/banks untouched', flush=True)
    return receipt


def restore(game, record, only=None):
    conflicts = []
    for rel in (only if only is not None else list(record['files'])):
        item = record['files'][rel]
        dest = target(game, rel)
        actual = digest(dest.read_bytes()) if dest.is_file() else None
        tmp = dest.with_name(dest.name + '.crwc-tmp')
        if tmp.exists():
            # A completed staged copy from a crash is ours only if its hash matches.
            if (tmp.is_file() and not reparse(tmp)
                    and digest(tmp.read_bytes()) in (item['installed'], item['original'])):
                tmp.unlink()
            else:
                conflicts.append(rel + '.crwc-tmp')
                continue
        if actual == item['original']:
            continue
        if actual != item['installed']:
            conflicts.append(rel)
            continue
        if item['original'] is None:
            dest.unlink()
        else:
            backup = target(game / STATE / 'backup', rel)
            require(digest(backup.read_bytes()) == item['original'], f'Corrupt original backup: {rel}')
            replace_file(backup, dest)
    # Remove empty patch-created directories only, never unrelated contents.
    for rel in record['files']:
        p = target(game, rel).parent
        while p != game and p != game / STATE and p.is_dir():
            try:
                p.rmdir()
            except OSError:
                break
            p = p.parent
    return conflicts


def recover(game):
    game = game.resolve()
    check_idle(game)
    if resume_retired(game):
        print('PASS: interrupted state cleanup completed')
        return
    state = target(game, STATE)
    pending = json.loads((state / 'pending.json').read_text())
    validate_record(game, pending)
    require(all(rel in pending['files'] for rel in pending['written']), 'Invalid recovery journal')
    for rel, item in pending['files'].items():
        if item['original']:
            require(digest(target(state / 'backup', rel).read_bytes()) == item['original'], f'Corrupt backup: {rel}')
    conflicts = restore(game, pending, pending['written'])
    require(not conflicts, f'Rollback preserved modified files; recovery still pending: {conflicts}')
    clear_state(game, pending)
    print('PASS: failed/interrupted installation rolled back to exact originals')


def uninstall(game):
    game = game.resolve()
    check_idle(game)
    if resume_retired(game):
        print('PASS: interrupted state cleanup completed')
        return []
    state = target(game, STATE)
    require(not (state / 'pending.json').exists(), 'Interrupted install: run recover first')
    path = state / 'receipt.json'
    record = json.loads(path.read_text())
    validate_record(game, record)
    require(record['schema'] == 1 and record['status'] in ('installed', 'restore-conflicts'), 'Invalid receipt')
    # Preflight every original backup before restoring any file.
    for rel, item in record['files'].items():
        if item['original']:
            require(digest(target(state / 'backup', rel).read_bytes()) == item['original'], f'Corrupt backup: {rel}')
    conflicts = restore(game, record)
    if conflicts:
        record['status'] = 'restore-conflicts'
        atomic_json(path, record)
        print('PRESERVED user-modified files; originals/receipt retained:', ', '.join(conflicts))
        return conflicts
    clear_state(game, record)
    print('PASS: exact original loose files restored; patch-owned files removed')
    return []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('install', 'uninstall', 'recover', 'reconstruct'))
    parser.add_argument('game', type=Path)
    parser.add_argument('--payload', type=Path, default=Path(__file__).with_name('payload'))
    parser.add_argument('--local-client', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.operation == 'install':
        require(args.local_client is not None, 'Supply --local-client with the existing private rebuilt client; no binary is bundled')
        install(args.game, args.payload, args.local_client)
    elif args.operation == 'uninstall':
        if uninstall(args.game):
            raise SystemExit(2)
    elif args.operation == 'recover':
        recover(args.game.resolve())
    else:
        require(args.output is not None and not args.output.exists(), 'Choose an absent reconstruction output')
        manifest, _ = load_payload(args.payload)
        verify_sources(args.game, manifest)
        reconstruct(args.game, args.payload, args.output)
        print('PASS: all 217 table and three metadata hashes match known-good files')


if __name__ == '__main__':
    main()

"""Developer-only build of ready-to-use CWRC content. Stock inputs are read-only.
GPL-3.0-or-later with repository Section 7 terms; Chinese text: APL-SA.
"""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
from pathlib import Path, PurePosixPath

PATCH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PATCH))
from stock import HEADER, stock_columns, addon_globals
from validate_content import validate

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
    path = root / relative
    require(path.resolve().is_relative_to(root.resolve()), f'Path outside data directory: {relative}')
    return path


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
    for k, v in addon_globals(game, with_rows=True, names=GLOBAL_ADDONS).items():
        values.setdefault(k, v)
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
        source = edit['source']
        if isinstance(source, list):
            from build_labels import pbo_parts
            data = pbo_parts(target(game, source[0]).read_bytes())[2][source[1].encode()]
        else:
            data = target(game, source).read_bytes()
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


def run_builders(patch, game, mod, check=False):
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
            sys.argv = [str(file), str(game), '--mod-dir', str(mod)] + (['--check'] if check else [])
            module.main()
        finally:
            sys.argv = saved


def build_content(game, mod):
    from make_payload import assemble
    game, mod = game.resolve(), mod.resolve()
    require(not mod.exists(), 'Choose an absent content output directory')
    require(not mod.is_relative_to(game), 'Build outside the installed game')
    # Construction and byte-exact checks happen once on the developer machine,
    # never on a player's first launch. Existing builders remain authoritative.
    with tempfile.TemporaryDirectory(prefix='cwrc-build-') as work:
        payload = Path(work) / 'payload'
        patch = Path(work) / 'patch'
        assemble(payload)
        manifest = reconstruct(game, payload, patch)
        validate(patch, manifest)
        shutil.copytree(patch / 'mod/bin', mod / 'bin', dirs_exist_ok=True)
        shutil.copytree(patch / 'campaign', mod / 'localization/Campaigns', dirs_exist_ok=True)
        for language, source in [('ChineseSimplified', patch / 'font'), ('ChineseTraditional', patch / 'font/ChineseTraditional')]:
            dest = mod / 'Fonts' / language
            dest.mkdir(parents=True, exist_ok=True)
            for font in source.glob('*.ttf'):
                shutil.copyfile(font, dest / font.name)
            shutil.copyfile(source / 'NOTICE.md', dest / 'NOTICE.md')
            shutil.copyfile(patch / 'font/OFL.txt', dest / 'OFL.txt')
        run_builders(patch, game, mod)
        sys.path.insert(0, str(PATCH / 'multiplayer'))
        from build_missions import pack
        standalone = patch / 'standalone'
        for folder in sorted({f.parent for f in standalone.rglob('stringtable.utf8.csv')}):
            relative = folder.relative_to(standalone)
            original = game / 'Missions' / relative
            require((original / 'mission.sqm').is_file(), f'Missing mission: {relative}')
            members = {f.relative_to(original).as_posix(): f.read_bytes()
                       for f in sorted(original.rglob('*')) if f.is_file()}
            members.update({f.relative_to(folder).as_posix(): f.read_bytes()
                            for f in folder.rglob('*') if f.is_file()})
            bank = mod / 'Missions' / (relative.as_posix() + '.pbo')
            bank.parent.mkdir(parents=True, exist_ok=True)
            bank.write_bytes(pack(members))
        run_builders(patch, game, mod, check=True)
    print(f'PASS: ready-to-use mod built; {len(manifest["tables"])} tables / '
          f'{len(manifest["edits"])} display-reference files verified; no player preparation')


def main():
    if sys.stdout:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('game', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        build_content(args.game, args.output)
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f'CWRC content build failed: {error}', flush=True)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

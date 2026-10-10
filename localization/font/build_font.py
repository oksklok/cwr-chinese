"""Rebuild five Chinese role fonts; requires fontTools 4.66.1.

Usage: python build_font.py SOURCE_DIRECTORY ORIGINAL_GAME_FONTS_DIRECTORY
Sources: NotoSansSC.ttf, NotoSerifSC.ttf, LXGWWenKai-Medium.ttf (see NOTICE.md).
For --language ChineseTraditional: NotoSansTC.ttf, NotoSerifTC.ttf,
Iansui-Regular.ttf; see ChineseTraditional/NOTICE.md. Existing SC fonts supply
only the Simplified picker-autonym glyph.
This is a font-only helper, not a game-data extraction/translation pipeline.
"""
import hashlib
import argparse
import csv
import json
import tempfile
from pathlib import Path

from fontTools import subset
from fontTools.merge import Merger
from fontTools.misc.transform import Transform
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from fontTools.ttLib.scaleUpem import scale_upem
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent
SOURCES = {
    'NotoSansSC.ttf': 'a3041811a78c361b1de50f953c805e0244951c21c5bd412f7232ef0d899af0da',
    'NotoSerifSC.ttf': '050080d9255a86808f2945bffac582b31ef32bc36411ce29563b4961670c66f9',
    'LXGWWenKai-Medium.ttf': 'd4bdeb38a39151d74d084cba5090f8cb7d20bf83eedb78c35939ae70b9f4e3f6',
}
TRADITIONAL_SOURCES = {
    'NotoSansTC.ttf': '864727d210d54f2537bbe23b3a839436c3992af72de9322af5270897246bd44f',
    'NotoSerifTC.ttf': '0077e18f57c6908f4a000969880940bdb0dad057c0e8d98b49dc364c3d1b09c6',
    'Iansui-Regular.ttf': '6e6340d80d618a42b48ade9370c34fa37a8210750c6fbc8efe65f23716538a2b',
}
# Font.cpp width scales; only Chinese outlines/advances are corrected.
ROLES = {
    'title': ('NotoSansSC.ttf', 700, .628),
    'body': ('NotoSansSC.ttf', 500, 1.0),
    'mono': ('NotoSansSC.ttf', 500, .8),
    'serif': ('NotoSerifSC.ttf', 600, .935),
    'hand': ('LXGWWenKai-Medium.ttf', 500, 1.05),
}
BASE_HASHES = {
    'title': '3651c7b0d540d412a536320e1ab296daeb254db20fa38bd33b186ff9bf1657fe',
    'body': 'cb244f96329b3504d7c198206a0b4ff1660fafb63882d9c211a1785d7083f424',
    'mono': 'c74ca4dc965b2f791483a43c4abd3b6b270b761c34dfe1b91fe2a038dd3a1de7',
    'serif': 'cc431374627239bcd1f7d1d82e45d0fe49867a81946a31289c17d43001ab1caa',
    'hand': 'ed12ceeb807081b63cd13b0580f3c734d1c04e7bbf8dc9525b1af8281c2e6ce0',
}


def checked_font(path, digest):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
    return TTFont(path, recalcTimestamp=False)


def chinese(cp):
    return (0x2E80 <= cp <= 0x9FFF or 0xF900 <= cp <= 0xFAFF or
            0xFF01 <= cp <= 0xFF60)


def scale_width(font, factor):
    glyphset = font.getGlyphSet()
    replacements = {}
    for name in font.getGlyphOrder():
        recording = DecomposingRecordingPen(glyphset)
        glyphset[name].draw(recording)
        pen = TTGlyphPen(None)
        recording.replay(TransformPen(pen, Transform(factor, 0, 0, 1, 0, 0)))
        replacements[name] = pen.glyph()
        advance, bearing = font['hmtx'][name]
        font['hmtx'][name] = (round(advance * factor), round(bearing * factor))
    font['glyf'].glyphs.update(replacements)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_dir', type=Path)
    parser.add_argument('base_dir', type=Path)
    parser.add_argument('--role', choices=ROLES, help='Rebuild only the demonstrated problem role')
    parser.add_argument('--language', choices=('ChineseSimplified', 'ChineseTraditional'), default='ChineseSimplified')
    args = parser.parse_args()
    source_dir, base_dir = args.source_dir, args.base_dir
    required = set()
    # The shipped Chinese-only master is authoritative; reconstructed CSVs are
    # developer fixtures and need not be present when extending a font subset.
    manifest = json.loads((ROOT.parent / 'distribution/payload.json').read_text(encoding='utf-8'))
    column = 1 if args.language == 'ChineseSimplified' else 2
    for table in manifest['tables']:
        for row in table['rows']:
            required.update(map(ord, row[column]))
    # A wording edit must not remove glyphs already available to players.
    existing_dir = ROOT / 'ChineseTraditional' if args.language == 'ChineseTraditional' else ROOT
    for existing in existing_dir.glob('cwr_*.ttf'):
        with TTFont(existing) as font:
            required.update(cp for cp in font.getBestCmap()
                            if 0x3400 <= cp <= 0x9FFF or 0xF900 <= cp <= 0xFAFF)
    for path in ROOT.parent.rglob('*.csv'):
        with path.open(encoding='utf-8-sig', newline='') as stream:
            rows = csv.reader(stream)
            header = next(rows, [])
            if args.language not in header:
                continue
            column = header.index(args.language)
            for row in rows:
                if len(row) > column:
                    required.update(map(ord, row[column]))
    required -= {10, 13}
    if args.language == 'ChineseTraditional':
        required.update(map(ord, '简体中文繁體中文'))
    # Common Simplified Chinese, not just the original 742-character sample.
    common = set()
    for lead in range(0xA1, 0xF8) if args.language == 'ChineseSimplified' else ():
        for trail in range(0xA1, 0xFF):
            try:
                common.update(map(ord, bytes((lead, trail)).decode('gb2312')))
            except UnicodeDecodeError:
                pass
    common |= required | set(range(0x3000, 0x3040)) | set(range(0xFF01, 0xFF61))
    for role, (source, weight, width) in ROLES.items():
        if args.role and role != args.role:
            continue
        base = checked_font(base_dir / f'cwr_{role}.ttf', BASE_HASHES[role])
        if 'fvar' in base:
            base = instantiateVariableFont(base, {a.axisTag: a.defaultValue
                                                   for a in base['fvar'].axes}, inplace=True)
        # Chinese already compensates for the title role's .628 width scale.
        # Do the same for Oswald in this Chinese-only asset: preserve its face,
        # weight, vertical proportions and baseline, without the extra squeeze.
        if role == 'title':
            scale_width(base, 1 / width)
        hashes = SOURCES
        if args.language == 'ChineseTraditional':
            source = 'Iansui-Regular.ttf' if role == 'hand' else 'NotoSerifTC.ttf' if role == 'serif' else 'NotoSansTC.ttf'
            if role == 'hand':
                weight = 400  # Iansui has a single Regular face, not a variable Medium.
            hashes = TRADITIONAL_SOURCES
        cjk = checked_font(source_dir / source, hashes[source])
        if 'fvar' in cjk:
            cjk = instantiateVariableFont(cjk, {'wght': weight}, inplace=True)
        base_cmap = base.getBestCmap().copy()
        # CJK punctuation uses the CJK face; original non-CJK glyphs survive.
        for table in base['cmap'].tables:
            if table.isUnicode():
                table.cmap = {cp: name for cp, name in table.cmap.items() if not chinese(cp)}
        original = set(base.getBestCmap())
        selected = (common & set(cjk.getBestCmap())) - original
        options = subset.Options()
        options.layout_features = []
        options.name_IDs = ['*']
        options.name_languages = ['*']
        sub = subset.Subsetter(options=options)
        sub.populate(unicodes=selected)
        sub.subset(cjk)
        for tag in ('BASE', 'GDEF', 'GPOS', 'GSUB', 'vhea', 'vmtx', 'VORG', 'STAT'):
            if tag in cjk:
                del cjk[tag]
        scale_upem(cjk, base['head'].unitsPerEm)
        # Decompose before transforming to avoid double-scaling components.
        if width != 1:
            scale_width(cjk, 1 / width)
        copyrights = '\n'.join((base['name'].getDebugName(0), cjk['name'].getDebugName(0)))
        with tempfile.TemporaryDirectory() as temp:
            paths = [Path(temp) / 'base.ttf', Path(temp) / 'cjk.ttf']
            base.save(paths[0])
            cjk.save(paths[1])
            # Iansui lacks the authored bird-name character 鷚. Supply only
            # genuinely required missing CJK glyphs from the already used TC sans.
            missing = {cp for cp in required - set(cjk.getBestCmap()) - original if chinese(cp)}
            if missing and args.language == 'ChineseTraditional' and role == 'hand':
                fallback = checked_font(source_dir / 'NotoSansTC.ttf', hashes['NotoSansTC.ttf'])
                fallback = instantiateVariableFont(fallback, {'wght': 500}, inplace=True)
                extra = subset.Subsetter(options=options)
                extra.populate(unicodes=missing)
                extra.subset(fallback)
                for tag in ('BASE', 'GDEF', 'GPOS', 'GSUB', 'vhea', 'vmtx', 'VORG', 'STAT'):
                    if tag in fallback:
                        del fallback[tag]
                scale_upem(fallback, base['head'].unitsPerEm)
                scale_width(fallback, 1 / width)
                fallback_path = Path(temp) / 'fallback.ttf'
                fallback.save(fallback_path)
                paths.append(fallback_path)
                copyrights += '\n' + fallback['name'].getDebugName(0)
            if args.language == 'ChineseTraditional' and ord('简') in missing:
                # The picker displays the Simplified autonym verbatim. Reuse
                # its already tuned glyph, without changing the SC asset.
                picker = TTFont(ROOT / f'cwr_{role}.ttf', recalcTimestamp=False)
                extra = subset.Subsetter(options=options)
                extra.populate(unicodes={ord('简')})
                extra.subset(picker)
                for tag in ('BASE', 'GDEF', 'GPOS', 'GSUB', 'vhea', 'vmtx', 'VORG', 'STAT'):
                    if tag in picker:
                        del picker[tag]
                picker_path = Path(temp) / 'picker.ttf'
                picker.save(picker_path)
                paths.append(picker_path)
                copyrights += '\n' + picker['name'].getDebugName(0)
            merged = Merger().merge([str(p) for p in paths])
        # Keep the original Latin baseline/line metrics, not the merger's maxima.
        for attr in ('ascent', 'descent', 'lineGap'):
            setattr(merged['hhea'], attr, getattr(base['hhea'], attr))
        for attr in ('sTypoAscender', 'sTypoDescender', 'sTypoLineGap',
                     'usWinAscent', 'usWinDescent', 'sxHeight', 'sCapHeight'):
            if hasattr(base['OS/2'], attr):
                setattr(merged['OS/2'], attr, getattr(base['OS/2'], attr))
        merged['head'].created = base['head'].created
        merged['head'].modified = base['head'].modified
        merged.recalcTimestamp = False
        family = f'CWR {"ZhTW" if args.language == "ChineseTraditional" else "ZhCN"} {role.title()}'
        merged['name'].names = []
        names = {0: copyrights, 1: family, 2: 'Regular', 3: family + ' 1.0',
                 4: family, 5: 'Version 1.0', 6: family.replace(' ', ''),
                 13: 'Licensed under the SIL Open Font License, Version 1.1.',
                 14: 'https://openfontlicense.org/', 16: family, 17: 'Regular'}
        for identifier, value in names.items():
            merged['name'].setName(value, identifier, 3, 1, 0x409)
        cmap = merged.getBestCmap()
        assert not (required - set(cmap)), (role, 'missing text characters', sorted(required - set(cmap)))
        assert not ({cp for cp in common if 0x4E00 <= cp <= 0x9FFF} - set(cmap))
        for cp, glyph in base_cmap.items():
            if not chinese(cp):
                assert merged['hmtx'][cmap[cp]] == base['hmtx'][glyph], (role, cp)
        output_dir = ROOT / 'ChineseTraditional' if args.language == 'ChineseTraditional' else ROOT
        output_dir.mkdir(exist_ok=True)
        output = output_dir / f'cwr_{role}.ttf'
        merged.save(output)
        print(f'{output.name}: {len(cmap)} codepoints; CJK weight {weight}, x {1/width:.6f}')


if __name__ == '__main__':
    main()

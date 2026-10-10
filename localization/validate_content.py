"""Validate reconstructed tables and font coverage without modifying a game install."""
import collections
import csv
import html
import io
import re

from fontTools.ttLib import TTFont
from stock import HEADER


def placeholders(value):
    return collections.Counter(re.findall(r'%(?:\d+(?:\.\d+)?|\.\d+[a-zA-Z]|[a-zA-Z])', value))


def anchors(value):
    return collections.Counter(re.findall(r'(?:href|name)\s*=\s*[\"\']([^\"\']+)[\"\']', value, re.I))


def text_references(value):
    return collections.Counter(re.findall(r'\$STR\w+', value, re.I))


def validate(patch, manifest):
    chars = [set(map(ord, '简体中文')), set(map(ord, '简体中文繁體中文'))]
    count = 0
    for table in manifest['tables']:
        rows = list(csv.reader(io.StringIO((patch / table['path']).read_text(encoding='utf-8')), strict=True))
        header = rows[0]
        assert header[:11] == HEADER, table['path']
        assert len({row[0] for row in rows[1:]}) == len(rows) - 1, table['path']
        for row in rows[1:]:
            assert len(row) == len(header), (table['path'], row[0])
            sc, tc = row[9:11]
            assert bool(sc) == bool(tc) and '\ufffd' not in sc + tc, (table['path'], row[0])
            for check in (placeholders, anchors, text_references):
                assert check(sc) == check(tc), (table['path'], row[0], check.__name__)
            assert re.findall(r'</?[A-Za-z][^>]*>', sc) == re.findall(r'</?[A-Za-z][^>]*>', tc), (table['path'], row[0], 'HTML')
            for token in ('\\n', '\\r', '\n', '\r'):
                assert sc.count(token) == tc.count(token), (table['path'], row[0], 'breaks')
            if row[0] == 'STR_CWRC_IDENTITY_VIKTOR_CANONICAL':
                assert sc == tc == row[1] == 'Victor Troska'
            for index, value in enumerate((sc, tc)):
                chars[index].update(map(ord, html.unescape(value)))
            count += 1
    for index, folder in enumerate(('font', 'font/ChineseTraditional')):
        for role in ('title', 'body', 'mono', 'serif', 'hand'):
            with TTFont(patch / folder / f'cwr_{role}.ttf') as font:
                missing = chars[index] - set(font.getBestCmap()) - {9, 10, 13}
                assert not missing, (folder, role, 'missing glyphs', sorted(missing))
    print(f'PASS: {count} SC/TC rows; protected syntax, canonical identity and ten-font coverage')

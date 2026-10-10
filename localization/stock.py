"""Stock CSV and add-on readers shared by reconstruction and tests."""
import csv
import io
import struct

LANGUAGES = ['English', 'French', 'Italian', 'Spanish', 'German', 'Czech', 'Polish', 'Russian']
HEADER = ['LANGUAGE'] + LANGUAGES + ['ChineseSimplified', 'ChineseTraditional']


def stock_csv_rows(text, strict=False):
    # Stock tables have spaces before opening quotes. CsvReadCell skips those
    # spaces before deciding whether a field is quoted; commas inside stay data.
    return list(csv.reader(io.StringIO(text), skipinitialspace=True, strict=strict))


def stock_columns(data, utf8=True):
    """Stock language cells using CsvReadCell whitespace and legacy French rules."""
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


def addon_globals(game, with_rows=False, names=None):
    """Read only stock add-on CSV members, including their other language columns."""
    values = {}
    for name in sorted(names if names is not None else (p.name for p in (game / 'AddOns').glob('*.pbo'))):
        data = (game / 'AddOns' / name).read_bytes()
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

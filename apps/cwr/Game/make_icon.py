"""Rebuild the original, neutral open-book icon (no game artwork)."""
import struct
from pathlib import Path


def bitmap(size):
    pixels = bytearray()
    for y in reversed(range(size)):
        for x in range(size):
            u, v = (x + .5) / size, (y + .5) / size
            color = (0, 0, 0, 0)
            if .10 <= u < .90 and .15 <= v < .85:
                color = (64, 85, 103, 255)
            if (.16 <= u < .47 or .53 <= u < .84) and .21 <= v < .77:
                color = (242, 238, 221, 255)
            if (.21 <= u < .42 or .58 <= u < .79) and any(a <= v < a + .045 for a in (.34, .47, .60)):
                color = (116, 144, 157, 255)
            r, g, b, a = color
            pixels.extend((b, g, r, a))
    mask = bytearray()
    for y in reversed(range(size)):
        row = bytearray(((size + 31) // 32) * 4)
        for x in range(size):
            if not (.10 <= (x + .5) / size < .90 and .15 <= (y + .5) / size < .85):
                row[x // 8] |= 128 >> (x % 8)
        mask.extend(row)
    return struct.pack('<IIIHHIIIIII', 40, size, size * 2, 1, 32, 0, len(pixels), 0, 0, 0, 0) + pixels + mask


if __name__ == '__main__':
    sizes = (16, 32, 48, 256)
    images = [bitmap(size) for size in sizes]
    offset = 6 + 16 * len(sizes)
    directory = bytearray(struct.pack('<HHH', 0, 1, len(sizes)))
    for size, data in zip(sizes, images):
        directory.extend(struct.pack('<BBBBHHII', size % 256, size % 256, 0, 0, 1, 32, len(data), offset))
        offset += len(data)
    Path(__file__).with_name('localization.ico').write_bytes(directory + b''.join(images))

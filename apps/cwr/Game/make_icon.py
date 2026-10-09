"""Rebuild our original gold star icon (no game artwork)."""
import math
import struct
from pathlib import Path


def star(radius):
    return [(.5 + (radius if i % 2 == 0 else radius * .44) * math.cos(-math.pi/2 + i*math.pi/5),
             .52 + (radius if i % 2 == 0 else radius * .44) * math.sin(-math.pi/2 + i*math.pi/5))
            for i in range(10)]


def inside(x, y, polygon):
    result = False
    for i, (ax, ay) in enumerate(polygon):
        bx, by = polygon[i - 1]
        if (ay > y) != (by > y) and x < (bx-ax)*(y-ay)/(by-ay)+ax:
            result = not result
    return result


def bitmap(size):
    pixels = bytearray()
    alpha = []
    outline, fill = star(.48), star(.435)
    for y in reversed(range(size)):
        for x in range(size):
            samples = []
            for sy in range(4):
                for sx in range(4):
                    u, v = (x + (sx+.5)/4)/size, (y + (sy+.5)/4)/size
                    if inside(u, v, outline):
                        # Warm gold, restrained edge, transparent silhouette.
                        samples.append((255-int(28*v), 239-int(82*v), 132-int(108*v))
                                       if inside(u, v, fill) else (129, 79, 12))
            a = round(255 * len(samples)/16)
            r, g, b = (tuple(round(sum(c[i] for c in samples)/len(samples)) for i in range(3))
                       if samples else (0, 0, 0))
            alpha.append(a)
            pixels.extend((b, g, r, a))
    mask = bytearray()
    for y in range(size):
        row = bytearray(((size + 31) // 32) * 4)
        for x in range(size):
            if alpha[y*size+x] == 0:
                row[x // 8] |= 128 >> (x % 8)
        mask.extend(row)
    return struct.pack('<IIIHHIIIIII', 40, size, size * 2, 1, 32, 0, len(pixels), 0, 0, 0, 0) + pixels + mask


if __name__ == '__main__':
    sizes = (16, 24, 32, 48, 256)
    images = [bitmap(size) for size in sizes]
    offset = 6 + 16 * len(sizes)
    directory = bytearray(struct.pack('<HHH', 0, 1, len(sizes)))
    for size, data in zip(sizes, images):
        directory.extend(struct.pack('<BBBBHHII', size % 256, size % 256, 0, 0, 1, 32, len(data), offset))
        offset += len(data)
    Path(__file__).with_name('localization.ico').write_bytes(directory + b''.join(images))

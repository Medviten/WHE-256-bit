"""Repaint the hands of the female Vrykul PC skin textures (VrykulFemaleSkin00_NN.blp).

These textures keep the hands in the strip below the arms (left half, v 0.5 to 0.625, where the model's hand UVs are),
but the female set has only a smeared, blocky strip there with a hard ragged edge, which shows as a dark crease across
the back of the hand. This replaces that strip, and the ragged last rows of the forearm band above it, with clean skin
copied from just above, in every mip level, so each skin colour keeps its own tone. The hands lose their (poor)
painted detail and become plain skin.

Raw BGRA (compression 3) BLPs only. usage: python -I vrykul_female_hands.py <skin.blp>...   (in place)"""
import struct
import sys

DEST = (244, 320)   # rows of the 512-high top mip to replace: the forearm's ragged bottom and the hand strip
SOURCE = 168        # first row of the clean skin copied there (the same height)
FADE = 12           # rows over which the copy fades in from the row above the strip


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for path in sys.argv[1:]:
        with open(path, 'rb') as f:
            data = bytearray(f.read())
        if data[:4] != b'BLP2' or data[8] != 3:
            print('%s: not a raw BGRA BLP, skipped' % path)
            continue
        width, height = struct.unpack_from('<II', data, 12)
        if (width, height) != (512, 512):
            print('%s: expected 512x512, skipped' % path)
            continue
        offsets = struct.unpack_from('<16I', data, 20)
        sizes = struct.unpack_from('<16I', data, 84)
        mips = 0
        for level in range(16):
            if not offsets[level] or not sizes[level]:
                break
            w, h = max(1, width >> level), max(1, height >> level)
            top, bottom, source = DEST[0] >> level, DEST[1] >> level, SOURCE >> level
            span = 4 * (w // 2)   # left half
            above = offsets[level] + 4 * w * max(top - 1, 0)
            edge = bytes(data[above:above + span])
            fade = max(1, FADE >> level)
            for row in range(bottom - top):
                dst = offsets[level] + 4 * w * (top + row)
                src = offsets[level] + 4 * w * min(source + row, h - 1)
                if row < fade:   # fade in from the row above, so the join leaves no line
                    f = (row + 1) / (fade + 1)
                    data[dst:dst + span] = bytes(int(round(a + (b - a) * f)) for a, b in zip(edge, data[src:src + span]))
                else:
                    data[dst:dst + span] = data[src:src + span]
            mips += 1
        with open(path, 'wb') as f:
            f.write(data)
        print('%s: hand strip repainted in %d mip levels' % (path, mips))


if __name__ == '__main__':
    main()

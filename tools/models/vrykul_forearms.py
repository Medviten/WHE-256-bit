"""Slim the forearms of the female Vrykul PC model, which bulge below the elbow: in the stand pose the upper forearm is
about 0.20 wide where the end of the upper arm is 0.15-0.17, so the lower arm looks wider than the arm it hangs from.

Every arm vertex near a forearm's line (from the elbow to the wrist bone pivot, a little past the elbow so the joint
blends) is pulled towards that line: by SLIM through the upper forearm, easing in from just above the elbow and out
towards the wrist, so the arm still meets the upper arm and the hand. The amount is decided per position, so vertices of
different geosets in the same place (bare arm, gloves, sleeves) move together and their seams stay closed.

usage: python -I vrykul_forearms.py <VrykulPCFemale.m2> [slim]   (in place; default slim 0.2)"""
import math
import struct
import sys

VERTEX_SIZE = 48
ARMS = ((17, 23, 27), (19, 25, 28))   # (upper arm, forearm, wrist) bones per side; the forearm's line runs between the
                                      # forearm and wrist bone pivots
REACH = 0.2                           # how far from the forearm's line a vertex may be
WELD = 1e-4


def smoothstep(a, b, x):
    x = min(1.0, max(0.0, (x - a) / (b - a)))
    return x * x * (3 - 2 * x)


def amount(t):
    """How much of SLIM applies at t along the forearm (0 elbow, 1 wrist)."""
    return smoothstep(-0.1, 0.1, t) * (1 - smoothstep(0.35, 0.8, t))


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    model = sys.argv[1]
    slim = float(sys.argv[2]) if len(sys.argv) == 3 else 0.2
    with open(model, 'rb') as f:
        data = bytearray(f.read())
    nbones, obones = struct.unpack_from('<II', data, 0x2C)
    nvert, overt = struct.unpack_from('<II', data, 0x3C)
    pivot = lambda b: struct.unpack_from('<3f', data, obones + 88 * b + 76)
    parent = lambda b: struct.unpack_from('<h', data, obones + 88 * b + 8)[0]

    def under(bone, ancestor):
        while bone != -1:
            if bone == ancestor:
                return True
            bone = parent(bone)
        return False

    # vertices count as one position when within WELD of each other (rounding alone splits some of those)
    cell = lambda p: tuple(int(math.floor(c / WELD)) for c in p)
    positions = [struct.unpack_from('<3f', data, overt + VERTEX_SIZE * i) for i in range(nvert)]
    grid = {}
    for i, p in enumerate(positions):
        grid.setdefault(cell(p), []).append(i)

    def same_place(p):
        c = cell(p)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for j in grid.get((c[0] + dx, c[1] + dy, c[2] + dz), ()):
                        if math.dist(p, positions[j]) < WELD:
                            yield j

    factor = {}
    for i, p in enumerate(positions):
        o = overt + VERTEX_SIZE * i
        weights, bones = data[o + 12:o + 16], data[o + 16:o + 20]
        dominant = bones[weights.index(max(weights))]
        for upper, forearm, wrist in ARMS:
            if not under(dominant, upper):
                continue
            a, b = pivot(forearm), pivot(wrist)
            axis = [b[j] - a[j] for j in range(3)]
            t = sum((p[j] - a[j]) * axis[j] for j in range(3)) / sum(x * x for x in axis)
            w = amount(t)
            if w <= 0 or t >= 1:
                continue
            q = [a[j] + axis[j] * t for j in range(3)]
            if math.dist(p, q) > REACH:
                continue
            for j in same_place(p):
                factor.setdefault(j, (1 - slim * w, q))

    for i, (s, q) in factor.items():
        p = positions[i]
        struct.pack_into('<3f', data, overt + VERTEX_SIZE * i, *(q[j] + (p[j] - q[j]) * s for j in range(3)))

    with open(model, 'wb') as f:
        f.write(data)
    print('%s: %d vertices slimmed (up to %d%%)' % (model, len(factor), round(slim * 100)))


if __name__ == '__main__':
    main()

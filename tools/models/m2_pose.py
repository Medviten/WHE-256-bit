"""Pose a 3.3.5 (version 264) model at the first frame of its stand animation: bone matrices, skinned positions and
the way back (posed position -> bind position through a vertex's blended bone transform). Shared by the model tools.

Bone matrix = parent * translate(pivot) * translate(t) * rotate(q) * scale(s) * translate(-pivot), with t, q, s the
first keys of the stand sequence (or of the track's global sequence)."""
import math
import struct

VERTEX_SIZE, BONE_SIZE = 48, 88


def _quat(v):
    return [(c + 32768 if c < 0 else c - 32767) / 32767.0 for c in v]


def _mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def _translate(t):
    return [[1, 0, 0, t[0]], [0, 1, 0, t[1]], [0, 0, 1, t[2]], [0, 0, 0, 1]]


def _rotate(q):
    x, y, z, w = q
    n = math.sqrt(x * x + y * y + z * z + w * w) or 1
    x, y, z, w = x / n, y / n, z / n, w / n
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w), 0],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w), 0],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y), 0], [0, 0, 0, 1]]


def _scale(s):
    return [[s[0], 0, 0, 0], [0, s[1], 0, 0], [0, 0, s[2], 0], [0, 0, 0, 1]]


def stand_matrices(data):
    """One 4x4 matrix per bone, at frame 0 of the stand animation."""
    nseq, oseq = struct.unpack_from('<II', data, 0x1C)
    stand = next(i for i in range(nseq) if struct.unpack_from('<HH', data, oseq + 64 * i) == (0, 0))
    nbones, obones = struct.unpack_from('<II', data, 0x2C)

    def first_key(track, size, fmt):
        interp, loop, ntimes, otimes, nkeys, okeys = struct.unpack_from('<hhIIII', data, track)
        s = 0 if loop >= 0 else stand
        if s >= nkeys:
            return None
        count, offset = struct.unpack_from('<II', data, okeys + 8 * s)
        if not count or offset + size > len(data):
            return None
        return struct.unpack_from(fmt, data, offset)

    mats = []
    for b in range(nbones):
        o = obones + BONE_SIZE * b
        parent = struct.unpack_from('<h', data, o + 8)[0]
        pivot = struct.unpack_from('<3f', data, o + 76)
        t = first_key(o + 0x10, 12, '<3f') or (0, 0, 0)
        r = first_key(o + 0x24, 8, '<4h')
        r = _quat(r) if r else (0, 0, 0, 1)
        s = first_key(o + 0x38, 12, '<3f') or (1, 1, 1)
        m = _mul(_translate(pivot), _mul(_translate(t), _mul(_rotate(r), _mul(_scale(s), _translate([-c for c in pivot])))))
        mats.append(_mul(mats[parent], m) if parent >= 0 else m)
    return mats


def blended(mats, weights, bones):
    """The 3x4 transform a vertex with these weights (0-255) and bones gets."""
    m = [[0.0] * 4 for _ in range(3)]
    for w, b in zip(weights, bones):
        if w:
            for i in range(3):
                for j in range(4):
                    m[i][j] += mats[b][i][j] * w / 255.0
    return m


def apply(m, p):
    return [m[i][0] * p[0] + m[i][1] * p[1] + m[i][2] * p[2] + m[i][3] for i in range(3)]


def unapply(m, q):
    """The point p with apply(m, p) == q."""
    a = [row[:3] for row in m]
    det = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
           + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    inv = [[(a[1][1] * a[2][2] - a[1][2] * a[2][1]) / det, (a[0][2] * a[2][1] - a[0][1] * a[2][2]) / det,
            (a[0][1] * a[1][2] - a[0][2] * a[1][1]) / det],
           [(a[1][2] * a[2][0] - a[1][0] * a[2][2]) / det, (a[0][0] * a[2][2] - a[0][2] * a[2][0]) / det,
            (a[0][2] * a[1][0] - a[0][0] * a[1][2]) / det],
           [(a[1][0] * a[2][1] - a[1][1] * a[2][0]) / det, (a[0][1] * a[2][0] - a[0][0] * a[2][1]) / det,
            (a[0][0] * a[1][1] - a[0][1] * a[1][0]) / det]]
    d = [q[i] - m[i][3] for i in range(3)]
    return [sum(inv[i][j] * d[j] for j in range(3)) for i in range(3)]


def vertex_skin(data, v):
    """(weights, bones) of model vertex v."""
    o = struct.unpack_from('<I', data, 0x40)[0] + VERTEX_SIZE * v
    return list(data[o + 12:o + 16]), list(data[o + 16:o + 20])

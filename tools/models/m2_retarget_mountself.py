#!/usr/bin/env python3
"""Add the MountSelf animations (618-650, Running Wild's) of one 3.3.5 Worgen model to another with a different rig.

Used for F-094: the alpha Worgen models have none, and their skeletons differ from the current models' (other bone
counts and hierarchy; the main joints sit in the same places). M2 rotations are deltas from the bind pose, so a pose
carries over as each bone's global rotation:

- bones are matched by comparing global rotations over the animations both models have (Stand, Walk, Run, ...), among
  source bones near the target bone. Target bones that never move there take a close source bone with the same parent
- each new sequence is sampled every 33 ms: a mapped bone's local rotation is the source bone's global rotation undone
  by its target parent's, and its translation puts its pivot where the source's is (hierarchies differ, so a source
  parent's translation can't be left to the target's parents)
- bones left unmapped keep the client's fallback for a sequence past their track's list, entry 0 (Stand)
- new sequences are stored in the model (flag 0x20), even when the source keeps them in .anim files. Events of the same
  sequences are copied too (a Worgen model's $CSD event plays MountSelfSpecial's sound, see F-063)

`check` retargets Run the same way and prints how far that lands from the target's own Run, without writing anything.

usage: python -I m2_retarget_mountself.py <source.m2> <target.m2> [check]   (target is changed in place, once)"""
import bisect
import math
import os
import struct
import sys

SEQ_SIZE, BONE_SIZE, EVENT_SIZE = 64, 88, 36
HAS_DATA, ALIAS = 0x20, 0x40
TRACK_OFFSETS = {'trans': 0x10, 'rot': 0x24, 'scale': 0x38}
MOUNT_SELF = range(618, 651)
SHARED = (0, 4, 5, 11, 12, 13)           # Stand, Walk, Run, ShuffleLeft, ShuffleRight, Walkbackwards
STEP = 33
NONE16 = 0xFFFF
MAX_SCORE = 25.0                         # degrees of global rotation for a match
NEAR = 0.2                               # distance between pivots of a match
CLOSE = 0.03                             # the same, for target bones that never move in SHARED


def qmul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by, aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw, aw * bw - ax * bx - ay * by - az * bz)


def qconj(q):
    return (-q[0], -q[1], -q[2], q[3])


def qrot(q, v):
    x, y, z, w = q
    tx, ty, tz = 2 * (y * v[2] - z * v[1]), 2 * (z * v[0] - x * v[2]), 2 * (x * v[1] - y * v[0])
    return (v[0] + w * tx + y * tz - z * ty, v[1] + w * ty + z * tx - x * tz, v[2] + w * tz + x * ty - y * tx)


def qnorm(q):
    n = math.sqrt(sum(c * c for c in q)) or 1.0
    return tuple(c / n for c in q)


def qangle(a, b):
    d = min(1.0, abs(sum(x * y for x, y in zip(a, b))))
    return math.degrees(2 * math.acos(d))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


IDENTITY, ZERO = (0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0)


class Model:
    def __init__(self, path):
        self.path = path
        self.data = open(path, 'rb').read()
        self.base = os.path.splitext(path)[0]
        d = self.data
        n, o = struct.unpack_from('<II', d, 0x1C)
        self.seqs = []
        for i in range(n):
            sid, var, dur = struct.unpack_from('<HHI', d, o + i * SEQ_SIZE)
            flags = struct.unpack_from('<I', d, o + i * SEQ_SIZE + 12)[0]
            alias = struct.unpack_from('<H', d, o + i * SEQ_SIZE + 62)[0]
            self.seqs.append(dict(index=i, id=sid, var=var, dur=dur, flags=flags, alias=alias, raw=d[o + i * SEQ_SIZE:o + (i + 1) * SEQ_SIZE]))
        n, o = struct.unpack_from('<II', d, 0x2C)
        self.bones = []
        for i in range(n):
            b = o + i * BONE_SIZE
            key, flags, parent = struct.unpack_from('<iIh', d, b)
            self.bones.append(dict(index=i, key=key, flags=flags, parent=parent, pos=b, pivot=struct.unpack_from('<3f', d, b + 76)))
            assert parent < i, 'bones must come after their parents'
        self.anims = {}
        self.cache = {}

    def find(self, sid):
        return next((s for s in self.seqs if s['id'] == sid and s['var'] == 0), None)

    def source_of(self, seq):
        """The sequence holding this one's data: aliases point along aliasNext to it."""
        seen = set()
        while seq['flags'] & ALIAS and seq['index'] not in seen:
            seen.add(seq['index'])
            seq = self.seqs[seq['alias']]
        return seq

    def buffer(self, seq):
        if seq['flags'] & HAS_DATA:
            return self.data
        if seq['index'] not in self.anims:
            name = '%s%04d-%02d.anim' % (self.base, seq['id'], seq['var'])
            self.anims[seq['index']] = open(name, 'rb').read()
        return self.anims[seq['index']]

    def track(self, pos, seq, fmt, size):
        """Times and values of a track for a sequence, the way the client picks them (entry 0 past the list's end)."""
        d = self.data
        interp, loop, tn, to, kn, ko = struct.unpack_from('<HHIIII', d, pos)
        if not tn or loop != NONE16:
            return [], []
        src = self.source_of(seq)
        index = src['index'] if src['index'] < tn else 0
        buf = self.buffer(self.seqs[index]) if index else self.buffer(src if src['index'] == 0 else self.seqs[0])
        cn, co = struct.unpack_from('<II', d, to + index * 8)
        vn, vo = struct.unpack_from('<II', d, ko + index * 8)
        if not cn or not vn:
            return [], []
        times = list(struct.unpack_from('<%dI' % cn, buf, co))
        values = [struct.unpack_from(fmt, buf, vo + i * size) for i in range(vn)]
        return times, values

    def bone_tracks(self, seq):
        key = seq['index']
        if key not in self.cache:
            rows = []
            for b in self.bones:
                t, r = self.track(b['pos'] + TRACK_OFFSETS['rot'], seq, '<4H', 8)
                r = [tuple(c * 0.000030518044 - 1.0 for c in v) for v in r]
                rows.append((self.track(b['pos'] + TRACK_OFFSETS['trans'], seq, '<3f', 12), (t, r)))
            self.cache[key] = rows
        return self.cache[key]

    def local(self, seq, bone, time):
        trans, rot = self.bone_tracks(seq)[bone]
        return sample(rot, time, True) or IDENTITY, sample(trans, time, False) or ZERO

    def pose(self, seq, time):
        """Global rotation and pivot position of each bone."""
        rots, poss = [], []
        for b in self.bones:
            q, t = self.local(seq, b['index'], time)
            p = b['pivot']
            if b['parent'] < 0:
                rots.append(qnorm(q))
                poss.append(add(p, t))
            else:
                par = self.bones[b['parent']]
                qp, pp = rots[b['parent']], poss[b['parent']]
                rots.append(qnorm(qmul(qp, q)))
                poss.append(add(pp, qrot(qp, sub(add(p, t), par['pivot']))))
        return rots, poss


def sample(track, time, is_quat):
    times, values = track
    if not times:
        return None
    if time <= times[0] or len(times) == 1:
        return values[0]
    if time >= times[-1]:
        return values[-1]
    i = bisect.bisect_right(times, time) - 1
    t0, t1 = times[i], times[i + 1]
    r = (time - t0) / (t1 - t0) if t1 > t0 else 0.0
    a, b = values[i], values[i + 1]
    if is_quat and sum(x * y for x, y in zip(a, b)) < 0:
        b = tuple(-c for c in b)
    v = tuple(x + (y - x) * r for x, y in zip(a, b))
    return qnorm(v) if is_quat else v


def movers(model, seqs):
    out = set()
    for seq in seqs:
        for i, (_, (t, r)) in enumerate(model.bone_tracks(seq)):
            if len(r) > 1 and any(qangle(r[0], v) > 0.5 for v in r):
                out.add(i)
    return out


def match(src, tgt):
    """{target bone: source bone}"""
    pairs = [(src.find(i), tgt.find(i)) for i in SHARED]
    pairs = [(a, b) for a, b in pairs if a and b]
    samples = []
    for a, b in pairs:
        for k in range(6):
            samples.append((src.pose(a, a['dur'] * k // 6)[0], tgt.pose(b, b['dur'] * k // 6)[0]))
    moved = movers(tgt, [b for _, b in pairs])
    src_moved = movers(src, [a for a, _ in pairs])
    by_key = {b['key']: b['index'] for b in src.bones if b['key'] >= 0}
    mapping, poor = {}, []
    for t in tgt.bones:
        i = t['index']
        if i not in moved:
            continue
        options = [s['index'] for s in src.bones if s['index'] in src_moved and dist(s['pivot'], t['pivot']) < NEAR]
        if t['key'] in by_key and by_key[t['key']] not in options:
            options.append(by_key[t['key']])
        best = None
        for s in options:
            score = sum(qangle(gs[s], gt[i]) for gs, gt in samples) / len(samples)
            score += dist(src.bones[s]['pivot'], t['pivot']) * 20    # 1 degree per 5 cm, to settle ties
            if best is None or score < best[0]:
                best = (score, s)
        if best and best[0] < MAX_SCORE:
            mapping[i] = best[1]
        else:
            poor.append((i, t['key'], None if not best else round(best[0], 1)))
    for t in tgt.bones:                 # bones that only move in other animations (jaw, ears, fingers)
        i = t['index']
        if i in mapping or i in moved or t['parent'] < 0 or t['parent'] not in mapping:
            continue
        options = [s for s in src.bones if s['parent'] == mapping[t['parent']] and dist(s['pivot'], t['pivot']) < CLOSE]
        if options:
            mapping[i] = min(options, key=lambda s: dist(s['pivot'], t['pivot']))['index']
    return mapping, poor, moved


def bake(src, tgt, mapping, seq, stand):
    """{target bone: (times, local rotations, local translations or None)} for a source sequence."""
    times = list(range(0, seq['dur'], STEP)) + [seq['dur']]
    out = {i: ([], [], []) for i in mapping}
    for time in times:
        rs, ps = src.pose(seq, time)
        rots, poss = [], []
        for b in tgt.bones:
            i, parent = b['index'], b['parent']
            qp = rots[parent] if parent >= 0 else IDENTITY
            pp = poss[parent] if parent >= 0 else ZERO
            pv = tgt.bones[parent]['pivot'] if parent >= 0 else ZERO
            if i in mapping:
                s = mapping[i]
                q = qnorm(rs[s])
                local = qnorm(qmul(qconj(qp), q))
                want = add(ps[s], sub(b['pivot'], src.bones[s]['pivot']))
                trans = sub(add(qrot(qconj(qp), sub(want, pp)), pv), b['pivot'])
                out[i][0].append(time)
                out[i][1].append(local)
                out[i][2].append(trans)
            else:
                local, trans = tgt.local(stand, i, min(time, stand['dur']))
                q = qnorm(qmul(qp, local))
            rots.append(q)
            poss.append(add(pp, qrot(qp, sub(add(b['pivot'], trans), pv))))
    return out


def fidelity(src, tgt, mapping, new_seqs):
    """How far the baked poses are from the source's own, per mapped bone, in the new sequences."""
    gaps = []
    for seq in new_seqs:
        baked = bake(src, tgt, mapping, seq, tgt.seqs[0])
        first = next(iter(baked))
        count = len(baked[first][0])
        for n in range(0, count, max(1, count // 6)):
            time = baked[first][0][n]
            _, source_pos = src.pose(seq, time)
            rots, poss = [], []
            for bn in tgt.bones:
                i, parent = bn['index'], bn['parent']
                qp = rots[parent] if parent >= 0 else IDENTITY
                pp = poss[parent] if parent >= 0 else ZERO
                pv = tgt.bones[parent]['pivot'] if parent >= 0 else ZERO
                if i in baked:
                    local, trans = baked[i][1][n], baked[i][2][n]
                else:
                    local, trans = tgt.local(tgt.seqs[0], i, time)
                rots.append(qnorm(qmul(qp, local)))
                poss.append(add(pp, qrot(qp, sub(add(bn['pivot'], trans), pv))))
            for t, s in mapping.items():
                bind_gap = dist(tgt.bones[t]['pivot'], src.bones[s]['pivot'])
                gaps.append((dist(poss[t], source_pos[s]) - bind_gap, t, seq['id']))
    gaps.sort()
    n = len(gaps)
    print('  MountSelf vs source (beyond the bind pose gap): position median %.3f, p90 %.3f, worst %.3f (bone %d, anim %d)'
          % (gaps[n // 2][0], gaps[n * 9 // 10][0], gaps[-1][0], gaps[-1][1], gaps[-1][2]))


def check(src, tgt, mapping, moved):
    """Retargets Run and compares it with the target's own: what is left is partly that their Runs differ."""
    a, b = src.find(5), tgt.find(5)
    baked = bake(src, tgt, mapping, a, tgt.seqs[0])
    angles, gaps = [], []
    for k in range(0, 8):
        time = a['dur'] * k // 8
        i_time = min(range(len(baked[next(iter(baked))][0])), key=lambda n: abs(baked[next(iter(baked))][0][n] - time))
        rots, poss = [], []
        for bn in tgt.bones:
            i, parent = bn['index'], bn['parent']
            qp = rots[parent] if parent >= 0 else IDENTITY
            pp = poss[parent] if parent >= 0 else ZERO
            pv = tgt.bones[parent]['pivot'] if parent >= 0 else ZERO
            if i in baked:
                local, trans = baked[i][1][i_time], baked[i][2][i_time]
            else:
                local, trans = tgt.local(tgt.seqs[0], i, time)
            rots.append(qnorm(qmul(qp, local)))
            poss.append(add(pp, qrot(qp, sub(add(bn['pivot'], trans), pv))))
        real_r, real_p = tgt.pose(b, b['dur'] * k // 8)
        for i in moved:
            angles.append(qangle(rots[i], real_r[i]))
            gaps.append(dist(poss[i], real_p[i]))
    angles.sort()
    gaps.sort()
    n = len(angles)
    print('  Run retargeted vs its own: rotation median %.1f, p90 %.1f degrees; position median %.3f, p90 %.3f, worst %.3f'
          % (angles[n // 2], angles[n * 9 // 10], gaps[n // 2], gaps[n * 9 // 10], gaps[-1]))


class Writer:
    def __init__(self, data):
        self.data = bytearray(data)

    def append(self, raw):
        self.data += bytes(-len(self.data) % 16)
        pos = len(self.data)
        self.data += raw
        return pos


def encode(q, last):
    if last and sum(x * y for x, y in zip(q, last)) < 0:
        q = tuple(-c for c in q)
    return q, struct.pack('<4H', *[max(0, min(65535, round((c + 1.0) * 32767.5))) for c in q])


def outer(w, pos, old_seqs, entries):
    """Rewrites the outer list at pos: its old entries (entry 0's for sequences past its end) and the new ones."""
    count, offset = struct.unpack_from('<II', w.data, pos)
    pairs = [struct.unpack_from('<II', w.data, offset + i * 8) for i in range(count)]
    fill = pairs[0] if pairs else (0, 0)
    pairs += [fill] * (old_seqs - len(pairs))
    pairs += entries
    raw = b''.join(struct.pack('<II', *p) for p in pairs)
    struct.pack_into('<II', w.data, pos, len(pairs), w.append(raw))


def events(src, tgt, new_seqs, mapping, w, old_seqs):
    """Copies the events of the new sequences to the target's events of the same id, adding the ids it lacks."""
    sn, so = struct.unpack_from('<II', src.data, 0x100)
    tn, to = struct.unpack_from('<II', tgt.data, 0x100)
    reverse = {}
    for t, s in mapping.items():
        reverse.setdefault(s, t)
    source = [src.data[so + i * EVENT_SIZE:so + (i + 1) * EVENT_SIZE] for i in range(sn)]
    target = [tgt.data[to + i * EVENT_SIZE:to + (i + 1) * EVENT_SIZE] for i in range(tn)]
    ids = {e[:4]: i for i, e in enumerate(target)}
    keys = {}                                                    # target event -> per new sequence: times
    for raw_index, raw in enumerate(source):
        pos = so + raw_index * EVENT_SIZE + 0x18
        for k, seq in enumerate(new_seqs):
            times, _ = src_event_times(src, pos, seq)
            if not times:
                continue
            ident = raw[:4]
            if ident not in ids:
                bone = struct.unpack_from('<H', raw, 8)[0]
                event = bytearray(raw)
                struct.pack_into('<H', event, 8, reverse.get(bone, 0))
                struct.pack_into('<HHII', event, 0x18, 0, NONE16, 0, 0)
                ids[ident] = len(target)
                target.append(bytes(event))
            keys.setdefault(ids[ident], {})[k] = times
    pos = w.append(b''.join(target))
    struct.pack_into('<II', w.data, 0x100, len(target), pos)
    for i in range(len(target)):
        entries = []
        for k in range(len(new_seqs)):
            times = keys.get(i, {}).get(k)
            entries.append((len(times), w.append(struct.pack('<%dI' % len(times), *times))) if times else (0, 0))
        outer(w, pos + i * EVENT_SIZE + 0x18 + 4, old_seqs, entries)
    return len(target) - tn, sum(len(v) for v in keys.values())


def src_event_times(src, pos, seq):
    d = src.data
    interp, loop, count, offset = struct.unpack_from('<HHII', d, pos)
    real = src.source_of(seq)
    if real['index'] >= count:
        return [], None
    n, o = struct.unpack_from('<II', d, offset + real['index'] * 8)
    if not n:
        return [], None
    return list(struct.unpack_from('<%dI' % n, src.buffer(real), o)), None


def write(src, tgt, mapping, new_seqs):
    w = Writer(tgt.data)
    old_seqs = len(tgt.seqs)
    stand = tgt.seqs[0]
    baked = [bake(src, tgt, mapping, s, stand) for s in new_seqs]
    # sequences
    raws = [s['raw'] for s in tgt.seqs]
    for k, s in enumerate(new_seqs):
        raw = bytearray(s['raw'])
        struct.pack_into('<H', raw, 2, 0)
        struct.pack_into('<I', raw, 12, (s['flags'] | HAS_DATA) & ~ALIAS)
        struct.pack_into('<HH', raw, 60, NONE16, old_seqs + k)
        raws.append(bytes(raw))
    struct.pack_into('<II', w.data, 0x1C, len(raws), w.append(b''.join(raws)))
    # the id hash: the client's own probing (M2Model HasSequence)
    hn, ho = struct.unpack_from('<II', w.data, 0x24)
    assert hn and (hn - old_seqs - len(new_seqs)) > 0, 'sequence hash table is full'
    for k, s in enumerate(new_seqs):
        slot, step = s['id'] % hn, 1
        while struct.unpack_from('<H', w.data, ho + slot * 2)[0] != NONE16:
            slot = (slot + step * step) % hn
            step += 1
        struct.pack_into('<H', w.data, ho + slot * 2, old_seqs + k)
    # bones
    for i in sorted(mapping):
        bone = tgt.bones[i]
        rot_entries, trans_entries = [], []
        moved_trans = False
        for bake_k in baked:
            times, rots, trans = bake_k[i]
            t_pos = w.append(struct.pack('<%dI' % len(times), *times))
            last, raw = None, []
            for q in rots:
                last, packed = encode(q, last)
                raw.append(packed)
            rot_entries.append(((len(times), t_pos), (len(rots), w.append(b''.join(raw)))))
            if any(dist(v, ZERO) > 1e-3 for v in trans):
                moved_trans = True
                trans_entries.append(((len(times), t_pos), (len(trans), w.append(b''.join(struct.pack('<3f', *v) for v in trans)))))
            else:
                trans_entries.append(((0, 0), (0, 0)))
        rot = bone['pos'] + TRACK_OFFSETS['rot']
        struct.pack_into('<HH', w.data, rot, 1, NONE16)
        outer(w, rot + 4, old_seqs, [e[0] for e in rot_entries])
        outer(w, rot + 12, old_seqs, [e[1] for e in rot_entries])
        if moved_trans:
            tr = bone['pos'] + TRACK_OFFSETS['trans']
            struct.pack_into('<HH', w.data, tr, 1, NONE16)
            outer(w, tr + 4, old_seqs, [e[0] for e in trans_entries])
            outer(w, tr + 12, old_seqs, [e[1] for e in trans_entries])
        struct.pack_into('<I', w.data, bone['pos'] + 4, bone['flags'] | 0x200)
    added, copied = events(src, tgt, new_seqs, mapping, w, old_seqs)
    with open(tgt.path, 'wb') as fh:
        fh.write(w.data)
    print('  wrote %d sequences (%d event ids added, %d event tracks copied), model %d -> %d bytes'
          % (len(new_seqs), added, copied, len(tgt.data), len(w.data)))


def retarget(source, target, check_only=False):
    src, tgt = Model(source), Model(target)
    if any(s['id'] in MOUNT_SELF for s in tgt.seqs):
        raise SystemExit('%s already has MountSelf sequences' % target)
    new_seqs = sorted((s for s in src.seqs if s['id'] in MOUNT_SELF and s['var'] == 0), key=lambda s: s['id'])
    mapping, poor, moved = match(src, tgt)
    print('%s: %d bones, %d mapped (%d move in the shared animations), %d movers without a match: %s'
          % (os.path.basename(target), len(tgt.bones), len(mapping), len(moved), len(poor), poor[:12]))
    check(src, tgt, mapping, moved & set(mapping))
    fidelity(src, tgt, mapping, new_seqs)
    if not check_only:
        write(src, tgt, mapping, new_seqs)
    return mapping


if __name__ == '__main__':
    retarget(sys.argv[1], sys.argv[2], len(sys.argv) > 3 and sys.argv[3] == 'check')

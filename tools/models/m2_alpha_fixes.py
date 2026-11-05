#!/usr/bin/env python3
"""Fixes to the alpha Worgen and Goblin models (F-094, F-095) that the client's Two Forms and blinks need.

Two Forms (Unit_C.cpp, see BeginAlteredFormTransition) plays ToAltered (486) on the Worgen model while it rides the human
model's attachment 50, then ToAlteredPostSwap (496) on its own once the human model's $ALT event fires. ToAltered relies
on colour tracks: alpha 0 hides the body, and the separate arm meshes fade in. A colour's alpha entry with no keys means
fully visible (M2Model.cpp, M2AnimateTrack's default of one), so every sequence must key what it hides.

- worgen_male: the model's own 486 and 496 come from Blizzard's, but its arm meshes have no keys in 496, so they stay
  visible for its 1.8 seconds, at the feet as nothing carries them any more. They get alpha 0 there. Its 486 also ends
  33 ms before the male Gilnean's $ALT (3166), so it is lengthened; poses and colours hold their last keys
- worgen_female: the model has neither anim, so she stands in Stand on the human's attachment throughout. Both are
  retargeted from F-024's model, as MountSelf is. 486 hides her whole body: every batch gets a colour with alpha 0 there
- port_arms: she also lacks the arm meshes that take over from the human's arms, which leaves its weapons floating. They
  are copied from F-024's model with the bones that carry them: new bones keeping their own hierarchy and 486 tracks, so
  they pose exactly as in that model. They are hidden in every other sequence
- hide_attachments: items on her hidden body would still show, a copy of her weapons floating above the human's head,
  so her attachments are hidden in 486. Items come back at the swap
- goblin: blinks make the eyes vanish. The male's Stand shows a mesh over the eye, mapped to bare skin above the painted
  eye, and the eye glow (geoset 1703: Death Knights and faces with flag 4) has a texture weight that turns it off, in
  both models. There is no closed eye to show, so both are removed and the eyes stay open

usage: python -I m2_alpha_fixes.py <WHE-common patch-A.MPQ>/Character   (models changed in place, once, after MountSelf)"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2_retarget_mountself as R

TO_ALTERED, POST_SWAP = 486, 496
COLOR_SIZE, ALPHA_TRACK, BATCH_SIZE, BATCH_COLOR, VERTEX_SIZE, SUBMESH_SIZE = 40, 0x14, 24, 8, 48, 48
ARM_ALPHA_KEYS = 4                  # a colour keyed in 486 with fade keys: 0, fade start, fade end, end
MALE_TO_ALTERED_LENGTH = 3300       # past the male Gilnean's $ALT at 3166
ATTACHMENT_SIZE, ATTACHMENT_TRACK = 40, 0x14
GLOW_WEIGHT = 1                     # the texture weight of the eye glow in both Goblin models
FULL_ALPHA = 32767


def load(path):
    with open(path, 'rb') as fh:
        return R.Writer(fh.read())


def save(path, w):
    with open(path, 'wb') as fh:
        fh.write(w.data)


def key_entry(w, value):
    """A one key entry at time 0: (times), (values)."""
    return (1, w.append(struct.pack('<I', 0))), (1, w.append(struct.pack('<h', value)))


def pairs(w, entries):
    return w.append(b''.join(struct.pack('<II', *p) for p in entries))


def white_rgb(w):
    """One white RGB key: with no keys the client never evaluates the track and the mesh renders black. The arrays are
    a colour's own: the client relocates each track's offsets, so tracks can't share them."""
    times = w.append(struct.pack('<II', 1, w.append(struct.pack('<I', 0))))
    values = w.append(struct.pack('<II', 1, w.append(struct.pack('<3f', 1.0, 1.0, 1.0))))
    return struct.pack('<HHIIII', 0, R.NONE16, 1, times, 1, values)


def worgen_male(path):
    model = R.Model(path)
    index = model.find(POST_SWAP)['index']
    to_altered = model.find(TO_ALTERED)
    if to_altered['dur'] >= MALE_TO_ALTERED_LENGTH:
        raise SystemExit('%s is already fixed' % path)
    w = R.Writer(model.data)
    count, offset = struct.unpack_from('<II', w.data, 0x48)
    fixed = 0
    for c in range(count):
        pos = offset + c * COLOR_SIZE + ALPHA_TRACK
        tn, to, kn, ko = struct.unpack_from('<IIII', w.data, pos + 4)
        keys = struct.unpack_from('<I', w.data, to + to_altered['index'] * 8)[0] if to_altered['index'] < tn else 0
        if keys != ARM_ALPHA_KEYS or struct.unpack_from('<I', w.data, to + index * 8)[0]:
            continue
        times, values = key_entry(w, 0)
        struct.pack_into('<II', w.data, to + index * 8, *times)
        struct.pack_into('<II', w.data, ko + index * 8, *values)
        fixed += 1
    seq_offset = struct.unpack_from('<I', w.data, 0x20)[0]
    struct.pack_into('<I', w.data, seq_offset + to_altered['index'] * R.SEQ_SIZE + 4, MALE_TO_ALTERED_LENGTH)
    save(path, w)
    print('%s: %d arm colours hidden in %d, %d lengthened to %d ms' % (os.path.basename(path), fixed, POST_SWAP, TO_ALTERED, MALE_TO_ALTERED_LENGTH))


def worgen_female(source, path):
    R.retarget(source, path, ids=(TO_ALTERED, POST_SWAP))
    model = R.Model(path)
    to_altered = model.find(TO_ALTERED)['index']
    post_swap = model.find(POST_SWAP)['index']
    first = min(to_altered, post_swap)
    total = len(model.seqs)
    w = R.Writer(model.data)
    # Colours that batches already use are keyed in 486 as well
    count, offset = struct.unpack_from('<II', w.data, 0x48)
    for c in range(count):
        pos = offset + c * COLOR_SIZE + ALPHA_TRACK
        entries = [((0, 0), (0, 0))] * (total - first)
        entries[to_altered - first] = key_entry(w, 0)
        R.outer(w, pos + 4, first, [e[0] for e in entries])
        R.outer(w, pos + 12, first, [e[1] for e in entries])
    # A new colour for the batches without one: alpha 0 in 486 and no keys elsewhere (visible)
    times = [(0, 0)] * total
    values = [(0, 0)] * total
    times[to_altered], values[to_altered] = key_entry(w, 0)
    color = white_rgb(w) + struct.pack('<HHIIII', 1, R.NONE16, total, pairs(w, times), total, pairs(w, values))
    colors = bytes(w.data[offset:offset + count * COLOR_SIZE]) + color
    struct.pack_into('<II', w.data, 0x48, count + 1, w.append(colors))
    save(path, w)
    views = struct.unpack_from('<I', w.data, 0x44)[0]
    changed = 0
    for view in range(views):
        skin_path = '%s%02d.skin' % (os.path.splitext(path)[0], view)
        skin = load(skin_path)
        batches, batch_offset = struct.unpack_from('<II', skin.data, 0x24)
        for i in range(batches):
            pos = batch_offset + i * BATCH_SIZE + BATCH_COLOR
            if struct.unpack_from('<h', skin.data, pos)[0] < 0:
                struct.pack_into('<h', skin.data, pos, count)
                changed += 1
        save(skin_path, skin)
    print('%s: %d batches take colour %d, hidden in %d' % (os.path.basename(path), changed, count, TO_ALTERED))


def arm_batches(src, src_skin, src_seq):
    """F-024's arm batches are those fading in during its 486: [(submesh, (alpha times, alpha values))]"""
    color_offset = struct.unpack_from('<I', src.data, 0x4C)[0]
    batches, batch_offset = struct.unpack_from('<II', src_skin, 0x24)
    arms = []
    for i in range(batches):
        sub, _, color = struct.unpack_from('<HHh', src_skin, batch_offset + i * BATCH_SIZE + 4)
        if color >= 0:
            track = src.track(color_offset + color * COLOR_SIZE + ALPHA_TRACK, src_seq, '<h', 2)
            if len(track[0]) > 1:
                arms.append((sub, track))
    return arms


def copy_bones(src, tgt, w, arms, src_skin, src_seq, to_altered):
    """Appends the bones the arm submeshes use with all their parents, parents first. {source bone: new bone}"""
    total = len(tgt.seqs)
    vertex_offset = struct.unpack_from('<I', src.data, 0x40)[0]
    skin_vertices = struct.unpack_from('<I', src_skin, 8)[0]
    sub_offset = struct.unpack_from('<I', src_skin, 0x20)[0]
    chain = set()
    for sub, _ in arms:
        start, count = struct.unpack_from('<HH', src_skin, sub_offset + sub * SUBMESH_SIZE + 4)
        for k in range(start, start + count):
            vertex = struct.unpack_from('<H', src_skin, skin_vertices + k * 2)[0]
            weights = struct.unpack_from('<4B', src.data, vertex_offset + vertex * VERTEX_SIZE + 12)
            indices = struct.unpack_from('<4B', src.data, vertex_offset + vertex * VERTEX_SIZE + 16)
            for bone in (b for b, a in zip(indices, weights) if a):
                while bone >= 0 and bone not in chain:
                    chain.add(bone)
                    bone = src.bones[bone]['parent']
    bone_map = {b: len(tgt.bones) + i for i, b in enumerate(sorted(chain))}
    bones = []
    for b in sorted(chain):
        bone = src.bones[b]
        raw = bytearray(src.data[bone['pos']:bone['pos'] + R.BONE_SIZE])
        struct.pack_into('<i', raw, 0, -1)
        struct.pack_into('<h', raw, 8, bone_map[bone['parent']] if bone['parent'] >= 0 else -1)
        for name, fmt, size in (('trans', '<3f', 12), ('rot', '<4H', 8), ('scale', '<3f', 12)):
            times, values = src.track(bone['pos'] + R.TRACK_OFFSETS[name], src_seq, fmt, size)
            outer_times, outer_values = [(0, 0)] * total, [(0, 0)] * total
            if times:
                outer_times[to_altered] = (len(times), w.append(struct.pack('<%dI' % len(times), *times)))
                outer_values[to_altered] = (len(values), w.append(b''.join(struct.pack(fmt, *v) for v in values)))
            interp = struct.unpack_from('<H', src.data, bone['pos'] + R.TRACK_OFFSETS[name])[0]
            struct.pack_into('<HHIIII', raw, R.TRACK_OFFSETS[name], interp, R.NONE16,
                             total, pairs(w, outer_times), total, pairs(w, outer_values))
        bones.append(bytes(raw))
    offset = struct.unpack_from('<I', w.data, 0x30)[0]
    old = bytes(w.data[offset:offset + len(tgt.bones) * R.BONE_SIZE])
    struct.pack_into('<II', w.data, 0x2C, len(tgt.bones) + len(bones), w.append(old + b''.join(bones)))
    return bone_map


def add_arm_colors(w, arms, total, to_altered):
    """The fade of F-024's 486, alpha 0 in every other sequence (no keys would mean visible). The first new colour."""
    colors, offset = struct.unpack_from('<II', w.data, 0x48)
    zero_time, zero_value = w.append(struct.pack('<I', 0)), w.append(struct.pack('<h', 0))
    new_colors = []
    for _, (times, values) in arms:
        outer_times, outer_values = [(1, zero_time)] * total, [(1, zero_value)] * total
        outer_times[to_altered] = (len(times), w.append(struct.pack('<%dI' % len(times), *times)))
        outer_values[to_altered] = (len(values), w.append(b''.join(struct.pack('<h', *v) for v in values)))
        new_colors.append(white_rgb(w) + struct.pack('<HHIIII', 1, R.NONE16, total, pairs(w, outer_times), total, pairs(w, outer_values)))
    old = bytes(w.data[offset:offset + colors * COLOR_SIZE])
    struct.pack_into('<II', w.data, 0x48, colors + len(new_colors), w.append(old + b''.join(new_colors)))
    return colors


def port_arms(source, path):
    src, tgt = R.Model(source), R.Model(path)
    w = R.Writer(tgt.data)
    src_seq = src.find(TO_ALTERED)
    to_altered = tgt.find(TO_ALTERED)['index']
    with open(src.base + '00.skin', 'rb') as fh:
        src_skin = fh.read()
    skin_path = tgt.base + '00.skin'
    skin = load(skin_path)
    arms = arm_batches(src, src_skin, src_seq)
    bone_map = copy_bones(src, tgt, w, arms, src_skin, src_seq, to_altered)
    first_color = add_arm_colors(w, arms, len(tgt.seqs), to_altered)
    # Vertices with their new bones, a bone palette per submesh, submeshes, and batches on the body's material
    vertex_offset = struct.unpack_from('<I', src.data, 0x40)[0]
    skin_vertices = struct.unpack_from('<I', src_skin, 8)[0]
    skin_triangles = struct.unpack_from('<I', src_skin, 0x10)[0]
    sub_offset = struct.unpack_from('<I', src_skin, 0x20)[0]
    tgt_vertices, tgt_vertex_offset = struct.unpack_from('<II', w.data, 0x3C)
    lookup, lookup_offset = struct.unpack_from('<II', w.data, 0x78)
    views = {pos: struct.unpack_from('<II', skin.data, pos) for pos in (4, 0xC, 0x14, 0x1C, 0x24)}
    template = bytes(skin.data[views[0x24][1]:views[0x24][1] + BATCH_SIZE])
    vertices, new_lookup, vertex_list, triangles, properties, subs, batches = [], [], [], [], [], [], []
    for n, (sub, _) in enumerate(arms):
        record = bytearray(src_skin[sub_offset + sub * SUBMESH_SIZE:sub_offset + (sub + 1) * SUBMESH_SIZE])
        geoset, _, start, count, tri_start, tri_count = struct.unpack_from('<6H', record, 0)
        palette = []
        first_list = views[4][0] + len(vertex_list)
        first_triangle = views[0xC][0] + len(triangles)
        for k in range(start, start + count):
            vertex = struct.unpack_from('<H', src_skin, skin_vertices + k * 2)[0]
            raw = bytearray(src.data[vertex_offset + vertex * VERTEX_SIZE:vertex_offset + (vertex + 1) * VERTEX_SIZE])
            mapped, local = [], []
            for a, b in zip(struct.unpack_from('<4B', raw, 12), struct.unpack_from('<4B', raw, 16)):
                if not a:
                    mapped.append(0)
                    local.append(0)
                    continue
                if b not in palette:
                    palette.append(b)
                mapped.append(bone_map[b])
                local.append(palette.index(b))
            struct.pack_into('<4B', raw, 16, *mapped)
            vertex_list.append(tgt_vertices + len(vertices))
            vertices.append(bytes(raw))
            properties.append(bytes(local))
        for k in range(tri_start, tri_start + tri_count):
            triangles.append(struct.unpack_from('<H', src_skin, skin_triangles + k * 2)[0] - start + first_list)
        center = struct.unpack_from('<H', record, 18)[0]
        struct.pack_into('<6H', record, 0, geoset, 0, first_list, count, first_triangle, tri_count)
        struct.pack_into('<HH', record, 12, len(palette), lookup + len(new_lookup))
        struct.pack_into('<H', record, 18, bone_map.get(center, bone_map[palette[0]]))
        new_lookup.extend(bone_map[b] for b in palette)
        subs.append(bytes(record))
        batch = bytearray(template)
        struct.pack_into('<HHh', batch, 4, views[0x1C][0] + n, views[0x1C][0] + n, first_color + n)
        batches.append(bytes(batch))
    old = bytes(w.data[tgt_vertex_offset:tgt_vertex_offset + tgt_vertices * VERTEX_SIZE])
    struct.pack_into('<II', w.data, 0x3C, tgt_vertices + len(vertices), w.append(old + b''.join(vertices)))
    old = bytes(w.data[lookup_offset:lookup_offset + lookup * 2])
    struct.pack_into('<II', w.data, 0x78, lookup + len(new_lookup), w.append(old + struct.pack('<%dH' % len(new_lookup), *new_lookup)))
    for pos, size, extra in ((4, 2, struct.pack('<%dH' % len(vertex_list), *vertex_list)),
                             (0xC, 2, struct.pack('<%dH' % len(triangles), *triangles)),
                             (0x14, 4, b''.join(properties)),
                             (0x1C, SUBMESH_SIZE, b''.join(subs)),
                             (0x24, BATCH_SIZE, b''.join(batches))):
        count, offset = views[pos]
        old = bytes(skin.data[offset:offset + count * size])
        struct.pack_into('<II', skin.data, pos, count + len(extra) // size, skin.append(old + extra))
    save(path, w)
    save(skin_path, skin)
    print('%s: %d arm batches, %d vertices and %d bones copied' % (os.path.basename(path), len(arms), len(vertices), len(bone_map)))


def hide_attachments(path):
    """Hiding her body leaves what its attachments carry: weapons, shoulders, a helmet. Their visibility tracks get 0 in
    486 (M2Model.cpp, AnimateAttachmentsMT); no keys elsewhere means visible. The tracks are empty in this model."""
    model = R.Model(path)
    w = R.Writer(model.data)
    to_altered = model.find(TO_ALTERED)['index']
    total = len(model.seqs)
    count, offset = struct.unpack_from('<II', w.data, 0xF0)
    time, value = w.append(struct.pack('<I', 0)), w.append(struct.pack('<B', 0))
    for i in range(count):
        pos = offset + i * ATTACHMENT_SIZE + ATTACHMENT_TRACK
        if struct.unpack_from('<I', w.data, pos + 4)[0]:
            raise SystemExit('%s: attachment %d already has a visibility track' % (path, i))
        times, values = [(0, 0)] * total, [(0, 0)] * total
        times[to_altered], values[to_altered] = (1, time), (1, value)
        struct.pack_into('<HHIIII', w.data, pos, 0, R.NONE16, total, pairs(w, times), total, pairs(w, values))
    save(path, w)
    print('%s: %d attachments hidden in %d' % (os.path.basename(path), count, TO_ALTERED))


def goblin(path):
    model = R.Model(path)
    w = R.Writer(model.data)
    colors, color_offset = struct.unpack_from('<II', w.data, 0x48)
    with open(model.base + '00.skin', 'rb') as fh:
        skin = fh.read()
    batches, batch_offset = struct.unpack_from('<II', skin, 0x24)
    stand = model.find(0)
    lids = set()
    for i in range(batches):
        color = struct.unpack_from('<h', skin, batch_offset + i * BATCH_SIZE + BATCH_COLOR)[0]
        if color >= 0:
            times, values = model.track(color_offset + color * COLOR_SIZE + ALPHA_TRACK, stand, '<h', 2)
            if len(times) > 1 and any(v[0] for v in values):
                lids.add(color)
    for color in lids:                  # the eyelid mesh: never shown
        kn, ko = struct.unpack_from('<II', w.data, color_offset + color * COLOR_SIZE + ALPHA_TRACK + 12)
        for s in range(min(kn, len(model.seqs))):
            count, offset = struct.unpack_from('<II', w.data, ko + s * 8)
            if count and model.seqs[s]['flags'] & R.HAS_DATA:
                struct.pack_into('<%dh' % count, w.data, offset, *[0] * count)
    weights, weight_offset = struct.unpack_from('<II', w.data, 0x58)
    if weights <= GLOW_WEIGHT:
        raise SystemExit('%s: no eye glow weight' % path)
    _, loop, _, _, _, ko = struct.unpack_from('<HHIIII', w.data, weight_offset + GLOW_WEIGHT * 20)
    count, offset = struct.unpack_from('<II', w.data, ko)
    if loop == R.NONE16 or not count:
        raise SystemExit('%s: expected a blink on a global sequence' % path)
    struct.pack_into('<%dh' % count, w.data, offset, *[FULL_ALPHA] * count)
    save(path, w)
    print('%s: %d eyelid colours removed, eye glow always on' % (os.path.basename(path), len(lids)))


def fix_all(character):
    worgen_male(os.path.join(character, 'AlphaWorgen', 'Male', 'AlphaWorgenMale.m2'))
    source = os.path.join(character, 'Worgen', 'female', 'worgenfemale.m2')
    target = os.path.join(character, 'AlphaWorgen', 'Female', 'AlphaWorgenFemale.m2')
    worgen_female(source, target)
    port_arms(source, target)
    hide_attachments(target)
    goblin(os.path.join(character, 'AlphaGoblin', 'Male', 'AlphaGoblinMale.m2'))
    goblin(os.path.join(character, 'AlphaGoblin', 'Female', 'AlphaGoblinFemale.m2'))


if __name__ == '__main__':
    fix_all(sys.argv[1])

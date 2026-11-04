"""Move a 3.3.5 (version 264) creature model up or down, for models that float above their origin (e.g. the Mana Wyrm,
F-011's Blood Elf aquatic form). DBCs have no height offset, so this has to be done in the M2.

Bone matrix = parent * translate(pivot + t) * rotate * scale * translate(-pivot): adding the same offset to every vertex
and pivot moves the model rigidly in every animation, with the tracks untouched. Attachments, events, particle emitters,
ribbons and lights are model-space positions on bones, so they move along; the bounding boxes and the cameras' bases
move too, so culling and portraits stay right. .skin files don't hold positions and can be copied as they are.

Usage: m2_shift_z.py <in.m2> <out.m2> <offset in model units, before display scale; negative lowers>"""
import struct
import sys

SEQUENCE_SIZE, VERTEX_SIZE, BONE_SIZE = 64, 48, 88

# header offset of the (count, offset) pair, record size, offsets of the positions in a record
POSITIONS = {
    'bones': (0x2C, BONE_SIZE, [76]),
    'vertices': (0x3C, VERTEX_SIZE, [0]),
    'bounding vertices': (0xE0, 12, [0]),
    'attachments': (0xF0, 40, [8]),
    'events': (0x100, 36, [12]),
    'lights': (0x108, 156, [4]),
    'cameras': (0x110, 100, [36, 68]),
    'ribbons': (0x120, 176, [8]),
    'particles': (0x128, 476, [8]),
}


def add_z(data, position_offset, dz):
    z = position_offset + 8
    struct.pack_into('<f', data, z, struct.unpack_from('<f', data, z)[0] + dz)


def main():
    source, target, dz = sys.argv[1], sys.argv[2], float(sys.argv[3])
    with open(source, 'rb') as f:
        data = bytearray(f.read())

    magic, version = struct.unpack_from('<4sI', data, 0)
    if magic != b'MD20' or version != 264:
        sys.exit('%s: not a version 264 M2 (%r %d)' % (source, magic, version))

    for name, (header, size, offsets) in POSITIONS.items():
        count, start = struct.unpack_from('<II', data, header)
        for i in range(count):
            for offset in offsets:
                add_z(data, start + i * size + offset, dz)
        print('%s: %d' % (name, count))

    # Overall bounding box (the collision box stays: it's a cylinder from the ground up, not this model's shape)
    add_z(data, 0xA0, dz)
    add_z(data, 0xAC, dz)

    # Each sequence's bounds: min and max at +32 and +44
    count, start = struct.unpack_from('<II', data, 0x1C)
    for i in range(count):
        add_z(data, start + i * SEQUENCE_SIZE + 32, dz)
        add_z(data, start + i * SEQUENCE_SIZE + 44, dz)

    with open(target, 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    main()

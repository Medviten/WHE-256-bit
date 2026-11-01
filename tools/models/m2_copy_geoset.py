"""Make a 3.3.5 character model also draw one geoset's triangles under another geoset id.

For every skin profile (<model>NN.skin) each skin section with id FROM gets a copy with id TO that points at the same
vertices and triangles, and each batch drawing such a section gets a copy drawing the new one (same material and
textures). Nothing is duplicated but the 48-byte section and 24-byte batch entries; the grown arrays are moved to the
end of the .skin file.

Used for models whose geoset TO leaves a hole that FROM closes, e.g. a retail-style female Vrykul whose robe (1302)
does not reach the hip seam that only the legs (1301) close: with "1301 1302" a robe also draws the legs, which the
compositor paints with the robe's leg texture. Running it twice adds the copies twice; it refuses if TO already has a
section over the same triangles.

usage: python -I m2_copy_geoset.py <model.m2> FROM TO   (skin files are changed in place)"""
import os
import struct
import sys

SECTION_SIZE, BATCH_SIZE = 48, 24


def copy_geoset(skin, source, target):
    data = bytearray(skin)
    nsec, osec = struct.unpack_from('<II', data, 0x1C)
    nbat, obat = struct.unpack_from('<II', data, 0x24)
    sections = [bytes(data[osec + i * SECTION_SIZE:osec + (i + 1) * SECTION_SIZE]) for i in range(nsec)]
    batches = [bytes(data[obat + i * BATCH_SIZE:obat + (i + 1) * BATCH_SIZE]) for i in range(nbat)]

    # the index range (level holds the high bits of the start) identifies a section's triangles
    def triangles(section):
        level, _, _, start, count = struct.unpack_from('<HHHHH', section, 2)
        return (level, start, count)

    existing = {triangles(s) for s in sections if struct.unpack_from('<H', s, 0)[0] == target}
    new_index = {}
    for i, s in enumerate(sections):
        if struct.unpack_from('<H', s, 0)[0] != source:
            continue
        if triangles(s) in existing:
            raise ValueError('geoset %d already draws the triangles of geoset %d' % (target, source))
        copy = bytearray(s)
        struct.pack_into('<H', copy, 0, target)
        new_index[i] = len(sections)
        sections.append(bytes(copy))
    if not new_index:
        return None
    for b in list(batches):
        section = struct.unpack_from('<H', b, 4)[0]
        if section in new_index:
            copy = bytearray(b)
            struct.pack_into('<HH', copy, 4, new_index[section], new_index[section])   # skin section, geoset index
            batches.append(bytes(copy))

    data += b'\0' * (-len(data) % 16)
    struct.pack_into('<II', data, 0x1C, len(sections), len(data))
    data += b''.join(sections)
    data += b'\0' * (-len(data) % 16)
    struct.pack_into('<II', data, 0x24, len(batches), len(data))
    data += b''.join(batches)
    return bytes(data), len(new_index)


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    model, source, target = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    with open(model, 'rb') as f:
        profiles = struct.unpack_from('<I', f.read(0x48), 0x44)[0]
    base = os.path.splitext(model)[0]
    for profile in range(profiles):
        path = '%s%02d.skin' % (base, profile)
        with open(path, 'rb') as f:
            skin = f.read()
        result = copy_geoset(skin, source, target)
        if result is None:
            print('%s: no geoset %d' % (path, source))
            continue
        with open(path, 'wb') as f:
            f.write(result[0])
        print('%s: %d section(s) of geoset %d now also drawn as %d' % (path, result[1], source, target))


if __name__ == '__main__':
    main()

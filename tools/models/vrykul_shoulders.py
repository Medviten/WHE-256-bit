"""Turn the female Vrykul PC model's right shoulder pad the right way up.

Shoulder pads attach to attachment points 5 (right) and 6 (left), each on a helper bone under the upper arm whose
constant rotation (on a global sequence) keeps the pad upright. In this model the right helper (bone 105) turns about
140 degrees where its left twin (106) turns about 50, so the right pad sits on its side / upside down. This copies the
left helper's rotation keys onto the right one, mirrored across the model's left-right plane ((x, y, z, w) ->
(-x, y, -z, w); negating a compressed quaternion component is a bitwise NOT).

usage: python -I vrykul_shoulders.py <VrykulPCFemale.m2>   (in place)"""
import struct
import sys

RIGHT, LEFT = 105, 106
BONE_SIZE, ROTATION = 88, 0x24


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    model = sys.argv[1]
    with open(model, 'rb') as f:
        data = bytearray(f.read())
    nbones, obones = struct.unpack_from('<II', data, 0x2C)

    def track(bone):
        interp, loop, ntimes, otimes, nkeys, okeys = struct.unpack_from('<hhIIII', data, obones + BONE_SIZE * bone + ROTATION)
        return loop, [struct.unpack_from('<II', data, okeys + 8 * i) for i in range(nkeys)]

    right_loop, right = track(RIGHT)
    left_loop, left = track(LEFT)
    if right_loop != left_loop or [c for c, _ in right] != [c for c, _ in left]:
        sys.exit('%s: bones %d and %d have differently shaped rotation tracks' % (model, RIGHT, LEFT))
    keys = 0
    for (count, rofs), (_, lofs) in zip(right, left):
        for k in range(count):
            x, y, z, w = struct.unpack_from('<4h', data, lofs + 8 * k)
            struct.pack_into('<4h', data, rofs + 8 * k, ~x, y, ~z, w)
            keys += 1
    with open(model, 'wb') as f:
        f.write(data)
    print('%s: %d rotation key(s) of bone %d set to the mirror of bone %d' % (model, keys, RIGHT, LEFT))


if __name__ == '__main__':
    main()

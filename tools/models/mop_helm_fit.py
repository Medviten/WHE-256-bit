#!/usr/bin/env python3
"""Raise MoP Classic's Pandaren helmets (*_pam.m2, *_paf.m2) to fit F-129's 5.4.8 Pandaren heads.

  python -I mop_helm_fit.py HEAD_FOLDER

MoP Classic's helmet variants are fitted to its HD Pandaren, whose head top sits closer above the head attachment
(id 11) than on the 5.4.8 models F-129 uses: 98th-percentile head-top vertex minus attachment height, male
0.166 vs 0.445, female 0.100 vs 0.385 (pandarenmale.m2 / pandarenfemale.m2 of 5.5.4.70631 against WHE-common's).
Hats such as Master Shang Xi's sunhat therefore sit about 0.28 too low and cut through the neck. This moves each
variant's vertices, bone pivots and bounds up by that difference.

The files done are listed in HEAD_FOLDER/mop_helm_fit.done, so a rerun doesn't raise them twice."""
import glob, os, struct, sys

RAISE = {'m': 0.279, 'f': 0.285}
VERTEX, BONE = 48, 88          # 3.3.5 M2Vertex; M2CompBone with three 20-byte tracks, pivot at +76


def raise_model(path, dz):
    d = bytearray(open(path, 'rb').read())
    if d[:4] != b'MD20':
        return False
    n, o = struct.unpack_from('<II', d, 0x3C)
    for i in range(n):
        k = o + VERTEX * i + 8
        struct.pack_into('<f', d, k, struct.unpack_from('<f', d, k)[0] + dz)
    n, o = struct.unpack_from('<II', d, 0x2C)
    for i in range(n):
        k = o + BONE * i + 76 + 8
        struct.pack_into('<f', d, k, struct.unpack_from('<f', d, k)[0] + dz)
    for box in (0xA0, 0xBC):             # bounding and collision box: min z, max z
        for k in (box + 8, box + 20):
            struct.pack_into('<f', d, k, struct.unpack_from('<f', d, k)[0] + dz)
    open(path, 'wb').write(d)
    return True


def main():
    folder = sys.argv[1]
    record = os.path.join(folder, 'mop_helm_fit.done')
    done = set(open(record).read().split()) if os.path.exists(record) else set()
    raised = []
    for path in sorted(glob.glob(os.path.join(folder, '*_pa[mf].m2'))):
        name = os.path.basename(path).lower()
        if name not in done and raise_model(path, RAISE[name[-4]]):
            raised.append(name)
    with open(record, 'a') as fh:
        fh.writelines(n + '\n' for n in raised)
    print('raised %d Pandaren helmets (%d done before)' % (len(raised), len(done)))


if __name__ == '__main__':
    main()

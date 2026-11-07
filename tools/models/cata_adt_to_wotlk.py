#!/usr/bin/env python3
"""Convert Cataclysm split ADTs (root + _tex0 + _obj0) to 3.3.5a single-file ADTs.

  python cata_adt_to_wotlk.py IN_DIR OUT_DIR --cata-dbc DIR --stock-dbc DIR [--effects GroundEffectTexture.dbc]
                               [--name NEW_PREFIX]

Converts every <map>_<x>_<y>.adt in IN_DIR that has its _tex0 and _obj0 files. The output keeps the input's names
(or NEW_PREFIX_<x>_<y>.adt). The 3.3.5a client must have the big alpha flag (0x4) set in the WDT of the map these
tiles are loaded for, as Cataclysm alpha maps are 4096 bytes (or compressed, MCLY flag 0x200), which 3.3.5a reads
only then. Open Azeroth's Kalimdor.wdt has it.

What goes where (3.3.5a layout as in Blizzard's and Open Azeroth's own tiles):
- MVER, MHDR (offsets from its data), MCIN (absolute offsets, sizes with the chunk header)
- MTEX and MTXF from _tex0 (MAMP is Cataclysm-only and dropped); MMDX, MMID, MWMO, MWID, MDDF, MODF from _obj0;
  MH2O from the root. Its layout didn't change, but later files give some liquid instances a LiquidObject id (42 and
  up) where 3.3.5a reads the vertex format (0-3), and liquid types 3.3.5a lacks (301 Shallow Water). Both are
  resolved from the Cataclysm DBCs (--cata-dbc: LiquidObject -> LiquidType -> LiquidMaterial's vertex format), a
  type stock LiquidType.dbc (--stock-dbc) lacks becomes the stock type of the same kind (water, ocean, magma or
  slime), and an instance whose vertex data doesn't fit its format becomes depth-only (format 2, no data)
- each MCNK: the root's 128-byte header with its offsets redone, then MCVT, MCCV, MCNR (written as 435 bytes plus
  13 padding bytes, as 3.3.5a does), MCLY, MCRF (the _obj0 chunk's MCRD doodad refs then MCRW map object refs),
  MCSH, MCAL, MCLQ (if the root has one) and MCSE. _tex0's MCMT is dropped. Cataclysm's high-res holes (flag
  0x10000, 8 bytes where 3.3.5a keeps the MCVT and MCNR offsets) become low-res holes: a 2 x 2 group of them that
  is all holes makes its low-res hole, as Zeppelin-Craft's server map builder does.
- MCLY ground effect ids are kept. The client skips ids GroundEffectTexture.dbc doesn't have (Open Azeroth's own
  tiles have such ids too); --effects (the client's GroundEffectTexture.dbc) sets them to 0 instead."""
import argparse, os, re, struct

MCNK_HEADER = 128
STOCK_KIND = {0: 1, 1: 2, 2: 3, 3: 4}  # LiquidType.Type (water, ocean, magma, slime) -> stock LiquidType id
VERTEX_BYTES = (5, 8, 1, 9)           # per vertex, by vertex format: height+depth, height+uv, depth, all three


def dbc_rows(path):
    d = open(path, "rb").read()
    _, n, f, size, _ = struct.unpack_from("<4s4I", d)
    return {r[0]: r for r in (struct.unpack_from(f"<{f}i", d, 20 + i * size) for i in range(n))}


class Liquids:
    def __init__(self, cata_dir, stock_dir):
        self.objects = dbc_rows(os.path.join(cata_dir, "LiquidObject.dbc"))      # id, flow dir, speed, type, ...
        self.types = dbc_rows(os.path.join(cata_dir, "LiquidType.dbc"))          # id, name, flags, kind, ... 14 material
        self.materials = dbc_rows(os.path.join(cata_dir, "LiquidMaterial.dbc"))  # id, vertex format, flags
        self.stock = set(dbc_rows(os.path.join(stock_dir, "LiquidType.dbc")))
        self.fixed = 0

    def fix(self, mh2o):
        """Rewrite the MH2O instances 3.3.5a can't read, in place."""
        size = len(mh2o)
        for k in range(256):
            first, count, _ = struct.unpack_from("<3I", mh2o, k * 12)
            for n in range(count):
                at = first + n * 24
                ltype, fmt, _, _, _, _, w, h, exists, data = struct.unpack_from("<HHffBBBBII", mh2o, at)
                old = (ltype, fmt, data)
                if fmt >= 42:
                    obj = self.objects.get(fmt)
                    kind = self.types.get(obj[3]) if obj else None
                    material = self.materials.get(kind[14]) if kind else None
                    fmt = material[1] if material else 2
                if ltype not in self.stock:
                    kind = self.types.get(ltype)
                    ltype = STOCK_KIND.get(kind[3] if kind else 0, 1)
                if data and (fmt > 3 or data + (w + 1) * (h + 1) * VERTEX_BYTES[fmt] > size):
                    fmt, data = 2, 0
                if (ltype, fmt, data) != old:
                    struct.pack_into("<HH", mh2o, at, ltype, fmt)
                    struct.pack_into("<I", mh2o, at + 20, data)
                    self.fixed += 1
        return bytes(mh2o)


def chunks(d, start=0, end=None):
    i, end = start, len(d) if end is None else end
    while i + 8 <= end:
        tag = d[i:i + 4][::-1].decode("latin1")
        size = struct.unpack_from("<I", d, i + 4)[0]
        yield tag, d[i + 8:i + 8 + size]
        i += 8 + size


def chunk(tag, data, size=None):
    return tag[::-1].encode("latin1") + struct.pack("<I", len(data) if size is None else size) + data


def top(d):
    out = {}
    mcnk = []
    for tag, data in chunks(d):
        if tag == "MCNK":
            mcnk.append(data)
        else:
            out[tag] = data
    return out, mcnk


def sub(data, start=0):
    out = {}
    for tag, payload in chunks(data, start):
        out.setdefault(tag, payload)
    return out


def known_effects(path):
    if not path:
        return None
    d = open(path, "rb").read()
    _, n, _, size, _ = struct.unpack_from("<4s4I", d)
    return {struct.unpack_from("<I", d, 20 + i * size)[0] for i in range(n)}


def convert(root_path, tex_path, obj_path, liquids, effects=None):
    root, root_mcnk = top(open(root_path, "rb").read())
    tex, tex_mcnk = top(open(tex_path, "rb").read())
    obj, obj_mcnk = top(open(obj_path, "rb").read())
    if "MH2O" in root:
        root["MH2O"] = liquids.fix(bytearray(root["MH2O"]))
    if not (len(root_mcnk) == len(tex_mcnk) == len(obj_mcnk) == 256):
        raise SystemExit(f"{root_path}: MCNK counts {len(root_mcnk)}/{len(tex_mcnk)}/{len(obj_mcnk)}, not 256")

    dropped = 0
    cells = []
    for r, t, o in zip(root_mcnk, tex_mcnk, obj_mcnk):
        header = bytearray(r[:MCNK_HEADER])
        if struct.unpack_from("<I", header, 0)[0] & 0x10000:
            hi = header[0x14:0x1C]
            low = 0
            for row in range(4):
                for col in range(4):
                    if all((hi[row * 2 + dr] >> (col * 2 + dc)) & 1 for dr in (0, 1) for dc in (0, 1)):
                        low |= 1 << (row * 4 + col)
            struct.pack_into("<I", header, 0, struct.unpack_from("<I", header, 0)[0] & ~0x10000)
            struct.pack_into("<H", header, 0x3C, low)
        rs, ts, os_ = sub(r, MCNK_HEADER), sub(t), sub(o)
        mcly = bytearray(ts.get("MCLY", b""))
        if effects is not None:
            for k in range(0, len(mcly), 16):
                effect = struct.unpack_from("<I", mcly, k + 12)[0]
                if effect and effect not in effects:
                    struct.pack_into("<I", mcly, k + 12, 0)
                    dropped += 1
        doodads, objects = os_.get("MCRD", b""), os_.get("MCRW", b"")
        body = bytearray()
        offsets = {}

        def put(tag, data, size=None):
            offsets[tag] = 8 + MCNK_HEADER + len(body)
            body.extend(chunk(tag, data, size))

        put("MCVT", rs["MCVT"])
        if "MCCV" in rs:
            put("MCCV", rs["MCCV"])
        normals = rs["MCNR"]
        put("MCNR", normals[:448].ljust(448, b"\0"), 435)
        put("MCLY", bytes(mcly))
        put("MCRF", doodads + objects)
        put("MCSH", ts.get("MCSH", b""))
        put("MCAL", ts.get("MCAL", b""))
        if "MCLQ" in rs:
            put("MCLQ", rs["MCLQ"])
        put("MCSE", rs.get("MCSE", b""))

        def field(index, value):
            struct.pack_into("<I", header, index * 4, value)
        field(3, len(mcly) // 16)                             # nLayers
        field(4, len(doodads) // 4)                           # nDoodadRefs
        field(5, offsets["MCVT"])
        field(6, offsets["MCNR"])
        field(7, offsets["MCLY"])
        field(8, offsets["MCRF"])
        field(9, offsets["MCAL"])
        field(10, len(ts.get("MCAL", b"")) + 8)               # sizeAlpha, as 3.3.5a stores it (with the header)
        field(11, offsets["MCSH"])
        field(12, len(ts.get("MCSH", b"")))                   # sizeShadow
        field(14, len(objects) // 4)                          # nMapObjRefs
        field(22, offsets["MCSE"])
        field(23, len(rs.get("MCSE", b"")) // 28)             # nSndEmitters (28-byte entries)
        field(24, offsets.get("MCLQ", 0))
        field(25, len(rs["MCLQ"]) + 8 if "MCLQ" in rs else 8)  # sizeLiquid: 8 with no MCLQ, as 3.3.5a writes it
        field(29, offsets.get("MCCV", 0))
        field(30, 0)                                          # ofsMCLV: Cataclysm only
        cells.append(bytes(header) + bytes(body))

    out = bytearray(chunk("MVER", struct.pack("<I", 18)))
    mhdr_at = len(out)
    out.extend(chunk("MHDR", bytes(64)))
    base = mhdr_at + 8
    mhdr = {}
    mcin_at = len(out)
    out.extend(chunk("MCIN", bytes(256 * 16)))
    mhdr["MCIN"] = mcin_at - base
    for tag, source in (("MTEX", tex), ("MMDX", obj), ("MMID", obj), ("MWMO", obj), ("MWID", obj),
                        ("MDDF", obj), ("MODF", obj), ("MH2O", root)):
        if tag in source or tag in ("MTEX", "MMDX", "MMID", "MWMO", "MWID", "MDDF", "MODF"):
            mhdr[tag] = len(out) - base
            out.extend(chunk(tag, source.get(tag, b"")))
    mcin = bytearray()
    for cell in cells:
        mcin.extend(struct.pack("<4I", len(out), len(cell) + 8, 0, 0))
        out.extend(chunk("MCNK", cell))
    if "MFBO" in root:
        mhdr["MFBO"] = len(out) - base
        out.extend(chunk("MFBO", root["MFBO"]))
    if "MTXF" in tex:
        mhdr["MTXF"] = len(out) - base
        out.extend(chunk("MTXF", tex["MTXF"]))
    out[mcin_at + 8:mcin_at + 8 + len(mcin)] = mcin
    order = ("MCIN", "MTEX", "MMDX", "MMID", "MWMO", "MWID", "MDDF", "MODF", "MFBO", "MH2O", "MTXF")
    values = [1 if "MFBO" in mhdr else 0] + [mhdr.get(tag, 0) for tag in order] + [0] * 4
    out[base:base + 64] = struct.pack("<16I", *values)
    return bytes(out), dropped


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--cata-dbc", required=True)
    p.add_argument("--stock-dbc", required=True)
    p.add_argument("--effects")
    p.add_argument("--name")
    a = p.parse_args()
    effects = known_effects(a.effects)
    liquids = Liquids(a.cata_dbc, a.stock_dbc)
    os.makedirs(a.output, exist_ok=True)
    files = {f.lower(): f for f in os.listdir(a.input)}
    done = 0
    for low, name in sorted(files.items()):
        m = re.fullmatch(r"(.+)_(\d+)_(\d+)\.adt", low)
        if not m:
            continue
        tex, obj = files.get(f"{m.group(1)}_{m.group(2)}_{m.group(3)}_tex0.adt"), files.get(
            f"{m.group(1)}_{m.group(2)}_{m.group(3)}_obj0.adt")
        if not tex or not obj:
            print(f"{name}: no _tex0/_obj0, skipped")
            continue
        before = liquids.fixed
        data, dropped = convert(*(os.path.join(a.input, f) for f in (name, tex, obj)), liquids, effects)
        if liquids.fixed > before:
            dropped_note = f", {liquids.fixed - before} liquid instances made readable"
        else:
            dropped_note = ""
        prefix = a.name or name[:-len(f"_{m.group(2)}_{m.group(3)}.adt")]
        target = os.path.join(a.output, f"{prefix}_{m.group(2)}_{m.group(3)}.adt")
        with open(target, "wb") as f:
            f.write(data)
        done += 1
        print(f"{os.path.basename(target)}: {len(data)} bytes" + dropped_note
              + (f", {dropped} unknown ground effects cleared" if dropped else ""))
    print(f"{done} tiles")


if __name__ == "__main__":
    main()

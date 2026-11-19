#!/usr/bin/env python3
"""Port a retail map (Exile's Reach, F-137) to WHE's 3.3.5a DBC and world SQL: mop_map_port.py on retail's tables.

  python -I -X utf8 retail_map_port.py CSV_DIR STOCK_DBC_DIR ADT_DIR MODPAKS_DIR MODPAK
                    [--map 2175 --tag F-137 --directory ExilesReach --name "Exile's Reach" --tele-base 21750]
                    [--graveyards TDB_GRAVEYARDS] [--lights-only | --graveyards-only | --tele-only]

CSV_DIR holds wago.tools' exports of the retail build the tiles come from (https://wago.tools/db2/<Table>/csv?build=
12.1.5.70961): Map, AreaTable, Light, LightParams, LightData, UiMap, UiMapAssignment. Retail has no DBCs, so they are
handed to mop_map_port.py in 5.4.8's DBC layout, and it writes the same files as for the Wandering Isle:
MODPAK/dbc/[TAG]_{map,areatable,light,lightparams,lightintband,lightfloatband,worldmaparea,worldmapoverlay}.sql and
MODPAK/sql/db-world/base/[TAG]_{game_tele,graveyard}.sql. What differs from 5.4.8's rows:
- Light: retail's GameCoords are yards in world coordinates; 5.4.8 stored (17066.67 - y, z, 17066.67 - x) x 36 and
  the falloffs x 36 (checked on the Wandering Isle's lights, in both). LightData's columns are matched by name.
- AreaTable: retail's flags mean other things, so a zone gets none and a subarea 0x40000000 (the Wandering Isle's
  5.4.8 rows, the same), both then F-006's flyable 0x4400. Retail has no exploration level or minimum elevation:
  1 for the zone and 5 for its subareas, and -500 (stock's usual).
- WorldMapArea: the zone's UiMap (UiMap Type 3 / 6 assigned to the map's zone area, or to area 0 on a map with one
  zone), its UiMapAssignment region
  scaled out from UiMin / UiMax to the whole map, named --directory (Interface/WorldMap/<directory>/, the art from
  tools/models/retail_map_art.py). No explored-area overlays and no continent: a single zone map, as the Wandering Isle.
- Graveyards: retail's are server side (TrinityCore's world_safe_locs / graveyard_zone): --graveyards is
  tdb_graveyards.py's "wsl|id|map|x|y|z|facing|comment" lines; rows whose comment has "Dungeon" are left out."""
import argparse, csv, os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mop_map_port  # noqa: E402
from cata406_dbc_port import Dbc  # noqa: E402

GRAVEYARDS = None


def bits(v):
    return struct.unpack("<i", struct.pack("<f", float(v)))[0]


def rows(csv_dir, table):
    csv.field_size_limit(1 << 24)
    with open(os.path.join(csv_dir, table + ".csv"), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


class Table:
    """A 5.4.8 Dbc stand-in: records are tuples in the DBC's field order, strings kept in place (s() returns them)."""

    def __init__(self, records):
        self.records = records
        self.rows = {}
        for r in records:
            self.rows.setdefault(r[0], r)

    def get(self, key):
        return self.rows.get(key)

    @staticmethod
    def s(value):
        return value


def pad(values, n):
    return tuple(values) + (0,) * (n - len(values))


def adapt(csv_dir, name, map_id, directory):
    i = lambda v: int(float(v))
    if name == "Map":
        return Table([pad((i(r["ID"]),) + (0,) * 13 + (i(r["TimeOfDayOverride"]),), 20) for r in rows(csv_dir, "Map")])
    if name == "AreaTable":
        out = []
        for r in rows(csv_dir, "AreaTable"):
            parent = i(r["ParentAreaID"])
            out.append(pad((i(r["ID"]), i(r["ContinentID"]), parent, i(r["AreaBit"]), 0x40000000 if parent else 0)
                           + (0,) * 7 + (5 if parent else 1, 0, i(r["FactionGroupMask"])) + (0,) * 4
                           + (bits(-500), bits(r["Ambient_multiplier"])), 24))
        return Table(out)
    if name == "Light":
        out = []
        for r in rows(csv_dir, "Light"):
            x, y, z = (float(r[f"GameCoords_{k}"]) for k in range(3))
            pos = (0, 0, 0) if not (x or y or z) else (bits((17066.666 - y) * 36), bits(z * 36), bits((17066.666 - x) * 36))
            out.append((i(r["ID"]), i(r["ContinentID"])) + pos + (bits(float(r["GameFalloffStart"]) * 36),
                       bits(float(r["GameFalloffEnd"]) * 36)) + tuple(i(r[f"LightParamsID_{k}"]) for k in range(8)))
        return Table(out)
    if name == "LightParams":
        return Table([(i(r["ID"]), i(r["HighlightSky"]), i(r["LightSkyboxID"]), i(r["CloudTypeID"]), bits(r["Glow"]),
                       bits(r["WaterShallowAlpha"]), bits(r["WaterDeepAlpha"]), bits(r["OceanShallowAlpha"]),
                       bits(r["OceanDeepAlpha"])) for r in rows(csv_dir, "LightParams")])
    if name == "LightData":
        colours = ("DirectColor", "AmbientColor", "SkyTopColor", "SkyMiddleColor", "SkyBand1Color", "SkyBand2Color",
                   "SkySmogColor", "SkyFogColor", "SunColor", "CloudSunColor", "CloudEmissiveColor",
                   "CloudLayer1AmbientColor", "CloudLayer2AmbientColor", "OceanCloseColor", "OceanFarColor",
                   "RiverCloseColor", "RiverFarColor", "ShadowOpacity")
        # retail fogs by density and leaves FogEnd 0, which the client takes as fog right at the camera; such rows
        # get 22000 (about 610 yards), the Wandering Isle's 5.4.8 fog end
        return Table([(i(r["ID"]), i(r["LightParamID"]), i(r["Time"])) + tuple(i(r[c]) for c in colours)
                      + (bits(float(r["FogEnd"]) or 22000.0), bits(r["FogScaler"]), bits(r["CloudDensity"]))
                      for r in rows(csv_dir, "LightData")])
    if name == "WorldMapArea":
        zones = {i(r["ID"]) for r in rows(csv_dir, "AreaTable") if i(r["ContinentID"]) == map_id and not i(r["ParentAreaID"])}
        types = {r["ID"]: r["Type"] for r in rows(csv_dir, "UiMap")}
        out = []
        for r in rows(csv_dir, "UiMapAssignment"):
            # Exile's Reach's UiMap is assigned to the whole map (area 0), not to its zone
            area = i(r["AreaID"]) or (min(zones) if len(zones) == 1 else 0)
            if i(r["MapID"]) != map_id or area not in zones or types.get(r["UiMapID"]) not in ("3", "6"):
                continue
            f = {k: float(v) for k, v in r.items() if k.startswith(("Ui", "Region")) and k != "UiMapID"}
            # the region spans UiMin..UiMax of the map image: x (north) runs down it, y (west) across
            span_y = (f["Region_4"] - f["Region_1"]) / (f["UiMax_0"] - f["UiMin_0"])
            span_x = (f["Region_3"] - f["Region_0"]) / (f["UiMax_1"] - f["UiMin_1"])
            left, top = f["Region_4"] + f["UiMin_0"] * span_y, f["Region_3"] + f["UiMin_1"] * span_x
            out.append((i(r["UiMapID"]), map_id, area, directory, bits(left), bits(left - span_y), bits(top),
                        bits(top - span_x), -1, 0, -1))
        return Table(out)
    if name in ("WorldMapOverlay", "WorldMapContinent"):
        return Table([])
    if name == "WorldSafeLocs":
        out = []
        for line in open(GRAVEYARDS, encoding="utf-8") if GRAVEYARDS else ():
            p = line.rstrip("\n").split("|")
            if p[0] == "wsl" and int(p[2]) == map_id and "Dungeon" not in p[7]:
                out.append((int(p[1]), int(p[2]), bits(p[3]), bits(p[4]), bits(p[5]), bits(p[6]), p[7]))
        return Table(out)
    sys.exit(f"no retail stand-in for {name}.dbc")


def main():
    global GRAVEYARDS
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for a in ("csv_dir", "stock_dbc", "adt_dir", "modpaks_dir", "modpak"):
        p.add_argument(a)
    p.add_argument("--map", type=int, default=2175)
    p.add_argument("--tag", default="F-137")
    p.add_argument("--directory", default="ExilesReach")
    p.add_argument("--name", default="Exile's Reach")
    p.add_argument("--tele-base", type=int, default=21750)
    p.add_argument("--graveyards")
    p.add_argument("--lights-only", action="store_true")
    p.add_argument("--graveyards-only", action="store_true")
    p.add_argument("--tele-only", action="store_true")
    a = p.parse_args()
    GRAVEYARDS = a.graveyards
    csv_dir = os.path.abspath(a.csv_dir)
    real = Dbc
    mop_map_port.Dbc = lambda path: (adapt(csv_dir, os.path.splitext(os.path.basename(path))[0], a.map, a.directory)
                                     if os.path.abspath(os.path.dirname(path)) == csv_dir else real(path))
    mop_map_port.HEADER = "-- Generated by tools/races/retail_map_port.py: change the script, not this file.\n\n"
    sys.argv = [sys.argv[0], csv_dir, a.stock_dbc, os.path.join(csv_dir, "AreaTable.csv"), a.adt_dir, a.modpaks_dir,
                a.modpak, "--map", str(a.map), "--tag", a.tag, "--directory", a.directory, "--name", a.name,
                "--tele-base", str(a.tele_base)] + [f for f in ("--lights-only", "--graveyards-only", "--tele-only")
                                                     if getattr(a, f[2:].replace("-", "_"))]
    mop_map_port.main()
    # the comments mop_map_port.py writes for MoP's rows
    for root, _, files in os.walk(a.modpak):
        for f in files:
            if f.startswith(f"[{a.tag}]_") and f.endswith(".sql"):
                path = os.path.join(root, f)
                text = open(path, encoding="utf-8").read()
                new = (text.replace("Mists of Pandaria's map", "retail's map").replace("(MoP area bit", "(retail area bit")
                       .replace("light (MoP's)", "light (retail's)").replace("-- MoP light params", "-- retail light params")
                       .replace("graveyards (MoP's WorldSafeLocs)", "graveyards (TrinityCore's world_safe_locs)"))
                if new != text:
                    open(path, "w", encoding="utf-8", newline="\n").write(new)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Port a Mists of Pandaria map (Pandaria, the Wandering Isle) to WHE's 3.3.5a DBC and world SQL.

  python mop_map_port.py MOP_DBC_DIR STOCK_DBC_DIR AREATABLE_CSV ADT_DIR MODPAKS_DIR MODPAK
                         [--map 870 --tag F-133 --directory HawaiiMainLand --name Pandaria --tele-base 87000]
                         [--move-continents]

The defaults are Pandaria's (F-133). For the Wandering Isle (F-134):
  --map 860 --tag F-134 --directory NewRaceStartZone --name "The Wandering Isle" --tele-base 86100

MOP_DBC_DIR: 5.4.8 (18414) DBCs (References/MoP/MoP_data/dbc). Their strings are ruRU, so English area names come from
AREATABLE_CSV, wago.tools' AreaTable export (https://wago.tools/db2/AreaTable/csv), matched by id.
ADT_DIR: the map's 3.3.5a tiles (Pandaria: World/Maps/HawaiiMainLand from the squished client's Patch-5.mpq; the
Wandering Isle: MoP Classic's tiles from tools/models/wago_folder.py, converted by cata_adt_to_wotlk.py --listfile).
MODPAKS_DIR: every modpak's areatable SQL is read, so the area bits given out here are free in all of them.

As run for F-133 (from the WHE-256-bit root, the ADTs unpacked by tools/models/mpq_unpack.py):
  python -I -X utf8 tools/races/mop_map_port.py ../References/MoP/MoP_data/dbc ../References/original-client-dbc
      AreaTable.csv <unpacked Patch-5>/World/maps/hawaiimainland modpaks modpaks/F-133_mop-pandaria --move-continents

Writes MODPAK/dbc/[TAG]_{map,areatable,light,worldmaparea,worldmapoverlay,worldmapcontinent}.sql and
MODPAK/sql/db-world/base/[TAG]_game_tele.sql.

- The map as Open Azeroth (F-010) has it, but expansion 2: the core refuses a map whose expansion is above the
  account's. Loading screen 3 (Kalimdor's): MoP's aren't in the client. Time of day override as MoP's.
- AreaTable: every 5.4.8 row on the map, keeping the ids (the tiles' MCNK area ids name them). Area bits are moved
  below 4096 (the 3.3.5a explored-zones field holds 128 x 32 bits; MoP's are 4498+), to bits stock and the modpaks
  don't use. Flags keep MoP's (same meanings for the bits these rows use) plus 0x4400, the flyable flags F-006
  sets. Sound provider prefs are 0; exploration level is capped at 80.
- Music: MoP's SoundAmbience, ZoneMusic and ZoneIntroMusicTable rows of the areas and the SoundEntries they play
  ([TAG]_music_soundentries.sql; fetch the files with zep_goblin_sounds.py --sql). --music-only rewrites these and
  the areatable SQL's three music columns, keeping its area bits.
- Light: MoP's lights of the map (ids and positions kept) with MoP's own parameters: each parameter set stock lacks
  becomes a LightParams row (no skybox: MoP's sky models aren't in the client) and LightIntBand/LightFloatBand rows
  from 5.4.8's LightData (which replaced the bands: one row per time of day). Stock's Eastern Kingdoms default
  (light 1, used before) gave the Wandering Isle's rivers its never-seen mauve river colour. --lights-only rewrites
  just these files.
- WorldMapArea/WorldMapOverlay/WorldMapContinent: MoP's continent, zone and explored-area rows (map coordinates,
  addons, the world map). The art is in WHE-common (downloaded by tools/models/mop_map_art.py). A map without a
  WorldMapContinent row (the Wandering Isle) is a single zone map, as 3.3.5a shows dungeons. --move-continents also
  moves Eastern Kingdoms, Kalimdor and Northrend to MoP's places on the World map (F-133, with MoP's World art). --uimap
  (https://wago.tools/db2/UiMapAssignment/csv?build=5.5.4.70631) takes those placements from MoP Classic, whose
  continent highlights the art is drawn for, instead of 5.4.8's rows.
- game_tele: one ".tele" target per zone and subarea the tiles have chunks of (named as the area, without spaces
  or apostrophes: .tele TheSingingPools), on the land chunk nearest the middle of the area's chunks. --tele-only
  rewrites just this file.
- Graveyards: MoP's WorldSafeLocs of the map (not its corpse catchers or starting locations) as game_graveyard rows
  (AC reads graveyards from the world database), each linked in graveyard_zone to every zone of the map for both
  factions, so the core picks the nearest. --graveyards-only rewrites just this file."""
import argparse, collections, csv, glob, os, re, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cata406_dbc_port import Dbc, block, f32  # noqa: E402

FLYABLE = 0x4400
MAX_BITS = 128 * 32
# LightData columns (5.4.8) for the 18 LightIntBand bands, in DayNight::LoadLightingBands' order: diffuse, ambient,
# six sky colours, shadow, five sun and cloud colours, ocean close/far, river close/far (LiquidProcTextures: colours
# 0-1 go with the ocean alphas, 2-3 with the water ones)
INT_BANDS = (3, 4, 5, 6, 7, 8, 9, 10, 20, 11, 12, 13, 14, 15, 16, 17, 18, 19)
# LightFloatBand: fog end and fog start multiplier from LightData, band 3 its cloud density; 2, 4 and 5 as stock's
FLOAT_BANDS = {0: 21, 1: 22, 3: 23}
FLOAT_STOCK = {2: 1.0, 4: 0.95, 5: 1.0}
TILE, CHUNK = 533.3333333, 533.3333333 / 16
HEADER = f"-- Generated by tools/races/mop_map_port.py: change the script, not this file.\n\n"


def used_bits(stock, modpaks_dir, own, tag):
    """Area bits stock and the other modpaks use, and the modpak's own files of other maps (F-137's dungeon file
    [F-137,DC] beside the island's [F-137])."""
    bits = {r[3] for r in stock.records}
    pat = re.compile(r"INSERT INTO `areatable` \([^)]*\) VALUES \((\d+), [^,]+, [^,]+, (\d+)|`area_bit` = (\d+)")
    for f in glob.glob(os.path.join(modpaks_dir, "*", "dbc", "*areatable.sql")):
        if os.path.basename(os.path.dirname(os.path.dirname(f))) == own and tag in os.path.basename(f):
            continue
        for m in pat.finditer(open(f, encoding="utf-8").read()):
            bits.add(int(m.group(2) or m.group(3)))
    return bits


def chunks(adt_dir):
    """(area id, centre x, centre y, ground z, has liquid) of every MCNK."""
    out = []
    for f in sorted(os.listdir(adt_dir)):
        if not f.lower().endswith(".adt"):
            continue
        d = open(os.path.join(adt_dir, f), "rb").read()
        mhdr = struct.unpack_from("<16I", d, 20)
        mcin = 20 + mhdr[1] + 8
        wet = set()
        if mhdr[10]:
            b = 20 + mhdr[10] + 8
            wet = {k for k in range(256) if struct.unpack_from("<III", d, b + k * 12)[1]}
        for k in range(256):
            h = struct.unpack_from("<I", d, mcin + k * 16)[0] + 8
            area = struct.unpack_from("<I", d, h + 0x34)[0]
            px, py, pz = struct.unpack_from("<3f", d, h + 0x68)
            mcvt = struct.unpack_from("<145f", d, h - 8 + struct.unpack_from("<I", d, h + 0x14)[0] + 8)
            ix, iy = struct.unpack_from("<II", d, h + 4)
            out.append((area, px - CHUNK / 2, py - CHUNK / 2, pz + mcvt[4 * 17 + 4], iy * 16 + ix in wet))
    return out


def taken_ids(modpaks_dir, table, own_tag):
    """Ids other modpaks' dbc/*<table>.sql insert."""
    ids = set()
    pat = re.compile(r"INSERT INTO `%s` \([^)]*\) VALUES \((\d+)|INSERT INTO `%s` SET\s*`id` = (\d+)" % (table, table))
    for f in glob.glob(os.path.join(modpaks_dir, "*", "dbc", f"*{table}.sql")):
        if own_tag in os.path.basename(f):
            continue
        ids |= {int(m.group(1) or m.group(2)) for m in pat.finditer(open(f, encoding="utf-8").read())}
    return ids


def uimap_placement(path):
    """WorldMapContinent placement solved from MoP Classic's UiMapAssignment rows on the World map (UiMap 947):
    3.3.5a puts world position p at (31.3125 + offset - p * scale / 533.33) / 62.625 of the map's width (20.875 and
    41.75 for the height), the region's tile-aligned corners give the boundaries."""
    out = {}
    for r in csv.DictReader(open(path, encoding="utf-8")):
        if r["UiMapID"] != "947" or int(r["MapID"]) not in (0, 1, 571, 870, 860):
            continue
        f = {k: float(v) for k, v in r.items() if k.startswith(("Ui", "Region"))}
        xmin, ymin, xmax, ymax = f["Region_0"], f["Region_1"], f["Region_3"], f["Region_4"]
        kx = (f["UiMax_0"] - f["UiMin_0"]) / (ymax - ymin)
        ky = (f["UiMax_1"] - f["UiMin_1"]) / (xmax - xmin)
        scale = round(kx * TILE * 62.625, 4)
        tile = lambda v: round((32 * TILE - v) / TILE)
        # the boundaries also clip the highlight: Azeroth's region stops short of Quel'Thalas' tip in the World art
        top = tile(xmax) - (3 if r["MapID"] == "0" else 0)
        out[int(r["MapID"])] = (tile(ymax), tile(ymin) - 1, top, tile(xmin) - 1,
                                round((f["UiMin_0"] + ymax * kx) * 62.625 - 31.3125, 5),
                                round((f["UiMin_1"] + xmax * ky) * 41.75 - 20.875, 5), scale)
    return out


def write_graveyards(mop_dbc, modpaks_dir, sql_dir, MAP, TAG, NAME):
    zones = sorted(r[0] for r in Dbc(os.path.join(mop_dbc, "AreaTable.dbc")).records if r[1] == MAP and r[2] == 0)
    safe = Dbc(os.path.join(mop_dbc, "WorldSafeLocs.dbc"))
    rows = [r for r in safe.records if r[1] == MAP and not re.search(r"Corpse Catcher|Starting Location", safe.s(r[6]))]
    taken = set()
    pat = re.compile(r"INSERT INTO `game_graveyard` \([^)]*\) VALUES\s*((?:\(\d+,[^)]*\),?\s*)+)")
    for f in glob.glob(os.path.join(modpaks_dir, "*", "sql", "db-world", "**", "*.sql"), recursive=True):
        if TAG in os.path.basename(f):
            continue
        for m in pat.finditer(open(f, encoding="utf-8", errors="replace").read()):
            taken |= {int(x) for x in re.findall(r"\((\d+),", m.group(1))}
    clash = [r[0] for r in rows if r[0] in taken]
    if clash:
        sys.exit(f"graveyard ids {clash} are taken")
    path = os.path.join(sql_dir, f"{TAG}_graveyard.sql")
    if not rows:                                    # a dungeon: its ghosts go to the map's corpse point instead
        if os.path.exists(path):
            os.remove(path)
        print(f"no graveyards for zones {zones}")
        return
    ids = in_ids([r[0] for r in rows])
    out = [HEADER, f"-- {NAME}'s graveyards (MoP's WorldSafeLocs), linked to every zone of map {MAP}",
           f"DELETE FROM `game_graveyard` WHERE `ID` IN {ids};",
           "INSERT INTO `game_graveyard` (`ID`, `Map`, `x`, `y`, `z`, `Comment`) VALUES",
           ",\n".join("  (%d, %d, %.3f, %.3f, %.3f, '%s')" % (r[0], MAP, f32(r[2]), f32(r[3]), f32(r[4]),
                                                            safe.s(r[6]).replace("'", "''")) for r in rows) + ";",
           f"DELETE FROM `graveyard_zone` WHERE `ID` IN {ids};",
           "INSERT INTO `graveyard_zone` (`ID`, `GhostZone`, `Faction`, `Comment`) VALUES",
           ",\n".join("  (%d, %d, 0, '%s')" % (r[0], z, NAME.replace("'", "''")) for r in rows for z in zones) + ";\n"]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out))
    print(f"{len(rows)} graveyards for zones {zones}")


def in_ids(ids):
    return "(" + ", ".join(str(i) for i in ids) + ")"


def write_lights(mop_dbc, stock_dbc, modpaks_dir, dbc_dir, MAP, TAG, NAME):
    light, params = Dbc(os.path.join(mop_dbc, "Light.dbc")), Dbc(os.path.join(mop_dbc, "LightParams.dbc"))
    data = collections.defaultdict(list)
    for r in Dbc(os.path.join(mop_dbc, "LightData.dbc")).records:
        data[r[1]].append(r)
    stock_light = Dbc(os.path.join(stock_dbc, "Light.dbc")).rows
    stock_params = Dbc(os.path.join(stock_dbc, "LightParams.dbc")).rows
    lights = [r for r in light.records if r[1] == MAP]
    taken = taken_ids(modpaks_dir, "light", TAG)
    clash = [r[0] for r in lights if r[0] in stock_light or r[0] in taken]
    if clash:
        sys.exit(f"light ids {clash} are taken")
    out = []
    for r in lights:
        row = {"id": r[0], "map_id": MAP, "pos_x": f32(r[2]), "pos_y": f32(r[3]), "pos_z": f32(r[4]),
               "falloff_start": f32(r[5]), "falloff_end": f32(r[6])}
        row.update(zip(["params_clear", "params_clear_underwater", "params_storm", "params_storm_underwater",
                        "params_death", "params_unk_1", "params_unk_2", "params_unk_3"], r[7:15]))
        out.append(block("light", r[0], row, f"{NAME}'s {'global ' if not any(r[2:5]) else ''}light (MoP's)"))
    with open(os.path.join(dbc_dir, f"{TAG}_light.sql"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(HEADER + "\n".join(out))

    wanted = {p for r in lights for p in r[7:15] if p and p not in stock_params}
    # params the modpak's other map already writes (F-137's island and dungeon share retail's 4414) are left to it
    own = set()
    for f in glob.glob(os.path.join(dbc_dir, "*lightparams.sql")):
        if TAG not in os.path.basename(f):
            own |= {int(i) for i in re.findall(r"INSERT INTO `lightparams` SET\s*`id` = (\d+)", open(f, encoding="utf-8").read())}
    wanted = sorted(wanted - own)
    taken = taken_ids(modpaks_dir, "lightparams", TAG) - own
    if set(wanted) & taken:
        sys.exit(f"light params {sorted(set(wanted) & taken)} are taken")
    out_p, out_i, out_f = [], [], []
    for pid in wanted:
        r = params.get(pid)
        keys = sorted(data[pid], key=lambda k: k[2])[:16]
        if not r or not keys:
            sys.exit(f"MoP has no light params / data {pid}")
        out_p.append(block("lightparams", pid, {
            "id": pid, "higlight_sky": r[1], "skybox_id": 0, "cloud_type": r[3], "glow": f32(r[4]),
            "water_shallow_alpha": f32(r[5]), "water_deep_alpha": f32(r[6]), "ocean_shallow_alpha": f32(r[7]),
            "ocean_deep_alpha": f32(r[8])}, f"MoP light params {pid}"))
        times = [k[2] for k in keys] + [0] * (16 - len(keys))
        for band, col in enumerate(INT_BANDS):
            bid = pid * 18 - 17 + band
            row = {"id": bid, "num_entries": len(keys)}
            row.update({f"time_value_{i + 1}": t for i, t in enumerate(times)})
            values = [k[col] & 0xFFFFFF for k in keys] + [0] * (16 - len(keys))
            row.update({f"colour_value_{i + 1}": v for i, v in enumerate(values)})
            out_i.append(block("lightintband", bid, row, f"params {pid} band {band}"))
        for band in range(6):
            bid = pid * 6 - 5 + band
            if band in FLOAT_BANDS:
                n, ts, values = len(keys), times, [f32(k[FLOAT_BANDS[band]]) for k in keys]
            else:
                n, ts, values = 1, [0] * 16, [FLOAT_STOCK[band]]
            row = {"id": bid, "num_entries": n}
            row.update({f"time_value_{i + 1}": t for i, t in enumerate(ts)})
            row.update({f"float_value_{i + 1}": v for i, v in enumerate(values + [0.0] * (16 - len(values)))})
            out_f.append(block("lightfloatband", bid, row, f"params {pid} float band {band}"))
    for table, rows in (("lightparams", out_p), ("lightintband", out_i), ("lightfloatband", out_f)):
        with open(os.path.join(dbc_dir, f"{TAG}_{table}.sql"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(HEADER + "\n".join(rows))
    print(f"{len(lights)} lights, {len(out_p)} light params from MoP's LightData")


# (table, its AreaTable field in 5.4.8, the AreaTable column 3.3.5a has it in, the table's SoundEntries fields)
MUSIC = (("soundambience", 8, "ambience", (1, 2)), ("zonemusic", 9, "zone_music", (6, 7)),
         ("zoneintromusictable", 11, "zone_music_intro", (2,)))
MUSIC_COLUMNS = {"soundambience": ("id", "sound_entry_id_day", "sound_entry_id_night"),
                 "zonemusic": ("id", "name", "silence_min_day", "silence_min_night", "silence_max_day",
                               "silence_max_night", "day_music", "night_music"),
                 "zoneintromusictable": ("id", "name", "sound_id", "priority", "min_delay_minutes")}


def write_music(mop_dbc, stock_dbc, modpaks_dir, dbc_dir, rows, TAG, NAME):
    """MoP's ambience, zone music and intro music of the map's areas, with the SoundEntries they play (files named
    through the community listfile, downloaded into WHE-common by zep_goblin_sounds.py --sql). Returns
    {area id: {areatable column: id}}."""
    from mop_wandering_isle_port import MopSounds
    sounds = MopSounds()
    out = collections.defaultdict(dict)
    for table, field, column, sound_fields in MUSIC:
        dbc_name = {"soundambience": "SoundAmbience", "zonemusic": "ZoneMusic",
                    "zoneintromusictable": "ZoneIntroMusicTable"}[table]
        mop, stock = Dbc(os.path.join(mop_dbc, dbc_name + ".dbc")), Dbc(os.path.join(stock_dbc, dbc_name + ".dbc"))
        taken = taken_ids(modpaks_dir, table, TAG)
        written = {}
        for r in rows:
            mid = r[field]
            src = mop.get(mid) if mid > 0 else None
            if not src:
                continue
            if mid not in written:
                row = list(src)
                s = stock.get(mid)
                if mid in taken or s and [s[i] for i in sound_fields] == [row[i] for i in sound_fields]:
                    written[mid] = None     # stock's row, or F-010's (Open Azeroth keeps Cataclysm's ids and rows)
                elif s:
                    sys.exit(f"{table} {mid} is a different row in stock")
                elif not any(sounds.sound(row[i]) for i in sound_fields):
                    written[mid] = 0                        # no file the listfile names
                else:
                    for i in sound_fields:
                        row[i] = sounds.sound(row[i])
                    cols = dict(zip(MUSIC_COLUMNS[table], row))
                    if "name" in cols:
                        cols["name"] = mop.s(row[1])
                    written[mid] = block(table, mid, cols, f"{NAME}: {cols.get('name', mid)} (MoP's)")
            if written[mid] != 0:
                out[r[0]][column] = mid
        with open(os.path.join(dbc_dir, f"{TAG}_{table}.sql"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(HEADER + "\n".join(b for b in written.values() if b))
    # sounds another modpak writes are left to it: F-010 has Cataclysm's ambience under the same ids (as .wav names,
    # which the client opens as .ogg); F-133 and F-134 share theirs, each writing the rows it uses
    other = set()
    for f in glob.glob(os.path.join(modpaks_dir, "*", "dbc", "*soundentries.sql")):
        if not re.search(r"\[F-13[34]\]", os.path.basename(f)):
            other |= {int(m[0] or m[1]) for m in re.findall(r"INSERT INTO `soundentries` \([^)]*\) VALUES \((\d+)|"
                                                            r"INSERT INTO `soundentries` SET\s*`id` = (\d+)",
                                                            open(f, encoding="utf-8").read())}
    entries = {k: v for k, v in sounds.out.get("soundentries", {}).items() if k not in other}
    with open(os.path.join(dbc_dir, f"{TAG}_music_soundentries.sql"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(HEADER + f"-- The files {NAME}'s music and ambience play (5.4.8 SoundEntries)\n\n" + "\n".join(
            block("soundentries", k, c, comment) for k, (c, comment) in sorted(entries.items())))
    print(f"music for {len(out)} areas, {len(entries)} sound entries")
    return out


def apply_music(path, music):
    """Sets the areatable SQL's ambience / zone_music / zone_music_intro to write_music's ids (area bits stay)."""
    text = open(path, encoding="utf-8").read()

    def area(m):
        cols = music.get(int(m.group(1)), {})
        return re.sub(r"`(ambience|zone_music|zone_music_intro)` = \d+",
                      lambda c: "`%s` = %d" % (c.group(1), cols.get(c.group(1), 0)), m.group(0))
    text = re.sub(r"INSERT INTO `areatable` SET\s*`id` = (\d+),.*?;\n", area, text, flags=re.S)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for a in ("mop_dbc", "stock_dbc", "areatable_csv", "adt_dir", "modpaks_dir", "modpak"):
        p.add_argument(a)
    p.add_argument("--map", type=int, default=870)
    p.add_argument("--tag", default="F-133")
    p.add_argument("--directory", default="HawaiiMainLand")
    p.add_argument("--name", default="Pandaria")
    p.add_argument("--tele-base", type=int, default=87000)
    p.add_argument("--move-continents", action="store_true")
    p.add_argument("--uimap", help="MoP Classic's UiMapAssignment CSV (wago.tools): continent placement for its art")
    p.add_argument("--lights-only", action="store_true")
    p.add_argument("--graveyards-only", action="store_true")
    p.add_argument("--tele-only", action="store_true")
    p.add_argument("--music-only", action="store_true")
    p.add_argument("--dungeon", nargs=3, type=float, metavar=("CORPSE_MAP", "X", "Y"),
                   help="a 5-player dungeon (instance type 1) whose ghosts go to (X, Y) on CORPSE_MAP")
    a = p.parse_args()
    MAP, TAG, NAME = a.map, f"[{a.tag}]", a.name
    if a.lights_only:
        return write_lights(a.mop_dbc, a.stock_dbc, a.modpaks_dir, os.path.join(a.modpak, "dbc"), MAP, TAG, NAME)
    if a.graveyards_only:
        return write_graveyards(a.mop_dbc, a.modpaks_dir, os.path.join(a.modpak, "sql", "db-world", "base"), MAP, TAG,
                                NAME)
    mop_map = Dbc(os.path.join(a.mop_dbc, "Map.dbc")).get(MAP)
    mop = Dbc(os.path.join(a.mop_dbc, "AreaTable.dbc"))
    stock = Dbc(os.path.join(a.stock_dbc, "AreaTable.dbc"))
    names = {int(r["ID"]): r["AreaName_lang"] for r in csv.DictReader(open(a.areatable_csv, encoding="utf-8"))}
    rows = sorted((r for r in mop.records if r[1] == MAP), key=lambda r: r[0])
    if a.tele_only:
        return write_tele(rows, names, a.adt_dir, os.path.join(a.modpak, "sql", "db-world", "base"), a.tele_base,
                          MAP, TAG, NAME)
    if a.music_only:
        dbc_dir = os.path.join(a.modpak, "dbc")
        return apply_music(os.path.join(dbc_dir, f"{TAG}_areatable.sql"),
                           write_music(a.mop_dbc, a.stock_dbc, a.modpaks_dir, dbc_dir, rows, TAG, NAME))
    clash = [r[0] for r in rows if r[0] in stock.rows]
    if clash:
        sys.exit(f"stock AreaTable already has ids {clash}")
    taken = used_bits(stock, a.modpaks_dir, os.path.basename(os.path.normpath(a.modpak)), TAG)
    free = (b for b in range(1, MAX_BITS) if b not in taken)

    dbc_dir = os.path.join(a.modpak, "dbc")
    sql_dir = os.path.join(a.modpak, "sql", "db-world", "base")
    os.makedirs(dbc_dir, exist_ok=True)
    os.makedirs(sql_dir, exist_ok=True)

    with open(os.path.join(dbc_dir, f"{TAG}_map.sql"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(HEADER + block("map", MAP, {
            "id": MAP, "directory": a.directory, "instance_type": 1 if a.dungeon else 0, "flags": 0, "pvp": 0,
            "name_enus": NAME, "name_flags": 16712190, "area_table_id": 0,
            "desc_0_enus": "", "desc_0_flags": 16712188, "desc_1_enus": "", "desc_1_flags": 16712188,
            "loading_screen_id": 3, "minimap_icon_scale": 1.0,
            "corpse_map_id": int(a.dungeon[0]) if a.dungeon else -1, "corpse_x": a.dungeon[1] if a.dungeon else 0.0,
            "corpse_y": a.dungeon[2] if a.dungeon else 0.0, "time_override": mop_map[14], "expansion": 2,
            "raid_offset": 0, "max_players": 5 if a.dungeon else 0},
            f"{NAME} (Mists of Pandaria's map {MAP})"))

    out, zones = [], {}
    for r in rows:
        name = names.get(r[0])
        if name is None:
            sys.exit(f"area {r[0]} isn't in {a.areatable_csv}")
        bit = next(free)
        if r[2] == 0:
            zones[r[0]] = name
        out.append(block("areatable", r[0], {
            "id": r[0], "map_id": MAP, "zone_id": r[2], "area_bit": bit, "flags": (r[4] & 0xFFFFFFFF) | FLYABLE,
            "sound_provider_pref": 0, "sound_provider_pref_underwater": 0, "ambience": 0, "zone_music": 0,
            "zone_music_intro": 0, "exploration_level": min(max(r[12], 0), 80), "name_enus": name,
            "name_flags": 16712190, "faction_group": r[14], "liquid_type_1": 0, "liquid_type_2": 0,
            "liquid_type_3": 0, "liquid_type_4": 0, "min_elevation": f32(r[19]), "light_ambient_multiplier": f32(r[20]),
            "light_id": 0}, f"{name} (MoP area bit {r[3]})"))
    with open(os.path.join(dbc_dir, f"{TAG}_areatable.sql"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(HEADER + "\n".join(out))
    apply_music(os.path.join(dbc_dir, f"{TAG}_areatable.sql"),
                write_music(a.mop_dbc, a.stock_dbc, a.modpaks_dir, dbc_dir, rows, TAG, NAME))

    write_lights(a.mop_dbc, a.stock_dbc, a.modpaks_dir, dbc_dir, MAP, TAG, NAME)
    write_graveyards(a.mop_dbc, a.modpaks_dir, sql_dir, MAP, TAG, NAME)

    # World map: the continent and its zones (not the shrines' dungeon floors or Krasarang's phase copy), so the
    # client can place the player (GetPlayerMapPosition, addons' coordinates) and draw the map.
    wma = Dbc(os.path.join(a.mop_dbc, "WorldMapArea.dbc"))
    out, kept = [], set()
    for r in wma.records:
        if r[1] != MAP or r[9] or r[10] not in (0, -1) or (r[2] and r[2] not in zones):
            continue
        kept.add(r[0])
        out.append(block("worldmaparea", r[0], {
            "id": r[0], "map_id": MAP, "area_id": r[2], "area_name": wma.s(r[3]), "loc_left": f32(r[4]),
            "loc_right": f32(r[5]), "loc_top": f32(r[6]), "loc_bottom": f32(r[7]), "display_map_id": r[8],
            "default_dungeon_floor": 0, "parent_world_map_id": 0}, zones.get(r[2], NAME)))
    with open(os.path.join(dbc_dir, f"{TAG}_worldmaparea.sql"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(HEADER + "\n".join(out))
    # Explored-area overlays of those maps. MoP's hit rectangles are 0 (it no longer used them); 3.3.5 shows a
    # subzone's name while the cursor is in its rectangle, so they get the overlay's own.
    wmo = Dbc(os.path.join(a.mop_dbc, "WorldMapOverlay.dbc"))
    out = []
    for r in wmo.records:
        if r[1] not in kept:
            continue
        w, h, x, y = r[7:11]
        out.append(block("worldmapoverlay", r[0], {
            "id": r[0], "map_area_id": r[1], "area_id_1": r[2], "area_id_2": r[3], "area_id_3": r[4],
            "area_id_4": r[5], "map_point_x": 0, "map_point_y": 0, "texture_name": wmo.s(r[6]), "texture_width": w,
            "texture_height": h, "offset_x": x, "offset_y": y, "hit_rect_top": y, "hit_rect_left": x,
            "hit_rect_bottom": y + h, "hit_rect_right": x + w}, wmo.s(r[6])))
    with open(os.path.join(dbc_dir, f"{TAG}_worldmapoverlay.sql"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(HEADER + "\n".join(out))

    continents = Dbc(os.path.join(a.mop_dbc, "WorldMapContinent.dbc")).records
    wmc = next((r for r in continents if r[1] == MAP), None)
    if wmc:
        # (left, right, top, bottom, offset x, offset y, scale) per map: 5.4.8's rows, or with --uimap MoP Classic's,
        # whose World map art and continent highlights are drawn for UiMapAssignment regions: 5.4.8's tile
        # boundaries size the highlights wrongly (Kalimdor's came out a third too small)
        place = {r[1]: (r[2], r[3], r[4], r[5], f32(r[6]), f32(r[7]), f32(r[8])) for r in continents}
        if a.uimap:
            place.update(uimap_placement(a.uimap))
        # MoP's World map art (WHE-common's patch-MoP.MPQ) places the other continents differently from Open
        # Azeroth's, and their clickable rectangles on the World map come from these rows. Outland's is the same.
        moved = ["\n-- MoP's placement of the other continents on the World map, to match MoP's World map art"]
        for m in (0, 1, 571):
            if a.move_continents and m in place:
                L, R, T, B, ox, oy, sc = place[m]
                moved.append(f"UPDATE `worldmapcontinent` SET `left_boundary` = {L}, `right_boundary` = {R}, "
                             f"`top_boundary` = {T}, `bottom_boundary` = {B}, `continent_offset_x` = "
                             f"{ox}, `continent_offset_y` = {oy}, `scale` = {sc} "
                             f"WHERE `map_id` = {m};")
        L, R, T, B, ox, oy, sc = place[MAP]
        with open(os.path.join(dbc_dir, f"{TAG}_worldmapcontinent.sql"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(HEADER + block("worldmapcontinent", wmc[0], {
                "id": wmc[0], "map_id": MAP, "left_boundary": L, "right_boundary": R,
                "top_boundary": T, "bottom_boundary": B, "continent_offset_x": ox,
                "continent_offset_y": oy, "scale": sc, "taxi_min_x": f32(wmc[9]),
                "taxi_min_y": f32(wmc[10]), "taxi_max_x": f32(wmc[11]), "taxi_max_y": f32(wmc[12]),
                "world_map_id": wmc[13]}, NAME) + ("\n".join(moved) + "\n" if len(moved) > 1 else ""))

    write_tele(rows, names, a.adt_dir, sql_dir, a.tele_base, MAP, TAG, NAME)
    print(f"{len(rows)} areas, {len(zones)} zones")


def write_tele(rows, names, adt_dir, sql_dir, tele_base, MAP, TAG, NAME):
    by_area = collections.defaultdict(list)
    for c in chunks(adt_dir):
        by_area[c[0]].append(c)
    tele, seen = [f"DELETE FROM `game_tele` WHERE `map` = {MAP};"], set()
    for i, r in enumerate(rows):
        cs = by_area.get(r[0])
        name = names[r[0]].replace(" ", "").replace(chr(39), "")
        if not cs or name in seen:
            continue
        seen.add(name)
        mx, my = sum(c[1] for c in cs) / len(cs), sum(c[2] for c in cs) / len(cs)
        land = [c for c in cs if not c[4]] or cs
        _, x, y, zz, _ = min(land, key=lambda c: (c[1] - mx) ** 2 + (c[2] - my) ** 2)
        tele.append(f"INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, "
                    f"`name`) VALUES ({tele_base + i}, {x:.1f}, {y:.1f}, {zz + 2:.1f}, 0, {MAP}, '{name}');")
    with open(os.path.join(sql_dir, f"{TAG}_game_tele.sql"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(HEADER + f"-- .tele targets for {NAME}'s zones and subareas\n" + "\n".join(tele) + "\n")
    print(f"{len(tele) - 1} tele targets")


if __name__ == "__main__":
    main()

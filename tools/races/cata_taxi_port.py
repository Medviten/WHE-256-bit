#!/usr/bin/env python3
"""Cataclysm's flight paths on Open Azeroth's world (F-139_cata-flight-paths), from the 4.0.6a client DBCs and Project
Neltharion's 4.3.4 world database.

  python -I cata_taxi_port.py extract WORLD_SQL EXTRACT_DIR [--base-dbc DIR]
  python -I cata_taxi_port.py port EXTRACT_DIR MODPAK_DIR [--base-dbc DIR]

WORLD_SQL is Neltharion's `source/sql/base/world.zip` unpacked (as for F-130). --base-dbc is a built client DBC folder
with every other modpak in it (default: the test client's 256-bit realm patch); its ids count as taken.

Open Azeroth's Eastern Kingdoms and Kalimdor are Cataclysm's terrain, so Cataclysm's taxi nodes stand on it. Which ones:
- the 4.0.6a TaxiNodes of maps 0 and 1 with a mount, without quest, test and transport nodes (NOT_A_NODE)
- a node stock (or another modpak) already has at the same spot (within SAME_SPOT) is that node: the stock network stays
  as it is. Nodes Open Azeroth (F-010) ported from Cataclysm under other ids (Vashj'ir, Surwich) map onto those
- a stock node Cataclysm moved by less than MOVED (Sentinel Hill, Orgrimmar, Gadgetzan, ...) stays where stock has it;
  Cataclysm's paths to and from it get the stock spot as their first or last point
- every other node is new and keeps its Cataclysm id unless something here has it already
- a new node needs a flight master: Neltharion's flight masters (npcflag 8192) within FM_RANGE of it. Nodes without one
  are left out
Paths: Cataclysm's TaxiPath rows (and their TaxiPathNode points) with a new node at one end and a node here at the
other, unless the pair is connected already. Path ids are new where taken; point ids are given when the SQL runs; points' events are dropped.
Mounts that AzerothCore has no creature for become the stock wind rider (Horde) or gryphon (Alliance).

The flight masters are ported by cata_gilneas_port.py's Port (templates, models, Cataclysm displays with their NPC
bakes, equipment, gossip), at their Neltharion spots. Levels above 80 go down by 10. A gossip menu without a taxi
option gets one; flight masters without a menu get stock's (4342, "I need a ride."). Stock flight masters keep their
stock templates.

Node ids past 448 need the core patch (patches/core/taxi-mask-size.patch): AzerothCore's masks stop at 448 nodes."""
import argparse, collections, json, math, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cata_gilneas_port as g  # noqa: E402
import cata_zone_extract as ze  # noqa: E402
import cata406_dbc_port as c406  # noqa: E402

TAG = "F-139"
BASE_DBC = r"C:\Users\Medviten\Desktop\WowSquished-256-bit\Data\patch-WHE.256-bit.MPQ\DBFilesClient"
AC_WORLD = r"D:\GitHub\azerothcore-wotlk-256-bit\data\sql\base\db_world"
MAPS = (0, 1)
NOT_A_NODE = ("Quest", "DISABLED", "Test", "Filming", "Flavor", "Generic", "Prologue", "NEVER", "Ebon Hold",
              "Transport", "4.x")
SAME_SPOT, MOVED, FM_RANGE = 50.0, 400.0, 60.0
HORDE_MOUNT, ALLIANCE_MOUNT = 2224, 541
FALLBACK_MENU = 4342                     # stock "I need a ride."
TAXI_OPTION = 4                          # gossip option type: taxi
NPCFLAG_MASK = 0x3FFFFFF                 # 3.3.5a's npc flags
CREATURE_GUID = 13950001
MENU_BASE = TEXT_BASE = 1390000
PATH_BASE = 13950000


def dist(a, b):
    return math.dist(a, b)


class Taxi:
    """Which Cataclysm nodes and paths come in, under which ids."""

    def __init__(self, base_dbc):
        cd = c406.Dbc(os.path.join(g.CATA_DBC, "TaxiNodes.dbc"))
        bd = c406.Dbc(os.path.join(base_dbc, "TaxiNodes.dbc"))
        self.cata_paths = c406.Dbc(os.path.join(g.CATA_DBC, "TaxiPath.dbc"))
        self.cata_points = c406.Dbc(os.path.join(g.CATA_DBC, "TaxiPathNode.dbc"))
        base_paths = c406.Dbc(os.path.join(base_dbc, "TaxiPath.dbc"))
        self.base_pairs = {(r[1], r[2]) for r in base_paths.records}
        self.taken_paths = {r[0] for r in base_paths.records}
        pos = lambda r: tuple(c406.f32(v) for v in r[2:5])
        self.base = {r[0]: (r[1], pos(r)) for r in bd.records}
        self.cata = {}                       # Cataclysm id -> (map, pos, name, mounts)
        for r in cd.records:
            name = cd.s(r[5])
            if r[1] in MAPS and (r[6] or r[7]) and not any(k in name for k in NOT_A_NODE):
                self.cata[r[0]] = (r[1], pos(r), name, (r[6], r[7]))
        self.node, self.moved, self.new = {}, {}, {}   # Cataclysm id -> id here; moved: -> stock spot; new: -> id
        for cid, (m, p, name, _) in sorted(self.cata.items()):
            here = self.base.get(cid)
            if here and here[0] == m and dist(here[1], p) < SAME_SPOT:
                self.node[cid] = cid
                continue
            same = [i for i, (bm, bp) in sorted(self.base.items()) if bm == m and dist(bp, p) < 15]
            if same:
                self.node[cid] = same[0]
            elif here and here[0] == m and dist(here[1], p) < MOVED:
                self.node[cid] = cid
                self.moved[cid] = here[1]
            else:
                self.new[cid] = None

    def assign(self, keep):
        """Ids for the new nodes in keep (the ones with a flight master); the rest are dropped."""
        self.new = {c: None for c in self.new if c in keep}
        taken = set(self.base) | {c for c in self.new if c not in self.base}
        free = (i for i in range(1, 2049) if i not in taken)
        for c in sorted(self.new):
            self.new[c] = c if c not in self.base else next(free)
        self.node.update(self.new)

    def paths(self):
        """(path id, from, to, cost, points) for the paths that come in; points are TaxiPathNode rows."""
        points = collections.defaultdict(list)
        for r in self.cata_points.records:
            points[r[1]].append(r)
        out, pairs = [], set(self.base_pairs)
        next_id = max(self.taken_paths | {r[0] for r in self.cata_paths.records}) + 1
        for r in sorted(self.cata_paths.records):
            a, b = r[1], r[2]
            if not (a in self.new or b in self.new) or a not in self.node or b not in self.node:
                continue
            pair = (self.node[a], self.node[b])
            if pair in pairs or not points[r[0]]:
                continue
            pairs.add(pair)
            pid = r[0]
            if pid in self.taken_paths:
                pid, next_id = next_id, next_id + 1
            self.taken_paths.add(pid)
            pts = [(p[3], c406.f32(p[4]), c406.f32(p[5]), c406.f32(p[6]), p[7], p[8])
                   for p in sorted(points[r[0]], key=lambda p: p[2])]
            m = pts[0][0]
            if a in self.moved:
                pts.insert(0, (m,) + self.moved[a] + (0, 0))
            if b in self.moved:
                pts.append((m,) + self.moved[b] + (0, 0))
            out.append((pid, pair[0], pair[1], r[3], pts))
        return out


def ac_entries():
    out = set()
    for line in open(os.path.join(AC_WORLD, "creature_template.sql"), encoding="utf-8"):
        m = re.match(r"\((\d+),", line)
        if m:
            out.add(int(m.group(1)))
    return out


def ac_spawns(entries):
    """Stock spawns of these entries: (entry, map, x, y, z)."""
    out = []
    for line in open(os.path.join(AC_WORLD, "creature.sql"), encoding="utf-8"):
        # guid, id1, id2, id3, map, zoneId, areaId, spawnMask, phaseMask, equipment_id, x, y, z
        m = re.match(r"\(\d+,(\d+),\d+,\d+,(\d+),\d+,\d+,\d+,\d+,-?\d+,(-?[\d.]+),(-?[\d.]+),(-?[\d.]+),", line)
        if m and int(m.group(1)) in entries:
            out.append((int(m.group(1)), int(m.group(2)), float(m.group(3)), float(m.group(4)), float(m.group(5))))
    return out


# ---- extract -------------------------------------------------------------------------------------------------------
def extract(world_sql, out, base_dbc):
    taxi = Taxi(base_dbc)
    tables = ze.read_dump(world_sql, set(MAPS))
    T = tables
    fms = {r["entry"]: r for r, _ in T["creature_template"].rows() if (r["npcflag"] or 0) & 8192}
    keep = collections.defaultdict(dict)
    spawns = [(r, line) for r, line in T["creature"].rows() if r["id"] in fms]
    nodes = {}
    for r, line in spawns:
        p = (r["position_x"], r["position_y"], r["position_z"])
        near = [c for c in taxi.new if taxi.cata[c][0] == r["map"] and dist(taxi.cata[c][1], p) < FM_RANGE]
        if near:
            keep["creature"][line] = r
            nodes.setdefault(min(near, key=lambda c: dist(taxi.cata[c][1], p)), []).append(r["id"])
    stock = ac_entries()
    entries = {r["id"] for r in keep["creature"].values()}
    # stock flight masters stock already spawns at the spot: nothing to add
    there = ac_spawns(entries & stock)
    for line, r in list(keep["creature"].items()):
        if r["id"] in stock and any(e == r["id"] and m == r["map"] and dist((x, y, z), (
                r["position_x"], r["position_y"], r["position_z"])) < FM_RANGE for e, m, x, y, z in there):
            del keep["creature"][line]
    entries = {r["id"] for r in keep["creature"].values()}
    guids = {r["guid"] for r in keep["creature"].values()}
    new_entries = entries - stock
    take = lambda t, pred: keep[t].update({line: r for r, line in T[t].rows() if pred(r)})
    take("creature_template", lambda r: r["entry"] in new_entries)
    take("creature_template_addon", lambda r: r["entry"] in new_entries)
    take("creature_addon", lambda r: r["guid"] in guids)
    equips = {r["equipment_id"] for r in keep["creature_template"].values()} | {r["equipment_id"] for r in keep["creature"].values()}
    take("creature_equip_template", lambda r: r["entry"] in equips)
    menus = {r["gossip_menu_id"] for r in keep["creature_template"].values()} - {0}
    take("gossip_menu", lambda r: r["entry"] in menus)
    take("gossip_menu_option", lambda r: r["menu_id"] in menus)
    texts = {r["text_id"] for r in keep["gossip_menu"].values()}
    take("npc_text", lambda r: r["ID"] in texts)
    displays = {r["modelid%d" % i] for r in keep["creature_template"].values() for i in range(1, 5)}
    take("creature_model_info", lambda r: r["modelid"] in displays)
    ze.write(tables, keep, {"nodes with a flight master": set(nodes), "stock flight masters": entries & stock,
                            "nodes without one": set(taxi.new) - set(nodes)}, out)
    json.dump({str(c): sorted(set(e)) for c, e in nodes.items()}, open(os.path.join(out, "nodes.json"), "w"), indent=1)
    print("%d of %d new nodes have a flight master: %d templates (%d stock), %d spawns"
          % (len(nodes), len(taxi.new), len(entries), len(entries & stock), len(keep["creature"])))
    print("without: %s" % ", ".join("%d %s" % (c, taxi.cata[c][2]) for c in sorted(set(taxi.new) - set(nodes))))


# ---- port ----------------------------------------------------------------------------------------------------------
class Port(g.Port):
    def __init__(self, extract_dir, dest, stock_fms):
        super().__init__(extract_dir, dest)
        for r in self.t["creature_template"]:
            r["npcflag"] &= NPCFLAG_MASK
            for k in ("minlevel", "maxlevel"):
                if r[k] > 80:
                    r[k] -= 10
            if r["gossip_menu_id"] not in self.menu:
                r["gossip_menu_id"] = 0
        self.stock_fms = stock_fms

    def gossip(self):
        super().gossip()
        # menus without a taxi option get one; flight masters with no menu get stock's
        opts = collections.defaultdict(list)
        for r in self.t["gossip_menu_option"]:
            opts[r["menu_id"]].append(r)
        add = [[self.menu[m], max([o["id"] for o in opts[m]], default=-1) + 1, 2, "I need a ride.", 3409, TAXI_OPTION,
                8192, 0, 0, 0, 0, "", 0] for m in sorted(self.menu) if not any(o["option_id"] == TAXI_OPTION
                                                                             for o in opts[m])]
        self.write("28_gossip_taxi_option", g.insert(
            "gossip_menu_option", "MenuID OptionID OptionIcon OptionText OptionBroadcastTextID OptionType OptionNpcFlag "
            "ActionMenuID ActionPoiID BoxCoded BoxMoney BoxText BoxBroadcastTextID".split(), add, None,
            "Menus whose Cataclysm taxi option was TrinityCore's default menu"))
        fallback = sorted(r["entry"] for r in self.t["creature_template"] if not r["gossip_menu_id"])
        if fallback:
            self.write("29_gossip_fallback", "UPDATE `creature_template` SET `gossip_menu_id` = %d WHERE `entry` IN %s;\n"
                       % (FALLBACK_MENU, g.in_list(fallback)))

    def spawns(self):
        c, a = [], []
        for r in sorted(self.t["creature"], key=lambda r: r["guid"]):
            if r["id"] not in self.known_creatures:
                continue
            q = r["equipment_id"]
            eq = 0 if q < 0 or r["id"] in self.stock_fms else (self.equip_ids.get((r["id"], q), 0) if q > 0 else
                                                                (1 if any(k[0] == r["id"] for k in self.equip_ids) else 0))
            c.append([self.cguid[r["guid"]], r["id"], r["map"], 0, 0, 1, 1, eq, r["position_x"], r["position_y"],
                      r["position_z"], r["orientation"], r["spawntimesecs"], 0, 0, 1, 0, 0, 0, 0, 0, "", 0, 1,
                      "[gen %s flight master]" % TAG])
        for r in self.t["creature_addon"]:
            guid = self.cguid.get(r["guid"])
            if guid:
                a.append([guid, 0, r["mount"], r["bytes1"], r["bytes2"], r["emote"], 0,
                          self.auras(r["auras"], "spawn %d" % r["guid"]), ""])
        self.write("40_creature", g.insert(
            "creature", "guid id map zoneId areaId spawnMask phaseMask equipment_id position_x position_y position_z "
            "orientation spawntimesecs wander_distance currentwaypoint curhealth curmana MovementType npcflag "
            "unit_flags dynamicflags ScriptName VerifiedBuild CreateObject Comment".split(), c,
            "DELETE FROM `creature` WHERE `Comment` LIKE '[gen %s%%';" % TAG))
        self.write("41_creature_addon", g.insert(
            "creature_addon", "guid path_id mount bytes1 bytes2 emote visibilityDistanceType auras Comment".split(), a,
            "DELETE FROM `creature_addon` WHERE `guid` BETWEEN %d AND %d;" % (CREATURE_GUID, CREATURE_GUID + 9999)))

    def taxi(self, taxi):
        stock = ac_entries()
        nodes, paths, points = [], [], []
        for c, i in sorted(taxi.new.items(), key=lambda x: x[1]):
            m, p, name, mounts = taxi.cata[c]
            h, al = (x if not x or x in stock else (HORDE_MOUNT, ALLIANCE_MOUNT)[n] for n, x in enumerate(mounts))
            nodes.append(dict(id=i, map=m, x=round(p[0], 4), y=round(p[1], 4), z=round(p[2], 4), name_enus=name,
                              name_flags=16712190, mount_creature_id_1=h, mount_creature_id_2=al))
        for pid, a, b, cost, pts in taxi.paths():
            paths.append(dict(id=pid, from_taxi_node=a, to_taxi_node=b, cost=cost))
            for n, (m, x, y, z, flags, delay) in enumerate(pts):
                points.append((pid, n, m, round(x, 4), round(y, 4), round(z, 4), flags, delay))
        known = set(taxi.base) | {n["id"] for n in nodes}
        assert all(n["id"] <= 2048 for n in nodes), "node ids past the patched core's masks"
        assert all(p["from_taxi_node"] in known and p["to_taxi_node"] in known for p in paths), "path to a missing node"
        assert len({(p["from_taxi_node"], p["to_taxi_node"]) for p in paths} | taxi.base_pairs) == \
            len(paths) + len(taxi.base_pairs), "a pair connected twice"
        self.write_dbc("taxinodes", nodes, "Cataclysm's taxi nodes (4.0.6a) Open Azeroth's world has none for")
        self.write_dbc("taxipath", paths, "Cataclysm's flight paths (4.0.6a) to and from them")
        # point ids after the highest one there when the SQL runs (as F-006 does): no clash with other modpaks' points
        self.files[os.path.join("dbc", "[%s]_taxipathnode.sql" % TAG)] = (
            "-- The points of those paths; a stock node Cataclysm moved keeps its spot, as the first or last point.\n\n"
            "DELETE FROM `taxipathnode` WHERE `path_id` IN %s;\n"
            "SET @TaxiPathNodeID = (SELECT COALESCE(MAX(id), 0) FROM `taxipathnode`);\n"
            "INSERT INTO `taxipathnode` (`id`, `path_id`, `node_index`, `map`, `x`, `y`, `z`, `flags`, `delay`, "
            "`arrival_event_id`, `departure_event_id`) VALUES\n%s;\n" % (
                g.in_list(p["id"] for p in paths),
                ",\n".join("  (@TaxiPathNodeID := @TaxiPathNodeID + 1, %d, %d, %d, %s, %s, %s, %d, %d, 0, 0)" % q
                           for q in points)))
        return len(nodes), len(paths), len(points)

    def run(self, taxi):
        self.trainers, self.faction_templates, self.bakes = [], set(), set()
        self.creatures()
        self.spawns()
        self.gossip()
        self.client_rows()
        counts = self.taxi(taxi)
        for name, sql in self.files.items():
            path = os.path.join(self.dest, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf8", newline="\n") as f:
                f.write("-- Generated by tools/races/cata_taxi_port.py: change the script, not this file.\n\n"
                        + sql.replace("cata_gilneas_port.py", "cata_taxi_port.py"))
        with open(os.path.join(self.x, "bakes.txt"), "w", encoding="utf8", newline="\n") as f:
            f.write("".join("Textures\\BakedNpcTextures\\%s\n" % b for b in sorted(self.bakes)))
        print("%d nodes, %d paths, %d points; %d flight masters, %d items, %d item displays, %d bakes (bakes.txt in the extract)" % (
            counts + (len(self.entries), sum(1 for v in self.item_ids.values() if v), len(self.items.added),
                      len(self.bakes))))
        for k, v in sorted(g.dropped.items()):
            v = sorted(set(map(str, v)))
            print("%s (%d): %s" % (k, len(v), ", ".join(v[:40]) + (" ..." if len(v) > 40 else "")))


def port(extract_dir, dest, base_dbc):
    g.TAG, g.CREATURE_GUID, g.PATH_BASE, g.MENU_BASE, g.TEXT_BASE = TAG, CREATURE_GUID, PATH_BASE, MENU_BASE, TEXT_BASE
    g.FIXES_DIR = os.path.join(HERE, "cata_taxi_fixes")
    taxi = Taxi(base_dbc)
    nodes = {int(c) for c in json.load(open(os.path.join(extract_dir, "nodes.json")))}
    taxi.assign(nodes)
    stock_fms = {r["id"] for r in g.rows(extract_dir, "creature")} - {r["entry"] for r in g.rows(extract_dir, "creature_template")}
    g.STOCK_CREATURES = stock_fms
    for sub in ("dbc", "sql"):
        shutil.rmtree(os.path.join(dest, sub), ignore_errors=True)
    Port(extract_dir, dest, stock_fms).run(taxi)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=("extract", "port"))
    ap.add_argument("source")
    ap.add_argument("out")
    ap.add_argument("--base-dbc", default=BASE_DBC)
    a = ap.parse_args()
    (extract if a.step == "extract" else port)(a.source, a.out, a.base_dbc)


if __name__ == "__main__":
    main()

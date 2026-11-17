#!/usr/bin/env python3
"""Pandaria's herb and ore nodes (F-133) from SkyFire 5.4.8's world database, for AzerothCore 3.3.5a.

  python -I -X utf8 mop_pandaria_nodes.py SFDB_SQL [--modpak modpaks/F-133_mop-pandaria] [--data D:/wow-scratch/wi/db2]

SFDB_SQL is SkyFire's full release (https://github.com/ProjectSkyfire/SkyFire_548/releases, a SQLyog dump: one row per
line). Every chest-type object template whose MoP lock is the herbalism or mining lock and that SkyFire spawns on map
870 is ported (Green Tea Leaf, Silkweed, Rain Poppy, Snow Lily, Fool's Cap, Golden Lotus, Sha-Touched Herb, Ghost
Iron, Kyparite, Trillium):

- gameobject_template: SkyFire's row (MoP's chest fields 0-16) with a stock 3.3.5a lock instead of MoP's (whose skill
  is 0: MoP took the requirement from elsewhere). MoP's nodes want 500-600 skill against WotLK's 450 cap, so the
  requirement (MoP's trivial range start, data23, less 25) maps to 425 below 550 and to 450 from 550 up, on stock locks
  with those values (herbalism 1789 / 1792, mining 1784 / 1785).
- gameobject spawns from guid 13500000, phase mask 1.
- gameobject_loot_template: SkyFire has no loot for these nodes (their loot id is 0), so each node drops its own herb
  or ore (rich ones more), herbs a 2 % Golden Lotus, Ghost Iron a 2 % chance of each Trillium ore. Loot id = entry.
- the MoP items (mop_items.py on the 5.4.8 client's tables, English names from wago's ItemSparse CSV), their Item.dbc
  and ItemDisplayInfo rows; the object displays (GameObjectDisplayInfo) stock lacks.
- MODPAK/wi_assets.txt gets the node models, for tools/models/mop_assets.py to fetch (it reads the item displays'
  icons from the itemdisplayinfo SQL itself)."""
import argparse, collections, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cata_items import sql_value, ITEM_TEMPLATE_COLUMNS, display_sql  # noqa: E402
from cata_gilneas_port import insert, in_list  # noqa: E402
from mop_items import MopItems  # noqa: E402
from mop_wandering_isle_port import MOP_DBC, STOCK_DBC, MODPAKS, dbc_ids, config_range  # noqa: E402
import cata406_dbc_port as c406  # noqa: E402

MAP, TAG = 870, "F-133"
GUID_BASE = 13500000
HERB, MINING = 2, 3                        # LockType indices
LOCKS = {(HERB, 425): 1789, (HERB, 450): 1792, (MINING, 425): 1784, (MINING, 450): 1785}
# node name -> [(item, chance, min, max)]
GOLDEN_LOTUS, BLACK_TRILLIUM, WHITE_TRILLIUM = 72238, 72094, 72103
LOOT = {
    "Green Tea Leaf": [(72234, 100, 1, 3), (GOLDEN_LOTUS, 2, 1, 1)],
    "Silkweed": [(72235, 100, 1, 3), (GOLDEN_LOTUS, 2, 1, 1)],
    "Rain Poppy": [(72237, 100, 1, 3), (GOLDEN_LOTUS, 2, 1, 1)],
    "Snow Lily": [(79010, 100, 1, 3), (GOLDEN_LOTUS, 2, 1, 1)],
    "Fool's Cap": [(79011, 100, 1, 3), (GOLDEN_LOTUS, 2, 1, 1)],
    "Golden Lotus": [(GOLDEN_LOTUS, 100, 1, 2)],
    "Sha-Touched Herb": [(89112, 100, 1, 3), (GOLDEN_LOTUS, 2, 1, 1)],
    "Ghost Iron Deposit": [(72092, 100, 1, 4), (BLACK_TRILLIUM, 2, 1, 1), (WHITE_TRILLIUM, 2, 1, 1)],
    "Rich Ghost Iron Deposit": [(72092, 100, 3, 7), (BLACK_TRILLIUM, 4, 1, 1), (WHITE_TRILLIUM, 4, 1, 1)],
    "Kyparite Deposit": [(72093, 100, 1, 4)],
    "Rich Kyparite Deposit": [(72093, 100, 3, 7)],
    "Trillium Vein": [(BLACK_TRILLIUM, 100, 1, 3), (WHITE_TRILLIUM, 100, 1, 3)],
}


ESCAPES = {"n": "\n", "r": "\r", "t": "\t", "0": "\0"}


def values(text):
    """The values of one SQL row "(...)" as strings (quotes and backslash escapes resolved)."""
    out, i, n = [], 1, len(text)
    while i < n:
        if text[i] == "'":
            j, buf = i + 1, []
            while text[j] != "'":
                if text[j] == "\\":
                    buf.append(ESCAPES.get(text[j + 1], text[j + 1]))
                    j += 2
                else:
                    buf.append(text[j])
                    j += 1
            out.append("".join(buf))
            i = j + 1
        else:
            j = i
            while j < n and text[j] not in ",)":
                j += 1
            out.append(text[i:j].strip())
            i = j
        while i < n and text[i] in " \t":
            i += 1
        if i < n and text[i] == ",":
            i += 1
        elif i < n and text[i] == ")":
            break
    return out


def sfdb(path, tables):
    """{table: [dict]} for the wanted tables of a SkyFire SQLyog dump (one row per line; strings may hold a bare CR,
    so it is split on LF only)."""
    out, table, cols = collections.defaultdict(list), None, []
    for line in open(path, "rb").read().split(b"\n"):
        if line.startswith(b"insert  into"):
            table = line.split(b"`")[1].decode()
            cols = [c.strip().strip(b"`").decode() for c in line[line.index(b"(") + 1:line.index(b")")].split(b",")]
            continue
        if table in tables and line.startswith(b"("):
            out[table].append(dict(zip(cols, values(line.strip().decode("utf8", "replace")))))
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("sfdb")
    p.add_argument("--modpak", default=os.path.join(MODPAKS, "F-133_mop-pandaria"))
    p.add_argument("--data", default="D:/wow-scratch/wi/db2")
    a = p.parse_args()
    db = sfdb(a.sfdb, {"gameobject_template", "gameobject"})
    lock = c406.Dbc(os.path.join(MOP_DBC, "Lock.dbc"))
    spawned = collections.Counter(int(r["id"]) for r in db["gameobject"] if int(r["map"]) == MAP)
    nodes = {}
    for r in db["gameobject_template"]:
        e = int(r["entry"])
        lk = lock.get(int(r["data0"])) if r["type"] == "3" else None
        if e in spawned and lk and lk[1] == 2 and lk[9] in (HERB, MINING):
            if r["name"] not in LOOT:
                print("no loot defined for", e, r["name"], "- skipped")
                continue
            nodes[e] = (r, lk[9])

    items = MopItems(MOP_DBC, STOCK_DBC, os.path.join(a.data, "ItemSparse.csv"), config_range("NextItemDisplayID"))
    stock_items = dbc_ids("Item")
    stock_gdisp = dbc_ids("GameObjectDisplayInfo")
    stock_sounds = dbc_ids("SoundEntries")
    gd = c406.Dbc(os.path.join(MOP_DBC, "GameObjectDisplayInfo.dbc"))

    tmpl, loot, disp, models, item_ids = [], [], [], set(), set()
    for e, (r, kind) in sorted(nodes.items()):
        mop_req = int(r["data23"]) - 25
        lock_id = LOCKS[(kind, 425 if mop_req < 550 else 450)]
        data = [int(float(r["data%d" % i])) for i in range(24)]
        data[0], data[1] = lock_id, e
        data[17:] = [0] * 7                       # MoP-only chest fields (xp level, trivial skill range, ...)
        d = int(r["displayId"])
        if d not in stock_gdisp and d not in {x["id"] for x in disp}:
            x = gd.get(d)
            disp.append(dict(id=d, model_name=gd.s(x[1]), **{"sound_%d" % (i + 1): x[2 + i] if x[2 + i] in stock_sounds
                                                              else 0 for i in range(10)},
                             **dict(zip(("geo_box_min_x", "geo_box_min_y", "geo_box_min_z", "geo_box_max_x",
                                         "geo_box_max_y", "geo_box_max_z"), (c406.f32(v) for v in x[12:18])))))
            models.add(gd.s(x[1]))
        tmpl.append([e, 3, d, r["name"], "", "", "", float(r["size"])] + data + ["", "", 0])
        for item, chance, lo, hi in LOOT[r["name"]]:
            loot.append([e, item, 0, chance, 0, 1, 0, lo, hi, "%s: %s" % (r["name"], items.name(item))])
            item_ids.add(item)

    spawns = []
    for r in sorted(db["gameobject"], key=lambda r: int(r["guid"])):
        if int(r["map"]) == MAP and int(r["id"]) in nodes:
            spawns.append([GUID_BASE + len(spawns), int(r["id"]), MAP, 0, 0, 1, 1] +
                          [float(r[k]) for k in ("position_x", "position_y", "position_z", "orientation", "rotation0",
                                                 "rotation1", "rotation2", "rotation3")] +
                          [int(r["spawntimesecs"]), 255, 1, "", 0, "F-133 Pandaria gathering node"])

    ports = sorted(i for i in item_ids if i not in stock_items)
    itmpl = [items.template(i, i) for i in ports]
    for t in itmpl:
        t["AllowableRace"] = -1
        t["AllowableClass"] = -1

    sql_dir = os.path.join(a.modpak, "sql", "db-world", "base")
    dbc_dir = os.path.join(a.modpak, "dbc")
    head = "-- Generated by tools/races/mop_pandaria_nodes.py from SkyFire 5.4.8's world database: change the script, not this file.\n\n"
    ents = in_list(nodes)
    files = {
        os.path.join(sql_dir, "zz_[AUTO,%s]_nodes_10_item_template.sql" % TAG): insert(
            "item_template", list(ITEM_TEMPLATE_COLUMNS), [[t[c] for c in ITEM_TEMPLATE_COLUMNS] for t in itmpl],
            "DELETE FROM `item_template` WHERE `entry` IN %s;" % in_list(ports), "Pandaria's herbs and ores (MoP items)"),
        os.path.join(sql_dir, "zz_[AUTO,%s]_nodes_20_gameobject_template.sql" % TAG): insert(
            "gameobject_template", ("entry type displayId name IconName castBarCaption unk1 size " +
                                    " ".join("Data%d" % i for i in range(24)) + " AIName ScriptName VerifiedBuild").split(),
            tmpl, "DELETE FROM `gameobject_template` WHERE `entry` IN %s;" % ents),
        os.path.join(sql_dir, "zz_[AUTO,%s]_nodes_30_gameobject_loot_template.sql" % TAG): insert(
            "gameobject_loot_template", "Entry Item Reference Chance QuestRequired LootMode GroupId MinCount MaxCount "
            "Comment".split(), loot, "DELETE FROM `gameobject_loot_template` WHERE `Entry` IN %s;" % ents),
        os.path.join(sql_dir, "zz_[AUTO,%s]_nodes_40_gameobject.sql" % TAG): insert(
            "gameobject", "guid id map zoneId areaId spawnMask phaseMask position_x position_y position_z orientation "
            "rotation0 rotation1 rotation2 rotation3 spawntimesecs animprogress state ScriptName VerifiedBuild "
            "Comment".split(), spawns,
            "DELETE FROM `gameobject` WHERE `guid` BETWEEN %d AND %d;" % (GUID_BASE, GUID_BASE + 99999)),
        os.path.join(dbc_dir, "[%s]_nodes_item.sql" % TAG): insert(
            "item", "id class subclass sound_override_subclass material display_id inventory_type sheath".split(),
            [[t["entry"], t["class"], t["subclass"], t["SoundOverrideSubclass"], t["Material"], t["displayid"],
              t["InventoryType"], t["sheath"]] for t in itmpl], "DELETE FROM `item` WHERE `id` IN %s;" % in_list(ports),
            "Item.dbc rows of the herbs and ores"),
        os.path.join(dbc_dir, "[%s]_nodes_itemdisplayinfo.sql" % TAG): display_sql(
            items, "-- MoP item displays (5.4.8) of the herbs and ores, stock lacks them.\n"),
        os.path.join(dbc_dir, "[%s]_nodes_gameobjectdisplayinfo.sql" % TAG): "\n".join(
            "DELETE FROM `gameobjectdisplayinfo` WHERE `id` = %d;\nINSERT INTO `gameobjectdisplayinfo` SET\n%s;\n" % (
                r["id"], ",\n".join("  `%s` = %s" % (k, sql_value(v)) for k, v in r.items())) for r in disp),
    }
    for path, sql in files.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf8", newline="\n") as f:
            f.write(head + sql)
    assets = os.path.join(a.modpak, "wi_assets.txt")
    old = set(open(assets, encoding="utf8").read().split("\n")) - {""} if os.path.exists(assets) else set()
    with open(assets, "w", encoding="utf8", newline="\n") as f:
        f.write("\n".join(sorted(old | models)) + "\n")
    kinds = collections.Counter(nodes[int(s[1])][0]["name"] for s in spawns)
    print("%d node templates, %d spawns, %d items, %d object displays" % (len(nodes), len(spawns), len(ports), len(disp)))
    for k, v in kinds.most_common():
        print("   %4d %s" % (v, k))


if __name__ == "__main__":
    main()

"""Pull one Cataclysm zone's world-DB rows out of Project Neltharion's 4.3.4 dump.

  python cata_zone_extract.py WORLD_SQL OUT_DIR --map 654 --map 655 --zone 4714 --zone 4755

WORLD_SQL is Neltharion's `source/sql/base/world.zip` unpacked (a HeidiSQL dump: `REPLACE INTO `t` (cols) VALUES`
then one `(row),` per line). OUT_DIR gets one `<table>.sql` per table, in the same format with only the rows the zone
uses, plus `scope.txt` listing what was found. It is the first step of porting a starting zone (F-130's Gilneas): the
dump takes minutes to read, the extract seconds, and it shows what the port has to translate.

What counts as the zone's:
- creature and gameobject spawns on the given maps, and their templates, plus the --creature ones
- quests in the given zones (QuestSortID / ZoneOrSort), the ones their NPCs and objects start or end, and the chain
  around them (PrevQuestId, NextQuestId, RewardNextQuest...)
- SmartAI of those creatures, objects, spawns and quests, the action lists it calls, and the creatures it summons
  (whose templates and SmartAI are followed in turn)
- texts, addons, equipment, model info, waypoints, gossip menus and their texts, loot, spell clicks, vehicle
  accessories, quest POIs, conditions on any of the above, and the phase/spell_area rows of the given zones
"""
import argparse, collections, os, re, sys

TOKEN = re.compile(r"'(?:[^'\\]|\\.|'')*'|NULL|[-+0-9.eE]+|0x[0-9A-Fa-f]+", re.S)
HEADER = re.compile(r"^(?:REPLACE|INSERT(?:\s+IGNORE)?)\s+INTO\s+`(\w+)`\s*\(([^)]*)\)\s*VALUES\s*(.*)$", re.S)

# Tables read from the dump. Spawns are filtered by map while reading (the dump has ~300k of them).
TABLES = """creature gameobject creature_template creature_template_addon creature_addon creature_equip_template
creature_model_info creature_text creature_questrelation creature_involvedrelation gameobject_template
gameobject_questrelation gameobject_involvedrelation quest_template quest_poi quest_poi_points smart_scripts
creature_ai_scripts creature_ai_texts conditions waypoint_data waypoints gossip_menu gossip_menu_option npc_text
creature_loot_template gameobject_loot_template reference_loot_template pickpocketing_loot_template
skinning_loot_template item_loot_template npc_spellclick_spells vehicle_template_accessory npc_vendor npc_trainer
phase_definitions spell_area creature_formations creature_summon_groups spell_script_names spell_target_position
areatrigger_involvedrelation areatrigger_scripts areatrigger_teleport event_scripts spell_scripts
creature_onkill_reward broadcast_text item_template""".split()

# SmartAI actions whose first param is a creature entry it brings into the world (summon, mount-to, ...).
SAI_SUMMON_ACTIONS = {12, 36, 43}         # SUMMON_CREATURE, UPDATE_TEMPLATE, MOUNT_TO_ENTRY_OR_MODEL
SAI_ACTIONLIST = {80}                      # CALL_TIMED_ACTIONLIST: param1
SAI_RANDOM_ACTIONLIST = {87, 88}           # CALL_RANDOM_TIMED_ACTIONLIST (6 params), RANGE (p1..p2)
SAI_WAYPOINT_START = 53                    # WP_START: param2 = waypoints id
SAI_SUMMON_GO = 50                         # SUMMON_GO: param1
SAI_TEXT_TARGETS = ()                      # texts come in through creature_text by entry


def values(text):
    """The values of one `(…)` row, as python strings/ints/floats/None."""
    out = []
    for t in TOKEN.findall(text):
        if t == "NULL":
            out.append(None)
        elif t[0] == "'":
            out.append(t[1:-1].replace("''", "'").replace("\\'", "'").replace('\\"', '"')
                       .replace("\\n", "\n").replace("\\r", "\r").replace("\\\\", "\\"))
        else:
            try:
                out.append(int(t))
            except ValueError:
                out.append(float(t))
    return out


class Table:
    def __init__(self, name):
        self.name, self.cols, self.lines = name, None, []

    def rows(self):
        """(dict, raw line) per row. Parsed lazily: most tables are only scanned for a few keys."""
        for cols, line in self.lines:
            v = values(line)
            if len(v) != len(cols):
                sys.exit("%s: %d values for %d columns in %r" % (self.name, len(v), len(cols), line[:200]))
            yield dict(zip(cols, v)), line


def read_dump(path, maps):
    tables = {t: Table(t) for t in TABLES}
    cur = cols = None
    mapcol = {}
    with open(path, encoding="utf8", errors="replace") as fh:
        for line in fh:
            if line.startswith(("REPLACE", "INSERT")):
                m = HEADER.match(line)
                cur = tables.get(m.group(1)) if m else None
                if cur:
                    cols = [c.strip().strip("`") for c in m.group(2).split(",")]
                    cur.cols = cols
                    mapcol[cur.name] = cols.index("map") if "map" in cols else None
                    rest = m.group(3).strip()
                    if rest.startswith("("):
                        sys.exit("%s: rows on the header line are not supported" % cur.name)
                continue
            if cur is None or not line.startswith(("\t(", "(")):
                if line.strip() and not line.startswith(("\t(", "(")):
                    cur = None
                continue
            row = line.strip().rstrip(";").rstrip(",")
            mc = mapcol.get(cur.name)
            if mc is not None and cur.name in ("creature", "gameobject"):
                # cheap map filter before parsing: the first few columns hold no strings
                if int(row[1:].split(",", mc + 1)[mc]) not in maps:
                    continue
            cur.lines.append((cols, row[1:-1]))
    return tables


def extract(tables, maps, zones, seeds=()):
    T = tables
    keep = collections.defaultdict(dict)         # table -> {raw line: row}

    def take(table, pred):
        n = 0
        for r, line in T[table].rows():
            if pred(r):
                keep[table][line] = r
                n += 1
        return n

    # spawns
    take("creature", lambda r: True)
    take("gameobject", lambda r: True)
    cguids = {r["guid"] for r in keep["creature"].values()}
    gguids = {r["guid"] for r in keep["gameobject"].values()}
    centries = {r["id"] for r in keep["creature"].values()} | set(seeds)
    gentries = {r["id"] for r in keep["gameobject"].values()}

    # quests: zone quests + what the zone's NPCs/objects start or end
    def qrel(table, entries):
        return {r["quest"] for r, _ in T[table].rows() if r["id"] in entries}
    zcol = "ZoneOrSort" if "ZoneOrSort" in (T["quest_template"].cols or []) else "QuestSortID"
    quests = {r["Id"] if "Id" in r else r["ID"] for r, _ in T["quest_template"].rows() if r.get(zcol) in zones}
    quests |= qrel("creature_questrelation", centries) | qrel("creature_involvedrelation", centries)
    quests |= qrel("gameobject_questrelation", gentries) | qrel("gameobject_involvedrelation", gentries)

    # SmartAI closure: summons add creatures, action lists add scripts
    smart = list(T["smart_scripts"].rows())
    actionlists, wps, summoned_gos = set(), set(), set()
    while True:
        before = (len(centries), len(gentries), len(actionlists))
        for r, line in smart:
            st, e = r["source_type"], r["entryorguid"]
            mine = ((st == 0 and (e in centries or -e in cguids)) or (st == 1 and (e in gentries or -e in gguids))
                    or (st == 5 and e in quests) or (st == 9 and e in actionlists))
            if not mine:
                continue
            keep["smart_scripts"][line] = r
            a, p = r["action_type"], [r["action_param%d" % i] for i in range(1, 7)]
            if a in SAI_SUMMON_ACTIONS and p[0]:
                centries.add(p[0])
            elif a in SAI_ACTIONLIST:
                actionlists.add(p[0])
            elif a == 87:
                actionlists.update(x for x in p if x)
            elif a == 88:
                actionlists.update(range(p[0], p[1] + 1))
            elif a == SAI_WAYPOINT_START:
                wps.add(p[1])
            elif a == SAI_SUMMON_GO and p[0]:
                gentries.add(p[0])
        if (len(centries), len(gentries), len(actionlists)) == before:
            break

    # spellclick/vehicle passengers bring in more creatures (one level is enough for this zone's vehicles)
    take("npc_spellclick_spells", lambda r: r["npc_entry"] in centries)
    take("vehicle_template_accessory", lambda r: r["entry"] in centries)
    centries |= {r["accessory_entry"] for r in keep["vehicle_template_accessory"].values()}
    take("creature_summon_groups", lambda r: r["summonerId"] in centries)
    centries |= {r["entry"] for r in keep["creature_summon_groups"].values()}

    take("creature_template", lambda r: r["entry"] in centries)
    take("gameobject_template", lambda r: r["entry"] in gentries)
    take("quest_template", lambda r: (r.get("Id") or r.get("ID")) in quests)
    # quest chain neighbours outside the zone (breadcrumbs in and out)
    chain = set()
    for r in keep["quest_template"].values():
        for k in ("PrevQuestId", "NextQuestId", "NextQuestIdChain", "RewardNextQuest", "ExclusiveGroup"):
            if r.get(k):
                chain.add(abs(r[k]))
    chain -= quests

    for t in ("creature_questrelation", "creature_involvedrelation", "gameobject_questrelation",
              "gameobject_involvedrelation"):
        take(t, lambda r: r["quest"] in quests)
    take("quest_poi", lambda r: r["questId"] in quests)
    take("quest_poi_points", lambda r: r["questId"] in quests)
    take("creature_template_addon", lambda r: r["entry"] in centries)
    take("creature_addon", lambda r: r["guid"] in cguids)
    take("creature_equip_template", lambda r: r["entry"] in centries)
    take("creature_text", lambda r: r["entry"] in centries)
    take("creature_ai_scripts", lambda r: r["creature_id"] in centries)
    take("creature_formations", lambda r: r["leaderGUID"] in cguids or r["memberGUID"] in cguids)
    take("creature_onkill_reward", lambda r: r["creature_id"] in centries)
    take("npc_vendor", lambda r: r["entry"] in centries)
    take("npc_trainer", lambda r: r["entry"] in centries)
    displays = set()
    for r in keep["creature_template"].values():
        displays |= {r[k] for k in ("modelid1", "modelid2", "modelid3", "modelid4") if r.get(k)}
    for r in keep["creature"].values():
        if r.get("modelid"):
            displays.add(r["modelid"])
    take("creature_model_info", lambda r: r["modelid"] in displays)

    paths = {r["path_id"] for t in ("creature_addon", "creature_template_addon") for r in keep[t].values()
             if r.get("path_id")}
    take("waypoint_data", lambda r: r["id"] in paths)
    take("waypoints", lambda r: r["entry"] in wps)

    menus = {r["gossip_menu_id"] for r in keep["creature_template"].values() if r.get("gossip_menu_id")}
    menus |= {r["data3"] for r in keep["gameobject_template"].values() if r.get("type") == 2 and r.get("data3")}
    while True:
        n = len(menus)
        opts = [r for r, _ in T["gossip_menu_option"].rows() if r["menu_id"] in menus]
        menus |= {r["action_menu_id"] for r in opts if r.get("action_menu_id")}
        if len(menus) == n:
            break
    take("gossip_menu", lambda r: r["entry"] in menus)
    take("gossip_menu_option", lambda r: r["menu_id"] in menus)
    texts = {r["text_id"] for r in keep["gossip_menu"].values()}
    take("npc_text", lambda r: r["ID"] in texts)

    loot = {r["lootid"] for r in keep["creature_template"].values() if r.get("lootid")}
    take("creature_loot_template", lambda r: r["entry"] in loot)
    gloot = {r["data1"] for r in keep["gameobject_template"].values() if r.get("type") in (3, 25) and r.get("data1")}
    take("gameobject_loot_template", lambda r: r["entry"] in gloot)
    take("pickpocketing_loot_template",
         lambda r: r["entry"] in {c["pickpocketloot"] for c in keep["creature_template"].values()})
    take("skinning_loot_template",
         lambda r: r["entry"] in {c["skinloot"] for c in keep["creature_template"].values()})
    refs = set()
    for t in ("creature_loot_template", "gameobject_loot_template"):
        refs |= {abs(r["mincountOrRef"]) for r in keep[t].values() if r.get("mincountOrRef", 0) < 0}
    take("reference_loot_template", lambda r: r["entry"] in refs)

    # items the zone hands out (loot, quest rewards/sources, vendors); item_template if the dump has it
    items = set()
    for t in ("creature_loot_template", "gameobject_loot_template", "reference_loot_template"):
        items |= {r["item"] for r in keep[t].values()}
    for r in keep["quest_template"].values():
        items |= {v for k, v in r.items() if v and re.match(r"(Rew|Reward|Required|Source|Req)\w*Item(Id)?\d*$", k)}
    items |= {r["item"] for r in keep["npc_vendor"].values()}
    take("item_template", lambda r: r["entry"] in items)

    # phasing: phase_definitions by zone, spell_area by the zone's areas (spell_area has no zone column; areas come
    # from the spawns)
    areas = {r.get("area") for r in keep["creature"].values()} | set(zones)
    take("phase_definitions", lambda r: r["zoneId"] in zones)
    take("spell_area", lambda r: r["area"] in areas or r["quest_start"] in quests or r["quest_end"] in quests)

    # conditions on anything kept: SourceTypeOrReferenceId -> what SourceGroup/SourceEntry mean
    def cond_mine(r):
        t, g, e = r["SourceTypeOrReferenceId"], r["SourceGroup"], r["SourceEntry"]
        if t in (1, 4):                                                            # creature/go loot
            return g in (loot if t == 1 else gloot)                                # 4 = gameobject loot
        if t in (14, 15):                                                          # gossip menu / option
            return g in menus
        if t in (19, 20):                                                          # quest accept / show mark
            return e in quests
        if t == 22:                                                                # SmartAI event
            return (r["SourceId"] == 0 and (e in centries or -e in cguids)) or \
                   (r["SourceId"] == 1 and (e in gentries or -e in gguids)) or (r["SourceId"] == 9 and e in actionlists)
        if t == 18:                                                                # spell click
            return g in centries
        if t == 23:                                                                # npc vendor
            return g in centries
        if t == 25:                                                                # phase definition
            return g in zones
        if t in (13, 17):                                                          # spell target / spell
            return e in spells
        return False
    spells = set()
    for r in keep["smart_scripts"].values():
        if r["action_type"] in (11, 85, 86, 75, 28):                               # CAST, SELF_CAST, CROSS_CAST, ADD/REMOVE_AURA
            spells.add(r["action_param1"])
        if r["event_type"] in (8, 31):                                             # SPELLHIT, SPELLHIT_TARGET
            spells.add(r["event_param1"])
    spells |= {r["spell_id"] for r in keep["npc_spellclick_spells"].values()}
    for r in keep["creature_template"].values():
        spells |= {r[k] for k in r if k.startswith("spell") and k[5:].isdigit() and r[k]}
    for r in keep["quest_template"].values():
        spells |= {v for k, v in r.items() if v and re.match(r"(RewSpell|RewSpellCast|RewardSpell\w*|SourceSpellid|SourceSpellID|RequiredSpellCast\d|RequiredSpell)$", k)}
    spells |= {r["spell"] for r in keep["spell_area"].values()}
    spells.discard(0)
    take("conditions", cond_mine)
    take("spell_script_names", lambda r: abs(r["spell_id"]) in spells)
    take("spell_target_position", lambda r: r["id"] in spells)

    # texts that only live in broadcast_text
    bt = {r["BroadcastTextID"] for r in keep["creature_text"].values() if r.get("BroadcastTextID")}
    if T["broadcast_text"].cols:
        take("broadcast_text", lambda r: r["ID"] in bt)

    return keep, dict(quests=quests, chain=chain, centries=centries, gentries=gentries, spells=spells,
                      actionlists=actionlists, menus=menus, items=items, areas=areas)


def write(tables, keep, scope, out):
    os.makedirs(out, exist_ok=True)
    for name, rows in keep.items():
        if not rows:
            continue
        cols = tables[name].cols
        with open(os.path.join(out, name + ".sql"), "w", encoding="utf8", newline="\n") as fh:
            fh.write("REPLACE INTO `%s` (%s) VALUES\n" % (name, ", ".join("`%s`" % c for c in cols)))
            fh.write(",\n".join("\t(%s)" % line for line in rows) + ";\n")
    script_names = collections.Counter()
    for r in keep["creature_template"].values():
        if r.get("ScriptName"):
            script_names[r["ScriptName"]] += 1
    for r in keep["gameobject_template"].values():
        if r.get("ScriptName"):
            script_names[r["ScriptName"]] += 1
    with open(os.path.join(out, "scope.txt"), "w", encoding="utf8", newline="\n") as fh:
        for name in sorted(keep):
            fh.write("%-30s %6d rows\n" % (name, len(keep[name])))
        for k in sorted(scope):
            fh.write("\n%s (%d): %s\n" % (k, len(scope[k]), " ".join(map(str, sorted(x for x in scope[k] if x is not None)))))
        fh.write("\nC++ scripts named by templates (%d):\n" % len(script_names))
        fh.write("".join("  %s\n" % s for s in sorted(script_names)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("world_sql")
    ap.add_argument("out_dir")
    ap.add_argument("--map", type=int, action="append", required=True)
    ap.add_argument("--zone", type=int, action="append", required=True)
    ap.add_argument("--creature", default="", help="comma-separated creatures to add: ones only spells summon, which "
                    "the port reports")
    a = ap.parse_args()
    tables = read_dump(a.world_sql, set(a.map))
    missing = [t for t in TABLES if tables[t].cols is None]
    if missing:
        print("not in the dump: " + " ".join(missing))
    for t in TABLES:                       # tables the dump lacks: empty, so lookups just find nothing
        if tables[t].cols is None:
            tables[t].cols = []
    seeds = [int(x) for x in a.creature.split(",") if x]
    keep, scope = extract(tables, set(a.map), set(a.zone), seeds)
    write(tables, keep, scope, a.out_dir)
    print(open(os.path.join(a.out_dir, "scope.txt"), encoding="utf8").read().split("\n\n")[0])


if __name__ == "__main__":
    main()

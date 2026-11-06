"""Port Zeppelin-Craft's zep-goblin-start zpak to F-013_zep-goblin-start.

  python zep_goblin_port.py ZPAK_DIR F013_DIR

Rerun it after pulling a new version of the zpak. It replaces dbc/ and sql/ in F013_DIR and leaves readme.md,
variables.sql and patches/ alone, so hand-written changes belong in those or in this script, not in the ported SQL.

What differs from the zpak:
- world SQL moves to sql/db-world/base, where build-dbc.sh looks for it
- table names get backticks: build-dbc.sh only exports DBC tables it finds written as `table`
- Zeppelin's race and faction ids become the variables of config.sql and variables.sql:
    - Faction 1133 and 1152 and template 2204 already exist as F-023's Bilgewater Cartel, "PLAYER, Goblin" and its
      template, with 256-bit masks and the Worgen bit, so they are not written again
    - template 2238 is @GoblinFactionTemplate here, so Zeppelin's Orgrimmar-aligned 2238 moves to a variable
    - race 12 is Worgen in Zeppelin but Fel Orc here (@Worgen is 22)
    - quest race masks get their second word
- the spell visual effects that collide with F-063 move to the variables in variables.sql
- rows the race modpaks already own (KEEP_EXISTING) are only added if missing
- stock NPCs and objects the zones spawn keep their stock rows (STOCK_CREATURES, STOCK_GAMEOBJECTS)
- taking Goblins off a stock class quest only clears their bit, so the races added by other modpaks keep the quest
- dbc/[F-013]_item.sql adds the new items to Item.dbc, which Zeppelin does at build time instead
- the files in zep_goblin_fixes/ next to this script are added: what the zpak refers to but doesn't have, taken from
  Project Neltharion's world database (Zeppelin's donor) and the Cataclysm 4.0.6a DBCs (cata406_dbc_port.py)
- positions Zeppelin left on map 648 (Cataclysm's Kezan and Lost Isles) move to Kalimdor: SmartAI targets, SmartAI
  teleports and quest POIs (SHIFT_648)
- references to what neither the zpak nor stock has are dropped or cleared: Cata items Zeppelin uses for something
  else, Neltharion's own marker spells and creatures, quest display spells that can't work here (see DEAD_*)
- creatures whose SmartAI has no rows left get no AIName, and Neltharion's NullAI is NullCreatureAI here
"""
import glob, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXES_DIR = os.path.join(HERE, "zep_goblin_fixes")

# Zeppelin's FactionTemplate id -> variable
FACTION_TEMPLATES = {
    2159: "@BilgewaterCivilianFactionTemplate",
    2160: "@BilgewaterCivilian2FactionTemplate",
    2200: "@PredatorFactionTemplate",
    2204: "@GoblinFactionTemplate",
    2227: "@BilgewaterFighterFactionTemplate",
    2228: "@OomlotFactionTemplate",
    2231: "@TownInABoxFactionTemplate",
    2238: "@OrgrimmarAlliedFactionTemplate",
}
# Zeppelin's Faction id -> variable, for the columns that hold one
FACTIONS = {1133: "@GoblinFaction", 1152: "@GoblinPlayer", 1157: "@PygmyFaction"}
# Zeppelin's ChrRaces id -> variable, for the creaturedisplayinfoextra.race column
RACES = {9: "@Goblin", 12: "@Worgen", 13: "@Naga"}
# Upstream quest race masks -> (word 1, word 2)
QUEST_RACES = {256: ("@GoblinMask", "@GoblinMask_2"), 946: ("@HordeMask", "@HordeMask_2")}

# Retail ids that F-023 and F-024 also use (@GoblinTrikeDisplay, @WorgenMaleModel, ...): their rows win. F-013 still
# adds them when those modpaks are off.
KEEP_EXISTING = {
    "creaturedisplayinfo": (32385, 35249),
    "creaturemodeldata": (3141, 3194, 3624),
    "itemdisplayinfo": (62573, 62614, 62617),
}

# Stock templates the generated rows would rewrite for the whole world, such as every Spirit Healer's gossip menu and AI,
# or the Icecrown text of the ELM General Purpose Bunny. The zones only need to spawn them, so the stock rows stay.
STOCK_CREATURES = (2110, 4075, 6491, 6827, 7395, 13321, 23837, 24021, 24110, 31688)
STOCK_GAMEOBJECTS = (181886, 185319, 202361)
# Stock skinning loot of 14 other creatures. Only Zeppelin's Cockroach used its version, and that keeps its stock row.
STOCK_SKINNING_LOOT = (100008,)
# Model info of the displays in KEEP_EXISTING's creaturedisplayinfo: only added if missing
KEEP_MODEL_INFO = (32385, 35249)

# Kezan and the Lost Isles are map 648 in Cataclysm (661 is a terrain-swap copy of it). Zeppelin moves them to
# Kalimdor with this shift, but its generator left SmartAI target positions, the map of SmartAI teleports (action 62)
# and the quest POI fields as they were. [I-277] fixed one of the positions by hand, to the same values.
SHIFT_648 = (-533.3333, -12800.0)
MAPS_648 = (648, 661)

# Cata items that Zeppelin's zep-dungeons uses for other items. [I-236] ports the three grey items the creature loot
# needs under new ids, but [I-338] adds loot rows after it with the old ids. The others have no item here.
ITEM_REMAP = {67252: 84511, 67256: 84512, 67257: 84513}
DEAD_ITEMS = frozenset({64433, 61320, *range(67253, 67256), *range(67280, 67324)})
# Quest display spells (cast on completion) that can't work here: 91847 plays a movie, which [I-280] does instead;
# 74103's hearthstone bind has no destination in Neltharion; 68063, 68345 and 69013 end in script effects only
# Neltharion's C++ handled.
DEAD_DISPLAY_SPELLS = (68063, 68345, 69013, 74103, 91847)
# creature_template_addon rows of creatures neither the zpak nor stock has
DEAD_ADDONS = (33111, 33765, 37490, 38819, 38908, 38979, 38984, 39375, 43359, 75114)
# Rows that point at something nothing here has: Neltharion's marker spells and objects, and 89822, a Felwood spell
DEAD_ROWS = {
    "70": (r"\(13, 1, 73425, 0, 1, 31, 0, 5, 202463,",       # land mine trap, spawned nowhere ([I-346])
           r"\(15, 510097, 0, 0, 0, 1, 0, (?:151099|151100),",  # Neltharion marker auras
           r"\(13, 1, 73532, ",),                            # no area target since spells.py's override: inert
    "65": (r"\((?:38318|4458[89]|4459[01]|75116|48310), 0, \d+, \d+, 8, \d+, \d+, \d+, (?:151145|151146|151150|89822),",),
}
# SmartAI parameters Neltharion set that AC's actions don't take (AC skips the whole row): (entry, id) -> column
UNUSED_SMART_PARAMS = {(36600, 2): "action_param2", (37602, 3): "event_param1"}

SQL_DIR = os.path.join("sql", "db-world", "base")
TABLE_STATEMENT = re.compile(r"^(\s*(?:INSERT(?:\s+IGNORE)?\s+INTO|REPLACE\s+INTO|DELETE\s+FROM|UPDATE)\s+)([A-Za-z_]\w*)\b", re.M)


def backtick_tables(sql):
    return TABLE_STATEMENT.sub(lambda m: f"{m.group(1)}`{m.group(2)}`", sql)


def sub_ids(pattern, ids, sql):
    """Replace the id in group 2 of pattern when it has a variable; group 1 is what comes before it."""
    def repl(m):
        var = ids.get(int(m.group(2)))
        return m.group(1) + var if var else m.group(0)
    return re.sub(pattern, repl, sql)


def port_common(sql):
    sql = backtick_tables(sql)
    return sub_ids(r"(`?\bfaction`?\s*=\s*)(\d+)\b", FACTION_TEMPLATES, sql)


def drop_blocks(sql, ids):
    """Remove the generated DELETE + INSERT ... SET rows of these ids."""
    alternatives = "|".join(map(str, ids))
    return re.sub(rf"DELETE FROM `(\w+)` WHERE (?:entry|CreatureI[dD]) = (?:{alternatives});\r?\n(?:INSERT INTO `\1` SET\r?\n.*?;\r?\n\r?\n?)+", "", sql, flags=re.S)


def drop_lines(sql, matches):
    """Remove the rows matches(line) is true for from multi-row INSERTs, ending the statement on the row before."""
    out = []
    for line in sql.split("\n"):
        if matches(line):
            if line.rstrip().endswith(";"):  # The statement's last row: the one before it ends the statement now
                if out[-1].rstrip().endswith(","):
                    out[-1] = out[-1].rstrip()[:-1] + ";"
                elif out[-1].rstrip().upper().endswith("VALUES"):
                    out.pop()
                else:
                    raise SystemExit(f"drop_lines: can't end the statement before {line[:40]}")
            continue
        out.append(line)
    return "\n".join(out)


VALUE = re.compile(r"'(?:[^'\\]|\\.|'')*'|[^,\s()][^,()]*")


def edit_rows(sql, table, edit):
    """Call edit(row) for every row of the multi-row INSERTs into table, with row a dict of its columns (as SQL text).
    edit changes row in place, or returns False to remove it."""
    columns, drop = None, set()
    lines = sql.split("\n")
    for n, line in enumerate(lines):
        insert = re.match(rf"\s*(?:INSERT(?:\s+IGNORE)?|REPLACE)\s+INTO\s+`{table}`\s*\(([^)]*)\)\s*VALUES\s*$", line)
        if insert:
            columns = [c.strip(" `") for c in insert.group(1).split(",")]
            continue
        row = re.match(r"(\s*)\((.*)\)([,;]?)(\s*(?:--.*)?)$", line) if columns else None
        if not row:
            columns = None if columns and line.strip() and not line.lstrip().startswith("--") else columns
            continue
        values = [v.strip() for v in VALUE.findall(row.group(2))]
        if len(values) != len(columns):
            raise SystemExit(f"edit_rows: {len(values)} values for {len(columns)} columns of {table}: {line[:60]}")
        fields = dict(zip(columns, values))
        if edit(fields) is False:
            drop.add(n)
        elif [fields[c] for c in columns] != values:  # rewrite only changed rows, which keeps hand alignment
            lines[n] = f"{row.group(1)}({', '.join(fields[c] for c in columns)}){row.group(3)}{row.group(4)}"
        if row.group(3) == ";":
            columns = None
    sql = "\n".join(lines)
    if drop:
        marked = "\n".join(("\0" + l) if i in drop else l for i, l in enumerate(sql.split("\n")))
        sql = drop_lines(marked, lambda l: l.startswith("\0"))
    return sql


def shift_648(x, y):
    return tuple(f"{float(v) + d:.4f}".rstrip("0").rstrip(".") for v, d in ((x, SHIFT_648[0]), (y, SHIFT_648[1])))


def num(value):
    """The number a column holds, or None for a variable, an expression or a string."""
    return float(value) if re.fullmatch(r"-?\d+(?:\.\d+)?", value) else None


def fix_smart_row(row):
    if num(row["target_type"]) == 8 and (num(row["target_y"]) or 0) > 0:  # Kalimdor's zones are at y < 0
        row["target_x"], row["target_y"] = shift_648(row["target_x"], row["target_y"])
    if num(row["action_type"]) == 62 and num(row["action_param1"]) in MAPS_648:  # SMART_ACTION_TELEPORT
        row["action_param1"] = "1"
    unused = UNUSED_SMART_PARAMS.get((num(row["entryorguid"]), num(row["id"])))
    if unused and num(row["source_type"]) == 0:
        row[unused] = "0"


def fix_items(sql):
    def loot(row):
        item = num(row["Item"])
        if item in DEAD_ITEMS:
            return False
        if item in ITEM_REMAP:
            row["Item"] = str(ITEM_REMAP[item])

    def vendor(row):
        return num(row["item"]) not in DEAD_ITEMS and None

    def equip(row):
        for k in ("ItemID1", "ItemID2", "ItemID3"):
            if num(row[k]) in DEAD_ITEMS:
                row[k] = "0"
    sql = edit_rows(sql, "creature_loot_template", loot)
    sql = edit_rows(sql, "npc_vendor", vendor)
    return edit_rows(sql, "creature_equip_template", equip)


def fix_quests(sql):
    def poi(m):
        x, y = shift_648(m.group(4), m.group(6))
        return f"{m.group(1)}1,{m.group(3)}{x},{m.group(5)}{y},"
    sql = re.sub(r"(`POIContinent` = )(\d+),(\s*`POIx` = )(-?[\d.]+),(\s*`POIy` = )(-?[\d.]+),",
                 lambda m: poi(m) if int(m.group(2)) in MAPS_648 else m.group(0), sql)
    # 4707 is an old "The Lost Isles" area under Dun Morogh; the other quests of the zone use 4720
    sql = sql.replace("`QuestSortID` = 4707,", "`QuestSortID` = 4720,")
    return re.sub(rf"(`RewardDisplaySpell` = )(?:{'|'.join(map(str, DEAD_DISPLAY_SPELLS))}),", r"\g<1>0,", sql)


def drop_value_rows(sql, ids):
    """Remove the rows of these ids from multi-row INSERTs, and the ids from the DELETEs before them."""
    alternatives = "|".join(map(str, ids))
    sql = drop_lines(sql, lambda line: re.match(rf"\s*\((?:{alternatives}),", line))
    sql = re.sub(rf"(WHERE (?:CreatureID|Entry) IN \()((?:\d+,)*\d+)\)", lambda m: m.group(1) + ",".join(
        i for i in m.group(2).split(",") if int(i) not in ids) + ")", sql)
    return re.sub(rf"DELETE FROM `smart_scripts` WHERE source_type=0 AND entryorguid=(?:{alternatives});\r?\n", "", sql)


def stock_spawns_unequipped(sql):
    """Spawns of STOCK_CREATURES get equipment_id 0: their stock templates have no creature_equip_template rows, so the
    generator's 1 only made the server log every spawn."""
    alternatives = "|".join(map(str, STOCK_CREATURES))
    return re.sub(rf"^(\s*\(\d+, (?:{alternatives}), (?:[^,]*, ){{5}})-?\d+,", r"\g<1>0,", sql, flags=re.M)


def keep_stock(name, sql):
    table = re.search(r"\[AUTO,F-011\]_(\d+)_", name)
    if not table:
        return sql
    if table.group(1) in ("10", "11", "12", "14"):
        return drop_blocks(sql, STOCK_CREATURES)
    if table.group(1) == "20":
        return drop_blocks(sql, STOCK_GAMEOBJECTS)
    if table.group(1) in ("16", "17", "65"):
        return drop_value_rows(sql, STOCK_CREATURES)
    if table.group(1) == "40":
        return stock_spawns_unequipped(sql)
    if table.group(1) == "51":
        return drop_value_rows(sql, STOCK_SKINNING_LOOT)
    if table.group(1) == "13":
        for row in KEEP_MODEL_INFO:
            sql, count = re.subn(rf"DELETE FROM `creature_model_info` WHERE DisplayID = {row};\r?\nINSERT INTO `creature_model_info` SET",
                                 "INSERT IGNORE INTO `creature_model_info` SET", sql)
            if count != 1:
                raise SystemExit(f"creature_model_info: expected one row {row}, found {count}")
    return sql


def port_world(name, sql):
    sql = keep_stock(name, port_common(sql))
    sql = sub_ids(r"(`?\bRewardFactionID\d`?\s*=\s*)(\d+)\b", FACTIONS, sql)
    sql = sub_ids(r"(`?\bRequiredFactionId\d`?\s*=\s*)(\d+)\b", FACTIONS, sql)

    def quest_races(m):
        words = QUEST_RACES.get(int(m.group(3)))
        if not words:
            return m.group(0)
        return f"{m.group(1)}{m.group(2)}{words[0]},\n{m.group(1)}`AllowableRaces_2` = {words[1]},"
    sql = re.sub(r"^(\s*)(`?AllowableRaces`?\s*=\s*)(\d+),", quest_races, sql, flags=re.M)

    # Zeppelin takes Goblins off stock class quests by writing the whole mask, which would also drop every race the
    # race modpaks added. Only clear the Goblin bit, which works because F-013 comes after them in the manifest.
    sql = re.sub(r"SET AllowableRaces = \d+ WHERE ID = (\d+);",
                 r"SET `AllowableRaces` = `AllowableRaces` & ~@GoblinMask, `AllowableRaces_2` = `AllowableRaces_2` & ~@GoblinMask_2 WHERE ID = \1;", sql)
    left = re.search(r"`?AllowableRaces`?\s*=\s*[1-9]\d*", sql)
    if left:
        raise SystemExit(f"{name}: no variable for {left.group(0)}, see QUEST_RACES")

    # "All races" in 31 bits: -1 is all of them here
    sql = re.sub(r"(`AllowableRace`\s*=\s*)2147483647\b", r"\g<1>-1", sql)
    if "playercreateinfo_kezan" in name:
        sql = re.sub(r"^SET @(map|zone|x|y|z|o) = .*\n", "", sql, flags=re.M)
        sql = sql.replace("map = @map", "map = @Kalimdor").replace("zone = @zone", "zone = @Kezan")
        for axis, var in (("x", "X"), ("y", "Y"), ("z", "Z")):
            sql = sql.replace(f"position_{axis} = @{axis}", f"position_{axis} = @GoblinStart{var}")
        sql = sql.replace("orientation = @o", "orientation = @GoblinStartO")
        sql = sql.replace("WHERE race = 9 AND class <> 6", "WHERE race = @Goblin AND class <> @DeathKnight")
    return fix_references(name, sql)


def fix_references(name, sql):
    table = re.search(r"\[AUTO,F-011\]_(\d+)_", name)
    group = table.group(1) if table else None
    if group in DEAD_ROWS:
        dead = re.compile(r"\s*(?:" + "|".join(DEAD_ROWS[group]) + ")")
        sql = drop_lines(sql, dead.match)
    if group == "11":
        sql = drop_blocks(sql, DEAD_ADDONS)
    if group == "12":
        # 16480, the display Neltharion gives its Wondi's Bunny markers, is an Imp: use the stock invisible stalker
        sql = sql.replace("`CreatureDisplayID` = 16480,", "`CreatureDisplayID` = 11686,")
    if "quest_template" in name:
        sql = fix_quests(sql)
    sql = fix_items(edit_rows(sql, "smart_scripts", fix_smart_row))
    return re.sub(r"(`?AIName`?\s*=\s*)'NullAI'", r"\g<1>'NullCreatureAI'", sql)


def unscripted_smart_ai(world_dir):
    """Clear the SmartAI of generated creatures that have no SmartAI rows left (the generator drops the rows that use
    what it couldn't port), which the server reports for every one of them."""
    scripted, guid_entry = set(), {}
    for path in glob.glob(os.path.join(world_dir, "*.sql")):
        sql = re.sub(r"--[^\n]*", "", read(path))
        variables = {m.group(1): int(m.group(2)) for m in re.finditer(r"SET\s+@(\w+)\s*:?=\s*(-?\d+)\s*;", sql)}
        value = lambda v: variables.get(v[1:]) if v.startswith("@") else int(v)
        # Rows of every INSERT, however they are laid out: what matters is the first two values of each
        for m in re.finditer(r"INSERT\s+(?:IGNORE\s+)?INTO\s+`?smart_scripts`?\s*\(([^)]*)\)\s*VALUES(.*?);\s*$", sql,
                             re.S | re.M):
            for row in re.finditer(r"\(\s*(-?\d+|@\w+)\s*,\s*(\d+)\s*,", m.group(2)):
                if row.group(2) == "0":
                    scripted.add(value(row.group(1)))
        for m in re.finditer(r"`?entryorguid`?\s*=\s*(-?\d+|@\w+)\s*,\s*`?source_type`?\s*=\s*0\b", sql):
            scripted.add(value(m.group(1)))
        for m in re.finditer(r"INSERT\s+INTO\s+`creature`\s*\(`guid`, `id`,[^)]*\)\s*VALUES(.*?);\s*$", sql, re.S | re.M):
            guid_entry.update((int(g), int(e)) for g, e in re.findall(r"\(\s*(\d+)\s*,\s*(\d+)\s*,", m.group(1)))
    scripted |= {guid_entry.get(-e) for e in scripted if e is not None and e < 0}
    path = os.path.join(world_dir, "zz_[AUTO,F-011]_10_creature_template.sql")

    def clear(m):
        return m.group(0) if int(m.group(1)) in scripted else m.group(0).replace("`AIName` = 'SmartAI',", "`AIName` = '',")
    write(path, re.sub(r"INSERT INTO `creature_template` SET\s+`entry` = (\d+),.*?;", clear, read(path), flags=re.S))


def keep_existing(table, sql):
    for row in KEEP_EXISTING.get(table, ()):
        sql, count = re.subn(rf"DELETE FROM `{table}` WHERE id = {row};\r?\nINSERT INTO `{table}` SET", f"INSERT IGNORE INTO `{table}` SET", sql)
        if count != 1:
            raise SystemExit(f"{table}: expected one row {row}, found {count}")
    return sql


def port_dbc(name, sql):
    sql = port_common(sql)
    auto = re.fullmatch(r"\[AUTO,F-011\]_(\w+)\.sql", name)
    if auto:
        sql = keep_existing(auto.group(1), sql)
    if name == "[I-337]_faction.sql":
        return FACTION_SQL
    if name == "[I-337]_factiontemplate.sql":
        return port_factiontemplate(sql)
    if name == "[I-334]_creaturedisplayinfoextra.sql":
        return sql.replace("SET race = 12 WHERE", "SET race = @Worgen WHERE")
    if name == "[AUTO,F-011]_creaturedisplayinfoextra.sql":
        sql = sub_ids(r"(`race`\s*=\s*)(\d+)\b", RACES, sql)
    if name == "[I-280]_goblin_intro_cinematic.sql":
        sql = sql.replace("`cinematic_sequence_id` = 172 WHERE `id` = 9", "`cinematic_sequence_id` = 172 WHERE `id` = @Goblin")
    # Spell 66987 Pygmy Helmet: force reaction with faction 1157
    sql = sub_ids(r"(`effect_misc_value_a_\d`\s*=\s*)(1157)\b", FACTIONS, sql)
    # Effects 90110 and 90111 are F-063's @AlteredFormPoofEffect and @AlteredFormAnimationPoofEffect
    sql = re.sub(r"(?<![\w.])90110(?![\w.])", "@ZepEffect90110", sql)
    sql = re.sub(r"(?<![\w.])90111(?![\w.])", "@ZepEffect90111", sql)
    return sql


FACTION_SQL = """-- Pygmy (Oomlot tribe), the only Cataclysm faction the goblin zone adds. Bilgewater Cartel (@GoblinFaction) and
-- "PLAYER, Goblin" (@GoblinPlayer) come from F-023 with their 256-bit race masks, so they aren't overwritten here.

DELETE FROM `faction` WHERE `id` = @PygmyFaction;
INSERT INTO `faction` SET
  `id` = @PygmyFaction,
  `reputation_index` = -1,
  `name_enus` = 'Pygmy',
  `name_flags` = 16712190,
  `description_flags` = 16712188;
"""


def port_factiontemplate(sql):
    """Drop the row F-023 already has, then use the variables."""
    sql = re.sub(r"-- \"PLAYER, Goblin\".*?;\n\n", "", sql, flags=re.S)
    if "= 2204" in sql:
        raise SystemExit("[I-337]_factiontemplate.sql: couldn't drop template 2204, see port_factiontemplate")
    sql = re.sub(r"DELETE FROM `factiontemplate` WHERE id IN \([^)]*\);", lambda m: "DELETE FROM `factiontemplate` WHERE id IN (" + ", ".join(
        v for k, v in FACTION_TEMPLATES.items() if k != 2204) + ");", sql)
    sql = re.sub(r"(?m)^(\s*id\s*=\s*)(\d+)\b", lambda m: m.group(1) + FACTION_TEMPLATES[int(m.group(2))], sql)
    sql = re.sub(r"(?m)^(\s*faction\s*=\s*)76\b", r"\g<1>@OrcFaction", sql)
    sql = re.sub(r"(?m)^(\s*(?:faction|enemies_\d|friends_\d)\s*=\s*)(1133|1157)\b",
                 lambda m: m.group(1) + FACTIONS[int(m.group(2))], sql)
    return sql


# item_template column -> (Item.dbc column, item_template default)
ITEM_DBC_COLUMNS = (
    ("class", "class", 0),
    ("subclass", "subclass", 0),
    ("SoundOverrideSubclass", "sound_override_subclass", -1),
    ("Material", "material", 0),
    ("displayid", "display_id", 0),
    ("InventoryType", "inventory_type", 0),
    ("sheath", "sheath", 0),
)
ITEM_DBC_FILE = "[F-013]_item.sql"


def item_dbc(world_dir):
    """Item.dbc rows for every item the world SQL adds.

    Zeppelin-Craft builds these from its live world database at build time (patch_builder.py's item-dbc-sync), so the
    zpak has none. The server only loads items that are in Item.dbc: without them it reports the zone's quest items as
    nonexistent. Later definitions win, as they do in the database, so the [I-xxx] fixes override the generated rows.
    """
    items = {}
    for name in sorted(os.listdir(world_dir)):
        sql = read(os.path.join(world_dir, name))
        if re.search(r"INSERT\s+INTO\s+`?item_template`?\s*\(", sql, re.I):
            raise SystemExit(f"{name}: item_template INSERT ... VALUES isn't supported, see item_dbc")
        variables = {m.group(1): int(m.group(2)) for m in re.finditer(r"^SET\s+@(\w+)\s*:?=\s*(-?\d+)\s*;", sql, re.M)}
        for block in re.finditer(r"INSERT\s+INTO\s+`item_template`\s+SET(.*?);", sql, re.S):
            fields = {}
            for m in re.finditer(r"`?(\w+)`?\s*=\s*(@\w+|-?\d+)", block.group(1)):
                value = m.group(2)
                if value.startswith("@"):
                    if value[1:] not in variables:
                        raise SystemExit(f"{name}: item_template uses {value}, which the file doesn't SET")
                    value = variables[value[1:]]
                fields[m.group(1).lower()] = int(value)
            items[fields["entry"]] = [fields.get(col.lower(), default) for col, _, default in ITEM_DBC_COLUMNS]
    if not items:
        return None

    columns = ", ".join(f"`{dbc}`" for _, dbc, _ in ITEM_DBC_COLUMNS)
    rows = ",\n".join(f"({entry}, " + ", ".join(map(str, values)) + ")" for entry, values in sorted(items.items()))
    return (f"-- Item.dbc rows of the {len(items)} items the world SQL adds. Generated by tools/races/zep_goblin_port.py from\n"
            "-- their item_template rows: change those, not this file.\n\n"
            f"DELETE FROM `item` WHERE `id` IN ({', '.join(map(str, sorted(items)))});\n"
            f"INSERT INTO `item` (`id`, {columns}) VALUES\n{rows};\n")


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def main(zpak, dest):
    for sub in ("dbc", "sql", "mpq"):
        shutil.rmtree(os.path.join(dest, sub), ignore_errors=True)

    for name in sorted(os.listdir(os.path.join(zpak, "dbc"))):
        if name.endswith("_md5translate.sql"):  # Minimap rows: nothing to port, build-dbc.sh writes the .trs
            write(os.path.join(dest, "dbc", name), read(os.path.join(zpak, "dbc", name)))
        elif name.endswith(".sql"):
            write(os.path.join(dest, "dbc", name), port_dbc(name, read(os.path.join(zpak, "dbc", name))))
    for name in sorted(os.listdir(os.path.join(zpak, "sql"))):
        if name.endswith(".sql"):
            write(os.path.join(dest, SQL_DIR, name), port_world(name, read(os.path.join(zpak, "sql", name))))
    for sub, target in (("dbc", "dbc"), ("sql", SQL_DIR)):
        for path in sorted(glob.glob(os.path.join(FIXES_DIR, sub, "*.sql"))):
            shutil.copy2(path, os.path.join(dest, target, os.path.basename(path)))
    unscripted_smart_ai(os.path.join(dest, SQL_DIR))
    items = item_dbc(os.path.join(dest, SQL_DIR))
    if items:
        write(os.path.join(dest, "dbc", ITEM_DBC_FILE), items)

    # Provenance of the client assets and the tools that made them
    for name in os.listdir(zpak):
        if name.endswith((".json", ".py")):
            shutil.copy2(os.path.join(zpak, name), os.path.join(dest, name))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

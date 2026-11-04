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
"""
import os, re, shutil, sys

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


def drop_value_rows(sql, ids):
    """Remove the rows of these ids from multi-row INSERTs, and the ids from the DELETEs before them."""
    alternatives = "|".join(map(str, ids))
    out = []
    for line in sql.split("\n"):
        if re.match(rf"\s*\((?:{alternatives}),", line):
            if line.rstrip().endswith(";"):  # The statement's last row: the one before it ends the statement now
                if out[-1].rstrip().endswith(","):
                    out[-1] = out[-1].rstrip()[:-1] + ";"
                elif out[-1].rstrip().upper().endswith("VALUES"):
                    out.pop()
                else:
                    raise SystemExit(f"drop_value_rows: can't end the statement before {line[:40]}")
            continue
        out.append(line)
    sql = "\n".join(out)
    sql = re.sub(rf"(WHERE (?:CreatureID|Entry) IN \()((?:\d+,)*\d+)\)", lambda m: m.group(1) + ",".join(
        i for i in m.group(2).split(",") if int(i) not in ids) + ")", sql)
    return re.sub(rf"DELETE FROM `smart_scripts` WHERE source_type=0 AND entryorguid=(?:{alternatives});\r?\n", "", sql)


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
    return sql


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
        if name.endswith("_md5translate.sql"):  # Not a DBC: F-010 keeps this table in the world database
            write(os.path.join(dest, SQL_DIR, "zz_" + name), read(os.path.join(zpak, "dbc", name)))
        elif name.endswith(".sql"):
            write(os.path.join(dest, "dbc", name), port_dbc(name, read(os.path.join(zpak, "dbc", name))))
    for name in sorted(os.listdir(os.path.join(zpak, "sql"))):
        if name.endswith(".sql"):
            write(os.path.join(dest, SQL_DIR, name), port_world(name, read(os.path.join(zpak, "sql", name))))

    # Provenance of the client assets and the tools that made them
    for name in os.listdir(zpak):
        if name.endswith((".json", ".py")):
            shutil.copy2(os.path.join(zpak, name), os.path.join(dest, name))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])

"""Port Project Neltharion's Gilneas (Cataclysm's Worgen starting zone) to F-130_cata-gilneas-start.

  python cata_gilneas_port.py EXTRACT_DIR F130_DIR

EXTRACT_DIR is cata_zone_extract.py's output for Gilneas (see F-130's readme for the command). Rerun this after
changing it: it replaces F130_DIR/dbc and F130_DIR/sql and leaves readme.md, variables.sql and patches/ alone, so fixes
belong in this script, in cata_gilneas_fixes/ next to it (copied in at the end), or in variables.sql.

What it does to Neltharion's TrinityCore 4.3.4 rows:
- spawns move from Cataclysm's map 654 to Eastern Kingdoms (map 0) unchanged: Open Azeroth's map 0 has Cataclysm's
  Gilneas at the same coordinates. They get new guids (CREATURE_GUID, GAMEOBJECT_GUID); waypoint paths follow them
- tables are rewritten to AzerothCore's columns the way Zeppelin-Craft's goblin generator does it (F-013): models to
  creature_template_model, InhabitType to creature_template_movement, equipment to creature_equip_template ids, flags
  and faction to gameobject_template_addon, the quest text tables, loot to the Reference/QuestRequired columns, class
  trainers to the stock trainer of their class
- gossip menus and npc_text get new ids (MENU_BASE, TEXT_BASE), everywhere they're used
- terrain swaps are left out: the phases play on Open Azeroth's Gilneas (terrainswapmap 0)
- the Worgen race and faction are F-024's variables; Cataclysm race masks become the config.sql masks
- stock creatures, objects and quests the zone uses keep their stock rows (STOCK_*)
- Cataclysm items stock lacks are added from the 4.0.6a client (cata_items.py), with their displays; Cataclysm
  spells stock lacks from the 4.0.6a DBCs (cata406_dbc_port.py), following the spells they trigger; visuals and visual
  kits whose ids stock uses for something else stay stock's
- creature displays, their extras (with Cataclysm's NPC bake names) and object displays stock lacks come from the
  4.0.6a DBCs; the bakes and models they name are listed by tools/checks/f013_item_assets.py --modpak
- Neltharion's own server spells (151xxx) and the few 4.3.4-only ones are written by cata_gilneas_fixes/; rows that
  use spells, creatures, items or scripts nothing here has are dropped and listed at the end
"""
import collections, glob, os, re, shutil, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cata_zone_extract import values  # noqa: E402
from cata_items import CataItems, display_sql, sql_value, ITEM_TEMPLATE_COLUMNS  # noqa: E402
import cata406_dbc_port as c406  # noqa: E402

CATA_DBC = "D:/GitHub/References/Cataclysm/Cataclysm_data/dbc"
STOCK_DBC = "D:/GitHub/References/original-client-dbc"
FIXES_DIR = os.path.join(HERE, "cata_gilneas_fixes")
TAG = "F-130"
SQL_DIR = os.path.join("sql", "db-world", "base")

SOURCE_MAPS = (654, 655)
CREATURE_GUID = 13000001
GAMEOBJECT_GUID = 7000001
PATH_BASE = 13000000          # waypoint path ids: PATH_BASE + n
MENU_BASE = 520000            # gossip_menu.MenuID
TEXT_BASE = 520000            # npc_text.ID

# Stock rows the zone uses: spawned, never rewritten
STOCK_CREATURES = {385, 620, 883, 1412, 1420, 1933, 2914, 4075, 4076, 6368, 6491, 6827, 14881, 15717, 17467, 28332}
STOCK_GAMEOBJECTS = {1617, 1618, 1619, 1731, 183812}
STOCK_QUESTS = {3861}
# Neltharion's own server features and scripts its source doesn't have
DEAD_SCRIPTS = {"npc_starting_options", "npc_xp_rates", "npc_lady_sylvanas_gilneas", "npc_gilneas_city_guard_phase1",
                "npc_lieutenant_walden"}
# Scripts the core patch (patches/core/gilneas-start.patch) implements, under the same names
SCRIPTS = {"npc_by_the_skin_of_his_teeth_controller", "npc_gilnean_mastiff_pet", "npc_king_greymanes_horse",
           "npc_crowleys_horse_vehicle", "npc_crowleys_horse_spellclick", "npc_drowning_watchtman_spellclick",
           "npc_mountain_horse_worgen", "npc_summoned_mountain_horse_worgen", "npc_swift_mountain_horse_worgen",
           "npc_stagecoach_harness_worgen", "npc_stout_mountain_horse_worgen", "npc_captured_riding_bat_worgen",
           "npc_gilneas_liam_camera", "npc_gilneas_captured_worgen", "spell_round_up_horse",
           "spell_gen_dismount_cancel_all_shapeshifts"}
# Creatures only the C++ summons or credits, which the extract has to be told about (--creature)
SCRIPT_CREATURES = {35170, 35188, 35230, 35231, 35753, 35907, 36331, 36450, 36451, 36555, 36560, 38148, 38286, 38538,
                    38612, 38756, 43338, 75138}
# Spells the C++ uses that no row names, so the closure wouldn't find them
SCRIPT_SPELLS = {46598, 63313, 50630, 64630, 42716, 56685, 50345, 55034, 47433, 54421, 68218, 67503, 67805, 68228,
                 72799, 68630, 69196, 68903, 68908, 68917, 68940, 68916, 72764, 86285, 71506, 85682, 89147, 47020,
                 68735, 68730, 88467, 49417, 93477, 98274}
# Spells that can't be ported, replaced by stock or ported ones (0: drop the row)
SPELL_SUBSTITUTES = {97239: 6660}
# Spells the fixes folder writes (Neltharion's server spells, the 4.3.4-only ones)
FIXED_SPELLS = {98914, 97995, 100615, 101644, 151049, 151111, 151159, 151168, 151170, 151174, 151180, 151189,
                151190, 151200, 151205, 151235}

# Cataclysm class -> stock trainer id of that class (AzerothCore's `trainer`)
CLASS_TRAINER = {1: 1, 2: 3, 3: 7, 4: 9, 5: 11, 6: 13, 7: 14, 8: 16, 9: 31, 11: 33}
# Cataclysm race id -> config.sql race
RACE_VARS = {1: "Human", 2: "Orc", 3: "Dwarf", 4: "NightElf", 5: "Undead", 6: "Tauren", 7: "Gnome", 8: "Troll",
             9: "Goblin", 10: "BloodElf", 11: "Draenei", 22: "Worgen"}
CATA_ALLIANCE = 1 | 4 | 8 | 64 | 1024 | (1 << 21)
CATA_HORDE = 2 | 16 | 32 | 128 | 256 | 512
# Cataclysm's faction 1134 (Gilneas) is F-024's @WorgenFaction
FACTION_VARS = {1134: "@WorgenFaction"}
WORGEN_MODELS = {3141: "@WorgenMaleModel", 3142: "@WorgenFemaleModel"}

# SmartAI opcodes that differ between Neltharion's core and AzerothCore (Zeppelin-Craft's audit, _spellscope.py)
SAI_MAX_EVENT, SAI_MAX_ACTION = 74, 135
SAI_ACTION_REMAP = {85: 134}
SAI_ACTION_DROP = {16, 103, 114, 121}
SAI_EVENT_DROP = {66, 78}
SAI_SPELL_ACTIONS = {11, 28, 75, 85, 86, 134}
SAI_SPELL_EVENTS = {8, 31}
# Neltharion condition types AzerothCore doesn't have
CONDITION_DROP = {201, 202}
CONDITION_AURA, CONDITION_SPELL = 1, 25
# Neltharion's phase definition condition source (25) is F-013's 26
CONDITION_PHASE_SOURCE = (25, 26)
# AzerothCore has invisibility types 0-11 (it indexes an array by them): Cataclysm's quest invisibility types above
# that move to ones stock doesn't use (6 is drunk, 7 and 8 the stock generic quest invisibility)
INVISIBILITY_TYPES = {18: 9, 30: 10, 36: 11}
INVISIBILITY_AURAS = (18, 19)
FALLBACK_DISPLAY = 646           # what Zeppelin-Craft's generator uses for a display nothing has

dropped = collections.defaultdict(list)


# ---- reading -------------------------------------------------------------------------------------------------------
def rows(extract, table):
    path = os.path.join(extract, table + ".sql")
    if not os.path.exists(path):
        return []
    lines = open(path, encoding="utf8").read().split("\n")
    cols = [c.strip("` ") for c in lines[0].split("(", 1)[1].split(") VALUES")[0].split(",")]
    out = []
    for line in lines[1:]:
        line = line.strip().rstrip(",;")
        if line.startswith("("):
            out.append(dict(zip(cols, values(line[1:-1]))))
    return out


def dbc_ids(name):
    d = open(os.path.join(STOCK_DBC, name + ".dbc"), "rb").read()
    n, _, rs, _ = struct.unpack_from("<4I", d, 4)
    return {struct.unpack_from("<I", d, 20 + i * rs)[0] for i in range(n)}


# ---- writing -------------------------------------------------------------------------------------------------------
def insert(table, cols, data, delete=None, comment=None):
    """DELETE (optional) + one INSERT ... VALUES of `data` (lists in `cols` order)."""
    if not data:
        return ""
    out = ["-- " + comment] if comment else []
    if delete:
        out.append(delete)
    out.append("INSERT INTO `%s` (%s) VALUES\n%s;\n" % (
        table, ", ".join("`%s`" % c for c in cols),
        ",\n".join("  (" + ", ".join(sql_value(v) for v in r) + ")" for r in data)))
    return "\n".join(out)


def in_list(ids):
    return "(" + ", ".join(str(i) for i in sorted(ids)) + ")"


def fix_invisibility(columns):
    """Move a spell's invisibility / detection types above AzerothCore's into its range (INVISIBILITY_TYPES)."""
    for n in (1, 2, 3):
        if columns.get("effect_apply_aura_name_%d" % n) in INVISIBILITY_AURAS:
            k = "effect_misc_value_a_%d" % n
            columns[k] = INVISIBILITY_TYPES.get(columns.get(k, 0), columns.get(k, 0))


def spell_blocks(path):
    """{id: {column: SQL literal}} of the `spell` blocks of a dbc/ file, in column order."""
    out = {}
    for block in re.findall(r"INSERT INTO `spell` SET\n(.*?);\n", open(path, encoding="utf8").read(), re.S):
        cols = dict(re.findall(r"^\s*`(\w+)` = (.*?),?$", block, re.M))
        out[int(cols["id"])] = cols
    return out


class Port:
    def __init__(self, extract, dest):
        self.x, self.dest = extract, dest
        self.files = {}                                   # file name -> SQL
        self.t = {t: rows(extract, t) for t in (
            "creature", "gameobject", "creature_template", "creature_template_addon", "creature_addon",
            "creature_equip_template", "creature_model_info", "creature_text", "creature_questrelation",
            "creature_involvedrelation", "gameobject_template", "gameobject_questrelation",
            "gameobject_involvedrelation", "quest_template", "quest_poi", "quest_poi_points", "smart_scripts",
            "conditions", "waypoint_data", "waypoints", "gossip_menu", "gossip_menu_option", "npc_text",
            "creature_loot_template", "gameobject_loot_template", "pickpocketing_loot_template",
            "skinning_loot_template", "npc_spellclick_spells", "vehicle_template_accessory", "npc_vendor",
            "phase_definitions", "spell_area", "spell_script_names", "spell_target_position")}
        self.stock_spells = dbc_ids("Spell")
        self.stock_sounds = dbc_ids("SoundEntries")
        self.stock_cdisp = dbc_ids("CreatureDisplayInfo")
        self.stock_extra = dbc_ids("CreatureDisplayInfoExtra")
        self.stock_models = dbc_ids("CreatureModelData")
        self.stock_gdisp = dbc_ids("GameObjectDisplayInfo")
        self.stock_ft = dbc_ids("FactionTemplate")
        self.stock_npcsounds = dbc_ids("NPCSounds")
        self.stock_soundData = dbc_ids("CreatureSoundData")
        self.items = CataItems(CATA_DBC, STOCK_DBC)
        self.entries = {r["entry"] for r in self.t["creature_template"]} - STOCK_CREATURES
        self.goentries = {r["entry"] for r in self.t["gameobject_template"]} - STOCK_GAMEOBJECTS
        self.quests = {r["Id"] for r in self.t["quest_template"]} - STOCK_QUESTS
        self.known_creatures = self.entries | STOCK_CREATURES
        self.cguid, self.gguid, self.paths = {}, {}, {}
        for r in sorted(self.t["creature"], key=lambda r: r["guid"]):
            self.cguid[r["guid"]] = CREATURE_GUID + len(self.cguid)
        for r in sorted(self.t["gameobject"], key=lambda r: r["guid"]):
            self.gguid[r["guid"]] = GAMEOBJECT_GUID + len(self.gguid)
        menus = sorted({r["entry"] for r in self.t["gossip_menu"]} | {r["menu_id"] for r in self.t["gossip_menu_option"]})
        self.menu = {m: MENU_BASE + i for i, m in enumerate(menus)}
        self.text = {t: TEXT_BASE + i for i, t in enumerate(sorted({r["ID"] for r in self.t["npc_text"]}))}
        self.item_ids = {}                                # Cataclysm item id -> id here
        self.spells = set()                               # Cataclysm spells to port

    # ---- ids --------------------------------------------------------------------------------------------------
    def spell_ok(self, sid):
        sid = SPELL_SUBSTITUTES.get(sid, sid)
        return sid if (not sid or sid in self.stock_spells or sid in self.spells or sid in FIXED_SPELLS) else None

    def item(self, cata):
        """Item id to use for a Cataclysm item id (0 when nothing has it)."""
        if not cata or cata in self.items.stock_items:
            return cata
        if cata in self.item_ids:
            return self.item_ids[cata]
        if not self.items.has(cata):
            dropped["items nothing has"].append(cata)
            self.item_ids[cata] = 0
            return 0
        self.item_ids[cata] = cata                     # Cataclysm's ids above stock's are free; kept for readability
        return cata

    def race_mask(self, mask):
        """(word 1, word 2) expressions for a Cataclysm race mask."""
        if mask in (0, -1) or mask & CATA_ALLIANCE == CATA_ALLIANCE and mask & CATA_HORDE == CATA_HORDE:
            return 0, 0
        if mask == CATA_ALLIANCE:
            return "@AllianceMask", "@AllianceMask_2"
        if mask == CATA_HORDE:
            return "@HordeMask", "@HordeMask_2"
        names = [RACE_VARS[b + 1] for b in range(32) if mask & (1 << b) and b + 1 in RACE_VARS]
        if not names:
            return 0, 0
        return (" | ".join("@%sMask" % n for n in names), " | ".join("@%sMask_2" % n for n in names))

    # ---- spells -----------------------------------------------------------------------------------------------
    def collect_spells(self):
        want = set(SCRIPT_SPELLS)
        for r in self.t["smart_scripts"]:
            if r["action_type"] in SAI_SPELL_ACTIONS:
                want.add(r["action_param1"])
            if r["event_type"] in SAI_SPELL_EVENTS:
                want.add(r["event_param1"])
        for r in self.t["creature_template"]:
            want |= {r["spell%d" % i] for i in range(1, 9)}
        for t in ("creature_addon", "creature_template_addon"):
            for r in self.t[t]:
                want |= {int(a) for a in (r["auras"] or "").split()}
        for r in self.t["npc_spellclick_spells"]:
            want.add(r["spell_id"])
        for r in self.t["spell_area"]:
            want |= {r["spell"], r["aura_spell"]}
        for r in self.t["quest_template"]:
            want |= {r["RewardSpell"], r["RewardSpellCast"], r["SourceSpellId"]}
            want |= {r["RequiredSpellCast%d" % i] for i in range(1, 5)}
        for r in self.t["conditions"]:
            if r["ConditionTypeOrReference"] in (CONDITION_AURA, CONDITION_SPELL):
                want.add(r["ConditionValue1"])
            if r["SourceTypeOrReferenceId"] in (13, 17):
                want.add(r["SourceEntry"])
        want = {abs(s) for s in want if s} - self.stock_spells - FIXED_SPELLS - set(SPELL_SUBSTITUTES)
        port = c406.Port(CATA_DBC, STOCK_DBC, type("A", (), dict(effect_name=[], no_sound=[], sound_map=[],
                                                                   sound_ext=None, skip_kit=[], skip_visual=[]))())
        port.skip_kit, port.skip_visual = set(), set()
        cata = c406.Dbc(os.path.join(CATA_DBC, "Spell.dbc"))
        effects = collections.defaultdict(list)
        for e in c406.Dbc(os.path.join(CATA_DBC, "SpellEffect.dbc")).records:
            effects[e[c406.EFFECT["spell"]]].append(e)
        todo, done, self.summoned = sorted(want), set(), set()
        while todo:
            sid = todo.pop()
            if sid in done:
                continue
            done.add(sid)
            if not cata.get(sid):
                dropped["spells neither stock nor 4.0.6a has"].append(sid)
                continue
            while True:
                try:
                    port.spells([sid])
                    break
                except SystemExit as e:
                    m = re.match(r"(spellvisualkit|spellvisual) (\d+) ", str(e))
                    n = re.match(r"SpellVisualEffectName (\d+) ", str(e))
                    if n:                                 # stock uses the id for another model: leave it out
                        port.effect_map[int(n.group(1))] = 0
                        continue
                    if not m:
                        dropped["spells 3.3.5a can't run"].append("%d (%s)" % (sid, e))
                        port.out.get("spell", {}).pop(sid, None)
                        break
                    (port.skip_kit if m.group(1) == "spellvisualkit" else port.skip_visual).add(int(m.group(2)))
            if sid not in port.out.get("spell", {}):
                continue
            self.spells.add(sid)
            fix_invisibility(port.out["spell"][sid][0])
            for e in effects[sid]:
                trig, kind, misc = e[c406.EFFECT["trigger"]], e[c406.EFFECT["effect"]], e[c406.EFFECT["misc_a"]]
                if trig and trig not in self.stock_spells and trig not in FIXED_SPELLS:
                    todo.append(trig)
                if kind in (28, 56, 90, 134) and misc:            # summon, summon pet, kill credit
                    self.summoned.add(misc)
        self.neltharion_spells()
        missing = sorted((self.summoned | SCRIPT_CREATURES) - self.known_creatures)
        if missing:
            print("creatures the spells summon or credit that the extract lacks (rerun cata_zone_extract.py with "
                  "--creature for them): " + ",".join(map(str, missing)))
        port.write(os.path.join(self.dest, "dbc"), "[%s]_cata" % TAG, "for F-130 (see its readme)")
        return sorted(port.skip_kit), sorted(port.skip_visual)

    def neltharion_spells(self):
        """Neltharion's server spells and the 4.3.4-only ones (FIXED_SPELLS), as 3.3.5a Spell.dbc rows: F-013 has
        98914 and 100615 from Zeppelin-Craft's 4.3.4 client; the others are its 98914 row with Neltharion's fields
        (spell_dbc + spelleffect_dbc in its world database)."""
        f013 = spell_blocks(os.path.join(HERE, "..", "..", "modpaks", "F-013_zep-goblin-start", "dbc",
                                         "[AUTO,F-011]_spell.sql"))
        base = dict(f013[98914])
        for k in base:
            if k.startswith("effect_") and k[-2:] in ("_1", "_2", "_3"):
                base[k] = "0"
        out = {98914: f013[98914], 100615: dict(f013[100615])}
        q = lambda s: "'" + s.replace("'", "''") + "'"
        hidden = (696254848, 1056, 273170437, 269681152, 8388736, 393224, 4608, 0)   # Neltharion's hidden-spell set
        # id: (name, attributes or None, duration index, range index, [effects])
        defs = {
            97995: ("See Quest Invis 22", None, 21, 1, [dict(effect=6, aura=19, misc=30, target_a=1)]),
            101644: ("Update Bind Post-Sacrifices", None, 0, 1, [dict(effect=11, misc=4817, target_a=1, target_b=17)]),
            151049: ("Gilneas phase 64", (0,) * 8, 21, 1, [dict(effect=6, aura=261, misc=64, target_a=1)]),
            151111: ("Gilneas fear", (538968320, 136, 67108868, 268435520, 2176, 0, 0, 0), 31, 13,
                     [dict(effect=6, aura=7, amplitude=1, target_a=1)]),
            151159: ("Gilneas dummy", hidden, 1, 13, [dict(effect=3, target_a=1)]),
            151168: ("Gilneas ping 151168", hidden, 1, 1, [dict(effect=3, radius=28, target_a=22, target_b=7)]),
            151170: ("Gilneas ping 151170", hidden, 1, 1, [dict(effect=3, radius=28, target_a=22, target_b=7)]),
            151174: ("Gilneas ping 151174", hidden, 1, 13, [dict(effect=3, radius=11, target_a=22, target_b=7)]),
            151180: ("Gilneas ping 151180", hidden, 1, 1, [dict(effect=3, radius=28, target_a=22, target_b=7)]),
            151189: ("Gilneas ping 151189", hidden, 1, 7, [dict(effect=3, radius=28, target_a=22, target_b=7)]),
            # Cataclysm summon properties 3122 and 2993 aren't in 3.3.5a: 64 is a plain guardian-less summon
            151190: ("Gilneas summon 38507", hidden, 6, 13, [dict(effect=28, misc=38507, misc_b=64, target_a=17)]),
            151200: ("Gilneas to Darnassus", hidden, 1, 1, [dict(effect=5, target_a=1, target_b=17)]),
            151205: ("Gilneas summon 36292", hidden, 21, 1, [dict(effect=28, misc=36292, misc_b=64, target_a=32)]),
            151235: ("Dismount and Cancel All Shapeshifts", hidden, 1, 1, [dict(effect=77, target_a=1)]),
        }
        names = dict(effect="effect_%d", aura="effect_apply_aura_name_%d", misc="effect_misc_value_a_%d",
                     misc_b="effect_misc_value_b_%d", target_a="effect_implicit_target_a_%d",
                     target_b="effect_implicit_target_b_%d", radius="effect_radius_index_%d",
                     amplitude="effect_amplitude_%d")
        for sid, (name, at, dur, rng, effects) in defs.items():
            row = dict(base)
            row.update(id=str(sid), spell_name_enus=q(name), duration_index=str(dur), range_index=str(rng))
            if at is not None:
                for k, v in zip(("attributes", "attributes_ex_1", "attributes_ex_2", "attributes_ex_3",
                                 "attributes_ex_4", "attributes_ex_5", "attributes_ex_6", "attributes_ex_7"), at):
                    row[k] = str(v)
            for i, e in enumerate(effects):
                for k, v in e.items():
                    row[names[k] % (i + 1)] = str(v)
            out[sid] = row
        for row in out.values():
            for n in (1, 2, 3):
                if row.get("effect_apply_aura_name_%d" % n) in ("18", "19"):
                    k = "effect_misc_value_a_%d" % n
                    row[k] = str(INVISIBILITY_TYPES.get(int(row[k]), int(row[k])))
        text = ["-- Neltharion's server-side spells and the 4.3.4-only spells the zone uses, as Spell.dbc rows. "
                "Generated by tools/races/cata_gilneas_port.py (neltharion_spells).\n"]
        for sid in sorted(out):
            row = out[sid]
            text.append("DELETE FROM `spell` WHERE `id` = %d;\nINSERT INTO `spell` SET\n%s;\n" % (
                sid, ",\n".join("  `%s` = %s" % (k, v) for k, v in row.items())))
        self.files[os.path.join("dbc", "[%s]_server_spells.sql" % TAG)] = "\n".join(text)

    # ---- creatures ------------------------------------------------------------------------------------------
    def creatures(self):
        T = self.t
        ai = {r["entryorguid"] for r in T["smart_scripts"] if r["source_type"] == 0 and r["entryorguid"] > 0}
        tmpl, models, movement, model_info, equip = [], [], [], [], []
        displays = set()
        equip_by_id = {r["entry"]: r for r in T["creature_equip_template"]}
        self.equip_ids = {}                                # (entry, Neltharion equipment id) -> AzerothCore ID
        for r in sorted(T["creature_template"], key=lambda r: r["entry"]):
            e = r["entry"]
            if e in STOCK_CREATURES:
                continue
            script = r["ScriptName"] or ""
            if script in DEAD_SCRIPTS or (script and script not in SCRIPTS):
                if script and script not in DEAD_SCRIPTS:
                    dropped["script names nothing implements"].append("%d %s" % (e, script))
                script = ""
            aname = r["AIName"] or ""
            if aname == "NullAI":
                aname = "NullCreatureAI"
            elif aname == "SmartAI" and e not in ai:
                aname = ""
            flags_extra = (r["flags_extra"] or 0) & 0x1FC1FF
            trainer = CLASS_TRAINER.get(r["trainer_class"]) if (r["npcflag"] & 0x10 and r["trainer_type"] == 0) else None
            if trainer:
                self.trainers.append((e, trainer))
            tmpl.append([e, r["difficulty_entry_1"], r["difficulty_entry_2"], r["difficulty_entry_3"],
                         r["KillCredit1"], r["KillCredit2"], r["name"], r["subname"] or None, r["IconName"] or None,
                         self.menu.get(r["gossip_menu_id"], 0), r["minlevel"], r["maxlevel"], min(r["exp"], 2),
                         self.faction(r["faction_A"]), r["npcflag"], r["speed_walk"], r["speed_run"], r["speed_swim"],
                         r["speed_fly"], 18, r["rank"], r["dmgschool"], r["dmg_multiplier"] or 1,
                         r["baseattacktime"] or 2000, r["rangeattacktime"] or 2000, 1, 1, r["unit_class"] or 1,
                         r["unit_flags"], r["unit_flags2"], r["dynamicflags"], r["family"], r["type"],
                         r["type_flags"], r["lootid"], r["pickpocketloot"], r["skinloot"], r["PetSpellDataId"],
                         r["VehicleId"], r["mingold"], r["maxgold"], aname, r["MovementType"],
                         r["HoverHeight"], r["Health_mod"], r["Mana_mod"], r["Armor_mod"], 1, r["RacialLeader"],
                         0, r["RegenHealth"], 0, flags_extra, script, 0])
            idx = 0
            for k in ("modelid1", "modelid2", "modelid3", "modelid4"):
                d = r[k]
                if d and d not in [m[2] for m in models if m[0] == e]:
                    models.append([e, idx, d, r["scale"] or 1, 1, 0])
                    displays.add(d)
                    idx += 1
            inhabit = r["InhabitType"] or 3
            movement.append([e, 1 if inhabit & 1 else 0, 1 if inhabit & 2 else 0, 1 if inhabit & 4 else 0])
            if r["equipment_id"] and r["equipment_id"] in equip_by_id:
                self.equip_ids[(e, r["equipment_id"])] = 1
        # spawn-specific equipment
        for s in T["creature"]:
            e, q = s["id"], s["equipment_id"]
            if q > 0 and q in equip_by_id and (e, q) not in self.equip_ids and e not in STOCK_CREATURES:
                self.equip_ids[(e, q)] = 1 + sum(1 for k in self.equip_ids if k[0] == e)
        for (e, q), i in sorted(self.equip_ids.items()):
            x = equip_by_id[q]
            equip.append([e, i] + [self.item(x["itemEntry%d" % n]) for n in (1, 2, 3)] + [0])
        info = {r["modelid"]: r for r in T["creature_model_info"]}
        self.displays = self.port_displays(displays)
        for d in sorted(self.displays):
            if d in info and d not in self.stock_cdisp:
                r = info[d]
                model_info.append([d, r["bounding_radius"], r["combat_reach"], r["gender"], 0, 0])
        for m in models:
            if m[2] not in self.stock_cdisp and m[2] not in self.displays:
                dropped["creature displays nothing has (fell back to %d)" % FALLBACK_DISPLAY].append(m[2])
                m[2] = FALLBACK_DISPLAY
        cols = ("entry difficulty_entry_1 difficulty_entry_2 difficulty_entry_3 KillCredit1 KillCredit2 name subname "
                "IconName gossip_menu_id minlevel maxlevel exp faction npcflag speed_walk speed_run speed_swim "
                "speed_flight detection_range rank dmgschool DamageModifier BaseAttackTime RangeAttackTime BaseVariance "
                "RangeVariance unit_class unit_flags unit_flags2 dynamicflags family type type_flags lootid "
                "pickpocketloot skinloot PetSpellDataId VehicleId mingold maxgold AIName MovementType HoverHeight "
                "HealthModifier ManaModifier ArmorModifier ExperienceModifier RacialLeader movementId RegenHealth "
                "CreatureImmunitiesId flags_extra ScriptName VerifiedBuild").split()
        ents = in_list(self.entries)
        self.write("10_creature_template", insert("creature_template", cols, tmpl,
                                                  "DELETE FROM `creature_template` WHERE `entry` IN %s;" % ents))
        self.write("11_creature_template_model", insert(
            "creature_template_model", "CreatureID Idx CreatureDisplayID DisplayScale Probability VerifiedBuild".split(),
            models, "DELETE FROM `creature_template_model` WHERE `CreatureID` IN %s;" % ents))
        self.write("12_creature_template_movement", insert(
            "creature_template_movement", "CreatureId Ground Swim Flight".split(), movement,
            "DELETE FROM `creature_template_movement` WHERE `CreatureId` IN %s;" % ents))
        self.write("13_creature_model_info", insert(
            "creature_model_info", "DisplayID BoundingRadius CombatReach Gender DisplayID_Other_Gender VerifiedBuild".split(),
            model_info, "DELETE FROM `creature_model_info` WHERE `DisplayID` IN %s;" % in_list(r[0] for r in model_info)))
        self.write("14_creature_equip_template", insert(
            "creature_equip_template", "CreatureID ID ItemID1 ItemID2 ItemID3 VerifiedBuild".split(), equip,
            "DELETE FROM `creature_equip_template` WHERE `CreatureID` IN %s;" % ents))
        # template addons
        addon = []
        for r in T["creature_template_addon"]:
            if r["entry"] in self.entries:
                addon.append([r["entry"], self.path(r["path_id"]), r["mount"], r["bytes1"], r["bytes2"], r["emote"],
                              0, self.auras(r["auras"], "creature_template_addon %d" % r["entry"])])
        self.write("15_creature_template_addon", insert(
            "creature_template_addon", "entry path_id mount bytes1 bytes2 emote visibilityDistanceType auras".split(),
            addon, "DELETE FROM `creature_template_addon` WHERE `entry` IN %s;" % ents))
        # texts
        text = [[r["entry"], r["groupid"], r["id"], r["text"], r["type"], r["language"], r["probability"], r["emote"],
                 r["duration"], r["sound"] if r["sound"] in self.stock_sounds else 0, 0, r["text_range"] or 0,
                 r["comment"] or ""] for r in T["creature_text"] if r["entry"] in self.entries]
        self.write("16_creature_text", insert(
            "creature_text", "CreatureID GroupID ID Text Type Language Probability Emote Duration Sound BroadcastTextId "
            "TextRange comment".split(), text, "DELETE FROM `creature_text` WHERE `CreatureID` IN %s;" % ents))

    def faction(self, ft):
        if not ft:
            return 35
        if ft in self.stock_ft:
            return ft
        self.faction_templates.add(ft)
        return ft

    def auras(self, text, where):
        keep = []
        for a in (text or "").split():
            s = self.spell_ok(int(a))
            if s:
                keep.append(str(s))
            else:
                dropped["auras of spells nothing has"].append("%s on %s" % (a, where))
        return " ".join(keep) or None

    def path(self, p):
        if not p:
            return 0
        if p not in self.paths:
            self.paths[p] = PATH_BASE + len(self.paths) + 1
        return self.paths[p]

    # ---- displays ---------------------------------------------------------------------------------------------
    def port_displays(self, ids):
        """Port the Cataclysm creature displays stock lacks; returns the ids that now exist."""
        cd = c406.Dbc(os.path.join(CATA_DBC, "CreatureDisplayInfo.dbc"))
        ce = c406.Dbc(os.path.join(CATA_DBC, "CreatureDisplayInfoExtra.dbc"))
        out_d, out_e, ok = [], [], set()
        for d in sorted(ids):
            if d in self.stock_cdisp:
                ok.add(d)
                continue
            r = cd.get(d)
            if not r:
                continue
            model = WORGEN_MODELS.get(r[1], r[1])
            if model == r[1] and r[1] not in self.stock_models:
                dropped["displays whose model stock lacks"].append("%d (model %d)" % (d, r[1]))
                continue
            extra = r[3]
            if extra and extra not in self.stock_extra:
                x = ce.get(extra)
                if not x:
                    continue
                race = "@Worgen" if x[1] == 22 else x[1]
                out_e.append(dict(id=extra, race=race, gender=x[2], skin_color=x[3], face_type=x[4],
                                  hair_style=x[5], hair_color=x[6], facial_hair=x[7],
                                  **{k: self.items.display_id(v) if v > 0 else 0 for k, v in zip(
                                      ("helm_id", "shoulders_id", "shirt_id", "chest_id", "belt_id", "legs_id",
                                       "boots_id", "wrists_id", "gloves_id", "tabard_id", "cape_id"), x[8:19])},
                                  can_equip=x[19], texture=ce.s(x[20])))
                self.bakes.add(ce.s(x[20]))
            out_d.append(dict(id=d, model_id=model, sound_id=r[2] if r[2] in self.stock_soundData else 0,
                              extended_display_info_id=extra, creature_model_scale=c406.f32(r[4]),
                              creature_model_alpha=r[5], texture_variation_1=cd.s(r[6]), texture_variation_2=cd.s(r[7]),
                              texture_variation_3=cd.s(r[8]), portrait_texture_name=cd.s(r[9]), blood_level=r[10],
                              blood_id=r[11], npc_sound_id=r[12] if r[12] in self.stock_npcsounds else 0,
                              praticle_color_id=r[13], creature_geoset_data=r[14], obj_effect_package_id=0))
            ok.add(d)
        self.write_dbc("creaturedisplayinfoextra", out_e, "Cataclysm NPC looks (CreatureDisplayInfoExtra, 4.0.6a); the "
                       "bakes they name are Textures\\BakedNpcTextures\\<texture>")
        self.write_dbc("creaturedisplayinfo", out_d, "Cataclysm creature displays (4.0.6a) stock lacks")
        return ok

    def write_dbc(self, table, data, comment):
        if not data:
            return
        out = ["-- %s. Generated by tools/races/cata_gilneas_port.py.\n" % comment]
        for r in data:
            out.append("DELETE FROM `%s` WHERE `id` = %s;\nINSERT INTO `%s` SET\n%s;\n" % (
                table, sql_value(r["id"]), table, ",\n".join("  `%s` = %s" % (k, sql_value(v)) for k, v in r.items())))
        self.files[os.path.join("dbc", "[%s]_%s.sql" % (TAG, table))] = "\n".join(out)

    # ---- spawns -----------------------------------------------------------------------------------------------
    def spawns(self):
        T = self.t
        c, a = [], []
        for r in sorted(T["creature"], key=lambda r: r["guid"]):
            e = r["id"]
            if e not in self.known_creatures:
                continue
            q = r["equipment_id"]
            eq = 0 if q < 0 or e in STOCK_CREATURES else (self.equip_ids.get((e, q), 0) if q > 0 else
                                                          (1 if any(k[0] == e for k in self.equip_ids) else 0))
            mt = r["MovementType"]
            c.append([self.cguid[r["guid"]], e, 0, 0, 0, 1, r["phaseMask"], eq, r["position_x"], r["position_y"],
                      r["position_z"], r["orientation"], r["spawntimesecs"], r["spawndist"], 0, 1, 0, mt, 0, 0, 0,
                      "", 0, 1, "[gen F-130 Gilneas]"])
        for r in T["creature_addon"]:
            g = self.cguid.get(r["guid"])
            if g:
                a.append([g, self.path(r["path_id"]), r["mount"], r["bytes1"], r["bytes2"], r["emote"], 0,
                          self.auras(r["auras"], "spawn %d" % r["guid"]), ""])
        g = [[self.gguid[r["guid"]], r["id"], 0, 0, 0, 1, r["phaseMask"], r["position_x"], r["position_y"],
              r["position_z"], r["orientation"], r["rotation0"], r["rotation1"], r["rotation2"], r["rotation3"],
              r["spawntimesecs"], r["animprogress"], r["state"], "", 0, "[gen F-130 Gilneas]"]
             for r in sorted(T["gameobject"], key=lambda r: r["guid"]) if r["id"] in self.goentries | STOCK_GAMEOBJECTS]
        self.write("40_creature", insert(
            "creature", "guid id map zoneId areaId spawnMask phaseMask equipment_id position_x position_y position_z "
            "orientation spawntimesecs wander_distance currentwaypoint curhealth curmana MovementType npcflag "
            "unit_flags dynamicflags ScriptName VerifiedBuild CreateObject Comment".split(), c,
            "DELETE FROM `creature` WHERE `Comment` LIKE '[gen F-130%';"))
        self.write("41_creature_addon", insert(
            "creature_addon", "guid path_id mount bytes1 bytes2 emote visibilityDistanceType auras Comment".split(), a,
            "DELETE FROM `creature_addon` WHERE `guid` BETWEEN %d AND %d;" % (CREATURE_GUID, CREATURE_GUID + 99999)))
        self.write("42_gameobject", insert(
            "gameobject", "guid id map zoneId areaId spawnMask phaseMask position_x position_y position_z orientation "
            "rotation0 rotation1 rotation2 rotation3 spawntimesecs animprogress state ScriptName VerifiedBuild "
            "Comment".split(), g, "DELETE FROM `gameobject` WHERE `Comment` LIKE '[gen F-130%';"))
        wp = []
        for r in T["waypoint_data"]:
            if r["id"] in self.paths:
                wp.append([self.paths[r["id"]], r["point"], r["position_x"], r["position_y"], r["position_z"],
                           r["orientation"], "", r["delay"], r["move_flag"], 0, 100, 0])
        self.write("43_waypoint_data", insert(
            "waypoint_data", "id point position_x position_y position_z orientation Comment delay move_type action "
            "action_chance wpguid".split(), wp,
            "DELETE FROM `waypoint_data` WHERE `id` BETWEEN %d AND %d;" % (PATH_BASE, PATH_BASE + 99999)))
        w = [[r["entry"], r["pointid"], r["position_x"], r["position_y"], r["position_z"], None, 0,
              r["point_comment"] or ""] for r in T["waypoints"]]
        self.write("44_waypoints", insert(
            "waypoints", "entry pointid position_x position_y position_z orientation delay point_comment".split(), w,
            "DELETE FROM `waypoints` WHERE `entry` IN %s;" % in_list({r[0] for r in w})))

    # ---- gameobjects ------------------------------------------------------------------------------------------
    def gameobjects(self):
        gd = c406.Dbc(os.path.join(CATA_DBC, "GameObjectDisplayInfo.dbc"))
        tmpl, addon, qitem, disp = [], [], [], []
        ai = {r["entryorguid"] for r in self.t["smart_scripts"] if r["source_type"] == 1 and r["entryorguid"] > 0}
        for r in sorted(self.t["gameobject_template"], key=lambda r: r["entry"]):
            e = r["entry"]
            if e in STOCK_GAMEOBJECTS:
                continue
            d = r["displayId"]
            if d and d not in self.stock_gdisp and d not in {x["id"] for x in disp}:
                x = gd.get(d)
                if x:
                    disp.append(dict(id=d, model_name=gd.s(x[1]), **{"sound_%d" % (i + 1): x[2 + i] if x[2 + i] in
                                     self.stock_sounds else 0 for i in range(10)},
                                     **dict(zip(("geo_box_min_x", "geo_box_min_y", "geo_box_min_z", "geo_box_max_x",
                                                 "geo_box_max_y", "geo_box_max_z"), (c406.f32(v) for v in x[12:18])))))
                else:
                    dropped["object displays nothing has"].append(d)
            data = [r["data%d" % i] for i in range(24)]
            if r["type"] == 2 and data[3]:            # questgiver gossip menu
                data[3] = self.menu.get(data[3], 0)
            script = r["ScriptName"] if r["ScriptName"] in SCRIPTS else ""
            tmpl.append([e, r["type"], d, r["name"], r["IconName"] or "", r["castBarCaption"] or "", r["unk1"] or "",
                         r["size"]] + data + ["SmartGameObjectAI" if r["AIName"] and e in ai else "", script, 0])
            addon.append([e, self.faction(r["faction"]) if r["faction"] else 0, r["flags"]])
            for i in range(1, 7):
                if r["questItem%d" % i]:
                    qitem.append([e, i - 1, self.item(r["questItem%d" % i]), 0])
        cols = ("entry type displayId name IconName castBarCaption unk1 size " + " ".join("Data%d" % i for i in range(24))
                + " AIName ScriptName VerifiedBuild").split()
        ents = in_list(self.goentries)
        self.write("20_gameobject_template", insert("gameobject_template", cols, tmpl,
                                                    "DELETE FROM `gameobject_template` WHERE `entry` IN %s;" % ents))
        self.write("21_gameobject_template_addon", insert(
            "gameobject_template_addon", "entry faction flags".split(), addon,
            "DELETE FROM `gameobject_template_addon` WHERE `entry` IN %s;" % ents))
        self.write("22_gameobject_questitem", insert(
            "gameobject_questitem", "GameObjectEntry Idx ItemId VerifiedBuild".split(), qitem,
            "DELETE FROM `gameobject_questitem` WHERE `GameObjectEntry` IN %s;" % ents))
        self.write_dbc("gameobjectdisplayinfo", disp, "Cataclysm object displays (4.0.6a) stock lacks")

    # ---- gossip -----------------------------------------------------------------------------------------------
    def gossip(self):
        T = self.t
        menus = [[self.menu[r["entry"]], self.text.get(r["text_id"], r["text_id"])] for r in T["gossip_menu"]]
        opts = [[self.menu[r["menu_id"]], r["id"], r["option_icon"], r["option_text"] or "", 0, r["option_id"],
                 r["npc_option_npcflag"], self.menu.get(r["action_menu_id"], 0), r["action_poi_id"], r["box_coded"],
                 r["box_money"], r["box_text"] or "", 0] for r in T["gossip_menu_option"]]
        texts = []
        for r in T["npc_text"]:
            row = [self.text[r["ID"]]]
            for i in range(8):
                row += [r["text%d_0" % i] or "", r["text%d_1" % i] or "", 0, r["lang%d" % i], r["prob%d" % i]]
                row += [r["em%d_%d" % (i, j)] for j in range(6)]
            texts.append(row + [0])
        cols = ["ID"]
        for i in range(8):
            cols += ["text%d_0" % i, "text%d_1" % i, "BroadcastTextID%d" % i, "lang%d" % i, "Probability%d" % i]
            cols += ["em%d_%d" % (i, j) for j in range(6)]
        cols.append("VerifiedBuild")
        self.write("25_npc_text", insert("npc_text", cols, texts, "DELETE FROM `npc_text` WHERE `ID` BETWEEN %d AND %d;"
                                         % (TEXT_BASE, TEXT_BASE + 9999)))
        self.write("26_gossip_menu", insert("gossip_menu", ["MenuID", "TextID"], menus,
                                            "DELETE FROM `gossip_menu` WHERE `MenuID` BETWEEN %d AND %d;"
                                            % (MENU_BASE, MENU_BASE + 9999)))
        self.write("27_gossip_menu_option", insert(
            "gossip_menu_option", "MenuID OptionID OptionIcon OptionText OptionBroadcastTextID OptionType OptionNpcFlag "
            "ActionMenuID ActionPoiID BoxCoded BoxMoney BoxText BoxBroadcastTextID".split(), opts,
            "DELETE FROM `gossip_menu_option` WHERE `MenuID` BETWEEN %d AND %d;" % (MENU_BASE, MENU_BASE + 9999)))

    # ---- quests -----------------------------------------------------------------------------------------------
    def quests_(self):
        T = self.t
        qt, addon, offer, req = [], [], [], []
        for s in sorted(T["quest_template"], key=lambda r: r["Id"]):
            q = s["Id"]
            if q in STOCK_QUESTS:
                continue
            races = self.race_mask(s["RequiredRaces"])
            it = self.item
            row = [q, s["Method"], s["Level"], s["MinLevel"], s["ZoneOrSort"], s["Type"], s["SuggestedPlayers"],
                   0, 0, 0, 0, s["NextQuestIdChain"], s["RewardXPId"], s["RewardOrRequiredMoney"],
                   s["RewardMoneyMaxLevel"], self.spell_ok(s["RewardSpellCast"]) or 0,
                   self.spell_ok(s["RewardSpell"]) or 0, s["RewardHonor"], 0, it(s["SourceItemId"]), s["Flags"],
                   s["RequiredPlayerKills"]]
            for n in range(1, 5):
                row += [it(s["RewardItemId%d" % n]), s["RewardItemCount%d" % n]]
            for n in range(1, 5):
                row += [it(s["RequiredSourceItemId%d" % n]), s["RequiredSourceItemCount%d" % n]]
            for n in range(1, 7):
                row += [it(s["RewardChoiceItemId%d" % n]), s["RewardChoiceItemCount%d" % n]]
            row += [0 if s["PointMapId"] in SOURCE_MAPS else s["PointMapId"], s["PointX"], s["PointY"],
                    s["PointOption"], s["RewardTitleId"], s["RewardTalents"], s["RewardArenaPoints"]]
            for n in range(1, 6):
                row += [s["RewardFactionId%d" % n] if s["RewardFactionId%d" % n] != 1134 else "@WorgenFaction",
                        s["RewardFactionValueId%d" % n], s["RewardFactionValueIdOverride%d" % n]]
            row += [s["LimitTime"], races[0], races[1], s["Title"] or "", s["Objectives"] or "", s["Details"] or "", "",
                    s["EndText"] or ""]
            for n in range(1, 5):
                row += [s["RequiredNpcOrGo%d" % n], s["RequiredNpcOrGoCount%d" % n]]
            for n in range(1, 7):
                row += [it(s["RequiredItemId%d" % n]), s["RequiredItemCount%d" % n]]
            row += [0] + [s["ObjectiveText%d" % n] or "" for n in range(1, 5)] + [0]
            qt.append(row)
            for n in range(1, 5):
                cast = s["RequiredSpellCast%d" % n]
                if cast and s["RequiredNpcOrGo%d" % n] > 0:
                    self.cast_credit.append((q, cast, s["RequiredNpcOrGo%d" % n]))
            addon.append([q, s["MaxLevel"], s["RequiredClasses"], self.spell_ok(s["SourceSpellId"]) or 0,
                          s["PrevQuestId"], s["NextQuestId"], s["ExclusiveGroup"], 0, s["RewardMailTemplateId"],
                          s["RewardMailDelay"], s["RequiredSkillId"], s["RequiredSkillPoints"],
                          s["RequiredMinRepFaction"], s["RequiredMaxRepFaction"], s["RequiredMinRepValue"],
                          s["RequiredMaxRepValue"], s["SourceItemCount"], s["SpecialFlags"] & 0xF])
            offer.append([q] + [s["OfferRewardEmote%d" % n] for n in range(1, 5)]
                         + [s["OfferRewardEmoteDelay%d" % n] for n in range(1, 5)] + [s["OfferRewardText"] or "", 0])
            req.append([q, s["EmoteOnComplete"], s["EmoteOnIncomplete"], s["RequestItemsText"] or "", 0])
        cols = ("ID QuestType QuestLevel MinLevel QuestSortID QuestInfoID SuggestedGroupNum RequiredFactionId1 "
                "RequiredFactionId2 RequiredFactionValue1 RequiredFactionValue2 RewardNextQuest RewardXPDifficulty "
                "RewardMoney RewardMoneyDifficulty RewardDisplaySpell RewardSpell RewardHonor RewardKillHonor StartItem "
                "Flags RequiredPlayerKills").split()
        cols += sum((["RewardItem%d" % n, "RewardAmount%d" % n] for n in range(1, 5)), [])
        cols += sum((["ItemDrop%d" % n, "ItemDropQuantity%d" % n] for n in range(1, 5)), [])
        cols += sum((["RewardChoiceItemID%d" % n, "RewardChoiceItemQuantity%d" % n] for n in range(1, 7)), [])
        cols += "POIContinent POIx POIy POIPriority RewardTitle RewardTalents RewardArenaPoints".split()
        cols += sum((["RewardFactionID%d" % n, "RewardFactionValue%d" % n, "RewardFactionOverride%d" % n]
                     for n in range(1, 6)), [])
        cols += ("TimeAllowed AllowableRaces AllowableRaces_2 LogTitle LogDescription QuestDescription AreaDescription "
                 "QuestCompletionLog").split()
        cols += sum((["RequiredNpcOrGo%d" % n, "RequiredNpcOrGoCount%d" % n] for n in range(1, 5)), [])
        cols += sum((["RequiredItemId%d" % n, "RequiredItemCount%d" % n] for n in range(1, 7)), [])
        cols += ["Unknown0"] + ["ObjectiveText%d" % n for n in range(1, 5)] + ["VerifiedBuild"]
        qs = in_list(self.quests)
        self.write("30_quest_template", insert("quest_template", cols, qt,
                                               "DELETE FROM `quest_template` WHERE `ID` IN %s;" % qs))
        self.write("31_quest_template_addon", insert(
            "quest_template_addon", "ID MaxLevel AllowableClasses SourceSpellID PrevQuestID NextQuestID ExclusiveGroup "
            "BreadcrumbForQuestId RewardMailTemplateID RewardMailDelay RequiredSkillID RequiredSkillPoints "
            "RequiredMinRepFaction RequiredMaxRepFaction RequiredMinRepValue RequiredMaxRepValue ProvidedItemCount "
            "SpecialFlags".split(), addon, "DELETE FROM `quest_template_addon` WHERE `ID` IN %s;" % qs))
        self.write("32_quest_offer_reward", insert(
            "quest_offer_reward", "ID Emote1 Emote2 Emote3 Emote4 EmoteDelay1 EmoteDelay2 EmoteDelay3 EmoteDelay4 "
            "RewardText VerifiedBuild".split(), offer, "DELETE FROM `quest_offer_reward` WHERE `ID` IN %s;" % qs))
        self.write("33_quest_request_items", insert(
            "quest_request_items", "ID EmoteOnComplete EmoteOnIncomplete CompletionText VerifiedBuild".split(), req,
            "DELETE FROM `quest_request_items` WHERE `ID` IN %s;" % qs))
        poi = [[r["questId"], r["id"], r["objIndex"], 0 if r["mapid"] in SOURCE_MAPS else r["mapid"],
                r["WorldMapAreaId"], r["FloorId"], 0, 0, 0] for r in T["quest_poi"] if r["questId"] in self.quests]
        pts = [[r["questId"], r["id"], r["idx"], r["x"], r["y"], 0] for r in T["quest_poi_points"]
               if r["questId"] in self.quests]
        self.write("34_quest_poi", insert("quest_poi", "QuestID id ObjectiveIndex MapID WorldMapAreaId Floor Priority "
                                          "Flags VerifiedBuild".split(), poi,
                                          "DELETE FROM `quest_poi` WHERE `QuestID` IN %s;" % qs))
        self.write("35_quest_poi_points", insert("quest_poi_points", "QuestID Idx1 Idx2 X Y VerifiedBuild".split(), pts,
                                                 "DELETE FROM `quest_poi_points` WHERE `QuestID` IN %s;" % qs))
        rel = lambda t, e: sorted({(r["id"], r["quest"]) for r in T[t] if r["quest"] in self.quests and r["id"] in e})
        for n, (t, src, ents) in enumerate((("creature_queststarter", "creature_questrelation", self.known_creatures),
                                            ("creature_questender", "creature_involvedrelation", self.known_creatures),
                                            ("gameobject_queststarter", "gameobject_questrelation", self.goentries),
                                            ("gameobject_questender", "gameobject_involvedrelation", self.goentries))):
            self.write("%d_%s" % (45 + n, t), insert(t, ["id", "quest"], rel(src, ents),
                                                     "DELETE FROM `%s` WHERE `quest` IN %s;" % (t, qs)))

    # ---- loot, vendors, trainers, clicks -------------------------------------------------------------------
    def loot(self):
        for n, t in enumerate(("creature_loot_template", "gameobject_loot_template", "pickpocketing_loot_template",
                               "skinning_loot_template")):
            data = []
            for r in self.t[t]:
                if r["mincountOrRef"] < 0:
                    dropped["loot references (Cataclysm world drops) left out"].append(r["entry"])
                    continue
                item = self.item(r["item"])
                if not item:
                    continue
                chance = r["ChanceOrQuestChance"]
                data.append([r["entry"], item, 0, abs(chance), 1 if chance < 0 else 0, r["lootmode"], r["groupid"],
                             r["mincountOrRef"], r["maxcount"]])
            ents = {r[0] for r in data}
            self.write("%d_%s" % (50 + n, t), insert(
                t, "Entry Item Reference Chance QuestRequired LootMode GroupId MinCount MaxCount".split(), data,
                "DELETE FROM `%s` WHERE `Entry` IN %s;" % (t, in_list(ents)) if ents else None))
        v = [[r["entry"], r["slot"], self.item(r["item"]), r["maxcount"], r["incrtime"], r["ExtendedCost"], 0]
             for r in self.t["npc_vendor"] if r["entry"] in self.entries and r["type"] == 1]
        v = [r for r in v if r[2]]
        self.write("55_npc_vendor", insert("npc_vendor", "entry slot item maxcount incrtime ExtendedCost VerifiedBuild"
                                           .split(), v, "DELETE FROM `npc_vendor` WHERE `entry` IN %s;"
                                           % in_list({r[0] for r in v}) if v else None))
        c = [[r["npc_entry"], self.spell_ok(r["spell_id"]), r["cast_flags"], r["user_type"]]
             for r in self.t["npc_spellclick_spells"] if r["npc_entry"] in self.entries]
        c = [r for r in c if r[1]]
        self.write("56_npc_spellclick_spells", insert("npc_spellclick_spells", "npc_entry spell_id cast_flags user_type"
                                                      .split(), c, "DELETE FROM `npc_spellclick_spells` WHERE "
                                                      "`npc_entry` IN %s;" % in_list({r[0] for r in c}) if c else None))
        self.write("57_creature_default_trainer", insert(
            "creature_default_trainer", ["CreatureId", "TrainerId"], self.trainers,
            "DELETE FROM `creature_default_trainer` WHERE `CreatureId` IN %s;" % in_list(r[0] for r in self.trainers)
            if self.trainers else None))
        acc = [[r["entry"], r["accessory_entry"], r["seat_id"], r["minion"], r["description"] or "", r["summontype"],
                r["summontimer"]] for r in self.t["vehicle_template_accessory"] if r["entry"] in self.entries]
        self.write("58_vehicle_template_accessory", insert(
            "vehicle_template_accessory", "entry accessory_entry seat_id minion description summontype summontimer"
            .split(), acc, "DELETE FROM `vehicle_template_accessory` WHERE `entry` IN %s;" % in_list(r[0] for r in acc)
            if acc else None))

    # ---- SmartAI and conditions -----------------------------------------------------------------------------
    def smart(self):
        out = []
        for r in self.t["smart_scripts"]:
            st, e = r["source_type"], r["entryorguid"]
            if st == 0 and e < 0:
                e = -self.cguid.get(-e, 0)
            elif st == 1 and e < 0:
                e = -self.gguid.get(-e, 0)
            if e == 0 or (st == 0 and e > 0 and e not in self.entries) or (st == 1 and e > 0 and e not in self.goentries):
                continue
            a, ev = SAI_ACTION_REMAP.get(r["action_type"], r["action_type"]), r["event_type"]
            p = [r["action_param%d" % i] for i in range(1, 7)]
            ep = [r["event_param%d" % i] for i in range(1, 5)]
            why = None
            if ev > SAI_MAX_EVENT or ev in SAI_EVENT_DROP:
                why = "event %d" % ev
            elif a > SAI_MAX_ACTION or a in SAI_ACTION_DROP:
                why = "action %d" % a
            if not why and a in SAI_SPELL_ACTIONS:
                s = self.spell_ok(p[0])
                why = None if s else "spell %d" % p[0]
                p[0] = s or 0
            if not why and ev in SAI_SPELL_EVENTS and ep[0]:
                s = self.spell_ok(ep[0])
                why = None if s else "spell %d" % ep[0]
                ep[0] = s or 0
            if why:
                dropped["SmartAI rows (%s)" % why.split()[0]].append("%d/%d/%d %s" % (r["entryorguid"], st, r["id"], why))
                continue
            if a == 62 and p[0] in SOURCE_MAPS:          # teleport
                p[0] = 0
            if a in (56, 57):                            # add / remove item
                p[0] = self.item(p[0])
            if a == 98:                                  # send gossip menu (menu, npc_text)
                p[0], p[1] = self.menu.get(p[0], p[0]), self.text.get(p[1], p[1])
            if ev == 62:                                 # gossip select (menu, option)
                ep[0] = self.menu.get(ep[0], ep[0])
            tt, tp = r["target_type"], [r["target_param%d" % i] for i in range(1, 5)]
            if tt == 10:                                 # creature guid
                tp[0] = self.cguid.get(tp[0], tp[0])
            elif tt == 14:                               # gameobject guid
                tp[0] = self.gguid.get(tp[0], tp[0])
            out.append([e, st, r["id"], r["link"], ev, r["event_phase_mask"], r["event_chance"], r["event_flags"]]
                       + ep + [0, 0, a] + p + [tt] + tp
                       + [r["target_x"], r["target_y"], r["target_z"], r["target_o"], r["comment"] or ""])
        # Cataclysm's "cast spell on NPC" quest objectives: AzerothCore has no RequiredSpellCast, so the NPC gives
        # the credit itself when the spell hits it
        for q, spell, npc in self.cast_credit:
            s = self.spell_ok(spell)
            if not s or npc not in self.entries:
                continue
            n = 900 + sum(1 for r in out if r[0] == npc and r[2] >= 900)
            out.append([npc, 0, n, 0, 8, 0, 100, 0, s, 0, 0, 0, 0, 0, 33, npc, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0,
                        "quest %d: credit when hit by %d" % (q, s)])
            self.cast_credit_npcs.add(npc)
        keys = sorted({(r[0], r[1]) for r in out})
        delete = "\n".join("DELETE FROM `smart_scripts` WHERE `entryorguid` = %d AND `source_type` = %d;" % k for k in keys)
        cols = ("entryorguid source_type id link event_type event_phase_mask event_chance event_flags event_param1 "
                "event_param2 event_param3 event_param4 event_param5 event_param6 action_type action_param1 "
                "action_param2 action_param3 action_param4 action_param5 action_param6 target_type target_param1 "
                "target_param2 target_param3 target_param4 target_x target_y target_z target_o comment").split()
        self.write("65_smart_scripts", insert("smart_scripts", cols, out, delete))

    def conditions(self):
        out = []
        for r in self.t["conditions"]:
            st, g, e = r["SourceTypeOrReferenceId"], r["SourceGroup"], r["SourceEntry"]
            ct = r["ConditionTypeOrReference"]
            v = [r["ConditionValue1"], r["ConditionValue2"], r["ConditionValue3"]]
            if ct in CONDITION_DROP:
                dropped["conditions of types AzerothCore lacks"].append("%d/%d/%d type %d" % (st, g, e, ct))
                continue
            if st == CONDITION_PHASE_SOURCE[0]:
                st = CONDITION_PHASE_SOURCE[1]
            elif st in (14, 15):
                g = self.menu.get(g, g)
            elif st == 22 and e < 0:
                e = -(self.cguid if r["SourceId"] == 0 else self.gguid).get(-e, 0)
            elif st in (13, 17):
                s = self.spell_ok(e)
                if not s:
                    dropped["conditions on spells nothing has"].append(e)
                    continue
                e = s
            if ct in (CONDITION_AURA, CONDITION_SPELL):
                s = self.spell_ok(v[0])
                if not s:
                    dropped["conditions on spells nothing has"].append(v[0])
                    continue
                v[0] = s
            if ct == 2:                                  # item
                v[0] = self.item(v[0])
            if ct == 22 and v[0] in SOURCE_MAPS:          # map
                v[0] = 0
            if ct == 31 and v[0] == 3 and v[2]:           # creature guid
                v[2] = self.cguid.get(v[2], v[2])
            out.append([st, g, e, r["SourceId"], r["ElseGroup"], ct, r["ConditionTarget"]] + v
                       + [r["NegativeCondition"], r["ErrorType"], r["ErrorTextId"], r["ScriptName"] or "",
                          r["Comment"] or ""])
        keys = sorted({(r[0], r[1], r[2], r[3]) for r in out})
        delete = "\n".join("DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId` = %d AND `SourceGroup` = %d AND "
                           "`SourceEntry` = %d AND `SourceId` = %d;" % k for k in keys)
        self.write("70_conditions", insert(
            "conditions", "SourceTypeOrReferenceId SourceGroup SourceEntry SourceId ElseGroup ConditionTypeOrReference "
            "ConditionTarget ConditionValue1 ConditionValue2 ConditionValue3 NegativeCondition ErrorType ErrorTextId "
            "ScriptName Comment".split(), out, delete))

    # ---- phasing, area auras, spell positions --------------------------------------------------------------
    def phasing(self):
        zones = sorted({r["zoneId"] for r in self.t["phase_definitions"]})
        rows_ = [[r["zoneId"], r["entry"], r["phaseMask"], 0, 0, 0, r["flags"], r["comment"] or ""]
                 for r in self.t["phase_definitions"]]
        create = open(os.path.join(FIXES_DIR, "phase_definitions_table.sql"), encoding="utf8").read()
        self.write("90_phase_definitions", create + "\n" + insert(
            "phase_definitions", "zoneId entry phaseMask phaseId originmap terrainswapmap flags comment".split(), rows_,
            "DELETE FROM `phase_definitions` WHERE `zoneId` IN %s;" % in_list(zones),
            "Terrain swaps (Cataclysm's 638, 655, 656) left out for now: the phases play on Open Azeroth's Gilneas"))
        area = []
        for r in self.t["spell_area"]:
            s = self.spell_ok(r["spell"])
            if not s:
                dropped["spell_area rows of spells nothing has"].append(r["spell"])
                continue
            race = self.race_mask(r["racemask"])[0]
            area.append([s, r["area"], r["quest_start"], r["quest_end"], self.spell_ok(r["aura_spell"]) or 0, race,
                         r["gender"], r["autocast"], r["quest_start_status"], r["quest_end_status"]])
        self.write("91_spell_area", insert(
            "spell_area", "spell area quest_start quest_end aura_spell racemask gender autocast quest_start_status "
            "quest_end_status".split(), area, "\n".join(
                "DELETE FROM `spell_area` WHERE `spell` = %d AND `area` = %d;" % (r[0], r[1]) for r in area)))
        pos = [[r["id"], 0, 0 if r["target_map"] in SOURCE_MAPS else r["target_map"], r["target_position_x"],
                r["target_position_y"], r["target_position_z"], r["target_orientation"]]
               for r in self.t["spell_target_position"] if self.spell_ok(r["id"])]
        self.write("60_spell_target_position", insert(
            "spell_target_position", "ID EffectIndex MapID PositionX PositionY PositionZ Orientation".split(), pos,
            "DELETE FROM `spell_target_position` WHERE `ID` IN %s;" % in_list(r[0] for r in pos) if pos else None))
        names = [[r["spell_id"], r["ScriptName"]] for r in self.t["spell_script_names"] if r["ScriptName"] in SCRIPTS]
        self.write("61_spell_script_names", insert(
            "spell_script_names", ["spell_id", "ScriptName"], names,
            "DELETE FROM `spell_script_names` WHERE `ScriptName` IN (%s);" % ", ".join(
                sql_value(n) for n in sorted({r[1] for r in names})) if names else None))

    # ---- client rows: items, factions -------------------------------------------------------------------------
    def client_rows(self):
        ports = sorted(c for c, i in self.item_ids.items() if i)
        tmpl = [self.items.template(c, self.item_ids[c]) for c in ports]
        for t in tmpl:                                   # race masks to the config.sql words
            t["AllowableRace"] = self.race_mask(t["AllowableRace"])[0] or -1
        cols = [c for c in ITEM_TEMPLATE_COLUMNS]
        self.write("05_item_template", insert(
            "item_template", cols, [[t[c] for c in cols] for t in tmpl],
            "DELETE FROM `item_template` WHERE `entry` IN %s;" % in_list(ports) if ports else None,
            "Cataclysm items the zone uses that stock lacks, from the 4.0.6a client (cata_items.py)"))
        item_dbc = [[t["entry"], t["class"], t["subclass"], t["SoundOverrideSubclass"], t["Material"], t["displayid"],
                     t["InventoryType"], t["sheath"]] for t in tmpl]
        if item_dbc:
            self.files[os.path.join("dbc", "[%s]_item.sql" % TAG)] = insert(
                "item", "id class subclass sound_override_subclass material display_id inventory_type sheath".split(),
                item_dbc, "DELETE FROM `item` WHERE `id` IN %s;" % in_list(ports),
                "Item.dbc rows of the items above: the client draws worn and wielded items from these")
        if self.items.added:
            self.files[os.path.join("dbc", "[%s]_cata_itemdisplayinfo.sql" % TAG)] = display_sql(
                self.items, "-- Cataclysm item displays (4.0.6a) stock lacks. Generated by cata_gilneas_port.py.\n")
        ft = c406.Dbc(os.path.join(CATA_DBC, "FactionTemplate.dbc"))
        out = []
        for i in sorted(self.faction_templates):
            r = ft.get(i)
            if not r:
                dropped["faction templates nothing has"].append(i)
                continue
            f = lambda v: FACTION_VARS.get(v, v)
            row = dict(id=i, faction=f(r[1]), flags=r[2], faction_group=r[3], friend_group=r[4], enemy_group=r[5])
            row.update({"enemies_%d" % (n + 1): f(r[6 + n]) for n in range(4)})
            row.update({"friends_%d" % (n + 1): f(r[10 + n]) for n in range(4)})
            out.append(row)
        self.write_dbc("factiontemplate", out, "Cataclysm faction templates (4.0.6a) of the zone's NPCs; faction 1134 "
                       "(Gilneas) is F-024's @WorgenFaction")

    # ---- output -----------------------------------------------------------------------------------------------
    def write(self, name, sql):
        if sql:
            self.files[os.path.join(SQL_DIR, "zz_[AUTO,%s]_%s.sql" % (TAG, name))] = sql

    def run(self):
        self.trainers, self.faction_templates, self.bakes = [], set(), set()
        self.cast_credit, self.cast_credit_npcs = [], set()
        kits, visuals = self.collect_spells()
        self.creatures()
        self.spawns()
        self.gameobjects()
        self.gossip()
        self.quests_()
        self.loot()
        self.smart()
        self.conditions()
        self.phasing()
        self.client_rows()
        # creatures that got credit rows need SmartAI
        if self.cast_credit_npcs:
            self.write("66_cast_credit_ai", "UPDATE `creature_template` SET `AIName` = 'SmartAI' WHERE `entry` IN %s;\n"
                       % in_list(self.cast_credit_npcs))
        for name, sql in self.files.items():
            path = os.path.join(self.dest, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf8", newline="\n") as f:
                f.write("-- Generated by tools/races/cata_gilneas_port.py from Project Neltharion's world database: "
                        "change the script, not this file.\n\n" + sql)
        for sub, target in (("dbc", "dbc"), ("sql", SQL_DIR)):
            for path in sorted(glob.glob(os.path.join(FIXES_DIR, sub, "*.sql"))):
                os.makedirs(os.path.join(self.dest, target), exist_ok=True)
                shutil.copy2(path, os.path.join(self.dest, target, os.path.basename(path)))
        print("visual kits / visuals left as stock's: %s / %s" % (kits, visuals))
        print("ported: %d creatures, %d objects, %d quests, %d spells, %d items, %d item displays, %d bakes" % (
            len(self.entries), len(self.goentries), len(self.quests), len(self.spells),
            sum(1 for v in self.item_ids.values() if v), len(self.items.added), len(self.bakes)))
        for k, v in sorted(dropped.items()):
            v = sorted(set(map(str, v)))
            print("%s (%d): %s" % (k, len(v), ", ".join(v[:40]) + (" ..." if len(v) > 40 else "")))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    dest = sys.argv[2]
    for sub in ("dbc", "sql"):
        shutil.rmtree(os.path.join(dest, sub), ignore_errors=True)
    Port(sys.argv[1], dest).run()

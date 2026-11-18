"""Port the Wandering Isle's NPCs, objects and quests (Mists of Pandaria's Pandaren start, map 860) to F-134.

  python -I -X utf8 mop_wandering_isle_port.py TC_UPDATES F134_DIR [--data D:/wow-scratch/wi/db2]

TC_UPDATES is the TrinityCore MoP Classic port's sql/updates/world/mop_classic (References/MoP/trinitycore-mop-classic):
its generated Wandering Isle import (2026_10_18_02, from TrinityCore master's TDB 1210 with SkyFire 5.4.8 levels) and
the later audit/fix files are replayed in order (SOURCE_FILES, tc_sql_load.py), then rewritten to AzerothCore's
3.3.5a tables. --data holds wago.tools' 5.5.4.70449 ItemSparse.csv (English item names).

Rerun it after changing it: it replaces only its own files (sql/db-world/base/zz_[AUTO,F-134]_wi_*.sql and
dbc/[F-134]_wi_*.sql) and leaves mop_map_port.py's terrain files, readme.md and patches/ alone.

What it does:
- spawns stay on map 860 with new guids (CREATURE_GUID, GAMEOBJECT_GUID); waypoint paths (TrinityCore's waypoint_path
  + waypoint_path_node) become waypoint_data paths from PATH_BASE, everywhere they're used
- creature/object/quest ids keep MoP's, except where config.sql or another modpak already uses one (entries move to
  ENTRY_BASE and up, displays to DISPLAY_BASE and up)
- phases: TrinityCore phase ids become phasemask bits (169, the default phase, is 1); phase_area + its phase
  conditions become F-013's phase_definitions for zone 5736 with an area condition, so they need the
  WanderingIsleStartZone core support (which turns GoblinStartZone's on)
- race masks: Pandaren (MoP races 24-26) become F-020/F-021's masks; the start is moved by the core script, not
  playercreateinfo
- SmartAI: TrinityCore's waypoint actions/events become AzerothCore's (53 -> 232, 54/55/65/127/158 -> 235/234/236,
  40/58 -> 108/109) and the 137+ actions AzerothCore has under other ids are moved; actions/events it lacks are dropped
- creature displays, their extras (MoP's NPC bake names), models, object displays, faction templates, area triggers
  and items come from the 5.4.8 DBCs (References/MoP/MoP_data/dbc; same layouts as 4.0.6a for these, see
  mop_items.py for Item-sparse); Pandaren NPCs use F-129's Pandaren models. The model files and bakes are not here yet
- MoP spells the rows use (and the spells those trigger) come from the 5.4.8 DBCs (mop_spells.py); TrinityCore's
  server-side spells are built from its serverside_spell rows. Rows that need a spell nothing has are dropped and
  listed, and so are ScriptNames (AzerothCore has none of the island's scripts yet)
"""
import argparse, collections, glob, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tc_sql_load import load, rows  # noqa: E402
from cata_items import sql_value, ITEM_TEMPLATE_COLUMNS, DISPLAY_COLUMNS, display_sql  # noqa: E402
from mop_items import MopItems  # noqa: E402
from mop_loot import LootFill, killable, gold  # noqa: E402
from mop_spells import MopSpells  # noqa: E402
from cata_gilneas_port import insert, in_list, MODEL_COLUMNS, MODEL_FLOATS, modpak_spells  # noqa: E402
import cata406_dbc_port as c406  # noqa: E402

REFS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "References"))
MOP_DBC = os.path.join(REFS, "MoP", "MoP_data", "dbc")
STOCK_DBC = os.path.join(REFS, "original-client-dbc")
MODPAKS = os.path.normpath(os.path.join(HERE, "..", "..", "modpaks"))
TAG = "F-134"
SQL_DIR = os.path.join("sql", "db-world", "base")
SQL_PREFIX = "zz_[AUTO,%s]_wi_" % TAG
DBC_PREFIX = "[%s]_wi_" % TAG

SOURCE_FILES = ("2026_10_18_02", "2026_10_19_02", "2026_10_19_03", "2026_10_19_04", "2026_10_19_10",
                "2026_10_19_33", "2026_10_19_34", "2026_10_19_35", "2026_10_19_36")
MAP, ZONE = 860, 5736
CREATURE_GUID = 13400001
GAMEOBJECT_GUID = 13400001
PATH_BASE = 13400000          # waypoint_data ids: PATH_BASE + n
MENU_BASE = 1340000           # gossip_menu.MenuID
TEXT_BASE = 1340000           # npc_text.ID
ENTRY_BASE = 1340000          # creature entries whose MoP id another modpak uses
DISPLAY_BASE = 1340000        # creature displays whose MoP id another modpak uses
FALLBACK_DISPLAY = 646
GENERIC_TEXT = 68             # stock npc_text "Greetings, $n.": MoP's menu texts aren't in any source here
DEFAULT_PHASES = (0, 169)     # TrinityCore's default phase: everyone sees it

# MoP race -> config.sql race mask variable(s); Pandaren of either side count for the neutral (pre-choice) race
RACE_VARS = {1: ["Human"], 2: ["Orc"], 3: ["Dwarf"], 4: ["NightElf"], 5: ["Undead"], 6: ["Tauren"], 7: ["Gnome"],
             8: ["Troll"], 9: ["Goblin"], 10: ["BloodElf"], 11: ["Draenei"], 22: ["Worgen"],
             24: ["AlliancePandaren", "HordePandaren"], 25: ["AlliancePandaren"], 26: ["HordePandaren"]}
PANDAREN_BITS = (1 << 23) | (1 << 24) | (1 << 25)
EXTRA_RACES = {9: "@Goblin", 22: "@Worgen", 24: "@NeutralPandaren", 25: "@AlliancePandaren", 26: "@HordePandaren"}
CLASS_MASK = 0x5FF            # the 3.3.5a classes (1-9, 11); MoP's Monk (512) is left to F-100's class 10 rules

# SmartAI: TrinityCore master -> AzerothCore (enum names compared in both SmartScriptMgr.h)
SAI_EVENT_MAP = {40: 108, 58: 109, 46: 46}
SAI_EVENT_DROP = {39, 55, 56, 57} | set(range(83, 100))
SAI_ACTION_MAP = {46: 224, 53: 232, 54: 235, 55: 234, 65: 236, 127: 235, 158: 236, 141: 207, 151: 223, 157: 203,
                  159: 210, 60: 60}
SAI_ACTION_DROP = {16, 114, 128, 129, 130, 137, 138, 139, 140, 143, 144, 145, 146, 147, 148, 149, 150, 152, 153, 154,
                   155, 156} | set(range(160, 200))
SAI_SPELL_ACTIONS = {11, 85, 86, 134}
SAI_SPELL_EVENTS = {8, 31}
SAI_ENTRY_ACTIONS = {12: 0, 33: 0}                  # action -> param index holding a creature entry
SAI_ENTRY_TARGETS = {9: 0, 11: 0, 19: 0}            # target -> param index holding a creature entry
CONDITION_SOURCE_DROP = {28, 29, 30, 31, 32, 33, 34, 35}
CONDITION_TYPE_MAP = {51: 31, 52: 32}
CONDITION_TYPE_DROP = {50, 53, 54, 55, 56, 57, 58, 59, 60}
CONDITION_AURA, CONDITION_SPELL, CONDITION_AREA, CONDITION_PHASE = 1, 25, 23, 26
# GossipOptionNpc -> (OptionType, OptionNpcFlag, OptionIcon)
GOSSIP_NPC = {0: (1, 1, 0), 1: (3, 128, 1), 2: (4, 8192, 2), 3: (5, 16, 3), 4: (6, 16384, 4), 5: (8, 65536, 5),
              6: (9, 131072, 6), 9: (12, 1048576, 9), 12: (14, 4194304, 0)}

# Scripts the core's wandering_isle.cpp implements, under TrinityCore's names (F-134's core patch)
SCRIPTS = {
    "npc_tushui_huojin_trainee", "npc_huojin_trainee", "npc_tushui_leading_trainee", "npc_instructor_zhi",
    "go_edict_of_temperance", "npc_jaomin_ro", "npc_jaomin_ro_hawk", "npc_min_dimwind_summon", "npc_amberleaf_scamp",
    "npc_aysa_cloudsinger_summon", "npc_aysa_cloudsinger_cave_of_meditation", "npc_master_li_fei_summon",
    "spell_force_summoner_to_ride_vehicle", "spell_ride_drake", "spell_meditation_timer_bar", "spell_flame_spout",
    "at_min_dimwind_captured", "at_cave_of_meditation", "at_inside_of_cave_of_meditation",
    "at_singing_pools_transform_frog", "at_singing_pools_transform_skunk", "at_singing_pools_transform_crocodile",
    "at_singing_pools_transform_crane", "at_singing_pools_transform_turtle", "npc_li_fei", "spell_fire_crash",
    "npc_li_fei_combat", "spell_feet_of_fury", "spell_flying_shadow_kick", "npc_delivery_cart", "spell_huo_offering",
    "npc_shu_water_spouts", "npc_water_spout_bunny", "npc_shu_wake_wugou", "boss_zhao_ren",
    "spell_firework_launcher_click", "npc_shang_xi_hot_air_balloon", "npc_uplifting_draft", "npc_injured_sailor",
    "at_none_left_behind", "spell_healing_shen_zin_su_bar", "npc_spirit_of_master_shang_xi",
}
# Spells only the C++ casts, so no row names them
SCRIPT_SPELLS = {46598, 50630, 108627, 102938, 102939, 102940, 102941, 102942, 102717, 133381, 108149, 108150, 102515,
                 108936, 108943, 108958, 108957, 128700, 109080, 88811, 108955, 108935, 108938, 108583, 108959, 108582,
                 109837, 17683, 106231, 106206, 106205, 116421, 102447, 128598, 102445, 114710, 84034, 114686, 114684,
                 102499, 109090, 109095, 109105, 109107, 109109, 116810, 117063, 116695, 117057, 116696, 104017, 126006,
                 125992, 125990, 128808, 104855, 125970, 125964, 105895, 105010, 45472, 68576, 104490, 105520, 108898,
                 117783, 102522, 125961}
# TrinityCore ids the C++ uses that the port renumbers: written to wandering_isle_ids.h (--core)
SCRIPT_PATHS = (5720800, 5949600, 5774000, 5650300, 5650301, 5965200, 5485600)
SCRIPT_MENUS = (13050, 13140, 13726)
VEHICLE_BASE = 1340                   # Vehicle / VehicleSeat ids another modpak or stock uses
LOOT_REF_BASE = 1340000               # reference_loot_template entries of the generated loot pools (mop_loot.py)
LINEN_CLOTH = 2589
WI_SKINS = [(2318, 100, 1, 2), (2934, 50, 1, 1)]     # Light Leather; Ruined Leather Scraps

dropped = collections.defaultdict(list)


def dbc_ids(name, base=STOCK_DBC):
    d = open(os.path.join(base, name + ".dbc"), "rb").read()
    n, _, rs, _ = struct.unpack_from("<4I", d, 4)
    return {struct.unpack_from("<I", d, 20 + i * rs)[0] for i in range(n)}


def config_range(var):
    """Ids config.sql allocates from @var (SET @var = N; then @var := @var + 1 per id)."""
    text = open(os.path.join(MODPAKS, "config.sql"), encoding="utf-8").read()
    start = int(re.search(r"^SET @%s\s*=\s*(\d+)\s*;" % var, text, re.M).group(1))
    return set(range(start + 1, start + 1 + len(re.findall(r"@%s := @%s \+1" % (var, var), text))))


def taken(table, column):
    """Literal ids other modpaks insert into `table` (first VALUES column or `column` = N in SET blocks)."""
    out = set()
    for path in glob.glob(os.path.join(MODPAKS, "*", "**", "*.sql"), recursive=True):
        if os.sep + TAG in path:
            continue
        text = open(path, encoding="utf8", errors="replace").read()
        if "`%s`" % table not in text:
            continue
        for m in re.finditer(r"INSERT INTO `%s`\s*\(([^)]*)\)\s*VALUES(.*?);\s*$" % table, text, re.S | re.M):
            cols = [c.strip(" `") for c in m.group(1).split(",")]
            if cols and cols[0] == column:
                out |= {int(v) for v in re.findall(r"\(\s*(\d+)\s*,", m.group(2))}
        for m in re.finditer(r"INSERT INTO `%s` SET\s*`%s` = (\d+)" % (table, column), text):
            out.add(int(m.group(1)))
    return out


def modpak_display_ids(modpak):
    """creaturedisplayinfo ids a modpak's dbc/ SQL writes."""
    out = set()
    for p in glob.glob(os.path.join(modpak, "dbc", "*creaturedisplayinfo.sql")):
        out |= {int(v) for v in re.findall(r"INSERT INTO `creaturedisplayinfo` SET\s*`id` = (\d+)", open(p, encoding="utf8").read())}
    return out


def base_ids(table):
    """Entries AzerothCore's own world database has (its data/sql/base dump), for stock spawns on the island."""
    path = os.path.join(HERE, "..", "..", "..", "azerothcore-wotlk-256-bit", "data", "sql", "base", "db_world",
                        table + ".sql")
    return {int(v) for v in re.findall(r"^\((\d+),", open(path, encoding="utf8", errors="replace").read(), re.M)}


def emote_names(stock):
    """MoP emote -> stock emote of the same animation (MoP's monk training emotes are the unarmed ones)."""
    mop, base = c406.Dbc(os.path.join(MOP_DBC, "Emotes.dbc")), c406.Dbc(os.path.join(STOCK_DBC, "Emotes.dbc"))
    by_name = {base.s(r[1]): r[0] for r in base.records}
    out = {}
    for r in mop.records:
        if r[0] in stock:
            continue
        name = mop.s(r[1]).replace("MONKOFFENSE_", "").replace("PALMSTRIKE", "ATTACKUNARMED").replace("SPECIALUNARMED", "ATTACKUNARMED")
        if name in by_name:
            out[r[0]] = by_name[name]
    return out


def taken_spells():
    """Spell ids other modpaks write in their dbc/ SQL."""
    out = set()
    for path in glob.glob(os.path.join(MODPAKS, "*", "dbc", "*.sql")):
        if os.sep + TAG in path:
            continue
        text = open(path, encoding="utf8", errors="replace").read()
        out |= {int(m) for m in re.findall(r"INSERT INTO `spell` SET\s*`id` = (\d+)", text)}
    return out


def taken_icons():
    """SpellIcon ids config.sql or other modpaks use."""
    text = open(os.path.join(MODPAKS, "config.sql"), encoding="utf-8").read()
    out = {int(v) for v in re.findall(r"^SET @Icon\w*\s*=\s*(\d+)\s*;", text, re.M)}
    return out | taken("spellicon", "id")


class MopSounds(c406.Port):
    """cata406_dbc_port's NPCSounds port on the 5.4.8 tables: their SoundEntries name files by FileDataID (fields
    3-12) and have no base directory, so the files come from the community listfile and the base directory is the
    first file's folder. Volume, flags, distances and EAX are 4.0.6a's 24-28 moved one down."""
    LISTFILE = "D:/wow-scratch/listfile/community-listfile.csv"

    def __init__(self):
        args = type("A", (), dict(effect_name=[], no_sound=[], sound_map=[], sound_ext=None, skip_kit=[],
                                  skip_visual=[]))()
        super().__init__(MOP_DBC, STOCK_DBC, args)
        self.paths = None

    def sound(self, sid):
        if sid <= 0:
            return sid
        if not hasattr(self, "cS"):
            self.cS, self.oS = self.c("SoundEntries"), self.o("SoundEntries")
        if self.oS.get(sid) or sid in self.out.get("soundentries", {}):
            return sid
        r = self.cS.get(sid)
        if not r:
            return 0
        if self.paths is None:
            want = set()
            for x in self.cS.records:
                want.update(x[3:13])
            self.paths = {}
            for line in open(self.LISTFILE, encoding="utf8", errors="replace"):
                f, _, p = line.strip().partition(";")
                if f.isdigit() and int(f) in want:
                    self.paths[int(f)] = p
        files = [(self.paths.get(f), q) for f, q in zip(r[3:13], r[13:23]) if f and self.paths.get(f)]
        if not files:
            return 0
        base = files[0][0].rsplit("/", 1)[0]
        c = {"id": sid, "sound_type": r[1], "name": self.cS.s(r[2])}
        for i, (path, freq) in enumerate(f for f in files if f[0].rsplit("/", 1)[0] == base):
            c["file_%d" % (i + 1)] = path.rsplit("/", 1)[1]
            c["frequency_%d" % (i + 1)] = freq
        c.update(base_dir=base.replace("/", "\\"), volume=c406.f32(r[23]), flags=r[24], min_distance=c406.f32(r[25]),
                 distance_cutoff=c406.f32(r[26]), eax_def=r[27], advanced_id=0)
        self.add("soundentries", sid, c, "%d %s" % (sid, c["name"]), self.oS)
        return sid


def num(v, default=0):
    if v is None:
        return default
    if isinstance(v, float) and v >= 2 ** 63:   # sqlite keeps 2^64-1 ("every race") as a float
        return -1
    return v


# AC VisibilityDistanceType for creatures the default 90 yards cuts short: Shen-zin Su, the turtle the island is
# built on, is one spawn in the island's middle; its limbs and head showed only near that point
VISIBILITY = {57769: 5}   # Infinite (533 yards)
# Creatures that float in MoP over ground the server can't see (no vmaps for the island's WMOs yet): without flight the
# core drops them to the terrain below, Shang Xi's Hot Air Balloon off its platform into Morning Breeze Lake
FLYING = {55650}
# Gameobjects the client should always draw: Shen-zin Su's flippers, spawned out at sea, showed only while a player
# was near their origin (the core loads a gameobject's cell only near players). They are placed in the island's
# tiles as doodads instead (tools/models/adt_add_doodads.py, uniqueIds 99000001-99000005), so no spawns here.
MAP_DOODADS = {213439, 213532}



# MoP pet families 3.3.5a has no CreatureFamily row for (a pet of one is broken): the nearest stock family
FAMILY_MAP = {50: 1, 52: 1,              # fox, dog -> wolf
              51: 9,                     # monkey -> gorilla
              53: 20,                    # beetle -> scorpid
              55: 3, 126: 3,             # shale spider, water strider -> spider
              68: 6, 130: 6,             # hydra, basilisk -> crocolisk
              125: 26,                   # crane -> bird of prey
              127: 5, 129: 5,            # rodent, goat -> boar
              128: 2,                    # quilen -> cat
              138: 43}                   # direhorn -> rhino

# Quest givers neither the TC import nor its TDB has: the core's start (wandering_isle_start.cpp) gives every class
# 29404 Much to Learn and the generic 29405 The Lesson of the Iron Staff follows (retail used the class versions,
# 30039-30045 and 30027/30033-30038), so Master Shang Xi has to end 29404 and give and end 29405
SHANG_XI = 53566
EXTRA_RELATIONS = {"creature_queststarter": [(SHANG_XI, 29405)],
                   "creature_questender": [(SHANG_XI, 29404), (SHANG_XI, 29405)]}


def pet_family(family, stock):
    """The 3.3.5a family for a MoP one: kept, mapped (FAMILY_MAP) or 0."""
    family = FAMILY_MAP.get(family, family)
    return family if family in stock else 0


class Port:
    def __init__(self, updates, dest, data):
        self.dest, self.data = dest, data
        self.spell_map = {}
        self.vehicles = {}
        self.files = {}
        self.db = load([os.path.join(updates, f + "_world.sql") for f in SOURCE_FILES])
        self.t = lambda table, where="1": rows(self.db, table, where)
        self.stock_spells = dbc_ids("Spell") | modpak_spells()
        self.stock_emotes = dbc_ids("Emotes")
        self.stock_sounds = dbc_ids("SoundEntries")
        self.stock_cdisp = dbc_ids("CreatureDisplayInfo")
        self.stock_extra = dbc_ids("CreatureDisplayInfoExtra")
        self.stock_models = dbc_ids("CreatureModelData")
        self.stock_gdisp = dbc_ids("GameObjectDisplayInfo")
        self.stock_ft = dbc_ids("FactionTemplate")
        self.stock_factions = dbc_ids("Faction") | {1352, 1353}      # + F-020/F-021's Huojin and Tushui
        self.stock_languages = dbc_ids("Languages")
        self.stock_movies = dbc_ids("Movie")
        self.stock_vehicles = dbc_ids("Vehicle")
        self.stock_families = dbc_ids("CreatureFamily")
        self.stock_soundData = dbc_ids("CreatureSoundData")
        self.stock_npcsounds = dbc_ids("NPCSounds")
        self.stock_at = dbc_ids("AreaTrigger")
        self.stock_creatures = base_ids("creature_template")
        self.stock_gameobjects = base_ids("gameobject_template")
        self.emote_map = emote_names(self.stock_emotes)
        self.items = MopItems(MOP_DBC, STOCK_DBC, os.path.join(data, "ItemSparse.csv"), config_range("NextItemDisplayID"))
        self.taken_entries = config_range("NextCreatureID") | taken("creature_template", "entry")
        # F-133 (Pandaria, mop_pandaria_port.py) writes the same 5.4.8 rows for the displays both use
        self.taken_displays = (config_range("NextDisplayID") | taken("creaturedisplayinfo", "id")) - \
            modpak_display_ids(os.path.join(MODPAKS, "F-133_mop-pandaria"))
        self.taken_quests = taken("quest_template", "ID")
        self.taken_goentries = taken("gameobject_template", "entry")

        self.ct = {r["entry"]: r for r in self.t("creature_template")}
        self.diff = {r["Entry"]: r for r in self.t("creature_template_difficulty", "DifficultyID = 0")}
        self.got = {r["entry"]: r for r in self.t("gameobject_template")}
        self.quests = {r["ID"]: r for r in self.t("quest_template")}
        clash = sorted(set(self.quests) & self.taken_quests)
        if clash:
            sys.exit("quest ids another modpak uses: %s" % clash)
        clash = sorted(set(self.got) & self.taken_goentries)
        if clash:
            sys.exit("gameobject entries another modpak uses: %s" % clash)
        self.entry_map = {}
        for e in sorted(self.ct):
            if e in self.taken_entries:
                self.entry_map[e] = ENTRY_BASE + len(self.entry_map)
        self.cguid = {r["guid"]: CREATURE_GUID + i for i, r in enumerate(sorted(self.t("creature"), key=lambda r: r["guid"]))}
        self.gguid = {r["guid"]: GAMEOBJECT_GUID + i for i, r in enumerate(sorted(self.t("gameobject"), key=lambda r: r["guid"]))}
        self.paths = {p["PathId"]: PATH_BASE + i + 1 for i, p in enumerate(sorted(self.t("waypoint_path"), key=lambda p: p["PathId"]))}
        menus = sorted({r["MenuID"] for r in self.t("gossip_menu")} | {r["MenuID"] for r in self.t("gossip_menu_option")}
                       | {r["MenuID"] for r in self.t("creature_template_gossip")})
        self.menu = {m: MENU_BASE + i for i, m in enumerate(menus)}
        phases = sorted({r["PhaseId"] for t in ("creature", "gameobject") for r in self.t(t)}
                        | {r["PhaseId"] for r in self.t("phase_area")} - set(DEFAULT_PHASES))
        self.phase_bit = {p: 1 << (i + 1) for i, p in enumerate(p for p in phases if p not in DEFAULT_PHASES)}
        if len(self.phase_bit) > 30:
            sys.exit("too many phases for a phasemask: %d" % len(self.phase_bit))
        self.item_ids = {}
        self.faction_templates = set()
        self.displays = {}                                  # MoP display -> display here
        self.bakes, self.models, self.belt_displays = set(), set(), set()
        self.triggers = set()

    # ---- ids --------------------------------------------------------------------------------------------------
    def entry(self, e):
        return self.entry_map.get(e, e) if e in self.ct else e

    def spell_ok(self, sid):
        """The id to use for a MoP spell id (sign kept), None when nothing has it."""
        if not sid:
            return sid
        a = abs(sid)
        out = a if a in self.stock_spells else self.spell_map.get(a)
        return None if out is None else (-out if sid < 0 else out)

    # ---- spells -----------------------------------------------------------------------------------------------
    def wanted_spells(self):
        want = set(SCRIPT_SPELLS)
        for r in self.t("smart_scripts"):
            if r["action_type"] in SAI_SPELL_ACTIONS:
                want.add(num(r["action_param1"]))
            if r["event_type"] in SAI_SPELL_EVENTS:
                want.add(num(r["event_param1"]))
        for t in ("creature_addon", "creature_template_addon"):
            for r in self.t(t):
                want |= {int(a) for a in (r["auras"] or "").split()}
        want |= {r["spell_id"] for r in self.t("npc_spellclick_spells")}
        for r in self.t("spell_area"):
            want |= {r["spell"], r["aura_spell"]}
        for r in self.quests.values():
            want |= {r["RewardDisplaySpell1"], r["RewardSpell"]}
        want |= {num(r["SourceSpellID"]) for r in self.t("quest_template_addon")}
        for r in self.t("conditions"):
            if r["ConditionTypeOrReference"] in (CONDITION_AURA, CONDITION_SPELL):
                want.add(num(r["ConditionValue1"]))
            if r["SourceTypeOrReferenceId"] in (13, 17, 18):
                want.add(r["SourceEntry"])
        # spells of the items the island hands out
        items = {r["Item"] for t in ("creature_loot_template", "gameobject_loot_template") for r in self.t(t)}
        items |= {r["ItemId"] for r in self.t("gameobject_questitem")} | {r["item"] for r in self.t("npc_vendor")}
        for q in self.quests.values():
            items |= {q[k] for k in q if k.startswith(("RewardItem", "RewardChoiceItemID", "ItemDrop")) or k == "StartItem"}
        items |= {r["ObjectID"] for r in self.t("quest_objectives", "Type = 1")}
        for i in items:
            if i and i not in self.items.stock_items and self.items.has(i):
                sp = self.items.sparse[i]
                want |= {sp[self.items.sp["spell"] + n] for n in range(5)}
        return {abs(x) for x in want if x}

    def server_spells(self):
        """TrinityCore's server-side spells (serverside_spell + serverside_spell_effect) as Spell.dbc rows."""
        effects = collections.defaultdict(list)
        for e in self.t("serverside_spell_effect"):
            effects[int(e["SpellID"])].append(e)
        attrs = ("attributes", "attributes_ex_1", "attributes_ex_2", "attributes_ex_3", "attributes_ex_4",
                 "attributes_ex_5", "attributes_ex_6", "attributes_ex_7")
        out = {}
        for r in self.t("serverside_spell"):
            sid = int(r["Id"])
            if int(r["DifficultyID"]):
                continue
            c = {"id": sid, "spell_name_enus": r["SpellName"], "cast_time_index": int(r["CastingTimeIndex"]) or 1,
                 "duration_index": int(r["DurationIndex"]), "range_index": int(r["RangeIndex"]) or 1,
                 "spell_icon_id": 1, "school_mask": int(r["SchoolMask"]), "proc_chance": 101,
                 "equipped_item_class": -1}
            for col, k in zip(attrs, ("Attributes", "AttributesEx", "AttributesEx2", "AttributesEx3", "AttributesEx4",
                                      "AttributesEx5", "AttributesEx6", "AttributesEx7")):
                c[col] = int(r[k]) & 0xFFFFFFFF
            for e in effects[sid]:
                n = int(e["EffectIndex"]) + 1
                # 3.3.5a's core asserts on targets it lacks (TrinityCore's tap list, 123); the scripts credit by hand
                if max(int(e["ImplicitTarget1"]), int(e["ImplicitTarget2"])) > c406.MAX_TARGET:
                    dropped["server-side spell effects with targets 3.3.5a lacks"].append(
                        "%d effect %d (targets %s/%s)" % (sid, n, e["ImplicitTarget1"], e["ImplicitTarget2"]))
                    continue
                misc = int(e["EffectMiscValue1"])
                if int(e["Effect"]) in (90, 134, 28):
                    misc = self.entry(misc)
                c.update({"effect_%d" % n: int(e["Effect"]), "effect_apply_aura_name_%d" % n: int(e["EffectAura"]),
                          "effect_base_points_%d" % n: int(float(e["EffectBasePoints"])),
                          "effect_misc_value_a_%d" % n: misc, "effect_misc_value_b_%d" % n: int(e["EffectMiscValue2"]),
                          "effect_implicit_target_a_%d" % n: int(e["ImplicitTarget1"]),
                          "effect_implicit_target_b_%d" % n: int(e["ImplicitTarget2"]),
                          "effect_radius_index_%d" % n: int(e["EffectRadiusIndex1"]),
                          "effect_trigger_spell_%d" % n: int(e["EffectTriggerSpell"]),
                          "effect_multiple_value_%d" % n: 1, "effect_damage_multiplier_%d" % n: 1})
            out[sid] = c
        return out

    def port_spells(self):
        self.spell_map = {}
        server = self.server_spells()
        taken = taken_spells() - self.stock_spells
        self.spells = MopSpells(MOP_DBC, STOCK_DBC, self.data, self.stock_spells | set(server), taken,
                                self.phase_bit, self.entry, self.vehicle)
        self.spells.taken_icons = taken_icons()
        self.spell_map = self.spells.port(sorted(self.wanted_spells()))
        for sid, row in server.items():
            self.spells.rows[sid] = row
            self.spell_map[sid] = sid
        for k, v in self.spells.dropped.items():
            dropped[k].extend(v)
        moved = sorted(s for s in SCRIPT_SPELLS if self.spell_map.get(s, s) != s)
        if moved:
            sys.exit("spells the C++ uses moved to other ids (give the header a spell map): %s" % moved)
        missing = sorted({e for e in self.spells.summons if e and e not in self.ct and e not in self.stock_creatures})
        if missing:
            dropped["creatures the ported spells summon that nothing defines"].extend(missing)
        comment = ("MoP spells the Wandering Isle uses, from the 5.4.8 client (tools/races/mop_spells.py), English text "
                   "from wago.tools; TrinityCore's server-side spells from its serverside_spell rows. Generated by "
                   "mop_wandering_isle_port.py.")
        for name, sql in self.spells.files(DBC_PREFIX, comment).items():
            self.files[os.path.join("dbc", name)] = sql

    def item(self, mop):
        if not mop or mop in self.items.stock_items:
            return mop
        if mop not in self.item_ids:
            self.item_ids[mop] = mop if self.items.has(mop) else 0
            if not self.item_ids[mop]:
                dropped["items the 5.4.8 client lacks"].append(mop)
        return self.item_ids[mop]

    def race_mask(self, mask):
        """(word 1, word 2) expressions for a MoP race mask; Pandaren-only masks are the two Pandaren races."""
        mask = num(mask)
        if mask in (0, -1) or mask >= (1 << 32) - 1 and not mask & ~((1 << 64) - 1) and mask & 0x7FF == 0x7FF:
            return 0, 0
        races = [b + 1 for b in range(64) if mask & (1 << b)]
        names = sorted({n for r in races for n in RACE_VARS.get(r, [])})
        if not names:
            return 0, 0
        return " | ".join("@%sMask" % n for n in names), " | ".join("@%sMask_2" % n for n in names)

    def phasemask(self, phase, group=0):
        if group:
            dropped["phase groups (spawn kept in the default phase)"].append(group)
        if phase in DEFAULT_PHASES:
            return 1
        return self.phase_bit[phase]

    def faction(self, ft):
        if not ft:
            return 35
        if ft not in self.stock_ft:
            self.faction_templates.add(ft)
        return ft

    def emote(self, e, where):
        e = self.emote_map.get(e, e)
        if e and e not in self.stock_emotes:
            dropped["emotes 3.3.5a lacks"].append("%s %s" % (e, where))
            return 0
        return e or 0

    def auras(self, text, where):
        keep = []
        for a in (text or "").split():
            sp = self.spell_ok(int(a))
            if sp:
                keep.append(str(sp))
            else:
                dropped["auras of spells nothing has"].append("%s on %s" % (a, where))
        return " ".join(keep) or None

    def path(self, p):
        return self.paths.get(p, 0) if p else 0

    # ---- creatures --------------------------------------------------------------------------------------------
    def creatures(self):
        ai = {r["entryorguid"] for r in self.t("smart_scripts", "source_type = 0 AND entryorguid > 0")}
        gossip = {}
        for r in self.t("creature_template_gossip"):
            gossip.setdefault(r["CreatureID"], self.menu[r["MenuID"]])
        tmpl, movement = [], []
        addon_by_entry = {r["entry"]: r for r in self.t("creature_template_addon")}
        for e, r in sorted(self.ct.items()):
            d = self.diff.get(e, {})
            script = r["ScriptName"] or ""
            if script and script not in SCRIPTS:
                dropped["script names nothing implements yet"].append("%d %s" % (e, script))
                script = ""
            aname = r["AIName"] or ""
            if aname == "SmartAI" and e not in ai:
                aname = ""
            family = pet_family(r["family"], self.stock_families)
            vehicle = self.vehicle(r["VehicleId"])
            if r["VehicleId"] and not vehicle:
                dropped["vehicle ids the 5.4.8 client lacks"].append("%d %d" % (e, r["VehicleId"]))
            tmpl.append([self.entry(e), 0, 0, 0, self.entry(r["KillCredit1"]), self.entry(r["KillCredit2"]), r["name"],
                         r["subname"] or None, r["IconName"] or None, gossip.get(e, 0), num(d.get("MinLevel"), 1),
                         num(d.get("MaxLevel"), 1), 0, self.faction(r["faction"]), num(r["npcflag"]) & 0x7FFFFFF,
                         r["speed_walk"], r["speed_run"], 1, 1, 18, r["Classification"], r["dmgschool"],
                         num(d.get("DamageModifier"), 1), r["BaseAttackTime"] or 2000, r["RangeAttackTime"] or 2000,
                         r["BaseVariance"] or 1, r["RangeVariance"] or 1, r["unit_class"] or 1, num(r["unit_flags"]),
                         num(r["unit_flags2"]) & 0x3FFFF, 0, family, r["type"], num(d.get("TypeFlags")),
                         num(d.get("LootID")) or (self.entry(e) if self.gen_loot.get(e) else 0),
                         num(d.get("PickPocketLootID")), self.entry(e) if self.gen_skin.get(e) else 0, 0, vehicle]
                        + list(self.gen_gold.get(e, (num(d.get("GoldMin")), num(d.get("GoldMax"))))) +
                        [aname, r["MovementType"], 1,
                         num(d.get("HealthModifier"), 1), num(d.get("ManaModifier"), 1), num(d.get("ArmorModifier"), 1),
                         r["ExperienceModifier"] or 1, r["RacialLeader"], 0, r["RegenHealth"], 0, 0, script, 0])
            a = addon_by_entry.get(e)
            movement.append([self.entry(e), 1, 1, 1 if (a and a["AnimTier"] == 3) or e in FLYING else 0])
        cols = ("entry difficulty_entry_1 difficulty_entry_2 difficulty_entry_3 KillCredit1 KillCredit2 name subname "
                "IconName gossip_menu_id minlevel maxlevel exp faction npcflag speed_walk speed_run speed_swim "
                "speed_flight detection_range rank dmgschool DamageModifier BaseAttackTime RangeAttackTime BaseVariance "
                "RangeVariance unit_class unit_flags unit_flags2 dynamicflags family type type_flags lootid "
                "pickpocketloot skinloot PetSpellDataId VehicleId mingold maxgold AIName MovementType HoverHeight "
                "HealthModifier ManaModifier ArmorModifier ExperienceModifier RacialLeader movementId RegenHealth "
                "CreatureImmunitiesId flags_extra ScriptName VerifiedBuild").split()
        ents = in_list(self.entry(e) for e in self.ct)
        self.write("10_creature_template", insert("creature_template", cols, tmpl,
                                                  "DELETE FROM `creature_template` WHERE `entry` IN %s;" % ents))
        self.write("12_creature_template_movement", insert(
            "creature_template_movement", "CreatureId Ground Swim Flight".split(), movement,
            "DELETE FROM `creature_template_movement` WHERE `CreatureId` IN %s;" % ents))
        # models and displays
        models = [r for r in self.t("creature_template_model") if r["CreatureID"] in self.ct]
        self.port_displays({r["CreatureDisplayID"] for r in models})
        out = []
        for r in sorted(models, key=lambda r: (r["CreatureID"], r["Idx"])):
            d = self.displays.get(r["CreatureDisplayID"])
            if d is None:
                dropped["creature displays nothing has (fell back to %d)" % FALLBACK_DISPLAY].append(r["CreatureDisplayID"])
                d = FALLBACK_DISPLAY
            out.append([self.entry(r["CreatureID"]), r["Idx"], d, r["DisplayScale"] or 1, r["Probability"] or 1, 0])
        self.write("11_creature_template_model", insert(
            "creature_template_model", "CreatureID Idx CreatureDisplayID DisplayScale Probability VerifiedBuild".split(),
            out, "DELETE FROM `creature_template_model` WHERE `CreatureID` IN %s;" % ents))
        info = []
        for r in self.t("creature_model_info"):
            d = self.displays.get(r["DisplayID"])
            if d and d not in self.stock_cdisp:
                info.append([d, r["BoundingRadius"], r["CombatReach"], self.gender.get(r["DisplayID"], 2), 0, 0])
        # the core won't spawn a creature whose display has no creature_model_info row; the TC import lacks some
        have = {row[0] for row in info}
        mop_of = {v: k for k, v in self.displays.items()}
        for d in sorted({row[2] for row in out} - have - self.stock_cdisp):
            info.append([d, 0.5, 1.5, self.gender.get(mop_of.get(d, d), 2), 0, 0])
            dropped["creature displays given a default creature_model_info row"].append(d)
        self.write("13_creature_model_info", insert(
            "creature_model_info", "DisplayID BoundingRadius CombatReach Gender DisplayID_Other_Gender VerifiedBuild".split(),
            info, "DELETE FROM `creature_model_info` WHERE `DisplayID` IN %s;" % in_list(r[0] for r in info)
            if info else None))
        equip = [[self.entry(r["CreatureID"]), r["ID"]] + [self.item(r["ItemID%d" % n]) for n in (1, 2, 3)] + [0]
                 for r in self.t("creature_equip_template") if r["CreatureID"] in self.ct]
        self.write("14_creature_equip_template", insert(
            "creature_equip_template", "CreatureID ID ItemID1 ItemID2 ItemID3 VerifiedBuild".split(), equip,
            "DELETE FROM `creature_equip_template` WHERE `CreatureID` IN %s;" % ents))
        addon = [[self.entry(e), self.path(a["PathId"]), a["mount"] if a["mount"] in self.stock_cdisp else 0,
                  self.bytes1(a), self.bytes2(a), self.emote(a["emote"], "template %d" % e),
                  VISIBILITY.get(e, a.get("visibilityDistanceType") or 0),
                  self.auras(a["auras"], "creature_template_addon %d" % e)]
                 for e, a in sorted(addon_by_entry.items()) if e in self.ct]
        self.write("15_creature_template_addon", insert(
            "creature_template_addon", "entry path_id mount bytes1 bytes2 emote visibilityDistanceType auras".split(),
            addon, "DELETE FROM `creature_template_addon` WHERE `entry` IN %s;" % ents))
        text = []
        for r in self.t("creature_text"):
            if r["CreatureID"] not in self.ct:
                continue
            lang = r["Language"] if r["Language"] in self.stock_languages else 0
            text.append([self.entry(r["CreatureID"]), r["GroupID"], r["ID"], r["Text"], r["Type"], lang, r["Probability"],
                         self.emote(r["Emote"], "text %d" % r["CreatureID"]), r["Duration"],
                         r["Sound"] if r["Sound"] in self.stock_sounds else 0, 0, r["TextRange"] or 0, r["comment"] or ""])
        self.write("16_creature_text", insert(
            "creature_text", "CreatureID GroupID ID Text Type Language Probability Emote Duration Sound BroadcastTextId "
            "TextRange comment".split(), text, "DELETE FROM `creature_text` WHERE `CreatureID` IN %s;" % ents))

    def vehicle(self, mid):
        """Vehicle id to use for a MoP one: stock's, or the 5.4.8 row and its seats in 3.3.5a's layout (Vehicle has one
        more field at 2; VehicleSeat drops ui_skin, 3.3.5a's 44, and adds fields at the end)."""
        if not mid or mid in self.stock_vehicles:
            return mid
        if mid in self.vehicles:
            return self.vehicles[mid]
        if not hasattr(self, "vdbc"):
            self.vdbc, self.sdbc = c406.Dbc(os.path.join(MOP_DBC, "Vehicle.dbc")), c406.Dbc(os.path.join(MOP_DBC, "VehicleSeat.dbc"))
            self.stock_seats = dbc_ids("VehicleSeat")
            self.taken_vehicles = taken("vehicle", "id")
            self.taken_seats = taken("vehicleseat", "id")
            self.out_vehicles, self.out_seats, self.seat_map = [], [], {}
        r = self.vdbc.get(mid)
        if not r:
            self.vehicles[mid] = 0
            return 0
        new = mid if mid not in self.taken_vehicles else VEHICLE_BASE + len(self.out_vehicles)
        row = list(r[:2]) + list(r[3:])
        seats = []
        for sid in row[6:14]:
            if sid and sid not in self.stock_seats:
                if sid not in self.seat_map:
                    s_ = self.sdbc.get(sid)
                    if not s_:
                        self.seat_map[sid] = 0
                    else:
                        snew = sid if sid not in self.taken_seats else VEHICLE_BASE + len(self.out_seats)
                        self.seat_map[sid] = snew
                        self.out_seats.append([snew] + list(s_[1:44]) + [0] + list(s_[44:57]))
                sid = self.seat_map[sid]
            seats.append(sid)
        row[0], row[6:14] = new, seats
        self.out_vehicles.append(row)
        self.vehicles[mid] = new
        return new

    def npc_sound(self, nid):
        """NPCSounds id to use for a display's greetings: stock's, or MoP's, ported by write_npc_sounds."""
        if nid and nid not in self.stock_npcsounds:
            if not hasattr(self, "npc_sound_ids"):
                self.npc_sound_ids = set()
            self.npc_sound_ids.add(nid)
        return nid

    def write_npc_sounds(self):
        """The displays' greeting / farewell / pissed voices: 5.4.8's NPCSounds rows and their SoundEntries, as F-013
        ports Kezan's from 4.0.6a. The files go to WHE-common with tools/races/zep_goblin_sounds.py --sql."""
        ids = sorted(getattr(self, "npc_sound_ids", ()))
        if not ids:
            return
        port = MopSounds()
        have = c406.Dbc(os.path.join(MOP_DBC, "NPCSounds.dbc"))
        port.npc_sounds([i for i in ids if have.get(i)])
        for table, rows_ in sorted(port.out.items()):
            text = ["-- MoP NPC voices (5.4.8 %s, files named through the community listfile). Generated by "
                    "tools/races/mop_wandering_isle_port.py.\n" % table]
            text += [c406.block(table, k, c, comment) for k, (c, comment) in sorted(rows_.items())]
            self.files[os.path.join("dbc", DBC_PREFIX + "npc_" + table + ".sql")] = "\n".join(text)

    def write_vehicles(self):
        if not getattr(self, "out_vehicles", None):
            return
        import json

        def meta(table):
            """(column, type) in file order, arrays expanded as DBCTool names them (seat_id_1..8)."""
            fields = json.load(open(os.path.join(HERE, "..", "..", "..", "DBCTool-256-bit", "meta", table + ".meta.json"),
                                    encoding="utf8"))["fields"]
            out = []
            for f in fields:
                n = f.get("count", 1)
                out += [((f["name"] + "_%d" % (i + 1)) if n > 1 else f["name"], f["type"]) for i in range(n)]
            return out

        def rows_(table, data, dbc):
            cols = meta(table)
            assert all(len(r) == len(cols) for r in data), (table, len(cols), {len(r) for r in data})
            # the DBC reader gives signed ints: unsigned columns (Vehicle flags with bit 31) need their unsigned value
            conv = {"float": c406.f32, "string": dbc.s, "uint32": c406.u32}
            return [{c: conv.get(t, lambda v: v)(v) for (c, t), v in zip(cols, r)} for r in data]

        self.write_dbc("vehicle", rows_("vehicle", self.out_vehicles, self.vdbc),
                       "MoP vehicles (5.4.8) of the island's carts, poles, balloon, draft and sailor rescue")
        self.write_dbc("vehicleseat", rows_("vehicleseat", self.out_seats, self.sdbc), "Their seats (5.4.8)")

    @staticmethod
    def bytes1(a):
        return (a["StandState"] or 0) | ((a["VisFlags"] or 0) << 16) | ((a["AnimTier"] or 0) << 24)

    @staticmethod
    def bytes2(a):
        return (a["SheathState"] or 0) | ((a["PvPFlags"] or 0) << 8)

    # ---- displays ---------------------------------------------------------------------------------------------
    def port_displays(self, ids):
        """MoP creature displays stock lacks (5.4.8 rows, 4.0.6a's layout for the first 17 fields); sets
        self.displays (MoP id -> id here) and self.gender."""
        cd = c406.Dbc(os.path.join(MOP_DBC, "CreatureDisplayInfo.dbc"))
        ce = c406.Dbc(os.path.join(MOP_DBC, "CreatureDisplayInfoExtra.dbc"))
        cm = c406.Dbc(os.path.join(MOP_DBC, "CreatureModelData.dbc"))
        pandaren = {}
        for r in cm.records:
            p = cm.s(r[2]).lower()
            if p.startswith("character\\pandaren\\"):
                pandaren[r[0]] = "@PandarenFemaleModel" if "female" in p else "@PandarenMaleModel"
        out_d, out_e, self.gender, moved = [], [], {}, 0
        for d in sorted(ids):
            if d in self.stock_cdisp:
                self.displays[d] = d
                continue
            r = cd.get(d)
            if not r:
                continue
            model = pandaren.get(r[1], r[1])
            if model == r[1] and r[1] not in self.stock_models:
                self.models.add(r[1])
            extra = r[3]
            if extra and extra not in self.stock_extra:
                x = ce.get(extra)
                if not x:
                    dropped["display extras the 5.4.8 client lacks"].append(extra)
                    continue
                self.gender[d] = x[2]
                out_e.append(dict(id=extra, race=EXTRA_RACES.get(x[1], x[1]), gender=x[2], skin_color=x[3],
                                  face_type=x[4], hair_style=x[5], hair_color=x[6], facial_hair=x[7],
                                  **{k: self.items.display_id(v) if v > 0 else 0 for k, v in zip(
                                      ("helm_id", "shoulders_id", "shirt_id", "chest_id", "belt_id", "legs_id",
                                       "boots_id", "wrists_id", "gloves_id", "tabard_id", "cape_id"), x[8:19])},
                                  can_equip=x[19], texture=ce.s(x[20])))
                self.bakes.add(ce.s(x[20]))
                if out_e[-1]["belt_id"]:
                    self.belt_displays.add(out_e[-1]["belt_id"])
            new = d
            if d in self.taken_displays:
                new = DISPLAY_BASE + moved
                moved += 1
            out_d.append(dict(id=new, model_id=model, sound_id=r[2] if r[2] in self.stock_soundData else 0,
                              extended_display_info_id=extra, creature_model_scale=c406.f32(r[4]),
                              creature_model_alpha=r[5], texture_variation_1=cd.s(r[6]), texture_variation_2=cd.s(r[7]),
                              texture_variation_3=cd.s(r[8]), portrait_texture_name=cd.s(r[9]), blood_level=r[10],
                              blood_id=r[11], npc_sound_id=self.npc_sound(r[12]),
                              praticle_color_id=r[13], creature_geoset_data=r[14], obj_effect_package_id=0))
            self.displays[d] = new
        out_m = []
        for m in sorted(self.models):
            r = cm.get(m)
            row = {k: (c406.f32(r[i]) if i in MODEL_FLOATS else r[i]) for i, k in enumerate(MODEL_COLUMNS)}
            row["model_path"] = cm.s(r[2])
            row["sound_data"] = r[13] if r[13] in self.stock_soundData else 0
            out_m.append(row)
        self.write_dbc("creaturemodeldata", out_m, "MoP creature models (CreatureModelData, 5.4.8); their files are "
                       "listed by the port, not in WHE-common yet")
        self.write_dbc("creaturedisplayinfoextra", out_e, "MoP NPC looks (CreatureDisplayInfoExtra, 5.4.8); the bakes "
                       "they name are Textures\\BakedNpcTextures\\<texture>")
        self.write_dbc("creaturedisplayinfo", out_d, "MoP creature displays (5.4.8) stock lacks; ids another modpak "
                       "uses moved to %d and up" % DISPLAY_BASE)

    def write_dbc(self, table, data, comment):
        if not data:
            return
        out = ["-- %s. Generated by tools/races/mop_wandering_isle_port.py.\n" % comment]
        for r in data:
            out.append("DELETE FROM `%s` WHERE `id` = %s;\nINSERT INTO `%s` SET\n%s;\n" % (
                table, sql_value(r["id"]), table, ",\n".join("  `%s` = %s" % (k, sql_value(v)) for k, v in r.items())))
        self.files[os.path.join("dbc", DBC_PREFIX + table + ".sql")] = "\n".join(out)

    # ---- spawns -----------------------------------------------------------------------------------------------
    def spawns(self):
        c, a = [], []
        for r in sorted(self.t("creature"), key=lambda r: r["guid"]):
            if r["id"] not in self.ct and r["id"] not in self.stock_creatures:
                dropped["spawns of creatures nothing defines"].append(r["id"])
                continue
            if r["map"] != MAP:
                dropped["spawns on other maps (the Stormwind/Orgrimmar finale)"].append("%d on %d" % (r["id"], r["map"]))
                continue
            if r["ScriptName"] and r["ScriptName"] not in SCRIPTS:
                dropped["spawn script names nothing implements yet"].append(r["ScriptName"])
            c.append([self.cguid[r["guid"]], self.entry(r["id"]), MAP, 0, 0, 1,
                      self.phasemask(r["PhaseId"], r["PhaseGroup"]), r["equipment_id"], r["position_x"], r["position_y"],
                      r["position_z"], r["orientation"], r["spawntimesecs"], r["wander_distance"], 0, 1, 0,
                      r["MovementType"], num(r["npcflag"]) & 0x7FFFFFF, num(r["unit_flags"]), 0,
                      r["ScriptName"] if r["ScriptName"] in SCRIPTS else "", 0, 1,
                      "[gen F-134 Wandering Isle]"])
        for r in self.t("creature_addon"):
            g = self.cguid.get(r["guid"])
            if g and any(x[0] == g for x in c[:1]) or g:
                a.append([g, self.path(r["PathId"]), r["mount"] if r["mount"] in self.stock_cdisp else 0,
                          self.bytes1(r), self.bytes2(r), self.emote(r["emote"], "spawn %d" % r["guid"]), 0,
                          self.auras(r["auras"], "spawn %d" % r["guid"]), ""])
        kept = {x[0] for x in c}
        a = [x for x in a if x[0] in kept]
        g, ga = [], []
        for r in sorted(self.t("gameobject"), key=lambda r: r["guid"]):
            if r["id"] in MAP_DOODADS:
                dropped["object spawns placed as map doodads instead (adt_add_doodads.py)"].append(r["id"])
                continue
            if r["id"] not in self.got and r["id"] not in self.stock_gameobjects or r["map"] != MAP:
                dropped["object spawns not on the island or of objects nothing defines"].append(r["id"])
                continue
            g.append([self.gguid[r["guid"]], r["id"], MAP, 0, 0, 1, self.phasemask(r["PhaseId"], r["PhaseGroup"]),
                      r["position_x"], r["position_y"], r["position_z"], r["orientation"], r["rotation0"], r["rotation1"],
                      r["rotation2"], r["rotation3"], r["spawntimesecs"], r["animprogress"], r["state"], "", 0,
                      "[gen F-134 Wandering Isle]"])
        gkept = {x[0] for x in g}
        for r in self.t("gameobject_addon"):
            guid = self.gguid.get(r["guid"])
            if guid not in gkept:
                continue
            # MoP's quest invisibility types (up to 30) need the core patch's 32 types (stock 12)
            ga.append([guid, r["parent_rotation0"], r["parent_rotation1"], r["parent_rotation2"], r["parent_rotation3"],
                       r["invisibilityType"] or 0, r["invisibilityValue"] or 0])
        self.write("40_creature", insert(
            "creature", "guid id map zoneId areaId spawnMask phaseMask equipment_id position_x position_y position_z "
            "orientation spawntimesecs wander_distance currentwaypoint curhealth curmana MovementType npcflag "
            "unit_flags dynamicflags ScriptName VerifiedBuild CreateObject Comment".split(), c,
            "DELETE FROM `creature` WHERE `Comment` LIKE '[gen F-134%';"))
        self.write("41_creature_addon", insert(
            "creature_addon", "guid path_id mount bytes1 bytes2 emote visibilityDistanceType auras Comment".split(), a,
            "DELETE FROM `creature_addon` WHERE `guid` BETWEEN %d AND %d;" % (CREATURE_GUID, CREATURE_GUID + 99999)))
        self.write("42_gameobject", insert(
            "gameobject", "guid id map zoneId areaId spawnMask phaseMask position_x position_y position_z orientation "
            "rotation0 rotation1 rotation2 rotation3 spawntimesecs animprogress state ScriptName VerifiedBuild "
            "Comment".split(), g, "DELETE FROM `gameobject` WHERE `Comment` LIKE '[gen F-134%';"))
        self.write("43_gameobject_addon", insert(
            "gameobject_addon", "guid parent_rotation0 parent_rotation1 parent_rotation2 parent_rotation3 "
            "invisibilityType invisibilityValue".split(), ga,
            "DELETE FROM `gameobject_addon` WHERE `guid` BETWEEN %d AND %d;" % (GAMEOBJECT_GUID, GAMEOBJECT_GUID + 99999)))
        move = {r["PathId"]: r["MoveType"] or 0 for r in self.t("waypoint_path")}
        wp = [[self.paths[r["PathId"]], r["NodeId"], r["PositionX"], r["PositionY"], r["PositionZ"], r["Orientation"],
               "", r["Delay"] or 0, move.get(r["PathId"], 0), 0, 100, 0]
              for r in self.t("waypoint_path_node") if r["PathId"] in self.paths]
        self.write("44_waypoint_data", insert(
            "waypoint_data", "id point position_x position_y position_z orientation Comment delay move_type action "
            "action_chance wpguid".split(), wp,
            "DELETE FROM `waypoint_data` WHERE `id` BETWEEN %d AND %d;" % (PATH_BASE, PATH_BASE + 99999)))

    # ---- gameobjects ------------------------------------------------------------------------------------------
    def gameobjects(self):
        gd = c406.Dbc(os.path.join(MOP_DBC, "GameObjectDisplayInfo.dbc"))
        ai = {r["entryorguid"] for r in self.t("smart_scripts", "source_type = 1 AND entryorguid > 0")}
        tmpl, addon, qitem, disp = [], [], [], []
        for e, r in sorted(self.got.items()):
            d = r["displayId"]
            if d and d not in self.stock_gdisp and d not in {x["id"] for x in disp}:
                x = gd.get(d)
                if x:
                    disp.append(dict(id=d, model_name=gd.s(x[1]), **{"sound_%d" % (i + 1): x[2 + i] if x[2 + i] in
                                     self.stock_sounds else 0 for i in range(10)},
                                     **dict(zip(("geo_box_min_x", "geo_box_min_y", "geo_box_min_z", "geo_box_max_x",
                                                 "geo_box_max_y", "geo_box_max_z"), (c406.f32(v) for v in x[12:18])))))
                    self.go_models.add(gd.s(x[1]))
                else:
                    dropped["object displays nothing has"].append(d)
            data = [num(r["Data%d" % i]) for i in range(24)]
            if r["type"] == 2 and data[3]:                 # questgiver gossip menu
                data[3] = self.menu.get(data[3], 0)
            if r["type"] > 35:
                dropped["object types 3.3.5a lacks"].append("%d type %d" % (e, r["type"]))
                continue
            script = r["ScriptName"] if r["ScriptName"] in SCRIPTS else ""
            if r["ScriptName"] and not script:
                dropped["object script names nothing implements yet"].append("%d %s" % (e, r["ScriptName"]))
            tmpl.append([e, r["type"], d, r["name"], r["IconName"] or "", r["castBarCaption"] or "", r["unk1"] or "",
                         r["size"]] + data + ["SmartGameObjectAI" if r["AIName"] and e in ai else "", script, 0])
        for r in self.t("gameobject_template_addon"):
            if r["entry"] in self.got:
                addon.append([r["entry"], self.faction(r["faction"]) if r["faction"] else 0, r["flags"]])
        for r in self.t("gameobject_questitem"):
            if r["GameObjectEntry"] in self.got:
                it = self.item(r["ItemId"])
                if it:
                    qitem.append([r["GameObjectEntry"], r["Idx"], it, 0])
        cols = ("entry type displayId name IconName castBarCaption unk1 size " + " ".join("Data%d" % i for i in range(24))
                + " AIName ScriptName VerifiedBuild").split()
        ents = in_list(self.got)
        self.write("20_gameobject_template", insert("gameobject_template", cols, tmpl,
                                                    "DELETE FROM `gameobject_template` WHERE `entry` IN %s;" % ents))
        self.write("21_gameobject_template_addon", insert(
            "gameobject_template_addon", "entry faction flags".split(), addon,
            "DELETE FROM `gameobject_template_addon` WHERE `entry` IN %s;" % ents))
        self.write("22_gameobject_questitem", insert(
            "gameobject_questitem", "GameObjectEntry Idx ItemId VerifiedBuild".split(), qitem,
            "DELETE FROM `gameobject_questitem` WHERE `GameObjectEntry` IN %s;" % ents))
        self.write_dbc("gameobjectdisplayinfo", disp, "MoP object displays (5.4.8) stock lacks")

    # ---- gossip -----------------------------------------------------------------------------------------------
    def gossip(self):
        menus = [[self.menu[r["MenuID"]], GENERIC_TEXT] for r in self.t("gossip_menu")]
        if menus:
            dropped["gossip menu texts (MoP npc_text isn't in any source here; stock's greeting instead)"].extend(
                r["TextID"] for r in self.t("gossip_menu"))
        have = {m[0] for m in menus}
        for m in self.menu.values():
            if m not in have:
                menus.append([m, GENERIC_TEXT])
        opts = []
        for r in self.t("gossip_menu_option"):
            kind = GOSSIP_NPC.get(r["OptionNpc"])
            if not kind:
                dropped["gossip options of kinds not mapped"].append("%d/%d npc %d" % (r["MenuID"], r["OptionID"],
                                                                                     r["OptionNpc"]))
                continue
            opts.append([self.menu[r["MenuID"]], r["OptionID"], kind[2], r["OptionText"] or "", 0, kind[0], kind[1],
                         self.menu.get(r["ActionMenuID"], 0), r["ActionPoiID"] or 0, r["BoxCoded"] or 0,
                         r["BoxMoney"] or 0, r["BoxText"] or "", 0])
        self.write("26_gossip_menu", insert("gossip_menu", ["MenuID", "TextID"], sorted(menus),
                                            "DELETE FROM `gossip_menu` WHERE `MenuID` BETWEEN %d AND %d;"
                                            % (MENU_BASE, MENU_BASE + 9999)))
        self.write("27_gossip_menu_option", insert(
            "gossip_menu_option", "MenuID OptionID OptionIcon OptionText OptionBroadcastTextID OptionType OptionNpcFlag "
            "ActionMenuID ActionPoiID BoxCoded BoxMoney BoxText BoxBroadcastTextID".split(), opts,
            "DELETE FROM `gossip_menu_option` WHERE `MenuID` BETWEEN %d AND %d;" % (MENU_BASE, MENU_BASE + 9999)))

    # ---- quests -----------------------------------------------------------------------------------------------
    def quests_(self):
        objectives = collections.defaultdict(list)
        for o in sorted(self.t("quest_objectives"), key=lambda o: (o["QuestID"], o["StorageIndex"], o["Order"])):
            objectives[o["QuestID"]].append(o)
        addon = {r["ID"]: r for r in self.t("quest_template_addon")}
        qt, qa, offer, req, details = [], [], [], [], []
        it = self.item
        for q, s in sorted(self.quests.items()):
            races = self.race_mask(s["AllowableRaces"])
            row = [q, s["QuestType"], s["QuestLevel"], s["MinLevel"], s["QuestSortID"], s["QuestInfoID"],
                   s["SuggestedGroupNum"], 0, 0, 0, 0, s["RewardNextQuest"], s["RewardXPDifficulty"], 0, 0,
                   self.spell_ok(s["RewardDisplaySpell1"]) or 0, self.spell_ok(s["RewardSpell"]) or 0,
                   s["RewardHonor"], 0, it(s["StartItem"]), s["Flags"] & 0xFFFFF, 0]
            for w in ("RewardDisplaySpell1", "RewardSpell"):
                if s[w] and not self.spell_ok(s[w]):
                    dropped["quest reward spells nothing has"].append("%d %s %d" % (q, w, s[w]))
            for n in range(1, 5):
                row += [it(s["RewardItem%d" % n]), s["RewardAmount%d" % n]]
            for n in range(1, 5):
                row += [it(s["ItemDrop%d" % n]), s["ItemDropQuantity%d" % n]]
            for n in range(1, 7):
                row += [it(s["RewardChoiceItemID%d" % n]), s["RewardChoiceItemQuantity%d" % n]]
            row += [0 if s["POIContinent"] == MAP else s["POIContinent"], s["POIx"], s["POIy"], s["POIPriority"],
                    s["RewardTitle"], 0, s["RewardArenaPoints"]]
            for n in range(1, 6):
                f = s["RewardFactionID%d" % n]
                if f and f not in self.stock_factions:
                    dropped["reputation rewards of factions 3.3.5a lacks"].append("%d faction %d" % (q, f))
                    f = 0
                row += [f, s["RewardFactionValue%d" % n] if f else 0, s["RewardFactionOverride%d" % n] if f else 0]
            row += [s["TimeAllowed"], races[0], races[1], s["LogTitle"] or "", s["LogDescription"] or "",
                    s["QuestDescription"] or "", s["AreaDescription"] or "", s["QuestCompletionLog"] or ""]
            npc, items, texts = [], [], []
            for o in objectives[q]:
                if o["Type"] in (0, 3):                        # monster / talk to
                    npc.append((self.entry(o["ObjectID"]), o["Amount"]))
                    texts.append(o["Description"] or "")
                elif o["Type"] == 2:                           # gameobject
                    npc.append((-o["ObjectID"], o["Amount"]))
                    texts.append(o["Description"] or "")
                elif o["Type"] == 1:
                    items.append((it(o["ObjectID"]), o["Amount"]))
                else:
                    dropped["quest objective types not mapped"].append("%d type %d" % (q, o["Type"]))
            if len(npc) > 4 or len(items) > 6:
                dropped["quests with more objectives than 3.3.5a holds"].append(q)
            npc, items, texts = (npc + [(0, 0)] * 4)[:4], (items + [(0, 0)] * 6)[:6], (texts + [""] * 4)[:4]
            for e, n in npc:
                row += [e, n]
            for i, n in items:
                row += [i, n]
            row += [0] + texts + [0]
            qt.append(row)
            a = addon.get(q, {})
            src = num(a.get("SourceSpellID"))
            if src and not self.spell_ok(src):
                dropped["quest accept spells nothing has"].append("%d %d" % (q, src))
            src = self.spell_ok(src) or 0
            classes = num(a.get("AllowableClasses"))
            qa.append([q, num(a.get("MaxLevel")), classes & CLASS_MASK if classes & CLASS_MASK else classes,
                       src, num(a.get("PrevQuestID")), num(a.get("NextQuestID")), num(a.get("ExclusiveGroup")),
                       num(a.get("BreadcrumbForQuestId")), num(a.get("RewardMailTemplateID")),
                       num(a.get("RewardMailDelay")), num(a.get("RequiredSkillID")), num(a.get("RequiredSkillPoints")),
                       0, 0, 0, 0, num(a.get("ProvidedItemCount")), num(a.get("SpecialFlags")) & 0xF])
        for r in self.t("quest_offer_reward"):
            offer.append([r["ID"]] + [self.emote(r["Emote%d" % n], "quest %d" % r["ID"]) for n in range(1, 5)]
                         + [r["EmoteDelay%d" % n] for n in range(1, 5)] + [r["RewardText"] or "", 0])
        for r in self.t("quest_request_items"):
            req.append([r["ID"], self.emote(r["EmoteOnComplete"], "quest %d" % r["ID"]),
                        self.emote(r["EmoteOnIncomplete"], "quest %d" % r["ID"]), r["CompletionText"] or "", 0])
        for r in self.t("quest_details"):
            details.append([r["ID"]] + [self.emote(r["Emote%d" % n], "quest %d" % r["ID"]) for n in range(1, 5)]
                           + [r["EmoteDelay%d" % n] for n in range(1, 5)] + [0])
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
                                               "DELETE FROM `quest_template` WHERE `ID` IN %s;" % qs,
                                               "RewardMoney is 0: MoP's money comes from QuestMoneyReward by "
                                               "RewardMoneyDifficulty, a table this port doesn't read"))
        self.write("31_quest_template_addon", insert(
            "quest_template_addon", "ID MaxLevel AllowableClasses SourceSpellID PrevQuestID NextQuestID ExclusiveGroup "
            "BreadcrumbForQuestId RewardMailTemplateID RewardMailDelay RequiredSkillID RequiredSkillPoints "
            "RequiredMinRepFaction RequiredMaxRepFaction RequiredMinRepValue RequiredMaxRepValue ProvidedItemCount "
            "SpecialFlags".split(), qa, "DELETE FROM `quest_template_addon` WHERE `ID` IN %s;" % qs))
        self.write("32_quest_offer_reward", insert(
            "quest_offer_reward", "ID Emote1 Emote2 Emote3 Emote4 EmoteDelay1 EmoteDelay2 EmoteDelay3 EmoteDelay4 "
            "RewardText VerifiedBuild".split(), offer, "DELETE FROM `quest_offer_reward` WHERE `ID` IN %s;" % qs))
        self.write("33_quest_request_items", insert(
            "quest_request_items", "ID EmoteOnComplete EmoteOnIncomplete CompletionText VerifiedBuild".split(), req,
            "DELETE FROM `quest_request_items` WHERE `ID` IN %s;" % qs))
        self.write("34_quest_details", insert(
            "quest_details", "ID Emote1 Emote2 Emote3 Emote4 EmoteDelay1 EmoteDelay2 EmoteDelay3 EmoteDelay4 "
            "VerifiedBuild".split(), details, "DELETE FROM `quest_details` WHERE `ID` IN %s;" % qs))
        wma = 808                                          # F-134's WorldMapArea for zone 5736 (mop_map_port.py)
        poi, seen = [], set()
        for r in sorted(self.t("quest_poi"), key=lambda r: (r["QuestID"], r["Idx1"], r["BlobIndex"])):
            # 3.3.5a has one blob per POI (QuestID, id is the key): MoP's extra blobs share the first one's points
            if r["QuestID"] in self.quests and (r["QuestID"], r["Idx1"]) not in seen:
                seen.add((r["QuestID"], r["Idx1"]))
                poi.append([r["QuestID"], r["Idx1"], r["ObjectiveIndex"], r["MapID"], wma if r["MapID"] == MAP else 0,
                            0, r["Priority"], r["Flags"], 0])
        pts = [[r["QuestID"], r["Idx1"], r["Idx2"], r["X"], r["Y"], 0] for r in self.t("quest_poi_points")
               if r["QuestID"] in self.quests]
        self.write("35_quest_poi", insert("quest_poi", "QuestID id ObjectiveIndex MapID WorldMapAreaId Floor Priority "
                                          "Flags VerifiedBuild".split(), poi,
                                          "DELETE FROM `quest_poi` WHERE `QuestID` IN %s;" % qs))
        self.write("36_quest_poi_points", insert("quest_poi_points", "QuestID Idx1 Idx2 X Y VerifiedBuild".split(), pts,
                                                 "DELETE FROM `quest_poi_points` WHERE `QuestID` IN %s;" % qs))
        for n, (t, ents, ent) in enumerate((("creature_queststarter", self.ct, self.entry),
                                            ("creature_questender", self.ct, self.entry),
                                            ("gameobject_queststarter", self.got, int),
                                            ("gameobject_questender", self.got, int))):
            rel = sorted({(ent(r["id"]), r["quest"]) for r in self.t(t) if r["quest"] in self.quests and r["id"] in ents}
                         | {(ent(e), q) for e, q in EXTRA_RELATIONS.get(t, ()) if q in self.quests})
            self.write("%d_%s" % (45 + n, t), insert(t, ["id", "quest"], rel,
                                                     "DELETE FROM `%s` WHERE `quest` IN %s;" % (t, qs)))

    # ---- loot, vendors, clicks ----------------------------------------------------------------------------------
    def plan_loot(self):
        """Generated loot (mop_loot.py) for the killable creatures the TC import has no loot for, from pools of what
        its 33 looted creatures drop; gold by level where it has none; Light Leather skins for beasts."""
        have = collections.defaultdict(list)
        for r in self.t("creature_loot_template"):
            if not r["ItemType"] and r["Chance"] > 0 and not r["QuestRequired"]:
                have[r["Entry"]].append(r["Item"])
        self.fill = LootFill(LOOT_REF_BASE, self.items, cloth=LINEN_CLOTH, skins=WI_SKINS)
        for e, r in self.ct.items():
            for i in have.get(num(self.diff.get(e, {}).get("LootID")), []):
                self.fill.learn(r["type"], r["family"], i)
        self.gen_loot, self.gen_skin, self.gen_gold = {}, {}, {}
        for e, r in self.ct.items():
            d = self.diff.get(e, {})
            if not killable(r["type"], num(r["unit_flags"]), num(r["npcflag"]), num(r["flags_extra"])):
                continue
            if num(d.get("LootID")) not in have:
                self.gen_loot[e] = self.fill.creature(r["type"], r["family"], r["Classification"])
            if not num(d.get("SkinLootID")):
                self.gen_skin[e] = self.fill.skinning(r["type"])
            if not num(d.get("GoldMax")):
                self.gen_gold[e] = gold(num(d.get("MaxLevel"), 1), r["Classification"])

    def loot(self):
        for n, (t, ents) in enumerate((("creature_loot_template", None), ("gameobject_loot_template", None))):
            data = []
            for r in self.t(t):
                if r["ItemType"]:
                    dropped["loot of currencies"].append(r["Item"])
                    continue
                item = self.item(r["Item"])
                if not item:
                    continue
                data.append([r["Entry"], item, 0, r["Chance"], r["QuestRequired"], r["LootMode"], r["GroupId"],
                             r["MinCount"], r["MaxCount"], r["Comment"] or ""])
            if t == "creature_loot_template":
                data += [[self.entry(e)] + row for e, v in sorted(self.gen_loot.items()) for row in v]
            keys = {r[0] for r in data}
            self.write("%d_%s" % (50 + n, t), insert(
                t, "Entry Item Reference Chance QuestRequired LootMode GroupId MinCount MaxCount Comment".split(), data,
                "DELETE FROM `%s` WHERE `Entry` IN %s;" % (t, in_list(keys)) if keys else None))
        cols = "Entry Item Reference Chance QuestRequired LootMode GroupId MinCount MaxCount Comment".split()
        skin = [[self.entry(e)] + row for e, v in sorted(self.gen_skin.items()) for row in v]
        ref = [[r[0], self.item(r[1])] + r[2:] for r in self.fill.references()[0]]
        ref = [r for r in ref if r[1]]
        for name, table, data in (("52", "skinning_loot_template", skin), ("53", "reference_loot_template", ref)):
            self.write("%s_%s" % (name, table), insert(table, cols, data, "DELETE FROM `%s` WHERE `Entry` IN %s;" % (
                table, in_list({r[0] for r in data})) if data else None))
        v = [[self.entry(r["entry"]), r["slot"], self.item(r["item"]), r["maxcount"], r["incrtime"], 0, 0]
             for r in self.t("npc_vendor") if r["entry"] in self.ct and r["type"] == 1]
        v = [r for r in v if r[2]]
        self.write("55_npc_vendor", insert("npc_vendor", "entry slot item maxcount incrtime ExtendedCost VerifiedBuild"
                                           .split(), v, "DELETE FROM `npc_vendor` WHERE `entry` IN %s;"
                                           % in_list({r[0] for r in v}) if v else None))
        c = []
        for r in self.t("npc_spellclick_spells"):
            if r["npc_entry"] in self.ct:
                if self.spell_ok(r["spell_id"]):
                    c.append([self.entry(r["npc_entry"]), self.spell_ok(r["spell_id"]), r["cast_flags"], r["user_type"]])
                else:
                    dropped["spell clicks of spells nothing has"].append("%d %d" % (r["npc_entry"], r["spell_id"]))
        self.write("56_npc_spellclick_spells", insert("npc_spellclick_spells", "npc_entry spell_id cast_flags user_type"
                                                      .split(), c, "DELETE FROM `npc_spellclick_spells` WHERE "
                                                      "`npc_entry` IN %s;" % in_list({r[0] for r in c}) if c else None))
        acc = [[self.entry(r["entry"]), self.entry(r["accessory_entry"]), r["seat_id"], r["minion"],
                r["description"] or "", r["summontype"], r["summontimer"]]
               for r in self.t("vehicle_template_accessory") if r["entry"] in self.ct]
        self.write("58_vehicle_template_accessory", insert(
            "vehicle_template_accessory", "entry accessory_entry seat_id minion description summontype summontimer"
            .split(), acc, "DELETE FROM `vehicle_template_accessory` WHERE `entry` IN %s;" % in_list(r[0] for r in acc)
            if acc else None))

    # ---- SmartAI and conditions -------------------------------------------------------------------------------
    def smart(self):
        out = []
        st_ok = {0, 1, 2, 9}
        for r in self.t("smart_scripts"):
            st, e = r["source_type"], r["entryorguid"]
            if st not in st_ok:
                dropped["SmartAI source types"].append(st)
                continue
            if st == 0:
                if e < 0:
                    e = -self.cguid.get(-e, 0)
                elif e in self.ct:
                    e = self.entry(e)
                else:
                    e = 0
            elif st == 1:
                if e < 0:
                    e = -self.gguid.get(-e, 0)
                elif e not in self.got:
                    e = 0
            elif st == 2:
                self.triggers.add(e)
            if not e:
                continue
            ev, a = r["event_type"], r["action_type"]
            ep = [num(r["event_param%d" % i]) for i in range(1, 5)]
            p = [num(r["action_param%d" % i]) for i in range(1, 7)]
            tt, tp = r["target_type"], [num(r["target_param%d" % i]) for i in range(1, 5)]
            why = None
            if ev in SAI_EVENT_DROP:
                why = "event %d" % ev
            elif a in SAI_ACTION_DROP:
                why = "action %d" % a
            elif tt > 29:
                why = "target %d" % tt
            ev = SAI_EVENT_MAP.get(ev, ev)
            if ev in (108, 109):
                ep[1] = self.path(ep[1]) if ep[1] else 0
            if a == 53:                                    # WP_START (run, path, repeat, ...) -> WAYPOINT_START
                p = [self.path(p[1]), p[2], 0, 0, 0, 0]
            elif a == 127:                                 # PAUSE_MOVEMENT (slot, timer, force) -> MOVEMENT_PAUSE
                p = [p[1], 0, 0, 0, 0, 0]
            a = SAI_ACTION_MAP.get(a, a)
            if not why and a in SAI_SPELL_ACTIONS:
                why = None if self.spell_ok(p[0]) else "spell %d" % p[0]
                p[0] = self.spell_ok(p[0]) or 0
            if not why and ev in SAI_SPELL_EVENTS and ep[0]:
                why = None if self.spell_ok(ep[0]) else "spell %d" % ep[0]
                ep[0] = self.spell_ok(ep[0]) or 0
            if not why and a == 68 and p[0] not in self.stock_movies:
                why = "movie %d" % p[0]
            if why:
                dropped["SmartAI rows (%s)" % why.split()[0]].append("%d/%d/%d %s" % (r["entryorguid"], st, r["id"], why))
                continue
            if a in SAI_ENTRY_ACTIONS:
                p[SAI_ENTRY_ACTIONS[a]] = self.entry(p[SAI_ENTRY_ACTIONS[a]])
            if a in (5, 10):                               # emotes
                p = [self.emote(x, "SmartAI %d" % r["entryorguid"]) if i < (1 if a == 5 else 6) else x
                     for i, x in enumerate(p)]
            if a in (56, 57):                              # add / remove item
                p[0] = self.item(p[0])
            if a == 115:                                   # random sound
                p[:4] = [x if x in self.stock_sounds else 0 for x in p[:4]]
            if a == 98:
                p[0] = self.menu.get(p[0], p[0])
                p[1] = GENERIC_TEXT
            if ev == 62:
                ep[0] = self.menu.get(ep[0], ep[0])
            if ev == 75:                                   # distance to creature (guid, entry, ...)
                ep[0] = self.cguid.get(ep[0], ep[0])
                ep[1] = self.entry(ep[1])
            if tt in SAI_ENTRY_TARGETS:
                tp[SAI_ENTRY_TARGETS[tt]] = self.entry(tp[SAI_ENTRY_TARGETS[tt]])
            elif tt == 10:
                tp[0] = self.cguid.get(tp[0], tp[0])
                tp[1] = self.entry(tp[1])
            elif tt == 14:
                tp[0] = self.gguid.get(tp[0], tp[0])
            out.append([e, st, r["id"], r["link"], ev, r["event_phase_mask"], r["event_chance"], r["event_flags"] & 0x1FF]
                       + ep + [num(r["event_param5"]), 0, a] + p + [tt] + tp
                       + [r["target_x"], r["target_y"], r["target_z"], r["target_o"], r["comment"] or ""])
        keys = sorted({(r[0], r[1]) for r in out})
        delete = "\n".join("DELETE FROM `smart_scripts` WHERE `entryorguid` = %d AND `source_type` = %d;" % k for k in keys)
        cols = ("entryorguid source_type id link event_type event_phase_mask event_chance event_flags event_param1 "
                "event_param2 event_param3 event_param4 event_param5 event_param6 action_type action_param1 "
                "action_param2 action_param3 action_param4 action_param5 action_param6 target_type target_param1 "
                "target_param2 target_param3 target_param4 target_x target_y target_z target_o comment").split()
        self.write("65_smart_scripts", insert("smart_scripts", cols, out, delete))

    def condition_values(self, r):
        """(type, values) of a condition row moved to AzerothCore, or None to drop it."""
        ct = CONDITION_TYPE_MAP.get(r["ConditionTypeOrReference"], r["ConditionTypeOrReference"])
        v = [num(r["ConditionValue1"]), num(r["ConditionValue2"]), num(r["ConditionValue3"])]
        if ct in CONDITION_TYPE_DROP:
            dropped["conditions of types AzerothCore lacks"].append(ct)
            return None
        if ct in (CONDITION_AURA, CONDITION_SPELL):
            if not self.spell_ok(v[0]):
                dropped["conditions on spells nothing has"].append(v[0])
                return None
            v[0] = self.spell_ok(v[0])
        if ct == CONDITION_PHASE:
            v[0] = sum(self.phasemask(p) for p in {v[0]})
        if ct == 2:
            v[0] = self.item(v[0])
        if ct == 29:                                       # near creature
            v[0] = self.entry(v[0])
        if ct == 31:                                       # object entry / guid
            if v[0] == 3:
                v[1], v[2] = self.entry(v[1]), self.cguid.get(v[2], v[2])
            elif v[0] == 5:
                v[2] = self.gguid.get(v[2], v[2])
        return ct, v

    def conditions(self):
        out = []
        for r in self.t("conditions"):
            st, g, e, sid = r["SourceTypeOrReferenceId"], r["SourceGroup"], r["SourceEntry"], r["SourceId"]
            if st in CONDITION_SOURCE_DROP or st == 26:
                if st != 26:
                    dropped["conditions of source types AzerothCore lacks"].append(st)
                continue
            if st in (14, 15):
                g = self.menu.get(g, g)
            elif st == 22:
                if sid == 0:
                    e = -self.cguid.get(-e, 0) if e < 0 else self.entry(e)
                elif sid == 1 and e < 0:
                    e = -self.gguid.get(-e, 0)
            elif st in (13, 17):
                if not self.spell_ok(e):
                    dropped["conditions on spells nothing has"].append(e)
                    continue
                e = self.spell_ok(e)
            elif st == 16:                                 # vehicle spell (creature, spell)
                g = self.entry(g)
            elif st == 18:                                 # spellclick (creature, spell)
                g = self.entry(g)
                if not self.spell_ok(e):
                    continue
                e = self.spell_ok(e)
            cv = self.condition_values(r)
            if not cv or not e and st == 22:
                continue
            out.append([st, g, e, sid, r["ElseGroup"], cv[0], r["ConditionTarget"]] + cv[1]
                       + [num(r["NegativeCondition"]), num(r["ErrorType"]), num(r["ErrorTextId"]), "", r["Comment"] or ""])
        # phases: one definition per phase_area row, with its area as a condition and the phase's own conditions
        # (SourceEntry the area or 0, any area) in each else group; entry 1 is the default phase for everyone
        phases = [[ZONE, 1, 1, 0, 0, 0, 0, "Wandering Isle default phase (TrinityCore 169)"]]
        conds = collections.defaultdict(list)
        for r in self.t("conditions", "SourceTypeOrReferenceId = 26"):
            conds[(r["SourceGroup"], r["SourceEntry"])].append(r)
        for a in sorted(self.t("phase_area"), key=lambda a: (a["PhaseId"], a["AreaId"])):
            if a["PhaseId"] in DEFAULT_PHASES:
                continue
            if a["AreaId"] not in self.island_areas:
                dropped["phase areas off the island (the finale)"].append("%d/%d" % (a["AreaId"], a["PhaseId"]))
                continue
            n = len(phases) + 1
            phases.append([ZONE, n, self.phase_bit[a["PhaseId"]], 0, 0, 0, 0, a["Comment"] or ""])
            mine = conds[(a["PhaseId"], a["AreaId"])] + conds[(a["PhaseId"], 0)]
            groups = sorted({c["ElseGroup"] for c in mine}) or [0]
            for gnum in groups:
                if a["AreaId"] != ZONE:
                    out.append([26, ZONE, n, 0, gnum, CONDITION_AREA, 0, a["AreaId"], 0, 0, 0, 0, 0, "",
                                "F-134 phase %d in area %d" % (a["PhaseId"], a["AreaId"])])
                for c in mine:
                    if c["ElseGroup"] != gnum:
                        continue
                    cv = self.condition_values(c)
                    if cv:
                        out.append([26, ZONE, n, 0, gnum, cv[0], c["ConditionTarget"]] + cv[1]
                                   + [num(c["NegativeCondition"]), 0, 0, "", "F-134 phase %d" % a["PhaseId"]])
        keys = sorted({(r[0], r[1], r[2], r[3]) for r in out if r[0] != 26})
        delete = "\n".join("DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId` = %d AND `SourceGroup` = %d AND "
                           "`SourceEntry` = %d AND `SourceId` = %d;" % k for k in keys)
        delete += "\nDELETE FROM `conditions` WHERE `SourceTypeOrReferenceId` = 26 AND `SourceGroup` = %d;" % ZONE
        self.write("70_conditions", insert(
            "conditions", "SourceTypeOrReferenceId SourceGroup SourceEntry SourceId ElseGroup ConditionTypeOrReference "
            "ConditionTarget ConditionValue1 ConditionValue2 ConditionValue3 NegativeCondition ErrorType ErrorTextId "
            "ScriptName Comment".split(), out, delete))
        create = open(os.path.join(HERE, "cata_gilneas_fixes", "phase_definitions_table.sql"), encoding="utf8").read()
        self.write("90_phase_definitions", create + "\n" + insert(
            "phase_definitions", "zoneId entry phaseMask phaseId originmap terrainswapmap flags comment".split(), phases,
            "DELETE FROM `phase_definitions` WHERE `zoneId` = %d;" % ZONE,
            "TrinityCore phase id -> phasemask bit: %s" % ", ".join("%d=%d" % kv for kv in sorted(self.phase_bit.items()))))

    def spell_rows(self):
        area = []
        for r in self.t("spell_area"):
            if not self.spell_ok(r["spell"]):
                dropped["spell_area rows of spells nothing has"].append(r["spell"])
                continue
            area.append([self.spell_ok(r["spell"]), r["area"], r["quest_start"], r["quest_end"], self.spell_ok(r["aura_spell"]) or 0,
                         self.race_mask(r["racemask"])[0], r["gender"], r["flags"] & 1, r["quest_start_status"],
                         r["quest_end_status"]])
        self.write("91_spell_area", insert(
            "spell_area", "spell area quest_start quest_end aura_spell racemask gender autocast quest_start_status "
            "quest_end_status".split(), area, "\n".join(
                "DELETE FROM `spell_area` WHERE `spell` = %d AND `area` = %d;" % (r[0], r[1]) for r in area)))
        pos, seen = [], set()
        for r in sorted(self.t("spell_target_position"), key=lambda r: (r["ID"], r["EffectIndex"], r["OrderIndex"])):
            # 3.3.5a has one position per spell effect: the first of MoP's (OrderIndex) is kept
            if self.spell_ok(r["ID"]) and (r["ID"], r["EffectIndex"]) not in seen:
                seen.add((r["ID"], r["EffectIndex"]))
                pos.append([self.spell_ok(r["ID"]), r["EffectIndex"], r["MapID"], r["PositionX"], r["PositionY"],
                            r["PositionZ"], r["Orientation"] or 0])
        names_ = [[self.spell_ok(r["spell_id"]), r["ScriptName"]] for r in self.t("spell_script_names")
                  if r["ScriptName"] in SCRIPTS and self.spell_ok(r["spell_id"])]
        self.write("61_spell_script_names", insert(
            "spell_script_names", ["spell_id", "ScriptName"], names_,
            "DELETE FROM `spell_script_names` WHERE `ScriptName` IN (%s);" % ", ".join(
                sql_value(n) for n in sorted({r[1] for r in names_})) if names_ else None))
        self.write("60_spell_target_position", insert(
            "spell_target_position", "ID EffectIndex MapID PositionX PositionY PositionZ Orientation".split(), pos,
            "DELETE FROM `spell_target_position` WHERE `ID` IN %s;" % in_list(r[0] for r in pos) if pos else None))
        # area triggers SmartAI uses (SmartTrigger), with their 5.4.8 AreaTrigger.dbc rows
        names = {r["entry"]: r["ScriptName"] for r in self.t("areatrigger_scripts")}
        at = c406.Dbc(os.path.join(MOP_DBC, "AreaTrigger.dbc"))
        scripts, dbc = [], []
        for e in sorted(self.triggers | set(names)):
            name = names.get(e, "SmartTrigger")
            if name != "SmartTrigger" and name not in SCRIPTS:
                dropped["area trigger scripts nothing implements yet"].append("%d %s" % (e, name))
                continue
            scripts.append([e, name])
            if e not in self.stock_at:
                x = at.get(e)
                if not x:
                    dropped["area triggers the 5.4.8 client lacks"].append(e)
                    continue
                dbc.append(dict(id=e, map_id=x[1], x=c406.f32(x[2]), y=c406.f32(x[3]), z=c406.f32(x[4]),
                                radius=c406.f32(x[8]), box_length=c406.f32(x[9]), box_width=c406.f32(x[10]),
                                box_height=c406.f32(x[11]), box_yaw=c406.f32(x[12])))
        self.write("62_areatrigger_scripts", insert(
            "areatrigger_scripts", ["entry", "ScriptName"], scripts,
            "DELETE FROM `areatrigger_scripts` WHERE `entry` IN %s;" % in_list(r[0] for r in scripts) if scripts else None))
        self.write_dbc("areatrigger", dbc, "MoP area triggers (5.4.8) the island's SmartAI uses")

    # ---- client rows: items, factions ---------------------------------------------------------------------------
    def client_rows(self):
        ports = sorted(c for c, i in self.item_ids.items() if i)
        tmpl = [self.items.template(c, c) for c in ports]
        for t in tmpl:
            t["AllowableRace"] = self.race_mask(t["AllowableRace"])[0] or -1
            for n in range(1, 6):
                if t["spellid_%d" % n]:
                    t["spellid_%d" % n] = self.spell_ok(t["spellid_%d" % n]) or 0
            t["AllowableClass"] = -1 if t["AllowableClass"] in (-1, 0x7FFF, 0x5FF) else t["AllowableClass"]
        cols = list(ITEM_TEMPLATE_COLUMNS)
        self.write("05_item_template", insert(
            "item_template", cols, [[t[c] for c in cols] for t in tmpl],
            "DELETE FROM `item_template` WHERE `entry` IN %s;" % in_list(ports) if ports else None,
            "MoP items the island uses, from the 5.4.8 client (mop_items.py), English names from wago.tools"))
        item_dbc = [[t["entry"], t["class"], t["subclass"], t["SoundOverrideSubclass"], t["Material"], t["displayid"],
                     t["InventoryType"], t["sheath"]] for t in tmpl]
        if item_dbc:
            self.files[os.path.join("dbc", DBC_PREFIX + "item.sql")] = insert(
                "item", "id class subclass sound_override_subclass material display_id inventory_type sheath".split(),
                item_dbc, "DELETE FROM `item` WHERE `id` IN %s;" % in_list(ports),
                "Item.dbc rows of the items above")
        # MoP's Pandaren belts show geoset 1803 (group 2), which neither the stock models nor F-129's Pandaren have:
        # the client hides the whole belt group, default belly included, and the waist goes see-through
        belts = self.belt_displays | {t["displayid"] for t in tmpl if t["InventoryType"] == 6}
        group = DISPLAY_COLUMNS.index("geoset_group_1")
        for i in belts & self.items.added.keys():
            if self.items.added[i][group] > 1:
                self.items.added[i] = self.items.added[i][:group] + (0,) + self.items.added[i][group + 1:]
        if self.items.added:
            self.files[os.path.join("dbc", DBC_PREFIX + "itemdisplayinfo.sql")] = display_sql(
                self.items, "-- MoP item displays (5.4.8) stock lacks. Generated by mop_wandering_isle_port.py.\n")
        ft = c406.Dbc(os.path.join(MOP_DBC, "FactionTemplate.dbc"))
        out = []
        for i in sorted(self.faction_templates):
            r = ft.get(i)
            if not r:
                dropped["faction templates nothing has"].append(i)
                continue
            if r[1] not in self.stock_factions:
                dropped["faction templates of factions 3.3.5a lacks (kept; no reputation)"].append("%d (%d)" % (i, r[1]))
            row = dict(id=i, faction=r[1], flags=r[2], faction_group=r[3], friend_group=r[4], enemy_group=r[5])
            row.update({"enemies_%d" % (n + 1): r[6 + n] for n in range(4)})
            row.update({"friends_%d" % (n + 1): r[10 + n] for n in range(4)})
            out.append(row)
        self.write_dbc("factiontemplate", out, "MoP faction templates (5.4.8) of the island's NPCs and objects")

    # ---- output -----------------------------------------------------------------------------------------------
    def write(self, name, sql):
        if sql:
            self.files[os.path.join(SQL_DIR, SQL_PREFIX + name + ".sql")] = sql

    def header(self, core):
        """wandering_isle_ids.h: the ids the core's wandering_isle.cpp takes from TrinityCore that this port renumbers."""
        spawn = {}
        for r in self.t("creature", "StringId IS NOT NULL AND StringId <> ''"):
            spawn[r["StringId"]] = self.cguid[r["guid"]]
        fn = lambda name, pairs: ("constexpr uint32 %s(uint32 id)\n{\n    switch (id)\n    {\n" % name
                                  + "".join("        case %d: return %d;\n" % kv for kv in pairs)
                                  + "        default: return id;\n    }\n}\n")
        text = ["// Generated by WHE's tools/races/mop_wandering_isle_port.py (F-134): the TrinityCore ids the Wandering Isle",
                "// scripts use, as F-134's SQL numbers them. Regenerate it with the port (--core) rather than editing it.",
                "", "#ifndef WANDERING_ISLE_IDS_H", "#define WANDERING_ISLE_IDS_H", "", "#include \"Define.h\"", "",
                "namespace WanderingIsleIds", "{",
                fn("Path", [(p, self.paths[p]) for p in SCRIPT_PATHS if p in self.paths]),
                fn("Menu", [(m, self.menu[m]) for m in SCRIPT_MENUS if m in self.menu]),
                fn("Entry", sorted(self.entry_map.items())),
                fn("PhaseMask", sorted(self.phase_bit.items())),
                "// creature spawns TrinityCore finds by StringId"]
        text += ["constexpr uint32 SPAWN_%s = %d;" % (k.upper(), v) for k, v in sorted(spawn.items())]
        text += ["}", "", "#endif", ""]
        path = os.path.join(core, "src", "server", "scripts", "Custom", "wandering_isle_ids.h")
        with open(path, "w", encoding="utf8", newline="\n") as f:
            f.write("\n".join(text))
        print("wrote %s" % path)

    def run(self):
        self.go_models = set()
        self.port_spells()
        at = c406.Dbc(os.path.join(MOP_DBC, "AreaTable.dbc"))
        self.island_areas = {r[0] for r in at.records if r[1] == MAP}
        self.plan_loot()
        self.creatures()
        self.spawns()
        self.gameobjects()
        self.gossip()
        self.quests_()
        self.loot()
        self.smart()
        self.conditions()
        self.spell_rows()
        self.client_rows()
        self.write_vehicles()
        self.write_npc_sounds()
        if self.core:
            self.header(self.core)
        for old in glob.glob(os.path.join(self.dest, SQL_DIR, SQL_PREFIX + "*.sql")) + \
                glob.glob(os.path.join(self.dest, "dbc", DBC_PREFIX + "*.sql")):
            os.remove(old)
        for name, sql in self.files.items():
            path = os.path.join(self.dest, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf8", newline="\n") as f:
                f.write("-- Generated by tools/races/mop_wandering_isle_port.py from the TrinityCore MoP Classic port's "
                        "Wandering Isle import: change the script, not this file.\n\n" + sql)
        cm = c406.Dbc(os.path.join(MOP_DBC, "CreatureModelData.dbc"))
        assets = sorted({cm.s(cm.get(m)[2]) for m in self.models} | self.go_models) + \
            sorted("Textures\\BakedNpcTextures\\" + b for b in self.bakes) + self.spells.icon_files()
        with open(os.path.join(self.dest, "wi_assets.txt"), "w", encoding="utf8", newline="\n") as f:
            f.write("\n".join(assets) + "\n")
        print("ported: %d creatures (%d moved), %d spawns, %d objects, %d quests, %d displays, %d models, %d bakes, "
              "%d object models, %d items, %d phases" % (
                  len(self.ct), len(self.entry_map), len(self.cguid), len(self.got), len(self.quests),
                  sum(1 for d, n in self.displays.items() if d not in self.stock_cdisp), len(self.models),
                  len(self.bakes), len(self.go_models), sum(1 for v in self.item_ids.values() if v),
                  len(self.phase_bit)))
        for k, v in sorted(dropped.items()):
            v = sorted(set(map(str, v)))
            print("%s (%d): %s" % (k, len(v), ", ".join(v[:30]) + (" ..." if len(v) > 30 else "")))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("updates")
    ap.add_argument("dest")
    ap.add_argument("--data", default="D:/wow-scratch/wi/db2")
    ap.add_argument("--core", help="azerothcore-wotlk checkout to write src/server/scripts/Custom/wandering_isle_ids.h to")
    a = ap.parse_args()
    port = Port(a.updates, a.dest, a.data)
    port.core = a.core
    port.run()

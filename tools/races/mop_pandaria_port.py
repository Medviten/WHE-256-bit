#!/usr/bin/env python3
"""Pandaria's NPCs (F-133) from SkyFire 5.4.8's world database, for AzerothCore 3.3.5a.

  python -I -X utf8 mop_pandaria_port.py SFDB_SQL [--modpak modpaks/F-133_mop-pandaria] [--data D:/wow-scratch/wi/db2]

SFDB_SQL is SkyFire's full release (https://github.com/ProjectSkyfire/SkyFire_548/releases). Its schema is the old
TrinityCore one AzerothCore kept, so rows map across nearly column for column. The DBC side reuses
mop_wandering_isle_port.py's Port (displays, factions, items, vehicles), pointed at F-133's files and id ranges.

Stage 1, NPCs: every creature SkyFire spawns on map 870 (2,876 templates, 29,796 spawns) with its template, models
and displays (CreatureDisplayInfo/Extra/ModelData rows stock lacks, bakes and models listed in wi_assets.txt for
tools/models/mop_assets.py), model info, movement, equipment, addons, texts, vendors (with their MoP items), gossip
menus with SkyFire's npc_text, and the faction templates stock lacks.

- Levels above 80 move down by 10 (Pandaria's 85-90 become 75-80): AzerothCore has no class stats past 83 and the
  players' cap is 80. Expansion (exp) is capped at 2.
- Entries another modpak or config.sql's creature range uses move to ENTRY_BASE and up; stock entries are kept as
  they are and not redefined; entries F-134 (the Wandering Isle) defines are left to it.
- Auras and SmartAI that need MoP spells, C++ script names (none ported yet), trainers' spell lists and flight
  paths come in later stages; such fields are dropped here and listed at the end.
- Loot: SkyFire's own for the 157 creatures it has loot for; every other killable creature gets generated loot
  (mop_loot.py: zone junk, white goods by creature type, cloth, BoE world greens/blues/epics from what SkyFire's
  looted creatures drop), gold by level where SkyFire has none, Exotic Leather skins for beasts and dragonkin.
- MoP gear is rescaled to WotLK's levels 71-80 by mop_items.py (required level, item level, stats, armour, damage);
  random-suffix groups come from SkyFire's item_enchantment_template, stock suffixes only.
- Spawns in SkyFire's phase 1740 (153) go into the default phase.

Quests: every quest a creature or object spawned on 870 starts or ends (971), with objectives (kill, talk, object,
item; MoP's currency/spell/reputation/pet-battle objectives are dropped), texts, emotes, POIs and givers. The objects
quests need (givers, objectives, chests holding quest items) are ported with their spawns from guid GAMEOBJECT_GUID;
those chests keep all their loot. Currency rewards, MoP reputation factions and MoP titles are dropped."""
import argparse, collections, glob, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mop_wandering_isle_port as wi  # noqa: E402
from mop_pandaria_nodes import sfdb  # noqa: E402
from cata_items import ITEM_TEMPLATE_COLUMNS, display_sql, sql_value  # noqa: E402
from cata_gilneas_port import insert, in_list  # noqa: E402
from mop_items import MopItems  # noqa: E402
from mop_loot import LootFill, killable, gold  # noqa: E402
import cata406_dbc_port as c406  # noqa: E402

MAP, TAG = 870, "F-133"
# point the island port's module constants at F-133
wi.TAG = TAG
wi.SQL_PREFIX = "zz_[AUTO,%s]_pa_" % TAG
wi.DBC_PREFIX = "[%s]_pa_" % TAG
wi.ENTRY_BASE = 1330000
wi.DISPLAY_BASE = 1335000
wi.MENU_BASE = 1330000
wi.TEXT_BASE = 1330000
CREATURE_GUID = 13500001
LEVEL_SHIFT = 10
NPCFLAG_MASK = 0x3FFFFFF          # 3.3.5a's npc flags (MoP adds 0x4000000 and up)
TABLES = {"creature", "creature_template", "creature_addon", "creature_template_addon", "creature_equip_template",
          "creature_model_info", "creature_text", "npc_vendor", "gossip_menu", "gossip_menu_option", "npc_text",
          "quest_template", "quest_objective", "quest_poi", "quest_poi_points", "creature_queststarter",
          "creature_questender", "gameobject_queststarter", "gameobject_questender", "creature_loot_template",
          "gameobject_loot_template", "gameobject_template", "gameobject", "skinning_loot_template",
          "item_enchantment_template"}
LOOT_REF_BASE = 1330000           # reference_loot_template entries of the generated pools
WINDWOOL_CLOTH = 72988
PANDARIA_SKINS = [(72120, 100, 1, 3), (72162, 5, 1, 1)]   # Exotic Leather; Sha-Touched Leather
GAMEOBJECT_GUID = 13600000        # the nodes (mop_pandaria_nodes.py) have 13500000-13599999
dropped = wi.dropped


def level(v):
    v = int(v)
    return v - LEVEL_SHIFT if v > 80 else v


class PandariaPort(wi.Port):
    def __init__(self, sfdb_sql, dest, data):
        self.dest, self.data, self.files = dest, data, {}
        self.spell_map, self.vehicles = {}, {}
        self.db = sfdb(sfdb_sql, TABLES)
        for rows_ in self.db.values():
            for r in rows_:
                for k, v in r.items():
                    if v == "NULL":
                        r[k] = None
        self.stock_spells = wi.dbc_ids("Spell") | wi.modpak_spells()
        self.stock_emotes = wi.dbc_ids("Emotes")
        self.stock_sounds = wi.dbc_ids("SoundEntries")
        self.stock_cdisp = wi.dbc_ids("CreatureDisplayInfo")
        self.stock_extra = wi.dbc_ids("CreatureDisplayInfoExtra")
        self.stock_models = wi.dbc_ids("CreatureModelData")
        self.stock_ft = wi.dbc_ids("FactionTemplate")
        self.stock_factions = wi.dbc_ids("Faction") | {1352, 1353}
        self.stock_languages = wi.dbc_ids("Languages")
        self.stock_vehicles = wi.dbc_ids("Vehicle")
        self.stock_families = wi.dbc_ids("CreatureFamily")
        self.stock_soundData = wi.dbc_ids("CreatureSoundData")
        self.stock_npcsounds = wi.dbc_ids("NPCSounds")
        self.stock_creatures = wi.base_ids("creature_template")
        self.emote_map = wi.emote_names(self.stock_emotes)
        self.items = MopItems(wi.MOP_DBC, wi.STOCK_DBC, os.path.join(data, "ItemSparse.csv"),
                              wi.config_range("NextItemDisplayID"))
        groups = collections.defaultdict(list)
        for r in self.db["item_enchantment_template"]:
            groups[int(r["entry"])].append((int(r["ench"]), float(r["chance"])))
        self.items.enchant_groups = dict(groups)
        f134 = os.path.join(wi.MODPAKS, "F-134_mop-wandering-isle")
        self.f134_entries = wi_entries(f134)
        self.taken_entries = (wi.config_range("NextCreatureID") | wi.taken("creature_template", "entry")) - self.f134_entries
        # F-134 writes the same 5.4.8 rows for the displays both use
        self.taken_displays = (wi.config_range("NextDisplayID") | wi.taken("creaturedisplayinfo", "id")) - \
            wi.modpak_display_ids(f134)
        spawns = [r for r in self.db["creature"] if int(r["map"]) == MAP]
        templates = {int(r["entry"]): r for r in self.db["creature_template"]}
        used = {int(r["id"]) for r in spawns}
        # the creatures this port defines: spawned here, not stock, not the Wandering Isle's
        self.ct = {e: templates[e] for e in sorted(used) if e in templates and e not in self.stock_creatures
                   and e not in self.f134_entries}
        self.spawn_rows = spawns
        self.entry_map = {}
        for e in self.ct:
            if e in self.taken_entries:
                self.entry_map[e] = wi.ENTRY_BASE + len(self.entry_map)
        self.item_ids, self.faction_templates, self.displays = {}, set(), {}
        self.bakes, self.models, self.belt_displays, self.gender = set(), set(), set(), {}
        menus = sorted({int(r["gossip_menu_id"]) for r in self.ct.values() if int(r["gossip_menu_id"])})
        self.menu = {m: wi.MENU_BASE + i for i, m in enumerate(menus)}
        self.select_quests()

    # ---- what the quest stage takes -----------------------------------------------------------------------------
    def select_quests(self):
        """Quests the creatures and objects spawned on 870 start or end; the objects they need (givers, objectives,
        chests holding their items); the quest-item loot of creatures and those chests."""
        cr = {int(r["id"]) for r in self.spawn_rows}
        gos = [r for r in self.db["gameobject"] if int(r["map"]) == MAP]
        go = {int(r["id"]) for r in gos}
        qs = {int(r["Id"]): r for r in self.db["quest_template"]}
        rel = lambda t, ids: {int(r["quest"]) for r in self.db[t] if int(r["id"]) in ids}
        f134 = wi_ids(os.path.join(wi.MODPAKS, "F-134_mop-wandering-isle"), "quest_template", "ID")
        self.quests = {q: qs[q] for q in sorted((rel("creature_queststarter", cr) | rel("creature_questender", cr) |
                                                 rel("gameobject_queststarter", go) | rel("gameobject_questender", go))
                                                & set(qs) - f134)}
        clash = sorted(set(self.quests) & (wi.taken("quest_template", "ID") - f134))
        if clash:
            sys.exit("quest ids another modpak uses: %s" % clash)
        self.objectives = collections.defaultdict(list)
        for o in sorted(self.db["quest_objective"], key=lambda o: (int(o["questId"]), int(o["index"]))):
            if int(o["questId"]) in self.quests:
                self.objectives[int(o["questId"])].append(o)
        qitems = {int(o["objectId"]) for v in self.objectives.values() for o in v if o["type"] == "1"}
        qitems |= {int(q["RequiredSourceItemId%d" % n]) for q in self.quests.values() for n in range(1, 5)} - {0}
        # SkyFire's loot, keyed by the loot id its templates name (none of Pandaria's uses reference tables);
        # chests count as quest objects when they hold a quest item
        self.creature_loot = collections.defaultdict(list)
        for r in self.db["creature_loot_template"]:
            if int(r["mincountOrRef"]) > 0:
                self.creature_loot[int(r["entry"])].append(r)
        go_loot = collections.defaultdict(list)
        for r in self.db["gameobject_loot_template"]:
            if int(r["mincountOrRef"]) > 0:
                go_loot[int(r["entry"])].append(r)
        go_loot = {k: v for k, v in go_loot.items() if any(int(r["item"]) in qitems for r in v)}
        gt = {int(r["entry"]): r for r in self.db["gameobject_template"]}
        want_go = rel_ids(self.db["gameobject_queststarter"], self.quests) | \
            rel_ids(self.db["gameobject_questender"], self.quests) | \
            {int(o["objectId"]) for v in self.objectives.values() for o in v if o["type"] == "2"}
        want_go |= {e for e in go if e in gt and gt[e]["type"] == "3" and int(gt[e]["data1"]) in go_loot}
        self.stock_gameobjects = wi.base_ids("gameobject_template")
        self.got = {e: gt[e] for e in sorted(want_go & go) if e in gt and e not in self.stock_gameobjects}
        clash = sorted(set(self.got) & wi.taken("gameobject_template", "entry"))
        if clash:
            sys.exit("gameobject entries another modpak uses: %s" % clash)
        self.go_loot = {int(r["data1"]): go_loot[int(r["data1"])] for r in self.got.values()
                        if r["type"] == "3" and int(r["data1"]) in go_loot}
        self.go_spawns = [r for r in sorted(gos, key=lambda r: int(r["guid"])) if int(r["id"]) in self.got]
        self.go_models = set()

    def entry(self, e):
        e = int(e)
        return self.entry_map.get(e, e)

    # ---- creatures --------------------------------------------------------------------------------------------
    def creatures(self):
        n = lambda r, k, d=0: int(float(r[k])) if r.get(k) not in (None, "", "NULL") else d
        f = lambda r, k, d=1.0: float(r[k]) if r.get(k) not in (None, "", "NULL") else d
        tmpl, movement, models = [], [], []
        for e, r in self.ct.items():
            if r.get("ScriptName"):
                dropped["C++ script names (not ported yet)"].append("%d %s" % (e, r["ScriptName"]))
            if r.get("AIName"):
                dropped["SmartAI (not ported yet)"].append(e)
            family = wi.pet_family(n(r, "family"), self.stock_families)
            vehicle = self.vehicle(n(r, "VehicleId"))
            tmpl.append([self.entry(e), 0, 0, 0, self.entry(r["KillCredit1"]), self.entry(r["KillCredit2"]), r["name"],
                         r["subname"] or None, r["IconName"] or None, self.menu.get(n(r, "gossip_menu_id"), 0),
                         level(r["minlevel"]), level(r["maxlevel"]), min(n(r, "exp"), 2), self.faction(n(r, "faction_A")),
                         n(r, "npcflag") & NPCFLAG_MASK & ~0x10, f(r, "speed_walk"), f(r, "speed_run"), 1, 1, 18,
                         n(r, "npc_rank"), n(r, "dmgschool"), f(r, "dmg_multiplier"), n(r, "baseattacktime", 2000) or 2000,
                         n(r, "rangeattacktime", 2000) or 2000, 1, 1, n(r, "unit_class", 1) or 1, n(r, "unit_flags"),
                         n(r, "unit_flags2") & 0x3FFFF, 0, family, n(r, "type"), n(r, "type_flags") & 0xFFFFF,
                         self.entry(e) if self.loot_rows.get(e) else 0, 0, self.entry(e) if self.skin_rows.get(e) else 0,
                         0, vehicle] + list(self.gold.get(e, (n(r, "mingold"), n(r, "maxgold")))) +
                        ["", n(r, "MovementType") & 1, f(r, "HoverHeight"),
                         f(r, "Health_mod"), f(r, "Mana_mod"), f(r, "Armor_mod"), 1, n(r, "RacialLeader"), 0,
                         n(r, "RegenHealth", 1), 0, n(r, "flags_extra") & 0x3FFFFFFF, "", 0])
            inhabit = n(r, "InhabitType", 3)
            movement.append([self.entry(e), 1 if inhabit & 1 else 0, 1 if inhabit & 2 else 0, 1 if inhabit & 4 else 0])
            for i in range(4):
                d = n(r, "modelid%d" % (i + 1))
                if d:
                    models.append((e, i, d))
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
        self.port_displays({d for _, _, d in models})
        out = []
        for e, i, d in models:
            nd = self.displays.get(d)
            if nd is None:
                dropped["creature displays nothing has (fell back to %d)" % wi.FALLBACK_DISPLAY].append(d)
                nd = wi.FALLBACK_DISPLAY
            out.append([self.entry(e), i, nd, 1, 1, 0])
        self.write("11_creature_template_model", insert(
            "creature_template_model", "CreatureID Idx CreatureDisplayID DisplayScale Probability VerifiedBuild".split(),
            out, "DELETE FROM `creature_template_model` WHERE `CreatureID` IN %s;" % ents))
        info, have = [], set()
        for r in self.db["creature_model_info"]:
            d = self.displays.get(int(r["modelid"]))
            if d and d not in self.stock_cdisp and d not in have:
                have.add(d)
                info.append([d, float(r["bounding_radius"]), float(r["combat_reach"]),
                             self.gender.get(int(r["modelid"]), int(r["gender"])), 0, 0])
        mop_of = {v: k for k, v in self.displays.items()}
        for d in sorted({row[2] for row in out} - have - self.stock_cdisp):
            info.append([d, 0.5, 1.5, self.gender.get(mop_of.get(d, d), 2), 0, 0])
        self.write("13_creature_model_info", insert(
            "creature_model_info", "DisplayID BoundingRadius CombatReach Gender DisplayID_Other_Gender VerifiedBuild".split(),
            info, "DELETE FROM `creature_model_info` WHERE `DisplayID` IN %s;" % in_list(r[0] for r in info)
            if info else None))
        equip = [[self.entry(r["entry"]), int(r["id"])] + [self.item(int(r["itemEntry%d" % k])) for k in (1, 2, 3)] + [0]
                 for r in self.db["creature_equip_template"] if int(r["entry"]) in self.ct]
        self.write("14_creature_equip_template", insert(
            "creature_equip_template", "CreatureID ID ItemID1 ItemID2 ItemID3 VerifiedBuild".split(), equip,
            "DELETE FROM `creature_equip_template` WHERE `CreatureID` IN %s;" % ents))
        addon = [[self.entry(r["entry"]), 0, int(r["mount"]) if int(r["mount"]) in self.stock_cdisp else 0,
                  int(r["bytes1"]), int(r["bytes2"]), self.emote(int(r["emote"]), "template %s" % r["entry"]), 0,
                  self.auras(r["auras"], "creature_template_addon %s" % r["entry"])]
                 for r in self.db["creature_template_addon"] if int(r["entry"]) in self.ct]
        self.write("15_creature_template_addon", insert(
            "creature_template_addon", "entry path_id mount bytes1 bytes2 emote visibilityDistanceType auras".split(),
            addon, "DELETE FROM `creature_template_addon` WHERE `entry` IN %s;" % ents))
        text = []
        for r in self.db["creature_text"]:
            e = int(r["entry"])
            if e not in self.ct:
                continue
            lang = int(r["language"]) if int(r["language"]) in self.stock_languages else 0
            text.append([self.entry(e), int(r["groupid"]), int(r["id"]), r["text"], int(r["type"]), lang,
                         float(r["probability"]), self.emote(int(r["emote"]), "text %d" % e), int(r["duration"]),
                         int(r["sound"]) if int(r["sound"]) in self.stock_sounds else 0, 0, 0, r["comment"] or ""])
        self.write("16_creature_text", insert(
            "creature_text", "CreatureID GroupID ID Text Type Language Probability Emote Duration Sound BroadcastTextId "
            "TextRange comment".split(), text, "DELETE FROM `creature_text` WHERE `CreatureID` IN %s;" % ents))
        trainers = sum(1 for r in self.ct.values() if int(r["npcflag"]) & 0x10)
        if trainers:
            dropped["trainer flag removed (MoP trainer spells come later)"].append(trainers)

    # ---- spawns -----------------------------------------------------------------------------------------------
    def spawns(self):
        c, a = [], []
        guid_of = {}
        for r in sorted(self.spawn_rows, key=lambda r: int(r["guid"])):
            e = int(r["id"])
            if e not in self.ct and e not in self.stock_creatures and e not in self.f134_entries:
                continue
            g = CREATURE_GUID + len(c)
            guid_of[int(r["guid"])] = g
            if int(r["phaseId"]):
                dropped["spawns in SkyFire phases (put in the default phase)"].append(r["phaseId"])
            c.append([g, self.entry(e), MAP, 0, 0, 1, 1, int(r["equipment_id"])] +
                     [float(r[k]) for k in ("position_x", "position_y", "position_z", "orientation")] +
                     [int(r["spawntimesecs"]), float(r["spawndist"]), 0, 0, 0, int(r["MovementType"]) & 1, 0, 0, 0, "",
                      0, 0, "[gen F-133 Pandaria]"])
        for r in self.db["creature_addon"]:
            g = guid_of.get(int(r["guid"]))
            if g:
                a.append([g, 0, int(r["mount"]) if int(r["mount"]) in self.stock_cdisp else 0, int(r["bytes1"]),
                          int(r["bytes2"]), self.emote(int(r["emote"]), "spawn %d" % g), 0,
                          self.auras(r["auras"], "creature_addon %d" % g)])
        self.write("40_creature", insert(
            "creature", "guid id map zoneId areaId spawnMask phaseMask equipment_id position_x position_y position_z "
            "orientation spawntimesecs wander_distance currentwaypoint curhealth curmana MovementType npcflag "
            "unit_flags dynamicflags ScriptName VerifiedBuild CreateObject Comment".split(), c,
            "DELETE FROM `creature` WHERE `Comment` LIKE '[gen F-133%';"))
        self.write("41_creature_addon", insert(
            "creature_addon", "guid path_id mount bytes1 bytes2 emote visibilityDistanceType auras".split(), a,
            "DELETE FROM `creature_addon` WHERE `guid` BETWEEN %d AND %d;" % (CREATURE_GUID, CREATURE_GUID + 99999)))

    # ---- vendors and gossip -----------------------------------------------------------------------------------
    def vendors(self):
        rows = []
        for r in self.db["npc_vendor"]:
            e = int(r["entry"])
            if e not in self.ct or int(r["type"]) != 1:      # type 2 = currency, which 3.3.5a lacks
                continue
            item = self.item(int(r["item"]))
            if item:
                rows.append([self.entry(e), int(r["slot"]), item, int(r["maxcount"]), int(r["incrtime"]), 0, 0])
            if int(r["ExtendedCost"]):
                dropped["vendor extended costs (sold for gold instead)"].append(r["ExtendedCost"])
        self.write("17_npc_vendor", insert(
            "npc_vendor", "entry slot item maxcount incrtime ExtendedCost VerifiedBuild".split(), rows,
            "DELETE FROM `npc_vendor` WHERE `entry` IN %s;" % in_list(self.entry(e) for e in self.ct)))

    def gossip_(self):
        menus, options, texts = [], [], {}
        for r in self.db["gossip_menu"]:
            m = self.menu.get(int(r["MenuID"]))
            if m:
                t = int(r["TextID"])
                texts.setdefault(t, wi.TEXT_BASE + len(texts))
                menus.append([m, texts[t]])
        for r in self.db["gossip_menu_option"]:
            m = self.menu.get(int(r["MenuID"]))
            if not m:
                continue
            action = self.menu.get(int(r["ActionMenuID"]), 0)
            options.append([m, int(r["OptionID"]), int(r["OptionIcon"]), r["OptionText"], 0, int(r["OptionType"]),
                            int(r["OptionNpcflag"]) & NPCFLAG_MASK, action, 0, int(r["BoxCoded"]), int(r["BoxMoney"]),
                            r["BoxText"] or "", 0, 0])
        npc = {int(r["ID"]): r for r in self.db["npc_text"]}
        out = []
        for t, new in sorted(texts.items(), key=lambda kv: kv[1]):
            r = npc.get(t)
            if not r:
                dropped["gossip texts SkyFire lacks (generic greeting)"].append(t)
                r = {"text0_0": "Greetings, $n.", "prob0": 1}
            row = [new]
            for k in range(8):
                row += [r.get("text%d_0" % k) or "", r.get("text%d_1" % k) or "", 0,
                        int(r.get("lang%d" % k) or 0) if int(r.get("lang%d" % k) or 0) in self.stock_languages else 0,
                        float(r.get("prob%d" % k) or 0)] + [int(r.get("em%d_%d" % (k, j)) or 0) for j in range(6)]
            out.append(row + [0])
        cols = ["ID"] + [c % k for k in range(8) for c in ("text%d_0", "text%d_1", "BroadcastTextID%d", "lang%d",
                                                          "Probability%d", "em%d_0", "em%d_1", "em%d_2", "em%d_3",
                                                          "em%d_4", "em%d_5")] + ["VerifiedBuild"]
        self.write("26_gossip_menu", insert("gossip_menu", "MenuID TextID".split(), menus,
                                            "DELETE FROM `gossip_menu` WHERE `MenuID` BETWEEN %d AND %d;" % (
                                                wi.MENU_BASE, wi.MENU_BASE + 9999)))
        self.write("27_gossip_menu_option", insert(
            "gossip_menu_option", "MenuID OptionID OptionIcon OptionText OptionBroadcastTextID OptionType OptionNpcFlag "
            "ActionMenuID ActionPoiID BoxCoded BoxMoney BoxText BoxBroadcastTextID VerifiedBuild".split(), options,
            "DELETE FROM `gossip_menu_option` WHERE `MenuID` BETWEEN %d AND %d;" % (wi.MENU_BASE, wi.MENU_BASE + 9999)))
        self.write("28_npc_text", insert("npc_text", cols, out, "DELETE FROM `npc_text` WHERE `ID` BETWEEN %d AND %d;" % (
            wi.TEXT_BASE, wi.TEXT_BASE + 9999)))

    # ---- quests ------------------------------------------------------------------------------------------------
    def quests_(self):
        n = lambda r, k: int(float(r[k])) if r.get(k) not in (None, "") else 0
        it = self.item
        qt, qa, offer, req, details = [], [], [], [], []
        for q, s in self.quests.items():
            row = [q, n(s, "Method"), level(s["Level"]) if n(s, "Level") > 0 else n(s, "Level"), level(s["MinLevel"]),
                   n(s, "ZoneOrSort"), n(s, "Type"), n(s, "SuggestedPlayers"), 0, 0, 0, 0, n(s, "NextQuestIdChain"),
                   n(s, "RewardXPId"), n(s, "RewardMoney"), 0,
                   self.spell_ok(n(s, "RewardSpell")) or 0, self.spell_ok(n(s, "RewardSpellCast")) or 0,
                   n(s, "RewardHonor"), 0, it(n(s, "SourceItemId")), n(s, "Flags") & 0xFFFFF, 0]
            for w in ("RewardSpell", "RewardSpellCast"):
                if n(s, w) and not self.spell_ok(n(s, w)):
                    dropped["quest reward spells nothing has"].append("%d %s %d" % (q, w, n(s, w)))
            for k in range(1, 5):
                row += [it(n(s, "RewardItemId%d" % k)), n(s, "RewardItemCount%d" % k)]
            for k in range(1, 5):
                row += [it(n(s, "RequiredSourceItemId%d" % k)), n(s, "RequiredSourceItemCount%d" % k)]
            for k in range(1, 7):
                row += [it(n(s, "RewardChoiceItemId%d" % k)), n(s, "RewardChoiceItemCount%d" % k)]
            title = n(s, "RewardTitleId")
            if title and title not in self.stock_titles:
                dropped["title rewards 3.3.5a lacks"].append("%d title %d" % (q, title))
                title = 0
            row += [n(s, "PointMapId"), float(s["PointX"]), float(s["PointY"]), n(s, "PointOption"), title,
                    n(s, "RewardTalents"), n(s, "RewardArenaPoints")]
            for k in range(1, 6):
                f = n(s, "RewardFactionId%d" % k)
                if f and f not in self.stock_factions:
                    dropped["reputation rewards of factions 3.3.5a lacks"].append(f)
                    f = 0
                row += [f, n(s, "RewardFactionValueId%d" % k) if f else 0, n(s, "RewardFactionValueIdOverride%d" % k) if f else 0]
            if n(s, "RewardCurrencyId1"):
                dropped["currency rewards (no currencies in 3.3.5a)"].append(q)
            row += [n(s, "LimitTime"), 0, 0, s["Title"] or "", s["Objectives"] or "", s["Details"] or "",
                    s["EndText"] or "", s["CompletedText"] or ""]
            npc, items, texts = [], [], []
            for o in self.objectives[q]:
                t, obj, amount = int(o["type"]), int(o["objectId"]), int(o["amount"])
                if t in (0, 3):                                 # kill / talk to
                    npc.append((self.entry(obj), amount))
                    texts.append(o["description"] or "")
                elif t == 2:
                    npc.append((-obj, amount))
                    texts.append(o["description"] or "")
                elif t == 1:
                    items.append((it(obj), amount))
                else:
                    dropped["quest objective types 3.3.5a lacks (currency, spell, reputation, pet battle, ...)"].append(
                        "%d type %d" % (q, t))
            if len(npc) > 4 or len(items) > 6:
                dropped["quests with more objectives than 3.3.5a holds"].append(q)
            npc, items, texts = (npc + [(0, 0)] * 4)[:4], (items + [(0, 0)] * 6)[:6], (texts + [""] * 4)[:4]
            for e, c in npc + items:
                row += [e, c]
            qt.append(row + [0] + texts + [0])
            classes = n(s, "RequiredClasses")
            src = n(s, "SourceSpellId")
            if src and not self.spell_ok(src):
                dropped["quest accept spells nothing has"].append("%d %d" % (q, src))
            rep = [n(s, k) for k in ("RequiredMinRepFaction", "RequiredMaxRepFaction")]
            rep = [f if f in self.stock_factions else 0 for f in rep]
            qa.append([q, level(s["MaxLevel"]) if n(s, "MaxLevel") else 0,
                       classes & wi.CLASS_MASK if classes & wi.CLASS_MASK else classes, self.spell_ok(src) or 0,
                       n(s, "PrevQuestId"), n(s, "NextQuestId"), n(s, "ExclusiveGroup"), 0, n(s, "RewardMailTemplateId"),
                       n(s, "RewardMailDelay"), n(s, "RequiredSkillId"), n(s, "RequiredSkillPoints"), rep[0], rep[1],
                       n(s, "RequiredMinRepValue") if rep[0] else 0, n(s, "RequiredMaxRepValue") if rep[1] else 0,
                       1 if n(s, "SourceItemId") else 0, n(s, "SpecialFlags") & 0xF])
            em = lambda k: self.emote(n(s, k), "quest %d" % q)
            if s["OfferRewardText"]:
                offer.append([q] + [em("OfferRewardEmote%d" % k) for k in range(1, 5)] +
                             [n(s, "OfferRewardEmoteDelay%d" % k) for k in range(1, 5)] + [s["OfferRewardText"], 0])
            if s["RequestItemsText"]:
                req.append([q, em("EmoteOnComplete"), em("EmoteOnIncomplete"), s["RequestItemsText"], 0])
            details.append([q] + [em("DetailsEmote%d" % k) for k in range(1, 5)] +
                           [n(s, "DetailsEmoteDelay%d" % k) for k in range(1, 5)] + [0])
        cols = ("ID QuestType QuestLevel MinLevel QuestSortID QuestInfoID SuggestedGroupNum RequiredFactionId1 "
                "RequiredFactionId2 RequiredFactionValue1 RequiredFactionValue2 RewardNextQuest RewardXPDifficulty "
                "RewardMoney RewardMoneyDifficulty RewardDisplaySpell RewardSpell RewardHonor RewardKillHonor StartItem "
                "Flags RequiredPlayerKills").split()
        cols += sum((["RewardItem%d" % k, "RewardAmount%d" % k] for k in range(1, 5)), [])
        cols += sum((["ItemDrop%d" % k, "ItemDropQuantity%d" % k] for k in range(1, 5)), [])
        cols += sum((["RewardChoiceItemID%d" % k, "RewardChoiceItemQuantity%d" % k] for k in range(1, 7)), [])
        cols += "POIContinent POIx POIy POIPriority RewardTitle RewardTalents RewardArenaPoints".split()
        cols += sum((["RewardFactionID%d" % k, "RewardFactionValue%d" % k, "RewardFactionOverride%d" % k]
                     for k in range(1, 6)), [])
        cols += ("TimeAllowed AllowableRaces AllowableRaces_2 LogTitle LogDescription QuestDescription AreaDescription "
                 "QuestCompletionLog").split()
        cols += sum((["RequiredNpcOrGo%d" % k, "RequiredNpcOrGoCount%d" % k] for k in range(1, 5)), [])
        cols += sum((["RequiredItemId%d" % k, "RequiredItemCount%d" % k] for k in range(1, 7)), [])
        cols += ["Unknown0"] + ["ObjectiveText%d" % k for k in range(1, 5)] + ["VerifiedBuild"]
        qs = in_list(self.quests)
        self.write("30_quest_template", insert("quest_template", cols, qt,
                                               "DELETE FROM `quest_template` WHERE `ID` IN %s;" % qs))
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
        # 910 is MoP 5.1's phased Krasarang (Krasarang_terrain1), drawn here as the one Krasarang map
        wma = lambda w: {910: 857}.get(w, w)
        poi = [[int(r["questId"]), int(r["id"]), int(r["objIndex"]), int(r["mapid"]), wma(int(r["WorldMapAreaId"])),
                int(r["FloorId"]), int(r["unk3"]), int(r["unk4"]), 0]
               for r in self.db["quest_poi"] if int(r["questId"]) in self.quests]
        pts = [[int(r["questId"]), int(r["id"]), int(r["idx"]), int(r["x"]), int(r["y"]), 0]
               for r in self.db["quest_poi_points"] if int(r["questId"]) in self.quests]
        self.write("35_quest_poi", insert("quest_poi", "QuestID id ObjectiveIndex MapID WorldMapAreaId Floor Priority "
                                          "Flags VerifiedBuild".split(), poi,
                                          "DELETE FROM `quest_poi` WHERE `QuestID` IN %s;" % qs))
        self.write("36_quest_poi_points", insert("quest_poi_points", "QuestID Idx1 Idx2 X Y VerifiedBuild".split(), pts,
                                                 "DELETE FROM `quest_poi_points` WHERE `QuestID` IN %s;" % qs))
        spawned = {int(r["id"]) for r in self.spawn_rows}
        for k, (t, ids, ent) in enumerate((("creature_queststarter", spawned, self.entry),
                                           ("creature_questender", spawned, self.entry),
                                           ("gameobject_queststarter", set(self.got), int),
                                           ("gameobject_questender", set(self.got), int))):
            rel = sorted({(ent(r["id"]), int(r["quest"])) for r in self.db[t]
                          if int(r["quest"]) in self.quests and int(r["id"]) in ids})
            self.write("%d_%s" % (45 + k, t), insert(t, ["id", "quest"], rel,
                                                     "DELETE FROM `%s` WHERE `quest` IN %s;" % (t, qs)))

    # ---- quest objects and loot ---------------------------------------------------------------------------------
    def gameobjects_(self):
        gd = c406.Dbc(os.path.join(wi.MOP_DBC, "GameObjectDisplayInfo.dbc"))
        stock_gdisp, stock_locks = wi.dbc_ids("GameObjectDisplayInfo"), wi.dbc_ids("Lock")
        tmpl, addon, disp = [], [], []
        for e, r in self.got.items():
            d, t = int(r["displayId"]), int(r["type"])
            if d and d not in stock_gdisp and d not in {x["id"] for x in disp}:
                x = gd.get(d)
                if x:
                    disp.append(dict(id=d, model_name=gd.s(x[1]), **{"sound_%d" % (i + 1): x[2 + i] if x[2 + i] in
                                     self.stock_sounds else 0 for i in range(10)},
                                     **dict(zip(("geo_box_min_x", "geo_box_min_y", "geo_box_min_z", "geo_box_max_x",
                                                 "geo_box_max_y", "geo_box_max_z"), (c406.f32(v) for v in x[12:18])))))
                    self.go_models.add(gd.s(x[1]))
                else:
                    dropped["object displays nothing has"].append(d)
            if t > 35:
                dropped["object types 3.3.5a lacks"].append("%d type %d" % (e, t))
                continue
            data = [int(float(r["data%d" % i])) for i in range(24)]
            if t in (3, 10, 2) and data[0] and data[0] not in stock_locks:   # chest / goober / questgiver lock
                dropped["object locks 3.3.5a lacks (opened freely)"].append("%d lock %d" % (e, data[0]))
                data[0] = 0
            if t == 3:
                data[1] = e if int(r["data1"]) in self.go_loot else 0
                data[17:] = [0] * 7                 # MoP-only chest fields
            if t == 10 and data[10] and not self.spell_ok(data[10]):
                dropped["object spells nothing has"].append("%d spell %d" % (e, data[10]))
                data[10] = 0
            if r.get("ScriptName"):
                dropped["object script names (not ported yet)"].append("%d %s" % (e, r["ScriptName"]))
            tmpl.append([e, t, d, r["name"], r["IconName"] or "", r["castBarCaption"] or "", r["unk1"] or "",
                         float(r["size"])] + data + ["", "", 0])
            if int(r["faction"]) or int(r["flags"]):
                addon.append([e, self.faction(int(r["faction"])) if int(r["faction"]) else 0, int(r["flags"])])
        ents = in_list(self.got)
        cols = ("entry type displayId name IconName castBarCaption unk1 size " + " ".join("Data%d" % i for i in range(24))
                + " AIName ScriptName VerifiedBuild").split()
        self.write("20_gameobject_template", insert("gameobject_template", cols, tmpl,
                                                    "DELETE FROM `gameobject_template` WHERE `entry` IN %s;" % ents))
        self.write("21_gameobject_template_addon", insert(
            "gameobject_template_addon", "entry faction flags".split(), addon,
            "DELETE FROM `gameobject_template_addon` WHERE `entry` IN %s;" % ents))
        qi = [[e, k, self.item(int(r["questItem%d" % (k + 1)])), 0] for e, r in self.got.items() for k in range(6)
              if int(r["questItem%d" % (k + 1)]) and self.item(int(r["questItem%d" % (k + 1)]))]
        self.write("22_gameobject_questitem", insert(
            "gameobject_questitem", "GameObjectEntry Idx ItemId VerifiedBuild".split(), qi,
            "DELETE FROM `gameobject_questitem` WHERE `GameObjectEntry` IN %s;" % ents))
        self.write_dbc("gameobjectdisplayinfo", disp, "MoP object displays (5.4.8) of Pandaria's quest objects")
        sp = [[GAMEOBJECT_GUID + i, int(r["id"]), MAP, 0, 0, 1, 1] +
              [float(r[k]) for k in ("position_x", "position_y", "position_z", "orientation", "rotation0", "rotation1",
                                     "rotation2", "rotation3")] +
              [int(r["spawntimesecs"]), int(r["animprogress"]), int(r["state"]), "", 0, "[gen F-133 Pandaria]"]
              for i, r in enumerate(self.go_spawns)]
        self.write("42_gameobject", insert(
            "gameobject", "guid id map zoneId areaId spawnMask phaseMask position_x position_y position_z orientation "
            "rotation0 rotation1 rotation2 rotation3 spawntimesecs animprogress state ScriptName VerifiedBuild "
            "Comment".split(), sp, "DELETE FROM `gameobject` WHERE `guid` BETWEEN %d AND %d;" % (
                GAMEOBJECT_GUID, GAMEOBJECT_GUID + 99999)))

    def plan_loot(self):
        """Loot per ported creature (self.loot_rows / skin_rows / gold, keyed by SkyFire entry): SkyFire's own where
        it has some (157 creatures), else generated from the zone's pools (mop_loot.py); gold by level where SkyFire
        has none; skins for beasts and dragonkin."""
        def rows(src):
            out = []
            for r in src:
                item = self.item(int(r["item"]))
                if item:
                    c = float(r["ChanceOrQuestChance"])
                    out.append([item, 0, abs(c), 1 if c < 0 else 0, int(r["lootmode"]), int(r["groupid"]),
                                int(r["mincountOrRef"]), int(r["maxcount"]), ""])
            return out
        templates = {int(r["entry"]): r for r in self.db["creature_template"]}
        skins = collections.defaultdict(list)
        for r in self.db["skinning_loot_template"]:
            if int(r["mincountOrRef"]) > 0:
                skins[int(r["entry"])].append(r)
        self.fill = LootFill(LOOT_REF_BASE, self.items, cloth=WINDWOOL_CLOTH, skins=PANDARIA_SKINS)
        for e in {int(r["id"]) for r in self.spawn_rows}:
            t = templates.get(e)
            for r in self.creature_loot.get(int(t["lootid"] or 0), []) if t else []:
                if float(r["ChanceOrQuestChance"]) > 0:
                    self.fill.learn(int(t["type"]), int(t["family"]), int(r["item"]))
        self.loot_rows, self.skin_rows, self.gold = {}, {}, {}
        generated = 0
        for e, r in self.ct.items():
            ctype, rank = int(r["type"]), int(r["npc_rank"])
            ok = killable(ctype, int(r["unit_flags"]), int(r["npcflag"]), int(r["flags_extra"]))
            lid, sid = int(r["lootid"] or 0), int(r["skinloot"] or 0)
            if lid in self.creature_loot:
                self.loot_rows[e] = rows(self.creature_loot[lid])
            elif ok:
                self.loot_rows[e] = self.fill.creature(ctype, int(r["family"]), rank)
                generated += 1
            if sid in skins:
                self.skin_rows[e] = rows(skins[sid])
            elif ok:
                self.skin_rows[e] = self.fill.skinning(ctype)
            if ok and not int(r["maxgold"]):
                self.gold[e] = gold(level(r["maxlevel"]), rank)
        self.generated_loot = generated

    def loot_(self):
        def rows(src, key):
            out = []
            for r in src:
                item = self.item(int(r["item"]))
                if item:
                    c = float(r["ChanceOrQuestChance"])
                    out.append([key, item, 0, abs(c), 1 if c < 0 else 0, int(r["lootmode"]), int(r["groupid"]),
                                int(r["mincountOrRef"]), int(r["maxcount"]), ""])
            return out
        cl = [[self.entry(e)] + row for e, v in self.loot_rows.items() for row in v]
        sl = [[self.entry(e)] + row for e, v in self.skin_rows.items() for row in v]
        ref, used = self.fill.references()
        ref = [[r[0], self.item(r[1])] + r[2:] for r in ref]
        ref = [r for r in ref if r[1]]
        gl = []
        for e, r in self.got.items():
            if r["type"] == "3" and int(r["data1"]) in self.go_loot:
                gl += rows(self.go_loot[int(r["data1"])], e)
        cols = "Entry Item Reference Chance QuestRequired LootMode GroupId MinCount MaxCount Comment".split()
        for name, table, data in (("50", "creature_loot_template", cl), ("51", "gameobject_loot_template", gl),
                                  ("52", "skinning_loot_template", sl), ("53", "reference_loot_template", ref)):
            self.write("%s_%s" % (name, table), insert(
                table, cols, data, "DELETE FROM `%s` WHERE `Entry` IN %s;" % (table, in_list({r[0] for r in data}))
                if data else None))

    def enchantments(self):
        """item_enchantment_template groups of the random-suffix items (mop_items.py's suffix_group)."""
        rows = getattr(self.items, "suffix_rows", [])
        self.write("06_item_enchantment_template", insert(
            "item_enchantment_template", "entry ench chance".split(), rows,
            "DELETE FROM `item_enchantment_template` WHERE `entry` IN %s;" % in_list({r[0] for r in rows})
            if rows else None, "random suffixes of the MoP items (SkyFire's groups, stock suffixes only)"))

    def run(self):
        self.stock_titles = wi.dbc_ids("CharTitles")
        self.plan_loot()
        self.creatures()
        self.spawns()
        self.vendors()
        self.gossip_()
        self.quests_()
        self.gameobjects_()
        self.loot_()
        self.client_rows()
        self.enchantments()
        self.write_vehicles()
        self.write_npc_sounds()
        for old in glob.glob(os.path.join(self.dest, wi.SQL_DIR, wi.SQL_PREFIX + "*.sql")) + \
                glob.glob(os.path.join(self.dest, "dbc", wi.DBC_PREFIX + "*.sql")):
            os.remove(old)
        head = "-- Generated by tools/races/mop_pandaria_port.py from SkyFire 5.4.8's world database: change the script, not this file.\n\n"
        for name, sql in self.files.items():
            path = os.path.join(self.dest, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf8", newline="\n") as fh:
                fh.write(head + sql)
        cm = c406.Dbc(os.path.join(wi.MOP_DBC, "CreatureModelData.dbc"))
        assets = os.path.join(self.dest, "wi_assets.txt")
        old = set(open(assets, encoding="utf8").read().split("\n")) - {""} if os.path.exists(assets) else set()
        new = {cm.s(cm.get(m)[2]) for m in self.models} | self.go_models | {"Textures\\BakedNpcTextures\\" + b for b in self.bakes if b}
        with open(assets, "w", encoding="utf8", newline="\n") as fh:
            fh.write("\n".join(sorted(old | new)) + "\n")
        print("ported: %d creatures (%d moved), %d spawns, %d displays, %d models, %d bakes, %d items, %d menus" % (
            len(self.ct), len(self.entry_map), len(self.spawn_rows),
            sum(1 for d, v in self.displays.items() if d not in self.stock_cdisp), len(self.models), len(self.bakes),
            sum(1 for v in self.item_ids.values() if v), len(self.menu)))
        print("quests: %d, quest objects: %d (%d spawns), chests with quest loot: %d" % (
            len(self.quests), len(self.got), len(self.go_spawns), len(self.go_loot)))
        print("loot: %d creatures (%d generated), %d skinnable, %d given gold; pools: %s; %d suffix groups" % (
            sum(1 for v in self.loot_rows.values() if v), self.generated_loot, sum(1 for v in self.skin_rows.values() if v),
            len(self.gold), {k if isinstance(k, str) else "goods": len(p) for k, (r, p) in self.fill.refs.items()},
            len(getattr(self.items, "suffix_map", {}))))
        for k, v in sorted(dropped.items()):
            v = sorted(set(map(str, v)))
            print("%s (%d): %s" % (k, len(v), ", ".join(v[:20]) + (" ..." if len(v) > 20 else "")))


def wi_entries(f134):
    """Creature entries F-134's SQL defines."""
    import re
    out = set()
    for p in glob.glob(os.path.join(f134, "sql", "db-world", "base", "*creature_template.sql")):
        m = re.search(r"DELETE FROM `creature_template` WHERE `entry` IN \(([^)]*)\)", open(p, encoding="utf8").read())
        if m:
            out |= {int(x) for x in m.group(1).split(",")}
    return out


def wi_ids(f134, table, col):
    """Ids F-134's SQL deletes from `table` (its insert() files start with DELETE ... WHERE `col` IN (...))."""
    import re
    out = set()
    for p in glob.glob(os.path.join(f134, "sql", "db-world", "base", "*_%s.sql" % table)):
        m = re.search(r"DELETE FROM `%s` WHERE `%s` IN \(([^)]*)\)" % (table, col), open(p, encoding="utf8").read())
        if m:
            out |= {int(x) for x in m.group(1).split(",")}
    return out


def rel_ids(rows, quests):
    return {int(r["id"]) for r in rows if int(r["quest"]) in quests}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("sfdb")
    p.add_argument("--modpak", default=os.path.join(wi.MODPAKS, "F-133_mop-pandaria"))
    p.add_argument("--data", default="D:/wow-scratch/wi/db2")
    a = p.parse_args()
    PandariaPort(a.sfdb, a.modpak, a.data).run()


if __name__ == "__main__":
    main()

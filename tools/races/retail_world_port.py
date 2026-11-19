#!/usr/bin/env python3
"""Port a retail map's spawns and quests (Exile's Reach, F-137) from TrinityCore's retail TDB to AzerothCore.

  python -I -X utf8 retail_world_port.py TDB_WORLD_SQL CSV_DIR MODPAK [--map 2175] [--zone 10424] [--tag F-137]
                                         [--world-map-area 1409] [--cache PICKLE]

TDB_WORLD_SQL is TrinityCore's TDB_full_world_*.sql (1210.26091 for F-137); --cache keeps the tables it reads in a
pickle, so later runs skip the 600 MB parse (delete it after changing TABLES). CSV_DIR holds wago.tools' exports of
the retail build the map's art comes from (12.1.5.70961): CreatureDisplayInfo, CreatureDisplayInfoExtra,
CreatureModelData, GameObjectDisplayInfo, FactionTemplate, Item, ItemSparse, ItemModifiedAppearance, ItemAppearance,
AreaTrigger; file ids are named through the community listfile at LISTFILE. Writes
MODPAK/sql/db-world/base/zz_[AUTO,TAG]_world_*.sql, MODPAK/dbc/[TAG]_world_*.sql and MODPAK/wi_assets.txt (the models
and icons tools/models/mop_assets.py fetches and converts). Rerun after changing it; it replaces only its own files.

Spawns:
- every creature and object spawn on --map. Retail's phases become object visibility conditions (conditions source
  type 30, SourceId = the spawn's guid) carrying the phase's own conditions (quest states, team, auras): the island
  has more phases than a phasemask has bits. The core rechecks them on quest changes (F-137's core patch).
  Trigger creatures (flags_extra 0x80, the scripts' helpers) and object types 3.3.5a lacks are left out
- levels: retail scales them (ContentTuning), so a creature gets the level band of the areas it spawns in, along
  the island's quest route (AREA_LEVELS); critters level 1
- displays: stock ids are kept (the stock model, not retail's newer one); the rest are retail's rows with their
  models and textures (all in the model's folder), the model rows numbered from MODEL_BASE (retail's model ids mean
  other models than stock's or MoP's), displays another modpak uses moved to DISPLAY_BASE and up. Dressed NPCs
  (CreatureDisplayInfoExtra: HD bakes on retail race models) get a stock display of their race and sex for now
- factions 3.3.5a lacks: retail's hostile ones (enemy group has players) become 14, the rest 35
- scripts (ScriptName, SmartAI) are dropped: enemies only melee, and the scripted quest steps need SmartAI (plan.md)
- equipment: retail item ids, none in 3.3.5a: left out

Quests (QuestSortID --zone, both factions' chains, class versions, the dungeon's):
- the Alliance and Horde chains share races (retail starts them from the faction's ship), so each quest gets a team
  condition (conditions source type 19) on top of retail's own; HORDE_QUESTS lists the Horde ones
- objectives: kill / talk (0, 3) and object (2) -> RequiredNpcOrGo, items (1) -> RequiredItem, area triggers (19) ->
  AreaTrigger.dbc rows, areatrigger_involvedrelation and the exploration flag. Criteria trees (14) have no 3.3.5a
  counterpart and are dropped (listed)
- class masks keep the 3.3.5a classes (CLASS_MASK); quests only for Monk, Demon Hunter or Evoker are left out
- QuestLevel -1 (the player's level), MinLevel 1; RewardMoney 0 (retail's comes from a table by level); gear comes
  from retail's quest packages (QuestPackageID), not ported yet
- quest items: retail's rows (names, stacks, bonding) with icon-only displays (ITEM_DISPLAY_BASE and up), Item.dbc rows
- objects the quests use keep their type (chests, goobers with the quest in data1, quest givers); the rest are props
"""
import argparse, collections, csv, os, pickle, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cata_items import sql_value, ITEM_TEMPLATE_COLUMNS  # noqa: E402
from cata_gilneas_port import insert, in_list, go_rotation  # noqa: E402
from mop_wandering_isle_port import dbc_ids, taken, base_ids, config_range, pet_family, STOCK_DBC  # noqa: E402
import cata406_dbc_port as c406  # noqa: E402
import mop_wandering_isle_port as wi  # noqa: E402

LISTFILE = "D:/wow-scratch/listfile/community-listfile.csv"
TABLES = ("creature", "gameobject", "creature_template", "creature_template_model", "creature_template_addon",
          "creature_addon", "creature_model_info", "creature_template_difficulty", "gameobject_template",
          "gameobject_addon", "gameobject_template_addon", "waypoint_path", "waypoint_path_node", "quest_template",
          "quest_template_addon", "quest_objectives", "quest_offer_reward", "quest_request_items", "quest_details",
          "creature_queststarter", "creature_questender", "gameobject_queststarter", "gameobject_questender",
          "conditions", "phase_area", "creature_loot_template", "gameobject_loot_template", "gameobject_questitem",
          "quest_poi", "quest_poi_points")
CREATURE_GUID = GAMEOBJECT_GUID = 13700001
PATH_BASE = 13700000
MODEL_BASE = 1370000
DISPLAY_BASE = 1370000
GO_DISPLAY_BASE = 137000
ITEM_DISPLAY_BASE = 1370000
TRIGGER = 0x80
# Exile's Reach's quest route (retail 1-10): beach and Murloc Hideaway, the camp, Darkmaul Plains, the Briarpatch,
# the Ogre Ruins, Harpy Roost, Hrun's Barrow, Killclaw's Lair, the bridge and Darkmaul Citadel
AREA_LEVELS = {10424: (1, 2), 10453: (1, 2), 10452: (2, 2), 12851: (2, 3), 10588: (2, 4), 10503: (3, 5),
               10529: (5, 7), 10528: (6, 8), 10527: (7, 9), 11011: (8, 10), 10568: (8, 9), 10530: (9, 10)}
FACTIONS = {2753: 18}            # retail's island murlocs -> stock Murloc
FAMILIES = {151: 5}              # stag -> boar (F-128's choice), on top of F-134's map
CLASSIFICATION = {5: 0, 6: 0}    # trivial / minus mobs are normal in 3.3.5a
FALLBACK_DISPLAYS = {92803: 17578}   # Hrun the Exiled: a dressed skeleton -> stock skeleton
# retail race -> the stock race whose look a dressed NPC borrows (allied races, Pandaren, Worgen ...)
STOCK_RACE = {22: 1, 24: 1, 25: 1, 26: 1, 27: 4, 28: 6, 29: 10, 30: 11, 31: 8, 32: 1, 34: 3, 35: 9, 36: 2, 37: 7}
CLASS_MASK = 0x5FF               # 3.3.5a's classes; Monk (512) is F-100's Hero here, DH and Evoker don't exist
ALLIANCE, HORDE = 469, 67
HORDE_QUESTS = set(range(59926, 60175)) - {60168} | {85679}
NEUTRAL_QUESTS = {66349}         # Training Rock: both factions
EXPLORATION = 0x2                # quest_template_addon.SpecialFlags
CONDITION_TYPES = {1, 2, 6, 8, 9, 14, 15, 28, 47}   # copied as they are (15: class masks match); 48 is remapped
# exploration triggers retail's AreaTrigger table lacks: TrinityCore spawns them itself (its `areatrigger` row and
# create properties); 3.3.5a's trigger is a sphere: (map, x, y, z, radius)
SERVER_TRIGGERS = {17635: (2175, -245.41, -2492.09, 18.3213, 40.0)}   # Finding the Lost Expedition: a 40-yard cylinder
GO_TYPES = {2, 3, 5, 10}
# TrinityCore's TDB names the givers of only 30 of the island's quests. The rest are inferred (infer_givers): the
# ender is the faction's quest giver standing within GIVER_RANGE of retail's turn-in marker (quest_poi objective -1),
# the starter the ender of the quest before it in the faction's quest lines (QuestLineXQuest; class quests follow
# the last quest for everyone), which also becomes its PrevQuestID
GIVER_RANGE = 25.0
QUEST_LINES = {ALLIANCE: (5366, 5367), HORDE: (5369, 5370)}
TEAM_NAMES = {ALLIANCE: {"Captain Garrick", "Henry Garrick", "Kee-La", "Bjorn Stouthands", "Alaria", "Austin Huxworth",
                         "Lindie Springstock", "Meredy Huntswell", "Quartermaster Richter", "Private Cole",
                         "Lady Jaina Proudmoore", "Ralia Dreamchaser"},
              HORDE: {"Warlord Breka Grimaxe", "Breka Grimaxe", "Shuja Grimaxe", "Bo", "Won'sa", "Mithdran Dawntracker",
                      "Cork Fizzlepop", "Lana Jordan", "Provisioner Jin'hake", "Provisoner Jin'hake", "Grunt Throg",
                      "Thrall", "Herbert Gloomburst"}}
B = "\\"


def tdb_tables(path, cache):
    """{table: [dict]} of TABLES from a TDB full world dump (values as strings, NULL as None)."""
    if cache and os.path.exists(cache):
        return pickle.load(open(cache, "rb"))
    tup = re.compile(r"\(((?:[^()']|'(?:[^'\\]|\\.)*')*)\)")
    val = re.compile(r"'((?:[^'\\]|\\.)*)'|(NULL)|([^,]+)")
    unescape = lambda s: re.sub(r"\\(.)", lambda e: {"n": "\n", "r": "\r", "t": "\t", "0": "\0"}.get(e.group(1), e.group(1)), s)
    cols, cur, out = {}, None, collections.defaultdict(list)
    for line in open(path, encoding="utf8", errors="replace"):
        m = re.match(r"CREATE TABLE `(\w+)`", line)
        if m:
            cur = m.group(1)
            cols[cur] = []
            continue
        if cur:
            if line.startswith("  `"):
                cols[cur].append(line.split("`")[1])
            elif line.startswith(")"):
                cur = None
            continue
        m = re.match(r"INSERT INTO `(\w+)` VALUES", line)
        if not m or m.group(1) not in TABLES:
            continue
        for t in tup.finditer(line, m.end()):
            vals = [unescape(v.group(1)) if v.group(1) is not None else None if v.group(2) else v.group(3).strip()
                    for v in val.finditer(t.group(1))]
            out[m.group(1)].append(dict(zip(cols[m.group(1)], vals)))
    out = dict(out)
    if cache:
        pickle.dump(out, open(cache, "wb"))
    return out


def n(v, default=0):
    """A dump value as a number."""
    if v is None or v == "":
        return default
    if not isinstance(v, str):
        return v
    f = float(v)
    return int(f) if f.is_integer() and "." not in v and "e" not in v.lower() else f


def table(csv_dir, name, key="ID"):
    csv.field_size_limit(1 << 24)
    with open(os.path.join(csv_dir, name + ".csv"), encoding="utf-8", newline="") as fh:
        return {r[key]: r for r in csv.DictReader(fh)}


class Port:
    def __init__(self, a):
        self.a, self.files, self.dropped = a, {}, collections.defaultdict(list)
        t = self.t = tdb_tables(a.tdb, a.cache)
        self.ct = {n(r["entry"]): r for r in t["creature_template"]}
        self.got = {n(r["entry"]): r for r in t["gameobject_template"]}
        self.spawns, self.gspawns = [], []
        for r in t["creature"]:
            if n(r["map"]) != a.map:
                continue
            e = n(r["id"])
            if e not in self.ct:
                self.dropped["spawns of creatures the TDB doesn't define"].append(e)
            elif n(self.ct[e]["flags_extra"]) & TRIGGER:
                self.dropped["trigger creatures (scripts' helpers)"].append(e)
            else:
                self.spawns.append(r)
        for r in t["gameobject"]:
            if n(r["map"]) != a.map:
                continue
            g = self.got.get(n(r["id"]))
            if not g or n(g["type"]) not in GO_TYPES:
                self.dropped["object spawns of types 3.3.5a lacks"].append("%s type %s" % (r["id"], g and g["type"]))
            else:
                self.gspawns.append(r)
        self.spawns.sort(key=lambda r: n(r["guid"]))
        self.gspawns.sort(key=lambda r: n(r["guid"]))
        self.cguid = {r["guid"]: CREATURE_GUID + i for i, r in enumerate(self.spawns)}
        self.gguid = {r["guid"]: GAMEOBJECT_GUID + i for i, r in enumerate(self.gspawns)}
        self.stock_creatures = base_ids("creature_template")
        self.stock_gos = base_ids("gameobject_template")
        self.stock_items = base_ids("item_template")
        self.entries = sorted({n(r["id"]) for r in self.spawns} - self.stock_creatures)
        self.goentries = sorted({n(r["id"]) for r in self.gspawns} - self.stock_gos)
        clash = (set(self.entries) & (config_range("NextCreatureID") | taken("creature_template", "entry"))) | \
            (set(self.goentries) & taken("gameobject_template", "entry"))
        if clash:
            sys.exit("entries another modpak uses: %s" % sorted(clash))
        self.stock_cdisp, self.stock_gdisp = dbc_ids("CreatureDisplayInfo"), dbc_ids("GameObjectDisplayInfo")
        self.stock_sounds, self.stock_ft = dbc_ids("CreatureSoundData"), dbc_ids("FactionTemplate")
        self.stock_families, self.stock_spells = dbc_ids("CreatureFamily"), dbc_ids("Spell")
        self.stock_emotes, self.stock_locks = dbc_ids("Emotes"), dbc_ids("Lock")
        self.stock_factions, self.stock_qinfo = dbc_ids("Faction"), dbc_ids("QuestInfo")
        self.cdi, self.cmd = table(a.csv_dir, "CreatureDisplayInfo"), table(a.csv_dir, "CreatureModelData")
        self.cdx = table(a.csv_dir, "CreatureDisplayInfoExtra")
        self.gdi, self.rft = table(a.csv_dir, "GameObjectDisplayInfo"), table(a.csv_dir, "FactionTemplate")
        self.assets = set()
        self.conditions = []
        self.select_quests()

    # ---- writing --------------------------------------------------------------------------------------------------
    def write(self, name, sql):
        if sql:
            self.files[os.path.join("sql", "db-world", "base", "zz_[AUTO,%s]_world_%s.sql" % (self.a.tag, name))] = \
                "-- Generated by tools/races/retail_world_port.py: change the script, not this file.\n\n" + sql

    def write_dbc(self, name, data, comment):
        out = ["-- %s. Generated by tools/races/retail_world_port.py.\n" % comment]
        for r in data:
            out.append("DELETE FROM `%s` WHERE `id` = %s;\nINSERT INTO `%s` SET\n%s;\n" % (
                name, r["id"], name, ",\n".join("  `%s` = %s" % (k, sql_value(v)) for k, v in r.items())))
        if data:
            self.files[os.path.join("dbc", "[%s]_world_%s.sql" % (self.a.tag, name))] = "\n".join(out)

    def paths(self, ids):
        want, out = {str(i) for i in ids}, {}
        for line in open(LISTFILE, encoding="utf8", errors="replace"):
            f, _, p = line.strip().partition(";")
            if f in want:
                out[f] = p
        return out

    # ---- quests: which, and their items ---------------------------------------------------------------------------
    def select_quests(self):
        addon = {n(r["ID"]): r for r in self.t["quest_template_addon"]}
        self.qaddon = addon
        self.quests = {}
        for r in self.t["quest_template"]:
            q = n(r["ID"])
            if n(r["QuestSortID"]) != self.a.zone:
                continue
            classes = n(addon.get(q, {}).get("AllowableClasses"))
            if classes and not classes & CLASS_MASK:
                self.dropped["quests only for classes 3.3.5a lacks (Monk, Demon Hunter, Evoker)"].append(q)
                continue
            self.quests[q] = r
        self.objectives = collections.defaultdict(list)
        for o in sorted(self.t["quest_objectives"], key=lambda o: (n(o["QuestID"]), n(o["StorageIndex"]), n(o["Order"]))):
            if n(o["QuestID"]) in self.quests:
                self.objectives[n(o["QuestID"])].append(o)
        # quest items: objectives, start items, drops, rewards
        items = set()
        for q, r in self.quests.items():
            items |= {n(r[k]) for k in ["StartItem"] + ["RewardItem%d" % i for i in range(1, 5)]
                      + ["ItemDrop%d" % i for i in range(1, 5)] + ["RewardChoiceItemID%d" % i for i in range(1, 7)]}
            items |= {n(o["ObjectID"]) for o in self.objectives[q] if n(o["Type"]) == 1}
        self.wanted_items = items - {0}

    def port_items(self):
        """retail item -> item here; writes item_template, Item.dbc and icon-only ItemDisplayInfo rows."""
        csvd = self.a.csv_dir
        sparse, item = table(csvd, "ItemSparse"), table(csvd, "Item")
        app = table(csvd, "ItemAppearance")
        ima = {}
        for r in table(csvd, "ItemModifiedAppearance").values():
            ima.setdefault(r["ItemID"], r)
        taken_items = taken("item_template", "entry")
        self.item_map = {i: i for i in self.wanted_items if i in self.stock_items}
        new = sorted(i for i in self.wanted_items if i not in self.stock_items)
        icons = {}
        for i in new:
            f = item.get(str(i), {}).get("IconFileDataID", "0")
            if f in ("0", "") and str(i) in ima:
                f = app.get(ima[str(i)]["ItemAppearanceID"], {}).get("DefaultIconFileDataID", "0")
            icons[i] = f
        names = self.paths(icons.values())
        tmpl, dbc, disp = [], [], []
        for k, i in enumerate(new):
            s, it = sparse.get(str(i)), item.get(str(i))
            if not s or not it:
                self.dropped["items retail's tables don't have"].append(i)
                continue
            if i in taken_items:
                sys.exit("item %d is another modpak's" % i)
            icon = names.get(icons[i], "").rsplit("/", 1)[-1].rsplit(".", 1)[0]
            if icon:
                self.assets.add("Interface\\Icons\\%s.blp" % icon)
            d = ITEM_DISPLAY_BASE + k
            disp.append(dict(id=d, left_model="", right_model="", left_model_texture="", right_model_texture="",
                             icon_1=icon, icon_2="", geoset_group_1=0, geoset_group_2=0, geoset_group_3=0, flags=0,
                             spell_visual_id=0, group_sound_index=0, helmet_geoset_male=0, helmet_geoset_female=0,
                             upper_arm_texture="", lower_arm_texture="", hands_texture="", upper_torso_texture="",
                             lower_torso_texture="", upper_leg_texture="", lower_leg_texture="", foot_texture="",
                             item_visual=0, particle_colour_id=0))
            cls, sub, inv = n(it["ClassID"]), n(it["SubclassID"]), n(it["InventoryType"])
            row = dict.fromkeys(ITEM_TEMPLATE_COLUMNS, 0)
            row.update(entry=i, **{"class": cls}, subclass=sub, SoundOverrideSubclass=-1, name=s["Display_lang"],
                       displayid=d, Quality=n(s["OverallQualityID"]) if "OverallQualityID" in s else 1, BuyCount=1,
                       BuyPrice=n(s["BuyPrice"]), SellPrice=n(s["SellPrice"]), InventoryType=inv, AllowableClass=-1,
                       AllowableRace=-1, ItemLevel=max(1, n(s["ItemLevel"])), RequiredLevel=n(s["RequiredLevel"]),
                       maxcount=n(s["MaxCount"]), stackable=max(1, n(s["Stackable"])),
                       ContainerSlots=n(s["ContainerSlots"]), bonding=n(s["Bonding"]),
                       description=s["Description_lang"] or "", startquest=n(s["StartQuestID"]) if
                       n(s["StartQuestID"]) in self.quests else 0, Material=n(it["Material"]),
                       sheath=n(it["SheatheType"]), ScriptName="", VerifiedBuild=0)
            for z in ("dmg_type1", "dmg_type2"):
                row[z] = 0
            tmpl.append([row[c] for c in ITEM_TEMPLATE_COLUMNS])
            dbc.append([i, cls, sub, -1, n(it["Material"]), d, inv, n(it["SheatheType"])])
            self.item_map[i] = i
        self.write("05_item_template", insert("item_template", ITEM_TEMPLATE_COLUMNS, tmpl,
                                              "DELETE FROM `item_template` WHERE `entry` IN %s;" % in_list(r[0] for r in tmpl)
                                              if tmpl else None, "Retail's quest items (12.1.5), icon-only displays"))
        if dbc:
            self.files[os.path.join("dbc", "[%s]_world_item.sql" % self.a.tag)] = (
                "-- Item.dbc rows of the quest items. Generated by tools/races/retail_world_port.py.\n\n"
                + insert("item", "id class subclass sound_override_subclass material display_id inventory_type sheath"
                         .split(), dbc, "DELETE FROM `item` WHERE `id` IN %s;" % in_list(r[0] for r in dbc)))
        self.write_dbc("itemdisplayinfo", disp, "Icon-only displays of the quest items")

    def item(self, i):
        i = n(i)
        return self.item_map.get(i, 0) if i else 0

    # ---- conditions -----------------------------------------------------------------------------------------------
    def convert_conditions(self, rows, source_type, group, entry, source_id, what):
        """AzerothCore rows for retail condition rows (one source), or [] when nothing is left."""
        out = []
        for r in rows:
            ct = n(r["ConditionTypeOrReference"])
            v1, v2, v3 = n(r["ConditionValue1"]), n(r["ConditionValue2"]), n(r["ConditionValue3"])
            if ct == 48:                # retail: objective id, -, count -> quest, objective slot, count
                slot = self.objective_slot.get(v1)
                if not slot:
                    self.dropped["objective conditions of quests not ported"].append("%s %d" % (what, v1))
                    continue
                ct, (v1, v2) = 48, slot
            elif ct not in CONDITION_TYPES:
                self.dropped["condition types not mapped"].append("%s type %d" % (what, ct))
                continue
            out.append([source_type, group, entry, source_id, n(r["ElseGroup"]), ct, n(r["ConditionTarget"]), v1, v2,
                        v3, n(r["NegativeCondition"]), 0, 0, "", r["Comment"] or what])
        return out

    # ---- displays -------------------------------------------------------------------------------------------------
    def stock_dressed(self):
        """(race, sex) -> the lowest stock display dressed as that race and sex."""
        cd = c406.Dbc(os.path.join(STOCK_DBC, "CreatureDisplayInfo.dbc"))
        ce = c406.Dbc(os.path.join(STOCK_DBC, "CreatureDisplayInfoExtra.dbc"))
        out = {}
        for r in sorted(cd.records):
            x = ce.get(r[3]) if r[3] else None
            if x:
                out.setdefault((x[1], x[2]), r[0])
        return out

    def displays(self, ids):
        """retail display -> display here; writes the new CreatureDisplayInfo / CreatureModelData rows."""
        taken_d = config_range("NextDisplayID") | taken("creaturedisplayinfo", "id")
        dressed = None
        out = {d: d for d in ids if d in self.stock_cdisp}
        out.update(FALLBACK_DISPLAYS)
        rows = []
        for d in sorted(ids):
            if d in out:
                continue
            r = self.cdi.get(str(d))
            if not r:
                self.dropped["displays retail lacks (fell back to 11686)"].append(d)
                out[d] = 11686
            elif r["ExtendedDisplayInfoID"] != "0":
                dressed = dressed or self.stock_dressed()
                x = self.cdx.get(r["ExtendedDisplayInfoID"], {})
                race, sex = n(x.get("DisplayRaceID"), 1), n(x.get("DisplaySexID"))
                race = STOCK_RACE.get(race, race if race <= 11 else 1)
                out[d] = dressed.get((race, sex)) or dressed[(1, sex)]
                self.dropped["dressed NPCs shown as a stock NPC of their race (stage 2)"].append(d)
            else:
                rows.append(r)
        files = self.paths([self.cmd[r["ModelID"]]["FileDataID"] for r in rows]
                           + [r["TextureVariationFileDataID_%d" % i] for r in rows for i in range(4)])
        models, out_d, out_m = {}, [], []
        self.gender = {}
        for r in rows:
            d, m = int(r["ID"]), self.cmd[r["ModelID"]]
            path = files.get(m["FileDataID"])
            if not path:
                self.dropped["displays whose model the listfile can't name (fell back to 11686)"].append(d)
                out[d] = 11686
                continue
            folder = path.rsplit("/", 1)[0]
            tex = [files.get(r["TextureVariationFileDataID_%d" % i]) for i in range(4)
                   if r["TextureVariationFileDataID_%d" % i] != "0"]
            if not all(x and x.rsplit("/", 1)[0] == folder for x in tex) or len(tex) > 3:
                self.dropped["displays with textures outside their model's folder (textures left out)"].append(d)
                tex = [x for x in tex if x and x.rsplit("/", 1)[0] == folder][:3]
            if path not in models:
                models[path] = MODEL_BASE + len(models)
                f = lambda k: float(m[k])
                out_m.append(dict(
                    id=models[path], flags=int(m["Flags"]) & 0xFFFF, model_path=path.upper().replace("/", B),
                    size_class=int(m["SizeClass"]), model_scale=f("ModelScale"), blood_id=0,
                    footprint_texture_id=0, footprint_texture_length=f("FootprintTextureLength"),
                    footprint_texture_width=f("FootprintTextureWidth"), footprint_particle_scale=f("FootprintParticleScale"),
                    foley_material_id=int(m["FoleyMaterialID"]), footstep_shake_size=0, death_thud_shake_size=0,
                    sound_data=int(m["SoundID"]) if int(m["SoundID"]) in self.stock_sounds else 0,
                    collision_width=f("CollisionWidth"), collision_height=f("CollisionHeight"),
                    mount_height=f("MountHeight"), **{"geo_box_%s_%s" % (mm, ax): f("GeoBox_%d" % (i * 3 + j))
                                                      for i, mm in enumerate(("min", "max"))
                                                      for j, ax in enumerate("xyz")},
                    world_effect_scale=f("WorldEffectScale"), attached_effect_scale=f("AttachedEffectScale"),
                    missile_collision_radius=f("MissileCollisionRadius"), missile_collision_push=f("MissileCollisionPush"),
                    missile_collision_raise=f("MissileCollisionRaise")))
                self.assets.add(path.upper().replace("/", B))
            here = d if d not in taken_d else DISPLAY_BASE + sum(1 for x in out_d if x["id"] >= DISPLAY_BASE)
            names = [x.rsplit("/", 1)[1].rsplit(".", 1)[0] for x in tex] + ["", "", ""]
            out_d.append(dict(id=here, model_id=models[path], sound_id=int(r["SoundID"]) if int(r["SoundID"]) in self.stock_sounds else 0,
                              extended_display_info_id=0, creature_model_scale=float(r["CreatureModelScale"]),
                              creature_model_alpha=int(r["CreatureModelAlpha"]), texture_variation_1=names[0],
                              texture_variation_2=names[1], texture_variation_3=names[2], portrait_texture_name="",
                              blood_level=0, blood_id=0, npc_sound_id=0, praticle_color_id=0,
                              creature_geoset_data=0, obj_effect_package_id=0))
            self.gender[here] = int(r["Gender"]) if r["Gender"] in ("0", "1") else 2
            out[d] = here
        self.write_dbc("creaturemodeldata", out_m, "Retail creature models (CreatureModelData, 12.1.5) of the island's "
                       "spawns, numbered from %d; the files are WHE-common's patch-ER.MPQ" % MODEL_BASE)
        self.write_dbc("creaturedisplayinfo", out_d, "Retail creature displays (12.1.5) stock lacks; ids another "
                       "modpak uses moved to %d and up" % DISPLAY_BASE)
        return out

    def faction(self, ft):
        ft = FACTIONS.get(ft, ft)
        if ft in self.stock_ft:
            return ft
        r = self.rft.get(str(ft))
        hostile = bool(r and n(r["EnemyGroup"]) & 1)
        self.dropped["factions 3.3.5a lacks (hostile ones 14, the rest 35)"].append(ft)
        return 14 if hostile else 35

    # ---- creatures ------------------------------------------------------------------------------------------------
    def creatures(self):
        diff = {n(r["Entry"]): r for r in self.t["creature_template_difficulty"] if n(r["DifficultyID"]) == 0}
        levels = {}
        for r in self.spawns:
            lo, hi = AREA_LEVELS.get(n(r["areaId"]), AREA_LEVELS[self.a.zone])
            l0, h0 = levels.get(n(r["id"]), (99, 0))
            levels[n(r["id"])] = (min(lo, l0), max(hi, h0))
        givers = {n(r["id"]) for t in ("creature_queststarter", "creature_questender") for r in self.t[t]
                  if n(r["quest"]) in self.quests}
        self.loot = {}
        loot_ids = collections.defaultdict(list)
        for r in self.t["creature_loot_template"]:
            loot_ids[n(r["Entry"])].append(r)
        models = [r for r in self.t["creature_template_model"] if n(r["CreatureID"]) in self.entries]
        disp = self.displays({n(r["CreatureDisplayID"]) for r in models})
        tmpl, movement, loot = [], [], []
        addons = {n(r["entry"]): r for r in self.t["creature_template_addon"]}
        for e in self.entries:
            r, d = self.ct[e], diff.get(e, {})
            lo, hi = (1, 1) if n(r["type"]) == 8 else levels[e]
            if r["ScriptName"] or r["AIName"]:
                self.dropped["scripts left for SmartAI (plan.md stage 3)"].append("%d %s" % (e, r["ScriptName"] or r["AIName"]))
            family = pet_family(FAMILIES.get(n(r["family"]), n(r["family"])), self.stock_families)
            rows = [x for x in loot_ids.get(n(d.get("LootID")), []) if not n(x["ItemType"]) and self.item(x["Item"])]
            loot += [[e, self.item(x["Item"]), 0, n(x["Chance"]), n(x["QuestRequired"]), n(x["LootMode"], 1) or 1,
                      n(x["GroupId"]), n(x["MinCount"], 1), n(x["MaxCount"], 1), x["Comment"] or ""] for x in rows]
            npcflag = n(r["npcflag"]) & 0x7FFFFFF | (2 if e in givers else 0)
            tmpl.append([e, 0, 0, 0, 0, 0, r["name"], r["subname"] or None, r["IconName"] or None, 0, lo, hi, 0,
                         self.faction(n(r["faction"])), npcflag, n(r["speed_walk"], 1), n(r["speed_run"], 1.14286), 1, 1,
                         18, CLASSIFICATION.get(n(r["Classification"]), n(r["Classification"])), n(r["dmgschool"]),
                         n(d.get("DamageModifier"), 1), n(r["BaseAttackTime"], 2000) or 2000,
                         n(r["RangeAttackTime"], 2000) or 2000, n(r["BaseVariance"], 1) or 1,
                         n(r["RangeVariance"], 1) or 1, n(r["unit_class"], 1) or 1, n(r["unit_flags"]),
                         n(r["unit_flags2"]) & 0x3FFFF, 0, family, n(r["type"]), 0, e if rows else 0, 0, 0, 0, 0, 0, 0,
                         "", n(r["MovementType"]), 1, n(d.get("HealthModifier"), 1), n(d.get("ManaModifier"), 1),
                         n(d.get("ArmorModifier"), 1), n(r["ExperienceModifier"], 1) or 1, n(r["RacialLeader"]), 0,
                         n(r["RegenHealth"], 1), 0, 0, "", 0])
            a = addons.get(e)
            movement.append([e, 1, 1, 1 if a and n(a["AnimTier"]) == 3 else 0])
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
            [[n(r["CreatureID"]), n(r["Idx"]), disp[n(r["CreatureDisplayID"])], n(r["DisplayScale"], 1) or 1,
              n(r["Probability"], 1) or 1, 0] for r in sorted(models, key=lambda r: (n(r["CreatureID"]), n(r["Idx"])))],
            "DELETE FROM `creature_template_model` WHERE `CreatureID` IN %s;" % ents))
        self.write("12_creature_template_movement", insert(
            "creature_template_movement", "CreatureId Ground Swim Flight".split(), movement,
            "DELETE FROM `creature_template_movement` WHERE `CreatureId` IN %s;" % ents))
        info = {n(r["DisplayID"]): r for r in self.t["creature_model_info"]}
        rows, seen = [], set()
        for retail, here in sorted(disp.items()):
            if here in self.stock_cdisp or here in seen:
                continue
            seen.add(here)
            i = info.get(retail, {})
            rows.append([here, n(i.get("BoundingRadius"), 0.5), n(i.get("CombatReach"), 1.5), self.gender.get(here, 2), 0, 0])
        self.write("13_creature_model_info", insert(
            "creature_model_info", "DisplayID BoundingRadius CombatReach Gender DisplayID_Other_Gender VerifiedBuild".split(),
            rows, "DELETE FROM `creature_model_info` WHERE `DisplayID` IN %s;" % in_list(r[0] for r in rows) if rows else None))
        self.write("15_creature_template_addon", insert(
            "creature_template_addon", "entry path_id mount bytes1 bytes2 emote visibilityDistanceType auras".split(),
            [[e, 0, 0, self.bytes1(a), self.bytes2(a), self.emote(a), 0, self.auras(a)]
             for e, a in sorted(addons.items()) if e in self.entries],
            "DELETE FROM `creature_template_addon` WHERE `entry` IN %s;" % ents))
        self.write("50_creature_loot_template", insert(
            "creature_loot_template", "Entry Item Reference Chance QuestRequired LootMode GroupId MinCount MaxCount "
            "Comment".split(), loot, "DELETE FROM `creature_loot_template` WHERE `Entry` IN %s;" % ents))

    @staticmethod
    def bytes1(a):
        return n(a["StandState"]) | (n(a["VisFlags"]) << 16) | (n(a["AnimTier"]) << 24)

    @staticmethod
    def bytes2(a):
        return n(a["SheathState"]) | (n(a["PvPFlags"]) << 8)

    def emote(self, a, key="emote"):
        e = n(a[key]) if isinstance(a, dict) else n(a)
        return e if e in self.stock_emotes else 0

    def auras(self, a):
        keep = [x for x in (a["auras"] or "").split() if int(x) in self.stock_spells]
        return " ".join(keep) or None

    # ---- spawns ---------------------------------------------------------------------------------------------------
    def phase_conditions(self, kind, entry, guid, r):
        """Visibility conditions (source type 30) for a spawn in a retail phase."""
        phase = n(r["PhaseId"])
        if n(r["PhaseGroup"]):
            self.dropped["spawns in phase groups (shown to everyone)"].append(guid)
        if not phase:
            return
        rows = self.phase_rows.get(phase, {})
        area = n(r["areaId"])
        pick = rows.get(area) or rows.get(0) or (rows[min(rows)] if rows else [])
        self.conditions += self.convert_conditions(pick, 30, kind, entry, guid, "phase %d" % phase)

    def spawn_rows(self):
        tag = "[gen %s %s]" % (self.a.tag, self.a.comment)
        self.phase_rows = collections.defaultdict(lambda: collections.defaultdict(list))
        for r in self.t["conditions"]:
            if n(r["SourceTypeOrReferenceId"]) == 26:
                self.phase_rows[n(r["SourceGroup"])][n(r["SourceEntry"])].append(r)
        paths = {}
        addon = {r["guid"]: r for r in self.t["creature_addon"]}
        c, ca = [], []
        for r in self.spawns:
            guid = self.cguid[r["guid"]]
            a = addon.get(r["guid"])
            path = n(a["PathId"]) if a else 0
            if path:
                paths.setdefault(path, PATH_BASE + len(paths) + 1)
            move = n(r["MovementType"])
            if move == 2 and not path:
                move = 0
            c.append([guid, n(r["id"]), self.a.map, 0, 0, 1, 1, 0, n(r["position_x"]), n(r["position_y"]),
                      n(r["position_z"]), n(r["orientation"]), n(r["spawntimesecs"], 300), n(r["wander_distance"]), 0, 1, 0,
                      move, 0, 0, 0, "", 0, 1, tag])
            if a:
                ca.append([guid, paths.get(path, 0), 0, self.bytes1(a), self.bytes2(a), self.emote(a), 0, self.auras(a), ""])
            self.phase_conditions(0, n(r["id"]), guid, r)
        self.write("40_creature", insert(
            "creature", "guid id map zoneId areaId spawnMask phaseMask equipment_id position_x position_y position_z "
            "orientation spawntimesecs wander_distance currentwaypoint curhealth curmana MovementType npcflag "
            "unit_flags dynamicflags ScriptName VerifiedBuild CreateObject Comment".split(), c,
            "DELETE FROM `creature` WHERE `Comment` = '%s';" % tag))
        self.write("41_creature_addon", insert(
            "creature_addon", "guid path_id mount bytes1 bytes2 emote visibilityDistanceType auras Comment".split(), ca,
            "DELETE FROM `creature_addon` WHERE `guid` BETWEEN %d AND %d;" % (CREATURE_GUID, CREATURE_GUID + 99999)))
        mtype = {n(r["PathId"]): n(r["MoveType"]) for r in self.t["waypoint_path"]}
        wp = [[paths[n(r["PathId"])], n(r["NodeId"]), n(r["PositionX"]), n(r["PositionY"]), n(r["PositionZ"]),
               n(r["Orientation"]) if r["Orientation"] is not None else None, "", n(r["Delay"]), mtype.get(n(r["PathId"]), 0),
               0, 100, 0] for r in self.t["waypoint_path_node"] if n(r["PathId"]) in paths]
        self.write("44_waypoint_data", insert(
            "waypoint_data", "id point position_x position_y position_z orientation Comment delay move_type action "
            "action_chance wpguid".split(), sorted(wp, key=lambda w: (w[0], w[1])),
            "DELETE FROM `waypoint_data` WHERE `id` BETWEEN %d AND %d;" % (PATH_BASE, PATH_BASE + 99999)))
        g = []
        for r in self.gspawns:
            guid = self.gguid[r["guid"]]
            g.append([guid, n(r["id"]), self.a.map, 0, 0, 1, 1, n(r["position_x"]), n(r["position_y"]),
                      n(r["position_z"]), n(r["orientation"])]
                     + [n(x) for x in go_rotation(r["orientation"], r["rotation0"], r["rotation1"], r["rotation2"], r["rotation3"])]
                     + [n(r["spawntimesecs"], 300), 255, 1, "", 0, tag])
            self.phase_conditions(1, n(r["id"]), guid, r)
        self.write("42_gameobject", insert(
            "gameobject", "guid id map zoneId areaId spawnMask phaseMask position_x position_y position_z orientation "
            "rotation0 rotation1 rotation2 rotation3 spawntimesecs animprogress state ScriptName VerifiedBuild "
            "Comment".split(), g, "DELETE FROM `gameobject` WHERE `Comment` = '%s';" % tag))

    # ---- objects --------------------------------------------------------------------------------------------------
    def gameobjects(self):
        taken_g = taken("gameobjectdisplayinfo", "id")
        rows = [self.got[e] for e in self.goentries]
        quest_of = {}                                   # object entry -> quest whose objective uses it
        for q, objs in self.objectives.items():
            for o in objs:
                if n(o["Type"]) == 2:
                    quest_of.setdefault(n(o["ObjectID"]), q)
        givers = {n(r["id"]) for t in ("gameobject_queststarter", "gameobject_questender") for r in self.t[t]
                  if n(r["quest"]) in self.quests}
        new = sorted({n(r["displayId"]) for r in rows} - self.stock_gdisp - {0})
        files = self.paths([self.gdi[str(d)]["FileDataID"] for d in new if str(d) in self.gdi])
        disp, out = {}, []
        for d in new:
            x = self.gdi.get(str(d))
            path = files.get(x["FileDataID"]) if x else None
            if not path:
                self.dropped["object displays nothing names"].append(d)
                continue
            path = path.replace("/", B)
            disp[d] = d if d not in taken_g else GO_DISPLAY_BASE + len([v for v in disp.values() if v >= GO_DISPLAY_BASE])
            out.append(dict(id=disp[d], model_name=re.sub(r"\.m2$", ".mdx", path, flags=re.I),
                            **{"sound_%d" % (i + 1): 0 for i in range(10)},
                            **{"geo_box_%s_%s" % (mm, ax): float(x["GeoBox_%d" % (i * 3 + j)])
                               for i, mm in enumerate(("min", "max")) for j, ax in enumerate("xyz")}))
            self.assets.add(path.upper() if path.lower().endswith(".m2") else path)
        tmpl, gloot, qitem = [], [], []
        loot_rows = collections.defaultdict(list)
        for r in self.t["gameobject_loot_template"]:
            loot_rows[n(r["Entry"])].append(r)
        for r in rows:
            e, d, typ = n(r["entry"]), n(r["displayId"]), n(r["type"])
            data = [n(r["Data%d" % i]) for i in range(24)]
            lock = data[0] if data[0] in self.stock_locks else 0
            used = e in quest_of or e in givers
            if typ == 3:                                # chest: lock, loot, restock .. linked trap, quest
                data = [lock] + data[1:9] + [0] * 15
                for x in loot_rows.get(data[1], []):
                    if not n(x["ItemType"]) and self.item(x["Item"]):
                        gloot.append([data[1], self.item(x["Item"]), 0, n(x["Chance"]), n(x["QuestRequired"]),
                                      n(x["LootMode"], 1) or 1, n(x["GroupId"]), n(x["MinCount"], 1), n(x["MaxCount"], 1),
                                      x["Comment"] or ""])
            elif typ == 10 and used:                    # goober: lock, the quest it counts for, .., spell
                spell = data[10] if data[10] in self.stock_spells else 0
                data = [lock, quest_of.get(e, 0), 0] + data[3:7] + [0, 0, 0, spell] + [0] * 13
            elif typ == 2:                              # quest giver
                data = [lock] + [0] * 23
            else:
                if typ != 5:
                    self.dropped["objects no quest uses (made props)"].append("%d %s type %d" % (e, r["name"], typ))
                typ, data = 5, [0] * 24
            tmpl.append([e, typ, disp.get(d, d), r["name"], "", "", "", n(r["size"], 1)] + data + ["", "", 0])
        for r in self.t["gameobject_questitem"]:
            if n(r["GameObjectEntry"]) in self.goentries and self.item(r["ItemId"]):
                qitem.append([n(r["GameObjectEntry"]), n(r["Idx"]), self.item(r["ItemId"]), 0])
        cols = ("entry type displayId name IconName castBarCaption unk1 size " + " ".join("Data%d" % i for i in range(24))
                + " AIName ScriptName VerifiedBuild").split()
        gents = in_list(self.goentries)
        self.write("20_gameobject_template", insert("gameobject_template", cols, tmpl,
                                                    "DELETE FROM `gameobject_template` WHERE `entry` IN %s;" % gents))
        self.write("22_gameobject_questitem", insert(
            "gameobject_questitem", "GameObjectEntry Idx ItemId VerifiedBuild".split(), qitem,
            "DELETE FROM `gameobject_questitem` WHERE `GameObjectEntry` IN %s;" % gents))
        self.write("51_gameobject_loot_template", insert(
            "gameobject_loot_template", "Entry Item Reference Chance QuestRequired LootMode GroupId MinCount MaxCount "
            "Comment".split(), gloot, "DELETE FROM `gameobject_loot_template` WHERE `Entry` IN %s;"
            % in_list({r[0] for r in gloot}) if gloot else None))
        self.write_dbc("gameobjectdisplayinfo", out, "Retail object displays (12.1.5) of the island's objects")

    # ---- quests ---------------------------------------------------------------------------------------------------
    def team(self, q):
        return None if q in NEUTRAL_QUESTS else HORDE if q in HORDE_QUESTS else ALLIANCE

    def infer_givers(self):
        """(starters, enders, prev) for the quests the TDB gives no giver on the island (see GIVER_RANGE)."""
        import math
        on_island = {n(r["id"]) for r in self.spawns}
        rel = {k: collections.defaultdict(list) for k in ("creature_queststarter", "creature_questender")}
        for k in rel:
            for r in self.t[k]:
                if n(r["quest"]) in self.quests and n(r["id"]) in on_island:
                    rel[k][n(r["quest"])].append(n(r["id"]))
        turn_in = collections.defaultdict(list)
        blobs = {(n(r["QuestID"]), n(r["Idx1"])) for r in self.t["quest_poi"]
                 if n(r["ObjectiveIndex"]) == -1 and n(r["MapID"]) == self.a.map}
        for r in self.t["quest_poi_points"]:
            if (n(r["QuestID"]), n(r["Idx1"])) in blobs:
                turn_in[n(r["QuestID"])].append((n(r["X"]), n(r["Y"])))
        givers = [r for r in self.spawns if n(self.ct[n(r["id"])]["npcflag"]) & 2]
        enders, starters, prev = {}, {}, {}
        for q in self.quests:
            if rel["creature_questender"].get(q) or q not in turn_in:
                continue
            pts = turn_in[q]
            cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
            names = TEAM_NAMES.get(self.team(q), set())
            best = min(((math.hypot(n(r["position_x"]) - cx, n(r["position_y"]) - cy), n(r["id"])) for r in givers
                        if self.ct[n(r["id"])]["name"] in names), default=None)
            if best and best[0] <= GIVER_RANGE:
                enders[q] = best[1]
        ender = lambda q: (rel["creature_questender"].get(q) or [enders.get(q)])[0]
        order = collections.defaultdict(list)
        for r in table(self.a.csv_dir, "QuestLineXQuest").values():
            order[n(r["QuestLineID"])].append((n(r["OrderIndex"]), n(r["QuestID"])))
        for team, lines in QUEST_LINES.items():
            chain = [q for line in lines for _, q in sorted(order[line]) if q in self.quests]
            last = None
            for q in chain:
                classes = n(self.qaddon.get(q, {}).get("AllowableClasses"))
                if last and not rel["creature_queststarter"].get(q) and q not in starters and ender(last):
                    starters[q] = ender(last)
                    prev[q] = last
                if not classes:
                    last = q
        return starters, enders, prev

    def quest_rows(self):
        self.inferred = self.infer_givers()
        qs = in_list(self.quests)
        self.objective_slot = {}
        qt, qa, triggers, involved = [], [], [], []
        at = table(self.a.csv_dir, "AreaTrigger")
        taken_at = taken("areatrigger", "id")
        for q, s in sorted(self.quests.items()):
            npc, items, texts, explore = [], [], [], []
            for o in self.objectives[q]:
                typ, obj = n(o["Type"]), n(o["ObjectID"])
                if typ in (0, 3):
                    self.objective_slot[n(o["ID"])] = (q, len(npc))
                    npc.append((obj, n(o["Amount"]) or 1))
                    texts.append(o["Description"] or "")
                elif typ == 2:
                    self.objective_slot[n(o["ID"])] = (q, len(npc))
                    npc.append((-obj, n(o["Amount"]) or 1))
                    texts.append(o["Description"] or "")
                elif typ == 1:
                    if not self.item(obj):
                        self.dropped["item objectives of items not ported"].append("%d %d" % (q, obj))
                        continue
                    items.append((self.item(obj), n(o["Amount"]) or 1))
                elif typ == 19:
                    explore.append(obj)
                else:
                    self.dropped["objective types 3.3.5a lacks (criteria trees; SmartAI later)"].append(
                        "%d type %d %s" % (q, typ, o["Description"] or ""))
            if len(npc) > 4 or len(items) > 6:
                self.dropped["quests with more objectives than 3.3.5a holds"].append(q)
            npc, items, texts = (npc + [(0, 0)] * 4)[:4], (items + [(0, 0)] * 6)[:6], (texts + [""] * 4)[:4]
            nxt = n(s["RewardNextQuest"])
            row = [q, n(s["QuestType"]), -1, 1, self.a.zone, n(s["QuestInfoID"]) if n(s["QuestInfoID"]) in self.stock_qinfo else 0,
                   n(s["SuggestedGroupNum"]), 0, 0, 0, 0, nxt if nxt in self.quests else 0,
                   min(n(s["RewardXPDifficulty"]), 9), 0, 0,
                   n(s["RewardDisplaySpell1"]) if n(s["RewardDisplaySpell1"]) in self.stock_spells else 0,
                   n(s["RewardSpell"]) if n(s["RewardSpell"]) in self.stock_spells else 0, 0, 0, self.item(s["StartItem"]),
                   n(s["Flags"]) & 0xFFFFF, 0]
            for i in range(1, 5):
                row += [self.item(s["RewardItem%d" % i]), n(s["RewardAmount%d" % i]) if self.item(s["RewardItem%d" % i]) else 0]
            for i in range(1, 5):
                row += [self.item(s["ItemDrop%d" % i]), n(s["ItemDropQuantity%d" % i]) if self.item(s["ItemDrop%d" % i]) else 0]
            for i in range(1, 7):
                row += [self.item(s["RewardChoiceItemID%d" % i]),
                        n(s["RewardChoiceItemQuantity%d" % i]) if self.item(s["RewardChoiceItemID%d" % i]) else 0]
            row += [0, 0, 0, 0, 0, 0, 0]
            for i in range(1, 6):
                f = n(s["RewardFactionID%d" % i])
                f = f if f in self.stock_factions else 0
                row += [f, n(s["RewardFactionValue%d" % i]) if f else 0, n(s["RewardFactionOverride%d" % i]) if f else 0]
            # retail's $<n>oa is objective n's amount; 3.3.5a would print it as it is
            amounts = [n(o["Amount"]) or 1 for o in self.objectives[q]]
            fix = lambda text: re.sub(r"\$(\d)oa", lambda m: str(amounts[int(m.group(1)) - 1])
                                      if int(m.group(1)) <= len(amounts) else m.group(0), text or "")
            row += [n(s["TimeAllowed"]), 0, 0, s["LogTitle"] or "", fix(s["LogDescription"]), fix(s["QuestDescription"]),
                    fix(s["AreaDescription"]), fix(s["QuestCompletionLog"])]
            for e, c in npc:
                row += [e, c]
            for i, c in items:
                row += [i, c]
            row += [0] + texts + [0]
            qt.append(row)
            a = self.qaddon.get(q, {})
            classes = n(a.get("AllowableClasses"))
            special = n(a.get("SpecialFlags")) & 0xF
            for t in explore:
                r = at.get(str(t))
                if not r and t in SERVER_TRIGGERS:
                    m, x, y, z, rad = SERVER_TRIGGERS[t]
                    r = dict(ContinentID=str(m), Pos_0=x, Pos_1=y, Pos_2=z, Radius=rad, Box_length=0, Box_width=0,
                             Box_height=0, Box_yaw=0)
                if not r:
                    self.dropped["area triggers nothing places (TrinityCore scripts them)"].append("%d %d" % (q, t))
                    continue
                if t in taken_at:
                    sys.exit("area trigger %d is another modpak's" % t)
                special |= EXPLORATION
                involved.append([t, q])
                if t not in {x["id"] for x in triggers}:
                    triggers.append(dict(id=t, map_id=n(r["ContinentID"]), x=float(r["Pos_0"]), y=float(r["Pos_1"]),
                                         z=float(r["Pos_2"]), radius=float(r["Radius"]), box_length=float(r["Box_length"]),
                                         box_width=float(r["Box_width"]), box_height=float(r["Box_height"]),
                                         box_yaw=float(r["Box_yaw"])))
            link = lambda k: n(a.get(k)) if abs(n(a.get(k))) in self.quests else 0
            qa.append([q, n(a.get("MaxLevel")), classes & CLASS_MASK, 0, link("PrevQuestID") or self.inferred[2].get(q, 0),
                       link("NextQuestID"),
                       n(a.get("ExclusiveGroup")), link("BreadcrumbForQuestId"), 0, 0, 0, 0, 0, 0, 0, 0,
                       n(a.get("ProvidedItemCount")), special])
        cols = ("ID QuestType QuestLevel MinLevel QuestSortID QuestInfoID SuggestedGroupNum RequiredFactionId1 "
                "RequiredFactionId2 RequiredFactionValue1 RequiredFactionValue2 RewardNextQuest RewardXPDifficulty "
                "RewardMoney RewardMoneyDifficulty RewardDisplaySpell RewardSpell RewardHonor RewardKillHonor StartItem "
                "Flags RequiredPlayerKills").split()
        cols += sum((["RewardItem%d" % i, "RewardAmount%d" % i] for i in range(1, 5)), [])
        cols += sum((["ItemDrop%d" % i, "ItemDropQuantity%d" % i] for i in range(1, 5)), [])
        cols += sum((["RewardChoiceItemID%d" % i, "RewardChoiceItemQuantity%d" % i] for i in range(1, 7)), [])
        cols += "POIContinent POIx POIy POIPriority RewardTitle RewardTalents RewardArenaPoints".split()
        cols += sum((["RewardFactionID%d" % i, "RewardFactionValue%d" % i, "RewardFactionOverride%d" % i]
                     for i in range(1, 6)), [])
        cols += ("TimeAllowed AllowableRaces AllowableRaces_2 LogTitle LogDescription QuestDescription AreaDescription "
                 "QuestCompletionLog").split()
        cols += sum((["RequiredNpcOrGo%d" % i, "RequiredNpcOrGoCount%d" % i] for i in range(1, 5)), [])
        cols += sum((["RequiredItemId%d" % i, "RequiredItemCount%d" % i] for i in range(1, 7)), [])
        cols += ["Unknown0"] + ["ObjectiveText%d" % i for i in range(1, 5)] + ["VerifiedBuild"]
        self.write("30_quest_template", insert("quest_template", cols, qt,
                                               "DELETE FROM `quest_template` WHERE `ID` IN %s;" % qs,
                                               "Retail's Exile's Reach quests; both factions share races, so each "
                                               "has a team condition (conditions file)"))
        self.write("31_quest_template_addon", insert(
            "quest_template_addon", "ID MaxLevel AllowableClasses SourceSpellID PrevQuestID NextQuestID ExclusiveGroup "
            "BreadcrumbForQuestId RewardMailTemplateID RewardMailDelay RequiredSkillID RequiredSkillPoints "
            "RequiredMinRepFaction RequiredMaxRepFaction RequiredMinRepValue RequiredMaxRepValue ProvidedItemCount "
            "SpecialFlags".split(), qa, "DELETE FROM `quest_template_addon` WHERE `ID` IN %s;" % qs))
        offer = [[n(r["ID"])] + [self.emote(r["Emote%d" % i]) for i in range(1, 5)]
                 + [n(r["EmoteDelay%d" % i]) for i in range(1, 5)] + [r["RewardText"] or "", 0]
                 for r in self.t["quest_offer_reward"] if n(r["ID"]) in self.quests]
        req = [[n(r["ID"]), self.emote(r["EmoteOnComplete"]), self.emote(r["EmoteOnIncomplete"]), r["CompletionText"] or "", 0]
               for r in self.t["quest_request_items"] if n(r["ID"]) in self.quests]
        det = [[n(r["ID"])] + [self.emote(r["Emote%d" % i]) for i in range(1, 5)]
               + [n(r["EmoteDelay%d" % i]) for i in range(1, 5)] + [0]
               for r in self.t["quest_details"] if n(r["ID"]) in self.quests]
        self.write("32_quest_offer_reward", insert(
            "quest_offer_reward", "ID Emote1 Emote2 Emote3 Emote4 EmoteDelay1 EmoteDelay2 EmoteDelay3 EmoteDelay4 "
            "RewardText VerifiedBuild".split(), offer, "DELETE FROM `quest_offer_reward` WHERE `ID` IN %s;" % qs))
        self.write("33_quest_request_items", insert(
            "quest_request_items", "ID EmoteOnComplete EmoteOnIncomplete CompletionText VerifiedBuild".split(), req,
            "DELETE FROM `quest_request_items` WHERE `ID` IN %s;" % qs))
        self.write("34_quest_details", insert(
            "quest_details", "ID Emote1 Emote2 Emote3 Emote4 EmoteDelay1 EmoteDelay2 EmoteDelay3 EmoteDelay4 "
            "VerifiedBuild".split(), det, "DELETE FROM `quest_details` WHERE `ID` IN %s;" % qs))
        # POIs: one blob per (quest, Idx1); objective indexes as 3.3.5a counts them (creatures 0-3, items 4-9)
        slot = {}
        for q, objs in self.objectives.items():
            k_npc = k_item = 0
            for o in objs:
                if n(o["Type"]) in (0, 2, 3):
                    slot[n(o["ID"])] = k_npc
                    k_npc += 1
                elif n(o["Type"]) == 1:
                    slot[n(o["ID"])] = 4 + k_item
                    k_item += 1
        poi, seen = [], set()
        for r in sorted(self.t["quest_poi"], key=lambda r: (n(r["QuestID"]), n(r["Idx1"]), n(r["BlobIndex"]))):
            q = n(r["QuestID"])
            if q in self.quests and n(r["MapID"]) == self.a.map and (q, n(r["Idx1"])) not in seen:
                idx = n(r["ObjectiveIndex"])
                if idx >= 0:
                    if n(r["QuestObjectiveID"]) not in slot:
                        continue
                    idx = slot[n(r["QuestObjectiveID"])]
                seen.add((q, n(r["Idx1"])))
                poi.append([q, n(r["Idx1"]), idx, self.a.map, self.a.world_map_area, 0, n(r["Priority"]), n(r["Flags"]), 0])
        pts = [[n(r["QuestID"]), n(r["Idx1"]), n(r["Idx2"]), n(r["X"]), n(r["Y"]), 0] for r in self.t["quest_poi_points"]
               if (n(r["QuestID"]), n(r["Idx1"])) in seen]
        self.write("35_quest_poi", insert("quest_poi", "QuestID id ObjectiveIndex MapID WorldMapAreaId Floor Priority "
                                          "Flags VerifiedBuild".split(), poi,
                                          "DELETE FROM `quest_poi` WHERE `QuestID` IN %s;" % qs))
        self.write("36_quest_poi_points", insert("quest_poi_points", "QuestID Idx1 Idx2 X Y VerifiedBuild".split(), pts,
                                                 "DELETE FROM `quest_poi_points` WHERE `QuestID` IN %s;" % qs))
        self.write("37_areatrigger_involvedrelation", insert(
            "areatrigger_involvedrelation", "id quest".split(), involved,
            "DELETE FROM `areatrigger_involvedrelation` WHERE `quest` IN %s;" % qs))
        self.write_dbc("areatrigger", triggers, "Retail's area triggers of the quests' exploration objectives")
        known = {"creature_queststarter": set(self.entries) | self.stock_creatures,
                 "creature_questender": set(self.entries) | self.stock_creatures,
                 "gameobject_queststarter": set(self.goentries), "gameobject_questender": set(self.goentries)}
        for k, t in enumerate(("creature_queststarter", "creature_questender", "gameobject_queststarter",
                               "gameobject_questender")):
            rel = {(n(r["id"]), n(r["quest"])) for r in self.t[t] if n(r["quest"]) in self.quests}
            for e, q in sorted(rel):
                if e not in known[t]:
                    self.dropped["%s of NPCs/objects not on the island" % t].append("%d %d" % (e, q))
            inferred = {"creature_queststarter": self.inferred[0], "creature_questender": self.inferred[1]}.get(t, {})
            rel = sorted(rel | {(e, q) for q, e in inferred.items()})
            if t.startswith("creature"):
                have = {q for e, q in rel if e in known[t]}
                self.dropped["quests with no %s (left for SmartAI / scripts)" % t.split("_")[1]].extend(
                    "%d %s" % (q, self.quests[q]["LogTitle"]) for q in sorted(set(self.quests) - have))
            self.write("%d_%s" % (45 + k, t), insert(t, ["id", "quest"], [x for x in rel if x[0] in known[t]],
                                                    "DELETE FROM `%s` WHERE `quest` IN %s;" % (t, qs)))
        # who may take them: retail's own conditions, each else-group with the quest's team added
        retail = collections.defaultdict(list)
        for r in self.t["conditions"]:
            if n(r["SourceTypeOrReferenceId"]) == 19 and n(r["SourceEntry"]) in self.quests:
                retail[n(r["SourceEntry"])].append(r)
        for q in sorted(self.quests):
            rows = self.convert_conditions(retail.get(q, []), 19, 0, q, 0, "quest %d" % q)
            if q in NEUTRAL_QUESTS:
                self.conditions += rows
                continue
            team = HORDE if q in HORDE_QUESTS else ALLIANCE
            groups = sorted({r[4] for r in rows}) or [0]
            self.conditions += rows + [[19, 0, q, 0, g, 6, 0, team, 0, 0, 0, 0, 0, "",
                                        "quest %d: %s only" % (q, "Horde" if team == HORDE else "Alliance")]
                                       for g in groups]

    def write_conditions(self):
        cols = ("SourceTypeOrReferenceId SourceGroup SourceEntry SourceId ElseGroup ConditionTypeOrReference "
                "ConditionTarget ConditionValue1 ConditionValue2 ConditionValue3 NegativeCondition ErrorType ErrorTextId "
                "ScriptName Comment").split()
        delete = ("DELETE FROM `conditions` WHERE (`SourceTypeOrReferenceId` = 19 AND `SourceEntry` IN %s) OR "
                  "(`SourceTypeOrReferenceId` = 30 AND `SourceId` BETWEEN %d AND %d);"
                  % (in_list(self.quests), CREATURE_GUID, CREATURE_GUID + 99999))
        self.write("60_conditions", insert("conditions", cols, self.conditions, delete,
                                           "Phased spawns' visibility (source type 30, per guid) and the quests' "
                                           "availability (19)"))

    def run(self):
        self.port_items()
        self.creatures()
        self.gameobjects()
        self.quest_rows()
        self.spawn_rows()
        self.write_conditions()
        self.files["wi_assets.txt"] = "".join(p + "\n" for p in sorted(self.assets))
        prefix = ("zz_[AUTO,%s]_world_" % self.a.tag, "[%s]_world_" % self.a.tag,
                  "zz_[AUTO,%s]_spawns_" % self.a.tag, "[%s]_spawns_" % self.a.tag)
        for sub in (os.path.join("sql", "db-world", "base"), "dbc"):
            folder = os.path.join(self.a.modpak, sub)
            for f in os.listdir(folder) if os.path.isdir(folder) else ():
                if f.startswith(prefix):
                    os.remove(os.path.join(folder, f))
        for rel, text in sorted(self.files.items()):
            path = os.path.join(self.a.modpak, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
        phased = sum(1 for r in self.spawns + self.gspawns if n(r["PhaseId"]))
        print("%d creature spawns of %d new creatures, %d object spawns of %d objects (%d phased), %d quests, "
              "%d items, %d conditions, %d files" % (len(self.spawns), len(self.entries), len(self.gspawns),
                                                     len(self.goentries), phased, len(self.quests),
                                                     len(self.item_map), len(self.conditions), len(self.files)))
        for k, v in sorted(self.dropped.items()):
            print("%s: %d (%s)" % (k, len(v), ", ".join(str(x) for x in sorted(set(v), key=str)[:10])))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("tdb")
    p.add_argument("csv_dir")
    p.add_argument("modpak")
    p.add_argument("--map", type=int, default=2175)
    p.add_argument("--zone", type=int, default=10424)
    p.add_argument("--world-map-area", type=int, default=1409)
    p.add_argument("--tag", default="F-137")
    p.add_argument("--comment", default="Exiles Reach")    # in spawn Comments and their DELETE: no quotes
    p.add_argument("--cache")
    a = p.parse_args()
    wi.TAG = a.tag      # taken() leaves out the modpak's own files
    Port(a).run()


if __name__ == "__main__":
    main()

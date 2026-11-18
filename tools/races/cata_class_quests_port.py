"""Port Cataclysm's starting-area class practice quests to F-029_all-trainers.

  python cata_class_quests_port.py WORLD_SQL F029_DIR [--acore AZEROTHCORE] [--cache PICKLE]

WORLD_SQL is Project Neltharion's `source/sql/base/world.zip` unpacked (as for cata_zone_extract.py). AZEROTHCORE is
the 256-bit core checkout: its base world SQL says which trainers stand where, their names and the spell ranks. Rerun
this after changing it: it replaces its own files in F029_DIR (sql/.../zz_[AUTO,F-029]_*.sql, dbc/[F-029]_*.sql) and
leaves F-029's hand-written ones alone.

Cataclysm gave every starting area a level-3 quest per class: learn a spell from the class trainer, then use it on a
training dummy (or heal a wounded NPC). This takes the ones of the eight stock starting areas and moves two of Echo
Isles' (priest, druid) to the Valley of Trials, whose classes Cataclysm left without them; the other Echo Isles and New
Tinkertown quests have Valley of Trials and Coldridge Valley twins already. Built on cata_gilneas_port.Port (F-130):
- the quest givers are the trainers of the quest's class that stand in its area here, stock's or F-029's (which
  places Cataclysm's new race/class trainers' counterparts); their names replace Cataclysm's in the texts. A zone
  condition keeps a trainer entry that also stands elsewhere (F-029 reuses stock entries) to its own area's quest
- the quests are open to the area's faction, not one race, and one per class (ExclusiveGroup): ARAC's and the custom
  races' characters train there too. The faction is a team condition with race mask 0, so ARAC's quest update (which
  opens every race-masked class quest to both factions) leaves them alone, whatever the manifest order. Prerequisites
  and follow-ups are dropped (Cataclysm's letters and starting-area chains mostly aren't here)
- the WotLK priest "Garments" quests, which Cataclysm replaced with these, are no longer offered; their "In Favor
  of..." breadcrumbs to the first town's priest trainer stay
- as F-013's [I-273]: level 4, and the spells 3.3.5a trains far above it become ones its trainers teach at 4
  (SPELL_SWAP, texts in TEXT_SWAP / TEXT_FIXES); every rank of the spell gives credit
- the dummies and wounded NPCs come over with their spawns, SmartAI and displays; Cataclysm's dummies use F-013's
  core script npc_zep_training_dummy (takes no damage, keeps its SmartAI)
- Valley of Trials' druid trainer is Zen'tabra, Echo Isles' troll druid, in place of F-029's tauren Gart Mistrunner
"""
import argparse, collections, math, os, pickle, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cata_zone_extract as X  # noqa: E402
import cata_gilneas_port as G  # noqa: E402

TAG = "F-029"
GARMENTS = (5621, 5624, 5625, 5648, 5650)       # WotLK priest "Garments of ..." quests
CREATURE_GUID = 13500001
F029 = os.path.join(HERE, "..", "..", "modpaks", "F-029_all-trainers", "sql", "db-world", "base")

# area: (map, x, y, zone id for the zone condition, faction mask, radius)
AREAS = {
    "Northshire": (0, -8900, -180, 12, G.CATA_ALLIANCE),
    "Coldridge Valley": (0, -6100, 385, 1, G.CATA_ALLIANCE),
    "Deathknell": (0, 1850, 1600, 85, G.CATA_HORDE),
    "Camp Narache": (1, -2900, -250, 215, G.CATA_HORDE),
    "Valley of Trials": (1, -620, -4210, 14, G.CATA_HORDE),
    "Shadowglen": (1, 10480, 790, 141, G.CATA_ALLIANCE),
    "Ammen Vale": (530, -4125, -13745, 3524, G.CATA_ALLIANCE),
    "Sunstrider Isle": (530, 10360, -6420, 3430, G.CATA_HORDE),
}
RADIUS = 250
# Echo Isles quests for classes the Valley of Trials has none for: quest -> area
TRANSPLANT = {24784: "Valley of Trials", 24766: "Valley of Trials"}
TRANSPLANT_TARGETS = {47057}                     # Wounded Darkspear Watcher: placed by the Valley's dummies
TROLL_DRUID, F029_VALLEY_DRUID_GUID = 38243, 6210113   # Zen'tabra; F-029's Gart Mistrunner spawn she replaces
# Cataclysm's trainers for its new race/class pairs in the second towns, with their 4.3.4 spawns: entry -> the stock
# trainer of the same class and faction whose trainer list and gossip they get (Neltharion's gossip isn't ported).
# The classes Cataclysm didn't add there are [F-029]_second_town_trainers.sql's
SECOND_TOWN_TRAINERS = {46983: 1231,    # Benjamin Foxworthy, Goldshire hunter (Grif Wildheart)
                        43464: 17212,   # Halbin Frosthammer, Kharanos shaman (Tuluun)
                        44380: 3064,    # Jabul, Razor Hill druid (Gennia Runetotem)
                        43015: 3706,    # Seer Alsoomse, Bloodhoof Village priest (Tai'jin)
                        43013: 16275,   # Sunwalker Iopi, Bloodhoof Village paladin (Noellene)
                        39100: 3171,    # Dedlow Wormwood, Brill hunter (Thotar)
                        43012: 2131}    # Lothan Silverblade, Falconwing Square warrior (Austil de Mon)
SECOND_TOWNS = {"Goldshire": (0, -9460, 40), "Kharanos": (0, -5600, -500), "Razor Hill": (1, 320, -4700),
                "Bloodhoof Village": (1, -2300, -370), "Brill": (0, 2260, 270), "Falconwing Square": (530, 9500, -6800)}
STOCK_TARGETS = {16971}                          # Injured Draenei: stock, spawned in Ammen Vale already
CREDIT = 44175                                   # Spell Practice Credit: the dummies' KillCredit

# Cataclysm class quest bit -> class id
CLASS_BITS = {1: 1, 2: 2, 4: 3, 8: 4, 16: 5, 64: 7, 128: 8, 256: 9, 1024: 11}
# spells 3.3.5a trains far above level 4 -> what its trainers teach at 4 (F-013's [I-273])
SPELL_SWAP = {56641: 1978, 5143: 116, 2061: 2052, 73899: 8042}
TEXT_SWAP = [("Steady Shot", "Serpent Sting"), ("Arcane Missiles", "Frostbolt"), ("Flash Heal", "Lesser Heal"),
             ("Primal Strike", "Earth Shock"), ("primal strike", "earth shock"), ("Reach level 3", "Reach level 4"),
             ("Rejuvination", "Rejuvenation"), ("Evisecerate", "Eviscerate")]
# trainer names Cataclysm's texts use besides the quest giver's own (short forms, typos, copied texts)
OTHER_NAMES = ("Sister Goldskimmer", "Zen'Tabra", "Tunari", "Llane Bershere", "Delios")
# stock's generic "<Class> Trainer" NPCs, which stand in the starting areas too; never the quest giver
GENERIC_TRAINERS = set(range(26324, 26333))
# texts a name swap can't fix: Cataclysm's mechanics (Arcane Missiles' proc, Primal Strike, focus), Echo Isles places
TEXT_FIXES = {
    24526: {"Details": "Excellent!  Let's get started.$b$bFirst, you're going to have to learn the spell Frostbolt.  "
                       "It strikes with bitter cold and slows whatever it hits, so your foes reach you later than "
                       "they'd like.  Why not get a feel for the spell using those training dummies the militia "
                       "trainees put up outside the entrance to Anvilmar?"},
    24965: {"Details": "Let's get some work done, shall we?  I've got a new spell for you.  You interested?$B$B"
                       "Frostbolt chills whatever it hits and slows it down.  Handy, when the thing in question would "
                       "rather eat you."},
    25149: {"Details": "Alright, here's the easy part.  All you have to do is listen to me.  And pay me a little bit of "
                       "copper.$b$bSpeak with me again and we'll teach you the rite of Frostbolt. This isn't just an "
                       "ordinary spell, $N. Its cold bites deep and slows your enemy, so use it well.$B$B Once your "
                       "lesson is finished, practice your new spell against a training dummy."},
    26916: {"Details": "As a mage, you will learn a variety of spells as your understanding grows. I want to show you a "
                       "new technique that hurls a bolt of frost at your opponent, chilling and slowing it: Frostbolt. "
                       " I'll show you how it's done, and then I want you to go try it on one of the training dummies "
                       "south of the entrance to the abbey."},
    26940: {"Details": "We are the heirs to a legacy of arcane magic and your path will not be an easy one. Many still "
                       "hold us responsible for the actions of our forebears, but our talents are needed.$B$BI want to "
                       "show you a new spell, Frostbolt. It strikes your foe with frost and slows it down.$B$BI want "
                       "you try it. Look for a training dummy near the southeastern edge of Aldrassil."},
    26968: {"Details": "In your future as a mage, you'll be expected to master a wide variety of spells. In fact, I want "
                       "to teach you one right now. It's called Frostbolt and it strikes your opponent with frost, "
                       "slowing its approach.$B$BI want you to try out this technique using the training dummies to "
                       "the northwest of the Crash Site."},
    24527: {"Details": "Excellent!  Let us begin.$b$bThe first skill you will learn is that of the Earth Shock.  The "
                       "spirits of earth, when called upon, will strike your foe with a jolt of their power.$b$b"
                       "Helpful, isn't it?"},
    25143: {"Details": "I will teach you the art of the earth shock.  By calling on the earth, you can strike your foes "
                       "from afar and break their concentration.  Speak with me again and I will show you the way.$B$B"
                       "After your lessons are complete, practice using the training dummies outside the Den."},
    25139: {"Details": "You already know how to loose an arrow.  Good.  But a single shot rarely brings down your prey. "
                       " I can teach you a sting that keeps hurting it long after the arrow lands."},
    24784: {"Objectives": "Reach level 4 and learn 'Lesser Heal' from {giver}. Practice casting Lesser Heal 3 times on "
                          "Wounded Darkspear Watchers.",
            "ObjectiveText1": "Practice Lesser Heal on Wounded Darkspear Watcher"},
    24766: {"Objectives": "Speak to {giver} to train Rejuvenation. Practice using Rejuvenation on a Wounded Darkspear "
                          "Watcher in the Valley of Trials."},
}
TEXT_FIELDS = ("Title", "Objectives", "Details", "EndText", "OfferRewardText", "RequestItemsText", "ObjectiveText1",
               "ObjectiveText2", "ObjectiveText3", "ObjectiveText4")
DUMMY_DISPLAYS = {32778: 3019}                   # Cataclysm's Coldridge dummy -> stock's dummy
# Cataclysm spells left out, with the rows that use them: the dummies' Arcane Missiles proc aura (83470) and death
# spell (71240; they can't die), the night elf quests' class skill tracker flag (92298)
DROP_SPELLS = {83470: 0, 71240: 0, 92298: 0}
DUMMY_SCRIPT = "npc_zep_training_dummy"
TABLES = ("quest_template", "quest_poi", "quest_poi_points", "creature_template", "creature", "creature_addon",
          "creature_template_addon", "creature_model_info", "creature_equip_template", "creature_text",
          "smart_scripts", "creature_questrelation", "creature_involvedrelation")


def load(world, cache):
    if cache and os.path.exists(cache) and os.path.getmtime(cache) > os.path.getmtime(world):
        return pickle.load(open(cache, "rb"))
    tabs = X.read_dump(world, {a[0] for a in AREAS.values()})
    t = {n: [r for r, _ in tabs[n].rows()] for n in TABLES}
    if cache:
        pickle.dump(t, open(cache, "wb"))
    return t


def acore_data(acore):
    """Stock trainer spawns (with F-029's), creature names, spell ranks."""
    base = os.path.join(acore, "data", "sql", "base", "db_world")
    read = lambda f: open(os.path.join(base, f), encoding="utf8").read()
    trainer = {int(i): (int(t), int(r)) for i, t, r in re.findall(r"^\((\d+),(\d+),(\d+),", read("trainer.sql"), re.M)}
    cdt = {int(c): int(t) for c, t in re.findall(r"^\((\d+),(\d+)\)", read("creature_default_trainer.sql"), re.M)}
    names = {int(e): n.replace("\\'", "'") for e, n in re.findall(
        r"^\((\d+),\d+,\d+,\d+,\d+,\d+,'((?:[^'\\]|\\.)*)'", read("creature_template.sql"), re.M)}
    spawns = [(int(e), int(m), float(x), float(y), "stock") for e, m, x, y in re.findall(
        r"^\(\d+,(\d+),\d+,\d+,(\d+),\d+,\d+,\d+,\d+,\d+,(-?[\d.]+),(-?[\d.]+)", read("creature.sql"), re.M)]
    for f in ("[F-029]_starting_area_trainers.sql", "[F-029]_worgen_class_trainers.sql"):
        text = open(os.path.join(F029, f), encoding="utf8").read()
        spawns += [(int(e), int(m), float(x), float(y), "F-029") for e, m, x, y in re.findall(
            r"^\(\d+, (\d+), (\d+), \d+, \d+, \d+, \d+, \d+, (-?[\d.]+), (-?[\d.]+)", text, re.M)]
        for e, n in re.findall(r"^\((\d+), \d+, \d+, \d+, \d+, \d+, '((?:[^']|'')*)'", text, re.M):
            names[int(e)] = n.replace("''", "'")
        block = re.search(r"INSERT INTO `creature_default_trainer`.*?;", text, re.S)
        cdt.update({int(c): int(t) for c, t in re.findall(r"^\((\d+), (\d+)\)", block.group(0) if block else "", re.M)})
    ranks = collections.defaultdict(list)
    first = {}
    for f, s, r in re.findall(r"^\((\d+),(\d+),(\d+)\)", read("spell_ranks.sql"), re.M):
        ranks[int(f)].append(int(s))
        first[int(s)] = int(f)
    klass = lambda e: trainer[cdt[e]][1] if e in cdt and cdt[e] in trainer and trainer[cdt[e]][0] == 0 else None
    return spawns, names, klass, {s: ranks[f] for s, f in first.items()}, cdt


def near(m, x, y, area):
    am, ax, ay = AREAS[area][:3]
    return m == am and math.hypot(x - ax, y - ay) < RADIUS


def area_of(m, x, y):
    return next((a for a in AREAS if near(m, x, y, a)), None)


class Port(G.Port):
    def __init__(self, t, dest):
        self.x, self.dest, self.files = None, dest, {}
        self.t = collections.defaultdict(list, t)
        self.stock_spells = G.dbc_ids("Spell") | G.modpak_spells()
        self.stock_sounds = G.dbc_ids("SoundEntries")
        self.stock_cdisp = G.dbc_ids("CreatureDisplayInfo")
        self.stock_extra = G.dbc_ids("CreatureDisplayInfoExtra")
        self.stock_models = G.dbc_ids("CreatureModelData")
        self.stock_gdisp = G.dbc_ids("GameObjectDisplayInfo")
        self.stock_ft = G.dbc_ids("FactionTemplate")
        self.stock_npcsounds = G.dbc_ids("NPCSounds")
        self.stock_soundData = G.dbc_ids("CreatureSoundData")
        self.items = G.CataItems(G.CATA_DBC, G.STOCK_DBC)
        self.entries = {r["entry"] for r in self.t["creature_template"]}
        self.goentries, self.quests = set(), {r["Id"] for r in self.t["quest_template"]}
        self.known_creatures = self.entries | set(t["givers"])
        self.cguid = {r["guid"]: CREATURE_GUID + i for i, r in enumerate(sorted(self.t["creature"],
                                                                                 key=lambda r: r["guid"]))}
        self.gguid, self.paths, self.menu, self.text = {}, {}, {}, {}
        self.item_ids, self.spells = {}, set()

    def neltharion_spells(self):
        pass

    def phasing(self):
        pass

    def spawns(self):
        c, a = [], []
        for r in sorted(self.t["creature"], key=lambda r: r["guid"]):
            c.append([self.cguid[r["guid"]], r["id"], r["map"], 0, 0, 1, 1, 0, r["position_x"], r["position_y"],
                      r["position_z"], r["orientation"], r["spawntimesecs"], 0, 0, 1, 0, 0, 0, 0, 0, "", 0, 1,
                      "[gen %s %s]" % (TAG, r["area"])])
        for r in self.t["creature_addon"]:
            g = self.cguid.get(r["guid"])
            if g:
                a.append([g, 0, r["mount"], r["bytes1"], r["bytes2"], r["emote"], 0,
                          self.auras(r["auras"], "spawn %d" % r["guid"]), ""])
        self.write("40_creature", G.insert(
            "creature", "guid id map zoneId areaId spawnMask phaseMask equipment_id position_x position_y position_z "
            "orientation spawntimesecs wander_distance currentwaypoint curhealth curmana MovementType npcflag "
            "unit_flags dynamicflags ScriptName VerifiedBuild CreateObject Comment".split(), c,
            "DELETE FROM `creature` WHERE `Comment` LIKE '[gen %s%%';" % TAG))
        self.write("41_creature_addon", G.insert(
            "creature_addon", "guid path_id mount bytes1 bytes2 emote visibilityDistanceType auras Comment".split(), a,
            "DELETE FROM `creature_addon` WHERE `guid` BETWEEN %d AND %d;" % (CREATURE_GUID, CREATURE_GUID + 9999)))

    def smart(self):
        # every rank of the practised spell gives credit, not only the one Cataclysm names; once per (spell, credit):
        # the areas' quests of a class share them
        seen = {}
        for q, s, npc in self.cast_credit:
            for r in self.t["ranks"].get(s, [s]):
                seen.setdefault((r, npc), q)
        self.cast_credit = [(q, r, npc) for (r, npc), q in seen.items()]
        super().smart()
        # the stock Injured Draenei has no SmartAI of its own
        rows = [[e, 0, 900 + i, 0, 8, 0, 100, 0, s, 0, 0, 0, 0, 0, 33, e, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0,
                 "quest %d: credit when hit by %d" % (q, s)]
                for i, (q, s, e) in enumerate(c for c in self.cast_credit if c[2] in STOCK_TARGETS)]
        if rows:
            cols = ("entryorguid source_type id link event_type event_phase_mask event_chance event_flags "
                    "event_param1 event_param2 event_param3 event_param4 event_param5 event_param6 action_type "
                    "action_param1 action_param2 action_param3 action_param4 action_param5 action_param6 target_type "
                    "target_param1 target_param2 target_param3 target_param4 target_x target_y target_z target_o "
                    "comment").split()
            ents = G.in_list({r[0] for r in rows})
            self.write("67_stock_target_credit", G.insert(
                "smart_scripts", cols, rows,
                "DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` IN %s AND `id` >= 900;" % ents)
                + "UPDATE `creature_template` SET `AIName` = 'SmartAI' WHERE `entry` IN %s;\n" % ents)

    def extras(self):
        """Zone and team conditions, the Valley of Trials druid trainer, the Garments quests."""
        cond = []
        for q, area in sorted(self.t["quest_area"].items()):
            team = 469 if AREAS[area][4] == G.CATA_ALLIANCE else 67
            cond.append([19, 0, q, 0, 0, 4, 0, AREAS[area][3], 0, 0, 0, 0, 0, "", "%s only" % area])
            cond.append([19, 0, q, 0, 0, 6, 0, team, 0, 0, 0, 0, 0, "", "%s only" % ("Alliance" if team == 469
                                                                                     else "Horde")])
        self.write("70_conditions", G.insert(
            "conditions", "SourceTypeOrReferenceId SourceGroup SourceEntry SourceId ElseGroup ConditionTypeOrReference "
            "ConditionTarget ConditionValue1 ConditionValue2 ConditionValue3 NegativeCondition ErrorType ErrorTextId "
            "ScriptName Comment".split(), cond,
            "DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId` = 19 AND `SourceEntry` IN %s;"
            % G.in_list(self.quests)))
        self.write("80_valley_druid_trainer",
                   "-- Zen'tabra (Echo Isles' troll druid trainer) stands where F-029 puts the tauren Gart Mistrunner "
                   "in the Valley of Trials,\n-- with the Horde druid trainer list and stock's Earth Mother gossip.\n"
                   "UPDATE `creature_template` SET `gossip_menu_id` = 4605, `AIName` = '' WHERE `entry` = %d;\n"
                   "UPDATE `creature` SET `id` = %d WHERE `guid` = %d;\n" % (TROLL_DRUID, TROLL_DRUID,
                                                                          F029_VALLEY_DRUID_GUID))
        self.write("81_second_town_trainers",
                   "-- Cataclysm's second-town trainers use the gossip of a stock trainer of their class and faction\n"
                   + "".join("UPDATE `creature_template` t JOIN `creature_template` s ON s.`entry` = %d "
                             "SET t.`gossip_menu_id` = s.`gossip_menu_id`, t.`AIName` = '' WHERE t.`entry` = %d;\n"
                             % (src, e) for e, src in sorted(SECOND_TOWN_TRAINERS.items())))
        self.write("85_priest_garments",
                   "-- The WotLK priest \"Garments of ...\" quests heal a wounded NPC as Healing the Wounded does; "
                   "Cataclysm replaced them\n-- with it, so their first-town trainers no longer offer them. The "
                   "\"In Favor of ...\" breadcrumbs there stay.\n"
                   "DELETE FROM `creature_queststarter` WHERE `quest` IN %s;\n" % G.in_list(GARMENTS))

    def run(self):
        self.trainers, self.faction_templates, self.bakes = [], set(), set()
        self.cast_credit, self.cast_credit_npcs = [], set()
        self.collect_spells()
        self.creatures()
        lists = dict(self.t["second_town_lists"])
        lists[TROLL_DRUID] = 34                                                    # Horde druid list
        self.trainers = [(e, lists.get(e, t)) for e, t in self.trainers]
        self.write("57_creature_default_trainer", G.insert(
            "creature_default_trainer", ["CreatureId", "TrainerId"], self.trainers,
            "DELETE FROM `creature_default_trainer` WHERE `CreatureId` IN %s;" % G.in_list(r[0] for r in self.trainers)))
        self.spawns()
        self.quests_()
        self.smart()
        self.extras()
        self.client_rows()
        if self.cast_credit_npcs:
            self.write("66_cast_credit_ai", "UPDATE `creature_template` SET `AIName` = 'SmartAI' WHERE `entry` IN %s;\n"
                       % G.in_list(self.cast_credit_npcs))
        for name, sql in self.files.items():
            path = os.path.join(self.dest, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf8", newline="\n") as f:
                f.write("-- Generated by tools/races/cata_class_quests_port.py from Project Neltharion's world "
                        "database: change the script, not this file.\n\n" + sql)
        print("ported: %d quests, %d creatures (%d spawns), %d spells, %d bakes" % (
            len(self.quests), len(self.entries), len(self.t["creature"]), len(self.spells), len(self.bakes)))
        for k, v in sorted(G.dropped.items()):
            v = sorted(set(map(str, v)))
            print("%s (%d): %s" % (k, len(v), ", ".join(v[:40]) + (" ..." if len(v) > 40 else "")))


def select(N, acore):
    spawns, names, klass, ranks, cdt = acore_data(acore)
    ct = {r["entry"]: r for r in N["creature_template"]}
    nspawn = collections.defaultdict(list)
    for r in N["creature"]:
        nspawn[r["id"]].append(r)
    starter = collections.defaultdict(list)
    for r in N["creature_questrelation"]:
        starter[r["quest"]].append(r["id"])
    stock_quests = set(int(q) for q in re.findall(r"^\((\d+),", open(os.path.join(
        acore, "data", "sql", "base", "db_world", "quest_template.sql"), encoding="utf8").read(), re.M))

    quests, quest_area = [], {}
    for q in N["quest_template"]:
        if q["Id"] in stock_quests or q["RequiredClasses"] not in CLASS_BITS or not 0 < (q["Level"] or 0) <= 10:
            continue
        if not any(q["RequiredSpellCast%d" % i] for i in range(1, 5)):
            continue
        area = TRANSPLANT.get(q["Id"]) or next((area_of(s["map"], s["position_x"], s["position_y"])
                                                for e in starter[q["Id"]] for s in nspawn[e]
                                                if area_of(s["map"], s["position_x"], s["position_y"])), None)
        if area:
            quests.append(dict(q))
            quest_area[q["Id"]] = area

    # givers: the trainers of the quest's class standing in its area here
    givers, rel, by_quest = set(), [], {}
    for q in quests:
        area, cls = quest_area[q["Id"]], CLASS_BITS[q["RequiredClasses"]]
        found = sorted({e for e, m, x, y, src in spawns if near(m, x, y, area) and klass(e) == cls}
                       - GENERIC_TRAINERS)
        if cls == 11 and area == "Valley of Trials":
            found = [TROLL_DRUID]
        if not found:
            sys.exit("no %d trainer in %s for quest %d" % (cls, area, q["Id"]))
        by_quest[q["Id"]] = found
        givers |= set(found) - {TROLL_DRUID}
        rel += [dict(id=e, quest=q["Id"]) for e in found]

    # texts: Cataclysm's trainer names -> this area's, swapped spells, the fixes
    for q in quests:
        found = by_quest[q["Id"]]
        giver = names.get(found[0], ct.get(found[0], {}).get("name")) if len(found) == 1 else "your trainer"
        old = {ct[e]["name"] for e in starter[q["Id"]] if e in ct} | set(OTHER_NAMES)
        for k in TEXT_FIELDS:
            v = q.get(k) or ""
            for o in sorted(old, key=len, reverse=True):
                v = v.replace(o, giver)
            for a, b in TEXT_SWAP:
                v = v.replace(a, b)
            q[k] = v
        for k, v in TEXT_FIXES.get(q["Id"], {}).items():
            q[k] = v.format(giver=giver)
        q["Objectives"] = q["Objectives"].replace("Injured Employees", "Wounded Darkspear Watchers")

    # targets: the quest NPCs, and the dummies whose KillCredit names them, spawned in the quest's area
    entries, cspawns = {CREDIT, TROLL_DRUID}, []
    for q in quests:
        area = quest_area[q["Id"]]
        for i in range(1, 5):
            npc = q["RequiredNpcOrGo%d" % i]
            if npc <= 0 or npc in STOCK_TARGETS:
                continue
            entries.add(npc)
            for e, r in ct.items():
                if npc not in (e, r["KillCredit1"], r["KillCredit2"]):
                    continue
                here = [s for s in nspawn[e] if near(s["map"], s["position_x"], s["position_y"], area)]
                if here:
                    entries.add(e)
                    cspawns += [dict(s, area=area) for s in here]
    # the second towns' Cataclysm trainers, where they stood in 4.3.4
    for e in SECOND_TOWN_TRAINERS:
        entries.add(e)
        for s in nspawn[e]:
            town = next((t for t, (m, x, y) in SECOND_TOWNS.items() if s["map"] == m
                         and math.hypot(s["position_x"] - x, s["position_y"] - y) < RADIUS), None)
            if town:
                cspawns.append(dict(s, area=town))
    cspawns = list({s["guid"]: s for s in cspawns}.values())
    # Echo Isles' wounded watchers: three yards from each Valley of Trials dummy
    dummies = sorted((s for s in cspawns if s["area"] == "Valley of Trials" and s["id"] != 47057),
                     key=lambda s: s["guid"])
    for n, s in enumerate(d for d in dummies if ct[d["id"]]["name"] == "Training Dummy"):
        a = s["orientation"] + math.pi / 2
        cspawns.append(dict(s, guid=9000000 + n, id=47057, position_x=s["position_x"] + 3 * math.cos(a),
                            position_y=s["position_y"] + 3 * math.sin(a), area="Valley of Trials"))
    cspawns = list({s["guid"]: s for s in cspawns}.values())

    # quests: level 4, the swapped spells, faction-wide, one per class, no chain
    group = {}
    for q in sorted(quests, key=lambda q: q["Id"]):
        group.setdefault(q["RequiredClasses"], q["Id"])
    for q in quests:
        q.update(Level=4, MinLevel=4, RequiredRaces=0, PrevQuestId=0, NextQuestId=0,
                 NextQuestIdChain=0, ExclusiveGroup=group[q["RequiredClasses"]])
        for i in range(1, 5):
            q["RequiredSpellCast%d" % i] = SPELL_SWAP.get(q["RequiredSpellCast%d" % i], q["RequiredSpellCast%d" % i])

    tmpl = []
    for e in sorted(entries):
        r = dict(ct[e])
        if r["ScriptName"] == "npc_training_dummy":
            r["ScriptName"] = DUMMY_SCRIPT
            for k in ("modelid1", "modelid2", "modelid3", "modelid4"):
                r[k] = DUMMY_DISPLAYS.get(r[k], r[k])
        tmpl.append(r)
    # Neltharion's own SmartAI on the dummies and wounded NPCs is left out: its credit rows name the wrong credit or
    # double the generated ones, and the rest is Cataclysm's (actions 88/99, the tiki masks, a despawn on heal).
    # The port's cast credit rows are all they need
    smart = []
    guids = {s["guid"] for s in cspawns}
    keep = lambda t, k, ids: [r for r in N[t] if r[k] in ids]
    transplanted = set(TRANSPLANT)
    qids = {q["Id"] for q in quests}
    return dict(
        quest_template=quests, creature_template=tmpl, creature=cspawns,
        creature_addon=keep("creature_addon", "guid", guids),
        creature_template_addon=keep("creature_template_addon", "entry", entries),
        creature_model_info=[r for r in N["creature_model_info"] if r["modelid"] in
                             {r[k] for r in tmpl for k in ("modelid1", "modelid2", "modelid3", "modelid4")}],
        creature_equip_template=keep("creature_equip_template", "entry", entries),
        creature_text=keep("creature_text", "entry", entries - {TROLL_DRUID}),
        smart_scripts=smart,
        quest_poi=[r for r in N["quest_poi"] if r["questId"] in qids - transplanted],
        quest_poi_points=[r for r in N["quest_poi_points"] if r["questId"] in qids - transplanted],
        creature_questrelation=rel, creature_involvedrelation=rel,
        givers=givers, quest_area=quest_area, ranks=ranks,
        second_town_lists={e: cdt[src] for e, src in SECOND_TOWN_TRAINERS.items()})


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("world")
    ap.add_argument("dest")
    ap.add_argument("--acore", default="D:/GitHub/azerothcore-wotlk-256-bit")
    ap.add_argument("--cache", default="D:/wow-scratch/cata-classquests/neltharion.pickle")
    a = ap.parse_args()
    # cata_gilneas_port's Gilneas specifics off
    G.TAG, G.STOCK_CREATURES, G.STOCK_GAMEOBJECTS, G.STOCK_QUESTS = TAG, set(), set(), set()
    G.SCRIPTS, G.DEAD_SCRIPTS, G.SCRIPT_SPELLS, G.SCRIPT_CREATURES = {DUMMY_SCRIPT}, set(), set(), set()
    G.FIXED_SPELLS, G.SPELL_SUBSTITUTES, G.SOURCE_MAPS, G.CATA_MODELS = set(), DROP_SPELLS, (), ()
    import glob
    for old in (glob.glob(os.path.join(a.dest, G.SQL_DIR, "zz_[[]AUTO,%s[]]_*.sql" % TAG))
                + glob.glob(os.path.join(a.dest, "dbc", "[[]%s[]]_*.sql" % TAG))):
        os.remove(old)
    Port(select(load(a.world, a.cache), a.acore), a.dest).run()

"""Mists of Pandaria spells for 3.3.5a: Spell.dbc rows from the 5.4.8 (18414) client's split spell tables.

  spells = MopSpells(MOP_DBC, STOCK_DBC, DATA_DIR, have, taken)
  spells.port(ids)        -> {MoP id: id here} for every spell ported (the closure of triggered spells included)
  spells.files(prefix)    -> {file name: SQL} (spell, spellicon, spellduration, spellcasttimes, summonproperties)

DATA_DIR holds wago.tools' English SpellName.csv and Spell.csv of 5.5.4.70449 (the 5.4.8 strings are ruRU).
have: spell ids that already exist here (stock, config.sql); they're used as they are and not ported.
taken: spell ids other modpaks write as other spells; a MoP spell with one of those ids moves to SPELL_BASE and up.

5.4.8 layouts, as checked against 4.0.6a on spells both clients have (116, 1459, 8690, 46598, 5185, ...):
- Spell (25): names 1-4, then sub-table ids: aura options 10, casting requirements 12, categories 13, class options 14,
  cooldowns 15, equipped items 16, interrupts 17, levels 18, target restrictions 22, misc 24
- SpellMisc (26): attributes 0-13 at 3-16, cast time 17, duration 18, range 19, speed 20, visuals 21-22, icons 23-24,
  school 25
- SpellEffect (30): 4.0.6a's fields with the difficulty inserted at 1 (effect 2 ... trigger 23), then 24 (scaling),
  target A 25, target B 26, spell 27, index 28; only difficulty 0 rows are read
- categories, cooldowns, interrupts, levels, equipped items and aura options insert the spell id and difficulty at 1-2,
  so 4.0.6a's fields are two later; target restrictions also insert two floats (radius, width) before max targets
- SpellRadius has one more field before the max radius; SpellCastTimes, SpellDuration, SummonProperties and the
  SpellRange values match stock

Rules:
- the 3.3.5a attributes are MoP's first eight words; effects 3+ are left out (reported)
- visuals keep MoP's ids (SpellMisc 21-22); the caller ports the rows (mop_wandering_isle_port.MopVisuals) and clears
  the ones it can't
- icons stock lacks are added (the BLPs are listed by icon_files()); duration rows stock lacks are added; cast time,
  range and radius indices map to the stock row with the same values, else the nearest larger one
- spells using effects, auras or targets 3.3.5a lacks are left out and reported; invisibility / detection types keep
  MoP's numbers (5-30 on the island), which needs the F-134 core patch's 32 invisibility types (stock has 12)
- phase auras (261): MoP's phase id becomes the port's phasemask bit (phase_bit)
- creature entries in summon / kill credit effects go through entry() (the port's moved entries)
"""
import collections, csv, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cata406_dbc_port as c406  # noqa: E402

SPELL_BASE = 13400000
ICON_BASE = 13400000
DURATION_BASE = 1340
SP = dict(auraopt=10, castreq=12, categories=13, classopt=14, cooldowns=15, equipped=16, interrupts=17, levels=18,
          targetres=22, misc=24)
EF = dict(effect=2, multiple_value=3, aura=4, amplitude=5, base_points=6, bonus_multiplier=7, damage_multiplier=8,
          chain_target=9, die_sides=10, item_type=11, mechanic=12, misc_a=13, misc_b=14, points_per_combo_point=15,
          radius=16, radius_max=17, real_points_per_level=18, mask_a=19, mask_b=20, mask_c=21, trigger=23,
          target_a=25, target_b=26, spell=27, index=28)
SUMMON_EFFECTS = {28, 56, 41, 42, 112}
CREDIT_EFFECTS = {90, 134}
INVISIBILITY_AURAS = {16, 18, 19}
PHASE_AURA = 261
PHASE_GROUP_AURA = 326          # MoP: every phase of PhaseXPhaseGroup group MiscValueB
TARGET_TAP_LIST = 123           # MoP: everyone who tapped the caster; 3.3.5a: enemies around it (TAP_LIST_RADIUS)
TARGET_SRC_CASTER, TARGET_UNIT_SRC_AREA_ENEMY = 22, 15
TAP_LIST_RADIUS = 50.0
# MoP effects with a script in the core's wandering_isle.cpp instead (effect, aura written, script name)
SCRIPTED_EFFECTS = {165: (2, "spell_gen_damage_from_max_health_pct"),     # damage from max health %: school damage
                    167: (3, "spell_gen_update_zone_auras_and_phases"),   # update player phase
                    170: (3, "spell_gen_update_zone_auras_and_phases")}   # update zone auras and phases
SET_VEHICLE_AURA = 296
MAX_INVISIBILITY = 32          # the F-134 core patch's TOTAL_INVISIBILITY_TYPES (stock 12)
# MoP types past it, moved to ones the island doesn't use (its spells and objects use 5, 7-9, 12-28, 30)
INVISIBILITY_REMAP = {34: 29, 35: 31, 36: 10, 37: 11}
MAX_EFFECT, MAX_AURA, MAX_TARGET = c406.MAX_EFFECT, c406.MAX_AURA, c406.MAX_TARGET
# Ids below 3.3.5a's limits mean the same in Cataclysm (TrinityCore 4.3.4's enums against AzerothCore's) and MoP, which
# only appended, except these: aura 128 is Fixate (3.3.5a: possess pet), effect 45 Play Movie (3.3.5a: add honor)
AURA_MEANING_DIFFERS = {128}
EFFECT_MEANING_DIFFERS = {45}


class MopSpells:
    def __init__(self, mop, stock, data, have, taken, phase_bit=None, entry=None, vehicle=None):
        self.m = lambda n: c406.Dbc(os.path.join(mop, n + ".dbc"))
        self.s = lambda n: c406.Dbc(os.path.join(stock, n + ".dbc"))
        self.have, self.taken = set(have), set(taken)
        self.phase_bit = phase_bit or {}
        self.entry = entry or (lambda e: e)
        self.vehicle = vehicle or (lambda v: v)
        self.spell, self.misc = self.m("Spell"), self.m("SpellMisc")
        self.sub = {k: self.m(n) for k, n in (
            ("auraopt", "SpellAuraOptions"), ("castreq", "SpellCastingRequirements"), ("categories", "SpellCategories"),
            ("classopt", "SpellClassOptions"), ("cooldowns", "SpellCooldowns"), ("equipped", "SpellEquippedItems"),
            ("interrupts", "SpellInterrupts"), ("levels", "SpellLevels"), ("targetres", "SpellTargetRestrictions"))}
        self.effects = collections.defaultdict(dict)
        for e in self.m("SpellEffect").records:
            if e[1] == 0:
                self.effects[e[EF["spell"]]].setdefault(e[EF["index"]], e)
        csv.field_size_limit(1 << 24)
        self.names = self._csv(os.path.join(data, "SpellName.csv"), "Name_lang")
        self.text = {}
        with open(os.path.join(data, "Spell.csv"), encoding="utf8", newline="") as f:
            for r in csv.DictReader(f):
                self.text[int(r["ID"])] = (r["NameSubtext_lang"], r["Description_lang"], r["AuraDescription_lang"])
        self.icons_m, self.icons_s = self.m("SpellIcon"), self.s("SpellIcon")
        self.idx = {k: (self.m(n), self.s(n)) for k, n in (("cast", "SpellCastTimes"), ("dur", "SpellDuration"),
                                                           ("rng", "SpellRange"), ("radius", "SpellRadius"),
                                                           ("summon", "SummonProperties"))}
        self.map = {}                 # MoP spell -> id here
        self.rows = {}                # id here -> columns
        self.dropped = collections.defaultdict(list)
        self.out = collections.defaultdict(dict)   # table -> {id: columns}
        self.icon_map, self.index_map = {}, {}
        self.summons = set()
        self.scripts = {}                 # MoP spell -> script names its replaced effects need
        self.group_masks = {}
        self.phase_groups = {}
        for r in self.m("PhaseXPhaseGroup").records:     # id, phase, group
            self.phase_groups.setdefault(r[2], []).append(r[1])

    @staticmethod
    def _csv(path, col):
        with open(path, encoding="utf8", newline="") as f:
            return {int(r["ID"]): r[col] for r in csv.DictReader(f)}

    # ---- index tables -------------------------------------------------------------------------------------------
    def _values(self, kind, row, mop=True):
        if kind == "radius":                       # MoP has one more field before the max radius
            return (c406.f32(row[1]), c406.f32(row[2]), c406.f32(row[4 if mop else 3]))
        if kind == "rng":
            return tuple(c406.f32(v) for v in row[1:5])
        return tuple(row[1:])

    def index(self, kind, mid):
        """Stock index row for a MoP one: same id with the same values, else the same values, else the nearest
        larger (cast, range, radius) or a new row (duration, summon properties)."""
        if not mid:
            return 0
        key = (kind, mid)
        if key in self.index_map:
            return self.index_map[key]
        m, s = self.idx[kind]
        r = m.get(mid)
        if not r:
            self.index_map[key] = 0
            return 0
        want = self._values(kind, r)
        stock = {x[0]: self._values(kind, x, mop=False) for x in s.records}
        if stock.get(mid) == want:
            out = mid
        elif want in stock.values():
            out = min(i for i, v in stock.items() if v == want)
        elif kind in ("dur", "summon"):
            out = mid if mid not in stock and mid not in self.out[kind] else DURATION_BASE + len(self.out[kind])
            names = (("id", "base_duration", "per_level", "max_duration") if kind == "dur" else
                     ("id", "control", "faction", "title", "slot", "flags"))
            self.out[kind][out] = dict(zip(names, (out,) + tuple(r[1:6])))
        else:
            first = {"cast": 0, "rng": 2, "radius": 0}[kind]   # compare base cast time / max range / radius
            bigger = sorted((v[first], i) for i, v in stock.items() if v[first] >= want[first])
            out = bigger[0][1] if bigger else max(stock, key=lambda i: stock[i][first])
        self.index_map[key] = out
        return out

    def icon(self, mid):
        if not mid:
            return 0
        if mid in self.icon_map:
            return self.icon_map[mid]
        r = self.icons_m.get(mid)
        if not r:
            return 0
        path = self.icons_m.s(r[1])
        s = self.icons_s.get(mid)
        if s and self.icons_s.s(s[1]).lower() == path.lower():
            out = mid
        elif not s and mid not in self.taken_icons:
            out = mid
        else:
            out = ICON_BASE + len([1 for v in self.icon_map.values() if v >= ICON_BASE])
        if not s or out != mid:
            self.out["icon"][out] = {"id": out, "name": path}
        self.icon_map[mid] = out
        return out

    taken_icons = set()

    def stock_radius(self, yards):
        """The stock SpellRadius row of exactly `yards`, else the nearest larger."""
        rows = [(c406.f32(r[1]), r[0]) for r in self.idx["radius"][1].records]
        return min((r for r in rows if r[0] >= yards), default=max(rows))[1]

    # ---- spells -------------------------------------------------------------------------------------------------
    def port(self, ids):
        todo = [i for i in ids if i and i not in self.have]
        seen = set()
        while todo:
            sid = todo.pop()
            if sid in seen or sid in self.have:
                continue
            seen.add(sid)
            triggers = self._spell(sid)
            todo += [t for t in triggers if t not in self.have]
        # a spell whose trigger was dropped keeps its other effects; the trigger id is cleared
        for row in self.rows.values():
            for n in (1, 2, 3):
                t = row.get("effect_trigger_spell_%d" % n)
                if t and t not in self.have and not (t in self.rows and t not in self.map):   # helpers stay
                    row["effect_trigger_spell_%d" % n] = self.map.get(t, 0)
        return dict(self.map)

    def _drop(self, why, sid):
        self.dropped[why].append(sid)
        return []

    def _spell(self, sid):
        r = self.spell.get(sid)
        if not r:
            return self._drop("spells the 5.4.8 client lacks", sid)
        misc = self.misc.get(r[SP["misc"]]) if r[SP["misc"]] else None
        if not misc:
            return self._drop("spells without a SpellMisc row", sid)
        effects = self.effects.get(sid, {})
        triggers, effs = [], []
        for i in sorted(effects):
            e = effects[i]
            E = lambda k: e[EF[k]]
            target_a, target_b = E("target_a"), E("target_b")
            radius = self.index("radius", E("radius") or E("radius_max"))
            if TARGET_TAP_LIST in (target_a, target_b):
                target_a, target_b = TARGET_SRC_CASTER, TARGET_UNIT_SRC_AREA_ENEMY
                radius = self.stock_radius(TAP_LIST_RADIUS)
                self.dropped["tap list targets made enemies around the caster"].append(sid)
            if target_a > MAX_TARGET or target_b > MAX_TARGET:
                return self._drop("spells using targets 3.3.5a lacks", "%d (targets %d/%d)" % (sid, target_a, target_b))
            effect, aura = E("effect"), E("aura")
            if effect in SCRIPTED_EFFECTS:
                effect, name = SCRIPTED_EFFECTS[effect]
                aura = 0
                self.scripts.setdefault(sid, set()).add(name)
            elif effect > MAX_EFFECT:
                self.dropped["effects 3.3.5a lacks, made dummies"].append("%d effect %d" % (sid, effect))
                effect, aura = 3, 0
            if aura == PHASE_GROUP_AURA:
                group = self.phase_groups.get(E("misc_b"), ())
                mask = 0
                for ph in group:
                    mask |= 1 if ph == 169 else self.phase_bit.get(ph, 0)
                if not mask:
                    return self._drop("phase group auras of groups the island lacks", "%d (group %d)" % (sid, E("misc_b")))
                aura = PHASE_AURA
                self.group_masks[sid] = mask
            if aura > MAX_AURA:
                # e.g. 346 enable alternate power (the meditation and Shen-zin Su bars): the scripts count the ticks
                self.dropped["auras 3.3.5a lacks, made dummy auras"].append("%d aura %d" % (sid, aura))
                aura = 4
            if aura in AURA_MEANING_DIFFERS and effect in (6, 27, 35, 65, 119, 128, 129, 143):
                return self._drop("spells with auras whose 3.3.5a id means something else", "%d (aura %d)" % (sid, E("aura")))
            if effect in EFFECT_MEANING_DIFFERS:
                self.dropped["effects whose 3.3.5a id means something else (cleared)"].append("%d effect %d" % (sid, E("effect")))
                continue
            misc_a, misc_b = E("misc_a"), E("misc_b")
            if aura in INVISIBILITY_AURAS and misc_a >= MAX_INVISIBILITY:
                if misc_a not in INVISIBILITY_REMAP:
                    return self._drop("invisibility types past the core's limit", "%d (type %d)" % (sid, misc_a))
                misc_a = INVISIBILITY_REMAP[misc_a]
            if aura == PHASE_AURA and sid in self.group_masks:
                misc_a, misc_b = self.group_masks[sid], 0
            elif aura == PHASE_AURA:
                phase = misc_b or misc_a                  # 5.4.8 keeps the phase id in MiscValueB (102515: 504)
                if phase not in self.phase_bit:
                    return self._drop("phase auras of phases the island lacks", "%d (phase %d)" % (sid, phase))
                misc_a, misc_b = self.phase_bit[phase], 0
            if aura == SET_VEHICLE_AURA:                 # the player becomes a MoP vehicle (None Left Behind: 1845)
                misc_a = self.vehicle(misc_a)
            if E("effect") in SUMMON_EFFECTS or E("effect") in CREDIT_EFFECTS:
                misc_a = self.entry(misc_a)
                if E("effect") in SUMMON_EFFECTS:
                    self.summons.add(misc_a)
                    if E("effect") == 28:
                        misc_b = self.index("summon", misc_b) or 64
            if E("trigger"):
                triggers.append(E("trigger"))
            effs.append({
                "effect": effect, "die_sides": E("die_sides"),
                "real_points_per_level": c406.f32(E("real_points_per_level")), "base_points": E("base_points"),
                "mechanic": E("mechanic"), "implicit_target_a": target_a, "implicit_target_b": target_b,
                "radius_index": radius, "apply_aura_name": aura,
                "amplitude": E("amplitude"), "multiple_value": c406.f32(E("multiple_value")),
                "chain_target": E("chain_target"), "item_type": E("item_type"), "misc_value_a": misc_a,
                "misc_value_b": misc_b, "trigger_spell": E("trigger"),
                "points_per_combo_point": c406.f32(E("points_per_combo_point")),
                "spell_class_mask_a": c406.u32(E("mask_a")), "spell_class_mask_b": c406.u32(E("mask_b")),
                "spell_class_mask_c": c406.u32(E("mask_c")), "damage_multiplier": c406.f32(E("damage_multiplier")),
                "bonus_multiplier": c406.f32(E("bonus_multiplier")),
            })
        new = sid if sid not in self.taken else self._new_id()
        name = self.names.get(sid, "")
        sub, desc, tip = self.text.get(sid, ("", "", ""))
        c = {"id": new}
        for i, col in enumerate(("attributes", "attributes_ex_1", "attributes_ex_2", "attributes_ex_3",
                                 "attributes_ex_4", "attributes_ex_5", "attributes_ex_6", "attributes_ex_7")):
            c[col] = c406.u32(misc[3 + i])
        c.update({
            "cast_time_index": self.index("cast", misc[17]) or 1,
            "duration_index": self.index("dur", misc[18]),
            "range_index": self.index("rng", misc[19]) or 1,
            "speed": c406.f32(misc[20]),
            "spell_visual_1": misc[21], "spell_visual_2": misc[22],
            "spell_icon_id": self.icon(misc[23]) or 1,
            "active_icon_id": self.icon(misc[24]),
            "school_mask": misc[25],
            "spell_name_enus": name, "spell_subtext_enus": sub, "spell_desc_enus": desc, "spell_tooltip_enus": tip,
            "proc_chance": 101, "equipped_item_class": -1, "damage_class": 0,
        })
        g = lambda k: self.sub[k].get(r[SP[k]]) if r[SP[k]] else None
        if (x := g("auraopt")):
            c.update(stack_amount=x[3], proc_chance=x[4], proc_charges=x[5], proc_flags=c406.u32(x[6]))
        if (x := g("castreq")):
            c.update(facing_caster_flags=x[1])
        if (x := g("categories")):
            c.update(category=x[3], damage_class=x[4], dispel=x[5], mechanic=x[6], prevention_type=x[7],
                     start_recovery_category=x[8])
        if (x := g("classopt")):
            c.update(spell_class_mask_1=c406.u32(x[2]), spell_class_mask_2=c406.u32(x[3]),
                     spell_class_mask_3=c406.u32(x[4]), spell_class_set=x[6])
        if (x := g("cooldowns")):
            c.update(category_recovery_time=x[3], recovery_time=x[4], start_recovery_time=x[5])
        if (x := g("equipped")):
            c.update(equipped_item_class=x[3], equipped_item_inventorytype_mask=x[4], equipped_item_subclass_mask=x[5])
        if (x := g("interrupts")):
            c.update(aura_interrupt_flags=c406.u32(x[3]), channel_interrupt_flags=c406.u32(x[5]), interrupt_flags=x[7])
        if (x := g("levels")):
            c.update(base_level=x[3], max_level=x[4], spell_level=x[5])
        if (x := g("targetres")):
            c.update(max_affected_targets=x[5], maximum_target_level=x[6], target_creature_type=x[7],
                     targets=c406.u32(x[8]))
        self.map[sid] = new
        self.rows[new] = c
        self._place(c, effs)
        return triggers

    def _new_id(self):
        self.next_id = getattr(self, "next_id", SPELL_BASE) + 1
        return self.next_id - 1

    def _place(self, c, effs, part=1):
        """Write effects into the 3 slots; past three, slot 3 triggers a helper spell carrying the rest (like F-002's
        druid Arcane Torrent), aimed like the first effect it carries."""
        if len(effs) > 3:
            helper = {k: v for k, v in c.items() if not k.startswith("effect_") and k not in (
                "category", "category_recovery_time", "recovery_time", "start_recovery_time",
                "start_recovery_category", "spell_icon_id", "active_icon_id", "spell_desc_enus", "spell_tooltip_enus",
                "spell_visual_1", "spell_visual_2")}
            hid = self._new_id()
            helper.update(id=hid, cast_time_index=1, spell_icon_id=1,
                          spell_name_enus="%s (part %d)" % (c["spell_name_enus"].split(" (part ")[0], part + 1),
                          attributes=helper.get("attributes", 0) | 0x80 | 0x100)       # passive-like: hidden, no log
            self.rows[hid] = helper
            self._place(helper, effs[2:], part + 1)
            effs = effs[:2] + [{"effect": 64, "trigger_spell": hid, "implicit_target_a": effs[2]["implicit_target_a"],
                                "implicit_target_b": effs[2]["implicit_target_b"],
                                "radius_index": effs[2]["radius_index"], "multiple_value": 1.0,
                                "damage_multiplier": 1.0, "bonus_multiplier": 1.0}]
            self.dropped["spells split into a helper for effects past the third"].append("%d -> %d" % (c["id"], hid))
        for n, e in enumerate(effs, 1):
            c.update({("effect_%d" % n) if k == "effect" else "effect_%s_%d" % (k, n): v for k, v in e.items()})

    # ---- output -------------------------------------------------------------------------------------------------
    def icon_files(self):
        return sorted(r["name"] for r in self.out["icon"].values())

    def files(self, prefix, comment):
        out = {}
        tables = (("spell", self.rows, lambda c: "%d %s" % (c["id"], c["spell_name_enus"])),
                  ("spellicon", self.out["icon"], lambda c: c["name"]),
                  ("spellduration", self.out["dur"], lambda c: "%d ms" % c["base_duration"]),
                  ("summonproperties", self.out["summon"], lambda c: "summon properties"))
        for table, rows, label in tables:
            if rows:
                text = ["-- %s\n" % comment] + [c406.block(table, k, rows[k], label(rows[k])) for k in sorted(rows)]
                out["%s%s.sql" % (prefix, table)] = "\n".join(text)
        return out


if __name__ == "__main__":
    # self-check: spells 3.3.5a and 5.4.8 both have come out as stock's (Frostbolt 116 keeps its school, cast time,
    # range, chill effect and English name)
    here = os.path.dirname(os.path.abspath(__file__))
    refs = os.path.join(here, "..", "..", "..", "References")
    sp = MopSpells(os.path.join(refs, "MoP", "MoP_data", "dbc"), os.path.join(refs, "original-client-dbc"),
                   sys.argv[1] if len(sys.argv) > 1 else "D:/wow-scratch/wi/db2", have=(), taken=())
    sp.port([116])
    c = sp.rows[116]
    assert c["spell_name_enus"] == "Frostbolt" and c["school_mask"] == 16 and c["range_index"] == 5, c
    assert c["effect_1"] == 6 and c["effect_apply_aura_name_1"] == 33 and c["effect_2"] == 2, c
    assert c["cast_time_index"] == 5 and c["recovery_time"] == 0 and c["start_recovery_time"] == 1500, c
    # a spell with more than three effects: slot 3 triggers a hidden helper carrying the rest
    sp.port([113244])
    main = sp.rows[113244]
    helper = sp.rows[main["effect_trigger_spell_3"]]
    assert main["effect_3"] == 64 and helper["effect_1"] and helper["attributes"] & 0x80, (main, helper)
    print("ok")

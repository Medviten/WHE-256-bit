#!/usr/bin/env python3
"""Port Cataclysm 4.0.6a (build 13623) client DBC rows to WHE's 3.3.5a DBC SQL.

  python cata406_dbc_port.py CATA_DBC_DIR STOCK_DBC_DIR OUT_DIR PREFIX [options]

  --spell ID[,ID...]         Spell.dbc rows, assembled from Spell + SpellEffect + the Spell* sub-tables. Their visuals
                             (SpellVisual, SpellVisualKit, SpellVisualKitModelAttach, the SoundEntries they play and any
                             SpellVisualEffectName stock lacks) come along.
  --sound ID[,ID...]         SoundEntries rows
  --focus ID[,ID...]         SpellFocusObject rows
  --npc-sound ID[,ID...]     NPCSounds rows (a display's greeting, farewell and pissed voices) and their SoundEntries
  --display ID[,ID...]       CreatureDisplayInfo rows, for models stock already has
  --skip-kit ID[,ID...]      visual kits a modpak already has: referenced, not written again
  --effect-name OLD=NEW      use SpellVisualEffectName NEW (a stock model) in place of Cata's OLD
  --no-sound ID[,ID...]      leave these sounds out of the visuals (0), e.g. when the client has no file for them
  --sound-map OLD=NEW        play stock sound NEW in the visuals in place of Cata's OLD
  --sound-ext OLD=NEW        rename the sound files' extension, e.g. .wav=.ogg when the files come from a client that
                             ships them as Ogg Vorbis

Writes OUT_DIR/PREFIX_<table>.sql for every table that has rows, in the DELETE + INSERT ... SET form of the other
modpak files, keeping the Cata ids. Every id is checked against the stock DBCs: a Cata id stock already uses for
something else stops the port, since writing it would replace a stock row.

Cata 4.0.6 layouts, as checked against stock 3.3.5a on rows both have:
- Spell.dbc (47 fields): the 3.3.5a attribute fields are 1-8 (4.0.6 adds Ex8 and Ex9 at 9-10); from the cast time
  index on, every field is one place before its 4.3.4 position (cast 11, duration 12, power 13, range 14, speed 15,
  visuals 16-17, icons 18-19, name 20, rank 21, description 22, tooltip 23, school 24), and the sub-table ids are
  aura options 30, casting requirements 33, categories 34, class options 35, cooldowns 36, equipped items 38,
  interrupts 39, levels 40, target restrictions 44.
- SpellEffect.dbc (26 fields) is the 4.3.4 layout, so its values are exact: 3.3.5a computes BasePoints + DieSides
  when DieSides is 1, and BasePoints alone when it is 0, so DieSides is copied as it is (0 for almost every row).
- SpellVisual (32) and SpellVisualEffectName (7) match 3.3.5a; SpellVisualKit has one more field, at 3;
  SpellVisualKitModelAttach and SoundEntries add fields at the end (14 and 34, against 10 and 30).
"""
import argparse, os, struct

SPELL = dict(cast=11, dur=12, power=13, rng=14, speed=15, vis1=16, vis2=17, icon=18, active=19, name=20, desc=22,
             tip=23, school=24, auraopt=30, castreq=33, categories=34, classopt=35, cooldowns=36, equipped=38,
             interrupts=39, levels=40, targetres=44)
EFFECT = dict(effect=1, multiple_value=2, aura=3, amplitude=4, base_points=5, bonus_multiplier=6,
              damage_multiplier=7, chain_target=8, die_sides=9, item_type=10, mechanic=11, misc_a=12, misc_b=13,
              points_per_combo_point=14, radius=15, radius_max=16, real_points_per_level=17, class_mask=18,
              trigger=21, target_a=22, target_b=23, spell=24, index=25)
KIT_EFFECTS = range(3, 15)  # head .. world effect, in the 3.3.5a layout
VISUAL_KITS = (1, 2, 3, 4, 5, 6, 14, 15, 22, 23, 24, 25)
# 3.3.5a has no SpellEffect / SpellAura beyond these
MAX_EFFECT, MAX_AURA, MAX_TARGET = 164, 316, 110


class Dbc:
    def __init__(self, path):
        data = open(path, "rb").read()
        _, n, self.fields, size, _ = struct.unpack("<4s4I", data[:20])
        self.strings = data[20 + n * size:]
        self.rows = {}
        for i in range(n):
            row = struct.unpack_from(f"<{self.fields}i", data, 20 + i * size)
            self.rows.setdefault(row[0], row)
        self.records = [struct.unpack_from(f"<{self.fields}i", data, 20 + i * size) for i in range(n)]

    def s(self, offset):
        return self.strings[offset:self.strings.index(b"\0", offset)].decode("utf-8")

    def get(self, key):
        return self.rows.get(key)


def f32(v):
    x = struct.unpack("<f", struct.pack("<i", v))[0]
    return float(f"{x:.7g}")


def u32(v):
    return v & 0xFFFFFFFF


def q(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "''") + "'"


def fmt(v):
    if isinstance(v, str):
        return q(v)
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)


def block(table, key, columns, comment):
    lines = [f"-- {comment}", f"DELETE FROM `{table}` WHERE `id` = {key};", f"INSERT INTO `{table}` SET"]
    items = list(columns.items())
    for i, (k, v) in enumerate(items):
        lines.append(f"  `{k}` = {fmt(v)}{';' if i == len(items) - 1 else ','}")
    return "\n".join(lines) + "\n"


class Port:
    def __init__(self, cata, stock, args):
        self.c = lambda name: Dbc(os.path.join(cata, name + ".dbc"))
        self.o = lambda name: Dbc(os.path.join(stock, name + ".dbc"))
        self.args = args
        self.out = {}            # table -> {id: (columns, comment)}
        self.effect_map = dict(map(int, x.split("=")) for x in args.effect_name)
        self.no_sound = set(args.no_sound)
        self.sound_map = dict(map(int, x.split("=")) for x in args.sound_map)
        self.sound_ext = tuple(args.sound_ext.split("=")) if args.sound_ext else None
        self.skip_kit = set(args.skip_kit)

    def add(self, table, key, columns, comment, stock):
        if stock.get(key):
            raise SystemExit(f"{table} {key} ({comment}) is a different row in stock 3.3.5a: give it a new id")
        self.out.setdefault(table, {})[key] = (columns, comment)

    # --- spells -------------------------------------------------------------------------------------------------
    def spells(self, ids):
        if not ids:
            return
        spell, effects = self.c("Spell"), self.c("SpellEffect")
        stock = self.o("Spell")
        sub = {k: self.c(n) for k, n in (("auraopt", "SpellAuraOptions"), ("castreq", "SpellCastingRequirements"),
                                         ("categories", "SpellCategories"), ("classopt", "SpellClassOptions"),
                                         ("cooldowns", "SpellCooldowns"), ("equipped", "SpellEquippedItems"),
                                         ("interrupts", "SpellInterrupts"), ("levels", "SpellLevels"),
                                         ("targetres", "SpellTargetRestrictions"))}
        known = {n: set(self.o(t).rows) for n, t in (("cast", "SpellCastTimes"), ("dur", "SpellDuration"),
                                                     ("rng", "SpellRange"), ("radius", "SpellRadius"))}
        by_spell = {}
        for e in effects.records:
            by_spell.setdefault(e[EFFECT["spell"]], {})[e[EFFECT["index"]]] = e
        for sid in ids:
            r = spell.get(sid)
            if not r:
                raise SystemExit(f"spell {sid} isn't in the Cata Spell.dbc")
            name = spell.s(r[SPELL["name"]])

            def index(kind, value, default):
                if value in known[kind] or value == 0:
                    return value
                print(f"spell {sid}: {kind} index {value} isn't in stock, using {default}")
                return default

            c = {"id": sid}
            for i, col in enumerate(("attributes", "attributes_ex_1", "attributes_ex_2", "attributes_ex_3",
                                     "attributes_ex_4", "attributes_ex_5", "attributes_ex_6", "attributes_ex_7")):
                c[col] = u32(r[1 + i])
            c.update({
                "cast_time_index": index("cast", r[SPELL["cast"]], 1),
                "duration_index": index("dur", r[SPELL["dur"]], 0),
                "range_index": index("rng", r[SPELL["rng"]], 1),
                "power_type": r[SPELL["power"]],
                "speed": f32(r[SPELL["speed"]]),
                "spell_visual_1": r[SPELL["vis1"]],
                "spell_visual_2": r[SPELL["vis2"]],
                "spell_icon_id": r[SPELL["icon"]],
                "active_icon_id": r[SPELL["active"]],
                "school_mask": r[SPELL["school"]],
                "spell_name_enus": name,
                "spell_desc_enus": spell.s(r[SPELL["desc"]]),
                "proc_chance": 101,
                "equipped_item_class": -1,
                "damage_class": 0,
            })
            tip = spell.s(r[SPELL["tip"]])
            if tip:
                c["spell_tooltip_enus"] = tip
            g = lambda k: sub[k].get(r[SPELL[k]]) if r[SPELL[k]] else None
            if (x := g("auraopt")):
                c.update(stack_amount=x[1], proc_chance=x[2], proc_charges=x[3], proc_flags=u32(x[4]))
            if (x := g("castreq")):
                c.update(facing_caster_flags=x[1], spell_focus_object=x[6])
            if (x := g("categories")):
                c.update(category=x[1], damage_class=x[2], dispel=x[3], mechanic=x[4], prevention_type=x[5],
                         start_recovery_category=x[6])
            if (x := g("classopt")):
                c.update(spell_class_mask_1=u32(x[2]), spell_class_mask_2=u32(x[3]), spell_class_mask_3=u32(x[4]),
                         spell_class_set=x[5])
            if (x := g("cooldowns")):
                c.update(category_recovery_time=x[1], recovery_time=x[2], start_recovery_time=x[3])
            if (x := g("equipped")):
                c.update(equipped_item_class=x[1], equipped_item_inventorytype_mask=x[2],
                         equipped_item_subclass_mask=x[3])
            if (x := g("interrupts")):
                c.update(aura_interrupt_flags=u32(x[1]), channel_interrupt_flags=u32(x[3]), interrupt_flags=x[5])
            if (x := g("levels")):
                c.update(base_level=x[1], max_level=x[2], spell_level=x[3])
            if (x := g("targetres")):
                c.update(max_affected_targets=x[1], maximum_target_level=x[2], target_creature_type=x[3],
                         targets=u32(x[4]))
            for i in range(3):
                e = by_spell.get(sid, {}).get(i)
                n = i + 1
                if not e:
                    continue
                E = lambda k: e[EFFECT[k]]
                if E("effect") > MAX_EFFECT or E("aura") > MAX_AURA or E("target_a") > MAX_TARGET \
                        or E("target_b") > MAX_TARGET:
                    raise SystemExit(f"spell {sid} effect {i}: effect {E('effect')} aura {E('aura')} targets "
                                     f"{E('target_a')}/{E('target_b')} don't exist in 3.3.5a")
                radius = E("radius") or E("radius_max")
                c.update({
                    f"effect_{n}": E("effect"),
                    f"effect_die_sides_{n}": E("die_sides"),
                    f"effect_real_points_per_level_{n}": f32(E("real_points_per_level")),
                    f"effect_base_points_{n}": E("base_points"),
                    f"effect_mechanic_{n}": E("mechanic"),
                    f"effect_implicit_target_a_{n}": E("target_a"),
                    f"effect_implicit_target_b_{n}": E("target_b"),
                    f"effect_radius_index_{n}": index("radius", radius, 0),
                    f"effect_apply_aura_name_{n}": E("aura"),
                    f"effect_amplitude_{n}": E("amplitude"),
                    f"effect_multiple_value_{n}": f32(E("multiple_value")),
                    f"effect_chain_target_{n}": E("chain_target"),
                    f"effect_item_type_{n}": E("item_type"),
                    f"effect_misc_value_a_{n}": E("misc_a"),
                    f"effect_misc_value_b_{n}": E("misc_b"),
                    f"effect_trigger_spell_{n}": E("trigger"),
                    f"effect_points_per_combo_point_{n}": f32(E("points_per_combo_point")),
                    f"effect_spell_class_mask_a_{n}": u32(e[18]),
                    f"effect_spell_class_mask_b_{n}": u32(e[19]),
                    f"effect_spell_class_mask_c_{n}": u32(e[20]),
                    f"effect_damage_multiplier_{n}": f32(E("damage_multiplier")),
                    f"effect_bonus_multiplier_{n}": f32(E("bonus_multiplier")),
                })
            self.add("spell", sid, c, f"{sid} {name}", stock)
            for v in (r[SPELL["vis1"]], r[SPELL["vis2"]]):
                if v:
                    self.visual(v, sid)

    # --- visuals ------------------------------------------------------------------------------------------------
    def visual(self, vid, sid):
        if not hasattr(self, "cV"):
            self.cV, self.cK, self.cE, self.cA = (self.c(n) for n in ("SpellVisual", "SpellVisualKit",
                                                                       "SpellVisualEffectName",
                                                                       "SpellVisualKitModelAttach"))
            self.oV, self.oK, self.oE, self.oA = (self.o(n) for n in ("SpellVisual", "SpellVisualKit",
                                                                       "SpellVisualEffectName",
                                                                       "SpellVisualKitModelAttach"))
            self.motions = set(self.o("SpellMissileMotion").rows)
        r = list(self.cV.get(vid))
        r[8] = self.effect_name(r[8])
        for i in (11, 12):
            r[i] = self.sound(r[i])
        if r[21] and r[21] not in self.motions:
            raise SystemExit(f"visual {vid}: missile motion {r[21]} isn't in stock")
        names = ("id precast_kit cast_kit impact_kit state_kit state_done_kit channel_kit has_missile missile_model "
                 "missile_path_type missile_dest_attachment missile_sound anim_event_sound_id flags caster_impact_kit "
                 "target_impact_kid missile_attachment missile_follow_ground_height missile_follow_drop_speed "
                 "missile_follow_approach missile_follow_ground_flags missile_motion missile_targeting_kit "
                 "instant_area_kit impact_area_kit persistent_area_kit missile_cast_offset_x missile_cast_offset_y "
                 "missile_cast_offset_z missile_impact_offset_x missile_impact_offset_y missile_impact_offset_z").split()
        c = {}
        for i, k in enumerate(names):
            c[k] = f32(r[i]) if i >= 26 else (u32(r[i]) if r[i] < 0 else r[i])
        self.add("spellvisual", vid, c, f"{vid} <- spell {sid}", self.oV)
        for i in VISUAL_KITS:
            if r[i] > 0:
                self.kit(r[i], vid)

    def kit(self, kid, vid):
        if kid in self.skip_kit or kid in self.out.get("spellvisualkit", {}):
            return
        k = self.cK.get(kid)
        w = list(k[:3] + k[4:])
        for i in KIT_EFFECTS:
            w[i] = self.effect_name(w[i])
        w[15] = self.sound(w[15])
        names = ["id", "start_anim_id", "anim_id", "head_effect", "chest_effect", "base_effect", "left_hand_effect",
                 "right_hand_effect", "breath_effect", "left_weapon_effect", "right_weapon_effect", "special_effect_1",
                 "special_effect_2", "special_effect_3", "world_effect", "sound_id", "shake_id", "char_proc_1",
                 "char_proc_2", "char_proc_3", "char_proc_4"]
        names += [f"char_param_{p}_{i}" for p in range(4) for i in range(1, 5)] + ["flags"]
        c = {k: (f32(v) if k.startswith("char_param") else u32(v) if v < 0 else v) for k, v in zip(names, w)}
        self.add("spellvisualkit", kid, c, f"{kid} <- visual {vid}", self.oK)
        for a in self.cA.records:
            if a[1] == kid:
                aid = a[0]
                c = dict(zip(("id", "parent_spell_vis_kit_id", "spell_vis_effect_name_id", "attachment_id"),
                             (aid, kid, self.effect_name(a[2]), u32(a[3]))))
                c.update(zip(("offset_x", "offset_y", "offset_z", "yaw", "pitch", "roll"), map(f32, a[4:10])))
                self.add("spellvisualkitmodelattach", aid, c, f"{aid} <- kit {kid}", self.oA)

    def effect_name(self, eid):
        if eid <= 0:
            return eid
        eid = self.effect_map.get(eid, eid)
        c, o = self.cE.get(eid), self.oE.get(eid)
        if o and (not c or o[2] and self.oE.s(o[2]).lower() == self.cE.s(c[2]).lower()):
            return eid  # stock has the same model
        if o:
            raise SystemExit(f"SpellVisualEffectName {eid} is {self.oE.s(o[2])} in stock but "
                             f"{self.cE.s(c[2])} in Cata: map it with --effect-name")
        cols = {"id": eid, "name": self.cE.s(c[1]), "file_name": self.cE.s(c[2]), "area_effect_size": f32(c[3]),
                "scale": f32(c[4]), "min_allowed_scale": f32(c[5]), "max_allowed_scale": f32(c[6])}
        self.add("spellvisualeffectname", eid, cols, f"{eid} {cols['file_name']}", self.oE)
        return eid

    # --- sounds and focus objects -------------------------------------------------------------------------------
    def sound(self, sid):
        if sid <= 0 or sid in self.no_sound:
            return 0 if sid in self.no_sound else sid
        sid = self.sound_map.get(sid, sid)
        if not hasattr(self, "cS"):
            self.cS, self.oS = self.c("SoundEntries"), self.o("SoundEntries")
        if self.oS.get(sid):
            return sid  # stock: the visual tables share their sound ids with Cata below 18020
        r = self.cS.get(sid)
        if not r:
            raise SystemExit(f"sound {sid} isn't in the Cata SoundEntries.dbc")
        c = {"id": sid, "sound_type": r[1], "name": self.cS.s(r[2])}
        for i in range(10):
            if r[3 + i]:
                c[f"file_{i + 1}"] = self.cS.s(r[3 + i])
                if self.sound_ext and c[f"file_{i + 1}"].lower().endswith(self.sound_ext[0].lower()):
                    c[f"file_{i + 1}"] = c[f"file_{i + 1}"][:-len(self.sound_ext[0])] + self.sound_ext[1]
                c[f"frequency_{i + 1}"] = r[13 + i]
        c.update({"base_dir": self.cS.s(r[23]), "volume": f32(r[24]), "flags": r[25], "min_distance": f32(r[26]),
                  "distance_cutoff": f32(r[27]), "eax_def": r[28], "advanced_id": 0})
        files = ", ".join(c[f"file_{i + 1}"] for i in range(10) if f"file_{i + 1}" in c)
        self.add("soundentries", sid, c, f"{sid} {c['name']} ({c['base_dir']}: {files})", self.oS)
        return sid

    def npc_sounds(self, ids):
        """NPCSounds rows (greeting, farewell, pissed and a spare sound) and the SoundEntries they play."""
        if not ids:
            return
        c, o = self.c("NPCSounds"), self.o("NPCSounds")
        for nid in ids:
            r = c.get(nid)
            if not r:
                raise SystemExit(f"NPCSounds {nid} isn't in the Cata NPCSounds.dbc")
            cols = {"id": nid}
            names = []
            for i in range(4):
                cols[f"sound_entry_{i + 1}"] = self.sound(r[1 + i])
                if r[1 + i]:
                    names.append(self.cS.s(self.cS.get(r[1 + i])[2]) if self.cS.get(r[1 + i]) else str(r[1 + i]))
            self.add("npcsounds", nid, cols, f"{nid} {', '.join(names)}", o)

    def focus(self, ids):
        if not ids:
            return
        c, o = self.c("SpellFocusObject"), self.o("SpellFocusObject")
        for fid in ids:
            name = c.s(c.get(fid)[1])
            self.add("spellfocusobject", fid, {"id": fid, "name_enus": name, "name_flags": 16712190}, f"{fid} {name}", o)

    def displays(self, ids):
        """CreatureDisplayInfo rows whose model stock has at the same id and path (Cata adds one field at the end)."""
        if not ids:
            return
        c, o = self.c("CreatureDisplayInfo"), self.o("CreatureDisplayInfo")
        cm, om = self.c("CreatureModelData"), self.o("CreatureModelData")
        names = ("id", "model_id", "sound_id", "extended_display_info_id", "creature_model_scale",
                 "creature_model_alpha", "texture_variation_1", "texture_variation_2", "texture_variation_3",
                 "portrait_texture_name", "blood_level", "blood_id", "npc_sound_id", "praticle_color_id",
                 "creature_geoset_data", "obj_effect_package_id")
        for did in ids:
            r = c.get(did)
            model = cm.s(cm.get(r[1])[2])
            if not om.get(r[1]) or om.s(om.get(r[1])[2]).lower() != model.lower():
                raise SystemExit(f"display {did}: model {r[1]} ({model}) isn't the same in stock")
            if r[3]:
                raise SystemExit(f"display {did} has extra display info {r[3]}, which isn't ported")
            cols = {}
            for i, k in enumerate(names):
                if 6 <= i <= 9:
                    cols[k] = c.s(r[i])
                elif k == "creature_model_scale":
                    cols[k] = f32(r[i])
                else:
                    cols[k] = r[i]
            for value, table in ((r[2], "CreatureSoundData"), (r[12], "NPCSounds")):
                if value and not self.o(table).get(value):
                    raise SystemExit(f"display {did}: {table} {value} isn't in stock")
            textures = ", ".join(t for t in (cols["texture_variation_1"], cols["texture_variation_2"],
                                             cols["texture_variation_3"]) if t)
            self.add("creaturedisplayinfo", did, cols, f"{did} {model} ({textures})", o)

    def write(self, out_dir, prefix, source):
        os.makedirs(out_dir, exist_ok=True)
        for table, rows in sorted(self.out.items()):
            text = [f"-- {table} rows ported from Cataclysm 4.0.6a (build 13623) by tools/races/cata406_dbc_port.py,",
                    f"-- {source}. Regenerate them with it rather than editing them here.", ""]
            text += [block(table, k, c, comment) for k, (c, comment) in sorted(rows.items())]
            path = os.path.join(out_dir, f"{prefix}_{table}.sql")
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(text))
            print(f"{path}: {len(rows)} rows")


def ids(text):
    out = []
    for part in text.split(","):
        lo, _, hi = part.partition("-")
        out += range(int(lo), int(hi or lo) + 1)
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cata")
    p.add_argument("stock")
    p.add_argument("out")
    p.add_argument("prefix")
    p.add_argument("--spell", type=ids, default=[])
    p.add_argument("--sound", type=ids, default=[])
    p.add_argument("--focus", type=ids, default=[])
    p.add_argument("--npc-sound", type=ids, default=[])
    p.add_argument("--display", type=ids, default=[])
    p.add_argument("--skip-kit", type=ids, default=[])
    p.add_argument("--no-sound", type=ids, default=[])
    p.add_argument("--effect-name", action="append", default=[])
    p.add_argument("--sound-map", action="append", default=[])
    p.add_argument("--sound-ext")
    p.add_argument("--source", default="see the modpak's readme")
    a = p.parse_args()
    port = Port(a.cata, a.stock, a)
    port.spells(a.spell)
    for s in a.sound:
        port.sound(s)
    port.npc_sounds(a.npc_sound)
    port.focus(a.focus)
    port.displays(a.display)
    port.write(a.out, a.prefix, a.source)


if __name__ == "__main__":
    main()

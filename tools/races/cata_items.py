"""Cataclysm items for 3.3.5a, from the 4.0.6a client's Item.db2, Item-sparse.db2 and ItemDisplayInfo.dbc.

Used by the starting-zone ports (zep_goblin_port.py for F-013, cata_gilneas_port.py for F-130):

  items = CataItems(CATA_DBC, STOCK_DBC)
  items.display(cata_item_id)       -> (display id, ItemDisplayInfo row to add or None when stock has it)
  items.template(cata_item_id, id)  -> item_template columns, in the column order AzerothCore's table has

Displays: an item keeps its Cataclysm display. When stock 3.3.5a has that id with the same content it is used as it
is, and so is a stock row with the same content under another id; when stock lacks the id the Cataclysm row is added under it (ids above stock's are Cataclysm's own, so every
modpak that ports the same display writes the same row); when stock has the id with other content the row goes to
DISPLAY_BASE and up. Fields that point at tables stock lacks rows for (helmet geoset visibility, item visuals, spell
visuals) are cleared.

Weapon damage and armour aren't stored in 4.x; the client works them out from the item level and quality with the
ItemDamage*, ItemArmor* and ArmorLocation tables, the same way as here (TrinityCore 4.3.4's ItemTemplate::GetDamage
and GetArmor). Patch 4.0.1 raised armour on all gear, so low-level pieces have several times their 3.3.5a armour; it
hardly matters at the levels these zones are played at. Durability is left at 0 (never breaks).

  python cata_items.py CATA_DBC STOCK_DBC ITEM_ID...   prints the rows, as a check
"""
import math, os, struct, sys

DISPLAY_BASE = 300000            # displays whose Cataclysm id stock uses for something else

# Item-sparse.db2 (4.0.6a, 131 fields): TrinityCore 4.3.4's ItemSparseEntry minus PriceRandomValue, PriceVariance and
# BuyCount (4.3.4 fields 4-6), so from BuyPrice on each index is 3 lower. TrinityCore skips field 111 (unknown); AreaID
# and the rest follow it.
SP = dict(quality=1, flags=2, flags2=3, buy=4, sell=5, inv=6, cls_mask=7, race_mask=8, ilvl=9, req_level=10,
          req_skill=11, req_skill_rank=12, req_spell=13, honor=14, city=15, rep_faction=16, rep_rank=17,
          max_count=18, stack=19, slots=20, stat_type=21, stat_value=31, scaling_dist=61, dmg_type=62, delay=63,
          range=64, spell=65, trigger=70, charges=75, cooldown=80, category=85, cat_cooldown=90, bonding=95,
          name=96, description=100, page=101, language=102, page_material=103, start_quest=104, lock=105,
          material=106, sheath=107, random_property=108, random_suffix=109, item_set=110, area=112, map=113,
          bag_family=114, totem=115, socket_color=116, socket_content=119, socket_bonus=122, gem=123,
          armor_dmg_mod=124, duration=125, limit_category=126, holiday=127, scaling_factor=128)
FLOAT_FIELDS = {SP["range"], SP["armor_dmg_mod"], SP["scaling_factor"]}

# Cataclysm stat types 3.3.5a doesn't have (mastery, and the 4.x extra-armor/resistance ids)
DROP_STATS = {49, 50, 51, 52, 53, 54, 55, 56, 57, 58}

INVTYPE_ROBE, INVTYPE_CHEST = 20, 5
ITEM_CLASS_WEAPON, ITEM_CLASS_ARMOR = 2, 4
ARMOR_SHIELD = 6
# weapon damage table by inventory type / subclass (caster variants by Flags2 0x200, "caster weapon")
WAND, BOW, GUN, CROSSBOW, THROWN = 19, 2, 3, 18, 16

ITEM_TEMPLATE_COLUMNS = """entry class subclass SoundOverrideSubclass name displayid Quality Flags FlagsExtra BuyCount
BuyPrice SellPrice InventoryType AllowableClass AllowableRace ItemLevel RequiredLevel RequiredSkill RequiredSkillRank
requiredspell requiredhonorrank RequiredCityRank RequiredReputationFaction RequiredReputationRank maxcount stackable
ContainerSlots stat_type1 stat_value1 stat_type2 stat_value2 stat_type3 stat_value3 stat_type4 stat_value4 stat_type5
stat_value5 stat_type6 stat_value6 stat_type7 stat_value7 stat_type8 stat_value8 stat_type9 stat_value9 stat_type10
stat_value10 ScalingStatDistribution ScalingStatValue dmg_min1 dmg_max1 dmg_type1 dmg_min2 dmg_max2 dmg_type2 armor
holy_res fire_res nature_res frost_res shadow_res arcane_res delay ammo_type RangedModRange spellid_1 spelltrigger_1
spellcharges_1 spellppmRate_1 spellcooldown_1 spellcategory_1 spellcategorycooldown_1 spellid_2 spelltrigger_2
spellcharges_2 spellppmRate_2 spellcooldown_2 spellcategory_2 spellcategorycooldown_2 spellid_3 spelltrigger_3
spellcharges_3 spellppmRate_3 spellcooldown_3 spellcategory_3 spellcategorycooldown_3 spellid_4 spelltrigger_4
spellcharges_4 spellppmRate_4 spellcooldown_4 spellcategory_4 spellcategorycooldown_4 spellid_5 spelltrigger_5
spellcharges_5 spellppmRate_5 spellcooldown_5 spellcategory_5 spellcategorycooldown_5 bonding description PageText
LanguageID PageMaterial startquest lockid Material sheath RandomProperty RandomSuffix block itemset MaxDurability area
Map BagFamily TotemCategory socketColor_1 socketContent_1 socketColor_2 socketContent_2 socketColor_3 socketContent_3
socketBonus GemProperties ArmorDamageModifier duration ItemLimitCategory HolidayId ScriptName FoodType DisenchantID
RequiredDisenchantSkill minMoneyLoot maxMoneyLoot flagsCustom VerifiedBuild""".split()

# ItemDisplayInfo.dbc columns as DBCTool names them (same 25-field layout in 3.3.5a and 4.0.6a)
DISPLAY_COLUMNS = """id left_model right_model left_model_texture right_model_texture icon_1 icon_2 geoset_group_1
geoset_group_2 geoset_group_3 flags spell_visual_id group_sound_index helmet_geoset_male helmet_geoset_female
upper_arm_texture lower_arm_texture hands_texture upper_torso_texture lower_torso_texture upper_leg_texture
lower_leg_texture foot_texture item_visual particle_colour_id""".split()
DISPLAY_STRINGS = {1, 2, 3, 4, 5, 6, 15, 16, 17, 18, 19, 20, 21, 22}


def read_table(path):
    """{id: [values]} of a WDBC or WDB2 file; strings resolved for the fields `strings` lists are left as offsets,
    with the string block returned so the caller can resolve them."""
    d = open(path, "rb").read()
    magic = d[:4]
    if magic == b"WDBC":
        n, f, rs, ss = struct.unpack_from("<4I", d, 4)
        o = 20
    elif magic == b"WDB2":
        n, f, rs, ss, _, build, _, mn, mx, _, copies = struct.unpack_from("<11I", d, 4)
        o = 48 + ((mx - mn + 1) * 6 if mx else 0)
    else:
        raise SystemExit("%s: not a DBC/DB2 file" % path)
    if rs != f * 4:
        raise SystemExit("%s: %d fields in %d bytes; only 4-byte fields are supported" % (path, f, rs))
    rows = {}
    for i in range(n):
        v = list(struct.unpack_from("<%di" % f, d, o + i * rs))
        rows[v[0]] = v
    strings = d[o + n * rs:o + n * rs + ss]
    return rows, strings


def as_float(i):
    return struct.unpack("<f", struct.pack("<i", i))[0]


def string(block, offset):
    return block[offset:block.index(b"\0", offset)].decode("utf-8", "replace")


class CataItems:
    def __init__(self, cata_dbc, stock_dbc, model_substitutes=None):
        """model_substitutes: {Cataclysm model: (model, texture)} for weapon models no client here has yet."""
        self.model_substitutes = {k.lower(): (m.lower(), t.lower()) for k, (m, t) in (model_substitutes or {}).items()}
        j = lambda *p: os.path.join(*p)
        self.item, _ = read_table(j(cata_dbc, "Item.db2"))
        self.sparse, self.sparse_str = read_table(j(cata_dbc, "Item-sparse.db2"))
        self.cdisp = self._displays(j(cata_dbc, "ItemDisplayInfo.dbc"))
        self.sdisp = self._displays(j(stock_dbc, "ItemDisplayInfo.dbc"))
        self.stock_by_content = {}
        for i in sorted(self.sdisp):
            self.stock_by_content.setdefault(self.sdisp[i][1:], i)
        self.stock_items = set(read_table(j(stock_dbc, "Item.dbc"))[0])
        self.stock_spells = set(read_table(j(stock_dbc, "Spell.dbc"))[0])
        self.stock_helmet_vis = set(read_table(j(stock_dbc, "HelmetGeosetVisData.dbc"))[0])
        self.stock_item_visuals = set(read_table(j(stock_dbc, "ItemVisuals.dbc"))[0])
        self.stock_spell_visuals = set(read_table(j(stock_dbc, "SpellVisual.dbc"))[0])
        self.stock_random_props = set(read_table(j(stock_dbc, "ItemRandomProperties.dbc"))[0])
        self.stock_item_sets = set(read_table(j(stock_dbc, "ItemSet.dbc"))[0])
        self.stock_limits = set(read_table(j(stock_dbc, "ItemLimitCategory.dbc"))[0])
        self.stock_totems = set(read_table(j(stock_dbc, "TotemCategory.dbc"))[0])
        self.tables = {n: read_table(j(cata_dbc, n + ".dbc"))[0] for n in (
            "ItemDamageOneHand", "ItemDamageOneHandCaster", "ItemDamageTwoHand", "ItemDamageTwoHandCaster",
            "ItemDamageRanged", "ItemDamageThrown", "ItemDamageWand", "ItemDamageAmmo", "ItemArmorQuality",
            "ItemArmorTotal", "ItemArmorShield", "ArmorLocation")}
        self.moved = {}                  # cata display id -> id it was added under
        self.added = {}                  # display id -> row (DISPLAY_COLUMNS order) to add
        self.spells_used = set()         # Cataclysm spells the items use that stock lacks (to port, or cleared)

    @staticmethod
    def _displays(path):
        rows, block = read_table(path)
        out = {}
        for i, v in rows.items():
            out[i] = tuple(string(block, x).lower() if k in DISPLAY_STRINGS else x for k, x in enumerate(v))
        return out

    def has(self, cata_id):
        return cata_id in self.item and cata_id in self.sparse

    def name(self, cata_id):
        return string(self.sparse_str, self.sparse[cata_id][SP["name"]])

    # ---- displays ----
    def display(self, cata_id):
        """Display id an item should use, adding the Cataclysm row when stock doesn't have it."""
        return self.display_id(self.item[cata_id][5])

    def display_id(self, cd):
        row = self.cdisp.get(cd)
        if row is None:
            return 0
        row = self._clean(row)
        if self._same(self.sdisp.get(cd), row):
            return cd
        if row[1:] in self.stock_by_content:        # stock has the same display under another id
            return self.stock_by_content[row[1:]]
        if cd not in self.sdisp:
            self.added[cd] = row
            return cd
        if cd not in self.moved:
            new = DISPLAY_BASE + len(self.moved)
            while new in self.sdisp:
                new += 1
            self.moved[cd] = new
            self.added[new] = (new,) + row[1:]
        return self.moved[cd]

    def _clean(self, row):
        row = list(row)
        for model, texture in ((1, 3), (2, 4)):
            if row[model] in self.model_substitutes:
                row[model], row[texture] = self.model_substitutes[row[model]]
        if row[11] not in self.stock_spell_visuals:
            row[11] = 0
        for k in (13, 14):
            if row[k] not in self.stock_helmet_vis:
                row[k] = 0
        if row[23] not in self.stock_item_visuals:
            row[23] = 0
        return tuple(row)

    @staticmethod
    def _same(a, b):
        return a is not None and a[1:] == b[1:]

    def known_displays(self, rows):
        """Displays a modpak already adds ({column: value} dicts, DISPLAY_COLUMNS names): an item whose Cataclysm
        display has the same content as one of them uses it instead of a new row."""
        for r in rows:
            row = tuple(str(r.get(c, "")).lower() if k in DISPLAY_STRINGS else int(r.get(c, 0) or 0)
                        for k, c in enumerate(DISPLAY_COLUMNS))
            self.sdisp.setdefault(row[0], row)
            self.stock_by_content.setdefault(row[1:], row[0])

    def matches(self, display, cata_id):
        """True when `display` already shows what the item's Cataclysm display does."""
        cd = self.cdisp.get(self.item[cata_id][5])
        return cd is not None and self._same(self.sdisp.get(display), self._clean(cd))

    def display_rows(self):
        """(id, {column: value}) for every display added so far."""
        for i in sorted(self.added):
            yield i, dict(zip(DISPLAY_COLUMNS, self.added[i]))

    # ---- item_template ----
    def _damage_table(self, cls, sub, inv, flags2):
        caster = flags2 & 0x200
        if sub == WAND:
            return "ItemDamageWand"
        if inv in (15, 26) or sub in (BOW, GUN, CROSSBOW):
            return "ItemDamageRanged"
        if inv == 25 or sub == THROWN:
            return "ItemDamageThrown"
        if inv == 24:
            return "ItemDamageAmmo"
        if inv == 17:
            return "ItemDamageTwoHandCaster" if caster else "ItemDamageTwoHand"
        return "ItemDamageOneHandCaster" if caster else "ItemDamageOneHand"

    def damage(self, cata_id):
        cls, sub, _, _, _, inv = self.item[cata_id][1:7]
        s = self.sparse[cata_id]
        q, ilvl, delay = s[SP["quality"]], s[SP["ilvl"]], s[SP["delay"]]
        if cls != ITEM_CLASS_WEAPON or q > 6 or not delay:
            return 0, 0
        row = self.tables[self._damage_table(cls, sub, inv, s[SP["flags2"]])].get(ilvl)
        if not row:
            return 0, 0
        dps = as_float(row[1 + q])
        avg = dps * delay / 1000.0
        f = as_float(s[SP["scaling_factor"]])
        return int(math.floor(avg * (1.0 - f * 0.5))), int(math.floor(avg * (1.0 + f * 0.5) + 0.5))

    def armor(self, cata_id):
        cls, sub, _, _, _, inv = self.item[cata_id][1:7]
        s = self.sparse[cata_id]
        q, ilvl = s[SP["quality"]], s[SP["ilvl"]]
        if cls != ITEM_CLASS_ARMOR or q > 6:
            return 0
        if sub == ARMOR_SHIELD:
            row = self.tables["ItemArmorShield"].get(ilvl)
            return int(as_float(row[2 + q]) + 0.5) if row else 0      # ID, ItemLevel, Quality[7]
        if not 1 <= sub <= 4:
            return 0
        quality = self.tables["ItemArmorQuality"].get(ilvl)
        total = self.tables["ItemArmorTotal"].get(ilvl)
        loc = self.tables["ArmorLocation"].get(INVTYPE_CHEST if inv == INVTYPE_ROBE else inv)
        if not (quality and total and loc):
            return 0
        return int(as_float(quality[1 + q]) * as_float(total[2 + sub - 1]) * as_float(loc[1 + sub - 1]) + 0.5)

    def _spell(self, sid):
        if not sid or sid in self.stock_spells:
            return sid
        self.spells_used.add(sid)
        return sid

    def template(self, cata_id, entry, race_mask=None):
        """item_template columns. race_mask: what to write for AllowableRace (Cataclysm's is kept when None)."""
        it, s = self.item[cata_id], self.sparse[cata_id]
        g = lambda k, i=0: s[SP[k] + i]
        cls, sub, sound, material, _, inv, sheath = it[1:8]
        dmin, dmax = self.damage(cata_id)
        row = dict.fromkeys(ITEM_TEMPLATE_COLUMNS, 0)
        row.update({
            "entry": entry, "class": cls, "subclass": sub, "SoundOverrideSubclass": sound,
            "name": string(self.sparse_str, g("name")), "displayid": self.display(cata_id),
            "Quality": g("quality"), "Flags": g("flags") & 0xFFFFFFFF, "FlagsExtra": g("flags2") & 0xFFFFFFFF,
            "BuyCount": 1, "BuyPrice": g("buy"), "SellPrice": g("sell"), "InventoryType": inv,
            "AllowableClass": g("cls_mask"), "AllowableRace": g("race_mask") if race_mask is None else race_mask,
            "ItemLevel": g("ilvl"), "RequiredLevel": g("req_level"), "RequiredSkill": g("req_skill"),
            "RequiredSkillRank": g("req_skill_rank"), "requiredspell": self._spell(max(g("req_spell"), 0)),
            "requiredhonorrank": g("honor"), "RequiredCityRank": g("city"),
            "RequiredReputationFaction": g("rep_faction"), "RequiredReputationRank": g("rep_rank"),
            "maxcount": g("max_count"), "stackable": g("stack"), "ContainerSlots": g("slots"),
            "ScalingStatDistribution": 0, "ScalingStatValue": 0,
            "dmg_min1": dmin, "dmg_max1": dmax, "dmg_type1": g("dmg_type") if dmax else 0,
            "armor": self.armor(cata_id), "delay": g("delay"), "RangedModRange": round(as_float(g("range")), 4),
            "bonding": g("bonding"), "description": string(self.sparse_str, g("description")),
            "PageText": g("page"), "LanguageID": g("language"), "PageMaterial": g("page_material"),
            "startquest": g("start_quest"), "lockid": g("lock"), "Material": material, "sheath": sheath,
            "RandomProperty": g("random_property") if g("random_property") in self.stock_random_props else 0,
            "RandomSuffix": 0,
            "itemset": g("item_set") if g("item_set") in self.stock_item_sets else 0,
            "area": g("area"), "Map": g("map"), "BagFamily": g("bag_family"),
            "TotemCategory": g("totem") if g("totem") in self.stock_totems else 0,
            "ArmorDamageModifier": round(as_float(g("armor_dmg_mod")), 4), "duration": g("duration"),
            "ItemLimitCategory": g("limit_category") if g("limit_category") in self.stock_limits else 0,
            "HolidayId": g("holiday"), "ScriptName": "", "RequiredDisenchantSkill": -1,
        })
        n = 0
        for i in range(10):
            t, v = g("stat_type", i), g("stat_value", i)
            if t > 0 and v and t not in DROP_STATS:
                n += 1
                row["stat_type%d" % n], row["stat_value%d" % n] = t, v
        for i in range(5):
            sid = g("spell", i)
            k = i + 1
            row["spellcooldown_%d" % k] = row["spellcategorycooldown_%d" % k] = -1
            if sid > 0:
                row["spellid_%d" % k] = self._spell(sid)
                row["spelltrigger_%d" % k] = g("trigger", i)
                row["spellcharges_%d" % k] = g("charges", i)
                row["spellcooldown_%d" % k] = g("cooldown", i)
                row["spellcategory_%d" % k] = g("category", i)
                row["spellcategorycooldown_%d" % k] = g("cat_cooldown", i)
        return row


def sql_value(v):
    if v is None:
        return "NULL"
    if isinstance(v, str):
        if v.startswith("@"):
            return v
        return "'" + v.replace("\\", "\\\\").replace("'", "''").replace("\r", "\\r").replace("\n", "\\n") + "'"
    if isinstance(v, float):
        return ("%.4f" % v).rstrip("0").rstrip(".") or "0"
    return str(v)


def display_sql(items, comment):
    """DELETE + INSERT ... SET blocks of the displays added so far, like the other dbc/ files."""
    out = [comment]
    for i, row in items.display_rows():
        out.append("DELETE FROM `itemdisplayinfo` WHERE `id` = %d;\nINSERT INTO `itemdisplayinfo` SET\n%s;\n" % (
            i, ",\n".join("  `%s` = %s" % (k, sql_value(v)) for k, v in row.items())))
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    items = CataItems(sys.argv[1], sys.argv[2])
    for a in sys.argv[3:]:
        c = int(a)
        t = items.template(c, c)
        print({k: v for k, v in t.items() if v not in (0, "", -1)})
    for i, row in items.display_rows():
        print("display", i, {k: v for k, v in row.items() if v})

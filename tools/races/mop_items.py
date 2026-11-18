"""Mists of Pandaria items for 3.3.5a: CataItems (cata_items.py) on the 5.4.8 (18414) client's tables.

  items = MopItems(MOP_DBC, STOCK_DBC, ITEMSPARSE_CSV, reserved_displays)

MOP_DBC is References/MoP/MoP_data/dbc. Its Item.db2, ItemDisplayInfo.dbc and the damage / armour tables have
4.0.6a's layout (ItemDisplayInfo has one more field at the end, dropped here). Item-sparse.db2 has three more fields
before BuyPrice (BuyCount is 4.0.6a's field 4 moved to 7, after the two price floats) and drops 4.0.6a's unknown field
111, so 4.0.6a's indices from 4 (BuyPrice) to 110 are 4 higher and the later ones 3; Quality and the flags (1-3) stay (checked on items 25 and 6948 in both clients).
Its strings are ruRU, so names and descriptions come from ITEMSPARSE_CSV, wago.tools' English ItemSparse export
(https://wago.tools/db2/ItemSparse/csv?build=5.5.4.70449), matched by id.
reserved_displays: ItemDisplayInfo ids other modpaks allocate (config.sql's @NextItemDisplayID block); a MoP
display with one of those ids is added under DISPLAY_BASE and up instead, like one stock uses for something else.
"""
import csv, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cata_items import CataItems, SP, read_table, string, ITEM_CLASS_WEAPON, ITEM_CLASS_ARMOR  # noqa: E402

MOP_SP = {k: v if v < 4 else v + 4 if v <= 110 else v + 3 for k, v in SP.items()}
DISPLAY_FIELDS = 25              # 3.3.5a / 4.0.6a ItemDisplayInfo


class MopItems(CataItems):
    sp = MOP_SP

    def __init__(self, mop_dbc, stock_dbc, itemsparse_csv, reserved_displays=()):
        super().__init__(mop_dbc, stock_dbc)
        self.mop_dbc, self.stock_dbc = mop_dbc, stock_dbc
        csv.field_size_limit(1 << 24)
        self.english = {}
        with open(itemsparse_csv, encoding="utf8", newline="") as f:
            for r in csv.DictReader(f):
                self.english[int(r["ID"])] = (r["Display_lang"], r["Description_lang"])
        for d in reserved_displays:
            # a placeholder no real row equals, so display_id() moves a MoP display with this id elsewhere
            self.sdisp.setdefault(d, (d, "<reserved>") + (0,) * (DISPLAY_FIELDS - 2))

    @staticmethod
    def _displays(path):
        rows, block = read_table(path)
        from cata_items import DISPLAY_STRINGS
        return {i: tuple(string(block, x).lower() if k in DISPLAY_STRINGS else x for k, x in enumerate(v[:DISPLAY_FIELDS]))
                for i, v in rows.items()}

    def name(self, mop_id):
        return self.english.get(mop_id, (super().name(mop_id), ""))[0]

    def template(self, mop_id, entry, race_mask=None):
        row = super().template(mop_id, entry, race_mask)
        if mop_id in self.english:
            row["name"], row["description"] = self.english[mop_id]
        self.wotlk_scale(mop_id, row)
        row["RandomSuffix"] = self.suffix_group(self.sparse[mop_id][self.sp["random_suffix"]])
        return row

    # random suffixes ("of the Monkey"): the server's item_enchantment_template groups, given by the caller
    # (enchant_groups = {group: [(suffix, chance)]}, e.g. SkyFire's table), as groups from SUFFIX_BASE that keep the
    # suffixes stock's ItemRandomSuffix.dbc has with the same enchantments (DBCTool can't add new suffix rows)
    enchant_groups = {}

    def suffix_group(self, group):
        if not group or group not in self.enchant_groups:
            return 0
        if not hasattr(self, "suffix_map"):
            self.suffix_map, self.suffix_rows = {}, []
            mop = read_table(os.path.join(self.mop_dbc, "ItemRandomSuffix.dbc"))[0]
            stock = read_table(os.path.join(self.stock_dbc, "ItemRandomSuffix.dbc"))[0]
            self.same_suffixes = {i for i, r in mop.items() if i in stock and list(r[3:13]) == list(stock[i][19:29])}
        if group not in self.suffix_map:
            keep = [(s, c) for s, c in self.enchant_groups[group] if s in self.same_suffixes]
            self.suffix_map[group] = SUFFIX_BASE + len(self.suffix_map) if keep else 0
            self.suffix_rows += [[self.suffix_map[group], s, c] for s, c in keep]
        return self.suffix_map[group]

    def wotlk_scale(self, mop_id, row):
        """Items for levels above 80 (Cataclysm's and MoP's 81-90), as 3.3.5a's 71-80 ones: required level less 10;
        gear also gets a WotLK item level (ILVL_MAP) and stats, armour, damage and price for it. Stats and price scale
        by the ratio of the stat budgets (RandPropPoints, by quality and slot) at the new and old item levels; armour
        and damage follow AzerothCore's own 3.3.5a items of that level, slot, armour type and quality (WotlkCurves;
        5.4.8's armour and damage tables only match WotLK's for plate)."""
        req, ilvl = row["RequiredLevel"], row["ItemLevel"]
        if req > 80:
            row["RequiredLevel"] = req - 10
        if row["class"] not in (ITEM_CLASS_WEAPON, ITEM_CLASS_ARMOR) or not (req > 80 or ilvl > MAX_WOTLK_ILVL):
            return
        new = wotlk_ilvl(ilvl)
        if not hasattr(self, "rpp"):
            self.rpp = (read_table(os.path.join(self.stock_dbc, "RandPropPoints.dbc"))[0],
                        read_table(os.path.join(self.mop_dbc, "RandPropPoints.dbc"))[0])
        col = rpp_column(row["Quality"], row["InventoryType"])
        stock, mop = self.rpp[0].get(new), self.rpp[1].get(ilvl)
        f = stock[col] / mop[col] if stock and mop and mop[col] and stock[col] else new / max(ilvl, 1)
        row["ItemLevel"] = new
        for n in range(1, 11):
            if row["stat_value%d" % n]:
                row["stat_value%d" % n] = max(1, int(round(row["stat_value%d" % n] * f)))
        row["BuyPrice"], row["SellPrice"] = int(row["BuyPrice"] * f), int(row["SellPrice"] * f)
        if not hasattr(self, "curves"):
            self.curves = WotlkCurves(self)
        if row["class"] == ITEM_CLASS_ARMOR:         # also Timeless Isle gear, armourless in 5.4.8's tables
            row["armor"] = self.curves.armor(row, new) or row["armor"]
        if row["dmg_max1"] and row["delay"]:
            avg = self.curves.dps(row, new) * row["delay"] / 1000.0
            old = (row["dmg_min1"] + row["dmg_max1"]) / 2.0
            if avg and old:
                row["dmg_min1"], row["dmg_max1"] = int(row["dmg_min1"] * avg / old), int(row["dmg_max1"] * avg / old + 0.5)


AC_ITEMS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "azerothcore-wotlk-256-bit", "data",
                        "sql", "base", "db_world", "item_template.sql")


class WotlkCurves:
    """Armour and weapon DPS by item level as AzerothCore's 3.3.5a items have them: per (armour subclass, slot,
    quality) and (damage table, quality), the median of the items nearest in level, scaled by level ratio."""

    def __init__(self, items, path=AC_ITEMS):
        from mop_pandaria_nodes import values
        from cata_items import ITEM_TEMPLATE_COLUMNS
        self.items, self.armor_pts, self.dps_pts = items, {}, {}
        for line in open(path, encoding="utf8", errors="replace"):
            if not line.startswith("("):
                continue
            v = dict(zip(ITEM_TEMPLATE_COLUMNS, values(line.rstrip().rstrip(",;").replace("''", "\\'"))))
            try:
                cls, sub, inv, q, ilvl = (int(v[k]) for k in ("class", "subclass", "InventoryType", "Quality", "ItemLevel"))
            except (KeyError, ValueError):
                continue
            if not 2 <= q <= 4 or ilvl < 60:
                continue
            if cls == ITEM_CLASS_ARMOR and int(v["armor"]) and (1 <= sub <= 4 or sub == 6):
                self.armor_pts.setdefault((sub, 5 if inv == 20 else inv, q), []).append((ilvl, int(v["armor"])))
            elif cls == ITEM_CLASS_WEAPON and int(v["delay"]) and float(v["dmg_max1"]):
                t = items._damage_table(cls, sub, inv, int(v["FlagsExtra"]))
                dps = (float(v["dmg_min1"]) + float(v["dmg_max1"])) / 2 / (int(v["delay"]) / 1000.0)
                self.dps_pts.setdefault((t, q), []).append((ilvl, dps))

    @staticmethod
    def _at(pts, ilvl):
        if not pts:
            return 0
        near = sorted(pts, key=lambda p: abs(p[0] - ilvl))[:7]
        vals = sorted(v * ilvl / max(i, 1) for i, v in near)
        return vals[len(vals) // 2]

    def armor(self, row, ilvl):
        sub, inv, q = row["subclass"], 5 if row["InventoryType"] == 20 else row["InventoryType"], min(max(row["Quality"], 2), 4)
        pts = self.armor_pts.get((sub, inv, q)) or [p for k, v in self.armor_pts.items() if k[:2] == (sub, inv) for p in v]
        return int(round(self._at(pts, ilvl)))

    def dps(self, row, ilvl):
        t = self.items._damage_table(row["class"], row["subclass"], row["InventoryType"], row["FlagsExtra"])
        q = min(max(row["Quality"], 2), 4)
        return self._at(self.dps_pts.get((t, q)) or [p for k, v in self.dps_pts.items() if k[0] == t for p in v], ilvl)


SUFFIX_BASE = 133000               # item_enchantment_template entries (AzerothCore's own end below 9000)
MAX_WOTLK_ILVL = 284
# (Cataclysm/MoP item level, WotLK item level): Cataclysm's 81-85 levelling gear -> 71-75's, MoP's 85-90 levelling
# greens -> Northrend's 75-80 ones, MoP's dungeon blues (463) -> WotLK's (200), raids and the Timeless Isle -> ICC's
ILVL_MAP = [(272, 145), (359, 162), (372, 165), (450, 187), (463, 200), (476, 213), (496, 226), (522, 245),
            (553, 258), (580, 271), (608, 284), (1000, 300)]


def wotlk_ilvl(ilvl):
    if ilvl <= ILVL_MAP[0][0]:
        return min(ilvl, ILVL_MAP[0][1])
    for (a, x), (b, y) in zip(ILVL_MAP, ILVL_MAP[1:]):
        if ilvl <= b:
            return int(round(x + (y - x) * (ilvl - a) / (b - a)))
    return ILVL_MAP[-1][1]


def rpp_column(quality, inv):
    """RandPropPoints field for a quality and inventory type (TrinityCore's GetRandomPropertyPoints slot groups)."""
    group = {1: 0, 5: 0, 7: 0, 17: 0, 20: 0, 3: 1, 6: 1, 8: 1, 10: 1, 12: 1, 2: 2, 9: 2, 11: 2, 14: 2, 16: 2, 23: 2,
             13: 3, 21: 3, 22: 3, 15: 4, 25: 4, 26: 4, 28: 4}.get(inv, 0)
    return 1 + group + (0 if quality >= 4 else 5 if quality == 3 else 10)


if __name__ == "__main__":
    # self-check on an item in both clients: 6948 Hearthstone keeps its spell, cooldown and English name
    here = os.path.dirname(os.path.abspath(__file__))
    refs = os.path.join(here, "..", "..", "..", "References")
    items = MopItems(os.path.join(refs, "MoP", "MoP_data", "dbc"), os.path.join(refs, "original-client-dbc"),
                     sys.argv[1] if len(sys.argv) > 1 else "D:/wow-scratch/wi/db2/ItemSparse.csv")
    t = items.template(6948, 6948)
    assert (t["name"], t["spellid_1"], t["spellcategory_1"], t["stackable"]) == ("Hearthstone", 8690, 1176, 1), t
    assert (t["Quality"], t["Flags"]) == (1, 64), t
    t = items.template(25, 25)
    assert (t["name"], t["Material"], t["sheath"], t["delay"]) == ("Worn Shortsword", 1, 3, 1900), t
    assert (wotlk_ilvl(200), wotlk_ilvl(463), wotlk_ilvl(496), wotlk_ilvl(2000)) == (145, 200, 226, 300)
    t = items.template(90573, 90573)            # a BoE world epic for level 90
    assert t["RequiredLevel"] <= 80 and t["ItemLevel"] <= 284, t
    print("ok", t["name"], t["ItemLevel"], t["RequiredLevel"], [(t["stat_type%d" % n], t["stat_value%d" % n])
                                                                for n in range(1, 5)], t["armor"])

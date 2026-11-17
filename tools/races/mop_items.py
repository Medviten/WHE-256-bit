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
from cata_items import CataItems, SP, read_table, string  # noqa: E402

MOP_SP = {k: v if v < 4 else v + 4 if v <= 110 else v + 3 for k, v in SP.items()}
DISPLAY_FIELDS = 25              # 3.3.5a / 4.0.6a ItemDisplayInfo


class MopItems(CataItems):
    sp = MOP_SP

    def __init__(self, mop_dbc, stock_dbc, itemsparse_csv, reserved_displays=()):
        super().__init__(mop_dbc, stock_dbc)
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
        return row


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
    print("ok")

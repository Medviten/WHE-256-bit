"""Generated loot for MoP-port creatures no source has loot for (mop_pandaria_port.py, mop_wandering_isle_port.py).

  fill = LootFill(ref_base, items, cloth=72988, skins=[(72120, 100, 1, 3)])
  fill.learn(creature_type, family, item)        # for every item the source's own loot drops
  rows = fill.creature(creature_type, family, rank) # creature_loot_template rows (without Entry), or [] if none
  fill.references()                                 # reference_loot_template rows of the pools used

Pools come from the loot the source does have, so a zone drops its own junk and gear:
- junk: grey items of any creature (20-35 % per kill, one of them)
- goods: white trade goods and consumables (not soulbound) creatures of the same type and family drop, else the same
  type (45 %), e.g. meat from beasts, food from humanoids
- cloth for humanoids (30 %, 1-2), skins for beasts and dragonkin (skinning_loot_template)
- bind-on-equip greens 3 %, blues 0.5 %, epics 0.03 % (elites x2; rares 15 % blue, 0.5 % epic)
Each pool is one reference_loot_template entry whose items share one group without chances, so one of them drops.
gold(level, rank) is copper by level (0.25 * level^2.4, x3 elite, x5 rare, x10 boss), +-30 %.
"""
import collections

KILLABLE_TYPES = {1, 2, 3, 4, 5, 6, 7, 9, 15}     # not critters (8), unspecified (10), totems, pets, clouds, wild pets
NOT_KILLABLE_FLAGS = 0x2 | 0x100 | 0x2000000      # UNIT_FLAG_NON_ATTACKABLE, IMMUNE_TO_PC, NOT_SELECTABLE
HUMANOIDS = {7}
SKINNABLE = {1, 2}
RANK_GOLD = {0: 1, 1: 3, 2: 5, 3: 10, 4: 5}
ITEM_CLASS_CONSUMABLE, ITEM_CLASS_WEAPON, ITEM_CLASS_ARMOR, ITEM_CLASS_TRADE = 0, 2, 4, 7
BIND_ON_EQUIP = 2


def killable(ctype, unit_flags, npcflag, flags_extra=0):
    return ctype in KILLABLE_TYPES and not unit_flags & NOT_KILLABLE_FLAGS and not npcflag and not flags_extra & 0x80


def gold(level, rank):
    base = 0.25 * max(level, 1) ** 2.4 * RANK_GOLD.get(rank, 1)
    return int(base * 0.7), int(base * 1.3) + 1


class LootFill:
    def __init__(self, ref_base, items, cloth=0, skins=()):
        """items: a CataItems/MopItems (its client tables give quality, class and binding)."""
        self.ref_base, self.items, self.cloth, self.skins = ref_base, items, cloth, list(skins)
        self.junk, self.gear = set(), collections.defaultdict(set)
        self.goods = collections.defaultdict(set)
        self.refs = {}                                     # pool key -> reference id

    def _info(self, item):
        it, s = self.items.item.get(item), self.items.sparse.get(item)
        if not it or not s:
            return None
        return s[self.items.sp["quality"]], it[1], s[self.items.sp["bonding"]]

    def learn(self, ctype, family, item):
        info = self._info(item)
        if not info:
            return
        q, cls, bond = info
        if q == 0:
            self.junk.add(item)
        elif q == 1 and cls in (ITEM_CLASS_CONSUMABLE, ITEM_CLASS_TRADE) and bond == 0 and item != self.cloth:
            self.goods[(ctype, family)].add(item)
            self.goods[(ctype, None)].add(item)
        elif 2 <= q <= 4 and cls in (ITEM_CLASS_WEAPON, ITEM_CLASS_ARMOR) and bond == BIND_ON_EQUIP:
            self.gear[q].add(item)

    def _ref(self, key, pool):
        if not pool:
            return 0
        if key not in self.refs:
            self.refs[key] = (self.ref_base + len(self.refs), sorted(pool))
        return self.refs[key][0]

    def creature(self, ctype, family, rank):
        """creature_loot_template rows after Entry: Item Reference Chance QuestRequired LootMode GroupId MinCount
        MaxCount Comment."""
        rows = []

        def ref(key, pool, chance, comment):
            r = self._ref(key, pool)
            if r:
                rows.append([r, r, chance, 0, 1, 0, 1, 1, comment])

        elite = 2 if rank else 1
        rare = rank in (2, 4)
        ref("junk", self.junk, 35 if ctype in HUMANOIDS else 20, "generated: junk")
        goods = self.goods.get((ctype, family)) or self.goods.get((ctype, None))
        ref(("goods", ctype, family if self.goods.get((ctype, family)) else None), goods, 45, "generated: goods")
        if ctype in HUMANOIDS and self.cloth:
            rows.append([self.cloth, 0, 30, 0, 1, 0, 1, 2, "generated: cloth"])
        ref("green", self.gear[2], 3 * elite, "generated: world green")
        ref("blue", self.gear[3], 15 if rare else 0.5 * elite, "generated: world blue")
        ref("epic", self.gear[4], 0.5 if rare else 0.03 * elite, "generated: world epic")
        return rows

    def skinning(self, ctype):
        return [[i, 0, c, 0, 1, 0, lo, hi, "generated: skinning"] for i, c, lo, hi in self.skins] \
            if ctype in SKINNABLE else []

    def references(self):
        """reference_loot_template rows (Entry Item Reference Chance QuestRequired LootMode GroupId MinCount MaxCount
        Comment) and the items they use."""
        rows, used = [], set()
        for key, (r, pool) in sorted(self.refs.items(), key=lambda kv: kv[1][0]):
            name = key if isinstance(key, str) else "goods %s/%s" % key[1:]
            for i in pool:
                rows.append([r, i, 0, 0, 0, 1, 1, 1, 1, "generated pool: %s" % name])
                used.add(i)
        return rows, used


if __name__ == "__main__":
    assert killable(7, 0, 0) and not killable(8, 0, 0) and not killable(7, 0x2000000, 0) and not killable(7, 0, 2)
    assert gold(80, 0)[0] > 5000 and gold(10, 0)[1] < 100, (gold(80, 0), gold(10, 0))

    class Fake:
        sp = {"quality": 0, "bonding": 1}
        item = {1: [1, 4], 2: [2, 7], 3: [3, 4]}
        sparse = {1: [0, 0], 2: [1, 0], 3: [2, 2]}
    f = LootFill(500, Fake(), cloth=9)
    for i in (1, 2, 3):
        f.learn(1, 5, i)
    rows = f.creature(1, 5, 0)
    assert [r[-1] for r in rows] == ["generated: junk", "generated: goods", "generated: world green"], rows
    refs, used = f.references()
    assert used == {1, 2, 3} and {r[0] for r in refs} == {500, 501, 502}, refs
    print("ok")

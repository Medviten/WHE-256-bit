"""The races of Ilusixn's CoA 1.9.9 release (References/Ilusixn/1.9.9 release) that WHE did not have, as WHE sees
them (F-105..F-127), and a reader for the release's EsteriaAppearance catalogs. Imported by coa199_race_modpaks.py,
coa_racials.py and models/coa199_race_prep.py.

Two kinds of race:
- catalog races (CoA draws them with EsteriaAppearance.dll): what coa_races.py says about the 1.9 races holds, but the
  1.9.9 catalogs also use record kinds 2 (a geoset by its absolute id), 3 (flags), 4 (which armour covers which
  geosets) and 5 (item texture overrides). Look199 keeps kinds 0-2 and ignores 3-5; a gender without skin textures
  (Sethrak females, Drakkin females) keeps the model's own textures and gets one empty skin row
- classic races (Alliance Orc .. Elune's Chosen): character models with CharSections rows of their own, which CoA's
  server DBCs carry in the stock 3.3.5 layout under the CoA race id

Left out: the release's races whose files neither it, a CoA-based client (Kalibro's Esteria client) nor retail has.
Leper Troll and Troglodyte (no models), Drakkari Troll (no .skin, animations or textures), Undead Gnome (no textures)
and Wretched (no textures: CoA's own, from the AllRaces v12 pack). Forgotten is WHE's Thin Human (F-041). The Titan's
male textures are missing too, so Titans use the female model for both genders (ONE_BODY).

Race ids come from config.sql. The CoA race id is the release's ChrRaces id; the racials (coa_racials.py) are keyed
separately, by the spell id's race part ('1.9' spells 14000000 + n * 10 + slot, 'v12' spells 15000000 + n * 10 + slot,
where n is CoA's own numbering for 1.9 and the ChrRaces id for v12)."""
import collections
import os

import coa_races

ALWAYS = coa_races.ALWAYS
HIDDEN_GEOSET = coa_races.HIDDEN_GEOSET

Race = collections.namedtuple('Race', 'key name plural fnum slug side home kin coa_id catalog prefix fname fdesc info spells')

# catalog: the Esteria<catalog>.bin of a catalog race, None for a classic race. prefix: the helmet model suffix
RACES = [
    Race('Sethrak', 'Sethrak', 'Sethrak', 105, 'sethrak', 'Alliance', 'Human', 'Troll', 82, 'Sethrak', 'Tr',
         'Heirs of Sethraliss', 'Sethrak of Vol\'dun who honour the fallen Loa of the Wind and fight beside the Alliance.',
         'The sethrak are serpent people of the deserts of Vol\'dun, once servants of the Loa Sethraliss. Those who turned from the Faithless have found allies in the Alliance.',
         [('1.9', 82)]),
    Race('Sureki', 'Sureki', 'Sureki', 106, 'sureki', 'Alliance', 'NightElf', 'NightElf', 86, 'Sureki', 'Gn',
         'Sureki Defectors', 'Nerubians of Azj-Kahet who fled the war beneath Khaz Algar and offered their silk to the Alliance.',
         'The sureki are the nerubians of Azj-Kahet, an empire deep beneath Khaz Algar. A few have fled its intrigues to seek a new hive above ground.',
         [('v12', 86)]),
    Race('Dreadlord', 'Dreadlord', 'Dreadlords', 107, 'dreadlord', 'Horde', 'Undead', 'Undead', 89, 'Dreadlord', 'Gn',
         'Nathrezim Defectors', 'Dreadlords who abandoned the Burning Legion for reasons they keep to themselves.',
         'The nathrezim are scheming demon lords of the Burning Legion, masters of fear and deceit. The Forsaken trust none of them, but use them all the same.',
         [('v12', 89)]),
    Race('Titan', 'Titan', 'Titans', 108, 'titan', 'Alliance', 'Dwarf', 'Human', 91, 'Titan', 'Gn',
         'Titan-Forged Vanguard', 'Titan-forged who answer to the Keepers and stand with the dwarves of Ironforge.',
         'The titan-forged were shaped by the Titans to guard the world\'s secrets. Some have woken from their long watch and taken up arms with the Alliance.',
         [('v12', 91)]),
    Race('Fungarian', 'Fungarian', 'Fungarians', 109, 'fungarian', 'Alliance', 'NightElf', 'Draenei', 93, 'Fungarian', 'Gn',
         'Fungarian Circle', 'Mushroom folk of Zangarmarsh who tend the spore groves beside the druids.',
         'The fungarians are walking mushrooms of the marshes of Outland, slow to anger and slower to leave. A few have drifted to Azeroth on the winds.',
         [('v12', 93)]),
    Race('Saberon', 'Saberon', 'Saberon', 110, 'saberon', 'Alliance', 'NightElf', 'NightElf', 97, 'Saberon', 'Ta',
         'Saberon Pride', 'Saberon of Draenor\'s jungles who hunt beside the night elves\' Sentinels.',
         'The saberon are cat-like hunters of Draenor, fierce and territorial. A pride that crossed into Azeroth has found kinship with the night elves.',
         [('1.9', 97)]),
    Race('Drakonid', 'Drakonid', 'Drakonid', 111, 'drakonid', 'Horde', 'Orc', 'Orc', 98, 'Drakonid', 'Dk',
         'Unbound Drakonid', 'Drakonid freed from the black dragonflight who fight for the Horde.',
         'Drakonid are the winged soldiers of the dragonflights. Freed from Nefarian\'s control, some have pledged their claws to the Horde.',
         []),
    Race('Sporeling', 'Sporeling', 'Sporelings', 112, 'sporeling', 'Alliance', 'Gnome', 'Gnome', 111, 'Sporeling', 'Gn',
         'Sporeggar Envoys', 'Sporelings of Sporeggar who came to Azeroth to see the world.',
         'The sporelings are small, curious mushroom people of Zangarmarsh. The gnomes of Gnomeregan find them excellent company.',
         [('v12', 111)]),
    Race('Stormforged', 'Stormforged', 'Stormforged', 113, 'stormforged', 'Alliance', 'Dwarf', 'Human', 114, 'Stormforged', 'Gn',
         'Stormforged Vanguard', 'Stormforged who resisted Loken\'s corruption and joined the Explorers\' League.',
         'The stormforged are titan-forged giants of the Storm Peaks. Freed from Loken\'s will, they stand with the dwarves who share their origins.',
         [('v12', 114)]),
    Race('Moarg', 'Mo\'arg', 'Mo\'arg', 114, 'moarg', 'Horde', 'Orc', 'Orc', 119, 'Moarg', 'Gn',
         'Felforge Renegades', 'Mo\'arg engineers who fled the Legion\'s forges and sell their skills to the Horde.',
         'The mo\'arg are the Burning Legion\'s brutish engineers and smiths. A few escaped the forges and found the Horde a willing buyer.',
         [('v12', 119)]),
    Race('Nerubian', 'Nerubian', 'Nerubians', 115, 'nerubian', 'Horde', 'Undead', 'Undead', 120, 'Nerubian', 'Gn',
         'Azjol Survivors', 'Nerubians of Azjol-Nerub who never bowed to the Lich King and fight beside the Forsaken.',
         'The nerubians once ruled an empire beneath Northrend, broken by the Scourge. The survivors share the Forsaken\'s hatred of the Lich King.',
         [('v12', 120)]),
    Race('Lich', 'Lich', 'Liches', 116, 'lich', 'Horde', 'Undead', 'Undead', 122, 'Lich', 'Gn',
         'Unbound Phylacteries', 'Liches who broke free of the Scourge and serve the Banshee Queen.',
         'Liches are undead sorcerers who bound their souls to phylacteries. Those freed from the Lich King lend their magic to the Forsaken.',
         [('v12', 122)]),
    Race('Mogu', 'Mogu', 'Mogu', 117, 'mogu', 'Alliance', 'Human', 'Human', 123, 'Mogu', 'Gn',
         'Mogu Penitents', 'Mogu who rejected the Thunder King\'s tyranny and seek honour with the Alliance.',
         'The mogu once ruled Pandaria with an iron fist. A handful have renounced their ancestors\' cruelty and joined the Alliance.',
         [('v12', 123)]),
    Race('LostOne', 'Lost One', 'Lost Ones', 118, 'lost-one', 'Alliance', 'Draenei', 'Draenei', 125, 'LostOne', 'Gn',
         'The Redeemed Lost', 'Lost ones of Draenor whom the naaru have begun to heal.',
         'The Lost Ones are draenei twisted by fel energy during their long exile on Draenor. With the naaru\'s help, some have found their way back to their people.',
         [('v12', 125)]),
    Race('Drakkin', 'Drakkin', 'Drakkin', 119, 'drakkin', 'Alliance', 'Human', 'Human', 99, 'Tarasek', 'Dr',
         'Drakkin of the Dragonflights', 'Dragons in mortal form who walk among the people of Stormwind.',
         'Drakkin are dragons who live in a smaller, mortal shape. Those who choose to stay among the younger races have found a home in Stormwind.',
         []),
    Race('AllianceOrc', 'Orc', 'Orcs', 120, 'alliance-orc', 'Alliance', 'Human', 'Orc', 52, None, 'Or',
         'Orcs of the Alliance', 'Orcs who left the Horde and pledged themselves to Stormwind.',
         'Not every orc follows the Warchief. Some, raised in human lands or weary of the Horde\'s wars, fight for the Alliance.',
         []),
    Race('Harpy', 'Harpy', 'Harpies', 121, 'harpy', 'Horde', 'Tauren', 'BloodElf', 56, None, 'Be',
         'Windfury Defectors', 'Harpies who broke from their flocks and made peace with Thunder Bluff.',
         'Harpies are winged raiders of Kalimdor\'s cliffs. A flock that tired of war has made an uneasy peace with the tauren.',
         [('1.9', 56)]),
    Race('IllidariBloodElf', 'Illidari Blood Elf', 'Illidari Blood Elves', 122, 'illidari-blood-elf', 'Horde', 'BloodElf', 'BloodElf', 60, None, 'Be',
         'Illidari of Silvermoon', 'Blood elf demon hunters who returned to Silvermoon after the fall of the Black Temple.',
         'Demon hunters give up their sight to see the Legion\'s magic. These blood elves trained under Illidan and now guard Quel\'Thalas.',
         [('1.9', 60)]),
    Race('IllidariNightElf', 'Illidari Night Elf', 'Illidari Night Elves', 123, 'illidari-night-elf', 'Alliance', 'NightElf', 'NightElf', 61, None, 'Ni',
         'Illidari of Darnassus', 'Night elf demon hunters whom Tyrande has allowed to come home.',
         'Night elf demon hunters were exiled for following Illidan into forbidden magic. With the Legion ever a threat, Darnassus has welcomed some of them back.',
         [('1.9', 61)]),
    Race('Jinyu', 'Jinyu', 'Jinyu', 124, 'jinyu', 'Alliance', 'NightElf', 'Draenei', 78, None, 'Dr',
         'Pearlfin Jinyu', 'Jinyu of the Pearlfin village who befriended the Alliance in Pandaria.',
         'The jinyu are fish-like people of Pandaria\'s rivers, guided by their waterspeakers. The Pearlfin jinyu offered their friendship to the Alliance.',
         [('1.9', 78)]),
    Race('TwoHeadedOgre', 'Two-Headed Ogre', 'Two-Headed Ogres', 125, 'two-headed-ogre', 'Horde', 'Orc', 'Orc', 85, None, 'Or',
         'Two-Headed Mercenaries', 'Two-headed ogres who argued their way into the Horde\'s ranks.',
         'Two-headed ogres are as strong as two ogres and almost as clever as one. The Horde pays them twice and asks no questions.',
         [('1.9', 53)]),
    Race('Grummle', 'Grummle', 'Grummles', 126, 'grummle', 'Alliance', 'Dwarf', 'Gnome', 103, None, 'Gn',
         'Grummle Traders', 'Grummles of Kun-Lai who carry goods along Alliance roads, and bring luck.',
         'Grummles are small, superstitious traders of Pandaria\'s mountains who believe in luck above all. Their caravans now follow Alliance roads.',
         [('1.9', 103)]),
    Race('EluneChosen', 'Elune\'s Chosen', 'Elune\'s Chosen', 127, 'elunes-chosen', 'Alliance', 'NightElf', 'NightElf', 118, None, 'Ni',
         'Elune\'s Chosen', 'Elves touched by the light of the Moon who answered Tyrande\'s call.',
         'Elune\'s Chosen are elves blessed by the Moon. They walk beside the night elves as Elune\'s watchful servants.',
         [('1.9', 121), ('v12', 118)]),
]


class Look199:
    """What WHE keeps of one gender's catalog entries (the attributes of coa_races.Look):

    skin_types: the texture types of option 0, type 11 first; empty for a gender without skin textures
    skins:      one tuple of paths per skin colour, in skin_types order ([] without skin textures)
    fixed:      {texture type: path} of the other options' first choices and the always-applied textures
    keep:       geosets that stay visible (always-applied ones and each option's first choice)
    driven:     geoset groups (id // 100) the catalog drives; their other geosets above 2000 are hidden"""

    def __init__(self, records):
        textures, groups = {}, {}
        for r in records:
            if r['kind'] == 1:
                textures.setdefault(r['type'], []).append(r)
            elif r['kind'] == 0:
                groups.setdefault(r['type'], []).append(r)
            elif r['kind'] == 2:   # absolute geoset id: its group is id // 100
                groups.setdefault(r['geoset'] // 100, []).append(r)
        # a type whose option 0 textures are all empty (Dreadlord's type 12) is not a skin texture
        self.skin_types = sorted(t for t, rs in textures.items() if any(r['option'] == 0 and r['path'] for r in rs))
        if self.skin_types and (self.skin_types[0] != 11 or len(self.skin_types) > 2):
            raise ValueError('unexpected skin textures: types %s' % self.skin_types)
        self.skins = []
        if self.skin_types:
            colours = sorted({r['choice'] for r in textures[11] if r['option'] == 0})
            by_choice = {t: {r['choice']: r['path'] for r in textures[t] if r['option'] == 0} for t in self.skin_types}
            self.skins = [tuple(by_choice[t].get(c) or by_choice[t][min(by_choice[t])] for t in self.skin_types) for c in colours]
        self.fixed = {}
        for t, rs in textures.items():
            if t in self.skin_types:
                continue
            rs = [r for r in rs if r['path']]
            if rs:
                self.fixed[t] = min(rs, key=lambda r: (r['option'] != ALWAYS, r['option'], r['choice']))['path']
        self.keep, self.driven = set(), set(groups)
        for group, rs in groups.items():
            self.keep.update(r['geoset'] for r in rs if r['option'] == ALWAYS)
            for option in {r['option'] for r in rs if r['option'] != ALWAYS}:
                self.keep.add(min((r for r in rs if r['option'] == option), key=lambda r: r['choice'])['geoset'])


def catalog(path):
    """{gender: Look199} of an EHM1 catalog."""
    by_gender = {}
    for r in coa_races.read_catalog(path):
        by_gender.setdefault(r['gender'], []).append(r)
    return {g: Look199(rs) for g, rs in by_gender.items()}


def look_for(looks, gender):
    """A gender's look; a gender the catalog lacks uses the other's (one body for both)."""
    return looks.get(gender, looks.get(0) or looks.get(1))


# CoA models that would replace a different file of the same name in WHE-common (Elune's Chosen's Nightborne models,
# CoA's own edit of them, against F-034's): copied under these names instead (.skin and .anim files follow the model)
RENAMED = {
    'character\\nightborne\\male\\nightbornemale.m2': 'Character\\Nightborne\\Elune\\Male\\EluneChosenMale.m2',
    'character\\nightborne\\female\\nightbornefemale.m2': 'Character\\Nightborne\\Elune\\Female\\EluneChosenFemale.m2',
}


def target(path):
    """The client path a CoA model is copied to."""
    return RENAMED.get(path.lower(), path)


# races that use one of CoA's two models for both genders (0 male, 1 female): the other model's files are missing
ONE_BODY = {'Titan': 1}


def models(male, female, race):
    """(male model, female model) of a race, given CoA's own."""
    if race.key in ONE_BODY:
        return ((male, female)[ONE_BODY[race.key]],) * 2
    return male, female


def by_key(key):
    return next(r for r in RACES if r.key == key)


def catalog_path(client, race):
    return os.path.join(client, 'Esteria%s.bin' % race.catalog)

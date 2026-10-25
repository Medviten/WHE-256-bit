"""The CoA Custom 1.9 races (Ilusixn's "all race files" package) as WHE sees them, and a reader for their
EsteriaAppearance catalogs. Imported by coa_race_modpaks.py, coa_racials.py and models/coa_race_prep.py.

CoA draws these races with EsteriaAppearance.dll: their CharSections rows are placeholders (HumanMaleSkin00_00) and
the DLL fills the models' creature texture slots (types 11-14) and picks their geosets from the Esteria<Race>.bin
catalog. Without the DLL, WHE keeps the stock customization only:
- the catalog's option 0 (skin colour) becomes the CharSections skin rows; its type 11 texture is the model's
  type 1 (the composited body, kept whole through the client's creatureSkinRaces) and a second option 0 texture
  (type 12) becomes type 8, the skin row's texture_2
- every other option is fixed at its first choice: its texture is written into the model, its geoset stays visible
  and the option's other geosets are hidden

Catalog layout (EHM1): 'EHM1', u32 version, u32 count, then 156-byte records: u32 gender, u32 kind (1 texture,
0 geoset), u32 type (texture type, or geoset group), u32 geoset id (kind 0), u16 option (customization row;
65535 = always applied), u16 choice (65535 for always), i32 -1, i32 -1, char[128] texture path (kind 1)."""
import os
import struct

# key, name, plural, F number, folder slug, side, home, kin, male only, CoA race id, catalog name, helmet prefix,
# model folder(s) in the CoA package, male model, female model (None: male only), display scale,
# faction name, faction description, race info
RACES = [
    ('Hozen', 'Hozen', 'Hozen', 64, 'hozen', 'Alliance', 'Human', 'Tauren', True, 112, 'Hozen', 'Hu',
     ['custom/hozen'], 'custom\\hozen\\unknown\\536927.m2', None, 1.15,
     'Hozen of the Jade Forest', 'Hozen who left the Jade Forest to see the wider world, and stayed for the bananas.',
     'The hozen are a boisterous race of monkey-like people from Pandaria. Quick to anger and quicker to laugh, a few tribes have thrown in with the Alliance.'),
    ('Sylvari', 'Sylvari', 'Sylvari', 65, 'sylvari', 'Alliance', 'NightElf', 'NightElf', False, 110, 'Vorkai', 'Be',
     ['custom/vorkai'], 'custom\\vorkai\\fmm\\faunmale.m2', 'custom\\vorkai\\fnf00\\faunfemale.m2', 1.0,
     'Grove Wardens', 'Fauns and dryads of the forest who guard the groves beside the night elves.',
     'Fleet-footed children of the forest, the sylvari tend the wild groves and answer the call of the Cenarion Circle.'),
    ('Mantid', 'Mantid', 'Mantid', 66, 'mantid', 'Horde', 'Tauren', 'Tauren', True, 106, 'Mantid', 'Be',
     ['custom/mantid'], 'custom\\mantid\\mt00\\mantid.m2', None, 1.0,
     'Klaxxi Exiles', 'Mantid paragons who broke with the Empress and found a new hive in the Horde.',
     'The mantid are an ancient insectoid empire of Pandaria. A handful of exiles have turned their blades to the Horde\'s cause.'),
    ('Ethereal', 'Ethereal', 'Ethereals', 67, 'ethereal', 'Alliance', 'NightElf', 'Draenei', True, 109, 'Ethereal', 'Be',
     ['custom/ethereal'], 'custom\\ethereal\\e\\etherial.m2', None, 1.0,
     'Consortium Envoys', 'Ethereal traders who offer the Alliance their wares and their blades.',
     'Ethereals are beings of pure energy bound in wrappings, refugees of a world consumed by the Void. They trade in secrets and arcane relics.'),
    ('Kyrian', 'Kyrian', 'Kyrian', 68, 'kyrian', 'Alliance', 'NightElf', 'Draenei', False, 107, 'Kyrian', 'Dr',
     ['custom/kyrian'], 'custom\\kyrian\\native\\kyrianmale.m2', 'custom\\kyrian\\native\\kyrianfemale.m2', 0.7,
     'Ascended of Bastion', 'Winged stewards of Bastion who left the Path of Ascension to guard the living.',
     'The kyrian are winged souls of Bastion who shepherd the dead. Some have taken up arms beside the Alliance.'),
    ('Venthyr', 'Venthyr', 'Venthyr', 69, 'venthyr', 'Horde', 'Undead', 'Undead', False, 101, 'Venthyr', 'Sc',
     ['custom/venthyr'], 'custom\\venthyr\\native\\vampire_male.m2', 'custom\\venthyr\\native\\vampire_female.m2', 0.75,
     'Court of Harvesters', 'Venthyr nobles of Revendreth who found kindred spirits among the Forsaken.',
     'The venthyr are the gothic aristocracy of Revendreth, who cleanse prideful souls of their sins. A few have found common cause with the Forsaken.'),
    # one body, kept for both genders (CoA: female only); two model rows so the core does not make it male only
    ('Banshee', 'Banshee', 'Banshees', 70, 'banshee', 'Horde', 'Undead', 'Undead', False, 90, 'Banshee', 'Be',
     ['Creature/Banshee'], 'Creature\\Banshee\\BansheePlayer.m2', 'Creature\\Banshee\\BansheePlayer.m2', 0.98,
     'Wailing Sisterhood', 'Banshees freed from the Scourge who serve the Banshee Queen.',
     'Banshees are the tormented spirits of elven women, bound to wail for eternity. Those freed from the Lich King now serve the Banshee Queen.'),
    ('FacelessOne', 'Faceless One', 'Faceless Ones', 71, 'faceless-one', 'Horde', 'Orc', 'Undead', True, 87, 'Faceless', 'Gn',
     ['Creature/FacelessOne'], 'Creature\\FacelessOne\\FacelessPlayer.m2', None, 1.5,
     'The Unspoken', 'Faceless ones who slipped the whispers of the Old Gods and serve the Horde in silence.',
     'The faceless ones are servants of the Old Gods, creatures of the deep places of the world. Few know why some have turned against their masters.'),
]
RACE_IDS = {'Hozen': 56, 'Sylvari': 57, 'Mantid': 58, 'Ethereal': 59, 'Kyrian': 60, 'Venthyr': 61, 'Banshee': 62, 'FacelessOne': 63}

# F-057's Centaur switches from WallCraft's converted Vanilla model to CoA's retail one (Horde centaur, CoA race 102)
CENTAUR = ('Centaur', 'Centaur', 'Centaur', 57, 'centaur', 'Horde', 'Tauren', 'Tauren', False, 102, 'Centaur', 'Ta',
           ['custom/centaur'], 'custom\\centaur\\unknown\\4036647.m2', 'custom\\centaur\\unknown\\4081379.m2', 1.6,
           'Gelkis Clan', 'Centaur of Desolace who honour the earth and made peace with the tauren.', '')

ALWAYS = 0xFFFF
HIDDEN_GEOSET = 1999   # in the 0-2000 range the character code hides and never shows again


def read_catalog(path):
    """Records of an EHM1 catalog as dicts: gender, kind, type, geoset, option, choice, path."""
    d = open(path, 'rb').read()
    magic, version, count = struct.unpack_from('<4sII', d)
    if magic != b'EHM1' or len(d) != 12 + 156 * count:
        raise ValueError('%s: not an EHM1 catalog' % path)
    out = []
    for i in range(count):
        o = 12 + 156 * i
        gender, kind, typ, geoset, option, choice = struct.unpack_from('<IIIIHH', d, o)
        name = d[o + 28:o + 156].split(b'\0')[0].decode('latin1')
        out.append(dict(gender=gender, kind=kind, type=typ, geoset=geoset, option=option, choice=choice, path=name))
    return out


class Look:
    """What WHE keeps of one gender's catalog entries.

    skin_types: the texture types of option 0, type 11 first (the CharSections skin row's texture_1, texture_2)
    skins:      one tuple of paths per skin colour, in skin_types order
    fixed:      {texture type: path} of the other options' first choices and the always-applied textures
    keep:       geosets that stay visible (always-applied ones and each option's first choice)
    driven:     geoset groups the catalog drives (their other geosets are hidden)"""

    def __init__(self, records):
        textures, geosets = {}, {}
        for r in records:
            (textures if r['kind'] == 1 else geosets).setdefault(r['type'], []).append(r)
        self.skin_types = sorted(t for t, rs in textures.items() if any(r['option'] == 0 for r in rs))
        if not self.skin_types or self.skin_types[0] != 11 or len(self.skin_types) > 2:
            raise ValueError('unexpected skin textures: types %s' % self.skin_types)
        colours = sorted({r['choice'] for r in textures[11] if r['option'] == 0})
        by_choice = {t: {r['choice']: r['path'] for r in textures[t] if r['option'] == 0} for t in self.skin_types}
        self.skins = [tuple(by_choice[t].get(c, by_choice[t][min(by_choice[t])]) for t in self.skin_types) for c in colours]
        self.fixed = {}
        for t, rs in textures.items():
            if t in self.skin_types:
                continue
            first = min(rs, key=lambda r: (r['option'] != ALWAYS, r['choice']))
            self.fixed[t] = first['path']
        self.keep, self.driven = set(), set(geosets)
        for group, rs in geosets.items():
            always = [r['geoset'] for r in rs if r['option'] == ALWAYS]
            self.keep.update(always)
            options = {r['option'] for r in rs if r['option'] != ALWAYS}
            for option in options:
                self.keep.add(min((r for r in rs if r['option'] == option), key=lambda r: r['choice'])['geoset'])


def catalog(path):
    """{gender: Look} of an EHM1 catalog."""
    by_gender = {}
    for r in read_catalog(path):
        by_gender.setdefault(r['gender'], []).append(r)
    return {g: Look(rs) for g, rs in by_gender.items()}

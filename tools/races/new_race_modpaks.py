#!/usr/bin/env python3
"""Generate the tentative modpaks for the races found in WallCraft's playable race set (F-047..F-054).

The files that only differ by race name come from F-046 (Slime Giant, Horde) and F-045 (Furbolg, Alliance), with the
Home race (classes, start, outfits, bars, stats, totems, druid forms, restricted quests/items) and Kin race (voice,
emotes, names) as variables. Customization rows are generated:
- the stock NPC races (Fel Orc, Skeleton, Forest Troll, Northrend Skeleton, Ice Troll) use the stock 3.3.5 models and
  the customization rows F-008 moved to 160 + race id, read from a built DBFilesClient folder;
- Qiraji, Eredar and Arakkoa use WallCraft's Vanilla models (converted with m2_256_to_264.py) and its donor rows, read
  from its Shared\\DBC folder.

usage: new_race_modpaks.py <built DBFilesClient> <WallCraft Shared/DBC/Assets/DBFilesClient> [modpaks dir] [output dir]

coa_race_modpaks.py imports this module and sets BUILT, DONOR, MODPAKS and OUTPUT itself."""
import glob, os, re, struct, sys

BUILT = DONOR = MODPAKS = OUTPUT = None
TEMPLATE = {'Horde': ('F-046', 'SlimeGiant', 'Slime Giant'), 'Alliance': ('F-045', 'Furbolg', 'Furbolg')}

# key, name, plural, F number, folder slug, side, home, kin, male only, model source, customization source, client
# prefix, faction name, faction description, race info
RACES = [
    ('FelOrc', 'Fel Orc', 'Fel Orcs', 47, 'fel-orc', 'Horde', 'Orc', 'Orc', False, ('stock', 2299, 2298), ('npc', 172), 'Or',
     'Fel Horde', 'Orcs who drank the blood of Mannoroth and broke free of the Legion.',
     'Fel orcs are orcs corrupted by demonic blood, their skin burned red by fel energy.'),
    ('Skeleton', 'Skeleton', 'Skeletons', 48, 'skeleton', 'Horde', 'Undead', 'Undead', False, ('stock', 2369, 2370), ('npc', 175), 'Sc',
     'Bonewalkers', 'Restless skeletons who answer to the Banshee Queen rather than the Lich King.',
     'Skeletons are the bare-boned dead, raised by necromancy and freed from the Scourge.'),
    ('ForestTroll', 'Forest Troll', 'Forest Trolls', 49, 'forest-troll', 'Horde', 'Troll', 'Troll', True, ('stock', 2613, None), ('npc', 178), 'Tr',
     'Revantusk Tribe', 'Forest trolls of the Hinterlands, allied with the Horde.',
     'Forest trolls once ruled the Amani empire of Quel\'Thalas. Some tribes now fight beside the Horde.'),
    ('NorthrendSkeleton', 'Northrend Skeleton', 'Northrend Skeletons', 50, 'northrend-skeleton', 'Horde', 'Undead', 'Undead', True, ('stock', 2940, None), ('npc', 180), 'Sc',
     'Bonewalkers of Northrend', 'Skeletal warriors of Northrend who broke free of the Lich King.',
     'The skeletal warriors of Northrend were raised from the fallen of the frozen north.'),
    ('IceTroll', 'Ice Troll', 'Ice Trolls', 51, 'ice-troll', 'Horde', 'Troll', 'Troll', True, ('stock', 2942, None), ('npc', 181), 'Tr',
     'Frostmane Exiles', 'Ice trolls who left their tribes to join the Horde.',
     'Ice trolls dwell in the coldest reaches of Azeroth, from Dun Morogh to Zul\'Drak.'),
    ('Qiraji', 'Qiraji', 'Qiraji', 52, 'qiraji', 'Horde', 'Orc', 'Orc', False,
     ('converted', 'Character\\\\Qiraji\\\\Male\\\\QirajiMale.mdx', 'Character\\\\Qiraji\\\\Female\\\\QirajiFemale.mdx'), ('donor', 26), 'Ni',
     'Swarm of the Sands', 'Qiraji who broke from C\'Thun\'s hive mind and fled Ahn\'Qiraj.',
     'The qiraji are the insectoid servants of C\'Thun. A few have broken free of the Old God\'s will.'),
    ('Eredar', 'Eredar', 'Eredar', 53, 'eredar', 'Alliance', 'Draenei', 'Draenei', False,
     ('converted', 'Character\\\\Eredar\\\\Male\\\\Eredar.mdx', 'Character\\\\Eredar\\\\Female\\\\EredarFemale.mdx'), ('donor', 29), 'Dr',
     'Eredar Penitents', 'Eredar who renounced the Legion and seek redemption among the draenei.',
     'The eredar are the ancestors of the draenei. Most serve the Burning Legion; a few have turned from it.'),
    ('Arakkoa', 'Arakkoa', 'Arakkoa', 54, 'arakkoa', 'Alliance', 'Draenei', 'Draenei', True,
     ('converted', 'Character\\\\Arakkoa\\\\Male\\\\Arakkoa.mdx', None), ('donor', 30), 'Hu',
     'Arakkoa Outcasts', 'Arakkoa of Terokkar Forest who stand with the Alliance.',
     'The arakkoa are a race of bird-like humanoids from Draenor, steeped in arcane and shadow magic.'),
]

# WallCraft's unregistered models (no race slot or customization rows): skins per gender as (texture_1, texture_2)
def skins(folder, names, alpha=None):
    return [('Character\\%s\\%s.blp' % (folder, n), ('Character\\%s\\%s%s.blp' % (folder, n, alpha)) if alpha else '') for n in names]

RACES += [
    ('FelElf', 'Fel Elf', 'Fel Elves', 55, 'fel-elf', 'Horde', 'BloodElf', 'BloodElf', False,
     ('converted', 'Character\\\\FelElf\\\\Male\\\\FelElfWarriorMale.mdx', 'Character\\\\FelElf\\\\Female\\\\FelElfCasterFemale.mdx'),
     ('skins', {0: skins('FelElf\\Male', ['FelElfWarriorMaleSkinPurple', 'FelElfWarriorMaleSkinRed', 'FelElfWarriorMaleSkinWhite', 'FelElfMaleSkin00_00']),
                1: skins('FelElf\\Female', ['FelElfCasterFemaleSkinViolet', 'FelElfCasterFemaleSkinBlack', 'FelElfCasterFemaleSkinLightBlue', 'FelElfFemaleSkin00_00'])}), 'Be',
     'Illidari Exiles', 'Fel elves who left Illidan\'s service and returned to their kin in the Horde.', ''),
    ('Quillboar', 'Quillboar', 'Quillboar', 56, 'quillboar', 'Horde', 'Tauren', 'Tauren', False,
     ('converted', 'Character\\\\Quillboar\\\\Male\\\\QuillBoar.mdx', 'Character\\\\Quillboar\\\\Female\\\\QuillBoarCaster.mdx'),
     ('skins', {0: skins('Quillboar\\Male', ['QuilBoarSkin', 'QuilBoarSkinBlack', 'QuilBoarSkinGrey', 'QuilBoarSkinWhite', 'QuilBoarSkinDeathsHead', 'QuilBoarSkinZombie',
                                             'QuilBoarSkinArmoredBlack', 'QuilBoarSkinArmoredBrown', 'QuilBoarSkinArmoredGrey', 'QuilBoarSkinArmoredWhite',
                                             'QuilBoarSkinArmoredDeathsHead', 'QuilBoarSkinArmoredZombie'], '_Alpha'),
                1: skins('Quillboar\\Female', ['QuilBoarCasterSkinBrown', 'QuilBoarCasterSkinBeige', 'QuilBoarCasterSkinBlack', 'QuilBoarCasterSkinPink'], '_Alpha')}), 'Ta',
     'Bristleback Outcasts', 'Quillboar of the Barrens who broke with Agamaggan\'s war against the Horde.', ''),
    ('Centaur', 'Centaur', 'Centaur', 57, 'centaur', 'Horde', 'Tauren', 'Tauren', False,
     ('converted', 'Character\\\\Centaur\\\\Male\\\\Centaur.mdx', 'Character\\\\Centaur\\\\Female\\\\CentaurCaster.mdx'),
     ('skins', {0: skins('Centaur\\Male', ['CentaurSkin', 'CentaurSkinBlack', 'CentaurSkinDarkgray', 'CentaurSkinGray', 'CentaurSkinWhite', 'CentaurSkinYellow']),
                1: skins('Centaur\\Female', ['CentaurCasterSkinBrown', 'CentaurCasterSkinBlack', 'CentaurCasterSkinGray', 'CentaurCasterSkinWhite', 'CentaurCasterSkinYellow'], '_Alpha')}), 'Ta',
     'Gelkis Clan', 'Centaur of Desolace who honour the earth and made peace with the tauren.', ''),
    ('Demon', 'Demon', 'Demons', 58, 'demon', 'Horde', 'BloodElf', 'BloodElf', True,
     ('converted', 'Character\\\\DemonForm\\\\DemonForm.mdx', None),
     ('skins', {0: [('Creature\\DemonForm\\WarlockDemonForm1.blp', '')]}), 'Be',
     'Illidari', 'Demonic followers of Illidan who fight the Legion alongside the Horde.', ''),
    ('Satyr', 'Satyr', 'Satyrs', 59, 'satyr', 'Alliance', 'NightElf', 'NightElf', False,
     ('converted', 'Character\\\\Satyr\\\\Male\\\\Satyr.mdx', 'Character\\\\Satyr\\\\Female\\\\CrystalSatyr.mdx'),
     ('skins', {0: skins('Satyr\\Male', ['SatyrSkinGreen', 'SatyrSkinAlbino', 'SatyrSkinBlue', 'SatyrSkinCrimson', 'SatyrSkinPink', 'SatyrSkinRed', 'SatyrSkinTurquoise',
                                         'SatyrSkinViolet', 'SatyrSkinYellow'], 'Alpha'),
                1: [('Character\\Satyr\\Female\\CrystalSatyrPurple.blp', 'Character\\Satyr\\Female\\CrystalSatyrglow.blp'),
                    ('Character\\Satyr\\Female\\CrystalSatyrWhite.blp', 'Character\\Satyr\\Female\\CrystalSatyrglow.blp')]}), 'Ni',
     'Redeemed Satyrs', 'Satyrs who seek to undo their corruption under the eyes of the Cenarion Circle.', ''),
    ('Gnoll', 'Gnoll', 'Gnolls', 60, 'gnoll', 'Alliance', 'Human', 'Human', False,
     ('converted', 'Character\\\\Gnoll\\\\Male\\\\gnoll.mdx', 'Character\\\\Gnoll\\\\Male\\\\gnoll.mdx'),   # one model, two skin sets
     ('skins', {0: skins('Gnoll\\Male', ['Gnollskin', 'GnollskinBlue', 'GnollskinGrey', 'GnollskinMagenta', 'GnollskinOrange', 'GnollskinRed']),
                1: skins('Gnoll\\Female', ['RiverPawGnollWhelpSkin', 'MossHideGnollWhelpSkin', 'RedRidgeGnollWhelpSkin', 'RothideGnollWhelpSkin', 'ShadowHideGnollWhelpSkin'])}), 'Hu',
     'Riverpaw Mercenaries', 'Gnolls who sell their spears to Stormwind instead of raiding its farms.', ''),
    ('Beholder', 'Beholder', 'Beholders', 61, 'beholder', 'Alliance', 'Gnome', 'Gnome', True,
     ('converted', 'Character\\\\Beholder\\\\Beholder.mdx', None),
     ('skins', {0: skins('Beholder', ['BeholderGreen', 'BeholderBeige', 'BeholderBlack', 'BeholderBlue', 'BeholderGray', 'BeholderRed'])}), 'Gn',
     'The All-Seeing', 'Beholders bound to the gnomes of Gnomeregan by an ancient pact.', ''),
    ('Shivan', 'Shivan', 'Shivan', 62, 'shivan', 'Alliance', 'Draenei', 'Draenei', True,
     ('converted', 'Character\\\\Shivan\\\\Shivan.mdx', None),
     ('skins', {0: skins('Shivan', ['ShivanSkin', 'ShivanSkin_Black', 'ShivanSkin_Blue', 'ShivanSkin_Green', 'ShivanSkin_Red'])}), 'Dr',
     'Shivarra Penitents', 'Shivarra who turned from the Burning Legion and serve the Naaru.', ''),
]
HOME_MODELS = {'Human': (49, 50), 'Orc': (51, 52), 'NightElf': (55, 56), 'Undead': (57, 58), 'Tauren': (59, 60), 'Gnome': (182, 183),
               'Troll': (185, 186), 'BloodElf': (2208, 2209), 'Draenei': (2248, 2250)}
HOME_DISPLAYS = {'Human': (49, 50), 'Orc': (51, 52), 'NightElf': (55, 56), 'Undead': (57, 58), 'Tauren': (59, 60), 'Gnome': (1563, 1564),
                 'Troll': (1478, 1479), 'BloodElf': (15476, 15475), 'Draenei': (16125, 16126)}
SECTIONS = {0: '@Skin', 1: '@Face', 2: '@FacialHair', 3: '@Hair', 4: '@Underwear'}
# Skin textures shipped with a donor race but missing from its CharSections rows: extra skin colours (donor race, gender)
EXTRA_SKINS = {(30, 0): ['Arakkoa_Blue', 'Arakkoa_Gray', 'Arakkoa_Green', 'Arakkoa_Yellow', 'ArakkoaGreen', 'ArakkoaPurple', 'ArakkoaYellow']}
OUTFIT_FALLBACK = {'Horde': ['Orc', 'Troll', 'Undead', 'Tauren', 'BloodElf'], 'Alliance': ['Human', 'Dwarf', 'NightElf', 'Gnome', 'Draenei']}


def load_dbc(path):
    d = open(path, 'rb').read()
    n, f, size, ss = struct.unpack_from('<4I', d, 4)
    rows = [d[20 + i * size:20 + (i + 1) * size] for i in range(n)]
    strings = d[20 + n * size:]
    return rows, strings, f


def template_dir(fnum):
    return next(os.path.join(MODPAKS, d) for d in os.listdir(MODPAKS) if d.startswith(fnum + '_'))


def string(strings, offset):
    return strings[offset:strings.index(b'\0', offset)].decode('latin1')


def sql_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


PLAYER_FLAGS = {}   # (gender, section, type, colour) -> flags of the source rows that are already player rows


def customization(source):
    """(charsections, hair geosets, facial hair styles) rows of a stock NPC race, a WallCraft donor race or a skin list."""
    kind, race = source
    if kind == 'skins':   # no rows: the skins, one bald hair style and one facial style; the other sections are filled below
        sections = [(g, 0, 0, c, [t1, t2, '']) for g, ss in race.items() for c, (t1, t2) in enumerate(ss)]
        hair = [(g, 0, 0, 0) for g in race]
        facial = [(g, 0, 0, 0, 0, 0, 0) for g in race]
        return fill(sorted(sections)), hair, facial
    folder = BUILT if kind == 'npc' else DONOR
    rows, strings, f = load_dbc(os.path.join(folder, 'CharSections.dbc'))
    sections = []
    PLAYER_FLAGS.clear()
    for r in rows:
        v = struct.unpack_from('<10I', r)
        if v[1] != race:
            continue
        if kind == 'npc':   # 3.3.5: id, race, gender, section, texture 1-3, flags, type, colour
            gender, section, tex, var, colour = v[2], v[3], v[4:7], v[8], v[9]
            if v[7] & 1:   # a playable race's rows (a Home race copy): keep its flags (NPC-only skins, Death Knight skins)
                PLAYER_FLAGS[(gender, section, var, colour)] = v[7]
        else:               # WallCraft (Vanilla): id, race, gender, section, type, colour, texture 1-3, flags
            gender, section, var, colour, tex = v[2], v[3], v[4], v[5], v[6:9]
        tex = [string(strings, o).strip() for o in tex]
        tex = [t.replace('Character\\FelOrc\\FemaleFelOrc', 'Character\\FelOrc\\Female\\FelOrc') for t in tex]   # stock typo
        sections.append((gender, section, var, colour, tex))
    for (donor, gender), skins in EXTRA_SKINS.items():
        if kind == 'donor' and donor == race:
            base = next(s for s in sections if s[0] == gender and s[1] == 0)[4][0]
            first = 1 + max(s[3] for s in sections if s[0] == gender and s[1] == 0)
            sections += [(gender, 0, 0, first + i, [base.rsplit('\\', 1)[0] + '\\' + n + '.blp', '', '']) for i, n in enumerate(skins)]
    rows, _, _ = load_dbc(os.path.join(folder, 'CharHairGeosets.dbc'))
    hair = sorted(struct.unpack_from('<6i', r)[2:] for r in rows if struct.unpack_from('<I', r, 4)[0] == race)
    rows, _, f = load_dbc(os.path.join(folder, 'CharacterFacialHairStyles.dbc'))
    facial = []
    for r in rows:
        v = struct.unpack_from('<%di' % f, r)
        if v[0] == race:   # race, gender, variation, geosets (stock pads with 0xCCCCCCCC: keep the first 5, real ones only)
            facial.append((v[1], v[2]) + tuple(g if g != -858993460 else 0 for g in v[3:8]))
    return fill(sorted(sections)), hair, sorted(facial)


def fill(sections):
    """Character creation expects every section: empty faces and underwear for each skin colour, one empty hair and facial
    hair row where a race has none (as F-044/F-046 do for models without them)."""
    for gender in sorted({s[0] for s in sections}):
        have = {(s[1], s[2], s[3]) for s in sections if s[0] == gender}
        colours = sorted({s[3] for s in sections if s[0] == gender and s[1] == 0}) or [0]
        for section in (1, 4):
            if not any(h[0] == section for h in have):
                sections += [(gender, section, 0, c, ['', '', '']) for c in colours]
        for section in (2, 3):
            if not any(h[0] == section for h in have):
                sections.append((gender, section, 0, 0, ['', '', '']))
    return sorted(sections)


def from_template(side, fnum, key, name, plural, home, text):
    tf, tkey, tname = TEMPLATE[side]
    text = text.replace(tf, 'F-0%d' % fnum).replace('@' + tkey, '@' + key)
    text = text.replace(tname + 's', plural).replace(tname, name)
    # F-046's Home race is Orc, F-045's Night Elf
    thome = 'Orc' if side == 'Horde' else 'NightElf'
    text = re.sub(r'@%s(Mask|FireTotem|EarthTotem|WaterTotem|AirTotem)\b' % thome, r'@%s\1' % home, text)
    text = text.replace('(as Orcs)', '(as %s)' % home).replace('(as Night Elves)', '(as %s)' % home)
    text = text.replace('Home race (Orc)', 'Home race (%s)' % home)
    return text


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text if text.endswith('\n') else text + '\n')


def main():
    for key, name, plural, fnum, slug, side, home, kin, male_only, model, source, prefix, fname, fdesc, info in RACES:
        out = os.path.join(OUTPUT, 'F-0%d_mod-playable-%s' % (fnum, slug))
        tdir = template_dir('F-046')
        tag = '[BASE,F-0%d]' % fnum
        generated = {'charsections', 'charhairgeosets', 'characterfacialhairstyles', 'barbershopstyle', 'creaturemodeldata',
                     'creaturedisplayinfo', 'creature_model_info', 'player_totem_model', 'charstartoutfit'}
        for sub in ('dbc', os.path.join('sql', 'db-world', 'base')):
            for f in sorted(os.listdir(os.path.join(tdir, sub))):
                table = f.split(']_', 1)[1][:-4]
                if table in generated:
                    continue
                if side == 'Alliance' and table in ('faction', 'factiontemplate'):   # Alliance reputation and faction groups
                    text = open(os.path.join(template_dir('F-045'), sub, '[BASE,F-045]_%s.sql' % table), encoding='utf-8').read()
                    text = from_template('Alliance', fnum, key, name, plural, home, text).replace('copied from Kul Tiran (Gnome)', 'Alliance faction groups (as Gnome)')
                else:
                    text = from_template('Horde', fnum, key, name, plural, home, open(os.path.join(tdir, sub, f), encoding='utf-8').read())
                write(os.path.join(out, sub, '%s_%s.sql' % (tag, table)), text)

        sections, hair, facial = customization(source)
        genders = ['@Male'] if male_only else ['@Male', '@Female']
        # In a male-only race the female slot shows the male body: give it the male rows
        rows_for = lambda g: [s for s in sections if s[0] == (0 if male_only else g)]
        lines = []
        for gi, g in enumerate(genders if not male_only else ['@Male', '@Female']):
            for gender, section, var, colour, tex in rows_for(gi):
                flags = PLAYER_FLAGS.get((gender, section, var, colour), 1 if section == 1 else 17)
                lines.append("(@CharSectionsID := @CharSectionsID +1, @%s, %-7s %-12s %s, %s, %s, %d, %d, %d)" % (
                    key, g + ',', SECTIONS[section] + ',', sql_str(tex[0]), sql_str(tex[1]), sql_str(tex[2]), flags, var, colour))
        origin = {'npc': lambda: 'the stock NPC race rows (race %d after F-008)' % source[1],
                  'donor': lambda: 'WallCraft\'s donor rows (race %d)' % source[1],
                  'skins': lambda: 'the skin textures shipped with the model (WallCraft has no rows for it)'}[source[0]]()
        write(os.path.join(out, 'dbc', tag + '_charsections.sql'),
              "-- charsections: %d inserts, 0 updates, 0 deletes\n-- From %s, flagged for character creation (17, faces 1)%s\n\n"
              "-- New entries\nDELETE FROM `charsections` WHERE `race` = @%s;\nSET @CharSectionsID = (SELECT COALESCE(MAX(id), 0) FROM `charsections`);\n"
              "INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES\n%s;"
              % (len(lines), origin, '; male-only race: the female slot gets the male rows' if male_only else '', key, ',\n'.join(lines)))

        lines = []
        for gi, g in enumerate(['@Male', '@Female']):
            for gender, var, geoset, scalp in [h for h in hair if h[0] == (0 if male_only else gi)]:
                lines.append("(@CharHairGeosetsID := @CharHairGeosetsID +1, @%s, %-8s %2d, %2d, %d)" % (key, g + ',', var, geoset, scalp))
        write(os.path.join(out, 'dbc', tag + '_charhairgeosets.sql'),
              "-- charhairgeosets: %d inserts, 0 updates, 0 deletes (from %s)\n\n-- New entries\nDELETE FROM `charhairgeosets` WHERE `race` = @%s;\n"
              "SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);\n"
              "INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES\n%s;" % (len(lines), origin, key, ',\n'.join(lines)))

        lines = []
        for gi, g in enumerate(['@Male', '@Female']):
            for row in [h for h in facial if h[0] == (0 if male_only else gi)]:
                lines.append("(@%s, %-8s %2d, %s)" % (key, g + ',', row[1], ', '.join('%d' % x for x in row[2:7])))
        write(os.path.join(out, 'dbc', tag + '_characterfacialhairstyles.sql'),
              "-- characterfacialhairstyles: %d inserts, 0 updates, 0 deletes (from %s)\n\n-- New entries\n"
              "DELETE FROM `characterfacialhairstyles` WHERE `race` = @%s;\n"
              "INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES\n%s;"
              % (len(lines), origin, key, ',\n'.join(lines)))

        # Barber shop: one generic entry per hair style and facial style
        cols = ', '.join(['`id`', '`type`'] + ['`display_name_%s`' % l for l in ('enus', 'kokr', 'frfr', 'dede', 'zhcn', 'zhtw', 'eses', 'esmx', 'ruru', 'jajp', 'ptpt', 'itit', 'unused_1', 'unused_2', 'unused_3', 'unused_4')]
                         + ['`display_name_flags`'] + ['`description_%s`' % l for l in ('enus', 'kokr', 'frfr', 'dede', 'zhcn', 'zhtw', 'eses', 'esmx', 'ruru', 'jajp', 'ptpt', 'itit', 'unused_1', 'unused_2', 'unused_3', 'unused_4')]
                         + ['`description_flags`', '`cost_modifier`', '`race`', '`gender`', '`data`'])
        lines = []
        for gi, g in enumerate(['@Male', '@Female']):
            src = 0 if male_only else gi
            for t, label, variations in ((0, 'Style', sorted({h[1] for h in hair if h[0] == src})), (2, 'Facial Style', sorted({h[1] for h in facial if h[0] == src}))):
                for v in variations:
                    lines.append("(@BarbershopStyleID := @BarbershopStyleID +1, %d, '%s %d', %s, 16712190, %s, 16712172, '%s', @%s, %s, %d)" % (
                        t, label, v + 1, ', '.join(["''"] * 15), ', '.join(["''"] * 16), '1.0000000000000000' if t == 0 else '0.7500000000000000', key, g, v))
        write(os.path.join(out, 'dbc', tag + '_barbershopstyle.sql'),
              "-- barbershopstyle: %d inserts, 0 updates, 0 deletes\n-- type 0 = hair style, type 2 = facial hair; generic names\n\n-- New entries\n"
              "DELETE FROM `barbershopstyle` WHERE `race` = @%s;\nSET @BarbershopStyleID = (SELECT COALESCE(MAX(id), 0) FROM `barbershopstyle`);\n"
              "INSERT INTO `barbershopstyle` (%s) VALUES\n%s;" % (len(lines), key, cols, ',\n'.join(lines)))

        # Model data: the stock model rows (stock races) or the Home race's (converted models), with player model flags
        cmd_cols = ['`size_class`', '`model_scale`', '`blood_id`', '`footprint_texture_id`', '`footprint_texture_length`', '`footprint_texture_width`',
                    '`footprint_particle_scale`', '`foley_material_id`', '`footstep_shake_size`', '`death_thud_shake_size`', '`sound_data`', '`collision_width`',
                    '`collision_height`', '`mount_height`', '`geo_box_min_x`', '`geo_box_min_y`', '`geo_box_min_z`', '`geo_box_max_x`', '`geo_box_max_y`', '`geo_box_max_z`',
                    '`world_effect_scale`', '`attached_effect_scale`', '`missile_collision_radius`', '`missile_collision_push`', '`missile_collision_raise`']
        home_models = HOME_MODELS[home]
        parts = []
        for g, gi in (('Male', 0), ('Female', 1)):
            if male_only and gi:
                continue
            if model[0] == 'stock':
                src, path = model[1 + gi], '`model_path`'
                note = 'stock model %d' % src
            else:
                src, path = home_models[gi], "@%s%sModelPath" % (key, g)
                note = '%s %s model %d' % (home, g.lower(), src)
            parts.append("SELECT @%s%sModel, 2052, %s, %s FROM `creaturemodeldata` WHERE `id` = %d /* %s */" % (key, g, path, ', '.join(cmd_cols), src, note))
        ids = '@%sMaleModel' % key + ('' if male_only else ', @%sFemaleModel' % key)
        write(os.path.join(out, 'dbc', tag + '_creaturemodeldata.sql'),
              "-- creaturemodeldata: %d inserts, 0 updates, 0 deletes\n-- %s, with the player model flags (0x804)%s\n\n"
              "DELETE FROM `creaturemodeldata` WHERE `id` IN (%s);\nINSERT INTO `creaturemodeldata` (`id`, `flags`, `model_path`, %s)\n%s;"
              % (len(parts), 'Copies of the stock model rows' if model[0] == 'stock' else 'Size, collision and sounds of the %s models' % home,
                 '. Male-only race: one model for both displays' if male_only else '', ids, ', '.join(cmd_cols), '\nUNION ALL\n'.join(parts)))

        female_model = '@%sMaleModel' % key if male_only else '@%sFemaleModel' % key
        write(os.path.join(out, 'dbc', tag + '_creaturedisplayinfo.sql'),
              "-- creaturedisplayinfo: 2 inserts, 0 updates, 0 deletes\n\n-- New entries\n"
              "DELETE FROM `creaturedisplayinfo` WHERE `id` IN (@{k}MaleDisplay, @{k}FemaleDisplay);\n"
              "INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, `creature_model_scale`, `creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, `texture_variation_3`, `portrait_texture_name`, `blood_level`, `blood_id`, `npc_sound_id`, `praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`) VALUES\n"
              "(@{k}MaleDisplay,   @{k}MaleModel, 0, @{k}MaleDisplayExtra,   '1.0000000000000000', 255, '', '', '', '', 3, 0, 0, 0, 0, 0),\n"
              "(@{k}FemaleDisplay, {fm}, 0, @{k}FemaleDisplayExtra, '1.0000000000000000', 255, '', '', '', '', 3, 0, 0, 0, 0, 0);{c}".format(
                  k=key, fm=female_model, c=' -- male-only race' if male_only else ''))

        home_displays = HOME_DISPLAYS[home]
        write(os.path.join(out, 'sql', 'db-world', 'base', tag + '_creature_model_info.sql'),
              "/* Model info for the player displays: bounding radius and combat reach of the %s displays%s */\n"
              "DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@{k}MaleDisplay, @{k}FemaleDisplay);\n".format(k=key) % (
                  home, ' (male-only race: both displays are male)' if male_only else '') +
              "INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`)\n"
              "SELECT @{k}MaleDisplay,   `BoundingRadius`, `CombatReach`, 0, 0 FROM `creature_model_info` WHERE `DisplayID` = {m}\nUNION ALL\n"
              "SELECT @{k}FemaleDisplay, `BoundingRadius`, `CombatReach`, {fg}, 0 FROM `creature_model_info` WHERE `DisplayID` = {f};".format(
                  k=key, m=home_displays[0], f=home_displays[0] if male_only else home_displays[1], fg=0 if male_only else 1))

        # F-026 gives every race without totems its faction's (Orc for the Horde, Dwarf for the Alliance): only Home
        # races with totems of their own need a file
        if home in ('Tauren', 'Troll', 'Draenei'):
            write(os.path.join(out, 'sql', 'db-world', 'base', tag + '_player_totem_model.sql'),
                  "DELETE FROM `player_totem_model` WHERE `RaceID` IN (@{k});\nINSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES\n"
                  "(1, @{k}, @{h}FireTotem),\n(2, @{k}, @{h}EarthTotem),\n(3, @{k}, @{h}WaterTotem),\n(4, @{k}, @{h}AirTotem);".format(k=key, h=home))

        fb = ', '.join('@' + r for r in [home] + [r for r in OUTFIT_FALLBACK[side] if r != home][:4])
        text = from_template('Horde', fnum, key, name, plural, home, open(os.path.join(tdir, 'dbc', '[BASE,F-046]_charstartoutfit.sql'), encoding='utf-8').read())
        text = re.sub(r"FIELD\(`(o`\.`)?race`, [^)]*\)", lambda m: 'FIELD(`%srace`, %s)' % (m.group(1) or '', fb), text)
        text = re.sub(r'-- @%s: .*' % key, '-- @%s: the outfits of @%sHome; classes it lacks come from %s' % (key, key, ', '.join(fb.split(', ')[1:])), text)
        write(os.path.join(out, 'dbc', tag + '_charstartoutfit.sql'), text)

        # the template's own modpak name survives in some file headers
        for f in glob.glob(os.path.join(out, '**', '*.sql'), recursive=True):
            text = open(f, encoding='utf-8').read()
            if 'mod-playable-slime-giant' in text:
                write(f, text.replace('mod-playable-slime-giant', 'mod-playable-' + slug))
        write_variables(out, key, name, plural, fnum, side, home, kin, male_only, model, prefix, fname, fdesc, source)
        write_readme(out, key, name, plural, fnum, slug, side, home, kin, male_only, model, source, prefix)
        print('wrote', out)


def write_variables(out, key, name, plural, fnum, side, home, kin, male_only, model, prefix, fname, fdesc, source):
    text = open(os.path.join(template_dir('F-046'), 'variables.sql'), encoding='utf-8').read()
    text = re.sub(r' *-- race ID \d+ → \d+', '', text)
    text = from_template('Horde', fnum, key, name, plural, home, text)
    faction = 1209 + 2 * (fnum - 47)
    if side == 'Alliance':   # the Alliance mask updates come from F-045
        ally = open(os.path.join(template_dir('F-045'), 'variables.sql'), encoding='utf-8').read()
        block = re.search(r'-- Important variable updates.*?\n\n', ally, re.S).group(0).replace('@Furbolg', '@' + key)
        text = re.sub(r'-- Important variable updates.*?\n\n', lambda m: block, text, flags=re.S)
    misc = ["SET @%sHome = @%s; -- classes, start outfits, start position, action bars, stats, totems and druid forms are copied from this race" % (key, home),
            "SET @%sKin = @%s; -- voice, emotes and names are copied from this race" % (key, kin),
            "SET @%sFlags = @%sFlags;" % (key, home),
            "SET @%sExplorationSound = @%sExplorationSound;" % (key, home),
            "SET @%sCinematicSequence = @%sCinematicSequence;" % (key, home),
            "SET @%sBlood = 1;" % key]
    if model[0] == 'converted':
        misc.append("SET @%sMaleModelPath = '%s'; -- WallCraft model, converted to the 3.3.5 format" % (key, model[1]))
        if not male_only:
            misc.append("SET @%sFemaleModelPath = '%s';" % (key, model[2]))
    misc += ["SET @%sFaction = %d; -- vacant slot" % (key, faction), "SET @%sPlayer = %d; -- vacant slot" % (key, faction + 1)]
    text = re.sub(r'-- Miscellaneous\n(?:SET [^\n]*\n)+', lambda m: '-- Miscellaneous\n' + '\n'.join(misc) + '\n', text)
    # strings: prefix, client string and customization labels from the race's own ChrRaces row
    rows, strings, f = load_dbc(os.path.join(BUILT if source[0] == 'npc' else DONOR, 'ChrRaces.dbc'))
    custom = ('NORMAL', 'NORMAL', 'NORMAL')
    if source[0] == 'npc':
        row = next(r for r in rows if struct.unpack_from('<I', r)[0] == source[1])
        custom = tuple(string(strings, struct.unpack_from('<I', row, 4 * i)[0]) or 'NORMAL' for i in (65, 66, 67))
    text = re.sub(r'(SET @%sClientPrefix\s*= )[^;]*;.*' % key, r"\g<1>'%s'; -- helmet models of this prefix" % prefix, text)
    text = re.sub(r'(SET @%sClientString\s*= )[^;]*;' % key, r"\g<1>'%s';" % key, text)
    for var, val in zip(('FacialHairCustomization1', 'FacialHairCustomization2', 'HairCustomization'), custom):
        text = re.sub(r'(SET @%s%s\s*= )[^;]*;.*' % (key, var), r"\g<1>'%s';" % val, text)
    text = re.sub(r"(SET @%sPlayerenUS\s*= )[^;]*;" % key, lambda m: m.group(1) + sql_str('"PLAYER", %s' % name) + ';', text)
    text = re.sub(r"(SET @%sFactionNameenUS\s*= )[^;]*;" % key, lambda m: m.group(1) + sql_str(fname) + ';', text)
    text = re.sub(r"(SET @%sFactionDescriptionenUS\s*= )[^;]*;" % key, lambda m: m.group(1) + sql_str(fdesc) + ';', text)
    text = re.sub(r"(SET @%sAchievementenUS\s*= )[^;]*;" % key, lambda m: m.group(1) + sql_str('Realm First! Level 80 %s' % name) + ';', text)
    text = re.sub(r"(SET @%sAchievementDescriptionenUS\s*= )[^;]*;" % key, lambda m: m.group(1) + sql_str('First %s on the realm to achieve level 80.' % name) + ';', text)
    # drop the template's own localizations (only enUS is known for these races)
    text = re.sub(r"(SET @%s[A-Za-z0-9]*(koKR|frFR|deDE|zhCN|zhTW|esES|esMX|ruRU|jaJP|ptPT|itIT)\s*= )'[^']*';" % key, r"\g<1>'';", text)
    text = re.sub(r"(SET @%senUS\s*= )'[^']*';" % key, r"\g<1>%s;" % sql_str(name), text)
    text = re.sub(r'-- Placeholder name and description.*', '-- Placeholder name and description', text)
    write(os.path.join(out, 'variables.sql'), text)


def write_readme(out, key, name, plural, fnum, slug, side, home, kin, male_only, model, source, prefix):
    if model[0] == 'stock':
        look = '    - Stock 3.3.5 model and customization (the NPC race rows F-008 moves to %d)' % source[1]
    else:
        look = ('    - WallCraft\'s playable %s model (Vanilla format, converted with m2_256_to_264.py) and its %s'
                % (name, 'donor customization rows' if source[0] == 'donor' else 'skin textures (no customization rows: skin colour only)'))
    lines = ['# mod-worgoblin-high-elf', '## F-0%d_mod-playable-%s' % (fnum, slug), '', '### Features',
             '- Playable %s (%s), race ID set in config.sql%s' % (plural, side, ', male only' if male_only else ''), look,
             '    - Home: %s (classes, start position, start outfits, action bars, stats, totems, druid forms, race-restricted' % home,
             '      quests and items)', '    - Kin: %s (voice, emotes and names, copied at build time)' % kin,
             '    - Helmet prefix \'%s\'' % prefix, '- Generated by `tools/races/new_race_modpaks.py` (tentative, for testing)', '',
             '### Requirements', '- Interface: a race button and the %s entries in `CharacterCreate.lua`, `GlueParent.lua` and `GlueStrings.lua`'
             % key.upper(), '', '### Known Issues', '- Tentative: not tested in game yet', '- No racial abilities yet', '- No racial mount',
             '- Placeholder race icon, racial faction name and description', '- Barber shop styles have generic names',
             '- Character creation camera is not tuned for the model\'s size']
    if male_only:
        lines.append('- Male only: female characters use the male model and customization')
    if model[0] == 'converted':
        lines.append('- Converted Vanilla model: armour may composite oddly (try adding the race to `creatureSkinRaces`)')
    write(os.path.join(out, 'readme.md'), '\n'.join(lines))


if __name__ == '__main__':
    BUILT, DONOR = sys.argv[1], sys.argv[2]
    MODPAKS = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(__file__), '..', '..', 'modpaks')
    OUTPUT = sys.argv[4] if len(sys.argv) > 4 else MODPAKS   # where the new modpaks go (the templates are read from MODPAKS)
    main()

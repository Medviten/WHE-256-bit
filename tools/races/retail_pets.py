#!/usr/bin/env python3
"""Give every race's hunters the starting pet Petopia's chart lists (https://www.wow-petopia.com/guides/starterpetchart.php).

Looks the stock client has use its displays. The rest come from retail (tools/models/retail_fetch.py, converted with
Kalibro's wotlkconv, then m2_unshare_tracks.py; the file ids are in PETS). Each pet is its own tameable creature, copied
from a stock beast of the family it behaves like: 3.3.5 has no Mechanical, Hound, Stag or Direhorn family.

This tool:
- copies the converted creature folders to WHE-common's Creature folder, without replacing any file already there
- writes F-128's dbc/[F-128]_retail_pets.sql (model rows copied from the donor's with the new paths, and the displays),
  its creature templates, and its variables.sql (model and display slots)
- writes each race's player_starting_pet row: the stock races' in F-128, the others' in their own modpak

usage: retail_pets.py <retail_fetch output (for listfile.csv)> <converted folder> <modpaks folder> [WHE-common patch-A.MPQ]"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAMILY = {  # stock tameable beast copied for the creature, and its display (model data, size)
    'wolf': (299, 31049), 'cat': (2031, 11454), 'spider': (1504, 513), 'bear': (1128, 8843), 'boar': (3098, 503),
    'crab': (2231, 1000), 'raptor': (3123, 1959), 'tallstrider': (2955, 1219), 'turtle': (33710, 28819),
    'bird': (1995, 10832), 'dragonhawk': (15650, 17545), 'warpstalker': (18464, 20025), 'serpent': (5048, 4317),
    'moth': (16520, 17574)}
# variable part, name, family, stock display, or retail (model file id, texture file id or 0 for the model's own, scale)
PETS = {
    'Timber': (69100, 'Wolf', 'wolf', 447, None),
    'Boar': (69101, 'Boar', 'boar', None, (3978441, 3978443)),
    'Bear': (69102, 'Bear', 'bear', None, (1266661, 1266697)),
    'Tiger': (69103, 'Cat', 'cat', 9956, None),
    'MineSpider': (69104, 'Spider', 'spider', None, (1513627, 1513656)),
    'Tallstrider': (69105, 'Tallstrider', 'tallstrider', None, (2323979, 2324104)),
    'Rabbit': (69106, 'Mechanical', 'cat', None, (383595, 383594)),
    'Raptor': (69107, 'Raptor', 'raptor', 1959, None),
    'Dragonhawk': (69108, 'Dragonhawk', 'dragonhawk', 17545, None),
    'Moth': (69109, 'Moth', 'moth', 17795, None),
    'Crab': (69110, 'Crab', 'crab', None, (1516641, 1517013)),
    'Mastiff': (69111, 'Hound', 'wolf', None, (320622, 320625)),
    'DarkHound': (69112, 'Hound', 'wolf', None, (2102977, 2102985)),
    'Eagle': (69113, 'Eagle', 'bird', None, (1100483, 1101620)),
    'Falcon': (69114, 'Falcon', 'bird', None, (1738730, 1738736)),
    'Talbuk': (69115, 'Stag', 'boar', None, (1601374, 1601397)),
    'DraenorWolf': (69116, 'Wolf', 'wolf', None, (926251, 926273)),
    'Mechanowolf': (69117, 'Mechanical', 'wolf', None, (1338909, 2565094)),
    'Saber': (69118, 'Cat', 'cat', None, (1093609, 1094383)),
    'DragonTurtle': (69119, 'Turtle', 'turtle', None, (606106, 606105)),
    'VoidStalker': (69120, 'Warp Stalker', 'warpstalker', None, ('creature/warpstalkervoid/warpstalkervoid.m2', 0)),
    'GiantSnake': (69121, 'Serpent', 'serpent', None, (1670968, 1671555)),
    'Direhorn': (69122, 'Direhorn', 'boar', None, (660332, 794644)),
}
STOCK = (('Human', 'Timber'), ('Orc', 'Boar'), ('Dwarf', 'Bear'), ('NightElf', 'Tiger'), ('Undead', 'MineSpider'),
         ('Tauren', 'Tallstrider'), ('Gnome', 'Rabbit'), ('Troll', 'Raptor'), ('BloodElf', 'Dragonhawk'), ('Draenei', 'Moth'))
RACES = (('F-023', 'Goblin', 'Crab'), ('F-024', 'Worgen', 'Mastiff'), ('F-016', 'DarkIronDwarf', 'DarkHound'),
         ('F-028', 'HighmountainTauren', 'Eagle'), ('F-025', 'KulTiran', 'Falcon'), ('F-033', 'LightforgedDraenei', 'Talbuk'),
         ('F-007', 'MagharOrc', 'DraenorWolf'), ('F-040', 'Mechagnome', 'Mechanowolf'), ('F-034', 'Nightborne', 'Saber'),
         ('F-020', 'AlliancePandaren', 'DragonTurtle'), ('F-021', 'HordePandaren', 'DragonTurtle'),
         ('F-035', 'VoidElf', 'VoidStalker'), ('F-019', 'Vulpera', 'GiantSnake'), ('F-017', 'ZandalariTroll', 'Direhorn'))
CMD_COLUMNS = ('`size_class`, `model_scale`, `blood_id`, `footprint_texture_id`, `footprint_texture_length`, '
               '`footprint_texture_width`, `footprint_particle_scale`, `foley_material_id`, `footstep_shake_size`, '
               '`death_thud_shake_size`, `sound_data`, `collision_width`, `collision_height`, `mount_height`, '
               '`geo_box_min_x`, `geo_box_min_y`, `geo_box_min_z`, `geo_box_max_x`, `geo_box_max_y`, `geo_box_max_z`, '
               '`world_effect_scale`, `attached_effect_scale`, `missile_collision_radius`, `missile_collision_push`, '
               '`missile_collision_raise`')


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text if text.endswith('\n') else text + '\n')


def row(race, key):
    entry, name = PETS[key][:2]
    return ("(@%s, %d)" % (race, entry), name)


def install(converted, common):
    """Adds what's missing: some folders (dragonturtle, triceratops, mechanicalrabbit) already serve other modpaks."""
    added = kept = 0
    src_root = os.path.join(converted, 'creature')
    for root, _, files in os.walk(src_root):
        rel = os.path.relpath(root, src_root)
        dest = os.path.join(common, 'Creature', rel)
        for f in files:
            d = os.path.join(dest, f)
            if os.path.exists(d):
                kept += 1
                continue
            os.makedirs(dest, exist_ok=True)
            shutil.copyfile(os.path.join(root, f), d)
            added += 1
    print('WHE-common: %d files added, %d already there' % (added, kept))


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    fetched, converted, modpaks = sys.argv[1:4]
    common = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, '..', '..', '..', 'WHE-common', 'patch-A.MPQ')
    names, by_path = {}, {}
    for line in open(os.path.join(fetched, 'listfile.csv'), encoding='utf-8'):
        fdid, _, path = line.strip().partition(';')
        names[int(fdid)] = path
        by_path[path] = int(fdid)
    install(converted, common)
    pack = next(d for d in os.listdir(modpaks) if d.startswith('F-128_'))
    base = os.path.join(modpaks, pack)

    variables, models, displays, info, templates = [], [], [], [], []
    for key, (entry, name, family, stock, retail) in PETS.items():
        donor, donor_display = FAMILY[family]
        display = stock if stock else '@Pet%sDisplay' % key
        if retail:
            model_id, texture = retail
            path = model_id if isinstance(model_id, str) else names[model_id]
            client = 'Creature\\\\' + path.split('/', 1)[1].replace('/', '\\\\')
            tex = names[texture].rsplit('/', 1)[1][:-4] if texture else ''
            variables += [('SET @Pet%sModel' % key).ljust(40) + '= @NextModelID := @NextModelID +1;',
                          ('SET @Pet%sDisplay' % key).ljust(40) + '= @NextDisplayID := @NextDisplayID +1;']
            models.append("SELECT @Pet%sModel, `flags`, '%s', %s FROM `creaturemodeldata` WHERE `id` = "
                          "(SELECT `model_id` FROM `creaturedisplayinfo` WHERE `id` = %d)" % (key, client, CMD_COLUMNS, donor_display))
            displays.append("(@Pet%sDisplay, @Pet%sModel, 0, 0, '1', 255, '%s', '', '', '', 1, 0, 0, 0, 0, 0)" % (key, key, tex))
            info.append("SELECT @Pet%sDisplay, `BoundingRadius`, `CombatReach`, `Gender`, 0 FROM `creature_model_info` WHERE `DisplayID` = %d" % (key, donor_display))
        templates.append((entry, name, donor, display))

    write(os.path.join(base, 'variables.sql'), '-- Model and display slots of the retail pets (tools/races/retail_pets.py)\n' + '\n'.join(variables))
    model_ids = ', '.join('@Pet%sModel' % k for k, p in PETS.items() if p[4])
    display_ids = ', '.join('@Pet%sDisplay' % k for k, p in PETS.items() if p[4])
    write(os.path.join(base, 'dbc', '[F-128]_retail_pets.sql'), '\n'.join([
        "-- Retail's starting pets (tools/races/retail_pets.py; the models are in WHE-common). The model rows copy the size and",
        '-- sounds of a stock beast of the same family.', '',
        'DELETE FROM `creaturemodeldata` WHERE `id` IN (%s);' % model_ids,
        'INSERT INTO `creaturemodeldata` (`id`, `flags`, `model_path`, %s)' % CMD_COLUMNS,
        '\nUNION ALL\n'.join(models) + ';', '',
        'DELETE FROM `creaturedisplayinfo` WHERE `id` IN (%s);' % display_ids,
        'INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, `creature_model_scale`, '
        '`creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, `texture_variation_3`, `portrait_texture_name`, '
        '`blood_level`, `blood_id`, `npc_sound_id`, `praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`) VALUES',
        ',\n'.join(displays) + ';']))

    entries = ', '.join(str(p[0]) for p in PETS.values())
    sql = ['/* The starting pets: tameable creatures copied from a stock beast of the same family (tools/races/retail_pets.py) */',
           'DELETE FROM `creature_template_model` WHERE `CreatureID` IN (%s);' % entries,
           'DELETE FROM `creature_template` WHERE `entry` IN (%s);' % entries, '',
           'DROP TEMPORARY TABLE IF EXISTS `pet_copy`;', 'CREATE TEMPORARY TABLE `pet_copy` LIKE `creature_template`;']
    for entry, name, donor, _ in templates:
        sql += ['INSERT INTO `pet_copy` SELECT * FROM `creature_template` WHERE `entry` = %d;' % donor,
                "UPDATE `pet_copy` SET `entry` = %d, `name` = '%s', `subname` = NULL, `minlevel` = 1, `maxlevel` = 1, `faction` = 35, "
                "`npcflag` = 0, `lootid` = 0, `pickpocketloot` = 0, `skinloot` = 0, `mingold` = 0, `maxgold` = 0, `AIName` = '', `ScriptName` = '';" % (entry, name),
                'INSERT INTO `creature_template` SELECT * FROM `pet_copy`;', 'DELETE FROM `pet_copy`;']
    sql += ['DROP TEMPORARY TABLE `pet_copy`;', '',
            'INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES',
            ',\n'.join('(%d, 0, %s, 1, 1, 0)' % (t[0], t[3]) for t in templates) + ';', '',
            'DELETE FROM `creature_model_info` WHERE `DisplayID` IN (%s);' % display_ids,
            'INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`)',
            '\nUNION ALL\n'.join(info) + ';']
    write(os.path.join(base, 'sql', 'db-world', 'base', '[BASE,F-128]_pet_templates.sql'), '\n'.join(sql))

    lines = ['/* The stock races\' starting pets (tools/races/retail_pets.py). Entries are in [BASE,F-128]_pet_templates.sql */',
             'DELETE FROM `player_starting_pet` WHERE `race` IN (%s);' % ', '.join('@' + r for r, _ in STOCK),
             'INSERT INTO `player_starting_pet` (`race`, `creature_entry`) VALUES']
    rows = [row(r, k) for r, k in STOCK]
    lines += [v + (',' if i < len(rows) - 1 else ';') + ' -- ' + n for i, (v, n) in enumerate(rows)]
    write(os.path.join(base, 'sql', 'db-world', 'base', '[BASE,F-128]_player_starting_pet.sql'), '\n'.join(lines))

    for fnum, race, key in RACES:
        folder = next((d for d in os.listdir(modpaks) if d.startswith(fnum + '_')), None)
        if folder:
            v, n = row(race, key)
            write(os.path.join(modpaks, folder, 'sql', 'db-world', 'base', '[BASE,%s]_player_starting_pet.sql' % fnum),
                  "/* The starting pet of this race's hunters, in F-128 (tools/races/retail_pets.py) */\n"
                  'DELETE FROM `player_starting_pet` WHERE `race` = @%s;\n'
                  'INSERT INTO `player_starting_pet` (`race`, `creature_entry`) VALUES\n%s; -- %s' % (race, v, n))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Give the post-Cataclysm shaman races retail's racial totems.

Retail picks a totem's model per spell and race (TrinityCore's spell_totem_model, TDB 1210.26091); 3.3.5 has one model
per element and race (player_totem_model). Each race gets the models retail gives its Liquid Magma (fire), Earthbind
(earth), Healing Stream (water) and Wind Rush (air) totems, the same element models the stock races' totems map to.
Pandaren's earth totem uses the Pandaren set's own pandarentotem_earth.m2 (retail's row points at an unrelated model).

The models come from retail (tools/models/retail_fetch.py, converted with Kalibro's wotlkconv): this tool copies the
converted files to WHE-common under their retail paths, writes dbc/[F-xxx]_retail_totems.sql into each race's modpak
(model rows copied from the Orc totems' with the new paths, displays copied from the Orc totem displays) and its
player_totem_model file, and adds the model and display slots to config.sql in a marked block.

usage: retail_totems.py <retail_fetch output (for listfile.csv)> <converted folder> [WHE-common patch-A.MPQ]"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MODPAKS = os.path.join(HERE, '..', '..', 'modpaks')
ELEMENTS = (('Fire', 1, 'OrcFireTotem', 3240), ('Earth', 2, 'OrcEarthTotem', 3239), ('Water', 3, 'OrcWaterTotem', 3241),
            ('Air', 4, 'OrcAirTotem', 3238))
# variable part: (race variables, modpaks, fire, earth, water, air model file ids)
RACES = {
    'Pandaren': (('AlliancePandaren', 'HordePandaren'), ('F-020', 'F-021'), (608637, 608634, 608640, 608631)),
    'HighmountainTauren': (('HighmountainTauren',), ('F-028',), (1778744, 1778746, 1778745, 1778743)),
    'ZandalariTroll': (('ZandalariTroll',), ('F-017',), (1940567, 1940574, 1940575, 1940573)),
    'KulTiran': (('KulTiran',), ('F-025',), (2574512, 2574513, 2574514, 2574515)),
    'DarkIronDwarf': (('DarkIronDwarf',), ('F-016',), (1958825, 1958821, 1970976, 1958823)),
    'Vulpera': (('Vulpera',), ('F-019',), (3177063, 3177065, 3177064, 3177066)),
    'MagharOrc': (('MagharOrc',), ('F-007',), (1967911, 1967913, 1967914, 1967909)),
    # not in TDB yet: retail's Haranir totem models by name (world/expansion10/doodads/wildelves/haranir_totem_*.m2)
    'Haranir': (('AllianceHaranir', 'HordeHaranir'), ('F-098', 'F-099'), (7426818, 7426819, 7426817, 7426816)),
}
BEGIN, END = '-- >>> Retail totems (tools/races/retail_totems.py) >>>', '-- <<< Retail totems <<<'
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


def modpak(fnum):
    return next(os.path.join(MODPAKS, d) for d in os.listdir(MODPAKS) if d.startswith(fnum + '_'))


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    fetched, converted = sys.argv[1:3]
    common = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, '..', '..', '..', 'WHE-common', 'patch-A.MPQ')
    names = {}
    for line in open(os.path.join(fetched, 'listfile.csv'), encoding='utf-8'):
        fdid, _, path = line.strip().partition(';')
        names[int(fdid)] = path
    # the converted tree has the retail paths: copy it whole (textures and effects come along)
    shutil.copytree(converted, common, dirs_exist_ok=True)
    config = []
    for key, (race_vars, fnums, fdids) in RACES.items():
        models, displays = [], []
        for (element, _, orc, orc_model), fdid in zip(ELEMENTS, fdids):
            path = names[fdid].replace('/', '\\\\')
            models.append("SELECT @%s%sTotemModel, `flags`, '%s', %s FROM `creaturemodeldata` WHERE `id` = %d /* Orc %s totem */"
                          % (key, element, path, CMD_COLUMNS, orc_model, element.lower()))
            displays.append("SELECT @%s%sTotem, @%s%sTotemModel, `sound_id`, 0, `creature_model_scale`, `creature_model_alpha`, "
                            "'', '', '', '', `blood_level`, `blood_id`, `npc_sound_id`, `praticle_color_id`, 0, "
                            "`obj_effect_package_id` FROM `creaturedisplayinfo` WHERE `id` = @%s" % (key, element, key, element, orc))
            config += [('SET @%s%sTotemModel' % (key, element)).ljust(64) + '=   @NextModelID := @NextModelID +1;',
                       ('SET @%s%sTotem' % (key, element)).ljust(64) + '=   @NextDisplayID := @NextDisplayID +1;']
        ids = lambda suffix: ', '.join('@%s%s%s' % (key, e[0], suffix) for e in ELEMENTS)
        dbc = ['-- Retail\'s %s totems (tools/races/retail_totems.py; the models are in WHE-common under their retail paths).' % key,
               '-- Model rows and displays are copies of the Orc totems\' with the new models.', '',
               'DELETE FROM `creaturemodeldata` WHERE `id` IN (%s);' % ids('TotemModel'),
               'INSERT INTO `creaturemodeldata` (`id`, `flags`, `model_path`, %s)' % CMD_COLUMNS,
               '\nUNION ALL\n'.join(models) + ';', '',
               'DELETE FROM `creaturedisplayinfo` WHERE `id` IN (%s);' % ids('Totem'),
               'INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, '
               '`creature_model_scale`, `creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, '
               '`texture_variation_3`, `portrait_texture_name`, `blood_level`, `blood_id`, `npc_sound_id`, '
               '`praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`)',
               '\nUNION ALL\n'.join(displays) + ';']
        for fnum, race in zip(fnums, race_vars):
            folder = modpak(fnum)
            write(os.path.join(folder, 'dbc', '[%s]_retail_totems.sql' % fnum), '\n'.join(dbc))
            rows = ',\n'.join('(%d, @%s, @%s%sTotem)' % (slot, race, key, element) for element, slot, _, _ in ELEMENTS)
            write(os.path.join(folder, 'sql', 'db-world', 'base', '[BASE,%s]_player_totem_model.sql' % fnum),
                  '-- Retail\'s %s totems (dbc/[%s]_retail_totems.sql)\nDELETE FROM `player_totem_model` WHERE `RaceID` = @%s;\n'
                  'INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES\n%s;' % (key, fnum, race, rows))
    path = os.path.join(MODPAKS, 'config.sql')
    text = open(path, encoding='utf-8').read()
    body = BEGIN + '\n' + '\n'.join(config) + '\n' + END + '\n'
    pattern = re.compile(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n', re.S)
    if pattern.search(text):
        text = pattern.sub(lambda m: body, text)
    else:   # after the Haranir druid forms' slots (the last display slots)
        m = re.search(r'^-- <<< Haranir druid forms <<<\n', text, re.M)
        text = text[:m.end()] + body + text[m.end():]
    write(path, text)
    print('%d races, %d models' % (len(RACES), 4 * len(RACES)))


if __name__ == '__main__':
    main()

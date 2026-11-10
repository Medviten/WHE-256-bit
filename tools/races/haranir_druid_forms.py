#!/usr/bin/env python3
"""Give the Haranir (F-098, F-099) retail's Haranir druid forms: cat, bear, travel, aquatic, moonkin and tree.

The models come from retail (tools/models/retail_fetch.py, converted with Kalibro's wotlkconv, then
m2_unshare_tracks.py), see FORMS for the file ids. Each form keeps retail's creature texture slots (types 11 and 12),
which 3.3.5 fills from the display's texture variations, so every retail colour is one CreatureDisplayInfo row. The
forms follow hair colour, as the race template says (shapeshift_skin_color 0): hair colour c gets the form's colour
c mod (its number of colours); colours without a row (255) get the first. Retail has no Haranir flight forms, so those
stay the Home race's.

This tool:
- copies the converted files from CONVERTED/creature/<form folder> to WHE-common's Creature/<form folder>
- writes dbc/[F-098]_haranir_druid_forms.sql (and the F-099 copy): creaturemodeldata rows (the stock Night Elf form
  models' size and sounds with the new paths) and the displays
- rewrites both modpaks' player_shapeshift_model file: these forms, then the Home race's for the rest
- adds the model and display slots to config.sql, in a marked block after the CoA 1.9.9 races' slots

usage: haranir_druid_forms.py <retail_fetch output (for listfile.csv)> <converted folder> [WHE-common patch-A.MPQ]"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MODPAKS = os.path.join(HERE, '..', '..', 'modpaks')
TARGETS = (('F-098', 'AllianceHaranir'), ('F-099', 'HordeHaranir'))
# form: (variable part, model file id, shapeshift form variables, stock Night Elf display whose model data is copied,
#        texture variations (type 11, type 12) in retail's display order; one empty pair: the model's own textures)
FORMS = {
    'cat': ('Cat', 5927360, ['@CatForm'], 892,
            [(6015473, 6379987), (6015472, 6379986), (6015471, 6379985), (6015474, 6379988), (6015475, 6379989)]),
    'bear': ('Bear', 6218499, ['@BearForm', '@DireBearForm'], 2281,
             [(6218503, 6379974), (6218501, 6379972), (6218505, 6379976), (6218504, 6379975), (6218502, 6379973)]),
    'travel': ('Travel', 6046789, ['@TravelForm'], 632,
               [(6116664, 6402048), (6116665, 6402049), (6116666, 6402050), (6116667, 6402051), (6116668, 6402052)]),
    'aquatic': ('Aquatic', 6120989, ['@AquaticForm'], 2428,
                [(6175408, 6379990), (6175409, 6379991), (6175410, 6379992), (6175411, 6379993), (6175413, 6379994)]),
    'moonkin': ('Moonkin', 6181811, ['@MoonkinForm'], 15374,
                [(6217568, 6379980), (6217571, 6379981), (6217572, 6379982), (6217573, 6379983), (6217575, 6379984)]),
    'tree': ('Tree', 6020447, ['@TreeForm'], 864, [(0, 0)]),
}
HAIR_COLOURS = 30   # F-098/F-099's hair colours (0-29)
BEGIN, END = '-- >>> Haranir druid forms (tools/races/haranir_druid_forms.py) >>>', '-- <<< Haranir druid forms <<<'
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


def colour_names(var, n):
    return ['@Druid%sHaranir%dDisplay' % (var, i) for i in range(n)]


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    fetched, converted = sys.argv[1:3]
    common = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, '..', '..', '..', 'WHE-common', 'patch-A.MPQ')
    names = {}
    for line in open(os.path.join(fetched, 'listfile.csv'), encoding='utf-8'):
        fdid, _, path = line.strip().partition(';')
        names[int(fdid)] = path
    models, displays, shapeshift, config = [], [], [], []
    for form, (var, model, shapes, stock, colours) in FORMS.items():
        path = names[model]                          # creature/druidcatharanir/druidcatharanir.m2
        folder = path.rsplit('/', 1)[0]
        src = os.path.join(converted, *folder.split('/'))
        dst = os.path.join(common, 'Creature', folder.split('/', 1)[1])
        shutil.copytree(src, dst, dirs_exist_ok=True)
        client = 'Creature\\\\' + path.split('/', 1)[1].replace('/', '\\\\')
        models.append("SELECT @Druid%sHaranirModel, `flags`, '%s', %s FROM `creaturemodeldata` WHERE `id` = "
                      "(SELECT `model_id` FROM `creaturedisplayinfo` WHERE `id` = %d) /* the Night Elf %s form's model */"
                      % (var, client, CMD_COLUMNS, stock, form))
        config.append(('SET @Druid%sHaranirModel' % var).ljust(64) + '=   @NextModelID := @NextModelID +1;')
        for i, (t1, t2) in enumerate(colours):
            tex = ["'%s'" % (names[t].rsplit('/', 1)[1][:-4] if t else '') for t in (t1, t2)]
            displays.append("(@Druid%sHaranir%dDisplay, @Druid%sHaranirModel, 0, 0, '1', 255, %s, %s, '', '', 3, 0, 0, 0, 0, 0)"
                            % (var, i, var, tex[0], tex[1]))
            config.append(('SET @Druid%sHaranir%dDisplay' % (var, i)).ljust(64) + '=   @NextDisplayID := @NextDisplayID +1;')
        for shape in shapes:
            for c in range(HAIR_COLOURS):
                shapeshift.append((shape, c, '@Druid%sHaranir%dDisplay' % (var, c % len(colours))))
            shapeshift.append((shape, 255, '@Druid%sHaranir0Display' % var))
    display_ids = [d.split(',', 1)[0][1:] for d in displays]
    model_ids = ['@Druid%sHaranirModel' % f[0] for f in FORMS.values()]
    dbc = ['-- Retail\'s Haranir druid forms (tools/races/haranir_druid_forms.py; the models are in WHE-common). The model rows',
           '-- copy the Night Elf forms\' size and sounds; each display is one of retail\'s colours (texture types 11 and 12).',
           '-- The same rows are in F-098 and F-099, so either one works alone.', '',
           'DELETE FROM `creaturemodeldata` WHERE `id` IN (%s);' % ', '.join(model_ids),
           'INSERT INTO `creaturemodeldata` (`id`, `flags`, `model_path`, %s)' % CMD_COLUMNS,
           '\nUNION ALL\n'.join(models) + ';', '',
           'DELETE FROM `creaturedisplayinfo` WHERE `id` IN (%s);' % ', '.join(display_ids),
           'INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, '
           '`creature_model_scale`, `creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, '
           '`texture_variation_3`, `portrait_texture_name`, `blood_level`, `blood_id`, `npc_sound_id`, '
           '`praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`) VALUES',
           ',\n'.join(displays) + ';']
    for fnum, race in TARGETS:
        folder = next(os.path.join(MODPAKS, d) for d in os.listdir(MODPAKS) if d.startswith(fnum + '_'))
        write(os.path.join(folder, 'dbc', '[%s]_haranir_druid_forms.sql' % fnum), '\n'.join(dbc))
        rows = ',\n'.join('(%s, @%s, %d, 2, %s)' % (shape, race, c, d) for shape, c, d in shapeshift)
        shapes = sorted({s for f in FORMS.values() for s in f[2]})
        write(os.path.join(folder, 'sql', 'db-world', 'base', '[BASE,%s]_player_shapeshift_model.sql' % fnum),
              '/* Retail\'s Haranir druid forms (dbc/[%s]_haranir_druid_forms.sql), following hair colour: colour c gets the\n'
              '   form\'s colour c mod its number of colours (255: the first). Flight forms copy the Home race\'s (F-011 or stock). */\n'
              'DELETE FROM `player_shapeshift_model` WHERE `RaceID` = @%s;\n'
              'INSERT INTO `player_shapeshift_model` (`ShapeshiftID`, `RaceID`, `CustomizationID`, `GenderID`, `ModelID`) VALUES\n'
              '%s;\n\n'
              'INSERT INTO `player_shapeshift_model` (`ShapeshiftID`, `RaceID`, `CustomizationID`, `GenderID`, `ModelID`)\n'
              'SELECT `ShapeshiftID`, @%s, 255, `GenderID`, MIN(`ModelID`)\nFROM `player_shapeshift_model`\n'
              'WHERE `RaceID` = @%sHome AND `ShapeshiftID` NOT IN (%s)\nGROUP BY `ShapeshiftID`, `GenderID`;'
              % (fnum, race, rows, race, race, ', '.join(shapes)))
    path = os.path.join(MODPAKS, 'config.sql')
    text = open(path, encoding='utf-8').read()
    body = BEGIN + '\n' + '\n'.join(config) + '\n' + END + '\n'
    pattern = re.compile(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n', re.S)
    if pattern.search(text):
        text = pattern.sub(lambda m: body, text)
    else:   # after the last race display slots: the CoA 1.9.9 block, else Horde Skyborne's
        m = re.search(r'^-- <<< CoA 1\.9\.9 races <<< displays\n', text, re.M) or \
            re.search(r'^SET @HordeSkyborneFemaleDisplay\s*=.*\n', text, re.M)
        text = text[:m.end()] + body + text[m.end():]
    write(path, text)
    print('%d models, %d displays, %d shapeshift rows per race' % (len(models), len(displays), len(shapeshift)))


if __name__ == '__main__':
    main()

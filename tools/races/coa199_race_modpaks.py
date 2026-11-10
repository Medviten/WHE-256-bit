#!/usr/bin/env python3
"""Generate the modpaks of the CoA 1.9.9 races (coa199_races.RACES, F-105..F-127) with new_race_modpaks.py's
templates (F-046 Horde, F-045 Alliance) and Home/Kin scheme, and give them their config.sql variables and manifest lines.

- catalog races: the skin colours of the release's appearance catalog, as coa_race_modpaks.py does for the 1.9 races
  (a gender the catalog has no skins for gets one empty skin row and keeps the model's own textures)
- classic races: the release's own CharSections, CharHairGeosets and CharacterFacialHairStyles rows (3.3.5 layout);
  a gender without rows (a one-body race) gets the other gender's
- model size from the release's CreatureModelData rows, display scale from its CreatureDisplayInfo rows (a race in
  STOCK_MODELS uses stock models and their rows instead)
- config.sql: race ids, masks, model/display/display-extra slots, racial skill lines, SkillRaceClassInfo, faction
  templates, reputation indices, achievements and criteria, in marked blocks after the last race's lines (rerunning
  replaces them). The factions themselves (@<Race>Faction/@<Race>Player) are 1401-1446, past the MoP ids WHE uses.
- manifest: one commented-out line per modpak

usage: coa199_race_modpaks.py <built DBFilesClient> <release server/dbc> <release client folder (catalogs)>
                              [modpaks dir] [output dir]
       (run tools/models/coa199_race_prep.py for the client files, coa_racials.py for the racials)"""
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'models'))
import coa199_races   # noqa: E402
import coa_race_modpaks   # noqa: E402
import new_race_modpaks as nrm   # noqa: E402
from coa199_race_prep import race_models   # noqa: E402

FACTION_BASE = 1401
# config.sql: race ids from the free ids in 67-128 (the second race-mask word)
RACE_IDS = [67, 68, 69, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 87, 88, 89, 90, 92, 93, 94]
SKILL_LINE_BASE, SRCI_BASE, FACTION_TEMPLATE_BASE, REP_INDEX_BASE, CRITERIA_BASE = 848, 1196, 2298, 166, 19446
ACHIEVEMENT_TAKEN = {1556, 1557, 1558, 1559, 1560, 1561, 1563, 1576}   # built Achievement.dbc ids from 1554 on
# catalog races whose always-shown 200xx geosets only the DLL textures (coa199_race_prep.py hides them)
BAKED_ARMOUR = {'Saberon', 'Drakonid', 'Drakkin'}
STOCK_MODELS = {}   # races on stock models (key: (male, female) stock CreatureModelData ids): their rows are copied
BEGIN, END = '-- >>> CoA 1.9.9 races (tools/races/coa199_race_modpaks.py) >>>', '-- <<< CoA 1.9.9 races <<<'
CREDITS = {
    'Sethrak': 'Project Ascension\'s model, in Ilusixn\'s CoA Custom release',
    'Saberon': 'Project Ascension\'s model, in Ilusixn\'s CoA Custom release',
    'Drakonid': 'Kalibros | Lord of Wen (STRHercules), Esteria races',
    'Drakkin': 'Kalibros | Lord of Wen (STRHercules) (male, Esteria races) and Dex (female)',
    'IllidariBloodElf': 'Furioz, Corruption and the Eunoia team',
    'IllidariNightElf': 'Furioz, Corruption and the Eunoia team',
    'Jinyu': 'Uncle Snowzo (SnowzoCraft)',
    'Grummle': 'the Grummle model from Ascension / retail assets, converted for WotLK',
    'TwoHeadedOgre': 'Stefan (stefanw1337): Two-Headed Ogre',
    'AllianceOrc': 'Project Ascension, in Ilusixn\'s CoA Custom release',
    'Harpy': 'Project Ascension, in Ilusixn\'s CoA Custom release',
}
V12 = 'the AllRaces v12 pack: Furioz, Corruption, Eunoia, Kalibros (STRHercules)'


def sql_path(path):
    return path.replace('\\', '\\\\')


def coa_display_scales(coa_dbc):
    rows, _, _ = nrm.load_dbc(os.path.join(coa_dbc, 'CreatureDisplayInfo.dbc'))
    return {struct.unpack_from('<I', r)[0]: struct.unpack_from('<f', r, 16)[0] for r in rows}


def coa_displays(coa_dbc, coa_id):
    rows, _, _ = nrm.load_dbc(os.path.join(coa_dbc, 'ChrRaces.dbc'))
    return next(struct.unpack_from('<6I', r)[4:6] for r in rows if struct.unpack_from('<I', r)[0] == coa_id)


def source_of(race, catalogs, coa_dbc):
    if not race.catalog:
        return ('coa', race.coa_id)
    looks = coa199_races.catalog(coa199_races.catalog_path(catalogs, race))
    skins = {}
    for g in (0, 1):
        look = coa199_races.look_for(looks, coa199_races.ONE_BODY.get(race.key, g))   # one body: its gender's look
        skins[g] = [(s[0], s[1] if len(s) > 1 else '') for s in look.skins] or [('', '')]
    return ('skins', skins)


def as_nrm(race, catalogs, coa_dbc):
    male, female = race_models(coa_dbc, race)
    if race.key in STOCK_MODELS:
        model = ('stock',) + STOCK_MODELS[race.key]
    else:
        model = ('converted', sql_path(coa199_races.target(male)), sql_path(coa199_races.target(female)))   # renamed: RENAMED
    return (race.key, race.name, race.plural, race.fnum, race.slug, race.side, race.home, race.kin, False, model,
            source_of(race, catalogs, coa_dbc), race.prefix, race.fname, race.fdesc, race.info)


def one_body_sections(customization):
    """customization() for 'coa' with a missing gender filled from the other (one model for both genders)."""
    def wrapped(source):
        sections, hair, facial = customization(source)
        if source[0] == 'coa':
            def fill_gender(rows):
                for missing, have in ((0, 1), (1, 0)):
                    if not any(r[0] == missing for r in rows) and any(r[0] == have for r in rows):
                        return sorted(rows + [(missing,) + tuple(r[1:]) for r in rows if r[0] == have]), missing, have
                return rows, None, None
            sections, missing, have = fill_gender(sections)
            if missing is not None:
                for k in [k for k in nrm.PLAYER_FLAGS if k[0] == have]:
                    nrm.PLAYER_FLAGS[(missing,) + k[1:]] = nrm.PLAYER_FLAGS[k]
            hair, facial = fill_gender(hair)[0], fill_gender(facial)[0]
        return sections, hair, facial
    return wrapped


def write_readme(out, key, name, plural, fnum, slug, side, home, kin, male_only, model, source, prefix):
    race = coa199_races.by_key(key)
    one_body = model[0] == 'converted' and model[1] == model[2]
    if race.catalog:
        colours = '/'.join(str(len([s for s in ss if s[0]])) for ss in source[1].values())
        look = ['    - Customization: the %s skin colours of CoA\'s appearance catalog (`Esteria%s.bin`); its other '
                'options (EsteriaAppearance.dll) are fixed at their first choice' % (colours, race.catalog)]
    else:
        look = ['    - Customization: CoA\'s own CharSections, hair and facial hair rows for its race %d' % race.coa_id]
    lines = ['# mod-worgoblin-high-elf', '## ' + nrm.folder_name(fnum, slug), '', '### Features',
             '- Playable %s (%s), race ID set in config.sql%s' % (plural, side, ', one body for both genders' if one_body else ''),
             '    - %s model and textures from Ilusixn\'s CoA 1.9.9 release (CoA race %d), prepared by '
             '`tools/models/coa199_race_prep.py`' % ('Stock gnome' if key in STOCK_MODELS else 'CoA\'s', race.coa_id)] + look + [
             '    - Home: %s (classes, start position, start outfits, action bars, stats, totems, druid forms, race-restricted' % home,
             '      quests and items)', '    - Kin: %s (voice, emotes and names, copied at build time)' % kin,
             '    - Helmet prefix \'%s\'' % prefix,
             '    - Model size and display scale from CoA\'s CreatureModelData/CreatureDisplayInfo rows'
             if key not in STOCK_MODELS else '    - Model size from the stock gnome models',
             '- Generated by `tools/races/coa199_race_modpaks.py` (tentative, for testing)', '',
             '### Requirements', '- Client files from `tools/models/coa199_race_prep.py` (in WHE-common\'s `patch-A.MPQ`)']
    if race.catalog:
        lines.append('- Custom client with `creatureSkinRaces` containing the race ID: the skin texture is composited whole '
                     'and armour textures are not drawn on it')
    lines += ['- Interface: race button and the %s entries in `CharacterCreate.lua/.xml`, `GlueParent.lua` and '
              '`GlueStrings.lua`' % key.upper(), '',
              '### Credits',
              '- Model and textures: %s. See `CREDITS.md` in Ilusixn\'s CoA 1.9.9 release, which must ship with them'
              % CREDITS.get(key, V12), '',
              '### Known Issues', '- Tentative: not tested in game yet', '- No racial abilities yet', '- No racial mount',
              '- Placeholder race icon', '- Barber shop styles have generic names',
              '- Character creation camera is not tuned for the model\'s size']
    if race.catalog:
        lines.append('- CoA\'s extra appearance options (EsteriaAppearance.dll) are not available')
        if key in BAKED_ARMOUR:
            lines.append('- The DLL\'s baked armour (geosets 200xx, drawn with its texture type 14) is hidden')
        if any(not s[0] for ss in source[1].values() for s in ss):
            lines.append('- One gender has no skin colours in the catalog: it keeps the model\'s own textures')
    if one_body and key in coa199_races.ONE_BODY:
        lines.append('- One body: CoA\'s %s model for both genders; the other model\'s textures are in neither the '
                     'release nor retail' % ('female', 'male')[1 - coa199_races.ONE_BODY[key]])
    elif one_body:
        lines.append('- One body: both genders use it, with the Kin race\'s voices')
    nrm.write(os.path.join(out, 'readme.md'), '\n'.join(lines))


def patch_files(out, race, model_rows, scales, coa_dbc):
    """CoA model size, display scale and faction ids; CoA wording in the generated comments."""
    tag = '[BASE,F-%03d]' % race.fnum
    key = race.key
    male, female = race_models(coa_dbc, race)
    if race.key not in STOCK_MODELS:
        path = os.path.join(out, 'dbc', tag + '_creaturemodeldata.sql')
        text = open(path, encoding='utf-8').read()
        updates = []
        for g, model in (('Male', male), ('Female', female)):
            row = model_rows[model.lower()]
            sets = ', '.join('`%s` = %s' % (c, ('%.6f' % row[c]).rstrip('0').rstrip('.') if c != 'size_class' else row[c])
                             for c in ['size_class'] + coa_race_modpaks.CMD_FLOATS)
            updates.append('UPDATE `creaturemodeldata` SET %s WHERE `id` = @%s%sModel;' % (sets, key, g))
        text = text.replace(', with the player model flags (0x804)', ', with the player model flags (0x804); size, '
                            'collision and bounds\n-- from CoA\'s rows for these models (below)')
        nrm.write(path, text.rstrip() + '\n\n-- Model scale, collision and bounds of CoA\'s rows\n' + '\n'.join(updates))
        displays = coa_displays(coa_dbc, race.coa_id)
        path = os.path.join(out, 'dbc', tag + '_creaturedisplayinfo.sql')
        lines = open(path, encoding='utf-8').read().split('\n')
        for i, line in enumerate(lines):
            for g, d in (('Male', displays[0]), ('Female', displays[1])):
                if line.startswith('(@%s%sDisplay,' % (key, g)):
                    lines[i] = line.replace("'1.0000000000000000', 255", "'%.10f000000', 255" % scales[d])
        text = '\n'.join(lines).replace('-- New entries', '-- New entries (display scale as CoA\'s displays %d/%d)' % displays)
        nrm.write(path, text)
    if race.catalog:
        for name in ('charsections', 'charhairgeosets', 'characterfacialhairstyles'):
            path = os.path.join(out, 'dbc', '%s_%s.sql' % (tag, name))
            text = open(path, encoding='utf-8').read()
            nrm.write(path, text.replace('the skin textures shipped with the model (WallCraft has no rows for it)',
                                         'the skin colours (option 0) of CoA\'s appearance catalog Esteria%s.bin' % race.catalog))
    path = os.path.join(out, 'variables.sql')
    text = open(path, encoding='utf-8').read()
    text = text.replace('-- WallCraft model, converted to the 3.3.5 format', '-- CoA 1.9.9 model (prepared by coa199_race_prep.py)')
    faction = FACTION_BASE + 2 * (race.fnum - 105)
    text = re.sub(r'SET @%sFaction = \d+; -- vacant slot' % key, 'SET @%sFaction = %d; -- vacant slot' % (key, faction), text)
    text = re.sub(r'SET @%sPlayer = \d+; -- vacant slot' % key, 'SET @%sPlayer = %d; -- vacant slot' % (key, faction + 1), text)
    nrm.write(path, text)


def block(text, marker, body):
    """text with the marked block for marker replaced, or inserted after the line matching marker's anchor."""
    begin, end = '%s %s' % (BEGIN, marker), '%s %s' % (END, marker)
    pattern = re.compile(re.escape(begin) + r'\n.*?' + re.escape(end) + r'\n', re.S)
    marked = begin + '\n' + body.rstrip('\n') + '\n' + end + '\n'
    if pattern.search(text):
        return pattern.sub(lambda m: marked, text)
    return None


def config_lines(races):
    """{anchor variable: lines inserted after its line} for config.sql."""
    pad = lambda s: s.ljust(64)
    achievements, a = [], 1554
    while len(achievements) < len(races):
        if a not in ACHIEVEMENT_TAKEN:
            achievements.append(a)
        a += 1
    out = {k: [] for k in ('ids', 'masks', 'extras', 'racials', 'srci', 'models', 'displays', 'templates', 'rep',
                           'achievements', 'criteria')}
    for i, r in enumerate(races):
        k, f = r.key, 'F-%03d' % r.fnum
        out['ids'].append(pad('SET @%s' % k) + '= %4d; -- CoA 1.9.9 race (%s)' % (RACE_IDS[i], f))
        out['masks'] += [pad('SET @%sMask' % k) + '=   0; -- ' + f, pad('SET @%sMask_2' % k) + '=   0; -- races 65-128',
                         pad('SET @%sHelmetMask' % k) + '=   0;']
        out['extras'] += [pad('SET @%s%sDisplayExtra' % (k, g)) + '=   @NextDisplayExtraID := @NextDisplayExtraID +1;'
                          for g in ('Male', 'Female')]
        out['racials'].append(pad('SET @%sRacials' % k) + '=   %d;' % (SKILL_LINE_BASE + i))
        out['srci'].append(pad('SET @%sRacialSkillRaceClass' % k) + '=   %d;' % (SRCI_BASE + i))
        out['models'] += [pad('SET @%s%sModel' % (k, g)) + '=   @NextModelID := @NextModelID +1;' for g in ('Male', 'Female')]
        out['displays'] += [pad('SET @%s%sDisplay' % (k, g)) + '=   @NextDisplayID := @NextDisplayID +1;' for g in ('Male', 'Female')]
        out['templates'].append(pad('SET @%sFactionTemplate' % k) + '=   %d; -- References @%sPlayer' % (FACTION_TEMPLATE_BASE + i, k))
        out['rep'].append(pad('SET @%sFactionRepIndex' % k) + '=   %d;' % (REP_INDEX_BASE + i))
        out['achievements'].append(pad('SET @%sAchievement' % k) + '=   %d;' % achievements[i])
        enemy = 'Achievement 246: Know Thy Enemy' if r.side == 'Alliance' else 'Achievement 1005: Know Thy Enemy'
        for n, what in enumerate((enemy, 'Achievement 2422: Shake Your Bunny-Maker', 'Achievement 291: Check Your Head',
                                  '@%sAchievement: Realm First! Level 80 %s' % (k, r.name))):
            out['criteria'].append(pad('SET @%sCriteria%d' % (k, n + 1)) + '=   %d; -- %s' % (CRITERIA_BASE + 4 * i + n, what))
    return out


# config.sql: each block goes after the line that sets this variable (the last race's before this tool)
ANCHORS = {'ids': '@HordeSkyborne','masks': '@HordeSkyborneHelmetMask', 'extras': '@HordeSkyborneFemaleDisplayExtra',
           'racials': '@HordeSkyborneRacials', 'srci': '@HordeSkyborneRacialSkillRaceClass', 'models': '@HordeSkyborneFemaleModel',
           'displays': '@HordeSkyborneFemaleDisplay', 'templates': '@HordeSkyborneFactionTemplate',
           'rep': '@HordeSkyborneFactionRepIndex', 'achievements': '@HordeSkyborneAchievement',
           'criteria': '@HordeSkyborneCriteria4'}


def write_config(modpaks, races):
    path = os.path.join(modpaks, 'config.sql')
    text = open(path, encoding='utf-8').read()
    for name, lines in config_lines(races).items():
        new = block(text, name, '\n'.join(lines))
        if new is None:
            m = re.search(r'^SET %s\s*=.*\n' % re.escape(ANCHORS[name]), text, re.M)
            if not m:
                raise SystemExit('config.sql: no line for %s' % ANCHORS[name])
            body = '%s %s\n%s\n%s %s\n' % (BEGIN, name, '\n'.join(lines), END, name)
            new = text[:m.end()] + body + text[m.end():]
        text = new
    nrm.write(path, text)


def write_manifest(races):
    path = os.path.join(HERE, '..', 'scripts', 'build-dbc.manifest')
    text = open(path, encoding='utf-8').read()
    lines = ['#%s # Off by default (CoA 1.9.9 race; tentative, untested; needs client assets in patch-A)'
             % nrm.folder_name(r.fnum, r.slug) for r in races]
    text = re.sub(r'#F-1(0[5-9]|[1-3]\d)_[^\n]*\n', '', text)
    anchor = re.search(r'^# END EXTRA RACES #', text, re.M)
    text = text[:anchor.start()] + '\n'.join(lines) + '\n' + text[anchor.start():]
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:   # the manifest has no final newline
        fh.write(text)


def main():
    args = sys.argv[1:]
    if len(args) < 3:
        sys.exit(__doc__)
    built, coa_dbc, catalogs = args[:3]
    nrm.BUILT, nrm.DONOR = built, coa_dbc
    nrm.MODPAKS = args[3] if len(args) > 3 else os.path.join(HERE, '..', '..', 'modpaks')
    nrm.OUTPUT = args[4] if len(args) > 4 else nrm.MODPAKS
    races = coa199_races.RACES
    nrm.RACES = [as_nrm(r, catalogs, coa_dbc) for r in races]
    nrm.write_readme = write_readme
    nrm.customization = one_body_sections(nrm.customization)
    nrm.main()
    model_rows = coa_race_modpaks.coa_model_rows(coa_dbc)
    scales = coa_display_scales(coa_dbc)
    for race in races:
        patch_files(os.path.join(nrm.OUTPUT, nrm.folder_name(race.fnum, race.slug)), race, model_rows, scales, coa_dbc)
    write_config(nrm.MODPAKS, races)
    write_manifest(races)


if __name__ == '__main__':
    main()

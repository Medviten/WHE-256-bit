#!/usr/bin/env python3
"""Give the races added after Cataclysm their own voices from retail (and Skyborne theirs from the Forever build).

For each race and sex, from the pinned build's tables (wago.tools DB2 CSVs):
- EmotesTextSound (ClassID 0, emotes the 3.3.5 EmotesText has) -> `emotestextsound`
- VocalUISounds (error lines; NormalSoundID_0 male, _1 female; enums the 3.3.5 client has) -> `vocaluisounds`
- the race's player model's CreatureSoundData (ChrRaceXChrModel -> ChrModel.DisplayID -> CreatureDisplayInfo.SoundID or
  CreatureModelData.SoundID): exertion, injury, death, stun, aggro, jump... -> a new `creaturesounddata` row per race and
  sex (the model's current row with those columns replaced), which the race's models are pointed at. Footsteps stay.
- every SoundKit these use -> a `soundentries` row with the kit's id (kits the stock client has are used as they are),
  its files (at most 10, those in the kit's main folder) downloaded from wago.tools by FileDataID into WHE-common under
  their retail paths (sound\\character\\pc<race><sex>\\...); a file the stock client has under the same name (old
  emotes reused by retail) is used from there instead.
Whatever retail lacks (an emote, an error line) keeps the Kin race's rows, as before.

usage: retail_voices.py download [--data DIR]          the tables and listfile (when missing), then a paced, resumable
                                                       download of the sound files the races use
       retail_voices.py write <modpaks dir> [--data DIR] [--common PATH] [--stock DIR]
--data holds db2/*.csv (db2/forever_*.csv for Forever), community-listfile.csv, files/ and forever-files/
(default D:\\wow-scratch\\retail-vo). Rewrites its files, so it can be rerun."""
import argparse, collections, csv, glob, os, re, shutil, struct, sys, time, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import new_race_modpaks as nrm   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BS = '\\'
SOURCES = {'retail': ('', '12.1.5.70448', 'files'), 'forever': ('forever_', '1.60.1.70124', 'forever-files')}
# source, retail race id, WHE race variable, modpak number, races sharing its voice (A/H pairs)
RACES = [
    ('retail', 25, 'AlliancePandaren', 20, (26,)), ('retail', 26, 'HordePandaren', 21, (25,)),
    ('retail', 27, 'Nightborne', 34, ()), ('retail', 28, 'HighmountainTauren', 28, ()),
    ('retail', 29, 'VoidElf', 35, ()), ('retail', 30, 'LightforgedDraenei', 33, ()),
    ('retail', 31, 'ZandalariTroll', 17, ()), ('retail', 32, 'KulTiran', 25, ()),
    ('retail', 34, 'DarkIronDwarf', 16, ()), ('retail', 35, 'Vulpera', 19, ()),
    ('retail', 36, 'MagharOrc', 7, ()), ('retail', 37, 'Mechagnome', 40, ()),
    ('retail', 52, 'AllianceDracthyr', 73, (70,)), ('retail', 70, 'HordeDracthyr', 74, (52,)),
    ('retail', 85, 'AllianceEarthen', 38, (84,)), ('retail', 84, 'HordeEarthen', 39, (85,)),
    ('retail', 86, 'AllianceHaranir', 98, (91,)), ('retail', 91, 'HordeHaranir', 99, (86,)),
    ('forever', 95, 'AllianceSkyborne', 103, (96,)), ('forever', 96, 'HordeSkyborne', 104, (95,)),
]
# Files earlier versions of these modpaks had for the same tables (copies of a stock race's sounds)
OLD_FILES = {16: ['[F-016]_emotestextsound.sql'], 25: ['[BASE,F-027]_emotestextsound.sql']}
# Cataclysm modpaks whose soundentries ids are Cata's, i.e. the same kits as retail's
SAME_KITS = ('F-013', 'F-024', 'F-027')
# retail CreatureSoundData column -> 3.3.5 column (the vocal ones; footsteps and the rest stay the model's)
CSD = [('SoundExertionID', 'sound_exertion_id'), ('SoundExertionCriticalID', 'sound_exertion_critical_id'),
       ('SoundInjuryID', 'sound_injury_id'), ('SoundInjuryCriticalID', 'sound_injury_critical_id'),
       ('SoundInjuryCrushingBlowID', 'sound_injury_crushing_blow_id'), ('SoundDeathID', 'sound_death_id'),
       ('SoundStunID', 'sound_stun_id'), ('SoundStandID', 'sound_stand_id'), ('SoundAggroID', 'sound_aggro_id'),
       ('SoundAlertID', 'sound_alert_id'), ('SoundJumpStartID', 'sound_jump_start_id'), ('SoundJumpEndID', 'sound_jump_end_id')]
CSD_COLUMNS = ['id', 'sound_exertion_id', 'sound_exertion_critical_id', 'sound_injury_id', 'sound_injury_critical_id',
               'sound_injury_crushing_blow_id', 'sound_death_id', 'sound_stun_id', 'sound_stand_id', 'sound_footstep_id',
               'sound_aggro_id', 'sound_wing_flap_id', 'sound_wing_glide_id', 'sound_alert_id'] + \
              ['sound_fidget_id_%d' % i for i in range(1, 6)] + ['sound_custom_attack_id_%d' % i for i in range(1, 5)] + \
              ['npc_sound_id', 'loop_sound_id', 'creature_impact_type', 'sound_jump_start_id', 'sound_jump_end_id',
               'sound_pet_attack_id', 'sound_pet_order_id', 'sound_pet_dismiss_id', 'fidget_delay_seconds_min',
               'fidget_delay_seconds_max', 'birth_sound_id', 'spell_cast_directed_sound_id', 'submerge_sound_id',
               'submerged_sound_id', 'creature_sound_data_id_pet']
SOUND_TYPE = {'emote': 29, 'vui': 12, 'combat': 10}   # what the stock client uses for each
FIRST_SOUND_DATA = 3201   # stock CreatureSoundData ends at 3108, F-023 uses 3110
MAX_VOCAL_UI_ENUM = 67
CONFIG_BEGIN = '-- Retail voices (tools/races/retail_voices.py): CreatureSoundData rows of the races it gives retail voices'
CONFIG_END = '-- End of retail voices'


class Source:
    def __init__(self, data, name):
        self.name = name
        prefix, self.version, files = SOURCES[name]
        self.files = os.path.join(data, files)
        rows = lambda t: list(csv.DictReader(open(os.path.join(data, 'db2', prefix + t + '.csv'), encoding='utf-8')))
        self.emotes = rows('EmotesTextSound')
        self.vui = rows('VocalUISounds')
        self.kit = {int(r['ID']): r for r in rows('SoundKit')}
        self.entries = collections.defaultdict(list)
        for r in rows('SoundKitEntry'):
            self.entries[int(r['SoundKitID'])].append(int(r['FileDataID']))
        self.models = rows('ChrRaceXChrModel')
        self.chrmodel = {int(r['ID']): r for r in rows('ChrModel')}
        self.display = {int(r['ID']): r for r in rows('CreatureDisplayInfo')}
        self.modeldata = {int(r['ID']): r for r in rows('CreatureModelData')}
        self.sounddata = {int(r['ID']): r for r in rows('CreatureSoundData')}

    def voice(self, race, sex, stock_emotes):
        """(emote rows {emote: kit}, error rows {enum: kit}, combat {3.3.5 column: kit})"""
        emotes = {}
        for r in self.emotes:
            if int(r['RaceID']) == race and int(r['SexID']) == sex and int(r['ClassID']) == 0 and int(r['EmotesTextID']) in stock_emotes:
                emotes.setdefault(int(r['EmotesTextID']), int(r['SoundID']))
        errors = {}
        for r in self.vui:
            if int(r['RaceID']) == race and int(r['ClassID']) == 0 and int(r['VocalUIEnum']) <= MAX_VOCAL_UI_ENUM:
                kit = int(r['NormalSoundID_%d' % sex])
                if kit:
                    errors.setdefault(int(r['VocalUIEnum']), kit)
        combat = {}
        for m in self.models:
            if int(m['ChrRacesID']) == race and int(m['Sex']) == sex:
                display = self.display.get(int(self.chrmodel[int(m['ChrModelID'])]['DisplayID']))
                if display:
                    sid = int(display['SoundID']) or int(self.modeldata[int(display['ModelID'])]['SoundID'])
                    for retail, column in CSD:
                        kit = int(self.sounddata.get(sid, {}).get(retail, 0) or 0)
                        if kit:
                            combat[column] = kit
                break
        return emotes, errors, combat


def stock_dbc(stock, name):
    d = open(os.path.join(stock, name + '.dbc'), 'rb').read()
    n, f, size, ss = struct.unpack_from('<4I', d, 4)
    return [struct.unpack_from('<%dI' % f, d, 20 + i * size) for i in range(n)], d[20 + n * size:]


def listfile(data):
    names = {}
    path = os.path.join(data, 'community-listfile.csv')
    for line in open(path, encoding='utf-8', errors='replace'):
        fdid, _, name = line.strip().partition(';')
        if fdid.isdigit():
            names[int(fdid)] = name
    return names


def plan(data, stock):
    """source name -> race id -> sex -> voice, and the stock tables needed to filter them"""
    emotes_text = {r[0] for r in stock_dbc(stock, 'EmotesText')[0]}
    sources = {name: Source(data, name) for name in SOURCES}
    voices = {}
    for source, race, key, fnum, _ in RACES:
        voices[race] = [sources[source].voice(race, sex, emotes_text) for sex in (0, 1)]
    return sources, voices


def kits_of(voices, race):
    out = {}
    for emotes, errors, combat in voices[race]:
        out.update({k: 'emote' for k in emotes.values()})
        out.update({k: 'vui' for k in errors.values()})
        out.update({k: 'combat' for k in combat.values()})
    return out


TABLES = ('EmotesTextSound', 'VocalUISounds', 'SoundKit', 'SoundKitEntry', 'ChrRaceXChrModel', 'ChrModel', 'CreatureDisplayInfo',
          'CreatureModelData', 'CreatureSoundData')
LISTFILE = 'https://github.com/wowdev/wow-listfile/releases/latest/download/community-listfile.csv'


def fetch(url, target):
    if os.path.exists(target):
        return
    os.makedirs(os.path.dirname(target), exist_ok=True)
    req = urllib.request.Request(url, headers={'User-Agent': 'whe-voice-import'})
    open(target + '.part', 'wb').write(urllib.request.urlopen(req, timeout=600).read())
    os.replace(target + '.part', target)
    print('fetched', os.path.basename(target), flush=True)


def download(data, stock):
    for name, (prefix, version, _) in SOURCES.items():
        for table in TABLES:
            fetch('https://wago.tools/db2/%s/csv?build=%s' % (table, version), os.path.join(data, 'db2', prefix + table + '.csv'))
    fetch(LISTFILE, os.path.join(data, 'community-listfile.csv'))
    sources, voices = plan(data, stock)
    for source in sources.values():
        races = [r for s, r, *_ in RACES if s == source.name]
        stock_ids = {r[0] for r in stock_dbc(stock, 'SoundEntries')[0]}
        ids = sorted({f for race in races for kit in kits_of(voices, race) if kit not in stock_ids for f in source.entries[kit]})
        os.makedirs(source.files, exist_ok=True)
        bad = os.path.join(source.files, 'unavailable.txt')
        unavailable = set(open(bad).read().split()) if os.path.exists(bad) else set()
        got = 0
        for i, f in enumerate(ids):
            target = os.path.join(source.files, '%d.bin' % f)
            if os.path.exists(target) or str(f) in unavailable:
                continue
            for attempt in range(6):
                try:
                    req = urllib.request.Request('https://wago.tools/api/casc/%d?download&version=%s' % (f, source.version),
                                                 headers={'User-Agent': 'whe-voice-import'})
                    body = urllib.request.urlopen(req, timeout=60).read()
                    if body:
                        open(target + '.part', 'wb').write(body)
                        os.replace(target + '.part', target)
                        got += 1
                        break
                except urllib.error.HTTPError as e:
                    if e.code == 400:   # "File unavailable" (encrypted or missing at that build)
                        unavailable.add(str(f))
                        open(bad, 'a').write('%d\n' % f)
                        break
                    time.sleep(5 * (attempt + 1))
                except Exception:
                    time.sleep(5 * (attempt + 1))
            time.sleep(0.3)
            if i % 250 == 0:
                print(source.name, i, 'of', len(ids), flush=True)
        print('%s: %d files needed, %d downloaded now, %d unavailable' % (source.name, len(ids), got, len(unavailable)), flush=True)


VUI_COLUMNS = '`id`, `vocal_ui_enum`, `race_id`, `normal_sound_id_1`, `normal_sound_id_2`, `pissed_sound_id_1`, `pissed_sound_id_2`'


def values(table, columns, lines):
    return 'INSERT INTO `%s` (%s) VALUES\n%s;\n' % (table, columns, ',\n'.join(lines)) if lines else ''


NO_VOICE = re.compile(r'^- (No sound yet|Voice may not be working.*|No \w+ voice: .*)$')
VOICE_LINE = '- Voice: %s emotes, error lines and combat sounds (`tools/races/retail_voices.py`; files in WHE-common `Sound/character`), the Kin race\'s where %s has none'


def update_readme(folder, origin):
    path = os.path.join(folder, 'readme.md')
    lines = [l for l in open(path, encoding='utf-8').read().split('\n') if not NO_VOICE.match(l) and not l.startswith('- Voice: ')]
    lines = [l.replace('(voice, emotes and names, copied at build time)', '(names, and the voice lines %s lacks)' % origin) for l in lines]
    start = lines.index('### Features')   # the end of the Features section
    at = next((i for i in range(start + 1, len(lines)) if lines[i].startswith('### ')), len(lines))
    while at > start + 1 and not lines[at - 1].strip():
        at -= 1
    lines.insert(at, VOICE_LINE % (origin.capitalize() + "'s", origin))
    nrm.write(path, '\n'.join(lines))


def sql_str(s):
    return "'" + s.replace(BS, BS * 2).replace("'", "\\'") + "'"


def write(modpaks, data, common, stock):
    sources, voices = plan(data, stock)
    names = listfile(data)
    se_rows, se_strings = stock_dbc(stock, 'SoundEntries')
    stock_ids = {r[0] for r in se_rows}
    st = lambda o: se_strings[o:se_strings.index(b'\0', o)].decode('latin1') if o else ''
    stock_files = {}   # lower-case dir\stem -> (dir, file) of the stock client's own files
    for r in se_rows:
        base = st(r[23])
        for o in r[3:13]:
            name = st(o)
            if name:
                stock_files[(base + BS + name.rsplit('.', 1)[0]).lower()] = (base, name)
    # soundentries ids other modpaks define (Cataclysm ports define the same kits, that is fine)
    targets = {'F-%03d' % fnum for _, _, _, fnum, _ in RACES}
    taken = {}
    for p in glob.glob(os.path.join(glob.escape(modpaks), 'F-*', 'dbc', '*soundentries*.sql')):
        owner = os.path.basename(os.path.dirname(os.path.dirname(p)))[:5]
        if owner in targets or owner in SAME_KITS:
            continue
        for m in re.finditer(r'^\((\d+),', open(p, encoding='utf-8', errors='replace').read(), re.M):
            taken[int(m.group(1))] = owner
    report = collections.Counter()
    copied = {}
    rows_of = {}   # (source, kit) -> soundentries row, or None when no file is usable

    def kit_row(source, kit, usage):
        if (source.name, kit) in rows_of:
            return rows_of[(source.name, kit)]
        files = []
        for fdid in source.entries[kit]:
            name = names.get(fdid, 'sound/character/retailvo/%d.ogg' % fdid).replace('/', BS)
            known = stock_files.get(name.rsplit('.', 1)[0].lower())
            if known:
                files.append((known[0], known[1], None))
                continue
            cached = os.path.join(source.files, '%d.bin' % fdid)
            if not os.path.exists(cached):
                report['file not downloaded'] += 1
                continue
            head = open(cached, 'rb').read(4)
            stem = name.rsplit('.', 1)[0]
            name = stem + ('.ogg' if head == b'OggS' else '.mp3' if head[:3] == b'ID3' or head[:2] in (b'\xff\xfb', b'\xff\xf3') else '.wav')
            folder, _, file = name.rpartition(BS)
            files.append((folder, file, cached))
        row = None
        if files:
            folder = collections.Counter(f[0].lower() for f in files).most_common(1)[0][0]
            mine = [f for f in files if f[0].lower() == folder]
            report['files outside the kit folder'] += len(files) - len(mine)
            report['files over 10'] += max(0, len(mine) - 10)
            mine = mine[:10]
            for f in mine:
                if f[2]:
                    copied[os.path.join(f[0], f[1]).lower()] = (os.path.join(f[0], f[1]), f[2])
            k = source.kit.get(kit, {})
            vid = kit + 1000000 if kit in taken else kit   # never clash with another modpak's own sounds
            report['kits moved past 1000000'] += vid != kit
            label = mine[0][1].rsplit('.', 1)[0].rstrip('0123456789').rstrip('_')
            min_d = float(k.get('MinDistance') or 0) or 8.0
            cut = float(k.get('DistanceCutoff') or 0) or 45.0
            vol = float(k.get('VolumeFloat') or 0) or 1.0
            padded = [f[1] for f in mine] + [''] * (10 - len(mine))
            row = (vid, "(%d, %d, %s, %s, %s, %s, '%.16f', 0, '%.16f', '%.16f', 0, 0)" % (
                vid, SOUND_TYPE[usage], sql_str(label), ', '.join(sql_str(f) for f in padded),
                ', '.join('1' if f else '0' for f in padded), sql_str(mine[0][0]), vol, min_d, cut))
        else:
            report['kits without a usable file'] += 1
        rows_of[(source.name, kit)] = row
        return row

    config, sound_data = [], FIRST_SOUND_DATA
    for source_name, race, key, fnum, siblings in RACES:
        source = sources[source_name]
        folders = glob.glob(os.path.join(glob.escape(modpaks), 'F-%03d_*' % fnum))
        assert len(folders) == 1, (fnum, folders)
        folder, tag = folders[0], '[BASE,F-%03d]' % fnum
        template = glob.glob(os.path.join(folder, 'sql', 'db-world', 'base', '*player_race_template.sql'))[0]
        kin = re.search(r'^\(@\w+, @\w+, (@\w+)', open(template, encoding='utf-8').read(), re.M).group(1)
        entries, ids = {}, {}

        def use(kit, usage):
            if kit in stock_ids:
                return kit
            row = kit_row(source, kit, usage)
            if not row:
                return 0
            entries[row[0]] = row[1]
            return row[0]

        emote_lines, vui_lines, csd_sql = [], [], []
        errors_by_enum = collections.defaultdict(lambda: [0, 0])
        for sex, (emotes, errors, combat) in enumerate(voices[race]):
            g = ('@Male', '@Female')[sex]
            for emote, kit in sorted(emotes.items()):
                kit = use(kit, 'emote')
                if kit:
                    emote_lines.append("(@EmotesTextSoundID := @EmotesTextSoundID +1, %3d, @%s, %-8s %7d)" % (emote, key, g + ',', kit))
            for enum, kit in errors.items():
                errors_by_enum[enum][sex] = use(kit, 'vui')
            mapped = {c: use(k, 'combat') for c, k in combat.items()}
            mapped = {c: k for c, k in mapped.items() if k}
            var = '@%s%sSoundData' % (key, ('Male', 'Female')[sex])
            config.append(('SET %s' % var).ljust(64) + '=   %d;' % sound_data)
            sound_data += 1
            display = '`%s_display_id`' % ('male', 'female')[sex]
            select = ', '.join([var] + [str(mapped[c]) if c in mapped else '`%s`' % c for c in CSD_COLUMNS[1:]])
            model = "(SELECT `cdi`.`model_id` FROM `creaturedisplayinfo` `cdi` JOIN `chrraces` `r` ON `cdi`.`id` = `r`.%s WHERE `r`.`id` = @%s)" % (display, key)
            others = ', '.join(['@%s' % key] + ['@%s' % k for _, r, k, _, _ in RACES if r in siblings])
            csd_sql.append(
                "-- %s: %s\nDELETE FROM `creaturesounddata` WHERE `id` = %s;\n"
                "INSERT INTO `creaturesounddata` (%s)\nSELECT %s\nFROM `creaturesounddata` WHERE `id` = (SELECT `sound_data` FROM `creaturemodeldata` WHERE `id` = %s);\n"
                "UPDATE `creaturemodeldata` SET `sound_data` = %s WHERE `id` = %s\n"
                "  AND `id` NOT IN (SELECT `cdi`.`model_id` FROM `creaturedisplayinfo` `cdi` JOIN `chrraces` `r` ON `cdi`.`id` IN (`r`.`male_display_id`, `r`.`female_display_id`)\n"
                "                   WHERE `r`.`id` NOT IN (%s)) -- never another race's model\n"
                "  AND EXISTS (SELECT 1 FROM `creaturesounddata` WHERE `id` = %s); -- the copy above found the model's row\n"
                % (('Male', 'Female')[sex], ', '.join('%s %d' % (c, k) for c, k in sorted(mapped.items())) or 'no retail combat sounds',
                   var, ', '.join('`%s`' % c for c in CSD_COLUMNS), select, model, var, model, others, var))
        for enum, (male, female) in sorted(errors_by_enum.items()):
            if male or female:
                vui_lines.append("(@VocalUISoundsID := @VocalUISoundsID +1, %2d, @%s, %7d, %7d, 0, 0)" % (enum, key, male, female))
        origin = 'Forever %s' % source.version if source_name == 'forever' else 'retail %s' % source.version
        dbc = os.path.join(folder, 'dbc', tag + '_%s.sql')
        for old in OLD_FILES.get(fnum, []):
            if os.path.exists(os.path.join(folder, 'dbc', old)):
                os.remove(os.path.join(folder, 'dbc', old))
        nrm.write(dbc % 'soundentries',
                  "-- soundentries: %d inserts, 0 updates, 0 deletes\n-- The %s voice kits of %s race %d (tools/races/retail_voices.py), with their ids\n\n"
                  "DELETE FROM `soundentries` WHERE `id` IN (%s);\n"
                  "INSERT INTO `soundentries` (`id`, `sound_type`, `name`, %s, %s, `base_dir`, `volume`, `flags`, `min_distance`, `distance_cutoff`, `eax_def`, `advanced_id`) VALUES\n%s;"
                  % (len(entries), origin.split()[0], origin.split()[0], race, ', '.join(str(i) for i in sorted(entries)),
                     ', '.join('`file_%d`' % i for i in range(1, 11)), ', '.join('`frequency_%d`' % i for i in range(1, 11)),
                     ',\n'.join(entries[i] for i in sorted(entries))))
        kin_note = "\n-- %s rows for what %s lacks\n" % (kin[1:], origin.split()[0].capitalize())
        nrm.write(dbc % 'emotestextsound',
                  "-- emotestextsound: the %s emote sounds of %s race %d (tools/races/retail_voices.py), then the Kin's for the rest\n\n"
                  "DELETE FROM `emotestextsound` WHERE `race_id` = @%s;\nSET @EmotesTextSoundID = (SELECT COALESCE(MAX(id), 0) FROM `emotestextsound`);\n"
                  "%s%s"
                  "INSERT INTO `emotestextsound` (`id`, `emotes_text_id`, `race_id`, `sex_id`, `sound_id`)\n"
                  "SELECT @EmotesTextSoundID := @EmotesTextSoundID +1, `emotes_text_id`, @%s, `sex_id`, `sound_id`\n"
                  "FROM (SELECT `k`.* FROM `emotestextsound` `k` LEFT JOIN `emotestextsound` `x` ON `x`.`race_id` = @%s AND `x`.`sex_id` = `k`.`sex_id`\n"
                  "      AND `x`.`emotes_text_id` = `k`.`emotes_text_id` WHERE `k`.`race_id` = %s AND `x`.`id` IS NULL ORDER BY `k`.`id`) AS `kin`;"
                  % (origin.split()[0], origin.split()[0], race, key,
                     values('emotestextsound', '`id`, `emotes_text_id`, `race_id`, `sex_id`, `sound_id`', emote_lines), kin_note, key, key, kin))
        nrm.write(dbc % 'vocaluisounds',
                  "-- vocaluisounds: the %s error voice lines of %s race %d (tools/races/retail_voices.py), then the Kin's for the rest\n\n"
                  "DELETE FROM `vocaluisounds` WHERE `race_id` = @%s;\nSET @VocalUISoundsID = (SELECT COALESCE(MAX(id), 0) FROM `vocaluisounds`);\n"
                  "%s%s"
                  "INSERT INTO `vocaluisounds` (`id`, `vocal_ui_enum`, `race_id`, `normal_sound_id_1`, `normal_sound_id_2`, `pissed_sound_id_1`, `pissed_sound_id_2`)\n"
                  "SELECT @VocalUISoundsID := @VocalUISoundsID +1, `vocal_ui_enum`, @%s, `normal_sound_id_1`, `normal_sound_id_2`, `pissed_sound_id_1`, `pissed_sound_id_2`\n"
                  "FROM (SELECT `k`.* FROM `vocaluisounds` `k` LEFT JOIN `vocaluisounds` `x` ON `x`.`race_id` = @%s AND `x`.`vocal_ui_enum` = `k`.`vocal_ui_enum`\n"
                  "      WHERE `k`.`race_id` = %s AND `x`.`id` IS NULL ORDER BY `k`.`id`) AS `kin`;"
                  % (origin.split()[0], origin.split()[0], race, key, values('vocaluisounds', VUI_COLUMNS, vui_lines), kin_note, key, key, kin))
        nrm.write(dbc % 'creaturesounddata',
                  "-- creaturesounddata: the %s combat sounds of %s race %d (tools/races/retail_voices.py): a copy of the model's\n"
                  "-- sound row with the vocal columns replaced (footsteps and the rest stay), then the race's models use it.\n"
                  "-- A model another race also uses keeps its row. Runs after creaturemodeldata (file order)\n\n%s"
                  % (origin.split()[0], origin.split()[0], race, '\n'.join(csd_sql)))
        update_readme(folder, origin.split()[0])
        print('%s: %d emotes, %d error lines, %d kits' % (os.path.basename(folder), len(emote_lines), len(vui_lines), len(entries)))
    # config.sql: the CreatureSoundData ids
    path = os.path.join(modpaks, 'config.sql')
    text = open(path, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in text else '\n'
    block = nl.join([CONFIG_BEGIN] + config + [CONFIG_END]) + nl
    if CONFIG_BEGIN in text:
        text = re.sub(re.escape(CONFIG_BEGIN) + r'.*?' + re.escape(CONFIG_END) + r'\r?\n', lambda m: block, text, flags=re.S)
    else:
        anchor = re.search(r'^-- Classes\r?$', text, re.M)
        text = text[:anchor.start()] + block + nl + text[anchor.start():]
    open(path, 'w', encoding='utf-8', newline='').write(text)
    # files
    size = 0
    for rel, cached in sorted(copied.values()):
        target = os.path.join(common, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        if not os.path.exists(target) or os.path.getsize(target) != os.path.getsize(cached):
            shutil.copyfile(cached, target)
        size += os.path.getsize(target)
    print('%d sound files (%d MB) in %s' % (len(copied), size >> 20, common))
    for k, v in sorted(report.items()):
        print('  %s: %d' % (k, v))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=('download', 'write'))
    ap.add_argument('modpaks', nargs='?', default=os.path.join(HERE, '..', '..', 'modpaks'))
    ap.add_argument('--data', default=r'D:\wow-scratch\retail-vo')
    ap.add_argument('--common', default=os.path.join(HERE, '..', '..', '..', 'WHE-common', 'patch-A.MPQ'))
    ap.add_argument('--stock', default=r'D:\GitHub\References\original-client-dbc')
    a = ap.parse_args()
    if a.mode == 'download':
        download(a.data, a.stock)
    else:
        write(a.modpaks, a.data, a.common, a.stock)


if __name__ == '__main__':
    main()

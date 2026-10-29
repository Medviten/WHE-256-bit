#!/usr/bin/env python3
"""Add the CoA Custom 1.9 racial spells (Ilusixn's CoA race files) to the WHE modpaks of the same races.

The spell rows come from CoA's client Spell.dbc (its server SQL stores the float fields as integers), renumbered into
vacant slots: CoA's ids (1400 + CoA race * 10 + slot, and three 8xxxxx helper copies of stock spells) would make the
client's spell table 14 million rows long. Fixes for 3.3.5:
- aura 345 (Ascension's spell power aura) becomes 13, SPELL_AURA_MOD_DAMAGE_DONE, for the magic schools (126)
- spell family 25 (Ascension) becomes 0; spell visuals the stock client lacks become 0
- icons: Ascension's SpellIcon ids are resolved to paths; stock icons keep their ids, retail icons get new SpellIcon
  rows when an icon folder has them, else a similar stock icon
- the flavour line of each tooltip loses its clause about Ascension's classes ("as every Witch Doctor learns")

Each modpak gets the spells, their SkillLineAbility rows (learned with the race's racial skill line) and spell icons
as marked blocks at the end of its spell, skilllineability and spellicon files (created when missing); rerunning
replaces the blocks. Modpaks that already give their race racial abilities (or copy a stock race's) get the block
commented out. The ids go into a marked block of config.sql.

usage: coa_racials.py <CoA server sql/14_races_1.9.sql> <CoA client Spell.dbc> <Ascension SpellIcon.dbc>
                      <stock DBFilesClient> [icon folder ...]"""
import glob
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import new_race_modpaks as nrm   # noqa: E402

MODPAKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'modpaks')
SPELL_BASE, SLA_BASE, ICON_BASE = 81000, 31600, 4400
BEGIN, END = '-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>', '-- <<< CoA Custom 1.9 racials <<<'
README = '### CoA Custom 1.9 racials'

# CoA race (from the spell id), WHE modpak, variable prefix, active, CoA race name / why the block is commented out
TARGETS = [
    (12, 'F-017', 'ZandalariTroll', False, 'Zandalari Troll', 'the race already gets the Troll racials'),
    (13, 'F-024', 'Worgen', False, 'Worgen', 'the race already has its Cataclysm racials'),
    (14, 'F-005', 'HighElf', False, 'High Elf', 'the race already has racials'),
    (15, 'F-042', 'Tuskarr', True, 'Tuskarr', ''),
    (16, 'F-025', 'KulTiran', True, 'Kul Tiran', ''),
    (17, 'F-032', 'Taunka', False, 'Taunka', 'the race already gets the Tauren racials'),
    (18, 'F-036', 'Vrykul', True, 'Vrykul', ''),
    (20, 'F-021', 'HordePandaren', True, 'Pandaren (Horde)', ''),
    (21, 'F-030', 'Naga', True, 'Naga', ''),
    (22, 'F-022', 'Broken', False, 'Broken', 'the race already gets the Draenei racials'),
    (23, 'F-047', 'FelOrc', True, 'Fel Orc', ''),
    (24, 'F-049', 'ForestTroll', True, 'Forest Troll', ''),
    (25, 'F-051', 'IceTroll', True, 'Ice Troll', ''),
    (26, 'F-048', 'Skeleton', True, 'Skeleton', ''),
    (29, 'F-020', 'AlliancePandaren', True, 'Pandaren (Alliance)', ''),
    (31, 'F-044', 'Murloc', True, 'Murloc (Horde)', ''),
    (32, 'F-041', 'ThinHuman', True, 'Forgotten (thin human)', ''),
    (48, 'F-016', 'DarkIronDwarf', False, 'Dark Iron Dwarf', 'the race already has Dungeon Delver'),
    (49, 'F-007', 'MagharOrc', False, 'Mag\'har Orc', 'the race already has its BfA racials'),
    (50, 'F-045', 'Furbolg', True, 'Furbolg', ''),
    (53, 'F-014', 'Ogre', True, 'Ogre', ''),
    (53, 'F-031', 'Ogre', True, 'Ogre', ''),
    (55, 'F-053', 'Eredar', True, 'Eredar', ''),
    (59, 'F-035', 'VoidElf', True, 'Void Elf', ''),
    (60, 'F-055', 'FelElf', True, 'Illidari Blood Elf', ''),
    (62, 'F-033', 'LightforgedDraenei', True, 'Lightforged Draenei', ''),
    (63, 'F-034', 'Nightborne', True, 'Nightborne', ''),
    (66, 'F-028', 'HighmountainTauren', True, 'Highmountain Tauren', ''),
    (67, 'F-040', 'Mechagnome', True, 'Mechagnome', ''),
    (68, 'F-038', 'AllianceEarthen', True, 'Earthen (Alliance)', ''),
    (69, 'F-039', 'HordeEarthen', True, 'Earthen (Horde)', ''),
    (74, 'F-019', 'Vulpera', True, 'Vulpera', ''),
    (81, 'F-043', 'Darkfallen', True, 'Darkfallen (Horde)', ''),
    (83, 'F-060', 'Gnoll', True, 'Gnoll', ''),
    (100, 'F-057', 'Centaur', True, 'Centaur', ''),
    (101, 'F-069', 'Venthyr', False, 'Venthyr', 'Aetheria\'s racials replace them'),
    (104, 'F-046', 'SlimeGiant', True, 'Slime Giant', ''),
    (107, 'F-068', 'Kyrian', False, 'Kyrian', 'Aetheria\'s racials replace them'),
    (112, 'F-064', 'Hozen', True, 'Hozen', ''),
    (114, 'F-065', 'Sylvari', True, 'Sylvari', ''),
    (115, 'F-066', 'Mantid', True, 'Mantid', ''),
    (116, 'F-067', 'Ethereal', True, 'Ethereal', ''),
    (120, 'F-070', 'Banshee', True, 'Banshee', ''),
    (122, 'F-071', 'FacelessOne', True, 'Faceless One', ''),
    (123, 'F-052', 'Qiraji', True, 'Qiraji (shelved in CoA 1.9)', ''),
    (54, 'F-073', 'AllianceDracthyr', True, 'Dracthyr (Alliance)', ''),
    (58, 'F-074', 'HordeDracthyr', True, 'Dracthyr (Horde)', ''),
]
# CoA races added after the first run: their spells and SkillLineAbility rows are numbered after everyone else's, so
# the spell ids characters may already have learned stay put
APPENDED = (54, 58)
HELPERS = {801044: 'SlowAndRootDispel', 820589: 'EscapeArtist', 828730: 'ArcaneTorrent'}
NOTES = {14001006: 'CoA drives it with the C++ scripts spell_centaur_gallop/_aura, which WHE does not have: '
                   'without them it is a plain speed buff'}
CLASS_WORDS = ['Witch Doctor', 'Ranger', 'Reaper', 'Starcaller', 'Barbarian', 'monks', 'Sun Cleric', 'Felsworn', 'Necromancer',
               'Pyromancer', 'Primalist', 'Tinker', 'Chronomancer', 'Cultist', 'Templar', 'Runemaster', 'Bloodmage', 'Venomancer']
# retail icons no client folder has: a similar stock icon
FALLBACK_ICONS = {
    'ability_demonhunter_illidansgrasp': 'Achievement_Boss_Illidan',
    'ability_mage_arcanebarrage_nightborne': 'Ability_Mage_ArcaneBarrage',
    'ability_racial_arcaneaffinity': 'Spell_Holy_MagicalSentry',
    'ability_racial_combatanalysis': 'INV_Gizmo_02',
    'ability_racial_forceshield': 'Spell_Holy_PowerWordShield',
    'ability_racial_hyperorganiclightoriginator': 'Spell_Holy_HolyBolt',
    'ability_racial_mastercraft': 'Trade_Engineering',
    'ability_racial_rearm': 'INV_Gizmo_RocketBoot_01',
    'ability_racial_skeletonpinkie': 'INV_Misc_Bone_HumanSkull_01',
    'achievement_alliedrace_magharorc': 'Achievement_Character_Orc_Male',
    'achievement_alliedrace_nightborne': 'Achievement_Character_Bloodelf_Female',
    'achievement_boss_argus_maleeredar': 'Achievement_Boss_Kiljaedan',
    'achievement_boss_elitenagamale': 'Achievement_Boss_LadyVashj',
    'achievement_boss_hellfire_felorccouncil': 'Spell_Shadow_UnholyFrenzy',
    'achievements_zone_highmountain': 'Achievement_Character_Tauren_Male',
    'spell_druid_bristlingfur': 'Ability_Racial_BearForm',
    '_pandaren_01': 'Spell_Misc_Food',
    'ability_demonhunter_spectralsight': 'Spell_Shadow_DetectInvisibility',
    'ability_monk_paralysis': 'Ability_Rogue_KidneyShot',
    'ability_racial_cantrips': 'Spell_Magic_LesserInvisibilty',
    'ability_racial_magicalresistance': 'Spell_Shadow_AntiMagicShell',
    'ability_racial_twoforms': 'Ability_Racial_BearForm',
    'ability_racial_viciousness': 'Ability_Druid_Rake',
    'ability_racial_wardoftheloafrost': 'Spell_Frost_FrostWard',
    'ability_racial_wardoftheloa': 'Spell_Nature_Regenerate',
    'achievement_boss_gruul': 'Achievement_Boss_GruulTheDragonkiller',
    'inv_cape_special_furbolg_d_01': 'INV_Misc_Pelt_Bear_01',
    'inv_misc_head_tuskarr': 'Achievement_Reputation_Tuskarr',
    '_monkspecialattack_dodgepandaren': 'Ability_Rogue_Feint',
    'ability_earthen_pillar': 'Spell_Nature_StoneSkinTotem',
    'ability_earthenfury_giftofearth': 'Spell_Nature_StoneClawTotem',
}

HERE = os.path.dirname(os.path.abspath(__file__))
COLUMNS = '''id category dispel mechanic attributes attributes_ex_1 attributes_ex_2 attributes_ex_3 attributes_ex_4
attributes_ex_5 attributes_ex_6 attributes_ex_7 stances unk_1 excluded_stances unk_2 targets target_creature_type
spell_focus_object facing_caster_flags caster_aura_state target_aura_state excluded_caster_aura_state
excluded_target_aura_state caster_aura_spell target_aura_spell excluded_caster_aura_spell excluded_target_aura_spell
cast_time_index recovery_time category_recovery_time interrupt_flags aura_interrupt_flags channel_interrupt_flags
proc_flags proc_chance proc_charges max_level base_level spell_level duration_index power_type power_cost
power_cost_per_level power_per_second power_per_second_per_level range_index speed modal_next_spell stack_amount
totem_1 totem_2 reagent_1 reagent_2 reagent_3 reagent_4 reagent_5 reagent_6 reagent_7 reagent_8 reagent_count_1
reagent_count_2 reagent_count_3 reagent_count_4 reagent_count_5 reagent_count_6 reagent_count_7 reagent_count_8
equipped_item_class equipped_item_subclass_mask equipped_item_inventorytype_mask effect_1 effect_2 effect_3
effect_die_sides_1 effect_die_sides_2 effect_die_sides_3 effect_real_points_per_level_1 effect_real_points_per_level_2
effect_real_points_per_level_3 effect_base_points_1 effect_base_points_2 effect_base_points_3 effect_mechanic_1
effect_mechanic_2 effect_mechanic_3 effect_implicit_target_a_1 effect_implicit_target_a_2 effect_implicit_target_a_3
effect_implicit_target_b_1 effect_implicit_target_b_2 effect_implicit_target_b_3 effect_radius_index_1
effect_radius_index_2 effect_radius_index_3 effect_apply_aura_name_1 effect_apply_aura_name_2 effect_apply_aura_name_3
effect_amplitude_1 effect_amplitude_2 effect_amplitude_3 effect_multiple_value_1 effect_multiple_value_2
effect_multiple_value_3 effect_chain_target_1 effect_chain_target_2 effect_chain_target_3 effect_item_type_1
effect_item_type_2 effect_item_type_3 effect_misc_value_a_1 effect_misc_value_a_2 effect_misc_value_a_3
effect_misc_value_b_1 effect_misc_value_b_2 effect_misc_value_b_3 effect_trigger_spell_1 effect_trigger_spell_2
effect_trigger_spell_3 effect_points_per_combo_point_1 effect_points_per_combo_point_2 effect_points_per_combo_point_3
effect_spell_class_mask_a_1 effect_spell_class_mask_a_2 effect_spell_class_mask_a_3 effect_spell_class_mask_b_1
effect_spell_class_mask_b_2 effect_spell_class_mask_b_3 effect_spell_class_mask_c_1 effect_spell_class_mask_c_2
effect_spell_class_mask_c_3 spell_visual_1 spell_visual_2 spell_icon_id active_icon_id spell_priority'''.split()
for part in ('spell_name', 'spell_subtext', 'spell_desc', 'spell_tooltip'):
    COLUMNS += ['%s_%s' % (part, l) for l in ('enus', 'kokr', 'frfr', 'dede', 'zhcn', 'zhtw', 'eses', 'esmx', 'ruru', 'jajp',
                                               'ptpt', 'itit', 'unused_1', 'unused_2', 'unused_3', 'unused_4', 'flags')]
COLUMNS += '''power_cost_percentage start_recovery_category start_recovery_time maximum_target_level spell_class_set
spell_class_mask_1 spell_class_mask_2 spell_class_mask_3 max_affected_targets damage_class prevention_type
stance_bar_order effect_damage_multiplier_1 effect_damage_multiplier_2 effect_damage_multiplier_3 min_faction_id
min_reputation req_aura_vision totem_category_1 totem_category_2 area_group_id school_mask rune_cost_id spell_missile_id
power_display_id effect_bonus_multiplier_1 effect_bonus_multiplier_2 effect_bonus_multiplier_3 spell_desc_variable_id
spell_difficulty_id'''.split()
assert len(COLUMNS) == 234
FLOATS = {47} | set(range(77, 80)) | set(range(101, 104)) | set(range(119, 122)) | set(range(216, 219)) | set(range(229, 232))
STRINGS = set(range(136, 152)) | set(range(153, 169)) | set(range(170, 186)) | set(range(187, 203))
ENUS = {136, 153, 170, 187}
# DBCTool's spell table: these integer columns are int32, every other one uint32
SIGNED = {COLUMNS.index(c) for c in COLUMNS if re.match(r'reagent_\d$|equipped_item_|effect_die_sides_|effect_base_points_|effect_misc_value_', c)}


def load_spells(path, wanted):
    d = open(path, 'rb').read()
    n, f, size, ss = struct.unpack_from('<4I', d, 4)
    base, out = 20 + n * size, {}
    for i in range(n):
        o = 20 + i * size
        sid = struct.unpack_from('<I', d, o)[0]
        if sid not in wanted:
            continue
        row = []
        for c, v in enumerate(struct.unpack_from('<234i', d, o)):
            if c in FLOATS:
                row.append(struct.unpack_from('<f', d, o + 4 * c)[0])
            elif c in STRINGS:
                row.append(d[base + v:d.index(b'\0', base + v)].decode('utf-8') if 0 <= v < ss else '')
            else:
                row.append(v if c in SIGNED else v & 0xFFFFFFFF)
        out[sid] = row
    return out


def ids_of(path):
    rows, _, _ = nrm.load_dbc(path)
    return {struct.unpack_from('<I', r)[0] for r in rows}


def trim(desc):
    """Drop the clause about Ascension's classes from the flavour line (the text before the first blank line)."""
    if '\n\n' not in desc:
        return desc
    first, rest = desc.split('\n\n', 1)
    hits = [first.find(w) for w in CLASS_WORDS if w in first]
    if hits:
        cut = first.rfind(',', 0, min(hits))
        if cut > 0:
            first = first[:cut] + '.'
    return first + '\n\n' + rest


def sql_text(s):
    return nrm.sql_str(s).replace('\r', '').replace('\n', '\\n')


def camel(name):
    return ''.join(p[:1].upper() + p[1:] for p in re.split(r'[_\W]+', name) if p)


class Plan:
    def __init__(self, sql, coa_spell, asc_icon, stock, icon_dirs):
        wanted_races = {t[0] for t in TARGETS}
        coa_ids = [int(m) for m in re.findall(r'REPLACE INTO `spell_dbc` VALUES \((\d+),', open(sql, encoding='utf-8').read())]
        self.racials = {}   # CoA race -> sorted CoA spell ids
        for sid in coa_ids:
            race = (sid - 14000000) // 10
            if race in wanted_races:
                self.racials.setdefault(race, []).append(sid)
        for race in self.racials:
            self.racials[race].sort()
        self.spells = load_spells(coa_spell, set(coa_ids) | set(HELPERS))
        self.new_id, self.var = {}, {}
        next_id = SPELL_BASE
        for sid in sorted(HELPERS):
            self.new_id[sid], self.var[sid] = next_id, '@CoAHelper' + HELPERS[sid]
            next_id += 1
        keys = {}
        for race, fnum, key, active, name, why in TARGETS:
            keys.setdefault(race, key)
        order = sorted(self.racials, key=lambda r: (r in APPENDED, APPENDED.index(r) if r in APPENDED else r))
        for race in order:
            for sid in self.racials[race]:
                self.new_id[sid], self.var[sid] = next_id, '@CoA%sRacial%d' % (keys[race], sid % 10)
                next_id += 1
        self.sla = {}
        next_sla = SLA_BASE
        for race in order:
            for sid in self.racials[race]:
                self.sla[sid] = (next_sla, '@CoA%sSkillLineAbility%d' % (keys[race], sid % 10))
                next_sla += 1
        # icons
        rows, strings, _ = nrm.load_dbc(asc_icon)
        asc = {struct.unpack_from('<I', r)[0]: nrm.string(strings, struct.unpack_from('<I', r, 4)[0]) for r in rows}
        rows, strings, _ = nrm.load_dbc(os.path.join(stock, 'SpellIcon.dbc'))
        stock_icons = {nrm.string(strings, struct.unpack_from('<I', r, 4)[0]).lower(): struct.unpack_from('<I', r)[0] for r in rows}
        have = {f.rsplit('.', 1)[0].lower() for d in icon_dirs for f in os.listdir(d)}
        self.icon = {}      # CoA icon id -> (value, comment)
        self.new_icons = {}  # path -> (id, var)
        for sid, row in self.spells.items():
            icon = row[133]
            if icon in self.icon:
                continue
            path = asc.get(icon)
            if path is None:
                raise SystemExit('spell %d: icon %d not in Ascension SpellIcon.dbc' % (sid, icon))
            base = path.rsplit('\\', 1)[-1]
            if path.lower() in stock_icons:
                self.icon[icon] = (str(stock_icons[path.lower()]), base)
            elif base.lower() in have:
                self.new_icons.setdefault(path, None)
                self.icon[icon] = (path, base)
            elif base.lower() in FALLBACK_ICONS:
                fb = 'interface\\icons\\' + FALLBACK_ICONS[base.lower()].lower()
                if fb not in stock_icons:
                    raise SystemExit('fallback icon %s for %s is not a stock icon' % (FALLBACK_ICONS[base.lower()], base))
                self.icon[icon] = (str(stock_icons[fb]), '%s (stock stand-in for %s)' % (FALLBACK_ICONS[base.lower()], base))
            else:
                raise SystemExit('spell %d: icon %s is neither stock, in an icon folder nor in FALLBACK_ICONS' % (sid, path))
        for n, path in enumerate(sorted(self.new_icons, key=str.lower)):
            self.new_icons[path] = (ICON_BASE + n, '@IconCoA' + camel(path.rsplit('\\', 1)[-1]))
        for icon, (value, comment) in list(self.icon.items()):
            if value in self.new_icons:
                self.icon[icon] = (self.new_icons[value][1], comment)
        self.visuals = ids_of(os.path.join(stock, 'SpellVisual.dbc'))

    def name(self, sid):
        return self.spells[sid][136]

    def text(self, sid, column=170):
        """The trimmed tooltip text with the helper spells' new ids."""
        return re.sub(r'\$(\d{6})', lambda m: '$%d' % self.new_id.get(int(m.group(1)), int(m.group(1))), trim(self.spells[sid][column]))

    def row_sql(self, sid):
        r, fixes = list(self.spells[sid]), []
        for k in range(3):
            if r[95 + k] == 345:
                r[95 + k], fixes = 13, fixes + ['aura 345 -> 13 (spell power)']
                if r[110 + k] == 127:
                    r[110 + k] = 126
            if r[116 + k] in self.var:
                r[116 + k] = self.var[r[116 + k]]
        if r[208] == 25:
            r[208], fixes = 0, fixes + ['spell family 25 -> 0']
        for c in (131, 132):
            if r[c] and r[c] not in self.visuals:
                r[c], fixes = 0, fixes + ['visual %d -> 0' % r[c]]
        icon_value, icon_comment = self.icon[r[133]]
        r[133] = icon_value
        for c in (170, 187):
            r[c] = self.text(sid, c)
        values = []
        for c, v in enumerate(r):
            if c == 0:
                values.append(self.var[sid])
            elif c in STRINGS:
                values.append(sql_text(v) if c in ENUS else "''")
            elif c in FLOATS:
                values.append(repr(float(v)).replace('.0', '') if float(v).is_integer() else repr(round(v, 6)))
            else:
                values.append(str(v))
        desc = r[170].split('\n\n')[-1].replace('\n', ' ')
        comment = '-- %s (CoA %d)%s: %s' % (self.name(sid), sid, ' [' + '; '.join(fixes) + ']' if fixes else '', desc[:150])
        if sid in NOTES:
            comment += '\n-- ' + NOTES[sid]
        comment += '\n-- icon: ' + icon_comment
        return comment + '\n(' + ', '.join(values) + ')'

    def deps(self, sids):
        return sorted({h for sid in sids for h in HELPERS
                       if h in (self.spells[sid][116], self.spells[sid][117], self.spells[sid][118]) or
                       re.search(r'\$%d' % h, self.spells[sid][170] + self.spells[sid][187])})


def block(text, body):
    """text with the marked CoA block replaced by (or appended as) body."""
    marked = BEGIN + '\n' + body.rstrip() + '\n' + END + '\n'
    pattern = re.compile(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n?', re.S)
    if pattern.search(text):
        return pattern.sub(lambda m: marked, text)
    return (text.rstrip() + '\n\n' if text.strip() else '') + marked


def update(path, body):
    text = open(path, encoding='utf-8').read() if os.path.exists(path) else ''
    nrm.write(path, block(text, body))


def wrap(lines, active, why):
    if active:
        return lines
    return ['-- Commented out: %s. Remove the comment markers to give the race CoA\'s racials instead.' % why, '/*'] + lines + ['*/']


def main():
    sql, coa_spell, asc_icon, stock = sys.argv[1:5]
    plan = Plan(sql, coa_spell, asc_icon, stock, sys.argv[5:])
    for race, fnum, key, active, name, why in TARGETS:
        sids = plan.racials.get(race, [])
        if not sids:
            print('no CoA spells for race %d (%s)' % (race, name))
            continue
        folder = glob.glob(os.path.join(MODPAKS, fnum + '_*'))[0]
        tag = '[BASE,%s]' % fnum
        header = ['-- %s racials from CoA Custom 1.9 (Ilusixn\'s CoA race files, CoA race %d), renumbered into vacant slots'
                  % (name, race)]
        spells = plan.deps(sids) + sids
        lines = ['DELETE FROM `spell` WHERE `id` IN (%s);' % ', '.join(plan.var[s] for s in spells),
                 'INSERT INTO `spell` (%s) VALUES' % ', '.join('`%s`' % c for c in COLUMNS),
                 ',\n'.join(plan.row_sql(s) for s in spells) + ';']
        update(os.path.join(folder, 'dbc', tag + '_spell.sql'), '\n'.join(header + wrap(lines, active, why)))
        rows = ['(%s, @%sRacials, %s, @%sMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0)%s -- %s' % (
            plan.sla[s][1], key, plan.var[s], key, ';' if s == sids[-1] else ',', plan.name(s)) for s in sids]
        lines = ['DELETE FROM `skilllineability` WHERE `id` IN (%s);' % ', '.join(plan.sla[s][1] for s in sids),
                 'INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, '
                 '`excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, '
                 '`skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES'] + rows
        update(os.path.join(folder, 'dbc', tag + '_skilllineability.sql'),
               '\n'.join(['-- The %s racials, learned with the racial skill line' % name] + wrap(lines, active, why)))
        icons = sorted({plan.icon[plan.spells[s][133]][0] for s in spells} & {v for _, v in plan.new_icons.values()})
        if icons:
            paths = {v: p for p, (_, v) in plan.new_icons.items()}
            lines = ['DELETE FROM `spellicon` WHERE `id` IN (%s);' % ', '.join(icons),
                     'INSERT INTO `spellicon` (`id`, `name`) VALUES',
                     ',\n'.join('(%s, %s)' % (v, nrm.sql_str(paths[v])) for v in icons) + ';']
            update(os.path.join(folder, 'dbc', tag + '_spellicon.sql'),
                   '\n'.join(['-- Retail icons of the %s racials (the client needs the icon files)' % name] + wrap(lines, active, why)))
        readme(folder, plan, sids, race, name, active, why, tag)
        print('%s %s: %d spells%s' % (fnum, key, len(sids), '' if active else ' (commented out)'))
    write_config(plan)


def readme(folder, plan, sids, race, name, active, why, tag):
    path = os.path.join(folder, 'readme.md')
    text = open(path, encoding='utf-8').read()
    text = text.split('\n' + README)[0].rstrip()
    if active:
        text = re.sub(r'\n- (No racial abilities yet|Racial abilities not yet implemented)[^\n]*', '', text)
    lines = ['', '', README,
             ('- Active: learned with the racial skill line' if active else '- Commented out (%s); remove the comment markers in the '
              'CoA blocks to use them' % why),
             '- From CoA race %d (%s), renumbered; blocks at the end of `%s_spell.sql`, `_skilllineability.sql` and `_spellicon.sql`'
             % (race, name, tag)]
    for s in sids:
        desc = plan.text(s).split('\n\n')[-1].replace('\n', ' ')
        lines.append('    - %s: %s' % (plan.name(s), desc))
        if s in NOTES:
            lines.append('      (%s)' % NOTES[s])
    nrm.write(path, text + '\n'.join(lines))


def write_config(plan):
    path = os.path.join(MODPAKS, 'config.sql')
    lines = ['-- CoA Custom 1.9 racials (Ilusixn\'s CoA race files): spells in vacant slots from %d, SkillLineAbility from %d,'
             % (SPELL_BASE, SLA_BASE), '-- spell icons from %d. The comment gives the CoA spell id.' % ICON_BASE]
    for sid in sorted(plan.new_id, key=plan.new_id.get):
        lines.append(('SET ' + plan.var[sid]).ljust(63) + '= %8d; -- %s (CoA %d)' % (plan.new_id[sid], plan.name(sid), sid))
    for sid in sorted(plan.sla, key=lambda s: plan.sla[s][0]):
        lines.append(('SET ' + plan.sla[sid][1]).ljust(63) + '= %8d; -- %s' % (plan.sla[sid][0], plan.name(sid)))
    for p, (i, v) in sorted(plan.new_icons.items(), key=lambda x: x[1][0]):
        lines.append(('SET ' + v).ljust(63) + '= %8d; -- %s' % (i, p))
    update(path, '\n'.join(lines))


if __name__ == '__main__':
    main()

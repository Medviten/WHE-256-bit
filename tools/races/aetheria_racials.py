#!/usr/bin/env python3
"""Add the Kyrian and Venthyr racials of Aetheria's Kyrian/Venthyr package (https://github.com/Shotboom12/aetheria-client
and aetheria-server) to F-068 and F-069, in place of CoA Custom 1.9's (coa_racials.py comments those out).

The spells keep Aetheria's ids (111100-111113, 111200-111212): the C++ scripts in src/ (kyrian_hover.cpp,
kyrian_racials.cpp, venthyr_racials.cpp, ported from aetheria-server) use them. The rows are the package's
data/spells.json, which matches the server migrations' final spell_dbc rows; Bat Form's creature becomes
@VenthyrBatCreature (Aetheria's own creature 9501110 is not in WHE). The spells Aetheria's scripts teach on login are
learned with the racial skill line instead (SkillLineAbility from 31780). spell_script_names and spell_bonus_data
come from the migrations.

Each modpak gets marked blocks at the end of its spell and skilllineability files, the world files
[BASE,F-0xx]_spell_script_names.sql and _spell_bonus_data.sql, and a readme section; config.sql gets the ids.

usage: aetheria_racials.py <aetheria-client> <aetheria-server> [modpaks dir]"""
import glob
import json
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coa_racials as cr          # noqa: E402
import new_race_modpaks as nrm    # noqa: E402

VERSION = 'kyrian-venthyr-20261027-1'
BEGIN, END = '-- >>> Aetheria racials (tools/races/aetheria_racials.py) >>>', '-- <<< Aetheria racials <<<'
README = '### Aetheria racials'
SLA_BASE = 31780
BAT_CREATURE = (9501110, '@VenthyrBatCreature', 16175, 'Vampiric Shadowbat')
# key, modpak, Aetheria race id, spell id range, the spells Aetheria's scripts teach on login (learned here with the
# racial skill line), notes for the readme
RACES = [
    ('Kyrian', 'F-068', 60, range(111100, 111114), [111100, 111104, 111105, 111106, 111107, 111108, 111110],
     ['Ascended Wings also halves fall damage (patches/whe-acore.patch)',
      'The wowdecomp-256-bit client does not have Aetheria\'s takeoff and landing animations for Ascended Hover yet']),
    ('Venthyr', 'F-069', 61, range(111200, 111213), [111200, 111201, 111202, 111203, 111204, 111206, 111209],
     ['Crimson Feast keeps fractional healing between ticks (patches/whe-acore.patch)',
      'Vampire Bat Form turns you into creature %d (%s, set in config.sql as %s; Aetheria uses its own bat) and '
      'flies only where flying mounts may, with 225 riding skill' % (BAT_CREATURE[2], BAT_CREATURE[3], BAT_CREATURE[1])]),
]
WORLD_TABLES = {
    'spell_script_names': ('`spell_id`, `ScriptName`', 'spell_id'),
    'spell_bonus_data': ('`entry`, `direct_bonus`, `dot_bonus`, `ap_bonus`, `ap_dot_bonus`, `comments`', 'entry'),
}


def load_spells(client):
    spells = {}
    for r in json.load(open(os.path.join(client, 'data', 'spells.json'), encoding='utf-8'))['rows']:
        w, row = r['words'], []
        for c in range(234):
            if c in cr.STRINGS:
                row.append(r['strings'].get(str(c), ''))
            elif c in cr.FLOATS:
                row.append(struct.unpack('<f', struct.pack('<I', w[c]))[0])
            elif c in cr.SIGNED and w[c] >= 1 << 31:
                row.append(w[c] - (1 << 32))
            else:
                row.append(w[c])
        spells[r['id']] = row
    return spells


def world_rows(server):
    """{table: [values]} of the migrations' INSERTs into spell_script_names and spell_bonus_data, in order."""
    order = json.load(open(os.path.join(server, 'package.json'), encoding='utf-8'))['migrationOrder']
    out = {t: {} for t in WORLD_TABLES}
    for name in order:
        text = open(os.path.join(server, 'migrations', name), encoding='utf-8').read()
        for table in WORLD_TABLES:
            for m in re.finditer(r'INSERT INTO `%s` \([^)]*\) VALUES\s*\((.*?)\);' % table, text, re.S):
                out[table][m.group(1)] = None
    return {t: list(rows) for t, rows in out.items()}


def row_sql(sid, row):
    r = list(row)
    for k in range(3):
        if r[110 + k] == BAT_CREATURE[0]:
            r[110 + k] = BAT_CREATURE[1]
    values = []
    for c, v in enumerate(r):
        if c in cr.STRINGS:
            values.append(cr.sql_text(v) if c in cr.ENUS else "''")
        elif c in cr.FLOATS:
            values.append(repr(float(v)).replace('.0', '') if float(v).is_integer() else repr(round(v, 6)))
        else:
            values.append(str(v))
    desc = (r[170] or r[187]).replace('\r', '').replace('\n', ' ')
    return '-- %s (%d): %s\n(%s)' % (r[136], sid, desc[:150], ', '.join(values))


def update(path, body):
    text = open(path, encoding='utf-8').read() if os.path.exists(path) else ''
    marked = BEGIN + '\n' + body.rstrip() + '\n' + END + '\n'
    pattern = re.compile(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n?', re.S)
    text = pattern.sub(lambda m: marked, text) if pattern.search(text) else \
        (text.rstrip() + '\n\n' if text.strip() else '') + marked
    nrm.write(path, text)


def sla_var(key, n):
    return '@Aetheria%sSkillLineAbility%d' % (key, n)


def main():
    client, server = sys.argv[1:3]
    modpaks = sys.argv[3] if len(sys.argv) > 3 else cr.MODPAKS
    spells, world = load_spells(client), world_rows(server)
    config, next_sla = [], SLA_BASE
    for key, fnum, aetheria_race, ids, learned, notes in RACES:
        folder = glob.glob(os.path.join(modpaks, fnum + '_*'))[0]
        tag = '[BASE,%s]' % fnum
        sids = [s for s in ids if s in spells]
        lines = ['-- %s racials from Aetheria\'s Kyrian/Venthyr package (%s), Aetheria\'s spell ids: the C++ scripts in src/ '
                 'use them' % (key, VERSION),
                 'DELETE FROM `spell` WHERE `id` BETWEEN %d AND %d;' % (sids[0], sids[-1]),
                 'INSERT INTO `spell` (%s) VALUES' % ', '.join('`%s`' % c for c in cr.COLUMNS),
                 ',\n'.join(row_sql(s, spells[s]) for s in sids) + ';']
        update(os.path.join(folder, 'dbc', tag + '_spell.sql'), '\n'.join(lines))

        slas = []
        for n, s in enumerate(learned, 1):
            slas.append((sla_var(key, n), s))
            config.append(('SET ' + sla_var(key, n)).ljust(63) + '= %8d; -- %s' % (next_sla, spells[s][136]))
            next_sla += 1
        rows = ['(%s, @%sRacials, %d, @%sMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0)%s -- %s' % (
            v, key, s, key, ';' if i == len(slas) - 1 else ',', spells[s][136]) for i, (v, s) in enumerate(slas)]
        lines = ['-- The %s racials of Aetheria\'s package, learned with the racial skill line' % key,
                 'DELETE FROM `skilllineability` WHERE `id` IN (%s);' % ', '.join(v for v, _ in slas),
                 'INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, '
                 '`excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, '
                 '`skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES'] + rows
        update(os.path.join(folder, 'dbc', tag + '_skilllineability.sql'), '\n'.join(lines))

        for table, (columns, id_column) in WORLD_TABLES.items():
            mine = [v for v in world[table] if int(v.split(',')[0]) in sids]
            ids_sql = sorted({int(v.split(',')[0]) for v in mine})
            text = ['-- %s racials of Aetheria\'s Kyrian/Venthyr package (%s, from its server migrations; tools/races/'
                    'aetheria_racials.py)' % (key, VERSION),
                    'DELETE FROM `%s` WHERE `%s` IN (%s);' % (table, id_column, ', '.join(map(str, ids_sql))),
                    'INSERT INTO `%s` (%s) VALUES' % (table, columns),
                    ',\n'.join('(%s)' % v for v in mine) + ';']
            nrm.write(os.path.join(folder, 'sql', 'db-world', 'base', '%s_%s.sql' % (tag, table)), '\n'.join(text))

        path = os.path.join(folder, 'readme.md')
        text = open(path, encoding='utf-8').read().split('\n' + README)[0].rstrip()
        lines = ['', '', README,
                 '- Active, in place of CoA\'s: learned with the racial skill line; from Aetheria\'s Kyrian/Venthyr package '
                 '(%s, Aetheria race %d) with its spell ids' % (VERSION, aetheria_race),
                 '- Blocks at the end of `%s_spell.sql` and `_skilllineability.sql`; `sql/db-world/base/%s_spell_script_names.sql` '
                 'and `_spell_bonus_data.sql`; C++ scripts in `src/`' % (tag, tag)]
        for s in learned:
            lines.append('    - %s: %s' % (spells[s][136], spells[s][170].replace('\r', '').replace('\n', ' ')))
        lines += ['- ' + n for n in notes]
        nrm.write(path, text + '\n'.join(lines))
        print('%s %s: %d spells, %d learned' % (fnum, key, len(sids), len(learned)))

    config.insert(0, '-- Aetheria racials (Kyrian/Venthyr package %s): spells at Aetheria\'s ids 111100-111113 and '
                     '111200-111212 (fixed: the C++ scripts use them), SkillLineAbility from %d' % (VERSION, SLA_BASE))
    config.append(('SET ' + BAT_CREATURE[1]).ljust(63) + '= %8d; -- %s, Vampire Bat Form\'s creature (any creature '
                  'with a bat model)' % (BAT_CREATURE[2], BAT_CREATURE[3]))
    update(os.path.join(modpaks, 'config.sql'), '\n'.join(config))


if __name__ == '__main__':
    main()

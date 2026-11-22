#!/usr/bin/env python3
"""Remove the skin colours of coa_races.MISFIT_SKINS from built race modpaks' CharSections SQL.

  python -I drop_misfit_skins.py MODPAK_DIR...

In each modpak's dbc/*charsections*.sql (the base rows and the death knight ones together): every skin colour whose
Skin row's texture_1 is a misfit (or a misfit's _dk tint) loses its Skin, Face and Underwear rows (the sections keyed
by skin colour), and the remaining colours are renumbered 0, 1, 2... per gender in their old order, so character
creation's skin colour list has no gaps. Hair and facial hair rows are keyed by hair colour and stay as they are.
coa_race_modpaks.py and coa199_race_modpaks.py leave the same colours out when they regenerate a modpak.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coa_races  # noqa: E402

ROW = re.compile(r"^\(@CharSectionsID := @CharSectionsID \+1, (@\w+), +(@\w+), +(@\w+), +'((?:[^'\\]|\\.)*)', "
                 r"'(?:[^'\\]|\\.)*', '(?:[^'\\]|\\.)*', \d+, \d+, (\d+)\)[,;]$")
BY_SKIN = {'@Skin', '@Face', '@Underwear'}


def fix(modpak):
    files = sorted(glob.glob(os.path.join(modpak, 'dbc', '*charsections*.sql')))
    texts = {f: open(f, encoding='utf-8').read().split('\n') for f in files}
    colours, dropped = {}, {}
    for lines in texts.values():
        for line in lines:
            m = ROW.match(line)
            if m and m.group(3) == '@Skin':
                gender, tex, colour = m.group(2), m.group(4).replace('\\\\', '\\'), int(m.group(5))
                colours.setdefault(gender, set()).add(colour)
                if coa_races.misfit(tex):
                    dropped.setdefault(gender, set()).add(colour)
    if not dropped:
        print('%s: no misfit skins' % os.path.basename(modpak))
        return
    remap = {g: {c: i for i, c in enumerate(sorted(cs - dropped.get(g, set())))} for g, cs in colours.items()}
    for f, lines in texts.items():
        out, removed = [], 0
        for line in lines:
            m = ROW.match(line)
            if m and m.group(3) in BY_SKIN:
                gender, colour = m.group(2), int(m.group(5))
                if colour in dropped.get(gender, ()):
                    removed += 1
                    continue
                line = line[:m.start(5)] + str(remap[gender][colour]) + line[m.end(5):]
            out.append(line)
        if not removed:
            continue
        for i, line in enumerate(out):   # the last row of an INSERT ends it
            if ROW.match(line):
                last = i + 1 >= len(out) or not ROW.match(out[i + 1])
                out[i] = line[:-1] + (';' if last else ',')
        rows = sum(1 for line in out if ROW.match(line))
        text = re.sub(r'^-- charsections: \d+ inserts', '-- charsections: %d inserts' % rows, '\n'.join(out), count=1,
                      flags=re.M)
        open(f, 'w', encoding='utf-8', newline='\n').write(text)
        print('%s: %d rows removed, colours %s dropped' % (os.path.relpath(f, os.path.dirname(modpak)), removed,
                                                           {g: sorted(c) for g, c in dropped.items()}))


if __name__ == '__main__':
    for modpak in sys.argv[1:]:
        fix(modpak)

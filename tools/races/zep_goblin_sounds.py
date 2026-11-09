#!/usr/bin/env python3
"""Download the sound files F-013's Cataclysm SoundEntries rows play that neither WHE-common nor the client has.

zep_goblin_fixes/dbc/[F-013]_cata_soundentries.sql (cata406_dbc_port.py) names Cataclysm's files, as .ogg (the goblin
NPCs' greetings, farewells and pissed lines among them). Zeppelin's client doesn't ship most of them; retail still has
them under the same paths, so each missing file is looked up in the community listfile and downloaded from wago.tools
by FileDataID into WHE-common at its client path.

usage: zep_goblin_sounds.py [--common PATH] [--client DATA] [--listfile CSV] [--build VERSION]
Resumable: files already in WHE-common are skipped."""
import argparse, glob, os, re, sys, time, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'checks'))
from check_f013_assets import Archive  # noqa: E402

B = chr(92)
SQL = os.path.join(HERE, 'zep_goblin_fixes', 'dbc', '[F-013]_cata_soundentries.sql')


def wanted():
    """Client paths of every file the rows play."""
    text = open(SQL, encoding='utf-8').read()
    out = []
    for block in re.findall(r"INSERT INTO `soundentries` SET(.*?);", text, re.S):
        row = dict(re.findall(r"`(\w+)` = '((?:[^'\\]|\\.)*)'", block))
        base = row.get('base_dir', '').replace(B * 2, B).rstrip(B)
        for k, v in sorted(row.items()):
            if k.startswith('file_') and v:
                out.append(base + B + v)
    return sorted(set(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--common', default='D:/GitHub/WHE-common/patch-A.MPQ')
    ap.add_argument('--client', default='C:/Users/Medviten/Desktop/WowSquished-256-bit/Data')
    ap.add_argument('--listfile', default='D:/wow-scratch/retail-vo/community-listfile.csv')
    ap.add_argument('--build', default='12.1.5.70448')
    a = ap.parse_args()
    archives = [Archive(p) for p in glob.glob(os.path.join(a.client, '*.[mM][pP][qQ]'))
                + glob.glob(os.path.join(a.client, 'enUS', '*.[mM][pP][qQ]')) if os.path.isfile(p)]
    paths = wanted()
    ids = {}
    want = {p.lower().replace(B, '/') for p in paths}
    with open(a.listfile, encoding='utf-8', errors='replace') as f:
        for line in f:
            fid, _, name = line.strip().partition(';')
            if name.lower() in want:
                ids[name.lower()] = int(fid)
    got = skipped = 0
    missing = []
    for path in paths:
        target = os.path.join(a.common, *path.split(B))
        if os.path.exists(target) or any(x.has(path) for x in archives):
            skipped += 1
            continue
        fid = ids.get(path.lower().replace(B, '/'))
        if not fid:
            missing.append(path)
            continue
        os.makedirs(os.path.dirname(target), exist_ok=True)
        for attempt in range(6):
            try:
                req = urllib.request.Request('https://wago.tools/api/casc/%d?download&version=%s' % (fid, a.build),
                                             headers={'User-Agent': 'whe-sound-import'})
                body = urllib.request.urlopen(req, timeout=60).read()
                if body:
                    open(target + '.part', 'wb').write(body)
                    os.replace(target + '.part', target)
                    got += 1
                break
            except urllib.error.HTTPError as e:
                if e.code == 400:
                    missing.append(path + ' (unavailable)')
                    break
                time.sleep(5 * (attempt + 1))
            except Exception:
                time.sleep(5 * (attempt + 1))
        time.sleep(0.3)
    print('%d files: %d present, %d downloaded, %d missing' % (len(paths), skipped, got, len(missing)))
    for path in missing:
        print('  missing', path)


if __name__ == '__main__':
    main()

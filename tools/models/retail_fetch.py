#!/usr/bin/env python3
"""Download retail model files from wago.tools by FileDataID, ready for Kalibro's wotlkconv.

For each model: the .m2 and every file its chunks name (SFID skins, AFID animations, SKID skeleton, BFID bones, TXID
textures, and the skeleton's own SKPD/AFID/BFID), plus any extra file ids given (texture variations the model doesn't
name itself, which come from CreatureDisplayInfo). Files are saved under their community listfile paths (looked up on
wago.tools by folder), or <folder>/<fdid>.<ext> when unnamed, and OUT/listfile.csv ("fdid;path", the format of
wotlkconv's -l) lists them all. Already downloaded files are kept.

usage: retail_fetch.py OUT_DIR [TERM:]MODEL_FDID[,EXTRA_FDID...] ...
       TERM: a wago.tools file search that finds the model's name (its folder name, e.g. druidbearharanir); without
       it the files go to unnamed/<model fdid>/"""
import json
import os
import struct
import sys
import time
import urllib.parse
import urllib.request

API = 'https://wago.tools/api'
HEADERS = {'User-Agent': 'whe-tools'}
EXT = {b'MD21': 'm2', b'SKIN': 'skin', b'SKL1': 'skel', b'BLP2': 'blp'}


def get(url):
    for attempt in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=180).read()
        except Exception:
            if attempt == 3:
                raise
            time.sleep(3 * (attempt + 1))


def chunks(data):
    out, at = {}, 0
    while at + 8 <= len(data):
        tag, size = data[at:at + 4], struct.unpack_from('<I', data, at + 4)[0]
        out.setdefault(tag, data[at + 8:at + 8 + size])
        at += 8 + size
    return out


def named(data):
    """The file ids a chunked file (.m2 or .skel) names."""
    c, ids = chunks(data), []
    for tag in (b'SFID', b'TXID', b'BFID', b'SKID', b'SKPD'):
        if tag in c:
            body = c[tag]
            if tag == b'SKPD':   # 8 unknown bytes, then the parent skeleton
                ids.append(struct.unpack_from('<I', body, 8)[0])
            else:
                ids += list(struct.unpack('<%dI' % (len(body) // 4), body))
    if b'AFID' in c:
        body = c[b'AFID']
        ids += [struct.unpack_from('<I', body, i + 4)[0] for i in range(0, len(body), 8)]
    return [i for i in ids if i]


class Names:
    """fdid -> listfile path, from wago.tools' file search on the model's folder."""

    def __init__(self):
        self.known, self.searched = {}, set()

    def search(self, term):
        if term in self.searched:
            return
        self.searched.add(term)
        found = json.loads(get('%s/files?search=%s' % (API, urllib.parse.quote(term))) or b'{}')
        if isinstance(found, dict):
            self.known.update({int(k): v for k, v in found.items()})

    def path(self, fdid, folder, ext):
        return self.known.get(fdid) or '%s/%d.%s' % (folder, fdid, ext)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out = sys.argv[1]
    names, listing = Names(), {}
    lf = os.path.join(out, 'listfile.csv')
    if os.path.exists(lf):
        for line in open(lf, encoding='utf-8'):
            fdid, _, path = line.strip().partition(';')
            listing[int(fdid)] = path
    for arg in sys.argv[2:]:
        term, _, ids = arg.rpartition(':')
        if term:
            names.search(term)
        model, *extra = [int(x) for x in ids.split(',')]
        queue, seen, folder = [model] + extra, set(), None
        while queue:
            fdid = queue.pop(0)
            if fdid in seen:
                continue
            seen.add(fdid)
            path = listing.get(fdid)
            data = open(os.path.join(out, path), 'rb').read() if path and os.path.exists(os.path.join(out, path)) else None
            if data is None:
                data = get('%s/casc/%d?download' % (API, fdid))
                ext = EXT.get(data[:4], 'anim' if fdid != model else 'm2')
                if folder is None:   # the model: name it, then search its folder for the rest
                    path = names.known.get(fdid)
                    if path:
                        folder = path.rsplit('/', 1)[0]
                        names.search(folder.rsplit('/', 1)[-1])
                    else:
                        folder = 'unnamed/%d' % fdid
                path = names.path(fdid, folder, ext)
                os.makedirs(os.path.dirname(os.path.join(out, path)), exist_ok=True)
                with open(os.path.join(out, path), 'wb') as fh:
                    fh.write(data)
                listing[fdid] = path
                print('%9d %s' % (fdid, path), flush=True)
                time.sleep(0.3)
            elif folder is None:
                folder = path.rsplit('/', 1)[0]
            if data[:4] in (b'MD21', b'SKL1'):
                queue += named(data)
    with open(lf, 'w', encoding='utf-8', newline='\n') as fh:
        fh.writelines('%d;%s\n' % (k, v) for k, v in sorted(listing.items()))


if __name__ == '__main__':
    main()

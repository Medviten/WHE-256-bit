#!/usr/bin/env python3
"""Download the retail textures the CoA 1.9.9 races' models name but neither the release nor a CoA client has, into
the release's unpacked Work folder, where coa199_race_prep.py then finds them.

The release ships the AllRaces v12 races' player models without their textures (it expects CoA's own client, which
has them from that pack). Most are retail creature textures under their retail names, or named after their retail
FileDataID (nerubianevolved_5306026.blp); they download from wago.tools by FileDataID. What retail does not have:
- the Wretched (crackelf2_*) and male Titan (titanmale2_*) textures: CoA's own, so those two races can't be made
- Harpy's tinted scroll textures (haryp2felscroll_orange/_red/_white): the untinted retail one stands in
- the female Stormforged's eye texture (ironvrykulfemale_eyes.blp): left out

usage: python -I coa199_retail_textures.py <release client Work folder>"""
import os
import sys
import time
import urllib.request

URL = 'https://wago.tools/api/casc/%d?download'
# client path -> retail FileDataID (from the community listfile: same name, the model's folder where there are several)
FDIDS = {
    'Creature\\Lich2\\lich2_bronze.blp': 3482567,
    'Creature\\Lich2\\lich2_silver.blp': 3482592,
    'Creature\\MoargEngineer\\Moarg.blp': 124914,
    'Creature\\MoargEngineer\\MoargArmor.blp': 124921,
    'Creature\\MoargMinion2\\MoargMinion2.blp': 124924,
    'Creature\\MoargMinion2\\MoargMinion3.blp': 124925,
    'Creature\\MoargMinion2\\MoargMinion4.blp': 124926,
    'Creature\\MoargMinion2\\MoargMinion5.blp': 124927,
    'Creature\\NerubianEvolvedBoss\\nerubianevolvedboss_armor.blp': 5547581,
    'Creature\\NerubianEvolvedBoss\\nerubianevolvedboss_body.blp': 5547582,
    'Creature\\NerubianPriest2\\nerubianpriest2_armor_red.blp': 5330379,
    'Creature\\NerubianPriest2\\nerubianpriest2_dark.blp': 5330375,
    'Creature\\NerubianPriest2\\nerubianpriest2_green.blp': 5330376,
    'Creature\\StormforgedVrykul\\ArmorReflect4.blp': 1290245,
    'Creature\\StormforgedVrykul\\Helm_Plate_RaidWarrior_D_01_Ponytail.blp': 1290247,
    'Creature\\StormforgedVrykul\\StomrforgedVrykulReflect.blp': 1290246,
    'Creature\\StormforgedVrykul\\stormforgedvrykularmor_dark.blp': 1292381,
    'Creature\\StormforgedVrykul\\stormforgedvrykularmor_gold.blp': 1292388,
    'Creature\\StormforgedVrykul\\stormforgedvrykularmor_silver.blp': 1292395,
    'Creature\\StormforgedVrykul\\stormforgedvrykulbody_dark.blp': 1292403,
    'Creature\\StormforgedVrykul\\stormforgedvrykulbody_gold.blp': 1292407,
    'Creature\\StormforgedVrykul\\stormforgedvrykulbody_silver.blp': 1292411,
    'Creature\\StormforgedVrykul\\stormforgedvrykulhair_dark.blp': 1292414,
    'Creature\\TrollLich\\trolllich_blue.blp': 1695691,
    'Creature\\TrollLich\\trolllich_green.blp': 1695692,
    'Creature\\TrollLich\\trolllich_red.blp': 1695693,
    'Creature\\TrollLich\\zandalarigold.blp': 1695685,
    'Creature\\DeepJinyuMelee\\armorreflect4.blp': 2617511,
    'Creature\\DeepJinyuMelee\\deepjinyumelee_3_2617512.blp': 2617512,
    'Creature\\Harpy2Fel\\armorreflect4.blp': 1568962,
    'Creature\\Harpy2Fel\\haryp2felscroll.blp': 1568963,
    'Creature\\Harpy2Fel\\haryp2felscroll_orange.blp': 1568963,
    'Creature\\Harpy2Fel\\haryp2felscroll_red.blp': 1568963,
    'Creature\\Harpy2Fel\\haryp2felscroll_white.blp': 1568963,
    'Creature\\IronVrykulFemale2\\armorreflect4.blp': 124573,
    'Creature\\NerubianEvolved\\dragonarmorspec.blp': 5306025,
    'Creature\\NerubianEvolved\\nerubianevolved_5306026.blp': 5306026,
    'Creature\\NerubianEvolved\\nerubianevolved_5306027.blp': 5306027,
    'Creature\\NerubianEvolved\\nerubianevolved_5559087.blp': 5559087,
    'Creature\\NerubianEvolved\\nerubianevolved_5559089.blp': 5559089,
    'Creature\\NerubianEvolvedBoss\\dragonarmorspec.blp': 5547584,
    'Creature\\NerubianEvolvedBoss\\nerubianevolvedboss_5547580.blp': 5547580,
    'Creature\\NerubianEvolvedBoss\\nerubianevolvedboss_5547583.blp': 5547583,
    'Creature\\NerubianEvolvedBoss\\nerubianevolvedboss_5547585.blp': 5547585,
}


def existing_dir(root, parts):
    """The real folder for a client path's folders (case-insensitive), created where missing."""
    cur = root
    for part in parts:
        hit = next((e for e in os.listdir(cur) if e.lower() == part.lower()), None) if os.path.isdir(cur) else None
        cur = os.path.join(cur, hit or part)
    os.makedirs(cur, exist_ok=True)
    return cur


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    work = sys.argv[1]
    cache = {}
    for path, fdid in FDIDS.items():
        parts = path.split('\\')
        folder = existing_dir(work, parts[:-1])
        if any(e.lower() == parts[-1].lower() for e in os.listdir(folder)):
            continue
        if fdid not in cache:
            req = urllib.request.Request(URL % fdid, headers={'User-Agent': 'whe-tools'})
            cache[fdid] = urllib.request.urlopen(req, timeout=120).read()
            time.sleep(0.5)
        if cache[fdid][:4] != b'BLP2':
            raise SystemExit('%s (%d): not a BLP2 file' % (path, fdid))
        with open(os.path.join(folder, parts[-1]), 'wb') as fh:
            fh.write(cache[fdid])
        print('%s <- %d' % (path, fdid))


if __name__ == '__main__':
    main()

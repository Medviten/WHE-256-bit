"""Second race-mask word for the variables: config.sql and every modpak variables.sql (WHE-256-bit).

- After every race mask definition `SET @XMask = 1 << (@X - 1);` add
  `SET @XMask_2 = IF(@X BETWEEN 65 AND 128, 1 << (@X - 65), 0);`
- After every assignment to a faction-wide mask (AGGREGATES) add the same assignment on the _2 variables.
Idempotent: lines that already have a _2 twin are left alone."""
import os, re, sys

MODPAKS, MODE = sys.argv[1], sys.argv[2]
AGGREGATES = ["VanillaAllianceMask", "VanillaHordeMask", "BaseAllianceMask", "BaseHordeMask", "AllianceMask", "HordeMask",
              "UndercityMask", "BarrensBros", "PlayableRaceMask", "GunHunters", "CrossbowHunters", "BowHunters",
              "ExtendedAllianceMask", "ExtendedHordeMask"]
MASK_DEF = re.compile(r"^(SET @(?!(?:Warrior|Paladin|Hunter|Rogue|Priest|DeathKnight|Shaman|Mage|Warlock|Monk|Druid|DemonHunter|Evoker)Mask)"
                      r"(\w+)Mask)(\s*)=\s*1\s*<<\s*\(@(\w+)\s*-\s*1\);(.*)$")
AGG_DEF = re.compile(r"^(SET @(%s))(\s*)=\s*(.*?);(.*)$" % "|".join(AGGREGATES))
VAR = re.compile(r"@(\w+)\b")


def maskvars(files):
    names = set(AGGREGATES)
    for f in files:
        for line in open(f, encoding="utf-8"):
            m = MASK_DEF.match(line)
            if m and not m.group(2).endswith("Helmet"):
                names.add(m.group(2) + "Mask")
    return names


def mirror(expr, names):
    return VAR.sub(lambda m: "@" + m.group(1) + "_2" if m.group(1) in names else m.group(0), expr)


def process(path, names):
    lines = open(path, encoding="utf-8").read().split("\n")
    existing = {m.group(1) for l in lines for m in [re.match(r"^SET @(\w+_2)\s*=", l)] if m}
    out, added = [], 0
    for line in lines:
        out.append(line)
        m = MASK_DEF.match(line)
        if m and not m.group(2).endswith("Helmet") and f"{m.group(2)}Mask_2" not in existing:
            race = m.group(4)
            out.append(f"{m.group(1)}_2".ljust(len(m.group(1)) + len(m.group(3)) + 0) +
                       f"= IF(@{race} BETWEEN 65 AND 128, 1 << (@{race} - 65), 0); -- races 65-128")
            added += 1
            continue
        a = AGG_DEF.match(line)
        if a and f"{a.group(2)}_2" not in existing:
            expr = a.group(4)
            out.append(f"{a.group(1)}_2".ljust(len(a.group(1)) + len(a.group(3))) + f"= {mirror(expr, names)}; -- races 65-128")
            added += 1
    if added and MODE == "apply":
        open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    return added, [l for l in out if l.endswith("-- races 65-128")]


files = [os.path.join(MODPAKS, "config.sql")] + [os.path.join(MODPAKS, d, "variables.sql") for d in sorted(os.listdir(MODPAKS))
                                                 if os.path.exists(os.path.join(MODPAKS, d, "variables.sql"))]
names = maskvars(files)
for f in files:
    n, sample = process(f, names)
    if n:
        print(f"{os.path.relpath(f, MODPAKS)}: +{n}")
        if MODE == "report":
            for s in sample[:3]:
                print("    ", s)

"""Replay TrinityCore world-update SQL files (INSERT / DELETE / UPDATE only) into an in-memory sqlite database.

  db = load(["a.sql", "b.sql"])           -> sqlite3.Connection, one table per table the files insert into
  rows(db, "creature")                    -> [dict], column names as in the files

Tables are created from the first INSERT's column list (untyped), so a DELETE or UPDATE on a table nothing has
inserted into yet is skipped. MySQL string escapes (\\' \\\\ \\n \\r \\t \\") are turned into plain sqlite strings.
Numbers stay numbers (sqlite keeps the literal's type). Other statements (SET, CREATE, ...) are ignored.
Used by mop_wandering_isle_port.py on the TrinityCore MoP Classic port's generated Wandering Isle updates.
"""
import re, sqlite3

ESCAPES = {"'": "'", "\\": "\\", "n": "\n", "r": "\r", "t": "\t", '"': '"', "0": "\0", "Z": "\x1a"}


def statements(text):
    """Split SQL text into statements, converting MySQL string literals to sqlite ones; comments dropped. A bare
    DEFAULT value becomes 0 (the generators use it for the columns they leave at the table default, all numeric)."""
    out, cur, plain, i, n = [], [], [], 0, len(text)

    def flush():
        if plain:
            cur.append(re.sub(r"\bDEFAULT\b", "0", "".join(plain)))
            plain.clear()

    while i < n:
        c = text[i]
        if c == "'":
            flush()
            j, buf = i + 1, []
            while True:
                d = text[j]
                if d == "\\":
                    buf.append(ESCAPES.get(text[j + 1], text[j + 1]))
                    j += 2
                elif d == "'":
                    if j + 1 < n and text[j + 1] == "'":
                        buf.append("'")
                        j += 2
                    else:
                        break
                else:
                    buf.append(d)
                    j += 1
            cur.append("'" + "".join(buf).replace("'", "''") + "'")
            i = j + 1
        elif c == "-" and text.startswith("--", i):
            i = text.find("\n", i)
            i = n if i < 0 else i
        elif c == "/" and text.startswith("/*", i):
            i = text.index("*/", i) + 2
        elif c == ";":
            flush()
            s = "".join(cur).strip()
            if s:
                out.append(s)
            cur, i = [], i + 1
        else:
            plain.append(c)
            i += 1
    flush()
    s = "".join(cur).strip()
    if s:
        out.append(s)
    return out


def upsert(db, table, insert, updates):
    """INSERT ... ON DUPLICATE KEY UPDATE, with the first column as the key (shortcut: true of every table the MoP
    updates use it on, creature_addon and quest_template_addon; give it the real key if another table needs it)."""
    db.execute("DROP TABLE IF EXISTS _dup")
    cols = re.match(r"INSERT INTO\s+`?\w+`?\s*\(([^)]*)\)", insert, re.I).group(1)
    names = [c.strip(" `") for c in cols.split(",")]
    db.execute("CREATE TABLE _dup (%s)" % cols)
    db.execute(re.sub(r"INSERT INTO\s+`?\w+`?", "INSERT INTO _dup", insert, count=1, flags=re.I))
    sets = []
    for part in re.split(r",\s*(?=`)", updates.strip()):
        col, val = [x.strip() for x in part.split("=", 1)]
        v = re.match(r"VALUES\(\s*`?(\w+)`?\s*\)", val, re.I)
        sets.append((col.strip("`"), ("d.`%s`" % v.group(1)) if v else val))
    key = names[0]
    for row in db.execute("SELECT rowid FROM _dup").fetchall():
        d = "(SELECT * FROM _dup WHERE rowid = %d)" % row[0]
        hit = db.execute("SELECT COUNT(*) FROM `%s` WHERE `%s` = (SELECT `%s` FROM _dup WHERE rowid = ?)"
                         % (table, key, key), row).fetchone()[0]
        if hit:
            db.execute("UPDATE `%s` SET %s WHERE `%s` = (SELECT `%s` FROM _dup WHERE rowid = %d)" % (
                table, ", ".join("`%s` = (SELECT %s FROM %s d)" % (c, v, d) for c, v in sets), key, key, row[0]))
        else:
            db.execute("INSERT INTO `%s` (%s) SELECT %s FROM _dup WHERE rowid = %d" % (
                table, cols, cols, row[0]))
    db.execute("DROP TABLE _dup")


def load(paths):
    db = sqlite3.connect(":memory:")
    tables = set()
    for path in paths:
        for s in statements(open(path, encoding="utf8").read()):
            m = re.match(r"(INSERT INTO|DELETE FROM|UPDATE)\s+`?(\w+)`?", s, re.I)
            if not m:
                continue
            kind, table = m.group(1).upper(), m.group(2)
            if kind == "INSERT INTO" and table not in tables:
                cols = re.match(r"INSERT INTO\s+`?\w+`?\s*\(([^)]*)\)", s, re.I).group(1)
                db.execute("CREATE TABLE `%s` (%s)" % (table, cols))
                tables.add(table)
            if table not in tables:
                continue
            dup = re.search(r"\s+ON DUPLICATE KEY UPDATE\s+(.*)$", s, re.I | re.S)
            if dup:
                upsert(db, table, s[:dup.start()], dup.group(1))
            else:
                db.execute(s)
    db.row_factory = sqlite3.Row
    return db


def rows(db, table, where="1"):
    try:
        return [dict(r) for r in db.execute("SELECT * FROM `%s` WHERE %s" % (table, where))]
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            return []
        raise


if __name__ == "__main__":
    # self-check: escapes and comments survive the conversion
    s = statements("-- c\nINSERT INTO `t` (`a`,`b`,`c`) VALUES (1,'it\\'s a \\\\ \"x\"; DEFAULT',DEFAULT),(2,'',3);\n"
                   "DELETE FROM `t` WHERE `a`=2;")
    assert len(s) == 2 and "it''s a \\ \"x\"; DEFAULT" in s[0], s
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE t (a, b, c)")
    for x in s:
        db.execute(x)
    assert db.execute("SELECT * FROM t").fetchall() == [(1, "it's a \\ \"x\"; DEFAULT", 0)]
    upsert(db, "t", "INSERT INTO `t` (`a`,`c`) VALUES (1,7),(5,8)", "`c` = VALUES(`c`)")
    assert db.execute("SELECT a, c FROM t ORDER BY a").fetchall() == [(1, 7), (5, 8)]
    print("ok")

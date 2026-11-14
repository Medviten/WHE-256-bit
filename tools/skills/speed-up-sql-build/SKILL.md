---
name: speed-up-sql-build
description: Find and remove the slow parts of a build or deploy that applies many SQL files to MySQL/MariaDB (DBC/DB2 editors, mod packs, migration runners, seed scripts). Use when a SQL-heavy build "takes forever", got slower as content was added, or the user asks why a deploy is slow and how to speed it up.
---

# Speed up a SQL-heavy build

A build that applies thousands of small SQL files often gets slow in ways no single file explains. Two
patterns account for most of it:

1. **A shared preamble repeated per file.** Each file gets the same block of statements (variables, settings)
   sent ahead of it. The cost is files x preamble size, and both grow as content is added, so each addition
   slows down all the others.
2. **Huge multi-row INSERTs that number their own rows** (`(@id := @id + 1, ...)`). MySQL 8 slows down far
   faster than the row count grows on these: in one case 88,000 rows took 238 s as one statement and 2.3 s
   as 1000-row statements.

Real result from applying both fixes: a deploy of 114 content packs (3,230 SQL files) went from about 95 minutes
to 12, with byte-identical output.

## Method

### 1. Measure before changing anything

Don't guess. Put a timestamp on every log line of one real run, without touching the build:

```bash
./build.sh 2>&1 | while IFS= read -r l; do printf '%(%H:%M:%S)T %s\n' -1 "$l"; done > build.log
```

From that log, get:
- **time per stage**: the gap between the stage headers;
- **time per file**: if the build prints each file's name before applying it, the gap to the next name is that
  file's cost. Sort descending; a handful of files often dominate;
- **how cost scales**: run once with a subset of the content (the build's own manifest or config, after
  backing it up). If dropping 70% of the content removes 90% of the time, the cost is superlinear. Look for
  something multiplied by the content size, not added once.

### 2. Shared preamble per file: send only what each file uses

Typical shape: a "variables snapshot" (`SET @Name = 'value';`, one per line, values already resolved) prepended
to every file, each file in its own connection. Check how many lines that snapshot has, and how many files get it.

If the snapshot lines are plain literals (no expressions that depend on each other), a file can only be affected
by the variables it names. Filter per file, case-insensitively (MySQL variable names ignore case):

```bash
{ grep -o '@[A-Za-z0-9_$]*' -- "$file" || true; } | tr 'A-Z' 'a-z' | sort -u > used.txt
awk 'NR == FNR { used[$0] = 1; next }
     match($0, /^SET @[A-Za-z0-9_$]+/) { if (tolower(substr($0, 5, RLENGTH - 4)) in used) print; next }
     { print }' used.txt snapshot.sql > file-snapshot.sql
```

Before relying on it, check for quoted variable names (``@`name` ``, `@'name'`), which the grep doesn't see:
`grep -rE "@[\`'\"]" --include=*.sql .` and read each hit (usually it's an `@` inside string data).

Keep one connection per file. Merging all files into one connection was measured too and saved only about
8% (11.5 vs 12.6 min). It gave up per-file error reporting, and variables set in one file then leak into the
next. Measure it before proposing it.

### 3. Huge self-numbering INSERTs: split at apply time

Find them: count rows per `INSERT ... VALUES` statement that use `:=`; anything in the tens of thousands is
suspect. Confirm on a scratch copy of the table (never the real build database): time the file as-is against
the same rows split into 1000-row statements.

Splitting keeps the rows in the same order, so `@id := @id + 1` numbering gives the same ids. Do it in the
build, as a filter on each file, rather than editing the SQL files and every generator that writes them. That
way it also covers files added later. This version handles the common generated layout: a header line ending
in `VALUES`, one row per line. It leaves statements with anything after the last row (e.g.
`ON DUPLICATE KEY UPDATE`) whole:

```bash
split_long_inserts() {
    awk -v max="${MAX_INSERT_ROWS:-1000}" '
        function flush(   i, n, rows, line) {
            if (buf[k] !~ /\);[[:space:]]*$/ || toupper(buf[k]) ~ /ON DUPLICATE KEY/) {
                for (i = 1; i <= k; i++) print buf[i]; k = 0; return
            }
            rows = 0
            for (i = 2; i <= k; i++) if (buf[i] ~ /^[[:space:]]*\(/) rows++
            n = 0; print buf[1]
            for (i = 2; i <= k; i++) {
                line = buf[i]
                if (line ~ /^[[:space:]]*\(/ && ++n % max == 0 && n < rows && line ~ /\),[[:space:]]*$/) {
                    sub(/,[[:space:]]*$/, ";", line); print line; print buf[1]; continue
                }
                print line
            }
            k = 0
        }
        k > 0 { buf[++k] = $0; if ($0 ~ /;[[:space:]]*$/) flush(); next }
        /^INSERT INTO .*VALUES[[:space:]]*$/ { k = 1; buf[1] = $0; next }
        { print }
        END { for (i = 1; i <= k; i++) print buf[i] }'
}
# in the per-file apply step:  cat "$file" | split_long_inserts >> "$batch"
```

Test it on a small hand-made input before using it: a split mid-list, a comment line inside the VALUES list, a
statement with `ON DUPLICATE KEY UPDATE`, and a following non-INSERT statement.

### 4. Prove the output didn't change

Speed changes to a build must not change what it builds. Before the change, copy the build's outputs aside
(exported files, or a dump of the result tables); after it, byte-compare:

```bash
for f in before/*; do cmp -s "$f" "after/$(basename "$f")" || echo "DIFF $f"; done
```

Report the comparison with the timings. Where something can't be compared (e.g. a database that is reset every
run), say so instead of implying it was checked.

## Rules

- **The user's data:** run experiments on scratch tables or scratch databases, never in the live build database.
  Generate test SQL into files and upload them, instead of building it inside nested shell quoting (a broken
  `sed` there silently ran a test against the real table).
- **Live configs:** back up the live manifest or config before trimming it for a timing run, and restore it
  afterwards. Tell the user when content is temporarily switched off, and what that breaks while it's off.
- **Report numbers per stage**, before and after, and stop when the remaining cost is fixed overhead
  (connection setup, database resets) rather than a pattern that grows with content.

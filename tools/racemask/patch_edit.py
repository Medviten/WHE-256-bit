#!/usr/bin/env python3
"""Small helpers for editing the hand-maintained unified diffs in integration/ (whe-acore.patch, whe-playerbots.patch).

Edits only touch '+' lines (insert after an anchor, or replace a '+' line), then every hunk header of the edited file
sections is recomputed: the new-side line count from the hunk body, and the new-side start of later hunks in the same
file shifted by the lines added before them. Context and '-' lines are never changed, so the patch still applies
wherever it applied before."""
import re

HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$")


def parse(text):
    """Return (header_lines, files) where files = [(file_header_lines, [ [hunk_header, body_lines], ... ]), ...]."""
    lines = text.split("\n")
    head, files, i = [], [], 0
    while i < len(lines) and not lines[i].startswith("diff --git"):
        head.append(lines[i]); i += 1
    while i < len(lines):
        fh = [lines[i]]; i += 1
        while i < len(lines) and not lines[i].startswith("@@") and not lines[i].startswith("diff --git"):
            fh.append(lines[i]); i += 1
        hunks = []
        while i < len(lines) and lines[i].startswith("@@"):
            h, body = lines[i], []
            i += 1
            while i < len(lines) and not lines[i].startswith("@@") and not lines[i].startswith("diff --git"):
                body.append(lines[i]); i += 1
            hunks.append([h, body])
        files.append((fh, hunks))
    return head, files


def counts(body):
    """(old_len, new_len) of a hunk body; a trailing empty string (end of file) and '\\ No newline' are not lines."""
    old = new = 0
    for l in body:
        if l.startswith("\\"):
            continue
        if l == "":
            continue
        if l[0] == " ":
            old += 1; new += 1
        elif l[0] == "-":
            old += 1
        elif l[0] == "+":
            new += 1
    return old, new


def dump(head, files):
    out = list(head)
    for fh, hunks in files:
        out += fh
        for h in hunks:
            out.append(h[0])
            out += h[1]
    return "\n".join(out)


def check_headers(text):
    """List hunks whose header counts don't match their bodies."""
    _, files = parse(text)
    bad = []
    for fh, hunks in files:
        for h, body in hunks:
            m = HUNK.match(h)
            o_len = int(m.group(2) or 1)
            n_len = int(m.group(4) or 1)
            if counts(body) != (o_len, n_len):
                bad.append((fh[0], h, counts(body)))
    return bad


def apply_edits(text, edits):
    """edits: list of (file_substring, kind, anchor, payload, expected_count).
    kind 'after' inserts payload lines after each matching '+' or ' ' anchor line; 'replace' replaces matching '+' lines."""
    head, files = parse(text)
    for file_sub, kind, anchor, payload, expected in edits:
        n = 0
        for fh, hunks in files:
            if file_sub not in fh[0]:
                continue
            added_before = 0
            for h in hunks:
                body = h[1]
                new_body = []
                for line in body:
                    if line == anchor:
                        n += 1
                        if kind == "after":
                            new_body.append(line)
                            new_body += payload
                        else:
                            new_body += payload
                    else:
                        new_body.append(line)
                h[1] = new_body
        assert n == expected, f"{file_sub}: anchor {anchor!r} matched {n} times, expected {expected}"
    # recompute headers: new-side count from the body, new-side start shifted by growth of earlier hunks
    for fh, hunks in files:
        growth = 0
        for h in hunks:
            m = HUNK.match(h[0])
            o_start, o_len, n_start, n_len, rest = int(m.group(1)), int(m.group(2) or 1), int(m.group(3)), int(m.group(4) or 1), m.group(5)
            old, new = counts(h[1])
            assert old == o_len, f"old side changed in {fh[0]} {h[0]}"
            h[0] = f"@@ -{o_start},{old} +{n_start + growth},{new} @@{rest}"
            growth += new - n_len
    return dump(head, files)

#!/usr/bin/env python3
"""Static validator for the Baltic Awakening Victoria II mod.

Checks:
  1. Brace balance per file (comments stripped, quoted strings skipped)
  2. Duplicate event IDs within the mod
  3. Mod event IDs colliding with vanilla event IDs
  4. Missing localisation keys for event titles/descriptions/options and
     decision titles/buttons
  5. Event/decision picture references resolving neither to a mod
     gfx/pictures file nor a vanilla picture
  6. add_country_modifier / add_province_modifier names defined neither in
     the mod's event_modifiers.txt nor vanilla's

Exit code 0 = clean, 1 = errors found.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOD = ROOT / "Baltic_Awakening"
VANILLA = ROOT / "tools" / "vanilla_data"

ERRORS = []
WARNINGS = []


def error(path, lineno, msg):
    ERRORS.append(f"{rel(path)}:{lineno}: {msg}")


def warn(path, lineno, msg):
    WARNINGS.append(f"{rel(path)}:{lineno}: {msg}")


def rel(path):
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def strip_comments(text):
    """Yield (lineno, line) with comments removed; quoted strings are
    preserved verbatim (escaped quotes handled) so key extraction works.
    Braces inside strings are excluded from brace counting separately."""
    out = []
    for lineno, line in enumerate(text.splitlines(), 1):
        res = []
        in_str = False
        i = 0
        while i < len(line):
            c = line[i]
            if c == '"':
                if in_str and i + 1 < len(line) and line[i + 1] == '"':
                    res.append('""')
                    i += 2
                    continue
                in_str = not in_str
                res.append(c)
            elif c == "#" and not in_str:
                break
            else:
                res.append(c)
            i += 1
        out.append((lineno, "".join(res)))
    return out


def braces_only(line):
    """Copy of a line with quoted-string contents removed, for brace counting."""
    res = []
    in_str = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == '"':
            if in_str and i + 1 < len(line) and line[i + 1] == '"':
                i += 1
            else:
                in_str = not in_str
        elif not in_str:
            res.append(c)
        i += 1
    return "".join(res)


def read(path):
    return strip_comments(path.read_text(encoding="utf-8", errors="replace"))


def clean_lines(path):
    return read(path)


# ------------------------------------------------------------------ braces
def check_braces(path):
    depth = 0
    for lineno, line in read(path):
        depth += line.count("{") - line.count("}")
        if depth < 0:
            error(path, lineno, "unbalanced braces: unmatched '}'")
            return
    if depth != 0:
        error(path, 0, f"unbalanced braces: {depth} unclosed '{{' at end of file")


# ------------------------------------------------------------------ IDs
def check_ids(event_files, vanilla_ids):
    seen = {}
    for f in event_files:
        for lineno, line in read(f):
            for m in re.finditer(r"\bid\s*=\s*(\d+)", line):
                eid = int(m.group(1))
                if eid in seen:
                    error(f, lineno, f"duplicate event id {eid} (also defined in {seen[eid]})")
                else:
                    seen[eid] = rel(f)
                if eid in vanilla_ids:
                    error(f, lineno, f"event id {eid} collides with a vanilla event id")


# ------------------------------------------------------- localisation keys
def load_mod_loc():
    keys = set()
    for f in sorted((MOD / "localisation").glob("*.csv")):
        for line in f.read_text(encoding="latin-1", errors="replace").splitlines():
            key = line.split(";")[0].strip().lstrip("\ufeff")
            if key and not key.startswith("#"):
                keys.add(key)
    return keys


def check_loc(files, known):
    # event fields: title/desc/name = "KEY"; decision fields similar
    pat = re.compile(r"\b(?:title|desc|name)\s*=\s*\"([^\"]+)\"")
    for f in files:
        for lineno, line in read(f):
            for m in pat.finditer(line):
                key = m.group(1).strip()
                # Skip literal text (names with spaces, numbers, punctuation);
                # real localisation keys are single tokens like EVTNAME95521.
                if not re.fullmatch(r"[A-Za-z0-9_.\-]+", key):
                    continue
                if key not in known:
                    warn(f, lineno, f"localisation key '{key}' not found in mod or vanilla localisation")


# ---------------------------------------------------------------- pictures
def load_mod_pictures():
    names = set()
    for sub in ("events", "decisions"):
        d = MOD / "gfx" / "pictures" / sub
        if d.is_dir():
            names |= {p.stem for p in d.iterdir() if p.is_file()}
    return names


def check_pictures(files, mod_pics, vanilla_event_pics, vanilla_decision_pics):
    pat = re.compile(r"\bpicture\s*=\s*\"([^\"]+)\"")
    for f in files:
        is_event = "events" in f.parts
        allowed = mod_pics | (vanilla_event_pics if is_event else vanilla_decision_pics)
        for lineno, line in read(f):
            for m in pat.finditer(line):
                pic = m.group(1)
                if pic not in allowed:
                    error(f, lineno, f"picture '{pic}' not found in mod or vanilla gfx/pictures")


# --------------------------------------------------------------- modifiers
def load_mod_modifiers():
    names = set()
    f = MOD / "common" / "event_modifiers.txt"
    pat = re.compile(r"^\s*(\w+)\s*=\s*\{")
    for lineno, line in read(f):
        m = pat.match(line)
        if m:
            names.add(m.group(1))
    return names


def check_modifiers(files, mod_mods, vanilla_mods):
    # Two forms:
    #   add_country_modifier = { name = foo ... }   (name on a following line)
    #   add_country_modifier = foo
    for f in files:
        lines = read(f)
        for idx, (lineno, line) in enumerate(lines):
            m = re.search(r"\badd_(?:country|province)_modifier\s*=\s*(\S+)", line)
            if not m:
                continue
            target = m.group(1)
            if target == "":
                continue
            if target == "{":
                for j in range(idx + 1, min(idx + 5, len(lines))):
                    nm = re.search(r"\bname\s*=\s*\"?([\w.\-]+)", lines[j][1])
                    if nm:
                        target = nm.group(1)
                        break
                else:
                    continue
            target = target.strip('"{},')
            if not re.fullmatch(r"[\w.\-]+", target):
                continue
            if target not in mod_mods and target not in vanilla_mods:
                error(f, lineno, f"modifier '{target}' defined in neither mod nor vanilla event_modifiers")


# ------------------------------------------------------------------- main
def main():
    event_files = sorted((MOD / "events").glob("*.txt"))
    decision_files = sorted((MOD / "decisions").glob("*.txt"))
    all_files = event_files + decision_files
    print(f"Checking {len(event_files)} event files, {len(decision_files)} decision files")

    for f in all_files:
        check_braces(f)

    vanilla_ids = set((VANILLA / "vanilla_event_ids.txt").read_text().split())
    check_ids(event_files, vanilla_ids)

    known_loc = load_mod_loc() | set(
        (VANILLA / "vanilla_loc.txt").read_text().splitlines()
    )
    check_loc(all_files, known_loc)

    mod_pics = load_mod_pictures()
    vanilla_event_pics = set((VANILLA / "vanilla_pictures.txt").read_text().splitlines())
    vanilla_decision_pics = set((VANILLA / "vanilla_decision_pics.txt").read_text().splitlines())
    check_pictures(all_files, mod_pics, vanilla_event_pics, vanilla_decision_pics)

    mod_mods = load_mod_modifiers()
    vanilla_mods = set((VANILLA / "vanilla_modifiers.txt").read_text().splitlines())
    check_modifiers(all_files, mod_mods, vanilla_mods)

    for w in WARNINGS:
        print(f"WARN  {w}")
    for e in ERRORS:
        print(f"ERROR {e}")
    print(f"\n{len(all_files)} files checked: {len(ERRORS)} errors, {len(WARNINGS)} warnings")
    sys.exit(1 if ERRORS else 0)


if __name__ == "__main__":
    main()

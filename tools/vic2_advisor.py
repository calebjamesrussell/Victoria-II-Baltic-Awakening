#!/usr/bin/env python3
"""Victoria II save -> Mistral Large 4 advisor harness.

Parses a Victoria II (Heart of Darkness) .v2 save file and produces a
structured game-state brief plus a ready-to-paste prompt for Mistral
Large 4 (via Le Chat or the Mistral API, mistral-large model family).

Usage:
  python tools/vic2_advisor.py SAVE.v2                      # brief to stdout
  python tools/vic2_advisor.py SAVE.v2 --format prompt        # brief + LLM prompt
  python tools/vic2_advisor.py SAVE.v2 --format json          # raw extracted data
  python tools/vic2_advisor.py SAVE.v2 --ask "Should I go to war with RUS?"
  python tools/vic2_advisor.py SAVE.v2 --out brief.md --watch # regenerate on change
  python tools/vic2_advisor.py --selftest                     # built-in fixture tests

Saves live in Documents/Paradox/Victoria II[/<mod name>]/savegames/.
The harness is read-only: it never modifies the save.
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MOD = ROOT / "Baltic_Awakening"

POINT_KEYS = [
    "research_points", "suppression_points", "leadership_points",
    "diplomatic_points", "colonial_points",
]

SCALAR_KEYS = [
    "tag", "human", "government", "ruling_party", "capital",
    "primary_culture", "religion", "prestige", "badboy", "plurality",
    "literacy", "consciousness", "militancy", "money", "tax_base",
    "tariffs", "rank", "great_power", "civilized", "released",
] + POINT_KEYS

POP_TYPES = {
    "farmers", "labourers", "craftsmen", "artisans", "clergymen",
    "bureaucrats", "officers", "soldiers", "aristocrats",
}

GOODS_OF_INTEREST = [
    "coal", "iron", "steel", "cement", "oil", "fuel", "timber", "wood",
    "grain", "cattle", "fish", "fruit", "wine", "tobacco", "tea",
    "coffee", "sugar", "silk", "dye", "wool", "cotton", "fabric",
    "liquor", "wine", "glass", "furniture", "luxury_furniture",
    "paper", "ammunition", "artillery", "explosives", "small_arms",
    "clippers", "steamer_convoy", "electric_gear", "automobiles",
    "aeroplanes", "tanks", "canned_food",
]


# ------------------------------------------------------------- save parser
def tokenize(text):
    tokens = []
    i, n = 0, len(text)
    in_str = False
    buf = []
    while i < n:
        c = text[i]
        if in_str:
            if c == '"':
                if i + 1 < n and text[i + 1] == '"':
                    buf.append('""')
                    i += 2
                    continue
                in_str = False
                tokens.append(("str", "".join(buf)))
                buf = []
            else:
                buf.append(c)
            i += 1
            continue
        if c == '"':
            in_str = True
            i += 1
            continue
        if c == "#":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c in "{}=":
            tokens.append((c, c))
            i += 1
            continue
        if c.isspace():
            i += 1
            continue
        j = i
        while j < n and not text[j].isspace() and text[j] not in '{}="#':
            j += 1
        tokens.append(("val", text[i:j]))
        i = j
    return tokens


def _add(obj, key, value):
    if key in obj:
        cur = obj[key]
        if isinstance(cur, list):
            cur.append(value)
        else:
            obj[key] = [cur, value]
    else:
        obj[key] = value


def _parse_block(tokens, pos, list_key):
    obj = {}
    items = []
    while pos < len(tokens):
        kind, tok = tokens[pos]
        if kind == "}":
            pos += 1
            break
        if kind == "str" or kind == "val":
            nxt = tokens[pos + 1] if pos + 1 < len(tokens) else (None, None)
            if nxt[0] == "=":
                pos += 2
                if pos < len(tokens) and tokens[pos][0] == "{":
                    sub, pos = _parse_block(tokens, pos + 1, tok)
                    _add(obj, tok, sub)
                else:
                    vk, vv = tokens[pos]
                    val = vv if vk == "str" else vv
                    _add(obj, tok, val)
                    pos += 1
            else:
                items.append(tok)
                pos += 1
        else:
            pos += 1
    if items:
        obj["_items"] = items if len(items) > 1 else items[0]
    return obj, pos


def parse_save(text):
    tokens = tokenize(text)
    top, _ = _parse_block(tokens, 0, None)
    return top


def as_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


def fnum(v, default=0.0):
    try:
        return float(str(v).strip('"'))
    except (TypeError, ValueError):
        return default


def unq(v):
    return str(v).strip('"') if v is not None else ""


def find_countries(top):
    out = []
    for key in ("countries", "country"):
        if key in top:
            for c in as_list(top[key]):
                if isinstance(c, dict) and "tag" in c:
                    out.append(c)
            if out:
                return out
    return out


def find_provinces(top):
    provs = []
    for key in ("provinces", "province"):
        if key in top:
            for p in as_list(top[key]):
                if isinstance(p, dict):
                    provs.append(p)
            if provs:
                return provs
    return provs


def find_wars(top):
    wars = []
    for key in ("wars", "war"):
        if key in top:
            for w in as_list(top[key]):
                if isinstance(w, dict):
                    wars.append(w)
    return wars


def pop_stats(provinces, tag):
    total = 0.0
    lit_w = 0.0
    con_w = 0.0
    mil_w = 0.0
    n_prov = 0
    for p in provinces:
        if unq(p.get("controller")) != tag:
            continue
        n_prov += 1
        for k, v in p.items():
            if k in POP_TYPES and isinstance(v, dict) and "size" in v:
                size = fnum(v.get("size"))
                total += size
                lit_w += size * fnum(v.get("literacy"))
                con_w += size * fnum(v.get("con", v.get("consciousness")))
                mil_w += size * fnum(v.get("mil", v.get("militancy")))
            elif isinstance(v, list):
                for sub in v:
                    if isinstance(sub, dict) and "size" in sub and k in POP_TYPES:
                        size = fnum(sub.get("size"))
                        total += size
                        lit_w += size * fnum(sub.get("literacy"))
                        con_w += size * fnum(sub.get("con", sub.get("consciousness")))
                        mil_w += size * fnum(sub.get("mil", sub.get("militancy")))
    avg = lambda w: (w / total) if total else 0.0
    return {
        "provinces": n_prov,
        "population": total,
        "literacy": avg(lit_w),
        "consciousness": avg(con_w),
        "militancy": avg(mil_w),
    }


def tech_list(country):
    techs = []
    t = country.get("technologies") or country.get("technology")
    if isinstance(t, dict):
        for area, val in t.items():
            if isinstance(val, dict):
                for name, lvl in val.items():
                    if str(lvl) not in ("0", "no", "false", ""):
                        techs.append(f"{area}/{name}")
            elif str(val) not in ("0", "no", "false", ""):
                techs.append(str(area))
    return techs


def extract(top, player_tag=None):
    date = unq(top.get("date", ""))
    player = unq(top.get("player", ""))
    tag = player_tag or player
    countries = find_countries(top)
    by_tag = {unq(c.get("tag")): c for c in countries}
    me = by_tag.get(tag)

    great = sorted(
        (c for c in countries if unq(c.get("great_power")) == "yes"),
        key=lambda c: fnum(c.get("prestige")), reverse=True,
    )
    ranked = sorted(
        (c for c in countries if "prestige" in c),
        key=lambda c: fnum(c.get("prestige")), reverse=True,
    )
    my_rank = next(
        (i + 1 for i, c in enumerate(ranked) if unq(c.get("tag")) == tag), None
    )

    provinces = find_provinces(top)
    pops = pop_stats(provinces, tag) if me else None

    wars = []
    for w in find_wars(top):
        wars.append({
            "name": unq(w.get("name", "?")),
            "attackers": [unq(x) for x in as_list(w.get("attackers", {}).get("_items", []))
                          ] if isinstance(w.get("attackers"), dict) else [],
            "defenders": [unq(x) for x in as_list(w.get("defenders", {}).get("_items", []))
                          ] if isinstance(w.get("defenders"), dict) else [],
        })

    market = {}
    wm = top.get("worldmarket")
    if isinstance(wm, dict):
        pool = wm.get("price_pool")
        if isinstance(pool, dict):
            market = {unq(k): fnum(v) for k, v in pool.items()}

    my_wars = [w for w in wars
               if tag in w["attackers"] or tag in w["defenders"]]

    data = {
        "date": date,
        "player_tag": tag,
        "rank": my_rank,
        "great_powers": [unq(c.get("tag")) for c in great],
        "top_by_prestige": [
            {"tag": unq(c.get("tag")), "prestige": fnum(c.get("prestige"))}
            for c in ranked[:8]
        ],
        "active_wars": len(wars),
        "my_wars": my_wars,
        "market": market,
    }
    if me:
        scalars = {k: unq(me.get(k)) for k in SCALAR_KEYS if k in me}
        data["country"] = scalars
        data["points"] = {k: fnum(me.get(k)) for k in POINT_KEYS if k in me}
        data["technologies"] = tech_list(me)
        data["industries"] = len(as_list(me.get("industry", me.get("factories"))))
        if pops:
            data["pops"] = pops
        data["sphere"] = [
            unq(x) for x in as_list(
                (me.get("sphere", {}) or {}).get("_items", [])
            ) if isinstance(me.get("sphere"), dict)
        ] if isinstance(me.get("sphere"), dict) else []
    return data


# ------------------------------------------------------- mod decisions
def load_loc_english(mod_dir):
    texts = {}
    loc = mod_dir / "localisation"
    if not loc.is_dir():
        return texts
    for f in sorted(loc.glob("*.csv")):
        for line in f.read_text(encoding="latin-1", errors="replace").splitlines():
            line = line.lstrip("\ufeff")
            cols = line.split(";")
            if len(cols) >= 2 and cols[0].strip():
                texts[cols[0].strip()] = cols[1].strip()
    return texts


def mod_decisions(mod_dir, tag):
    """Decisions in the mod whose potential matches the given tag."""
    out = []
    loc = load_loc_english(mod_dir)
    dec_dir = mod_dir / "decisions"
    if not dec_dir.is_dir():
        return out
    for f in sorted(dec_dir.glob("*.txt")):
        text = f.read_text(encoding="utf-8", errors="replace")
        top = parse_save(text)
        for _group, body in top.items():
            if not isinstance(body, dict):
                continue
            for name, block in body.items():
                if not isinstance(block, dict) or "potential" not in block:
                    continue
                pot = block.get("potential")
                pot_text = json.dumps(pot) if isinstance(pot, dict) else str(pot)
                tags = set(re.findall(r"\"tag\"\s*[:=]\s*\"?([A-Z]{3})\"?", pot_text, re.I))
                if tags and tag not in tags:
                    continue
                title_key = ""
                tm = re.search(r"\btitle\s*=\s*\"([^\"]+)\"", json.dumps(block))
                if tm:
                    title_key = tm.group(1)
                conds = []
                allow = block.get("allow")
                if isinstance(allow, dict):
                    for k, v in allow.items():
                        if not isinstance(v, (dict, list)):
                            conds.append(f"{k}={unq(v)}")
                out.append({
                    "decision": name,
                    "title": loc.get(title_key, title_key),
                    "tag_specific": sorted(tags),
                    "allow": conds[:8],
                })
    return out


# ------------------------------------------------------------- brief
def fmt_pct(v):
    return f"{fnum(v) * 100:.1f}%" if fnum(v) <= 1.0 else f"{fnum(v):.1f}%"


def render_brief(data, mod_dir=None):
    lines = []
    lines.append("# Victoria II game-state brief")
    lines.append(f"- Date: {data['date']}  |  Playing as: **{data['player_tag']}**"
                 + (f"  |  World rank: #{data['rank']}" if data.get("rank") else ""))
    c = data.get("country", {})
    if c:
        lines.append("")
        lines.append(f"## Your nation: {data['player_tag']}")
        if c.get("government") or c.get("ruling_party"):
            lines.append(f"- Government: {c.get('government', '?')}, "
                         f"ruling party: {c.get('ruling_party', '?')}")
        bits = []
        if c.get("prestige"):
            bits.append(f"prestige {fnum(c['prestige']):.1f}")
        if c.get("badboy"):
            bits.append(f"infamy {fnum(c['badboy']):.2f}/25")
        if c.get("great_power"):
            bits.append(f"great power: {c['great_power']}")
        if bits:
            lines.append("- " + ", ".join(bits))
        pts = data.get("points", {})
        if pts:
            lines.append("- Points: " + ", ".join(f"{k.replace('_points', '')} {v:.1f}"
                                                   for k, v in pts.items()))
        if c.get("money") or c.get("tax_base"):
            lines.append(f"- Treasury: {fnum(c.get('money')):.0f} (daily balance base "
                         f"{fnum(c.get('tax_base')):.1f})"
                         + (f", tariffs {fmt_pct(c['tariffs'])}" if c.get("tariffs") else ""))
        p = data.get("pops", {})
        if p:
            lines.append(f"- Population: {p['population']:.0f} in {p['provinces']} provinces; "
                         f"literacy {p['literacy'] * 100:.1f}%, "
                         f"avg consciousness {p['consciousness']:.2f}, "
                         f"avg militancy {p['militancy']:.2f}")
        if c.get("plurality"):
            lines.append(f"- Plurality: {fmt_pct(c['plurality'])}")
        techs = data.get("technologies", [])
        if techs:
            lines.append(f"- Technologies researched: {len(techs)}")
            lines.append("  " + ", ".join(techs[:25]) + (" ..." if len(techs) > 25 else ""))
        if data.get("industries"):
            lines.append(f"- Factories: {data['industries']}")
        if data.get("sphere"):
            lines.append(f"- Sphere of influence: {', '.join(data['sphere'])}")
    lines.append("")
    lines.append("## World")
    if data.get("great_powers"):
        lines.append("- Great powers: " + ", ".join(data["great_powers"]))
    lines.append("- Top 8 by prestige: " + ", ".join(
        f"{e['tag']} ({e['prestige']:.0f})" for e in data.get("top_by_prestige", [])))
    lines.append(f"- Active wars: {data.get('active_wars', 0)}"
                 + (f" — you are at war: "
                    + "; ".join(w["name"] for w in data.get("my_wars", []))
                    if data.get("my_wars") else ""))
    market = data.get("market", {})
    if market:
        top_goods = sorted(market.items(), key=lambda kv: kv[1], reverse=True)[:10]
        lines.append("- World market, most expensive: "
                     + ", ".join(f"{g} {p:.2f}" for g, p in top_goods))
        cheap = [g for g in GOODS_OF_INTEREST if g in market]
        if cheap:
            lines.append("- Key goods prices: "
                         + ", ".join(f"{g} {market[g]:.2f}" for g in cheap[:12]))
    if mod_dir and data.get("player_tag"):
        decs = mod_decisions(mod_dir, data["player_tag"])
        if decs:
            lines.append("")
            lines.append(f"## Mod decisions in scope ({mod_dir.name})")
            for d in decs:
                line = f"- **{d['title'] or d['decision']}**"
                if d["allow"]:
                    line += " — requires: " + ", ".join(d["allow"])
                lines.append(line)
    return "\n".join(lines) + "\n"


SYSTEM_PROMPT = (
    "You are an expert Victoria II (Heart of Darkness) strategy advisor. "
    "The player pastes a structured brief parsed from their .v2 save file. "
    "Give concrete, actionable advice grounded in the numbers in the brief: "
    "immediate priorities for the next few months, technology and national-focus "
    "recommendations, industrialization and economy, politics and reforms, "
    "diplomacy and spheres, and war conduct if at war. Use short sections with "
    "bullets. Do not invent numbers that are not in the brief."
)

DEFAULT_ASK = "What should I prioritize right now, and why?"


def render_prompt(brief, ask):
    return (
        "=== SYSTEM ===\n" + SYSTEM_PROMPT + "\n\n"
        "=== USER ===\n" + brief + "\nQuestion: " + ask + "\n"
    )


# ------------------------------------------------------------- selftest
FIXTURE = """
date=1890.5.12
player="EST"
country={
	tag="EST" human=yes government="democracy" ruling_party="liberal"
	capital=370 primary_culture="estonian" religion="protestant"
	prestige=42.5 badboy=3.25 plurality=0.55 literacy=0.61
	research_points=12.4 leadership_points=8.1 suppression_points=2.0
	diplomatic_points=4.5 colonial_points=0 money=15234.5 tax_base=812.3 tariffs=0.1
	great_power=no civilized=yes rank=34
	technologies={ culture={ revolution_and_counter_revolution=1 } }
	industry={ id=1 } industry={ id=2 }
}
country={
	tag="RUS" human=no government="absolute_monarchy" prestige=812.0 badboy=8.0
	great_power=yes rank=1
}
country={
	tag="GER" human=no government="constitutional_monarchy" prestige=700.0
	great_power=yes rank=2
}
war={ name="The Baltic War" attackers={ "EST" } defenders={ "RUS" } }
worldmarket={ price_pool={ coal=2.27 iron=3.1 steel=8.4 grain=1.2 oil=6.0 } }
province={
	id=370 controller="EST" core="EST" life_rating=40
	size=120000
	farmers={ id=1 size=80000 literacy=0.6 con=3.1 mil=2.2 }
	craftsmen={ id=2 size=20000 literacy=0.7 con=4.0 mil=1.5 }
	soldiers={ id=3 size=20000 literacy=0.5 con=2.5 mil=1.0 }
}
province={ id=371 controller="RUS" core="RUS" farmers={ id=4 size=90000 literacy=0.4 } }
"""


def selftest():
    top = parse_save(FIXTURE)
    data = extract(top)
    assert data["date"] == "1890.5.12", data["date"]
    assert data["player_tag"] == "EST"
    assert data["rank"] == 3, data["rank"]
    assert data["great_powers"] == ["RUS", "GER"], data["great_powers"]
    assert data["country"]["government"] == "democracy"
    assert data["points"]["research_points"] == 12.4
    assert data["pops"]["provinces"] == 1
    assert abs(data["pops"]["population"] - 120000) < 1e-6
    assert abs(data["pops"]["literacy"] - (80000 * 0.6 + 20000 * 0.7 + 20000 * 0.5) / 120000) < 1e-9
    assert data["technologies"] == ["culture/revolution_and_counter_revolution"]
    assert data["industries"] == 2
    assert data["active_wars"] == 1 and data["my_wars"][0]["name"] == "The Baltic War"
    assert abs(data["market"]["coal"] - 2.27) < 1e-9
    brief = render_brief(data, DEFAULT_MOD)
    assert "Playing as: **EST**" in brief
    assert "infamy 3.25/25" in brief
    assert "Great powers: RUS, GER" in brief
    prompt = render_prompt(brief, DEFAULT_ASK)
    assert "=== SYSTEM ===" in prompt and "=== USER ===" in prompt
    decs = mod_decisions(DEFAULT_MOD, "EST")
    assert isinstance(decs, list)
    print("selftest OK")


# ------------------------------------------------------------- main
def read_save(path):
    raw = path.read_bytes()
    for enc in ("utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def build_output(args):
    top = parse_save(read_save(Path(args.save)))
    data = extract(top, args.player)
    if args.format == "json":
        return json.dumps(data, indent=2, default=str) + "\n"
    brief = render_brief(data, DEFAULT_MOD if args.mod else None)
    if args.format == "prompt":
        return render_prompt(brief, args.ask or DEFAULT_ASK)
    return brief


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("save", nargs="?", help="path to a .v2 save file")
    ap.add_argument("--player", help="override player tag (default: save's player=)")
    ap.add_argument("--format", choices=["brief", "prompt", "json"], default="brief")
    ap.add_argument("--ask", help="question to append in prompt format")
    ap.add_argument("--out", help="write output to this file instead of stdout")
    ap.add_argument("--no-mod", dest="mod", action="store_false",
                    help="skip Baltic Awakening decision cross-reference")
    ap.add_argument("--watch", action="store_true",
                    help="keep running and regenerate when the save changes")
    ap.add_argument("--interval", type=float, default=3.0, help="watch poll seconds")
    ap.add_argument("--selftest", action="store_true", help="run built-in fixture tests")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return 0
    if not args.save:
        ap.error("save path required (or use --selftest)")

    save_path = Path(args.save)
    if args.watch:
        out_path = Path(args.out) if args.out else None
        last = None
        print(f"Watching {save_path} (Ctrl-C to stop)...", file=sys.stderr)
        while True:
            try:
                mtime = save_path.stat().st_mtime
                if mtime != last:
                    last = mtime
                    text = build_output(args)
                    if out_path:
                        out_path.write_text(text, encoding="utf-8")
                        print(f"[{time.strftime('%H:%M:%S')}] wrote {out_path}",
                              file=sys.stderr)
                    else:
                        sys.stdout.write(text + "\n")
            except FileNotFoundError:
                print(f"waiting for {save_path} ...", file=sys.stderr)
            except Exception as e:
                print(f"error: {e}", file=sys.stderr)
            time.sleep(args.interval)
    text = build_output(args)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

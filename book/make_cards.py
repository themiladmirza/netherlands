#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build study cards from the chapters.

    python3 book/make_cards.py                     # -> ~/.claude/dutch-tips.json (spinner)
    python3 book/make_cards.py --json cards.json   # -> a separate card deck

Reads each chapter's content.py (ch01-…, ch02-…) and turns words, phrases,
greetings and numerals into short cards. One line per card, because the
spinner shows them on a single line.
"""
import argparse, glob, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "shared", "lib"))
from text import plain, slugify
from modules import load   # practice.py uses make_cards.load

def cards_from(mod, chapter):
    out = []
    def add(kind, front, back):
        front, back = plain(front), plain(back)
        if not front or not back:
            return
        out.append({"id": f"nl{chapter}-{kind}-{slugify(front)}", "kind": kind,
                    "front": front, "back": back, "chapter": chapter})

    for dutch, english in getattr(mod, "VOC", []):
        add("word", dutch, english)
    for group in (getattr(mod, "VOORSTELLEN", []), getattr(mod, "INFORMATIE", [])):
        for q, a in group:
            add("phrase", q, a)
    for row in getattr(mod, "LANDEN", []):
        add("phrase", row[0], " / ".join(plain(x) for x in row[1:]))
    for group in (getattr(mod, "BEGROETEN", []), getattr(mod, "AFSCHEID", [])):
        for dutch, english in group:
            add("greeting", dutch, english)
    for name in ("NUMS_A", "NUMS_B", "NUMS_C", "NUMS_D"):
        for n, word in getattr(mod, name, []):
            add("number", word, str(n))
    for row in getattr(mod, "VERBS", []):
        add("verb", f"{plain(row[0])} + luisteren / hebben / zijn",
            " · ".join(plain(x) for x in row[1:]))
    for q, a in getattr(mod, "ZINSACCENT", []):
        add("dialogue", q, a)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="write the card deck here")
    ap.add_argument("--tips", default=os.path.expanduser("~/.claude/dutch-tips.json"))
    ap.add_argument("--cooldown", type=int, default=3)
    a = ap.parse_args()

    everything = []
    for d in sorted(glob.glob(os.path.join(ROOT, "ch[0-9][0-9]-*"))):
        cp = os.path.join(d, "content.py")
        if not os.path.exists(cp):
            continue
        chapter = int(os.path.basename(d)[2:4])
        got = cards_from(load(cp, f"content_ch{chapter}"), chapter)
        everything += got
        print(f"  ch{chapter:02d} {os.path.basename(d):<24} {len(got):>4} cards")
    if not everything:
        sys.exit("no chapters with a content.py were found")

    seen, unique = set(), []
    for c in everything:
        if c["id"] in seen:
            continue
        seen.add(c["id"]); unique.append(c)

    if a.json:
        json.dump(unique, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"card deck:    {a.json} ({len(unique)} cards)")

    tips = [{"id": c["id"], "text": f'{c["front"]} → {c["back"]}'[:500],
             "cooldownSessions": a.cooldown} for c in unique]
    os.makedirs(os.path.dirname(a.tips), exist_ok=True)
    json.dump(tips, open(a.tips, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"spinner tips: {a.tips} ({len(tips)} cards)")

if __name__ == "__main__":
    main()

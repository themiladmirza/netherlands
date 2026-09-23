#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Practise Dutch vocabulary — active recall with Leitner boxes.

    python3 book/practice.py                    # whatever is due today
    python3 book/practice.py --chapter 1        # one chapter only
    python3 book/practice.py --kind word        # word | phrase | greeting | number | verb | dialogue
    python3 book/practice.py --direction en-nl  # ask in English
    python3 book/practice.py --count 15         # cards this round
    python3 book/practice.py --stats            # just show progress

While practising:  enter = reveal · y = knew it · n = not yet · q = quit

Progress lives in ~/.claude/dutch-progress.json (box 1-5; higher box = longer wait).
Meant to run in a second terminal pane while Claude is busy.
"""
import argparse, glob, importlib.util, json, os, random, sys, time

ROOT  = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.expanduser("~/.claude/dutch-progress.json")
DAYS  = {1: 0, 2: 1, 3: 3, 4: 7, 5: 21}     # box -> days before it comes back

class C:
    off="\033[0m"; bold="\033[1m"; dim="\033[2m"
    orange="\033[38;5;173m"; teal="\033[38;5;30m"; green="\033[38;5;71m"; red="\033[38;5;167m"

def all_cards():
    sys.path.insert(0, ROOT)
    import make_cards
    out = []
    for d in sorted(glob.glob(os.path.join(ROOT, "ch[0-9][0-9]-*"))):
        cp = os.path.join(d, "content.py")
        if os.path.exists(cp):
            chapter = int(os.path.basename(d)[2:4])
            out += make_cards.cards_from(make_cards.load(cp, f"c{chapter}"), chapter)
    seen, unique = set(), []
    for c in out:
        if c["id"] not in seen:
            seen.add(c["id"]); unique.append(c)
    return unique

def load_state():
    try:    return json.load(open(STATE, encoding="utf-8"))
    except Exception: return {}

def save_state(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(s, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def is_due(card, state, now):
    st = state.get(card["id"])
    return True if not st else now >= st.get("due", 0)

def show_stats(cards, state):
    per = {i: 0 for i in range(1, 6)}
    fresh = 0
    for c in cards:
        st = state.get(c["id"])
        if st: per[st.get("box", 1)] = per.get(st.get("box", 1), 0) + 1
        else:  fresh += 1
    learned = sum(v for b, v in per.items() if b >= 3)
    print(f"\n{C.bold}Progress{C.off}  {len(cards)} cards")
    print(f"  {C.dim}new{C.off}        {fresh}")
    for b in range(1, 6):
        print(f"  box {b}      {per[b]:>4}  {C.teal}{'█'*min(40, per[b])}{C.off}")
    pct = 100*learned/len(cards) if cards else 0
    print(f"  {C.green}solid{C.off}      {learned}  ({pct:.0f}%)\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", type=int)
    ap.add_argument("--kind")
    ap.add_argument("--direction", default="nl-en", choices=["nl-en", "en-nl", "both"])
    ap.add_argument("--count", type=int, default=20)
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args()

    cards = all_cards()
    if a.chapter: cards = [c for c in cards if c["chapter"] == a.chapter]
    if a.kind:    cards = [c for c in cards if c["kind"] == a.kind]
    if not cards: sys.exit("no cards found")

    state = load_state()
    if a.stats:
        show_stats(cards, state); return

    now = time.time()
    due = [c for c in cards if is_due(c, state, now)]
    random.shuffle(due)
    due = due[:a.count]
    if not due:
        print(f"\n{C.green}Nothing due — come back later.{C.off}")
        show_stats(cards, state); return

    print(f"\n{C.orange}{C.bold}Dutch practice{C.off}  ·  {len(due)} cards"
          f"  {C.dim}(enter = reveal · y/n · q = quit){C.off}\n")
    right = wrong = 0
    for i, c in enumerate(due, 1):
        flip = (a.direction == "en-nl") or (a.direction == "both" and random.random() < .5)
        question, answer = (c["back"], c["front"]) if flip else (c["front"], c["back"])
        label = "EN→NL" if flip else "NL→EN"
        print(f"{C.dim}{i}/{len(due)}  {label}  ch{c['chapter']:02d} {c['kind']}{C.off}")
        print(f"  {C.bold}{question}{C.off}")
        try: key = input(f"  {C.dim}enter…{C.off}")
        except (EOFError, KeyboardInterrupt): break
        if key.strip().lower() == "q": break
        print(f"  {C.teal}{answer}{C.off}")
        try: grade = input(f"  {C.dim}did you know it? y/n {C.off}").strip().lower()
        except (EOFError, KeyboardInterrupt): break
        if grade == "q": break
        st = state.get(c["id"], {"box": 1})
        if grade.startswith("n"):
            st["box"] = 1; wrong += 1
            print(f"  {C.red}→ back to box 1{C.off}\n")
        else:
            st["box"] = min(5, st.get("box", 1) + 1); right += 1
            print(f"  {C.green}→ box {st['box']}{C.off}\n")
        st["due"] = now + DAYS[st["box"]] * 86400
        state[c["id"]] = st
        save_state(state)

    done = right + wrong
    if done:
        print(f"{C.bold}Done{C.off}  {right} right · {wrong} not yet  ({100*right/done:.0f}%)")
    show_stats(cards, state)

if __name__ == "__main__":
    main()

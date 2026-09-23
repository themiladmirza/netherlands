# -*- coding: utf-8 -*-
"""Turn a chapter's Woordenlijst into practice cards. Only the Woordenlijst.

VOC is the word list the book prints under "§N.2 Woordenlijst" — it is the only
list rendered with layout.vocab_rows(), and it is the only source of cards. Every
other list in content.py (countries, verbs, the clock, possessives, numerals,
greetings, family words) belongs to a teaching section, not the word list, and
must NOT be turned into cards: doing that once produced fronts like
"Ik kom uit China." that asked no question at all.

Each word is two cards, in the order the recall research recommends:

  A · recognition   de verjaardag  +  "Gefeliciteerd met je verjaardag."  -> flip
  B · production    "Gefeliciteerd met je ______."  (birthday)            -> type it

Stage B needs a sentence to blank, and the sentence is *lifted from the chapter*,
never written for the occasion — transcribe-never-invent governs study material
exactly as it governs the page. A word the book never uses in running text gets
recognition only.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))                      # book/ — for make_cards
from make_cards import plain, slugify                  # noqa: E402

# Attributes holding running Dutch prose, mined for cloze sentences. Exercise
# prompts and grammar tables are excluded: a cloze wants a sentence someone says.
PROSE = ("DIALOOG", "DIALOOG_INTRO", "DIALOOG_2", "DIALOOG_3", "TEKST", "CULTUUR",
         "PRAKTIJK", "DATING", "BESTELLEN", "AFREKENEN", "BEDANKEN", "BESCHRIJVEN")

_SENT = re.compile(r"[^.!?…]*[.!?…]")
_PAREN = re.compile(r"\s*\([^)]*\)\s*$")

# A cloze sentence has to stand on its own once the word is blanked out. Measure
# that in words, not characters: a 14-character floor threw away "Hoe heet je?"
# (12 chars, and one of the best cards in chapter 1) while keeping any long
# rambling line. Three words means at least two remain as context after blanking.
MIN_WORDS = 3
MAX_SENTENCE = 110

# Answers longer than this are flipped rather than typed.
MAX_TYPED_WORDS = 2


def cell(value):
    """Text of a word-list cell, where a <br> separates two alternative forms.

    "onze les<br>ons adres" is two examples, not one phrase: collapsing the break
    to a space produced "onze les ons adres". They are alternatives, so join them
    with " / " — the separator the book already uses inside a single cell.
    """
    parts = [plain(p).strip().strip("/").strip()
             for p in re.split(r"<br\s*/?>", str(value), flags=re.I)]
    return " / ".join(p for p in parts if p)


def headword(dutch):
    """VOC spelling -> the matchable form. 'ben (zijn)' -> 'ben'."""
    head = _PAREN.sub("", plain(dutch)).strip().rstrip("?").strip()
    return "" if (not head or "…" in head or "..." in head) else head


def forms(head):
    """Longest first: 'de plaats' before the bare 'plaats'."""
    out = [head]
    bare = re.sub(r"^(?:de|het)\s+", "", head, flags=re.IGNORECASE)
    if bare.lower() != head.lower() and " " not in bare:
        out.append(bare)
    return out


def _pattern(head):
    alts = "|".join(re.escape(f) for f in sorted(forms(head), key=len, reverse=True))
    return re.compile(rf"(?<!\w)({alts})(?!\w)", re.IGNORECASE)


def sentences(mod):
    """Every usable sentence of running Dutch in the chapter, in book order."""
    out, seen = [], set()
    for name in PROSE:
        value = getattr(mod, name, None)
        if value is None:
            continue
        items = value if isinstance(value, (list, tuple)) else [value]
        for item in items:
            parts = item if isinstance(item, (list, tuple)) else [item]
            for part in parts:
                text = plain(part)
                if not text:
                    continue
                found = [s.strip() for s in _SENT.findall(text)] or [text]
                for s in found:
                    if (len(s.split()) >= MIN_WORDS and len(s) <= MAX_SENTENCE
                            and s not in seen):
                        seen.add(s)
                        out.append(s)
    return out


def _blank(sentence, match):
    """Replace the matched word with a blank of the same visual weight."""
    return sentence[:match.start()] + "______" + sentence[match.end():]


def _card(chapter, kind, front, back, dutch):
    """One word list entry. `dutch` is spoken, and is what a typed answer must match."""
    return {
        "id":       f"nl{chapter}-{kind}-{slugify(front)}",
        "kind":     kind,
        "front":    front,
        "back":     back,
        "dutch":    dutch,
        "chapter":  chapter,
        "sentence": None,
        "cloze":    None,
        "meaning":  None,
    }


def deck(mod, chapter):
    """Cards for this chapter's Woordenlijst, in the order the book prints it."""
    pool = sentences(mod)
    cards, seen_ids = [], set()

    # The word list prints some words twice with different meanings — ch1 has
    # "jullie = your (plural)" and "jullie = you (plural)", ch2 has "nog = any"
    # and "nog = as well". One word, one card: merge the meanings instead of
    # letting the second entry silently drop out.
    merged, order = {}, []
    for dutch, english in getattr(mod, "VOC", []) or []:
        front, back = cell(dutch), cell(english)
        head = headword(front)
        if not head or not back:
            continue                       # discontinuous entry ("waar … vandaan")
        key = slugify(front)
        if key not in merged:
            merged[key] = [front, [back], head]
            order.append(key)
        elif back not in merged[key][1]:
            merged[key][1].append(back)

    for key in order:
        front, backs, head = merged[key]
        card = _card(chapter, "word", front, " / ".join(backs), head)
        seen_ids.add(card["id"])

        # stage B: the book's own sentence, with the word blanked out
        pattern = _pattern(head)
        bare = re.sub(r"[^\w ]+", "", head.lower()).strip()
        for candidate in pool:
            # a "sentence" that is just the entry again teaches nothing:
            # VOC "hoe heet jij?" matched the line "Hoe heet jij?"
            if re.sub(r"[^\w ]+", "", candidate.lower()).strip() == bare:
                continue
            m = pattern.search(candidate)
            if m:
                card["sentence"] = candidate
                card["cloze"] = _blank(candidate, m)
                break
        cards.append(card)

    return cards


def attach_meaning(cards, translations):
    """Give each card's sentence its English, from the chapter's translations.py.

    The book prints no English for its dialogue, so unlike everything else on the
    page these sentences are translated for the cards rather than transcribed.
    They live in <chapter>/translations.py, deliberately outside content.py, so
    the line between "the book" and "written for this project" stays visible.

    A missing translation is reported, never invented and never silently skipped:
    the card would otherwise reveal a sentence with no meaning attached.
    """
    missing = []
    for card in cards:
        sentence = card.get("sentence")
        if not sentence:
            continue
        english = translations.get(sentence)
        if english:
            card["meaning"] = english
        else:
            missing.append(sentence)
    return sorted(set(missing))

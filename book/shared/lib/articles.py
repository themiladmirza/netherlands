# -*- coding: utf-8 -*-
"""The de/het nouns of a chapter's Woordenlijst, for the article drill.

Only what the word list prints with its article counts: "de verjaardag", or the
base form a diminutive points to, "biertje (het bier)". A noun the list gives
without an article stays out — the drill must never guess one.
"""
import html, re

# Word-list entries that start with "de"/"het" but are not article + noun.
NOT_NOUNS = {"het is"}      # ch1: "it is"

def nouns(voc):
    """[{"article", "noun", "en"}] in word-list order, each noun once."""
    out, seen = [], set()
    for head, en in voc:
        m = (re.match(r"^(de|het) ([^<(]+?)\s*$", head)
             or re.search(r"<small>\((de|het) ([^)]+)\)</small>", head))
        if not m or f"{m.group(1)} {m.group(2).strip()}" in NOT_NOUNS:
            continue
        noun = html.unescape(m.group(2)).strip()
        if noun in seen:
            continue
        seen.add(noun)
        out.append({"article": m.group(1), "noun": noun,
                    "en": html.unescape(re.sub(r"<[^>]+>", "", en))})
    return out

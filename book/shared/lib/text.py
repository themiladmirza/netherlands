# -*- coding: utf-8 -*-
"""Small text utilities shared by the card builders (make_cards.py, cloze.py)."""
import html, re, unicodedata


def plain(s):
    """Visible text of a cell: no tags, no entities, single spaces.

    Line-breaking tags become a space before the rest are stripped — without that
    "onze les<br>ons adres" collapsed into the non-word "onze lesons adres". And
    entities are unescaped *before* whitespace is collapsed, not after, or the
    &nbsp; padding in "de man /<br>&nbsp;&nbsp;&nbsp;de echtgenoot" survives as a
    run of three spaces.
    """
    s = re.sub(r"<br\s*/?>|</(?:p|div|li|tr|h\d)>", " ", str(s), flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s.replace("&nbsp;", " "))
    return re.sub(r"\s+", " ", s).strip()

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]

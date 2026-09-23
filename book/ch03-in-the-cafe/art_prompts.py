# -*- coding: utf-8 -*-
"""Chapter 3 — In het café.  Prompts for the illustrations.

The shared style preamble (../shared/lib/art_style.py) is prepended to every
SCENE automatically. Never mention text or numbers in the image.

`cafes` replaces the three photographs the original prints for Opdracht 10. The
reading text describes a waterside terrace with boats, so the three scenes must
be clearly distinguishable — that is the whole task.

Generate:  python3 book/generate_art.py ch03-in-the-cafe
"""

JOBS = [
 ("opener", "portrait",
  "The interior of a traditional Dutch brown café in the early evening: a long wooden bar with "
  "brass fittings and taps, shelves of bottles and glassware, warm hanging lamps, a few regulars "
  "talking over drinks at the bar and at small tables. Cosy, lived-in, amber light."),

 ("dialoog", "landscape",
  "Three friends around a small café table celebrating a birthday: two young women and a young man, "
  "raising a glass of red wine, a beer and a cola in a toast, all smiling. A waiter in an apron "
  "stands beside the table with a round tray. Warm café interior behind them."),

 ("bestellen", "square",
  "A café customer seated at a table raising a hand to catch the attention of a waiter who is "
  "approaching with an empty round tray under one arm. Small marble table, a menu card lying flat "
  "and blank. Friendly, ordinary moment of ordering."),

 ("cafes", "landscape",
  "Three clearly separate café scenes side by side in three equal panels, each very different from "
  "the others. LEFT: a dim cosy interior with a wooden bar, lamps and bottles. MIDDLE: a small "
  "outdoor terrace against a whitewashed stone wall with climbing plants, tables under a canopy. "
  "RIGHT: a canal-side terrace with tables along the water, moored boats on the canal and tall "
  "narrow Dutch houses opposite. The three must be instantly tellable apart."),

 ("praktijk", "square",
  "A person at a café counter ordering, holding up one finger to indicate an order, while the "
  "barista listens and reaches for a cup. Coffee machine, cups and a small plant on the counter. "
  "Warm and encouraging."),

 ("reflectie", "square",
  "An abstract flat illustration of steady progress: a gentle ascending path of rounded steps with "
  "small check marks, a rising sun, and a person standing partway up looking ahead. Calm, encouraging."),
]

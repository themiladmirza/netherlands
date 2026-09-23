# -*- coding: utf-8 -*-
"""Chapter 2 — In de kantine.  Prompts for the illustrations.

The shared style preamble (../shared/lib/art_style.py) is prepended to every
SCENE automatically. Describe only the scene here — not the style, not the palette.
Never mention text or numbers in the image: all type is set as real vector text.

`gezinnen` replaces the three family snapshots the original prints for Opdracht 2;
the task is to describe a person in one of them, so the image has to show several
clearly different people.

Generate:  python3 book/generate_art.py ch02-in-the-canteen
Shapes:    portrait (1024x1536) · landscape (1536x1024) · square (1024x1024)
"""

JOBS = [
 ("opener", "portrait",
  "A bright, busy university canteen at midday. A young woman sits at a light wooden table with "
  "a cup of coffee and a sandwich, looking up with an easy, welcoming smile. Tall windows, potted "
  "plants, other students at tables further back, trays and cups. Warm, sociable, everyday."),

 ("dialoog", "landscape",
  "Two young women sitting across a small canteen table with cups of coffee, mid-conversation. "
  "One holds out a printed photograph to show the other, who leans in to look. One has short light "
  "hair, the other long dark hair. Relaxed and friendly, a window and other tables behind them."),

 ("familie", "square",
  "A warm three-generation family group portrait: grandparents, parents, and children of different "
  "ages standing and sitting together, plus an aunt and uncle at the edges. Everyone distinct in "
  "height, hair and clothing so individuals can be told apart. Decorative and clear, not a snapshot."),

 ("gezinnen", "landscape",
  "Three separate family groups side by side, clearly divided into three panels. Left: a couple with "
  "two teenagers. Middle: grandparents with a grown son and daughter. Right: two parents with three "
  "young children. Every person visibly different in height, build, hair colour and clothing, so each "
  "one can be picked out and described. Full-length figures, plain backgrounds."),

 ("seizoenen", "landscape",
  "A horizontal strip of the same Dutch canal street through four seasons, divided into four equal "
  "panels: bare branches and a grey sky; then blossom and tulips; then full green trees and bright "
  "sun; then falling amber leaves. Continuous composition, the same houses recognisable in each."),

 ("praktijk", "square",
  "One person on a city pavement turning to another and gesturing at their wrist to ask the time, "
  "the other glancing down at a watch and answering. A large public clock on a pole nearby, its face "
  "blank with no markings. Friendly, everyday street moment."),

 ("reflectie", "square",
  "An abstract flat illustration of steady progress: a gentle ascending path of rounded steps with "
  "small check marks, a rising sun, and a person standing partway up looking ahead. Calm, encouraging."),
]

# Where each image is placed in pages.py:
#   opener -> cover · dialoog -> the dialogue support page · familie -> 2.3
#   gezinnen -> Opdracht 2 · seizoenen -> 2.11 · praktijk -> In de praktijk
#   reflectie -> Reflectie

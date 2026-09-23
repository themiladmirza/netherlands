# Chapter 1 — Welkom

Original: pp. 20–31 (12 pages) → redesign: 20 pages.

## Content
Everything carried over: 89 vocabulary entries, 18 dialogue turns, 12 exercises,
33 numerals, 19 greetings/farewells, 10 sentence-stress pairs, the personal
details form, the surname top 10, Cultuur, Reflectie.

## Two deliberate departures from the original
1. **The word list reads top-to-bottom per column** (the original used six
   columns read across — the weakest page in the book). The infinitive is set
   small and grey after the stem.
2. **"Wie is wie in de dialoog?" card on p. 3** — no new material, just a summary
   of who Karin, Paul, Susy and Ning are according to the dialogue. It fills an
   otherwise half-empty page. Safe to drop; it stands alone in `pages.py`.

## Illustrations
10 of them, `gpt-image-2.5-flare`, 2026-09-12. Prompts in `art_prompts.py`.
`formulier.png` ended up unplaced: the form itself already fills p. 15. The image
is kept in case the layout changes.

## What the redesign does not fix
§1.1 and §1.9 are built around audio that sits behind the code on the inside
cover (coutinho.nl/nederlandsingang3). Without sound those two sections lose
their point.

## Instructions in English
Task rubrics, directions, the Reflectie self-checks and the Verdiepingsmateriaal
list are in English; every exercise item, the dialogue, the word list, the
reference cards and the grammar notes stay Dutch. The original prints its
rubrics in Dutch — this is a deliberate departure, so the task is never the
puzzle. The book's own section names and the label *Opdracht* stay Dutch.

Precedent from the original: its *Eigen vocabulaire* page already gives the
instruction in Dutch and then again in English. Here that block is English only.

## Pagination: the dialogue stays whole
The dialogue was originally split across our pages 2 and 3 — page 3 opened on
*"Docent: Waar woon je?"* with no heading, mid-conversation, while the audio ran
1:38 straight through. The original fits the whole conversation on book p.21.

Fixed by moving the illustration and the supporting cards to the facing page, so
p.2 now carries the complete dialogue exactly as the original does. It is wrapped
in `keep("dialoog-1.1", …)`, and `build.py` now fails if any keep-block lands on
more than one page.

Seven blocks are guarded in this chapter: `dialoog-1.1`, `woordenlijst-a/-b`,
`werkwoord-1.4`, `opdracht-2`, `opdracht-3`, `zinsaccent-1.9`.

Two section-level spreads remain, and are fine — no block is cut, the sections
merely shared a page in the original: §1.3's reference cards (p.6) with Opdracht 1
(p.7), and In de praktijk (p.18) with Eigen vocabulaire (p.19).

## Pagination: sections keep their own exercises
§1.5 Telwoorden originally left Opdracht 4–5 on the next page, above §1.6's
heading — so p.12 opened with two exercises that looked like they belonged to the
alphabet. Fixed by moving them onto p.11 with Telwoorden; the houses illustration
moved to p.12, where it sits next to Opdracht 6 ("Wat zijn de letters van je
postcode?") and pairs with the Dutch front doors.

`build.py` now fails on this pattern (`section mix`): a page may continue one
section or start a new one, never both.

Pages that merely continue a section without repeating the heading are fine —
p.3, p.5, p.7, p.9, p.10, p.15 — because the running head names the section, which
is exactly how the original handles its own word-list spill.

## Sweep of all 20 pages
Automated: geometry clean on every page (no overflow, no element past the page
box, no upscaled image, no stranded heading, nothing under the footer). Content
inventory checked against `content.py` — 89 vocabulary entries, 18 dialogue turns,
33 numerals, 19 greetings, 10 zinsaccent pairs, 11 form fields, 10 surnames,
10 objectives, all present. All 13 referenced assets resolve.

Three real faults found by eye and fixed:
1. **Numerals read across instead of down** — 0,1,2 / 3,4,5 … instead of the
   original's units | teens | tens columns, which destroyed the -tien / -tig
   patterns. Same class of bug as the word list. Now `number_columns()`.
2. **"u of jij ?"** — `h2.sec` is a flex container, so the trailing question mark
   became its own flex item with a 3.4 mm gap. Wrapped in `.lock`.
3. **Eigen vocabulaire** stopped 13 lines down a page whose whole purpose is
   blank writing space. Now 22 lines per column.

Left alone deliberately: pages at 55–63 % fill (p7, p9, p10, p13, p18). Nothing is
cut and every one is a single complete section; the original is denser because it
crams, which is the thing being fixed.

`art/formulier.png` remains unplaced — the form itself fills p.15.

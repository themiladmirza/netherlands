# Chapter 3 — In het café

Original: book pp. 46–57 (12 pages) → redesign: 20 pages.

## Content
Everything carried over: 24 dialogue turns across three scenes, 51 vocabulary
entries, 13 exercises, the article/diminutive tables, 22 ordinals, the word
cloud, the invitation e-mail, the reading text, 18 word-stress items and 30 o/oo
words, Cultuur, In de praktijk, Reflectie. Verified against `content.py`.

## The blue part in Opdracht 6 — reconstructed, not transcribed
The book prints the phrase to be fronted in **blue**. `hard.pdf` is a pure
greyscale scan — I measured it: zero pixels with any channel spread, so the
colour is simply not in the file. The apparent bolding in the scan is the MRC
text layer and is unreliable (it appears to mark *niet* in item 4, but
*"Niet weet ik dat"* is ungrammatical).

So each fronted phrase in `OPD6` is reconstructed on grammatical grounds: for
every sentence exactly one constituent yields a well-formed inversion, and that
is the one marked. They are shown in teal rather than blue to match the palette.
If you have the printed book to hand, worth a spot-check against p. 52.

## Decisions
- **Andres and the ober join the cast** (`voices.py`); Susy and Edit keep the
  voices they have had since chapters 1–2.
- **`cafes.png` replaces the original's three café photographs** for Opdracht 10.
  The a/b/c labels are typeset over the image, not generated into it. The reading
  text describes a waterside terrace with boats, so the three scenes are drawn to
  be unmistakably different — that difference *is* the task.
- **The word cloud is typeset**, not an image: real text at varying sizes, so it
  stays searchable and sharp.
- **Opdracht 12 has no audio**, for the same reason as ch2's Opdracht 15 — the
  word pairs are never printed. Opdrachten 11 and 13 print theirs and are recorded.

## Pagination
The word list is 51 entries — fewer than ch1 (89) or ch2 (76). Putting it all on
one page overflowed by 55 px, and splitting it evenly left both halves half-empty,
so it is split 34/17 with Opdracht 1 joining the continuation. Likewise §3.8
keeps its own Opdracht 7, and Opdrachten 8–9 share the following page. That took
the chapter from 22 pages to 20 with no page running thin.

## Rangtelwoorden drill (screen only)

`extra.js` / `extra.css` add a typing drill straight after the 3.8 page: the card
shows "2e", you type "tweede", and Enter checks it and plays the word
(`audio/rang-<n>.mp3`, 22 clips, docent voice, card settings, approved by ear on
2026-10-09). The pairs are read from the printed Rangtelwoorden card, so
`content.py` stays the only copy. Chapter-only, so nothing in `shared/` changed.

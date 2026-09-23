# Chapter 2 — In de kantine

Original: book pp. 32–45 (14 pages) → redesign: 25 pages.

## Content
Everything carried over: 20 dialogue turns, 76 vocabulary entries, 16 exercises,
21 family-relation terms, 12 clock phrases + 4 durations, 7 day sentences,
12 months, 4 seasons, 16 dating-agency names, 30 a/aa words, Cultuur,
In de praktijk, Reflectie. Verified against `content.py` — nothing missing.

## Decisions
- **Clock faces are drawn as SVG** (`layout.clock()`), not generated art, so the
  hands are exactly right for each time being taught. All six verified by eye:
  elf uur, tien over elf, kwart over elf, half twaalf, kwart voor twaalf,
  vijf voor twaalf.
- **The 1-1-2 sign is typeset, not generated.** It is a public emergency number
  the book reproduces; setting it as type keeps it accurate and avoids generating
  something that imitates real signage.
- **`gezinnen.png` replaces the original's three family snapshots** for Opdracht 2.
  The task is to describe a person, so the image shows clearly distinct people.
- **Edit joins the cast** (`voices.py`) and keeps her own voice from here on.
  Susy keeps her chapter-1 voice.

## Opdracht 15 has no audio, deliberately
The exercise plays word pairs and triples that the book never prints — they exist
only on the publisher's audio. There is nothing to transcribe, and inventing them
would be making up content. The exercise and its answer grids are kept and the
icon is left inert. Opdracht 16 *does* print its words, so it is recorded.

## Faults found in the sweep and fixed
1. Opdracht 16's audio icon was not wired (`task(...)` without `audio=`), so only
   one of two audio links existed. Caught by the build's link count.
2. De klok overflowed the trim by 79 px; the clock row went from two rows of
   three to one row of six.
3. Opdracht 15's tick tables had no cell borders, so empty cells read as solid
   bars, and table B carried an empty header the original does not have.

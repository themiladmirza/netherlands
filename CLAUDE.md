# Nederlands in gang — redesigned chapters

Redesigning chapters of *Nederlands in gang* (Coutinho, 3rd revised edition 2017)
from the scan in `hard.pdf` into properly typeset PDFs with original illustrations.
Personal study material, made alongside an owned copy of the book.

Chapters 1–3 are done: ch1 20 pages (10 illustrations, 4 audio), ch2 25 pages
(7 illustrations, 2 audio), ch3 20 pages (6 illustrations, 3 audio). The usual job
in a new session is **"do chapter N"** — treat those as the reference for what
finished looks like.
Full docs: `book/README.md`. Chapter-specific decisions: `book/ch<NN>-<slug>/NOTES.md`.

## Language rules

Two separate rules. Get both right.

**In the code: English is structure, Dutch is content.** Folder names, filenames,
identifiers, CLI flags, CSS classes, comments, docstrings and docs are English.
Don't "helpfully" name things in Dutch — that was done once and had to be undone.

**On the page: English tells you what to do, Dutch is what you study.**

| English | Dutch |
|---|---|
| Opdracht instructions — *"Fill in a personal pronoun."* | every exercise item, the dialogue, the word list |
| directions — *"Listen and repeat."*, *"Example"*, *"(move on to the next student)"* | reference cards, grammar tables, examples |
| Reflectie self-checks, *yes / not yet* | grammar explanations (*"In de inversie verandert de vorm…"*) |
| notes about how to use a section | the book's own section names — Dialoog, Woordenlijst, Telwoorden, Cultuur, Reflectie, Verdiepingsmateriaal, and the label **Opdracht** |
| the Verdiepingsmateriaal list of online extras | the running head, the PDF title, page numbers as Dutch words |

The learner should never have to decode a rubric to find out what the task is —
but every word they are meant to read, learn or produce stays Dutch. When in
doubt: is this the exercise, or is it telling me how to do the exercise?

---

## Workflow for a new chapter

```bash
# 1. scaffold            number, Dutch title (printed), English slug (folder)
python3 book/new_chapter.py 2 "In de kantine" in-the-canteen

# 2. pull the source out of the scan: chapter folder, first & last BOOK page
python3 book/extract_source.py ch02-in-the-canteen 32 45
#    -> source/scan-cleaned.pdf + source/scan-text.txt

# 3. transcribe into content.py  (read the cleaned scan; OCR is a draft, not truth)

# 4. describe the illustrations in art_prompts.py, then
python3 book/generate_art.py ch02-in-the-canteen

# 5. write audio_script.py (what is spoken, by whom, with which emotion tags), then
python3 book/generate_audio.py ch02-in-the-canteen

# 6. lay out pages.py — audio_icon("audio/x.mp3") on every audio item — then build
python3 book/build.py ch02-in-the-canteen

# 7. refresh the study cards
python3 book/make_cards.py

# 8. look at BOTH outputs — serve from book/, never from the chapter folder,
#    or ../shared/style.css 404s and you measure an unstyled page
python3 -m http.server 8000 --directory book
#    -> http://localhost:8000/ch02-in-the-canteen/index.html
```

Both API keys load from `.env` automatically (`shared/lib/env.py`), so no `export`
is needed. A real environment variable still overrides it for a one-off run.

---

## Things that will bite you

**`hard.pdf` page mapping.** 318 PDF pages = 318 book pages, and
**book page = PDF page + 1** (verified at ch1 and ch18). Every PDF page carries a
CropBox selecting ONE book page out of the scanned spread, so PyMuPDF renders a
single page. **The Read tool ignores CropBox** and shows the whole spread *twice* —
that is a rendering artifact, not duplication in the file. Don't conclude the file
has duplicate pages; that mistake was made once already.

**Reading `hard.pdf`.** It's 318 pages, so Read *requires* the `pages:` parameter
(max 20 per call). There is no text layer — it's an MRC scan: crisp 200 dpi bitonal
text over a blurry 100 dpi grey background. That's why the tinted boxes carry
bleed-through from the facing page, and why `extract_source.py` *rebuilds* the
tints rather than filtering them. 200 dpi is the hard ceiling on detail.

**The scan is pure greyscale — colour-only cues are lost.** The book marks some
things in blue (the phrase to front in ch3's Opdracht 6). I measured it: zero
pixels with any channel spread, so that colour is simply not in `hard.pdf`. Worse,
the apparent **bold** in the scan is the MRC text layer and is *not* the book's
emphasis — in ch3 it appeared to mark *niet*, where fronting it is ungrammatical.
When an exercise depends on a highlight, reconstruct it on grammatical grounds,
say so in NOTES.md, and flag it for a spot-check against the printed book.

**macOS `sed` has no `\b`.** Word-boundary renames silently do nothing. Use Python
for any token rename across files.

**Image API rate limit: 5 per minute.** `generate_art.py` catches it, waits 35 s
and retries up to six times. Expect a chapter's art to take a few minutes.

**Audio: only `eleven_v3` interprets emotion tags.** On the other models
`[warmly]` risks being read aloud. Verified on v3: tagged and untagged renders
come out the same length, so the bracket is acted on, not spoken.

**Audio verification scores wobble.** `generate_audio.py` transcribes each file
back and diffs it against the script. The same untouched files scored 89 % and
then 99 % on consecutive runs — speech-to-text is non-deterministic, and letter
spelling (`t w` heard as `tw`) drags the number down. Re-run before believing a
low score; it catches mangled Dutch, not an ugly read. Listen before shipping.

**Pin the speech-to-text language.** `transcribe()` sends `language_code=nld`.
Without it, auto-detect guesses from the audio alone, and on short clips it guessed
Swedish — scoring a perfectly good "En waar kom je vandaan?" at 51%. Pinning it took
chapter 1's card audio from 26/30 to 28/30 verified with no re-recording. What is
left after that is the real wobble: a 3-word clip where one word is misheard caps
out near 67% however good the read is, so judge short clips by ear, not by score.

**Some listening exercises never print their words.** ch2 Opdracht 15 and ch3
Opdracht 12 play word pairs that exist only on the publisher's audio. There is
nothing to transcribe and inventing them would break the transcribe-never-invent
rule: keep the exercise and its answer grid, leave the icon inert, and note it in
`audio_script.py`. Exercises that *do* print their words (ch2 Opdr 16, ch3 Opdr
11/13) get recorded normally.

**Runtime-built UI leaks into the PDF unless you hide it in *every* medium.**
`flashcards.js` creates its launcher and overlay at runtime, and print-to-pdf runs
the script too. Styling those nodes only inside `@media screen` left an unstyled
`<button>Oefenen</button>` in the print flow and chapter 1 came out 21 pages. The
rule: declare `display:none` outside any media query, then switch it back on inside
`@media screen` — hide first, reveal for screen, never the reverse. And restate
`.deck-overlay[hidden]{display:none}`, because `.deck-overlay{display:flex}` has the
same specificity as the user agent's `[hidden]` rule and wins on order, so the
overlay would never close.

**Chrome bakes absolute paths into PDF file links.** The audio icons are `<a href>`
so print-to-pdf turns them into real link annotations — but Chrome writes
`/Users/…/audio/x.mp3` into them. `build.py` rewrites these to relative
(`audio/x.mp3`) after rendering; without that the PDF breaks when moved and leaks
the home directory.

**Glossing runs on every build.** `build.py` marks the first occurrence of each
glossary word — first in the *book*, not the chapter — with a hover translation in
`index.html`. It regenerates every earlier chapter in memory to work that out, so
chapters must stay importable in isolation. Excluded: word lists, running heads,
footers, `<title>`, and the cover (`ch.page(..., nogloss=True)`) — glossing
`<title>` corrupted the browser tab caption, and the cover's contents list was
claiming words the dialogue should get. Both silently spent first-occurrences
before the reading text was reached. The PDF is
unaffected (`@media print`), and its word count is a good regression check.
Debugging the tooltip in a browser: do **not** set `document.documentElement.
style.zoom` — CSS zoom desyncs `getBoundingClientRect()` from absolute
`top`/`left`, and the tip appears to land hundreds of px away. That is the zoom,
not the code.

**Spinner cards need a restart.** `~/.claude/dutch-tips.json` is read once per CLI
process, so after `make_cards.py` you must restart Claude Code to see new cards.

**Chrome headless** at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
does the PDF rendering. It emits `CVDisplayLinkCreateWithCGDisplay` errors on
stderr — harmless, ignore them.

**Dependencies.** `extract_source.py` needs numpy, which is not in the system
Python (PEP 668). Use a venv with `--system-site-packages`, or
`pip install --break-system-packages numpy`. Also needs tesseract with the `nld`
pack. `build.py` needs PyMuPDF (already present).

---

## Rules

- **Transcribe, never invent.** Every word must match the book. Read the cleaned
  scan images; `scan-text.txt` is an OCR draft with real errors (`naarde`,
  `jüj/je`, lone `I` → `[`). Verify counts against the original.
- **Never change `book/shared/lib/art_style.py`.** The fixed, shared style preamble
  is what makes eighteen chapters look like one book. Changing it means
  regenerating every chapter's art.
- **Never mention text, letters or numbers in an art prompt.** Models render
  letterforms unreliably. All type on the page is real vector text from
  `content.py`. Every prompt already ends with that ban — keep it.
- **Keys live in `.env` at the project root** (chmod 600, gitignored) and load
  automatically. Never commit it, never print a key into the transcript, and never
  copy one into a second file — `.env` is the only place they exist on disk.
- **Never recast a recurring character.** `shared/lib/voices.py` is the cast for
  all eighteen chapters; the teacher must always sound like the teacher. Same
  reasoning as `art_style.py`.
- **Audio text must match `content.py` word for word.** It is the book read
  aloud, not a paraphrase. Numbers and postcodes are spelled out in words in
  `audio_script.py` so the model reads them as Dutch, not as digits.
- **Verify before claiming done.** `build.py` checks three things and exits 1 on
  any: content past the trim (`overflow`), a `keep()` block landing on two pages
  (`keep-blocks`), and a page mixing two sections (`section mix`). It also prints
  a `glossary` line — *N first occurrences marked, M introduced earlier, K
  headwords*. Not a failure, but the numbers should only ever grow as chapters are
  added; a drop means an earlier chapter changed and took the words with it.
  All three checks are structural: they cannot see ugliness, a page that opens
  mid-thought, a list reading the wrong direction, or half a page of white space.
  So also look at the output — **both** outputs. Render a few PDF pages to images,
  *and* open `index.html` in a browser. They are not the same document: for three
  chapters every page sat flush against the left edge of the browser window with
  all the slack on the right, because verification only ever went through the PDF,
  where `@page` hid the missing `margin:0 auto`.
  Layout bugs found this way in ch1: a clipped cover lockup, a vocabulary grid
  flowing the wrong direction, a form running off the trim, and a dialogue
  split across a page turn that no automated check would have caught before the
  keep rule existed.
- **Compare against the original when paginating.** Open the matching page of
  `source/scan-cleaned.pdf`. If the book keeps something whole, keep it whole.
- Don't publish any of this to a web artifact. It's a copyrighted textbook;
  personal use, local files only.

---

## Layout conventions

- Trim 170 × 240 mm. Page 1 is a full-bleed cover:
  `ch.page(..., variant="bleed", head=False, foot=False, nogloss=True)`.
  `nogloss` keeps the contents list from claiming a word's first occurrence.
- **`index.html` and the PDF are laid out by different rules.** `@page` sizes the
  sheet in print; on screen a `.page` is just a fixed 170 mm block, so without
  `margin:0 auto` it pins to the left edge and dumps all the slack on the right.
  The `@media screen` block at the foot of `style.css` centres the sheets on a
  `--desk` backdrop. Anything screen-only belongs in that block — never touch the
  shared rules to fix something you only saw in the browser. Chrome caches
  `../shared/style.css` hard: after editing it, reload with cache disabled, or you
  will be measuring the old stylesheet.
- Content must end above **877 px** (240 mm at 96 dpi, minus footer). In ch1 the
  fullest page sits at 822.
- A 10–12-page original becomes 20–25 redesigned pages (ch1 20, ch2 25, ch3 20). Don't cram — the original's
  worst trait was density. Pages at 60–70% full are fine — but 25–45% is a fault
  in the other direction: ch3 first came out with the word list split 26/25 and
  Rangtelwoorden filling a quarter of a page. Consolidating took it 22 → 20 pages
  with nothing thin. Measure the fill before shipping. **But giving a section
  more room never means cutting a block in half.** Spread *between* units, never
  *through* one. Over-applying "don't cram" once split the chapter-1 dialogue
  across two pages, so page 3 opened mid-conversation with no heading.
- **Wrap every indivisible block in `keep("name", …)`** — a dialogue, a
  conjugation table, an exercise together with its items, a form. `build.py`
  fails the build if a keep-block lands on more than one page. Names must be
  unique per chapter (`dialoog-1.1`, `opdracht-2`, `woordenlijst-a/-b`).
  If a keep-block won't fit, move something else off the page — shrink or
  relocate an illustration — rather than slicing the block.
- **A page continues one section or starts a new one, never both.** An exercise
  sitting above a section heading has nothing telling the reader which section it
  belongs to. `build.py` fails on this (`section mix`). This happened in ch1:
  §1.5's Opdracht 4–5 ended up above §1.6's heading, so the page opened with two
  exercises that looked like they belonged to the alphabet.
- **Keep a section with its own exercises** where they fit. A page that merely
  *continues* one section without a heading is fine — the running head labels it,
  which is what the original does for its own word-list spill. Mixing two sections
  is not.
- Reuse the helpers in `book/shared/lib/layout.py` — `card`, `task`, `qa`,
  `vocab_rows`, `pairs`, `numbers`, `number_columns`, `lines`, `icon`,
  `audio_icon`, `keep`, `clock` — rather than raw HTML. `clock(hour, minute,
  label)` draws an SVG clock face: ch2 teaches telling the time, and a drawn
  face puts the hands exactly where the text says, which generated art cannot.
- Anything the original marks with a speaker icon gets `audio_icon("audio/x.mp3")`,
  or `task(..., audio="audio/x.mp3")` for an Opdracht. It plays inline in
  `index.html` and is a clickable link in the PDF — same markup, both outputs.
- **Every multi-column list reads top-to-bottom per column, never across.** A CSS
  grid fills rows first by default, which silently destroys the grouping. This bit
  twice in ch1: the word list (fixed with `vocab_rows`) and then the numerals,
  which came out 0,1,2 / 3,4,5 across instead of the original's units | teens |
  tens columns — so the *-tien* and *-tig* patterns no longer lined up, which is
  the only reason to print them in columns at all. Use `vocab_rows` and
  `number_columns`; if you build a new multi-column list, check the reading
  direction against the scan before shipping.
- **The practice deck is generated, never hand-written.** `shared/lib/cloze.py`
  reads the chapter, `build.py` emits the cards as JSON into `index.html`, and
  `shared/flashcards.js` runs them. The panel is placed automatically straight
  after the last page holding a `.vocab` table — below the word list, in the flow
  of the chapter. It is **not** a `.page`: screen-only furniture, invisible to the
  PDF and to build.py's page checks.
- **The deck is the Woordenlijst and nothing else.** `VOC` is the word list the
  book prints under "§N.2 Woordenlijst"; it is the only list rendered with
  `vocab_rows()`, and the only source of cards. Do NOT pull cards out of the other
  lists in content.py — countries, verb tables, the clock, possessives, numerals,
  greetings, family words. Those belong to teaching sections, and turning them into
  cards produced fronts like "Ik kom uit China." that ask no question, and a
  country card whose two halves were unrelated table columns. If the deck looks
  thin, that is what the chapter teaches; adding material from elsewhere is not the
  fix. `build.py` reports "N cards from M Woordenlijst entries" so the two numbers
  can be compared at a glance.
- **The word list prints some words twice.** ch1 has *jullie = your (plural)* and
  *jullie = you (plural)*; ch2 has *nog = any* and *nog = as well*. One word gets
  one card with the meanings merged — an earlier dedup silently dropped the second
  entry, losing a meaning the book teaches.
- Cloze sentences are lifted from the chapter's own prose, never written for the
  card. A word the book never uses in running text gets recognition only.
- **`flashcards.js` is linked, not inlined.** That is the whole point of the
  component — edit it once and all eighteen chapters change on reload, with no
  rebuild. Only new *cards* need `build.py`. Don't inline it "for convenience".
- **The cards speak with the browser, not ElevenLabs.** `flashcards.js` uses
  `speechSynthesis`, preferring a *local* nl-NL voice (macOS ships Xander) over a
  network one, and nl-BE last — this book teaches Netherlands Dutch. That means no
  clips to generate, nothing to ship, and chapter 18 speaks the day it is written.
  ElevenLabs still does the **page** audio (dialogues, Opdracht recordings); only
  the cards changed. Speech never fires before the reader clicks, and never speaks
  an answer that is still hidden — a produce card is silent until it is revealed.
- **The quoted sentence gets one English translation, in `<chapter>/translations.py`.**
  This is the ONLY text in the project that is not the book's: the book prints no
  English for its dialogue, so these are written for the cards. That is why they
  live outside `content.py` — the boundary between "the book" and "written for
  this project" has to stay visible. Show the sentence translated whole; a
  word-by-word gloss was tried and is not what reading practice needs.
  `build.py` lists any sentence with no entry and **exits 1** — never invent one
  at render time, and never let a card reveal a sentence with no meaning.
- **Recognition flips, production types.** A flashcard that makes you type the
  English is a spelling test in the wrong language. Flip and self-grade for
  recognition; typing is reserved for producing Dutch, where the article and the
  spelling are the point. A `produce` card whose answer runs past two words flips
  too — typing "Nee, ik kom uit Hongarije." tests typing, not recall.
- Progress lives in `localStorage` under `nl-deck-v1` and is the **only** copy —
  `practice.py` no longer owns it. The component re-reads before every round so two
  chapter tabs can't clobber each other, and falls back to memory (saying so on the
  summary screen) if storage is blocked, which Chrome does on some `file://` setups.
- Vocabulary: infinitive small and grey after the stem.
- Set `ch.toc` in `pages.py` — `build.py` turns it into PDF bookmarks.

---

## Chapter index (book pages)

| # | Title | Pages | | # | Title | Pages |
|---|---|---|---|---|---|---|
| 1 | Welkom | 20–31 ✅ | | 10 | Bij de fietsenmaker | 142–155 |
| 2 | In de kantine | 32–45 ✅ | | 11 | Op een verjaardag | 158–171 |
| 3 | In het café | 46–57 ✅ | | 12 | Naar de Evenementenhal | 172–181 |
| 4 | Op straat | 58–67 | | 13 | Bij vrienden | 182–193 |
| 5 | Op de markt | 70–83 | | 14 | In de sportschool | 194–207 |
| 6 | In een restaurant | 84–95 | | 15 | In de trein | 208–221 |
| 7 | In een kledingzaak | 96–109 | | 16 | Naar de bioscoop | 222–231 |
| 8 | Bij de makelaar | 110–125 | | 17 | Thuis | 234–249 |
| 9 | Bij de huisarts | 126–141 | | 18 | Bij de politie | 250–260 |

Standalone *Taalbiografie* pages sit at 68, 156 and 232 — not part of any chapter.
Appendices run 261–310 (2 = grammar overview, 3 = irregular verbs, 8 = answer key).

Every chapter follows the same shape: Dialoog → Woordenlijst → numbered sections
with Opdrachten → Tekst → Uitspraak → Cultuur → In de praktijk → Eigen vocabulaire
→ Reflectie.

---

## Studying while you wait

`make_cards.py` turns every chapter's `content.py` into flashcards that replace the
Claude Code spinner tips (`spinnerTipsOverride` in `~/.claude/settings.json`), and
`practice.py` is a Leitner trainer. `autostudy.py` opens that trainer in an iTerm2
split pane automatically once Claude has been busy 25s, and closes it the moment
Claude finishes or needs input — wired through hooks that sit alongside the user's
existing `cc-status` hooks. Kill switch: `python3 book/autostudy.py disable`.

All three grow automatically as chapters are added. Details in `book/README.md`.

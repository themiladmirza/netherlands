# Nederlands in gang — redesigned chapters

Redesigning chapters of *Nederlands in gang* (Coutinho, 3rd revised edition 2017)
from the scan in `hard.pdf` into properly typeset PDFs with original illustrations.
Personal study material, made alongside an owned copy of the book.

Chapters 1–3 are done: ch1 20 pages (10 illustrations, 4 audio), ch2 24 pages
(7 illustrations, 2 audio), ch3 20 pages (6 illustrations, 3 audio). The usual job
in a new session is **"do chapter N"** — treat those as the reference for what
finished looks like; `ch03-in-the-cafe/pages.py` is the cleanest model to copy.

- `book/README.md` — how the system works (tools, outputs, deck, audio, glossing)
- `book/LESSONS.md` — **why** each rule below exists: the incident and the numbers.
  Read the matching section before overriding a rule.
- `book/ch<NN>-<slug>/NOTES.md` — decisions specific to one chapter

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

When in doubt: is this the exercise, or is it telling me how to do the exercise?

---

## Workflow for a new chapter

```bash
# 1. scaffold            number, Dutch title (printed), English slug (folder)
python3 book/new_chapter.py 4 "Op straat" on-the-street

# 2. pull the source out of the scan: chapter folder, first & last BOOK page
python3 book/extract_source.py ch04-on-the-street 58 67
#    -> source/scan-cleaned.pdf + source/scan-text.txt

# 3. transcribe into content.py  (read the cleaned scan; OCR is a draft, not truth)

# 4. describe the illustrations in art_prompts.py, then
python3 book/generate_art.py ch04-on-the-street

# 5. write audio_script.py (what is spoken, by whom, with which emotion tags), then
python3 book/generate_audio.py ch04-on-the-street

# 6. lay out pages.py with the layout.py helpers, then build
python3 book/build.py ch04-on-the-street

# 7. card sentences: write translations.py (build lists what is missing), then
python3 book/generate_audio.py ch04-on-the-street --cards
python3 book/make_cards.py

# 8. look at BOTH outputs — serve from book/, never from the chapter folder,
#    or ../shared/style.css 404s and you measure an unstyled page
python3 -m http.server 8000 --directory book
```

Refactoring `pages.py`, `layout.py` or `style.css`? Commit first, then
`build.py <chapter> --compare` — it fails unless every PDF page is pixel-identical
to HEAD and `index.html` matches.

Both API keys load from `.env` automatically (`shared/lib/env.py`).

---

## What build.py enforces (exit 1 on any)

overflow past the trim · a `keep()` block split across pages · a page mixing two
sections · a bookmark not on its page · an answer not placed on its question (or
its Opdracht missing) · a `content.py` name in neither `cloze.PROSE` nor
`cloze.NOT_PROSE` · a card sentence without a translation · a cloze whose answer is
not the removed text · Chrome returning no layout result.

It also prints a `glossary` line and a searchable word count. Neither fails, but
the glossary numbers should only grow as chapters are added, and the word count
must not move when only screen-only code changed (a jump means it leaked into the
PDF).

**All of these are structural.** They cannot see ugliness, a page opening
mid-thought, a list reading the wrong way, or half a page of white space. Look at
both outputs: render PDF pages to images *and* open `index.html` in a browser.

---

## Rules

**Content**
- **Transcribe, never invent — including whole sections.** The test is "is it on
  the page", not "is it accurate". Before shipping, list every heading and `card()`
  title and check each against the scan; an English card title is the tell.
- `scan-text.txt` is an OCR draft with real errors. Read the cleaned scan images.
- Colour-only cues are lost in the greyscale scan, and its apparent **bold** is
  not the book's emphasis. Reconstruct on grammatical grounds, note it in NOTES.md,
  flag it for a spot-check.
- Some listening exercises never print their words (ch2 Opdr 15, ch3 Opdr 12).
  Keep the exercise and grid, leave the icon inert, record nothing.
- Most exercises have no answer in Bijlage 8. Leave them with none — no placeholder.
- Drawn aids (`clock()`, `timeline()`) show only pairings the book states.

**Art**
- Never change `book/shared/lib/art_style.py` — it is what makes 18 chapters one book.
- Never mention text, letters or numbers in an art prompt. Every prompt ends with that ban.

**Audio**
- Audio text matches `content.py` word for word; numbers spelled out as Dutch words.
- Never recast a recurring character (`shared/lib/voices.py`). Check a new voice's
  clarity first: energy above 8 kHz vs full band; past about -30 dB is muffled.
- Dialogues: `eleven_v4` with `"gap": 0.45`. Lists of short tokens (the alphabet):
  `eleven_v3`, and diff the transcript word by word.
- Emotion tags: at most about four words, keeping the one direction that matters.
  Don't re-record a working take just to shorten a tag.
- Never judge a take by its match score alone — diff the words, check the FIRST
  word for a leaked tag, re-run before believing a low score, and listen.

**Layout**
- Trim 170 × 240 mm; content ends above **877 px**. 10–12 book pages become about
  20–25. Pages 60–70% full are fine, 25–45% is a fault — but spread space
  *between* blocks, never through one.
- Wrap every indivisible block in `keep("unique-name", …)`. If it won't fit, move
  something else off the page.
- A page continues one section or starts a new one, never both. Keep a section
  with its own exercises where they fit.
- Every multi-column list reads top-to-bottom per column (`vocab_rows`,
  `number_columns`, `word_columns`). Check reading direction against the scan.
- Compose pages from `layout.py` helpers (`sec`, `phrases`, `items`, `blanks`,
  `lettered`, `term_grid`, `word_columns`, `tick_table`, `ch.cover()`,
  `ch.eigen_vocabulaire()`, `ch.reflectie()`, …). Raw HTML only for one-offs.
- Bookmarks: `ch.page(..., toc=[(level, label)])` — never type page numbers.
- Anything the book marks with a speaker icon gets `audio_icon(...)` or
  `task(..., audio=...)`. Vocabulary: infinitive small and grey after the stem.
- Screen-only fixes go in the `@media screen` block at the foot of `style.css`.
- Runtime-built UI (deck, answers): `display:none` outside every media query, then
  reveal inside `@media screen`. Never the reverse, or it prints.

**Deck and answers**
- The deck is the Woordenlijst (`VOC`) and nothing else. One word, one card;
  duplicate headwords merge their meanings.
- Cloze sentences are lifted from the chapter's prose, never written. A cloze is
  answered with the removed text (`card.blank`), not the headword.
- `translations.py` is the ONLY non-book text: whole-sentence English, kept out of
  `content.py`. Never invent one at render time.
- Recognition flips, production types (and flips past two words).
- `flashcards.js` and `answers.js` are linked, not inlined.
- Answers come from Bijlage 8 (`answers.py`) and land ON the question;
  `answers.js` knows the shapes. A new shape fails the build — teach `answers.js`
  the shape rather than falling back to a block.

**Housekeeping**
- Keys live only in `.env` (chmod 600, gitignored). Never commit, print or copy one.
- Use Python, not `sed`, for token renames — macOS `sed` has no `\b`.
- Don't publish any of this to a web artifact. It's a copyrighted textbook;
  personal use, local files only.

---

## Things that will bite you

- **`hard.pdf`**: book page = PDF page + 1. Each page has a CropBox selecting one
  page of the spread; the Read tool ignores it and shows the spread *twice* — not
  duplication. Read needs `pages:` (max 20). No text layer (MRC scan, 200 dpi ceiling).
- **Bijlage 8 pages** carry `/Rotate 90`: render with `get_pixmap(dpi=N)` and **no
  `clip`**, or you silently get half a page.
- **Chrome headless** (`/Applications/Google Chrome.app/...`) prints
  `CVDisplayLinkCreateWithCGDisplay` errors — harmless. It caches
  `../shared/style.css` hard: reload with cache disabled after editing it.
- **Don't set `document.documentElement.style.zoom`** while debugging the
  tooltip — it desyncs `getBoundingClientRect()` and the tip appears misplaced.
- **Image API: 5 per minute.** `generate_art.py` waits and retries.
- **Spinner cards** are read once per CLI process — restart after `make_cards.py`.
- **numpy** isn't in the system Python (PEP 668): venv with
  `--system-site-packages`, or `pip install --break-system-packages numpy`.
  `extract_source.py` also needs tesseract with `nld`.

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
Appendices run 261–319: 1 = CEFR checklist, 2 = grammar overview, 3 = irregular
verbs, 4 = sources, 6 = map, 7 = Register (thematic word list, 296–309),
**8 = Antwoorden bij de opdrachten, 310 to the end** — selective: ch1 answers
Opdracht 2, 3; ch2 1, 3, 4, 10, 13; ch3 1, 5, 6, 10. (The key runs in two
columns per page; a heading at the top of the right column usually continues the
previous chapter — ch2's Opdracht 13 was once misread as ch1's.) *Mogelijke antwoorden* is a
sample, not the answer.

Every chapter follows the same shape: Dialoog → Woordenlijst → numbered sections
with Opdrachten → Tekst → Uitspraak → Cultuur → In de praktijk → Eigen vocabulaire
→ Reflectie.

---

## Studying while you wait

`make_cards.py` → Claude Code spinner tips; `practice.py` → terminal Leitner
trainer; `autostudy.py` opens it in an iTerm2 split after 25 s of Claude being busy
(kill switch: `python3 book/autostudy.py disable`). Details in `book/README.md`.

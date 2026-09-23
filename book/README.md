# Nederlands in gang — redesigned

Chapters of *Nederlands in gang* (Berna de Boer, Margaret van der Kamp,
Birgit Lijmbach — Uitgeverij Coutinho, 3rd revised edition 2017), redesigned and
typeset from scratch as real vector type, with original illustrations.

Personal study material, made alongside an owned copy of the book.

Everything structural is in English. Everything Dutch is *content* — the chapter
text, the words on the page, the titles printed in the PDF.

---

## Layout

    book/
    ├── build.py            build one chapter into a PDF
    ├── generate_art.py     generate a chapter's illustrations
    ├── new_chapter.py      scaffold a new chapter folder
    ├── make_cards.py       build study cards from the chapters
    ├── practice.py         flashcard trainer
    │
    ├── shared/             ← one source of truth for the whole series
    │   ├── style.css       design system: palette, type, components
    │   ├── fonts/          Bricolage Grotesque + Source Sans 3 (SIL OFL)
    │   └── lib/
    │       ├── layout.py   Chapter + building blocks (card, task, vocab_rows, …)
    │       └── art_style.py shared illustration preamble + model choice
    │
    ├── _template/          empty chapter to copy from
    │
    └── ch01-welcome/       ← one folder per chapter
        ├── content.py      all of the chapter's text
        ├── pages.py        page composition + bookmarks
        ├── art_prompts.py  the prompts that produced art/
        ├── art/            the illustrations (PNG)
        ├── cards.json      generated study cards
        ├── index.html      generated — do not hand-edit
        ├── ch01-welcome.pdf the finished chapter
        ├── NOTES.md        decisions specific to this chapter
        └── source/         the scan this redesign was based on

**Why `shared/` is separate:** palette, typography and illustration style should
have a single source. Change `style.css` or `art_style.py` and the whole series
follows — that is what keeps eighteen chapters looking like one book. Only what
genuinely differs per chapter (text, layout, art) lives in the chapter folder.

Folder names are `ch<NN>-<english-slug>`; the Dutch title the book actually
prints is set in `pages.py` (`Chapter(1, "Welkom")`).

---

## Building a chapter

    python3 book/build.py ch01-welcome

Runs `pages.py` → `index.html` → Chrome print-to-pdf → bookmarks and metadata,
then checks every page for content spilling past the trim and reports `OVERFLOW`
if it finds any.

Trim size 170 × 240 mm. Text stays real vector (sharp at any zoom) and searchable.

## Generating illustrations

    export OPENAI_API_KEY=sk-...
    python3 book/generate_art.py ch01-welcome         # only what's missing
    python3 book/generate_art.py ch01-welcome --all   # everything again

Model: `gpt-image-2.5-flare`, quality `high` (see `shared/lib/art_style.py`).
Tested against `gpt-image-2.5-sunburst` and `gpt-image-2`; flare is flatter and
more graphic, and stays more consistent across a whole chapter.

Two rules do most of the work:

1. **The style preamble is fixed and shared.** Only the scene differs per image.
   That is why the illustrations read as one series.
2. **Never text in the image.** Every prompt ends with a ban on letters and
   numbers — models render them unreliably. All type on the page is real vector
   text from `content.py`.

The API allows **5 images per minute**. The script catches the limit, waits 35 s
and retries (up to six times per image).

## A new chapter

    python3 book/new_chapter.py 2 "In de kantine" in-the-canteen

Creates `ch02-in-the-canteen/` from `_template/` with the number and title filled
in. Then: text into `content.py`, scenes into `art_prompts.py`, `generate_art.py`,
layout in `pages.py`, `build.py`.

---

## Design system (`shared/style.css`)

| | |
|---|---|
| Paper | `#FDFAF4` warm cream |
| Ink | `#1E2A2E` |
| Orange | `#E8632A` — chapter numbers, tasks, accents |
| Deep teal | `#14616B` — translations, table heads, page numbers |
| Mustard / coral / sage | `#E9B44C` `#F2A08A` `#9CB29B` |
| Display | Bricolage Grotesque 300–800 |
| Body | Source Sans 3 300–900 (latin-ext, for ë ï é) |

Components: `.card` reference card · `.task` exercise block with a skill icon
(speak / write / read / audio / web) · `.vocab` word list · `.grid` table ·
`.numbers` numeral chips · `.alpha` alphabet tiles · `.form` fill-in form ·
`.dialogue` dialogue · `.example` example box · `.dutch` Dutch term.

Page numbers appear as digits *and* Dutch words (`zes | 6`) — that idea comes
from the original and is worth keeping.

## Source material

`hard.pdf` in the project root is the scan of the whole book (318 pp.).

Each chapter keeps what the redesign was based on in `source/`:

    ch01-welcome/source/
    ├── scan-cleaned.pdf   this chapter's scan, cleaned up + OCR
    └── scan-text.txt      the OCR text, to lift into content.py

The cleaned scan was made from `hard.pdf`: edge streaks removed, bleed-through
filtered out of the tinted boxes, tints flattened again, OCR in Dutch + English.
Handy as a reference next to the redesign.

---

## Studying Dutch while you wait

Two things, both fed by the same `content.py` files.

### 1. Spinner cards (passive, automatic)

While Claude Code works, tips rotate in the spinner. Those are replaced with
words from this book — exactly where you are already looking.

    python3 book/make_cards.py        # -> ~/.claude/dutch-tips.json

In `~/.claude/settings.json`:

    "spinnerTipsEnabled": true,
    "spinnerTipsOverride": {
      "tipsFile": "~/.claude/dutch-tips.json",
      "excludeDefault": true,
      "label": "NL"
    }

Set `excludeDefault: false` to mix Claude Code's own tips back in. The file is
read once per session, so restart Claude Code after running `make_cards.py`.

### 2. Vocabulary cards in the chapter itself (the main trainer)

Open any chapter's `index.html` and scroll to **Woorden oefenen**, straight below
the word list. Screen only — the PDF never contains it.

Every card is one entry of that chapter's **Woordenlijst** — nothing else in the
book becomes a card:

| chapter | Woordenlijst entries | cards |
|---|---|---|
| 1 | 89 | 86 |
| 2 | 76 | 75 |
| 3 | 51 | 51 |

The small differences are honest: `waar … vandaan` is discontinuous and cannot be
blanked, and a few words the book lists twice with different meanings become one
card carrying both (*jullie — your (plural) / you (plural)*).

You see the Dutch word with a sentence from the chapter, try to recall it, flip,
and grade yourself *Nog niet* / *Gewust*.

Once a translate card reaches box 3, it unlocks a **production** card: the same
sentence with the word blanked out, and you type the Dutch. That is where typing
earns its keep — nouns keep their article, so `de verjaardag` is also the de/het
drill and `verjaardag` alone is marked wrong. A one-character slip counts as close.

Recognition flips rather than types on purpose: making you spell the *English* for
a Dutch word tests the wrong language. Typing is reserved for producing Dutch.

When you reveal a card you get the word's meaning **and** the sentence's meaning:

    de naam
    Wat is jouw naam?
    name
    What is your name?

Those sentence translations are the one thing here that is not the book's — the
book prints no English for its dialogue — so they live in
`<chapter>/translations.py`, separate from `content.py`. Correct any that read
wrong; nothing else depends on the wording. `build.py` fails if a quoted sentence
has no translation.

Pronunciation comes from the browser's own Dutch voice (macOS: Xander), so there
are no audio files to generate. Press **▶ uitspraak** to hear it again. Nothing is
spoken before you interact with the card, and a card never speaks an answer you
have not revealed yet.

Keys: space flips, 1 = nog niet, 2 = gewust, enter checks and advances.

Leitner boxes 1–5 (0 / 1 / 3 / 7 / 21 days). Progress lives in the browser under
`localStorage["nl-deck-v1"]` and is the only copy — serve the pages over HTTP
(`python3 -m http.server --directory book`) rather than opening them as `file://`,
where Chrome may refuse to keep it. The panel says so if that happens.

Cards come from `shared/lib/cloze.py`. To include a new chapter's lists, add them
to its `LISTS` table; nothing else needs changing.

### 3. Terminal trainer (`practice.py`)

Still here for a second pane next to Claude, but it keeps its own separate
progress file — the browser deck above is where review state now lives.

    python3 book/practice.py                    # whatever is due
    python3 book/practice.py --chapter 1
    python3 book/practice.py --direction en-nl
    python3 book/practice.py --kind number
    python3 book/practice.py --stats            # progress only

Leitner boxes 1–5 (0 / 1 / 3 / 7 / 21 days). Progress in
`~/.claude/dutch-progress.json`. Keys: enter = reveal · y/n · q = quit.

Cards come from every chapter at once: add chapter 2 and both streams grow
with it.

### 4. Automatic practice pane (hands-off)

`autostudy.py` makes the trainer appear on its own while Claude Code is busy and
disappear the moment it isn't.

    Claude starts working
      └─ 25s later ─> iTerm2 splits, practice.py opens on the right, focused
    Claude finishes, or needs you (permission prompt / question)
      └─ pane closes, focus snaps back to Claude

Wired through hooks in `~/.claude/settings.json`, appended next to any hooks you
already have:

| event | action |
|---|---|
| `UserPromptSubmit`, `PreToolUse` | `autostudy.py start` — mark busy, ensure a watcher |
| `Stop`, `StopFailure`, `Notification`, `PermissionRequest`, `SessionEnd` | `autostudy.py stop` — unmark, close pane |

All hooks are `async: true`, so they never block a tool call.

Nothing tells us in advance that a tool will be slow, so there is no prediction —
a detached watcher polls the busy marker and only opens the pane once Claude has
been busy past the threshold. Short calls never reach it.

    python3 book/autostudy.py status     # what it thinks is happening
    python3 book/autostudy.py disable    # kill switch, survives restarts
    python3 book/autostudy.py enable
    AUTOSTUDY_DELAY=10 …                 # change the threshold (default 25s)

Only acts inside iTerm2 — in plain Terminal, over ssh or in CI it is a no-op.
Every entry point is wrapped so a failure can never break a Claude session.

---

## Audio

Every audio icon in a chapter is clickable. In the browser (`index.html`) it plays
inline; in the PDF it is a link annotation that opens the file in your player.
Both come from the same markup — an `<a href>` the page's script intercepts.

The key loads from `.env` automatically; export one only to override it.

    python3 book/generate_audio.py ch01-welcome          # only what's missing
    python3 book/generate_audio.py ch01-welcome --all    # everything again
    python3 book/generate_audio.py ch01-welcome --check  # verify existing files

`<chapter>/audio_script.py` holds what is spoken, by whom, with what delivery.
`shared/lib/voices.py` holds the cast — keep a character on one voice across all
eighteen chapters so the teacher always sounds like the teacher.

**Emotion tags.** The model is `eleven_v3`, the one that interprets tags: writing
`[warmly] Goedemorgen` shapes the delivery and is not read aloud (verified —
tagged and untagged renders come out the same length). Tags are chosen to fit the
moment: the teacher opens warmly, Ning politely corrects a misheard house number,
the teacher laughs off the formal *u*. In the zinsaccent drill every answer is a
contrastive correction, so the answers are tagged emphatic — that stress pattern
is the whole point of the exercise.

**Verification.** Each file is transcribed back with speech-to-text and compared
to its script with the tags stripped. Chapter 1 scores 99 / 99 / 100 / 89 %; the
89 % is spelling noise (`t w` heard as `tw`, `Sara` as `Sarah`), not bad audio.
This catches mangled Dutch or a tag being read aloud — it cannot catch a merely
ugly read, so listen before shipping a chapter.

Chapter 1 audio: dialogue 1:38 · numbers 0:48 · alphabet 0:31 · zinsaccent 0:42.

---

## Hover translations

The word lists carry translations, but a learner meeting a word in the *running
text* has nowhere to look it up. So the **first occurrence of every glossary word
— first in the book as a whole, not first in its chapter** — is underlined with a
fine dotted rule in `index.html` and shows its English on hover.

Applied automatically by `build.py`; no separate command. To work out what counts
as "first", it generates every earlier chapter in Python (no Chrome) purely to
learn which words are already spoken for, so a single-chapter rebuild gives the
same answer as a full rebuild. The build reports it:

    glossary  : 68 first occurrences marked (94 already introduced earlier, 253 headwords)

**Not glossed:** the word lists themselves (they *are* the translation), running
heads, page footers, `<title>`, and the **cover**. The cover's objectives list is
a contents page; letting it claim a word's first occurrence robbed the dialogue —
where the learner actually meets the word in a sentence — of the tooltip. Covers
opt out explicitly with `ch.page(..., nogloss=True)`, so a future chapter can
exclude any page the same way.

**A "de X" entry also matches the bare noun.** The running text says *je
verjaardag*, never *de verjaardag*; both spellings share one entry, so the word
is marked once whichever form appears first, and the tip shows the headword as
the book prints it — *de verjaardag · birthday*.

**The PDF is untouched.** `@media print` drops the underline and the tip, and the
searchable word count is identical to before glossing — verified.

Only two entries are never marked: `geeft les` and `komen op bezoek`, which the
text always splits (*"Hij geeft twee dagen les"*), so they never occur as a
contiguous phrase.

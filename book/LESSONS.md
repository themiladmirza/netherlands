# Lessons — why the rules are what they are

The long form of the rules in `/CLAUDE.md`: what went wrong, how it was found,
and what the measurement said. CLAUDE.md keeps the rule; this file keeps the
reason, so the rule can be judged when a new case doesn't quite fit.

Moved here from CLAUDE.md on 2026-10-08, nearly verbatim.

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

**Audio: emotion tags need v3 or v4.** On the older models `[warmly]` risks
being read aloud. Verified on both v3 and v4: the tag is acted on, never spoken.

**Dialogues use `eleven_v4` with `"gap": 0.45`.** v4 reads a conversation far more
naturally than v3 — the user's words were "much more real" — but it runs the turns
together: 0.29 s of silence between speakers against v3's 0.69 s, too quick to
follow. `pad_gaps()` lengthens each silence after generation, so v4's delivery is
untouched and only the pacing changes. Gaps are *extended*, not normalised, so a
thinking pause stays longer than a quick "Ja, graag". All three chapters now land
near 0.7 s.

**The audio metrics cannot hear whether a voice sounds real.** Energy above 8 kHz
and words-per-minute said v3 won on chapter 3's dialogue, and listening said the
opposite, emphatically. Those numbers catch a *broken* take — a duplicated run of
letters, a swallowed word — and nothing about naturalness. Use them to reject, never
to choose: for anything a learner listens to, play both.

**`eleven_v4` is high-variance on letter recitation — take the best of N.** v4
does Dutch, costs the same as v3, honours `[emotion]` tags (verified: not read
aloud) and works on `/v1/text-to-dialogue`. Chapter 1 runs entirely on it, pinned
per item: `audio_script.py` entries carry `"model"`, and `generate_audio.py` takes
`--model`.

The catch is variance on letter recitation. Across **six** v4 takes of the
alphabet — two voices, best-of-N each — every one duplicated a run of letters
("A B C D E F G A B C D E F G…"). v3 rendered the same script at 100% on three
takes out of three, with the digraph names right. So `alfabet` stays on v3 while
the rest of chapter 1 is v4. The clarity gain came from the *voice*, not the
model: v3 with the new teacher measures -16.3 dB against v4's -16.8. When a
track is a list of short tokens, prefer v3 and diff the transcript.

**The move to v4 everywhere (2026-10-08).** v4 became the default. The four tracks
still on v3 — all lists of short tokens — got three v4 takes each, every take
transcribed and diffed word by word against the script:

| track | v3 (kept as reference) | v4, 3 takes | decision |
|---|---|---|---|
| ch2 `opdracht16` (a/aa words) | 30/30 | 30/30 ×3 | v4 |
| ch3 `opdracht13` (o/oo words) | 30/30 | 30/30 ×3 | v4 |
| ch3 `opdracht11` (word stress) | 18/18 | 17/18 ×3 — *pauze* missing | v3 |
| ch1 `alfabet` | 38/38 | one duplicated "a…g", two complete | v4 take 2, approved by ear |

*pauze* was not a transcription miss: word timestamps put 0.65 s between
"adres" and "familie", the same as every other gap, so the word was never
spoken. Three of three is a pattern, not noise. The alphabet's complete takes
still hit the ij / y blind spot below, so take 2 was played to the user before
adoption — it passed.

**Do not judge a take by the match score alone** — it called a broken alphabet
"ok" at 87%. Diff the transcript against the script word by word. Doing that
overturned two conclusions drawn from scores: the v4 dialogue looked like it had
dropped ~54 characters, but all 197 words are present and the gap is STT writing
*Suzy* for *Susy* and digits for spelled-out numbers (`tweeëntwintig` → "22",
`drieëndertig eenentachtig T W` → "3381 TW"). And the alphabet's remaining
mismatch is `ij` transcribed as "y", which proves nothing: Dutch *ij* and *y* are
pronounced the same, so STT cannot separate them. That one needs an ear.

**Keep emotion tags short on word-list items — a long one gets read aloud.**
ch2's Opdracht 16 carried a fifteen-word tag, *[clearly and slowly, leaving a
pause after every word, contrasting the short and long a]*. v3 voiced its tail:
all six takes measured opened with an English fragment ("Contrast", "De short en
lang"), and several also swallowed the first Dutch word. Cutting it to `[slowly]`
removed the leak in 3 of 3 takes.

**Cap a tag at about four words, keeping the one direction that matters** — not a
blanket `[slowly]`. ch3's Opdracht 11 is *about* word stress, so its tag is
`[stressing each accent]`; flattening that would have stripped the exercise's
whole point. A bracketed cue is a cue; fifteen words inside brackets is prose, and
the model sometimes reads prose.

Long tags do not fail reliably, which is the trap: ch3's Opdracht 13 carried a tag
as long as the broken one and recorded clean every time. So **do not re-record a
working take just to apply a shorter tag** — shorten it and let it take effect the
next time that item is generated for some other reason. Chapter 1's alphabet keeps
its twelve-word tag outright: that take verifies at 100% on the most
failure-prone content in the book, and a re-roll came back at 99%.

Check the FIRST word of a new recording specifically — a leaked tag sits in front
of the content, where a similarity score barely notices it.

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

- **Transcribe, never invent — and that includes whole sections.** A card headed
  "Who's who in the dialogue", summarising each speaker, shipped in all three
  chapters (removed from ch1 last, where its bookmark had also gone stale). It is nowhere in the book: every fact in it was true, lifted from the
  dialogue, which is exactly why it survived review. The rule is not "is this
  accurate" but "is this on the page". Before shipping a chapter, list its
  headings and every `card()` title and check each one against the scan; an
  English title on a card is the tell, because the book's own cards are Dutch.
  A second invented card, "Listening — listen at coutinho.nl", sat on every
  chapter's dialogue spread until 2026-10-08. The book points at the site from
  its Verdiepingsmateriaal section instead. Its removal left ch1's and ch3's
  page 3 holding only the dialogue illustration, now shown uncropped and centred
  (`variant="plate"`); ch2's illustration grew into the freed space.
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
- **Voice clarity is measurable — check it before adopting a voice.** Four of the
original eight were cloned from dull source audio and sounded, in the user's
words, "like a very old recording on a walkman". Render one identical line per
voice and compare the energy above 8 kHz against the whole band:

    ffmpeg -i v.mp3 -af volumedetect -f null -                  # full band
    ffmpeg -i v.mp3 -af "highpass=f=8000,volumedetect" -f null - # above 8 kHz

The gap is the number that matters. The old teacher lost **46.9 dB** up there;
her replacement loses 20.0. Anything past about -30 dB sounds muffled. Recasting
took chapter 1's numerals from -41.0 to -14.5 dB. The format was never the
problem — every file is already 44.1 kHz / 128 kbps.

**Never recast a recurring character.** `shared/lib/voices.py` is the cast for
  all eighteen chapters; the teacher must always sound like the teacher. Same
  reasoning as `art_style.py`.
- **Audio text must match `content.py` word for word.** It is the book read
  aloud, not a paraphrase. Numbers and postcodes are spelled out in words in
  `audio_script.py` so the model reads them as Dutch, not as digits.
- **Verify before claiming done.** `build.py` checks four things and exits 1 on
  any: content past the trim (`overflow`), a `keep()` block landing on two pages
  (`keep-blocks`), a page mixing two sections (`section mix`), and a `ch.toc`
  bookmark whose page does not show its section number, Opdracht or name
  (`bookmarks`) — the page numbers are typed by hand, and ch2's were all one off
  for a while after a page was removed. It also prints
  a `glossary` line — *N first occurrences marked, M introduced earlier, K
  headwords*. Not a failure, but the numbers should only ever grow as chapters are
  added; a drop means an earlier chapter changed and took the words with it.
  All four checks are structural: they cannot see ugliness, a page that opens
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
- A 10–12-page original becomes 20–25 redesigned pages (ch1 20, ch2 24, ch3 20). Don't cram — the original's
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
- **A cloze is answered with the text that was removed (`card.blank`), never the
  word list's headword.** The list says *de naam*; the blank in
  "Wat is jouw ______?" is *naam*, and checking against the headword made 14
  chapter-1 cards unpassable — the only accepted answer was the ungrammatical
  "Wat is jouw de naam?". Where the sentence itself prints the article, the blank
  contains it and the de/het drill still applies; across ch1-3 that is 6 cards.
  Build-time check: for every card, `sentence` minus `cloze` must equal `blank`.
- **Deck shortcuts are bound to the document, but only act while the deck is on
  screen.** A panel-scoped listener never fired — nothing inside the deck has focus
  on load, so the browser just scrolled the page instead of flipping the card.
  Binding to the document fixes that, and the on-screen test keeps space working
  as scroll everywhere else in a 24-page chapter. Space is the whole round: reveal,
  then "knew it, next". In the answer box a space is just a space, and after a
  typed answer space only advances — the grade came from what was typed.
- **`flashcards.js` is linked, not inlined.** That is the whole point of the
  component — edit it once and all eighteen chapters change on reload, with no
  rebuild. Only new *cards* need `build.py`. Don't inline it "for convenience".
- **A card plays the SENTENCE it quotes, not the bare word.** You learn the word
  in use. `generate_audio.py <chapter> --cards` records one clip per distinct
  sentence with `eleven_v4` and the `kaart` narrator; several cards quoting the
  same line share a recording, so chapters 1-3 need only 84 clips for 212 cards.
  v4 is right here — its weakness is lists of short tokens, and these are prose:
  all 84 verified at 100%.
  The ~1 word in 6 the book never uses in a sentence falls back to the browser's
  `speechSynthesis` saying the word, preferring a *local* nl-NL voice (macOS ships
  Xander), nl-BE last. Audio never fires before the reader acts — and **a keypress
  counts as acting**, not just a click, or driving by space leaves the first card
  silent. A production card stays silent until checked: its sentence is the answer.
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
- **Answers come from Bijlage 8 and land ON the question.** `<chapter>/answers.py`
  holds the book's own key by Opdracht number; `layout.py` tags each exercise
  `data-opdracht`, and `shared/answers.js` puts each answer where the question
  asks for it, behind a fixed toggle (press **a** anywhere). It handles five
  shapes, and falls back to a block only for the two that genuinely are prose:

  | shape | where the answer goes |
  |---|---|
  | `ol.items` with `.blank` | into each blank, in order |
  | `.choice` ("Hebben / hebt") | the right form, after the pair |
  | `ol.choice-items` a/b | the correct `.opt` is marked |
  | a/b/c grid, or photo labels | the right letter is marked |
  | bare nouns in a grid | *de* / *het* in front of each |
  | numbered questions, numbered answers | each answer under the question it answers |
  | "Mogelijke antwoorden: …" | same, with the caveat kept above the list |

  Nothing falls back to a block any more. "Answer the questions" looked
  unplaceable until you notice its eleven answers are numbered against eleven
  questions — so each one goes under its own question. Check that before deciding
  an answer has nowhere to sit. The "Mogelijke antwoorden" caveat is kept, printed
  once above the list, so a sample answer is never shown as the only one.

  A comma inside one item's answer means that item has several blanks
  ("1 op, om"); a slash does not ("jij / je" is one answer). An exercise's
  illustration can sit *after* the `.task` div, so the search runs to the next
  exercise, not just inside the task.
- **Hide every runtime node outside all media queries.** Styling `.answer-fill`
  only inside `@media screen` put the answers in the PDF: print had no rule, so
  they rendered. It showed up as the searchable word count moving 2002 → 2026 —
  which is exactly why build.py prints it. Leak test: search the built PDF for a
  six-word run of every answer and find nothing.
- **Most exercises have no answer, and that is correct.** The book answers 2 of
  chapter 1's 12, 5 of chapter 2's 16, 4 of chapter 3's 13. Speaking and open
  writing tasks have none. Leave them with no block at all — do not write one,
  and do not add a "no answer" placeholder.
- **`timeline()` (ch2 §2.10) is a drawn aid, not book content.** The book prints
  its days as a plain list with an arrow at *Vandaag*. The line shows the same
  seven days in order with the five relative words above them; every pairing is
  one the book states outright (*Eergisteren was het dinsdag*), none is inferred.
  SVG for the same reason as `clock()`. *zondag* and *maandag* carry no relative
  word because the book gives them none — do not invent *overovermorgen*.
- Vocabulary: infinitive small and grey after the stem.
- Bookmarks used to be typed by hand in `ch.toc` and went stale: ch2's were all
  one page off after a page was removed. Now `ch.page(..., toc=[…])` fills in the
  number, and `build.py`'s `bookmarks` check would catch a stale one anyway.
- All three chapters were moved from hand-written HTML to the `layout.py` helpers
  in October 2026, each verified pixel-identical with `build.py --compare`.

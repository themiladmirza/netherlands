# Nederlands in gang — redesigned

A personal redesign of the Dutch coursebook *Nederlands in gang* (Coutinho,
3rd revised edition), rebuilt from scratch as properly typeset pages: original
illustrations, recorded dialogues, hover translations, and a practice deck built
from each chapter's word list.

**Read it:** https://themiladmirza.github.io/netherlands/

| # | Chapter | Pages | Cards |
|---|---------|-------|-------|
| 1 | Welkom | 20 | 86 |
| 2 | In de kantine | 25 | 75 |
| 3 | In het café | 20 | 51 |

## Not affiliated with the publisher

*Nederlands in gang* is © Coutinho. This is a personal study rebuild made
alongside a purchased copy. The publisher's own scans are **not** in this
repository — `hard.pdf` and every `source/` folder are gitignored. If you are
learning Dutch, buy the book; it comes with audio this cannot replace.

## How it is built

Each chapter is a folder under `book/`. `content.py` holds the transcribed text,
`pages.py` lays it out, and `build.py` renders `index.html` plus a print PDF
through headless Chrome.

    python3 book/build.py ch01-welcome

Illustrations come from `art_prompts.py` via OpenAI, dialogue audio from
`audio_script.py` via ElevenLabs. Both read their key from a gitignored `.env`;
neither is needed to read or rebuild what is already here.

Full documentation: [`book/README.md`](book/README.md). Working notes and the
rules this project follows: [`CLAUDE.md`](CLAUDE.md).

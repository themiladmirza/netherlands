# -*- coding: utf-8 -*-
"""Chapter {{NUMBER}} — {{TITLE}}.  Page composition.

Text lives in content.py, styling in ../shared/style.css,
building blocks in ../shared/lib/layout.py.
Build with:  python3 book/build.py {{FOLDER}}

Compose pages from the layout.py helpers; ch03-in-the-cafe/pages.py is the model.
Raw HTML only for a block that is genuinely one of a kind.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "shared", "lib")]

from layout import (Chapter, task, card, vocab_rows, keep, sec, kicker_head, img, web_note,
                    WORDLIST_NOTE, phrases, example, bullets, items, blanks, dialogue, audio_head)
from content import *

ch = Chapter({{NUMBER}}, "{{TITLE}}")

# ---------------------------------------------------------------- 1  COVER
ch.cover(OBJECTIVES)

# ---------------------------------------------------------------- 2  DIALOOG
# ch.page(keep("dialoog-{{NUMBER}}.1", f'''
# {sec("{{NUMBER}}.1", "Dialoog")}
# {audio_head("audio/dialoog.mp3", "…", "…")}
# {dialogue(DIALOOG, {"…"}, audio="audio/dialoog.mp3")}'''), section="{{NUMBER}}.1 Dialoog",
#  toc=[(2, "{{NUMBER}}.1  Dialoog — …")])

# ---------------------------------------------------------------- closing pages
# ch.eigen_vocabulaire()
# ch.reflectie(REFLECTIE, VERDIEPING)

if __name__ == "__main__":
    n = ch.write(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html"))
    print(f"hoofdstuk {ch.number} — {n} pagina's")

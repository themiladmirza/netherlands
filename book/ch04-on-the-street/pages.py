# -*- coding: utf-8 -*-
"""Chapter 4 — Op straat.  Page composition.

Text lives in content.py, styling in ../shared/style.css,
building blocks in ../shared/lib/layout.py.
Build with:  python3 book/build.py ch04-on-the-street
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "shared", "lib")]

from layout import (Chapter, icon, task, card, vocab_rows, keep, lines, sec, kicker_head, img,
                    web_note, WORDLIST_NOTE, phrases, example, items, blanks, term_grid,
                    lettered, word_rows, dialogue, audio_head)
from content import *

ch = Chapter(4, "Op straat")

def rated(rows):
    """Phrases marked ++ / + / +– / – down the margin, as the book prints them."""
    return term_grid(rows, size=9.6, gap="0.9mm 4mm", first="orange")

# ---------------------------------------------------------------- 1  COVER
ch.cover(OBJECTIVES, crop="50% 45%")

# ---------------------------------------------------------------- 2  DIALOOG
ch.page(keep("dialoog-4.1", f'''
{sec("4.1", "Dialoog")}
{audio_head("audio/dialoog.mp3", "Bert en Hans op straat", DIALOOG_INTRO, align="flex-start")}
{dialogue(DIALOOG, {"Bert"}, audio="audio/dialoog.mp3")}'''), section="4.1 Dialoog",
 toc=[(2, "4.1  Dialoog — Bert en Hans op straat")])

# ---------------------------------------------------------------- 3  illustration
ch.page(img("dialoog"), variant="plate", section="4.1 Dialoog")

# ---------------------------------------------------------------- 4-5  WOORDENLIJST
half = 36
ch.page(keep("woordenlijst-a", f'''
{sec("4.2", "Woordenlijst")}
{WORDLIST_NOTE}
{vocab_rows(VOC[:half])}'''), section="4.2 Woordenlijst", toc=[(2, "4.2  Woordenlijst")])

ch.page(f'''
{keep("woordenlijst-b", vocab_rows(VOC[half:]))}
<div class="sp"></div>
{keep("opdracht-1", task(1, "read", None, "Are these sentences true (<i>waar</i>) or not true (<i>niet waar</i>)?",
  items([f'{s}<span style="float:right;color:var(--ink-faint)">waar / niet waar</span>' for s in OPD1], 2.0)))}''',
 section="4.2 Woordenlijst", toc=[(3, "Opdracht 1")])

# ---------------------------------------------------------------- 6  4.3
ex2 = "".join(f'<b>{who}:</b> {line}' + ("<br>" if i % 3 == 2 else " &nbsp; ")
              for i, (who, line) in enumerate(OPD2_EX))
ch.page(keep("hoe-het-gaat-4.3", f'''
{sec("4.3", "Vragen en vertellen hoe het gaat")}
{card("vragen hoe het gaat <span style='font-weight:400'>(asking how someone is)</span>", phrases(VRAGEN))}
{card("vertellen hoe het gaat <span style='font-weight:400'>(telling someone how you are)</span>",
      rated(VERTELLEN), "teal")}
{task(2, "speak", None,
 "Walk around the classroom. Ask another student how they are. They answer and ask how you are. "
 "You answer. Ask four students.", "",
 example(f'<div style="line-height:1.9">{ex2}</div>'))}'''),
 section="4.3 Hoe het gaat", toc=[(2, "4.3  Vragen en vertellen hoe het gaat"), (3, "Opdracht 2")])

# ---------------------------------------------------------------- 7  4.4
o3 = [f'<span style="display:inline-block;width:52mm">{a}</span>'
      f'<span style="color:var(--ink-soft)">{b}</span>' for a, b in OPD3]
ch.page(keep("zullen-4.4", f'''
{sec("4.4", "Zullen (1) – voorstel")}
{card(None, phrases(ZULLEN))}
<div class="sp"></div>
{task(3, "write", None,
 "React with <b>Zal ik …?</b> / <b>Zullen we …?</b> In your reaction, use the words in the second column.",
 items(o3, 2.0),
 example(f'<div style="display:grid;grid-template-columns:52mm 1fr;gap:1mm 0">'
         f'<div>{OPD3_EX[0]}</div><div style="color:var(--ink-soft)">{OPD3_EX[1]}</div>'
         f'<div></div><div><b>{OPD3_EX[2]}</b></div></div>', "margin-bottom:3mm"))}'''),
 section="4.4 Zullen", toc=[(2, "4.4  Zullen (1) – voorstel"), (3, "Opdracht 3")])

# ---------------------------------------------------------------- 8  4.5
ch.page(keep("afspraak-4.5", f'''
{sec("4.5", "Een afspraak maken en positief of negatief reageren")}
{card("een afspraak maken / iemand uitnodigen <span style='font-weight:400'>(arranging to meet / "
      "to invite someone)</span>", phrases(AFSPRAAK))}
{card("positief / negatief reageren <span style='font-weight:400'>(positive / negative responses)</span>",
      rated(REAGEREN_1), "teal")}
<div class="sp"></div>
{task(4, "speak", None, "Respond positively or negatively to the suggestions.", items(OPD4, 2.0))}'''),
 section="4.5 Afspraak", toc=[(2, "4.5  Een afspraak maken"), (3, "Opdracht 4")])

# ---------------------------------------------------------------- 9  4.6
ch.page(keep("samen-4.6", f'''
{sec("4.6", "Vragen iets samen te doen en positief of negatief reageren")}
{card("vragen iets samen te doen <span style='font-weight:400'>(asking to do something together)</span>",
      phrases(SAMEN))}
{card("positief / negatief reageren <span style='font-weight:400'>(positive / negative responses)</span>",
      rated(REAGEREN_2), "teal")}
<div class="sp"></div>
{task(5, "speak", None, "Work in pairs. Together, make up a dialogue. In the dialogue you have to:",
      items(OPD5, 2.0))}'''),
 section="4.6 Samen", toc=[(2, "4.6  Vragen iets samen te doen"), (3, "Opdracht 5")])

# ---------------------------------------------------------------- 10  opdracht 6 + 7
ch.page(f'''
{keep("opdracht-6", task(6, "write", "Woorden invullen", "Which words fit in these sentences?",
  items([blanks(s, 26) for s in OPD6], 2.2)))}
<div class="sp"></div>
{keep("opdracht-7", task(7, "speak", "Een afspraak maken", "",
  lettered([("A", "You get a diary. Write five activities in it. Write down the time too."
                  + example(OPD7_EX, "margin:2.5mm 0 1mm")),
            ("B", "You work in a group of three students. You may not see each other’s diary. "
                  "Together, make an appointment for this week. Agree on the activity, the time "
                  "and the place.")])))}
{img("agenda", 62, "-top:5mm")}''', section="4.6 Samen",
 toc=[(3, "Opdracht 6: Woorden invullen"), (3, "Opdracht 7: Een afspraak maken")])

# ---------------------------------------------------------------- 11  4.7 tekst
ch.page(keep("tekst-4.7", f'''
{sec("4.7", "Tekst")}
<div style="display:flex;gap:3mm;align-items:flex-start;margin-bottom:4mm">{icon("read")}
  <div style="flex:1">
    <div class="readbox" style="margin-bottom:3mm">{TEKST}<br><br>{TEKST_GROET}</div>
    <div class="readbox">{TEKST_ADRES}<br><br>{TEKST_TIJDEN}</div>
  </div></div>
{task(8, "read", None, "You want to go to the office (<i>secretariaat</i>) of the Talencentrum. "
      "You work every day until 17.00. When can you go to the office?", lines(1, "margin-top:3mm"))}'''), section="4.7 Tekst", toc=[(2, "4.7  Tekst"), (3, "Opdracht 8")])

# ---------------------------------------------------------------- 12  4.8 uitspraak
# No audio for Opdracht 9: the words exist only on the publisher's recording.
grid9 = ('<table class="grid" style="max-width:110mm;margin:3mm 0 0"><thead><tr>'
         '<th style="width:50%">6</th><th>2</th></tr></thead><tbody>'
         + '<tr><td style="height:7mm"></td><td></td></tr>' * 8 + '</tbody></table>')
ch.page(f'''
{keep("opdracht-9", f"""{sec("4.8", "Uitspraak: e – ee")}
{task(9, "audio", "e – ee",
  "You hear words with <i>e</i> – <i>ee</i>. Which words have the same sound as <b>6</b> (<i>zes</i>)? "
  "Which have the same sound as <b>2</b> (<i>twee</i>)? Put the words in the right column. "
  "You hear each word twice.", grid9)}""")}
<div class="sp2"></div>
{keep("opdracht-10", task(10, "audio", "e – ee", "Listen carefully to these words and repeat them.",
  word_rows(OPD10), audio="audio/opdracht10.mp3"))}''', section="4.8 Uitspraak",
 toc=[(2, "4.8  Uitspraak: e – ee"), (3, "Opdracht 9"), (3, "Opdracht 10")])

# ---------------------------------------------------------------- 13  cultuur + praktijk
ch.page(f'''
{kicker_head("Cultuur", CULTUUR_VRAAG)}
{card(None, term_grid([(r, "ja / nee") for r in CULTUUR_ROWS], size=9.6, gap="1.6mm 12mm",
                      second="ink-faint"))}
<div class="sp2"></div>
{kicker_head("In de praktijk", "In de praktijk")}
{card(None, f'<div style="font-size:9.6pt">{PRAKTIJK}</div>', "teal")}
{img("praktijk", 60, "-top:5mm")}''', section="In de praktijk",
 toc=[(2, "Cultuur"), (2, "In de praktijk")])

# ---------------------------------------------------------------- closing pages
ch.eigen_vocabulaire()
ch.reflectie(REFLECTIE, VERDIEPING, img_mm=52)

if __name__ == "__main__":
    n = ch.write(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html"))
    print(f"hoofdstuk {ch.number} — {n} pagina's")

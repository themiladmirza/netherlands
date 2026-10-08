# -*- coding: utf-8 -*-
"""Chapter 3 — In het café.  Page composition.

Text lives in content.py, styling in ../shared/style.css,
building blocks in ../shared/lib/layout.py.
Build with:  python3 book/build.py ch03-in-the-cafe
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "shared", "lib")]

from layout import (Chapter, icon, task, card, vocab_rows, number_columns, keep, lines, sec, kicker_head,
                    img, web_note, WORDLIST_NOTE, phrases, example, side_by_side, bullets,
                    items, blanks, word_columns, word_rows, tick_table, sentence_grid,
                    data_table, dialogue, scene_break, audio_head)
from content import *

ch = Chapter(3, "In het café")
YOU = {"Susy", "Andres", "Susy en Andres", "Ober"}

# ---------------------------------------------------------------- 1  COVER
ch.cover(OBJECTIVES, crop="50% 40%", title_pt=36)

# ---------------------------------------------------------------- 2  DIALOOG
ch.page(keep("dialoog-3.1", f'''
{sec("3.1", "Dialoog")}
{audio_head("audio/dialoog.mp3", "Edit viert haar verjaardag", DIALOOG_INTRO, align="flex-start")}
{dialogue(DIALOOG, YOU, "dialogue tight")}
{scene_break("(een poosje later)")}
{dialogue(DIALOOG_2, YOU, "dialogue tight")}
{scene_break("(nog weer later)")}
{dialogue(DIALOOG_3, YOU, "dialogue tight")}'''), section="3.1 Dialoog",
 toc=[(2, "3.1  Dialoog — Edit viert haar verjaardag")])

# ---------------------------------------------------------------- 3  illustration
# The dialogue page has no room for it, so it gets a page of its own, uncropped.
ch.page(img("dialoog"), variant="plate", section="3.1 Dialoog")

# ---------------------------------------------------------------- 4-5  WOORDENLIJST
# 51 entries need two pages; Opdracht 1 joins the continuation so neither runs thin
half = 34
ch.page(keep("woordenlijst-a", f'''
{sec("3.2", "Woordenlijst")}
{WORDLIST_NOTE}
{vocab_rows(VOC[:half])}'''), section="3.2 Woordenlijst", toc=[(2, "3.2  Woordenlijst")])

o1 = [f'<div class="stem">{s}</div><div class="opt"><span>a</span>{a}</div>'
      f'<div class="opt"><span>b</span>{b}</div>' for s, a, b in OPD1]
ch.page(f'''
{keep("woordenlijst-b", vocab_rows(VOC[half:]))}
<div class="sp"></div>
{web_note("The full word list is also online in <b>Dutch, English, German and Arabic</b>.")}
<div class="sp"></div>
{keep("opdracht-1", task(1, "read", None, "Choose the correct ending: a or b.",
  items(o1, cls="items choice-items")))}''', section="3.2 Woordenlijst", toc=[(3, "Opdracht 1")])

# ---------------------------------------------------------------- 6  3.3 / 3.4 / 3.5
ch.page(f'''
{sec("3.3", "Bestellen")}
{card(None, phrases(BESTELLEN))}
{task(2, "speak", None,
 "One person orders something. The next repeats it and orders something too. The third "
 "repeats the first two orders and adds their own.", "",
 example('<div style="line-height:1.7"><b>A:</b> Ik wil graag een cola.<br>'
         '<b>B:</b> Voor mij een cola en een biertje.<br>'
         '<b>C:</b> Mag ik een cola, een biertje en een rode wijn?<br>'
         '<b>D:</b> …</div>'))}
<div class="sp"></div>
{sec("3.4", "Afrekenen")}
{card(None, phrases(AFREKENEN))}
<div class="sp"></div>
{sec("3.5", "Bedanken")}
{card(None, phrases(BEDANKEN), "teal")}''', section="3.5 Bedanken",
 toc=[(2, "3.3  Bestellen"), (3, "Opdracht 2"), (2, "3.4  Afrekenen"), (2, "3.5  Bedanken")])

# ---------------------------------------------------------------- 7  opdracht 3
ch.page(f'''
{task(3, "speak", "Variëren in de dialoog",
 "Work in groups of three: 1 = Edit, 2 = Susy, 3 = Andres + the waiter.",
 '<div style="font-size:9.5pt;line-height:1.8;margin-bottom:1mm">'
 'Lees de tekst twee keer voor.<br>Lees de eerste keer de tekst gewoon.<br>'
 'Maak de tweede keer veranderingen in de tekst.</div>',
 example(side_by_side("Ik neem rode wijn.", "Ik wil witte wijn.")))}
{img("bestellen", 62, "-top:6mm")}''', section="3.5 Bedanken",
 toc=[(3, "Opdracht 3: Variëren in de dialoog")])

# ---------------------------------------------------------------- 8  opdracht 4
o4 = "".join('<dt></dt><dd style="height:2.4mm"></dd>' if not s
             else f'<dt>{s}:</dt><dd>{blanks(t, 26)}</dd>' for s, t in OPD4)
ch.page(keep("opdracht-4", task(4, "write", "De tekst compleet maken",
  "Complete the café conversation. Fill in one or two words.",
  f'<div class="note" style="font-style:normal;margin-bottom:3mm">{OPD4_INTRO}</div>'
  f'<dl class="dialogue">{o4}</dl>')), section="3.5 Bedanken",
  toc=[(3, "Opdracht 4: De tekst compleet maken")])

# ---------------------------------------------------------------- 9  3.6 artikel
ch.page(keep("artikel-3.6", f'''
{sec("3.6", "Artikel")}
{card(None, phrases(ARTIKEL_EX, 9.4, 1.8))}
{data_table(("", "definiet", "indefiniet"), ARTIKEL)}
<div class="sp"></div>
{card('diminutief', phrases(DIMINUTIEF), "teal")}'''), section="3.6 Artikel",
 toc=[(2, "3.6  Artikel")])

# ---------------------------------------------------------------- 10  opdracht 5
ch.page(keep("opdracht-5", task(5, "write", None,
  "Choose the correct article for each word: <b>de</b> or <b>het</b>. Check your answers against "
  "the word list. Note down the words you got wrong, with the right article.",
  word_columns(OPD5, 3, max_width=100, extra="margin-top:2mm;"))), section="3.6 Artikel",
  toc=[(3, "Opdracht 5")])

# ---------------------------------------------------------------- 11  3.7 inversie
# The fronted phrase is reconstructed, not transcribed — see NOTES.md.
o6 = [f'{a} <b style="color:var(--teal)">{b}</b>{(" " + c) if c else ""}' for a, b, c in OPD6]
ch.page(keep("inversie-3.7", f'''
{sec("3.7", "Hoofdzin met inversie")}
{card(None, sentence_grid(INVERSIE))}
{task(6, "speak", None, "Read the sentence, but start with the highlighted part.",
 items(o6, 2.05),
 example(side_by_side('Ik wil <b style="color:var(--teal)">nu</b> een cola.', '<b>Nu</b> wil ik een cola.'),
         "margin-bottom:3mm"))}'''), section="3.7 Inversie",
 toc=[(2, "3.7  Hoofdzin met inversie"), (3, "Opdracht 6")])

# ---------------------------------------------------------------- 12  3.8 rangtelwoorden
ch.page(keep("rangtelwoorden-3.8", f'''
{sec("3.8", "Rangtelwoorden")}
{card(None, number_columns(RANG_A, RANG_B, RANG_C))}
<div class="sp"></div>
{task(7, "speak", None, "Ask the person next to you.", bullets(OPD7))}'''),
 section="3.8 Rangtelwoorden", toc=[(2, "3.8  Rangtelwoorden"), (3, "Opdracht 7")])

# ---------------------------------------------------------------- 13  opdracht 8 + 9
cloud = " ".join(f'<span style="font-size:{sz}pt">{w}</span>' for w, sz in WOORDWOLK)
ch.page(f'''
{task(8, "speak", "Woordwolk",
 "Here is a word cloud. Talk in pairs. Make sentences with the words from the cloud. Use every word.",
 f'<div class="wordcloud">{cloud}</div>')}
<div class="sp"></div>
{task(9, "write", "Reageren op een uitnodiging", "You receive this invitation by e-mail:",
  f'<div class="mail">{OPD9_MAIL}</div>',
  '<div style="margin-top:3.5mm">Schrijf een reactie naar Benedetta.</div>'
  + lines(6, "margin-top:3mm"))}''', section="3.8 Rangtelwoorden",
 toc=[(3, "Opdracht 8: Woordwolk"), (3, "Opdracht 9: Reageren op een uitnodiging")])

# ---------------------------------------------------------------- 14  3.9 tekst
ch.page(keep("tekst-3.9", f'''
{sec("3.9", "Tekst")}
<div style="display:flex;gap:3mm;align-items:flex-start;margin-bottom:5mm">{icon("read")}
  <div class="readbox">{TEKST}</div></div>
{task(10, "read", None, "Op welke foto staat dit café?")}
<div style="position:relative;margin-top:2mm">
  {img("cafes", 56)}
  <div class="photolabels"><span>a</span><span>b</span><span>c</span></div>
</div>'''), section="3.9 Tekst", toc=[(2, "3.9  Tekst"), (3, "Opdracht 10")])

# ---------------------------------------------------------------- 15  3.10 + opdracht 11
ch.page(keep("uitspraak-3.10", f'''
{sec("3.10", "Uitspraak: o – oo")}
{task(11, "audio", "Woordaccent",
 "Which part of the word carries the stress, the accent? Underline that part.",
 example('<div>be<u>gin</u>nen</div>', "max-width:52mm;margin:0 0 4mm")
 + word_columns(OPD11, 3, max_width=110),
 audio="audio/opdracht11.mp3")}'''), section="3.10 Uitspraak",
 toc=[(2, "3.10  Uitspraak: o – oo"), (3, "Opdracht 11: Woordaccent")])

# ---------------------------------------------------------------- 16  opdracht 12
# No audio: the word pairs exist only on the publisher's recording.
ch.page(keep("opdracht-12", task(12, "audio", "o – oo",
  "You hear two words each time. Is it the same sound (+) or a different one (–)?",
  tick_table(10))), section="3.10 Uitspraak", toc=[(3, "Opdracht 12")])

# ---------------------------------------------------------------- 17  opdracht 13
ch.page(keep("opdracht-13", task(13, "audio", "o – oo",
  "Listen carefully to these words and repeat them.", word_rows(OPD13),
  audio="audio/opdracht13.mp3")), section="3.10 Uitspraak", toc=[(3, "Opdracht 13")])

# ---------------------------------------------------------------- 18  cultuur + praktijk
ch.page(f'''
{kicker_head("Cultuur", CULTUUR_VRAAG)}
{card(None, phrases(CULTUUR, lh=1.9))}
<div class="sp2"></div>
{kicker_head("In de praktijk", "Bestel iets in het Nederlands")}
{card(None, f'<div style="font-size:9.6pt">{PRAKTIJK}</div>', "teal")}
{img("praktijk", 56, "-top:5mm")}''', section="In de praktijk",
 toc=[(2, "Cultuur"), (2, "In de praktijk")])

# ---------------------------------------------------------------- 19-20  closing pages
ch.eigen_vocabulaire()
ch.reflectie(REFLECTIE, VERDIEPING, img_mm=48)

if __name__ == "__main__":
    n = ch.write(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html"))
    print(f"hoofdstuk {ch.number} — {n} pagina's")

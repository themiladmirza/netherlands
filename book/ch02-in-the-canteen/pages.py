# -*- coding: utf-8 -*-
"""Chapter 2 — In de kantine.  Page composition.

Text lives in content.py, styling in ../shared/style.css,
building blocks in ../shared/lib/layout.py.
Build with:  python3 book/build.py ch02-in-the-canteen
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "shared", "lib")]

from layout import (Chapter, task, card, vocab_rows, keep, clock, timeline, sec, kicker_head,
                    img, web_note, WORDLIST_NOTE, phrases, example, bullets, items, blanks,
                    word_columns, word_rows, tick_table, sentence_grid, data_table, dialogue,
                    audio_head, term_grid, lettered, two_columns)
from content import *

ch = Chapter(2, "In de kantine")

# ---------------------------------------------------------------- 1  COVER
ch.cover(OBJECTIVES, crop="50% 26%", title_pt=34)

# ---------------------------------------------------------------- 2  DIALOOG
ch.page(f'''{keep("dialoog-2.1", f"""
{sec("2.1", "Dialoog")}
{audio_head("audio/dialoog.mp3", "Susy en Edit in de kantine",
            "Susy en Edit hebben pauze en zitten in de kantine.")}
{dialogue(DIALOOG, {"Susy"}, audio="audio/dialoog.mp3")}""")}
{img("dialoog", 60, "-top:4mm")}''',
 section="2.1 Dialoog", toc=[(2, "2.1  Dialoog — in de kantine")])

ch.talk("audio/dialoog.mp3")

# ---------------------------------------------------------------- 3-4  WOORDENLIJST
half = 38
ch.page(keep("woordenlijst-a", f'''
{sec("2.2", "Woordenlijst")}
{WORDLIST_NOTE}
{vocab_rows(VOC[:half])}'''), section="2.2 Woordenlijst", toc=[(2, "2.2  Woordenlijst")])
ch.page(keep("woordenlijst-b", f'''{vocab_rows(VOC[half:])}
<div class="sp2"></div>
{web_note("The full word list is also online in <b>Dutch, English, German and Arabic</b>.")}'''),
 section="2.2 Woordenlijst")

# ---------------------------------------------------------------- 5  opdracht 1
ch.page(keep("opdracht-1", task(1, "speak", None, "Answer the questions.", items(OPD1, 2.2))),
 section="2.2 Woordenlijst", toc=[(3, "Opdracht 1")])

# ---------------------------------------------------------------- 6  2.3 familierelaties
fam = [pair for a, b in zip(FAMILIE_A + [("", "")], FAMILIE_B) for pair in (a, b)]
ch.page(keep("familie-2.3", f'''
{sec("2.3", "Familierelaties")}
{card(None, term_grid(fam, size=9.3, gap="1.3mm 5mm", second="teal", per_row=2))}
{img("familie", 62, "-top:2mm")}'''), section="2.3 Familierelaties",
 toc=[(2, "2.3  Familierelaties")])

# ---------------------------------------------------------------- 7  2.4 + opdracht 2
ch.page(f'''
{sec("2.4", 'Beschrijven van mensen '
     '<span style="font-size:10pt;color:var(--ink-faint);font-weight:600;margin-left:2.15mm">describing people</span>')}
{card(None, phrases(BESCHRIJVEN))}
<div class="sp"></div>
{task(2, "speak", None, "You will see photos of families. Work in pairs. Choose one person from a family.",
 lettered([
   ("A", "Beschrijf hoe hij / zij eruitziet."),
   ("B", "Vertel / fantaseer:<br>1&nbsp; Hoe heet hij / zij?<br>2&nbsp; Hoe oud is hij / zij?"),
   ("C", "Vertel / fantaseer over zijn / haar broers en zussen en ouders:<br>"
         "1&nbsp; Wat doen ze?<br>2&nbsp; Waar wonen ze?<br>3&nbsp; Waar zijn ze nu (op de foto)?")]))}
{img("gezinnen", 50, "-top:3mm")}''', section="2.4 Beschrijven van mensen",
 toc=[(2, "2.4  Beschrijven van mensen"), (3, "Opdracht 2")])

# ---------------------------------------------------------------- 8  2.5 / 2.6 / 2.7
ch.page(f'''
{sec("2.5", "Hoofdzin")}
{card(None, sentence_grid(HOOFDZIN, dutch_cols=(0,), size=9.5))}
<div class="sp"></div>
{sec("2.6", "Ja / nee-vragen")}
{card(None, phrases(JANEE, 9.5, 1.8))}
<div class="sp"></div>
{sec("2.7", "Vraagwoordvragen")}
{card(None, two_columns([VRAAGWOORD_A, VRAAGWOORD_B]))}''', section="2.7 Vraagwoordvragen",
 toc=[(2, "2.5  Hoofdzin"), (2, "2.6  Ja / nee-vragen"), (2, "2.7  Vraagwoordvragen")])

# ---------------------------------------------------------------- 9  opdracht 3
o3 = [f'<div class="qline">{blanks(q)}</div><div class="aline">{a}</div>' for q, a in OPD3]
ch.page(keep("opdracht-3", task(3, "write", None, "Fill in a question word. Look at the answer!",
  items(o3, cls="items qa-items"))), section="2.7 Vraagwoordvragen", toc=[(3, "Opdracht 3")])

# ---------------------------------------------------------------- 10  2.8 possessief
ch.page(keep("possessief-2.8", f'''
{sec("2.8", "Possessief pronomen")}
{card(None, phrases(["<b>Mijn</b> broer komt.", "Komen <b>je</b> ouders ook op bezoek?"], 9.5, 1.8))}
{data_table(("subject", "possessief pronomen"), POSSESSIEF, first_width=34)}'''),
 section="2.8 Possessief pronomen", toc=[(2, "2.8  Possessief pronomen")])

# ---------------------------------------------------------------- 11  opdracht 4
ch.page(keep("opdracht-4", task(4, "write", None, "Fill in a possessive pronoun.",
  items([blanks(s) for s in OPD4], 2.5))), section="2.8 Possessief pronomen",
  toc=[(3, "Opdracht 4")])

# ---------------------------------------------------------------- 12  2.9 de klok
# Clock faces are drawn, not generated, so the hands are exactly right.
ch.page(keep("klok-2.9", f'''
{sec("2.9", "De klok")}
{card("Hoe laat is het?",
 term_grid(KLOK) + '<div style="height:3.5mm"></div>'
 + term_grid(DUUR, second="teal", style="max-width:70mm"))}
<div class="clocks">{"".join(clock(h, m, lbl) for h, m, lbl in KLOK_FACES)}</div>'''),
 section="2.9 De klok", toc=[(2, "2.9  De klok")])

# ---------------------------------------------------------------- 13  opdracht 5 + 6
ch.page(f'''
{task(5, "speak", None, "Ask the person next to you.", bullets(OPD5))}
{task(6, "read", None, "Your teacher will give you a worksheet.")}''', section="2.9 De klok",
 toc=[(3, "Opdracht 5–6")])

# ---------------------------------------------------------------- 14  2.10 dagen
ch.page(keep("dagen-2.10", f'''
{sec("2.10", "De dagen van de week")}
{card('dagen &nbsp;<em>days</em>', phrases(DAGEN, 9.6, 1.9))}
<div class="note" style="margin:3.5mm 0 0">The same week on a line. Ours, not the book's.</div>
{timeline([("eergisteren","dinsdag"), ("gisteren","woensdag"),
           ("vandaag","donderdag"), ("morgen","vrijdag"),
           ("overmorgen","zaterdag"), ("","zondag"), ("","maandag")], today=2)}
<div class="sp"></div>
{task(7, "speak", None, "Ask the person next to you.", bullets(OPD7))}'''),
 section="2.10 De dagen van de week", toc=[(2, "2.10  De dagen van de week"), (3, "Opdracht 7")])

# ---------------------------------------------------------------- 15  2.11 maanden
ch.page(keep("maanden-2.11", f'''
{sec("2.11", "Maanden en seizoenen")}
{card('maanden &nbsp;<em>months</em>', word_columns(MAANDEN, 4, gap="0 5mm", size=9.5, lh=1.8))}
{card('seizoenen &nbsp;<em>seasons</em>', phrases(SEIZOENEN, 9.5, 1.8), "teal")}
{img("seizoenen", 34, "-bottom:5mm")}
{task(8, "speak", None, "Ask the person next to you.", bullets(OPD8))}
{task(9, "speak", None, "Name something you associate with each month. Which is your favourite month?")}'''),
 section="2.11 Maanden en seizoenen", toc=[(2, "2.11  Maanden en seizoenen"), (3, "Opdracht 8–9")])

# ---------------------------------------------------------------- 16  opdracht 10
ch.page(keep("opdracht-10", task(10, "write", "Een prepositie invullen",
  "Fill in: <b>op</b>, <b>om</b> or <b>in</b>.", items([blanks(s, 16) for s in OPD10], 2.4))),
  section="2.11 Maanden en seizoenen", toc=[(3, "Opdracht 10: Een prepositie invullen")])

# ---------------------------------------------------------------- 17  opdracht 11 + 12
ch.page(f'''
{task(11, "speak", "Interviewen", None, lettered([
  ("A", "Work in pairs. Think up questions for an interview. Use the word list, and use both "
        "types of question: the <i>ja / nee</i>-question and the question-word question."),
  ("B", "Form new pairs. Interview each other using the questions from part A.")], gap="2.2mm 2mm"))}
<div class="sp"></div>
{task(12, "write", "Een tekst schrijven", "Choose task A or B.", lettered([
  ("A", "Schrijf een tekst bij een foto van opdracht 2."),
  ("B", "Schrijf een tekst bij een foto van je familie.")], gap="2.2mm 2mm"))}''',
 section="2.11 Maanden en seizoenen",
 toc=[(3, "Opdracht 11: Interviewen"), (3, "Opdracht 12: Een tekst schrijven")])

# ---------------------------------------------------------------- 18  2.12 tekst
# The 1-1-2 sign is typeset: a public emergency number, kept accurate as type.
ch.page(keep("tekst-2.12", f'''
{sec("2.12", "Tekst")}
<div style="display:flex;gap:8mm;align-items:flex-start">
  <div style="flex:1">
  {task(13, "read", None, "Wat is dit?",
   lettered([("a", "een adres"), ("b", "een postcode"), ("c", "een telefoonnummer")], size=9.5))}
  </div>
  <div style="flex:0 0 auto;padding-top:6mm">
    <div class="sign"><div class="big">1-1-2</div><div class="small">ALS ELKE<br>SECONDE TELT</div></div>
  </div>
</div>'''), section="2.12 Tekst", toc=[(2, "2.12  Tekst"), (3, "Opdracht 13")])

# ---------------------------------------------------------------- 19  2.13 + opdracht 14
ch.page(keep("uitspraak-2.13", f'''
{sec("2.13", "Uitspraak: a – aa")}
{task(14, "speak", "Vocalen",
 "You work at a dating agency — an odd one: you match people who share the same first vowel. "
 "These people are looking for a partner:",
 word_columns(list(zip(*DATING)), 4, gap="0 5mm", size=9.5, lh=1.9, extra="margin:1mm 0 3mm")
 + f'<div class="note" style="font-style:normal">{DATING_NOTE}</div>')}'''),
 section="2.13 Uitspraak", toc=[(2, "2.13  Uitspraak: a – aa"), (3, "Opdracht 14: Vocalen")])

# ---------------------------------------------------------------- 20  opdracht 15
# No audio: the word pairs exist only on the publisher's recording.
ch.page(keep("opdracht-15", task(15, "audio", "a – aa", None,
  lettered([("A", "You hear two words each time. Is it the same sound (+) or a different one (–)?")],
           gap="2.4mm 2mm")
  + tick_table(5, style="max-width:62mm;margin:3mm 0 6mm")
  + lettered([("B", "You hear three words each time. Which two have the same sound?")], gap="2.4mm 2mm")
  + example('<table class="grid tick noindex" style="margin:0"><thead><tr><th>jarig</th><th>naam</th>'
            '<th>dag</th></tr></thead><tbody><tr><td>+</td><td>+</td><td>–</td></tr></tbody></table>',
            "max-width:74mm;margin:3mm 0 2mm")
  + tick_table(7, heads=("", "", ""), style="max-width:74mm;margin:3mm 0 0", head=False))),
  section="2.13 Uitspraak", toc=[(3, "Opdracht 15")])

# ---------------------------------------------------------------- 21  opdracht 16
ch.page(keep("opdracht-16", task(16, "audio", "a – aa",
  "Listen carefully to these words and repeat them.", word_rows(OPD16),
  audio="audio/opdracht16.mp3")), section="2.13 Uitspraak", toc=[(3, "Opdracht 16")])

# ---------------------------------------------------------------- 22  cultuur + praktijk
ch.page(f'''
{kicker_head("Cultuur", "Hoeveel kinderen?")}
{card(None, phrases(CULTUUR, 9.6, 1.8))}
<div class="sp2"></div>
{kicker_head("In de praktijk", "Hoe laat is het?")}
{card(None, phrases(PRAKTIJK, 9.6, None), "teal")}
{img("praktijk", 58, "-top:5mm")}''', section="In de praktijk",
 toc=[(2, "Cultuur"), (2, "In de praktijk")])

# ---------------------------------------------------------------- 23-24  closing pages
ch.eigen_vocabulaire()
ch.reflectie(REFLECTIE, ["grammar and pronunciation videos", "a gap-fill of the dialogue",
                         "extra exercises", "an intensive listening text"])

if __name__ == "__main__":
    n = ch.write(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html"))
    print(f"hoofdstuk {ch.number} — {n} pagina's")

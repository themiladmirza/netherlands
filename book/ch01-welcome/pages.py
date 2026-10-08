# -*- coding: utf-8 -*-
"""Chapter 1 — Welkom.  Page composition.

Text lives in content.py, styling in ../shared/style.css,
building blocks in ../shared/lib/layout.py.
Build with:  python3 book/build.py ch01-welcome
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "shared", "lib")]

from layout import (Chapter, task, card, qa, vocab_rows, pairs, numbers, number_columns, keep,
                    sec, kicker_head, img, web_note, WORDLIST_NOTE, bullets, items, blanks,
                    data_table, dialogue, audio_head, audio_note, term_grid)
from content import *

ch = Chapter(1, "Welkom")

# ---------------------------------------------------------------- 1  COVER
ch.cover(OBJECTIVES, crop="50% 22%", title_pt=40, title_lh=".86")

# ---------------------------------------------------------------- 2  DIALOOG
# The whole conversation on one page, as in the original (book p.21). It is
# wrapped in keep() so it can never be split again; the illustration and the
# supporting cards move to the facing page to make room.
ch.page(keep("dialoog-1.1", f'''
{sec("1.1", "Dialoog")}
{audio_head("audio/dialoog.mp3", "De cursus begint", "De cursus begint.")}
{dialogue(DIALOOG, {s for s, _ in DIALOOG} - {"Docent"})}
<div style="text-align:center;color:var(--ink-faint);font-family:var(--disp);
            font-size:12pt;letter-spacing:.3em;margin:3.5mm 0">(…)</div>
{dialogue(DIALOOG_END)}'''), section="1.1 Dialoog",
 toc=[(2, "1.1  Dialoog — De cursus begint")])

# ---------------------------------------------------------------- 3  illustration + luisteren
ch.page(f'''
{img("dialoog", 112, "-bottom:7mm")}
<div class="sp"></div>
{web_note("Listen to this dialogue at <b>coutinho.nl/nederlandsingang3</b> and repeat the sentences. "
          "Each time you listen you will understand more.", "teal", title="Listening")}''',
 section="1.1 Dialoog")

# ---------------------------------------------------------------- 4-5  WOORDENLIJST
half = 48
ch.page(keep("woordenlijst-a", f'''
{sec("1.2", "Woordenlijst")}
{WORDLIST_NOTE}
{vocab_rows(VOC[:half])}'''), section="1.2 Woordenlijst", toc=[(2, "1.2  Woordenlijst")])
ch.page(keep("woordenlijst-b", f'''{vocab_rows(VOC[half:])}
<div class="sp2"></div>
{web_note("The full word list is also online in <b>Dutch, English, German and Arabic</b>.")}'''),
 section="1.2 Woordenlijst")

# ---------------------------------------------------------------- 6  1.3
ch.page(f'''
{sec("1.3", "Zich voorstellen /<br>informatie vragen / landen")}
{card('zich voorstellen &nbsp;<em>introducing yourself</em>', qa(VOORSTELLEN))}
{card('informatie vragen &nbsp;<em>adres en land van herkomst</em>', qa(INFORMATIE), "teal")}
{card('landen / talen / nationaliteiten',
  f'<div style="display:grid;grid-template-columns:1fr 1fr 1.25fr;gap:1.4mm 4mm;font-size:9pt">'
  f'{"".join(f"<div>{a}</div><div>{b}</div><div>{c}</div>" for a, b, c in LANDEN)}</div>')}''',
 section="1.3 Zich voorstellen", toc=[(2, "1.3  Zich voorstellen / informatie vragen / landen")])

# ---------------------------------------------------------------- 7  landen + opdracht 1
ch.page(f'''
{img("landen", 78, ":0 0 6mm")}
{task(1, "speak", None, "Talk to the person next to you. Ask:",
 '<div class="two"><ol class="items"><li>Wie ben jij?</li><li>Wat is je adres?</li>'
 '<li>Uit welk land kom je?</li></ol><ol class="items" start="4" style="counter-reset:it 3">'
 '<li>Welke taal spreek je?</li><li>Wat is je nationaliteit?</li></ol></div>',
 '<div class="note" style="margin-top:2.5mm">Now ask the person on your other side.</div>')}''',
 section="1.3 Zich voorstellen", toc=[(3, "Opdracht 1")])

# ---------------------------------------------------------------- 8  1.4 verbs
VERB = '<div style="font-style:italic;color:var(--orange);font-weight:600">{}</div>'
ch.page(keep("werkwoord-1.4", f'''
{sec("1.4", "Personaal pronomen + werkwoord")}
{card(None,
 '<div style="display:grid;grid-template-columns:auto auto 1fr;gap:1.1mm 4mm;font-size:9.3pt">'
 '<div class="dutch">Ik</div>' + VERB.format("ben") + '<div>Susy.</div>'
 '<div class="dutch">Hij</div>' + VERB.format("geeft") + '<div>twee dagen les en ik drie.</div>'
 '<div class="dutch">We</div>' + VERB.format("luisteren") + '<div>naar de tekst.</div>'
 '</div><div style="height:3mm"></div>'
 '<div style="font-size:9.3pt">Waar <i style="color:var(--orange)">woon</i> je?<br>'
 '<i style="color:var(--orange)">Woont</i> u ook in Utrecht?</div>')}
{data_table(("", "luisteren", "hebben", "zijn"), VERBS, first_width=34)}
<div class="sp"></div>
{web_note('In de <b>inversie</b> verandert de vorm: <i>je luistert</i> &rarr; <i>luister je?</i> · '
          '<i>je hebt</i> &rarr; <i>heb je?</i> · <i>je bent</i> &rarr; <i>ben je?</i>',
          "teal", align="center")}'''),
 section="1.4 Personaal pronomen", toc=[(2, "1.4  Personaal pronomen + werkwoord")])

# ---------------------------------------------------------------- 9  opdracht 2
ch.page(keep("opdracht-2", task(2, "write", None, "Fill in a personal pronoun.",
  items([blanks(s) for s in OPD2], 2.5))), section="1.4 Personaal pronomen",
  toc=[(3, "Opdracht 2")])

# ---------------------------------------------------------------- 10  opdracht 3
o3 = [f'{pre} <span class="choice">{choice}</span> {post}' if mode == "pre"
      else f'<span class="choice">{pre} / {choice}</span> {post}' for pre, choice, post, mode in OPD3]
ch.page(keep("opdracht-3", task(3, "write", None, "Choose the correct form of the verb.",
  items(o3, 2.1))), section="1.4 Personaal pronomen", toc=[(3, "Opdracht 3")])

# ---------------------------------------------------------------- 11  1.5 telwoorden
# §1.5 keeps its own exercises. The illustration shrinks to make room rather than
# pushing Opdracht 4-5 onto the next page, where they would sit above §1.6's
# heading with nothing saying which section they belong to.
ch.page(keep("telwoorden-1.5", f'''
{sec("1.5", "Telwoorden")}
{audio_note("audio/telwoorden.mp3", "Telwoorden", "Listen and repeat.")}
{card(None, number_columns(NUMS_A, NUMS_B, NUMS_C)
  + '<div style="height:3mm"></div>' + numbers(NUMS_D))}
{task(4, "speak", None, "Ask the person next to you.",
 bullets(["Wat is je huisnummer?", "Wat is je telefoonnummer?",
          "Wat is je geboortedatum?", "Wat is je postcode?"]))}
{task(5, "read", None, "Your teacher will give you a worksheet.")}'''), section="1.5 Telwoorden",
 toc=[(2, "1.5  Telwoorden"), (3, "Opdracht 4–5")])

# ---------------------------------------------------------------- 12  1.6 het alfabet
ch.page(keep("alfabet-1.6", f'''
{sec("1.6", "Het alfabet")}
{audio_note("audio/alfabet.mp3", "Het alfabet", "Listen and repeat the letters.", mb=3)}
<div class="alpha">{"".join(f"<span>{c}</span>" for c in "abcdefghijklmnopqrstuvwxyz")}</div>
<div class="sp"></div>
{card(None, term_grid([("ij", "lange ij"), ("ei", "korte ei"), ("y", "Griekse ij")],
                      gap="1.2mm 4mm", first="orange"))}
<div class="sp"></div>
{task(6, "speak", None, None, bullets(["Wat zijn de letters van je postcode?",
  "Wat is je voorletter?", "Met welke letter begint je achternaam?"]))}
{task(7, "speak", None, "Line up in alphabetical order, by surname.")}
{img("telwoorden", 48, "-top:5mm")}'''), section="1.6 Het alfabet",
 toc=[(2, "1.6  Het alfabet"), (3, "Opdracht 6–7")])

# ---------------------------------------------------------------- 13  1.7 spellen
ch.page(f'''
{sec("1.7", "Spellen")}
{card(None,'<div style="font-size:9.5pt;line-height:1.75">'
 'Kun je dat spellen? / Kunt u dat spellen?<br>Hoe spel je dat? / Hoe spelt u dat?</div>'
 '<div style="height:3mm"></div>'
 '<div style="font-size:9.5pt;line-height:1.75"><span class="dutch">Wall, hoe spel je dat?</span><br>'
 '<span style="margin-left:5mm;color:var(--teal)">Met dubbel l.</span></div>'
 '<div style="height:2.5mm"></div>'
 '<div style="font-size:9.5pt;line-height:1.75"><span class="dutch">Susy, is dat met een s of een z?</span><br>'
 '<span style="margin-left:5mm;color:var(--teal)">Met een s, en met een Griekse y.</span></div>')}
{img("alfabet", 48, "-bottom:4mm")}
{task(8, "speak", None, "Ask three other students for their first name and surname. How are they spelled?")}''',
 section="1.7 Spellen", toc=[(2, "1.7  Spellen"), (3, "Opdracht 8")])

# ---------------------------------------------------------------- 14  1.8 begroeten
ch.page(f'''
{sec("1.8", "Begroeten en afscheid nemen")}
{img("begroeten", 40, "-bottom:4.5mm")}
<div class="two" style="gap:0 6mm">
  <div>{pairs(BEGROETEN,"begroeten","greetings")}</div>
  <div>{pairs(AFSCHEID,"afscheid nemen","saying goodbye")}</div>
</div>
<div class="sp"></div>
{task(9, "speak", None, "Walk around the room. Greet a student. The student says goodbye. "
  "Move on to another student and greet them.", "",
  '<div class="example"><div class="lbl">Example</div>'
  '<div style="display:grid;grid-template-columns:1fr 1fr;gap:.8mm 4mm">'
  '<div><b>A:</b> Goedemorgen.</div><div><b>B:</b> Dag. <span class="note">(move on to the next student)</span></div>'
  '<div><b>A:</b> Hoi.</div><div><b>C:</b> Tot ziens.</div></div></div>')}''', section="1.8 Begroeten",
 toc=[(2, "1.8  Begroeten en afscheid nemen"), (3, "Opdracht 9")])

# ------------------------------------------------- 15  opdracht 10 + 11 (formulier)
RULE = '<span style="border-bottom:.7pt solid var(--rule);height:4.6mm"></span>'
fr = ""
for f in FORM:
    if f == "Geslacht":
        fr += ('<div class="fr"><div class="fl">Geslacht</div><div>'
               '<span class="box"></span>man &nbsp;&nbsp;<span class="box"></span>vrouw</div></div>')
    elif "|" in f:
        a2, b2 = f.split("|")
        fr += (f'<div class="fr"><div class="fl">{a2}</div>'
               f'<div style="display:grid;grid-template-columns:1fr auto 1fr;gap:3mm;align-items:baseline">'
               f'{RULE}<span class="fl" style="font-size:8.4pt">{b2}</span>{RULE}</div></div>')
    else:
        fr += (f'<div class="fr"><div class="fl">{f}</div>'
               f'<div style="border-bottom:.7pt solid var(--rule);height:4.6mm"></div></div>')
ch.page(f'''
{task(10, "speak", None, "Work in pairs. Think up questions for an interview. "
  "Ask about: name, address, country, language, nationality.", "",
  '<div class="example"><div class="lbl">Example</div>'
  '<div style="display:grid;grid-template-columns:1fr 1fr;gap:.8mm 4mm">'
  '<div><b>A:</b> Dag, ik ben Elena. Wie ben jij?</div><div><b>B:</b> Ik ben Bertrand. Waar woon je?</div>'
  '<div><b>A:</b> Ik woon in Nijmegen. En jij?</div>'
  '<div><b>B:</b> Ik woon ook in Nijmegen. Wat is je adres?</div></div></div>')}
<div class="sp"></div>
{task(11, "write", "Filling in a form", "Fill in your personal details.")}
<div class="form" style="padding:5mm 6mm"><div style="font-family:var(--disp);font-weight:700;color:var(--orange);
  font-size:10pt;margin-bottom:3mm;letter-spacing:.02em">Persoonlijke gegevens</div>{fr}</div>''',
 section="1.8 Begroeten",
 toc=[(3, "Opdracht 10"), (3, "Opdracht 11: Een formulier invullen")])

# ---------------------------------------------------------------- 16  1.9 zinsaccent
za = [f'{q}<div style="color:var(--teal);margin-left:0">{a}</div>' for q, a in ZINSACCENT]
ch.page(keep("zinsaccent-1.9", f'''
{sec("1.9", "Uitspraak: zinsaccent")}
{task(12, "audio", "Zinsaccent", "Listen to the question and the answer. Which words carry the stress? "
 "Repeat the answer.", items(za, 1.65), audio="audio/zinsaccent.mp3")}'''),
 section="1.9 Uitspraak", toc=[(2, "1.9  Uitspraak: zinsaccent"), (3, "Opdracht 12")])

# ---------------------------------------------------------------- 17  cultuur
BOX = '<div style="text-align:center"><span class="box"></span></div>'
ch.page(f'''
{kicker_head("Cultuur", '<span class="lock"><span class="num" style="font-size:15pt">u</span>'
                        ' of <span style="color:var(--teal)">jij</span>?</span>')}
{img("cultuur", 44, "-bottom:5mm")}
{card("Who do you say <i>u</i> to? Who do you say <i>jij</i> to?",
 '<div style="display:grid;grid-template-columns:1fr 18mm 18mm;gap:1.8mm 3mm;font-size:9.4pt">'
 '<div></div><div style="text-align:center;font-family:var(--disp);font-weight:700;color:var(--orange)">u</div>'
 '<div style="text-align:center;font-family:var(--disp);font-weight:700;color:var(--teal)">jij</div>'
 + "".join(f'<div>{r}</div>{BOX}{BOX}' for r in CULTUUR_ROWS) + '</div>')}''',
 section="Cultuur", toc=[(2, "Cultuur — u of jij?")])

# ---------------------------------------------------------------- 18  in de praktijk
sn = "".join(f'<div class="n"><b>{i+1}</b><span>{s}</span></div>' for i, s in enumerate(SURNAMES))
ch.page(f'''
{kicker_head("In de praktijk", "De top 10 van familienamen<br>in Nederland")}
<div class="note" style="margin-bottom:4mm">Do you know anyone with these surnames?</div>
<div class="two" style="gap:0 7mm">
 <div class="numbers" style="grid-template-columns:1fr">{sn}</div>
 {img("praktijk", 72)}
</div>''', section="In de praktijk", toc=[(2, "In de praktijk — top 10 familienamen")])

# ---------------------------------------------------------------- 19-20  closing pages
ch.eigen_vocabulaire()
ch.reflectie([
  "Can you now understand the dialogue at the start of this chapter?",
  "Can you give your name and address, and ask others for theirs?",
  "Can you count to 20?", "Can you spell your name and address?",
  "Can you fill in a form with personal details?", "Can you greet someone and say goodbye?"],
  ["a grammar video", "a gap-fill of the dialogue", "extra exercises", "an intensive listening text"])

if __name__ == "__main__":
    n = ch.write(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html"))
    print(f"hoofdstuk {ch.number} — {n} pagina's")

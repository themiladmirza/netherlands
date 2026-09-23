# -*- coding: utf-8 -*-
"""Chapter 2 — In de kantine.  Page composition.

Text lives in content.py, styling in ../shared/style.css,
building blocks in ../shared/lib/layout.py.
Build with:  python3 book/build.py ch02-in-the-canteen
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "shared", "lib")]

from layout import (Chapter, icon, audio_icon, task, card, qa, vocab_rows, pairs,
                    numbers, number_columns, lines, keep, clock)
from content import *

ch = Chapter(2, "In de kantine")

# ---------------------------------------------------------------- 1  COVER
half_i = len(OBJECTIVES)//2 + len(OBJECTIVES) % 2
colA = "".join(f'<li>{o}</li>' for o in OBJECTIVES[:half_i])
colB = "".join(f'<li>{o}</li>' for o in OBJECTIVES[half_i:])
ch.page(f'''
<img src="art/opener.png" style="position:absolute;inset:0;width:100%;height:100%;
     object-fit:cover;object-position:50% 26%">
<div style="position:absolute;left:0;right:0;bottom:0;height:130mm;
     background:linear-gradient(180deg,rgba(253,250,244,0) 0%,rgba(253,250,244,.55) 26%,rgba(253,250,244,1) 46%)"></div>
<div style="position:absolute;left:0;right:0;bottom:0;padding:0 15mm 15mm">
  <div class="kicker" style="color:var(--teal);margin-bottom:2.5mm">Nederlands in gang &nbsp;·&nbsp; Methode Nederlands</div>
  <div style="display:flex;align-items:flex-end;gap:6mm;margin-bottom:7mm">
    <div style="font-family:var(--disp);font-size:78pt;font-weight:800;color:var(--orange);
                line-height:.72;letter-spacing:-.06em">2</div>
    <div style="font-family:var(--disp);font-size:34pt;font-weight:800;letter-spacing:-.035em;
                line-height:.88;color:var(--ink);padding-bottom:1mm">In de kantine</div>
  </div>
  <div style="height:.7pt;background:var(--rule);margin-bottom:5mm"></div>
  <div class="kicker" style="margin-bottom:3mm">In this chapter you will learn</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 8mm">
    <ul class="bullet" style="font-size:9.4pt">{colA}</ul>
    <ul class="bullet" style="font-size:9.4pt">{colB}</ul>
  </div>
</div>''', variant="bleed", head=False, foot=False, nogloss=True)

# ---------------------------------------------------------------- 2  DIALOOG
dl = "".join(f'<dt{" class=you" if s=="Susy" else ""}>{s}:</dt><dd>{t}</dd>' for s, t in DIALOOG)
ch.page(keep("dialoog-2.1", f'''
<h2 class="sec"><span class="num">2.1</span> Dialoog</h2>
<div style="display:flex;align-items:center;gap:2.4mm;margin-bottom:3mm">
  {audio_icon("audio/dialoog.mp3","Susy en Edit in de kantine")}<div style="font-family:var(--disp);font-weight:700;font-size:10pt">Susy en Edit hebben pauze en zitten in de kantine.</div>
</div>
<dl class="dialogue">{dl}</dl>'''), section="2.1 Dialoog")

# ---------------------------------------------------------------- 3  cast + luisteren
ch.page(f'''
<img src="art/dialoog.png" class="img" style="height:52mm;object-fit:cover;margin-bottom:6mm">
{card("Who's who in the dialogue",
 '<div style="display:grid;grid-template-columns:auto 1fr;gap:2.2mm 5mm;font-size:9.3pt">'
 '<div class="dutch" style="color:var(--orange)">Susy</div>'
 '<div>cursist &nbsp;·&nbsp; woont pas drie dagen in Utrecht &nbsp;·&nbsp; jarig in december</div>'
 '<div class="dutch" style="color:var(--orange)">Edit</div>'
 '<div>cursist &nbsp;·&nbsp; morgen jarig &nbsp;·&nbsp; donker haar</div>'
 '<div class="dutch" style="color:var(--orange)">de broer van Edit</div>'
 '<div>jonger, maar wel langer &nbsp;·&nbsp; komt op bezoek</div>'
 '<div class="dutch" style="color:var(--orange)">de zus van Edit</div>'
 '<div>kort, blond haar &nbsp;·&nbsp; een heel ander type</div>'
 '<div class="dutch" style="color:var(--orange)">de ouders van Edit</div>'
 '<div>op dit moment in Indonesië &nbsp;·&nbsp; op vakantie en voor het werk</div>'
 '</div>')}
<div class="sp"></div>
{card("Listening", '<div style="display:flex;gap:3mm;align-items:flex-start">'+icon("web")+
 '<div>Listen to this dialogue at <b>coutinho.nl/nederlandsingang3</b> and repeat the sentences. '
 'Each time you listen you will understand more.</div></div>', "teal")}''', section="2.1 Dialoog")

# ---------------------------------------------------------------- 4-5  WOORDENLIJST
half = 38
ch.page(keep("woordenlijst-a", f'''
<h2 class="sec"><span class="num">2.2</span> Woordenlijst</h2>
<div class="note" style="margin-bottom:3.5mm">The words appear in the order they occur in the dialogue.
The infinitive or singular form is given in brackets.</div>
{vocab_rows(VOC[:half])}'''), section="2.2 Woordenlijst")
ch.page(keep("woordenlijst-b", f'''{vocab_rows(VOC[half:])}
<div class="sp2"></div>
{card(None,'<div style="display:flex;gap:3mm;align-items:flex-start">'+icon("web")+
 '<div>The full word list is also online in <b>Dutch, English, German and Arabic</b>.</div></div>')}'''),
 section="2.2 Woordenlijst")

# ---------------------------------------------------------------- 6  opdracht 1
o1 = "".join(f'<li>{q}</li>' for q in OPD1)
ch.page(keep("opdracht-1", task(1, "speak", None, "Answer the questions.",
  f'<ol class="items" style="line-height:2.2">{o1}</ol>')), section="2.2 Woordenlijst")

# ---------------------------------------------------------------- 7  2.3 familierelaties
def famcol(rows):
    return "".join(f'<div class="dutch">{a}</div><div style="color:var(--teal)">{b}</div>'
                   for a, b in rows)
ch.page(keep("familie-2.3", f'''
<h2 class="sec"><span class="num">2.3</span> Familierelaties</h2>
{card(None,
 '<div style="display:grid;grid-template-columns:auto 1fr auto 1fr;gap:1.3mm 5mm;font-size:9.3pt">'
 + "".join(f'<div class="dutch">{a}</div><div style="color:var(--teal)">{b}</div>'
           f'<div class="dutch">{c}</div><div style="color:var(--teal)">{d}</div>'
           for (a, b), (c, d) in zip(FAMILIE_A + [("", "")], FAMILIE_B))
 + '</div>')}
<img src="art/familie.png" class="img" style="height:62mm;object-fit:cover;margin-top:2mm">'''),
 section="2.3 Familierelaties")

# ---------------------------------------------------------------- 8  2.4 + opdracht 2
besch = "<br>".join(BESCHRIJVEN)
ch.page(f'''
<h2 class="sec"><span class="num">2.4</span> Beschrijven van mensen
  <span style="font-size:10pt;color:var(--ink-faint);font-weight:600">describing people</span></h2>
{card(None, f'<div style="font-size:9.6pt;line-height:1.85">{besch}</div>')}
<div class="sp"></div>
{task(2,"speak",None,"You will see photos of families. Work in pairs. Choose one person from a family.",
 '<div style="display:grid;grid-template-columns:6mm 1fr;gap:1.6mm 2mm;font-size:9.4pt">'
 '<div class="dutch" style="color:var(--orange)">A</div><div>Beschrijf hoe hij / zij eruitziet.</div>'
 '<div class="dutch" style="color:var(--orange)">B</div>'
 '<div>Vertel / fantaseer:<br>1&nbsp; Hoe heet hij / zij?<br>2&nbsp; Hoe oud is hij / zij?</div>'
 '<div class="dutch" style="color:var(--orange)">C</div>'
 '<div>Vertel / fantaseer over zijn / haar broers en zussen en ouders:<br>'
 '1&nbsp; Wat doen ze?<br>2&nbsp; Waar wonen ze?<br>3&nbsp; Waar zijn ze nu (op de foto)?</div>'
 '</div>')}
<img src="art/gezinnen.png" class="img" style="height:50mm;object-fit:cover;margin-top:3mm">''',
 section="2.4 Beschrijven van mensen")

# ---------------------------------------------------------------- 9  2.5 / 2.6 / 2.7
hz = "".join(f'<div class="dutch">{a}</div><div style="color:var(--orange);font-weight:600">{b}</div>'
             f'<div>{c}</div><div>{d}</div>' for a, b, c, d in HOOFDZIN)
ch.page(f'''
<h2 class="sec"><span class="num">2.5</span> Hoofdzin</h2>
{card(None, f'<div style="display:grid;grid-template-columns:auto auto auto 1fr;'
            f'gap:1.6mm 6mm;font-size:9.5pt">{hz}</div>')}
<div class="sp"></div>
<h2 class="sec"><span class="num">2.6</span> Ja / nee-vragen</h2>
{card(None, '<div style="font-size:9.5pt;line-height:1.8">' + "<br>".join(JANEE) + '</div>')}
<div class="sp"></div>
<h2 class="sec"><span class="num">2.7</span> Vraagwoordvragen</h2>
{card(None, '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.2mm 6mm;font-size:9.4pt">'
 '<div>' + "<br>".join(VRAAGWOORD_A) + '</div>'
 '<div>' + "<br>".join(VRAAGWOORD_B) + '</div></div>')}''',
 section="2.7 Vraagwoordvragen")

# ---------------------------------------------------------------- 10  opdracht 3
o3 = "".join(f'<li><div class="qline">{q.replace("___", chr(60)+"span class=blank"+chr(62)+chr(60)+"/span"+chr(62))}'
             f'</div><div class="aline">{a}</div></li>' for q, a in OPD3)
ch.page(keep("opdracht-3", task(3, "write", None,
  "Fill in a question word. Look at the answer!",
  f'<ol class="items qa-items">{o3}</ol>')), section="2.7 Vraagwoordvragen")

# ---------------------------------------------------------------- 11  2.8 possessief
pp = "".join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in POSSESSIEF)
ch.page(keep("possessief-2.8", f'''
<h2 class="sec"><span class="num">2.8</span> Possessief pronomen</h2>
{card(None, '<div style="font-size:9.5pt;line-height:1.8">'
 '<b>Mijn</b> broer komt.<br>Komen <b>je</b> ouders ook op bezoek?</div>')}
<table class="grid"><thead><tr><th style="width:34%">subject</th>
<th>possessief pronomen</th></tr></thead><tbody>{pp}</tbody></table>'''),
 section="2.8 Possessief pronomen")

# ---------------------------------------------------------------- 12  opdracht 4
o4 = "".join('<li>' + s.replace("___", '<span class="blank"></span>') + '</li>' for s in OPD4)
ch.page(keep("opdracht-4", task(4, "write", None, "Fill in a possessive pronoun.",
  f'<ol class="items" style="line-height:2.5">{o4}</ol>')), section="2.8 Possessief pronomen")

# ---------------------------------------------------------------- 13  2.9 de klok
kl = "".join(f'<div class="dutch">{t}</div><div>{p}</div>' for t, p in KLOK)
du = "".join(f'<div class="dutch">{a}</div><div style="color:var(--teal)">{b}</div>' for a, b in DUUR)
faces = "".join(clock(h, m, lbl) for h, m, lbl in KLOK_FACES)
ch.page(keep("klok-2.9", f'''
<h2 class="sec"><span class="num">2.9</span> De klok</h2>
{card("Hoe laat is het?",
 f'<div style="display:grid;grid-template-columns:auto 1fr;gap:1.2mm 5mm;font-size:9.4pt">{kl}</div>'
 f'<div style="height:3.5mm"></div>'
 f'<div style="display:grid;grid-template-columns:auto 1fr;gap:1.2mm 5mm;font-size:9.4pt;'
 f'max-width:70mm">{du}</div>')}
<div class="clocks">{faces}</div>'''), section="2.9 De klok")

# ---------------------------------------------------------------- 14  opdracht 5 + 6
o5 = "".join(f'<li>{q}</li>' for q in OPD5)
ch.page(f'''
{task(5,"speak",None,"Ask the person next to you.", f'<ul class="bullet">{o5}</ul>')}
{task(6,"read",None,"Your teacher will give you a worksheet.")}''', section="2.9 De klok")

# ---------------------------------------------------------------- 15  2.10 dagen
o7 = "".join(f'<li>{q}</li>' for q in OPD7)
ch.page(keep("dagen-2.10", f'''
<h2 class="sec"><span class="num">2.10</span> De dagen van de week</h2>
{card('dagen &nbsp;<em>days</em>',
 '<div style="font-size:9.6pt;line-height:1.9">' + "<br>".join(DAGEN) + '</div>')}
<div class="sp"></div>
{task(7,"speak",None,"Ask the person next to you.", f'<ul class="bullet">{o7}</ul>')}'''),
 section="2.10 De dagen van de week")

# ---------------------------------------------------------------- 16  2.11 maanden
mn = "".join('<div>' + "<br>".join(col) + '</div>' for col in MAANDEN)
o8 = "".join(f'<li>{q}</li>' for q in OPD8)
ch.page(keep("maanden-2.11", f'''
<h2 class="sec"><span class="num">2.11</span> Maanden en seizoenen</h2>
{card('maanden &nbsp;<em>months</em>',
 f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0 5mm;'
 f'font-size:9.5pt;line-height:1.8">{mn}</div>')}
{card('seizoenen &nbsp;<em>seasons</em>',
 '<div style="font-size:9.5pt;line-height:1.8">' + "<br>".join(SEIZOENEN) + '</div>', "teal")}
<img src="art/seizoenen.png" class="img" style="height:34mm;object-fit:cover;margin-bottom:5mm">
{task(8,"speak",None,"Ask the person next to you.", f'<ul class="bullet">{o8}</ul>')}
{task(9,"speak",None,"Name something you associate with each month. Which is your favourite month?")}'''),
 section="2.11 Maanden en seizoenen")

# ---------------------------------------------------------------- 17  opdracht 10
o10 = "".join('<li>' + s.replace("___", '<span class="blank" style="min-width:16mm"></span>')
              + '</li>' for s in OPD10)
ch.page(keep("opdracht-10", task(10, "write", "Een prepositie invullen",
  "Fill in: <b>op</b>, <b>om</b> or <b>in</b>.",
  f'<ol class="items" style="line-height:2.4">{o10}</ol>')),
  section="2.11 Maanden en seizoenen")

# ---------------------------------------------------------------- 18  opdracht 11 + 12
ch.page(f'''
{task(11,"speak","Interviewen",None,
 '<div style="display:grid;grid-template-columns:6mm 1fr;gap:2.2mm 2mm;font-size:9.4pt">'
 '<div class="dutch" style="color:var(--orange)">A</div>'
 '<div>Work in pairs. Think up questions for an interview. Use the word list, and use both '
 'types of question: the <i>ja / nee</i>-question and the question-word question.</div>'
 '<div class="dutch" style="color:var(--orange)">B</div>'
 '<div>Form new pairs. Interview each other using the questions from part A.</div></div>')}
<div class="sp"></div>
{task(12,"write","Een tekst schrijven","Choose task A or B.",
 '<div style="display:grid;grid-template-columns:6mm 1fr;gap:2.2mm 2mm;font-size:9.4pt">'
 '<div class="dutch" style="color:var(--orange)">A</div>'
 '<div>Schrijf een tekst bij een foto van opdracht 2.</div>'
 '<div class="dutch" style="color:var(--orange)">B</div>'
 '<div>Schrijf een tekst bij een foto van je familie.</div></div>')}''',
 section="2.11 Maanden en seizoenen")

# ---------------------------------------------------------------- 19  2.12 tekst
ch.page(keep("tekst-2.12", f'''
<h2 class="sec"><span class="num">2.12</span> Tekst</h2>
<div style="display:flex;gap:8mm;align-items:flex-start">
  <div style="flex:1">
  {task(13,"read",None,"Wat is dit?",
   '<div style="display:grid;grid-template-columns:6mm 1fr;gap:1.6mm 2mm;font-size:9.5pt">'
   '<div class="dutch" style="color:var(--orange)">a</div><div>een adres</div>'
   '<div class="dutch" style="color:var(--orange)">b</div><div>een postcode</div>'
   '<div class="dutch" style="color:var(--orange)">c</div><div>een telefoonnummer</div></div>')}
  </div>
  <div style="flex:0 0 auto;padding-top:6mm">
    <div class="sign"><div class="big">1-1-2</div><div class="small">ALS ELKE<br>SECONDE TELT</div></div>
  </div>
</div>'''), section="2.12 Tekst")

# ---------------------------------------------------------------- 20  2.13 + opdracht 14
dt = "".join('<div>' + "<br>".join(col) + '</div>' for col in zip(*DATING))
ch.page(keep("uitspraak-2.13", f'''
<h2 class="sec"><span class="num">2.13</span> Uitspraak: a – aa</h2>
{task(14,"speak","Vocalen",
 "You work at a dating agency — an odd one: you match people who share the same first vowel. "
 "These people are looking for a partner:",
 f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0 5mm;font-size:9.5pt;'
 f'line-height:1.9;margin:1mm 0 3mm">{dt}</div>'
 f'<div class="note" style="font-style:normal">{DATING_NOTE}</div>')}'''),
 section="2.13 Uitspraak")

# ---------------------------------------------------------------- 21  opdracht 15
rows5 = "".join(f'<tr><td>{i}</td><td></td><td></td></tr>' for i in range(1, 6))
rows7 = "".join(f'<tr><td>{i}</td><td></td><td></td><td></td></tr>' for i in range(1, 8))
ch.page(keep("opdracht-15", f'''
{task(15,"audio","a – aa",None,
 '<div style="display:grid;grid-template-columns:6mm 1fr;gap:2.4mm 2mm;font-size:9.4pt">'
 '<div class="dutch" style="color:var(--orange)">A</div>'
 '<div>You hear two words each time. Is it the same sound (+) or a different one (–)?</div>'
 '</div>'
 f'<table class="grid tick" style="max-width:62mm;margin:3mm 0 6mm">'
 f'<thead><tr><th style="width:12mm"></th><th>+</th><th>–</th></tr></thead>'
 f'<tbody>{rows5}</tbody></table>'
 '<div style="display:grid;grid-template-columns:6mm 1fr;gap:2.4mm 2mm;font-size:9.4pt">'
 '<div class="dutch" style="color:var(--orange)">B</div>'
 '<div>You hear three words each time. Which two have the same sound?</div></div>'
 '<div class="example" style="max-width:74mm;margin:3mm 0 2mm"><div class="lbl">Example</div>'
 '<table class="grid tick noindex" style="margin:0"><thead><tr><th>jarig</th><th>naam</th><th>dag</th></tr></thead>'
 '<tbody><tr><td>+</td><td>+</td><td>–</td></tr></tbody></table></div>'
 f'<table class="grid tick" style="max-width:74mm;margin:3mm 0 0">'
 f'<tbody>{rows7}</tbody></table>')}'''), section="2.13 Uitspraak")

# ---------------------------------------------------------------- 22  opdracht 16
o16 = "".join('<div class="wordrow">' + " &nbsp;<span>&#9642;</span>&nbsp; ".join(row) + '</div>'
              for row in OPD16)
ch.page(keep("opdracht-16", task(16, "audio", "a – aa",
  "Listen carefully to these words and repeat them.",
  f'<div style="font-size:10pt;line-height:2.4;margin-top:2mm">{o16}</div>',
  audio="audio/opdracht16.mp3")), section="2.13 Uitspraak")

# ---------------------------------------------------------------- 23  cultuur + praktijk
ch.page(f'''
<div class="kicker">Cultuur</div>
<h2 class="sec" style="font-size:15pt">Hoeveel kinderen?</h2>
{card(None, f'<div style="font-size:9.6pt;line-height:1.8">{CULTUUR}</div>')}
<div class="sp2"></div>
<div class="kicker">In de praktijk</div>
<h2 class="sec" style="font-size:15pt">Hoe laat is het?</h2>
{card(None, f'<div style="font-size:9.6pt">{PRAKTIJK}</div>', "teal")}
<img src="art/praktijk.png" class="img" style="height:58mm;object-fit:cover;margin-top:5mm">''',
 section="In de praktijk")

# ---------------------------------------------------------------- 24  eigen vocabulaire
wl = '<div class="lines">' + '<div class="ln"></div>'*22 + '</div>'
ch.page(f'''
<div class="kicker">Eigen vocabulaire</div>
<h2 class="sec" style="font-size:15pt">Eigen vocabulaire</h2>
<div style="margin-bottom:5mm">The theme of this chapter is <b>In de kantine</b>.
Which words would you like to add? Write them below.</div>
<div class="two" style="gap:0 8mm">{wl}{wl}</div>''', section="Eigen vocabulaire")

# ---------------------------------------------------------------- 25  reflectie
rr = "".join(f'<div class="fr" style="grid-template-columns:1fr 27mm">'
  f'<div>{r}</div><div style="text-align:right"><span class="box"></span>'
  f'<span class="note" style="font-style:normal;margin-right:3mm">yes</span>'
  f'<span class="box"></span><span class="note" style="font-style:normal">not yet</span></div></div>'
  for r in REFLECTIE)
ch.page(f'''
<div class="kicker">Reflectie</div>
<h2 class="sec" style="font-size:15pt">What can you do now?</h2>
<div class="form" style="padding:5mm 6mm">{rr}</div>
<div class="sp2"></div>
<div style="display:flex;gap:5mm;align-items:flex-start">
 <img src="art/reflectie.png" style="width:52mm;height:52mm;object-fit:cover;border-radius:3mm;flex:0 0 auto">
 <div>
  <div style="display:flex;gap:2.4mm;align-items:center;margin-bottom:2.5mm">{icon("web")}
   <div style="font-family:var(--disp);font-weight:700;font-size:10.5pt">Verdiepingsmateriaal</div></div>
  <div style="margin-bottom:2mm">At <b>coutinho.nl/nederlandsingang3</b> you can work on:</div>
  <ul class="bullet"><li>grammar and pronunciation videos</li><li>a gap-fill of the dialogue</li>
   <li>extra exercises</li><li>an intensive listening text</li></ul>
 </div>
</div>''', section="Reflectie")

# ---------------------------------------------------------------- PDF bookmarks
ch.toc = [
 [1,"Hoofdstuk 2 — In de kantine",1],
 [2,"2.1  Dialoog — in de kantine",2],
 [3,"Who's who in the dialogue",3],
 [2,"2.2  Woordenlijst",4],
 [3,"Opdracht 1",6],
 [2,"2.3  Familierelaties",7],
 [2,"2.4  Beschrijven van mensen",8],
 [3,"Opdracht 2",8],
 [2,"2.5  Hoofdzin",9],
 [2,"2.6  Ja / nee-vragen",9],
 [2,"2.7  Vraagwoordvragen",9],
 [3,"Opdracht 3",10],
 [2,"2.8  Possessief pronomen",11],
 [3,"Opdracht 4",12],
 [2,"2.9  De klok",13],
 [3,"Opdracht 5–6",14],
 [2,"2.10  De dagen van de week",15],
 [3,"Opdracht 7",15],
 [2,"2.11  Maanden en seizoenen",16],
 [3,"Opdracht 8–9",16],
 [3,"Opdracht 10: Een prepositie invullen",17],
 [3,"Opdracht 11: Interviewen",18],
 [3,"Opdracht 12: Een tekst schrijven",18],
 [2,"2.12  Tekst",19],
 [3,"Opdracht 13",19],
 [2,"2.13  Uitspraak: a – aa",20],
 [3,"Opdracht 14: Vocalen",20],
 [3,"Opdracht 15",21],
 [3,"Opdracht 16",22],
 [2,"Cultuur",23],
 [2,"In de praktijk",23],
 [2,"Eigen vocabulaire",24],
 [2,"Reflectie — wat kun je nu?",25],
]

if __name__ == "__main__":
    n = ch.write(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html"))
    print(f"hoofdstuk {ch.number} — {n} pagina's")

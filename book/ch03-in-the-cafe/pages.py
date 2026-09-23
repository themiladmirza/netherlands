# -*- coding: utf-8 -*-
"""Chapter 3 — In het café.  Page composition.

Text lives in content.py, styling in ../shared/style.css,
building blocks in ../shared/lib/layout.py.
Build with:  python3 book/build.py ch03-in-the-cafe
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "shared", "lib")]

from layout import (Chapter, icon, audio_icon, task, card, qa, vocab_rows, pairs,
                    numbers, number_columns, lines, keep, clock)
from content import *

ch = Chapter(3, "In het café")
YOU = {"Susy", "Andres", "Susy en Andres", "Ober"}

# ---------------------------------------------------------------- 1  COVER
half_i = len(OBJECTIVES)//2 + len(OBJECTIVES) % 2
colA = "".join(f'<li>{o}</li>' for o in OBJECTIVES[:half_i])
colB = "".join(f'<li>{o}</li>' for o in OBJECTIVES[half_i:])
ch.page(f'''
<img src="art/opener.png" style="position:absolute;inset:0;width:100%;height:100%;
     object-fit:cover;object-position:50% 40%">
<div style="position:absolute;left:0;right:0;bottom:0;height:130mm;
     background:linear-gradient(180deg,rgba(253,250,244,0) 0%,rgba(253,250,244,.55) 26%,rgba(253,250,244,1) 46%)"></div>
<div style="position:absolute;left:0;right:0;bottom:0;padding:0 15mm 15mm">
  <div class="kicker" style="color:var(--teal);margin-bottom:2.5mm">Nederlands in gang &nbsp;·&nbsp; Methode Nederlands</div>
  <div style="display:flex;align-items:flex-end;gap:6mm;margin-bottom:7mm">
    <div style="font-family:var(--disp);font-size:78pt;font-weight:800;color:var(--orange);
                line-height:.72;letter-spacing:-.06em">3</div>
    <div style="font-family:var(--disp);font-size:36pt;font-weight:800;letter-spacing:-.035em;
                line-height:.88;color:var(--ink);padding-bottom:1mm">In het café</div>
  </div>
  <div style="height:.7pt;background:var(--rule);margin-bottom:5mm"></div>
  <div class="kicker" style="margin-bottom:3mm">In this chapter you will learn</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 8mm">
    <ul class="bullet" style="font-size:9.4pt">{colA}</ul>
    <ul class="bullet" style="font-size:9.4pt">{colB}</ul>
  </div>
</div>''', variant="bleed", head=False, foot=False, nogloss=True)

# ---------------------------------------------------------------- 2  DIALOOG
def turns(rows):
    return "".join(f'<dt{" class=you" if s in YOU else ""}>{s}:</dt><dd>{t}</dd>'
                   for s, t in rows)
BREAK = ('<div style="color:var(--ink-faint);font-style:italic;font-size:9pt;'
         'margin:2.6mm 0 2.6mm 25mm">{}</div>')
ch.page(keep("dialoog-3.1", f'''
<h2 class="sec"><span class="num">3.1</span> Dialoog</h2>
<div style="display:flex;align-items:flex-start;gap:2.4mm;margin-bottom:3mm">
  {audio_icon("audio/dialoog.mp3","Edit viert haar verjaardag")}<div style="font-family:var(--disp);font-weight:700;font-size:10pt">{DIALOOG_INTRO}</div>
</div>
<dl class="dialogue tight">{turns(DIALOOG)}</dl>
{BREAK.format("(een poosje later)")}
<dl class="dialogue tight">{turns(DIALOOG_2)}</dl>
{BREAK.format("(nog weer later)")}
<dl class="dialogue tight">{turns(DIALOOG_3)}</dl>'''), section="3.1 Dialoog")

# ---------------------------------------------------------------- 3  cast + luisteren
ch.page(f'''
<img src="art/dialoog.png" class="img" style="height:52mm;object-fit:cover;margin-bottom:6mm">
{card("Who's who in the dialogue",
 '<div style="display:grid;grid-template-columns:auto 1fr;gap:2.2mm 5mm;font-size:9.3pt">'
 '<div class="dutch" style="color:var(--orange)">Edit</div>'
 '<div>is jarig &nbsp;·&nbsp; trakteert &nbsp;·&nbsp; betaalt het eerste rondje</div>'
 '<div class="dutch" style="color:var(--orange)">Andres</div>'
 '<div>de broer van Edit &nbsp;·&nbsp; betaalt het tweede rondje</div>'
 '<div class="dutch" style="color:var(--orange)">Susy</div>'
 '<div>kent Edit van de cursus Nederlands</div>'
 '<div class="dutch" style="color:var(--orange)">de ober</div>'
 '<div>neemt de bestelling op</div>'
 '</div>')}
<div class="sp"></div>
{card("Listening", '<div style="display:flex;gap:3mm;align-items:flex-start">'+icon("web")+
 '<div>Listen to this dialogue at <b>coutinho.nl/nederlandsingang3</b> and repeat the sentences. '
 'Each time you listen you will understand more.</div></div>', "teal")}''', section="3.1 Dialoog")

# ---------------------------------------------------------------- 4-5  WOORDENLIJST
# 51 entries need two pages; Opdracht 1 joins the continuation so neither runs thin
half = 34
ch.page(keep("woordenlijst-a", f'''
<h2 class="sec"><span class="num">3.2</span> Woordenlijst</h2>
<div class="note" style="margin-bottom:3.5mm">The words appear in the order they occur in the dialogue.
The infinitive or singular form is given in brackets.</div>
{vocab_rows(VOC[:half])}'''), section="3.2 Woordenlijst")

o1 = "".join(f'<li><div class="stem">{s}</div>'
             f'<div class="opt"><span>a</span>{a}</div>'
             f'<div class="opt"><span>b</span>{b}</div></li>' for s, a, b in OPD1)
ch.page(f'''
{keep("woordenlijst-b", vocab_rows(VOC[half:]))}
<div class="sp"></div>
{card(None,'<div style="display:flex;gap:3mm;align-items:flex-start">'+icon("web")+
 '<div>The full word list is also online in <b>Dutch, English, German and Arabic</b>.</div></div>')}
<div class="sp"></div>
{keep("opdracht-1", task(1, "read", None, "Choose the correct ending: a or b.",
  f'<ol class="items choice-items">{o1}</ol>'))}''', section="3.2 Woordenlijst")

# ---------------------------------------------------------------- 7  3.3 / 3.4 / 3.5
ch.page(f'''
<h2 class="sec"><span class="num">3.3</span> Bestellen</h2>
{card(None,'<div style="font-size:9.6pt;line-height:1.85">' + "<br>".join(BESTELLEN) + '</div>')}
{task(2,"speak",None,
 "One person orders something. The next repeats it and orders something too. The third "
 "repeats the first two orders and adds their own.","",
 '<div class="example"><div class="lbl">Example</div>'
 '<div style="line-height:1.7"><b>A:</b> Ik wil graag een cola.<br>'
 '<b>B:</b> Voor mij een cola en een biertje.<br>'
 '<b>C:</b> Mag ik een cola, een biertje en een rode wijn?<br>'
 '<b>D:</b> …</div></div>')}
<div class="sp"></div>
<h2 class="sec"><span class="num">3.4</span> Afrekenen</h2>
{card(None,'<div style="font-size:9.6pt;line-height:1.85">' + "<br>".join(AFREKENEN) + '</div>')}
<div class="sp"></div>
<h2 class="sec"><span class="num">3.5</span> Bedanken</h2>
{card(None,'<div style="font-size:9.6pt;line-height:1.85">' + "<br>".join(BEDANKEN) + '</div>',"teal")}''',
 section="3.5 Bedanken")

# ---------------------------------------------------------------- 8  opdracht 3
ch.page(f'''
{task(3,"speak","Variëren in de dialoog",
 "Work in groups of three: 1 = Edit, 2 = Susy, 3 = Andres + the waiter.",
 '<div style="font-size:9.5pt;line-height:1.8;margin-bottom:1mm">'
 'Lees de tekst twee keer voor.<br>Lees de eerste keer de tekst gewoon.<br>'
 'Maak de tweede keer veranderingen in de tekst.</div>',
 '<div class="example"><div class="lbl">Example</div>'
 '<div style="display:grid;grid-template-columns:1fr 1fr;gap:2mm">'
 '<div>Ik neem rode wijn.</div><div>Ik wil witte wijn.</div></div></div>')}
<img src="art/bestellen.png" class="img" style="height:62mm;object-fit:cover;margin-top:6mm">''',
 section="3.5 Bedanken")

# ---------------------------------------------------------------- 9  opdracht 4
o4 = ""
for s, t in OPD4:
    if not s:
        o4 += '<dt></dt><dd style="height:2.4mm"></dd>'
    else:
        o4 += (f'<dt>{s}:</dt><dd>'
               + t.replace("___", '<span class="blank" style="min-width:26mm"></span>') + '</dd>')
ch.page(keep("opdracht-4", task(4, "write", "De tekst compleet maken",
  "Complete the café conversation. Fill in one or two words.",
  f'<div class="note" style="font-style:normal;margin-bottom:3mm">{OPD4_INTRO}</div>'
  f'<dl class="dialogue">{o4}</dl>')), section="3.5 Bedanken")

# ---------------------------------------------------------------- 10  3.6 artikel
ar = "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in ARTIKEL)
ch.page(keep("artikel-3.6", f'''
<h2 class="sec"><span class="num">3.6</span> Artikel</h2>
{card(None,'<div style="font-size:9.4pt;line-height:1.8">' + "<br>".join(ARTIKEL_EX) + '</div>')}
<table class="grid"><thead><tr><th style="width:30%"></th><th>definiet</th>
<th>indefiniet</th></tr></thead><tbody>{ar}</tbody></table>
<div class="sp"></div>
{card('diminutief', '<div style="font-size:9.6pt;line-height:1.85">'
 + "<br>".join(DIMINUTIEF) + '</div>', "teal")}'''), section="3.6 Artikel")

# ---------------------------------------------------------------- 11  opdracht 5
o5 = "".join('<div>' + "<br>".join(col) + '</div>' for col in OPD5)
ch.page(keep("opdracht-5", task(5, "write", None,
  "Choose the correct article for each word: <b>de</b> or <b>het</b>. Check your answers against "
  "the word list. Note down the words you got wrong, with the right article.",
  f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0 6mm;font-size:10pt;'
  f'line-height:2.3;margin-top:2mm;max-width:100mm">{o5}</div>')), section="3.6 Artikel")

# ---------------------------------------------------------------- 12  3.7 inversie
iv = "".join(f'<div class="dutch">{a}</div><div style="color:var(--orange);font-weight:600">{b}</div>'
             f'<div class="dutch">{c}</div><div>{d}</div>' for a, b, c, d in INVERSIE)
o6 = "".join(f'<li>{a} <b style="color:var(--teal)">{b}</b>{(" " + c) if c else ""}</li>'
             for a, b, c in OPD6)
ch.page(keep("inversie-3.7", f'''
<h2 class="sec"><span class="num">3.7</span> Hoofdzin met inversie</h2>
{card(None, f'<div style="display:grid;grid-template-columns:auto auto auto 1fr;'
            f'gap:1.6mm 6mm;font-size:9.6pt">{iv}</div>')}
{task(6,"speak",None,"Read the sentence, but start with the highlighted part.",
 f'<ol class="items" style="line-height:2.05">{o6}</ol>',
 '<div class="example" style="margin-bottom:3mm"><div class="lbl">Example</div>'
 '<div style="display:grid;grid-template-columns:1fr 1fr;gap:2mm">'
 '<div>Ik wil <b style="color:var(--teal)">nu</b> een cola.</div>'
 '<div><b>Nu</b> wil ik een cola.</div></div></div>')}'''), section="3.7 Inversie")

# ---------------------------------------------------------------- 13  3.8 rangtelwoorden
def rang(rows):
    return ('<div class="numbers">'
            + "".join(f'<div class="n"><b>{n}</b><span>{w}</span></div>' for n, w in rows)
            + '</div>')
o7 = "".join(f'<li>{q}</li>' for q in OPD7)
ch.page(keep("rangtelwoorden-3.8", f'''
<h2 class="sec"><span class="num">3.8</span> Rangtelwoorden</h2>
{card(None, '<div class="numcols">' + rang(RANG_A) + rang(RANG_B) + rang(RANG_C) + '</div>')}
<div class="sp"></div>
{task(7,"speak",None,"Ask the person next to you.", f'<ul class="bullet">{o7}</ul>')}'''),
 section="3.8 Rangtelwoorden")

# ---------------------------------------------------------------- 14  opdracht 8 + 9
cloud = " ".join(f'<span style="font-size:{sz}pt">{w}</span>' for w, sz in WOORDWOLK)
ch.page(f'''
{task(8,"speak","Woordwolk",
 "Here is a word cloud. Talk in pairs. Make sentences with the words from the cloud. Use every word.",
 f'<div class="wordcloud">{cloud}</div>')}
<div class="sp"></div>
{task(9,"write","Reageren op een uitnodiging","You receive this invitation by e-mail:",
  f'<div class="mail">{OPD9_MAIL}</div>',
  '<div style="margin-top:3.5mm">Schrijf een reactie naar Benedetta.</div>'
  + '<div class="lines" style="margin-top:3mm">' + '<div class="ln"></div>'*6 + '</div>')}''',
 section="3.8 Rangtelwoorden")

# ---------------------------------------------------------------- 16  3.9 tekst
ch.page(keep("tekst-3.9", f'''
<h2 class="sec"><span class="num">3.9</span> Tekst</h2>
<div style="display:flex;gap:3mm;align-items:flex-start;margin-bottom:5mm">{icon("read")}
  <div class="readbox">{TEKST}</div></div>
{task(10,"read",None,"Op welke foto staat dit café?")}
<div style="position:relative;margin-top:2mm">
  <img src="art/cafes.png" class="img" style="height:56mm;object-fit:cover">
  <div class="photolabels"><span>a</span><span>b</span><span>c</span></div>
</div>'''), section="3.9 Tekst")

# ---------------------------------------------------------------- 17  3.10 + opdracht 11
o11 = "".join('<div>' + "<br>".join(col) + '</div>' for col in OPD11)
ch.page(keep("uitspraak-3.10", f'''
<h2 class="sec"><span class="num">3.10</span> Uitspraak: o – oo</h2>
{task(11,"audio","Woordaccent",
 "Which part of the word carries the stress, the accent? Underline that part.",
 f'<div class="example" style="max-width:52mm;margin:0 0 4mm"><div class="lbl">Example</div>'
 f'<div>be<u>gin</u>nen</div></div>'
 f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0 6mm;font-size:10pt;'
 f'line-height:2.3;max-width:110mm">{o11}</div>',
 audio="audio/opdracht11.mp3")}'''), section="3.10 Uitspraak")

# ---------------------------------------------------------------- 18  opdracht 12
rows10 = "".join(f'<tr><td>{i}</td><td></td><td></td></tr>' for i in range(1, 11))
ch.page(keep("opdracht-12", task(12, "audio", "o – oo",
  "You hear two words each time. Is it the same sound (+) or a different one (–)?",
  f'<table class="grid tick" style="max-width:62mm;margin:3mm 0 0">'
  f'<thead><tr><th style="width:12mm"></th><th>+</th><th>–</th></tr></thead>'
  f'<tbody>{rows10}</tbody></table>')), section="3.10 Uitspraak")

# ---------------------------------------------------------------- 19  opdracht 13
o13 = "".join('<div class="wordrow">' + " &nbsp;<span>&#9642;</span>&nbsp; ".join(row) + '</div>'
              for row in OPD13)
ch.page(keep("opdracht-13", task(13, "audio", "o – oo",
  "Listen carefully to these words and repeat them.",
  f'<div style="font-size:10pt;line-height:2.4;margin-top:2mm">{o13}</div>',
  audio="audio/opdracht13.mp3")), section="3.10 Uitspraak")

# ---------------------------------------------------------------- 20  cultuur + praktijk
ch.page(f'''
<div class="kicker">Cultuur</div>
<h2 class="sec" style="font-size:15pt">{CULTUUR_VRAAG}</h2>
{card(None,'<div style="font-size:9.6pt;line-height:1.9">' + "<br>".join(CULTUUR) + '</div>')}
<div class="sp2"></div>
<div class="kicker">In de praktijk</div>
<h2 class="sec" style="font-size:15pt">Bestel iets in het Nederlands</h2>
{card(None, f'<div style="font-size:9.6pt">{PRAKTIJK}</div>', "teal")}
<img src="art/praktijk.png" class="img" style="height:56mm;object-fit:cover;margin-top:5mm">''',
 section="In de praktijk")

# ---------------------------------------------------------------- 21  eigen vocabulaire
wl = '<div class="lines">' + '<div class="ln"></div>'*22 + '</div>'
ch.page(f'''
<div class="kicker">Eigen vocabulaire</div>
<h2 class="sec" style="font-size:15pt">Eigen vocabulaire</h2>
<div style="margin-bottom:5mm">The theme of this chapter is <b>In het café</b>.
Which words would you like to add? Write them below.</div>
<div class="two" style="gap:0 8mm">{wl}{wl}</div>''', section="Eigen vocabulaire")

# ---------------------------------------------------------------- 22  reflectie
rr = "".join(f'<div class="fr" style="grid-template-columns:1fr 27mm">'
  f'<div>{r}</div><div style="text-align:right"><span class="box"></span>'
  f'<span class="note" style="font-style:normal;margin-right:3mm">yes</span>'
  f'<span class="box"></span><span class="note" style="font-style:normal">not yet</span></div></div>'
  for r in REFLECTIE)
vd = "".join(f'<li>{v}</li>' for v in VERDIEPING)
ch.page(f'''
<div class="kicker">Reflectie</div>
<h2 class="sec" style="font-size:15pt">What can you do now?</h2>
<div class="form" style="padding:5mm 6mm">{rr}</div>
<div class="sp2"></div>
<div style="display:flex;gap:5mm;align-items:flex-start">
 <img src="art/reflectie.png" style="width:48mm;height:48mm;object-fit:cover;border-radius:3mm;flex:0 0 auto">
 <div>
  <div style="display:flex;gap:2.4mm;align-items:center;margin-bottom:2.5mm">{icon("web")}
   <div style="font-family:var(--disp);font-weight:700;font-size:10.5pt">Verdiepingsmateriaal</div></div>
  <div style="margin-bottom:2mm">At <b>coutinho.nl/nederlandsingang3</b> you can work on:</div>
  <ul class="bullet">{vd}</ul>
 </div>
</div>''', section="Reflectie")

# ---------------------------------------------------------------- PDF bookmarks
ch.toc = [
 [1,"Hoofdstuk 3 — In het café",1],
 [2,"3.1  Dialoog — Edit viert haar verjaardag",2],
 [3,"Who's who in the dialogue",3],
 [2,"3.2  Woordenlijst",4],
 [3,"Opdracht 1",5],
 [2,"3.3  Bestellen",6],
 [3,"Opdracht 2",6],
 [2,"3.4  Afrekenen",6],
 [2,"3.5  Bedanken",6],
 [3,"Opdracht 3: Variëren in de dialoog",7],
 [3,"Opdracht 4: De tekst compleet maken",8],
 [2,"3.6  Artikel",9],
 [3,"Opdracht 5",10],
 [2,"3.7  Hoofdzin met inversie",11],
 [3,"Opdracht 6",11],
 [2,"3.8  Rangtelwoorden",12],
 [3,"Opdracht 7",12],
 [3,"Opdracht 8: Woordwolk",13],
 [3,"Opdracht 9: Reageren op een uitnodiging",13],
 [2,"3.9  Tekst",14],
 [3,"Opdracht 10",14],
 [2,"3.10  Uitspraak: o – oo",15],
 [3,"Opdracht 11: Woordaccent",15],
 [3,"Opdracht 12",16],
 [3,"Opdracht 13",17],
 [2,"Cultuur",18],
 [2,"In de praktijk",18],
 [2,"Eigen vocabulaire",19],
 [2,"Reflectie — wat kun je nu?",20],
]

if __name__ == "__main__":
    n = ch.write(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html"))
    print(f"hoofdstuk {ch.number} — {n} pagina's")

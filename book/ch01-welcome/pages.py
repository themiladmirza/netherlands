# -*- coding: utf-8 -*-
"""Chapter 1 — Welkom.  Page composition.

Text lives in content.py, styling in ../shared/style.css,
building blocks in ../shared/lib/layout.py.
Build with:  python3 book/build.py ch01-welcome
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "shared", "lib")]

from layout import Chapter, icon, audio_icon, task, card, qa, vocab_rows, pairs, numbers, number_columns, lines, keep
from content import *

ch = Chapter(1, "Welkom")

# ---------------------------------------------------------------- 1  COVER
half_i = len(OBJECTIVES)//2 + len(OBJECTIVES)%2
colA = "".join(f'<li>{o}</li>' for o in OBJECTIVES[:half_i])
colB = "".join(f'<li>{o}</li>' for o in OBJECTIVES[half_i:])
ch.page(f'''
<img src="art/opener.png" style="position:absolute;inset:0;width:100%;height:100%;
     object-fit:cover;object-position:50% 22%">
<div style="position:absolute;left:0;right:0;bottom:0;height:130mm;
     background:linear-gradient(180deg,rgba(253,250,244,0) 0%,rgba(253,250,244,.55) 26%,rgba(253,250,244,1) 46%)"></div>
<div style="position:absolute;left:0;right:0;bottom:0;padding:0 15mm 15mm">
  <div class="kicker" style="color:var(--teal);margin-bottom:2.5mm">Nederlands in gang &nbsp;·&nbsp; Methode Nederlands</div>
  <div style="display:flex;align-items:flex-end;gap:6mm;margin-bottom:7mm">
    <div style="font-family:var(--disp);font-size:78pt;font-weight:800;color:var(--orange);
                line-height:.72;letter-spacing:-.06em">1</div>
    <div style="font-family:var(--disp);font-size:40pt;font-weight:800;letter-spacing:-.035em;
                line-height:.86;color:var(--ink);padding-bottom:1mm">Welkom</div>
  </div>
  <div style="height:.7pt;background:var(--rule);margin-bottom:5mm"></div>
  <div class="kicker" style="margin-bottom:3mm">In this chapter you will learn</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 8mm">
    <ul class="bullet" style="font-size:9.4pt">{colA}</ul>
    <ul class="bullet" style="font-size:9.4pt">{colB}</ul>
  </div>
</div>''', variant="bleed", head=False, foot=False, nogloss=True)

# ---------------------------------------------------------------- 2  DIALOOG
# The whole conversation on one page, as in the original (book p.21). It is
# wrapped in keep() so it can never be split again; the illustration and the
# supporting cards move to the facing page to make room.
dl  = "".join(f'<dt{" class=you" if s!="Docent" else ""}>{s}:</dt><dd>{t}</dd>' for s,t in DIALOOG)
dl3 = "".join(f'<dt>{s}:</dt><dd>{t}</dd>' for s,t in DIALOOG_END)
ch.page(keep("dialoog-1.1", f'''
<h2 class="sec"><span class="num">1.1</span> Dialoog</h2>
<div style="display:flex;align-items:center;gap:2.4mm;margin-bottom:3mm">
  {audio_icon("audio/dialoog.mp3","De cursus begint")}<div style="font-family:var(--disp);font-weight:700;font-size:10pt">De cursus begint.</div>
</div>
<dl class="dialogue">{dl}</dl>
<div style="text-align:center;color:var(--ink-faint);font-family:var(--disp);
            font-size:12pt;letter-spacing:.3em;margin:3.5mm 0">(…)</div>
<dl class="dialogue">{dl3}</dl>'''), section="1.1 Dialoog")

# ---------------------------------------------------------------- 3  DIALOOG — wie & luisteren
ch.page(f'''
<img src="art/dialoog.png" class="img" style="height:52mm;object-fit:cover;margin-bottom:6mm">
{card("Who\'s who in the dialogue",
 '<div style="display:grid;grid-template-columns:auto 1fr;gap:2.2mm 5mm;font-size:9.3pt">'
 '<div class="dutch" style="color:var(--orange)">Karin Dijkstra</div>'
 '<div>de docent &nbsp;·&nbsp; woont al twintig jaar in Utrecht</div>'
 '<div class="dutch" style="color:var(--orange)">Paul de Vries</div>'
 '<div>de andere docent &nbsp;·&nbsp; geeft twee dagen les</div>'
 '<div class="dutch" style="color:var(--orange)">Susy Wall</div>'
 '<div>cursist &nbsp;·&nbsp; komt uit Engeland</div>'
 '<div class="dutch" style="color:var(--orange)">Ning</div>'
 '<div>cursist &nbsp;·&nbsp; komt uit China &nbsp;·&nbsp; Hofstraat 22, 3581 TW Utrecht</div>'
 '</div>')}
<div class="sp"></div>
{card("Listening", '<div style="display:flex;gap:3mm;align-items:flex-start">'+icon("web")+
 '<div>Listen to this dialogue at <b>coutinho.nl/nederlandsingang3</b> and repeat the sentences. '
 'Each time you listen you will understand more.</div></div>', "teal")}''', section="1.1 Dialoog")

# ---------------------------------------------------------------- 4-5  WOORDENLIJST
half = 48
ch.page(keep("woordenlijst-a", f'''
<h2 class="sec"><span class="num">1.2</span> Woordenlijst</h2>
<div class="note" style="margin-bottom:3.5mm">The words appear in the order they occur in the dialogue.
The infinitive or singular form is given in brackets.</div>
{vocab_rows(VOC[:half])}'''), section="1.2 Woordenlijst")
ch.page(keep("woordenlijst-b", f'''{vocab_rows(VOC[half:])}
<div class="sp2"></div>
{card(None,'<div style="display:flex;gap:3mm;align-items:flex-start">'+icon("web")+
 '<div>The full word list is also online in <b>Dutch, English, German and Arabic</b>.</div></div>')}'''),
 section="1.2 Woordenlijst")

# ---------------------------------------------------------------- 6  1.3
ch.page(f'''
<h2 class="sec"><span class="num">1.3</span> Zich voorstellen /<br>informatie vragen / landen</h2>
{card('zich voorstellen &nbsp;<em>introducing yourself</em>', qa(VOORSTELLEN))}
{card('informatie vragen &nbsp;<em>adres en land van herkomst</em>', qa(INFORMATIE), "teal")}
{card('landen / talen / nationaliteiten',
  f'<div style="display:grid;grid-template-columns:1fr 1fr 1.25fr;gap:1.4mm 4mm;font-size:9pt">{"".join(f"<div>{a}</div><div>{b}</div><div>{c}</div>" for a,b,c in LANDEN)}</div>')}''',
 section="1.3 Zich voorstellen")

# ---------------------------------------------------------------- 7  landen + opdracht 1
ch.page(f'''
<img src="art/landen.png" class="img" style="height:78mm;object-fit:cover;margin:0 0 6mm">
{task(1,"speak",None,"Talk to the person next to you. Ask:",
 '<div class="two"><ol class="items"><li>Wie ben jij?</li><li>Wat is je adres?</li>'
 '<li>Uit welk land kom je?</li></ol><ol class="items" start="4" style="counter-reset:it 3">'
 '<li>Welke taal spreek je?</li><li>Wat is je nationaliteit?</li></ol></div>',
 '<div class="note" style="margin-top:2.5mm">Now ask the person on your other side.</div>')}''',
 section="1.3 Zich voorstellen")

# ---------------------------------------------------------------- 8  1.4 verbs
vr = "".join(f'<tr><td>{p}</td><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for p,a,b,c in VERBS)
ch.page(keep("werkwoord-1.4", f'''
<h2 class="sec"><span class="num">1.4</span> Personaal pronomen + werkwoord</h2>
{card(None,
 '<div style="display:grid;grid-template-columns:auto auto 1fr;gap:1.1mm 4mm;font-size:9.3pt">'
 '<div class="dutch">Ik</div><div style="font-style:italic;color:var(--orange);font-weight:600">ben</div><div>Susy.</div>'
 '<div class="dutch">Hij</div><div style="font-style:italic;color:var(--orange);font-weight:600">geeft</div><div>twee dagen les en ik drie.</div>'
 '<div class="dutch">We</div><div style="font-style:italic;color:var(--orange);font-weight:600">luisteren</div><div>naar de tekst.</div>'
 '</div><div style="height:3mm"></div>'
 '<div style="font-size:9.3pt">Waar <i style="color:var(--orange)">woon</i> je?<br>'
 '<i style="color:var(--orange)">Woont</i> u ook in Utrecht?</div>')}
<table class="grid">
 <thead><tr><th style="width:34%"></th><th>luisteren</th><th>hebben</th><th>zijn</th></tr></thead>
 <tbody>{vr}</tbody></table>
<div class="sp"></div>
{card(None,'<div style="display:flex;gap:3mm;align-items:center">'+icon("web")+
 '<div>In de <b>inversie</b> verandert de vorm: <i>je luistert</i> &rarr; <i>luister je?</i> · '
 '<i>je hebt</i> &rarr; <i>heb je?</i> · <i>je bent</i> &rarr; <i>ben je?</i></div></div>',"teal")}'''),
 section="1.4 Personaal pronomen")

# ---------------------------------------------------------------- 9  opdracht 2
o2 = "".join('<li>'+s.replace("___",'<span class="blank"></span>')+'</li>' for s in OPD2)
ch.page(keep("opdracht-2", task(2,"write",None,"Fill in a personal pronoun.",
  f'<ol class="items" style="line-height:2.5">{o2}</ol>')), section="1.4 Personaal pronomen")

# ---------------------------------------------------------------- 10  opdracht 3
o3=""
for pre,choice,post,mode in OPD3:
    
    if mode=="pre": o3 += f'<li>{pre} <span class="choice">{choice}</span> {post}</li>'
    else:           o3 += f'<li><span class="choice">{pre} / {choice}</span> {post}</li>'
ch.page(keep("opdracht-3", task(3,"write",None,"Choose the correct form of the verb.",
  f'<ol class="items" style="line-height:2.1">{o3}</ol>')), section="1.4 Personaal pronomen")

# ---------------------------------------------------------------- 11  1.5 telwoorden
# §1.5 keeps its own exercises. The illustration shrinks to make room rather than
# pushing Opdracht 4-5 onto the next page, where they would sit above §1.6's
# heading with nothing saying which section they belong to.
ch.page(keep("telwoorden-1.5", f'''
<h2 class="sec"><span class="num">1.5</span> Telwoorden</h2>
<div style="display:flex;gap:2.4mm;align-items:center;margin-bottom:3.5mm">{audio_icon("audio/telwoorden.mp3","Telwoorden")}
<div class="note" style="font-style:normal">Listen and repeat.</div></div>
{card(None, number_columns(NUMS_A, NUMS_B, NUMS_C)
  + '<div style="height:3mm"></div>' + numbers(NUMS_D))}
{task(4,"speak",None,"Ask the person next to you.",
 '<ul class="bullet"><li>Wat is je huisnummer?</li><li>Wat is je telefoonnummer?</li>'
 '<li>Wat is je geboortedatum?</li><li>Wat is je postcode?</li></ul>')}
{task(5,"read",None,"Your teacher will give you a worksheet.")}'''), section="1.5 Telwoorden")

# ---------------------------------------------------------------- 12  1.6 het alfabet
ch.page(keep("alfabet-1.6", f'''
<h2 class="sec"><span class="num">1.6</span> Het alfabet</h2>
<div style="display:flex;gap:2.4mm;align-items:center;margin-bottom:3mm">{audio_icon("audio/alfabet.mp3","Het alfabet")}
<div class="note" style="font-style:normal">Listen and repeat the letters.</div></div>
<div class="alpha">{"".join(f"<span>{c}</span>" for c in "abcdefghijklmnopqrstuvwxyz")}</div>
<div class="sp"></div>
{card(None,'<div style="display:grid;grid-template-columns:auto 1fr;gap:1.2mm 4mm;font-size:9.4pt">'
 '<div class="dutch" style="color:var(--orange)">ij</div><div>lange ij</div>'
 '<div class="dutch" style="color:var(--orange)">ei</div><div>korte ei</div>'
 '<div class="dutch" style="color:var(--orange)">y</div><div>Griekse ij</div></div>')}
<div class="sp"></div>
{task(6,"speak",None,None,'<ul class="bullet"><li>Wat zijn de letters van je postcode?</li>'
 '<li>Wat is je voorletter?</li><li>Met welke letter begint je achternaam?</li></ul>')}
{task(7,"speak",None,"Line up in alphabetical order, by surname.")}
<img src="art/telwoorden.png" class="img" style="height:48mm;object-fit:cover;margin-top:5mm">'''),
 section="1.6 Het alfabet")

# ---------------------------------------------------------------- 13  opdr 6/7 + 1.7
ch.page(f'''
<h2 class="sec"><span class="num">1.7</span> Spellen</h2>
{card(None,'<div style="font-size:9.5pt;line-height:1.75">'
 'Kun je dat spellen? / Kunt u dat spellen?<br>Hoe spel je dat? / Hoe spelt u dat?</div>'
 '<div style="height:3mm"></div>'
 '<div style="font-size:9.5pt;line-height:1.75"><span class="dutch">Wall, hoe spel je dat?</span><br>'
 '<span style="margin-left:5mm;color:var(--teal)">Met dubbel l.</span></div>'
 '<div style="height:2.5mm"></div>'
 '<div style="font-size:9.5pt;line-height:1.75"><span class="dutch">Susy, is dat met een s of een z?</span><br>'
 '<span style="margin-left:5mm;color:var(--teal)">Met een s, en met een Griekse y.</span></div>')}
<img src="art/alfabet.png" class="img" style="height:48mm;object-fit:cover;margin-bottom:4mm">
{task(8,"speak",None,"Ask three other students for their first name and surname. How are they spelled?")}''',
 section="1.7 Spellen")

# ---------------------------------------------------------------- 14  1.8 begroeten
ch.page(f'''
<h2 class="sec"><span class="num">1.8</span> Begroeten en afscheid nemen</h2>
<img src="art/begroeten.png" class="img" style="height:40mm;object-fit:cover;margin-bottom:4.5mm">
<div class="two" style="gap:0 6mm">
  <div>{pairs(BEGROETEN,"begroeten","greetings")}</div>
  <div>{pairs(AFSCHEID,"afscheid nemen","saying goodbye")}</div>
</div>
<div class="sp"></div>
{task(9,"speak",None,"Walk around the room. Greet a student. The student says goodbye. "
  "Move on to another student and greet them.","",
  '<div class="example"><div class="lbl">Example</div>'
  '<div style="display:grid;grid-template-columns:1fr 1fr;gap:.8mm 4mm">'
  '<div><b>A:</b> Goedemorgen.</div><div><b>B:</b> Dag. <span class="note">(move on to the next student)</span></div>'
  '<div><b>A:</b> Hoi.</div><div><b>C:</b> Tot ziens.</div></div></div>')}''', section="1.8 Begroeten")

# ------------------------------------------------- 15  opdracht 10 + 11 (formulier)
fr=""
for f in FORM:
    if f=="Geslacht":
        fr+=('<div class="fr"><div class="fl">Geslacht</div><div>'
             '<span class="box"></span>man &nbsp;&nbsp;<span class="box"></span>vrouw</div></div>')
    elif "|" in f:
        a2,b2=f.split("|")
        fr+=(f'<div class="fr"><div class="fl">{a2}</div>'
             f'<div style="display:grid;grid-template-columns:1fr auto 1fr;gap:3mm;align-items:baseline">'
             f'<span style="border-bottom:.7pt solid var(--rule);height:4.6mm"></span>'
             f'<span class="fl" style="font-size:8.4pt">{b2}</span>'
             f'<span style="border-bottom:.7pt solid var(--rule);height:4.6mm"></span></div></div>')
    else:
        fr+=(f'<div class="fr"><div class="fl">{f}</div>'
             f'<div style="border-bottom:.7pt solid var(--rule);height:4.6mm"></div></div>')
ch.page(f'''
{task(10,"speak",None,"Work in pairs. Think up questions for an interview. "
  "Ask about: name, address, country, language, nationality.","",
  '<div class="example"><div class="lbl">Example</div>'
  '<div style="display:grid;grid-template-columns:1fr 1fr;gap:.8mm 4mm">'
  '<div><b>A:</b> Dag, ik ben Elena. Wie ben jij?</div><div><b>B:</b> Ik ben Bertrand. Waar woon je?</div>'
  '<div><b>A:</b> Ik woon in Nijmegen. En jij?</div>'
  '<div><b>B:</b> Ik woon ook in Nijmegen. Wat is je adres?</div></div></div>')}
<div class="sp"></div>
{task(11,"write","Filling in a form","Fill in your personal details.")}
<div class="form" style="padding:5mm 6mm"><div style="font-family:var(--disp);font-weight:700;color:var(--orange);
  font-size:10pt;margin-bottom:3mm;letter-spacing:.02em">Persoonlijke gegevens</div>{fr}</div>''',
 section="1.8 Begroeten")


# ---------------------------------------------------------------- 17  1.9 zinsaccent
za="".join(f'<li>{q}<div style="color:var(--teal);margin-left:0">{a}</div></li>' for q,a in ZINSACCENT)
ch.page(keep("zinsaccent-1.9", f'''
<h2 class="sec"><span class="num">1.9</span> Uitspraak: zinsaccent</h2>
{task(12,"audio","Zinsaccent","Listen to the question and the answer. Which words carry the stress? "
 "Repeat the answer.", f'<ol class="items" style="line-height:1.65">{za}</ol>',
 audio="audio/zinsaccent.mp3")}'''),
 section="1.9 Uitspraak")

# ---------------------------------------------------------------- 18  cultuur
cr="".join(f'<div>{r}</div><div style="text-align:center"><span class="box"></span></div>'
           f'<div style="text-align:center"><span class="box"></span></div>' for r in CULTUUR_ROWS)
ch.page(f'''
<div class="kicker">Cultuur</div>
<h2 class="sec" style="font-size:15pt"><span class="lock"><span class="num" style="font-size:15pt">u</span>
  of <span style="color:var(--teal)">jij</span>?</span></h2>
<img src="art/cultuur.png" class="img" style="height:44mm;object-fit:cover;margin-bottom:5mm">
{card("Who do you say <i>u</i> to? Who do you say <i>jij</i> to?",
 '<div style="display:grid;grid-template-columns:1fr 18mm 18mm;gap:1.8mm 3mm;font-size:9.4pt">'
 '<div></div><div style="text-align:center;font-family:var(--disp);font-weight:700;color:var(--orange)">u</div>'
 '<div style="text-align:center;font-family:var(--disp);font-weight:700;color:var(--teal)">jij</div>'
 +cr+'</div>')}''', section="Cultuur")

# ---------------------------------------------------------------- 19  in de praktijk
sn="".join(f'<div class="n"><b>{i+1}</b><span>{s}</span></div>' for i,s in enumerate(SURNAMES))
ch.page(f'''
<div class="kicker">In de praktijk</div>
<h2 class="sec" style="font-size:15pt">De top 10 van familienamen<br>in Nederland</h2>
<div class="note" style="margin-bottom:4mm">Do you know anyone with these surnames?</div>
<div class="two" style="gap:0 7mm">
 <div class="numbers" style="grid-template-columns:1fr">{sn}</div>
 <img src="art/praktijk.png" class="img" style="height:72mm;object-fit:cover">
</div>''', section="In de praktijk")

# ---------------------------------------------------------------- 20  eigen vocabulaire
lines = '<div class="lines">' + '<div class="ln"></div>'*22 + '</div>'
ch.page(f'''
<div class="kicker">Eigen vocabulaire</div>
<h2 class="sec" style="font-size:15pt">Eigen vocabulaire</h2>
<div style="margin-bottom:5mm">The theme of this chapter is <b>Welkom</b>.
Which words would you like to add? Write them below.</div>
<div class="two" style="gap:0 8mm">{lines}{lines}</div>''', section="Eigen vocabulaire")

# ---------------------------------------------------------------- 21  reflectie
refl=["Can you now understand the dialogue at the start of this chapter?",
 "Can you give your name and address, and ask others for theirs?",
 "Can you count to 20?","Can you spell your name and address?",
 "Can you fill in a form with personal details?","Can you greet someone and say goodbye?"]
rr="".join(f'<div class="fr" style="grid-template-columns:1fr 27mm">'
  f'<div>{r}</div><div style="text-align:right"><span class="box"></span>'
  f'<span class="note" style="font-style:normal;margin-right:3mm">yes</span>'
  f'<span class="box"></span><span class="note" style="font-style:normal">not yet</span></div></div>' for r in refl)
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
  <ul class="bullet"><li>a grammar video</li><li>a gap-fill of the dialogue</li>
   <li>extra exercises</li><li>an intensive listening text</li></ul>
 </div>
</div>''', section="Reflectie")


# ---------------------------------------------------------------- PDF-bladwijzers
ch.toc = [
 [1,"Hoofdstuk 1 — Welkom",1],
 [2,"1.1  Dialoog — De cursus begint",2],
 [3,"Wie is wie in de dialoog?",3],
 [2,"1.2  Woordenlijst",4],
 [2,"1.3  Zich voorstellen / informatie vragen / landen",6],
 [3,"Opdracht 1",7],
 [2,"1.4  Personaal pronomen + werkwoord",8],
 [3,"Opdracht 2",9],
 [3,"Opdracht 3",10],
 [2,"1.5  Telwoorden",11],
 [3,"Opdracht 4–5",12],
 [2,"1.6  Het alfabet",12],
 [3,"Opdracht 6–7",12],
 [2,"1.7  Spellen",13],
 [3,"Opdracht 8",13],
 [2,"1.8  Begroeten en afscheid nemen",14],
 [3,"Opdracht 9",14],
 [3,"Opdracht 10",15],
 [3,"Opdracht 11: Een formulier invullen",15],
 [2,"1.9  Uitspraak: zinsaccent",16],
 [3,"Opdracht 12",16],
 [2,"Cultuur — u of jij?",17],
 [2,"In de praktijk — top 10 familienamen",18],
 [2,"Eigen vocabulaire",19],
 [2,"Reflectie — wat kun je nu?",20],
]

if __name__ == "__main__":
    n = ch.write(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html"))
    print(f"hoofdstuk 1 — {n} pagina's")

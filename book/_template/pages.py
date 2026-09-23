# -*- coding: utf-8 -*-
"""Chapter {{NUMBER}} — {{TITLE}}.  Page composition.

Build with:  python3 book/build.py {{FOLDER}}
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "shared", "lib")]

from layout import Chapter, icon, task, card, qa, vocab_rows, pairs, numbers, lines
from content import *

ch = Chapter({{NUMBER}}, "{{TITLE}}")

# ---------------------------------------------------------------- 1  COVER
colA = "".join(f'<li>{o}</li>' for o in OBJECTIVES[:len(OBJECTIVES)//2 + len(OBJECTIVES)%2])
colB = "".join(f'<li>{o}</li>' for o in OBJECTIVES[len(OBJECTIVES)//2 + len(OBJECTIVES)%2:])
ch.page(f'''
<img src="art/opener.png" style="position:absolute;inset:0;width:100%;height:100%;
     object-fit:cover;object-position:50% 22%">
<div style="position:absolute;left:0;right:0;bottom:0;height:130mm;
     background:linear-gradient(180deg,rgba(253,250,244,0) 0%,rgba(253,250,244,.55) 26%,rgba(253,250,244,1) 46%)"></div>
<div style="position:absolute;left:0;right:0;bottom:0;padding:0 15mm 15mm">
  <div class="kicker" style="color:var(--teal);margin-bottom:2.5mm">Nederlands in gang &nbsp;·&nbsp; Methode Nederlands</div>
  <div style="display:flex;align-items:flex-end;gap:6mm;margin-bottom:7mm">
    <div style="font-family:var(--disp);font-size:78pt;font-weight:800;color:var(--orange);
                line-height:.72;letter-spacing:-.06em">{ch.number}</div>
    <div style="font-family:var(--disp);font-size:40pt;font-weight:800;letter-spacing:-.035em;
                line-height:.86;color:var(--ink);padding-bottom:1mm">{ch.title}</div>
  </div>
  <div style="height:.7pt;background:var(--rule);margin-bottom:5mm"></div>
  <div class="kicker" style="margin-bottom:3mm">In dit hoofdstuk leer je</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 8mm">
    <ul class="bullet" style="font-size:9.4pt">{colA}</ul>
    <ul class="bullet" style="font-size:9.4pt">{colB}</ul>
  </div>
</div>''', variant="bleed", head=False, foot=False, nogloss=True)

# ---------------------------------------------------------------- 2  DIALOOG
# dl = "".join(f'<dt{" class=you" if s!="Docent" else ""}>{s}:</dt><dd>{t}</dd>' for s,t in DIALOOG)
# ch.page(f'''<h2 class="sec"><span class="num">{ch.number}.1</span> Dialoog</h2>
# <img src="art/dialoog.png" class="img" style="height:46mm;object-fit:cover;margin-bottom:4.5mm">
# <dl class="dialogue">{dl}</dl>''', section=f"{ch.number}.1 Dialoog")

ch.toc = [[1, f"Hoofdstuk {ch.number} — {ch.title}", 1]]

if __name__ == "__main__":
    n = ch.write(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html"))
    print(f"hoofdstuk {ch.number} — {n} pagina's")

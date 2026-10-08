# -*- coding: utf-8 -*-
"""Shared layout building blocks for every chapter.

A chapter composes its pages with Chapter.page(...) plus the helpers below.
All visual styling lives in shared/style.css — this file only builds structure.
"""
import json


# Page numbers spelled out in Dutch, for the footer (book content, stays Dutch)
NUMBER_WORDS = ["", "een","twee","drie","vier","vijf","zes","zeven","acht","negen","tien",
 "elf","twaalf","dertien","veertien","vijftien","zestien","zeventien","achttien","negentien","twintig",
 "eenentwintig","tweeëntwintig","drieëntwintig","vierentwintig","vijfentwintig","zesentwintig",
 "zevenentwintig","achtentwintig","negenentwintig","dertig","eenendertig","tweeëndertig",
 "drieëndertig","vierendertig","vijfendertig","zesendertig","zevenendertig","achtendertig",
 "negenendertig","veertig"]

ICONS = {
 "speak":'<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4L3 21l1.1-4.3A8.4 8.4 0 1 1 21 11.5Z"/>',
 "write":'<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
 "read" :'<path d="M4 4h11l5 5v11H4Z"/><path d="M8 12h8M8 16h6"/>',
 "audio":'<path d="M11 5 6 9H3v6h3l5 4Z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/>',
 "web"  :'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18"/>',
}

def icon(kind):
    """Skill icon: speak / write / read / audio / web."""
    return f'<span class="icon i-{kind}"><svg viewBox="0 0 24 24">{ICONS[kind]}</svg></span>'

def audio_icon(src, label=""):
    """The audio icon, but clickable: plays `src` in the browser.

    Renders identically to icon("audio") on paper, so the printed PDF is unchanged.
    """
    # An <a href> so Chrome's print-to-pdf emits a real PDF link annotation —
    # the icon is then clickable in the PDF too. In the browser the script calls
    # preventDefault() and plays it inline instead of navigating.
    return (f'<a class="icon i-audio play" href="{src}" data-src="{src}" '
            f'aria-label="{label or "speel audio"}">'
            f'<svg viewBox="0 0 24 24" class="ic-play">{ICONS["audio"]}</svg>'
            f'<svg viewBox="0 0 24 24" class="ic-stop"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>'
            f'</a>')

def task(num, skill, title, instruction, body="", extra="", audio=None):
    """An exercise block ("Opdracht") with icon, number and instruction.

    Pass audio="audio/x.mp3" to make the icon a play button.
    """
    mark = audio_icon(audio, f"Opdracht {num}") if audio else icon(skill)
    heading = f'Opdracht <span>{num}</span>' + (
        f' &nbsp;<span style="color:var(--ink-faint);font-weight:600">{title}</span>' if title else '')
    # data-opdracht lets answers.js find this exercise at runtime and append the
    # book's answer to it. Nothing is written into the markup here, so the PDF
    # never contains an answer.
    return (f'<div class="task" data-opdracht="{num}">'
            f'<div class="oh">{mark}<div class="ttl">{heading}</div></div>'
            f'{f"<div class=ins>{instruction}</div>" if instruction else ""}{body}{extra}</div>')

def card(title, inner, variant=""):
    """Tinted reference card. variant="teal" gives the cooler version."""
    return f'<div class="card {variant}">{f"<div class=ct>{title}</div>" if title else ""}{inner}</div>'

def qa(rows):
    """Two columns of question / answer."""
    return '<div class="qa">' + "".join(
        f'<div class="q">{q}</div><div class="a">{a}</div>' for q, a in rows) + '</div>'

def vocab_rows(items):
    """Vocabulary list: reads top-to-bottom per column, zebra striping per row."""
    import math
    rows = math.ceil(len(items)/2)
    cells = []
    for i, (dutch, english) in enumerate(items):
        alt = " alt" if (i % rows) % 2 else ""
        cells.append(f'<div class="row{alt}"><div class="d">{dutch}</div>'
                     f'<div class="e">{english}</div></div>')
    return f'<div class="vocab" style="grid-template-rows:repeat({rows},auto)">' + "".join(cells) + '</div>'

def pairs(rows, label, subtitle):
    """Card with two columns: Dutch term + translation."""
    body = "".join(f'<div class="dutch">{a}</div><div style="color:var(--teal)">{b}</div>'
                   for a, b in rows)
    return card(f'{label} &nbsp;<em>{subtitle}</em>',
        f'<div style="display:grid;grid-template-columns:auto 1fr;gap:1.1mm 6mm;font-size:9.3pt">{body}</div>')

def numbers(items):
    """One column of numeral chips: digit + word."""
    return ('<div class="numbers">'
            + "".join(f'<div class="n"><b>{n}</b><span>{w}</span></div>' for n, w in items)
            + '</div>')

def number_columns(*groups):
    """Numeral columns read top-to-bottom, as the original does: units, teens,
    tens. Reading them across would break the -tien / -tig patterns that make the
    grouping worth printing at all."""
    return '<div class="numcols">' + "".join(numbers(g) for g in groups) + '</div>' 

def clock(hour, minute, label=""):
    """An analogue clock face drawn as SVG.

    The original prints clock faces beside the time phrases. Drawing them means
    the hands are exactly right for the time being taught — a generated image
    cannot be trusted to put them in the correct place.
    """
    import math
    ha = math.radians((hour % 12 + minute/60) * 30 - 90)
    ma = math.radians(minute * 6 - 90)
    ticks = "".join(
        f'<line x1="{50+40*math.cos(math.radians(a-90)):.1f}" y1="{50+40*math.sin(math.radians(a-90)):.1f}"'
        f' x2="{50+45*math.cos(math.radians(a-90)):.1f}" y2="{50+45*math.sin(math.radians(a-90)):.1f}"'
        f' stroke="var(--ink-faint)" stroke-width="{2.4 if a % 90 == 0 else 1.2}"/>'
        for a in range(0, 360, 30))
    cap = (f'<div class="clocklabel">{label}</div>' if label else "")
    return (f'<div class="clock"><svg viewBox="0 0 100 100">'
            f'<circle cx="50" cy="50" r="47" fill="#fff" stroke="var(--rule)" stroke-width="2"/>'
            f'{ticks}'
            f'<line x1="50" y1="50" x2="{50+26*math.cos(ha):.1f}" y2="{50+26*math.sin(ha):.1f}"'
            f' stroke="var(--ink)" stroke-width="4.5" stroke-linecap="round"/>'
            f'<line x1="50" y1="50" x2="{50+37*math.cos(ma):.1f}" y2="{50+37*math.sin(ma):.1f}"'
            f' stroke="var(--orange)" stroke-width="3" stroke-linecap="round"/>'
            f'<circle cx="50" cy="50" r="3" fill="var(--ink)"/>'
            f'</svg>{cap}</div>')

def keep(name, html):
    """Mark html as one indivisible block.

    build.py fails if a block with this name lands on more than one page, or if
    it runs past the trim. Use it for anything that has to be read as a whole:
    a dialogue, a conjugation table, an exercise together with its items.

    The original book fits its dialogue on a single page; splitting one across a
    page turn loses the thread and strands the audio, so the rule is enforced
    rather than left to judgement.
    """
    return f'<div class="keep" data-keep="{name}">{html}</div>'

def lines(count):
    """`count` blank writing lines."""
    return '<div class="lines">' + '<div class="ln"></div>'*count + '</div>'


class Chapter:
    """Collects pages and writes them out as a single index.html.

    number / title  -> running head and cover
    toc             -> [[level, label, page], ...] for the PDF bookmarks
    """
    def __init__(self, number, title, css="../shared/style.css",
                 deck_js="../shared/flashcards.js",
                 answers_js="../shared/answers.js"):
        self.number, self.title, self.css = number, title, css
        self.deck_js = deck_js
        self.answers_js = answers_js
        self.pages, self.toc = [], []
        self.deck = []          # set by build.py; cards for the practice overlay
        self.answers = {}       # set by build.py; Opdracht number -> answer html

    def page(self, body, variant="", head=True, foot=True, section="", nogloss=False):
        """nogloss=True excludes the page from hover translations.

        Used for the cover: its objectives list is a contents page, so letting it
        claim a word's first occurrence would rob the dialogue — where the learner
        actually meets the word in a sentence — of the tooltip.
        """
        n = len(self.pages) + 1
        header = (f'<div class="rh"><span><span class="chap">Hoofdstuk {self.number}</span>'
                  f' &nbsp;·&nbsp; {self.title}</span><span>{section}</span></div>') if head else ""
        footer = (f'<div class="pf"><span class="w">{NUMBER_WORDS[n]}</span>'
                  f'<span class="n">{n}</span></div>') if foot else ""
        mark = " data-nogloss" if nogloss else ""
        self.pages.append(
            f'<section class="page {variant}"{mark}>{header}{body}{footer}</section>')
        return n

    PLAYER = """
<script>
(function () {
  // ---- audio: click an icon to play, click again to stop ----
  var audio = new Audio(), current = null;
  function reset() { if (current) current.classList.remove("playing"); current = null; }
  audio.addEventListener("ended", reset);
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("a.i-audio"); if (!btn) return;
    e.preventDefault();
    if (current === btn) { audio.pause(); reset(); return; }
    reset();
    audio.src = btn.dataset.src; audio.currentTime = 0;
    audio.play().then(function () { current = btn; btn.classList.add("playing"); })
                .catch(function () { btn.classList.add("failed"); });
  });

  // ---- first-occurrence translations ----
  // The tip lives on <body>, not inside .page: a page clips its overflow, which
  // would cut off a wide tip ("(for friendliness, usually not translated)") on a
  // word near the margin. Positioned here so it can also be clamped on screen.
  var tip = document.createElement("div");
  tip.className = "glosstip"; tip.hidden = true;
  document.addEventListener("DOMContentLoaded", function () { document.body.appendChild(tip); });
  function show(el) {
    tip.textContent = el.dataset.en;
    tip.hidden = false;
    var r = el.getBoundingClientRect(), t = tip.getBoundingClientRect();
    // Left-aligned to the word, not centred on it: a centred tip spreads both
    // ways across the line above and buries the start of the previous sentence.
    // Hanging right from the word keeps that sentence's opening readable.
    var x = r.left;
    x = Math.max(6, Math.min(x, document.documentElement.clientWidth - t.width - 6));
    var y = r.top - t.height - 4;
    if (y < 4) y = r.bottom + 4;                 // no room above: drop below
    tip.style.left = (x + window.scrollX) + "px";
    tip.style.top  = (y + window.scrollY) + "px";
  }
  // Mouse: hover. Touch: tap to open, tap again or elsewhere to close — a phone
  // has no hover, so without this the translations are simply unreachable there.
  var touched = false;

  document.addEventListener("mouseover", function (e) {
    if (touched) return;
    var g = e.target.closest(".gloss"); if (g) show(g);
  });
  document.addEventListener("mouseout", function (e) {
    if (touched) return;
    if (e.target.closest(".gloss")) tip.hidden = true;
  });

  document.addEventListener("touchstart", function () { touched = true; }, {passive: true});
  document.addEventListener("click", function (e) {
    if (!touched) return;
    var g = e.target.closest(".gloss");
    if (!g) { tip.hidden = true; return; }
    // tapping the open word closes it again
    if (!tip.hidden && tip.dataset.for === g.dataset.en) { tip.hidden = true; return; }
    tip.dataset.for = g.dataset.en;
    show(g);
  });
})();
</script>"""

    def deck_html(self):
        """The practice cards, as data plus a linked script.

        Linked rather than inlined so a change to the component reaches all
        eighteen chapters on reload — only new *cards* need a rebuild. The script
        builds its own DOM at runtime, so nothing of it exists in the print
        document, and build.py's layout probe (which measures inside .page)
        cannot see it either.
        """
        if not self.deck:
            return ""
        payload = json.dumps(self.deck, ensure_ascii=False, separators=(",", ":"))
        return ('<script type="application/json" id="nl-deck-data">'
                + payload.replace("</", "<\\/") + "</script>"
                + f'<script src="{self.deck_js}" defer></script>')

    def answers_html(self):
        """This chapter's answers as data, plus the script that reveals them.

        Built at runtime like the practice deck, so the PDF stays an unanswered
        workbook — printing a key into it would spoil every exercise.
        """
        if not self.answers:
            return ""
        payload = json.dumps(self.answers, ensure_ascii=False, separators=(",", ":"))
        return ('<script type="application/json" id="nl-answers-data">'
                + payload.replace("</", "<\\/") + "</script>"
                + f'<script src="{self.answers_js}" defer></script>')

    def body(self):
        """Pages, with the practice panel sitting straight after the word list.

        The panel goes where a learner would want it — below the Woordenlijst,
        in the flow of the chapter rather than floating over it. It is NOT a
        .page: it is screen-only furniture, so it never reaches the PDF and
        build.py's page checks never see it. Placement is automatic: the last
        page carrying a .vocab table is the end of the word list.
        """
        if not self.deck:
            return "".join(self.pages)
        last = -1
        for i, page in enumerate(self.pages):
            if 'class="vocab' in page:
                last = i
        panel = '<div id="nl-deck"></div>'
        if last < 0:                       # no word list: put it at the end
            return "".join(self.pages) + panel
        return ("".join(self.pages[:last + 1]) + panel
                + "".join(self.pages[last + 1:]))

    def html(self):
        # Without the viewport meta a phone lays the page out at ~980px and then
        # zooms the whole thing out — the sheet is legible only by pinching. It
        # costs nothing in print, where @page decides the size.
        return (f'<meta charset="utf-8">'
                f'<meta name="viewport" content="width=device-width, initial-scale=1">'
                f'<title>Nederlands in gang — Hoofdstuk {self.number}: {self.title}</title>'
                f'<link rel="stylesheet" href="{self.css}">'
                + self.body() + self.PLAYER + self.deck_html() + self.answers_html())

    def write(self, path):
        open(path, "w", encoding="utf-8").write(self.html())
        return len(self.pages)


def family_tree():
    """A family tree drawn from chapter 2's own Familierelaties words.

    Drawn as SVG rather than generated art for the same reason as clock(): a tree
    is nothing but labels, and image models render letterforms unreliably.

    Every one of the chapter's 21 family words appears, and each is placed rather
    than defined — the spouses hang off their partner, *het kleinkind* is a dotted
    link back to the grandparents, and *het gezin* / *de familie* are nested
    outlines. Showing a relationship beats writing a definition for it, which
    would be inventing Dutch the book never printed.

    NOTE: the book prints no family tree. This is a study aid, like the sentence
    translations, not transcribed content.
    """
    ink, teal, orange, rule, soft = "#1E2A2E", "#14616B", "#E8632A", "#D9CFBC", "#B9AC95"

    def node(cx, cy, nl, en, lead=False, small=False):
        fs, sub, h = (4.3, 3.4, 13) if small else (4.9, 3.8, 14.5)
        w = max(27, len(nl) * (2.0 if small else 2.25) + 8)
        fill = "#FBEDE6" if lead else "#FFFFFF"
        edge = orange if lead else (soft if small else rule)
        return (f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" '
                f'height="{h}" rx="3.2" fill="{fill}" stroke="{edge}" '
                f'stroke-width="{0.9 if lead else 0.6}"/>'
                f'<text x="{cx:.1f}" y="{cy - 0.8:.1f}" text-anchor="middle" '
                f'font-size="{fs}" font-weight="700" fill="{ink}">{nl}</text>'
                f'<text x="{cx:.1f}" y="{cy + 4.4:.1f}" text-anchor="middle" '
                f'font-size="{sub}" fill="{teal}">{en}</text>')

    def couple(x1, x2, y):
        return "".join(
            f'<line x1="{x1:.1f}" y1="{y + d:.1f}" x2="{x2:.1f}" y2="{y + d:.1f}" '
            f'stroke="{rule}" stroke-width="0.7"/>' for d in (-1, 1))

    def descend(px, py, kids, kid_y):
        mid = (py + kid_y) / 2
        out = [f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px:.1f}" y2="{mid:.1f}" '
               f'stroke="{rule}" stroke-width="0.7"/>',
               f'<line x1="{min(kids):.1f}" y1="{mid:.1f}" x2="{max(kids):.1f}" '
               f'y2="{mid:.1f}" stroke="{rule}" stroke-width="0.7"/>']
        for k in kids:
            out.append(f'<line x1="{k:.1f}" y1="{mid:.1f}" x2="{k:.1f}" '
                       f'y2="{kid_y:.1f}" stroke="{rule}" stroke-width="0.7"/>')
        return "".join(out)

    def band(x1, y1, x2, y2, label, dash="3 2.2", colour=None):
        c = colour or orange
        return (f'<rect x="{x1:.1f}" y="{y1:.1f}" width="{x2 - x1:.1f}" '
                f'height="{y2 - y1:.1f}" rx="4" fill="none" stroke="{c}" '
                f'stroke-width="0.6" stroke-dasharray="{dash}"/>'
                f'<text x="{x1 + 3:.1f}" y="{y1 - 1.8:.1f}" font-size="4" '
                f'font-weight="700" fill="{c}">{label}</text>')

    OPA, OMA       = 112, 152
    OOM, TANTE     = 28, 68
    NEEF, NICHT    = 28, 68
    BROER, IK, ZUS = 104, 152, 200
    ZOON, DOCHTER  = 130, 174
    yA, yB, yC, yD = 18, 56, 96, 136

    s = []
    # de familie: everyone on the chart
    s.append(band(8, 10, 240, 152, "de familie", dash="1.6 2.4", colour=soft))
    # het gezin: the household the learner grew up in
    # het gezin is the household: parents and their children, no in-laws,
    # and clear of the cousins on the left
    s.append(band(88, 38, 212, 108, "het gezin"))

    # generation 1 -> their two children: de oom and de vader
    s.append(couple(OPA + 14, OMA - 14, yA))
    s.append(descend((OPA + OMA) / 2, yA + 8, [OOM, 112], yB - 8))
    s.append(node(OPA, yA, "de opa", "grandfather"))
    s.append(node(OMA, yA, "de oma", "grandmother"))

    # generation 2
    s.append(couple(OOM + 14, TANTE - 14, yB))
    s.append(couple(112 + 15, 152 - 15, yB))
    s.append(descend((OOM + TANTE) / 2, yB + 8, [NEEF, NICHT], yC - 8))
    s.append(descend(132, yB + 8, [BROER, IK, ZUS], yC - 8))
    s.append(node(OOM, yB, "de oom", "uncle"))
    s.append(node(TANTE, yB, "de tante", "aunt"))
    s.append(node(112, yB, "de vader", "father"))
    s.append(node(152, yB, "de moeder", "mother"))
    s.append(f'<text x="132" y="{yB - 11}" text-anchor="middle" font-size="4" '
             f'font-weight="700" fill="{orange}">de ouders</text>')

    # generation 3, each with the partner the chapter names
    s.append(node(NEEF, yC, "de neef", "nephew / cousin"))
    s.append(node(NICHT, yC, "de nicht", "niece / cousin"))
    for cx, nl, en, partner, pen in (
            (BROER, "de broer", "brother", "de schoonzus", "sister in law"),
            (IK, "ik", "me", "de man / de vrouw", "husband / wife"),
            (ZUS, "de zus", "sister", "de zwager", "brother in law")):
        s.append(f'<line x1="{cx:.1f}" y1="{yC + 7.5:.1f}" x2="{cx:.1f}" '
                 f'y2="{yC + 13:.1f}" stroke="{soft}" stroke-width="0.6"/>')
        s.append(node(cx, yC + 19, partner, pen, small=True))
        s.append(node(cx, yC, nl, en, lead=(nl == "ik")))

    # generation 4 — and what they are to the grandparents
    s.append(descend(IK, yC + 26, [ZOON, DOCHTER], yD - 8))
    s.append(node(ZOON, yD, "de zoon", "son"))
    s.append(node(DOCHTER, yD, "de dochter", "daughter"))
    s.append(f'<text x="152" y="{yD + 12.5}" text-anchor="middle" font-size="4" '
             f'font-weight="700" fill="{orange}">het kind</text>')
    # het kleinkind: what de zoon and de dochter are to MY parents. Running this
    # line up to de opa / de oma would be a generation out — to them these two are
    # achterkleinkinderen, a word this chapter does not teach.
    s.append(f'<path d="M {DOCHTER + 16} {yD} H 226 V {yB} H 172" fill="none" '
             f'stroke="{teal}" stroke-width="0.6" stroke-dasharray="2 2"/>')
    s.append(f'<text x="231" y="{(yB + yD) / 2:.1f}" text-anchor="middle" '
             f'font-size="4" font-weight="700" fill="{teal}" '
             f'transform="rotate(90 231 {(yB + yD) / 2:.1f})">het kleinkind</text>')

    return ('<svg class="tree" viewBox="0 0 256 162" role="img" '
            'aria-label="Family tree built from this chapter\'s words">'
            + "".join(s) + "</svg>")

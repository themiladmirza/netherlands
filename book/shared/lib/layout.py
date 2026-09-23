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
    return (f'<div class="task"><div class="oh">{mark}<div class="ttl">{heading}</div></div>'
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
                 deck_js="../shared/flashcards.js"):
        self.number, self.title, self.css = number, title, css
        self.deck_js = deck_js
        self.pages, self.toc = [], []
        self.deck = []          # set by build.py; cards for the practice overlay

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
                + self.body() + self.PLAYER + self.deck_html())

    def write(self, path):
        open(path, "w", encoding="utf-8").write(self.html())
        return len(self.pages)

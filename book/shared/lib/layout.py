# -*- coding: utf-8 -*-
"""Shared layout building blocks for every chapter.

A chapter composes its pages with Chapter.page(...) plus the helpers below.
All visual styling lives in shared/style.css — this file only builds structure.
"""
import json, os, re


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

def lines(count, style=""):
    """`count` blank writing lines."""
    st = f' style="{style}"' if style else ""
    return f'<div class="lines"{st}>' + '<div class="ln"></div>'*count + '</div>'


# ---------------------------------------------------------------- recurring blocks
# Every block below appeared hand-written, near-identically, in at least two
# chapters. A chapter's pages.py should read as a list of these, with raw HTML
# left only for what is genuinely one of a kind (a clock, a word cloud, a form).

def sec(num, title):
    """A numbered section heading: `3.1 Dialoog`.

    The title sits in one span: h2.sec is a flex row, so any element loose inside
    it (a <b>, or a hover translation glossary.py wraps round "de week") would
    become its own flex item and open a gap in the printed heading."""
    return f'<h2 class="sec"><span class="num">{num}</span> <span class="t">{title}</span></h2>'

def kicker_head(kicker, title):
    """The heading of an unnumbered closing section: Cultuur, In de praktijk, …"""
    return (f'<div class="kicker">{kicker}</div>\n'
            f'<h2 class="sec" style="font-size:15pt"><span class="t">{title}</span></h2>')

def img(name, height=None, margin=""):
    """A chapter illustration from art/, cropped to `height` mm (None: uncropped)."""
    if height is None:
        return f'<img src="art/{name}.png" class="img">'
    m = f";margin{margin}" if margin else ""
    return f'<img src="art/{name}.png" class="img" style="height:{height}mm;object-fit:cover{m}">'

def web_note(html, variant="", title=None, align="flex-start"):
    """A card pointing at the publisher's site, with the globe icon."""
    return card(title, f'<div style="display:flex;gap:3mm;align-items:{align}">'
                + icon("web") + f'<div>{html}</div></div>', variant)

WORDLIST_NOTE = ('<div class="note" style="margin-bottom:3.5mm">The words appear in the order '
                 'they occur in the dialogue.\nThe infinitive or singular form is given in brackets.</div>')

def phrases(rows, size=9.6, lh=1.85):
    """Lines of Dutch, one per row, as a reference card prints them.

    `rows` may be a single string; lh=None leaves the line height alone."""
    rows = [rows] if isinstance(rows, str) else rows
    l = f";line-height:{lh}" if lh else ""
    return f'<div style="font-size:{size}pt{l}">' + "<br>".join(rows) + '</div>'

def term_grid(rows, size=9.4, gap="1.2mm 5mm", second="", first="", per_row=1, style=""):
    """Term | gloss pairs in a grid. second="teal" colours the gloss,
    first="orange" the term; per_row=2 sets two pairs side by side."""
    c1 = f' style="color:var(--{first})"' if first else ""
    c2 = f' style="color:var(--{second})"' if second else ""
    cols = " ".join(["auto 1fr"] * per_row)
    cells = "".join(f'<div class="dutch"{c1}>{a}</div><div{c2}>{b}</div>' for a, b in rows)
    return (f'<div style="display:grid;grid-template-columns:{cols};gap:{gap};'
            f'font-size:{size}pt{";" + style if style else ""}">{cells}</div>')

def lettered(rows, gap="1.6mm 2mm", size=9.4):
    """Sub-tasks or options labelled A / B / C (or a / b / c) in the margin."""
    cells = "".join(f'<div class="dutch" style="color:var(--orange)">{k}</div><div>{v}</div>'
                    for k, v in rows)
    return (f'<div style="display:grid;grid-template-columns:6mm 1fr;gap:{gap};'
            f'font-size:{size}pt">{cells}</div>')

def audio_note(src, label, text, mb=3.5):
    """The audio icon with a direction beside it: "Listen and repeat." """
    return (f'<div style="display:flex;gap:2.4mm;align-items:center;margin-bottom:{mb}mm">'
            f'{audio_icon(src, label)}\n<div class="note" style="font-style:normal">{text}</div></div>')

def example(inner, style=""):
    """The "Example" box inside an exercise."""
    st = f' style="{style}"' if style else ""
    return f'<div class="example"{st}><div class="lbl">Example</div>{inner}</div>'

def side_by_side(a, b):
    """Two cells next to each other: a sentence and its variation."""
    return (f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:2mm">'
            f'<div>{a}</div><div>{b}</div></div>')

def bullets(rows):
    return '<ul class="bullet">' + "".join(f'<li>{r}</li>' for r in rows) + '</ul>'

def items(rows, lh=None, cls="items"):
    """A numbered exercise list."""
    st = f' style="line-height:{lh}"' if lh else ""
    return f'<ol class="{cls}"{st}>' + "".join(f'<li>{r}</li>' for r in rows) + '</ol>'

def blanks(text, width=None):
    """Turn every ___ in an exercise item into a write-in blank."""
    st = f' style="min-width:{width}mm"' if width else ""
    return text.replace("___", f'<span class="blank"{st}></span>')

def word_columns(cols, n=3, max_width=None, extra="", gap="0 6mm", size=10, lh=2.3):
    """Words in `n` columns, each read top to bottom — never across."""
    mw = f"max-width:{max_width}mm" if max_width else ""
    l = f"line-height:{lh};" if lh else ""
    return (f'<div style="display:grid;grid-template-columns:repeat({n},1fr);gap:{gap};font-size:{size}pt;'
            f'{l}{extra}{mw}">'
            + "".join('<div>' + "<br>".join(c) + '</div>' for c in cols) + '</div>')

def word_rows(rows):
    """Rows of words split by small squares, for listen-and-repeat drills."""
    return ('<div style="font-size:10pt;line-height:2.4;margin-top:2mm">'
            + "".join('<div class="wordrow">' + " &nbsp;<span>&#9642;</span>&nbsp; ".join(r) + '</div>'
                      for r in rows) + '</div>')

def tick_table(count, heads=("+", "–"), style="max-width:62mm;margin:3mm 0 0", head=True):
    """Numbered rows of empty boxes to tick while listening. head=False drops
    the header row, for a table whose columns the example above explains."""
    th = '<th style="width:12mm"></th>' + "".join(f'<th>{h}</th>' for h in heads)
    body = "".join(f'<tr><td>{i}</td>' + '<td></td>' * len(heads) + '</tr>'
                   for i in range(1, count + 1))
    thead = f'<thead><tr>{th}</tr></thead>' if head else ""
    return f'<table class="grid tick" style="{style}">{thead}<tbody>{body}</tbody></table>'

def two_columns(cols, size=9.4, gap="1.2mm 6mm"):
    """Lines of Dutch in two side-by-side columns."""
    return (f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:{gap};font-size:{size}pt">'
            + "".join('<div>' + "<br>".join(c) + '</div>' for c in cols) + '</div>')

def sentence_grid(rows, dutch_cols=(0, 2), size=9.6):
    """Word-order table: subject | verb (orange) | … , one sentence per row."""
    cells = ""
    for row in rows:
        for i, c in enumerate(row):
            if i == 1:
                cells += f'<div style="color:var(--orange);font-weight:600">{c}</div>'
            elif i in dutch_cols:
                cells += f'<div class="dutch">{c}</div>'
            else:
                cells += f'<div>{c}</div>'
    return (f'<div style="display:grid;grid-template-columns:auto auto auto 1fr;'
            f'gap:1.6mm 6mm;font-size:{size}pt">{cells}</div>')

def data_table(heads, rows, first_width=30):
    """A grammar table; the first column is the row label."""
    th = f'<th style="width:{first_width}%">{heads[0]}</th>' + "".join(f'<th>{h}</th>' for h in heads[1:])
    tr = "".join('<tr>' + "".join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="grid"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'

def sentences(text):
    """Wrap each sentence of a dialogue turn in <span class="say">.

    build.py gives every span its start and end in the recording (timings.py),
    and the player lets you click one to hear just that sentence. The spans are
    unstyled in print, so the PDF does not change.
    """
    out = []
    for part in re.split(r"(<br>)", text):
        if part == "<br>":
            out.append(part); continue
        out.append(" ".join(f'<span class="say">{s}</span>'
                            for s in re.split(r"(?<=[.?!])\s+", part.strip()) if s))
    return "".join(out)

def dialogue(rows, you=(), cls="dialogue", audio=None):
    """Speaker turns. Speakers in `you` are set in the second colour.

    Pass audio="audio/dialoog.mp3" (the recording of these turns) to make every
    sentence replayable on screen. Several dialogue() calls may share one file;
    they are aligned to it in page order.
    """
    say = sentences if audio else (lambda t: t)
    return (f'<dl class="{cls}"' + (f' data-audio="{audio}"' if audio else '') + '>'
            + "".join(f'<dt{" class=you" if s in you else ""}>{s}:</dt><dd>{say(t)}</dd>' for s, t in rows)
            + '</dl>')

def scene_break(text):
    """A stage direction between two scenes of a dialogue: (een poosje later)."""
    return ('<div style="color:var(--ink-faint);font-style:italic;font-size:9pt;'
            f'margin:2.6mm 0 2.6mm 25mm">{text}</div>')

def audio_head(src, label, text, align="center"):
    """The audio icon beside a dialogue's title line."""
    return (f'<div style="display:flex;align-items:{align};gap:2.4mm;margin-bottom:3mm">\n'
            f'  {audio_icon(src, label)}<div style="font-family:var(--disp);font-weight:700;'
            f'font-size:10pt">{text}</div>\n</div>')


class Chapter:
    """Collects pages and writes them out as a single index.html.

    number / title  -> running head and cover
    toc             -> [[level, label, page], ...] for the PDF bookmarks
    """
    def __init__(self, number, title, css="../shared/style.css",
                 deck_js="../shared/flashcards.js",
                 answers_js="../shared/answers.js",
                 articles_js="../shared/articles.js",
                 talk_js="../shared/talk.js"):
        self.number, self.title, self.css = number, title, css
        self.deck_js = deck_js
        self.answers_js = answers_js
        self.articles_js = articles_js
        self.talk_js = talk_js
        self.pages, self.toc = [], []
        self.deck = []          # set by build.py; cards for the practice overlay
        self.answers = {}       # set by build.py; Opdracht number -> answer html
        self.articles = []      # set by build.py; de/het nouns [{article, noun, en}]
        self.folder = None      # set by build.py; finds this chapter's extra.css / extra.js
        self.talks = []         # set by talk(); recordings with a speak-the-dialogue drill

    def page(self, body, variant="", head=True, foot=True, section="", nogloss=False, toc=()):
        """nogloss=True excludes the page from hover translations.

        Used for the cover: its objectives list is a contents page, so letting it
        claim a word's first occurrence would rob the dialogue — where the learner
        actually meets the word in a sentence — of the tooltip.

        toc=[(level, label), …] adds PDF bookmarks pointing at this page. The
        page number is filled in here, so it can never go stale.
        """
        n = len(self.pages) + 1
        self.toc += [[level, label, n] for level, label in toc]
        header = (f'<div class="rh"><span><span class="chap">Hoofdstuk {self.number}</span>'
                  f' &nbsp;·&nbsp; {self.title}</span><span>{section}</span></div>') if head else ""
        footer = (f'<div class="pf"><span class="w">{NUMBER_WORDS[n]}</span>'
                  f'<span class="n">{n}</span></div>') if foot else ""
        mark = " data-nogloss" if nogloss else ""
        self.pages.append(
            f'<section class="page {variant}"{mark}>{header}{body}{footer}</section>')
        return n

    # ------------------------------------------------ pages every chapter has
    def cover(self, objectives, crop="50% 22%", title_pt=40, title_lh=".88"):
        """Page 1: full-bleed opener with number, title and the objectives.

        `crop` positions the opener image; `title_pt` shrinks a long title so it
        stays on one line beside the number.
        """
        half = len(objectives)//2 + len(objectives) % 2
        col = lambda rows: "".join(f'<li>{o}</li>' for o in rows)
        return self.page(f'''
<img src="art/opener.png" style="position:absolute;inset:0;width:100%;height:100%;
     object-fit:cover;object-position:{crop}">
<div style="position:absolute;left:0;right:0;bottom:0;height:130mm;
     background:linear-gradient(180deg,rgba(253,250,244,0) 0%,rgba(253,250,244,.55) 26%,rgba(253,250,244,1) 46%)"></div>
<div style="position:absolute;left:0;right:0;bottom:0;padding:0 15mm 15mm">
  <div class="kicker" style="color:var(--teal);margin-bottom:2.5mm">Nederlands in gang &nbsp;·&nbsp; Methode Nederlands</div>
  <div style="display:flex;align-items:flex-end;gap:6mm;margin-bottom:7mm">
    <div style="font-family:var(--disp);font-size:78pt;font-weight:800;color:var(--orange);
                line-height:.72;letter-spacing:-.06em">{self.number}</div>
    <div style="font-family:var(--disp);font-size:{title_pt}pt;font-weight:800;letter-spacing:-.035em;
                line-height:{title_lh};color:var(--ink);padding-bottom:1mm">{self.title}</div>
  </div>
  <div style="height:.7pt;background:var(--rule);margin-bottom:5mm"></div>
  <div class="kicker" style="margin-bottom:3mm">In this chapter you will learn</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 8mm">
    <ul class="bullet" style="font-size:9.4pt">{col(objectives[:half])}</ul>
    <ul class="bullet" style="font-size:9.4pt">{col(objectives[half:])}</ul>
  </div>
</div>''', variant="bleed", head=False, foot=False, nogloss=True,
            toc=[(1, f"Hoofdstuk {self.number} — {self.title}")])

    def eigen_vocabulaire(self):
        """Two columns of blank lines for the learner's own words."""
        wl = lines(22)
        return self.page(f'''
{kicker_head("Eigen vocabulaire", "Eigen vocabulaire")}
<div style="margin-bottom:5mm">The theme of this chapter is <b>{self.title}</b>.
Which words would you like to add? Write them below.</div>
<div class="two" style="gap:0 8mm">{wl}{wl}</div>''', section="Eigen vocabulaire",
            toc=[(2, "Eigen vocabulaire")])

    def reflectie(self, checks, extras, img_mm=52):
        """The closing self-check (yes / not yet) and the online extras."""
        rr = "".join(f'<div class="fr" style="grid-template-columns:1fr 27mm">'
          f'<div>{r}</div><div style="text-align:right"><span class="box"></span>'
          f'<span class="note" style="font-style:normal;margin-right:3mm">yes</span>'
          f'<span class="box"></span><span class="note" style="font-style:normal">not yet</span></div></div>'
          for r in checks)
        return self.page(f'''
{kicker_head("Reflectie", "What can you do now?")}
<div class="form" style="padding:5mm 6mm">{rr}</div>
<div class="sp2"></div>
<div style="display:flex;gap:5mm;align-items:flex-start">
 <img src="art/reflectie.png" style="width:{img_mm}mm;height:{img_mm}mm;object-fit:cover;border-radius:3mm;flex:0 0 auto">
 <div>
  <div style="display:flex;gap:2.4mm;align-items:center;margin-bottom:2.5mm">{icon("web")}
   <div style="font-family:var(--disp);font-weight:700;font-size:10.5pt">Verdiepingsmateriaal</div></div>
  <div style="margin-bottom:2mm">At <b>coutinho.nl/nederlandsingang3</b> you can work on:</div>
  {bullets(extras)}
 </div>
</div>''', section="Reflectie", toc=[(2, "Reflectie — wat kun je nu?")])

    PLAYER = """
<script>
(function () {
  // ---- audio: click an icon to play, click again to stop ----
  // A dialogue sentence (span.say with data-t="start,end", from build.py) plays
  // just that stretch of the recording: click to hear it, click again to hear it
  // again, Shift-click to loop it until the next click.
  var audio = new Audio(), current = null, until = 0, from = 0, loop = false;
  function reset() {
    if (current) current.classList.remove("playing", "speaking");
    current = null; until = 0; loop = false;
  }
  audio.addEventListener("ended", reset);
  function watch() {                     // timeupdate is too coarse to stop on a word
    if (!until || !current) return;
    if (audio.currentTime >= until) {
      if (loop) audio.currentTime = from;
      else { audio.pause(); reset(); return; }
    }
    requestAnimationFrame(watch);
  }
  function start(el, src, a, b, cls) {
    reset();
    if (audio.getAttribute("src") !== src) audio.src = src;
    audio.currentTime = a;
    audio.play().then(function () {
      current = el; el.classList.add(cls); from = a; until = b;
      if (b) requestAnimationFrame(watch);
    }).catch(function () { el.classList.add("failed"); });
  }
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("a.i-audio");
    if (btn) {
      e.preventDefault();
      if (current === btn) { audio.pause(); reset(); return; }
      start(btn, btn.dataset.src, 0, 0, "playing");
      return;
    }
    var say = e.target.closest(".say[data-t]");
    // on a touch screen a tap on a glossed word opens its translation instead
    if (!say || (touched && e.target.closest(".gloss"))) return;
    if (current === say && loop) { audio.pause(); reset(); return; }
    var t = say.dataset.t.split(",").map(Number);
    start(say, say.closest("dl").dataset.audio, t[0], t[1], "speaking");
    loop = e.shiftKey;
  });
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".say[data-t]").forEach(function (s) {
      s.title = "Click to hear this sentence (Shift-click to loop it)";
    });
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

    def articles_html(self):
        """The de/het nouns as data, plus the typing drill that uses them.

        Same shape as the deck: linked script, DOM built at runtime, screen only.
        """
        if not self.articles:
            return ""
        payload = json.dumps(self.articles, ensure_ascii=False, separators=(",", ":"))
        return ('<script type="application/json" id="nl-articles-data">'
                + payload.replace("</", "<\\/") + "</script>"
                + f'<script src="{self.articles_js}" defer></script>')

    def talk(self, audio, same=None):
        """Add a speak-the-dialogue drill for one dialogue recording.

        The drill (shared/talk.js) reads every dialogue() printed with this
        audio=, in page order. `same` merges book labels that name one person,
        so the learner picks a person, not a label: {"Cursist": "Susy"}.
        """
        self.talks.append({"audio": audio, "same": same or {}})

    def talk_html(self):
        """The drills as data, plus the script that builds them. Screen only."""
        if not self.talks:
            return ""
        payload = json.dumps(self.talks, ensure_ascii=False, separators=(",", ":"))
        return ('<script type="application/json" id="nl-talk-data">'
                + payload.replace("</", "<\\/") + "</script>"
                + f'<script src="{self.talk_js}" defer></script>')

    def extras(self):
        """This chapter's own extra.css and extra.js, if its folder has them.

        The one place for styling or behaviour that belongs to a single chapter:
        nothing in shared/ changes, and deleting the file removes the feature.
        extra.css loads after style.css, so it can override it, and it reaches the
        PDF too. extra.js runs in print as well: build any screen-only UI hidden
        and reveal it under @media screen, like the deck.
        """
        if not self.folder:
            return "", ""
        has = lambda name: os.path.exists(os.path.join(self.folder, name))
        return ('<link rel="stylesheet" href="extra.css">' if has("extra.css") else "",
                '<script src="extra.js" defer></script>' if has("extra.js") else "")

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
        if self.articles:
            panel += '<div id="nl-articles"></div>'
        if last < 0:                       # no word list: put it at the end
            return "".join(self.pages) + panel
        return ("".join(self.pages[:last + 1]) + panel
                + "".join(self.pages[last + 1:]))

    def html(self):
        # Without the viewport meta a phone lays the page out at ~980px and then
        # zooms the whole thing out — the sheet is legible only by pinching. It
        # costs nothing in print, where @page decides the size.
        css, js = self.extras()
        return (f'<meta charset="utf-8">'
                f'<meta name="viewport" content="width=device-width, initial-scale=1">'
                f'<title>Nederlands in gang — Hoofdstuk {self.number}: {self.title}</title>'
                f'<link rel="stylesheet" href="{self.css}">' + css
                + self.body() + self.PLAYER + self.deck_html() + self.answers_html()
                + self.articles_html() + self.talk_html() + js)

    def write(self, path):
        open(path, "w", encoding="utf-8").write(self.html())
        return len(self.pages)


def timeline(points, today=None):
    """A small horizontal time line: [(relative word, day), …].

    Drawn as SVG rather than generated art for the same reason as clock(): it is
    nothing but labels. Pass today= to mark one point as the present.

    NOTE: the book prints its days as a plain list. This is a study aid, like the
    sentence translations, not transcribed content — every pairing shown is one
    the book states, nothing is inferred.
    """
    ink, teal, orange, rule = "#1E2A2E", "#14616B", "#E8632A", "#D9CFBC"
    n = len(points)
    x0, x1, y = 16, 232, 26          # the arrow needs room past the last tick
    step = (x1 - x0) / (n - 1) if n > 1 else 0

    s = [f'<line x1="{x0 - 8}" y1="{y}" x2="{x1 + 20}" y2="{y}" stroke="{rule}" '
         f'stroke-width="0.8"/>',
         f'<path d="M {x1 + 20} {y} l -3.4 -2 v 4 Z" fill="{rule}"/>']
    for i, (word, day) in enumerate(points):
        cx = x0 + step * i
        now = (today is not None and i == today)
        s.append(f'<circle cx="{cx:.1f}" cy="{y}" r="{2.6 if now else 1.6:.1f}" '
                 f'fill="{orange if now else rule}"/>')
        if word:
            s.append(f'<text x="{cx:.1f}" y="{y - 6.5:.1f}" text-anchor="middle" '
                     f'font-size="{5.0 if now else 4.5}" font-weight="700" '
                     f'fill="{orange if now else ink}">{word}</text>')
        s.append(f'<text x="{cx:.1f}" y="{y + 10:.1f}" text-anchor="middle" '
                 f'font-size="4.3" fill="{teal}">{day}</text>')
    return ('<svg class="tline" viewBox="0 0 260 40" role="img" '
            'aria-label="Time line of the days">' + "".join(s) + "</svg>")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build one chapter into a PDF.

    python3 book/build.py ch01-welcome
    python3 book/build.py ch01-welcome --compare   # must match what HEAD has

--compare is for changes that should not change the output — a refactor of
pages.py, layout.py or style.css. Every page is rendered and compared pixel for
pixel with the PDF committed at HEAD, and index.html with HEAD's (whitespace
ignored). Any difference fails the build and names the page.

Pipeline: pages.py -> sentence timings -> index.html -> Chrome (print-to-pdf) -> bookmarks + metadata.
Afterwards it checks every page for content spilling outside the trim size.
"""
import glob, json, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "shared", "lib"))
from modules import load
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PAGE_HEIGHT_PX = 907     # 240 mm at 96 dpi
FOOTER_MARGIN  = 30      # space reserved at the bottom for the running foot

LAYOUT_CHECK = """
<script>addEventListener("load",()=>{
  const LIMIT=%d-%d, pages=[...document.querySelectorAll(".page")];
  const keeps={}, over=[], mixed=[];
  pages.forEach((p,i)=>{
    // A page may continue the previous section, or start a new one — not both.
    // An exercise sitting above a section heading has nothing telling the reader
    // which section it belongs to.
    const h2=p.querySelector("h2.sec"), task=p.querySelector(".task");
    if(h2 && task && (h2.compareDocumentPosition(task) & Node.DOCUMENT_POSITION_PRECEDING))
      mixed.push("p"+(i+1));
    p.querySelectorAll("[data-keep]").forEach(k=>{
      (keeps[k.dataset.keep] = keeps[k.dataset.keep] || []).push(i+1); });
    if(p.classList.contains("bleed")) return;
    let max=0, top=p.getBoundingClientRect().top;
    p.querySelectorAll("*").forEach(e=>{
      if(e.closest(".rh")||e.closest(".pf")) return;
      const r=e.getBoundingClientRect();
      if(r.height&&r.width) max=Math.max(max,r.bottom-top); });
    if(max>LIMIT) over.push("p"+(i+1)+":"+max.toFixed(0));
  });
  const split=Object.keys(keeps).filter(n=>new Set(keeps[n]).size>1)
        .map(n=>n+"@p"+[...new Set(keeps[n])].join("+p"));
  // The result travels back as JSON in a script element, read from --dump-dom.
  const out=document.createElement("script");
  out.type="application/json"; out.id="layout-result";
  out.textContent=JSON.stringify({over, split, mixed, keeps:Object.keys(keeps).length,
                                  answers: window.__answerReport || null});
  document.body.appendChild(out);
});</script>
""" % (PAGE_HEIGHT_PX, FOOTER_MARGIN)


def load_chapter(cdir):
    """Import a chapter's pages.py in isolation and return its Chapter."""
    saved = list(sys.path)
    for stale in ("content", "pages"):
        sys.modules.pop(stale, None)
    try:
        ch = load(os.path.join(cdir, "pages.py"), "pages", register=True).ch
        ch.folder = cdir
        return ch
    finally:
        sys.path[:] = saved


def glossed_html(cdir, ch):
    """This chapter's HTML with first-in-the-book hover translations applied.

    "First" means first in the whole book, so every earlier chapter is generated
    (in Python only, no Chrome) purely to learn which words are already spoken for.
    """
    sys.path.insert(0, os.path.join(ROOT, "shared", "lib"))
    from glossary import build_glossary, gloss_html
    chapters = sorted(glob.glob(os.path.join(ROOT, "ch[0-9][0-9]-*")))
    glossary = build_glossary(chapters)
    seen = set()
    for earlier in chapters:
        if os.path.abspath(earlier) == os.path.abspath(cdir):
            break
        gloss_html(load_chapter(earlier).html(), glossary, seen)
    before = len(seen)
    out = gloss_html(ch.html(), glossary, seen)
    print(f"  glossary  : {len(seen)-before} first occurrences marked "
          f"({before} already introduced earlier, {len(glossary)} headwords)")
    return out


def build_deck(cdir, ch):
    """Attach this chapter's practice cards, and say what audio is still missing.

    Safe to run before glossing: the cards ride in a <script type="application/json">
    block, and glossary.py skips <script> subtrees, so the deck is never glossed.
    """
    sys.path.insert(0, os.path.join(ROOT, "shared", "lib"))
    from glossary import load_chapter_content
    import cloze
    content = load_chapter_content(cdir)
    ch.deck = cloze.deck(content, ch.number)
    unknown = cloze.unclassified(content)
    if unknown:
        print(f"  CARDS     : content.py name(s) not classified for cards: {', '.join(unknown)}"
              "\n              add each to cloze.PROSE (mined for sentences) or cloze.NOT_PROSE")

    # <chapter>/translations.py holds the English for the quoted sentences. It is
    # the one file here whose text is not the book's, so it is kept separate from
    # content.py and a gap in it is reported rather than filled in.
    tpath = os.path.join(cdir, "translations.py")
    translations = {}
    if os.path.exists(tpath):
        translations = getattr(load(tpath, "translations"), "SENTENCES", {})
    missing = cloze.attach_meaning(ch.deck, translations)

    # <chapter>/answers.py is the book's own Bijlage 8, transcribed. It is
    # optional: most exercises have no printed answer and must stay that way.
    apath = os.path.join(cdir, "answers.py")
    if os.path.exists(apath):
        amod = load(apath, "answers")
        ch.answers = {str(k): v for k, v in getattr(amod, "ANSWERS", {}).items()}
        # column answers keep the book's down-the-column reading order
        for num, cols in getattr(amod, "ANSWER_COLUMNS", {}).items():
            cells = "".join(f"<span>{c}</span>" for col in cols for c in col)
            ch.answers[str(num)] = f'<div class="answer-cols">{cells}</div>'

    voc = len(getattr(load_chapter_content(cdir), "VOC", []) or [])
    import articles
    ch.articles = articles.nouns(getattr(content, "VOC", []) or [])
    print(f"  articles  : {len(ch.articles)} de/het nouns for the typing drill")
    produce = sum(1 for c in ch.deck if c["cloze"])
    # A production card is answered with the text taken out of the sentence.
    # If `blank` ever drifts from what the cloze actually removed, the card
    # becomes unpassable — that shipped once, for 14 cards in chapter 1.
    wrong_blank = []
    for c in ch.deck:
        if not c["cloze"]:
            continue
        pre, _, post = c["cloze"].partition("______")
        removed = c["sentence"][len(pre):len(c["sentence"]) - len(post)]
        if (c["blank"] or "") != removed:
            wrong_blank.append(f'{c["front"]}: blank={c["blank"]!r} removed={removed!r}')

    withmeaning = sum(1 for c in ch.deck if c["meaning"])
    print(f"  cards     : {len(ch.deck)} from {voc} Woordenlijst entries")
    print(f"              {produce} unlock a typed production card, "
          f"{withmeaning} carry a translated sentence")
    if ch.answers:
        nums = sorted(int(n) for n in ch.answers)
        print(f"  answers   : {len(nums)} of {len(set(re.findall(r'data-opdracht=.([0-9]+).', ch.html())))}"
              f" Opdrachten (from Bijlage 8): " + ", ".join(str(n) for n in nums))
    if unknown:
        return ch.deck, True
    if wrong_blank:
        print(f"  CLOZE     : {len(wrong_blank)} card(s) whose answer is not the "
              f"text removed from the sentence:")
        for line in wrong_blank[:5]:
            print(f"              {line}")
        return ch.deck, True
    if missing:
        print(f"  MEANINGS  : {len(missing)} sentence(s) with no entry in "
              f"translations.py — add them:")
        for sentence in missing:
            print(f"              {sentence}")
        return ch.deck, True
    return ch.deck, False


def git_head(path):
    """The bytes of `path` as committed at HEAD, or None."""
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    if not top:
        return None
    rel = os.path.relpath(path, top)
    r = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=top, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def compare_with_head(pdf_path, html_path):
    """Pixel-compare the new PDF, and compare index.html, with HEAD's."""
    import fitz
    problems = False
    old = git_head(pdf_path)
    if old is None:
        print("  compare   : PROBLEM, no committed PDF at HEAD to compare with")
        return True
    a, b = fitz.open(stream=old, filetype="pdf"), fitz.open(pdf_path)
    if a.page_count != b.page_count:
        print(f"  compare   : PROBLEM, {a.page_count} pages at HEAD, {b.page_count} now")
        problems = True
    differ = []
    for i in range(min(a.page_count, b.page_count)):
        pa, pb = a[i].get_pixmap(dpi=100), b[i].get_pixmap(dpi=100)
        if (pa.width, pa.height) != (pb.width, pb.height) or pa.samples != pb.samples:
            differ.append(f"p{i+1}")
    print("  compare   :", "PDF pixel-identical to HEAD" if not differ
          else "PROBLEM, pages differ from HEAD: " + " ".join(differ))
    problems = problems or bool(differ)

    norm = lambda t: re.sub(r">\s+<", "><", re.sub(r"\s+", " ", t))
    old_html = git_head(html_path)
    new_html = norm(open(html_path, encoding="utf-8").read())
    if old_html is not None and norm(old_html.decode("utf-8")) != new_html:
        old_html = norm(old_html.decode("utf-8"))
        at = next((i for i, (x, y) in enumerate(zip(old_html, new_html)) if x != y),
                  min(len(old_html), len(new_html)))
        print(f"              PROBLEM, index.html differs from HEAD near: "
              f"{new_html[max(0, at-50):at+50]!r}")
        problems = True
    elif old_html is not None:
        print("              index.html identical to HEAD")
    return problems


def report_answers(ch, report):
    """Every answer in answers.py must land on its question.

    answers.js chooses a spot by the shape of the exercise. A new shape it does
    not know falls back to a block under the exercise, and an answer whose
    Opdracht is missing from the page is dropped — both silently, in the browser.
    The report it leaves behind makes them a build failure instead.
    """
    if not ch.answers:
        return False
    if report is None:
        print("  answers   : PROBLEM, answers.js did not report — is it linked?")
        return True
    bad = []
    if report["missing"]:
        bad.append("no Opdracht on the page for " + ", ".join(report["missing"]))
    if report["block"]:
        bad.append("not placed on the question (fell back to a block): "
                   + ", ".join(report["block"]))
    print("  answer fit:", f"{len(report['inline'])} placed on their question"
          if not bad else "PROBLEM, " + "; ".join(bad))
    return bool(bad)


def main():
    problems = False
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    compare = "--compare" in sys.argv
    if not args:
        print(__doc__); sys.exit(1)
    chapter = args[0].rstrip("/")
    cdir = os.path.join(ROOT, chapter)
    if not os.path.isdir(cdir):
        sys.exit(f"no such directory: {cdir}")

    ch = load_chapter(cdir)
    _, deck_problem = build_deck(cdir, ch)
    problems = problems or deck_problem
    # Each dialogue sentence gets its place in the recording, so it can be replayed
    # alone. A sentence that cannot be placed would play the wrong words.
    import timings
    ch.pages, said, unplaced = timings.attach(cdir, ch.pages)
    if unplaced:
        print("  sentences : PROBLEM, " + "; ".join(unplaced))
        problems = True
    elif not said.startswith("0 "):
        print(f"  sentences : {said} timed for replay")
    page_html = glossed_html(cdir, ch)
    html = os.path.join(cdir, "index.html")
    open(html, "w", encoding="utf-8").write(page_html)
    print(f"{chapter}: {len(ch.pages)} pages -> index.html")

    # --- does any content fall outside the trim? ---
    probe = os.path.join(cdir, "_check.html")
    open(probe, "w", encoding="utf-8").write(page_html + LAYOUT_CHECK)
    try:
        dom = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                              "--virtual-time-budget=20000", "--dump-dom", "file://" + probe],
                             capture_output=True, text=True, timeout=180).stdout
        m = re.search(r'<script type="application/json" id="layout-result">(.*?)</script>', dom, re.S)
        if not m:
            print("  layout    : PROBLEM, Chrome returned no result — the checks did not run")
            problems = True
        else:
            r = json.loads(m.group(1))
            over, split, mixed = r["over"], r["split"], r["mixed"]
            print("  overflow  :", "clean" if not over
                  else "PROBLEM, past the trim: " + " ".join(over))
            print(f"  keep-blocks: {r['keeps']} checked,",
                  "none split" if not split
                  else "PROBLEM, split across pages: " + " ".join(split))
            print("  section mix:", "clean" if not mixed
                  else "PROBLEM, exercises above a new section heading on " + " ".join(mixed))
            problems = problems or bool(over or split or mixed)
            problems = report_answers(ch, r["answers"]) or problems
    finally:
        os.path.exists(probe) and os.remove(probe)

    # --- PDF ---
    raw = os.path.join(tempfile.gettempdir(), chapter + "_raw.pdf")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", f"--print-to-pdf={raw}",
                    "--virtual-time-budget=30000", "file://" + html],
                   capture_output=True, timeout=300)

    import fitz
    doc = fitz.open(raw)

    # Chrome bakes an absolute path into file links. Make them relative so the
    # PDF keeps working when it is moved, and so no home directory leaks out.
    fixed = 0
    for page in doc:
        for link in page.get_links():
            target = link.get("file") or ""
            if "/audio/" in target:
                link["file"] = "audio/" + os.path.basename(target)
                page.update_link(link); fixed += 1
    if fixed:
        print(f"  audio links: {fixed} rewritten to relative paths")

    if getattr(ch, "toc", None):
        doc.set_toc(ch.toc)
        # Bookmark page numbers are typed by hand, so they go stale when a page
        # is added or removed — ch2's were all one off after its page 3 went.
        # Each bookmark's page must show its section number, its Opdracht, or
        # (for Cultuur, Reflectie, …) its name.
        stale = []
        for level, label, pno in ch.toc:
            if level == 1:
                continue
            m = re.match(r"(\d+\.\d+)|Opdracht (\d+)", label)
            if m and m.group(1):
                key = r"(?<![\d.])" + re.escape(m.group(1)) + r"(?!\d)"
            elif m:
                key = r"opdracht\s*" + m.group(2) + r"(?!\d)"
            else:
                key = re.escape(re.sub(r"\s+", "", label.split("—")[0]).lower())
            text = doc[pno - 1].get_text() if 0 < pno <= doc.page_count else ""
            if not re.search(key, re.sub(r"\s+", "", text).lower() if not m else text.lower()):
                stale.append(f"{label.strip()}@p{pno}")
        print("  bookmarks :", "clean" if not stale
              else "PROBLEM, not on their page: " + ", ".join(stale))
        problems = problems or bool(stale)
    doc.set_metadata({
        "title": f"Nederlands in gang — Hoofdstuk {ch.number}: {ch.title} (redesigned)",
        "author": "Berna de Boer, Margaret van der Kamp, Birgit Lijmbach",
        "subject": (f"Chapter {ch.number} of Nederlands in gang (Coutinho, 3rd revised edition 2017), "
                    "redesigned and typeset from scratch."),
        "keywords": "Nederlands, Dutch, A1, A2, NT2",
        "creator": "HTML/CSS -> Chrome print pipeline",
        "producer": "Chrome headless + PyMuPDF",
    })
    out = os.path.join(cdir, f"{chapter}.pdf")
    doc.save(out, deflate=True, garbage=4)
    os.remove(raw)
    final = fitz.open(out)
    words = sum(len(final[i].get_text().split()) for i in range(final.page_count))
    print(f"  {os.path.basename(out)}: {final.page_count} pages, "
          f"{os.path.getsize(out)//1024} KB, {len(final.get_toc())} bookmarks, "
          f"{words} searchable words")
    if compare:
        problems = compare_with_head(out, html) or problems
    if problems:
        print("  -> problems above; the PDF was still written so you can look at it")
        sys.exit(1)

if __name__ == "__main__":
    main()

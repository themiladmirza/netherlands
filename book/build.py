#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build one chapter into a PDF.

    python3 book/build.py ch01-welcome

Pipeline: pages.py -> index.html -> Chrome (print-to-pdf) -> bookmarks + metadata.
Afterwards it checks every page for content spilling outside the trim size.
"""
import glob, importlib.util, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PAGE_HEIGHT_PX = 907     # 240 mm at 96 dpi
FOOTER_MARGIN  = 30      # space reserved at the bottom for the running foot

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

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
  document.title="R over="+over.join(",")+"|split="+split.join(",")
                +"|mixed="+mixed.join(",")+"|keeps="+Object.keys(keeps).length;
});</script>
""" % (PAGE_HEIGHT_PX, FOOTER_MARGIN)


def load_chapter(cdir):
    """Import a chapter's pages.py in isolation and return its Chapter."""
    saved = list(sys.path)
    for stale in ("content", "pages"):
        sys.modules.pop(stale, None)
    try:
        spec = importlib.util.spec_from_file_location("pages", os.path.join(cdir, "pages.py"))
        mod = importlib.util.module_from_spec(spec)
        sys.modules["pages"] = mod
        spec.loader.exec_module(mod)
        return mod.ch
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
    ch.deck = cloze.deck(load_chapter_content(cdir), ch.number)

    # <chapter>/translations.py holds the English for the quoted sentences. It is
    # the one file here whose text is not the book's, so it is kept separate from
    # content.py and a gap in it is reported rather than filled in.
    tpath = os.path.join(cdir, "translations.py")
    translations = {}
    if os.path.exists(tpath):
        spec = importlib.util.spec_from_file_location("translations", tpath)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        translations = getattr(mod, "SENTENCES", {})
    missing = cloze.attach_meaning(ch.deck, translations)
    voc = len(getattr(load_chapter_content(cdir), "VOC", []) or [])
    produce = sum(1 for c in ch.deck if c["cloze"])
    withmeaning = sum(1 for c in ch.deck if c["meaning"])
    print(f"  cards     : {len(ch.deck)} from {voc} Woordenlijst entries")
    print(f"              {produce} unlock a typed production card, "
          f"{withmeaning} carry a translated sentence")
    if missing:
        print(f"  MEANINGS  : {len(missing)} sentence(s) with no entry in "
              f"translations.py — add them:")
        for sentence in missing:
            print(f"              {sentence}")
        return ch.deck, True
    return ch.deck, False


def main():
    problems = False
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    chapter = sys.argv[1].rstrip("/")
    cdir = os.path.join(ROOT, chapter)
    if not os.path.isdir(cdir):
        sys.exit(f"no such directory: {cdir}")

    ch = load_chapter(cdir)
    _, deck_problem = build_deck(cdir, ch)
    problems = problems or deck_problem
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
        m = re.search(r"<title>R ([^<]*)</title>", dom)
        if m:
            parts = dict(kv.split("=", 1) for kv in m.group(1).split("|"))
            over  = [x for x in parts.get("over", "").split(",") if x]
            split = [x for x in parts.get("split", "").split(",") if x]
            print("  overflow  :", "clean" if not over
                  else "PROBLEM, past the trim: " + " ".join(over))
            mixed = [x for x in parts.get("mixed", "").split(",") if x]
            print(f"  keep-blocks: {parts.get('keeps','0')} checked,",
                  "none split" if not split
                  else "PROBLEM, split across pages: " + " ".join(split))
            print("  section mix:", "clean" if not mixed
                  else "PROBLEM, exercises above a new section heading on " + " ".join(mixed))
            problems = problems or bool(over or split or mixed)
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
    if problems:
        print("  -> problems above; the PDF was still written so you can look at it")
        sys.exit(1)

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Hover translations for the first occurrence of every Dutch word in the book.

The word lists already carry translations, so a learner meeting a word *in the
running text* has nowhere to look it up. This wraps the FIRST occurrence of each
glossary headword — first in the book as a whole, not first in its chapter — in a
span that shows its English on hover.

Deliberately excluded, via `data-nogloss` or the skip list below:
  * the word lists themselves (they are the translation)
  * running heads and page footers, which repeat on every page
  * <title>, which is text but not page content — glossing it corrupted the
    browser tab caption and silently spent three first-occurrences before the
    body was even reached

The glossary is built from every chapter's own VOC, in chapter order, so the
translation shown is the book's own.

Print is unaffected: style.css removes the underline under @media print, so the
PDF looks exactly as it did.
"""
import html as _html
import importlib.util
import os
import re
import sys

# elements whose subtree is never glossed
SKIP_CLASSES = {"vocab", "rh", "pf"}
VOID = {"img", "br", "hr", "input", "meta", "link", "source", "col"}

_TOKEN = re.compile(r"<[^>]+>|[^<]+")
_OPEN = re.compile(r"^<\s*([a-zA-Z][\w-]*)")
_CLOSE = re.compile(r"^<\s*/\s*([a-zA-Z][\w-]*)")
_CLASS = re.compile(r'class\s*=\s*"([^"]*)"')


def _strip(markup):
    """Visible text of a glossary cell: no tags, no entities, collapsed spaces."""
    text = re.sub(r"<[^>]+>", "", markup)
    text = _html.unescape(text.replace("&nbsp;", " "))
    return re.sub(r"\s+", " ", text).strip()


def load_chapter_content(chapter_dir):
    """Import one chapter's content.py in isolation and hand back the module."""
    for stale in ("content", "pages"):
        sys.modules.pop(stale, None)
    path = os.path.join(chapter_dir, "content.py")
    spec = importlib.util.spec_from_file_location("content", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["content"] = mod
    spec.loader.exec_module(mod)
    return mod


def build_glossary(chapter_dirs):
    """matchable phrase (lowercased) -> (canonical key, headword, English).

    A "de X" / "het X" entry also registers the bare noun, because the running
    text almost never repeats the article — the dialogue says *je verjaardag*,
    never *de verjaardag*. Both spellings share one canonical key, so the word is
    marked once in the book whichever form turns up first. The tooltip always
    shows the headword as the book prints it, article included.
    """
    glossary = {}
    for cdir in chapter_dirs:
        voc = getattr(load_chapter_content(cdir), "VOC", [])
        for dutch, english in voc:
            head = _strip(dutch)
            # drop the parenthesised infinitive/singular: "ben (zijn)" -> "ben"
            head = re.sub(r"\s*\([^)]*\)\s*$", "", head).strip()
            head = head.rstrip("?").strip()
            if not head or "…" in head or "..." in head:
                continue                      # discontinuous entry, nothing to match
            canonical = head.lower()
            if canonical in {v[0] for v in glossary.values()}:
                continue                      # an earlier chapter already owns it
            forms = [head]
            bare = re.sub(r"^(?:de|het)\s+", "", head, flags=re.IGNORECASE)
            if bare.lower() != head.lower() and " " not in bare:
                forms.append(bare)
            for form in forms:
                glossary.setdefault(form.lower(), (canonical, head, _strip(english)))
    return glossary


def _pattern(glossary):
    """One alternation, longest phrase first so multi-word entries win."""
    heads = sorted(glossary, key=len, reverse=True)
    if not heads:
        return None
    alts = "|".join(re.escape(h) for h in heads)
    # (?<!\w) / (?!\w) rather than \b so that é ë ï behave as word characters
    return re.compile(rf"(?<!\w)({alts})(?!\w)", re.IGNORECASE)


def gloss_html(markup, glossary, seen):
    """Wrap the first not-yet-seen occurrence of each headword. Mutates `seen`."""
    pattern = _pattern(glossary)
    if pattern is None:
        return markup

    out, stack, skip_depth = [], [], None

    for token in _TOKEN.findall(markup):
        if token.startswith("<"):
            close = _CLOSE.match(token)
            if close:
                if stack:
                    stack.pop()
                if skip_depth is not None and len(stack) < skip_depth:
                    skip_depth = None
                out.append(token)
                continue
            open_ = _OPEN.match(token)
            if open_:
                tag = open_.group(1).lower()
                if tag not in VOID and not token.rstrip().endswith("/>"):
                    m_cls = _CLASS.search(token)
                    classes = set(m_cls.group(1).split()) if m_cls else set()
                    stack.append(tag)
                    if skip_depth is None and (
                        "data-nogloss" in token
                        or tag in ("script", "style", "svg", "title", "head")
                        or classes & SKIP_CLASSES
                    ):
                        skip_depth = len(stack)
            out.append(token)
            continue

        # ---- text node ----
        if skip_depth is not None or not token.strip():
            out.append(token)
            continue

        pos, pieces = 0, []
        for m in pattern.finditer(token):
            entry = glossary.get(m.group(1).lower())
            if entry is None or entry[0] in seen:
                continue
            canonical, headword, english = entry
            seen.add(canonical)
            pieces.append(token[pos:m.start()])
            # show the book's headword too when the text uses a different form
            # ("verjaardag" in the sentence, "de verjaardag" in the word list)
            label = english if m.group(1).lower() == headword.lower() \
                else f"{headword} · {english}"
            pieces.append(
                f'<span class="gloss" data-en="{_html.escape(label, quote=True)}">'
                f'{m.group(1)}</span>')
            pos = m.end()
        pieces.append(token[pos:])
        out.append("".join(pieces))

    return "".join(out)

# -*- coding: utf-8 -*-
"""Where each dialogue sentence sits in its recording.

The page's sentences (layout.sentences) are matched word by word against the
speech-to-text word timings that generate_audio.py saves beside each dialogue
(<id>.words.json). Words the transcript renders differently — "22" spoken as
"tweeëntwintig" — simply don't match; the cut between two sentences is placed
in the longest pause between the last word matched to one and the first word
matched to the next, so an unmatched word still lands in the right sentence.
"""
import difflib, html, json, os, re

LEAD, TAIL = 0.25, 0.45     # seconds kept before the first and after the last word
MIN_LENGTH = 0.3            # a shorter sentence means the alignment went wrong

def words_of(text):
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return [w for w in (re.sub(r"[^\w]", "", t.lower()) for t in text.split()) if w]

def align(sentences, words):
    """[(start, end)] per sentence, or raise ValueError saying why not."""
    page = [(i, w) for i, s in enumerate(sentences) for w in words_of(s)]
    heard = [re.sub(r"[^\w]", "", w[0].lower()) for w in words]
    owner = {}                                  # transcript index -> sentence
    sm = difflib.SequenceMatcher(None, [w for _, w in page], heard, autojunk=False)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            owner[b + k] = page[a + k][0]

    n = len(sentences)
    matched = [sorted(t for t, s in owner.items() if s == i) for i in range(n)]
    if not any(matched):
        raise ValueError("no sentence matches the recording")
    # cuts[i] is the time between sentence i and i+1
    cuts, i = [], 0
    while i < n - 1:
        lo = max((m[-1] for m in matched[:i + 1] if m), default=-1)
        j = next((k for k in range(i + 1, n) if matched[k]), None)
        if j is None:
            raise ValueError(f"nothing after sentence {i + 1} matches: {sentences[i + 1]!r}")
        hi = matched[j][0]
        need = j - i                            # unmatched sentences need cuts too
        gaps = sorted(range(max(lo, 0), hi), reverse=True,
                      key=lambda t: words[t + 1][1] - words[t][2])[:need]
        if len(gaps) < need:
            raise ValueError(f"cannot place the cut before {sentences[i + 1]!r}")
        for t in sorted(gaps):
            cuts.append((words[t][2] + words[t + 1][1]) / 2)
        i = j
    bounds = [max(0.0, words[0][1] - LEAD)] + cuts + [words[-1][2] + TAIL]
    spans = [(round(bounds[k], 2), round(bounds[k + 1], 2)) for k in range(n)]
    for (a, b), s in zip(spans, sentences):
        if b - a < MIN_LENGTH:
            raise ValueError(f"{s!r} came out {b - a:.2f}s long")
    return spans

SAY = re.compile(r'<span class="say">(.*?)</span>')

def attach(cdir, pages):
    """Give every <span class="say"> in `pages` its data-t="start,end".

    Returns (pages, report, problems). Dialogues sharing a recording are aligned
    together, in page order.
    """
    groups = {}                                 # audio -> sentences in order
    for page in pages:
        for dl in re.finditer(r'<dl class="[^"]*" data-audio="([^"]+)">(.*?)</dl>', page, re.S):
            groups.setdefault(dl.group(1), []).extend(SAY.findall(dl.group(2)))
    spans, problems = {}, []
    for audio, sents in groups.items():
        path = os.path.join(cdir, audio[:-4] + ".words.json")
        if not os.path.exists(path):
            problems.append(f"{audio}: no word timings — run generate_audio.py --check")
            continue
        try:
            spans[audio] = iter(align(sents, json.load(open(path, encoding="utf-8"))))
        except ValueError as e:
            problems.append(f"{audio}: {e}")

    def mark(dl):
        it = spans.get(dl.group(1))
        if it is None:
            return dl.group(0)
        return SAY.sub(lambda m: '<span class="say" data-t="%s,%s">%s</span>'
                       % (*next(it), m.group(1)), dl.group(0))
    pages = [re.sub(r'<dl class="[^"]*" data-audio="([^"]+)">.*?</dl>', mark, p, flags=re.S)
             for p in pages]
    count = sum(len(s) for a, s in groups.items() if a in spans)
    return pages, f"{count} sentences in {len(spans)} recording(s)", problems

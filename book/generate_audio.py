#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a chapter's audio with ElevenLabs.

    # key comes from .env automatically; to override:  export ELEVENLABS_API_KEY=sk_...
    python3 book/generate_audio.py ch01-welcome          # only what's missing
    python3 book/generate_audio.py ch01-welcome --all    # everything again
    python3 book/generate_audio.py ch01-welcome --check  # verify existing files only
    python3 book/generate_audio.py ch01-welcome --all --model eleven_v4
    python3 book/generate_audio.py ch01-welcome --cards  # flashcard sentences

Reads <chapter>/audio_script.py (what is said, by whom, with what delivery) and
shared/lib/voices.py (the cast). Writes <chapter>/audio/<id>.mp3.

Multi-speaker items go to /v1/text-to-dialogue so the voices answer each other in
one take. Single-speaker items go to /v1/text-to-speech.

Every file is verified by transcribing it back (speech-to-text) and comparing to
the script with the emotion tags stripped. That catches a voice mangling Dutch or
reading a tag aloud — it will not catch a merely ugly read, so listen too.
"""
import argparse, difflib, importlib.util, json, os, re, sys, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "shared", "lib"))
from env import load_env; load_env()
import voices as cast

API = "https://api.elevenlabs.io/v1"

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def post(url, payload, key, tries=6):
    """POST with backoff, so a single 429 never ends a run."""
    for attempt in range(tries):
        req = urllib.request.Request(url, data=json.dumps(payload).encode(),
            headers={"xi-api-key": key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            retryable = e.code == 429 or e.code >= 500
            if not retryable or attempt == tries - 1:
                raise
            wait = int(e.headers.get("retry-after") or (2 ** attempt) * 5)
            print(f"        {e.code} — waiting {wait}s", flush=True)
            time.sleep(wait)

def spoken(text):
    """The script with [emotion tags] removed — what should actually be heard."""
    return re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", " ", text)).strip()

def transcribe(path, key):
    boundary = "----nlverify"
    body = b""
    body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"model_id\"\r\n\r\nscribe_v1\r\n".encode()
    # Pin the language. Everything recorded here is Dutch, and on short clips
    # ("En u, mevrouw?") auto-detect guessed Swedish and scored a good file at 51%.
    body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"language_code\"\r\n\r\nnld\r\n".encode()
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"a.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n").encode()
    body += open(path, "rb").read() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(f"{API}/speech-to-text", data=body,
        headers={"xi-api-key": key, "Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r).get("text", "")

def norm(s):
    return re.sub(r"[^a-zà-ÿ0-9 ]", "", s.lower()).strip()

def verify(path, expected, key):
    try:
        got = transcribe(path, key)
    except Exception as e:
        return None, f"transcription failed: {e}"
    ratio = difflib.SequenceMatcher(None, norm(expected), norm(got)).ratio()
    return ratio, got

def cards(cdir, key, redo, check_only):
    """Record the sentence a flashcard quotes, one clip per distinct sentence.

    The cards play the sentence rather than the bare word, so the learner hears
    the word used. Sentences are deduped: several cards quote the same line.
    Recorded with eleven_v4 and one narrator for the whole book — these are
    reference recordings, so clarity matters more than character.
    """
    sys.path.insert(0, os.path.join(ROOT, "shared", "lib"))
    from glossary import load_chapter_content
    import cloze as cloze_mod

    number = int(os.path.basename(cdir.rstrip("/"))[2:4])
    deck = cloze_mod.deck(load_chapter_content(cdir), number)
    clips = cloze_mod.sentence_clips(deck)
    os.makedirs(os.path.join(cdir, "audio", "cards"), exist_ok=True)

    todo = [(rel, text) for rel, text in clips
            if redo or not os.path.exists(os.path.join(cdir, rel))]
    print(f"  {len(clips)} sentences, {len(todo)} to record "
          f"({sum(len(t) for _, t in todo):,} characters)")

    made = 0
    for rel, text in todo:
        if check_only:
            break
        data = post(f"{API}/text-to-speech/{cast.VOICES['kaart']}", {
            "model_id": "eleven_v4", "text": text,
            "voice_settings": cast.CARD_SETTINGS}, key)
        open(os.path.join(cdir, rel), "wb").write(data)
        made += 1
        if made % 20 == 0:
            print(f"        {made}/{len(todo)}", flush=True)

    # Sentences are whole phrases, which is what speech-to-text handles well, so
    # every one is verified -- unlike the single words, which it cannot score.
    bad = 0
    for rel, text in clips:
        path = os.path.join(cdir, rel)
        if not os.path.exists(path):
            continue
        ratio, got = verify(path, text, key)
        if ratio is not None and ratio < 0.85:
            bad += 1
            print(f"  CHECK {rel}  match {ratio:.0%}")
            print(f"        expected: {text[:80]}")
            print(f"        heard   : {got[:80]}")
    missing = [r for r, _ in clips if not os.path.exists(os.path.join(cdir, r))]
    print(f"  recorded {made}, {len(missing)} missing, "
          f"{len(clips) - bad - len(missing)}/{len(clips) - len(missing)} verified")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter"); ap.add_argument("--all", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--cards", action="store_true",
                    help="record the sentences the flashcards quote")
    ap.add_argument("--model", default=cast.MODEL,
                    help=f"TTS model id (default {cast.MODEL}). Lets one chapter "
                         "try a new model without recasting the whole book.")
    a = ap.parse_args()

    key = os.environ.get("ELEVENLABS_API_KEY") or sys.exit("ELEVENLABS_API_KEY is not set")
    cdir = os.path.join(ROOT, a.chapter.rstrip("/"))
    if a.cards:
        return cards(cdir, key, a.all, a.check)
    script = load(os.path.join(cdir, "audio_script.py"), "audio_script")
    outdir = os.path.join(cdir, "audio"); os.makedirs(outdir, exist_ok=True)

    for item in script.ITEMS:
        # An item may pin its own model. Chapter 1 does: v4 reads the numerals
        # and the sentence-stress drill better, but mangles the alphabet —
        # it duplicates runs of letters and says "Y" for both ij and ei.
        model = item.get("model", a.model)
        path = os.path.join(outdir, item["id"] + ".mp3")
        expected = (" ".join(spoken(t) for _, t in item["lines"])
                    if item["kind"] == "dialogue" else spoken(item["text"]))
        if not a.check and (a.all or not os.path.exists(path)):
            if item["kind"] == "dialogue":
                data = post(f"{API}/text-to-dialogue", {
                    "model_id": model,
                    "inputs": [{"voice_id": cast.VOICES[role], "text": text}
                               for role, text in item["lines"]]}, key)
            else:
                data = post(f"{API}/text-to-speech/{cast.VOICES[item['voice']]}", {
                    "model_id": model, "text": item["text"],
                    "voice_settings": cast.SETTINGS}, key)
            open(path, "wb").write(data)
        if not os.path.exists(path):
            print(f"  {item['id']:<12} missing"); continue
        kb = os.path.getsize(path)//1024
        ratio, got = verify(path, expected, key)
        flag = "ok  " if (ratio or 0) >= 0.85 else "CHECK"
        print(f"  {flag} {item['id']:<12} {kb:>4} KB   match {ratio:.0%}" if ratio
              else f"  ?    {item['id']:<12} {kb:>4} KB   {got}")
        if ratio and ratio < 0.85:
            print(f"        expected: {expected[:90]}")
            print(f"        heard   : {got[:90]}")

if __name__ == "__main__":
    main()

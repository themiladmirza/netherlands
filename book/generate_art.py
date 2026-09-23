#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a chapter's illustrations.

    # key comes from .env automatically; to override:  export OPENAI_API_KEY=sk-...
    python3 book/generate_art.py ch01-welcome         # only what's missing
    python3 book/generate_art.py ch01-welcome --all   # regenerate everything

Reads the scenes from <chapter>/art_prompts.py and the shared style from
shared/lib/art_style.py. Writes <chapter>/art/<name>.png.
The API allows 5 images per minute; on a rate limit this waits and retries.
"""
import base64, importlib.util, json, os, sys, time, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "shared", "lib"))
from env import load_env; load_env()
import art_style

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    regenerate_all = "--all" in sys.argv
    if not args:
        print(__doc__); sys.exit(1)
    chapter = args[0].rstrip("/")
    cdir = os.path.join(ROOT, chapter)
    prompts = load(os.path.join(cdir, "art_prompts.py"), "art_prompts")
    outdir = os.path.join(cdir, "art"); os.makedirs(outdir, exist_ok=True)

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY is not set in the environment.")

    todo = [j for j in prompts.JOBS
            if regenerate_all or not os.path.exists(os.path.join(outdir, j[0] + ".png"))]
    if not todo:
        print("nothing to do — every image already exists (use --all to replace)"); return
    print(f"{chapter}: {len(todo)} image(s) with {art_style.MODEL}")

    for name, shape, scene in todo:
        size = art_style.SIZES[shape]
        body = json.dumps({"model": art_style.MODEL,
                           "prompt": art_style.STYLE + "\n\nSCENE: " + scene,
                           "n": 1, "size": size,
                           "quality": art_style.QUALITY}).encode()
        for attempt in range(6):
            req = urllib.request.Request(
                "https://api.openai.com/v1/images/generations", data=body,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=600) as r:
                    data = json.load(r)
                path = os.path.join(outdir, name + ".png")
                open(path, "wb").write(base64.b64decode(data["data"][0]["b64_json"]))
                print(f"  ok    {name:<12} {size:>9}  {os.path.getsize(path)//1024} KB")
                break
            except Exception as e:
                msg = e.read().decode()[:100] if hasattr(e, "read") else str(e)[:100]
                print(f"  wait  {name} ({attempt+1}/6): {msg}")
                time.sleep(35)
        else:
            print(f"  FAILED {name}")

if __name__ == "__main__":
    main()

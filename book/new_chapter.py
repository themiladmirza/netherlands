#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scaffold a new chapter folder from _template.

    python3 book/new_chapter.py 2 "In de kantine" in-the-canteen

Arguments: chapter number, the chapter's Dutch title (shown in the book),
and an English slug used for the folder name.
"""
import os, re, shutil, sys, unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def main():
    if len(sys.argv) < 4:
        print(__doc__); sys.exit(1)
    number, title, slug = int(sys.argv[1]), sys.argv[2], slugify(sys.argv[3])
    folder = f"ch{number:02d}-{slug}"
    dest = os.path.join(ROOT, folder)
    if os.path.exists(dest):
        sys.exit(f"{folder} already exists")
    shutil.copytree(os.path.join(ROOT, "_template"), dest)
    for f in ("content.py", "pages.py", "art_prompts.py"):
        p = os.path.join(dest, f)
        text = open(p, encoding="utf-8").read()
        text = (text.replace("{{NUMBER}}", str(number)).replace("{{TITLE}}", title)
                    .replace("{{FOLDER}}", folder).replace("{{PAGES}}", "?"))
        open(p, "w", encoding="utf-8").write(text)
    os.makedirs(os.path.join(dest, "art"), exist_ok=True)
    print(f"created: book/{folder}")
    print("  1. put the chapter text in content.py")
    print("  2. describe the illustrations in art_prompts.py")
    print(f"  3. python3 book/generate_art.py {folder}")
    print("  4. lay out the pages in pages.py")
    print(f"  5. python3 book/build.py {folder}")

if __name__ == "__main__":
    main()

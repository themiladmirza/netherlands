# -*- coding: utf-8 -*-
"""Load API keys from the project's .env so the scripts just work.

Walks up from this file to find .env, then puts any KEY=VALUE pairs into
os.environ. A variable already set in the real environment always wins, so you
can still override a key for one run:

    ELEVENLABS_API_KEY=sk_other python3 book/generate_audio.py ch01-welcome
"""
import os

def load_env(filename=".env"):
    here = os.path.dirname(os.path.abspath(__file__))
    while True:
        candidate = os.path.join(here, filename)
        if os.path.isfile(candidate):
            for line in open(candidate, encoding="utf-8"):
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
            return candidate
        parent = os.path.dirname(here)
        if parent == here:
            return None
        here = parent

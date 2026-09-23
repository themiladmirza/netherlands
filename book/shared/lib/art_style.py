# -*- coding: utf-8 -*-
"""Shared illustration style for ALL chapters.

This preamble is prepended to every scene prompt. Do not tweak it per chapter —
reusing it unchanged is exactly what keeps the 18 chapters looking like one book.
If you do change it, regenerate every chapter's art.
"""

MODEL   = "gpt-image-2.5-flare"   # newest available on 2026-09-12
QUALITY = "high"

# Tested against gpt-image-2.5-sunburst and gpt-image-2 on a classroom scene.
# 'flare' is flatter and more graphic, and stays more consistent across a chapter.

PALETTE = {
 "orange": "#E8632A", "deep_teal": "#14616B", "coral": "#F2A08A",
 "mustard": "#E9B44C", "sage": "#9CB29B", "cream": "#FDF6EC", "charcoal": "#23272A",
}

STYLE = (
 "Modern editorial flat-vector illustration for a premium adult language textbook. "
 "Geometric flat shapes, confident linework, generous negative space, subtle paper-grain texture, "
 "sophisticated and grown-up (never childish, no cartoon faces, no big shiny eyes, no emoji). "
 "Strict palette only: warm orange #E8632A, deep teal #14616B, soft coral #F2A08A, mustard #E9B44C, "
 "sage #9CB29B, warm cream #FDF6EC background, charcoal #23272A. "
 "CRITICAL: absolutely no text, no letters, no words, no numbers, no signage, no writing of any kind anywhere."
)

# Why "no text": the model renders letterforms unreliably. Every word on the page
# is real vector type from content.py — the art only carries atmosphere.

SIZES = {"portrait": "1024x1536", "landscape": "1536x1024", "square": "1024x1024"}

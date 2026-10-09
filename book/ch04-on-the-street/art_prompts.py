# -*- coding: utf-8 -*-
"""Chapter 4 — Op straat.  Illustration prompts.

The shared style preamble (../shared/lib/art_style.py) is prepended to every
SCENE automatically. Describe only the scene here — not the style, not the palette.
Never mention text or numbers in the image: all type is set as real vector text.

Bert is the waiter from chapter 3, now off duty; Hans is his friend.

Generate:  python3 book/generate_art.py ch04-on-the-street
Shapes:    portrait (1024x1536) · landscape (1536x1024) · square (1024x1024)
"""

JOBS = [
 ("opener", "portrait",
  "Four young friends chatting on a stone canal bridge in an old Dutch city in late-afternoon "
  "light: two young women leaning on the railing, a young man standing, and a young man astride a "
  "bicycle with one foot on the ground. Behind them a canal with moored boats and a row of tall, "
  "narrow gabled canal houses. Relaxed, sociable, everyday street life."),

 ("dialoog", "landscape",
  "Two men in their forties bump into each other on a busy Dutch shopping street and greet each "
  "other warmly with a handshake and a pat on the shoulder. One is off-duty waiter in a casual "
  "jacket carrying an empty shopping bag; the other has a small camera bag over his shoulder. "
  "Brick shop fronts with awnings, parked bicycles, a few passers-by. Cheerful, lively."),

 ("agenda", "square",
  "An open paper diary lying on a café table with a pen resting across it, the pages divided into "
  "blank day boxes with no writing at all, a cup of coffee and a phone beside it. Seen from above. "
  "Calm, organised, planning a week."),

 ("praktijk", "square",
  "Two friends standing on a pavement; one is cheerfully suggesting something and pointing towards "
  "a café terrace across the street, the other is nodding with a smile. Bicycles and a lamppost "
  "nearby. Friendly, inviting."),

 ("reflectie", "square",
  "An abstract flat illustration of steady progress: a winding path through a small city street "
  "with rounded milestones bearing check marks, a rising sun, and a person on a bicycle partway "
  "along looking ahead. Calm, encouraging."),
]

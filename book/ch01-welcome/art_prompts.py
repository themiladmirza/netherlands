# -*- coding: utf-8 -*-
"""Chapter 1 — Welkom.  The prompts that produced art/*.png.

Generated 2026-09-12 with gpt-image-2.5-flare, quality=high.
The shared style preamble lives in ../shared/lib/art_style.py and is
automatically prepended to every SCENE below.

Regenerate:  python3 book/generate_art.py ch01-welcome          (only what's missing)
             python3 book/generate_art.py ch01-welcome --all    (everything)

Note: the API allows 5 images per minute; the script waits and retries.
"""

JOBS = [
 ("opener", "staand",
  "The first day of a Dutch language course. A warm female teacher stands welcoming a small diverse group of "
  "adult learners seated at light wooden desks with notebooks. Tall windows reveal Amsterdam canal houses, "
  "a canal and a parked bicycle. Bright morning light, optimistic and inviting."),

 ("dialoog", "liggend",
  "Three adults in a bright classroom introducing themselves to one another: a friendly teacher gesturing warmly, "
  "a young woman and a young man seated beside each other turning to greet each other. Empty blank speech bubbles "
  "float above them with no writing inside. Warm, welcoming, conversational."),

 ("landen", "vierkant",
  "A stylised globe surrounded by floating flat-shape motifs representing different countries: a Dutch canal house "
  "and tulip, a British double-decker bus and umbrella, a Chinese pagoda roof and lantern. Blank unmarked pennant "
  "flags in the palette colours. Clean, balanced, decorative composition."),

 ("telwoorden", "vierkant",
  "A row of narrow colourful Dutch canal houses with brightly painted front doors, doorbell panels and window boxes, "
  "seen straight on. A hand reaches toward a doorbell. Charming and graphic. Doors and panels are completely blank "
  "with no numbers or writing."),

 ("alfabet", "vierkant",
  "Two adults facing each other in conversation, one carefully sounding out something while the other listens and "
  "writes in a notebook. Abstract geometric sound-shapes and dots flow between them suggesting spoken letters. "
  "No actual letters or writing visible anywhere."),

 ("begroeten", "liggend",
  "A horizontal triptych of the same friendly street corner at three times of day: sunrise morning with a cyclist, "
  "bright midday with people walking, and dusk evening with warm window glow and a rising moon. People wave and "
  "greet each other in each panel. Continuous flowing composition."),

 ("formulier", "vierkant",
  "Overhead view of a desk: a blank paper form with empty ruled lines and empty tick boxes, a pen, a pair of glasses, "
  "a cup of coffee and a small plant. Clean, tidy, inviting. The form is entirely blank with no writing on it."),

 ("cultuur", "liggend",
  "Split composition contrasting two social registers: on the left a respectful formal greeting between an older "
  "person and a younger adult with a polite handshake and slight bow; on the right two friends greeting casually "
  "with a relaxed wave and warm laughter. A soft vertical divider separates the halves."),

 ("praktijk", "vierkant",
  "A close, graphic view of a Dutch front door with a vintage brass doorbell panel of blank nameplates, a letterbox, "
  "a potted plant and a bicycle leaning beside it. Warm and characterful. All nameplates completely blank."),

 ("reflectie", "vierkant",
  "An abstract flat illustration of progress and confidence: a gentle ascending path of rounded steps with small "
  "check marks, a rising sun, and a person standing at the top looking forward. Calm, encouraging, uplifting."),
]

# Where each image is placed in pages.py:
#   opener -> cover p1 · dialoog -> p2 · landen -> p7 · telwoorden -> p11
#   alfabet -> p13 · begroeten -> p14 · cultuur -> p17 · praktijk -> p18
#   reflectie -> p20 · formulier -> not placed (the form itself fills p15)

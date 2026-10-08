# -*- coding: utf-8 -*-
"""Shared voice cast for the whole series.

Keep the same person on the same voice across all eighteen chapters — the
recurring characters (the teacher, Susy, Ning) must sound like themselves.
Swap an id here and every chapter follows.

All native Dutch voices from the ElevenLabs shared library; they can be used by
id directly, no import step needed.

MODEL is eleven_v3 because it is the one that interprets emotion tags —
`[warmly] Goedemorgen` shapes the delivery, it does not read the bracket aloud
(verified: tagged and untagged renders are the same length).
"""

MODEL = "eleven_v3"

VOICES = {
    # role        voice id                name     who
    # Four roles were recast once, in October 2026, for clarity — the originals
    # were cloned from dull source audio and sounded, in the user's words, "like a
    # very old recording on a walkman". Measured as the drop in energy above 8 kHz
    # on an identical line: the old teacher lost 46.9 dB up there, the new one
    # 20.0 dB. The three unchanged voices already sit in the -23 to -28 band.
    "docent":   "3fjjbhBA9yI42Aoj0o18",  # Ariel  — the teacher: female, warm   (was Leonie, -46.9 dB)
    "susy":     "6e6TrJGLhrDGMKOy5x2i",  # Noa    — cursist from England: female, young
    "ning":     "awkQxhhcMytABHFHH3TX",  # Devin  — cursist from China: male, young (was Dean, -30.2 dB)
    "edit":     "p4efl2GlWK0o6sAQEEkp",  # Fenna  — cursist, ch2: female, young
    "andres":   "Pk1wM1jtot5sJaptlRWQ",  # Robin  — Edit's brother, ch3: male, young
    "ober":     "HGg2c3eDR1tMpbtDRAzL",  # Pieter — the waiter, ch3: male, middle-aged (was Jan, -34.3 dB)
    "vraag":    "3fjjbhBA9yI42Aoj0o18",  # Ariel  — asks in the drills (same as docent)
    "kaart":    "MkRWZTk4OBui6Jb2lgK0",  # Ruben  — reads the flashcard sentences
    "antwoord": "MkRWZTk4OBui6Jb2lgK0",  # Ruben  — answers: male, clearest measured (was Remko, -30.1 dB)
}

# The flashcard sentences use ONE voice for the whole book: a card is a reference
# recording, so diction matters more than character, and the same sentence must
# not change speaker between chapters. Ruben measured clearest of the 18 Dutch
# voices tested (-17.9 dB above 8 kHz).
CARD_SETTINGS = {"stability": 0.6, "similarity_boost": 0.8, "style": 0.0}

# Low stability keeps the emotion tags expressive; raising it flattens the read
# but makes it more predictable. Style adds delivery variation.
SETTINGS = {"stability": 0.4, "similarity_boost": 0.75, "style": 0.3}

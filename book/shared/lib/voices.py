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
    "docent":   "7kJ33vnB1HkX76L4U5km",  # Leonie — the teacher: female, warm, upbeat
    "susy":     "6e6TrJGLhrDGMKOy5x2i",  # Noa    — cursist from England: female, young
    "ning":     "NZxSzTQSMSWwkdFLuZsv",  # Dean   — cursist from China: male, young
    "edit":     "p4efl2GlWK0o6sAQEEkp",  # Fenna  — cursist, ch2: female, young, warm
    "andres":   "Pk1wM1jtot5sJaptlRWQ",  # Robin  — Edit's brother, ch3: male, young
    "ober":     "vojvEumHZHcjlpEPNZKW",  # Jan    — the waiter, ch3: male, middle-aged
    "vraag":    "7kJ33vnB1HkX76L4U5km",  # Leonie — asks in the drills
    "antwoord": "0qLmDzgqulxcvv0yf3kg",  # Remko  — answers: male, very clear diction
}

# Low stability keeps the emotion tags expressive; raising it flattens the read
# but makes it more predictable. Style adds delivery variation.
SETTINGS = {"stability": 0.4, "similarity_boost": 0.75, "style": 0.3}

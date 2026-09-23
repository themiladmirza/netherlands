# -*- coding: utf-8 -*-
"""Chapter 2 — In de kantine.  What gets spoken, by whom, with what delivery.

Text must match content.py word for word — this is the book read aloud.
Emotion tags in [brackets] steer delivery and are not spoken.

Susy keeps her chapter-1 voice. Edit is new to this chapter (see voices.py).

NOT recorded: Opdracht 15. That exercise plays word pairs and triples that the
book never prints — they exist only on the publisher's audio — so there is
nothing to transcribe, and inventing them would be making up content. The
exercise and its answer grid are kept; the icon is left inert.

Generate:  python3 book/generate_audio.py ch02-in-the-canteen
"""

ITEMS = [
 # ---------------------------------------------------------------- 2.1 Dialoog
 {"id": "dialoog", "kind": "dialogue", "label": "Susy en Edit in de kantine",
  "lines": [
   ("susy", "[politely, a little tentative] Is deze plaats vrij?"),
   ("edit", "[warmly] Ja hoor."),
   ("susy", "[settling in, contented] Zo, een lekker kopje koffie."),
   ("edit", "[making conversation] Woon je al lang in Utrecht?"),
   ("susy", "[cheerfully] Nee, pas drie dagen, of vier. Welke dag is het eigenlijk vandaag?"),
   ("edit", "Het is donderdag twintig augustus. [brightening] Morgen ben ik jarig."),
   ("susy", "[delighted] Wat leuk! Ik ben in december jarig, dus in de winter. "
            "[curious] Krijg je nog bezoek?"),
   ("edit", "Ja, mijn broer komt."),
   ("susy", "[interested] Wie is jonger? Hij of jij?"),
   ("edit", "[amused] Hij is jonger, maar wel langer."),
   ("susy", "Heb je nog meer broers of zussen?"),
   ("edit", "[pleased] Ja, ik heb nog een zus. Kijk, hier is een foto."),
   ("susy", "[surprised] Goh, ze is een heel ander type. "
            "Ze heeft kort, blond haar en jij donker haar."),
   ("susy", "[curious] Komen je ouders ook op bezoek?"),
   ("edit", "Nee, ze zijn op dit moment in Indonesië."),
   ("susy", "[intrigued] Wat doen ze daar? Zijn ze daar op vakantie?"),
   ("edit", "Ja, en mijn vader is daar ook voor zijn werk."),
   ("susy", "Welk seizoen is het daar nu? Wanneer is het daar zomer?"),
   ("edit", "[laughing lightly] Ik weet het niet. Maar vertel eens over jouw familie."),
   ("susy", "[keen, then checking] Dat wil ik wel, maar hoe laat is het eigenlijk?"),
   ("edit", "[startled] Het is elf uur. We moeten weer naar de les."),
  ]},

 # ---------------------------------------------------------------- Opdracht 16
 {"id": "opdracht16", "kind": "speech", "voice": "docent", "label": "Opdracht 16 — a / aa",
  "text": "[clearly and slowly, leaving a pause after every word, contrasting the short and long a] "
          "acht. wat. ander. was. straks. dag. half. kantine. land. lang. "
          "jaar. plaats. maand. naar. naam. dagen. jarig. ja. vader. maken. "
          "acht. jaar. was. dagen. dag. plaats. straks. land. maken. vader."},
]

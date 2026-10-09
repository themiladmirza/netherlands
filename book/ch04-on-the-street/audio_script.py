# -*- coding: utf-8 -*-
"""Chapter 4 — Op straat.  What gets spoken, by whom, with what delivery.

Text must match content.py word for word; numbers are spelled out as Dutch words
("De 29ste" -> "De negenentwintigste", "16.00 uur" -> "zestien uur"). Emotion tags
steer delivery and are not spoken; keep them to a few words.

Bert is the waiter from chapter 3, so he keeps the "ober" voice. Hans is new
(see voices.py).

NOT recorded: Opdracht 9. Like ch2's Opdracht 15 and ch3's Opdracht 12, it plays
e / ee words the book never prints. Opdracht 10 prints its words and is recorded.

Generate:  python3 book/generate_audio.py ch04-on-the-street
"""

ITEMS = [
 {"id": "dialoog", "gap": 0.45, "kind": "dialogue", "label": "Bert en Hans op straat",
  "lines": [
   ("ober", "[surprised, delighted] Hé Hans, hallo!"),
   ("hans", "[delighted] Hé Bert, hoi. Dat is lang geleden, zeg. Wat leuk! Alles goed?"),
   ("ober", "[cheerful] Ja, prima. En met jou, hoe is het met jou?"),
   ("hans", "[shrugging, then brightening] Het gaat wel. Ik heb problemen met de buren, maar "
            "dat is nu niet zo belangrijk. Ik heb vakantie en Wilma en ik gaan deze week een "
            "paar dagen naar Venetië."),
   ("ober", "[impressed] Wauw! Venetië is prachtig. Ga je veel foto’s maken?"),
   ("hans", "Nee, we hebben sinds gisteren een nieuwe camera, dus we gaan een romantische "
            "film maken. Kom je na de vakantie naar de film kijken?"),
   ("ober", "[keen] Ja, leuk. Zullen we direct iets afspreken?"),
   ("hans", "Goed. We zijn op vrijdag weer thuis. Zullen we voor zaterdag een afspraak maken?"),
   ("ober", "Welke datum is het dan?"),
   ("hans", "De negenentwintigste."),
   ("ober", "[apologetic] Nee, dat lukt niet. Dan heb ik al een afspraak. "
            "Zondag dertig augustus kan ik wel."),
   ("hans", "[easy-going] Dat kan ook. Zullen we om zestien uur bij ons thuis afspreken? "
            "Blijf je ook eten? Zal ik dan spaghetti carbonara maken?"),
   ("ober", "[enthusiastic] Ja, lekker. Goed plan. Ik schrijf het straks in mijn agenda. "
            "Hartstikke leuk."),
   ("hans", "Ja, vind ik ook."),
   ("ober", "[in a hurry] Ik moet ervandoor. Ik moet nog gauw even naar de winkel. Ik wens "
            "jullie een fijne vakantie. Doe de groeten aan Wilma en tot volgende week zondag."),
   ("hans", "[warmly] Doe ik. Tot dan. Doeg."),
  ]},

 {"id": "opdracht10", "kind": "speech", "voice": "docent", "label": "Opdracht 10 — e / ee",
  "text": "[slowly, pausing] "
          "wel. verder. hebben. lekker. hetzelfde. moment. wensen. prettig. tekst. vertellen. "
          "week. heeft. idee. probleem. deze. geven. tegen. uitstekend. nemen. "
          "hetzelfde. nemen. probleem. deze. tegen. wel. verder. idee. prettig. hebben."},
]

# -*- coding: utf-8 -*-
"""Chapter 3 — In het café.  What gets spoken, by whom, with what delivery.

Text must match content.py word for word. Emotion tags steer delivery and are
not spoken. Susy and Edit keep their voices from chapters 1-2; Andres and the
ober are new to this chapter (see voices.py).

NOT recorded: Opdracht 12. Like ch2's Opdracht 15, it plays word pairs the book
never prints, so there is nothing to transcribe. Opdrachten 11 and 13 do print
their words and are recorded.

Generate:  python3 book/generate_audio.py ch03-in-the-cafe
"""

ITEMS = [
 {"id": "dialoog", "kind": "dialogue", "label": "Edit viert haar verjaardag",
  "lines": [
   ("susy",   "[warmly, celebrating] Hoi Edit. Gefeliciteerd met je verjaardag."),
   ("edit",   "[pleased] Dank je wel. Dit is mijn broer Andres."),
   ("susy",   "[friendly, introducing herself] Dag, ik ben Susy. Prettig met je kennis te maken."),
   ("andres", "[easy, curious] Hoi. Hoe kennen jullie elkaar eigenlijk?"),
   ("susy",   "Van de cursus Nederlands."),
   ("edit",   "[generous] Wat willen jullie drinken? Ik trakteer."),
   ("andres", "Ik wil graag cola."),
   ("susy",   "Doe mij maar een biertje."),
   ("edit",   "Ik neem rode wijn. Ik roep de ober. [calling out politely] Mag ik bestellen?"),
   ("ober",   "[professional, obliging] Zegt u het maar."),
   ("edit",   "Een cola, een rode wijn en een biertje alstublieft."),
   ("ober",   "[helpful] Een Franse, Spaanse of Zuid-Afrikaanse wijn?"),
   ("edit",   "[hesitating, then deciding] Hm, ik weet het niet. Doe de Spaanse maar."),
   ("susy",   "[raising a glass, cheerful] Nou, Edit. Proost. Op je verjaardag!"),
   ("edit",   "[touched] Bedankt."),
   ("edit",   "[after a pause, brightly] Zullen we nog een keer bestellen?"),
   ("andres", "[approving] Dat is een goed idee."),
   ("edit",   "Willen jullie hetzelfde?"),
   ("susy",   "[happily] Ja, graag."),
   ("andres", "[insisting good-naturedly] Nu wil ik ook een biertje. Dit rondje betaal ik. "
              "Wat wil jij, Edit?"),
   ("edit",   "Geef mij nog maar een glas rode wijn."),
   ("edit",   "[later, catching the waiter] Ober, mogen we afrekenen?"),
   ("ober",   "Alles samen?"),
   ("edit",   "[explaining] Nee, ik ben jarig, daarom betaal ik het eerste rondje. "
              "Het tweede rondje betaalt hij."),
  ]},

 {"id": "opdracht11", "kind": "speech", "voice": "docent", "label": "Opdracht 11 — woordaccent",
  "text": "[clearly, pausing after each word, stressing the accented syllable strongly] "
          "voornaam. docent. Nederlands. adres. pauze. familie. "
          "vandaag. minuut. februari. moment. vakantie. gezin. "
          "verjaardag. rondje. bestellen. afrekenen. gefeliciteerd. bladzijde."},

 {"id": "opdracht13", "kind": "speech", "voice": "docent", "label": "Opdracht 13 — o / oo",
  "text": "[clearly and slowly, leaving a pause after every word, contrasting the short and long o] "
          "blond. donderdag. donker. welkom. stoppen. jong. koffie. kopje. morgen. nog. "
          "hoor. voor. ook. woon. voorjaar. zomer. docent. komen. zo. wonen. "
          "blond. ook. donker. docent. koffie. kopje. zomer. woon. wonen. stoppen."},
]

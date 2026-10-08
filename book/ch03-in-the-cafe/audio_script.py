# -*- coding: utf-8 -*-
"""Chapter 3 — In het café.  What gets spoken, by whom, with what delivery.

Text must match content.py word for word. Emotion tags steer delivery and are
not spoken. Susy and Edit keep their voices from chapters 1-2; Andres and the
ober are new to this chapter (see voices.py).

NOT recorded: Opdracht 12. Like ch2's Opdracht 15, it plays word pairs the book
never prints, so there is nothing to transcribe. Opdrachten 11 and 13 do print
their words and are recorded.

All three items stay on the default eleven_v3. eleven_v4 was tried here the way
it was tried on chapter 1 — three takes per item, each transcribed back — and it
won nothing: it swallowed "pauze" in Opdracht 11 in 3 of 3 takes (reading the
word as a direction to pause), and in 1 of 3 takes of Opdracht 13 it repeated a
run of six words and cleared its throat. On the dialogue it matched v3 for
accuracy but came out ~1.5 dB duller above 8 kHz and 30 % faster, which is the
wrong direction for a chapter learners listen to. Don't re-pin v4 without
re-measuring.

Tags here are capped at a few words. A long one gets voiced: ch2's Opdracht 16
carried a fifteen-word tag and every take opened with an English fragment from its
tail, swallowing the first Dutch word. These items were NOT re-recorded when the
tags were shortened — their current takes verify clean, and re-rolling a good take
of a word list is a bad bet. The shorter tag applies the next time they are
generated.

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
  "text": "[stressing each accent] "
          "voornaam. docent. Nederlands. adres. pauze. familie. "
          "vandaag. minuut. februari. moment. vakantie. gezin. "
          "verjaardag. rondje. bestellen. afrekenen. gefeliciteerd. bladzijde."},

 {"id": "opdracht13", "kind": "speech", "voice": "docent", "label": "Opdracht 13 — o / oo",
  "text": "[slowly, pausing] "
          "blond. donderdag. donker. welkom. stoppen. jong. koffie. kopje. morgen. nog. "
          "hoor. voor. ook. woon. voorjaar. zomer. docent. komen. zo. wonen. "
          "blond. ook. donker. docent. koffie. kopje. zomer. woon. wonen. stoppen."},
]

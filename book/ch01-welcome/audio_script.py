# -*- coding: utf-8 -*-
"""Chapter 1 — Welkom.  What gets spoken, by whom, with what delivery.

One entry per audio icon in pages.py. Text must match content.py word for word —
this is the book being read aloud, not a paraphrase.

Emotion tags in [brackets] steer delivery and are not spoken. Chosen to fit the
moment: the teacher opens warmly, Ning corrects a misheard house number, the
teacher waves away the formal "u". In the zinsaccent drill every answer carries a
contrastive correction, so the answers are tagged emphatic — that stress pattern
is the entire point of the exercise.

Generate:  python3 book/generate_audio.py ch01-welcome
"""

ITEMS = [
 # ---------------------------------------------------------------- 1.1 Dialoog
 {"id": "dialoog", "kind": "dialogue", "label": "De cursus begint",
  "lines": [
   ("docent", "[warmly] Goedemorgen allemaal. Welkom in de cursus Nederlands."),
   ("docent", "[friendly] Ik ben Karin Dijkstra en ik ben jullie docent. "
              "Jullie hebben twee docenten. De andere docent is Paul de Vries. "
              "Hij geeft twee dagen les en ik drie."),
   ("docent", "[encouraging] We beginnen met kennismaken. Wie ben jij? Wat is jouw naam?"),
   ("susy",   "[friendly] Ik ben Susy. Mijn naam is Susy."),
   ("docent", "[warmly] Dag Susy. Susy is je voornaam. En wat is je achternaam?"),
   ("susy",   "Mijn achternaam is Wall."),
   ("docent", "[curious] Uit welk land kom je?"),
   ("susy",   "Ik kom uit Engeland."),
   ("docent", "[turning to someone else] De buurman van Susy: Wie ben jij? Hoe heet jij?"),
   ("ning",   "[politely] Ik heet Ning."),
   ("docent", "[warmly] Dag Ning. En waar kom je vandaan?"),
   ("ning",   "Ik kom uit China."),
   ("docent", "Waar woon je?"),
   ("ning",   "Ik woon nu in Utrecht."),
   ("docent", "Wat is je adres?"),
   ("ning",   "Mijn adres is Hofstraat tweeëntwintig."),
   ("docent", "[checking] Op welk nummer? Wat is je antwoord? Drieëntwintig?"),
   ("ning",   "[correcting politely] Nee, op tweeëntwintig. "
              "En mijn postcode is drieëndertig eenentachtig T W in Utrecht."),
   ("ning",   "[politely] En u, mevrouw? Woont u ook in Utrecht?"),
   ("docent", "[laughs softly] Zeg maar jij, hoor. Ja, ik woon hier al twintig jaar."),
   ("docent", "[briskly] Oké, we gaan verder met de les. Heeft iedereen het boek? "
              "We beginnen met tekst één op bladzijde acht. "
              "We gaan naar de tekst luisteren. We gaan de tekst ook lezen."),
   ("docent", "[brightly] We stoppen even, het is pauze. Tot straks."),
  ]},

 # ---------------------------------------------------------------- 1.5 Telwoorden
 {"id": "telwoorden", "kind": "speech", "voice": "docent", "label": "Telwoorden",
  "text": "[clearly, slowly, leaving a pause after each number] "
          "nul. één. twee. drie. vier. vijf. zes. zeven. acht. negen. tien. "
          "elf. twaalf. dertien. veertien. vijftien. zestien. zeventien. achttien. negentien. twintig. "
          "eenentwintig. tweeëntwintig. "
          "dertig. veertig. vijftig. zestig. zeventig. tachtig. negentig. honderd. "
          "honderdvierentwintig. duizend."},

 # ---------------------------------------------------------------- 1.6 Het alfabet
 {"id": "alfabet", "kind": "speech", "voice": "docent", "label": "Het alfabet",
  "text": "[clearly, slowly, pausing between each letter, as a teacher reciting the alphabet] "
          "a. b. c. d. e. f. g. h. i. j. k. l. m. "
          "n. o. p. q. r. s. t. u. v. w. x. y. z. "
          "[explaining] ij, de lange ij. ei, de korte ei. y, de Griekse ij."},

 # ---------------------------------------------------------------- Opdracht 12
 {"id": "zinsaccent", "kind": "dialogue", "label": "Opdracht 12 — Zinsaccent",
  "lines": [
   ("vraag",    "[asking] Kom je uit Nederland?"),
   ("antwoord", "[emphatic correction] Nee, ik kom uit Hongarije."),
   ("vraag",    "[asking] Heet je buurman Peter?"),
   ("antwoord", "[emphatic correction] Nee, mijn docent heet Peter."),
   ("vraag",    "[asking] Woon je in de Hofstraat?"),
   ("antwoord", "[emphatic correction] Nee, ik woon in de Kerkstraat."),
   ("vraag",    "[asking] Woon je in Groningen?"),
   ("antwoord", "[emphatic correction] Nee, ik woon in Leeuwarden."),
   ("vraag",    "[asking] Woont u hier al twintig jaar?"),
   ("antwoord", "[emphatic correction] Nee, ik woon hier al dertig jaar."),
   ("vraag",    "[asking] Is je postcode drieëndertig eenentachtig T B?"),
   ("antwoord", "[emphatic correction] Nee, mijn postcode is drieëndertig eenentachtig T W."),
   ("vraag",    "[asking] Ben jij Lily Lander?"),
   ("antwoord", "[emphatic correction] Nee, ik ben Sara Lander."),
   ("vraag",    "[asking] Beginnen we met tekst twee?"),
   ("antwoord", "[emphatic correction] Nee, we beginnen met tekst één."),
   ("vraag",    "[asking] Is Abdul je voornaam?"),
   ("antwoord", "[emphatic correction] Nee, Abdul is mijn achternaam."),
   ("vraag",    "[asking] Is het pauze?"),
   ("antwoord", "[confirming, relieved] Ja, het is pauze."),
  ]},
]

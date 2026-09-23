# -*- coding: utf-8 -*-
"""Chapter 3 — In het café.  All of the chapter's text.

Transcribed from Nederlands in gang (Coutinho, 3rd revised edition 2017), pp. 46-57.
The values stay Dutch on purpose — this is the book's content, not structure.
"""

OBJECTIVES = [
 "bestellen en afrekenen", "bedanken", "rangtelwoorden", "artikel", "diminutief",
 "structuur van hoofdzin met inversie", "uitspraak: woordaccent en o – oo",
]

# ---------------------------------------------------------------- 3.1 Dialoog
DIALOOG_INTRO = "Edit viert haar verjaardag in het café, samen met haar broer Andres en Susy."
DIALOOG = [
 ("Susy",   "Hoi Edit. Gefeliciteerd met je verjaardag."),
 ("Edit",   "Dank je wel. Dit is mijn broer Andres."),
 ("Susy",   "Dag, ik ben Susy. Prettig met je kennis te maken."),
 ("Andres", "Hoi. Hoe kennen jullie elkaar eigenlijk?"),
 ("Susy",   "Van de cursus Nederlands."),
 ("Edit",   "Wat willen jullie drinken? Ik trakteer."),
 ("Andres", "Ik wil graag cola."),
 ("Susy",   "Doe mij maar een biertje."),
 ("Edit",   "Ik neem rode wijn. Ik roep de ober.<br>Mag ik bestellen?"),
 ("Ober",   "Zegt u het maar."),
 ("Edit",   "Een cola, een rode wijn en een biertje alstublieft."),
 ("Ober",   "Een Franse, Spaanse of Zuid-Afrikaanse wijn?"),
 ("Edit",   "Hm, ik weet het niet. Doe de Spaanse maar."),
 ("Susy en Andres", "Nou, Edit. Proost. Op je verjaardag!"),
 ("Edit",   "Bedankt."),
]
DIALOOG_2 = [
 ("Edit",   "Zullen we nog een keer bestellen?"),
 ("Andres", "Dat is een goed idee."),
 ("Edit",   "Willen jullie hetzelfde?"),
 ("Susy",   "Ja, graag."),
 ("Andres", "Nu wil ik ook een biertje. Dit rondje betaal ik. Wat wil jij, Edit?"),
 ("Edit",   "Geef mij nog maar een glas rode wijn."),
]
DIALOOG_3 = [
 ("Edit",  "Ober, mogen we afrekenen?"),
 ("Ober",  "Alles samen?"),
 ("Edit",  "Nee, ik ben jarig, daarom betaal ik het eerste rondje.<br>"
           "Het tweede rondje betaalt hij."),
]

# ---------------------------------------------------------------- 3.2 Woordenlijst
VOC = [
 ("viert <small>(vieren)</small>","is celebrating"),("de verjaardag","birthday"),
 ("het café","café / pub"),("samen","together"),("gefeliciteerd","happy birthday"),
 ("dank je wel","thank you"),("dit is","this is"),
 ("prettig met je<br>&nbsp;&nbsp;kennis te maken<br>&nbsp;&nbsp;<small>(kennismaken)</small>",
  "pleased to meet you"),
 ("kennen <small>(kennen)</small>","know (people)"),("elkaar","one another"),
 ("drinken","drink"),("ik trakteer <small>(trakteren)</small>","it’s my treat"),
 ("wil graag <small>(graag willen)</small>","would like"),("de cola","cola"),
 ("biertje <small>(het bier)</small>","beer"),("neem <small>(nemen)</small>","have (take)"),
 ("rode <small>(rood)</small>","red"),("de wijn","wine"),
 ("roep <small>(roepen)</small>","call"),("de ober","waiter"),
 ("mag <small>(mogen)</small>","may"),("bestellen","order"),("alstublieft","please"),
 ("Franse <small>(Frans)</small>","French"),
 ("Spaanse <small>(Spaans)</small>","Spanish"),
 ("Zuid-Afrikaanse<br>&nbsp;&nbsp;<small>(Zuid-Afrikaans)</small>","South African"),
 ("de","the"),("nou","well then"),("proost","cheers"),
 ("op je verjaardag","happy birthday"),("bedankt","thanks"),
 ("het poosje","short while"),("later <small>(laat)</small>","later"),
 ("zullen <small>(zullen)</small>","shall"),("nog een keer","once more"),
 ("dat is","that is"),("goed","good"),("het idee","idea"),("hetzelfde","the same"),
 ("ja, graag","yes please"),("dit","this"),("het rondje","round"),
 ("betaal <small>(betalen)</small>","pay"),("geef <small>(geven)</small>","give"),
 ("nog maar","another"),("het glas","glass"),("afrekenen","pay / settle the bill"),
 ("alles","everything"),("daarom","that’s why"),("eerste","first"),("tweede","second"),
]

OPD1 = [
 ("Edit, Andres en Susy zijn", "in een café.", "in de les."),
 ("Andres is", "de zus van Edit.", "de broer van Edit."),
 ("Edit en Susy kennen elkaar", "van de cursus.", "van het werk."),
 ("Edit is jarig en zij geeft", "een rondje.", "een glas wijn."),
 ("Andres betaalt", "alles.", "het tweede rondje."),
]

# ---------------------------------------------------------------- 3.3 / 3.4 / 3.5
BESTELLEN = ["Mag ik een biertje?","Ik wil graag een biertje.",
             "Een biertje, alstublieft.","Voor mij een biertje."]
AFREKENEN = ["Mag ik de rekening (alstublieft)?","Ik wil graag afrekenen / betalen.",
             "Mogen / Kunnen we betalen / afrekenen?"]
BEDANKEN  = ["dank je / dank je wel / dank u (wel)","bedankt"]

# ---------------------------------------------------------------- Opdracht 4
OPD4_INTRO = "Henk, Raiza en Ella zijn in een café. Ze gaan samen iets drinken."
OPD4 = [
 ("Henk",  "Wat willen jullie ___?"),
 ("Raiza", "Ik neem ___."),
 ("Henk",  "En jij, Ella? Wat ___?"),
 ("Ella",  "O, ik ___ het niet. Ik neem ook wijn. Of koffie? Ja, ik ___ koffie."),
 ("Raiza", "Daar is de ober. Meneer! Kunnen wij ___?"),
 ("Ober",  "Ja, zegt u het maar."),
 ("Henk",  "Een biertje, een ___ en ___."),
 ("Ober",  "Prima."),
 ("", ""),
 ("Ober",  "Voor ___ is de koffie?"),
 ("Ella",  "Voor mij. Dank ___."),
 ("", ""),
 ("Raiza", "Hoe laat is het?"),
 ("Henk",  "___."),
 ("Raiza", "O, ik moet weg. Ik heb een afspraak om ___.<br>Zullen we ___?"),
 ("Ella",  "Ik betaal ___."),
 ("Raiza", "___.<br>Tot ziens!"),
 ("Henk",  "___."),
]

# ---------------------------------------------------------------- 3.6 Artikel
ARTIKEL_EX = ["Welkom in <b>de</b> cursus Nederlands.","Ik roep <b>de</b> ober.",
 "Edit viert haar verjaardag in <b>het</b> café.",
 "Nee, ik ben jarig, daarom betaal ik <b>het</b> eerste rondje.",
 "Doe mij maar <b>een</b> biertje.","Zullen we nog een keer bestellen?",
 "Ik wil graag cola.","Ik neem rode wijn."]
ARTIKEL = [("de-woord","de cursus","een cursus"),
           ("het-woord","het café","een café"),
           ("diminutief","het rondje","een rondje"),
           ("pluralis","de cursussen<br>de cafés<br>de rondjes","cursussen<br>cafés<br>rondjes")]
DIMINUTIEF = ["het rond<b>je</b>","het zus<b>je</b>","het kop<b>je</b>"]
OPD5 = [["adres","broer","café","cursus","rondje","foto"],
        ["gezin","haar","zomer","kantine","koffie","biertje"],
        ["zus","seizoen","maand","land","pauze","tekst"]]

# ---------------------------------------------------------------- 3.7 Inversie
INVERSIE = [("Nu","wil","ik","ook een biertje."),
            ("Dit rondje","betaal","ik","")]
# The book prints the element to be fronted in blue. The scan is pure greyscale,
# so that colour is gone; each fronted phrase below is the only one that yields a
# grammatical inversion. See NOTES.md.
OPD6 = [
 ("Joyce is", "donderdag", "jarig."),
 ("We drinken koffie", "in de kantine", ""),
 ("Ze zijn", "op het moment", "in Indonesië."),
 ("Ik weet", "dat", "niet."),
 ("Ze wonen", "in de winter", "in Barcelona."),
 ("We gaan", "na de pauze", "verder."),
 ("Ik heb", "Susy’s adres", "niet."),
 ("We spreken", "later", "over de tekst."),
 ("Ik neem", "nu", "ook wijn."),
 ("Eddy geeft", "vandaag", "les."),
 ("We beginnen", "morgen", "met tekst 3."),
 ("De tekst begint", "op bladzijde 2", ""),
]

# ---------------------------------------------------------------- 3.8 Rangtelwoorden
RANG_A = [("1e","eerste"),("2e","tweede"),("3e","derde"),("4e","vierde"),("5e","vijfde"),
          ("6e","zesde"),("7e","zevende"),("8e","achtste"),("9e","negende"),("10e","tiende")]
RANG_B = [("11e","elfde"),("12e","twaalfde"),("13e","dertiende"),("14e","veertiende"),
          ("15e","vijftiende"),("16e","zestiende"),("17e","zeventiende"),
          ("18e","achttiende"),("19e","negentiende"),("20e","twintigste")]
RANG_C = [("21e","eenentwintigste"),("100e","honderdste")]

OPD7 = ["Welke dag van de week is maandag?","Welke maand van het jaar is juli?",
 "Welke letter van het alfabet is de d?","Op welke dag ben jij jarig?",
 "Welke dag is het nu?",
 "Hoeveel kinderen heeft jullie gezin? Het hoeveelste kind ben jij?",
 "De hoeveelste les is dit?"]

# Opdracht 8 — word cloud. (word, relative size)
WOORDWOLK = [("gefeliciteerd",34),("proost",30),("drinken",28),("afrekenen",26),
 ("verjaardag",26),("café",26),("cola",24),("bier",24),("wijn",22),("bestellen",20),
 ("cursus",18),("ober",18),("kennen",16),("trakteer",16),("hetzelfde",14),("rondje",12)]

OPD9_MAIL = ("Hoi,<br>Volgende week woensdag 9 mei ben ik jarig en dan word ik 20! "
 "Ik wil dit graag met jullie vieren.<br>Kom je ook naar café De Dromer vanaf 21.00 uur?<br>"
 "Benedetta")

# ---------------------------------------------------------------- 3.9 Tekst
TEKST = ("Bij goed weer kun je op dit terras zitten. Je drinkt dan buiten een lekker kopje "
         "koffie, een biertje of cola. In de zomer kijk je naar de boten in het water.")

# ---------------------------------------------------------------- 3.10 Uitspraak
OPD11 = [["voornaam","docent","Nederlands","adres","pauze","familie"],
         ["vandaag","minuut","februari","moment","vakantie","gezin"],
         ["verjaardag","rondje","bestellen","afrekenen","gefeliciteerd","bladzijde"]]
OPD13 = [
 ["blond","donderdag","donker","welkom","stoppen","jong","koffie","kopje","morgen","nog"],
 ["hoor","voor","ook","woon","voorjaar","zomer","docent","komen","zo","wonen"],
 ["blond","ook","donker","docent","koffie","kopje","zomer","woon","wonen","stoppen"],
]

# ---------------------------------------------------------------- closers
CULTUUR_VRAAG = "Hoe vier jij je verjaardag?"
CULTUUR = ["Ik vier mijn verjaardag thuis / in een café / niet / …",
 "Mijn familie / vrienden / collega’s / buren / … komen op mijn verjaardag.",
 "Ik trakteer op taart / op … / niet."]
PRAKTIJK = "Ga je naar een café of restaurant? Bestel dan iets in het Nederlands."

REFLECTIE = [
 "Can you now understand the dialogue at the start of this chapter?",
 "Can you congratulate someone?",
 "Can you order something in a café?",
 "Can you read a drinks menu?",
 "Can you settle the bill in a café?",
 "Can you thank someone?",
 "Can you reply to an invitation to a party?",
]
VERDIEPING = ["grammar and pronunciation videos","a gap-fill of the dialogue",
 "extra exercises","an intensive listening text","a Dutch song with an exercise"]

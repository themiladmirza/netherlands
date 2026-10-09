# -*- coding: utf-8 -*-
"""Chapter 4 — Op straat.  All of the chapter's text.

Keep text separate from layout: pages.py only decides the arrangement.
Transcribed from Nederlands in gang (Coutinho, 3rd revised edition 2017), pp. 58-67.
Values stay Dutch — that is the book's content.
"""

OBJECTIVES = [
 "vragen en vertellen hoe het gaat", "een afspraak maken", "een voorstel doen",
 "positief / negatief reageren", "zullen", "uitspraak: e – ee",
]

# ---------------------------------------------------------------- 4.1 Dialoog
DIALOOG_INTRO = "De ober, Bert, komt op straat zijn vriend Hans tegen."
DIALOOG = [
 ("Bert", "Hé Hans, hallo!"),
 ("Hans", "Hé Bert, hoi. Dat is lang geleden, zeg. Wat leuk! Alles goed?"),
 ("Bert", "Ja, prima. En met jou, hoe is het met jou?"),
 ("Hans", "Het gaat wel. Ik heb problemen met de buren, maar dat is nu niet zo "
          "belangrijk. Ik heb vakantie en Wilma en ik gaan deze week een paar dagen "
          "naar Venetië."),
 ("Bert", "Wauw! Venetië is prachtig. Ga je veel foto’s maken?"),
 ("Hans", "Nee, we hebben sinds gisteren een nieuwe camera, dus we gaan een "
          "romantische film maken. Kom je na de vakantie naar de film kijken?"),
 ("Bert", "Ja, leuk. Zullen we direct iets afspreken?"),
 ("Hans", "Goed. We zijn op vrijdag weer thuis. Zullen we voor zaterdag een afspraak maken?"),
 ("Bert", "Welke datum is het dan?"),
 ("Hans", "De 29ste."),
 ("Bert", "Nee, dat lukt niet. Dan heb ik al een afspraak. Zondag 30 augustus kan ik wel."),
 ("Hans", "Dat kan ook. Zullen we om 16.00 uur bij ons thuis afspreken? Blijf je "
          "ook eten? Zal ik dan spaghetti carbonara maken?"),
 ("Bert", "Ja, lekker. Goed plan. Ik schrijf het straks in mijn agenda. Hartstikke leuk."),
 ("Hans", "Ja, vind ik ook."),
 ("Bert", "Ik moet ervandoor. Ik moet nog gauw even naar de winkel. Ik wens jullie "
          "een fijne vakantie. Doe de groeten aan Wilma en tot volgende week zondag."),
 ("Hans", "Doe ik. Tot dan. Doeg."),
]

# ---------------------------------------------------------------- 4.2 Woordenlijst
# In the book's reading order: down the first column, then down the second, on
# each of the two pages.
VOC = [
 ("de straat","street"),("vriend","friend"),
 ("komt tegen <small>(tegenkomen)</small>","meets"),("hé","hey"),("geleden","ago"),
 ("leuk","nice"),("prima","wonderful"),
 ("jou","you"),("het gaat wel","all right"),
 ("problemen <small>(het probleem)</small>","problems"),("buren","neighbours"),
 ("niet zo","not so"),("belangrijk","important"),("gaan <small>(gaan)</small>","go"),
 ("de week","week"),("een paar dagen <small>(dag)</small>","a few days"),
 ("Venetië","Venice"),("wauw","wow"),("prachtig","fine / splendid"),("veel","many"),
 ("foto’s maken","take photos"),("sinds","since"),("nieuw","new"),("de camera","camera"),
 ("romantische <small>(romantisch)</small>","romantic"),("de film","film"),("na","after"),
 ("kijken naar","look at"),("direct","right now"),("iets","something"),
 ("afspreken","set a date / make an appointment"),("goed","okay"),("thuis","at home"),
 ("de afspraak","date / appointment"),("maken","to make"),("de datum","date"),
 ("dat lukt niet <small>(lukken)</small>","that doesn’t work"),
 ("dan","then"),("kan <small>(kunnen)</small>","can"),("blijf <small>(blijven)</small>","stay"),
 ("eten","eat"),("zal <small>(zullen)</small>","will / shall"),
 ("de spaghetti carbonara","spaghetti carbonara"),("het plan","plan"),
 ("schrijf <small>(schrijven)</small>","write"),("de agenda","diary"),
 ("hartstikke","very / completely"),("hartstikke leuk","terrific / fantastic"),
 ("vind ik ook <small>(vinden)</small>","I think so too"),("ik moet ervandoor","I have to go"),
 ("ervandoor","away / off"),("gauw","quickly"),("de winkel","shop"),
 ("wens <small>(wensen)</small>","wish"),("jullie","you"),("fijne <small>(fijn)</small>","nice / good"),
 ("doe de groeten aan <small>(de groeten doen aan)</small>","give my regards to"),
 ("volgende","next"),("tot dan","until then"),
]

OPD1 = [
 "Bert en Hans hebben elkaar lang niet gezien.",
 "Hans en Wilma gaan in Venetië wonen.",
 "Hans gaat een film maken in de vakantie.",
 "Hans en Bert maken een afspraak om samen te eten.",
 "Hans en Wilma komen 30 augustus bij Bert eten.",
]

# ---------------------------------------------------------------- 4.3 Hoe het gaat
VRAGEN = ["Alles goed?", "Hoe gaat het (met jou / met u)?", "Hoe is het (met jou / met u)?"]
VERTELLEN = [("++","prima"),("++","fantastisch"),("++","uitstekend"),("++","heel goed"),
             ("++","hartstikke goed"),("+","goed"),("+–","het gaat wel"),
             ("+–","niet zo (goed)"),("–","niet goed"),("–","slecht")]
OPD2_EX = [("A","Hoe gaat het?"),("B","Het gaat wel. Hoe is het met jou?"),("A","Heel goed."),
           ("A","Alles goed?"),("C","Prima. En met jou?"),("A","Niet zo.")]

# ---------------------------------------------------------------- 4.4 Zullen (1)
ZULLEN = ["Zullen we iets afspreken?", "Zullen we voor zaterdag een afspraak maken?",
          "Zullen we om 16.00 uur bij ons thuis afspreken?",
          "Zal ik dan spaghetti carbonara maken?"]
OPD3_EX = ("Ik wil iets drinken.", "cola bestellen", "Zullen we cola bestellen?")
OPD3 = [
 ("Ik wil op vakantie!", "een paar dagen naar Parijs gaan"),
 ("Dit is een leuk café!", "hier iets drinken"),
 ("Waar zijn Bart en Astrid?", "in de kantine kijken"),
 ("Ik wil afrekenen.", "de ober roepen"),
 ("Wat zeg je? Wat is je naam?", "mijn naam spellen"),
 ("Hé Hans, lang niet gezien!", "een afspraak maken"),
 ("Wat eten we?", "spaghetti maken"),
 ("Edit is jarig.", "een boek geven"),
]

# ---------------------------------------------------------------- 4.5 Afspraak maken
AFSPRAAK = ["Zullen we voor zaterdag een afspraak maken?", "Zullen we iets afspreken?"]
REAGEREN_1 = [("+","Ja, dat kan."),("+","Ja, dat is goed."),("–","Nee, dat lukt niet."),
              ("–","Nee, ik heb al een afspraak."),("–","Nee, dan kan ik niet.")]
OPD4 = [
 "Zal ik spaghetti carbonara maken? (reageer positief)",
 "Zullen we voor zaterdag een afspraak maken? (reageer negatief)",
 "Ga je mee iets drinken? (positief)",
 "Heb je zin om naar de bioscoop te gaan? (negatief)",
 "Zullen we naar de buren gaan? (positief)",
 "Ga je mee naar de kantine? (positief)",
 "Zal ik nog een keer bestellen? (negatief)",
 "Heb je zin om foto’s van mijn familie te zien? (positief)",
]

# ---------------------------------------------------------------- 4.6 Samen iets doen
SAMEN = ["Ga je mee (naar) …?", "Heb je zin om …?"]
REAGEREN_2 = [("+","Ja, leuk."),("+","Ja, goed idee."),("–","Nee, ik kan niet."),
              ("–","Nee, dat vind ik niet zo leuk."),("–","Nee, ik heb geen zin.")]
OPD5 = ["een voorstel doen (Zullen we …?)", "negatief reageren",
        "een ander voorstel doen", "positief reageren"]
OPD6 = [
 "Kun je om 16.00 uur komen? Ja, ___ kan.",
 "Ik moet ervandoor. ___ de groeten aan je ouders.",
 "Kun je woensdag de 8ste? Nee, ___ kan ik niet.",
 "Ik ga naar het café. Gaat Susy ___ naar het café?",
 "Alles goed? Ja, prima. En ___ jou?",
]
OPD7_EX = "Donderdag 21.00 Susy, café De Lente."

# ---------------------------------------------------------------- 4.7 Tekst
TEKST = ("Voor informatie over de diensten van het Talencentrum van de Rijksuniversiteit "
         "Groningen kunt u onze website bezoeken: www.rug.nl/talencentrum.<br>"
         "Hebt u vragen die niet beantwoord zijn na het raadplegen van onze website, dan "
         "doen wij ons best uw e-mail zo spoedig mogelijk te beantwoorden.")
TEKST_GROET = "Met vriendelijke groet,<br><br>Het secretariaat"
TEKST_ADRES = ("Secretariaat Talencentrum, Rijksuniversiteit Groningen<br>"
               "Harmoniecomplex, kamer (13)15.0129<br>Oude Kijk in ’t Jatstraat 26<br>"
               "Postbus 716<br>9700 AS Groningen")
TEKST_TIJDEN = ("Openingstijden van het secretariaat: maandag t/m vrijdag 12.00-16.00 uur, "
                "donderdag 12.00-20.00 uur.<br>Het secretariaat is op werkdagen van 9.00 tot "
                "17.00 uur telefonisch bereikbaar, tel. 050-3635802.")

# ---------------------------------------------------------------- 4.8 Uitspraak
OPD10 = [
 ["wel","verder","hebben","lekker","hetzelfde","moment","wensen","prettig","tekst","vertellen"],
 ["week","heeft","idee","probleem","deze","geven","tegen","uitstekend","nemen"],
 ["hetzelfde","nemen","probleem","deze","tegen","wel","verder","idee","prettig","hebben"],
]

# ---------------------------------------------------------------- closers
CULTUUR_VRAAG = "Voor welke activiteiten maak je een afspraak?"
CULTUUR_ROWS = ["naar een café gaan met een vriend", "koffiedrinken met een collega",
                "eten bij vrienden / familie / …", "je verjaardag vieren"]
PRAKTIJK = "Doe een voorstel aan iemand. Gebruik <b>Zullen we … / Zal ik …?</b>"

REFLECTIE = [
 "Can you now understand the dialogue at the start of this chapter?",
 "Can you ask how someone is?",
 "Can you say how you are?",
 "Can you make an appointment?",
 "Can you ask someone to do something together?",
 "Can you respond to a suggestion?",
 "Can you read an informative text?",
]
VERDIEPING = ["grammar and pronunciation videos", "a gap-fill of the dialogue",
              "extra exercises", "an intensive listening text"]

"""Danish phrasebook with practical learner-facing expressions."""
from app.data._types import PhrasebookCategory,PhrasebookEntry
_DATA=[
("da-greetings-a1","A1","Hilsner","👋",[("Hej!","Når du møder nogen.","neutral"),("Godmorgen!","Om morgenen.","neutral"),("Hvordan har du det?","Når du spørger til en persons velbefindende.","neutral")]),
("da-intro-a1","A1","Præsentation","🧑",[("Jeg hedder ...","Når du fortæller dit navn.","neutral"),("Jeg kommer fra ...","Når du fortæller hvor du kommer fra.","neutral"),("Rart at møde dig.","Ved en første introduktion.","neutral")]),
("da-shopping-a2","A2","Indkøb","🛒",[("Hvad koster det?","Når du spørger om prisen.","neutral"),("Jeg vil gerne købe den.","Når du vil købe noget.","neutral"),("Kan jeg betale med kort?","Når du spørger om betalingsmuligheder.","neutral")]),
("da-travel-a2","A2","Rejser","🧳",[("Hvor ligger stationen?","Når du leder efter stationen.","neutral"),("Hvornår går toget?","Når du spørger om afgangstid.","neutral"),("Jeg har en reservation.","Når du ankommer til et reserveret sted.","neutral")]),
("da-health-a2","A2","Sundhed","🩺",[("Jeg har det ikke godt.","Når du føler dig syg.","neutral"),("Jeg har brug for en læge.","Når du søger lægehjælp.","neutral"),("Hvor gør det ondt?","Når du beskriver smerter.","neutral")]),
("da-work-b1","B1","Arbejde","💼",[("Jeg vil gerne drøfte opgaven.","Når du starter en faglig samtale.","neutral"),("Kan vi holde et møde?","Når du foreslår et møde.","neutral"),("Jeg vender tilbage senere.","Når du vil følge op senere.","neutral")]),
("da-opinion-b1","B1","Meninger","💬",[("Efter min mening ...","Når du giver din vurdering.","neutral"),("Jeg er enig.","Når du støtter en andens synspunkt.","neutral"),("Jeg er ikke helt enig.","Når du er delvist uenig.","neutral")]),
("da-debate-b2","B2","Debat","⚖️",[("Jeg vil gerne nuancere pointen.","Når du vil tilføje en præcisering.","formal"),("Det afhænger af situationen.","Når svaret ikke er entydigt.","neutral"),("Lad os se på et andet perspektiv.","Når du vil udvide diskussionen.","neutral")]),
("da-formal-b2","B2","Formel kommunikation","📝",[("Jeg vil gerne understrege, at ...","Når en vigtig pointe skal fremhæves.","formal"),("Tak for Deres henvendelse.","I formel skriftlig kommunikation.","formal"),("Jeg ser frem til Deres svar.","Ved afslutning af en formel besked.","formal")]),
("da-academic-c1","C1","Akademisk samtale","🎓",[("Resultaterne tyder på, at ...","Når du præsenterer en fortolkning.","formal"),("Dette kan forklares med ...","Når du angiver en årsag.","formal"),("Der er behov for yderligere forskning.","Når evidensen ikke er tilstrækkelig.","formal")]),
("da-analysis-c1","C1","Analyse","🔎",[("Det centrale spørgsmål er ...","Når du definerer fokus.","formal"),("En mulig fortolkning er ...","Når du præsenterer en fortolkning.","formal"),("Dette argument kræver nærmere undersøgelse.","Når du vurderer et argument.","formal")]),
("da-rhetoric-c2","C2","Retorik og præcision","🎙️",[("Lad os skelne mellem to begreber.","Når to nært beslægtede begreber skal adskilles.","formal"),("Det er værd at bemærke, at ...","Når du fremhæver en vigtig detalje.","formal"),("Spørgsmålet er snarere, om ...","Når du omformulerer en debat.","formal")]),
("da-social-b1","B1","Sociale situationer","🤝",[("Hvad synes du om det?","Når du spørger om en mening.","neutral"),("Det lyder interessant.","Når du reagerer positivt.","neutral"),("Kan du fortælle lidt mere?","Når du beder om en uddybning.","neutral")]),
("da-problems-b1","B1","Problemer og løsninger","🧩",[("Vi skal finde en løsning.","Når du taler om et problem.","neutral"),("Hvad foreslår du?","Når du beder om et forslag.","neutral"),("Lad os undersøge mulighederne.","Når du vil finde flere løsninger.","neutral")]),
("da-negotiation-b2","B2","Forhandling","🤝",[("Jeg forstår dit synspunkt, men ...","Når du svarer på et modargument.","neutral"),("Kan vi finde et kompromis?","Når du søger en fælles løsning.","neutral"),("Det afhænger af betingelserne.","Når resultatet afhænger af flere forhold.","formal")]),
("da-meetings-b2","B2","Møder","📋",[("Kan vi afklare dette først?","Når du styrer en diskussion.","formal"),("Jeg foreslår, at vi ...","Når du fremsætter et forslag.","formal"),("Lad os opsummere beslutningen.","Når du afslutter et punkt.","formal")]),
("da-research-c1","C1","Forskning","🔬",[("Dataene tyder på, at ...","Når du præsenterer evidens forsigtigt.","formal"),("Der er behov for yderligere undersøgelser.","Når evidensen ikke er tilstrækkelig.","formal"),("Denne fortolkning kræver nærmere analyse.","Når du vurderer en forklaring.","formal")]),
("da-precision-c2","C2","Nuancer og præcision","🎯",[("Det er vigtigt at skelne mellem ...","Når du adskiller to begreber.","formal"),("Denne konklusion bør tages med forbehold.","Når du markerer en begrænsning.","formal"),("Påstanden kan ikke underbygges entydigt.","Når evidensen ikke er afgørende.","formal")])
]
PHRASEBOOK_CATEGORIES=[
 PhrasebookCategory(id=i,level=l,situation=s,icon=icon,phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in phrases])
 for i,l,s,icon,phrases in _DATA
]

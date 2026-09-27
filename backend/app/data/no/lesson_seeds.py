"""Curated Norwegian A2-C2 lesson seeds for JUBA LISAN."""
from __future__ import annotations
from typing import Any

LEVELS = ("A2", "B1", "B2", "C1", "C2")
SKILLS = ("grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review")

TOPICS = {
"A2":[
("1","Reiser og transport","preteritum","Fortell om en reise du har hatt og hvordan du kom deg fram.",["reise","tog","buss","ankomme"]),
("2","Helse og avtaler","modal verbs","Forklar hva du bør gjøre når du trenger hjelp eller en time.",["lege","avtale","symptom","behandle"]),
("3","Arbeid og rutiner","word order","Beskriv en vanlig arbeidsdag og hva du gjør først og senere.",["arbeidsdag","oppgave","pause","tidlig"]),
("4","Byliv","prepositions","Beskriv et sted i byen og hvordan man finner fram.",["gate","stasjon","sentrum","nær"]),
("5","Planer","future expressions","Fortell om planene dine for neste uke.",["plan","skal","helg","besøke"]),
("6","Sammenligning","comparatives","Sammenlign to steder, aktiviteter eller produkter.",["billigere","større","bedre","roligere"]),
("7","Erfaringer","perfect tense","Fortell om noe du har lært eller opplevd.",["har vært","har lært","erfaring","nytt"]),
("8","Hverdagsvalg","subordination","Forklar et valg og gi en enkel begrunnelse.",["fordi","hvis","derfor","valg"]),
],
"B1":[
("1","Utdanning og mål","conditional","Forklar hvilke ferdigheter du ønsker å utvikle og hvorfor.",["utdanning","ferdighet","mål","utvikle"]),
("2","Arbeid og erfaring","reported speech","Oppsummer en erfaring eller et råd fra en annen person.",["erfaring","arbeidsmiljø","råd","ansvar"]),
("3","Miljø og løsninger","causal clauses","Forklar et miljøproblem og foreslå en løsning.",["miljø","utslipp","løsning","forbruk"]),
("4","Medier og informasjon","source language","Sammenfat informasjon fra en artikkel og skill mellom fakta og mening.",["kilde","nyhet","påstand","fakta"]),
("5","Samfunn","concession","Presenter et synspunkt og ta med et relevant motargument.",["samfunn","fordel","ulempe","selv om"]),
("6","Kommunikasjon","relative clauses","Beskriv en person eller organisasjon med presise detaljer.",["som","der","kontakt","rolle"]),
("7","Problemløsning","conditionals","Drøft hva som kan gjøres når en plan ikke fungerer.",["problem","alternativ","konsekvens","mulighet"]),
("8","B1-repetisjon","cohesion","Lag en sammenhengende forklaring med tydelige forbindelser.",["for det første","dessuten","derfor","til slutt"]),
],
"B2":[
("1","Argumentasjon","argumentation","Presenter en tydelig påstand og støtt den med grunner og eksempler.",["påstand","argument","bevis","motargument"]),
("2","Arbeidsliv og teknologi","passive","Forklar hvordan en digital prosess gjennomføres og vurderes.",["digitalisering","prosess","effektiv","gjennomføre"]),
("3","Medier og kildekritikk","reported speech","Sammenlign to kilder og vurder hvordan de framstiller samme sak.",["kildekritikk","opplysning","vurdere","framstilling"]),
("4","Økonomi","nominalization","Forklar en økonomisk utvikling med presist og formelt språk.",["økonomi","utvikling","investering","kostnad"]),
("5","Samfunn og politikk","complex conditionals","Drøft mulige konsekvenser av ulike samfunnsvalg.",["konsekvens","tiltak","forutsetning","prioritere"]),
("6","Kultur og identitet","register","Tilpass samme budskap til en formell og en uformell mottaker.",["identitet","kultur","register","tilhørighet"]),
("7","Profesjonell kommunikasjon","indirect questions","Formuler høflige spørsmål og tydelige svar i en arbeidssituasjon.",["henvendelse","avklare","forespørsel","vedrørende"]),
("8","B2-repetisjon","discourse","Skriv og presenter et balansert argument med motforestillinger.",["imidlertid","dessuten","på den annen side","samlet"]),
],
"C1":[
("1","Akademisk argumentasjon","hedging","Formuler konklusjoner som skiller mellom dokumentasjon, sannsynlighet og tolkning.",["tyder på","kan indikere","forskning","konklusjon"]),
("2","Forskningsmetode","nominalization","Beskriv metode, funn og begrensninger med presist fagspråk.",["metode","funn","begrensning","analyse"]),
("3","Institusjonelt språk","formal register","Skriv en formell redegjørelse til en organisasjon eller myndighet.",["redegjørelse","prosedyre","forpliktelse","vedtak"]),
("4","Arbeidsliv","information structure","Strukturer en profesjonell tekst slik at ny og kjent informasjon blir tydelig.",["prioritet","implementering","ansvar","oppfølging"]),
("5","Kilde og evidens","evidentiality","Vurder styrken i en påstand ut fra kvaliteten på kilden.",["evidens","datagrunnlag","indikere","usikkerhet"]),
("6","Retorikk","rhetoric","Analyser hvordan ordvalg og struktur påvirker et arguments virkning.",["retorikk","kontrast","perspektiv","vektlegging"]),
("7","Pragmatikk","pragmatics","Forklar hvordan tone, relasjon og kontekst påvirker betydningen.",["underforstått","tone","hensyn","kontekst"]),
("8","C1-repetisjon","cohesion","Rediger en faglig tekst for presisjon, flyt og passende forbehold.",["sammenheng","presisjon","forbehold","nyanse"]),
],
"C2":[
("1","Avansert argumentasjon","argumentation","Analyser eksplisitte og implisitte premisser og formuler et balansert svar.",["premiss","forutsetning","motargument","konklusjon"]),
("2","Pragmatisk presisjon","pragmatics","Forklar hvordan indirekte formuleringer kan uttrykke kritikk, høflighet eller avstand.",["indirekte","høflighet","kritikk","undertekst"]),
("3","Retorisk organisering","rhetoric","Bruk kontrast, gjentakelse og perspektivbevegelser uten å miste presisjon.",["kontrast","gjentakelse","perspektiv","vektlegging"]),
("4","Diskursanalyse","discourse","Analyser hvordan ordvalg rammer inn en sak og påvirker mottakerens tolkning.",["diskurs","rammesetting","posisjonering","tolkning"]),
("5","Register og stil","register","Omskriv samme budskap til akademisk, juridisk og dagligdags norsk.",["formelt","nøytralt","uformelt","faglig"]),
("6","Oversettelsespresisjon","translation","Forklar hvorfor direkte oversettelser noen ganger endrer pragmatisk betydning.",["nyanse","ekvivalens","kontekst","idiom"]),
("7","Litterær og kritisk stil","stylistics","Analyser undertekst, ironi og stilistiske valg i en kompleks tekst.",["ironi","undertekst","stil","fortellerstemme"]),
("8","C2-syntese","synthesis","Sammenhold motstridende evidens og skriv en presis, nyansert konklusjon.",["evidens","motstridende","avveiing","nyanse"]),
],
}

def _seed(level: str, number: str, skill: str) -> dict[str, Any]:
    _, title, grammar, prompt, words = next(x for x in TOPICS[level] if x[0] == number)
    unit_id = f"no-{level.lower()}-unit-{number}"
    base = {
        "title": title,
        "objective": f"Utvikle norsk {level}-kompetanse gjennom temaet {title.lower()}.",
        "grammar": [grammar],
        "words": [(w, f"norsk uttrykk knyttet til {title.lower()}", f"Bruk «{w}» i en naturlig norsk setning.") for w in words],
        "examples": [f"Eksempel: {prompt}"],
        "source": "curated_norwegian",
        "unit_id": unit_id,
    }
    if skill == "grammar":
        base["objective"] = f"Bruk {title.lower()} korrekt og naturlig på norsk."
        base["grammar_examples"] = [f"Eksempel på {title.lower()}: {prompt}"]
    elif skill == "vocabulary":
        base["objective"] = f"Bruk sentralt norsk ordforråd om {title.lower()} i sammenheng."
    elif skill == "reading":
        base["text"] = f"{prompt} Teksten legger vekt på uttrykk som {', '.join(words)}."
        base["questions"] = ["Hva er hovedideen?", "Hvilke to uttrykk er sentrale?", "Hvilken detalj støtter hovedideen?"]
    elif skill == "listening":
        base["transcript"] = f"{prompt} Vi bruker blant annet uttrykkene {', '.join(words)}."
        base["questions"] = ["Hva er hovedbudskapet?", "Hvilke detaljer hørte du?", "Hvilket uttrykk viser talerens holdning?"]
    elif skill == "speaking":
        base["prompt"] = prompt
        base["phrases"] = words
        base["examples"] = [f"Jeg vil gjerne forklare hvordan {title.lower()} henger sammen med mine erfaringer."]
    elif skill == "writing":
        base["prompt"] = prompt
        base["guidance"] = [f"Bruk minst tre uttrykk: {', '.join(words)}.", "Knytt ideene sammen med tydelige overganger.", "Tilpass språk og detaljer til mottakeren."]
    elif skill == "review":
        base["questions"] = [f"Skriv to setninger om {title.lower()}.", f"Bruk minst to av uttrykkene: {', '.join(words)}.", "Forklar med egne ord når strukturen passer."]
    return base

S = {(level, f"no-{level.lower()}-unit-{number}", skill): _seed(level, number, skill)
     for level in LEVELS for number, *_ in TOPICS[level] for skill in SKILLS}

def get_lesson_seed(level: str, unit_id: str, lesson_type: str) -> dict[str, Any] | None:
    return S.get((str(level).upper(), str(unit_id), str(lesson_type).lower()))

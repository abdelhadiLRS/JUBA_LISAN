"""Curated Danish A2-C2 lesson seeds for JUBA LISAN.

The foundation file supplies the full Danish curriculum. This module adds a
deterministic, skill-complete authored layer so lesson generation does not
depend on an LLM for core Danish content.
"""
from __future__ import annotations

from typing import Any

_LEVELS = ("A2", "B1", "B2", "C1", "C2")
_SKILLS = ("grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review")

_UNITS: dict[str, list[tuple[str, str, str, str, list[str]]]] = {
    "A2": [
        ("1", "Fortid", "past", "Fortæl om noget, du lavede i går eller sidste weekend.", ["arbejdede", "rejste", "besøgte", "spiste"]),
        ("2", "Fremtid", "future", "Fortæl om dine planer for i morgen og næste uge.", ["skal", "vil", "planlægge", "rejse"]),
        ("3", "Anmodninger", "imperative", "Bed høfligt om hjælp, information eller en service.", ["kom", "vent", "hjælp", "gentag"]),
        ("4", "Modalverber", "modal", "Forklar, hvad du skal, kan, må eller vil gøre.", ["skal", "kan", "må", "vil"]),
        ("5", "Sammenligning", "comparative", "Sammenlign to steder, produkter eller aktiviteter.", ["bedre", "billigere", "større", "mere"]),
        ("6", "Perfektum", "perfect", "Fortæl om erfaringer, du har haft.", ["har været", "har set", "har lært", "har besøgt"]),
        ("7", "Refleksive verber", "reflexive", "Beskriv din morgenrutine og andre daglige vaner.", ["glæder mig", "skynder mig", "sætter mig", "klæder mig på"]),
        ("8", "Ledsætninger", "subordination", "Fortæl om en plan og forklar, hvornår eller hvorfor den sker.", ["når", "fordi", "hvis", "selvom"]),
    ],
    "B1": [
        ("1", "Relative sætninger", "relative", "Beskriv en person, et sted eller en ting med en relativsætning.", ["som", "der", "hvor", "hvilken"]),
        ("2", "Betingelser", "conditional", "Forklar, hvad du ville gøre i en bestemt situation.", ["hvis", "ville", "ellers", "så"]),
        ("3", "Refereret tale", "reported", "Fortæl, hvad en anden person har sagt eller forklaret.", ["siger", "fortæller", "mener", "at"]),
        ("4", "Årsag", "causal", "Forklar årsagerne til en beslutning eller et problem.", ["fordi", "derfor", "på grund af", "årsag"]),
        ("5", "Formål", "purpose", "Forklar, hvorfor du gør noget, og hvad du vil opnå.", ["for at", "så", "med det formål at", "for"]),
        ("6", "Indrømmelse", "concession", "Præsenter et synspunkt og nævn en relevant undtagelse.", ["selvom", "trods", "alligevel", "dog"]),
        ("7", "Beskrivelser", "relative", "Beskriv en nyhed, et projekt eller en begivenhed med præcise detaljer.", ["som", "der", "hvor", "hvis"]),
        ("8", "Refereret information", "reported", "Sammenfat information fra en samtale, artikel eller kilde.", ["ifølge", "oplyser", "fremgår", "hævdede"]),
    ],
    "B2": [
        ("1", "Passiv", "passive", "Forklar en proces eller begivenhed med fokus på handlingens resultat.", ["blev gennemført", "bliver undersøgt", "er blevet ændret", "udføres"]),
        ("2", "Kausativ", "causative", "Forklar, hvordan du får nogen til at udføre en opgave eller får noget repareret.", ["får repareret", "får lavet", "lader", "beder"]),
        ("3", "Pluskvamperfektum", "pluperfect", "Fortæl om en tidligere handling, der allerede var afsluttet.", ["havde gjort", "var gået", "havde læst", "var begyndt"]),
        ("4", "Indirekte spørgsmål", "indirect_questions", "Formulér spørgsmål indirekte i en professionel eller social samtale.", ["jeg ved ikke, om", "jeg vil gerne vide, hvor", "kan du forklare, hvorfor", "spørgsmålet er, hvordan"]),
        ("5", "Tekstbinding", "discourse", "Byg et sammenhængende argument med tydelige forbindelser.", ["derfor", "desuden", "imidlertid", "på den anden side"]),
        ("6", "Komplekse betingelser", "conditional", "Diskutér mulige konsekvenser af politiske, sociale eller arbejdsmæssige valg.", ["hvis", "ville", "kunne", "forudsat at"]),
        ("7", "Passiv i formelle tekster", "passive", "Omskriv en uformel beskrivelse til et mere formelt procesfokus.", ["det blev besluttet", "undersøgelsen gennemføres", "resultatet vurderes", "data indsamles"]),
        ("8", "Kausative mønstre", "causative", "Forklar ansvar, delegation og serviceydelser præcist.", ["få nogen til", "få noget gjort", "lade nogen", "sørge for"]),
    ],
    "C1": [
        ("1", "Nominalisering", "nominalization", "Omskriv centrale handlinger til præcise nominaliseringer i akademisk dansk.", ["undersøgelse", "vurdering", "implementering", "udvikling"]),
        ("2", "Akademisk forsigtighed", "hedging", "Formulér en konklusion med passende forbehold og evidens.", ["tyder på", "kan indikere", "synes at", "muligvis"]),
        ("3", "Informationsstruktur", "information_structure", "Fremhæv ny og kendt information for at skabe en klar argumentation.", ["det er", "netop", "især", "hvad angår"]),
        ("4", "Formelt register", "register", "Skriv en formel meddelelse til en institution eller samarbejdspartner.", ["hermed", "vedrørende", "såfremt", "i henhold til"]),
        ("5", "Argumentation", "argumentation", "Opbyg et argument med påstand, belæg, begrænsning og konklusion.", ["påstand", "belæg", "imidlertid", "konklusion"]),
        ("6", "Nuanceret forsigtighed", "hedging", "Skeln mellem sikker viden, sandsynlighed og fortolkning.", ["det er sandsynligt", "det kan ikke udelukkes", "resultaterne antyder", "der er tegn på"]),
        ("7", "Institutionelt sprog", "register", "Tilpas en tekst til en myndighed, organisation eller professionel modtager.", ["anmodning", "redegørelse", "procedure", "forpligtelse"]),
        ("8", "Akademisk formulering", "nominalization", "Redigér et afsnit, så det bliver præcist, sammenhængende og fagligt.", ["undersøgelsen", "analysen", "vurderingen", "resultatet"]),
    ],
    "C2": [
        ("1", "Avanceret argumentation", "argumentation", "Analyser og formulér et komplekst argument med eksplicitte og implicitte præmisser.", ["præmis", "forudsætning", "modargument", "konklusion"]),
        ("2", "Pragmatik", "pragmatics", "Forklar, hvordan høflighed, relation og kontekst ændrer betydningen.", ["indirekte", "hensyn", "underforstået", "tone"]),
        ("3", "Retorisk nuance", "rhetoric", "Brug retoriske greb uden at miste præcision eller faglighed.", ["kontrast", "gentagelse", "perspektiv", "vægtning"]),
        ("4", "Diskursanalyse", "discourse_analysis", "Analyser, hvordan ordvalg og struktur fremstiller en sag fra et bestemt perspektiv.", ["diskurs", "rammesætning", "perspektiv", "positionering"]),
        ("5", "Informationsstruktur", "information_structure", "Forklar, hvordan fokus og informationsrækkefølge påvirker fortolkningen.", ["fokus", "kontrast", "topik", "ny information"]),
        ("6", "Register og stil", "register", "Omskriv den samme pointe til juridisk, akademisk og almindeligt dansk.", ["formelt", "neutralt", "uformelt", "specialiseret"]),
        ("7", "Kompleks argumentation", "argumentation", "Sammenhold modstridende evidens og formuler en afbalanceret konklusion.", ["evidens", "modstridende", "begrænsning", "afvejning"]),
        ("8", "Avanceret retorik", "rhetoric", "Redigér en tekst for stilistisk præcision, implicit betydning og overbevisningskraft.", ["nuance", "undertekst", "ironi", "præcision"]),
    ],
}

def _unit(level: str, number: str) -> tuple[str, str, str, str, list[str]]:
    return next(item for item in _UNITS[level] if item[0] == number)

def _seed(level: str, number: str, skill: str) -> dict[str, Any]:
    _, title, grammar, prompt, words = _unit(level, number)
    unit_id = f"da-{level.lower()}-unit-{number}"
    vocab_text = ", ".join(words)
    examples = [
        f"Dansk: {words[0]}.",
        f"Eksempel: {prompt}",
    ]
    base: dict[str, Any] = {
        "title": title,
        "objective": f"Behersk {title.lower()} på {level}-niveau i dansk.",
        "grammar": [grammar],
        "words": [(word, "relevant dansk udtryk", f"Brug {word} i en naturlig sætning.") for word in words],
        "examples": examples,
        "source": "curated_danish",
        "unit_id": unit_id,
    }
    if skill == "grammar":
        base["objective"] = f"Brug {title.lower()} korrekt og naturligt i dansk."
        base["grammar_examples"] = [
            f"Jeg arbejdede i går, fordi jeg havde tid." if level == "A2" and number == "1"
            else f"Det tyder på, at resultatet kan være vigtigt." if level in {"C1", "C2"}
            else f"Dette er et eksempel på {title.lower()}."
        ]
    elif skill == "vocabulary":
        base["objective"] = f"Brug centralt ordforråd om {title.lower()} i sammenhæng."
    elif skill == "reading":
        base["objective"] = f"Læs og analyser en kort dansk tekst om {title.lower()}."
        base["text"] = f"{prompt} Centrale udtryk er: {vocab_text}. Brug teksten til at finde hovedidé, detaljer og sproglige valg."
        base["questions"] = [
            "Hvad er tekstens hovedidé?",
            "Hvilke to udtryk er vigtigst for forståelsen?",
            "Hvilken detalje understøtter hovedidéen?",
        ]
    elif skill == "listening":
        base["objective"] = f"Forstå hovedidé og detaljer i dansk tale om {title.lower()}."
        base["transcript"] = f"{prompt} Vi bruger blandt andet udtrykkene {vocab_text}."
        base["questions"] = [
            "Hvad er hovedbudskabet?",
            "Hvilke to detaljer hørte du?",
            "Hvilket udtryk viser talerens holdning eller intention?",
        ]
    elif skill == "speaking":
        base["objective"] = f"Tal sammenhængende og naturligt om {title.lower()}."
        base["prompt"] = prompt
        base["phrases"] = words
        base["examples"] = [f"Jeg vil gerne forklare, hvordan {title.lower()} hænger sammen med min hverdag eller mit arbejde."]
    elif skill == "writing":
        base["objective"] = f"Skriv en sammenhængende tekst på dansk om {title.lower()}."
        base["prompt"] = prompt
        base["guidance"] = [
            f"Brug mindst tre udtryk: {vocab_text}.",
            "Brug tydelige forbindelser mellem dine idéer.",
            "Tilpas register og detaljer til modtageren.",
        ]
    elif skill == "review":
        base["objective"] = f"Repetér {title.lower()} og integrér grammatik og ordforråd."
        base["questions"] = [
            f"Skriv to sætninger, der viser {title.lower()}.",
            f"Brug mindst to af disse udtryk: {vocab_text}.",
            "Forklar med egne ord, hvornår strukturen passer.",
        ]
    return base

S = {
    (level, f"da-{level.lower()}-unit-{number}", skill): _seed(level, number, skill)
    for level in _LEVELS
    for number, *_ in _UNITS[level]
    for skill in _SKILLS
}

def get_lesson_seed(level: str, unit_id: str, lesson_type: str) -> dict[str, Any] | None:
    return S.get((str(level).upper(), str(unit_id), str(lesson_type).lower()))

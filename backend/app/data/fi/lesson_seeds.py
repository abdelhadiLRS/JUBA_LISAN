"""Curated Finnish A2-C2 lesson seeds for JUBA LISAN.

The seed layer keeps authored Finnish wording in the runtime path instead of
falling back to generic instructional English.
"""
from __future__ import annotations

from typing import Any

_LEVEL_UNITS = {
    "A2": [
        ("fi-a2-unit-1", "Päivittäiset rutiinit"),
        ("fi-a2-unit-2", "Menetelmät ja asiointi"),
        ("fi-a2-unit-3", "Matkustaminen"),
        ("fi-a2-unit-4", "Terveys ja hyvinvointi"),
        ("fi-a2-unit-5", "Menneet tapahtumat"),
        ("fi-a2-unit-6", "Suunnitelmat ja vertailu"),
        ("fi-a2-unit-7", "Kokemukset ja mielipiteet"),
        ("fi-a2-unit-8", "Kertaus ja A2-viestintä"),
    ],
    "B1": [
        ("fi-b1-unit-1", "Työ ja opiskelu"),
        ("fi-b1-unit-2", "Kertominen menneestä"),
        ("fi-b1-unit-3", "Objektin sijat käytössä"),
        ("fi-b1-unit-4", "Palvelut ja yhteiskunta"),
        ("fi-b1-unit-5", "Ehdot ja kohteliaisuus"),
        ("fi-b1-unit-6", "Suhdelauseet ja kuvailu"),
        ("fi-b1-unit-7", "Perustelut ja keskustelu"),
        ("fi-b1-unit-8", "Kertaus ja B1-viestintä"),
    ],
    "B2": [
        ("fi-b2-unit-1", "Media ja lähdekritiikki"),
        ("fi-b2-unit-2", "Passiivi ja muodollinen kieli"),
        ("fi-b2-unit-3", "Referointi ja näkökulmat"),
        ("fi-b2-unit-4", "Ympäristö ja yhteiskunta"),
        ("fi-b2-unit-5", "Lauseenvastikkeet"),
        ("fi-b2-unit-6", "Tekstin koheesio"),
        ("fi-b2-unit-7", "Rekisteri ja argumentointi"),
        ("fi-b2-unit-8", "Kertaus ja B2-viestintä"),
    ],
    "C1": [
        ("fi-c1-unit-1", "Akateeminen kirjoittaminen"),
        ("fi-c1-unit-2", "Monipolviset rakenteet"),
        ("fi-c1-unit-3", "Hallinto ja työelämä"),
        ("fi-c1-unit-4", "Varovaisuus ja evidenssi"),
        ("fi-c1-unit-5", "Argumentin rakentaminen"),
        ("fi-c1-unit-6", "Pragmatiikka ja sävy"),
        ("fi-c1-unit-7", "Tekstin muokkaus"),
        ("fi-c1-unit-8", "Kertaus ja C1-viestintä"),
    ],
    "C2": [
        ("fi-c2-unit-1", "Retoriikan analyysi"),
        ("fi-c2-unit-2", "Tyylin ja rekisterin hallinta"),
        ("fi-c2-unit-3", "Käännöksen täsmällisyys"),
        ("fi-c2-unit-4", "Kirjalliset vivahteet"),
        ("fi-c2-unit-5", "Diskurssin analyysi"),
        ("fi-c2-unit-6", "Vaativa argumentointi"),
        ("fi-c2-unit-7", "Kielellinen editointi"),
        ("fi-c2-unit-8", "Kertaus ja C2-viestintä"),
    ],
}

_GRAMMAR = {
    "A2": ["genetiivi ja omistus", "imperfekti", "perfekti", "tulevaisuudesta puhuminen",
           "vertailu", "käskyt ja kohteliaisuus", "verbien rektiot"],
    "B1": ["objektin sijamuodot", "passiivi", "konditionaali", "suhdelauseet",
           "partisiipit", "täytyy, pitää ja on tehtävä", "referointi"],
    "B2": ["myönnytys ja vastakohta", "infinitiivit ja lauseenvastikkeet",
           "passiivin aikamuodot", "teema ja informaatiorakenne", "nominalisointi",
           "rekisteri ja puhekieli", "monipolviset sivulauseet"],
    "C1": ["tieteellinen varovaisuus", "monipolviset sivulauseet",
           "argumentointi ja tekstin rakenne", "hallinto- ja työelämän kieli",
           "pragmatiikka ja kohteliaisuus", "nominalisointi"],
    "C2": ["retoriikka ja vaikuttaminen", "käännöksen täsmällisyys",
           "kirjallinen tyyli ja vivahteet", "diskurssin analyysi",
           "argumentointi", "pragmatiikka", "rekisteri"],
}

_WORDS = {
    "A2": [("matka", "trip", "Suunnittelemme matkaa."), ("terveys", "health", "Terveys on tärkeää."),
            ("kokemus", "experience", "Se oli hyvä kokemus."), ("suunnitelma", "plan", "Minulla on suunnitelma.")],
    "B1": [("työpaikka", "workplace", "Uusi työpaikka alkaa maanantaina."), ("opiskelu", "studying", "Opiskelu vaatii aikaa."),
            ("palvelu", "service", "Palvelu oli nopeaa."), ("perustelu", "justification", "Tarvitsen hyvän perustelun.")],
    "B2": [("lähde", "source", "Lähde pitää tarkistaa."), ("väite", "claim", "Väite vaatii perusteluja."),
            ("näkökulma", "perspective", "Toinen näkökulma muuttaa tulkintaa."), ("rekisteri", "register", "Rekisteri riippuu tilanteesta.")],
    "C1": [("aineisto", "data/material", "Aineisto on rajallinen."), ("evidenssi", "evidence", "Evidenssi tukee tulkintaa."),
            ("johtopäätös", "conclusion", "Johtopäätös perustuu aineistoon."), ("rajoitus", "limitation", "Tutkimuksella on selvä rajoitus.")],
    "C2": [("vivahde", "nuance", "Vivahde vaikuttaa tulkintaan."), ("ennakko-oletus", "presupposition", "Ennakko-oletus ei ole aina näkyvä."),
            ("sävy", "tone", "Sävy muuttuu kontekstin mukaan."), ("retoriikka", "rhetoric", "Retoriikka ohjaa lukijan huomiota.")],
}

def _unit_level(unit_id: str) -> str | None:
    for level, units in _LEVEL_UNITS.items():
        if any(uid == unit_id for uid, _ in units):
            return level
    return None

def get_lesson_seed(level: str, unit_id: str, lesson_type: str) -> dict[str, Any] | None:
    level = str(level).upper()
    skill = str(lesson_type).lower()
    titles = dict(_LEVEL_UNITS.get(level, []))
    title = titles.get(str(unit_id))
    if not title or skill not in {"grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"}:
        return None

    grammar = _GRAMMAR[level]
    words = [(word, definition, example) for word, definition, example in _WORDS[level]]
    examples = [example for _, _, example in words]
    seed: dict[str, Any] = {
        "title": title,
        "objective": f"Harjoittele suomea aiheesta {title}.",
        "grammar": grammar[:4],
        "words": words,
        "examples": examples,
        "source": "curated_finnish",
    }

    if skill == "grammar":
        seed["objective"] = f"Käytä oikein rakenteita: {', '.join(grammar[:3])}."
    elif skill == "vocabulary":
        seed["objective"] = f"Laajenna sanastoa aiheessa {title} ja käytä uusia sanoja lauseissa."
    elif skill == "reading":
        seed["objective"] = f"Ymmärrä suomenkielinen teksti aiheesta {title}."
        seed["text"] = f"{title}. Tässä kokonaisuudessa tarkastelemme käytännön tilanteita ja niiden merkityksiä. {examples[0]} {examples[1]}"
        seed["questions"] = [
            "Mikä on tekstin pääaihe?",
            "Mitä kaksi tärkeää ilmaisua löydät tekstistä?",
            "Miten selittäisit tekstin keskeisen ajatuksen omin sanoin?",
        ]
    elif skill == "listening":
        seed["objective"] = f"Poimi keskeiset tiedot kuullusta tekstistä aiheesta {title}."
        seed["transcript"] = f"{title}. Keskustelussa puhutaan käytännön tilanteesta ja perustellaan eri näkökulmia. {examples[0]} {examples[2]}"
        seed["questions"] = [
            "Mikä on keskustelun pääasia?",
            "Mitkä kaksi yksityiskohtaa kuulet?",
            "Mikä ilmaus kertoo puhujan näkökulmasta?",
        ]
    elif skill == "speaking":
        seed["objective"] = f"Puhu suomeksi aiheesta {title} ja perustele omat ajatuksesi."
        seed["prompt"] = f"Kerro aiheesta {title}. Käytä vähintään kolmea uutta sanaa ja yhtä rakenteista: {grammar[0]}."
        seed["phrases"] = examples
    elif skill == "writing":
        seed["objective"] = f"Kirjoita selkeä suomenkielinen teksti aiheesta {title}."
        seed["prompt"] = f"Kirjoita lyhyt teksti aiheesta {title}. Käytä vähintään kolmea kohdesanaa ja rakennetta {grammar[1]}."
        seed["guidance"] = [
            f"Käytä rakennetta {grammar[0]}.",
            "Käytä vähintään kolmea uutta sanaa.",
            "Yhdistä ajatukset kokonaisiksi kappaleiksi.",
        ]
    elif skill == "review":
        seed["objective"] = f"Kertaa aiheen {title} keskeinen kieliaines."
        seed["questions"] = [
            f"Muodosta yksi lause käyttäen rakennetta {grammar[0]}.",
            f"Käytä kahta sanaa aiheesta {title} samassa tekstissä.",
            "Muotoile yksi ajatus uudelleen täsmällisemmin.",
        ]
    return seed

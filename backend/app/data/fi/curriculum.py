"""Full CEFR Finnish curriculum for JUBA LISAN."""
from app.data._types import CurriculumUnit

_LEVELS = {
    "A1": [
        ("Tervehdykset ja identiteetti", ["personal-pronouns","word-order"], ["fi-a1-greetings","fi-a1-identity"], ["Tervehtiä ja esitellä itsensä","Antaa perustietoja itsestään"]),
        ("Perhe ja ihmiset", ["possessive","present-tense"], ["fi-a1-family","fi-a1-daily"], ["Kertoa perheestä","Kuvata arkea"]),
        ("Koti ja ympäristö", ["local-cases","possessive"], ["fi-a1-home","fi-a1-places"], ["Kuvata kotia","Kertoa sijainnista"]),
        ("Ruoka ja asiointi", ["partitive","questions"], ["fi-a1-food","fi-a1-shopping"], ["Tilata ruokaa","Kysyä hintoja"]),
    ],
    "A2": [
        ("Päivittäiset tilanteet", ["past-tense","object-cases"], ["fi-a2-routines","fi-a2-time"], ["Kertoa menneestä päivästä","Kuvata aikatauluja"]),
        ("Matkustaminen", ["local-cases","motion-verbs"], ["fi-a2-travel","fi-a2-transport"], ["Selviytyä matkasta","Kysyä reiteistä"]),
        ("Terveys ja vapaa-aika", ["imperative","comparatives"], ["fi-a2-health","fi-a2-leisure"], ["Kertoa terveydestä","Verrata vaihtoehtoja"]),
        ("Työ ja palvelut", ["perfect","modal-verbs"], ["fi-a2-work","fi-a2-services"], ["Asioida palveluissa","Kuvata työkokemusta"]),
    ],
    "B1": [
        ("Opinnot ja tavoitteet", ["conditional","relative-clauses"], ["fi-b1-education","fi-b1-goals"], ["Kertoa tavoitteista","Perustella valintoja"]),
        ("Työelämä", ["passive","reported-speech"], ["fi-b1-career","fi-b1-workplace"], ["Keskustella työstä","Referoida tietoa"]),
        ("Media ja yhteiskunta", ["connectors","nominalization"], ["fi-b1-media","fi-b1-society"], ["Ymmärtää uutisia","Rakentaa perusteltu mielipide"]),
        ("Ihmissuhteet ja kokemukset", ["perfect","subordinate-clauses"], ["fi-b1-relationships","fi-b1-experiences"], ["Kertoa kokemuksista","Kuvata syy-seuraussuhteita"]),
    ],
    "B2": [
        ("Väittely ja argumentointi", ["concessive-clauses","complex-syntax"], ["fi-b2-debate","fi-b2-argument"], ["Puolustaa näkökulmaa","Vastata vastaväitteisiin"]),
        ("Kulttuuri ja identiteetti", ["participle-structures","register"], ["fi-b2-culture","fi-b2-identity"], ["Keskustella kulttuurista","Säätää ilmaisun sävyä"]),
        ("Talous ja ammatillinen viestintä", ["verb-government","nominal-style"], ["fi-b2-economy","fi-b2-professional"], ["Käsitellä talousaiheita","Kirjoittaa ammatillisesti"]),
        ("Ongelmat ja ratkaisut", ["conditionals","causality"], ["fi-b2-problems","fi-b2-solutions"], ["Analysoida ongelmia","Ehdottaa ratkaisuja"]),
    ],
    "C1": [
        ("Akateeminen kieli", ["academic-register","nominalization"], ["fi-c1-academic","fi-c1-research"], ["Kirjoittaa analyyttisesti","Esittää tutkimustietoa"]),
        ("Ammatillinen viestintä", ["formal-register","politeness"], ["fi-c1-professional","fi-c1-meetings"], ["Johtaa keskustelua","Muotoilla virallisia viestejä"]),
        ("Yhteiskunta ja analyysi", ["hedging","reported-discourse"], ["fi-c1-society","fi-c1-analysis"], ["Arvioida lähteitä","Ilmaista epävarmuutta täsmällisesti"]),
        ("Retoriikka ja tyyli", ["discourse-markers","cohesion"], ["fi-c1-rhetoric","fi-c1-style"], ["Rakentaa vakuuttava teksti","Hallita tekstin sidosteisuutta"]),
    ],
    "C2": [
        ("Merkityksen hienovaraisuudet", ["semantic-precision","aspect-nuance"], ["fi-c2-nuance","fi-c2-semantics"], ["Erotella merkitysvivahteita","Valita täsmällinen ilmaus"]),
        ("Edistynyt argumentointi", ["advanced-conditionals","concessive-nuance"], ["fi-c2-debate","fi-c2-rhetoric"], ["Käsitellä vastakkaisia näkemyksiä","Rakentaa monitasoinen argumentti"]),
        ("Erikois- ja akateeminen kieli", ["technical-register","dense-syntax"], ["fi-c2-specialized","fi-c2-academic"], ["Mukauttaa terminologiaa","Tulkitse vaativaa tekstiä"]),
        ("Synteesi ja ilmaisun hallinta", ["synthesis","stylistic-precision"], ["fi-c2-synthesis","fi-c2-expression"], ["Yhdistää useita lähteitä","Tuottaa erittäin täsmällistä tekstiä"]),
    ],
}
CURRICULUM = {
    level: [
        CurriculumUnit(id=f"fi-{level.lower()}-{index}", level=level, unit_number=index, title=title,
            grammar_points=grammar, vocabulary_set_ids=vocab,
            lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],
            competency_checklist=competencies, default_weeks=2,
            prerequisite_unit=(f"fi-{level.lower()}-{index-1}" if index > 1 else None))
        for index, (title, grammar, vocab, competencies) in enumerate(units, 1)
    ] for level, units in _LEVELS.items()
}

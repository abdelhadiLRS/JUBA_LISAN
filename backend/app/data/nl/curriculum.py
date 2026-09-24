"""Nederlands CEFR curriculum A1-C2."""
from app.data._types import CurriculumUnit

def _u(level, n, title, grammar, vocab, goals, prereq=None):
    return CurriculumUnit(
        id=f"{level.lower()}-unit-{n}",
        level=level,
        unit_number=n,
        title=title,
        grammar_points=grammar,
        vocabulary_set_ids=vocab,
        lesson_types=["grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"],
        competency_checklist=goals,
        default_weeks=2,
        prerequisite_unit=prereq,
    )

CURRICULUM = {
    "A1": [
        _u("A1", 1, "Kennismaken en basiszinnen", ["pronouns", "word-order", "present-tense"], ["greetings_a1", "identity_a1"], ["Jezelf voorstellen", "Eenvoudige zinnen begrijpen en maken"]),
        _u("A1", 2, "Familie en dagelijks leven", ["articles", "plural", "adjectives"], ["family_a1", "daily-life_a1"], ["Familie beschrijven", "Dagelijkse routines vertellen"], "a1-unit-1"),
        _u("A1", 3, "Tijd, vragen en afspraken", ["questions", "negation"], ["time_a1", "appointments_a1"], ["Tijd en afspraken bespreken", "Eenvoudige vragen stellen"], "a1-unit-2"),
        _u("A1", 4, "Eten en winkelen", ["articles", "word-order"], ["food_a1", "shopping_a1"], ["Eten bestellen", "Prijzen en voorkeuren bespreken"], "a1-unit-3"),
    ],
    "A2": [
        _u("A2", 1, "Wonen en omgeving", ["present-perfect", "adjectives"], ["home_a2", "neighborhood_a2"], ["Wonen beschrijven", "De weg en omgeving uitleggen"], ["a1-unit-4"]),
        _u("A2", 2, "Reizen en vervoer", ["past-tense", "separable-verbs"], ["travel_a2", "transport_a2"], ["Een reis plannen", "Vervoer en ervaringen bespreken"], "a2-unit-1"),
        _u("A2", 3, "Gezondheid en diensten", ["modal-verbs", "imperative"], ["health_a2", "services_a2"], ["Klachten beschrijven", "Hulp en diensten vragen"], "a2-unit-2"),
        _u("A2", 4, "Werk en vrije tijd", ["comparatives", "reflexive-verbs"], ["work_a2", "leisure_a2"], ["Werk en hobby's bespreken", "Voorkeuren vergelijken"], "a2-unit-3"),
    ],
    "B1": [
        _u("B1", 1, "Opleiding en werkervaring", ["perfect", "subordinate-clauses"], ["education_b1", "career_b1"], ["Ervaring en plannen beschrijven", "Redenen en gevolgen verbinden"], ["a2-unit-4"]),
        _u("B1", 2, "Nieuws en maatschappij", ["relative-pronouns", "reported-speech"], ["media_b1", "society_b1"], ["Nieuws samenvatten", "Een standpunt uitleggen"], "b1-unit-1"),
        _u("B1", 3, "Relaties en gevoelens", ["conditional", "conjunctions"], ["relationships_b1", "emotions_b1"], ["Gevoelens genuanceerd beschrijven", "Advies geven"], "b1-unit-2"),
        _u("B1", 4, "Reizen en problemen oplossen", ["future", "modal-verbs"], ["travel_b1", "solutions_b1"], ["Een probleem uitleggen", "Oplossingen voorstellen"], "b1-unit-3"),
    ],
    "B2": [
        _u("B2", 1, "Argumentatie en debat", ["passive", "conditionals"], ["argumentation_b2", "debate_b2"], ["Argumenten structureren", "Tegenargumenten formuleren"], ["b1-unit-4"]),
        _u("B2", 2, "Werk en leiderschap", ["nominalization", "advanced-conjunctions"], ["leadership_b2", "workplace_b2"], ["Professionele situaties analyseren", "Voorstellen onderbouwen"], "b2-unit-1"),
        _u("B2", 3, "Cultuur en identiteit", ["reported-speech", "relative-clauses"], ["culture_b2", "identity_b2"], ["Culturele verschillen bespreken", "Nuances in betekenis herkennen"], "b2-unit-2"),
        _u("B2", 4, "Problemen en oplossingen", ["passive", "complex-conditionals"], ["problems_b2", "solutions_b2"], ["Complexe problemen analyseren", "Een uitvoerbaar plan presenteren"], "b2-unit-3"),
    ],
    "C1": [
        _u("C1", 1, "Nuance en register", ["register", "syntactic-variation"], ["nuance_c1", "register_c1"], ["Formeel en informeel register beheersen", "Betekenisnuances uitdrukken"], ["b2-unit-4"]),
        _u("C1", 2, "Academisch Nederlands", ["nominalization", "cohesion"], ["academic_c1", "research_c1"], ["Academische teksten structureren", "Bronnen en argumenten verbinden"], "c1-unit-1"),
        _u("C1", 3, "Professionele communicatie", ["reported-speech", "passive"], ["professional_c1", "meetings_c1"], ["Professionele correspondentie schrijven", "Vergaderingen leiden en samenvatten"], "c1-unit-2"),
        _u("C1", 4, "Maatschappelijke analyse", ["complex-subordination", "discourse-markers"], ["society_c1", "analysis_c1"], ["Complexe teksten interpreteren", "Analytische conclusies formuleren"], "c1-unit-3"),
    ],
    "C2": [
        _u("C2", 1, "Stijl en register", ["style", "register"], ["style_c2", "register_c2"], ["Taalstijl bewust aanpassen", "Subtiele registerverschillen herkennen"], ["c1-unit-4"]),
        _u("C2", 2, "Geavanceerde argumentatie", ["rhetoric", "inversion"], ["rhetoric_c2", "argumentation_c2"], ["Complexe argumenten evalueren", "Retorische effecten doelgericht inzetten"], "c2-unit-1"),
        _u("C2", 3, "Kritische analyse", ["discourse", "cohesion"], ["critical_c2", "analysis_c2"], ["Impliciete betekenissen analyseren", "Nuance en perspectief onderscheiden"], "c2-unit-2"),
        _u("C2", 4, "Precisie en synthese", ["syntactic-variation", "focus"], ["precision_c2", "synthesis_c2"], ["Geavanceerde teksten synthetiseren", "Zeer precieze formuleringen produceren"], "c2-unit-3"),
    ],
}

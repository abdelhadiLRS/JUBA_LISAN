"""Czech A1-C2 curriculum for JUBA LISAN."""
from app.data._types import CurriculumUnit

def _unit(level, n, title, grammar, vocab, weeks=1):
    return CurriculumUnit(
        id=f"cs-{level.lower()}-{n}", level=level, unit_number=n, title=title,
        grammar_points=grammar, vocabulary_set_ids=vocab,
        lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],
        competency_checklist=[
            f"Understand and use Czech for {title.lower()} at {level} level",
            "Apply the target grammar in a short communicative task",
            "Use topic vocabulary in context",
        ],
        default_weeks=weeks,
        prerequisite_unit=f"cs-{level.lower()}-{n-1}" if n>1 else None,
    )

CURRICULUM = {
"A1":[
_unit("A1",1,"Pozdravy a představování",["a1-pronouns","a1-questions"],["greetings_a1","identity_a1"]),
_unit("A1",2,"Rodina a lidé",["a1-gender","a1-cases"],["family_a1","people_a1"]),
_unit("A1",3,"Každodenní život",["a1-present","a1-negation"],["daily_a1","routine_a1"]),
_unit("A1",4,"Čas a plán dne",["a1-questions","a1-present"],["time_a1","schedule_a1"]),
],
"A2":[
_unit("A2",1,"Bydlení a okolí",["a2-cases","a2-prepositions"],["home_a2","neighborhood_a2"]),
_unit("A2",2,"Cestování a doprava",["a2-future","a2-word-order"],["travel_a2","transport_a2"]),
_unit("A2",3,"Zdraví a volný čas",["a2-past","a2-comparison"],["health_a2","leisure_a2"]),
_unit("A2",4,"Práce a služby",["a2-reflexive","a2-relative"],["work_a2","services_a2"]),
],
"B1":[
_unit("B1",1,"Studium a cíle",["b1-conditional","b1-purpose"],["education_b1","goals_b1"]),
_unit("B1",2,"Práce a zkušenosti",["b1-case-government","b1-reported"],["career_b1","experience_b1"]),
_unit("B1",3,"Média a společnost",["b1-connectors","b1-relative-cases"],["media_b1","society_b1"]),
_unit("B1",4,"Problémy a řešení",["b1-passive","b1-perfective-nuance"],["problems_b1","solutions_b1"]),
],
"B2":[
_unit("B2",1,"Argumentace a debata",["b2-contrast","b2-discourse"],["debate_b2","argument_b2"]),
_unit("B2",2,"Kultura a identita",["b2-concession","b2-complex-syntax"],["culture_b2","identity_b2"]),
_unit("B2",3,"Ekonomika a profesní komunikace",["b2-formal-register","b2-verb-valency"],["economy_b2","professional_b2"]),
_unit("B2",4,"Analýza a prezentace řešení",["b2-nominalization","b2-participles"],["analysis_b2","solutions_b2"]),
],
"C1":[
_unit("C1",1,"Akademický jazyk a výzkum",["c1-academic","c1-reporting"],["academic_c1","research_c1"]),
_unit("C1",2,"Profesionální komunikace",["c1-politeness","c1-hedging"],["professional_c1","meetings_c1"]),
_unit("C1",3,"Společnost a analýza",["c1-cohesion","c1-syntax"],["society_c1","analysis_c1"]),
_unit("C1",4,"Rétorika a styl",["c1-lexical-precision","c1-cohesion"],["rhetoric_c1","style_c1"]),
],
"C2":[
_unit("C2",1,"Sémantická nuance",["c2-semantic","c2-idiomatic"],["nuance_c2","semantics_c2"]),
_unit("C2",2,"Pokročilá argumentace",["c2-rhetoric","c2-discourse-markers"],["argument_c2","debate_c2"]),
_unit("C2",3,"Specializovaný a odborný jazyk",["c2-register","c2-complexity"],["specialist_c2","academic_c2"]),
_unit("C2",4,"Syntéza a přesné vyjadřování",["c2-synthesis","c2-semantic"],["synthesis_c2","expression_c2"]),
],
}

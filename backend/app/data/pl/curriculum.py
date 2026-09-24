"""Polski CEFR curriculum A1-C2."""
from app.data._types import CurriculumUnit

def _u(level, n, title, grammar, vocab, competencies):
    return CurriculumUnit(
        id=f"{level.lower()}-unit-{n}", level=level, unit_number=n, title=title,
        grammar_points=grammar, vocabulary_set_ids=vocab,
        lesson_types=["grammar","vocabulary","reading","writing","listening","review"],
        competency_checklist=competencies, default_weeks=2,
        prerequisite_unit=f"{level.lower()}-unit-{n-1}" if n > 1 else None,
    )

CURRICULUM = {
"A1":[
_u("A1",1,"Poznajmy się",["pronouns","gender","present-tense"],["greetings_a1","identity_a1"],["Przedstawianie się","Podawanie podstawowych informacji"]),
_u("A1",2,"Rodzina i codzienność",["adjectives","present-tense","negation"],["family_a1","daily-life_a1"],["Mówienie o rodzinie","Opisywanie rutyny"]),
_u("A1",3,"Czas, miejsce i spotkania",["questions","numbers","locative-case"],["time_a1","places_a1"],["Pytanie o czas i miejsce","Umawianie prostego spotkania"]),
_u("A1",4,"Jedzenie i zakupy",["accusative-case","genitive-case","imperative"],["food_a1","shopping_a1"],["Robienie zakupów","Zamawianie jedzenia"]),
],
"A2":[
_u("A2",1,"Dom i okolica",["past-tense","locative-case","prepositions"],["home_a2","neighborhood_a2"],["Opisywanie mieszkania","Orientowanie się w okolicy"]),
_u("A2",2,"Podróże i transport",["motion-verbs","instrumental-case","future-tense"],["travel_a2","transport_a2"],["Planowanie podróży","Pytanie o drogę i transport"]),
_u("A2",3,"Zdrowie i usługi",["dative-case","reflexive-verbs","imperative"],["health_a2","services_a2"],["Opis prostych dolegliwości","Korzystanie z usług"]),
_u("A2",4,"Praca i czas wolny",["aspect-intro","comparatives","conjunctions"],["work_a2","leisure_a2"],["Mówienie o pracy","Rozmowa o zainteresowaniach"]),
],
"B1":[
_u("B1",1,"Nauka i doświadczenie",["aspect","participles-intro","genitive-quantities"],["education_b1","experience_b1"],["Opisywanie doświadczeń","Rozmowa o edukacji"]),
_u("B1",2,"Media i społeczeństwo",["relative-clauses","reported-speech","instrumental"],["media_b1","society_b1"],["Streszczanie informacji","Wyrażanie opinii o społeczeństwie"]),
_u("B1",3,"Relacje i emocje",["conditional","verb-government","reflexive"],["relationships_b1","emotions_b1"],["Wyrażanie uczuć","Rozmowa o relacjach"]),
_u("B1",4,"Problemy i rozwiązania",["subordinate-clauses","purpose-clauses","aspect"],["problems_b1","solutions_b1"],["Opisywanie problemów","Proponowanie rozwiązań"]),
],
"B2":[
_u("B2",1,"Argumentacja i debata",["discourse-markers","conditional","concessive-clauses"],["argumentation_b2","debate_b2"],["Budowanie argumentu","Udział w dyskusji"]),
_u("B2",2,"Praca i przywództwo",["passive","nominalization","complex-government"],["leadership_b2","workplace_b2"],["Komunikacja zawodowa","Opisywanie procesów i decyzji"]),
_u("B2",3,"Kultura i tożsamość",["advanced-aspect","relative-clauses","modal-expressions"],["culture_b2","identity_b2"],["Analiza tekstów kultury","Mówienie o tożsamości"]),
_u("B2",4,"Polityka, zmiana i rozwiązania",["complex-conjunctions","impersonal-constructions","reported-speech"],["policy_b2","solutions_b2"],["Omawianie zmian","Porównywanie propozycji"]),
],
"C1":[
_u("C1",1,"Niuans i rejestr",["register","modality","information-structure"],["nuance_c1","register_c1"],["Dobór rejestru","Precyzyjne wyrażanie stanowiska"]),
_u("C1",2,"Język akademicki",["academic-syntax","nominalization","cohesion"],["academic_c1","research_c1"],["Streszczanie badań","Budowanie tekstu akademickiego"]),
_u("C1",3,"Komunikacja profesjonalna",["professional-style","hedging","complex-subordination"],["professional_c1","meetings_c1"],["Prowadzenie spotkania","Formułowanie rekomendacji"]),
_u("C1",4,"Analiza społeczna",["discourse-organization","argumentation","impersonal-style"],["society_c1","analysis_c1"],["Analiza zjawisk","Synteza wielu źródeł"]),
],
"C2":[
_u("C2",1,"Styl i głos autora",["stylistic-syntax","register-variation","ellipsis"],["style_c2","register_c2"],["Rozpoznawanie stylu","Świadome kształtowanie głosu autora"]),
_u("C2",2,"Zaawansowana argumentacja",["rhetoric","complex-argumentation","information-focus"],["rhetoric_c2","argumentation_c2"],["Budowanie złożonej argumentacji","Analiza środków retorycznych"]),
_u("C2",3,"Analiza krytyczna",["critical-reading","semantic-precision","cohesion"],["critical_c2","analysis_c2"],["Krytyczna interpretacja","Ocena spójności i założeń tekstu"]),
_u("C2",4,"Precyzja i synteza",["syntactic-variation","lexical-precision","synthesis"],["precision_c2","synthesis_c2"],["Redagowanie z wysoką precyzją","Synteza złożonych materiałów"]),
],
}

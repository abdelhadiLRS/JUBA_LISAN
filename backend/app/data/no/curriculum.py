from app.data._types import CurriculumUnit

def _u(level: str, number: int, title: str, grammar: list[str], vocab: list[str], weeks: int = 2, prerequisite: str | None = None) -> CurriculumUnit:
    return CurriculumUnit(
        id=f"no-{level.lower()}-{number}",
        level=level,
        unit_number=number,
        title=title,
        grammar_points=grammar,
        vocabulary_set_ids=vocab,
        lesson_types=["grammar", "vocabulary", "reading", "writing", "listening", "review"],
        competency_checklist=["Forstå og bruke sentrale strukturer i naturlig norsk", "Kommunisere muntlig og skriftlig i relevante situasjoner"],
        default_weeks=weeks,
        prerequisite_unit=prerequisite,
    )

CURRICULUM = {
    "A1": [
        _u("A1", 1, "Hilsener og presentasjon", ["personlige pronomen", "å være og å hete", "ja/nei-spørsmål"], ["no-a1-greetings", "no-a1-identity"]),
        _u("A1", 2, "Familie og hverdag", ["presens", "bestemt og ubestemt form", "genitiv"], ["no-a1-family", "no-a1-daily"]),
        _u("A1", 3, "Tid og steder", ["preposisjoner", "klokkeslett og datoer", "V2-ordstilling"], ["no-a1-time", "no-a1-city"]),
        _u("A1", 4, "Mat og handling", ["mengdeord", "adjektiv i grunnform", "modalverbet kan"], ["no-a1-food", "no-a1-shopping"]),
    ],
    "A2": [
        _u("A2", 1, "Bolig og nærmiljø", ["adjektivbøying", "det finnes", "refleksive verb"], ["no-a2-home", "no-a2-neighborhood"], prerequisite="no-a1-4"),
        _u("A2", 2, "Reise og transport", ["preteritum", "skal og vil", "spørreord"], ["no-a2-travel", "no-a2-transport"]),
        _u("A2", 3, "Helse og fritid", ["perfektum", "bør og må", "adverbplassering"], ["no-a2-health", "no-a2-leisure"]),
        _u("A2", 4, "Arbeid og service", ["leddsetninger med at", "fordi og derfor", "sammenligning"], ["no-a2-work", "no-a2-service"]),
    ],
    "B1": [
        _u("B1", 1, "Utdanning og mål", ["pluskvamperfektum", "infinitiv med å", "relative setninger"], ["no-b1-education", "no-b1-goals"], prerequisite="no-a2-4"),
        _u("B1", 2, "Yrkesliv og arbeidsmiljø", ["passiv med -s", "indirekte tale", "setningsadverbialer"], ["no-b1-career", "no-b1-workplace"]),
        _u("B1", 3, "Medier og samfunn", ["konjunksjoner og subjunksjoner", "kontrast", "argumenterende struktur"], ["no-b1-media", "no-b1-society"]),
        _u("B1", 4, "Relasjoner og erfaringer", ["som-setninger", "betingelser med hvis", "verbpartikler"], ["no-b1-relationships", "no-b1-experiences"]),
    ],
    "B2": [
        _u("B2", 1, "Argumentasjon og debatt", ["konjunktiv-lignende hypotetiske uttrykk", "innrømmende leddsetninger", "diskursmarkører"], ["no-b2-argument", "no-b2-debate"], prerequisite="no-b1-4"),
        _u("B2", 2, "Kultur og identitet", ["nominalisering", "partisippkonstruksjoner", "kompleks V2-ordstilling"], ["no-b2-culture", "no-b2-identity"]),
        _u("B2", 3, "Økonomi og profesjonelt språk", ["verbvalens", "passiv og upersonlige konstruksjoner", "formell stil"], ["no-b2-economy", "no-b2-professional"]),
        _u("B2", 4, "Problemer og løsninger", ["årsaks- og konsekvenskonstruksjoner", "substantiviske ledd", "presis modalitet"], ["no-b2-problems", "no-b2-solutions"]),
    ],
    "C1": [
        _u("C1", 1, "Akademisk språk og forskning", ["nominalstil", "komplekse relative setninger", "kildehenvisende språk"], ["no-c1-academic", "no-c1-research"], prerequisite="no-b2-4"),
        _u("C1", 2, "Møter og profesjonell kommunikasjon", ["høflige forespørsler", "modalitet og forbehold", "refererende uttrykk"], ["no-c1-professional", "no-c1-meetings"]),
        _u("C1", 3, "Samfunn og analyse", ["kohesjon", "parallelle konstruksjoner", "avanserte bindeord"], ["no-c1-society", "no-c1-analysis"]),
        _u("C1", 4, "Retorikk og stil", ["retoriske kontraster", "informasjonsstruktur", "registerskifte"], ["no-c1-rhetoric", "no-c1-style"]),
    ],
    "C2": [
        _u("C2", 1, "Semantisk presisjon", ["betydningsnyanser", "idiomatisk syntaks", "leksikalsk presisjon"], ["no-c2-nuance", "no-c2-semantics"], prerequisite="no-c1-4"),
        _u("C2", 2, "Avansert debatt", ["komplekse hypotetiske uttrykk", "implisitte premisser", "argumentasjonsstrategier"], ["no-c2-argument", "no-c2-debate"]),
        _u("C2", 3, "Spesialisert og akademisk norsk", ["tett nominalsyntaks", "faglig register", "komprimert informasjonsstruktur"], ["no-c2-specialized", "no-c2-academic"]),
        _u("C2", 4, "Syntese og uttrykkskraft", ["stilistiske variasjoner", "kohesjon på tekstnivå", "idiomatiske nyanser"], ["no-c2-synthesis", "no-c2-expression"]),
    ],
}

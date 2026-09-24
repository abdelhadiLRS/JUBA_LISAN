"""Πλήρες CEFR πρόγραμμα ελληνικών A1–C2 για JUBA LISAN."""
from app.data._types import CurriculumUnit

_LEVELS = {
    "A1": [
        ("Χαιρετισμοί και ταυτότητα", ["pronouns", "articles", "gender"], ["greetings_a1", "identity_a1"]),
        ("Οικογένεια και καθημερινότητα", ["present-tense", "negation"], ["family_a1", "daily_a1"]),
        ("Χρόνος και μετακίνηση", ["questions", "prepositions"], ["time_a1", "city_a1"]),
        ("Φαγητό και αγορές", ["accusative", "adjectives"], ["food_a1", "shopping_a1"]),
    ],
    "A2": [
        ("Σπίτι και γειτονιά", ["past-tense", "articles"], ["home_a2", "neighborhood_a2"]),
        ("Ταξίδια και μεταφορές", ["future-tense", "prepositions"], ["travel_a2", "transport_a2"]),
        ("Υγεία και ευεξία", ["imperative", "reflexive-verbs"], ["health_a2", "body_a2"]),
        ("Εργασία και ελεύθερος χρόνος", ["comparatives", "subordinate-clauses"], ["work_a2", "leisure_a2"]),
    ],
    "B1": [
        ("Εκπαίδευση και στόχοι", ["perfective-imperfective", "purpose-clauses"], ["education_b1", "goals_b1"]),
        ("Εργασία και επαγγελματική ζωή", ["relative-clauses", "conditionals"], ["career_b1", "workplace_b1"]),
        ("Μέσα και κοινωνία", ["reported-speech", "connectors"], ["media_b1", "society_b1"]),
        ("Σχέσεις και εμπειρίες", ["subjunctive", "aspect-review"], ["relationships_b1", "experiences_b1"]),
    ],
    "B2": [
        ("Επιχειρηματολογία και συζήτηση", ["concessive-clauses", "conditionals"], ["argument_b2", "debate_b2"]),
        ("Πολιτισμός και ταυτότητα", ["nominalization", "participles"], ["culture_b2", "identity_b2"]),
        ("Οικονομία και επαγγελματική επικοινωνία", ["passive-voice", "verb-government"], ["economy_b2", "professional_b2"]),
        ("Προβλήματα και λύσεις", ["discourse-markers", "complex-syntax"], ["problems_b2", "solutions_b2"]),
    ],
    "C1": [
        ("Ακαδημαϊκός λόγος", ["academic-register", "nominal-style"], ["academic_c1", "research_c1"]),
        ("Επαγγελματική επικοινωνία", ["formal-register", "polite-requests"], ["professional_c1", "meetings_c1"]),
        ("Κοινωνική ανάλυση", ["hedging", "reported-discourse"], ["society_c1", "analysis_c1"]),
        ("Ρητορική και ύφος", ["rhetorical-devices", "cohesion"], ["rhetoric_c1", "style_c1"]),
    ],
    "C2": [
        ("Λεπτές σημασιολογικές αποχρώσεις", ["semantic-precision", "aspect-nuance"], ["nuance_c2", "semantics_c2"]),
        ("Σύνθετη επιχειρηματολογία", ["advanced-conditionals", "concessive-nuance"], ["argument_c2", "debate_c2"]),
        ("Εξειδικευμένος και ακαδημαϊκός λόγος", ["technical-register", "dense-syntax"], ["specialized_c2", "academic_c2"]),
        ("Σύνθεση και δημιουργική έκφραση", ["style-shifting", "discourse-synthesis"], ["synthesis_c2", "expression_c2"]),
    ],
}

_OBJECTIVES = {
    "A1": ["Να συστήνεται και να ανταλλάσσει βασικές πληροφορίες", "Να κατανοεί και να παράγει απλές καθημερινές προτάσεις"],
    "A2": ["Να χειρίζεται συνηθισμένες καταστάσεις με μεγαλύτερη αυτονομία", "Να αφηγείται απλές εμπειρίες και σχέδια"],
    "B1": ["Να επικοινωνεί με σαφήνεια σε εργασία, σπουδές και κοινωνικές περιστάσεις", "Να υποστηρίζει απόψεις και να αφηγείται εμπειρίες"],
    "B2": ["Να επιχειρηματολογεί με ακρίβεια και συνοχή", "Να προσαρμόζει το ύφος σε τυπικά και ημιτυπικά περιβάλλοντα"],
    "C1": ["Να κατανοεί σύνθετο λόγο και να εκφράζει λεπτές αποχρώσεις", "Να παράγει συνεκτικό ακαδημαϊκό και επαγγελματικό λόγο"],
    "C2": ["Να χειρίζεται σχεδόν πλήρως τις σημασιολογικές και υφολογικές αποχρώσεις", "Να συνθέτει σύνθετα επιχειρήματα με φυσικό και ακριβή λόγο"],
}

CURRICULUM = {}
for level, units in _LEVELS.items():
    CURRICULUM[level] = []
    for n, (title, grammar, vocab) in enumerate(units, 1):
        CURRICULUM[level].append(
            CurriculumUnit(
                id=f"{level.lower()}-unit-{n}",
                level=level,
                unit_number=n,
                title=title,
                grammar_points=grammar,
                vocabulary_set_ids=vocab,
                lesson_types=["grammar", "vocabulary", "reading", "writing", "listening", "review"],
                competency_checklist=_OBJECTIVES[level],
                default_weeks=2,
                prerequisite_unit=f"{level.lower()}-unit-{n-1}" if n > 1 else None,
            )
        )

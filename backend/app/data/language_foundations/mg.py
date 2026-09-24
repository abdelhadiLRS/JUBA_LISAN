"""Malagasy foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

CURRICULUM={
 "A1":[
CurriculumUnit(id="mg-a1-unit-1",level="A1",unit_number=1,title="Malagasy: greetings",grammar_points=["mg-a1-g1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use salama in a basic exchange","Understand a short greetings interaction"],default_weeks=1),
CurriculumUnit(id="mg-a1-unit-2",level="A1",unit_number=2,title="Malagasy: identity",grammar_points=["mg-a1-g2"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use anarana in a basic exchange","Understand a short identity interaction"],default_weeks=1),
CurriculumUnit(id="mg-a1-unit-3",level="A1",unit_number=3,title="Malagasy: family",grammar_points=["mg-a1-g3"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use reny in a basic exchange","Understand a short family interaction"],default_weeks=1),
CurriculumUnit(id="mg-a1-unit-4",level="A1",unit_number=4,title="Malagasy: home",grammar_points=["mg-a1-g4"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use trano in a basic exchange","Understand a short home interaction"],default_weeks=1),
CurriculumUnit(id="mg-a1-unit-5",level="A1",unit_number=5,title="Malagasy: routine",grammar_points=["mg-a1-g5"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use mianatra in a basic exchange","Understand a short routine interaction"],default_weeks=1),
CurriculumUnit(id="mg-a1-unit-6",level="A1",unit_number=6,title="Malagasy: time",grammar_points=["mg-a1-g6"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use fotoana in a basic exchange","Understand a short time interaction"],default_weeks=1),
CurriculumUnit(id="mg-a1-unit-7",level="A1",unit_number=7,title="Malagasy: food",grammar_points=["mg-a1-g7"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use rano in a basic exchange","Understand a short food interaction"],default_weeks=1),
CurriculumUnit(id="mg-a1-unit-8",level="A1",unit_number=8,title="Malagasy: places",grammar_points=["mg-a1-g8"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use sekoly in a basic exchange","Understand a short places interaction"],default_weeks=1)
 ]
}
for level in LEVELS[1:]:
 CURRICULUM[level]=[CurriculumUnit(id=f"mg-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Malagasy {level} communication",grammar_points=["intermediate grammar"],vocabulary_set_ids=[],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Handle extended communication"],default_weeks=2)]

GRAMMAR_TOPICS=[
GrammarTopic(slug="mg-a1-g1",title="Personal pronouns",level="A1",category="grammar",summary="Use common pronouns in simple clauses.",explanation="Use common pronouns in simple clauses.",examples=[GrammarExample(text="Izaho dia mpianatra.")]),
GrammarTopic(slug="mg-a1-g2",title="Copula",level="A1",category="grammar",summary="Identify people and things with dia.",explanation="Identify people and things with dia.",examples=[GrammarExample(text="Izy dia mpampianatra.")]),
GrammarTopic(slug="mg-a1-g3",title="Present tense",level="A1",category="grammar",summary="Describe current actions.",explanation="Describe current actions.",examples=[GrammarExample(text="Mianatra aho.")]),
GrammarTopic(slug="mg-a1-g4",title="Negation",level="A1",category="grammar",summary="Negate simple statements with tsy.",explanation="Negate simple statements with tsy.",examples=[GrammarExample(text="Tsy mianatra aho.")]),
GrammarTopic(slug="mg-a1-g5",title="Questions",level="A1",category="grammar",summary="Ask basic information questions.",explanation="Ask basic information questions.",examples=[GrammarExample(text="Aiza ianao?")]),
GrammarTopic(slug="mg-a1-g6",title="Possession",level="A1",category="grammar",summary="Express possession with simple noun phrases.",explanation="Express possession with simple noun phrases.",examples=[GrammarExample(text="Ny bokiko.")]),
GrammarTopic(slug="mg-a1-g7",title="Locatives",level="A1",category="grammar",summary="Say where someone is.",explanation="Say where someone is.",examples=[GrammarExample(text="Ao an-trano aho.")]),
GrammarTopic(slug="mg-a1-g8",title="Plural nouns",level="A1",category="grammar",summary="Use common plural markers and forms.",explanation="Use common plural markers and forms.",examples=[GrammarExample(text="olona / olona")])
]
VOCABULARY_SETS=[
VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="mg-a1-unit-1",words=[VocabularyEntry(word="salama",pos="noun",definition="hello / well",example="Salama!")]),
VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="mg-a1-unit-2",words=[VocabularyEntry(word="anarana",pos="noun",definition="name",example="Ny anarako dia Lova.")]),
VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="mg-a1-unit-3",words=[VocabularyEntry(word="reny",pos="noun",definition="mother",example="Ao an-trano ny reniko.")]),
VocabularySet(id="home_a1",level="A1",topic="home",unit_ref="mg-a1-unit-4",words=[VocabularyEntry(word="trano",pos="noun",definition="house",example="Lehibe ny trano.")]),
VocabularySet(id="routine_a1",level="A1",topic="routine",unit_ref="mg-a1-unit-5",words=[VocabularyEntry(word="mianatra",pos="noun",definition="to study",example="Mianatra aho.")]),
VocabularySet(id="time_a1",level="A1",topic="time",unit_ref="mg-a1-unit-6",words=[VocabularyEntry(word="fotoana",pos="noun",definition="time",example="Amin'ny firy izao?")]),
VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="mg-a1-unit-7",words=[VocabularyEntry(word="rano",pos="noun",definition="water",example="Mila rano aho.")]),
VocabularySet(id="places_a1",level="A1",topic="places",unit_ref="mg-a1-unit-8",words=[VocabularyEntry(word="sekoly",pos="noun",definition="school",example="Any an-tsekoly aho.")])
]
PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="greetings_a1_1",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="Salama.",context="Hello.",register="neutral")]),
PhrasebookCategory(id="greetings_a1_2",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="Misaotra.",context="Thank you.",register="neutral")]),
PhrasebookCategory(id="help_a1_3",level="A1",situation="help",icon="💬",phrases=[PhrasebookEntry(text="Azafady.",context="Please / excuse me.",register="neutral")]),
PhrasebookCategory(id="directions_a1_4",level="A1",situation="directions",icon="💬",phrases=[PhrasebookEntry(text="Aiza ny sekoly?",context="Where is the school?",register="neutral")])
]
ASSESSMENT_BANK=[
AssessmentQuestion(id="mg-a1-001",skill="vocabulary",difficulty="A1",question="Choose the correct Malagasy form for A1.",options=["salama","anarana","reny","trano"],correct="salama"),
AssessmentQuestion(id="mg-a1-002",skill="grammar",difficulty="A1",question="Choose the correct Malagasy form for A1.",options=["anarana","reny","trano","mianatra"],correct="anarana"),
AssessmentQuestion(id="mg-a1-003",skill="reading",difficulty="A1",question="Choose the correct Malagasy form for A1.",options=["reny","trano","mianatra","fotoana"],correct="reny"),
AssessmentQuestion(id="mg-a1-004",skill="speaking",difficulty="A1",question="Choose the correct Malagasy form for A1.",options=["trano","mianatra","fotoana","rano"],correct="trano"),
AssessmentQuestion(id="mg-a1-005",skill="vocabulary",difficulty="A1",question="Choose the correct Malagasy form for A1.",options=["mianatra","fotoana","rano","sekoly"],correct="mianatra"),
AssessmentQuestion(id="mg-a1-006",skill="grammar",difficulty="A1",question="Choose the correct Malagasy form for A1.",options=["fotoana","rano","sekoly","salama"],correct="fotoana"),
AssessmentQuestion(id="mg-a1-007",skill="reading",difficulty="A1",question="Choose the correct Malagasy form for A1.",options=["rano","sekoly","salama","anarana"],correct="rano"),
AssessmentQuestion(id="mg-a1-008",skill="speaking",difficulty="A1",question="Choose the correct Malagasy form for A1.",options=["sekoly","salama","anarana","reny"],correct="sekoly"),
AssessmentQuestion(id="mg-a1-009",skill="vocabulary",difficulty="A1",question="Choose the correct Malagasy form for A1.",options=["salama","anarana","reny","trano"],correct="salama"),
AssessmentQuestion(id="mg-a1-010",skill="grammar",difficulty="A1",question="Choose the correct Malagasy form for A1.",options=["anarana","reny","trano","mianatra"],correct="anarana")
]

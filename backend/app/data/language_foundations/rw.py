"""Kinyarwanda foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

CURRICULUM={
 "A1":[
CurriculumUnit(id="rw-a1-unit-1",level="A1",unit_number=1,title="Kinyarwanda: greetings",grammar_points=["rw-a1-g1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use muraho in a basic exchange","Understand a short greetings interaction"],default_weeks=1),
CurriculumUnit(id="rw-a1-unit-2",level="A1",unit_number=2,title="Kinyarwanda: identity",grammar_points=["rw-a1-g2"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use izina in a basic exchange","Understand a short identity interaction"],default_weeks=1),
CurriculumUnit(id="rw-a1-unit-3",level="A1",unit_number=3,title="Kinyarwanda: family",grammar_points=["rw-a1-g3"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use mama in a basic exchange","Understand a short family interaction"],default_weeks=1),
CurriculumUnit(id="rw-a1-unit-4",level="A1",unit_number=4,title="Kinyarwanda: home",grammar_points=["rw-a1-g4"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use inzu in a basic exchange","Understand a short home interaction"],default_weeks=1),
CurriculumUnit(id="rw-a1-unit-5",level="A1",unit_number=5,title="Kinyarwanda: routine",grammar_points=["rw-a1-g5"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use kwiga in a basic exchange","Understand a short routine interaction"],default_weeks=1),
CurriculumUnit(id="rw-a1-unit-6",level="A1",unit_number=6,title="Kinyarwanda: time",grammar_points=["rw-a1-g6"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use igihe in a basic exchange","Understand a short time interaction"],default_weeks=1),
CurriculumUnit(id="rw-a1-unit-7",level="A1",unit_number=7,title="Kinyarwanda: food",grammar_points=["rw-a1-g7"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use amazi in a basic exchange","Understand a short food interaction"],default_weeks=1),
CurriculumUnit(id="rw-a1-unit-8",level="A1",unit_number=8,title="Kinyarwanda: places",grammar_points=["rw-a1-g8"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ishuri in a basic exchange","Understand a short places interaction"],default_weeks=1)
 ]
}
for level in LEVELS[1:]:
 CURRICULUM[level]=[CurriculumUnit(id=f"rw-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Kinyarwanda {level} communication",grammar_points=["intermediate grammar"],vocabulary_set_ids=[],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Handle extended communication"],default_weeks=2)]

GRAMMAR_TOPICS=[
GrammarTopic(slug="rw-a1-g1",title="Subject pronouns",level="A1",category="grammar",summary="Use common personal pronouns.",explanation="Use common personal pronouns.",examples=[GrammarExample(text="Jye ndi umunyeshuri.")]),
GrammarTopic(slug="rw-a1-g2",title="Copula",level="A1",category="grammar",summary="Identify people and things.",explanation="Identify people and things.",examples=[GrammarExample(text="Uyu ni umwarimu.")]),
GrammarTopic(slug="rw-a1-g3",title="Present tense",level="A1",category="grammar",summary="Describe current actions.",explanation="Describe current actions.",examples=[GrammarExample(text="Ndiga.")]),
GrammarTopic(slug="rw-a1-g4",title="Negation",level="A1",category="grammar",summary="Negate simple statements.",explanation="Negate simple statements.",examples=[GrammarExample(text="Sinsoma.")]),
GrammarTopic(slug="rw-a1-g5",title="Questions",level="A1",category="grammar",summary="Ask basic information questions.",explanation="Ask basic information questions.",examples=[GrammarExample(text="Uri he?")]),
GrammarTopic(slug="rw-a1-g6",title="Possession",level="A1",category="grammar",summary="Express ownership.",explanation="Express ownership.",examples=[GrammarExample(text="Igitabo cyanjye.")]),
GrammarTopic(slug="rw-a1-g7",title="Locatives",level="A1",category="grammar",summary="Say where someone is.",explanation="Say where someone is.",examples=[GrammarExample(text="Ndi mu rugo.")]),
GrammarTopic(slug="rw-a1-g8",title="Plural nouns",level="A1",category="grammar",summary="Recognize common noun class changes.",explanation="Recognize common noun class changes.",examples=[GrammarExample(text="umuntu / abantu")])
]
VOCABULARY_SETS=[
VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="rw-a1-unit-1",words=[VocabularyEntry(word="muraho",pos="noun",definition="hello",example="Muraho neza.")]),
VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="rw-a1-unit-2",words=[VocabularyEntry(word="izina",pos="noun",definition="name",example="Izina ryanjye ni Aline.")]),
VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="rw-a1-unit-3",words=[VocabularyEntry(word="mama",pos="noun",definition="mother",example="Mama ari mu rugo.")]),
VocabularySet(id="home_a1",level="A1",topic="home",unit_ref="rw-a1-unit-4",words=[VocabularyEntry(word="inzu",pos="noun",definition="house",example="Inzu ni nini.")]),
VocabularySet(id="routine_a1",level="A1",topic="routine",unit_ref="rw-a1-unit-5",words=[VocabularyEntry(word="kwiga",pos="noun",definition="to study",example="Ndiga buri munsi.")]),
VocabularySet(id="time_a1",level="A1",topic="time",unit_ref="rw-a1-unit-6",words=[VocabularyEntry(word="igihe",pos="noun",definition="time",example="Ni iki gihe?")]),
VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="rw-a1-unit-7",words=[VocabularyEntry(word="amazi",pos="noun",definition="water",example="Ndashaka amazi.")]),
VocabularySet(id="places_a1",level="A1",topic="places",unit_ref="rw-a1-unit-8",words=[VocabularyEntry(word="ishuri",pos="noun",definition="school",example="Ndi ku ishuri.")])
]
PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="greetings_a1_1",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="Muraho.",context="Hello.",register="neutral")]),
PhrasebookCategory(id="greetings_a1_2",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="Murakoze.",context="Thank you.",register="neutral")]),
PhrasebookCategory(id="help_a1_3",level="A1",situation="help",icon="💬",phrases=[PhrasebookEntry(text="Mfashe.",context="Help me.",register="neutral")]),
PhrasebookCategory(id="directions_a1_4",level="A1",situation="directions",icon="💬",phrases=[PhrasebookEntry(text="Ishuri riri he?",context="Where is the school?",register="neutral")])
]
ASSESSMENT_BANK=[
AssessmentQuestion(id="rw-a1-001",skill="vocabulary",difficulty="A1",question="Choose the correct Kinyarwanda form for A1.",options=["muraho","izina","mama","inzu"],correct="muraho"),
AssessmentQuestion(id="rw-a1-002",skill="grammar",difficulty="A1",question="Choose the correct Kinyarwanda form for A1.",options=["izina","mama","inzu","kwiga"],correct="izina"),
AssessmentQuestion(id="rw-a1-003",skill="reading",difficulty="A1",question="Choose the correct Kinyarwanda form for A1.",options=["mama","inzu","kwiga","igihe"],correct="mama"),
AssessmentQuestion(id="rw-a1-004",skill="speaking",difficulty="A1",question="Choose the correct Kinyarwanda form for A1.",options=["inzu","kwiga","igihe","amazi"],correct="inzu"),
AssessmentQuestion(id="rw-a1-005",skill="vocabulary",difficulty="A1",question="Choose the correct Kinyarwanda form for A1.",options=["kwiga","igihe","amazi","ishuri"],correct="kwiga"),
AssessmentQuestion(id="rw-a1-006",skill="grammar",difficulty="A1",question="Choose the correct Kinyarwanda form for A1.",options=["igihe","amazi","ishuri","muraho"],correct="igihe"),
AssessmentQuestion(id="rw-a1-007",skill="reading",difficulty="A1",question="Choose the correct Kinyarwanda form for A1.",options=["amazi","ishuri","muraho","izina"],correct="amazi"),
AssessmentQuestion(id="rw-a1-008",skill="speaking",difficulty="A1",question="Choose the correct Kinyarwanda form for A1.",options=["ishuri","muraho","izina","mama"],correct="ishuri"),
AssessmentQuestion(id="rw-a1-009",skill="vocabulary",difficulty="A1",question="Choose the correct Kinyarwanda form for A1.",options=["muraho","izina","mama","inzu"],correct="muraho"),
AssessmentQuestion(id="rw-a1-010",skill="grammar",difficulty="A1",question="Choose the correct Kinyarwanda form for A1.",options=["izina","mama","inzu","kwiga"],correct="izina")
]

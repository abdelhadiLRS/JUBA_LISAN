"""Chichewa foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

CURRICULUM={
 "A1":[
CurriculumUnit(id="ny-a1-unit-1",level="A1",unit_number=1,title="Chichewa: greetings",grammar_points=["ny-a1-g1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use moni in a basic exchange","Understand a short greetings interaction"],default_weeks=1),
CurriculumUnit(id="ny-a1-unit-2",level="A1",unit_number=2,title="Chichewa: identity",grammar_points=["ny-a1-g2"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use dzina in a basic exchange","Understand a short identity interaction"],default_weeks=1),
CurriculumUnit(id="ny-a1-unit-3",level="A1",unit_number=3,title="Chichewa: family",grammar_points=["ny-a1-g3"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use mayi in a basic exchange","Understand a short family interaction"],default_weeks=1),
CurriculumUnit(id="ny-a1-unit-4",level="A1",unit_number=4,title="Chichewa: home",grammar_points=["ny-a1-g4"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use nyumba in a basic exchange","Understand a short home interaction"],default_weeks=1),
CurriculumUnit(id="ny-a1-unit-5",level="A1",unit_number=5,title="Chichewa: routine",grammar_points=["ny-a1-g5"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use kuphunzira in a basic exchange","Understand a short routine interaction"],default_weeks=1),
CurriculumUnit(id="ny-a1-unit-6",level="A1",unit_number=6,title="Chichewa: time",grammar_points=["ny-a1-g6"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use nthawi in a basic exchange","Understand a short time interaction"],default_weeks=1),
CurriculumUnit(id="ny-a1-unit-7",level="A1",unit_number=7,title="Chichewa: food",grammar_points=["ny-a1-g7"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use madzi in a basic exchange","Understand a short food interaction"],default_weeks=1),
CurriculumUnit(id="ny-a1-unit-8",level="A1",unit_number=8,title="Chichewa: places",grammar_points=["ny-a1-g8"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use sukulu in a basic exchange","Understand a short places interaction"],default_weeks=1)
 ]
}
for level in LEVELS[1:]:
 CURRICULUM[level]=[CurriculumUnit(id=f"ny-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Chichewa {level} communication",grammar_points=["intermediate grammar"],vocabulary_set_ids=[],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Handle extended communication"],default_weeks=2)]

GRAMMAR_TOPICS=[
GrammarTopic(slug="ny-a1-g1",title="Subject prefixes",level="A1",category="grammar",summary="Use subject markers with common verbs.",explanation="Use subject markers with common verbs.",examples=[GrammarExample(text="Ndimaphunzira.")]),
GrammarTopic(slug="ny-a1-g2",title="Copula",level="A1",category="grammar",summary="Identify people and things.",explanation="Identify people and things.",examples=[GrammarExample(text="Ine ndine wophunzira.")]),
GrammarTopic(slug="ny-a1-g3",title="Present tense",level="A1",category="grammar",summary="Describe regular/current actions.",explanation="Describe regular/current actions.",examples=[GrammarExample(text="Ndimadya.")]),
GrammarTopic(slug="ny-a1-g4",title="Negation",level="A1",category="grammar",summary="Negate simple present statements.",explanation="Negate simple present statements.",examples=[GrammarExample(text="Sindimadya.")]),
GrammarTopic(slug="ny-a1-g5",title="Questions",level="A1",category="grammar",summary="Ask basic information questions.",explanation="Ask basic information questions.",examples=[GrammarExample(text="Uli kuti?")]),
GrammarTopic(slug="ny-a1-g6",title="Possession",level="A1",category="grammar",summary="Express ownership with possessive forms.",explanation="Express ownership with possessive forms.",examples=[GrammarExample(text="Buku langa.")]),
GrammarTopic(slug="ny-a1-g7",title="Locatives",level="A1",category="grammar",summary="Say where someone is.",explanation="Say where someone is.",examples=[GrammarExample(text="Ndili kunyumba.")]),
GrammarTopic(slug="ny-a1-g8",title="Plural nouns",level="A1",category="grammar",summary="Recognize common noun class pairs.",explanation="Recognize common noun class pairs.",examples=[GrammarExample(text="munthu / anthu")])
]
VOCABULARY_SETS=[
VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="ny-a1-unit-1",words=[VocabularyEntry(word="moni",pos="noun",definition="hello",example="Moni!")]),
VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="ny-a1-unit-2",words=[VocabularyEntry(word="dzina",pos="noun",definition="name",example="Dzina langa ndi Banda.")]),
VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="ny-a1-unit-3",words=[VocabularyEntry(word="mayi",pos="noun",definition="mother",example="Mayi ali kunyumba.")]),
VocabularySet(id="home_a1",level="A1",topic="home",unit_ref="ny-a1-unit-4",words=[VocabularyEntry(word="nyumba",pos="noun",definition="house",example="Nyumba ndi yayikulu.")]),
VocabularySet(id="routine_a1",level="A1",topic="routine",unit_ref="ny-a1-unit-5",words=[VocabularyEntry(word="kuphunzira",pos="noun",definition="to study",example="Ndimaphunzira tsiku lililonse.")]),
VocabularySet(id="time_a1",level="A1",topic="time",unit_ref="ny-a1-unit-6",words=[VocabularyEntry(word="nthawi",pos="noun",definition="time",example="Ndi nthawi yanji?")]),
VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="ny-a1-unit-7",words=[VocabularyEntry(word="madzi",pos="noun",definition="water",example="Ndikufuna madzi.")]),
VocabularySet(id="places_a1",level="A1",topic="places",unit_ref="ny-a1-unit-8",words=[VocabularyEntry(word="sukulu",pos="noun",definition="school",example="Ndili kusukulu.")])
]
PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="greetings_a1_1",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="Moni.",context="Hello.",register="neutral")]),
PhrasebookCategory(id="greetings_a1_2",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="Zikomo.",context="Thank you.",register="neutral")]),
PhrasebookCategory(id="help_a1_3",level="A1",situation="help",icon="💬",phrases=[PhrasebookEntry(text="Chonde.",context="Please.",register="neutral")]),
PhrasebookCategory(id="directions_a1_4",level="A1",situation="directions",icon="💬",phrases=[PhrasebookEntry(text="Sukulu ili kuti?",context="Where is the school?",register="neutral")])
]
ASSESSMENT_BANK=[
AssessmentQuestion(id="ny-a1-001",skill="vocabulary",difficulty="A1",question="Choose the correct Chichewa form for A1.",options=["moni","dzina","mayi","nyumba"],correct="moni"),
AssessmentQuestion(id="ny-a1-002",skill="grammar",difficulty="A1",question="Choose the correct Chichewa form for A1.",options=["dzina","mayi","nyumba","kuphunzira"],correct="dzina"),
AssessmentQuestion(id="ny-a1-003",skill="reading",difficulty="A1",question="Choose the correct Chichewa form for A1.",options=["mayi","nyumba","kuphunzira","nthawi"],correct="mayi"),
AssessmentQuestion(id="ny-a1-004",skill="speaking",difficulty="A1",question="Choose the correct Chichewa form for A1.",options=["nyumba","kuphunzira","nthawi","madzi"],correct="nyumba"),
AssessmentQuestion(id="ny-a1-005",skill="vocabulary",difficulty="A1",question="Choose the correct Chichewa form for A1.",options=["kuphunzira","nthawi","madzi","sukulu"],correct="kuphunzira"),
AssessmentQuestion(id="ny-a1-006",skill="grammar",difficulty="A1",question="Choose the correct Chichewa form for A1.",options=["nthawi","madzi","sukulu","moni"],correct="nthawi"),
AssessmentQuestion(id="ny-a1-007",skill="reading",difficulty="A1",question="Choose the correct Chichewa form for A1.",options=["madzi","sukulu","moni","dzina"],correct="madzi"),
AssessmentQuestion(id="ny-a1-008",skill="speaking",difficulty="A1",question="Choose the correct Chichewa form for A1.",options=["sukulu","moni","dzina","mayi"],correct="sukulu"),
AssessmentQuestion(id="ny-a1-009",skill="vocabulary",difficulty="A1",question="Choose the correct Chichewa form for A1.",options=["moni","dzina","mayi","nyumba"],correct="moni"),
AssessmentQuestion(id="ny-a1-010",skill="grammar",difficulty="A1",question="Choose the correct Chichewa form for A1.",options=["dzina","mayi","nyumba","kuphunzira"],correct="dzina")
]

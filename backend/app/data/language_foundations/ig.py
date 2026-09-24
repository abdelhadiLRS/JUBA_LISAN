"""Igbo foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

CURRICULUM={
 "A1":[
CurriculumUnit(id="ig-a1-unit-1",level="A1",unit_number=1,title="Igbo: greetings",grammar_points=["ig-a1-g1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ndewo in a basic exchange","Understand a short greetings interaction"],default_weeks=1),
CurriculumUnit(id="ig-a1-unit-2",level="A1",unit_number=2,title="Igbo: identity",grammar_points=["ig-a1-g2"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use aha in a basic exchange","Understand a short identity interaction"],default_weeks=1),
CurriculumUnit(id="ig-a1-unit-3",level="A1",unit_number=3,title="Igbo: family",grammar_points=["ig-a1-g3"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use nne in a basic exchange","Understand a short family interaction"],default_weeks=1),
CurriculumUnit(id="ig-a1-unit-4",level="A1",unit_number=4,title="Igbo: home",grammar_points=["ig-a1-g4"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ụlọ in a basic exchange","Understand a short home interaction"],default_weeks=1),
CurriculumUnit(id="ig-a1-unit-5",level="A1",unit_number=5,title="Igbo: routine",grammar_points=["ig-a1-g5"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ịmụ ihe in a basic exchange","Understand a short routine interaction"],default_weeks=1),
CurriculumUnit(id="ig-a1-unit-6",level="A1",unit_number=6,title="Igbo: time",grammar_points=["ig-a1-g6"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use oge in a basic exchange","Understand a short time interaction"],default_weeks=1),
CurriculumUnit(id="ig-a1-unit-7",level="A1",unit_number=7,title="Igbo: food",grammar_points=["ig-a1-g7"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use mmiri in a basic exchange","Understand a short food interaction"],default_weeks=1),
CurriculumUnit(id="ig-a1-unit-8",level="A1",unit_number=8,title="Igbo: places",grammar_points=["ig-a1-g8"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ụlọ akwụkwọ in a basic exchange","Understand a short places interaction"],default_weeks=1)
 ]
}
for level in LEVELS[1:]:
 CURRICULUM[level]=[CurriculumUnit(id=f"ig-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Igbo {level} communication",grammar_points=["intermediate grammar"],vocabulary_set_ids=[],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Handle extended communication"],default_weeks=2)]

GRAMMAR_TOPICS=[
GrammarTopic(slug="ig-a1-g1",title="Personal pronouns",level="A1",category="grammar",summary="Use common subject pronouns.",explanation="Use common subject pronouns.",examples=[GrammarExample(text="A bụ nwa akwụkwọ.")]),
GrammarTopic(slug="ig-a1-g2",title="Copula",level="A1",category="grammar",summary="Identify people and things.",explanation="Identify people and things.",examples=[GrammarExample(text="Ọ bụ onye nkuzi.")]),
GrammarTopic(slug="ig-a1-g3",title="Present tense",level="A1",category="grammar",summary="Describe current actions.",explanation="Describe current actions.",examples=[GrammarExample(text="Ana m amụ ihe.")]),
GrammarTopic(slug="ig-a1-g4",title="Negation",level="A1",category="grammar",summary="Make simple negative statements.",explanation="Make simple negative statements.",examples=[GrammarExample(text="Adịghị m ebe a.")]),
GrammarTopic(slug="ig-a1-g5",title="Questions",level="A1",category="grammar",summary="Ask basic information questions.",explanation="Ask basic information questions.",examples=[GrammarExample(text="Ebee ka ị nọ?")]),
GrammarTopic(slug="ig-a1-g6",title="Possession",level="A1",category="grammar",summary="Express ownership.",explanation="Express ownership.",examples=[GrammarExample(text="Akwụkwọ m.")]),
GrammarTopic(slug="ig-a1-g7",title="Locatives",level="A1",category="grammar",summary="Say where someone is.",explanation="Say where someone is.",examples=[GrammarExample(text="Anọ m n'ụlọ.")]),
GrammarTopic(slug="ig-a1-g8",title="Plural nouns",level="A1",category="grammar",summary="Recognize common plural patterns.",explanation="Recognize common plural patterns.",examples=[GrammarExample(text="onye / ndị mmadụ")])
]
VOCABULARY_SETS=[
VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="ig-a1-unit-1",words=[VocabularyEntry(word="ndewo",pos="noun",definition="hello",example="Ndewo, kedu?")]),
VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="ig-a1-unit-2",words=[VocabularyEntry(word="aha",pos="noun",definition="name",example="Aha m bụ Chika.")]),
VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="ig-a1-unit-3",words=[VocabularyEntry(word="nne",pos="noun",definition="mother",example="Nne m nọ n'ụlọ.")]),
VocabularySet(id="home_a1",level="A1",topic="home",unit_ref="ig-a1-unit-4",words=[VocabularyEntry(word="ụlọ",pos="noun",definition="house",example="Ụlọ anyị dị mma.")]),
VocabularySet(id="routine_a1",level="A1",topic="routine",unit_ref="ig-a1-unit-5",words=[VocabularyEntry(word="ịmụ ihe",pos="noun",definition="to study",example="Ana m amụ ihe.")]),
VocabularySet(id="time_a1",level="A1",topic="time",unit_ref="ig-a1-unit-6",words=[VocabularyEntry(word="oge",pos="noun",definition="time",example="Olee oge?")]),
VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="ig-a1-unit-7",words=[VocabularyEntry(word="mmiri",pos="noun",definition="water",example="Achọrọ m mmiri.")]),
VocabularySet(id="places_a1",level="A1",topic="places",unit_ref="ig-a1-unit-8",words=[VocabularyEntry(word="ụlọ akwụkwọ",pos="noun",definition="school",example="Aga m ụlọ akwụkwọ.")])
]
PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="greetings_a1_1",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="Ndewo.",context="Hello.",register="neutral")]),
PhrasebookCategory(id="greetings_a1_2",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="Daalụ.",context="Thank you.",register="neutral")]),
PhrasebookCategory(id="help_a1_3",level="A1",situation="help",icon="💬",phrases=[PhrasebookEntry(text="Biko nyere m aka.",context="Please help me.",register="neutral")]),
PhrasebookCategory(id="directions_a1_4",level="A1",situation="directions",icon="💬",phrases=[PhrasebookEntry(text="Ebee ka ụlọ akwụkwọ dị?",context="Where is the school?",register="neutral")])
]
ASSESSMENT_BANK=[
AssessmentQuestion(id="ig-a1-001",skill="vocabulary",difficulty="A1",question="Choose the correct Igbo form for A1.",options=["ndewo","aha","nne","ụlọ"],correct="ndewo"),
AssessmentQuestion(id="ig-a1-002",skill="grammar",difficulty="A1",question="Choose the correct Igbo form for A1.",options=["aha","nne","ụlọ","ịmụ ihe"],correct="aha"),
AssessmentQuestion(id="ig-a1-003",skill="reading",difficulty="A1",question="Choose the correct Igbo form for A1.",options=["nne","ụlọ","ịmụ ihe","oge"],correct="nne"),
AssessmentQuestion(id="ig-a1-004",skill="speaking",difficulty="A1",question="Choose the correct Igbo form for A1.",options=["ụlọ","ịmụ ihe","oge","mmiri"],correct="ụlọ"),
AssessmentQuestion(id="ig-a1-005",skill="vocabulary",difficulty="A1",question="Choose the correct Igbo form for A1.",options=["ịmụ ihe","oge","mmiri","ụlọ akwụkwọ"],correct="ịmụ ihe"),
AssessmentQuestion(id="ig-a1-006",skill="grammar",difficulty="A1",question="Choose the correct Igbo form for A1.",options=["oge","mmiri","ụlọ akwụkwọ","ndewo"],correct="oge"),
AssessmentQuestion(id="ig-a1-007",skill="reading",difficulty="A1",question="Choose the correct Igbo form for A1.",options=["mmiri","ụlọ akwụkwọ","ndewo","aha"],correct="mmiri"),
AssessmentQuestion(id="ig-a1-008",skill="speaking",difficulty="A1",question="Choose the correct Igbo form for A1.",options=["ụlọ akwụkwọ","ndewo","aha","nne"],correct="ụlọ akwụkwọ"),
AssessmentQuestion(id="ig-a1-009",skill="vocabulary",difficulty="A1",question="Choose the correct Igbo form for A1.",options=["ndewo","aha","nne","ụlọ"],correct="ndewo"),
AssessmentQuestion(id="ig-a1-010",skill="grammar",difficulty="A1",question="Choose the correct Igbo form for A1.",options=["aha","nne","ụlọ","ịmụ ihe"],correct="aha")
]

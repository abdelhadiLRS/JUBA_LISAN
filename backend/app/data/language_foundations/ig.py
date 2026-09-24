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
PhrasebookCategory(id="ig-greetings-a1",level="A1",situation="greetings",icon="👋",phrases=[PhrasebookEntry(text="Ndewo.",context="Hello.",register="neutral"),PhrasebookEntry(text="Kedu?",context="How are you?",register="neutral"),PhrasebookEntry(text="Ọ dị mma.",context="I am fine / It is good.",register="neutral")]),
PhrasebookCategory(id="ig-thanks-a1",level="A1",situation="thanks",icon="🙏",phrases=[PhrasebookEntry(text="Daalụ.",context="Thank you.",register="neutral"),PhrasebookEntry(text="Daalụ nke ukwuu.",context="Thank you very much.",register="neutral"),PhrasebookEntry(text="Ọ dịghị ihe.",context="You're welcome / It's nothing.",register="neutral")]),
PhrasebookCategory(id="ig-shopping-a1",level="A1",situation="shopping",icon="🛒",phrases=[PhrasebookEntry(text="Ego ole ka nke a bụ?",context="How much is this?",register="neutral"),PhrasebookEntry(text="Achọrọ m nke a.",context="I want this.",register="neutral"),PhrasebookEntry(text="Biko, belata ọnụ ahịa ya.",context="Please reduce the price.",register="polite")]),
PhrasebookCategory(id="ig-help-a1",level="A1",situation="help",icon="🆘",phrases=[PhrasebookEntry(text="Biko nyere m aka.",context="Please help me.",register="polite"),PhrasebookEntry(text="Aghọtaghị m.",context="I don't understand.",register="neutral"),PhrasebookEntry(text="Biko kwuo ya ọzọ.",context="Please say it again.",register="polite")])
]
ASSESSMENT_BANK=[
AssessmentQuestion(id="ig-a1-001",skill="communication",difficulty="A1",question="You meet someone. Which Igbo phrase means “Hello”?",options=["Ndewo.","Daalụ.","Ego ole ka nke a bụ?","Aghọtaghị m."],correct="Ndewo."),
AssessmentQuestion(id="ig-a1-002",skill="communication",difficulty="A1",question="Which phrase asks “How are you?”",options=["Kedu?","Ọ dị mma.","Achọrọ m nke a.","Daalụ."],correct="Kedu?"),
AssessmentQuestion(id="ig-a1-003",skill="vocabulary",difficulty="A1",question="Which phrase means “Thank you”?",options=["Daalụ.","Ndewo.","Ọ dịghị ihe.","Biko nyere m aka."],correct="Daalụ."),
AssessmentQuestion(id="ig-a1-004",skill="shopping",difficulty="A1",question="At a shop, how do you ask “How much is this?”",options=["Ego ole ka nke a bụ?","Aghọtaghị m.","Ọ dị mma.","Daalụ."],correct="Ego ole ka nke a bụ?"),
AssessmentQuestion(id="ig-a1-005",skill="shopping",difficulty="A1",question="Which phrase means “I want this”?",options=["Achọrọ m nke a.","Ndewo.","Ọ dịghị ihe.","Kedu?"],correct="Achọrọ m nke a."),
AssessmentQuestion(id="ig-a1-006",skill="help",difficulty="A1",question="Which phrase means “Please help me”?",options=["Biko nyere m aka.","Daalụ.","Ego ole ka nke a bụ?","Ọ dị mma."],correct="Biko nyere m aka."),
AssessmentQuestion(id="ig-a1-007",skill="communication",difficulty="A1",question="You do not understand. Which phrase should you use?",options=["Aghọtaghị m.","Ndewo.","Achọrọ m nke a.","Daalụ nke ukwuu."],correct="Aghọtaghị m."),
AssessmentQuestion(id="ig-a1-008",skill="communication",difficulty="A1",question="Which phrase asks someone to repeat what they said?",options=["Biko kwuo ya ọzọ.","Ọ dịghị ihe.","Ego ole ka nke a bụ?","Ọ dị mma."],correct="Biko kwuo ya ọzọ."),
AssessmentQuestion(id="ig-a1-009",skill="politeness",difficulty="A1",question="Someone thanks you. Which phrase can mean “You're welcome / It's nothing”?",options=["Ọ dịghị ihe.","Ndewo.","Kedu?","Achọrọ m nke a."],correct="Ọ dịghị ihe."),
AssessmentQuestion(id="ig-a1-010",skill="communication",difficulty="A1",question="Which phrase means “I am fine / It is good”?",options=["Ọ dị mma.","Daalụ nke ukwuu.","Aghọtaghị m.","Ego ole ka nke a bụ?"],correct="Ọ dị mma.")
]

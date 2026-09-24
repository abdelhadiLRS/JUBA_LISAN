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
PhrasebookCategory(id="rw-greetings-a1",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="Muraho.",context="Hello.",register="neutral"),PhrasebookEntry(text="Amakuru?",context="How are you?",register="neutral"),PhrasebookEntry(text="Ni meza, murakoze.",context="Fine, thank you.",register="neutral")]),
PhrasebookCategory(id="rw-thanks-a1",level="A1",situation="thanks",icon="🙏",phrases=[PhrasebookEntry(text="Murakoze.",context="Thank you.",register="neutral"),PhrasebookEntry(text="Murakoze cyane.",context="Thank you very much.",register="neutral"),PhrasebookEntry(text="Nta kibazo.",context="No problem.",register="neutral")]),
PhrasebookCategory(id="rw-shopping-a1",level="A1",situation="shopping",icon="🛒",phrases=[PhrasebookEntry(text="Ibi ni angahe?",context="How much is this?",register="neutral"),PhrasebookEntry(text="Ndashaka ibi.",context="I want this.",register="neutral"),PhrasebookEntry(text="Mpa ibi, ndakwinginze.",context="Please give me this.",register="polite")]),
PhrasebookCategory(id="rw-help-a1",level="A1",situation="help",icon="🆘",phrases=[PhrasebookEntry(text="Mwamfasha, ndakwinginze?",context="Could you help me, please?",register="polite"),PhrasebookEntry(text="Sinumva.",context="I don't understand / I can't hear.",register="neutral"),PhrasebookEntry(text="Subiramo, ndakwinginze.",context="Please say it again.",register="polite")])
]
ASSESSMENT_BANK=[
AssessmentQuestion(id="rw-a1-001",skill="communication",difficulty="A1",question="You meet someone. Which Kinyarwanda phrase means “Hello”?",options=["Muraho.","Murakoze.","Ibi ni angahe?","Sinumva."],correct="Muraho."),
AssessmentQuestion(id="rw-a1-002",skill="communication",difficulty="A1",question="Which phrase asks “How are you?”",options=["Amakuru?","Ni meza, murakoze.","Ndashaka ibi.","Murakoze."],correct="Amakuru?"),
AssessmentQuestion(id="rw-a1-003",skill="vocabulary",difficulty="A1",question="Which phrase means “Thank you”?",options=["Murakoze.","Muraho.","Nta kibazo.","Mwamfasha, ndakwinginze?"],correct="Murakoze."),
AssessmentQuestion(id="rw-a1-004",skill="shopping",difficulty="A1",question="At a shop, how do you ask “How much is this?”",options=["Ibi ni angahe?","Sinumva.","Ni meza, murakoze.","Murakoze."],correct="Ibi ni angahe?"),
AssessmentQuestion(id="rw-a1-005",skill="shopping",difficulty="A1",question="Which phrase means “I want this”?",options=["Ndashaka ibi.","Muraho.","Nta kibazo.","Amakuru?"],correct="Ndashaka ibi."),
AssessmentQuestion(id="rw-a1-006",skill="help",difficulty="A1",question="Which phrase politely asks for help?",options=["Mwamfasha, ndakwinginze?","Murakoze.","Ibi ni angahe?","Ni meza, murakoze."],correct="Mwamfasha, ndakwinginze?"),
AssessmentQuestion(id="rw-a1-007",skill="communication",difficulty="A1",question="You do not understand. Which phrase should you use?",options=["Sinumva.","Muraho.","Ndashaka ibi.","Murakoze cyane."],correct="Sinumva."),
AssessmentQuestion(id="rw-a1-008",skill="communication",difficulty="A1",question="Which phrase asks someone to repeat?",options=["Subiramo, ndakwinginze.","Nta kibazo.","Ibi ni angahe?","Ni meza, murakoze."],correct="Subiramo, ndakwinginze."),
AssessmentQuestion(id="rw-a1-009",skill="politeness",difficulty="A1",question="Which phrase means “No problem”?",options=["Nta kibazo.","Muraho.","Amakuru?","Ndashaka ibi."],correct="Nta kibazo."),
AssessmentQuestion(id="rw-a1-010",skill="communication",difficulty="A1",question="Which phrase means “Fine, thank you”?",options=["Ni meza, murakoze.","Murakoze cyane.","Sinumva.","Ibi ni angahe?"],correct="Ni meza, murakoze.")
]

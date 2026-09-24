"""Southern Sotho foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion
LEVELS=["A1","A2","B1","B2","C1","C2"]
CURRICULUM={"A1":[
CurriculumUnit(id="st-a1-unit-1",level="A1",unit_number=1,title="Southern Sotho: greetings",grammar_points=["st-a1-g1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use lumela in a basic exchange","Understand a short greetings interaction"],default_weeks=1),
CurriculumUnit(id="st-a1-unit-2",level="A1",unit_number=2,title="Southern Sotho: identity",grammar_points=["st-a1-g2"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use lebitso in a basic exchange","Understand a short identity interaction"],default_weeks=1),
CurriculumUnit(id="st-a1-unit-3",level="A1",unit_number=3,title="Southern Sotho: family",grammar_points=["st-a1-g3"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use mme in a basic exchange","Understand a short family interaction"],default_weeks=1),
CurriculumUnit(id="st-a1-unit-4",level="A1",unit_number=4,title="Southern Sotho: home",grammar_points=["st-a1-g4"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ntlo in a basic exchange","Understand a short home interaction"],default_weeks=1),
CurriculumUnit(id="st-a1-unit-5",level="A1",unit_number=5,title="Southern Sotho: routine",grammar_points=["st-a1-g5"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ithuta in a basic exchange","Understand a short routine interaction"],default_weeks=1),
CurriculumUnit(id="st-a1-unit-6",level="A1",unit_number=6,title="Southern Sotho: time",grammar_points=["st-a1-g6"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use nako in a basic exchange","Understand a short time interaction"],default_weeks=1),
CurriculumUnit(id="st-a1-unit-7",level="A1",unit_number=7,title="Southern Sotho: food",grammar_points=["st-a1-g7"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use metsi in a basic exchange","Understand a short food interaction"],default_weeks=1),
CurriculumUnit(id="st-a1-unit-8",level="A1",unit_number=8,title="Southern Sotho: places",grammar_points=["st-a1-g8"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use sekolo in a basic exchange","Understand a short places interaction"],default_weeks=1)
]}
for level in LEVELS[1:]:
 CURRICULUM[level]=[CurriculumUnit(id=f"st-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Southern Sotho {level} communication",grammar_points=["intermediate grammar"],vocabulary_set_ids=[],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Handle extended communication"],default_weeks=2)]
GRAMMAR_TOPICS=[
GrammarTopic(slug="st-a1-g1",title="Pronouns",level="A1",category="grammar",summary="Use pronouns in basic communication.",explanation="Practice pronouns through short everyday exchanges.",examples=[GrammarExample(text="Ke moithuti.")]),
GrammarTopic(slug="st-a1-g2",title="Copula",level="A1",category="grammar",summary="Use copula in basic communication.",explanation="Practice copula through short everyday exchanges.",examples=[GrammarExample(text="Ke tichere.")]),
GrammarTopic(slug="st-a1-g3",title="Present",level="A1",category="grammar",summary="Use present in basic communication.",explanation="Practice present through short everyday exchanges.",examples=[GrammarExample(text="Ke a ithuta.")]),
GrammarTopic(slug="st-a1-g4",title="Negation",level="A1",category="grammar",summary="Use negation in basic communication.",explanation="Practice negation through short everyday exchanges.",examples=[GrammarExample(text="Ha ke tsebe.")]),
GrammarTopic(slug="st-a1-g5",title="Questions",level="A1",category="grammar",summary="Use questions in basic communication.",explanation="Practice questions through short everyday exchanges.",examples=[GrammarExample(text="U hokae?")]),
GrammarTopic(slug="st-a1-g6",title="Possession",level="A1",category="grammar",summary="Use possession in basic communication.",explanation="Practice possession through short everyday exchanges.",examples=[GrammarExample(text="Ena ke buka ea ka.")]),
GrammarTopic(slug="st-a1-g7",title="Locative",level="A1",category="grammar",summary="Use locative in basic communication.",explanation="Practice locative through short everyday exchanges.",examples=[GrammarExample(text="Ke lapeng.")]),
GrammarTopic(slug="st-a1-g8",title="Plural",level="A1",category="grammar",summary="Use plural in basic communication.",explanation="Practice plural through short everyday exchanges.",examples=[GrammarExample(text="Batho ba teng.")])
]
VOCABULARY_SETS=[
VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="st-a1-unit-1",words=[VocabularyEntry(word="lumela",pos="noun",definition="hello",example="Lumela, ntate.")]),
VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="st-a1-unit-2",words=[VocabularyEntry(word="lebitso",pos="noun",definition="name",example="Lebitso la ka ke Thabo.")]),
VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="st-a1-unit-3",words=[VocabularyEntry(word="mme",pos="noun",definition="mother",example="Mme o lapeng.")]),
VocabularySet(id="home_a1",level="A1",topic="home",unit_ref="st-a1-unit-4",words=[VocabularyEntry(word="ntlo",pos="noun",definition="house",example="Ntlo e kholo.")]),
VocabularySet(id="routine_a1",level="A1",topic="routine",unit_ref="st-a1-unit-5",words=[VocabularyEntry(word="ithuta",pos="noun",definition="study",example="Ke ithuta letsatsi le leng le le leng.")]),
VocabularySet(id="time_a1",level="A1",topic="time",unit_ref="st-a1-unit-6",words=[VocabularyEntry(word="nako",pos="noun",definition="time",example="Ke nako mang?")]),
VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="st-a1-unit-7",words=[VocabularyEntry(word="metsi",pos="noun",definition="water",example="Ke batla metsi.")]),
VocabularySet(id="places_a1",level="A1",topic="places",unit_ref="st-a1-unit-8",words=[VocabularyEntry(word="sekolo",pos="noun",definition="school",example="Ke sekolong.")])
]
PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="st_a1_phrase_1",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="Lumela.",context="Hello.",register="neutral")]),
PhrasebookCategory(id="st_a1_phrase_2",level="A1",situation="thanks",icon="💬",phrases=[PhrasebookEntry(text="Kea leboha.",context="Thank you.",register="neutral")]),
PhrasebookCategory(id="st_a1_phrase_3",level="A1",situation="help",icon="💬",phrases=[PhrasebookEntry(text="Nthuse ka kopo.",context="Please help me.",register="neutral")]),
PhrasebookCategory(id="st_a1_phrase_4",level="A1",situation="directions",icon="💬",phrases=[PhrasebookEntry(text="Sekolo se hokae?",context="Where is the school?",register="neutral")])
]
ASSESSMENT_BANK=[
AssessmentQuestion(id="st-a1-001",skill="vocabulary",difficulty="A1",question="You want to greet someone. Which Southern Sotho phrase should you use?",options=["Lumela.","Kea leboha.","Nthuse ka kopo.","Sekolo se hokae?"],correct="Lumela."),
AssessmentQuestion(id="st-a1-002",skill="grammar",difficulty="A1",question="You introduce yourself by saying your name is Thabo. Which sentence is correct?",options=["Lebitso la ka ke Thabo.","Mme o lapeng.","Ke batla metsi.","Sekolo se hokae?"],correct="Lebitso la ka ke Thabo."),
AssessmentQuestion(id="st-a1-003",skill="vocabulary",difficulty="A1",question="You are talking about your mother. Which Southern Sotho word means mother?",options=["mme","ntlo","nako","metsi"],correct="mme"),
AssessmentQuestion(id="st-a1-004",skill="vocabulary",difficulty="A1",question="You are thirsty and want water. Which word means water?",options=["metsi","ntlo","sekolo","lebitso"],correct="metsi"),
AssessmentQuestion(id="st-a1-005",skill="reading",difficulty="A1",question="Buka e holim'a tafole. Where is the book?",options=["On the table","At school","At home","In the shop"],correct="On the table"),
AssessmentQuestion(id="st-a1-006",skill="vocabulary",difficulty="A1",question="You ask what time it is. Which Southern Sotho word means time?",options=["nako","metsi","mme","ntlo"],correct="nako"),
AssessmentQuestion(id="st-a1-007",skill="communication",difficulty="A1",question="You need help. Which Southern Sotho phrase should you use?",options=["Nthuse ka kopo.","Lumela.","Kea leboha.","Sekolo se hokae?"],correct="Nthuse ka kopo."),
AssessmentQuestion(id="st-a1-008",skill="communication",difficulty="A1",question="You want to ask where the school is. Which phrase should you use?",options=["Sekolo se hokae?","Kea leboha.","Lumela.","Metsi."],correct="Sekolo se hokae?"),
AssessmentQuestion(id="st-a1-009",skill="communication",difficulty="A1",question="Someone helps you. What do you say to thank them?",options=["Kea leboha.","Lumela.","Nthuse ka kopo.","Sekolo se hokae?"],correct="Kea leboha."),
AssessmentQuestion(id="st-a1-010",skill="vocabulary",difficulty="A1",question="You are going to school. Which Southern Sotho word means school?",options=["sekolo","metsi","nako","mme"],correct="sekolo")
]

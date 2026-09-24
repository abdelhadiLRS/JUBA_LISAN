"""Shona foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion
LEVELS=["A1","A2","B1","B2","C1","C2"]
CURRICULUM={"A1":[
CurriculumUnit(id="sn-a1-unit-1",level="A1",unit_number=1,title="Shona: greetings",grammar_points=["sn-a1-g1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use mhoro in a basic exchange","Understand a short greetings interaction"],default_weeks=1),
CurriculumUnit(id="sn-a1-unit-2",level="A1",unit_number=2,title="Shona: identity",grammar_points=["sn-a1-g2"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use zita in a basic exchange","Understand a short identity interaction"],default_weeks=1),
CurriculumUnit(id="sn-a1-unit-3",level="A1",unit_number=3,title="Shona: family",grammar_points=["sn-a1-g3"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use amai in a basic exchange","Understand a short family interaction"],default_weeks=1),
CurriculumUnit(id="sn-a1-unit-4",level="A1",unit_number=4,title="Shona: home",grammar_points=["sn-a1-g4"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use imba in a basic exchange","Understand a short home interaction"],default_weeks=1),
CurriculumUnit(id="sn-a1-unit-5",level="A1",unit_number=5,title="Shona: routine",grammar_points=["sn-a1-g5"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use kudzidza in a basic exchange","Understand a short routine interaction"],default_weeks=1),
CurriculumUnit(id="sn-a1-unit-6",level="A1",unit_number=6,title="Shona: time",grammar_points=["sn-a1-g6"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use nguva in a basic exchange","Understand a short time interaction"],default_weeks=1),
CurriculumUnit(id="sn-a1-unit-7",level="A1",unit_number=7,title="Shona: food",grammar_points=["sn-a1-g7"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use mvura in a basic exchange","Understand a short food interaction"],default_weeks=1),
CurriculumUnit(id="sn-a1-unit-8",level="A1",unit_number=8,title="Shona: places",grammar_points=["sn-a1-g8"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use chikoro in a basic exchange","Understand a short places interaction"],default_weeks=1)
]}
for level in LEVELS[1:]:
 CURRICULUM[level]=[CurriculumUnit(id=f"sn-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Shona {level} communication",grammar_points=["intermediate grammar"],vocabulary_set_ids=[],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Handle extended communication"],default_weeks=2)]
GRAMMAR_TOPICS=[
GrammarTopic(slug="sn-a1-g1",title="Pronouns",level="A1",category="grammar",summary="Use pronouns in basic communication.",explanation="Practice pronouns through short everyday exchanges.",examples=[GrammarExample(text="Mau ndi...")]),
GrammarTopic(slug="sn-a1-g2",title="Copula",level="A1",category="grammar",summary="Use copula in basic communication.",explanation="Practice copula through short everyday exchanges.",examples=[GrammarExample(text="Ndiri mudzidzi.")]),
GrammarTopic(slug="sn-a1-g3",title="Present",level="A1",category="grammar",summary="Use present in basic communication.",explanation="Practice present through short everyday exchanges.",examples=[GrammarExample(text="Ndinodzidza.")]),
GrammarTopic(slug="sn-a1-g4",title="Negation",level="A1",category="grammar",summary="Use negation in basic communication.",explanation="Practice negation through short everyday exchanges.",examples=[GrammarExample(text="Handisi kumba.")]),
GrammarTopic(slug="sn-a1-g5",title="Questions",level="A1",category="grammar",summary="Use questions in basic communication.",explanation="Practice questions through short everyday exchanges.",examples=[GrammarExample(text="Uri kupi?")]),
GrammarTopic(slug="sn-a1-g6",title="Possession",level="A1",category="grammar",summary="Use possession in basic communication.",explanation="Practice possession through short everyday exchanges.",examples=[GrammarExample(text="Iri ibhuku rangu.")]),
GrammarTopic(slug="sn-a1-g7",title="Locative",level="A1",category="grammar",summary="Use locative in basic communication.",explanation="Practice locative through short everyday exchanges.",examples=[GrammarExample(text="Ndiri kumba.")]),
GrammarTopic(slug="sn-a1-g8",title="Plural",level="A1",category="grammar",summary="Use plural in basic communication.",explanation="Practice plural through short everyday exchanges.",examples=[GrammarExample(text="Vanhu vari pano.")])
]
VOCABULARY_SETS=[
VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="sn-a1-unit-1",words=[VocabularyEntry(word="mhoro",pos="noun",definition="hello",example="Mhoro, shamwari.")]),
VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="sn-a1-unit-2",words=[VocabularyEntry(word="zita",pos="noun",definition="name",example="Zita rangu ndiTariro.")]),
VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="sn-a1-unit-3",words=[VocabularyEntry(word="amai",pos="noun",definition="mother",example="Amai vari kumba.")]),
VocabularySet(id="home_a1",level="A1",topic="home",unit_ref="sn-a1-unit-4",words=[VocabularyEntry(word="imba",pos="noun",definition="house",example="Imba yedu yakakura.")]),
VocabularySet(id="routine_a1",level="A1",topic="routine",unit_ref="sn-a1-unit-5",words=[VocabularyEntry(word="kudzidza",pos="noun",definition="study",example="Ndinodzidza mangwanani.")]),
VocabularySet(id="time_a1",level="A1",topic="time",unit_ref="sn-a1-unit-6",words=[VocabularyEntry(word="nguva",pos="noun",definition="time",example="Inguvai?")]),
VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="sn-a1-unit-7",words=[VocabularyEntry(word="mvura",pos="noun",definition="water",example="Ndinoda mvura.")]),
VocabularySet(id="places_a1",level="A1",topic="places",unit_ref="sn-a1-unit-8",words=[VocabularyEntry(word="chikoro",pos="noun",definition="school",example="Ndiri kuchikoro.")])
]
PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="sn_a1_phrase_1",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="Mhoro.",context="Hello.",register="neutral")]),
PhrasebookCategory(id="sn_a1_phrase_2",level="A1",situation="thanks",icon="💬",phrases=[PhrasebookEntry(text="Ndatenda.",context="Thank you.",register="neutral")]),
PhrasebookCategory(id="sn_a1_phrase_3",level="A1",situation="help",icon="💬",phrases=[PhrasebookEntry(text="Ndibatsirei.",context="Please help me.",register="neutral")]),
PhrasebookCategory(id="sn_a1_phrase_4",level="A1",situation="directions",icon="💬",phrases=[PhrasebookEntry(text="Chikoro chiri kupi?",context="Where is the school?",register="neutral")])
]
ASSESSMENT_BANK=[
AssessmentQuestion(id="sn-a1-001",skill="vocabulary",difficulty="A1",question="Choose the correct Shona expression for this A1 task.",options=["mhoro","zita","amai","imba"],correct="mhoro"),
AssessmentQuestion(id="sn-a1-002",skill="grammar",difficulty="A1",question="Choose the correct Shona expression for this A1 task.",options=["zita","amai","imba","kudzidza"],correct="zita"),
AssessmentQuestion(id="sn-a1-003",skill="reading",difficulty="A1",question="Choose the correct Shona expression for this A1 task.",options=["amai","imba","kudzidza","nguva"],correct="amai"),
AssessmentQuestion(id="sn-a1-004",skill="speaking",difficulty="A1",question="Choose the correct Shona expression for this A1 task.",options=["imba","kudzidza","nguva","mvura"],correct="imba"),
AssessmentQuestion(id="sn-a1-005",skill="vocabulary",difficulty="A1",question="Choose the correct Shona expression for this A1 task.",options=["kudzidza","nguva","mvura","chikoro"],correct="kudzidza"),
AssessmentQuestion(id="sn-a1-006",skill="grammar",difficulty="A1",question="Choose the correct Shona expression for this A1 task.",options=["nguva","mvura","chikoro","mhoro"],correct="nguva"),
AssessmentQuestion(id="sn-a1-007",skill="reading",difficulty="A1",question="Choose the correct Shona expression for this A1 task.",options=["mvura","chikoro","mhoro","zita"],correct="mvura"),
AssessmentQuestion(id="sn-a1-008",skill="speaking",difficulty="A1",question="Choose the correct Shona expression for this A1 task.",options=["chikoro","mhoro","zita","amai"],correct="chikoro"),
AssessmentQuestion(id="sn-a1-009",skill="vocabulary",difficulty="A1",question="Choose the correct Shona expression for this A1 task.",options=["mhoro","zita","amai","imba"],correct="mhoro"),
AssessmentQuestion(id="sn-a1-010",skill="grammar",difficulty="A1",question="Choose the correct Shona expression for this A1 task.",options=["zita","amai","imba","kudzidza"],correct="zita")
]

"""Xhosa foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

CURRICULUM={
 "A1":[
CurriculumUnit(id="xh-a1-unit-1",level="A1",unit_number=1,title="Xhosa: greetings",grammar_points=["xh-a1-g1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use Molo in a basic exchange","Understand a short greetings interaction"],default_weeks=1),
CurriculumUnit(id="xh-a1-unit-2",level="A1",unit_number=2,title="Xhosa: identity",grammar_points=["xh-a1-g2"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use igama in a basic exchange","Understand a short identity interaction"],default_weeks=1),
CurriculumUnit(id="xh-a1-unit-3",level="A1",unit_number=3,title="Xhosa: family",grammar_points=["xh-a1-g3"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use umama in a basic exchange","Understand a short family interaction"],default_weeks=1),
CurriculumUnit(id="xh-a1-unit-4",level="A1",unit_number=4,title="Xhosa: home",grammar_points=["xh-a1-g4"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use indlu in a basic exchange","Understand a short home interaction"],default_weeks=1),
CurriculumUnit(id="xh-a1-unit-5",level="A1",unit_number=5,title="Xhosa: routine",grammar_points=["xh-a1-g5"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ukufunda in a basic exchange","Understand a short routine interaction"],default_weeks=1),
CurriculumUnit(id="xh-a1-unit-6",level="A1",unit_number=6,title="Xhosa: time",grammar_points=["xh-a1-g6"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ixesha in a basic exchange","Understand a short time interaction"],default_weeks=1),
CurriculumUnit(id="xh-a1-unit-7",level="A1",unit_number=7,title="Xhosa: food",grammar_points=["xh-a1-g7"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ukutya in a basic exchange","Understand a short food interaction"],default_weeks=1),
CurriculumUnit(id="xh-a1-unit-8",level="A1",unit_number=8,title="Xhosa: places",grammar_points=["xh-a1-g8"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use idolophu in a basic exchange","Understand a short places interaction"],default_weeks=1)
 ]
}
for level in LEVELS[1:]:
 CURRICULUM[level]=[CurriculumUnit(id=f"xh-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Xhosa {level} communication",grammar_points=["intermediate grammar"],vocabulary_set_ids=[],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Handle extended communication"],default_weeks=2)]

GRAMMAR_TOPICS=[
GrammarTopic(slug="xh-a1-g1",title="Personal pronouns",level="A1",category="grammar",summary="Use basic subject pronouns.",explanation="Use basic subject pronouns.",examples=[GrammarExample(text="Mna ndingu... / Wena ungu...")]),
GrammarTopic(slug="xh-a1-g2",title="Copulative identity",level="A1",category="grammar",summary="Identify people and things.",explanation="Identify people and things.",examples=[GrammarExample(text="Lo ngumfundisi.")]),
GrammarTopic(slug="xh-a1-g3",title="Present tense",level="A1",category="grammar",summary="Describe current actions.",explanation="Describe current actions.",examples=[GrammarExample(text="Ndiyafunda.")]),
GrammarTopic(slug="xh-a1-g4",title="Negation",level="A1",category="grammar",summary="Make simple negative statements.",explanation="Make simple negative statements.",examples=[GrammarExample(text="Andifundi.")]),
GrammarTopic(slug="xh-a1-g5",title="Question forms",level="A1",category="grammar",summary="Ask who, what, where and yes/no questions.",explanation="Ask who, what, where and yes/no questions.",examples=[GrammarExample(text="Uphi? / Ngubani lo?")]),
GrammarTopic(slug="xh-a1-g6",title="Possessive forms",level="A1",category="grammar",summary="Express ownership and relationships.",explanation="Express ownership and relationships.",examples=[GrammarExample(text="Le yincwadi yam.")]),
GrammarTopic(slug="xh-a1-g7",title="Locative basics",level="A1",category="grammar",summary="Say where people and things are.",explanation="Say where people and things are.",examples=[GrammarExample(text="Usekhaya.")]),
GrammarTopic(slug="xh-a1-g8",title="Plural nouns",level="A1",category="grammar",summary="Recognize common singular/plural noun patterns.",explanation="Recognize common singular/plural noun patterns.",examples=[GrammarExample(text="umntu / abantu")])
]
VOCABULARY_SETS=[
VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="xh-a1-unit-1",words=[VocabularyEntry(word="Molo",pos="noun",definition="hello",example="Molo, Tata.")]),
VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="xh-a1-unit-2",words=[VocabularyEntry(word="igama",pos="noun",definition="name",example="Igama lam nguLwazi.")]),
VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="xh-a1-unit-3",words=[VocabularyEntry(word="umama",pos="noun",definition="mother",example="Umama usekhaya.")]),
VocabularySet(id="home_a1",level="A1",topic="home",unit_ref="xh-a1-unit-4",words=[VocabularyEntry(word="indlu",pos="noun",definition="house",example="Indlu inkulu.")]),
VocabularySet(id="routine_a1",level="A1",topic="routine",unit_ref="xh-a1-unit-5",words=[VocabularyEntry(word="ukufunda",pos="noun",definition="to study",example="Ndiyafunda kusasa.")]),
VocabularySet(id="time_a1",level="A1",topic="time",unit_ref="xh-a1-unit-6",words=[VocabularyEntry(word="ixesha",pos="noun",definition="time",example="Liliphi ixesha?")]),
VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="xh-a1-unit-7",words=[VocabularyEntry(word="ukutya",pos="noun",definition="food",example="Ndifuna ukutya.")]),
VocabularySet(id="places_a1",level="A1",topic="places",unit_ref="xh-a1-unit-8",words=[VocabularyEntry(word="idolophu",pos="noun",definition="town",example="Ndiya edolophini.")])
]
PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="xh-greetings-a1",level="A1",situation="greetings",icon="👋",phrases=[PhrasebookEntry(text="Molo.",context="Hello.",register="neutral"),PhrasebookEntry(text="Unjani?",context="How are you?",register="neutral"),PhrasebookEntry(text="NdinguLwazi.",context="I am Lwazi.",register="neutral")]),
PhrasebookCategory(id="xh-thanks-a1",level="A1",situation="thanks",icon="🙏",phrases=[PhrasebookEntry(text="Enkosi.",context="Thank you.",register="neutral"),PhrasebookEntry(text="Enkosi kakhulu.",context="Thank you very much.",register="neutral"),PhrasebookEntry(text="Wamkelekile.",context="You are welcome.",register="neutral")]),
PhrasebookCategory(id="xh-shopping-a1",level="A1",situation="shopping",icon="🛒",phrases=[PhrasebookEntry(text="Ixabisa malini le?",context="How much does this cost?",register="neutral"),PhrasebookEntry(text="Ndifuna le.",context="I want this one.",register="neutral"),PhrasebookEntry(text="Nceda, yehlisa ixabiso.",context="Please lower the price.",register="neutral")]),
PhrasebookCategory(id="xh-help-a1",level="A1",situation="help",icon="🆘",phrases=[PhrasebookEntry(text="Nceda undincede.",context="Please help me.",register="neutral"),PhrasebookEntry(text="Andiqondi.",context="I do not understand.",register="neutral"),PhrasebookEntry(text="Nceda uphinde.",context="Please repeat.",register="neutral")]),
]
ASSESSMENT_BANK=[
AssessmentQuestion(id="xh-a1-001",skill="communication",difficulty="A1",question="You meet someone. Which Xhosa phrase means “Hello”?",options=["Molo.","Enkosi.","Andiqondi.","Ixabisa malini le?"],correct="Molo."),
AssessmentQuestion(id="xh-a1-002",skill="speaking",difficulty="A1",question="You want to say your name is Lwazi. Which sentence should you use?",options=["NdinguLwazi.","Ndifuna le.","Nceda undincede.","Enkosi kakhulu."],correct="NdinguLwazi."),
AssessmentQuestion(id="xh-a1-003",skill="communication",difficulty="A1",question="Someone helps you. Which phrase means “Thank you very much”?",options=["Enkosi kakhulu.","Unjani?","Andiqondi.","Nceda uphinde."],correct="Enkosi kakhulu."),
AssessmentQuestion(id="xh-a1-004",skill="shopping",difficulty="A1",question="At a shop, how do you ask “How much does this cost?”",options=["Ixabisa malini le?","NdinguLwazi.","Molo.","Nceda undincede."],correct="Ixabisa malini le?"),
AssessmentQuestion(id="xh-a1-005",skill="shopping",difficulty="A1",question="You want one item. Which phrase means “I want this one”?",options=["Ndifuna le.","Wamkelekile.","Unjani?","Andiqondi."],correct="Ndifuna le."),
AssessmentQuestion(id="xh-a1-006",skill="help",difficulty="A1",question="You need assistance. Which phrase asks someone to help you?",options=["Nceda undincede.","Ixabisa malini le?","Enkosi.","NdinguLwazi."],correct="Nceda undincede."),
AssessmentQuestion(id="xh-a1-007",skill="listening",difficulty="A1",question="You did not understand. Which Xhosa phrase should you say?",options=["Andiqondi.","Molo.","Ndifuna le.","Enkosi kakhulu."],correct="Andiqondi."),
AssessmentQuestion(id="xh-a1-008",skill="help",difficulty="A1",question="You want someone to repeat. Which phrase means “Please repeat”?",options=["Nceda uphinde.","Wamkelekile.","Unjani?","Ixabisa malini le?"],correct="Nceda uphinde."),
AssessmentQuestion(id="xh-a1-009",skill="shopping",difficulty="A1",question="You want to ask the seller to lower the price. Which phrase fits?",options=["Nceda, yehlisa ixabiso.","Molo.","NdinguLwazi.","Andiqondi."],correct="Nceda, yehlisa ixabiso."),
AssessmentQuestion(id="xh-a1-010",skill="communication",difficulty="A1",question="Someone thanks you. Which Xhosa response means “You are welcome”?",options=["Wamkelekile.","Ixabisa malini le?","Nceda undincede.","Ndifuna le."],correct="Wamkelekile."),
]

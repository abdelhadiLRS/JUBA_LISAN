"""Haitian Creole A1 deep foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]
GRAMMAR_TOPICS=[
    GrammarTopic(slug="greetings-a1",title="Greetings and introductions",level="A1",category="phrase",summary="Use common greetings in Haitian Creole.",explanation="Use common greetings in Haitian Creole.",examples=[GrammarExample(text="Bonjou")]),
    GrammarTopic(slug="identity-a1",title="Personal identity",level="A1",category="grammar",summary="Build simple first-person identity statements in Haitian Creole.",explanation="Build simple first-person identity statements in Haitian Creole.",examples=[GrammarExample(text="Mwen rele...")]),
    GrammarTopic(slug="family-a1",title="Family and possession",level="A1",category="grammar",summary="Talk about family and simple possession in Haitian Creole.",explanation="Talk about family and simple possession in Haitian Creole.",examples=[GrammarExample(text="fanmi")]),
    GrammarTopic(slug="routine-a1",title="Daily routine",level="A1",category="verb",summary="Use basic present-tense or habitual expressions in Haitian Creole.",explanation="Use basic present-tense or habitual expressions in Haitian Creole.",examples=[GrammarExample(text="mwen ale")]),
    GrammarTopic(slug="time-a1",title="Time and dates",level="A1",category="time",summary="Express basic time and day references in Haitian Creole.",explanation="Express basic time and day references in Haitian Creole.",examples=[GrammarExample(text="jodi a")]),
    GrammarTopic(slug="food-a1",title="Food and needs",level="A1",category="vocabulary",summary="Ask for and identify everyday food and drink in Haitian Creole.",explanation="Ask for and identify everyday food and drink in Haitian Creole.",examples=[GrammarExample(text="dlo")]),
    GrammarTopic(slug="places-a1",title="Places and directions",level="A1",category="syntax",summary="Name places and make simple location statements in Haitian Creole.",explanation="Name places and make simple location statements in Haitian Creole.",examples=[GrammarExample(text="lakay")]),
    GrammarTopic(slug="review-a1",title="A1 review and repair",level="A1",category="discourse",summary="Combine familiar A1 patterns into short exchanges in Haitian Creole.",explanation="Combine familiar A1 patterns into short exchanges in Haitian Creole.",examples=[GrammarExample(text="mèsi")]),
]

VOCABULARY_SETS=[
    VocabularySet(id="saludos_a1",level="A1",topic="Saludos",unit_ref="ht-a1-unit-1",words=[VocabularyEntry(word="Bonjou",pos="phrase",definition="good morning/hello",example="Bonjou")]),
    VocabularySet(id="identidad_a1",level="A1",topic="Identidad",unit_ref="ht-a1-unit-2",words=[VocabularyEntry(word="Mwen rele...",pos="phrase",definition="my name is...",example="Mwen rele...")]),
    VocabularySet(id="familia_a1",level="A1",topic="Familia",unit_ref="ht-a1-unit-3",words=[VocabularyEntry(word="fanmi",pos="phrase",definition="family",example="fanmi")]),
    VocabularySet(id="rutina_a1",level="A1",topic="Rutina",unit_ref="ht-a1-unit-4",words=[VocabularyEntry(word="mwen ale",pos="phrase",definition="I go",example="mwen ale")]),
    VocabularySet(id="tiempo_a1",level="A1",topic="Tiempo",unit_ref="ht-a1-unit-5",words=[VocabularyEntry(word="jodi a",pos="phrase",definition="today",example="jodi a")]),
    VocabularySet(id="comida_a1",level="A1",topic="Comida",unit_ref="ht-a1-unit-6",words=[VocabularyEntry(word="dlo",pos="phrase",definition="water",example="dlo")]),
    VocabularySet(id="lugares_a1",level="A1",topic="Lugares",unit_ref="ht-a1-unit-7",words=[VocabularyEntry(word="lakay",pos="phrase",definition="home",example="lakay")]),
    VocabularySet(id="repaso_a1",level="A1",topic="Repaso",unit_ref="ht-a1-unit-8",words=[VocabularyEntry(word="mèsi",pos="phrase",definition="thank you",example="mèsi")]),
]

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Saludos",icon="👋",phrases=[PhrasebookEntry(text="Bonjou",context="good morning/hello",register="neutral")]),
    PhrasebookCategory(id="identity_a1",level="A1",situation="Identidad",icon="🪪",phrases=[PhrasebookEntry(text="Mwen rele...",context="my name is...",register="neutral")]),
    PhrasebookCategory(id="family_a1",level="A1",situation="Familia",icon="👨‍👩‍👧",phrases=[PhrasebookEntry(text="fanmi",context="family",register="neutral")]),
    PhrasebookCategory(id="routine_a1",level="A1",situation="Rutina",icon="⏰",phrases=[PhrasebookEntry(text="mwen ale",context="I go",register="neutral")]),
]

CURRICULUM={}
for level in LEVELS:
    if level=="A1":
        CURRICULUM[level]=[
            CurriculumUnit(id="ht-a1-unit-1",level="A1",unit_number=1,title="Greetings and introductions",grammar_points=["greetings-a1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-2",level="A1",unit_number=2,title="Personal identity",grammar_points=["identity-a1"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-3",level="A1",unit_number=3,title="Family and possession",grammar_points=["family-a1"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-4",level="A1",unit_number=4,title="Daily routine",grammar_points=["routine-a1"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-5",level="A1",unit_number=5,title="Time and dates",grammar_points=["time-a1"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-6",level="A1",unit_number=6,title="Food and needs",grammar_points=["food-a1"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-7",level="A1",unit_number=7,title="Places and directions",grammar_points=["places-a1"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-8",level="A1",unit_number=8,title="A1 review and repair",grammar_points=["review-a1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
        ]
    else:
        CURRICULUM[level]=[CurriculumUnit(id=f"ht-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Haitian Creole {level} communication",grammar_points=["progressive grammar and communication"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Build level-appropriate communication"],default_weeks=2)]

ASSESSMENT_BANK=[
    AssessmentQuestion(id="ht-a1-001",skill="speaking",difficulty="A1",question="What does Bonjou mean in this lesson?",options=["good morning/hello","family","school","yesterday"],correct="good morning/hello"),
    AssessmentQuestion(id="ht-a1-002",skill="vocabulary",difficulty="A1",question="What does Mwen rele... mean in this lesson?",options=["my name is...","family","school","yesterday"],correct="my name is..."),
    AssessmentQuestion(id="ht-a1-003",skill="grammar",difficulty="A1",question="What does fanmi mean in this lesson?",options=["family","family","school","yesterday"],correct="family"),
    AssessmentQuestion(id="ht-a1-004",skill="speaking",difficulty="A1",question="What does mwen ale mean in this lesson?",options=["I go","family","school","yesterday"],correct="I go"),
    AssessmentQuestion(id="ht-a1-005",skill="vocabulary",difficulty="A1",question="What does jodi a mean in this lesson?",options=["today","family","school","yesterday"],correct="today"),
    AssessmentQuestion(id="ht-a1-006",skill="grammar",difficulty="A1",question="What does dlo mean in this lesson?",options=["water","family","school","yesterday"],correct="water"),
    AssessmentQuestion(id="ht-a1-007",skill="speaking",difficulty="A1",question="What does lakay mean in this lesson?",options=["home","family","school","yesterday"],correct="home"),
    AssessmentQuestion(id="ht-a1-008",skill="vocabulary",difficulty="A1",question="What does mèsi mean in this lesson?",options=["thank you","family","school","yesterday"],correct="thank you"),
    AssessmentQuestion(id="ht-a1-009",skill="reading",difficulty="A1",question="Choose the expression that belongs to an everyday A1 exchange.",options=["Bonjou","B2 academic term","technical formula","rare literary phrase"],correct="Bonjou"),
    AssessmentQuestion(id="ht-a1-010",skill="production",difficulty="A1",question="Choose the expression learners can use to close a polite exchange.",options=["mèsi","technical term","advanced idiom","academic citation"],correct="mèsi"),
]

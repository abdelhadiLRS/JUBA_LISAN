"""Nahuatl A1 deep foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]
GRAMMAR_TOPICS=[
    GrammarTopic(slug="greetings-a1",title="Greetings and introductions",level="A1",category="phrase",summary="Use common greetings in Nahuatl.",explanation="Use common greetings in Nahuatl.",examples=[GrammarExample(text="Pialli")]),
    GrammarTopic(slug="identity-a1",title="Personal identity",level="A1",category="grammar",summary="Build simple first-person identity statements in Nahuatl.",explanation="Build simple first-person identity statements in Nahuatl.",examples=[GrammarExample(text="Nehuatl ...")]),
    GrammarTopic(slug="family-a1",title="Family and possession",level="A1",category="grammar",summary="Talk about family and simple possession in Nahuatl.",explanation="Talk about family and simple possession in Nahuatl.",examples=[GrammarExample(text="nocal")]),
    GrammarTopic(slug="routine-a1",title="Daily routine",level="A1",category="verb",summary="Use basic present-tense or habitual expressions in Nahuatl.",explanation="Use basic present-tense or habitual expressions in Nahuatl.",examples=[GrammarExample(text="nicua")]),
    GrammarTopic(slug="time-a1",title="Time and dates",level="A1",category="time",summary="Express basic time and day references in Nahuatl.",explanation="Express basic time and day references in Nahuatl.",examples=[GrammarExample(text="cemilhuitl")]),
    GrammarTopic(slug="food-a1",title="Food and needs",level="A1",category="vocabulary",summary="Ask for and identify everyday food and drink in Nahuatl.",explanation="Ask for and identify everyday food and drink in Nahuatl.",examples=[GrammarExample(text="tlaxcalli")]),
    GrammarTopic(slug="places-a1",title="Places and directions",level="A1",category="syntax",summary="Name places and make simple location statements in Nahuatl.",explanation="Name places and make simple location statements in Nahuatl.",examples=[GrammarExample(text="calpan")]),
    GrammarTopic(slug="review-a1",title="A1 review and repair",level="A1",category="discourse",summary="Combine familiar A1 patterns into short exchanges in Nahuatl.",explanation="Combine familiar A1 patterns into short exchanges in Nahuatl.",examples=[GrammarExample(text="cualtzin")]),
]

VOCABULARY_SETS=[
    VocabularySet(id="saludos_a1",level="A1",topic="Saludos",unit_ref="nah-a1-unit-1",words=[VocabularyEntry(word="Pialli",pos="phrase",definition="hello",example="Pialli")]),
    VocabularySet(id="identidad_a1",level="A1",topic="Identidad",unit_ref="nah-a1-unit-2",words=[VocabularyEntry(word="Nehuatl ...",pos="phrase",definition="I am ...",example="Nehuatl ...")]),
    VocabularySet(id="familia_a1",level="A1",topic="Familia",unit_ref="nah-a1-unit-3",words=[VocabularyEntry(word="nocal",pos="phrase",definition="my house",example="nocal")]),
    VocabularySet(id="rutina_a1",level="A1",topic="Rutina",unit_ref="nah-a1-unit-4",words=[VocabularyEntry(word="nicua",pos="phrase",definition="I eat",example="nicua")]),
    VocabularySet(id="tiempo_a1",level="A1",topic="Tiempo",unit_ref="nah-a1-unit-5",words=[VocabularyEntry(word="cemilhuitl",pos="phrase",definition="one day",example="cemilhuitl")]),
    VocabularySet(id="comida_a1",level="A1",topic="Comida",unit_ref="nah-a1-unit-6",words=[VocabularyEntry(word="tlaxcalli",pos="phrase",definition="tortilla",example="tlaxcalli")]),
    VocabularySet(id="lugares_a1",level="A1",topic="Lugares",unit_ref="nah-a1-unit-7",words=[VocabularyEntry(word="calpan",pos="phrase",definition="at home",example="calpan")]),
    VocabularySet(id="repaso_a1",level="A1",topic="Repaso",unit_ref="nah-a1-unit-8",words=[VocabularyEntry(word="cualtzin",pos="phrase",definition="good/beautiful",example="cualtzin")]),
]

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Saludos",icon="👋",phrases=[PhrasebookEntry(text="Pialli",context="hello",register="neutral")]),
    PhrasebookCategory(id="identity_a1",level="A1",situation="Identidad",icon="🪪",phrases=[PhrasebookEntry(text="Nehuatl ...",context="I am ...",register="neutral")]),
    PhrasebookCategory(id="family_a1",level="A1",situation="Familia",icon="👨‍👩‍👧",phrases=[PhrasebookEntry(text="nocal",context="my house",register="neutral")]),
    PhrasebookCategory(id="routine_a1",level="A1",situation="Rutina",icon="⏰",phrases=[PhrasebookEntry(text="nicua",context="I eat",register="neutral")]),
]

CURRICULUM={}
for level in LEVELS:
    if level=="A1":
        CURRICULUM[level]=[
            CurriculumUnit(id="nah-a1-unit-1",level="A1",unit_number=1,title="Greetings and introductions",grammar_points=["greetings-a1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-2",level="A1",unit_number=2,title="Personal identity",grammar_points=["identity-a1"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-3",level="A1",unit_number=3,title="Family and possession",grammar_points=["family-a1"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-4",level="A1",unit_number=4,title="Daily routine",grammar_points=["routine-a1"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-5",level="A1",unit_number=5,title="Time and dates",grammar_points=["time-a1"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-6",level="A1",unit_number=6,title="Food and needs",grammar_points=["food-a1"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-7",level="A1",unit_number=7,title="Places and directions",grammar_points=["places-a1"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-8",level="A1",unit_number=8,title="A1 review and repair",grammar_points=["review-a1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
        ]
    else:
        CURRICULUM[level]=[CurriculumUnit(id=f"nah-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Nahuatl {level} communication",grammar_points=["progressive grammar and communication"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Build level-appropriate communication"],default_weeks=2)]

ASSESSMENT_BANK=[
    AssessmentQuestion(id="nah-a1-001",skill="speaking",difficulty="A1",question="What does Pialli mean in this lesson?",options=["hello","family","school","yesterday"],correct="hello"),
    AssessmentQuestion(id="nah-a1-002",skill="vocabulary",difficulty="A1",question="What does Nehuatl ... mean in this lesson?",options=["I am ...","family","school","yesterday"],correct="I am ..."),
    AssessmentQuestion(id="nah-a1-003",skill="grammar",difficulty="A1",question="What does nocal mean in this lesson?",options=["my house","family","school","yesterday"],correct="my house"),
    AssessmentQuestion(id="nah-a1-004",skill="speaking",difficulty="A1",question="What does nicua mean in this lesson?",options=["I eat","family","school","yesterday"],correct="I eat"),
    AssessmentQuestion(id="nah-a1-005",skill="vocabulary",difficulty="A1",question="What does cemilhuitl mean in this lesson?",options=["one day","family","school","yesterday"],correct="one day"),
    AssessmentQuestion(id="nah-a1-006",skill="grammar",difficulty="A1",question="What does tlaxcalli mean in this lesson?",options=["tortilla","family","school","yesterday"],correct="tortilla"),
    AssessmentQuestion(id="nah-a1-007",skill="speaking",difficulty="A1",question="What does calpan mean in this lesson?",options=["at home","family","school","yesterday"],correct="at home"),
    AssessmentQuestion(id="nah-a1-008",skill="vocabulary",difficulty="A1",question="What does cualtzin mean in this lesson?",options=["good/beautiful","family","school","yesterday"],correct="good/beautiful"),
    AssessmentQuestion(id="nah-a1-009",skill="reading",difficulty="A1",question="Choose the expression that belongs to an everyday A1 exchange.",options=["Pialli","B2 academic term","technical formula","rare literary phrase"],correct="Pialli"),
    AssessmentQuestion(id="nah-a1-010",skill="production",difficulty="A1",question="Choose the expression learners can use to close a polite exchange.",options=["cualtzin","technical term","advanced idiom","academic citation"],correct="cualtzin"),
]

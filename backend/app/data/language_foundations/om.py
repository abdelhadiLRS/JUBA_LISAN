"""Oromo A1 deep foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]
GRAMMAR_TOPICS=[
    GrammarTopic(slug="greetings-a1",title="Greetings and introductions",level="A1",category="phrase",summary="Use common greetings in Oromo.",explanation="Use common greetings in Oromo.",examples=[GrammarExample(text="Akkam?")]),
    GrammarTopic(slug="identity-a1",title="Personal identity",level="A1",category="grammar",summary="Build simple first-person identity statements in Oromo.",explanation="Build simple first-person identity statements in Oromo.",examples=[GrammarExample(text="Maqaan koo...")]),
    GrammarTopic(slug="family-a1",title="Family and possession",level="A1",category="grammar",summary="Talk about family and simple possession in Oromo.",explanation="Talk about family and simple possession in Oromo.",examples=[GrammarExample(text="maatii")]),
    GrammarTopic(slug="routine-a1",title="Daily routine",level="A1",category="verb",summary="Use basic present-tense or habitual expressions in Oromo.",explanation="Use basic present-tense or habitual expressions in Oromo.",examples=[GrammarExample(text="ani deema")]),
    GrammarTopic(slug="time-a1",title="Time and dates",level="A1",category="time",summary="Express basic time and day references in Oromo.",explanation="Express basic time and day references in Oromo.",examples=[GrammarExample(text="har'a")]),
    GrammarTopic(slug="food-a1",title="Food and needs",level="A1",category="vocabulary",summary="Ask for and identify everyday food and drink in Oromo.",explanation="Ask for and identify everyday food and drink in Oromo.",examples=[GrammarExample(text="bishaan")]),
    GrammarTopic(slug="places-a1",title="Places and directions",level="A1",category="syntax",summary="Name places and make simple location statements in Oromo.",explanation="Name places and make simple location statements in Oromo.",examples=[GrammarExample(text="mana")]),
    GrammarTopic(slug="review-a1",title="A1 review and repair",level="A1",category="discourse",summary="Combine familiar A1 patterns into short exchanges in Oromo.",explanation="Combine familiar A1 patterns into short exchanges in Oromo.",examples=[GrammarExample(text="galatoomi")]),
]

VOCABULARY_SETS=[
    VocabularySet(id="saludos_a1",level="A1",topic="Saludos",unit_ref="om-a1-unit-1",words=[VocabularyEntry(word="Akkam?",pos="phrase",definition="how are you?",example="Akkam?")]),
    VocabularySet(id="identidad_a1",level="A1",topic="Identidad",unit_ref="om-a1-unit-2",words=[VocabularyEntry(word="Maqaan koo...",pos="phrase",definition="my name is...",example="Maqaan koo...")]),
    VocabularySet(id="familia_a1",level="A1",topic="Familia",unit_ref="om-a1-unit-3",words=[VocabularyEntry(word="maatii",pos="phrase",definition="family",example="maatii")]),
    VocabularySet(id="rutina_a1",level="A1",topic="Rutina",unit_ref="om-a1-unit-4",words=[VocabularyEntry(word="ani deema",pos="phrase",definition="I go",example="ani deema")]),
    VocabularySet(id="tiempo_a1",level="A1",topic="Tiempo",unit_ref="om-a1-unit-5",words=[VocabularyEntry(word="har'a",pos="phrase",definition="today",example="har'a")]),
    VocabularySet(id="comida_a1",level="A1",topic="Comida",unit_ref="om-a1-unit-6",words=[VocabularyEntry(word="bishaan",pos="phrase",definition="water",example="bishaan")]),
    VocabularySet(id="lugares_a1",level="A1",topic="Lugares",unit_ref="om-a1-unit-7",words=[VocabularyEntry(word="mana",pos="phrase",definition="house",example="mana")]),
    VocabularySet(id="repaso_a1",level="A1",topic="Repaso",unit_ref="om-a1-unit-8",words=[VocabularyEntry(word="galatoomi",pos="phrase",definition="thank you",example="galatoomi")]),
]

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Saludos",icon="👋",phrases=[PhrasebookEntry(text="Akkam?",context="how are you?",register="neutral")]),
    PhrasebookCategory(id="identity_a1",level="A1",situation="Identidad",icon="🪪",phrases=[PhrasebookEntry(text="Maqaan koo...",context="my name is...",register="neutral")]),
    PhrasebookCategory(id="family_a1",level="A1",situation="Familia",icon="👨‍👩‍👧",phrases=[PhrasebookEntry(text="maatii",context="family",register="neutral")]),
    PhrasebookCategory(id="routine_a1",level="A1",situation="Rutina",icon="⏰",phrases=[PhrasebookEntry(text="ani deema",context="I go",register="neutral")]),
]

CURRICULUM={}
for level in LEVELS:
    if level=="A1":
        CURRICULUM[level]=[
            CurriculumUnit(id="om-a1-unit-1",level="A1",unit_number=1,title="Greetings and introductions",grammar_points=["greetings-a1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="om-a1-unit-2",level="A1",unit_number=2,title="Personal identity",grammar_points=["identity-a1"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="om-a1-unit-3",level="A1",unit_number=3,title="Family and possession",grammar_points=["family-a1"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="om-a1-unit-4",level="A1",unit_number=4,title="Daily routine",grammar_points=["routine-a1"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="om-a1-unit-5",level="A1",unit_number=5,title="Time and dates",grammar_points=["time-a1"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="om-a1-unit-6",level="A1",unit_number=6,title="Food and needs",grammar_points=["food-a1"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="om-a1-unit-7",level="A1",unit_number=7,title="Places and directions",grammar_points=["places-a1"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="om-a1-unit-8",level="A1",unit_number=8,title="A1 review and repair",grammar_points=["review-a1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
        ]
    else:
        CURRICULUM[level]=[CurriculumUnit(id=f"om-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Oromo {level} communication",grammar_points=["progressive grammar and communication"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Build level-appropriate communication"],default_weeks=2)]

ASSESSMENT_BANK=[
    AssessmentQuestion(id="om-a1-001",skill="speaking",difficulty="A1",question="What does Akkam? mean in this lesson?",options=["how are you?","family","school","yesterday"],correct="how are you?"),
    AssessmentQuestion(id="om-a1-002",skill="vocabulary",difficulty="A1",question="What does Maqaan koo... mean in this lesson?",options=["my name is...","family","school","yesterday"],correct="my name is..."),
    AssessmentQuestion(id="om-a1-003",skill="grammar",difficulty="A1",question="What does maatii mean in this lesson?",options=["family","family","school","yesterday"],correct="family"),
    AssessmentQuestion(id="om-a1-004",skill="speaking",difficulty="A1",question="What does ani deema mean in this lesson?",options=["I go","family","school","yesterday"],correct="I go"),
    AssessmentQuestion(id="om-a1-005",skill="vocabulary",difficulty="A1",question="What does har'a mean in this lesson?",options=["today","family","school","yesterday"],correct="today"),
    AssessmentQuestion(id="om-a1-006",skill="grammar",difficulty="A1",question="What does bishaan mean in this lesson?",options=["water","family","school","yesterday"],correct="water"),
    AssessmentQuestion(id="om-a1-007",skill="speaking",difficulty="A1",question="What does mana mean in this lesson?",options=["house","family","school","yesterday"],correct="house"),
    AssessmentQuestion(id="om-a1-008",skill="vocabulary",difficulty="A1",question="What does galatoomi mean in this lesson?",options=["thank you","family","school","yesterday"],correct="thank you"),
    AssessmentQuestion(id="om-a1-009",skill="reading",difficulty="A1",question="Choose the expression that belongs to an everyday A1 exchange.",options=["Akkam?","B2 academic term","technical formula","rare literary phrase"],correct="Akkam?"),
    AssessmentQuestion(id="om-a1-010",skill="production",difficulty="A1",question="Choose the expression learners can use to close a polite exchange.",options=["galatoomi","technical term","advanced idiom","academic citation"],correct="galatoomi"),
]

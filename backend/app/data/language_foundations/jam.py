"""Jamaican Creole A1 deep foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]
GRAMMAR_TOPICS=[
    GrammarTopic(slug="greetings-a1",title="Greetings and introductions",level="A1",category="phrase",summary="Use common greetings in Jamaican Creole.",explanation="Use common greetings in Jamaican Creole.",examples=[GrammarExample(text="Wah gwaan?")]),
    GrammarTopic(slug="identity-a1",title="Personal identity",level="A1",category="grammar",summary="Build simple first-person identity statements in Jamaican Creole.",explanation="Build simple first-person identity statements in Jamaican Creole.",examples=[GrammarExample(text="Mi name a Tasha.")]),
    GrammarTopic(slug="family-a1",title="Family and possession",level="A1",category="grammar",summary="Talk about family and simple possession in Jamaican Creole.",explanation="Talk about family and simple possession in Jamaican Creole.",examples=[GrammarExample(text="Mi sista name a Keisha.")]),
    GrammarTopic(slug="routine-a1",title="Daily routine",level="A1",category="verb",summary="Use basic present-tense or habitual expressions in Jamaican Creole.",explanation="Use basic present-tense or habitual expressions in Jamaican Creole.",examples=[GrammarExample(text="Mi go a work every day.")]),
    GrammarTopic(slug="time-a1",title="Time and dates",level="A1",category="time",summary="Express basic time and day references in Jamaican Creole.",explanation="Express basic time and day references in Jamaican Creole.",examples=[GrammarExample(text="Today a Monday.")]),
    GrammarTopic(slug="food-a1",title="Food and needs",level="A1",category="vocabulary",summary="Ask for and identify everyday food and drink in Jamaican Creole.",explanation="Ask for and identify everyday food and drink in Jamaican Creole.",examples=[GrammarExample(text="Mi drink water.")]),
    GrammarTopic(slug="places-a1",title="Places and directions",level="A1",category="syntax",summary="Name places and make simple location statements in Jamaican Creole.",explanation="Name places and make simple location statements in Jamaican Creole.",examples=[GrammarExample(text="Mi deh yaad home.")]),
    GrammarTopic(slug="review-a1",title="A1 review and repair",level="A1",category="discourse",summary="Combine familiar A1 patterns into short exchanges in Jamaican Creole.",explanation="Combine familiar A1 patterns into short exchanges in Jamaican Creole.",examples=[GrammarExample(text="Respect, mi friend.")]),
]

VOCABULARY_SETS=[
    VocabularySet(id="saludos_a1",level="A1",topic="Saludos",unit_ref="jam-a1-unit-1",words=[VocabularyEntry(word="Wah gwaan?",pos="phrase",definition="how are you/what's up?",example="Wah gwaan?")]),
    VocabularySet(id="identidad_a1",level="A1",topic="Identidad",unit_ref="jam-a1-unit-2",words=[VocabularyEntry(word="Mi name a...",pos="phrase",definition="my name is...",example="Mi name a Tasha.")]),
    VocabularySet(id="familia_a1",level="A1",topic="Familia",unit_ref="jam-a1-unit-3",words=[VocabularyEntry(word="famili",pos="phrase",definition="family",example="Mi sista name a Keisha.")]),
    VocabularySet(id="rutina_a1",level="A1",topic="Rutina",unit_ref="jam-a1-unit-4",words=[VocabularyEntry(word="mi deh go",pos="phrase",definition="I am going",example="Mi go a work every day.")]),
    VocabularySet(id="tiempo_a1",level="A1",topic="Tiempo",unit_ref="jam-a1-unit-5",words=[VocabularyEntry(word="tideh",pos="phrase",definition="today",example="Today a Monday.")]),
    VocabularySet(id="comida_a1",level="A1",topic="Comida",unit_ref="jam-a1-unit-6",words=[VocabularyEntry(word="nyam",pos="phrase",definition="eat",example="Mi drink water.")]),
    VocabularySet(id="lugares_a1",level="A1",topic="Lugares",unit_ref="jam-a1-unit-7",words=[VocabularyEntry(word="yaad",pos="phrase",definition="home",example="Mi deh yaad home.")]),
    VocabularySet(id="repaso_a1",level="A1",topic="Repaso",unit_ref="jam-a1-unit-8",words=[VocabularyEntry(word="tank yuh",pos="phrase",definition="thank you",example="Respect, mi friend.")]),
]

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Saludos",icon="👋",phrases=[PhrasebookEntry(text="Wah gwaan?",context="how are you/what's up?",register="neutral")]),
    PhrasebookCategory(id="identity_a1",level="A1",situation="Identidad",icon="🪪",phrases=[PhrasebookEntry(text="Mi name a Tasha.",context="my name is...",register="neutral")]),
    PhrasebookCategory(id="family_a1",level="A1",situation="Familia",icon="👨‍👩‍👧",phrases=[PhrasebookEntry(text="Mi sista name a Keisha.",context="family",register="neutral")]),
    PhrasebookCategory(id="routine_a1",level="A1",situation="Rutina",icon="⏰",phrases=[PhrasebookEntry(text="Mi go a work every day.",context="I am going",register="neutral")]),
]

CURRICULUM={}
for level in LEVELS:
    if level=="A1":
        CURRICULUM[level]=[
            CurriculumUnit(id="jam-a1-unit-1",level="A1",unit_number=1,title="Greetings and introductions",grammar_points=["greetings-a1"],vocabulary_set_ids=["saludos_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="jam-a1-unit-2",level="A1",unit_number=2,title="Personal identity",grammar_points=["identity-a1"],vocabulary_set_ids=["identidad_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="jam-a1-unit-3",level="A1",unit_number=3,title="Family and possession",grammar_points=["family-a1"],vocabulary_set_ids=["familia_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="jam-a1-unit-4",level="A1",unit_number=4,title="Daily routine",grammar_points=["routine-a1"],vocabulary_set_ids=["rutina_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="jam-a1-unit-5",level="A1",unit_number=5,title="Time and dates",grammar_points=["time-a1"],vocabulary_set_ids=["tiempo_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="jam-a1-unit-6",level="A1",unit_number=6,title="Food and needs",grammar_points=["food-a1"],vocabulary_set_ids=["comida_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="jam-a1-unit-7",level="A1",unit_number=7,title="Places and directions",grammar_points=["places-a1"],vocabulary_set_ids=["lugares_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="jam-a1-unit-8",level="A1",unit_number=8,title="A1 review and repair",grammar_points=["review-a1"],vocabulary_set_ids=["repaso_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
        ]
    else:
        CURRICULUM[level]=[CurriculumUnit(id=f"jam-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Jamaican Creole {level} communication",grammar_points=["progressive grammar and communication"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Build level-appropriate communication"],default_weeks=2)]

ASSESSMENT_BANK=[
    AssessmentQuestion(id="jam-a1-001",skill="speaking",difficulty="A1",question="You greet a friend casually. Which Jamaican Creole expression fits?",options=["how are you/what's up?","family","school","yesterday"],correct="how are you/what's up?"),
    AssessmentQuestion(id="jam-a1-002",skill="vocabulary",difficulty="A1",question="You introduce yourself. Which phrase gives your name?",options=["my name is...","family","school","yesterday"],correct="my name is..."),
    AssessmentQuestion(id="jam-a1-003",skill="grammar",difficulty="A1",question="You talk about your sister. Which sentence fits?",options=["family","family","school","yesterday"],correct="family"),
    AssessmentQuestion(id="jam-a1-004",skill="speaking",difficulty="A1",question="You describe your daily destination. Which sentence fits?",options=["I am going","family","school","yesterday"],correct="I am going"),
    AssessmentQuestion(id="jam-a1-005",skill="vocabulary",difficulty="A1",question="You say what day it is. Which expression fits?",options=["today","family","school","yesterday"],correct="today"),
    AssessmentQuestion(id="jam-a1-006",skill="grammar",difficulty="A1",question="You ask for a drink of water. Which phrase fits?",options=["eat","family","school","yesterday"],correct="eat"),
    AssessmentQuestion(id="jam-a1-007",skill="speaking",difficulty="A1",question="You tell a friend where you are. Which sentence fits?",options=["home","family","school","yesterday"],correct="home"),
    AssessmentQuestion(id="jam-a1-008",skill="vocabulary",difficulty="A1",question="You close the exchange warmly. Which expression fits?",options=["thank you","family","school","yesterday"],correct="thank you"),
    AssessmentQuestion(id="jam-a1-009",skill="reading",difficulty="A1",question="Which phrase is useful when greeting a friend?",options=["Wah gwaan?","B2 academic term","technical formula","rare literary phrase"],correct="Wah gwaan?"),
    AssessmentQuestion(id="jam-a1-010",skill="production",difficulty="A1",question="Which expression can close a friendly A1 exchange?",options=["tank yuh","technical term","advanced idiom","academic citation"],correct="tank yuh"),
]

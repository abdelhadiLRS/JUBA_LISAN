"""Nahuatl A1 deep foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]
GRAMMAR_TOPICS=[
    GrammarTopic(slug="greetings-a1",title="Greetings and introductions",level="A1",category="phrase",summary="Use common greetings in Nahuatl.",explanation="Use common greetings in Nahuatl.",examples=[GrammarExample(text="Pialli, ¿quen tichmati?")]),
    GrammarTopic(slug="identity-a1",title="Personal identity",level="A1",category="grammar",summary="Build simple first-person identity statements in Nahuatl.",explanation="Build simple first-person identity statements in Nahuatl.",examples=[GrammarExample(text="Nehuatl nimitstlatlauhtia.")]),
    GrammarTopic(slug="family-a1",title="Family and possession",level="A1",category="grammar",summary="Talk about family and simple possession in Nahuatl.",explanation="Talk about family and simple possession in Nahuatl.",examples=[GrammarExample(text="Nocniuh itoca Juan.")]),
    GrammarTopic(slug="routine-a1",title="Daily routine",level="A1",category="verb",summary="Use basic present-tense or habitual expressions in Nahuatl.",explanation="Use basic present-tense or habitual expressions in Nahuatl.",examples=[GrammarExample(text="Axcan nicua in tlaxcalli.")]),
    GrammarTopic(slug="time-a1",title="Time and dates",level="A1",category="time",summary="Express basic time and day references in Nahuatl.",explanation="Express basic time and day references in Nahuatl.",examples=[GrammarExample(text="Axcan cemilhuitl.")]),
    GrammarTopic(slug="food-a1",title="Food and needs",level="A1",category="vocabulary",summary="Ask for and identify everyday food and drink in Nahuatl.",explanation="Ask for and identify everyday food and drink in Nahuatl.",examples=[GrammarExample(text="Niqui in atl.")]),
    GrammarTopic(slug="places-a1",title="Places and directions",level="A1",category="syntax",summary="Name places and make simple location statements in Nahuatl.",explanation="Name places and make simple location statements in Nahuatl.",examples=[GrammarExample(text="Nican nica calpan.")]),
    GrammarTopic(slug="review-a1",title="A1 review and repair",level="A1",category="discourse",summary="Combine familiar A1 patterns into short exchanges in Nahuatl.",explanation="Combine familiar A1 patterns into short exchanges in Nahuatl.",examples=[GrammarExample(text="Cualtzin in tonalli.")]),
]

VOCABULARY_SETS=[
    VocabularySet(id="saludos_a1",level="A1",topic="Saludos",unit_ref="nah-a1-unit-1",words=[VocabularyEntry(word="Pialli",pos="phrase",definition="hello",example="Pialli, ¿quen tichmati?")]),
    VocabularySet(id="identidad_a1",level="A1",topic="Identidad",unit_ref="nah-a1-unit-2",words=[VocabularyEntry(word="Nehuatl ...",pos="phrase",definition="I am ...",example="Nehuatl nimitstlatlauhtia.")]),
    VocabularySet(id="familia_a1",level="A1",topic="Familia",unit_ref="nah-a1-unit-3",words=[VocabularyEntry(word="nocal",pos="phrase",definition="my house",example="Nocniuh itoca Juan.")]),
    VocabularySet(id="rutina_a1",level="A1",topic="Rutina",unit_ref="nah-a1-unit-4",words=[VocabularyEntry(word="nicua",pos="phrase",definition="I eat",example="Axcan nicua in tlaxcalli.")]),
    VocabularySet(id="tiempo_a1",level="A1",topic="Tiempo",unit_ref="nah-a1-unit-5",words=[VocabularyEntry(word="cemilhuitl",pos="phrase",definition="one day",example="Axcan cemilhuitl.")]),
    VocabularySet(id="comida_a1",level="A1",topic="Comida",unit_ref="nah-a1-unit-6",words=[VocabularyEntry(word="tlaxcalli",pos="phrase",definition="tortilla",example="Niqui in atl.")]),
    VocabularySet(id="lugares_a1",level="A1",topic="Lugares",unit_ref="nah-a1-unit-7",words=[VocabularyEntry(word="calpan",pos="phrase",definition="at home",example="Nican nica calpan.")]),
    VocabularySet(id="repaso_a1",level="A1",topic="Repaso",unit_ref="nah-a1-unit-8",words=[VocabularyEntry(word="cualtzin",pos="phrase",definition="good/beautiful",example="Cualtzin in tonalli.")]),
]

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Saludos",icon="👋",phrases=[PhrasebookEntry(text="Pialli, ¿quen tichmati?",context="hello",register="neutral")]),
    PhrasebookCategory(id="identity_a1",level="A1",situation="Identidad",icon="🪪",phrases=[PhrasebookEntry(text="Nehuatl nimitstlatlauhtia.",context="I am ...",register="neutral")]),
    PhrasebookCategory(id="family_a1",level="A1",situation="Familia",icon="👨‍👩‍👧",phrases=[PhrasebookEntry(text="Nocniuh itoca Juan.",context="my house",register="neutral")]),
    PhrasebookCategory(id="routine_a1",level="A1",situation="Rutina",icon="⏰",phrases=[PhrasebookEntry(text="Axcan nicua in tlaxcalli.",context="I eat",register="neutral")]),
]

CURRICULUM={}
for level in LEVELS:
    if level=="A1":
        CURRICULUM[level]=[
            CurriculumUnit(id="nah-a1-unit-1",level="A1",unit_number=1,title="Greetings and introductions",grammar_points=["greetings-a1"],vocabulary_set_ids=["saludos_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-2",level="A1",unit_number=2,title="Personal identity",grammar_points=["identity-a1"],vocabulary_set_ids=["identidad_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-3",level="A1",unit_number=3,title="Family and possession",grammar_points=["family-a1"],vocabulary_set_ids=["familia_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-4",level="A1",unit_number=4,title="Daily routine",grammar_points=["routine-a1"],vocabulary_set_ids=["rutina_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-5",level="A1",unit_number=5,title="Time and dates",grammar_points=["time-a1"],vocabulary_set_ids=["tiempo_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-6",level="A1",unit_number=6,title="Food and needs",grammar_points=["food-a1"],vocabulary_set_ids=["comida_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-7",level="A1",unit_number=7,title="Places and directions",grammar_points=["places-a1"],vocabulary_set_ids=["lugares_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="nah-a1-unit-8",level="A1",unit_number=8,title="A1 review and repair",grammar_points=["review-a1"],vocabulary_set_ids=["repaso_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
        ]
    else:
        CURRICULUM[level]=[CurriculumUnit(id=f"nah-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Nahuatl {level} communication",grammar_points=["progressive grammar and communication"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Build level-appropriate communication"],default_weeks=2)]

ASSESSMENT_BANK=[
    AssessmentQuestion(id="nah-a1-001",skill="speaking",difficulty="A1",question="You meet someone and want to greet them. Which Nahuatl phrase should you use?",options=["Pialli, ¿quen tichmati?","Nehuatl nimitstlatlauhtia.","Nocniuh itoca Juan.","Cualtzin in tonalli."],correct="Pialli, ¿quen tichmati?"),
    AssessmentQuestion(id="nah-a1-002",skill="communication",difficulty="A1",question="You are introducing yourself. Which Nahuatl phrase from the lesson can you use?",options=["Nehuatl nimitstlatlauhtia.","Pialli, ¿quen tichmati?","Axcan cemilhuitl.","Nican nica calpan."],correct="Nehuatl nimitstlatlauhtia."),
    AssessmentQuestion(id="nah-a1-003",skill="family",difficulty="A1",question="You tell a learner your brother's name. Which Nahuatl sentence fits?",options=["Nocniuh itoca Juan.","Axcan nicua in tlaxcalli.","Nican nica calpan.","Pialli, ¿quen tichmati?"],correct="Nocniuh itoca Juan."),
    AssessmentQuestion(id="nah-a1-004",skill="speaking",difficulty="A1",question="You are talking about eating tortillas today. Which Nahuatl sentence from the lesson fits?",options=["Axcan nicua in tlaxcalli.","Cualtzin in tonalli.","Nican nica calpan.","Nehuatl nimitstlatlauhtia."],correct="Axcan nicua in tlaxcalli."),
    AssessmentQuestion(id="nah-a1-005",skill="time",difficulty="A1",question="You want to make a simple reference to a day. Which Nahuatl expression from the lesson fits?",options=["Axcan cemilhuitl.","Pialli, ¿quen tichmati?","Nocniuh itoca Juan.","Nican nica calpan."],correct="Axcan cemilhuitl."),
    AssessmentQuestion(id="nah-a1-006",skill="food",difficulty="A1",question="You are talking about drinking water. Which Nahuatl sentence from the lesson fits?",options=["Niqui in atl.","Nocniuh itoca Juan.","Cualtzin in tonalli.","Pialli, ¿quen tichmati?"],correct="Niqui in atl."),
    AssessmentQuestion(id="nah-a1-007",skill="places",difficulty="A1",question="You want to say that you are at home. Which Nahuatl expression from the lesson fits?",options=["Nican nica calpan.","Axcan cemilhuitl.","Nehuatl nimitstlatlauhtia.","Cualtzin in tonalli."],correct="Nican nica calpan."),
    AssessmentQuestion(id="nah-a1-008",skill="vocabulary",difficulty="A1",question="You want to describe the day positively. Which Nahuatl expression from the lesson fits?",options=["Cualtzin in tonalli.","Niqui in atl.","Nocniuh itoca Juan.","Axcan cemilhuitl."],correct="Cualtzin in tonalli."),
    AssessmentQuestion(id="nah-a1-009",skill="reading",difficulty="A1",question="Which phrase is a greeting rather than a statement about family, food, or home?",options=["Pialli, ¿quen tichmati?","Nocniuh itoca Juan.","Niqui in atl.","Nican nica calpan."],correct="Pialli, ¿quen tichmati?"),
    AssessmentQuestion(id="nah-a1-010",skill="production",difficulty="A1",question="Which phrase can be used to give a positive description of the day?",options=["Cualtzin in tonalli.","Nehuatl nimitstlatlauhtia.","Axcan nicua in tlaxcalli.","Nican nica calpan."],correct="Cualtzin in tonalli."),
]

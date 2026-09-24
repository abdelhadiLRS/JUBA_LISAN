"""Haitian Creole A1 deep foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]
GRAMMAR_TOPICS=[
    GrammarTopic(slug="greetings-a1",title="Greetings and introductions",level="A1",category="phrase",summary="Use common greetings in Haitian Creole.",explanation="Use common greetings in Haitian Creole.",examples=[GrammarExample(text="Bonjou, kijan ou ye?")]),
    GrammarTopic(slug="identity-a1",title="Personal identity",level="A1",category="grammar",summary="Build simple first-person identity statements in Haitian Creole.",explanation="Build simple first-person identity statements in Haitian Creole.",examples=[GrammarExample(text="Mwen rele Marie.")]),
    GrammarTopic(slug="family-a1",title="Family and possession",level="A1",category="grammar",summary="Talk about family and simple possession in Haitian Creole.",explanation="Talk about family and simple possession in Haitian Creole.",examples=[GrammarExample(text="Frè mwen rele Paul.")]),
    GrammarTopic(slug="routine-a1",title="Daily routine",level="A1",category="verb",summary="Use basic present-tense or habitual expressions in Haitian Creole.",explanation="Use basic present-tense or habitual expressions in Haitian Creole.",examples=[GrammarExample(text="Mwen ale lekòl chak jou.")]),
    GrammarTopic(slug="time-a1",title="Time and dates",level="A1",category="time",summary="Express basic time and day references in Haitian Creole.",explanation="Express basic time and day references in Haitian Creole.",examples=[GrammarExample(text="Jodi a se lendi.")]),
    GrammarTopic(slug="food-a1",title="Food and needs",level="A1",category="vocabulary",summary="Ask for and identify everyday food and drink in Haitian Creole.",explanation="Ask for and identify everyday food and drink in Haitian Creole.",examples=[GrammarExample(text="Mwen bwè dlo.")]),
    GrammarTopic(slug="places-a1",title="Places and directions",level="A1",category="syntax",summary="Name places and make simple location statements in Haitian Creole.",explanation="Name places and make simple location statements in Haitian Creole.",examples=[GrammarExample(text="Mwen lakay mwen.")]),
    GrammarTopic(slug="review-a1",title="A1 review and repair",level="A1",category="discourse",summary="Combine familiar A1 patterns into short exchanges in Haitian Creole.",explanation="Combine familiar A1 patterns into short exchanges in Haitian Creole.",examples=[GrammarExample(text="Mèsi anpil pou èd la.")]),
]

VOCABULARY_SETS=[
    VocabularySet(id="saludos_a1",level="A1",topic="Saludos",unit_ref="ht-a1-unit-1",words=[VocabularyEntry(word="Bonjou",pos="phrase",definition="good morning/hello",example="Bonjou, kijan ou ye?")]),
    VocabularySet(id="identidad_a1",level="A1",topic="Identidad",unit_ref="ht-a1-unit-2",words=[VocabularyEntry(word="Mwen rele...",pos="phrase",definition="my name is...",example="Mwen rele Marie.")]),
    VocabularySet(id="familia_a1",level="A1",topic="Familia",unit_ref="ht-a1-unit-3",words=[VocabularyEntry(word="fanmi",pos="phrase",definition="family",example="Frè mwen rele Paul.")]),
    VocabularySet(id="rutina_a1",level="A1",topic="Rutina",unit_ref="ht-a1-unit-4",words=[VocabularyEntry(word="mwen ale",pos="phrase",definition="I go",example="Mwen ale lekòl chak jou.")]),
    VocabularySet(id="tiempo_a1",level="A1",topic="Tiempo",unit_ref="ht-a1-unit-5",words=[VocabularyEntry(word="jodi a",pos="phrase",definition="today",example="Jodi a se lendi.")]),
    VocabularySet(id="comida_a1",level="A1",topic="Comida",unit_ref="ht-a1-unit-6",words=[VocabularyEntry(word="dlo",pos="phrase",definition="water",example="Mwen bwè dlo.")]),
    VocabularySet(id="lugares_a1",level="A1",topic="Lugares",unit_ref="ht-a1-unit-7",words=[VocabularyEntry(word="lakay",pos="phrase",definition="home",example="Mwen lakay mwen.")]),
    VocabularySet(id="repaso_a1",level="A1",topic="Repaso",unit_ref="ht-a1-unit-8",words=[VocabularyEntry(word="mèsi",pos="phrase",definition="thank you",example="Mèsi anpil pou èd la.")]),
]

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Saludos",icon="👋",phrases=[PhrasebookEntry(text="Bonjou, kijan ou ye?",context="good morning/hello",register="neutral")]),
    PhrasebookCategory(id="identity_a1",level="A1",situation="Identidad",icon="🪪",phrases=[PhrasebookEntry(text="Mwen rele Marie.",context="my name is...",register="neutral")]),
    PhrasebookCategory(id="family_a1",level="A1",situation="Familia",icon="👨‍👩‍👧",phrases=[PhrasebookEntry(text="Frè mwen rele Paul.",context="family",register="neutral")]),
    PhrasebookCategory(id="routine_a1",level="A1",situation="Rutina",icon="⏰",phrases=[PhrasebookEntry(text="Mwen ale lekòl chak jou.",context="I go",register="neutral")]),
]

CURRICULUM={}
for level in LEVELS:
    if level=="A1":
        CURRICULUM[level]=[
            CurriculumUnit(id="ht-a1-unit-1",level="A1",unit_number=1,title="Greetings and introductions",grammar_points=["greetings-a1"],vocabulary_set_ids=["saludos_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-2",level="A1",unit_number=2,title="Personal identity",grammar_points=["identity-a1"],vocabulary_set_ids=["identidad_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-3",level="A1",unit_number=3,title="Family and possession",grammar_points=["family-a1"],vocabulary_set_ids=["familia_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-4",level="A1",unit_number=4,title="Daily routine",grammar_points=["routine-a1"],vocabulary_set_ids=["rutina_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-5",level="A1",unit_number=5,title="Time and dates",grammar_points=["time-a1"],vocabulary_set_ids=["tiempo_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-6",level="A1",unit_number=6,title="Food and needs",grammar_points=["food-a1"],vocabulary_set_ids=["comida_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-7",level="A1",unit_number=7,title="Places and directions",grammar_points=["places-a1"],vocabulary_set_ids=["lugares_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ht-a1-unit-8",level="A1",unit_number=8,title="A1 review and repair",grammar_points=["review-a1"],vocabulary_set_ids=["repaso_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
        ]
    else:
        CURRICULUM[level]=[CurriculumUnit(id=f"ht-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Haitian Creole {level} communication",grammar_points=["progressive grammar and communication"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Build level-appropriate communication"],default_weeks=2)]

ASSESSMENT_BANK=[
    AssessmentQuestion(id="ht-a1-001",skill="speaking",difficulty="A1",question="You meet someone in the morning. Which Haitian Creole phrase should you use?",options=["Bonjou, kijan ou ye?","Mwen rele Marie.","Mwen bwè dlo.","Mwen lakay mwen."],correct="Bonjou, kijan ou ye?"),
    AssessmentQuestion(id="ht-a1-002",skill="communication",difficulty="A1",question="You are introducing yourself. Which Haitian Creole phrase gives your name?",options=["Mwen rele Marie.","Bonjou, kijan ou ye?","Jodi a se lendi.","Mèsi anpil pou èd la."],correct="Mwen rele Marie."),
    AssessmentQuestion(id="ht-a1-003",skill="family",difficulty="A1",question="You tell someone your brother's name. Which Haitian Creole sentence fits?",options=["Frè mwen rele Paul.","Mwen ale lekòl chak jou.","Mwen lakay mwen.","Mwen bwè dlo."],correct="Frè mwen rele Paul."),
    AssessmentQuestion(id="ht-a1-004",skill="speaking",difficulty="A1",question="You describe your daily routine. Which Haitian Creole sentence says you go to school every day?",options=["Mwen ale lekòl chak jou.","Jodi a se lendi.","Mwen rele Marie.","Mèsi anpil pou èd la."],correct="Mwen ale lekòl chak jou."),
    AssessmentQuestion(id="ht-a1-005",skill="time",difficulty="A1",question="You want to say that today is Monday. Which Haitian Creole sentence fits?",options=["Jodi a se lendi.","Mwen bwè dlo.","Mwen lakay mwen.","Bonjou, kijan ou ye?"],correct="Jodi a se lendi."),
    AssessmentQuestion(id="ht-a1-006",skill="food",difficulty="A1",question="You are talking about drinking water. Which Haitian Creole sentence fits?",options=["Mwen bwè dlo.","Mwen ale lekòl chak jou.","Frè mwen rele Paul.","Mèsi anpil pou èd la."],correct="Mwen bwè dlo."),
    AssessmentQuestion(id="ht-a1-007",skill="places",difficulty="A1",question="You want to tell someone that you are at home. Which Haitian Creole sentence fits?",options=["Mwen lakay mwen.","Jodi a se lendi.","Mwen rele Marie.","Bonjou, kijan ou ye?"],correct="Mwen lakay mwen."),
    AssessmentQuestion(id="ht-a1-008",skill="communication",difficulty="A1",question="Someone helped you and you want to thank them. Which Haitian Creole phrase fits?",options=["Mèsi anpil pou èd la.","Mwen bwè dlo.","Mwen ale lekòl chak jou.","Mwen lakay mwen."],correct="Mèsi anpil pou èd la."),
    AssessmentQuestion(id="ht-a1-009",skill="reading",difficulty="A1",question="Which phrase is useful when opening a simple conversation?",options=["Bonjou, kijan ou ye?","Mwen bwè dlo.","Jodi a se lendi.","Mwen lakay mwen."],correct="Bonjou, kijan ou ye?"),
    AssessmentQuestion(id="ht-a1-010",skill="production",difficulty="A1",question="Which phrase is appropriate when thanking someone for help?",options=["Mèsi anpil pou èd la.","Mwen rele Marie.","Jodi a se lendi.","Mwen ale lekòl chak jou."],correct="Mèsi anpil pou èd la."),
]

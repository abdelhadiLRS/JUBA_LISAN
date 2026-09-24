"""Samburu A1 deep foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

GRAMMAR_TOPICS=[
    GrammarTopic(slug="greetings-a1",title="Greetings and introductions",level="A1",category="phrase",summary="Use everyday greetings and polite openings.",explanation="Use everyday greetings and polite openings.",examples=[GrammarExample(text="Supa")]),
    GrammarTopic(slug="identity-a1",title="Personal identity",level="A1",category="syntax",summary="Introduce yourself and ask for a name.",explanation="Introduce yourself and ask for a name.",examples=[GrammarExample(text="Nanyor...")]),
    GrammarTopic(slug="family-a1",title="Family and home",level="A1",category="grammar",summary="Talk about family and familiar people.",explanation="Talk about family and familiar people.",examples=[GrammarExample(text="enkaji")]),
    GrammarTopic(slug="routine-a1",title="Daily routine",level="A1",category="verbs",summary="Describe simple habitual actions.",explanation="Describe simple habitual actions.",examples=[GrammarExample(text="aisho")]),
    GrammarTopic(slug="time-a1",title="Time and daily schedule",level="A1",category="time",summary="Use basic day and time expressions.",explanation="Use basic day and time expressions.",examples=[GrammarExample(text="aitidua")]),
    GrammarTopic(slug="food-a1",title="Food and drink",level="A1",category="vocabulary",summary="Identify basic food and drink needs.",explanation="Identify basic food and drink needs.",examples=[GrammarExample(text="enkare")]),
    GrammarTopic(slug="places-a1",title="Places and location",level="A1",category="syntax",summary="Say where people or things are.",explanation="Say where people or things are.",examples=[GrammarExample(text="enkaji")]),
    GrammarTopic(slug="review-a1",title="A1 review and interaction",level="A1",category="discourse",summary="Combine core A1 patterns in short exchanges.",explanation="Combine core A1 patterns in short exchanges.",examples=[GrammarExample(text="ashe")]),
]

VOCABULARY_SETS=[
    VocabularySet(id="greetings_a1",level="A1",topic="Greetings",unit_ref="suq-a1-unit-1",words=[VocabularyEntry(word="Supa",pos="phrase",definition="hello",example="Supa")]),
    VocabularySet(id="identity_a1",level="A1",topic="Identity",unit_ref="suq-a1-unit-2",words=[VocabularyEntry(word="Nanyor...",pos="phrase",definition="my name is...",example="Nanyor...")]),
    VocabularySet(id="family_a1",level="A1",topic="Family",unit_ref="suq-a1-unit-3",words=[VocabularyEntry(word="enkaji",pos="phrase",definition="house/home",example="enkaji")]),
    VocabularySet(id="routine_a1",level="A1",topic="Routine",unit_ref="suq-a1-unit-4",words=[VocabularyEntry(word="aisho",pos="phrase",definition="work",example="aisho")]),
    VocabularySet(id="time_a1",level="A1",topic="Time",unit_ref="suq-a1-unit-5",words=[VocabularyEntry(word="aitidua",pos="phrase",definition="today",example="aitidua")]),
    VocabularySet(id="food_a1",level="A1",topic="Food",unit_ref="suq-a1-unit-6",words=[VocabularyEntry(word="enkare",pos="phrase",definition="water",example="enkare")]),
    VocabularySet(id="places_a1",level="A1",topic="Places",unit_ref="suq-a1-unit-7",words=[VocabularyEntry(word="enkaji",pos="phrase",definition="home",example="enkaji")]),
    VocabularySet(id="review_a1",level="A1",topic="Review",unit_ref="suq-a1-unit-8",words=[VocabularyEntry(word="ashe",pos="phrase",definition="thank you",example="ashe")]),
]

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Greetings",icon="👋",phrases=[PhrasebookEntry(text="Supa",context="hello",register="neutral")]),
    PhrasebookCategory(id="identity_a1",level="A1",situation="Identity",icon="🪪",phrases=[PhrasebookEntry(text="Nanyor...",context="my name is...",register="neutral")]),
    PhrasebookCategory(id="family_a1",level="A1",situation="Family",icon="👨‍👩‍👧",phrases=[PhrasebookEntry(text="enkaji",context="house/home",register="neutral")]),
    PhrasebookCategory(id="routine_a1",level="A1",situation="Routine",icon="⏰",phrases=[PhrasebookEntry(text="aisho",context="work",register="neutral")]),
]

CURRICULUM={}
for level in LEVELS:
    if level=="A1":
        CURRICULUM[level]=[
            CurriculumUnit(id="suq-a1-unit-1",level="A1",unit_number=1,title="Greetings and introductions",grammar_points=["greetings-a1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="suq-a1-unit-2",level="A1",unit_number=2,title="Personal identity",grammar_points=["identity-a1"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="suq-a1-unit-3",level="A1",unit_number=3,title="Family and home",grammar_points=["family-a1"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="suq-a1-unit-4",level="A1",unit_number=4,title="Daily routine",grammar_points=["routine-a1"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="suq-a1-unit-5",level="A1",unit_number=5,title="Time and daily schedule",grammar_points=["time-a1"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="suq-a1-unit-6",level="A1",unit_number=6,title="Food and drink",grammar_points=["food-a1"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="suq-a1-unit-7",level="A1",unit_number=7,title="Places and location",grammar_points=["places-a1"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="suq-a1-unit-8",level="A1",unit_number=8,title="A1 review and interaction",grammar_points=["review-a1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
        ]
    else:
        CURRICULUM[level]=[CurriculumUnit(id=f"suq-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Samburu {level} communication",grammar_points=["progressive grammar and communication"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Build level-appropriate communication"],default_weeks=2)]

ASSESSMENT_BANK=[
    AssessmentQuestion(id="suq-a1-001",skill="speaking",difficulty="A1",question="You meet someone in the morning. Which Samburu expression from the lesson means 'hello'?",options=["Supa","enkaji","enkare","ashe"],correct="Supa"),
    AssessmentQuestion(id="suq-a1-002",skill="communication",difficulty="A1",question="You are introducing yourself and want to give your name. Which expression should you use?",options=["Nanyor...","Supa","enkaji","aitidua"],correct="Nanyor..."),
    AssessmentQuestion(id="suq-a1-003",skill="vocabulary",difficulty="A1",question="You are talking about where you live. Which Samburu word from the lesson means 'house/home'?",options=["enkaji","enkare","aisho","ashe"],correct="enkaji"),
    AssessmentQuestion(id="suq-a1-004",skill="vocabulary",difficulty="A1",question="Someone asks what you do during the day. Which word from the lesson means 'work'?",options=["aisho","enkaji","Supa","aitidua"],correct="aisho"),
    AssessmentQuestion(id="suq-a1-005",skill="vocabulary",difficulty="A1",question="You are talking about today. Which Samburu word should you choose?",options=["aitidua","enkare","enkaji","ashe"],correct="aitidua"),
    AssessmentQuestion(id="suq-a1-006",skill="vocabulary",difficulty="A1",question="You are thirsty and need water. Which Samburu word from the lesson means 'water'?",options=["enkare","aisho","enkaji","Supa"],correct="enkare"),
    AssessmentQuestion(id="suq-a1-007",skill="communication",difficulty="A1",question="You are talking about your home with another learner. Which expression matches the home topic?",options=["enkaji","Nanyor...","aitidua","ashe"],correct="enkaji"),
    AssessmentQuestion(id="suq-a1-008",skill="communication",difficulty="A1",question="Someone thanks you. Which expression from the lesson means 'thank you'?",options=["ashe","Supa","enkare","aisho"],correct="ashe"),
    AssessmentQuestion(id="suq-a1-009",skill="speaking",difficulty="A1",question="You want to start a simple conversation with a new person. Which expression should come first?",options=["Supa","enkare","aitidua","enkaji"],correct="Supa"),
    AssessmentQuestion(id="suq-a1-010",skill="vocabulary",difficulty="A1",question="Which expression is connected with introducing yourself rather than food, water, or home?",options=["Nanyor...","enkare","enkaji","Supa"],correct="Nanyor...")
]

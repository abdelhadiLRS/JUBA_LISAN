"""Bulgarian A1 deep foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

GRAMMAR_TOPICS=[
    GrammarTopic(slug="greetings-a1",title="Greetings and introductions",level="A1",category="phrase",summary="Use everyday greetings and polite openings.",explanation="Use everyday greetings and polite openings.",examples=[GrammarExample(text="Здравейте")]),
    GrammarTopic(slug="identity-a1",title="Personal identity",level="A1",category="syntax",summary="Introduce yourself and ask for a name.",explanation="Introduce yourself and ask for a name.",examples=[GrammarExample(text="Казвам се...")]),
    GrammarTopic(slug="family-a1",title="Family and home",level="A1",category="grammar",summary="Talk about family and familiar people.",explanation="Talk about family and familiar people.",examples=[GrammarExample(text="семейство")]),
    GrammarTopic(slug="routine-a1",title="Daily routine",level="A1",category="verbs",summary="Describe simple habitual actions.",explanation="Describe simple habitual actions.",examples=[GrammarExample(text="работя")]),
    GrammarTopic(slug="time-a1",title="Time and daily schedule",level="A1",category="time",summary="Use basic day and time expressions.",explanation="Use basic day and time expressions.",examples=[GrammarExample(text="днес")]),
    GrammarTopic(slug="food-a1",title="Food and drink",level="A1",category="vocabulary",summary="Identify basic food and drink needs.",explanation="Identify basic food and drink needs.",examples=[GrammarExample(text="вода")]),
    GrammarTopic(slug="places-a1",title="Places and location",level="A1",category="syntax",summary="Say where people or things are.",explanation="Say where people or things are.",examples=[GrammarExample(text="вкъщи")]),
    GrammarTopic(slug="review-a1",title="A1 review and interaction",level="A1",category="discourse",summary="Combine core A1 patterns in short exchanges.",explanation="Combine core A1 patterns in short exchanges.",examples=[GrammarExample(text="Благодаря")]),
]

VOCABULARY_SETS=[
    VocabularySet(id="greetings_a1",level="A1",topic="Поздрави",unit_ref="bg-a1-unit-1",words=[VocabularyEntry(word="Здравейте",pos="phrase",definition="hello",example="Здравейте")]),
    VocabularySet(id="identity_a1",level="A1",topic="Представяне",unit_ref="bg-a1-unit-2",words=[VocabularyEntry(word="Казвам се...",pos="phrase",definition="my name is...",example="Казвам се...")]),
    VocabularySet(id="family_a1",level="A1",topic="Семейство",unit_ref="bg-a1-unit-3",words=[VocabularyEntry(word="семейство",pos="phrase",definition="family",example="семейство")]),
    VocabularySet(id="routine_a1",level="A1",topic="Рутина",unit_ref="bg-a1-unit-4",words=[VocabularyEntry(word="работя",pos="phrase",definition="I work",example="работя")]),
    VocabularySet(id="time_a1",level="A1",topic="Време",unit_ref="bg-a1-unit-5",words=[VocabularyEntry(word="днес",pos="phrase",definition="today",example="днес")]),
    VocabularySet(id="food_a1",level="A1",topic="Храна",unit_ref="bg-a1-unit-6",words=[VocabularyEntry(word="вода",pos="phrase",definition="water",example="вода")]),
    VocabularySet(id="places_a1",level="A1",topic="Места",unit_ref="bg-a1-unit-7",words=[VocabularyEntry(word="вкъщи",pos="phrase",definition="at home",example="вкъщи")]),
    VocabularySet(id="review_a1",level="A1",topic="Преговор",unit_ref="bg-a1-unit-8",words=[VocabularyEntry(word="Благодаря",pos="phrase",definition="thank you",example="Благодаря")]),
]

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Поздрави",icon="👋",phrases=[PhrasebookEntry(text="Здравейте",context="hello",register="neutral")]),
    PhrasebookCategory(id="identity_a1",level="A1",situation="Представяне",icon="🪪",phrases=[PhrasebookEntry(text="Казвам се...",context="my name is...",register="neutral")]),
    PhrasebookCategory(id="family_a1",level="A1",situation="Семейство",icon="👨‍👩‍👧",phrases=[PhrasebookEntry(text="семейство",context="family",register="neutral")]),
    PhrasebookCategory(id="routine_a1",level="A1",situation="Рутина",icon="⏰",phrases=[PhrasebookEntry(text="работя",context="I work",register="neutral")]),
]

CURRICULUM={}
for level in LEVELS:
    if level=="A1":
        CURRICULUM[level]=[
            CurriculumUnit(id="bg-a1-unit-1",level="A1",unit_number=1,title="Greetings and introductions",grammar_points=["greetings-a1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="bg-a1-unit-2",level="A1",unit_number=2,title="Personal identity",grammar_points=["identity-a1"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="bg-a1-unit-3",level="A1",unit_number=3,title="Family and home",grammar_points=["family-a1"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="bg-a1-unit-4",level="A1",unit_number=4,title="Daily routine",grammar_points=["routine-a1"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="bg-a1-unit-5",level="A1",unit_number=5,title="Time and daily schedule",grammar_points=["time-a1"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="bg-a1-unit-6",level="A1",unit_number=6,title="Food and drink",grammar_points=["food-a1"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="bg-a1-unit-7",level="A1",unit_number=7,title="Places and location",grammar_points=["places-a1"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="bg-a1-unit-8",level="A1",unit_number=8,title="A1 review and interaction",grammar_points=["review-a1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
        ]
    else:
        CURRICULUM[level]=[CurriculumUnit(id=f"bg-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Bulgarian {level} communication",grammar_points=["progressive grammar and communication"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Build level-appropriate communication"],default_weeks=2)]

ASSESSMENT_BANK=[
    AssessmentQuestion(id="bg-a1-001",skill="speaking",difficulty="A1",question="Which expression matches the lesson meaning 'hello'?",options=["Здравейте","technical term","advanced idiom","unrelated expression"],correct="Здравейте"),
    AssessmentQuestion(id="bg-a1-002",skill="vocabulary",difficulty="A1",question="Which expression matches the lesson meaning 'my name is...'?",options=["Казвам се...","technical term","advanced idiom","unrelated expression"],correct="Казвам се..."),
    AssessmentQuestion(id="bg-a1-003",skill="grammar",difficulty="A1",question="Which expression matches the lesson meaning 'family'?",options=["семейство","technical term","advanced idiom","unrelated expression"],correct="семейство"),
    AssessmentQuestion(id="bg-a1-004",skill="speaking",difficulty="A1",question="Which expression matches the lesson meaning 'I work'?",options=["работя","technical term","advanced idiom","unrelated expression"],correct="работя"),
    AssessmentQuestion(id="bg-a1-005",skill="vocabulary",difficulty="A1",question="Which expression matches the lesson meaning 'today'?",options=["днес","technical term","advanced idiom","unrelated expression"],correct="днес"),
    AssessmentQuestion(id="bg-a1-006",skill="grammar",difficulty="A1",question="Which expression matches the lesson meaning 'water'?",options=["вода","technical term","advanced idiom","unrelated expression"],correct="вода"),
    AssessmentQuestion(id="bg-a1-007",skill="speaking",difficulty="A1",question="Which expression matches the lesson meaning 'at home'?",options=["вкъщи","technical term","advanced idiom","unrelated expression"],correct="вкъщи"),
    AssessmentQuestion(id="bg-a1-008",skill="vocabulary",difficulty="A1",question="Which expression matches the lesson meaning 'thank you'?",options=["Благодаря","technical term","advanced idiom","unrelated expression"],correct="Благодаря"),
    AssessmentQuestion(id="bg-a1-009",skill="reading",difficulty="A1",question="Select the everyday A1 expression.",options=["Здравейте","advanced academic phrase","technical formula","rare literary term"],correct="Здравейте"),
    AssessmentQuestion(id="bg-a1-010",skill="production",difficulty="A1",question="Select the polite expression for closing an everyday exchange.",options=["Благодаря","technical term","advanced idiom","unrelated expression"],correct="Благодаря"),
]

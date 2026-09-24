"""Serbian A1 deep foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

GRAMMAR_TOPICS=[
    GrammarTopic(slug="greetings-a1",title="Greetings and introductions",level="A1",category="phrase",summary="Use everyday greetings and polite openings.",explanation="Use everyday greetings and polite openings.",examples=[GrammarExample(text="Здраво")]),
    GrammarTopic(slug="identity-a1",title="Personal identity",level="A1",category="syntax",summary="Introduce yourself and ask for a name.",explanation="Introduce yourself and ask for a name.",examples=[GrammarExample(text="Зовем се...")]),
    GrammarTopic(slug="family-a1",title="Family and home",level="A1",category="grammar",summary="Talk about family and familiar people.",explanation="Talk about family and familiar people.",examples=[GrammarExample(text="породица")]),
    GrammarTopic(slug="routine-a1",title="Daily routine",level="A1",category="verbs",summary="Describe simple habitual actions.",explanation="Describe simple habitual actions.",examples=[GrammarExample(text="радим")]),
    GrammarTopic(slug="time-a1",title="Time and daily schedule",level="A1",category="time",summary="Use basic day and time expressions.",explanation="Use basic day and time expressions.",examples=[GrammarExample(text="данас")]),
    GrammarTopic(slug="food-a1",title="Food and drink",level="A1",category="vocabulary",summary="Identify basic food and drink needs.",explanation="Identify basic food and drink needs.",examples=[GrammarExample(text="вода")]),
    GrammarTopic(slug="places-a1",title="Places and location",level="A1",category="syntax",summary="Say where people or things are.",explanation="Say where people or things are.",examples=[GrammarExample(text="код куће")]),
    GrammarTopic(slug="review-a1",title="A1 review and interaction",level="A1",category="discourse",summary="Combine core A1 patterns in short exchanges.",explanation="Combine core A1 patterns in short exchanges.",examples=[GrammarExample(text="Хвала")]),
]

VOCABULARY_SETS=[
    VocabularySet(id="greetings_a1",level="A1",topic="Поздрави",unit_ref="sr-a1-unit-1",words=[VocabularyEntry(word="Здраво",pos="phrase",definition="hello",example="Здраво! Како си?")]),
    VocabularySet(id="identity_a1",level="A1",topic="Представљање",unit_ref="sr-a1-unit-2",words=[VocabularyEntry(word="Зовем се...",pos="phrase",definition="my name is...",example="Зовем се Марко.")]),
    VocabularySet(id="family_a1",level="A1",topic="Породица",unit_ref="sr-a1-unit-3",words=[VocabularyEntry(word="породица",pos="phrase",definition="family",example="Моја породица живи у Београду.")]),
    VocabularySet(id="routine_a1",level="A1",topic="Рутина",unit_ref="sr-a1-unit-4",words=[VocabularyEntry(word="радим",pos="phrase",definition="I work",example="Данас радим у канцеларији.")]),
    VocabularySet(id="time_a1",level="A1",topic="Време",unit_ref="sr-a1-unit-5",words=[VocabularyEntry(word="данас",pos="phrase",definition="today",example="Данас учим српски.")]),
    VocabularySet(id="food_a1",level="A1",topic="Храна",unit_ref="sr-a1-unit-6",words=[VocabularyEntry(word="вода",pos="phrase",definition="water",example="Молим вас, чашу воде.")]),
    VocabularySet(id="places_a1",level="A1",topic="Места",unit_ref="sr-a1-unit-7",words=[VocabularyEntry(word="код куће",pos="phrase",definition="at home",example="Данас сам код куће.")]),
    VocabularySet(id="review_a1",level="A1",topic="Понављање",unit_ref="sr-a1-unit-8",words=[VocabularyEntry(word="Хвала",pos="phrase",definition="thank you",example="Хвала вам на помоћи.")]),
]

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Поздрави",icon="👋",phrases=[PhrasebookEntry(text="Здраво!",context="greeting",register="neutral"),PhrasebookEntry(text="Како си?",context="asking how someone is",register="neutral"),PhrasebookEntry(text="Зовем се Марко.",context="introducing yourself",register="neutral")]),
    PhrasebookCategory(id="shopping_a1",level="A1",situation="Куповина",icon="🛒",phrases=[PhrasebookEntry(text="Колико ово кошта?",context="asking the price",register="neutral"),PhrasebookEntry(text="Хтео бих ово, молим.",context="requesting an item",register="neutral"),PhrasebookEntry(text="Молим вас, воду.",context="asking for water",register="neutral")]),
    PhrasebookCategory(id="directions_a1",level="A1",situation="Правци",icon="🧭",phrases=[PhrasebookEntry(text="Где је школа?",context="asking for a location",register="neutral"),PhrasebookEntry(text="Где је станица?",context="asking for a station",register="neutral"),PhrasebookEntry(text="Лево или десно?",context="checking a direction",register="neutral")]),
    PhrasebookCategory(id="help_a1",level="A1",situation="Помоћ",icon="🆘",phrases=[PhrasebookEntry(text="Молим вас, помозите ми.",context="asking for help",register="neutral"),PhrasebookEntry(text="Не разумем.",context="saying you do not understand",register="neutral"),PhrasebookEntry(text="Можете ли да поновите?",context="asking someone to repeat",register="neutral")]),
]

CURRICULUM={}
for level in LEVELS:
    if level=="A1":
        CURRICULUM[level]=[
            CurriculumUnit(id="sr-a1-unit-1",level="A1",unit_number=1,title="Greetings and introductions",grammar_points=["greetings-a1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sr-a1-unit-2",level="A1",unit_number=2,title="Personal identity",grammar_points=["identity-a1"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sr-a1-unit-3",level="A1",unit_number=3,title="Family and home",grammar_points=["family-a1"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sr-a1-unit-4",level="A1",unit_number=4,title="Daily routine",grammar_points=["routine-a1"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sr-a1-unit-5",level="A1",unit_number=5,title="Time and daily schedule",grammar_points=["time-a1"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sr-a1-unit-6",level="A1",unit_number=6,title="Food and drink",grammar_points=["food-a1"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sr-a1-unit-7",level="A1",unit_number=7,title="Places and location",grammar_points=["places-a1"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sr-a1-unit-8",level="A1",unit_number=8,title="A1 review and interaction",grammar_points=["review-a1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
        ]
    else:
        CURRICULUM[level]=[CurriculumUnit(id=f"sr-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Serbian {level} communication",grammar_points=["progressive grammar and communication"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Build level-appropriate communication"],default_weeks=2)]

ASSESSMENT_BANK=[AssessmentQuestion(id="sr-a1-001",skill="speaking",difficulty="A1",question="You meet someone informally. Which Serbian phrase is a natural greeting?",options=["Здраво!","Колико ово кошта?","Не разумем.","Где је школа?"],correct="Здраво!"),
AssessmentQuestion(id="sr-a1-002",skill="communication",difficulty="A1",question="You introduce yourself as Marko. Which Serbian sentence should you use?",options=["Зовем се Марко.","Хтео бих ово, молим.","Данас учим српски.","Данас сам код куће."],correct="Зовем се Марко."),
AssessmentQuestion(id="sr-a1-003",skill="vocabulary",difficulty="A1",question="You are talking about your relatives. Which Serbian word means “family”?",options=["породица","вода","данас","школа"],correct="породица"),
AssessmentQuestion(id="sr-a1-004",skill="grammar",difficulty="A1",question="You tell a friend that you are working today. Which sentence is appropriate?",options=["Данас радим у канцеларији.","Моја породица живи у Београду.","Молим вас, чашу воде.","Данас сам код куће."],correct="Данас радим у канцеларији."),
AssessmentQuestion(id="sr-a1-005",skill="vocabulary",difficulty="A1",question="You are thirsty. Which Serbian word means “water”?",options=["вода","породица","радим","станица"],correct="вода"),
AssessmentQuestion(id="sr-a1-006",skill="communication",difficulty="A1",question="You want to ask the price in a shop. Which Serbian phrase should you use?",options=["Колико ово кошта?","Како си?","Не разумем.","Где је станица?"],correct="Колико ово кошта?"),
AssessmentQuestion(id="sr-a1-007",skill="communication",difficulty="A1",question="You need directions to the school. Which Serbian question should you use?",options=["Где је школа?","Молим вас, воду.","Хвала вам на помоћи.","Зовем се Марко."],correct="Где је школа?"),
AssessmentQuestion(id="sr-a1-008",skill="communication",difficulty="A1",question="You do not understand what someone said. Which Serbian phrase should you use?",options=["Не разумем.","Здраво!","Колико ово кошта?","Где је станица?"],correct="Не разумем."),
AssessmentQuestion(id="sr-a1-009",skill="communication",difficulty="A1",question="You need someone to repeat their words. Which Serbian phrase is appropriate?",options=["Можете ли да поновите?","Данас сам код куће.","Хтео бих ово, молим.","Како си?"],correct="Можете ли да поновите?"),
AssessmentQuestion(id="sr-a1-010",skill="production",difficulty="A1",question="Someone helps you and you want to thank them. Which Serbian phrase should you use?",options=["Хвала вам на помоћи.","Не разумем.","Где је школа?","Колико ово кошта?"],correct="Хвала вам на помоћи.")]

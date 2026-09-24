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
    VocabularySet(id="greetings_a1",level="A1",topic="Поздрави",unit_ref="bg-a1-unit-1",words=[VocabularyEntry(word="Здравейте",pos="phrase",definition="hello",example="Здравейте! Как сте?")]),
    VocabularySet(id="identity_a1",level="A1",topic="Представяне",unit_ref="bg-a1-unit-2",words=[VocabularyEntry(word="Казвам се...",pos="phrase",definition="my name is...",example="Казвам се Иван.")]),
    VocabularySet(id="family_a1",level="A1",topic="Семейство",unit_ref="bg-a1-unit-3",words=[VocabularyEntry(word="семейство",pos="phrase",definition="family",example="Моето семейство е в София.")]),
    VocabularySet(id="routine_a1",level="A1",topic="Рутина",unit_ref="bg-a1-unit-4",words=[VocabularyEntry(word="работя",pos="phrase",definition="I work",example="Днес работя в офиса.")]),
    VocabularySet(id="time_a1",level="A1",topic="Време",unit_ref="bg-a1-unit-5",words=[VocabularyEntry(word="днес",pos="phrase",definition="today",example="Днес уча български.")]),
    VocabularySet(id="food_a1",level="A1",topic="Храна",unit_ref="bg-a1-unit-6",words=[VocabularyEntry(word="вода",pos="phrase",definition="water",example="Искам чаша вода, моля.")]),
    VocabularySet(id="places_a1",level="A1",topic="Места",unit_ref="bg-a1-unit-7",words=[VocabularyEntry(word="вкъщи",pos="phrase",definition="at home",example="Аз съм вкъщи.")]),
    VocabularySet(id="review_a1",level="A1",topic="Преговор",unit_ref="bg-a1-unit-8",words=[VocabularyEntry(word="Благодаря",pos="phrase",definition="thank you",example="Благодаря за помощта.")]),
]

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Поздрави",icon="👋",phrases=[PhrasebookEntry(text="Здравейте!",context="greeting",register="neutral"),PhrasebookEntry(text="Как сте?",context="asking how someone is",register="neutral"),PhrasebookEntry(text="Казвам се Иван.",context="introducing yourself",register="neutral")]),
    PhrasebookCategory(id="shopping_a1",level="A1",situation="Пазаруване",icon="🛒",phrases=[PhrasebookEntry(text="Колко струва това?",context="asking the price",register="neutral"),PhrasebookEntry(text="Искам това, моля.",context="requesting an item",register="neutral"),PhrasebookEntry(text="Може ли вода?",context="asking for water",register="neutral")]),
    PhrasebookCategory(id="directions_a1",level="A1",situation="Посоки",icon="🧭",phrases=[PhrasebookEntry(text="Къде е училището?",context="asking for a location",register="neutral"),PhrasebookEntry(text="Къде е гарата?",context="asking for a station",register="neutral"),PhrasebookEntry(text="Наляво или надясно?",context="checking a direction",register="neutral")]),
    PhrasebookCategory(id="help_a1",level="A1",situation="Помощ",icon="🆘",phrases=[PhrasebookEntry(text="Моля, помогнете ми.",context="asking for help",register="neutral"),PhrasebookEntry(text="Не разбирам.",context="saying you do not understand",register="neutral"),PhrasebookEntry(text="Може ли да повторите?",context="asking someone to repeat",register="neutral")]),
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

ASSESSMENT_BANK=[AssessmentQuestion(id="bg-a1-001",skill="speaking",difficulty="A1",question="You meet someone in the morning. Which Bulgarian phrase is a natural greeting?",options=["Здравейте!","Колко струва това?","Не разбирам.","Къде е училището?"],correct="Здравейте!"),
AssessmentQuestion(id="bg-a1-002",skill="communication",difficulty="A1",question="You introduce yourself as Ivan. Which Bulgarian sentence should you use?",options=["Казвам се Иван.","Искам това, моля.","Днес уча български.","Аз съм вкъщи."],correct="Казвам се Иван."),
AssessmentQuestion(id="bg-a1-003",skill="vocabulary",difficulty="A1",question="You are talking about your relatives. Which Bulgarian word means “family”?",options=["семейство","вода","днес","училище"],correct="семейство"),
AssessmentQuestion(id="bg-a1-004",skill="grammar",difficulty="A1",question="You tell a friend that you are working today. Which sentence is appropriate?",options=["Днес работя в офиса.","Моето семейство е в София.","Искам чаша вода, моля.","Аз съм вкъщи."],correct="Днес работя в офиса."),
AssessmentQuestion(id="bg-a1-005",skill="vocabulary",difficulty="A1",question="You are thirsty in a café. Which Bulgarian word means “water”?",options=["вода","семейство","работя","гара"],correct="вода"),
AssessmentQuestion(id="bg-a1-006",skill="communication",difficulty="A1",question="You want to ask the price in a shop. Which Bulgarian phrase should you use?",options=["Колко струва това?","Как сте?","Не разбирам.","Къде е гарата?"],correct="Колко струва това?"),
AssessmentQuestion(id="bg-a1-007",skill="communication",difficulty="A1",question="You need directions to the school. Which Bulgarian question should you use?",options=["Къде е училището?","Може ли вода?","Благодаря за помощта.","Казвам се Иван."],correct="Къде е училището?"),
AssessmentQuestion(id="bg-a1-008",skill="communication",difficulty="A1",question="You do not understand what someone said. Which Bulgarian phrase should you use?",options=["Не разбирам.","Здравейте!","Колко струва това?","Къде е гарата?"],correct="Не разбирам."),
AssessmentQuestion(id="bg-a1-009",skill="communication",difficulty="A1",question="You need someone to repeat their words. Which Bulgarian phrase is appropriate?",options=["Може ли да повторите?","Аз съм вкъщи.","Искам това, моля.","Как сте?"],correct="Може ли да повторите?"),
AssessmentQuestion(id="bg-a1-010",skill="production",difficulty="A1",question="Someone helps you and you want to thank them. Which Bulgarian phrase should you use?",options=["Благодаря за помощта.","Не разбирам.","Къде е училището?","Колко струва това?"],correct="Благодаря за помощта.")]

"""Ewe A1 deep foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

GRAMMAR_TOPICS=[
    GrammarTopic(slug="greetings-a1",title="Greetings and introductions",level="A1",category="phrase",summary="Use everyday greetings and polite openings.",explanation="Use everyday greetings and polite openings.",examples=[GrammarExample(text="Woezɔ")]),
    GrammarTopic(slug="identity-a1",title="Personal identity",level="A1",category="syntax",summary="Introduce yourself and ask for a name.",explanation="Introduce yourself and ask for a name.",examples=[GrammarExample(text="nye ŋkɔe...")]),
    GrammarTopic(slug="family-a1",title="Family and home",level="A1",category="grammar",summary="Talk about family and familiar people.",explanation="Talk about family and familiar people.",examples=[GrammarExample(text="aƒe")]),
    GrammarTopic(slug="routine-a1",title="Daily routine",level="A1",category="verbs",summary="Describe simple habitual actions.",explanation="Describe simple habitual actions.",examples=[GrammarExample(text="melé...")]),
    GrammarTopic(slug="time-a1",title="Time and daily schedule",level="A1",category="time",summary="Use basic day and time expressions.",explanation="Use basic day and time expressions.",examples=[GrammarExample(text="egbe")]),
    GrammarTopic(slug="food-a1",title="Food and drink",level="A1",category="vocabulary",summary="Identify basic food and drink needs.",explanation="Identify basic food and drink needs.",examples=[GrammarExample(text="tsi")]),
    GrammarTopic(slug="places-a1",title="Places and location",level="A1",category="syntax",summary="Say where people or things are.",explanation="Say where people or things are.",examples=[GrammarExample(text="afi")]),
    GrammarTopic(slug="review-a1",title="A1 review and interaction",level="A1",category="discourse",summary="Combine core A1 patterns in short exchanges.",explanation="Combine core A1 patterns in short exchanges.",examples=[GrammarExample(text="akpe")]),
]

VOCABULARY_SETS=[
    VocabularySet(id="greetings_a1",level="A1",topic="Greetings",unit_ref="ee-a1-unit-1",words=[VocabularyEntry(word="Woezɔ",pos="phrase",definition="welcome/hello",example="Woezɔ")]),
    VocabularySet(id="identity_a1",level="A1",topic="Identity",unit_ref="ee-a1-unit-2",words=[VocabularyEntry(word="nye ŋkɔe...",pos="phrase",definition="my name is...",example="nye ŋkɔe...")]),
    VocabularySet(id="family_a1",level="A1",topic="Family",unit_ref="ee-a1-unit-3",words=[VocabularyEntry(word="aƒe",pos="phrase",definition="home/house",example="aƒe")]),
    VocabularySet(id="routine_a1",level="A1",topic="Routine",unit_ref="ee-a1-unit-4",words=[VocabularyEntry(word="melé...",pos="phrase",definition="I am doing...",example="melé...")]),
    VocabularySet(id="time_a1",level="A1",topic="Time",unit_ref="ee-a1-unit-5",words=[VocabularyEntry(word="egbe",pos="phrase",definition="today",example="egbe")]),
    VocabularySet(id="food_a1",level="A1",topic="Food",unit_ref="ee-a1-unit-6",words=[VocabularyEntry(word="tsi",pos="phrase",definition="water",example="tsi")]),
    VocabularySet(id="places_a1",level="A1",topic="Places",unit_ref="ee-a1-unit-7",words=[VocabularyEntry(word="afi",pos="phrase",definition="place",example="afi")]),
    VocabularySet(id="review_a1",level="A1",topic="Review",unit_ref="ee-a1-unit-8",words=[VocabularyEntry(word="akpe",pos="phrase",definition="thank you",example="akpe")]),
]

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Greetings",icon="👋",phrases=[PhrasebookEntry(text="Woezɔ",context="welcome/hello",register="neutral")]),
    PhrasebookCategory(id="identity_a1",level="A1",situation="Identity",icon="🪪",phrases=[PhrasebookEntry(text="nye ŋkɔe...",context="my name is...",register="neutral")]),
    PhrasebookCategory(id="family_a1",level="A1",situation="Family",icon="👨‍👩‍👧",phrases=[PhrasebookEntry(text="aƒe",context="home/house",register="neutral")]),
    PhrasebookCategory(id="routine_a1",level="A1",situation="Routine",icon="⏰",phrases=[PhrasebookEntry(text="melé...",context="I am doing...",register="neutral")]),
]

CURRICULUM={}
for level in LEVELS:
    if level=="A1":
        CURRICULUM[level]=[
            CurriculumUnit(id="ee-a1-unit-1",level="A1",unit_number=1,title="Greetings and introductions",grammar_points=["greetings-a1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ee-a1-unit-2",level="A1",unit_number=2,title="Personal identity",grammar_points=["identity-a1"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ee-a1-unit-3",level="A1",unit_number=3,title="Family and home",grammar_points=["family-a1"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ee-a1-unit-4",level="A1",unit_number=4,title="Daily routine",grammar_points=["routine-a1"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ee-a1-unit-5",level="A1",unit_number=5,title="Time and daily schedule",grammar_points=["time-a1"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ee-a1-unit-6",level="A1",unit_number=6,title="Food and drink",grammar_points=["food-a1"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ee-a1-unit-7",level="A1",unit_number=7,title="Places and location",grammar_points=["places-a1"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="ee-a1-unit-8",level="A1",unit_number=8,title="A1 review and interaction",grammar_points=["review-a1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
        ]
    else:
        CURRICULUM[level]=[CurriculumUnit(id=f"ee-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Ewe {level} communication",grammar_points=["progressive grammar and communication"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Build level-appropriate communication"],default_weeks=2)]

ASSESSMENT_BANK=[
    AssessmentQuestion(id="ee-a1-001",skill="speaking",difficulty="A1",question="You meet someone and want to greet them. Which Ewe expression should you use?",options=["Woezɔ","nye ŋkɔe...","aƒe","tsi"],correct="Woezɔ"),
    AssessmentQuestion(id="ee-a1-002",skill="communication",difficulty="A1",question="You introduce yourself and give your name. Which Ewe expression is appropriate?",options=["nye ŋkɔe...","Woezɔ","akpe","afi"],correct="nye ŋkɔe..."),
    AssessmentQuestion(id="ee-a1-003",skill="vocabulary",difficulty="A1",question="You are talking about where you live. Which Ewe expression means “home/house”?",options=["aƒe","tsi","egbe","akpe"],correct="aƒe"),
    AssessmentQuestion(id="ee-a1-004",skill="speaking",difficulty="A1",question="You describe an action you are doing. Which Ewe expression from the lesson matches “I am doing...”?",options=["melé...","Woezɔ","afi","egbe"],correct="melé..."),
    AssessmentQuestion(id="ee-a1-005",skill="vocabulary",difficulty="A1",question="You are talking about the current day. Which Ewe expression means “today”?",options=["egbe","tsi","aƒe","nye ŋkɔe..."],correct="egbe"),
    AssessmentQuestion(id="ee-a1-006",skill="vocabulary",difficulty="A1",question="You are thirsty and need water. Which Ewe word should you choose?",options=["tsi","afi","akpe","egbe"],correct="tsi"),
    AssessmentQuestion(id="ee-a1-007",skill="vocabulary",difficulty="A1",question="You are talking about a place. Which Ewe word means “place”?",options=["afi","aƒe","tsi","Woezɔ"],correct="afi"),
    AssessmentQuestion(id="ee-a1-008",skill="communication",difficulty="A1",question="Someone helps you and you want to say “thank you”. Which Ewe expression should you use?",options=["akpe","egbe","melé...","aƒe"],correct="akpe"),
    AssessmentQuestion(id="ee-a1-009",skill="communication",difficulty="A1",question="You start a short everyday exchange with a new person. Which expression is an appropriate opening?",options=["Woezɔ","tsi","afi","egbe"],correct="Woezɔ"),
    AssessmentQuestion(id="ee-a1-010",skill="production",difficulty="A1",question="You want to close a simple exchange politely by thanking the other person. Which expression should you use?",options=["akpe","aƒe","nye ŋkɔe...","melé..."],correct="akpe"),
]

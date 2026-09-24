"""Slovak A1 deep foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

GRAMMAR_TOPICS=[
    GrammarTopic(slug="greetings-a1",title="Greetings and introductions",level="A1",category="phrase",summary="Use everyday greetings and polite openings.",explanation="Use everyday greetings and polite openings.",examples=[GrammarExample(text="Dobrý deň")]),
    GrammarTopic(slug="identity-a1",title="Personal identity",level="A1",category="syntax",summary="Introduce yourself and ask for a name.",explanation="Introduce yourself and ask for a name.",examples=[GrammarExample(text="Volám sa...")]),
    GrammarTopic(slug="family-a1",title="Family and home",level="A1",category="grammar",summary="Talk about family and familiar people.",explanation="Talk about family and familiar people.",examples=[GrammarExample(text="rodina")]),
    GrammarTopic(slug="routine-a1",title="Daily routine",level="A1",category="verbs",summary="Describe simple habitual actions.",explanation="Describe simple habitual actions.",examples=[GrammarExample(text="pracujem")]),
    GrammarTopic(slug="time-a1",title="Time and daily schedule",level="A1",category="time",summary="Use basic day and time expressions.",explanation="Use basic day and time expressions.",examples=[GrammarExample(text="dnes")]),
    GrammarTopic(slug="food-a1",title="Food and drink",level="A1",category="vocabulary",summary="Identify basic food and drink needs.",explanation="Identify basic food and drink needs.",examples=[GrammarExample(text="voda")]),
    GrammarTopic(slug="places-a1",title="Places and location",level="A1",category="syntax",summary="Say where people or things are.",explanation="Say where people or things are.",examples=[GrammarExample(text="doma")]),
    GrammarTopic(slug="review-a1",title="A1 review and interaction",level="A1",category="discourse",summary="Combine core A1 patterns in short exchanges.",explanation="Combine core A1 patterns in short exchanges.",examples=[GrammarExample(text="Ďakujem")]),
]

VOCABULARY_SETS=[
    VocabularySet(id="greetings_a1",level="A1",topic="Pozdravy",unit_ref="sk-a1-unit-1",words=[VocabularyEntry(word="Dobrý deň",pos="phrase",definition="hello/good day",example="Dobrý deň! Ako sa máte?")]),
    VocabularySet(id="identity_a1",level="A1",topic="Predstavenie",unit_ref="sk-a1-unit-2",words=[VocabularyEntry(word="Volám sa...",pos="phrase",definition="my name is...",example="Volám sa Peter.")]),
    VocabularySet(id="family_a1",level="A1",topic="Rodina",unit_ref="sk-a1-unit-3",words=[VocabularyEntry(word="rodina",pos="phrase",definition="family",example="Moja rodina býva v Bratislave.")]),
    VocabularySet(id="routine_a1",level="A1",topic="Rutina",unit_ref="sk-a1-unit-4",words=[VocabularyEntry(word="pracujem",pos="phrase",definition="I work",example="Dnes pracujem v kancelárii.")]),
    VocabularySet(id="time_a1",level="A1",topic="Čas",unit_ref="sk-a1-unit-5",words=[VocabularyEntry(word="dnes",pos="phrase",definition="today",example="Dnes sa učím po slovensky.")]),
    VocabularySet(id="food_a1",level="A1",topic="Jedlo",unit_ref="sk-a1-unit-6",words=[VocabularyEntry(word="voda",pos="phrase",definition="water",example="Prosím si pohár vody.")]),
    VocabularySet(id="places_a1",level="A1",topic="Miesta",unit_ref="sk-a1-unit-7",words=[VocabularyEntry(word="doma",pos="phrase",definition="at home",example="Som dnes doma.")]),
    VocabularySet(id="review_a1",level="A1",topic="Opakovanie",unit_ref="sk-a1-unit-8",words=[VocabularyEntry(word="Ďakujem",pos="phrase",definition="thank you",example="Ďakujem za pomoc.")]),
]

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Pozdravy",icon="👋",phrases=[PhrasebookEntry(text="Dobrý deň!",context="greeting",register="neutral"),PhrasebookEntry(text="Ako sa máte?",context="asking how someone is",register="neutral"),PhrasebookEntry(text="Volám sa Peter.",context="introducing yourself",register="neutral")]),
    PhrasebookCategory(id="shopping_a1",level="A1",situation="Nakupovanie",icon="🛒",phrases=[PhrasebookEntry(text="Koľko to stojí?",context="asking the price",register="neutral"),PhrasebookEntry(text="Prosím si toto.",context="requesting an item",register="neutral"),PhrasebookEntry(text="Prosím si vodu.",context="asking for water",register="neutral")]),
    PhrasebookCategory(id="directions_a1",level="A1",situation="Smer",icon="🧭",phrases=[PhrasebookEntry(text="Kde je škola?",context="asking for a location",register="neutral"),PhrasebookEntry(text="Kde je stanica?",context="asking for a station",register="neutral"),PhrasebookEntry(text="Doľava alebo doprava?",context="checking a direction",register="neutral")]),
    PhrasebookCategory(id="help_a1",level="A1",situation="Pomoc",icon="🆘",phrases=[PhrasebookEntry(text="Prosím, pomôžte mi.",context="asking for help",register="neutral"),PhrasebookEntry(text="Nerozumiem.",context="saying you do not understand",register="neutral"),PhrasebookEntry(text="Môžete to zopakovať?",context="asking someone to repeat",register="neutral")]),
]

CURRICULUM={}
for level in LEVELS:
    if level=="A1":
        CURRICULUM[level]=[
            CurriculumUnit(id="sk-a1-unit-1",level="A1",unit_number=1,title="Greetings and introductions",grammar_points=["greetings-a1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sk-a1-unit-2",level="A1",unit_number=2,title="Personal identity",grammar_points=["identity-a1"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sk-a1-unit-3",level="A1",unit_number=3,title="Family and home",grammar_points=["family-a1"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sk-a1-unit-4",level="A1",unit_number=4,title="Daily routine",grammar_points=["routine-a1"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sk-a1-unit-5",level="A1",unit_number=5,title="Time and daily schedule",grammar_points=["time-a1"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sk-a1-unit-6",level="A1",unit_number=6,title="Food and drink",grammar_points=["food-a1"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sk-a1-unit-7",level="A1",unit_number=7,title="Places and location",grammar_points=["places-a1"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
            CurriculumUnit(id="sk-a1-unit-8",level="A1",unit_number=8,title="A1 review and interaction",grammar_points=["review-a1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","speaking","listening","review"],competency_checklist=["Recognize the target pattern","Produce a short everyday exchange"],default_weeks=1),
        ]
    else:
        CURRICULUM[level]=[CurriculumUnit(id=f"sk-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Slovak {level} communication",grammar_points=["progressive grammar and communication"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Build level-appropriate communication"],default_weeks=2)]

ASSESSMENT_BANK=[AssessmentQuestion(id="sk-a1-001",skill="speaking",difficulty="A1",question="You meet someone during the day. Which Slovak phrase is a natural greeting?",options=["Dobrý deň!","Koľko to stojí?","Nerozumiem.","Kde je škola?"],correct="Dobrý deň!"),
AssessmentQuestion(id="sk-a1-002",skill="communication",difficulty="A1",question="You introduce yourself as Peter. Which Slovak sentence should you use?",options=["Volám sa Peter.","Prosím si toto.","Dnes sa učím po slovensky.","Som dnes doma."],correct="Volám sa Peter."),
AssessmentQuestion(id="sk-a1-003",skill="vocabulary",difficulty="A1",question="You are talking about your relatives. Which Slovak word means “family”?",options=["rodina","voda","dnes","škola"],correct="rodina"),
AssessmentQuestion(id="sk-a1-004",skill="grammar",difficulty="A1",question="You tell a friend that you are working today. Which sentence is appropriate?",options=["Dnes pracujem v kancelárii.","Moja rodina býva v Bratislave.","Prosím si pohár vody.","Som dnes doma."],correct="Dnes pracujem v kancelárii."),
AssessmentQuestion(id="sk-a1-005",skill="vocabulary",difficulty="A1",question="You are thirsty. Which Slovak word means “water”?",options=["voda","rodina","pracujem","stanica"],correct="voda"),
AssessmentQuestion(id="sk-a1-006",skill="communication",difficulty="A1",question="You want to ask the price in a shop. Which Slovak phrase should you use?",options=["Koľko to stojí?","Ako sa máte?","Nerozumiem.","Kde je stanica?"],correct="Koľko to stojí?"),
AssessmentQuestion(id="sk-a1-007",skill="communication",difficulty="A1",question="You need directions to the school. Which Slovak question should you use?",options=["Kde je škola?","Prosím si vodu.","Ďakujem za pomoc.","Volám sa Peter."],correct="Kde je škola?"),
AssessmentQuestion(id="sk-a1-008",skill="communication",difficulty="A1",question="You do not understand what someone said. Which Slovak phrase should you use?",options=["Nerozumiem.","Dobrý deň!","Koľko to stojí?","Kde je stanica?"],correct="Nerozumiem."),
AssessmentQuestion(id="sk-a1-009",skill="communication",difficulty="A1",question="You need someone to repeat their words. Which Slovak phrase is appropriate?",options=["Môžete to zopakovať?","Som dnes doma.","Prosím si toto.","Ako sa máte?"],correct="Môžete to zopakovať?"),
AssessmentQuestion(id="sk-a1-010",skill="production",difficulty="A1",question="Someone helps you and you want to thank them. Which Slovak phrase should you use?",options=["Ďakujem za pomoc.","Nerozumiem.","Kde je škola?","Koľko to stojí?"],correct="Ďakujem za pomoc.")]

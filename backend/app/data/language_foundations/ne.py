"""Nepali foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion
LEVELS=["A1","A2","B1","B2","C1","C2"]
CURRICULUM={"A1":[
CurriculumUnit(id="ne-a1-unit-1",level="A1",unit_number=1,title="Nepali: greetings",grammar_points=["ne-a1-g1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use नमस्ते in a basic exchange","Understand a short greetings interaction"],default_weeks=1),
CurriculumUnit(id="ne-a1-unit-2",level="A1",unit_number=2,title="Nepali: identity",grammar_points=["ne-a1-g2"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use नाम in a basic exchange","Understand a short identity interaction"],default_weeks=1),
CurriculumUnit(id="ne-a1-unit-3",level="A1",unit_number=3,title="Nepali: family",grammar_points=["ne-a1-g3"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use आमा in a basic exchange","Understand a short family interaction"],default_weeks=1),
CurriculumUnit(id="ne-a1-unit-4",level="A1",unit_number=4,title="Nepali: home",grammar_points=["ne-a1-g4"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use घर in a basic exchange","Understand a short home interaction"],default_weeks=1),
CurriculumUnit(id="ne-a1-unit-5",level="A1",unit_number=5,title="Nepali: routine",grammar_points=["ne-a1-g5"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use पढ्नु in a basic exchange","Understand a short routine interaction"],default_weeks=1),
CurriculumUnit(id="ne-a1-unit-6",level="A1",unit_number=6,title="Nepali: time",grammar_points=["ne-a1-g6"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use समय in a basic exchange","Understand a short time interaction"],default_weeks=1),
CurriculumUnit(id="ne-a1-unit-7",level="A1",unit_number=7,title="Nepali: food",grammar_points=["ne-a1-g7"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use पानी in a basic exchange","Understand a short food interaction"],default_weeks=1),
CurriculumUnit(id="ne-a1-unit-8",level="A1",unit_number=8,title="Nepali: places",grammar_points=["ne-a1-g8"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use विद्यालय in a basic exchange","Understand a short places interaction"],default_weeks=1)
]}
for level in LEVELS[1:]:
 CURRICULUM[level]=[CurriculumUnit(id=f"ne-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Nepali {level} communication",grammar_points=["intermediate grammar"],vocabulary_set_ids=[],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Handle extended communication"],default_weeks=2)]
GRAMMAR_TOPICS=[
GrammarTopic(slug="ne-a1-g1",title="Pronouns",level="A1",category="grammar",summary="Use pronouns in basic communication.",explanation="Practice pronouns through short everyday exchanges.",examples=[GrammarExample(text="म विद्यार्थी हुँ।")]),
GrammarTopic(slug="ne-a1-g2",title="Copula",level="A1",category="grammar",summary="Use copula in basic communication.",explanation="Practice copula through short everyday exchanges.",examples=[GrammarExample(text="यो शिक्षक हो।")]),
GrammarTopic(slug="ne-a1-g3",title="Present",level="A1",category="grammar",summary="Use present in basic communication.",explanation="Practice present through short everyday exchanges.",examples=[GrammarExample(text="म पढ्छु।")]),
GrammarTopic(slug="ne-a1-g4",title="Negation",level="A1",category="grammar",summary="Use negation in basic communication.",explanation="Practice negation through short everyday exchanges.",examples=[GrammarExample(text="म घरमा छैन।")]),
GrammarTopic(slug="ne-a1-g5",title="Questions",level="A1",category="grammar",summary="Use questions in basic communication.",explanation="Practice questions through short everyday exchanges.",examples=[GrammarExample(text="तपाईं कहाँ हुनुहुन्छ?")]),
GrammarTopic(slug="ne-a1-g6",title="Possession",level="A1",category="grammar",summary="Use possession in basic communication.",explanation="Practice possession through short everyday exchanges.",examples=[GrammarExample(text="यो मेरो किताब हो।")]),
GrammarTopic(slug="ne-a1-g7",title="Locative",level="A1",category="grammar",summary="Use locative in basic communication.",explanation="Practice locative through short everyday exchanges.",examples=[GrammarExample(text="म घरमा छु।")]),
GrammarTopic(slug="ne-a1-g8",title="Plural",level="A1",category="grammar",summary="Use plural in basic communication.",explanation="Practice plural through short everyday exchanges.",examples=[GrammarExample(text="मान्छेहरू यहाँ छन्।")])
]
VOCABULARY_SETS=[
VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="ne-a1-unit-1",words=[VocabularyEntry(word="नमस्ते",pos="noun",definition="hello",example="नमस्ते!")]),
VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="ne-a1-unit-2",words=[VocabularyEntry(word="नाम",pos="noun",definition="name",example="मेरो नाम सीता हो।")]),
VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="ne-a1-unit-3",words=[VocabularyEntry(word="आमा",pos="noun",definition="mother",example="आमा घरमा हुनुहुन्छ।")]),
VocabularySet(id="home_a1",level="A1",topic="home",unit_ref="ne-a1-unit-4",words=[VocabularyEntry(word="घर",pos="noun",definition="house",example="मेरो घर ठूलो छ।")]),
VocabularySet(id="routine_a1",level="A1",topic="routine",unit_ref="ne-a1-unit-5",words=[VocabularyEntry(word="पढ्नु",pos="noun",definition="to study",example="म बिहान पढ्छु।")]),
VocabularySet(id="time_a1",level="A1",topic="time",unit_ref="ne-a1-unit-6",words=[VocabularyEntry(word="समय",pos="noun",definition="time",example="समय कति भयो?")]),
VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="ne-a1-unit-7",words=[VocabularyEntry(word="पानी",pos="noun",definition="water",example="मलाई पानी चाहिन्छ।")]),
VocabularySet(id="places_a1",level="A1",topic="places",unit_ref="ne-a1-unit-8",words=[VocabularyEntry(word="विद्यालय",pos="noun",definition="school",example="म विद्यालयमा छु।")])
]
PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="ne_a1_phrase_1",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="नमस्ते।",context="Greetings",register="neutral"),PhrasebookEntry(text="नमस्ते! तपाईंलाई भेटेर खुशी लाग्यो।",context="Greetings",register="neutral"),PhrasebookEntry(text="शुभ प्रभात!",context="Greetings",register="neutral")]),
PhrasebookCategory(id="ne_a1_phrase_2",level="A1",situation="thanks",icon="💬",phrases=[PhrasebookEntry(text="धन्यवाद।",context="Thanks",register="neutral"),PhrasebookEntry(text="धेरै धन्यवाद।",context="Thanks",register="neutral"),PhrasebookEntry(text="स्वागत छ।",context="Thanks",register="neutral")]),
PhrasebookCategory(id="ne_a1_phrase_3",level="A1",situation="help",icon="💬",phrases=[PhrasebookEntry(text="कृपया मद्दत गर्नुहोस्।",context="Help",register="neutral"),PhrasebookEntry(text="म बुझिनँ।",context="Help",register="neutral"),PhrasebookEntry(text="फेरि भन्नुहोस्, कृपया।",context="Help",register="neutral")]),
PhrasebookCategory(id="ne_a1_phrase_4",level="A1",situation="directions",icon="💬",phrases=[PhrasebookEntry(text="विद्यालय कहाँ छ?",context="Directions",register="neutral"),PhrasebookEntry(text="बजार कहाँ छ?",context="Directions",register="neutral"),PhrasebookEntry(text="बायाँ जानुहोस्।",context="Directions",register="neutral")])]
ASSESSMENT_BANK=[
AssessmentQuestion(id="ne-a1-001",skill="vocabulary",difficulty="A1",question="Which Nepali word means 'water'?",options=["पानी","घर","आमा","विद्यालय"],correct="पानी"),
AssessmentQuestion(id="ne-a1-002",skill="grammar",difficulty="A1",question="Which sentence says 'I am at home'?",options=["म घरमा छु।","म विद्यालय जान्छु।","म पानी पिउँछु।","यो किताब हो।"],correct="म घरमा छु।"),
AssessmentQuestion(id="ne-a1-003",skill="vocabulary",difficulty="A1",question="What does आमा mean?",options=["mother","father","friend","teacher"],correct="mother"),
AssessmentQuestion(id="ne-a1-004",skill="grammar",difficulty="A1",question="Which question asks 'What is your name?'",options=["तपाईंको नाम के हो?","तपाईं कहाँ हुनुहुन्छ?","यो के हो?","कति बजे हो?"],"correct"="तपाईंको नाम के हो?"),
AssessmentQuestion(id="ne-a1-005",skill="reading",difficulty="A1",question="विद्यालय नजिकै छ। Where is the school?",options=["Nearby","At home","In the market","Far away"],correct="Nearby"),
AssessmentQuestion(id="ne-a1-006",skill="vocabulary",difficulty="A1",question="Which word means 'name'?",options=["नाम","समय","पानी","घर"],correct="नाम"),
AssessmentQuestion(id="ne-a1-007",skill="communication",difficulty="A1",question="Which phrase asks someone to repeat?",options=["फेरि भन्नुहोस्।","धन्यवाद।","नमस्ते।","बिदा।"],correct="फेरि भन्नुहोस्।"),
AssessmentQuestion(id="ne-a1-008",skill="grammar",difficulty="A1",question="Which sentence says 'I drink water'?",options=["म पानी पिउँछु।","म घरमा छु।","म पढ्छु।","यो घर हो।"],correct="म पानी पिउँछु।"),
AssessmentQuestion(id="ne-a1-009",skill="vocabulary",difficulty="A1",question="What does समय mean?",options=["time","school","water","name"],correct="time"),
AssessmentQuestion(id="ne-a1-010",skill="communication",difficulty="A1",question="Which is a natural greeting?",options=["नमस्ते!","पानी चाहिन्छ।","घर कहाँ छ?","म बुझिनँ।"],correct="नमस्ते!")
]

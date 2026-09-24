"""Punjabi foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion
LEVELS=["A1","A2","B1","B2","C1","C2"]
CURRICULUM={"A1":[
CurriculumUnit(id="pa-a1-unit-1",level="A1",unit_number=1,title="Punjabi: greetings",grammar_points=["pa-a1-g1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ਸਤ ਸ੍ਰੀ ਅਕਾਲ in a basic exchange","Understand a short greetings interaction"],default_weeks=1),
CurriculumUnit(id="pa-a1-unit-2",level="A1",unit_number=2,title="Punjabi: identity",grammar_points=["pa-a1-g2"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ਨਾਮ in a basic exchange","Understand a short identity interaction"],default_weeks=1),
CurriculumUnit(id="pa-a1-unit-3",level="A1",unit_number=3,title="Punjabi: family",grammar_points=["pa-a1-g3"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ਮਾਂ in a basic exchange","Understand a short family interaction"],default_weeks=1),
CurriculumUnit(id="pa-a1-unit-4",level="A1",unit_number=4,title="Punjabi: home",grammar_points=["pa-a1-g4"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ਘਰ in a basic exchange","Understand a short home interaction"],default_weeks=1),
CurriculumUnit(id="pa-a1-unit-5",level="A1",unit_number=5,title="Punjabi: routine",grammar_points=["pa-a1-g5"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ਪੜ੍ਹਨਾ in a basic exchange","Understand a short routine interaction"],default_weeks=1),
CurriculumUnit(id="pa-a1-unit-6",level="A1",unit_number=6,title="Punjabi: time",grammar_points=["pa-a1-g6"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ਸਮਾਂ in a basic exchange","Understand a short time interaction"],default_weeks=1),
CurriculumUnit(id="pa-a1-unit-7",level="A1",unit_number=7,title="Punjabi: food",grammar_points=["pa-a1-g7"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ਪਾਣੀ in a basic exchange","Understand a short food interaction"],default_weeks=1),
CurriculumUnit(id="pa-a1-unit-8",level="A1",unit_number=8,title="Punjabi: places",grammar_points=["pa-a1-g8"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ਸਕੂਲ in a basic exchange","Understand a short places interaction"],default_weeks=1)
]}
for level in LEVELS[1:]:
 CURRICULUM[level]=[CurriculumUnit(id=f"pa-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Punjabi {level} communication",grammar_points=["intermediate grammar"],vocabulary_set_ids=[],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Handle extended communication"],default_weeks=2)]
GRAMMAR_TOPICS=[
GrammarTopic(slug="pa-a1-g1",title="Pronouns",level="A1",category="grammar",summary="Use pronouns in basic communication.",explanation="Practice pronouns through short everyday exchanges.",examples=[GrammarExample(text="ਮੈਂ ਵਿਦਿਆਰਥੀ ਹਾਂ।")]),
GrammarTopic(slug="pa-a1-g2",title="Copula",level="A1",category="grammar",summary="Use copula in basic communication.",explanation="Practice copula through short everyday exchanges.",examples=[GrammarExample(text="ਇਹ ਅਧਿਆਪਕ ਹੈ।")]),
GrammarTopic(slug="pa-a1-g3",title="Present",level="A1",category="grammar",summary="Use present in basic communication.",explanation="Practice present through short everyday exchanges.",examples=[GrammarExample(text="ਮੈਂ ਪੜ੍ਹਦਾ ਹਾਂ।")]),
GrammarTopic(slug="pa-a1-g4",title="Negation",level="A1",category="grammar",summary="Use negation in basic communication.",explanation="Practice negation through short everyday exchanges.",examples=[GrammarExample(text="ਮੈਂ ਘਰ ਨਹੀਂ ਹਾਂ।")]),
GrammarTopic(slug="pa-a1-g5",title="Questions",level="A1",category="grammar",summary="Use questions in basic communication.",explanation="Practice questions through short everyday exchanges.",examples=[GrammarExample(text="ਤੁਸੀਂ ਕਿੱਥੇ ਹੋ?")]),
GrammarTopic(slug="pa-a1-g6",title="Possession",level="A1",category="grammar",summary="Use possession in basic communication.",explanation="Practice possession through short everyday exchanges.",examples=[GrammarExample(text="ਇਹ ਮੇਰੀ ਕਿਤਾਬ ਹੈ।")]),
GrammarTopic(slug="pa-a1-g7",title="Locative",level="A1",category="grammar",summary="Use locative in basic communication.",explanation="Practice locative through short everyday exchanges.",examples=[GrammarExample(text="ਮੈਂ ਘਰ ਵਿੱਚ ਹਾਂ।")]),
GrammarTopic(slug="pa-a1-g8",title="Plural",level="A1",category="grammar",summary="Use plural in basic communication.",explanation="Practice plural through short everyday exchanges.",examples=[GrammarExample(text="ਲੋਕ ਇੱਥੇ ਹਨ।")])
]
VOCABULARY_SETS=[
VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="pa-a1-unit-1",words=[VocabularyEntry(word="ਸਤ ਸ੍ਰੀ ਅਕਾਲ",pos="noun",definition="hello",example="ਸਤ ਸ੍ਰੀ ਅਕਾਲ!")]),
VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="pa-a1-unit-2",words=[VocabularyEntry(word="ਨਾਮ",pos="noun",definition="name",example="ਮੇਰਾ ਨਾਮ ਅਮਨ ਹੈ।")]),
VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="pa-a1-unit-3",words=[VocabularyEntry(word="ਮਾਂ",pos="noun",definition="mother",example="ਮਾਂ ਘਰ ਵਿੱਚ ਹੈ।")]),
VocabularySet(id="home_a1",level="A1",topic="home",unit_ref="pa-a1-unit-4",words=[VocabularyEntry(word="ਘਰ",pos="noun",definition="house",example="ਮੇਰਾ ਘਰ ਵੱਡਾ ਹੈ।")]),
VocabularySet(id="routine_a1",level="A1",topic="routine",unit_ref="pa-a1-unit-5",words=[VocabularyEntry(word="ਪੜ੍ਹਨਾ",pos="noun",definition="to study",example="ਮੈਂ ਸਵੇਰੇ ਪੜ੍ਹਦਾ ਹਾਂ।")]),
VocabularySet(id="time_a1",level="A1",topic="time",unit_ref="pa-a1-unit-6",words=[VocabularyEntry(word="ਸਮਾਂ",pos="noun",definition="time",example="ਸਮਾਂ ਕੀ ਹੋਇਆ ਹੈ?")]),
VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="pa-a1-unit-7",words=[VocabularyEntry(word="ਪਾਣੀ",pos="noun",definition="water",example="ਮੈਨੂੰ ਪਾਣੀ ਚਾਹੀਦਾ ਹੈ।")]),
VocabularySet(id="places_a1",level="A1",topic="places",unit_ref="pa-a1-unit-8",words=[VocabularyEntry(word="ਸਕੂਲ",pos="noun",definition="school",example="ਮੈਂ ਸਕੂਲ ਵਿੱਚ ਹਾਂ।")])
]
PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="pa_a1_phrase_1",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="ਸਤ ਸ੍ਰੀ ਅਕਾਲ।",context="Hello.",register="neutral")]),
PhrasebookCategory(id="pa_a1_phrase_2",level="A1",situation="thanks",icon="💬",phrases=[PhrasebookEntry(text="ਧੰਨਵਾਦ।",context="Thank you.",register="neutral")]),
PhrasebookCategory(id="pa_a1_phrase_3",level="A1",situation="help",icon="💬",phrases=[PhrasebookEntry(text="ਕਿਰਪਾ ਕਰਕੇ ਮਦਦ ਕਰੋ।",context="Please help me.",register="neutral")]),
PhrasebookCategory(id="pa_a1_phrase_4",level="A1",situation="directions",icon="💬",phrases=[PhrasebookEntry(text="ਸਕੂਲ ਕਿੱਥੇ ਹੈ?",context="Where is the school?",register="neutral")])
]
ASSESSMENT_BANK=[
AssessmentQuestion(id="pa-a1-001",skill="vocabulary",difficulty="A1",question="Choose the correct Punjabi expression for this A1 task.",options=["ਸਤ ਸ੍ਰੀ ਅਕਾਲ","ਨਾਮ","ਮਾਂ","ਘਰ"],correct="ਸਤ ਸ੍ਰੀ ਅਕਾਲ"),
AssessmentQuestion(id="pa-a1-002",skill="grammar",difficulty="A1",question="Choose the correct Punjabi expression for this A1 task.",options=["ਨਾਮ","ਮਾਂ","ਘਰ","ਪੜ੍ਹਨਾ"],correct="ਨਾਮ"),
AssessmentQuestion(id="pa-a1-003",skill="reading",difficulty="A1",question="Choose the correct Punjabi expression for this A1 task.",options=["ਮਾਂ","ਘਰ","ਪੜ੍ਹਨਾ","ਸਮਾਂ"],correct="ਮਾਂ"),
AssessmentQuestion(id="pa-a1-004",skill="speaking",difficulty="A1",question="Choose the correct Punjabi expression for this A1 task.",options=["ਘਰ","ਪੜ੍ਹਨਾ","ਸਮਾਂ","ਪਾਣੀ"],correct="ਘਰ"),
AssessmentQuestion(id="pa-a1-005",skill="vocabulary",difficulty="A1",question="Choose the correct Punjabi expression for this A1 task.",options=["ਪੜ੍ਹਨਾ","ਸਮਾਂ","ਪਾਣੀ","ਸਕੂਲ"],correct="ਪੜ੍ਹਨਾ"),
AssessmentQuestion(id="pa-a1-006",skill="grammar",difficulty="A1",question="Choose the correct Punjabi expression for this A1 task.",options=["ਸਮਾਂ","ਪਾਣੀ","ਸਕੂਲ","ਸਤ ਸ੍ਰੀ ਅਕਾਲ"],correct="ਸਮਾਂ"),
AssessmentQuestion(id="pa-a1-007",skill="reading",difficulty="A1",question="Choose the correct Punjabi expression for this A1 task.",options=["ਪਾਣੀ","ਸਕੂਲ","ਸਤ ਸ੍ਰੀ ਅਕਾਲ","ਨਾਮ"],correct="ਪਾਣੀ"),
AssessmentQuestion(id="pa-a1-008",skill="speaking",difficulty="A1",question="Choose the correct Punjabi expression for this A1 task.",options=["ਸਕੂਲ","ਸਤ ਸ੍ਰੀ ਅਕਾਲ","ਨਾਮ","ਮਾਂ"],correct="ਸਕੂਲ"),
AssessmentQuestion(id="pa-a1-009",skill="vocabulary",difficulty="A1",question="Choose the correct Punjabi expression for this A1 task.",options=["ਸਤ ਸ੍ਰੀ ਅਕਾਲ","ਨਾਮ","ਮਾਂ","ਘਰ"],correct="ਸਤ ਸ੍ਰੀ ਅਕਾਲ"),
AssessmentQuestion(id="pa-a1-010",skill="grammar",difficulty="A1",question="Choose the correct Punjabi expression for this A1 task.",options=["ਨਾਮ","ਮਾਂ","ਘਰ","ਪੜ੍ਹਨਾ"],correct="ਨਾਮ")
]

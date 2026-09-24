"""Sinhala foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion
LEVELS=["A1","A2","B1","B2","C1","C2"]
CURRICULUM={"A1":[
CurriculumUnit(id="si-a1-unit-1",level="A1",unit_number=1,title="Sinhala: greetings",grammar_points=["si-a1-g1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ආයුබෝවන් in a basic exchange","Understand a short greetings interaction"],default_weeks=1),
CurriculumUnit(id="si-a1-unit-2",level="A1",unit_number=2,title="Sinhala: identity",grammar_points=["si-a1-g2"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use නම in a basic exchange","Understand a short identity interaction"],default_weeks=1),
CurriculumUnit(id="si-a1-unit-3",level="A1",unit_number=3,title="Sinhala: family",grammar_points=["si-a1-g3"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use අම්මා in a basic exchange","Understand a short family interaction"],default_weeks=1),
CurriculumUnit(id="si-a1-unit-4",level="A1",unit_number=4,title="Sinhala: home",grammar_points=["si-a1-g4"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ගෙදර in a basic exchange","Understand a short home interaction"],default_weeks=1),
CurriculumUnit(id="si-a1-unit-5",level="A1",unit_number=5,title="Sinhala: routine",grammar_points=["si-a1-g5"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use ඉගෙන ගන්නවා in a basic exchange","Understand a short routine interaction"],default_weeks=1),
CurriculumUnit(id="si-a1-unit-6",level="A1",unit_number=6,title="Sinhala: time",grammar_points=["si-a1-g6"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use වේලාව in a basic exchange","Understand a short time interaction"],default_weeks=1),
CurriculumUnit(id="si-a1-unit-7",level="A1",unit_number=7,title="Sinhala: food",grammar_points=["si-a1-g7"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use වතුර in a basic exchange","Understand a short food interaction"],default_weeks=1),
CurriculumUnit(id="si-a1-unit-8",level="A1",unit_number=8,title="Sinhala: places",grammar_points=["si-a1-g8"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=["Use පාසල in a basic exchange","Understand a short places interaction"],default_weeks=1)
]}
for level in LEVELS[1:]:
 CURRICULUM[level]=[CurriculumUnit(id=f"si-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Sinhala {level} communication",grammar_points=["intermediate grammar"],vocabulary_set_ids=[],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Handle extended communication"],default_weeks=2)]
GRAMMAR_TOPICS=[
GrammarTopic(slug="si-a1-g1",title="Pronouns",level="A1",category="grammar",summary="Use pronouns in basic communication.",explanation="Practice pronouns through short everyday exchanges.",examples=[GrammarExample(text="මම ශිෂ්‍යයෙක්.")]),
GrammarTopic(slug="si-a1-g2",title="Copula",level="A1",category="grammar",summary="Use copula in basic communication.",explanation="Practice copula through short everyday exchanges.",examples=[GrammarExample(text="මේ ගුරුවරයා.")]),
GrammarTopic(slug="si-a1-g3",title="Present",level="A1",category="grammar",summary="Use present in basic communication.",explanation="Practice present through short everyday exchanges.",examples=[GrammarExample(text="මම ඉගෙන ගන්නවා.")]),
GrammarTopic(slug="si-a1-g4",title="Negation",level="A1",category="grammar",summary="Use negation in basic communication.",explanation="Practice negation through short everyday exchanges.",examples=[GrammarExample(text="මම ගෙදර නැහැ.")]),
GrammarTopic(slug="si-a1-g5",title="Questions",level="A1",category="grammar",summary="Use questions in basic communication.",explanation="Practice questions through short everyday exchanges.",examples=[GrammarExample(text="ඔයා කොහෙද?")]),
GrammarTopic(slug="si-a1-g6",title="Possession",level="A1",category="grammar",summary="Use possession in basic communication.",explanation="Practice possession through short everyday exchanges.",examples=[GrammarExample(text="මේ මගේ පොත.")]),
GrammarTopic(slug="si-a1-g7",title="Locative",level="A1",category="grammar",summary="Use locative in basic communication.",explanation="Practice locative through short everyday exchanges.",examples=[GrammarExample(text="මම ගෙදර ඉන්නවා.")]),
GrammarTopic(slug="si-a1-g8",title="Plural",level="A1",category="grammar",summary="Use plural in basic communication.",explanation="Practice plural through short everyday exchanges.",examples=[GrammarExample(text="මිනිසුන් මෙහි ඉන්නවා.")])
]
VOCABULARY_SETS=[
VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="si-a1-unit-1",words=[VocabularyEntry(word="ආයුබෝවන්",pos="noun",definition="hello",example="ආයුබෝවන්!")]),
VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="si-a1-unit-2",words=[VocabularyEntry(word="නම",pos="noun",definition="name",example="මගේ නම නිමල්.")]),
VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="si-a1-unit-3",words=[VocabularyEntry(word="අම්මා",pos="noun",definition="mother",example="අම්මා ගෙදර ඉන්නවා.")]),
VocabularySet(id="home_a1",level="A1",topic="home",unit_ref="si-a1-unit-4",words=[VocabularyEntry(word="ගෙදර",pos="noun",definition="home",example="මගේ ගෙදර ලොකුයි.")]),
VocabularySet(id="routine_a1",level="A1",topic="routine",unit_ref="si-a1-unit-5",words=[VocabularyEntry(word="ඉගෙන ගන්නවා",pos="noun",definition="study",example="මම උදේ ඉගෙන ගන්නවා.")]),
VocabularySet(id="time_a1",level="A1",topic="time",unit_ref="si-a1-unit-6",words=[VocabularyEntry(word="වේලාව",pos="noun",definition="time",example="වේලාව කීයද?")]),
VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="si-a1-unit-7",words=[VocabularyEntry(word="වතුර",pos="noun",definition="water",example="මට වතුර ඕනේ.")]),
VocabularySet(id="places_a1",level="A1",topic="places",unit_ref="si-a1-unit-8",words=[VocabularyEntry(word="පාසල",pos="noun",definition="school",example="මම පාසලේ ඉන්නවා.")])
]
PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="si_a1_phrase_1",level="A1",situation="greetings",icon="💬",phrases=[PhrasebookEntry(text="ආයුබෝවන්.",context="greetings",register="neutral"),PhrasebookEntry(text="සුභ උදෑසනක්.",context="greetings",register="neutral"),PhrasebookEntry(text="ඔබට කොහොමද?",context="greetings",register="neutral")]),
PhrasebookCategory(id="si_a1_phrase_2",level="A1",situation="thanks",icon="💬",phrases=[PhrasebookEntry(text="ස්තුතියි.",context="thanks",register="neutral"),PhrasebookEntry(text="බොහොම ස්තුතියි.",context="thanks",register="neutral"),PhrasebookEntry(text="කමක් නැහැ.",context="thanks",register="neutral")]),
PhrasebookCategory(id="si_a1_phrase_3",level="A1",situation="help",icon="💬",phrases=[PhrasebookEntry(text="කරුණාකර උදව් කරන්න.",context="help",register="neutral"),PhrasebookEntry(text="මට තේරෙන්නේ නැහැ.",context="help",register="neutral"),PhrasebookEntry(text="ආයෙත් කියන්න, කරුණාකර.",context="help",register="neutral")]),
PhrasebookCategory(id="si_a1_phrase_4",level="A1",situation="directions",icon="💬",phrases=[PhrasebookEntry(text="පාසල කොහෙද?",context="directions",register="neutral"),PhrasebookEntry(text="වෙළඳසැල කොහෙද?",context="directions",register="neutral"),PhrasebookEntry(text="දකුණට යන්න.",context="directions",register="neutral")])]
ASSESSMENT_BANK=[
AssessmentQuestion(id="si-a1-001",skill="vocabulary",difficulty="A1",question="Which Sinhala word means 'water'?",options=["වතුර","ගෙදර","අම්මා","පාසල"],correct="වතුර"),
AssessmentQuestion(id="si-a1-002",skill="grammar",difficulty="A1",question="Which sentence says 'I am at home'?",options=["මම ගෙදර ඉන්නවා.","මම පාසලට යනවා.","මම වතුර බොනවා.","මේ පොතක්."],correct="මම ගෙදර ඉන්නවා."),
AssessmentQuestion(id="si-a1-003",skill="vocabulary",difficulty="A1",question="What does අම්මා mean?",options=["mother","father","friend","teacher"],correct="mother"),
AssessmentQuestion(id="si-a1-004",skill="grammar",difficulty="A1",question="Which question asks 'Where are you?'",options=["ඔයා කොහෙද ඉන්නේ?","ඔයාගේ නම මොකක්ද?","මේ මොකක්ද?","මිල කීයද?"],"correct"="ඔයා කොහෙද ඉන්නේ?"),
AssessmentQuestion(id="si-a1-005",skill="reading",difficulty="A1",question="පොත මේසය උඩ තියෙනවා. Where is the book?",options=["On the table","At school","At home","In the shop"],correct="On the table"),
AssessmentQuestion(id="si-a1-006",skill="vocabulary",difficulty="A1",question="Which word means 'name'?",options=["නම","වේලාව","වතුර","ගෙදර"],correct="නම"),
AssessmentQuestion(id="si-a1-007",skill="communication",difficulty="A1",question="Which phrase asks someone to repeat?",options=["ආයෙත් කියන්න.","ස්තුතියි.","ආයුබෝවන්.","ගිහින් එන්නම්."],correct="ආයෙත් කියන්න."),
AssessmentQuestion(id="si-a1-008",skill="grammar",difficulty="A1",question="Which sentence says 'I drink water'?",options=["මම වතුර බොනවා.","මම ගෙදර ඉන්නවා.","මම ඉගෙන ගන්නවා.","මේ ගෙදරක්."],correct="මම වතුර බොනවා."),
AssessmentQuestion(id="si-a1-009",skill="vocabulary",difficulty="A1",question="What does වේලාව mean?",options=["time","school","water","name"],correct="time"),
AssessmentQuestion(id="si-a1-010",skill="communication",difficulty="A1",question="Which is a natural greeting?",options=["ආයුබෝවන්!","මට වතුර ඕනේ.","පාසල කොහෙද?","මට තේරෙන්නේ නැහැ."],correct="ආයුබෝවන්!")
]

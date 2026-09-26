"""Indonesian A1 rich foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion
LEVELS=["A1","A2","B1","B2","C1","C2"]
GRAMMAR_TOPICS=[
GrammarTopic(slug="greetings-a1",title="Greetings and introductions",level="A1",category="phrase",summary="Use greetings and introductions in everyday communication.",explanation="Build accurate A1 greetings and introductions patterns with controlled practice.",examples=[GrammarExample(text="Halo"),GrammarExample(text="Halo")]),
GrammarTopic(slug="identity-a1",title="Personal identity",level="A1",category="syntax",summary="Use personal identity in everyday communication.",explanation="Build accurate A1 personal identity patterns with controlled practice.",examples=[GrammarExample(text="Nama saya..."),GrammarExample(text="Nama saya...")]),
GrammarTopic(slug="family-a1",title="Family and possession",level="A1",category="grammar",summary="Use family and possession in everyday communication.",explanation="Build accurate A1 family and possession patterns with controlled practice.",examples=[GrammarExample(text="Ini keluarga saya"),GrammarExample(text="Ini keluarga saya")]),
GrammarTopic(slug="routine-a1",title="Daily routine",level="A1",category="verbs",summary="Use daily routine in everyday communication.",explanation="Build accurate A1 daily routine patterns with controlled practice.",examples=[GrammarExample(text="Saya bekerja"),GrammarExample(text="Saya bekerja")]),
GrammarTopic(slug="time-a1",title="Time and dates",level="A1",category="time",summary="Use time and dates in everyday communication.",explanation="Build accurate A1 time and dates patterns with controlled practice.",examples=[GrammarExample(text="Hari ini"),GrammarExample(text="Hari ini")]),
GrammarTopic(slug="food-a1",title="Food and drink",level="A1",category="vocabulary",summary="Use food and drink in everyday communication.",explanation="Build accurate A1 food and drink patterns with controlled practice.",examples=[GrammarExample(text="Saya mau air"),GrammarExample(text="Saya mau air")]),
GrammarTopic(slug="places-a1",title="Places and location",level="A1",category="syntax",summary="Use places and location in everyday communication.",explanation="Build accurate A1 places and location patterns with controlled practice.",examples=[GrammarExample(text="Di rumah"),GrammarExample(text="Di rumah")]),
GrammarTopic(slug="review-a1",title="A1 review and interaction",level="A1",category="discourse",summary="Use a1 review and interaction in everyday communication.",explanation="Build accurate A1 a1 review and interaction patterns with controlled practice.",examples=[GrammarExample(text="Terima kasih"),GrammarExample(text="Terima kasih")]),
]
VOCABULARY_SETS=[
VocabularySet(id="greetings_a1",level="A1",topic="Greetings and introductions",unit_ref="id-a1-unit-1",words=[VocabularyEntry(word="Halo",pos="phrase",definition="hello",example="Halo")]),
VocabularySet(id="identity_a1",level="A1",topic="Personal identity",unit_ref="id-a1-unit-2",words=[VocabularyEntry(word="Nama saya...",pos="phrase",definition="my name is...",example="Nama saya...")]),
VocabularySet(id="family_a1",level="A1",topic="Family and possession",unit_ref="id-a1-unit-3",words=[VocabularyEntry(word="Ini keluarga saya",pos="phrase",definition="this is my family",example="Ini keluarga saya")]),
VocabularySet(id="routine_a1",level="A1",topic="Daily routine",unit_ref="id-a1-unit-4",words=[VocabularyEntry(word="Saya bekerja",pos="phrase",definition="I work",example="Saya bekerja")]),
VocabularySet(id="time_a1",level="A1",topic="Time and dates",unit_ref="id-a1-unit-5",words=[VocabularyEntry(word="Hari ini",pos="phrase",definition="today",example="Hari ini")]),
VocabularySet(id="food_a1",level="A1",topic="Food and drink",unit_ref="id-a1-unit-6",words=[VocabularyEntry(word="Saya mau air",pos="phrase",definition="I want water",example="Saya mau air")]),
VocabularySet(id="places_a1",level="A1",topic="Places and location",unit_ref="id-a1-unit-7",words=[VocabularyEntry(word="Di rumah",pos="phrase",definition="at home",example="Di rumah")]),
VocabularySet(id="review_a1",level="A1",topic="A1 review and interaction",unit_ref="id-a1-unit-8",words=[VocabularyEntry(word="Terima kasih",pos="phrase",definition="thank you",example="Terima kasih")]),
]
PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="greetings_a1",level="A1",situation="Greetings and introductions",icon="👋",phrases=[PhrasebookEntry(text="Halo",context="hello",register="neutral"),PhrasebookEntry(text="Halo",context="hello",register="polite")]),
PhrasebookCategory(id="identity_a1",level="A1",situation="Personal identity",icon="🪪",phrases=[PhrasebookEntry(text="Nama saya...",context="my name is...",register="neutral"),PhrasebookEntry(text="Nama saya...",context="my name is...",register="polite")]),
PhrasebookCategory(id="family_a1",level="A1",situation="Family and possession",icon="👨‍👩‍👧",phrases=[PhrasebookEntry(text="Ini keluarga saya",context="this is my family",register="neutral"),PhrasebookEntry(text="Ini keluarga saya",context="this is my family",register="polite")]),
PhrasebookCategory(id="routine_a1",level="A1",situation="Daily routine",icon="⏰",phrases=[PhrasebookEntry(text="Saya bekerja",context="I work",register="neutral"),PhrasebookEntry(text="Saya bekerja",context="I work",register="polite")]),
]

_ADVANCED = [
("past","Past events","A2","Talk about completed actions.","Kemarin saya pergi ke Bandung."),
("future","Plans and intentions","A2","Express plans and intentions.","Besok saya akan belajar."),
("comparatives","Comparisons and preferences","A2","Compare people, objects, and choices.","Kereta ini lebih cepat."),
("requests","Polite requests","A2","Make polite requests and instructions.","Tolong ulangi sekali lagi."),
("relative","Relative clauses with yang","B1","Combine information with yang.","Buku yang saya baca menarik."),
("conditions","Conditions and consequences","B1","Express conditions and results.","Jika hujan, kami tinggal di rumah."),
("reported","Reported information","B1","Report what another person said.","Dia mengatakan bahwa rapat dimulai pukul sembilan."),
("causation","Cause and purpose","B2","Explain causes, purposes, and results.","Kami belajar agar dapat bekerja lebih baik."),
("passive","Passive voice","B2","Focus on the object or result with passive forms.","Dokumen itu sudah dikirim."),
("discourse","Discourse connectors","B2","Organize contrast, cause, and conclusion.","Namun, hasilnya belum final."),
("formal","Formal register","C1","Adapt language to professional settings.","Mohon menyampaikan dokumen sebelum tanggal tersebut."),
("evidence","Evidence and hedging","C1","State evidence and cautious claims.","Berdasarkan data, perubahan ini mungkin signifikan."),
("nominalization","Academic nominalization","C1","Use dense noun phrases in formal prose.","Peningkatan kualitas memerlukan evaluasi."),
("pragmatics","Pragmatic meaning","C2","Interpret implication and politeness.","Apakah Anda berkenan menunggu sebentar?"),
("idioms","Idioms and figurative language","C2","Interpret figurative meaning in context.","Ia menjadi kambing hitam dalam masalah itu."),
("argumentation","Advanced argumentation","C2","Build arguments with evidence and counterpoints.","Argumen tersebut kuat, meskipun datanya terbatas."),
]
GRAMMAR_TOPICS.extend([GrammarTopic(slug=s,title=t,level=l,category="grammar",summary=d,explanation=d,examples=[GrammarExample(text=e)]) for s,t,l,d,e in _ADVANCED])

CURRICULUM={}
for level in LEVELS:
 if level=="A1":
  CURRICULUM[level]=[
CurriculumUnit(id="id-a1-unit-1",level="A1",unit_number=1,title="Greetings and introductions",grammar_points=["greetings-a1"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","speaking","listening","reading","writing","review"],competency_checklist=["Recognize the target pattern","Use it in a short exchange","Complete a controlled production task"],default_weeks=1),
CurriculumUnit(id="id-a1-unit-2",level="A1",unit_number=2,title="Personal identity",grammar_points=["identity-a1"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","speaking","listening","reading","writing","review"],competency_checklist=["Recognize the target pattern","Use it in a short exchange","Complete a controlled production task"],default_weeks=1),
CurriculumUnit(id="id-a1-unit-3",level="A1",unit_number=3,title="Family and possession",grammar_points=["family-a1"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","speaking","listening","reading","writing","review"],competency_checklist=["Recognize the target pattern","Use it in a short exchange","Complete a controlled production task"],default_weeks=1),
CurriculumUnit(id="id-a1-unit-4",level="A1",unit_number=4,title="Daily routine",grammar_points=["routine-a1"],vocabulary_set_ids=["routine_a1"],lesson_types=["grammar","vocabulary","speaking","listening","reading","writing","review"],competency_checklist=["Recognize the target pattern","Use it in a short exchange","Complete a controlled production task"],default_weeks=1),
CurriculumUnit(id="id-a1-unit-5",level="A1",unit_number=5,title="Time and dates",grammar_points=["time-a1"],vocabulary_set_ids=["time_a1"],lesson_types=["grammar","vocabulary","speaking","listening","reading","writing","review"],competency_checklist=["Recognize the target pattern","Use it in a short exchange","Complete a controlled production task"],default_weeks=1),
CurriculumUnit(id="id-a1-unit-6",level="A1",unit_number=6,title="Food and drink",grammar_points=["food-a1"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","speaking","listening","reading","writing","review"],competency_checklist=["Recognize the target pattern","Use it in a short exchange","Complete a controlled production task"],default_weeks=1),
CurriculumUnit(id="id-a1-unit-7",level="A1",unit_number=7,title="Places and location",grammar_points=["places-a1"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","speaking","listening","reading","writing","review"],competency_checklist=["Recognize the target pattern","Use it in a short exchange","Complete a controlled production task"],default_weeks=1),
CurriculumUnit(id="id-a1-unit-8",level="A1",unit_number=8,title="A1 review and interaction",grammar_points=["review-a1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","speaking","listening","reading","writing","review"],competency_checklist=["Recognize the target pattern","Use it in a short exchange","Complete a controlled production task"],default_weeks=1),
]
 else:\n  base = ["past","future","comparatives","requests"] if level=="A2" else (["relative","conditions","reported","causation"] if level=="B1" else (["passive","discourse","causation","relative"] if level=="B2" else (["formal","evidence","nominalization","discourse"] if level=="C1" else ["pragmatics","idioms","argumentation","formal"])))\n  CURRICULUM[level]=[CurriculumUnit(id=f"id-{level.lower()}-unit-{i+1}",level=level,unit_number=i+1,title=f"Indonesian {level} · {topic}",grammar_points=[slug],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","writing","speaking","listening","review"],competency_checklist=[f"Communicate at {level} level",f"Apply Indonesian grammar in context"],default_weeks=2) for i,(slug,topic) in enumerate([(x,next(t for s,t,*_ in _ADVANCED if s==x)) for x in base])]
ASSESSMENT_BANK=[
AssessmentQuestion(id="id-a1-001",skill="speaking",difficulty="A1",question="Which expression matches 'hello'?",options=["Halo","advanced academic phrase","unrelated expression","technical term"],correct="Halo"),
AssessmentQuestion(id="id-a1-002",skill="vocabulary",difficulty="A1",question="Which expression matches 'my name is...'?",options=["Nama saya...","advanced academic phrase","unrelated expression","technical term"],correct="Nama saya..."),
AssessmentQuestion(id="id-a1-003",skill="grammar",difficulty="A1",question="Which expression matches 'this is my family'?",options=["Ini keluarga saya","advanced academic phrase","unrelated expression","technical term"],correct="Ini keluarga saya"),
AssessmentQuestion(id="id-a1-004",skill="listening",difficulty="A1",question="Which expression matches 'I work'?",options=["Saya bekerja","advanced academic phrase","unrelated expression","technical term"],correct="Saya bekerja"),
AssessmentQuestion(id="id-a1-005",skill="speaking",difficulty="A1",question="Which expression matches 'today'?",options=["Hari ini","advanced academic phrase","unrelated expression","technical term"],correct="Hari ini"),
AssessmentQuestion(id="id-a1-006",skill="vocabulary",difficulty="A1",question="Which expression matches 'I want water'?",options=["Saya mau air","advanced academic phrase","unrelated expression","technical term"],correct="Saya mau air"),
AssessmentQuestion(id="id-a1-007",skill="grammar",difficulty="A1",question="Which expression matches 'at home'?",options=["Di rumah","advanced academic phrase","unrelated expression","technical term"],correct="Di rumah"),
AssessmentQuestion(id="id-a1-008",skill="listening",difficulty="A1",question="Which expression matches 'thank you'?",options=["Terima kasih","advanced academic phrase","unrelated expression","technical term"],correct="Terima kasih"),
]

"""Estonian A1 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def _g(slug,title,summary,examples):
    return GrammarTopic(slug=slug,title=title,level="A1",category="core",summary=summary,explanation=summary,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS=[_g("pronouns","Personal pronouns","Personal pronouns in basic A1 use.",["Mina olen õpilane.","Tema on õpetaja."]),
_g("copula","Olema","Olema in basic A1 use.",["Ma olen eestlane.","See on maja."]),
_g("questions","Questions","Questions in basic A1 use.",["Mis see on?","Kus sa oled?"]),
_g("present","Present tense","Present tense in basic A1 use.",["Ma õpin eesti keelt.","Ta töötab siin."]),
_g("negation","Negation","Negation in basic A1 use.",["Ma ei tööta täna.","See ei ole raamat."]),
_g("partitive","Basic partitive","Basic partitive in basic A1 use.",["Ma joon vett.","Ma söön leiba."]),
_g("plural","Plural nouns","Plural nouns in basic A1 use.",["Need on raamatud.","Minu sõbrad tulevad."]),
_g("location","Location cases","Location cases in basic A1 use.",["Ma olen kodus.","Raamat on laual."])]

def _v(i,t,words):
    return VocabularySet(id=i,level="A1",topic=t,unit_ref="et-a1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])

VOCABULARY_SETS=[_v("greetings_a1","hello",[["tere","noun","hello","tere."]]),
_v("family_a1","mother",[["ema","noun","mother","ema."]]),
_v("home_a1","home",[["kodu","noun","home","kodu."]]),
_v("daily_a1","morning",[["hommik","noun","morning","hommik."]]),
_v("food_a1","water",[["vesi","noun","water","vesi."]]),
_v("places_a1","station",[["jaam","noun","station","jaam."]]),
_v("communication_a1","help",[["abi","noun","help","abi."]]),
_v("review_a1","friend",[["sõber","noun","friend","sõber."]])]

def _p(i,s,items):
    return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in items])

PHRASEBOOK_CATEGORIES=[_p("greetings_a1","Greetings",[["Hello!","greeting","neutral"]]),
_p("shopping_a1","Shopping",[["How much is this?","asking price","neutral"]]),
_p("directions_a1","Directions",[["Where is the station?","asking location","neutral"]]),
_p("help_a1","Help",[["Please help me.","asking for help","neutral"]])]

CURRICULUM={"A1":[CurriculumUnit(id="et-a1-unit-1",level="A1",unit_number=1,title="Tervitused ja tutvumine",grammar_points=["pronouns"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Tervitused ja tutvumine","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="et-a1-unit-2",level="A1",unit_number=2,title="Perekond",grammar_points=["copula"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Perekond","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="et-a1-unit-3",level="A1",unit_number=3,title="Kodu",grammar_points=["questions"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Kodu","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="et-a1-unit-4",level="A1",unit_number=4,title="Igapäevaelu",grammar_points=["present"],vocabulary_set_ids=["daily_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Igapäevaelu","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="et-a1-unit-5",level="A1",unit_number=5,title="Toit ja ostlemine",grammar_points=["negation"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Toit ja ostlemine","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="et-a1-unit-6",level="A1",unit_number=6,title="Kohad ja suunad",grammar_points=["partitive"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Kohad ja suunad","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="et-a1-unit-7",level="A1",unit_number=7,title="Suhtlus",grammar_points=["plural"],vocabulary_set_ids=["communication_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Suhtlus","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="et-a1-unit-8",level="A1",unit_number=8,title="Kordamine",grammar_points=["location"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Kordamine","Use core A1 language"],default_weeks=2)]}
for level in ["A2","B1","B2","C1","C2"]:
    CURRICULUM[level]=[CurriculumUnit(id=f"et-{level.lower()}-foundation",level=level,unit_number=1,title=f"Estonian {level}",grammar_points=["review A1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=[f"Build {level} communication"],default_weeks=2)]

ASSESSMENT_BANK=[
    AssessmentQuestion(id="et-a1-001",skill="vocabulary",difficulty="A1",question="Which word is the greeting?",options=["tere","station","water","book"],correct="tere"),
    AssessmentQuestion(id="et-a1-002",skill="grammar",difficulty="A1",question="Choose the first model sentence.",options=["Mina olen õpilane.","Tema on õpetaja.","No sentence","Tomorrow"],correct="Mina olen õpilane."),
    AssessmentQuestion(id="et-a1-003",skill="grammar",difficulty="A1",question="Which sentence shows the target grammar?",options=["Ma olen eestlane.","See on maja.","Hello","Goodbye"],correct="Ma olen eestlane."),
    AssessmentQuestion(id="et-a1-004",skill="vocabulary",difficulty="A1",question="Which word means mother?",options=["ema","station","friend","water"],correct="ema"),
    AssessmentQuestion(id="et-a1-005",skill="vocabulary",difficulty="A1",question="Which word belongs to the home theme?",options=["kodu","tomorrow","thanks","station"],correct="kodu"),
    AssessmentQuestion(id="et-a1-006",skill="reading",difficulty="A1",question="Read the first model sentence and identify its function.",options=["Basic A1 communication","Advanced literature","Past narrative","Formal report"],correct="Basic A1 communication"),
    AssessmentQuestion(id="et-a1-007",skill="grammar",difficulty="A1",question="Which example belongs to the questions topic?",options=["Ma õpin eesti keelt.","Ma ei tööta täna.","Hello","Thank you"],correct="Ma õpin eesti keelt."),
    AssessmentQuestion(id="et-a1-008",skill="communication",difficulty="A1",question="Which phrase asks for help?",options=["Please help me.","Goodbye.","Thank you.","My name is..."],correct="Please help me."),
    AssessmentQuestion(id="et-a1-009",skill="communication",difficulty="A1",question="Which phrase asks for a location?",options=["Where is the station?","Thank you.","Goodbye.","I am a student."],correct="Where is the station?"),
    AssessmentQuestion(id="et-a1-010",skill="vocabulary",difficulty="A1",question="Which word is the review/friend item?",options=["sõber","water","station","morning"],correct="sõber")
]
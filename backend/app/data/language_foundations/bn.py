"""Bengali A1 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def _g(slug,title,summary,examples):
    return GrammarTopic(slug=slug,title=title,level="A1",category="core",summary=summary,explanation=summary,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS=[_g("pronouns","Personal pronouns","Personal pronouns in basic A1 use.",["আমি ছাত্র।","সে শিক্ষক।"]),
_g("copula","Basic identity","Basic identity in basic A1 use.",["আমি শিক্ষক।","এটা বই।"]),
_g("demonstratives","Demonstratives","Demonstratives in basic A1 use.",["এই বই।","ওই বাড়ি।"]),
_g("questions","Questions","Questions in basic A1 use.",["এটা কী؟","আপনি কোথায়?"]),
_g("present","Present verbs","Present verbs in basic A1 use.",["আমি বাংলা পড়ি।","সে কাজ করে।"]),
_g("negation","Negation","Negation in basic A1 use.",["আমি যাই না।","এটা বই নয়।"]),
_g("plural","Plural nouns","Plural nouns in basic A1 use.",["ছাত্ররা আসে।","বইগুলো টেবিলে।"]),
_g("postpositions","Postpositions","Postpositions in basic A1 use.",["বাড়িতে আছি।","বন্ধুর সঙ্গে যাই।"])]

def _v(i,t,words):
    return VocabularySet(id=i,level="A1",topic=t,unit_ref="bn-a1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])

VOCABULARY_SETS=[_v("greetings_a1","hello",[["নমস্কার","noun","hello","নমস্কার."]]),
_v("family_a1","mother",[["মা","noun","mother","মা."]]),
_v("home_a1","home",[["বাড়ি","noun","home","বাড়ি."]]),
_v("daily_a1","morning",[["সকাল","noun","morning","সকাল."]]),
_v("food_a1","water",[["জল","noun","water","জল."]]),
_v("places_a1","station",[["স্টেশন","noun","station","স্টেশন."]]),
_v("communication_a1","help",[["সাহায্য","noun","help","সাহায্য."]]),
_v("review_a1","friend",[["বন্ধু","noun","friend","বন্ধু."]])]

def _p(i,s,items):
    return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in items])

PHRASEBOOK_CATEGORIES=[_p("greetings_a1","Greetings",[["Hello!","greeting","neutral"]]),
_p("shopping_a1","Shopping",[["How much is this?","asking price","neutral"]]),
_p("directions_a1","Directions",[["Where is the station?","asking location","neutral"]]),
_p("help_a1","Help",[["Please help me.","asking for help","neutral"]])]

CURRICULUM={"A1":[CurriculumUnit(id="bn-a1-unit-1",level="A1",unit_number=1,title="পরিচয়",grammar_points=["pronouns"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle পরিচয়","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="bn-a1-unit-2",level="A1",unit_number=2,title="পরিবার",grammar_points=["copula"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle পরিবার","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="bn-a1-unit-3",level="A1",unit_number=3,title="বাড়ি",grammar_points=["demonstratives"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle বাড়ি","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="bn-a1-unit-4",level="A1",unit_number=4,title="দৈনন্দিন জীবন",grammar_points=["questions"],vocabulary_set_ids=["daily_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle দৈনন্দিন জীবন","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="bn-a1-unit-5",level="A1",unit_number=5,title="খাবার ও কেনাকাটা",grammar_points=["present"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle খাবার ও কেনাকাটা","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="bn-a1-unit-6",level="A1",unit_number=6,title="স্থান ও দিক",grammar_points=["negation"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle স্থান ও দিক","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="bn-a1-unit-7",level="A1",unit_number=7,title="যোগাযোগ",grammar_points=["plural"],vocabulary_set_ids=["communication_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle যোগাযোগ","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="bn-a1-unit-8",level="A1",unit_number=8,title="পুনরাবৃত্তি",grammar_points=["postpositions"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle পুনরাবৃত্তি","Use core A1 language"],default_weeks=2)]}
for level in ["A2","B1","B2","C1","C2"]:
    CURRICULUM[level]=[CurriculumUnit(id=f"bn-{level.lower()}-foundation",level=level,unit_number=1,title=f"Bengali {level}",grammar_points=["review A1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=[f"Build {level} communication"],default_weeks=2)]

ASSESSMENT_BANK=[
    AssessmentQuestion(id="bn-a1-001",skill="vocabulary",difficulty="A1",question="Which word is the greeting?",options=["নমস্কার","station","water","book"],correct="নমস্কার"),
    AssessmentQuestion(id="bn-a1-002",skill="grammar",difficulty="A1",question="Choose the first model sentence.",options=["আমি ছাত্র।","সে শিক্ষক।","No sentence","Tomorrow"],correct="আমি ছাত্র।"),
    AssessmentQuestion(id="bn-a1-003",skill="grammar",difficulty="A1",question="Which sentence shows the target grammar?",options=["আমি শিক্ষক।","এটা বই।","Hello","Goodbye"],correct="আমি শিক্ষক।"),
    AssessmentQuestion(id="bn-a1-004",skill="vocabulary",difficulty="A1",question="Which word means mother?",options=["মা","station","friend","water"],correct="মা"),
    AssessmentQuestion(id="bn-a1-005",skill="vocabulary",difficulty="A1",question="Which word belongs to the home theme?",options=["বাড়ি","tomorrow","thanks","station"],correct="বাড়ি"),
    AssessmentQuestion(id="bn-a1-006",skill="reading",difficulty="A1",question="Read the first model sentence and identify its function.",options=["Basic A1 communication","Advanced literature","Past narrative","Formal report"],correct="Basic A1 communication"),
    AssessmentQuestion(id="bn-a1-007",skill="grammar",difficulty="A1",question="Which example belongs to the questions topic?",options=["এটা কী؟","আমি বাংলা পড়ি।","Hello","Thank you"],correct="এটা কী؟"),
    AssessmentQuestion(id="bn-a1-008",skill="communication",difficulty="A1",question="Which phrase asks for help?",options=["Please help me.","Goodbye.","Thank you.","My name is..."],correct="Please help me."),
    AssessmentQuestion(id="bn-a1-009",skill="communication",difficulty="A1",question="Which phrase asks for a location?",options=["Where is the station?","Thank you.","Goodbye.","I am a student."],correct="Where is the station?"),
    AssessmentQuestion(id="bn-a1-010",skill="vocabulary",difficulty="A1",question="Which word is the review/friend item?",options=["বন্ধু","water","station","morning"],correct="বন্ধু")
]
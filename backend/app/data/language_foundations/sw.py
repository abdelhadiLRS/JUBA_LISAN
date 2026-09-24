"""Swahili A1 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def _g(slug,title,summary,examples):
    return GrammarTopic(slug=slug,title=title,level="A1",category="core",summary=summary,explanation=summary,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS=[_g("pronouns","Personal pronouns","Personal pronouns in basic A1 use.",["Mimi ni mwanafunzi.","Yeye ni mwalimu."]),
_g("copula","Basic identity","Basic identity in basic A1 use.",["Hii ni nyumba.","Mimi ni Juma."]),
_g("demonstratives","Demonstratives","Demonstratives in basic A1 use.",["Kitabu hiki.","Nyumba hiyo."]),
_g("questions","Questions","Questions in basic A1 use.",["Hii ni nini?","Uko wapi?"]),
_g("present","Present tense","Present tense in basic A1 use.",["Ninasoma Kiswahili.","Anafanya kazi."]),
_g("negation","Negation","Negation in basic A1 use.",["Sikimbii.","Hii si nyumba."]),
_g("noun-classes","Noun classes","Noun classes in basic A1 use.",["mtoto / watoto","kitabu / vitabu"]),
_g("prepositions","Prepositions","Prepositions in basic A1 use.",["Niko nyumbani.","Ninaenda na rafiki."])]

def _v(i,t,words):
    return VocabularySet(id=i,level="A1",topic=t,unit_ref="sw-a1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])

VOCABULARY_SETS=[_v("greetings_a1","Salamu",[["habari","phrase","hello","Habari!"],["asante","phrase","thank you","Asante sana."],["kwaheri","phrase","goodbye","Kwaheri!"],["tafadhali","phrase","please","Tafadhali."]]),
_v("family_a1","Familia",[["mama","noun","mother","Mama yangu yuko nyumbani."],["baba","noun","father","Baba yangu anafanya kazi."],["dada","noun","sister","Nina dada."],["kaka","noun","brother","Nina kaka."]]),
_v("home_a1","Nyumbani",[["nyumba","noun","house","Nyumba yangu ni kubwa."],["chumba","noun","room","Chumba changu ni kidogo."],["meza","noun","table","Kitabu kiko mezani."],["mlango","noun","door","Mlango umefungwa."]]),
_v("daily_a1","Maisha ya kila siku",[["asubuhi","noun","morning","Asubuhi ninafanya kazi."],["kula","verb","eat","Ninakula asubuhi."],["kunywa","verb","drink","Ninakunywa maji."],["kulala","verb","sleep","Ninalala usiku."]]),
_v("food_a1","Chakula na manunuzi",[["maji","noun","water","Ninakunywa maji."],["mkate","noun","bread","Ninanunua mkate."],["maziwa","noun","milk","Nataka maziwa."],["bei","noun","price","Bei ni gani?"]]),
_v("places_a1","Maeneo na maelekezo",[["duka","noun","shop","Duka liko hapa."],["kituo","noun","station","Kituo kiko wapi?"],["kulia","adverb","right","Geuka kulia."],["kushoto","adverb","left","Geuka kushoto."]]),
_v("communication_a1","Mawasiliano",[["msaada","noun","help","Nahitaji msaada."],["kusaidia","verb","help","Unaweza kunisaidia?"],["kuelewa","verb","understand","Naelewa."],["polepole","adverb","slowly","Sema polepole."]]),
_v("review_a1","Marudio A1",[["rafiki","noun","friend","Huyu ni rafiki yangu."],["leo","adverb","today","Leo ninafanya kazi."],["kesho","adverb","tomorrow","Kesho nitasoma."],["saa","noun","time","Ni saa ngapi?"]])]

def _p(i,s,items):
    return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in items])

PHRASEBOOK_CATEGORIES=[_p("greetings_a1","Greetings",[["Hello!","greeting","neutral"]]),
_p("shopping_a1","Shopping",[["How much is this?","asking price","neutral"]]),
_p("directions_a1","Directions",[["Where is the station?","asking location","neutral"]]),
_p("help_a1","Help",[["Please help me.","asking for help","neutral"]])]

CURRICULUM={"A1":[CurriculumUnit(id="sw-a1-unit-1",level="A1",unit_number=1,title="Salamu na utambulisho",grammar_points=["pronouns"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Salamu na utambulisho","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="sw-a1-unit-2",level="A1",unit_number=2,title="Familia",grammar_points=["copula"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Familia","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="sw-a1-unit-3",level="A1",unit_number=3,title="Nyumba",grammar_points=["demonstratives"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Nyumba","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="sw-a1-unit-4",level="A1",unit_number=4,title="Maisha ya kila siku",grammar_points=["questions"],vocabulary_set_ids=["daily_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Maisha ya kila siku","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="sw-a1-unit-5",level="A1",unit_number=5,title="Chakula na ununuzi",grammar_points=["present"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Chakula na ununuzi","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="sw-a1-unit-6",level="A1",unit_number=6,title="Maeneo na maelekezo",grammar_points=["negation"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Maeneo na maelekezo","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="sw-a1-unit-7",level="A1",unit_number=7,title="Mawasiliano",grammar_points=["noun-classes"],vocabulary_set_ids=["communication_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Mawasiliano","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="sw-a1-unit-8",level="A1",unit_number=8,title="Marudio",grammar_points=["prepositions"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Marudio","Use core A1 language"],default_weeks=2)]}
for level in ["A2","B1","B2","C1","C2"]:
    CURRICULUM[level]=[CurriculumUnit(id=f"sw-{level.lower()}-foundation",level=level,unit_number=1,title=f"Swahili {level}",grammar_points=["review A1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=[f"Build {level} communication"],default_weeks=2)]

ASSESSMENT_BANK=[
    AssessmentQuestion(id="sw-a1-001",skill="vocabulary",difficulty="A1",question="Which word is the greeting?",options=["habari","station","water","book"],correct="habari"),
    AssessmentQuestion(id="sw-a1-002",skill="grammar",difficulty="A1",question="Choose the first model sentence.",options=["Mimi ni mwanafunzi.","Yeye ni mwalimu.","No sentence","Tomorrow"],correct="Mimi ni mwanafunzi."),
    AssessmentQuestion(id="sw-a1-003",skill="grammar",difficulty="A1",question="Which sentence shows the target grammar?",options=["Hii ni nyumba.","Mimi ni Juma.","Hello","Goodbye"],correct="Hii ni nyumba."),
    AssessmentQuestion(id="sw-a1-004",skill="vocabulary",difficulty="A1",question="Which word means mother?",options=["mama","station","friend","water"],correct="mama"),
    AssessmentQuestion(id="sw-a1-005",skill="vocabulary",difficulty="A1",question="Which word belongs to the home theme?",options=["nyumba","tomorrow","thanks","station"],correct="nyumba"),
    AssessmentQuestion(id="sw-a1-006",skill="reading",difficulty="A1",question="Read the first model sentence and identify its function.",options=["Basic A1 communication","Advanced literature","Past narrative","Formal report"],correct="Basic A1 communication"),
    AssessmentQuestion(id="sw-a1-007",skill="grammar",difficulty="A1",question="Which example belongs to the questions topic?",options=["Hii ni nini?","Ninasoma Kiswahili.","Hello","Thank you"],correct="Hii ni nini?"),
    AssessmentQuestion(id="sw-a1-008",skill="communication",difficulty="A1",question="Which phrase asks for help?",options=["Please help me.","Goodbye.","Thank you.","My name is..."],correct="Please help me."),
    AssessmentQuestion(id="sw-a1-009",skill="communication",difficulty="A1",question="Which phrase asks for a location?",options=["Where is the station?","Thank you.","Goodbye.","I am a student."],correct="Where is the station?"),
    AssessmentQuestion(id="sw-a1-010",skill="vocabulary",difficulty="A1",question="Which word is the review/friend item?",options=["rafiki","water","station","morning"],correct="rafiki")
]
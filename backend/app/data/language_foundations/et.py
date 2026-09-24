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

VOCABULARY_SETS=[_v("greetings_a1","Tervitused",[["tere","phrase","hello","Tere!"],["aitäh","phrase","thank you","Aitäh!"],["palun","phrase","please","Palun istu."],["hüvasti","phrase","goodbye","Hüvasti!"]]),
_v("family_a1","Perekond",[["ema","noun","mother","Minu ema on kodus."],["isa","noun","father","Minu isa töötab."],["õde","noun","sister","Mul on õde."],["vend","noun","brother","Mul on vend."]]),
_v("home_a1","Kodu",[["kodu","noun","home","Ma olen kodus."],["tuba","noun","room","Minu tuba on väike."],["laud","noun","table","Raamat on laual."],["uks","noun","door","Uks on lahti."]]),
_v("daily_a1","Igapäev",[["hommik","noun","morning","Hommikul ma töötan."],["sööma","verb","eat","Ma söön."],["jooma","verb","drink","Ma joon vett."],["magama","verb","sleep","Ma lähen magama."]]),
_v("food_a1","Toit ja ostud",[["vesi","noun","water","Ma joon vett."],["leib","noun","bread","Ma ostan leiba."],["piim","noun","milk","Palun piima."],["hind","noun","price","Mis on hind?"]]),
_v("places_a1","Kohad ja suunad",[["pood","noun","shop","Pood on lähedal."],["jaam","noun","station","Kus on jaam?"],["parem","adverb","right","Pööra paremale."],["vasak","adverb","left","Pööra vasakule."]]),
_v("communication_a1","Suhtlus",[["abi","noun","help","Vajan abi."],["aitama","verb","help","Kas sa saad mind aidata?"],["aru saama","verb","understand","Ma saan aru."],["aeglaselt","adverb","slowly","Palun räägi aeglaselt."]]),
_v("review_a1","A1 kordamine",[["sõber","noun","friend","Ta on minu sõber."],["täna","adverb","today","Täna ma töötan."],["homme","adverb","tomorrow","Homme ma õpin."],["aeg","noun","time","Mul on aega."]])]

def _p(i,s,items):
    return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in items])

PHRASEBOOK_CATEGORIES=[_p("greetings_a1","Tervitused",[["Tere!","greeting","neutral"],["Minu nimi on Mari.","introducing yourself","neutral"],["Meeldiv tutvuda.","meeting someone","neutral"]]),
_p("shopping_a1","Ostlemine",[["Kui palju see maksab?","asking price","neutral"],["Ma soovin seda.","requesting an item","neutral"],["Kas saan kaardiga maksta?","payment","neutral"]]),
_p("directions_a1","Suunad",[["Kus jaam on?","asking location","neutral"],["Mine otse.","giving directions","neutral"],["Pööra paremale.","giving directions","neutral"]]),
_p("help_a1","Abi",[["Kas sa saad mind aidata?","asking for help","neutral"],["Ma ei saa aru.","clarification","neutral"],["Palun räägi aeglasemalt.","asking someone to slow down","neutral"]]),_p("appointments_a1","Aeg ja kohtumised",[["Mis kell?","asking time","neutral"],["Kohtume kell viis.","making an appointment","neutral"],["Homme sobib.","accepting a time","neutral"]])]

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

ASSESSMENT_BANK=[AssessmentQuestion(id="et-a1-001",skill="vocabulary",difficulty="A1",question="What does “aitäh” mean?",options=["hello","thank you","goodbye","help"],correct="thank you"),
AssessmentQuestion(id="et-a1-002",skill="grammar",difficulty="A1",question="Choose the correct sentence for “I am a student.”",options=["Mina olen õpilane.","Mina õpilane olen.","Mina on õpilane.","Õpilane mina olen."],correct="Mina olen õpilane."),
AssessmentQuestion(id="et-a1-003",skill="grammar",difficulty="A1",question="Which sentence is negative?",options=["Ma ei tööta täna.","Ma tööta täna.","Ma ei töötan täna.","Ma töötan ei täna."],correct="Ma ei tööta täna."),
AssessmentQuestion(id="et-a1-004",skill="grammar",difficulty="A1",question="Which question asks where someone is?",options=["Kus sa oled?","Mis see on?","Kui palju see maksab?","Mis su nimi on?"],correct="Kus sa oled?"),
AssessmentQuestion(id="et-a1-005",skill="vocabulary",difficulty="A1",question="Which word means “mother”?",options=["ema","isa","õde","vend"],correct="ema"),
AssessmentQuestion(id="et-a1-006",skill="vocabulary",difficulty="A1",question="Which word means “shop”?",options=["pood","jaam","kodu","tuba"],correct="pood"),
AssessmentQuestion(id="et-a1-007",skill="grammar",difficulty="A1",question="Choose the correct sentence for “I drink water.”",options=["Ma joon vett.","Ma joo vett.","Ma joon vesi.","Mina jooma vett."],correct="Ma joon vett."),
AssessmentQuestion(id="et-a1-008",skill="communication",difficulty="A1",question="Which phrase asks for help?",options=["Kas sa saad mind aidata?","Hüvasti!","Aitäh!","Minu nimi on Mari."],correct="Kas sa saad mind aidata?"),
AssessmentQuestion(id="et-a1-009",skill="communication",difficulty="A1",question="Which phrase asks for the station's location?",options=["Kus jaam on?","Kui palju see maksab?","Ma soovin seda.","Tere!"],correct="Kus jaam on?"),
AssessmentQuestion(id="et-a1-010",skill="vocabulary",difficulty="A1",question="Which word means “friend”?",options=["sõber","aeg","homme","tänа"],correct="sõber")]
ASSESSMENT_BANK=[
    AssessmentQuestion(id="et-a1-001",skill="vocabulary",difficulty="A1",question="Which word is the greeting?",options=["tere","station","water","book"],correct="tere"),
    AssessmentQuestion(id="et-a1-002",skill="grammar",difficulty="A1",question="Choose the first model sentence.",options=["Mina olen õpilane.","Tema on õpetaja.","No sentence","Tomorrow"],correct="Mina olen õpilane."),
    AssessmentQuestion(id="et-a1-003",skill="grammar",difficulty="A1",question="Which sentence shows the target grammar?",options=["Ma olen eestlane.","See on maja.","Hello","Goodbye"],correct="Ma olen eestlane."),
    AssessmentQuestion(id="et-a1-004",skill="vocabulary",difficulty="A1",question="Which word means mother?",options=["ema","station","friend","water"],correct="ema"),
    AssessmentQuestion(id="et-a1-005",skill="vocabulary",difficulty="A1",question="Which word belongs to the home theme?",options=["kodu","tomorrow","thanks","station"],correct="kodu"),
    AssessmentQuestion(id="et-a1-006",skill="reading",difficulty="A1",question="Read the first model sentence and identify its function.",options=["Basic A1 communication","Advanced literature","Past narrative","Formal report"],correct="Basic A1 communication"),
    AssessmentQuestion(id="et-a1-007",skill="grammar",difficulty="A1",question="Which example is a basic question?",options=["Kus sa oled?","Ma õpin eesti keelt.","Ma ei tööta täna.","See on raamat."],correct="Kus sa oled?"),
    AssessmentQuestion(id="et-a1-008",skill="communication",difficulty="A1",question="Which phrase asks for help?",options=["Please help me.","Goodbye.","Thank you.","My name is..."],correct="Please help me."),
    AssessmentQuestion(id="et-a1-009",skill="communication",difficulty="A1",question="Which phrase asks for a location?",options=["Where is the station?","Thank you.","Goodbye.","I am a student."],correct="Where is the station?"),
    AssessmentQuestion(id="et-a1-010",skill="vocabulary",difficulty="A1",question="Which word is the review/friend item?",options=["sõber","water","station","morning"],correct="sõber")
]
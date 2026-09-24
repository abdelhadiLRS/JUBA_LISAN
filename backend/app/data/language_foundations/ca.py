"""Catalan A1 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def _g(slug,title,summary,examples):
    return GrammarTopic(slug=slug,title=title,level="A1",category="core",summary=summary,explanation=summary,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS=[_g("pronouns","Personal pronouns","Personal pronouns in basic A1 use.",["Jo sóc estudiant.","Ella és professora."]),
_g("ser","Ser","Ser in basic A1 use.",["Sóc de Barcelona.","Ell és metge."]),
_g("estar","Estar","Estar in basic A1 use.",["Estic a casa.","Ella està cansada."]),
_g("questions","Questions","Questions in basic A1 use.",["Què és això?","On ets?"]),
_g("present","Present tense","Present tense in basic A1 use.",["Estudio català.","Ella treballa aquí."]),
_g("negation","Negation","Negation in basic A1 use.",["No estudio avui.","Això no és un llibre."]),
_g("gender-number","Gender and number","Gender and number in basic A1 use.",["un llibre / una casa","els amics / les amigues"]),
_g("prepositions","Prepositions","Prepositions in basic A1 use.",["Sóc de Girona.","Vaig amb el meu amic."])]

def _v(i,t,words):
    return VocabularySet(id=i,level="A1",topic=t,unit_ref="ca-a1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])

VOCABULARY_SETS=[_v("greetings_a1","Salutacions",[["hola","phrase","hello","Hola!"],["adéu","phrase","goodbye","Adéu!"],["gràcies","phrase","thanks","Gràcies!"],["si us plau","phrase","please","Si us plau."]]),
_v("family_a1","Família",[["mare","noun","mother","La meva mare és a casa."],["pare","noun","father","El meu pare treballa."],["germana","noun","sister","Tinc una germana."],["germà","noun","brother","Tinc un germà."]]),
_v("home_a1","Casa",[["casa","noun","house","La casa és petita."],["habitació","noun","room","La meva habitació és gran."],["taula","noun","table","El llibre és a la taula."],["porta","noun","door","La porta és oberta."]]),
_v("daily_a1","Vida quotidiana",[["matí","noun","morning","Al matí treballo."],["menjar","verb","eat","Menjo al matí."],["beure","verb","drink","Bec aigua."],["dormir","verb","sleep","Vaig a dormir."]]),
_v("food_a1","Menjar i compres",[["aigua","noun","water","Bec aigua."],["pa","noun","bread","Compro pa."],["llet","noun","milk","Vull llet."],["preu","noun","price","Quin és el preu?"]]),
_v("places_a1","Llocs i direccions",[["botiga","noun","shop","La botiga és aquí."],["estació","noun","station","On és l’estació?"],["dreta","noun","right","Gira a la dreta."],["esquerra","noun","left","Gira a l’esquerra."]]),
_v("communication_a1","Comunicació",[["ajudar","verb","help","Em pots ajudar?"],["entendre","verb","understand","Ho entenc."],["preguntar","verb","ask","Vull preguntar."],["lentament","adverb","slowly","Parla lentament."]]),
_v("review_a1","Repàs A1",[["amic","noun","friend","És el meu amic."],["avui","adverb","today","Avui treballo."],["demà","adverb","tomorrow","Demà estudio."],["hora","noun","time","Quina hora és?"]])]

def _p(i,s,items):
    return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in items])

PHRASEBOOK_CATEGORIES=[_p("greetings_a1","Greetings",[["Hello!","greeting","neutral"]]),
_p("shopping_a1","Shopping",[["How much is this?","asking price","neutral"]]),
_p("directions_a1","Directions",[["Where is the station?","asking location","neutral"]]),
_p("help_a1","Help",[["Please help me.","asking for help","neutral"]])]

CURRICULUM={"A1":[CurriculumUnit(id="ca-a1-unit-1",level="A1",unit_number=1,title="Salutacions i identitat",grammar_points=["pronouns"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Salutacions i identitat","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="ca-a1-unit-2",level="A1",unit_number=2,title="Família",grammar_points=["ser"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Família","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="ca-a1-unit-3",level="A1",unit_number=3,title="Casa",grammar_points=["estar"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Casa","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="ca-a1-unit-4",level="A1",unit_number=4,title="Vida quotidiana",grammar_points=["questions"],vocabulary_set_ids=["daily_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Vida quotidiana","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="ca-a1-unit-5",level="A1",unit_number=5,title="Menjar i compres",grammar_points=["present"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Menjar i compres","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="ca-a1-unit-6",level="A1",unit_number=6,title="Llocs i direccions",grammar_points=["negation"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Llocs i direccions","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="ca-a1-unit-7",level="A1",unit_number=7,title="Comunicació",grammar_points=["gender-number"],vocabulary_set_ids=["communication_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Comunicació","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="ca-a1-unit-8",level="A1",unit_number=8,title="Repàs",grammar_points=["prepositions"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Repàs","Use core A1 language"],default_weeks=2)]}
for level in ["A2","B1","B2","C1","C2"]:
    CURRICULUM[level]=[CurriculumUnit(id=f"ca-{level.lower()}-foundation",level=level,unit_number=1,title=f"Catalan {level}",grammar_points=["review A1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=[f"Build {level} communication"],default_weeks=2)]

ASSESSMENT_BANK=[AssessmentQuestion(id="ca-a1-001",skill="vocabulary",difficulty="A1",question="What does “gràcies” mean?",options=["hello","thanks","goodbye","please"],correct="thanks"),
AssessmentQuestion(id="ca-a1-002",skill="grammar",difficulty="A1",question="Choose the correct sentence for “I am a student.”",options=["Jo sóc estudiant.","Jo és estudiant.","Jo sóc estudiants.","Jo estudiant sóc."],correct="Jo sóc estudiant."),
AssessmentQuestion(id="ca-a1-003",skill="grammar",difficulty="A1",question="Which sentence uses estar correctly?",options=["Estic a casa.","Sóc a casa.","Estic casa sóc.","A casa és jo."],correct="Estic a casa."),
AssessmentQuestion(id="ca-a1-004",skill="grammar",difficulty="A1",question="Which question asks “Where are you?”",options=["On ets?","Què és això?","Quin és el preu?","Com et dius?"],correct="On ets?"),
AssessmentQuestion(id="ca-a1-005",skill="vocabulary",difficulty="A1",question="Which word means “mother”?",options=["mare","pare","germana","germà"],correct="mare"),
AssessmentQuestion(id="ca-a1-006",skill="vocabulary",difficulty="A1",question="Which word means “station”?",options=["botiga","estació","casa","porta"],correct="estació"),
AssessmentQuestion(id="ca-a1-007",skill="grammar",difficulty="A1",question="Choose the correct negative sentence.",options=["No estudio avui.","No estudiar avui.","Estudio no avui.","No estudis avui."],correct="No estudio avui."),
AssessmentQuestion(id="ca-a1-008",skill="communication",difficulty="A1",question="Which phrase asks for help?",options=["Em pots ajudar?","Adéu!","Gràcies!","Sóc estudiant."],correct="Em pots ajudar?"),
AssessmentQuestion(id="ca-a1-009",skill="communication",difficulty="A1",question="Which phrase asks for a location?",options=["On és l’estació?","Vull llet.","Gràcies!","Adéu!"],correct="On és l’estació?"),
AssessmentQuestion(id="ca-a1-010",skill="vocabulary",difficulty="A1",question="Which word means “friend”?",options=["amic","aigua","hora","botiga"],correct="amic")]
ASSESSMENT_BANK=[
    AssessmentQuestion(id="ca-a1-001",skill="vocabulary",difficulty="A1",question="Which word is the greeting?",options=["hola","station","water","book"],correct="hola"),
    AssessmentQuestion(id="ca-a1-002",skill="grammar",difficulty="A1",question="Choose the first model sentence.",options=["Jo sóc estudiant.","Ella és professora.","No sentence","Tomorrow"],correct="Jo sóc estudiant."),
    AssessmentQuestion(id="ca-a1-003",skill="grammar",difficulty="A1",question="Which sentence shows the target grammar?",options=["Sóc de Barcelona.","Ell és metge.","Hello","Goodbye"],correct="Sóc de Barcelona."),
    AssessmentQuestion(id="ca-a1-004",skill="vocabulary",difficulty="A1",question="Which word means mother?",options=["mare","station","friend","water"],correct="mare"),
    AssessmentQuestion(id="ca-a1-005",skill="vocabulary",difficulty="A1",question="Which word belongs to the home theme?",options=["casa","tomorrow","thanks","station"],correct="casa"),
    AssessmentQuestion(id="ca-a1-006",skill="reading",difficulty="A1",question="Read the first model sentence and identify its function.",options=["Basic A1 communication","Advanced literature","Past narrative","Formal report"],correct="Basic A1 communication"),
    AssessmentQuestion(id="ca-a1-007",skill="grammar",difficulty="A1",question="Which example belongs to the questions topic?",options=["Què és això?","Estudio català.","Hello","Thank you"],correct="Què és això?"),
    AssessmentQuestion(id="ca-a1-008",skill="communication",difficulty="A1",question="Which phrase asks for help?",options=["Please help me.","Goodbye.","Thank you.","My name is..."],correct="Please help me."),
    AssessmentQuestion(id="ca-a1-009",skill="communication",difficulty="A1",question="Which phrase asks for a location?",options=["Where is the station?","Thank you.","Goodbye.","I am a student."],correct="Where is the station?"),
    AssessmentQuestion(id="ca-a1-010",skill="vocabulary",difficulty="A1",question="Which word is the review/friend item?",options=["amic","water","station","morning"],correct="amic")
]
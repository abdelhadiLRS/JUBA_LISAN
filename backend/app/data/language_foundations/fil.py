"""Filipino A1 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def _g(slug,title,summary,examples):
    return GrammarTopic(slug=slug,title=title,level="A1",category="core",summary=summary,explanation=summary,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS=[_g("pronouns","Personal pronouns","Personal pronouns in basic A1 use.",["Ako ay estudyante.","Siya ay guro."]),
_g("ay","Ay sentences","Ay sentences in basic A1 use.",["Ako ay Pilipino.","Ito ay bahay."]),
_g("ang","Basic noun marking","Basic noun marking in basic A1 use.",["Ang libro ay bago.","Ang bahay ay malaki."]),
_g("questions","Questions","Questions in basic A1 use.",["Ano ito?","Nasaan ka?"]),
_g("present","Present actions","Present actions in basic A1 use.",["Nag-aaral ako.","Nagtatrabaho siya."]),
_g("negation","Negation","Negation in basic A1 use.",["Hindi ako pagod.","Wala akong oras."]),
_g("plural","Plural nouns","Plural nouns in basic A1 use.",["Mga libro ito.","Mga kaibigan ko sila."]),
_g("markers","Basic markers","Basic markers in basic A1 use.",["Nasa bahay ako.","Kasama ko ang kaibigan ko."])]

def _v(i,t,words):
    return VocabularySet(id=i,level="A1",topic=t,unit_ref="fil-a1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])

VOCABULARY_SETS=[_v("greetings_a1","Pagbati",[["kumusta","phrase","hello / how are you","Kumusta!"],["salamat","phrase","thank you","Salamat!"],["paalam","phrase","goodbye","Paalam!"],["pakiusap","phrase","please","Pakiusap."]]),
_v("family_a1","Pamilya",[["nanay","noun","mother","Nasa bahay ang nanay ko."],["tatay","noun","father","Nagtatrabaho ang tatay ko."],["ate","noun","older sister","May ate ako."],["kuya","noun","older brother","May kuya ako."]]),
_v("home_a1","Bahay",[["bahay","noun","house","Malaki ang bahay namin."],["kuwarto","noun","room","Maliit ang kuwarto ko."],["mesa","noun","table","Nasa mesa ang libro."],["pinto","noun","door","Bukas ang pinto."]]),
_v("daily_a1","Araw-araw",[["umaga","noun","morning","Sa umaga ako nag-aaral."],["kumain","verb","eat","Kumakain ako."],["uminom","verb","drink","Umiinom ako ng tubig."],["matulog","verb","sleep","Matutulog ako mamaya."]]),
_v("food_a1","Pagkain at pamimili",[["tubig","noun","water","Umiinom ako ng tubig."],["tinapay","noun","bread","Bumibili ako ng tinapay."],["gatas","noun","milk","Gusto ko ng gatas."],["presyo","noun","price","Magkano ang presyo?"]]),
_v("places_a1","Mga lugar at direksyon",[["tindahan","noun","shop","Malapit ang tindahan."],["istasyon","noun","station","Nasaan ang istasyon?"],["kanan","noun","right","Kumanan ka."],["kaliwa","noun","left","Kumaliwa ka."]]),
_v("communication_a1","Komunikasyon",[["tulong","noun","help","Kailangan ko ng tulong."],["tumulong","verb","help","Maaari mo ba akong tulungan?"],["maintindihan","verb","understand","Hindi ko maintindihan."],["dahan-dahan","adverb","slowly","Magsalita ka nang dahan-dahan."]]),
_v("review_a1","Pagbabalik-aral",[["kaibigan","noun","friend","Kaibigan ko siya."],["ngayon","adverb","today","Ngayon ako nagtatrabaho."],["bukas","adverb","tomorrow","Bukas ako mag-aaral."],["oras","noun","time","Anong oras na?"])]

def _p(i,s,items):
    return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in items])

PHRASEBOOK_CATEGORIES=[_p("greetings_a1","Greetings",[["Hello!","greeting","neutral"]]),
_p("shopping_a1","Shopping",[["How much is this?","asking price","neutral"]]),
_p("directions_a1","Directions",[["Where is the station?","asking location","neutral"]]),
_p("help_a1","Help",[["Please help me.","asking for help","neutral"]])]

CURRICULUM={"A1":[CurriculumUnit(id="fil-a1-unit-1",level="A1",unit_number=1,title="Pagbati at pagkakakilanlan",grammar_points=["pronouns"],vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Pagbati at pagkakakilanlan","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="fil-a1-unit-2",level="A1",unit_number=2,title="Pamilya",grammar_points=["ay"],vocabulary_set_ids=["family_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Pamilya","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="fil-a1-unit-3",level="A1",unit_number=3,title="Bahay",grammar_points=["ang"],vocabulary_set_ids=["home_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Bahay","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="fil-a1-unit-4",level="A1",unit_number=4,title="Araw-araw na buhay",grammar_points=["questions"],vocabulary_set_ids=["daily_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Araw-araw na buhay","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="fil-a1-unit-5",level="A1",unit_number=5,title="Pagkain at pamimili",grammar_points=["present"],vocabulary_set_ids=["food_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Pagkain at pamimili","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="fil-a1-unit-6",level="A1",unit_number=6,title="Mga lugar at direksyon",grammar_points=["negation"],vocabulary_set_ids=["places_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Mga lugar at direksyon","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="fil-a1-unit-7",level="A1",unit_number=7,title="Komunikasyon",grammar_points=["plural"],vocabulary_set_ids=["communication_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Komunikasyon","Use core A1 language"],default_weeks=2),
CurriculumUnit(id="fil-a1-unit-8",level="A1",unit_number=8,title="Pagbabalik-aral",grammar_points=["markers"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=["Handle Pagbabalik-aral","Use core A1 language"],default_weeks=2)]}
for level in ["A2","B1","B2","C1","C2"]:
    CURRICULUM[level]=[CurriculumUnit(id=f"fil-{level.lower()}-foundation",level=level,unit_number=1,title=f"Filipino {level}",grammar_points=["review A1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=[f"Build {level} communication"],default_weeks=2)]

ASSESSMENT_BANK=[
    AssessmentQuestion(id="fil-a1-001",skill="vocabulary",difficulty="A1",question="Which word is the greeting?",options=["kumusta","station","water","book"],correct="kumusta"),
    AssessmentQuestion(id="fil-a1-002",skill="grammar",difficulty="A1",question="Choose the first model sentence.",options=["Ako ay estudyante.","Siya ay guro.","No sentence","Tomorrow"],correct="Ako ay estudyante."),
    AssessmentQuestion(id="fil-a1-003",skill="grammar",difficulty="A1",question="Which sentence shows the target grammar?",options=["Ako ay Pilipino.","Ito ay bahay.","Hello","Goodbye"],correct="Ako ay Pilipino."),
    AssessmentQuestion(id="fil-a1-004",skill="vocabulary",difficulty="A1",question="Which word means mother?",options=["nanay","station","friend","water"],correct="nanay"),
    AssessmentQuestion(id="fil-a1-005",skill="vocabulary",difficulty="A1",question="Which word belongs to the home theme?",options=["bahay","tomorrow","thanks","station"],correct="bahay"),
    AssessmentQuestion(id="fil-a1-006",skill="reading",difficulty="A1",question="Read the first model sentence and identify its function.",options=["Basic A1 communication","Advanced literature","Past narrative","Formal report"],correct="Basic A1 communication"),
    AssessmentQuestion(id="fil-a1-007",skill="grammar",difficulty="A1",question="Which example belongs to the questions topic?",options=["Ano ito?","Nag-aaral ako.","Hello","Thank you"],correct="Ano ito?"),
    AssessmentQuestion(id="fil-a1-008",skill="communication",difficulty="A1",question="Which phrase asks for help?",options=["Please help me.","Goodbye.","Thank you.","My name is..."],correct="Please help me."),
    AssessmentQuestion(id="fil-a1-009",skill="communication",difficulty="A1",question="Which phrase asks for a location?",options=["Where is the station?","Thank you.","Goodbye.","I am a student."],correct="Where is the station?"),
    AssessmentQuestion(id="fil-a1-010",skill="vocabulary",difficulty="A1",question="Which word is the review/friend item?",options=["kaibigan","water","station","morning"],correct="kaibigan")
]
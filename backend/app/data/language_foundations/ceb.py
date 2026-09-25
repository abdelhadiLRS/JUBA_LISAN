"""Cebuano A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

def _g(slug, title, level, explanation, examples):
    return GrammarTopic(
        slug=slug, title=title, level=level, category="grammar",
        summary=f"Cebuano {level} grammar for practical communication.",
        explanation=explanation,
        examples=[GrammarExample(text=x) for x in examples],
    )

GRAMMAR_TOPICS = [
    _g("pronouns","Personal pronouns and reference","A1","Use personal pronouns for identity and everyday reference.",["Ako si Maria.","Ikaw ba si Juan?"]),
    _g("nominal_predicates","Nominal predicates and identity","A1","Form identity statements with Cebuano nominal predicates.",["Estudyante ko.","Maestra siya."]),
    _g("present","Present and habitual actions","A1","Describe current and habitual activities.",["Nagtuon ko og Cebuano.","Motrabaho siya kada adlaw."]),
    _g("questions","Question words and yes-no questions","A1","Ask who, what, where, when and how questions.",["Unsa imong ngalan?","Asa ka nagpuyo?"]),
    _g("negation","Negation with dili and wala","A1","Distinguish common negative patterns for present and non-present situations.",["Dili ko kasabot.","Wala koy oras."]),
    _g("demonstratives","Demonstratives and reference","A1","Point to people and things using proximal and distal demonstratives.",["Kini akong libro.","Kana nga balay dako."]),
    _g("possessives","Possession and possessive phrases","A1","Express ownership and relationships.",["Akong igsoon siya.","Ang libro ni Ana."]),
    _g("location","Existence and location","A1","Express where people and things are located.",["Naa ang libro sa lamesa.","Naa ko sa balay."]),
    _g("plurality","Plural nouns and quantity","A1","Talk about groups and quantities using common Cebuano patterns.",["Daghang estudyante dinhi.","Duha ka libro."]),
    _g("case_markers","Ang, ug, og and sa markers","A1","Use core Cebuano noun markers in simple clauses.",["Nikaon ko og isda.","Naa siya sa eskwelahan."]),
    _g("past","Past events with completed aspect","A2","Describe completed actions and past events.",["Nikaon ko ganina.","Niadto siya sa merkado kagahapon."]),
    _g("future","Future and intended actions","A2","Talk about planned or expected actions.",["Moadto ko ugma.","Magtuon siya karong gabhiona."]),
    _g("progressive","Ongoing actions and aspect","A2","Describe actions in progress and distinguish aspectual meanings.",["Nagbasa ko karon.","Nagluto siya sa kusina."]),
    _g("imperatives","Commands and polite requests","A2","Give instructions and make polite requests.",["Palihog lingkod.","Ayaw pagdali."]),
    _g("comparatives","Comparison and degree","A2","Compare people, objects and situations.",["Mas dako kini kaysa niana.","Labing maayo ang ikaduha."]),
    _g("modality","Ability, obligation and desire","A2","Express ability, necessity, permission and desire.",["Makakat-on ko niini.","Kinahanglan ko moadto."]),
    _g("pronoun_clitics","Pronoun placement and focus","A2","Use Cebuano pronoun forms in natural clause patterns.",["Gihatag niya ang libro nako.","Nakakita ko kaniya."]),
    _g("motion","Motion and direction","A2","Describe movement toward, away from and between places.",["Moadto ko sa eskwelahan.","Gikan siya sa lungsod."]),
    _g("conditional","Conditional clauses","B1","Build real and hypothetical conditions.",["Kung moulan, magpabilin ko sa balay.","Kung adunay oras, motabang ko."]),
    _g("relative","Relative clauses","B1","Modify nouns with relative clauses.",["Ang libro nga akong gibasa maayo.","Ang tawo nga akong nakita mao si Ana."]),
    _g("cause_purpose","Cause, reason and purpose","B1","Explain causes, reasons and purposes.",["Miadto ko aron motabang.","Wala siya miadto kay nasakit siya."]),
    _g("reported","Reported speech","B1","Report statements and questions while preserving their meaning.",["Miingon siya nga moadto siya.","Nangutana siya kung asa ko."]),
    _g("reflexive_reciprocal","Reflexive and reciprocal meanings","B1","Express actions directed toward oneself or shared between people.",["Nagtinabangay sila.","Gitan-aw niya ang iyang kaugalingon."]),
    _g("causative","Causative and induced events","B1","Express causing, arranging or enabling an action.",["Gipaayo niya ang sakyanan.","Gitudloan niya ang bata."]),
    _g("passive_voice","Passive and voice/focus patterns","B2","Interpret and produce Cebuano voice and focus constructions.",["Gipalit ni Maria ang libro.","Gihatag ang regalo kang Ana."]),
    _g("aspect","Aspectual contrasts and event structure","B2","Choose aspectual forms to present events as completed, ongoing or habitual.",["Nakahuman na siya.","Makanunay siyang nagbasa."]),
    _g("concession","Concession and contrast","B2","Connect contrasting or concessive propositions.",["Bisan og kapoy siya, nagpadayon siya.","Apan gusto gihapon niya."]),
    _g("discourse_connectors","Discourse connectors and cohesion","B2","Organize explanations with cause, sequence, contrast and conclusion markers.",["Una, magplano kita. Dayon, sugdan nato.","Busa, importante kini."]),
    _g("subordination","Complex subordinate clauses","B2","Combine clauses for time, condition, cause and complement relations.",["Sa dihang miabot siya, nagsugod ang miting.","Human siya mokaon, nanglakaw sila."]),
    _g("nominalization","Nominalization and formal style","C1","Turn processes and propositions into formal noun phrases.",["Ang pagpalambo sa edukasyon importante.","Ang pagdumala sa proyekto komplikado."]),
    _g("hedging","Academic hedging and stance","C1","Express claims with appropriate degrees of certainty.",["Posible nga adunay laing hinungdan.","Murag nagpakita kini og kausaban."]),
    _g("embedded_questions","Embedded questions","C1","Embed questions inside statements and formal requests.",["Wala ko kahibalo kung asa siya.","Pangutan-a siya unsa ang problema."]),
    _g("information_structure","Topic, focus and emphasis","C1","Manage information structure to highlight new or contrastive information.",["Kini ang problema nga atong hisgutan.","Si Ana ang nakakita sa dokumento."]),
    _g("formal_register","Formal, professional and institutional Cebuano","C1","Adjust grammar and vocabulary for workplace and institutional contexts.",["Gipahibalo sa opisina ang bag-ong pamaagi.","Palihog isumite ang dokumento sa takdang panahon."]),
    _g("argumentation","Academic argumentation and counterargument","C1","Build claims, evidence, qualifications and responses to opposing views.",["Base sa datos, makatarunganon ang maong konklusyon.","Bisan pa niini, adunay laing interpretasyon."]),
    _g("pragmatics","Politeness, implication and register","C2","Interpret indirectness, politeness, social meaning and context.",["Kung mahimo, palihog susiha kini pag-usab.","Mas maayo tingali kung atong hisgutan una."]),
    _g("rhetoric","Rhetorical and literary nuance","C2","Use repetition, contrast, imagery and rhetorical framing.",["Dili lamang kini problema; usa kini ka hagit sa tanan."]),
    _g("idioms","Idiomatic Cebuano and figurative meaning","C2","Interpret idioms and figurative expressions without translating literally.",["Ayaw kabalaka, naa ra ko dinhi.","Lisod siya sabton kung literal ra ang pagbasa."]),
    _g("translation","Translation precision and paraphrase","C2","Reformulate meaning while preserving register, implication and discourse function.",["Mahimo nimong ipasabut kini sa laing paagi.","Kinahanglan mapreserbar ang kahulogan ug tono."]),
    _g("discourse_analysis","Discourse analysis and register shifting","C2","Analyze cohesion, stance, genre and register across extended Cebuano texts.",["Sa pormal nga teksto, mas estrikto ang pagpili sa mga pulong.","Ang tono nag-usab depende sa mamiminaw."]),
]

def _v(id_, level, topic, ref, words):
    return VocabularySet(id=id_, level=level, topic=topic, unit_ref=ref, words=[
        VocabularyEntry(word=w, pos=p, definition=d, example=e) for w,p,d,e in words
    ])

VOCABULARY_SETS = [
    _v("greetings_a1","A1","greetings","ceb-a1-unit-1",[("Kumusta","phrase","hello / how are you","Kumusta ka?"),("salamat","phrase","thank you","Salamat kaayo."),("palihog","adverb","please","Palihog tabangi ko."),("maayong buntag","phrase","good morning","Maayong buntag!")]),
    _v("identity_a1","A1","identity","ceb-a1-unit-2",[("ako","pronoun","I / me","Ako si Maria."),("ikaw","pronoun","you","Ikaw ba si Juan?"),("ngalan","noun","name","Unsa imong ngalan?"),("estudyante","noun","student","Estudyante ko.")]),
    _v("family_a1","A1","family","ceb-a1-unit-3",[("inahan","noun","mother","Ang akong inahan naa sa balay."),("amahan","noun","father","Ang akong amahan nagtrabaho."),("igsoon","noun","sibling","Ang akong igsoon naa sa eskwelahan."),("anak","noun","child","Ang anak naa sa balay.")]),
    _v("home_a1","A1","home","ceb-a1-unit-4",[("balay","noun","home","Ang akong balay duol sa merkado."),("kwarto","noun","room","Ang akong kwarto limpyo."),("pultahan","noun","door","Abli ang pultahan."),("lamesa","noun","table","Ang libro naa sa lamesa.")]),
    _v("daily_a1","A1","daily life","ceb-a1-unit-5",[("buntag","noun","morning","Sa buntag, moadto ko sa eskwelahan."),("adlaw","noun","day","Karon nga adlaw init."),("trabaho","noun","work","Aduna koy trabaho karon."),("tubig","noun","water","Moinom ko og tubig.")]),
    _v("food_a1","A1","food","ceb-a1-unit-6",[("bugas","noun","uncooked rice","Naa koy bugas sa kusina."),("tinapay","noun","bread","Mopalit ko og tinapay."),("tsaa","noun","tea","Moinom ko og tsaa."),("mansanas","noun","apple","Nikaon ko og mansanas.")]),
    _v("places_a1","A1","places","ceb-a1-unit-7",[("merkado","noun","market","Ang merkado duol sa among balay."),("eskwelahan","noun","school","Ang eskwelahan duol sa merkado."),("ospital","noun","hospital","Ang ospital naa sa lungsod."),("dalan","noun","road / street","Ang dalan padulong sa merkado.")]),
    _v("communication_a1","A1","communication","ceb-a1-unit-8",[("pangutana","noun","question","Aduna koy pangutana."),("tabang","noun","help","Kinahanglan ko og tabang."),("pinulongan","noun","language","Ang Cebuano usa ka pinulongan."),("istorya","verb","talk / tell","Makig-istorya ko sa akong higala.")]),
    _v("travel_a2","A2","travel","ceb-a2-unit-1",[("biyahe","noun","trip","Nindot ang among biyahe."),("sakyanan","noun","vehicle","Asa ang sakyanan?"),("istasyon","noun","station","Duol ang istasyon."),("lugar","noun","place","Nindot nga lugar kini.")]),
    _v("health_a2","A2","health","ceb-a2-unit-2",[("sakit","noun","illness / pain","Aduna koy sakit."),("tambal","noun","medicine","Kinahanglan ko og tambal."),("doktor","noun","doctor","Nakita nako ang doktor."),("himsog","adjective","healthy","Himsog siya karon.")]),
    _v("study_a2","A2","study","ceb-a2-unit-3",[("leksyon","noun","lesson","Nagsugod ang leksyon."),("eksamen","noun","exam","Adunay eksamen ugma."),("basa","verb","read","Nagbasa ko sa libro."),("sulat","verb","write","Nagsulat siya og tubag.")]),
    _v("work_b1","B1","work","ceb-b1-unit-1",[("katungdanan","noun","responsibility","Importante ang iyang katungdanan."),("miting","noun","meeting","Adunay miting karon."),("proyekto","noun","project","Nahuman ang proyekto."),("desisyon","noun","decision","Lisod ang desisyon.")]),
    _v("society_b1","B1","society","ceb-b1-unit-2",[("komunidad","noun","community","Nagtinabangay ang komunidad."),("serbisyo","noun","service","Maayo ang serbisyo."),("katungod","noun","right","Kinahanglan respetohon ang katungod."),("responsibilidad","noun","responsibility","Aduna kitay responsibilidad.")]),
    _v("environment_b2","B2","environment","ceb-b2-unit-1",[("kalikupan","noun","environment","Atong ampingan ang kalikupan."),("polusyon","noun","pollution","Kinahanglan pakunhuran ang polusyon."),("basura","noun","waste","Ibulag ang basura."),("kahinguhaan","noun","resource","Limitado ang mga kahinguhaan.")]),
    _v("economy_b2","B2","economy","ceb-b2-unit-2",[("ekonomiya","noun","economy","Nag-uswag ang ekonomiya."),("negosyo","noun","business","Adunay gamay nga negosyo."),("presyo","noun","price","Misaka ang presyo."),("kita","noun","income / profit","Nausab ang kita.")]),
    _v("media_c1","C1","media","ceb-c1-unit-1",[("balita","noun","news","Gisusi niya ang balita."),("tinubdan","noun","source","Kinahanglan klaro ang tinubdan."),("report","noun","report","Gibasa nako ang report."),("opinyon","noun","opinion","Lahi ang iyang opinyon.")]),
    _v("academic_c1","C1","academic","ceb-c1-unit-2",[("panukiduki","noun","research","Importante ang panukiduki."),("ebidensya","noun","evidence","Adunay ebidensya."),("pamaagi","noun","method","Klaro ang pamaagi."),("konklusyon","noun","conclusion","Lig-on ang konklusyon.")]),
    _v("institutional_c1","C1","institutional","ceb-c1-unit-3",[("palisiya","noun","policy","Giusab ang palisiya."),("pamaagi","noun","procedure / method","Sunda ang pamaagi."),("dokumento","noun","document","Isumite ang dokumento."),("aplikasyon","noun","application","Giproseso ang aplikasyon.")]),
    _v("culture_c2","C2","culture","ceb-c2-unit-1",[("kabilin","noun","heritage","Importante ang kabilin."),("tradisyon","noun","tradition","Girespeto ang tradisyon."),("panulundon","noun","legacy","Dakong panulundon kini."),("panan-aw","noun","perspective","Lahi ang iyang panan-aw.")]),
    _v("discourse_c2","C2","discourse","ceb-c2-unit-2",[("diskurso","noun","discourse","Komplikado ang diskurso."),("panaglalis","noun","debate / dispute","Adunay panaglalis sa isyu."),("baruganan","noun","position / stance","Klaro ang iyang baruganan."),("pagpasabot","noun","explanation / interpretation","Kinahanglan tukma ang pagpasabot.")]),
]

PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id="greetings_a1",level="A1",situation="greetings",icon="👋",phrases=[PhrasebookEntry(text="Maayong buntag!",context="greeting",register="neutral"),PhrasebookEntry(text="Kumusta ka?",context="asking how someone is",register="neutral"),PhrasebookEntry(text="Ako si ...",context="introducing yourself",register="neutral")]),
    PhrasebookCategory(id="thanks_a1",level="A1",situation="thanks",icon="🙏",phrases=[PhrasebookEntry(text="Salamat.",context="saying thank you",register="neutral"),PhrasebookEntry(text="Daghang salamat.",context="emphasizing thanks",register="neutral"),PhrasebookEntry(text="Walay sapayan.",context="responding to thanks",register="neutral")]),
    PhrasebookCategory(id="shopping_a1",level="A1",situation="shopping",icon="🛒",phrases=[PhrasebookEntry(text="Pila kini?",context="asking the price",register="neutral"),PhrasebookEntry(text="Gusto ko niini.",context="requesting an item",register="neutral"),PhrasebookEntry(text="Aduna moy mas dako?",context="asking for a larger size",register="neutral")]),
    PhrasebookCategory(id="directions_a1",level="A1",situation="directions",icon="🧭",phrases=[PhrasebookEntry(text="Asa ang merkado?",context="asking a location",register="neutral"),PhrasebookEntry(text="Asa paingon sa eskwelahan?",context="asking how to get somewhere",register="neutral"),PhrasebookEntry(text="Sa wala o sa tuo?",context="checking direction",register="neutral")]),
    PhrasebookCategory(id="help_a1",level="A1",situation="help",icon="🆘",phrases=[PhrasebookEntry(text="Palihog tabangi ko.",context="asking for help",register="neutral"),PhrasebookEntry(text="Dili ko kasabot.",context="saying you do not understand",register="neutral"),PhrasebookEntry(text="Palihog sulti pag-usab.",context="asking someone to repeat",register="neutral")]),
    PhrasebookCategory(id="travel_a2",level="A2",situation="travel",icon="🚌",phrases=[PhrasebookEntry(text="Asa ang estasyon?",context="asking for a station",register="neutral"),PhrasebookEntry(text="Pila ang plete?",context="asking the fare",register="neutral"),PhrasebookEntry(text="Asa ko manaog?",context="asking where to get off",register="neutral")]),
    PhrasebookCategory(id="health_a2",level="A2",situation="health",icon="🩺",phrases=[PhrasebookEntry(text="Asa ang ospital?",context="asking for a hospital",register="neutral"),PhrasebookEntry(text="Dili ko maayo ang paminaw.",context="describing discomfort",register="neutral"),PhrasebookEntry(text="Kinahanglan ko og doktor.",context="asking for medical help",register="neutral")]),
    PhrasebookCategory(id="study_a2",level="A2",situation="study",icon="📚",phrases=[PhrasebookEntry(text="Pwede nimo ipasabut?",context="asking for an explanation",register="neutral"),PhrasebookEntry(text="Unsaon ni?",context="asking how to do something",register="neutral"),PhrasebookEntry(text="Mahimo ba nimong balikon?",context="asking for repetition",register="polite")]),
    PhrasebookCategory(id="work_b1",level="B1",situation="work",icon="💼",phrases=[PhrasebookEntry(text="Atong hisgutan ang proyekto.",context="starting a work discussion",register="neutral"),PhrasebookEntry(text="Aduna koy sugyot.",context="offering a suggestion",register="neutral"),PhrasebookEntry(text="Uyon ko niini.",context="expressing agreement",register="neutral")]),
    PhrasebookCategory(id="formal_b2",level="B2",situation="formal communication",icon="📝",phrases=[PhrasebookEntry(text="Palihog isumite ang dokumento.",context="formal instruction",register="formal"),PhrasebookEntry(text="Gipahibalo namo kini sa tanan.",context="formal notice",register="formal"),PhrasebookEntry(text="Salamat sa inyong kooperasyon.",context="formal closing",register="formal")]),
    PhrasebookCategory(id="academic_c1",level="C1",situation="academic discussion",icon="🎓",phrases=[PhrasebookEntry(text="Base sa ebidensya...",context="introducing evidence",register="formal"),PhrasebookEntry(text="Posible nga...",context="hedging a claim",register="academic"),PhrasebookEntry(text="Sa laing bahin...",context="introducing a contrast",register="academic")]),
    PhrasebookCategory(id="presentation_c1",level="C1",situation="presentation",icon="🎤",phrases=[PhrasebookEntry(text="Una, atong tan-awon...",context="opening a point",register="formal"),PhrasebookEntry(text="Ang punto mao nga...",context="stating the main point",register="formal"),PhrasebookEntry(text="Sa katapusan...",context="closing an argument",register="formal")]),
    PhrasebookCategory(id="pragmatics_c2",level="C2",situation="nuance and politeness",icon="🗣️",phrases=[PhrasebookEntry(text="Kung mahimo, palihog...",context="softening a request",register="polite"),PhrasebookEntry(text="Mas maayo tingali kung...",context="tentative suggestion",register="polite"),PhrasebookEntry(text="Nasabtan nako ang imong punto, apan...",context="polite disagreement",register="formal")]),
]

def _unit(level, number, title, grammar_ids, vocab_ids):
    return CurriculumUnit(
        id=f"ceb-{level.lower()}-unit-{number}", level=level, unit_number=number,
        title=title, grammar_points=grammar_ids, vocabulary_set_ids=vocab_ids,
        lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],
        competency_checklist=["Handle a meaningful exchange","Understand and produce level-appropriate Cebuano"],
        default_weeks=2,
    )

CURRICULUM = {
    "A1": [_unit("A1",1,"Pangumusta ug pagpaila",["pronouns","nominal_predicates"],["greetings_a1","identity_a1"]),
           _unit("A1",2,"Pamilya ug relasyon",["possessives","plurality"],["family_a1"]),
           _unit("A1",3,"Balay ug lokasyon",["location","demonstratives"],["home_a1"]),
           _unit("A1",4,"Adlaw-adlaw nga kinabuhi",["present","questions"],["daily_a1"]),
           _unit("A1",5,"Pagkaon ug pagpamalit",["case_markers"],["food_a1"]),
           _unit("A1",6,"Mga lugar ug direksyon",["location","questions"],["places_a1"]),
           _unit("A1",7,"Komunikasyon ug panginahanglan",["negation","pronouns"],["communication_a1"]),
           _unit("A1",8,"A1 nga balik-aral",["pronouns","negation","questions"],["greetings_a1","communication_a1"])],
    "A2": [_unit("A2",1,"Pagbiyahe",["past","motion"],["travel_a2"]),_unit("A2",2,"Panglawas",["present","imperatives"],["health_a2"]),_unit("A2",3,"Pagtuon",["progressive","modality"],["study_a2"]),_unit("A2",4,"Mga plano",["future","modality"],["daily_a1","travel_a2"]),_unit("A2",5,"Pagkumpara",["comparatives","pronoun_clitics"],["identity_a1","places_a1"]),_unit("A2",6,"Paghangyo ug sugo",["imperatives","negation"],["communication_a1"]),_unit("A2",7,"Aspeto sa lihok",["past","progressive"],["daily_a1"]),_unit("A2",8,"A2 nga balik-aral",["future","comparatives"],["travel_a2","study_a2"])],
    "B1": [_unit("B1",1,"Kondisyon ug posibilidad",["conditional","modality"],["work_b1"]),_unit("B1",2,"Mga paryente nga sugnay",["relative","subordination"],["society_b1"]),_unit("B1",3,"Hinungdan ug katuyoan",["cause_purpose","reported"],["work_b1"]),_unit("B1",4,"Pagreport sa impormasyon",["reported","reflexive_reciprocal"],["media_c1"]),_unit("B1",5,"Pagpahinabo ug serbisyo",["causative","passive_voice"],["work_b1"]),_unit("B1",6,"Komunidad ug katungod",["discourse_connectors","cause_purpose"],["society_b1"]),_unit("B1",7,"Paghan-ay sa diskurso",["subordination","reported"],["environment_b2"]),_unit("B1",8,"B1 nga balik-aral",["conditional","relative","reported"],["work_b1","society_b1"])],
    "B2": [_unit("B2",1,"Voice ug focus",["passive_voice","aspect"],["economy_b2"]),_unit("B2",2,"Komplikadong aspeto",["aspect","subordination"],["environment_b2"]),_unit("B2",3,"Kontrasta ug konsesyon",["concession","discourse_connectors"],["society_b1"]),_unit("B2",4,"Mga sugnay ug relasyon",["subordination","relative"],["economy_b2"]),_unit("B2",5,"Ekonomiya ug katilingban",["discourse_connectors","passive_voice"],["economy_b2"]),_unit("B2",6,"Kalikupan",["cause_purpose","concession"],["environment_b2"]),_unit("B2",7,"Pagpasabot ug pagtandi",["comparatives","aspect"],["media_c1"]),_unit("B2",8,"B2 nga balik-aral",["passive_voice","concession","subordination"],["economy_b2","environment_b2"])],
    "C1": [_unit("C1",1,"Panukiduki ug ebidensya",["nominalization","hedging"],["academic_c1"]),_unit("C1",2,"Institusyon ug palisiya",["formal_register","argumentation"],["institutional_c1"]),_unit("C1",3,"Media ug tinubdan",["information_structure","reported"],["media_c1"]),_unit("C1",4,"Embedded nga mga pangutana",["embedded_questions","subordination"],["academic_c1"]),_unit("C1",5,"Pagpresentar sa argumento",["argumentation","discourse_connectors"],["academic_c1"]),_unit("C1",6,"Pormal nga komunikasyon",["formal_register","pragmatics"],["institutional_c1"]),_unit("C1",7,"Pagdumala sa diskurso",["information_structure","hedging"],["media_c1"]),_unit("C1",8,"C1 nga balik-aral",["argumentation","formal_register","embedded_questions"],["academic_c1","institutional_c1"])],
    "C2": [_unit("C2",1,"Pragmatics ug nuance",["pragmatics","idioms"],["discourse_c2"]),_unit("C2",2,"Rhetoric ug literary style",["rhetoric","discourse_analysis"],["culture_c2"]),_unit("C2",3,"Register shifting",["formal_register","pragmatics"],["institutional_c1"]),_unit("C2",4,"Discourse analysis",["discourse_analysis","information_structure"],["discourse_c2"]),_unit("C2",5,"Translation ug paraphrase",["translation","idioms"],["culture_c2"]),_unit("C2",6,"Advanced argumentation",["argumentation","rhetoric"],["discourse_c2"]),_unit("C2",7,"Literary ug media Cebuano",["rhetoric","discourse_analysis"],["culture_c2","media_c1"]),_unit("C2",8,"C2 nga mastery review",["translation","pragmatics","discourse_analysis"],["discourse_c2","culture_c2"])],
}

ASSESSMENT_BANK = [
    AssessmentQuestion(id="ceb-a1-001",skill="vocabulary",difficulty="A1",question="What does “salamat” mean?",options=["hello","thank you","please","goodbye"],correct="thank you"),
    AssessmentQuestion(id="ceb-a1-002",skill="grammar",difficulty="A1",question="Choose the correct sentence for “I am a student.”",options=["Estudyante ko.","Ko estudyante.","Estudyante ang ko.","Ko ang estudyante."],correct="Estudyante ko."),
    AssessmentQuestion(id="ceb-a1-003",skill="grammar",difficulty="A1",question="Which sentence is negative?",options=["Dili ko kasabot.","Kasabot ko.","Naa ko sa balay.","Kini akong libro."],correct="Dili ko kasabot."),
    AssessmentQuestion(id="ceb-a1-004",skill="grammar",difficulty="A2",question="Which sentence describes a completed past action?",options=["Nikaon ko ganina.","Nagkaon ko karon.","Moadto ko ugma.","Nagtuon ko kada adlaw."],correct="Nikaon ko ganina."),
    AssessmentQuestion(id="ceb-b1-001",skill="grammar",difficulty="B1",question="Choose the conditional sentence.",options=["Kung moulan, magpabilin ko sa balay.","Naa ko sa balay.","Nikaon ko ganina.","Moadto ko ugma."],correct="Kung moulan, magpabilin ko sa balay."),
    AssessmentQuestion(id="ceb-b1-002",skill="reading",difficulty="B1",question="Which sentence reports another person's statement?",options=["Miingon siya nga moadto siya.","Moadto ko ugma.","Naa siya sa balay.","Nikaon siya."],correct="Miingon siya nga moadto siya."),
    AssessmentQuestion(id="ceb-b2-001",skill="grammar",difficulty="B2",question="Which sentence expresses concession?",options=["Bisan og kapoy siya, nagpadayon siya.","Naa siya sa balay.","Moadto siya ugma.","Nagtuon siya."],correct="Bisan og kapoy siya, nagpadayon siya."),
    AssessmentQuestion(id="ceb-b2-002",skill="discourse",difficulty="B2",question="Which connector introduces a conclusion or consequence?",options=["Busa","Apan","Kung","Kay"],correct="Busa"),
    AssessmentQuestion(id="ceb-c1-001",skill="academic",difficulty="C1",question="Which phrase appropriately hedges an academic claim?",options=["Posible nga adunay laing hinungdan.","Sigurado gyud kini.","Walay lain nga posibilidad.","Mao gyud kini sa tanang panahon."],correct="Posible nga adunay laing hinungdan."),
    AssessmentQuestion(id="ceb-c1-002",skill="formal",difficulty="C1",question="Which is a formal institutional instruction?",options=["Palihog isumite ang dokumento sa takdang panahon.","Kumusta ka?","Asa ang merkado?","Gusto ko og tubig."],correct="Palihog isumite ang dokumento sa takdang panahon."),
    AssessmentQuestion(id="ceb-c2-001",skill="pragmatics",difficulty="C2",question="Which phrase softens a request?",options=["Kung mahimo, palihog...","Buhata dayon!","Dili ko gusto.","Ayaw na."],correct="Kung mahimo, palihog..."),
    AssessmentQuestion(id="ceb-c2-002",skill="translation",difficulty="C2",question="Which practice best preserves meaning in advanced translation?",options=["Preserve meaning, register and discourse function.","Translate every word literally.","Ignore the social context.","Replace formal language with slang."],correct="Preserve meaning, register and discourse function."),
]
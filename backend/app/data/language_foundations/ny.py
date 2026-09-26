"""Chichewa foundation data for JUBA LISAN.

Language-specific A1-C2 curriculum, vocabulary, phrasebook and assessment data.
"""
from app.data._types import (
    CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry,
    VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def _g(slug, title, level, summary, examples):
    return GrammarTopic(
        slug=slug, title=title, level=level, category="grammar",
        summary=summary, explanation=summary,
        examples=[GrammarExample(text=e) for e in examples],
    )


GRAMMAR_TOPICS = [
    _g("ny-a1-g1", "Subject prefixes", "A1", "Use Chichewa subject markers with common verbs.", ["Ndimaphunzira.", "Akugwira ntchito."]),
    _g("ny-a1-g2", "Copular identity", "A1", "Identify people and roles with ndi.", ["Ine ndine wophunzira.", "Iye ndi mphunzitsi."]),
    _g("ny-a1-g3", "Present and habitual", "A1", "Describe current and habitual actions.", ["Ndikuphunzira.", "Ndimadya m'mawa."]),
    _g("ny-a1-g4", "Negation", "A1", "Negate present and copular clauses.", ["Sindimadya nyama.", "Ine sindine dokotala."]),
    _g("ny-a1-g5", "Questions", "A1", "Ask basic information and yes-no questions.", ["Uli kuti?", "Dzina lako ndi ndani?"]),
    _g("ny-a1-g6", "Possessives", "A1", "Use agreeing possessive forms.", ["Buku langa lili pano.", "Nyumba yathu ndi yayikulu."]),
    _g("ny-a1-g7", "Locatives", "A1", "Express location with ku-, pa- and mu-.", ["Ndili kunyumba.", "Ali kusukulu."]),
    _g("ny-a1-g8", "Noun classes and plurals", "A1", "Recognize common noun-class pairs and agreement.", ["munthu / anthu", "buku / mabuku"]),
    _g("ny-a2-g1", "Noun-class agreement", "A2", "Match adjectives and verbs with noun classes.", ["Mwana wamng'ono akusewera.", "Ana ang'ono akusewera."]),
    _g("ny-a2-g2", "Past tense", "A2", "Talk about completed events.", ["Ndinapita kusukulu dzulo.", "Anagula chakudya."]),
    _g("ny-a2-g3", "Future and intention", "A2", "Express future plans and intentions.", ["Ndidzaphunzira mawa.", "Tidzapita ku Lilongwe."]),
    _g("ny-a2-g4", "Object markers", "A2", "Use object markers in transitive clauses.", ["Ndikumuwona.", "Ndikukonda Chichewa."]),
    _g("ny-a2-g5", "Adjectives and agreement", "A2", "Describe people and things accurately.", ["Nyumba yayikulu.", "Nyumba zazikulu."]),
    _g("ny-a2-g6", "Comparatives", "A2", "Compare qualities and quantities.", ["Uyu ndi wamkulu kuposa uja.", "Ichi ndi chabwino kwambiri."]),
    _g("ny-a2-g7", "Imperatives and polite requests", "A2", "Give instructions and make respectful requests.", ["Bwera kuno.", "Chonde khalani pansi."]),
    _g("ny-a2-g8", "Time and frequency", "A2", "Express time, duration and frequency.", ["Ndimaphunzira tsiku lililonse.", "Anabwera dzulo."]),
    _g("ny-b1-g1", "Relative clauses", "B1", "Modify nouns with relative constructions.", ["Munthu amene anabwera ndi bambo anga.", "Buku limene ndinawerenga ndi latsopano."]),
    _g("ny-b1-g2", "Conditionals", "B1", "Express conditions and consequences.", ["Ngati uphunzira, udzapambana.", "Ngati mvula igwa, tidzakhala kunyumba."]),
    _g("ny-b1-g3", "Infinitive and purpose", "B1", "Use ku- infinitives for activities and purposes.", ["Ndimakonda kuphunzira.", "Anapita kukagula chakudya."]),
    _g("ny-b1-g4", "Causative constructions", "B1", "Express causing another person to act.", ["Mphunzitsi amaphunzitsa ana.", "Anandipangitsa kugwira ntchito."]),
    _g("ny-b1-g5", "Passive voice", "B1", "Foreground the affected participant with passive forms.", ["Buku linawerengedwa ndi mwana.", "Nyumba inamangidwa chaka chatha."]),
    _g("ny-b1-g6", "Aspect and progressive", "B1", "Distinguish ongoing, habitual and completed events.", ["Ndikuphunzira tsopano.", "Ndatha kudya."]),
    _g("ny-b1-g7", "Cause, purpose and result", "B1", "Connect clauses by reason, purpose and consequence.", ["Anachedwa chifukwa cha mvula.", "Anabwera kudzaphunzira."]),
    _g("ny-b1-g8", "Reported speech", "B1", "Report statements, questions and instructions.", ["Anati adzabwera.", "Anandifunsa ngati ndipita."]),
    _g("ny-b2-g1", "Complex subordination", "B2", "Build multi-clause sentences with precise relations.", ["Ngakhale anali atatopa, anapitiriza kugwira ntchito."]),
    _g("ny-b2-g2", "Concession and contrast", "B2", "Express concession, contrast and qualification.", ["Ngakhale ndizovuta, tipitiriza."]),
    _g("ny-b2-g3", "Cohesion and reference", "B2", "Maintain reference across extended discourse.", ["Ntchito yomwe tinakambirana yatha."]),
    _g("ny-b2-g4", "Discourse connectors", "B2", "Organize arguments with causal, contrastive and sequential markers.", ["Chifukwa chake, tiyenera kukonzekera bwino."]),
    _g("ny-b2-g5", "Focus and information structure", "B2", "Highlight topic, focus and contrastive information.", ["Chimene ndikufuna ndi mtendere.", "Lero ndi pamene tinayamba."]),
    _g("ny-b2-g6", "Nominalization", "B2", "Turn events and qualities into noun-like expressions.", ["Kuphunzira Chichewa kumafuna nthawi."]),
    _g("ny-b2-g7", "Modality and stance", "B2", "Express obligation, possibility, certainty and evaluation.", ["N'zotheka kuti abwere.", "Ayenera kuchita zimenezi."]),
    _g("ny-b2-g8", "Register and politeness", "B2", "Adapt wording to social and professional contexts.", ["Mungandiuze kumene kuli ofesi, chonde?"]),
    _g("ny-c1-g1", "Formal and institutional Chichewa", "C1", "Handle formal administrative and institutional language.", ["Msonkhano udzachitika Lolemba kuti tikambirane ndondomeko yatsopano."]),
    _g("ny-c1-g2", "Academic argumentation", "C1", "Present claims, evidence, qualifications and conclusions.", ["Kafukufuku ukusonyeza kuti maphunziro amathandiza kwambiri pa chitukuko."]),
    _g("ny-c1-g3", "Academic hedging", "C1", "Qualify claims with appropriate epistemic caution.", ["N'zotheka kuti zotsatirazi zimadalira momwe gululo lilili."]),
    _g("ny-c1-g4", "Embedded questions", "C1", "Integrate questions into complex sentences.", ["Ndikufuna kudziwa ngati ntchitoyo yatha."]),
    _g("ny-c1-g5", "Information packaging", "C1", "Manage information flow in coherent formal prose.", ["Vuto lalikulu ndi momwe tingakulitsire khalidwe la ntchito."]),
    _g("ny-c1-g6", "Media and public discourse", "C1", "Produce precise public-facing language.", ["Lipoti latsopano latulutsidwa lero."]),
    _g("ny-c1-g7", "Idiomatic and pragmatic meaning", "C1", "Interpret implication, idioms and culturally appropriate wording.", ["Kugwirizana ndi kumene kumathandiza kuti ntchito iyende bwino."]),
    _g("ny-c1-g8", "Professional correspondence", "C1", "Write concise formal requests and responses.", ["Tikukupemphani kuti mutitumizire zikalata zofunika pasanafike tsiku lomaliza."]),
    _g("ny-c2-g1", "Advanced discourse cohesion", "C2", "Control long-range reference and rhetorical progression.", ["Ngakhale lipotili likusonyeza kupita patsogolo, likuwonetsanso mavuto omwe amafuna njira zokhazikika."]),
    _g("ny-c2-g2", "Nuanced modality", "C2", "Express subtle degrees of certainty, obligation and evaluation.", ["Sizingakhale kukokomeza kunena kuti ndondomekoyi ingakhale ndi zotsatira zokhalitsa."]),
    _g("ny-c2-g3", "Complex nominalization", "C2", "Compress propositions for academic and institutional prose.", ["Kusanthula kwa zotsatira za kafukufukuyu kwachititsa kuti pakhale chisankho chatsopano."]),
    _g("ny-c2-g4", "Rhetorical organization", "C2", "Control emphasis, concession and counterargument.", ["Ngakhale yankho ili ndi ubwino, vuto lalikulu ndi kukhazikitsa kwake."]),
    _g("ny-c2-g5", "Legal and administrative formulation", "C2", "Interpret precise obligations and procedural language.", ["Wopempha ntchito ayenera kupereka zikalata zonse zofunika malinga ndi malamulo."]),
    _g("ny-c2-g6", "Translation precision", "C2", "Preserve meaning, register and pragmatic force across languages.", ["Kumasulira kuyenera kusunga tanthauzo ndi kalembedwe ka mawu oyambirira."]),
    _g("ny-c2-g7", "Literary and rhetorical style", "C2", "Interpret figurative language and deliberate stylistic choices.", ["Mawu a wolemba amapanga chithunzi cha moyo wa anthu."]),
    _g("ny-c2-g8", "Discourse analysis and register shifting", "C2", "Shift deliberately among conversational, professional and academic styles.", ["Chichewa cha tsiku ndi tsiku chimasiyana ndi chinenero cha kafukufuku."]),
]


def _v(id_, level, topic, unit, entries):
    return VocabularySet(
        id=id_, level=level, topic=topic, unit_ref=unit,
        words=[VocabularyEntry(word=w, pos=p, definition=d, example=e) for w,p,d,e in entries],
    )


VOCABULARY_SETS = [
    _v("greetings_a1","A1","greetings","ny-a1-unit-1",[("moni","phrase","hello","Moni, bwenzi."),("muli bwanji","phrase","how are you","Muli bwanji lero?"),("tiwonana","phrase","see you","Tiwonana mawa.")]),
    _v("identity_a1","A1","identity","ny-a1-unit-2",[("dzina","noun","name","Dzina langa ndi Banda."),("wophunzira","noun","student","Ndine wophunzira."),("mphunzitsi","noun","teacher","Iye ndi mphunzitsi.")]),
    _v("family_a1","A1","family","ny-a1-unit-3",[("mayi","noun","mother","Mayi ali kunyumba."),("bambo","noun","father","Bambo akugwira ntchito."),("m'bale","noun","sibling","M'bale wanga ali kunyumba.")]),
    _v("home_a1","A1","home","ny-a1-unit-4",[("nyumba","noun","house","Nyumba ndi yayikulu."),("chipinda","noun","room","Chipinda ndi choyera."),("khomo","noun","door","Khomo latseguka.")]),
    _v("routine_a1","A1","routine","ny-a1-unit-5",[("kuphunzira","verb","to study","Ndimaphunzira tsiku lililonse."),("kugwira ntchito","verb","to work","Ndimagwira ntchito lero."),("kugona","verb","to sleep","Ndimagona usiku.")]),
    _v("time_a1","A1","time","ny-a1-unit-6",[("nthawi","noun","time","Ndi nthawi yanji?"),("lero","adverb","today","Ndikugwira ntchito lero."),("mawa","adverb","tomorrow","Ndidzaphunzira mawa.")]),
    _v("food_a1","A1","food","ny-a1-unit-7",[("madzi","noun","water","Ndikufuna madzi."),("mkate","noun","bread","Ndikudya mkate."),("chakudya","noun","food","Ndikufuna chakudya.")]),
    _v("places_a1","A1","places","ny-a1-unit-8",[("sukulu","noun","school","Ndili kusukulu."),("msika","noun","market","Ndili kumsika."),("sitolo","noun","shop","Sitolo ili pafupi.")]),
    _v("people_a2","A2","people and descriptions","ny-a2-unit-1",[("munthu","noun","person","Ndi munthu wabwino."),("mwana","noun","child","Mwana akusewera."),("anthu","noun","people","Anthu akubwera.")]),
    _v("travel_a2","A2","travel","ny-a2-unit-2",[("ulendo","noun","journey","Ulendo wayamba."),("kupita","verb","to go","Ndikupita ku Lilongwe."),("kubwerera","verb","to return","Ndibwerera mawa.")]),
    _v("daily_a2","A2","daily life","ny-a2-unit-3",[("m'mawa","noun","morning","M'mawa ndimagwira ntchito."),("madzulo","noun","evening","Madzulo timacheza."),("tsiku lililonse","phrase","every day","Ndimaphunzira tsiku lililonse.")]),
    _v("health_a2","A2","health","ny-a2-unit-4",[("thanzi","noun","health","Thanzi ndi lofunika."),("dokotala","noun","doctor","Dokotala akubwera."),("ululu","noun","pain","Ndikumva ululu.")]),
    _v("education_b1","B1","education","ny-b1-unit-1",[("maphunziro","noun","education/studies","Maphunziro ndi ofunika."),("kafukufuku","noun","research","Kafukufuku ukupitirira."),("chidziwitso","noun","knowledge/information","Chidziwitso chikuwonjezeka.")]),
    _v("work_b1","B1","work and projects","ny-b1-unit-2",[("ntchito","noun","work/job","Ndili ndi ntchito."),("ntchito yaikulu","noun","project","Ntchito yaikulu yatha."),("msonkhano","noun","meeting","Msonkhano udzakhala mawa.")]),
    _v("society_b1","B1","society","ny-b1-unit-3",[("chitukuko","noun","development","Chitukuko chikupitirirabe."),("mgwirizano","noun","cooperation","Mgwirizano ndi wofunika."),("ntchito za anthu","noun","public services","Ntchito za anthu zikufunika.")]),
    _v("environment_b1","B1","environment","ny-b1-unit-4",[("chilengedwe","noun","environment","Tiyenera kuteteza chilengedwe."),("madzi","noun","water","Madzi oyera ndi ofunika."),("nkhalango","noun","forest","Nkhalango ikutetezedwa.")]),
    _v("economy_b2","B2","economy","ny-b2-unit-1",[("chuma","noun","economy/wealth","Chuma chikukula."),("ndalama","noun","money","Ndalamazi ndizofunika."),("msika","noun","market","Msika ukusintha.")]),
    _v("governance_b2","B2","governance","ny-b2-unit-2",[("boma","noun","government","Boma lalengeza ndondomeko."),("malamulo","noun","laws","Malamulo ayenera kutsatiridwa."),("ndondomeko","noun","policy/plan","Ndondomeko yatsopano yalengezedwa.")]),
    _v("communication_b2","B2","communication","ny-b2-unit-3",[("uthenga","noun","message","Uthenga wafika."),("kulankhulana","verb","to communicate","Kulankhulana ndikofunika."),("nkhani","noun","news/topic","Nkhani yatsopanoyi yafalikira.")]),
    _v("media_b2","B2","media","ny-b2-unit-4",[("wailesi","noun","radio","Ndamva pa wailesi."),("lipoti","noun","report","Lipoti latulutsidwa."),("kafukufuku","noun","survey/research","Kafukufuku wafalitsidwa.")]),
    _v("academic_c1","C1","academic language","ny-c1-unit-1",[("umboni","noun","evidence","Tikufuna umboni wokwanira."),("kusanthula","noun","analysis","Kusanthula kukupitirirabe."),("mfundo","noun","argument/point","Mfundo yayikulu ndi yomveka.")]),
    _v("professional_c1","C1","professional language","ny-c1-unit-2",[("chikalata","noun","document","Tumizani chikalata."),("malangizo","noun","instructions","Malangizo ayenera kutsatiridwa."),("udindo","noun","responsibility","Udindo wake ndi kuyang'anira.")]),
    _v("abstract_c1","C1","abstract concepts","ny-c1-unit-3",[("zotsatira","noun","results/effects","Zotsatira zikusonyeza kusintha."),("cholinga","noun","objective","Cholinga ndi kukulitsa khalidwe."),("yankho","noun","solution/answer","Tapeza yankho.")]),
    _v("rhetoric_c2","C2","rhetoric","ny-c2-unit-1",[("mkangano","noun","debate/conflict","Mkangano wakhazikitsidwa pa umboni."),("mapeto","noun","conclusion/end","Mapeto alengezedwa."),("mfundo yayikulu","noun","main point","Mfundo yayikulu ndi yomveka.")]),
    _v("discourse_c2","C2","discourse analysis","ny-c2-unit-2",[("mawu","noun","expression/words","Mawu ayenera kugwirizana ndi omvera."),("tanthauzo","noun","meaning","Tanthauzo lake ndi lomveka."),("kalembedwe","noun","style of writing","Kalembedwe ka wolemba ndi kapadera.")]),
]


def _unit(level, n, title, grammar, vocab, checks):
    return CurriculumUnit(
        id=f"ny-{level.lower()}-unit-{n}", level=level, unit_number=n,
        title=title, grammar_points=[grammar], vocabulary_set_ids=[vocab],
        lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],
        competency_checklist=checks, default_weeks=1 if level in ("A1","A2") else 2,
    )


CURRICULUM = {
    "A1": [
        _unit("A1",1,"Greetings and introductions","ny-a1-g1","greetings_a1",["Greet someone naturally.","Introduce yourself."]),
        _unit("A1",2,"Identity","ny-a1-g2","identity_a1",["Identify people and roles."]),
        _unit("A1",3,"Family","ny-a1-g3","family_a1",["Describe immediate family."]),
        _unit("A1",4,"Home and location","ny-a1-g7","home_a1",["Say where people and objects are."]),
        _unit("A1",5,"Daily routine","ny-a1-g3","routine_a1",["Describe a simple routine."]),
        _unit("A1",6,"Time","ny-a1-g5","time_a1",["Ask and answer basic time questions."]),
        _unit("A1",7,"Food and drink","ny-a1-g4","food_a1",["Order simple food and drink."]),
        _unit("A1",8,"Places","ny-a1-g8","places_a1",["Name common places and movements."]),
    ],
    "A2": [
        _unit("A2",1,"People and agreement","ny-a2-g1","people_a2",["Use noun-class agreement in descriptions."]),
        _unit("A2",2,"Travel","ny-a2-g2","travel_a2",["Talk about past and future travel."]),
        _unit("A2",3,"Daily life","ny-a2-g8","daily_a2",["Describe routines and time references."]),
        _unit("A2",4,"Health","ny-a2-g3","health_a2",["Describe simple health needs."]),
        _unit("A2",5,"Objects and ownership","ny-a2-g4","identity_a1",["Use object and possessive forms."]),
        _unit("A2",6,"Descriptions and comparison","ny-a2-g6","people_a2",["Compare people and things."]),
        _unit("A2",7,"Requests and instructions","ny-a2-g7","places_a1",["Make polite requests and instructions."]),
        _unit("A2",8,"Integrated conversation","ny-a2-g8","daily_a2",["Sustain an everyday exchange."]),
    ],
    "B1": [
        _unit("B1",1,"Education","ny-b1-g1","education_b1",["Describe academic topics with relative clauses."]),
        _unit("B1",2,"Work and projects","ny-b1-g3","work_b1",["Discuss work and projects."]),
        _unit("B1",3,"Society","ny-b1-g2","society_b1",["Explain conditions and consequences."]),
        _unit("B1",4,"Environment","ny-b1-g7","environment_b1",["Give reasons and purposes."]),
        _unit("B1",5,"Passive and causative","ny-b1-g4","work_b1",["Describe actions with passive and causative forms."]),
        _unit("B1",6,"Aspect and events","ny-b1-g6","daily_a2",["Distinguish ongoing and completed events."]),
        _unit("B1",7,"Reported speech","ny-b1-g8","communication_b2",["Report statements and questions."]),
        _unit("B1",8,"Integrated communication","ny-b1-g5","education_b1",["Give a connected explanation."]),
    ],
    "B2": [
        _unit("B2",1,"Economy","ny-b2-g1","economy_b2",["Explain economic relationships."]),
        _unit("B2",2,"Governance","ny-b2-g4","governance_b2",["Discuss institutional processes."]),
        _unit("B2",3,"Communication","ny-b2-g5","communication_b2",["Control topic and focus."]),
        _unit("B2",4,"Media","ny-b2-g6","media_b2",["Summarize media information."]),
        _unit("B2",5,"Nominalization","ny-b2-g6","academic_c1",["Use formal noun phrases."]),
        _unit("B2",6,"Modality","ny-b2-g7","governance_b2",["Express certainty and obligation."]),
        _unit("B2",7,"Register","ny-b2-g8","professional_c1",["Adapt language to professional contexts."]),
        _unit("B2",8,"Complex discourse","ny-b2-g2","communication_b2",["Build a coherent multi-paragraph argument."]),
    ],
    "C1": [
        _unit("C1",1,"Formal institutions","ny-c1-g1","professional_c1",["Write formal institutional prose."]),
        _unit("C1",2,"Academic argumentation","ny-c1-g2","academic_c1",["Present claims and evidence coherently."]),
        _unit("C1",3,"Academic hedging","ny-c1-g3","abstract_c1",["Qualify claims precisely."]),
        _unit("C1",4,"Embedded questions","ny-c1-g4","communication_b2",["Integrate questions into complex prose."]),
        _unit("C1",5,"Information structure","ny-c1-g5","discourse_c2",["Manage information flow."]),
        _unit("C1",6,"Media discourse","ny-c1-g6","media_b2",["Produce precise public language."]),
        _unit("C1",7,"Pragmatics and idioms","ny-c1-g7","rhetoric_c2",["Interpret implied and idiomatic meaning."]),
        _unit("C1",8,"Professional correspondence","ny-c1-g8","professional_c1",["Draft precise professional requests."]),
    ],
    "C2": [
        _unit("C2",1,"Cohesion","ny-c2-g1","discourse_c2",["Control long-range discourse cohesion."]),
        _unit("C2",2,"Nuanced modality","ny-c2-g2","abstract_c1",["Express subtle stance."]),
        _unit("C2",3,"Advanced nominalization","ny-c2-g3","academic_c1",["Handle dense academic formulations."]),
        _unit("C2",4,"Rhetorical organization","ny-c2-g4","rhetoric_c2",["Build and rebut complex arguments."]),
        _unit("C2",5,"Legal and administrative language","ny-c2-g5","professional_c1",["Interpret precise procedural wording."]),
        _unit("C2",6,"Translation precision","ny-c2-g6","discourse_c2",["Preserve register and pragmatic force."]),
        _unit("C2",7,"Literary style","ny-c2-g7","rhetoric_c2",["Interpret figurative and rhetorical language."]),
        _unit("C2",8,"Discourse and register shifting","ny-c2-g8","discourse_c2",["Shift deliberately among registers."]),
    ],
}


PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id="ny-greetings-a1",level="A1",situation="greetings",icon="👋",phrases=[
        PhrasebookEntry(text="Moni.",context="Hello.",register="neutral"),
        PhrasebookEntry(text="Muli bwanji?",context="How are you?",register="neutral"),
        PhrasebookEntry(text="Ndili bwino, zikomo.",context="I am fine, thank you.",register="neutral"),
    ]),
    PhrasebookCategory(id="ny-introduction-a1",level="A1",situation="introductions",icon="👤",phrases=[
        PhrasebookEntry(text="Dzina langa ndi Banda.",context="My name is Banda.",register="neutral"),
        PhrasebookEntry(text="Ndine wophunzira.",context="I am a student.",register="neutral"),
    ]),
    PhrasebookCategory(id="ny-thanks-a1",level="A1",situation="thanks",icon="🙏",phrases=[
        PhrasebookEntry(text="Zikomo kwambiri.",context="Thank you very much.",register="neutral"),
        PhrasebookEntry(text="Palibe kanthu.",context="You are welcome.",register="neutral"),
    ]),
    PhrasebookCategory(id="ny-shopping-a1",level="A1",situation="shopping",icon="🛒",phrases=[
        PhrasebookEntry(text="Izi ndi ndalama zingati?",context="How much does this cost?",register="neutral"),
        PhrasebookEntry(text="Ndikufuna ichi.",context="I want this.",register="neutral"),
        PhrasebookEntry(text="Chonde, chepetsani mtengo.",context="Please lower the price.",register="polite"),
    ]),
    PhrasebookCategory(id="ny-help-a1",level="A1",situation="help",icon="🆘",phrases=[
        PhrasebookEntry(text="Chonde ndithandizeni.",context="Please help me.",register="polite"),
        PhrasebookEntry(text="Sindikumvetsa.",context="I do not understand.",register="neutral"),
        PhrasebookEntry(text="Chonde bwerezaninso.",context="Please repeat.",register="polite"),
    ]),
    PhrasebookCategory(id="ny-travel-a2",level="A2",situation="travel",icon="🚌",phrases=[
        PhrasebookEntry(text="Ndikupita ku Lilongwe.",context="I am going to Lilongwe.",register="neutral"),
        PhrasebookEntry(text="Ndidzabwerera liti?",context="When will I return?",register="neutral"),
    ]),
    PhrasebookCategory(id="ny-health-a2",level="A2",situation="health",icon="🩺",phrases=[
        PhrasebookEntry(text="Sindikumva bwino.",context="I do not feel well.",register="neutral"),
        PhrasebookEntry(text="Ndikufuna dokotala.",context="I need a doctor.",register="neutral"),
    ]),
    PhrasebookCategory(id="ny-study-b1",level="B1",situation="study",icon="📚",phrases=[
        PhrasebookEntry(text="Ndikuphunzira Chichewa.",context="I am studying Chichewa.",register="neutral"),
        PhrasebookEntry(text="Izi zikutanthauza chiyani?",context="What does this mean?",register="neutral"),
    ]),
    PhrasebookCategory(id="ny-work-b1",level="B1",situation="work",icon="💼",phrases=[
        PhrasebookEntry(text="Msonkhano udzakhala liti?",context="When will the meeting be?",register="neutral"),
        PhrasebookEntry(text="Ntchito yatha.",context="The work is finished.",register="neutral"),
    ]),
    PhrasebookCategory(id="ny-professional-b2",level="B2",situation="professional",icon="🏢",phrases=[
        PhrasebookEntry(text="Mungandipatse zambiri?",context="Could you give me more details?",register="polite"),
        PhrasebookEntry(text="Chifukwa chake, tikupempha nthawi yowonjezera.",context="For that reason, we request more time.",register="formal"),
    ]),
    PhrasebookCategory(id="ny-academic-c1",level="C1",situation="academic",icon="🎓",phrases=[
        PhrasebookEntry(text="Kafukufuku ukusonyeza kuti...",context="The research shows that...",register="formal"),
        PhrasebookEntry(text="N'zotheka kuti...",context="It is possible that...",register="formal"),
    ]),
    PhrasebookCategory(id="ny-formal-c1",level="C1",situation="formal correspondence",icon="✉️",phrases=[
        PhrasebookEntry(text="Tikukupemphani kuti mutitumizire...",context="We request that you send us...",register="formal"),
        PhrasebookEntry(text="Tikukuthokozani chifukwa cha mgwirizano wanu.",context="We thank you for your cooperation.",register="formal"),
    ]),
    PhrasebookCategory(id="ny-debate-c2",level="C2",situation="discussion and debate",icon="🗣️",phrases=[
        PhrasebookEntry(text="Ngakhale zimenezo zili zoona, vuto lalikulu ndi...",context="Although that is true, the main issue is...",register="formal"),
        PhrasebookEntry(text="Kumbali ina...",context="On the other hand...",register="formal"),
    ]),
]


ASSESSMENT_BANK = [
    AssessmentQuestion(id="ny-a1-001",skill="communication",difficulty="A1",question="Which Chichewa phrase means “Hello”?",options=["Moni.","Zikomo.","Sindikumvetsa.","Muli bwanji?"],correct="Moni."),
    AssessmentQuestion(id="ny-a1-002",skill="communication",difficulty="A1",question="Which phrase means “How are you?”",options=["Muli bwanji?","Zikomo.","Ndikufuna ichi.","Chonde ndithandizeni."],correct="Muli bwanji?"),
    AssessmentQuestion(id="ny-a1-003",skill="vocabulary",difficulty="A1",question="Which word means “name”?",options=["dzina","nyumba","madzi","sukulu"],correct="dzina"),
    AssessmentQuestion(id="ny-a1-004",skill="grammar",difficulty="A1",question="Complete: “I am at home” — “Ndili ___.”",options=["kunyumba","kusukulu","kumsika","pa tebulo"],correct="kunyumba"),
    AssessmentQuestion(id="ny-a2-001",skill="grammar",difficulty="A2",question="Which pair shows a common singular/plural contrast?",options=["munthu / anthu","mayi / bambo","madzi / mkate","sukulu / sitolo"],correct="munthu / anthu"),
    AssessmentQuestion(id="ny-a2-002",skill="communication",difficulty="A2",question="Which phrase is a polite request?",options=["Chonde khalani pansi.","Moni.","Ndidzaphunzira mawa.","Ndili kusukulu."],correct="Chonde khalani pansi."),
    AssessmentQuestion(id="ny-b1-001",skill="grammar",difficulty="B1",question="Which sentence introduces a condition?",options=["Ngati uphunzira, udzapambana.","Moni.","Ndikufuna madzi.","Ndili kunyumba."],correct="Ngati uphunzira, udzapambana."),
    AssessmentQuestion(id="ny-b1-002",skill="grammar",difficulty="B1",question="Which example is passive?",options=["Buku linawerengedwa ndi mwana.","Ndimaphunzira.","Ndikupita kusukulu.","Ndikufuna madzi."],correct="Buku linawerengedwa ndi mwana."),
    AssessmentQuestion(id="ny-b2-001",skill="discourse",difficulty="B2",question="Which phrase marks a consequence?",options=["Chifukwa chake","Moni","Muli bwanji?","Dzina langa ndi Banda."],correct="Chifukwa chake"),
    AssessmentQuestion(id="ny-b2-002",skill="formal",difficulty="B2",question="Which phrase fits a formal request?",options=["Tikukupemphani kuti mutitumizire...","Mpa ichi.","Moni.","Muli bwanji?"],correct="Tikukupemphani kuti mutitumizire..."),
    AssessmentQuestion(id="ny-c1-001",skill="academic",difficulty="C1",question="Which phrase appropriately hedges an academic claim?",options=["N'zotheka kuti...","Moni.","Mpa ichi.","Zikomo."],correct="N'zotheka kuti..."),
    AssessmentQuestion(id="ny-c1-002",skill="formal",difficulty="C1",question="Which sentence is a formal institutional request?",options=["Tikukupemphani kuti mutitumizire zikalata zofunika.","Ndili kunyumba.","Ndikufuna madzi.","Muli bwanji?"],correct="Tikukupemphani kuti mutitumizire zikalata zofunika."),
    AssessmentQuestion(id="ny-c2-001",skill="discourse",difficulty="C2",question="Which phrase introduces a counterargument?",options=["Ngakhale zimenezo zili zoona, vuto lalikulu ndi...","Moni.","Ndili bwino.","Nitwa Banda."],correct="Ngakhale zimenezo zili zoona, vuto lalikulu ndi..."),
    AssessmentQuestion(id="ny-c2-002",skill="translation",difficulty="C2",question="What should advanced translation preserve besides literal meaning?",options=["Register and pragmatic force","Only word order","Only punctuation","Only word length"],correct="Register and pragmatic force"),
]

"""Shona foundation data for JUBA LISAN.

Language-specific Shona structures, native examples, vocabulary, phrasebook,
curriculum sequencing and assessments for A1-C2.
"""
from app.data._types import (
    AssessmentQuestion, CurriculumUnit, GrammarExample, GrammarTopic,
    PhrasebookCategory, PhrasebookEntry, VocabularyEntry, VocabularySet,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def _g(slug, title, level, summary, examples):
    return GrammarTopic(
        slug=slug, title=title, level=level, category="grammar",
        summary=summary, explanation=summary,
        examples=[GrammarExample(text=e) for e in examples],
    )


GRAMMAR_TOPICS = [
    _g("sn-a1-g1", "Personal pronouns and subject prefixes", "A1", "Use personal pronouns and common subject markers.", ["Ini ndiri mudzidzi.", "Iye mudzidzisi."]),
    _g("sn-a1-g2", "Copulative identity", "A1", "Identify people and things with ndi/iri/ichi patterns.", ["Ndiri mudzidzi.", "Iri ibhuku."]),
    _g("sn-a1-g3", "Present and habitual action", "A1", "Describe current and habitual activities with verbal prefixes.", ["Ndinodzidza.", "Anoshanda mangwanani."]),
    _g("sn-a1-g4", "Negation", "A1", "Negate basic nominal and verbal clauses.", ["Handisi kumba.", "Handidzidzi nhasi."]),
    _g("sn-a1-g5", "Questions", "A1", "Ask yes-no and information questions.", ["Uri kupi?", "Unonzi ani?"]),
    _g("sn-a1-g6", "Possession", "A1", "Express possession and relationships.", ["Iri ibhuku rangu.", "Imba yedu yakakura."]),
    _g("sn-a1-g7", "Locatives", "A1", "Say where people and objects are using pa-, ku-, mu- forms.", ["Ndiri kumba.", "Bhuku riri patafura."]),
    _g("sn-a1-g8", "Noun classes and plurals", "A1", "Recognize common Shona noun-class pairs.", ["munhu / vanhu", "bhuku / mabhuku"]),
    _g("sn-a2-g1", "Noun-class agreement", "A2", "Match adjectives and verbs with noun-class agreement.", ["Munhu akanaka.", "Vanhu vakanaka."]),
    _g("sn-a2-g2", "Past tense", "A2", "Talk about completed events.", ["Ndakaenda kuchikoro.", "Akauya nezuro."]),
    _g("sn-a2-g3", "Future and intention", "A2", "Express future plans with common future forms.", ["Ndichaenda mangwana.", "Tichadzidza."]),
    _g("sn-a2-g4", "Object markers", "A2", "Use object markers in transitive clauses.", ["Ndiri kumuona.", "Ndichazvitenga."]),
    _g("sn-a2-g5", "Adjectives and concords", "A2", "Describe nouns with appropriate agreement.", ["Imba huru.", "Mabhuku makuru."]),
    _g("sn-a2-g6", "Comparatives", "A2", "Compare people and things.", ["Uyu mukuru kupfuura uya.", "Ichi chiri nani."]),
    _g("sn-a2-g7", "Imperatives and polite requests", "A2", "Give instructions and polite requests.", ["Huya pano.", "Ndibatsirei, ndapota."]),
    _g("sn-a2-g8", "Time and frequency", "A2", "Place events in time and express frequency.", ["Ndinodzidza zuva nezuva.", "Akauya nezuro."]),
    _g("sn-b1-g1", "Relative clauses", "B1", "Link nouns to relative clauses with class-sensitive forms.", ["Munhu wandakaona ndiye mudzidzisi.", "Bhuku randaverenga idzva."]),
    _g("sn-b1-g2", "Conditionals", "B1", "Express conditions and consequences.", ["Kana ukadzidza, uchapasa.", "Kana mvura ikanaya, tichagara kumba."]),
    _g("sn-b1-g3", "Infinitives and verbal nouns", "B1", "Use ku- infinitives for activities and purpose.", ["Ndinoda kudzidza.", "Akaenda kunotenga."]),
    _g("sn-b1-g4", "Causative constructions", "B1", "Express causing another action.", ["Mudzidzisi akavadzidzisa.", "Akandinyoresa."]),
    _g("sn-b1-g5", "Passive voice", "B1", "Foreground affected participants in passive clauses.", ["Bhuku rakaverengwa nemudzidzi.", "Imba yakavakwa gore rapfuura."]),
    _g("sn-b1-g6", "Aspect and event structure", "B1", "Distinguish ongoing, habitual and completed events.", ["Ari kudzidza.", "Akatopedza basa."]),
    _g("sn-b1-g7", "Cause, purpose and result", "B1", "Connect clauses by reason, purpose and consequence.", ["Akanonoka nekuda kwemvura.", "Akauya kuzodzidza."]),
    _g("sn-b1-g8", "Reported speech", "B1", "Report statements, questions and instructions.", ["Akati achauya.", "Akabvunza kana ndaenda."]),
    _g("sn-b2-g1", "Complex subordination", "B2", "Build multi-clause sentences with precise relations.", ["Kunyange zvazvo akaneta, akaramba achishanda."]),
    _g("sn-b2-g2", "Concession and contrast", "B2", "Express concession, contrast and qualification.", ["Kunyange zvakaoma, tichaenderera mberi."]),
    _g("sn-b2-g3", "Discourse reference and cohesion", "B2", "Maintain reference across extended discourse.", ["Nyaya yatakataura nezvayo yakakosha."]),
    _g("sn-b2-g4", "Discourse connectors", "B2", "Organize explanations with causal and sequential markers.", ["Naizvozvo, tinofanira kugadzirira."]),
    _g("sn-b2-g5", "Focus and information structure", "B2", "Highlight topic, focus and contrastive information.", ["Chandinoda imvura.", "Nhasi ndipo patakatanga."]),
    _g("sn-b2-g6", "Nominalization", "B2", "Use noun-like expressions for events and properties.", ["Kudzidza mutauro kunoda nguva."]),
    _g("sn-b2-g7", "Modality and stance", "B2", "Express possibility, obligation, certainty and evaluation.", ["Zvinokwanisika kuti achauya.", "Anofanira kuenda."]),
    _g("sn-b2-g8", "Register and politeness", "B2", "Adapt wording to social and professional settings.", ["Munganditsanangurira here, ndapota?"]),
    _g("sn-c1-g1", "Formal and institutional Shona", "C1", "Handle formal administrative and institutional language.", ["Musangano uchaitwa neMuvhuro kuti tiongorore chirongwa chitsva."]),
    _g("sn-c1-g2", "Academic argumentation", "C1", "Present claims, evidence, qualifications and conclusions.", ["Tsvakurudzo inoratidza kuti dzidzo ine basa guru mukusimudzira upfumi."]),
    _g("sn-c1-g3", "Academic hedging", "C1", "Qualify claims precisely.", ["Zvinogona kunge zviri izvo kuti mhedzisiro inosiyana nemamiriro eboka."]),
    _g("sn-c1-g4", "Embedded questions", "C1", "Integrate questions into complex clauses.", ["Ndinoda kuziva kana chirongwa chapera."]),
    _g("sn-c1-g5", "Information packaging", "C1", "Control information flow in extended prose.", ["Nyaya huru ndeyekuti tingavandudza sei basa iri."]),
    _g("sn-c1-g6", "Media and public discourse", "C1", "Produce precise public-facing language.", ["Mushumo mutsva wakaburitswa nhasi."]),
    _g("sn-c1-g7", "Idiomatic and pragmatic meaning", "C1", "Interpret implication and culturally appropriate phrasing.", ["Kubatana ndiko kunoita kuti basa rifambe zvakanaka."]),
    _g("sn-c1-g8", "Professional correspondence", "C1", "Write concise formal requests and responses.", ["Tinokumbira kuti mutitumire magwaro anodiwa zuva rekupedzisira risati rasvika."]),
    _g("sn-c2-g1", "Advanced discourse cohesion", "C2", "Control long-range reference and rhetorical progression.", ["Kunyange mushumo uchiratidza kufambira mberi, unoratidzawo zvipingamupinyi zvinoda mhinduro dzakasimba."]),
    _g("sn-c2-g2", "Nuanced modality", "C2", "Express subtle degrees of certainty, obligation and evaluation.", ["Hazvingave kuwedzeredza kutaura kuti chirongwa ichi chinogona kuva nemigumisiro yenguva refu."]),
    _g("sn-c2-g3", "Complex nominalization", "C2", "Compress complex propositions for academic prose.", ["Ongororo yezvakabuda mutsvakurudzo yakatungamirira pakutorwa kwechisarudzo chitsva."]),
    _g("sn-c2-g4", "Rhetorical organization", "C2", "Control emphasis, concession and counterargument.", ["Kunyange mhinduro iyi iine zvayakanakira, dambudziko guru nderekushandiswa kwayo."]),
    _g("sn-c2-g5", "Legal and administrative formulation", "C2", "Interpret precise obligations and procedural language.", ["Munhu anokumbira basa anofanira kupa magwaro ose anodiwa maererano nemitemo."]),
    _g("sn-c2-g6", "Translation precision", "C2", "Preserve meaning, register and pragmatic force in translation.", ["Dudziro inofanira kuchengetedza zvinorehwa uye chimiro chemashoko ekutanga."]),
    _g("sn-c2-g7", "Literary and rhetorical style", "C2", "Interpret figurative language and deliberate stylistic choices.", ["Munyori anoshandisa mufananidzo kuvaka pfungwa yehupenyu hwevanhu."]),
    _g("sn-c2-g8", "Discourse analysis and register shifting", "C2", "Shift deliberately among conversational, professional and academic styles.", ["Mutauro wekutaura mazuva ose unosiyana nemutauro wetsvakurudzo."]),
]


def _vset(id_, level, topic, unit_ref, entries):
    return VocabularySet(
        id=id_, level=level, topic=topic, unit_ref=unit_ref,
        words=[VocabularyEntry(word=w, pos=p, definition=d, example=e) for w,p,d,e in entries],
    )


VOCABULARY_SETS = [
    _vset("greetings_a1","A1","greetings","sn-a1-unit-1",[("mhoro","phrase","hello","Mhoro, shamwari."),("mazvita","phrase","thank you","Mazvita zvikuru."),("mangwanani","noun","morning","Mangwanani akanaka.")]),
    _vset("identity_a1","A1","identity","sn-a1-unit-2",[("zita","noun","name","Zita rangu ndiTariro."),("ini","pronoun","I","Ini ndiri mudzidzi."),("iwe","pronoun","you","Iwe uri kupi?")]),
    _vset("family_a1","A1","family","sn-a1-unit-3",[("amai","noun","mother","Amai vari kumba."),("baba","noun","father","Baba vari kubasa."),("mwana","noun","child","Mwana ari kuchikoro.")]),
    _vset("home_a1","A1","home","sn-a1-unit-4",[("imba","noun","house","Imba yedu yakakura."),("kamuri","noun","room","Kamuri kangu kakachena."),("gonhi","noun","door","Gonhi rakavhurika.")]),
    _vset("routine_a1","A1","routine","sn-a1-unit-5",[("kudzidza","verb","to study","Ndinodzidza mangwanani."),("kuenda","verb","to go","Ndinoenda kuchikoro."),("kudya","verb","to eat","Ndinodya mangwanani.")]),
    _vset("time_a1","A1","time","sn-a1-unit-6",[("nguva","noun","time","Inguvai?"),("nhasi","adverb","today","Nhasi ndiri kumba."),("mangwana","adverb","tomorrow","Mangwana ndinoenda kuchikoro.")]),
    _vset("food_a1","A1","food","sn-a1-unit-7",[("mvura","noun","water","Ndinoda mvura."),("sadza","noun","maize meal","Ndinodya sadza."),("tii","noun","tea","Ndinonwa tii.")]),
    _vset("places_a1","A1","places","sn-a1-unit-8",[("chikoro","noun","school","Ndiri kuchikoro."),("musika","noun","market","Musika uri pedyo."),("pano","adverb","here","Ndiri pano.")]),
    _vset("people_a2","A2","people","sn-a2-unit-1",[("munhu","noun","person","Munhu akanaka."),("vanhu","noun","people","Vanhu vari pano."),("shamwari","noun","friend","Shamwari yangu auya.")]),
    _vset("travel_a2","A2","travel","sn-a2-unit-2",[("rwendo","noun","journey","Rwendo rwedu rwakatanga."),("bhazi","noun","bus","Bhazi rasvika."),("kuenda","verb","to go","Tiri kuenda kuHarare.")]),
    _vset("daily_life_a2","A2","daily life","sn-a2-unit-3",[("mangwanani","noun","morning","Ndinomuka mangwanani."),("manheru","noun","evening","Manheru tinotaura."),("zuva nezuva","phrase","every day","Ndinodzidza zuva nezuva.")]),
    _vset("health_a2","A2","health","sn-a2-unit-4",[("utano","noun","health","Utano hwakakosha."),("chiremba","noun","doctor","Chiremba ari kuuya."),("kurwadziwa","verb","to hurt","Musoro uri kurwadziwa.")]),
    _vset("education_b1","B1","education","sn-b1-unit-1",[("dzidzo","noun","education","Dzidzo yakakosha."),("tsvakurudzo","noun","research","Tsvakurudzo iri kuenderera."),("ruzivo","noun","knowledge/information","Ruzivo rwuri kuwedzera.")]),
    _vset("work_b1","B1","work","sn-b1-unit-2",[("basa","noun","work/job","Ndine basa."),("chirongwa","noun","project/programme","Chirongwa chapera."),("musangano","noun","meeting","Musangano uchaitwa mangwana.")]),
    _vset("society_b1","B1","society","sn-b1-unit-3",[("budiriro","noun","development/success","Budiriro iri kuenderera."),("kubatana","noun","cooperation/unity","Kubatana kwakakosha."),("rubatsiro","noun","assistance","Rubatsiro runodiwa.")]),
    _vset("environment_b1","B1","environment","sn-b1-unit-4",[("nharaunda","noun","environment/community","Tinofanira kuchengetedza nharaunda."),("sango","noun","forest","Sango riri kuchengetedzwa."),("rwizi","noun","river","Rwizi rwakazara.")]),
    _vset("economy_b2","B2","economy","sn-b2-unit-1",[("upfumi","noun","economy/wealth","Upfumi hwenyika huri kukura."),("kudyara mari","verb","to invest","Kudyara mari kunoda ruzivo."),("musika","noun","market","Musika uri kuchinja.")]),
    _vset("governance_b2","B2","governance","sn-b2-unit-2",[("hutongi","noun","governance","Hutongi hwakanaka hunodiwa."),("mutemo","noun","law","Mutemo unofanira kuteverwa."),("bumbiro","noun","constitution/policy framework","Bumbiro rinosimbisa kodzero.")]),
    _vset("communication_b2","B2","communication","sn-b2-unit-3",[("mashoko","noun","information/news","Mashoko matsva aburitswa."),("kutaurirana","verb","communication","Kutaurirana kwakakosha."),("shoko","noun","message/word","Shoko rasvika.")]),
    _vset("media_b2","B2","media","sn-b2-unit-4",[("vezvenhau","noun","media","Vezvenhau vaburitsa nhau."),("mushumo","noun","report","Mushumo waburitswa."),("hurukuro","noun","discussion/interview","Hurukuro iri kuenderera.")]),
    _vset("academic_c1","C1","academic language","sn-c1-unit-1",[("pfungwa","noun","idea","Pfungwa iyi inofanira kutsanangurwa."),("uchapupu","noun","evidence","Tinoda uchapupu hwakasimba."),("ongororo","noun","analysis","Ongororo iri kuenderera.")]),
    _vset("professional_c1","C1","professional language","sn-c1-unit-2",[("gwaro","noun","document","Tumirai gwaro."),("mirayiridzo","noun","instructions/regulations","Mirayiridzo inofanira kuteverwa."),("basa","noun","responsibility/work","Basa rake nderekutarisa.")]),
    _vset("abstract_c1","C1","abstract concepts","sn-c1-unit-3",[("mhedzisiro","noun","result/consequence","Mhedzisiro yacho yakajeka."),("chinangwa","noun","objective","Chinangwa ndechekuvandudza basa."),("mhinduro","noun","solution/answer","Tawana mhinduro.")]),
    _vset("rhetoric_c2","C2","rhetoric","sn-c2-unit-1",[("gakava","noun","debate/argument","Gakava racho rakavakirwa pauchapupu."),("mhedziso","noun","conclusion","Mhedziso yakaziviswa."),("nyaya","noun","issue/point","Nyaya huru yakajeka.")]),
]


def _unit(level, n, title, grammar, vocab, checks):
    return CurriculumUnit(
        id=f"sn-{level.lower()}-unit-{n}", level=level, unit_number=n,
        title=title, grammar_points=[grammar], vocabulary_set_ids=[vocab],
        lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],
        competency_checklist=checks, default_weeks=1 if level in ("A1","A2") else 2,
    )


CURRICULUM = {
    "A1": [
        _unit("A1",1,"Greetings and introductions","sn-a1-g1","greetings_a1",["Greet someone naturally.","Introduce yourself."]),
        _unit("A1",2,"Identity","sn-a1-g2","identity_a1",["Identify yourself and others."]),
        _unit("A1",3,"Family","sn-a1-g3","family_a1",["Describe immediate family."]),
        _unit("A1",4,"Home and location","sn-a1-g7","home_a1",["Say where people and objects are."]),
        _unit("A1",5,"Daily routine","sn-a1-g3","routine_a1",["Describe a simple routine."]),
        _unit("A1",6,"Time","sn-a1-g5","time_a1",["Ask and answer basic time questions."]),
        _unit("A1",7,"Food and drink","sn-a1-g4","food_a1",["Order simple food and drink."]),
        _unit("A1",8,"Places","sn-a1-g8","places_a1",["Name common places and say where you go."]),
    ],
    "A2": [
        _unit("A2",1,"People and agreement","sn-a2-g1","people_a2",["Use noun-class agreement in descriptions."]),
        _unit("A2",2,"Travel and past events","sn-a2-g2","travel_a2",["Talk about past travel."]),
        _unit("A2",3,"Daily life and time","sn-a2-g8","daily_life_a2",["Describe routines and time references."]),
        _unit("A2",4,"Health","sn-a2-g3","health_a2",["Describe simple health needs."]),
        _unit("A2",5,"Objects and ownership","sn-a2-g4","identity_a1",["Use object and possessive marking."]),
        _unit("A2",6,"Descriptions and comparison","sn-a2-g6","people_a2",["Compare people and things."]),
        _unit("A2",7,"Requests and instructions","sn-a2-g7","places_a1",["Make polite requests."]),
        _unit("A2",8,"Future plans","sn-a2-g3","travel_a2",["Discuss future intentions."]),
    ],
    "B1": [
        _unit("B1",1,"Education","sn-b1-g1","education_b1",["Use relative clauses in explanations."]),
        _unit("B1",2,"Work and projects","sn-b1-g3","work_b1",["Discuss work and project activities."]),
        _unit("B1",3,"Society","sn-b1-g2","society_b1",["Explain conditions and consequences."]),
        _unit("B1",4,"Environment","sn-b1-g7","environment_b1",["Give reasons and purposes."]),
        _unit("B1",5,"Passive and causative","sn-b1-g4","work_b1",["Use passive and causative structures."]),
        _unit("B1",6,"Aspect and events","sn-b1-g6","daily_life_a2",["Distinguish ongoing and completed events."]),
        _unit("B1",7,"Reported speech","sn-b1-g8","communication_b2",["Report statements and questions."]),
        _unit("B1",8,"Integrated communication","sn-b1-g5","education_b1",["Give a connected explanation on a familiar topic."]),
    ],
    "B2": [
        _unit("B2",1,"Economy","sn-b2-g1","economy_b2",["Explain economic relationships."]),
        _unit("B2",2,"Governance","sn-b2-g4","governance_b2",["Discuss institutional processes precisely."]),
        _unit("B2",3,"Communication","sn-b2-g5","communication_b2",["Control topic and focus."]),
        _unit("B2",4,"Media","sn-b2-g6","media_b2",["Summarize information from media."]),
        _unit("B2",5,"Nominalization","sn-b2-g6","academic_c1",["Use formal noun-like formulations."]),
        _unit("B2",6,"Modality","sn-b2-g7","governance_b2",["Express certainty and obligation."]),
        _unit("B2",7,"Register","sn-b2-g8","professional_c1",["Adapt language to professional contexts."]),
        _unit("B2",8,"Complex discourse","sn-b2-g2","communication_b2",["Build a coherent multi-paragraph argument."]),
    ],
    "C1": [
        _unit("C1",1,"Formal institutions","sn-c1-g1","professional_c1",["Write formal institutional prose."]),
        _unit("C1",2,"Academic argumentation","sn-c1-g2","academic_c1",["Present claims and evidence."]),
        _unit("C1",3,"Academic hedging","sn-c1-g3","abstract_c1",["Qualify claims precisely."]),
        _unit("C1",4,"Embedded questions","sn-c1-g4","communication_b2",["Integrate questions into complex prose."]),
        _unit("C1",5,"Information structure","sn-c1-g5","rhetoric_c2",["Manage information flow."]),
        _unit("C1",6,"Media discourse","sn-c1-g6","media_b2",["Produce precise public-facing language."]),
        _unit("C1",7,"Pragmatics and idioms","sn-c1-g7","rhetoric_c2",["Interpret implied and idiomatic meaning."]),
        _unit("C1",8,"Professional correspondence","sn-c1-g8","professional_c1",["Draft precise professional requests."]),
    ],
    "C2": [
        _unit("C2",1,"Advanced cohesion","sn-c2-g1","rhetoric_c2",["Control long-range discourse cohesion."]),
        _unit("C2",2,"Nuanced modality","sn-c2-g2","abstract_c1",["Express subtle stance."]),
        _unit("C2",3,"Advanced nominalization","sn-c2-g3","academic_c1",["Handle dense academic formulations."]),
        _unit("C2",4,"Rhetorical organization","sn-c2-g4","rhetoric_c2",["Build and rebut complex arguments."]),
        _unit("C2",5,"Legal and administrative language","sn-c2-g5","professional_c1",["Interpret precise procedural wording."]),
        _unit("C2",6,"Translation precision","sn-c2-g6","rhetoric_c2",["Preserve register and pragmatic force."]),
        _unit("C2",7,"Literary style","sn-c2-g7","rhetoric_c2",["Interpret figurative and rhetorical language."]),
        _unit("C2",8,"Discourse and register shifting","sn-c2-g8","rhetoric_c2",["Shift deliberately among major registers."]),
    ],
}


PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id="sn-greetings-a1",level="A1",situation="greetings",icon="💬",phrases=[
        PhrasebookEntry(text="Mhoro.",context="Hello.",register="neutral"),
        PhrasebookEntry(text="Makadii?",context="How are you?",register="neutral"),
        PhrasebookEntry(text="Ndiripo, mazvita.",context="I am fine, thank you.",register="neutral"),
    ]),
    PhrasebookCategory(id="sn-thanks-a1",level="A1",situation="thanks",icon="🙏",phrases=[
        PhrasebookEntry(text="Ndatenda zvikuru.",context="Thank you very much.",register="neutral"),
        PhrasebookEntry(text="Hapana chakaipa.",context="No problem.",register="neutral"),
    ]),
    PhrasebookCategory(id="sn-introduction-a1",level="A1",situation="introductions",icon="👋",phrases=[
        PhrasebookEntry(text="Unonzi ani?",context="What is your name?",register="neutral"),
        PhrasebookEntry(text="Ndinonzi Tariro.",context="My name is Tariro.",register="neutral"),
    ]),
    PhrasebookCategory(id="sn-shopping-a1",level="A1",situation="shopping",icon="🛒",phrases=[
        PhrasebookEntry(text="Izvi zvinodhura zvakadii?",context="How much does this cost?",register="neutral"),
        PhrasebookEntry(text="Ndinoda izvi.",context="I want this.",register="neutral"),
    ]),
    PhrasebookCategory(id="sn-help-a1",level="A1",situation="help",icon="🆘",phrases=[
        PhrasebookEntry(text="Ndibatsirei, ndapota.",context="Please help me.",register="polite"),
        PhrasebookEntry(text="Handisi kunzwisisa.",context="I do not understand.",register="neutral"),
        PhrasebookEntry(text="Dzokororai, ndapota.",context="Please repeat.",register="polite"),
    ]),
    PhrasebookCategory(id="sn-travel-a2",level="A2",situation="travel",icon="🚌",phrases=[
        PhrasebookEntry(text="Ndiri kuenda kuHarare.",context="I am going to Harare.",register="neutral"),
        PhrasebookEntry(text="Bhazi rinosimuka nguvai?",context="What time does the bus leave?",register="neutral"),
    ]),
    PhrasebookCategory(id="sn-health-a2",level="A2",situation="health",icon="🩺",phrases=[
        PhrasebookEntry(text="Handisi kunzwa zvakanaka.",context="I do not feel well.",register="neutral"),
        PhrasebookEntry(text="Ndinoda kuona chiremba.",context="I need to see a doctor.",register="neutral"),
    ]),
    PhrasebookCategory(id="sn-study-b1",level="B1",situation="study",icon="📚",phrases=[
        PhrasebookEntry(text="Ndiri kudzidza chiShona.",context="I am studying Shona.",register="neutral"),
        PhrasebookEntry(text="Izvi zvinorevei?",context="What does this mean?",register="neutral"),
    ]),
    PhrasebookCategory(id="sn-work-b1",level="B1",situation="work",icon="💼",phrases=[
        PhrasebookEntry(text="Musangano uchaitwa riini?",context="When will the meeting take place?",register="neutral"),
        PhrasebookEntry(text="Chirongwa chapera.",context="The project is finished.",register="neutral"),
    ]),
    PhrasebookCategory(id="sn-professional-b2",level="B2",situation="professional",icon="🏢",phrases=[
        PhrasebookEntry(text="Munganditsanangurira zvakadzama here?",context="Could you explain in more detail?",register="polite"),
        PhrasebookEntry(text="Naizvozvo, tinokumbira nguva yakawedzerwa.",context="Therefore, we request additional time.",register="formal"),
    ]),
    PhrasebookCategory(id="sn-academic-c1",level="C1",situation="academic",icon="🎓",phrases=[
        PhrasebookEntry(text="Tsvakurudzo inoratidza kuti...",context="Research shows that...",register="formal"),
        PhrasebookEntry(text="Zvinogona kunge zviri izvo kuti...",context="It may be the case that...",register="formal"),
    ]),
    PhrasebookCategory(id="sn-formal-c1",level="C1",situation="formal correspondence",icon="✉️",phrases=[
        PhrasebookEntry(text="Tinokumbira kuti mutitumire...",context="We request that you send us...",register="formal"),
        PhrasebookEntry(text="Tinotenda nekubatana kwenyu.",context="We thank you for your cooperation.",register="formal"),
    ]),
    PhrasebookCategory(id="sn-debate-c2",level="C2",situation="discussion and debate",icon="🗣️",phrases=[
        PhrasebookEntry(text="Kunyange zvazvo izvi zviri zvechokwadi, nyaya huru ndeyekuti...",context="Although this is true, the main issue is...",register="formal"),
        PhrasebookEntry(text="Kune rimwe divi...",context="On the other hand...",register="formal"),
    ]),
]


ASSESSMENT_BANK = [
    AssessmentQuestion(id="sn-a1-001",skill="communication",difficulty="A1",question="Which Shona phrase means “Hello”?",options=["Mhoro.","Ndatenda.","Handisi kunzwisisa.","Hapana chakaipa."],correct="Mhoro."),
    AssessmentQuestion(id="sn-a1-002",skill="vocabulary",difficulty="A1",question="Which word means “water”?",options=["mvura","imba","amai","chikoro"],correct="mvura"),
    AssessmentQuestion(id="sn-a1-003",skill="grammar",difficulty="A1",question="Which sentence means “I am at home”?",options=["Ndiri kumba.","Ndinoenda kuchikoro.","Ndinonwa mvura.","Iri ibhuku."],correct="Ndiri kumba."),
    AssessmentQuestion(id="sn-a1-004",skill="vocabulary",difficulty="A1",question="What does amai mean?",options=["mother","father","friend","teacher"],correct="mother"),
    AssessmentQuestion(id="sn-a1-005",skill="grammar",difficulty="A1",question="Which question asks “What is your name?”",options=["Unonzi ani?","Uri kupi?","Ichi chii?","Inguvai?"],correct="Unonzi ani?"),
    AssessmentQuestion(id="sn-a2-001",skill="grammar",difficulty="A2",question="Which sentence expresses future action?",options=["Ndichaenda mangwana.","Ndakaenda nezuro.","Ndiri kumba.","Ndinodzidza."],correct="Ndichaenda mangwana."),
    AssessmentQuestion(id="sn-a2-002",skill="communication",difficulty="A2",question="Which is a polite request?",options=["Ndibatsirei, ndapota.","Mhoro.","Ndinoda mvura.","Ndiri pano."],correct="Ndibatsirei, ndapota."),
    AssessmentQuestion(id="sn-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["Kana ukadzidza, uchapasa.","Mhoro.","Ndiri kumba.","Ndinoda mvura."],correct="Kana ukadzidza, uchapasa."),
    AssessmentQuestion(id="sn-b1-002",skill="grammar",difficulty="B1",question="Which example is passive?",options=["Bhuku rakaverengwa nemudzidzi.","Ndinodzidza zuva nezuva.","Ndiri kuenda.","Ndinoda mvura."],correct="Bhuku rakaverengwa nemudzidzi."),
    AssessmentQuestion(id="sn-b2-001",skill="discourse",difficulty="B2",question="Which phrase marks a consequence?",options=["Naizvozvo","Mhoro","Unonzi ani?","Ndinonzi Tariro."],correct="Naizvozvo"),
    AssessmentQuestion(id="sn-c1-001",skill="academic",difficulty="C1",question="Which phrase appropriately hedges an academic claim?",options=["Zvinogona kunge zviri izvo kuti...","Zviri pachena chete.","Mhoro.","Mpa izvi."],correct="Zvinogona kunge zviri izvo kuti..."),
    AssessmentQuestion(id="sn-c2-001",skill="translation",difficulty="C2",question="Advanced translation should preserve what besides literal meaning?",options=["Register and pragmatic force","Only word order","Only punctuation","Only word length"],correct="Register and pragmatic force"),
]

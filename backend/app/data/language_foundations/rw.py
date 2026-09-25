"""Kinyarwanda foundation data for JUBA LISAN.

The module intentionally keeps Kinyarwanda-specific structures, vocabulary and
native examples so generated lessons are grounded in the target language.
"""
from app.data._types import (
    AssessmentQuestion,
    CurriculumUnit,
    GrammarExample,
    GrammarTopic,
    PhrasebookCategory,
    PhrasebookEntry,
    VocabularyEntry,
    VocabularySet,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def _g(slug, title, level, summary, examples):
    return GrammarTopic(
        slug=slug, title=title, level=level, category="grammar",
        summary=summary, explanation=summary,
        examples=[GrammarExample(text=e) for e in examples],
    )


GRAMMAR_TOPICS = [
    _g("rw-a1-g1", "Personal pronouns and subject marking", "A1", "Use personal pronouns and basic subject forms.", ["Jye ndi umunyeshuri.", "We uri umwarimu."]),
    _g("rw-a1-g2", "Copulative identity", "A1", "Identify people and things with ni.", ["Uyu ni umwarimu.", "Ari umunyeshuri."]),
    _g("rw-a1-g3", "Present tense", "A1", "Describe habitual and current actions.", ["Ndiga buri munsi.", "Arakora."]),
    _g("rw-a1-g4", "Negation", "A1", "Negate simple verbal and nominal clauses.", ["Sinsoma.", "Si umunyeshuri."]),
    _g("rw-a1-g5", "Questions", "A1", "Ask basic yes-no and information questions.", ["Uri he?", "Witwa nde?"]),
    _g("rw-a1-g6", "Possessive constructions", "A1", "Express possession with agreeing possessives.", ["Igitabo cyanjye.", "Inzu yacu."]),
    _g("rw-a1-g7", "Locative prepositions", "A1", "Express location with mu, ku and related forms.", ["Ndi mu rugo.", "Ari ku ishuri."]),
    _g("rw-a1-g8", "Noun classes and plurals", "A1", "Recognize common noun-class pairs and agreement.", ["umuntu / abantu", "igitabo / ibitabo"]),
    _g("rw-a2-g1", "Noun-class agreement", "A2", "Match adjectives and verbs with noun-class agreement.", ["Umwana muto arakina.", "Abana bato barakina."]),
    _g("rw-a2-g2", "Past tense", "A2", "Talk about completed and recent events.", ["Nagiye ku ishuri ejo.", "Yabonye inshuti ye."]),
    _g("rw-a2-g3", "Future and intention", "A2", "Express future plans and intentions.", ["Nziga ejo.", "Tuzajya i Kigali."]),
    _g("rw-a2-g4", "Object marking", "A2", "Use object markers in simple transitive clauses.", ["Ndakubona.", "Ndakunda ururimi."]),
    _g("rw-a2-g5", "Adjectives and agreement", "A2", "Describe people and objects with agreement.", ["Umuntu mwiza.", "Ibintu byiza."]),
    _g("rw-a2-g6", "Comparatives", "A2", "Compare people, objects and quantities.", ["Uyu aruta undi.", "Iyi ni nziza kurusha iyo."]),
    _g("rw-a2-g7", "Imperatives and polite requests", "A2", "Give instructions and make respectful requests.", ["Ngwino hano.", "Mwicare, ndakwinginze."]),
    _g("rw-a2-g8", "Time and frequency", "A2", "Place actions in time and describe frequency.", ["Niga buri munsi.", "Yaje ejo hashize."]),
    _g("rw-b1-g1", "Relative clauses", "B1", "Link noun phrases to relative clauses.", ["Umuntu waje ni data.", "Igitabo nasomye ni gishya."]),
    _g("rw-b1-g2", "Conditional clauses", "B1", "Express conditions and consequences.", ["Niba wiga, uzatsinda.", "Iyo imvura iguye, turaguma mu rugo."]),
    _g("rw-b1-g3", "Infinitive and verbal nouns", "B1", "Use ku- infinitives to discuss activities and purposes.", ["Nkunda kwiga.", "Yagiye kugura ibiryo."]),
    _g("rw-b1-g4", "Causative constructions", "B1", "Express causing another action.", ["Umwarimu yigisha abanyeshuri.", "Yatumye dukora."]),
    _g("rw-b1-g5", "Passive voice", "B1", "Form passive clauses and foreground affected participants.", ["Igitabo cyasomwe n'umunyeshuri.", "Inzu yarubatswe."]),
    _g("rw-b1-g6", "Aspect and event structure", "B1", "Distinguish ongoing, habitual and completed events.", ["Arimo kwiga.", "Yarangije gukora."]),
    _g("rw-b1-g7", "Purpose and cause", "B1", "Connect clauses using purpose and causal relations.", ["Naje kwiga.", "Yatinze kubera imvura."]),
    _g("rw-b1-g8", "Reported speech", "B1", "Report statements, questions and instructions.", ["Yavuze ko aza.", "Yambajije niba nzagenda."]),
    _g("rw-b2-g1", "Complex subordination", "B2", "Build multi-clause sentences with precise relations.", ["Nubwo yari ananiwe, yakomeje gukora."]),
    _g("rw-b2-g2", "Concession and contrast", "B2", "Express concession, contrast and qualification.", ["Nubwo bigoye, tuzakomeza."]),
    _g("rw-b2-g3", "Relative reference and cohesion", "B2", "Maintain reference across extended discourse.", ["Umushinga twavuzeho warangiye."]),
    _g("rw-b2-g4", "Discourse connectors", "B2", "Organize arguments with causal, contrastive and sequential markers.", ["Kubera iyo mpamvu, tugomba gutegura neza."]),
    _g("rw-b2-g5", "Focus and information structure", "B2", "Highlight new, given and contrastive information.", ["Icyo nshaka ni amahoro.", "Uyu munsi ni bwo twatangiye."]),
    _g("rw-b2-g6", "Nominalization", "B2", "Turn events and properties into noun-like expressions.", ["Kwiga ururimi bisaba igihe."]),
    _g("rw-b2-g7", "Modality and evidential stance", "B2", "Express obligation, possibility, certainty and reported evidence.", ["Birashoboka ko azaza.", "Agomba kubikora."]),
    _g("rw-b2-g8", "Register and politeness", "B2", "Adapt wording to social and professional contexts.", ["Mwambwira aho ibiro biherereye, ndakwinginze?"]),
    _g("rw-c1-g1", "Formal and institutional Kinyarwanda", "C1", "Handle formal administrative and institutional language.", ["Inama izaterana ku wa mbere kugira ngo hasuzumwe gahunda nshya."]),
    _g("rw-c1-g2", "Academic argumentation", "C1", "Present claims, evidence, qualifications and conclusions.", ["Ubushakashatsi bwerekana ko uburezi bugira uruhare runini mu iterambere."]),
    _g("rw-c1-g3", "Academic hedging", "C1", "Qualify claims without weakening logical precision.", ["Birashoboka ko ibisubizo byaterwa n'imiterere y'itsinda."]),
    _g("rw-c1-g4", "Embedded questions", "C1", "Integrate questions into complex sentences.", ["Ndashaka kumenya niba umushinga warangiye."]),
    _g("rw-c1-g5", "Information packaging", "C1", "Use topic, focus and clause structure for coherent prose.", ["Ikibazo cy'ingenzi ni uburyo twakongera ireme rya serivisi."]),
    _g("rw-c1-g6", "Media and public discourse", "C1", "Interpret and produce precise public-facing language.", ["Raporo nshya yasohotse uyu munsi."]),
    _g("rw-c1-g7", "Idiomatic and pragmatic meaning", "C1", "Interpret idioms, implication and culturally appropriate wording.", ["Gushyira hamwe ni byo bituma akazi kagenda neza."]),
    _g("rw-c1-g8", "Professional correspondence", "C1", "Write concise professional requests and responses.", ["Turabasaba ko mwatwoherereza inyandiko zikenewe mbere y'itariki ntarengwa."]),
    _g("rw-c2-g1", "Advanced discourse cohesion", "C2", "Control long-range reference, cohesion and rhetorical progression.", ["Nubwo raporo igaragaza intambwe imaze guterwa, irerekana kandi imbogamizi zisaba ibisubizo birambye."]),
    _g("rw-c2-g2", "Nuanced modality", "C2", "Express subtle degrees of certainty, obligation and evaluation.", ["Ntibyaba ari ugukabya kuvuga ko iyi gahunda ishobora kugira ingaruka zirambye."]),
    _g("rw-c2-g3", "Complex nominalization", "C2", "Compress complex propositions for academic and institutional prose.", ["Isesengura ry'ibyavuye mu bushakashatsi ryatumye hafatwa umwanzuro mushya."]),
    _g("rw-c2-g4", "Rhetorical organization", "C2", "Control emphasis, concession and counterargument.", ["Nubwo iki gisubizo gifite ibyiza, ikibazo nyamukuru gisigaye ni ugushyira mu bikorwa."]),
    _g("rw-c2-g5", "Legal and administrative formulation", "C2", "Interpret precise obligations, conditions and procedural language.", ["Uwasabye serivisi agomba gutanga inyandiko zose zisabwa hakurikijwe amabwiriza."]),
    _g("rw-c2-g6", "Translation precision", "C2", "Preserve meaning, register and pragmatic force across languages.", ["Ubusobanuro bugomba kubahiriza igisobanuro n'imvugo y'inkomoko."]),
    _g("rw-c2-g7", "Literary and rhetorical style", "C2", "Interpret figurative language and deliberate stylistic choices.", ["Imvugo y'umwanditsi yubaka ishusho y'ubuzima bw'abaturage."]),
    _g("rw-c2-g8", "Discourse analysis and register shifting", "C2", "Move deliberately between conversational, professional and academic styles.", ["Imvugo ikoreshwa mu biganiro bya buri munsi itandukanye n'imvugo y'inyandiko y'ubushakashatsi."]),
]


def _vset(id_, level, topic, unit_ref, entries):
    return VocabularySet(
        id=id_, level=level, topic=topic, unit_ref=unit_ref,
        words=[VocabularyEntry(word=w, pos=p, definition=d, example=e) for w, p, d, e in entries],
    )


VOCABULARY_SETS = [
    _vset("greetings_a1","A1","greetings","rw-a1-unit-1",[("muraho","phrase","hello","Muraho neza."),("murakoze","phrase","thank you","Murakoze cyane."),("amakuru","noun","news/how are you","Amakuru yawe?")]),
    _vset("identity_a1","A1","identity","rw-a1-unit-2",[("izina","noun","name","Izina ryanjye ni Aline."),("umunyeshuri","noun","student","Ndi umunyeshuri."),("umwarimu","noun","teacher","Uyu ni umwarimu.")]),
    _vset("family_a1","A1","family","rw-a1-unit-3",[("mama","noun","mother","Mama ari mu rugo."),("data","noun","father","Data arakora."),("umuryango","noun","family","Umuryango wanjye ni munini.")]),
    _vset("home_a1","A1","home","rw-a1-unit-4",[("inzu","noun","house","Inzu yacu ni nziza."),("urugi","noun","door","Funga urugi."),("ameza","noun","table","Igitabo kiri ku meza.")]),
    _vset("routine_a1","A1","routine","rw-a1-unit-5",[("kwiga","verb","to study","Ndiga buri munsi."),("gukora","verb","to work","Nkora mu gitondo."),("kuryama","verb","to sleep","Nryama nijoro.")]),
    _vset("time_a1","A1","time","rw-a1-unit-6",[("igihe","noun","time","Ni iki gihe?"),("uyu munsi","phrase","today","Uyu munsi ndiga."),("ejo","noun","tomorrow/yesterday","Nzagaruka ejo.")]),
    _vset("food_a1","A1","food","rw-a1-unit-7",[("amazi","noun","water","Ndashaka amazi."),("ibiryo","noun","food","Ibiryo birashyushye."),("amata","noun","milk","Nanywa amata.")]),
    _vset("places_a1","A1","places","rw-a1-unit-8",[("ishuri","noun","school","Ndi ku ishuri."),("isoko","noun","market","Ajya ku isoko."),("ibiro","noun","office","Ari mu biro.")]),
    _vset("people_a2","A2","people and descriptions","rw-a2-unit-1",[("umuntu","noun","person","Ni umuntu mwiza."),("umwana","noun","child","Umwana arakina."),("abantu","noun","people","Abantu baraza.")]),
    _vset("travel_a2","A2","travel","rw-a2-unit-2",[("urugendo","noun","journey","Urugendo rwatangiye."),("kujya","verb","to go","Ngiye i Kigali."),("kugaruka","verb","to return","Nzagaruka ejo.")]),
    _vset("daily_life_a2","A2","daily life","rw-a2-unit-3",[("gitondo","noun","morning","Mu gitondo ndakora."),("nimugoroba","noun","evening","Nimugoroba turaganira."),("buri munsi","phrase","every day","Niga buri munsi.")]),
    _vset("health_a2","A2","health","rw-a2-unit-4",[("ubuzima","noun","health/life","Ubuzima ni ingenzi."),("muganga","noun","doctor","Muganga araza."),("ububabare","noun","pain","Mfite ububabare.")]),
    _vset("education_b1","B1","education","rw-b1-unit-1",[("uburezi","noun","education","Uburezi ni ingenzi."),("ubushakashatsi","noun","research","Ubushakashatsi burakomeza."),("ubumenyi","noun","knowledge","Ubumenyi buriyongera.")]),
    _vset("work_b1","B1","work","rw-b1-unit-2",[("akazi","noun","work/job","Mfite akazi."),("umushinga","noun","project","Umushinga warangiye."),("inama","noun","meeting/advice","Inama izaba ejo.")]),
    _vset("society_b1","B1","society","rw-b1-unit-3",[("iterambere","noun","development","Iterambere rirakomeza."),("ubufatanye","noun","cooperation","Ubufatanye ni ingenzi."),("serivisi","noun","service","Serivisi nziza irakenewe.")]),
    _vset("environment_b1","B1","environment","rw-b1-unit-4",[("ibidukikije","noun","environment","Tugomba kurinda ibidukikije."),("amazi","noun","water","Amazi meza ni ingenzi."),("ishyamba","noun","forest","Ishyamba ririnzwe.")]),
    _vset("economy_b2","B2","economy","rw-b2-unit-1",[("ubukungu","noun","economy","Ubukungu burakura."),("ishoramari","noun","investment","Ishoramari ririyongera."),("isoko","noun","market","Isoko rirahinduka.")]),
    _vset("governance_b2","B2","governance","rw-b2-unit-2",[("ubuyobozi","noun","leadership/government","Ubuyobozi bushya bwatangijwe."),("amategeko","noun","laws","Amategeko agomba kubahirizwa."),("politiki","noun","policy/politics","Politiki nshya yatangajwe.")]),
    _vset("communication_b2","B2","communication","rw-b2-unit-3",[("amakuru","noun","information/news","Amakuru mashya yatangajwe."),("itumanaho","noun","communication","Itumanaho ririhuta."),("ubutumwa","noun","message","Ubutumwa bwageze.")]),
    _vset("media_b2","B2","media","rw-b2-unit-4",[("itangazamakuru","noun","media","Itangazamakuru ryatangaje amakuru."),("raporo","noun","report","Raporo yasohotse."),("ikiganiro","noun","discussion/interview","Ikiganiro kirakomeje.")]),
    _vset("academic_c1","C1","academic language","rw-c1-unit-1",[("igitekerezo","noun","idea","Igitekerezo kigomba gusobanurwa."),("ikimenyetso","noun","evidence/sign","Dukeneye ikimenyetso gifatika."),("isesengura","noun","analysis","Isesengura rirakomeza.")]),
    _vset("professional_c1","C1","professional language","rw-c1-unit-2",[("inyandiko","noun","document","Ohereza inyandiko."),("amabwiriza","noun","instructions/regulations","Amabwiriza agomba gukurikizwa."),("inshingano","noun","responsibility","Inshingano ye ni ukugenzura.")]),
    _vset("abstract_c1","C1","abstract concepts","rw-c1-unit-3",[("ingaruka","noun","effect/consequence","Ibyemezo bigira ingaruka."),("intego","noun","objective","Intego ni ukuzamura ireme."),("igisubizo","noun","solution/answer","Twabonye igisubizo.")]),
    _vset("rhetoric_c2","C2","rhetoric","rw-c2-unit-1",[("impaka","noun","debate","Impaka zishingiye ku bimenyetso."),("umwanzuro","noun","conclusion","Umwanzuro watangajwe."),("ingingo","noun","point/issue","Ingingo nyamukuru irasobanutse.")]),
    _vset("discourse_c2","C2","discourse analysis","rw-c2-unit-2",[("imvugo","noun","speech/expression","Imvugo igomba guhuza n'abayumva."),("igisobanuro","noun","meaning/explanation","Igisobanuro kirumvikana."),("umwimerere","noun","originality/original form","Umwimerere w'inyandiko wararinzwe.")]),
]


def _unit(level, n, title, grammar, vocab, checks):
    return CurriculumUnit(
        id=f"rw-{level.lower()}-unit-{n}", level=level, unit_number=n,
        title=title, grammar_points=[grammar], vocabulary_set_ids=[vocab],
        lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],
        competency_checklist=checks, default_weeks=1 if level in ("A1","A2") else 2,
    )


CURRICULUM = {
    "A1": [
        _unit("A1",1,"Greetings and introductions","rw-a1-g1","greetings_a1",["Greet someone naturally.","Introduce yourself."]),
        _unit("A1",2,"Identity and the copula","rw-a1-g2","identity_a1",["Identify people and roles."]),
        _unit("A1",3,"Family","rw-a1-g3","family_a1",["Describe immediate family."]),
        _unit("A1",4,"Home and location","rw-a1-g7","home_a1",["Say where objects and people are."]),
        _unit("A1",5,"Daily routine","rw-a1-g3","routine_a1",["Describe a simple routine."]),
        _unit("A1",6,"Time","rw-a1-g5","time_a1",["Ask and answer basic time questions."]),
        _unit("A1",7,"Food and drink","rw-a1-g4","food_a1",["Order simple food and drink."]),
        _unit("A1",8,"Places","rw-a1-g8","places_a1",["Name common places and say where you go."]),
    ],
    "A2": [
        _unit("A2",1,"People and agreement","rw-a2-g1","people_a2",["Use noun-class agreement in descriptions."]),
        _unit("A2",2,"Travel and movement","rw-a2-g2","travel_a2",["Talk about past and future travel."]),
        _unit("A2",3,"Daily life and time","rw-a2-g8","daily_life_a2",["Describe routines and time references."]),
        _unit("A2",4,"Health","rw-a2-g3","health_a2",["Describe simple health needs."]),
        _unit("A2",5,"Objects and ownership","rw-a2-g4","identity_a1",["Use object and possessive marking."]),
        _unit("A2",6,"Descriptions and comparison","rw-a2-g6","people_a2",["Compare people and things."]),
        _unit("A2",7,"Requests and instructions","rw-a2-g7","places_a1",["Make polite requests."]),
        _unit("A2",8,"Review and practical conversation","rw-a2-g8","daily_life_a2",["Sustain a short everyday exchange."]),
    ],
    "B1": [
        _unit("B1",1,"Education and study","rw-b1-g1","education_b1",["Use relative clauses to describe academic topics."]),
        _unit("B1",2,"Work and projects","rw-b1-g3","work_b1",["Discuss work and project activities."]),
        _unit("B1",3,"Society","rw-b1-g2","society_b1",["Explain conditions and consequences."]),
        _unit("B1",4,"Environment","rw-b1-g7","environment_b1",["Give reasons and purposes."]),
        _unit("B1",5,"Passive and causative","rw-b1-g4","work_b1",["Describe actions with passive and causative structures."]),
        _unit("B1",6,"Aspect and events","rw-b1-g6","daily_life_a2",["Distinguish ongoing and completed events."]),
        _unit("B1",7,"Reported speech","rw-b1-g8","communication_b2",["Report statements and questions."]),
        _unit("B1",8,"Integrated communication","rw-b1-g5","education_b1",["Give a connected explanation on a familiar topic."]),
    ],
    "B2": [
        _unit("B2",1,"Economy","rw-b2-g1","economy_b2",["Explain complex economic relationships."]),
        _unit("B2",2,"Governance","rw-b2-g4","governance_b2",["Discuss institutional processes precisely."]),
        _unit("B2",3,"Communication","rw-b2-g5","communication_b2",["Control topic and focus in extended speech."]),
        _unit("B2",4,"Media","rw-b2-g6","media_b2",["Summarize and connect information from media."]),
        _unit("B2",5,"Nominalization","rw-b2-g6","academic_c1",["Compress propositions into formal noun phrases."]),
        _unit("B2",6,"Modality","rw-b2-g7","governance_b2",["Express degrees of certainty and obligation."]),
        _unit("B2",7,"Register","rw-b2-g8","professional_c1",["Adapt language to professional contexts."]),
        _unit("B2",8,"Complex discourse","rw-b2-g2","communication_b2",["Build a coherent multi-paragraph argument."]),
    ],
    "C1": [
        _unit("C1",1,"Formal institutions","rw-c1-g1","professional_c1",["Write formal institutional prose."]),
        _unit("C1",2,"Academic argumentation","rw-c1-g2","academic_c1",["Present claims and evidence coherently."]),
        _unit("C1",3,"Academic hedging","rw-c1-g3","abstract_c1",["Qualify claims precisely."]),
        _unit("C1",4,"Embedded questions","rw-c1-g4","communication_b2",["Integrate questions into complex prose."]),
        _unit("C1",5,"Information structure","rw-c1-g5","discourse_c2",["Manage information flow in long texts."]),
        _unit("C1",6,"Media discourse","rw-c1-g6","media_b2",["Produce precise public-facing language."]),
        _unit("C1",7,"Pragmatics and idioms","rw-c1-g7","rhetoric_c2",["Interpret implied and idiomatic meaning."]),
        _unit("C1",8,"Professional correspondence","rw-c1-g8","professional_c1",["Draft precise professional requests."]),
    ],
    "C2": [
        _unit("C2",1,"Cohesion","rw-c2-g1","discourse_c2",["Control long-range discourse cohesion."]),
        _unit("C2",2,"Nuanced modality","rw-c2-g2","abstract_c1",["Express subtle epistemic and deontic stance."]),
        _unit("C2",3,"Advanced nominalization","rw-c2-g3","academic_c1",["Handle dense academic formulations."]),
        _unit("C2",4,"Rhetorical organization","rw-c2-g4","rhetoric_c2",["Build and rebut complex arguments."]),
        _unit("C2",5,"Legal and administrative language","rw-c2-g5","professional_c1",["Interpret precise procedural wording."]),
        _unit("C2",6,"Translation precision","rw-c2-g6","discourse_c2",["Preserve register and pragmatic force in translation."]),
        _unit("C2",7,"Literary style","rw-c2-g7","rhetoric_c2",["Interpret figurative and rhetorical language."]),
        _unit("C2",8,"Discourse and register shifting","rw-c2-g8","discourse_c2",["Shift deliberately among major registers."]),
    ],
}


PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id="rw-greetings-a1",level="A1",situation="greetings",icon="💬",phrases=[
        PhrasebookEntry(text="Muraho.",context="Hello.",register="neutral"),
        PhrasebookEntry(text="Amakuru?",context="How are you?",register="neutral"),
        PhrasebookEntry(text="Ni meza, murakoze.",context="Fine, thank you.",register="neutral"),
    ]),
    PhrasebookCategory(id="rw-thanks-a1",level="A1",situation="thanks",icon="🙏",phrases=[
        PhrasebookEntry(text="Murakoze cyane.",context="Thank you very much.",register="neutral"),
        PhrasebookEntry(text="Nta kibazo.",context="No problem.",register="neutral"),
    ]),
    PhrasebookCategory(id="rw-introduction-a1",level="A1",situation="introductions",icon="👋",phrases=[
        PhrasebookEntry(text="Witwa nde?",context="What is your name?",register="neutral"),
        PhrasebookEntry(text="Nitwa Aline.",context="My name is Aline.",register="neutral"),
    ]),
    PhrasebookCategory(id="rw-shopping-a1",level="A1",situation="shopping",icon="🛒",phrases=[
        PhrasebookEntry(text="Ibi ni angahe?",context="How much is this?",register="neutral"),
        PhrasebookEntry(text="Ndashaka ibi.",context="I want this.",register="neutral"),
        PhrasebookEntry(text="Mpa ibi, ndakwinginze.",context="Please give me this.",register="polite"),
    ]),
    PhrasebookCategory(id="rw-help-a1",level="A1",situation="help",icon="🆘",phrases=[
        PhrasebookEntry(text="Mwamfasha, ndakwinginze?",context="Could you help me, please?",register="polite"),
        PhrasebookEntry(text="Sinumva.",context="I do not understand.",register="neutral"),
        PhrasebookEntry(text="Subiramo, ndakwinginze.",context="Please say it again.",register="polite"),
    ]),
    PhrasebookCategory(id="rw-travel-a2",level="A2",situation="travel",icon="🚌",phrases=[
        PhrasebookEntry(text="Ngiye i Kigali.",context="I am going to Kigali.",register="neutral"),
        PhrasebookEntry(text="Nagaruka ryari?",context="When will I return?",register="neutral"),
    ]),
    PhrasebookCategory(id="rw-health-a2",level="A2",situation="health",icon="🩺",phrases=[
        PhrasebookEntry(text="Ndumva ntameze neza.",context="I do not feel well.",register="neutral"),
        PhrasebookEntry(text="Nkeneye umuganga.",context="I need a doctor.",register="neutral"),
    ]),
    PhrasebookCategory(id="rw-study-b1",level="B1",situation="study",icon="📚",phrases=[
        PhrasebookEntry(text="Ndimo kwiga Kinyarwanda.",context="I am studying Kinyarwanda.",register="neutral"),
        PhrasebookEntry(text="Ibi bisobanura iki?",context="What does this mean?",register="neutral"),
    ]),
    PhrasebookCategory(id="rw-work-b1",level="B1",situation="work",icon="💼",phrases=[
        PhrasebookEntry(text="Inama izaba ryari?",context="When will the meeting be?",register="neutral"),
        PhrasebookEntry(text="Umushinga warangiye.",context="The project is finished.",register="neutral"),
    ]),
    PhrasebookCategory(id="rw-professional-b2",level="B2",situation="professional",icon="🏢",phrases=[
        PhrasebookEntry(text="Mwambwira ibisobanuro birambuye?",context="Could you give me more details?",register="polite"),
        PhrasebookEntry(text="Kubera iyo mpamvu, turasaba ko twongera igihe.",context="For that reason, we request more time.",register="formal"),
    ]),
    PhrasebookCategory(id="rw-academic-c1",level="C1",situation="academic",icon="🎓",phrases=[
        PhrasebookEntry(text="Ubushakashatsi bwerekana ko...",context="The research shows that...",register="formal"),
        PhrasebookEntry(text="Birashoboka ko...",context="It is possible that...",register="formal"),
    ]),
    PhrasebookCategory(id="rw-formal-c1",level="C1",situation="formal correspondence",icon="✉️",phrases=[
        PhrasebookEntry(text="Turabasaba ko mwatwoherereza...",context="We request that you send us...",register="formal"),
        PhrasebookEntry(text="Tubashimiye ubufatanye bwanyu.",context="We thank you for your cooperation.",register="formal"),
    ]),
    PhrasebookCategory(id="rw-discussion-c2",level="C2",situation="discussion and debate",icon="🗣️",phrases=[
        PhrasebookEntry(text="Nubwo ibyo ari ukuri, ikibazo nyamukuru ni...",context="Although that is true, the main issue is...",register="formal"),
        PhrasebookEntry(text="Ku rundi ruhande...",context="On the other hand...",register="formal"),
    ]),
]


ASSESSMENT_BANK = [
    AssessmentQuestion(id="rw-a1-001",skill="communication",difficulty="A1",question="Which Kinyarwanda phrase means “Hello”?",options=["Muraho.","Murakoze.","Sinumva.","Nta kibazo."],correct="Muraho."),
    AssessmentQuestion(id="rw-a1-002",skill="communication",difficulty="A1",question="Which phrase asks “How are you?”",options=["Amakuru?","Murakoze.","Ndashaka ibi.","Subiramo."],correct="Amakuru?"),
    AssessmentQuestion(id="rw-a1-003",skill="vocabulary",difficulty="A1",question="Which word means “name”?",options=["izina","inzu","ishuri","amazi"],correct="izina"),
    AssessmentQuestion(id="rw-a1-004",skill="grammar",difficulty="A1",question="Complete: “I am at home” — “Ndi ___ rugo.”",options=["mu","ku","na","kuri"],correct="mu"),
    AssessmentQuestion(id="rw-a2-001",skill="grammar",difficulty="A2",question="Which pair shows a common singular/plural noun-class contrast?",options=["umuntu / abantu","izina / amazi","inzu / ishuri","mama / data"],correct="umuntu / abantu"),
    AssessmentQuestion(id="rw-a2-002",skill="communication",difficulty="A2",question="Which phrase is a polite request?",options=["Mwicara, ndakwinginze.","Muraho.","Ngiye i Kigali.","Amakuru?"],"correct":"Mwicara, ndakwinginze."),
    AssessmentQuestion(id="rw-b1-001",skill="grammar",difficulty="B1",question="Which construction introduces a condition?",options=["Niba wiga, uzatsinda.","Muraho neza.","Ndashaka amazi.","Ndi mu rugo."],"correct":"Niba wiga, uzatsinda."),
    AssessmentQuestion(id="rw-b1-002",skill="grammar",difficulty="B1",question="Which example is passive?",options=["Igitabo cyasomwe n'umunyeshuri.","Ndiga buri munsi.","Ngiye ku ishuri.","Ndashaka amazi."],"correct":"Igitabo cyasomwe n'umunyeshuri."),
    AssessmentQuestion(id="rw-b2-001",skill="discourse",difficulty="B2",question="Which phrase explicitly marks a consequence?",options=["Kubera iyo mpamvu","Muraho","Amakuru?","Nitwa Aline."],"correct":"Kubera iyo mpamvu"),
    AssessmentQuestion(id="rw-b2-002",skill="register",difficulty="B2",question="Which phrase is appropriate for a formal request?",options=["Turabasaba ko mwatwoherereza...","Mpa ibi.","Muraho.","Amakuru?"],"correct":"Turabasaba ko mwatwoherereza..."),
    AssessmentQuestion(id="rw-c1-001",skill="academic",difficulty="C1",question="Which phrase appropriately hedges an academic claim?",options=["Birashoboka ko...","Ni byo rwose gusa.","Muraho.","Mpa ibi."],"correct":"Birashoboka ko..."),
    AssessmentQuestion(id="rw-c1-002",skill="professional",difficulty="C1",question="Which sentence is a formal institutional request?",options=["Turabasaba ko mwatwoherereza inyandiko zikenewe.","Ndi mu rugo.","Ndashaka amazi.","Amakuru?"],"correct":"Turabasaba ko mwatwoherereza inyandiko zikenewe."),
    AssessmentQuestion(id="rw-c2-001",skill="discourse",difficulty="C2",question="Which phrase introduces a counterargument?",options=["Nubwo ibyo ari ukuri, ikibazo nyamukuru ni...","Muraho.","Ni meza.","Nitwa Aline."],"correct":"Nubwo ibyo ari ukuri, ikibazo nyamukuru ni..."),
    AssessmentQuestion(id="rw-c2-002",skill="translation",difficulty="C2",question="In advanced translation, what should be preserved besides literal meaning?",options=["Register and pragmatic force","Only word order","Only punctuation","Only word length"],correct="Register and pragmatic force"),
]

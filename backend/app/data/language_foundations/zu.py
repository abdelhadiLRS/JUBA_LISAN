"""Zulu foundation data for JUBA LISAN — A1 to C2."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

_TOPICS = [
("noun-classes", "Noun classes and agreement", "A1", "morphology", "Recognize core noun classes and concordial agreement.", "Umfana omncane ufunda incwadi."),
("subject-concords", "Subject concords", "A1", "verbs", "Build affirmative clauses with subject concords.", "Ngiyafunda isiZulu."),
("copulative", "Copulative constructions", "A1", "syntax", "Identify people and things with copulative patterns.", "Ngingumfundi."),
("present-progressive", "Present and progressive forms", "A1", "verbs", "Describe current and habitual activities.", "Ngifunda nsuku zonke."),
("negation", "Verb and copulative negation", "A1", "verbs", "Form common negative statements.", "Angiqondi."),
("questions", "Questions and question words", "A1", "communication", "Ask who, what, where, when and yes/no questions.", "Uhlala kuphi?"),
("possessives", "Possessive concords", "A1", "noun-phrase", "Express ownership and relationships using possessive concords.", "Le yindlu yami."),
("locatives", "Location and direction", "A1", "locative", "Describe location, movement and destinations.", "Ngisekhaya."),
("plural-classes", "Plural noun-class alternations", "A2", "morphology", "Use singular/plural class pairs in connected speech.", "Abafundi bafunda izincwadi."),
("object-concords", "Object concords", "A2", "verbs", "Mark affected objects with appropriate object concords.", "Ngiyayibona indlu."),
("past", "Past tense", "A2", "verbs", "Narrate completed actions and recent events.", "Izolo ngaya emakethe."),
("future", "Future tense", "A2", "verbs", "Talk about plans, intentions and predictions.", "Kusasa ngizoya emsebenzini."),
("imperative", "Imperatives and polite requests", "A2", "communication", "Give instructions and soften requests with polite forms.", "Ngicela uhlale lapha."),
("comparatives", "Comparatives and superlatives", "A2", "adjectives", "Compare people, objects and situations.", "Le ndawo inkulu kunaleya."),
("modalities", "Ability, necessity and desire", "A2", "modality", "Express ability, obligation, possibility and desire.", "Ngifuna ukufunda isiZulu."),
("relative", "Relative clauses", "B1", "syntax", "Modify nouns with relative constructions.", "Umuntu engimbone izolo ungumngane wami."),
("subjunctive", "Subjunctive and dependent verb forms", "B1", "verbs", "Express purpose, recommendation and dependent actions.", "Kubalulekile ukuthi ufunde."),
("conditional", "Conditional constructions", "B1", "syntax", "Express real and hypothetical conditions.", "Uma isikhathi sikhona, sizohamba."),
("reported-speech", "Reported speech", "B1", "discourse", "Report statements, questions and intentions.", "Uthe uzofika kusasa."),
("causal-concessive", "Cause, result and concession", "B1", "discourse", "Connect explanations, consequences and contrasts.", "Noma kunzima, siyaqhubeka."),
("aspect", "Aspect and event structure", "B2", "verbs", "Distinguish ongoing, completed, habitual and sequential events.", "Ubelokhu efunda kusukela ekuseni."),
("passive", "Passive constructions", "B2", "verbs", "Present events from the affected participant's perspective.", "Incwadi ibhalwe nguthisha."),
("causative", "Causative constructions", "B2", "derivation", "Express caused actions and changes of state.", "Uthisha ufundisa abafundi."),
("discourse-connectors", "Discourse cohesion", "B2", "discourse", "Organize arguments and narratives with cohesive devices.", "Okokuqala, sizohlola inkinga; bese sibheka isixazululo."),
("nominalization", "Nominalization", "C1", "academic", "Use derived nouns and compact nominal structures in formal prose.", "Ukuthuthukiswa kwemfundo kubalulekile."),
("academic-hedging", "Academic hedging", "C1", "academic", "Qualify claims and separate evidence from interpretation.", "Lokhu kungase kubonise ushintsho oluthile."),
("embedded-questions", "Embedded questions", "C1", "syntax", "Embed questions within formal statements and reports.", "Angazi ukuthi uzofika nini."),
("information-structure", "Topic and focus", "C1", "discourse", "Control emphasis, contrast and information packaging.", "Le nkinga yiyo esiyicwaningayo."),
("formal-register", "Formal and professional register", "C1", "register", "Shift from conversational isiZulu to institutional and professional prose.", "Sicela uthumele isicelo sakho ngokubhaliwe."),
("argumentation", "Academic argumentation", "C1", "rhetoric", "Present claims, evidence, counterarguments and conclusions.", "Ubufakazi busekela lo mbono."),
("pragmatics", "Pragmatics and politeness", "C2", "pragmatics", "Interpret indirectness, politeness and social meaning.", "Mhlawumbe singabheka lolu daba futhi."),
("idioms", "Idiomatic isiZulu", "C2", "lexis", "Interpret figurative expressions through context.", "Unyawo alunampumuzo."),
("media-language", "Media and public language", "C2", "register", "Read concise reporting and public institutional language.", "Uhulumeni umemezele inqubomgomo entsha."),
("rhetoric", "Rhetorical and literary style", "C2", "rhetoric", "Analyze metaphor, repetition, parallelism and rhetorical effect.", "Amazwi akhe ayizibani ebumnyameni."),
("translation", "Translation precision", "C2", "translation", "Choose context-sensitive isiZulu equivalents rather than literal substitutions.", "Incazelo incike kumongo."),
("discourse-analysis", "Discourse analysis", "C2", "discourse", "Analyze cohesion, stance, reference and rhetorical structure.", "Umbhalo wakhe ulandela impikiswano ngokucacile."),
("register-shifting", "Register shifting", "C2", "register", "Reformulate the same message for casual, professional and academic contexts.", "Lo mlayezo ungabhalwa ngendlela esemthethweni."),
]
GRAMMAR_TOPICS = [GrammarTopic(slug=s, title=t, level=l, category=c, summary=sm, explanation=f"{sm} Native isiZulu model: {ex}", examples=[GrammarExample(text=ex)]) for s,t,l,c,sm,ex in _TOPICS]

_VOCAB = [
("zu-a1-1","Greetings","sawubona","hello","Sawubona, unjani?"),
("zu-a1-2","Family","umndeni","family","Umndeni wami mkhulu."),
("zu-a1-3","Home","ikhaya","home","Ngisekhaya."),
("zu-a1-4","Daily life","umsebenzi","work","Ngiya emsebenzini."),
("zu-a1-5","Time","isikhathi","time","Asinaso isikhathi."),
("zu-a1-6","Food","ukudla","food","Ngiyakuthanda lokhu kudla."),
("zu-a1-7","Places","imakethe","market","Ngaya emakethe."),
("zu-a1-8","Directions","indlela","way/road","Le yindlela eya esikoleni."),
("zu-a2-1","Travel","uhambo","journey","Uhambo lude."),
("zu-a2-2","Health","impilo","health/life","Impilo ibalulekile."),
("zu-a2-3","Education","imfundo","education","Imfundo iyasiza."),
("zu-a2-4","Workplace","ihhovisi","office","Usehhovisi."),
("zu-b1-1","Communication","umyalezo","message","Ngithumele umyalezo."),
("zu-b1-2","Community","umphakathi","community","Umphakathi uyabambisana."),
("zu-b1-3","Environment","imvelo","environment","Kumele sivikele imvelo."),
("zu-b1-4","Technology","ubuchwepheshe","technology","Ubuchwepheshe buyashintsha."),
("zu-b2-1","Economy","umnotho","economy","Umnotho uyakhula."),
("zu-b2-2","Policy","inqubomgomo","policy","Inqubomgomo entsha iyasetshenziswa."),
("zu-b2-3","Evidence","ubufakazi","evidence","Ubufakazi bubalulekile."),
("zu-b2-4","Research","ucwaningo","research","Ucwaningo luveza imiphumela."),
("zu-c1-1","Analysis","ukuhlaziya","analysis","Ukuhlaziya kudinga ubufakazi."),
("zu-c1-2","Argument","impikiswano","argument/debate","Impikiswano yakhe icacile."),
("zu-c2-1","Rhetoric","inkulumo","discourse/speech","Inkulumo yakhe iyakhanga."),
("zu-c2-2","Context","umongo","context","Incazelo incike kumongo."),
("zu-c2-3","Translation","inguqulo","translation/version","Le nguqulo inembile."),
]
VOCABULARY_SETS = [VocabularySet(id=i, level=i.split("-")[1].upper(), topic=topic, unit_ref=f"zu-{i.split("-")[1]}-unit-{int(i.split("-")[2])}", words=[VocabularyEntry(word=w,pos="noun",definition=d,example=e)]) for i,topic,w,d,e in _VOCAB]

_UNIT_TOPICS = {
"A1":["Greetings and identity","Family and people","Home and location","Daily routine","Time and appointments","Food and shopping","Places and directions","Everyday communication"],
"A2":["Noun classes and agreement","Object concords","Past narration","Future plans","Polite requests","Comparison","Ability and obligation","Everyday problem solving"],
"B1":["Relative clauses","Subjunctive forms","Conditions","Cause and contrast","Reported speech","Storytelling","Opinions and reasons","Connected conversation"],
"B2":["Aspect","Passive voice","Causative forms","Discourse cohesion","Formal correspondence","Media texts","Evidence and explanation","Professional communication"],
"C1":["Nominalization","Academic hedging","Embedded questions","Topic and focus","Professional register","Argumentation","Research communication","Institutional language"],
"C2":["Pragmatics","Idiomatic language","Media analysis","Rhetorical style","Translation precision","Discourse analysis","Register shifting","Literary and professional synthesis"],
}
CURRICULUM = {}
for level in LEVELS:
    CURRICULUM[level] = []
    for n,title in enumerate(_UNIT_TOPICS[level],1):
        candidates=[v[0] for v in _VOCAB if v[0].split("-")[1].upper()==level]
        vocab_ids=candidates[n-1:n]
        level_topics=[topic for topic in GRAMMAR_TOPICS if topic.level == level]
        idx=min(n-1, len(level_topics)-1)
        grammar_ids=[level_topics[idx].slug] if level_topics else []
        CURRICULUM[level].append(CurriculumUnit(id=f"zu-{level.lower()}-unit-{n}",level=level,unit_number=n,title=f"Zulu {level} · {title}",grammar_points=grammar_ids,vocabulary_set_ids=vocab_ids,lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=[f"Use {level} isiZulu in {title.lower()}","Understand learner-level authentic isiZulu","Produce accurate spoken and written responses"],default_weeks=2))

PHRASEBOOK_CATEGORIES = [
PhrasebookCategory(id="zu-greetings",level="A1",situation="Greetings",icon="👋",phrases=[PhrasebookEntry(text="Sawubona.",context="Hello.",register="neutral"),PhrasebookEntry(text="Unjani?",context="How are you?",register="neutral"),PhrasebookEntry(text="Ngiyaphila.",context="I am well.",register="neutral")]),
PhrasebookCategory(id="zu-thanks",level="A1",situation="Thanks",icon="🙏",phrases=[PhrasebookEntry(text="Ngiyabonga.",context="Thank you.",register="neutral"),PhrasebookEntry(text="Ngiyabonga kakhulu.",context="Thank you very much.",register="polite"),PhrasebookEntry(text="Kulungile.",context="It's alright / no problem.",register="neutral")]),
PhrasebookCategory(id="zu-shopping",level="A1",situation="Shopping",icon="🛒",phrases=[PhrasebookEntry(text="Kubiza malini lokhu?",context="How much does this cost?",register="neutral"),PhrasebookEntry(text="Ngifuna lokhu.",context="I want this.",register="neutral"),PhrasebookEntry(text="Ngicela lokhu.",context="I would like this, please.",register="polite")]),
PhrasebookCategory(id="zu-help",level="A1",situation="Help",icon="🆘",phrases=[PhrasebookEntry(text="Ngicela ungisize.",context="Please help me.",register="polite"),PhrasebookEntry(text="Angiqondi.",context="I don't understand.",register="neutral"),PhrasebookEntry(text="Ngicela uphinde usho.",context="Please say it again.",register="polite")]),
PhrasebookCategory(id="zu-directions",level="A1",situation="Directions",icon="🧭",phrases=[PhrasebookEntry(text="Uphi umgwaqo oya esiteshini?",context="Where is the road to the station?",register="neutral"),PhrasebookEntry(text="Ngifuna ukuya esikoleni.",context="I want to go to the school.",register="neutral"),PhrasebookEntry(text="Hamba uqonde.",context="Go straight.",register="neutral")]),
PhrasebookCategory(id="zu-restaurant",level="A2",situation="Restaurant",icon="🍽️",phrases=[PhrasebookEntry(text="Ngicela imenyu.",context="Please give me the menu.",register="polite"),PhrasebookEntry(text="Ngifuna amanzi.",context="I want water.",register="neutral"),PhrasebookEntry(text="Ngicela isikweletu.",context="Please bring the bill.",register="polite")]),
PhrasebookCategory(id="zu-travel",level="A2",situation="Travel",icon="✈️",phrases=[PhrasebookEntry(text="Iphi ithikithi lami?",context="Where is my ticket?",register="neutral"),PhrasebookEntry(text="Ngifuna indawo yokulala.",context="I need a place to stay.",register="neutral"),PhrasebookEntry(text="Isikhathi sokuhamba singakanani?",context="How long is the journey?",register="neutral")]),
PhrasebookCategory(id="zu-health",level="A2",situation="Health",icon="🩺",phrases=[PhrasebookEntry(text="Ngifuna ukubona udokotela.",context="I need to see a doctor.",register="neutral"),PhrasebookEntry(text="Ngizwa ubuhlungu.",context="I am in pain.",register="neutral"),PhrasebookEntry(text="Isibhedlela sikuphi?",context="Where is the hospital?",register="neutral")]),
PhrasebookCategory(id="zu-work",level="B1",situation="Work",icon="💼",phrases=[PhrasebookEntry(text="Ake siqale umhlangano.",context="Let's start the meeting.",register="formal"),PhrasebookEntry(text="Ngicela unikeze ubufakazi.",context="Please provide the evidence.",register="professional"),PhrasebookEntry(text="Siyavumelana ngalolu daba.",context="We agree on this matter.",register="professional")]),
PhrasebookCategory(id="zu-debate",level="B2",situation="Debate and opinion",icon="💬",phrases=[PhrasebookEntry(text="Ngokombono wami...",context="In my opinion...",register="neutral"),PhrasebookEntry(text="Ubufakazi bubonisa ukuthi...",context="The evidence shows that...",register="formal"),PhrasebookEntry(text="Ngakolunye uhlangothi...",context="On the other hand...",register="formal")]),
PhrasebookCategory(id="zu-academic",level="C1",situation="Academic writing",icon="📚",phrases=[PhrasebookEntry(text="Lolu cwaningo lubonisa ukuthi...",context="This study shows that...",register="formal"),PhrasebookEntry(text="Lokhu kungase kubonise...",context="This may indicate...",register="academic"),PhrasebookEntry(text="Kudingeka olunye ucwaningo.",context="Further research is needed.",register="academic")]),
PhrasebookCategory(id="zu-formal",level="C1",situation="Formal correspondence",icon="📝",phrases=[PhrasebookEntry(text="Mayelana nesicelo sakho...",context="Regarding your application...",register="formal"),PhrasebookEntry(text="Sicela uthumele isicelo sakho.",context="Please submit your application.",register="formal"),PhrasebookEntry(text="Sizokuphendula maduze.",context="We will respond shortly.",register="formal")]),
PhrasebookCategory(id="zu-pragmatics",level="C2",situation="Nuance and pragmatics",icon="🎯",phrases=[PhrasebookEntry(text="Mhlawumbe singabheka lolu daba futhi.",context="Perhaps we can reconsider this matter.",register="neutral"),PhrasebookEntry(text="Lokhu kuncike kumongo.",context="This depends on the context.",register="formal"),PhrasebookEntry(text="Ake sikubeke ngenye indlela.",context="Let's put it another way.",register="nuanced")]),
]

ASSESSMENT_BANK = [
AssessmentQuestion(id="zu-a1-001",skill="communication",difficulty="A1",question="Which isiZulu expression means ‘Hello’?",options=["Sawubona.","Ngiyabonga.","Angiqondi.","Unjani?"],correct="Sawubona."),
AssessmentQuestion(id="zu-a1-002",skill="communication",difficulty="A1",question="Which phrase asks ‘How are you?’",options=["Unjani?","Ngiyaphila.","Ngifuna lokhu.","Kulungile."],correct="Unjani?"),
AssessmentQuestion(id="zu-a1-003",skill="vocabulary",difficulty="A1",question="Which word means ‘family’?",options=["umndeni","indlela","isikhathi","imakethe"],correct="umndeni"),
AssessmentQuestion(id="zu-a1-004",skill="communication",difficulty="A1",question="How do you ask the price of an item?",options=["Kubiza malini lokhu?","Uhlala kuphi?","Ngiyaphila.","Ngicela ungisize."],correct="Kubiza malini lokhu?"),
AssessmentQuestion(id="zu-a2-005",skill="grammar",difficulty="A2",question="Which sentence refers to yesterday?",options=["Izolo ngaya emakethe.","Kusasa ngizoya emsebenzini.","Ngifunda nsuku zonke.","Ngifuna ukufunda isiZulu."],correct="Izolo ngaya emakethe."),
AssessmentQuestion(id="zu-a2-006",skill="communication",difficulty="A2",question="Which is a polite request?",options=["Ngicela uhlale lapha.","Angiqondi.","Ngisekhaya.","Ngaya emakethe."],correct="Ngicela uhlale lapha."),
AssessmentQuestion(id="zu-b1-007",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["Uma isikhathi sikhona, sizohamba.","Izolo ngaya emakethe.","Ngingumfundi.","Ngiyabonga."],correct="Uma isikhathi sikhona, sizohamba."),
AssessmentQuestion(id="zu-b1-008",skill="discourse",difficulty="B1",question="Which sentence reports what someone said?",options=["Uthe uzofika kusasa.","Ngiyaphila.","Sawubona.","Ngifuna lokhu."],correct="Uthe uzofika kusasa."),
AssessmentQuestion(id="zu-b2-009",skill="discourse",difficulty="B2",question="Which expression introduces a contrasting point?",options=["Ngakolunye uhlangothi...","Sawubona.","Ngicela ungisize.","Ngiyaphila."],correct="Ngakolunye uhlangothi..."),
AssessmentQuestion(id="zu-c1-010",skill="academic",difficulty="C1",question="Which phrase appropriately hedges an academic claim?",options=["Lokhu kungase kubonise...","Lokhu kufakazela konke ngokuphelele.","Sawubona.","Kubiza malini lokhu?"],correct="Lokhu kungase kubonise..."),
AssessmentQuestion(id="zu-c1-011",skill="formal",difficulty="C1",question="Which phrase belongs to formal correspondence?",options=["Sicela uthumele isicelo sakho.","Unjani?","Ngifuna lokhu.","Sawubona."],correct="Sicela uthumele isicelo sakho."),
AssessmentQuestion(id="zu-c2-012",skill="pragmatics",difficulty="C2",question="Which phrase explicitly refers to contextual interpretation?",options=["Lokhu kuncike kumongo.","Ngiyabonga.","Ngisekhaya.","Kubiza malini lokhu?"],correct="Lokhu kuncike kumongo."),
]

"""Croatian A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

GRAMMAR_TOPICS=[
GrammarTopic(slug="pronouns",title="Personal pronouns and reference",level="A1",category="grammar",summary="Introduce people and refer to participants clearly.",explanation="Croatian personal pronouns are often omitted when the verb ending already identifies the subject.",examples=[GrammarExample(text="Ja sam Ana."),GrammarExample(text="Učim hrvatski.")]),
GrammarTopic(slug="cases",title="Cases and prepositions",level="A2",category="grammar",summary="Use Croatian case endings in everyday contexts.",explanation="Nouns change form according to grammatical role and preposition; common A2 patterns include accusative for destinations and genitive after many prepositions.",examples=[GrammarExample(text="Idem u školu."),GrammarExample(text="Nema vode.")]),
GrammarTopic(slug="past",title="Perfect tense",level="A2",category="grammar",summary="Talk about completed past events.",explanation="The Croatian perfect combines the auxiliary biti with the l-participle, with agreement in gender and number.",examples=[GrammarExample(text="Jučer sam radio."),GrammarExample(text="Ona je stigla rano.")]),
GrammarTopic(slug="future",title="Future I",level="A2",category="grammar",summary="Describe plans and predictions.",explanation="Future I commonly uses the auxiliary ću/ćeš/će plus an infinitive or clitic placement pattern.",examples=[GrammarExample(text="Sutra ću raditi."),GrammarExample(text="Ona će doći.")]),
GrammarTopic(slug="aspect",title="Verbal aspect",level="B1",category="grammar",summary="Distinguish ongoing and completed actions.",explanation="Croatian pairs imperfective and perfective verbs to express process versus bounded completion.",examples=[GrammarExample(text="Čitam knjigu."),GrammarExample(text="Pročitao sam knjigu.")]),
GrammarTopic(slug="comparatives",title="Comparison",level="B1",category="grammar",summary="Compare people, objects and situations.",explanation="Use comparative and superlative forms with agreement and appropriate complements.",examples=[GrammarExample(text="Ovaj je zadatak lakši."),GrammarExample(text="To je najbolji izbor.")]),
GrammarTopic(slug="conditional",title="Conditional mood",level="B2",category="grammar",summary="Express hypotheses, wishes and polite proposals.",explanation="The conditional uses the past auxiliary bi with the l-participle.",examples=[GrammarExample(text="Pomogao bih ti."),GrammarExample(text="Kad bih imao vremena, putovao bih.")]),
GrammarTopic(slug="relative",title="Relative clauses",level="B2",category="grammar",summary="Combine information into precise complex sentences.",explanation="Relative clauses commonly use koji/koja/koje and their declined forms.",examples=[GrammarExample(text="To je knjiga koju sam kupio.")]),
GrammarTopic(slug="reported_speech",title="Reported speech",level="C1",category="grammar",summary="Report information accurately and coherently.",explanation="Reported content can be introduced with da or interrogative conjunctions while maintaining tense and reference.",examples=[GrammarExample(text="Rekao je da će doći.")]),
GrammarTopic(slug="register",title="Formal and professional register",level="C1",category="grammar",summary="Adapt grammar and vocabulary to institutional contexts.",explanation="Formal Croatian favors explicit reference, precise connectors and conventional administrative phrasing.",examples=[GrammarExample(text="Molimo vas da dostavite dokumentaciju.")]),
GrammarTopic(slug="nominalization",title="Academic nominalization and complex syntax",level="C2",category="grammar",summary="Handle dense academic and analytical prose.",explanation="Advanced Croatian uses nominalizations, participial structures and layered subordination to compress complex arguments.",examples=[GrammarExample(text="Provedba mjere zahtijeva prethodnu procjenu učinaka.")]),
GrammarTopic(slug="pragmatics",title="Idiomatic and pragmatic nuance",level="C2",category="grammar",summary="Interpret tone, implication and idiomatic meaning.",explanation="Advanced proficiency requires recognizing collocations, discourse stance, irony and register-sensitive formulations.",examples=[GrammarExample(text="Nije sve crno-bijelo.")]),
]

VOCABULARY_SETS=[
VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="hr-a1-unit-1",words=[VocabularyEntry(word="Bok",pos="phrase",definition="hi",example="Bok! Kako si?"),VocabularyEntry(word="dobro jutro",pos="phrase",definition="good morning",example="Dobro jutro!"),VocabularyEntry(word="hvala",pos="phrase",definition="thank you",example="Hvala na pomoći."),VocabularyEntry(word="doviđenja",pos="phrase",definition="goodbye",example="Doviđenja i ugodan dan.")]),
VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="hr-a1-unit-2",words=[VocabularyEntry(word="ime",pos="noun",definition="name",example="Kako ti je ime?"),VocabularyEntry(word="učenik",pos="noun",definition="student",example="Ja sam učenik."),VocabularyEntry(word="prijatelj",pos="noun",definition="friend",example="On je moj prijatelj."),VocabularyEntry(word="jezik",pos="noun",definition="language",example="Hrvatski je moj ciljni jezik.")]),
VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="hr-a1-unit-3",words=[VocabularyEntry(word="majka",pos="noun",definition="mother",example="Moja majka radi."),VocabularyEntry(word="otac",pos="noun",definition="father",example="Moj otac je kod kuće."),VocabularyEntry(word="brat",pos="noun",definition="brother",example="Moj brat studira."),VocabularyEntry(word="sestra",pos="noun",definition="sister",example="Moja sestra čita.")]),
VocabularySet(id="home_a1",level="A1",topic="home",unit_ref="hr-a1-unit-4",words=[VocabularyEntry(word="kuća",pos="noun",definition="house",example="Moja kuća je velika."),VocabularyEntry(word="soba",pos="noun",definition="room",example="Soba je svijetla."),VocabularyEntry(word="vrata",pos="noun",definition="door",example="Vrata su otvorena."),VocabularyEntry(word="stol",pos="noun",definition="table",example="Knjiga je na stolu.")]),
VocabularySet(id="daily_a1",level="A1",topic="daily",unit_ref="hr-a1-unit-5",words=[VocabularyEntry(word="jutro",pos="noun",definition="morning",example="Ujutro pijem kavu."),VocabularyEntry(word="posao",pos="noun",definition="work",example="Idem na posao."),VocabularyEntry(word="voda",pos="noun",definition="water",example="Pijem vodu."),VocabularyEntry(word="danas",pos="noun",definition="today",example="Danas učim hrvatski.")]),
VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="hr-a1-unit-6",words=[VocabularyEntry(word="kruh",pos="noun",definition="bread",example="Kupujem kruh."),VocabularyEntry(word="kava",pos="noun",definition="coffee",example="Želim kavu."),VocabularyEntry(word="jabuka",pos="noun",definition="apple",example="Jedem jabuku."),VocabularyEntry(word="račun",pos="noun",definition="bill",example="Molim račun.")]),
VocabularySet(id="places_a1",level="A1",topic="places",unit_ref="hr-a1-unit-7",words=[VocabularyEntry(word="škola",pos="noun",definition="school",example="Škola je blizu."),VocabularyEntry(word="tržnica",pos="noun",definition="market",example="Gdje je tržnica?"),VocabularyEntry(word="bolnica",pos="noun",definition="hospital",example="Bolnica je u centru."),VocabularyEntry(word="ulica",pos="noun",definition="street",example="Živim u ovoj ulici.")]),
VocabularySet(id="communication_a1",level="A1",topic="communication",unit_ref="hr-a1-unit-8",words=[VocabularyEntry(word="pitanje",pos="noun",definition="question",example="Imam jedno pitanje."),VocabularyEntry(word="pomoć",pos="noun",definition="help",example="Trebam pomoć."),VocabularyEntry(word="razgovor",pos="noun",definition="conversation",example="Imamo kratak razgovor."),VocabularyEntry(word="razumjeti",pos="verb",definition="to understand",example="Ne razumijem pitanje.")]),
VocabularySet(id="past_a2",level="A2",topic="past experiences",unit_ref="hr-a2-unit-1",words=[VocabularyEntry(word="jučer",pos="adverb",definition="yesterday",example="Jučer sam radio."),VocabularyEntry(word="putovati",pos="verb",definition="to travel",example="Putovali smo prošlog ljeta."),VocabularyEntry(word="stići",pos="verb",definition="to arrive",example="Stigli smo na vrijeme."),VocabularyEntry(word="posjetiti",pos="verb",definition="to visit",example="Posjetila je Zagreb.")]),
VocabularySet(id="travel_a2",level="A2",topic="travel",unit_ref="hr-a2-unit-2",words=[VocabularyEntry(word="kolodvor",pos="noun",definition="station",example="Kolodvor je blizu."),VocabularyEntry(word="karta",pos="noun",definition="ticket",example="Trebam povratnu kartu."),VocabularyEntry(word="smještaj",pos="noun",definition="accommodation",example="Rezervirali smo smještaj."),VocabularyEntry(word="putovanje",pos="noun",definition="journey",example="Putovanje traje tri sata.")]),
VocabularySet(id="work_b1",level="B1",topic="work",unit_ref="hr-b1-unit-1",words=[VocabularyEntry(word="sastanak",pos="noun",definition="meeting",example="Sastanak počinje u devet."),VocabularyEntry(word="rok",pos="noun",definition="deadline",example="Rok je u petak."),VocabularyEntry(word="iskustvo",pos="noun",definition="experience",example="Imam iskustvo u prodaji."),VocabularyEntry(word="vještina",pos="noun",definition="skill",example="Komunikacijske vještine su važne.")]),
VocabularySet(id="media_b1",level="B1",topic="media",unit_ref="hr-b1-unit-2",words=[VocabularyEntry(word="vijest",pos="noun",definition="news item",example="Pročitao sam vijest."),VocabularyEntry(word="izvor",pos="noun",definition="source",example="Provjeri izvor informacije."),VocabularyEntry(word="stav",pos="noun",definition="viewpoint",example="Izrazio je svoj stav."),VocabularyEntry(word="rasprava",pos="noun",definition="discussion",example="Rasprava je bila zanimljiva.")]),
VocabularySet(id="society_b2",level="B2",topic="society",unit_ref="hr-b2-unit-1",words=[VocabularyEntry(word="društvo",pos="noun",definition="society",example="Društvo se brzo mijenja."),VocabularyEntry(word="održivost",pos="noun",definition="sustainability",example="Održivost je važan cilj."),VocabularyEntry(word="posljedica",pos="noun",definition="consequence",example="Moramo procijeniti posljedice."),VocabularyEntry(word="rješenje",pos="noun",definition="solution",example="Predloženo je novo rješenje.")]),
VocabularySet(id="argumentation_b2",level="B2",topic="argumentation",unit_ref="hr-b2-unit-2",words=[VocabularyEntry(word="međutim",pos="adverb",definition="however",example="Međutim, postoje i drugačiji podaci."),VocabularyEntry(word="stoga",pos="adverb",definition="therefore",example="Stoga predlažemo promjenu."),VocabularyEntry(word="dokaz",pos="noun",definition="evidence",example="Dokaz podupire tvrdnju."),VocabularyEntry(word="pretpostavka",pos="noun",definition="assumption",example="Ta pretpostavka nije potvrđena.")]),
VocabularySet(id="professional_c1",level="C1",topic="professional communication",unit_ref="hr-c1-unit-1",words=[VocabularyEntry(word="dostaviti",pos="verb",definition="to submit/provide",example="Molimo vas da dostavite dokumentaciju."),VocabularyEntry(word="provedba",pos="noun",definition="implementation",example="Provedba mjere počinje u lipnju."),VocabularyEntry(word="zahtjev",pos="noun",definition="request/application",example="Zahtjev je zaprimljen."),VocabularyEntry(word="nadležnost",pos="noun",definition="jurisdiction/responsibility",example="To je u nadležnosti odjela.")]),
VocabularySet(id="academic_c1",level="C1",topic="academic language",unit_ref="hr-c1-unit-2",words=[VocabularyEntry(word="istraživanje",pos="noun",definition="research",example="Istraživanje pokazuje trend."),VocabularyEntry(word="metodologija",pos="noun",definition="methodology",example="Metodologija je jasno opisana."),VocabularyEntry(word="nalaz",pos="noun",definition="finding",example="Nalazi potvrđuju hipotezu."),VocabularyEntry(word="ograničenje",pos="noun",definition="limitation",example="Istraživanje ima nekoliko ograničenja.")]),
VocabularySet(id="nuance_c2",level="C2",topic="nuance and style",unit_ref="hr-c2-unit-1",words=[VocabularyEntry(word="dvosmislen",pos="adjective",definition="ambiguous",example="Izjava je namjerno dvosmislena."),VocabularyEntry(word="nijansa",pos="noun",definition="nuance",example="Važna je semantička nijansa."),VocabularyEntry(word="pretpostaviti",pos="verb",definition="to assume",example="Ne možemo unaprijed pretpostaviti ishod."),VocabularyEntry(word="ublažiti",pos="verb",definition="to mitigate/soften",example="Autor nastoji ublažiti tvrdnju.")]),
VocabularySet(id="idioms_c2",level="C2",topic="idioms",unit_ref="hr-c2-unit-2",words=[VocabularyEntry(word="držati figu u džepu",pos="phrase",definition="to secretly have a different intention",example="Čini se da drži figu u džepu."),VocabularyEntry(word="baciti oko",pos="idiom",definition="to take a look",example="Baci oko na ovaj prijedlog."),VocabularyEntry(word="nije sve crno-bijelo",pos="phrase",definition="things are not simply one-sided",example="Situacija je složena; nije sve crno-bijelo.")])
]

PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="greetings_a1",level="A1",situation="greetings",icon="👋",phrases=[PhrasebookEntry(text="Dobro jutro!",context="greetings",register="neutral"),PhrasebookEntry(text="Kako si?",context="greetings",register="neutral"),PhrasebookEntry(text="Drago mi je.",context="introductions",register="neutral")]),
PhrasebookCategory(id="daily_a1",level="A1",situation="daily",icon="☀️",phrases=[PhrasebookEntry(text="Idem na posao.",context="daily",register="neutral"),PhrasebookEntry(text="Trebam pomoć.",context="daily",register="neutral")]),
PhrasebookCategory(id="shopping_a1",level="A1",situation="shopping",icon="🛒",phrases=[PhrasebookEntry(text="Koliko ovo košta?",context="shopping",register="neutral"),PhrasebookEntry(text="Molim račun.",context="shopping",register="neutral")]),
PhrasebookCategory(id="directions_a1",level="A1",situation="directions",icon="🧭",phrases=[PhrasebookEntry(text="Gdje je kolodvor?",context="directions",register="neutral"),PhrasebookEntry(text="Kako mogu doći do centra?",context="directions",register="neutral")]),
PhrasebookCategory(id="travel_a2",level="A2",situation="travel",icon="✈️",phrases=[PhrasebookEntry(text="Imam rezervaciju.",context="travel",register="neutral"),PhrasebookEntry(text="Kada polazi autobus?",context="travel",register="neutral")]),
PhrasebookCategory(id="work_b1",level="B1",situation="work",icon="💼",phrases=[PhrasebookEntry(text="Možemo li dogovoriti sastanak?",context="work",register="neutral"),PhrasebookEntry(text="Rok za ovaj zadatak je u petak.",context="work",register="neutral")]),
PhrasebookCategory(id="discussion_b2",level="B2",situation="discussion",icon="💬",phrases=[PhrasebookEntry(text="Slažem se s tim argumentom.",context="discussion",register="neutral"),PhrasebookEntry(text="Međutim, moramo uzeti u obzir i drugu stranu.",context="discussion",register="formal")]),
PhrasebookCategory(id="formal_c1",level="C1",situation="formal",icon="📄",phrases=[PhrasebookEntry(text="Molimo vas da dostavite potrebnu dokumentaciju.",context="formal",register="formal"),PhrasebookEntry(text="U skladu s navedenim okolnostima predlažemo izmjenu.",context="formal",register="formal")]),
PhrasebookCategory(id="academic_c2",level="C2",situation="academic",icon="🎓",phrases=[PhrasebookEntry(text="Ovaj nalaz valja tumačiti s određenom dozom opreza.",context="academic",register="formal"),PhrasebookEntry(text="Ne može se zanemariti činjenica da su rezultati višeznačni.",context="academic",register="formal")])
]

_CURRICULUM_META={
"A1":["Pozdravi i upoznavanje","Obitelj i dom","Svakodnevni život","Hrana i kupovina","Mjesta i smjerovi","Komunikacija","Vrijeme i planovi","Ponavljanje"],
"A2":["Prošlost i iskustva","Putovanja","Zdravlje i usluge","Planovi i budućnost","Usporedbe","Posao i obaveze","Stanovanje i grad","Ponavljanje"],
"B1":["Pripovijedanje i aspekt","Posao i suradnja","Društvo","Mediji i izvori","Argumentiranje","Kultura","Problemi i rješenja","Ponavljanje"],
"B2":["Složene rečenice","Profesionalna komunikacija","Društvene teme","Analiza medija","Argumentacija","Formalni stil","Debata i pregovaranje","Ponavljanje"],
"C1":["Precizno izražavanje","Institucionalni jezik","Analitičko čitanje","Akademski stil","Sažimanje i parafraza","Prezentacije","Profesionalno pisanje","Ponavljanje"],
"C2":["Semantička nijansa","Stil i registar","Kritička analiza","Apstraktna argumentacija","Idiomi i kolokacije","Retorika","Uređivanje naprednog teksta","Ponavljanje"]
}

_LEVEL_GRAMMAR={
"A1":["pronouns","nominal","present","questions","negation","demonstratives","possessive","location"],
"A2":["cases","past","future","questions","location","comparatives","negation","present"],
"B1":["aspect","comparatives","past","future","cases","conditional","relative","present"],
"B2":["conditional","relative","reported_speech","cases","aspect","comparatives","register","future"],
"C1":["reported_speech","register","relative","conditional","nominalization","aspect","cases","pragmatics"],
"C2":["nominalization","pragmatics","register","reported_speech","relative","conditional","aspect","cases"]
}

_LEVEL_VOCAB={
"A1":["greetings_a1","identity_a1","family_a1","home_a1","daily_a1","food_a1","places_a1","communication_a1"],
"A2":["past_a2","travel_a2","past_a2","travel_a2","past_a2","travel_a2","past_a2","travel_a2"],
"B1":["work_b1","media_b1","work_b1","media_b1","work_b1","media_b1","work_b1","media_b1"],
"B2":["society_b2","argumentation_b2","society_b2","argumentation_b2","society_b2","argumentation_b2","society_b2","argumentation_b2"],
"C1":["professional_c1","academic_c1","professional_c1","academic_c1","professional_c1","academic_c1","professional_c1","academic_c1"],
"C2":["nuance_c2","idioms_c2","academic_c1","argumentation_b2","idioms_c2","nuance_c2","academic_c1","idioms_c2"]
}

CURRICULUM={}
for level in LEVELS:
    CURRICULUM[level]=[]
    for i,title in enumerate(_CURRICULUM_META[level],1):
        CURRICULUM[level].append(CurriculumUnit(
            id=f"hr-{level.lower()}-unit-{i}",level=level,unit_number=i,title=title,
            grammar_points=[_LEVEL_GRAMMAR[level][i-1]],
            vocabulary_set_ids=[_LEVEL_VOCAB[level][i-1]],
            lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],
            competency_checklist=["Understand the unit theme in Croatian","Use target structures in context","Complete a short communicative task"],
            default_weeks=2
        ))

ASSESSMENT_BANK=[
AssessmentQuestion(id="hr-a1-001",skill="grammar",difficulty="A1",question="Choose the natural Croatian greeting for the morning.",options=["Dobro jutro!","Doviđenja!","Hvala!","Laku noć!"],correct="Dobro jutro!"),
AssessmentQuestion(id="hr-a1-002",skill="grammar",difficulty="A1",question="Complete: ___ sam Ana.",options=["Ja","Moj","Ona","Mi"],correct="Ja"),
AssessmentQuestion(id="hr-a1-003",skill="vocabulary",difficulty="A1",question="Which word means 'brother'?",options=["brat","sestra","majka","otac"],correct="brat"),
AssessmentQuestion(id="hr-a1-004",skill="communication",difficulty="A1",question="How do you ask someone's name?",options=["Kako ti je ime?","Koliko ovo košta?","Gdje je škola?","Što radiš sutra?"],correct="Kako ti je ime?"),
AssessmentQuestion(id="hr-a2-001",skill="grammar",difficulty="A2",question="Choose the correct Croatian sentence for a completed action.",options=["Jučer sam radio.","Jučer radim.","Jučer ću raditi.","Jučer raditi."],correct="Jučer sam radio."),
AssessmentQuestion(id="hr-a2-002",skill="grammar",difficulty="A2",question="Choose the natural future form.",options=["Sutra ću putovati.","Sutra sam putovao.","Sutra putovao.","Sutra sam putovati."],correct="Sutra ću putovati."),
AssessmentQuestion(id="hr-b1-001",skill="grammar",difficulty="B1",question="Which pair contrasts an ongoing activity with a completed action?",options=["Čitam / pročitam","sam / si","kuća / kuće","dobar / najbolji"],correct="Čitam / pročitam"),
AssessmentQuestion(id="hr-b1-002",skill="vocabulary",difficulty="B1",question="Which word means 'deadline'?",options=["rok","izvor","stav","vještina"],correct="rok"),
AssessmentQuestion(id="hr-b2-001",skill="grammar",difficulty="B2",question="Choose the conditional sentence.",options=["Pomogao bih ti.","Pomažem ti.","Pomogao sam ti.","Pomozi mi."],correct="Pomogao bih ti."),
AssessmentQuestion(id="hr-b2-002",skill="grammar",difficulty="B2",question="Choose the relative clause.",options=["To je knjiga koju sam kupio.","To je knjiga kupio.","To je knjiga sam kupio.","To je knjiga kupujem."],correct="To je knjiga koju sam kupio."),
AssessmentQuestion(id="hr-c1-001",skill="register",difficulty="C1",question="Which phrase is appropriate for a formal request?",options=["Molimo vas da dostavite dokumentaciju.","Bok, pošalji papire.","Daj mi to.","Ajde, pošalji."],correct="Molimo vas da dostavite dokumentaciju."),
AssessmentQuestion(id="hr-c1-002",skill="academic",difficulty="C1",question="Which word means 'methodology'?",options=["metodologija","nadležnost","zahtjev","nalaz"],correct="metodologija"),
AssessmentQuestion(id="hr-c2-001",skill="pragmatics",difficulty="C2",question="Which expression explicitly signals semantic nuance?",options=["nijansa","vrata","kolodvor","kruh"],correct="nijansa"),
AssessmentQuestion(id="hr-c2-002",skill="pragmatics",difficulty="C2",question="Which expression conveys that a situation is not simply one-sided?",options=["Nije sve crno-bijelo.","Dobro jutro!","Molim račun.","Idem na posao."],correct="Nije sve crno-bijelo.")
]

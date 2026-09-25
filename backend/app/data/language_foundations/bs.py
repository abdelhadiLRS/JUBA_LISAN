"""Bosnian A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def g(slug,title,summary,level,category,examples):
    return GrammarTopic(slug=slug,title=title,level=level,category=category,summary=summary,explanation=summary,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS = [
    g("pronouns","Personal pronouns","Use subject and object pronouns in everyday Bosnian.","A1","core",["Ja sam student.","Ona me razumije."]),
    g("gender","Gender and agreement","Match nouns, adjectives and past participles for gender.","A1","core",["Ovo je nova knjiga.","On je umoran."]),
    g("cases","Core case system","Use nominative, accusative, genitive, dative, instrumental and locative.","A1","core",["Vidim prijatelja.","Razgovaram s prijateljem."]),
    g("present","Present tense","Conjugate common verbs for routines and current actions.","A1","core",["Učim bosanski.","Radimo danas."]),
    g("questions","Questions","Form yes/no and wh-questions with appropriate word order.","A1","core",["Gdje živiš?","Da li radiš danas?"]),
    g("negation","Negation","Use ne and nije to negate verbal and nominal clauses.","A1","core",["Ne razumijem.","Ovo nije problem."]),
    g("possessives","Possession","Express ownership with possessive pronouns and genitive patterns.","A1","core",["Ovo je moja knjiga.","Kuća mog brata je velika."]),
    g("location","Location and prepositions","Use locative and prepositional phrases for places.","A1","core",["Knjiga je na stolu.","Živim u Sarajevu."]),
    g("past","Past tense","Narrate completed events with the perfect.","A2","core",["Jučer sam radio.","Ona je došla rano."]),
    g("future","Future tense","Express future plans and predictions.","A2","core",["Sutra ću raditi.","Vidjet ćemo kasnije."]),
    g("aspect","Verb aspect","Distinguish perfective and imperfective meanings.","A2","core",["Čitam knjigu.","Pročitao sam knjigu."]),
    g("comparatives","Comparison","Form comparative and superlative constructions.","A2","core",["Ovaj grad je veći.","To je najbolji izbor."]),
    g("imperative","Imperative and politeness","Give commands and polite requests.","A2","core",["Dođite, molim vas.","Nemoj kasniti."]),
    g("modality","Modality","Express ability, necessity, intention and probability.","A2","core",["Moram učiti.","Možda će doći."]),
    g("relative","Relative clauses","Use koji, koja, koje and case forms to connect clauses.","A2","core",["To je knjiga koju čitam.","Čovjek koji radi ovdje je ljubazan."]),
    g("conditional","Conditional","Use bih/bi/bismo/biste/bismo with participles for hypothetical meaning.","A2","core",["Došao bih da imam vremena.","Kad bih znao, rekao bih."]),
    g("purpose_cause","Cause and purpose","Express reasons and goals with jer, zato što, da and radi.","B1","intermediate",["Ostao sam jer je padala kiša.","Učim da bih položio ispit."]),
    g("reported","Reported speech","Report statements and questions with da, kako and embedded clauses.","B1","intermediate",["Rekao je da će doći.","Pitala je gdje živim."]),
    g("passive","Passive voice","Form passive clauses with biti and passive participles.","B1","intermediate",["Izvještaj je napisan.","Dokumenti su poslani."]),
    g("reflexive","Reflexive constructions","Use se and svoj for reflexive reference.","B1","intermediate",["Ana je kupila sebi knjigu.","On je uzeo svoj kaput."]),
    g("connectors","Discourse connectors","Link clauses with ali, međutim, zato, stoga and dok.","B1","intermediate",["Želim doći, ali nemam vremena.","Zato smo ostali."]),
    g("concession","Concession and contrast","Express although, despite and contrastive relations.","B1","intermediate",["Iako je kasno, nastavljamo.","Uprkos problemu, radimo dalje."]),
    g("subordination","Complex subordination","Build temporal, causal and conditional subordinate clauses.","B1","intermediate",["Kada stigne, počet ćemo.","Ako bude vremena, razgovarat ćemo."]),
    g("nominalization","Nominalization","Use abstract nouns in formal and analytical Bosnian.","B1","intermediate",["Provedba projekta je važna.","Poboljšanje kvaliteta zahtijeva vrijeme."]),
    g("hedging","Academic hedging","Qualify claims with moguće je, čini se, vjerovatno and related forms.","B2","intermediate",["Moguće je da će rezultat biti drugačiji.","Čini se da je pristup učinkovit."]),
    g("embedded_questions","Embedded questions","Embed questions in formal and reported structures.","B2","intermediate",["Nije jasno zašto je odluka promijenjena.","Ne znam kada će sastanak početi."]),
    g("formal_admin","Formal and administrative Bosnian","Handle notices, requests and institutional procedures.","B2","intermediate",["Molimo vas da dostavite dokumente.","Zahtjev treba podnijeti do navedenog roka."]),
    g("academic_argument","Academic argumentation","Present claims, evidence, qualifications and conclusions.","B2","intermediate",["Dostupni podaci podržavaju ovaj zaključak.","Međutim, uzorak je ograničen."]),
    g("information_structure","Topic and focus","Manage emphasis, topic and contrast through word order and particles.","C1","advanced",["Što se tiče ovog pitanja, raspravit ćemo kasnije.","Posebno je važna kvaliteta podataka."]),
    g("register","Register and politeness","Shift between informal, neutral and formal Bosnian.","C1","advanced",["Gdje si?","Gdje ste, molim vas?"]),
    g("pragmatics","Pragmatics and indirectness","Use context-sensitive requests, refusals and politeness.","C1","advanced",["Biste li mogli poslati dokument?","Ako nije problem, možemo li razgovarati?"]),
    g("rhetoric","Rhetorical Bosnian","Use parallelism, contrast and emphasis in persuasive discourse.","C1","advanced",["S jedne strane postoje prednosti, s druge rizici.","Najvažnije je da odluka bude utemeljena."]),
    g("literary","Literary and idiomatic language","Interpret idioms, figurative language and literary register.","C1","advanced",["Vrijeme leti.","On je stub porodice."]),
    g("translation","Translation precision","Preserve case relations, aspect, register and discourse meaning.","C1","advanced",["Izbor glagolskog vida mijenja značenje rečenice.","Formalni izraz treba prilagoditi kontekstu."]),
    g("discourse_analysis","Discourse analysis","Analyze cohesion, reference, stance, genre and paragraph structure.","C2","advanced",["Stoga navedeni argument treba posmatrati u širem kontekstu.","Ipak, zaključak se temelji na ograničenim podacima."]),
]

def v(i,level,topic,words):
    return VocabularySet(id=i,level=level,topic=topic,unit_ref=f"bs-{level.lower()}",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])

VOCABULARY_SETS = [
    v("greetings_a1","A1","Greetings",[["zdravo","phrase","hello","Zdravo!"],["hvala","phrase","thank you","Hvala vam."],["ime","noun","name","Moje ime je Amel."],["prijatelj","noun","friend","On je moj prijatelj."]]),
    v("family_a1","A1","Family",[["majka","noun","mother","Moja majka je kod kuće."],["otac","noun","father","Moj otac radi."],["sestra","noun","sister","Moja sestra studira."],["brat","noun","brother","Moj brat je ovdje."]]),
    v("home_a1","A1","Home",[["kuća","noun","house","Moja kuća je velika."],["soba","noun","room","Soba je čista."],["sto","noun","table","Knjiga je na stolu."],["vrata","noun","door","Vrata su otvorena."]]),
    v("daily_a1","A1","Daily life",[["jutro","noun","morning","Ujutro učim."],["raditi","verb","work","Radim svaki dan."],["učiti","verb","study","Učim bosanski."],["spavati","verb","sleep","Spavam noću."]]),
    v("food_a1","A1","Food",[["voda","noun","water","Molim vas, voda."],["hljeb","noun","bread","Kupujem hljeb."],["kafa","noun","coffee","Pijem kafu."],["cijena","noun","price","Koja je cijena?"]]),
    v("places_a1","A1","Places",[["ulica","noun","street","Ova ulica je duga."],["stanica","noun","station","Stanica je blizu."],["lijevo","adverb","left","Skrenite lijevo."],["desno","adverb","right","Skrenite desno."]]),
    v("time_a2","A2","Time",[["vrijeme","noun","time","Nemam vremena."],["sedmica","noun","week","Vidimo se sljedeće sedmice."],["rano","adverb","early","Dođite rano."],["kasno","adverb","late","Danas je kasno."]]),
    v("travel_a2","A2","Travel",[["karta","noun","ticket","Trebam kartu."],["aerodrom","noun","airport","Gdje je aerodrom?"],["putovanje","noun","journey","Putovanje je dugo."],["rezervacija","noun","reservation","Imam rezervaciju."]]),
    v("health_a2","A2","Health",[["bol","noun","pain","Imam bol u glavi."],["lijek","noun","medicine","Doktor je propisao lijek."],["bolnica","noun","hospital","Bolnica je blizu."],["odmor","noun","rest","Treba mi odmor."]]),
    v("education_b1","B1","Education",[["obrazovanje","noun","education","Obrazovanje je važno."],["ispit","noun","exam","Ispit je sljedeće sedmice."],["nastavnik","noun","teacher","Nastavnik objašnjava."],["istraživanje","noun","research","Istraživanje traje godinu dana."]]),
    v("work_b1","B1","Work",[["ured","noun","office","Ured se otvara u devet."],["sastanak","noun","meeting","Sastanak počinje uskoro."],["iskustvo","noun","experience","Imam pet godina iskustva."],["odgovornost","noun","responsibility","To je moja odgovornost."]]),
    v("society_b2","B2","Society",[["društvo","noun","society","Društvo se mijenja."],["jednakost","noun","equality","Jednakost je važna."],["pravo","noun","right","Svako ima prava."],["politika","noun","policy","Nova politika stupa na snagu."]]),
    v("environment_b2","B2","Environment",[["okoliš","noun","environment","Zaštita okoliša je važna."],["zagađenje","noun","pollution","Zagađenje treba smanjiti."],["resurs","noun","resource","Resursi su ograničeni."],["klima","noun","climate","Klima se mijenja."]]),
    v("technology_b2","B2","Technology",[["tehnologija","noun","technology","Tehnologija se brzo razvija."],["softver","noun","software","Softver je ažuriran."],["podaci","noun","data","Podaci su analizirani."],["sigurnost","noun","security","Sigurnost podataka je važna."]]),
    v("economy_c1","C1","Economy",[["ekonomija","noun","economy","Ekonomija se oporavlja."],["ulaganje","noun","investment","Ulaganja rastu."],["produktivnost","noun","productivity","Produktivnost je porasla."],["tržište","noun","market","Tržište je konkurentno."]]),
    v("governance_c1","C1","Governance",[["uprava","noun","administration","Uprava je objavila informaciju."],["postupak","noun","procedure","Postupak je jasan."],["pravilnik","noun","regulation","Pravilnik je objavljen."],["usklađenost","noun","compliance","Usklađenost je obavezna."]]),
    v("academic_c1","C1","Academic discourse",[["hipoteza","noun","hypothesis","Hipoteza je testirana."],["analiza","noun","analysis","Analiza pokazuje razliku."],["dokaz","noun","evidence","Dokazi nisu dovoljni."],["zaključak","noun","conclusion","Zaključak je jasan."]]),
    v("media_c2","C2","Media and public discourse",[["diskurs","noun","discourse","Javni diskurs se mijenja."],["stav","noun","viewpoint","To je drugačiji stav."],["tumačenje","noun","interpretation","Postoje različita tumačenja."],["relevantnost","noun","relevance","Relevantnost pitanja je jasna."]]),
    v("literary_c2","C2","Literary language",[["metafora","noun","metaphor","Metafora je snažna."],["nijansa","noun","nuance","Nijansa je važna u prijevodu."],["izraz","noun","expression","Ovaj izraz je idiomatski."],["stil","noun","style","Stil autora je prepoznatljiv."]]),
]

def p(i,level,situation,items):
    return PhrasebookCategory(id=i,level=level,situation=situation,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in items])

PHRASEBOOK_CATEGORIES = [
    p("greetings_a1","A1","Greetings",[["Dobar dan, kako ste?","greeting","polite"],["Moje ime je Amel.","introducing yourself","neutral"]]),
    p("shopping_a1","A1","Shopping",[["Koliko ovo košta?","asking price","neutral"],["Molim vas, trebam ovo.","requesting an item","polite"]]),
    p("directions_a1","A1","Directions",[["Gdje je stanica?","asking location","neutral"],["Skrenite desno.","giving directions","neutral"]]),
    p("help_a1","A1","Help",[["Možete li mi pomoći?","asking for help","polite"],["Možete li ponoviti?","asking for repetition","polite"]]),
    p("travel_a2","A2","Travel",[["Gdje je moja rezervacija?","checking reservation","neutral"],["Kada polazi autobus?","asking departure time","neutral"]]),
    p("health_a2","A2","Health",[["Moram kod doktora.","requesting medical help","neutral"],["Ovdje me boli.","describing pain","neutral"]]),
    p("education_b1","B1","Education",[["Možete li objasniti ovaj pojam?","asking for explanation","polite"],["Predao sam zadatak.","reporting submission","neutral"]]),
    p("work_b1","B1","Work",[["Možemo li početi sastanak?","starting a meeting","neutral"],["Predlažem da ovo razmotrimo.","offering a formal suggestion","formal"]]),
    p("formal_b2","B2","Formal requests",[["Molimo vas da dostavite potrebnu dokumentaciju.","administrative request","formal"],["Zahtjev podnesite do navedenog roka.","formal instruction","formal"]]),
    p("academic_c1","C1","Academic discussion",[["Dostupni podaci podržavaju ovaj zaključak.","presenting evidence","academic"],["Ovaj pristup ima određena ograničenja.","qualifying an argument","academic"]]),
    p("administration_c1","C1","Administration",[["Molimo vas da postupite prema pravilniku.","official instruction","formal"],["Dokumentacija treba biti dostavljena u roku.","formal requirement","formal"]]),
    p("public_c2","C2","Public discourse",[["O ovom pitanju postoje različiti stavovi.","framing a debate","formal"],["Za ovu tvrdnju nema dovoljno dokaza.","challenging a claim","formal"]]),
    p("literary_c2","C2","Literary analysis",[["Ova metafora naglašava prolaznost vremena.","literary analysis","literary"],["Izraz dobija drugačiju nijansu u ovom kontekstu.","interpreting nuance","literary"]]),
]

def u(level,n,title,grammar,vocab,c1,c2):
    return CurriculumUnit(id=f"bs-{level.lower()}-{n}",level=level,unit_number=n,title=title,grammar_points=grammar,vocabulary_set_ids=[vocab],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=[c1,c2],default_weeks=2)

CURRICULUM = {}
CURRICULUM["A1"] = [
    u("A1",1,"Pozdravi i predstavljanje",["pronouns","gender"],"greetings_a1","Handle A1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A1",2,"Porodica i ljudi",["gender","present"],"family_a1","Handle A1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A1",3,"Dom i mjesta",["present","questions"],"home_a1","Handle A1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A1",4,"Svakodnevni život",["questions","negation"],"daily_a1","Handle A1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A1",5,"Hrana i kupovina",["negation","possessives"],"food_a1","Handle A1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A1",6,"Grad i pravci",["possessives","location"],"places_a1","Handle A1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A1",7,"Razgovor i pomoć",["location","imperative"],"greetings_a1","Handle A1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A1",8,"Ponavljanje A1",["imperative","pronouns"],"family_a1","Handle A1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
]
CURRICULUM["A2"] = [
    u("A2",1,"Vrijeme i planovi",["cases","past"],"time_a2","Handle A2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A2",2,"Putovanje",["past","future"],"travel_a2","Handle A2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A2",3,"Zdravlje",["future","aspect"],"health_a2","Handle A2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A2",4,"Usluge",["aspect","comparatives"],"daily_a1","Handle A2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A2",5,"Iskustva i poređenje",["comparatives","modality"],"time_a2","Handle A2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A2",6,"Ljubaznost i zahtjevi",["modality","relative"],"travel_a2","Handle A2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A2",7,"Prošlost i budućnost",["relative","purpose_cause"],"health_a2","Handle A2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("A2",8,"Ponavljanje A2",["purpose_cause","cases"],"daily_a1","Handle A2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
]
CURRICULUM["B1"] = [
    u("B1",1,"Obrazovanje",["conditional","reported"],"education_b1","Handle B1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B1",2,"Posao",["reported","passive"],"work_b1","Handle B1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B1",3,"Uzrok i cilj",["passive","reflexive"],"education_b1","Handle B1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B1",4,"Uslovi i planovi",["reflexive","connectors"],"work_b1","Handle B1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B1",5,"Relativne rečenice",["connectors","concession"],"education_b1","Handle B1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B1",6,"Izvještavanje",["concession","subordination"],"work_b1","Handle B1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B1",7,"Problemi i rješenja",["subordination","modality"],"education_b1","Handle B1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B1",8,"Ponavljanje B1",["modality","conditional"],"work_b1","Handle B1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
]
CURRICULUM["B2"] = [
    u("B2",1,"Pasiv i službeni jezik",["nominalization","hedging"],"society_b2","Handle B2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B2",2,"Društvo",["hedging","embedded_questions"],"environment_b2","Handle B2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B2",3,"Okoliš",["embedded_questions","formal_admin"],"technology_b2","Handle B2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B2",4,"Tehnologija",["formal_admin","academic_argument"],"society_b2","Handle B2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B2",5,"Dokazi i zaključci",["academic_argument","information_structure"],"environment_b2","Handle B2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B2",6,"Kontrast i ustupanje",["information_structure","register"],"technology_b2","Handle B2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B2",7,"Mediji",["register","pragmatics"],"society_b2","Handle B2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("B2",8,"Ponavljanje B2",["pragmatics","nominalization"],"environment_b2","Handle B2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
]
CURRICULUM["C1"] = [
    u("C1",1,"Formalni jezik",["rhetoric","translation"],"economy_c1","Handle C1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C1",2,"Akademsko pisanje",["translation","discourse_analysis"],"governance_c1","Handle C1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C1",3,"Složene rečenice",["discourse_analysis","nominalization"],"academic_c1","Handle C1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C1",4,"Administracija",["nominalization","hedging"],"economy_c1","Handle C1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C1",5,"Argumentacija",["hedging","academic_argument"],"governance_c1","Handle C1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C1",6,"Struktura informacija",["academic_argument","information_structure"],"academic_c1","Handle C1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C1",7,"Pragmatika",["information_structure","formal_admin"],"economy_c1","Handle C1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C1",8,"Ponavljanje C1",["formal_admin","rhetoric"],"governance_c1","Handle C1 Bosnian in this topic","Use connected Bosnian with appropriate register"),
]
CURRICULUM["C2"] = [
    u("C2",1,"Javni diskurs",["rhetoric","literary"],"media_c2","Handle C2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C2",2,"Retorika",["literary","translation"],"literary_c2","Handle C2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C2",3,"Prevođenje",["translation","discourse_analysis"],"academic_c1","Handle C2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C2",4,"Analiza diskursa",["discourse_analysis","pragmatics"],"media_c2","Handle C2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C2",5,"Književni stil",["pragmatics","register"],"literary_c2","Handle C2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C2",6,"Profesionalni registar",["register","academic_argument"],"academic_c1","Handle C2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C2",7,"Sinteza izvora",["academic_argument","information_structure"],"media_c2","Handle C2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
    u("C2",8,"Ponavljanje C2",["information_structure","rhetoric"],"literary_c2","Handle C2 Bosnian in this topic","Use connected Bosnian with appropriate register"),
]

ASSESSMENT_BANK = [
    AssessmentQuestion(id="bs-a1-001",skill="vocabulary",difficulty="A1",question="What does hvala mean?",options=["thank you","hello","water","friend"],correct="thank you"),
    AssessmentQuestion(id="bs-a1-002",skill="grammar",difficulty="A1",question="Which sentence is negative?",options=["Ne razumijem.","Razumijem.","Razumijete.","Razumio sam."],correct="Ne razumijem."),
    AssessmentQuestion(id="bs-a2-003",skill="grammar",difficulty="A2",question="Which case is used after s in 's prijateljem'?",options=["instrumental","nominative","accusative","genitive"],correct="instrumental"),
    AssessmentQuestion(id="bs-a2-004",skill="vocabulary",difficulty="A2",question="What does rezervacija mean?",options=["reservation","medicine","market","office"],correct="reservation"),
    AssessmentQuestion(id="bs-b1-005",skill="grammar",difficulty="B1",question="Which expresses a hypothetical condition?",options=["Kad bih znao, rekao bih.","Znam odgovor.","Rekao je odgovor.","Odgovaram sada."],correct="Kad bih znao, rekao bih."),
    AssessmentQuestion(id="bs-b1-006",skill="grammar",difficulty="B1",question="Which is passive?",options=["Izvještaj je napisan.","Pišem izvještaj.","Izvještaj pišem.","Izvještaj je važan."],correct="Izvještaj je napisan."),
    AssessmentQuestion(id="bs-b2-007",skill="academic",difficulty="B2",question="Which uses hedging?",options=["Moguće je da će rezultat biti drugačiji.","Rezultat je uvijek isti.","Zdravo!","Knjiga je na stolu."],correct="Moguće je da će rezultat biti drugačiji."),
    AssessmentQuestion(id="bs-b2-008",skill="formal",difficulty="B2",question="Which is formal administrative language?",options=["Molimo vas da dostavite potrebnu dokumentaciju.","Gdje si?","Vidimo se sutra.","Daj mi to."],correct="Molimo vas da dostavite potrebnu dokumentaciju."),
    AssessmentQuestion(id="bs-c1-009",skill="academic",difficulty="C1",question="Which presents evidence?",options=["Dostupni podaci podržavaju ovaj zaključak.","Dođi ovamo.","Kako si?","Ovo je moja kuća."],correct="Dostupni podaci podržavaju ovaj zaključak."),
    AssessmentQuestion(id="bs-c1-010",skill="grammar",difficulty="C1",question="Which is an embedded question?",options=["Ne znam kada će sastanak početi.","Sastanak počinje.","Sastanak je dug.","Počni sastanak."],correct="Ne znam kada će sastanak početi."),
    AssessmentQuestion(id="bs-c2-011",skill="discourse",difficulty="C2",question="Which sentence signals contrast?",options=["Ipak, zaključak se temelji na ograničenim podacima.","Zdravo!","Moja kuća je velika.","Stanica je blizu."],correct="Ipak, zaključak se temelji na ograničenim podacima."),
    AssessmentQuestion(id="bs-c2-012",skill="translation",difficulty="C2",question="What should precise translation preserve?",options=["case, aspect, register and discourse meaning","word order only","number of words only","punctuation only"],correct="case, aspect, register and discourse meaning"),
]

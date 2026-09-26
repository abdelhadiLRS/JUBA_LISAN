"""Danish A1-C2 language foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]
_G=[
("pronouns","Personal pronouns","A1","grammar","Jeg er studerende."),
("word_order","Basic word order","A1","syntax","Jeg bor i København."),
("present","Present tense","A1","verbs","Jeg lærer dansk."),
("questions","Questions","A1","syntax","Hvor bor du?"),
("negation","Negation","A1","grammar","Jeg forstår ikke."),
("articles","Definite and indefinite nouns","A1","grammar","Det er en bog."),
("possession","Possessives","A1","grammar","Det er min bog."),
("location","Prepositions of place","A1","syntax","Bogen ligger på bordet."),
("past","Past tense","A2","verbs","Jeg arbejdede i går."),
("future","Future and intention","A2","verbs","Jeg vil rejse i morgen."),
("imperative","Imperatives","A2","verbs","Kom her, tak."),
("modal","Modal verbs","A2","modality","Jeg skal arbejde."),
("comparative","Comparison","A2","syntax","Denne bog er bedre."),
("perfect","Perfect tense","A2","verbs","Jeg har spist."),
("reflexive","Reflexive verbs","A2","grammar","Jeg glæder mig."),
("subordination","Subordinate clauses","A2","syntax","Når jeg kommer, ringer jeg."),
("relative","Relative clauses","B1","syntax","Manden, som bor her, er læge."),
("conditional","Conditional meaning","B1","syntax","Hvis jeg har tid, kommer jeg."),
("reported","Reported speech","B1","discourse","Hun siger, at hun kommer."),
("causal","Cause and reason","B1","syntax","Jeg bliver hjemme, fordi jeg er syg."),
("purpose","Purpose clauses","B1","syntax","Jeg læser for at lære."),
("concession","Concession","B1","syntax","Selvom det regner, går vi ud."),
("passive","Passive voice","B2","grammar","Døren blev åbnet."),
("causative","Causative constructions","B2","grammar","Jeg får bilen repareret."),
("pluperfect","Pluperfect","B2","verbs","Han var allerede gået."),
("indirect_questions","Embedded questions","B2","syntax","Jeg ved ikke, hvor han bor."),
("discourse","Discourse connectors","B2","discourse","Derfor er resultatet vigtigt."),
("nominalization","Nominalization","C1","academic","Undersøgelsen viser en ændring."),
("hedging","Academic hedging","C1","academic","Det tyder på, at resultatet er vigtigt."),
("information_structure","Information structure","C1","discourse","Det er netop dette problem, vi undersøger."),
("register","Formal register","C1","register","Vi skal hermed informere om ændringen."),
("argumentation","Academic argumentation","C2","discourse","På denne baggrund kan man konkludere, at..."),
("pragmatics","Pragmatics and politeness","C2","pragmatics","Hvis De har mulighed for det, må De gerne kontakte os."),
("rhetoric","Rhetorical nuance","C2","rhetoric","Det er værd at bemærke, at spørgsmålet er komplekst."),
("discourse_analysis","Advanced discourse analysis","C2","discourse","Argumentet må forstås i en bredere samfundsmæssig sammenhæng."),
]
GRAMMAR_TOPICS=[GrammarTopic(slug=s,title=t,level=l,category=c,summary=f"Use {t.lower()} accurately in Danish.",explanation=f"Develop natural Danish control of {t.lower()} at {l}.",examples=[GrammarExample(text=e)]) for s,t,l,c,e in _G]

_V=[
("greetings_a1","Greetings","A1",[("Hej","phrase","hello","Hej, hvordan har du det?"),("tak","phrase","thank you","Tak for hjælpen."),("farvel","phrase","goodbye","Farvel og på gensyn."),("undskyld","phrase","sorry","Undskyld, må jeg spørge?")]),
("identity_a1","Identity","A1",[("navn","noun","name","Mit navn er Anna."),("elev","noun","student","Jeg er elev."),("lærer","noun","teacher","Hun er lærer."),("ven","noun","friend","Han er min ven.")]),
("family_a1","Family","A1",[("mor","noun","mother","Min mor bor her."),("far","noun","father","Min far arbejder."),("søster","noun","sister","Min søster læser."),("bror","noun","brother","Min bror er hjemme.")]),
("home_a1","Home","A1",[("hus","noun","house","Vores hus er stort."),("værelse","noun","room","Mit værelse er lyst."),("dør","noun","door","Døren er åben."),("bord","noun","table","Bogen ligger på bordet.")]),
("daily_a1","Daily life","A1",[("morgen","noun","morning","Godmorgen!"),("dag","noun","day","I dag arbejder jeg."),("arbejde","noun","work","Jeg går på arbejde."),("vand","noun","water","Jeg drikker vand.")]),
("food_a1","Food and drink","A1",[("brød","noun","bread","Jeg spiser brød."),("kaffe","noun","coffee","Jeg drikker kaffe."),("mælk","noun","milk","Mælken er kold."),("æble","noun","apple","Jeg spiser et æble.")]),
("places_a1","Places","A1",[("skole","noun","school","Skolen ligger her."),("butik","noun","shop","Butikken er åben."),("hospital","noun","hospital","Hospitalet ligger i byen."),("vej","noun","road","Vejen er lang.")]),
("communication_a1","Basic communication","A1",[("spørgsmål","noun","question","Jeg har et spørgsmål."),("hjælp","noun","help","Jeg har brug for hjælp."),("sprog","noun","language","Dansk er et sprog."),("forstå","verb","understand","Jeg forstår dansk.")]),
("shopping_a2","Shopping","A2",[("pris","noun","price","Hvad er prisen?"),("størrelse","noun","size","Hvilken størrelse vil du have?"),("købe","verb","buy","Jeg vil købe den."),("billig","adjective","cheap","Den er billig.")]),
("travel_a2","Travel","A2",[("rejse","noun","trip","Vi planlægger en rejse."),("billet","noun","ticket","Jeg har en billet."),("station","noun","station","Hvor ligger stationen?"),("hotel","noun","hotel","Hotellet er centralt.")]),
("health_a2","Health","A2",[("sundhed","noun","health","Sundhed er vigtigt."),("smerte","noun","pain","Jeg har smerter."),("læge","noun","doctor","Jeg skal til lægen."),("medicin","noun","medicine","Jeg tager medicin.")]),
("weather_a2","Weather","A2",[("regn","noun","rain","Det regner."),("sne","noun","snow","Det sner."),("varm","adjective","warm","Det er varmt."),("kold","adjective","cold","Det er koldt.")]),
("study_a2","Study","A2",[("lektie","noun","homework","Jeg laver mine lektier."),("eksamen","noun","exam","Jeg har eksamen i morgen."),("bog","noun","book","Jeg læser en bog."),("lære","verb","learn","Jeg lærer dansk.")]),
("work_a2","Work","A2",[("kontor","noun","office","Jeg arbejder på et kontor."),("kollega","noun","colleague","Min kollega kommer snart."),("møde","noun","meeting","Vi har et møde."),("projekt","noun","project","Projektet er vigtigt.")]),
("transport_a2","Transport","A2",[("bus","noun","bus","Jeg tager bussen."),("tog","noun","train","Toget kommer klokken otte."),("bil","noun","car","Vi har en bil."),("lufthavn","noun","airport","Lufthavnen ligger uden for byen.")]),
("society_b1","Society","B1",[("samfund","noun","society","Samfundet ændrer sig."),("borger","noun","citizen","Alle borgere har rettigheder."),("rettighed","noun","right","Mennesker har rettigheder."),("ansvar","noun","responsibility","Det er et stort ansvar.")]),
("environment_b1","Environment","B1",[("miljø","noun","environment","Vi skal beskytte miljøet."),("natur","noun","nature","Naturen er vigtig."),("forurening","noun","pollution","Forurening er et problem."),("ressource","noun","resource","Vand er en vigtig ressource.")]),
("media_b1","Media","B1",[("nyhed","noun","news","Jeg læser nyhederne."),("avis","noun","newspaper","Avisen udkommer hver dag."),("kilde","noun","source","Kilden er pålidelig."),("debat","noun","debate","Der er en offentlig debat.")]),
("culture_b1","Culture","B1",[("kultur","noun","culture","Kultur forbinder mennesker."),("litteratur","noun","literature","Jeg læser dansk litteratur."),("kunst","noun","art","Kunst er en del af kulturen."),("arv","noun","heritage","Kulturarven skal bevares.")]),
("technology_b1","Technology","B1",[("teknologi","noun","technology","Teknologi ændrer vores hverdag."),("data","noun","data","Data skal beskyttes."),("netværk","noun","network","Netværket fungerer godt."),("sikkerhed","noun","security","Digital sikkerhed er vigtig.")]),
]
VOCABULARY_SETS=[VocabularySet(id=i,level=l,topic=t,unit_ref=f"da-{l.lower()}-unit-{((n-1)%8)+1}",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words]) for n,(i,t,l,words) in enumerate(_V,1)]

PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="greetings",level="A1",situation="Greetings",icon="👋",phrases=[PhrasebookEntry(text="Hej!",context="greeting",register="neutral"),PhrasebookEntry(text="Hvordan har du det?",context="asking how someone is",register="neutral"),PhrasebookEntry(text="På gensyn!",context="farewell",register="neutral")]),
PhrasebookCategory(id="courtesy",level="A1",situation="Courtesy",icon="🙏",phrases=[PhrasebookEntry(text="Tak skal du have.",context="thanks",register="neutral"),PhrasebookEntry(text="Undskyld.",context="apology",register="polite"),PhrasebookEntry(text="Værsgo.",context="offering something",register="neutral")]),
PhrasebookCategory(id="shopping",level="A2",situation="Shopping",icon="🛒",phrases=[PhrasebookEntry(text="Hvad koster den?",context="asking price",register="neutral"),PhrasebookEntry(text="Jeg vil gerne købe den.",context="buying",register="polite"),PhrasebookEntry(text="Har I en større størrelse?",context="asking for size",register="neutral")]),
PhrasebookCategory(id="directions",level="A2",situation="Directions",icon="🧭",phrases=[PhrasebookEntry(text="Hvor ligger stationen?",context="asking location",register="neutral"),PhrasebookEntry(text="Hvordan kommer jeg til centrum?",context="asking directions",register="neutral"),PhrasebookEntry(text="Er det til højre?",context="checking direction",register="neutral")]),
PhrasebookCategory(id="travel",level="A2",situation="Travel",icon="✈️",phrases=[PhrasebookEntry(text="Jeg vil gerne købe en billet.",context="buying ticket",register="polite"),PhrasebookEntry(text="Hvornår går toget?",context="departure time",register="neutral"),PhrasebookEntry(text="Hvor ligger hotellet?",context="finding hotel",register="neutral")]),
PhrasebookCategory(id="health",level="A2",situation="Health",icon="🩺",phrases=[PhrasebookEntry(text="Jeg har det ikke godt.",context="feeling unwell",register="neutral"),PhrasebookEntry(text="Jeg har ondt i hovedet.",context="describing pain",register="neutral"),PhrasebookEntry(text="Hvor er lægen?",context="finding doctor",register="neutral")]),
PhrasebookCategory(id="work",level="A2",situation="Work",icon="💼",phrases=[PhrasebookEntry(text="Jeg arbejder på kontor.",context="work",register="neutral"),PhrasebookEntry(text="Kan du sende dokumentet?",context="request",register="polite"),PhrasebookEntry(text="Hvornår er mødet?",context="meeting time",register="neutral")]),
PhrasebookCategory(id="study",level="A2",situation="Study",icon="📚",phrases=[PhrasebookEntry(text="Hvad betyder dette ord?",context="asking meaning",register="neutral"),PhrasebookEntry(text="Kan du gentage det?",context="asking to repeat",register="polite"),PhrasebookEntry(text="Jeg øver mig på dansk.",context="language learning",register="neutral")]),
PhrasebookCategory(id="social",level="B1",situation="Social conversation",icon="💬",phrases=[PhrasebookEntry(text="Hvad synes du?",context="asking opinion",register="neutral"),PhrasebookEntry(text="Jeg er enig.",context="agreeing",register="neutral"),PhrasebookEntry(text="Jeg er ikke helt enig.",context="polite disagreement",register="polite")]),
PhrasebookCategory(id="formal",level="B2",situation="Formal communication",icon="🏛️",phrases=[PhrasebookEntry(text="Vi vil gerne informere Dem om...",context="formal information",register="formal"),PhrasebookEntry(text="Med venlig hilsen",context="formal closing",register="formal"),PhrasebookEntry(text="I henhold til...",context="formal reference",register="formal")]),
PhrasebookCategory(id="academic",level="C1",situation="Academic discussion",icon="🎓",phrases=[PhrasebookEntry(text="Resultaterne tyder på, at...",context="evidence",register="academic"),PhrasebookEntry(text="På denne baggrund kan man konkludere, at...",context="conclusion",register="academic"),PhrasebookEntry(text="Det er muligt, at...",context="hedging",register="academic")]),
PhrasebookCategory(id="professional",level="C1",situation="Professional negotiation",icon="🤝",phrases=[PhrasebookEntry(text="Vi foreslår, at...",context="proposal",register="formal"),PhrasebookEntry(text="Kan vi genoverveje dette punkt?",context="negotiation",register="polite"),PhrasebookEntry(text="Lad os fokusere på de vigtigste spørgsmål.",context="agenda",register="professional")]),
PhrasebookCategory(id="advanced",level="C2",situation="Advanced discourse",icon="🗣️",phrases=[PhrasebookEntry(text="Ikke desto mindre er spørgsmålet komplekst.",context="qualified contrast",register="formal"),PhrasebookEntry(text="Dette argument bør ses i en bredere samfundsmæssig sammenhæng.",context="contextualizing argument",register="academic"),PhrasebookEntry(text="Hvis De tillader det, vil jeg gerne fremsætte et forslag.",context="polite advanced suggestion",register="formal")]),
]
_TOPICS={
"A1":["pronouns","word_order","present","questions","negation","articles","possession","location"],
"A2":["past","future","imperative","modal","comparative","perfect","reflexive","subordination"],
"B1":["relative","conditional","reported","causal","purpose","concession","relative","reported"],
"B2":["passive","causative","pluperfect","indirect_questions","discourse","conditional","passive","causative"],
"C1":["nominalization","hedging","information_structure","register","argumentation","hedging","register","nominalization"],
"C2":["argumentation","pragmatics","rhetoric","discourse_analysis","information_structure","register","argumentation","rhetoric"],
}
_TITLES={
"A1":["Personlig information","Ordstilling","Hverdagsverber","Spørgsmål","Nægtelse","Navneord","Ejerskab","Sted og retning"],
"A2":["Fortid","Fremtid","Anmodninger","Modalverber","Sammenligning","Perfektum","Refleksive verber","Ledsætninger"],
"B1":["Relative sætninger","Betingelser","Refereret tale","Årsag","Formål","Indrømmelse","Beskrivelser","Refereret information"],
"B2":["Passiv","Kausativ","Pluskvamperfektum","Indirekte spørgsmål","Tekstbinding","Komplekse betingelser","Passiv i formelle tekster","Kausative mønstre"],
"C1":["Nominalisering","Akademisk forsigtighed","Informationsstruktur","Formelt register","Argumentation","Nuanceret forsigtighed","Institutionelt sprog","Akademisk formulering"],
"C2":["Avanceret argumentation","Pragmatik","Retorisk nuance","Diskursanalyse","Informationsstruktur","Register og stil","Kompleks argumentation","Avanceret retorik"],
}
_UNITS=[]
for level in LEVELS:
 for i,slug in enumerate(_TOPICS[level],1):
  _UNITS.append(CurriculumUnit(id=f"da-{level.lower()}-unit-{i}",level=level,unit_number=i,title=_TITLES[level][i-1],grammar_points=[slug],vocabulary_set_ids=[VOCABULARY_SETS[((i-1)%len(VOCABULARY_SETS))].id],lesson_types=["grammar","vocabulary","speaking","listening","reading","writing","review"],competency_checklist=["Understand the target Danish structure","Use it in a guided exchange","Produce a level-appropriate response"],default_weeks=2))
CURRICULUM={level:[u for u in _UNITS if u.level==level] for level in LEVELS}

ASSESSMENT_BANK=[
AssessmentQuestion(id="da-a1-001",skill="vocabulary",difficulty="A1",question="What does “Hej” mean?",options=["Hello","Goodbye","Book","Water"],correct="Hello"),
AssessmentQuestion(id="da-a1-002",skill="grammar",difficulty="A1",question="Which sentence means “I am a student”?",options=["Jeg er studerende.","Jeg er en bog.","Jeg er hjemme.","Jeg er vand."],correct="Jeg er studerende."),
AssessmentQuestion(id="da-a2-001",skill="grammar",difficulty="A2",question="Which sentence refers to yesterday?",options=["Jeg arbejdede i går.","Jeg vil rejse i morgen.","Jeg lærer dansk.","Hej!"],correct="Jeg arbejdede i går."),
AssessmentQuestion(id="da-a2-002",skill="communication",difficulty="A2",question="Which phrase asks the price?",options=["Hvad koster den?","Hvor ligger stationen?","Hvordan har du det?","Farvel!"],correct="Hvad koster den?"),
AssessmentQuestion(id="da-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["Hvis jeg har tid, kommer jeg.","Jeg drikker kaffe.","Det regner.","Hej!"],correct="Hvis jeg har tid, kommer jeg."),
AssessmentQuestion(id="da-b1-002",skill="reading",difficulty="B1",question="Which connector introduces a reason?",options=["fordi","i morgen","tak","farvel"],correct="fordi"),
AssessmentQuestion(id="da-b2-001",skill="grammar",difficulty="B2",question="Which sentence uses passive voice?",options=["Døren blev åbnet.","Jeg åbnede døren.","Jeg åbner døren.","Jeg vil åbne døren."],correct="Døren blev åbnet."),
AssessmentQuestion(id="da-b2-002",skill="grammar",difficulty="B2",question="Which phrase contains an embedded question?",options=["Jeg ved ikke, hvor han bor.","Han bor her.","Han kommer i morgen.","Jeg læser."],correct="Jeg ved ikke, hvor han bor."),
AssessmentQuestion(id="da-c1-001",skill="academic",difficulty="C1",question="Which phrase appropriately hedges a claim?",options=["Det tyder på, at resultatet er vigtigt.","Det er altid sandt.","Hej!","Kom her!"],correct="Det tyder på, at resultatet er vigtigt."),
AssessmentQuestion(id="da-c1-002",skill="academic",difficulty="C1",question="Which phrase introduces a formal conclusion?",options=["På denne baggrund kan man konkludere, at...","Hvad koster den?","Tak!","Hvor bor du?"],correct="På denne baggrund kan man konkludere, at..."),
AssessmentQuestion(id="da-c2-001",skill="pragmatics",difficulty="C2",question="Which is a formal polite request?",options=["Hvis De tillader det, vil jeg gerne fremsætte et forslag.","Giv mig den!","Hej!","Jeg er træt."],correct="Hvis De tillader det, vil jeg gerne fremsætte et forslag."),
AssessmentQuestion(id="da-c2-002",skill="discourse",difficulty="C2",question="Which phrase provides a qualified contrast?",options=["Ikke desto mindre er spørgsmålet komplekst.","Jeg drikker vand.","Godmorgen!","Hvor er toget?"],correct="Ikke desto mindre er spørgsmålet komplekst."),
AssessmentQuestion(id="da-c2-003",skill="academic",difficulty="C2",question="Which phrase contextualizes an argument?",options=["Dette argument bør ses i en bredere samfundsmæssig sammenhæng.","Jeg vil have kaffe.","Tak.","Hvor er stationen?"],correct="Dette argument bør ses i en bredere samfundsmæssig sammenhæng."),
AssessmentQuestion(id="da-c2-004",skill="rhetoric",difficulty="C2",question="Which phrase signals rhetorical nuance?",options=["Det er værd at bemærke, at spørgsmålet er komplekst.","Jeg er hjemme.","Hej.","Jeg læser."],correct="Det er værd at bemærke, at spørgsmålet er komplekst."),
]

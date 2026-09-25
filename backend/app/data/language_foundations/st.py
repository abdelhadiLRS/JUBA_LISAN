"""Southern Sotho (Sesotho) foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

def _g(slug, title, level, summary, examples):
    return GrammarTopic(slug=slug, title=title, level=level, category="grammar",
        summary=summary, explanation=summary, examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS = [
_g("st-a1-g1","Pronouns and subject concords","A1","Use personal pronouns and basic subject concords.",["Ke moithuti.","U mosuoe."]),
_g("st-a1-g2","Copulative identity","A1","Identify people and things with ke.",["Ke tichere.","Ena ke buka."]),
_g("st-a1-g3","Present tense","A1","Describe current and habitual actions.",["Ke a ithuta.","O sebetsa sekolong."]),
_g("st-a1-g4","Negation","A1","Negate basic verbal and nominal clauses.",["Ha ke tsebe.","Ha se buka."]),
_g("st-a1-g5","Questions","A1","Ask basic information and yes-no questions.",["U hokae?","Lebitso la hao ke mang?"]),
_g("st-a1-g6","Possession","A1","Express possession with agreeing possessives.",["Buka ea ka e teng.","Ntlo ea rona e kholo."]),
_g("st-a1-g7","Locatives","A1","Express location and destination.",["Ke lapeng.","Ke ea sekolong."]),
_g("st-a1-g8","Noun classes and plurals","A1","Recognize common noun-class pairs and agreement.",["motho / batho","ngoana / bana"]),
_g("st-a2-g1","Noun-class agreement","A2","Match adjectives and verbs with noun classes.",["Ngoana e monyenyane oa bapala.","Bana ba banyenyane baa bapala."]),
_g("st-a2-g2","Past tense","A2","Talk about completed events.",["Ke ile sekolong maobane.","O rekile lijo."]),
_g("st-a2-g3","Future and intention","A2","Express future plans and intentions.",["Ke tla ithuta hosane.","Re tla ea Maseru."]),
_g("st-a2-g4","Object marking","A2","Use object forms in transitive clauses.",["Ke a mo bona.","Ke rata Sesotho."]),
_g("st-a2-g5","Adjectives and agreement","A2","Describe people and objects accurately.",["Ntlo e kholo.","Matlo a maholo."]),
_g("st-a2-g6","Comparatives","A2","Compare qualities and quantities.",["O moholo ho feta nna.","Ena e ntle haholo."]),
_g("st-a2-g7","Imperatives and polite requests","A2","Give instructions and make polite requests.",["Tloo mona.","Ka kopo, lula fatše."]),
_g("st-a2-g8","Time and frequency","A2","Express time, duration and frequency.",["Ke ithuta letsatsi le leng le le leng.","O fihlile maobane."]),
_g("st-b1-g1","Relative clauses","B1","Modify nouns with relative constructions.",["Motho ea tlileng ke ntate.","Buka eo ke e balileng e ncha."]),
_g("st-b1-g2","Conditionals","B1","Express conditions and consequences.",["Haeba u ithuta, u tla pasa.","Ha pula e na, re lula lapeng."]),
_g("st-b1-g3","Infinitives and purpose","B1","Use infinitives to discuss activities and purpose.",["Ke rata ho ithuta.","O ile ho reka lijo."]),
_g("st-b1-g4","Causative constructions","B1","Express causing another action.",["Mosuoe o ruta bana.","O ile a mpelisa mosebetsi."]),
_g("st-b1-g5","Passive voice","B1","Foreground affected participants with passive forms.",["Buka e baliloe ke moithuti.","Ntlo e hahiloe selemong se fetileng."]),
_g("st-b1-g6","Aspect and event structure","B1","Distinguish ongoing, habitual and completed events.",["Ke ntse ke ithuta.","Ke qetile ho ja."]),
_g("st-b1-g7","Cause, purpose and result","B1","Connect clauses by reason, purpose and consequence.",["O liehile ka lebaka la pula.","O tlile ho ithuta."]),
_g("st-b1-g8","Reported speech","B1","Report statements, questions and instructions.",["O itse o tla tla.","O mpotse hore na ke tla ea."]),
_g("st-b2-g1","Complex subordination","B2","Build multi-clause sentences with precise relations.",["Le hoja a ne a khathetse, o ile a tsoela pele ho sebetsa."]),
_g("st-b2-g2","Concession and contrast","B2","Express concession, contrast and qualification.",["Le hoja ho le thata, re tla tsoela pele."]),
_g("st-b2-g3","Cohesion and reference","B2","Maintain reference across extended discourse.",["Morero oo re buileng ka oona o phethetsoe."]),
_g("st-b2-g4","Discourse connectors","B2","Organize arguments with causal and contrastive markers.",["Ka lebaka leo, re lokela ho itokisetsa hantle."]),
_g("st-b2-g5","Focus and information structure","B2","Highlight topic, focus and contrastive information.",["Seo ke se batlang ke khotso.","Kajeno ke moo re qalileng teng."]),
_g("st-b2-g6","Nominalization","B2","Turn events into noun-like expressions for formal discourse.",["Ho ithuta Sesotho ho hloka nako."]),
_g("st-b2-g7","Modality and stance","B2","Express obligation, possibility and certainty.",["Ho ka etsahala hore a tle.","O tlameha ho e etsa."]),
_g("st-b2-g8","Register and politeness","B2","Adapt wording to social and professional contexts.",["Na le ka mpolella moo ofisi e leng teng, ka kopo?"]),
_g("st-c1-g1","Formal and institutional Sesotho","C1","Handle formal administrative and institutional language.",["Seboka se tla tšoaroa ka Mantaha ho hlahloba leano le lecha."]),
_g("st-c1-g2","Academic argumentation","C1","Present claims, evidence, qualifications and conclusions.",["Patlisiso e bontša hore thuto e kenya letsoho haholo nts'etsopele."]),
_g("st-c1-g3","Academic hedging","C1","Qualify claims with appropriate epistemic caution.",["Ho ka etsahala hore liphetho li itšetlehe ka sebopeho sa sehlopha."]),
_g("st-c1-g4","Embedded questions","C1","Integrate questions into complex sentences.",["Ke batla ho tseba hore na morero o phethetsoe."]),
_g("st-c1-g5","Information packaging","C1","Manage information flow in formal prose.",["Taba ea bohlokoa ke mokhoa oo re ka ntlafatsang boleng ba litšebeletso ka oona."]),
_g("st-c1-g6","Media and public discourse","C1","Produce precise public-facing language.",["Tlaleho e ncha e phatlalalitsoe kajeno."]),
_g("st-c1-g7","Idiomatic and pragmatic meaning","C1","Interpret implication, idioms and culturally appropriate wording.",["Bonngoe ke matla a etsang hore mosebetsi o tsoele pele hantle."]),
_g("st-c1-g8","Professional correspondence","C1","Write concise formal requests and responses.",["Re le kopa hore le re romelle litokomane tse hlokahalang pele ho letsatsi la ho qetela."]),
_g("st-c2-g1","Advanced discourse cohesion","C2","Control long-range reference and rhetorical progression.",["Le hoja tlaleho e bontša tsoelo-pele, e boetse e bontša liphephetso tse hlokang tharollo e tšoarellang."]),
_g("st-c2-g2","Nuanced modality","C2","Express subtle degrees of certainty, obligation and evaluation.",["E ke ke ea e-ba ho feteletsa litaba ho re leano lena le ka ba le litlamorao tsa nako e telele."]),
_g("st-c2-g3","Complex nominalization","C2","Compress propositions for academic and institutional prose.",["Tlhahlobo ea liphetho tsa lipatlisiso e entse hore ho nkoe qeto e ncha."]),
_g("st-c2-g4","Rhetorical organization","C2","Control emphasis, concession and counterargument.",["Le hoja tharollo ena e na le melemo, bothata bo ka sehloohong ke ho e phethahatsa."]),
_g("st-c2-g5","Legal and administrative formulation","C2","Interpret precise obligations and procedural language.",["Mokopi o tlameha ho fana ka litokomane tsohle tse hlokahalang ho latela melao."]),
_g("st-c2-g6","Translation precision","C2","Preserve meaning, register and pragmatic force across languages.",["Phetolelo e lokela ho boloka moelelo le mokhoa oa puo ea pele."]),
_g("st-c2-g7","Literary and rhetorical style","C2","Interpret figurative language and deliberate stylistic choices.",["Puo ea mongoli e haha setšoantšo sa bophelo ba sechaba."]),
_g("st-c2-g8","Discourse analysis and register shifting","C2","Shift deliberately among conversational, professional and academic styles.",["Puo ea letsatsi le letsatsi e fapane le puo ea sengoloa sa lipatlisiso."]),
]


def _v(id_, level, topic, unit, entries):
    return VocabularySet(id=id_, level=level, topic=topic, unit_ref=unit,
        words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in entries])

VOCABULARY_SETS = [
_v("greetings_a1","A1","greetings","st-a1-unit-1",[("lumela","phrase","hello","Lumela, ntate."),("kea leboha","phrase","thank you","Kea leboha haholo."),("hoseng","noun","morning","Hoseng ho monate.")]),
_v("identity_a1","A1","identity","st-a1-unit-2",[("lebitso","noun","name","Lebitso la ka ke Thabo."),("moithuti","noun","student","Ke moithuti."),("tichere","noun","teacher","Ke tichere.")]),
_v("family_a1","A1","family","st-a1-unit-3",[("mme","noun","mother","Mme o lapeng."),("ntate","noun","father","Ntate o mosebetsing."),("ngoana","noun","child","Ngoana o sekolong.")]),
_v("home_a1","A1","home","st-a1-unit-4",[("ntlo","noun","house","Ntlo e kholo."),("kamore","noun","room","Kamore e hloekile."),("monyako","noun","door","Monyako o butsoe.")]),
_v("routine_a1","A1","routine","st-a1-unit-5",[("ithuta","verb","to study","Ke ithuta letsatsi le leng le le leng."),("sebetsa","verb","to work","Ke sebetsa letsatsi le letsatsi."),("robala","verb","to sleep","Ke robala bosiu.")]),
_v("time_a1","A1","time","st-a1-unit-6",[("nako","noun","time","Ke nako mang?"),("kajeno","adverb","today","Kajeno ke lapeng."),("hosane","adverb","tomorrow","Hosane ke ea sekolong.")]),
_v("food_a1","A1","food","st-a1-unit-7",[("metsi","noun","water","Ke batla metsi."),("bohobe","noun","bread","Ke ja bohobe."),("lebese","noun","milk","Ke noa lebese.")]),
_v("places_a1","A1","places","st-a1-unit-8",[("sekolo","noun","school","Ke sekolong."),("mmaraka","noun","market","Mmaraka o haufi."),("ofisi","noun","office","O ka ofising.")]),
_v("people_a2","A2","people","st-a2-unit-1",[("motho","noun","person","Ke motho ea molemo."),("batho","noun","people","Batho baa tla."),("motsoalle","noun","friend","Motsoalle oa ka o teng.")]),
_v("travel_a2","A2","travel","st-a2-unit-2",[("leeto","noun","journey","Leeto le qalile."),("tsamaea","verb","to go/walk","Ke tsamaea ho ea Maseru."),("khutla","verb","to return","Ke tla khutla hosane.")]),
_v("daily_a2","A2","daily life","st-a2-unit-3",[("mantsiboea","noun","evening","Mantsiboea rea qoqa."),("letsatsi","noun","day","Letsatsi le lelelele."),("beke","noun","week","Bekeng ena ke sebetsa.")]),
_v("health_a2","A2","health","st-a2-unit-4",[("bophelo","noun","health/life","Bophelo bo bohlokoa."),("ngaka","noun","doctor","Ngaka ea tla."),("bohloko","noun","pain","Ke utloa bohloko.")]),
_v("education_b1","B1","education","st-b1-unit-1",[("thuto","noun","education","Thuto e bohlokoa."),("patlisiso","noun","research","Patlisiso e tsoela pele."),("tsebo","noun","knowledge","Tsebo ea eketseha.")]),
_v("work_b1","B1","work","st-b1-unit-2",[("mosebetsi","noun","work/job","Ke na le mosebetsi."),("morero","noun","project/plan","Morero o phethetsoe."),("seboka","noun","meeting","Seboka se tla ba hosane.")]),
_v("society_b1","B1","society","st-b1-unit-3",[("nts'etsopele","noun","development","Nts'etsopele e tsoela pele."),("tšebelisano","noun","cooperation","Tšebelisano e bohlokoa."),("litšebeletso","noun","services","Litšebeletso li hlokahala.")]),
_v("environment_b1","B1","environment","st-b1-unit-4",[("tikoloho","noun","environment","Re lokela ho sireletsa tikoloho."),("metsi","noun","water","Metsi a hloekileng a bohlokoa."),("moru","noun","forest","Moru oa sireletsoa.")]),
_v("economy_b2","B2","economy","st-b2-unit-1",[("moruo","noun","economy","Moruo oa hola."),("matsete","noun","investment","Matsete aa eketseha."),("maraka","noun","market","Maraka oa fetoha.")]),
_v("governance_b2","B2","governance","st-b2-unit-2",[("mmuso","noun","government","Mmuso o phatlalalitse leano."),("melao","noun","laws","Melao e lokela ho lateloa."),("leano","noun","policy/strategy","Leano le lecha le phatlalalitsoe.")]),
_v("communication_b2","B2","communication","st-b2-unit-3",[("tlhaiso-leseling","noun","information","Tlhaiso-leseling e ncha e fihlile."),("puisano","noun","communication","Puisano e bohlokoa."),("molaetsa","noun","message","Molaetsa o fihlile.")]),
_v("media_b2","B2","media","st-b2-unit-4",[("mecha ea litaba","noun","media","Mecha ea litaba e phatlalalitse litaba."),("tlaleho","noun","report","Tlaleho e phatlalalitsoe."),("puisano","noun","discussion/interview","Puisano e ntse e tsoela pele.")]),
_v("academic_c1","C1","academic language","st-c1-unit-1",[("khopolo","noun","idea/theory","Khopolo e hloka tlhaloso."),("bopaki","noun","evidence","Re hloka bopaki bo tiileng."),("tlhatlhobo","noun","analysis","Tlhatlhobo e ntse e tsoela pele.")]),
_v("professional_c1","C1","professional language","st-c1-unit-2",[("tokomane","noun","document","Romela tokomane."),("litaelo","noun","instructions/regulations","Litaelo li lokela ho lateloa."),("boikarabelo","noun","responsibility","Boikarabelo ba hae ke ho hlahloba.")]),
_v("abstract_c1","C1","abstract concepts","st-c1-unit-3",[("litlamorao","noun","effects/consequences","Liqeto li na le litlamorao."),("sepheo","noun","objective","Sepheo ke ho ntlafatsa boleng."),("tharollo","noun","solution","Re fumane tharollo.")]),
_v("rhetoric_c2","C2","rhetoric","st-c2-unit-1",[("khang","noun","debate/argument","Khang e thehiloe bopaking."),("qeto","noun","conclusion/decision","Qeto e phatlalalitsoe."),("ntlha","noun","point/issue","Ntlha ea bohlokoa e hlakile.")]),
_v("discourse_c2","C2","discourse analysis","st-c2-unit-2",[("puo","noun","speech/language","Puo e lokela ho lumellana le bamameli."),("moelelo","noun","meaning","Moelelo oa hlaka."),("mokhoa","noun","style/method","Mokhoa oa mongoli o ikhethile.")]),
]

def _unit(level,n,title,grammar,vocab,checks):
    return CurriculumUnit(id=f"st-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,
        grammar_points=[grammar],vocabulary_set_ids=[vocab],
        lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],
        competency_checklist=checks,default_weeks=1 if level in ("A1","A2") else 2)

CURRICULUM = {
"A1":[_unit("A1",1,"Greetings and introductions","st-a1-g1","greetings_a1",["Greet someone naturally.","Introduce yourself."]),_unit("A1",2,"Identity","st-a1-g2","identity_a1",["Identify people and roles."]),_unit("A1",3,"Family","st-a1-g3","family_a1",["Describe family."]),_unit("A1",4,"Home and location","st-a1-g7","home_a1",["Say where people and objects are."]),_unit("A1",5,"Daily routine","st-a1-g3","routine_a1",["Describe a simple routine."]),_unit("A1",6,"Time","st-a1-g5","time_a1",["Ask and answer time questions."]),_unit("A1",7,"Food and drink","st-a1-g4","food_a1",["Order simple food and drink."]),_unit("A1",8,"Places","st-a1-g8","places_a1",["Name common places."])],
"A2":[_unit("A2",1,"People and agreement","st-a2-g1","people_a2",["Use noun-class agreement."]),_unit("A2",2,"Travel","st-a2-g2","travel_a2",["Talk about past and future travel."]),_unit("A2",3,"Daily life","st-a2-g8","daily_a2",["Describe routines and time."]),_unit("A2",4,"Health","st-a2-g3","health_a2",["Describe health needs."]),_unit("A2",5,"Objects and ownership","st-a2-g4","identity_a1",["Use object and possessive forms."]),_unit("A2",6,"Comparison","st-a2-g6","people_a2",["Compare people and things."]),_unit("A2",7,"Requests","st-a2-g7","places_a1",["Make polite requests."]),_unit("A2",8,"Integrated conversation","st-a2-g8","daily_a2",["Sustain an everyday exchange."])],
"B1":[_unit("B1",1,"Education","st-b1-g1","education_b1",["Use relative clauses."]),_unit("B1",2,"Work and projects","st-b1-g3","work_b1",["Discuss work and projects."]),_unit("B1",3,"Society","st-b1-g2","society_b1",["Explain conditions and consequences."]),_unit("B1",4,"Environment","st-b1-g7","environment_b1",["Give reasons and purposes."]),_unit("B1",5,"Passive and causative","st-b1-g4","work_b1",["Use passive and causative structures."]),_unit("B1",6,"Aspect and events","st-b1-g6","daily_a2",["Distinguish event structures."]),_unit("B1",7,"Reported speech","st-b1-g8","communication_b2",["Report statements and questions."]),_unit("B1",8,"Integrated communication","st-b1-g5","education_b1",["Give connected explanations."])],
"B2":[_unit("B2",1,"Economy","st-b2-g1","economy_b2",["Explain economic relationships."]),_unit("B2",2,"Governance","st-b2-g4","governance_b2",["Discuss institutional processes."]),_unit("B2",3,"Communication","st-b2-g5","communication_b2",["Control information focus."]),_unit("B2",4,"Media","st-b2-g6","media_b2",["Summarize media information."]),_unit("B2",5,"Nominalization","st-b2-g6","academic_c1",["Use formal noun phrases."]),_unit("B2",6,"Modality","st-b2-g7","governance_b2",["Express certainty and obligation."]),_unit("B2",7,"Register","st-b2-g8","professional_c1",["Adapt professional language."]),_unit("B2",8,"Complex discourse","st-b2-g2","communication_b2",["Build a coherent argument."])],
"C1":[_unit("C1",1,"Formal institutions","st-c1-g1","professional_c1",["Write formal institutional prose."]),_unit("C1",2,"Academic argumentation","st-c1-g2","academic_c1",["Present claims and evidence."]),_unit("C1",3,"Academic hedging","st-c1-g3","abstract_c1",["Qualify claims precisely."]),_unit("C1",4,"Embedded questions","st-c1-g4","communication_b2",["Integrate embedded questions."]),_unit("C1",5,"Information structure","st-c1-g5","discourse_c2",["Manage information flow."]),_unit("C1",6,"Media discourse","st-c1-g6","media_b2",["Produce precise public language."]),_unit("C1",7,"Pragmatics and idioms","st-c1-g7","rhetoric_c2",["Interpret implied meaning."]),_unit("C1",8,"Professional correspondence","st-c1-g8","professional_c1",["Draft formal requests."])],
"C2":[_unit("C2",1,"Cohesion","st-c2-g1","discourse_c2",["Control discourse cohesion."]),_unit("C2",2,"Nuanced modality","st-c2-g2","abstract_c1",["Express subtle stance."]),_unit("C2",3,"Advanced nominalization","st-c2-g3","academic_c1",["Handle dense academic prose."]),_unit("C2",4,"Rhetorical organization","st-c2-g4","rhetoric_c2",["Build and rebut arguments."]),_unit("C2",5,"Legal and administrative language","st-c2-g5","professional_c1",["Interpret procedural wording."]),_unit("C2",6,"Translation precision","st-c2-g6","discourse_c2",["Preserve register and pragmatic force."]),_unit("C2",7,"Literary style","st-c2-g7","rhetoric_c2",["Interpret figurative language."]),_unit("C2",8,"Discourse and register shifting","st-c2-g8","discourse_c2",["Shift deliberately among registers."])],
}

PHRASEBOOK_CATEGORIES = [
PhrasebookCategory(id="st-greetings-a1",level="A1",situation="greetings",icon="👋",phrases=[PhrasebookEntry(text="Lumela.",context="Hello.",register="neutral"),PhrasebookEntry(text="U phetse joang?",context="How are you?",register="neutral"),PhrasebookEntry(text="Ke phetse hantle, kea leboha.",context="I am well, thank you.",register="neutral")]),
PhrasebookCategory(id="st-introduction-a1",level="A1",situation="introductions",icon="👤",phrases=[PhrasebookEntry(text="Lebitso la ka ke Thabo.",context="My name is Thabo.",register="neutral"),PhrasebookEntry(text="Ke moithuti.",context="I am a student.",register="neutral")]),
PhrasebookCategory(id="st-thanks-a1",level="A1",situation="thanks",icon="🙏",phrases=[PhrasebookEntry(text="Kea leboha haholo.",context="Thank you very much.",register="neutral"),PhrasebookEntry(text="Ha ho bothata.",context="No problem.",register="neutral")]),
PhrasebookCategory(id="st-shopping-a1",level="A1",situation="shopping",icon="🛒",phrases=[PhrasebookEntry(text="Sena ke bokae?",context="How much is this?",register="neutral"),PhrasebookEntry(text="Ke batla sena.",context="I want this.",register="neutral"),PhrasebookEntry(text="Ka kopo, fokotsa theko.",context="Please lower the price.",register="polite")]),
PhrasebookCategory(id="st-help-a1",level="A1",situation="help",icon="🆘",phrases=[PhrasebookEntry(text="Nthuse ka kopo.",context="Please help me.",register="polite"),PhrasebookEntry(text="Ha ke utloisise.",context="I do not understand.",register="neutral"),PhrasebookEntry(text="Pheta hape, ka kopo.",context="Please repeat.",register="polite")]),
PhrasebookCategory(id="st-travel-a2",level="A2",situation="travel",icon="🚌",phrases=[PhrasebookEntry(text="Ke ea Maseru.",context="I am going to Maseru.",register="neutral"),PhrasebookEntry(text="Ke tla khutla neng?",context="When will I return?",register="neutral")]),
PhrasebookCategory(id="st-health-a2",level="A2",situation="health",icon="🩺",phrases=[PhrasebookEntry(text="Ha ke phele hantle.",context="I do not feel well.",register="neutral"),PhrasebookEntry(text="Ke hloka ngaka.",context="I need a doctor.",register="neutral")]),
PhrasebookCategory(id="st-study-b1",level="B1",situation="study",icon="📚",phrases=[PhrasebookEntry(text="Ke ithuta Sesotho.",context="I am studying Sesotho.",register="neutral"),PhrasebookEntry(text="Sena se bolela'ng?",context="What does this mean?",register="neutral")]),
PhrasebookCategory(id="st-work-b1",level="B1",situation="work",icon="💼",phrases=[PhrasebookEntry(text="Seboka se tla ba neng?",context="When will the meeting be?",register="neutral"),PhrasebookEntry(text="Morero o phethetsoe.",context="The project is finished.",register="neutral")]),
PhrasebookCategory(id="st-professional-b2",level="B2",situation="professional",icon="🏢",phrases=[PhrasebookEntry(text="Na le ka mpha lintlha tse eketsehileng?",context="Could you give me more details?",register="polite"),PhrasebookEntry(text="Ka lebaka leo, re kopa nako e eketsehileng.",context="For that reason, we request more time.",register="formal")]),
PhrasebookCategory(id="st-academic-c1",level="C1",situation="academic",icon="🎓",phrases=[PhrasebookEntry(text="Patlisiso e bontša hore...",context="The research shows that...",register="formal"),PhrasebookEntry(text="Ho ka etsahala hore...",context="It is possible that...",register="formal")]),
PhrasebookCategory(id="st-formal-c1",level="C1",situation="formal correspondence",icon="✉️",phrases=[PhrasebookEntry(text="Re le kopa hore le re romelle...",context="We request that you send us...",register="formal"),PhrasebookEntry(text="Re leboha tšebelisano-'moho ea lona.",context="We thank you for your cooperation.",register="formal")]),
PhrasebookCategory(id="st-debate-c2",level="C2",situation="discussion and debate",icon="🗣️",phrases=[PhrasebookEntry(text="Le hoja seo e le 'nete, taba ea bohlokoa ke...",context="Although that is true, the main issue is...",register="formal"),PhrasebookEntry(text="Ka lehlakoreng le leng...",context="On the other hand...",register="formal")]),
]

ASSESSMENT_BANK = [
AssessmentQuestion(id="st-a1-001",skill="communication",difficulty="A1",question="Which phrase means “Hello” in Southern Sotho?",options=["Lumela.","Kea leboha.","Nthuse ka kopo.","Sena ke bokae?"],correct="Lumela."),
AssessmentQuestion(id="st-a1-002",skill="communication",difficulty="A1",question="Which sentence means “My name is Thabo”?",options=["Lebitso la ka ke Thabo.","Ke batla metsi.","Ke ea sekolong.","Mme o lapeng."],correct="Lebitso la ka ke Thabo."),
AssessmentQuestion(id="st-a1-003",skill="vocabulary",difficulty="A1",question="Which word means “water”?",options=["metsi","ntlo","nako","sekolo"],correct="metsi"),
AssessmentQuestion(id="st-a1-004",skill="grammar",difficulty="A1",question="Which phrase asks “Where are you?”",options=["U hokae?","Kea leboha.","Ke batla sena.","Lumela."],correct="U hokae?"),
AssessmentQuestion(id="st-a2-001",skill="grammar",difficulty="A2",question="Which pair shows a common singular/plural contrast?",options=["motho / batho","metsi / lebese","mme / ntate","nako / hosane"],correct="motho / batho"),
AssessmentQuestion(id="st-a2-002",skill="communication",difficulty="A2",question="Which is a polite request?",options=["Ka kopo, lula fatše.","Ke ea sekolong.","Kajeno ke lapeng.","Ke nako mang?"],correct="Ka kopo, lula fatše."),
AssessmentQuestion(id="st-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["Haeba u ithuta, u tla pasa.","Lumela.","Ke batla metsi.","Ke lapeng."],correct="Haeba u ithuta, u tla pasa."),
AssessmentQuestion(id="st-b1-002",skill="grammar",difficulty="B1",question="Which example is passive?",options=["Buka e baliloe ke moithuti.","Ke ithuta letsatsi le leng le le leng.","Ke ea sekolong.","Ke noa lebese."],correct="Buka e baliloe ke moithuti."),
AssessmentQuestion(id="st-b2-001",skill="discourse",difficulty="B2",question="Which phrase marks a consequence?",options=["Ka lebaka leo","Lumela","Lebitso la ka ke Thabo.","Kea leboha."],correct="Ka lebaka leo"),
AssessmentQuestion(id="st-b2-002",skill="register",difficulty="B2",question="Which phrase fits a formal request?",options=["Re le kopa hore le re romelle...","Lumela.","Ke batla sena.","U hokae?"],correct="Re le kopa hore le re romelle..."),
AssessmentQuestion(id="st-c1-001",skill="academic",difficulty="C1",question="Which phrase appropriately hedges an academic claim?",options=["Ho ka etsahala hore...","Lumela.","Kea leboha.","Ke batla sena."],correct="Ho ka etsahala hore..."),
AssessmentQuestion(id="st-c1-002",skill="professional",difficulty="C1",question="Which sentence is a formal institutional request?",options=["Re le kopa hore le re romelle litokomane tse hlokahalang.","Ke lapeng.","Ke batla metsi.","U hokae?"],correct="Re le kopa hore le re romelle litokomane tse hlokahalang."),
AssessmentQuestion(id="st-c2-001",skill="discourse",difficulty="C2",question="Which phrase introduces a counterargument?",options=["Le hoja seo e le 'nete, taba ea bohlokoa ke...","Lumela.","Ke phetse hantle.","Lebitso la ka ke Thabo."],correct="Le hoja seo e le 'nete, taba ea bohlokoa ke..."),
AssessmentQuestion(id="st-c2-002",skill="translation",difficulty="C2",question="What should advanced translation preserve besides literal meaning?",options=["Register and pragmatic force","Only word order","Only punctuation","Only word length"],correct="Register and pragmatic force"),
]

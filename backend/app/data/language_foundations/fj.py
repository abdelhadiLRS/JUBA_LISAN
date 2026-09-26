"""Fijian A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

def _g(slug,title,level,explanation,examples):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=f"Fijian {level} grammar.",explanation=explanation,examples=[GrammarExample(text=x) for x in examples])

_topics=[
("pronouns","Personal pronouns","A1","Use personal pronouns.","Au sa gonevuli."),
("copula","Nominal and identifying clauses","A1","Identify people and things.","Oqo na noqu vale."),
("questions","Question words and questions","A1","Ask basic questions.","O cei na yacamu?"),
("negation","Negation with sega ni","A1","Form negative clauses.","Au sega ni kila."),
("possession","Possession","A1","Express ownership.","Na noqu vale e levu."),
("location","Location with e and tiko","A1","Express location.","Au tiko e Suva."),
("requests","Requests and politeness","A1","Make polite requests.","Vukei au mada, kerekere."),
("present","Present and habitual actions","A2","Describe current and habitual actions.","Au dau lako ena mataka."),
("past","Past events","A2","Describe completed events.","Au sa lesu mai."),
("future","Future and intention","A2","Express plans and future events.","Au na lako nimataka."),
("aspect","Aspectual particles","A2","Use sa, se and oti for event state.","Au se vuli tiko."),
("plural","Plural participants","A2","Distinguish singular and plural.","Era tiko e vale."),
("comparatives","Comparison","A2","Compare qualities.","E levu cake na vale oqo."),
("modality","Ability, desire and obligation","A2","Express ability, desire and necessity.","Au rawa ni lako."),
("serial_verbs","Serial verb constructions","B1","Link actions and meanings.","Lako mai ka raica."),
("prepositions","Relational and directional phrases","B1","Express source and direction.","Au lako ki na makete."),
("conditional","Conditional clauses","B1","Express conditions.","Kevaka o rawa, vukei au."),
("relative","Relative clauses","B1","Modify noun phrases.","Na tamata e lako tiko e noqu itokani."),
("causal","Cause, purpose and result","B1","Connect reason and consequence.","Au tiko eke baleta niu cakacaka."),
("reported","Reported speech","B1","Report another speaker.","E kaya ni na lako mai."),
("reflexive","Reflexive and reciprocal meaning","B1","Express self-directed actions.","Era veivukei."),
("passive","Passive and affected constructions","B2","Focus on affected participants.","Sa vakarautaki na kakana."),
("causative","Causative constructions","B2","Express causing or enabling.","Au vakavulici koya."),
("concessive","Concession and contrast","B2","Express contrast.","E dina ni draki ca, keimami a lako."),
("discourse","Discourse connectors","B2","Organize extended discourse.","Taumada, eda raica na leqa."),
("nominalization","Nominalization","C1","Build formal process nouns.","Na vakatorocaketaki ni vuli e bibi."),
("hedging","Academic hedging and stance","C1","Qualify claims.","E rawa ni tukuni ni sa veisau na ituvaki."),
("embedded","Embedded questions","C1","Embed questions and propositions.","Au sega ni kila na vanua e tiko kina."),
("information_structure","Topic and focus","C1","Highlight information in discourse.","Na ka oqo, au na vakamacalataka mada."),
("formal","Formal and institutional Fijian","C1","Use professional language.","E kerei me vakauta na pepa."),
("argumentation","Academic argumentation","C1","Build claims and counterarguments.","Na ivakadinadina e tokona na vakasama."),
("pragmatics","Politeness and pragmatic nuance","C2","Interpret indirectness and respect.","Kevaka e rawa, yalovinaka ni raica tale."),
("register","Register shifting","C2","Shift between conversational and formal language.","Na ivakarau ni vosa e veisau."),
("rhetoric","Rhetorical and literary style","C2","Use contrast and persuasive framing.","E sega ni leqa wale ga, ia e dua na madigi."),
("translation","Translation and paraphrase","C2","Preserve meaning and register.","Me maroroi na ibaleebale kei na iwalewale."),
("discourse_analysis","Discourse analysis","C2","Analyze cohesion, audience and genre.","Na ibaleebale e vakatau ena ituvaki.")
]
GRAMMAR_TOPICS=[_g(*x) for x in _topics]

def _v(id_,level,topic,ref,items):
    return VocabularySet(id=id_,level=level,topic=topic,unit_ref=ref,words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in items])

VOCABULARY_SETS=[
_v("greetings_a1","A1","greetings","fj-a1-unit-1",[("bula","phrase","hello","Bula!"),("vinaka","phrase","thank you","Vinaka vakalevu."),("kerekere","phrase","please","Kerekere."),("moce","phrase","goodbye","Moce!")]),
_v("identity_a1","A1","identity","fj-a1-unit-2",[("yacamu","noun","your name","O cei na yacamu?"),("au","pronoun","I","Au tiko e Suva."),("iko","pronoun","you","O iko?"),("gonevuli","noun","student","Au sa gonevuli.")]),
_v("family_a1","A1","family","fj-a1-unit-3",[("tina","noun","mother","Au veivosaki kei tinaqu."),("tamaqu","noun","my father","E cakacaka tamaqu."),("vuvale","noun","family","E levu na noqu vuvale."),("gone","noun","child","Na gone e tiko e vale.")]),
_v("home_a1","A1","home","fj-a1-unit-4",[("vale","noun","house","Oqo na noqu vale."),("rumu","noun","room","Au tiko ena noqu rumu."),("teveli","noun","table","Na ivola e dela ni teveli."),("katuba","noun","door","Dolava na katuba.")]),
_v("routine_a1","A1","daily routine","fj-a1-unit-5",[("cakacaka","verb","work","Au cakacaka nikua."),("vuli","verb","study","Au vuli nikua."),("kana","verb","eat","Au kana ena mataka."),("moce","verb","sleep","Au lako moce.")]),
_v("food_a1","A1","food and drink","fj-a1-unit-6",[("wai","noun","water","Au vinakata na wai."),("kakana","noun","food","Sa vakarautaki na kakana."),("inu","verb","drink","Au via inu wai."),("ika","noun","fish","Keitou kana ika.")]),
_v("places_a1","A1","places","fj-a1-unit-7",[("makete","noun","market","Na makete e voleka."),("vanua","noun","place","Na vanua oqo e vinaka."),("Suva","proper_noun","Suva","Au tiko e Suva."),("gaunisala","noun","road","Na gaunisala e balavu.")]),
_v("help_a1","A1","help","fj-a1-unit-8",[("veivukei","noun","help","Au gadreva na veivukei."),("kila","verb","know","Au kila na ka oqo."),("vukea","verb","help","Vukei au mada."),("vosa","noun","language","Au vulica na vosa vakaViti.")]),
_v("travel_a2","A2","travel","fj-a2-unit-1",[("lako","verb","go","Au na lako nimataka."),("soko","verb","travel by sea","Keitou soko ki na yanuyanu."),("tikite","noun","ticket","Au volia na tikite."),("yanuyanu","noun","island","Na yanuyanu e totoka.")]),
_v("health_a2","A2","health","fj-a2-unit-2",[("tauvimate","verb","be ill","Au tauvimate nikua."),("vuniwai","noun","doctor","Au gadreva na vuniwai."),("bulabula","adjective","healthy","Au sa bulabula vinaka."),("wai ni mate","noun","medicine","Au taura na wai ni mate.")]),
_v("study_a2","A2","study","fj-a2-unit-3",[("ivola","noun","book","Au wilika na ivola."),("kalasi","noun","class","Na kalasi e tekivu nikua."),("vakadidike","verb","research","Keitou vakadidike tiko."),("ivakamacala","noun","explanation","Na ivakamacala e matata.")]),
_v("work_b1","B1","work","fj-b1-unit-1",[("cakacaka","noun","work","Na cakacaka e bibi."),("soqoni","noun","meeting","Na soqoni ena tekivu."),("tavi","noun","task","Oqo na noqu tavi."),("tuvatuva","noun","plan","E tiko na tuvatuva vou.")]),
_v("society_b1","B1","society","fj-b1-unit-2",[("itikotiko","noun","community","Na itikotiko e cakacaka vata."),("dodonu","adjective","right","E dodonu me veidokai."),("itavi","noun","responsibility","Na itavi e bibi."),("veimaliwai","noun","social relations","E vinaka na veimaliwai.")]),
_v("environment_b2","B2","environment","fj-b2-unit-1",[("veika bula","noun","natural environment","E dodonu me maroroi na veika bula."),("maroroya","verb","protect","Eda dodonu me da maroroya na vanua."),("veivakacacani","noun","damage","Na veivakacacani e levu."),("vuravura","noun","world","Na vuravura e dodonu me maroroi.")]),
_v("economy_b2","B2","economy","fj-b2-unit-2",[("bisinisi","noun","business","Na bisinisi e tubu."),("iyaqaqa","noun","resources","E vakaiyalayala na iyaqaqa."),("rawa","verb","be possible","E rawa ni veisau."),("volitaki","verb","sell/trade","Era volitaki na iyaya.")]),
_v("media_c1","C1","media","fj-c1-unit-1",[("itukutuku","noun","information/news","Na itukutuku e vakadodonutaki."),("ivurevure","noun","source","Na ivurevure e dodonu me nuitaki."),("tukutuku","noun","report","Na tukutuku e vakaraitaka na dina."),("rai","noun","viewpoint","Na nona rai e duidui.")]),
_v("academic_c1","C1","academic","fj-c1-unit-2",[("vakadidike","noun","research","Na vakadidike e vakaraitaka na kena revurevu."),("ivakadinadina","noun","evidence","E tiko na ivakadinadina."),("vakasama","noun","argument/idea","Na vakasama e bibi."),("jike","noun","analysis","Na dikevi ni itukutuku e bibi.")]),
_v("institutional_c1","C1","institutional","fj-c1-unit-3",[("vakatulewa","noun","decision/governance","Na vakatulewa e sa vakadonui."),("kerekere","noun","application","Na kerekere sa ciqomi."),("vakadonuya","verb","approve","Era vakadonuya na kerekere."),("gauna","noun","time","Na gauna e sa voleka.")]),
_v("culture_c2","C2","culture","fj-c2-unit-1",[("itovo vakavanua","noun","cultural practices","E bibi na itovo vakavanua."),("vakarau","noun","custom/manner","E duidui na vakarau."),("vakarokoroko","noun","respect","Na vakarokoroko e bibi."),("vanua","noun","land/community","Na vanua e dua na yavu bibi.")]),
_v("discourse_c2","C2","discourse","fj-c2-unit-2",[("veivosaki","noun","conversation/discourse","Na veivosaki e gadreva na vakarorogo."),("ibaleebale","noun","meaning","Na ibaleebale e vakatau ena ituvaki."),("ivakarau","noun","style","Na ivakarau ni vosa e veisau."),("vakadewa","noun","translation","Na vakadewa e maroroya na ibaleebale.")])
]

def _p(id_,level,situation,items,register="neutral"):
    return PhrasebookCategory(id=id_,level=level,situation=situation,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=register) for t,c in items])

PHRASEBOOK_CATEGORIES=[
_p("greetings_a1","A1","greetings",[("Bula!","greeting"),("O cei na yacamu?","asking a name"),("Moce!","saying goodbye")]),
_p("thanks_a1","A1","thanks",[("Vinaka.","thanks"),("Vinaka vakalevu.","emphasis"),("E sega ni dua na leqa.","polite response")]),
_p("shopping_a1","A1","shopping",[("E vica na kena isau?","asking price"),("Au vinakata na ka oqo.","requesting an item"),("Au vinakata na wai.","requesting a drink")]),
_p("directions_a1","A1","directions",[("E vei na makete?","asking location"),("E voleka.","saying nearby"),("Kere veivuke, kerekere.","asking help")]),
_p("daily_a1","A1","daily life",[("Au cakacaka nikua.","work"),("Au sa vuli.","study"),("Au tiko e Suva.","location")]),
_p("travel_a2","A2","travel",[("Au na lako nimataka.","future plan"),("E vei na gaunisala?","asking directions"),("Au volia na tikite.","ticket")]),
_p("health_a2","A2","health",[("Au tauvimate nikua.","illness"),("Au gadreva na vuniwai.","doctor"),("Au vinakata na wai ni mate.","medicine")]),
_p("study_b1","B1","study",[("Au gadreva na ivakamacala.","asking explanation"),("Au sega ni kila.","clarification"),("Tukuna tale mada.","repeat request")]),
_p("work_b1","B1","work",[("Me da veivosaki mada.","start discussion"),("Au vakatura ni ...","suggestion"),("Au duavata.","agreement")]),
_p("formal_b2","B2","formal communication",[("E kerei me ...","formal request"),("E vakaraitaki kina ni ...","formal statement"),("Vinaka ena nomuni veivuke.","formal thanks")],"formal"),
_p("academic_c1","C1","academic discussion",[("E rawa ni tukuni ni ...","hedging"),("Na ivakadinadina e vakaraitaka ...","evidence"),("Ia, e dodonu me dikevi tale ...","qualification")],"academic"),
_p("presentation_c1","C1","presentation",[("Taumada, eda na raica ...","opening"),("Na ka bibi duadua ...","highlight"),("Kena itinitini ...","closing")],"formal"),
_p("pragmatics_c2","C2","pragmatic nuance",[("Kevaka e rawa, yalovinaka ...","softening"),("Au kila na nomuni rai, ia ...","polite disagreement"),("E rawa ni da dikeva tale ...","tentative suggestion")],"polite")
]

def _u(level,n,title,grammar,vocab):
    return CurriculumUnit(id=f"fj-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=grammar,vocabulary_set_ids=vocab,lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=[f"Communicate effectively at {level}",f"Understand level-appropriate Fijian"],default_weeks=2)

CURRICULUM={}
plans={
"A1":[("Bula kei na veikilai",["pronouns","copula"],["greetings_a1"]),("Veika me baleta na tamata",["questions","possession"],["identity_a1"]),("Vuvale",["possession","plural"],["family_a1"]),("Vale kei na vanua",["location","questions"],["home_a1"]),("Na veika e caka e veisiga",["present","negation"],["routine_a1"]),("Kakana kei na gunu",["possession","requests"],["food_a1"]),("Veivanua kei na sala",["location","questions"],["places_a1"]),("Veivukei kei na veivosaki",["requests","negation"],["help_a1"])],
"A2":[("Lako voli",["future","prepositions"],["travel_a2"]),("Bula kei na tauvimate",["modality","aspect"],["health_a2"]),("Vuli",["past","aspect"],["study_a2"]),("Na veika e dau caka",["present","plural"],["routine_a1"]),("Gagade kei na tuvatuva",["modality","future"],["work_b1"]),("Veidutaitaki",["comparatives","modality"],["society_b1"]),("Na gauna sa oti",["past","aspect"],["travel_a2"]),("A2 vakadidike",["past","future","aspect"],["health_a2","study_a2"])],
"B1":[("Veimaliwai kei na vosa",["serial_verbs","prepositions"],["society_b1"]),("Tuvatuva kei na ivakarau",["conditional","future"],["work_b1"]),("Veika e sema",["relative","discourse"],["environment_b2"]),("Vuna kei na inaki",["causal","concessive"],["society_b1"]),("Vosa e tukuna tale",["reported","embedded"],["media_c1"]),("Veimaliwai",["reflexive","discourse"],["society_b1"]),("Tukutuku kei na vakamacala",["reported","relative"],["media_c1"]),("B1 vakadidike",["conditional","causal","reported"],["work_b1","media_c1"])],
"B2":[("Cakacaka e vakayacori",["passive","causative"],["work_b1"]),("Veika e vakavuna",["causative","aspect"],["economy_b2"]),("Veibasai kei na veivosaki",["concessive","discourse"],["society_b1"]),("Veika vakailavo",["passive","discourse"],["economy_b2"]),("Veika bula kei na vanua",["concessive","causal"],["environment_b2"]),("Vakamacala vakavinaka",["discourse","relative"],["media_c1"]),("Veivakadodonutaki ni itukutuku",["passive","reported"],["media_c1"]),("B2 vakadidike",["passive","concessive","discourse"],["environment_b2","economy_b2"])],
"C1":[("Vakadidike kei na ivakadinadina",["nominalization","hedging"],["academic_c1"]),("Veika vakamatanitu",["formal","argumentation"],["institutional_c1"]),("Tukutuku kei na ivurevure",["information_structure","reported"],["media_c1"]),("Taro e tiko ena vosa",["embedded","causal"],["academic_c1"]),("Veivosaki vakavuku",["argumentation","discourse"],["academic_c1"]),("Veitaratara vakamatanitu",["formal","hedging"],["institutional_c1"]),("Ulutaga kei na vakabibitaki",["information_structure","nominalization"],["media_c1"]),("C1 vakadidike",["argumentation","formal","embedded"],["academic_c1","institutional_c1"])],
"C2":[("Vakarokoroko kei na pragmatics",["pragmatics","register"],["discourse_c2"]),("Vosa vakavuku kei na rhetoric",["rhetoric","discourse_analysis"],["culture_c2"]),("Veisautaki ni ivakarau ni vosa",["register","pragmatics"],["institutional_c1"]),("Dikevi ni veivosaki",["discourse_analysis","information_structure"],["discourse_c2"]),("Vakadewa kei na paraphrase",["translation","register"],["culture_c2"]),("Argumentation vakavuku",["argumentation","rhetoric"],["discourse_c2"]),("iTovo kei na media",["rhetoric","register"],["culture_c2","media_c1"]),("C2 vakadidike",["translation","pragmatics","discourse_analysis"],["discourse_c2","culture_c2"])]
}
for level,items in plans.items():
    CURRICULUM[level]=[_u(level,i+1,title,grammar,vocab) for i,(title,grammar,vocab) in enumerate(items)]

ASSESSMENT_BANK=[
AssessmentQuestion(id="fj-a1-001",skill="vocabulary",difficulty="A1",question="What does “bula” mean?",options=["hello","water","house","help"],correct="hello"),
AssessmentQuestion(id="fj-a1-002",skill="communication",difficulty="A1",question="Which phrase asks someone's name?",options=["O cei na yacamu?","Au tiko e Suva.","Au cakacaka nikua.","Moce!"],correct="O cei na yacamu?"),
AssessmentQuestion(id="fj-a1-003",skill="vocabulary",difficulty="A1",question="Which word means “mother”?",options=["tina","vale","wai","makete"],correct="tina"),
AssessmentQuestion(id="fj-a2-001",skill="grammar",difficulty="A2",question="Which sentence expresses a future plan?",options=["Au na lako nimataka.","Au tiko e Suva.","Au sa gonevuli.","Au sega ni kila."],correct="Au na lako nimataka."),
AssessmentQuestion(id="fj-a2-002",skill="grammar",difficulty="A2",question="Which sentence expresses ability?",options=["Au rawa ni lako.","Au na lako nimataka.","Au tauvimate nikua.","Bula!"],correct="Au rawa ni lako."),
AssessmentQuestion(id="fj-b1-001",skill="grammar",difficulty="B1",question="Which sentence introduces a condition?",options=["Kevaka o rawa, vukei au.","Au tiko e Suva.","Au sa vuli.","Vinaka vakalevu."],correct="Kevaka o rawa, vukei au."),
AssessmentQuestion(id="fj-b1-002",skill="grammar",difficulty="B1",question="Which phrase reports another statement?",options=["E kaya ni na lako mai.","Bula!","Au vinakata na wai.","E vei na makete?"],correct="E kaya ni na lako mai."),
AssessmentQuestion(id="fj-b2-001",skill="grammar",difficulty="B2",question="Which example is passive or affected?",options=["Sa vakarautaki na kakana.","Au na lako nimataka.","O cei na yacamu?","Au tiko e Suva."],correct="Sa vakarautaki na kakana."),
AssessmentQuestion(id="fj-b2-002",skill="discourse",difficulty="B2",question="Which phrase introduces a sequence?",options=["Taumada, eda raica na leqa.","Bula!","Moce!","O cei na yacamu?"],correct="Taumada, eda raica na leqa."),
AssessmentQuestion(id="fj-c1-001",skill="academic",difficulty="C1",question="Which phrase hedges an academic claim?",options=["E rawa ni tukuni ni sa veisau na ituvaki.","E sega ni dua tale na rai.","E dina sara ga.","Tukuna vakadodonu."],correct="E rawa ni tukuni ni sa veisau na ituvaki."),
AssessmentQuestion(id="fj-c1-002",skill="formal",difficulty="C1",question="Which phrase is a formal request?",options=["E kerei me ...","Bula!","Moce!","Au via kana."],correct="E kerei me ..."),
AssessmentQuestion(id="fj-c2-001",skill="pragmatics",difficulty="C2",question="Which phrase softens a request?",options=["Kevaka e rawa, yalovinaka ...","Mo cakava oqo!","Sega!","Au vinakata oqo."],correct="Kevaka e rawa, yalovinaka ..."),
AssessmentQuestion(id="fj-c2-002",skill="translation",difficulty="C2",question="What should advanced translation preserve?",options=["Meaning, register and discourse function","Only literal words","Only word order","Only punctuation"],correct="Meaning, register and discourse function")
]

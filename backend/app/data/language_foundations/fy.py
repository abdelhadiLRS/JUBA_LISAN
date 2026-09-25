"""Western Frisian (Frysk) A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def _g(slug,title,level,summary,explanation,examples):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=summary,explanation=explanation,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS=[
_g("pronouns","Persoanlike foarnamwurden","A1","Use personal pronouns.","Learn ik, do, hy, sy, it, wy, jimme and hja in everyday clauses.",["Ik bin Anna.","Wy wenje yn Fryslân."]),
_g("word-order","Basis wurdfolchoarder","A1","Build simple sentences.","Use normal subject-verb order and learn the position of common adverbs.",["Ik wenje yn Ljouwert.","Hjoed wurkje ik thús."]),
_g("present","Notiid","A1","Talk about current actions.","Conjugate common regular verbs in the present tense.",["Ik praat Frysk.","Sy wurket hjoed."]),
_g("questions","Fragen","A1","Ask everyday questions.","Use interrogatives and inversion in simple questions.",["Wêr wenje do?","Praatsto Frysk?"]),
_g("negation","Untkenning","A1","Make negative statements.","Use net and gjin in basic clauses.",["Ik begryp it net.","Ik ha gjin tiid."]),
_g("articles","Lidwurden","A1","Use definite and indefinite articles.","Distinguish de, it and in in basic noun phrases.",["de stêd","it hûs","in boek"]),
_g("possessives","Besitlike foarnamwurden","A1","Express possession.","Use myn, dyn, syn, har, ús and harren.",["Dit is myn boek.","Dat is har hûs."]),
_g("locations","Plak en rjochting","A1","Talk about place and movement.","Use common prepositions such as yn, op, ûnder, nei and fan.",["Ik bin yn 'e stêd.","Wy geane nei skoalle."]),
_g("past","Doetiid","A2","Describe past events.","Use common past-tense patterns and recognize strong and weak verbs.",["Juster wurke ik thús.","Hy gie nei Ljouwert."]),
_g("perfect","Perfektum","A2","Talk about completed experiences.","Use hawwe/weze with past participles in common constructions.",["Ik ha it boek lêzen.","Sy is nei hûs gien."]),
_g("future","Takomst en bedoeling","A2","Talk about plans.","Use sille and present-tense expressions for future meaning.",["Moarn sil ik wurkje.","Wy geane sneon nei de merk."]),
_g("comparatives","Fergeliking","A2","Compare things and people.","Use comparative and superlative forms with as...as and than constructions.",["Dizze auto is flugger.","Hy is de grutste."]),
_g("imperative","Gebiedende foarm en hoflikheid","A2","Give instructions and requests.","Use imperatives and polite modal phrases.",["Kom hjir!","Kinst my helpe?"]),
_g("modal-verbs","Modale tiidwurden","B1","Express ability, obligation and possibility.","Work with kinne, moatte, meie, wolle and their complements.",["Ik moat moarn wurkje.","Meisto hjir sitte?"]),
_g("separable-verbs","Skiedbere tiidwurden","B1","Handle separable verb particles.","Recognize particle placement in main clauses and infinitive constructions.",["Ik stean moarns betiid op.","Ik wol betiid opstean."]),
_g("subordination","Bysinnen","B1","Join clauses accurately.","Use dat, omdat, as, wylst and other subordinators with appropriate word order.",["Ik bliuw thús, omdat it reint.","Ik wit dat er komt."]),
_g("relative","Betreklike bysinnen","B1","Describe nouns with relative clauses.","Use relative structures with common pronouns and prepositions.",["It boek dat ik lêze is nij.","De frou mei wa't ik praat is learaar."]),
_g("conditional","Betingsten","B1","Express hypothetical conditions.","Use as-clauses and modal forms for real and hypothetical conditions.",["As ik tiid ha, kom ik.","As ik tiid hie, soe ik komme."]),
_g("reported-speech","Yndirekte rede","B1","Report statements and questions.","Use dat-clauses and indirect questions in speech and writing.",["Hy seit dat er moarn komt.","Ik wit net wêr't sy wennet."]),
_g("passive","Lijdende foarm","B2","Use passive constructions.","Form passive clauses with wurde and wêze where appropriate.",["It hûs wurdt boud.","De brief is ferstjoerd."]),
_g("aspect","Aksje en ferrin","B2","Describe completed and ongoing situations.","Choose tense and aspectual expressions to distinguish events, states and duration.",["Ik bin al begûn.","Wy binne noch oan it wurk."]),
_g("concession","Kontrast en tajefte","B2","Express contrast and concession.","Use hoewol, ek al, dochs, mar and related connectors.",["Hoewol't it reint, geane wy nei bûten.","It is djoer, mar dochs keapje ik it."]),
_g("discourse-connectors","Binde- en argumintaasjewurden","B2","Connect ideas coherently.","Use dêrom, om't, lykwols, boppedat and dêrneist to organize discourse.",["It reinde; dêrom bleaunen wy thús.","Boppedat wie it let."]),
_g("nominalization","Nominalisaasje","B2","Build compact formal noun phrases.","Recognize deverbal nouns and nominal structures in formal Frisian.",["It nimmen fan it beslút duorre lang.","De útfiering fan it plan begjint moarn."]),
_g("register","Taalregister en omgongstaal","B2","Adapt language to context.","Distinguish informal conversation from standard written Frisian.",["Komsto ek?","Komme jo moarn by de gearkomste?"]),
_g("academic-hedging","Akademyske foarsichtigens","C1","Qualify claims.","Use constructions such as it liket derop dat, nei alle gedachten and kin der op wize.",["It liket derop dat de resultaten ferskille.","De gegevens kinne derop wize dat it effekt lyts is."]),
_g("complex-subordination","Komplekse ûnderskikking","C1","Manage multiple subordinate clauses.","Maintain clear reference and word order in dense written syntax.",["Hoewol't de gegevens beheind binne, litte de resultaten sjen dat de trend trochgiet."]),
_g("argumentation","Argumintaasje","C1","Build evidence-based arguments.","Signal claims, evidence, qualification and conclusions precisely.",["Earst lit de stúdzje sjen dat..., wylst in oare ynterpretaasje mooglik bliuwt."]),
_g("institutional","Formeel en bestjoerlik Frysk","C1","Write formal institutional texts.","Use conventional administrative structures while keeping sentences readable.",["It formulier moat foar freed ynlevere wurde.","It fersyk wurdt yn de folgjende gearkomste behannele."]),
_g("pragmatics","Pragmatyk en hoflikheid","C1","Manage implied meaning and politeness.","Adjust directness and modality to relationship, status and setting.",["Soene jo dat nochris útlizze kinne?","Foar safier't ik wit, jildt dit allinnich foar de earste faze."]),
_g("rhetoric","Retoryk","C2","Analyze persuasive language.","Study framing, repetition, contrast and metaphor in advanced Frisian discourse.",["It giet net allinnich om kosten, mar ek om ferantwurdlikens."]),
_g("translation","Oersettingskrektens","C2","Preserve meaning across languages.","Maintain register, modality, idiom and information structure rather than translating word for word.",["De oersetting behâldt de foarsichtigens fan it orizjineel."]),
_g("literary-style","Literêre styl","C2","Interpret literary nuance.","Analyze rhythm, imagery, idiom and shifts between registers.",["De stilte hong yn 'e keamer as in fraach sûnder antwurd."]),
_g("discourse-analysis","Diskursanalyse","C2","Analyze cohesion and stance.","Track reference, presupposition, evaluation, framing and register shifts.",["De tekst skept in dúdlike tsjinstelling troch werhelle wurdearringstaal."])
]

def _v(i,level,topic,items):
    return VocabularySet(id=i,level=level,topic=topic,unit_ref=f"fy-{level.lower()}-unit-1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in items])

VOCABULARY_SETS=[
_v("greetings_a1","A1","Groetnis",[("hallo","phrase","hello","Hallo!"),("goeiemoarn","phrase","good morning","Goeiemoarn!"),("tank","phrase","thanks","Tank foar dyn help."),("oant sjen","phrase","goodbye","Oant sjen!")]),
_v("identity_a1","A1","Identiteit",[("namme","noun","name","Wat is dyn namme?"),("freon","noun","friend","Hy is myn freon."),("learaar","noun","teacher","Sy is learaar."),("studint","noun","student","Ik bin studint.")]),
_v("family_a1","A1","Famylje",[("mem","noun","mother","Myn mem wennet hjir."),("heit","noun","father","Myn heit wurket hjoed."),("suster","noun","sister","Ik ha in suster."),("broer","noun","brother","Myn broer is jong.")]),
_v("home_a1","A1","Thús",[("hûs","noun","house","Wy ha in hûs."),("keamer","noun","room","De keamer is grut."),("doar","noun","door","De doar is iepen."),("finster","noun","window","It finster is iepen.")]),
_v("daily_a1","A1","Deistich libben",[("moarns","adverb","in the morning","Moarns drink ik kofje."),("wurk","noun","work","Ik ha hjoed wurk."),("iten","noun","food","It iten is klear."),("sliepe","verb","sleep","Ik wol sliepe.")]),
_v("food_a1","A1","Iten en winkeljen",[("bôle","noun","bread","Ik keapje bôle."),("molke","noun","milk","Ik drink molke."),("apel","noun","apple","Ik yt in apel."),("priis","noun","price","Wat is de priis?")]),
_v("places_a2","A2","Plakken en reizgjen",[("stêd","noun","city","Ljouwert is in stêd."),("doarp","noun","village","Wy wenje yn in doarp."),("stasjon","noun","station","It stasjon is tichtby."),("trein","noun","train","De trein komt om tsien oere.")]),
_v("health_a2","A2","Sûnens",[("sûn","adjective","healthy","Ik fiel my sûn."),("dokter","noun","doctor","Ik gean nei de dokter."),("pine","noun","pain","Ik ha pine yn 'e holle."),("medisyn","noun","medicine","Ik nim myn medisyn.")]),
_v("work_b1","B1","Wurk",[("gearwurkjen","noun","cooperation","Gearwurkjen is wichtich."),("gearkomste","noun","meeting","De gearkomste begjint om njoggen oere."),("taak","noun","task","Myn taak is dúdlik."),("deadline","noun","deadline","De deadline is freed.")]),
_v("education_b1","B1","Underwiis",[("ûnderwiis","noun","education","Goed ûnderwiis is wichtich."),("les","noun","lesson","De les begjint no."),("ûndersyk","noun","research","It ûndersyk duorret twa jier."),("eksamen","noun","exam","It eksamen is moarn.")]),
_v("society_b1","B1","Mienskip",[("mienskip","noun","community","De mienskip helpt elkoar."),("belied","noun","policy","It nije belied wurdt besprutsen."),("rjocht","noun","right/law","Elkenien hat rjocht op ynformaasje."),("beslút","noun","decision","It beslút is publisearre.")]),
_v("media_b2","B2","Media",[("nijs","noun","news","It nijs ferspraat him fluch."),("boarne","noun","source","De boarne moat kontrolearre wurde."),("bewearing","noun","claim","De bewearing freget om bewiis."),("perspektyf","noun","perspective","It artikel jout in oar perspektyf.")]),
_v("environment_b2","B2","Miljeu",[("klimaatferoaring","noun","climate change","Klimaatferoaring hat grutte gefolgen."),("duorsum","adjective","sustainable","Wy wolle duorsume enerzjy."),("fersmoarging","noun","pollution","Fersmoarging skeint it miljeu."),("biodiversiteit","noun","biodiversity","Biodiversiteit moat beskerme wurde.")]),
_v("academic_c1","C1","Akademyske taal",[("gegevens","noun","data","De gegevens binne beheind."),("resultaat","noun","result","It resultaat stipet de hypoteze."),("konklúzje","noun","conclusion","De konklúzje folget út de gegevens."),("beheining","noun","limitation","De stúdzje hat ferskate beheiningen.")]),
_v("institutional_c1","C1","Bestjoer en belied",[("oanbefelling","noun","recommendation","De oanbefelling is dúdlik."),("útfiering","noun","implementation","De útfiering begjint yn jannewaris."),("belutsen partij","noun","stakeholder","De belutsen partijen waarden rieplachte."),("ynfloedanalyse","noun","impact assessment","De ynfloedanalyse is tafoege.")]),
_v("rhetoric_c2","C2","Retoryk en styl",[("foarming","noun","framing","De foarming beynfloedet de ynterpretaasje."),("ymplisyt","adjective","implicit","De tekst befettet in ymplisite oanname."),("nuânse","noun","nuance","De wurdkar bringt in oare nuânse."),("tsjinstelling","noun","contrast/opposition","De tekst bout in dúdlike tsjinstelling op.")]),
_v("idioms_c2","C2","Fêste útdrukkingen",[("rekken hâlde mei","phrase","take into account","Wy moatte mei alle belangen rekken hâlde."),("in konklúzje lûke","phrase","draw a conclusion","Wy kinne hjir gjin fêste konklúzje út lûke."),("it punt reitsje","phrase","hit the point","Syn antwurd rekket it punt."),("om 'e nocht","phrase","in vain","It sykjen wie om 'e nocht.")])
]

_TITLES={"A1":["Groetnis en identiteit","Famylje en minsken","Thús en dingen","Deistige routines","Iten en winkeljen","Plakken en rjochtingen","Petear en help","A1-kertier en werhelling"],"A2":["Tiid en plannen","Reizen en ferfier","Sûnens en wolwêzen","Underfiningen út it ferline","Fergelykje en beskriuwe","Tsjinsten en saken dwaan","Miening en petear","A2-kertier en werhelling"],"B1":["Wurk en stúdzje","Modale tiidwurden","Skiedbere tiidwurden","Bysin en ferbining","Relatyf beskriuwe","Betingsten","Referinsje en petear","B1-kertier en werhelling"],"B2":["Media en boarnen","Passyf en formeel taalgebrûk","Kontrast en tajefte","Mienskip en miljeu","Nominalisaasje","Tekstkohezje","Register en argumintaasje","B2-kertier en werhelling"],"C1":["Akademysk skriuwen","Komplekse bysinnen","Bestjoer en wurk","Foarsichtigens en evidinsje","Argumintaasje","Pragmatyk en toan","Tekstredaksje","C1-kertier en werhelling"],"C2":["Retoryske analyze","Register en styl","Oersettingskrektens","Literêre nuânses","Diskursanalyse","Avansearre argumintaasje","Taalkundige redaksje","C2-kertier en werhelling"]}
_GR={"A1":["pronouns","word-order","present","questions","negation","articles","possessives","locations"],"A2":["past","perfect","future","comparatives","imperative","modal-verbs","separable-verbs","subordination"],"B1":["modal-verbs","separable-verbs","subordination","relative","conditional","reported-speech","passive","aspect"],"B2":["passive","aspect","concession","discourse-connectors","nominalization","register","complex-subordination","argumentation"],"C1":["academic-hedging","complex-subordination","argumentation","institutional","pragmatics","nominalization","register","discourse-connectors"],"C2":["rhetoric","translation","literary-style","discourse-analysis","argumentation","pragmatics","register","complex-subordination"]}
_V={"A1":["greetings_a1","identity_a1","family_a1","home_a1","daily_a1","food_a1","identity_a1","greetings_a1"],"A2":["places_a2","health_a2","food_a1","daily_a1","places_a2","health_a2","identity_a1","places_a2"],"B1":["work_b1","education_b1","society_b1","work_b1","education_b1","society_b1","work_b1","education_b1"],"B2":["media_b2","environment_b2","society_b1","work_b1","media_b2","environment_b2","media_b2","environment_b2"],"C1":["academic_c1","institutional_c1","work_b1","society_b1","academic_c1","institutional_c1","media_b2","academic_c1"],"C2":["rhetoric_c2","idioms_c2","academic_c1","institutional_c1","rhetoric_c2","idioms_c2","media_b2","rhetoric_c2"]}

CURRICULUM={}
for level,titles in _TITLES.items():
    CURRICULUM[level]=[]
    for n,title in enumerate(titles,1):
        gs=_GR[level] if n==8 else [_GR[level][(n-1)%len(_GR[level])],_GR[level][n%len(_GR[level])]]
        CURRICULUM[level].append(CurriculumUnit(id=f"fy-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=gs,vocabulary_set_ids=[_V[level][n-1]],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=[f"Brûk it Frysk yn: {title.lower()}","Kombinearje de nije strukturen yn in koarte kommunikaasjetaak"],default_weeks=2))

def _p(i,s,phrases):
    return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in phrases])
PHRASEBOOK_CATEGORIES=[
_p("greetings_a1","Groetnis en yntroduksje",[("Goeiemoarn!","greeting","neutral"),("Myn namme is Anna.","introducing yourself","neutral"),("Leuk dy te moetsjen.","meeting someone","neutral")]),
_p("daily_a1","Deistich libben",[("Hoe giet it mei dy?","asking how someone is","neutral"),("It giet goed mei my.","answering","neutral"),("Oant moarn!","saying goodbye","neutral")]),
_p("shopping_a1","Winkeljen",[("Wat kostet dit?","asking a price","neutral"),("Ik wol graach twa broden.","buying food","neutral"),("Kin ik mei pin betelje?","payment","neutral")]),
_p("directions_a1","Rjochtingen",[("Wêr is it stasjon?","asking directions","neutral"),("Gean rjochtút.","giving directions","neutral"),("Gean nei links.","giving directions","neutral")]),
_p("help_a1","Help en ferdúdliking",[("Kinst my helpe?","asking for help","neutral"),("Ik begryp it net.","asking for clarification","neutral"),("Kinst it stadiger sizze?","asking someone to slow down","neutral")]),
_p("work_b1","Wurk",[("Kinsto de gearkomste befêstigje?","confirming a meeting","polite"),("Ik stjoer de ynformaasje hjoed.","follow-up","neutral"),("Kinst de deadline ferdúdlikje?","clarifying a deadline","polite")]),
_p("academic_c1","Akademysk petear",[("De gegevens wize derop dat…","introducing evidence","formal"),("Dizze ynterpretaasje moat foarsichtich besjoen wurde.","critical discussion","formal"),("Kin dizze konklúzje generalisearre wurde?","asking about generalization","formal")]),
_p("formal_c1","Formele kommunikaasje",[("Ik freegje jo freonlik om mear ynformaasje.","formal inquiry","formal"),("It fersyk is binnen de termyn yntsjinne.","administrative update","formal"),("Tank foar jo antwurd.","formal thanks","formal")])
]

ASSESSMENT_BANK=[
AssessmentQuestion(id="fy-a1-001",skill="grammar",difficulty="A1",question="Which sentence means “I do not understand”?",options=["Ik begryp it net.","Ik net begryp it.","Ik begryp gjin.","Ik begryp it."],correct="Ik begryp it net."),
AssessmentQuestion(id="fy-a1-002",skill="grammar",difficulty="A1",question="Which question asks where someone lives?",options=["Wêr wenje do?","Wêr do wenje?","Do wêr wenje?","Wêr wenjen do?"],correct="Wêr wenje do?"),
AssessmentQuestion(id="fy-a2-001",skill="grammar",difficulty="A2",question="Which sentence refers clearly to a past event?",options=["Juster wurke ik thús.","Moarn wurkje ik thús.","Ik wurkje thús.","Ik sil thús wurkje."],correct="Juster wurke ik thús."),
AssessmentQuestion(id="fy-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["As ik tiid ha, kom ik.","Ik kom hjoed.","Ik kaam juster.","Kom hjir!"],correct="As ik tiid ha, kom ik."),
AssessmentQuestion(id="fy-b2-001",skill="grammar",difficulty="B2",question="Which sentence uses a passive construction?",options=["It hûs wurdt boud.","Ik bou it hûs.","Wy bouwe in hûs.","Hy boude it hûs."],correct="It hûs wurdt boud."),
AssessmentQuestion(id="fy-c1-001",skill="reading",difficulty="C1",question="Which phrase signals a cautious academic claim?",options=["It liket derop dat de resultaten ferskille.","Dit bewiist alles.","Elkenien wit dit.","It is absolút wis."],correct="It liket derop dat de resultaten ferskille."),
AssessmentQuestion(id="fy-c2-001",skill="communication",difficulty="C2",question="What should an accurate Frisian translation preserve?",options=["Register, modality, idiom and information structure.","Only word order.","Only individual words.","No stylistic distinctions."],correct="Register, modality, idiom and information structure.")
]

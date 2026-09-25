"""Latvian curriculum foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS = ["A1","A2","B1","B2","C1","C2"]

def _g(slug,title,level,explanation,examples):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=f"Latvian {level} grammar for real communication.",explanation=explanation,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS=[
_g("pronouns","Personas vietniekvārdi","A1","Use personal reference in introductions and everyday exchanges.",["Es esmu students.","Viņa ir mana draudzene."]),
_g("present","Tagadnes laiks","A1","Describe current actions and routines with common present-tense forms.",["Es mācos latviešu valodu.","Mēs dzīvojam Rīgā."]),
_g("questions","Jautājuma teikumi","A1","Ask basic information and yes/no questions.",["Kur tu dzīvo?","Vai tu runā latviski?"]),
_g("cases","Locījumi un prievārdi","A2","Use Latvian case endings with common prepositions and locations.",["Es dzīvoju Rīgā.","Es eju uz skolu."]),
_g("past","Pagātnes laiks","A2","Describe completed events in the past.",["Vakar es strādāju mājās.","Viņa vakar lasīja grāmatu."]),
_g("future","Nākotnes laiks","A2","Discuss plans, intentions and future events.",["Rīt es mācīšos.","Mēs brauksim uz Liepāju."]),
_g("aspect","Darbības veida nozīme","B1","Distinguish ongoing, completed and repeated actions through verb choice and context.",["Es visu vakaru lasīju.","Es izlasīju rakstu."]),
_g("comparatives","Salīdzinājuma pakāpes","B1","Compare objects, people and situations accurately.",["Šis ceļš ir īsāks.","Tas ir labākais risinājums."]),
_g("conditional","Vēlējuma un nosacījuma izteiksme","B2","Express hypothetical situations, wishes and advice.",["Ja man būtu laiks, es ceļotu.","Es gribētu uzzināt vairāk."]),
_g("relative","Relatīvie teikumi","B2","Link clauses and identify people or objects precisely.",["Grāmata, kuru es lasu, ir interesanta.","Cilvēks, ar kuru es runāju, ir skolotājs."]),
_g("reported-speech","Netiešā runa","C1","Report statements while maintaining reference and discourse relationships.",["Viņš teica, ka rīt ieradīsies.","Viņa paskaidroja, ka sanāksme ir atcelta."]),
_g("nominalization","Nominalizācija un formālais stils","C1","Use formal nominal structures in academic and professional Latvian.",["Lēmuma pieņemšana aizņēma laiku.","Pētījuma rezultātu analīze turpinās."]),
_g("complex-syntax","Sarežģīta sintakse","C2","Control coordination, subordination, information structure and nuanced connectors.",["Lai gan rezultāti bija negaidīti, secinājumi apstiprināja sākotnējo hipotēzi."]),
_g("register","Stils un pragmatika","C2","Select appropriate informal, professional, academic and formal language.",["Vēlos noskaidrot iespēju piedalīties projektā.","Būsim pateicīgi, ja sniegsiet papildu informāciju."]),
]

def _v(id,level,topic,unit,items):
    return VocabularySet(id=id,level=level,topic=topic,unit_ref=unit,words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in items])

VOCABULARY_SETS=[
_v("lv_a1_greetings","A1","greetings","lv-a1-unit-1",[("sveiki","expression","hello","Sveiki! Kā jums klājas?"),("labdien","expression","good afternoon/hello","Labdien, kundze."),("paldies","word","thank you","Paldies par palīdzību."),("lūdzu","word","please/you are welcome","Lūdzu, apsēdieties."),("uz redzēšanos","expression","goodbye","Uz redzēšanos, līdz rītdienai.")]),
_v("lv_a1_identity","A1","identity","lv-a1-unit-2",[("vārds","noun","name","Kā tevi sauc?"),("uzvārds","noun","surname","Mans uzvārds ir Ozols."),("students","noun","student","Es esmu students."),("draugs","noun","friend","Tas ir mans draugs."),("dzīvot","verb","to live","Es dzīvoju Latvijā.")]),
_v("lv_a1_family","A1","family","lv-a1-unit-3",[("māte","noun","mother","Mana māte ir mājās."),("tēvs","noun","father","Mans tēvs strādā."),("brālis","noun","brother","Man ir viens brālis."),("māsa","noun","sister","Mana māsa studē."),("ģimene","noun","family","Mana ģimene dzīvo pilsētā.")]),
_v("lv_a1_home","A1","home","lv-a1-unit-4",[("māja","noun","house","Mana māja ir liela."),("dzīvoklis","noun","apartment","Es dzīvoju mazā dzīvoklī."),("istaba","noun","room","Mana istaba ir gaiša."),("virtuve","noun","kitchen","Virtuve ir blakus viesistabai."),("galds","noun","table","Grāmata ir uz galda.")]),
_v("lv_a1_daily","A1","daily life","lv-a1-unit-5",[("rīts","noun","morning","No rīta es dzeru kafiju."),("darbs","noun","work","Es eju uz darbu astoņos."),("mācīties","verb","to study","Es katru dienu mācos latviešu valodu."),("šodien","adverb","today","Šodien es esmu mājās."),("rīt","adverb","tomorrow","Rīt es strādāšu.")]),
_v("lv_a1_food","A1","food","lv-a1-unit-6",[("maize","noun","bread","Es pērku svaigu maizi."),("ūdens","noun","water","Dzeriet vairāk ūdens."),("ābols","noun","apple","Es ēdu ābolu."),("tēja","noun","tea","Es gribētu tēju."),("garšīgs","adjective","tasty","Ēdiens ir ļoti garšīgs.")]),
_v("lv_a1_places","A1","places","lv-a1-unit-7",[("skola","noun","school","Skola ir netālu."),("slimnīca","noun","hospital","Kur atrodas slimnīca?"),("veikals","noun","shop","Veikals ir slēgts."),("iela","noun","street","Es dzīvoju šajā ielā."),("stacija","noun","station","Stacija atrodas centrā.")]),
_v("lv_a1_communication","A1","communication","lv-a1-unit-8",[("saprast","verb","to understand","Es saprotu jautājumu."),("atkārtot","verb","to repeat","Lūdzu, atkārtojiet."),("palīdzība","noun","help","Man vajag palīdzību."),("jautājums","noun","question","Man ir jautājums."),("runāt","verb","to speak","Vai jūs runājat angliski?")]),
_v("lv_a2_time","A2","time and plans","lv-a2-unit-1",[("pagājušajā nedēļā","expression","last week","Pagājušajā nedēļā biju Cēsīs."),("nākamajā mēnesī","expression","next month","Nākamajā mēnesī ceļosim."),("bieži","adverb","often","Es bieži braucu ar autobusu."),("dažreiz","adverb","sometimes","Dažreiz strādāju no mājām."),("vēlāk","adverb","later","Tiksimies vēlāk.")]),
_v("lv_a2_services","A2","services","lv-a2-unit-2",[("rēķins","noun","bill","Lūdzu, rēķinu."),("pasūtījums","noun","order","Mans pasūtījums ir gatavs."),("biļete","noun","ticket","Es nopirku biļeti."),("reģistrācija","noun","registration","Reģistrācija sākas no rīta."),("cena","noun","price","Kāda ir šīs preces cena?")]),
_v("lv_a2_travel","A2","travel","lv-a2-unit-3",[("ceļojums","noun","trip","Ceļojums bija garš."),("lidosta","noun","airport","Lidosta atrodas ārpus pilsētas."),("vilciens","noun","train","Vilciens atiet deviņos."),("viesnīca","noun","hotel","Viesnīca atrodas centrā."),("karte","noun","map","Kur es varu dabūt karti?")]),
_v("lv_b1_work","B1","work","lv-b1-unit-1",[("sanāksme","noun","meeting","Rīt mums ir svarīga sanāksme."),("termiņš","noun","deadline","Projekta termiņš tuvojas."),("uzdevums","noun","task","Šo uzdevumu izpildīšu šodien."),("pieredze","noun","experience","Man ir piecu gadu pieredze."),("atbildība","noun","responsibility","Tā ir liela atbildība.")]),
_v("lv_b1_society","B1","society","lv-b1-unit-2",[("kopiena","noun","community","Kopiena organizē pasākumu."),("vide","noun","environment","Mums jāsargā vide."),("risinājums","noun","solution","Mums jāatrod risinājums."),("viedoklis","noun","opinion","Kāds ir jūsu viedoklis?"),("likums","noun","law","Jaunais likums stājās spēkā.")]),
_v("lv_b2_argumentation","B2","argumentation","lv-b2-unit-1",[("pierādījums","noun","evidence","Jāiesniedz pierādījumi."),("pieņēmums","noun","assumption","Šis pieņēmums nav pietiekami pamatots."),("secinājums","noun","conclusion","Pētījuma secinājums ir skaidrs."),("iemesls","noun","reason/cause","Svarīgi noteikt iemeslu."),("sekas","noun","consequences","Lēmumam būs ilgtermiņa sekas.")]),
_v("lv_b2_media","B2","media","lv-b2-unit-2",[("avots","noun","source","Pārbaudiet informācijas avotu."),("ziņojums","noun","report/announcement","Izlasīju oficiālo ziņojumu."),("sabiedrības viedoklis","noun phrase","public opinion","Sabiedrības viedoklis mainījās."),("neobjektivitāte","noun","bias","Rakstā redzama neobjektivitāte."),("uzticams","adjective","reliable","Tas ir uzticams avots.")]),
_v("lv_c1_academic","C1","academic language","lv-c1-unit-1",[("pētījums","noun","research/study","Pētījums atklāja jaunus rezultātus."),("metodoloģija","noun","methodology","Metodoloģija aprakstīta ziņojumā."),("hipotēze","noun","hypothesis","Hipotēze tika pārbaudīta."),("dati","noun","data","Dati tika analizēti vairākus mēnešus."),("būtībā","adverb","essentially","Būtībā šie rezultāti sakrīt.")]),
_v("lv_c1_professional","C1","professional","lv-c1-unit-2",[("īstenot","verb","to implement","Plāns jāīsteno pa posmiem."),("sadarboties","verb","to cooperate","Uzņēmumi sāka sadarboties."),("prioritāte","noun","priority","Drošība ir galvenā prioritāte."),("efektivitāte","noun","effectiveness","Mēs novērtējām pasākuma efektivitāti."),("ņemt vērā","verb phrase","to take into account","Jāņem vērā visi apstākļi.")]),
_v("lv_c2_nuance","C2","nuance","lv-c2-unit-1",[("nianse","noun","nuance","Šī nianse maina teikuma nozīmi."),("divdomīgs","adjective","ambiguous","Formulējums var būt divdomīgs."),("konotācija","noun","connotation","Vārdam ir negatīva konotācija."),("nosacīti","adverb","conditionally/relatively","Šo apgalvojumu var pieņemt tikai nosacīti."),("smalks","adjective","subtle","Tā ir smalka stilistiska atšķirība.")]),
_v("lv_c2_formal","C2","formal style","lv-c2-unit-2",[("ņemot vērā","expression","in view of","Ņemot vērā apstākļus, lēmums tiek atlikts."),("jāuzsver","expression","it should be emphasized","Jāuzsver, ka dati nav galīgi."),("var uzskatīt","expression","it may be considered","Var uzskatīt, ka pasākums būs efektīvs."),("neskatoties uz","preposition","despite","Neskatoties uz grūtībām, projekts turpinās."),("attiecīgi","adverb","accordingly","Rezultāti attiecīgi tika koriģēti.")]),
]

PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="lv_a1_greetings",level="A1",situation="greetings",icon="👋",phrases=[PhrasebookEntry(text="Labdien!",context="polite greeting",register="formal"),PhrasebookEntry(text="Kā tev klājas?",context="asking how someone is",register="neutral"),PhrasebookEntry(text="Prieks iepazīties.",context="first meeting",register="neutral")]),
PhrasebookCategory(id="lv_a1_daily",level="A1",situation="daily",icon="☀️",phrases=[PhrasebookEntry(text="Es nesaprotu.",context="asking for clarification",register="neutral"),PhrasebookEntry(text="Lūdzu, atkārtojiet.",context="asking someone to repeat",register="polite"),PhrasebookEntry(text="Kur ir tualete?",context="finding a facility",register="neutral")]),
PhrasebookCategory(id="lv_a2_shopping",level="A2",situation="shopping",icon="🛒",phrases=[PhrasebookEntry(text="Cik tas maksā?",context="asking price",register="neutral"),PhrasebookEntry(text="Vai var maksāt ar karti?",context="payment",register="polite"),PhrasebookEntry(text="Es vēlētos to atgriezt.",context="returning an item",register="polite")]),
PhrasebookCategory(id="lv_a2_travel",level="A2",situation="travel",icon="🧭",phrases=[PhrasebookEntry(text="Kur atrodas dzelzceļa stacija?",context="asking directions",register="neutral"),PhrasebookEntry(text="Kad atiet autobuss?",context="transport schedule",register="neutral"),PhrasebookEntry(text="Man vajag biļeti uz Rīgu.",context="buying a ticket",register="neutral")]),
PhrasebookCategory(id="lv_b1_work",level="B1",situation="work",icon="💼",phrases=[PhrasebookEntry(text="Vai varam apspriest šo jautājumu?",context="work discussion",register="professional"),PhrasebookEntry(text="Ierosinu tikties nākamnedēļ.",context="making a proposal",register="professional"),PhrasebookEntry(text="Atbildi sniegšu līdz piektdienai.",context="setting a deadline",register="professional")]),
PhrasebookCategory(id="lv_b2_discussion",level="B2",situation="discussion",icon="💬",phrases=[PhrasebookEntry(text="Manuprāt, ir svarīgi ņemt vērā kontekstu.",context="argumentation",register="formal"),PhrasebookEntry(text="Šis apgalvojums būtu jāpamato ar datiem.",context="critical discussion",register="formal"),PhrasebookEntry(text="Tomēr pastāv arī cita perspektīva.",context="introducing contrast",register="neutral")]),
PhrasebookCategory(id="lv_c1_academic",level="C1",situation="academic",icon="🎓",phrases=[PhrasebookEntry(text="Pētījuma rezultāti liecina, ka...",context="presenting findings",register="academic"),PhrasebookEntry(text="Šis pieņēmums prasa papildu pamatojumu.",context="academic critique",register="academic"),PhrasebookEntry(text="Apkopojot var secināt, ka...",context="conclusion",register="academic")]),
PhrasebookCategory(id="lv_c2_formal",level="C2",situation="formal",icon="🏛️",phrases=[PhrasebookEntry(text="Ņemot vērā iepriekš izklāstītos apstākļus...",context="formal writing",register="formal"),PhrasebookEntry(text="Jāuzsver, ka šis vērtējums nav galīgs.",context="qualified statement",register="formal"),PhrasebookEntry(text="Būsim pateicīgi, ja sniegsiet papildu informāciju.",context="formal request",register="formal")]),
]

TITLES={
"A1":["Sveicieni un iepazīšanās","Ģimene un cilvēki","Māja un lietas","Ikdiena","Ēdiens un iepirkšanās","Vietas un virzieni","Saziņa un palīdzība","A1 atkārtojums"],
"A2":["Laiks un plāni","Pakalpojumi un nauda","Ceļošana","Veselība un pašsajūta","Mācības un darbs","Brīvais laiks","Pieredze un viedokļi","A2 atkārtojums"],
"B1":["Darbs un atbildība","Kopiena un sabiedrība","Ziņas un informācija","Attiecības un problēmu risināšana","Kultūra un identitāte","Vide un dzīvesveids","Argumentācija","B1 atkārtojums"],
"B2":["Argumenti un pierādījumi","Mediji un kritiskā domāšana","Profesionālā saziņa","Sabiedrības jautājumi","Zinātne un tehnoloģijas","Debates un perspektīvas","Stils un precizitāte","B2 atkārtojums"],
"C1":["Akadēmiskais diskurss","Profesionālā komunikācija","Pētījumi un metodoloģija","Sarežģīti teksti","Publiskā runa","Analīze un sintēze","Reģistrs un stils","C1 atkārtojums"],
"C2":["Stilistiskā kontrole","Nozīmes nianses","Akadēmiskā argumentācija","Profesionālais un administratīvais stils","Retorika un diskurss","Vērtēšana un kritika","Idiomātika un pragmatika","C2 integrācija"],
}
G_BY={"A1":["pronouns","present","questions"],"A2":["cases","past","future"],"B1":["aspect","comparatives"],"B2":["conditional","relative"],"C1":["reported-speech","nominalization"],"C2":["complex-syntax","register"]}
V_BY={"A1":["lv_a1_greetings","lv_a1_identity","lv_a1_family","lv_a1_home","lv_a1_daily","lv_a1_food","lv_a1_places","lv_a1_communication"],"A2":["lv_a2_time","lv_a2_services","lv_a2_travel"],"B1":["lv_b1_work","lv_b1_society"],"B2":["lv_b2_argumentation","lv_b2_media"],"C1":["lv_c1_academic","lv_c1_professional"],"C2":["lv_c2_nuance","lv_c2_formal"]}

CURRICULUM={}
for level in LEVELS:
    CURRICULUM[level]=[
        CurriculumUnit(id=f"lv-{level.lower()}-unit-{i}",level=level,unit_number=i,title=TITLES[level][i-1],
            grammar_points=G_BY[level] if i==1 else [G_BY[level][(i-1)%len(G_BY[level])]],
            vocabulary_set_ids=V_BY[level] if i==1 else [V_BY[level][(i-1)%len(V_BY[level])]],
            lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],
            competency_checklist=["Understand and produce Latvian appropriate to the level.","Use target vocabulary in a realistic communicative task.","Demonstrate control of the unit grammar."],
            default_weeks=2 if level in {"A1","A2"} else 3) for i in range(1,9)
    ]

ASSESSMENT_BANK=[
AssessmentQuestion(id="lv-a1-001",skill="communication",difficulty="A1",question="How do you greet someone politely during the day?",options=["Labdien!","Uz redzēšanos!","Paldies.","Labrīt."],correct="Labdien!"),
AssessmentQuestion(id="lv-a1-002",skill="identity",difficulty="A1",question="Which sentence means 'I am a student'?",options=["Es esmu students.","Es dzīvoju Rīgā.","Man ir brālis.","Es strādāju mājās."],correct="Es esmu students."),
AssessmentQuestion(id="lv-a2-001",skill="grammar",difficulty="A2",question="Which sentence correctly describes yesterday?",options=["Vakar es strādāju mājās.","Rīt es strādāšu mājās.","Tagad es strādāju mājās.","Bieži es strādāšu mājās."],correct="Vakar es strādāju mājās."),
AssessmentQuestion(id="lv-a2-002",skill="travel",difficulty="A2",question="How do you ask when the bus leaves?",options=["Kad atiet autobuss?","Kur tu dzīvo?","Cik tas maksā?","Kā tev klājas?"],correct="Kad atiet autobuss?"),
AssessmentQuestion(id="lv-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a completed reading action?",options=["Es izlasīju rakstu.","Es visu vakaru lasīju.","Es rīt lasīšu.","Es tagad lasu."],correct="Es izlasīju rakstu."),
AssessmentQuestion(id="lv-b1-002",skill="argumentation",difficulty="B1",question="Which word means 'conclusion'?",options=["secinājums","pieņēmums","sekas","atbildība"],correct="secinājums"),
AssessmentQuestion(id="lv-b2-001",skill="grammar",difficulty="B2",question="Which sentence expresses a hypothetical condition?",options=["Ja man būtu laiks, es ceļotu.","Vakar es ceļoju.","Rīt es ceļošu.","Tagad es ceļoju."],correct="Ja man būtu laiks, es ceļotu."),
AssessmentQuestion(id="lv-b2-002",skill="reading",difficulty="B2",question="Which term means evidence supporting an argument?",options=["pierādījums","nianse","uzvārds","ceļojums"],correct="pierādījums"),
AssessmentQuestion(id="lv-c1-001",skill="academic",difficulty="C1",question="Which phrase introduces research findings?",options=["Pētījuma rezultāti liecina, ka...","Sveiki!","Cik tas maksā?","Kur ir stacija?"],correct="Pētījuma rezultāti liecina, ka..."),
AssessmentQuestion(id="lv-c1-002",skill="formal",difficulty="C1",question="Which expression is appropriate for a qualified formal statement?",options=["Var uzskatīt, ka pasākums būs efektīvs.","Sveiks, kas jauns?","Es gribu šo.","Kur ir tirgus?"],correct="Var uzskatīt, ka pasākums būs efektīvs."),
AssessmentQuestion(id="lv-c2-001",skill="pragmatics",difficulty="C2",question="Which expression refers formally to previously stated circumstances?",options=["Ņemot vērā iepriekš izklāstītos apstākļus...","Labrīt!","Cik tas maksā?","Es gribu ūdeni."],correct="Ņemot vērā iepriekš izklāstītos apstākļus..."),
AssessmentQuestion(id="lv-c2-002",skill="style",difficulty="C2",question="Which word describes a subtle stylistic difference?",options=["smalks","skaļš","ikdienas","ātrs"],correct="smalks"),
]

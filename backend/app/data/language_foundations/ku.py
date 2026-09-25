"""Kurdish (Kurmanji) A1-C2 foundation data for JUBA LISAN."""
from app.data._types import (
    AssessmentQuestion, CurriculumUnit, GrammarExample, GrammarTopic,
    PhrasebookCategory, PhrasebookEntry, VocabularyEntry, VocabularySet,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def g(slug, title, level, summary, examples, category="grammar"):
    return GrammarTopic(
        slug=slug, title=title, level=level, category=category,
        summary=summary, explanation=summary,
        examples=[GrammarExample(text=x) for x in examples],
    )


GRAMMAR_TOPICS = [
    g("pronouns", "Personal pronouns", "A1", "Use ez, tu, ew, em, hûn and ew in basic exchanges.", ["Ez xwendekar im.", "Tu mamoste yî."]),
    g("copula", "Present copula", "A1", "Use present copular forms for identity and description.", ["Ez mamoste me.", "Ew xwendekar e."]),
    g("present", "Present tense", "A1", "Describe current and habitual actions with present forms.", ["Ez kurdî fêr dibim.", "Ew her roj dixebite."]),
    g("questions", "Questions and question words", "A1", "Ask yes-no and information questions with çi, kî, li ku and çawa.", ["Tu çawa yî?", "Tu li ku dijî?"]),
    g("negation", "Negation", "A1", "Negate copular and verbal clauses with ne and na-.", ["Ez mamoste nînim.", "Ez nizanim."]),
    g("demonstratives", "Demonstratives", "A1", "Point to people and things with ev and ew.", ["Ev pirtûk e.", "Ew mal e."]),
    g("possessive", "Possession", "A1", "Express ownership with possessive pronouns and izafe structures.", ["Ev pirtûka min e.", "Mala bavê min mezin e."]),
    g("location", "Location and prepositions", "A1", "Describe location using li and common spatial expressions.", ["Pirtûk li ser maseyê ye.", "Ez li Hewlêrê dijîm."]),
    g("plural", "Plural nouns", "A2", "Form and use common plural noun patterns.", ["Pirtûkên nû hene.", "Zarok li dibistanê ne."]),
    g("past", "Simple past", "A2", "Describe completed events using past-tense forms.", ["Min duh pirtûk xwend.", "Ew çû bajarê."]),
    g("future", "Future and intention", "A2", "Express plans and expected events with dê and related structures.", ["Ez ê sibê werim.", "Ew ê bixwîne."]),
    g("progressive", "Progressive meaning", "A2", "Describe actions currently in progress and temporary states.", ["Ez niha dixwînim.", "Ew li malê dixebite."]),
    g("imperative", "Imperatives and polite requests", "A2", "Give instructions and make direct or polite requests.", ["Were vir!", "Ji kerema xwe re dîsa bibêje."]),
    g("comparatives", "Comparison", "A2", "Compare people and things with zêdetir, kêm and herî.", ["Ev ji wê mezintir e.", "Ew herî baş e."]),
    g("oblique", "Oblique and ezafe constructions", "B1", "Use oblique forms and izafe chains accurately in expanded noun phrases.", ["Kitêba mamosteyê nû ye.", "Min bi hevalê xwe re axivî."]),
    g("modal", "Ability, necessity and permission", "B1", "Express ability, obligation, possibility and permission.", ["Ez dikarim biçim.", "Divê em dest pê bikin."]),
    g("conditional", "Conditional clauses", "B1", "Build real and hypothetical conditions with heke/hger and appropriate verb forms.", ["Heke baran bibare, em dê li malê bimînin.", "Heger dem hebe, em dê hev bibînin."]),
    g("relative", "Relative clauses", "B1", "Modify nouns through relative clauses and ezafe structures.", ["Mirovê ku hat mamosteyê min e.", "Pirtûka ku min xwend baş bû."]),
    g("converbs", "Converbs and event sequencing", "B1", "Link actions through participial and converb-like structures.", ["Piştî ku xwend, ew derket.", "Bi kenîn re axivî."]),
    g("causal", "Cause, purpose and result", "B1", "Express reasons, purposes and consequences with ji ber ku, da ku and related connectors.", ["Ji ber ku baran dibarî, em man.", "Da ku fêr bibim, ez her roj dixwînim."]),
    g("reflexive", "Reflexive and reciprocal reference", "B1", "Refer back to participants and express reciprocal actions.", ["Ew xwe amade kir.", "Wan bi hev re axivî."]),
    g("reported", "Reported speech", "B2", "Report statements, questions and requests using ku and appropriate tense relationships.", ["Wî got ku dê were.", "Mamoste pirsî ka ez amade me."]),
    g("passive", "Passive constructions", "B2", "Present events from the affected participant's perspective.", ["Pirtûk hat çapkirin.", "Derî hat vekirin."]),
    g("aspect", "Aspect and event viewpoint", "B2", "Distinguish ongoing, habitual and completed event interpretations.", ["Min pirtûk dixwend.", "Min pirtûk xwendiye."]),
    g("subordination", "Complex subordination", "B2", "Combine clauses to express time, condition, cause and contrast.", ["Her çend ku westiyayî bû, ew berdewam kir.", "Dema ku ez hatim, ew çû."]),
    g("concession", "Contrast and concession", "B2", "Connect opposing propositions with lê, her çend and related structures.", ["Her çend dijwar bû, em dawî anîn.", "Ew hat, lê dem dereng bû."]),
    g("discourse", "Discourse connectors and cohesion", "B2", "Organize explanations with sequential, causal and contrastive connectors.", ["Pêşî em pirsgirêkê diyar dikin; paşê çareseriyê pêşniyar dikin."]),
    g("nominalization", "Nominalization", "C1", "Use noun-based structures for formal and analytical discourse.", ["Pêkanîna planê girîng e.", "Biryardana rast şert e."]),
    g("hedging", "Academic hedging and stance", "C1", "Qualify claims and distinguish evidence from interpretation.", ["Dibe ku ev encam ji şertan ve girêdayî be.", "Ev dîtin dikare pêdiviya lêkolîna zêdetir nîşan bide."]),
    g("embedded_questions", "Embedded questions", "C1", "Embed questions inside reports, explanations and formal requests.", ["Em nizanin ka ew kengî dê were.", "Ez dixwazim bizanim çima ev bû."]),
    g("information_structure", "Topic and focus", "C1", "Control emphasis through constituent order, context and contrast.", ["Ev pirsgirêk em îro tenê nîqaş dikin.", "Ya girîng ew e ku em planê pêk bînin."]),
    g("formal_register", "Formal and institutional Kurmanji", "C1", "Adapt language to administrative, professional and public contexts.", ["Ji bo ragihandina zêdetir, ji kerema xwe re forma pêvek dagirin."]),
    g("argumentation", "Academic argumentation", "C1", "Present claims, evidence, counterarguments and conclusions coherently.", ["Li gorî daneyên heyî, em dikarin encameke maqûl derxin."]),
    g("pragmatics", "Pragmatics and politeness", "C2", "Manage indirectness, respect, emphasis and social meaning.", ["Heke gengaz be, dikarin vê mijarê careke din binirxînin?"]),
    g("rhetoric", "Rhetorical and literary style", "C2", "Use metaphor, parallelism and stylistic variation appropriately.", ["Ev gotin wêneyek hêzdar ji guherîna civakî çêdike."]),
    g("translation", "Translation precision", "C2", "Preserve meaning, register and discourse function across contexts.", ["Termînolojî divê li gorî bikaranîna warê were wergerandin."]),
    g("discourse_analysis", "Discourse analysis and register shifting", "C2", "Analyze genre, cohesion, stance and shifts between spoken and written language.", ["Şêwaza nivîsandina fermî ji axaftina rojane cuda ye."]),
]

def v(i, level, topic, words):
    return VocabularySet(
        id=i, level=level, topic=topic, unit_ref=i,
        words=[VocabularyEntry(word=w, pos=p, definition=d, example=e) for w, p, d, e in words],
    )

VOCABULARY_SETS = [
    v("greetings_a1", "A1", "Silav û nasîn", [("silav","phrase","hello","Silav!"),("spas","phrase","thanks","Spas ji bo alîkariya te."),("nav","noun","name","Navê min Azad e."),("heval","noun","friend","Ew hevalê min e.")]),
    v("identity_a1", "A1", "Nasname", [("xwendekar","noun","student","Ez xwendekar im."),("mamoste","noun","teacher","Ew mamoste ye."),("jin","noun","woman","Ew jin e."),("mêr","noun","man","Ew mêr e.")]),
    v("family_a1", "A1", "Malbat", [("dayik","noun","mother","Dayika min li malê ye."),("bav","noun","father","Bavê min dixebite."),("birayê","noun","brother","Birayê min li dibistanê ye."),("xwişk","noun","sister","Xwişka min dixwîne.")]),
    v("home_a1", "A1", "Mal", [("mal","noun","home","Mala me mezin e."),("ode","noun","room","Odeya min paqij e."),("derî","noun","door","Derî vekirî ye."),("mase","noun","table","Pirtûk li ser maseyê ye.")]),
    v("daily_a1", "A1", "Jiyana rojane", [("sibeh","noun","morning","Sibeh ez dixebitim."),("roj","noun","day","Îro rojeke baş e."),("kar","noun","work","Karê min dijwar e."),("av","noun","water","Ez av dixwazim.")]),
    v("food_a1", "A1", "Xwarin", [("nan","noun","bread","Ez nan dixwim."),("çay","noun","tea","Ez çay dixwim."),("pirinc","noun","rice","Pirinc germ e."),("sêv","noun","apple","Sêvek sor e.")]),
    v("places_a1", "A1", "Cih û rê", [("bazaar","noun","market","Bazaar li vir e."),("dibistan","noun","school","Dibistan nêzîk e."),("nexweşxane","noun","hospital","Nexweşxane li ku ye?"),("rê","noun","road","Rê li ber me ye.")]),
    v("communication_a1", "A1", "Ragihandin", [("pirs","noun","question","Pirseke min heye."),("alîkarî","noun","help","Ji kerema xwe re alîkarî bike."),("ziman","noun","language","Kurdî zimanek e."),("axaftin","noun","speaking","Axaftina wî zelal e.")]),
    v("people_a2", "A2", "Mirov û civak", [("cîran","noun","neighbor","Cîranê me baş e."),("zêvî","noun","guest","Zêvî hat."),("kom","noun","group","Kom mezin e."),("pîşeyî","adjective","professional","Ew mirovê pîşeyî ye.")]),
    v("travel_a2", "A2", "Rêwîtî", [("balafir","noun","airplane","Balafir sibeh radibe."),("trên","noun","train","Trên hat."),("bilêt","noun","ticket","Bilêt ji ku tê kirîn?"),("otêl","noun","hotel","Em li otêlê dimînin.")]),
    v("health_a2", "A2", "Tenduristî", [("bijîşk","noun","doctor","Bijîşk li vir e."),("dijwarî","noun","pain/difficulty","Ez êşê hîs dikim."),("derman","noun","medicine","Derman li ser maseyê ye."),("nexweşxane","noun","hospital","Nexweşxane nêzîk e.")]),
    v("study_b1", "B1", "Xwendin û lêkolîn", [("lêkolîn","noun","research","Lêkolîn girîng e."),("erk","noun","assignment","Erkê xwe temam kir."),("azmûn","noun","exam","Azmûn sibê ye."),("mamoste","noun","teacher","Mamoste dersê rave dike.")]),
    v("work_b1", "B1", "Kar û pîşe", [("xebatkar","noun","employee","Xebatkar raporê şandin."),("civîn","noun","meeting","Civîn saet sêyan dest pê dike."),("ezmûn","noun","experience","Ezmûna wî zêde ye."),("berpirsyarî","noun","responsibility","Berpirsyariya min ev e.")]),
    v("society_b2", "B2", "Civak", [("civak","noun","society","Civak diguhere."),("pêşveçûn","noun","development","Pêşveçûn girîng e."),("siyaset","noun","policy/politics","Siyaseta nû tê nîqaşkirin."),("welatî","noun","citizen","Welatî mafên xwe dizane.")]),
    v("economy_b2", "B2", "Aborî", [("aborî","noun","economy","Aboriya herêmê mezin dibe."),("bazaar","noun","market","Bazaar daxwazê nîşan dide."),("veberhênan","noun","investment","Vebêrhênan zêde bû."),("hatin","noun","income","Hatina malbatê zêde bû.")]),
    v("media_c1", "C1", "Medya", [("agahî","noun","information","Agahî divê were piştrastkirin."),("nivîs","noun","article/text","Nivîs di rojnameyê de hat."),("çavkanî","noun","source","Çavkaniyê diyar kirin."),("hevpeyvîn","noun","interview","Ew hevpeyvîn da.")]),
    v("academic_c1", "C1", "Zimanê akademîk", [("lêkolîn","noun","research","Lêkolîna nû encamên girîng nîşan dide."),("delîl","noun","evidence","Delîl têr e."),("hîpotez","noun","hypothesis","Hîpotez tê ceribandin."),("encam","noun","conclusion/result","Encam bi delîlan re tê piştgirîkirin.")]),
    v("institutional_c1", "C1", "Zimanê fermî", [("rêzik","noun","regulation","Rêzik divê were şopandin."),("serlêdan","noun","application","Serlêdan hate wergirtin."),("biryar","noun","decision","Biryar bi fermî hate dayîn."),("pêkanîn","noun","implementation","Pêkanîna planê tê şopandin.")]),
    v("culture_c2", "C2", "Çand û edebiyat", [("mîras","noun","heritage","Mîrasa çandî divê were parastin."),("edebiyat","noun","literature","Edebiyata kurdî dewlemend e."),("wêne","noun","image/imagery","Nivîskar wêneyên hêzdar bikar tîne."),("sembol","noun","symbol","Sembol di nivîsê de girîng e.")]),
    v("discourse_c2", "C2", "Dîskurs û şêwe", [("şêwe","noun","style","Şêweya nivîsê fermî ye."),("ton","noun","tone","Tona gotinê girîng e."),("wateya veşartî","phrase","implicit meaning","Wateya veşartî bi kontekstê tê fêmkirin."),("termînolojî","noun","terminology","Termînolojî divê yekgirtî be.")]),
]

def p(i, level, situation, items, register="neutral"):
    return PhrasebookCategory(
        id=i, level=level, situation=situation, icon="💬",
        phrases=[PhrasebookEntry(text=t, context=c, register=register) for t, c in items],
    )

PHRASEBOOK_CATEGORIES = [
    p("greetings_a1","A1","Silav û nasîn",[("Silav!","greeting"),("Navê te çi ye?","asking a name"),("Ez ji bo nasîna te kêfxweş im.","meeting someone")]),
    p("thanks_a1","A1","Spas û lêborîn",[("Spas.","thanks"),("Ji kerema xwe re.","please"),("Bibore.","apology")]),
    p("shopping_a1","A1","Kirîn",[("Ev çend e?","asking price"),("Ez vê dixwazim.","requesting an item"),("Ma rengê din heye?","asking for another option")]),
    p("directions_a1","A1","Cih û rê",[("Bazaar li ku ye?","asking location"),("Dibistan li ku ye?","asking direction"),("Bi vê rê ve biçin.","giving directions")]),
    p("help_a1","A1","Alîkarî",[("Ji kerema xwe re alîkarî bike.","asking for help"),("Ez fêm nakim.","saying you do not understand"),("Ji kerema xwe re dîsa bibêje.","asking for repetition")]),
    p("travel_a2","A2","Rêwîtî",[("Bilêt ji ku tê kirîn?","buying a ticket"),("Otêl li ku ye?","finding a hotel"),("Rezervasyona min piştrast bikin.","confirming a booking")]),
    p("health_a2","A2","Tenduristî",[("Ez êşê hîs dikim.","describing pain"),("Ez dixwazim bijîşk bibînim.","requesting medical help"),("Ev derman çawa tê bikaranîn?","asking about medicine")]),
    p("study_b1","B1","Xwendin",[("Ev raman dikarî rave bikî?","asking for explanation"),("Erkê xwe di demê de didim.","discussing an assignment"),("Ez vê çavkaniyê bikar anîm.","citing a source")]),
    p("work_b1","B1","Kar",[("Were em civînê dest pê bikin.","starting a meeting"),("Bila em vê pirsgirêkê nîqaş bikin.","opening discussion"),("Raporê sibê dişînim.","work commitment")]),
    p("public_b2","B2","Nîqaşa giştî",[("Ev pirsgirêk ji çend hêmanan ve bandor dibe.","explaining causes"),("Ji aliyekî din ve...","introducing contrast"),("Li ser bingeha delîlan...","introducing evidence")],"formal"),
    p("academic_c1","C1","Nîqaşa akademîk",[("Ev lêkolîn nîşan dide ku...","stating a finding"),("Divê em vê encamê bi baldarî şîrove bikin.","hedging"),("Pêdivî ye ku ev mijar zêdetir were lêkolînkirin.","proposing further research")],"academic"),
    p("institutional_c1","C1","Ragihandina fermî",[("Serlêdan hate wergirtin.","acknowledging an application"),("Li gorî rêzikê dê biryar were dayîn.","formal procedure"),("Ji kerema xwe re agahiyên pêwendîdar bişînin.","formal request")],"formal"),
    p("rhetoric_c2","C2","Axaftina nuansdar",[("Hêjayî ye ku li ser vê xalê rawestin.","foregrounding a point"),("Em dikarin binirxînin ka ev şîrove têr e an na.","critical evaluation"),("Li pişt vê gotinê dibe ku wateyeke din hebe.","interpreting implicit meaning")],"formal"),
]

def u(level, number, title, grammar, vocab, a, b):
    return CurriculumUnit(
        id=f"ku-{level.lower()}-{number:02}",
        level=level, unit_number=number, title=title,
        grammar_points=grammar, vocabulary_set_ids=[vocab],
        lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],
        competency_checklist=[a,b], default_weeks=2,
    )

CURRICULUM = {
    "A1":[
        u("A1",1,"Silav û nasîn",["pronouns","copula"],"greetings_a1","Xwe nas dike","Silav li hev dike"),
        u("A1",2,"Nasname û malbat",["possessive","questions"],"identity_a1","Nasnameya xwe vedibêje","Pirsên bingehîn dike"),
        u("A1",3,"Mal û cih",["location","demonstratives"],"home_a1","Malê vedibêje","Cihê tiştan dibêje"),
        u("A1",4,"Jiyana rojane",["present","negation"],"daily_a1","Rutîna xwe vedibêje","Nehatiyê bişopîne"),
        u("A1",5,"Xwarin û kirîn",["questions","numbers"],"food_a1","Xwarin daxwaz dike","Buhayê dipirse"),
        u("A1",6,"Cih û rê",["location","questions"],"places_a1","Cih dipirse","Rê nîşan dide"),
        u("A1",7,"Ragihandin û alîkarî",["negation","questions"],"communication_a1","Nefêmkirinê vedibêje","Alîkarî dixwaze"),
        u("A1",8,"Dubarekirina A1",["present","possessive"],"greetings_a1","Di mijarên nas de diaxive","Diyaloga kurt pêk tîne"),
    ],
    "A2":[
        u("A2",1,"Mirov û civak",["plural","present"],"people_a2","Mirovan vedibêje","Rutîn û têkiliyên xwe vedibêje"),
        u("A2",2,"Rêwîtî",["past","future"],"travel_a2","Rêwîtiya borî vedibêje","Planê pêşerojê dide"),
        u("A2",3,"Tenduristî",["progressive","imperative"],"health_a2","Nîşanên nexweşiyê vedibêje","Daxwaza rêkûpêk dike"),
        u("A2",4,"Dem û plan",["future","questions"],"daily_a1","Planê xwe dide","Bernameyê diafirîne"),
        u("A2",5,"Berawird",["comparatives","plural"],"home_a1","Tiştan berawird dike","Cûdahiyê vedibêje"),
        u("A2",6,"Têkiliya bi rêz",["imperative","questions"],"communication_a1","Daxwaza rêzdar dike","Ravekirinê dipirse"),
        u("A2",7,"Xizmet û bajêr",["location","oblique"],"places_a1","Cihên xizmetê vedibêje","Rê û cihê rave dike"),
        u("A2",8,"Dubarekirina A2",["past","future"],"travel_a2","Borî û pêşerojê cuda dike","Di rewşên rêwîtiyê de diaxive"),
    ],
    "B1":[
        u("B1",1,"Xwendin û lêkolîn",["oblique","modal"],"study_b1","Pêvajoya xwendinê rave dike","Şîret dide"),
        u("B1",2,"Kar û pîşe",["modal","conditional"],"work_b1","Erkên karê vedibêje","Pêşniyara şertî dide"),
        u("B1",3,"Sedem û armanc",["causal","converbs"],"society_b2","Sedemê rave dike","Armancê vedibêje"),
        u("B1",4,"Şert û plan",["conditional","future"],"travel_a2","Plana şertî çêdike","Encama gengaz vedibêje"),
        u("B1",5,"Ravekirina navan",["relative","oblique"],"study_b1","Navan bi hûrgulî rave dike","Agahiyên zêde dide"),
        u("B1",6,"Rêza bûyeran",["converbs","past"],"daily_a1","Bûyeran li pey hev vedibêje","Pêvajoyê rave dike"),
        u("B1",7,"Çareserkirina pirsgirêkan",["causal","modal"],"work_b1","Sedem û çareseriyê vedibêje","Pêşniyar û pêdiviyê nîşan dide"),
        u("B1",8,"Dubarekirina B1",["relative","conditional"],"study_b1","Hevokên tevlihev bikar tîne","Li ser xwendin û karê diaxive"),
    ],
    "B2":[
        u("B2",1,"Axaftina neyekser",["reported","subordination"],"media_c1","Gotinên kesên din vedibêje","Çavkaniyan cuda dike"),
        u("B2",2,"Pasîf û perspektîf",["passive","aspect"],"institutional_c1","Perspektîfa bûyerê diguhezîne","Dem û pêvajoyê cuda dike"),
        u("B2",3,"Delîl û texmîn",["evidentiality","modal"],"academic_c1","Asta delîlê nîşan dide","Texmîna baldar dike"),
        u("B2",4,"Berawird û lihevhatin",["concession","discourse"],"society_b2","Ramanên dijber girê dide","Lihevhatinê rave dike"),
        u("B2",5,"Aborî",["reported","causal"],"economy_b2","Agahiyên aborî rave dike","Sedem û encamê girê dide"),
        u("B2",6,"Pirsgirêkên civakî",["discourse","concession"],"society_b2","Pirsgirêkên pir-alî nîqaş dike","Nêrînên dijber dide"),
        u("B2",7,"Nivîsên medyayê",["reported","evidentiality"],"media_c1","Çavkaniya agahiyê rave dike","Rastî û texmînê cuda dike"),
        u("B2",8,"Dubarekirina B2",["passive","discourse"],"media_c1","Agahiyên tevlihev dike yek","Ravekirina dirêj dide"),
    ],
    "C1":[
        u("C1",1,"Zimanê fermî",["nominalization","formal_register"],"institutional_c1","Bi şêwazê fermî dinivîse","Pêvajoyan bi navan vedike"),
        u("C1",2,"Zimanê akademîk",["hedging","evidentiality"],"academic_c1","Asta baweriyê nîşan dide","Encama baldar dide"),
        u("C1",3,"Hevokên tevlihev",["subordination","embedded_questions"],"academic_c1","Ramanên tevlihev ava dike","Pirsên veşartî bikar tîne"),
        u("C1",4,"Mijar û girîngkirin",["information_structure","discourse"],"discourse_c2","Agahiyên girîng rêk dixe","Li gorî kontekstê rêza peyvan hilbijêre"),
        u("C1",5,"Ragihandina sazî",["formal_register","nominalization"],"institutional_c1","Nivîsa fermî bikar tîne","Proseduran rave dike"),
        u("C1",6,"Argumenta akademîk",["argumentation","hedging"],"academic_c1","Argument bi delîlan ava dike","Nêrîna dijber dixe ber çavan"),
        u("C1",7,"Medya û siyaseta giştî",["information_structure","formal_register"],"media_c1","Ragihandina giştî analîz dike","Tonê fermî diguhezîne"),
        u("C1",8,"Dubarekirina C1",["subordination","argumentation"],"academic_c1","Şirovekirina akademîk dirêj dinivîse","Ramanên hûr bi hev ve girê dide"),
    ],
    "C2":[
        u("C2",1,"Pragmatîk",["pragmatics","information_structure"],"discourse_c2","Wateya vekirî û veşartî cuda dike","Rêza civakî birêve dibe"),
        u("C2",2,"Retorîk û edebiyat",["rhetoric","discourse_analysis"],"culture_c2","Teknîkên retorîk bikar tîne","Wêneyên edebî şîrove dike"),
        u("C2",3,"Werger û hûrgulî",["translation","pragmatics"],"discourse_c2","Wate û ton diparêze","Termînolojiyê bi kontekstê hilbijêre"),
        u("C2",4,"Analîza dîskursê",["discourse_analysis","information_structure"],"discourse_c2","Cure û şêwazê analîz dike","Girêdana dîskursê rave dike"),
        u("C2",5,"Şêwaza edebî",["rhetoric","translation"],"culture_c2","Zimanê edebî nas dike","Hilbijartina wêneyan rave dike"),
        u("C2",6,"Zimanê pîşeyî",["formal_register","pragmatics"],"institutional_c1","Ramanên pîşeyî bi hûrgulî vedibêje","Rêzdariya bi kontekstê diguhezîne"),
        u("C2",7,"Kombûna çavkaniyan",["argumentation","discourse_analysis"],"media_c1","Çavkaniyên piralî yek dike","Delîlên cuda berawird dike"),
        u("C2",8,"Nirxandina yekgirtî ya C2",["translation","rhetoric"],"academic_c1","Nivîsa akademîk a hûr dinivîse","Şêwazê li gorî armancê diguhezîne"),
    ],
}

ASSESSMENT_BANK = [
    AssessmentQuestion(id=f"ku-{i:03}", skill=skill, difficulty=level, question=q, options=opts, correct=correct)
    for i,(level,skill,q,opts,correct) in enumerate([
        ("A1","vocabulary","What does silav mean?",["hello","goodbye","water","school"],"hello"),
        ("A1","grammar","Which sentence means 'I am a student'?",["Ez xwendekar im.","Ez mamoste me.","Tu xwendekar î.","Ew li mal e."],"Ez xwendekar im."),
        ("A1","vocabulary","What does dayik mean?",["mother","father","friend","teacher"],"mother"),
        ("A2","grammar","Which sentence describes a completed past event?",["Min duh pirtûk xwend.","Ez niha dixwînim.","Ez ê biçim.","Ez nizanim."],"Min duh pirtûk xwend."),
        ("A2","vocabulary","What does bilêt mean?",["ticket","medicine","meeting","source"],"ticket"),
        ("B1","grammar","Which expression introduces a condition?",["Heke...","Ji ber ku...","Her çend...","Piştî ku..."],"Heke..."),
        ("B1","grammar","Which connector expresses purpose?",["Da ku...","Ji ber ku...","Lê...","Paşê..."],"Da ku..."),
        ("B2","grammar","Which structure introduces reported speech?",["Wî got ku...","Ev çend e?","Silav!","Li ku ye?"],"Wî got ku..."),
        ("B2","vocabulary","What does delîl mean?",["evidence","holiday","neighbor","ticket"],"evidence"),
        ("C1","academic","Which expression is a hedge?",["Dibe ku...","Silav!","Ev çend e?","Bibore."],"Dibe ku..."),
        ("C1","formal","Which is formal institutional language?",["Li gorî rêzikê dê biryar were dayîn.","Silav!","Ev çend e?","Ez av dixwazim."],"Li gorî rêzikê dê biryar were dayîn."),
        ("C2","discourse","What should a translator preserve?",["meaning, register and discourse function","word count only","literal word order only","punctuation only"],"meaning, register and discourse function"),
    ],1)
]

"""Swahili (Kiswahili) foundation data for JUBA LISAN.

Structured A1-C2 curriculum with native Swahili examples, vocabulary,
phrasebook entries, and assessments.
"""
from app.data._types import (
    CurriculumUnit, GrammarExample, GrammarTopic,
    VocabularyEntry, VocabularySet, PhrasebookCategory,
    PhrasebookEntry, AssessmentQuestion,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

_GRAMMAR = [
("pronouns","Viwakilishi vya nafsi","A1","syntax","Tumia mimi, wewe, yeye, sisi, ninyi na wao katika sentensi rahisi.","Mimi ni mwanafunzi."),
("copula","Sentensi za utambulisho","A1","grammar","Tumia ni na si kuonyesha utambulisho na kukanusha.","Yeye ni mwalimu."),
("demonstratives","Viashiria","A1","grammar","Tumia huyu, hiki, hii, huyo, hicho na hiyo kuonyesha watu na vitu.","Kitabu hiki ni changu."),
("questions","Maswali ya msingi","A1","communication","Tumia nini, nani, wapi, lini, kwa nini na vipi kuuliza habari.","Unaishi wapi?"),
("present","Wakati wa sasa","A1","verbs","Tumia viambishi vya nafsi na -na- kueleza vitendo vinavyoendelea au mazoea.","Ninasoma Kiswahili."),
("negation","Kukanusha","A1","syntax","Tumia viambishi vya kukanusha katika sentensi rahisi.","Sielewi swali."),
("noun-classes","Ngeli za nomino","A1","nouns","Tambua upatanisho wa msingi wa ngeli za M-WA na KI-VI.","Mtoto anasoma; watoto wanasoma."),
("prepositions","Mahali na viambishi vya mahali","A1","grammar","Tumia katika, kwenye, kwa na kutoka kueleza mahali na mwendo.","Niko shuleni."),
("past","Wakati uliopita","A2","verbs","Tumia -li- kueleza kitendo kilichotokea.","Jana nilisoma kitabu."),
("future","Wakati ujao","A2","verbs","Tumia -ta- kueleza mipango na matukio yajayo.","Kesho nitasafiri."),
("object-markers","Viambishi vya yambwa","A2","verbs","Ongeza kiambishi cha yambwa kinacholingana na nomino.","Ninakiona kitabu."),
("adjectives","Vivumishi na upatanisho","A2","grammar","Patanisha kivumishi na ngeli ya nomino.","Watoto wazuri wanacheza."),
("possessives","Umilikaji","A2","grammar","Tumia wa, ya, cha, vya na miundo ya -angu, -ako na -ake.","Hiki ni kitabu changu."),
("comparatives","Ulinganishi","A2","adjectives","Linganisha vitu kwa kutumia kuliko na zaidi ya.","Juma ni mrefu kuliko Ali."),
("imperatives","Amri na maombi","A2","communication","Tumia amri na maombi kwa heshima katika hali za kila siku.","Tafadhali fungua mlango."),
("relative-clauses","Virai vya uhusiano","B1","syntax","Unganisha nomino na maelezo kwa kutumia viambishi vya uhusiano.","Mtu anayesoma hapa ni rafiki yangu."),
("subordinate-clauses","Sentensi tegemezi","B1","syntax","Tumia kwa sababu, ingawa, ikiwa, wakati na kwamba kuunganisha mawazo.","Nitakuja ikiwa nitapata muda."),
("conditional","Masharti","B1","verbs","Eleza hali za masharti na matokeo yake.","Kama ungekuja, tungezungumza."),
("perfect","Kitendo kilichokamilika","B1","verbs","Tumia -me- kuonyesha hali au kitendo kilichokamilika.","Nimefika nyumbani."),
("habitual","Mazoea kwa hu-","B1","verbs","Tumia hu- kueleza matendo ya kawaida.","Kila asubuhi huenda kazini."),
("passive","Kauli ya kutendwa","B1","syntax","Badilisha mtazamo wa sentensi ili kitendo kisisitizwe kuliko mtendaji.","Barua imeandikwa na Asha."),
("reported-speech","Usemi wa taarifa","B1","discourse","Ripoti kauli za watu kwa kutumia kwamba au kuwa.","Alisema kwamba atakuja."),
("connectors","Viunganishi vya hoja","B1","discourse","Unganisha sentensi kwa lakini, kwa hiyo, hata hivyo, kwa sababu na hivyo.","Alikuwa mgonjwa, kwa hiyo hakwenda."),
("causative","Kauli ya kusababisha","B2","verbs","Tumia miundo ya kusababisha kueleza kwamba mtu husababisha kitendo.","Mwalimu alimfundisha mwanafunzi."),
("applicative","Kauli ya kutendea","B2","verbs","Tumia -i- kueleza mnufaika au mahali pa kitendo.","Nilimnunulia mtoto kitabu."),
("reciprocal","Kauli ya kutendana","B2","verbs","Tumia -ana kueleza kitendo cha pande mbili.","Marafiki wanasaidiana."),
("relative-complex","Uhusiano changamano","B2","syntax","Tumia miundo ya uhusiano katika sentensi ndefu.","Kitabu nilichokisoma jana ni kizuri."),
("indirect-questions","Maswali yaliyomo","B2","syntax","Jumuisha swali ndani ya sentensi nyingine kwa mpangilio unaofaa.","Sijui anaishi wapi."),
("discourse-markers","Alama za mazungumzo","B2","discourse","Tumia kwa kweli, kwanza, aidha, hata hivyo na kwa ujumla kupanga maelezo.","Kwanza, tutajadili tatizo."),
("subjunctive","Hali ya -e","C1","verbs","Tumia -e katika mapendekezo, matakwa na miundo tegemezi.","Ni muhimu usome kwa bidii."),
("nominalization","Uundaji wa nomino","C1","word-formation","Badilisha vitendo au sifa kuwa nomino kwa matumizi rasmi.","Utafiti wa lugha unaendelea."),
("information-structure","Mpangilio wa taarifa","C1","discourse","Panga mada, mkazo na taarifa mpya kwa uwazi.","Jambo muhimu zaidi ni usalama."),
("formal-register","Usajili rasmi","C1","register","Chagua msamiati na miundo inayofaa maandishi rasmi.","Tafadhali wasilisha maombi yako kabla ya tarehe hiyo."),
("idioms","Nahau na misemo","C2","lexis","Tambua maana isiyo ya moja kwa moja ya nahau kulingana na muktadha.","Amefunga safari ya mbali."),
("rhetoric","Balagha na hoja","C2","rhetoric","Jenga hoja yenye ushahidi, pingamizi na hitimisho lenye uwiano.","Hoja hii ina nguvu, ingawa ushahidi wake ni mdogo."),
]

GRAMMAR_TOPICS = [
    GrammarTopic(slug=s, title=t, level=l, category=c, summary=sm, explanation=sm,
                 examples=[GrammarExample(text=e)])
    for s,t,l,c,sm,e in _GRAMMAR
]

_VOCAB = {
"A1":[
("Salamu","habari","phrase","hello","Habari, unaendeleaje?"),
("Utambulisho","jina","noun","name","Jina langu ni Asha."),
("Familia","familia","noun","family","Familia yangu ina watu watano."),
("Nyumbani","nyumba","noun","house","Nyumba yetu iko karibu."),
("Ratiba","asubuhi","noun","morning","Asubuhi ninaenda kazini."),
("Chakula","chakula","noun","food","Ninapenda chakula hiki."),
("Maeneo","soko","noun","market","Soko liko katikati ya mji."),
("Mawasiliano","msaada","noun","help","Nahitaji msaada, tafadhali."),
],
"A2":[
("Usafiri","safari","noun","journey","Safari yangu inaanza kesho."),
("Afya","hospitali","noun","hospital","Anaenda hospitalini leo."),
("Ununuzi","bei","noun","price","Bei ya bidhaa hii ni gani?"),
("Hali ya hewa","mvua","noun","rain","Leo kuna mvua nyingi."),
],
"B1":[
("Kazi","uzoefu","noun","experience","Nina uzoefu wa miaka mitatu."),
("Elimu","elimu","noun","education","Elimu ni muhimu kwa jamii."),
("Jamii","mazingira","noun","environment","Tunapaswa kulinda mazingira."),
("Maoni","maoni","noun","opinion","Ningependa kusikia maoni yako."),
],
"B2":[
("Biashara","biashara","noun","business","Biashara yake imekua haraka."),
("Teknolojia","teknolojia","noun","technology","Teknolojia inabadilisha kazi nyingi."),
("Vyombo vya habari","habari","noun","news","Vyombo vya habari vimeripoti tukio hilo."),
("Utawala","sera","noun","policy","Sera hiyo inalenga kuboresha huduma."),
],
"C1":[
("Utafiti","uchambuzi","noun","analysis","Uchambuzi wa data unaonyesha mwelekeo mpya."),
("Sheria","mkataba","noun","contract","Mkataba unasainiwa leo."),
("Taaluma","tasnifu","noun","thesis","Tasnifu hii inachunguza matumizi ya lugha."),
("Uandishi rasmi","taarifa","noun","report","Taarifa rasmi imetumwa kwa idara."),
],
"C2":[
("Balagha","msimamo","noun","stance","Mwandishi anaeleza msimamo wake kwa uangalifu."),
("Isimu","muktadha","noun","context","Maana ya neno hutegemea muktadha."),
("Fasihi","taswira","noun","imagery","Mwandishi anatumia taswira yenye nguvu."),
("Tafsiri","usawa","noun","equivalence","Mtafsiri anatafuta usawa wa maana."),
],
}

VOCABULARY_SETS = []
for level, rows in _VOCAB.items():
    for index, (topic, word, pos, definition, example) in enumerate(rows, 1):
        sid = f"sw-{level.lower()}-{index}"
        VOCABULARY_SETS.append(
            VocabularySet(id=sid, level=level, topic=topic, unit_ref=f"sw-{level.lower()}-unit-{index}",
                          words=[VocabularyEntry(word=word, pos=pos, definition=definition, example=example)])
        )

_PHRASES = [
("greetings","Salamu",[("Habari!","greeting","neutral"),("Hujambo?","greeting","neutral"),("Nafurahi kukutana nawe.","meeting someone","neutral")]),
("introductions","Utambulisho",[("Jina langu ni Asha.","introducing yourself","neutral"),("Unatoka wapi?","asking origin","neutral"),("Ninatoka Algeria.","stating origin","neutral")]),
("daily","Maisha ya kila siku",[("Ninaenda kazini sasa.","daily routine","neutral"),("Nitarudi jioni.","daily routine","neutral"),("Sielewi.","asking for clarification","neutral")]),
("shopping","Manunuzi",[("Bei ya hii ni gani?","asking the price","neutral"),("Nataka hii, tafadhali.","requesting an item","neutral"),("Naweza kulipa kwa kadi?","asking about payment","neutral")]),
("directions","Maelekezo",[("Kituo kiko wapi?","asking for a location","neutral"),("Nenda moja kwa moja.","giving directions","neutral"),("Geuka kulia.","giving a direction","neutral")]),
("food","Chakula",[("Naomba maji, tafadhali.","ordering a drink","neutral"),("Ninataka chakula hiki.","ordering food","neutral"),("Chakula hiki ni kitamu.","commenting on food","neutral")]),
("health","Afya",[("Ninaumwa kichwa.","describing a symptom","neutral"),("Nahitaji kumuona daktari.","seeking care","neutral"),("Ninajisikia vizuri sasa.","describing recovery","neutral")]),
("work","Kazi",[("Nafanya kazi katika kampuni hii.","talking about work","neutral"),("Nina mkutano saa kumi.","talking about a meeting","neutral"),("Tutaonana kesho ofisini.","work arrangement","neutral")]),
("travel","Safari",[("Nina tiketi ya kwenda Dar es Salaam.","travel information","neutral"),("Treni inaondoka saa ngapi?","asking departure time","neutral"),("Nimepoteza pasipoti yangu.","reporting a problem","neutral")]),
("opinions","Maoni",[("Kwa maoni yangu, wazo hili linafaa.","giving an opinion","neutral"),("Nakubaliana nawe.","agreeing","neutral"),("Sikubaliani kabisa.","disagreeing politely","neutral")]),
("formal","Mawasiliano rasmi",[("Tafadhali pokea maombi yangu.","formal request","formal"),("Ningependa kupata maelezo zaidi.","formal inquiry","formal"),("Asante kwa ushirikiano wako.","formal thanks","formal")]),
("academic","Masomo na utafiti",[("Utafiti huu unaonyesha matokeo mapya.","discussing research","formal"),("Tafadhali rejelea chanzo hiki.","academic reference","formal"),("Hitimisho linategemea data.","academic discussion","formal")]),
("idioms","Nahau na mazungumzo ya hali ya juu",[("Pole na kazi.","acknowledging someone's effort","neutral"),("Kila la heri!","wishing success","neutral"),("Hakuna matata.","reassuring someone","informal")]),
]

PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id=f"sw-phrase-{i}", level="A1" if i <= 5 else "B1",
                       situation=situation, icon=icon,
                       phrases=[PhrasebookEntry(text=t, context=c, register=r) for t,c,r in items])
    for i,(situation, name, items) in enumerate(_PHRASES, 1)
    for icon in ["💬"]
]

_LEVEL_THEMES = {
"A1":["Salamu na utambulisho","Familia","Nyumbani","Ratiba ya kila siku","Chakula","Maeneo","Mawasiliano","Marudio"],
"A2":["Usafiri","Afya","Ununuzi","Hali ya hewa","Mipango","Huduma","Kulinganisha","Marudio"],
"B1":["Kazi","Elimu","Jamii","Maoni","Matukio","Mahusiano","Habari","Marudio"],
"B2":["Biashara","Teknolojia","Vyombo vya habari","Utawala","Mazingira","Utamaduni","Hoja","Marudio"],
"C1":["Utafiti","Sheria","Taaluma","Uandishi rasmi","Uchambuzi","Taarifa","Mijadala","Marudio"],
"C2":["Balagha","Isimu","Fasihi","Tafsiri","Muktadha","Mtindo","Hoja changamano","Marudio"],
}
_LEVEL_GRAMMAR = {
"A1":["pronouns","copula","demonstratives","questions","present","negation","noun-classes","prepositions"],
"A2":["past","future","object-markers","adjectives","possessives","comparatives","imperatives","adjectives"],
"B1":["relative-clauses","subordinate-clauses","conditional","perfect","habitual","passive","reported-speech","connectors"],
"B2":["causative","applicative","reciprocal","relative-complex","indirect-questions","discourse-markers","conditional","passive"],
"C1":["subjunctive","nominalization","information-structure","formal-register","reported-speech","connectors","subordinate-clauses","relative-clauses"],
"C2":["idioms","rhetoric","information-structure","formal-register","nominalization","discourse-markers","relative-complex","subordinate-clauses"],
}

CURRICULUM = {}
for level in LEVELS:
    themes = _LEVEL_THEMES[level]
    grammar = _LEVEL_GRAMMAR[level]
    units = []
    for n, title in enumerate(themes, 1):
        vocab_id = f"sw-{level.lower()}-{min(n, 8 if level == 'A1' else 4)}"
        units.append(CurriculumUnit(
            id=f"sw-{level.lower()}-unit-{n}", level=level, unit_number=n, title=title,
            grammar_points=[grammar[n-1]], vocabulary_set_ids=[vocab_id],
            lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],
            competency_checklist=[f"Communicate in Swahili about {title.lower()}", f"Apply {level} grammar in context"],
            default_weeks=2,
        ))
    CURRICULUM[level] = units

ASSESSMENT_BANK = [
    AssessmentQuestion(id="sw-a1-001",skill="vocabulary",difficulty="A1",question="Which word means “hello”?",options=["habari","bei","soko","msaada"],correct="habari"),
    AssessmentQuestion(id="sw-a1-002",skill="grammar",difficulty="A1",question="Choose the correct sentence for “I am a student.”",options=["Mimi ni mwanafunzi.","Mimi mwanafunzi ni.","Mimi ni wanafunzi.","Mwanafunzi mimi."],correct="Mimi ni mwanafunzi."),
    AssessmentQuestion(id="sw-a1-003",skill="grammar",difficulty="A1",question="Which sentence uses the present tense correctly?",options=["Ninasoma Kiswahili.","Nilisoma Kiswahili.","Nitasoma Kiswahili.","Soma Kiswahili."],correct="Ninasoma Kiswahili."),
    AssessmentQuestion(id="sw-a1-004",skill="grammar",difficulty="A1",question="Which sentence is a location question?",options=["Unaishi wapi?","Niko nyumbani.","Ninakunywa maji.","Hii ni nyumba."],correct="Unaishi wapi?"),
    AssessmentQuestion(id="sw-a1-005",skill="vocabulary",difficulty="A1",question="Which word means “family”?",options=["familia","soko","asubuhi","msaada"],correct="familia"),
    AssessmentQuestion(id="sw-a1-006",skill="vocabulary",difficulty="A1",question="Which word means “price”?",options=["bei","maji","duka","mkate"],correct="bei"),
    AssessmentQuestion(id="sw-a1-007",skill="grammar",difficulty="A1",question="Choose the negative sentence.",options=["Sielewi swali.","Ninaelewa swali.","Nitaelewa swali.","Elewa swali."],correct="Sielewi swali."),
    AssessmentQuestion(id="sw-a1-008",skill="communication",difficulty="A1",question="Which phrase asks for help?",options=["Nahitaji msaada, tafadhali.","Kwaheri!","Asante sana.","Jina langu ni Asha."],correct="Nahitaji msaada, tafadhali."),
    AssessmentQuestion(id="sw-a1-009",skill="communication",difficulty="A1",question="Which phrase asks for a location?",options=["Kituo kiko wapi?","Bei ya hii ni gani?","Sielewi.","Nataka hii."],correct="Kituo kiko wapi?"),
    AssessmentQuestion(id="sw-a1-010",skill="vocabulary",difficulty="A1",question="Which word means “friend”?",options=["rafiki","saa","leo","kesho"],correct="rafiki"),
    AssessmentQuestion(id="sw-b1-011",skill="grammar",difficulty="B1",question="Which sentence uses the perfect marker -me-?",options=["Nimefika nyumbani.","Nilifika nyumbani.","Nitafika nyumbani.","Hufika nyumbani."],correct="Nimefika nyumbani."),
    AssessmentQuestion(id="sw-b1-012",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["Nitakuja ikiwa nitapata muda.","Nimefika nyumbani.","Ninasoma kila siku.","Kitabu hiki ni changu."],correct="Nitakuja ikiwa nitapata muda."),
    AssessmentQuestion(id="sw-b2-013",skill="grammar",difficulty="B2",question="Which sentence uses a reciprocal verb?",options=["Marafiki wanasaidiana.","Mwalimu anafundisha.","Ninasoma kitabu.","Asha alifika jana."],correct="Marafiki wanasaidiana."),
    AssessmentQuestion(id="sw-c1-014",skill="register",difficulty="C1",question="Which expression is appropriate in a formal request?",options=["Ningependa kupata maelezo zaidi.","Hebu niambie!","Vipi?","Sema tu."],correct="Ningependa kupata maelezo zaidi."),
]

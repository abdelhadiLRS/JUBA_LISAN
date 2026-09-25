"""Maltese foundation data for JUBA LISAN.

CEFR A1-C2 curriculum with Maltese-specific grammar, vocabulary, phrasebook
and assessment material.  Maltese examples use the standard Latin orthography.
"""
from app.data._types import (
    CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet,
    PhrasebookCategory, PhrasebookEntry, AssessmentQuestion,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

_GRAMMAR = [
("identity-pronouns","Identity, pronouns and copular clauses","A1","syntax","Introduce people and identify things.","Jien student."),
("basic-word-order","Basic Maltese sentence order","A1","syntax","Build simple subject-verb-object clauses.","Il-mara tistudja."),
("present-verbs","Present tense of regular verbs","A1","verbs","Describe current actions and routines.","Naħdem kuljum."),
("definite-article","The Maltese definite article il-/l-","A1","nouns","Use the definite article with common nouns.","il-ktieb"),
("gender-agreement","Gender and agreement","A1","nouns","Recognise masculine and feminine agreement.","tifla tajba"),
("negation","Negation with ma...x","A1","verbs","Negate finite clauses in everyday speech.","Ma nafx."),
("questions","Question words and yes/no questions","A1","communication","Ask basic information questions.","Fejn tgħix?"),
("possessives","Possessive suffixes and possessive phrases","A1","grammar","Express ownership and relationships.","dar tiegħi"),
("plural-nouns","Common Maltese plural patterns","A1","nouns","Recognise sound and broken plurals.","ktieb / kotba"),
("prepositions","Core prepositions and pronominal forms","A1","grammar","Use basic location and relation words.","ġo d-dar"),
("past-tense","Perfect/past forms in everyday narration","A2","verbs","Talk about completed events.","Mort il-belt."),
("future","Future particle se and future meaning","A2","verbs","Express plans and predictions.","Se mmur għada."),
("imperative","Imperatives and polite requests","A2","communication","Give instructions and requests.","Ejja hawn."),
("object-pronouns","Object pronouns and clitic forms","A2","pronouns","Refer to direct and indirect objects.","Rajtu lbieraħ."),
("comparatives","Comparative and superlative patterns","A2","adjectives","Compare people and things.","akbar minn"),
("modal-verbs","Ability, obligation and desire","A2","modality","Express need, ability and intention.","Għandi mmur."),
("progressive","Progressive constructions","B1","aspect","Distinguish ongoing actions from completed events.","Qed naqra."),
("relative-clauses","Relative clauses with li","B1","syntax","Combine clauses to identify people and things.","Il-ktieb li qrajt..."),
("conditional","Conditional clauses","B1","syntax","Discuss hypothetical and conditional situations.","Kieku kelli ħin..."),
("reported-speech","Reported statements and questions","B1","discourse","Report what another person said.","Qal li kien mar."),
("causative","Causative constructions with għamel","B1","verbs","Describe causing an action or state.","Għamlu jaħdem."),
("connectors","Causal, temporal and concessive connectors","B1","discourse","Link ideas clearly in connected speech.","għax, għalhekk, għalkemm"),
("passive","Passive and impersonal formulations","B2","syntax","Use passive and impersonal styles where natural.","Il-bieb infetaħ."),
("subordination","Complex subordinate clauses","B2","syntax","Build multi-clause arguments and explanations.","Għalkemm kien għajjien..."),
("nominalization","Nominalization and formal noun phrases","B2","academic","Turn processes into formal noun phrases.","it-tkabbir tal-belt"),
("discourse-markers","Discourse markers and information flow","B2","discourse","Organise explanations, contrast and conclusions.","madankollu, barra minn hekk"),
("formal-register","Formal and professional Maltese","C1","register","Shift vocabulary and syntax for professional contexts.","Nitolbok tieħu nota..."),
("academic-hedging","Academic hedging and cautious claims","C1","academic","Qualify claims without overstating evidence.","jidher li..."),
("embedded-questions","Embedded questions and complements","C1","syntax","Integrate questions into longer sentences.","Ma nafx jekk hux..."),
("information-structure","Topic, focus and emphasis","C1","discourse","Control emphasis and old/new information.","Dan il-punt huwa importanti."),
("idiomatic-language","Idiomatic and figurative Maltese","C2","pragmatics","Interpret and use idiomatic language appropriately.","għandu qalbu tajba"),
("register-shifting","Register, politeness and pragmatic nuance","C2","pragmatics","Adapt language to social and institutional context.","B'rispett, nitlobkom..."),
("rhetorical-style","Rhetorical and persuasive structures","C2","rhetoric","Build nuanced arguments and persuasive prose.","Minn naħa waħda... min-naħa l-oħra..."),
("literary-style","Literary and elevated Maltese style","C2","style","Recognise marked literary vocabulary and syntax.","Fil-qalba tal-belt..."),
("translation-precision","Translation, paraphrase and lexical precision","C2","translation","Choose precise Maltese wording across registers.","dan ifisser, mhux sempliċement..."),
]
GRAMMAR_TOPICS = [
    GrammarTopic(slug=s,title=t,level=l,category=c,summary=su,explanation=ex,
                 examples=[GrammarExample(text=e)]) 
    for (s,t,l,c,su,e), ex in [
        ((s,t,l,c,su,ex), ex) for s,t,l,c,su,ex in _GRAMMAR
    ]
]

_VOCAB = [
("A1","mt-a1-1","Greetings and identity",[("bongu","phrase","good morning","Bongu, kif int?"),("grazzi","phrase","thank you","Grazzi ħafna."),("isem","noun","name","X'inhu ismek?"),("ħabib","noun","friend","Dan huwa ħabib tiegħi.")]),
("A1","mt-a1-2","Family and people",[("familja","noun","family","Il-familja tiegħi kbira."),("omm","noun","mother","Omm qiegħda d-dar."),("missier","noun","father","Missieri jaħdem."),("tifel","noun","boy/child","It-tifel qiegħed jilgħab.")]),
("A1","mt-a1-3","Home",[("dar","noun","house/home","Din hija d-dar tiegħi."),("kamra","noun","room","Il-kamra żgħira."),("bieb","noun","door","Agħlaq il-bieb."),("mejda","noun","table","Il-ktieb fuq il-mejda.")]),
("A1","mt-a1-4","Routine",[("xogħol","noun","work","Immur għax-xogħol."),("naqra","verb","I read","Naqra kuljum."),("niekol","verb","I eat","Niekol filgħodu."),("norqod","verb","I sleep","Norqod kmieni.")]),
("A1","mt-a1-5","Time",[("illum","adverb","today","Illum għandi lezzjoni."),("għada","adverb","tomorrow","Għada mmur l-iskola."),("bieraħ","adverb","yesterday","Bieraħ kont id-dar."),("siegħa","noun","hour","Għandna siegħa.")]),
("A1","mt-a1-6","Food",[("ħobż","noun","bread","Irrid il-ħobż."),("ilma","noun","water","Nixtieq l-ilma."),("tè","noun","tea","Nieħu t-tè."),("suq","noun","market","Immur is-suq.")]),
("A1","mt-a1-7","Places",[("skola","noun","school","It-tfal qegħdin l-iskola."),("belt","noun","city","Ngħix fil-belt."),("triq","noun","street","Din it-triq twila."),("ħanut","noun","shop","Il-ħanut miftuħ.")]),
("A1","mt-a1-8","Everyday communication",[("fejn","adverb","where","Fejn tgħix?"),("meta","adverb","when","Meta tasal?"),("għaliex","adverb","why","Għaliex ġejt?"),("jekk jogħġbok","phrase","please","Għinni, jekk jogħġbok.")]),
("A2","mt-a2-1","Travel and transport",[("vjaġġ","noun","trip","Il-vjaġġ kien twil."),("ajruport","noun","airport","Wasalt fl-ajruport."),("biljett","noun","ticket","Għandi biljett."),("ferrovija","noun","train","Il-ferrovija waslet.")]),
("A2","mt-a2-2","Health and body",[("saħħa","noun","health","Is-saħħa importanti."),("tabib","noun","doctor","Għandi appuntament mat-tabib."),("uġigħ","noun","pain","Għandi uġigħ f'rasi."),("mediċina","noun","medicine","Għandi bżonn il-mediċina.")]),
("A2","mt-a2-3","Plans and obligations",[("pjan","noun","plan","Għandi pjan."),("bżonn","noun","need","Għandi bżonn l-għajnuna."),("nista'","verb","I can","Nista' ngħinek."),("għandi","verb","I have/must","Għandi mmur.")]),
("A2","mt-a2-4","Shopping and services",[("prezz","noun","price","Kemm hu l-prezz?"),("ħlas","noun","payment","Il-ħlas bil-karta."),("riċevuta","noun","receipt","Għandi r-riċevuta."),("servizz","noun","service","Is-servizz tajjeb.")]),
("B1","mt-b1-1","Education",[("studju","noun","study","L-istudju jeħtieġ ħin."),("eżami","noun","exam","Għandi eżami."),("riċerka","noun","research","Qed nagħmel riċerka."),("għarfien","noun","knowledge","L-għarfien jikber.")]),
("B1","mt-b1-2","Work",[("laqgħa","noun","meeting","Għandna laqgħa."),("kollega","noun","colleague","Il-kollega tiegħi wasal."),("proġett","noun","project","Il-proġett beda."),("esperjenza","noun","experience","Għandi esperjenza.")]),
("B1","mt-b1-3","Society",[("komunità","noun","community","Il-komunità qiegħda tikber."),("ambjent","noun","environment","Irridu nħarsu l-ambjent."),("liġi","noun","law","Il-liġi tapplika għal kulħadd."),("dritt","noun","right","Kull persuna għandha dritt.")]),
("B1","mt-b1-4","Opinions and reasons",[("opinjoni","noun","opinion","Din hija l-opinjoni tiegħi."),("raġuni","noun","reason","Hemm raġuni ċara."),("evidenza","noun","evidence","Għandna evidenza."),("argument","noun","argument","L-argument huwa b'saħħtu.")]),
("B2","mt-b2-1","Media and technology",[("aħbar","noun","news","Qrajt l-aħbar."),("sors","noun","source","Is-sors affidabbli."),("dejta","noun","data","Id-dejta ġiet analizzata."),("teknoloġija","noun","technology","It-teknoloġija qed tinbidel.")]),
("B2","mt-b2-2","Economy",[("ekonomija","noun","economy","L-ekonomija qed tikber."),("investiment","noun","investment","L-investiment żdied."),("negozju","noun","business","Għandu negozju żgħir."),("suq","noun","market","Is-suq internazzjonali.")]),
("B2","mt-b2-3","Culture",[("kultura","noun","culture","Il-kultura Maltija rikka."),("wirt","noun","heritage","Il-wirt għandu jiġi protett."),("tradizzjoni","noun","tradition","Din it-tradizzjoni antika."),("letteratura","noun","literature","Naqra l-letteratura Maltija.")]),
("B2","mt-b2-4","Environment",[("tniġġis","noun","pollution","It-tniġġis huwa problema."),("riżorsa","noun","resource","L-ilma riżorsa prezzjuża."),("enerġija","noun","energy","Għandna bżonn enerġija nadifa."),("sostenibbiltà","noun","sustainability","Is-sostenibbiltà importanti.")]),
("C1","mt-c1-1","Academic argumentation",[("ipoteżi","noun","hypothesis","L-ipoteżi trid tiġi ttestjata."),("metodoloġija","noun","methodology","Il-metodoloġija hija ċara."),("konklużjoni","noun","conclusion","Il-konklużjoni tibni fuq l-evidenza."),("interpretazzjoni","noun","interpretation","Din hija interpretazzjoni possibbli.")]),
("C1","mt-c1-2","Public administration",[("politika","noun","policy","Il-politika ġiet aġġornata."),("regolament","noun","regulation","Ir-regolament japplika."),("proċedura","noun","procedure","Segwi l-proċedura."),("applikazzjoni","noun","application","Ibgħat l-applikazzjoni.")]),
("C1","mt-c1-3","Professional communication",[("rapport","noun","report","Ir-rapport lest."),("proposta","noun","proposal","Il-proposta ġiet diskussa."),("negozjar","noun","negotiation","In-negozjar kompla."),("ftehim","noun","agreement","Wasalna għal ftehim.")]),
("C1","mt-c1-4","Critical analysis",[("kritika","noun","critique","Il-kritika hija kostruttiva."),("preġudizzju","noun","bias","Irridu nevitaw il-preġudizzju."),("perspettiva","noun","perspective","Il-perspettiva tinbidel."),("kuntrast","noun","contrast","Hemm kuntrast ċar.")]),
("C2","mt-c2-1","Rhetoric",[("retorika","noun","rhetoric","Ir-retorika għandha rwol importanti."),("persważjoni","noun","persuasion","Il-persważjoni teħtieġ evidenza."),("enfasi","noun","emphasis","L-enfasi tinsab hawn."),("konċessjoni","noun","concession","Il-konċessjoni ssaħħaħ l-argument.")]),
("C2","mt-c2-2","Nuance and idiom",[("sfumatura","noun","nuance","Hemm sfumatura fit-tifsira."),("metafora","noun","metaphor","Il-metafora tagħti qawwa lit-test."),("ironija","noun","irony","L-ironija tiddependi mill-kuntest."),("idjoma","noun","idiom","Din hija idjoma komuni.")]),
("C2","mt-c2-3","Literary language",[("narrattiva","noun","narrative","In-narrattiva kumplessa."),("simbolu","noun","symbol","Is-simbolu jirrepeti ruħu."),("stil","noun","style","L-istil huwa distintiv."),("ton","noun","tone","It-ton jinbidel.")]),
("C2","mt-c2-4","Translation and precision",[("tifsira","noun","meaning","It-tifsira tiddependi mill-kuntest."),("ekwivalenza","noun","equivalence","L-ekwivalenza mhix dejjem diretta."),("parafrażi","noun","paraphrase","Agħmel parafrażi preċiża."),("preċiżjoni","noun","precision","Il-preċiżjoni lingwistika importanti.")]),
]
VOCABULARY_SETS = [
    VocabularySet(id=i,level=l,topic=t,unit_ref=f"mt-{l.lower()}-unit-{n}",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])
    for (l,i,t,words), n in zip(_VOCAB, [((idx % 8)+1) for idx in range(len(_VOCAB))])
]

_TOPICS = [
("A1",["Introductions and identity","Family and home","Daily routine","Time and appointments","Food and shopping","Places and directions","Questions and negation","A1 consolidation"]),
("A2",["Travel and transport","Health and wellbeing","Plans and obligations","Shopping and services","Past events","Future plans","Comparisons and preferences","A2 consolidation"]),
("B1",["Education and learning","Workplace communication","Society and community","Opinions and reasons","Reported information","Conditions and consequences","Connected speech","B1 consolidation"]),
("B2",["Media and technology","Economy and business","Culture and heritage","Environment","Formal explanations","Complex subordination","Argument structure","B2 consolidation"]),
("C1",["Academic argumentation","Public administration","Professional communication","Critical analysis","Evidence and methodology","Formal writing","Hedging and nuance","C1 consolidation"]),
("C2",["Rhetoric and persuasion","Idioms and pragmatics","Literary language","Translation precision","Discourse analysis","Register shifting","Advanced style","C2 consolidation"]),
]
CURRICULUM = {}
for level,titles in _TOPICS:
    units=[]
    for n,title in enumerate(titles,1):
        vid=f"mt-{level.lower()}-{n}"
        units.append(CurriculumUnit(
            id=f"mt-{level.lower()}-unit-{n}",level=level,unit_number=n,
            title=f"Maltese {level} · {title}",
            grammar_points=[g[1] for g in _GRAMMAR if g[2]==level][:2] or ["Maltese language consolidation"],
            vocabulary_set_ids=[vid] if any(v[1]==vid for v in _VOCAB) else ["mt-a1-1"],
            lesson_types=["grammar","vocabulary","reading","writing","listening","review"],
            competency_checklist=[f"Handle {level} communication on {title.lower()}","Use Maltese forms accurately in context"],
            default_weeks=2))
    CURRICULUM[level]=units

PHRASE_DATA = [
("A1","Greetings",["Bongu.","Kif int?","Għandi pjaċir niltaqa' miegħek."]),
("A1","Polite requests",["Jekk jogħġbok.","Tista' tgħinni?","Grazzi ħafna."]),
("A2","Travel",["Fejn hi l-istazzjon?","Fejn nista' nixtri biljett?","Meta jitlaq il-karozz?"]),
("A2","Health",["Għandi bżonn tabib.","Ma nħossnix tajjeb.","Fejn hi l-ispiżerija?"]),
("B1","Work",["Nistgħu nibdew il-laqgħa?","X'inhi l-opinjoni tiegħek?","Naqbel ma' dan il-punt."]),
("B1","Clarification",["Tista' tispjegaha?","X'tixtieq tfisser?","Ħalli niċċara dan il-punt."]),
("B2","Formal discussion",["Skont is-sorsi disponibbli...","Min-naħa l-oħra...","Madankollu, hemm problema."]),
("B2","Professional email",["Nitolbok tieħu nota.","Qed nibgħat id-dokument mehmuż.","Nistenna t-tweġiba tiegħek."]),
("C1","Academic",["L-evidenza tissuġġerixxi li...","Jista' jiġi argumentat li...","Din il-konklużjoni teħtieġ aktar evidenza."]),
("C1","Administration",["Skont ir-regolament...","L-applikazzjoni ġiet riċevuta.","Jekk jogħġbok segwi l-proċedura."]),
("C2","Debate",["F'dan ir-rigward...","Dan l-argument jinjora l-fatt li...","Ta' min jinnota li..."]),
("C2","Nuance",["It-tifsira tiddependi mill-kuntest.","Hemm differenza sottili bejn dawn iż-żewġ termini.","B'mod ġenerali, iżda mhux mingħajr eċċezzjonijiet."]),
]
PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id=f"mt-{l.lower()}-phrase-{n}",level=l,situation=s,icon="💬",
        phrases=[PhrasebookEntry(text=p,context=s.lower(),register="formal" if l in ["C1","C2"] else "neutral") for p in phrases])
    for n,(l,s,phrases) in enumerate(PHRASE_DATA,1)
]

ASSESSMENT_BANK = [
    AssessmentQuestion(id=f"mt-{l.lower()}-{n:03}",skill=skill,difficulty=l,question=q,options=[correct,"Għażla A","Għażla B","Għażla C"],correct=correct,grammar_slug=slug)
    for n,(l,skill,q,correct,slug) in enumerate([
        ("A1","grammar","Choose the correct negative form: ___ nafx.","Ma nafx.","negation"),
        ("A1","vocabulary","Which word means family?","familja","identity-pronouns"),
        ("A2","grammar","Choose the future marker: ___ mmur għada.","Se","future"),
        ("A2","vocabulary","Which word means ticket?","biljett","travel"),
        ("B1","grammar","Which connector introduces a reason?","għax","connectors"),
        ("B1","vocabulary","Which word means evidence?","evidenza","reported-speech"),
        ("B2","grammar","Which form introduces a concessive clause?","Għalkemm","subordination"),
        ("B2","vocabulary","Which word means sustainability?","sostenibbiltà","discourse-markers"),
        ("C1","grammar","Which expression appropriately hedges an academic claim?","jidher li","academic-hedging"),
        ("C1","vocabulary","Which word means methodology?","metodoloġija","formal-register"),
        ("C2","grammar","Which concept concerns adaptation to social context?","register-shifting","register-shifting"),
        ("C2","vocabulary","Which word means nuance?","sfumatura","idiomatic-language"),
    ],1)
]

"""Cymraeg (Welsh) foundation data for JUBA LISAN — CEFR A1-C2."""
from app.data._types import (
    CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet,
    PhrasebookCategory, PhrasebookEntry, AssessmentQuestion,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

GRAMMAR_TOPICS = [
    GrammarTopic(slug="cy-a1-bod", title="Verb bod and present patterns", level="A1", category="verbs", summary="Use bod to describe identity, location and states.", explanation="Welsh uses forms of bod with noun, adjective and prepositional complements; colloquial present patterns commonly use Dw i'n.", examples=[GrammarExample(text="Dw i'n fyfyriwr."), GrammarExample(text="Mae hi yn y tŷ.")]),
    GrammarTopic(slug="cy-a1-word-order", title="Basic Welsh word order", level="A1", category="syntax", summary="Build short everyday clauses.", explanation="Use common Welsh patterns for statements, questions and identification.", examples=[GrammarExample(text="Dw i'n gweithio."), GrammarExample(text="Mae Tom yn darllen.")]),
    GrammarTopic(slug="cy-a1-negation", title="Present negation", level="A1", category="syntax", summary="Negate simple present statements.", explanation="Use ddim with the appropriate bod construction.", examples=[GrammarExample(text="Dw i ddim yn flinedig."), GrammarExample(text="Dydy e ddim yma.")]),
    GrammarTopic(slug="cy-a1-questions", title="Basic questions", level="A1", category="syntax", summary="Ask who, what, where and how much.", explanation="Use question words such as ble, beth, pwy and faint, with appropriate bod patterns.", examples=[GrammarExample(text="Ble wyt ti?"), GrammarExample(text="Beth yw dy enw?")]),
    GrammarTopic(slug="cy-a1-possessives", title="Possessives", level="A1", category="grammar", summary="Express ownership and relationships.", explanation="Use fy, dy and ei with nouns and learn their common mutation effects.", examples=[GrammarExample(text="Dyma fy enw."), GrammarExample(text="Ble mae dy lyfr?")]),
    GrammarTopic(slug="cy-a1-mutation", title="Soft mutation", level="A1", category="phonology", summary="Recognise common initial consonant changes.", explanation="Soft mutation changes initial consonants in specific grammatical environments and is fundamental to Welsh reading.", examples=[GrammarExample(text="fy nghar"), GrammarExample(text="ei char hi")]),
    GrammarTopic(slug="cy-a2-past", title="Past tense patterns", level="A2", category="verbs", summary="Talk about completed events.", explanation="Use common past-tense constructions, including the preterite of frequent verbs and colloquial patterns.", examples=[GrammarExample(text="Es i i'r siop ddoe."), GrammarExample(text="Roedd hi'n hapus.")]),
    GrammarTopic(slug="cy-a2-future", title="Future and intention", level="A2", category="verbs", summary="Discuss plans and future events.", explanation="Use future forms and bod constructions to express plans, predictions and intentions.", examples=[GrammarExample(text="Bydda i yno yfory."), GrammarExample(text="Dw i'n mynd i brynu car.")]),
    GrammarTopic(slug="cy-a2-adjectives", title="Adjectives and comparison", level="A2", category="adjectives", summary="Describe and compare people and things.", explanation="Welsh adjectives often follow nouns and show mutation or special comparative forms in common constructions.", examples=[GrammarExample(text="tŷ mawr"), GrammarExample(text="Mae'r car hwn yn well.")]),
    GrammarTopic(slug="cy-a2-prepositions", title="Prepositions and pronouns", level="A2", category="grammar", summary="Handle common prepositional forms.", explanation="Learn inflected prepositions such as gyda fi, gyda ti and ataf/ato in more formal patterns.", examples=[GrammarExample(text="Dewch gyda fi."), GrammarExample(text="Mae hi'n siarad â fi.")]),
    GrammarTopic(slug="cy-a2-relative", title="Relative clauses", level="A2", category="syntax", summary="Add information about people and things.", explanation="Use common relative constructions with a, sydd and other relative patterns.", examples=[GrammarExample(text="Y dyn sy'n byw yma."), GrammarExample(text="Y llyfr a ddarllenais.")]),
    GrammarTopic(slug="cy-b1-verb-nouns", title="Verbal nouns", level="B1", category="verbs", summary="Describe ongoing actions and activities.", explanation="Use bod + yn + verbal noun and related patterns to discuss activities, habits and processes.", examples=[GrammarExample(text="Dw i'n dysgu Cymraeg."), GrammarExample(text="Roedden nhw'n gweithio.")]),
    GrammarTopic(slug="cy-b1-conditionals", title="Conditional and hypothetical forms", level="B1", category="syntax", summary="Discuss possibilities and hypothetical situations.", explanation="Use conditional patterns with byddwn, pe and related clause structures.", examples=[GrammarExample(text="Pe bai gen i amser, byddwn i'n mynd."), GrammarExample(text="Byddwn i'n helpu pe gallwn.")]),
    GrammarTopic(slug="cy-b1-mutational-system", title="Mutation in connected Welsh", level="B1", category="morphology", summary="Apply soft, nasal and aspirate mutation in context.", explanation="Different grammatical environments trigger different mutation systems; learn them as productive patterns rather than isolated spellings.", examples=[GrammarExample(text="fy nghartref"), GrammarExample(text="tri chi"), GrammarExample(text="ei thŷ hi")]),
    GrammarTopic(slug="cy-b1-opinion", title="Opinion and discourse markers", level="B1", category="pragmatics", summary="Give reasons, opinions and contrasts.", explanation="Use connectors such as oherwydd, er bod, ond and felly to make speech coherent.", examples=[GrammarExample(text="Dw i'n meddwl bod hyn yn bwysig."), GrammarExample(text="Er bod hi'n hwyr, aethon ni.")]),
    GrammarTopic(slug="cy-b2-reported", title="Reported speech", level="B2", category="syntax", summary="Report statements and questions.", explanation="Use bod and other clause patterns to report what people said, believed or asked.", examples=[GrammarExample(text="Dywedodd hi ei bod hi'n brysur."), GrammarExample(text="Gofynnodd e ble roeddwn i.")]),
    GrammarTopic(slug="cy-b2-passive", title="Passive and impersonal constructions", level="B2", category="syntax", summary="Focus on actions and processes.", explanation="Use passive and impersonal patterns to foreground events, especially in formal information.", examples=[GrammarExample(text="Cafodd y llyfr ei gyhoeddi."), GrammarExample(text="Mae'r penderfyniad wedi'i wneud.")]),
    GrammarTopic(slug="cy-b2-subordination", title="Complex subordination", level="B2", category="syntax", summary="Connect causes, concessions and conditions.", explanation="Build multi-clause arguments with oherwydd, er bod, os, pan and related subordinators.", examples=[GrammarExample(text="Er bod y dasg yn anodd, fe wnaethon ni ei chwblhau."), GrammarExample(text="Os bydd amser gennym, byddwn yn parhau.")]),
    GrammarTopic(slug="cy-b2-register", title="Formal and professional Welsh", level="B2", category="style", summary="Adapt language to workplace and official contexts.", explanation="Choose formal vocabulary, precise clause structures and appropriate politeness for professional communication.", examples=[GrammarExample(text="Yn ôl yr adroddiad, mae angen rhagor o ymchwil."), GrammarExample(text="Dylid ystyried y mater yn ofalus.")]),
    GrammarTopic(slug="cy-c1-nominalisation", title="Formal nominal style", level="C1", category="style", summary="Package complex information in formal prose.", explanation="Use abstract nouns and compact clause structures in reports, essays and institutional writing.", examples=[GrammarExample(text="Mae cynnydd sylweddol wedi digwydd."), GrammarExample(text="Mae angen adolygiad cynhwysfawr o'r polisi.")]),
    GrammarTopic(slug="cy-c1-hedging", title="Hedging and academic discourse", level="C1", category="pragmatics", summary="Qualify claims and distinguish certainty from interpretation.", explanation="Use cautious formulations such as mae'n ymddangos, gellid dadlau and efallai to calibrate claims.", examples=[GrammarExample(text="Mae'n ymddangos bod y canlyniadau'n awgrymu newid."), GrammarExample(text="Gellid dadlau bod angen dull arall.")]),
    GrammarTopic(slug="cy-c1-idiom", title="Idiomatic and pragmatic nuance", level="C1", category="pragmatics", summary="Interpret implied meaning and register.", explanation="Develop sensitivity to fixed expressions, politeness, understatement and context-dependent choices.", examples=[GrammarExample(text="Mae'n hen bryd inni weithredu."), GrammarExample(text="Nid yw hynny o reidrwydd yn golygu hynny.")]),
    GrammarTopic(slug="cy-c2-advanced-syntax", title="Advanced syntax and information structure", level="C2", category="syntax", summary="Control embedded and emphatic structures.", explanation="Combine relative clauses, subordinate clauses and emphasis with precise information packaging.", examples=[GrammarExample(text="Yr hyn sy'n bwysig yw ein bod yn deall y rhesymau dros y newid."), GrammarExample(text="Er na ellir rhagweld y canlyniad yn union, gellir asesu'r risgiau.")]),
    GrammarTopic(slug="cy-c2-rhetoric", title="Rhetorical and literary register", level="C2", category="style", summary="Produce sophisticated formal and cultural Welsh.", explanation="Use rhetorical contrast, lexical precision and controlled register shifts in essays, commentary and public communication.", examples=[GrammarExample(text="Nid yn unig y newidiodd y prosiect y system, ond newidiodd y ffordd yr oedd pobl yn ei gweld hefyd."), GrammarExample(text="O'r herwydd, mae'n werth edrych y tu hwnt i'r ffigurau eu hunain.")]),
]

def _unit(level, n, title, grammar, vocab):
    return CurriculumUnit(
        id=f"cy-{level.lower()}-unit-{n}", level=level, unit_number=n, title=title,
        grammar_points=grammar, vocabulary_set_ids=[vocab],
        lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],
        competency_checklist=[f"Use {title.lower()} vocabulary", f"Apply {grammar[0]} in connected Welsh"],
        default_weeks=2,
    )

CURRICULUM = {
    "A1": [
        _unit("A1",1,"Cyfarchion a chyflwyno eich hun",["cy-a1-bod"],"cy_a1_social"),
        _unit("A1",2,"Teulu a pherthnasoedd",["cy-a1-possessives"],"cy_a1_family"),
        _unit("A1",3,"Cartref a threfn ddyddiol",["cy-a1-word-order"],"cy_a1_home"),
        _unit("A1",4,"Cwestiynau a negyddu",["cy-a1-questions","cy-a1-negation"],"cy_a1_questions"),
        _unit("A1",5,"Bwyd a siopa",["cy-a1-mutation"],"cy_a1_food"),
        _unit("A1",6,"Amser a lleoedd",["cy-a1-mutation"],"cy_a1_time"),
    ],
    "A2": [
        _unit("A2",1,"Ddoe a phrofiadau",["cy-a2-past"],"cy_a2_past"),
        _unit("A2",2,"Cynlluniau a'r dyfodol",["cy-a2-future"],"cy_a2_future"),
        _unit("A2",3,"Disgrifio a chymharu",["cy-a2-adjectives"],"cy_a2_comparison"),
        _unit("A2",4,"Pobl a pherthnasoedd",["cy-a2-prepositions"],"cy_a2_people"),
        _unit("A2",5,"Lleoedd a phrofiadau",["cy-a2-relative"],"cy_a2_experience"),
        _unit("A2",6,"Cyfathrebu bob dydd",["cy-a2-past","cy-a2-future"],"cy_a2_review"),
    ],
    "B1": [
        _unit("B1",1,"Gweithgareddau a nodau",["cy-b1-verb-nouns"],"cy_b1_activities"),
        _unit("B1",2,"Posibiliadau ac amodau",["cy-b1-conditionals"],"cy_b1_conditions"),
        _unit("B1",3,"Treigladau mewn cyd-destun",["cy-b1-mutational-system"],"cy_b1_language"),
        _unit("B1",4,"Barn a rhesymau",["cy-b1-opinion"],"cy_b1_opinion"),
        _unit("B1",5,"Gwaith ac astudio",["cy-b1-verb-nouns"],"cy_b1_work"),
        _unit("B1",6,"Straeon a thrafodaeth",["cy-b1-opinion","cy-b1-conditionals"],"cy_b1_discussion"),
    ],
    "B2": [
        _unit("B2",1,"Adrodd a gwybodaeth",["cy-b2-reported"],"cy_b2_reporting"),
        _unit("B2",2,"Newyddion a phrosesau",["cy-b2-passive"],"cy_b2_media"),
        _unit("B2",3,"Achos, gwrthgyferbyniad a chanfyddiadau",["cy-b2-subordination"],"cy_b2_argument"),
        _unit("B2",4,"Cyfathrebu proffesiynol",["cy-b2-register"],"cy_b2_professional"),
        _unit("B2",5,"Cymdeithas a gwasanaethau",["cy-b2-subordination"],"cy_b2_society"),
        _unit("B2",6,"Adolygiad B2",["cy-b2-reported","cy-b2-passive"],"cy_b2_review"),
    ],
    "C1": [
        _unit("C1",1,"Ysgrifennu ffurfiol",["cy-c1-nominalisation"],"cy_c1_formal"),
        _unit("C1",2,"Dadlau a thystiolaeth",["cy-c1-hedging"],"cy_c1_argument"),
        _unit("C1",3,"Nuance a phragmateg",["cy-c1-idiom"],"cy_c1_pragmatics"),
        _unit("C1",4,"Diwylliant a hunaniaeth",["cy-c1-hedging"],"cy_c1_culture"),
        _unit("C1",5,"Ymchwil a bywyd cyhoeddus",["cy-c1-nominalisation"],"cy_c1_public"),
        _unit("C1",6,"Adolygiad C1",["cy-c1-nominalisation","cy-c1-hedging"],"cy_c1_review"),
    ],
    "C2": [
        _unit("C2",1,"Cystrawen gymhleth",["cy-c2-advanced-syntax"],"cy_c2_syntax"),
        _unit("C2",2,"Rhethreg a steil",["cy-c2-rhetoric"],"cy_c2_rhetoric"),
        _unit("C2",3,"Dadansoddiad beirniadol",["cy-c1-hedging"],"cy_c2_analysis"),
        _unit("C2",4,"Nuance a rhyngweithio",["cy-c1-idiom"],"cy_c2_nuance"),
        _unit("C2",5,"Ysgrifennu academaidd a phroffesiynol",["cy-c2-advanced-syntax"],"cy_c2_academic"),
        _unit("C2",6,"Meistrolaeth yn Gymraeg",["cy-c2-advanced-syntax","cy-c2-rhetoric"],"cy_c2_mastery"),
    ],
}

def _vset(id_, level, topic, unit_ref, words):
    return VocabularySet(id=id_, level=level, topic=topic, unit_ref=unit_ref,
        words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])

VOCABULARY_SETS = [
    _vset("cy_a1_social","A1","Cyfarchion","cy-a1-unit-1",[
        ("helo","interjection","hello","Helo, sut wyt ti?"),("bore da","phrase","good morning","Bore da!"),("hwyl","interjection","bye","Hwyl am y tro."),("diolch","phrase","thank you","Diolch yn fawr."),("os gwelwch yn dda","phrase","please","Coffi, os gwelwch yn dda."),("croeso","phrase","welcome/you're welcome","Croeso i Gymru."),
    ]),
    _vset("cy_a1_family","A1","Teulu","cy-a1-unit-2",[
        ("enw","noun","name","Beth yw dy enw?"),("teulu","noun","family","Mae gen i deulu mawr."),("mam","noun","mother","Mae fy mam yma."),("tad","noun","father","Mae fy nhad yn gweithio."),("brawd","noun","brother","Mae gen i frawd."),("chwaer","noun","sister","Mae gen i chwaer."),
    ]),
    _vset("cy_a1_home","A1","Cartref","cy-a1-unit-3",[
        ("tŷ","noun","house","Dw i yn y tŷ."),("ystafell","noun","room","Mae'r ystafell yn fawr."),("drws","noun","door","Agorwch y drws."),("cegin","noun","kitchen","Mae'r gegin yn lân."),("bwrdd","noun","table","Mae'r llyfr ar y bwrdd."),("gwely","noun","bed","Mae'r gwely yn ystafell wely."),
    ]),
    _vset("cy_a1_questions","A1","Cwestiynau","cy-a1-unit-4",[
        ("ble","adverb","where","Ble wyt ti?"),("beth","pronoun","what","Beth yw hwn?"),("pwy","pronoun","who","Pwy yw e?"),("faint","pronoun","how much/how many","Faint yw e?"),("pam","adverb","why","Pam?"),("sut","adverb","how","Sut wyt ti?"),
    ]),
    _vset("cy_a1_food","A1","Bwyd","cy-a1-unit-5",[
        ("bara","noun","bread","Hoffwn i fara."),("dŵr","noun","water","Dw i eisiau dŵr."),("llaeth","noun","milk","Mae llaeth yn yr oergell."),("coffi","noun","coffee","Hoffwn i goffi."),("afal","noun","apple","Mae gen i afal."),("bwyd","noun","food","Mae'r bwyd yn dda."),
    ]),
    _vset("cy_a1_time","A1","Amser a lleoedd","cy-a1-unit-6",[
        ("heddiw","adverb","today","Dw i'n gweithio heddiw."),("yfory","adverb","tomorrow","Dw i'n teithio yfory."),("ddoe","adverb","yesterday","Roeddwn i yno ddoe."),("nawr","adverb","now","Dw i'n brysur nawr."),("siop","noun","shop","Mae'r siop gerllaw."),("gorsaf","noun","station","Ble mae'r orsaf?"),
    ]),
    _vset("cy_a2_past","A2","Y gorffennol","cy-a2-unit-1",[
        ("es i","verb phrase","I went","Es i i'r siop ddoe."),("gwelais","verb","I saw","Gwelais ffilm neithiwr."),("prynais","verb","I bought","Prynais lyfr newydd."),("cefais","verb","I got/had","Cefais neges."),("neithiwr","adverb","last night","Roeddwn i'n darllen neithiwr."),("profiad","noun","experience","Roedd yn brofiad da."),
    ]),
    _vset("cy_a2_future","A2","Y dyfodol","cy-a2-unit-2",[
        ("yfory","adverb","tomorrow","Bydda i yno yfory."),("cynllun","noun","plan","Mae gen i gynllun."),("mynd i","construction","going to","Dw i'n mynd i astudio."),("bydda i","verb phrase","I will be","Bydda i'n barod."),("nes ymlaen","phrase","later","Gwelwn ni chi nes ymlaen."),("gobaith","noun","hope","Mae gen i obaith."),
    ]),
    _vset("cy_a2_comparison","A2","Disgrifio a chymharu","cy-a2-unit-3",[
        ("mawr","adjective","big","Mae tŷ mawr yno."),("bach","adjective","small","Mae car bach ganddo."),("gwell","adjective","better","Mae hwn yn well."),("gorau","adjective","best","Dyma'r un gorau."),("rhatach","adjective","cheaper","Mae hwn yn rhatach."),("drutach","adjective","more expensive","Mae'r un arall yn ddrutach."),
    ]),
    _vset("cy_a2_people","A2","Pobl a pherthnasoedd","cy-a2-unit-4",[
        ("gyda fi","phrase","with me","Dewch gyda fi."),("gyda ti","phrase","with you","Dw i'n mynd gyda ti."),("ffrind","noun","friend","Mae hi'n ffrind da."),("cymydog","noun","neighbour","Mae fy nghymydog yma."),("perthynas","noun","relationship/relative","Mae perthynas agos rhyngom."),("cydweithiwr","noun","colleague","Mae fy nghydweithiwr yn y cyfarfod."),
    ]),
    _vset("cy_a2_experience","A2","Profiadau","cy-a2-unit-5",[
        ("taith","noun","trip","Cawsom daith dda."),("ymweliad","noun","visit","Roedd yr ymweliad yn ddiddorol."),("lle","noun","place","Mae'n lle hardd."),("diddorol","adjective","interesting","Mae'r llyfr yn ddiddorol."),("cofio","verb","remember","Dw i'n cofio'r lle."),("anghofio","verb","forget","Peidiwch ag anghofio."),
    ]),
    _vset("cy_a2_review","A2","Cyfathrebu A2","cy-a2-unit-6",[
        ("cwestiwn","noun","question","Mae gen i gwestiwn."),("ateb","noun","answer","Dyma'r ateb."),("esboniad","noun","explanation","Diolch am yr esboniad."),("cyfle","noun","opportunity","Mae'n gyfle da."),("penderfyniad","noun","decision","Mae angen penderfyniad."),("hapus","adjective","happy","Dw i'n hapus."),
    ]),
    _vset("cy_b1_activities","B1","Gweithgareddau a nodau","cy-b1-unit-1",[
        ("dysgu","verb","learn","Dw i'n dysgu Cymraeg."),("datblygu","verb","develop","Rydyn ni'n datblygu'r prosiect."),("nod","noun","goal","Mae gen i nod clir."),("ymarfer","noun","practice","Mae angen ymarfer."),("ymdrech","noun","effort","Gwnaeth hi ymdrech fawr."),("cynnydd","noun","progress","Mae cynnydd da wedi'i wneud."),
    ]),
    _vset("cy_b1_conditions","B1","Amodau a phosibiliadau","cy-b1-unit-2",[
        ("pe bai","conjunction","if it were","Pe bai gen i amser, byddwn i'n mynd."),("byddwn i","conditional","I would","Byddwn i'n helpu."),("posibilrwydd","noun","possibility","Mae posibilrwydd arall."),("cyfle","noun","chance","Mae cyfle da gennym."),("oni bai","conjunction","unless","Ni fydd yn digwydd oni bai..."),("rhag ofn","phrase","in case","Ewch â chôt rhag ofn."),
    ]),
    _vset("cy_b1_language","B1","Treigladau a gramadeg","cy-b1-unit-3",[
        ("treiglad meddal","noun","soft mutation","Mae treiglad meddal yma."),("treiglad trwynol","noun","nasal mutation","Mae treiglad trwynol mewn rhai patrymau."),("treiglad llaes","noun","aspirate mutation","Mae treiglad llaes yn newid rhai cytseiniaid."),("berf","noun","verb","Mae'r ferf yn y gorffennol."),("enw","noun","noun","Mae'r enw yn dilyn yr ansoddair mewn rhai patrymau."),("ansoddair","noun","adjective","Mae'r ansoddair yn disgrifio'r enw."),
    ]),
    _vset("cy_b1_opinion","B1","Barn a rhesymau","cy-b1-unit-4",[
        ("meddwl","verb","think","Dw i'n meddwl bod hyn yn bwysig."),("oherwydd","conjunction","because","Arosom oherwydd y tywydd."),("er bod","conjunction","although","Er bod hi'n hwyr, aethon ni."),("felly","connector","therefore/so","Roedd hi'n hwyr, felly aethon ni adref."),("barn","noun","opinion","Beth yw dy farn?"),("rheswm","noun","reason","Dyma'r rheswm."),
    ]),
    _vset("cy_b1_work","B1","Gwaith ac astudio","cy-b1-unit-5",[
        ("gwaith","noun","work","Mae llawer o waith."),("cyfarfod","noun","meeting","Mae cyfarfod am ddeg."),("prosiect","noun","project","Mae'r prosiect yn bwysig."),("ymchwil","noun","research","Mae ymchwil yn parhau."),("sgil","noun","skill","Mae'n sgil ddefnyddiol."),("cyfrifoldeb","noun","responsibility","Mae gen i gyfrifoldeb."),
    ]),
    _vset("cy_b1_discussion","B1","Trafodaeth","cy-b1-unit-6",[
        ("dadl","noun","argument/debate","Mae dadl dda gennym."),("cytuno","verb","agree","Dw i'n cytuno."),("anghytuno","verb","disagree","Dw i'n anghytuno."),("enghraifft","noun","example","Dyma enghraifft dda."),("safbwynt","noun","viewpoint","Mae safbwynt arall."),("tystiolaeth","noun","evidence","Mae angen tystiolaeth."),
    ]),
    _vset("cy_b2_reporting","B2","Adrodd a gwybodaeth","cy-b2-unit-1",[
        ("dywedodd","verb","said","Dywedodd hi ei bod hi'n brysur."),("gofynnodd","verb","asked","Gofynnodd e ble roeddwn i."),("honiad","noun","claim","Mae'r honiad yn ddadleuol."),("ffynhonnell","noun","source","Gwiriwch y ffynhonnell."),("adroddiad","noun","report","Darllenais yr adroddiad."),("datganiad","noun","statement","Cyhoeddwyd datganiad."),
    ]),
    _vset("cy_b2_media","B2","Cyfryngau a phrosesau","cy-b2-unit-2",[
        ("newyddion","noun","news","Gwrandewais ar y newyddion."),("cyhoeddi","verb","publish","Cafodd yr adroddiad ei gyhoeddi."),("erthygl","noun","article","Darllenais yr erthygl."),("penawd","noun","headline","Roedd y pennawd yn glir."),("digwyddiad","noun","event","Adroddwyd am y digwyddiad."),("gwybodaeth","noun","information","Mae angen rhagor o wybodaeth."),
    ]),
    _vset("cy_b2_argument","B2","Dadlau ac achosiaeth","cy-b2-unit-3",[
        ("er bod","conjunction","although","Er bod y dasg yn anodd, fe wnaethon ni ei chwblhau."),("oherwydd","conjunction","because","Oherwydd y tywydd, arhosom adref."),("canlyniad","noun","result","Dyma'r canlyniad."),("effaith","noun","effect","Mae effaith fawr."),("achos","noun","cause/reason","Mae angen deall yr achos."),("gwrthgyferbyniad","noun","contrast","Mae gwrthgyferbyniad clir."),
    ]),
    _vset("cy_b2_professional","B2","Cyfathrebu proffesiynol","cy-b2-unit-4",[
        ("yn ôl","phrase","according to","Yn ôl yr adroddiad..."),("dylid","impersonal verb","one should","Dylid ystyried y mater."),("argymhelliad","noun","recommendation","Dyma argymhelliad y tîm."),("penderfyniad","noun","decision","Gwnaed y penderfyniad."),("cynnig","noun","proposal/offer","Mae cynnig newydd."),("polisi","noun","policy","Adolygwyd y polisi."),
    ]),
    _vset("cy_b2_society","B2","Cymdeithas a gwasanaethau","cy-b2-unit-5",[
        ("cymuned","noun","community","Mae'r gymuned yn cymryd rhan."),("cymdeithas","noun","society","Mae cymdeithas yn newid."),("gwasanaeth","noun","service","Mae'r gwasanaeth ar gael."),("addysg","noun","education","Mae addysg yn bwysig."),("amgylchedd","noun","environment","Rhaid gwarchod yr amgylchedd."),("adnodd","noun","resource","Mae'r adnodd yn werthfawr."),
    ]),
    _vset("cy_b2_review","B2","Adolygiad B2","cy-b2-unit-6",[
        ("cymhleth","adjective","complex","Mae'n fater cymhleth."),("manwl","adjective","detailed","Mae disgrifiad manwl."),("perthnasol","adjective","relevant","Mae'r wybodaeth yn berthnasol."),("dibynadwy","adjective","reliable","Mae'r ffynhonnell yn ddibynadwy."),("niwtral","adjective","neutral","Defnyddiwch iaith niwtral."),("cyson","adjective","consistent","Rhaid bod yn gyson."),
    ]),
    _vset("cy_c1_formal","C1","Ysgrifennu ffurfiol","cy-c1-unit-1",[
        ("cynnydd","noun","increase/progress","Mae cynnydd sylweddol wedi digwydd."),("gostyngiad","noun","reduction","Gwelwyd gostyngiad yn y costau."),("newid","noun","change","Mae angen newid systematig."),("gofyniad","noun","requirement","Mae hwn yn ofyniad."),("dull","noun","approach/method","Mae dull newydd wedi'i gynnig."),("egwyddor","noun","principle","Mae'r egwyddor yn glir."),
    ]),
    _vset("cy_c1_argument","C1","Dadansoddiad a thystiolaeth","cy-c1-unit-2",[
        ("mae'n ymddangos","expression","it appears","Mae'n ymddangos bod newid."),("gellid dadlau","expression","one could argue","Gellid dadlau bod angen dull arall."),("yn seiliedig ar","phrase","based on","Mae'r penderfyniad yn seiliedig ar ddata."),("asesiad","noun","assessment","Cafodd asesiad ei gwblhau."),("dehongliad","noun","interpretation","Mae dehongliad arall yn bosibl."),("prawf","noun","proof/test","Nid oes prawf pendant."),
    ]),
    _vset("cy_c1_pragmatics","C1","Nuance a phragmateg","cy-c1-unit-3",[
        ("goblygiad","noun","implication","Mae goblygiad pwysig."),("is-destun","noun","subtext","Mae'r is-destun yn bwysig."),("pwyslais","noun","emphasis","Rhoddodd bwyslais ar y pwynt."),("ewyllys da","noun phrase","goodwill","Dangosodd ewyllys da."),("cwrtais","adjective","polite","Mae'r ateb yn gwrtais."),("priodol","adjective","appropriate","Mae'r tôn yn briodol."),
    ]),
    _vset("cy_c1_culture","C1","Diwylliant a hunaniaeth","cy-c1-unit-4",[
        ("treftadaeth","noun","heritage","Mae'n rhan o'r dreftadaeth."),("traddodiad","noun","tradition","Mae'r traddodiad yn fyw."),("hunaniaeth","noun","identity","Trafodwyd hunaniaeth ddiwylliannol."),("iaith leiafrifol","noun phrase","minority language","Mae'n iaith leiafrifol mewn rhai cyd-destunau."),("adfywiad","noun","revival","Mae adfywiad ieithyddol yn digwydd."),("llenyddiaeth","noun","literature","Mae hi'n darllen llenyddiaeth Gymraeg."),
    ]),
    _vset("cy_c1_public","C1","Bywyd cyhoeddus","cy-c1-unit-5",[
        ("llywodraethu","noun","governance","Mae llywodraethu da yn bwysig."),("cyfranogiad","noun","participation","Mae cyfranogiad y cyhoedd yn bwysig."),("atebolrwydd","noun","accountability","Mae atebolrwydd yn hanfodol."),("tryloywder","noun","transparency","Mae angen tryloywder."),("mesur","noun","measure","Cymerwyd mesur priodol."),("strategaeth","noun","strategy","Mae strategaeth hirdymor."),
    ]),
    _vset("cy_c1_review","C1","Adolygiad C1","cy-c1-unit-6",[
        ("cynnil","adjective","subtle","Mae'n wahaniaeth cynnil."),("amwys","adjective","ambiguous","Mae'r datganiad yn amwys."),("cynhwysfawr","adjective","comprehensive","Mae'n adolygiad cynhwysfawr."),("beirniadol","adjective","critical","Mae angen darllen beirniadol."),("annibynnol","adjective","independent","Mae'n asesiad annibynnol."),("cywirdeb","noun","accuracy","Mae cywirdeb yn bwysig."),
    ]),
    _vset("cy_c2_syntax","C2","Cystrawen gymhleth","cy-c2-unit-1",[
        ("yr hyn sy'n","relative phrase","what/that which is","Yr hyn sy'n bwysig yw..."),("o'r herwydd","connector","therefore","O'r herwydd, mae angen newid."),("er na ellir","phrase","although one cannot","Er na ellir rhagweld y canlyniad..."),("ar y llaw arall","connector","on the other hand","Ar y llaw arall, mae manteision."),("nid yn unig","connector","not only","Nid yn unig y newidiodd y system..."),("o reidrwydd","adverb","necessarily","Nid yw hynny'n wir o reidrwydd."),
    ]),
    _vset("cy_c2_rhetoric","C2","Rhethreg a steil","cy-c2-unit-2",[
        ("yn y lle cyntaf","connector","first of all","Yn y lle cyntaf, rhaid deall y cyd-destun."),("yn y pen draw","connector","ultimately","Yn y pen draw, mae'n fater o werthoedd."),("ar y naill law","connector","on the one hand","Ar y naill law, mae manteision."),("ar y llaw arall","connector","on the other hand","Ar y llaw arall, mae risgiau."),("pwysleisio","verb","emphasise","Mae'n bwysig pwysleisio hyn."),("tu hwnt i","phrase","beyond","Edrychwch y tu hwnt i'r ffigurau."),
    ]),
    _vset("cy_c2_analysis","C2","Dadansoddiad beirniadol","cy-c2-unit-3",[
        ("dadansoddiad","noun","analysis","Mae angen dadansoddiad manwl."),("rhagdybiaeth","noun","assumption/hypothesis","Rhaid herio'r rhagdybiaeth."),("gwrthddadl","noun","counterargument","Mae gwrthddadl gref."),("cyd-destun","noun","context","Rhaid ystyried y cyd-destun."),("cwmpas","noun","scope","Mae cwmpas yr astudiaeth yn gyfyng."),("dibynadwyedd","noun","reliability","Aseswyd dibynadwyedd y data."),
    ]),
    _vset("cy_c2_nuance","C2","Nuance","cy-c2-unit-4",[
        ("cliw","noun","clue","Mae'r gair yn rhoi cliw."),("tôn","noun","tone","Mae'r tôn yn newid."),("awgrym","noun","hint/suggestion","Rhoddodd awgrym cynnil."),("eironi","noun","irony","Mae eironi yn dibynnu ar gyd-destun."),("ffurfioldeb","noun","formality","Mae lefel y ffurfioldeb yn newid."),("addasu","verb","adapt","Mae angen addasu'r iaith."),
    ]),
    _vset("cy_c2_academic","C2","Academaidd a phroffesiynol","cy-c2-unit-5",[
        ("rhagdybiaeth","noun","hypothesis","Mae'r rhagdybiaeth i'w phrofi."),("methodoleg","noun","methodology","Esbonnir y fethodoleg."),("cydberthynas","noun","correlation","Nid yw cydberthynas yn golygu achosiaeth."),("adolygiad","noun","review","Cyhoeddwyd adolygiad cynhwysfawr."),("casgliad","noun","conclusion","Dyma'r casgliad mwyaf rhesymol."),("cyfyngiad","noun","limitation","Dylid cydnabod y cyfyngiad."),
    ]),
    _vset("cy_c2_mastery","C2","Meistrolaeth","cy-c2-unit-6",[
        ("manwl gywirdeb","noun","precision","Mae manwl gywirdeb yn hanfodol."),("hyblygrwydd","noun","flexibility","Mae'n dangos hyblygrwydd arddull."),("rhuglder","noun","fluency","Mae ganddi ruglder uchel."),("cyfoeth","noun","richness","Mae cyfoeth geirfaol yn amlwg."),("gwahaniaethu","noun","distinction","Mae gwahaniaethu yn bwysig."),("meistrolaeth","noun","mastery","Mae'r testun yn dangos meistrolaeth."),
    ]),
]

PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id="cy-a1-social",level="A1",situation="Cyfarchion",icon="💬",phrases=[
        PhrasebookEntry(text="Helo! Sut wyt ti?",context="greeting",register="neutral"),
        PhrasebookEntry(text="Dw i'n iawn, diolch.",context="reply",register="neutral"),
        PhrasebookEntry(text="Bore da!",context="morning",register="neutral"),
        PhrasebookEntry(text="Hwyl am y tro.",context="farewell",register="neutral"),
    ]),
    PhrasebookCategory(id="cy-a1-survival",level="A1",situation="Anghenion dyddiol",icon="🧭",phrases=[
        PhrasebookEntry(text="Ble mae'r toiled?",context="location",register="neutral"),
        PhrasebookEntry(text="Helpwch fi, os gwelwch yn dda.",context="help",register="neutral"),
        PhrasebookEntry(text="Dw i ddim yn deall.",context="comprehension",register="neutral"),
        PhrasebookEntry(text="Allwch chi ddweud hynny eto?",context="clarification",register="neutral"),
    ]),
    PhrasebookCategory(id="cy-a2-shopping",level="A2",situation="Siopa",icon="🛍️",phrases=[
        PhrasebookEntry(text="Faint yw e?",context="price",register="neutral"),
        PhrasebookEntry(text="Hoffwn i hwn.",context="purchase",register="neutral"),
        PhrasebookEntry(text="Oes un rhatach gennych chi?",context="comparison",register="neutral"),
        PhrasebookEntry(text="Mae hynny'n iawn.",context="agreement",register="neutral"),
    ]),
    PhrasebookCategory(id="cy-a2-travel",level="A2",situation="Teithio",icon="🚌",phrases=[
        PhrasebookEntry(text="Ble mae'r orsaf?",context="directions",register="neutral"),
        PhrasebookEntry(text="Hoffwn i docyn, os gwelwch yn dda.",context="ticket",register="neutral"),
        PhrasebookEntry(text="Pryd mae'r bws yn gadael?",context="schedule",register="neutral"),
        PhrasebookEntry(text="Pa mor hir fydd e'n cymryd?",context="duration",register="neutral"),
    ]),
    PhrasebookCategory(id="cy-b1-work",level="B1",situation="Gwaith ac astudio",icon="💼",phrases=[
        PhrasebookEntry(text="Hoffwn i roi fy marn.",context="discussion",register="neutral"),
        PhrasebookEntry(text="Dw i'n meddwl bod hyn yn bosibl.",context="opinion",register="neutral"),
        PhrasebookEntry(text="Allwn ni drafod hyn yn nes ymlaen?",context="meeting",register="neutral"),
        PhrasebookEntry(text="Mae angen rhagor o wybodaeth.",context="information",register="neutral"),
    ]),
    PhrasebookCategory(id="cy-b2-professional",level="B2",situation="Cyfathrebu ffurfiol",icon="📄",phrases=[
        PhrasebookEntry(text="Yn ôl yr adroddiad, mae angen newid.",context="reporting",register="formal"),
        PhrasebookEntry(text="Dylid ystyried y mater yn ofalus.",context="recommendation",register="formal"),
        PhrasebookEntry(text="Hoffwn ofyn am eglurhad.",context="clarification",register="formal"),
        PhrasebookEntry(text="Edrychaf ymlaen at glywed gennych.",context="correspondence",register="formal"),
    ]),
    PhrasebookCategory(id="cy-c1-discussion",level="C1",situation="Dadlau ac ymchwil",icon="🧠",phrases=[
        PhrasebookEntry(text="Gellid dadlau bod dewis arall.",context="argument",register="formal"),
        PhrasebookEntry(text="Mae'n ymddangos bod y mater yn fwy cymhleth.",context="qualification",register="formal"),
        PhrasebookEntry(text="Dylid ystyried y cyd-destun.",context="analysis",register="formal"),
        PhrasebookEntry(text="Nid yw'r ddau beth o reidrwydd yn gyfystyr.",context="distinction",register="formal"),
    ]),
    PhrasebookCategory(id="cy-c2-rhetoric",level="C2",situation="Rhethreg a steil",icon="✍️",phrases=[
        PhrasebookEntry(text="Yn y lle cyntaf, mae'n werth ystyried y cyd-destun.",context="opening_argument",register="formal"),
        PhrasebookEntry(text="Ar y llaw arall, mae tystiolaeth arall.",context="contrast",register="formal"),
        PhrasebookEntry(text="Nid yn unig y mae'r mater yn berthnasol, mae hefyd yn fater brys.",context="emphasis",register="formal"),
        PhrasebookEntry(text="Yn y pen draw, mae'n fater o werthoedd.",context="conclusion",register="formal"),
    ]),
]

ASSESSMENT_BANK = [
    AssessmentQuestion(id="cy-a1-001",skill="communication",difficulty="A1",question="How do you say “hello” in Welsh?",options=["Helo","Diolch","Hwyl","Ble wyt ti?"],correct="Helo"),
    AssessmentQuestion(id="cy-a1-002",skill="grammar",difficulty="A1",question="Which sentence means “I am a student”?",options=["Dw i'n fyfyriwr.","Mae fyfyriwr i.","Fyfyriwr dw i ddim.","Dw i fyfyriwr yn."],correct="Dw i'n fyfyriwr."),
    AssessmentQuestion(id="cy-a1-003",skill="grammar",difficulty="A1",question="Which sentence means “I am not tired”?",options=["Dw i ddim yn flinedig.","Dw i'n flinedig.","Dydy hi ddim yma.","Dw i ddim yma."],correct="Dw i ddim yn flinedig."),
    AssessmentQuestion(id="cy-a1-004",skill="vocabulary",difficulty="A1",question="Which Welsh word means “friend”?",options=["ffrind","enw","tŷ","bwyd"],correct="ffrind"),
    AssessmentQuestion(id="cy-a2-001",skill="grammar",difficulty="A2",question="Which sentence refers to a completed past event?",options=["Es i i'r siop ddoe.","Bydda i'n mynd yfory.","Dw i'n mynd nawr.","Dw i'n mynd i fynd."],correct="Es i i'r siop ddoe."),
    AssessmentQuestion(id="cy-a2-002",skill="grammar",difficulty="A2",question="Which expression means “I am going to study”?",options=["Dw i'n mynd i astudio.","Es i astudio.","Bydda i astudio.","Dw i ddim astudio."],correct="Dw i'n mynd i astudio."),
    AssessmentQuestion(id="cy-a2-003",skill="grammar",difficulty="A2",question="Which word means “better”?",options=["gwell","mawr","bach","gorau"],correct="gwell"),
    AssessmentQuestion(id="cy-b1-001",skill="grammar",difficulty="B1",question="Complete: “Dw i'n ___ Cymraeg.”",options=["dysgu","dysgais","byddwn","gofynnodd"],correct="dysgu"),
    AssessmentQuestion(id="cy-b1-002",skill="grammar",difficulty="B1",question="Which sentence is hypothetical?",options=["Pe bai gen i amser, byddwn i'n mynd.","Dw i'n mynd heddiw.","Es i ddoe.","Bydd hi yfory."],correct="Pe bai gen i amser, byddwn i'n mynd."),
    AssessmentQuestion(id="cy-b1-003",skill="language",difficulty="B1",question="What is treiglad meddal?",options=["soft mutation","a tense","a noun","a question word"],correct="soft mutation"),
    AssessmentQuestion(id="cy-b2-001",skill="grammar",difficulty="B2",question="Which sentence reports what someone said?",options=["Dywedodd hi ei bod hi'n brysur.","Mae hi'n brysur.","Bydd hi'n brysur.","Roedd hi'n brysur."],correct="Dywedodd hi ei bod hi'n brysur."),
    AssessmentQuestion(id="cy-b2-002",skill="writing",difficulty="B2",question="Which expression suits a formal report?",options=["Yn ôl yr adroddiad...","Helo!","Hwyl!","Faint yw e?"],correct="Yn ôl yr adroddiad..."),
    AssessmentQuestion(id="cy-b2-003",skill="vocabulary",difficulty="B2",question="What does tystiolaeth mean?",options=["evidence","headline","family","tomorrow"],correct="evidence"),
    AssessmentQuestion(id="cy-c1-001",skill="writing",difficulty="C1",question="Which phrase appropriately qualifies a claim?",options=["Mae'n ymddangos bod...","Mae hyn bob amser yn wir.","Helo!","Hwyl!"],correct="Mae'n ymddangos bod..."),
    AssessmentQuestion(id="cy-c1-002",skill="analysis",difficulty="C1",question="Which term means “implication”?",options=["goblygiad","treftadaeth","gorsaf","bwrdd"],correct="goblygiad"),
    AssessmentQuestion(id="cy-c1-003",skill="analysis",difficulty="C1",question="What is the function of hedging?",options=["To calibrate the strength of a claim","To greet someone","To form a plural","To ask a price"],correct="To calibrate the strength of a claim"),
    AssessmentQuestion(id="cy-c2-001",skill="style",difficulty="C2",question="Which connector means “on the other hand”?",options=["ar y llaw arall","yn y lle cyntaf","diolch","yfory"],correct="ar y llaw arall"),
    AssessmentQuestion(id="cy-c2-002",skill="analysis",difficulty="C2",question="Which term means “counterargument”?",options=["gwrthddadl","rhagdybiaeth","pwyslais","ffurfioldeb"],correct="gwrthddadl"),
    AssessmentQuestion(id="cy-c2-003",skill="style",difficulty="C2",question="Which phrase works as a formal conclusion?",options=["Yn y pen draw...","Helo!","Ble mae'r toiled?","Dw i eisiau dŵr."],correct="Yn y pen draw..."),
]

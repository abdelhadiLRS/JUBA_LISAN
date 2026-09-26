"""Guarani A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

def _g(slug,title,level,explanation,examples):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=f"Guarani {level} grammar.",explanation=explanation,examples=[GrammarExample(text=x) for x in examples])

_topics=[
("pronouns","Personal pronouns","A1","Use basic subject pronouns.","Che mbo'ehára."),
("identity","Nominal identification","A1","Identify people and things without an English-style copula.","Che héra Ana."),
("questions","Question words","A1","Ask who, what, where and how much.","Mba'éichapa nde réra?"),
("negation","Basic negation","A1","Negate simple clauses with nd- ... -i.","Ndaha'éi che róga."),
("possession","Possession with che/ne/nde","A1","Express personal possession.","Kóva che róga."),
("location","Location and existence","A1","Express where people and things are.","Aime Paraguaýpe."),
("requests","Imperatives and polite requests","A1","Make simple requests and commands.","Epytyvõmi, ikatúpa."),
("present","Present and habitual actions","A2","Describe current and habitual actions.","Añe'ẽ guaraníme."),
("past","Past events","A2","Describe completed events with past marking.","Aguata kuri ko'ápe."),
("future","Future and intention","A2","Express future actions and plans.","Ahaíta ko'ẽrõ."),
("aspect","Aspect and event state","A2","Distinguish ongoing, completed and habitual events.","Aikuaa gueteri."),
("plural","Plural participants and inclusive/exclusive meaning","A2","Use plural pronouns and participant distinctions.","Ñande jaha ko'ápe."),
("comparatives","Comparatives and superlatives","A2","Compare people, places and objects.","Ko óga tuichave."),
("modality","Ability, desire and obligation","A2","Express ability, desire and necessity.","Aikuaa hag̃ua mba'éichapa."),
("serial","Serial and linked actions","B1","Connect actions in natural sequences.","Aguata aheka hag̃ua."),
("postpositions","Relational phrases and postpositions","B1","Express direction, source and relation.","Aguata pe óga gotyo."),
("conditional","Conditional clauses","B1","Express conditions and hypothetical situations.","Rejúramo, roho hag̃ua."),
("relative","Relative clauses","B1","Modify nouns with relative clauses.","Pe kuimba'e oúva che irũ."),
("causal","Cause, purpose and result","B1","Connect reasons, purposes and consequences.","Aju ahecha hag̃ua chupe."),
("reported","Reported speech","B1","Report statements and information.","Ha'e ouha ko'ẽrõ."),
("reflexive","Reflexive and reciprocal meaning","B1","Express actions involving the participants themselves.","Ojohayhu hikuái."),
("passive","Passive and impersonal constructions","B2","Shift focus to the affected participant.","Ojejapo peteĩ tembiapo."),
("causative","Causative constructions","B2","Express causing or making something happen.","Ambo'e chupe guaraní."),
("concessive","Concession and contrast","B2","Express despite, although and contrast.","Jepémo oky, roho."),
("discourse","Discourse connectors","B2","Organize extended speech and writing.","Ñepyrũrã, jahechamína pe problema."),
("nominalization","Nominalization and deverbal nouns","C1","Build formal nouns from processes and actions.","Ñemoarandu iporãiterei."),
("hedging","Academic hedging and stance","C1","Qualify claims and signal degrees of certainty.","Ikatu ja'e ko resultado oñemoambueha."),
("embedded","Embedded questions and clauses","C1","Embed questions and propositions.","Ndikuaái moõpa oĩ."),
("information_structure","Topic and focus","C1","Highlight old and new information.","Ko mba'e, che aikuaa porã."),
("formal","Formal and institutional Guarani","C1","Use professional and institutional registers.","Ojejerure oñemondo hag̃ua marandu."),
("argumentation","Academic argumentation","C1","Build claims, evidence and counterarguments.","Ko je'epy oñemopyenda kuaapy rehe."),
("pragmatics","Politeness and pragmatic nuance","C2","Interpret indirectness, respect and social meaning.","Ikatúramo, ejesareko jeýna."),
("register","Register shifting","C2","Shift between colloquial, neutral and formal styles.","Ñe'ẽ ojuehegua iñambue contexto rupi."),
("rhetoric","Rhetorical and persuasive style","C2","Use emphasis, contrast and persuasive framing.","Ndaha'éi peteĩ problema año, ha'e avei peteĩ oportunidad."),
("translation","Translation and paraphrase","C2","Preserve meaning, register and discourse function.","Ñembohasa porã omantene he'iséva."),
("discourse_analysis","Discourse analysis","C2","Analyze cohesion, audience, genre and pragmatic effect.","He'iséva odepende contexto rehe.")
]
GRAMMAR_TOPICS=[_g(*x) for x in _topics]

def _v(id_,level,topic,ref,items):
    return VocabularySet(id=id_,level=level,topic=topic,unit_ref=ref,words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in items])

VOCABULARY_SETS=[
_v("greetings_a1","A1","greetings","gn-a1-unit-1",[("mba'éichapa","phrase","hello / how are you","Mba'éichapa!"),("aguyje","phrase","thank you","Aguyje nde pytyvõre."),("maitei","noun","greeting","Amondo ndéve maitei."),("jajotopata","phrase","see you","Jajotopata ko'ẽrõ.")]),
_v("identity_a1","A1","identity","gn-a1-unit-2",[("che","pronoun","I / my","Che héra Ana."),("nde","pronoun","you / your","Mba'éichapa nde réra?"),("téra","noun","name","Mba'épa nde réra?"),("mbo'ehára","noun","teacher","Ha'e mbo'ehára.")]),
_v("family_a1","A1","family","gn-a1-unit-3",[("sy","noun","mother","Che sy oiko Paraguaýpe."),("túva","noun","father","Che túva omba'apo."),("mitã","noun","child","Pe mitã opuka."),("irũ","noun","friend","Kóva che irũ.")]),
_v("home_a1","A1","home","gn-a1-unit-4",[("óga","noun","house","Kóva che róga."),("koty","noun","room","Aime che kotýpe."),("okẽ","noun","door","Eike pe okẽ rupi."),("mesa","noun","table","Pe kuatia oĩ mesa ári.")]),
_v("routine_a1","A1","daily routine","gn-a1-unit-5",[("mba'apo","verb","work","Amba'apo ko árape."),("moñe'ẽ","verb","read","Amoñe'ẽ peteĩ kuatia."),("ke","verb","sleep","Ake pyhare."),("guata","verb","walk","Aguata ko'ẽju.")]),
_v("food_a1","A1","food and drink","gn-a1-unit-6",[("y","noun","water","Ay'u y."),("tembi'u","noun","food","Akaru tembi'u."),("ka'ay","noun","tea","A'u ka'ay."),("mbujape","noun","bread","Akaru mbujape.")]),
_v("places_a1","A1","places and directions","gn-a1-unit-7",[("tenda","noun","place","Ko tenda iporã."),("tavaguasu","noun","city","Paraguay tavaguasu guasu."),("tapereko","noun","road / route","Ko tapereko ipuku."),("mercádo","noun","market","Aha mercado-pe.")]),
_v("help_a1","A1","help and communication","gn-a1-unit-8",[("pytyvõ","noun","help","Aikotevẽ nde pytyvõ."),("kuaa","verb","know","Aikuaa ko ñe'ẽ."),("ñe'ẽ","noun","language / speech","Añe'ẽ guaraníme."),("ikatu","verb","can / be possible","Ikatu piko reipytyvõ?")]),
_v("travel_a2","A2","travel","gn-a2-unit-1",[("jeguata","noun","trip / journey","Ore roho jeguata."),("avión","noun","airplane","Aguata avión-pe."),("mba'yrú","noun","vehicle","Ko mba'yrú iporã."),("tíquete","noun","ticket","Ajogua peteĩ tíquete.")]),
_v("health_a2","A2","health","gn-a2-unit-2",[("hasy","verb","hurt / be ill","Cherasy ko árape."),("pohãnohára","noun","doctor","Aha pohãnohára rendápe."),("pohã","noun","medicine","Aiporu pohã."),("tesãi","noun","health","Tesãi iñimportanteterei.")]),
_v("study_a2","A2","study","gn-a2-unit-3",[("mbo'e","verb","teach","Ambo'e guaraní."),("ñemoarandu","noun","study / education","Añeha'ã ñemoarandúpe."),("aranduka","noun","book","Amoñe'ẽ aranduka."),("temimbo'e","noun","student","Ha'e temimbo'e.")]),
_v("society_b1","B1","society","gn-b1-unit-1",[("tavaygua","noun","citizens / people","Tavaygua omba'apo oñondive."),("tekoha","noun","community / place","Ko tekoha oñomoirũ."),("ñopytyvõ","verb","help one another","Ñopytyvõ ñane rembiapo."),("tekoporã","noun","good conduct","Tekoporã iñimportante.")]),
_v("work_b1","B1","work and plans","gn-b1-unit-2",[("tembiapo","noun","work / task","Ko tembiapo ipuku."),("apopyre","noun","result / product","Pe apopyre oĩma."),("tavayguára","noun","public servant","Pe tavayguára omba'apo porã."),("tavayguára rembiapo","noun","public service","Tavayguára rembiapo oipytyvõ heta tapichápe.")]),
_v("environment_b2","B2","environment","gn-b2-unit-1",[("tekoha","noun","environment / habitat","Ñañangareko ñane tekoha rehe."),("ka'aguy","noun","forest","Ka'aguy tekotevẽ oñeñangareko hese."),("yvy","noun","land / earth","Yvy iporã ñande rekove hag̃ua."),("marandu","noun","information","Marandu pyahu oguahẽ.")]),
_v("economy_b2","B2","economy","gn-b2-unit-2",[("viru","noun","money","Aikotevẽ viru."),("ñemu","noun","commerce / trade","Ñemu oñemongakuaa."),("tembiapo","noun","employment / work","Tembiapo iporã tavayguápe g̃uarã."),("jehepyme'ẽ","noun","payment","Jehepyme'ẽ ojejapo ko árape.")]),
_v("media_c1","C1","media","gn-c1-unit-1",[("marandu","noun","news / information","Marandu oñembohasa pya'e."),("mombe'upy","noun","report / account","Mombe'upy oñemopyenda kuaapy rehe."),("he'iséva","noun","meaning","He'iséva odepende contexto rehe."),("mohendaha","noun","publisher / broadcaster","Mohendaha omosarambi marandu.")]),
_v("academic_c1","C1","academic","gn-c1-unit-2",[("kuaapy","noun","knowledge","Kuaapy oñembyatypa."),("jeporeka","noun","research / inquiry","Jeporeka oguereko heta mba'e."),("mbojoaju","noun","connection","Mbojoaju oipytyvõ oñeikũmby hag̃ua."),("mombe'u","noun","argument / account","Ko mombe'u oñemopyenda evidencia rehe.")]),
_v("institutional_c1","C1","institutional","gn-c1-unit-3",[("mboaje","noun","approval / recognition","Oñeme'ẽ mboaje pe tembiapópe."),("jerure","noun","request","Oñemondo jerure oficial."),("motenonde","verb","lead / direct","Ha'e omotenonde aty."),("mba'erechaha","noun","institution / organization","Pe mba'erechaha omba'apo tavayguáre.")]),
_v("culture_c2","C2","culture","gn-c2-unit-1",[("teko","noun","way of life / culture","Teko oñemoambue tiempo rupi."),("jerovia","noun","belief / trust","Jerovia oñemopyenda experiencia rehe."),("ñande reko","noun","our cultural identity","Ñande reko oñeñangareko va'erã."),("ñemoñare","noun","generation / descendants","Ñemoñare ogueraha ñane ñe'ẽ.")]),
_v("discourse_c2","C2","discourse and translation","gn-c2-unit-2",[("ñe'ẽjoaju","noun","discourse / connected speech","Ñe'ẽjoaju oikotevẽ joaju porã."),("he'iséva","noun","meaning","He'iséva iñambue contexto rupi."),("ñembohasa","noun","translation","Ñembohasa tekotevẽ oñangareko registro rehe."),("jehai","noun","writing","Je hai académico oikotevẽ claridad.")])
]

def _p(id_,level,situation,items,register="neutral"):
    return PhrasebookCategory(id=id_,level=level,situation=situation,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=register) for t,c in items])

PHRASEBOOK_CATEGORIES=[
_p("greetings_a1","A1","greetings",[("Mba'éichapa?","greeting"),("Mba'éichapa reime?","asking how someone is"),("Jajotopata!","saying see you")]),
_p("thanks_a1","A1","thanks and courtesy",[("Aguyje.","thanks"),("Aguyje nde pytyvõre.","thanks for your help"),("Iporãiterei.","positive response")]),
_p("shopping_a1","A1","shopping",[("Mboypa kóva?","asking price"),("Aipota kóva.","requesting an item"),("Ajogua kóva.","buying an item")]),
_p("directions_a1","A1","directions",[("Moõpa oĩ pe tenda?","asking location"),("Mba'éichapa aha upépe?","asking how to get there"),("Epytyvõmi, ikatúpa?","asking for help")]),
_p("daily_a1","A1","daily life",[("Amba'apo ko árape.","work"),("Añe'ẽ guaraníme.","language ability"),("Aime Paraguaýpe.","location")]),
_p("travel_a2","A2","travel",[("Ahaíta ko'ẽrõ.","future plan"),("Moõpa oĩ pe estación?","asking a location"),("Ajogua peteĩ tíquete.","buying a ticket")]),
_p("health_a2","A2","health",[("Cherasy ko árape.","illness"),("Aha pohãnohára rendápe.","going to doctor"),("Aikotevẽ pohã.","asking for medicine")]),
_p("study_b1","B1","study",[("Ndaikũmbýi, ikatúpa remyesakã?","asking clarification"),("Ere jeymi.","asking to repeat"),("Añeha'ã aikuaa porã hag̃ua.","study strategy")]),
_p("work_b1","B1","work",[("Ñañemongeta ko asunto rehe.","starting a discussion"),("Che apytu'ũme, ...","giving an opinion"),("Añe'ẽme'ẽ ko propuesta rehe.","making a proposal")]),
_p("formal_b2","B2","formal communication",[("Ojejerure oñemondo hag̃ua marandu.","formal request"),("Oñemomarandu ko decisión.","formal notice"),("Aguyje pende pytyvõre.","formal thanks")],"formal"),
_p("academic_c1","C1","academic discussion",[("Ikatu ja'e ko resultado ...","hedging"),("Ko evidencia ohechauka ...","presenting evidence"),("Upéicharõ jepe, tekotevẽ ñahesa'ỹijo ...","qualification")],"academic"),
_p("presentation_c1","C1","presentation",[("Ñepyrũrã, ñahesa'ỹijóta ...","opening"),("Ko punto iñimportante ...","highlighting"),("Ipahápe, ikatu ñamombe'u ...","closing")],"formal"),
_p("pragmatics_c2","C2","pragmatic nuance",[("Ikatúramo, ejesareko jeýna.","softening a request"),("Aikũmby nde re'íva, jepémo ...","polite disagreement"),("Ikatu ñahesa'ỹijo ambue hendáicha.","tentative suggestion")],"polite")
]

def _u(level,n,title,grammar,vocab):
    return CurriculumUnit(id=f"gn-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=grammar,vocabulary_set_ids=vocab,lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=[f"Communicate effectively at {level}",f"Understand level-appropriate Guarani"],default_weeks=2)

CURRICULUM={}
plans={
"A1":[("Maitei ha ñemoñe'ẽ",["pronouns","identity"],["greetings_a1"]),("Ñe'ẽme'ẽ ha marandu personal",["questions","possession"],["identity_a1"]),("Ñande rogaygua",["possession","plural"],["family_a1"]),("Óga ha tenda",["location","questions"],["home_a1"]),("Ára ha tembiapo",["present","negation"],["routine_a1"]),("Tembi'u ha y'u",["requests","possession"],["food_a1"]),("Tenda ha tape",["location","questions"],["places_a1"]),("Pytyvõ ha ñomongeta",["requests","negation"],["help_a1"])],
"A2":[("Jejapo ha jeguata",["future","postpositions"],["travel_a2"]),("Tesãi",["modality","aspect"],["health_a2"]),("Mbo'e ha ñemoarandu",["past","aspect"],["study_a2"]),("Tembiapo ára ha ára",["present","plural"],["routine_a1"]),("Potapy ha plan",["modality","future"],["work_b1"]),("Ñembojoja",["comparatives","modality"],["society_b1"]),("Tembiasakue",["past","aspect"],["travel_a2"]),("A2 ñemoarandu",["past","future","aspect"],["health_a2","study_a2"])],
"B1":[("Ñomongeta ha ñopytyvõ",["serial","postpositions"],["society_b1"]),("Plan ha condición",["conditional","future"],["work_b1"]),("Ñe'ẽjoaju ha ñemyesakã",["relative","discourse"],["environment_b2"]),("Mba'ére ha mba'épe g̃uarã",["causal","concessive"],["society_b1"]),("Marandu oñemombe'úva",["reported","embedded"],["media_c1"]),("Ñande jupe ha ambue",["reflexive","discourse"],["society_b1"]),("Marandu ha ñemombe'u",["reported","relative"],["media_c1"]),("B1 ñemoarandu",["conditional","causal","reported"],["work_b1","media_c1"])],
"B2":[("Tembiapo ha ñemomba'apo",["passive","causative"],["work_b1"]),("Mba'e omoheñói",["causative","aspect"],["economy_b2"]),("Jepémo ha joavy",["concessive","discourse"],["society_b1"]),("Viru ha ñemu",["passive","discourse"],["economy_b2"]),("Tekoha ha ka'aguy",["concessive","causal"],["environment_b2"]),("Marandu ñemohenda",["discourse","relative"],["media_c1"]),("Marandu jehecha ha ñemohenda",["passive","reported"],["media_c1"]),("B2 ñemoarandu",["passive","concessive","discourse"],["environment_b2","economy_b2"])],
"C1":[("Kuaapy ha evidencia",["nominalization","hedging"],["academic_c1"]),("Mba'erechaha ha teko formal",["formal","argumentation"],["institutional_c1"]),("Marandu ha ivurevure",["information_structure","reported"],["media_c1"]),("Porandu oñembojoajúva",["embedded","causal"],["academic_c1"]),("Ñomongeta académico",["argumentation","discourse"],["academic_c1"]),("Ñe'ẽ institucional",["formal","hedging"],["institutional_c1"]),("Tema ha énfasis",["information_structure","nominalization"],["media_c1"]),("C1 ñemoarandu",["argumentation","formal","embedded"],["academic_c1","institutional_c1"])],
"C2":[("Pragmática ha ñemomba'e",["pragmatics","register"],["discourse_c2"]),("Rhetoric ha ñe'ẽ académico",["rhetoric","discourse_analysis"],["culture_c2"]),("Registro ha contexto",["register","pragmatics"],["institutional_c1"]),("Ñe'ẽjoaju ñehesa'ỹijo",["discourse_analysis","information_structure"],["discourse_c2"]),("Ñembohasa ha paraphrase",["translation","register"],["culture_c2"]),("Argumentación académico",["argumentation","rhetoric"],["discourse_c2"]),("Teko ha media",["rhetoric","register"],["culture_c2","media_c1"]),("C2 ñemoarandu",["translation","pragmatics","discourse_analysis"],["discourse_c2","culture_c2"]])
}
for level,items in plans.items():
    CURRICULUM[level]=[_u(level,i+1,title,grammar,vocab) for i,(title,grammar,vocab) in enumerate(items)]

ASSESSMENT_BANK=[
AssessmentQuestion(id="gn-a1-001",skill="vocabulary",difficulty="A1",question="What does “mba'éichapa” express?",options=["hello/how are you","water","house","work"],correct="hello/how are you"),
AssessmentQuestion(id="gn-a1-002",skill="communication",difficulty="A1",question="Which phrase asks someone's name?",options=["Mba'épa nde réra?","Mboypa kóva?","Moõpa oĩ?","Jajotopata!"],correct="Mba'épa nde réra?"),
AssessmentQuestion(id="gn-a1-003",skill="vocabulary",difficulty="A1",question="Which word means mother?",options=["sy","óga","y","pytyvõ"],correct="sy"),
AssessmentQuestion(id="gn-a1-004",skill="grammar",difficulty="A1",question="Which sentence identifies the speaker's name?",options=["Che héra Ana.","Amba'apo ko árape.","Aime Paraguaýpe.","Ay'u y."],correct="Che héra Ana."),
AssessmentQuestion(id="gn-a2-001",skill="grammar",difficulty="A2",question="Which sentence expresses a future action?",options=["Ahaíta ko'ẽrõ.","Aime Paraguaýpe.","Amba'apo.","Aguyje."],correct="Ahaíta ko'ẽrõ."),
AssessmentQuestion(id="gn-a2-002",skill="grammar",difficulty="A2",question="Which sentence expresses a completed past event?",options=["Aguata kuri ko'ápe.","Ahaíta ko'ẽrõ.","Añe'ẽ guaraníme.","Mba'éichapa!"],correct="Aguata kuri ko'ápe."),
AssessmentQuestion(id="gn-b1-001",skill="grammar",difficulty="B1",question="Which phrase introduces a condition?",options=["Rejúramo, roho hag̃ua.","Mba'éichapa!","Aguyje.","Aime Paraguaýpe."],correct="Rejúramo, roho hag̃ua."),
AssessmentQuestion(id="gn-b1-002",skill="grammar",difficulty="B1",question="Which sentence reports information?",options=["Ha'e ouha ko'ẽrõ.","Che héra Ana.","Ay'u y.","Mboypa kóva?"],correct="Ha'e ouha ko'ẽrõ."),
AssessmentQuestion(id="gn-b2-001",skill="grammar",difficulty="B2",question="Which example uses concessive meaning?",options=["Jepémo oky, roho.","Aime Paraguaýpe.","Aguyje.","Che héra Ana."],correct="Jepémo oky, roho."),
AssessmentQuestion(id="gn-b2-002",skill="discourse",difficulty="B2",question="Which phrase organizes a discourse opening?",options=["Ñepyrũrã, ñahesa'ỹijóta.","Jajotopata.","Aguyje.","Mba'éichapa?"],correct="Ñepyrũrã, ñahesa'ỹijóta."),
AssessmentQuestion(id="gn-c1-001",skill="academic",difficulty="C1",question="Which phrase hedges an academic claim?",options=["Ikatu ja'e ko resultado oñemoambueha.","Pe resultado katuete upéicha.","Ani reñe'ẽ upévare.","Ahaíta ko'ẽrõ."],correct="Ikatu ja'e ko resultado oñemoambueha."),
AssessmentQuestion(id="gn-c1-002",skill="formal",difficulty="C1",question="Which phrase is an institutional request?",options=["Ojejerure oñemondo hag̃ua marandu.","Mba'éichapa!","Jajotopata!","Akaru mbujape."],correct="Ojejerure oñemondo hag̃ua marandu."),
AssessmentQuestion(id="gn-c2-001",skill="pragmatics",difficulty="C2",question="Which phrase softens a request?",options=["Ikatúramo, ejesareko jeýna.","Ejapo ko'ág̃a.","Sapy'ánte.","Aipota kóva."],correct="Ikatúramo, ejesareko jeýna."),
AssessmentQuestion(id="gn-c2-002",skill="translation",difficulty="C2",question="What should advanced translation preserve?",options=["Meaning, register and discourse function","Only literal words","Only word order","Only punctuation"],correct="Meaning, register and discourse function")
]

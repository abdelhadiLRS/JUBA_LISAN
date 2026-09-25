"""Xhosa foundation data for JUBA LISAN — A1 to C2."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

_DATA=[
("noun-classes","Noun classes and agreement","A1","morphology","Recognize common noun classes and agreement.","Umntu omdala uhamba."),
("copulative","Copulative identity","A1","syntax","Identify people and things.","Ndingumfundi."),
("present","Present tense","A1","verbs","Describe current and habitual actions.","Ndiyafunda yonke imihla."),
("negation","Negation","A1","verbs","Form negative statements.","Andifundi ngoku."),
("questions","Questions","A1","communication","Ask basic information questions.","Uhlala phi?"),
("possessives","Possessive constructions","A1","noun-phrase","Express ownership.","Le yincwadi yam."),
("locatives","Location and direction","A1","locative","Describe location and movement.","Usekhaya."),
("plural","Plural noun classes","A1","morphology","Recognize singular and plural classes.","Umntu / abantu."),
("past","Past tense","A2","verbs","Narrate completed events.","Izolo ndiye evenkileni."),
("future","Future tense","A2","verbs","Talk about plans and intentions.","Ndiza kufunda ngomso."),
("imperative","Imperatives and polite requests","A2","communication","Give instructions and requests.","Nceda uhlale apha."),
("comparison","Comparison","A2","adjectives","Compare people and things.","Le ndlu inkulu kunaleya."),
("modality","Ability obligation and desire","A2","modality","Express ability, necessity and desire.","Ndifuna ukufunda isiXhosa."),
("verbal-nouns","Verbal nouns","B1","verbs","Use verbal nouns as subjects and complements.","Ukufunda kubalulekile."),
("relative","Relative clauses","B1","syntax","Modify nouns with relative constructions.","Umntu endimbone ngumhlobo wam."),
("conditional","Conditional clauses","B1","syntax","Express real and hypothetical conditions.","Ukuba ixesha likhona, siza kuhamba."),
("reported","Reported speech","B1","discourse","Report statements and intentions.","Uthe uza kufika ngomso."),
("concession","Cause result and concession","B1","discourse","Connect causes and contrasts.","Nangona kunzima, siyaqhubeka."),
("aspect","Aspect and event structure","B2","verbs","Distinguish ongoing and completed events.","Bendisaqhubeka nokufunda."),
("passive","Passive constructions","B2","verbs","Focus on the affected participant.","Incwadi ibhalwe ngutitshala."),
("causative","Causative constructions","B2","derivation","Express caused actions.","Utitshala ufundisa abafundi."),
("connectors","Discourse connectors","B2","discourse","Organize arguments coherently.","Okokuqala sijonga ingxaki; emva koko sifune isisombululo."),
("formal","Formal professional register","B2","register","Use professional isiXhosa.","Nceda ungenise isicelo sakho ngokubhaliweyo."),
("nominalization","Nominalization","C1","academic","Use compact nominal structures.","Uphuhliso lwemfundo lubalulekile."),
("hedging","Academic hedging","C1","academic","Qualify academic claims.","Oku kungabonisa utshintsho oluthile."),
("embedded","Embedded questions","C1","syntax","Embed questions in formal statements.","Andazi ukuba uza kufika nini."),
("focus","Topic and focus","C1","discourse","Control emphasis and contrast.","Le ngxaki yeyona siyiphandayo."),
("argumentation","Academic argumentation","C1","rhetoric","Present claims and evidence.","Ubungqina buyayixhasa le mbono."),
("pragmatics","Pragmatics and politeness","C2","pragmatics","Interpret indirectness and social meaning.","Mhlawumbi singaphinda silijonge eli daba."),
("idioms","Idiomatic isiXhosa","C2","lexis","Interpret figurative expressions.","Umntu ngumntu ngabantu."),
("media","Media and public language","C2","register","Read reporting and institutional language.","Urhulumente ubhengeze umgaqo-nkqubo omtsha."),
("rhetoric","Rhetorical and literary style","C2","rhetoric","Analyze metaphor and rhetorical effect.","Amazwi akhe sisibane ebumnyameni."),
("translation","Translation precision","C2","translation","Choose context-sensitive equivalents.","Intsingiselo ixhomekeke kumxholo."),
("discourse-analysis","Discourse analysis","C2","discourse","Analyze cohesion and stance.","Umbhalo wakhe ulandela ingxoxo ngokucacileyo."),
("register-shift","Register shifting","C2","register","Reformulate messages across registers.","Lo myalezo ungabhalwa ngolwimi olusesikweni."),
]
GRAMMAR_TOPICS=[GrammarTopic(slug=s,title=t,level=l,category=c,summary=sm,explanation=f"{sm} Native isiXhosa model: {ex}",examples=[GrammarExample(text=ex)]) for s,t,l,c,sm,ex in _DATA]

_V=[
("xh-a1-1","Greetings","Molo","hello","Molo, Tata."),("xh-a1-2","Identity","igama","name","Igama lam nguLwazi."),("xh-a1-3","Family","umama","mother","Umama usekhaya."),("xh-a1-4","Home","indlu","house","Indlu inkulu."),("xh-a1-5","Routine","ukufunda","to study","Ndiyafunda kusasa."),("xh-a1-6","Time","ixesha","time","Liliphi ixesha?"),("xh-a1-7","Food","ukutya","food","Ndifuna ukutya."),("xh-a1-8","Places","idolophu","town","Ndiya edolophini."),
("xh-a2-1","Travel","uhambo","journey","Uhambo lude."),("xh-a2-2","Health","impilo","health","Impilo ibalulekile."),("xh-a2-3","Education","imfundo","education","Imfundo iyasinceda."),("xh-a2-4","Work","iofisi","office","Useofisini."),
("xh-b1-1","Communication","umyalezo","message","Ndithumele umyalezo."),("xh-b1-2","Community","uluntu","community","Uluntu luyasebenzisana."),("xh-b1-3","Environment","indalo","nature","Sikhusela indalo."),("xh-b1-4","Technology","ubuchwepheshe","technology","Ubuchwepheshe buyatshintsha."),
("xh-b2-1","Economy","uqoqosho","economy","Uqoqosho luyakhula."),("xh-b2-2","Policy","umgaqo-nkqubo","policy","Umgaqo-nkqubo omtsha uphunyezwa."),("xh-b2-3","Evidence","ubungqina","evidence","Ubungqina bubalulekile."),("xh-b2-4","Research","uphando","research","Uphando luvelisa iziphumo."),
("xh-c1-1","Analysis","uhlalutyo","analysis","Uhlalutyo lufuna ubungqina."),("xh-c1-2","Argument","ingxoxo","argument","Ingxoxo yakhe icacile."),("xh-c2-1","Rhetoric","intetho","rhetoric","Intetho yakhe iyakhuthaza."),("xh-c2-2","Context","umxholo","context","Intsingiselo ixhomekeke kumxholo."),("xh-c2-3","Translation","inguqulelo","translation","Le nguqulelo ichanekile.")]
VOCABULARY_SETS=[VocabularySet(id=i,level=i.split("-")[1].upper(),topic=t,unit_ref=f"{i}-unit-1",words=[VocabularyEntry(word=w,pos="noun",definition=d,example=e)]) for i,t,w,d,e in _V]

_UNITS={"A1":["Greetings and identity","Family and people","Home and location","Daily routine","Time and appointments","Food and shopping","Places and directions","Everyday communication"],"A2":["Past events","Future plans","Polite requests","Comparison","Ability and desire","Travel","Health","Education and work"],"B1":["Verbal nouns","Relative clauses","Conditions","Cause and contrast","Reported speech","Storytelling","Opinions","Connected conversation"],"B2":["Aspect","Passive voice","Causative forms","Discourse connectors","Formal register","Media texts","Evidence","Professional communication"],"C1":["Nominalization","Academic hedging","Embedded questions","Topic and focus","Argumentation","Research","Institutional language","Formal writing"],"C2":["Pragmatics","Idiomatic language","Media analysis","Rhetorical style","Translation precision","Discourse analysis","Register shifting","Literary synthesis"]}
CURRICULUM={}
for level in LEVELS:
    CURRICULUM[level]=[]
    for n,title in enumerate(_UNITS[level],1):
        vids=[v[0] for v in _V if v[0].split("-")[1].upper()==level] or ["xh-a1-1"]
        idx=min(LEVELS.index(level)*6+n-1,len(GRAMMAR_TOPICS)-1)
        CURRICULUM[level].append(CurriculumUnit(id=f"xh-{level.lower()}-unit-{n}",level=level,unit_number=n,title=f"Xhosa {level} · {title}",grammar_points=[GRAMMAR_TOPICS[idx].title],vocabulary_set_ids=vids[:1],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=[f"Use {level} isiXhosa in {title.lower()}","Understand authentic learner-level isiXhosa","Produce accurate spoken and written responses"],default_weeks=2))

PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="xh-greetings",level="A1",situation="Greetings",icon="👋",phrases=[PhrasebookEntry(text="Molo.",context="Hello.",register="neutral"),PhrasebookEntry(text="Unjani?",context="How are you?",register="neutral"),PhrasebookEntry(text="Ndiyaphila.",context="I am well.",register="neutral")]),
PhrasebookCategory(id="xh-thanks",level="A1",situation="Thanks",icon="🙏",phrases=[PhrasebookEntry(text="Enkosi.",context="Thank you.",register="neutral"),PhrasebookEntry(text="Enkosi kakhulu.",context="Thank you very much.",register="polite"),PhrasebookEntry(text="Wamkelekile.",context="You are welcome.",register="neutral")]),
PhrasebookCategory(id="xh-shopping",level="A1",situation="Shopping",icon="🛒",phrases=[PhrasebookEntry(text="Ixabisa malini le?",context="How much does this cost?",register="neutral"),PhrasebookEntry(text="Ndifuna le.",context="I want this one.",register="neutral"),PhrasebookEntry(text="Nceda, yehlisa ixabiso.",context="Please lower the price.",register="polite")]),
PhrasebookCategory(id="xh-help",level="A1",situation="Help",icon="🆘",phrases=[PhrasebookEntry(text="Nceda undincede.",context="Please help me.",register="polite"),PhrasebookEntry(text="Andiqondi.",context="I do not understand.",register="neutral"),PhrasebookEntry(text="Nceda uphinde.",context="Please repeat.",register="polite")]),
PhrasebookCategory(id="xh-directions",level="A1",situation="Directions",icon="🧭",phrases=[PhrasebookEntry(text="Isikhululo sikuphi?",context="Where is the station?",register="neutral"),PhrasebookEntry(text="Ndiya esikolweni.",context="I am going to school.",register="neutral"),PhrasebookEntry(text="Hamba ngqo.",context="Go straight.",register="neutral")]),
PhrasebookCategory(id="xh-restaurant",level="A2",situation="Restaurant",icon="🍽️",phrases=[PhrasebookEntry(text="Nceda undiphe imenyu.",context="Please give me the menu.",register="polite"),PhrasebookEntry(text="Ndifuna amanzi.",context="I want water.",register="neutral"),PhrasebookEntry(text="Nceda undiphe ityala.",context="Please bring the bill.",register="polite")]),
PhrasebookCategory(id="xh-travel",level="A2",situation="Travel",icon="✈️",phrases=[PhrasebookEntry(text="Iphi itikiti lam?",context="Where is my ticket?",register="neutral"),PhrasebookEntry(text="Ndifuna indawo yokulala.",context="I need a place to stay.",register="neutral"),PhrasebookEntry(text="Uhambo luthatha ixesha elingakanani?",context="How long does the journey take?",register="neutral")]),
PhrasebookCategory(id="xh-health",level="A2",situation="Health",icon="🩺",phrases=[PhrasebookEntry(text="Ndifuna ukubona ugqirha.",context="I need to see a doctor.",register="neutral"),PhrasebookEntry(text="Ndibuhlungu.",context="I am in pain.",register="neutral"),PhrasebookEntry(text="Siphi isibhedlele?",context="Where is the hospital?",register="neutral")]),
PhrasebookCategory(id="xh-work",level="B1",situation="Work",icon="💼",phrases=[PhrasebookEntry(text="Masiqale intlanganiso.",context="Let's start the meeting.",register="professional"),PhrasebookEntry(text="Nceda unikeze ubungqina.",context="Please provide the evidence.",register="professional"),PhrasebookEntry(text="Siyavumelana ngalo mba.",context="We agree on this matter.",register="professional")]),
PhrasebookCategory(id="xh-debate",level="B2",situation="Debate",icon="💬",phrases=[PhrasebookEntry(text="Ngokombono wam...",context="In my opinion...",register="neutral"),PhrasebookEntry(text="Ubungqina bubonisa ukuba...",context="The evidence shows that...",register="formal"),PhrasebookEntry(text="Kwelinye icala...",context="On the other hand...",register="formal")]),
PhrasebookCategory(id="xh-academic",level="C1",situation="Academic writing",icon="📚",phrases=[PhrasebookEntry(text="Olu phando lubonisa ukuba...",context="This study shows that...",register="academic"),PhrasebookEntry(text="Oku kungabonisa...",context="This may indicate...",register="academic"),PhrasebookEntry(text="Uphando olongezelelekileyo luyafuneka.",context="Further research is needed.",register="academic")]),
PhrasebookCategory(id="xh-formal",level="C1",situation="Formal correspondence",icon="📝",phrases=[PhrasebookEntry(text="Ngokuphathelele kwisicelo sakho...",context="Regarding your application...",register="formal"),PhrasebookEntry(text="Nceda ungenise isicelo sakho.",context="Please submit your application.",register="formal"),PhrasebookEntry(text="Siza kukuphendula kungekudala.",context="We will respond shortly.",register="formal")]),
PhrasebookCategory(id="xh-pragmatics",level="C2",situation="Nuance and pragmatics",icon="🎯",phrases=[PhrasebookEntry(text="Mhlawumbi singaphinda silijonge eli daba.",context="Perhaps we can reconsider this matter.",register="nuanced"),PhrasebookEntry(text="Oku kuxhomekeke kumxholo.",context="This depends on the context.",register="formal"),PhrasebookEntry(text="Masiyibeke ngenye indlela.",context="Let's put it another way.",register="nuanced")]),
]

ASSESSMENT_BANK=[
AssessmentQuestion(id="xh-a1-001",skill="communication",difficulty="A1",question="Which isiXhosa expression means Hello?",options=["Molo.","Enkosi.","Andiqondi.","Unjani?"],correct="Molo."),
AssessmentQuestion(id="xh-a1-002",skill="speaking",difficulty="A1",question="Which sentence means I am Lwazi?",options=["NdinguLwazi.","Ndifuna le.","Nceda undincede.","Enkosi kakhulu."],correct="NdinguLwazi."),
AssessmentQuestion(id="xh-a1-003",skill="vocabulary",difficulty="A1",question="Which word means name?",options=["igama","indlu","ixesha","ukutya"],correct="igama"),
AssessmentQuestion(id="xh-a1-004",skill="shopping",difficulty="A1",question="How do you ask the price?",options=["Ixabisa malini le?","Uhlala phi?","Ndiyaphila.","Nceda undincede."],correct="Ixabisa malini le?"),
AssessmentQuestion(id="xh-a2-005",skill="grammar",difficulty="A2",question="Which sentence refers to tomorrow?",options=["Ndiza kufunda ngomso.","Izolo ndiye evenkileni.","Ndiyafunda yonke imihla.","Ndifuna ukutya."],correct="Ndiza kufunda ngomso."),
AssessmentQuestion(id="xh-a2-006",skill="communication",difficulty="A2",question="Which is a polite request?",options=["Nceda uhlale apha.","Andifundi ngoku.","Usekhaya.","Ndiya edolophini."],correct="Nceda uhlale apha."),
AssessmentQuestion(id="xh-b1-007",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["Ukuba ixesha likhona, siza kuhamba.","Izolo ndiye evenkileni.","Ndingumfundi.","Enkosi."],correct="Ukuba ixesha likhona, siza kuhamba."),
AssessmentQuestion(id="xh-b1-008",skill="discourse",difficulty="B1",question="Which sentence reports what someone said?",options=["Uthe uza kufika ngomso.","Ndiyaphila.","Molo.","Ndifuna le."],correct="Uthe uza kufika ngomso."),
AssessmentQuestion(id="xh-b2-009",skill="discourse",difficulty="B2",question="Which expression introduces a contrast?",options=["Kwelinye icala...","Molo.","Nceda undincede.","Ndiyaphila."],correct="Kwelinye icala..."),
AssessmentQuestion(id="xh-c1-010",skill="academic",difficulty="C1",question="Which phrase appropriately hedges an academic claim?",options=["Oku kungabonisa...","Oku kungqina yonke into ngokupheleleyo.","Molo.","Ixabisa malini le?"],correct="Oku kungabonisa..."),
AssessmentQuestion(id="xh-c1-011",skill="formal",difficulty="C1",question="Which phrase fits formal correspondence?",options=["Nceda ungenise isicelo sakho.","Unjani?","Ndifuna le.","Molo."],correct="Nceda ungenise isicelo sakho."),
AssessmentQuestion(id="xh-c2-012",skill="pragmatics",difficulty="C2",question="Which phrase refers to context?",options=["Oku kuxhomekeke kumxholo.","Enkosi.","Usekhaya.","Ixabisa malini le?"],correct="Oku kuxhomekeke kumxholo."),
]

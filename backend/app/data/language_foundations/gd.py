"""Scottish Gaelic foundation data for JUBA LISAN."""

from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

_G=[
("copula","An copula agus dearbh-aithne","A1","grammar","Use Is for identification and description.","Is e oileanach a th' annam."),
("pronouns","Pronouns","A1","syntax","Use personal pronouns in simple exchanges.","Tha mi toilichte."),
("present-existential","Tha agus seilbh","A1","verbs","Use tha for states, location and possession.","Tha taigh agam."),
("lenition","Sèimheachadh","A1","phonology","Recognise common initial consonant changes after grammatical triggers.","Tha mo mhàthair an seo."),
("questions","Ceistean","A1","communication","Form basic questions with dè, cò, càit and ciamar.","Càit a bheil thu?"),
("negation","Negation","A1","syntax","Use chan eil and related negative patterns.","Chan eil mi sgìth."),
("possessives","Possessive adjectives","A1","grammar","Use mo, do, a, ar and related forms.","Seo mo leabhar."),
("basic-prepositions","Basic prepositions","A1","grammar","Use common prepositions for place and movement.","Tha e aig an taigh."),
("past-tense","Past tense","A2","verbs","Use past forms to describe completed events.","Bha mi ag obair an-dè."),
("future","Future and intentions","A2","verbs","Use future forms for plans and predictions.","Bidh mi ann a-màireach."),
("verbal-noun","Verbal noun","A2","verbs","Use verbal nouns in progressive and purpose constructions.","Tha mi ag ionnsachadh Gàidhlig."),
("numbers-time","Numbers and time","A2","lexis","Talk about times, dates and quantities.","Tha e trì uairean."),
("comparatives","Comparison","A2","adjectives","Compare people and things in common constructions.","Tha seo nas fheàrr."),
("modal-expressions","Ability and obligation","A2","modality","Express ability, necessity and intention.","Feumaidh mi falbh."),
("subordinate-clauses","Subordinate clauses","B1","syntax","Connect clauses with common subordinators.","Fuirichidh mi gus an tig e."),
("relative-clauses","Relative clauses","B1","syntax","Describe people and objects with relative structures.","An duine a chunnaic mi."),
("conditional","Conditional","B1","verbs","Express hypothetical situations and consequences.","Nam biodh ùine agam, bhithinn ann."),
("reported-speech","Reported speech","B1","discourse","Report information from another speaker.","Thuirt e gun tigeadh e."),
("past-narrative","Narrative past","B1","discourse","Organise events and background in narration.","Bha an t-uisge ann nuair a ràinig sinn."),
("connectors","Discourse connectors","B1","discourse","Link reasons, contrasts and conclusions.","Ach, mar sin, ge-tà."),
("passive","Passive constructions","B2","syntax","Describe actions without foregrounding the agent.","Chaidh an obair a dhèanamh."),
("causal-concessive","Cause and concession","B2","syntax","Express because, although and despite relations.","Ged a bha e fadalach, dh'fhuirich sinn."),
("relative-pronouns","Advanced relatives","B2","syntax","Handle more complex relative structures accurately.","An rud a bha sinn a' sireadh."),
("nominalization","Nominal style","B2","style","Use compact noun-based structures in formal writing.","Cur an gnìomh a' phlana."),
("formal-register","Formal register","B2","register","Adapt language to professional and institutional contexts.","Tha sinn ag iarraidh air sibh ..."),
("academic-hedging","Academic hedging","C1","academic","Qualify claims and distinguish evidence from interpretation.","Dh'fhaodadh seo nochdadh gu bheil ..."),
("embedded-questions","Embedded questions","C1","syntax","Embed questions in statements and requests.","Chan eil fios agam cuin a thig e."),
("information-structure","Focus and topic","C1","discourse","Control information focus for clarity and contrast.","Is ann an seo a thachair e."),
("complex-subordination","Complex subordination","C1","syntax","Combine several subordinate relations coherently.","Ged a bha an suidheachadh iom-fhillte, lean sinn air adhart."),
("institutional-language","Institutional Gaelic","C1","professional","Use precise language for public and organisational documents.","Feumar an fhoirm a chur a-steach."),
("idioms","Idiomatic Gaelic","C2","lexis","Interpret idioms beyond literal meaning.","Tha e a' cur connadh ris an teine."),
("register-shifting","Register shifting","C2","pragmatics","Move between conversational, professional and literary registers.","Am b' urrainn dhuibh dearbhadh?"),
("rhetoric","Rhetoric and argument","C2","rhetoric","Build nuanced claims, concessions and rebuttals.","Ged a tha an argamaid làidir, tha na fianais cuibhrichte."),
("literary-style","Literary style","C2","style","Interpret imagery and deliberate stylistic variation.","Dhùisg am baile fo sholas na maidne."),
("translation-precision","Translation precision","C2","translation","Choose context-sensitive Gaelic equivalents rather than literal calques.","Feumaidh an abairt a bhith freagarrach don cho-theacsa."),
]

GRAMMAR_TOPICS=[GrammarTopic(slug=s,title=t,level=l,category=c,summary=sm,explanation=sm,examples=[GrammarExample(text=e)]) for s,t,l,c,sm,e in _G]

_V={
"A1":[("Greetings","Halò","phrase","hello","Halò, ciamar a tha thu?"),("Identity","ainm","noun","name","Dè an t-ainm a th' ort?"),("Family","teaghlach","noun","family","Tha teaghlach mòr agam."),("Home","taigh","noun","house","Tha mi aig an taigh."),("Routine","obair","noun","work","Tha mi aig obair."),("Time","uair","noun","hour","Tha e dà uair."),("Food","tì","noun","tea","Bu toil leam tì."),("Places","stèisean","noun","station","Càit a bheil an stèisean?")],
"A2":[("Travel","tiogaid","noun","ticket","Tha tiogaid a dhìth orm."),("Health","dotair","noun","doctor","Tha mi a' dol chun an dotair."),("Shopping","prìs","noun","price","Dè a' phrìs a th' air?"),("Weather","sìde","noun","weather","Tha an aimsir math.")],
"B1":[("Work","eòlas","noun","experience","Tha tòrr eòlais agam."),("Education","cùrsa","noun","course","Tha mi air cùrsa Gàidhlig."),("Society","coimhearsnachd","noun","community","Tha a' choimhearsnachd gnìomhach."),("Opinion","beachd","noun","opinion","Nam bheachd-sa, tha e cudromach.")],
"B2":[("Professional","dàta","noun","data","Tha an dàta air a dhìon."),("Administration","iarrtas","noun","application","Chaidh an t-iarrtas a chur a-steach."),("Media","naidheachd","noun","news","Chuala mi an naidheachd."),("Environment","àrainneachd","noun","environment","Feumaidh sinn an àrainneachd a dhìon.")],
"C1":[("Academic","fianais","noun","evidence","Tha an fhianais buntainneach."),("Analysis","leasachadh","noun","development","Tha an leasachadh cudromach."),("Administration","riatanas","noun","requirement","Tha seo na riatanas."),("Argument","co-dhùnadh","noun","conclusion","Tha an co-dhùnadh faiceallach.")],
"C2":[("Rhetoric","nuance","noun","nuance","Tha an nuance cudromach."),("Pragmatics","co-theacsa","noun","context","Tha an co-theacsa deatamach."),("Literature","meafar","noun","metaphor","Tha am meafar cumhachdach."),("Translation","ciall","noun","meaning","Tha an ciall an urra ris a' cho-theacsa.")],
}
VOCABULARY_SETS=[]
for level,rows in _V.items():
    for i,(topic,word,pos,definition,example) in enumerate(rows,1):
        VOCABULARY_SETS.append(VocabularySet(id=f"gd-{level.lower()}-{i}",level=level,topic=topic,unit_ref=f"gd-{level.lower()}-unit-{i}",words=[VocabularyEntry(word=word,pos=pos,definition=definition,example=example)]))

_T={
"A1":["Dearbh-aithne","Teaghlach","Dachaigh","Cleachdadh làitheil","Ùine","Biadh","Àiteachan","Ath-sgrùdadh"],
"A2":["Eòlasan","Planaichean","Comas agus dleastanas","Siubhal","Coimeas","Slàinte"],
"B1":["Adhbharan","Tuairisgeulan","Cumhachan","Aithris","Sgeulachdan","Deasbad"],
"B2":["Pròiseasan","Concession","Tuairisgeulan iom-fhillte","Rianachd","Obair phroifeiseanta","Sgrìobhadh foirmeil"],
"C1":["Fianais","Ceistean agus freagairtean","Fòcas","Argamaid","Institiudan","Sgrìobhadh adhartach"],
"C2":["Idioman","Clàr cànain","Reul-eòlas","Litreachas","Eadar-theangachadh","Synthesis"],
}
CURRICULUM={}
_offsets={"A1":0,"A2":8,"B1":14,"B2":20,"C1":26,"C2":32}
for level,titles in _T.items():
    CURRICULUM[level]=[]
    for i,title in enumerate(titles,1):
        gslug=_G[_offsets[level]+i-1][0]
        CURRICULUM[level].append(CurriculumUnit(id=f"gd-{level.lower()}-unit-{i}",level=level,unit_number=i,title=f"Scottish Gaelic {level} · {title}",grammar_points=[gslug],vocabulary_set_ids=[f"gd-{level.lower()}-{min(i,len(_V[level]))}"],lesson_types=["grammar","vocabulary","reading","writing","listening","review"],competency_checklist=[f"Use Gaelic for {title.lower()}","Complete guided CEFR-level tasks"],default_weeks=2))

_P={
"A1":[("Greetings","👋",["Halò, ciamar a tha thu?","Is e ... an t-ainm a th' orm.","Tapadh leat."]),("Help","🆘",["Cuidich mi, mas e do thoil e.","Chan eil mi a' tuigsinn.","Am bruidhinn thu nas slaodaiche?"])],
"A2":[("Travel","🧳",["Càit a bheil an stèisean?","Aon tiogaid, mas e do thoil e.","Cuin a tha an trèana a' falbh?"]),("Health","🩺",["Chan eil mi gu math.","Tha feum agam air dotair.","Tha coinneamh agam."])],
"B1":[("Opinions","💭",["Nam bheachd-sa ...","Tha mi ag aontachadh.","Tha mi a' tuigsinn do bheachd."]),("Work","💼",["An urrainn dhuinn bruidhinn mu dheidhinn?","Cuiridh mi an sgrìobhainn thugad.","Cuin a tha a' choinneamh?"])],
"B2":[("Meetings","📅",["Am b' urrainn dhuinn seo a dheasbad?","Tha mi a' moladh gum ...","Dèanamaid coimeas eadar na roghainnean."]),("Administration","🏛️",["Chaidh an t-iarrtas a chur a-steach.","Am b' urrainn dhuibh dearbhadh sgrìobhte a thoirt?","Feumar an sgrìobhainn a chur a-steach."])],
"C1":[("Academic","🎓",["Dh'fhaodadh na toraidhean sealltainn gu bheil ...","Tha e cudromach an dàta a mhìneachadh.","Tha an fhianais a' toirt taic don cho-dhùnadh."]),("Presentation","📊",["Leig dhomh cuideam a chur air a' phuing seo.","An toiseach ...","Mu dheireadh, faodar a ràdh gu bheil ..."])],
"C2":[("Debate","⚖️",["Tha an mìneachadh seo comasach, ach ...","Tha e an urra gu mòr ris a' cho-theacsa.","Bu mhath leam eadar-dhealachadh a dhèanamh eadar ..."]),("Literature","📚",["Tha dà chiall aig an abairt seo.","Tha an ìomhaigheachd a' neartachadh a' chuspair.","Faodar an earrann a leughadh ann an diofar dhòighean."])],
}
PHRASEBOOK_CATEGORIES=[]
for level,cats in _P.items():
    for i,(situation,icon,phrases) in enumerate(cats,1):
        PHRASEBOOK_CATEGORIES.append(PhrasebookCategory(id=f"gd-{level.lower()}-phrases-{i}",level=level,situation=situation,icon=icon,phrases=[PhrasebookEntry(text=p,context=situation,register="neutral" if level in ("A1","A2") else "formal",unit_ref=f"gd-{level.lower()}-unit-{i}") for p in phrases]))

ASSESSMENT_BANK=[
AssessmentQuestion(id="gd-a1-001",skill="grammar",difficulty="A1",question="Which sentence identifies the speaker?",options=["Is e oileanach a th' annam.","Tha oileanach annam.","Oileanach tha mi.","Is oileanach mi a."],correct="Is e oileanach a th' annam.",grammar_slug="copula"),
AssessmentQuestion(id="gd-a1-002",skill="grammar",difficulty="A1",question="Which sentence is negative?",options=["Chan eil mi sgìth.","Tha mi sgìth.","Is toil leam tì.","Tha mi aig an taigh."],correct="Chan eil mi sgìth.",grammar_slug="negation"),
AssessmentQuestion(id="gd-a2-001",skill="grammar",difficulty="A2",question="Which sentence refers to tomorrow?",options=["Bidh mi ann a-màireach.","Bha mi ann an-dè.","Tha mi ann an-diugh.","Bha mi a-muigh."],correct="Bidh mi ann a-màireach.",grammar_slug="future"),
AssessmentQuestion(id="gd-a2-002",skill="vocabulary",difficulty="A2",question="Which word means doctor?",options=["dotair","tiogaid","prìs","sìde"],correct="dotair"),
AssessmentQuestion(id="gd-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a hypothetical condition?",options=["Nam biodh ùine agam, bhithinn ann.","Tha ùine agam.","Bidh ùine agam.","Bha ùine agam."],correct="Nam biodh ùine agam, bhithinn ann.",grammar_slug="conditional"),
AssessmentQuestion(id="gd-b1-002",skill="grammar",difficulty="B1",question="Which phrase introduces an opinion?",options=["Nam bheachd-sa ...","Tapadh leat.","Halò.","Càit a bheil e?"],correct="Nam bheachd-sa ...",grammar_slug="connectors"),
AssessmentQuestion(id="gd-b2-001",skill="grammar",difficulty="B2",question="Which sentence uses a passive construction?",options=["Chaidh an obair a dhèanamh.","Rinn iad an obair.","Bha iad ag obair.","Tha an obair math."],correct="Chaidh an obair a dhèanamh.",grammar_slug="passive"),
AssessmentQuestion(id="gd-b2-002",skill="communication",difficulty="B2",question="Which phrase is suitable for formal administration?",options=["Am b' urrainn dhuibh dearbhadh sgrìobhte a thoirt?","Hey, thoir dhomh e.","Dè tha seo?","Thoir dhomh sin."],correct="Am b' urrainn dhuibh dearbhadh sgrìobhte a thoirt?",grammar_slug="formal-register"),
AssessmentQuestion(id="gd-c1-001",skill="grammar",difficulty="C1",question="Which sentence contains an embedded question?",options=["Chan eil fios agam cuin a thig e.","Cuin a thig e?","Thig e a-màireach.","Tha fios agam."],correct="Chan eil fios agam cuin a thig e.",grammar_slug="embedded-questions"),
AssessmentQuestion(id="gd-c1-002",skill="reading",difficulty="C1",question="Which phrase appropriately hedges a claim?",options=["Dh'fhaodadh seo nochdadh gu bheil ...","Tha seo an-còmhnaidh fìor.","Tha seo a' dearbhadh a h-uile càil.","Chan eil teagamh sam bith ann."],correct="Dh'fhaodadh seo nochdadh gu bheil ...",grammar_slug="academic-hedging"),
AssessmentQuestion(id="gd-c2-001",skill="grammar",difficulty="C2",question="Which phrase introduces a qualified rebuttal?",options=["Tha an mìneachadh seo comasach, ach ...","Tha sin ceàrr.","Chan eil fhios agam.","Chan eil e gu diofar."],correct="Tha an mìneachadh seo comasach, ach ...",grammar_slug="rhetoric"),
AssessmentQuestion(id="gd-c2-002",skill="reading",difficulty="C2",question="What is central to advanced translation?",options=["Context-sensitive equivalents","Literal word-for-word translation","Ignoring context","One synonym everywhere"],correct="Context-sensitive equivalents",grammar_slug="translation-precision"),
]

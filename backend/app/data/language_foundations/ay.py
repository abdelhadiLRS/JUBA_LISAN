"""Aymara A1-C2 curriculum data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

def _g(slug, title, level, summary, example):
    return GrammarTopic(slug=slug, title=title, level=level, category="grammar",
        summary=summary, explanation=f"Practice {title.lower()} in authentic Aymara contexts.",
        examples=[GrammarExample(text=example)])

GRAMMAR_TOPICS = [
    _g("a1-pronouns","Personal pronouns","A1","Use personal pronouns and basic reference.","Nayax Ana satawa."),
    _g("a1-copula","Identity and nominal predicates","A1","Introduce people and identify things.","Akax utaawa."),
    _g("a1-present","Present and habitual actions","A1","Talk about current and usual actions.","Aymar aru yatiqaskta."),
    _g("a1-questions","Question words and yes-no questions","A1","Ask who, what, where and how.","Kunas sutimaxa?"),
    _g("a1-negation","Negation with jani","A1","Make simple negative statements.","Janiw yatkti."),
    _g("a1-possessive","Possessive suffixes","A1","Express basic possession.","Utajaxa."),
    _g("a1-location","Location and basic case marking","A1","Say where people and objects are.","Uta manqhanwa jikxatasta."),
    _g("a1-requests","Requests and polite expressions","A1","Make simple requests politely.","Yanapt'ita, mirä."),
    _g("a2-past","Past events","A2","Describe completed and recent events.","Qharüru La Pazaru sarayäta."),
    _g("a2-future","Future and intention","A2","Talk about plans and intentions.","Qharüru yatiqañaru sarä."),
    _g("a2-cases","Core case suffixes","A2","Use case suffixes for relations and movement.","Utaru sarä."),
    _g("a2-comparison","Comparison and degree","A2","Compare people, objects and situations.","Jilax jisk'a."),
    _g("a2-imperative","Commands and polite instructions","A2","Give instructions and requests.","Qillqam."),
    _g("a2-ability","Ability, necessity and desire","A2","Express ability, need and desire.","Yatiqañ munta."),
    _g("b1-aspect","Aspect and event structure","B1","Distinguish ongoing, habitual and completed events.","Yatiqaskta."),
    _g("b1-subordination","Subordinate clauses","B1","Connect clauses to explain events and reasons.","Kunatix jutkta uk yatiyta."),
    _g("b1-conditionals","Conditional clauses","B1","Talk about conditions and consequences.","Jutäta ukhaxa, sarä."),
    _g("b1-relative","Relative clauses","B1","Identify people and things with relative clauses.","Nayax uñjkta uka jaqi."),
    _g("b1-causality","Cause, purpose and result","B1","Explain causes, purposes and results.","Yatiqañatakiw jutäta."),
    _g("b1-converbs","Converb and clause chaining","B1","Link sequential actions naturally.","Manq'asaw sarä."),
    _g("b1-reported","Reported speech","B1","Report what another person said.","Jupax jutaniwa sasaw säna."),
    _g("b1-commands","Indirect requests and advice","B1","Give advice and indirect instructions.","Uñjañamawa."),
    _g("b2-evidentiality","Evidentiality and information source","B2","Mark information source and speaker stance.","Ukax yatitäwa."),
    _g("b2-focus","Topic and focus","B2","Highlight important information in discourse.","Nayax uk yatiyta."),
    _g("b2-passive","Passive and affected constructions","B2","Describe events without foregrounding the agent.","Utax luratawa."),
    _g("b2-concession","Concession and contrast","B2","Express contrast and concession.","Ukhamäkchisa, sarä."),
    _g("b2-discourse","Discourse connectors","B2","Build coherent spoken and written discourse.","Ukampis nayax sarä."),
    _g("b2-nominalization","Nominalization","B2","Turn actions and qualities into discourse nouns.","Yatiqañax wakiskiriwa."),
    _g("b2-complex","Complex clause combinations","B2","Combine several subordinate relationships.","Kunapachatix jutki ukhaxa, aruskipä."),
    _g("c1-formal","Formal and institutional Aymara","C1","Use appropriate formal and administrative language.","Markan kamachinakapa yäqañawa."),
    _g("c1-academic","Academic register and hedging","C1","Present claims carefully in academic contexts.","Aka yatxatawix mä amuyuwa."),
    _g("c1-argumentation","Argumentation and evidence","C1","Develop claims, reasons and evidence.","Aka amuyux pä tuqitwa ch'amanchasi."),
    _g("c1-embedded","Embedded questions and propositions","C1","Embed questions and propositions in complex sentences.","Kunjamatsa lurasi uk yatitawa."),
    _g("c1-media","Media and public language","C1","Understand formal public and media discourse.","Yatiyawinakax markaru puriwayi."),
    _g("c1-pragmatics","Pragmatics and politeness","C1","Adjust meaning to relationship and context.","Mirä, yanapt'apxita."),
    _g("c1-rhetoric","Rhetorical structure","C1","Use emphasis, contrast and persuasive structure.","Ukhamarakiw amuyt'asiñasa."),
    _g("c2-literary","Literary and idiomatic Aymara","C2","Interpret figurative and idiomatic language.","Jach'a chuymaw markapar uñji."),
    _g("c2-translation","Translation and lexical precision","C2","Choose precise equivalents across contexts.","Arunakan amuyupa mayjt'ayaspawa."),
    _g("c2-discourse-analysis","Discourse analysis and register shifting","C2","Analyse register, stance and discourse structure.","Arunakax pachaparjamaw mayjt'ayi."),
    _g("c2-rhetorical-nuance","Advanced rhetorical nuance","C2","Handle subtle stance, implication and literary effect.","Amuyt'awix jach'a qhananchäwiwa."),
]

_vocab_data = [
("greetings","A1",[("kamisaraki","hello","Kamisaraki!"),("yuspajara","thank you","Yuspajara yanapt'awitata.")]),
("identity","A1",[("suti","name","Kunas sutimaxa?"),("naya","I","Nayax Ana satawa.")]),
("family","A1",[("tayka","mother","Taykajax utankiwa."),("awki","father","Awkijax irnaqaski.")]),
("home","A1",[("uta","house","Akax utaawa."),("manqha","inside","Uta manqhanwa jikxatasta.")]),
("study","A1",[("yatiqaña","to learn","Aymar aru yatiqaskta."),("yatichiri","teacher","Yatichirix yatichaski.")]),
("food","A1",[("manq'a","food","Manq'a munta."),("uma","water","Umaña munta.")]),
("market","A1",[("qhathu","market","Qhatun alasta."),("qullqi","money","Qullqix utjitu.")]),
("places","A1",[("marka","town","Markan jakasta."),("uta","home","Utaru sarä.")]),
("daily-routine","A2",[("irnaqaña","to work","Jichhürux irnaqta."),("saraña","to go","Markaru sarä.")]),
("travel","A2",[("thakhi","road","Thakhin sarä."),("qala","stone","Thakhin qala utji.")]),
("time","A2",[("jichha","now","Jichhax yatiqaskta."),("qharüru","tomorrow","Qharüru sarä.")]),
("health","A2",[("usuta","ill","Usutawa."),("qullaña","to heal/treat","Qullañ munta.")]),
("community","B1",[("ayllu","community","Ayllun irnaqapxta."),("marka","community/town","Markax jilaski.")]),
("nature","B1",[("uma","water","Umax wali wakiskiriwa."),("uraqi","land","Uraqix jiwasankiwa.")]),
("work","B1",[("irnaqawi","work","Irnaqawix wakiskiriwa."),("kamachi","rule","Kamachinak yäqañawa.")]),
("communication","B2",[("aruskipaña","to converse","Jichhax aruskipt'añani."),("yatiyawi","information","Yatiyawinakax puriwayi.")]),
("education","C1",[("yatxatawi","research","Aka yatxatawix ch'amanchatawa."),("amuyt'aña","to reflect","Amuyt'añax wakiskiriwa.")]),
("culture","C2",[("sarnaqawi","culture/custom","Sarnaqawix wali ch'amawa."),("aru","language","Arux markan jakañapawa.")]),
]

VOCABULARY_SETS = [
    VocabularySet(id=f"ay-{i+1}-{level.lower()}",level=level,topic=topic,unit_ref=f"ay-{level.lower()}-unit-{(i%8)+1}",
        words=[VocabularyEntry(word=w,pos="verb" if d.startswith("to ") else "noun",definition=d,example=e) for w,d,e in words])
    for i,(topic,level,words) in enumerate(_vocab_data)
]

_phrase_data = [
("Greetings","👋",[("Kamisaraki!","greeting"),("Kunjamasktsa?","asking how someone is")]),
("Introductions","👤",[("Nayax Ana satawa.","introducing yourself"),("Kunas sutimaxa?","asking a name")]),
("Courtesy","🙏",[("Yuspajara.","thanks"),("Mirä.","polite request marker")]),
("Home","🏠",[("Kawkhansa utaxa?","asking location"),("Uta manqhanwa jikxatasta.","describing location")]),
("Study","📚",[("Aymar aru yatiqaskta.","talking about learning"),("Yanapt'ita, mirä.","asking for help")]),
("Shopping","🛒",[("Qhawqhas chanipaxa?","asking price"),("Qhatun alasta.","shopping at a market")]),
("Directions","🧭",[("Kawkirus sarä?","asking where to go"),("Utaru sarä.","saying destination")]),
("Daily life","☀️",[("Jichhax irnaqaskta.","talking about today"),("Qharüru sarä.","talking about tomorrow")]),
("Formal public","🏛️",[("Kamachinak yäqañawa.","formal obligation"),("Yatiyawinakax puriwayi.","public information")]),
("Discussion","💬",[("Nayax uk yatiyta.","stating a position"),("Ukampis nayax sarä.","contrasting a point")]),
]
PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id=f"ay-phrase-{i+1}",level=("A1" if i<5 else "A2" if i<8 else "B2" if i==9 else "C1"),
        situation=situation,icon=icon,
        phrases=[PhrasebookEntry(text=text,context=context,register="neutral" if i<8 else "formal") for text,context in phrases])
    for i,(situation,icon,phrases) in enumerate(_phrase_data)
]

CURRICULUM = {}
_titles = {
    "A1":["Greetings and identity","Personal information","Family and home","Study and learning","Food and shopping","Places and directions","Daily routine","Communication"],
    "A2":["Past experiences","Future plans","Movement and places","Descriptions and comparison","Requests and instructions","Ability and necessity","Review and conversation","A2 consolidation"],
    "B1":["Aspect and events","Complex sentences","Conditions","Descriptions with relatives","Cause and purpose","Connected actions","Reported speech","Advice and indirect requests"],
    "B2":["Information source","Focus and emphasis","Affected and passive events","Contrast and concession","Coherent discourse","Nominalized language","Complex subordination","B2 consolidation"],
    "C1":["Formal institutions","Academic language","Argumentation","Embedded propositions","Media and public language","Pragmatics and politeness","Rhetorical structure","C1 consolidation"],
    "C2":["Literary language","Translation precision","Discourse analysis","Advanced rhetoric","Register shifting","Idiomatic nuance","Critical interpretation","C2 synthesis"],
}
_topic_by_level = {level:[g.title for g in GRAMMAR_TOPICS if g.level==level] for level in LEVELS}
for level in LEVELS:
    CURRICULUM[level] = []
    for n,title in enumerate(_titles[level],1):
        topic = _topic_by_level[level][n-1]
        vocab_id = f"ay-{n if level=='A1' else (9 if level=='A2' else 1)}-{level.lower()}"
        matching = [v.id for v in VOCABULARY_SETS if v.level==level]
        if not matching:
            matching = [VOCABULARY_SETS[(n-1)%len(VOCABULARY_SETS)].id]
        else:
            vocab_id = matching[(n-1)%len(matching)]
        CURRICULUM[level].append(CurriculumUnit(
            id=f"ay-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,
            grammar_points=[topic],vocabulary_set_ids=[vocab_id],
            lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],
            competency_checklist=[f"Use Aymara for {title.lower()} at {level} level."],default_weeks=2 if level in ("A1","A2") else 3))

ASSESSMENT_BANK = [
    AssessmentQuestion(id=f"ay-{i+1:03d}",skill=skill,difficulty=level,question=q,options=options,correct=correct)
    for i,(skill,level,q,options,correct) in enumerate([
        ("vocabulary","A1","Which phrase is a greeting?",["Kamisaraki!","Qharüru sarä.","Uta manqhanwa.","Kamachinak yäqañawa."],"Kamisaraki!"),
        ("grammar","A1","Which phrase asks for a name?",["Kunas sutimaxa?","Yuspajara.","Janiw yatkti.","Utaru sarä."],"Kunas sutimaxa?"),
        ("communication","A1","Which phrase politely asks for help?",["Yanapt'ita, mirä.","Jichhax irnaqta.","Qhatun alasta.","Nayax Ana satawa."],"Yanapt'ita, mirä."),
        ("vocabulary","A2","Which word means tomorrow?",["qharüru","jichha","uma","marka"],"qharüru"),
        ("grammar","A2","Which sentence expresses a destination?",["Utaru sarä.","Janiw yatkti.","Kamisaraki!","Nayax Ana satawa."],"Utaru sarä."),
        ("grammar","B1","Which sentence reports another person's statement?",["Jupax jutaniwa sasaw säna.","Kamisaraki!","Umaña munta.","Qhatun alasta."],"Jupax jutaniwa sasaw säna."),
        ("grammar","B1","Which construction introduces a condition?",["Jutäta ukhaxa, sarä.","Yuspajara.","Nayax Ana satawa.","Akax utaawa."],"Jutäta ukhaxa, sarä."),
        ("grammar","B2","Which phrase marks contrast?",["Ukampis nayax sarä.","Kamisaraki!","Umaña munta.","Kawkhansa utaxa?"],"Ukampis nayax sarä."),
        ("communication","B2","Which phrase presents a position?",["Nayax uk yatiyta.","Yuspajara.","Utaru sarä.","Qhatun alasta."],"Nayax uk yatiyta."),
        ("register","C1","Which phrase is appropriate for formal obligation?",["Kamachinak yäqañawa.","Kamisaraki!","Umaña munta.","Taykajax utankiwa."],"Kamachinak yäqañawa."),
        ("academic","C1","Which phrase introduces a research claim?",["Aka yatxatawix mä amuyuwa.","Kunjamasktsa?","Qhatun alasta.","Yuspajara."],"Aka yatxatawix mä amuyuwa."),
        ("translation","C2","Which statement emphasizes contextual lexical precision?",["Arunakan amuyupa mayjt'ayaspawa.","Kamisaraki!","Qharüru sarä.","Umaña munta."],"Arunakan amuyupa mayjt'ayaspawa."),
    ])
]

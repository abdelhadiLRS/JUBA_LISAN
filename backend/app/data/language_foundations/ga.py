"""Gaeilge (Irish) foundation data for JUBA LISAN — CEFR A1-C2."""
from app.data._types import (
    CurriculumUnit,
    GrammarExample,
    GrammarTopic,
    VocabularyEntry,
    VocabularySet,
    PhrasebookCategory,
    PhrasebookEntry,
    AssessmentQuestion,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

GRAMMAR_TOPICS = [
    GrammarTopic(slug="ga-a1-word-order", title="Basic Irish word order", level="A1", category="syntax", summary="Build simple verb-first clauses.", explanation="Irish normally places the finite verb before the subject in independent declarative clauses.", examples=[GrammarExample(text="Tá mé anseo."), GrammarExample(text="Léann sí an leabhar.")]),
    GrammarTopic(slug="ga-a1-copula", title="Copula: is", level="A1", category="grammar", summary="Identify people, occupations and categories.", explanation="Use is to link a noun phrase with an identity or category.", examples=[GrammarExample(text="Is mac léinn mé."), GrammarExample(text="Is múinteoir í.")]),
    GrammarTopic(slug="ga-a1-present", title="Present tense", level="A1", category="verbs", summary="Describe current and habitual actions.", explanation="Use the present-tense verb forms for actions and routines.", examples=[GrammarExample(text="Oibrím i mBaile Átha Cliath."), GrammarExample(text="Léann sé gach lá.")]),
    GrammarTopic(slug="ga-a1-prepositions", title="Prepositions and location", level="A1", category="grammar", summary="Express basic location and direction.", explanation="Use common prepositions such as i, ag, ar and le; learn their initial mutations.", examples=[GrammarExample(text="Tá sí sa teach."), GrammarExample(text="Tá an leabhar ar an mbord.")]),
    GrammarTopic(slug="ga-a1-possessives", title="Possessive adjectives", level="A1", category="grammar", summary="Express possession.", explanation="Use mo, do and a before nouns, observing their effects on initial consonants.", examples=[GrammarExample(text="Seo mo leabhar."), GrammarExample(text="Cá bhfuil do mhála?")]),
    GrammarTopic(slug="ga-a1-questions", title="Questions and negation", level="A1", category="syntax", summary="Ask and negate simple statements.", explanation="Use question particles such as an and interrogative words such as cá, cén and cad; use ní for present-tense negation.", examples=[GrammarExample(text="Cá bhfuil tú?"), GrammarExample(text="Nílim tuirseach.")]),
    GrammarTopic(slug="ga-a2-past", title="Past tense and lenition", level="A2", category="verbs", summary="Talk about completed events.", explanation="The past tense commonly uses initial lenition after the past-tense marker and has distinct affirmative and negative patterns.", examples=[GrammarExample(text="Chuaigh mé abhaile."), GrammarExample(text="Ní dheachaigh mé inné.")]),
    GrammarTopic(slug="ga-a2-future", title="Future tense", level="A2", category="verbs", summary="Talk about plans and future events.", explanation="Use the future tense for expected events, intentions and scheduled actions.", examples=[GrammarExample(text="Rachaidh mé amárach."), GrammarExample(text="Déanfaidh sí é níos déanaí.")]),
    GrammarTopic(slug="ga-a2-prepositional-pronouns", title="Prepositional pronouns", level="A2", category="grammar", summary="Combine prepositions with pronouns.", explanation="Irish combines many prepositions with personal pronouns, producing forms such as liom, leat, aige and aici.", examples=[GrammarExample(text="Tar liom."), GrammarExample(text="Tá an leabhar aige.")]),
    GrammarTopic(slug="ga-a2-comparatives", title="Comparatives and superlatives", level="A2", category="adjectives", summary="Compare people and things.", explanation="Use the comparative form and related structures to express difference and degree.", examples=[GrammarExample(text="Tá an carr seo níos saoire."), GrammarExample(text="Is é seo an ceann is fearr.")]),
    GrammarTopic(slug="ga-a2-relative", title="Basic relative clauses", level="A2", category="syntax", summary="Connect information about a noun.", explanation="Use relative structures with a relative particle to give additional information.", examples=[GrammarExample(text="An fear atá ina chónaí anseo."), GrammarExample(text="An leabhar a léigh mé.")]),
    GrammarTopic(slug="ga-b1-verbal-noun", title="The verbal noun", level="B1", category="verbs", summary="Describe ongoing activity and purpose.", explanation="The verbal noun is central to Irish constructions for ongoing actions, obligation and purpose.", examples=[GrammarExample(text="Tá mé ag foghlaim Gaeilge."), GrammarExample(text="Chuaigh sí ag obair.")]),
    GrammarTopic(slug="ga-b1-conditionals", title="Conditional and hypothetical clauses", level="B1", category="syntax", summary="Express conditions, possibilities and hypotheticals.", explanation="Use dá and conditional verb forms to discuss hypothetical or dependent situations.", examples=[GrammarExample(text="Dá mbeadh am agam, rachainn."), GrammarExample(text="Bheinn sásta dá dtiocfadh tú.")]),
    GrammarTopic(slug="ga-b1-relative-advanced", title="Relative clauses with prepositions", level="B1", category="syntax", summary="Handle more complex relative reference.", explanation="Use relative structures after prepositions and distinguish direct and indirect relative relationships.", examples=[GrammarExample(text="An duine a raibh mé ag caint leis."), GrammarExample(text="An áit ina bhfuil cónaí orm.")]),
    GrammarTopic(slug="ga-b1-mutations", title="Initial mutations", level="B1", category="morphology", summary="Control lenition and eclipsis in connected speech.", explanation="Mutation is grammatical rather than optional spelling decoration; learn when particles and possessives trigger lenition or eclipsis.", examples=[GrammarExample(text="mo chara"), GrammarExample(text="ár gcarr")]),
    GrammarTopic(slug="ga-b2-reported-speech", title="Reported speech", level="B2", category="syntax", summary="Report statements, questions and claims.", explanation="Combine quotation, tense and clause structures to report what another person said or believed.", examples=[GrammarExample(text="Dúirt sé go raibh sé gnóthach."), GrammarExample(text="D'fhiafraigh sí cá raibh mé.")]),
    GrammarTopic(slug="ga-b2-passive", title="Passive and impersonal constructions", level="B2", category="syntax", summary="Focus on events rather than an explicit agent.", explanation="Use passive and impersonal forms to foreground processes, especially in formal and informational language.", examples=[GrammarExample(text="Rinneadh an cinneadh inné."), GrammarExample(text="Foilsíodh an tuarascáil.")]),
    GrammarTopic(slug="ga-b2-subordination", title="Complex subordination", level="B2", category="syntax", summary="Build multi-clause arguments.", explanation="Use causal, concessive, temporal and conditional connectors to organize complex ideas.", examples=[GrammarExample(text="Cé go raibh sé déanach, leanamar ar aghaidh."), GrammarExample(text="Ó tharla go raibh sé ag cur báistí, d'fhanamar istigh.")]),
    GrammarTopic(slug="ga-b2-register", title="Formal and professional register", level="B2", category="style", summary="Adapt Irish to professional contexts.", explanation="Choose precise vocabulary, impersonal constructions and cohesive connectors for reports, correspondence and workplace communication.", examples=[GrammarExample(text="De réir na tuarascála, tá gá le tuilleadh taighde."), GrammarExample(text="Ba cheart dúinn an cheist a mheas go cúramach.")]),
    GrammarTopic(slug="ga-c1-nominalisation", title="Nominalisation and formal style", level="C1", category="style", summary="Express complex information in formal prose.", explanation="Use abstract nouns, participial structures and compact clause packaging while preserving natural Irish syntax.", examples=[GrammarExample(text="Tá méadú suntasach tagtha ar an éileamh."), GrammarExample(text="Is léir an gá atá le hathrú córasach.")]),
    GrammarTopic(slug="ga-c1-discourse", title="Discourse organization and hedging", level="C1", category="pragmatics", summary="Qualify claims and structure arguments.", explanation="Use cohesive markers and cautious formulations to distinguish evidence, interpretation and certainty.", examples=[GrammarExample(text="Is cosúil go bhfuil an scéal níos casta ná mar a cheapamar."), GrammarExample(text="D'fhéadfaí a mhaíomh go bhfuil rogha eile ann.")]),
    GrammarTopic(slug="ga-c1-idiom", title="Idiomatic and pragmatic nuance", level="C1", category="pragmatics", summary="Interpret implied meaning and idiomatic usage.", explanation="Develop sensitivity to fixed expressions, understatement, politeness and context-dependent choices.", examples=[GrammarExample(text="Ní hé sin le rá nach bhfuil fadhbanna ann."), GrammarExample(text="Tá sé thar am againn beart a dhéanamh.")]),
    GrammarTopic(slug="ga-c2-advanced-syntax", title="Advanced syntax and stylistic control", level="C2", category="syntax", summary="Control complex structures with precision.", explanation="Combine embedding, emphasis, relative structures and information packaging without losing idiomatic flow.", examples=[GrammarExample(text="Is é an rud is tábhachtaí ná go dtuigfimis na cúiseanna atá taobh thiar den athrú."), GrammarExample(text="Cé nach féidir an toradh a thuar go cruinn, is féidir na rioscaí a mheas.")]),
    GrammarTopic(slug="ga-c2-literary-register", title="Literary and rhetorical register", level="C2", category="style", summary="Recognise and produce sophisticated written Irish.", explanation="Use rhetorical contrast, lexical precision and register shifts appropriate to essays, cultural commentary and formal public communication.", examples=[GrammarExample(text="Ní hamháin gur athraigh an tionscadal an córas, ach d'athraigh sé an dearcadh ina leith freisin."), GrammarExample(text="Ar an ábhar sin, is fiú féachaint níos faide ná na huimhreacha féin.")]),
]

def _unit(level, number, title, grammar, vocab, weeks=2):
    return CurriculumUnit(
        id=f"ga-{level.lower()}-unit-{number}",
        level=level,
        unit_number=number,
        title=title,
        grammar_points=grammar,
        vocabulary_set_ids=[vocab],
        lesson_types=["grammar", "vocabulary", "listening", "speaking", "reading", "writing", "review"],
        competency_checklist=[f"Use {title.lower()} vocabulary", f"Apply {grammar[0]} in connected Irish"],
        default_weeks=weeks,
    )

CURRICULUM = {
    "A1": [
        _unit("A1", 1, "Beannachtaí agus aithne", ["ga-a1-word-order"], "ga_a1_greetings"),
        _unit("A1", 2, "Féiniúlacht agus teaghlach", ["ga-a1-copula"], "ga_a1_identity"),
        _unit("A1", 3, "Gnáthamh agus am", ["ga-a1-present"], "ga_a1_routine"),
        _unit("A1", 4, "Baile agus áiteanna", ["ga-a1-prepositions"], "ga_a1_places"),
        _unit("A1", 5, "Seilbh agus rudaí", ["ga-a1-possessives"], "ga_a1_possession"),
        _unit("A1", 6, "Ceisteanna agus riachtanais", ["ga-a1-questions"], "ga_a1_needs"),
    ],
    "A2": [
        _unit("A2", 1, "Inné agus an deireadh seachtaine", ["ga-a2-past"], "ga_a2_past"),
        _unit("A2", 2, "Pleananna agus an todhchaí", ["ga-a2-future"], "ga_a2_future"),
        _unit("A2", 3, "Daoine agus caidrimh", ["ga-a2-prepositional-pronouns"], "ga_a2_people"),
        _unit("A2", 4, "Comparáid agus rogha", ["ga-a2-comparatives"], "ga_a2_comparison"),
        _unit("A2", 5, "Áiteanna agus eispéiris", ["ga-a2-relative"], "ga_a2_experience"),
        _unit("A2", 6, "Athbhreithniú cumarsáide", ["ga-a2-past", "ga-a2-future"], "ga_a2_review"),
    ],
    "B1": [
        _unit("B1", 1, "Gníomhaíochtaí agus spriocanna", ["ga-b1-verbal-noun"], "ga_b1_activities"),
        _unit("B1", 2, "Féidearthacht agus coinníollacha", ["ga-b1-conditionals"], "ga_b1_conditions"),
        _unit("B1", 3, "Scéalta agus cur síos", ["ga-b1-relative-advanced"], "ga_b1_narrative"),
        _unit("B1", 4, "Litriú agus athruithe tosaigh", ["ga-b1-mutations"], "ga_b1_language"),
        _unit("B1", 5, "Obair agus staidéar", ["ga-b1-verbal-noun"], "ga_b1_work"),
        _unit("B1", 6, "Tuairimí agus plé", ["ga-b1-conditionals", "ga-b1-relative-advanced"], "ga_b1_discussion"),
    ],
    "B2": [
        _unit("B2", 1, "Tuairisciú agus tuairimí", ["ga-b2-reported-speech"], "ga_b2_reporting"),
        _unit("B2", 2, "Nuacht agus faisnéis", ["ga-b2-passive"], "ga_b2_media"),
        _unit("B2", 3, "Argóint agus cúisíocht", ["ga-b2-subordination"], "ga_b2_argument"),
        _unit("B2", 4, "Obair agus cumarsáid fhoirmiúil", ["ga-b2-register"], "ga_b2_professional"),
        _unit("B2", 5, "Sochaí agus seirbhísí", ["ga-b2-subordination"], "ga_b2_society"),
        _unit("B2", 6, "Athbhreithniú ardleibhéil", ["ga-b2-reported-speech", "ga-b2-passive"], "ga_b2_review"),
    ],
    "C1": [
        _unit("C1", 1, "Scríbhneoireacht fhoirmiúil", ["ga-c1-nominalisation"], "ga_c1_formal"),
        _unit("C1", 2, "Argóint agus fianaise", ["ga-c1-discourse"], "ga_c1_argument"),
        _unit("C1", 3, "Stíl agus impleacht", ["ga-c1-idiom"], "ga_c1_pragmatics"),
        _unit("C1", 4, "Cultúr agus féiniúlacht", ["ga-c1-discourse"], "ga_c1_culture"),
        _unit("C1", 5, "Taighde agus an saol poiblí", ["ga-c1-nominalisation"], "ga_c1_public"),
        _unit("C1", 6, "Athbhreithniú C1", ["ga-c1-nominalisation", "ga-c1-discourse"], "ga_c1_review"),
    ],
    "C2": [
        _unit("C2", 1, "Comhréir chasta", ["ga-c2-advanced-syntax"], "ga_c2_syntax"),
        _unit("C2", 2, "Reitric agus stíl", ["ga-c2-literary-register"], "ga_c2_rhetoric"),
        _unit("C2", 3, "Anailís chriticiúil", ["ga-c1-discourse"], "ga_c2_analysis"),
        _unit("C2", 4, "Idirghníomhaíocht agus nuance", ["ga-c1-idiom"], "ga_c2_nuance"),
        _unit("C2", 5, "Scríbhneoireacht ghairmiúil agus acadúil", ["ga-c2-advanced-syntax"], "ga_c2_academic"),
        _unit("C2", 6, "Máistreacht sa Ghaeilge", ["ga-c2-advanced-syntax", "ga-c2-literary-register"], "ga_c2_mastery"),
    ],
}

def _vset(id_, level, topic, unit_ref, words):
    return VocabularySet(
        id=id_, level=level, topic=topic, unit_ref=unit_ref,
        words=[VocabularyEntry(word=w, pos=p, definition=d, example=e) for w, p, d, e in words],
    )

VOCABULARY_SETS = [
    _vset("ga_a1_greetings", "A1", "Beannachtaí", "ga-a1-unit-1", [
        ("Dia duit","phrase","hello","Dia duit, a Mháire."), ("slán","phrase","goodbye","Slán go fóill."), ("maidin","noun","morning","Maidin mhaith."), ("le do thoil","phrase","please","Uisce, le do thoil."), ("go raibh maith agat","phrase","thank you","Go raibh maith agat."), ("fáilte","noun","welcome","Fáilte romhat."),
    ]),
    _vset("ga_a1_identity", "A1", "Féiniúlacht", "ga-a1-unit-2", [
        ("ainm","noun","name","Cén t-ainm atá ort?"), ("duine","noun","person","Is duine cineálta é."), ("mac léinn","noun","student","Is mac léinn mé."), ("múinteoir","noun","teacher","Is múinteoir í."), ("cara","noun","friend","Seo mo chara."), ("teaghlach","noun","family","Tá teaghlach mór agam."),
    ]),
    _vset("ga_a1_routine", "A1", "Gnáthamh", "ga-a1-unit-3", [
        ("éirigh","verb","get up","Éirím ar a seacht."), ("obair","noun","work","Téim chun oibre."), ("scoil","noun","school","Téann sí ar scoil."), ("ithe","verb","eat","Ithim bricfeasta."), ("codladh","noun","sleep","Teastaíonn codladh uaim."), ("inniu","adverb","today","Tá mé gnóthach inniu."),
    ]),
    _vset("ga_a1_places", "A1", "Baile agus áiteanna", "ga-a1-unit-4", [
        ("teach","noun","house","Tá mé sa teach."), ("seomra","noun","room","Tá an seomra mór."), ("siopa","noun","shop","Tá an siopa anseo."), ("cathair","noun","city","Tá cónaí orm sa chathair."), ("sráid","noun","street","Tá an siopa ar an tsráid."), ("stáisiún","noun","station","Cá bhfuil an stáisiún?"),
    ]),
    _vset("ga_a1_possession", "A1", "Seilbh", "ga-a1-unit-5", [
        ("mo","determiner","my","Seo mo mhála."), ("do","determiner","your","Cá bhfuil do leabhar?"), ("mála","noun","bag","Tá mo mhála anseo."), ("leabhar","noun","book","Tá mo leabhar ar an mbord."), ("fón","noun","phone","Cá bhfuil mo fhón?"), ("eochair","noun","key","Tá an eochair agam."),
    ]),
    _vset("ga_a1_needs", "A1", "Ceisteanna agus riachtanais", "ga-a1-unit-6", [
        ("cá","adverb","where","Cá bhfuil tú?"), ("cad","pronoun","what","Cad é seo?"), ("cén","determiner","which/what","Cén t-am é?"), ("cabhair","noun","help","Teastaíonn cabhair uaim."), ("leithreas","noun","toilet","Cá bhfuil an leithreas?"), ("uisce","noun","water","Ba mhaith liom uisce."),
    ]),
    _vset("ga_a2_past", "A2", "An t-am atá thart", "ga-a2-unit-1", [
        ("inné","adverb","yesterday","Chuaigh mé ann inné."), ("an deireadh seachtaine","noun phrase","the weekend","Bhí mé gnóthach ag an deireadh seachtaine."), ("chuaigh","verb","went","Chuaigh sí abhaile."), ("rinne","verb","did/made","Rinne mé an obair."), ("chonaic","verb","saw","Chonaic mé an scannán."), ("tháinig","verb","came","Tháinig sé aréir."),
    ]),
    _vset("ga_a2_future", "A2", "An todhchaí", "ga-a2-unit-2", [
        ("amárach","adverb","tomorrow","Feicfidh mé thú amárach."), ("rachaidh","verb","will go","Rachaidh mé ar maidin."), ("déanfaidh","verb","will do","Déanfaidh sí é."), ("feicfidh","verb","will see","Feicfidh muid thú."), ("plean","noun","plan","Tá plean maith againn."), ("níos déanaí","adverb","later","Glaofaidh mé ort níos déanaí."),
    ]),
    _vset("ga_a2_people", "A2", "Daoine agus caidrimh", "ga-a2-unit-3", [
        ("liom","prepositional pronoun","with me","Tar liom."), ("leat","prepositional pronoun","with you","Ba mhaith liom labhairt leat."), ("aige","prepositional pronoun","at/having him","Tá an ticéad aige."), ("aici","prepositional pronoun","at/having her","Tá an eochair aici."), ("caidreamh","noun","relationship","Tá caidreamh maith acu."), ("comharsa","noun","neighbour","Is comharsa maith é."),
    ]),
    _vset("ga_a2_comparison", "A2", "Comparáid", "ga-a2-unit-4", [
        ("níos fearr","adjective phrase","better","Tá an ceann seo níos fearr."), ("níos mó","adjective phrase","more/bigger","Tá níos mó ama agam."), ("níos lú","adjective phrase","less/smaller","Tá an seomra níos lú."), ("is fearr","superlative","best","Is é seo an ceann is fearr."), ("saor","adjective","cheap","Tá an ticéad saor."), ("daor","adjective","expensive","Tá an t-óstán daor."),
    ]),
    _vset("ga_a2_experience", "A2", "Eispéiris", "ga-a2-unit-5", [
        ("taithí","noun","experience","Tá taithí agam air."), ("turas","noun","trip","Bhí turas deas againn."), ("áit","noun","place","Is áit álainn í."), ("aithne","noun","acquaintance","Tá aithne agam air."), ("cuairt","noun","visit","Thugamar cuairt ar an músaem."), ("suimiúil","adjective","interesting","Bhí an scéal suimiúil."),
    ]),
    _vset("ga_a2_review", "A2", "Cumarsáid A2", "ga-a2-unit-6", [
        ("ceist","noun","question","Tá ceist agam."), ("freagra","noun","answer","Seo an freagra."), ("míniú","noun","explanation","Teastaíonn míniú uaim."), ("cuimhneamh","verb","remember","Déan iarracht cuimhneamh air."), ("dearmad","noun","forgetting","Rinne mé dearmad."), ("sásta","adjective","happy/satisfied","Tá mé sásta."),
    ]),
    _vset("ga_b1_activities", "B1", "Gníomhaíochtaí", "ga-b1-unit-1", [
        ("foghlaim","verb","learn","Tá mé ag foghlaim Gaeilge."), ("forbairt","noun","development","Tá forbairt á déanamh againn."), ("sprioc","noun","goal","Tá sprioc shoiléir agam."), ("cleachtadh","noun","practice","Teastaíonn cleachtadh rialta."), ("iarracht","noun","effort","Rinne sí iarracht."), ("dul chun cinn","noun phrase","progress","Tá dul chun cinn maith déanta agam."),
    ]),
    _vset("ga_b1_conditions", "B1", "Coinníollacha", "ga-b1-unit-2", [
        ("dá","conjunction","if (hypothetical)","Dá mbeadh am agam, rachainn."), ("mbeadh","verb","would be/had","Dá mbeadh airgead agam..."), ("rachainn","verb","I would go","Rachainn leat."), ("féidearthacht","noun","possibility","Tá féidearthacht ann."), ("seans","noun","chance","Tá seans maith ann."), ("murach","preposition/conjunction","were it not for","Murach an chabhair, bheadh sé deacair."),
    ]),
    _vset("ga_b1_narrative", "B1", "Scéal agus cur síos", "ga-b1-unit-3", [
        ("scéal","noun","story","Is scéal suimiúil é."), ("eachtra","noun","event/adventure","Is cuimhin liom an eachtra."), ("cuimhne","noun","memory","Tá cuimhne mhaith aici."), ("timpeall","adverb","around","Shiúil muid timpeall na cathrach."), ("cúis","noun","reason","Mínigh an chúis."), ("toradh","noun","result","Ba mhaith linn an toradh a thuiscint."),
    ]),
    _vset("ga_b1_language", "B1", "An Ghaeilge féin", "ga-b1-unit-4", [
        ("séimhiú","noun","lenition","Tá séimhiú sa fhocal seo."), ("urú","noun","eclipsis","Tá urú i ndiaidh an réamhfhocail."), ("ainmfhocal","noun","noun","Is ainmfhocal é."), ("briathar","noun","verb","Is briathar é."), ("aidiacht","noun","adjective","Is aidiacht í."), ("réamhfhocal","noun","preposition","Is réamhfhocal é le."),
    ]),
    _vset("ga_b1_work", "B1", "Obair agus staidéar", "ga-b1-unit-5", [
        ("post","noun","job","Tá post nua agam."), ("cruinniú","noun","meeting","Tá cruinniú againn."), ("tionscadal","noun","project","Tá an tionscadal ar siúl."), ("taighde","noun","research","Tá taighde ar siúl."), ("scil","noun","skill","Is scil úsáideach í."), ("freagracht","noun","responsibility","Tá freagracht mhór air."),
    ]),
    _vset("ga_b1_discussion", "B1", "Plé agus tuairim", "ga-b1-unit-6", [
        ("tuairim","noun","opinion","Is é mo thuairim..."), ("aontaigh","verb","agree","Aontaím leat."), ("easaontaigh","verb","disagree","Ní aontaím leis sin."), ("argóint","noun","argument","Tá argóint láidir aige."), ("sampla","noun","example","Seo sampla maith."), ("dearcadh","noun","viewpoint","Tá dearcadh eile ann."),
    ]),
    _vset("ga_b2_reporting", "B2", "Tuairisciú", "ga-b2-unit-1", [
        ("dúirt","verb","said","Dúirt sé go raibh sé gnóthach."), ("d'fhiafraigh","verb","asked","D'fhiafraigh sí cá raibh mé."), ("éileamh","noun","claim/demand","Rinne sé éileamh láidir."), ("maíomh","noun","assertion","Is deacair an maíomh a chruthú."), ("foinse","noun","source","Seiceáil an fhoinse."), ("tuarascáil","noun","report","Léigh mé an tuarascáil."),
    ]),
    _vset("ga_b2_media", "B2", "Nuacht agus faisnéis", "ga-b2-unit-2", [
        ("nuacht","noun","news","Chuala mé an nuacht."), ("foilsigh","verb","publish","Foilsíodh an tuarascáil."), ("alt","noun","article","Léigh mé an t-alt."), ("ceannlíne","noun","headline","Bhí an cheannlíne soiléir."), ("imeacht","noun","event","Clúdaíonn an nuacht an t-imeacht."), ("eolas","noun","information","Tá tuilleadh eolais uainn."),
    ]),
    _vset("ga_b2_argument", "B2", "Argóint agus cúisíocht", "ga-b2-unit-3", [
        ("cé go","conjunction","although","Cé go raibh sé déanach, leanamar ar aghaidh."), ("mar gheall ar","prepositional phrase","because of","Mar gheall ar an aimsir, d'fhanamar istigh."), ("céim","noun","step/stage","Is céim thábhachtach í."), ("fianaise","noun","evidence","Níl go leor fianaise ann."), ("tionchar","noun","impact","Bhí tionchar mór aige."), ("iarmhairt","noun","consequence","Caithfimid na hiarmhairtí a mheas."),
    ]),
    _vset("ga_b2_professional", "B2", "Gairmiúil", "ga-b2-unit-4", [
        ("de réir","prepositional phrase","according to","De réir na tuarascála..."), ("ba cheart","expression","should","Ba cheart dúinn tosú."), ("moladh","noun","recommendation","Seo moladh praiticiúil."), ("cinneadh","noun","decision","Rinneadh an cinneadh."), ("togra","noun","proposal","Tá togra nua againn."), ("beartas","noun","policy","Pléadh an beartas."),
    ]),
    _vset("ga_b2_society", "B2", "Sochaí", "ga-b2-unit-5", [
        ("pobal","noun","community","Tá an pobal páirteach."), ("sochaí","noun","society","Tá an tsochaí ag athrú."), ("seirbhís","noun","service","Tá an tseirbhís ar fáil."), ("oideachas","noun","education","Tá oideachas tábhachtach."), ("comhshaol","noun","environment","Ní mór an comhshaol a chosaint."), ("acmhainn","noun","resource","Is acmhainn luachmhar í."),
    ]),
    _vset("ga_b2_review", "B2", "Athbhreithniú B2", "ga-b2-unit-6", [
        ("casta","adjective","complex","Is ceist chasta í."), ("beacht","adjective","precise","Bí beacht sa chur síos."), ("comhsheasmhach","adjective","consistent","Caithfidh an argóint a bheith comhsheasmhach."), ("ábhartha","adjective","relevant","Tá an sampla ábhartha."), ("iontaofa","adjective","reliable","Is foinse iontaofa í."), ("neodrach","adjective","neutral","Bain úsáid as teanga neodrach."),
    ]),
    _vset("ga_c1_formal", "C1", "Foirmiúlacht", "ga-c1-unit-1", [
        ("méadú","noun","increase","Tá méadú suntasach tagtha ar an éileamh."), ("laghdú","noun","reduction","Tá laghdú tagtha ar na costais."), ("athrú","noun","change","Tá athrú córasach de dhíth."), ("riachtanas","noun","requirement","Is riachtanas é seo."), ("cur chuige","noun phrase","approach","Tá cur chuige nua molta."), ("prionsabal","noun","principle","Tá an prionsabal soiléir."),
    ]),
    _vset("ga_c1_argument", "C1", "Anailís agus fianaise", "ga-c1-unit-2", [
        ("is cosúil","expression","it seems","Is cosúil go bhfuil an scéal casta."), ("d'fhéadfaí","expression","one could","D'fhéadfaí a mhaíomh go bhfuil rogha eile ann."), ("bunaithe ar","phrase","based on","Tá an moladh bunaithe ar fhianaise."), ("measúnú","noun","assessment","Rinneadh measúnú neamhspleách."), ("léirmhíniú","noun","interpretation","Tá níos mó ná léirmhíniú amháin ann."), ("cruthúnas","noun","proof","Níl cruthúnas cinnte againn."),
    ]),
    _vset("ga_c1_pragmatics", "C1", "Nuance agus praiticiúlacht", "ga-c1-unit-3", [
        ("impleacht","noun","implication","Tá impleacht thábhachtach aige."), ("fo-théacs","noun","subtext","Tuig an fo-théacs."), ("béim","noun","emphasis","Leag sé béim ar an gceist."), ("dea-thoil","noun","goodwill","Léirigh sí dea-thoil."), ("béasach","adjective","polite","Tá an freagra béasach."), ("oiriúnach","adjective","appropriate","Tá an ton oiriúnach."),
    ]),
    _vset("ga_c1_culture", "C1", "Cultúr agus féiniúlacht", "ga-c1-unit-4", [
        ("oidhreacht","noun","heritage","Is cuid den oidhreacht í."), ("traidisiún","noun","tradition","Tá an traidisiún beo."), ("féiniúlacht","noun","identity","Pléadh féiniúlacht chultúrtha."), ("mionteanga","noun","minority language","Is mionteanga í i gcomhthéacs áirithe."), ("athbheochan","noun","revival","Tá athbheochan teanga ar siúl."), ("litríocht","noun","literature","Léann sí litríocht na Gaeilge."),
    ]),
    _vset("ga_c1_public", "C1", "Saol poiblí", "ga-c1-unit-5", [
        ("rialachas","noun","governance","Tá rialachas trédhearcach riachtanach."), ("rannpháirtíocht","noun","participation","Tá rannpháirtíocht an phobail tábhachtach."), ("cuntasacht","noun","accountability","Tá cuntasacht riachtanach."), ("trédhearcacht","noun","transparency","Teastaíonn trédhearcacht."), ("beart","noun","measure/action","Glacadh beart láithreach."), ("straitéis","noun","strategy","Tá straitéis fhadtéarmach de dhíth."),
    ]),
    _vset("ga_c1_review", "C1", "Athbhreithniú C1", "ga-c1-unit-6", [
        ("caolchúiseach","adjective","subtle","Is idirdhealú caolchúiseach é."), ("soiléir","adjective","clear","Tá an seasamh soiléir."), ("débhríoch","adjective","ambiguous","Tá an abairt débhríoch."), ("cuimsitheach","adjective","comprehensive","Is measúnú cuimsitheach é."), ("criticiúil","adjective","critical","Tá an léamh criticiúil."), ("neamhspleách","adjective","independent","Is measúnú neamhspleách é."),
    ]),
    _vset("ga_c2_syntax", "C2", "Comhréir chasta", "ga-c2-unit-1", [
        ("in ainneoin","phrase","despite","In ainneoin na ndeacrachtaí, leanamar ar aghaidh."), ("ar an ábhar sin","connector","for that reason","Ar an ábhar sin, is fiú leanúint."), ("a bhfuil","relative form","which/that has","An córas a bhfuilimid ag brath air."), ("is é an rud is tábhachtaí","phrase","the most important thing is","Is é an rud is tábhachtaí ná..."), ("ní hamháin","adverb","not only","Ní hamháin gur athraigh sé an córas..."), ("ach oiread","adverb","either/as well","Ní raibh sé sásta ach oiread."),
    ]),
    _vset("ga_c2_rhetoric", "C2", "Reitric agus stíl", "ga-c2-unit-2", [
        ("béim a leagan ar","phrase","emphasise","Leagadh béim ar an bpointe."), ("i bhfad ó","phrase","far from","Tá sé i bhfad ó bheith simplí."), ("gan dabht","adverb","without doubt","Gan dabht, is ceist chasta í."), ("ar an gcéad dul síos","connector","first of all","Ar an gcéad dul síos, caithfimid na sonraí a scrúdú."), ("ar deireadh thiar","connector","ultimately","Ar deireadh thiar, is cinneadh luachanna é."), ("os a choinne sin","connector","on the other hand","Os a choinne sin, tá buntáiste soiléir ann."),
    ]),
    _vset("ga_c2_analysis", "C2", "Anailís chriticiúil", "ga-c2-unit-3", [
        ("anailís","noun","analysis","Teastaíonn anailís mhionsonraithe."), ("toimhde","noun","assumption","Ní mór an toimhde a cheistiú."), ("frithargóint","noun","counterargument","Tá frithargóint láidir ann."), ("comhthéacs","noun","context","Ní mór an comhthéacs a chur san áireamh."), ("fairsinge","noun","scope","Tá fairsinge an staidéir teoranta."), ("iontaofacht","noun","reliability","Caithfear iontaofacht na sonraí a mheas."),
    ]),
    _vset("ga_c2_nuance", "C2", "Nuance", "ga-c2-unit-4", [
        ("leid","noun","clue","Tugann an focal seo leid dúinn."), ("ton","noun","tone","Athraíonn an ton de réir an chomhthéacs."), ("leathleid","noun","hint","Thug sé leathleid faoin bhfreagra."), ("searbhas","noun","sarcasm","Ní mór searbhas a aithint ón gcomhthéacs."), ("foirmiúlacht","noun","formality","Athraíonn an fhoirmiúlacht de réir an lucht éisteachta."), ("oiriúnú","noun","adaptation","Tá oiriúnú teanga riachtanach."),
    ]),
    _vset("ga_c2_academic", "C2", "Acadúil agus gairmiúil", "ga-c2-unit-5", [
        ("hipitéis","noun","hypothesis","Tá an hipitéis le tástáil."), ("modheolaíocht","noun","methodology","Mínítear an mhodheolaíocht."), ("comhghaol","noun","correlation","Ní ionann comhghaol agus cúisíocht."), ("athbhreithniú","noun","review","Foilsíodh athbhreithniú cuimsitheach."), ("tátal","noun","conclusion/inference","Is é seo an tátal is réasúnta."), ("teorainn","noun","limitation","Ba cheart an teorainn a admháil."),
    ]),
    _vset("ga_c2_mastery", "C2", "Máistreacht", "ga-c2-unit-6", [
        ("beachtas","noun","precision","Tá beachtas na teanga ríthábhachtach."), ("solúbthacht","noun","flexibility","Léiríonn sé solúbthacht stíle."), ("líofacht","noun","fluency","Tá líofacht ard aige."), ("saibhreas","noun","richness","Tá saibhreas foclóra aici."), ("idirdhealú","noun","distinction","Tá idirdhealú tábhachtach anseo."), ("máistreacht","noun","mastery","Léiríonn an téacs máistreacht teanga."),
    ]),
]

PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id="ga-a1-social", level="A1", situation="Comhrá sóisialta", icon="💬", phrases=[
        PhrasebookEntry(text="Dia duit!", context="greeting", register="neutral"),
        PhrasebookEntry(text="Conas atá tú?", context="wellbeing", register="neutral"),
        PhrasebookEntry(text="Tá mé go maith, go raibh maith agat.", context="reply", register="neutral"),
        PhrasebookEntry(text="Slán go fóill.", context="farewell", register="neutral"),
    ]),
    PhrasebookCategory(id="ga-a1-survival", level="A1", situation="Riachtanais laethúla", icon="🧭", phrases=[
        PhrasebookEntry(text="Cá bhfuil an leithreas?", context="location", register="neutral"),
        PhrasebookEntry(text="Cabhraigh liom, le do thoil.", context="help", register="neutral"),
        PhrasebookEntry(text="Ní thuigim.", context="comprehension", register="neutral"),
        PhrasebookEntry(text="An féidir leat é sin a rá arís?", context="clarification", register="neutral"),
    ]),
    PhrasebookCategory(id="ga-a2-shopping", level="A2", situation="Siopadóireacht", icon="🛍️", phrases=[
        PhrasebookEntry(text="Cé mhéad é?", context="price", register="neutral"),
        PhrasebookEntry(text="Ba mhaith liom é seo.", context="purchase", register="neutral"),
        PhrasebookEntry(text="An bhfuil ceann níos saoire agat?", context="comparison", register="neutral"),
        PhrasebookEntry(text="Tá sé sin ceart go leor.", context="agreement", register="neutral"),
    ]),
    PhrasebookCategory(id="ga-a2-travel", level="A2", situation="Taisteal", icon="🚌", phrases=[
        PhrasebookEntry(text="Cá bhfuil an stáisiún?", context="directions", register="neutral"),
        PhrasebookEntry(text="Ba mhaith liom ticéad amháin.", context="ticket", register="neutral"),
        PhrasebookEntry(text="Cén t-am a fhágann an bus?", context="schedule", register="neutral"),
        PhrasebookEntry(text="Cá fhad a thógfaidh sé?", context="duration", register="neutral"),
    ]),
    PhrasebookCategory(id="ga-b1-work", level="B1", situation="Obair agus staidéar", icon="💼", phrases=[
        PhrasebookEntry(text="Ba mhaith liom mo thuairim a thabhairt.", context="discussion", register="neutral"),
        PhrasebookEntry(text="Is é mo thuairim go bhfuil sé indéanta.", context="opinion", register="neutral"),
        PhrasebookEntry(text="An bhféadfaimis é seo a phlé níos déanaí?", context="meeting", register="neutral"),
        PhrasebookEntry(text="Tá gá le tuilleadh eolais.", context="information", register="neutral"),
    ]),
    PhrasebookCategory(id="ga-b2-professional", level="B2", situation="Cumarsáid fhoirmiúil", icon="📄", phrases=[
        PhrasebookEntry(text="De réir na tuarascála, tá gá le hathrú.", context="reporting", register="formal"),
        PhrasebookEntry(text="Ba cheart dúinn an cheist a mheas.", context="recommendation", register="formal"),
        PhrasebookEntry(text="Ba mhaith liom soiléiriú a iarraidh.", context="clarification", register="formal"),
        PhrasebookEntry(text="Táim ag tnúth le do fhreagra.", context="correspondence", register="formal"),
    ]),
    PhrasebookCategory(id="ga-c1-discussion", level="C1", situation="Argóint agus anailís", icon="🧠", phrases=[
        PhrasebookEntry(text="D'fhéadfaí a mhaíomh go bhfuil rogha eile ann.", context="argument", register="formal"),
        PhrasebookEntry(text="Is cosúil go bhfuil an cheist níos casta.", context="qualification", register="formal"),
        PhrasebookEntry(text="Ba cheart an comhthéacs a chur san áireamh.", context="analysis", register="formal"),
        PhrasebookEntry(text="Ní gá gurb ionann an dá rud.", context="distinction", register="formal"),
    ]),
    PhrasebookCategory(id="ga-c2-rhetoric", level="C2", situation="Reitric agus stíl", icon="✍️", phrases=[
        PhrasebookEntry(text="Ar an gcéad dul síos, is fiú an comhthéacs a scrúdú.", context="opening_argument", register="formal"),
        PhrasebookEntry(text="Os a choinne sin, tá fianaise eile ann.", context="contrast", register="formal"),
        PhrasebookEntry(text="Ní hamháin go bhfuil an cheist ábhartha, ach tá sí práinneach freisin.", context="emphasis", register="formal"),
        PhrasebookEntry(text="Ar deireadh thiar, is ceist í a bhaineann le luachanna.", context="conclusion", register="formal"),
    ]),
]

ASSESSMENT_BANK = [
    AssessmentQuestion(id="ga-a1-001", skill="communication", difficulty="A1", question="How do you greet someone in Irish?", options=["Dia duit","Slán","Inné","Cá bhfuil?"], correct="Dia duit"),
    AssessmentQuestion(id="ga-a1-002", skill="grammar", difficulty="A1", question="Choose the correct sentence for “I am a student.”", options=["Is mac léinn mé.","Tá mac léinn mé.","Mac léinn is mé?","Mé mac léinn tá."], correct="Is mac léinn mé."),
    AssessmentQuestion(id="ga-a1-003", skill="grammar", difficulty="A1", question="Which sentence means “I am not tired”?", options=["Nílim tuirseach.","Tá mé tuirseach.","Nílim anseo.","Tá mé anseo."], correct="Nílim tuirseach."),
    AssessmentQuestion(id="ga-a1-004", skill="vocabulary", difficulty="A1", question="Which word means “friend”?", options=["cara","teach","uisce","scoil"], correct="cara"),
    AssessmentQuestion(id="ga-a2-001", skill="grammar", difficulty="A2", question="Which sentence correctly uses the past tense?", options=["Chuaigh mé abhaile.","Rachaidh mé abhaile.","Téim abhaile.","Tá mé abhaile."], correct="Chuaigh mé abhaile."),
    AssessmentQuestion(id="ga-a2-002", skill="grammar", difficulty="A2", question="Which form means “I will go”?", options=["Rachaidh mé.","Rachainn.","Chuaigh mé.","Téim."], correct="Rachaidh mé."),
    AssessmentQuestion(id="ga-a2-003", skill="grammar", difficulty="A2", question="Which phrase means “with me”?", options=["liom","leat","aige","aici"], correct="liom"),
    AssessmentQuestion(id="ga-b1-001", skill="grammar", difficulty="B1", question="Complete the sentence: “Tá mé ___ Gaeilge.”", options=["ag foghlaim","chuaigh","dúirt","aige"], correct="ag foghlaim"),
    AssessmentQuestion(id="ga-b1-002", skill="grammar", difficulty="B1", question="Which sentence expresses a hypothetical condition?", options=["Dá mbeadh am agam, rachainn.","Tá am agam.","Rachaidh mé amárach.","Chuaigh mé inné."], correct="Dá mbeadh am agam, rachainn."),
    AssessmentQuestion(id="ga-b1-003", skill="language", difficulty="B1", question="What is séimhiú?", options=["lenition","eclipsis","a noun","a tense"], correct="lenition"),
    AssessmentQuestion(id="ga-b2-001", skill="grammar", difficulty="B2", question="Which sentence reports what someone said?", options=["Dúirt sé go raibh sé gnóthach.","Tá sé gnóthach.","Beidh sé gnóthach.","Bheadh sé gnóthach."], correct="Dúirt sé go raibh sé gnóthach."),
    AssessmentQuestion(id="ga-b2-002", skill="writing", difficulty="B2", question="Which expression is appropriate for a formal report?", options=["De réir na tuarascála...","Dia duit!","Cad é seo?","Slán go fóill."], correct="De réir na tuarascála..."),
    AssessmentQuestion(id="ga-b2-003", skill="reading", difficulty="B2", question="What does “fianaise” mean?", options=["evidence","station","family","tomorrow"], correct="evidence"),
    AssessmentQuestion(id="ga-c1-001", skill="writing", difficulty="C1", question="Which phrase appropriately qualifies a claim?", options=["Is cosúil go...","Tá sé cinnte i gcónaí...","Dia duit...","Slán..."], correct="Is cosúil go..."),
    AssessmentQuestion(id="ga-c1-002", skill="writing", difficulty="C1", question="Which term means “implication”?", options=["impleacht","oidhreacht","stáisiún","mála"], correct="impleacht"),
    AssessmentQuestion(id="ga-c1-003", skill="analysis", difficulty="C1", question="What is the purpose of discourse hedging?", options=["To qualify the strength of a claim","To greet someone","To form a plural","To give a phone number"], correct="To qualify the strength of a claim"),
    AssessmentQuestion(id="ga-c2-001", skill="style", difficulty="C2", question="Which connector means “on the other hand”?", options=["os a choinne sin","ar an gcéad dul síos","go raibh maith agat","amárach"], correct="os a choinne sin"),
    AssessmentQuestion(id="ga-c2-002", skill="analysis", difficulty="C2", question="Which concept refers to a counterargument?", options=["frithargóint","toimhde","béim","foirmiúlacht"], correct="frithargóint"),
    AssessmentQuestion(id="ga-c2-003", skill="style", difficulty="C2", question="Which phrase is suited to a formal conclusion?", options=["Ar deireadh thiar...","Dia duit!","Cá bhfuil an leithreas?","Ba mhaith liom uisce."], correct="Ar deireadh thiar..."),
]

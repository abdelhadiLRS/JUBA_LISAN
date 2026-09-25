"""తెలుగు foundation data for JUBA LISAN — CEFR A1-C2 curriculum."""
from app.data._types import (
    CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry,
    VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

GRAMMAR_DATA = {
    "A1": [
        ("word-order", "Basic Telugu word order", "syntax", "Subject-object-verb order", "Telugu commonly places the verb at the end of the clause.", "నేను తెలుగు నేర్చుకుంటాను."),
        ("pronouns", "Personal pronouns and honorifics", "pronouns", "Use personal pronouns with appropriate politeness", "నేను, నువ్వు, మీరు and other pronouns encode person and politeness.", "మీరు ఎలా ఉన్నారు?"),
        ("copula", "Nominal and adjectival sentences", "grammar", "Identify people and describe things", "Telugu often uses ఉన్నాను/ఉన్నారు for existential or locative meanings, while nominal predicates can omit a present copula.", "నేను విద్యార్థిని."),
        ("locative", "Location with లో", "morphology", "Say where someone or something is", "The locative suffix లో marks location.", "పుస్తకం బ్యాగులో ఉంది."),
        ("possession", "Possession with దగ్గర / యొక్క", "grammar", "Express possession", "దగ్గర is common for possession; యొక్క marks a more formal possessive relation.", "నా దగ్గర ఒక పుస్తకం ఉంది."),
        ("questions-negation", "Questions and basic negation", "syntax", "Ask and negate simple statements", "Question words and లేద/లేదు or verbal negative forms are used according to construction.", "మీరు ఎక్కడ ఉన్నారు?"),
    ],
    "A2": [
        ("plural-honorific", "Plural nouns and honorific agreement", "morphology", "Talk about groups and respect", "Plural marking and honorific verb forms help distinguish number and social respect.", "విద్యార్థులు తరగతిలో ఉన్నారు."),
        ("past", "Past tense", "verbs", "Describe completed events", "Past forms distinguish completed actions and states.", "నేను నిన్న హైదరాబాద్ వెళ్లాను."),
        ("future-intent", "Future and intention", "verbs", "Talk about plans and predictions", "Future-oriented forms and context express plans, intention and expectation.", "నేను రేపు చదువుతాను."),
        ("cases", "Case suffixes and postpositions", "morphology", "Connect nouns to their grammatical roles", "Telugu uses suffixes such as కు, తో, నుండి and లో for roles and relations.", "నేను స్నేహితుడితో మాట్లాడాను."),
        ("progressive", "Progressive aspect", "verbs", "Describe an action in progress", "The auxiliary construction -తున్న- expresses ongoing activity.", "ఆమె పుస్తకం చదువుతోంది."),
        ("comparisons", "Comparatives and preferences", "syntax", "Compare people and things", "కంటే and related constructions express comparison.", "ఈ పుస్తకం ఆ పుస్తకం కంటే సులభంగా ఉంది."),
    ],
    "B1": [
        ("perfect", "Perfect and resultative meanings", "aspect", "Relate completed actions to the present", "Telugu combines participial forms and auxiliaries to express completion and resulting states.", "నేను పని పూర్తి చేశాను."),
        ("conditional", "Conditional clauses", "syntax", "Express conditions and consequences", "If-then relationships are commonly formed with conditional verb morphology and అయితే/అయితే.", "వర్షం పడితే, నేను ఇంట్లో ఉంటాను."),
        ("relative", "Relative and adjectival clauses", "syntax", "Modify nouns with clauses", "Participial forms can modify nouns without a relative pronoun.", "నిన్న వచ్చిన వ్యక్తి నా స్నేహితుడు."),
        ("causative", "Causative constructions", "verbs", "Say that one person causes another action", "Causative morphology changes the argument structure of the verb.", "ఉపాధ్యాయుడు విద్యార్థులతో పాఠం చదివించాడు."),
        ("reported-speech", "Reported speech", "syntax", "Report statements and questions", "అని introduces quoted or reported content.", "ఆమె రేపు వస్తానని చెప్పింది."),
        ("connectors", "Discourse connectors and contrast", "discourse", "Link reasons, contrast and sequence", "కానీ, అందువల్ల, ఎందుకంటే, అయితే and తర్వాత organize discourse.", "వర్షం పడింది, అయినా మేము బయటికి వెళ్లాము."),
    ],
    "B2": [
        ("passive", "Passive and impersonal constructions", "syntax", "Focus on an event or result", "Passive-like constructions and impersonal wording shift attention away from the agent.", "నివేదికను నిన్న సమర్పించారు."),
        ("concession", "Concession and complex conditions", "syntax", "Express despite, even if and unless", "Complex conditional and concessive clauses create nuanced relationships.", "సమయం తక్కువైనా, మేము పని పూర్తి చేస్తాము."),
        ("nominalization", "Nominalization for formal writing", "style", "Turn actions into abstract nouns", "Nominalized forms are frequent in administrative and academic prose.", "పథకం అమలు విజయవంతమైంది."),
        ("indirect-question", "Embedded questions", "syntax", "Embed questions inside statements", "Question clauses can function as complements of knowing, asking and explaining.", "అతను ఎక్కడికి వెళ్లాడో నాకు తెలియదు."),
        ("register", "Formal and professional register", "style", "Adapt Telugu to workplace contexts", "Formal vocabulary, respectful forms and explicit connectors create professional prose.", "మీ అభ్యర్థనను పరిశీలించి త్వరలో తెలియజేస్తాము."),
        ("information-structure", "Topic, focus and emphasis", "discourse", "Control information flow", "Word order and particles can foreground contrastive or topical information.", "ఈ విషయాన్ని నేను ప్రత్యేకంగా వివరించాను."),
    ],
    "C1": [
        ("academic-hedging", "Academic hedging and evidential nuance", "academic", "Qualify claims responsibly", "Forms such as కావచ్చు, అనిపిస్తుంది and ఆధారాల ప్రకారం calibrate certainty.", "ఈ మార్పు దీర్ఘకాలంలో ప్రభావం చూపవచ్చని భావించవచ్చు."),
        ("subordination", "Dense subordinate clauses", "syntax", "Build complex multi-clause arguments", "Participles, complement clauses and connectors allow compact complex syntax.", "విధానం మారినప్పటికీ, ఫలితాలు ఆశించిన స్థాయికి చేరలేదని నివేదిక పేర్కొంది."),
        ("argumentation", "Argumentation and counterargument", "rhetoric", "Present claims, evidence and objections", "Formal Telugu uses structured connectors to distinguish claims, evidence and concessions.", "ఈ వాదనకు ఆధారాలు ఉన్నప్పటికీ, ప్రత్యామ్నాయ వివరణను కూడా పరిగణించాలి."),
        ("media-style", "Media and public-information style", "register", "Read and produce public-facing prose", "Headlines and reports favor compressed syntax and information-dense vocabulary.", "ప్రభుత్వం కొత్త విధానాన్ని ప్రకటించినట్లు అధికారులు తెలిపారు."),
        ("idiomatic", "Idiomatic and pragmatic nuance", "pragmatics", "Interpret implied meaning and politeness", "Meaning depends on context, honorific choice, indirectness and idiomatic expressions.", "చూద్దాం అనేది సందర్భాన్ని బట్టి అంగీకారం లేదా వాయిదాను సూచించవచ్చు."),
        ("translation", "Translation and paraphrase control", "translation", "Reformulate meaning without literal calques", "Advanced learners should preserve Telugu syntax, register and discourse relations when paraphrasing.", "అసలు భావాన్ని మార్చకుండా వాక్యాన్ని మరింత అధికారికంగా పునర్రచించండి."),
    ],
    "C2": [
        ("literary-style", "Literary and rhetorical Telugu", "style", "Handle elevated and figurative prose", "Literary Telugu uses imagery, parallelism, rhythm and lexical choice beyond everyday prose.", "ఆ నిశ్శబ్దం నగరపు జ్ఞాపకాలను మెల్లగా మేల్కొలిపింది."),
        ("complex-focus", "Advanced focus and information structure", "discourse", "Manipulate emphasis precisely", "Advanced prose uses ordering, particles and repetition to control contrast and rhetorical focus.", "అది కేవలం మార్పు కాదు; సమాజం తనను తాను చూసుకునే కొత్త దృష్టికోణం."),
        ("legal-administrative", "Legal and administrative formulation", "register", "Read precise institutional language", "Institutional Telugu favors explicit scope, conditions, obligations and nominalized structures.", "నిబంధనలకు అనుగుణంగా దరఖాస్తును నిర్ణీత గడువులో సమర్పించాలి."),
        ("rhetorical-concession", "Sophisticated concession and rebuttal", "rhetoric", "Anticipate and rebut objections", "Concessive structures can acknowledge evidence while redirecting the conclusion.", "ఈ విమర్శలో కొంత నిజం ఉన్నప్పటికీ, మొత్తం పరిస్థితిని అదే ఆధారంగా వివరించడం సాధ్యం కాదు."),
        ("lexical-register", "Lexical register and stylistic precision", "lexicon", "Choose exact formal or literary vocabulary", "C2 control requires deliberate selection between colloquial, neutral, formal and literary vocabulary.", "ఈ నిర్ణయం తాత్కాలిక పరిష్కారంగా మాత్రమే పరిగణించాలి."),
        ("discourse-analysis", "Discourse analysis and pragmatic interpretation", "discourse", "Infer stance, implication and rhetorical purpose", "Advanced comprehension tracks presupposition, stance, politeness, omission and context.", "ఆయన సమాధానం స్పష్టంగా లేకపోవడం కూడా ఒక నిర్దిష్ట వైఖరిని సూచిస్తుంది."),
    ],
}

VOCAB_DATA = {
    "A1": [("identity","పేరు","noun","name","నా పేరు అనిత."),("family","కుటుంబం","noun","family","నా కుటుంబం హైదరాబాద్‌లో ఉంది."),("home","ఇల్లు","noun","home; house","మా ఇల్లు పెద్దది."),("daily","ఈరోజు","adverb","today","ఈరోజు నేను పని చేస్తున్నాను.")],
    "A2": [("travel","ప్రయాణం","noun","travel; journey","మా ప్రయాణం రేపు ప్రారంభమవుతుంది."),("health","ఆరోగ్యం","noun","health","ఆరోగ్యం చాలా ముఖ్యం."),("education","చదువు","noun","education; study","ఆమె చదువుపై శ్రద్ధ పెడుతోంది."),("shopping","ధర","noun","price","ఈ పుస్తకం ధర ఎంత?")],
    "B1": [("work","అనుభవం","noun","experience","ఈ పనిలో నాకు మంచి అనుభవం ఉంది."),("society","సమాజం","noun","society","సమాజంలో మార్పు నెమ్మదిగా జరుగుతుంది."),("environment","పర్యావరణం","noun","environment","పర్యావరణాన్ని కాపాడాలి."),("technology","సాంకేతికత","noun","technology","సాంకేతికత పని విధానాన్ని మార్చింది.")],
    "B2": [("policy","విధానం","noun","policy; approach","కొత్త విధానం వచ్చే నెల నుంచి అమలవుతుంది."),("economy","ఆర్థిక వ్యవస్థ","noun","economy","ఆర్థిక వ్యవస్థపై అనేక అంశాలు ప్రభావం చూపుతాయి."),("research","పరిశోధన","noun","research","ఈ పరిశోధన కొత్త ఫలితాలను చూపించింది."),("communication","సంభాషణ","noun","communication; dialogue","స్పష్టమైన సంభాషణ సమస్యలను తగ్గిస్తుంది.")],
    "C1": [("evidence","ఆధారం","noun","evidence; basis","ఈ వాదనకు తగిన ఆధారం ఉంది."),("analysis","విశ్లేషణ","noun","analysis","విశ్లేషణలో ప్రధాన కారణాలు స్పష్టమయ్యాయి."),("perspective","దృక్కోణం","noun","perspective","ఈ సమస్యను మరో దృక్కోణంలో చూడాలి."),("implication","పర్యవసానం","noun","consequence; implication","ఈ నిర్ణయానికి దీర్ఘకాలిక పర్యవసానాలు ఉన్నాయి.")],
    "C2": [("rhetoric","వాక్చాతుర్యం","noun","rhetorical skill","ఆమె వాక్చాతుర్యం ప్రేక్షకులను ఆకట్టుకుంది."),("nuance","సూక్ష్మభేదం","noun","subtle distinction","ఈ రెండు పదాల మధ్య సూక్ష్మభేదం ఉంది."),("consensus","ఏకాభిప్రాయం","noun","consensus","చర్చల తర్వాత ఏకాభిప్రాయం ఏర్పడింది."),("ambiguity","అస్పష్టత","noun","ambiguity","వాక్యంలో కొంత అస్పష్టత ఉంది.")],
}

PHRASES = {
    "A1": [("greetings","Greetings","👋",[("నమస్కారం!","greeting","neutral"),("మీరు ఎలా ఉన్నారు?","asking how someone is","neutral"),("ధన్యవాదాలు.","thanking","neutral")]),("daily","Daily life","☀️",[("నాకు అర్థం కాలేదు.","asking for clarification","neutral"),("దయచేసి మళ్లీ చెప్పండి.","asking for repetition","neutral"),("నాకు సహాయం కావాలి.","asking for help","neutral")])],
    "A2": [("travel","Travel","✈️",[("స్టేషన్ ఎక్కడ ఉంది?","finding a station","neutral"),("నాకు ఒక టికెట్ కావాలి.","buying a ticket","neutral"),("రేపు ఉదయం బయలుదేరుతాను.","stating a plan","neutral")]),("health","Health","🩺",[("నాకు ఆరోగ్యం బాగాలేదు.","saying you feel unwell","neutral"),("డాక్టర్‌ను కలవాలి.","saying you need a doctor","neutral"),("నొప్పి ఎక్కడ ఉంది?","asking about pain","neutral")])],
    "B1": [("work","Work","💼",[("ఈ పని గురించి మాట్లాడుకుందాం.","suggesting a work discussion","neutral"),("నా అభిప్రాయం ప్రకారం ఇది సాధ్యమే.","giving an opinion","neutral"),("మరింత సమాచారం అవసరం.","requesting more information","formal")]),("discussion","Discussion","💬",[("మీ మాటలో కొంత నిజం ఉంది.","acknowledging a point","neutral"),("అయితే మరో కోణాన్ని కూడా చూడాలి.","introducing another perspective","neutral"),("దీనికి కారణం ఏమిటి?","asking for a reason","neutral")])],
    "B2": [("professional","Professional","📊",[("మీ అభ్యర్థనను పరిశీలిస్తాము.","responding formally","formal"),("దయచేసి అవసరమైన పత్రాలు పంపండి.","requesting documents","formal"),("ఈ విషయం గురించి తరువాత తెలియజేస్తాము.","promising a later update","formal")]),("argument","Argumentation","⚖️",[("ఈ వాదనకు తగిన ఆధారం ఉంది.","supporting a claim","formal"),("అయితే దీనికి మరో వివరణ కూడా ఉంది.","introducing a counterpoint","neutral"),("ఈ నిర్ణయానికి పర్యవసానాలు ఉంటాయి.","discussing implications","formal")])],
    "C1": [("academic","Academic","🎓",[("అందుబాటులో ఉన్న ఆధారాల ప్రకారం...","qualifying a claim","formal"),("ఈ ఫలితాన్ని జాగ్రత్తగా అర్థం చేసుకోవాలి.","qualifying interpretation","formal"),("మరోవైపు, ప్రత్యామ్నాయ వివరణను పరిగణించాలి.","introducing an alternative","formal")]),("media","Media","📰",[("అధికారుల ప్రకారం...","attributing information","formal"),("నివేదికలో పేర్కొన్నట్లుగా...","referring to a report","formal"),("ఈ పరిణామం విస్తృత ప్రభావం చూపవచ్చు.","discussing possible impact","formal")])],
    "C2": [("rhetoric","Rhetoric","🎙️",[("ఈ వాదనలోని ప్రధాన సమస్య ఏమిటంటే...","framing a critique","formal"),("ఈ అభ్యంతరాన్ని పూర్తిగా విస్మరించలేం.","acknowledging an objection","formal"),("సందర్భాన్ని పరిగణనలోకి తీసుకుంటే...","contextualizing a claim","formal")]),("formal-writing","Formal writing","📝",[("పై అంశాల ఆధారంగా పరిశీలిస్తే...","drawing a conclusion","formal"),("ఇది తాత్కాలిక పరిష్కారంగా మాత్రమే పరిగణించాలి.","limiting a conclusion","formal"),("ఈ అంశంపై మరింత పరిశోధన అవసరం.","calling for further research","formal")])],
}

CURRICULUM = {}
for level in LEVELS:
    units = []
    grammar = GRAMMAR_DATA[level]
    vocab = VOCAB_DATA[level]
    for i, (slug, title, *_rest) in enumerate(grammar, 1):
        units.append(CurriculumUnit(
            id=f"te-{level.lower()}-unit-{i}", level=level, unit_number=i,
            title=title, grammar_points=[slug],
            vocabulary_set_ids=[f"{vocab[(i-1) % len(vocab)][0]}_{level.lower()}"],
            lesson_types=["grammar","vocabulary","listening","speaking","reading","writing"],
            competency_checklist=[f"Use {title.lower()} accurately", "Apply the pattern in a short Telugu exchange"],
            default_weeks=1 if level in ["A1","A2"] else 2,
        ))
    CURRICULUM[level] = units

GRAMMAR_TOPICS = []
for level in LEVELS:
    for slug, title, category, summary, explanation, example in GRAMMAR_DATA[level]:
        GRAMMAR_TOPICS.append(GrammarTopic(
            slug=slug, title=title, level=level, category=category,
            summary=summary, explanation=explanation,
            examples=[GrammarExample(text=example, translation=None)],
        ))

VOCABULARY_SETS = []
for level in LEVELS:
    vocab = VOCAB_DATA[level]
    for i, (topic, word, pos, definition, example) in enumerate(vocab, 1):
        unit_number = i
        unit_ref = f"te-{level.lower()}-unit-{unit_number}"
        VOCABULARY_SETS.append(VocabularySet(
            id=f"{topic}_{level.lower()}", level=level, topic=topic,
            unit_ref=unit_ref,
            words=[VocabularyEntry(word=word, pos=pos, definition=definition, example=example)],
        ))

PHRASEBOOK_CATEGORIES = []
for level in LEVELS:
    for slug, situation, icon, entries in PHRASES[level]:
        PHRASEBOOK_CATEGORIES.append(PhrasebookCategory(
            id=f"te-{slug}_{level.lower()}", level=level, situation=situation, icon=icon,
            phrases=[PhrasebookEntry(text=t, context=c, register=r) for t,c,r in entries],
        ))

ASSESSMENT_BANK = [
    AssessmentQuestion(id="te-a1-001", skill="grammar", difficulty="A1", question="Which sentence means 'I am at home'?", options=["నేను ఇంట్లో ఉన్నాను.","నేను పని చేస్తున్నాను.","నేను రేపు వెళ్తాను.","అతను పుస్తకం చదివాడు."], correct="నేను ఇంట్లో ఉన్నాను.", grammar_slug="locative"),
    AssessmentQuestion(id="te-a2-001", skill="grammar", difficulty="A2", question="Which form expresses an action in progress?", options=["చదువుతోంది","చదివింది","చదువుతుంది","చదవలేదు"], correct="చదువుతోంది", grammar_slug="progressive"),
    AssessmentQuestion(id="te-b1-001", skill="grammar", difficulty="B1", question="Which sentence expresses a condition?", options=["వర్షం పడితే, నేను ఇంట్లో ఉంటాను.","నేను నిన్న వెళ్లాను.","ఆమె పుస్తకం చదువుతోంది.","అతను విద్యార్థి."], correct="వర్షం పడితే, నేను ఇంట్లో ఉంటాను.", grammar_slug="conditional"),
    AssessmentQuestion(id="te-b2-001", skill="grammar", difficulty="B2", question="Which sentence contains an embedded question?", options=["అతను ఎక్కడికి వెళ్లాడో నాకు తెలియదు.","నేను ఇంటికి వెళ్తాను.","ఆమె పుస్తకం చదువుతోంది.","మేము నిన్న కలిశాము."], correct="అతను ఎక్కడికి వెళ్లాడో నాకు తెలియదు.", grammar_slug="indirect-question"),
    AssessmentQuestion(id="te-c1-001", skill="reading", difficulty="C1", question="Which expression appropriately qualifies an academic claim?", options=["ఆధారాల ప్రకారం","చాలా బాగుంది","రండి కూర్చోండి","ఇది ఎంత?"], correct="ఆధారాల ప్రకారం", grammar_slug="academic-hedging"),
    AssessmentQuestion(id="te-c2-001", skill="reading", difficulty="C2", question="Which phrase explicitly limits a conclusion?", options=["ఇది తాత్కాలిక పరిష్కారంగా మాత్రమే పరిగణించాలి.","నమస్కారం!","నాకు నీరు కావాలి.","ఎక్కడికి వెళ్తున్నారు?"], correct="ఇది తాత్కాలిక పరిష్కారంగా మాత్రమే పరిగణించాలి.", grammar_slug="lexical-register"),
]

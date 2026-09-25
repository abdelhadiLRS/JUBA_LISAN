"""मराठी foundation data for JUBA LISAN — CEFR A1-C2 curriculum."""
from app.data._types import (
    CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry,
    VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

GRAMMAR_DATA = {
    "A1": [
        ("word-order","Basic Marathi sentence order","syntax","Build simple subject-object-verb sentences","Marathi normally places the finite verb at the end of the clause.","मी मराठी शिकतो."),
        ("pronouns","Personal pronouns and politeness","pronouns","Use मी, तू, तुम्ही and other personal pronouns appropriately","Pronoun choice reflects person, number and politeness.","तुम्ही कसे आहात?"),
        ("gender-agreement","Gender and agreement","morphology","Match common nouns and adjectives","Marathi has grammatical gender and agreement patterns that affect forms.","ही माझी बहीण आहे."),
        ("present","Present and habitual forms","verbs","Talk about current and regular activities","Present and habitual constructions describe states, actions and routines.","मी रोज काम करतो."),
        ("negation","Basic negation","syntax","Negate simple statements","नाही and negative verbal forms are used according to the construction.","मला चहा नको आहे."),
        ("questions","Questions and question words","syntax","Ask who, what, where and when","कोण, काय, कुठे, कधी and किती form common A1 questions.","बाजार कुठे आहे?"),
    ],
    "A2": [
        ("past","Past tense","verbs","Describe completed events","Marathi past forms interact with gender and transitivity.","मी काल पुण्याला गेलो."),
        ("future","Future and plans","verbs","Talk about future events","Future forms express intention, prediction and scheduled events.","मी उद्या येईन."),
        ("case-postpositions","Case and postpositions","morphology","Express relations such as to, from, with and in","Marathi uses postpositions and oblique noun forms for grammatical relations.","मी मित्रासोबत बाजारात गेलो."),
        ("progressive","Progressive constructions","aspect","Describe actions in progress","The progressive construction expresses an ongoing activity.","ती पुस्तक वाचत आहे."),
        ("comparative","Comparison and degree","syntax","Compare people and things","पेक्षा and degree expressions build comparisons.","हे घर त्या घरापेक्षा मोठे आहे."),
        ("modal","Ability, necessity and desire","modality","Express can, must, want and need","Modal expressions combine lexical verbs and constructions to express stance.","मला आज काम करायचे आहे."),
    ],
    "B1": [
        ("perfect","Perfect and completed-result meanings","aspect","Connect completed events to a present result","Perfect constructions describe completed actions and their relevance.","मी अहवाल पूर्ण केला आहे."),
        ("conditional","Conditional clauses","syntax","Express conditions and consequences","जर...तर and conditional verb forms link hypothetical conditions to outcomes.","जर पाऊस पडला तर आपण घरी राहू."),
        ("relative","Relative and participial clauses","syntax","Modify nouns with clauses","Marathi uses relative-correlative structures such as जो...तो and participles.","जो मुलगा आला तो माझा मित्र आहे."),
        ("reported","Reported speech","syntax","Report statements and questions","Reported content can be introduced with की and related complement structures.","तिने सांगितले की ती उद्या येईल."),
        ("causative","Causative constructions","verbs","Express causing or arranging an action","Causative morphology and lexical causatives change who causes an event.","शिक्षकांनी विद्यार्थ्यांना वाचायला लावले."),
        ("connectors","Reason, contrast and sequence","discourse","Link ideas coherently","कारण, म्हणून, पण, तरीही and नंतर organize connected discourse.","पाऊस पडत होता, तरीही आम्ही गेलो."),
    ],
    "B2": [
        ("passive","Passive and impersonal constructions","syntax","Focus on an action rather than its agent","Passive and impersonal wording is useful in reports and formal prose.","अहवाल काल सादर करण्यात आला."),
        ("concession","Concession and complex conditions","syntax","Express despite, even if and unless","जरी...तरी and related patterns encode concession and complex conditions.","जरी वेळ कमी असला तरी आम्ही काम पूर्ण करू."),
        ("nominalization","Nominalization in formal prose","style","Turn processes into abstract nouns","Formal Marathi frequently uses abstract nouns for institutional and academic writing.","योजनेची अंमलबजावणी सुरू झाली."),
        ("embedded-question","Embedded questions","syntax","Embed questions in larger clauses","Question clauses can function as complements of knowing, asking and explaining.","तो कुठे गेला हे मला माहीत नाही."),
        ("register","Professional and formal register","style","Adapt Marathi to workplace contexts","Respectful forms, formal vocabulary and explicit connectors create professional prose.","आपल्या अर्जाची तपासणी करून कळविण्यात येईल."),
        ("focus","Topic and focus","discourse","Control emphasis and information flow","Word order, particles and repetition can highlight contrastive information.","ही बाब मी विशेषतः स्पष्ट केली आहे."),
    ],
    "C1": [
        ("hedging","Academic hedging and evidential nuance","academic","Calibrate certainty and evidence","कदाचित, उपलब्ध पुराव्यानुसार and असे दिसते that-like expressions qualify claims.","उपलब्ध पुराव्यानुसार हा बदल दीर्घकालीन परिणाम करू शकतो."),
        ("subordination","Dense subordinate structures","syntax","Build multi-clause arguments","Participial, complement and conditional structures allow compact complex prose.","धोरण बदलले असले तरी अपेक्षित परिणाम साध्य झाले नाहीत असे अहवालात नमूद आहे."),
        ("argumentation","Argumentation and counterargument","rhetoric","Present claims, evidence and concessions","Formal discourse distinguishes claim, evidence, objection and response.","या मताला काही आधार असला तरी पर्यायी स्पष्टीकरण विचारात घ्यावे."),
        ("media","Media and public-information style","register","Read and write information-dense reports","News prose favors attribution, compressed clauses and formal lexical choices.","अधिकाऱ्यांनी नवीन धोरण जाहीर केल्याचे सांगितले."),
        ("pragmatics","Pragmatic and idiomatic nuance","pragmatics","Interpret indirectness and context","Meaning depends on politeness, context, idioms and what is left implicit.","पाहूया हे संदर्भानुसार मान्यता किंवा पुढे ढकलणे दर्शवू शकते."),
        ("paraphrase","Advanced paraphrase and translation","translation","Reformulate meaning without literal calques","Advanced learners preserve Marathi register, syntax and discourse relations when paraphrasing.","मूळ आशय कायम ठेवून वाक्य अधिक औपचारिक करा."),
    ],
    "C2": [
        ("literary","Literary and rhetorical Marathi","style","Handle elevated and figurative prose","Literary Marathi uses imagery, rhythm, parallelism and deliberate lexical selection.","त्या शांततेने शहराच्या आठवणी हळूहळू जाग्या केल्या."),
        ("advanced-focus","Advanced focus and information structure","discourse","Manipulate emphasis precisely","Advanced prose uses ordering and discourse devices to create contrast and rhetorical focus.","हा केवळ बदल नाही; समाजाकडे पाहण्याचा नवा दृष्टिकोन आहे."),
        ("legal","Legal and administrative formulation","register","Read precise institutional language","Institutional Marathi specifies scope, obligations, exceptions and procedures explicitly.","नियमांनुसार अर्ज निर्धारित मुदतीत सादर करणे आवश्यक आहे."),
        ("rebuttal","Sophisticated concession and rebuttal","rhetoric","Acknowledge and rebut objections","Concessive clauses can recognize evidence while redirecting the conclusion.","या टीकेत काही तथ्य असले तरी संपूर्ण परिस्थितीचे स्पष्टीकरण त्यातून होत नाही."),
        ("lexical-precision","Lexical register and stylistic precision","lexicon","Choose exact formal, neutral or literary vocabulary","C2 control requires deliberate register selection rather than literal synonym choice.","हा निर्णय केवळ तात्पुरता उपाय म्हणून विचारात घ्यावा."),
        ("discourse-analysis","Discourse analysis and pragmatic interpretation","discourse","Infer stance, implication and rhetorical purpose","Advanced comprehension tracks presupposition, stance, politeness and omission.","त्याचे उत्तर अस्पष्ट राहणे हीदेखील एक विशिष्ट भूमिका सूचित करते."),
    ],
}

VOCAB_DATA = {
    "A1":[("identity","नाव","noun","name","माझे नाव अनिता आहे."),("family","कुटुंब","noun","family","माझे कुटुंब पुण्यात आहे."),("home","घर","noun","home; house","हे माझे घर आहे."),("routine","काम","noun","work","मी रोज काम करतो.")],
    "A2":[("travel","प्रवास","noun","journey; travel","आमचा प्रवास उद्या सुरू होईल."),("health","आरोग्य","noun","health","आरोग्य खूप महत्त्वाचे आहे."),("education","शिक्षण","noun","education","शिक्षणासाठी वेळ देणे आवश्यक आहे."),("shopping","किंमत","noun","price","या पुस्तकाची किंमत किती आहे?")],
    "B1":[("work","अनुभव","noun","experience","या कामाचा मला चांगला अनुभव आहे."),("society","समाज","noun","society","समाजात बदल हळूहळू होतो."),("environment","पर्यावरण","noun","environment","पर्यावरणाचे संरक्षण करणे गरजेचे आहे."),("technology","तंत्रज्ञान","noun","technology","तंत्रज्ञानामुळे कामाची पद्धत बदलली आहे.")],
    "B2":[("policy","धोरण","noun","policy; approach","नवे धोरण पुढील महिन्यापासून लागू होईल."),("economy","अर्थव्यवस्था","noun","economy","अर्थव्यवस्थेवर अनेक घटकांचा परिणाम होतो."),("research","संशोधन","noun","research","या संशोधनातून नवे निष्कर्ष मिळाले."),("communication","संवाद","noun","communication; dialogue","स्पष्ट संवादामुळे गैरसमज कमी होतात.")],
    "C1":[("evidence","पुरावा","noun","evidence","या दाव्याला पुरेसा पुरावा आहे."),("analysis","विश्लेषण","noun","analysis","विश्लेषणातून मुख्य कारणे स्पष्ट झाली."),("perspective","दृष्टिकोन","noun","perspective","हा प्रश्न दुसऱ्या दृष्टिकोनातून पाहावा."),("implication","परिणाम","noun","consequence; implication","या निर्णयाचे दीर्घकालीन परिणाम आहेत.")],
    "C2":[("rhetoric","वक्तृत्व","noun","rhetoric; public speaking","त्यांच्या वक्तृत्वाने श्रोते प्रभावित झाले."),("nuance","सूक्ष्मभेद","noun","subtle distinction","या दोन शब्दांमध्ये सूक्ष्मभेद आहे."),("consensus","एकमत","noun","consensus","चर्चेनंतर एकमत झाले."),("ambiguity","अस्पष्टता","noun","ambiguity","या वाक्यात काही अस्पष्टता आहे.")],
}

PHRASES = {
    "A1":[("greetings","Greetings","👋",[("नमस्कार!","greeting","neutral"),("तुम्ही कसे आहात?","asking how someone is","neutral"),("धन्यवाद.","thanking","neutral")]),("daily","Daily life","☀️",[("मला समजले नाही.","asking for clarification","neutral"),("कृपया पुन्हा सांगा.","asking for repetition","neutral"),("कृपया मला मदत करा.","asking for help","neutral")])],
    "A2":[("travel","Travel","✈️",[("स्थानक कुठे आहे?","finding a station","neutral"),("मला एक तिकीट हवे आहे.","buying a ticket","neutral"),("मी उद्या सकाळी निघेन.","stating a plan","neutral")]),("health","Health","🩺",[("माझी तब्येत ठीक नाही.","saying you feel unwell","neutral"),("मला डॉक्टरांना भेटायचे आहे.","saying you need a doctor","neutral"),("दुखत कुठे आहे?","asking about pain","neutral")])],
    "B1":[("work","Work","💼",[("या कामाबद्दल बोलूया.","suggesting a work discussion","neutral"),("माझ्या मते हे शक्य आहे.","giving an opinion","neutral"),("अधिक माहिती आवश्यक आहे.","requesting more information","formal")]),("discussion","Discussion","💬",[("तुमच्या म्हणण्यात काही तथ्य आहे.","acknowledging a point","neutral"),("तरीही दुसरा दृष्टिकोन पाहायला हवा.","introducing another perspective","neutral"),("याचे कारण काय आहे?","asking for a reason","neutral")])],
    "B2":[("professional","Professional","📊",[("आपल्या अर्जाची तपासणी करू.","responding formally","formal"),("कृपया आवश्यक कागदपत्रे पाठवा.","requesting documents","formal"),("या विषयाबद्दल नंतर कळवू.","promising an update","formal")]),("argument","Argumentation","⚖️",[("या दाव्याला पुरेसा पुरावा आहे.","supporting a claim","formal"),("तथापि, दुसरे स्पष्टीकरणही शक्य आहे.","introducing a counterpoint","formal"),("या निर्णयाचे परिणाम होतील.","discussing implications","formal")])],
    "C1":[("academic","Academic","🎓",[("उपलब्ध पुराव्यानुसार...","qualifying a claim","formal"),("या निष्कर्षाचा काळजीपूर्वक अर्थ लावावा.","qualifying interpretation","formal"),("दुसरीकडे, पर्यायी स्पष्टीकरण विचारात घ्यावे.","introducing an alternative","formal")]),("media","Media","📰",[("अधिकाऱ्यांच्या म्हणण्यानुसार...","attributing information","formal"),("अहवालात नमूद केल्याप्रमाणे...","referring to a report","formal"),("या घडामोडीचा व्यापक परिणाम होऊ शकतो.","discussing possible impact","formal")])],
    "C2":[("rhetoric","Rhetoric","🎙️",[("या युक्तिवादातील मुख्य अडचण अशी आहे की...","framing a critique","formal"),("हा आक्षेप पूर्णपणे दुर्लक्षित करता येणार नाही.","acknowledging an objection","formal"),("संदर्भ लक्षात घेतल्यास...","contextualizing a claim","formal")]),("formal-writing","Formal writing","📝",[("वरील मुद्द्यांच्या आधारे पाहता...","drawing a conclusion","formal"),("हा केवळ तात्पुरता उपाय म्हणून विचारात घ्यावा.","limiting a conclusion","formal"),("या विषयावर अधिक संशोधन आवश्यक आहे.","calling for further research","formal")])],
}

CURRICULUM = {}
for level in LEVELS:
    units=[]
    grammar=GRAMMAR_DATA[level]
    vocab=VOCAB_DATA[level]
    for i,(slug,title,*_) in enumerate(grammar,1):
        topic=vocab[(i-1)%len(vocab)][0]
        units.append(CurriculumUnit(
            id=f"mr-{level.lower()}-unit-{i}", level=level, unit_number=i,
            title=title, grammar_points=[slug], vocabulary_set_ids=[f"{topic}_{level.lower()}"],
            lesson_types=["grammar","vocabulary","listening","speaking","reading","writing"],
            competency_checklist=[f"Use {title.lower()} accurately","Apply the pattern in a short Marathi exchange"],
            default_weeks=1 if level in ["A1","A2"] else 2,
        ))
    CURRICULUM[level]=units

GRAMMAR_TOPICS=[]
for level in LEVELS:
    for slug,title,category,summary,explanation,example in GRAMMAR_DATA[level]:
        GRAMMAR_TOPICS.append(GrammarTopic(slug=slug,title=title,level=level,category=category,summary=summary,explanation=explanation,examples=[GrammarExample(text=example)]))

VOCABULARY_SETS=[]
for level in LEVELS:
    for i,(topic,word,pos,definition,example) in enumerate(VOCAB_DATA[level],1):
        VOCABULARY_SETS.append(VocabularySet(
            id=f"{topic}_{level.lower()}", level=level, topic=topic,
            unit_ref=f"mr-{level.lower()}-unit-{i}", words=[VocabularyEntry(word=word,pos=pos,definition=definition,example=example)]
        ))

PHRASEBOOK_CATEGORIES=[]
for level in LEVELS:
    for slug,situation,icon,entries in PHRASES[level]:
        PHRASEBOOK_CATEGORIES.append(PhrasebookCategory(
            id=f"mr-{slug}_{level.lower()}", level=level, situation=situation, icon=icon,
            phrases=[PhrasebookEntry(text=text,context=context,register=register) for text,context,register in entries]
        ))

ASSESSMENT_BANK=[
    AssessmentQuestion(id="mr-a1-001",skill="grammar",difficulty="A1",question="Which sentence says 'My name is Anita'?",options=["माझे नाव अनिता आहे.","मी रोज काम करतो.","बाजार कुठे आहे?","हे माझे घर आहे."],correct="माझे नाव अनिता आहे.",grammar_slug="pronouns"),
    AssessmentQuestion(id="mr-a2-001",skill="grammar",difficulty="A2",question="Which sentence expresses an action in progress?",options=["ती पुस्तक वाचत आहे.","मी काल गेलो.","मी उद्या येईन.","मला चहा नको आहे."],correct="ती पुस्तक वाचत आहे.",grammar_slug="progressive"),
    AssessmentQuestion(id="mr-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["जर पाऊस पडला तर आपण घरी राहू.","मी अहवाल पूर्ण केला आहे.","ती पुस्तक वाचते.","तो माझा मित्र आहे."],correct="जर पाऊस पडला तर आपण घरी राहू.",grammar_slug="conditional"),
    AssessmentQuestion(id="mr-b2-001",skill="grammar",difficulty="B2",question="Which sentence contains an embedded question?",options=["तो कुठे गेला हे मला माहीत नाही.","मी घरी जातो.","ती काम करते.","आम्ही काल भेटलो."],correct="तो कुठे गेला हे मला माहीत नाही.",grammar_slug="embedded-question"),
    AssessmentQuestion(id="mr-c1-001",skill="reading",difficulty="C1",question="Which expression appropriately qualifies an academic claim?",options=["उपलब्ध पुराव्यानुसार","नमस्कार!","कितीला आहे?","लवकर या."],correct="उपलब्ध पुराव्यानुसार",grammar_slug="hedging"),
    AssessmentQuestion(id="mr-c2-001",skill="reading",difficulty="C2",question="Which sentence explicitly limits a conclusion?",options=["हा केवळ तात्पुरता उपाय म्हणून विचारात घ्यावा.","नमस्कार!","मला पाणी हवे आहे.","कुठे जात आहात?"],correct="हा केवळ तात्पुरता उपाय म्हणून विचारात घ्यावा.",grammar_slug="lexical-precision"),
]

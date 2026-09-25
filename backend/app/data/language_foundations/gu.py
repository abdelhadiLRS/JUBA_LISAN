"""ગુજરાતી foundation data for JUBA LISAN — CEFR A1-C2 curriculum."""
from app.data._types import (
    CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry,
    VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion,
)

LEVELS=["A1","A2","B1","B2","C1","C2"]

GRAMMAR_DATA={
"A1":[
("word-order","Basic Gujarati sentence order","syntax","Build subject-object-verb sentences","Gujarati commonly places the finite verb at the end of the clause.","હું ગુજરાતી શીખું છું."),
("pronouns","Personal pronouns and politeness","pronouns","Use હું, તું, તમે and related forms","Pronoun selection reflects person, number and politeness.","તમે કેમ છો?"),
("copula","Present copula and identity","grammar","Identify people and objects","છું, છો, છે and related copular forms express identity and description.","હું વિદ્યાર્થી છું."),
("possession","Possession with પાસે and મારું","grammar","Express ownership and possession","Gujarati commonly uses પાસે for possession and possessive forms such as મારું.","મારી પાસે એક પુસ્તક છે."),
("present","Present and habitual actions","verbs","Describe current and regular activity","Present forms express ongoing or habitual actions.","હું દરરોજ કામ કરું છું."),
("questions-negation","Questions and negation","syntax","Ask basic questions and make negative statements","Question words such as ક્યાં, શું, કોણ and negative forms organize basic exchanges.","તમે ક્યાં રહો છો?"),
],
"A2":[
("past","Past tense","verbs","Describe completed events","Past forms vary with verb type and gender/number agreement in relevant constructions.","હું ગઈકાલે અમદાવાદ ગયો હતો."),
("future","Future and plans","verbs","Discuss plans and predictions","Future forms express intention, expectation and scheduled events.","હું કાલે આવીશ."),
("postpositions","Postpositions and oblique forms","morphology","Express relations such as to, from, with and in","Gujarati uses postpositions with appropriate noun forms.","હું મિત્ર સાથે બજારમાં ગયો."),
("progressive","Progressive aspect","aspect","Describe an action in progress","The progressive construction combines a verb stem with auxiliary forms.","તે પુસ્તક વાંચી રહી છે."),
("comparison","Comparatives and superlatives","syntax","Compare people and things","કરતાં and degree words create comparisons.","આ ઘર તે ઘર કરતાં મોટું છે."),
("modality","Ability, necessity and desire","modality","Express can, should, need and want","Modal constructions encode ability, obligation, preference and intention.","મારે આજે કામ કરવું છે."),
],
"B1":[
("perfect","Perfect and resultative meanings","aspect","Connect completed actions to present results","Perfect constructions describe completed actions with current relevance.","મેં કામ પૂરું કર્યું છે."),
("conditional","Conditional clauses","syntax","Express conditions and consequences","જો...તો and conditional verb forms create hypothetical and real conditions.","જો વરસાદ પડે તો આપણે ઘરે રહીશું."),
("relative","Relative-correlative clauses","syntax","Modify nouns with clauses","જે...તે and related forms connect relative and correlative clauses.","જે છોકરો આવ્યો તે મારો મિત્ર છે."),
("reported","Reported speech","syntax","Report statements and questions","કે introduces many reported propositions.","તેણીએ કહ્યું કે તે કાલે આવશે."),
("causative","Causative constructions","verbs","Express causing an action","Causative morphology or lexical constructions show who causes an event.","શિક્ષકે વિદ્યાર્થીઓને વાંચવા કરાવ્યું."),
("connectors","Reason, contrast and sequence","discourse","Link arguments and events","કારણ કે, તેથી, પરંતુ, છતાં અને પછી structure connected discourse.","વરસાદ પડતો હતો, છતાં અમે ગયા."),
],
"B2":[
("passive","Passive and impersonal constructions","syntax","Focus on an event or result","Passive and impersonal wording is useful in reports and formal prose.","અહેવાલ ગઈકાલે રજૂ કરવામાં આવ્યો."),
("concession","Concession and complex conditions","syntax","Express despite and even if","જોકે...છતાં and conditional patterns encode concession and complex relationships.","જોકે સમય ઓછો હતો, છતાં કામ પૂરું થયું."),
("nominalization","Nominalization in formal writing","style","Use abstract nouns for processes","Formal Gujarati frequently uses nominalized forms in institutional and academic writing.","યોજનાનો અમલ સફળ રહ્યો."),
("embedded","Embedded questions","syntax","Embed questions in larger clauses","Question clauses function as complements of knowing, asking and explaining.","તે ક્યાં ગયો તે મને ખબર નથી."),
("register","Professional and formal Gujarati","style","Adapt Gujarati to workplace contexts","Respectful forms, formal vocabulary and explicit connectors create professional prose.","તમારી અરજીની તપાસ કરીને જાણ કરવામાં આવશે."),
("focus","Topic, focus and emphasis","discourse","Control information flow","Word order and discourse particles can foreground contrastive information.","આ બાબત મેં ખાસ કરીને સમજાવી છે."),
],
"C1":[
("hedging","Academic hedging and evidential nuance","academic","Qualify claims and calibrate certainty","કદાચ, ઉપલબ્ધ પુરાવા મુજબ and લાગે છે help distinguish certainty from interpretation.","ઉપલબ્ધ પુરાવા મુજબ આ ફેરફાર લાંબા ગાળે અસર કરી શકે છે."),
("subordination","Dense subordinate clauses","syntax","Build complex multi-clause arguments","Participial, complement and conditional clauses support compact formal prose.","નીતિ બદલાઈ હોવા છતાં અપેક્ષિત પરિણામ મળ્યું નથી એવું અહેવાલમાં જણાવાયું છે."),
("argumentation","Argumentation and counterargument","rhetoric","Present claims, evidence and objections","Formal discourse distinguishes claims, evidence, concessions and responses.","આ દાવાને કેટલાક પુરાવા મળે છે, છતાં વૈકલ્પિક સમજૂતી પણ વિચારવી જોઈએ."),
("media","Media and public-information style","register","Read and produce information-dense reports","News prose favors attribution, compressed syntax and formal vocabulary.","અધિકારીઓએ નવી નીતિ જાહેર કરી હોવાનું જણાવ્યું."),
("pragmatics","Idiomatic and pragmatic nuance","pragmatics","Interpret indirectness and contextual meaning","Meaning depends on politeness, context, idioms and implied stance.","જોઈશું સંદર્ભ પ્રમાણે સંમતિ અથવા મુલતવી રાખવાનું સૂચવી શકે છે."),
("paraphrase","Advanced paraphrase and translation","translation","Reformulate without literal calques","Advanced learners preserve Gujarati syntax, register and discourse relations when paraphrasing.","મૂળ અર્થ જાળવીને વાક્યને વધુ ઔપચારિક રીતે ફરી લખો."),
],
"C2":[
("literary","Literary and rhetorical Gujarati","style","Handle elevated and figurative prose","Literary Gujarati uses imagery, rhythm, parallelism and deliberate lexical choice.","એ શાંતિએ શહેરની યાદોને ધીમે ધીમે જાગૃત કરી."),
("advanced-focus","Advanced information structure","discourse","Manipulate emphasis precisely","Advanced prose controls contrast, topic and focus through syntax and discourse devices.","આ માત્ર ફેરફાર નથી; સમાજને જોવાનો નવો દૃષ્ટિકોણ છે."),
("legal","Legal and administrative formulation","register","Read precise institutional language","Institutional Gujarati specifies scope, obligations, conditions and procedures.","નિયમો અનુસાર અરજી નિર્ધારિત સમયમર્યાદામાં રજૂ કરવી જરૂરી છે."),
("rebuttal","Sophisticated concession and rebuttal","rhetoric","Acknowledge objections and redirect conclusions","Concessive structures recognize evidence while limiting its implications.","આ ટીકા અંશતઃ યોગ્ય હોવા છતાં સમગ્ર પરિસ્થિતિનું સમાધાન તેનાથી થતું નથી."),
("lexical-precision","Lexical register and stylistic precision","lexicon","Choose exact formal, neutral or literary vocabulary","C2 control requires deliberate register selection rather than literal synonym choice.","આ નિર્ણયને માત્ર તાત્કાલિક ઉકેલ તરીકે જ ગણવો જોઈએ."),
("discourse-analysis","Discourse analysis and pragmatic interpretation","discourse","Infer stance, implication and rhetorical purpose","Advanced comprehension tracks presupposition, stance, politeness and omission.","તેનો અસ્પષ્ટ જવાબ પણ એક ચોક્કસ વલણ સૂચવી શકે છે."),
]}

VOCAB_DATA={
"A1":[("identity","નામ","noun","name","મારું નામ અનિતા છે."),("family","પરિવાર","noun","family","મારો પરિવાર નાનો છે."),("home","ઘર","noun","home; house","આ મારું ઘર છે."),("routine","કામ","noun","work","હું દરરોજ કામ કરું છું.")],
"A2":[("travel","પ્રવાસ","noun","journey; travel","અમારો પ્રવાસ કાલે શરૂ થશે."),("health","આરોગ્ય","noun","health","આરોગ્ય ખૂબ મહત્વનું છે."),("education","શિક્ષણ","noun","education","શિક્ષણ માટે સમય આપવો જરૂરી છે."),("shopping","કિંમત","noun","price","આ પુસ્તકની કિંમત કેટલી છે?")],
"B1":[("work","અનુભવ","noun","experience","આ કામનો મને સારો અનુભવ છે."),("society","સમાજ","noun","society","સમાજમાં ફેરફાર ધીમે થાય છે."),("environment","પર્યાવરણ","noun","environment","પર્યાવરણનું રક્ષણ કરવું જરૂરી છે."),("technology","ટેકનોલોજી","noun","technology","ટેકનોલોજીએ કામ કરવાની રીત બદલી છે.")],
"B2":[("policy","નીતિ","noun","policy","નવી નીતિ આવતા મહિનાથી અમલમાં આવશે."),("economy","અર્થતંત્ર","noun","economy","અર્થતંત્ર પર ઘણા પરિબળોની અસર થાય છે."),("research","સંશોધન","noun","research","આ સંશોધનથી નવા તારણો મળ્યા."),("communication","સંવાદ","noun","communication; dialogue","સ્પષ્ટ સંવાદ ગેરસમજ ઘટાડે છે.")],
"C1":[("evidence","પુરાવો","noun","evidence","આ દાવા માટે પૂરતો પુરાવો છે."),("analysis","વિશ્લેષણ","noun","analysis","વિશ્લેષણથી મુખ્ય કારણો સ્પષ્ટ થયા."),("perspective","દૃષ્ટિકોણ","noun","perspective","આ પ્રશ્નને બીજા દૃષ્ટિકોણથી જોવો જોઈએ."),("implication","પરિણામ","noun","consequence; implication","આ નિર્ણયના લાંબા ગાળાના પરિણામો છે.")],
"C2":[("rhetoric","વક્તૃત્વ","noun","rhetoric; oratory","તેમના વક્તૃત્વે શ્રોતાઓને પ્રભાવિત કર્યા."),("nuance","સૂક્ષ્મ તફાવત","noun","subtle distinction","આ બે શબ્દો વચ્ચે સૂક્ષ્મ તફાવત છે."),("consensus","સર્વસંમતિ","noun","consensus","ચર્ચા પછી સર્વસંમતિ બની."),("ambiguity","અસ્પષ્ટતા","noun","ambiguity","વાક્યમાં થોડી અસ્પષ્ટતા છે.")],
}

PHRASES={
"A1":[("greetings","Greetings","👋",[("નમસ્તે!","greeting","neutral"),("તમે કેમ છો?","asking how someone is","neutral"),("આભાર.","thanking","neutral")]),("daily","Daily life","☀️",[("મને સમજાયું નથી.","asking for clarification","neutral"),("કૃપા કરીને ફરી કહો.","asking for repetition","neutral"),("કૃપા કરીને મને મદદ કરો.","asking for help","neutral")])],
"A2":[("travel","Travel","✈️",[("સ્ટેશન ક્યાં છે?","finding a station","neutral"),("મારે એક ટિકિટ જોઈએ છે.","buying a ticket","neutral"),("હું કાલે સવારે નીકળીશ.","stating a plan","neutral")]),("health","Health","🩺",[("મારી તબિયત સારી નથી.","saying you feel unwell","neutral"),("મારે ડૉક્ટરને મળવું છે.","saying you need a doctor","neutral"),("ક્યાં દુખે છે?","asking about pain","neutral")])],
"B1":[("work","Work","💼",[("આ કામ વિશે વાત કરીએ.","suggesting a work discussion","neutral"),("મારા મતે આ શક્ય છે.","giving an opinion","neutral"),("વધુ માહિતી જરૂરી છે.","requesting information","formal")]),("discussion","Discussion","💬",[("તમારી વાતમાં કંઈક સત્ય છે.","acknowledging a point","neutral"),("છતાં બીજો દૃષ્ટિકોણ પણ જોવો જોઈએ.","introducing another perspective","neutral"),("તેનું કારણ શું છે?","asking for a reason","neutral")])],
"B2":[("professional","Professional","📊",[("તમારી અરજીની તપાસ કરવામાં આવશે.","formal response","formal"),("કૃપા કરીને જરૂરી દસ્તાવેજો મોકલો.","requesting documents","formal"),("આ વિષય વિશે પછી જાણ કરવામાં આવશે.","promising an update","formal")]),("argument","Argumentation","⚖️",[("આ દાવા માટે પૂરતો પુરાવો છે.","supporting a claim","formal"),("જોકે, બીજું સમજૂતી પણ શક્ય છે.","introducing a counterpoint","formal"),("આ નિર્ણયના પરિણામો આવશે.","discussing implications","formal")])],
"C1":[("academic","Academic","🎓",[("ઉપલબ્ધ પુરાવા મુજબ...","qualifying a claim","formal"),("આ પરિણામનું અર્થઘટન સાવધાનીથી કરવું જોઈએ.","qualifying interpretation","formal"),("બીજી તરફ, વૈકલ્પિક સમજૂતી વિચારવી જોઈએ.","introducing an alternative","formal")]),("media","Media","📰",[("અધિકારીઓના જણાવ્યા મુજબ...","attributing information","formal"),("અહેવાલમાં જણાવ્યા મુજબ...","referring to a report","formal"),("આ ઘટનાની વ્યાપક અસર થઈ શકે છે.","discussing possible impact","formal")])],
"C2":[("rhetoric","Rhetoric","🎙️",[("આ દલીલની મુખ્ય મુશ્કેલી એ છે કે...","framing a critique","formal"),("આ વાંધાને સંપૂર્ણપણે અવગણી શકાય નહીં.","acknowledging an objection","formal"),("સંદર્ભ ધ્યાનમાં લેતા...","contextualizing a claim","formal")]),("formal-writing","Formal writing","📝",[("ઉપરોક્ત મુદ્દાઓના આધારે...","drawing a conclusion","formal"),("આને માત્ર તાત્કાલિક ઉકેલ તરીકે જ ગણવું જોઈએ.","limiting a conclusion","formal"),("આ વિષય પર વધુ સંશોધન જરૂરી છે.","calling for further research","formal")])],
}

CURRICULUM={}
for level in LEVELS:
    units=[]
    for i,(slug,title,*_) in enumerate(GRAMMAR_DATA[level],1):
        topic=VOCAB_DATA[level][(i-1)%len(VOCAB_DATA[level])][0]
        units.append(CurriculumUnit(
            id=f"gu-{level.lower()}-unit-{i}",level=level,unit_number=i,title=title,
            grammar_points=[slug],vocabulary_set_ids=[f"{topic}_{level.lower()}"],
            lesson_types=["grammar","vocabulary","listening","speaking","reading","writing"],
            competency_checklist=[f"Use {title.lower()} accurately","Apply the pattern in a short Gujarati exchange"],
            default_weeks=1 if level in ["A1","A2"] else 2))
    CURRICULUM[level]=units

GRAMMAR_TOPICS=[]
for level in LEVELS:
    for slug,title,category,summary,explanation,example in GRAMMAR_DATA[level]:
        GRAMMAR_TOPICS.append(GrammarTopic(slug=slug,title=title,level=level,category=category,summary=summary,explanation=explanation,examples=[GrammarExample(text=example)]))

VOCABULARY_SETS=[]
for level in LEVELS:
    for i,(topic,word,pos,definition,example) in enumerate(VOCAB_DATA[level],1):
        VOCABULARY_SETS.append(VocabularySet(id=f"{topic}_{level.lower()}",level=level,topic=topic,unit_ref=f"gu-{level.lower()}-unit-{i}",words=[VocabularyEntry(word=word,pos=pos,definition=definition,example=example)]))

PHRASEBOOK_CATEGORIES=[]
for level in LEVELS:
    for slug,situation,icon,entries in PHRASES[level]:
        PHRASEBOOK_CATEGORIES.append(PhrasebookCategory(id=f"gu-{slug}_{level.lower()}",level=level,situation=situation,icon=icon,phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in entries]))

ASSESSMENT_BANK=[
AssessmentQuestion(id="gu-a1-001",skill="grammar",difficulty="A1",question="Which sentence says 'My name is Anita'?",options=["મારું નામ અનિતા છે.","હું દરરોજ કામ કરું છું.","બજાર ક્યાં છે?","આ મારું ઘર છે."],correct="મારું નામ અનિતા છે.",grammar_slug="pronouns"),
AssessmentQuestion(id="gu-a2-001",skill="grammar",difficulty="A2",question="Which sentence expresses an action in progress?",options=["તે પુસ્તક વાંચી રહી છે.","હું ગઈકાલે ગયો.","હું કાલે આવીશ.","મારે ચા જોઈએ છે."],correct="તે પુસ્તક વાંચી રહી છે.",grammar_slug="progressive"),
AssessmentQuestion(id="gu-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["જો વરસાદ પડે તો આપણે ઘરે રહીશું.","મેં કામ પૂરું કર્યું છે.","તે પુસ્તક વાંચે છે.","તે મારો મિત્ર છે."],correct="જો વરસાદ પડે તો આપણે ઘરે રહીશું.",grammar_slug="conditional"),
AssessmentQuestion(id="gu-b2-001",skill="grammar",difficulty="B2",question="Which sentence contains an embedded question?",options=["તે ક્યાં ગયો તે મને ખબર નથી.","હું ઘરે જાઉં છું.","તે કામ કરે છે.","અમે ગઈકાલે મળ્યા."],correct="તે ક્યાં ગયો તે મને ખબર નથી.",grammar_slug="embedded"),
AssessmentQuestion(id="gu-c1-001",skill="reading",difficulty="C1",question="Which expression appropriately qualifies an academic claim?",options=["ઉપલબ્ધ પુરાવા મુજબ","નમસ્તે!","આ કેટલામાં છે?","જલ્દી આવો."],correct="ઉપલબ્ધ પુરાવા મુજબ",grammar_slug="hedging"),
AssessmentQuestion(id="gu-c2-001",skill="reading",difficulty="C2",question="Which sentence explicitly limits a conclusion?",options=["આને માત્ર તાત્કાલિક ઉકેલ તરીકે જ ગણવું જોઈએ.","નમસ્તે!","મારે પાણી જોઈએ છે.","ક્યાં જઈ રહ્યા છો?"],correct="આને માત્ર તાત્કાલિક ઉકેલ તરીકે જ ગણવું જોઈએ.",grammar_slug="lexical-precision"),
]

"""Հայերեն foundation data for JUBA LISAN — expanded A1-C2 content."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

A1_UNITS = [
    CurriculumUnit(id="hy-a1-unit-1", level="A1", unit_number=1, title="Ողջույններ", grammar_points=["basic-word-order"], vocabulary_set_ids=["greetings_a1"], lesson_types=["grammar","vocabulary","listening","speaking","reading","writing"], competency_checklist=["Greet people politely","Introduce a simple exchange"], default_weeks=1),
    CurriculumUnit(id="hy-a1-unit-2", level="A1", unit_number=2, title="Ինքնություն", grammar_points=["present"], vocabulary_set_ids=["identity_a1"], lesson_types=["grammar","vocabulary","listening","speaking","reading","writing"], competency_checklist=["Give personal information","Use the present tense"], default_weeks=1),
    CurriculumUnit(id="hy-a1-unit-3", level="A1", unit_number=3, title="Ընտանիք", grammar_points=["copula"], vocabulary_set_ids=["family_a1"], lesson_types=["grammar","vocabulary","listening","speaking","reading","writing"], competency_checklist=["Describe family members","Use the Armenian copula"], default_weeks=1),
    CurriculumUnit(id="hy-a1-unit-4", level="A1", unit_number=4, title="Տուն", grammar_points=["cases"], vocabulary_set_ids=["home_a1"], lesson_types=["grammar","vocabulary","listening","speaking","reading","writing"], competency_checklist=["Describe a home","Use basic case forms"], default_weeks=1),
    CurriculumUnit(id="hy-a1-unit-5", level="A1", unit_number=5, title="Առօրյա", grammar_points=["possession"], vocabulary_set_ids=["routine_a1"], lesson_types=["grammar","vocabulary","listening","speaking","reading","writing"], competency_checklist=["Describe a daily routine","Express possession"], default_weeks=1),
    CurriculumUnit(id="hy-a1-unit-6", level="A1", unit_number=6, title="Սնունդ", grammar_points=["questions"], vocabulary_set_ids=["food_a1"], lesson_types=["grammar","vocabulary","listening","speaking","reading","writing"], competency_checklist=["Order simple food","Ask basic questions"], default_weeks=1),
    CurriculumUnit(id="hy-a1-unit-7", level="A1", unit_number=7, title="Վայրեր", grammar_points=["negation"], vocabulary_set_ids=["places_a1"], lesson_types=["grammar","vocabulary","listening","speaking","reading","writing"], competency_checklist=["Ask for directions","Negate simple statements"], default_weeks=1),
    CurriculumUnit(id="hy-a1-unit-8", level="A1", unit_number=8, title="Ժամանակ", grammar_points=["plural"], vocabulary_set_ids=["time_a1"], lesson_types=["grammar","vocabulary","listening","speaking","reading","writing"], competency_checklist=["Talk about time","Recognise common plural forms"], default_weeks=1),
]

def _units(level, titles, grammar, vocab):
    return [
        CurriculumUnit(
            id=f"hy-{level.lower()}-unit-{i}",
            level=level,
            unit_number=i,
            title=title,
            grammar_points=[point],
            vocabulary_set_ids=[vocab_id],
            lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],
            competency_checklist=[f"Use {point} in context", f"Discuss {title} with level-appropriate Armenian"],
            default_weeks=2,
        )
        for i, (title, point, vocab_id) in enumerate(zip(titles, grammar, vocab), 1)
    ]

CURRICULUM = {"A1": A1_UNITS}
CURRICULUM["A2"] = _units(
    "A2",
    ["Օրակարգ և սովորություններ","Անցյալը","Ապագայի ծրագրեր","Գնումներ և ծառայություններ","Ճանապարհորդություն","Առողջություն"],
    ["past-imperfect","past-perfect","future","comparatives","motion-cases","necessity"],
    ["routine_a2","past_a2","future_a2","shopping_a2","travel_a2","health_a2"],
)
CURRICULUM["B1"] = _units(
    "B1",
    ["Փորձ և պատմություն","Պատճառ և հետևանք","Կարծիք և համաձայնություն","Աշխատանք","Կրթություն","Հասարակություն"],
    ["aspectual-past","causality","subordination","professional-communication","relative-clauses","conditionals"],
    ["experience_b1","causality_b1","opinions_b1","work_b1","education_b1","society_b1"],
)
CURRICULUM["B2"] = _units(
    "B2",
    ["Փաստարկում","Պաշտոնական հաղորդակցություն","Զեկուցված խոսք","Բարդ ժամանակաձևեր","Հանրային խնդիրներ","Մեդիա"],
    ["complex-subordination","formal-register","reported-speech","verbal-periphrases","discourse-markers","media-language"],
    ["argument_b2","formal_b2","reported_b2","complex-verbs_b2","issues_b2","media_b2"],
)
CURRICULUM["C1"] = _units(
    "C1",
    ["Ակադեմիական խոսք","Վերլուծություն","Քաղաքականություն և հասարակություն","Գիտություն և տեխնոլոգիա","Մշակույթ","Մասնագիտական գրություն"],
    ["nominalization","hedging","information-structure","academic-connectors","stylistic-register","professional-writing"],
    ["academic_c1","analysis_c1","civic_c1","science_c1","culture_c1","professional-writing_c1"],
)
CURRICULUM["C2"] = _units(
    "C2",
    ["Նրբերանգ և ենթատեքստ","Հռետորաբանություն","Գրական ոճ","Բանավեճ","Թարգմանական ճշգրտություն","Լեզվական վարպետություն"],
    ["pragmatics","rhetoric","literary-style","debate-register","translation-equivalence","idiomatic-nuance"],
    ["nuance_c2","rhetoric_c2","literature_c2","debate_c2","translation_c2","mastery_c2"],
)

def _topic(slug, title, level, category, explanation, examples):
    return GrammarTopic(slug=slug, title=title, level=level, category=category, summary=explanation, explanation=explanation, examples=[GrammarExample(text=e) for e in examples])

GRAMMAR_TOPICS = [
    _topic("basic-word-order","Basic Armenian word order","A1","syntax","Use common subject-object-verb patterns while recognising Armenian word-order flexibility.",["Ես գիրք եմ կարդում։","Նա այստեղ է։"]),
    _topic("present","Present tense","A1","verbs","Use the present indicative and present forms of եմ with everyday verbs.",["Ես աշխատում եմ։","Նա սովորում է։"]),
    _topic("copula","Copula եմ","A1","grammar","Use եմ, ես, է and related forms for identity and description.",["Ես ուսանող եմ։","Նա բժիշկ է։"]),
    _topic("cases","Basic case forms","A1","morphology","Recognise common Armenian case endings in location and object phrases.",["Ես տանն եմ։","Գիրքը սեղանի վրա է։"]),
    _topic("possession","Possession","A1","grammar","Express possession with ունեմ and possessive forms.",["Ես գիրք ունեմ։","Սա իմ տունն է։"]),
    _topic("questions","Question patterns","A1","syntax","Form information questions with ով, ինչ, որտեղ, երբ and ինչպես.",["Որտե՞ղ ես։","Ինչպե՞ս ես։"]),
    _topic("negation","Negation","A1","syntax","Negate present statements with չեմ, չես, չէ and related forms.",["Ես չեմ աշխատում։","Նա այստեղ չէ։"]),
    _topic("plural","Plural nouns","A1","morphology","Form common plurals, including -ներ and irregular lexical patterns.",["Ընկերները այստեղ են։","Երեխաները խաղում են։"]),
    _topic("past-imperfect","Imperfect and simple past","A2","verbs","Talk about completed and ongoing past situations using Armenian past forms.",["Երեկ աշխատում էի։","Նա երեկ եկավ։"]),
    _topic("past-perfect","Pluperfect and anteriority","A2","verbs","Place one past event before another past reference point.",["Մինչև նրա գալը ես արդեն գնացել էի։"]),
    _topic("future","Future and intention","A2","verbs","Express future events, plans and expectations with Armenian future constructions.",["Վաղը կգնամ Երևան։","Մենք կաշխատենք միասին։"]),
    _topic("comparatives","Comparatives and superlatives","A2","adjectives","Compare people, objects and situations naturally.",["Այս ճանապարհը ավելի կարճ է։","Սա ամենալավ տարբերակն է։"]),
    _topic("motion-cases","Motion and case government","A2","morphology","Use direction and location forms with գնալ, գալ, մտնել and դուրս գալ.",["Գնում եմ դպրոց։","Մտա սենյակ։"]),
    _topic("necessity","Necessity and obligation","A2","modality","Express need, obligation and permission in everyday situations.",["Պետք է աշխատեմ։","Կարո՞ղ եմ ներս մտնել։"]),
    _topic("aspectual-past","Past viewpoint and aspectual meaning","B1","verbs","Distinguish repeated, ongoing and completed events through Armenian tense-aspect choices.",["Ամեն օր կարդում էի։","Գիրքը կարդացի երեկ։"]),
    _topic("causality","Cause and consequence","B1","syntax","Connect causes and consequences with որովհետև, քանի որ, այդ պատճառով and related structures.",["Չեկա, որովհետև հիվանդ էի։","Անձրև էր գալիս, այդ պատճառով մնացինք տանը։"]),
    _topic("subordination","Subordinate clauses","B1","syntax","Build temporal, causal and concessive subordinate clauses.",["Երբ հասնեմ, կզանգեմ։","Թեև հոգնած էր, շարունակեց։"]),
    _topic("professional-communication","Professional communication","B1","register","Use polite requests, proposals and workplace interaction.",["Կարո՞ղ եք ուղարկել փաստաթուղթը։","Առաջարկում եմ հանդիպել վաղը։"]),
    _topic("relative-clauses","Relative clauses","B1","syntax","Describe people and things with որ and related relative-clause patterns.",["Գիրքը, որը կարդում եմ, հետաքրքիր է։"]),
    _topic("conditionals","Conditionals","B1","syntax","Express real and hypothetical conditions.",["Եթե ժամանակ ունենամ, կգամ։","Եթե ավելի շուտ գայի, կհանդիպեինք։"]),
    _topic("complex-subordination","Complex subordination","B2","syntax","Combine multiple subordinate clauses without losing reference clarity.",["Չնայած նրան, որ ուշ էր, նա շարունակեց աշխատել։"]),
    _topic("formal-register","Formal Armenian register","B2","register","Shift from conversational Armenian to formal administrative and professional style.",["Խնդրում ենք ներկայացնել անհրաժեշտ փաստաթղթերը։"]),
    _topic("reported-speech","Reported speech","B2","syntax","Report statements, questions and instructions while controlling tense and reference.",["Նա ասաց, որ վաղը կգա։"]),
    _topic("verbal-periphrases","Complex verbal constructions","B2","verbs","Use auxiliary and periphrastic constructions for nuanced temporal and modal meaning.",["Պետք է շարունակենք քննարկումը։","Նա սկսեց աշխատել։"]),
    _topic("discourse-markers","Discourse organisation","B2","discourse","Organise arguments with սակայն, այնուամենայնիվ, հետևաբար, մինչդեռ and similar markers.",["Սակայն խնդիրը դեռ լուծված չէ։","Հետևաբար, պետք է վերանայել ծրագիրը։"]),
    _topic("media-language","Media language","B2","register","Interpret headlines, formal reports and public commentary.",["Ըստ հաղորդագրության՝ հանդիպումը տեղի կունենա այսօր։"]),
    _topic("nominalization","Academic nominalization","C1","academic","Convert propositions into compact nominal structures typical of academic Armenian.",["Ծրագրի իրականացումը պահանջում է ժամանակ։"]),
    _topic("hedging","Academic hedging","C1","academic","Qualify claims with evidence-sensitive expressions rather than absolute assertions.",["Այս արդյունքը կարող է վկայել որոշակի միտման մասին։"]),
    _topic("information-structure","Information structure","C1","discourse","Control emphasis, topic and focus for precise written and spoken communication.",["Հենց այս հարցն է կարևոր։"]),
    _topic("academic-connectors","Academic connective system","C1","academic","Build coherent multi-paragraph arguments with formal connective phrases.",["Մի կողմից՝ արդյունքները դրական են, մյուս կողմից՝ սահմանափակումներ կան։"]),
    _topic("stylistic-register","Stylistic register","C1","style","Adapt vocabulary and syntax to academic, journalistic, professional and literary contexts.",["Հետազոտությունը ցույց է տալիս էական տարբերություն։"]),
    _topic("professional-writing","Professional writing","C1","writing","Write precise reports, proposals and formal correspondence.",["Կից ներկայացվում է հաշվետվության վերջնական տարբերակը։"]),
    _topic("pragmatics","Pragmatic nuance","C2","pragmatics","Interpret implied meaning, politeness, stance and context-dependent choices.",["Կարծում եմ՝ կարելի է վերանայել այս տարբերակը։"]),
    _topic("rhetoric","Rhetorical Armenian","C2","rhetoric","Use parallelism, contrast and controlled emphasis in persuasive speech and writing.",["Խնդիրը ոչ միայն տնտեսական է, այլև սոցիալական։"]),
    _topic("literary-style","Literary style","C2","style","Recognise and produce sophisticated literary syntax, imagery and register shifts.",["Քաղաքը արթնանում էր լույսի առաջին շողերի հետ։"]),
    _topic("debate-register","Advanced debate register","C2","rhetoric","Present counterarguments, concessions and precise rebuttals.",["Թեև այս տեսակետը համոզիչ է, այն անտեսում է մեկ կարևոր հանգամանք։"]),
    _topic("translation-equivalence","Translation equivalence","C2","translation","Choose Armenian structures that preserve meaning, tone and pragmatic force across languages.",["Բառացի թարգմանությունը միշտ չէ, որ փոխանցում է իմաստային նրբերանգը։"]),
    _topic("idiomatic-nuance","Idiomatic and pragmatic nuance","C2","lexis","Interpret idioms, collocations and culturally marked expressions from context.",["Այս արտահայտությունը բառացի իմաստով չի գործածվում։"]),
]

def _vset(id_, level, topic, unit_ref, entries):
    return VocabularySet(id=id_, level=level, topic=topic, unit_ref=unit_ref, words=[
        VocabularyEntry(word=w, pos=p, definition=d, example=e) for w,p,d,e in entries
    ])

VOCABULARY_SETS = [
    _vset("greetings_a1","A1","Ողջույններ","hy-a1-unit-1",[("բարև","interjection","hello","Բարև, ինչպե՞ս ես։"),("ցտեսություն","interjection","goodbye","Ցտեսություն, մինչև վաղը։"),("շնորհակալություն","noun","thank you","Շնորհակալություն օգնության համար։"),("խնդրում եմ","phrase","please / you're welcome","Խնդրում եմ, նստեք։")]),
    _vset("identity_a1","A1","Ինքնություն","hy-a1-unit-2",[("անուն","noun","name","Իմ անունը Անի է։"),("մարդ","noun","person","Նա լավ մարդ է։"),("ուսանող","noun","student","Ես ուսանող եմ։"),("ընկեր","noun","friend","Նա իմ ընկերն է։")]),
    _vset("family_a1","A1","Ընտանիք","hy-a1-unit-3",[("մայր","noun","mother","Մայրս տանն է։"),("հայր","noun","father","Հայրս աշխատում է։"),("եղբայր","noun","brother","Եղբայրս ուսանող է։"),("քույր","noun","sister","Քույրս դպրոցում է։")]),
    _vset("home_a1","A1","Տուն","hy-a1-unit-4",[("տուն","noun","home/house","Իմ տունը մեծ չէ։"),("սենյակ","noun","room","Սենյակը լուսավոր է։"),("դուռ","noun","door","Դուռը բաց է։"),("խոհանոց","noun","kitchen","Խոհանոցը փոքր է։")]),
    _vset("routine_a1","A1","Առօրյա","hy-a1-unit-5",[("առավոտ","noun","morning","Առավոտյան շուտ եմ արթնանում։"),("աշխատանք","noun","work","Ես աշխատանքի եմ գնում։"),("դպրոց","noun","school","Երեխան դպրոց է գնում։"),("քնել","verb","to sleep","Ես ժամը տասնմեկին եմ քնում։")]),
    _vset("food_a1","A1","Սնունդ","hy-a1-unit-6",[("հաց","noun","bread","Հաց եմ ուզում։"),("ջուր","noun","water","Մի բաժակ ջուր, խնդրում եմ։"),("կաթ","noun","milk","Կաթը սառը է։"),("սուրճ","noun","coffee","Առավոտյան սուրճ եմ խմում։")]),
    _vset("places_a1","A1","Վայրեր","hy-a1-unit-7",[("խանութ","noun","shop","Խանութը մոտ է։"),("կայարան","noun","station","Կայարանը որտե՞ղ է։"),("փողոց","noun","street","Այս փողոցը երկար է։"),("քաղաք","noun","city","Ես քաղաքում եմ ապրում։")]),
    _vset("time_a1","A1","Ժամանակ","hy-a1-unit-8",[("այսօր","adverb","today","Այսօր աշխատում եմ։"),("վաղը","adverb","tomorrow","Վաղը կգամ։"),("հիմա","adverb","now","Հիմա զբաղված եմ։"),("ժամ","noun","hour/time","Քանի՞ ժամ է։")]),
    _vset("routine_a2","A2","Սովորություններ","hy-a2-unit-1",[("արթնանալ","verb","to wake up","Ես ժամը յոթին եմ արթնանում։"),("սովորաբար","adverb","usually","Ես սովորաբար տանը եմ աշխատում։"),("զբաղվել","verb","to engage in","Ազատ ժամանակ սպորտով եմ զբաղվում։"),("հանգստանալ","verb","to rest","Կիրակի օրը հանգստանում եմ։")]),
    _vset("past_a2","A2","Անցյալ","hy-a2-unit-2",[("երեկ","adverb","yesterday","Երեկ տանը էի։"),("անցյալ","adjective","past/previous","Անցյալ շաբաթ զբաղված էի։"),("հանդիպել","verb","to meet","Երեկ ընկերոջս հանդիպեցի։"),("վերադառնալ","verb","to return","Երեկ ուշ վերադարձա։")]),
    _vset("future_a2","A2","Ապագա","hy-a2-unit-3",[("ծրագիր","noun","plan","Վաղվա ծրագրերը պատրաստ են։"),("որոշել","verb","to decide","Որոշել եմ վաղը գնալ։"),("կհանդիպենք","verb","we will meet","Վաղը կհանդիպենք։"),("հաջորդ","adjective","next","Հաջորդ շաբաթ կսկսենք։")]),
    _vset("shopping_a2","A2","Գնումներ","hy-a2-unit-4",[("գին","noun","price","Այս ապրանքի գինը բարձր է։"),("զեղչ","noun","discount","Այսօր զեղչ կա։"),("ապրանք","noun","product","Ապրանքը որակյալ է։"),("վճարել","verb","to pay","Կարո՞ղ եմ քարտով վճարել։")]),
    _vset("travel_a2","A2","Ճանապարհորդություն","hy-a2-unit-5",[("ուղևորություն","noun","trip","Ուղևորությունը երկար էր։"),("տոմս","noun","ticket","Երկու տոմս եմ ուզում։"),("ուղեբեռ","noun","luggage","Ուղեբեռս ծանր է։"),("մեկնել","verb","to depart","Գնացքը ժամը ութին է մեկնում։")]),
    _vset("health_a2","A2","Առողջություն","hy-a2-unit-6",[("առողջություն","noun","health","Առողջությունը կարևոր է։"),("ցավ","noun","pain","Գլուխս ցավում է։"),("բժիշկ","noun","doctor","Բժշկի մոտ եմ գնում։"),("դեղ","noun","medicine","Դեղը օրը երկու անգամ ընդունեք։")]),
    _vset("experience_b1","B1","Փորձ","hy-b1-unit-1",[("փորձ","noun","experience","Այս աշխատանքը լավ փորձ էր։"),("հիշել","verb","to remember","Լավ եմ հիշում այդ օրը։"),("սովորել","verb","to learn","Այս փորձից շատ բան սովորեցի։"),("հաջողություն","noun","success","Նախագիծը հաջողություն ունեցավ։")]),
    _vset("causality_b1","B1","Պատճառ և հետևանք","hy-b1-unit-2",[("պատճառ","noun","reason/cause","Խնդրի պատճառը պարզ չէ։"),("հետևանք","noun","consequence","Որոշման հետևանքները կարևոր են։"),("ազդել","verb","to affect","Որոշումը ազդում է բոլորի վրա։"),("արդյունքում","adverb","as a result","Արդյունքում ժամանակ խնայեցինք։")]),
    _vset("opinions_b1","B1","Կարծիք","hy-b1-unit-3",[("կարծիք","noun","opinion","Իմ կարծիքով՝ սա կարևոր է։"),("համաձայնել","verb","to agree","Ես համաձայն եմ ձեզ հետ։"),("վիճել","verb","to argue","Նրանք երկար վիճեցին։"),("տեսակետ","noun","viewpoint","Նրա տեսակետը հետաքրքիր է։")]),
    _vset("work_b1","B1","Աշխատանք","hy-b1-unit-4",[("աշխատակից","noun","employee/colleague","Նա մեր նոր աշխատակիցն է։"),("պարտականություն","noun","responsibility","Սա իմ հիմնական պարտականությունն է։"),("հանդիպում","noun","meeting","Հանդիպումը ժամը տասին է։"),("առաջարկել","verb","to propose","Նա նոր լուծում առաջարկեց։")]),
    _vset("education_b1","B1","Կրթություն","hy-b1-unit-5",[("կրթություն","noun","education","Կրթությունը կարևոր ներդրում է։"),("հետազոտություն","noun","research","Նա հետազոտություն է կատարում։"),("գիտելիք","noun","knowledge","Գիտելիքը պետք է կիրառել։"),("քննություն","noun","exam","Քննությունը հաջորդ շաբաթ է։")]),
    _vset("society_b1","B1","Հասարակություն","hy-b1-unit-6",[("հասարակություն","noun","society","Հասարակությունը արագ է փոխվում։"),("համայնք","noun","community","Համայնքը միասին աշխատեց։"),("քաղաքացի","noun","citizen","Յուրաքանչյուր քաղաքացի ունի իրավունքներ։"),("միջավայր","noun","environment/context","Աշխատանքային միջավայրը բարելավվեց։")]),
    _vset("argument_b2","B2","Փաստարկում","hy-b2-unit-1",[("փաստարկ","noun","argument","Նա ներկայացրեց ուժեղ փաստարկ։"),("ապացույց","noun","evidence","Անհրաժեշտ է լրացուցիչ ապացույց։"),("ենթադրել","verb","to assume","Չպետք է առանց տվյալների ենթադրել։"),("հակափաստարկ","noun","counterargument","Նա ներկայացրեց հակափաստարկ։")]),
    _vset("formal_b2","B2","Պաշտոնական խոսք","hy-b2-unit-2",[("պաշտոնական","adjective","official/formal","Պաշտոնական նամակն ուղարկվել է։"),("դիմում","noun","application","Դիմումը պետք է ստորագրել։"),("պահանջ","noun","requirement/demand","Պահանջները հստակ են։"),("ներկայացնել","verb","to submit/present","Խնդրում ենք ներկայացնել փաստաթուղթը։")]),
    _vset("reported_b2","B2","Զեկուցված խոսք","hy-b2-unit-3",[("հայտարարել","verb","to announce","Նախարարը հայտարարեց փոփոխության մասին։"),("պնդել","verb","to claim","Նա պնդում է, որ ճիշտ է։"),("տեղեկացնել","verb","to inform","Նրանք տեղեկացրին, որ հանդիպումը հետաձգվել է։"),("նշել","verb","to note","Զեկույցը նշում է հիմնական խնդիրները։")]),
    _vset("complex-verbs_b2","B2","Բարդ բայեր","hy-b2-unit-4",[("շարունակել","verb","to continue","Նա շարունակեց աշխատել։"),("սկսել","verb","to begin","Նրանք սկսեցին քննարկել հարցը։"),("կարողանալ","verb","to be able","Մենք կարողացանք լուծել խնդիրը։"),("պետք է","modal","must/should","Պետք է ավարտենք աշխատանքը։")]),
    _vset("issues_b2","B2","Հանրային խնդիրներ","hy-b2-unit-5",[("խնդիր","noun","issue/problem","Խնդիրը բարդ է։"),("քաղաքականություն","noun","policy/politics","Նոր քաղաքականությունը քննարկվում է։"),("զարգացում","noun","development","Տարածաշրջանի զարգացումը կարևոր է։"),("ռեսուրս","noun","resource","Ռեսուրսները սահմանափակ են։")]),
    _vset("media_b2","B2","Մեդիա","hy-b2-unit-6",[("լրատվամիջոց","noun","media outlet","Լրատվամիջոցները տարածեցին լուրը։"),("հաղորդագրություն","noun","statement/message","Պաշտոնական հաղորդագրությունը հրապարակվեց։"),("վերլուծություն","noun","analysis","Հոդվածը մանրամասն վերլուծություն է։"),("աղբյուր","noun","source","Աղբյուրը պետք է ստուգել։")]),
    _vset("academic_c1","C1","Ակադեմիական բառապաշար","hy-c1-unit-1",[("մեթոդաբանություն","noun","methodology","Հետազոտության մեթոդաբանությունը հստակ է։"),("եզրակացություն","noun","conclusion","Եզրակացությունը հիմնված է տվյալների վրա։"),("մոտեցում","noun","approach","Այս մոտեցումն արդյունավետ է։"),("վարկած","noun","hypothesis","Վարկածը պետք է ստուգել։")]),
    _vset("analysis_c1","C1","Վերլուծություն","hy-c1-unit-2",[("համեմատել","verb","to compare","Ուսումնասիրությունը համեմատում է երկու մեթոդ։"),("գնահատել","verb","to evaluate","Պետք է գնահատել արդյունքները։"),("միտում","noun","trend","Տվյալները ցույց են տալիս միտում։"),("փոխկապակցված","adjective","interrelated","Գործոնները փոխկապակցված են։")]),
    _vset("civic_c1","C1","Հասարակական կյանք","hy-c1-unit-3",[("իրավունք","noun","right","Քաղաքացիների իրավունքները պաշտպանված են։"),("պարտավորություն","noun","obligation","Օրենքը սահմանում է պարտավորություններ։"),("մասնակցություն","noun","participation","Հանրային մասնակցությունը կարևոր է։"),("թափանցիկություն","noun","transparency","Թափանցիկությունը բարձրացնում է վստահությունը։")]),
    _vset("science_c1","C1","Գիտություն և տեխնոլոգիա","hy-c1-unit-4",[("տեխնոլոգիա","noun","technology","Նոր տեխնոլոգիաները փոխում են ոլորտը։"),("տվյալներ","noun","data","Տվյալները վերլուծվել են։"),("նորարարություն","noun","innovation","Նորարարությունը կարող է բարձրացնել արդյունավետությունը։"),("ալգորիթմ","noun","algorithm","Ալգորիթմը մշակվել է տվյալների մշակման համար։")]),
    _vset("culture_c1","C1","Մշակույթ","hy-c1-unit-5",[("ժառանգություն","noun","heritage","Մշակութային ժառանգությունը պահպանվում է։"),("ինքնություն","noun","identity","Լեզուն մշակութային ինքնության մաս է։"),("ավանդույթ","noun","tradition","Այս ավանդույթը սերունդներով փոխանցվել է։"),("ստեղծագործություն","noun","creative work","Ստեղծագործությունը մեծ ազդեցություն ունեցավ։")]),
    _vset("professional-writing_c1","C1","Մասնագիտական գրություն","hy-c1-unit-6",[("հաշվետվություն","noun","report","Հաշվետվությունը պատրաստ է։"),("առաջարկություն","noun","proposal","Առաջարկությունը ներկայացվել է ղեկավարությանը։"),("կցել","verb","to attach","Խնդրում ենք կցել անհրաժեշտ ֆայլերը։"),("վերջնաժամկետ","noun","deadline","Վերջնաժամկետը ուրբաթ է։")]),
    _vset("nuance_c2","C2","Նրբերանգ","hy-c2-unit-1",[("ենթատեքստ","noun","subtext","Խոսքի ենթատեքստը պետք է հաշվի առնել։"),("նրբերանգ","noun","nuance","Թարգմանության մեջ կարևոր նրբերանգ կա։"),("ակնարկ","noun","hint/allusion","Նա ակնարկեց խնդրի մասին։"),("երկիմաստություն","noun","ambiguity","Այս նախադասությունը երկիմաստություն ունի։")]),
    _vset("rhetoric_c2","C2","Հռետորաբանություն","hy-c2-unit-2",[("հռետորաբանություն","noun","rhetoric","Ելույթը ուժեղ հռետորաբանություն ուներ։"),("համոզիչ","adjective","persuasive","Նրա փաստարկը համոզիչ էր։"),("զուգահեռություն","noun","parallelism","Հռետորական զուգահեռությունը շեշտադրում է գաղափարը։"),("հակադրություն","noun","contrast","Հեղինակը օգտագործում է հակադրություն։")]),
    _vset("literature_c2","C2","Գրականություն","hy-c2-unit-3",[("փոխաբերություն","noun","metaphor","Տեքստը հարուստ է փոխաբերություններով։"),("պատկերավոր","adjective","figurative","Պատկերավոր լեզուն ուժեղ է։"),("պատմողական","adjective","narrative","Պատմողական ոճը դանդաղ է զարգանում։"),("բառախաղ","noun","wordplay","Հեղինակը օգտագործում է բառախաղ։")]),
    _vset("debate_c2","C2","Բանավեճ","hy-c2-unit-4",[("առարկություն","noun","objection","Նա ներկայացրեց հիմնավորված առարկություն։"),("զիջում","noun","concession","Զիջումը չի նշանակում հրաժարվել հիմնական դիրքորոշումից։"),("հերքել","verb","to refute","Տվյալները հերքում են այդ պնդումը։"),("վերապահում","noun","qualification/reservation","Նա համաձայնեց որոշ վերապահումներով։")]),
    _vset("translation_c2","C2","Թարգմանություն","hy-c2-unit-5",[("համարժեքություն","noun","equivalence","Թարգմանության մեջ իմաստային համարժեքությունը կարևոր է։"),("գրանցամատյան","noun","register","Թարգմանիչը պետք է պահպանի գրանցամատյանը։"),("բարբառ","noun","dialect","Տեքստում օգտագործվում է բարբառային բառապաշար։"),("հարմարվել","verb","to adapt","Արտահայտությունը պետք է հարմարեցնել համատեքստին։")]),
    _vset("mastery_c2","C2","Լեզվական վարպետություն","hy-c2-unit-6",[("ճշգրտություն","noun","precision","Գիտական գրության մեջ ճշգրտությունը կարևոր է։"),("սահունություն","noun","fluency","Խոսքի սահունությունը բարելավվեց։"),("կապակցվածություն","noun","cohesion","Տեքստի կապակցվածությունը բարձր է։"),("ոճական","adjective","stylistic","Ընտրությունը ունի ոճական հետևանքներ։")]),
]

PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id="greetings_a1", level="A1", situation="Ողջույններ", icon="💬", phrases=[PhrasebookEntry(text="Բարև։",context="greeting",register="neutral"),PhrasebookEntry(text="Ինչպե՞ս եք։",context="polite greeting",register="polite"),PhrasebookEntry(text="Շնորհակալություն։",context="thanks",register="neutral"),PhrasebookEntry(text="Ցտեսություն։",context="farewell",register="neutral")]),
    PhrasebookCategory(id="help_a1", level="A1", situation="Օգնություն", icon="🆘", phrases=[PhrasebookEntry(text="Օգնեք ինձ, խնդրում եմ։",context="request",register="neutral"),PhrasebookEntry(text="Որտե՞ղ է զուգարանը։",context="location",register="neutral"),PhrasebookEntry(text="Չեմ հասկանում։",context="clarification",register="neutral"),PhrasebookEntry(text="Խնդրում եմ, կրկնեք։",context="repeat",register="polite")]),
    PhrasebookCategory(id="shopping_a1", level="A1", situation="Գնումներ", icon="🛍️", phrases=[PhrasebookEntry(text="Որքա՞ն արժե։",context="price",register="neutral"),PhrasebookEntry(text="Սա եմ ուզում։",context="purchase",register="neutral"),PhrasebookEntry(text="Կարո՞ղ եմ քարտով վճարել։",context="payment",register="polite")]),
    PhrasebookCategory(id="travel_a1", level="A1", situation="Ճանապարհորդություն", icon="🚌", phrases=[PhrasebookEntry(text="Որտե՞ղ է կայարանը։",context="directions",register="neutral"),PhrasebookEntry(text="Մի տոմս եմ ուզում։",context="ticket",register="neutral"),PhrasebookEntry(text="Ո՞ր ժամին է մեկնում գնացքը։",context="schedule",register="neutral")]),
    PhrasebookCategory(id="work_b1", level="B1", situation="Աշխատավայր", icon="💼", phrases=[PhrasebookEntry(text="Կարո՞ղ եք ուղարկել փաստաթուղթը։",context="request",register="polite"),PhrasebookEntry(text="Առաջարկում եմ քննարկել այս հարցը։",context="proposal",register="formal"),PhrasebookEntry(text="Եկեք պայմանավորվենք հանդիպման մասին։",context="scheduling",register="neutral")]),
    PhrasebookCategory(id="formal_b2", level="B2", situation="Պաշտոնական հաղորդակցություն", icon="📄", phrases=[PhrasebookEntry(text="Խնդրում ենք ներկայացնել անհրաժեշտ փաստաթղթերը։",context="formal request",register="formal"),PhrasebookEntry(text="Կից ներկայացվում է հաշվետվությունը։",context="formal attachment",register="formal"),PhrasebookEntry(text="Շնորհակալություն համագործակցության համար։",context="formal closing",register="formal")]),
    PhrasebookCategory(id="academic_c1", level="C1", situation="Ակադեմիական խոսք", icon="🎓", phrases=[PhrasebookEntry(text="Տվյալները վկայում են այն մասին, որ…",context="evidence",register="formal"),PhrasebookEntry(text="Այս արդյունքը կարող է վկայել…",context="hedging",register="formal"),PhrasebookEntry(text="Մի կողմից՝ …, մյուս կողմից՝ …",context="balanced argument",register="formal")]),
    PhrasebookCategory(id="debate_c2", level="C2", situation="Բանավեճ", icon="🗣️", phrases=[PhrasebookEntry(text="Թեև այս տեսակետը համոզիչ է, այն անտեսում է…",context="counterargument",register="formal"),PhrasebookEntry(text="Այդ պնդումը պահանջում է լրացուցիչ հիմնավորում։",context="challenge",register="formal"),PhrasebookEntry(text="Այս հարցում անհրաժեշտ է տարբերակել երկու մակարդակ։",context="distinction",register="formal")]),
]

ASSESSMENT_BANK = [
    AssessmentQuestion(id="hy-a1-001",skill="communication",difficulty="A1",question="Which Armenian phrase means “Hello”?",options=["Բարև","Շնորհակալություն","Ցտեսություն","Խնդրում եմ"],correct="Բարև"),
    AssessmentQuestion(id="hy-a1-002",skill="grammar",difficulty="A1",question="Which sentence says “I am a student”?",options=["Ես ուսանող եմ։","Ես տանն եմ։","Նա իմ ընկերն է։","Մայրս տանն է։"],correct="Ես ուսանող եմ։"),
    AssessmentQuestion(id="hy-a1-003",skill="vocabulary",difficulty="A1",question="Which word means “mother”?",options=["մայր","հայր","եղբայր","քույր"],correct="մայր"),
    AssessmentQuestion(id="hy-a1-004",skill="grammar",difficulty="A1",question="Which sentence expresses possession?",options=["Ես գիրք ունեմ։","Ես սովորում եմ։","Դուռը բաց է։","Ցտեսություն։"],correct="Ես գիրք ունեմ։"),
    AssessmentQuestion(id="hy-a1-005",skill="vocabulary",difficulty="A1",question="Which word means “water”?",options=["ջուր","հաց","սուրճ","գին"],correct="ջուր"),
    AssessmentQuestion(id="hy-a1-006",skill="communication",difficulty="A1",question="How do you ask “How much is it?”",options=["Որքա՞ն արժե։","Կայարանը որտե՞ղ է։","Ինչպե՞ս ես։","Ցտեսություն։"],correct="Որքա՞ն արժե։"),
    AssessmentQuestion(id="hy-a2-001",skill="grammar",difficulty="A2",question="Which sentence expresses a future event?",options=["Վաղը կգնամ Երևան։","Երեկ գնացի Երևան։","Հիմա Երևանում եմ։","Երեկ տանն էի։"],correct="Վաղը կգնամ Երևան։"),
    AssessmentQuestion(id="hy-a2-002",skill="vocabulary",difficulty="A2",question="Which word means “discount”?",options=["զեղչ","տոմս","ցավ","կայարան"],correct="զեղչ"),
    AssessmentQuestion(id="hy-b1-001",skill="grammar",difficulty="B1",question="Which connector introduces a cause?",options=["քանի որ","սակայն","հետևաբար","մինչդեռ"],correct="քանի որ"),
    AssessmentQuestion(id="hy-b1-002",skill="communication",difficulty="B1",question="Which is a polite workplace request?",options=["Կարո՞ղ եք ուղարկել փաստաթուղթը։","Գնա՛ հիմա։","Չեմ ուզում։","Ցտեսություն։"],correct="Կարո՞ղ եք ուղարկել փաստաթուղթը։"),
    AssessmentQuestion(id="hy-b2-001",skill="grammar",difficulty="B2",question="Which sentence reports another person's statement?",options=["Նա ասաց, որ վաղը կգա։","Նա վաղը կգա։","Ես այսօր աշխատում եմ։","Նա երեկ եկավ։"],correct="Նա ասաց, որ վաղը կգա։"),
    AssessmentQuestion(id="hy-b2-002",skill="register",difficulty="B2",question="Which phrase is most appropriate for a formal request?",options=["Խնդրում ենք ներկայացնել անհրաժեշտ փաստաթղթերը։","Արի այստեղ։","Ի՞նչ կա։","Հետո կխոսենք։"],correct="Խնդրում ենք ներկայացնել անհրաժեշտ փաստաթղթերը։"),
    AssessmentQuestion(id="hy-c1-001",skill="academic",difficulty="C1",question="Which phrase appropriately hedges an academic claim?",options=["Այս արդյունքը կարող է վկայել որոշակի միտման մասին։","Սա հաստատ միշտ ճիշտ է։","Բոլորը սխալ են։","Ես պարզապես կարծում եմ։"],correct="Այս արդյունքը կարող է վկայել որոշակի միտման մասին։"),
    AssessmentQuestion(id="hy-c1-002",skill="academic",difficulty="C1",question="Which word means “methodology”?",options=["մեթոդաբանություն","ժառանգություն","վերջնաժամկետ","բառախաղ"],correct="մեթոդաբանություն"),
    AssessmentQuestion(id="hy-c2-001",skill="pragmatics",difficulty="C2",question="Which concept concerns implied meaning beyond the literal wording?",options=["ենթատեքստ","տոմս","ուղեբեռ","զեղչ"],correct="ենթատեքստ"),
    AssessmentQuestion(id="hy-c2-002",skill="rhetoric",difficulty="C2",question="Which sentence introduces a concession and counterargument?",options=["Թեև այս տեսակետը համոզիչ է, այն անտեսում է մեկ կարևոր հանգամանք։","Ես այսօր աշխատում եմ։","Վաղը կգամ։","Բարև։"],correct="Թեև այս տեսակետը համոզիչ է, այն անտեսում է մեկ կարևոր հանգամանք։"),
]

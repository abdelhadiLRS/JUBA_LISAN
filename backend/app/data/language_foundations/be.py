"""Belarusian A1-C2 curriculum data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]
def _g(slug,title,level,summary,example):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=summary,explanation=f"Practice {title.lower()} in authentic Belarusian contexts.",examples=[GrammarExample(text=example)])

GRAMMAR_TOPICS=[
_g("a1-pronouns","Personal pronouns","A1","Use personal pronouns in everyday exchanges.","Я вучань."),
_g("a1-nominal","Nominal sentences","A1","Identify people and objects.","Гэта мой дом."),
_g("a1-present","Present tense","A1","Describe current and habitual actions.","Я вывучаю беларускую мову."),
_g("a1-questions","Basic questions","A1","Ask practical questions.","Як ты?"),
_g("a1-negation","Negation","A1","Form simple negative statements.","Я не разумею."),
_g("a1-demonstratives","Demonstratives","A1","Point to people and objects.","Гэта мая кніга."),
_g("a1-possessive","Possessive forms","A1","Express ownership and relationships.","Гэта мая маці."),
_g("a1-location","Location and prepositions","A1","Describe where things are.","Кніга на стале."),
_g("a2-gender","Gender and agreement","A2","Use grammatical gender and agreement.","Новая кніга ляжыць на стале."),
_g("a2-cases","Nominative, accusative and genitive","A2","Use core cases in everyday contexts.","Я бачу брата."),
_g("a2-dative","Dative and instrumental","A2","Express recipients and means.","Я даю брату кнігу."),
_g("a2-past","Past tense","A2","Talk about completed past events.","Учора я быў дома."),
_g("a2-future","Future constructions","A2","Talk about plans and future events.","Заўтра я буду вучыцца."),
_g("a2-aspect","Verb aspect","A2","Distinguish completed and ongoing actions.","Я чытаю кнігу."),
_g("a2-comparison","Comparatives and superlatives","A2","Compare people and things.","Гэты дом большы."),
_g("b1-reflexive","Reflexive constructions","B1","Express actions directed back to the subject.","Я рыхтуюся да экзамену."),
_g("b1-imperative","Imperative and polite requests","B1","Give instructions and requests appropriately.","Калі ласка, паўтарыце."),
_g("b1-motion","Motion verbs and prefixes","B1","Describe directed and repeated movement.","Я пайшоў у школу."),
_g("b1-conditionals","Conditional constructions","B1","Express conditions and consequences.","Калі будзе час, я прыйду."),
_g("b1-relative","Relative clauses","B1","Identify people and things with subordinate clauses.","Гэта кніга, якую я чытаю."),
_g("b1-reported","Reported speech","B1","Report statements and questions.","Ён сказаў, што прыйдзе."),
_g("b1-causal","Cause, purpose and result","B1","Connect reasons, goals and consequences.","Я прыйшоў, каб дапамагчы."),
_g("b1-concessive","Concession and contrast","B1","Express contrast and concession.","Хоць ішоў дождж, мы пайшлі."),
_g("b2-participles","Participles and verbal adjectives","B2","Use participial structures in description.","Чалавек, які працуе, стаміўся."),
_g("b2-adverbial","Adverbial participles","B2","Link simultaneous and sequential actions.","Ідучы дадому, ён думаў."),
_g("b2-passive","Passive constructions","B2","Describe processes without foregrounding the agent.","Праект быў завершаны."),
_g("b2-impersonal","Impersonal and modal constructions","B2","Express necessity, possibility and evaluation.","Трэба працаваць."),
_g("b2-discourse","Discourse connectors","B2","Build coherent spoken and written discourse.","Аднак вынік быў іншым."),
_g("b2-nominalization","Nominalization","B2","Use abstract nouns in formal discourse.","Развіццё мовы патрабуе падтрымкі."),
_g("b2-information","Information structure","B2","Manage topic, focus and emphasis.","Менавіта гэта важна."),
_g("c1-formal","Formal and institutional register","C1","Write appropriately for institutions and administration.","Згодна з рашэннем камісіі..."),
_g("c1-academic","Academic register and hedging","C1","Present claims cautiously and precisely.","Можна меркаваць, што вынікі значныя."),
_g("c1-argumentation","Argumentation and evidence","C1","Develop claims, reasons and evidence.","Гэты аргумент пацвярджаецца дадзенымі."),
_g("c1-embedded","Embedded questions and propositions","C1","Embed questions and propositions in complex syntax.","Важна высветліць, чаму гэта адбылося."),
_g("c1-media","Media and public language","C1","Interpret formal public and media discourse.","Паводле паведамлення прэсы, сустрэча адбудзецца заўтра."),
_g("c1-pragmatics","Pragmatics and register shifting","C1","Adjust wording to audience and situation.","Дазвольце ўдакладніць гэты момант."),
_g("c1-rhetoric","Rhetorical structure","C1","Use emphasis, contrast and persuasive structure.","Такім чынам, неабходна зрабіць выснову."),
_g("c2-literary","Literary and idiomatic language","C2","Interpret figurative and idiomatic Belarusian.","Ён узяў сябе ў рукі."),
_g("c2-translation","Translation precision","C2","Choose precise equivalents across contexts.","Сэнс выразу залежыць ад кантэксту."),
_g("c2-discourse","Discourse analysis","C2","Analyse stance, cohesion and register.","Выбар словаў змяняе танальнасць выказвання."),
_g("c2-rhetorical","Advanced rhetorical nuance","C2","Handle implication, irony and nuanced stance.","Нібыта ўсё было проста, але вынік быў складаны.")
]

_vocab=[
("greetings","A1",[("прывітанне","greeting","Прывітанне!"),("дзякуй","thank you","Дзякуй за дапамогу.")]),
("identity","A1",[("імя","name","Мяне завуць Аляксей."),("вучань","student","Я вучань.")]),
("family","A1",[("маці","mother","Гэта мая маці."),("бацька","father","Мой бацька дома.")]),
("home","A1",[("дом","house","Гэта мой дом."),("пакой","room","Пакой вялікі.")]),
("daily-life","A1",[("раніца","morning","Добрай раніцы!"),("праца","work","Я іду на працу.")]),
("food","A1",[("хлеб","bread","Я купляю хлеб."),("вада","water","Я хачу вады.")]),
("places","A1",[("рынак","market","Дзе рынак?"),("школа","school","Школа побач.")]),
("communication","A1",[("пытанне","question","У мяне ёсць пытанне."),("дапамога","help","Мне патрэбна дапамога.")]),
("travel","A2",[("дарога","road","Дарога доўгая."),("білет","ticket","Мне патрэбны білет.")]),
("health","A2",[("лекар","doctor","Мне патрэбен лекар."),("лекі","medicine","Я прымаю лекі.")]),
("study","B1",[("экзамен","exam","Я рыхтуюся да экзамену."),("веды","knowledge","Веды важныя.")]),
("work","B1",[("праект","project","Праект завершаны."),("рашэнне","decision","Мы прынялі рашэнне.")]),
("society","B2",[("грамадства","society","Грамадства змяняецца."),("адказнасць","responsibility","Гэта наша адказнасць.")]),
("economy","B2",[("эканоміка","economy","Эканоміка развіваецца."),("рынок","market","Рынак змяняецца.")]),
("media","C1",[("паведамленне","report","Паведамленне апублікавана."),("крыніца","source","Крыніца надзейная.")]),
("academic","C1",[("даследаванне","research","Даследаванне працягваецца."),("вынік","result","Вынік пацвярджае гіпотэзу.")]),
("culture","C2",[("спадчына","heritage","Культурная спадчына важная."),("традыцыя","tradition","Традыцыя перадаецца пакаленнямі.")]),
("discourse","C2",[("кантэкст","context","Сэнс залежыць ад кантэксту."),("адценне","nuance","Гэта адценне значэння.")
])]

VOCABULARY_SETS=[VocabularySet(id=f"be-vocab-{i+1}",level=level,topic=topic,unit_ref=f"be-{level.lower()}-unit-{(i%8)+1}",words=[VocabularyEntry(word=w,pos="word",definition=d,example=e) for w,d,e in words]) for i,(topic,level,words) in enumerate(_vocab)]

_phr=[
("Greetings","👋","A1",[("Добрай раніцы!","morning greeting"),("Як ты?","asking how someone is")]),
("Introductions","👤","A1",[("Мяне завуць Аляксей.","introducing yourself"),("Кім ты працуеш?","asking occupation")]),
("Courtesy","🙏","A1",[("Калі ласка.","polite response"),("Дзякуй за дапамогу.","thanking someone")]),
("Shopping","🛒","A1",[("Колькі гэта каштуе?","asking price"),("Я хачу гэта.","expressing a purchase choice")]),
("Directions","🧭","A1",[("Дзе рынак?","asking directions"),("Як дайсці да школы?","asking how to reach school")]),
("Daily life","☀️","A2",[("Я іду на працу.","daily routine"),("Заўтра я буду вучыцца.","future plan")]),
("Travel","✈️","A2",[("Дзе можна купіць білет?","travel question"),("Калі адпраўляецца цягнік?","transport question")]),
("Health","🩺","A2",[("Мне патрэбен лекар.","asking for a doctor"),("У мяне баліць галава.","describing a symptom")]),
("Discussion","💬","B1",[("Я лічу, што...","stating an opinion"),("Я згодны з вамі.","agreement")]),
("Work","💼","B2",[("Згодна з рашэннем...","formal reference"),("Трэба ўлічыць гэты факт.","formal obligation")]),
("Formal","🏛️","C1",[("Згодна з рашэннем камісіі...","institutional language"),("Просім разгледзець пытанне.","formal request")]),
("Academic","📚","C1",[("Можна меркаваць, што...","academic hedging"),("Вынікі даследавання паказваюць...","academic reporting")]),
("Rhetoric","🎙️","C2",[("Такім чынам, неабходна зрабіць выснову.","conclusion"),("Гэта пытанне патрабуе асаблівай увагі.","emphasis")])
]
PHRASEBOOK_CATEGORIES=[PhrasebookCategory(id=f"be-phrase-{i+1}",level=level,situation=s,icon=icon,phrases=[PhrasebookEntry(text=t,context=c,register="formal" if level in ("C1","C2") else "neutral") for t,c in ps]) for i,(s,icon,level,ps) in enumerate(_phr)]

_titles={
"A1":["Прывітанне і знаёмства","Сям'я і дом","Штодзённае жыццё","Ежа і пакупкі","Месцы і напрамкі","Зносіны","Навучанне","Паўтарэнне"],
"A2":["Род і ўзгадненне","Склоны","Мінулы час","Будучы час","Від дзеяслова","Параўнанне","Зваротныя формы","Паўтарэнне"],
"B1":["Загад і ветлівыя просьбы","Дзеясловы руху","Умоўныя сказы","Адносныя сказы","Паведамленне чужой мовы","Прычына і мэта","Саступка","Звязны дыялог"],
"B2":["Дзеепрыметнікі","Дзеепрыслоўі","Пасіўныя формы","Безасабовыя канструкцыі","Сувязнасць тэксту","Наміналізацыя","Тэма і фокус","Складаны сінтаксіс"],
"C1":["Афіцыйны стыль","Акадэмічная мова","Аргументацыя","Убудаваныя пытанні","Медыя і публічная мова","Прагматыка","Рытарычная структура","Пісьмовая камунікацыя"],
"C2":["Мастацкая мова","Дакладнасць перакладу","Аналіз дыскурсу","Рытарычныя адценні","Змена рэгістра","Ідыяматыка","Крытычнае чытанне","Сінтэз C2"]
}
_levels={l:[g for g in GRAMMAR_TOPICS if g.level==l] for l in LEVELS}
CURRICULUM={}
for level in LEVELS:
    CURRICULUM[level]=[]
    for n,title in enumerate(_titles[level],1):
        gs=_levels[level]
        CURRICULUM[level].append(CurriculumUnit(id=f"be-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=[gs[n-1].title],vocabulary_set_ids=[v.id for v in VOCABULARY_SETS if v.level==level][:1] or ["be-vocab-1"],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=[f"Use Belarusian for {title.lower()} at {level} level."],default_weeks=2 if level in ("A1","A2") else 3))

_AS=[("communication","A1","Which phrase is a morning greeting?",["Добрай раніцы!","дзякуй","дом","маці"],"Добрай раніцы!"),("identity","A1","Which sentence introduces a student?",["Я вучань.","Кніга на стале.","Дзе рынак?","Я хачу вады."],"Я вучань."),("communication","A1","Which phrase asks how someone is?",["Як ты?","Калі ласка.","Дзе рынак?","Я іду на працу."],"Як ты?"),("shopping","A1","Which phrase asks the price?",["Колькі гэта каштуе?","Я не разумею.","Добрай раніцы!","Гэта мой дом."],"Колькі гэта каштуе?"),("directions","A1","Which question asks for the market?",["Дзе рынак?","Я хачу вады.","Як ты?","Гэта мая кніга."],"Дзе рынак?"),("grammar","A2","Which sentence describes a future plan?",["Заўтра я буду вучыцца.","Я не разумею.","Гэта мой дом.","Як ты?"],"Заўтра я буду вучыцца."),("grammar","A2","Which sentence expresses a destination?",["Я іду ў школу.","Добрай раніцы!","Дзякуй.","Гэта мая маці."],"Я іду ў школу."),("grammar","B1","Which sentence is conditional?",["Калі будзе час, я прыйду.","Дзякуй за дапамогу.","Я вучань.","Дзе рынак?"],"Калі будзе час, я прыйду."),("grammar","B1","Which sentence reports speech?",["Ён сказаў, што прыйдзе.","Я хачу вады.","Колькі гэта каштуе?","Гэта мой дом."],"Ён сказаў, што прыйдзе."),("register","B2","Which expression is formal?",["Згодна з рашэннем камісіі...","Прывітанне!","Як ты?","Я хачу гэта."],"Згодна з рашэннем камісіі..."),("academic","C1","Which phrase is academic hedging?",["Можна меркаваць, што вынікі значныя.","Прывітанне!","Дзе рынак?","Я хачу вады."],"Можна меркаваць, што вынікі значныя."),("translation","C2","Which statement highlights contextual meaning?",["Сэнс выразу залежыць ад кантэксту.","Добрай раніцы!","Я іду на працу.","Дзякуй."] ,"Сэнс выразу залежыць ад кантэксту.")]
ASSESSMENT_BANK=[AssessmentQuestion(id=f"be-{i+1:03d}",skill=s,difficulty=l,question=q,options=o,correct=c) for i,(s,l,q,o,c) in enumerate(_AS)]

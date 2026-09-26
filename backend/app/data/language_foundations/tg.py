"""Tajik A1-C2 language foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

_GRAMMAR=[
("pronouns","Personal pronouns","A1","grammar","Ман донишҷӯ ҳастам."),
("copula","Nominal sentences","A1","grammar","Ин китоби ман аст."),
("present","Present tense","A1","verbs","Ман тоҷикӣ меомӯзам."),
("questions","Question words","A1","syntax","Шумо дар куҷо ҳастед?"),
("negation","Basic negation","A1","grammar","Ман намедонам."),
("demonstratives","Demonstratives","A1","syntax","Ин хонаи ман аст."),
("possession","Possession","A1","grammar","Ин китоби ман аст."),
("location","Location and prepositions","A1","syntax","Китоб рӯи миз аст."),
("past","Past tense","A2","verbs","Дирӯз ба бозор рафтам."),
("future","Future intention","A2","verbs","Фардо ба Душанбе меравам."),
("imperative","Imperatives and requests","A2","verbs","Лутфан, дарро кушоед."),
("comparative","Comparison","A2","syntax","Ин китоб аз он китоб ҷолибтар аст."),
("modal","Ability and obligation","A2","modality","Ман бояд имрӯз кор кунам."),
("reflexive","Reflexive reference","A2","grammar","Ман худро хуб ҳис мекунам."),
("aspect","Aspect and ongoing action","A2","verbs","Ҳоло китоб мехонам."),
("subordination","Basic subordinate clauses","A2","syntax","Вақте ки меоям, ба шумо занг мезанам."),
("relative","Relative clauses","B1","syntax","Шахсе, ки он ҷо истодааст, бародари ман аст."),
("conditional","Conditionals","B1","syntax","Агар вақт дошта бошам, меоям."),
("reported","Reported speech","B1","discourse","Ӯ гуфт, ки пагоҳ меояд."),
("causal","Cause and reason","B1","syntax","Азбаски борон меборад, дар хона мемонем."),
("purpose","Purpose clauses","B1","syntax","Барои он ки беҳтар омӯзам, ҳар рӯз мехонам."),
("concessive","Concession","B1","syntax","Гарчанде хаста бошам, корро тамом мекунам."),
("reciprocal","Reciprocal constructions","B1","grammar","Онҳо якдигарро хуб мешиносанд."),
("causative","Causative constructions","B2","grammar","Муаллим ба донишҷӯён матнро хонд."),
("passive","Passive constructions","B2","grammar","Қарор имрӯз қабул шуд."),
("perfect","Perfect and resultative meaning","B2","verbs","Ман вазифаро аллакай иҷро кардаам."),
("pluperfect","Anterior past","B2","verbs","Пеш аз омаданам, ӯ рафта буд."),
("indirect_question","Embedded questions","B2","syntax","Намедонам, ӯ кай меояд."),
("nominalization","Nominalization","C1","academic","Омӯзиши забон вақти зиёд талаб мекунад."),
("hedging","Academic hedging","C1","academic","Эҳтимол, ин натиҷа дуруст бошад."),
("information_structure","Information structure","C1","discourse","Маҳз ҳамин масъала муҳим аст."),
("register","Formal and institutional register","C1","register","Лутфан, аризаи худро пешниҳод намоед."),
("argumentation","Argumentation and cohesion","C2","discourse","Аз ин рӯ, метавон ба чунин хулоса омад."),
("rhetoric","Rhetorical nuance","C2","rhetoric","Бо вуҷуди ин, масъала аз чанд ҷиҳат баҳснок аст."),
("pragmatics","Pragmatics and politeness","C2","pragmatics","Агар зид набошед, мехостам як пешниҳод кунам."),
("discourse_analysis","Advanced discourse analysis","C2","discourse","Ин мавқеъро бояд дар заминаи васеътари иҷтимоӣ баррасӣ кард."),
]
GRAMMAR_TOPICS=[
GrammarTopic(slug=s,title=t,level=l,category=c,summary=f"Use {t.lower()} accurately in Tajik.",explanation=f"Develop controlled and natural Tajik use of {t.lower()} at {l}.",examples=[GrammarExample(text=e)])
for s,t,l,c,e in _GRAMMAR
]

_VOCAB=[
("greetings_a1","Greetings and courtesy","A1",[("Салом","phrase","hello","Салом, чӣ ҳол доред?"),("раҳмат","noun","thanks","Раҳмат барои кӯмак."),("лутфан","adverb","please","Лутфан, нишинед."),("хайр","phrase","goodbye","Хайр, то боздид.")]),
("identity_a1","Identity and people","A1",[("ном","noun","name","Номи ман Али аст."),("донишҷӯ","noun","student","Ман донишҷӯ ҳастам."),("муаллим","noun","teacher","Ӯ муаллим аст."),("дӯст","noun","friend","Ӯ дӯсти ман аст.")]),
("family_a1","Family","A1",[("модар","noun","mother","Модари ман дар хона аст."),("падар","noun","father","Падарам кор мекунад."),("бародар","noun","brother","Бародарам донишҷӯ аст."),("хоҳар","noun","sister","Хоҳарам китоб мехонад.")]),
("home_a1","Home and objects","A1",[("хона","noun","home","Хонаи мо калон аст."),("ҳуҷра","noun","room","Ҳуҷраи ман равшан аст."),("дар","noun","door","Дарро кушоед."),("миз","noun","table","Китоб рӯи миз аст.")]),
("daily_a1","Daily routine","A1",[("субҳ","noun","morning","Субҳ барвақт мехезам."),("рӯз","noun","day","Имрӯз рӯзи хуб аст."),("кор","noun","work","Ман ба кор меравам."),("об","noun","water","Ман об менӯшам.")]),
("food_a1","Food and drink","A1",[("нон","noun","bread","Ман нон мехӯрам."),("чой","noun","tea","Ман чой менӯшам."),("биринҷ","noun","rice","Биринҷ тайёр аст."),("себ","noun","apple","Ман як себ мехӯрам.")]),
("places_a1","Places and directions","A1",[("бозор","noun","market","Бозор дар наздикии хона аст."),("мактаб","noun","school","Мактаб дур нест."),("беморхона","noun","hospital","Беморхона дар марказ аст."),("роҳ","noun","road","Роҳ ба шаҳр меравад.")]),
("communication_a1","Basic communication","A1",[("савол","noun","question","Ман як савол дорам."),("ёрӣ","noun","help","Ман ба ёрӣ ниёз дорам."),("забон","noun","language","Ман забони тоҷикӣ меомӯзам."),("сӯҳбат","noun","conversation","Мо сӯҳбат мекунем.")]),
("shopping_a2","Shopping","A2",[("нарх","noun","price","Нархи ин чанд аст?"),("мағоза","noun","shop","Ин мағоза калон аст."),("харидан","verb","to buy","Ман мехоҳам китоб харам."),("арзон","adjective","cheap","Ин либос арзон аст.")]),
("travel_a2","Travel","A2",[("сафар","noun","trip","Сафари мо фардо оғоз мешавад."),("чипта","noun","ticket","Ман чипта харидам."),("истгоҳ","noun","station","Истгоҳ дар куҷост?"),("меҳмонхона","noun","hotel","Меҳмонхона дар марказ аст.")]),
("health_a2","Health","A2",[("саломатӣ","noun","health","Саломатӣ муҳим аст."),("дард","noun","pain","Сари ман дард мекунад."),("табиб","noun","doctor","Табиб маро муоина кард."),("дорӯ","noun","medicine","Доруро сари вақт гиред.")]),
("weather_a2","Weather","A2",[("борон","noun","rain","Имрӯз борон меборад."),("барф","noun","snow","Зимистон барф меборад."),("гарм","adjective","hot","Имрӯз ҳаво гарм аст."),("сард","adjective","cold","Субҳ ҳаво сард буд.")]),
("study_a2","Study","A2",[("дарс","noun","lesson","Дарс соати нӯҳ оғоз мешавад."),("имтиҳон","noun","exam","Фардо имтиҳон дорем."),("омӯхтан","verb","to learn","Ман забон меомӯзам."),("китоб","noun","book","Ин китоби нав аст.")]),
("work_a2","Workplace","A2",[("идора","noun","office","Ман дар идора кор мекунам."),("ҳамкор","noun","colleague","Ҳамкорам имрӯз меояд."),("лоиҳа","noun","project","Лоиҳа муҳим аст."),("маош","noun","salary","Маош ҳар моҳ дода мешавад.")]),
("transport_a2","Transport","A2",[("автобус","noun","bus","Ман бо автобус меравам."),("қатор","noun","train","Қатор соати ҳафт меояд."),("мошин","noun","car","Мошини мо нав аст."),("фурудгоҳ","noun","airport","Фурудгоҳ аз шаҳр дур аст.")]),
("city_b1","City and society","B1",[("шаҳр","noun","city","Ин шаҳр таърихи қадим дорад."),("кӯча","noun","street","Кӯча имрӯз серодам аст."),("маҳалла","noun","neighborhood","Маҳаллаи мо ором аст."),("хизматрасонӣ","noun","service","Хизматрасонӣ беҳтар шудааст.")]),
("environment_b1","Environment","B1",[("муҳити зист","noun","environment","Ҳифзи муҳити зист муҳим аст."),("табиат","noun","nature","Мо бояд табиатро ҳифз кунем."),("ифлосшавӣ","noun","pollution","Ифлосшавӣ мушкили ҷиддӣ аст."),("захира","noun","resource","Захираҳои об маҳдуданд.")]),
("media_b1","Media and information","B1",[("хабар","noun","news","Ман хабарро хондам."),("рӯзнома","noun","newspaper","Рӯзнома ҳар саҳар нашр мешавад."),("барнома","noun","program","Барнома соати ҳашт оғоз мешавад."),("манбаъ","noun","source","Ин манбаъ боэътимод аст.")]),
("culture_b1","Culture","B1",[("фарҳанг","noun","culture","Фарҳанг қисми муҳими ҷомеа аст."),("адабиёт","noun","literature","Ман адабиёти тоҷикро дӯст медорам."),("санъат","noun","art","Санъат одамонро ба ҳам меорад."),("мерос","noun","heritage","Мероси фарҳангиро бояд ҳифз кард.")]),
("society_b1","Society","B1",[("ҷомеа","noun","society","Ҷомеа тағйир меёбад."),("шаҳрванд","noun","citizen","Ҳар шаҳрванд ҳуқуқ дорад."),("ҳуқуқ","noun","right","Ҳуқуқи инсон бояд ҳифз шавад."),("масъулият","noun","responsibility","Ин вазифа масъулияти калон дорад.")]),
]
VOCABULARY_SETS=[
VocabularySet(id=i,level=l,topic=t,unit_ref=f"tg-{l.lower()}-unit-{((n-1)%8)+1}",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])
for n,(i,t,l,words) in enumerate(_VOCAB,1)
]
PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="greetings",level="A1",situation="Greetings",icon="👋",phrases=[PhrasebookEntry(text="Салом!",context="greeting",register="neutral"),PhrasebookEntry(text="Чӣ ҳол доред?",context="asking how someone is",register="polite"),PhrasebookEntry(text="Хайр, то боздид!",context="farewell",register="neutral")]),
PhrasebookCategory(id="thanks",level="A1",situation="Thanks and apology",icon="🙏",phrases=[PhrasebookEntry(text="Раҳмат!",context="thanks",register="neutral"),PhrasebookEntry(text="Хеле раҳмат.",context="strong thanks",register="neutral"),PhrasebookEntry(text="Бубахшед.",context="apology",register="polite")]),
PhrasebookCategory(id="shopping",level="A2",situation="Shopping",icon="🛒",phrases=[PhrasebookEntry(text="Ин чанд пул аст?",context="asking price",register="neutral"),PhrasebookEntry(text="Ман инро мехоҳам.",context="requesting an item",register="neutral"),PhrasebookEntry(text="Каме арзонтар мешавад?",context="negotiating price",register="polite")]),
PhrasebookCategory(id="directions",level="A2",situation="Directions",icon="🧭",phrases=[PhrasebookEntry(text="Бозор дар куҷост?",context="asking location",register="neutral"),PhrasebookEntry(text="Чӣ тавр ба истгоҳ равам?",context="asking directions",register="neutral"),PhrasebookEntry(text="Рост ё чап?",context="checking direction",register="neutral")]),
PhrasebookCategory(id="travel",level="A2",situation="Travel",icon="✈️",phrases=[PhrasebookEntry(text="Ман чипта мехоҳам.",context="buying a ticket",register="neutral"),PhrasebookEntry(text="Қатор соати чанд меравад?",context="asking departure time",register="neutral"),PhrasebookEntry(text="Меҳмонхона дар куҷост?",context="finding a hotel",register="neutral")]),
PhrasebookCategory(id="health",level="A2",situation="Health",icon="🩺",phrases=[PhrasebookEntry(text="Ман худро хуб ҳис намекунам.",context="saying you feel unwell",register="neutral"),PhrasebookEntry(text="Сари ман дард мекунад.",context="describing pain",register="neutral"),PhrasebookEntry(text="Табиб дар куҷост?",context="finding a doctor",register="neutral")]),
PhrasebookCategory(id="work",level="A2",situation="Work",icon="💼",phrases=[PhrasebookEntry(text="Ман дар идора кор мекунам.",context="describing work",register="neutral"),PhrasebookEntry(text="Лутфан, ин ҳуҷҷатро имзо кунед.",context="work request",register="polite"),PhrasebookEntry(text="Мӯҳлати лоиҳа кай аст?",context="asking a deadline",register="neutral")]),
PhrasebookCategory(id="study",level="A2",situation="Study",icon="📚",phrases=[PhrasebookEntry(text="Ман барои имтиҳон тайёр мешавам.",context="study",register="neutral"),PhrasebookEntry(text="Ин калима чӣ маъно дорад?",context="asking meaning",register="neutral"),PhrasebookEntry(text="Метавонед такрор кунед?",context="asking to repeat",register="polite")]),
PhrasebookCategory(id="social",level="B1",situation="Social conversation",icon="💬",phrases=[PhrasebookEntry(text="Ба назари шумо чӣ гуна аст?",context="asking an opinion",register="neutral"),PhrasebookEntry(text="Ман бо ин фикр розӣ ҳастам.",context="agreeing",register="neutral"),PhrasebookEntry(text="Ман каме дигар хел фикр мекунам.",context="disagreeing politely",register="polite")]),
PhrasebookCategory(id="formal",level="B2",situation="Formal communication",icon="🏛️",phrases=[PhrasebookEntry(text="Лутфан, аризаи худро пешниҳод намоед.",context="formal request",register="formal"),PhrasebookEntry(text="Мувофиқи маълумоти пешниҳодшуда...",context="formal reference",register="formal"),PhrasebookEntry(text="Бо эҳтиром...",context="formal closing",register="formal")]),
PhrasebookCategory(id="academic",level="C1",situation="Academic discussion",icon="🎓",phrases=[PhrasebookEntry(text="Далелҳо нишон медиҳанд, ки...",context="introducing evidence",register="formal"),PhrasebookEntry(text="Аз ин рӯ, метавон ба чунин хулоса омад.",context="drawing a conclusion",register="formal"),PhrasebookEntry(text="Эҳтимол, ин натиҷа ба омилҳои дигар вобаста бошад.",context="hedging a claim",register="formal")]),
PhrasebookCategory(id="professional",level="C1",situation="Professional negotiation",icon="🤝",phrases=[PhrasebookEntry(text="Мо пешниҳод мекунем, ки...",context="proposal",register="formal"),PhrasebookEntry(text="Оё метавон ин шартро бозбинӣ кард?",context="negotiating",register="polite"),PhrasebookEntry(text="Биёед масъалаҳои асосиро муайян кунем.",context="setting an agenda",register="formal")]),
PhrasebookCategory(id="advanced",level="C2",situation="Advanced discourse",icon="🗣️",phrases=[PhrasebookEntry(text="Бо вуҷуди ин, масъала аз чанд ҷиҳат баҳснок аст.",context="qualified contrast",register="formal"),PhrasebookEntry(text="Ин мавқеъро бояд дар заминаи васеътари иҷтимоӣ баррасӣ кард.",context="contextualizing an argument",register="formal"),PhrasebookEntry(text="Агар зид набошед, мехостам як пешниҳод кунам.",context="polite advanced suggestion",register="formal")]),
]
_LEVEL_TOPICS={
"A1":["pronouns","copula","present","questions","negation","demonstratives","possession","location"],
"A2":["past","future","imperative","comparative","modal","reflexive","aspect","subordination"],
"B1":["relative","conditional","reported","causal","purpose","concessive","reciprocal","relative"],
"B2":["causative","passive","perfect","pluperfect","indirect_question","reported","causal","conditional"],
"C1":["nominalization","hedging","information_structure","register","argumentation","nominalization","hedging","register"],
"C2":["argumentation","rhetoric","pragmatics","discourse_analysis","information_structure","register","argumentation","rhetoric"],
}
_UNITS=[]
for level,slugs in _LEVEL_TOPICS.items():
 for i,slug in enumerate(slugs,1):
  title={
   "A1":["Салом ва шиносоӣ","Оила ва хона","Рӯзмарра","Вақт ва ҷой","Хӯрок","Харид","Самтҳо","Муоширати асосӣ"],
   "A2":["Таҷрибаи гузашта","Нақшаҳои оянда","Дархост ва маслиҳат","Муқоиса","Қобилият ва ӯҳдадорӣ","Эҳсосот","Амалҳои давомдор","Ҷумлаҳои пайрав"],
   "B1":["Шахс ва ҷомеа","Шарт ва имконият","Гуфтори нақлшуда","Сабаб","Мақсад","Имтиёз ва зиддият","Муносибатҳои мутақобил","Ҷумлаҳои нисбӣ"],
   "B2":["Сабабгорӣ","Ҷумлаҳои пассив","Натиҷаи амал","Замони пешина","Саволҳои дохилшуда","Гуфтори ғайримустақим","Пайвастагии матн","Шартҳои мураккаб"],
   "C1":["Номгузории мафҳумҳо","Эҳтимол ва эҳтиёт","Сохтори иттилоот","Забони расмӣ","Далел ва пайвастагӣ","Мафҳумсозӣ","Баён бо эҳтиёт","Муоширати расмӣ"],
   "C2":["Баҳс ва далел","Нозукиҳои риторикӣ","Прагматика","Таҳлили дискурс","Сохтори иттилоот","Услуб ва регистр","Аргументатсияи пешрафта","Риторикаи пешрафта"]
  }[level][i-1]
  _UNITS.append(CurriculumUnit(id=f"tg-{level.lower()}-unit-{i}",level=level,unit_number=i,title=title,grammar_points=[slug],vocabulary_set_ids=[_VOCAB[min((ord(level[0])-65)*3+i-1,len(_VOCAB)-1)][0]],lesson_types=["grammar","vocabulary","speaking","listening","reading","writing","review"],competency_checklist=["Understand the target structure in authentic Tajik","Use it in a guided exchange","Produce a short level-appropriate response"],default_weeks=2))
CURRICULUM={level:[u for u in _UNITS if u.level==level] for level in LEVELS}

ASSESSMENT_BANK=[
AssessmentQuestion(id="tg-a1-001",skill="vocabulary",difficulty="A1",question="What does «Салом» mean?",options=["Hello","Market","School","Water"],correct="Hello"),
AssessmentQuestion(id="tg-a1-002",skill="grammar",difficulty="A1",question="Choose the correct Tajik sentence for “I am a student.”",options=["Ман донишҷӯ ҳастам.","Ман бозор ҳастам.","Ман об ҳастам.","Ман роҳ ҳастам."],correct="Ман донишҷӯ ҳастам."),
AssessmentQuestion(id="tg-a1-003",skill="vocabulary",difficulty="A1",question="Which word means “mother”?",options=["модар","падар","бародар","дӯст"],correct="модар"),
AssessmentQuestion(id="tg-a1-004",skill="communication",difficulty="A1",question="How do you politely say “please”?",options=["лутфан","хайр","бозор","рӯз"],correct="лутфан"),
AssessmentQuestion(id="tg-a2-001",skill="grammar",difficulty="A2",question="Which sentence refers to yesterday?",options=["Дирӯз ба бозор рафтам.","Фардо ба Душанбе меравам.","Ман чой менӯшам.","Салом!"],correct="Дирӯз ба бозор рафтам."),
AssessmentQuestion(id="tg-a2-002",skill="communication",difficulty="A2",question="Which phrase asks for a lower price?",options=["Каме арзонтар мешавад?","Бозор дар куҷост?","Чӣ ҳол доред?","Ман об мехоҳам."],correct="Каме арзонтар мешавад?"),
AssessmentQuestion(id="tg-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["Агар вақт дошта бошам, меоям.","Ман об менӯшам.","Салом!","Ин китоби ман аст."],correct="Агар вақт дошта бошам, меоям."),
AssessmentQuestion(id="tg-b1-002",skill="reading",difficulty="B1",question="Which connector introduces a reason?",options=["Азбаски","Фардо","Лутфан","Хайр"],correct="Азбаски"),
AssessmentQuestion(id="tg-b2-001",skill="grammar",difficulty="B2",question="Which sentence uses a passive construction?",options=["Қарор имрӯз қабул шуд.","Ман қарорро хондам.","Ӯ пагоҳ меояд.","Мо сӯҳбат мекунем."],correct="Қарор имрӯз қабул шуд."),
AssessmentQuestion(id="tg-b2-002",skill="grammar",difficulty="B2",question="Which sentence expresses a completed result?",options=["Ман вазифаро аллакай иҷро кардаам.","Ман вазифаро иҷро мекунам.","Ман вазифаро иҷро хоҳам кард.","Ман вазифаро намедонам."],correct="Ман вазифаро аллакай иҷро кардаам."),
AssessmentQuestion(id="tg-c1-001",skill="academic",difficulty="C1",question="Which phrase appropriately hedges an academic claim?",options=["Эҳтимол, ин натиҷа дуруст бошад.","Ин ҳатман дуруст аст.","Салом!","Ман ба бозор меравам."],correct="Эҳтимол, ин натиҷа дуруст бошад."),
AssessmentQuestion(id="tg-c1-002",skill="academic",difficulty="C1",question="Which phrase introduces a formal conclusion?",options=["Аз ин рӯ, метавон ба чунин хулоса омад.","Ман об мехоҳам.","Бозор дар куҷост?","Хайр!"],correct="Аз ин рӯ, метавон ба чунин хулоса омад."),
AssessmentQuestion(id="tg-c2-001",skill="discourse",difficulty="C2",question="Which phrase provides a qualified contrast?",options=["Бо вуҷуди ин, масъала аз чанд ҷиҳат баҳснок аст.","Салом!","Ман донишҷӯ ҳастам.","Ин чанд пул аст?"],correct="Бо вуҷуди ин, масъала аз чанд ҷиҳат баҳснок аст."),
AssessmentQuestion(id="tg-c2-002",skill="pragmatics",difficulty="C2",question="Which phrase makes an advanced polite suggestion?",options=["Агар зид набошед, мехостам як пешниҳод кунам.","Дарро кушо!","Ман об мехоҳам.","Хайр."],correct="Агар зид набошед, мехостам як пешниҳод кунам."),
]

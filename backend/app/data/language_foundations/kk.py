"""Қазақ тілі A1 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion
LEVELS=["A1","A2","B1","B2","C1","C2"]
def g(s,t,m,e): return GrammarTopic(slug=s,title=t,level="A1",category="core",summary=m,explanation=m,examples=[GrammarExample(text=x) for x in e])
GRAMMAR_TOPICS=[g(*x) for x in [
("pronouns","Жіктеу есімдіктері","Use мен, сен, сіз, ол and біз in basic sentences.",["Мен студентпін.","Сіз мұғалімсіз."]),
("identity","Present identity","Use the personal endings of бол- in simple identity statements.",["Мен дәрігермін.","Ол мұғалім."]),
("possessive","Possession","Use менің/сенің and possessive endings with familiar nouns.",["Бұл менің кітабым.","Бұл оның үйі."]),
("location","Location and movement","Use -да/-де and -ға/-ге with common places.",["Мен үйдемін.","Мен мектепке барамын."]),
("questions","Question forms","Use кім, не, қайда and қанша for basic questions.",["Бұл не?","Сіз қайдасыз?"]),
("negation","Negation","Use емес and -ма/-ме forms for simple negatives.",["Мен мұғалім емеспін.","Мен бармаймын."]),
("plural","Plural nouns","Use common plural suffixes -лар/-лер/-дар/-дер.",["Достарым осында.","Кітаптар үстелде."]),
("time","Time expressions","Talk about today, tomorrow and daily schedules.",["Бүгін жұмыс істеймін.","Ертең мектепке барамын."])
]]
def v(i,t,ws): return VocabularySet(id=i,level="A1",topic=t,unit_ref="kk-a1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in ws])
VOCABULARY_SETS=[v(*x) for x in [
("greetings_a1","Амандасу",[("Сәлеметсіз бе","phrase","hello (polite)","Сәлеметсіз бе! Қалыңыз қалай?"),("Сәлем","phrase","hello","Сәлем!"),("Рақмет","phrase","thank you","Рақмет сізге."),("Аты","noun","name","Менің атым Айдана.")]),
("family_a1","Отбасы",[("ана","noun","mother","Менің анам үйде."),("әке","noun","father","Менің әкем жұмыс істейді."),("аға","noun","older brother","Менің ағам студент."),("әпке","noun","older sister","Менің әпкем мектепте.")]),
("home_a1","Үй",[("үй","noun","home","Менің үйім жақын."),("бөлме","noun","room","Бөлме таза."),("үстел","noun","table","Кітап үстелде жатыр."),("есік","noun","door","Есік ашық.")]),
("daily_a1","Күнделікті өмір",[("таңертең","adverb","in the morning","Таңертең жұмыс істеймін."),("жұмыс істеу","verb","to work","Мен күнде жұмыс істеймін."),("оқу","verb","to study/read","Мен кешке оқимын."),("ұйықтау","verb","to sleep","Мен түнде ұйықтаймын.")]),
("food_a1","Тамақ және сауда",[("су","noun","water","Маған су керек."),("нан","noun","bread","Мен нан сатып аламын."),("шай","noun","tea","Мен шай ішемін."),("баға","noun","price","Мынау қанша тұрады?")]),
("places_a1","Орындар және бағыт",[("көше","noun","street","Бұл көше қайда апарады?"),("бекет","noun","station","Бекет қайда?"),("оңға","adverb","to the right","Оңға бұрылыңыз."),("солға","adverb","to the left","Солға бұрылыңыз.")]),
("communication_a1","Қарым-қатынас",[("көмек","noun","help","Маған көмек керек."),("өтінемін","adverb","please","Өтінемін, қайталаңыз."),("түсіну","verb","to understand","Мен түсінбеймін."),("қайталау","verb","to repeat","Сұрақты қайталаңыз.")]),
("review_a1","A1 қайталау",[("бүгін","adverb","today","Бүгін мен үйдемін."),("ертең","adverb","tomorrow","Ертең жұмыс істеймін."),("дос","noun","friend","Ол менің досым."),("уақыт","noun","time","Менің уақытым бар.")])
]]
def p(i,s,items): return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register="neutral") for t,c in items])
PHRASEBOOK_CATEGORIES=[p(*x) for x in [
("greetings_a1","Greetings",[("Сәлеметсіз бе!","greeting"),("Менің атым Айдана.","introducing yourself"),("Мен Алжирденмін.","saying where you are from")]),
("shopping_a1","Shopping",[("Мынау қанша тұрады?","asking price"),("Маған бір нан беріңізші.","requesting an item"),("Картамен төлеуге бола ма?","asking about payment")]),
("directions_a1","Directions",[("Бекет қайда?","asking location"),("Оңға бұрылыңыз.","giving directions"),("Бұл жер алыс па?","checking distance")]),
("help_a1","Help",[("Маған көмектесіңізші.","asking for help"),("Мен түсінбеймін.","clarification"),("Өтінемін, жайырақ сөйлеңіз.","asking someone to slow down")])
]]
def u(i,t,g,v,a,b): return CurriculumUnit(id=f"kk-a1-unit-{i}",level="A1",unit_number=i,title=t,grammar_points=g,vocabulary_set_ids=[v],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=[a,b],default_weeks=2)
CURRICULUM={"A1":[u(1,"Амандасу және танысу",["pronouns","identity"],"greetings_a1","Introduce yourself","Exchange greetings"),u(2,"Отбасы",["possessive","plural"],"family_a1","Describe family","Talk about relationships"),u(3,"Үй",["possessive","location"],"home_a1","Describe your home","Locate objects"),u(4,"Күнделікті өмір",["time","negation"],"daily_a1","Talk about routines","Say what you do not do"),u(5,"Тамақ және сауда",["questions","negation"],"food_a1","Buy basic food","Ask prices"),u(6,"Орындар және бағыт",["location","questions"],"places_a1","Ask directions","Give a simple route"),u(7,"Қарым-қатынас",["questions","negation"],"communication_a1","Ask for help","Repair a misunderstanding"),u(8,"A1 қайталау",["pronouns","time","questions"],"review_a1","Review core A1","Handle familiar exchanges")]}
for level in LEVELS[1:]: CURRICULUM[level]=[CurriculumUnit(id=f"kk-{level.lower()}-foundation",level=level,unit_number=1,title=f"Қазақ тілі {level}",grammar_points=["review A1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=[f"Build {level} communication"],default_weeks=2)]
ASSESSMENT_BANK=[AssessmentQuestion(id=f"kk-a1-{i:03}",skill=s,difficulty="A1",question=q,options=o,correct=c) for i,(s,q,o,c) in enumerate([
("vocabulary","Which phrase is a polite greeting?",["Сәлеметсіз бе!","Рақмет.","Қайырлы түн.","Кешіріңіз."],"Сәлеметсіз бе!"),
("grammar","Which means 'I am a student'?",["Мен студентпін.","Мен студент емеспін.","Ол мұғалім.","Сіз қайдасыз?"],"Мен студентпін."),
("grammar","Which sentence shows possession?",["Бұл менің кітабым.","Мен мектепке барамын.","Мен бармаймын.","Бұл не?"],"Бұл менің кітабым."),
("vocabulary","Which word means mother?",["ана","әке","аға","дос"],"ана"),
("vocabulary","What does баға mean?",["price","water","time","help"],"price"),
("reading","Кітап үстелде жатыр. Where is the book?",["On the table","At school","At home","In the street"],"On the table"),
("grammar","Which sentence is negative?",["Мен бармаймын.","Мен барамын.","Мен студентпін.","Бұл менің үйім."],"Мен бармаймын."),
("communication","How do you ask for help?",["Маған көмектесіңізші.","Рақмет.","Сәлем!","Бекет қайда?"],"Маған көмектесіңізші."),
("communication","How do you ask someone to repeat?",["Өтінемін, қайталаңыз.","Сәлеметсіз бе!","Мен үйдемін.","Ертең барамын."],"Өтінемін, қайталаңыз."),
("vocabulary","What does ертең mean?",["tomorrow","today","morning","friend"],"tomorrow")
],1)]
"""Persian A1 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def g(s,t,m,e): return GrammarTopic(slug=s,title=t,level="A1",category="core",summary=m,explanation=m,examples=[GrammarExample(text=x) for x in e])
GRAMMAR_TOPICS=[g(*x) for x in [
("pronouns","Personal pronouns","Use من، تو، او، ما، شما، آنها in simple sentences.",["من دانشجو هستم.","شما معلم هستید."]),
("ezafe","Ezafe","Link a noun to a modifier or possessor.",["کتابِ خوب","دوستِ علی"]),
("copula","Present copula","Use هستم، هستی، است and plural forms for identity.",["من ایرانی هستم.","آنها دانشجو هستند."]),
("negation","Negation","Use نیست and نمی‌ for basic negative statements.",["این کتاب نیست.","من قهوه نمی‌نوشم."]),
("questions","Question words","Ask who, what, where and how much.",["این چیست؟","ایستگاه کجاست؟"]),
("present","Present verb forms","Use می‌ + verb stem for habitual or current actions.",["من فارسی می‌خوانم.","او کار می‌کند."]),
("plural","Plural nouns","Use ها and common plural patterns.",["کتاب‌ها روی میز هستند.","دوست‌ها اینجا هستند."]),
("prepositions","Prepositions","Use در، به، با، از for location and simple relations.",["در خانه هستم.","با دوستم به بازار می‌روم."])
]]
def v(i,t,ws): return VocabularySet(id=i,level="A1",topic=t,unit_ref="fa-a1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in ws])
VOCABULARY_SETS=[v(*x) for x in [
("greetings_a1","Greetings and identity",[("سلام","phrase","hello","سلام، حال شما چطور است؟"),("خداحافظ","phrase","goodbye","خداحافظ، فردا می‌بینمتان."),("ممنون","phrase","thanks","ممنون از کمک شما."),("نام","noun","name","نام من سارا است.")]),
("family_a1","Family",[("مادر","noun","mother","مادرم در خانه است."),("پدر","noun","father","پدرم کار می‌کند."),("خواهر","noun","sister","خواهرم دانشجو است."),("برادر","noun","brother","برادرم در تهران زندگی می‌کند.")]),
("home_a1","Home",[("خانه","noun","home","خانه من کوچک است."),("اتاق","noun","room","اتاق من روشن است."),("میز","noun","table","کتاب روی میز است."),("کلید","noun","key","کلید روی میز است.")]),
("daily_a1","Daily routine",[("صبح","noun","morning","صبح زود بیدار می‌شوم."),("کار کردن","verb","to work","هر روز کار می‌کنم."),("خواندن","verb","to read","شب کتاب می‌خوانم."),("خوابیدن","verb","to sleep","ساعت یازده می‌خوابم.")]),
("food_a1","Food and shopping",[("آب","noun","water","لطفاً یک لیوان آب می‌خواهم."),("نان","noun","bread","نان تازه می‌خرم."),("چای","noun","tea","من چای می‌نوشم."),("قیمت","noun","price","قیمت این چقدر است؟")]),
("places_a1","Places and directions",[("خیابان","noun","street","این خیابان کجاست؟"),("ایستگاه","noun","station","ایستگاه نزدیک است."),("راست","noun","right","به راست بروید."),("چپ","noun","left","به چپ بپیچید.")]),
("communication_a1","Communication",[("کمک","noun","help","لطفاً کمک کنید."),("لطفاً","adverb","please","لطفاً آرام‌تر صحبت کنید."),("فهمیدن","verb","to understand","این جمله را نمی‌فهمم."),("دوباره","adverb","again","لطفاً دوباره بگویید.")]),
("review_a1","A1 review",[("امروز","adverb","today","امروز وقت دارم."),("فردا","adverb","tomorrow","فردا به دانشگاه می‌روم."),("دوست","noun","friend","او دوست من است."),("وقت","noun","time","الان وقت ندارم.")])
]]
def p(i,s,items): return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register="neutral") for t,c in items])
PHRASEBOOK_CATEGORIES=[p(*x) for x in [
("greetings_a1","Greetings",[("سلام، حال شما چطور است؟","greeting"),("نام من سارا است.","introducing yourself"),("من اهل الجزایر هستم.","saying where you are from")]),
("shopping_a1","Shopping",[("قیمت این چقدر است؟","asking price"),("لطفاً یک کیلو نان می‌خواهم.","requesting an item"),("کارت قبول می‌کنید؟","asking about payment")]),
("directions_a1","Directions",[("ایستگاه کجاست؟","asking location"),("به راست بروید.","giving directions"),("آیا اینجا نزدیک است؟","checking distance")]),
("help_a1","Help",[("لطفاً کمک کنید.","asking for help"),("متوجه نمی‌شوم.","clarification"),("لطفاً آهسته‌تر صحبت کنید.","asking someone to slow down")])
]]
def u(i,t,g,v,a,b): return CurriculumUnit(id=f"fa-a1-unit-{i}",level="A1",unit_number=i,title=t,grammar_points=g,vocabulary_set_ids=[v],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=[a,b],default_weeks=2)
CURRICULUM={"A1":[u(1,"سلام و معرفی",["pronouns","copula"],"greetings_a1","Introduce yourself","Exchange greetings"),u(2,"خانواده",["ezafe","plural"],"family_a1","Describe family","Talk about relationships"),u(3,"خانه",["ezafe","prepositions"],"home_a1","Describe your home","Locate objects"),u(4,"زندگی روزمره",["present","negation"],"daily_a1","Talk about routines","Say what you do not do"),u(5,"غذا و خرید",["questions","negation"],"food_a1","Buy basic food","Ask prices"),u(6,"مکان‌ها و مسیرها",["prepositions","questions"],"places_a1","Ask for directions","Give a simple route"),u(7,"ارتباط",["questions","present"],"communication_a1","Ask for help","Repair a misunderstanding"),u(8,"مرور A1",["pronouns","copula","questions"],"review_a1","Review core A1","Handle familiar exchanges")]}
for level in ["A2","B1","B2","C1","C2"]: CURRICULUM[level]=[CurriculumUnit(id=f"fa-{level.lower()}-foundation",level=level,unit_number=1,title=f"Persian {level}",grammar_points=["review A1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=[f"Build {level} communication"],default_weeks=2)]
ASSESSMENT_BANK=[AssessmentQuestion(id=f"fa-a1-{i:03}",skill=s,difficulty="A1",question=q,options=o,correct=c) for i,(s,q,o,c) in enumerate([
("vocabulary","What does سلام mean?",["hello","thanks","station","water"],"hello"),
("grammar","Choose the correct 'I am a student'.",["من دانشجو هستم.","من دانشجو است.","من دانشجو هستند.","من دانشجو نیست."],"من دانشجو هستم."),
("grammar","Which sentence is negative?",["این کتاب نیست.","این کتاب است.","این کتاب‌ها هستند.","کتاب کجاست؟"],"این کتاب نیست."),
("vocabulary","What is مادر?",["mother","father","friend","bread"],"mother"),
("vocabulary","What does قیمت mean?",["price","help","morning","name"],"price"),
("reading","کتاب روی میز است. Where is the book?",["On the table","In the street","At school","With a friend"],"On the table"),
("grammar","Which asks 'Where is the station?'",["ایستگاه کجاست؟","این چیست؟","نام شما چیست؟","چند کتاب؟"],"ایستگاه کجاست؟"),
("communication","How do you ask someone to repeat?",["لطفاً دوباره بگویید.","خداحافظ.","صبح بخیر.","نام من سارا است."],"لطفاً دوباره بگویید."),
("communication","What can you say when you do not understand?",["متوجه نمی‌شوم.","ممنون.","فردا می‌آیم.","ایستگاه کجاست؟"],"متوجه نمی‌شوم"),
("vocabulary","What does فردا mean?",["tomorrow","today","morning","time"],"tomorrow")
],1)]
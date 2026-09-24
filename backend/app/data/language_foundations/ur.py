"""اردو A1 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion
LEVELS=["A1","A2","B1","B2","C1","C2"]
def g(s,t,m,e): return GrammarTopic(slug=s,title=t,level="A1",category="core",summary=m,explanation=m,examples=[GrammarExample(text=x) for x in e])
GRAMMAR_TOPICS=[g(*x) for x in [
("pronouns","Personal pronouns","Use میں، آپ، تم، وہ and ہم in simple sentences.",["میں طالب علم ہوں۔","آپ استاد ہیں۔"]),
("identity","Identity with ہوں/ہے/ہیں","Build present identity statements with the appropriate form of ہونا.",["میں ڈاکٹر ہوں۔","وہ استاد ہے۔"]),
("possessive","Possession","Use میرا/میری/میرے with familiar nouns.",["یہ میری کتاب ہے۔","یہ میرا گھر ہے۔"]),
("location","Location phrases","Use میں and پر for familiar locations.",["میں گھر میں ہوں۔","کتاب میز پر ہے۔"]),
("questions","Question words","Ask basic what, where, who and how much questions.",["آپ کہاں ہیں؟","یہ کیا ہے؟"]),
("negation","Negation with نہیں","Negate basic present-tense statements.",["میں مصروف نہیں ہوں۔","یہ میری کتاب نہیں ہے۔"]),
("present","Present habitual forms","Use common present forms for everyday routines.",["میں روز کام کرتا ہوں۔","وہ اردو پڑھتی ہے۔"]),
("plural","Plural nouns","Use common plural forms in familiar contexts.",["دوست یہاں ہیں۔","کتابیں میز پر ہیں۔"])
]]
def v(i,t,ws): return VocabularySet(id=i,level="A1",topic=t,unit_ref="ur-a1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in ws])
VOCABULARY_SETS=[v(*x) for x in [
("greetings_a1","Greetings",[("سلام","phrase","hello","سلام!"),("شکریہ","phrase","thank you","شکریہ۔"),("خدا حافظ","phrase","goodbye","خدا حافظ!"),("نام","noun","name","میرا نام علی ہے۔")]),
("family_a1","Family",[("ماں","noun","mother","میری ماں گھر میں ہیں۔"),("والد","noun","father","میرے والد کام کرتے ہیں۔"),("بھائی","noun","brother","میرا بھائی طالب علم ہے۔"),("بہن","noun","sister","میری بہن اسکول جاتی ہے۔")]),
("home_a1","Home",[("گھر","noun","home","میرا گھر قریب ہے۔"),("کمرہ","noun","room","کمرہ صاف ہے۔"),("میز","noun","table","کتاب میز پر ہے۔"),("دروازہ","noun","door","دروازہ کھلا ہے۔")]),
("daily_a1","Daily routine",[("صبح","noun","morning","صبح میں کام کرتا ہوں۔"),("کام کرنا","verb","to work","میں روز کام کرتا ہوں۔"),("پڑھنا","verb","to read/study","میں شام کو پڑھتا ہوں۔"),("سونا","verb","to sleep","میں رات کو سوتا ہوں۔")]),
("food_a1","Food and shopping",[("پانی","noun","water","مجھے پانی چاہیے۔"),("روٹی","noun","bread","میں روٹی خریدتا ہوں۔"),("چائے","noun","tea","میں چائے پیتا ہوں۔"),("قیمت","noun","price","اس کی قیمت کتنی ہے؟")]),
("places_a1","Places and directions",[("سڑک","noun","street","یہ سڑک کہاں جاتی ہے؟"),("اسٹیشن","noun","station","اسٹیشن کہاں ہے؟"),("دائیں","adverb","right","دائیں جائیں۔"),("بائیں","adverb","left","بائیں جائیں۔")]),
("communication_a1","Communication",[("مدد","noun","help","مجھے مدد چاہیے۔"),("براہ کرم","adverb","please","براہ کرم دوبارہ کہیں۔"),("سمجھنا","verb","to understand","میں نہیں سمجھتا۔"),("دوبارہ","adverb","again","دوبارہ کہیں، براہ کرم۔")]),
("review_a1","A1 review",[("آج","adverb","today","آج میں گھر پر ہوں۔"),("کل","adverb","tomorrow","کل میں کام کروں گا۔"),("دوست","noun","friend","وہ میرا دوست ہے۔"),("وقت","noun","time","میرے پاس وقت ہے۔")])
]]
def p(i,s,items): return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register="neutral") for t,c in items])
PHRASEBOOK_CATEGORIES=[p(*x) for x in [
("greetings_a1","Greetings",[("السلام علیکم!","greeting"),("میرا نام علی ہے۔","introducing yourself"),("میں الجزائر سے ہوں۔","saying where you are from")]),
("shopping_a1","Shopping",[("اس کی قیمت کتنی ہے؟","asking price"),("مجھے ایک کلو روٹی چاہیے۔","requesting an item"),("کیا آپ کارڈ لیتے ہیں؟","asking about payment")]),
("directions_a1","Directions",[("اسٹیشن کہاں ہے؟","asking location"),("دائیں جائیں۔","giving directions"),("یہاں سے کتنی دور ہے؟","checking distance")]),
("help_a1","Help",[("براہ کرم میری مدد کریں۔","asking for help"),("میں نہیں سمجھتا۔","clarification"),("براہ کرم آہستہ بولیں۔","asking someone to slow down")])
]]
def u(i,t,g,v,a,b): return CurriculumUnit(id=f"ur-a1-unit-{i}",level="A1",unit_number=i,title=t,grammar_points=g,vocabulary_set_ids=[v],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=[a,b],default_weeks=2)
CURRICULUM={"A1":[u(1,"سلام اور تعارف",["pronouns","identity"],"greetings_a1","Introduce yourself","Exchange greetings"),u(2,"خاندان",["possessive","plural"],"family_a1","Describe family","Talk about relationships"),u(3,"گھر",["possessive","location"],"home_a1","Describe your home","Locate objects"),u(4,"روزمرہ زندگی",["present","negation"],"daily_a1","Talk about routines","Say what you do not do"),u(5,"کھانا اور خریداری",["questions","negation"],"food_a1","Buy basic food","Ask prices"),u(6,"جگہیں اور راستے",["location","questions"],"places_a1","Ask directions","Give a simple route"),u(7,"رابطہ",["questions","negation"],"communication_a1","Ask for help","Repair a misunderstanding"),u(8,"A1 دہرائی",["pronouns","present","questions"],"review_a1","Review core A1","Handle familiar exchanges")]}
for level in LEVELS[1:]: CURRICULUM[level]=[CurriculumUnit(id=f"ur-{level.lower()}-foundation",level=level,unit_number=1,title=f"اردو {level}",grammar_points=["A1 review"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=[f"Build {level} communication"],default_weeks=2)]
ASSESSMENT_BANK=[AssessmentQuestion(id=f"ur-a1-{i:03}",skill=s,difficulty="A1",question=q,options=o,correct=c) for i,(s,q,o,c) in enumerate([
("vocabulary","Which word means hello?",["سلام","شکریہ","گھر","پانی"],"سلام"),
("grammar","Which means 'I am a student'?",["میں طالب علم ہوں۔","وہ استاد ہے۔","میں گھر میں ہوں۔","یہ کتاب نہیں ہے۔"],"میں طالب علم ہوں۔"),
("grammar","Which sentence shows possession?",["یہ میری کتاب ہے۔","میں کام کرتا ہوں۔","آپ کہاں ہیں؟","میں مصروف نہیں ہوں۔"],"یہ میری کتاب ہے۔"),
("vocabulary","Which word means mother?",["ماں","والد","بہن","دوست"],"ماں"),
("vocabulary","What does قیمت mean?",["price","water","morning","help"],"price"),
("reading","کتاب میز پر ہے۔ Where is the book?",["On the table","At home","At the station","On the street"],"On the table"),
("grammar","Which sentence is negative?",["میں مصروف نہیں ہوں۔","میں مصروف ہوں۔","یہ کتاب ہے۔","وہ استاد ہے۔"],"میں مصروف نہیں ہوں۔"),
("communication","How do you ask for help?",["براہ کرم میری مدد کریں۔","خدا حافظ!","شکریہ۔","میرا نام علی ہے۔"],"براہ کرم میری مدد کریں۔"),
("communication","How do you ask someone to repeat?",["براہ کرم دوبارہ کہیں۔","سلام!","میں گھر میں ہوں۔","کل آؤں گا۔"],"براہ کرم دوبارہ کہیں۔"),
("vocabulary","What does کل mean here?",["tomorrow","today","morning","friend"],"tomorrow")
],1)]
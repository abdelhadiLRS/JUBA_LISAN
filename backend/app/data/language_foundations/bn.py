"""Bengali A1 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def g(s,t,m,e): return GrammarTopic(slug=s,title=t,level="A1",category="core",summary=m,explanation=m,examples=[GrammarExample(text=x) for x in e])
GRAMMAR_TOPICS=[g(*x) for x in [
("pronouns","Personal pronouns","Use আমি, তুমি/আপনি, সে and আমরা in basic sentences.",["আমি ছাত্র।","আপনি শিক্ষক।"]),
("copula","Identity and noun sentences","Build simple identity statements without an overt present-tense copula.",["আমি ছাত্র।","এটা বই।"]),
("demonstratives","Demonstratives","Use এই, ওই and সেই with familiar nouns.",["এই বইটি নতুন।","ওই বাড়িটি বড়।"]),
("questions","Question words","Ask what, where, who and how much.",["এটা কী?","আপনি কোথায় থাকেন?"]),
("present","Present verbs","Use common present forms for routines and current facts.",["আমি বাংলা পড়ি।","সে কাজ করে।"]),
("negation","Negation","Use না and নয় in simple negative sentences.",["আমি যাই না।","এটা বই নয়।"]),
("plural","Plural markers","Use common plural markers such as -রা and -গুলো.",["ছাত্ররা আসে।","বইগুলো টেবিলে আছে।"]),
("postpositions","Postpositions","Use -এ and সঙ্গে for location and accompaniment.",["আমি বাড়িতে আছি।","বন্ধুর সঙ্গে যাই।"])
]]
def v(i,t,ws): return VocabularySet(id=i,level="A1",topic=t,unit_ref="bn-a1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in ws])
VOCABULARY_SETS=[v(*x) for x in [
("greetings_a1","Greetings",[("নমস্কার","phrase","hello","নমস্কার!"),("হ্যালো","phrase","hello","হ্যালো, কেমন আছেন?"),("ধন্যবাদ","phrase","thank you","ধন্যবাদ।"),("নাম","noun","name","আমার নাম রাহুল।")]),
("family_a1","Family",[("মা","noun","mother","আমার মা বাড়িতে আছেন।"),("বাবা","noun","father","আমার বাবা কাজ করেন।"),("ভাই","noun","brother","আমার ভাই ছাত্র।"),("বোন","noun","sister","আমার বোন স্কুলে যায়।")]),
("home_a1","Home",[("বাড়ি","noun","home","আমার বাড়ি ঢাকায়।"),("ঘর","noun","room","ঘরটি পরিষ্কার।"),("টেবিল","noun","table","বইটি টেবিলে আছে।"),("দরজা","noun","door","দরজা খোলা।")]),
("daily_a1","Daily life",[("সকাল","noun","morning","সকালে আমি কাজ করি।"),("কাজ করা","verb","to work","আমি প্রতিদিন কাজ করি।"),("পড়া","verb","to read/study","আমি রাতে পড়ি।"),("ঘুমানো","verb","to sleep","আমি রাতে ঘুমাই।")]),
("food_a1","Food and shopping",[("জল","noun","water","আমি জল চাই।"),("ভাত","noun","rice","আমি ভাত খাই।"),("চা","noun","tea","আমি চা পান করি।"),("দাম","noun","price","এটার দাম কত?")]),
("places_a1","Places and directions",[("রাস্তা","noun","street","এই রাস্তা কোথায় যায়?"),("স্টেশন","noun","station","স্টেশন কোথায়?"),("ডান","noun","right","ডান দিকে যান।"),("বাম","noun","left","বাম দিকে যান।")]),
("communication_a1","Communication",[("সাহায্য","noun","help","আমার সাহায্য দরকার।"),("দয়া করে","phrase","please","দয়া করে আবার বলুন।"),("বোঝা","verb","to understand","আমি বুঝতে পারছি না।"),("আবার","adverb","again","দয়া করে আবার বলুন।")]),
("review_a1","A1 review",[("আজ","adverb","today","আজ আমি বাড়িতে আছি।"),("কাল","adverb","tomorrow","কাল আমি স্কুলে যাব।"),("বন্ধু","noun","friend","সে আমার বন্ধু।"),("সময়","noun","time","আমার সময় আছে।")])
]]
def p(i,s,items): return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register="neutral") for t,c in items])
PHRASEBOOK_CATEGORIES=[p(*x) for x in [
("greetings_a1","Greetings",[("নমস্কার!","greeting"),("আমার নাম রাহুল।","introducing yourself"),("আমি বাংলাদেশ থেকে এসেছি।","saying where you are from")]),
("shopping_a1","Shopping",[("এটার দাম কত?","asking price"),("আমি এক কেজি ভাত চাই।","requesting an item"),("কার্ডে দিতে পারি?","asking about payment")]),
("directions_a1","Directions",[("স্টেশন কোথায়?","asking location"),("ডান দিকে যান।","giving directions"),("এখান থেকে কত দূর?","checking distance")]),
("help_a1","Help",[("আমাকে সাহায্য করুন।","asking for help"),("আমি বুঝতে পারছি না।","clarification"),("দয়া করে ধীরে বলুন।","asking someone to slow down")])
]]
def u(i,t,g,v,a,b): return CurriculumUnit(id=f"bn-a1-unit-{i}",level="A1",unit_number=i,title=t,grammar_points=g,vocabulary_set_ids=[v],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=[a,b],default_weeks=2)
CURRICULUM={"A1":[u(1,"পরিচয়",["pronouns","copula"],"greetings_a1","Introduce yourself","Exchange greetings"),u(2,"পরিবার",["pronouns","plural"],"family_a1","Describe family","Ask about relatives"),u(3,"বাড়ি",["demonstratives","postpositions"],"home_a1","Describe your home","Locate objects"),u(4,"দৈনন্দিন জীবন",["present","negation"],"daily_a1","Talk about routines","Say what you do not do"),u(5,"খাবার ও কেনাকাটা",["questions","negation"],"food_a1","Buy basic food","Ask prices"),u(6,"জায়গা ও দিকনির্দেশ",["postpositions","questions"],"places_a1","Ask directions","Give a simple route"),u(7,"যোগাযোগ",["questions","negation"],"communication_a1","Ask for help","Repair a misunderstanding"),u(8,"A1 পুনরাবৃত্তি",["pronouns","present","questions"],"review_a1","Review core A1","Handle familiar exchanges")]}
for level in ["A2","B1","B2","C1","C2"]: CURRICULUM[level]=[CurriculumUnit(id=f"bn-{level.lower()}-foundation",level=level,unit_number=1,title=f"Bengali {level}",grammar_points=["review A1"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=[f"Build {level} communication"],default_weeks=2)]
ASSESSMENT_BANK=[AssessmentQuestion(id=f"bn-a1-{i:03}",skill=s,difficulty="A1",question=q,options=o,correct=c) for i,(s,q,o,c) in enumerate([
("vocabulary","Which word means hello?",["নমস্কার","স্টেশন","জল","বই"],"নমস্কার"),
("grammar","Which sentence means 'I am a student'?",["আমি ছাত্র।","সে শিক্ষক।","আমি যাই না।","বইটি টেবিলে আছে।"],"আমি ছাত্র।"),
("grammar","Which is a question asking 'What is this?'",["এটা কী?","আমি বাংলা পড়ি।","এটা বই নয়।","সে কাজ করে।"],"এটা কী?"),
("vocabulary","Which word means mother?",["মা","বাবা","বন্ধু","ভাই"],"মা"),
("vocabulary","Which word means price?",["দাম","সকাল","সাহায্য","নাম"],"দাম"),
("reading","বইটি টেবিলে আছে। Where is the book?",["On the table","At the station","In the street","At school"],"On the table"),
("grammar","Which sentence is negative?",["আমি যাই না।","আমি যাই।","আমি ছাত্র।","এটা বই।"],"আমি যাই না।"),
("communication","Which phrase asks for help?",["আমাকে সাহায্য করুন।","ধন্যবাদ।","নমস্কার।","বিদায়।"],"আমাকে সাহায্য করুন।"),
("communication","Which phrase asks someone to repeat?",["দয়া করে আবার বলুন।","নমস্কার!","আমার নাম রাহুল।","কাল যাব।"],"দয়া করে আবার বলুন।"),
("vocabulary","What does কাল mean in this lesson?",["tomorrow","today","morning","friend"],"tomorrow")
],1)]
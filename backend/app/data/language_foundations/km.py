"""Khmer A1 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion
LEVELS=["A1","A2","B1","B2","C1","C2"]
def g(slug,title,summary,ex): return GrammarTopic(slug=slug,title=title,level="A1",category="core",summary=summary,explanation=summary,examples=[GrammarExample(text=x) for x in ex])
GRAMMAR_TOPICS=[g(*x) for x in [
("pronouns","Personal pronouns","Use ខ្ញុំ, អ្នក and គាត់ in simple statements.",["ខ្ញុំជាសិស្ស។","អ្នកជាគ្រូ។"]),
("copula","Identity statements","Use ជា to identify people and things.",["គាត់ជាគ្រូ។","នេះជាសៀវភៅ។"]),
("negation","Negation","Use មិន...ទេ for simple negative statements.",["ខ្ញុំមិនមែនជាគ្រូទេ។","ខ្ញុំមិននៅផ្ទះទេ។"]),
("questions","Basic questions","Form everyday questions with អ្វី, ណា and ណា.",["នេះជាអ្វី?","អ្នកនៅឯណា?"]),
("demonstratives","Demonstratives","Point to people and objects with នេះ and នោះ.",["នេះជាផ្ទះ។","នោះជាសាលា។"]),
("numbers","Numbers and quantity","Use basic numbers with familiar nouns.",["ខ្ញុំមានសៀវភៅពីរ។","មានមនុស្សបីនាក់។"]),
("time","Time expressions","Talk about today, tomorrow and simple times.",["ថ្ងៃនេះខ្ញុំធ្វើការ។","ស្អែកខ្ញុំទៅសាលា។"]),
("location","Location and movement","Use នៅ and ទៅ for location and movement.",["ខ្ញុំនៅផ្ទះ។","ខ្ញុំទៅផ្សារ។"])
]]
def v(i,t,ws): return VocabularySet(id=i,level="A1",topic=t,unit_ref="km-a1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in ws])
VOCABULARY_SETS=[v(*x) for x in [
("greetings_a1","Greetings",[("សួស្តី","phrase","hello","សួស្តី!"),("អរគុណ","phrase","thank you","អរគុណ។"),("លា","phrase","goodbye","លា!"),("ឈ្មោះ","noun","name","ខ្ញុំឈ្មោះសុភា។")]),
("family_a1","Family",[("ម្តាយ","noun","mother","ម្តាយខ្ញុំជាគ្រូ។"),("ឪពុក","noun","father","ឪពុកខ្ញុំធ្វើការ។"),("បង","noun","older sibling","បងខ្ញុំនៅផ្ទះ។"),("ប្អូន","noun","younger sibling","ប្អូនខ្ញុំទៅសាលា។")]),
("home_a1","Home",[("ផ្ទះ","noun","house","ផ្ទះខ្ញុំធំ។"),("បន្ទប់","noun","room","បន្ទប់នេះស្អាត។"),("តុ","noun","table","សៀវភៅនៅលើតុ។"),("ទ្វារ","noun","door","ទ្វារបើក។")]),
("daily_a1","Daily life",[("ព្រឹក","noun","morning","ព្រឹកនេះខ្ញុំធ្វើការ។"),("ទៅ","verb","go","ខ្ញុំទៅសាលា។"),("ធ្វើការ","verb","work","ខ្ញុំធ្វើការ។"),("ដេក","verb","sleep","ខ្ញុំដេកនៅយប់។")]),
("food_a1","Food and shopping",[("ទឹក","noun","water","ខ្ញុំចង់បានទឹក។"),("បាយ","noun","rice","ខ្ញុំញ៉ាំបាយ។"),("កាហ្វេ","noun","coffee","ខ្ញុំផឹកកាហ្វេ។"),("តម្លៃ","noun","price","តម្លៃប៉ុន្មាន?")]),
("places_a1","Places and directions",[("ផ្សារ","noun","market","ផ្សារនៅជិត។"),("សាលា","noun","school","សាលានៅទីនេះ។"),("ស្តាំ","noun","right","ទៅខាងស្តាំ។"),("ឆ្វេង","noun","left","ទៅខាងឆ្វេង។")]),
("communication_a1","Communication",[("ជួយ","verb","help","សូមជួយខ្ញុំ។"),("សូម","adverb","please","សូមនិយាយម្តងទៀត។"),("យល់","verb","understand","ខ្ញុំមិនយល់ទេ។"),("ម្តងទៀត","adverb","again","សូមនិយាយម្តងទៀត។")]),
("review_a1","A1 review",[("ថ្ងៃនេះ","adverb","today","ថ្ងៃនេះខ្ញុំនៅផ្ទះ។"),("ស្អែក","adverb","tomorrow","ស្អែកខ្ញុំទៅធ្វើការ។"),("មិត្ត","noun","friend","គាត់ជាមិត្តខ្ញុំ។"),("ពេល","noun","time","ខ្ញុំមានពេល។")])]]
def p(i,s,items): return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register="neutral") for t,c in items])
PHRASEBOOK_CATEGORIES=[p(*x) for x in [
("greetings_a1","Greetings",[("សួស្តី!","greeting"),("ខ្ញុំឈ្មោះសុភា។","introducing yourself")]),
("shopping_a1","Shopping",[("តម្លៃប៉ុន្មាន?","asking price"),("ខ្ញុំចង់បានមួយ។","requesting an item")]),
("directions_a1","Directions",[("ផ្សារនៅឯណា?","asking location"),("ទៅខាងស្តាំ។","giving directions")]),
("help_a1","Help",[("សូមជួយខ្ញុំ។","asking for help"),("ខ្ញុំមិនយល់ទេ។","asking for clarification")])]]
def unit(i,title,g,v,c1,c2): return CurriculumUnit(id=f"km-a1-unit-{i}",level="A1",unit_number=i,title=title,grammar_points=g,vocabulary_set_ids=[v],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=[c1,c2],default_weeks=2)
CURRICULUM={"A1":[unit(1,"ការស្វាគមន៍",["pronouns","copula"],"greetings_a1","Introduce yourself","Exchange greetings"),unit(2,"គ្រួសារ",["pronouns","demonstratives"],"family_a1","Describe family","Ask about relatives"),unit(3,"ផ្ទះ",["demonstratives","location"],"home_a1","Describe your home","Locate objects"),unit(4,"ជីវិតប្រចាំថ្ងៃ",["questions","negation"],"daily_a1","Talk about routines","State simple negatives"),unit(5,"អាហារ និងការទិញ",["questions","numbers"],"food_a1","Buy basic food","Ask prices"),unit(6,"ទីកន្លែង",["location","questions"],"places_a1","Ask directions","Give directions"),unit(7,"ការទំនាក់ទំនង",["negation","questions"],"communication_a1","Ask for help","Clarify meaning"),unit(8,"ពិនិត្យ A1",["time","numbers"],"review_a1","Review familiar topics","Handle basic exchanges")]}
for level in LEVELS[1:]: CURRICULUM[level]=[CurriculumUnit(id=f"km-{level.lower()}-foundation",level=level,unit_number=1,title=f"Khmer {level}",grammar_points=["A1 review"],vocabulary_set_ids=["review_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=[f"Build {level} communication"],default_weeks=2)]
ASSESSMENT_BANK=[AssessmentQuestion(id=f"km-a1-{i:03}",skill=s,difficulty="A1",question=q,options=o,correct=c) for i,(s,q,o,c) in enumerate([
("vocabulary","What does សួស្តី mean?",["hello","goodbye","water","market"],"hello"),("grammar","Which is a negative statement?",["ខ្ញុំមិនយល់ទេ។","ខ្ញុំយល់។","នេះជាសៀវភៅ។","ខ្ញុំទៅផ្សារ។"],"ខ្ញុំមិនយល់ទេ។"),("vocabulary","What is ម្តាយ?",["mother","father","friend","teacher"],"mother"),("grammar","How do you ask 'What is this?'",["នេះជាអ្វី?","អ្នកនៅឯណា?","តម្លៃប៉ុន្មាន?","សួស្តី!"],"នេះជាអ្វី?"),("vocabulary","What does ទឹក mean?",["water","rice","coffee","bread"],"water"),("reading","សៀវភៅនៅលើតុ។ Where is the book?",["On the table","At school","In the market","At home"],"On the table"),("communication","How do you ask for help?",["សូមជួយខ្ញុំ។","អរគុណ។","លា!","ស្អែកខ្ញុំទៅ។"],"សូមជួយខ្ញុំ។"),("vocabulary","What does ស្អែក mean?",["tomorrow","today","morning","right"],"tomorrow"),("grammar","Which sentence says 'I am at home'?",["ខ្ញុំនៅផ្ទះ។","ខ្ញុំទៅសាលា។","ខ្ញុំមិនយល់ទេ។","នេះជាផ្ទះ។"],"ខ្ញុំនៅផ្ទះ។"),("communication","What can you say when you do not understand?",["ខ្ញុំមិនយល់ទេ។","អរគុណ។","សួស្តី។","លា។"],"ខ្ញុំមិនយល់ទេ។")],1)]

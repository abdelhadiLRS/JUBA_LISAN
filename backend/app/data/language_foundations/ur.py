"""اردو foundation data for JUBA LISAN — A1–C2."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

def _g(slug,title,level,category,summary,examples,rules=None):
    return GrammarTopic(slug=slug,title=title,level=level,category=category,summary=summary,explanation=summary,rules=rules or [],examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS=[
_g("pronouns","ضمائر شخصی","A1","syntax","میں، آپ، تم، وہ اور ہم کو بنیادی جملوں میں استعمال کریں۔",["میں طالب علم ہوں۔","آپ استاد ہیں۔"]),
_g("identity","ہونا: ہوں، ہے، ہیں","A1","grammar","شناخت اور تعارف کے جملے بنائیں۔",["میں ڈاکٹر ہوں۔","وہ استاد ہے۔"]),
_g("possessive","ملکیت: میرا، میری، میرے","A1","morphology","ملکیت کو جنس اور عدد کے مطابق ظاہر کریں۔",["یہ میری کتاب ہے۔","یہ میرا گھر ہے۔"]),
_g("location","مقامی حروف: میں، پر","A1","syntax","جگہ اور مقام بتائیں۔",["میں گھر میں ہوں۔","کتاب میز پر ہے۔"]),
_g("questions","استفہامی الفاظ","A1","syntax","کیا، کہاں، کون، کب اور کتنے سے سوال کریں۔",["آپ کہاں ہیں؟","یہ کیا ہے؟"]),
_g("negation","نفی: نہیں","A1","syntax","بنیادی جملوں کی نفی کریں۔",["میں مصروف نہیں ہوں۔","یہ میری کتاب نہیں ہے۔"]),
_g("present","حال عادی","A1","verbs","روزمرہ عادات اور معمولات بیان کریں۔",["میں روز کام کرتا ہوں۔","وہ اردو پڑھتی ہے۔"]),
_g("plural","اسم کی جمع","A1","morphology","عام جمع اور اسم و فعل کی مطابقت سمجھیں۔",["کتابیں میز پر ہیں۔"]),
_g("past","ماضی سادہ","A2","verbs","مکمل ہو چکے واقعات بیان کریں؛ متعدی جملوں میں ergative انداز پہچانیں۔",["میں نے کتاب پڑھی۔","وہ کل آیا۔"]),
_g("future","مستقبل","A2","verbs","مستقبل کے ارادے اور واقعات بیان کریں۔",["میں کل جاؤں گا۔","وہ اگلے ہفتے آئے گی۔"]),
_g("postpositions","حروفِ اضافت","A2","syntax","کے، کو، سے، میں، پر اور لیے کے استعمال کو سمجھیں۔",["علی کے ساتھ جاؤ۔","مجھے دوست کو بلانا ہے۔"]),
_g("imperative","امریہ اور مؤدبانہ درخواست","A2","pragmatics","حکم، مشورہ اور درخواست کو مناسب انداز میں کہیں۔",["براہ کرم بیٹھیں۔","ذرا آہستہ بولیں۔"]),
_g("comparative","تقابل","A2","adjectives","زیادہ، کم، سب سے اور سے کے ذریعے موازنہ کریں۔",["یہ کتاب اس سے زیادہ دلچسپ ہے۔","یہ سب سے اچھا راستہ ہے۔"]),
_g("modal","چاہیے، سکتا، ممکن","A2","modality","ضرورت، قابلیت اور امکان ظاہر کریں۔",["مجھے آج کام کرنا چاہیے۔","میں اردو بول سکتا ہوں۔"]),
_g("perfect","ماضی کامل","B1","verbs","ماضی کے مکمل تجربات اور نتائج بیان کریں۔",["میں لاہور جا چکا ہوں۔","وہ کام کر چکی ہے۔"]),
_g("progressive","جاری عمل","B1","aspect","رہے ہونا کے ذریعے جاری عمل بیان کریں۔",["میں کتاب پڑھ رہا ہوں۔","وہ کام کر رہی ہے۔"]),
_g("conditional","اگر...تو","B1","syntax","شرط، امکان اور نتیجہ بیان کریں۔",["اگر وقت ہو تو آئیں۔","اگر بارش ہوئی تو ہم گھر رہیں گے۔"]),
_g("relative","جو، جس، جسے","B1","syntax","متعلقہ جملوں سے لوگوں اور چیزوں کی وضاحت کریں۔",["جو لڑکا آیا تھا وہ میرا بھائی ہے۔","یہ وہ کتاب ہے جسے میں پڑھ رہا ہوں۔"]),
_g("reported","بالواسطہ کلام","B1","syntax","کسی کے قول یا خیال کو بالواسطہ بیان کریں۔",["اس نے کہا کہ وہ کل آئے گا۔","مجھے معلوم ہوا کہ وہ مصروف ہے۔"]),
_g("causative","سببیت","B2","verbs","کسی سے کام کروانے کے مفہوم کو بیان کریں۔",["استاد نے طلبہ سے مشق کروائی۔","اس نے بچے کو سلا دیا۔"]),
_g("passive","مجہول","B2","verbs","عمل پر توجہ مرکوز کرنے کے لیے مجہول ساخت استعمال کریں۔",["خط لکھا گیا۔","دروازہ بند کر دیا گیا۔"]),
_g("concession","اگرچہ...لیکن","B2","discourse","تضاد، رعایت اور پیچیدہ دلیل قائم کریں۔",["اگرچہ وقت کم تھا، لیکن ہم نے کام مکمل کیا۔"]),
_g("connectors","ربط کے الفاظ","B2","discourse","وجہ، نتیجہ، تضاد اور اضافہ واضح کریں۔",["اس لیے ہم دیر سے پہنچے۔","مزید برآں، نتائج بھی بہتر ہوئے۔"]),
_g("register","رسمی اور پیشہ ورانہ اردو","B2","register","اداروں اور کام کی جگہ پر مناسب رجسٹر اختیار کریں۔",["براہ کرم مطلوبہ دستاویزات فراہم کریں۔"]),
_g("subordination","پیچیدہ تابع جملے","C1","syntax","متعدد تابع جملوں کو منطقی ربط سے جوڑیں۔",["چونکہ اجلاس مؤخر ہوا، اس لیے رپورٹ بھی بعد میں جاری کی گئی۔"]),
_g("nominalization","اسمیہ سازی","C1","academic","عمل کو رسمی اسمیہ تراکیب میں پیکج کریں۔",["منصوبے کی تکمیل سے کارکردگی میں بہتری آئی۔"]),
_g("hedging","علمی احتیاط","C1","academic","دعویٰ، امکان اور ثبوت کے درمیان درست درجہ بندی کریں۔",["یہ نتیجہ بعض حالات میں درست ہو سکتا ہے۔"]),
_g("formal-writing","رسمی تحریر","C1","register","رپورٹ، درخواست اور ادارہ جاتی متن لکھیں۔",["اس سلسلے میں ضروری کارروائی کی درخواست ہے۔"]),
_g("argumentation","استدلال","C1","rhetoric","دعویٰ، ثبوت، اعتراض اور نتیجہ منظم کریں۔",["دستیاب شواہد کی بنیاد پر یہ نتیجہ اخذ کیا جا سکتا ہے۔"]),
_g("information-structure","موضوع اور focus","C2","discourse","الفاظ کی ترتیب سے معلوماتی ترجیح اور تقابل پیدا کریں۔",["اصل مسئلہ یہی ہے کہ وسائل محدود ہیں۔"]),
_g("idioms","محاورات اور استعارات","C2","pragmatics","محاوراتی معنی کو سیاق، رجسٹر اور ثقافتی اشاروں کے ساتھ سمجھیں۔",["اس نے آسمان سر پر اٹھا لیا۔"]),
_g("rhetoric","بلاغت اور اسلوب","C2","rhetoric","پیچیدہ رسمی اور ادبی اظہار میں لہجے اور زور کو کنٹرول کریں۔",["یہ سوال محض انتظامی نہیں بلکہ بنیادی اصولوں سے متعلق ہے۔"]),
_g("translation","ترجمہ اور معنی","C2","translation","لفظی اور سیاقی معنی کے فرق کو حل کریں۔",["اس اصطلاح کا مناسب ترجمہ سیاق پر منحصر ہے۔"]),
_g("literary-register","ادبی رجسٹر","C2","literary","ادبی زبان میں تشبیہ، استعارہ اور صوتی و نحوی انتخاب کو پہچانیں۔",["خاموش شہر پر شام کی روشنی پھیل گئی۔"])
]

def _v(id_,level,topic,unit,items):
    return VocabularySet(id=id_,level=level,topic=topic,unit_ref=unit,words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in items])

VOCABULARY_SETS=[
_v("greetings_a1","A1","تعرف","ur-a1-unit-1",[("سلام","phrase","hello","سلام!"),("شکریہ","phrase","thank you","شکریہ۔"),("خدا حافظ","phrase","goodbye","خدا حافظ!"),("نام","noun","name","میرا نام علی ہے۔")]),
_v("family_a1","A1","خاندان","ur-a1-unit-2",[("ماں","noun","mother","میری ماں گھر میں ہیں۔"),("والد","noun","father","میرے والد کام کرتے ہیں۔"),("بھائی","noun","brother","میرا بھائی طالب علم ہے۔"),("بہن","noun","sister","میری بہن اسکول جاتی ہے۔")]),
_v("home_a1","A1","گھر","ur-a1-unit-3",[("گھر","noun","home","میرا گھر قریب ہے۔"),("کمرہ","noun","room","کمرہ صاف ہے۔"),("میز","noun","table","کتاب میز پر ہے۔"),("دروازہ","noun","door","دروازہ کھلا ہے۔")]),
_v("daily_a1","A1","روزمرہ","ur-a1-unit-4",[("صبح","noun","morning","صبح میں کام کرتا ہوں۔"),("کام کرنا","verb","to work","میں روز کام کرتا ہوں۔"),("پڑھنا","verb","to study/read","میں شام کو پڑھتا ہوں۔"),("سونا","verb","to sleep","میں رات کو سوتا ہوں۔")]),
_v("food_a1","A1","کھانا","ur-a1-unit-5",[("پانی","noun","water","مجھے پانی چاہیے۔"),("روٹی","noun","bread","میں روٹی خریدتا ہوں۔"),("چائے","noun","tea","میں چائے پیتا ہوں۔"),("قیمت","noun","price","اس کی قیمت کتنی ہے؟")]),
_v("places_a1","A1","مقامات","ur-a1-unit-6",[("سڑک","noun","street","یہ سڑک کہاں جاتی ہے؟"),("اسٹیشن","noun","station","اسٹیشن کہاں ہے؟"),("دائیں","adverb","right","دائیں جائیں۔"),("بائیں","adverb","left","بائیں جائیں۔")]),
_v("past_a2","A2","ماضی","ur-a2-unit-1",[("کل","adverb","yesterday/tomorrow","کل میں لاہور گیا تھا۔"),("کل","adverb","tomorrow","کل میں کام کروں گا۔"),("ملنا","verb","to meet","ہم کل ملے۔"),("خریدنا","verb","to buy","میں نے کتاب خریدی۔")]),
_v("travel_a2","A2","سفر","ur-a2-unit-2",[("سفر","noun","journey","سفر آرام دہ تھا۔"),("ٹکٹ","noun","ticket","مجھے ٹکٹ چاہیے۔"),("راستہ","noun","route","یہ راستہ اسٹیشن جاتا ہے۔"),("منزل","noun","destination","ہم منزل پر پہنچ گئے۔")]),
_v("health_a2","A2","صحت","ur-a2-unit-3",[("درد","noun","pain","میرے سر میں درد ہے۔"),("دوا","noun","medicine","ڈاکٹر نے دوا دی۔"),("آرام","noun","rest","آپ کو آرام کرنا چاہیے۔"),("بخار","noun","fever","اسے بخار ہے۔")]),
_v("study_b1","B1","تعلیم","ur-b1-unit-4",[("تحقیق","noun","research","وہ زبان پر تحقیق کر رہا ہے۔"),("تجربہ","noun","experience/experiment","اس تجربے کا نتیجہ اہم ہے۔"),("مہارت","noun","skill","مواصلاتی مہارت ضروری ہے۔"),("مضمون","noun","article/essay","میں نے ایک مضمون لکھا۔")]),
_v("work_b2","B2","پیشہ ورانہ زبان","ur-b2-unit-5",[("رپورٹ","noun","report","رپورٹ تیار ہے۔"),("اجلاس","noun","meeting","اجلاس دس بجے ہے۔"),("دستاویز","noun","document","دستاویز فراہم کریں۔"),("ذمہ داری","noun","responsibility","یہ میری ذمہ داری ہے۔")]),
_v("academic_c1","C1","علمی زبان","ur-c1-unit-2",[("شواہد","noun","evidence","دستیاب شواہد محدود ہیں۔"),("نتیجہ","noun","conclusion/result","نتیجہ واضح ہے۔"),("تجزیہ","noun","analysis","تجزیہ مزید تحقیق چاہتا ہے۔"),("مفروضہ","noun","hypothesis","مفروضے کی جانچ کی گئی۔")]),
_v("rhetoric_c2","C2","بلاغت","ur-c2-unit-2",[("سیاق","noun","context","لفظ کا مفہوم سیاق سے بدل سکتا ہے۔"),("لہجہ","noun","tone","تحریر کا لہجہ رسمی ہے۔"),("استعارہ","noun","metaphor","شاعر نے خوب صورت استعارہ استعمال کیا۔"),("نکتہ","noun","point/nuance","اس نکتے پر مزید غور ضروری ہے۔")]),
]

def _unit(level,n,title,grammar,vocab,checks):
    return CurriculumUnit(id=f"ur-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=grammar,vocabulary_set_ids=[vocab],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=checks,default_weeks=2)

_PLAN={
"A1":[("سلام اور تعارف","pronouns","greetings_a1",["سلام اور تعارف کریں","اپنا نام بتائیں"]),("خاندان","possessive","family_a1",["خاندان بیان کریں","ملکیت بتائیں"]),("گھر","location","home_a1",["گھر بیان کریں","اشیا کی جگہ بتائیں"]),("روزمرہ زندگی","present","daily_a1",["معمول بیان کریں","سادہ نفی کریں"]),("کھانا اور خریداری","questions","food_a1",["قیمت پوچھیں","بنیادی خریداری کریں"]),("مقامات اور راستے","location","places_a1",["راستہ پوچھیں","سادہ ہدایات دیں"])],
"A2":[("ماضی","past","past_a2",["ماضی کے واقعات بیان کریں","ماضی کے متعدی جملے سمجھیں"]),("سفر","postpositions","travel_a2",["سفر کا انتظام کریں","راستہ اور منزل بیان کریں"]),("صحت","modal","health_a2",["علامات بیان کریں","ضرورت اور مشورہ دیں"]),("موازنہ","comparative","travel_a2",["اختیارات کا موازنہ کریں","ترجیحات بیان کریں"]),("منصوبے","future","past_a2",["مستقبل کے منصوبے بتائیں","ارادے بیان کریں"]),("درخواستیں","imperative","health_a2",["مؤدبانہ درخواست کریں","ہدایات سمجھیں"])],
"B1":[("تجربات","perfect","study_b1",["تجربات بیان کریں","مکمل اعمال کو مربوط کریں"]),("جاری عمل","progressive","study_b1",["جاری عمل بیان کریں","پس منظر قائم کریں"]),("شرط","conditional","study_b1",["شرائط بیان کریں","ممکنہ نتائج سمجھائیں"]),("متعلقہ جملے","relative","study_b1",["تفصیلی وضاحت کریں","پیچیدہ اسم گروپ سمجھیں"]),("رپورٹ شدہ کلام","reported","study_b1",["دوسروں کی بات نقل کریں","رپورٹ کا مفہوم سمجھیں"]),("تعلیم و تحقیق","perfect","study_b1",["تعلیمی موضوعات پر گفتگو کریں","دلائل کا خلاصہ کریں"])],
"B2":[("سببیت","causative","work_b2",["سبب اور نتیجہ بیان کریں","سببیتی ساخت سمجھیں"]),("مجہول","passive","work_b2",["رسمی مجہول جملے سمجھیں","عمل پر توجہ مرکوز کریں"]),("تضاد","concession","work_b2",["رعایت کے ساتھ دلیل دیں","متضاد خیالات جوڑیں"]),("ربط","connectors","work_b2",["منطقی ربط قائم کریں","نتائج واضح کریں"]),("پیشہ ورانہ اردو","register","work_b2",["ادارتی گفتگو کریں","رسمی درخواست لکھیں"]),("رسمی دستاویزات","register","work_b2",["رپورٹ سمجھیں","ادارہ جاتی ہدایات لکھیں"])],
"C1":[("پیچیدہ جملے","subordination","academic_c1",["تابع جملوں سے استدلال کریں","منطقی تعلق واضح کریں"]),("اسمیہ سازی","nominalization","academic_c1",["علمی اسلوب استعمال کریں","عمل کو اسمیہ تراکیب میں بدلیں"]),("احتیاطی دعوے","hedging","academic_c1",["دعویٰ محدود کریں","ثبوت اور امکان میں فرق کریں"]),("رسمی تحریر","formal-writing","academic_c1",["درخواست اور رپورٹ لکھیں","ادارہ جاتی لہجہ برقرار رکھیں"]),("استدلال","argumentation","academic_c1",["ثبوت کے ساتھ دلیل دیں","اعتراض کا جواب دیں"]),("تحقیقی خلاصہ","argumentation","academic_c1",["تحقیق کا خلاصہ لکھیں","نتیجہ اخذ کریں"])],
"C2":[("موضوع اور focus","information-structure","rhetoric_c2",["معلوماتی ترجیح کو کنٹرول کریں","تقابلی زور پیدا کریں"]),("محاورات","idioms","rhetoric_c2",["محاوراتی معنی سمجھیں","ثقافتی سیاق پہچانیں"]),("بلاغت","rhetoric","rhetoric_c2",["پیچیدہ دلیل بنائیں","لہجہ اور زور کنٹرول کریں"]),("ترجمہ","translation","rhetoric_c2",["سیاقی معنی حل کریں","رجسٹر منتقل کریں"]),("ادبی زبان","literary-register","rhetoric_c2",["ادبی متن کا تجزیہ کریں","اسلوبی انتخاب سمجھیں"]),("حتمی تکمیل","rhetoric","rhetoric_c2",["مختلف رجسٹرز میں روانی سے اظہار کریں","پیچیدہ متن کی تنقیدی تعبیر کریں"])]
}
CURRICULUM={level:[_unit(level,i+1,t,g,v,c) for i,(t,g,v,c) in enumerate(items)] for level,items in _PLAN.items()}

PHRASEBOOK_CATEGORIES=[
PhrasebookCategory(id="greetings_a1",level="A1",situation="سلام اور تعارف",icon="👋",phrases=[PhrasebookEntry("السلام علیکم!","greeting","formal"),PhrasebookEntry("میرا نام ... ہے۔","introducing yourself","neutral"),PhrasebookEntry("آپ کیسے ہیں؟","asking how someone is","neutral"),PhrasebookEntry("میں الجزائر سے ہوں۔","saying where you are from","neutral")]),
PhrasebookCategory(id="daily_a2",level="A2",situation="روزمرہ ضروریات",icon="☀️",phrases=[PhrasebookEntry("مجھے ... چاہیے۔","stating a need","neutral"),PhrasebookEntry("اس کی قیمت کتنی ہے؟","asking price","neutral"),PhrasebookEntry("مجھے ڈاکٹر سے ملنا ہے۔","explaining a need","neutral"),PhrasebookEntry("ذرا آہستہ بولیں۔","asking someone to slow down","neutral")]),
PhrasebookCategory(id="travel_b1",level="B1",situation="سفر",icon="🧳",phrases=[PhrasebookEntry("یہ راستہ اسٹیشن جاتا ہے؟","checking route","neutral"),PhrasebookEntry("ٹکٹ کہاں سے ملے گا؟","buying a ticket","neutral"),PhrasebookEntry("یہاں سے کتنی دور ہے؟","asking distance","neutral"),PhrasebookEntry("مجھے منزل تک پہنچنا ہے۔","stating destination","neutral")]),
PhrasebookCategory(id="work_b2",level="B2",situation="پیشہ ورانہ گفتگو",icon="💼",phrases=[PhrasebookEntry("براہ کرم مطلوبہ دستاویزات فراہم کریں۔","formal request","formal"),PhrasebookEntry("اس مسئلے پر گفتگو کرتے ہیں۔","suggesting discussion","neutral"),PhrasebookEntry("رپورٹ کب تک مکمل ہوگی؟","asking about deadline","formal"),PhrasebookEntry("مزید معلومات درکار ہیں۔","requesting information","formal")]),
PhrasebookCategory(id="academic_c1",level="C1",situation="علمی گفتگو",icon="📚",phrases=[PhrasebookEntry("دستیاب شواہد کی بنیاد پر...","introducing evidence","formal"),PhrasebookEntry("اس نتیجے کو احتیاط سے دیکھنا چاہیے۔","qualifying a conclusion","formal"),PhrasebookEntry("دوسری جانب، ...","introducing contrast","formal"),PhrasebookEntry("مزید تحقیق کی ضرورت ہے۔","identifying a research gap","formal")]),
PhrasebookCategory(id="debate_c2",level="C2",situation="مباحثہ اور پیچیدہ استدلال",icon="🗣️",phrases=[PhrasebookEntry("میں اس نکتے سے جزوی طور پر متفق ہوں۔","qualified agreement","neutral"),PhrasebookEntry("اس مسئلے کا ایک اور پہلو بھی ہے۔","introducing another aspect","neutral"),PhrasebookEntry("اگرچہ یہ دلیل قابلِ غور ہے، تاہم...","concession","formal"),PhrasebookEntry("سیاق کو نظر انداز کرنا مناسب نہیں ہوگا۔","challenging an interpretation","formal")])
]

ASSESSMENT_BANK=[
AssessmentQuestion(id="ur-a1-001",skill="grammar",difficulty="A1",question="صحیح جملہ منتخب کریں: I am a student.",options=["میں طالب علم ہوں۔","وہ استاد ہے۔","میں گھر میں ہوں۔","یہ کتاب ہے۔"],correct="میں طالب علم ہوں۔",grammar_slug="identity"),
AssessmentQuestion(id="ur-a1-002",skill="vocabulary",difficulty="A1",question="کون سا لفظ mother کا مطلب رکھتا ہے؟",options=["ماں","والد","بھائی","دوست"],correct="ماں"),
AssessmentQuestion(id="ur-a2-001",skill="grammar",difficulty="A2",question="ماضی کا درست جملہ کون سا ہے؟",options=["میں نے کتاب پڑھی۔","میں کتاب پڑھتا ہوں۔","میں کتاب پڑھ رہا ہوں۔","میں کتاب پڑھوں گا۔"],correct="میں نے کتاب پڑھی۔",grammar_slug="past"),
AssessmentQuestion(id="ur-a2-002",skill="grammar",difficulty="A2",question="کون سا جملہ مستقبل ظاہر کرتا ہے؟",options=["میں کل جاؤں گا۔","میں کل گیا تھا۔","میں جا رہا ہوں۔","میں گیا ہوں۔"],correct="میں کل جاؤں گا۔",grammar_slug="future"),
AssessmentQuestion(id="ur-b1-001",skill="grammar",difficulty="B1",question="شرطیہ جملہ منتخب کریں۔",options=["اگر وقت ہو تو آئیں۔","وقت بہت کم ہے۔","میں کل آیا تھا۔","وہ گھر میں ہے۔"],correct="اگر وقت ہو تو آئیں۔",grammar_slug="conditional"),
AssessmentQuestion(id="ur-b1-002",skill="reading",difficulty="B1",question="کون سا جملہ بالواسطہ کلام کی مثال ہے؟",options=["اس نے کہا کہ وہ کل آئے گا۔","وہ کل آئے گا۔","وہ کل آیا۔","وہ آ رہا ہے۔"],correct="اس نے کہا کہ وہ کل آئے گا۔",grammar_slug="reported"),
AssessmentQuestion(id="ur-b2-001",skill="grammar",difficulty="B2",question="مجہول ساخت منتخب کریں۔",options=["خط لکھا گیا۔","علی نے خط لکھا۔","علی خط لکھ رہا ہے۔","علی خط لکھے گا۔"],correct="خط لکھا گیا۔",grammar_slug="passive"),
AssessmentQuestion(id="ur-b2-002",skill="vocabulary",difficulty="B2",question="رسمی پیشہ ورانہ متن میں مطلوبہ کاغذ کو کیا کہتے ہیں؟",options=["دستاویز","سفر","محاورہ","لہجہ"],correct="دستاویز"),
AssessmentQuestion(id="ur-c1-001",skill="grammar",difficulty="C1",question="علمی احتیاط والا جملہ منتخب کریں۔",options=["یہ نتیجہ بعض حالات میں درست ہو سکتا ہے۔","یہ نتیجہ ہمیشہ درست ہے۔","یہ نتیجہ کبھی نہیں بدلتا۔","یہ نتیجہ بالکل قطعی ہے۔"],correct="یہ نتیجہ بعض حالات میں درست ہو سکتا ہے۔",grammar_slug="hedging"),
AssessmentQuestion(id="ur-c1-002",skill="reading",difficulty="C1",question="شواہد متعارف کرانے کے لیے کون سا فقرہ زیادہ رسمی ہے؟",options=["دستیاب شواہد کی بنیاد پر...","سلام!","آپ کیسے ہیں؟","خدا حافظ!"],correct="دستیاب شواہد کی بنیاد پر...",grammar_slug="argumentation"),
AssessmentQuestion(id="ur-c2-001",skill="grammar",difficulty="C2",question="رعایت اور تضاد کی ساخت منتخب کریں۔",options=["اگرچہ یہ دلیل قابلِ غور ہے، تاہم...","یہ دلیل واضح ہے۔","یہ دلیل ختم ہو گئی۔","دلیل موجود نہیں۔"],correct="اگرچہ یہ دلیل قابلِ غور ہے، تاہم...",grammar_slug="rhetoric"),
AssessmentQuestion(id="ur-c2-002",skill="reading",difficulty="C2",question="محاوراتی معنی سمجھنے میں سب سے اہم چیز کیا ہے؟",options=["سیاق اور رجسٹر","لفظ کی لمبائی","حروف کی تعداد","الفاظ کی ترتیب فقط"],correct="سیاق اور رجسٹر",grammar_slug="idioms")
]

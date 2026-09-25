"""Persian (فارسی) A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def _g(slug,title,level,summary,explanation,examples):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=summary,explanation=explanation,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS=[
_g("pronouns","ضمیرهای شخصی","A1","Introduce people and refer to participants.","Use من، تو، او، ما، شما، آنها in basic clauses.",["من دانشجو هستم.","او معلم است."]),
_g("ezafe","اضافه","A1","Link nouns to modifiers and possessors.","Use the ezafe construction to connect nouns, adjectives and names.",["کتابِ خوب","دوستِ علی"]),
_g("copula","فعل ربطی","A1","Express identity and description.","Use هستم، هستی، است، هستیم، هستید، هستند in present identity clauses.",["من ایرانی هستم.","آنها دانشجو هستند."]),
_g("negation","منفی‌سازی","A1","Negate nominal and verbal clauses.","Use نیست and نمی‌ with appropriate verb forms.",["این کتاب نیست.","من قهوه نمی‌نوشم."]),
_g("questions","واژه‌های پرسشی","A1","Ask practical questions.","Use چه، کی، کجا، چرا، چگونه، چند and related forms.",["این چیست؟","ایستگاه کجاست؟"]),
_g("present","حال اخباری","A1","Describe current and habitual actions.","Use می‌ plus the present stem and personal endings.",["فارسی می‌خوانم.","او کار می‌کند."]),
_g("plural","جمع بستن اسم","A1","Talk about more than one item.","Use ها and common plural patterns such as ان in appropriate contexts.",["کتاب‌ها روی میز هستند.","دانشجویان وارد کلاس شدند."]),
_g("prepositions","حرف‌های اضافه","A1","Express location and relations.","Use در، به، با، از، برای and common complements.",["در خانه هستم.","با دوستم به بازار می‌روم."]),
_g("past","گذشته ساده","A2","Talk about completed past events.","Form common past verbs with the past stem and personal endings.",["دیروز به مدرسه رفتم.","کتاب را خواندم."]),
_g("imperfective","گذشته استمراری و عادت","A2","Describe ongoing or habitual past events.","Use می‌ with past forms for repeated or ongoing situations.",["هر روز ورزش می‌کردم.","وقتی آمد، غذا می‌خوردم."]),
_g("future","آینده و قصد","A2","Talk about future events and plans.","Recognize formal future forms and common colloquial present-for-future usage.",["فردا خواهم آمد.","فردا به دانشگاه می‌روم."]),
_g("comparatives","صفت تفضیلی و عالی","A2","Compare people and things.","Use تر، ترین and از برای common comparisons.",["این کتاب بهتر است.","او از من سریع‌تر است."]),
_g("imperative","امر و درخواست مؤدبانه","A2","Give instructions and requests.","Use imperative forms and polite expressions such as لطفاً and می‌شود؟.",["لطفاً بنشینید.","این جمله را بخوان."]),
_g("object-marker","را و مفعول معین","A2","Mark definite direct objects.","Use را with definite and specific objects.",["کتاب را خواندم.","دوستم را دیدم."]),
_g("progressive","استمراری و در حال","B1","Describe actions in progress.","Use در حالِ ... بودن and contextual present/past forms.",["دارم کتاب می‌خوانم.","او در حال صحبت کردن است."]),
_g("perfect","گذشته نقلی","B1","Connect past events to the present.","Use past participle plus است forms and recognize evidential/resultative meanings.",["کتاب را خوانده‌ام.","او به تهران رفته است."]),
_g("conditional","شرطی","B1","Express hypothetical conditions.","Build اگر clauses and conditional consequences.",["اگر وقت داشته باشم، می‌آیم.","اگر می‌دانستم، کمک می‌کردم."]),
_g("relative","جمله‌واره موصولی","B1","Describe nouns through relative clauses.","Use که to link a noun to a descriptive clause.",["کتابی که خریدم جالب است.","مردی که آنجا ایستاده دوست من است."]),
_g("modality","وجهیت و الزام","B1","Express ability, necessity and possibility.","Use باید، می‌توانم، ممکن است and related constructions.",["باید امروز کار کنم.","ممکن است دیر برسد."]),
_g("causal","علت و نتیجه","B1","Explain reasons and consequences.","Connect propositions with چون، زیرا، بنابراین، پس and related markers.",["چون باران می‌بارید، در خانه ماندیم.","بنابراین تصمیم را تغییر دادیم."]),
_g("reported","نقل قول و گفتار غیرمستقیم","B2","Report statements and questions.","Use گفت که, reported questions and appropriate tense/reference shifts.",["او گفت که فردا می‌آید.","نمی‌دانم چه اتفاقی افتاده است."]),
_g("passive","ساخت مجهول","B2","Describe processes and results.","Use the شدن passive pattern and recognize formal passive constructions.",["نامه نوشته شد.","گزارش منتشر شده است."]),
_g("subordination","جمله‌های مرکب","B2","Build complex sentences.","Combine subordinate clauses while preserving clear reference and conjunctions.",["اگرچه زمان کم بود، پروژه را به پایان رساندیم."]),
_g("concession","امتیاز و تضاد","B2","Express contrast and concession.","Use اگرچه، بااین‌حال، اما، در حالی که and related discourse structures.",["اگرچه خسته بود، ادامه داد.","هزینه زیاد بود؛ بااین‌حال، پروژه موفق شد."]),
_g("discourse","انسجام و پیوندهای متنی","B2","Organize connected discourse.","Use sequence, contrast, cause, result and conclusion markers.",["ابتدا داده‌ها را بررسی می‌کنیم؛ سپس نتیجه را توضیح می‌دهیم."]),
_g("nominalization","اسم‌سازی","C1","Read and produce dense formal noun phrases.","Recognize کردن/شدن nominalizations and unpack them for clarity.",["بررسی نتایج نشان می‌دهد که تغییر مهم است.","اجرای طرح نیازمند هماهنگی است."]),
_g("academic-hedging","احتیاط علمی","C1","Qualify academic claims.","Use به نظر می‌رسد، احتمالاً، می‌توان گفت and evidence-based framing.",["به نظر می‌رسد این عامل تأثیر محدودی داشته باشد.","می‌توان گفت نتایج از این فرضیه حمایت می‌کنند."]),
_g("argumentation","استدلال و ساختار متن","C1","Build evidence-based arguments.","Signal claims, evidence, counterarguments and conclusions precisely.",["از یک سو شواهد این دیدگاه را تأیید می‌کنند؛ از سوی دیگر، محدودیت‌هایی وجود دارد."]),
_g("institutional","زبان اداری و رسمی","C1","Write formal institutional Persian.","Use conventional administrative structures while maintaining clarity.",["درخواست شما در مهلت مقرر بررسی خواهد شد.","مدارک باید تا پایان هفته ارسال شوند."]),
_g("embedded","پرسش غیرمستقیم","C1","Embed questions in formal discourse.","Use نمی‌دانم که/آیا and question-word clauses after reporting verbs.",["نمی‌دانم آیا جلسه برگزار می‌شود.","او توضیح داد که چرا تصمیم تغییر کرد."]),
_g("information","موضوع و کانون","C1","Control information structure.","Use fronting, contrastive particles and lexical choices to foreground new information.",["این نکته را باید در نظر گرفت.","دقیقاً همین مسئله موضوع اصلی بحث است."]),
_g("register","سطح زبان و ادب","C1","Adapt language to audience and context.","Distinguish colloquial, neutral, professional and formal Persian.",["می‌شه این موضوع رو توضیح بدی؟","ممکن است این موضوع را توضیح دهید؟"]),
_g("pragmatics","کاربردشناسی","C2","Interpret implied meaning and stance.","Manage indirectness, politeness, implication and context-sensitive wording.",["اگر ممکن است، این بخش را کمی روشن‌تر کنید.","به نظر من شاید راه دیگری هم وجود داشته باشد."]),
_g("rhetoric","بلاغت و اقناع","C2","Analyze persuasive discourse.","Study framing, repetition, contrast, metaphor and rhetorical organization.",["مسئله فقط هزینه نیست؛ مسئله کیفیت و دسترسی نیز هست."]),
_g("translation","دقت ترجمه","C2","Preserve meaning across languages.","Preserve modality, register, idioms, information structure and discourse relations.",["ترجمه باید لحن و احتیاط معنایی متن اصلی را حفظ کند."]),
_g("literary","سبک ادبی","C2","Interpret literary Persian.","Analyze imagery, rhythm, idiom, metaphor and stylistic shifts.",["سکوت شب مانند پرسشی بی‌پاسخ در اتاق ماند."]),
_g("discourse-analysis","تحلیل گفتمان","C2","Analyze advanced discourse strategies.","Track reference, presupposition, evaluation, cohesion and shifts in register.",["متن با تکرار واژگان ارزشی، دو دیدگاه را در برابر هم قرار می‌دهد."]),
_g("lexical","دقت واژگانی","C2","Choose precise vocabulary.","Distinguish near-synonyms and select wording by genre and communicative force.",["انتخاب واژه می‌تواند شدت ادعا را تغییر دهد."])
]

def _v(i,level,topic,words):
    return VocabularySet(id=i,level=level,topic=topic,unit_ref=f"fa-{level.lower()}-unit-1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])

VOCABULARY_SETS=[
_v("greetings_a1","A1","سلام و معرفی",[("سلام","phrase","hello","سلام! حال شما چطور است؟"),("خداحافظ","phrase","goodbye","خداحافظ، فردا می‌بینمتان."),("ممنون","phrase","thanks","ممنون از کمک شما."),("نام","noun","name","نام من سارا است.")]),
_v("family_a1","A1","خانواده",[("مادر","noun","mother","مادرم در خانه است."),("پدر","noun","father","پدرم کار می‌کند."),("خواهر","noun","sister","خواهرم دانشجو است."),("برادر","noun","brother","برادرم در تهران زندگی می‌کند.")]),
_v("home_a1","A1","خانه",[("خانه","noun","home","خانه من کوچک است."),("اتاق","noun","room","اتاق من روشن است."),("میز","noun","table","کتاب روی میز است."),("کلید","noun","key","کلید روی میز است.")]),
_v("food_a1","A1","غذا و خرید",[("آب","noun","water","یک لیوان آب می‌خواهم."),("نان","noun","bread","نان تازه می‌خرم."),("چای","noun","tea","من چای می‌نوشم."),("قیمت","noun","price","قیمت این چقدر است؟")]),
_v("places_a1","A1","مکان‌ها",[("خیابان","noun","street","این خیابان کجاست؟"),("ایستگاه","noun","station","ایستگاه نزدیک است."),("راست","noun","right","به راست بروید."),("چپ","noun","left","به چپ بپیچید.")]),
_v("daily_a2","A2","زندگی روزمره",[("صبح","noun","morning","صبح زود بیدار می‌شوم."),("کار کردن","verb","to work","هر روز کار می‌کنم."),("معمولاً","adverb","usually","معمولاً ساعت هفت بیدار می‌شوم."),("دیروز","adverb","yesterday","دیروز به بازار رفتم.")]),
_v("travel_a2","A2","سفر",[("بلیط","noun","ticket","بلیط قطار را خریدم."),("قطار","noun","train","قطار ساعت هشت حرکت می‌کند."),("فرودگاه","noun","airport","فرودگاه دور است."),("چمدان","noun","suitcase","چمدان من سنگین است.")]),
_v("health_a2","A2","سلامت",[("پزشک","noun","doctor","فردا نزد پزشک می‌روم."),("درد","noun","pain","سرم درد می‌کند."),("دارو","noun","medicine","دارو را بعد از غذا بخورید."),("قرار","noun","appointment","برای فردا قرار دارم.")]),
_v("work_b1","B1","کار",[("جلسه","noun","meeting","جلسه ساعت ده شروع می‌شود."),("پروژه","noun","project","پروژه هنوز تمام نشده است."),("مهلت","noun","deadline","مهلت ارسال فرداست."),("مسئولیت","noun","responsibility","این مسئولیت بر عهده تیم است.")]),
_v("education_b1","B1","تحصیل",[("دوره","noun","course","دوره در پاییز آغاز می‌شود."),("پژوهش","noun","research","پژوهش ادامه دارد."),("آزمون","noun","exam","آزمون دشوار بود."),("مهارت","noun","skill","این مهارت با تمرین بهتر می‌شود.")]),
_v("society_b1","B1","جامعه",[("جامعه","noun","society","جامعه به خدمات عمومی نیاز دارد."),("شهروند","noun","citizen","شهروندان می‌توانند نظر خود را بیان کنند."),("خدمت","noun","service","این خدمت رایگان است."),("قانون","noun","law","همه باید قانون را رعایت کنند.")]),
_v("media_b2","B2","رسانه",[("خبر","noun","news","خبر امروز منتشر شد."),("منبع","noun","source","منبع خبر باید بررسی شود."),("ادعا","noun","claim","این ادعا به شواهد نیاز دارد."),("دیدگاه","noun","viewpoint","مقاله دیدگاه متفاوتی ارائه می‌کند.")]),
_v("environment_b2","B2","محیط زیست",[("آلودگی","noun","pollution","آلودگی هوا کاهش یافته است."),("تغییر اقلیم","noun","climate change","تغییر اقلیم مسئله‌ای جهانی است."),("منبع","noun","resource","منابع طبیعی محدود هستند."),("پایداری","noun","sustainability","پایداری نیازمند برنامه‌ریزی است.")]),
_v("academic_c1","C1","زبان دانشگاهی",[("داده","noun","data","داده‌ها در جدول ارائه شده‌اند."),("فرضیه","noun","hypothesis","فرضیه باید آزمون شود."),("نتیجه","noun","result","نتیجه با داده‌ها سازگار است."),("محدودیت","noun","limitation","پژوهش چند محدودیت دارد.")]),
_v("institutional_c1","C1","اداری و سازمانی",[("درخواست","noun","request","درخواست شما ثبت شد."),("مدرک","noun","document","مدارک باید ارسال شوند."),("کمیسیون","noun","commission","کمیسیون گزارش را بررسی می‌کند."),("ارزیابی","noun","assessment","ارزیابی اثرات انجام شد.")]),
_v("rhetoric_c2","C2","تحلیل و بلاغت",[("چارچوب‌بندی","noun","framing","چارچوب‌بندی بر برداشت مخاطب اثر می‌گذارد."),("تلویحی","adjective","implicit","متن یک فرض تلویحی دارد."),("تناقض","noun","contradiction","دو گزاره با هم تناقض دارند."),("ظرافت","noun","nuance","انتخاب واژه ظرافت معنایی ایجاد می‌کند.")]),
_v("idioms_c2","C2","اصطلاحات و تعبیرها",[("در نظر گرفتن","phrase","take into account","باید همه عوامل را در نظر گرفت."),("به نتیجه رسیدن","phrase","reach a conclusion","پس از بررسی به نتیجه رسیدند."),("در جریان بودن","phrase","be underway/informed","من در جریان موضوع هستم."),("موضوع را روشن کردن","phrase","clarify the issue","گزارش موضوع را روشن می‌کند.")])
]

_TITLES={
"A1":["سلام و معرفی","خانواده و افراد","خانه و اشیا","زندگی روزمره","غذا و خرید","مکان‌ها و مسیرها","کمک و ارتباط","مرور A1"],
"A2":["روتین و زمان","خدمات و کارهای روزانه","سفر و حمل‌ونقل","سلامت","رویدادهای گذشته","برنامه‌ها و مقایسه","تجربه و نظر","مرور A2"],
"B1":["کار و تحصیل","روایت تجربه‌ها","مفعول و ساخت جمله","جامعه و خدمات","شرط و ادب","جمله‌های موصولی","علت و استدلال","مرور B1"],
"B2":["رسانه و منبع","مجهول و زبان رسمی","گفتار غیرمستقیم","محیط زیست","جمله‌های مرکب","انسجام متن","سبک و دیدگاه","مرور B2"],
"C1":["نوشتار دانشگاهی","ساختارهای پیچیده","زبان اداری","شواهد و احتیاط","ساخت استدلال","کاربردشناسی","ویرایش و پرسش غیرمستقیم","مرور C1"],
"C2":["تحلیل بلاغی","کنترل سبک و سطح زبان","ترجمه دقیق","سبک ادبی","تحلیل گفتمان","استدلال پیشرفته","دقت واژگانی","مرور C2"]}

_G={"A1":["pronouns","ezafe","copula","negation","questions","present","plural","prepositions"],"A2":["past","imperfective","future","comparatives","imperative","object-marker","questions","prepositions"],"B1":["progressive","perfect","conditional","relative","modality","causal","object-marker","relative"],"B2":["reported","passive","subordination","concession","discourse","aspect","register","nominalization"],"C1":["academic-hedging","argumentation","institutional","embedded","information","register","nominalization","subordination"],"C2":["pragmatics","rhetoric","translation","literary","discourse-analysis","lexical","argumentation","register"]}
_V={"A1":["greetings_a1","family_a1","home_a1","daily_a2","food_a1","places_a1","greetings_a1","home_a1"],"A2":["daily_a2","travel_a2","health_a2","food_a1","places_a1","daily_a2","travel_a2","health_a2"],"B1":["work_b1","education_b1","society_b1","daily_a2","work_b1","education_b1","society_b1","work_b1"],"B2":["media_b2","environment_b2","society_b1","work_b1","media_b2","environment_b2","media_b2","environment_b2"],"C1":["academic_c1","institutional_c1","work_b1","society_b1","academic_c1","institutional_c1","media_b2","academic_c1"],"C2":["rhetoric_c2","idioms_c2","academic_c1","institutional_c1","rhetoric_c2","idioms_c2","media_b2","rhetoric_c2"]}

CURRICULUM={}
for level,titles in _TITLES.items():
    CURRICULUM[level]=[]
    for n,title in enumerate(titles,1):
        gs=_G[level]
        CURRICULUM[level].append(CurriculumUnit(id=f"fa-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=[gs[(n-1)%len(gs)],gs[n%len(gs)]],vocabulary_set_ids=[_V[level][n-1]],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=[f"Use Persian in the context: {title}","Apply the unit grammar and vocabulary in a communicative task"],default_weeks=2))

def _p(i,level,situation,phrases):
    return PhrasebookCategory(id=i,level=level,situation=situation,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in phrases])

PHRASEBOOK_CATEGORIES=[
_p("greetings_a1","A1","سلام و معرفی",[("سلام، حال شما چطور است؟","greeting","neutral"),("نام من سارا است.","introducing yourself","neutral"),("خوشبختم.","meeting someone","neutral"),("ممنون از شما.","thanking","neutral")]),
_p("daily_a1","A1","روزمره",[("حال شما چطور است؟","asking how someone is","neutral"),("خوبم، ممنون.","answering","neutral"),("فردا می‌بینمتان.","saying goodbye","neutral")]),
_p("shopping_a1","A1","خرید",[("قیمت این چقدر است؟","asking price","neutral"),("لطفاً یک کیلو نان می‌خواهم.","requesting an item","polite"),("کارت قبول می‌کنید؟","payment","neutral")]),
_p("directions_a1","A1","مسیر",[("ایستگاه کجاست؟","asking location","neutral"),("به راست بروید.","giving directions","neutral"),("چقدر دور است؟","asking distance","neutral")]),
_p("help_a1","A1","کمک",[("لطفاً کمک کنید.","asking for help","polite"),("متوجه نمی‌شوم.","clarification","neutral"),("لطفاً آهسته‌تر صحبت کنید.","asking to slow down","polite")]),
_p("travel_a2","A2","سفر",[("بلیط از کجا می‌توانم بخرم؟","travel information","neutral"),("قطار چه ساعتی حرکت می‌کند؟","departure time","neutral"),("چمدان من کجاست؟","luggage","neutral")]),
_p("work_b1","B1","کار",[("می‌توانیم جلسه‌ای تعیین کنیم؟","arranging a meeting","polite"),("گزارش را امروز ارسال می‌کنم.","follow-up","neutral"),("مهلت انجام کار چه زمانی است؟","clarifying deadline","polite")]),
_p("academic_c1","C1","گفت‌وگوی دانشگاهی",[("شواهد نشان می‌دهد که…","introducing evidence","formal"),("این تفسیر نیاز به بررسی بیشتری دارد.","critical discussion","formal"),("می‌توان گفت که…","qualifying a claim","formal")]),
_p("formal_c1","C1","مکاتبات رسمی",[("برای درخواست اطلاعات با شما تماس می‌گیرم.","formal inquiry","formal"),("درخواست شما دریافت شد.","administrative update","formal"),("از پاسخ شما سپاسگزارم.","formal thanks","formal")]),
_p("discussion_c2","C2","استدلال پیشرفته",[("به نظر من، این تمایز اهمیت دارد.","nuanced position","formal"),("بااین‌حال، باید فرضیه دیگری را نیز در نظر گرفت.","counterargument","formal"),("این نکته تفاوت مهمی را روشن می‌کند.","emphasis","formal")])
]

ASSESSMENT_BANK=[
AssessmentQuestion(id="fa-a1-001",skill="grammar",difficulty="A1",question="Which sentence means 'I am a student'?",options=["من دانشجو هستم.","من دانشجو است.","من دانشجو هستند.","من دانشجو نیستم."],correct="من دانشجو هستم."),
AssessmentQuestion(id="fa-a1-002",skill="grammar",difficulty="A1",question="Which asks 'Where is the station?'",options=["ایستگاه کجاست؟","این چیست؟","نام شما چیست؟","چند کتاب؟"],correct="ایستگاه کجاست؟"),
AssessmentQuestion(id="fa-a2-001",skill="grammar",difficulty="A2",question="Which sentence uses the definite object marker را?",options=["کتاب را خواندم.","کتاب خواندن.","کتاب می‌خوانم.","کتاب است."],correct="کتاب را خواندم."),
AssessmentQuestion(id="fa-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a hypothetical condition?",options=["اگر وقت داشته باشم، می‌آیم.","دیروز آمدم.","امروز می‌آیم.","فردا خواهم آمد."],correct="اگر وقت داشته باشم، می‌آیم."),
AssessmentQuestion(id="fa-b2-001",skill="grammar",difficulty="B2",question="Which sentence reports a statement?",options=["او گفت که فردا می‌آید.","او فردا می‌آید.","او دیروز آمد.","او هر روز می‌آید."],correct="او گفت که فردا می‌آید."),
AssessmentQuestion(id="fa-c1-001",skill="communication",difficulty="C1",question="Which phrase appropriately hedges an academic claim?",options=["به نظر می‌رسد این عامل تأثیر محدودی داشته باشد.","این همیشه و قطعاً درست است.","همه می‌دانند که این درست است.","هیچ شکی وجود ندارد."],correct="به نظر می‌رسد این عامل تأثیر محدودی داشته باشد."),
AssessmentQuestion(id="fa-c1-002",skill="communication",difficulty="C1",question="Which is appropriate in a formal administrative exchange?",options=["از پاسخ شما سپاسگزارم.","هی، چه خبر؟","اون رو بده.","باشه، خداحافظ."],correct="از پاسخ شما سپاسگزارم."),
AssessmentQuestion(id="fa-c2-001",skill="communication",difficulty="C2",question="What should a precise Persian translation preserve?",options=["Modality, register, idiom and discourse relations.","Only word order.","Only dictionary meanings.","No stylistic nuance."],correct="Modality, register, idiom and discourse relations.")
]

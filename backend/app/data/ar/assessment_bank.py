"""Modern Standard Arabic assessment bank with expanded A1 practice."""
from app.data._types import AssessmentQuestion

ASSESSMENT_BANK = [
# Grammar A1
AssessmentQuestion(id="ar-a1-g-001",skill="grammar",difficulty="A1",question="اختر الضمير الصحيح: ___ طالبٌ.",options=["أنا","هي","هم","أنتن"],correct="أنا",grammar_slug="pronouns"),
AssessmentQuestion(id="ar-a1-g-002",skill="grammar",difficulty="A1",question="اختر الجملة الصحيحة.",options=["هذه سيارة.","هذا سيارة.","هذه كتاب.","هذا مدرسة."],correct="هذه سيارة.",grammar_slug="gender-agreement"),
AssessmentQuestion(id="ar-a1-g-003",skill="grammar",difficulty="A1",question="أكمل: ___ اسمك؟",options=["ما","أين","متى","كم"],correct="ما",grammar_slug="question-words"),
AssessmentQuestion(id="ar-a1-g-004",skill="grammar",difficulty="A1",question="اختر الجملة الصحيحة.",options=["أنا أدرس العربية.","أنا يدرس العربية.","أنا تدرس العربية.","أنا يدرسون العربية."],correct="أنا أدرس العربية.",grammar_slug="present-tense"),
AssessmentQuestion(id="ar-a1-g-005",skill="grammar",difficulty="A1",question="اختر النفي الصحيح: ___ أفهم.",options=["لا","ليس","لم","لن"],correct="لا",grammar_slug="negation"),
AssessmentQuestion(id="ar-a1-g-006",skill="grammar",difficulty="A1",question="اختر الصيغة الصحيحة: الكتاب ___ الطاولة.",options=["على","إلى","من","مع"],correct="على",grammar_slug="prepositions"),
AssessmentQuestion(id="ar-a1-g-007",skill="grammar",difficulty="A1",question="اختر الصيغة الصحيحة: كتاب ___ الطالب.",options=["الطالبِ","الطالبُ","الطالبَ","طالبٌ"],correct="الطالبِ",grammar_slug="possessive-construct"),
AssessmentQuestion(id="ar-a1-g-008",skill="grammar",difficulty="A1",question="اختر الصفة الصحيحة: البيت ___ .",options=["كبير","كبيرة","كبيرون","كبيرات"],correct="كبير",grammar_slug="adjectives"),
AssessmentQuestion(id="ar-a1-g-009",skill="grammar",difficulty="A1",question="أكمل: ___ كتاب على الطاولة.",options=["يوجد","توجد","هم","نحن"],correct="يوجد",grammar_slug="there-is-there-are"),
AssessmentQuestion(id="ar-a1-g-010",skill="grammar",difficulty="A1",question="اختر الجملة الصحيحة.",options=["أقرأ كتابًا.","أقرأ كتابٌ.","أقرأ كتابٍ.","أقرأ كتبٌ."],correct="أقرأ كتابًا.",grammar_slug="accusative-intro"),
AssessmentQuestion(id="ar-a1-g-011",skill="grammar",difficulty="A1",question="كيف تطلب من شخص أن يقرأ؟",options=["اقرأ.","يقرأ.","قرأت.","سأقرأ."],correct="اقرأ.",grammar_slug="imperative-intro"),
AssessmentQuestion(id="ar-a1-g-012",skill="grammar",difficulty="A1",question="اختر السؤال الصحيح عن المكان.",options=["أين تسكن؟","متى تسكن؟","كم تسكن؟","من تسكن؟"],correct="أين تسكن؟",grammar_slug="question-words"),
# Vocabulary A1
AssessmentQuestion(id="ar-a1-v-001",skill="vocabulary",difficulty="A1",question="ما معنى «أب»؟",options=["والد","والدة","أخ","صديق"],correct="والد"),
AssessmentQuestion(id="ar-a1-v-002",skill="vocabulary",difficulty="A1",question="أين ننام عادةً؟",options=["المطبخ","السرير","السوق","المطار"],correct="السرير"),
AssessmentQuestion(id="ar-a1-v-003",skill="vocabulary",difficulty="A1",question="ما عكس «كبير»؟",options=["قديم","صغير","غالي","بعيد"],correct="صغير"),
AssessmentQuestion(id="ar-a1-v-004",skill="vocabulary",difficulty="A1",question="ماذا نشرب؟",options=["الماء","الكرسي","الكتاب","المفتاح"],correct="الماء"),
AssessmentQuestion(id="ar-a1-v-005",skill="vocabulary",difficulty="A1",question="ما المكان الذي نشتري منه الطعام أو الأشياء؟",options=["السوق","السرير","الحمام","الفصل"],correct="السوق"),
AssessmentQuestion(id="ar-a1-v-006",skill="vocabulary",difficulty="A1",question="ما معنى «غدًا»؟",options=["اليوم السابق","هذا الصباح","اليوم التالي","الآن"],correct="اليوم التالي"),
AssessmentQuestion(id="ar-a1-v-007",skill="vocabulary",difficulty="A1",question="أي كلمة تدل على جهة؟",options=["يمين","كتاب","طبيب","حليب"],correct="يمين"),
AssessmentQuestion(id="ar-a1-v-008",skill="vocabulary",difficulty="A1",question="ماذا نقول عندما نريد معرفة السعر؟",options=["كم السعر؟","أين تسكن؟","ما اسمك؟","متى تنام؟"],correct="كم السعر؟"),
AssessmentQuestion(id="ar-a1-v-009",skill="vocabulary",difficulty="A1",question="من يعمل في المستشفى ويعالج المرضى؟",options=["طبيب","مهندس","طالب","سائق"],correct="طبيب"),
AssessmentQuestion(id="ar-a1-v-010",skill="vocabulary",difficulty="A1",question="ما معنى «بعيد»؟",options=["قريب جدًا","على مسافة كبيرة","جديد","نظيف"],correct="على مسافة كبيرة"),
# Reading A1
AssessmentQuestion(id="ar-a1-r-001",skill="reading",difficulty="A1",question="اقرأ: «اسمي سامي. أنا طالب. أسكن في الجزائر.» من هو سامي؟",options=["طالب","طبيب","معلم","مهندس"],correct="طالب"),
AssessmentQuestion(id="ar-a1-r-002",skill="reading",difficulty="A1",question="اقرأ: «تستيقظ ليلى الساعة السابعة وتذهب إلى المدرسة الساعة الثامنة.» متى تستيقظ ليلى؟",options=["السابعة","الثامنة","التاسعة","العاشرة"],correct="السابعة"),
AssessmentQuestion(id="ar-a1-r-003",skill="reading",difficulty="A1",question="اقرأ: «البيت صغير، لكنه نظيف. فيه غرفتان ومطبخ.» كيف هو البيت؟",options=["كبير وغير نظيف","صغير ونظيف","كبير ونظيف","صغير وقديم"],correct="صغير ونظيف"),
AssessmentQuestion(id="ar-a1-r-004",skill="reading",difficulty="A1",question="اقرأ: «ذهب أحمد إلى السوق. اشترى خبزًا وحليبًا.» ماذا اشترى أحمد؟",options=["خبزًا وحليبًا","كتابًا وقلمًا","قهوة وأرزًا","تفاحة وماءً"],correct="خبزًا وحليبًا"),
AssessmentQuestion(id="ar-a1-r-005",skill="reading",difficulty="A1",question="اقرأ: «المستشفى بجانب البنك، والصيدلية أمام المستشفى.» أين الصيدلية؟",options=["خلف البنك","أمام المستشفى","داخل البنك","بعيدًا عن المستشفى"],correct="أمام المستشفى"),
AssessmentQuestion(id="ar-a1-r-006",skill="reading",difficulty="A1",question="اقرأ: «لدي موعد الساعة العاشرة. سأذهب إلى الجامعة مبكرًا.» أين سيذهب المتحدث؟",options=["إلى الجامعة","إلى السوق","إلى المطار","إلى المستشفى"],correct="إلى الجامعة"),
# Review A1
AssessmentQuestion(id="ar-a1-rv-001",skill="grammar",difficulty="A1",question="اختر الجملة المناسبة للتعريف بالنفس.",options=["اسمي أحمد.","أين السوق؟","كم السعر؟","أين الحمام؟"],correct="اسمي أحمد."),
AssessmentQuestion(id="ar-a1-rv-002",skill="vocabulary",difficulty="A1",question="ما الرد الطبيعي على «شكرًا»؟",options=["عفوًا","وداعًا","صباح الخير","أين؟"],correct="عفوًا"),
AssessmentQuestion(id="ar-a1-rv-003",skill="grammar",difficulty="A1",question="اختر الصيغة الصحيحة: أنا ___ من الجزائر.",options=["من","في","إلى","على"],correct="من",grammar_slug="prepositions"),
AssessmentQuestion(id="ar-a1-rv-004",skill="reading",difficulty="A1",question="اقرأ: «أنا أدرس العربية كل يوم. أحب اللغة وأفهم الجمل البسيطة.» ماذا يدرس المتحدث؟",options=["العربية","الفرنسية","الرياضيات","التاريخ"],correct="العربية"),
# Existing progression checks
AssessmentQuestion(id="ar-a2-001",skill="grammar",difficulty="A2",question="اختر صيغة الماضي الصحيحة: أنا ___ الرسالة.",options=["كتب","كتبتُ","يكتب","سأكتب"],correct="كتبتُ",grammar_slug="past-tense"),
AssessmentQuestion(id="ar-a2-002",skill="grammar",difficulty="A2",question="اختر المستقبل الصحيح.",options=["سأدرس غدًا.","درست غدًا.","أدرس أمس.","سوف درست."],correct="سأدرس غدًا.",grammar_slug="future-particles"),
AssessmentQuestion(id="ar-b1-001",skill="grammar",difficulty="B1",question="اختر الاسم الموصول الصحيح: الطالبة ___ نجحت.",options=["الذي","التي","الذين","اللذان"],correct="التي",grammar_slug="relative-clauses"),
AssessmentQuestion(id="ar-b2-001",skill="grammar",difficulty="B2",question="اختر المبني للمجهول.",options=["كتب الطالب الرسالة.","كُتبت الرسالةُ.","يكتب الطالب.","سيكتب الطالب."],correct="كُتبت الرسالةُ.",grammar_slug="passive-voice"),
AssessmentQuestion(id="ar-c1-001",skill="grammar",difficulty="C1",question="أي عبارة أنسب للسجل الأكاديمي؟",options=["تشير النتائج إلى ارتفاع المعدل.","النتائج مرة رهيبة.","النتائج شيء كبير جدًا.","النتائج حلوة."],correct="تشير النتائج إلى ارتفاع المعدل.",grammar_slug="academic-register"),
AssessmentQuestion(id="ar-c2-001",skill="grammar",difficulty="C2",question="ما الذي يساعد على فهم المعنى الضمني؟",options=["السياق والنبرة","عدد الكلمات فقط","شكل الحروف فقط","علامة الترقيم فقط"],correct="السياق والنبرة",grammar_slug="implicature"),
]

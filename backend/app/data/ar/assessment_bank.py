"""Arabic assessment bank."""
from app.data._types import AssessmentQuestion

ASSESSMENT_BANK = [
AssessmentQuestion(id="ar-a1-001",skill="grammar",difficulty="A1",question="اختر الجملة الصحيحة:",options=["أنا طالب.","أنا طالبةٌ هو.","أنا يكون طالب.","أنا هو طالبون."],correct="أنا طالب.",grammar_slug="nominal-sentence"),
AssessmentQuestion(id="ar-a1-002",skill="grammar",difficulty="A1",question="أكمل: ___ أدرس العربية.",options=["أنا","هو","هي","هم"],correct="أنا",grammar_slug="pronouns"),
AssessmentQuestion(id="ar-a1-003",skill="vocabulary",difficulty="A1",question="ما معنى «أب»؟",options=["والد","والدة","أخ","صديق"],correct="والد"),
AssessmentQuestion(id="ar-a2-001",skill="grammar",difficulty="A2",question="اختر صيغة الماضي الصحيحة: أنا ___ الرسالة.",options=["كتب","كتبتُ","يكتب","سأكتب"],correct="كتبتُ",grammar_slug="past-tense"),
AssessmentQuestion(id="ar-a2-002",skill="grammar",difficulty="A2",question="اختر المستقبل الصحيح:",options=["سأدرس غدًا.","درست غدًا.","أدرس أمس.","سوف درست."],correct="سأدرس غدًا.",grammar_slug="future-particles"),
AssessmentQuestion(id="ar-b1-001",skill="grammar",difficulty="B1",question="اختر الاسم الموصول الصحيح: الطالبة ___ نجحت.",options=["الذي","التي","الذين","اللذان"],correct="التي",grammar_slug="relative-clauses"),
AssessmentQuestion(id="ar-b1-002",skill="grammar",difficulty="B1",question="أكمل: إذا درستَ ___ .",options=["تنجحُ","نجحتَ أمس","سوف درست","تدرسُ أمس"],correct="تنجحُ",grammar_slug="conditional"),
AssessmentQuestion(id="ar-b2-001",skill="grammar",difficulty="B2",question="اختر المبني للمجهول:",options=["كتب الطالب الرسالة.","كُتبت الرسالةُ.","يكتب الطالب.","سيكتب الطالب."],correct="كُتبت الرسالةُ.",grammar_slug="passive-voice"),
AssessmentQuestion(id="ar-b2-002",skill="vocabulary",difficulty="B2",question="أي كلمة تناسب الكتابة الحجاجية؟",options=["حجة","ملعقة","نافذة","وسادة"],correct="حجة"),
AssessmentQuestion(id="ar-c1-001",skill="grammar",difficulty="C1",question="أي عبارة أنسب للسجل الأكاديمي؟",options=["النتائج تشير إلى ارتفاع المعدل.","النتائج مرة رهيبة.","النتائج شيء كبير جدًا.","النتائج حلوة."],correct="النتائج تشير إلى ارتفاع المعدل.",grammar_slug="academic-register"),
AssessmentQuestion(id="ar-c1-002",skill="vocabulary",difficulty="C1",question="ما الكلمة التي تعني بيانات تستخدم للتحليل؟",options=["معطيات","تحية","رحلة","شارع"],correct="معطيات"),
AssessmentQuestion(id="ar-c2-001",skill="grammar",difficulty="C2",question="ما الذي يساعد على فهم المعنى الضمني؟",options=["السياق والنبرة","عدد الكلمات فقط","شكل الحروف فقط","علامة الترقيم فقط"],correct="السياق والنبرة",grammar_slug="implicature"),
]

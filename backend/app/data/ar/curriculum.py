"""Modern Standard Arabic curriculum, A1-C2."""
from app.data._types import CurriculumUnit

def _u(level, n, title, grammar, vocab, goals, weeks=2, prereq=None):
    return CurriculumUnit(
        id=f"{level.lower()}-unit-{n}", level=level, unit_number=n, title=title,
        grammar_points=grammar, vocabulary_set_ids=vocab,
        lesson_types=["grammar","vocabulary","reading","writing","review"],
        competency_checklist=goals, default_weeks=weeks, prerequisite_unit=prereq,
    )

CURRICULUM = {
"A1": [
_u("A1",1,"التحية والتعارف",["pronouns","nominal-sentence","question-words"],["greetings_a1","identity_a1"],["التعريف بالنفس","طرح أسئلة شخصية بسيطة","فهم التحيات الأساسية"]),
_u("A1",2,"الأسرة والحياة اليومية",["possessive-construct","definite-article","present-tense"],["family_a1","daily-life_a1"],["وصف الأسرة","الحديث عن الروتين اليومي"]),
_u("A1",3,"الوقت والأماكن",["numbers","prepositions","demonstratives"],["numbers_time_a1","places_a1"],["ذكر الوقت والمكان","طلب الاتجاهات البسيطة"]),
_u("A1",4,"المراجعة والتواصل",["adjectives","negation","basic-questions"],["common-verbs_a1","adjectives_a1"],["إجراء حوار قصير","قراءة نصوص يومية بسيطة"]),
],
"A2": [
_u("A2",1,"الماضي والسرد البسيط",["past-tense","verb-agreement","time-expressions"],["travel_a2","events_a2"],["وصف أحداث سابقة","سرد تجربة قصيرة"],prereq="a1-unit-4"),
_u("A2",2,"الصحة والطعام",["imperative","negation-past","quantifiers"],["health_a2","food_a2"],["طلب الطعام","وصف أعراض بسيطة"]),
_u("A2",3,"العمل والتسوق",["comparatives","adverbs","object-pronouns"],["work_a2","shopping_a2"],["التعامل في متجر","وصف المنتجات والأسعار"]),
_u("A2",4,"المستقبل والخطط",["future-particles","intention","connected-sentences"],["plans_a2","weather_a2"],["الحديث عن الخطط","فهم محادثات يومية متوسطة"]),
],
"B1": [
_u("B1",1,"السرد والوصف المتقدم",["verbal-sentence","relative-clauses","past-aspect"],["storytelling_b1","experiences_b1"],["سرد قصة مترابطة","وصف أشخاص وأحداث بدقة"],prereq="a2-unit-4"),
_u("B1",2,"التعليم والعمل",["subordination","conditional","passive-intro"],["education_b1","career_b1"],["مناقشة الدراسة والعمل","كتابة رسالة عملية"]),
_u("B1",3,"الإعلام والمجتمع",["reported-speech","connectors","emphasis"],["media_b1","society_b1"],["تلخيص خبر","عرض رأي مع أسباب"]),
_u("B1",4,"المهام التواصلية",["relative-clauses","conditionals","modals"],["communication_b1"],["إدارة نقاش يومي","فهم نصوص عامة"]),
],
"B2": [
_u("B2",1,"الحجاج وإبداء الرأي",["subjunctive","conditional-structures","rhetorical-connectors"],["opinions_b2","debate_b2"],["بناء حجة","الموافقة والاعتراض بأدب"],prereq="b1-unit-4"),
_u("B2",2,"العربية الرسمية",["formal-register","passive-voice","verbal-nouns"],["formal_b2","institutions_b2"],["فهم النصوص الرسمية","كتابة طلب رسمي"]),
_u("B2",3,"الصحافة والتحليل",["reported-speech-advanced","nominalization","discourse-markers"],["news_b2","analysis_b2"],["تلخيص وتحليل مقال","تمييز النبرة والموقف"]),
_u("B2",4,"الإنتاج المتقدم",["complex-sentences","cohesion","style"],["production_b2"],["كتابة نص مترابط","عرض موضوع شفهيًا"]),
],
"C1": [
_u("C1",1,"اللغة الأكاديمية",["academic-register","complex-subordination","nominalization"],["academic_c1","research_c1"],["قراءة نص أكاديمي","تلخيص مصادر وأفكار"],prereq="b2-unit-4"),
_u("C1",2,"الأسلوب والبلاغة",["rhetorical-devices","ellipsis","parallelism"],["rhetoric_c1","literature_c1"],["تحليل الأسلوب","استخدام تراكيب بلاغية مناسبة"]),
_u("C1",3,"التحرير المهني",["cohesion-advanced","register-shift","precision"],["professional_c1"],["تحرير نص مهني","اختيار السجل اللغوي المناسب"]),
_u("C1",4,"البحث والعرض",["argumentation","hedging","discourse-organization"],["presentation_c1"],["عرض حجة مركبة","الدفاع عن موقف بالأدلة"]),
],
"C2": [
_u("C2",1,"التحكم الأسلوبي",["advanced-syntax","register-control","ellipsis-advanced"],["style_c2"],["التحكم في الأسلوب والسجل","فهم الفروق الدقيقة"]),
_u("C2",2,"النصوص المتخصصة",["specialized-discourse","dense-nominalization","cohesion-c2"],["specialized_c2"],["قراءة نصوص متخصصة","إعادة صياغة دقيقة"]),
_u("C2",3,"البلاغة والنقد",["rhetoric-c2","pragmatics","implicature"],["criticism_c2"],["تحليل الخطاب","استنتاج المعاني الضمنية"]),
_u("C2",4,"الإنتاج الاحترافي",["stylistic-variation","precision-c2","editing"],["professional_c2"],["إنتاج نص احترافي رفيع المستوى","التحرير والمراجعة الذاتية"]),
],
}

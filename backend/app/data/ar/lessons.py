"""Sequenced Arabic A1 lesson map.

This module is the deterministic course-plan layer above curriculum data.
It does not contain generated lesson prose; it tells the lesson service what
each session is meant to accomplish and which existing content it should use.
"""

from dataclasses import dataclass
from typing import Literal

LessonType = Literal["grammar", "vocabulary", "reading", "writing", "listening", "review"]


@dataclass(frozen=True)
class ArabicA1Lesson:
    id: str
    unit_id: str
    week: int
    day: int
    lesson_type: LessonType
    title: str
    objective: str
    grammar_refs: tuple[str, ...]
    vocabulary_set_ids: tuple[str, ...]
    phrasebook_ids: tuple[str, ...]


def _lesson(
    unit: int,
    week: int,
    day: int,
    lesson_type: LessonType,
    title: str,
    objective: str,
    grammar: tuple[str, ...],
    vocab: tuple[str, ...],
    phrases: tuple[str, ...],
) -> ArabicA1Lesson:
    return ArabicA1Lesson(
        id=f"a1-u{unit}-w{week}-d{day}",
        unit_id=f"a1-unit-{unit}",
        week=week,
        day=day,
        lesson_type=lesson_type,
        title=title,
        objective=objective,
        grammar_refs=grammar,
        vocabulary_set_ids=vocab,
        phrasebook_ids=phrases,
    )


ARABIC_A1_LESSONS: tuple[ArabicA1Lesson, ...] = (
    # Unit 1 — Greetings and introductions
    _lesson(1,1,1,"grammar","التحية والتعريف بالنفس","استخدام الضمائر والجملة الاسمية للتعريف بالنفس.",("pronouns","nominal-sentence"),("greetings_a1","identity_a1"),("greetings_a1","personal_a1")),
    _lesson(1,1,2,"vocabulary","الاسم والبلد والمهنة","تقديم الاسم والبلد والدراسة أو العمل في جمل قصيرة.",("pronouns","gender-agreement"),("greetings_a1","identity_a1"),("personal_a1",)),
    _lesson(1,1,3,"listening","فهم التعارف","فهم حوار تعارف قصير واستخراج الاسم والبلد والمهنة.",("pronouns","question-words"),("greetings_a1","identity_a1"),("greetings_a1","personal_a1")),
    _lesson(1,1,4,"reading","حوار التعارف","قراءة حوار A1 عن شخصين واستخراج المعلومات الأساسية.",("nominal-sentence","gender-agreement","question-words"),("identity_a1",),("personal_a1",)),
    _lesson(1,1,5,"writing","ملفي الشخصي","كتابة تعريف من 4–5 جمل عن الاسم والبلد والعمل أو الدراسة.",("pronouns","nominal-sentence","gender-agreement"),("identity_a1",),("personal_a1",)),
    _lesson(1,2,1,"grammar","الأسئلة الأساسية","طرح أسئلة قصيرة باستخدام من وما وأين وكيف.",("question-words","basic-questions"),("identity_a1",),("personal_a1",)),
    _lesson(1,2,2,"vocabulary","معلومات شخصية إضافية","توسيع مفردات العمر والمدينة واللغة والأسرة القريبة.",("question-words","gender-agreement"),("identity_a1",),("personal_a1",)),
    _lesson(1,2,3,"listening","التعارف في موقف حقيقي","فهم أسئلة وأجوبة قصيرة في موقف تعارف.",("question-words","pronouns"),("identity_a1","greetings_a1"),("greetings_a1","personal_a1")),
    _lesson(1,2,4,"grammar","مراجعة الوحدة","التمييز بين الضمائر وأدوات السؤال والجمل الاسمية.",("pronouns","nominal-sentence","question-words"),("greetings_a1","identity_a1"),("greetings_a1","personal_a1")),
    _lesson(1,2,5,"review","اختبار التواصل الأول","إجراء حوار تعارف قصير ثم استرجاع مفردات الوحدة.",("pronouns","nominal-sentence","question-words","gender-agreement"),("greetings_a1","identity_a1"),("greetings_a1","personal_a1")),

    # Unit 2 — Family and possession
    _lesson(2,1,1,"grammar","الملكية والإضافة","فهم الإضافة وضمائر الملكية في جمل أسرية بسيطة.",("possessive-construct","possessive-pronouns"),("family_a1","personal-info_a1"),()),
    _lesson(2,1,2,"vocabulary","أفراد الأسرة","وصف الأسرة باستخدام مفردات الأب والأم والإخوة والأبناء.",("gender-agreement","possessive-pronouns"),("family_a1",),()),
    _lesson(2,1,3,"reading","عائلة بسيطة","قراءة وصف قصير لعائلة واستخراج علاقات الملكية والقرابة.",("possessive-construct","gender-agreement"),("family_a1",),()),
    _lesson(2,1,4,"listening","من هذا؟","فهم وصف أفراد الأسرة والرد عن صلة القرابة.",("possessive-pronouns","question-words"),("family_a1",),()),
    _lesson(2,1,5,"writing","وصف عائلتي","كتابة 5 جمل عن أفراد الأسرة واستخدام الملكية.",("possessive-construct","possessive-pronouns","gender-agreement"),("family_a1","personal-info_a1"),()),
    _lesson(2,2,1,"grammar","أل التعريف مع الأسرة","التمييز بين الاسم المعرفة والنكرة في وصف الأشخاص والأشياء.",("definite-article","gender-agreement"),("family_a1",),()),
    _lesson(2,2,2,"vocabulary","العلاقات والملكية","إعادة تدوير مفردات الأسرة مع كتابي وبيتي وأخي ونحوها.",("possessive-pronouns","definite-article"),("family_a1","personal-info_a1"),()),
    _lesson(2,2,3,"reading","صورة عائلية","فهم نص قصير يصف صورة عائلية.",("definite-article","adjectives","possessive-construct"),("family_a1",),()),
    _lesson(2,2,4,"review","التحدث عن الأسرة","إجراء حوار سؤال وجواب عن الأسرة والملكية.",("question-words","possessive-pronouns"),("family_a1",),()),
    _lesson(2,2,5,"review","مراجعة الأسرة والملكية","استرجاع مفردات الأسرة والإضافة وضمائر الملكية دون قاعدة جديدة.",("possessive-construct","possessive-pronouns","definite-article","gender-agreement"),("family_a1","personal-info_a1"),()),

    # Unit 3 — Home and objects
    _lesson(3,1,1,"grammar","هذا وهذه","اختيار اسم الإشارة الصحيح ووصف الأشياء القريبة.",("demonstratives","gender-agreement"),("home_a1","objects_a1"),()),
    _lesson(3,1,2,"vocabulary","الغرف والأشياء","تسمية الغرف والأثاث والأشياء المنزلية الأساسية.",("definite-article","adjectives"),("home_a1","objects_a1"),()),
    _lesson(3,1,3,"grammar","الصفة والموصوف","مطابقة الصفة للاسم في جمل وصف المنزل.",("adjectives","definite-article","gender-agreement"),("home_a1","objects_a1"),()),
    _lesson(3,1,4,"reading","بيتي","قراءة وصف بسيط للبيت وتحديد الغرف والأشياء وصفاتها.",("demonstratives","adjectives","definite-article"),("home_a1","objects_a1"),()),
    _lesson(3,1,5,"writing","وصف غرفتي","كتابة وصف قصير لغرفة باستخدام أسماء الإشارة والصفات.",("demonstratives","adjectives","prepositions"),("home_a1","objects_a1"),()),
    _lesson(3,2,1,"grammar","حروف الجر والمكان","استخدام في وعلى ومن وإلى ومع لوصف الموقع.",("prepositions","place-expressions"),("home_a1","objects_a1"),()),
    _lesson(3,2,2,"vocabulary","الموقع والاتجاه داخل البيت","استخدام أمام وخلف وبجانب وبين مع مفردات المنزل.",("prepositions","place-expressions"),("home_a1","objects_a1"),()),
    _lesson(3,2,3,"listening","أين الشيء؟","فهم وصف شفهي لموقع الأشياء داخل المنزل.",("prepositions","place-expressions","demonstratives"),("home_a1","objects_a1"),()),
    _lesson(3,2,4,"review","جولة في البيت","وصف موقع 5 أشياء في حوار قصير.",("prepositions","place-expressions","adjectives"),("home_a1","objects_a1"),()),
    _lesson(3,2,5,"review","مراجعة البيت","دمج أسماء الإشارة والصفات وحروف الجر وتعبيرات المكان.",("demonstratives","adjectives","prepositions","place-expressions"),("home_a1","objects_a1"),()),

    # Unit 4 — Daily routine
    _lesson(4,1,1,"grammar","المضارع","استخدام المضارع للتحدث عن العادات اليومية.",("present-tense","present-subject-agreement"),("daily-life_a1","common-verbs_a1"),("daily_a1",)),
    _lesson(4,1,2,"vocabulary","أفعال اليوم","التحدث عن الاستيقاظ والدراسة والعمل والعودة والنوم.",("present-tense","adverbs-frequency"),("daily-life_a1","common-verbs_a1"),("daily_a1",)),
    _lesson(4,1,3,"listening","يومي المعتاد","فهم تسلسل يوم بسيط واستخراج أوقات وأنشطة أساسية.",("present-tense","adverbs-frequency"),("daily-life_a1","common-verbs_a1"),("daily_a1",)),
    _lesson(4,1,4,"grammar","النفي","نفي الأفعال المضارعة في الروتين اليومي باستخدام لا.",("negation","present-subject-agreement"),("daily-life_a1","common-verbs_a1"),("daily_a1",)),
    _lesson(4,1,5,"writing","يومي","كتابة 5–6 جمل عن يوم معتاد مع ظرفي تكرار على الأقل.",("present-tense","negation","adverbs-frequency"),("daily-life_a1","common-verbs_a1"),("daily_a1",)),
    _lesson(4,2,1,"grammar","مطابقة الفعل والفاعل","تثبيت صيغ المضارع مع أنا وهو وهي ونحن وهم.",("present-subject-agreement","present-tense"),("common-verbs_a1",),("daily_a1",)),
    _lesson(4,2,2,"vocabulary","دائمًا وأحيانًا","تمييز ظروف التكرار واستخدامها في جمل جديدة.",("adverbs-frequency","present-tense"),("daily-life_a1",),("daily_a1",)),
    _lesson(4,2,3,"reading","روتين شخصين","مقارنة روتين شخصين في نص قصير.",("present-tense","negation","adverbs-frequency"),("daily-life_a1","common-verbs_a1"),("daily_a1",)),
    _lesson(4,2,4,"review","ما الذي تفعله؟","إجراء مقابلة قصيرة عن الروتين اليومي.",("question-words","present-tense","negation"),("daily-life_a1","common-verbs_a1"),("daily_a1",)),
    _lesson(4,2,5,"review","مراجعة الروتين","استرجاع المضارع والنفي ومفردات الروتين والتكرار.",("present-tense","present-subject-agreement","negation","adverbs-frequency"),("daily-life_a1","common-verbs_a1"),("daily_a1",)),

    # Units 5–8 use the same explicit progression and existing content IDs.
    _lesson(5,1,1,"grammar","الأعداد والوقت","استخدام الأعداد الأساسية والسؤال عن الساعة.",("numbers","clock-time"),("numbers_time_a1","appointments_a1"),("time_a1",)),
    _lesson(5,1,2,"vocabulary","المواعيد","ذكر الوقت والموعد واليوم في مواقف يومية.",("clock-time","prepositions"),("numbers_time_a1","appointments_a1"),("time_a1",)),
    _lesson(5,1,3,"listening","موعد في الساعة","فهم وقت وموعد من حوار قصير.",("clock-time","numbers"),("numbers_time_a1","appointments_a1"),("time_a1",)),
    _lesson(5,1,4,"review","تحديد موعد","اقتراح موعد والسؤال عن الوقت.",("clock-time","question-words"),("appointments_a1","numbers_time_a1"),("time_a1",)),
    _lesson(5,1,5,"review","مراجعة الوقت","تثبيت الأعداد والساعة والمواعيد دون قاعدة جديدة.",("numbers","clock-time","prepositions"),("numbers_time_a1","appointments_a1"),("time_a1",)),
    _lesson(6,1,1,"grammar","الكمية والسعر","استخدام كلمات الكمية والمفعول به في طلبات بسيطة.",("quantifiers","accusative-intro"),("food_a1","shopping_a1"),("restaurant_a1","shopping_a1")),
    _lesson(6,1,2,"vocabulary","الطعام والشراء","تسمية أطعمة وأسعار وطرق دفع أساسية.",("quantifiers","question-words"),("food_a1","shopping_a1"),("restaurant_a1","shopping_a1")),
    _lesson(6,1,3,"listening","في المطعم","فهم طلب طعام وسؤال عن السعر أو الحساب.",("accusative-intro","question-words"),("food_a1","shopping_a1"),("restaurant_a1",)),
    _lesson(6,1,4,"review","في المتجر","إجراء حوار شراء قصير عن السعر والكمية.",("question-words","quantifiers"),("shopping_a1","food_a1"),("shopping_a1",)),
    _lesson(6,1,5,"review","مراجعة الطعام والشراء","دمج الطلب والسعر والكمية والدفع.",("quantifiers","accusative-intro","question-words"),("food_a1","shopping_a1"),("restaurant_a1","shopping_a1")),
    _lesson(7,1,1,"grammar","أين يوجد؟","استخدام يوجد وتوجد مع تعبيرات المكان.",("there-is-there-are","place-expressions"),("places_a1","directions_a1"),("directions_a1",)),
    _lesson(7,1,2,"vocabulary","الأماكن والاتجاهات","تسمية الأماكن واليمين واليسار وأمام وخلف.",("place-expressions","prepositions"),("places_a1","directions_a1"),("directions_a1",)),
    _lesson(7,1,3,"listening","اسأل عن الطريق","فهم تعليمات اتجاه قصيرة.",("imperative-intro","place-expressions"),("places_a1","directions_a1"),("directions_a1",)),
    _lesson(7,1,4,"review","إعطاء الاتجاهات","إعطاء طريق بسيط من مكان إلى آخر.",("imperative-intro","prepositions","place-expressions"),("places_a1","directions_a1"),("directions_a1",)),
    _lesson(7,1,5,"review","مراجعة الأماكن","دمج سؤال المكان والوجود والاتجاهات.",("there-is-there-are","place-expressions","prepositions","imperative-intro"),("places_a1","directions_a1"),("directions_a1",)),
    _lesson(8,1,1,"grammar","أسئلة التواصل","استخدام هل وماذا وكيف ولماذا في مواقف يومية.",("basic-questions","question-words"),("communication_a1","review_a1"),("help_a1",)),
    _lesson(8,1,2,"vocabulary","طلب المساعدة","استخدام عبارات عدم الفهم وطلب التكرار والإبطاء.",("basic-questions","negation"),("communication_a1","review_a1"),("help_a1",)),
    _lesson(8,1,3,"reading","نص A1 متكامل","قراءة نص قصير يجمع التعارف والبيت والروتين والشراء.",("pronouns","present-tense","adjectives","question-words"),("review_a1","communication_a1"),("help_a1",)),
    _lesson(8,1,4,"review","مهمة تواصل نهائية","إدارة حوار قصير يجمع عدة مواقف من مستوى A1.",("question-words","present-tense","prepositions","negation"),("review_a1","communication_a1"),("help_a1",)),
    _lesson(8,1,5,"review","اختبار نهاية A1","استرجاع القواعد والمفردات والتعبيرات الأساسية والاستعداد لـA2.",("pronouns","question-words","present-tense","prepositions"),("review_a1","communication_a1"),("help_a1",)),
)


def get_arabic_a1_lessons(unit_id: str | None = None) -> tuple[ArabicA1Lesson, ...]:
    """Return the full A1 sequence or only lessons belonging to one unit."""
    if unit_id is None:
        return ARABIC_A1_LESSONS
    return tuple(lesson for lesson in ARABIC_A1_LESSONS if lesson.unit_id == unit_id)

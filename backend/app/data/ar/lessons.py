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


@dataclass(frozen=True)
class ArabicA1ContentSeed:
    """Curated seed content used to ground LLM lesson generation."""
    lesson_id: str
    target_phrases: tuple[str, ...]
    model_sentences: tuple[str, ...]
    comprehension_prompt: str
    production_prompt: str


ARABIC_A1_CONTENT_SEEDS: tuple[ArabicA1ContentSeed, ...] = (
    ArabicA1ContentSeed("a1-u1-w2-d2", ("كم عمرك؟", "أنا في العشرين.", "أين تسكن؟", "أسكن في الجزائر."), ("كم عمرك؟ عمري عشرون سنة.", "أين تسكن؟ أسكن في وهران."), "استخرج العمر والمدينة واللغة من الحوار.", "قدّم ثلاث معلومات شخصية باستخدام الأسئلة المستهدفة."),
    ArabicA1ContentSeed("a1-u1-w2-d3", ("هل أنت طالب؟", "نعم، أنا طالب.", "هل تعمل؟", "نعم، أعمل في شركة."), ("هل أنت طالب؟ نعم، أدرس في الجامعة.", "هل تعمل؟ نعم، أعمل صباحًا."), "حدد الأسئلة والإجابات المتطابقة.", "أنشئ حوارًا قصيرًا من أربعة أسئلة وأجوبة."),
    ArabicA1ContentSeed("a1-u1-w2-d4", ("من أنت؟", "أنا طالب.", "من أين أنت؟", "أنا من الجزائر."), ("من أنت؟ أنا سليم.", "من أين أنت؟ أنا من الجزائر."), "ميّز بين سؤال الهوية وسؤال البلد.", "أجرِ حوار تعارف كاملًا باستخدام ما تعلمته في الوحدة."),
    ArabicA1ContentSeed("a1-u1-w1-d1", ("مرحبًا", "اسمي", "أنا من الجزائر", "أنا طالب"), ("مرحبًا، اسمي أحمد.", "أنا طالب من الجزائر."), "استخرج التحية والاسم والبلد والمهنة من الحوار.", "قدّم نفسك في أربع جمل قصيرة باستخدام مفردات التعارف."),
    ArabicA1ContentSeed("a1-u1-w1-d2", ("ما اسمك؟", "من أين أنت؟", "ماذا تعمل؟", "أدرس في الجامعة."), ("ما اسمك؟ اسمي علي.", "من أين أنت؟ أنا من وهران.", "ماذا تعمل؟ أنا أعمل في شركة."), "حدد الاسم والمدينة والعمل أو الدراسة.", "اكتب حوارًا من سؤالين وجوابين عن المعلومات الشخصية."),
    ArabicA1ContentSeed("a1-u1-w1-d3", ("مرحبًا", "أهلًا", "صباح الخير", "مساء الخير"), ("مرحبًا، اسمي محمد.", "مساء الخير، أنا طالب."), "حدد التحية المناسبة في بداية الحوار ونهايته.", "استخدم تحيتين مختلفتين في حوار تعارف قصير."),
    ArabicA1ContentSeed("a1-u1-w1-d4", ("أنا طالب من الجزائر.", "هي طالبة من تونس.", "هو مهندس.", "هي طبيبة."), ("أنا خالد. أنا من الجزائر.", "هذه مريم. هي طالبة."), "اقرأ الحوار وحدد الضمائر والجمل الاسمية.", "اكتب تعريفًا قصيرًا لشخصين."),
    ArabicA1ContentSeed("a1-u1-w1-d5", ("اسمي ...", "أنا من ...", "أنا طالب/طالبة.", "أعمل في ..."), ("اسمي ليلى.", "أنا من قسنطينة.", "أنا طالبة.", "أدرس اللغة العربية."), "اقرأ نموذج التعريف واستخرج أربع معلومات.", "اكتب ملفك الشخصي في أربع أو خمس جمل."),
    ArabicA1ContentSeed("a1-u1-w2-d1", ("اسم", "بلد", "مدينة", "لغة"), ("ما اسمك؟ اسمي علي.", "ما بلدك؟ أنا من الجزائر."), "استخرج الاسم والبلد والمدينة واللغة من الحوار.", "اسأل عن أربع معلومات شخصية وأجب عنها."),
    ArabicA1ContentSeed("a1-u1-w2-d5", ("ما اسمك؟", "من أين أنت؟", "ماذا تدرس؟", "تشرفت بك."), ("ما اسمك؟ اسمي نور.", "ماذا تدرس؟ أدرس العربية."), "تحقق من فهم حوار التعارف.", "نفّذ حوار تعارف من ست جمل دون استخدام لغة وسيطة."),
    ArabicA1ContentSeed("a1-u2-w1-d1", ("هذا أبي.", "هذه أمي.", "هذا أخي.", "هذه أختي."), ("هذا أبي. هذه أمي.", "هذا أخي وهذه أختي."), "سمِّ أفراد الأسرة المذكورين وحدد صلة كل شخص.", "قدّم أربعة أفراد من عائلتك باستخدام هذا/هذه."),
    ArabicA1ContentSeed("a1-u2-w1-d2", ("من هذا؟", "هذا أخي.", "من هذه؟", "هذه أختي."), ("من هذا؟ هذا أخي.", "من هذه؟ هذه أختي."), "طابق كل سؤال مع الشخص المناسب في وصف الأسرة.", "أنشئ حوارًا من أربعة أسئلة وأجوبة عن أفراد الأسرة."),
    ArabicA1ContentSeed("a1-u2-w1-d3", ("عائلة صغيرة", "عائلتي كبيرة.", "عندي أخ واحد.", "عندي أخت واحدة."), ("عندي أخ واحد وأخت واحدة.", "عائلتي صغيرة."), "استخرج عدد أفراد الأسرة وعلاقات القرابة من النص.", "اكتب وصفًا قصيرًا لعائلتك باستخدام عندي."),
    ArabicA1ContentSeed("a1-u2-w1-d4", ("كتاب أبي", "هاتف أمي", "حقيبة أخي", "غرفة أختي"), ("هذا كتاب أبي.", "هذه حقيبة أخي."), "حدد صاحب كل شيء في الوصف.", "صف ثلاثة أشياء تخص أفرادًا من عائلتك."),
    ArabicA1ContentSeed("a1-u2-w1-d5", ("أخي طالب.", "أختي طالبة.", "أبي موظف.", "أمي طبيبة."), ("أخي طالب في الجامعة.", "أمي طبيبة في المستشفى."), "استخرج مهن أفراد الأسرة من النص.", "اكتب خمس جمل عن أسرتك وملكية الأشياء أو المهن."),
    ArabicA1ContentSeed("a1-u2-w2-d1", ("البيتُ الكبيرُ", "الأبُ الجديدُ", "الأمُّ الطيبةُ", "الأخُ الصغيرُ"), ("هذا الأخُ الصغيرُ.", "هذه الأمُّ الطيبةُ."), "حدد الاسم المعرفة والصفة في كل تركيب.", "كوّن أربع عبارات معرفة تصف أفراد أسرتك."),
    ArabicA1ContentSeed("a1-u2-w2-d2", ("ما رقم هاتفك؟", "هذا هاتفي.", "ما عنوانك؟", "ما عملك؟"), ("هذا هاتفي، وهذا عنواني.", "ما عملك؟ أنا موظف."), "استخرج رقم الهاتف والعنوان والعمل من الحوار.", "قدّم أربع معلومات شخصية باستخدام مفردات الوحدة."),
    ArabicA1ContentSeed("a1-u2-w2-d3", ("هذه صورة العائلة.", "في الصورة أبي.", "في الصورة أمي.", "في الصورة أختي."), ("هذه صورة عائلتي في البيت.", "أختي الصغيرة بجانب أمي."), "استخرج أفراد الأسرة ومواقعهم في الصورة.", "صف صورة عائلية في خمس جمل بسيطة."),
    ArabicA1ContentSeed("a1-u2-w2-d4", ("من هذا الرجل؟", "هذا أبي.", "من هذه المرأة؟", "هذه أمي."), ("من هذا؟ هذا أبي.", "من هذه؟ هذه أمي."), "استخرج أسئلة القرابة وإجاباتها.", "أجرِ حوارًا قصيرًا لتقديم شخصين من عائلتك."),
    ArabicA1ContentSeed("a1-u2-w2-d5", ("هذه عائلتي.", "هذا أبي وهذه أمي.", "هذا أخي وهذه أختي.", "أحب عائلتي."), ("أبي في العمل وأمي في البيت.", "أخي يدرس وأختي تقرأ."), "استخرج أفراد الأسرة والأفعال المرتبطة بهم.", "قدّم عائلتك في ست جمل باستخدام مفردات الوحدة."),
    ArabicA1ContentSeed("a1-u3-w1-d1", ("هذا بيتٌ صغيرٌ.", "هذه غرفةٌ كبيرةٌ.", "هذا مطبخٌ نظيفٌ.", "هذا حمامٌ صغيرٌ."), ("هذا بيت صغير وهذه غرفة كبيرة.", "المطبخ نظيف والحمام صغير."), "حدد أسماء الغرف والصفات.", "صف بيتك بأربع جمل باستخدام هذا وهذه."),
    ArabicA1ContentSeed("a1-u3-w1-d2", ("غرفة النوم", "المطبخ", "الحمام", "غرفة الجلوس"), ("في البيت غرفة نوم.", "المطبخ بجانب غرفة الجلوس."), "استخرج أسماء الغرف من النص.", "اذكر خمس غرف أو أماكن في بيتك."),
    ArabicA1ContentSeed("a1-u3-w1-d3", ("هذا كرسيٌ جديدٌ.", "هذه طاولةٌ قديمةٌ.", "هذا سريرٌ كبيرٌ.", "هذه نافذةٌ نظيفةٌ."), ("الكرسي جديد والطاولة قديمة.", "السرير كبير والنافذة نظيفة."), "حدد الصفة المناسبة لكل اسم.", "صف أربعة أشياء في غرفتك مع صفاتها."),
    ArabicA1ContentSeed("a1-u3-w1-d4", ("أين الكتاب؟", "الكتاب على الطاولة.", "أين المفتاح؟", "المفتاح بجانب الحقيبة."), ("الكتاب على الطاولة والمفتاح بجانب الحقيبة.", "الحقيبة قرب الباب."), "حدد مكان كل شيء في النص.", "اكتب أربع جمل تحدد أماكن أشياء في بيتك."),
    ArabicA1ContentSeed("a1-u3-w1-d5", ("غرفتي صغيرة.", "في غرفتي سرير.", "على الطاولة كتاب.", "بجانب السرير حقيبة."), ("غرفتي صغيرة وفيها سرير.", "على الطاولة كتاب وبجانب السرير حقيبة."), "استخرج الأشياء ومواقعها في الغرفة.", "صف غرفتك بخمس جمل مكانية."),
    ArabicA1ContentSeed("a1-u3-w2-d1", ("الكتاب في الحقيبة.", "المفتاح على الطاولة.", "الحقيبة بجانب الباب.", "الكرسي أمام الطاولة."), ("أين المفتاح؟ هو على الطاولة.", "أين الحقيبة؟ هي بجانب الباب."), "حدد حروف الجر وتعبيرات المكان.", "اسأل عن مكان ثلاثة أشياء وأجب عنها."),
    ArabicA1ContentSeed("a1-u3-w2-d2", ("السرير أمام النافذة.", "الكرسي خلف الطاولة.", "الحقيبة بين الكرسي والباب.", "القلم بجانب الدفتر."), ("الحقيبة بين الكرسي والباب.", "القلم بجانب الدفتر."), "استخرج علاقات المكان من الوصف.", "صف موقع أربعة أشياء في غرفتك."),
    ArabicA1ContentSeed("a1-u3-w2-d3", ("أين القلم؟", "القلم على المكتب.", "أين المفتاح؟", "المفتاح في الحقيبة."), ("القلم على المكتب والمفتاح في الحقيبة.", "الكتاب بجانب النافذة."), "استمع وحدد مكان كل شيء.", "أعطِ تعليمات لشخص يبحث عن ثلاثة أشياء."),
    ArabicA1ContentSeed("a1-u3-w2-d4", ("أين سريري؟", "سريرك في الغرفة.", "أين كتابي؟", "كتابك على الطاولة."), ("سريري في الغرفة وكتابي على الطاولة.", "حقيبتي بجانب الباب."), "أجب عن أسئلة المكان من الحوار.", "أجرِ جولة صوتية قصيرة في غرفتك."),
    ArabicA1ContentSeed("a1-u3-w2-d5", ("هذا بيتي.", "هذه غرفتي.", "الكتاب على الطاولة.", "المفتاح بجانب الباب."), ("بيتي صغير لكنه مريح.", "في غرفتي سرير وكتاب."), "استخرج أسماء الأشياء وتعبيرات المكان.", "صف بيتك في ست جمل تجمع أسماء الإشارة والمكان."),
    ArabicA1ContentSeed("a1-u4-w1-d1", ("أستيقظ صباحًا.", "أشرب الماء.", "أذهب إلى العمل.", "أعود إلى البيت."), ("أستيقظ صباحًا وأشرب الماء.", "أذهب إلى العمل ثم أعود إلى البيت."), "رتّب أنشطة الصباح والعودة في تسلسل صحيح.", "صف بداية يومك بأربع جمل."),
    ArabicA1ContentSeed("a1-u4-w1-d2", ("أقرأ كل يوم.", "أكتب في الدفتر.", "أعمل صباحًا.", "أنام ليلًا."), ("أقرأ كل يوم وأكتب في الدفتر.", "أعمل صباحًا وأنام ليلًا."), "حدد الأفعال اليومية في النص.", "اكتب أربع جمل عن أنشطتك اليومية."),
    ArabicA1ContentSeed("a1-u4-w1-d3", ("أستيقظ في السابعة.", "أذهب إلى الجامعة.", "أدرس العربية.", "أعود مساءً."), ("أستيقظ في السابعة وأذهب إلى الجامعة.", "أدرس العربية ثم أعود مساءً."), "استخرج أوقات وأنشطة اليوم.", "اكتب جدولًا بسيطًا ليومك."),
    ArabicA1ContentSeed("a1-u4-w1-d4", ("لا أعمل اليوم.", "لا أذهب إلى السوق.", "لا أشرب القهوة.", "لا أنام مبكرًا."), ("لا أعمل اليوم ولا أذهب إلى السوق.", "لا أشرب القهوة مساءً."), "حدد الجمل المنفية بالفعل لا.", "اكتب ثلاث جمل مثبتة وثلاث جمل منفية عن يومك."),
    ArabicA1ContentSeed("a1-u4-w1-d5", ("أستيقظ مبكرًا.", "أدرس صباحًا.", "أعمل بعد الظهر.", "أنام ليلًا."), ("أستيقظ مبكرًا وأدرس صباحًا.", "أعمل بعد الظهر وأنام ليلًا."), "استخرج أربع فترات من اليوم والأنشطة.", "اكتب ست جمل تصف يومك المعتاد."),
    ArabicA1ContentSeed("a1-u4-w2-d1", ("أنا أقرأ.", "هو يعمل.", "هي تدرس.", "هم يذهبون."), ("أنا أقرأ كل يوم.", "هم يذهبون إلى العمل صباحًا."), "طابق الفاعل مع صيغة الفعل.", "اكتب جملة مع أنا وهو وهي وهم."),
    ArabicA1ContentSeed("a1-u4-w2-d2", ("دائمًا أدرس صباحًا.", "أحيانًا أشرب القهوة.", "غالبًا أقرأ ليلًا.", "نادرًا أذهب متأخرًا."), ("دائمًا أدرس صباحًا وأحيانًا أقرأ ليلًا.", "غالبًا أعمل مبكرًا."), "حدد ظروف التكرار في النص.", "صف عاداتك باستخدام دائمًا وأحيانًا وغالبًا."),
    ArabicA1ContentSeed("a1-u4-w2-d3", ("علي يستيقظ مبكرًا.", "سارة تدرس صباحًا.", "علي لا يعمل مساءً.", "سارة تقرأ ليلًا."), ("علي يستيقظ مبكرًا وسارة تدرس صباحًا.", "علي لا يعمل مساءً وسارة تقرأ ليلًا."), "قارن روتين الشخصين.", "اكتب فرقين بين روتينك وروتين شخص آخر."),
    ArabicA1ContentSeed("a1-u4-w2-d4", ("ماذا تفعل صباحًا؟", "أستيقظ وأدرس.", "متى تذهب إلى العمل؟", "أذهب الساعة الثامنة."), ("ماذا تفعل مساءً؟ أعود إلى البيت.", "متى تنام؟ أنام ليلًا."), "استخرج أسئلة الروتين وأجوبتها.", "أجرِ مقابلة من أربعة أسئلة عن الروتين."),
    ArabicA1ContentSeed("a1-u4-w2-d5", ("أستيقظ صباحًا.", "أدرس العربية.", "أذهب إلى العمل.", "لا أعمل يوم الجمعة."), ("أحيانًا أقرأ ليلًا.", "أعود إلى البيت مساءً."), "استخرج الأفعال والنفي وظروف التكرار.", "قدّم روتينك اليومي في ست جمل."),
    ArabicA1ContentSeed("a1-u5-w1-d1", ("الساعة الواحدة.", "الساعة الثالثة.", "الساعة السادسة.", "الساعة التاسعة."), ("الساعة الثالثة الآن.", "موعدي الساعة التاسعة."), "حدد الأوقات المذكورة.", "قل أربع ساعات مختلفة بصوت واضح."),
    ArabicA1ContentSeed("a1-u5-w1-d2", ("متى الموعد؟", "الموعد الساعة العاشرة.", "اليوم الاثنين.", "الموعد صباحًا."), ("الموعد الساعة العاشرة صباحًا.", "اليوم الاثنين ولدي موعد."), "استخرج اليوم والوقت من الحوار.", "حدّد موعدًا لشخص آخر باستخدام اليوم والساعة."),
    ArabicA1ContentSeed("a1-u5-w1-d3", ("كم الساعة؟", "الساعة الخامسة.", "متى نلتقي؟", "نلتقي الساعة الرابعة."), ("كم الساعة الآن؟ الساعة الخامسة.", "نلتقي الساعة الرابعة مساءً."), "حدد سؤال الوقت وإجابته.", "اكتب حوارًا قصيرًا للسؤال عن الوقت."),
    ArabicA1ContentSeed("a1-u5-w1-d4", ("لدي موعد.", "موعدي الساعة الثامنة.", "هل نلتقي غدًا؟", "نعم، غدًا مناسب."), ("موعدي الساعة الثامنة غدًا.", "هل نلتقي غدًا صباحًا؟ نعم."), "استخرج تفاصيل الموعد.", "اقترح موعدًا وحدد اليوم والساعة."),
    ArabicA1ContentSeed("a1-u5-w1-d5", ("الساعة الثانية.", "الساعة السابعة.", "الساعة العاشرة.", "الساعة الثانية عشرة."), ("الدرس الساعة السابعة.", "الموعد الساعة العاشرة."), "اختبر فهم الأعداد والساعة.", "اكتب أربعة مواعيد مختلفة."),
    ArabicA1ContentSeed("a1-u5-w2-d1", ("اليوم الثلاثاء.", "غدًا الأربعاء.", "أمس الاثنين.", "موعدي غدًا."), ("غدًا لدي موعد صباحًا.", "أمس كان عندي درس."), "حدد كلمات الزمن: اليوم وغدًا وأمس.", "اكتب ثلاث جمل عن اليوم وغدًا وأمس."),
    ArabicA1ContentSeed("a1-u5-w2-d2", ("لدي موعد الساعة التاسعة.", "أريد تغيير الموعد.", "الموعد الجديد الساعة الحادية عشرة.", "هل يناسبك الوقت الجديد؟"), ("أريد تغيير الموعد إلى الساعة الحادية عشرة.", "نعم، الوقت الجديد مناسب."), "حدد سبب تغيير الموعد والوقت الجديد.", "أجرِ حوارًا لتغيير موعد."),
    ArabicA1ContentSeed("a1-u5-w2-d3", ("موعد الطبيب صباحًا.", "موعد العمل بعد الظهر.", "الساعة التاسعة للطبيب.", "الساعة الثانية للعمل."), ("أذهب إلى الطبيب الساعة التاسعة.", "أذهب إلى العمل الساعة الثانية."), "استخرج المواعيد من الجدول.", "اكتب جدول مواعيد ليوم واحد."),
    ArabicA1ContentSeed("a1-u5-w2-d4", ("متى تبدأ؟", "أبدأ الساعة الثامنة.", "متى ينتهي الدرس؟", "ينتهي الساعة العاشرة."), ("أبدأ الساعة الثامنة وينتهي الدرس العاشرة.", "موعدنا بعد الظهر."), "حدد بداية ونهاية النشاط.", "أجرِ حوارًا عن بداية موعد ونهايته."),
    ArabicA1ContentSeed("a1-u5-w2-d5", ("كم الساعة؟", "متى الموعد؟", "لدي موعد صباحًا.", "سأغيّر الموعد إلى المساء."), ("الساعة التاسعة صباحًا.", "موعدي مساءً عند الساعة السادسة."), "استخرج الوقت والموعد من النص.", "قدّم موقفًا كاملًا لتحديد موعد أو تغييره."),
    ArabicA1ContentSeed("a1-u6-w1-d1", ("أريد خبزًا.", "أريد ماءً.", "أريد أرزًا.", "أريد حليبًا."), ("أريد خبزًا وماءً.", "أريد أرزًا وحليبًا."), "استخرج طلبات الطعام.", "اطلب أربعة أطعمة أو مشروبات في جمل قصيرة."),
    ArabicA1ContentSeed("a1-u6-w1-d2", ("تفاحة واحدة.", "كيلو تفاح.", "بعض الأرز.", "قليل من الماء."), ("أريد كيلو تفاح.", "أريد بعض الأرز من فضلك."), "حدد كلمات الكمية.", "اطلب كميات مختلفة من ثلاثة أطعمة."),
    ArabicA1ContentSeed("a1-u6-w1-d3", ("كم سعر الخبز؟", "سعر الخبز عشرة.", "كم سعر الحليب؟", "سعر الحليب خمسة."), ("سعر الخبز عشرة وسعر الحليب خمسة.", "كم سعر التفاح؟ سعره ثمانية."), "استخرج الأسعار من الحوار.", "أجرِ حوارًا عن سعر ثلاثة منتجات."),
    ArabicA1ContentSeed("a1-u6-w1-d4", ("أريد القائمة.", "أريد شوربة.", "أريد هذا الطبق.", "الحساب من فضلك."), ("أريد شوربة وهذا الطبق.", "الحساب من فضلك بعد الطعام."), "حدد طلبات المطعم وتسلسلها.", "مثّل حوارًا قصيرًا في مطعم."),
    ArabicA1ContentSeed("a1-u6-w1-d5", ("أريد ماءً باردًا.", "أريد خبزًا طازجًا.", "أريد تفاحة كبيرة.", "أريد طبقًا صغيرًا."), ("أريد ماءً باردًا وتفاحة كبيرة.", "أريد طبقًا صغيرًا وخبزًا طازجًا."), "حدد الاسم والصفة في طلبات الطعام.", "كوّن أربعة طلبات تجمع الطعام والصفة."),
    ArabicA1ContentSeed("a1-u6-w2-d1", ("هذا غالٍ.", "هذا رخيص.", "السعر مناسب.", "أريد سعرًا أقل."), ("هذا المنتج غالٍ جدًا.", "السعر مناسب لكن أريد واحدًا آخر."), "استخرج عبارات تقييم السعر.", "تفاوض على سعر منتج في حوار قصير."),
    ArabicA1ContentSeed("a1-u6-w2-d2", ("أدفع نقدًا.", "أدفع بالبطاقة.", "أين الصندوق؟", "أين الحساب؟"), ("أدفع بالبطاقة عند الصندوق.", "أين الصندوق؟ أريد الدفع."), "حدد طريقة الدفع ومكان الصندوق.", "أكمل حوار شراء من اختيار المنتج إلى الدفع."),
    ArabicA1ContentSeed("a1-u6-w2-d3", ("هل لديك مقاس آخر؟", "هل لديك منتج آخر؟", "أريد هذا المقاس.", "سآخذ هذا."), ("هل لديك مقاس آخر؟ نعم، هذا مناسب.", "سآخذ هذا المنتج."), "حدد سؤال البديل وقرار الشراء.", "اطلب منتجًا آخر ثم قرر ما ستشتريه."),
    ArabicA1ContentSeed("a1-u6-w2-d4", ("ماذا تنصح؟", "أريد هذا الطبق.", "هل هذا حار؟", "لا، هذا غير حار."), ("ماذا تنصح؟ أنصح بهذا الطبق.", "هل هذا حار؟ لا، إنه غير حار."), "استخرج السؤال والجواب عن الطعام.", "أجرِ حوارًا تطلب فيه توصية عن طبق."),
    ArabicA1ContentSeed("a1-u6-w2-d5", ("أريد خبزًا.", "كم سعره؟", "أدفع نقدًا.", "شكرًا."), ("أريد خبزًا وماءً.", "كم السعر؟ أدفع نقدًا."), "استخرج مراحل الشراء: الطلب والسعر والدفع.", "نفّذ موقف شراء كاملًا من أربع مراحل."),
    ArabicA1ContentSeed("a1-u7-w1-d1", ("يوجد بنك هنا.", "توجد مدرسة هناك.", "يوجد سوق قريب.", "توجد صيدلية بجانب البنك."), ("يوجد بنك هنا وسوق قريب.", "توجد صيدلية بجانب البنك."), "حدد الأماكن واستخدام يوجد/توجد.", "صف أربعة أماكن في منطقتك."),
    ArabicA1ContentSeed("a1-u7-w1-d2", ("أين المدرسة؟", "المدرسة أمام البنك.", "أين السوق؟", "السوق خلف المدرسة."), ("المدرسة أمام البنك والسوق خلفها.", "الصيدلية بجانب السوق."), "استخرج علاقات المكان.", "صف موقع ثلاثة أماكن بالنسبة إلى بعضها."),
    ArabicA1ContentSeed("a1-u7-w1-d3", ("أين المستشفى؟", "كيف أصل إلى المستشفى؟", "اذهب إلى الأمام.", "ثم انعطف يمينًا."), ("اذهب إلى الأمام ثم انعطف يمينًا.", "المستشفى بعد البنك."), "حدد خطوات الطريق.", "أعطِ طريقًا من أربع خطوات إلى مكان قريب."),
    ArabicA1ContentSeed("a1-u7-w1-d4", ("انعطف يمينًا.", "انعطف يسارًا.", "اذهب إلى الأمام.", "توقف عند البنك."), ("انعطف يمينًا ثم اذهب إلى الأمام.", "توقف عند البنك ثم اسأل عن المدرسة."), "استخرج أفعال الأمر في التعليمات.", "أعطِ أربع تعليمات لشخص يبحث عن مكان."),
    ArabicA1ContentSeed("a1-u7-w1-d5", ("المحطة قريبة.", "المطار بعيد.", "المستشفى هنا.", "الجامعة هناك."), ("المحطة قريبة والمطار بعيد.", "المستشفى هنا والجامعة هناك."), "قارن قرب وبعد الأماكن.", "صف أربعة أماكن قريبة أو بعيدة."),
    ArabicA1ContentSeed("a1-u7-w2-d1", ("البنك بجانب السوق.", "المدرسة بين البنك والمستشفى.", "المحطة خلف الفندق.", "الصيدلية أمام المدرسة."), ("المدرسة بين البنك والمستشفى.", "الصيدلية أمام المدرسة."), "حدد علاقات بين الأماكن.", "صف خريطة صغيرة باستخدام بين وأمام وخلف."),
    ArabicA1ContentSeed("a1-u7-w2-d2", ("أين المحطة؟", "المحطة قريبة.", "كيف أصل إلى الفندق؟", "اذهب إلى اليمين."), ("أين المحطة؟ هي قريبة.", "اذهب إلى اليمين ثم إلى الأمام."), "استخرج سؤال المكان وتعليمات الطريق.", "أجرِ حوارًا للسؤال عن مكان ثم إعطاء الطريق."),
    ArabicA1ContentSeed("a1-u7-w2-d3", ("من المدرسة إلى السوق.", "اخرج من المدرسة.", "اذهب إلى اليسار.", "اعبر الشارع."), ("اخرج من المدرسة واذهب إلى اليسار.", "اعبر الشارع ثم ستجد السوق."), "حدد نقطة البداية والخطوات.", "صف طريقًا من المدرسة إلى السوق."),
    ArabicA1ContentSeed("a1-u7-w2-d4", ("المستشفى بجانب البنك.", "البنك أمام المحطة.", "المحطة قريبة.", "السوق بعيد."), ("البنك أمام المحطة والسوق بعيد.", "المستشفى بجانب البنك."), "استخرج المواقع والمسافات.", "صف أربعة أماكن في حيّك."),
    ArabicA1ContentSeed("a1-u7-w2-d5", ("أين المكان؟", "كيف أصل إليه؟", "يوجد سوق قريب.", "اذهب إلى اليمين."), ("يوجد سوق قريب من المحطة.", "اذهب إلى اليمين ثم إلى الأمام."), "استخرج سؤال المكان والجواب والتعليمات.", "مثّل موقفًا كاملًا للسؤال عن الطريق."),
    ArabicA1ContentSeed("a1-u8-w1-d1", ("هل تفهم؟", "نعم، أفهم.", "هل يمكنك التكرار؟", "تحدث ببطء من فضلك."), ("هل تفهم السؤال؟ نعم.", "هل يمكنك التكرار ببطء؟"), "حدد عبارات التحقق من الفهم.", "اطلب من شريكك إعادة جملة ببطء."),
    ArabicA1ContentSeed("a1-u8-w1-d2", ("لا أفهم.", "ماذا يعني هذا؟", "ماذا يعني هذا السؤال؟", "هل يمكنك الشرح؟"), ("لا أفهم هذه الكلمة.", "ماذا يعني هذا؟ هل يمكنك الشرح؟"), "حدد عبارات طلب التوضيح.", "اكتب أربعة أسئلة عندما لا تفهم الدرس."),
    ArabicA1ContentSeed("a1-u8-w1-d3", ("من فضلك، أعد.", "تحدث ببطء.", "مرة أخرى من فضلك.", "شكرًا لك."), ("من فضلك أعد الجملة.", "تحدث ببطء ومرة أخرى من فضلك."), "استخرج عبارات طلب الإعادة.", "مثّل موقفًا تطلب فيه تكرار شرح قصير."),
    ArabicA1ContentSeed("a1-u8-w1-d4", ("هل يمكنك مساعدتي؟", "نعم، بالتأكيد.", "أحتاج إلى مساعدة.", "شكرًا جزيلًا."), ("هل يمكنك مساعدتي في السؤال؟", "نعم، بالتأكيد. سأساعدك."), "حدد طلب المساعدة والرد عليه.", "أجرِ حوارًا من أربعة أدوار لطلب المساعدة."),
    ArabicA1ContentSeed("a1-u8-w1-d5", ("أفهم السؤال.", "لا أفهم الكلمة.", "أعرف الجواب.", "لا أعرف الجواب."), ("أفهم السؤال لكن لا أعرف الجواب.", "لا أفهم الكلمة، هل يمكنك شرحها؟"), "ميّز بين أفهم ولا أفهم وأعرف ولا أعرف.", "اكتب أربع جمل عن فهمك أثناء التعلم."),
    ArabicA1ContentSeed("a1-u8-w2-d1", ("ماذا يعني هذا؟", "كيف أقول هذا؟", "هل هذا صحيح؟", "نعم، صحيح."), ("هل هذا صحيح؟ نعم، هذا صحيح.", "كيف أقول هذه الكلمة بالعربية؟"), "حدد أسئلة التحقق من اللغة.", "اطرح ثلاثة أسئلة للتحقق من إجابتك."),
    ArabicA1ContentSeed("a1-u8-w2-d2", ("أريد أن أتعلم العربية.", "أتعلم كل يوم.", "أقرأ وأكتب بالعربية.", "أريد أن أتحدث أفضل."), ("أتعلم العربية كل يوم.", "أقرأ وأكتب وأريد أن أتحدث أفضل."), "استخرج أهداف المتعلم وأنشطته.", "اكتب خطة تعلم قصيرة من أربع جمل."),
    ArabicA1ContentSeed("a1-u8-w2-d3", ("هل تفهم السؤال؟", "لا أفهم", "ماذا يعني هذا؟", "تحدث ببطء"), ("لا أفهم السؤال.", "ماذا يعني هذا؟ تحدث ببطء من فضلك."), "حدد عبارات عدم الفهم وطلب التوضيح.", "اطلب شرح كلمة أو سؤال باستخدام عبارات التواصل."),
    ArabicA1ContentSeed("a1-u8-w2-d4", ("هل يمكنك أن تساعدني؟", "أحتاج إلى مساعدة", "من فضلك", "شكرًا"), ("هل يمكنك أن تساعدني؟ أحتاج إلى مساعدة.", "من فضلك، أعد السؤال. شكرًا."), "استخرج طلب المساعدة وعبارة الشكر.", "مثّل حوارًا قصيرًا لطلب المساعدة وشكر الشخص."),
    ArabicA1ContentSeed("a1-u8-w2-d5", ("هل تفهم؟", "أين تسكن؟", "ماذا تعمل؟", "كيف أصل إلى السوق؟"), ("أفهم السؤال وأستطيع الإجابة.", "أذهب إلى السوق ثم أعود إلى البيت."), "استخرج الأسئلة والمهارات التي تمت مراجعتها.", "نفّذ موقفًا نهائيًا يجمع سؤالًا شخصيًا وروتينًا واتجاهًا."),
)


def get_arabic_a1_content_seed(lesson_id: str) -> ArabicA1ContentSeed | None:
    return next((seed for seed in ARABIC_A1_CONTENT_SEEDS if seed.lesson_id == lesson_id), None)


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
    _lesson(5,2,1,"grammar","مراجعة الأعداد والموعد","استرجاع الأعداد والوقت ثم استخدام موعد في جملة جديدة.",("numbers","clock-time"),("numbers_time_a1","appointments_a1"),("time_a1",)),
    _lesson(5,2,2,"reading","جدول اليوم","قراءة جدول مواعيد واستخراج الأوقات الأساسية.",("clock-time","prepositions"),("numbers_time_a1","appointments_a1"),("time_a1",)),
    _lesson(5,2,3,"listening","تغيير الموعد","فهم طلب تغيير موعد ووقت جديد.",("clock-time","question-words"),("appointments_a1","numbers_time_a1"),("time_a1",)),
    _lesson(5,2,4,"review","مهمة المواعيد","إدارة حوار قصير لتحديد موعد وتأكيده أو تغييره.",("clock-time","question-words","prepositions"),("appointments_a1","numbers_time_a1"),("time_a1",)),
    _lesson(5,2,5,"review","اختبار الوقت","إثبات القدرة على السؤال عن الوقت وذكر موعد وفهمه.",("numbers","clock-time"),("numbers_time_a1","appointments_a1"),("time_a1",)),
    _lesson(6,2,1,"grammar","طلب مهذب","دمج الأمر والطلب مع مفردات الطعام والشراء.",("imperative-intro","accusative-intro"),("food_a1","shopping_a1"),("restaurant_a1","shopping_a1")),
    _lesson(6,2,2,"reading","قائمة وأسعار","قراءة قائمة بسيطة واستخراج الأطعمة والأسعار.",("quantifiers","accusative-intro"),("food_a1","shopping_a1"),("restaurant_a1","shopping_a1")),
    _lesson(6,2,3,"listening","حوار الشراء","فهم حوار عن منتج وسعر وكمية وطريقة الدفع.",("question-words","quantifiers"),("shopping_a1","food_a1"),("shopping_a1",)),
    _lesson(6,2,4,"review","مهمة المطعم والمتجر","تنفيذ موقفين قصيرين: طلب طعام ثم شراء منتج.",("imperative-intro","quantifiers","accusative-intro"),("food_a1","shopping_a1"),("restaurant_a1","shopping_a1")),
    _lesson(6,2,5,"review","اختبار الطعام والشراء","استرجاع اللغة اللازمة للطلب والسعر والكمية والدفع.",("question-words","quantifiers","accusative-intro"),("food_a1","shopping_a1"),("restaurant_a1","shopping_a1")),
    _lesson(7,2,1,"grammar","الأمر والاتجاهات","استخدام صيغة الأمر في تعليمات الطريق القصيرة.",("imperative-intro","place-expressions"),("directions_a1","places_a1"),("directions_a1",)),
    _lesson(7,2,2,"reading","خريطة بسيطة","قراءة وصف طريق وتحديد أماكن متتابعة.",("prepositions","place-expressions"),("places_a1","directions_a1"),("directions_a1",)),
    _lesson(7,2,3,"listening","تعليمات الطريق","فهم تعليمات من عدة خطوات دون فقد الاتجاه.",("imperative-intro","prepositions"),("directions_a1","places_a1"),("directions_a1",)),
    _lesson(7,2,4,"review","مهمة الاتجاهات","إعطاء طريق من نقطة البداية إلى وجهة باستخدام 4–5 تعليمات.",("imperative-intro","place-expressions","prepositions"),("directions_a1","places_a1"),("directions_a1",)),
    _lesson(7,2,5,"review","اختبار الأماكن","دمج الوجود وحروف الجر والأمر وتعبيرات المكان.",("there-is-there-are","imperative-intro","place-expressions"),("places_a1","directions_a1"),("directions_a1",)),
    _lesson(8,2,1,"grammar","المراجعة الذكية","استرجاع أكثر القواعد استعمالًا في A1 من خلال أسئلة متباعدة.",("pronouns","question-words","present-tense"),("review_a1","communication_a1"),("help_a1",)),
    _lesson(8,2,2,"reading","رسالة قصيرة","قراءة رسالة يومية قصيرة واستخراج المعلومات والأفعال الأساسية.",("present-tense","prepositions","adjectives"),("review_a1","communication_a1"),("help_a1",)),
    _lesson(8,2,3,"listening","محادثة A1 كاملة","فهم محادثة تجمع التعارف والروتين والمكان والطلب.",("question-words","present-tense","prepositions","negation"),("review_a1","communication_a1"),("help_a1",)),
    _lesson(8,2,4,"review","مهمة نهاية المستوى","حل سلسلة مواقف قصيرة دون تقديم قاعدة جديدة.",("pronouns","present-tense","prepositions","question-words"),("review_a1","communication_a1"),("help_a1",)),
    _lesson(8,2,5,"review","بوابة A2","مراجعة نهائية مركزة على المهارات التي يحتاجها المتعلم للانتقال إلى A2.",("pronouns","question-words","present-tense","negation"),("review_a1","communication_a1"),("help_a1",)),
)


def get_arabic_a1_lessons(unit_id: str | None = None) -> tuple[ArabicA1Lesson, ...]:
    """Return the full A1 sequence or only lessons belonging to one unit."""
    if unit_id is None:
        return ARABIC_A1_LESSONS
    return tuple(lesson for lesson in ARABIC_A1_LESSONS if lesson.unit_id == unit_id)


def validate_arabic_a1_content_quality() -> list[str]:
    """Return deterministic content-integrity issues for the complete A1 course map."""
    from app.data.ar.grammar import GRAMMAR_TOPICS
    from app.data.ar.vocabulary import VOCABULARY_SETS
    from app.data.ar.phrasebook import PHRASEBOOK_CATEGORIES

    issues: list[str] = []
    lessons = get_arabic_a1_lessons()
    lesson_ids = {lesson.id for lesson in lessons}
    seed_ids = [seed.lesson_id for seed in ARABIC_A1_CONTENT_SEEDS]

    if len(lessons) != 80:
        issues.append(f"expected 80 lessons, found {len(lessons)}")
    if len(seed_ids) != 80:
        issues.append(f"expected 80 seeds, found {len(seed_ids)}")
    if len(seed_ids) != len(set(seed_ids)):
        issues.append("duplicate content-seed lesson IDs")
    if set(seed_ids) != lesson_ids:
        issues.append("lesson/seed coverage mismatch")

    grammar_ids = {topic.slug for topic in GRAMMAR_TOPICS}
    vocabulary_ids = {item.id for item in VOCABULARY_SETS}
    phrasebook_ids = {item.id for item in PHRASEBOOK_CATEGORIES}

    for lesson in lessons:
        for slug in lesson.grammar_refs:
            if slug not in grammar_ids:
                issues.append(f"{lesson.id}: missing grammar ref {slug}")
        for vocab_id in lesson.vocabulary_set_ids:
            if vocab_id not in vocabulary_ids:
                issues.append(f"{lesson.id}: missing vocabulary set {vocab_id}")
        for phrase_id in lesson.phrasebook_ids:
            if phrase_id not in phrasebook_ids:
                issues.append(f"{lesson.id}: missing phrasebook category {phrase_id}")

    for seed in ARABIC_A1_CONTENT_SEEDS:
        if len(seed.target_phrases) < 4:
            issues.append(f"{seed.lesson_id}: fewer than 4 target phrases")
        if len(seed.model_sentences) < 2:
            issues.append(f"{seed.lesson_id}: fewer than 2 model sentences")
        if not seed.comprehension_prompt.strip():
            issues.append(f"{seed.lesson_id}: empty comprehension prompt")
        if not seed.production_prompt.strip():
            issues.append(f"{seed.lesson_id}: empty production prompt")

    return issues


def _normalize_arabic_lexeme(token: str) -> str:
    """Normalize common Arabic clitics and simple present-tense/person endings for grounding checks."""
    token = token.strip(" ،؛؟!,.\"'()[]{}:؛")
    if token.startswith("ال") and len(token) > 3:
        token = token[2:]
    for suffix in ("كما", "كم", "كن", "هما", "هم", "هن", "ها", "نا", "ني", "ك", "ه", "ي"):
        if token.endswith(suffix) and len(token) - len(suffix) >= 3:
            token = token[: -len(suffix)]
            break
    if token.endswith("ت") and len(token) >= 4:
        token = token[:-1] + "ة"
    for prefix in ("أ", "ن", "ت", "ي"):
        if token.startswith(prefix) and len(token) >= 4:
            token = token[1:]
            break
    for suffix in ("ون", "ين", "ان"):
        if token.endswith(suffix) and len(token) - len(suffix) >= 3:
            token = token[:-len(suffix)]
            break
    return token


def _seed_matches_vocab(text: str, lesson_words: set[str]) -> bool:
    normalized_words = {_normalize_arabic_lexeme(word) for word in lesson_words if word}
    tokens = [part for part in text.split() if part]
    return any(
        _normalize_arabic_lexeme(token) in normalized_words
        or any(word and word in token for word in lesson_words)
        for token in tokens
    )


def get_arabic_a1_content_quality_report() -> dict[str, object]:
    """Summarize lexical grounding and duplication without blocking valid course data."""
    from collections import Counter
    from app.data.ar.vocabulary import VOCABULARY_SETS

    vocab_by_id = {item.id: {word.word for word in item.words} for item in VOCABULARY_SETS}
    seed_by_id = {seed.lesson_id: seed for seed in ARABIC_A1_CONTENT_SEEDS}
    lexical_hits = 0
    lexical_total = 0
    signatures: Counter[tuple[tuple[str, ...], tuple[str, ...]]] = Counter()
    lesson_grounding: dict[str, float] = {}

    for lesson in get_arabic_a1_lessons():
        seed = seed_by_id[lesson.id]
        lesson_words = set().union(*(vocab_by_id.get(v, set()) for v in lesson.vocabulary_set_ids))
        searchable = seed.target_phrases + seed.model_sentences
        lesson_hits = sum(
            1 for text in searchable
            if _seed_matches_vocab(text, lesson_words)
        )
        lexical_total += len(searchable)
        lexical_hits += lesson_hits
        lesson_grounding[lesson.id] = round(lesson_hits / len(searchable), 3) if searchable else 0.0
        signatures[(seed.target_phrases, seed.model_sentences)] += 1

    duplicate_groups = sum(1 for count in signatures.values() if count > 1)
    duplicate_seed_lessons = sum(count for count in signatures.values() if count > 1)
    return {
        "lesson_count": len(get_arabic_a1_lessons()),
        "seed_count": len(ARABIC_A1_CONTENT_SEEDS),
        "lexical_grounding_ratio": round(lexical_hits / lexical_total, 3) if lexical_total else 0.0,
        "duplicate_seed_groups": duplicate_groups,
        "duplicate_seed_lessons": duplicate_seed_lessons,
        "fully_unique_seed_signatures": sum(1 for count in signatures.values() if count == 1),
        "lesson_grounding": lesson_grounding,
        "low_grounding_lessons": tuple(sorted(lesson_id for lesson_id, ratio in lesson_grounding.items() if ratio < 0.65)),
    }

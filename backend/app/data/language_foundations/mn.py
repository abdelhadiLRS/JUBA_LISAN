"""Mongolian A1-C2 foundation data for JUBA LISAN."""
from app.data._types import (
    AssessmentQuestion, CurriculumUnit, GrammarExample, GrammarTopic,
    PhrasebookCategory, PhrasebookEntry, VocabularyEntry, VocabularySet,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def g(slug, title, level, summary, examples, category="grammar"):
    return GrammarTopic(
        slug=slug, title=title, level=level, category=category,
        summary=summary, explanation=summary,
        examples=[GrammarExample(text=x) for x in examples],
    )


GRAMMAR_TOPICS = [
    g("pronouns", "Personal pronouns", "A1", "Use би, чи, тэр, бид and та in basic exchanges.", ["Би оюутан.", "Та багш байна."]),
    g("copula", "Nominal predicates and байна", "A1", "Identify people and things with nominal predicates and байна.", ["Би оюутан байна.", "Энэ бол ном."]),
    g("negation", "Negation with биш, үгүй and -гүй", "A1", "Form nominal, existential and verbal negatives.", ["Би багш биш.", "Надад мөнгө байхгүй."]),
    g("questions", "Question formation", "A1", "Ask information and yes/no questions with уу, вэ and question words.", ["Та хаана байна вэ?", "Энэ юу вэ?"]),
    g("possessive", "Possession and possessive suffixes", "A1", "Express ownership with genitive phrases and possessive forms.", ["Энэ миний ном.", "Болдын гэр том."]),
    g("case_core", "Core case suffixes", "A1", "Use nominative, genitive, dative-locative and accusative in familiar contexts.", ["Би сургуульд явна.", "Би номыг уншина."]),
    g("numbers", "Numbers, counters and quantity", "A1", "Use cardinal numbers and quantity expressions naturally.", ["Гурван хүн байна.", "Хоёр ном авлаа."]),
    g("time", "Time and dates", "A1", "Talk about days, clock time and simple schedules.", ["Өнөөдөр Даваа гараг.", "Маргааш найман цагт уулзъя."]),
    g("plural", "Plural suffixes", "A2", "Form common plural nouns with -ууд/-үүд and -нууд/-нүүд.", ["Оюутнууд хичээлдээ орлоо.", "Номууд ширээн дээр байна."]),
    g("present", "Present and habitual actions", "A2", "Describe current, habitual and general actions.", ["Би монгол хэл сурдаг.", "Тэр өдөр бүр ажилладаг."]),
    g("past", "Past tense and completed events", "A2", "Describe completed past events and personal experience.", ["Өчигдөр би ажилласан.", "Бид кино үзсэн."]),
    g("future", "Future and intention", "A2", "Express plans, predictions and intended actions.", ["Маргааш явна.", "Би энэ номыг уншина."]),
    g("progressive", "Progressive and ongoing events", "A2", "Describe actions in progress with natural Mongolian aspectual forms.", ["Би одоо ажиллаж байна.", "Тэд ярилцаж байна."]),
    g("comparatives", "Comparison and superlatives", "A2", "Compare people, objects and degrees of quality.", ["Энэ ном тэр номоос сонирхолтой.", "Хамгийн өндөр уул."]),
    g("imperative", "Imperatives and polite requests", "A2", "Give instructions and make polite requests.", ["Энд сууна уу.", "Дахин хэлнэ үү."]),
    g("case_extended", "Extended case system", "B1", "Use ablative, instrumental, comitative and directional case suffixes.", ["Улаанбаатараас ирсэн.", "Найзтайгаа явлаа."]),
    g("modality", "Ability, necessity and intention", "B1", "Express possibility, obligation, permission and intention.", ["Би явж чадна.", "Энд суух хэрэгтэй."]),
    g("conditional", "Conditional -вал/-вэл", "B1", "Build real and hypothetical conditions.", ["Завтай бол уулзъя.", "Хэрэв бороо орвол гэртээ байна."]),
    g("relative", "Participial relative clauses", "B1", "Modify nouns with participial forms and relative structures.", ["Өчигдөр ирсэн хүн бол миний багш.", "Унших номоо сонголоо."]),
    g("converbs", "Converbs and event sequencing", "B1", "Link events through converbal constructions.", ["Ажлаа дуусаад гэртээ харьсан.", "Инээж ярив."]),
    g("causal", "Cause, purpose and result", "B1", "Express reasons, purposes and consequences.", ["Бороо орсон учраас бид үлдсэн.", "Сурахын тулд номын санд очлоо."]),
    g("reported", "Reported speech", "B2", "Report statements, questions and requests with appropriate clause structures.", ["Тэр маргааш ирнэ гэж хэлсэн.", "Багш шалгалт болно гэсэн."]),
    g("passive", "Passive and causative constructions", "B2", "Use passive and causative morphology to change event perspective.", ["Номыг хэвлэсэн.", "Багш оюутнуудад дасгал хийлгэсэн."]),
    g("aspect", "Aspect, completion and event viewpoint", "B2", "Distinguish ongoing, habitual and completed events in discourse.", ["Би ном уншиж байсан.", "Тэр ажлаа дуусгасан."]),
    g("evidentiality", "Evidential and inferential meaning", "B2", "Signal information source, discovery and inference.", ["Тэр ирсэн бололтой.", "Гадаа цас орж байх шиг байна."]),
    g("concession", "Contrast and concession", "B2", "Connect opposing ideas with боловч, хэдий ч and related structures.", ["Хэдий орой болсон ч бид үргэлжлүүлэв.", "Завгүй боловч ирсэн."]),
    g("discourse", "Discourse connectors and cohesion", "B2", "Organize explanations using causal, contrastive and sequential markers.", ["Нэгдүгээрт, асуудлыг тодорхойлно. Дараа нь шийднэ."]),
    g("nominalization", "Nominalization", "C1", "Turn clauses and actions into abstract nouns for formal discourse.", ["Судалгааг хэрэгжүүлэх нь чухал.", "Шийдвэр гаргалтын үйл явц урт байсан."]),
    g("academic_hedging", "Academic stance and hedging", "C1", "Qualify claims with cautious, evidence-sensitive language.", ["Энэ үр дүнг цаашид нарийвчлан судлах шаардлагатай байж болох юм."]),
    g("subordination", "Complex subordination", "C1", "Build multi-clause sentences with embedded propositions and logical relations.", ["Хэрэв мэдээлэл баталгаажвал төслийг дараагийн шатанд шилжүүлнэ."]),
    g("embedded_questions", "Embedded questions", "C1", "Embed questions inside reports, requests and formal explanations.", ["Тэр хэзээ ирэхийг бид мэдэхгүй байна."]),
    g("information_structure", "Topic, focus and information structure", "C1", "Control emphasis and contrast through word order and discourse context.", ["Энэ асуудлыг бид өнөөдөр л хэлэлцэнэ."]),
    g("formal_register", "Formal and institutional Mongolian", "C1", "Adapt vocabulary and constructions for administration, policy and professional contexts.", ["Өргөдлийг хүлээн авч, холбогдох журмын дагуу шийдвэрлэнэ."]),
    g("argumentation", "Academic argumentation", "C1", "Present claims, evidence, counterarguments and conclusions coherently.", ["Энэхүү баримтад үндэслэн дараах дүгнэлтийг хийж болно."]),
    g("pragmatics", "Pragmatics and politeness", "C2", "Manage indirectness, respect, stance and social meaning.", ["Боломжтой бол энэ асуудлыг дахин авч үзэж болох уу?"]),
    g("rhetoric", "Rhetorical and literary style", "C2", "Recognize metaphor, parallelism, emphasis and stylistic variation.", ["Энэ санаа нь нийгмийн өөрчлөлтийн өргөн хүрээтэй холбоотой."]),
    g("translation", "Translation precision", "C2", "Choose Mongolian wording that preserves meaning, register and discourse function.", ["Нэр томьёог салбарын хэрэглээнд нийцүүлэн орчуулна."]),
    g("discourse_analysis", "Discourse analysis and register shifting", "C2", "Analyze cohesion, stance, genre and shifts between spoken and written registers.", ["Албан бичгийн хэл найруулга нь ярианы хэлээс ялгаатай."]),
]


def v(i, level, topic, words):
    return VocabularySet(
        id=i, level=level, topic=topic, unit_ref=i,
        words=[VocabularyEntry(word=w, pos=p, definition=d, example=e) for w, p, d, e in words],
    )


VOCABULARY_SETS = [
    v("greetings_a1", "A1", "Мэндчилгээ", [
        ("Сайн байна уу", "phrase", "hello", "Сайн байна уу!"), ("Баярлалаа", "phrase", "thank you", "Баярлалаа."),
        ("Баяртай", "phrase", "goodbye", "Баяртай!"), ("нэр", "noun", "name", "Миний нэр Болд.")
    ]),
    v("family_a1", "A1", "Гэр бүл", [
        ("ээж", "noun", "mother", "Миний ээж гэрт байна."), ("аав", "noun", "father", "Миний аав ажилладаг."),
        ("ах", "noun", "older brother", "Ах маань энд байна."), ("дүү", "noun", "younger sibling", "Дүү сургуульд явна.")
    ]),
    v("home_a1", "A1", "Гэр орон", [
        ("гэр", "noun", "home", "Миний гэр том."), ("өрөө", "noun", "room", "Өрөө цэвэрхэн байна."),
        ("ширээ", "noun", "table", "Ном ширээн дээр байна."), ("хаалга", "noun", "door", "Хаалга нээлттэй байна.")
    ]),
    v("daily_a1", "A1", "Өдөр тутмын амьдрал", [
        ("өглөө", "noun", "morning", "Өглөө би ажиллана."), ("ажиллах", "verb", "work", "Би ажиллана."),
        ("явах", "verb", "go", "Би сургууль явна."), ("унтах", "verb", "sleep", "Би орой унтана.")
    ]),
    v("food_a1", "A1", "Хоол ба худалдаа", [
        ("ус", "noun", "water", "Би ус ууна."), ("талх", "noun", "bread", "Би талх авна."),
        ("цай", "noun", "tea", "Би цай ууна."), ("үнэ", "noun", "price", "Энэ хэдэн төгрөг вэ?")
    ]),
    v("places_a1", "A1", "Газар ба чиглэл", [
        ("дэлгүүр", "noun", "shop", "Дэлгүүр ойрхон байна."), ("сургууль", "noun", "school", "Сургууль энд байна."),
        ("баруун", "noun", "right", "Баруун тийш яв."), ("зүүн", "noun", "left", "Зүүн тийш яв.")
    ]),
    v("communication_a1", "A1", "Харилцаа", [
        ("туслах", "verb", "help", "Надад туслаач."), ("ойлгох", "verb", "understand", "Би ойлгохгүй байна."),
        ("дахин", "adverb", "again", "Дахин хэлнэ үү."), ("гуйя", "phrase", "please", "Гуйя, дахин хэлнэ үү.")
    ]),
    v("people_a2", "A2", "Хүмүүс ба харилцаа", [
        ("найз", "noun", "friend", "Тэр миний сайн найз."), ("хөрш", "noun", "neighbor", "Манай хөрш их найрсаг."),
        ("хамт олон", "noun", "colleagues", "Хамт олон маань тусалсан."), ("зочин", "noun", "guest", "Өнөөдөр зочин ирнэ.")
    ]),
    v("travel_a2", "A2", "Аялал", [
        ("онгоц", "noun", "airplane", "Онгоц өглөө ниснэ."), ("галт тэрэг", "noun", "train", "Галт тэрэг хөдөллөө."),
        ("буудал", "noun", "hotel/stop", "Бид буудалд бууна."), ("тасалбар", "noun", "ticket", "Тасалбар хаанаас авах вэ?")
    ]),
    v("health_a2", "A2", "Эрүүл мэнд", [
        ("эмч", "noun", "doctor", "Эмч үзлэг хийж байна."), ("өвдөх", "verb", "hurt/be ill", "Толгой өвдөж байна."),
        ("эм", "noun", "medicine", "Эмээ цагт нь ууна."), ("эмнэлэг", "noun", "hospital", "Эмнэлэг ойрхон байна.")
    ]),
    v("study_b1", "B1", "Сургууль ба суралцахуй", [
        ("судлах", "verb", "study/research", "Би хэл шинжлэл судалдаг."), ("даалгавар", "noun", "assignment", "Даалгавраа дуусгалаа."),
        ("шалгалт", "noun", "exam", "Шалгалт маргааш болно."), ("хичээл", "noun", "lesson", "Хичээл сонирхолтой байна.")
    ]),
    v("work_b1", "B1", "Ажил ба карьер", [
        ("ажилтан", "noun", "employee", "Ажилтан тайлангаа илгээв."), ("уулзалт", "noun", "meeting", "Уулзалт гурван цагт эхэлнэ."),
        ("туршлага", "noun", "experience", "Тэр их туршлагатай."), ("үүрэг", "noun", "responsibility", "Энэ бол миний үндсэн үүрэг.")
    ]),
    v("society_b2", "B2", "Нийгэм", [
        ("нийгэм", "noun", "society", "Нийгэм хурдан өөрчлөгдөж байна."), ("хөгжил", "noun", "development", "Тогтвортой хөгжил чухал."),
        ("бодлого", "noun", "policy", "Шинэ бодлого хэрэгжиж эхэллээ."), ("иргэн", "noun", "citizen", "Иргэн эрхээ мэдэх хэрэгтэй.")
    ]),
    v("economy_b2", "B2", "Эдийн засаг", [
        ("эдийн засаг", "noun", "economy", "Эдийн засгийн өсөлт хэлэлцэгдэв."), ("зах зээл", "noun", "market", "Зах зээлийн эрэлт өссөн."),
        ("хөрөнгө оруулалт", "noun", "investment", "Хөрөнгө оруулалт нэмэгдэв."), ("орлого", "noun", "income", "Өрхийн орлого өсжээ.")
    ]),
    v("media_c1", "C1", "Хэвлэл мэдээлэл", [
        ("мэдээлэл", "noun", "information", "Мэдээллийг шалгах шаардлагатай."), ("нийтлэл", "noun", "article", "Нийтлэлд шинэ баримт дурджээ."),
        ("сурвалж", "noun", "source", "Эх сурвалжийг тодорхой заасан."), ("ярилцлага", "noun", "interview", "Тэр ярилцлага өгсөн.")
    ]),
    v("academic_c1", "C1", "Академик хэл", [
        ("судалгаа", "noun", "research", "Судалгааны үр дүн сонирхолтой."), ("нотолгоо", "noun", "evidence", "Нотолгоо хангалттай байна."),
        ("таамаглал", "noun", "hypothesis", "Таамаглалыг шалгав."), ("дүгнэлт", "noun", "conclusion", "Дүгнэлтэд үндэслэл өгсөн.")
    ]),
    v("institutional_c1", "C1", "Албан ба захиргааны хэл", [
        ("журам", "noun", "regulation", "Журмын дагуу шийдвэрлэнэ."), ("өргөдөл", "noun", "application", "Өргөдлийг хүлээн авлаа."),
        ("шийдвэр", "noun", "decision", "Шийдвэр албан ёсоор гарсан."), ("хэрэгжилт", "noun", "implementation", "Хэрэгжилтийг хянаж байна.")
    ]),
    v("culture_c2", "C2", "Соёл ба уран зохиол", [
        ("өв", "noun", "heritage", "Соёлын өвийг хамгаална."), ("уран зохиол", "noun", "literature", "Монголын уран зохиол баялаг."),
        ("дүрслэл", "noun", "imagery", "Зохиолч хүчтэй дүрслэл ашигласан."), ("бэлгэдэл", "noun", "symbolism", "Бэлгэдлийн утгыг тайлбарлав.")
    ]),
    v("discourse_c2", "C2", "Дискурс ба хэл найруулга", [
        ("найруулга", "noun", "style", "Албан бичгийн найруулга тодорхой байна."), ("өнгө аяс", "noun", "tone", "Өгүүлбэрийн өнгө аясыг анхаарна."),
        ("далд утга", "noun", "implicit meaning", "Далд утгыг контекстоор ойлгоно."), ("нэр томьёо", "noun", "terminology", "Нэр томьёог нэг мөр хэрэглэв.")
    ]),
]


def p(i, level, situation, items, register="neutral"):
    return PhrasebookCategory(
        id=i, level=level, situation=situation, icon="💬",
        phrases=[PhrasebookEntry(text=t, context=c, register=register) for t, c in items],
    )


PHRASEBOOK_CATEGORIES = [
    p("greetings_a1", "A1", "Greetings", [("Сайн байна уу!", "formal greeting"), ("Сайн уу?", "informal greeting"), ("Миний нэр Болд.", "introducing yourself")]),
    p("thanks_a1", "A1", "Thanks and apologies", [("Баярлалаа.", "thanks"), ("Уучлаарай.", "apology"), ("Зүгээр ээ.", "responding politely")]),
    p("shopping_a1", "A1", "Shopping", [("Энэ хэдэн төгрөг вэ?", "asking price"), ("Энийг авъя.", "requesting an item"), ("Өөр өнгө байна уу?", "asking for another option")]),
    p("directions_a1", "A1", "Directions", [("Дэлгүүр хаана байна?", "asking location"), ("Сургууль руу яаж явах вэ?", "asking route"), ("Баруун тийш явна уу.", "giving directions")]),
    p("help_a1", "A1", "Help and clarification", [("Надад туслаач.", "asking for help"), ("Би ойлгохгүй байна.", "saying you do not understand"), ("Дахин хэлнэ үү.", "asking for repetition")]),
    p("travel_a2", "A2", "Travel", [("Тасалбар хаанаас авах вэ?", "buying a ticket"), ("Буух буудал аль вэ?", "asking where to get off"), ("Би захиалгаа баталгаажуулъя.", "confirming a booking")]),
    p("health_a2", "A2", "Health", [("Толгой өвдөж байна.", "describing a symptom"), ("Эмчтэй уулзмаар байна.", "requesting medical help"), ("Энэ эмийг яаж хэрэглэх вэ?", "asking about medicine")]),
    p("study_b1", "B1", "Study", [("Энэ санааг тайлбарлаж өгнө үү.", "asking for explanation"), ("Даалгавраа хугацаанд нь өгнө.", "discussing an assignment"), ("Би энэ эх сурвалжийг ашигласан.", "citing a source")]),
    p("work_b1", "B1", "Work", [("Уулзалтыг эхэлье.", "starting a meeting"), ("Энэ асуудлыг хэлэлцье.", "opening discussion"), ("Тайланг маргааш илгээнэ.", "work commitment")]),
    p("society_b2", "B2", "Public discussion", [("Энэ асуудалд хэд хэдэн хүчин зүйл нөлөөлж байна.", "explaining causes"), ("Нөгөө талаас авч үзвэл...", "introducing contrast"), ("Баримтад үндэслэн...", "introducing evidence")], "formal"),
    p("academic_c1", "C1", "Academic discussion", [("Энэхүү судалгаа нь ... харуулж байна.", "stating a finding"), ("Энэ дүгнэлтийг болгоомжтой тайлбарлах хэрэгтэй.", "hedging"), ("Үүнийг цаашид судлах шаардлагатай.", "proposing further research")], "academic"),
    p("institutional_c1", "C1", "Institutional communication", [("Өргөдлийг хүлээн авлаа.", "acknowledging an application"), ("Журмын дагуу шийдвэрлэнэ.", "formal procedure"), ("Холбогдох мэдээллийг ирүүлнэ үү.", "formal request")], "formal"),
    p("rhetoric_c2", "C2", "Rhetorical and nuanced speech", [("Энд анхаарах нэг чухал зүйл бий.", "foregrounding a point"), ("Энэ тайлбар хангалттай үндэслэлтэй эсэхийг авч үзье.", "critical evaluation"), ("Үүний цаана өөр нэг утга агуулагдаж болно.", "interpreting implicit meaning")], "formal"),
]


def u(level, number, title, grammar, vocab, a, b):
    return CurriculumUnit(
        id=f"mn-{level.lower()}-{number:02}",
        level=level, unit_number=number, title=title,
        grammar_points=grammar, vocabulary_set_ids=[vocab],
        lesson_types=["grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"],
        competency_checklist=[a, b], default_weeks=2,
    )


CURRICULUM = {
    "A1": [
        u("A1", 1, "Мэндчилгээ ба танилцах", ["pronouns", "copula"], "greetings_a1", "Өөрийгөө танилцуулна", "Мэндчилгээ солилцоно"),
        u("A1", 2, "Гэр бүл", ["possessive", "pronouns"], "family_a1", "Гэр бүлийнхээ тухай ярилцана", "Эзэмшлийг илэрхийлнэ"),
        u("A1", 3, "Гэр орон", ["case_core", "possessive"], "home_a1", "Гэрээ дүрслэнэ", "Зүйлийн байршил хэлнэ"),
        u("A1", 4, "Өдөр тутмын амьдрал", ["present", "negation"], "daily_a1", "Өдөр тутмын үйлдлээ ярьна", "Үгүйсгэсэн өгүүлбэр зохионо"),
        u("A1", 5, "Хоол ба худалдаа", ["questions", "numbers"], "food_a1", "Хоол хүнс худалдаж авна", "Үнэ асууна"),
        u("A1", 6, "Газар ба чиглэл", ["case_core", "questions"], "places_a1", "Байршил асууна", "Чиглэл өгнө"),
        u("A1", 7, "Харилцаа ба тусламж", ["negation", "questions"], "communication_a1", "Ойлгоогүй зүйлээ тодруулна", "Тусламж хүснэ"),
        u("A1", 8, "A1 давтлага", ["time", "numbers"], "greetings_a1", "Танил сэдвээр ярилцана", "Анхан шатны харилцан яриа өрнүүлнэ"),
    ],
    "A2": [
        u("A2", 1, "Хүмүүс ба харилцаа", ["plural", "present"], "people_a2", "Хүмүүсийг дүрслэнэ", "Дадал зуршлаа ярьна"),
        u("A2", 2, "Аялал", ["past", "future"], "travel_a2", "Өнгөрсөн аяллаа ярьна", "Аяллын төлөвлөгөө хэлнэ"),
        u("A2", 3, "Эрүүл мэнд", ["progressive", "imperative"], "health_a2", "Шинж тэмдэг тайлбарлана", "Эелдгээр хүсэлт гаргана"),
        u("A2", 4, "Цаг хугацаа ба төлөвлөгөө", ["future", "time"], "daily_a1", "Төлөвлөгөө гаргана", "Хуваарь ярилцана"),
        u("A2", 5, "Харьцуулалт", ["comparatives", "plural"], "home_a1", "Зүйлийг харьцуулна", "Хэмжээ, чанарыг тайлбарлана"),
        u("A2", 6, "Эелдэг харилцаа", ["imperative", "questions"], "communication_a1", "Эелдгээр хүсэлт гаргана", "Тодруулга асууна"),
        u("A2", 7, "Хот ба үйлчилгээ", ["case_extended", "questions"], "places_a1", "Үйлчилгээний газар чиглүүлнэ", "Зам, байршил тайлбарлана"),
        u("A2", 8, "A2 давтлага", ["past", "future"], "travel_a2", "Өнгөрсөн ба ирээдүйг ялган ярьна", "Аяллын нөхцөлд харилцана"),
    ],
    "B1": [
        u("B1", 1, "Суралцахуй", ["case_extended", "modality"], "study_b1", "Суралцах үйл явцаа тайлбарлана", "Зөвлөгөө өгнө"),
        u("B1", 2, "Ажил ба карьер", ["modality", "conditional"], "work_b1", "Ажлын үүргээ тайлбарлана", "Нөхцөлт санал гаргана"),
        u("B1", 3, "Шалтгаан ба зорилго", ["causal", "converbs"], "society_b2", "Шалтгаан тайлбарлана", "Зорилго илэрхийлнэ"),
        u("B1", 4, "Нөхцөл ба төлөвлөгөө", ["conditional", "future"], "travel_a2", "Нөхцөлт төлөвлөгөө гаргана", "Боломжит үр дүнг хэлнэ"),
        u("B1", 5, "Хамаатуулах бүтэц", ["relative", "case_extended"], "study_b1", "Нэр үгийг дэлгэрүүлнэ", "Нарийн мэдээлэл өгнө"),
        u("B1", 6, "Үйл явдлын дараалал", ["converbs", "aspect"], "daily_a1", "Үйл явдлыг дараалуулна", "Үйл явцын явцыг тайлбарлана"),
        u("B1", 7, "Асуудал шийдвэрлэх", ["causal", "modality"], "work_b1", "Шалтгаан ба шийдэл хэлнэ", "Зөвлөгөө, шаардлага илэрхийлнэ"),
        u("B1", 8, "B1 давтлага", ["relative", "conditional"], "study_b1", "Нийлмэл өгүүлбэр хэрэглэнэ", "Сургууль, ажил сэдвээр ярилцана"),
    ],
    "B2": [
        u("B2", 1, "Дам яриа", ["reported", "subordination"], "media_c1", "Бусдын санааг дамжуулна", "Эх сурвалжийг ялгана"),
        u("B2", 2, "Идэвх ба хэв", ["passive", "aspect"], "institutional_c1", "Үйл явдлын төвийг өөрчилнө", "Гүйцсэн, үргэлжилсэн үйлдлийг ялгана"),
        u("B2", 3, "Нотолгоо ба таамаг", ["evidentiality", "modality"], "academic_c1", "Нотолгооны түвшинг илэрхийлнэ", "Таамаглалаа болгоомжтой хэлнэ"),
        u("B2", 4, "Эсрэгцэл ба буулт", ["concession", "discourse"], "society_b2", "Эсрэг санаа холбоно", "Буулттай тайлбар өгнө"),
        u("B2", 5, "Эдийн засаг", ["reported", "causal"], "economy_b2", "Эдийн засгийн мэдээлэл тайлбарлана", "Шалтгаан-үр дагаврыг холбоно"),
        u("B2", 6, "Нийгмийн асуудал", ["discourse", "concession"], "society_b2", "Олон талт асуудлыг хэлэлцэнэ", "Эсрэг байр суурийг танилцуулна"),
        u("B2", 7, "Хэвлэл мэдээллийн эх", ["reported", "evidentiality"], "media_c1", "Мэдээллийн эх сурвалжийг тайлбарлана", "Баримт ба таамгийг ялгана"),
        u("B2", 8, "B2 давтлага", ["passive", "discourse"], "media_c1", "Нарийн мэдээллийг нэгтгэнэ", "Урт тайлбар зохионо"),
    ],
    "C1": [
        u("C1", 1, "Нэршүүлэлт ба албан хэл", ["nominalization", "formal_register"], "institutional_c1", "Албан найруулгаар бичнэ", "Үйл явцыг нэршүүлнэ"),
        u("C1", 2, "Академик болгоомжлол", ["academic_hedging", "evidentiality"], "academic_c1", "Баталгааны түвшинг ялгана", "Болгоомжтой дүгнэлт гаргана"),
        u("C1", 3, "Нийлмэл дэд өгүүлбэр", ["subordination", "embedded_questions"], "academic_c1", "Нийлмэл санаа бүтээнэ", "Далд асуулт хэрэглэнэ"),
        u("C1", 4, "Сэдэв ба онцлол", ["information_structure", "discourse"], "discourse_c2", "Онцлох мэдээллээ зохион байгуулна", "Контекстэд нийцүүлэн үгсийн дараалал сонгоно"),
        u("C1", 5, "Байгууллагын харилцаа", ["formal_register", "nominalization"], "institutional_c1", "Албан бичгийн хэл хэрэглэнэ", "Процедур тайлбарлана"),
        u("C1", 6, "Академик аргумент", ["argumentation", "academic_hedging"], "academic_c1", "Нотолгоонд тулгуурласан аргумент бичнэ", "Эсрэг санааг авч үзнэ"),
        u("C1", 7, "Хэвлэл ба бодлогын хэл", ["information_structure", "formal_register"], "media_c1", "Нийтийн мэдээллийг задлан шинжилнэ", "Албан өнгө аясыг тохируулна"),
        u("C1", 8, "C1 давтлага", ["subordination", "argumentation"], "academic_c1", "Урт академик тайлбар бичнэ", "Нарийн санааг уялдуулна"),
    ],
    "C2": [
        u("C2", 1, "Прагматик утга", ["pragmatics", "information_structure"], "discourse_c2", "Шууд ба далд утгыг ялгана", "Эелдэг бус байдлыг багасгана"),
        u("C2", 2, "Уран илтгэлийн хэл", ["rhetoric", "discourse_analysis"], "culture_c2", "Риторик арга хэрэглэнэ", "Уран дүрслэлийг тайлбарлана"),
        u("C2", 3, "Орчуулгын нарийвчлал", ["translation", "pragmatics"], "discourse_c2", "Утга ба өнгө аясыг хадгална", "Нэр томьёог контекстоор сонгоно"),
        u("C2", 4, "Дискурсын шинжилгээ", ["discourse_analysis", "information_structure"], "discourse_c2", "Жанр ба регистрийг шинжилнэ", "Дискурсын уялдааг тайлбарлана"),
        u("C2", 5, "Уран зохиолын регистр", ["rhetoric", "translation"], "culture_c2", "Уран зохиолын хэл найруулгыг танина", "Дүрслэлийн сонголтыг тайлбарлана"),
        u("C2", 6, "Мэргэжлийн өндөр түвшний хэл", ["formal_register", "pragmatics"], "institutional_c1", "Мэргэжлийн нарийн санаа илэрхийлнэ", "Соёлын нөхцөлд эелдэг байдлыг тохируулна"),
        u("C2", 7, "Олон эх сурвалжийн нэгтгэл", ["argumentation", "discourse_analysis"], "media_c1", "Олон эх сурвалжийг нэгтгэнэ", "Зөрүүтэй нотолгоог харьцуулна"),
        u("C2", 8, "C2 нэгдсэн үнэлгээ", ["translation", "rhetoric"], "academic_c1", "Нарийн академик эсээ бичнэ", "Хэл найруулгаа зорилгод нийцүүлнэ"),
    ],
}


ASSESSMENT_BANK = [
    AssessmentQuestion(id=f"mn-{i:03}", skill=skill, difficulty=level, question=q, options=opts, correct=correct)
    for i, (level, skill, q, opts, correct) in enumerate([
        ("A1", "vocabulary", "What does Сайн байна уу mean?", ["hello", "goodbye", "water", "school"], "hello"),
        ("A1", "grammar", "Which means 'I am not a teacher'?", ["Би багш биш.", "Би багш байна.", "Тэр багш.", "Би оюутан."], "Би багш биш."),
        ("A1", "vocabulary", "What does ээж mean?", ["mother", "father", "friend", "teacher"], "mother"),
        ("A2", "grammar", "Which sentence describes a completed past action?", ["Өчигдөр би ажилласан.", "Маргааш би ажиллана.", "Би ажиллаж байна.", "Би ажиллахгүй."], "Өчигдөр би ажилласан."),
        ("A2", "vocabulary", "What does тасалбар mean?", ["ticket", "medicine", "meeting", "source"], "ticket"),
        ("B1", "grammar", "Which form expresses a condition?", ["Хэрэв бороо орвол...", "Би ажилласан.", "Энэ ном байна.", "Би уншиж байна."], "Хэрэв бороо орвол..."),
        ("B1", "grammar", "What does -хын тулд typically express?", ["purpose", "comparison", "ownership", "location"], "purpose"),
        ("B2", "grammar", "Which introduces reported speech?", ["гэж хэлсэн", "хамгийн", "руу", "байна уу"], "гэж хэлсэн"),
        ("B2", "vocabulary", "What does нотолгоо mean?", ["evidence", "holiday", "neighbor", "ticket"], "evidence"),
        ("C1", "academic", "Which phrase is an academic hedge?", ["байж болох юм", "яг одоо", "Сайн уу", "Баяртай"], "байж болох юм"),
        ("C1", "formal", "Which phrase is formal institutional language?", ["Журмын дагуу шийдвэрлэнэ.", "Сайн уу?", "Энийг авъя.", "Баяртай!"], "Журмын дагуу шийдвэрлэнэ."),
        ("C2", "discourse", "What should a translator preserve besides basic meaning?", ["meaning, register and discourse function", "word count only", "punctuation only", "literal word order only"], "meaning, register and discourse function"),
    ], 1)
]

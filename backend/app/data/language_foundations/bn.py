"""Bengali A1-C2 foundation data for JUBA LISAN."""
from app.data._types import (
    AssessmentQuestion, CurriculumUnit, GrammarExample, GrammarTopic,
    PhrasebookCategory, PhrasebookEntry, VocabularyEntry, VocabularySet,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def g(slug, title, level, summary, examples):
    return GrammarTopic(
        slug=slug, title=title, level=level, category="grammar",
        summary=summary, explanation=summary,
        examples=[GrammarExample(text=x) for x in examples],
    )


GRAMMAR_TOPICS = [
    g("pronouns", "Personal pronouns", "A1", "Use আমি, তুমি, আপনি, সে and আমরা in everyday exchanges.", ["আমি ছাত্র।", "আপনি শিক্ষক।"]),
    g("copula", "Identity and noun sentences", "A1", "Build present identity sentences and distinguish nominal predicates.", ["আমি ছাত্র।", "এটা বই।"]),
    g("demonstratives", "Demonstratives", "A1", "Use এই, ওই and সেই with familiar nouns.", ["এই বইটি নতুন।", "ওই বাড়িটি বড়।"]),
    g("questions", "Question words", "A1", "Ask what, who, where, when and how much.", ["এটা কী?", "আপনি কোথায় থাকেন?"]),
    g("present", "Present habitual forms", "A1", "Describe routines and current facts with common verb forms.", ["আমি বাংলা পড়ি।", "সে কাজ করে।"]),
    g("negation", "Negation with না and নয়", "A1", "Negate verbal and nominal clauses.", ["আমি যাই না।", "এটা বই নয়।"]),
    g("plural", "Plural and classifiers", "A2", "Use -রা, -গুলো and common measure expressions.", ["ছাত্ররা আসে।", "তিনটি বই আছে।"]),
    g("postpositions", "Postpositions and location", "A2", "Use case-like suffixes and postpositions for place and relations.", ["আমি বাড়িতে আছি।", "বন্ধুর সঙ্গে যাই।"]),
    g("past", "Simple past", "A2", "Describe completed events and experiences.", ["আমি গতকাল ঢাকায় গিয়েছিলাম।", "সে বইটি পড়ল।"]),
    g("future", "Future and intention", "A2", "Express plans, predictions and intentions.", ["আমি কাল যাব।", "সে আগামীকাল আসবে।"]),
    g("progressive", "Progressive aspect", "A2", "Describe actions in progress with -ছি forms.", ["আমি বই পড়ছি।", "তারা কাজ করছে।"]),
    g("perfect", "Perfect and resultative meaning", "A2", "Connect completed actions with present relevance.", ["আমি কাজটি শেষ করেছি।", "সে চলে গেছে।"]),
    g("imperative", "Imperatives and polite requests", "A2", "Give instructions and make polite requests.", ["দয়া করে বসুন।", "আবার বলুন।"]),
    g("comparatives", "Comparison", "A2", "Compare qualities and quantities.", ["এই বইটি ওটার চেয়ে ভালো।", "এটাই সবচেয়ে বড়।"]),
    g("case_marking", "Object and oblique marking", "B1", "Use -কে, -র/-এর and other markers with appropriate noun roles.", ["আমি রাহুলকে দেখেছি।", "রাহুলের বইটি নতুন।"]),
    g("honorifics", "Honorific agreement and register", "B1", "Choose respectful pronouns and verb forms.", ["আপনি কেমন আছেন?", "তিনি আজ আসবেন।"]),
    g("modality", "Ability, necessity and intention", "B1", "Express ability, obligation, permission and desire.", ["আমি যেতে পারি।", "আমাকে কাজটি করতে হবে।"]),
    g("conditional", "Conditional clauses", "B1", "Express real and hypothetical conditions with যদি and -লে.", ["যদি বৃষ্টি হয়, আমরা যাব না।", "সময় পেলে দেখা করব।"]),
    g("relative", "Relative-correlative clauses", "B1", "Build Bengali relative-correlative patterns with যে/যে...সে.", ["যে মানুষটি এসেছেন, তিনি আমার শিক্ষক।"]),
    g("conjunctive_participle", "Conjunctive participles", "B1", "Sequence actions with -ে and related non-finite forms.", ["খেয়ে আমি কাজে গেলাম।", "হেসে সে উত্তর দিল।"]),
    g("causal_purpose", "Cause, purpose and result", "B1", "Connect reasons, purposes and consequences.", ["বৃষ্টি হওয়ায় আমরা বাড়িতে রইলাম।", "শেখার জন্য সে বই কিনল।"]),
    g("reported", "Reported speech", "B2", "Report statements, questions and beliefs with যে and related structures.", ["সে বলল যে কাল আসবে।", "তিনি জিজ্ঞেস করলেন কখন যাব।"]),
    g("passive", "Passive constructions", "B2", "Shift focus from an agent to an affected participant.", ["চিঠিটি লেখা হয়েছে।", "সিদ্ধান্তটি নেওয়া হয়েছিল।"]),
    g("causative", "Causative constructions", "B2", "Express making or arranging someone to perform an action.", ["শিক্ষক ছাত্রদের দিয়ে কাজটি করালেন।"]),
    g("aspect", "Aspect and event viewpoint", "B2", "Contrast habitual, progressive, perfect and completed events.", ["সে প্রতিদিন পড়ে।", "সে এখন পড়ছে।"]),
    g("concession", "Contrast and concession", "B2", "Connect opposing claims with কিন্তু, যদিও and তবুও.", ["যদিও কঠিন, তবুও কাজটি সম্ভব।"]),
    g("discourse", "Discourse connectors", "B2", "Organize arguments with causal, sequential and contrastive markers.", ["প্রথমত, তথ্যটি যাচাই করতে হবে। তারপর সিদ্ধান্ত নেওয়া হবে।"]),
    g("nominalization", "Nominalization", "C1", "Turn actions and clauses into abstract nouns for formal prose.", ["পরিকল্পনার বাস্তবায়ন জরুরি।", "সিদ্ধান্ত গ্রহণের প্রক্রিয়া দীর্ঘ ছিল।"]),
    g("hedging", "Academic hedging and stance", "C1", "Qualify claims and distinguish evidence from interpretation.", ["এই ফলাফল আরও গবেষণার প্রয়োজন নির্দেশ করতে পারে।"]),
    g("subordination", "Complex subordination", "C1", "Build multi-clause sentences with embedded logical relations.", ["যদি তথ্যটি নিশ্চিত হয়, তাহলে প্রকল্পটি পরবর্তী পর্যায়ে যাবে।"]),
    g("embedded_questions", "Embedded questions", "C1", "Embed questions in formal reports and explanations.", ["আমরা জানি না তিনি কখন আসবেন।"]),
    g("information_structure", "Topic, focus and emphasis", "C1", "Manage information flow through particles, order and discourse context.", ["এই বিষয়টিই আমরা আজ আলোচনা করব।"]),
    g("formal_register", "Formal and institutional Bengali", "C1", "Adapt language for administration, policy and professional contexts.", ["আবেদনটি বিধি অনুযায়ী বিবেচনা করা হবে।"]),
    g("argumentation", "Academic argumentation", "C1", "Present claims, evidence, counterarguments and conclusions.", ["উপলব্ধ তথ্যের ভিত্তিতে এই সিদ্ধান্তে পৌঁছানো যায়।"]),
    g("pragmatics", "Pragmatics and politeness", "C2", "Manage indirectness, social distance and implied meaning.", ["সম্ভব হলে বিষয়টি আরেকবার বিবেচনা করবেন কি?"]),
    g("rhetoric", "Rhetorical and literary style", "C2", "Interpret metaphor, parallelism, emphasis and stylistic variation.", ["এই বক্তব্যে রূপকের মাধ্যমে সামাজিক পরিবর্তনকে তুলে ধরা হয়েছে।"]),
    g("translation", "Translation precision", "C2", "Preserve meaning, register and discourse function across languages.", ["পরিভাষাটি প্রেক্ষাপট অনুযায়ী অনুবাদ করতে হবে।"]),
    g("discourse_analysis", "Discourse analysis and register shifting", "C2", "Analyze genre, cohesion, stance and shifts between spoken and written Bengali.", ["প্রাতিষ্ঠানিক ভাষার রীতি কথ্য ভাষা থেকে আলাদা।"]),
]


def v(i, level, topic, words):
    return VocabularySet(
        id=i, level=level, topic=topic, unit_ref=i,
        words=[VocabularyEntry(word=w, pos=p, definition=d, example=e) for w, p, d, e in words],
    )


VOCABULARY_SETS = [
    v("greetings_a1", "A1", "Greetings", [("নমস্কার", "phrase", "hello", "নমস্কার!"), ("ধন্যবাদ", "phrase", "thank you", "ধন্যবাদ।"), ("বিদায়", "phrase", "goodbye", "বিদায়!"), ("নাম", "noun", "name", "আমার নাম রাহুল।")]),
    v("family_a1", "A1", "Family", [("মা", "noun", "mother", "আমার মা বাড়িতে আছেন।"), ("বাবা", "noun", "father", "আমার বাবা কাজ করেন।"), ("ভাই", "noun", "brother", "আমার ভাই ছাত্র।"), ("বোন", "noun", "sister", "আমার বোন স্কুলে যায়।")]),
    v("home_a1", "A1", "Home", [("বাড়ি", "noun", "home", "আমার বাড়ি ঢাকায়।"), ("ঘর", "noun", "room", "ঘরটি পরিষ্কার।"), ("টেবিল", "noun", "table", "বইটি টেবিলে আছে।"), ("দরজা", "noun", "door", "দরজা খোলা।")]),
    v("daily_a1", "A1", "Daily life", [("সকাল", "noun", "morning", "সকালে আমি কাজ করি।"), ("কাজ করা", "verb", "to work", "আমি প্রতিদিন কাজ করি।"), ("পড়া", "verb", "to study/read", "আমি রাতে পড়ি।"), ("ঘুমানো", "verb", "to sleep", "আমি রাতে ঘুমাই।")]),
    v("food_a1", "A1", "Food", [("জল", "noun", "water", "আমি জল চাই।"), ("ভাত", "noun", "rice", "আমি ভাত খাই।"), ("চা", "noun", "tea", "আমি চা পান করি।"), ("দাম", "noun", "price", "এটার দাম কত?")]),
    v("places_a1", "A1", "Places", [("রাস্তা", "noun", "street", "এই রাস্তা কোথায় যায়?"), ("স্টেশন", "noun", "station", "স্টেশন কোথায়?"), ("ডান", "noun", "right", "ডান দিকে যান।"), ("বাম", "noun", "left", "বাম দিকে যান।")]),
    v("communication_a1", "A1", "Communication", [("সাহায্য", "noun", "help", "আমার সাহায্য দরকার।"), ("দয়া করে", "phrase", "please", "দয়া করে আবার বলুন।"), ("বোঝা", "verb", "understand", "আমি বুঝতে পারছি না।"), ("আবার", "adverb", "again", "দয়া করে আবার বলুন।")]),
    v("review_a1", "A1", "Review", [("আজ", "adverb", "today", "আজ আমি বাড়িতে আছি।"), ("কাল", "adverb", "tomorrow", "কাল আমি স্কুলে যাব।"), ("বন্ধু", "noun", "friend", "সে আমার বন্ধু।"), ("সময়", "noun", "time", "আমার সময় আছে।")]),
    v("travel_a2", "A2", "Travel", [("টিকিট", "noun", "ticket", "একটি টিকিট চাই।"), ("বিমান", "noun", "airplane", "বিমান সকাল আটটায় ছাড়ে।"), ("হোটেল", "noun", "hotel", "হোটেলটি স্টেশনের কাছে।"), ("ভ্রমণ", "noun", "travel", "ভ্রমণ করতে ভালো লাগে।")]),
    v("health_a2", "A2", "Health", [("ডাক্তার", "noun", "doctor", "ডাক্তারের সঙ্গে দেখা করব।"), ("ওষুধ", "noun", "medicine", "ওষুধটি সময়মতো খান।"), ("ব্যথা", "noun", "pain", "আমার মাথায় ব্যথা।"), ("হাসপাতাল", "noun", "hospital", "হাসপাতালটি কাছে।")]),
    v("study_b1", "B1", "Education", [("শিক্ষা", "noun", "education", "শিক্ষা সমাজের জন্য গুরুত্বপূর্ণ।"), ("গবেষণা", "noun", "research", "গবেষণা চলছে।"), ("পরীক্ষা", "noun", "exam", "পরীক্ষা আগামীকাল।"), ("অ্যাসাইনমেন্ট", "noun", "assignment", "অ্যাসাইনমেন্ট শেষ করেছি।")]),
    v("work_b1", "B1", "Work", [("কর্মী", "noun", "employee", "কর্মী প্রতিবেদন জমা দিলেন।"), ("সভা", "noun", "meeting", "সভা তিনটায় শুরু হবে।"), ("অভিজ্ঞতা", "noun", "experience", "তার অনেক অভিজ্ঞতা আছে।"), ("দায়িত্ব", "noun", "responsibility", "এটি আমার দায়িত্ব।")]),
    v("society_b2", "B2", "Society", [("সমাজ", "noun", "society", "সমাজ দ্রুত পরিবর্তিত হচ্ছে।"), ("উন্নয়ন", "noun", "development", "টেকসই উন্নয়ন জরুরি।"), ("নীতি", "noun", "policy", "নতুন নীতি ঘোষণা করা হয়েছে।"), ("নাগরিক", "noun", "citizen", "নাগরিকদের অধিকার জানা দরকার।")]),
    v("economy_b2", "B2", "Economy", [("অর্থনীতি", "noun", "economy", "অর্থনীতি নিয়ে আলোচনা চলছে।"), ("বাজার", "noun", "market", "বাজারে চাহিদা বেড়েছে।"), ("বিনিয়োগ", "noun", "investment", "বিনিয়োগ বৃদ্ধি পেয়েছে।"), ("আয়", "noun", "income", "পরিবারের আয় বেড়েছে।")]),
    v("media_c1", "C1", "Media", [("সংবাদ", "noun", "news", "সংবাদটি যাচাই করা দরকার।"), ("প্রতিবেদন", "noun", "report", "প্রতিবেদনে নতুন তথ্য আছে।"), ("উৎস", "noun", "source", "উৎসটি উল্লেখ করা হয়েছে।"), ("সাক্ষাৎকার", "noun", "interview", "তিনি সাক্ষাৎকার দিয়েছেন।")]),
    v("academic_c1", "C1", "Academic language", [("গবেষণা", "noun", "research", "গবেষণার ফল গুরুত্বপূর্ণ।"), ("প্রমাণ", "noun", "evidence", "প্রমাণ যথেষ্ট নয়।"), ("অনুমান", "noun", "hypothesis", "অনুমানটি পরীক্ষা করা হয়েছে।"), ("উপসংহার", "noun", "conclusion", "উপসংহারে মূল ফল তুলে ধরা হয়েছে।")]),
    v("institutional_c1", "C1", "Institutional language", [("বিধি", "noun", "regulation", "বিধি অনুযায়ী ব্যবস্থা নেওয়া হবে।"), ("আবেদন", "noun", "application", "আবেদনটি গ্রহণ করা হয়েছে।"), ("সিদ্ধান্ত", "noun", "decision", "সিদ্ধান্তটি আনুষ্ঠানিকভাবে জানানো হয়েছে।"), ("বাস্তবায়ন", "noun", "implementation", "বাস্তবায়ন পর্যবেক্ষণ করা হচ্ছে।")]),
    v("culture_c2", "C2", "Culture and literature", [("ঐতিহ্য", "noun", "heritage", "সাংস্কৃতিক ঐতিহ্য রক্ষা করা দরকার।"), ("সাহিত্য", "noun", "literature", "বাংলা সাহিত্য সমৃদ্ধ।"), ("রূপক", "noun", "metaphor", "লেখক রূপক ব্যবহার করেছেন।"), ("প্রতীক", "noun", "symbol", "প্রতীকের অর্থ ব্যাখ্যা করা হয়েছে।")]),
    v("discourse_c2", "C2", "Discourse and style", [("শৈলী", "noun", "style", "লেখার শৈলী আনুষ্ঠানিক।"), ("সুর", "noun", "tone", "বক্তব্যের সুর পরিবর্তিত হয়েছে।"), ("অন্তর্নিহিত অর্থ", "noun", "implicit meaning", "অন্তর্নিহিত অর্থ প্রসঙ্গ থেকে বোঝা যায়।"), ("পরিভাষা", "noun", "terminology", "পরিভাষা একভাবে ব্যবহার করা উচিত।")]),
]


def p(i, level, situation, items, register="neutral"):
    return PhrasebookCategory(
        id=i, level=level, situation=situation, icon="💬",
        phrases=[PhrasebookEntry(text=t, context=c, register=register) for t, c in items],
    )


PHRASEBOOK_CATEGORIES = [
    p("greetings_a1", "A1", "Greetings", [("নমস্কার!", "greeting"), ("আমার নাম রাহুল।", "introducing yourself"), ("আপনার সঙ্গে পরিচিত হয়ে ভালো লাগল।", "polite introduction")]),
    p("thanks_a1", "A1", "Thanks and apologies", [("ধন্যবাদ।", "thanks"), ("দুঃখিত।", "apology"), ("কোনো সমস্যা নেই।", "polite response")]),
    p("shopping_a1", "A1", "Shopping", [("এটার দাম কত?", "asking price"), ("আমি এটি চাই।", "requesting an item"), ("কার্ডে দিতে পারি?", "asking about payment")]),
    p("directions_a1", "A1", "Directions", [("স্টেশন কোথায়?", "asking location"), ("ডান দিকে যান।", "giving directions"), ("এখান থেকে কত দূর?", "checking distance")]),
    p("help_a1", "A1", "Help", [("আমাকে সাহায্য করুন।", "asking for help"), ("আমি বুঝতে পারছি না।", "clarification"), ("দয়া করে ধীরে বলুন।", "asking someone to slow down")]),
    p("travel_a2", "A2", "Travel", [("টিকিট কোথায় পাব?", "buying a ticket"), ("ট্রেন কখন ছাড়বে?", "asking departure time"), ("আমার বুকিং নিশ্চিত করতে চাই।", "confirming a booking")]),
    p("health_a2", "A2", "Health", [("আমার মাথায় ব্যথা।", "describing a symptom"), ("ডাক্তারের সঙ্গে দেখা করতে চাই।", "requesting care"), ("এই ওষুধ কীভাবে খাব?", "asking about medicine")]),
    p("study_b1", "B1", "Study", [("এই বিষয়টি একটু ব্যাখ্যা করবেন?", "asking for explanation"), ("আমি সময়মতো কাজটি জমা দেব।", "assignment"), ("এই উৎসটি ব্যবহার করেছি।", "citing a source")]),
    p("work_b1", "B1", "Work", [("সভা শুরু করা যাক।", "starting a meeting"), ("এই বিষয়টি আলোচনা করি।", "opening discussion"), ("প্রতিবেদনটি আগামীকাল পাঠাব।", "work commitment")]),
    p("public_b2", "B2", "Public discussion", [("এই সমস্যায় কয়েকটি কারণ প্রভাব ফেলছে।", "explaining causes"), ("অন্যদিকে...", "introducing contrast"), ("প্রমাণের ভিত্তিতে...", "introducing evidence")], "formal"),
    p("academic_c1", "C1", "Academic discussion", [("এই গবেষণা দেখায় যে...", "stating a finding"), ("এই ফলাফল সতর্কতার সঙ্গে ব্যাখ্যা করা উচিত।", "hedging"), ("এটি আরও গবেষণার দাবি রাখে।", "proposing further research")], "academic"),
    p("institutional_c1", "C1", "Institutional communication", [("আবেদনটি গ্রহণ করা হয়েছে।", "acknowledgement"), ("বিধি অনুযায়ী ব্যবস্থা নেওয়া হবে।", "formal procedure"), ("প্রয়োজনীয় তথ্য পাঠানোর অনুরোধ করছি।", "formal request")], "formal"),
    p("rhetoric_c2", "C2", "Rhetorical and nuanced speech", [("এখানে একটি গুরুত্বপূর্ণ বিষয় বিবেচনা করা দরকার।", "foregrounding a point"), ("এই ব্যাখ্যার ভিত্তি কতটা শক্তিশালী, তা দেখা যাক।", "critical evaluation"), ("এর পেছনে অন্য একটি অর্থও থাকতে পারে।", "interpreting implicit meaning")], "formal"),
]


def u(level, number, title, grammar, vocab, a, b):
    return CurriculumUnit(
        id=f"bn-{level.lower()}-{number:02}",
        level=level, unit_number=number, title=title,
        grammar_points=grammar, vocabulary_set_ids=[vocab],
        lesson_types=["grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"],
        competency_checklist=[a, b], default_weeks=2,
    )


CURRICULUM = {
    "A1": [
        u("A1", 1, "পরিচয় ও অভিবাদন", ["pronouns", "copula"], "greetings_a1", "নিজের পরিচয় দিতে পারবে", "অভিবাদন বিনিময় করতে পারবে"),
        u("A1", 2, "পরিবার", ["pronouns", "plural"], "family_a1", "পরিবারের সদস্যদের বর্ণনা করতে পারবে", "সহজ প্রশ্ন করতে পারবে"),
        u("A1", 3, "বাড়ি", ["demonstratives", "postpositions"], "home_a1", "বাড়ি বর্ণনা করতে পারবে", "বস্তুর অবস্থান বলতে পারবে"),
        u("A1", 4, "দৈনন্দিন জীবন", ["present", "negation"], "daily_a1", "রুটিন বলতে পারবে", "কী করেন না তা বলতে পারবে"),
        u("A1", 5, "খাবার ও কেনাকাটা", ["questions", "negation"], "food_a1", "সহজ খাবার কিনতে পারবে", "দাম জিজ্ঞেস করতে পারবে"),
        u("A1", 6, "স্থান ও দিকনির্দেশ", ["postpositions", "questions"], "places_a1", "স্থান জিজ্ঞেস করতে পারবে", "সহজ পথ বলতে পারবে"),
        u("A1", 7, "যোগাযোগ ও সাহায্য", ["questions", "negation"], "communication_a1", "সাহায্য চাইতে পারবে", "ভুল বোঝাবুঝি পরিষ্কার করতে পারবে"),
        u("A1", 8, "A1 পুনরাবৃত্তি", ["pronouns", "present", "questions"], "review_a1", "পরিচিত বিষয়ে কথা বলতে পারবে", "সহজ দৈনন্দিন বিনিময় করতে পারবে"),
    ],
    "A2": [
        u("A2", 1, "ভ্রমণ", ["past", "future"], "travel_a2", "আগের ভ্রমণ বর্ণনা করতে পারবে", "ভ্রমণের পরিকল্পনা বলতে পারবে"),
        u("A2", 2, "স্বাস্থ্য", ["progressive", "imperative"], "health_a2", "উপসর্গ বর্ণনা করতে পারবে", "ভদ্র অনুরোধ করতে পারবে"),
        u("A2", 3, "অতীত অভিজ্ঞতা", ["past", "perfect"], "daily_a1", "সম্পন্ন ঘটনা বলতে পারবে", "বর্তমান ফলের সঙ্গে অতীত যুক্ত করতে পারবে"),
        u("A2", 4, "ভবিষ্যৎ পরিকল্পনা", ["future", "questions"], "travel_a2", "পরিকল্পনা করতে পারবে", "সময় সম্পর্কে জিজ্ঞেস করতে পারবে"),
        u("A2", 5, "তুলনা", ["comparatives", "plural"], "home_a1", "বস্তু তুলনা করতে পারবে", "গুণ ও পরিমাণ ব্যাখ্যা করতে পারবে"),
        u("A2", 6, "ভদ্র যোগাযোগ", ["imperative", "honorifics"], "communication_a1", "ভদ্র অনুরোধ করতে পারবে", "সামাজিক দূরত্ব অনুযায়ী ভাষা বেছে নিতে পারবে"),
        u("A2", 7, "শহর ও সেবা", ["case_marking", "postpositions"], "places_a1", "সেবার স্থান খুঁজে নিতে পারবে", "অবস্থান ব্যাখ্যা করতে পারবে"),
        u("A2", 8, "A2 পুনরাবৃত্তি", ["past", "future"], "travel_a2", "অতীত ও ভবিষ্যৎ আলাদা করে বলতে পারবে", "ভ্রমণ পরিস্থিতিতে কথা বলতে পারবে"),
    ],
    "B1": [
        u("B1", 1, "শিক্ষা", ["case_marking", "modality"], "study_b1", "শেখার অভিজ্ঞতা ব্যাখ্যা করতে পারবে", "পরামর্শ দিতে পারবে"),
        u("B1", 2, "কর্মজীবন", ["modality", "honorifics"], "work_b1", "কাজের দায়িত্ব বর্ণনা করতে পারবে", "পেশাগত ভদ্রতা বজায় রাখতে পারবে"),
        u("B1", 3, "কারণ ও উদ্দেশ্য", ["causal_purpose", "conjunctive_participle"], "society_b2", "কারণ ব্যাখ্যা করতে পারবে", "উদ্দেশ্য প্রকাশ করতে পারবে"),
        u("B1", 4, "শর্ত ও ফল", ["conditional", "future"], "work_b1", "শর্তযুক্ত পরিকল্পনা করতে পারবে", "সম্ভাব্য ফল বলতে পারবে"),
        u("B1", 5, "সম্পর্কসূচক বাক্য", ["relative", "case_marking"], "study_b1", "বিশদভাবে মানুষ ও বিষয় বর্ণনা করতে পারবে", "অতিরিক্ত তথ্য যোগ করতে পারবে"),
        u("B1", 6, "ঘটনার ক্রম", ["conjunctive_participle", "aspect"], "daily_a1", "ঘটনা ধারাবাহিকভাবে বলতে পারবে", "ক্রিয়ার দৃষ্টিভঙ্গি বোঝাতে পারবে"),
        u("B1", 7, "সমস্যা সমাধান", ["causal_purpose", "modality"], "work_b1", "সমস্যার কারণ ও সমাধান বলতে পারবে", "প্রয়োজনীয়তা প্রকাশ করতে পারবে"),
        u("B1", 8, "B1 পুনরাবৃত্তি", ["relative", "conditional"], "study_b1", "জটিল বাক্য ব্যবহার করতে পারবে", "শিক্ষা ও কাজ নিয়ে আলোচনা করতে পারবে"),
    ],
    "B2": [
        u("B2", 1, "পরোক্ষ বক্তব্য", ["reported", "subordination"], "media_c1", "অন্যের বক্তব্য উপস্থাপন করতে পারবে", "উৎসের পার্থক্য বুঝতে পারবে"),
        u("B2", 2, "নিষ্ক্রিয় ও কার্যকারক", ["passive", "causative"], "institutional_c1", "ঘটনার দৃষ্টিকোণ পরিবর্তন করতে পারবে", "কারও দ্বারা কাজ করানোর অর্থ প্রকাশ করতে পারবে"),
        u("B2", 3, "প্রমাণ ও দৃষ্টিভঙ্গি", ["aspect", "hedging"], "academic_c1", "প্রমাণের মাত্রা প্রকাশ করতে পারবে", "সতর্ক অনুমান করতে পারবে"),
        u("B2", 4, "বিপরীত ও ছাড়", ["concession", "discourse"], "society_b2", "বিপরীত ধারণা যুক্ত করতে পারবে", "ছাড়ের সঙ্গে যুক্তি দিতে পারবে"),
        u("B2", 5, "অর্থনীতি", ["reported", "causal"], "economy_b2", "অর্থনৈতিক তথ্য ব্যাখ্যা করতে পারবে", "কারণ-ফল যুক্ত করতে পারবে"),
        u("B2", 6, "সামাজিক বিষয়", ["discourse", "concession"], "society_b2", "বহুমাত্রিক বিষয় আলোচনা করতে পারবে", "বিপরীত মত উপস্থাপন করতে পারবে"),
        u("B2", 7, "গণমাধ্যম", ["reported", "aspect"], "media_c1", "সংবাদ উৎস বিশ্লেষণ করতে পারবে", "তথ্য ও অনুমান আলাদা করতে পারবে"),
        u("B2", 8, "B2 পুনরাবৃত্তি", ["passive", "discourse"], "media_c1", "জটিল তথ্য সংক্ষেপ করতে পারবে", "দীর্ঘ ব্যাখ্যা লিখতে পারবে"),
    ],
    "C1": [
        u("C1", 1, "আনুষ্ঠানিক নামীকরণ", ["nominalization", "formal_register"], "institutional_c1", "আনুষ্ঠানিক ভাষায় লিখতে পারবে", "প্রক্রিয়াকে বিমূর্ত বিশেষ্যে প্রকাশ করতে পারবে"),
        u("C1", 2, "একাডেমিক সতর্কতা", ["hedging", "aspect"], "academic_c1", "নিশ্চয়তার মাত্রা বোঝাতে পারবে", "সতর্ক সিদ্ধান্ত লিখতে পারবে"),
        u("C1", 3, "জটিল অধীন বাক্য", ["subordination", "embedded_questions"], "academic_c1", "বহুস্তরীয় বক্তব্য তৈরি করতে পারবে", "পরোক্ষ প্রশ্ন ব্যবহার করতে পারবে"),
        u("C1", 4, "বিষয় ও গুরুত্ব", ["information_structure", "discourse"], "media_c1", "গুরুত্বপূর্ণ তথ্য সামনে আনতে পারবে", "প্রসঙ্গ অনুযায়ী বাক্য সাজাতে পারবে"),
        u("C1", 5, "প্রাতিষ্ঠানিক যোগাযোগ", ["formal_register", "nominalization"], "institutional_c1", "আনুষ্ঠানিক চিঠি লিখতে পারবে", "প্রক্রিয়া ব্যাখ্যা করতে পারবে"),
        u("C1", 6, "একাডেমিক যুক্তি", ["argumentation", "hedging"], "academic_c1", "প্রমাণভিত্তিক যুক্তি লিখতে পারবে", "বিপরীত মত বিবেচনা করতে পারবে"),
        u("C1", 7, "নীতি ও গণমাধ্যমের ভাষা", ["information_structure", "formal_register"], "media_c1", "সার্বজনীন লেখা বিশ্লেষণ করতে পারবে", "আনুষ্ঠানিক সুর সামঞ্জস্য করতে পারবে"),
        u("C1", 8, "C1 পুনরাবৃত্তি", ["subordination", "argumentation"], "academic_c1", "দীর্ঘ একাডেমিক ব্যাখ্যা লিখতে পারবে", "জটিল ধারণা সংযুক্ত করতে পারবে"),
    ],
    "C2": [
        u("C2", 1, "প্রয়োগগত অর্থ", ["pragmatics", "information_structure"], "discourse_c2", "সরাসরি ও অন্তর্নিহিত অর্থ আলাদা করতে পারবে", "ভদ্রতার সূক্ষ্মতা সামলাতে পারবে"),
        u("C2", 2, "অলংকারমূলক ভাষা", ["rhetoric", "discourse_analysis"], "culture_c2", "অলংকার ব্যবহার বিশ্লেষণ করতে পারবে", "সাহিত্যিক চিত্রকল্প ব্যাখ্যা করতে পারবে"),
        u("C2", 3, "অনুবাদের নির্ভুলতা", ["translation", "pragmatics"], "discourse_c2", "অর্থ ও সুর বজায় রেখে অনুবাদ করতে পারবে", "পরিভাষা প্রসঙ্গ অনুযায়ী বেছে নিতে পারবে"),
        u("C2", 4, "ডিসকোর্স বিশ্লেষণ", ["discourse_analysis", "information_structure"], "media_c1", "ধরন ও রেজিস্টার বিশ্লেষণ করতে পারবে", "ডিসকোর্সের সংহতি ব্যাখ্যা করতে পারবে"),
        u("C2", 5, "সাহিত্যিক রেজিস্টার", ["rhetoric", "translation"], "culture_c2", "সাহিত্যিক ভাষার বৈশিষ্ট্য চিনতে পারবে", "অলংকারিক পছন্দ ব্যাখ্যা করতে পারবে"),
        u("C2", 6, "উচ্চতর পেশাগত বাংলা", ["formal_register", "pragmatics"], "institutional_c1", "সূক্ষ্ম পেশাগত ধারণা প্রকাশ করতে পারবে", "সামাজিক প্রেক্ষাপটে ভদ্রতা সামঞ্জস্য করতে পারবে"),
        u("C2", 7, "বহু উৎসের সংশ্লেষ", ["argumentation", "discourse_analysis"], "media_c1", "একাধিক উৎস তুলনা করতে পারবে", "বিরোধী প্রমাণ সংশ্লেষ করতে পারবে"),
        u("C2", 8, "C2 সমন্বিত মূল্যায়ন", ["translation", "rhetoric"], "academic_c1", "জটিল একাডেমিক লেখা তৈরি করতে পারবে", "উদ্দেশ্য অনুযায়ী রেজিস্টার পরিবর্তন করতে পারবে"),
    ],
}


ASSESSMENT_BANK = [
    AssessmentQuestion(id="bn-001", skill="vocabulary", difficulty="A1", question="Which word means hello?", options=["নমস্কার", "স্টেশন", "জল", "বই"], correct="নমস্কার"),
    AssessmentQuestion(id="bn-002", skill="grammar", difficulty="A1", question="Which means 'I am a student'?", options=["আমি ছাত্র।", "সে শিক্ষক।", "আমি যাই না।", "বইটি টেবিলে আছে।"], correct="আমি ছাত্র।"),
    AssessmentQuestion(id="bn-003", skill="grammar", difficulty="A1", question="Which asks 'What is this?'", options=["এটা কী?", "আমি বাংলা পড়ি।", "এটা বই নয়।", "সে কাজ করে।"], correct="এটা কী?"),
    AssessmentQuestion(id="bn-004", skill="vocabulary", difficulty="A2", question="Which word means price?", options=["দাম", "সকাল", "সাহায্য", "নাম"], correct="দাম"),
    AssessmentQuestion(id="bn-005", skill="grammar", difficulty="A2", question="Which sentence is progressive?", options=["আমি বই পড়ছি।", "আমি বই পড়ি।", "আমি বই পড়েছিলাম।", "আমি বই পড়ব।"], correct="আমি বই পড়ছি।"),
    AssessmentQuestion(id="bn-006", skill="grammar", difficulty="B1", question="Which expresses purpose?", options=["শেখার জন্য", "যদিও", "কিন্তু", "কাল"], correct="শেখার জন্য"),
    AssessmentQuestion(id="bn-007", skill="grammar", difficulty="B1", question="Which is a conditional clause?", options=["যদি বৃষ্টি হয়", "আমি এসেছি", "সে পড়ছে", "এটি বই"], correct="যদি বৃষ্টি হয়"),
    AssessmentQuestion(id="bn-008", skill="grammar", difficulty="B2", question="Which reports another person's statement?", options=["সে বলল যে কাল আসবে।", "সে আজ আসে।", "সে বই পড়ে।", "সে বাড়িতে আছে।"], correct="সে বলল যে কাল আসবে।"),
    AssessmentQuestion(id="bn-009", skill="vocabulary", difficulty="B2", question="What does প্রমাণ mean?", options=["evidence", "holiday", "neighbor", "ticket"], correct="evidence"),
    AssessmentQuestion(id="bn-010", skill="academic", difficulty="C1", question="Which is an academic hedge?", options=["হতে পারে", "নমস্কার", "বিদায়", "এখানে"], correct="হতে পারে"),
    AssessmentQuestion(id="bn-011", skill="formal", difficulty="C1", question="Which is institutional language?", options=["বিধি অনুযায়ী ব্যবস্থা নেওয়া হবে।", "নমস্কার!", "আমি এটি চাই।", "এটার দাম কত?"], correct="বিধি অনুযায়ী ব্যবস্থা নেওয়া হবে।"),
    AssessmentQuestion(id="bn-012", skill="discourse", difficulty="C2", question="What should advanced translation preserve?", options=["meaning, register and discourse function", "word count only", "literal order only", "punctuation only"], correct="meaning, register and discourse function"),
]

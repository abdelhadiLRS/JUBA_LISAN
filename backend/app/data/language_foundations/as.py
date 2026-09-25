"""Assamese A1-C2 foundation data for JUBA LISAN."""
from app.data._types import AssessmentQuestion, CurriculumUnit, GrammarExample, GrammarTopic, PhrasebookCategory, PhrasebookEntry, VocabularyEntry, VocabularySet

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def g(slug, title, level, summary, examples):
    return GrammarTopic(
        slug=slug, title=title, level=level, category="grammar",
        summary=summary, explanation=summary,
        examples=[GrammarExample(text=x) for x in examples],
    )


GRAMMAR_TOPICS = [
    g("pronouns","Personal pronouns","A1","Use মই, তুমি, আপুনি, তেওঁ and আমি in everyday reference.",["মই ছাত্ৰ।","আপুনি শিক্ষক।"]),
    g("copula","Nominal sentences","A1","Identify people and things with Assamese nominal patterns.",["তেওঁ শিক্ষক।","এইটো কিতাপ।"]),
    g("present","Present and habitual actions","A1","Describe current and habitual actions with natural Assamese verb forms.",["মই অসমীয়া পঢ়োঁ।","তেওঁ কাম কৰে।"]),
    g("questions","Questions and question words","A1","Ask yes-no and information questions with কি, ক'ত, কোন and কেনেকৈ.",["এইটো কি?","আপুনি ক'ত আছে?"]),
    g("negation","Negation","A1","Negate verbal and nominal clauses with natural Assamese negative forms.",["মই নাযাওঁ।","এইটো কিতাপ নহয়।"]),
    g("demonstratives","Demonstratives","A1","Point to nearby and distant people and things.",["এইটো মোৰ কিতাপ।","সেইটো ঘৰ।"]),
    g("possessive","Possession","A1","Express possession with মোৰ, তোমাৰ, তেওঁৰ and related noun phrases.",["এইটো মোৰ ঘৰ।","তেওঁৰ কিতাপখন নতুন।"]),
    g("location","Location and postpositions","A1","Describe location with ঘৰত, স্কুলত and other locative patterns.",["মই ঘৰত আছোঁ।","কিতাপখন মেজত আছে।"]),
    g("plural","Plural and classifiers","A2","Form common plurals with -বোৰ/-বিলাক and quantify nouns.",["কিতাপবোৰ ইয়াত আছে।","ছাত্ৰসকল আহিল।"]),
    g("past","Past tense","A2","Describe completed events and past experience.",["মই কালি বজাৰলৈ গ'লোঁ।","তেওঁ ভাত খালে।"]),
    g("future","Future and intention","A2","Express future plans, predictions and intentions.",["মই কাইলৈ যাম।","তেওঁ পিছত আহিব।"]),
    g("progressive","Progressive actions","A2","Describe actions in progress with আছে and appropriate verbal forms.",["মই এতিয়া পঢ়ি আছোঁ।","তেওঁ কাম কৰি আছে।"]),
    g("imperative","Imperatives and polite requests","A2","Give instructions and make respectful requests.",["বহক।","অনুগ্ৰহ কৰি আকৌ কওক।"]),
    g("comparison","Comparison","A2","Compare people and things with অধিক, কম and আটাইতকৈ.",["এইটো অধিক ডাঙৰ।","তেওঁ আটাইতকৈ দ্ৰুত।"]),
    g("time","Time, dates and frequency","A2","Talk about schedules, dates, duration and frequency.",["মই ৰাতিপুৱা কাম কৰোঁ।","আমি পাঁচ বজাত লগ পাম।"]),
    g("case_postpositions","Case and postpositional phrases","B1","Use Assamese postpositions and case-like markers accurately.",["মই বন্ধুৰ সৈতে গ'লোঁ।","তেওঁ ঘৰৰ পৰা আহিল।"]),
    g("modality","Ability, necessity and permission","B1","Express ability, obligation, possibility and permission.",["মই যাব পাৰোঁ।","তোমাৰ পঢ়িব লাগে।"]),
    g("conditional","Conditional clauses","B1","Build real and hypothetical conditions with যদি and তেন্তে.",["যদি বৰষুণ দিয়ে, তেন্তে আমি নাযাম।","যদি সময় পাওঁ, আহিম।"]),
    g("relative","Relative clauses","B1","Modify nouns with যে and relative constructions.",["যিজন মানুহ আহিল, তেওঁ মোৰ শিক্ষক।","মই পঢ়া কিতাপখন ভাল।"]),
    g("converbs","Conjunctive participles and sequencing","B1","Link actions through -ই and related sequential constructions.",["ভাত খাই তেওঁ ওলাই গ'ল।","কাম শেষ কৰি ঘৰলৈ গ'লোঁ।"]),
    g("causal","Cause, purpose and result","B1","Express reasons, goals and consequences with কাৰণ, বাবে and যাতে.",["বৰষুণৰ বাবে আমি নাযালোঁ।","পঢ়িবলৈ মই পুথিভঁৰাললৈ গ'লোঁ।"]),
    g("reflexive","Reflexive and reciprocal reference","B1","Refer back to participants and express reciprocal actions.",["তেওঁ নিজকে প্ৰস্তুত কৰিলে।","তেওঁলোকে ইজনে সিজনক সহায় কৰিলে।"]),
    g("reported","Reported speech","B2","Report statements, questions and requests while preserving tense and meaning.",["তেওঁ ক'লে যে কাইলৈ আহিব।","শিক্ষকে সুধিলে মই সাজু নেকি।"]),
    g("passive","Passive constructions","B2","Present events from the affected participant's perspective.",["চিঠিখন লিখা হ'ল।","দুৱাৰখন খোলা হ'ল।"]),
    g("aspect","Aspect and event viewpoint","B2","Distinguish ongoing, completed and habitual interpretations.",["মই কিতাপখন পঢ়ি আছিলোঁ।","তেওঁ কামটো শেষ কৰিছে।"]),
    g("concession","Contrast and concession","B2","Connect opposing ideas with যদিও, কিন্তু and related markers.",["যদিও বৰষুণ দিছিল, তথাপি আমি গ'লোঁ।","মই ব্যস্ত, কিন্তু আহিম।"]),
    g("discourse","Discourse cohesion","B2","Organize explanations with sequence, cause, contrast and conclusion markers.",["প্ৰথমতে সমস্যাটো বুজিব লাগিব। তাৰ পিছত সমাধান বিচাৰিব লাগিব।"]),
    g("nominalization","Nominalization","C1","Use abstract noun phrases in formal and analytical Assamese.",["শিক্ষাৰ উন্নয়ন অতি প্ৰয়োজনীয়।","সিদ্ধান্ত গ্ৰহণৰ প্ৰক্ৰিয়াটো দীঘলীয়া।"]),
    g("hedging","Academic hedging and stance","C1","Qualify claims and distinguish evidence from interpretation.",["এই ফলাফলে সম্ভৱতঃ এটা পৰিৱৰ্তনৰ ইংগিত দিয়ে।","এই দাবীটো অধিক অধ্যয়নৰ প্ৰয়োজন।"]),
    g("subordination","Complex subordination","C1","Build multi-clause sentences expressing logical and temporal relations.",["যদি তথ্যসমূহ নিশ্চিত হয়, তেন্তে পৰিকল্পনাটো আগবঢ়াব পাৰি।"]),
    g("embedded_questions","Embedded questions","C1","Embed questions inside reports, requests and formal explanations.",["তেওঁ কেতিয়া আহিব আমি নাজানো।","মই জানিব বিচাৰোঁ কিয় এনে হ'ল।"]),
    g("information_structure","Topic and focus","C1","Control emphasis through constituent order and discourse context.",["এই সমস্যাটো আমি আজি আলোচনা কৰিম।","গুৰুত্বপূৰ্ণ কথাটো হ'ল তথ্যসমূহ।"]),
    g("formal_register","Formal and institutional Assamese","C1","Adapt vocabulary and syntax for administration, education and public communication.",["অনুগ্ৰহ কৰি প্ৰয়োজনীয় নথিপত্ৰসমূহ দাখিল কৰক।"]),
    g("argumentation","Academic argumentation","C1","Present claims, evidence, counterarguments and conclusions coherently.",["উপলব্ধ তথ্যৰ ভিত্তিত এই সিদ্ধান্তত উপনীত হ'ব পাৰি।"]),
    g("pragmatics","Pragmatics and politeness","C2","Manage indirectness, respect, social distance and implied meaning.",["সম্ভৱ হ'লে এই বিষয়টো পুনৰ বিবেচনা কৰিবনে?"]),
    g("rhetoric","Rhetorical and literary style","C2","Use metaphor, repetition, parallelism and stylistic variation.",["এই বাক্যই সমাজৰ পৰিৱৰ্তনৰ এক শক্তিশালী ছবি আঁকে।"]),
    g("translation","Translation precision","C2","Preserve meaning, register and discourse function across contexts.",["অনুবাদত অৰ্থ আৰু ভাষাশৈলী দুয়োটাই সংৰক্ষণ কৰিব লাগে।"]),
    g("discourse_analysis","Discourse analysis and register shifting","C2","Analyze genre, cohesion, stance and shifts between spoken and written Assamese.",["চৰকাৰী লিখনীৰ ভাষাশৈলী দৈনন্দিন কথিত ভাষাৰ পৰা পৃথক।"]),
]


def v(i, level, topic, words):
    return VocabularySet(
        id=i, level=level, topic=topic, unit_ref=i,
        words=[VocabularyEntry(word=w, pos=p, definition=d, example=e) for w,p,d,e in words],
    )


VOCABULARY_SETS = [
    v("greetings_a1","A1","পৰিচয়",[("নমস্কাৰ","phrase","hello","নমস্কাৰ।"),("ধন্যবাদ","phrase","thank you","ধন্যবাদ।"),("বিদায়","phrase","goodbye","বিদায়।"),("নাম","noun","name","মোৰ নাম ৰবি।")]),
    v("identity_a1","A1","পৰিচয়",[("ছাত্ৰ","noun","student","মই ছাত্ৰ।"),("শিক্ষক","noun","teacher","তেওঁ শিক্ষক।"),("মানুহ","noun","person","তেওঁ এজন ভাল মানুহ।"),("বন্ধু","noun","friend","তেওঁ মোৰ বন্ধু।")]),
    v("family_a1","A1","পৰিয়াল",[("মা","noun","mother","মোৰ মা ঘৰত আছে।"),("দেউতা","noun","father","মোৰ দেউতা কাম কৰে।"),("ভাই","noun","brother","মোৰ ভাই স্কুললৈ যায়।"),("ভনী","noun","sister","মোৰ ভনী পঢ়ে।")]),
    v("home_a1","A1","ঘৰ",[("ঘৰ","noun","home","এইটো মোৰ ঘৰ।"),("কোঠা","noun","room","কোঠাটো পৰিষ্কাৰ।"),("দুৱাৰ","noun","door","দুৱাৰখন খোলা।"),("মেজ","noun","table","কিতাপখন মেজত আছে।")]),
    v("daily_a1","A1","দৈনন্দিন জীৱন",[("পুৱা","noun","morning","পুৱাই মই কাম কৰোঁ।"),("দিন","noun","day","আজি ভাল দিন।"),("কাম","noun","work","মই কাম কৰোঁ।"),("পানী","noun","water","মোক পানী লাগে।")]),
    v("food_a1","A1","খাদ্য",[("ভাত","noun","rice","মই ভাত খাওঁ।"),("ৰুটি","noun","bread","মই ৰুটি খাওঁ।"),("চাহ","noun","tea","মই চাহ খাওঁ।"),("আপেল","noun","apple","আপেলটো ৰঙা।")]),
    v("places_a1","A1","ঠাই আৰু দিশ",[("বজাৰ","noun","market","বজাৰখন ক'ত?"),("বিদ্যালয়","noun","school","বিদ্যালয়খন ওচৰত।"),("হাস্পতাল","noun","hospital","হাস্পতালখন ক'ত আছে?"),("ৰাস্তা","noun","road","ৰাস্তাটো দীঘল।")]),
    v("communication_a1","A1","যোগাযোগ",[("প্ৰশ্ন","noun","question","মোৰ এটা প্ৰশ্ন আছে।"),("সহায়","noun","help","মোক সহায় লাগে।"),("ভাষা","noun","language","অসমীয়া এটা ভাষা।"),("কোৱা","verb","speak/say","অনুগ্ৰহ কৰি কওক।")]),
    v("people_a2","A2","মানুহ আৰু সমাজ",[("চুবুৰীয়া","noun","neighbor","মোৰ চুবুৰীয়া ভাল।"),("অতিথি","noun","guest","আজি এজন অতিথি আহিছে।"),("দল","noun","group","দলটো ডাঙৰ।"),("সম্প্ৰদায়","noun","community","সম্প্ৰদায়টোৱে একেলগে কাম কৰে।")]),
    v("travel_a2","A2","ভ্ৰমণ",[("বিমান","noun","airplane","বিমানখন পুৱা উৰিব।"),("ৰেল","noun","train","ৰেলখন আহিছে।"),("টিকট","noun","ticket","টিকট ক'ত কিনিম?"),("হোটেল","noun","hotel","আমি হোটেলত থাকিম।")]),
    v("health_a2","A2","স্বাস্থ্য",[("ডাক্তৰ","noun","doctor","মই ডাক্তৰৰ ওচৰলৈ যাম।"),("অসুস্থ","adjective","ill","মই আজি অসুস্থ।"),("ঔষধ","noun","medicine","ঔষধটো সময়মতে খাব।"),("চিকিৎসালয়","noun","hospital","চিকিৎসালয়খন ওচৰত।")]),
    v("study_b1","B1","শিক্ষা",[("অধ্যয়ন","noun","study","অধ্যয়নটো গুৰুত্বপূৰ্ণ।"),("গৃহকাৰ্য","noun","assignment","গৃহকাৰ্যটো শেষ কৰিলোঁ।"),("পৰীক্ষা","noun","exam","পৰীক্ষা কাইলৈ।"),("গৱেষণা","noun","research","গৱেষণাটো নতুন।")]),
    v("work_b1","B1","কৰ্মজীৱন",[("কৰ্মচাৰী","noun","employee","কৰ্মচাৰীয়ে প্ৰতিবেদন দিলে।"),("সভা","noun","meeting","সভাখন তিনিবজাত।"),("অভিজ্ঞতা","noun","experience","তেওঁৰ অভিজ্ঞতা আছে।"),("দায়িত্ব","noun","responsibility","এইটো মোৰ দায়িত্ব।")]),
    v("society_b2","B2","সমাজ",[("সমাজ","noun","society","সমাজ সলনি হৈ আছে।"),("উন্নয়ন","noun","development","টেকসই উন্নয়ন প্ৰয়োজনীয়।"),("নীতি","noun","policy","নতুন নীতি ঘোষণা কৰা হ'ল।"),("নাগৰিক","noun","citizen","নাগৰিকে নিজৰ অধিকাৰ জানিব লাগে।")]),
    v("economy_b2","B2","অৰ্থনীতি",[("অৰ্থনীতি","noun","economy","অৰ্থনীতিৰ বিকাশ হৈছে।"),("বজাৰ","noun","market","বজাৰৰ চাহিদা বাঢ়িছে।"),("বিনিয়োগ","noun","investment","বিনিয়োগ বৃদ্ধি পাইছে।"),("আয়","noun","income","পৰিয়ালৰ আয় বাঢ়িছে।")]),
    v("media_c1","C1","মাধ্যম",[("তথ্য","noun","information","তথ্যসমূহ পৰীক্ষা কৰিব লাগে।"),("প্ৰবন্ধ","noun","article","প্ৰবন্ধটো দীঘল।"),("উৎস","noun","source","উৎসটো স্পষ্ট।"),("সাক্ষাৎকাৰ","noun","interview","সাক্ষাৎকাৰটো ৰেকৰ্ড কৰা হ'ল।")]),
    v("academic_c1","C1","শৈক্ষিক ভাষা",[("গৱেষণা","noun","research","গৱেষণাই নতুন ফলাফল দেখুৱাইছে।"),("প্ৰমাণ","noun","evidence","প্ৰমাণ যথেষ্ট নহয়।"),("অনুমান","noun","hypothesis","অনুমানটো পৰীক্ষা কৰা হ'ল।"),("উপসংহাৰ","noun","conclusion","উপসংহাৰটো তথ্যৰ ওপৰত আধাৰিত।")]),
    v("institutional_c1","C1","চৰকাৰী আৰু আনুষ্ঠানিক ভাষা",[("নিয়ম","noun","regulation","নিয়ম অনুসৰি সিদ্ধান্ত লোৱা হ'ব।"),("আবেদন","noun","application","আবেদনখন গ্ৰহণ কৰা হ'ল।"),("সিদ্ধান্ত","noun","decision","সিদ্ধান্তটো প্ৰকাশ কৰা হ'ল।"),("কাৰ্যকৰীকৰণ","noun","implementation","কাৰ্যকৰীকৰণ পৰ্যবেক্ষণ কৰা হৈছে।")]),
    v("culture_c2","C2","সংস্কৃতি আৰু সাহিত্য",[("ঐতিহ্য","noun","heritage","সাংস্কৃতিক ঐতিহ্য সংৰক্ষণ কৰিব লাগে।"),("সাহিত্য","noun","literature","অসমীয়া সাহিত্য সমৃদ্ধ।"),("চিত্ৰকল্প","noun","imagery","লেখকে শক্তিশালী চিত্ৰকল্প ব্যৱহাৰ কৰিছে।"),("প্ৰতীক","noun","symbol","প্ৰতীকৰ অৰ্থ গুৰুত্বপূৰ্ণ।")]),
    v("discourse_c2","C2","বক্তব্য আৰু ভাষাশৈলী",[("ভাষাশৈলী","noun","style","চৰকাৰী ভাষাশৈলী পৃথক।"),("সুৰ","noun","tone","বাক্যটোৰ সুৰ লক্ষ্য কৰিব লাগে।"),("অন্তৰ্নিহিত অৰ্থ","phrase","implicit meaning","অন্তৰ্নিহিত অৰ্থটো প্ৰসংগৰ পৰা বুজা যায়।"),("পৰিভাষা","noun","terminology","পৰিভাষা একে ধৰণে ব্যৱহাৰ কৰিব লাগে।")]),
]


def p(i, level, situation, items, register="neutral"):
    return PhrasebookCategory(
        id=i, level=level, situation=situation, icon="💬",
        phrases=[PhrasebookEntry(text=t, context=c, register=register) for t,c in items],
    )


PHRASEBOOK_CATEGORIES = [
    p("greetings_a1","A1","পৰিচয়",[("নমস্কাৰ।","greeting"),("আপোনাৰ নাম কি?","asking a name"),("মোৰ নাম ৰবি।","introducing yourself")]),
    p("thanks_a1","A1","ধন্যবাদ আৰু ক্ষমা",[("ধন্যবাদ।","thanks"),("অনুগ্ৰহ কৰি।","please"),("ক্ষমা কৰিব।","apology")]),
    p("shopping_a1","A1","বজাৰ",[("এইটো কিমান?","asking price"),("মোক এইটো লাগে।","requesting an item"),("আন ৰং আছে নেকি?","asking for another option")]),
    p("directions_a1","A1","দিশ",[("বজাৰখন ক'ত আছে?","asking location"),("বিদ্যালয়লৈ কেনেকৈ যাম?","asking a route"),("পোনে পোনে গৈ সোঁফালে যাব।","giving directions")]),
    p("help_a1","A1","সহায়",[("অনুগ্ৰহ কৰি মোক সহায় কৰক।","asking for help"),("মই বুজি পোৱা নাই।","saying you do not understand"),("অনুগ্ৰহ কৰি আকৌ কওক।","asking for repetition")]),
    p("travel_a2","A2","ভ্ৰমণ",[("টিকট ক'ৰ পৰা কিনিম?","buying a ticket"),("হোটেলখন ক'ত আছে?","finding a hotel"),("মোৰ বুকিংটো নিশ্চিত কৰিব বিচাৰোঁ।","confirming a booking")]),
    p("health_a2","A2","স্বাস্থ্য",[("মোৰ মূৰ বিষাইছে।","describing a symptom"),("মই ডাক্তৰক লগ পাব বিচাৰোঁ।","requesting medical help"),("এই ঔষধটো কেনেকৈ খাব লাগে?","asking about medicine")]),
    p("study_b1","B1","অধ্যয়ন",[("এই কথাটো বুজাই দিবনে?","asking for explanation"),("মোৰ গৃহকাৰ্য শেষ হৈছে।","discussing an assignment"),("মই এই উৎসটো ব্যৱহাৰ কৰিছোঁ।","citing a source")]),
    p("work_b1","B1","কৰ্মক্ষেত্ৰ",[("সভাখন আৰম্ভ কৰোঁ আহক।","starting a meeting"),("এই সমস্যাটো আলোচনা কৰোঁ আহক।","opening discussion"),("প্ৰতিবেদনটো কাইলৈ পঠাম।","work commitment")]),
    p("public_b2","B2","ৰাজহুৱা আলোচনা",[("এই সমস্যাটোৰ কেইবাটাও কাৰণ আছে।","explaining causes"),("আনহাতে...","introducing contrast"),("উপলব্ধ প্ৰমাণৰ ভিত্তিত...","introducing evidence")],"formal"),
    p("academic_c1","C1","শৈক্ষিক আলোচনা",[("এই গৱেষণাই দেখুৱাইছে যে...","stating a finding"),("এই ফলাফলটো সাৱধানে ব্যাখ্যা কৰা উচিত।","hedging"),("এই বিষয়টো অধিক অধ্যয়নৰ প্ৰয়োজন।","proposing further research")],"academic"),
    p("institutional_c1","C1","আনুষ্ঠানিক যোগাযোগ",[("আবেদনখন গ্ৰহণ কৰা হৈছে।","acknowledging an application"),("নিয়ম অনুসৰি সিদ্ধান্ত লোৱা হ'ব।","formal procedure"),("অনুগ্ৰহ কৰি প্ৰয়োজনীয় তথ্য দাখিল কৰক।","formal request")],"formal"),
    p("rhetoric_c2","C2","সূক্ষ্ম আৰু অলংকাৰিক ভাষা",[("এটা গুৰুত্বপূৰ্ণ কথা ইয়াত লক্ষ্য কৰিব লাগে।","foregrounding a point"),("এই ব্যাখ্যাটো যথেষ্ট শক্তিশালী নেকি বিবেচনা কৰোঁ আহক।","critical evaluation"),("এই কথাৰ আঁৰত আন এটা অৰ্থ থাকিব পাৰে।","interpreting implicit meaning")],"formal"),
]


def u(level, n, title, grammar, vocab, a, b):
    return CurriculumUnit(
        id=f"as-{level.lower()}-{n:02}", level=level, unit_number=n, title=title,
        grammar_points=grammar, vocabulary_set_ids=[vocab],
        lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],
        competency_checklist=[a,b], default_weeks=2,
    )


CURRICULUM = {
    "A1":[
        u("A1",1,"নমস্কাৰ আৰু পৰিচয়",["pronouns","copula"],"greetings_a1","নিজকে পৰিচয় কৰাব", "মৌলিক সম্ভাষণ কৰিব"),
        u("A1",2,"পৰিয়াল",["possessive","questions"],"family_a1","পৰিয়ালৰ বিষয়ে ক'ব","মৌলিক প্ৰশ্ন সুধিব"),
        u("A1",3,"ঘৰ",["location","demonstratives"],"home_a1","ঘৰ বৰ্ণনা কৰিব","বস্তুৰ স্থান ক'ব"),
        u("A1",4,"দৈনন্দিন জীৱন",["present","negation"],"daily_a1","দৈনন্দিন কাম বৰ্ণনা কৰিব","নাকাৰাত্মক বাক্য গঠন কৰিব"),
        u("A1",5,"খাদ্য আৰু বজাৰ",["questions","numbers"],"food_a1","খাদ্য কিনিব","দাম আৰু পৰিমাণ সুধিব"),
        u("A1",6,"ঠাই আৰু দিশ",["location","questions"],"places_a1","স্থান সুধিব","দিশ দেখুৱাব"),
        u("A1",7,"যোগাযোগ",["negation","questions"],"communication_a1","সহায় বিচাৰিব","নুবুজা কথা স্পষ্ট কৰিব"),
        u("A1",8,"A1 পুনৰাবৃত্তি",["present","possessive"],"greetings_a1","চিনাকি বিষয়ত কথা পাতিব","চুটি সংলাপ চলাব"),
    ],
    "A2":[
        u("A2",1,"মানুহ আৰু সম্পৰ্ক",["plural","present"],"people_a2","মানুহ আৰু গোট বৰ্ণনা কৰিব","অভ্যাসৰ বিষয়ে ক'ব"),
        u("A2",2,"ভ্ৰমণ",["past","future"],"travel_a2","অতীতৰ ভ্ৰমণ বৰ্ণনা কৰিব","ভৱিষ্যৎ পৰিকল্পনা ক'ব"),
        u("A2",3,"স্বাস্থ্য",["progressive","imperative"],"health_a2","লক্ষণ বৰ্ণনা কৰিব","ভদ্ৰ অনুৰোধ কৰিব"),
        u("A2",4,"সময় আৰু পৰিকল্পনা",["future","time"],"daily_a1","সময়সূচী ক'ব","পৰিকল্পনা আলোচনা কৰিব"),
        u("A2",5,"তুলনা",["comparison","plural"],"home_a1","বস্তু তুলনা কৰিব","গুণ আৰু আকাৰ বৰ্ণনা কৰিব"),
        u("A2",6,"ভদ্ৰ যোগাযোগ",["imperative","questions"],"communication_a1","ভদ্ৰভাৱে অনুৰোধ কৰিব","স্পষ্টীকৰণ বিচাৰিব"),
        u("A2",7,"চহৰ আৰু সেৱা",["location","case_postpositions"],"places_a1","সেৱাৰ স্থান বিচাৰিব","পথ বৰ্ণনা কৰিব"),
        u("A2",8,"A2 পুনৰাবৃত্তি",["past","future"],"travel_a2","অতীত আৰু ভৱিষ্যৎ পৃথক কৰিব","ভ্ৰমণৰ পৰিস্থিতিত কথা পাতিব"),
    ],
    "B1":[
        u("B1",1,"শিক্ষা",["case_postpositions","modality"],"study_b1","শিক্ষাৰ প্ৰক্ৰিয়া বৰ্ণনা কৰিব","পৰামৰ্শ দিব"),
        u("B1",2,"কৰ্মজীৱন",["modality","conditional"],"work_b1","কৰ্মৰ দায়িত্ব বৰ্ণনা কৰিব","চৰ্তসাপেক্ষ প্ৰস্তাৱ দিব"),
        u("B1",3,"কাৰণ আৰু উদ্দেশ্য",["causal","converbs"],"society_b2","কাৰণ ব্যাখ্যা কৰিব","উদ্দেশ্য প্ৰকাশ কৰিব"),
        u("B1",4,"চৰ্ত আৰু পৰিকল্পনা",["conditional","future"],"travel_a2","চৰ্তসাপেক্ষ পৰিকল্পনা কৰিব","সম্ভাৱ্য ফলাফল ক'ব"),
        u("B1",5,"সম্বন্ধসূচক বাক্য",["relative","case_postpositions"],"study_b1","নামপদ অধিক স্পষ্ট কৰিব","অতিৰিক্ত তথ্য দিব"),
        u("B1",6,"ঘটনাৰ ক্ৰম",["converbs","past"],"daily_a1","ঘটনা ক্ৰমে ক'ব","প্ৰক্ৰিয়া বৰ্ণনা কৰিব"),
        u("B1",7,"সমস্যা সমাধান",["causal","modality"],"work_b1","কাৰণ আৰু সমাধান ক'ব","প্ৰয়োজন আৰু পৰামৰ্শ প্ৰকাশ কৰিব"),
        u("B1",8,"B1 পুনৰাবৃত্তি",["relative","conditional"],"study_b1","জটিল বাক্য ব্যৱহাৰ কৰিব","শিক্ষা আৰু কামৰ বিষয়ে আলোচনা কৰিব"),
    ],
    "B2":[
        u("B2",1,"পৰোক্ষ বক্তব্য",["reported","subordination"],"media_c1","আন মানুহৰ বক্তব্য জনাব","উৎস পৃথক কৰিব"),
        u("B2",2,"কৰ্মবাচ্য আৰু দৃষ্টিভংগী",["passive","aspect"],"institutional_c1","ঘটনাৰ কেন্দ্ৰ সলনি কৰিব","ঘটনাৰ অৱস্থা পৃথক কৰিব"),
        u("B2",3,"প্ৰমাণ আৰু অনুমান",["aspect","modality"],"academic_c1","নিশ্চয়তাৰ স্তৰ প্ৰকাশ কৰিব","অনুমান সাৱধানে ক'ব"),
        u("B2",4,"বিৰোধ আৰু ৰেহাই",["concession","discourse"],"society_b2","বিৰোধী ধাৰণা সংযোগ কৰিব","অন্য দৃষ্টিভংগী স্বীকাৰ কৰিব"),
        u("B2",5,"অৰ্থনীতি",["reported","causal"],"economy_b2","অৰ্থনৈতিক তথ্য ব্যাখ্যা কৰিব","কাৰণ আৰু ফল সংযোগ কৰিব"),
        u("B2",6,"সামাজিক সমস্যা",["discourse","concession"],"society_b2","বহুমুখী সমস্যা আলোচনা কৰিব","বিভিন্ন মতামত উপস্থাপন কৰিব"),
        u("B2",7,"মাধ্যম",["reported","aspect"],"media_c1","তথ্যৰ উৎস ব্যাখ্যা কৰিব","প্ৰমাণ আৰু অনুমান পৃথক কৰিব"),
        u("B2",8,"B2 পুনৰাবৃত্তি",["passive","discourse"],"media_c1","দীঘল তথ্য সংক্ষেপ কৰিব","সংগঠিত ব্যাখ্যা দিব"),
    ],
    "C1":[
        u("C1",1,"আনুষ্ঠানিক ভাষা",["nominalization","formal_register"],"institutional_c1","আনুষ্ঠানিক শৈলীত লিখিব","নামীকৰণ ব্যৱহাৰ কৰিব"),
        u("C1",2,"শৈক্ষিক ভাষা",["hedging","aspect"],"academic_c1","প্ৰমাণ আৰু ব্যাখ্যা পৃথক কৰিব","সাৱধানী সিদ্ধান্ত লিখিব"),
        u("C1",3,"জটিল বাক্য",["subordination","embedded_questions"],"academic_c1","জটিল ধাৰণা গঠন কৰিব","অন্তৰ্ভুক্ত প্ৰশ্ন ব্যৱহাৰ কৰিব"),
        u("C1",4,"বিষয় আৰু গুৰুত্ব",["information_structure","discourse"],"discourse_c2","মুখ্য তথ্য সংগঠিত কৰিব","প্ৰসংগ অনুসৰি বাক্য বিন্যাস বাছিব"),
        u("C1",5,"প্ৰাতিষ্ঠানিক যোগাযোগ",["formal_register","nominalization"],"institutional_c1","চৰকাৰী লিখনী গঠন কৰিব","প্ৰক্ৰিয়া ব্যাখ্যা কৰিব"),
        u("C1",6,"শৈক্ষিক যুক্তি",["argumentation","hedging"],"academic_c1","প্ৰমাণভিত্তিক যুক্তি দিব","বিকল্প মত বিবেচনা কৰিব"),
        u("C1",7,"মাধ্যম আৰু ৰাজহুৱা ভাষা",["information_structure","formal_register"],"media_c1","ৰাজহুৱা তথ্য বিশ্লেষণ কৰিব","ভাষাৰ সুৰ সলনি কৰিব"),
        u("C1",8,"C1 পুনৰাবৃত্তি",["subordination","argumentation"],"academic_c1","দীঘল বিশ্লেষণ লিখিব","জটিল ধাৰণা সংযোগ কৰিব"),
    ],
    "C2":[
        u("C2",1,"প্ৰয়োগবাদ আৰু অন্তৰ্নিহিত অৰ্থ",["pragmatics","information_structure"],"discourse_c2","প্ৰত্যক্ষ আৰু অন্তৰ্নিহিত অৰ্থ পৃথক কৰিব","সামাজিক দূৰত্ব নিয়ন্ত্ৰণ কৰিব"),
        u("C2",2,"অলংকাৰ আৰু সাহিত্য",["rhetoric","discourse_analysis"],"culture_c2","অলংকাৰিক কৌশল ব্যৱহাৰ কৰিব","সাহিত্যিক শৈলী বিশ্লেষণ কৰিব"),
        u("C2",3,"অনুবাদ আৰু নিখুঁততা",["translation","pragmatics"],"discourse_c2","অৰ্থ আৰু ভাষাশৈলী সংৰক্ষণ কৰিব","প্ৰসংগ অনুসৰি পৰিভাষা বাছিব"),
        u("C2",4,"বক্তব্য বিশ্লেষণ",["discourse_analysis","information_structure"],"discourse_c2","ধৰণ আৰু ৰেজিষ্টাৰ বিশ্লেষণ কৰিব","বক্তব্যৰ সংযোগ ব্যাখ্যা কৰিব"),
        u("C2",5,"সাহিত্যিক ৰেজিষ্টাৰ",["rhetoric","translation"],"culture_c2","সাহিত্যিক ভাষা চিনাক্ত কৰিব","শৈলীগত পছন্দ ব্যাখ্যা কৰিব"),
        u("C2",6,"উচ্চ স্তৰৰ পেছাদাৰী ভাষা",["formal_register","pragmatics"],"institutional_c1","পেছাদাৰী ধাৰণা সূক্ষ্মভাৱে প্ৰকাশ কৰিব","প্ৰসংগ অনুসৰি ভদ্ৰতা সলনি কৰিব"),
        u("C2",7,"বহু উৎসৰ সংহতি",["argumentation","discourse_analysis"],"media_c1","বহু উৎস সংহত কৰিব","বিৰোধী প্ৰমাণ তুলনা কৰিব"),
        u("C2",8,"C2 সমন্বিত মূল্যায়ন",["translation","rhetoric"],"academic_c1","বিশদ শৈক্ষিক ৰচনা লিখিব","উদ্দেশ্য অনুসৰি ভাষাশৈলী বাছিব"),
    ],
}


_ASSESSMENTS = [
    ("A1","vocabulary","What does নমস্কাৰ mean?",["hello","goodbye","water","school"],"hello"),
    ("A1","grammar","Which means 'My name is Rabi'?",["মোৰ নাম ৰবি।","মই ঘৰত আছোঁ।","মোক পানী লাগে।","ধন্যবাদ।"],"মোৰ নাম ৰবি।"),
    ("A1","vocabulary","What does মা mean?",["mother","father","friend","teacher"],"mother"),
    ("A2","grammar","Which sentence describes a completed past action?",["মই কালি বজাৰলৈ গ'লোঁ।","মই এতিয়া পঢ়ি আছোঁ।","মই কাইলৈ যাম।","মই নাযাওঁ।"],"মই কালি বজাৰলৈ গ'লোঁ।"),
    ("A2","vocabulary","What does টিকট mean?",["ticket","medicine","meeting","source"],"ticket"),
    ("B1","grammar","Which expression introduces a condition?",["যদি... তেন্তে...","কাৰণ...","কিন্তু...","তাৰ পিছত..."],"যদি... তেন্তে..."),
    ("B1","grammar","Which expression introduces purpose?",["যাতে...","কাৰণ...","কিন্তু...","কালি..."],"যাতে..."),
    ("B2","grammar","Which introduces reported speech?",["তেওঁ ক'লে যে...","এইটো কিমান?","নমস্কাৰ!","ক'ত আছে?"],"তেওঁ ক'লে যে..."),
    ("B2","vocabulary","What does প্ৰমাণ mean?",["evidence","holiday","neighbor","ticket"],"evidence"),
    ("C1","academic","Which expression is a hedge?",["সম্ভৱতঃ...","নমস্কাৰ!","এইটো কিমান?","ধন্যবাদ।"],"সম্ভৱতঃ..."),
    ("C1","formal","Which is formal institutional language?",["নিয়ম অনুসৰি সিদ্ধান্ত লোৱা হ'ব।","নমস্কাৰ!","মোক এইটো লাগে।","মই পানী খাওঁ।"],"নিয়ম অনুসৰি সিদ্ধান্ত লোৱা হ'ব।"),
    ("C2","discourse","What should a translator preserve?",["meaning, register and discourse function","word count only","literal word order only","punctuation only"],"meaning, register and discourse function"),
]

ASSESSMENT_BANK = [
    AssessmentQuestion(id=f"as-{i:03}", skill=skill, difficulty=level, question=q, options=opts, correct=correct)
    for i,(level,skill,q,opts,correct) in enumerate(_ASSESSMENTS,1)
]

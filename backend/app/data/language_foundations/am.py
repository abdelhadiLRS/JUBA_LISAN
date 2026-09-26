"""Amharic foundation data for JUBA LISAN — A1 to C2."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

_TOPIC_DATA = [
("pronouns-copula", "Pronouns and copula", "A1", "syntax", "Identify people and entities with personal pronouns and the copula.", "እኔ ተማሪ ነኝ።"),
("basic-sentence-order", "Basic sentence order", "A1", "syntax", "Build simple Amharic clauses with subject, object and verb.", "እኔ አማርኛ እማራለሁ።"),
("present-imperfect", "Present and imperfect forms", "A1", "verbs", "Use common present/imperfect verb forms for habits and current actions.", "በየቀኑ እሰራለሁ።"),
("negation", "Negation", "A1", "verbs", "Form negative statements in everyday situations.", "አልጠጣም።"),
("yes-no-questions", "Yes/no and information questions", "A1", "communication", "Ask and answer basic questions with question words and intonation.", "ስምህ ማን ነው?"),
("possessive-forms", "Possession and genitive", "A1", "noun-phrase", "Express ownership and relationships between nouns.", "ይህ መጽሐፌ ነው።"),
("plural-nouns", "Plural nouns", "A1", "morphology", "Recognize and use common plural noun forms.", "ተማሪዎች መጡ።"),
("locative-direction", "Location and direction", "A1", "prepositions", "Describe where people and objects are and where they move.", "ቤት ውስጥ ነኝ።"),
("definite-noun-forms", "Definiteness and noun phrases", "A2", "noun-phrase", "Use definite noun forms and modifiers in connected speech.", "መጽሐፉን አነበብኩ።"),
("object-marking", "Object marking and pronouns", "A2", "morphology", "Use object-related morphology and pronoun forms accurately.", "መጽሐፉን አየሁ።"),
("past-tense", "Past tense", "A2", "verbs", "Narrate completed events in the past.", "ትናንት ወደ ገበያ ሄድኩ።"),
("future-intention", "Future and intention", "A2", "verbs", "Talk about plans, predictions and intended actions.", "ነገ እሄዳለሁ።"),
("imperative-politeness", "Imperatives and polite requests", "A2", "communication", "Give instructions and make polite requests.", "እባክዎ ይጠብቁ።"),
("comparatives", "Comparison", "A2", "syntax", "Compare people, objects and situations.", "ይህ ከዚያ ይሻላል።"),
("modal-verbs", "Ability, obligation and desire", "A2", "modality", "Express ability, necessity, permission and desire.", "መሄድ እፈልጋለሁ።"),
("gerund-verbal-noun", "Verbal nouns and dependent actions", "B1", "verbs", "Connect actions through verbal-noun constructions and complements.", "ማንበብ እወዳለሁ።"),
("relative-clauses", "Relative clauses", "B1", "syntax", "Modify nouns with relative clauses in spoken and written language.", "ያነበብኩት መጽሐፍ ጥሩ ነው።"),
("conditional", "Conditional clauses", "B1", "syntax", "Express real and hypothetical conditions.", "ጊዜ ካገኘሁ እመጣለሁ።"),
("causal-concessive", "Cause, result and concession", "B1", "discourse", "Link clauses to explain causes, results and contrasts.", "ስለዘገየ በጊዜ አልደረሰም።"),
("reported-speech", "Reported speech", "B1", "discourse", "Report what another person said or thought.", "እንደሚመጣ ነገረኝ።"),
("aspect-event-structure", "Event structure and aspect", "B2", "verbs", "Distinguish ongoing, completed, habitual and sequential events.", "ሲደርስ እየሰራሁ ነበር።"),
("passive-causative", "Passive and causative patterns", "B2", "morphology", "Describe affected participants and caused events.", "ቤቱ ተገነባ።"),
("subordination", "Complex subordination", "B2", "syntax", "Combine multiple dependent clauses coherently.", "ምንም እንኳን ዘግይቶ ቢመጣም ስራውን ጨረሰ።"),
("discourse-connectors", "Discourse connectors", "B2", "discourse", "Organize explanations and arguments with cohesive connectors.", "በመጀመሪያ ጉዳዩን እንመልከት፤ ከዚያም መፍትሔ እንፈልጋለን።"),
("nominalization", "Nominalization", "C1", "academic", "Turn propositions and actions into compact noun phrases.", "የፕሮጀክቱ መጠናቀቅ ወሳኝ ነው።"),
("academic-hedging", "Academic hedging", "C1", "academic", "Qualify claims and distinguish evidence from interpretation.", "ይህ ውጤት ሊያመለክት ይችላል።"),
("embedded-questions", "Embedded questions", "C1", "syntax", "Embed questions within statements and formal requests.", "መቼ እንደሚመጣ አላውቅም።"),
("information-structure", "Topic and focus", "C1", "discourse", "Manage information structure, emphasis and contrast.", "ይህን ጉዳይ ነው የምንመረምረው።"),
("formal-register", "Formal and professional register", "C1", "register", "Shift from conversational Amharic to institutional and professional prose.", "እባክዎ ማመልከቻዎን በጽሑፍ ያቅርቡ።"),
("argumentation", "Academic argumentation", "C1", "rhetoric", "State claims, evidence, counterarguments and conclusions clearly.", "ይህ አቋም በተገኘው ማስረጃ ይደገፋል።"),
("pragmatics", "Pragmatics and politeness", "C2", "pragmatics", "Interpret indirectness, politeness, stance and social context.", "እስቲ ይህን ጉዳይ እንደገና እንመልከት።"),
("idiomatic-language", "Idiomatic Amharic", "C2", "lexis", "Interpret common idiomatic and figurative expressions from context.", "እጄን አጠራለሁ።"),
("media-style", "News and media language", "C2", "register", "Read concise reporting, headlines and institutional media prose.", "መንግሥት አዲስ ፖሊሲ አስታወቀ።"),
("rhetoric", "Rhetorical and literary style", "C2", "rhetoric", "Analyze emphasis, parallelism, metaphor and rhetorical effect.", "ቃሉ እንደ ብርሃን ይመራል።"),
("translation-precision", "Translation and lexical precision", "C2", "translation", "Choose context-sensitive Amharic equivalents rather than literal substitutions.", "ትርጉሙን እንደ አውዱ መምረጥ አለብን።"),
("discourse-analysis", "Discourse analysis", "C2", "discourse", "Analyze cohesion, stance, reference and rhetorical structure across texts.", "ጽሑፉ ዋናውን ክርክር በተከታታይ ያቀርባል።"),
("register-shifting", "Register shifting and style control", "C2", "register", "Reformulate the same message for casual, professional and academic contexts.", "ይህን መልዕክት በመደበኛ ቋንቋ እንደገና እንጽፈው።"),
]

GRAMMAR_TOPICS = [GrammarTopic(slug=s, title=t, level=l, category=c, summary=sm, explanation=f"{sm} Native Amharic model: {ex}", examples=[GrammarExample(text=ex)]) for s,t,l,c,sm,ex in _TOPIC_DATA]

_VOCAB = [
("am-a1-1","Greetings and identity","ሰላም","Hello","ሰላም፣ ስሜ ሚካኤል ነው።"),
("am-a1-2","Family","ቤተሰብ","family","ቤተሰቤ እዚህ ነው።"),
("am-a1-3","Home","ቤት","house/home","ቤት ውስጥ ነኝ።"),
("am-a1-4","Daily life","ሥራ","work","በየቀኑ እሰራለሁ።"),
("am-a1-5","Time","ሰዓት","time/hour","ስንት ሰዓት ነው?"),
("am-a1-6","Food","እንጀራ","injera","እንጀራ እወዳለሁ።"),
("am-a1-7","Places","ገበያ","market","ወደ ገበያ እሄዳለሁ።"),
("am-a1-8","Directions","መንገድ","road/way","መንገዱ የት ነው?"),
("am-a2-1","Travel","ጉዞ","travel","ጉዞው ረጅም ነበር።"),
("am-a2-2","Health","ጤና","health","ጤና ይስጥልኝ።"),
("am-a2-3","Education","ትምህርት","education","ትምህርት ይወዳል።"),
("am-a2-4","Work","ቢሮ","office","በቢሮ እሰራለሁ።"),
("am-b1-1","Communication","መልዕክት","message","መልዕክት ላክሁ።"),
("am-b1-2","Society","ማህበረሰብ","community/society","ማህበረሰቡ ተሳትፏል።"),
("am-b1-3","Environment","አካባቢ","environment","አካባቢውን እንጠብቃለን።"),
("am-b1-4","Technology","ቴክኖሎጂ","technology","ቴክኖሎጂ ስራውን አቀላጠፈ።"),
("am-b2-1","Economy","ኢኮኖሚ","economy","ኢኮኖሚው እየተሻሻለ ነው።"),
("am-b2-2","Policy","ፖሊሲ","policy","አዲስ ፖሊሲ ተወጣ።"),
("am-b2-3","Evidence","ማስረጃ","evidence","ማስረጃ ማቅረብ አስፈላጊ ነው።"),
("am-b2-4","Research","ምርምር","research","ምርምሩ አዲስ ውጤት አሳየ።"),
("am-c1-1","Analysis","ትንተና","analysis","ትንተናው ግልጽ ነው።"),
("am-c1-2","Argument","ክርክር","argument/debate","ክርክሩን በማስረጃ አቀረበ።"),
("am-c2-1","Rhetoric","አነጋገር","rhetorical expression","አነጋገሩ በጣም አሳማኝ ነው።"),
("am-c2-2","Translation","ትርጉም","translation/meaning","ትርጉሙ እንደ አውዱ ይለያያል።"),
]
VOCABULARY_SETS = [VocabularySet(id=i, level=i.split("-")[1].upper(), topic=topic, unit_ref=f"{i}-unit-1", words=[VocabularyEntry(word=w, pos="noun", definition=d, example=e)]) for i,topic,w,d,e in _VOCAB]

_UNIT_TOPICS = {
"A1":["Identity and pronouns","Family and people","Home and location","Daily routines","Time and appointments","Food and shopping","Places and directions","Everyday communication"],
"A2":["Definiteness and noun phrases","Object marking","Past narration","Future plans","Polite requests","Comparison","Ability and obligation","Everyday problem solving"],
"B1":["Verbal nouns","Relative clauses","Conditions","Cause and contrast","Reported speech","Storytelling","Opinions and reasons","Connected conversation"],
"B2":["Aspect and event structure","Passive and causative","Complex subordination","Discourse connectors","Formal correspondence","Media texts","Evidence and explanation","Professional communication"],
"C1":["Nominalization","Academic hedging","Embedded questions","Topic and focus","Professional register","Argumentation","Research communication","Policy and institutional language"],
"C2":["Pragmatics","Idiomatic language","Media analysis","Rhetorical style","Translation precision","Discourse analysis","Register shifting","Literary and professional synthesis"],
}
CURRICULUM = {}
for level in LEVELS:
    CURRICULUM[level] = []
    for n, title in enumerate(_UNIT_TOPICS[level], 1):
        topic_index = min((LEVELS.index(level)*6 + n - 1), len(GRAMMAR_TOPICS)-1)
        vocab_ids = [v[0] for v in _VOCAB if v[0].split("-")[1].upper() == level][:1]
        if not vocab_ids:
            vocab_ids = ["am-a1-1"]
        CURRICULUM[level].append(CurriculumUnit(id=f"am-{level.lower()}-unit-{n}", level=level, unit_number=n, title=f"Amharic {level} · {title}", grammar_points=[GRAMMAR_TOPICS[topic_index].title], vocabulary_set_ids=vocab_ids, lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"], competency_checklist=[f"Use {level} Amharic in {title.lower()}","Understand authentic learner-level Amharic input","Produce accurate spoken and written responses"], default_weeks=2))

PHRASEBOOK_CATEGORIES = [
PhrasebookCategory(id="am-greetings",level="A1",situation="Greetings",icon="👋",phrases=[PhrasebookEntry(text="ሰላም።",context="Hello.",register="neutral"),PhrasebookEntry(text="እንዴት ነህ?",context="How are you? (to a man)",register="neutral"),PhrasebookEntry(text="ደህና ነኝ።",context="I am fine.",register="neutral")]),
PhrasebookCategory(id="am-thanks",level="A1",situation="Thanks",icon="🙏",phrases=[PhrasebookEntry(text="አመሰግናለሁ።",context="Thank you.",register="neutral"),PhrasebookEntry(text="በጣም አመሰግናለሁ።",context="Thank you very much.",register="polite"),PhrasebookEntry(text="ምንም አይደለም።",context="You're welcome / No problem.",register="neutral")]),
PhrasebookCategory(id="am-shopping",level="A1",situation="Shopping",icon="🛒",phrases=[PhrasebookEntry(text="ይህ ስንት ነው?",context="How much is this?",register="neutral"),PhrasebookEntry(text="ይህን እፈልጋለሁ።",context="I want this.",register="neutral"),PhrasebookEntry(text="ዋጋውን ዝቅ ማድረግ ይቻላል?",context="Can the price be reduced?",register="polite")]),
PhrasebookCategory(id="am-directions",level="A1",situation="Directions",icon="🧭",phrases=[PhrasebookEntry(text="የት ነው?",context="Where is it?",register="neutral"),PhrasebookEntry(text="ወደ ጣቢያው እንዴት እደርሳለሁ?",context="How do I get to the station?",register="neutral"),PhrasebookEntry(text="በቀጥታ ይሂዱ።",context="Go straight.",register="neutral")]),
PhrasebookCategory(id="am-help",level="A1",situation="Help",icon="🆘",phrases=[PhrasebookEntry(text="እባክዎ እርዱኝ።",context="Please help me.",register="polite"),PhrasebookEntry(text="እንደገና ይናገሩ።",context="Please say it again.",register="polite"),PhrasebookEntry(text="በዝግታ ይናገሩ።",context="Please speak slowly.",register="polite")]),
PhrasebookCategory(id="am-restaurant",level="A2",situation="Restaurant",icon="🍽️",phrases=[PhrasebookEntry(text="ምናሌውን እባክዎ ይስጡኝ።",context="Please give me the menu.",register="polite"),PhrasebookEntry(text="ይህን እፈልጋለሁ።",context="I would like this.",register="neutral"),PhrasebookEntry(text="ደረሰኙን እባክዎ ይስጡኝ።",context="Please give me the receipt.",register="polite")]),
PhrasebookCategory(id="am-travel",level="A2",situation="Travel",icon="✈️",phrases=[PhrasebookEntry(text="ትኬቴ የት ነው?",context="Where is my ticket?",register="neutral"),PhrasebookEntry(text="መንገዱ ምን ያህል ይርቃል?",context="How far is the route?",register="neutral"),PhrasebookEntry(text="ማረፊያ ቦታ እፈልጋለሁ።",context="I need accommodation.",register="neutral")]),
PhrasebookCategory(id="am-health",level="A2",situation="Health",icon="🩺",phrases=[PhrasebookEntry(text="ሐኪም ማየት እፈልጋለሁ።",context="I need to see a doctor.",register="neutral"),PhrasebookEntry(text="ህመም አለብኝ።",context="I am in pain.",register="neutral"),PhrasebookEntry(text="የት ሆስፒታል አለ?",context="Where is there a hospital?",register="neutral")]),
PhrasebookCategory(id="am-work",level="B1",situation="Work",icon="💼",phrases=[PhrasebookEntry(text="ስብሰባውን እንጀምር።",context="Let's start the meeting.",register="formal"),PhrasebookEntry(text="እባክዎ ማስረጃውን ያቅርቡ።",context="Please provide the evidence.",register="formal"),PhrasebookEntry(text="በዚህ ጉዳይ እንስማማለን።",context="We agree on this matter.",register="formal")]),
PhrasebookCategory(id="am-opinion",level="B2",situation="Opinions and debate",icon="💬",phrases=[PhrasebookEntry(text="በእኔ እምነት...",context="In my view...",register="neutral"),PhrasebookEntry(text="ማስረጃው የሚያሳየው...",context="The evidence shows...",register="formal"),PhrasebookEntry(text="በሌላ በኩል...",context="On the other hand...",register="formal")]),
PhrasebookCategory(id="am-academic",level="C1",situation="Academic writing",icon="📚",phrases=[PhrasebookEntry(text="ይህ ጥናት ያሳያል...",context="This study shows...",register="formal"),PhrasebookEntry(text="ይህ ሊያመለክት ይችላል...",context="This may indicate...",register="formal"),PhrasebookEntry(text="ተጨማሪ ምርምር ያስፈልጋል።",context="Further research is needed.",register="formal")]),
PhrasebookCategory(id="am-formal",level="C1",situation="Formal correspondence",icon="📝",phrases=[PhrasebookEntry(text="ለጥያቄዎ ምላሽ ለመስጠት...",context="In response to your request...",register="formal"),PhrasebookEntry(text="እባክዎ ማመልከቻዎን ያቅርቡ።",context="Please submit your application.",register="formal"),PhrasebookEntry(text="በቅርቡ እንመልስልዎታለን።",context="We will respond shortly.",register="formal")]),
PhrasebookCategory(id="am-pragmatics",level="C2",situation="Nuance and pragmatics",icon="🎯",phrases=[PhrasebookEntry(text="እስቲ ይህን እንደገና እንመልከት።",context="Let's reconsider this.",register="neutral"),PhrasebookEntry(text="ጉዳዩ በአውዱ ላይ ይመረኮዛል።",context="It depends on the context.",register="formal"),PhrasebookEntry(text="ይህን በሌላ መንገድ ማቅረብ ይቻላል።",context="This can be presented another way.",register="neutral")]),
]

ASSESSMENT_BANK = [
AssessmentQuestion(id="am-a1-001",skill="communication",difficulty="A1",question="Which Amharic expression means ‘Hello’?",options=["ሰላም።","አመሰግናለሁ።","የት ነው?","ይህ ስንት ነው?"],correct="ሰላም።"),
AssessmentQuestion(id="am-a1-002",skill="communication",difficulty="A1",question="Which phrase means ‘I am fine’?",options=["ደህና ነኝ።","እባክዎ እርዱኝ።","ይህን እፈልጋለሁ።","ሰላም።"],correct="ደህና ነኝ።"),
AssessmentQuestion(id="am-a1-003",skill="vocabulary",difficulty="A1",question="Which word means ‘family’?",options=["ቤተሰብ","ገበያ","መንገድ","ሥራ"],correct="ቤተሰብ"),
AssessmentQuestion(id="am-a1-004",skill="communication",difficulty="A1",question="How do you ask ‘How much is this?’",options=["ይህ ስንት ነው?","የት ነው?","እንዴት ነህ?","በዝግታ ይናገሩ።"],correct="ይህ ስንት ነው?"),
AssessmentQuestion(id="am-a2-005",skill="grammar",difficulty="A2",question="Which sentence refers to a completed past event?",options=["ትናንት ወደ ገበያ ሄድኩ።","ነገ እሄዳለሁ።","እሄዳለሁ።","እሄድ ነበር።"],correct="ትናንት ወደ ገበያ ሄድኩ።"),
AssessmentQuestion(id="am-a2-006",skill="communication",difficulty="A2",question="Which phrase is a polite request to wait?",options=["እባክዎ ይጠብቁ።","ወደ ገበያ እሄዳለሁ።","ሰላም።","ጤና ይስጥልኝ።"],correct="እባክዎ ይጠብቁ።"),
AssessmentQuestion(id="am-b1-007",skill="grammar",difficulty="B1",question="Which sentence contains a conditional meaning?",options=["ጊዜ ካገኘሁ እመጣለሁ።","ትናንት መጣሁ።","እኔ ተማሪ ነኝ።","መጽሐፉን አነበብኩ።"],correct="ጊዜ ካገኘሁ እመጣለሁ።"),
AssessmentQuestion(id="am-b1-008",skill="discourse",difficulty="B1",question="Which expression introduces reported content?",options=["እንደሚመጣ ነገረኝ።","ሰላም።","ይህ ስንት ነው?","ቤት ውስጥ ነኝ።"],correct="እንደሚመጣ ነገረኝ።"),
AssessmentQuestion(id="am-b2-009",skill="discourse",difficulty="B2",question="Which phrase functions as a contrastive connector?",options=["በሌላ በኩል...","በየቀኑ...","እባክዎ...","ሰላም..."],correct="በሌላ በኩል..."),
AssessmentQuestion(id="am-c1-010",skill="academic",difficulty="C1",question="Which expression appropriately hedges an academic claim?",options=["ይህ ሊያመለክት ይችላል።","ይህ በእርግጥ ሁሉንም ያረጋግጣል።","ሰላም።","ይህ ስንት ነው?"],correct="ይህ ሊያመለክት ይችላል።"),
AssessmentQuestion(id="am-c1-011",skill="formal",difficulty="C1",question="Which phrase is suitable for a formal application context?",options=["እባክዎ ማመልከቻዎን ያቅርቡ።","እንዴት ነህ?","ይህን እፈልጋለሁ።","ሰላም።"],correct="እባክዎ ማመልከቻዎን ያቅርቡ።"),
AssessmentQuestion(id="am-c2-012",skill="pragmatics",difficulty="C2",question="Which expression explicitly refers to contextual interpretation?",options=["ጉዳዩ በአውዱ ላይ ይመረኮዛል።","ሰላም።","ቤት ውስጥ ነኝ።","ይህ ስንት ነው?"],correct="ጉዳዩ በአውዱ ላይ ይመረኮዛል።"),
]

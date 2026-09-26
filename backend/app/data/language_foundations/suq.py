"""Samburu (suq) A1-C2 foundation data for JUBA LISAN.

The authored examples intentionally keep the target-language material short and
reusable by the lesson generator.  English definitions are metadata only.
"""
from app.data._types import (
    AssessmentQuestion,
    CurriculumUnit,
    GrammarExample,
    GrammarTopic,
    PhrasebookCategory,
    PhrasebookEntry,
    VocabularyEntry,
    VocabularySet,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

_GRAMMAR = [
    ("greetings", "Greetings and introductions", "A1", "phrase", "Open and close a basic interaction.", "Supa."),
    ("identity", "Personal identity", "A1", "syntax", "Introduce yourself and ask for a name.", "Nanyor..."),
    ("family", "Family and home", "A1", "noun", "Talk about close family and home.", "enkaji."),
    ("routine", "Daily routine", "A1", "verbs", "Describe simple habitual actions.", "aisho."),
    ("time", "Time and daily schedule", "A1", "time", "Use basic day and time expressions.", "aitidua."),
    ("food", "Food and drink", "A1", "vocabulary", "Express basic food and drink needs.", "enkare."),
    ("places", "Places and location", "A1", "syntax", "Say where people and things are.", "enkaji."),
    ("politeness", "Polite interaction", "A1", "discourse", "Use short polite exchanges.", "ashe."),
    ("questions", "Information questions", "A2", "syntax", "Ask and answer practical questions.", "Kaji?"),
    ("negation", "Negation", "A2", "grammar", "Negate simple statements.", "Meyia."),
    ("possession", "Possession", "A2", "noun", "Express ownership and relationships.", "enkaji."),
    ("location", "Locative expressions", "A2", "syntax", "Give and understand locations.", "enkaji."),
    ("commands", "Commands and requests", "A2", "verbs", "Make simple requests and instructions.", "Kaitin..."),
    ("comparison", "Comparison", "A2", "adjective", "Compare people, objects, and places.", "nabo."),
    ("aspect", "Habitual and ongoing actions", "A2", "verbs", "Distinguish routine from ongoing activity.", "aisho."),
    ("past", "Past events", "B1", "verbs", "Narrate completed everyday events.", "Aisho ake."),
    ("future", "Future plans", "B1", "verbs", "Talk about intentions and plans.", "Aisho neme."),
    ("sequence", "Sequencing events", "B1", "discourse", "Link events in a clear sequence.", "enkai."),
    ("reason", "Reasons and causes", "B1", "discourse", "Explain why something happened.", "na."),
    ("condition", "Conditions", "B1", "syntax", "Describe possible conditions and results.", "meishia."),
    ("experience", "Personal experience", "B1", "discourse", "Describe experiences and outcomes.", "Aisho."),
    ("reported", "Reported information", "B1", "discourse", "Report what another person said or told you.", "Nanyor..."),
    ("relative", "Relative descriptions", "B2", "syntax", "Add identifying information to a noun.", "enkaji."),
    ("discourse", "Connected discourse", "B2", "discourse", "Connect several ideas into a coherent account.", "ashe."),
    ("contrast", "Contrast and concession", "B2", "discourse", "Contrast alternatives and acknowledge exceptions.", "nabo."),
    ("emphasis", "Focus and emphasis", "B2", "discourse", "Highlight important information.", "Supa."),
    ("register", "Social register", "C1", "pragmatics", "Adapt wording to social context.", "ashe."),
    ("stance", "Attitude and stance", "C1", "pragmatics", "Express certainty, doubt, and attitude.", "Meyia."),
    ("narrative", "Extended narrative", "C1", "discourse", "Sustain a detailed narrative.", "Aisho."),
    ("argument", "Explanation and argument", "C1", "discourse", "Explain and defend a position.", "nabo."),
    ("cohesion", "Cohesion and reference", "C2", "discourse", "Maintain reference across extended speech.", "enkaji."),
    ("nuance", "Meaning and pragmatic nuance", "C2", "pragmatics", "Interpret subtle contextual meanings.", "ashe."),
    ("style", "Style and genre", "C2", "pragmatics", "Adapt language to genre and purpose.", "Supa."),
    ("mediation", "Mediation and reformulation", "C2", "discourse", "Reformulate complex information for another listener.", "Aisho."),
]

GRAMMAR_TOPICS = [
    GrammarTopic(
        slug=slug,
        title=title,
        level=level,
        category=category,
        summary=summary,
        explanation=summary,
        examples=[GrammarExample(text=example), GrammarExample(text=f"{example} Ashe.")],
    )
    for slug, title, level, category, summary, example in _GRAMMAR
]

_VOCAB = [
    ("greetings", "Greetings", ["Supa", "ashe", "Nanyor..."]),
    ("identity", "Identity", ["Nanyor...", "enkaji", "Supa"]),
    ("family", "Family", ["enkaji", "enkito", "ashe"]),
    ("home", "Home", ["enkaji", "enkare", "aisho"]),
    ("routine", "Daily routine", ["aisho", "aitidua", "enkaji"]),
    ("time", "Time", ["aitidua", "enkai", "aisho"]),
    ("food", "Food", ["enkare", "enkaji", "ashe"]),
    ("drink", "Food and drink", ["enkare", "ashe", "Supa"]),
    ("community", "Community", ["enkaji", "aisho", "nabo"]),
    ("travel", "Travel", ["enkaji", "aitidua", "enkare"]),
    ("shopping", "Shopping", ["enkare", "aisho", "ashe"]),
    ("work", "Work", ["aisho", "aitidua", "enkaji"]),
    ("school", "Learning", ["aisho", "Nanyor...", "enkaji"]),
    ("health", "Health", ["enkare", "ashe", "enkaji"]),
    ("nature", "Nature", ["enkare", "enkaji", "aitidua"]),
    ("weather", "Weather", ["aitidua", "enkare", "nabo"]),
    ("society", "Society", ["enkaji", "aisho", "ashe"]),
    ("storytelling", "Storytelling", ["Aisho", "nabo", "ashe"]),
    ("ideas", "Ideas and opinions", ["nabo", "Meyia", "ashe"]),
    ("formal", "Formal communication", ["ashe", "nabo", "Supa"]),
]

_VOCAB_DEFS = {
    "Supa": "hello",
    "ashe": "thank you",
    "Nanyor...": "my name is...",
    "enkaji": "home / house",
    "enkito": "child",
    "enkare": "water",
    "aisho": "work",
    "aitidua": "today",
    "enkai": "day / time",
    "nabo": "like / as",
    "Meyia": "no / not",
    "Aisho": "work / working",
}

VOCABULARY_SETS = [
    VocabularySet(
        id=f"suq_{idx}_{level.lower()}",
        level=level,
        topic=topic,
        unit_ref=f"suq-{level.lower()}-unit-{idx}",
        words=[
            VocabularyEntry(
                word=word,
                pos="noun" if not word.endswith("...") else "phrase",
                definition=_VOCAB_DEFS.get(word, "target-language vocabulary"),
                example=f"{word}.",
            )
            for word in words
        ],
    )
    for idx, (key, topic, words) in enumerate(_VOCAB, 1)
    for level in (["A1"] if idx <= 8 else ["A2"] if idx <= 12 else ["B1"] if idx <= 15 else ["B2"] if idx <= 17 else ["C1"] if idx <= 19 else ["C2"])
]

# Give every level a complete set of unit-linked vocabulary references.
_LEVEL_VOCAB = {level: [v for v in VOCABULARY_SETS if v.level == level] for level in LEVELS}

PHRASE_DATA = [
    ("Greetings", "👋", ["Supa", "Ashe.", "Nanyor..."]),
    ("Introductions", "🪪", ["Nanyor...", "Supa.", "Ashe."]),
    ("Family", "👨‍👩‍👧", ["enkaji.", "enkito.", "Ashe."]),
    ("Home", "🏠", ["enkaji.", "Supa.", "ashe."]),
    ("Daily routine", "⏰", ["aisho.", "aitidua.", "enkai."]),
    ("Food and drink", "🍽️", ["enkare.", "ashe.", "Supa."]),
    ("Shopping", "🛒", ["enkare.", "ashe.", "Nanyor..."]),
    ("Directions", "🧭", ["enkaji.", "aitidua.", "ashe."]),
    ("Travel", "🚌", ["enkaji.", "enkare.", "Supa."]),
    ("Health", "🩺", ["enkare.", "ashe.", "enkaji."]),
    ("Work", "💼", ["aisho.", "aitidua.", "ashe."]),
    ("Opinions", "💬", ["nabo.", "Meyia.", "ashe."]),
    ("Formal interaction", "🤝", ["ashe.", "Supa.", "nabo."]),
]
PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(
        id=f"suq_phrase_{idx}",
        level="A1" if idx <= 8 else "A2" if idx <= 10 else "B1",
        situation=situation,
        icon=icon,
        phrases=[PhrasebookEntry(text=p, context=situation.lower(), register="neutral") for p in phrases],
    )
    for idx, (situation, icon, phrases) in enumerate(PHRASE_DATA, 1)
]

_UNIT_TITLES = {
    "A1": ["Greetings", "Identity", "Family", "Home", "Routine", "Time", "Food", "Places"],
    "A2": ["Questions", "Negation", "Possession", "Requests", "Comparison", "Daily activities", "Community", "Review"],
    "B1": ["Past events", "Future plans", "Sequencing", "Reasons", "Conditions", "Experience", "Reported information", "Review"],
    "B2": ["Relative descriptions", "Connected discourse", "Contrast", "Emphasis", "Practical narratives", "Community topics", "Extended reading", "Review"],
    "C1": ["Social register", "Stance", "Extended narrative", "Argument", "Formal communication", "Cultural topics", "Critical reading", "Review"],
    "C2": ["Cohesion", "Pragmatic nuance", "Style and genre", "Mediation", "Complex narratives", "Interpretation", "Advanced discourse", "Review"],
}
_LEVEL_GRAMMAR = {level: [g.slug for g in GRAMMAR_TOPICS if g.level == level] for level in LEVELS}

CURRICULUM = {}
for level in LEVELS:
    grammar_slugs = _LEVEL_GRAMMAR[level]
    vocab_sets = _LEVEL_VOCAB[level]
    units = []
    for number, title in enumerate(_UNIT_TITLES[level], 1):
        gslug = grammar_slugs[(number - 1) % len(grammar_slugs)]
        vset = vocab_sets[(number - 1) % len(vocab_sets)]
        units.append(
            CurriculumUnit(
                id=f"suq-{level.lower()}-unit-{number}",
                level=level,
                unit_number=number,
                title=title,
                grammar_points=[gslug],
                vocabulary_set_ids=[vset.id],
                lesson_types=["grammar", "vocabulary", "speaking", "listening", "reading", "review"],
                competency_checklist=[f"Use Samburu at {level} level in a short contextual task", "Recognize and produce the target pattern"],
                default_weeks=1 if level in ("A1", "A2") else 2,
            )
        )
    CURRICULUM[level] = units

ASSESSMENT_BANK = [
    AssessmentQuestion(
        id=f"suq-{level.lower()}-{idx:03d}",
        skill=skill,
        difficulty=level,
        question=question,
        options=options,
        correct=correct,
    )
    for level, skill, question, options, correct in [
        ("A1", "communication", "Which Samburu expression is used as a greeting?", ["Supa", "enkare", "aisho", "Meyia"], "Supa"),
        ("A1", "communication", "Which expression introduces your name?", ["Nanyor...", "enkaji", "aitidua", "ashe"], "Nanyor..."),
        ("A1", "vocabulary", "Which word is associated with home?", ["enkaji", "enkare", "aisho", "Supa"], "enkaji"),
        ("A1", "vocabulary", "Which word is associated with water?", ["enkare", "enkaji", "aisho", "ashe"], "enkare"),
        ("A2", "grammar", "Which topic helps you say that something is not the case?", ["Negation", "Greetings", "Time", "Family"], "Negation"),
        ("A2", "communication", "Which topic helps you make a simple request?", ["Commands and requests", "Family", "Food", "Time"], "Commands and requests"),
        ("B1", "grammar", "Which topic is used to narrate completed events?", ["Past events", "Greetings", "Possession", "Politeness"], "Past events"),
        ("B1", "communication", "Which topic connects events into a sequence?", ["Sequencing events", "Identity", "Food", "Places"], "Sequencing events"),
        ("B1", "grammar", "Which topic expresses a possible condition and result?", ["Conditions", "Greetings", "Home", "Time"], "Conditions"),
        ("B2", "discourse", "Which topic helps connect several ideas coherently?", ["Connected discourse", "Greetings", "Food", "Identity"], "Connected discourse"),
        ("B2", "pragmatics", "Which topic focuses attention on important information?", ["Focus and emphasis", "Family", "Time", "Water"], "Focus and emphasis"),
        ("C1", "pragmatics", "Which topic adapts language to social context?", ["Social register", "Past events", "Food", "Home"], "Social register"),
        ("C2", "discourse", "Which topic maintains reference across extended speech?", ["Cohesion and reference", "Greetings", "Family", "Shopping"], "Cohesion and reference"),
        ("C2", "discourse", "Which topic involves reformulating complex information for another listener?", ["Mediation and reformulation", "Time", "Identity", "Food"], "Mediation and reformulation"),
    ]
]

# Keep the public access pattern consistent with the other foundation modules.

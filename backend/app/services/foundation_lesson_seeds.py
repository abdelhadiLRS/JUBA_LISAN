"""Runtime lesson seeds derived from authored language foundations."""
from __future__ import annotations

import importlib
from typing import Any

from app.data.curriculum import get_curriculum
from app.data.grammar import get_grammar_topics
from app.data.vocabulary import get_vocabulary_sets


def _base_language(target_language: str) -> str:
    return str(target_language).replace("_", "-").split("-")[0].lower()


def _foundation_available(target_language: str) -> bool:
    code = _base_language(target_language)
    if not code:
        return False
    try:
        importlib.import_module(f"app.data.language_foundations.{code}")
    except (ImportError, ModuleNotFoundError):
        return False
    return True


def _curated_seed(
    target_language: str,
    cefr_level: str,
    unit_id: str,
    lesson_type: str,
) -> dict[str, Any] | None:
    """Load a language-specific curated seed when one exists.

    This keeps the main generator stable while allowing newly authored
    languages to opt into the curated runtime layer incrementally.
    """
    code = _base_language(target_language)
    if not code:
        return None
    try:
        module = importlib.import_module(f"app.data.{code}.lesson_seeds")
        getter = getattr(module, "get_lesson_seed", None)
        if getter is None:
            return None
        seed = getter(cefr_level, unit_id, lesson_type)
        if seed is not None:
            return dict(seed)
    except (ImportError, ModuleNotFoundError, AttributeError):
        return None
    return None


def _find_unit(target_language: str, level: str, unit_id: str) -> Any | None:
    curriculum = get_curriculum(target_language)
    for unit in curriculum.get(str(level).upper(), []):
        if unit.id == str(unit_id):
            return unit
    return None


def _grammar_for_unit(target_language: str, level: str, unit: Any | None) -> list[Any]:
    topics = get_grammar_topics(target_language)
    by_slug = {topic.slug: topic for topic in topics}
    selected = [by_slug[slug] for slug in (unit.grammar_points if unit else []) if slug in by_slug]
    return (selected or [topic for topic in topics if topic.level == str(level).upper()])[:4]


def _vocabulary_for_unit(target_language: str, level: str, unit: Any | None) -> list[Any]:
    sets = get_vocabulary_sets(target_language)
    by_id = {item.id: item for item in sets}
    selected = [by_id[item_id] for item_id in (unit.vocabulary_set_ids if unit else []) if item_id in by_id]
    return (selected or [item for item in sets if item.level == str(level).upper()])[:3]


def get_foundation_lesson_seed(
    target_language: str,
    cefr_level: str,
    unit_id: str,
    lesson_type: str,
) -> dict[str, Any] | None:
    """Return curated language material first, then foundation-derived material."""
    level = str(cefr_level).upper()
    skill = str(lesson_type).lower()
    if level not in {"A1", "A2", "B1", "B2", "C1", "C2"}:
        return None

    curated = _curated_seed(target_language, level, unit_id, skill)
    if curated is not None:
        return curated

    if not _foundation_available(target_language):
        return None

    unit = _find_unit(target_language, level, unit_id)
    if unit is None:
        return None

    grammar = _grammar_for_unit(target_language, level, unit)
    vocabulary = _vocabulary_for_unit(target_language, level, unit)
    if not grammar and not vocabulary:
        return None

    title = str(unit.title)
    grammar_examples = [
        example.text for topic in grammar for example in topic.examples[:2]
    ][:6]
    words = [
        (word.word, word.definition, word.example)
        for vocab_set in vocabulary
        for word in vocab_set.words[:5]
    ][:12]
    vocabulary_examples = [item[2] for item in words if item[2]][:6]
    vocabulary_words = [item[0] for item in words][:8]
    source_text = " ".join((grammar_examples[:3] + vocabulary_examples[:3])).strip() or title
    grammar_names = [topic.title for topic in grammar]
    competencies = list(getattr(unit, "competency_checklist", []) or [])[:4]

    phrases: list[str] = []
    try:
        from app.data.phrasebook import get_phrasebook_categories
        for category in get_phrasebook_categories(target_language):
            if str(category.level).upper() != level:
                continue
            for phrase in category.phrases:
                if phrase.text not in phrases:
                    phrases.append(phrase.text)
                if len(phrases) >= 6:
                    break
            if len(phrases) >= 6:
                break
    except (ImportError, AttributeError):
        phrases = []

    # Keep the fallback seed teachable rather than merely exposing raw data.
    # These fields give every generated lesson a small input -> retrieval ->
    # production sequence even when a language has no curated lesson seed yet.
    target_words = vocabulary_words[:6]
    target_phrases = phrases[:4]
    input_examples = (grammar_examples[:3] + vocabulary_examples[:3])[:6]
    content_quality = {
        "input_examples": input_examples,
        "target_words": target_words,
        "target_phrases": target_phrases,
        "meaning_check": [
            "Explain the meaning of two target items using the lesson context.",
            "Choose the target item that best fits a new situation and explain why.",
        ],
        "controlled_practice": [
            "Complete one short task using the target language with the model available.",
            "Change one detail in the model and produce a new, accurate sentence.",
        ],
        "retrieval_sequence": [
            "Recall the meaning of three target items without looking.",
            "Use two target items in new sentences.",
            "Complete the final task using the target grammar or skill.",
        ],
        "transfer_task": f"Apply the target language to a new situation related to {title}, without copying the model.",
        "production_requirement": "Use at least three target words and one target structure in a new context.",
        "reflection_prompt": "Identify one language choice you can reuse in a similar real-life situation.",
        "error_check": [
            "Review one answer for meaning, grammar, and word choice before moving on.",
            "Correct one deliberate or noticed mistake and explain the correction briefly.",
        ],
        "level_calibration": {
            "A1": "Use short, highly familiar language with clear models and concrete situations.",
            "A2": "Combine familiar language in practical situations and add simple reasons or details.",
            "B1": "Connect ideas independently, handle everyday variation, and justify basic choices.",
            "B2": "Express precise relationships between ideas, handle less predictable situations, and support claims.",
            "C1": "Adapt register and structure to context, distinguish subtle meanings, and justify language choices.",
            "C2": "Handle nuanced meaning, formal or specialised contexts, and precise stylistic choices.",
        }[level],
        "spaced_retrieval": [
            "Revisit the same target items later in the lesson without showing the answer first.",
            "Revisit them in the next related lesson with a changed context.",
            "Check delayed recall again after several lessons before introducing extra load.",
        ],
        "input_design": {
            "A1": "Prefer short, concrete examples with one main meaning at a time.",
            "A2": "Use familiar situations with a small amount of variation and clear context.",
            "B1": "Use connected examples that require learners to infer meaning from context.",
            "B2": "Use varied contexts, collocations, and distinctions between near-synonyms.",
            "C1": "Use authentic-looking contexts with register, implication, and nuanced distinctions.",
            "C2": "Use demanding contexts where precision, stance, register, and subtle meaning matter.",
        }[level],
    }

    base: dict[str, Any] = {
        "title": title,
        "objective": f"Build {target_language} {level} skills around {title}.",
        "grammar": [topic.slug for topic in grammar],
        "words": words,
        "vocabulary_words": vocabulary_words,
        "examples": grammar_examples,
        "source": "language_foundation",
        "can_do": competencies,
        "success_criteria": [
            "Use the target language naturally in the unit context.",
            f"Reuse at least three target words from {title}.",
            "Show accurate use of the lesson's target structure or skill.",
        ],
        "recycle": vocabulary_words[:4] + phrases[:2],
        "phrases": phrases,
        "content_quality": content_quality,
    }

    if skill == "grammar":
        base["objective"] = f"Use the target grammar for {title} at {level} level."
        base["scenario"] = f"Complete a short real-life interaction related to {title} using the target structure."
    elif skill == "vocabulary":
        base["objective"] = f"Use topic vocabulary for {title} at {level} level."
        base["scenario"] = f"Use the new vocabulary to solve a practical task about {title}."
    elif skill == "reading":
        base["objective"] = f"Read and understand a short text about {title}."
        base["text"] = source_text
        base["questions"] = [
            f"Identify the main topic of the text: {title}.",
            "Find two useful expressions in the text.",
            "Explain one detail using your own words.",
            "Use one target word from the text in a new sentence.",
        ]
        base["scenario"] = f"Read the text and then use its information to complete a short task about {title}."
        base["retrieval_prompts"] = ["What is the main idea?", "Which two words or phrases do you remember?", "What can you say about the topic without looking?"]
    elif skill == "listening":
        base["objective"] = f"Understand key information about {title} in connected speech."
        base["transcript"] = source_text
        base["questions"] = [
            "Identify the main idea you hear.",
            "Note two useful expressions from the recording.",
            "Give one detail that supports the main idea.",
            "Repeat one useful phrase and adapt it to your own situation.",
        ]
        base["scenario"] = f"Listen for information you would need in a real interaction about {title}."
        base["retrieval_prompts"] = ["What was the main idea?", "Which detail did you hear?", "Which phrase could you reuse?"]
    elif skill == "speaking":
        base["objective"] = f"Speak about {title} using the target grammar and vocabulary."
        base["prompt"] = f"Speak about {title}. Use the target grammar and at least three topic words, then answer one follow-up question."
        base["phrases"] = (grammar_examples + vocabulary_examples)[:6]
        base["examples"] = grammar_examples[:2]
        base["scenario"] = f"Role-play a short conversation about {title} and respond without reading a model."
        base["retrieval_prompts"] = ["Say one target sentence from memory.", "Use two topic words in a new sentence.", "Respond to a realistic follow-up question."]
    elif skill == "writing":
        base["objective"] = f"Write a connected text about {title} with accurate grammar and vocabulary."
        base["prompt"] = f"Write a short text about {title} using the target grammar and vocabulary."
        base["guidance"] = [
            f"Use at least one structure from: {', '.join(grammar_names[:3])}.",
            "Use at least three topic vocabulary items.",
            "Connect your ideas with complete sentences.",
        ]
        base["examples"] = grammar_examples[:2]
        base["scenario"] = f"Write a useful message or short response connected to {title}."
        base["retrieval_prompts"] = ["Recall one target structure.", "Recall three topic words.", "Rewrite one example in a new context."]
    elif skill == "review":
        base["objective"] = f"Review the grammar and vocabulary for {title}."
        base["questions"] = [
            f"Use one target structure from {', '.join(grammar_names[:3])}.",
            f"Write two sentences about {title} using topic vocabulary.",
            "Explain one difference between two expressions from the lesson.",
        ]
        base["scenario"] = f"Complete a mixed retrieval task that combines earlier language from {title}; do not introduce a new grammar point."
        base["retrieval_prompts"] = ["Recall the core structure.", "Use three target words without looking.", "Explain one common mistake and how to avoid it."]
    else:
        return None

    return base

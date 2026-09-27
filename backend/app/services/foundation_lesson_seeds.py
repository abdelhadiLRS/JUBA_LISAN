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

    base: dict[str, Any] = {
        "title": title,
        "objective": f"Build {target_language} {level} skills around {title}.",
        "grammar": [topic.slug for topic in grammar],
        "words": words,
        "vocabulary_words": vocabulary_words,
        "examples": grammar_examples,
        "source": "language_foundation",
    }

    if skill == "grammar":
        base["objective"] = f"Use the target grammar for {title} at {level} level."
    elif skill == "vocabulary":
        base["objective"] = f"Use topic vocabulary for {title} at {level} level."
    elif skill == "reading":
        base["objective"] = f"Read and understand a short text about {title}."
        base["text"] = source_text
        base["questions"] = [
            f"Identify the main topic of the text: {title}.",
            "Find two useful expressions in the text.",
            "Explain one detail using your own words.",
        ]
    elif skill == "listening":
        base["objective"] = f"Understand key information about {title} in connected speech."
        base["transcript"] = source_text
        base["questions"] = [
            "Identify the main idea you hear.",
            "Note two useful expressions from the recording.",
            "Give one detail that supports the main idea.",
        ]
    elif skill == "speaking":
        base["objective"] = f"Speak about {title} using the target grammar and vocabulary."
        base["prompt"] = f"Speak about {title}. Use the target grammar and at least three topic words."
        base["phrases"] = (grammar_examples + vocabulary_examples)[:6]
        base["examples"] = grammar_examples[:2]
    elif skill == "writing":
        base["objective"] = f"Write a connected text about {title} with accurate grammar and vocabulary."
        base["prompt"] = f"Write a short text about {title} using the target grammar and vocabulary."
        base["guidance"] = [
            f"Use at least one structure from: {', '.join(grammar_names[:3])}.",
            "Use at least three topic vocabulary items.",
            "Connect your ideas with complete sentences.",
        ]
        base["examples"] = grammar_examples[:2]
    elif skill == "review":
        base["objective"] = f"Review the grammar and vocabulary for {title}."
        base["questions"] = [
            f"Use one target structure from {', '.join(grammar_names[:3])}.",
            f"Write two sentences about {title} using topic vocabulary.",
            "Explain one difference between two expressions from the lesson.",
        ]
    else:
        return None

    return base

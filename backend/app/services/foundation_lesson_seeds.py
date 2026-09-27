"""Runtime lesson seeds derived from the authored language foundations.

This adapter turns the broad A1-C2 foundation datasets into deterministic lesson
material for languages that do not yet have a hand-curated lesson_seeds.py file.
Curated seeds always take precedence in the lesson generator.
"""
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


def _find_unit(target_language: str, level: str, unit_id: str) -> Any | None:
    curriculum = get_curriculum(target_language)
    wanted = str(unit_id)
    for unit in curriculum.get(str(level).upper(), []):
        if unit.id == wanted:
            return unit
    return None


def _grammar_for_unit(target_language: str, level: str, unit: Any | None) -> list[Any]:
    topics = get_grammar_topics(target_language)
    by_slug = {topic.slug: topic for topic in topics}
    selected = [by_slug[slug] for slug in (unit.grammar_points if unit else []) if slug in by_slug]
    if selected:
        return selected[:4]
    return [topic for topic in topics if topic.level == str(level).upper()][:4]


def _vocabulary_for_unit(target_language: str, level: str, unit: Any | None) -> list[Any]:
    sets = get_vocabulary_sets(target_language)
    by_id = {item.id: item for item in sets}
    selected = [by_id[item_id] for item_id in (unit.vocabulary_set_ids if unit else []) if item_id in by_id]
    if selected:
        return selected[:3]
    return [item for item in sets if item.level == str(level).upper()][:3]


def get_foundation_lesson_seed(
    target_language: str,
    cefr_level: str,
    unit_id: str,
    lesson_type: str,
) -> dict[str, Any] | None:
    """Build a runtime lesson seed from a language foundation, if available."""
    level = str(cefr_level).upper()
    skill = str(lesson_type).lower()
    if level not in {"A1", "A2", "B1", "B2", "C1", "C2"} or not _foundation_available(target_language):
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
        example.text
        for topic in grammar
        for example in topic.examples[:2]
    ][:6]
    words = [
        (word.word, word.definition, word.example)
        for vocab_set in vocabulary
        for word in vocab_set.words[:5]
    ][:12]
    grammar_names = [topic.title for topic in grammar]

    base: dict[str, Any] = {
        "title": title,
        "objective": f"Build {target_language} {level} skills around {title}.",
        "grammar": [topic.slug for topic in grammar],
        "words": words,
        "examples": grammar_examples,
    }

    if skill == "grammar":
        base["objective"] = f"Use the target grammar for {title} at {level} level."
        base["examples"] = grammar_examples
    elif skill == "vocabulary":
        base["objective"] = f"Use topic vocabulary for {title} at {level} level."
    elif skill == "reading":
        base["text"] = " ".join(grammar_examples[:4])
        base["questions"] = [
            f"What grammar point is illustrated in the text?",
            f"Which vocabulary items relate to {title}?",
        ]
    elif skill == "listening":
        base["transcript"] = " ".join(grammar_examples[:4])
        base["questions"] = [
            "Which key idea can you identify?",
            f"Which expression relates to {title}?",
        ]
    elif skill == "speaking":
        base["prompt"] = f"Speak about {title}. Use the target grammar and at least three topic words."
        base["phrases"] = grammar_examples[:4]
        base["examples"] = grammar_examples[:2]
    elif skill == "writing":
        base["prompt"] = f"Write a short text about {title} using the target grammar and vocabulary."
        base["guidance"] = [
            f"Use at least one structure from: {', '.join(grammar_names[:3])}.",
            "Use at least three topic vocabulary items.",
        ]
        base["examples"] = grammar_examples[:2]
    elif skill == "review":
        base["questions"] = [
            f"Use one target structure from {', '.join(grammar_names[:3])}.",
            f"Write two sentences about {title} using topic vocabulary.",
            "Explain one difference between two expressions from the lesson.",
        ]
    else:
        return None

    return base

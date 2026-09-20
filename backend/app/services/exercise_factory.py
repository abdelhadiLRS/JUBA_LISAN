from __future__ import annotations

from copy import deepcopy
from typing import Any


# Canonical exercise variants. The factory changes interaction, not language content.
VARIANT_ALIASES = {
    "choice": "multiple_choice",
    "mcq": "multiple_choice",
    "translation": "translate",
    "gap": "fill_blank",
    "writing": "free_write",
}


def _normalise_type(value: str) -> str:
    return VARIANT_ALIASES.get(value.strip().lower(), value.strip().lower())


def build_exercise_variants(
    source: dict[str, Any],
    *,
    variants: list[str] | None = None,
    max_variants: int = 4,
) -> list[dict[str, Any]]:
    """Project one canonical content item into deterministic exercise variants.

    The source object remains the single source of truth. Variants only alter
    interaction metadata/options; they must never invent a different answer.
    """
    if max_variants < 1:
        return []

    canonical = deepcopy(source)
    correct = str(canonical.get("correct") or canonical.get("translation") or "").strip()
    question = str(canonical.get("question") or canonical.get("example") or "").strip()
    content_id = str(canonical.get("content_id") or "").strip()

    if not correct or not question:
        raise ValueError("source content requires question/example and correct/translation")
    if not content_id:
        raise ValueError("source content requires a stable content_id")

    requested = variants or [
        "multiple_choice",
        "translate",
        "fill_blank",
        "free_write",
    ]
    output: list[dict[str, Any]] = []
    seen: set[str] = set()

    for raw_type in requested:
        exercise_type = _normalise_type(raw_type)
        if exercise_type in seen or len(output) >= max_variants:
            continue

        item = {
            "type": exercise_type,
            "question": question,
            "correct": correct,
            "content_id": content_id,
            "variant": exercise_type,
        }
        for key in (
            "explanation",
            "native_explanation",
            "native_hint",
            "accepted_answers",
            "metadata",
        ):
            if key in canonical and canonical[key] is not None:
                item[key] = deepcopy(canonical[key])

        if exercise_type == "multiple_choice":
            options = [str(x).strip() for x in canonical.get("options", []) if str(x).strip()]
            if correct not in options:
                options.insert(0, correct)
            if len(options) < 2:
                continue
            item["options"] = options

        elif exercise_type == "fill_blank":
            item["question"] = _make_gap(question, correct)

        elif exercise_type == "free_write":
            item["metadata"] = {"source": "canonical_content"}

        else:
            item["metadata"] = {"source": "canonical_content"}

        output.append(item)
        seen.add(exercise_type)

    return output


def _make_gap(question: str, correct: str) -> str:
    if "___" in question:
        return question
    if correct and correct in question:
        return question.replace(correct, "___", 1)
    return f"{question} ___"


def build_persisted_exercise_variants(
    source_exercises: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Expand generated lesson exercises conservatively for richer practice.

    Each source exercise remains the canonical content item. We keep its
    original interaction and add at most one deterministic alternate:
    multiple-choice -> translation, fill-blank -> free-write. Other types
    remain one-to-one until their dedicated interaction is implemented.
    """
    output: list[dict[str, Any]] = []

    for source in source_exercises:
        source_type = _normalise_type(str(source.get("type") or "multiple_choice"))
        alternate = {
            "multiple_choice": "translate",
            "fill_blank": "free_write",
        }.get(source_type)

        requested = [source_type]
        if alternate:
            requested.append(alternate)

        variants = build_exercise_variants(
            source,
            variants=requested,
            max_variants=2,
        )
        output.extend(variants)

    return output

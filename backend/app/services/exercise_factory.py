from __future__ import annotations

import hashlib
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


def _stable_distractors(
    source: dict[str, Any],
    candidates: list[str],
    *,
    max_options: int = 4,
) -> list[str]:
    """Return deterministic distractors from canonical sibling answers.

    Only answers already present in the lesson are eligible. The correct answer
    and accepted answers are excluded, and ordering is stable for a given
    content_id/candidate set.
    """
    correct = str(source.get("correct") or source.get("translation") or "").strip()
    accepted = {
        str(answer).strip().casefold()
        for answer in (source.get("accepted_answers") or [])
        if str(answer).strip()
    }
    excluded = accepted | ({correct.casefold()} if correct else set())
    unique = {}
    for candidate in candidates:
        value = str(candidate).strip()
        key = value.casefold()
        if value and key not in excluded:
            unique[key] = value

    seed = str(source.get("content_id") or "")
    ranked = sorted(
        unique.values(),
        key=lambda value: hashlib.sha256(f"{seed}\0{value}".encode("utf-8")).hexdigest(),
    )
    return ranked[: max(0, max_options - 1)]


def _ensure_multiple_choice_options(
    source: dict[str, Any],
    candidates: list[str] | None = None,
) -> list[str]:
    correct = str(source.get("correct") or source.get("translation") or "").strip()
    options = [str(x).strip() for x in source.get("options", []) if str(x).strip()]
    if correct and correct not in options:
        options.insert(0, correct)
    if len(options) < 4 and candidates:
        options.extend(
            _stable_distractors(
                source,
                candidates,
                max_options=4,
            )
        )
    # De-duplicate while preserving the canonical/source order.
    seen: set[str] = set()
    result: list[str] = []
    for option in options:
        key = option.casefold()
        if key in seen:
            continue
        seen.add(key)
        result.append(option)
    return result[:4]


def build_exercise_variants(
    source: dict[str, Any],
    *,
    variants: list[str] | None = None,
    max_variants: int = 4,
    distractor_candidates: list[str] | None = None,
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
            options = _ensure_multiple_choice_options(
                canonical,
                distractor_candidates,
            )
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

    For multiple-choice items, missing options are filled only from correct
    answers of sibling canonical exercises in the same lesson. This keeps
    distractors deterministic and prevents fabricated answer content.
    """
    sibling_answers = [
        str(source.get("correct") or source.get("translation") or "").strip()
        for source in source_exercises
    ]
    output: list[dict[str, Any]] = []

    for source in source_exercises:
        source_type = _normalise_type(str(source.get("type") or "multiple_choice"))
        alternate = {
            "multiple_choice": "translate",
            "fill_blank": "free_write",
        }.get(source_type)

        canonical = deepcopy(source)
        if source_type == "multiple_choice":
            canonical["options"] = _ensure_multiple_choice_options(
                canonical,
                sibling_answers,
            )

        requested = [source_type]
        if alternate:
            requested.append(alternate)

        variants = build_exercise_variants(
            canonical,
            variants=requested,
            max_variants=2,
            distractor_candidates=sibling_answers,
        )
        output.extend(variants)

    return output

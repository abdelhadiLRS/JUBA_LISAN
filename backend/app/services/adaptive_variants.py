from __future__ import annotations

from collections.abc import Callable, Collection, Sequence
import math
from typing import TypeVar

from app.services.exercise_retry import (
    classify_score,
    get_retry_variant,
    normalise_variant,
)

ExerciseT = TypeVar("ExerciseT")

MASTERY_STRUGGLING_THRESHOLD = 0.50
MASTERY_REQUIRED_SCORE = 0.80
MASTERY_REQUIRED_VARIANTS = 2


def _get_attr(name: str) -> Callable[[object], object]:
    return lambda exercise: getattr(exercise, name, None)


def _normalise_exercise_id(value: object) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        return None
    return value


def _normalise_attempted_exercise_ids(
    values: Collection[object] | None,
) -> set[int]:
    return {
        exercise_id
        for value in values or set()
        if (exercise_id := _normalise_exercise_id(value)) is not None
    }


def collect_attempted_exercise_ids(
    attempts: Sequence[object],
    *,
    get_exercise_id: Callable[[object], object] = _get_attr("exercise_id"),
) -> set[int]:
    """Return valid exercise ids represented in persisted attempt history."""
    attempted: set[int] = set()
    for attempt in attempts:
        exercise_id = _normalise_exercise_id(get_exercise_id(attempt))
        if exercise_id is not None:
            attempted.add(exercise_id)
    return attempted


def _normalise_content_id(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def _normalise_attempted_adaptive_identities(
    values: Collection[object] | None,
) -> set[tuple[str, str]]:
    identities: set[tuple[str, str]] = set()
    for value in values or set():
        if not isinstance(value, (tuple, list)) or len(value) != 2:
            continue
        content_id = _normalise_content_id(value[0])
        raw_variant = value[1]
        variant = normalise_variant(raw_variant if isinstance(raw_variant, str) else None)
        if content_id and variant:
            identities.add((content_id, variant))
    return identities


def collect_attempted_adaptive_identities(
    attempts: Sequence[object],
    *,
    get_content_id: Callable[[object], object] = _get_attr("content_id"),
    get_variant: Callable[[object], object] = _get_attr("variant"),
) -> set[tuple[str, str]]:
    """Return canonical content/variant identities represented in attempt history."""
    attempted: set[tuple[str, str]] = set()
    for attempt in attempts:
        content_id = _normalise_content_id(get_content_id(attempt))
        raw_variant = get_variant(attempt)
        variant = normalise_variant(raw_variant if isinstance(raw_variant, str) else None)
        if content_id and variant:
            attempted.add((content_id, variant))
    return attempted


def summarize_adaptive_mastery(
    attempts: Sequence[object],
    *,
    content_id: str,
    get_content_id: Callable[[object], object] = _get_attr("content_id"),
    get_variant: Callable[[object], object] = _get_attr("variant"),
    get_score: Callable[[object], object] = _get_attr("score"),
) -> tuple[float, str, int]:
    """Summarize mastery from the best score achieved on each distinct variant."""
    normalized_content_id = _normalise_content_id(content_id)
    if not normalized_content_id:
        return 0.0, "unseen", 0

    best_by_variant: dict[str, float] = {}
    for attempt in attempts:
        candidate_content_id = _normalise_content_id(get_content_id(attempt))
        if candidate_content_id != normalized_content_id:
            continue
        raw_variant = get_variant(attempt)
        variant = normalise_variant(raw_variant if isinstance(raw_variant, str) else None)
        if not variant:
            continue
        try:
            score = _normalise_score(get_score(attempt))
        except (TypeError, ValueError):
            continue
        best_by_variant[variant] = max(best_by_variant.get(variant, 0.0), score)

    if not best_by_variant:
        return 0.0, "unseen", 0

    mastery_score = sum(best_by_variant.values()) / len(best_by_variant)
    covered_variants = len(best_by_variant)
    if (
        mastery_score >= MASTERY_REQUIRED_SCORE
        and covered_variants >= MASTERY_REQUIRED_VARIANTS
    ):
        state = "mastered"
    elif mastery_score < MASTERY_STRUGGLING_THRESHOLD:
        state = "struggling"
    else:
        state = "learning"
    return round(mastery_score, 3), state, covered_variants


def select_unanswered_variant(
    exercises: Sequence[ExerciseT],
    *,
    content_id: str,
    current_variant: str | None,
    succeeded: bool,
    attempted_exercise_ids: Collection[object] | None = None,
    attempted_adaptive_identities: Collection[object] | None = None,
    get_exercise_id: Callable[[ExerciseT], object] = _get_attr("id"),
    get_variant: Callable[[ExerciseT], object] = _get_attr("variant"),
    get_content_id: Callable[[ExerciseT], object] = _get_attr("content_id"),
) -> ExerciseT | None:
    """Select the adjacent unanswered variant for one stable content identity.

    The selector is independent of SQLAlchemy. Callers that keep variant/content
    metadata in lesson JSON can provide callbacks that read that metadata while
    still sharing the same retry/adaptive candidate rules.
    """
    normalized_content_id = content_id.strip()
    if not normalized_content_id:
        return None

    attempted = _normalise_attempted_exercise_ids(attempted_exercise_ids)
    attempted_identities = _normalise_attempted_adaptive_identities(
        attempted_adaptive_identities
    )
    candidates: list[tuple[ExerciseT, str]] = []
    available_variants: list[str] = []

    for exercise in exercises:
        candidate_content_id = str(get_content_id(exercise) or "").strip()
        if candidate_content_id != normalized_content_id:
            continue

        raw_variant = get_variant(exercise)
        variant = normalise_variant(raw_variant if isinstance(raw_variant, str) else None)
        if not variant:
            continue
        available_variants.append(variant)

        exercise_id = _normalise_exercise_id(get_exercise_id(exercise))
        identity = (normalized_content_id, variant)
        if (
            exercise_id is None
            or exercise_id in attempted
            or identity in attempted_identities
        ):
            continue
        candidates.append((exercise, variant))

    target_variant = get_retry_variant(
        current_variant,
        succeeded=succeeded,
        available_variants=available_variants,
    )
    if not target_variant:
        return None

    return next(
        (exercise for exercise, variant in candidates if variant == target_variant),
        None,
    )


def _normalise_score(score: object) -> float:
    """Coerce finite runtime score values before applying the shared score policy."""
    if isinstance(score, bool):
        raise ValueError("score must be numeric")
    normalized = float(score)
    if not math.isfinite(normalized):
        raise ValueError("score must be finite")
    return normalized


def recommend_adaptive_action(
    score: object,
    current_variant: str | None,
    available_variants: Collection[object] | None = None,
) -> tuple[str, str | None]:
    """Return an adaptive action and optional variant without requiring exercise rows."""
    classification = classify_score(_normalise_score(score))
    if classification == "middle":
        return "reinforce", None

    variant = get_retry_variant(
        current_variant,
        succeeded=classification == "success",
        available_variants=list(available_variants or ()),
    )
    if variant is None:
        return ("advance", None) if classification == "success" else ("reinforce", None)

    action = "advance_harder" if classification == "success" else "retry_easier"
    return action, variant


def recommend_adaptive_variant(
    exercises: Sequence[ExerciseT],
    *,
    content_id: str,
    current_variant: str | None,
    score: object,
    attempted_exercise_ids: Collection[object] | None = None,
    attempted_adaptive_identities: Collection[object] | None = None,
    attempt_history: Sequence[object] | None = None,
    get_exercise_id: Callable[[ExerciseT], object] = _get_attr("id"),
    get_variant: Callable[[ExerciseT], object] = _get_attr("variant"),
    get_content_id: Callable[[ExerciseT], object] = _get_attr("content_id"),
) -> tuple[str, str | None, ExerciseT | None]:
    """Return one adaptive action and its unanswered target.

    Score classification is delegated to the shared retry policy so endpoint
    callers cannot drift from the canonical 0.50/0.80 boundaries.
    """
    classification = classify_score(_normalise_score(score))
    if classification == "middle":
        mastery_score, mastery_state, _covered_variants = summarize_adaptive_mastery(
            attempt_history or (),
            content_id=content_id,
        )
        if mastery_state == "mastered" and mastery_score >= MASTERY_REQUIRED_SCORE:
            return "advance", None, None
        return "reinforce", None, None

    target = select_unanswered_variant(
        exercises,
        content_id=content_id,
        current_variant=current_variant,
        succeeded=classification == "success",
        attempted_exercise_ids=attempted_exercise_ids,
        attempted_adaptive_identities=attempted_adaptive_identities,
        get_exercise_id=get_exercise_id,
        get_variant=get_variant,
        get_content_id=get_content_id,
    )
    if target is None:
        return ("advance", None, None) if classification == "success" else ("reinforce", None, None)

    raw_target_variant = get_variant(target)
    target_variant = normalise_variant(
        raw_target_variant if isinstance(raw_target_variant, str) else None
    )
    if not target_variant:
        return ("advance", None, None) if classification == "success" else ("reinforce", None, None)

    action = "advance_harder" if classification == "success" else "retry_easier"
    return action, target_variant, target

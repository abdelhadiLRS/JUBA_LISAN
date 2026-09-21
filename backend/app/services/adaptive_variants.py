from __future__ import annotations

from collections.abc import Callable, Collection, Sequence
from typing import TypeVar

from app.services.exercise_retry import (
    classify_score,
    get_retry_variant,
    normalise_variant,
)

ExerciseT = TypeVar("ExerciseT")


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


def select_unanswered_variant(
    exercises: Sequence[ExerciseT],
    *,
    content_id: str,
    current_variant: str | None,
    succeeded: bool,
    attempted_exercise_ids: Collection[object] | None = None,
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
        if exercise_id is None or exercise_id in attempted:
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
    """Coerce runtime score values before applying the shared score policy."""
    return float(score)


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
        return "reinforce", None, None

    target = select_unanswered_variant(
        exercises,
        content_id=content_id,
        current_variant=current_variant,
        succeeded=classification == "success",
        attempted_exercise_ids=attempted_exercise_ids,
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

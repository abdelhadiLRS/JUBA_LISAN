from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TypeVar

from app.services.exercise_retry import (
    classify_score,
    get_retry_variant,
    normalise_variant,
)

ExerciseT = TypeVar("ExerciseT")


def _get_attr(name: str) -> Callable[[object], object]:
    return lambda exercise: getattr(exercise, name, None)


def collect_attempted_exercise_ids(
    attempts: Sequence[object],
    *,
    get_exercise_id: Callable[[object], object] = _get_attr("exercise_id"),
) -> set[int]:
    """Return valid exercise ids represented in persisted attempt history."""
    attempted: set[int] = set()
    for attempt in attempts:
        exercise_id = get_exercise_id(attempt)
        if isinstance(exercise_id, int) and not isinstance(exercise_id, bool) and exercise_id > 0:
            attempted.add(exercise_id)
    return attempted


def select_unanswered_variant(
    exercises: Sequence[ExerciseT],
    *,
    content_id: str,
    current_variant: str | None,
    succeeded: bool,
    attempted_exercise_ids: set[int] | None = None,
    get_exercise_id: Callable[[ExerciseT], int] = _get_attr("id"),
    get_variant: Callable[[ExerciseT], object] = _get_attr("variant"),
    get_content_id: Callable[[ExerciseT], object] = _get_attr("content_id"),
) -> ExerciseT | None:
    """Select the adjacent unanswered variant for one stable content identity.

    The selector is independent of SQLAlchemy. Callers that keep variant/content
    metadata in lesson JSON can provide callbacks that read that metadata while
    still sharing the same retry/adaptive candidate rules.
    """
    if not content_id.strip():
        return None

    attempted = attempted_exercise_ids or set()
    candidates: list[tuple[ExerciseT, str]] = []
    available_variants: list[str] = []

    for exercise in exercises:
        if str(get_content_id(exercise) or "") != content_id:
            continue

        raw_variant = get_variant(exercise)
        variant = normalise_variant(raw_variant if isinstance(raw_variant, str) else None)
        if not variant:
            continue
        available_variants.append(variant)

        if get_exercise_id(exercise) in attempted:
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


def recommend_adaptive_variant(
    exercises: Sequence[ExerciseT],
    *,
    content_id: str,
    current_variant: str | None,
    score: float,
    attempted_exercise_ids: set[int] | None = None,
    get_exercise_id: Callable[[ExerciseT], int] = _get_attr("id"),
    get_variant: Callable[[ExerciseT], object] = _get_attr("variant"),
    get_content_id: Callable[[ExerciseT], object] = _get_attr("content_id"),
) -> tuple[str, str | None, ExerciseT | None]:
    """Return one adaptive action and its unanswered target.

    Score classification is delegated to the shared retry policy so endpoint
    callers cannot drift from the canonical 0.50/0.80 boundaries.
    """
    classification = classify_score(score)
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

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

from app.services.exercise_retry import get_retry_variant, normalise_variant

ExerciseT = TypeVar("ExerciseT")


def select_unanswered_variant(
    exercises: Sequence[ExerciseT],
    *,
    content_id: str,
    current_variant: str | None,
    succeeded: bool,
    attempted_exercise_ids: set[int] | None = None,
    get_exercise_id=lambda exercise: exercise.id,
    get_variant=lambda exercise: exercise.variant,
    get_content_id=lambda exercise: exercise.content_id,
) -> ExerciseT | None:
    """Select the adjacent unanswered variant for one stable content identity.

    The selector is intentionally independent of SQLAlchemy so retry and adaptive
    progression can share identical candidate semantics at the router boundary.
    """
    if not content_id.strip():
        return None

    attempted = attempted_exercise_ids or set()
    candidates: list[tuple[ExerciseT, str]] = []
    available_variants: list[str] = []

    for exercise in exercises:
        if str(get_content_id(exercise) or "") != content_id:
            continue

        variant = normalise_variant(get_variant(exercise))
        if not variant:
            continue
        available_variants.append(variant)

        exercise_id = get_exercise_id(exercise)
        if exercise_id in attempted:
            continue
        candidates.append((exercise, variant))

    target_variant = get_retry_variant(
        current_variant,
        succeeded=succeeded,
        available_variants=available_variants,
    )
    if not target_variant:
        return None

    for exercise, variant in candidates:
        if variant == target_variant:
            return exercise
    return None

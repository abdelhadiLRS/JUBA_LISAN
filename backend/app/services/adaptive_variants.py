from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TypeVar

from app.services.exercise_retry import get_retry_variant, normalise_variant

ExerciseT = TypeVar("ExerciseT")


def _get_attr(name: str) -> Callable[[object], object]:
    return lambda exercise: getattr(exercise, name, None)


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

        variant = normalise_variant(
            get_variant(exercise) if isinstance(get_variant(exercise), str) else None
        )
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

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

from app.services.adaptive_variants import summarize_adaptive_mastery


@dataclass(frozen=True)
class LessonMasteryCandidate:
    exercise: object
    mastery_score: float
    mastery_state: str
    mastery_variants: int


def select_next_mastery_candidate(
    exercises: Sequence[object],
    attempts: Sequence[object],
    *,
    get_content_id: Callable[[object], object],
    get_exercise_id: Callable[[object], object],
) -> LessonMasteryCandidate | None:
    """Select the lowest-priority mastery target without returning mastered items."""
    state_priority = {"struggling": 0, "unseen": 1, "learning": 2, "mastered": 3}
    selected: tuple[tuple[int, float, int], LessonMasteryCandidate] | None = None

    for exercise in exercises:
        raw_content_id = get_content_id(exercise)
        content_id = raw_content_id.strip() if isinstance(raw_content_id, str) else ""
        score, state, variants = summarize_adaptive_mastery(
            attempts,
            content_id=content_id,
        )
        if state == "mastered":
            continue
        raw_id = get_exercise_id(exercise)
        exercise_id = raw_id if isinstance(raw_id, int) and not isinstance(raw_id, bool) else 0
        candidate = LessonMasteryCandidate(exercise, score, state, variants)
        key = (state_priority.get(state, 2), score, exercise_id)
        if selected is None or key < selected[0]:
            selected = (key, candidate)

    return selected[1] if selected is not None else None


@dataclass(frozen=True)
class LessonMasteryAggregate:
    total_exercises: int
    attempted_exercises: int
    mastered_exercises: int
    learning_exercises: int
    struggling_exercises: int
    unseen_exercises: int
    average_mastery_score: float
    attempt_rate: float
    mastery_rate: float
    covered_variants: int


def summarize_lesson_mastery(
    exercises: Sequence[object],
    attempts: Sequence[object],
    *,
    get_content_id: Callable[[object], object],
) -> LessonMasteryAggregate:
    total = len(exercises)
    scores: list[float] = []
    covered_variants = 0
    mastered = learning = struggling = unseen = 0

    for exercise in exercises:
        raw_content_id = get_content_id(exercise)
        content_id = raw_content_id.strip() if isinstance(raw_content_id, str) else ""
        score, state, variants = summarize_adaptive_mastery(
            attempts,
            content_id=content_id,
        )
        scores.append(score)
        covered_variants += variants
        if state == "mastered":
            mastered += 1
        elif state == "learning":
            learning += 1
        elif state == "struggling":
            struggling += 1
        else:
            unseen += 1

    attempted = total - unseen
    return LessonMasteryAggregate(
        total_exercises=total,
        attempted_exercises=attempted,
        mastered_exercises=mastered,
        learning_exercises=learning,
        struggling_exercises=struggling,
        unseen_exercises=unseen,
        average_mastery_score=round(sum(scores) / total, 3) if total else 0.0,
        attempt_rate=round(attempted / total, 3) if total else 0.0,
        mastery_rate=round(mastered / total, 3) if total else 0.0,
        covered_variants=covered_variants,
    )

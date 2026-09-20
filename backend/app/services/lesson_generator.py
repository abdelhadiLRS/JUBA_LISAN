import hashlib
import json
import re
from typing import Any

from app.data.curriculum import get_curriculum
from app.schemas.lessons import (
    ExerciseContent,
    FillBlankEvaluation,
    FreeWriteEvaluation,
    LessonContent,
    PronunciationEvaluation,
)
from app.services.language_helpers import get_language_name, get_native_language_name
from app.services.llm_adapter import llm_adapter
from app.services.prompts import lesson as lesson_prompts
from app.services.prompts.common import get_language_prompt_overlay
from app.services.prompts.lesson import (
    build_fill_blank_eval_prompt,
    build_free_write_eval_prompt,
    build_lesson_generation_prompt,
    build_pronunciation_eval_prompt,
    build_regenerate_exercise_prompt,
)

LESSON_GENERATION_PROMPT = lesson_prompts.LESSON_GENERATION_PROMPT
FILL_BLANK_EVAL_PROMPT = lesson_prompts.FILL_BLANK_EVAL_PROMPT
FREE_WRITE_EVAL_PROMPT = lesson_prompts.FREE_WRITE_EVAL_PROMPT
PRONUNCIATION_EVAL_PROMPT = lesson_prompts.PRONUNCIATION_EVAL_PROMPT


def hint_reveals_answer(native_hint: str | None, correct_answer: str | None) -> bool:
    if not native_hint or not correct_answer:
        return False
    hint = native_hint.casefold()
    answers = [part.strip().casefold() for part in correct_answer.split("/")]
    for answer in answers:
        if not answer:
            continue
        if re.search(r"\s", answer) or not answer.replace("'", "").isalnum():
            if answer in hint:
                return True
            continue
        if re.search(rf"(?<!\w){re.escape(answer)}(?!\w)", hint):
            return True
    return False


def _stable_exercise_id(
    *,
    target_language: str,
    cefr_level: str,
    lesson_type: str,
    topic: str,
    unit_id: str,
    index: int,
    exercise: ExerciseContent,
) -> str:
    """Create a deterministic content identity independent of database row IDs."""
    payload = {
        "language": target_language,
        "level": cefr_level,
        "lesson_type": lesson_type,
        "topic": topic.strip().casefold(),
        "unit_id": unit_id,
        "index": index,
        "type": exercise.type,
        "question": exercise.question.strip(),
        "correct": exercise.correct.strip(),
    }
    digest = hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    return f"exercise_{digest}"


def _attach_stable_exercise_metadata(
    lesson: LessonContent,
    *,
    target_language: str,
    topic: str,
    unit_id: str,
) -> None:
    """Add reusable content identity without changing existing exercise semantics."""
    for index, exercise in enumerate(lesson.exercises):
        if not exercise.content_id:
            exercise.content_id = _stable_exercise_id(
                target_language=target_language,
                cefr_level=lesson.cefr_level,
                lesson_type=lesson.lesson_type,
                topic=topic,
                unit_id=unit_id,
                index=index,
                exercise=exercise,
            )
        if not exercise.variant:
            exercise.variant = exercise.type


def get_valid_grammar_slugs(target_language: str = "en-GB") -> set[str]:
    """Return the set of valid grammar slugs for a given target language."""
    curriculum = get_curriculum(target_language)
    return {slug for units in curriculum.values() for unit in units for slug in unit.grammar_points}


async def generate_lesson(
    cefr_level: str,
    lesson_type: str,
    topic: str,
    week: int,
    day: int,
    unit_id: str = "",
    grammar_points: list[str] | None = None,
    vocabulary_set_ids: list[str] | None = None,
    target_language: str = "en-GB",
    native_language: str | None = None,
) -> LessonContent:
    gp_str = ", ".join(grammar_points) if grammar_points else "none specified"
    vs_str = ", ".join(vocabulary_set_ids) if vocabulary_set_ids else "general"
    target_language_name = get_language_name(target_language)
    native_language_name = get_native_language_name(native_language) if native_language else "none"
    language_prompt_overlay = get_language_prompt_overlay(target_language)
    valid_slugs = get_valid_grammar_slugs(target_language)
    valid_slugs_str = ", ".join(sorted(valid_slugs))
    prompt = build_lesson_generation_prompt(
        cefr_level=cefr_level,
        target_language_name=target_language_name,
        native_language_name=native_language_name,
        lesson_type=lesson_type,
        topic=topic,
        unit_id=unit_id or "—",
        grammar_points=gp_str,
        vocabulary_set_ids=vs_str,
        week=week,
        day=day,
        valid_slugs=valid_slugs_str,
        language_prompt_overlay=language_prompt_overlay,
    )

    lesson = await llm_adapter.structured_output(
        [{"role": "system", "content": prompt}],
        LessonContent,
    )
    lesson.grammar_refs = [s for s in lesson.grammar_refs if s in valid_slugs]
    # Sanitize fill_blank exercises: question MUST contain ___ (the gapped sentence).
    # If the LLM put the instruction in question and the actual sentence in explanation,
    # swap them so the user always sees the gapped sentence in the UI.
    for ex in lesson.exercises:
        if ex.type == "fill_blank" and "___" not in ex.question:
            if ex.explanation and "___" in ex.explanation:
                ex.question, ex.explanation = ex.explanation, ex.question
        if hint_reveals_answer(ex.native_hint, ex.correct):
            ex.native_hint = None
    _attach_stable_exercise_metadata(
        lesson,
        target_language=target_language,
        topic=topic,
        unit_id=unit_id,
    )
    return lesson


async def regenerate_exercise(
    *,
    cefr_level: str,
    lesson_type: str,
    topic: str,
    exercise_type: str,
    lesson_explanation: dict[str, Any],
    lesson_vocabulary: list[dict[str, Any]] | None,
    invalid_exercise: dict[str, Any],
    target_language: str = "en-GB",
    native_language: str | None = None,
) -> ExerciseContent:
    target_language_name = get_language_name(target_language)
    native_language_name = get_native_language_name(native_language) if native_language else "none"
    language_prompt_overlay = get_language_prompt_overlay(target_language)
    options_schema = {
        "multiple_choice": '["option 1", "option 2", "option 3", "option 4"]',
        "fill_blank": "null",
        "free_write": '["grading criterion 1", "grading criterion 2"]',
        "pronunciation": '["short pronunciation hint"]',
    }.get(exercise_type, "null")
    prompt = build_regenerate_exercise_prompt(
        cefr_level=cefr_level,
        target_language_name=target_language_name,
        native_language_name=native_language_name,
        lesson_type=lesson_type,
        topic=topic,
        exercise_type=exercise_type,
        lesson_explanation=json.dumps(lesson_explanation or {}, ensure_ascii=False),
        lesson_vocabulary=json.dumps(lesson_vocabulary or [], ensure_ascii=False),
        invalid_exercise=json.dumps(invalid_exercise, ensure_ascii=False),
        options_schema=options_schema,
        language_prompt_overlay=language_prompt_overlay,
    )

    exercise = await llm_adapter.structured_output(
        [{"role": "system", "content": prompt}],
        ExerciseContent,
    )
    if exercise.type != exercise_type:
        raise ValueError("Regenerated exercise type does not match original type")
    if exercise.type == "fill_blank" and "___" not in exercise.question:
        if exercise.explanation and "___" in exercise.explanation:
            exercise.question, exercise.explanation = (
                exercise.explanation,
                exercise.question,
            )
    if hint_reveals_answer(exercise.native_hint, exercise.correct):
        exercise.native_hint = None
    if not exercise.content_id:
        exercise.content_id = _stable_exercise_id(
            target_language=target_language,
            cefr_level=cefr_level,
            lesson_type=lesson_type,
            topic=topic,
            unit_id="",
            index=0,
            exercise=exercise,
        )
    if not exercise.variant:
        exercise.variant = exercise.type
    return exercise


async def evaluate_free_write(
    cefr_level: str,
    prompt: str,
    criteria: list[str],
    answer: str,
    target_language: str = "en-GB",
    native_language: str | None = None,
) -> FreeWriteEvaluation:
    target_language_name = get_language_name(target_language)
    native_language_name = (
        get_native_language_name(native_language) if native_language else "English"
    )
    language_prompt_overlay = get_language_prompt_overlay(target_language)
    eval_prompt = build_free_write_eval_prompt(
        cefr_level=cefr_level,
        target_language_name=target_language_name,
        native_language_name=native_language_name,
        prompt=prompt,
        criteria=", ".join(criteria),
        answer=answer,
        language_prompt_overlay=language_prompt_overlay,
    )

    result = await llm_adapter.structured_output(
        [{"role": "system", "content": eval_prompt}],
        FreeWriteEvaluation,
    )
    return result


async def evaluate_pronunciation(
    cefr_level: str,
    target: str,
    transcription: str,
    target_language: str = "en-GB",
    native_language: str | None = None,
) -> PronunciationEvaluation:
    target_language_name = get_language_name(target_language)
    native_language_name = (
        get_native_language_name(native_language) if native_language else "English"
    )
    language_prompt_overlay = get_language_prompt_overlay(target_language)
    eval_prompt = build_pronunciation_eval_prompt(
        cefr_level=cefr_level,
        target_language_name=target_language_name,
        native_language_name=native_language_name,
        target=target,
        transcription=transcription,
        language_prompt_overlay=language_prompt_overlay,
    )
    result = await llm_adapter.structured_output(
        [{"role": "system", "content": eval_prompt}],
        PronunciationEvaluation,
    )
    return result


async def evaluate_fill_blank(
    cefr_level: str,
    question: str,
    correct_answer: str,
    student_answer: str,
    target_language: str = "en-GB",
    native_language: str | None = None,
) -> FillBlankEvaluation:
    target_language_name = get_language_name(target_language)
    native_language_name = (
        get_native_language_name(native_language) if native_language else "English"
    )
    language_prompt_overlay = get_language_prompt_overlay(target_language)
    eval_prompt = build_fill_blank_eval_prompt(
        cefr_level=cefr_level,
        target_language_name=target_language_name,
        native_language_name=native_language_name,
        question=question,
        correct_answer=correct_answer,
        student_answer=student_answer,
        language_prompt_overlay=language_prompt_overlay,
    )
    result = await llm_adapter.structured_output(
        [{"role": "system", "content": eval_prompt}],
        FillBlankEvaluation,
    )
    return result

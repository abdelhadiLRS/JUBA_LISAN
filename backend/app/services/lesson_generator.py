import hashlib
import json
import re
from typing import Any

from app.data.curriculum import get_curriculum
from app.data.ar.lessons import get_arabic_a1_lessons, get_arabic_a1_content_seed
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


def _resolve_scheduled_lesson(
    *,
    target_language: str,
    cefr_level: str,
    unit_id: str,
    week: int,
    day: int,
) -> dict[str, Any] | None:
    """Resolve a deterministic course-map entry when one exists."""
    if target_language != "ar" or cefr_level != "A1" or not unit_id:
        return None
    scheduled = get_arabic_a1_lessons(unit_id)
    match = next((lesson for lesson in scheduled if lesson.week == week and lesson.day == day), None)
    if match is None:
        return None
    return {
        "lesson_type": match.lesson_type,
        "topic": match.title,
        "grammar_points": list(match.grammar_refs),
        "vocabulary_set_ids": list(match.vocabulary_set_ids),
        "unit_id": match.unit_id,
        "objective": match.objective,
    }


def get_valid_grammar_slugs(target_language: str = "en-GB") -> set[str]:
    """Return the set of valid grammar slugs for a given target language."""
    curriculum = get_curriculum(target_language)
    return {slug for units in curriculum.values() for unit in units for slug in unit.grammar_points}


def _fallback_lesson(*, cefr_level: str, lesson_type: str, topic: str, unit_id: str, target_language: str) -> LessonContent | None:
    """Keep the authored A1 English starter course launchable without an LLM."""
    if target_language not in {"en", "en-GB", "en_US"} or cefr_level.upper() != "A1":
        return None
    title = topic.strip() or "Identity & Greetings"
    base = {
        "lesson_type": lesson_type, "title": title, "cefr_level": cefr_level,
        "unit_id": unit_id, "grammar_refs": ["to-be", "subject-pronouns", "questions", "yes-no"],
    }
    if lesson_type == "grammar":
        base["explanation"] = {"title": "Introducing yourself", "body": "Use am, is and are with subject pronouns.", "examples": ["I am Sara.", "You are from Algeria.", "Is he a student?"]}
        base["exercises"] = [
            ExerciseContent(type="multiple_choice", question="___ am Alex.", options=["I", "He", "They"], correct="I", explanation="Use I with am."),
            ExerciseContent(type="multiple_choice", question="She ___ from London.", options=["am", "is", "are"], correct="is", explanation="Use is with she."),
            ExerciseContent(type="fill_blank", question="You ___ a student.", correct="are", accepted_answers=["are"], explanation="Use are with you."),
            ExerciseContent(type="multiple_choice", question="___ you from Algeria?", options=["Am", "Is", "Are"], correct="Are", explanation="Questions with you use are."),
        ]
    elif lesson_type == "vocabulary":
        base["explanation"] = {"title": "Greetings and introductions", "body": "Learn simple phrases for meeting someone.", "examples": ["Hello!", "Nice to meet you.", "My name is Adam."]}
        base["exercises"] = [
            ExerciseContent(type="multiple_choice", question="What do you say when you meet someone?", options=["Hello!", "Goodbye!", "Thanks!"], correct="Hello!"),
            ExerciseContent(type="multiple_choice", question="Complete: My ___ is Adam.", options=["name", "hello", "student"], correct="name"),
            ExerciseContent(type="fill_blank", question="Nice to ___ you.", correct="meet", accepted_answers=["meet"]),
        ]
    elif lesson_type == "listening":
        base["explanation"] = {"title": "Listen for names and introductions", "body": "Listen for the speaker's name and where they are from.", "examples": ["Hello, I'm Adam. I'm from London."]}
        base["exercises"] = [
            ExerciseContent(type="multiple_choice", question="Listen: 'Hello, I'm Adam.' What is his name?", options=["Adam", "Alex", "Sam"], correct="Adam"),
            ExerciseContent(type="multiple_choice", question="'I'm from London.' Where is he from?", options=["London", "Paris", "Rome"], correct="London"),
        ]
    elif lesson_type == "reading":
        base["explanation"] = {"title": "A short introduction", "body": "Read for key personal information.", "examples": ["Hello. My name is Emma. I am a student."]}
        base["exercises"] = [
            ExerciseContent(type="multiple_choice", question="Read: 'My name is Emma.' What is her name?", options=["Emma", "Anna", "Emily"], correct="Emma"),
            ExerciseContent(type="multiple_choice", question="Read: 'I am a student.' What is Emma?", options=["A student", "A teacher", "A doctor"], correct="A student"),
        ]
    elif lesson_type == "writing":
        base["explanation"] = {"title": "Write a simple introduction", "body": "Write your name, where you are from and one fact about yourself.", "examples": ["My name is Adam. I am from Algeria."]}
        base["exercises"] = [ExerciseContent(type="free_write", question="Write three short sentences to introduce yourself.", correct="My name is Adam. I am from Algeria. I am a student.", explanation="Include your name, where you are from and one fact about yourself.")]
    else:
        base["explanation"] = {"title": "Review: Identity & Greetings", "body": "Review greetings, subject pronouns and the verb to be.", "examples": ["I am", "You are", "She is"]}
        base["exercises"] = [
            ExerciseContent(type="multiple_choice", question="I ___ from Algeria.", options=["am", "is", "are"], correct="am"),
            ExerciseContent(type="multiple_choice", question="They ___ students.", options=["am", "is", "are"], correct="are"),
            ExerciseContent(type="multiple_choice", question="___ she from London?", options=["Am", "Is", "Are"], correct="Is"),
        ]
    lesson = LessonContent(**base)
    _attach_stable_exercise_metadata(lesson, target_language=target_language, topic=title, unit_id=unit_id)
    return lesson


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
    scheduled = _resolve_scheduled_lesson(
        target_language=target_language,
        cefr_level=cefr_level,
        unit_id=unit_id,
        week=week,
        day=day,
    )
    if scheduled is not None:
        lesson_type = scheduled["lesson_type"]
        topic = scheduled["topic"]
        grammar_points = scheduled["grammar_points"]
        vocabulary_set_ids = scheduled["vocabulary_set_ids"]
        unit_id = scheduled["unit_id"]

    scheduled_objective = ""
    seed = (
        get_arabic_a1_content_seed(f"a1-u{unit_id.split('-')[-1]}-w{week}-d{day}")
        if target_language == "ar" and cefr_level == "A1" and unit_id.startswith("a1-unit-")
        else None
    )
    gp_str = ", ".join(grammar_points) if grammar_points else "none specified"
    vs_str = ", ".join(vocabulary_set_ids) if vocabulary_set_ids else "general"
    seed_str = "none"
    if seed is not None:
        seed_str = json.dumps({
            "target_phrases": seed.target_phrases,
            "model_sentences": seed.model_sentences,
            "comprehension_prompt": seed.comprehension_prompt,
            "production_prompt": seed.production_prompt,
            "course_objective": scheduled_objective,
            "grammar_points": grammar_points or [],
            "vocabulary_set_ids": vocabulary_set_ids or [],
        }, ensure_ascii=False)
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
        content_seed=seed_str,
        week=week,
        day=day,
        valid_slugs=valid_slugs_str,
        language_prompt_overlay=language_prompt_overlay,
    )

    # Do not block the first authored course on an optional local Ollama service.
    # The A1 English starter content is deterministic and can launch immediately.
    fallback = _fallback_lesson(
        cefr_level=cefr_level,
        lesson_type=lesson_type,
        topic=topic,
        unit_id=unit_id,
        target_language=target_language,
    )
    if fallback is not None:
        lesson = fallback
    else:
        try:
            lesson = await llm_adapter.structured_output(
                [{"role": "system", "content": prompt}],
                LessonContent,
            )
        except Exception:
            if fallback is None:
                raise
            lesson = fallback

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

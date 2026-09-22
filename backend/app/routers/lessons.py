import copy
import json
import re
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from redis.asyncio import Redis
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import (
    check_subscription_or_freemium_access,
    get_current_user,
    get_redis,
)
from app.core.limiter import limiter
from app.models.exercise_attempt import ExerciseAttempt
from app.models.lesson import Exercise, Lesson
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.lessons import (
    ExerciseAnswerRequest,
    AdaptiveNextResponse,
    ExerciseAnswerResponse,
    ExerciseAttemptResponse,
    ExerciseAttemptSummaryResponse,
    ExerciseResponse,
    LessonDetailResponse,
    LessonMasteryNextResponse,
    LessonMasteryResponse,
    SkillMasteryResponse,
    LessonResponse,
    NativeExerciseExplanationResponse,
    NativeExerciseHintResponse,
    NativeExplanationResponse,
)
from app.services.language_helpers import get_language_name, get_native_language_name
from app.services.lesson_mastery import (
    mastery_reason,
    select_next_mastery_candidate,
    summarize_lesson_mastery,
    summarize_skill_mastery,
)
from app.services.lesson_generator import (
    evaluate_fill_blank,
    evaluate_free_write,
    evaluate_pronunciation,
    hint_reveals_answer,
    regenerate_exercise,
)
from app.services.llm_adapter import (
    LLMError,
    LLMTimeoutError,
    LLMUnavailableError,
    llm_adapter,
)
from app.services.exercise_retry import normalise_variant
from app.services.adaptive_variants import (
    collect_attempted_adaptive_identities,
    collect_attempted_exercise_ids,
    recommend_adaptive_action,
    recommend_adaptive_variant,
    summarize_adaptive_mastery,
)
from app.services.progress_service import update_daily_progress, upsert_unit_competency

router = APIRouter(prefix="/api/lessons", tags=["lessons"])


_ANSWER_FEEDBACK: dict[str, dict[str, str]] = {
    "en": {
        "correct": "Correct!",
        "correct_answer": "The correct answer is: {answer}",
        "free_write_unavailable": "Could not evaluate free-write answer at this time.",
        "good_pronunciation": "Good pronunciation!",
        "target_phrase": "The target phrase was: {answer}",
    },
    "es": {
        "correct": "Correcto!",
        "correct_answer": "La respuesta correcta es: {answer}",
        "free_write_unavailable": "No se pudo evaluar la respuesta escrita en este momento.",
        "good_pronunciation": "Buena pronunciacion!",
        "target_phrase": "La frase objetivo era: {answer}",
    },
    "de": {
        "correct": "Richtig!",
        "correct_answer": "Die richtige Antwort ist: {answer}",
        "free_write_unavailable": "Die schriftliche Antwort konnte momentan nicht bewertet werden.",
        "good_pronunciation": "Gute Aussprache!",
        "target_phrase": "Der Zielsatz war: {answer}",
    },
    "fr": {
        "correct": "Correct !",
        "correct_answer": "La bonne reponse est : {answer}",
        "free_write_unavailable": "Impossible d'evaluer la reponse ecrite pour le moment.",
        "good_pronunciation": "Bonne prononciation !",
        "target_phrase": "La phrase cible etait : {answer}",
    },
    "it": {
        "correct": "Corretto!",
        "correct_answer": "La risposta corretta e: {answer}",
        "free_write_unavailable": "Non e possibile valutare la risposta scritta in questo momento.",
        "good_pronunciation": "Buona pronuncia!",
        "target_phrase": "La frase obiettivo era: {answer}",
    },
    "pt": {
        "correct": "Correto!",
        "correct_answer": "A resposta correta e: {answer}",
        "free_write_unavailable": "Nao foi possivel avaliar a resposta escrita neste momento.",
        "good_pronunciation": "Boa pronuncia!",
        "target_phrase": "A frase-alvo era: {answer}",
    },
    "ru": {
        "correct": "Правильно!",
        "correct_answer": "Правильный ответ: {answer}",
        "free_write_unavailable": "Сейчас не удалось оценить письменный ответ.",
        "good_pronunciation": "Хорошее произношение!",
        "target_phrase": "Целевая фраза была: {answer}",
    },
    "nl": {
        "correct": "Correct!",
        "correct_answer": "Het juiste antwoord is: {answer}",
        "free_write_unavailable": "Het geschreven antwoord kan momenteel niet worden beoordeeld.",
        "good_pronunciation": "Goede uitspraak!",
        "target_phrase": "De doelzin was: {answer}",
    },
    "pl": {
        "correct": "Poprawnie!",
        "correct_answer": "Prawidlowa odpowiedz to: {answer}",
        "free_write_unavailable": "Nie mozna teraz ocenic odpowiedzi pisemnej.",
        "good_pronunciation": "Dobra wymowa!",
        "target_phrase": "Fraza docelowa to: {answer}",
    },
    "ro": {
        "correct": "Corect!",
        "correct_answer": "Raspunsul corect este: {answer}",
        "free_write_unavailable": "Nu s-a putut evalua raspunsul scris momentan.",
        "good_pronunciation": "Pronuntie buna!",
        "target_phrase": "Fraza tinta a fost: {answer}",
    },
}


def _answer_feedback(native_language: str, key: str, *, answer: str = "") -> str:
    messages = _ANSWER_FEEDBACK.get(native_language, _ANSWER_FEEDBACK["en"])
    return messages[key].format(answer=answer)



def _map_content_exercises(
    lesson_exercises: list[Exercise],
    content_exercises: list[object],
) -> dict[int, dict]:
    """Map persisted exercise ids to their lesson-content metadata by stable order."""
    mapped: dict[int, dict] = {}
    for index, exercise in enumerate(lesson_exercises):
        if index < len(content_exercises) and isinstance(content_exercises[index], dict):
            mapped[exercise.id] = content_exercises[index]
    return mapped


def _build_exercise_response(
    exercise: Exercise,
    *,
    content: dict,
    question: str | None = None,
    explanation: str | None = None,
    content_id: str | None = None,
    variant: str | None = None,
    mastery_score: float = 0.0,
    mastery_state: str = "unseen",
    mastery_variants: int = 0,
) -> ExerciseResponse:
    """Build the public exercise payload with optional lesson-content metadata."""
    return ExerciseResponse(
        id=exercise.id,
        lesson_id=exercise.lesson_id,
        exercise_type=exercise.exercise_type,
        question=question if isinstance(question, str) else exercise.question,
        options=exercise.options,
        correct_answer=exercise.correct_answer,
        user_answer=exercise.user_answer,
        score=exercise.score,
        feedback=exercise.feedback,
        explanation=explanation if isinstance(explanation, str) else exercise.explanation,
        native_explanation=(
            content.get("native_explanation")
            if isinstance(content.get("native_explanation"), str)
            else None
        ),
        native_hint=(
            content.get("native_hint")
            if isinstance(content.get("native_hint"), str)
            else None
        ),
        content_id=content_id if isinstance(content_id, str) else None,
        variant=variant if isinstance(variant, str) else None,
        accepted_answers=(
            content.get("accepted_answers")
            if isinstance(content.get("accepted_answers"), list)
            else None
        ),
        metadata=(
            content.get("metadata")
            if isinstance(content.get("metadata"), dict)
            else None
        ),
        skills=(
            [skill.strip() for skill in content.get("skills", []) if isinstance(skill, str) and skill.strip()]
            if isinstance(content.get("skills"), list)
            else None
        ),
        answered_at=exercise.answered_at,
        mastery_score=mastery_score,
        mastery_state=mastery_state,
        mastery_variants=mastery_variants,
    )


def _exercise_has_technical_error(exercise: Exercise) -> bool:
    if not exercise.question.strip() or not exercise.correct_answer.strip():
        return True
    if exercise.exercise_type == "multiple_choice":
        options = [opt for opt in (exercise.options or []) if isinstance(opt, str) and opt.strip()]
        return len(options) < 2 or exercise.correct_answer not in options
    if exercise.exercise_type == "fill_blank":
        return "___" not in exercise.question
    return False


async def _get_lesson_for_user(
    lesson_id: int,
    user_id: int,
    db: AsyncSession,
    *,
    for_update: bool = False,
) -> Lesson:
    """Fetch a lesson and verify it belongs to the requesting user via its study plan."""
    from app.models.user_language import UserLanguage

    query = (
        select(Lesson)
        .join(StudyPlan, Lesson.study_plan_id == StudyPlan.id)
        .join(UserLanguage, StudyPlan.user_language_id == UserLanguage.id)
        .where(Lesson.id == lesson_id, UserLanguage.user_id == user_id)
    )
    if for_update:
        query = query.with_for_update(of=Lesson)
    result = await db.execute(query)
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return lesson


async def _get_exercise_content_entry(
    exercise: Exercise,
    lesson: Lesson,
    db: AsyncSession,
) -> tuple[dict, list, dict]:
    result = await db.execute(
        select(Exercise)
        .where(Exercise.lesson_id == lesson.id)
        .order_by(Exercise.id)
        .with_for_update()
    )
    lesson_exercises = result.scalars().all()
    exercise_index = next(
        (index for index, item in enumerate(lesson_exercises) if item.id == exercise.id),
        None,
    )
    if exercise_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    content = copy.deepcopy(lesson.content or {})
    content_exercises = content.get("exercises")
    if not isinstance(content_exercises, list):
        content_exercises = []
    while len(content_exercises) <= exercise_index:
        content_exercises.append({})

    content_exercise = content_exercises[exercise_index]
    if not isinstance(content_exercise, dict):
        content_exercise = {}
        content_exercises[exercise_index] = content_exercise

    return content, content_exercises, content_exercise


async def _get_latest_attempt(
    db: AsyncSession,
    *,
    user_id: int,
    exercise_id: int,
    for_update: bool = False,
) -> ExerciseAttempt | None:
    """Load the authoritative persisted attempt by monotonically increasing identity."""
    query = (
        select(ExerciseAttempt)
        .where(
            ExerciseAttempt.user_id == user_id,
            ExerciseAttempt.exercise_id == exercise_id,
        )
        .order_by(ExerciseAttempt.attempt_number.desc())
        .limit(1)
    )
    if for_update:
        query = query.with_for_update()
    return await db.scalar(query)


def _persisted_attempt_identity(
    attempt: ExerciseAttempt,
    *,
    fallback_content_id: object,
    fallback_variant: object,
) -> tuple[str, str] | None:
    """Return normalized content/variant identity, preferring the persisted attempt."""
    content_id = attempt.content_id or fallback_content_id
    variant = attempt.variant or fallback_variant
    if not isinstance(content_id, str) or not content_id.strip():
        return None
    if not isinstance(variant, str) or not variant.strip():
        return None
    normalized_variant = normalise_variant(variant)
    if not normalized_variant:
        return None
    return content_id.strip(), normalized_variant


async def _get_exercise_index(exercise: Exercise, lesson: Lesson, db: AsyncSession) -> int:
    result = await db.execute(
        select(Exercise).where(Exercise.lesson_id == lesson.id).order_by(Exercise.id)
    )
    lesson_exercises = result.scalars().all()
    exercise_index = next(
        (index for index, item in enumerate(lesson_exercises) if item.id == exercise.id),
        None,
    )
    if exercise_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return exercise_index


@router.get("/{lesson_id}", response_model=LessonDetailResponse)
@limiter.limit("60/minute")
async def get_lesson(
    request: Request,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    lesson = await _get_lesson_for_user(lesson_id, current_user.id, db)

    result = await db.execute(
        select(Exercise).where(Exercise.lesson_id == lesson_id).order_by(Exercise.id)
    )
    exercises = result.scalars().all()

    # Sanitize fill_blank exercises that were generated before constraint #6 was enforced:
    # if `question` is an instruction text (no ___) but `explanation` has the gapped sentence,
    # swap them so the user sees the sentence — without touching the DB.
    content_exercises = []
    if isinstance(lesson.content, dict) and isinstance(lesson.content.get("exercises"), list):
        content_exercises = lesson.content["exercises"]

    attempt_result = await db.execute(
        select(ExerciseAttempt).where(
            ExerciseAttempt.lesson_id == lesson.id,
            ExerciseAttempt.user_id == current_user.id,
        )
    )
    lesson_attempts = attempt_result.scalars().all()

    fixed: list[ExerciseResponse] = []
    for index, ex in enumerate(exercises):
        q, exp = ex.question, ex.explanation
        if ex.exercise_type == "fill_blank" and "___" not in q:
            if exp and "___" in exp:
                q, exp = exp, q
        content_item = content_exercises[index] if index < len(content_exercises) else {}
        if not isinstance(content_item, dict):
            content_item = {}
        exercise_content_id = content_item.get("content_id")
        mastery_score, mastery_state, mastery_variants = summarize_adaptive_mastery(
            lesson_attempts,
            content_id=exercise_content_id if isinstance(exercise_content_id, str) else "",
        )
        fixed.append(
            _build_exercise_response(
                ex,
                content=content_item,
                question=q,
                explanation=exp,
                content_id=exercise_content_id,
                variant=content_item.get("variant"),
                mastery_score=mastery_score,
                mastery_state=mastery_state,
                mastery_variants=mastery_variants,
            )
        )

    return LessonDetailResponse(lesson=lesson, exercises=fixed)


@router.post("/{lesson_id}/start", response_model=LessonResponse)
@limiter.limit("60/minute")
async def start_lesson(
    request: Request,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    lesson = await _get_lesson_for_user(lesson_id, current_user.id, db)
    return lesson


@router.post("/{lesson_id}/complete", response_model=LessonResponse)
@limiter.limit("60/minute")
async def complete_lesson(
    request: Request,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db),
):
    lesson = await _get_lesson_for_user(lesson_id, current_user.id, db, for_update=True)

    if lesson.is_completed:
        return lesson

    await check_subscription_or_freemium_access("lessons", redis, current_user)

    lesson.is_completed = True
    lesson.completed_at = datetime.now(UTC).replace(tzinfo=None)

    await update_daily_progress(
        db,
        current_user.id,
        lesson_completed=True,
        skill=lesson.lesson_type,
        study_plan_id=lesson.study_plan_id,
        commit=False,
    )

    if lesson.unit_id:
        from app.data.curriculum import get_curriculum_units  # noqa: PLC0415
        from app.models.study_plan import StudyPlan  # noqa: PLC0415

        plan = await db.get(StudyPlan, lesson.study_plan_id)
        if plan:
            for u in get_curriculum_units(plan.cefr_level, plan.target_language):
                if u.id == lesson.unit_id:
                    # Score this lesson: average of answered exercises
                    result_ex = await db.execute(
                        select(Exercise).where(
                            Exercise.lesson_id == lesson.id,
                            Exercise.score.is_not(None),
                        )
                    )
                    exercises = result_ex.scalars().all()
                    lesson_score = (
                        sum(e.score for e in exercises if e.score is not None) / len(exercises)
                        if exercises
                        else 0.5
                    )
                    await upsert_unit_competency(
                        db,
                        current_user.id,
                        unit_id=lesson.unit_id,
                        competency_texts=u.competency_checklist,
                        lesson_score=lesson_score,
                        study_plan_id=lesson.study_plan_id,
                    )
                    break

    await db.commit()
    await db.refresh(lesson)

    # Record freemium lesson usage only after the database transaction succeeds.
    from app.services.freemium_service import maybe_record_freemium_usage

    await maybe_record_freemium_usage(current_user, "lessons")

    return lesson


@router.post("/exercises/{exercise_id}/answer", response_model=ExerciseAnswerResponse)
@limiter.limit("20/minute")
async def answer_exercise(
    request: Request,
    exercise_id: int,
    data: ExerciseAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    exercise = (
        await db.execute(
            select(Exercise).where(Exercise.id == exercise_id).with_for_update()
        )
    ).scalar_one_or_none()
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    lesson = await _get_lesson_for_user(exercise.lesson_id, current_user.id, db)

    plan = await db.get(StudyPlan, lesson.study_plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Study plan not found for lesson",
        )
    target_language = plan.target_language

    _content, _content_exercises, content_exercise = await _get_exercise_content_entry(
        exercise, lesson, db
    )
    accepted_answers = []
    raw_accepted = content_exercise.get("accepted_answers")
    if isinstance(raw_accepted, list):
        accepted_answers = [
            str(answer).strip().casefold()
            for answer in raw_accepted
            if str(answer).strip()
        ]
    canonical_answer = exercise.correct_answer.strip().casefold()
    if canonical_answer and canonical_answer not in accepted_answers:
        accepted_answers.insert(0, canonical_answer)

    if exercise.exercise_type == "free_write":
        prompt = exercise.question
        # Bug 4: use exercise-specific criteria from options if available
        criteria = [opt for opt in (exercise.options or []) if isinstance(opt, str) and opt.strip()]
        if not criteria:
            criteria = ["grammar", "spelling", "coherence"]
        try:
            eval_result = await evaluate_free_write(
                cefr_level=lesson.cefr_level,
                prompt=prompt,
                criteria=criteria,
                answer=data.answer,
                target_language=target_language,
                native_language=current_user.native_language,
            )
            sco = eval_result.score if hasattr(eval_result, "score") else eval_result["score"]
            fb = (
                eval_result.feedback
                if hasattr(eval_result, "feedback")
                else eval_result["feedback"]
            )
            exercise.score = sco
            exercise.feedback = fb
        except (LLMTimeoutError, LLMUnavailableError, LLMError):
            exercise.score = 0.5
            exercise.feedback = _answer_feedback(
                current_user.native_language, "free_write_unavailable"
            )
    elif exercise.exercise_type == "fill_blank":
        try:
            eval_result = await evaluate_fill_blank(
                cefr_level=lesson.cefr_level,
                question=exercise.question,
                correct_answer=exercise.correct_answer,
                student_answer=data.answer,
                target_language=target_language,
                native_language=current_user.native_language,
            )
            exercise.score = eval_result.score
            exercise.feedback = eval_result.feedback
        except (LLMTimeoutError, LLMUnavailableError, LLMError):
            # Fallback: normalised string comparison
            ua = data.answer.strip().lower().rstrip(".,!?")
            ca = exercise.correct_answer.strip().lower().rstrip(".,!?")
            alternatives = [a.strip().lower() for a in ca.split("/")]
            is_correct = ua == ca or ua in alternatives or ua in accepted_answers
            exercise.score = 1.0 if is_correct else 0.0
            exercise.feedback = (
                _answer_feedback(current_user.native_language, "correct")
                if is_correct
                else _answer_feedback(
                    current_user.native_language,
                    "correct_answer",
                    answer=exercise.correct_answer,
                )
            )
    elif exercise.exercise_type == "pronunciation":
        transcription = data.answer
        try:
            eval_result = await evaluate_pronunciation(
                cefr_level=lesson.cefr_level,
                target=exercise.correct_answer,
                transcription=transcription,
                target_language=target_language,
                native_language=current_user.native_language,
            )
            exercise.score = eval_result.score
            exercise.feedback = eval_result.feedback
        except (LLMTimeoutError, LLMUnavailableError, LLMError):
            # Fallback: normalised comparison stripping punctuation
            norm_target = re.sub(r"[^\w\s]", "", exercise.correct_answer).strip().lower()
            norm_answer = re.sub(r"[^\w\s]", "", transcription).strip().lower()
            is_close = (
                norm_target == norm_answer
                or norm_target in norm_answer
                or norm_answer in norm_target
            )
            exercise.score = 1.0 if is_close else 0.0
            exercise.feedback = (
                _answer_feedback(current_user.native_language, "good_pronunciation")
                if is_close
                else _answer_feedback(
                    current_user.native_language,
                    "target_phrase",
                    answer=exercise.correct_answer,
                )
            )
    else:
        user_ans = data.answer.strip().lower()
        correct_ans = exercise.correct_answer.strip().lower()
        # Compatibility: old exercises may store correct_answer as bare letter ("a")
        # while clients now submit full option text ("a. works"). Accept both.
        _stripped = re.sub(r"^[a-z]\. *", "", user_ans)
        is_correct = (
            user_ans == correct_ans
            or _stripped == correct_ans
            or user_ans == re.sub(r"^[a-z]\. *", "", correct_ans)
            or user_ans in accepted_answers
            or _stripped in accepted_answers
        )
        exercise.score = 1.0 if is_correct else 0.0
        exercise.feedback = (
            _answer_feedback(current_user.native_language, "correct")
            if is_correct
            else _answer_feedback(
                current_user.native_language,
                "correct_answer",
                answer=exercise.correct_answer,
            )
        )

    # Keep every evaluator on the same canonical score domain used by mastery/progress logic.
    try:
        exercise.score = max(0.0, min(1.0, float(exercise.score)))
    except (TypeError, ValueError):
        exercise.score = 0.0

    exercise.user_answer = data.answer
    exercise.answered_at = datetime.now(UTC).replace(tzinfo=None)

    latest_attempt = await _get_latest_attempt(
        db,
        user_id=current_user.id,
        exercise_id=exercise.id,
    )
    max_attempt = latest_attempt.attempt_number if latest_attempt else None
    attempt_number = int(max_attempt or 0) + 1

    # Persist adaptive identity in its canonical form so later regeneration or
    # retry requests can rely on a stable content/variant pair.
    raw_content_id = content_exercise.get("content_id")
    persisted_content_id = (
        raw_content_id.strip() if isinstance(raw_content_id, str) and raw_content_id.strip() else None
    )
    raw_variant = content_exercise.get("variant")
    persisted_variant = normalise_variant(
        raw_variant if isinstance(raw_variant, str) and raw_variant.strip() else exercise.exercise_type
    ) or normalise_variant(exercise.exercise_type)

    attempt = ExerciseAttempt(
        user_id=current_user.id,
        exercise_id=exercise.id,
        lesson_id=lesson.id,
        study_plan_id=lesson.study_plan_id,
        content_id=persisted_content_id,
        variant=persisted_variant,
        attempt_number=attempt_number,
        user_answer=data.answer,
        score=exercise.score,
        feedback=exercise.feedback or "",
        answered_at=exercise.answered_at,
    )
    prior_content_attempt = max_attempt is not None
    if attempt.content_id:
        prior_content_attempt = (
            await db.scalar(
                select(ExerciseAttempt.id).where(
                    ExerciseAttempt.user_id == current_user.id,
                    ExerciseAttempt.content_id == attempt.content_id,
                ).limit(1)
            )
        ) is not None
    db.add(attempt)

    # Feed each answered exercise into the unit competency engine immediately.
    # This makes adaptive performance visible to the Learning Journey without
    # waiting for the whole lesson to be completed.
    if lesson.unit_id:
        from app.data.curriculum import get_curriculum_units  # noqa: PLC0415

        curriculum_unit = next(
            (
                unit
                for unit in get_curriculum_units(plan.cefr_level, plan.target_language)
                if unit.id == lesson.unit_id
            ),
            None,
        )
        if curriculum_unit and curriculum_unit.competency_checklist:
            scored_result = await db.execute(
                select(Exercise).where(
                    Exercise.lesson_id == lesson.id,
                    Exercise.score.is_not(None),
                )
            )
            scored_exercises = scored_result.scalars().all()
            lesson_score = (
                sum(item.score for item in scored_exercises if item.score is not None)
                / len(scored_exercises)
                if scored_exercises
                else exercise.score
            )
            await upsert_unit_competency(
                db,
                current_user.id,
                unit_id=lesson.unit_id,
                competency_texts=curriculum_unit.competency_checklist,
                lesson_score=lesson_score,
                study_plan_id=lesson.study_plan_id,
            )

    if not prior_content_attempt:
        await update_daily_progress(
            db,
            current_user.id,
            exercise_correct=exercise.score >= 0.5,
            skill=lesson.lesson_type,
            skill_score=exercise.score,
            study_plan_id=lesson.study_plan_id,
            commit=False,
        )

    await db.commit()
    await db.refresh(exercise)
    await db.refresh(attempt)

    # Reuse the canonical adaptive engine for the immediate answer response.
    # The current attempt is already persisted, so collect the full history and
    # prevent recommendations from pointing back to any answered sibling.
    history_result = await db.execute(
        select(ExerciseAttempt).where(
            ExerciseAttempt.user_id == current_user.id,
            ExerciseAttempt.lesson_id == lesson.id,
        )
    )
    history_attempts = history_result.scalars().all()
    attempted_exercise_ids = collect_attempted_exercise_ids(history_attempts)
    attempted_adaptive_identities = collect_attempted_adaptive_identities(history_attempts)

    lesson_exercise_result = await db.execute(
        select(Exercise).where(Exercise.lesson_id == lesson.id).order_by(Exercise.id)
    )
    lesson_exercises = lesson_exercise_result.scalars().all()
    content_by_exercise_id = _map_content_exercises(lesson_exercises, _content_exercises)

    if attempt.content_id:
        recommended_action, recommended_variant, _target = recommend_adaptive_variant(
            lesson_exercises,
            content_id=attempt.content_id,
            current_variant=attempt.variant,
            score=exercise.score,
            attempted_exercise_ids=attempted_exercise_ids,
            attempted_adaptive_identities=attempted_adaptive_identities,
            attempt_history=history_attempts,
            get_exercise_id=lambda item: item.id,
            get_variant=lambda item: (
                content_by_exercise_id.get(item.id, {}).get("variant")
                or item.exercise_type
            ),
            get_content_id=lambda item: content_by_exercise_id.get(item.id, {}).get(
                "content_id"
            ),
        )
    else:
        recommended_action, recommended_variant = recommend_adaptive_action(
            exercise.score, attempt.variant
        )

    answer_mastery_score, answer_mastery_state, answer_mastery_variants = summarize_adaptive_mastery(
        history_attempts,
        content_id=attempt.content_id or "",
    )

    return ExerciseAnswerResponse(
        id=exercise.id,
        score=exercise.score,
        feedback=exercise.feedback,
        correct_answer=exercise.correct_answer,
        attempt_id=attempt.id,
        attempt_number=attempt.attempt_number,
        content_id=attempt.content_id,
        variant=attempt.variant,
        attempts_count=attempt.attempt_number,
        score_delta=round(
            exercise.score - latest_attempt.score, 3
        ) if latest_attempt is not None else 0.0,
        mastered=answer_mastery_state == "mastered",
        mastery_score=answer_mastery_score,
        mastery_state=answer_mastery_state,
        mastery_variants=answer_mastery_variants,
        recommended_action=recommended_action,
        recommended_variant=recommended_variant,
    )


@router.get("/exercises/{exercise_id}/attempts", response_model=list[ExerciseAttemptResponse])
@limiter.limit("60/minute")
async def list_exercise_attempts(
    request: Request,
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    exercise = await db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    await _get_lesson_for_user(exercise.lesson_id, current_user.id, db)
    result = await db.execute(
        select(ExerciseAttempt)
        .where(
            ExerciseAttempt.exercise_id == exercise_id,
            ExerciseAttempt.user_id == current_user.id,
        )
        .order_by(ExerciseAttempt.attempt_number)
    )
    return result.scalars().all()


@router.get(
    "/{lesson_id}/mastery/next",
    response_model=LessonMasteryNextResponse,
)
@limiter.limit("60/minute")
async def get_next_mastery_exercise(
    request: Request,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return the next lesson exercise that needs the most mastery work."""
    lesson = await _get_lesson_for_user(lesson_id, current_user.id, db)
    exercise_result = await db.execute(
        select(Exercise).where(Exercise.lesson_id == lesson.id).order_by(Exercise.id)
    )
    exercises = exercise_result.scalars().all()
    if not exercises:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No exercises available for mastery",
        )

    attempt_result = await db.execute(
        select(ExerciseAttempt).where(
            ExerciseAttempt.lesson_id == lesson.id,
            ExerciseAttempt.user_id == current_user.id,
        )
    )
    attempts = attempt_result.scalars().all()
    content_exercises = (
        lesson.content.get("exercises", [])
        if isinstance(lesson.content, dict)
        else []
    )

    content_by_exercise_id = _map_content_exercises(exercises, content_exercises)
    candidate = select_next_mastery_candidate(
        exercises,
        attempts,
        get_content_id=lambda item: content_by_exercise_id.get(item.id, {}).get("content_id"),
        get_exercise_id=lambda item: item.id,
    )
    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="All lesson exercises are mastered",
        )

    exercise = candidate.exercise
    content = content_by_exercise_id.get(exercise.id, {})
    if not isinstance(content, dict):
        content = {}

    return LessonMasteryNextResponse(
        exercise=_build_exercise_response(
            exercise,
            content=content,
            content_id=content.get("content_id"),
            variant=content.get("variant"),
            mastery_score=candidate.mastery_score,
            mastery_state=candidate.mastery_state,
            mastery_variants=candidate.mastery_variants,
        ),
        reason=mastery_reason(candidate.mastery_state),
    )


@router.get(
    "/{lesson_id}/attempt-summary",
    response_model=list[ExerciseAttemptSummaryResponse],
)
@limiter.limit("60/minute")
async def list_lesson_attempt_summary(
    request: Request,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    lesson = await _get_lesson_for_user(lesson_id, current_user.id, db)
    result = await db.execute(
        select(ExerciseAttempt)
        .where(
            ExerciseAttempt.lesson_id == lesson.id,
            ExerciseAttempt.user_id == current_user.id,
        )
        .order_by(ExerciseAttempt.exercise_id, ExerciseAttempt.attempt_number)
    )
    grouped: dict[int, list[ExerciseAttempt]] = {}
    for attempt in result.scalars().all():
        grouped.setdefault(attempt.exercise_id, []).append(attempt)

    lesson_exercise_result = await db.execute(
        select(Exercise).where(Exercise.lesson_id == lesson.id).order_by(Exercise.id)
    )
    lesson_exercises = lesson_exercise_result.scalars().all()
    content_exercises = (
        lesson.content.get("exercises", [])
        if isinstance(lesson.content, dict)
        else []
    )
    content_by_exercise_id = _map_content_exercises(lesson_exercises, content_exercises)

    all_attempts = [attempt for items in grouped.values() for attempt in items]
    attempted_exercise_ids = collect_attempted_exercise_ids(all_attempts)
    attempted_adaptive_identities = collect_attempted_adaptive_identities(all_attempts)

    summaries = []
    for exercise_id, items in grouped.items():
        latest = max(items, key=lambda item: (item.attempt_number, item.answered_at))
        first = min(items, key=lambda item: item.attempt_number)
        best_score = max(item.score for item in items)
        mastery_score, mastery_state, covered_variants = summarize_adaptive_mastery(
            all_attempts,
            content_id=latest.content_id or content_by_exercise_id.get(exercise_id, {}).get("content_id") or "",
        )

        current_exercise = next(
            (exercise for exercise in lesson_exercises if exercise.id == exercise_id),
            None,
        )
        if current_exercise is not None and latest.content_id:
            action, recommended_variant, _target = recommend_adaptive_variant(
                lesson_exercises,
                content_id=latest.content_id,
                current_variant=latest.variant or current_exercise.exercise_type,
                score=latest.score,
                attempted_exercise_ids=attempted_exercise_ids,
                attempted_adaptive_identities=attempted_adaptive_identities,
                attempt_history=all_attempts,
                get_exercise_id=lambda item: item.id,
                get_variant=lambda item: (
                    content_by_exercise_id.get(item.id, {}).get("variant")
                    or item.exercise_type
                ),
                get_content_id=lambda item: content_by_exercise_id.get(item.id, {}).get(
                    "content_id"
                ),
            )
        else:
            action, recommended_variant = recommend_adaptive_action(
                latest.score, latest.variant
            )

        latest_identity = _persisted_attempt_identity(
            latest,
            fallback_content_id=(
                content_by_exercise_id.get(exercise_id, {}).get("content_id")
            ),
            fallback_variant=(
                latest.variant
                or content_by_exercise_id.get(exercise_id, {}).get("variant")
                or (current_exercise.exercise_type if current_exercise is not None else None)
            ),
        )
        latest_variant = latest_identity[1] if latest_identity is not None else latest.variant

        summaries.append(
            ExerciseAttemptSummaryResponse(
                exercise_id=exercise_id,
                attempts=len(items),
                best_score=best_score,
                latest_score=latest.score,
                first_score=first.score,
                improvement=round(latest.score - first.score, 3),
                mastered=mastery_state == "mastered",
                needs_retry=mastery_state == "struggling",
                mastery_score=mastery_score,
                mastery_state=mastery_state,
                mastery_variants=covered_variants,
                latest_variant=latest_variant,
                recommended_action=action,
                recommended_variant=recommended_variant,
                latest_answered_at=latest.answered_at,
            )
        )
    return summaries


@router.get(
    "/{lesson_id}/mastery",
    response_model=LessonMasteryResponse,
)
@limiter.limit("60/minute")
async def get_lesson_mastery(
    request: Request,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return an aggregate mastery snapshot for every exercise in a lesson."""
    lesson = await _get_lesson_for_user(lesson_id, current_user.id, db)
    result = await db.execute(
        select(ExerciseAttempt)
        .where(
            ExerciseAttempt.lesson_id == lesson.id,
            ExerciseAttempt.user_id == current_user.id,
        )
    )
    attempts = result.scalars().all()
    exercise_result = await db.execute(
        select(Exercise).where(Exercise.lesson_id == lesson.id).order_by(Exercise.id)
    )
    exercises = exercise_result.scalars().all()
    content_exercises = lesson.content.get("exercises", []) if isinstance(lesson.content, dict) else []
    content_by_exercise_id = _map_content_exercises(exercises, content_exercises)

    aggregate = summarize_lesson_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: content_by_exercise_id.get(item.id, {}).get("content_id"),
    )
    skill_aggregates = summarize_skill_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: content_by_exercise_id.get(item.id, {}).get("content_id"),
        get_skills=lambda item: content_by_exercise_id.get(item.id, {}).get("skills"),
    )
    return LessonMasteryResponse(
        **aggregate.__dict__,
        skills=[SkillMasteryResponse(**item.__dict__) for item in skill_aggregates],
    )


@router.get(
    "/{lesson_id}/mastery/skills",
    response_model=list[SkillMasteryResponse],
)
@limiter.limit("60/minute")
async def get_lesson_skill_mastery(
    request: Request,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return mastery coverage grouped by the skills attached to lesson exercises."""
    lesson = await _get_lesson_for_user(lesson_id, current_user.id, db)
    attempts_result = await db.execute(
        select(ExerciseAttempt).where(
            ExerciseAttempt.lesson_id == lesson.id,
            ExerciseAttempt.user_id == current_user.id,
        )
    )
    attempts = attempts_result.scalars().all()
    exercise_result = await db.execute(
        select(Exercise).where(Exercise.lesson_id == lesson.id).order_by(Exercise.id)
    )
    exercises = exercise_result.scalars().all()
    content_exercises = (
        lesson.content.get("exercises", [])
        if isinstance(lesson.content, dict)
        else []
    )
    content_by_exercise_id = _map_content_exercises(exercises, content_exercises)

    aggregates = summarize_skill_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: content_by_exercise_id.get(item.id, {}).get("content_id"),
        get_skills=lambda item: content_by_exercise_id.get(item.id, {}).get("skills"),
    )
    return [SkillMasteryResponse(**aggregate.__dict__) for aggregate in aggregates]


@router.post(
    "/exercises/{exercise_id}/adaptive-next",
    response_model=AdaptiveNextResponse,
)
@limiter.limit("20/minute")
async def adaptive_next_exercise(
    request: Request,
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return the next unanswered sibling variant selected from the latest attempt."""
    exercise = await db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    lesson = await _get_lesson_for_user(exercise.lesson_id, current_user.id, db, for_update=True)
    if lesson.is_completed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Completed lesson exercises cannot be advanced adaptively",
        )

    _content, content_exercises, content_exercise = await _get_exercise_content_entry(
        exercise, lesson, db
    )
    content_id = content_exercise.get("content_id")
    current_variant = content_exercise.get("variant") or exercise.exercise_type

    latest_attempt = await _get_latest_attempt(
        db,
        user_id=current_user.id,
        exercise_id=exercise.id,
    )
    if latest_attempt is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exercise must be answered before adaptive progression",
        )

    # Base adaptive progression on the persisted attempt identity. The lesson
    # content can be regenerated or normalized after an answer, but the latest
    # attempt remains the authoritative variant/content identity for the score.
    persisted_identity = _persisted_attempt_identity(
        latest_attempt,
        fallback_content_id=content_id,
        fallback_variant=current_variant,
    )
    if persisted_identity is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Latest attempt does not have a stable content identity",
        )
    attempted_content_id, attempted_variant = persisted_identity

    result = await db.execute(
        select(Exercise).where(Exercise.lesson_id == lesson.id).order_by(Exercise.id)
    )
    lesson_exercises = result.scalars().all()

    content_by_exercise_id = _map_content_exercises(lesson_exercises, content_exercises)

    attempt_result = await db.execute(
        select(ExerciseAttempt).where(
            ExerciseAttempt.user_id == current_user.id,
            ExerciseAttempt.lesson_id == lesson.id,
        )
    )
    attempt_history = attempt_result.scalars().all()
    attempted_exercise_ids = collect_attempted_exercise_ids(attempt_history)
    attempted_adaptive_identities = collect_attempted_adaptive_identities(attempt_history)

    action, target_variant, target = recommend_adaptive_variant(
        lesson_exercises,
        content_id=attempted_content_id,
        current_variant=attempted_variant,
        score=latest_attempt.score,
        attempted_exercise_ids=attempted_exercise_ids,
        attempted_adaptive_identities=attempted_adaptive_identities,
        attempt_history=attempt_history,
        get_exercise_id=lambda item: item.id,
        get_variant=lambda item: (
            content_by_exercise_id.get(item.id, {}).get("variant") or item.exercise_type
        ),
        get_content_id=lambda item: content_by_exercise_id.get(item.id, {}).get("content_id"),
    )
    if target is None or target_variant is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No unanswered adaptive variant is available",
        )

    target_content = content_by_exercise_id.get(target.id, {})
    return AdaptiveNextResponse(
        action=action,
        recommended_variant=target_variant,
        exercise=_build_exercise_response(
            target,
            content=target_content,
            content_id=attempted_content_id,
            variant=target_variant,
        ),
    )


@router.post("/exercises/{exercise_id}/retry", response_model=ExerciseResponse)
@limiter.limit("20/minute")
async def retry_exercise(
    request: Request,
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    exercise = await db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    lesson = await _get_lesson_for_user(exercise.lesson_id, current_user.id, db, for_update=True)
    if lesson.is_completed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Completed lesson exercises cannot be retried",
        )
    _content, content_exercises, content_exercise = await _get_exercise_content_entry(
        exercise, lesson, db
    )
    content_id = content_exercise.get("content_id")

    latest_attempt = await _get_latest_attempt(
        db,
        user_id=current_user.id,
        exercise_id=exercise.id,
        for_update=True,
    )
    if latest_attempt is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exercise must be answered before retry",
        )
    if latest_attempt.score >= 0.5:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only failed exercises can be retried",
        )

    result = await db.execute(
        select(Exercise)
        .where(Exercise.lesson_id == lesson.id)
        .order_by(Exercise.id)
        .with_for_update()
    )
    lesson_exercises = result.scalars().all()
    content_by_exercise_id = _map_content_exercises(lesson_exercises, content_exercises)

    attempt_result = await db.execute(
        select(ExerciseAttempt).where(
            ExerciseAttempt.user_id == current_user.id,
            ExerciseAttempt.lesson_id == lesson.id,
        )
    )
    attempt_history = attempt_result.scalars().all()
    attempted_exercise_ids = collect_attempted_exercise_ids(attempt_history)
    attempted_adaptive_identities = collect_attempted_adaptive_identities(attempt_history)

    persisted_identity = _persisted_attempt_identity(
        latest_attempt,
        fallback_content_id=content_id,
        fallback_variant=content_exercise.get("variant") or exercise.exercise_type,
    )
    if persisted_identity is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Latest attempt does not have a stable content identity for retry",
        )
    attempted_content_id, attempted_variant = persisted_identity

    _action, target_variant, target = recommend_adaptive_variant(
        lesson_exercises,
        content_id=attempted_content_id,
        current_variant=attempted_variant,
        score=latest_attempt.score,
        attempted_exercise_ids=attempted_exercise_ids,
        attempted_adaptive_identities=attempted_adaptive_identities,
        attempt_history=attempt_history,
        get_exercise_id=lambda item: item.id,
        get_variant=lambda item: (
            content_by_exercise_id.get(item.id, {}).get("variant") or item.exercise_type
        ),
        get_content_id=lambda item: content_by_exercise_id.get(item.id, {}).get("content_id"),
    )
    if target is None or target_variant is None or latest_attempt.score >= 0.5:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No easier unanswered exercise variant is available",
        )

    target_content = content_by_exercise_id.get(target.id, {})
    return _build_exercise_response(
        target,
        content=target_content,
        content_id=attempted_content_id,
        variant=target_variant,
    )


@router.post("/exercises/{exercise_id}/regenerate", response_model=ExerciseResponse)
@limiter.limit("5/hour")
async def regenerate_invalid_exercise(
    request: Request,
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    exercise = await db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    lesson = await _get_lesson_for_user(exercise.lesson_id, current_user.id, db)
    if lesson.is_completed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Completed lesson exercises cannot be regenerated",
        )
    if exercise.answered_at is not None or exercise.score is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Answered exercises cannot be regenerated",
        )
    if not _exercise_has_technical_error(exercise):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exercise does not need regeneration",
        )

    plan = await db.get(StudyPlan, lesson.study_plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Study plan not found for lesson",
        )

    content, content_exercises, _content_exercise = await _get_exercise_content_entry(
        exercise, lesson, db
    )
    exercise_index = await _get_exercise_index(exercise, lesson, db)
    invalid_exercise = {
        "type": exercise.exercise_type,
        "question": exercise.question,
        "options": exercise.options,
        "correct": exercise.correct_answer,
        "explanation": exercise.explanation,
    }

    try:
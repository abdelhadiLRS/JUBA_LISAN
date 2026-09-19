from datetime import date
from typing import cast

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.limiter import limiter
from app.data._types import CEFRLevel
from app.data.vocabulary import get_vocabulary_by_level
from app.models.flashcard import Flashcard
from app.models.progress import Progress
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.progress import GameProgressUpdate, ProgressHistoryResponse, ProgressResponse, ProgressSummary
from app.services.progress_service import get_unit_competencies
from app.services.user_language_service import get_active_language

router = APIRouter(prefix="/api/progress", tags=["progress"])


async def _get_active_plan_or_none(db: AsyncSession, user_id: int) -> StudyPlan | None:
    """Return the active study plan for the user's active language, or None if not set up yet."""
    active_lang = await get_active_language(db, user_id)
    if not active_lang:
        return None
    result = await db.execute(
        select(StudyPlan).where(
            StudyPlan.user_language_id == active_lang.id,
            StudyPlan.is_active.is_(True),
        )
    )
    return result.scalar_one_or_none()


async def _get_vocabulary_level_progress(
    db: AsyncSession, user_id: int, plan: StudyPlan
) -> tuple[int, int, float]:
    vocab_sets = get_vocabulary_by_level(cast(CEFRLevel, plan.cefr_level), plan.target_language)
    total_words = sum(len(vocab_set.words) for vocab_set in vocab_sets)
    if total_words == 0:
        return 0, 0, 0.0

    result = await db.execute(
        select(Flashcard.word).where(
            Flashcard.user_id == user_id,
            Flashcard.study_plan_id == plan.id,
            Flashcard.repetitions > 0,
        )
    )
    mastered_words = {word.strip().lower() for word in result.scalars().all()}
    mastered_count = sum(
        1
        for vocab_set in vocab_sets
        for word in vocab_set.words
        if word.word.strip().lower() in mastered_words
    )
    return mastered_count, total_words, mastered_count / total_words


@router.get("/summary", response_model=ProgressSummary)
@limiter.limit("60/minute")
async def get_summary(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        return ProgressSummary(
            total_xp=0,
            current_streak=0,
            total_lessons=0,
            total_exercises=0,
            exercises_correct=0,
            accuracy=0.0,
            skills={},
        )

    vocabulary_mastered, vocabulary_total, vocabulary_progress = (
        await _get_vocabulary_level_progress(db, current_user.id, plan)
    )

    result = await db.execute(
        select(Progress).where(Progress.study_plan_id == plan.id).order_by(Progress.date.desc())
    )
    all_entries = result.scalars().all()

    if not all_entries:
        return ProgressSummary(
            total_xp=0,
            current_streak=0,
            total_lessons=0,
            total_exercises=0,
            exercises_correct=0,
            accuracy=0.0,
            skills={},
            vocabulary_level=plan.cefr_level,
            vocabulary_mastered=vocabulary_mastered,
            vocabulary_total=vocabulary_total,
            vocabulary_progress=round(vocabulary_progress, 2),
        )

    total_xp = sum(e.xp_earned for e in all_entries)
    total_lessons = sum(e.lessons_completed for e in all_entries)
    total_exercises = sum(e.exercises_total for e in all_entries)
    exercises_correct = sum(e.exercises_correct for e in all_entries)
    accuracy = exercises_correct / total_exercises if total_exercises > 0 else 0.0

    latest_skills = all_entries[0].skills if all_entries else {}

    return ProgressSummary(
        total_xp=total_xp,
        current_streak=all_entries[0].streak_day,
        total_lessons=total_lessons,
        total_exercises=total_exercises,
        exercises_correct=exercises_correct,
        accuracy=round(accuracy, 2),
        skills=latest_skills,
        vocabulary_level=plan.cefr_level,
        vocabulary_mastered=vocabulary_mastered,
        vocabulary_total=vocabulary_total,
        vocabulary_progress=round(vocabulary_progress, 2),
    )


@router.post("/game", response_model=ProgressResponse)
@limiter.limit("60/minute")
async def record_game_progress(
    request: Request,
    data: GameProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No active study plan found")

    entry = await update_daily_progress(
        db,
        current_user.id,
        study_plan_id=plan.id,
        xp=max(0, data.xp),
        commit=False,
    )
    entry.exercises_total += max(0, data.questions_answered)
    entry.exercises_correct += min(
        max(0, data.correct_answers), max(0, data.questions_answered)
    )
    if data.skills:
        skills = dict(entry.skills or {})
        for skill, score in data.skills.items():
            if not isinstance(skill, str) or not skill.strip():
                continue
            safe_score = max(0.0, min(1.0, float(score)))
            old = skills.get(skill, safe_score)
            skills[skill] = round(old * 0.7 + safe_score * 0.3, 3)
        entry.skills = skills
    await db.commit()
    await db.refresh(entry)
    return entry


@router.get("/history", response_model=ProgressHistoryResponse)
@limiter.limit("60/minute")
async def get_history(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        return ProgressHistoryResponse(entries=[])

    result = await db.execute(
        select(Progress)
        .where(Progress.study_plan_id == plan.id)
        .order_by(Progress.date.desc())
        .limit(90)
    )
    entries = result.scalars().all()
    return ProgressHistoryResponse(entries=entries)


@router.get("/competencies", response_model=list)
@limiter.limit("60/minute")
async def get_competencies(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        return []
    return await get_unit_competencies(db, current_user.id, study_plan_id=plan.id)

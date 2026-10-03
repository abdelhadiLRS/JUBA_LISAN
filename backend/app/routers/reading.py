from __future__ import annotations
import asyncio
import logging
from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user, get_active_study_plan, get_redis, require_not_maintenance, require_learner
from app.core.limiter import limiter
from app.models.study_plan import StudyPlan
from app.models.reading import ReadingExercise
from app.models.user import User
from app.schemas.reading import (CorrectAnswerOut, QuestionOut, ReadingAttemptOut, ReadingExerciseOut, ReadingGeneratingResponse,
    ReadingHistoryResponse, ReadingNextResponse, ReadingSubmitRequest, ReadingSubmitResponse)
from app.services.reading_service import generate_and_save_exercise, get_available_exercise, get_user_history, submit_attempt
from app.services.feature_quota_service import reserve, settle
from app.services.generation_lease import release_generation_lock
from app.utils.db import db_session

router = APIRouter(prefix="/api/reading", tags=["reading"], dependencies=[Depends(require_learner)])
logger = logging.getLogger(__name__)


def _build_exercise_out(exercise) -> ReadingExerciseOut:
    return ReadingExerciseOut(id=exercise.id, level=exercise.level, target_language=exercise.target_language,
        exercise_type=exercise.exercise_type, topic=exercise.topic, text=exercise.text,
        questions=[QuestionOut(index=q["index"], question=q["question"], options=q["options"]) for q in exercise.questions])


async def _background_generate(level: str, target_language: str, lock_key: str, reservation=None, lock_token: str = "") -> None:
    success = False
    try:
        async with db_session() as db:
            exercise = await generate_and_save_exercise(level, target_language, db)
            if exercise is None:
                raise ValueError("No exercise was saved")
        if reservation is not None:
            await settle(reservation, success=True)
        success = True
    except Exception:
        logger.exception("Reading generation failed")
    finally:
        if reservation is not None and not success:
            await settle(reservation, success=False)
        await release_generation_lock(lock_key, lock_token)


@router.get("/next", response_model=ReadingNextResponse)
@limiter.limit("10/minute")
async def get_next_exercise(request: Request, _maintenance: None = Depends(require_not_maintenance), wait: bool = False,
    plan: StudyPlan = Depends(get_active_study_plan), current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db), redis: Redis | None = Depends(get_redis)) -> ReadingNextResponse:
    level, target = plan.cefr_level, plan.target_language
    exercise = await get_available_exercise(level, target, current_user.id, db)
    if exercise:
        return ReadingNextResponse(available=True, exercise=_build_exercise_out(exercise))
    if wait:
        for _ in range(90):
            await asyncio.sleep(1)
            exercise = await get_available_exercise(level, target, current_user.id, db)
            if exercise:
                return ReadingNextResponse(available=True, exercise=_build_exercise_out(exercise))
            if redis is not None and not await redis.exists(f"reading:generating:{level}:{target}"):
                break
    return ReadingNextResponse(available=False)


@router.post("/generate", response_model=ReadingGeneratingResponse, status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("5/minute")
async def generate_exercise(request: Request, background_tasks: BackgroundTasks, _maintenance: None = Depends(require_not_maintenance),
    plan: StudyPlan = Depends(get_active_study_plan), current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db), redis: Redis | None = Depends(get_redis)) -> ReadingGeneratingResponse:
    level, target = plan.cefr_level, plan.target_language
    if await get_available_exercise(level, target, current_user.id, db) is not None:
        return ReadingGeneratingResponse(status="generating")
    key, token = f"reading:generating:{level}:{target}", str(uuid4()) if redis is not None else ""
    if redis is not None and not await redis.set(key, token, nx=True, ex=300):
        return ReadingGeneratingResponse(status="generating")
    try:
        reservation = await reserve(current_user, "reading")
        background_tasks.add_task(_background_generate, level, target, key, reservation, token)
    except BaseException:
        await release_generation_lock(key, token)
        raise
    return ReadingGeneratingResponse(status="generating")


@router.post("/attempt", response_model=ReadingSubmitResponse)
@limiter.limit("20/minute")
async def submit_reading_attempt(request: Request, body: ReadingSubmitRequest, _maintenance: None = Depends(require_not_maintenance),
    plan: StudyPlan = Depends(get_active_study_plan), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> ReadingSubmitResponse:
    exercise = await db.get(ReadingExercise, body.exercise_id)
    if exercise is None or exercise.target_language != plan.target_language:
        raise HTTPException(status_code=404, detail="exercise_not_found")
    try:
        attempt, exercise = await submit_attempt(body.exercise_id, current_user.id, body.answers, db, is_replay=body.replay, study_plan_id=plan.id)
    except ValueError as exc:
        reason = str(exc)
        raise HTTPException(status_code=404 if reason == "exercise_not_found" else 409 if reason == "already_attempted" else 400, detail=reason) from exc
    return ReadingSubmitResponse(score=attempt.score, xp_earned=attempt.xp_earned,
        correct_answers=[CorrectAnswerOut(index=q["index"], correct=q["correct"]) for q in exercise.questions])


@router.get("/history", response_model=ReadingHistoryResponse)
@limiter.limit("60/minute")
async def get_reading_history(request: Request, _maintenance: None = Depends(require_not_maintenance),
    skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50), plan: StudyPlan = Depends(get_active_study_plan),
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> ReadingHistoryResponse:
    rows, total = await get_user_history(current_user.id, db, skip=skip, limit=limit, target_language=plan.target_language)
    items = [ReadingAttemptOut(id=attempt.id, score=attempt.score, xp_earned=attempt.xp_earned, completed_at=attempt.completed_at,
        exercise=_build_exercise_out(exercise), answers=attempt.answers,
        correct_answers=[CorrectAnswerOut(index=q["index"], correct=q["correct"]) for q in exercise.questions]) for attempt, exercise in rows]
    return ReadingHistoryResponse(items=items, total=total, skip=skip, limit=limit)

from collections import defaultdict
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.app_logger import get_logger
from app.core.database import get_db
from app.core.deps import get_active_study_plan, get_current_user, require_learner
from app.core.limiter import limiter
from app.models.flashcard import Flashcard
from app.models.lesson import Exercise, Lesson
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.models.user_language import UserLanguage
from app.schemas.study_plan import (GenerateStudyPlanRequest, PendingLessonResponse, PlanLessonResponse, StudyPlanResponse,
    TodayLesson, TodayResponse, LearningJourneyLessonResponse, LearningJourneyResponse, LearningJourneySectionResponse,
    LearningJourneyUnitResponse, LaunchLessonRequest)
from app.services.lesson_generator import generate_lesson
from app.services.exercise_factory import build_persisted_exercise_variants
from app.services.feature_quota_service import feature_quota
from app.services.study_plan_generator import generate_study_plan
from app.services.user_language_service import ensure_user_language, get_active_language
from app.services.progress_service import get_unit_competencies

logger = get_logger(__name__)
router = APIRouter(prefix="/api/study-plan", tags=["study-plan"], dependencies=[Depends(require_learner)])


def _get_weekly_plan_items(generated_plan: object) -> list:
    values = _get_plan_value(generated_plan, "weekly_plan")
    return [item for item in values if isinstance(item, dict) or hasattr(item, "week")] if isinstance(values, list) else []


def _get_week_days(week: object) -> list:
    values = _get_plan_value(week, "days")
    return values if isinstance(values, list) else []


def _get_plan_value(item: object, key: str, default: object = None) -> object:
    return item.get(key, default) if isinstance(item, dict) else getattr(item, key, default)


@router.get("/current", response_model=Optional[StudyPlanResponse])
@limiter.limit("60/minute")
async def get_current_plan(request: Request, language: str | None = Query(None), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if language:
        row = (await db.execute(select(UserLanguage).where(UserLanguage.user_id == current_user.id, UserLanguage.target_language == language))).scalar_one_or_none()
        if row is None:
            return None
        return (await db.execute(select(StudyPlan).where(StudyPlan.user_language_id == row.id, StudyPlan.is_active.is_(True)).order_by(StudyPlan.created_at.desc()).limit(1))).scalar_one_or_none()
    try:
        return await get_active_study_plan(current_user, db)
    except HTTPException:
        return None


@router.post("/generate", response_model=StudyPlanResponse)
@limiter.limit("10/minute")
async def create_study_plan(request: Request, data: GenerateStudyPlanRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    language = data.target_language
    if not language:
        active = await get_active_language(db, current_user.id)
        language = active.target_language if active else current_user.target_language
    user_language = await ensure_user_language(db, current_user.id, language)
    old_plans = (await db.execute(select(StudyPlan).where(StudyPlan.user_language_id == user_language.id, StudyPlan.is_active.is_(True)))).scalars().all()
    for old in old_plans:
        old.is_active = False
    generated = await generate_study_plan(data, target_language=language)
    from app.data.curriculum import get_curriculum_units
    units = get_curriculum_units(data.cefr_level, language)
    plan = StudyPlan(user_id=current_user.id, user_language_id=user_language.id, cefr_level=data.cefr_level,
        target_language=language, goals=data.goals, duration_weeks=data.duration_weeks, days_per_week=data.days_per_week,
        current_unit=units[0].id if units else "", generated_plan=generated.model_dump() if hasattr(generated, "model_dump") else generated, is_active=True)
    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return plan


@router.get("/today", response_model=TodayResponse)
@limiter.limit("20/minute")
async def get_today_lessons(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    empty = dict(plan_id=0, cefr_level="", lessons=[], progress_day=0, total_days=0, pending_count=0, review_due_count=0)
    active = await get_active_language(db, current_user.id)
    if not active:
        return empty
    plan = (await db.execute(select(StudyPlan).where(StudyPlan.user_language_id == active.id, StudyPlan.is_active.is_(True)))).scalar_one_or_none()
    if plan is None:
        return empty
    plan_id, user_id, native = plan.id, current_user.id, current_user.native_language
    total_days = plan.duration_weeks * plan.days_per_week
    due = (await db.execute(select(Flashcard.id).where(Flashcard.user_id == user_id, Flashcard.study_plan_id == plan_id, Flashcard.next_review <= date.today()))).scalars().all()
    all_lessons = (await db.execute(select(Lesson).where(Lesson.study_plan_id == plan_id))).scalars().all()
    lessons_by_day = defaultdict(list)
    for lesson in all_lessons:
        lessons_by_day[(lesson.week_number, lesson.day_number)].append(lesson)
    original = plan.progress_day
    while plan.progress_day < total_days:
        week = plan.progress_day // plan.days_per_week + 1
        day = plan.progress_day % plan.days_per_week + 1
        values = lessons_by_day.get((week, day), [])
        if values and all(item.is_completed for item in values):
            plan.progress_day += 1
        else:
            break
    if plan.progress_day != original:
        await db.commit()
    pending = sum(1 for item in all_lessons if not item.is_completed and _lesson_slot_index(item, plan.days_per_week) < plan.progress_day)
    def result(lessons):
        return TodayResponse(plan_id=plan_id, cefr_level=plan.cefr_level, lessons=lessons, progress_day=plan.progress_day,
            total_days=total_days, pending_count=pending, review_due_count=len(due))
    if plan.progress_day >= total_days:
        return result([])
    current_week, current_day = plan.progress_day // plan.days_per_week + 1, plan.progress_day % plan.days_per_week + 1
    weekly = _get_weekly_plan_items(plan.generated_plan)
    if not weekly:
        raise HTTPException(status_code=500, detail="Study plan data is malformed")
    week = next((item for item in weekly if _get_plan_value(item, "week") == current_week), None)
    if week is None:
        return result([])
    by_title = {item.title: (item.id, item.is_completed) for item in lessons_by_day.get((current_week, current_day), [])}
    today = []
    quota_error = None
    for day in _get_week_days(week):
        if _get_plan_value(day, "day") != current_day:
            continue
        title, kind = _get_plan_value(day, "title", ""), _get_plan_value(day, "lesson_type", "review")
        objectives, minutes, unit = _get_plan_value(day, "objectives", []), _get_plan_value(day, "estimated_minutes", 25), _get_plan_value(day, "unit_id", "")
        if not isinstance(title, str) or not title.strip():
            continue
        kind = kind if isinstance(kind, str) and kind.strip() else "review"
        objectives = [value for value in objectives if isinstance(value, str)] if isinstance(objectives, list) else []
        minutes = minutes if isinstance(minutes, int) and not isinstance(minutes, bool) and minutes > 0 else 25
        unit = unit if isinstance(unit, str) else ""
        lesson_id, completed = by_title.get(title, (None, False))
        if lesson_id is None:
            grammar, vocabulary = [], []
            if unit:
                from app.data.curriculum import get_curriculum_units
                curriculum = next((item for item in get_curriculum_units(plan.cefr_level, plan.target_language) if item.id == unit), None)
                if curriculum:
                    grammar, vocabulary = curriculum.grammar_points, curriculum.vocabulary_set_ids
            try:
                async with feature_quota(current_user, "lessons", db=db) as quota:
                    content = await generate_lesson(cefr_level=plan.cefr_level, lesson_type=kind, topic=title,
                        week=current_week, day=current_day, unit_id=unit, grammar_points=grammar, vocabulary_set_ids=vocabulary,
                        target_language=plan.target_language, native_language=native)
                    content_dict = content.model_dump() if hasattr(content, "model_dump") else content
                    exercises = build_persisted_exercise_variants(content_dict.get("exercises") or [])
                    if not exercises:
                        raise ValueError("Lesson generated with no valid exercises")
                    content_dict["exercises"] = exercises
                    lesson = Lesson(study_plan_id=plan_id, title=title, lesson_type=kind, cefr_level=plan.cefr_level,
                        week_number=current_week, day_number=current_day, unit_id=unit, content=content_dict)
                    db.add(lesson)
                    await db.flush()
                    for exercise in exercises:
                        db.add(Exercise(lesson_id=lesson.id, exercise_type=exercise.get("type", "multiple_choice"), question=exercise.get("question", ""),
                            options=exercise.get("options"), correct_answer=exercise.get("correct", ""), explanation=exercise.get("explanation")))
                    await quota.commit(db)
                    await db.refresh(lesson)
                    lesson_id = lesson.id
            except IntegrityError:
                await db.rollback()
                await db.refresh(plan)
                await db.refresh(current_user)
                duplicate = (await db.execute(select(Lesson).where(Lesson.study_plan_id == plan_id,
                    Lesson.week_number == current_week, Lesson.day_number == current_day, Lesson.title == title))).scalar_one_or_none()
                if duplicate:
                    lesson_id, completed = duplicate.id, duplicate.is_completed
            except HTTPException as exc:
                if exc.status_code != 402:
                    raise
                quota_error = exc
            except Exception:
                await db.rollback()
                await db.refresh(plan)
                await db.refresh(current_user)
                logger.exception("Failed to generate or persist lesson for plan %s", plan_id)
        if lesson_id is not None:
            today.append(TodayLesson(id=lesson_id, title=title, lesson_type=kind, week=current_week, day=current_day,
                objectives=objectives, estimated_minutes=minutes, unit_id=unit, is_completed=completed))
    if not today and quota_error is not None:
        raise quota_error
    return result(today)


@router.post("/skip-day")
@limiter.limit("60/minute")
async def skip_today(request: Request, plan: StudyPlan = Depends(get_active_study_plan), db: AsyncSession = Depends(get_db)):
    total = plan.duration_weeks * plan.days_per_week
    plan.progress_day = min(plan.progress_day + 1, total)
    await db.commit()
    return {"progress_day": plan.progress_day, "total_days": total}


@router.get("/pending-lessons", response_model=list[PendingLessonResponse])
@limiter.limit("60/minute")
async def get_pending_lessons(request: Request, plan: StudyPlan = Depends(get_active_study_plan), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Lesson).where(Lesson.study_plan_id == plan.id, Lesson.is_completed.is_(False)))).scalars().all()
    return [item for item in rows if _lesson_slot_index(item, plan.days_per_week) < plan.progress_day]


@router.get("/lessons", response_model=list[PlanLessonResponse])
@limiter.limit("60/minute")
async def get_plan_lessons(request: Request, plan: StudyPlan = Depends(get_active_study_plan), db: AsyncSession = Depends(get_db)):
    return (await db.execute(select(Lesson).where(Lesson.study_plan_id == plan.id).order_by(Lesson.week_number, Lesson.day_number, Lesson.id))).scalars().all()


def _lesson_slot_index(lesson: Lesson, days_per_week: int) -> int:
    return (lesson.week_number - 1) * days_per_week + lesson.day_number - 1


async def _learning_path_state(db: AsyncSession, user_id: int, plan: StudyPlan):
    from app.data.curriculum import get_curriculum_units
    units = get_curriculum_units(plan.cefr_level, plan.target_language)
    persisted = (await db.execute(select(Lesson).where(Lesson.study_plan_id == plan.id).order_by(Lesson.week_number, Lesson.day_number, Lesson.id))).scalars().all()
    by_unit = defaultdict(list)
    for lesson in persisted:
        if lesson.unit_id:
            by_unit[lesson.unit_id].append(lesson)
    competencies = {row["unit_id"]: row for row in await get_unit_competencies(db, user_id, study_plan_id=plan.id)}
    metadata, expected = {}, defaultdict(int)
    for week in _get_weekly_plan_items(plan.generated_plan):
        week_number = _get_plan_value(week, "week")
        for day in _get_week_days(week):
            number = _get_plan_value(day, "day")
            if isinstance(week_number, int) and isinstance(number, int):
                metadata[(week_number, number)] = {"title": _get_plan_value(day, "title", ""), "objectives": _get_plan_value(day, "objectives", []), "estimated_minutes": _get_plan_value(day, "estimated_minutes", 25)}
            unit = _get_plan_value(day, "unit_id")
            if isinstance(unit, str) and unit.strip():
                expected[unit] += 1
    completed_units = set()
    next_lesson_id = next_unit_id = None
    section_units = []
    for unit in units:
        lessons = by_unit.get(unit.id, [])
        data = competencies.get(unit.id, {})
        slots = expected.get(unit.id, len(lessons))
        complete = slots > 0 and sum(1 for item in lessons if item.is_completed) >= slots
        prerequisite = unit.prerequisite_unit is None or unit.prerequisite_unit in completed_units
        state = "completed" if complete else "active" if prerequisite and lessons else "available" if prerequisite else "locked"
        responses, prior_complete = [], True
        for lesson in sorted(lessons, key=lambda item: (_lesson_slot_index(item, plan.days_per_week), item.id)):
            available = state in {"active", "available"} and prior_complete
            meta = metadata.get((lesson.week_number, lesson.day_number), {})
            objectives = meta.get("objectives", [])
            objectives = [item for item in objectives if isinstance(item, str)] if isinstance(objectives, list) else []
            minutes = meta.get("estimated_minutes", 25)
            if isinstance(minutes, bool) or not isinstance(minutes, (int, float)) or minutes <= 0:
                minutes = 25
            responses.append(LearningJourneyLessonResponse(id=lesson.id, title=lesson.title, lesson_type=lesson.lesson_type,
                week_number=lesson.week_number, day_number=lesson.day_number, unit_id=unit.id, is_completed=lesson.is_completed,
                available=available, state="completed" if lesson.is_completed else "available" if available else "locked",
                objectives=objectives, estimated_minutes=int(minutes)))
            if not lesson.is_completed:
                prior_complete = False
                if available and next_lesson_id is None:
                    next_lesson_id, next_unit_id = lesson.id, unit.id
        section_units.append(LearningJourneyUnitResponse(id=unit.id, title=unit.title, level=unit.level, unit_number=unit.unit_number,
            prerequisite_unit=unit.prerequisite_unit, state=state, progress=round(float(data.get("score", 0)), 3),
            mastered_count=int(data.get("mastered_count", 0)), competency_count=int(data.get("total_count", len(unit.competency_checklist))), lessons=responses))
        if complete:
            completed_units.add(unit.id)
    section = LearningJourneySectionResponse(id=plan.cefr_level.lower(), title=f"{plan.cefr_level} Learning Section", level=plan.cefr_level,
        state="completed" if section_units and all(item.state == "completed" for item in section_units) else "active", units=section_units)
    return [section], next_lesson_id, next_unit_id


async def _current_plan_or_404(db, user):
    language = await get_active_language(db, user.id)
    if not language:
        raise HTTPException(status_code=404, detail="No active language set")
    plan = (await db.execute(select(StudyPlan).where(StudyPlan.user_language_id == language.id, StudyPlan.is_active.is_(True)))).scalar_one_or_none()
    if plan is None:
        raise HTTPException(status_code=404, detail="No active study plan found")
    return plan


@router.get("/learning-path", response_model=LearningJourneyResponse)
@limiter.limit("60/minute")
async def get_learning_path(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    plan = await _current_plan_or_404(db, current_user)
    sections, lesson, unit = await _learning_path_state(db, current_user.id, plan)
    return LearningJourneyResponse(plan_id=plan.id, target_language=plan.target_language, cefr_level=plan.cefr_level,
        current_unit=plan.current_unit, sections=sections, next_lesson_id=lesson, next_unit_id=unit)


@router.post("/launch-lesson")
@limiter.limit("20/minute")
async def launch_lesson(request: Request, data: LaunchLessonRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    plan = await _current_plan_or_404(db, current_user)
    lesson = (await db.execute(select(Lesson).where(Lesson.id == data.lesson_id, Lesson.study_plan_id == plan.id))).scalar_one_or_none()
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    sections, next_lesson, _ = await _learning_path_state(db, current_user.id, plan)
    requested = next((item for section in sections for unit in section.units for item in unit.lessons if item.id == lesson.id), None)
    if requested is None or (not requested.available and not lesson.is_completed):
        raise HTTPException(status_code=409, detail="Lesson is locked")
    return {"id":lesson.id, "title":lesson.title, "lesson_type":lesson.lesson_type, "unit_id":lesson.unit_id,
        "week_number":lesson.week_number, "day_number":lesson.day_number, "is_completed":lesson.is_completed, "next_lesson_id":next_lesson}

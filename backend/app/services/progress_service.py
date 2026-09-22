from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.competency import UserCompetency
from app.models.learning_goal import LearningGoal
from app.models.learning_goal_milestone import LearningGoalMilestone
from app.models.progress import Progress

XP_LESSON_COMPLETE = 20
XP_EXERCISE_CORRECT = 5
XP_EXERCISE_WRONG = 1
XP_FLASHCARD_REVIEW = 2
GOAL_DAILY_REWARD_XP = 25
GOAL_WEEKLY_REWARD_XP = 75


async def update_daily_progress(
    db: AsyncSession,
    user_id: int,
    *,
    study_plan_id: int,
    lesson_completed: bool = False,
    exercise_correct: bool | None = None,
    exercise_total_delta: int = 0,
    exercise_correct_delta: int = 0,
    activity_recorded: bool = False,
    flashcard_reviewed: bool = False,
    xp: int = 0,
    skill: str | None = None,
    skill_score: float | None = None,
    commit: bool = True,
) -> Progress | None:
    # Do not create a progress row (and therefore do not start/advance a streak)
    # for a call that records no learning activity. This matters for idempotent
    # or empty API calls such as a game submission with zero XP/questions.
    has_activity = (
        lesson_completed
        or exercise_correct is not None
        or exercise_total_delta > 0
        or exercise_correct_delta > 0
        or activity_recorded
        or flashcard_reviewed
        or xp > 0
        or (skill is not None and skill_score is not None)
    )
    if not has_activity:
        return None

    today = date.today()

    base_filter = [
        Progress.user_id == user_id,
        Progress.study_plan_id == study_plan_id,
    ]

    result = await db.execute(select(Progress).where(*base_filter, Progress.date == today))
    entry = result.scalar_one_or_none()

    if not entry:
        yesterday = today - timedelta(days=1)
        yest_result = await db.execute(
            select(Progress).where(*base_filter, Progress.date == yesterday)
        )
        yest = yest_result.scalar_one_or_none()
        streak = (yest.streak_day + 1) if yest else 1

        entry = Progress(
            user_id=user_id,
            date=today,
            xp_earned=0,
            reward_xp=0,
            lessons_completed=0,
            exercises_correct=0,
            exercises_total=0,
            streak_day=streak,
            skills={},
            study_plan_id=study_plan_id,
        )
        try:
            async with db.begin_nested():
                db.add(entry)
                await db.flush()
        except IntegrityError:
            # Another request may have created today's row concurrently.
            # The savepoint keeps the outer transaction usable; reload the
            # canonical row and continue accumulating activity on it.
            result = await db.execute(
                select(Progress).where(*base_filter, Progress.date == today)
            )
            entry = result.scalar_one()

    if lesson_completed:
        entry.lessons_completed += 1
        entry.xp_earned += XP_LESSON_COMPLETE

    if exercise_correct is not None:
        entry.exercises_total += 1
        if exercise_correct:
            entry.exercises_correct += 1
            entry.xp_earned += XP_EXERCISE_CORRECT
        else:
            entry.xp_earned += XP_EXERCISE_WRONG

    if exercise_total_delta > 0:
        entry.exercises_total += exercise_total_delta
    if exercise_correct_delta > 0:
        entry.exercises_correct += min(exercise_correct_delta, exercise_total_delta or exercise_correct_delta)

    if flashcard_reviewed:
        entry.xp_earned += XP_FLASHCARD_REVIEW

    if xp > 0:
        entry.xp_earned += xp

    if skill and skill_score is not None:
        skills = dict(entry.skills or {})
        old = skills.get(skill, skill_score)
        skills[skill] = round(old * 0.7 + skill_score * 0.3, 3)
        entry.skills = skills

    # Goal rewards are awarded exactly once per period and are calculated
    # against learning XP before the reward itself is added.
    goal_result = await db.execute(
        select(LearningGoal).where(
            LearningGoal.user_id == user_id,
            LearningGoal.study_plan_id == study_plan_id,
        ).with_for_update()
    )
    goal = goal_result.scalar_one_or_none()
    if goal is None:
        goal = LearningGoal(
            user_id=user_id,
            study_plan_id=study_plan_id,
            daily_xp_target=50,
            weekly_xp_target=250,
        )
        try:
            async with db.begin_nested():
                db.add(goal)
                await db.flush()
        except IntegrityError:
            goal_result = await db.execute(
                select(LearningGoal).where(
                    LearningGoal.user_id == user_id,
                    LearningGoal.study_plan_id == study_plan_id,
                )
            )
            goal = goal_result.scalar_one()

    week_start = today - timedelta(days=today.weekday())
    weekly_result = await db.execute(
        select(Progress.xp_earned).where(
            Progress.user_id == user_id,
            Progress.study_plan_id == study_plan_id,
            Progress.date >= week_start,
            Progress.date <= today,
        )
    )
    weekly_xp_result = await db.execute(
        select(Progress.xp_earned, Progress.reward_xp).where(
            Progress.user_id == user_id,
            Progress.study_plan_id == study_plan_id,
            Progress.date >= week_start,
            Progress.date <= today,
        )
    )
    weekly_xp_before_rewards = sum(
        max(xp - reward_xp, 0) for xp, reward_xp in weekly_xp_result.all()
    )
    daily_activity_xp = max(entry.xp_earned - entry.reward_xp, 0)

    if daily_activity_xp >= goal.daily_xp_target and goal.daily_reward_date != today:
        achieved_xp = daily_activity_xp
        entry.xp_earned += GOAL_DAILY_REWARD_XP
        entry.reward_xp += GOAL_DAILY_REWARD_XP
        goal.daily_reward_date = today
        db.add(
            LearningGoalMilestone(
                user_id=user_id,
                study_plan_id=study_plan_id,
                goal_type="daily",
                period_start=today,
                period_end=today,
                target_xp=goal.daily_xp_target,
                achieved_xp=achieved_xp,
                reward_xp=GOAL_DAILY_REWARD_XP,
            )
        )

    if weekly_xp_before_rewards >= goal.weekly_xp_target and goal.weekly_reward_start != week_start:
        entry.xp_earned += GOAL_WEEKLY_REWARD_XP
        entry.reward_xp += GOAL_WEEKLY_REWARD_XP
        goal.weekly_reward_start = week_start
        db.add(
            LearningGoalMilestone(
                user_id=user_id,
                study_plan_id=study_plan_id,
                goal_type="weekly",
                period_start=week_start,
                period_end=week_start + timedelta(days=6),
                target_xp=goal.weekly_xp_target,
                achieved_xp=weekly_xp_before_rewards,
                reward_xp=GOAL_WEEKLY_REWARD_XP,
            )
        )

    if commit:
        await db.commit()
        await db.refresh(entry)
    else:
        await db.flush()
    return entry


async def upsert_unit_competency(
    db: AsyncSession,
    user_id: int,
    unit_id: str,
    competency_texts: list[str],
    lesson_score: float,
    *,
    study_plan_id: int,
) -> None:
    """
    Update (or create) UserCompetency rows for all competencies in a unit.

    Uses an exponential moving average:  new = 0.7 * old + 0.3 * lesson_score
    Marks a competency as mastered when score >= 0.80.
    """
    if not unit_id or not competency_texts:
        return

    now = datetime.now(UTC).replace(tzinfo=None)

    for text in competency_texts:
        result = await db.execute(
            select(UserCompetency).where(
                UserCompetency.user_id == user_id,
                UserCompetency.unit_id == unit_id,
                UserCompetency.competency_text == text,
                UserCompetency.study_plan_id == study_plan_id,
            )
        )
        row: UserCompetency | None = result.scalar_one_or_none()

        if row is None:
            row = UserCompetency(
                user_id=user_id,
                unit_id=unit_id,
                competency_text=text,
                score=lesson_score,
                mastered=lesson_score >= 0.80,
                updated_at=now,
                study_plan_id=study_plan_id,
            )
            db.add(row)
        else:
            row.score = round(row.score * 0.7 + lesson_score * 0.3, 3)
            row.mastered = row.score >= 0.80
            row.updated_at = now

    await db.flush()


async def get_unit_competencies(
    db: AsyncSession,
    user_id: int,
    study_plan_id: int | None = None,
) -> list[dict]:
    """Return aggregated competency scores per unit for the given user."""
    conditions = [UserCompetency.user_id == user_id]
    if study_plan_id is not None:
        conditions.append(UserCompetency.study_plan_id == study_plan_id)
    result = await db.execute(
        select(UserCompetency).where(*conditions).order_by(
            UserCompetency.unit_id, UserCompetency.competency_text
        )
    )
    rows = result.scalars().all()

    # Aggregate per unit in one pass to avoid repeatedly scanning all rows.
    unit_scores: dict[str, list[float]] = {}
    mastered_counts: dict[str, int] = {}
    for row in rows:
        unit_scores.setdefault(row.unit_id, []).append(row.score)
        if row.mastered:
            mastered_counts[row.unit_id] = mastered_counts.get(row.unit_id, 0) + 1

    return [
        {
            "unit_id": uid,
            "score": round(sum(scores) / len(scores), 3),
            "mastered_count": mastered_counts.get(uid, 0),
            "total_count": len(scores),
        }
        for uid, scores in unit_scores.items()
    ]

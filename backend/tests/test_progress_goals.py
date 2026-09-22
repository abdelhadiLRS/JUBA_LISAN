from datetime import date, timedelta

import pytest
from sqlalchemy import select


@pytest.mark.asyncio
async def test_learning_goals_default_and_progress(client, test_user, db_session):
    user, headers = test_user
    from app.models.progress import Progress
    from tests.conftest import make_study_plan

    plan = await make_study_plan(\n        db_session, user_id=user.id, cefr_level="A1", target_language="en-US", goals=["grammar"], duration_weeks=4, days_per_week=4, current_unit="", generated_plan={}, is_active=True\n    )\n    db_session.add_all([
        Progress(user_id=user.id, study_plan_id=plan.id, date=date.today(), xp_earned=30, skills={}),
        Progress(user_id=user.id, study_plan_id=plan.id, date=date.today() - timedelta(days=2), xp_earned=40, skills={}),
    ])
    await db_session.commit()

    response = await client.get("/api/progress/goals", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["daily_xp_target"] == 50
    assert data["weekly_xp_target"] == 250
    assert data["daily_xp"] == 30
    assert data["weekly_xp"] == 70
    assert data["daily_completed"] is False
    assert data["weekly_completed"] is False


@pytest.mark.asyncio
async def test_learning_goals_update_persists(client, test_user, db_session):
    user, headers = test_user
    from tests.conftest import make_study_plan

    await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )

    response = await client.put(
        "/api/progress/goals",
        json={"daily_xp_target": 80, "weekly_xp_target": 400},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["daily_xp_target"] == 80
    assert response.json()["weekly_xp_target"] == 400

    response = await client.get("/api/progress/goals", headers=headers)
    assert response.status_code == 200
    assert response.json()["daily_xp_target"] == 80
    assert response.json()["weekly_xp_target"] == 400


@pytest.mark.asyncio
async def test_learning_goals_reject_invalid_targets(client, test_user):
    _, headers = test_user
    response = await client.put(
        "/api/progress/goals",
        json={"daily_xp_target": 0, "weekly_xp_target": 250},
        headers=headers,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_daily_goal_reward_is_claimed_once(db_session, test_user):
    from app.models.progress import Progress
    from app.services.progress_service import update_daily_progress
    from tests.conftest import make_study_plan

    user, _ = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    db_session.add(
        Progress(
            user_id=user.id,
            study_plan_id=plan.id,
            date=date.today(),
            xp_earned=45,
            lessons_completed=0,
            exercises_correct=0,
            exercises_total=0,
            streak_day=1,
            skills={},
        )
    )
    await db_session.commit()

    first = await update_daily_progress(
        db_session,
        user.id,
        study_plan_id=plan.id,
        xp=5,
        commit=True,
    )
    assert first is not None
    assert first.xp_earned == 75

    second = await update_daily_progress(
        db_session,
        user.id,
        study_plan_id=plan.id,
        xp=5,
        commit=True,
    )
    assert second is not None
    assert second.xp_earned == 80


@pytest.mark.asyncio
async def test_goal_rewards_do_not_count_toward_learning_goal_xp(db_session, test_user):
    from app.models.learning_goal import LearningGoal
    from app.models.learning_goal_milestone import LearningGoalMilestone
    from app.models.progress import Progress
    from app.services.progress_service import update_daily_progress
    from tests.conftest import make_study_plan

    user, _ = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    db_session.add(LearningGoal(
        user_id=user.id,
        study_plan_id=plan.id,
        daily_xp_target=1000,
        weekly_xp_target=250,
    ))
    db_session.add(Progress(
        user_id=user.id,
        study_plan_id=plan.id,
        date=date.today() - timedelta(days=1),
        xp_earned=275,
        reward_xp=75,
        lessons_completed=0,
        exercises_correct=0,
        exercises_total=0,
        streak_day=1,
        skills={},
    ))
    await db_session.commit()

    result = await update_daily_progress(
        db_session, user.id, study_plan_id=plan.id, xp=5, commit=True
    )
    assert result is not None
    assert result.reward_xp == 0

    milestones = (
        await db_session.execute(
            select(LearningGoalMilestone).where(
                LearningGoalMilestone.user_id == user.id,
                LearningGoalMilestone.study_plan_id == plan.id,
            )
        )
    ).scalars().all()
    assert milestones == []


@pytest.mark.asyncio
async def test_goal_milestone_history_records_daily_and_weekly_rewards(client, test_user, db_session):
    from app.models.learning_goal_milestone import LearningGoalMilestone
    from app.models.progress import Progress
    from app.models.learning_goal import LearningGoal
    from app.services.progress_service import update_daily_progress
    from tests.conftest import make_study_plan

    user, headers = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    goal = LearningGoal(
        user_id=user.id,
        study_plan_id=plan.id,
        daily_xp_target=50,
        weekly_xp_target=60,
    )
    db_session.add(goal)
    db_session.add(
        Progress(
            user_id=user.id,
            study_plan_id=plan.id,
            date=date.today(),
            xp_earned=55,
            lessons_completed=0,
            exercises_correct=0,
            exercises_total=0,
            streak_day=1,
            skills={},
        )
    )
    await db_session.commit()

    result = await update_daily_progress(
        db_session,
        user.id,
        study_plan_id=plan.id,
        xp=5,
        commit=True,
    )
    assert result is not None

    rows = (
        await db_session.execute(
            select(LearningGoalMilestone).where(
                LearningGoalMilestone.user_id == user.id,
                LearningGoalMilestone.study_plan_id == plan.id,
            )
        )
    ).scalars().all()
    assert {(row.goal_type, row.reward_xp) for row in rows} == {
        ("daily", 25),
        ("weekly", 75),
    }

    response = await client.get("/api/progress/goals/history", headers=headers)
    assert response.status_code == 200
    history = response.json()
    assert len(history) == 2
    assert {item["goal_type"] for item in history} == {"daily", "weekly"}
    assert all(item["target_xp"] in {50, 60} for item in history)


@pytest.mark.asyncio
async def test_goal_milestone_summary_counts_rewards(client, test_user, db_session):
    from app.models.learning_goal_milestone import LearningGoalMilestone
    from tests.conftest import make_study_plan

    user, headers = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    db_session.add_all([
        LearningGoalMilestone(
            user_id=user.id, study_plan_id=plan.id, goal_type="daily",
            period_start=date.today(), period_end=date.today(),
            target_xp=50, achieved_xp=55, reward_xp=25,
        ),
        LearningGoalMilestone(
            user_id=user.id, study_plan_id=plan.id, goal_type="weekly",
            period_start=date.today(), period_end=date.today() + timedelta(days=6),
            target_xp=250, achieved_xp=260, reward_xp=75,
        ),
    ])
    await db_session.commit()

    response = await client.get("/api/progress/goals/milestones/summary", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "total_milestones": 2,
        "daily_milestones": 1,
        "weekly_milestones": 1,
        "total_reward_xp": 100,
        "daily_reward_xp": 25,
        "weekly_reward_xp": 75,
    }


@pytest.mark.asyncio
async def test_goal_milestone_history_is_user_scoped(client, test_user, db_session):
    from app.models.learning_goal_milestone import LearningGoalMilestone
    from app.core.security import hash_password
    from app.models.user import User
    from app.models.user_language import UserLanguage
    from tests.conftest import make_study_plan

    user, headers = test_user
    other = User(
        username="othergoalhistory",
        email="other-goal-history@example.com",
        display_name="Other Goal History",
        hashed_password=hash_password("test-password"),
        role="user",
        native_language="es",
        target_language="fr-FR",
        is_active=True,
    )
    db_session.add(other)
    await db_session.flush()
    db_session.add(UserLanguage(user_id=other.id, target_language="fr-FR", is_active=True))
    other_plan = await make_study_plan(
        db_session,
        user_id=other.id,
        cefr_level="A1",
        target_language="fr-FR",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    db_session.add(
        LearningGoalMilestone(
            user_id=other.id,
            study_plan_id=other_plan.id,
            goal_type="daily",
            period_start=date.today(),
            period_end=date.today(),
            target_xp=50,
            achieved_xp=60,
            reward_xp=25,
        )
    )
    await db_session.commit()

    response = await client.get("/api/progress/goals/history", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_goal_response_excludes_reward_xp(client, test_user, db_session):
    user, headers = test_user
    from app.models.progress import Progress
    from app.models.learning_goal import LearningGoal
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    db_session.add(LearningGoal(
        user_id=user.id, study_plan_id=plan.id,
        daily_xp_target=100, weekly_xp_target=300,
    ))
    db_session.add(Progress(
        user_id=user.id, study_plan_id=plan.id, date=date.today(),
        xp_earned=125, reward_xp=75, skills={},
    ))
    await db_session.commit()

    response = await client.get("/api/progress/goals", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["daily_xp"] == 50
    assert data["weekly_xp"] == 50
    assert data["daily_completed"] is False
    assert data["daily_reward_claimed"] is False

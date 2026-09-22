from datetime import date, timedelta

import pytest


@pytest.mark.asyncio
async def test_learning_goals_default_and_progress(client, test_user, db_session):
    user, headers = test_user
    from app.models.progress import Progress
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
    db_session.add_all([
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

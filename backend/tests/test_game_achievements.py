from datetime import date

import pytest
from sqlalchemy import select

from app.models.game_progress import GameProgress
from app.models.game_session import GameSession
from app.models.progress import Progress
from tests.conftest import make_study_plan


async def _start_perfect_round(client, headers, db_session, game_id="math"):
    started = await client.post(
        "/api/progress/game-session",
        json={"game_id": game_id, "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    for question in session.questions:
        question["answer"] = question["choices"][0]
    await db_session.commit()

    answers = [
        {"question_id": question["id"], "choice": question["choices"][0]}
        for question in payload["questions"]
    ]
    completed = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=headers,
    )
    assert completed.status_code == 200
    return completed.json()


@pytest.mark.asyncio
async def test_game_achievement_thresholds_are_awarded_when_crossed(
    client, test_user, db_session
):
    user, headers = test_user
    await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )

    result = await _start_perfect_round(client, headers, db_session)

    assert {"first_game", "perfect_round", "xp_100"}.issubset(
        set(result["new_achievements"])
    )
    assert result["xp_earned"] == 125
    assert result["total_xp"] == 125

    game_progress = (
        await db_session.execute(
            select(GameProgress).where(GameProgress.user_id == user.id)
        )
    ).scalar_one()
    assert game_progress.achievements.count("xp_100") == 1


@pytest.mark.asyncio
async def test_game_achievements_are_not_repaid_on_later_rounds(
    client, test_user, db_session
):
    user, headers = test_user
    await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )

    first = await _start_perfect_round(client, headers, db_session)
    second = await _start_perfect_round(client, headers, db_session)

    assert first["new_achievements"]
    assert second["new_achievements"] == []
    assert second["xp_earned"] == 25
    assert second["total_xp"] == 150

    game_progress = (
        await db_session.execute(
            select(GameProgress).where(GameProgress.user_id == user.id)
        )
    ).scalar_one()
    assert len(game_progress.achievements) == len(set(game_progress.achievements))


@pytest.mark.asyncio
async def test_game_achievement_xp_500_can_be_crossed_in_one_round(
    client, test_user, db_session
):
    user, headers = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )
    db_session.add(
        Progress(
            user_id=user.id,
            study_plan_id=plan.id,
            date=date.today(),
            xp_earned=425,
            lessons_completed=0,
            exercises_correct=0,
            exercises_total=0,
            streak_day=1,
            skills={},
        )
    )
    await db_session.commit()

    result = await _start_perfect_round(client, headers, db_session)

    assert {"xp_100", "xp_500"}.issubset(set(result["new_achievements"]))
    assert result["xp_earned"] == 225
    assert result["total_xp"] == 650

    game_progress = (
        await db_session.execute(
            select(GameProgress).where(GameProgress.user_id == user.id)
        )
    ).scalar_one()
    assert game_progress.achievements.count("xp_100") == 1
    assert game_progress.achievements.count("xp_500") == 1

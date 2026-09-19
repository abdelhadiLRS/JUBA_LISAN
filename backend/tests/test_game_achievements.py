from datetime import UTC, date, datetime, timedelta

import pytest
from sqlalchemy import select

from app.models.game_progress import GameProgress
from app.models.game_progress_event import GameProgressEvent
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


@pytest.mark.asyncio
async def test_daily_challenge_is_counted_once_per_day(
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

    first_started = await client.post(
        "/api/progress/game-session",
        json={"game_id": "math", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert first_started.status_code == 200
    first_payload = first_started.json()
    first_session = await db_session.get(GameSession, first_payload["session_id"])
    assert first_session is not None
    for question in first_session.questions:
        question["answer"] = question["choices"][0]
    await db_session.commit()

    answers = [
        {"question_id": question["id"], "choice": question["choices"][0]}
        for question in first_payload["questions"]
    ]
    daily_date = date.today().isoformat()
    first = await client.post(
        "/api/progress/game-session/complete",
        json={
            "session_id": first_payload["session_id"],
            "answers": answers,
            "daily_challenge": True,
            "daily_challenge_date": daily_date,
        },
        headers=headers,
    )
    assert first.status_code == 200
    assert "daily_challenge" in first.json()["new_achievements"]
    assert first.json()["daily_challenges_completed"] == 1

    second = await _start_perfect_round(client, headers, db_session)
    assert "daily_challenge" not in second["new_achievements"]

    game_progress = (
        await db_session.execute(
            select(GameProgress).where(GameProgress.user_id == user.id)
        )
    ).scalar_one()
    assert game_progress.daily_challenges_completed == 1
    assert game_progress.last_daily_challenge_date == daily_date
    assert game_progress.achievements.count("daily_challenge") == 1


@pytest.mark.asyncio
async def test_game_progress_row_is_initialized_once_for_multiple_sessions(
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

    first = await client.post(
        "/api/progress/game-session",
        json={"game_id": "math", "language": "en", "difficulty": 1},
        headers=headers,
    )
    second = await client.post(
        "/api/progress/game-session",
        json={"game_id": "math", "language": "en", "difficulty": 1},
        headers=headers,
    )

    assert first.status_code == 200
    assert second.status_code == 200

    rows = (
        await db_session.execute(
            select(GameProgress).where(
                GameProgress.user_id == user.id,
            )
        )
    ).scalars().all()

    assert len(rows) == 1
    assert rows[0].games_played == 0
    assert rows[0].achievements == []


@pytest.mark.asyncio
async def test_duplicate_game_progress_insert_isolated_from_session_creation(
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

    first = await client.post(
        "/api/progress/game-session",
        json={"game_id": "math", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert first.status_code == 200

    # A second session must remain creatable even though its GameProgress
    # initialization hits the unique (user_id, study_plan_id) constraint.
    second = await client.post(
        "/api/progress/game-session",
        json={"game_id": "math", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert second.status_code == 200

    sessions = (
        await db_session.execute(
            select(GameSession).where(
                GameSession.user_id == user.id,
            )
        )
    ).scalars().all()
    assert len(sessions) == 2


@pytest.mark.asyncio
async def test_replayed_game_session_does_not_duplicate_progress_or_event(
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

    started = await client.post(
        "/api/progress/game-session",
        json={"game_id": "math", "language": "en", "difficulty": 1},
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
    first = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=headers,
    )
    assert first.status_code == 200

    replay = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=headers,
    )
    assert replay.status_code == 409

    game_progress = (
        await db_session.execute(
            select(GameProgress).where(GameProgress.user_id == user.id)
        )
    ).scalar_one()
    events = (
        await db_session.execute(
            select(GameProgressEvent).where(GameProgressEvent.user_id == user.id)
        )
    ).scalars().all()
    progress_rows = (
        await db_session.execute(
            select(Progress).where(
                Progress.user_id == user.id,
                Progress.study_plan_id == session.study_plan_id,
            )
        )
    ).scalars().all()

    assert game_progress.games_played == 1
    assert game_progress.questions_answered == 5
    assert game_progress.correct_answers == 5
    assert len(events) == 1
    assert events[0].event_id == payload["session_id"]
    assert events[0].xp_earned == first.json()["xp_earned"]
    assert sum(row.xp_earned for row in progress_rows) == first.json()["xp_earned"]


@pytest.mark.asyncio
async def test_duplicate_event_conflict_rolls_back_game_completion(
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

    started = await client.post(
        "/api/progress/game-session",
        json={"game_id": "math", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    for question in session.questions:
        question["answer"] = question["choices"][0]
    db_session.add(
        GameProgressEvent(
            event_id=payload["session_id"],
            user_id=user.id,
            study_plan_id=plan.id,
            game_id="math",
            questions_answered=0,
            correct_answers=0,
            round_score=0,
            daily_challenge=False,
            daily_challenge_date="",
            achievements=[],
            xp_earned=0,
        )
    )
    await db_session.commit()

    answers = [
        {"question_id": question["id"], "choice": question["choices"][0]}
        for question in payload["questions"]
    ]
    result = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=headers,
    )
    assert result.status_code == 409
    assert result.json()["detail"] == "Game completion already recorded"

    await db_session.refresh(session)
    assert session.completed is False

    game_progress = (
        await db_session.execute(
            select(GameProgress).where(
                GameProgress.user_id == user.id,
                GameProgress.study_plan_id == plan.id,
            )
        )
    ).scalar_one()
    assert game_progress.games_played == 0
    assert game_progress.questions_answered == 0
    assert game_progress.correct_answers == 0

    progress_rows = (
        await db_session.execute(
            select(Progress).where(
                Progress.user_id == user.id,
                Progress.study_plan_id == plan.id,
            )
        )
    ).scalars().all()
    assert progress_rows == []


@pytest.mark.asyncio
async def test_game_session_expiry_is_rechecked_after_write_phase_starts(
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

    started = await client.post(
        "/api/progress/game-session",
        json={"game_id": "math", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    session.expires_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(seconds=1)
    await db_session.commit()

    answers = [
        {"question_id": question["id"], "choice": question["choices"][0]}
        for question in payload["questions"]
    ]
    result = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=headers,
    )
    assert result.status_code == 410
    assert result.json()["detail"] == "Game session expired"

    await db_session.refresh(session)
    assert session.completed is False

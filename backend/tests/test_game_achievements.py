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
async def test_game_xp_is_scoped_to_the_active_study_plan(
    client, test_user, db_session
):
    user, headers = test_user
    inactive_plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=False,
    )
    active_plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A2",
        goals=["conversation"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A2-u1",
        generated_plan={},
        is_active=True,
    )
    db_session.add(
        Progress(
            user_id=user.id,
            study_plan_id=inactive_plan.id,
            date=date.today(),
            xp_earned=900,
            lessons_completed=0,
            exercises_correct=0,
            exercises_total=0,
            streak_day=1,
            skills={},
        )
    )
    await db_session.commit()

    summary = await client.get("/api/progress/game-summary", headers=headers)
    assert summary.status_code == 200
    assert summary.json()["total_xp"] == 0

    result = await _start_perfect_round(client, headers, db_session)

    assert result["total_xp"] == result["xp_earned"]
    assert result["total_xp"] < 900
    assert "xp_500" not in result["new_achievements"]

    active_progress = (
        await db_session.execute(
            select(Progress).where(
                Progress.user_id == user.id,
                Progress.study_plan_id == active_plan.id,
            )
        )
    ).scalars().all()
    inactive_progress = (
        await db_session.execute(
            select(Progress).where(
                Progress.user_id == user.id,
                Progress.study_plan_id == inactive_plan.id,
            )
        )
    ).scalars().all()

    assert sum(row.xp_earned for row in active_progress) == result["xp_earned"]
    assert sum(row.xp_earned for row in inactive_progress) == 900


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
    assert result["xp_earned"] == 165
    assert result["total_xp"] == 165

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
    assert second["total_xp"] == 190

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
    assert result["xp_earned"] == 265
    assert result["total_xp"] == 690

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
async def test_game_progress_is_created_only_after_valid_completion(
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
            select(GameProgress).where(GameProgress.user_id == user.id)
        )
    ).scalars().all()
    assert rows == []


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

    # A second session remains creatable because aggregate persistence is
    # deferred until a completion has passed validation.
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
    study_plan_id = session.study_plan_id
    progress_rows = (
        await db_session.execute(
            select(Progress).where(
                Progress.user_id == user.id,
                Progress.study_plan_id == study_plan_id,
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

    persisted_session = await db_session.get(GameSession, payload["session_id"])
    assert persisted_session is not None
    await db_session.refresh(persisted_session)
    assert persisted_session.completed is False

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
async def test_game_completion_uses_captured_ownership_after_rollback(
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
    result = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=headers,
    )

    assert result.status_code == 200
    assert result.json()["total_xp"] > 0

    progress_rows = (
        await db_session.execute(
            select(Progress).where(
                Progress.user_id == user.id,
                Progress.study_plan_id == session.study_plan_id,
            )
        )
    ).scalars().all()
    assert sum(row.xp_earned for row in progress_rows) == result.json()["xp_earned"]


def test_game_session_complete_rejects_malformed_daily_challenge_date():
    from pydantic import ValidationError

    from app.schemas.progress import GameSessionComplete

    with pytest.raises(ValidationError):
        GameSessionComplete(
            session_id="session-1",
            daily_challenge=True,
            daily_challenge_date="20-09-2026",
        )


def test_game_session_complete_accepts_iso_daily_challenge_date():
    from app.schemas.progress import GameSessionComplete

    payload = GameSessionComplete(
        session_id="session-1",
        daily_challenge=True,
        daily_challenge_date="2026-09-20",
    )

    assert payload.daily_challenge_date == "2026-09-20"


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

@pytest.mark.asyncio
async def test_interactive_completion_rejects_answer_payload(
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
        json={"game_id": "memory", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()

    result = await client.post(
        "/api/progress/game-session/complete",
        json={
            "session_id": payload["session_id"],
            "answers": [{"question_id": "ignored", "choice": "ignored"}],
            "interaction_trace": [],
        },
        headers=headers,
    )

    assert result.status_code == 422
    assert "interaction_trace" in result.json()["detail"]


@pytest.mark.asyncio
async def test_interactive_attempts_do_not_inflate_scored_questions_or_xp(
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
        json={"game_id": "memory", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()
    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None

    solution = session.questions[0]["interaction"]["solution"]
    cards_by_pair = {}
    for card_id, pair_id in solution["pairs"].items():
        cards_by_pair.setdefault(pair_id, []).append(card_id)
    correct_pairs = list(cards_by_pair.values())
    assert len(correct_pairs) == solution["pair_count"]

    trace = [
        {"first": pair[0], "second": pair[1]}
        for pair in correct_pairs
    ]
    wrong_pair = {"first": correct_pairs[0][0], "second": correct_pairs[1][0]}
    trace.extend([wrong_pair] * 20)

    result = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "interaction_trace": trace},
        headers=headers,
    )

    assert result.status_code == 200
    body = result.json()
    assert body["round_correct"] == solution["pair_count"]
    assert body["round_questions"] == solution["pair_count"]
    assert body["round_score"] == 25
    assert body["xp_earned"] == solution["pair_count"] * 5 + 75
    assert body["total_xp"] == body["xp_earned"]

    game_progress = (
        await db_session.execute(
            select(GameProgress).where(
                GameProgress.user_id == user.id,
                GameProgress.study_plan_id == plan.id,
            )
        )
    ).scalar_one()
    assert game_progress.questions_answered == solution["pair_count"]


@pytest.mark.asyncio
async def test_matching_attempts_do_not_inflate_scored_questions_or_xp(
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
        json={"game_id": "matching", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()
    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None

    solution = session.questions[0]["interaction"]["solution"]
    pairs = solution["pairs"]
    correct = [{"left": left_id, "right": right_id} for left_id, right_id in pairs.items()]
    wrong = {"left": correct[0]["left"], "right": correct[1]["right"]}

    result = await client.post(
        "/api/progress/game-session/complete",
        json={
            "session_id": payload["session_id"],
            "interaction_trace": [wrong] * 20 + correct,
        },
        headers=headers,
    )

    assert result.status_code == 200
    body = result.json()
    assert body["round_correct"] == solution["pair_count"]
    assert body["round_questions"] == solution["pair_count"]
    assert body["round_score"] == 25
    assert body["xp_earned"] == solution["pair_count"] * 5 + 75

    game_progress = (
        await db_session.execute(
            select(GameProgress).where(
                GameProgress.user_id == user.id,
                GameProgress.study_plan_id == plan.id,
            )
        )
    ).scalar_one()
    assert game_progress.questions_answered == solution["pair_count"]


@pytest.mark.asyncio
async def test_ordering_attempts_do_not_inflate_scored_questions_or_xp(
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
        json={"game_id": "ordering", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()
    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None

    solution = session.questions[0]["interaction"]["solution"]
    target = solution["target"]
    rotated = target[1:] + target[:1]

    result = await client.post(
        "/api/progress/game-session/complete",
        json={
            "session_id": payload["session_id"],
            "interaction_trace": [{"order": rotated}] * 20 + [{"order": target}],
        },
        headers=headers,
    )

    assert result.status_code == 200
    body = result.json()
    assert body["round_correct"] == 1
    assert body["round_questions"] == 1
    assert body["round_score"] == 25
    assert body["xp_earned"] == 80

    game_progress = (
        await db_session.execute(
            select(GameProgress).where(
                GameProgress.user_id == user.id,
                GameProgress.study_plan_id == plan.id,
            )
        )
    ).scalar_one()
    assert game_progress.questions_answered == 1


@pytest.mark.asyncio
async def test_game_session_cannot_be_completed_by_another_user(
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

    from app.core.security import create_access_token, hash_password
    from app.models.user import User
    from app.models.user_language import UserLanguage

    other = User(
        username="other-game-user",
        email="other-game-user@example.com",
        display_name="Other Game User",
        hashed_password=hash_password("otherpass"),
        role="user",
        native_language="fr",
        target_language="en-US",
        is_active=True,
    )
    db_session.add(other)
    await db_session.flush()
    db_session.add(UserLanguage(user_id=other.id, target_language="en-US", is_active=True))
    await db_session.commit()
    other_headers = {"Authorization": f"Bearer {create_access_token(other.id, other.role)}"}

    result = await client.post(
        "/api/progress/game-session/complete",
        json={
            "session_id": payload["session_id"],
            "answers": [
                {"question_id": question["id"], "choice": question["choices"][0]}
                for question in payload["questions"]
            ],
        },
        headers=other_headers,
    )

    assert result.status_code == 404
    assert result.json()["detail"] == "Game session not found"

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    assert session.user_id == user.id
    assert session.completed is False


@pytest.mark.asyncio
async def test_valid_game_completion_creates_game_progress_once(client, test_user, db_session):
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
    assert result.status_code == 200

    rows = (
        await db_session.execute(
            select(GameProgress).where(
                GameProgress.user_id == user.id,
                GameProgress.study_plan_id == plan.id,
            )
        )
    ).scalars().all()
    assert len(rows) == 1
    assert rows[0].games_played == 1
    assert rows[0].questions_answered == 5


@pytest.mark.asyncio
async def test_game_session_public_payload_never_exposes_answers(
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

    for game_id in ("math", "words", "sequence"):
        started = await client.post(
            "/api/progress/game-session",
            json={"game_id": game_id, "language": "en", "difficulty": 1},
            headers=headers,
        )
        assert started.status_code == 200
        payload = started.json()
        assert payload["questions"]
        assert all("answer" not in question for question in payload["questions"])

        session = await db_session.get(GameSession, payload["session_id"])
        assert session is not None
        assert all("answer" in question for question in session.questions)


@pytest.mark.asyncio
async def test_interactive_game_session_public_payload_never_exposes_solution(
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

    for game_id in ("memory", "matching", "ordering"):
        started = await client.post(
            "/api/progress/game-session",
            json={"game_id": game_id, "language": "en", "difficulty": 1},
            headers=headers,
        )
        assert started.status_code == 200
        payload = started.json()
        assert payload["interaction"]
        assert "solution" not in payload["interaction"]

        session = await db_session.get(GameSession, payload["session_id"])
        assert session is not None
        stored_interaction = session.questions[0]["interaction"]
        assert "solution" in stored_interaction


@pytest.mark.asyncio
async def test_game_skill_projection_is_scoped_to_current_user(
    client, test_user, admin_user, db_session
):
    user, headers = test_user
    other_user, _ = admin_user
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

    # A malicious or stale row can reference the same plan ID with another
    # user. The game projection must never inherit that user's skill history.
    db_session.add(
        Progress(
            user_id=other_user.id,
            study_plan_id=plan.id,
            date=date.today(),
            skills={"vocabulary": 0.8, "logic": 0.7, "memory": 0.9},
        )
    )
    await db_session.commit()

    result = await _start_perfect_round(client, headers, db_session)

    assert "multi_skill" not in result["new_achievements"]

    own_progress = (
        await db_session.execute(
            select(Progress).where(
                Progress.user_id == user.id,
                Progress.study_plan_id == plan.id,
            )
        )
    ).scalars().all()
    assert own_progress
    assert set(own_progress[-1].skills) == {"math"}

@pytest.mark.asyncio
async def test_tampered_game_answer_is_rejected_without_persisting_progress(
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

    answers = [
        {"question_id": question["id"], "choice": "CLIENT_TAMPERED_CHOICE"}
        for question in payload["questions"]
    ]
    result = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=headers,
    )

    assert result.status_code == 422
    assert result.json()["detail"] == "Invalid choice for game question"

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    assert session.completed is False

    game_progress = (
        await db_session.execute(
            select(GameProgress).where(
                GameProgress.user_id == user.id,
                GameProgress.study_plan_id == plan.id,
            )
        )
    ).scalars().all()
    assert game_progress == []

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
async def test_daily_challenge_with_non_today_date_is_rejected_before_persistence(
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

    yesterday = (date.today() - timedelta(days=1)).isoformat()
    result = await client.post(
        "/api/progress/game-session/complete",
        json={
            "session_id": payload["session_id"],
            "answers": [
                {"question_id": question["id"], "choice": question["choices"][0]}
                for question in payload["questions"]
            ],
            "daily_challenge": True,
            "daily_challenge_date": yesterday,
        },
        headers=headers,
    )

    assert result.status_code == 422
    assert result.json()["detail"] == "daily_challenge_date must be today"

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    assert session.completed is False

    game_progress = (
        await db_session.execute(
            select(GameProgress).where(
                GameProgress.user_id == user.id,
                GameProgress.study_plan_id == plan.id,
            )
        )
    ).scalars().all()
    assert game_progress == []

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
@pytest.mark.parametrize(
    ("game_id", "trace_factory", "detail"),
    [
        (
            "memory",
            lambda solution: [
                {
                    "first": next(iter(solution["pairs"])),
                    "second": "client-forged-card-id",
                }
            ],
            "Unknown memory card",
        ),
        (
            "matching",
            lambda solution: [
                {
                    "left": "client-forged-left-id",
                    "right": next(iter(solution["pairs"].values())),
                }
            ],
            "Unknown matching item",
        ),
        (
            "ordering",
            lambda solution: [{"order": solution["target"] + ["client-forged-item"]}],
            "Invalid ordering interaction",
        ),
    ],
)
async def test_interactive_tampering_is_rejected_before_persistence(
    client, test_user, db_session, game_id, trace_factory, detail
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
        json={"game_id": game_id, "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    solution = session.questions[0]["interaction"]["solution"]

    result = await client.post(
        "/api/progress/game-session/complete",
        json={
            "session_id": payload["session_id"],
            "interaction_trace": trace_factory(solution),
        },
        headers=headers,
    )

    assert result.status_code == 422
    assert result.json()["detail"] == detail

    await db_session.refresh(session)
    assert session.completed is False

    game_progress = (
        await db_session.execute(
            select(GameProgress).where(
                GameProgress.user_id == user.id,
                GameProgress.study_plan_id == plan.id,
            )
        )
    ).scalars().all()
    assert game_progress == []

    progress_rows = (
        await db_session.execute(
            select(Progress).where(
                Progress.user_id == user.id,
                Progress.study_plan_id == plan.id,
            )
        )
    ).scalars().all()
    assert progress_rows == []


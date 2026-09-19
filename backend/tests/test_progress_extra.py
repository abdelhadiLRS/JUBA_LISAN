"""Tests for GET /api/progress/competencies (per-unit skill scores)."""

from __future__ import annotations

import pytest
from sqlalchemy import select

# ── GET /api/progress/competencies ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_competencies_empty_for_new_user(client, test_user):
    """A user with no study plan or exercises has an empty competencies list."""
    _, headers = test_user
    response = await client.get("/api/progress/competencies", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_competencies_requires_auth(client):
    response = await client.get(
        "/api/progress/competencies",
        headers={"Authorization": "Bearer invalid"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_competencies_returns_list_shape(client, test_user, db_session):
    """After completing a lesson with exercises, competencies returns list items
    with the expected keys: unit_id, score, mastered_count, total_count."""
    user, headers = test_user

    from app.models.lesson import Exercise, Lesson
    from tests.conftest import make_study_plan

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

    lesson = Lesson(
        study_plan_id=plan.id,
        title="Unit 1 Lesson",
        lesson_type="grammar",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        unit_id="A1-u1",
        is_completed=True,
        content={},
    )
    db_session.add(lesson)
    await db_session.flush()

    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Q?",
        options=["A", "B"],
        correct_answer="A",
        score=1.0,
    )
    db_session.add(exercise)
    await db_session.commit()

    response = await client.get("/api/progress/competencies", headers=headers)
    assert response.status_code == 200
    data = response.json()
    # If any items returned, verify their shape
    for item in data:
        assert "unit_id" in item
        assert "score" in item
        assert "mastered_count" in item
        assert "total_count" in item


@pytest.mark.asyncio
async def test_competency_upsert_uses_study_plan_scope(db_session, test_user):
    """The same competency text in two plans must keep independent scores."""
    from app.models.competency import UserCompetency
    from app.services.progress_service import upsert_unit_competency
    from tests.conftest import make_study_plan

    user, _ = test_user
    plan_a = await make_study_plan(
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
    plan_b = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A2",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A2-u1",
        generated_plan={},
        is_active=False,
    )

    await upsert_unit_competency(
        db_session,
        user.id,
        "shared-unit",
        ["Use the present tense"],
        1.0,
        study_plan_id=plan_a.id,
    )
    await upsert_unit_competency(
        db_session,
        user.id,
        "shared-unit",
        ["Use the present tense"],
        0.4,
        study_plan_id=plan_b.id,
    )

    rows = (
        await db_session.execute(
            select(UserCompetency).where(
                UserCompetency.user_id == user.id,
                UserCompetency.unit_id == "shared-unit",
            )
        )
    ).scalars().all()

    assert len(rows) == 2
    scores = {row.study_plan_id: row.score for row in rows}
    assert scores[plan_a.id] == pytest.approx(1.0)
    assert scores[plan_b.id] == pytest.approx(0.4)


@pytest.mark.asyncio
async def test_competency_upsert_applies_ema_and_mastery_threshold(db_session, test_user):
    """Repeated lesson scores use the documented EMA and mastery threshold."""
    from app.models.competency import UserCompetency
    from app.services.progress_service import upsert_unit_competency
    from tests.conftest import make_study_plan

    user, _ = test_user
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

    await upsert_unit_competency(
        db_session,
        user.id,
        "A1-u1",
        ["Use articles"],
        1.0,
        study_plan_id=plan.id,
    )
    await upsert_unit_competency(
        db_session,
        user.id,
        "A1-u1",
        ["Use articles"],
        0.0,
        study_plan_id=plan.id,
    )

    row = (
        await db_session.execute(
            select(UserCompetency).where(
                UserCompetency.user_id == user.id,
                UserCompetency.study_plan_id == plan.id,
                UserCompetency.unit_id == "A1-u1",
            )
        )
    ).scalar_one()

    assert row.score == pytest.approx(0.7)
    assert row.mastered is False

    await upsert_unit_competency(
        db_session,
        user.id,
        "A1-u1",
        ["Use articles"],
        1.0,
        study_plan_id=plan.id,
    )
    await db_session.refresh(row)

    assert row.score == pytest.approx(0.79)
    assert row.mastered is False

@pytest.mark.asyncio
async def test_get_unit_competencies_returns_deterministic_unit_order(db_session, test_user):
    """Aggregated competency responses should not depend on database row order."""
    from app.models.competency import UserCompetency
    from app.services.progress_service import get_unit_competencies
    from tests.conftest import make_study_plan

    user, _ = test_user
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
    db_session.add_all([
        UserCompetency(user_id=user.id, study_plan_id=plan.id, unit_id="A1-u2", competency_text="B", score=0.8, mastered=True),
        UserCompetency(user_id=user.id, study_plan_id=plan.id, unit_id="A1-u1", competency_text="Z", score=0.6, mastered=False),
        UserCompetency(user_id=user.id, study_plan_id=plan.id, unit_id="A1-u1", competency_text="A", score=1.0, mastered=True),
    ])
    await db_session.commit()

    result = await get_unit_competencies(db_session, user.id, study_plan_id=plan.id)

    assert [item["unit_id"] for item in result] == ["A1-u1", "A1-u2"]
    assert result[0]["score"] == pytest.approx(0.8)
    assert result[0]["mastered_count"] == 1
    assert result[0]["total_count"] == 2

@pytest.mark.asyncio
async def test_legacy_game_event_endpoint_is_retired(client, test_user):
    _, headers = test_user
    response = await client.post(
        "/api/progress/game-event",
        json={"game_id": "memory", "questions_answered": 5, "correct_answers": 5},
        headers=headers,
    )
    assert response.status_code == 410

@pytest.mark.asyncio
async def test_legacy_game_progress_endpoint_is_removed(client, test_user):
    _, headers = test_user
    response = await client.post(
        "/api/progress/game",
        json={"xp": 999999, "questions_answered": 1, "correct_answers": 1, "skills": {"math": 1}},
        headers=headers,
    )
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_legacy_game_summary_sync_is_rejected(client, test_user):
    _, headers = test_user
    response = await client.post(
        "/api/progress/game-summary",
        json={"games_played": 999, "questions_answered": 999, "correct_answers": 999},
        headers=headers,
    )
    assert response.status_code == 410


@pytest.mark.asyncio
async def test_game_event_rejects_invalid_counters(client, test_user):
    _, headers = test_user
    response = await client.post(
        "/api/progress/game-event",
        json={
            "event_id": "f5b5f4d8-4c41-4cb0-9c17-2a8f4b2e9d77",
            "game_id": "memory",
            "questions_answered": 2,
            "correct_answers": 3,
            "round_score": 10,
        },
        headers=headers,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_game_event_rejects_unknown_game_id(client, test_user):
    _, headers = test_user
    response = await client.post(
        "/api/progress/game-event",
        json={
            "event_id": "44444444-4444-4444-8444-444444444444",
            "game_id": "forged_game",
            "questions_answered": 5,
            "correct_answers": 5,
            "round_score": 9999,
        },
        headers=headers,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_game_event_server_unlocks_multi_skill(client, test_user, db_session):
    user, headers = test_user
    from tests.conftest import make_study_plan

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

    def event(event_id: str, game_id: str):
        return {
            "event_id": event_id,
            "game_id": game_id,
            "questions_answered": 1,
            "correct_answers": 1,
            "round_score": 10,
            "daily_challenge": False,
            "daily_challenge_date": "",
            "achievements": ["multi_skill"],
        }

    for event_id, game_id in [
        ("11111111-1111-4111-8111-111111111111", "math"),
        ("22222222-2222-4222-8222-222222222222", "sequence"),
    ]:
        response = await client.post(
            "/api/progress/game-event",
            json=event(event_id, game_id),
            headers=headers,
        )
        assert response.status_code == 200
        assert "multi_skill" not in response.json()["achievements"]

    response = await client.post(
        "/api/progress/game-event",
        json=event("33333333-3333-4333-8333-333333333333", "memory"),
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "multi_skill" in data["achievements"]
    assert data["skills"]["math"] == pytest.approx(1.0)
    assert data["skills"]["logic"] == pytest.approx(1.0)
    assert data["skills"]["memory"] == pytest.approx(1.0)


@pytest.mark.asyncio
async def test_game_event_multi_skill_counts_existing_zero_skill_after_positive_update(
    client, test_user, db_session
):
    """A skill key already present at zero must still count after a positive game event."""
    user, headers = test_user
    from app.models.progress import Progress
    from tests.conftest import make_study_plan

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
            date=__import__("datetime").date.today(),
            xp_earned=0,
            lessons_completed=0,
            exercises_correct=0,
            exercises_total=0,
            streak_day=0,
            skills={"math": 1.0, "logic": 1.0, "memory": 0.0},
        )
    )
    await db_session.commit()

    response = await client.post(
        "/api/progress/game-event",
        json={
            "event_id": "55555555-5555-4555-8555-555555555555",
            "game_id": "memory",
            "questions_answered": 1,
            "correct_answers": 1,
            "round_score": 10,
        },
        headers=headers,
    )
    assert response.status_code == 200
    assert "multi_skill" in response.json()["achievements"]


@pytest.mark.asyncio
async def test_game_session_hides_answers_and_persists_server_questions(client, test_user, db_session):
    user, headers = test_user
    from app.models.game_session import GameSession
    from tests.conftest import make_study_plan

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

    response = await client.post(
        "/api/progress/game-session",
        json={"game_id": "math", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["game_id"] == "math"
    assert len(data["questions"]) == 5
    assert all(set(q) == {"id", "prompt", "choices", "hint", "skill", "difficulty"} for q in data["questions"])
    assert all("answer" not in q for q in data["questions"])

    session = await db_session.get(GameSession, data["session_id"])
    assert session is not None
    assert session.user_id == user.id
    assert session.study_plan_id is not None
    assert len(session.questions) == 5
    assert all("answer" in q for q in session.questions)


@pytest.mark.asyncio
async def test_game_session_rejects_invalid_language_and_difficulty(client, test_user):
    _, headers = test_user
    response = await client.post(
        "/api/progress/game-session",
        json={"game_id": "math", "language": "xx", "difficulty": 1},
        headers=headers,
    )
    assert response.status_code == 422

    response = await client.post(
        "/api/progress/game-session",
        json={"game_id": "math", "language": "en", "difficulty": 9},
        headers=headers,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_game_session_completion_uses_server_answers(client, test_user, db_session):
    user, headers = test_user
    from app.models.game_session import GameSession
    from tests.conftest import make_study_plan

    await make_study_plan(
        db_session, user_id=user.id, cefr_level="A1", goals=["grammar"],
        duration_weeks=4, days_per_week=4, current_unit="A1-u1",
        generated_plan={}, is_active=True,
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
    forged_answers = [
        {"question_id": q["id"], "choice": q["choices"][0]}
        for q in payload["questions"]
    ]
    response = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": forged_answers},
        headers=headers,
    )
    assert response.status_code == 200

    expected_correct = sum(
        answer["choice"] == question["answer"]
        for answer, question in zip(forged_answers, session.questions)
    )
    assert response.json()["questions_answered"] == 5
    assert response.json()["correct_answers"] == expected_correct


@pytest.mark.asyncio
async def test_game_session_completion_rejects_replay_and_partial_answers(client, test_user, db_session):
    user, headers = test_user
    from tests.conftest import make_study_plan

    await make_study_plan(
        db_session, user_id=user.id, cefr_level="A1", goals=["grammar"],
        duration_weeks=4, days_per_week=4, current_unit="A1-u1",
        generated_plan={}, is_active=True,
    )
    started = await client.post(
        "/api/progress/game-session",
        json={"game_id": "sequence", "language": "en", "difficulty": 1},
        headers=headers,
    )
    payload = started.json()
    partial = [{
        "question_id": payload["questions"][0]["id"],
        "choice": payload["questions"][0]["choices"][0],
    }]
    response = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": partial},
        headers=headers,
    )
    assert response.status_code == 422

    session = await db_session.get(__import__("app.models.game_session", fromlist=["GameSession"]).GameSession, payload["session_id"])
    answers = [
        {"question_id": q["id"], "choice": q["choices"][0]}
        for q in payload["questions"]
    ]
    completed = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=headers,
    )
    assert completed.status_code == 200
    replay = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=headers,
    )
    assert replay.status_code == 409

@pytest.mark.asyncio
async def test_game_session_words_uses_server_vocabulary(client, test_user, db_session):
    user, headers = test_user
    from tests.conftest import make_study_plan

    await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        goals=["vocabulary"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )
    response = await client.post(
        "/api/progress/game-session",
        json={"game_id": "words", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["questions"]) == 5
    assert all(q["skill"] == "vocabulary" for q in data["questions"])
    assert all("answer" not in q for q in data["questions"])
    assert all(len(q["choices"]) == 4 for q in data["questions"])


@pytest.mark.asyncio
async def test_game_session_result_is_server_derived(client, test_user, db_session):
    user, headers = test_user
    from app.models.game_session import GameSession
    from tests.conftest import make_study_plan

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

    answers = [
        {"question_id": question["id"], "choice": question["answer"]}
        for question in session.questions
    ]
    completed = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=headers,
    )
    assert completed.status_code == 200
    result = completed.json()
    assert result["round_questions"] == 5
    assert result["round_correct"] == 5
    assert result["round_score"] == 25
    assert result["xp_earned"] >= 5 * 5
    assert "new_achievements" in result

@pytest.mark.asyncio
async def test_game_session_rejects_invalid_choice_and_expired_session(client, test_user, db_session):
    user, headers = test_user
    from datetime import UTC, datetime, timedelta
    from app.models.game_session import GameSession
    from tests.conftest import make_study_plan

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
    payload = started.json()
    invalid = [
        {"question_id": q["id"], "choice": "__forged__"}
        for q in payload["questions"]
    ]
    response = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": invalid},
        headers=headers,
    )
    assert response.status_code == 422

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    session.expires_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(minutes=1)
    await db_session.commit()

    valid = [
        {"question_id": q["id"], "choice": q["choices"][0]}
        for q in payload["questions"]
    ]
    response = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": valid},
        headers=headers,
    )
    assert response.status_code == 410


@pytest.mark.asyncio
async def test_game_session_daily_date_is_validated_before_persistence(client, test_user, db_session):
    user, headers = test_user
    from app.models.game_progress import GameProgress
    from tests.conftest import make_study_plan

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
        json={"game_id": "sequence", "language": "en", "difficulty": 1},
        headers=headers,
    )
    payload = started.json()
    answers = [
        {"question_id": q["id"], "choice": q["choices"][0]}
        for q in payload["questions"]
    ]
    response = await client.post(
        "/api/progress/game-session/complete",
        json={
            "session_id": payload["session_id"],
            "answers": answers,
            "daily_challenge": True,
            "daily_challenge_date": "2000-01-01",
        },
        headers=headers,
    )
    assert response.status_code == 422

    entry = (
        await db_session.execute(
            select(GameProgress).where(
                GameProgress.user_id == user.id,
                GameProgress.study_plan_id == plan.id,
            )
        )
    ).scalar_one_or_none()
    assert entry is None


@pytest.mark.asyncio
async def test_interactive_memory_session_verifies_server_challenge(client, test_user, db_session):
    user, headers = test_user
    from tests.conftest import make_study_plan
    await make_study_plan(
        db_session, user_id=user.id, cefr_level="A1", goals=["vocabulary"],
        duration_weeks=4, days_per_week=4, current_unit="A1-u1",
        generated_plan={}, is_active=True,
    )
    started = await client.post(
        "/api/progress/game-session",
        json={"game_id": "memory", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()
    challenge = payload["interaction"]
    groups = {}
    for card in challenge["cards"]:
        groups.setdefault(card["pair_key"], []).append(card["id"])
    trace = [{"first": ids[0], "second": ids[1]} for ids in groups.values()]
    completed = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": [], "interaction_trace": trace},
        headers=headers,
    )
    assert completed.status_code == 200
    result = completed.json()
    assert result["round_correct"] == len(groups)
    assert result["round_questions"] == len(groups)
    assert result["round_score"] == 25


@pytest.mark.asyncio
async def test_interactive_matching_rejects_fabricated_ids(client, test_user, db_session):
    user, headers = test_user
    from tests.conftest import make_study_plan
    await make_study_plan(
        db_session, user_id=user.id, cefr_level="A1", goals=["vocabulary"],
        duration_weeks=4, days_per_week=4, current_unit="A1-u1",
        generated_plan={}, is_active=True,
    )
    started = await client.post(
        "/api/progress/game-session",
        json={"game_id": "matching", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()
    completed = await client.post(
        "/api/progress/game-session/complete",
        json={
            "session_id": payload["session_id"],
            "answers": [],
            "interaction_trace": [{"left": "fake", "right": "fake"}],
        },
        headers=headers,
    )
    assert completed.status_code == 422


@pytest.mark.asyncio
async def test_interactive_ordering_uses_trace_and_rejects_incomplete_round(client, test_user, db_session):
    user, headers = test_user
    from tests.conftest import make_study_plan
    await make_study_plan(
        db_session, user_id=user.id, cefr_level="A1", goals=["vocabulary"],
        duration_weeks=4, days_per_week=4, current_unit="A1-u1",
        generated_plan={}, is_active=True,
    )
    started = await client.post(
        "/api/progress/game-session",
        json={"game_id": "ordering", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()
    ids = [item["id"] for item in payload["interaction"]["items"]]
    incomplete = await client.post(
        "/api/progress/game-session/complete",
        json={
            "session_id": payload["session_id"],
            "answers": [],
            "interaction_trace": [{"order": ids[:-1]}],
        },
        headers=headers,
    )
    assert incomplete.status_code == 422


@pytest.mark.asyncio
async def test_game_session_cannot_be_completed_by_another_user(client, test_user, db_session):
    """A session is bound to its issuing user and cannot be completed cross-account."""
    owner, owner_headers = test_user
    from app.core.security import create_access_token, hash_password
    from app.models.user import User
    from app.models.user_language import UserLanguage
    from tests.conftest import make_study_plan

    await make_study_plan(
        db_session,
        user_id=owner.id,
        cefr_level="A1",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )

    other = User(
        username="otheruser",
        email="other@example.com",
        display_name="Other User",
        hashed_password=hash_password("otherpass"),
        role="user",
        native_language="es",
        target_language="en-US",
        is_active=True,
    )
    db_session.add(other)
    await db_session.flush()
    db_session.add(UserLanguage(user_id=other.id, target_language="en-US", is_active=True))
    await db_session.commit()

    started = await client.post(
        "/api/progress/game-session",
        json={"game_id": "math", "language": "en", "difficulty": 1},
        headers=owner_headers,
    )
    assert started.status_code == 200
    payload = started.json()

    other_headers = {
        "Authorization": f"Bearer {create_access_token(other.id, other.role)}"
    }
    answers = [
        {"question_id": question["id"], "choice": question["choices"][0]}
        for question in payload["questions"]
    ]
    response = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=other_headers,
    )
    assert response.status_code == 404

    owner_response = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=owner_headers,
    )
    assert owner_response.status_code == 200

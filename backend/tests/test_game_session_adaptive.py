"""Focused tests for server-driven adaptive game rounds."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_generic_game_session_reveals_one_question_and_adapts(client, test_user, db_session):
    user, headers = test_user
    from app.models.game_session import GameSession
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

    started = await client.post(
        "/api/progress/game-session",
        json={"game_id": "quick_choice", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()
    assert len(payload["questions"]) == 1
    public_question = payload["questions"][0]
    assert "answer" not in public_question

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    first = session.questions[0]

    response = await client.post(
        "/api/progress/game-session/next",
        json={
            "session_id": payload["session_id"],
            "question_id": public_question["id"],
            "choice": first["answer"],
        },
        headers=headers,
    )
    assert response.status_code == 200
    result = response.json()
    assert result["correct"] is True
    assert result["finished"] is False
    assert result["question"]["difficulty"] == 2
    assert result["adaptive_mode"] == "challenge"

    await db_session.refresh(session)
    assert len(session.questions) == 2
    assert session.questions[0]["_answered"] is True
    assert session.questions[0]["_attempts"][0]["correct"] is True
    assert session.questions[1]["_served"] is True
    assert session.questions[1]["_answered"] is False


@pytest.mark.asyncio
async def test_wrong_fifth_answer_closes_round_for_completion(client, test_user, db_session):
    user, headers = test_user
    from app.models.game_session import GameSession
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

    started = await client.post(
        "/api/progress/game-session",
        json={"game_id": "quick_choice", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()
    answers = []

    for index in range(5):
        session = await db_session.get(GameSession, payload["session_id"])
        assert session is not None
        current = next(item for item in session.questions if not item.get("_answered"))
        choice = (
            current["answer"]
            if index < 4
            else next(option for option in current["choices"] if option != current["answer"])
        )
        answers.append({"question_id": current["id"], "choice": choice})

        response = await client.post(
            "/api/progress/game-session/next",
            json={
                "session_id": payload["session_id"],
                "question_id": current["id"],
                "choice": choice,
            },
            headers=headers,
        )
        assert response.status_code == 200
        result = response.json()
        assert result["answered"] == index + 1

        if index < 4:
            assert result["finished"] is False
            assert result["question"] is not None
        else:
            assert result["correct"] is False
            assert result["finished"] is True
            assert result["question"] is None

    completed = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=headers,
    )
    assert completed.status_code == 200
    result = completed.json()
    assert result["round_questions"] == 5
    assert result["round_correct"] == 4

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    assert session.completed is True

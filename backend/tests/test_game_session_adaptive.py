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
async def test_wrong_answer_reissues_same_logical_item_for_targeted_review(
    client, test_user, db_session
):
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
        json={"game_id": "quick_choice", "language": "en", "difficulty": 2},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()
    public_question = payload["questions"][0]

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    original = session.questions[0]
    wrong_choice = next(option for option in original["choices"] if option != original["answer"])

    response = await client.post(
        "/api/progress/game-session/next",
        json={
            "session_id": payload["session_id"],
            "question_id": public_question["id"],
            "choice": wrong_choice,
        },
        headers=headers,
    )
    assert response.status_code == 200
    result = response.json()
    assert result["correct"] is False
    assert result["finished"] is False
    assert result["adaptive_mode"] == "review"
    assert result["question"]["id"] == public_question["id"]
    assert result["question"]["skill"] == original["skill"]
    assert result["question"]["difficulty"] <= original["difficulty"]

    await db_session.refresh(session)
    current = session.questions[0]
    assert len(session.questions) == 1
    assert current["_answered"] is False
    assert current["_attempts"][0]["choice"] == wrong_choice
    assert current["_attempts"][0]["correct"] is False


@pytest.mark.asyncio
async def test_fifth_logical_item_requires_retry_before_round_finishes(
    client, test_user, db_session
):
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

    # Resolve four logical questions normally. Each correct answer issues
    # exactly one new server-owned question.
    for _ in range(4):
        session = await db_session.get(GameSession, payload["session_id"])
        assert session is not None
        current = next(item for item in session.questions if not item.get("_answered"))
        choice = current["answer"]
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
        assert result["finished"] is False
        assert result["question"] is not None

    # The fifth logical item is deliberately missed. It remains unresolved and
    # is replaced by a targeted retry under the same logical question ID.
    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    retry = next(item for item in session.questions if not item.get("_answered"))
    wrong_choice = next(option for option in retry["choices"] if option != retry["answer"])
    retry_id = retry["id"]

    response = await client.post(
        "/api/progress/game-session/next",
        json={
            "session_id": payload["session_id"],
            "question_id": retry_id,
            "choice": wrong_choice,
        },
        headers=headers,
    )
    assert response.status_code == 200
    result = response.json()
    assert result["correct"] is False
    assert result["finished"] is False
    assert result["answered"] == 4
    assert result["question"]["id"] == retry_id
    assert result["adaptive_mode"] == "review"

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    retry = next(item for item in session.questions if not item.get("_answered"))
    assert retry["id"] == retry_id
    assert len(retry["_attempts"]) >= 1
    assert retry["_attempts"][-1]["correct"] is False

    # Resolve the retry. The same logical ID is answered again, so completion
    # receives one answer per logical question rather than one answer per attempt.
    response = await client.post(
        "/api/progress/game-session/next",
        json={
            "session_id": payload["session_id"],
            "question_id": retry_id,
            "choice": retry["answer"],
        },
        headers=headers,
    )
    assert response.status_code == 200
    result = response.json()
    assert result["correct"] is True
    assert result["finished"] is True
    assert result["question"] is None
    assert result["answered"] == 5

    answers.append({"question_id": retry_id, "choice": retry["answer"]})

    completed = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=headers,
    )
    assert completed.status_code == 200
    result = completed.json()
    assert result["round_questions"] == 5
    assert result["round_correct"] == 5

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    assert session.completed is True

@pytest.mark.asyncio
async def test_answering_an_already_resolved_question_is_idempotency_safe(
    client, test_user, db_session
):
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
    question = payload["questions"][0]

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    answer = session.questions[0]["answer"]
    request_body = {
        "session_id": payload["session_id"],
        "question_id": question["id"],
        "choice": answer,
    }

    first = await client.post(
        "/api/progress/game-session/next",
        json=request_body,
        headers=headers,
    )
    assert first.status_code == 200
    assert first.json()["correct"] is True

    duplicate = await client.post(
        "/api/progress/game-session/next",
        json=request_body,
        headers=headers,
    )
    assert duplicate.status_code == 409
    assert duplicate.json()["detail"] == "Question already answered"

    await db_session.refresh(session)
    assert len(session.questions[0]["_attempts"]) == 1

def test_speaking_open_response_hides_authoritative_answer():
    from app.routers.progress import _apply_skill_review_variant

    question = {
        "skill": "speaking",
        "answer": "I am going to the market today.",
        "word": "market",
        "prompt": "Which sentence best uses 'market'?",
        "language": "en",
        "target_language": "en-GB",
        "cefr_level": "A1",
        "topic": "shopping",
    }

    replay = _apply_skill_review_variant(question, 2)

    assert replay["mechanic_variant"] == "open_response"
    assert replay["input_mode"] == "text"
    assert replay["choices"] == []
    assert question["answer"] not in replay["prompt"]
    assert replay["hint"] == "Use a complete natural sentence."



@pytest.mark.asyncio
async def test_review_mix_uses_due_pool_and_retries_same_review_identity(
    client, test_user, db_session
):
    user, headers = test_user
    from datetime import UTC, datetime, timedelta

    from app.models.game_progress_event import GameProgressEvent
    from app.models.game_session import GameSession
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        goals=["vocabulary", "grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )

    source = await client.post(
        "/api/progress/game-session",
        json={"game_id": "quick_choice", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert source.status_code == 200
    source_session = await db_session.get(GameSession, source.json()["session_id"])
    assert source_session is not None
    source_question = dict(source_session.questions[0])
    review_key = "|".join(
        str(source_question.get(key, "")).strip().casefold()
        for key in ("skill", "topic", "prompt", "answer")
    )

    now = datetime.now(UTC).replace(tzinfo=None)
    db_session.add(
        GameProgressEvent(
            event_id="review-mix-test-event",
            user_id=user.id,
            study_plan_id=plan.id,
            game_id="quick_choice",
            questions_answered=1,
            correct_answers=0,
            round_score=0,
            mistakes=[
                {
                    "review_key": review_key,
                    "question": source_question,
                    "resolved": False,
                    "review_count": 0,
                    "review_streak": 0,
                    "next_review_at": (now - timedelta(minutes=1)).isoformat(),
                }
            ],
            xp_earned=0,
        )
    )
    await db_session.commit()

    started = await client.post(
        "/api/progress/game-session",
        json={"game_id": "review_mix", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200
    payload = started.json()
    assert len(payload["questions"]) == 1
    public_question = payload["questions"][0]

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    first = next(item for item in session.questions if item["id"] == public_question["id"])
    assert first["review_identity"] == review_key
    assert first["review"] is True
    assert first["source_game_id"] == "quick_choice"

    wrong = next(option for option in first["choices"] if option != first["answer"])
    response = await client.post(
        "/api/progress/game-session/next",
        json={
            "session_id": payload["session_id"],
            "question_id": public_question["id"],
            "choice": wrong,
        },
        headers=headers,
    )
    assert response.status_code == 200
    result = response.json()
    assert result["correct"] is False
    assert result["finished"] is False
    assert result["question"]["id"] == public_question["id"]
    assert result["adaptive_mode"] == "review"

    await db_session.refresh(session)
    retry = next(item for item in session.questions if item["id"] == public_question["id"])
    assert retry["review_identity"] == review_key
    assert retry["_answered"] is False
    assert retry["_attempts"][-1]["correct"] is False
    assert len(session.questions) == 5

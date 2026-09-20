import pytest


@pytest.mark.asyncio
async def test_interactive_game_difficulty_scales_challenge_size(
    client, test_user, db_session
):
    from tests.conftest import make_study_plan

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

    expected_sizes = {1: 3, 2: 4, 3: 5}
    for game_id in ("memory", "matching", "ordering"):
        for difficulty, expected_size in expected_sizes.items():
            response = await client.post(
                "/api/progress/game-session",
                json={"game_id": game_id, "language": "en", "difficulty": difficulty},
                headers=headers,
            )
            assert response.status_code == 200
            payload = response.json()
            interaction = payload["interaction"]

            assert "solution" not in interaction
            if game_id == "memory":
                assert len(interaction["cards"]) == expected_size * 2
            elif game_id == "matching":
                assert len(interaction["left"]) == expected_size
                assert len(interaction["right"]) == expected_size
            else:
                assert len(interaction["items"]) == expected_size

            assert all("answer" not in question for question in payload["questions"])


@pytest.mark.asyncio
async def test_interactive_game_session_keeps_solution_server_side(
    client, test_user, db_session
):
    from app.models.game_session import GameSession
    from tests.conftest import make_study_plan

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

    response = await client.post(
        "/api/progress/game-session",
        json={"game_id": "ordering", "language": "en", "difficulty": 2},
        headers=headers,
    )
    assert response.status_code == 200
    payload = response.json()

    public_items = payload["interaction"]["items"]
    assert "solution" not in payload["interaction"]
    assert all(set(item) == {"id", "label"} for item in public_items)

    session = await db_session.get(GameSession, payload["session_id"])
    assert session is not None
    stored_interaction = session.questions[0]["interaction"]
    assert stored_interaction["solution"]["target"]
    assert stored_interaction["solution"]["target"] != []


@pytest.mark.asyncio
async def test_completed_interactive_session_cannot_be_replayed(
    client, test_user, db_session
):
    from tests.conftest import make_study_plan

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

    cards_by_pair = {}
    for card in payload["interaction"]["cards"]:
        cards_by_pair.setdefault(card["pair_key"], []).append(card["id"])
    trace = [
        {"first": ids[0], "second": ids[1]}
        for ids in cards_by_pair.values()
    ]

    first = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "interaction_trace": trace},
        headers=headers,
    )
    assert first.status_code == 200
    assert first.json()["round_correct"] == first.json()["round_questions"]

    replay = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "interaction_trace": trace},
        headers=headers,
    )
    assert replay.status_code == 409
    assert replay.json()["detail"] == "Game session already completed"

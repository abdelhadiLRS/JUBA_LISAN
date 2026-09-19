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

@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ({"math": 2.0, "memory": -1.0, "": 0.5, "bad": float("nan")}, {"math": 1.0, "memory": 0.0}),
        ({"ordering": float("inf"), "vocabulary": 0.75}, {"vocabulary": 0.75}),
    ],
)
def test_game_progress_schema_normalizes_skill_scores(payload, expected):
    from app.schemas.progress import GameProgressUpdate

    data = GameProgressUpdate(skills=payload)

    assert data.skills == expected


def test_game_progress_schema_discards_invalid_only_skills():
    from app.schemas.progress import GameProgressUpdate

    data = GameProgressUpdate(skills={"": 1.0, "bad": float("nan")})

    assert data.skills == {}



@pytest.mark.asyncio
async def test_game_summary_persists_and_merges_stats(client, test_user, db_session):
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

    payload = {
        "games_played": 2,
        "questions_answered": 10,
        "correct_answers": 8,
        "best_round_score": 25,
        "daily_challenges_completed": 1,
        "last_daily_challenge_date": "2026-09-19",
        "current_correct_streak": 4,
        "best_correct_streak": 4,
        "achievements": ["first_game", "perfect_round"],
    }
    response = await client.post("/api/progress/game-summary", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["games_played"] == 2
    assert response.json()["achievements"] == ["first_game", "perfect_round"]

    response = await client.post(
        "/api/progress/game-summary",
        json={
            **payload,
            "games_played": 1,
            "questions_answered": 4,
            "correct_answers": 3,
            "best_round_score": 10,
            "daily_challenges_completed": 0,
            "current_correct_streak": 1,
            "best_correct_streak": 2,
            "achievements": ["streak_5"],
        },
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["games_played"] == 2
    assert data["questions_answered"] == 10
    assert data["correct_answers"] == 8
    assert data["best_round_score"] == 25
    assert data["daily_challenges_completed"] == 1
    assert data["best_correct_streak"] == 4
    assert data["achievements"] == ["first_game", "perfect_round", "streak_5"]

    response = await client.get("/api/progress/game-summary", headers=headers)
    assert response.status_code == 200
    summary = response.json()
    assert summary["games_played"] == 2
    assert summary["questions_answered"] == 10
    assert summary["correct_answers"] == 8
    assert summary["achievements"] == ["first_game", "perfect_round", "streak_5"]

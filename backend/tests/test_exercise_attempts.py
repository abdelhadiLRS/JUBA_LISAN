from __future__ import annotations

import pytest
from sqlalchemy import select

from app.models.exercise_attempt import ExerciseAttempt
from app.models.lesson import Exercise


async def _lesson_with_variants(db_session, user_id):
    from tests.test_lessons_router import _create_lesson_with_plan

    lesson = await _create_lesson_with_plan(
        db_session,
        user_id,
        content={
            "exercises": [
                {
                    "content_id": "content-1",
                    "variant": "multiple_choice",
                    "accepted_answers": ["B"],
                },
                {
                    "content_id": "content-1",
                    "variant": "fill_blank",
                    "accepted_answers": ["B"],
                },
            ]
        },
    )
    first = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Choose B",
        options=["A", "B"],
        correct_answer="B",
    )
    second = Exercise(
        lesson_id=lesson.id,
        exercise_type="fill_blank",
        question="___",
        options=None,
        correct_answer="B",
    )
    db_session.add_all([first, second])
    await db_session.commit()
    await db_session.refresh(first)
    await db_session.refresh(second)
    return lesson, first, second


@pytest.mark.asyncio
async def test_answer_persists_attempt(client, test_user, db_session):
    user, headers = test_user
    _, exercise, _ = await _lesson_with_variants(db_session, user.id)

    response = await client.post(
        f"/api/lessons/exercises/{exercise.id}/answer",
        headers=headers,
        json={"answer": "A"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["attempt_id"] is not None
    assert data["attempt_number"] == 1
    assert data["content_id"] == "content-1"
    assert data["variant"] == "multiple_choice"

    attempts = (
        await db_session.execute(
            select(ExerciseAttempt).where(
                ExerciseAttempt.user_id == user.id,
                ExerciseAttempt.exercise_id == exercise.id,
            )
        )
    ).scalars().all()
    assert len(attempts) == 1
    assert attempts[0].score == 0


@pytest.mark.asyncio
async def test_failed_attempt_returns_easier_variant(client, test_user, db_session):
    user, headers = test_user
    lesson, _exercise, _easier = await _lesson_with_variants(db_session, user.id)
    from app.models.lesson import Exercise
    exercise = (await db_session.execute(
        select(Exercise).where(
            Exercise.lesson_id == lesson.id,
            Exercise.exercise_type == "fill_blank",
        )
    )).scalar_one()
    easier = (await db_session.execute(
        select(Exercise).where(
            Exercise.lesson_id == lesson.id,
            Exercise.exercise_type == "multiple_choice",
        )
    )).scalar_one()

    answer = await client.post(
        f"/api/lessons/exercises/{exercise.id}/answer",
        headers=headers,
        json={"answer": "A"},
    )
    assert answer.status_code == 200

    retry = await client.post(
        f"/api/lessons/exercises/{exercise.id}/retry",
        headers=headers,
    )

    assert retry.status_code == 200
    data = retry.json()
    assert data["id"] == easier.id
    assert data["content_id"] == "content-1"
    assert data["variant"] == "multiple_choice"
    assert data["answered_at"] is None


@pytest.mark.asyncio
async def test_retry_requires_failed_attempt(client, test_user, db_session):
    user, headers = test_user
    _, exercise, _ = await _lesson_with_variants(db_session, user.id)

    response = await client.post(
        f"/api/lessons/exercises/{exercise.id}/retry",
        headers=headers,
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_attempt_history_is_user_scoped(client, test_user, db_session):
    user, headers = test_user
    _, exercise, _ = await _lesson_with_variants(db_session, user.id)

    answer = await client.post(
        f"/api/lessons/exercises/{exercise.id}/answer",
        headers=headers,
        json={"answer": "A"},
    )
    assert answer.status_code == 200

    history = await client.get(
        f"/api/lessons/exercises/{exercise.id}/attempts",
        headers=headers,
    )
    assert history.status_code == 200
    data = history.json()
    assert len(data) == 1
    assert data[0]["attempt_number"] == 1
    assert data[0]["content_id"] == "content-1"


@pytest.mark.asyncio
async def test_lesson_attempt_summary_is_user_scoped(client, test_user, db_session):
    user, headers = test_user
    lesson, exercise, easier = await _lesson_with_variants(db_session, user.id)

    first = await client.post(
        f"/api/lessons/exercises/{exercise.id}/answer",
        headers=headers,
        json={"answer": "A"},
    )
    assert first.status_code == 200

    retry = await client.post(
        f"/api/lessons/exercises/{exercise.id}/retry",
        headers=headers,
    )
    assert retry.status_code == 200

    second = await client.post(
        f"/api/lessons/exercises/{easier.id}/answer",
        headers=headers,
        json={"answer": "B"},
    )
    assert second.status_code == 200

    summary = await client.get(
        f"/api/lessons/{lesson.id}/attempt-summary",
        headers=headers,
    )
    assert summary.status_code == 200
    data = summary.json()
    by_exercise = {item["exercise_id"]: item for item in data}
    assert by_exercise[exercise.id]["attempts"] == 1
    assert by_exercise[exercise.id]["best_score"] == 0
    assert by_exercise[easier.id]["attempts"] == 1
    assert by_exercise[easier.id]["best_score"] == 1
    assert by_exercise[easier.id]["latest_variant"] == "multiple_choice"


@pytest.mark.asyncio
async def test_retry_is_rejected_after_lesson_completion(client, test_user, db_session):
    user, headers = test_user
    lesson, exercise, _ = await _lesson_with_variants(db_session, user.id)

    answer = await client.post(
        f"/api/lessons/exercises/{exercise.id}/answer",
        headers=headers,
        json={"answer": "A"},
    )
    assert answer.status_code == 200

    lesson.is_completed = True
    await db_session.commit()

    retry = await client.post(
        f"/api/lessons/exercises/{exercise.id}/retry",
        headers=headers,
    )

    assert retry.status_code == 409


@pytest.mark.asyncio
async def test_lesson_attempt_summary_tracks_best_and_latest_attempts(client, test_user, db_session):
    user, headers = test_user
    lesson, exercise, _ = await _lesson_with_variants(db_session, user.id)

    first = await client.post(
        f"/api/lessons/exercises/{exercise.id}/answer",
        headers=headers,
        json={"answer": "A"},
    )
    assert first.status_code == 200

    second = await client.post(
        f"/api/lessons/exercises/{exercise.id}/answer",
        headers=headers,
        json={"answer": "B"},
    )
    assert second.status_code == 200

    summary = await client.get(
        f"/api/lessons/{lesson.id}/attempt-summary",
        headers=headers,
    )
    assert summary.status_code == 200
    item = next(row for row in summary.json() if row["exercise_id"] == exercise.id)
    assert item["attempts"] == 2
    assert item["best_score"] == 1
    assert item["latest_score"] == 1
    assert item["latest_variant"] == "multiple_choice"

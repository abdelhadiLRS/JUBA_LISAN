"""One scored first attempt per user and reading/listening exercise.

Covers the partial unique index (model metadata and migration 0071 share it),
read-only replays, and concurrent first submissions through the real ASGI
routes on a file-backed SQLite database.
"""
import asyncio

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.models.listening import ListeningAttempt, ListeningExercise
from app.models.progress import Progress
from app.models.reading import ReadingAttempt, ReadingExercise
from tests.test_operational_integration import operational  # noqa: F401  (fixture)

QUESTIONS = [
    {"index": i, "question": f"Q{i}?", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct": "B"}
    for i in range(5)
]
ALL_CORRECT = {str(i): "B" for i in range(5)}


async def _reading_exercise(ctx) -> int:
    async with ctx.sessions() as db:
        exercise = ReadingExercise(level="A1", target_language="en-US", exercise_type="notice",
                                   topic="Shop sign", text="Open from 9 to 5.", questions=QUESTIONS)
        db.add(exercise)
        await db.commit()
        return exercise.id


async def _listening_exercise(ctx) -> int:
    async with ctx.sessions() as db:
        exercise = ListeningExercise(level="A1", target_language="en-US", exercise_type="monologue",
                                     topic="Greetings", text="Hello and welcome.", audio_path="/tmp/x.mp3",
                                     questions=QUESTIONS)
        db.add(exercise)
        await db.commit()
        return exercise.id


async def _xp(ctx) -> int:
    """Learning XP only; goal rewards (daily target 50) are excluded."""
    async with ctx.sessions() as db:
        total = await db.scalar(
            select(func.coalesce(func.sum(Progress.xp_earned - Progress.reward_xp), 0)).where(Progress.user_id == ctx.user_id)
        )
        return int(total)


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["reading", "listening"])
async def test_concurrent_first_attempts_persist_once_and_award_xp_once(operational, kind):  # noqa: F811
    ctx = operational
    exercise_id = await (_reading_exercise(ctx) if kind == "reading" else _listening_exercise(ctx))
    body = {"exercise_id": exercise_id, "answers": ALL_CORRECT}
    responses = await asyncio.gather(
        ctx.client.post(f"/api/{kind}/attempt", headers=ctx.headers, json=body),
        ctx.client.post(f"/api/{kind}/attempt", headers=ctx.headers, json=body),
    )
    assert sorted(r.status_code for r in responses) == [200, 409], [r.text for r in responses]
    attempt_model, exercise_model, counter = (
        (ReadingAttempt, ReadingExercise, "view_count") if kind == "reading" else (ListeningAttempt, ListeningExercise, "play_count")
    )
    async with ctx.sessions() as db:
        assert await db.scalar(select(func.count(attempt_model.id))) == 1
        assert getattr(await db.get(exercise_model, exercise_id), counter) == 1
    assert await _xp(ctx) == 50


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["reading", "listening"])
async def test_replay_is_read_only(operational, kind):  # noqa: F811
    ctx = operational
    exercise_id = await (_reading_exercise(ctx) if kind == "reading" else _listening_exercise(ctx))
    first = await ctx.client.post(f"/api/{kind}/attempt", headers=ctx.headers,
                                  json={"exercise_id": exercise_id, "answers": ALL_CORRECT})
    assert first.status_code == 200 and first.json()["xp_earned"] == 50
    for _ in range(3):
        replay = await ctx.client.post(f"/api/{kind}/attempt", headers=ctx.headers,
                                       json={"exercise_id": exercise_id, "answers": ALL_CORRECT, "replay": True})
        assert replay.status_code == 200
        assert replay.json()["xp_earned"] == 0 and replay.json()["score"] == 5
    attempt_model, exercise_model, counter = (
        (ReadingAttempt, ReadingExercise, "view_count") if kind == "reading" else (ListeningAttempt, ListeningExercise, "play_count")
    )
    async with ctx.sessions() as db:
        assert await db.scalar(select(func.count(attempt_model.id))) == 1
        assert getattr(await db.get(exercise_model, exercise_id), counter) == 1
    history = await ctx.client.get(f"/api/{kind}/history", headers=ctx.headers)
    assert history.status_code == 200 and history.json()["total"] == 1
    assert await _xp(ctx) == 50


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["reading", "listening"])
async def test_replay_without_scored_attempt_is_rejected(operational, kind):  # noqa: F811
    """A replay must not reveal answers before the scored first attempt."""
    ctx = operational
    exercise_id = await (_reading_exercise(ctx) if kind == "reading" else _listening_exercise(ctx))
    replay = await ctx.client.post(f"/api/{kind}/attempt", headers=ctx.headers,
                                   json={"exercise_id": exercise_id, "answers": ALL_CORRECT, "replay": True})
    assert replay.status_code == 409 and replay.json()["detail"] == "not_attempted"
    first = await ctx.client.post(f"/api/{kind}/attempt", headers=ctx.headers,
                                  json={"exercise_id": exercise_id, "answers": ALL_CORRECT})
    assert first.status_code == 200 and first.json()["xp_earned"] == 50


@pytest.mark.asyncio
async def test_unique_index_allows_only_one_first_attempt(operational):  # noqa: F811
    ctx = operational
    exercise_id = await _reading_exercise(ctx)
    row = dict(user_id=ctx.user_id, exercise_id=exercise_id, study_plan_id=ctx.plan_id, answers=ALL_CORRECT, score=5, xp_earned=50)
    async with ctx.sessions() as db:
        db.add(ReadingAttempt(**row))
        await db.commit()
        # Historical duplicates marked as replay by migration 0071 remain valid.
        db.add(ReadingAttempt(**row, is_replay=True))
        await db.commit()
        db.add(ReadingAttempt(**row))
        with pytest.raises(IntegrityError):
            await db.commit()

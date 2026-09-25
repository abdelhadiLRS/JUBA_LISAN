"""Focused regression tests for adaptive and mixed game review selection."""

from __future__ import annotations

import pytest

from app.routers import progress as progress_router
from tests.conftest import make_study_plan


def _mistake(skill: str, key: str, *, review_count: int = 0) -> dict:
    return {
        "review_key": key,
        "skill": skill,
        "topic": f"{skill}-topic",
        "prompt": f"Review {key}",
        "choices": ["A", "B", "C", "D"],
        "hint": "",
        "answer": "A",
        "difficulty": 1,
        "input_mode": "choice",
        "review_count": review_count,
        "target_language": "en-US",
        "cefr_level": "A1",
    }


@pytest.mark.asyncio
async def test_review_mix_balances_weak_skills_before_repeating_due_items(
    db_session, test_user, monkeypatch
):
    user, _ = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        target_language="en-US",
        cefr_level="A1",
        goals=["vocabulary", "grammar", "listening", "writing", "speaking"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )

    due = [
        _mistake("vocabulary", "v1"),
        _mistake("vocabulary", "v2"),
        _mistake("vocabulary", "v3"),
        _mistake("grammar", "g1"),
        _mistake("listening", "l1"),
        _mistake("writing", "w1"),
    ]
    monkeypatch.setattr(
        progress_router,
        "_get_recent_game_mistakes",
        lambda *args, **kwargs: due,
    )
    monkeypatch.setattr(
        progress_router,
        "_get_game_skills",
        lambda *args, **kwargs: {
            "vocabulary": 0.75,
            "grammar": 0.25,
            "listening": 0.35,
            "writing": 0.55,
            "speaking": 0.10,
        },
    )

    def fake_questions(game_id, language, difficulty, target_language, cefr_level):
        skill_by_game = {
            "quick_choice": "vocabulary",
            "grammar_duel": "grammar",
            "listening_detective": "listening",
            "translation_sprint": "writing",
            "context_quest": "speaking",
        }
        skill = skill_by_game[game_id]
        return [
            {
                "id": f"fresh-{skill}-{index}",
                "prompt": f"Fresh {skill} {index}",
                "choices": ["A", "B", "C", "D"],
                "hint": "",
                "answer": "A",
                "skill": skill,
                "difficulty": difficulty,
                "input_mode": "choice",
            }
            for index in range(5)
        ]

    monkeypatch.setattr(progress_router, "_server_game_questions", fake_questions)

    questions = await progress_router._build_multi_skill_review_questions(
        db_session, user.id, plan, "en", 2
    )

    assert len(questions) == 5
    skills = [question["skill"] for question in questions]
    assert set(skills) >= {"vocabulary", "grammar", "listening"}
    assert skills.count("vocabulary") <= 2
    assert all(question["review"] is True for question in questions[:4])


@pytest.mark.asyncio
async def test_review_mix_fills_short_due_queue_with_weak_skill_content(
    db_session, test_user, monkeypatch
):
    user, _ = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        target_language="en-US",
        cefr_level="A1",
        goals=["grammar", "speaking"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )

    due = [_mistake("grammar", "g1")]
    monkeypatch.setattr(
        progress_router,
        "_get_recent_game_mistakes",
        lambda *args, **kwargs: due,
    )
    monkeypatch.setattr(
        progress_router,
        "_get_game_skills",
        lambda *args, **kwargs: {"grammar": 0.20, "speaking": 0.30},
    )

    def fake_questions(game_id, language, difficulty, target_language, cefr_level):
        skill = {
            "grammar_duel": "grammar",
            "context_quest": "speaking",
        }[game_id]
        count = 1 if skill == "grammar" else 5
        return [
            {
                "id": f"fresh-{skill}-{index}",
                "prompt": f"Fresh {skill} {index}",
                "choices": ["A", "B"],
                "hint": "",
                "answer": "A",
                "skill": skill,
                "difficulty": difficulty,
                "input_mode": "choice",
            }
            for index in range(count)
        ]

    monkeypatch.setattr(progress_router, "_server_game_questions", fake_questions)

    questions = await progress_router._build_multi_skill_review_questions(
        db_session, user.id, plan, "en", 1
    )

    assert len(questions) == 5
    assert questions[0]["review"] is True
    assert {question["skill"] for question in questions} == {"grammar", "speaking"}


@pytest.mark.asyncio
async def test_review_mix_filters_mistakes_to_current_language_and_cefr(
    db_session, test_user, monkeypatch
):
    user, _ = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        target_language="en-US",
        cefr_level="A1",
        goals=["vocabulary"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )

    due = [
        _mistake("vocabulary", "correct"),
        {**_mistake("vocabulary", "wrong-language"), "target_language": "fr-FR"},
        {**_mistake("grammar", "wrong-level"), "cefr_level": "B2"},
    ]
    monkeypatch.setattr(
        progress_router,
        "_get_recent_game_mistakes",
        lambda *args, **kwargs: due,
    )
    monkeypatch.setattr(
        progress_router,
        "_get_game_skills",
        lambda *args, **kwargs: {"vocabulary": 0.2},
    )

    monkeypatch.setattr(
        progress_router,
        "_server_game_questions",
        lambda *args, **kwargs: [],
    )

    questions = await progress_router._build_multi_skill_review_questions(
        db_session, user.id, plan, "en", 1
    )

    assert len(questions) == 5
    assert questions[0]["review_key"] == "correct"
    assert all(
        question.get("target_language") == "en-US"
        and question.get("cefr_level") == "A1"
        for question in questions[:1]
    )


def test_review_interval_progresses_with_review_count():
    assert progress_router._review_interval(0).total_seconds() == 10 * 60
    assert progress_router._review_interval(1).total_seconds() == 60 * 60
    assert progress_router._review_interval(2).total_seconds() == 24 * 60 * 60
    assert progress_router._review_interval(3).total_seconds() == 3 * 24 * 60 * 60
    assert progress_router._review_interval(4).total_seconds() == 7 * 24 * 60 * 60
    assert progress_router._review_interval(99).total_seconds() == 7 * 24 * 60 * 60


def test_review_key_is_stable_and_normalized():
    first = {
        "skill": " Grammar ",
        "topic": "Past Tense",
        "prompt": "Choose the correct form",
        "answer": " Went ",
    }
    second = {
        "skill": "grammar",
        "topic": "past tense",
        "prompt": "choose the correct form",
        "answer": "went",
    }
    assert progress_router._review_key(first) == progress_router._review_key(second)


@pytest.mark.asyncio
async def test_review_mix_does_not_reuse_the_same_due_review_key(
    db_session, test_user, monkeypatch
):
    user, _ = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        target_language="en-US",
        cefr_level="A1",
        goals=["vocabulary", "grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )
    duplicate = _mistake("vocabulary", "same-key")
    due = [duplicate, {**duplicate, "prompt": "Same content again"}]
    monkeypatch.setattr(
        progress_router,
        "_get_recent_game_mistakes",
        lambda *args, **kwargs: due,
    )
    monkeypatch.setattr(
        progress_router,
        "_get_game_skills",
        lambda *args, **kwargs: {"vocabulary": 0.2, "grammar": 0.3},
    )
    monkeypatch.setattr(
        progress_router,
        "_server_game_questions",
        lambda *args, **kwargs: [
            {
                "id": "fresh-grammar",
                "prompt": "Fresh grammar",
                "choices": ["A", "B"],
                "hint": "",
                "answer": "A",
                "skill": "grammar",
                "difficulty": 1,
                "input_mode": "choice",
            }
        ],
    )

    questions = await progress_router._build_multi_skill_review_questions(
        db_session, user.id, plan, "en", 1
    )
    keys = [question.get("review_key") for question in questions if question.get("review")]
    assert len(keys) == len(set(keys))


@pytest.mark.asyncio
async def test_smart_review_uses_latest_marker_within_an_event(
    db_session, test_user
):
    from datetime import UTC, datetime, timedelta

    from app.models.game_progress_event import GameProgressEvent

    user, _ = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        target_language="en-US",
        cefr_level="A1",
        goals=["vocabulary"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )

    question = {
        "skill": "vocabulary",
        "topic": "daily-life",
        "prompt": "Choose the correct word",
        "answer": "hello",
        "input_mode": "choice",
        "target_language": "en-US",
        "cefr_level": "A1",
    }
    key = progress_router._review_key(question)
    event = GameProgressEvent(
        event_id="review-marker-order",
        user_id=user.id,
        study_plan_id=plan.id,
        game_id="quick_choice",
        questions_answered=1,
        correct_answers=1,
        round_score=25,
        created_at=datetime.now(UTC).replace(tzinfo=None) - timedelta(minutes=1),
        mistakes=[
            {
                "review_key": key,
                "review_count": 1,
                "next_review_at": (datetime.now(UTC).replace(tzinfo=None) - timedelta(minutes=2)).isoformat(),
                "question": question,
            },
            {"review_key": key, "resolved": True},
        ],
    )
    db_session.add(event)
    await db_session.commit()

    due = await progress_router._get_recent_game_mistakes(
        db_session, user.id, plan.id, limit=10
    )

    assert due == []


@pytest.mark.asyncio
async def test_smart_review_reopens_when_latest_marker_is_a_new_mistake(
    db_session, test_user
):
    from datetime import UTC, datetime, timedelta

    from app.models.game_progress_event import GameProgressEvent

    user, _ = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        target_language="en-US",
        cefr_level="A1",
        goals=["vocabulary"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )
    question = {
        "skill": "vocabulary",
        "topic": "daily-life",
        "prompt": "Choose the correct word",
        "answer": "hello",
        "input_mode": "choice",
        "target_language": "en-US",
        "cefr_level": "A1",
    }
    key = progress_router._review_key(question)
    due_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(minutes=2)
    event = GameProgressEvent(
        event_id="review-marker-reopen",
        user_id=user.id,
        study_plan_id=plan.id,
        game_id="quick_choice",
        questions_answered=1,
        correct_answers=0,
        round_score=0,
        created_at=datetime.now(UTC).replace(tzinfo=None) - timedelta(minutes=1),
        mistakes=[
            {"review_key": key, "resolved": True},
            {
                "review_key": key,
                "review_count": 2,
                "next_review_at": due_at.isoformat(),
                "question": question,
            },
        ],
    )
    db_session.add(event)
    await db_session.commit()

    due = await progress_router._get_recent_game_mistakes(
        db_session, user.id, plan.id, limit=10
    )

    assert len(due) == 1
    assert due[0]["review_key"] == key
    assert due[0]["review_count"] == 2


@pytest.mark.asyncio
async def test_smart_review_prefers_latest_marker_across_events(
    db_session, test_user
):
    from datetime import UTC, datetime, timedelta

    from app.models.game_progress_event import GameProgressEvent

    user, _ = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        target_language="en-US",
        cefr_level="A1",
        goals=["vocabulary"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )
    question = {
        "skill": "vocabulary",
        "topic": "daily-life",
        "prompt": "Choose the correct word",
        "answer": "hello",
        "input_mode": "choice",
        "target_language": "en-US",
        "cefr_level": "A1",
    }
    key = progress_router._review_key(question)
    now = datetime.now(UTC).replace(tzinfo=None)
    older = GameProgressEvent(
        event_id="older-review-marker",
        user_id=user.id,
        study_plan_id=plan.id,
        game_id="quick_choice",
        questions_answered=1,
        correct_answers=0,
        round_score=0,
        created_at=now - timedelta(minutes=3),
        mistakes=[{
            "review_key": key,
            "review_count": 1,
            "next_review_at": (now - timedelta(minutes=2)).isoformat(),
            "question": question,
        }],
    )
    newer = GameProgressEvent(
        event_id="newer-resolve-marker",
        user_id=user.id,
        study_plan_id=plan.id,
        game_id="quick_choice",
        questions_answered=1,
        correct_answers=1,
        round_score=25,
        created_at=now - timedelta(minutes=1),
        mistakes=[{"review_key": key, "resolved": True}],
    )
    db_session.add_all([older, newer])
    await db_session.commit()

    due = await progress_router._get_recent_game_mistakes(
        db_session, user.id, plan.id, limit=10
    )

    assert due == []


@pytest.mark.asyncio
async def test_game_session_completion_is_idempotent_for_xp_mastery_and_event_ledger(
    client, db_session, test_user_with_plan
):
    from sqlalchemy import func, select

    from app.models.game_progress import GameProgress
    from app.models.game_progress_event import GameProgressEvent
    from app.models.progress import Progress

    user, headers = test_user_with_plan

    started = await client.post(
        "/api/progress/game-session",
        json={"game_id": "quick_choice", "language": "en", "difficulty": 1},
        headers=headers,
    )
    assert started.status_code == 200, started.text
    session = started.json()

    payload = {
        "session_id": session["session_id"],
        "answers": [
            {"question_id": question["id"], "choice": question["choices"][0]}
            for question in session["questions"]
        ],
    }

    first = await client.post(
        "/api/progress/game-session/complete",
        json=payload,
        headers=headers,
    )
    assert first.status_code == 200, first.text
    first_result = first.json()

    progress_before = (
        await db_session.execute(
            select(GameProgress).where(
                GameProgress.user_id == user.id,
                GameProgress.study_plan_id == 1,
            )
        )
    ).scalar_one()
    event_count_before = (
        await db_session.execute(
            select(func.count(GameProgressEvent.id)).where(
                GameProgressEvent.user_id == user.id,
                GameProgressEvent.study_plan_id == 1,
            )
        )
    ).scalar_one()
    xp_before = (
        await db_session.execute(
            select(func.coalesce(func.sum(Progress.xp_earned), 0)).where(
                Progress.user_id == user.id,
                Progress.study_plan_id == 1,
            )
        )
    ).scalar_one()

    second = await client.post(
        "/api/progress/game-session/complete",
        json=payload,
        headers=headers,
    )
    assert second.status_code == 409, second.text

    progress_after = (
        await db_session.execute(
            select(GameProgress).where(
                GameProgress.user_id == user.id,
                GameProgress.study_plan_id == 1,
            )
        )
    ).scalar_one()
    event_count_after = (
        await db_session.execute(
            select(func.count(GameProgressEvent.id)).where(
                GameProgressEvent.user_id == user.id,
                GameProgressEvent.study_plan_id == 1,
            )
        )
    ).scalar_one()
    xp_after = (
        await db_session.execute(
            select(func.coalesce(func.sum(Progress.xp_earned), 0)).where(
                Progress.user_id == user.id,
                Progress.study_plan_id == 1,
            )
        )
    ).scalar_one()

    assert first_result["xp_earned"] >= 0
    assert progress_after.games_played == progress_before.games_played == 1
    assert progress_after.questions_answered == progress_before.questions_answered
    assert progress_after.correct_answers == progress_before.correct_answers
    assert event_count_after == event_count_before == 1
    assert xp_after == xp_before

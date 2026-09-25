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

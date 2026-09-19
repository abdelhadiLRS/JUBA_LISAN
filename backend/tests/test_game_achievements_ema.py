import pytest
from sqlalchemy import select

from app.models.game_progress import GameProgress
from app.models.game_session import GameSession
from app.models.progress import Progress
from tests.conftest import make_study_plan


@pytest.mark.asyncio
async def test_multi_skill_uses_projected_ema_score(
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
            date=__import__("datetime").date.today(),
            xp_earned=0,
            lessons_completed=0,
            exercises_correct=0,
            exercises_total=0,
            streak_day=1,
            skills={"math": 0.1, "vocabulary": 0.5, "grammar": 0.2},
        )
    )
    await db_session.commit()

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
        {
            "question_id": question["id"],
            "choice": next(
                choice
                for choice in question["choices"]
                if choice != session.questions[index]["answer"]
            ),
        }
        for index, question in enumerate(payload["questions"])
    ]
    completed = await client.post(
        "/api/progress/game-session/complete",
        json={"session_id": payload["session_id"], "answers": answers},
        headers=headers,
    )
    assert completed.status_code == 200
    result = completed.json()

    assert "multi_skill" in result["new_achievements"]

    progress = (
        await db_session.execute(
            select(Progress).where(Progress.study_plan_id == plan.id)
        )
    ).scalar_one()
    assert progress.skills["math"] == 0.07

    game_progress = (
        await db_session.execute(
            select(GameProgress).where(GameProgress.study_plan_id == plan.id)
        )
    ).scalar_one()
    assert "multi_skill" in game_progress.achievements

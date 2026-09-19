from datetime import date, timedelta

import pytest


@pytest.mark.asyncio
async def test_progress_summary_empty(client, test_user):
    user, headers = test_user

    response = await client.get("/api/progress/summary", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_xp"] == 0
    assert data["current_streak"] == 0


@pytest.mark.asyncio
async def test_progress_summary_and_history_ignore_other_user_rows(
    client, test_user, db_session
):
    user, headers = test_user

    from app.models.progress import Progress
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )

    from app.core.security import hash_password
    from app.models.user import User
    from app.models.user_language import UserLanguage

    other = User(
        username="progress-isolation-user",
        email="progress-isolation-user@example.com",
        display_name="Progress Isolation User",
        hashed_password=hash_password("otherpass"),
        role="user",
        native_language="fr",
        target_language="en-US",
        is_active=True,
    )
    db_session.add(other)
    await db_session.flush()
    db_session.add(UserLanguage(user_id=other.id, target_language="en-US", is_active=True))
    db_session.add(
        Progress(
            user_id=other.id,
            study_plan_id=plan.id,
            xp_earned=9999,
            lessons_completed=99,
            exercises_correct=99,
            exercises_total=100,
            streak_day=99,
            skills={"grammar": 0.99},
        )
    )
    await db_session.commit()

    summary = await client.get("/api/progress/summary", headers=headers)
    assert summary.status_code == 200
    assert summary.json()["total_xp"] == 0
    assert summary.json()["total_lessons"] == 0
    assert summary.json()["total_exercises"] == 0

    history = await client.get("/api/progress/history", headers=headers)
    assert history.status_code == 200
    assert history.json()["entries"] == []


@pytest.mark.asyncio
async def test_progress_history_empty(client, test_user):
    user, headers = test_user

    response = await client.get("/api/progress/history", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["entries"] == []


@pytest.mark.asyncio
async def test_progress_with_data(client, test_user, db_session):
    user, headers = test_user

    from app.data.vocabulary import get_vocabulary_by_level
    from app.models.flashcard import Flashcard
    from app.models.progress import Progress
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )

    progress = Progress(
        user_id=user.id,
        study_plan_id=plan.id,
        xp_earned=50,
        lessons_completed=2,
        exercises_correct=8,
        exercises_total=10,
        streak_day=3,
        skills={"grammar": 0.6, "vocabulary": 0.4},
    )
    db_session.add(progress)
    vocab_sets = get_vocabulary_by_level("A1", "en-US")
    first_word = vocab_sets[0].words[0].word
    second_word = vocab_sets[0].words[1].word
    total_a1_words = sum(len(vocab_set.words) for vocab_set in vocab_sets)
    db_session.add_all(
        [
            Flashcard(
                user_id=user.id,
                study_plan_id=plan.id,
                word=first_word,
                definition="Definition",
                example_sentence="Example sentence.",
                translation="Translation",
                repetitions=1,
            ),
            Flashcard(
                user_id=user.id,
                study_plan_id=plan.id,
                word=second_word,
                definition="Definition",
                example_sentence="Example sentence.",
                translation="Translation",
                repetitions=0,
            ),
        ]
    )
    await db_session.commit()

    response = await client.get("/api/progress/summary", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_xp"] == 50
    assert data["current_streak"] == 3
    assert data["accuracy"] == 0.8
    assert data["vocabulary_level"] == "A1"
    assert data["vocabulary_mastered"] == 1
    assert data["vocabulary_total"] == total_a1_words
    assert data["vocabulary_progress"] == round(1 / total_a1_words, 2)


@pytest.mark.asyncio
async def test_progress_summary_expires_stale_streak(client, test_user, db_session):
    user, headers = test_user

    from app.models.progress import Progress
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    db_session.add(
        Progress(
            user_id=user.id,
            study_plan_id=plan.id,
            date=date.today() - timedelta(days=2),
            xp_earned=30,
            lessons_completed=1,
            exercises_correct=1,
            exercises_total=1,
            streak_day=4,
            skills={},
        )
    )
    await db_session.commit()

    response = await client.get("/api/progress/summary", headers=headers)
    assert response.status_code == 200
    assert response.json()["current_streak"] == 0


@pytest.mark.asyncio
async def test_empty_progress_update_does_not_create_streak_entry(db_session, test_user):
    user, _ = test_user

    from sqlalchemy import select

    from app.models.progress import Progress
    from app.services.progress_service import update_daily_progress
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )

    entry = await update_daily_progress(
        db_session,
        user.id,
        study_plan_id=plan.id,
        commit=False,
    )
    assert entry is None

    result = await db_session.execute(
        select(Progress).where(Progress.user_id == user.id)
    )
    assert result.scalars().all() == []


@pytest.mark.asyncio
async def test_activity_after_yesterday_continues_streak(db_session, test_user):
    user, _ = test_user

    from app.models.progress import Progress
    from app.services.progress_service import update_daily_progress
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    db_session.add(
        Progress(
            user_id=user.id,
            study_plan_id=plan.id,
            date=date.today() - timedelta(days=1),
            xp_earned=10,
            lessons_completed=0,
            exercises_correct=0,
            exercises_total=0,
            streak_day=4,
            skills={},
        )
    )
    await db_session.commit()

    entry = await update_daily_progress(
        db_session,
        user.id,
        study_plan_id=plan.id,
        lesson_completed=True,
        commit=False,
    )
    assert entry is not None
    assert entry.streak_day == 5


@pytest.mark.asyncio
async def test_same_day_activity_accumulates_in_one_progress_row(db_session, test_user):
    user, _ = test_user

    from sqlalchemy import select

    from app.models.progress import Progress
    from app.services.progress_service import update_daily_progress
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )

    first = await update_daily_progress(
        db_session,
        user.id,
        study_plan_id=plan.id,
        lesson_completed=True,
        commit=False,
    )
    second = await update_daily_progress(
        db_session,
        user.id,
        study_plan_id=plan.id,
        exercise_correct=True,
        commit=False,
    )
    await db_session.commit()

    assert first is second
    assert second.streak_day == 1
    assert second.lessons_completed == 1
    assert second.exercises_total == 1
    assert second.exercises_correct == 1

    result = await db_session.execute(
        select(Progress).where(
            Progress.user_id == user.id,
            Progress.study_plan_id == plan.id,
        )
    )
    assert len(result.scalars().all()) == 1


@pytest.mark.asyncio
async def test_streak_does_not_cross_study_plans(db_session, test_user):
    user, _ = test_user

    from app.models.progress import Progress
    from app.services.progress_service import update_daily_progress
    from tests.conftest import make_study_plan

    previous_plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    current_plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A2",
        target_language="en-US",
        goals=["vocabulary"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=False,
    )
    db_session.add(
        Progress(
            user_id=user.id,
            study_plan_id=previous_plan.id,
            date=date.today() - timedelta(days=1),
            xp_earned=10,
            lessons_completed=1,
            exercises_correct=0,
            exercises_total=0,
            streak_day=7,
            skills={},
        )
    )
    await db_session.commit()

    entry = await update_daily_progress(
        db_session,
        user.id,
        study_plan_id=current_plan.id,
        lesson_completed=True,
        commit=False,
    )
    assert entry is not None
    assert entry.streak_day == 1
    assert entry.study_plan_id == current_plan.id

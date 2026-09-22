import pytest


@pytest.mark.asyncio
async def test_mastery_center_returns_empty_snapshot_without_active_plan(client, test_user):
    _, headers = test_user
    response = await client.get("/api/progress/mastery", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "mastery_state": "unseen",
        "total_exercises": 0,
        "attempted_exercises": 0,
        "mastered_exercises": 0,
        "learning_exercises": 0,
        "struggling_exercises": 0,
        "unseen_exercises": 0,
        "average_mastery_score": 0.0,
        "mastery_rate": 0.0,
        "attempt_rate": 0.0,
        "covered_variants": 0,
        "skills": [],
        "lessons": [],
        "next_skill": None,
    }


@pytest.mark.asyncio
async def test_mastery_center_aggregates_lessons_skills_and_next_skill(client, test_user, db_session):
    from app.models.lesson import Exercise, Lesson
    from app.models.exercise_attempt import ExerciseAttempt
    from tests.conftest import make_study_plan

    user, headers = test_user
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
    first = Lesson(
        study_plan_id=plan.id,
        title="Grammar basics",
        lesson_type="lesson",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        content={"exercises": [
            {"content_id": "grammar-1", "skills": ["Grammar"]},
            {"content_id": "grammar-2", "skills": ["Grammar"]},
        ]},
    )
    second = Lesson(
        study_plan_id=plan.id,
        title="Vocabulary basics",
        lesson_type="lesson",
        cefr_level="A1",
        week_number=1,
        day_number=2,
        content={"exercises": [
            {"content_id": "vocab-1", "skills": ["Vocabulary"]},
        ]},
    )
    db_session.add_all([first, second])
    await db_session.flush()

    exercises = [
        Exercise(lesson_id=first.id, exercise_type="multiple_choice", question="q1", correct_answer="a"),
        Exercise(lesson_id=first.id, exercise_type="multiple_choice", question="q2", correct_answer="a"),
        Exercise(lesson_id=second.id, exercise_type="multiple_choice", question="q3", correct_answer="a"),
    ]
    db_session.add_all(exercises)
    await db_session.flush()
    db_session.add_all([
        ExerciseAttempt(
            user_id=user.id, exercise_id=exercises[0].id, lesson_id=first.id, study_plan_id=plan.id,
            content_id="grammar-1", variant="a", attempt_number=1, user_answer="a", score=0.9, feedback="ok",
        ),
        ExerciseAttempt(
            user_id=user.id, exercise_id=exercises[0].id, lesson_id=first.id, study_plan_id=plan.id,
            content_id="grammar-1", variant="b", attempt_number=2, user_answer="a", score=0.9, feedback="ok",
        ),
        ExerciseAttempt(
            user_id=user.id, exercise_id=exercises[1].id, lesson_id=first.id, study_plan_id=plan.id,
            content_id="grammar-2", variant="a", attempt_number=1, user_answer="a", score=0.2, feedback="retry",
        ),
        ExerciseAttempt(
            user_id=user.id, exercise_id=exercises[2].id, lesson_id=second.id, study_plan_id=plan.id,
            content_id="vocab-1", variant="a", attempt_number=1, user_answer="a", score=0.6, feedback="keep practicing",
        ),
    ])
    await db_session.commit()

    response = await client.get("/api/progress/mastery", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["mastery_state"] == "struggling"
    assert data["total_exercises"] == 3
    assert data["attempted_exercises"] == 3
    assert data["mastered_exercises"] == 1
    assert data["struggling_exercises"] == 1
    assert data["unseen_exercises"] == 0
    assert data["attempt_rate"] == 1.0
    assert len(data["lessons"]) == 2
    assert data["lessons"][0]["title"] == "Grammar basics"
    assert data["lessons"][0]["mastery_state"] == "struggling"
    assert {row["skill"] for row in data["skills"]} == {"grammar", "vocabulary"}
    assert data["next_skill"]["skill"] == "grammar"
    assert data["next_skill"]["mastery_state"] == "struggling"


@pytest.mark.asyncio
async def test_mastery_center_is_scoped_to_current_user(client, test_user, db_session):
    from app.core.security import create_access_token, hash_password
    from app.models.exercise_attempt import ExerciseAttempt
    from app.models.lesson import Exercise, Lesson
    from app.models.user import User
    from tests.conftest import make_study_plan

    user, headers = test_user
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
    lesson = Lesson(
        study_plan_id=plan.id,
        title="Scoped lesson",
        lesson_type="lesson",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        content={"exercises": [{"content_id": "scope-1", "skills": ["Grammar"]}]},
    )
    db_session.add(lesson)
    await db_session.flush()
    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="q",
        correct_answer="a",
    )
    db_session.add(exercise)
    await db_session.flush()

    other = User(
        username="mastery-other",
        email="mastery-other@example.com",
        display_name="Other Mastery User",
        hashed_password=hash_password("test-password"),
        role="user",
        native_language="es",
        target_language="en-US",
        is_active=True,
    )
    db_session.add(other)
    await db_session.flush()
    other_plan = await make_study_plan(
        db_session,
        user_id=other.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    other_lesson = Lesson(
        study_plan_id=other_plan.id,
        title="Other lesson",
        lesson_type="lesson",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        content={"exercises": [{"content_id": "other-1", "skills": ["Grammar"]}]},
    )
    db_session.add(other_lesson)
    await db_session.flush()
    other_exercise = Exercise(
        lesson_id=other_lesson.id,
        exercise_type="multiple_choice",
        question="other",
        correct_answer="a",
    )
    db_session.add(other_exercise)
    await db_session.flush()
    db_session.add(ExerciseAttempt(
        user_id=other.id,
        exercise_id=other_exercise.id,
        lesson_id=other_lesson.id,
        study_plan_id=other_plan.id,
        content_id="other-1",
        variant="a",
        attempt_number=1,
        user_answer="a",
        score=0.9,
        feedback="ok",
    ))
    await db_session.commit()

    response = await client.get("/api/progress/mastery", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["total_exercises"] == 1
    assert data["attempted_exercises"] == 0
    assert data["unseen_exercises"] == 1
    assert data["skills"] == [{
        "skill": "grammar",
        "mastery_state": "unseen",
        "total_exercises": 1,
        "attempted_exercises": 0,
        "mastered_exercises": 0,
        "learning_exercises": 0,
        "struggling_exercises": 0,
        "unseen_exercises": 1,
        "average_mastery_score": 0.0,
        "attempt_rate": 0.0,
        "mastery_rate": 0.0,
        "covered_variants": 0,
    }]
    assert data["next_skill"]["skill"] == "grammar"

    # The endpoint must never accept a caller-supplied user identity.
    other_headers = {"Authorization": f"Bearer {create_access_token(other.id, other.role)}"}
    other_response = await client.get("/api/progress/mastery", headers=other_headers)
    assert other_response.status_code == 200
    assert other_response.json()["total_exercises"] == 1
    assert other_response.json()["attempted_exercises"] == 1


@pytest.mark.asyncio
async def test_mastery_center_does_not_count_unmapped_exercise_content_as_attempted(client, test_user, db_session):
    from app.models.exercise_attempt import ExerciseAttempt
    from app.models.lesson import Exercise, Lesson
    from tests.conftest import make_study_plan

    user, headers = test_user
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
    lesson = Lesson(
        study_plan_id=plan.id,
        title="Unmapped lesson",
        lesson_type="lesson",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        content={"exercises": []},
    )
    db_session.add(lesson)
    await db_session.flush()
    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="q",
        correct_answer="a",
    )
    db_session.add(exercise)
    await db_session.flush()
    db_session.add(ExerciseAttempt(
        user_id=user.id,
        exercise_id=exercise.id,
        lesson_id=lesson.id,
        study_plan_id=plan.id,
        content_id="orphan-content",
        variant="a",
        attempt_number=1,
        user_answer="a",
        score=0.9,
        feedback="ok",
    ))
    await db_session.commit()

    response = await client.get("/api/progress/mastery", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["total_exercises"] == 1
    assert data["attempted_exercises"] == 0
    assert data["unseen_exercises"] == 1
    assert data["average_mastery_score"] == 0.0

@pytest.mark.asyncio
async def test_mastery_center_normalizes_and_deduplicates_skill_labels(client, test_user, db_session):
    from app.models.lesson import Exercise, Lesson
    from tests.conftest import make_study_plan

    user, headers = test_user
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
    lesson = Lesson(
        study_plan_id=plan.id,
        title="Normalized skills",
        lesson_type="lesson",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        content={"exercises": [{
            "content_id": "normalized-1",
            "skills": [" Grammar ", "grammar", "", 7],
        }]},
    )
    db_session.add(lesson)
    await db_session.flush()
    db_session.add(Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="q",
        correct_answer="a",
    ))
    await db_session.commit()

    response = await client.get("/api/progress/mastery", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert [skill["skill"] for skill in data["skills"]] == ["grammar"]
    assert data["skills"][0]["total_exercises"] == 1
    assert data["next_skill"]["skill"] == "grammar"

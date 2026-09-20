from app.schemas.lessons import ExerciseContent


def test_exercise_content_accepts_reusable_content_metadata():
    exercise = ExerciseContent(
        type="translate",
        question="Translate: Hello",
        correct="Bonjour",
        accepted_answers=["Bonjour", "bonjour"],
        content_id="exercise_demo",
        variant="translation",
        metadata={"stage": "discover"},
    )

    assert exercise.content_id == "exercise_demo"
    assert exercise.variant == "translation"
    assert exercise.correct in exercise.accepted_answers
    assert exercise.metadata == {"stage": "discover"}


def test_exercise_content_inserts_canonical_answer_into_accepted_answers():
    exercise = ExerciseContent(
        type="translate",
        question="Translate: Hello",
        correct="Bonjour",
        accepted_answers=["bonjour"],
    )

    assert exercise.accepted_answers == ["bonjour", "Bonjour"]


def test_legacy_exercise_payload_remains_valid():
    exercise = ExerciseContent(
        type="multiple_choice",
        question="Choose the greeting",
        options=["Hello", "Goodbye"],
        correct="Hello",
    )

    assert exercise.content_id is None
    assert exercise.variant is None
    assert exercise.accepted_answers is None

from app.services.exercise_factory import build_exercise_variants, build_persisted_exercise_variants


def test_build_exercise_variants_reuses_one_content_id():
    source = {
        "content_id": "vocab_hello",
        "question": "Say hello: Hello",
        "correct": "Bonjour",
        "options": ["Bonjour", "Au revoir", "Merci"],
    }

    variants = build_exercise_variants(source)

    assert [item["type"] for item in variants] == [
        "multiple_choice",
        "translate",
        "fill_blank",
        "free_write",
    ]
    assert {item["content_id"] for item in variants} == {"vocab_hello"}
    assert all(item["correct"] == "Bonjour" for item in variants)
    assert variants[0]["options"][0] == "Bonjour"
    assert "___" in variants[2]["question"]


def test_factory_accepts_common_variant_aliases():
    source = {
        "content_id": "vocab_hello",
        "example": "Bonjour, comment allez-vous ?",
        "translation": "Hello, how are you?",
        "options": ["Hello, how are you?", "Good night"],
    }

    variants = build_exercise_variants(
        source,
        variants=["choice", "gap"],
        max_variants=2,
    )

    assert [item["type"] for item in variants] == ["multiple_choice", "fill_blank"]


def test_factory_rejects_content_without_stable_id():
    source = {
        "question": "Hello",
        "correct": "Bonjour",
    }

    try:
        build_exercise_variants(source)
    except ValueError as exc:
        assert "content_id" in str(exc)
    else:
        raise AssertionError("expected stable content id validation")


def test_persisted_factory_adds_deterministic_sibling_distractors():
    source = [
        {
            "type": "multiple_choice",
            "question": "Bonjour means?",
            "correct": "Hello",
            "content_id": "hello_01",
            "options": ["Hello"],
        },
        {
            "type": "multiple_choice",
            "question": "Au revoir means?",
            "correct": "Goodbye",
            "content_id": "bye_01",
            "options": ["Goodbye"],
        },
        {
            "type": "multiple_choice",
            "question": "Merci means?",
            "correct": "Thanks",
            "content_id": "thanks_01",
            "options": ["Thanks"],
        },
    ]

    first = build_persisted_exercise_variants(source)
    second = build_persisted_exercise_variants(source)

    first_options = first[0]["options"]
    second_options = second[0]["options"]
    assert first_options == second_options
    assert first_options[0] == "Hello"
    assert len(first_options) == 3
    assert set(first_options[1:]) == {"Goodbye", "Thanks"}


def test_distractors_exclude_accepted_answers_and_correct_answer():
    source = {
        "content_id": "hello_01",
        "question": "Hello",
        "correct": "Bonjour",
        "accepted_answers": ["Bonjour", "Salut"],
    }

    variants = build_exercise_variants(
        source,
        variants=["multiple_choice"],
        distractor_candidates=["Bonjour", "Salut", "Merci", "Au revoir"],
    )

    assert variants[0]["options"] == ["Bonjour", "Merci", "Au revoir"]


def test_distractors_are_independent_of_candidate_order_without_reordering_options():
    source = {
        "content_id": "hello_01",
        "question": "Hello",
        "correct": "Bonjour",
        "accepted_answers": ["Salut"],
        "options": ["Merci", "Salut", "Au revoir"],
    }

    first = build_exercise_variants(
        source,
        variants=["multiple_choice"],
        distractor_candidates=["Bonsoir", "Merci"],
    )
    second = build_exercise_variants(
        source,
        variants=["multiple_choice"],
        distractor_candidates=["Merci", "Bonsoir"],
    )

    assert first[0]["options"] == second[0]["options"]
    assert "Salut" not in first[0]["options"]
    assert first[0]["options"][:3] == ["Bonjour", "Merci", "Au revoir"]


def test_distractors_choose_one_stable_spelling_for_casefold_duplicates():
    source = {
        "content_id": "hello_01",
        "question": "Hello",
        "correct": "Bonjour",
    }

    first = build_exercise_variants(
        source,
        variants=["multiple_choice"],
        distractor_candidates=["MERCI", "merci", "Au revoir"],
    )
    second = build_exercise_variants(
        source,
        variants=["multiple_choice"],
        distractor_candidates=["merci", "Au revoir", "MERCI"],
    )

    assert first[0]["options"] == second[0]["options"]
    assert len({option.casefold() for option in first[0]["options"]}) == len(first[0]["options"])


def test_factory_preserves_canonical_metadata_when_setting_variant_source():
    source = {
        "content_id": "hello_01",
        "question": "Hello",
        "correct": "Bonjour",
        "metadata": {"difficulty": "beginner", "topic": "greetings"},
    }

    variants = build_exercise_variants(source, variants=["translate"])

    assert variants[0]["metadata"] == {
        "difficulty": "beginner",
        "topic": "greetings",
        "source": "canonical_content",
    }

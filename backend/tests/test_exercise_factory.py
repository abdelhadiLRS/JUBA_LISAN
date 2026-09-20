from app.services.exercise_factory import build_exercise_variants


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

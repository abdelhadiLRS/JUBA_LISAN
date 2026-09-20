from app.services.exercise_factory import build_persisted_exercise_variants


def test_persisted_variants_keep_original_and_add_one_alternate():
    source = [
        {
            "type": "multiple_choice",
            "question": "How are you?",
            "correct": "Comment allez-vous ?",
            "options": ["Comment allez-vous ?", "Bonsoir"],
            "content_id": "hello_01",
            "explanation": "Formal greeting.",
            "accepted_answers": ["Comment allez-vous ?", "Comment vas-tu ?"],
        },
        {
            "type": "fill_blank",
            "question": "Je ___ bien.",
            "correct": "vais",
            "content_id": "hello_02",
        },
    ]

    result = build_persisted_exercise_variants(source)

    assert [item["type"] for item in result] == [
        "multiple_choice",
        "translate",
        "fill_blank",
        "free_write",
    ]
    assert [item["content_id"] for item in result] == [
        "hello_01",
        "hello_01",
        "hello_02",
        "hello_02",
    ]
    assert result[1]["correct"] == result[0]["correct"]
    assert result[1]["accepted_answers"] == source[0]["accepted_answers"]
    assert "___" in result[2]["question"]


def test_non_expandable_types_remain_one_to_one():
    source = [
        {
            "type": "pronunciation",
            "question": "Repeat: hello",
            "correct": "bonjour",
            "content_id": "speak_01",
        }
    ]

    result = build_persisted_exercise_variants(source)

    assert len(result) == 1
    assert result[0]["type"] == "pronunciation"
    assert result[0]["content_id"] == "speak_01"

from app.routers.progress import _server_game_questions


def test_word_game_issues_five_distinct_questions():
    questions = _server_game_questions("words", "en", 1, "en-GB")

    assert len(questions) == 5
    assert len({question["prompt"] for question in questions}) == 5
    assert all(question["skill"] == "vocabulary" for question in questions)


def test_word_game_keeps_four_distinct_choices_per_question():
    questions = _server_game_questions("words", "en", 1, "en-GB")

    assert all(len(question["choices"]) == 4 for question in questions)
    assert all(len(set(question["choices"])) == 4 for question in questions)
    assert all(question["answer"] in question["choices"] for question in questions)

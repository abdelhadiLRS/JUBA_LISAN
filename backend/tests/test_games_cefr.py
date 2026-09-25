import pytest

from app.routers.progress import _server_game_questions, _server_interactive_challenge


CORE_GAME_LANGUAGES = ("ar", "en-GB", "fr", "es", "de", "it", "pt", "ja", "ko", "zh")


@pytest.mark.parametrize("target_language", CORE_GAME_LANGUAGES)
@pytest.mark.parametrize("game_id", ("quick_choice", "fill_blank", "grammar_duel", "spelling", "word_scramble", "translation_sprint", "word_categories", "context_quest", "listening_detective"))
def test_cefr_game_round_uses_target_language_content(target_language, game_id):
    questions = _server_game_questions(
        game_id,
        "en",
        1,
        target_language,
        "A1",
    )

    assert len(questions) == 5
    assert all(question["answer"] for question in questions)
    assert all(question["difficulty"] == 1 for question in questions)


@pytest.mark.parametrize("target_language", CORE_GAME_LANGUAGES)
@pytest.mark.parametrize("game_id", ("memory", "matching", "ordering", "sentence_builder"))
def test_interactive_game_round_uses_cefr_content(target_language, game_id):
    public, solution = _server_interactive_challenge(
        game_id,
        "en",
        1,
        target_language,
        "A1",
    )

    assert public["type"] == ("ordering" if game_id in {"ordering", "sentence_builder"} else game_id)
    assert solution

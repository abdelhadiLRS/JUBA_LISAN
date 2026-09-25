import pytest

from app.routers.progress import (
    _apply_smart_review,
    _prioritize_curriculum_entries,
    _server_game_questions,
    _server_interactive_challenge,
)


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



def test_smart_review_prefers_due_mistake_for_matching_skill():
    fresh = [
        {"id": "fresh-1", "prompt": "new", "choices": ["new", "alt"], "answer": "new", "skill": "vocabulary", "input_mode": "choice"},
        {"id": "fresh-2", "prompt": "new 2", "choices": ["two", "alt"], "answer": "two", "skill": "vocabulary", "input_mode": "choice"},
        {"id": "fresh-3", "prompt": "new 3", "choices": ["three", "alt"], "answer": "three", "skill": "vocabulary", "input_mode": "choice"},
        {"id": "fresh-4", "prompt": "new 4", "choices": ["four", "alt"], "answer": "four", "skill": "vocabulary", "input_mode": "choice"},
        {"id": "fresh-5", "prompt": "new 5", "choices": ["five", "alt"], "answer": "five", "skill": "vocabulary", "input_mode": "choice"},
    ]
    mistake = {
        "id": "old",
        "prompt": "old prompt",
        "choices": ["old answer", "wrong"],
        "answer": "old answer",
        "skill": "vocabulary",
        "input_mode": "choice",
        "target_language": "fr",
        "cefr_level": "A1",
    }

    reviewed = _apply_smart_review(fresh, [mistake], "fr", "A1")

    assert reviewed[0]["review"] is True
    assert reviewed[0]["answer"] == "old answer"
    assert reviewed[0]["id"] != "old"


def test_smart_review_rejects_cross_language_or_cefr_mistakes():
    fresh = [{"id": "fresh", "prompt": "new", "choices": ["new", "alt"], "answer": "new", "skill": "vocabulary", "input_mode": "choice"}]
    wrong_language = {"prompt": "old", "answer": "ancien", "choices": ["ancien", "other"], "skill": "vocabulary", "input_mode": "choice", "target_language": "fr", "cefr_level": "A1"}

    reviewed = _apply_smart_review(fresh, [wrong_language], "de", "A1")

    assert reviewed == fresh


def test_smart_review_backfills_with_fresh_questions():
    fresh = [
        {"id": "q1", "prompt": "one", "choices": ["one", "alt"], "answer": "one", "skill": "grammar", "input_mode": "choice"},
        {"id": "q2", "prompt": "two", "choices": ["two", "alt"], "answer": "two", "skill": "grammar", "input_mode": "choice"},
        {"id": "q3", "prompt": "three", "choices": ["three", "alt"], "answer": "three", "skill": "grammar", "input_mode": "choice"},
        {"id": "q4", "prompt": "four", "choices": ["four", "alt"], "answer": "four", "skill": "grammar", "input_mode": "choice"},
        {"id": "q5", "prompt": "five", "choices": ["five", "alt"], "answer": "five", "skill": "grammar", "input_mode": "choice"},
    ]
    mistakes = [
        {"prompt": "old", "answer": "old", "choices": ["old", "q"], "skill": "grammar", "input_mode": "choice", "target_language": "en-GB", "cefr_level": "A1"},
    ]

    reviewed = _apply_smart_review(fresh, mistakes, "en-GB", "A1")

    assert len(reviewed) == 5
    assert reviewed[0]["review"] is True
    assert all(item.get("review") is not True for item in reviewed[1:])


def test_smart_review_keeps_server_answer_private_from_public_projection():
    fresh = [{"id": "q1", "prompt": "one", "choices": ["one", "alt"], "answer": "one", "skill": "vocabulary", "input_mode": "choice"}]
    mistake = {"prompt": "old", "answer": "secret-answer", "choices": ["secret-answer", "wrong"], "skill": "vocabulary", "input_mode": "choice", "target_language": "fr", "cefr_level": "A1"}
    reviewed = _apply_smart_review(fresh, [mistake], "fr", "A1")
    public = {key: reviewed[0].get(key) for key in ("id", "prompt", "choices", "hint", "skill", "difficulty", "input_mode")}

    assert "answer" not in public
    assert reviewed[0]["answer"] == "secret-answer"



def test_curriculum_topic_priority_keeps_weak_topic_majority_and_diversity():
    entries = [
        (f"travel-{index}", "travel") for index in range(6)
    ] + [
        (f"food-{index}", "food") for index in range(6)
    ]
    selected = _prioritize_curriculum_entries(entries, ["travel"], count=5)
    selected_topics = [topic for entry in selected for candidate, topic in entries if candidate == entry]

    assert len(selected) == 5
    assert selected_topics.count("travel") >= 3
    assert selected_topics.count("food") >= 1


def test_curriculum_topic_priority_without_history_remains_broad():
    entries = [("one", "travel"), ("two", "food"), ("three", "school"), ("four", "home"), ("five", "work")]
    selected = _prioritize_curriculum_entries(entries, None, count=5)

    assert set(selected) == {entry for entry, _topic in entries}

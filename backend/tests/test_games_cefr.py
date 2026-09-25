import pytest
from datetime import datetime, timedelta
from types import SimpleNamespace

from app.data.vocabulary import get_vocabulary_by_level
from app.routers.progress import (
    _apply_smart_review,
    _item_mastery_from_events,
    _mastery_review_count,
    _prioritize_curriculum_entries,
    _server_game_questions,
    _server_interactive_challenge,
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


@pytest.mark.parametrize("game_id", ("memory", "matching", "ordering", "sentence_builder"))
def test_interactive_game_accepts_topic_preferences(game_id):
    public, solution = _server_interactive_challenge(
        game_id,
        "en",
        1,
        "en-GB",
        "A1",
        ["travel"],
    )

    assert public["type"] == ("ordering" if game_id in {"ordering", "sentence_builder"} else game_id)
    assert solution


def test_interactive_review_prefers_exact_previous_item():
    vocabulary = get_vocabulary_by_level("A1", "en-GB")
    entry = vocabulary[0].words[0]
    reviewed_public, _ = _server_interactive_challenge(
        "memory",
        "en",
        1,
        "en-GB",
        "A1",
        None,
        [{"word": entry.word, "definition": entry.definition}],
    )
    assert any(card["label"] == entry.word for card in reviewed_public["cards"])



@pytest.mark.parametrize(
    ("mastery_items", "total", "difficulty", "expected"),
    [
        ([], 5, 1, 0),
        ([{"mastery_state": "learning"}], 5, 1, 1),
        ([{"mastery_state": "learning"}, {"mastery_state": "learning"}], 5, 1, 2),
        ([{"mastery_state": "reviewing"}], 5, 2, 2),
        ([{"mastery_state": "weak"}], 5, 2, 2),
        ([{"mastery_state": "weak"}, {"mastery_state": "weak"}], 5, 1, 4),
        ([{"mastery_state": "weak"}, {"mastery_state": "reviewing"}, {"mastery_state": "mastered"}], 5, 2, 2),
        ([{"mastery_state": "mastered"}, {"mastery_state": "mastered"}], 5, 1, 0),
    ],
)
def test_mastery_review_count_balances_fresh_and_review_content(
    mastery_items, total, difficulty, expected
):
    assert _mastery_review_count(mastery_items, total, difficulty) == expected


def test_mastery_review_count_never_exceeds_available_active_items():
    items = [{"mastery_state": "weak"}]
    assert _mastery_review_count(items, 5, 1) == 1


def test_mastery_review_count_keeps_more_fresh_content_at_high_difficulty():
    weak_items = [{"mastery_state": "reviewing"}]
    assert _mastery_review_count(weak_items, 5, 3) == 2


def _mastery_event(at, key, *, question=None, resolved=False):
    item = {"review_key": key, "resolved": resolved}
    if question is not None:
        item["question"] = question
    return SimpleNamespace(created_at=at, mistakes=[item])


async def test_tracked_mastery_summary_groups_items_by_skill_and_state():
    from app.routers.progress import _get_tracked_mastery_summary

    question_v = {"skill": "vocabulary", "target_language": "fr", "cefr_level": "A1"}
    question_g = {"skill": "grammar", "target_language": "fr", "cefr_level": "A1"}
    base = datetime(2026, 1, 1)
    events = [
        SimpleNamespace(
            created_at=base,
            mistakes=[
                {"review_key": "v:hello", "question": question_v},
                {"review_key": "g:past", "question": question_g},
            ],
        ),
        SimpleNamespace(
            created_at=base + timedelta(days=1),
            mistakes=[
                {"review_key": "v:hello", "resolved": True},
                {"review_key": "g:past", "question": question_g},
            ],
        ),
        SimpleNamespace(
            created_at=base + timedelta(days=2),
            mistakes=[
                {"review_key": "v:hello", "resolved": True},
                {"review_key": "v:hello", "resolved": True},
            ],
        ),
    ]

    class FakeResult:
        def scalars(self):
            return self

        def all(self):
            return events

    class FakeDB:
        async def execute(self, _query):
            return FakeResult()

    summary = await _get_tracked_mastery_summary(FakeDB(), 1, 1)

    assert summary["tracked_items"] == 2
    assert summary["counts"]["mastered"] == 1
    assert summary["counts"]["weak"] == 1
    assert summary["skills"]["vocabulary"]["items"] == 1
    assert summary["skills"]["grammar"]["items"] == 1


def test_tracked_mastery_summary_uses_study_plan_scope():
    from app.routers.progress import _get_tracked_mastery_summary

    class FakeResult:
        def scalars(self):
            return self

        def all(self):
            return []

    class FakeDB:
        def __init__(self):
            self.query = None

        async def execute(self, query):
            self.query = query
            return FakeResult()

    db = FakeDB()
    import asyncio
    summary = asyncio.run(_get_tracked_mastery_summary(db, 7, 42))

    assert summary["tracked_items"] == 0
    assert "game_progress_events.study_plan_id" in str(db.query)
    assert "game_progress_events.user_id" in str(db.query)


def test_item_mastery_repeated_misses_becomes_weak():
    key = "vocabulary:travel:hello:bonjour"
    base = datetime(2026, 1, 1)
    events = [
        _mastery_event(base + timedelta(days=index), key, question={"skill": "vocabulary", "target_language": "fr", "cefr_level": "A1"})
        for index in range(3)
    ]

    mastery = _item_mastery_from_events(events, key, "vocabulary", "fr", "A1")

    assert mastery["state"] == "weak"
    assert mastery["misses"] == 3
    assert float(mastery["score"]) < 0.5


def test_item_mastery_successful_retrieval_moves_to_reviewing():
    key = "vocabulary:travel:hello:bonjour"
    base = datetime(2026, 1, 1)
    question = {"skill": "vocabulary", "target_language": "fr", "cefr_level": "A1"}
    events = [
        _mastery_event(base, key, question=question),
        _mastery_event(base + timedelta(days=1), key, resolved=True),
    ]

    mastery = _item_mastery_from_events(events, key, "vocabulary", "fr", "A1")

    assert mastery["state"] == "reviewing"
    assert mastery["misses"] == 1
    assert mastery["resolutions"] == 1


def test_item_mastery_repeated_successes_becomes_mastered():
    key = "vocabulary:travel:hello:bonjour"
    base = datetime(2026, 1, 1)
    question = {"skill": "vocabulary", "target_language": "fr", "cefr_level": "A1"}
    events = [
        _mastery_event(base, key, question=question),
        _mastery_event(base + timedelta(days=1), key, resolved=True),
        _mastery_event(base + timedelta(days=2), key, resolved=True),
        _mastery_event(base + timedelta(days=3), key, resolved=True),
    ]

    mastery = _item_mastery_from_events(events, key, "vocabulary", "fr", "A1")

    assert mastery["state"] == "mastered"
    assert float(mastery["score"]) > 0.7


def test_item_mastery_filters_language_and_cefr():
    key = "vocabulary:travel:hello:bonjour"
    base = datetime(2026, 1, 1)
    events = [
        _mastery_event(
            base,
            key,
            question={"skill": "vocabulary", "target_language": "de", "cefr_level": "B1"},
        ),
    ]

    mastery = _item_mastery_from_events(events, key, "vocabulary", "fr", "A1")

    assert mastery["state"] == "new"
    assert mastery["misses"] == 0


def test_item_mastery_score_prioritizes_weak_over_mastered():
    key_weak = "vocabulary:travel:weak:bonjour"
    key_mastered = "vocabulary:travel:mastered:salut"
    base = datetime(2026, 1, 1)
    question = {"skill": "vocabulary", "target_language": "fr", "cefr_level": "A1"}
    weak_events = [
        _mastery_event(base, key_weak, question=question),
        _mastery_event(base + timedelta(days=1), key_weak, question=question),
        _mastery_event(base + timedelta(days=2), key_weak, question=question),
    ]
    mastered_events = [
        _mastery_event(base, key_mastered, question=question),
        _mastery_event(base + timedelta(days=1), key_mastered, resolved=True),
        _mastery_event(base + timedelta(days=2), key_mastered, resolved=True),
        _mastery_event(base + timedelta(days=3), key_mastered, resolved=True),
    ]

    weak = _item_mastery_from_events(weak_events, key_weak, "vocabulary", "fr", "A1")
    mastered = _item_mastery_from_events(mastered_events, key_mastered, "vocabulary", "fr", "A1")

    assert float(weak["score"]) < float(mastered["score"])
    assert weak["state"] == "weak"
    assert mastered["state"] == "mastered"


def test_review_game_changes_mechanic_with_mastery_state():
    from app.routers.progress import _review_game_for_item

    assert _review_game_for_item("vocabulary", "weak") == "quick_choice"
    assert _review_game_for_item("vocabulary", "learning") == "quick_choice"
    assert _review_game_for_item("vocabulary", "reviewing") == "word_categories"
    assert _review_game_for_item("grammar", "weak") == "grammar_duel"
    assert _review_game_for_item("grammar", "reviewing") == "fill_blank"
    assert _review_game_for_item("listening", "weak") == "listening_detective"
    assert _review_game_for_item("speaking", "reviewing") == "context_quest"
    assert _review_game_for_item("unknown", "weak") is None

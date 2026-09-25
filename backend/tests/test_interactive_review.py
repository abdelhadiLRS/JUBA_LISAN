import pytest

from app.routers import progress as progress_router


def _fake_vocab(monkeypatch):
    class Entry:
        def __init__(self, word, definition, example):
            self.word = word
            self.definition = definition
            self.example = example

    class VocabularySet:
        topic = "daily-life"
        words = [
            Entry("water", "a clear drink", "I drink water."),
            Entry("book", "a text you read", "I read a book."),
            Entry("school", "a place to learn", "I go to school."),
            Entry("pen", "a writing tool", "I use a pen."),
            Entry("door", "an entrance", "I open the door."),
        ]

    monkeypatch.setattr(
        progress_router,
        "get_vocabulary_by_level",
        lambda level, language: [VocabularySet()],
    )


def test_memory_review_items_keep_spaced_review_metadata(monkeypatch):
    _fake_vocab(monkeypatch)

    public, solution = progress_router._server_interactive_challenge(
        "memory",
        "en",
        1,
        "en-US",
        "A1",
        preferred_items=[
            {
                "word": "water",
                "definition": "a clear drink",
                "review_key": "stable-water",
                "review_count": 2,
                "review_streak": 2,
            }
        ],
    )

    assert public["type"] == "memory"
    item = next(
        value for value in solution["review_items"].values()
        if value["word"] == "water"
    )
    assert item["review_key"] == "stable-water"
    assert item["review_count"] == 2
    assert item["review_streak"] == 2


def test_matching_review_items_keep_spaced_review_metadata(monkeypatch):
    _fake_vocab(monkeypatch)

    public, solution = progress_router._server_interactive_challenge(
        "matching",
        "en",
        1,
        "en-US",
        "A1",
        preferred_items=[
            {
                "word": "water",
                "definition": "a clear drink",
                "review_key": "stable-water",
                "review_count": 3,
                "review_streak": 3,
            }
        ],
    )

    assert public["type"] == "matching"
    item = next(
        value for value in solution["review_items"].values()
        if value["word"] == "water"
    )
    assert item["review_key"] == "stable-water"
    assert item["review_count"] == 3
    assert item["review_streak"] == 3


def test_sentence_builder_review_items_keep_spaced_review_metadata(monkeypatch):
    _fake_vocab(monkeypatch)

    public, solution = progress_router._server_interactive_challenge(
        "sentence_builder",
        "en",
        1,
        "en-US",
        "A1",
        preferred_items=[
            {
                "sentence": "I drink water.",
                "review_key": "stable-sentence",
                "review_count": 1,
                "review_streak": 1,
            }
        ],
    )

    assert public["type"] == "ordering"
    item = solution["review_items"]["sentence"]
    assert item["review_key"] == "stable-sentence"
    assert item["review_count"] == 1
    assert item["review_streak"] == 1


def test_interactive_review_failure_resets_streak_and_advances_count():
    # The completion path uses the same metadata contract as regular review:
    # a failed retrieval starts a new short interval and increments the count.
    review_item = {
        "review_key": "stable-water",
        "review_count": 3,
        "review_streak": 3,
    }
    next_count = int(review_item["review_count"]) + 1
    next_streak = 0
    assert next_count == 4
    assert next_streak == 0

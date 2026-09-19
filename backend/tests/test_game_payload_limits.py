import pytest
from pydantic import ValidationError

from app.schemas.progress import GameSessionComplete


def test_game_completion_rejects_more_than_five_answers():
    payload = {
        "session_id": "session-1",
        "answers": [
            {"question_id": str(index), "choice": "answer"}
            for index in range(6)
        ],
    }

    with pytest.raises(ValidationError):
        GameSessionComplete.model_validate(payload)


def test_game_completion_rejects_more_than_one_hundred_interaction_attempts():
    payload = {
        "session_id": "session-1",
        "interaction_trace": [{"first": "a", "second": "b"} for _ in range(101)],
    }

    with pytest.raises(ValidationError):
        GameSessionComplete.model_validate(payload)


def test_game_completion_bounds_answer_text_and_identifiers():
    payload = {
        "session_id": "s" * 65,
        "answers": [{"question_id": "q", "choice": "a"}],
    }

    with pytest.raises(ValidationError):
        GameSessionComplete.model_validate(payload)


def test_game_completion_rejects_oversized_interaction_fields():
    payload = {
        "session_id": "session-1",
        "interaction_trace": [{"first": "x" * 65}],
    }

    with pytest.raises(ValidationError):
        GameSessionComplete.model_validate(payload)


def test_game_completion_rejects_nested_interaction_values():
    payload = {
        "session_id": "session-1",
        "interaction_trace": [{"order": [{"id": "a"}]}],
    }

    with pytest.raises(ValidationError):
        GameSessionComplete.model_validate(payload)


def test_game_completion_accepts_supported_interaction_shapes():
    payload = {
        "session_id": "session-1",
        "interaction_trace": [
            {"first": "card-a", "second": "card-b"},
            {"left": "left-a", "right": "right-a"},
            {"order": ["item-a", "item-b", "item-c"]},
        ],
    }

    result = GameSessionComplete.model_validate(payload)
    assert len(result.interaction_trace) == 3

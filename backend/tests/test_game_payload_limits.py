from app.schemas.progress import GameSessionComplete


def test_game_completion_rejects_more_than_five_answers():
    payload = {
        "session_id": "session-1",
        "answers": [
            {"question_id": str(index), "choice": "answer"}
            for index in range(6)
        ],
    }

    result = GameSessionComplete.model_validate(payload)

    assert False, result

from datetime import date, datetime, timezone

from app.schemas.flashcards import FlashcardListResponse, FlashcardResponse


def make_card(card_id: int) -> FlashcardResponse:
    return FlashcardResponse(
        id=card_id,
        user_id=1,
        word="hello",
        definition="a greeting",
        example_sentence="Hello there!",
        translation="bonjour",
        source="test",
        ease_factor=2.5,
        interval=1,
        repetitions=0,
        next_review=date(2026, 9, 8),
        created_at=datetime(2026, 9, 8, tzinfo=timezone.utc),
    )


def test_flashcard_list_response_populates_flashcards_alias() -> None:
    due = [make_card(1), make_card(2)]

    response = FlashcardListResponse(due=due, total=2)

    assert response.flashcards == due
    assert response.model_dump()["flashcards"] == due
    assert response.model_dump(mode="json")["flashcards"][0]["id"] == 1

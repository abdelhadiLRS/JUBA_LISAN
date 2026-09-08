from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class FlashcardCreate(BaseModel):
    word: str
    definition: str
    example_sentence: str
    translation: str
    source: Optional[str] = None


class FlashcardBulkCreate(BaseModel):
    flashcards: list[FlashcardCreate]


class FlashcardBulkResponse(BaseModel):
    created: int


class FlashcardReview(BaseModel):
    quality: int


class FlashcardFromWordRequest(BaseModel):
    word: str
    context: str = ""
    cefr_level: str = "B1"


class FlashcardGenerateRequest(BaseModel):
    topic: str
    count: int = Field(default=5, ge=1, le=20)
    cefr_level: str = "B1"
    target_language: str | None = None


class FlashcardResponse(BaseModel):
    id: int
    user_id: int
    word: str
    definition: str
    example_sentence: str
    translation: str
    source: Optional[str] = None
    ease_factor: float
    interval: int
    repetitions: int
    next_review: date
    created_at: datetime

    model_config = {"from_attributes": True}


class FlashcardListResponse(BaseModel):
    due: list[FlashcardResponse]
    total: int
    # Compatibility alias for clients that expect a generic `flashcards` list.
    flashcards: list[FlashcardResponse] | None = None

    @model_validator(mode="after")
    def populate_flashcards_alias(self):
        if self.flashcards is None:
            self.flashcards = self.due
        return self


class VocabularyListResponse(BaseModel):
    items: list[FlashcardResponse]
    total: int
    page: int
    pages: int


class GeneratedFlashcard(BaseModel):
    word: str
    definition: str
    example_sentence: str
    translation: str


class FlashcardGenerateResponse(BaseModel):
    flashcards: list[GeneratedFlashcard]

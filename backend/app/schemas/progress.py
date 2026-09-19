from __future__ import annotations

import math
from datetime import date

from pydantic import BaseModel, Field, field_serializer, field_validator


class ProgressResponse(BaseModel):
    id: int
    user_id: int
    date: date
    xp_earned: int
    lessons_completed: int
    exercises_correct: int
    exercises_total: int
    streak_day: int
    skills: dict

    model_config = {"from_attributes": True}

    @field_serializer("date")
    def serialize_date(self, v: date, _info):
        return v.isoformat()


class ProgressSummary(BaseModel):
    total_xp: int
    current_streak: int
    total_lessons: int
    total_exercises: int
    exercises_correct: int
    accuracy: float
    skills: dict
    vocabulary_level: str | None = None
    vocabulary_mastered: int = 0
    vocabulary_total: int = 0
    vocabulary_progress: float = 0.0


class ProgressHistoryResponse(BaseModel):
    entries: list[ProgressResponse]


class GameStatsResponse(BaseModel):
    total_xp: int = 0
    games_played: int
    questions_answered: int
    correct_answers: int
    best_round_score: int
    daily_challenges_completed: int
    last_daily_challenge_date: str
    current_correct_streak: int
    best_correct_streak: int
    achievements: list[str]
    skills: dict[str, float] = Field(default_factory=dict)

    model_config = {"from_attributes": True}


class GameSessionStart(BaseModel):
    game_id: str
    language: str = "en"
    difficulty: int = 1

    @field_validator("game_id")
    @classmethod
    def validate_game_id(cls, value: str) -> str:
        value = value.strip()
        if value not in {"math", "words", "sequence", "memory", "matching", "ordering"}:
            raise ValueError("game_id must be one of the supported games")
        return value

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in {"ar", "fr", "en"}:
            raise ValueError("language must be ar, fr or en")
        return value

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, value: int) -> int:
        if value not in {1, 2, 3}:
            raise ValueError("difficulty must be 1, 2 or 3")
        return value


class GameSessionQuestion(BaseModel):
    id: str
    prompt: str
    choices: list[str]
    hint: str
    skill: str
    difficulty: int


class GameSessionResponse(BaseModel):
    session_id: str
    game_id: str
    questions: list[GameSessionQuestion]
    expires_at: str
    interaction: dict | None = None


class GameSessionResultResponse(GameStatsResponse):
    round_score: int
    round_correct: int
    round_questions: int
    xp_earned: int
    new_achievements: list[str] = Field(default_factory=list)


class GameSessionAnswer(BaseModel):
    question_id: str
    choice: str


class GameSessionComplete(BaseModel):
    session_id: str
    answers: list[GameSessionAnswer] = Field(default_factory=list)
    interaction_trace: list[dict] = Field(default_factory=list)
    daily_challenge: bool = False
    daily_challenge_date: str = ""

    @field_validator("answers")
    @classmethod
    def validate_answers(cls, value: list[GameSessionAnswer]) -> list[GameSessionAnswer]:
        if not value:
            return []
        seen: set[str] = set()
        for answer in value:
            if answer.question_id in seen:
                raise ValueError("duplicate question_id")
            seen.add(answer.question_id)
        return value

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


class GameProgressUpdate(BaseModel):
    xp: int = 0
    correct_answers: int = 0
    questions_answered: int = 0
    skills: dict[str, float] = Field(default_factory=dict)

    @field_validator("skills")
    @classmethod
    def normalize_skills(cls, value: dict[str, float]) -> dict[str, float]:
        normalized: dict[str, float] = {}
        for skill, score in value.items():
            if not isinstance(skill, str) or not skill.strip():
                continue
            if not isinstance(score, (int, float)) or not math.isfinite(float(score)):
                continue
            normalized[skill.strip()] = max(0.0, min(1.0, float(score)))
        return normalized


class GameStatsResponse(BaseModel):
    games_played: int
    questions_answered: int
    correct_answers: int
    best_round_score: int
    daily_challenges_completed: int
    last_daily_challenge_date: str
    current_correct_streak: int
    best_correct_streak: int
    achievements: list[str]

    model_config = {"from_attributes": True}


class GameProgressEventCreate(BaseModel):
    event_id: str
    game_id: str
    questions_answered: int
    correct_answers: int
    round_score: int = 0
    daily_challenge: bool = False
    daily_challenge_date: str = ""
    achievements: list[str] = Field(default_factory=list)

    @field_validator("event_id")
    @classmethod
    def validate_event_id(cls, value: str) -> str:
        import uuid

        try:
            return str(uuid.UUID(value))
        except (ValueError, AttributeError, TypeError) as exc:
            raise ValueError("event_id must be a valid UUID") from exc

    @field_validator("game_id")
    @classmethod
    def validate_game_id(cls, value: str) -> str:
        value = value.strip()
        if not value or len(value) > 32:
            raise ValueError("game_id must be a non-empty value of at most 32 characters")
        return value

    @field_validator("questions_answered", "correct_answers", "round_score")
    @classmethod
    def validate_non_negative(cls, value: int) -> int:
        return max(0, value)

    @field_validator("achievements")
    @classmethod
    def normalize_achievements(cls, value: list[str]) -> list[str]:
        allowed = {
            "first_game",
            "perfect_round",
            "streak_5",
            "xp_100",
            "xp_500",
            "multi_skill",
            "daily_challenge",
        }
        return list(
            dict.fromkeys(
                item.strip()
                for item in value
                if isinstance(item, str) and item.strip() in allowed
            )
        )

    @field_validator("daily_challenge_date")
    @classmethod
    def normalize_daily_date(cls, value: str) -> str:
        value = value.strip()
        if value:
            try:
                date.fromisoformat(value)
            except ValueError as exc:
                raise ValueError("daily_challenge_date must be YYYY-MM-DD") from exc
        return value

    @field_validator("correct_answers")
    @classmethod
    def validate_correct_answers(cls, value: int, info) -> int:
        questions = info.data.get("questions_answered", 0)
        if value > questions:
            raise ValueError("correct_answers cannot exceed questions_answered")
        return value

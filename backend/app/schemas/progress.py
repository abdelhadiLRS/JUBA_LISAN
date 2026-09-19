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


class GameProgressSync(BaseModel):
    games_played: int = 0
    questions_answered: int = 0
    correct_answers: int = 0
    best_round_score: int = 0
    daily_challenges_completed: int = 0
    last_daily_challenge_date: str = ""
    current_correct_streak: int = 0
    best_correct_streak: int = 0
    achievements: list[str] = Field(default_factory=list)

    @field_validator(
        "games_played",
        "questions_answered",
        "correct_answers",
        "best_round_score",
        "daily_challenges_completed",
        "current_correct_streak",
        "best_correct_streak",
    )
    @classmethod
    def normalize_non_negative(cls, value: int) -> int:
        return max(0, value)

    @field_validator("achievements")
    @classmethod
    def normalize_achievements(cls, value: list[str]) -> list[str]:
        return list(dict.fromkeys(item.strip() for item in value if isinstance(item, str) and item.strip()))

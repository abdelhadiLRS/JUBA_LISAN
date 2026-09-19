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

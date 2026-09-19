from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, field_serializer, field_validator


SUPPORTED_LESSON_TYPES = {
    "grammar",
    "vocabulary",
    "reading",
    "writing",
    "listening",
    "conversation",
    "review",
    "level_test",
}


class StudyPlanGoal(BaseModel):
    goal: str


class GenerateStudyPlanRequest(BaseModel):
    cefr_level: str
    goals: list[str] = ["grammar", "vocabulary", "reading", "writing"]
    duration_weeks: int = 12
    days_per_week: int = 4
    weaknesses: list[str] = []
    strengths: list[str] = []
    target_language: str | None = None


class DayPlan(BaseModel):
    day: int
    lesson_type: str
    title: str
    objectives: list[str]
    estimated_minutes: int
    unit_id: str = ""
    grammar_points: list[str] = []
    vocabulary_set_ids: list[str] = []


class WeekPlan(BaseModel):
    week: int
    theme: str
    days: list[DayPlan]


class GeneratedPlan(BaseModel):
    title: str
    cefr_level: str = ""
    duration_weeks: int = 12
    days_per_week: int = 4
    ends_with_test: bool = True
    weekly_plan: list[WeekPlan]


class StudyPlanResponse(BaseModel):
    id: int
    user_id: int
    cefr_level: str
    goals: list[str]
    duration_weeks: int
    days_per_week: int
    current_unit: str
    progress_day: int = 0
    generated_plan: dict
    is_active: bool
    completion_test_taken: bool
    completion_test_score: float | None
    completion_test_recommendation: str | None
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("generated_plan", mode="before")
    @classmethod
    def normalize_generated_plan(cls, value: object) -> dict:
        """Keep persisted/corrupted plan JSON safe for frontend consumers."""
        if not isinstance(value, dict):
            return {"title": "", "weekly_plan": []}

        normalized = dict(value)
        weekly_plan = value.get("weekly_plan")
        if not isinstance(weekly_plan, list):
            normalized["weekly_plan"] = []
            return normalized

        safe_weeks: list[dict] = []
        for week in weekly_plan:
            if not isinstance(week, dict):
                continue
            week_number = week.get("week")
            days = week.get("days")
            if not isinstance(week_number, int) or isinstance(week_number, bool):
                continue
            if not isinstance(days, list):
                continue

            safe_days: list[dict] = []
            for day in days:
                if not isinstance(day, dict):
                    continue
                day_number = day.get("day")
                title = day.get("title")
                if not isinstance(day_number, int) or isinstance(day_number, bool):
                    continue
                if not isinstance(title, str) or not title.strip():
                    continue

                safe_day = dict(day)
                safe_day["day"] = day_number
                safe_day["title"] = title
                if not isinstance(safe_day.get("lesson_type"), str):
                    safe_day["lesson_type"] = "review"
                if not isinstance(safe_day.get("objectives"), list):
                    safe_day["objectives"] = []
                else:
                    safe_day["objectives"] = [
                        item for item in safe_day["objectives"] if isinstance(item, str)
                    ]
                minutes = safe_day.get("estimated_minutes")
                if isinstance(minutes, bool) or not isinstance(minutes, (int, float)) or minutes <= 0:
                    safe_day["estimated_minutes"] = 25
                else:
                    safe_day["estimated_minutes"] = int(minutes)
                if not isinstance(safe_day.get("unit_id"), str):
                    safe_day["unit_id"] = ""
                safe_days.append(safe_day)

            safe_week = dict(week)
            safe_week["week"] = week_number
            safe_week["days"] = safe_days
            if not isinstance(safe_week.get("theme"), str):
                safe_week["theme"] = ""
            safe_weeks.append(safe_week)

        normalized["weekly_plan"] = safe_weeks
        return normalized

    @field_serializer("created_at")
    def serialize_created_at(self, v: datetime, _info):
        return v.isoformat()


class TodayLesson(BaseModel):
    id: int | None = None
    title: str
    lesson_type: str
    week: int
    day: int
    objectives: list[str]
    estimated_minutes: int
    unit_id: str = ""
    is_completed: bool = False

    @field_validator("lesson_type", mode="before")
    @classmethod
    def normalize_lesson_type(cls, value: object) -> str:
        if not isinstance(value, str):
            return "review"
        normalized = value.strip().lower()
        return normalized if normalized in SUPPORTED_LESSON_TYPES else "review"

    @field_validator("objectives", mode="before")
    @classmethod
    def normalize_objectives(cls, value: object) -> list[str]:
        if not isinstance(value, list):
            return []
        return [item for item in value if isinstance(item, str)]

    @field_validator("estimated_minutes", mode="before")
    @classmethod
    def normalize_estimated_minutes(cls, value: object) -> int:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return 25
        minutes = int(value)
        return minutes if minutes > 0 else 25


class TodayResponse(BaseModel):
    plan_id: int
    cefr_level: str
    lessons: list[TodayLesson]
    progress_day: int = 0
    total_days: int = 0
    pending_count: int = 0
    review_due_count: int = 0


class PendingLessonResponse(BaseModel):
    id: int
    title: str
    lesson_type: str
    week_number: int
    day_number: int

    model_config = {"from_attributes": True}


class PlanLessonResponse(BaseModel):
    id: int
    title: str
    lesson_type: str
    week_number: int
    day_number: int
    unit_id: str | None
    is_completed: bool

    model_config = {"from_attributes": True}

from __future__ import annotations

from datetime import datetime
from typing import Self

from pydantic import BaseModel, field_serializer, field_validator, model_validator


class ExerciseContent(BaseModel):
    type: str
    question: str
    options: list[str] | None = None
    correct: str
    explanation: str | None = None
    native_explanation: str | None = None
    native_hint: str | None = None
    content_id: str | None = None
    variant: str | None = None
    accepted_answers: list[str] | None = None
    metadata: dict[str, str] | None = None

    @model_validator(mode="after")
    def validate_exercise_content(self) -> Self:
        if not self.question.strip():
            raise ValueError("exercises must include a question")
        if not self.correct.strip():
            raise ValueError("exercises must include a correct answer")
        if self.accepted_answers is not None:
            self.accepted_answers = [
                answer.strip() for answer in self.accepted_answers if answer.strip()
            ]
            if self.correct not in self.accepted_answers:
                self.accepted_answers.insert(0, self.correct)
        if self.type == "fill_blank" and "___" not in self.question:
            if self.explanation and "___" in self.explanation:
                self.question, self.explanation = self.explanation, self.question
            else:
                raise ValueError("fill_blank exercises must include ___ in the question")
        if self.type != "multiple_choice":
            return self
        options = [option for option in (self.options or []) if option.strip()]
        if len(options) < 2:
            raise ValueError("multiple_choice exercises must include at least two options")
        if self.correct not in options:
            raise ValueError("multiple_choice correct answer must match one option exactly")
        self.options = options
        return self


class LessonVocabularyItem(BaseModel):
    word: str
    definition: str
    example: str
    translation: str | None = None
    example_translation: str | None = None
    note: str | None = None
    reading: str | None = None


class LessonContent(BaseModel):
    lesson_type: str
    title: str
    cefr_level: str
    explanation: dict
    native_explanation: dict | None = None
    exercises: list[ExerciseContent]
    vocabulary: list[LessonVocabularyItem] | None = None
    grammar_refs: list[str] = []
    unit_id: str | None = None


class LessonResponse(BaseModel):
    id: int
    study_plan_id: int
    title: str
    lesson_type: str
    cefr_level: str
    week_number: int
    day_number: int
    content: dict
    is_completed: bool
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}

    @field_serializer("completed_at")
    def serialize_completed_at(self, v: datetime | None, _info):
        return v.isoformat() if v else None


class ExerciseResponse(BaseModel):
    id: int
    lesson_id: int
    exercise_type: str
    question: str
    options: list | None = None
    correct_answer: str
    user_answer: str | None = None
    score: float | None = None
    feedback: str | None = None
    explanation: str | None = None
    native_explanation: str | None = None
    native_hint: str | None = None
    content_id: str | None = None
    variant: str | None = None
    accepted_answers: list[str] | None = None
    metadata: dict[str, str] | None = None
    answered_at: datetime | None = None
    mastery_score: float = 0.0
    mastery_state: str = "unseen"
    mastery_variants: int = 0

    model_config = {"from_attributes": True}

    @field_serializer("answered_at")
    def serialize_answered_at(self, v: datetime | None, _info):
        return v.isoformat() if v else None


class LessonDetailResponse(BaseModel):
    lesson: LessonResponse
    exercises: list[ExerciseResponse]


class ExerciseAnswerRequest(BaseModel):
    answer: str

    @field_validator("answer")
    @classmethod
    def validate_answer(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("answer must not be empty")
        if len(value) > 5000:
            raise ValueError("answer is too long")
        return value


class ExerciseAttemptResponse(BaseModel):
    id: int
    exercise_id: int
    lesson_id: int
    content_id: str | None = None
    variant: str | None = None
    attempt_number: int
    user_answer: str
    score: float
    feedback: str
    answered_at: datetime

    model_config = {"from_attributes": True}

    @field_serializer("answered_at")
    def serialize_answered_at(self, v: datetime, _info):
        return v.isoformat()


class ExerciseAttemptSummaryResponse(BaseModel):
    exercise_id: int
    attempts: int
    best_score: float
    latest_score: float
    first_score: float
    improvement: float
    mastered: bool
    needs_retry: bool
    mastery_score: float = 0.0
    mastery_state: str = "unseen"
    mastery_variants: int = 0
    latest_variant: str | None = None
    recommended_action: str = "reinforce"
    recommended_variant: str | None = None
    latest_answered_at: datetime


class LessonMasteryResponse(BaseModel):
    total_exercises: int
    attempted_exercises: int
    mastered_exercises: int
    learning_exercises: int
    struggling_exercises: int
    unseen_exercises: int
    average_mastery_score: float
    attempt_rate: float
    mastery_rate: float
    covered_variants: int


class AdaptiveNextResponse(BaseModel):
    action: str
    recommended_variant: str | None = None
    exercise: ExerciseResponse


class ExerciseAnswerResponse(BaseModel):
    id: int
    score: float
    feedback: str
    correct_answer: str
    attempt_id: int | None = None
    attempt_number: int = 1
    content_id: str | None = None
    variant: str | None = None
    attempts_count: int = 1
    score_delta: float = 0.0
    mastered: bool = False
    mastery_score: float = 0.0
    mastery_state: str = "unseen"
    mastery_variants: int = 0
    recommended_action: str = "reinforce"
    recommended_variant: str | None = None


class FreeWriteEvaluation(BaseModel):
    score: float
    feedback: str
    corrections: list[dict]


class FillBlankEvaluation(BaseModel):
    is_correct: bool
    score: float
    feedback: str


class PronunciationEvaluation(BaseModel):
    score: float
    feedback: str
    is_correct: bool


class NativeExplanationResponse(BaseModel):
    text: str
    key_points: list[str]
    examples: list[dict]
    common_traps: list[dict] | None = None
    mini_glossary: list[dict] | None = None


class NativeExerciseExplanationResponse(BaseModel):
    native_explanation: str


class NativeExerciseHintResponse(BaseModel):
    native_hint: str

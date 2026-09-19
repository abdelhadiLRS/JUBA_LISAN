from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class GameProgress(Base):
    __tablename__ = "game_progress"

    __table_args__ = (
        UniqueConstraint("user_id", "study_plan_id", name="uq_game_progress_user_plan"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    study_plan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("study_plans.id", ondelete="CASCADE"), nullable=False, index=True
    )
    games_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    questions_answered: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    correct_answers: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    best_round_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    daily_challenges_completed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_daily_challenge_date: Mapped[str] = mapped_column(String(10), nullable=False, default="")
    current_correct_streak: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    best_correct_streak: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    achievements: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )

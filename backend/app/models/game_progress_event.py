from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class GameProgressEvent(Base):
    __tablename__ = "game_progress_events"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "study_plan_id",
            "event_id",
            name="uq_game_progress_event_user_plan_event",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(String(36), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    study_plan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("study_plans.id", ondelete="CASCADE"), nullable=False, index=True
    )
    game_id: Mapped[str] = mapped_column(String(32), nullable=False)
    questions_answered: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_answers: Mapped[int] = mapped_column(Integer, nullable=False)
    round_score: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_challenge: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    daily_challenge_date: Mapped[str] = mapped_column(String(10), nullable=False, default="")
    achievements: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    xp_earned: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )

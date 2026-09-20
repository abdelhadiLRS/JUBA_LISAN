from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class GameSession(Base):
    __tablename__ = "game_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    study_plan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("study_plans.id", ondelete="CASCADE"), nullable=False, index=True
    )
    game_id: Mapped[str] = mapped_column(String(32), nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    questions: Mapped[list] = mapped_column(JSON, nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # Server-owned daily slot captured when the session is issued.
    daily_challenge_date: Mapped[str] = mapped_column(String(10), nullable=False, default="")
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

from __future__ import annotations

from datetime import UTC, date, datetime

from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LeagueSeason(Base):
    __tablename__ = "league_seasons"
    __table_args__ = (
        UniqueConstraint("target_language", "week_start", name="uq_league_language_week"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    target_language: Mapped[str] = mapped_column(String(10), nullable=False)
    week_start: Mapped[date] = mapped_column(Date, nullable=False)
    finalized: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class LeagueMembership(Base):
    __tablename__ = "league_memberships"
    __table_args__ = (
        UniqueConstraint("season_id", "user_id", name="uq_league_season_user"),
        CheckConstraint("tier >= 0 AND tier <= 5", name="ck_league_tier"),
        CheckConstraint("next_tier IS NULL OR (next_tier >= 0 AND next_tier <= 5)", name="ck_league_next_tier"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("league_seasons.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tier: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    final_xp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    final_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    next_tier: Mapped[int | None] = mapped_column(Integer, nullable=True)

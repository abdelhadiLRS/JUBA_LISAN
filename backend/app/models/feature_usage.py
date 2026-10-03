from __future__ import annotations
from datetime import datetime
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class FeatureUsage(Base):
    __tablename__ = "feature_usage"
    __table_args__ = (
        UniqueConstraint("user_id", "feature", "period_start", name="uq_feature_usage_period"),
        CheckConstraint("used >= 0 AND reserved >= 0", name="ck_feature_usage_nonnegative"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    feature: Mapped[str] = mapped_column(String(24), nullable=False)
    period_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    reserved: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")


class FeatureReservation(Base):
    __tablename__ = "feature_reservations"
    __table_args__ = (CheckConstraint("amount > 0", name="ck_feature_reservation_amount"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    usage_id: Mapped[int] = mapped_column(ForeignKey("feature_usage.id", ondelete="CASCADE"), nullable=False, index=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    state: Mapped[str] = mapped_column(String(12), nullable=False, default="pending")
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

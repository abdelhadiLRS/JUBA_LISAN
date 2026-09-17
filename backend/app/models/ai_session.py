"""AI Tutor Session and Speech Analysis Models"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SessionStatus(str, Enum):
    """Status of an AI tutoring session"""
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SpeechQuality(str, Enum):
    """Quality rating for speech analysis"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    NEEDS_IMPROVEMENT = "needs_improvement"


class AISession(Base):
    """AI Tutoring Session tracking"""
    __tablename__ = "ai_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    language: Mapped[str] = mapped_column(String(10), nullable=False)  # e.g., 'en', 'de', 'fr'
    topic: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[SessionStatus] = mapped_column(
        SQLEnum(SessionStatus), nullable=False, default=SessionStatus.ACTIVE
    )
    total_messages: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)  # Overall session score
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )

    # Relationships
    user = relationship("User", back_populates="ai_sessions")
    speech_analyses = relationship("SpeechAnalysis", back_populates="session", cascade="all, delete-orphan")


class SpeechAnalysis(Base):
    """Individual speech analysis records"""
    __tablename__ = "speech_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ai_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    audio_url: Mapped[str | None] = mapped_column(Text, nullable=True)  # S3 or local storage
    transcription: Mapped[str | None] = mapped_column(Text, nullable=True)
    expected_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    pronunciation_score: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0-100
    fluency_score: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0-100
    accuracy_score: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0-100
    overall_quality: Mapped[SpeechQuality | None] = mapped_column(
        SQLEnum(SpeechQuality), nullable=True
    )
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    phoneme_errors: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON array string
    analyzed_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )

    # Relationships
    session = relationship("AISession", back_populates="speech_analyses")

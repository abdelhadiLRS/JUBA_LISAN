"""Legacy AI tutor endpoints with account-wide chat generation accounting."""
from __future__ import annotations
import json
from datetime import UTC, datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user, require_learner
from app.models.ai_session import AISession, SpeechAnalysis, SessionStatus, SpeechQuality
from app.models.user import User
from app.services.feature_quota_service import feature_quota
from app.services.openai_service import OpenAIService
from app.services.speech_service import SpeechService

router = APIRouter(prefix="/api/ai", tags=["AI Tutor"], dependencies=[Depends(require_learner)])


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    language: str = Field(..., pattern="^[a-z]{2}(-[A-Z]{2})?$")
    topic: str | None = Field(None, max_length=255)


class ChatResponse(BaseModel):
    response: str
    session_id: int
    message_count: int
    suggested_topic: str | None = None


class SpeechAnalysisRequest(BaseModel):
    audio_base64: str = Field(..., description="Base64 encoded audio data")
    expected_text: str = Field(..., max_length=500)
    language: str = Field(..., pattern="^[a-z]{2}(-[A-Z]{2})?$")


class SpeechAnalysisResponse(BaseModel):
    transcription: str | None
    pronunciation_score: float | None
    fluency_score: float | None
    accuracy_score: float | None
    overall_quality: str | None
    feedback: str | None
    phoneme_errors: list[str] | None = None


class SessionHistory(BaseModel):
    id: int
    language: str
    topic: str | None
    status: str
    total_messages: int
    duration_seconds: int
    score: float | None
    started_at: datetime
    ended_at: datetime | None


@router.post("/tutor/chat", response_model=ChatResponse)
async def chat_with_tutor(request: ChatMessage, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> ChatResponse:
    if not request.message.strip():
        raise HTTPException(status_code=422, detail="Message must not be empty")
    async with feature_quota(current_user, "chat"):
        try:
            session = (await db.execute(select(AISession).where(AISession.user_id == current_user.id, AISession.language == request.language,
                AISession.topic == request.topic, AISession.status == SessionStatus.ACTIVE))).scalar_one_or_none() if request.topic else None
            if session is None:
                session = AISession(user_id=current_user.id, language=request.language, topic=request.topic, status=SessionStatus.ACTIVE, total_messages=0, duration_seconds=0)
                db.add(session)
                await db.flush()
            response = await OpenAIService().get_tutor_response(message=request.message, language=request.language, topic=request.topic,
                                                                conversation_history=[], user_level="intermediate")
            if not str(response.get("response", "")).strip():
                raise ValueError("Empty tutor response")
            session.total_messages += 1
            await db.commit()
            result = ChatResponse(response=response["response"], session_id=session.id, message_count=session.total_messages, suggested_topic=response.get("suggested_topic"))
        except HTTPException:
            raise
        except Exception as exc:
            await db.rollback()
            raise HTTPException(status_code=503, detail="The tutor is temporarily unavailable") from exc
    return result


@router.post("/speech/analyze", response_model=SpeechAnalysisResponse)
async def analyze_speech(request: SpeechAnalysisRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> SpeechAnalysisResponse:
    try:
        service = SpeechService()
        transcription = (await service.transcribe_audio(audio_base64=request.audio_base64, language=request.language)).get("transcription", "")
        analysis = await service.analyze_pronunciation(transcription=transcription, expected_text=request.expected_text, language=request.language)
        score = analysis.get("overall_score", 0)
        quality = SpeechQuality.EXCELLENT if score >= 90 else SpeechQuality.GOOD if score >= 75 else SpeechQuality.FAIR if score >= 60 else SpeechQuality.NEEDS_IMPROVEMENT
        record = SpeechAnalysis(session_id=None, transcription=transcription, expected_text=request.expected_text,
            pronunciation_score=analysis.get("pronunciation_score"), fluency_score=analysis.get("fluency_score"), accuracy_score=analysis.get("accuracy_score"),
            overall_quality=quality, feedback=analysis.get("feedback"), phoneme_errors=json.dumps(analysis.get("phoneme_errors", [])))
        db.add(record)
        await db.commit()
        return SpeechAnalysisResponse(transcription=transcription, pronunciation_score=analysis.get("pronunciation_score"),
            fluency_score=analysis.get("fluency_score"), accuracy_score=analysis.get("accuracy_score"), overall_quality=quality.value,
            feedback=analysis.get("feedback"), phoneme_errors=analysis.get("phoneme_errors"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Speech analysis is temporarily unavailable") from exc


@router.get("/sessions", response_model=list[SessionHistory])
async def get_user_sessions(limit: int = 20, offset: int = 0, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> list[SessionHistory]:
    rows = (await db.execute(select(AISession).where(AISession.user_id == current_user.id).order_by(desc(AISession.started_at)).offset(max(0, offset)).limit(max(1, min(limit, 100))))).scalars().all()
    return [SessionHistory(id=item.id, language=item.language, topic=item.topic, status=item.status.value, total_messages=item.total_messages,
        duration_seconds=item.duration_seconds, score=item.score, started_at=item.started_at, ended_at=item.ended_at) for item in rows]


@router.post("/sessions/{session_id}/end")
async def end_session(session_id: int, score: float | None = None, feedback: str | None = None,
                      current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    session = (await db.execute(select(AISession).where(AISession.id == session_id, AISession.user_id == current_user.id))).scalar_one_or_none()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    session.status, session.ended_at = SessionStatus.COMPLETED, datetime.now(UTC).replace(tzinfo=None)
    if score is not None:
        session.score = score
    if feedback:
        session.feedback = feedback
    await db.commit()
    return {"message": "Session ended successfully", "session_id": session_id}

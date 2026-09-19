"""AI Tutor and Speech Analysis API Router"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.ai_session import AISession, SpeechAnalysis, SessionStatus, SpeechQuality
from app.models.user import User
from app.services.openai_service import OpenAIService
from app.services.speech_service import SpeechService

router = APIRouter(prefix="/api/ai", tags=["AI Tutor"])


class ChatMessage(BaseModel):
    """Chat message request"""
    message: str = Field(..., min_length=1, max_length=2000)
    language: str = Field(..., pattern="^[a-z]{2}(-[A-Z]{2})?$")  # e.g., 'en', 'de', 'fr'
    topic: str | None = Field(None, max_length=255)


class ChatResponse(BaseModel):
    """Chat message response"""
    response: str
    session_id: int
    message_count: int
    suggested_topic: str | None = None


class SpeechAnalysisRequest(BaseModel):
    """Speech analysis request"""
    audio_base64: str = Field(..., description="Base64 encoded audio data")
    expected_text: str = Field(..., max_length=500)
    language: str = Field(..., pattern="^[a-z]{2}(-[A-Z]{2})?$")


class SpeechAnalysisResponse(BaseModel):
    """Speech analysis response"""
    transcription: str | None
    pronunciation_score: float | None
    fluency_score: float | None
    accuracy_score: float | None
    overall_quality: str | None
    feedback: str | None
    phoneme_errors: list[str] | None = None


class SessionHistory(BaseModel):
    """Session history response"""
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
async def chat_with_tutor(
    request: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """
    Chat with AI language tutor.
    
    This endpoint creates or continues an AI tutoring session,
    sends the message to OpenAI, and returns the response.
    """
    try:
        # Find active session for this language and topic
        active_session = None
        if request.topic:
            # Try to find session with same topic
            from sqlalchemy import select
            stmt = select(AISession).where(
                AISession.user_id == current_user.id,
                AISession.language == request.language,
                AISession.topic == request.topic,
                AISession.status == SessionStatus.ACTIVE
            )
            result = await db.execute(stmt)
            active_session = result.scalar_one_or_none()
        
        # If no session found, create a new one
        if not active_session:
            active_session = AISession(
                user_id=current_user.id,
                language=request.language,
                topic=request.topic,
                status=SessionStatus.ACTIVE,
                total_messages=0,
                duration_seconds=0
            )
            db.add(active_session)
            await db.commit()
            await db.refresh(active_session)
        
        # Initialize OpenAI service
        openai_service = OpenAIService()
        
        # Get conversation history (last 10 messages for context)
        # In production, you'd store conversation history in DB or Redis
        conversation_history = []  # Placeholder
        
        # Call OpenAI API
        ai_response = await openai_service.get_tutor_response(
            message=request.message,
            language=request.language,
            topic=request.topic,
            conversation_history=conversation_history,
            user_level="intermediate"  # Could be fetched from user profile
        )
        
        # Update session
        active_session.total_messages += 1
        await db.commit()
        
        return ChatResponse(
            response=ai_response["response"],
            session_id=active_session.id,
            message_count=active_session.total_messages,
            suggested_topic=ai_response.get("suggested_topic")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI tutor error: {str(e)}"
        )


@router.post("/speech/analyze", response_model=SpeechAnalysisResponse)
async def analyze_speech(
    request: SpeechAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SpeechAnalysisResponse:
    """
    Analyze speech pronunciation and fluency.
    
    This endpoint sends audio to Google Cloud Speech-to-Text,
    compares it with expected text, and provides feedback.
    """
    try:
        # Initialize speech service
        speech_service = SpeechService()
        
        # Transcribe audio using Google Cloud Speech
        transcription_result = await speech_service.transcribe_audio(
            audio_base64=request.audio_base64,
            language=request.language
        )
        
        transcription = transcription_result.get("transcription", "")
        
        # Analyze pronunciation and fluency
        analysis = await speech_service.analyze_pronunciation(
            transcription=transcription,
            expected_text=request.expected_text,
            language=request.language
        )
        
        # Determine overall quality
        overall_score = analysis.get("overall_score", 0)
        if overall_score >= 90:
            quality = SpeechQuality.EXCELLENT
        elif overall_score >= 75:
            quality = SpeechQuality.GOOD
        elif overall_score >= 60:
            quality = SpeechQuality.FAIR
        else:
            quality = SpeechQuality.NEEDS_IMPROVEMENT
        
        # Create speech analysis record
        speech_analysis = SpeechAnalysis(
            session_id=None,  # Can be linked to a session if needed
            transcription=transcription,
            expected_text=request.expected_text,
            pronunciation_score=analysis.get("pronunciation_score"),
            fluency_score=analysis.get("fluency_score"),
            accuracy_score=analysis.get("accuracy_score"),
            overall_quality=quality,
            feedback=analysis.get("feedback"),
            phoneme_errors=json.dumps(analysis.get("phoneme_errors", []))
        )
        db.add(speech_analysis)
        await db.commit()
        await db.refresh(speech_analysis)
        
        return SpeechAnalysisResponse(
            transcription=transcription,
            pronunciation_score=analysis.get("pronunciation_score"),
            fluency_score=analysis.get("fluency_score"),
            accuracy_score=analysis.get("accuracy_score"),
            overall_quality=quality.value if quality else None,
            feedback=analysis.get("feedback"),
            phoneme_errors=analysis.get("phoneme_errors")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Speech analysis error: {str(e)}"
        )


@router.get("/sessions", response_model=list[SessionHistory])
async def get_user_sessions(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[SessionHistory]:
    """Get user's AI tutoring session history"""
    try:
        from sqlalchemy import select, desc
        
        stmt = (
            select(AISession)
            .where(AISession.user_id == current_user.id)
            .order_by(desc(AISession.started_at))
            .offset(offset)
            .limit(limit)
        )
        
        result = await db.execute(stmt)
        sessions = result.scalars().all()
        
        return [
            SessionHistory(
                id=session.id,
                language=session.language,
                topic=session.topic,
                status=session.status.value,
                total_messages=session.total_messages,
                duration_seconds=session.duration_seconds,
                score=session.score,
                started_at=session.started_at,
                ended_at=session.ended_at
            )
            for session in sessions
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching sessions: {str(e)}"
        )


@router.post("/sessions/{session_id}/end")
async def end_session(
    session_id: int,
    score: float | None = None,
    feedback: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """End an AI tutoring session"""
    try:
        from sqlalchemy import select
        
        stmt = select(AISession).where(
            AISession.id == session_id,
            AISession.user_id == current_user.id
        )
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        session.status = SessionStatus.COMPLETED
        session.ended_at = datetime.now(UTC).replace(tzinfo=None)
        if score is not None:
            session.score = score
        if feedback:
            session.feedback = feedback
        
        await db.commit()
        
        return {"message": "Session ended successfully", "session_id": session_id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ending session: {str(e)}"
        )

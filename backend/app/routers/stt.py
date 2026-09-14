from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
import httpx
import openai

from app.core.app_logger import get_logger
from app.core.deps import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.schemas.tts_stt import STTResponse

router = APIRouter(prefix="/api", tags=["stt"])
logger = get_logger(__name__)


@router.post("/stt", response_model=STTResponse)
@limiter.limit("20/minute")
async def speech_to_text(
    request: Request,
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
) -> STTResponse:
    """Proxy STT request to Whisper service. Returns transcribed text."""
    stt_service = getattr(request.app.state, "stt_service", None)
    if stt_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="STT service is not enabled",
        )
    audio_bytes = await audio.read()
    if len(audio_bytes) > 50 * 1024 * 1024:  # 50 MB
        raise HTTPException(status_code=413, detail="Audio file too large (max 50 MB)")
    try:
        text = await stt_service.transcribe(
            audio_bytes,
            audio.filename or "audio.webm",
            mime_type=audio.content_type or "audio/webm",
        )
    except (httpx.HTTPError, openai.APIError) as exc:
        logger.warning(
            "stt_unavailable",
            user_id=current_user.id,
            provider=type(stt_service).__name__,
            error=str(exc),
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="STT service is temporarily unavailable",
        ) from None
    return STTResponse(text=text)

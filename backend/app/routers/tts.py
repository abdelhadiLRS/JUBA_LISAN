import asyncio
import os
import time
import uuid
import httpx
import openai
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.app_logger import get_logger
from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_user, require_learner
from app.core.limiter import limiter
from app.models.user import User
from app.schemas.tts_stt import TTSRequest
from app.services.audio_duration import audio_seconds
from app.services.feature_quota_service import feature_quota, quota_status
from app.services.prompts.common import TUTOR_DISPLAY_NAME

router = APIRouter(prefix="/api", tags=["tts"], dependencies=[Depends(require_learner)])
logger = get_logger(__name__)
_PREVIEW_DIR = "/app/tts_previews"
_OPENAI_VOICES = frozenset({"alloy", "ash", "coral", "echo", "fable", "nova", "onyx", "sage", "shimmer"})
_PREVIEW_TEXT = f"Hello! I'm {TUTOR_DISPLAY_NAME}, your tutor. This is how I sound, warm, clear, and ready to help you practise every day. Let's get started!"


@router.post("/tts")
@limiter.limit("20/minute")
async def text_to_speech(request: Request, body: TTSRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Response:
    start = time.perf_counter()
    trace = request.headers.get("X-TTS-Trace-ID") or f"tts-{uuid.uuid4().hex[:12]}"
    service = getattr(request.app.state, "tts_service", None)
    if service is None:
        raise HTTPException(status_code=503, detail="TTS service is not enabled")
    if not body.text.strip():
        raise HTTPException(status_code=422, detail="Text must not be empty")
    amount = 1
    if settings.STRIPE_ENABLED:
        state = await quota_status(db, current_user)
        amount = state["features"]["tts"]["remaining"]
        if amount <= 0:
            raise HTTPException(status_code=402, detail={"reason": "quota_exhausted", "feature": "tts", **state["features"]["tts"]})
    synth_start = time.perf_counter()
    async with feature_quota(current_user, "tts", amount) as quota:
        try:
            voice = body.voice if settings.TTS_PROVIDER != "local" else None
            audio = await asyncio.wait_for(service.synthesize(body.text, voice), timeout=600)
        except (httpx.HTTPError, openai.APIError, TimeoutError) as exc:
            logger.warning("tts_unavailable", trace=trace, user_id=current_user.id, error=str(exc))
            raise HTTPException(status_code=503, detail="TTS service is temporarily unavailable") from None
        if settings.STRIPE_ENABLED:
            try:
                duration = audio_seconds(audio)
            except Exception as exc:
                raise HTTPException(status_code=502, detail="Could not measure synthesized audio duration") from exc
            if duration > amount:
                raise HTTPException(status_code=402, detail="Generated audio exceeds remaining pronunciation allowance; use shorter text")
            quota.charge(duration)
        elif not audio:
            raise HTTPException(status_code=502, detail="TTS returned no audio")
    synth_ms, total_ms = (time.perf_counter() - synth_start) * 1000, (time.perf_counter() - start) * 1000
    logger.info("tts", trace=trace, user_id=current_user.id, text_len=len(body.text), audio_bytes=len(audio), synth_ms=round(synth_ms, 1), total_ms=round(total_ms, 1))
    return Response(content=audio, media_type="audio/mpeg", headers={"X-TTS-Trace-ID": trace,
        "X-TTS-Backend-Synth-Ms": f"{synth_ms:.1f}", "X-TTS-Backend-Total-Ms": f"{total_ms:.1f}"})


@router.get("/tts/preview/{voice}")
@limiter.limit("60/minute")
async def voice_preview(request: Request, voice: str, current_user: User = Depends(get_current_user)) -> FileResponse:
    if settings.TTS_PROVIDER != "openai":
        raise HTTPException(status_code=404, detail="Voice preview is only available with OpenAI TTS")
    if voice not in _OPENAI_VOICES:
        raise HTTPException(status_code=400, detail="Invalid voice name")
    service = getattr(request.app.state, "tts_service", None)
    if service is None:
        raise HTTPException(status_code=503, detail="TTS service is not enabled")
    path = os.path.join(_PREVIEW_DIR, f"{voice}.mp3")
    if not os.path.exists(path):
        os.makedirs(_PREVIEW_DIR, exist_ok=True)
        try:
            audio = await service.synthesize(_PREVIEW_TEXT, voice)
        except (httpx.HTTPError, openai.APIError) as exc:
            logger.warning("tts_preview_unavailable", voice=voice, error=str(exc))
            raise HTTPException(status_code=503, detail="TTS service is temporarily unavailable") from None
        temporary = path + f".{uuid.uuid4().hex}.tmp"
        with open(temporary, "wb") as output:
            output.write(audio)
        os.replace(temporary, path)
    return FileResponse(path, media_type="audio/mpeg")

import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from alembic.config import Config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from alembic import command

from app.core.config import settings
from app.core.limiter import limiter

logging.basicConfig(level=settings.LOG_LEVEL.upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
_APP_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
_DATA_DIR = Path(settings.DATA_DIR or (Path.home() / "JUBA_LISAN"))
_AVATARS_DIR = _DATA_DIR / "avatars"
_TTS_PREVIEWS_DIR = _DATA_DIR / "tts_previews"


def _run_migrations() -> None:
    cfg = Config(str(_APP_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(_APP_DIR / "alembic"))
    command.upgrade(cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.SECRET_KEY or "CHANGE_ME" in settings.SECRET_KEY or len(settings.SECRET_KEY) < 32:
        raise RuntimeError("SECRET_KEY is insecure or unconfigured. Set a random value of at least 32 characters in your .env file.")
    await asyncio.to_thread(_run_migrations)
    _AVATARS_DIR.mkdir(parents=True, exist_ok=True)
    _TTS_PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    if settings.TTS_PROVIDER == "openai":
        if not settings.OPENAI_API_KEY:
            raise ValueError("TTS_PROVIDER=openai requires OPENAI_API_KEY to be set")
        from app.services.tts_service import OpenAITTSService
        app.state.tts_service = OpenAITTSService(api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_TTS_MODEL, voice=settings.OPENAI_TTS_VOICE, speed=settings.OPENAI_TTS_SPEED)
    else:
        from app.services.tts_service import KokoroTTSService
        app.state.tts_service = KokoroTTSService(settings.TTS_BASE_URL, settings.TTS_VOICE)
    if settings.STT_PROVIDER == "openai":
        if not settings.OPENAI_API_KEY:
            raise ValueError("STT_PROVIDER=openai requires OPENAI_API_KEY to be set")
        from app.services.stt_service import OpenAISTTService
        app.state.stt_service = OpenAISTTService(api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_STT_MODEL)
    else:
        from app.services.stt_service import WhisperSTTService
        app.state.stt_service = WhisperSTTService(settings.STT_BASE_URL)
    yield


app = FastAPI(title="JUBA LISAN API", version="0.1.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS,
                   allow_origin_regex=r"^https?://(?:127\.0\.0\.1|localhost)(?::\d+)?$" if settings.DESKTOP_MODE else None,
                   allow_credentials=True, allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"], allow_headers=["*"])


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next) -> Response:
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-XSS-Protection"] = "0"
    if request.url.path not in {"/docs", "/redoc", "/docs/oauth2-redirect"}:
        response.headers["Content-Security-Policy"] = "default-src 'self'; object-src 'none'; base-uri 'self'"
    return response


from app.routers import (
    admin, admin_dashboard_banner, ai_tutor, assessment, auth, chat, contact,
    conversation, curriculum, dashboard_banner, feedback, flashcards, freemium,
    grammar, invites, languages, lessons, listening, memories, phrasebook, progress,
    reading, reviews, social, stt, study_plan, tts, vocabulary, translate,
)
from app.routers import config as config_router
from app.routers import health as health_router
from app.routers import community_professional as community_router
from app.routers import leagues as leagues_router
from app.routers import game_results as game_results_router
from app.routers import subscriptions as subscriptions_router

for module in (auth, admin, admin_dashboard_banner, ai_tutor, assessment, study_plan,
               lessons, flashcards, grammar, chat, progress, listening, reading,
               reviews, tts, stt, translate, conversation, config_router, contact,
               curriculum, dashboard_banner, feedback, freemium, memories,
               phrasebook, languages, invites, health_router, vocabulary, social,
               community_router, leagues_router, game_results_router, subscriptions_router):
    app.include_router(module.router)

if settings.STRIPE_ENABLED:
    import stripe as _stripe
    from app.routers import billing as billing_router
    _stripe.api_key = settings.STRIPE_SECRET_KEY
    app.include_router(billing_router.router)

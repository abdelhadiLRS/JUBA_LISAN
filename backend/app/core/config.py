import os
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DESKTOP_MODE: bool = True
    DATABASE_URL: str = ""
    DATA_DIR: str = ""
    REDIS_URL: str = ""
    REDIS_ENABLED: bool = False

    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ALLOW_REGISTRATION: bool = True
    FIRST_USER_IS_ADMIN: bool = True
    BLOCKED_EMAIL_DOMAINS: list[str] = []
    LLM_PROVIDER: str = "ollama"
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "juba-coder"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-5.4-mini"
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-4-5-haiku"
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_MODEL: str = "deepseek-v4-flash"
    TTS_PROVIDER: str = "local"
    TTS_BASE_URL: str = "http://127.0.0.1:8880"
    TTS_VOICE: str = "af_heart"
    OPENAI_TTS_MODEL: str = "tts-1"
    OPENAI_TTS_VOICE: str = "nova"
    OPENAI_TTS_SPEED: float = 1.0
    STT_PROVIDER: str = "local"
    STT_BASE_URL: str = "http://127.0.0.1:9000"
    OPENAI_STT_MODEL: str = "whisper-1"
    RATE_LIMIT_ENABLED: bool = True
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    COOKIE_SECURE: bool = False
    LOG_LEVEL: str = "INFO"

    DEFAULT_CONVERSATION_MAX_DURATION: int = 1800
    DEFAULT_CONVERSATION_INACTIVITY_TIMEOUT: int = 180
    DEFAULT_CONVERSATION_WEEKLY_SESSIONS: int = 0
    DEFAULT_CONVERSATION_DAILY_MINUTES: int = 30
    DEFAULT_CONVERSATION_WEEKLY_MINUTES: int = 90
    DEFAULT_MONTHLY_TOKENS_LIMIT: int = 1_000_000
    ASSESSMENT_VOICE_TRIAL_DURATION_SECONDS: int = 300

    FREEMIUM_CHAT_DAILY_MESSAGES: int = 5
    FREEMIUM_LESSONS_DAILY: int = 3
    FREEMIUM_LISTENING_WEEKLY: int = 3
    FREEMIUM_READING_WEEKLY: int = 3
    FREEMIUM_VOICE_WEEKLY_MINUTES: int = 5
    FREEMIUM_TRIAL_ENABLED: bool = True
    FREEMIUM_TRIAL_DAYS: int = 7

    STRIPE_ENABLED: bool = False
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_MONTHLY: str = ""
    STRIPE_PRICE_YEARLY: str = ""
    STRIPE_TRIAL_DAYS: int = 7
    STRIPE_BASE_URL: str = "http://127.0.0.1:3000"

    PRICE_MONTHLY: float = 0.0
    PRICE_YEARLY: float = 0.0
    TOTAL_PRICE_MONTHLY: float = 0.0
    TOTAL_PRICE_YEARLY: float = 0.0

    EMAIL_ENABLED: bool = False
    CONTACT_EMAIL: str = ""
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@jubalisan.com"
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    APP_BASE_URL: str = "http://127.0.0.1:3000"

    AUDIO_STORAGE_PATH: str = ""
    AVAILABLE_TARGET_LANGUAGES: list[str] = [
        "de-DE", "en-GB", "en-US", "es-ES", "fr-FR",
        "it-IT", "ja-JP", "ko-KR", "pt-PT", "zh-CN", "ar",
    ]

    @field_validator(
        "DEFAULT_CONVERSATION_WEEKLY_SESSIONS",
        "DEFAULT_CONVERSATION_DAILY_MINUTES",
        "DEFAULT_CONVERSATION_WEEKLY_MINUTES",
        "DEFAULT_MONTHLY_TOKENS_LIMIT",
    )
    @classmethod
    def validate_unlimited_quota(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Quota defaults must be greater than or equal to 0")
        return value

    @field_validator("DEFAULT_CONVERSATION_MAX_DURATION")
    @classmethod
    def validate_default_max_duration(cls, value: int) -> int:
        if value not in (900, 1800):
            raise ValueError("DEFAULT_CONVERSATION_MAX_DURATION must be 900 or 1800")
        return value

    @field_validator("DEFAULT_CONVERSATION_INACTIVITY_TIMEOUT")
    @classmethod
    def validate_default_inactivity_timeout(cls, value: int) -> int:
        if value not in (60, 180, 300):
            raise ValueError("DEFAULT_CONVERSATION_INACTIVITY_TIMEOUT must be 60, 180, or 300")
        return value

    @field_validator(
        "FREEMIUM_CHAT_DAILY_MESSAGES",
        "FREEMIUM_LESSONS_DAILY",
        "FREEMIUM_LISTENING_WEEKLY",
        "FREEMIUM_READING_WEEKLY",
        "FREEMIUM_VOICE_WEEKLY_MINUTES",
        "FREEMIUM_TRIAL_DAYS",
    )
    @classmethod
    def validate_freemium_quotas(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Freemium quota values must be >= 0")
        return value

    @field_validator("ASSESSMENT_VOICE_TRIAL_DURATION_SECONDS")
    @classmethod
    def validate_trial_duration(cls, value: int) -> int:
        if value <= 0 or value > 1800:
            raise ValueError(
                "ASSESSMENT_VOICE_TRIAL_DURATION_SECONDS must be between 1 and 1800"
            )
        return value

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()


def get_settings() -> Settings:
    return settings


def initialize_desktop_mode(data_dir: str) -> Settings:
    os.environ["DESKTOP_MODE"] = "True"
    os.environ["DATA_DIR"] = data_dir

    db_path = os.path.join(data_dir, "database", "juba_lisan.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{db_path}"

    os.environ["REDIS_ENABLED"] = "False"
    os.environ["REDIS_URL"] = ""
    os.environ["AUDIO_STORAGE_PATH"] = os.path.join(data_dir, "audio")
    os.makedirs(os.environ["AUDIO_STORAGE_PATH"], exist_ok=True)

    if not os.environ.get("SECRET_KEY"):
        import secrets
        os.environ["SECRET_KEY"] = secrets.token_urlsafe(32)

    global settings
    settings = Settings()
    return settings

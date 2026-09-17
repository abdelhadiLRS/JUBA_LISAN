import os
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


def get_database_url() -> str:
    """Get database URL based on mode (desktop or server)."""
    if settings.DATABASE_URL:
        return settings.DATABASE_URL
    
    # Default fallback for development
    if settings.DESKTOP_MODE:
        # Desktop mode: SQLite in user data directory
        data_dir = settings.DATA_DIR or os.path.join(os.path.expanduser("~"), "JUBA_LISAN")
        db_path = os.path.join(data_dir, "database", "juba_lisan.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        return f"sqlite+aiosqlite:///{db_path}"
    else:
        # Server mode: PostgreSQL default
        return "postgresql+asyncpg://user:pass@localhost/db"


engine = create_async_engine(
    get_database_url(),
    echo=False,
    connect_args={
        "timeout": 10,
        "command_timeout": 10,
    },
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

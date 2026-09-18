import os
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


def get_database_url() -> str:
    """Resolve the configured database URL, defaulting to Desktop SQLite."""
    if settings.DATABASE_URL:
        return settings.DATABASE_URL

    data_dir = settings.DATA_DIR or os.path.join(
        os.path.expanduser("~"), "JUBA_LISAN"
    )
    db_path = Path(data_dir) / "database" / "juba_lisan.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if settings.DESKTOP_MODE:
        return f"sqlite+aiosqlite:///{db_path}"

    return "postgresql+asyncpg://user:pass@localhost/db"


DATABASE_URL = get_database_url()
_is_sqlite = DATABASE_URL.startswith("sqlite")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"timeout": 10} if _is_sqlite else {"command_timeout": 10},
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

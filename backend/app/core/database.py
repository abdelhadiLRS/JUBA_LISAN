import os
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


def get_database_url() -> str:
    if settings.DATABASE_URL:
        if settings.DATABASE_URL.startswith("sqlite"):
            path = settings.DATABASE_URL.split("///", 1)[-1]
            if path:
                Path(path).parent.mkdir(parents=True, exist_ok=True)
        return settings.DATABASE_URL
    directory = settings.DATA_DIR or os.path.join(os.path.expanduser("~"), "JUBA_LISAN")
    path = Path(directory) / "database" / "juba_lisan.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite+aiosqlite:///{path}" if settings.DESKTOP_MODE else "postgresql+asyncpg://user:pass@localhost/db"


DATABASE_URL = get_database_url()
_is_sqlite = DATABASE_URL.startswith("sqlite")
engine = create_async_engine(DATABASE_URL, echo=False, connect_args={"timeout": 10} if _is_sqlite else {"command_timeout": 10})
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    from app.core.session_factory import current_session_factory
    async with current_session_factory()() as session:
        try:
            yield session
        except BaseException:
            await session.rollback()
            raise

from __future__ import annotations
from contextlib import asynccontextmanager
from app.core.session_factory import current_session_factory


@asynccontextmanager
async def db_session(session_factory=None):
    factory = session_factory or current_session_factory()
    async with factory() as session:
        try:
            yield session
        except BaseException:
            await session.rollback()
            raise

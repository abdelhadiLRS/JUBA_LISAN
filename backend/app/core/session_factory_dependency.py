"""Yield-scoped factory binding, overridable through FastAPI dependencies."""
from fastapi import Depends
from app.core.session_factory import get_session_factory, set_session_factory, reset_session_factory


async def bind_session_factory(factory=Depends(get_session_factory)):
    token = set_session_factory(factory)
    try:
        yield factory
    finally:
        reset_session_factory(token)

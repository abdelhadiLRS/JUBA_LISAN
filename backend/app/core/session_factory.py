"""Request/task-local factory for short quota transactions and background work.

Tests override get_session_factory, not just get_db. Background tasks capture this
factory rather than reusing a request session after its lifetime has ended.
"""
from contextvars import ContextVar
from app.core.database import AsyncSessionLocal

_factory = ContextVar("application_session_factory", default=None)


def current_session_factory():
    return _factory.get() or AsyncSessionLocal


def get_session_factory():
    return AsyncSessionLocal


def set_session_factory(factory):
    return _factory.set(factory)


def reset_session_factory(token):
    _factory.reset(token)

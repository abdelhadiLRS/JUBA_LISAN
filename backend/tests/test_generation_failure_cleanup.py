from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from app.routers import reading, listening


@pytest.mark.asyncio
@pytest.mark.parametrize("module", [reading,listening])
async def test_lock_is_released_even_if_quota_cleanup_raises(module,monkeypatch):
    @asynccontextmanager
    async def broken_db(*args):
        raise RuntimeError("DB unavailable")
        yield
    monkeypatch.setattr(module,"db_session",broken_db)
    monkeypatch.setattr(module,"settle",AsyncMock(side_effect=RuntimeError("cleanup unavailable")))
    release = AsyncMock()
    monkeypatch.setattr(module,"release_generation_lock",release)
    reservation = SimpleNamespace(committed=False)
    if module is reading:
        await module._background_generate("A1","en-US","lock",reservation,"token")
    else:
        await module._background_generate("A1","en-US",object(),"/unused","lock","",reservation,"token")
    release.assert_awaited_once_with("lock","token")

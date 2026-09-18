import pytest

from app.routers.auth import (
    _DESKTOP_REFRESH_TOKENS,
    _consume_refresh_token,
    _delete_refresh_token,
    _store_refresh_token,
)


@pytest.mark.asyncio
async def test_desktop_refresh_tokens_are_single_use():
    token = "desktop-test-token"
    _DESKTOP_REFRESH_TOKENS.clear()

    await _store_refresh_token(None, token, 42, 3600)
    assert await _consume_refresh_token(None, token) == 42
    assert await _consume_refresh_token(None, token) is None


@pytest.mark.asyncio
async def test_desktop_refresh_token_can_be_deleted():
    token = "desktop-delete-token"
    _DESKTOP_REFRESH_TOKENS.clear()

    await _store_refresh_token(None, token, 7, 3600)
    await _delete_refresh_token(None, token)

    assert await _consume_refresh_token(None, token) is None

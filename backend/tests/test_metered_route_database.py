from unittest.mock import AsyncMock
import pytest
from app.core.config import settings


@pytest.mark.asyncio
async def test_real_translation_route_uses_injected_quota_database(client, test_user, monkeypatch):
    from app.routers.translate import llm_adapter
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr(llm_adapter, "chat", AsyncMock(return_value="Bonjour"))
    user, headers = test_user
    for _ in range(5):
        response = await client.post("/api/translate", headers=headers, json={"text":"Hello", "source":"en", "target":"fr"})
        assert response.status_code == 200
    response = await client.post("/api/translate", headers=headers, json={"text":"Hello", "source":"en", "target":"fr"})
    assert response.status_code == 402
    status = await client.get("/api/subscriptions/me", headers=headers)
    assert status.status_code == 200
    assert status.json()["features"]["translation"]["used"] == 5


@pytest.mark.asyncio
async def test_translation_failure_does_not_consume_and_input_cap_matches(client, test_user, monkeypatch):
    from app.routers.translate import llm_adapter
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr(llm_adapter, "chat", AsyncMock(side_effect=RuntimeError("provider error")))
    headers = test_user[1]
    response = await client.post("/api/translate", headers=headers, json={"text":"Hello", "source":"en", "target":"fr"})
    assert response.status_code == 502
    status = (await client.get("/api/subscriptions/me",headers=headers)).json()
    assert status["features"]["translation"]["used"] == 0
    assert status["features"]["translation"]["reserved"] == 0
    assert (await client.post("/api/translate",headers=headers,json={"text":"a"*1001,"source":"en","target":"fr"})).status_code == 422
    assert (await client.post("/api/translate",json={"text":"Hello","source":"en","target":"fr"})).status_code == 401

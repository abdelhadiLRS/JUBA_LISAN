from unittest.mock import AsyncMock
import pytest
from app.services.voice_quota_delivery import VoiceDelivery


@pytest.mark.asyncio
async def test_requires_user_assistant_audio_and_completion():
    socket = AsyncMock()
    delivery = VoiceDelivery(socket)
    await delivery.send_json({"type": "transcript", "role": "assistant", "text": "Hello", "final": True, "turn_id": 1})
    await delivery.send_bytes(b"greeting")
    await delivery.send_json({"type": "turn_complete", "turn_id": 1})
    assert not delivery.successful_turns
    await delivery.send_json({"type": "transcript", "role": "user", "text": "Hi", "final": True, "turn_id": 2})
    await delivery.send_bytes(b"audio")
    await delivery.send_json({"type": "transcript", "role": "assistant", "text": "Good job", "final": True, "turn_id": 2})
    await delivery.send_json({"type": "turn_complete", "turn_id": 2})
    assert delivery.successful_turns == {2}


@pytest.mark.asyncio
async def test_empty_text_or_text_only_does_not_charge():
    delivery = VoiceDelivery(AsyncMock())
    await delivery.send_json({"type": "transcript", "role": "user", "text": "Hi", "final": True, "turn_id": 3})
    await delivery.send_json({"type": "turn_complete", "turn_id": 3})
    assert not delivery.successful_turns
    await delivery.send_json({"type": "transcript", "role": "assistant", "text": "Hello", "final": True, "turn_id": 3})
    await delivery.send_json({"type": "turn_complete", "turn_id": 3})
    assert not delivery.successful_turns

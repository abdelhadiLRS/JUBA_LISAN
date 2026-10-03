import io
import wave
import pytest
from app.services.audio_duration import audio_seconds


def test_wav_measured_seconds_round_up():
    data = io.BytesIO()
    with wave.open(data, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(16000)
        audio.writeframes(b"\0" * 40000)
    assert audio_seconds(data.getvalue()) == 2


def test_empty_audio_not_successful_usage():
    with pytest.raises(ValueError):
        audio_seconds(b"")

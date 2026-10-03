"""Measure generated audio, not an estimate based on input characters."""
import io
import math
import wave


def audio_seconds(audio: bytes) -> int:
    if not audio:
        raise ValueError("Empty synthesized audio")
    try:
        with wave.open(io.BytesIO(audio), "rb") as wav:
            duration = wav.getnframes() / wav.getframerate()
    except (wave.Error, EOFError):
        from mutagen.mp3 import MP3
        duration = MP3(io.BytesIO(audio)).info.length
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("Invalid synthesized audio duration")
    return math.ceil(duration)

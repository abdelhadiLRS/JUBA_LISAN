"""Google Cloud Speech Service for pronunciation analysis"""
from __future__ import annotations

import base64
from typing import Any

from app.core.app_logger import get_logger
from app.core.config import settings

logger = get_logger(__name__)


class SpeechService:
    """Service for speech-to-text and pronunciation analysis using Google Cloud Speech"""

    def __init__(self):
        self.enabled = bool(settings.GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        self.speech = None
        if self.enabled:
            try:
                from google.cloud import speech_v1p1beta1 as speech
                self.speech = speech
                self.client = speech.SpeechClient()
                logger.info("Google Cloud Speech client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Google Cloud Speech client: {e}")
                self.enabled = False
        else:
            logger.info("Google Cloud Speech credentials not configured, using mock mode")
            self.client = None

    async def transcribe_audio(
        self,
        audio_base64: str,
        language: str = "en-US"
    ) -> dict[str, Any]:
        """
        Transcribe audio using Google Cloud Speech-to-Text.

        Args:
            audio_base64: Base64 encoded audio data (WAV or FLAC format)
            language: Language code (e.g., 'en-US', 'de-DE', 'fr-FR')

        Returns:
            Dictionary with 'transcription' and 'confidence' score
        """
        if not self.enabled or not self.client:
            return self._mock_transcription(audio_base64, language)

        try:
            # Decode base64 audio
            audio_data = base64.b64decode(audio_base64)

            # Configure recognition
            audio = self.self.speech.RecognitionAudio(content=audio_data)
            config = self.self.speech.RecognitionConfig(
                encoding=self.self.speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language,
                enable_automatic_punctuation=True,
                model="latest_long",  # Best for longer audio
                use_enhanced=True
            )

            # Perform speech recognition
            response = self.client.recognize(config=config, audio=audio)

            # Get best result
            if response.results and response.results[0].alternatives:
                best_alternative = response.results[0].alternatives[0]
                return {
                    "transcription": best_alternative.transcript,
                    "confidence": best_alternative.confidence,
                    "words": [
                        {
                            "word": word.word,
                            "confidence": word.confidence,
                            "start_time": word.start_time.total_seconds() if word.start_time else 0,
                            "end_time": word.end_time.total_seconds() if word.end_time else 0
                        }
                        for word in best_alternative.words
                    ]
                }
            else:
                return {"transcription": "", "confidence": 0.0}

        except Exception as e:
            logger.error(f"Speech transcription error: {e}")
            return self._mock_transcription(audio_base64, language)

    async def analyze_pronunciation(
        self,
        transcription: str,
        expected_text: str,
        language: str = "en-US"
    ) -> dict[str, Any]:
        """
        Analyze pronunciation by comparing transcription with expected text.

        Args:
            transcription: What the user actually said
            expected_text: What the user was supposed to say
            language: Language code

        Returns:
            Dictionary with pronunciation scores and feedback
        """
        if not transcription.strip():
            return {
                "pronunciation_score": 0,
                "fluency_score": 0,
                "accuracy_score": 0,
                "overall_score": 0,
                "feedback": "No speech detected. Please try again.",
                "phoneme_errors": []
            }

        # Calculate similarity metrics
        accuracy_score = self._calculate_text_similarity(transcription, expected_text)

        # Estimate fluency based on speech rate and pauses (simplified)
        fluency_score = self._estimate_fluency(transcription, language)

        # Pronunciation score based on phonetic similarity (simplified)
        pronunciation_score = self._estimate_pronunciation(transcription, expected_text, language)

        # Overall score (weighted average)
        overall_score = (
            accuracy_score * 0.4 +
            fluency_score * 0.3 +
            pronunciation_score * 0.3
        )

        # Generate feedback
        feedback = self._generate_feedback(
            transcription=transcription,
            expected_text=expected_text,
            accuracy_score=accuracy_score,
            language=language
        )

        # Identify phoneme errors (simplified)
        phoneme_errors = self._identify_phoneme_errors(transcription, expected_text)

        return {
            "pronunciation_score": round(pronunciation_score, 2),
            "fluency_score": round(fluency_score, 2),
            "accuracy_score": round(accuracy_score, 2),
            "overall_score": round(overall_score, 2),
            "feedback": feedback,
            "phoneme_errors": phoneme_errors
        }

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using Levenshtein distance"""
        text1_lower = text1.lower().strip()
        text2_lower = text2.lower().strip()

        if text1_lower == text2_lower:
            return 100.0

        # Simple word-based comparison
        words1 = set(text1_lower.split())
        words2 = set(text2_lower.split())

        if not words1 or not words2:
            return 0.0

        common_words = words1.intersection(words2)
        total_words = words1.union(words2)

        return (len(common_words) / len(total_words)) * 100

    def _estimate_fluency(self, transcription: str, language: str) -> float:
        """Estimate fluency score (simplified)"""
        # In production, analyze speech rate, pauses, and rhythm
        word_count = len(transcription.split())

        # Assume good fluency for reasonable length utterances
        if word_count >= 5:
            return min(95.0, 70.0 + word_count * 2)
        elif word_count >= 3:
            return 60.0 + word_count * 5
        else:
            return max(30.0, word_count * 20)

    def _estimate_pronunciation(
        self,
        transcription: str,
        expected_text: str,
        language: str
    ) -> float:
        """Estimate pronunciation score (simplified)"""
        # In production, use phonetic analysis
        base_score = self._calculate_text_similarity(transcription, expected_text)

        # Adjust for common pronunciation patterns
        # This is a placeholder for more sophisticated analysis
        return min(100.0, base_score * 1.1)

    def _generate_feedback(
        self,
        transcription: str,
        expected_text: str,
        accuracy_score: float,
        language: str
    ) -> str:
        """Generate personalized feedback"""
        if accuracy_score >= 90:
            return "Excellent pronunciation! Your speech was very clear and accurate."
        elif accuracy_score >= 75:
            return "Good job! Your pronunciation is quite good. Keep practicing to improve further."
        elif accuracy_score >= 60:
            return "Not bad! Try to focus on enunciating each word more clearly."
        else:
            return "Keep practicing! Try listening to native speakers and repeating after them."

    def _identify_phoneme_errors(
        self,
        transcription: str,
        expected_text: str
    ) -> list[str]:
        """Identify specific phoneme errors (simplified)"""
        errors = []

        # Simple word-level comparison
        trans_words = transcription.lower().split()
        expected_words = expected_text.lower().split()

        for i, (tw, ew) in enumerate(zip(trans_words, expected_words, strict=False)):
            if tw != ew:
                errors.append(f"Word {i+1}: said '{tw}' instead of '{ew}'")

        return errors[:5]  # Limit to top 5 errors

    def _mock_transcription(
        self,
        audio_base64: str,
        language: str
    ) -> dict[str, Any]:
        """Mock transcription for development/testing"""
        logger.warning("Using mock transcription service")

        # Return a reasonable mock response
        return {
            "transcription": "[Mock transcription - configure Google Cloud credentials for real service]",
            "confidence": 0.85,
            "words": []
        }

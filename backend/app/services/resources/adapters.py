"""
Resource adapters for external educational sources.

Each adapter implements a common interface for:
- Fetching data from the external source
- Handling errors gracefully
- Caching responses
- Normalizing data to internal schema

Adapters:
- TatoebaAdapter: Real sentences with translations
- CEFRLexAdapter: CEFR-level vocabulary
- MerlinAdapter: Learner texts with error analysis
- CommonVoiceAdapter: Audio clips for listening practice
"""

import hashlib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generic, TypeVar

import httpx

from app.data._types import CEFRLevel, VocabularyEntry
from .cache import ResourceCache

logger = logging.getLogger(__name__)

T = TypeVar('T')


@dataclass
class SentenceData:
    """Normalized sentence data from external sources."""
    id: str
    text: str
    language: str
    translations: list[dict[str, str]] = field(default_factory=list)
    audio_available: bool = False
    audio_path: str | None = None
    cefr_level: CEFRLevel | None = None
    tags: list[str] = field(default_factory=list)
    source: str = "unknown"


@dataclass
class VocabularyData:
    """Normalized vocabulary data from external sources."""
    word: str
    language: str
    cefr_level: CEFRLevel
    pos: str | None = None
    definition: str | None = None
    example: str | None = None
    frequency_rank: int | None = None
    source: str = "unknown"


@dataclass
class AudioData:
    """Normalized audio data from external sources."""
    clip_id: str
    text: str
    language: str
    audio_path: str | None = None
    audio_url: str | None = None
    duration_ms: int | None = None
    speaker_info: dict[str, Any] = field(default_factory=dict)
    cefr_level: CEFRLevel | None = None
    source: str = "unknown"


@dataclass
class LearnerTextData:
    """Normalized learner text data from MERLIN corpus."""
    text_id: str
    text: str
    language: str
    cefr_level: CEFRLevel
    learner_l1: str | None = None
    errors: list[dict[str, Any]] = field(default_factory=list)
    corrections: str | None = None
    source: str = "merlin"


class BaseAdapter(ABC, Generic[T]):
    """Base class for all resource adapters."""
    
    def __init__(self, cache: ResourceCache | None = None):
        """
        Initialize adapter with optional cache.
        
        Args:
            cache: ResourceCache instance for caching responses
        """
        self.cache = cache or ResourceCache()
        self.session = httpx.Client(timeout=30.0, follow_redirects=True)
    
    @abstractmethod
    def fetch(self, **kwargs) -> list[T]:
        """Fetch data from the external source."""
        pass
    
    def _generate_cache_key(self, prefix: str, **kwargs) -> str:
        """Generate a unique cache key."""
        key_string = f"{prefix}:{sorted(kwargs.items())}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()


class TatoebaAdapter(BaseAdapter[SentenceData]):
    """
    Adapter for Tatoeba sentence database.
    
    Provides real-world example sentences with translations in 400+ languages.
    """
    
    API_BASE = "https://tatoeba.org"
    
    def __init__(self, cache: ResourceCache | None = None):
        super().__init__(cache)
        self.cache_prefix = "tatoeba_sentences"
    
    def fetch(
        self,
        query: str = "",
        target_language: str = "eng",
        translation_language: str | None = None,
        limit: int = 20,
        cefr_level: CEFRLevel | None = None,
    ) -> list[SentenceData]:
        """
        Fetch sentences from Tatoeba.
        
        Args:
            query: Search term (word or phrase, empty for random)
            target_language: ISO 3-letter code (e.g., 'eng', 'spa')
            translation_language: Optional translation language code
            limit: Maximum number of results
            cefr_level: Filter by CEFR level (if supported)
            
        Returns:
            List of SentenceData objects
        """
        # Try cache first
        cached = self.cache.get(
            self.cache_prefix,
            query=query,
            target_language=target_language,
            translation_language=translation_language,
            limit=limit,
        )
        
        if cached is not None:
            logger.debug(f"Tatoeba cache hit for query='{query}'")
            return [SentenceData(**s) for s in cached]
        
        # Fetch from API
        try:
            sentences = self._fetch_from_api(
                query=query,
                target_language=target_language,
                translation_language=translation_language,
                limit=limit,
            )
            
            # Cache results
            self.cache.set(
                self.cache_prefix,
                [self._sentence_to_dict(s) for s in sentences],
                query=query,
                target_language=target_language,
                translation_language=translation_language,
                limit=limit,
            )
            
            return sentences
            
        except Exception as e:
            logger.error(f"Tatoeba fetch failed: {e}")
            return []
    
    def _fetch_from_api(
        self,
        query: str,
        target_language: str,
        translation_language: str | None,
        limit: int,
    ) -> list[SentenceData]:
        """Fetch sentences from Tatoeba API."""
        # Try multiple endpoints
        endpoints = [
            f"{self.API_BASE}/api/v1/sentences",
            f"{self.API_BASE}/en/api/v1/sentences",
        ]
        
        for endpoint in endpoints:
            try:
                params = {
                    "search": query,
                    "from": target_language,
                    "to": translation_language or "none",
                    "limit": limit,
                }
                
                response = self.session.get(endpoint, params=params, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", data.get("sentences", []))
                    return self._parse_results(results, target_language, translation_language)
                    
            except httpx.TimeoutException:
                logger.warning(f"Tatoeba timeout on {endpoint}")
                continue
            except httpx.HTTPError as e:
                logger.debug(f"Tatoeba HTTP error on {endpoint}: {e}")
                continue
            except Exception as e:
                logger.debug(f"Tatoeba error on {endpoint}: {e}")
                continue
        
        # Fallback: return empty list (no mock data)
        logger.warning("Tatoeba API unavailable, returning empty results")
        return []
    
    def _parse_results(
        self,
        results: list[dict],
        target_language: str,
        translation_language: str | None,
    ) -> list[SentenceData]:
        """Parse API results into SentenceData objects."""
        sentences = []
        
        for item in results:
            translations = []
            if "translations" in item:
                for t in item["translations"]:
                    translations.append({
                        "text": t.get("text", ""),
                        "language": t.get("lang", ""),
                    })
            
            sentence = SentenceData(
                id=str(item.get("id", "")),
                text=item.get("text", ""),
                language=item.get("lang", target_language),
                translations=translations,
                audio_available=bool(item.get("audio_url")),
                tags=item.get("tags", []),
                source="tatoeba",
            )
            sentences.append(sentence)
        
        return sentences
    
    def _sentence_to_dict(self, sentence: SentenceData) -> dict:
        """Convert SentenceData to dictionary for caching."""
        return {
            "id": sentence.id,
            "text": sentence.text,
            "language": sentence.language,
            "translations": sentence.translations,
            "audio_available": sentence.audio_available,
            "tags": sentence.tags,
            "source": sentence.source,
        }
    
    def download_audio(self, sentence_id: str, language: str) -> str | None:
        """
        Download audio for a sentence.
        
        Args:
            sentence_id: Tatoeba sentence ID
            language: Language code
            
        Returns:
            Local file path or None
        """
        # Check cache first
        cached_path = self.cache.get_audio_file("tatoeba", f"{sentence_id}.mp3")
        if cached_path:
            return cached_path
        
        try:
            audio_url = f"{self.API_BASE}/audio/{sentence_id}.mp3"
            response = self.session.get(audio_url, timeout=10.0)
            
            if response.status_code == 200:
                file_path = self.cache.cache_audio_file(
                    "tatoeba",
                    f"{sentence_id}.mp3",
                    response.content,
                )
                return file_path
                
        except Exception as e:
            logger.warning(f"Failed to download Tatoeba audio for {sentence_id}: {e}")
        
        return None


class CEFRLexAdapter(BaseAdapter[VocabularyData]):
    """
    Adapter for CEFRLex vocabulary database.
    
    Provides vocabulary lists organized by CEFR levels (A1-C2).
    """
    
    # Mapping of language codes to CEFRLex datasets
    LEXICON_MAP = {
        "en": "EFLLex",
        "es": "SVALex",
        "fr": "FLELex",
        "de": "DEFLex",
        "it": "ITALLex",
        "pt": "PLELex",
        "nl": "DutchLex",
    }
    
    # Sample vocabulary for fallback when API unavailable
    SAMPLE_VOCAB = {
        "en": {
            "A1": [
                ("hello", "noun", "a greeting", "Hello, how are you?", 1),
                ("water", "noun", "a clear liquid", "I need some water.", 5),
                ("eat", "verb", "to consume food", "Let's eat breakfast.", 3),
                ("good", "adjective", "of high quality", "This is good coffee.", 2),
                ("house", "noun", "a building for living", "They bought a house.", 4),
            ],
            "A2": [
                ("journey", "noun", "a trip or travel", "The journey was long.", 15),
                ("decide", "verb", "to make a choice", "She decided to go.", 12),
            ],
            "B1": [
                ("experience", "noun", "knowledge from doing", "He has work experience.", 20),
                ("improve", "verb", "to make better", "Practice improves skills.", 18),
            ],
            "B2": [
                ("significant", "adjective", "important or notable", "A significant change.", 30),
                ("analyze", "verb", "to examine in detail", "Analyze the data.", 25),
            ],
            "C1": [
                ("comprehensive", "adjective", "complete and thorough", "A comprehensive guide.", 50),
                ("implement", "verb", "to put into action", "Implement the plan.", 45),
            ],
            "C2": [
                ("ubiquitous", "adjective", "present everywhere", "Technology is ubiquitous.", 100),
                ("paradigm", "noun", "a model or pattern", "A new paradigm shift.", 90),
            ],
        },
    }
    
    def __init__(self, cache: ResourceCache | None = None):
        super().__init__(cache)
        self.cache_prefix = "cefrlex_words"
    
    def fetch(
        self,
        language: str,
        cefr_level: CEFRLevel,
        limit: int = 100,
    ) -> list[VocabularyData]:
        """
        Fetch vocabulary words for a specific CEFR level.
        
        Args:
            language: ISO 2-letter language code
            cefr_level: CEFR level (A1, A2, B1, B2, C1, C2)
            limit: Maximum number of words
            
        Returns:
            List of VocabularyData objects
        """
        # Try cache first
        cached = self.cache.get(
            self.cache_prefix,
            language=language,
            cefr_level=cefr_level,
            limit=limit,
        )
        
        if cached is not None:
            logger.debug(f"CEFRLex cache hit for {language} {cefr_level}")
            return [VocabularyData(**w) for w in cached]
        
        # Fetch from source
        try:
            words = self._fetch_words(language, cefr_level, limit)
            
            # Cache results
            self.cache.set(
                self.cache_prefix,
                [self._word_to_dict(w) for w in words],
                language=language,
                cefr_level=cefr_level,
                limit=limit,
            )
            
            return words
            
        except Exception as e:
            logger.error(f"CEFRLex fetch failed: {e}")
            return []
    
    def _fetch_words(
        self,
        language: str,
        cefr_level: CEFRLevel,
        limit: int,
    ) -> list[VocabularyData]:
        """Fetch words from CEFRLex or fallback to sample data."""
        lexicon_name = self.LEXICON_MAP.get(language)
        
        if not lexicon_name:
            logger.warning(f"No CEFRLex dataset for language: {language}")
            return self._get_sample_words(language, cefr_level, limit)
        
        # Try to fetch from GitHub raw content
        try:
            base_url = f"https://raw.githubusercontent.com/CEFRlex/{lexicon_name}/main/data/"
            file_url = f"{base_url}{lexicon_name.lower()}_{cefr_level.lower()}.csv"
            
            response = self.session.get(file_url, timeout=15.0)
            
            if response.status_code == 200:
                return self._parse_csv(response.text, cefr_level, language, limit)
            else:
                logger.warning(f"CEFRLex file not found: {file_url}")
                return self._get_sample_words(language, cefr_level, limit)
                
        except Exception as e:
            logger.warning(f"CEFRLex fetch error, using sample data: {e}")
            return self._get_sample_words(language, cefr_level, limit)
    
    def _parse_csv(
        self,
        csv_content: str,
        cefr_level: CEFRLevel,
        language: str,
        limit: int,
    ) -> list[VocabularyData]:
        """Parse CSV content into VocabularyData objects."""
        words = []
        lines = csv_content.strip().split('\n')
        
        # Skip header if present
        start_idx = 1 if lines and 'word' in lines[0].lower() else 0
        
        for line in lines[start_idx:limit]:
            parts = line.split(',')
            if len(parts) >= 3:
                word = VocabularyData(
                    word=parts[0].strip(),
                    language=language,
                    cefr_level=cefr_level,
                    pos=parts[1].strip() if len(parts) > 1 else None,
                    definition=parts[2].strip() if len(parts) > 2 else None,
                    source="cefrlex",
                )
                words.append(word)
        
        return words
    
    def _get_sample_words(
        self,
        language: str,
        cefr_level: CEFRLevel,
        limit: int,
    ) -> list[VocabularyData]:
        """Get sample vocabulary words as fallback."""
        sample_data = self.SAMPLE_VOCAB.get(language, {}).get(cefr_level, [])
        
        if not sample_data:
            # Use English A1 as universal fallback
            sample_data = self.SAMPLE_VOCAB.get("en", {}).get(cefr_level, [])
        
        words = []
        for item in sample_data[:limit]:
            word, pos, definition, example, rank = item
            words.append(VocabularyData(
                word=word,
                language=language,
                cefr_level=cefr_level,
                pos=pos,
                definition=definition,
                example=example,
                frequency_rank=rank,
                source="cefrlex_sample",
            ))
        
        return words
    
    def _word_to_dict(self, word: VocabularyData) -> dict:
        """Convert VocabularyData to dictionary for caching."""
        return {
            "word": word.word,
            "language": word.language,
            "cefr_level": word.cefr_level,
            "pos": word.pos,
            "definition": word.definition,
            "example": word.example,
            "frequency_rank": word.frequency_rank,
            "source": word.source,
        }


class MerlinAdapter(BaseAdapter[LearnerTextData]):
    """
    Adapter for MERLIN Corpus of learner texts.
    
    Provides authentic learner writings with CEFR annotations and error analysis.
    """
    
    CORPUS_URL = "https://merlin-corpus.github.io"
    
    def __init__(self, cache: ResourceCache | None = None):
        super().__init__(cache)
        self.cache_prefix = "merlin_texts"
    
    def fetch(
        self,
        language: str,
        cefr_level: CEFRLevel,
        limit: int = 20,
        learner_l1: str | None = None,
    ) -> list[LearnerTextData]:
        """
        Fetch learner texts from MERLIN corpus.
        
        Args:
            language: Target language code
            cefr_level: CEFR level
            limit: Maximum number of texts
            learner_l1: Optional filter by learner's native language
            
        Returns:
            List of LearnerTextData objects
        """
        # Try cache first
        cached = self.cache.get(
            self.cache_prefix,
            language=language,
            cefr_level=cefr_level,
            learner_l1=learner_l1,
            limit=limit,
        )
        
        if cached is not None:
            logger.debug(f"MERLIN cache hit for {language} {cefr_level}")
            return [LearnerTextData(**t) for t in cached]
        
        # Fetch from source
        try:
            texts = self._fetch_texts(language, cefr_level, limit, learner_l1)
            
            # Cache results
            self.cache.set(
                self.cache_prefix,
                [self._text_to_dict(t) for t in texts],
                language=language,
                cefr_level=cefr_level,
                learner_l1=learner_l1,
                limit=limit,
            )
            
            return texts
            
        except Exception as e:
            logger.error(f"MERLIN fetch failed: {e}")
            return []
    
    def _fetch_texts(
        self,
        language: str,
        cefr_level: CEFRLevel,
        limit: int,
        learner_l1: str | None,
    ) -> list[LearnerTextData]:
        """Fetch texts from MERLIN corpus."""
        # MERLIN corpus access is limited; return sample data for now
        # In production, this would connect to the actual corpus API
        logger.info(f"MERLIN: Returning sample texts for {language} {cefr_level}")
        
        return self._get_sample_texts(language, cefr_level, limit, learner_l1)
    
    def _get_sample_texts(
        self,
        language: str,
        cefr_level: CEFRLevel,
        limit: int,
        learner_l1: str | None,
    ) -> list[LearnerTextData]:
        """Generate sample learner texts as placeholder."""
        samples = [
            {
                "text": "Hello, my name is Maria. I am from Spain. I like learning English.",
                "errors": [{"wrong": "am", "correct": "is", "type": "verb_agreement"}],
                "correction": "Hello, my name is Maria. I is from Spain...",
            },
            {
                "text": "Yesterday I go to the park with my friends. We play football.",
                "errors": [{"wrong": "go", "correct": "went", "type": "past_tense"}],
                "correction": "Yesterday I went to the park...",
            },
        ]
        
        texts = []
        for i, sample in enumerate(samples[:limit]):
            text = LearnerTextData(
                text_id=f"merlin_{language}_{cefr_level}_{i}",
                text=sample["text"],
                language=language,
                cefr_level=cefr_level,
                learner_l1=learner_l1 or "unknown",
                errors=sample.get("errors", []),
                corrections=sample.get("correction"),
                source="merlin_sample",
            )
            texts.append(text)
        
        return texts
    
    def _text_to_dict(self, text: LearnerTextData) -> dict:
        """Convert LearnerTextData to dictionary for caching."""
        return {
            "text_id": text.text_id,
            "text": text.text,
            "language": text.language,
            "cefr_level": text.cefr_level,
            "learner_l1": text.learner_l1,
            "errors": text.errors,
            "corrections": text.corrections,
            "source": text.source,
        }


class CommonVoiceAdapter(BaseAdapter[AudioData]):
    """
    Adapter for Mozilla Common Voice dataset.
    
    Provides crowdsourced audio clips for speech recognition and listening practice.
    """
    
    BASE_URL = "https://commonvoice.mozilla.org"
    
    def __init__(self, cache: ResourceCache | None = None):
        super().__init__(cache)
        self.cache_prefix = "common_voice_audio"
    
    def fetch(
        self,
        language: str,
        cefr_level: CEFRLevel | None = None,
        limit: int = 10,
    ) -> list[AudioData]:
        """
        Fetch audio clips from Common Voice.
        
        Args:
            language: Language code
            cefr_level: Optional CEFR level filter
            limit: Maximum number of clips
            
        Returns:
            List of AudioData objects
        """
        # Try cache first
        cached = self.cache.get(
            self.cache_prefix,
            language=language,
            cefr_level=cefr_level,
            limit=limit,
        )
        
        if cached is not None:
            logger.debug(f"Common Voice cache hit for {language}")
            return [AudioData(**a) for a in cached]
        
        # Fetch metadata only (audio downloaded on-demand)
        try:
            clips = self._fetch_metadata(language, limit)
            
            # Cache metadata
            self.cache.set(
                self.cache_prefix,
                [self._clip_to_dict(c) for c in clips],
                language=language,
                cefr_level=cefr_level,
                limit=limit,
            )
            
            return clips
            
        except Exception as e:
            logger.error(f"Common Voice fetch failed: {e}")
            return []
    
    def _fetch_metadata(self, language: str, limit: int) -> list[AudioData]:
        """Fetch audio clip metadata from Common Voice."""
        # Common Voice doesn't have a public API for browsing clips
        # This would typically use pre-downloaded metadata files
        logger.info(f"Common Voice: Returning metadata placeholders for {language}")
        
        # Return placeholder metadata
        clips = []
        for i in range(limit):
            clip = AudioData(
                clip_id=f"cv_{language}_{i}",
                text=f"Sample text {i + 1} for {language}",
                language=language,
                source="common_voice",
            )
            clips.append(clip)
        
        return clips
    
    def download_clip(self, clip_id: str, language: str) -> str | None:
        """
        Download an audio clip on-demand.
        
        Args:
            clip_id: Clip identifier
            language: Language code
            
        Returns:
            Local file path or None
        """
        # Check cache first
        cached_path = self.cache.get_audio_file("common_voice", f"{clip_id}.mp3")
        if cached_path:
            return cached_path
        
        # In production, this would download from Common Voice CDN
        # For now, return None (audio not available)
        logger.warning(f"Common Voice audio download not implemented for {clip_id}")
        return None
    
    def _clip_to_dict(self, clip: AudioData) -> dict:
        """Convert AudioData to dictionary for caching."""
        return {
            "clip_id": clip.clip_id,
            "text": clip.text,
            "language": clip.language,
            "audio_path": clip.audio_path,
            "audio_url": clip.audio_url,
            "duration_ms": clip.duration_ms,
            "speaker_info": clip.speaker_info,
            "source": clip.source,
        }

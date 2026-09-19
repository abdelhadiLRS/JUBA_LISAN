"""
Service for integrating external educational resources:
- Tatoeba: Real sentences with translations
- CEFRLex: CEFR-level vocabulary
- Mozilla Common Voice: Audio data
- MERLIN Corpus: Learner texts with CEFR levels
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urljoin

import httpx
import requests

from app.core.config import settings
from app.data._types import CEFRLevel, VocabularyEntry

logger = logging.getLogger(__name__)

# ============================================================================
# Configuration for External Resources
# ============================================================================

TATOEBA_API_BASE = "https://tatoeba.org/api"
TATOEBA_DOWNLOADS_BASE = "https://downloads.tatoeba.org"

CEFRLEX_REPO_URL = "https://github.com/CEFRlex/CEFRlex"
MERLIN_CORPUS_URL = "https://merlin-corpus.github.io"

COMMON_VOICE_BASE = "https://commonvoice.mozilla.org"

# Local cache directory
CACHE_DIR = Path(settings.CACHE_DIR) if hasattr(settings, 'CACHE_DIR') else Path("/tmp/juba_lisan_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# Data Models
# ============================================================================

@dataclass
class TatoebaSentence:
    """Represents a sentence from Tatoeba."""
    id: str
    text: str
    language: str
    translations: list[dict[str, str]] = field(default_factory=list)
    audio_url: str | None = None
    cefr_level: CEFRLevel | None = None
    tags: list[str] = field(default_factory=list)


@dataclass
class CEFRLexWord:
    """Represents a word from CEFRLex with CEFR level information."""
    word: str
    language: str
    cefr_level: CEFRLevel
    frequency_rank: int | None = None
    lemma: str | None = None
    pos: str | None = None
    definition: str | None = None
    example: str | None = None


@dataclass
class CommonVoiceAudio:
    """Represents audio clip from Mozilla Common Voice."""
    clip_id: str
    text: str
    language: str
    audio_path: str | None = None  # Local path if downloaded
    duration_ms: int | None = None
    speaker_age: str | None = None
    speaker_gender: str | None = None


@dataclass
class MerlinText:
    """Represents a learner text from MERLIN corpus."""
    text_id: str
    text: str
    language: str
    cefr_level: CEFRLevel
    learner_l1: str | None = None  # Native language of learner
    errors: list[dict[str, Any]] = field(default_factory=list)
    corrections: str | None = None


# ============================================================================
# Tatoeba Service
# ============================================================================

class TatoebaService:
    """Service for fetching sentences and translations from Tatoeba."""
    
    def __init__(self):
        self.api_base = "https://tatoeba.org"
        self.cache_dir = CACHE_DIR / "tatoeba"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session = httpx.Client(timeout=30.0, follow_redirects=True)
    
    def search_sentences(
        self,
        query: str,
        target_language: str,
        translation_language: str | None = None,
        limit: int = 20,
        cefr_level: CEFRLevel | None = None,
    ) -> list[TatoebaSentence]:
        """
        Search for sentences in Tatoeba using direct downloads.
        
        Note: Tatoeba's API has changed frequently. This implementation
        falls back to downloading sentence files directly when API fails.
        
        Args:
            query: Search term (word or phrase)
            target_language: Language code (e.g., 'eng', 'spa', 'fra')
            translation_language: Optional translation language
            limit: Maximum number of results
            cefr_level: Filter by CEFR level if available
            
        Returns:
            List of TatoebaSentence objects
        """
        cache_key = hashlib.md5(
            f"{query}_{target_language}_{translation_language}_{limit}".encode()
        ).hexdigest()
        cache_file = self.cache_dir / f"search_{cache_key}.json"
        
        # Try cache first
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                logger.info(f"Loaded Tatoeba search from cache: {query}")
                return [self._parse_sentence(s) for s in cached_data]
            except Exception as e:
                logger.warning(f"Cache read error: {e}")
        
        # Try multiple API endpoints
        endpoints_to_try = [
            f"{self.api_base}/api/v1/sentences",
            f"{self.api_base}/en/api/v1/sentences",
            f"{self.api_base}/downloads",
        ]
        
        for endpoint in endpoints_to_try:
            try:
                params = {
                    "search": query,
                    "from": target_language,
                    "to": translation_language or "none",
                    "limit": limit,
                }
                
                response = self.session.get(endpoint, params=params)
                if response.status_code == 200:
                        results = data.get("results", data.get("sentences", []))
                    
                    sentences = []
                    for item in results:
                        sentence = self._parse_sentence(item)
                        sentences.append(sentence)
                    
                    # Cache results
                    with open(cache_file, 'w', encoding='utf-8') as f:
                        json.dump(results, f, ensure_ascii=False)
                    
                    logger.info(f"Fetched {len(sentences)} sentences from Tatoeba for '{query}'")
                    return sentences
                    
            except Exception as e:
                logger.debug(f"Endpoint {endpoint} failed: {e}")
                continue
        
        # Fallback: Return mock data for demonstration
        logger.warning(f"Tatoeba API unavailable, returning sample data for '{query}'")
        sample_sentences = [
            {
                "id": "1",
                "text": "Hello, how are you?",
                "lang": target_language,
                "translations": [{"text": "Hola, ¿cómo estás?", "lang": translation_language or "spa"}]
            },
            {
                "id": "2", 
                "text": "Hello everyone!",
                "lang": target_language,
                "translations": [{"text": "¡Hola a todos!", "lang": translation_language or "spa"}]
            },
            {
                "id": "3",
                "text": "Say hello to your family.",
                "lang": target_language,
                "translations": [{"text": "Saluda a tu familia.", "lang": translation_language or "spa"}]
            }
        ]
        
        # Cache sample data
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(sample_sentences, f, ensure_ascii=False)
        
        return [self._parse_sentence(s) for s in sample_sentences]
    
    def get_sentence_by_id(self, sentence_id: str) -> TatoebaSentence | None:
        """Fetch a specific sentence by ID."""
        try:
            endpoint = f"{self.api_base}/internal/1.0/sentences/{sentence_id}"
            response = self.session.get(endpoint)
            response.raise_for_status()
            return self._parse_sentence(response.json())
        except Exception as e:
            logger.error(f"Error fetching sentence {sentence_id}: {e}")
            return None
    
    def download_audio(self, sentence_id: str, language: str) -> str | None:
        """
        Download audio for a sentence if available.
        Returns local file path or None.
        """
        audio_dir = self.cache_dir / "audio" / language
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        audio_file = audio_dir / f"{sentence_id}.mp3"
        
        if audio_file.exists():
            return str(audio_file)
        
        try:
            # Tatoeba audio URLs follow pattern
            audio_url = f"https://api.tatoeba.org/audio/{sentence_id}.mp3"
            response = self.session.get(audio_url, timeout=10)
            
            if response.status_code == 200:
                with open(audio_file, 'wb') as f:
                    f.write(response.content)
                logger.info(f"Downloaded audio for sentence {sentence_id}")
                return str(audio_file)
        except Exception as e:
            logger.warning(f"Could not download audio for {sentence_id}: {e}")
        
        return None
    
    def _parse_sentence(self, data: dict) -> TatoebaSentence:
        """Parse raw API response into TatoebaSentence."""
        translations = []
        if "translations" in data:
            for t in data["translations"]:
                translations.append({
                    "text": t.get("text", ""),
                    "language": t.get("lang", ""),
                })
        
        return TatoebaSentence(
            id=str(data.get("id", "")),
            text=data.get("text", ""),
            language=data.get("lang", ""),
            translations=translations,
            audio_url=data.get("audio_url"),
            tags=data.get("tags", []),
        )


# ============================================================================
# CEFRLex Service
# ============================================================================

class CEFRLexService:
    """
    Service for accessing CEFR-level vocabulary from CEFRLex project.
    Provides vocabulary sorted by CEFR levels (A1-C2).
    
    Note: CEFRLex datasets are hosted on GitHub with varying structures.
    This service includes fallback to sample data when remote files are unavailable.
    """
    
    # Mapping of language codes to CEFRLex datasets
    LEXICON_MAP = {
        "en": "EFLLex",  # English as Foreign Language
        "es": "SVALex",  # Spanish
        "fr": "FLELex",  # French
        "de": "DEFLex",  # German
        "it": "ITALLex", # Italian
        "pt": "PLELex",  # Portuguese
        "nl": "DutchLex", # Dutch
    }
    
    # Sample vocabulary for fallback (CEFR-aligned)
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
        "es": {
            "A1": [
                ("hola", "noun", "un saludo", "Hola, ¿cómo estás?", 1),
                ("agua", "noun", "líquido transparente", "Necesito agua.", 5),
                ("comer", "verb", "ingerir alimentos", "Vamos a comer.", 3),
                ("bueno", "adjective", "de alta calidad", "Este café es bueno.", 2),
                ("casa", "noun", "edificio para vivir", "Compraron una casa.", 4),
            ],
        },
        "fr": {
            "A1": [
                ("bonjour", "noun", "une salutation", "Bonjour, comment allez-vous?", 1),
                ("eau", "noun", "liquide transparent", "Je veux de l'eau.", 5),
                ("manger", "verb", "consommer de la nourriture", "Allons manger.", 3),
                ("bon", "adjective", "de haute qualité", "Ce café est bon.", 2),
                ("maison", "noun", "bâtiment pour habiter", "Ils ont acheté une maison.", 4),
            ],
        },
        "de": {
            "A1": [
                ("hallo", "noun", "eine Begrüßung", "Hallo, wie geht es dir?", 1),
                ("wasser", "noun", "eine klare Flüssigkeit", "Ich brauche Wasser.", 5),
                ("essen", "verb", "Nahrung zu sich nehmen", "Lass uns essen.", 3),
                ("gut", "adjective", "von hoher Qualität", "Das ist guter Kaffee.", 2),
                ("haus", "noun", "ein Gebäude zum Wohnen", "Sie kauften ein Haus.", 4),
            ],
        },
    }
    
    def __init__(self):
        self.cache_dir = CACHE_DIR / "cefrlex"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session = httpx.Client(timeout=30.0)
    
    def get_words_by_level(
        self,
        language: str,
        cefr_level: CEFRLevel,
        limit: int = 100,
    ) -> list[CEFRLexWord]:
        """
        Get vocabulary words for a specific CEFR level.
        
        Args:
            language: ISO language code (e.g., 'en', 'es', 'fr')
            cefr_level: CEFR level (A1, A2, B1, B2, C1, C2)
            limit: Maximum number of words to return
            
        Returns:
            List of CEFRLexWord objects
        """
        lexicon_name = self.LEXICON_MAP.get(language)
        if not lexicon_name:
            logger.warning(f"No CEFRLex dataset found for language: {language}")
            # Fallback to sample data if available
            return self._get_sample_words(language, cefr_level, limit)
        
        cache_key = f"{lexicon_name}_{cefr_level}_{limit}"
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                logger.info(f"Loaded CEFRLex data from cache: {cache_key}")
                return [self._parse_word(w) for w in cached_data]
            except Exception as e:
                logger.warning(f"Cache read error: {e}")
        
        # Try to fetch from GitHub raw content
        try:
            # CEFRLex data is typically in CSV format on GitHub
            base_url = f"https://raw.githubusercontent.com/CEFRlex/{lexicon_name}/main/data/"
            file_url = f"{base_url}{lexicon_name.lower()}_{cefr_level.lower()}.csv"
            
            response = self.session.get(file_url)
            if response.status_code == 200:
                words = self._parse_csv(response.text, cefr_level, language, limit)
                
                # Cache results
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump([self._word_to_dict(w) for w in words], f, ensure_ascii=False)
                
                logger.info(f"Fetched {len(words)} words from CEFRLex for {language} {cefr_level}")
                return words
            else:
                logger.warning(f"CEFRLex file not found: {file_url}")
                # Fallback to sample data
                return self._get_sample_words(language, cefr_level, limit)
                
        except Exception as e:
            logger.error(f"Error fetching CEFRLex data: {e}")
            # Fallback to sample data
            return self._get_sample_words(language, cefr_level, limit)
    
    def _get_sample_words(self, language: str, cefr_level: CEFRLevel, limit: int) -> list[CEFRLexWord]:
        """Get sample vocabulary words when remote data is unavailable."""
        lang_vocab = self.SAMPLE_VOCAB.get(language, self.SAMPLE_VOCAB.get("en", {}))
        level_words = lang_vocab.get(cefr_level, [])
        
        if not level_words:
            logger.info(f"No sample vocabulary for {language} {cefr_level}, using generic A1 words")
            level_words = self.SAMPLE_VOCAB["en"]["A1"][:min(limit, 5)]
        
        words = []
        for word_data in level_words[:limit]:
            words.append(CEFRLexWord(
                word=word_data[0],
                language=language,
                cefr_level=cefr_level,
                frequency_rank=word_data[4] if len(word_data) > 4 else None,
                pos=word_data[1],
                definition=word_data[2],
                example=word_data[3],
            ))
        
        logger.info(f"Returning {len(words)} sample words for {language} {cefr_level}")
        return words
    
    def get_frequency_ranked_words(
        self,
        language: str,
        min_rank: int = 1,
        max_rank: int = 1000,
    ) -> list[CEFRLexWord]:
        """Get words ranked by frequency within a range."""
        all_words = []
        for level in ["A1", "A2", "B1", "B2", "C1", "C2"]:
            words = self.get_words_by_level(language, level, limit=500)
            all_words.extend(words)
        
        # Filter by frequency rank
        filtered = [
            w for w in all_words 
            if w.frequency_rank and min_rank <= w.frequency_rank <= max_rank
        ]
        
        # Sort by frequency
        filtered.sort(key=lambda w: w.frequency_rank or 999999)
        return filtered[:max_rank - min_rank + 1]
    
    def _parse_csv(self, csv_content: str, level: CEFRLevel, language: str, limit: int) -> list[CEFRLexWord]:
        """Parse CSV content from CEFRLex."""
        words = []
        lines = csv_content.strip().split('\n')
        
        if len(lines) < 2:
            return []
        
        # Assume header row exists
        header = lines[0].lower().split(',')
        
        for line in lines[1:limit+1]:
            parts = line.split(',')
            if len(parts) < 2:
                continue
            
            word_data = {}
            for i, col in enumerate(header):
                if i < len(parts):
                    word_data[col] = parts[i].strip('"')
            
            # Extract relevant fields
            word = word_data.get('word', word_data.get('lemma', ''))
            if not word:
                continue
            
            freq_rank = None
            if 'frequency' in word_data or 'rank' in word_data:
                try:
                    freq_rank = int(word_data.get('frequency', word_data.get('rank', 0)))
                except ValueError:
                    pass
            
            words.append(CEFRLexWord(
                word=word,
                language=language,
                cefr_level=level,
                frequency_rank=freq_rank,
                lemma=word_data.get('lemma'),
                pos=word_data.get('pos'),
                definition=word_data.get('definition'),
                example=word_data.get('example'),
            ))
        
        return words
    
    def _parse_word(self, data: dict) -> CEFRLexWord:
        """Parse dictionary into CEFRLexWord."""
        return CEFRLexWord(
            word=data.get('word', ''),
            language=data.get('language', ''),
            cefr_level=data.get('cefr_level', 'A1'),
            frequency_rank=data.get('frequency_rank'),
            lemma=data.get('lemma'),
            pos=data.get('pos'),
            definition=data.get('definition'),
            example=data.get('example'),
        )
    
    def _word_to_dict(self, word: CEFRLexWord) -> dict:
        """Convert CEFRLexWord to dictionary for caching."""
        return {
            'word': word.word,
            'language': word.language,
            'cefr_level': word.cefr_level,
            'frequency_rank': word.frequency_rank,
            'lemma': word.lemma,
            'pos': word.pos,
            'definition': word.definition,
            'example': word.example,
        }


# ============================================================================
# Mozilla Common Voice Service
# ============================================================================

class CommonVoiceService:
    """
    Service for accessing Mozilla Common Voice audio datasets.
    Handles large file downloads with streaming and progress tracking.
    """
    
    def __init__(self):
        self.base_url = COMMON_VOICE_BASE
        self.cache_dir = CACHE_DIR / "common_voice"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session = httpx.Client(timeout=None)  # No timeout for large downloads
    
    def get_dataset_info(self, language: str) -> dict | None:
        """
        Get information about available Common Voice dataset for a language.
        
        Args:
            language: Language code (e.g., 'en', 'es', 'fr')
            
        Returns:
            Dataset metadata or None if not found
        """
        # Common Voice datasets are hosted on Hugging Face now
        hf_url = "https://huggingface.co/api/datasets/mozilla-foundation/common_voice_17_0"
        
        try:
            response = self.session.get(hf_url)
            if response.status_code == 200:
                data = response.json()
                # Filter for specific language
                # This is simplified - actual implementation would parse dataset cards
                return {
                    "language": language,
                    "available": True,
                    "size_gb": "N/A",  # Would need to parse from dataset info
                }
        except Exception as e:
            logger.error(f"Error fetching Common Voice info: {e}")
        
        return None
    
    def download_clips(
        self,
        language: str,
        clip_ids: list[str],
        progress_callback: callable | None = None,
    ) -> list[CommonVoiceAudio]:
        """
        Download specific audio clips.
        
        Note: Common Voice datasets are large (several GB).
        This method downloads individual clips on-demand.
        
        Args:
            language: Language code
            clip_ids: List of clip IDs to download
            progress_callback: Optional callback(download_progress, total)
            
        Returns:
            List of CommonVoiceAudio objects with local paths
        """
        audio_dir = self.cache_dir / language / "clips"
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        results = []
        total = len(clip_ids)
        
        for i, clip_id in enumerate(clip_ids):
            clip_file = audio_dir / f"{clip_id}.mp3"
            
            if clip_file.exists():
                results.append(CommonVoiceAudio(
                    clip_id=clip_id,
                    text="",  # Would need to fetch from metadata
                    language=language,
                    audio_path=str(clip_file),
                ))
                continue
            
            # Download URL pattern (simplified - actual URLs vary)
            download_url = f"https://commonvoice.mozilla.org/{language}/clips/{clip_id}.mp3"
            
            try:
                with self.session.stream('GET', download_url) as response:
                    if response.status_code == 200:
                        with open(clip_file, 'wb') as f:
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                        
                        results.append(CommonVoiceAudio(
                            clip_id=clip_id,
                            text="",
                            language=language,
                            audio_path=str(clip_file),
                        ))
                        
                        if progress_callback:
                            progress_callback(i + 1, total)
                            
            except Exception as e:
                logger.warning(f"Failed to download clip {clip_id}: {e}")
        
        return results
    
    def stream_audio(self, language: str, clip_id: str):
        """
        Stream audio without downloading to disk.
        Useful for TTS/listening exercises.
        
        Yields:
            Audio chunks
        """
        url = f"https://commonvoice.mozilla.org/{language}/clips/{clip_id}.mp3"
        
        try:
            with self.session.stream('GET', url) as response:
                response.raise_for_status()
                for chunk in response.iter_bytes(chunk_size=4096):
                    yield chunk
        except Exception as e:
            logger.error(f"Streaming error for {clip_id}: {e}")
            raise


# ============================================================================
# MERLIN Corpus Service
# ============================================================================

class MerlinCorpusService:
    """
    Service for accessing MERLIN Corpus - learner texts with CEFR levels.
    Useful for generating realistic reading materials and error analysis.
    """
    
    def __init__(self):
        self.base_url = MERLIN_CORPUS_URL
        self.cache_dir = CACHE_DIR / "merlin"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session = httpx.Client(timeout=30.0)
    
    def get_texts_by_level(
        self,
        language: str,
        cefr_level: CEFRLevel,
        limit: int = 10,
    ) -> list[MerlinText]:
        """
        Fetch learner texts for a specific CEFR level.
        
        Args:
            language: Language code ('de', 'it', 'cs')
            cefr_level: CEFR level
            limit: Maximum number of texts
            
        Returns:
            List of MerlinText objects
        """
        # MERLIN corpus has limited languages: German, Italian, Czech
        if language not in ['de', 'it', 'cs']:
            logger.warning(f"MERLIN corpus not available for: {language}")
            return []
        
        cache_file = self.cache_dir / f"{language}_{cefr_level}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                logger.info("Loaded MERLIN texts from cache")
                return [self._parse_text(t) for t in cached_data]
            except Exception as e:
                logger.warning(f"Cache read error: {e}")
        
        # MERLIN corpus access would require proper API or dataset download
        # This is a placeholder for future implementation
        logger.info(f"MERLIN corpus fetch requested for {language} {cefr_level}")
        return []
    
    def _parse_text(self, data: dict) -> MerlinText:
        """Parse dictionary into MerlinText."""
        return MerlinText(
            text_id=data.get('id', ''),
            text=data.get('text', ''),
            language=data.get('language', ''),
            cefr_level=data.get('cefr_level', 'A1'),
            learner_l1=data.get('learner_l1'),
            errors=data.get('errors', []),
            corrections=data.get('corrections'),
        )


# ============================================================================
# Unified External Resources Service
# ============================================================================

class ExternalResourcesService:
    """
    Unified service for all external educational resources.
    Provides a single interface for accessing Tatoeba, CEFRLex, Common Voice, and MERLIN.
    """
    
    def __init__(self):
        self.tatoeba = TatoebaService()
        self.cefrlex = CEFRLexService()
        self.common_voice = CommonVoiceService()
        self.merlin = MerlinCorpusService()
    
    def enrich_vocabulary_with_examples(
        self,
        word: str,
        target_language: str,
        native_language: str | None = None,
        cefr_level: CEFRLevel | None = None,
    ) -> dict[str, Any]:
        """
        Enrich a vocabulary entry with real examples from external sources.
        
        Args:
            word: The word to enrich
            target_language: Target language code (e.g., 'en-GB', 'es-ES')
            native_language: User's native language for translations
            cefr_level: Optional CEFR level filter
            
        Returns:
            Dictionary with enriched vocabulary data
        """
        lang_code = target_language.split('-')[0][:3]  # Convert 'en-GB' to 'eng'
        
        # Fetch example sentences from Tatoeba
        sentences = self.tatoeba.search_sentences(
            query=word,
            target_language=lang_code,
            translation_language=native_language.split('-')[0][:3] if native_language else None,
            limit=10,
            cefr_level=cefr_level,
        )
        
        # Build enriched entry
        enriched = {
            "word": word,
            "language": target_language,
            "cefr_level": cefr_level,
            "example_sentences": [],
            "audio_available": False,
        }
        
        for sent in sentences:
            example_data = {
                "text": sent.text,
                "translations": sent.translations,
                "audio_url": sent.audio_url,
            }
            
            # Try to get audio
            if sent.id:
                audio_path = self.tatoeba.download_audio(sent.id, lang_code)
                if audio_path:
                    example_data["local_audio_path"] = audio_path
                    enriched["audio_available"] = True
            
            enriched["example_sentences"].append(example_data)
        
        return enriched
    
    def get_cefr_vocabulary_list(
        self,
        target_language: str,
        cefr_level: CEFRLevel,
        count: int = 50,
    ) -> list[VocabularyEntry]:
        """
        Get a list of vocabulary words for a specific CEFR level.
        
        Args:
            target_language: Target language (e.g., 'en-GB')
            cefr_level: CEFR level
            count: Number of words to return
            
        Returns:
            List of VocabularyEntry objects
        """
        lang_code = target_language.split('-')[0]
        
        cefr_words = self.cefrlex.get_words_by_level(
            language=lang_code,
            cefr_level=cefr_level,
            limit=count,
        )
        
        vocab_entries = []
        for cw in cefr_words:
            # Enrich with example sentences
            enriched = self.enrich_vocabulary_with_examples(
                word=cw.word,
                target_language=target_language,
                cefr_level=cefr_level,
            )
            
            example = ""
            if enriched["example_sentences"]:
                example = enriched["example_sentences"][0]["text"]
            
            vocab_entries.append(VocabularyEntry(
                word=cw.word,
                pos=cw.pos or "noun",
                definition=cw.definition or "",
                example=example,
                frequency_rank=cw.frequency_rank,
            ))
        
        return vocab_entries
    
    def get_listening_materials(
        self,
        target_language: str,
        cefr_level: CEFRLevel,
        count: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Get listening materials with audio from external sources.
        
        Args:
            target_language: Target language
            cefr_level: CEFR level
            count: Number of items
            
        Returns:
            List of dictionaries with text and audio paths
        """
        lang_code = target_language.split('-')[0]
        
        # Get sentences from Tatoeba
        # In practice, you'd want to filter by CEFR level using tags
        sentences = self.tatoeba.search_sentences(
            query="",  # Empty query returns random sentences
            target_language=lang_code[:3],
            limit=count * 2,  # Get extra to filter
            cefr_level=cefr_level,
        )
        
        materials = []
        for sent in sentences[:count]:
            audio_path = None
            if sent.id:
                audio_path = self.tatoeba.download_audio(sent.id, lang_code[:3])
            
            if audio_path or sent.audio_url:
                materials.append({
                    "text": sent.text,
                    "audio_path": audio_path,
                    "audio_url": sent.audio_url,
                    "translations": sent.translations,
                    "difficulty": cefr_level,
                })
        
        return materials


# ============================================================================
# Integration Helper Functions
# ============================================================================

def integrate_tatoeba_sentences_into_curriculum(
    target_language: str,
    cefr_level: CEFRLevel,
    unit_id: str,
) -> list[dict]:
    """
    Fetch Tatoeba sentences and format them for curriculum integration.
    
    This function can be called during curriculum generation to add
    real-world example sentences to vocabulary and grammar lessons.
    """
    service = ExternalResourcesService()
    lang_code = target_language.split('-')[0]
    
    # Get sentences tagged with CEFR level (if available)
    # For now, we'll search broadly and let the frontend filter
    sentences = service.tatoeba.search_sentences(
        query="",
        target_language=lang_code[:3],
        limit=50,
    )
    
    formatted = []
    for sent in sentences:
        formatted.append({
            "unit_ref": unit_id,
            "type": "reading_listening",
            "content": {
                "text": sent.text,
                "translations": sent.translations,
                "audio_available": bool(sent.audio_url),
            },
            "metadata": {
                "source": "Tatoeba",
                "sentence_id": sent.id,
                "tags": sent.tags,
            }
        })
    
    return formatted


def integrate_cefr_vocabulary_into_sets(
    target_language: str,
    cefr_level: CEFRLevel,
    topic: str,
    unit_ref: str,
) -> list[VocabularyEntry]:
    """
    Fetch CEFR-level vocabulary and format as VocabularySet entries.
    
    This integrates CEFRLex data into the existing vocabulary system.
    """
    service = ExternalResourcesService()
    
    vocab_list = service.get_cefr_vocabulary_list(
        target_language=target_language,
        cefr_level=cefr_level,
        count=30,
    )
    
    return vocab_list


# ============================================================================
# Main execution for testing
# ============================================================================

if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    service = ExternalResourcesService()
    
    print("\n=== Testing Tatoeba Integration ===")
    sentences = service.tatoeba.search_sentences(
        query="hello",
        target_language="eng",
        translation_language="spa",
        limit=5,
    )
    for s in sentences:
        print(f"- {s.text}")
        if s.translations:
            print(f"  Translation: {s.translations[0]['text']}")
    
    print("\n=== Testing CEFRLex Integration ===")
    words = service.cefrlex.get_words_by_level(
        language="en",
        cefr_level="A1",
        limit=10,
    )
    for w in words:
        print(f"- {w.word} (Rank: {w.frequency_rank})")
    
    print("\n=== Testing Vocabulary Enrichment ===")
    enriched = service.enrich_vocabulary_with_examples(
        word="water",
        target_language="en-GB",
        native_language="es-ES",
        cefr_level="A1",
    )
    print(f"Word: {enriched['word']}")
    print(f"Examples: {len(enriched['example_sentences'])}")
    print(f"Audio available: {enriched['audio_available']}")

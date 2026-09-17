"""
Educational Resource Resolver.

This module implements the core logic for deciding when to use:
- Local curriculum data (primary, always available)
- External resources (enrichment, optional)
- Hybrid approach (local + external)

The resolver ensures that external resource failures never break the application.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from app.data._types import CEFRLevel, VocabularyEntry
from app.data.curriculum import get_curriculum
from app.data.vocabulary import get_vocabulary_set as local_get_vocabulary_set

from .adapters import (
    TatoebaAdapter,
    CEFRLexAdapter,
    MerlinAdapter,
    CommonVoiceAdapter,
    SentenceData,
    VocabularyData,
    AudioData,
    LearnerTextData,
)
from .cache import ResourceCache

logger = logging.getLogger(__name__)


class SourceStrategy(Enum):
    """Strategy for selecting data sources."""
    LOCAL_ONLY = "local_only"
    EXTERNAL_ONLY = "external_only"
    HYBRID = "hybrid"  # Local primary, external enrichment
    EXTERNAL_PRIMARY = "external_primary"  # External primary, local fallback


@dataclass
class ResourceConfig:
    """Configuration for resource resolution."""
    strategy: SourceStrategy = SourceStrategy.HYBRID
    enable_tatoeba: bool = True
    enable_cefrlex: bool = True
    enable_merlin: bool = True
    enable_common_voice: bool = True
    max_external_results: int = 50
    timeout_seconds: float = 10.0
    use_cache: bool = True


@dataclass
class ResolvedVocabulary:
    """Result of vocabulary resolution."""
    words: list[VocabularyEntry]
    source: str  # 'local', 'external', 'hybrid'
    enriched_count: int = 0
    warnings: list[str] = field(default_factory=list)


@dataclass
class ResolvedSentences:
    """Result of sentence resolution."""
    sentences: list[dict[str, Any]]
    source: str
    count: int
    warnings: list[str] = field(default_factory=list)


@dataclass
class ResolvedAudio:
    """Result of audio resolution."""
    clips: list[dict[str, Any]]
    source: str
    count: int
    warnings: list[str] = field(default_factory=list)


class EducationalResourceResolver:
    """
    Central resolver for educational resources.
    
    Implements fallback logic:
    1. Try external sources if enabled and available
    2. Fall back to local curriculum on failure
    3. Never break the application due to external failures
    
    Usage:
        resolver = EducationalResourceResolver()
        
        # Get vocabulary with external enrichment
        vocab = resolver.get_vocabulary("en-GB", "A1", topic="greetings")
        
        # Get example sentences
        sentences = resolver.get_example_sentences("water", "en-GB")
        
        # Get listening materials
        audio = resolver.get_listening_materials("en-GB", "A2")
    """
    
    def __init__(self, config: ResourceConfig | None = None):
        """
        Initialize the resolver.
        
        Args:
            config: Optional configuration override
        """
        self.config = config or ResourceConfig()
        self.cache = ResourceCache() if self.config.use_cache else None
        
        # Initialize adapters
        cache = self.cache
        self.tatoeba = TatoebaAdapter(cache) if self.config.enable_tatoeba else None
        self.cefrlex = CEFRLexAdapter(cache) if self.config.enable_cefrlex else None
        self.merlin = MerlinAdapter(cache) if self.config.enable_merlin else None
        self.common_voice = CommonVoiceAdapter(cache) if self.config.enable_common_voice else None
        
        logger.info(f"EducationalResourceResolver initialized with strategy={self.config.strategy.value}")
    
    def get_vocabulary(
        self,
        target_language: str,
        cefr_level: CEFRLevel,
        topic: str | None = None,
        limit: int = 30,
    ) -> ResolvedVocabulary:
        """
        Get vocabulary words with optional external enrichment.
        
        Args:
            target_language: Language code (e.g., 'en-GB')
            cefr_level: CEFR level
            topic: Optional topic filter
            limit: Maximum number of words
            
        Returns:
            ResolvedVocabulary with words and source information
        """
        warnings = []
        local_words = []
        external_words = []
        
        # Strategy: LOCAL_ONLY
        if self.config.strategy == SourceStrategy.LOCAL_ONLY:
            local_words = self._get_local_vocabulary(target_language, cefr_level, topic, limit)
            return ResolvedVocabulary(
                words=local_words,
                source="local",
                warnings=warnings,
            )
        
        # Strategy: EXTERNAL_ONLY or HYBRID or EXTERNAL_PRIMARY
        if self.cefrlex and self.config.strategy != SourceStrategy.LOCAL_ONLY:
            try:
                lang_code = target_language.split('-')[0]
                cefr_words = self.cefrlex.fetch(
                    language=lang_code,
                    cefr_level=cefr_level,
                    limit=limit,
                )
                
                # Convert to internal VocabularyEntry format
                for cw in cefr_words:
                    entry = VocabularyEntry(
                        word=cw.word,
                        pos=cw.pos or "noun",
                        definition=cw.definition or "",
                        example=cw.example or "",
                        frequency_rank=cw.frequency_rank,
                    )
                    external_words.append(entry)
                
                logger.debug(f"Fetched {len(external_words)} external vocabulary words")
                
            except Exception as e:
                logger.warning(f"CEFRLex failed, using local fallback: {e}")
                warnings.append(f"External vocabulary unavailable: {e}")
        
        # Get local vocabulary for hybrid or fallback
        if (self.config.strategy in (SourceStrategy.HYBRID, SourceStrategy.LOCAL_ONLY) or 
            not external_words):
            local_words = self._get_local_vocabulary(target_language, cefr_level, topic, limit)
        
        # Merge results based on strategy
        if self.config.strategy == SourceStrategy.EXTERNAL_ONLY:
            final_words = external_words or local_words
            source = "external" if external_words else "local_fallback"
        elif self.config.strategy == SourceStrategy.HYBRID:
            # Merge without duplicates
            merged = self._merge_vocabulary(local_words, external_words)
            final_words = merged[:limit]
            source = "hybrid" if external_words else "local"
        elif self.config.strategy == SourceStrategy.EXTERNAL_PRIMARY:
            final_words = external_words or local_words
            source = "external" if external_words else "local_fallback"
        else:  # LOCAL_ONLY
            final_words = local_words
            source = "local"
        
        enriched_count = len([w for w in final_words if w.example])
        
        return ResolvedVocabulary(
            words=final_words,
            source=source,
            enriched_count=enriched_count,
            warnings=warnings,
        )
    
    def get_example_sentences(
        self,
        word: str,
        target_language: str,
        native_language: str | None = None,
        limit: int = 10,
    ) -> ResolvedSentences:
        """
        Get example sentences for a word from external sources.
        
        Args:
            word: The word to find examples for
            target_language: Target language code
            native_language: User's native language for translations
            limit: Maximum number of sentences
            
        Returns:
            ResolvedSentences with sentences and source information
        """
        warnings = []
        
        # Try Tatoeba if enabled
        if self.tatoeba:
            try:
                lang_code = target_language.split('-')[0][:3]
                native_code = None
                if native_language:
                    native_code = native_language.split('-')[0][:3]
                
                sentences = self.tatoeba.fetch(
                    query=word,
                    target_language=lang_code,
                    translation_language=native_code,
                    limit=limit,
                )
                
                if sentences:
                    # Convert to dict format for API response
                    result_sentences = []
                    for sent in sentences:
                        sent_dict = {
                            "text": sent.text,
                            "language": sent.language,
                            "translations": sent.translations,
                            "audio_available": sent.audio_available,
                            "source": "tatoeba",
                        }
                        
                        # Download audio if available
                        if sent.id and sent.audio_available:
                            audio_path = self.tatoeba.download_audio(sent.id, lang_code)
                            if audio_path:
                                sent_dict["audio_path"] = audio_path
                        
                        result_sentences.append(sent_dict)
                    
                    return ResolvedSentences(
                        sentences=result_sentences,
                        source="tatoeba",
                        count=len(result_sentences),
                        warnings=warnings,
                    )
                    
            except Exception as e:
                logger.warning(f"Tatoeba failed for word '{word}': {e}")
                warnings.append(f"Example sentences unavailable: {e}")
        
        # Fallback: no sentences (don't mock)
        return ResolvedSentences(
            sentences=[],
            source="none",
            count=0,
            warnings=warnings,
        )
    
    def get_listening_materials(
        self,
        target_language: str,
        cefr_level: CEFRLevel,
        limit: int = 10,
    ) -> ResolvedAudio:
        """
        Get listening materials from external sources.
        
        Args:
            target_language: Target language code
            cefr_level: CEFR level
            limit: Maximum number of clips
            
        Returns:
            ResolvedAudio with clips and source information
        """
        warnings = []
        clips = []
        
        # Try Common Voice first
        if self.common_voice:
            try:
                lang_code = target_language.split('-')[0]
                audio_clips = self.common_voice.fetch(
                    language=lang_code,
                    cefr_level=cefr_level,
                    limit=limit,
                )
                
                for clip in audio_clips:
                    clip_dict = {
                        "text": clip.text,
                        "language": clip.language,
                        "source": "common_voice",
                        "clip_id": clip.clip_id,
                    }
                    
                    # Try to download audio on-demand
                    if clip.clip_id:
                        audio_path = self.common_voice.download_clip(clip.clip_id, lang_code)
                        if audio_path:
                            clip_dict["audio_path"] = audio_path
                    
                    clips.append(clip_dict)
                
            except Exception as e:
                logger.warning(f"Common Voice failed: {e}")
                warnings.append(f"Common Voice unavailable: {e}")
        
        # Also try Tatoeba for sentence audio
        if self.tatoeba and len(clips) < limit:
            try:
                lang_code = target_language.split('-')[0][:3]
                sentences = self.tatoeba.fetch(
                    query="",
                    target_language=lang_code,
                    limit=limit - len(clips),
                )
                
                for sent in sentences:
                    if sent.audio_available:
                        audio_path = None
                        if sent.id:
                            audio_path = self.tatoeba.download_audio(sent.id, lang_code)
                        
                        clip_dict = {
                            "text": sent.text,
                            "language": sent.language,
                            "translations": sent.translations,
                            "source": "tatoeba",
                            "audio_path": audio_path,
                        }
                        clips.append(clip_dict)
                        
            except Exception as e:
                logger.warning(f"Tatoeba audio failed: {e}")
                warnings.append(f"Tatoeba audio unavailable: {e}")
        
        source = "hybrid" if len(clips) > 0 else "none"
        
        return ResolvedAudio(
            clips=clips,
            source=source,
            count=len(clips),
            warnings=warnings,
        )
    
    def get_learner_examples(
        self,
        target_language: str,
        cefr_level: CEFRLevel,
        limit: int = 5,
    ) -> list[LearnerTextData]:
        """
        Get learner text examples from MERLIN corpus.
        
        Args:
            target_language: Target language code
            cefr_level: CEFR level
            limit: Maximum number of texts
            
        Returns:
            List of LearnerTextData objects
        """
        if not self.merlin:
            return []
        
        try:
            lang_code = target_language.split('-')[0]
            texts = self.merlin.fetch(
                language=lang_code,
                cefr_level=cefr_level,
                limit=limit,
            )
            return texts
            
        except Exception as e:
            logger.warning(f"MERLIN failed: {e}")
            return []
    
    def _get_local_vocabulary(
        self,
        target_language: str,
        cefr_level: CEFRLevel,
        topic: str | None,
        limit: int,
    ) -> list[VocabularyEntry]:
        """Get vocabulary from local curriculum."""
        try:
            # Try to get from local vocabulary sets
            if topic:
                vocab_set = local_get_vocabulary_set(target_language, f"{topic}_{cefr_level.lower()}")
                if vocab_set:
                    return vocab_set.words[:limit]
            
            # Fallback: get from curriculum
            curriculum = get_curriculum(target_language)
            words = []
            
            for level_units in curriculum.values():
                for unit in level_units:
                    if unit.level == cefr_level:
                        # Would need to fetch actual vocabulary here
                        # For now, return empty (local data structure varies)
                        pass
            
            return words
            
        except Exception as e:
            logger.error(f"Local vocabulary fetch failed: {e}")
            return []
    
    def _merge_vocabulary(
        self,
        local: list[VocabularyEntry],
        external: list[VocabularyEntry],
    ) -> list[VocabularyEntry]:
        """Merge local and external vocabulary, removing duplicates."""
        seen_words = set()
        merged = []
        
        # Add external first (usually richer)
        for word in external:
            if word.word.lower() not in seen_words:
                merged.append(word)
                seen_words.add(word.word.lower())
        
        # Add local (fill gaps)
        for word in local:
            if word.word.lower() not in seen_words:
                merged.append(word)
                seen_words.add(word.word.lower())
        
        return merged
    
    def get_stats(self) -> dict[str, Any]:
        """Get resolver and cache statistics."""
        stats = {
            "strategy": self.config.strategy.value,
            "enabled_adapters": [],
            "cache_stats": None,
        }
        
        if self.tatoeba:
            stats["enabled_adapters"].append("tatoeba")
        if self.cefrlex:
            stats["enabled_adapters"].append("cefrlex")
        if self.merlin:
            stats["enabled_adapters"].append("merlin")
        if self.common_voice:
            stats["enabled_adapters"].append("common_voice")
        
        if self.cache:
            stats["cache_stats"] = self.cache.get_stats()
        
        return stats
    
    def close(self):
        """Close all adapter sessions."""
        for adapter in [self.tatoeba, self.cefrlex, self.merlin, self.common_voice]:
            if adapter:
                adapter.close()

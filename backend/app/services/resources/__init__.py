"""
External Educational Resources Layer for JUBA LISAN.

This module provides a clean architecture for integrating external educational resources
while maintaining fallback to local curriculum data.

Architecture:
    API/Service Layer
        ↓
    ResourceResolver (decides local vs external vs hybrid)
        ↓
    Resource Adapters (one per source)
        ↓
    External Sources / Local Cache
"""

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
from .resolver import (
    EducationalResourceResolver,
    ResourceConfig,
    SourceStrategy,
    ResolvedVocabulary,
    ResolvedSentences,
    ResolvedAudio,
)
from .cache import ResourceCache

__all__ = [
    # Adapters
    "TatoebaAdapter",
    "CEFRLexAdapter",
    "MerlinAdapter",
    "CommonVoiceAdapter",
    # Data types
    "SentenceData",
    "VocabularyData",
    "AudioData",
    "LearnerTextData",
    # Resolver
    "EducationalResourceResolver",
    "ResourceConfig",
    "SourceStrategy",
    "ResolvedVocabulary",
    "ResolvedSentences",
    "ResolvedAudio",
    # Cache
    "ResourceCache",
]

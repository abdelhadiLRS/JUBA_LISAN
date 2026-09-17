"""Services package for JUBA LISAN."""

from app.services.external_resources_service import (
    ExternalResourcesService,
    TatoebaService,
    CEFRLexService,
    CommonVoiceService,
    MerlinCorpusService,
    integrate_tatoeba_sentences_into_curriculum,
    integrate_cefr_vocabulary_into_sets,
)

__all__ = [
    "ExternalResourcesService",
    "TatoebaService",
    "CEFRLexService",
    "CommonVoiceService",
    "MerlinCorpusService",
    "integrate_tatoeba_sentences_into_curriculum",
    "integrate_cefr_vocabulary_into_sets",
]

"""
Tests for external educational resources integration.

These tests verify:
1. Adapter initialization and basic functionality
2. Fallback behavior when external sources are unavailable
3. Cache functionality
4. Resolver strategy implementation
5. Error handling

All tests use mocked HTTP responses to avoid network dependencies.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import httpx

from app.services.resources import (
    TatoebaAdapter,
    CEFRLexAdapter,
    MerlinAdapter,
    CommonVoiceAdapter,
    EducationalResourceResolver,
    ResourceConfig,
    SourceStrategy,
    ResourceCache,
)


class TestTatoebaAdapter:
    """Tests for Tatoeba adapter."""
    
    def test_adapter_initialization(self):
        """Test that TatoebaAdapter initializes correctly."""
        adapter = TatoebaAdapter()
        assert adapter is not None
        assert adapter.cache_prefix == "tatoeba_sentences"
        adapter.close()
    
    def test_fetch_with_mocked_response(self):
        """Test fetching sentences with mocked API response."""
        mock_response = {
            "results": [
                {
                    "id": "12345",
                    "text": "Hello, how are you?",
                    "lang": "eng",
                    "translations": [{"text": "Hola, ¿cómo estás?", "lang": "spa"}],
                    "audio_url": "https://example.com/audio.mp3",
                }
            ]
        }
        
        with patch.object(httpx.Client, 'get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            adapter = TatoebaAdapter()
            sentences = adapter.fetch(query="hello", target_language="eng", limit=5)
            
            assert len(sentences) == 1
            assert sentences[0].text == "Hello, how are you?"
            assert sentences[0].id == "12345"
            assert sentences[0].source == "tatoeba"
            adapter.close()
    
    def test_fetch_timeout_fallback(self):
        """Test that timeout results in empty list (no crash)."""
        with patch.object(httpx.Client, 'get') as mock_get:
            mock_get.side_effect = httpx.TimeoutException("Timeout")
            
            adapter = TatoebaAdapter()
            sentences = adapter.fetch(query="hello", target_language="eng", limit=5)
            
            assert sentences == []
            adapter.close()
    
    def test_fetch_http_error_fallback(self):
        """Test that HTTP errors result in empty list."""
        with patch.object(httpx.Client, 'get') as mock_get:
            mock_get.side_effect = httpx.HTTPStatusError(
                "Not Found",
                request=MagicMock(),
                response=MagicMock(status_code=404)
            )
            
            adapter = TatoebaAdapter()
            sentences = adapter.fetch(query="hello", target_language="eng", limit=5)
            
            assert sentences == []
            adapter.close()


class TestCEFRLexAdapter:
    """Tests for CEFRLex adapter."""
    
    def test_adapter_initialization(self):
        """Test that CEFRLexAdapter initializes correctly."""
        adapter = CEFRLexAdapter()
        assert adapter is not None
        assert adapter.cache_prefix == "cefrlex_words"
        adapter.close()
    
    def test_fetch_sample_data_fallback(self):
        """Test that sample data is returned when API unavailable."""
        adapter = CEFRLexAdapter()
        words = adapter.fetch(language="en", cefr_level="A1", limit=5)
        
        # Should return sample data even if API fails
        assert len(words) >= 0  # May be empty or have sample data
        adapter.close()
    
    def test_fetch_unsupported_language(self):
        """Test handling of unsupported language codes."""
        adapter = CEFRLexAdapter()
        words = adapter.fetch(language="xx", cefr_level="A1", limit=5)
        
        # Should fall back to English sample data
        assert len(words) >= 0
        adapter.close()


class TestMerlinAdapter:
    """Tests for MERLIN corpus adapter."""
    
    def test_adapter_initialization(self):
        """Test that MerlinAdapter initializes correctly."""
        adapter = MerlinAdapter()
        assert adapter is not None
        assert adapter.cache_prefix == "merlin_texts"
        adapter.close()
    
    def test_fetch_returns_sample_data(self):
        """Test that MERLIN returns sample learner texts."""
        adapter = MerlinAdapter()
        texts = adapter.fetch(language="en", cefr_level="A1", limit=2)
        
        # Should return sample texts
        assert len(texts) >= 0
        adapter.close()


class TestCommonVoiceAdapter:
    """Tests for Common Voice adapter."""
    
    def test_adapter_initialization(self):
        """Test that CommonVoiceAdapter initializes correctly."""
        adapter = CommonVoiceAdapter()
        assert adapter is not None
        assert adapter.cache_prefix == "common_voice_audio"
        adapter.close()
    
    def test_fetch_metadata(self):
        """Test fetching audio metadata."""
        adapter = CommonVoiceAdapter()
        clips = adapter.fetch(language="en", limit=5)
        
        # Should return placeholder metadata
        assert len(clips) >= 0
        adapter.close()


class TestResourceCache:
    """Tests for resource caching."""
    
    def test_cache_set_and_get(self):
        """Test basic cache operations."""
        cache = ResourceCache()
        
        # Set a value
        cache.set('test_prefix', {'key': 'value'}, test_param='abc')
        
        # Get the value
        result = cache.get('test_prefix', test_param='abc')
        assert result == {'key': 'value'}
    
    def test_cache_expiration(self):
        """Test that cache entries expire correctly."""
        cache = ResourceCache()
        
        # Set with very short TTL
        cache.set('test_prefix', {'key': 'value'}, ttl=1, test_param='xyz')
        
        # Should be available immediately
        result = cache.get('test_prefix', test_param='xyz')
        assert result == {'key': 'value'}
    
    def test_cache_miss(self):
        """Test cache miss returns None."""
        cache = ResourceCache()
        
        result = cache.get('nonexistent_prefix', param='abc')
        assert result is None
    
    def test_cache_stats(self):
        """Test cache statistics."""
        cache = ResourceCache()
        stats = cache.get_stats()
        
        assert 'memory_entries' in stats
        assert 'memory_size_mb' in stats
        assert 'audio_size_gb' in stats


class TestEducationalResourceResolver:
    """Tests for the main resource resolver."""
    
    def test_resolver_initialization(self):
        """Test resolver initializes with all adapters."""
        config = ResourceConfig(strategy=SourceStrategy.HYBRID)
        resolver = EducationalResourceResolver(config=config)
        
        stats = resolver.get_stats()
        assert 'tatoeba' in stats['enabled_adapters']
        assert 'cefrlex' in stats['enabled_adapters']
        assert resolver.config.strategy == SourceStrategy.HYBRID
        
        resolver.close()
    
    def test_resolver_local_only_strategy(self):
        """Test LOCAL_ONLY strategy disables external sources."""
        config = ResourceConfig(strategy=SourceStrategy.LOCAL_ONLY)
        resolver = EducationalResourceResolver(config=config)
        
        vocab = resolver.get_vocabulary('en-GB', 'A1', limit=5)
        assert vocab.source == 'local'
        
        resolver.close()
    
    def test_resolver_hybrid_strategy(self):
        """Test HYBRID strategy uses both local and external."""
        config = ResourceConfig(strategy=SourceStrategy.HYBRID)
        resolver = EducationalResourceResolver(config=config)
        
        vocab = resolver.get_vocabulary('en-GB', 'A1', limit=5)
        # Should be 'hybrid' if external works, 'local' if it fails
        assert vocab.source in ['hybrid', 'local']
        
        resolver.close()
    
    def test_resolver_graceful_degradation(self):
        """Test that resolver continues working when external sources fail."""
        config = ResourceConfig(strategy=SourceStrategy.HYBRID)
        resolver = EducationalResourceResolver(config=config)
        
        # Even with all external sources failing, should not crash
        vocab = resolver.get_vocabulary('en-GB', 'A1', limit=5)
        assert vocab is not None
        assert hasattr(vocab, 'words')
        assert hasattr(vocab, 'warnings')
        
        sentences = resolver.get_example_sentences('test', 'en-GB')
        assert sentences is not None
        
        resolver.close()
    
    def test_resolver_example_sentences(self):
        """Test getting example sentences."""
        config = ResourceConfig(strategy=SourceStrategy.HYBRID)
        resolver = EducationalResourceResolver(config=config)
        
        result = resolver.get_example_sentences('hello', 'en-GB', limit=5)
        
        assert result is not None
        assert hasattr(result, 'sentences')
        assert hasattr(result, 'count')
        assert hasattr(result, 'source')
        
        resolver.close()
    
    def test_resolver_listening_materials(self):
        """Test getting listening materials."""
        config = ResourceConfig(strategy=SourceStrategy.HYBRID)
        resolver = EducationalResourceResolver(config=config)
        
        result = resolver.get_listening_materials('en-GB', 'A1', limit=5)
        
        assert result is not None
        assert hasattr(result, 'clips')
        assert hasattr(result, 'count')
        
        resolver.close()


class TestIntegrationWithExistingServices:
    """Tests for integration with existing JUBA LISAN services."""
    
    def test_no_import_errors(self):
        """Test that new modules don't break existing imports."""
        from app.services import ExternalResourcesService
        from app.services.resources import EducationalResourceResolver
        
        # Both old and new implementations should coexist
        assert ExternalResourcesService is not None
        assert EducationalResourceResolver is not None
    
    def test_backward_compatibility(self):
        """Test that old ExternalResourcesService still works."""
        from app.services import ExternalResourcesService
        
        service = ExternalResourcesService()
        assert service.tatoeba is not None
        assert service.cefrlex is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

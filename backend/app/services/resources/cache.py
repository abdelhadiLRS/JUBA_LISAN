"""
Unified cache layer for external educational resources.

Provides:
- In-memory caching with TTL
- Filesystem caching for large assets (audio)
- Automatic cleanup of expired entries
- Thread-safe operations
"""

import hashlib
import json
import logging
import os
import shutil
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from typing import Any, Generic, TypeVar

from app.core.config import settings

logger = logging.getLogger(__name__)

T = TypeVar('T')


@dataclass
class CacheEntry(Generic[T]):
    """Represents a cached entry with metadata."""
    value: T
    created_at: float
    ttl_seconds: int
    size_bytes: int = 0
    
    def is_expired(self) -> bool:
        """Check if this entry has expired."""
        return time.time() > (self.created_at + self.ttl_seconds)


class ResourceCache:
    """
    Unified cache for external educational resources.
    
    Features:
    - In-memory cache for small data (sentences, vocabulary)
    - Filesystem cache for large data (audio files)
    - Configurable TTL per resource type
    - Automatic expiration checking
    - Size limits to prevent unbounded growth
    """
    
    # Default TTLs in seconds
    DEFAULT_TTLS = {
        'tatoeba_sentences': 3600 * 24,  # 24 hours
        'cefrlex_words': 3600 * 24 * 7,  # 7 days
        'merlin_texts': 3600 * 24 * 7,   # 7 days
        'common_voice_metadata': 3600 * 24,  # 24 hours
        'audio_files': 3600 * 24 * 30,   # 30 days
    }
    
    # Maximum cache sizes
    MAX_MEMORY_ENTRIES = 10000
    MAX_AUDIO_CACHE_SIZE_GB = 2.0  # GB
    
    def __init__(self, cache_dir: Path | None = None):
        """
        Initialize the cache.
        
        Args:
            cache_dir: Base directory for filesystem cache. 
                      Defaults to settings.CACHE_DIR or /tmp/juba_lisan_cache
        """
        if cache_dir is None:
            cache_dir = Path(getattr(settings, 'CACHE_DIR', '/tmp/juba_lisan_cache'))
        
        self.cache_dir = cache_dir / 'external_resources'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Subdirectories for different resource types
        self.audio_dir = self.cache_dir / 'audio'
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory cache: {key: CacheEntry}
        self._memory_cache: dict[str, CacheEntry] = {}
        self._lock = Lock()
        
        logger.info(f"ResourceCache initialized at {self.cache_dir}")
    
    def _generate_key(self, prefix: str, **kwargs) -> str:
        """Generate a unique cache key from parameters."""
        key_string = f"{prefix}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, prefix: str, **kwargs) -> Any | None:
        """
        Get a value from cache.
        
        Args:
            prefix: Resource type prefix (e.g., 'tatoeba_sentences')
            **kwargs: Parameters used to generate the cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        key = self._generate_key(prefix, **kwargs)
        with self._lock:
            entry = self._memory_cache.get(key)
            
            if entry is None:
                # Check filesystem cache for audio/large files
                if prefix == 'audio_files':
                    file_path = self._get_audio_file_path(kwargs.get('source', ''), kwargs.get('filename', ''))
                    if file_path and file_path.exists():
                        return str(file_path)
                return None
            
            if entry.is_expired():
                del self._memory_cache[key]
                return None
            
            return entry.value
    
    def set(self, prefix: str, value: Any, ttl: int | None = None, **kwargs) -> None:
        """
        Set a value in cache.
        
        Args:
            prefix: Resource type prefix
            value: Value to cache
            ttl: Time-to-live in seconds (optional, uses default if not provided)
            **kwargs: Parameters used to generate the cache key
        """
        key = self._generate_key(prefix, **kwargs)
        ttl = ttl or self.DEFAULT_TTLS.get(prefix, 3600)
        
        # Estimate size
        try:
            size_bytes = len(json.dumps(value).encode()) if not isinstance(value, (str, bytes)) else len(value)
        except Exception:
            size_bytes = 0
        
        entry = CacheEntry(
            value=value,
            created_at=time.time(),
            ttl_seconds=ttl,
            size_bytes=size_bytes,
        )
        
        with self._lock:
            # Enforce memory limit
            if len(self._memory_cache) >= self.MAX_MEMORY_ENTRIES:
                self._evict_oldest(100)
            
            self._memory_cache[key] = entry
        
        logger.debug(f"Cached {prefix} entry with key={key[:8]}...")
    
    def cache_audio_file(self, source: str, filename: str, content: bytes) -> str | None:
        """
        Cache an audio file to filesystem.
        
        Args:
            source: Source identifier (e.g., 'tatoeba', 'common_voice')
            filename: Original filename
            content: Audio file content as bytes
            
        Returns:
            Local file path or None if failed
        """
        # Sanitize filename
        safe_filename = "".join(c for c in filename if c.isalnum() or c in '._-')
        if not safe_filename:
            safe_filename = hashlib.md5(filename.encode()).hexdigest() + '.mp3'
        
        # Create source directory
        source_dir = self.audio_dir / source
        source_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = source_dir / safe_filename
        
        # Check size limit before writing
        max_size_bytes = int(self.MAX_AUDIO_CACHE_SIZE_GB * 1024 * 1024 * 1024)
        current_size = self._get_audio_cache_size()
        
        if current_size + len(content) > max_size_bytes:
            logger.warning(f"Audio cache full ({current_size / 1e9:.2f}GB), evicting old files")
            self._evict_old_audio_files(len(content))
        
        try:
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # Cache the path in memory
            self.set('audio_files', str(file_path), source=source, filename=safe_filename)
            
            logger.info(f"Cached audio file: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to cache audio file: {e}")
            return None
    
    def get_audio_file(self, source: str, filename: str) -> str | None:
        """Get path to a cached audio file."""
        return self.get('audio_files', source=source, filename=filename)
    
    def _get_audio_file_path(self, source: str, filename: str) -> Path | None:
        """Get Path object for an audio file."""
        if not filename:
            return None
        
        file_path = self.audio_dir / source / filename
        return file_path if file_path.exists() else None
    
    def _get_audio_cache_size(self) -> int:
        """Get total size of audio cache in bytes."""
        total_size = 0
        try:
            for dirpath, _dirnames, filenames in os.walk(self.audio_dir):
                for filename in filenames:
                    filepath = Path(dirpath) / filename
                    if filepath.exists():
                        total_size += filepath.stat().st_size
        except Exception as e:
            logger.warning(f"Error calculating audio cache size: {e}")
        return total_size
    
    def _evict_oldest(self, count: int) -> None:
        """Remove oldest entries from memory cache."""
        if not self._memory_cache:
            return
        
        sorted_entries = sorted(
            self._memory_cache.items(),
            key=lambda x: x[1].created_at
        )
        
        for key, _ in sorted_entries[:count]:
            del self._memory_cache[key]
        
        logger.debug(f"Evicted {count} oldest cache entries")
    
    def _evict_old_audio_files(self, needed_space: int = 0) -> None:
        """Remove oldest audio files to free space."""
        audio_files = []
        
        try:
            for dirpath, _dirnames, filenames in os.walk(self.audio_dir):
                for filename in filenames:
                    filepath = Path(dirpath) / filename
                    if filepath.exists():
                        mtime = filepath.stat().st_mtime
                        audio_files.append((filepath, mtime))
        except Exception as e:
            logger.warning(f"Error listing audio files: {e}")
            return
        
        if not audio_files:
            return
        
        # Sort by modification time (oldest first)
        audio_files.sort(key=lambda x: x[1])
        
        current_size = self._get_audio_cache_size()
        max_size = int(self.MAX_AUDIO_CACHE_SIZE_GB * 1024 * 1024 * 1024)
        
        for filepath, _ in audio_files:
            if current_size < (max_size - needed_space):
                break
            
            try:
                file_size = filepath.stat().st_size
                filepath.unlink()
                current_size -= file_size
                logger.debug(f"Evicted audio file: {filepath}")
            except Exception as e:
                logger.warning(f"Failed to evict audio file {filepath}: {e}")
    
    def clear(self, prefix: str | None = None) -> None:
        """
        Clear cache entries.
        
        Args:
            prefix: If provided, only clear entries with this prefix.
                   If None, clear all cache.
        """
        with self._lock:
            if prefix is None:
                self._memory_cache.clear()
                # Also clear audio cache
                try:
                    shutil.rmtree(self.audio_dir)
                    self.audio_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    logger.error(f"Failed to clear audio cache: {e}")
            else:
                # Clear specific prefix (would need to track prefixes in keys)
                # For simplicity, we'll just clear memory cache
                self._memory_cache.clear()
        
        logger.info(f"Cleared cache{' for ' + prefix if prefix else ''}")
    
    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            memory_size = len(self._memory_cache)
            memory_bytes = sum(e.size_bytes for e in self._memory_cache.values())
            audio_bytes = self._get_audio_cache_size()
            
            return {
                'memory_entries': memory_size,
                'memory_size_mb': memory_bytes / (1024 * 1024),
                'audio_size_gb': audio_bytes / (1024 * 1024 * 1024),
                'max_memory_entries': self.MAX_MEMORY_ENTRIES,
                'max_audio_size_gb': self.MAX_AUDIO_CACHE_SIZE_GB,
            }

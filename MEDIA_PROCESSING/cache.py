"""
Caching layer for image processing results.

This module provides caching functionality to avoid reprocessing images
that have already been processed with the same parameters.
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class ImageCache:
    """Cache for image processing results."""

    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize the cache.

        Args:
            cache_dir: Directory for cache files. If None, uses .cache in current dir.
        """
        if cache_dir is None:
            cache_dir = os.path.join(os.getcwd(), '.image_cache')
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / 'cache.json'

        # Load existing cache
        self.cache: Dict[str, Dict[str, Any]] = {}
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
            except Exception:
                self.cache = {}

    def _get_cache_key(
        self,
        image_path: str,
        operation: str,
        params: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a cache key for an operation.

        Args:
            image_path: Path to the image
            operation: Operation name (e.g., 'upscale', 'resize')
            params: Operation parameters

        Returns:
            Cache key string
        """
        # Get file modification time for cache invalidation
        try:
            mtime = os.path.getmtime(image_path)
        except OSError:
            mtime = 0

        # Create hash from operation and params
        param_str = json.dumps(params or {}, sort_keys=True)
        key_data = f"{image_path}:{mtime}:{operation}:{param_str}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(
        self,
        image_path: str,
        operation: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached result if available.

        Args:
            image_path: Path to the image
            operation: Operation name
            params: Operation parameters

        Returns:
            Cached result dict or None if not found
        """
        key = self._get_cache_key(image_path, operation, params)
        return self.cache.get(key)

    def set(
        self,
        image_path: str,
        operation: str,
        result: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Cache a processing result.

        Args:
            image_path: Path to the image
            operation: Operation name
            result: Result dictionary to cache
            params: Operation parameters
        """
        key = self._get_cache_key(image_path, operation, params)
        self.cache[key] = result

        # Save cache to disk
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception:
            pass  # Cache write failure is not critical

    def clear(self) -> None:
        """Clear all cached results."""
        self.cache = {}
        if self.cache_file.exists():
            self.cache_file.unlink()

    def cleanup(self, max_age_days: int = 30) -> int:
        """
        Remove old cache entries.

        Args:
            max_age_days: Maximum age in days for cache entries

        Returns:
            Number of entries removed
        """
        # Simple implementation - just clear if cache is too large
        if len(self.cache) > 1000:
            self.clear()
            return len(self.cache)
        return 0


# Global cache instance
_global_cache: Optional[ImageCache] = None


def get_cache(cache_dir: Optional[str] = None) -> ImageCache:
    """
    Get the global cache instance.

    Args:
        cache_dir: Cache directory (only used on first call)

    Returns:
        ImageCache instance
    """
    global _global_cache
    if _global_cache is None:
        _global_cache = ImageCache(cache_dir)
    return _global_cache


def cache_image_result(
    image_path: str,
    operation: str,
    result: Dict[str, Any],
    params: Optional[Dict[str, Any]] = None
) -> None:
    """
    Cache an image processing result.

    Args:
        image_path: Path to the image
        operation: Operation name
        result: Result dictionary
        params: Operation parameters
    """
    cache = get_cache()
    cache.set(image_path, operation, result, params)


def get_cached_result(
    image_path: str,
    operation: str,
    params: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """
    Get a cached image processing result.

    Args:
        image_path: Path to the image
        operation: Operation name
        params: Operation parameters

    Returns:
        Cached result or None
    """
    cache = get_cache()
    return cache.get(image_path, operation, params)

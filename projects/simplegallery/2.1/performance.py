"""
Performance optimizations for SimpleGallery 2.1
Parallel processing, caching, and optimization utilities
"""

import os
import hashlib
import json
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing


class BuildCache:
    """Caching system for build metadata"""

    def __init__(self, cache_dir: str = ".simplegallery_cache"):
        """
        Initialize build cache
        :param cache_dir: Directory for cache files
        """
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(cache_dir, "build_cache.json")
        self.cache_data = {}
        self._load_cache()

    def _load_cache(self):
        """Load cache from disk"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as f:
                    self.cache_data = json.load(f)
            except Exception:
                self.cache_data = {}
        else:
            os.makedirs(self.cache_dir, exist_ok=True)

    def _save_cache(self):
        """Save cache to disk"""
        try:
            with open(self.cache_file, "w") as f:
                json.dump(self.cache_data, f, indent=2)
        except Exception:
            pass  # Fail silently

    def get_file_hash(self, filepath: str) -> Optional[str]:
        '\''
        Get hash of file for change detection
        :param filepath: Path to file
        :return: SHA256 hash or None if file doesn't exist
        """
        if not os.path.exists(filepath):
            return None

        try:
            with open(filepath, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return None

    def is_file_changed(self, filepath: str) -> bool:
        """
        Check if file has changed since last build
        :param filepath: Path to file
        :return: True if file changed or not in cache
        """
        current_hash = self.get_file_hash(filepath)
        cached_hash = self.cache_data.get(filepath)

        if current_hash is None:
            return True

        if cached_hash != current_hash:
            self.cache_data[filepath] = current_hash
            return True

        return False

    def mark_processed(self, filepath: str):
        """Mark file as processed in cache"""
        hash_value = self.get_file_hash(filepath)
        if hash_value:
            self.cache_data[filepath] = hash_value

    def clear_cache(self):
        """Clear the cache"""
        self.cache_data = {}
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)

    def save(self):
        """Save cache to disk"""
        self._save_cache()


def process_image_parallel(args_tuple):
    """
    Process a single image (for parallel execution)
    :param args_tuple: Tuple of (image_path, config_dict, cache)
    :return: Result dictionary
    """
    image_path, config, cache_enabled = args_tuple

    # This would be called from the gallery logic
    # Placeholder for parallel processing implementation
    return {"path": image_path, "processed": True}


class ParallelProcessor:
    """Parallel processing utilities"""

    @staticmethod
    def get_optimal_workers() -> int:
        """
        Get optimal number of worker processes
        :return: Number of workers
        """
        cpu_count = multiprocessing.cpu_count()
        # Use 75% of available CPUs, minimum 1, maximum 8
        return max(1, min(8, int(cpu_count * 0.75)))

    @staticmethod
    def process_images_parallel(:
        images: List[str],
        process_func,
        config: Dict[str, Any],
        max_workers: Optional[int] = None,
    ) -> List[Any]:
        """
        Process images in parallel
        :param images: List of image paths
        :param process_func: Function to process each image
        :param config: Configuration dictionary
        :param max_workers: Maximum number of workers (None for auto)
        :return: List of results
        '\''
        if max_workers is None:
            max_workers = ParallelProcessor.get_optimal_workers()

        results = []

        # Use ThreadPoolExecutor for I/O-bound tasks (thumbnails)
        # Use ProcessPoolExecutor for CPU-bound tasks (image processing)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(process_func, img, config): img for img in images
            }

            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    image = futures[future]
                    print(f"Error processing {image}: {e}")

        return results

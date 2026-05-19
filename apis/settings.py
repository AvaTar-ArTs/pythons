# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"

# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080

import asyncio
import logging
import re
from functools import lru_cache, wraps
from pathlib import Path
from typing import Any, Dict, List, Tuple

import aiohttp
from rich.console import Console

logger = logging.getLogger(__name__)


# =============================================================================
# HTTP Utilities
# =============================================================================

async def async_request(url: str, session: aiohttp.ClientSession) -> str:
    """Async HTTP request."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logger.error(f"Async request failed: {e}")
        return None


async def process_urls(urls: List[str]) -> List[str]:
    """Process multiple URLs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [async_request(url, session) for url in urls]
        return await asyncio.gather(*tasks)


# =============================================================================
# Decorators
# =============================================================================

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper


def retry_decorator(max_retries=3):
    """Decorator to retry function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper
    return decorator


# =============================================================================
# Base Processor
# =============================================================================

from abc import ABC, abstractmethod


class BaseProcessor(ABC):
    """Abstract base class for processors."""

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


# =============================================================================
# Singleton Metaclass
# =============================================================================

import threading


class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# =============================================================================
# Configuration
# =============================================================================

# SECURITY NOTE: This file previously contained eval() calls copied from
# config/crawl.py (e.g. eval(checks["type"])(value)). Those were dead code
# fragments from a corrupted file merge. The safe type-conversion logic lives
# in config/crawl.py via _SAFE_TYPE_MAP and _safe_type_convert().


class Config:
    """Configuration class for global variables."""
    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1024 * 1024
    GB_SIZE = 1024 * 1024 * 1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9 * 1024 * 1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    cache = {}
    logger = logging.getLogger(__name__)
    console = Console()


# =============================================================================
# Input Validation
# =============================================================================

def validate_input(data, validators) -> bool:
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


# =============================================================================
# Memoization
# =============================================================================

def memoize(func) -> Any:
    """Memoization decorator."""
    cache = {}

    def wrapper(*args, **kwargs) -> Any:
        key = args + tuple(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper

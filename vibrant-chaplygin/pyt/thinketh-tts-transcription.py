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
import aiohttp

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


from functools import wraps

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

def retry_decorator(max_retries = 3):
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


from abc import ABC, abstractmethod

@dataclass
class BaseProcessor(ABC):
    """Abstract base @dataclass
class for processors."""

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


@dataclass
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

from docx import Document
from dotenv import load_dotenv
from functools import lru_cache
from openai import OpenAI
from pathlib import Path
from pydub import AudioSegment
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import logging
import os
import re

@dataclass
class Config:
    """Configuration @dataclass
class for global variables."""
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
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1048576
    GB_SIZE = 1073741824
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9437184
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    logger = logging.getLogger(__name__)
    DOCX_PATH = Path("~/Downloads/Compressed/thinketh_tts_package/AS-A-MAN-THINKETH-nonformat.docx")
    OUT_DIR = Path("~/Downloads/Compressed/thinketh_tts_package/output_mp3")
    MODEL = "gpt-4o-mini-tts"
    VOICE = "sage"   # try "alloy", "verse", or "cove" if you like different timbres
    CHAPTERS = [
    CHUNK_SIZE = 6000  # ~1500 tokens (safe)
    doc = Document(docx_path)
    t = t.replace("\\\r\\\n", "\\\n").replace("\\\r", "\\\n")
    t = re.sub(r"\\s+", " ", t)
    joined = "\\\n".join(paragraphs)
    parts = []
    pattern = re.compile(rf"\\\b{re.escape(title)}\\\b", re.I)
    match = pattern.search(joined)
    start = match.end()
    end = None
    nxt = re.search(rf"\\\b{re.escape(next_title)}\\\b", joined[start:], re.I)
    end = start + nxt.start()
    body = joined[start:end].strip() if end else joined[start:].strip()
    # paragraphs = re.split(r'(?<=\n)\n(?=\S)', body)  # Split on double newlines
    paragraphs = body.split('\n\n')  # Simple split
    current = para
    full_audio = AudioSegment.empty()
    response = client.audio.speech.create(
    model = model,
    voice = voice,
    input = chunk,
    response_format = "mp3"
    temp_chunk_path = out_path.parent / f"{out_path.stem}_part{i}.mp3"
    segment = AudioSegment.from_mp3(temp_chunk_path)
    client = OpenAI()
    paragraphs = read_docx_text(DOCX_PATH)
    chapters = extract_chapters(paragraphs)
    slug = f"{idx:02d}-{slugify(title)}"
    mp3_path = OUT_DIR / f"{slug}.mp3"
    @lru_cache(maxsize = 128)
    load_dotenv(Path.home() / ".env", override = False)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    chunks, current = [], ""
    current + = " " + para
    full_audio + = segment
    full_audio.export(out_path, format = "mp3")
    @lru_cache(maxsize = 128)
    OUT_DIR.mkdir(parents = True, exist_ok


# Constants



async def validate_input(data, validators):
def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
def memoize(func): -> Any
    """Memoization decorator."""

    async def wrapper(*args, **kwargs):
    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper


# Constants


@dataclass
class Config:
    # TODO: Replace global variable with proper structure

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
thinketh_tts.py
Text-to-Speech generator for 'As A Man Thinketh' (James Allen)

Features:
 - Reads DOCX
 - Splits into chapters automatically
 - Handles token limits by chunking text
 - Merges all chunks into one MP3 per chapter
 - Skips already completed files
"""


# ---------------- CONFIG ---------------- #
    "Foreword",
    "Thought and Character",
    "Effect of Thought on Circumstances",
    "Effect of Thought on Health and the Body",
    "Thought and Purpose",
    "The Thought-Factor in Achievement",
    "Visions and Ideals",
    "Serenity",
]
# ---------------------------------------- #


async def load_env():
def load_env(): -> Any
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Missing OPENAI_API_KEY in ~/.env")


async def read_docx_text(docx_path: Path):
def read_docx_text(docx_path: Path): -> Any
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]


async def normalize_text(t: str) -> str:
def normalize_text(t: str) -> str:
    return t.strip()


async def slugify(s: str) -> str:
def slugify(s: str) -> str:
    return re.sub(r"[^\\w\-]+", "-", s.strip().lower()).strip("-")


async def extract_chapters(paragraphs):
def extract_chapters(paragraphs): -> Any
    """Divide text by known chapter titles."""
    for i, title in enumerate(CHAPTERS):
        if not match:
            continue
        for next_title in CHAPTERS[i + 1:]:
            if nxt:
                break
        parts.append((title, normalize_text(body)))
    if not parts:
        return [("Full Text", normalize_text(joined))]
    return parts


async def synthesize_to_mp3(client, text: str, out_path: Path, model: str, voice: str):
def synthesize_to_mp3(client, text: str, out_path: Path, model: str, voice: str): -> Any
    """
    Split long text into chunks, synthesize each, then merge into one MP3.
    """

    for para in paragraphs:
        if len(current) + len(para) > CHUNK_SIZE:
            chunks.append(current.strip())
        else:
    if current.strip():
        chunks.append(current.strip())

    logger.info(f"    ↳ Splitting into {len(chunks)} chunks")


    for i, chunk in enumerate(chunks, start = 1):
        logger.info(f"      🗣️ Chunk {i}/{len(chunks)} ({len(chunk)} chars)")
        )
        temp_chunk_path.write_bytes(response.read())

        os.remove(temp_chunk_path)



async def main():
def main(): -> Any
    load_env()

    logger.info(f"📖 Reading {DOCX_PATH.name}...")
    logger.info(f"🎬 Found {len(chapters)} chapters.")

    for idx, (title, text) in enumerate(chapters):

        if mp3_path.exists():
            logger.info(f"✅ Skipping already done: {mp3_path.name}")
            continue

        logger.info(f"🔊 Synthesizing: {title} → {mp3_path.name}")
        try:
            synthesize_to_mp3(client, text, mp3_path, MODEL, VOICE)
            logger.info(f"🎧 Saved: {mp3_path.name}")
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            logger.info(f"⚠️ Error while processing {title}: {e}")
            break

    logger.info(f"\\\n✅ All done! Files saved in: {OUT_DIR}")


if __name__ == "__main__":
    main()

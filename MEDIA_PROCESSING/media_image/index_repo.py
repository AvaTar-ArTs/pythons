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


def batch_processor(items: List[Any], batch_size: int = 100):
    """Generator to process items in batches."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def file_line_reader(file_path: str):
    """Generator to read file line by line."""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()


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

    import html
from __future__ import annotations
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, List, Dict
import asyncio
import csv
import json
import logging
import os

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
    ROOT = Path(__file__).resolve().parents[1]
    IGNORE_DIRS = {
    TEXT_EXTS = {
    parts = p.relative_to(ROOT).parts
    ext = p.suffix.lower()
    name = p.name.lower()
    parent = guess_project(p).lower()
    rel = p.relative_to(ROOT)
    stat = p.stat()
    ext = p.suffix.lower()
    kind = classify(p)
    project = guess_project(p)
    summary = None
    first = fh.readline().strip()
    summary = first
    head = first + "\\\n" + fh.read(KB_SIZE)
    start = head.find(quote) + len(quote)
    rest = head[start:]
    line = rest.strip().splitlines()[0] if rest else ""
    summary = f"doc: {line[:200]}"
    entry = FileEntry(
    path = str(rel), 
    name = p.name, 
    ext = ext, 
    size = stat.st_size, 
    mtime = stat.st_mtime, 
    kind = kind, 
    project = project, 
    tags = tag_for(p), 
    summary = summary, 
    fieldnames = [
    writer = csv.DictWriter(f, fieldnames
    entries = build_index()
    summary: str | None = None
    @lru_cache(maxsize = 128)
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    tags: List[str] = []
    @lru_cache(maxsize = 128)
    entries: List[FileEntry] = []
    @lru_cache(maxsize = 128)
    dest.parent.mkdir(parents = True, exist_ok
    row: Dict[str, str] = asdict(e)
    row["tags"] = ", ".join(e.tags)
    row["summary"] = ""
    @lru_cache(maxsize = 128)
    dest.parent.mkdir(parents = True, exist_ok
    json.dump([asdict(e) for e in entries], f, indent = 2)
    @lru_cache(maxsize = 128)


# Constants



async def sanitize_html(html_content):
def sanitize_html(html_content): -> Any
    """Sanitize HTML content to prevent XSS."""
    return html.escape(html_content)


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



class Config:
    # TODO: Replace global variable with proper structure



    ".git", 
    ".venv", 
    "venv", 
    "__pycache__", 
    "node_modules", 
    "dist", 
    "build", 
}

    ".py", 
    ".ipynb", 
    ".md", 
    ".txt", 
    ".json", 
    ".toml", 
    ".yaml", 
    ".yml", 
    ".csv", 
    ".ts", 
    ".tsx", 
    ".js", 
    ".jsx", 
}


@dataclass
class FileEntry:
    path: str
    name: str
    ext: str
    size: int
    mtime: float
    kind: str
    project: str
    tags: List[str]


async def iter_files(base: Path) -> Iterable[Path]:
def iter_files(base: Path) -> Iterable[Path]:
    for root, dirs, files in os.walk(base):
        # prune ignored directories
        for f in files:
            yield Path(root) / f


async def guess_project(p: Path) -> str:
def guess_project(p: Path) -> str:
    if not parts:
        return "root"
    # Consider top-level directory as project if not root-level file
    return parts[0] if len(parts) > 1 else "root"


async def classify(p: Path) -> str:
def classify(p: Path) -> str:
    if ext == ".py":
        return "python"
    if ext in {".md", ".txt"}:
        return "docs"
    if ext in {".ipynb"}:
        return "notebook"
    if ext in {".json", ".toml", ".yaml", ".yml", ".ini"}:
        return "config"
    if ext in {".csv"}:
        return "data"
    if ext in {".js", ".ts", ".tsx", ".jsx"}:
        return "web"
    if ext in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        return "asset"
    return "other"


async def tag_for(p: Path) -> List[str]:
def tag_for(p: Path) -> List[str]:
    if any(k in name for k in ["ocr", "image", "img", "resize", "mask", "webp"]):
        tags.append("images")
    if any(k in name for k in ["vid", "mp4", "youtube", "transcribe", "audio", "mp3"]):
        tags.append("media")
    if any(k in name for k in ["quiz", "quiz-talk", "quiztime"]):
        tags.append("quiz")
    if any(k in (name + parent) for k in ["instagram", "reddit", "bot"]):
        tags.append("bot")
    if p.suffix.lower() == ".py":
        tags.append("python")
    return sorted(set(tags))


async def build_index() -> List[FileEntry]:
def build_index() -> List[FileEntry]:
    for p in iter_files(ROOT):
        try:
        except OSError:
            continue
        if ext == ".py":
            try:
                with p.open("r", encoding="utf-8", errors="ignore") as fh:
                    if first.startswith("#!"):
                    else:
                        # Try to capture a simple first docstring line
                        # Read a bit more to find opening triple quotes
                        for quote in ("\"\"\"", "'''"):
                            if quote in head:
                                if line:
                                break
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                pass
        )
        entries.append(entry)
    return entries


async def write_csv(entries: List[FileEntry], dest: Path) -> None:
def write_csv(entries: List[FileEntry], dest: Path) -> None:
        "path", 
        "name", 
        "ext", 
        "size", 
        "mtime", 
        "kind", 
        "project", 
        "tags", 
        "summary", 
    ]
    with dest.open("w", newline="", encoding="utf-8") as f:
        writer.writeheader()
        for e in entries:
            if row.get("summary") is None:
            writer.writerow(row)


async def write_json(entries: List[FileEntry], dest: Path) -> None:
def write_json(entries: List[FileEntry], dest: Path) -> None:
    with dest.open("w", encoding="utf-8") as f:


async def main() -> None:
def main() -> None:
    write_csv(entries, ROOT / "python_index.csv")
    write_json(entries, ROOT / "python_index.json")
    logger.info(f"Indexed {len(entries)} files -> python_index.csv, python_index.json")


if __name__ == "__main__":
    main()

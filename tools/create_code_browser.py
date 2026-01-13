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

class Observer(ABC):
    """Observer interface."""
    @abstractmethod
    def update(self, subject: Any) -> None:
        """Update method called by subject."""
        pass

class Subject:
    """Subject class for observer pattern."""
    def __init__(self):
        self._observers: List[Observer] = []
        self._lock = threading.Lock()

    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        with self._lock:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observers."""
        with self._lock:
            for observer in self._observers:
                try:
                    observer.update(self)
                except Exception as e:
                    logger.error(f"Observer notification failed: {e}")


class Factory:
    """Generic factory pattern implementation."""
    _creators = {}

    @classmethod
    def register(cls, name: str, creator: callable):
        """Register a creator function."""
        cls._creators[name] = creator

    @classmethod
    def create(cls, name: str, *args, **kwargs):
        """Create an object using registered creator."""
        if name not in cls._creators:
            raise ValueError(f"Unknown type: {name}")
        return cls._creators[name](*args, **kwargs)


@dataclass
class DependencyContainer:
    """Simple dependency injection container."""
    _services = {}

    @classmethod
    def register(cls, name: str, service: Any) -> None:
        """Register a service."""
        cls._services[name] = service

    @classmethod
    def get(cls, name: str) -> Any:
        """Get a service."""
        if name not in cls._services:
            raise ValueError(f"Service not found: {name}")
        return cls._services[name]


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
class Factory:
    """Generic factory pattern implementation."""
    _creators = {}

    @classmethod
    def register(cls, name: str, creator: Callable):
        """Register a creator function."""
        cls._creators[name] = creator

    @classmethod
    def create(cls, name: str, *args, **kwargs):
        """Create an object using registered creator."""
        if name not in cls._creators:
            raise ValueError(f"Unknown type: {name}")
        return cls._creators[name](*args, **kwargs)


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

    from {
    import html
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import base64
import json
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
    @lru_cache(maxsize = 128)
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
    subdirs = ["css", "js", "data", "images"]
    files_data = []
    categories = {}
    content = f.read()
    file_data = self.extract_file_metadata(py_file, content)
    category = self.get_category_from_path(py_file)
    relative_path = file_path.relative_to(self.base_path)
    name = file_path.stem
    size = file_path.stat().st_size
    lines = len(content.splitlines())
    docstring = self.extract_docstring(content)
    imports = self.extract_imports(content)
    functions = self.extract_functions(content)
    classes = self.extract_classes(content)
    preview_lines = content.splitlines()[:20]
    preview = '\\\n'.join(preview_lines)
    file_type = self.determine_file_type(content, name)
    keywords = self.extract_keywords(content, name)
    lines = content.splitlines()
    docstring_lines = []
    docstring_lines = []
    comment_lines = []
    imports = []
    lines = content.splitlines()
    line = line.strip()
    functions = []
    lines = content.splitlines()
    line = line.strip()
    func_name = line.split('(')[0].replace('def ', '').strip()
    classes = []
    lines = content.splitlines()
    line = line.strip()
    class_name = line.split('(')[0].replace('@dataclass
class ', '').strip()
    content_lower = content.lower()
    filename_lower = filename.lower()
    keywords = set()
    filename_words = re.findall(r'[a-zA-Z]+', filename.lower())
    tech_keywords = [
    content_lower = content.lower()
    relative_path = file_path.relative_to(self.base_path)
    path_parts = relative_path.parts
    html_content = f'''<!DOCTYPE html>
    options = []
    count = len(files)
    cards = []
    preview = file_data['preview']
    preview = preview[:500] + "..."
    type_icon = self.get_type_icon(file_data['file_type'])
    size_kb = file_data['size'] / KB_SIZE
    keywords_html = ''.join([f'<span class
    card_html = f'''
    icons = {
    css_content = '''
    css_file = self.browser_path / "css" / "style.css"
    js_content = '''
    js_file = self.browser_path / "js" / "script.js"
    data = {
    data_file = self.browser_path / "data" / "files_data.json"
    generator = CodeBrowserGenerator()
    async def __init__(self, base_path = "~/Documents/python"):
    self._lazy_loaded = {}
    self.base_path = Path(base_path)
    self.browser_path = self.base_path / "code_browser"
    self.html_path = self.browser_path / "index.html"
    self.browser_path.mkdir(exist_ok = True)
    (self.browser_path / subdir).mkdir(exist_ok = True)
    categories[category] = []
    files_data.sort(key = lambda x: x['name'].lower())
    <html lang = "en">
    <meta charset = "UTF-8">
    <meta name = "viewport" content
    <link rel = "stylesheet" href
    <link rel = "icon" href
    <link href = "https://fonts.googleapis.com/css2?family
    <link href = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel
    <div @dataclass
class = "app">
    <header @dataclass
class = "header">
    <div @dataclass
class = "header-content">
    <div @dataclass
class = "controls">
    <div @dataclass
class = "search-container">
    <input type = "text" id
    <div @dataclass
class = "search-icon">🔍</div>
    <div @dataclass
class = "filter-container">
    <select id = "categoryFilter">
    <option value = "">All Categories</option>
    <select id = "typeFilter">
    <option value = "">All Types</option>
    <option value = "transcription">Transcription</option>
    <option value = "analysis">Analysis</option>
    <option value = "youtube">YouTube</option>
    <option value = "image_processing">Image Processing</option>
    <option value = "video_processing">Video Processing</option>
    <option value = "audio_processing">Audio Processing</option>
    <option value = "web_tools">Web Tools</option>
    <option value = "data_processing">Data Processing</option>
    <option value = "testing">Testing</option>
    <option value = "setup">Setup</option>
    <option value = "organization">Organization</option>
    <option value = "utility">Utility</option>
    <button id = "sortBtn" class
    <div @dataclass
class = "stats">
    <div @dataclass
class = "stat">
    <span @dataclass
class = "stat-number">{len(files_data)}</span>
    <span @dataclass
class = "stat-label">Scripts</span>
    <div @dataclass
class = "stat">
    <span @dataclass
class = "stat-number">{len(categories)}</span>
    <span @dataclass
class = "stat-label">Categories</span>
    <div @dataclass
class = "stat">
    <span @dataclass
class = "stat-number" id
    <span @dataclass
class = "stat-label">Visible</span>
    <div @dataclass
class = "code-grid" id
    <div @dataclass
class = "modal" id
    <div @dataclass
class = "modal-content">
    <div @dataclass
class = "modal-header">
    <h2 id = "modalTitle">Script Name</h2>
    <button @dataclass
class = "close-btn" id
    <div @dataclass
class = "modal-body">
    <div @dataclass
class = "file-info">
    <div @dataclass
class = "info-item">
    <span @dataclass
class = "info-label">Path:</span>
    <span @dataclass
class = "info-value" id
    <div @dataclass
class = "info-item">
    <span @dataclass
class = "info-label">Lines:</span>
    <span @dataclass
class = "info-value" id
    <div @dataclass
class = "info-item">
    <span @dataclass
class = "info-label">Size:</span>
    <span @dataclass
class = "info-value" id
    <div @dataclass
class = "info-item">
    <span @dataclass
class = "info-label">Type:</span>
    <span @dataclass
class = "info-value" id
    <div @dataclass
class = "code-preview">
    <pre><code id = "modalCode" class
    <script src = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
    <script src = "js/script.js"></script>
    window.filesData = {json.dumps(files_data)};
    window.categories = {json.dumps(categories)};
    options.append(f'<option value = "{category}">{category} ({count})</option>')
    <div @dataclass
class = "code-card" data-category
    <div @dataclass
class = "card-header">
    <div @dataclass
class = "file-icon">{type_icon}</div>
    <div @dataclass
class = "file-info">
    <h3 @dataclass
class = "file-name">{file_data['name']}</h3>
    <p @dataclass
class = "file-path">{file_data['path']}</p>
    <div @dataclass
class = "file-stats">
    <span @dataclass
class = "lines">{file_data['lines']} lines</span>
    <span @dataclass
class = "size">{size_kb:.1f} KB</span>
    <div @dataclass
class = "card-body">
    <div @dataclass
class = "file-description">
    <div @dataclass
class = "keywords">
    <div @dataclass
class = "functions">
    <div @dataclass
class = "card-footer">
    <div @dataclass
class = "preview-code">
    <pre><code @dataclass
class = "language-python">{self.escape_html(preview[:DPI_300])}</code></pre>
    <button @dataclass
class = "view-code-btn" onclick
    this.files = window.filesData || [];
    this.categories = window.categories || {};
    this.filteredFiles = [...this.files];
    this.sortOrder = 'name';
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', (e) = > {
    const categoryFilter = document.getElementById('categoryFilter');
    categoryFilter.addEventListener('change', (e) = > {
    const typeFilter = document.getElementById('typeFilter');
    typeFilter.addEventListener('change', (e) = > {
    const sortBtn = document.getElementById('sortBtn');
    sortBtn.addEventListener('click', (e) = > {
    const closeModal = document.getElementById('closeModal');
    closeModal.addEventListener('click', (e) = > {
    const modal = document.getElementById('codeModal');
    modal.addEventListener('click', (e) = > {
    document.addEventListener('keydown', (e) = > {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const categoryFilter = document.getElementById('categoryFilter').value;
    const typeFilter = document.getElementById('typeFilter').value;
    this.filteredFiles = this.files.filter(file
    const matchesSearch = !searchTerm ||
    file.keywords.some(kw = > kw.toLowerCase().includes(searchTerm)) ||
    file.functions.some(fn = > fn.toLowerCase().includes(searchTerm));
    const matchesCategory = !categoryFilter || file.category
    const matchesType = !typeFilter || file.type
    const sortBtn = document.getElementById('sortBtn');
    this.sortOrder = 'lines';
    sortBtn.textContent = 'Sort by Lines';
    this.sortOrder = 'size';
    sortBtn.textContent = 'Sort by Size';
    this.sortOrder = 'name';
    sortBtn.textContent = 'Sort A-Z';
    this.filteredFiles.sort((a, b) = > {
    const grid = document.getElementById('codeGrid');
    grid.innerHTML = '';
    this.filteredFiles.forEach(file = > {
    const card = this.createFileCard(file);
    const cards = grid.querySelectorAll('.code-card');
    cards.forEach((card, index) = > {
    card.style.animationDelay = `${index * 0.1}s`;
    const card = document.createElement('div');
    card.className = 'code-card';
    const typeIcon = this.getTypeIcon(file.type);
    const sizeKb = (file.size / KB_SIZE).toFixed(1);
    const keywordsHtml = file.keywords.slice(0, 5).map(kw
    `<span @dataclass
class = "keyword">${kw}</span>`
    const functionsText = file.functions.length > 0 ?
    const preview = this.escapeHtml(file.preview.substring(0, DPI_DPI_300));
    card.innerHTML = `
    <div @dataclass
class = "card-header">
    <div @dataclass
class = "file-icon">${typeIcon}</div>
    <div @dataclass
class = "file-info">
    <h3 @dataclass
class = "file-name">${file.name}</h3>
    <p @dataclass
class = "file-path">${file.path}</p>
    <div @dataclass
class = "file-stats">
    <span @dataclass
class = "lines">${file.lines} lines</span>
    <span @dataclass
class = "size">${sizeKb} KB</span>
    <div @dataclass
class = "card-body">
    <div @dataclass
class = "file-description">
    <div @dataclass
class = "keywords">
    <div @dataclass
class = "functions">
    <div @dataclass
class = "card-footer">
    <div @dataclass
class = "preview-code">
    <pre><code @dataclass
class = "language-python">${preview}</code></pre>
    <button @dataclass
class = "view-code-btn" onclick
    const file = this.files.find(f
    const modal = document.getElementById('codeModal');
    const title = document.getElementById('modalTitle');
    const path = document.getElementById('modalPath');
    const lines = document.getElementById('modalLines');
    const size = document.getElementById('modalSize');
    const type = document.getElementById('modalType');
    const code = document.getElementById('modalCode');
    title.textContent = file.name;
    path.textContent = file.path;
    lines.textContent = file.lines;
    size.textContent = `${(file.size / KB_SIZE).toFixed(1)} KB`;
    type.textContent = file.type;
    code.textContent = file.preview;
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
    const modal = document.getElementById('codeModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
    const visibleCount = document.getElementById('visibleCount');
    visibleCount.textContent = this.filteredFiles.length;
    const icons = {
    const div = document.createElement('div');
    div.textContent = text;
    document.addEventListener('DOMContentLoaded', () = > {
    window.codeBrowser = new CodeBrowser();
    json.dump(data, f, indent = 2, ensure_ascii
    logger.info(" = " * 50)
    files_data, categories = self.scan_python_files()
    @lru_cache(maxsize = 128)


# Constants



async def sanitize_html(html_content):
def sanitize_html(html_content): -> Any
    """Sanitize HTML content to prevent XSS."""
    return html.escape(html_content)


async def safe_sql_query(query, params):
def safe_sql_query(query, params): -> Any
    """Execute SQL query safely with parameterized queries."""
    # Use parameterized queries to prevent SQL injection
    return execute_query(query, params)


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

@dataclass
class Factory:
    """Factory @dataclass
class for creating objects."""

    @staticmethod
    async def create_object(object_type: str, **kwargs):
    def create_object(object_type: str, **kwargs): -> Any
        """Create object based on type."""
        if object_type == 'user':
            return User(**kwargs)
        elif object_type == 'order':
            return Order(**kwargs)
        else:
            raise ValueError(f"Unknown object type: {object_type}")


# Constants


@dataclass
class Config:
    # TODO: Replace global variable with proper structure

#!/usr/bin/env python3
"""
Code Browser Generator
Creates a visual code browser similar to avatararts.org/dalle.html
Displays Python scripts as interactive cards with code previews
"""


@dataclass
class CodeBrowserGenerator:
    def __init__(self, base_path="~/Documents/python"): -> Any

    async def create_directory_structure(self):
    def create_directory_structure(self): -> Any
        """Create the code browser directory structure."""
        logger.info("📁 Creating code browser structure...")


        # Create subdirectories
        for subdir in subdirs:

        logger.info(f"✅ Created code browser structure in {self.browser_path}")

    async def scan_python_files(self):
    def scan_python_files(self): -> Any
        """Scan all Python files and extract metadata."""
        logger.info("🔍 Scanning Python files...")


        # Scan all Python files
        for py_file in self.base_path.rglob("*.py"):
            if py_file.is_file() and not py_file.name.startswith('.'):
                try:
                    # Read file content
                    with open(py_file, 'r', encoding='utf-8') as f:

                    # Extract metadata
                    files_data.append(file_data)

                    # Group by category
                    if category not in categories:
                    categories[category].append(file_data)

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                    logger.info(f"⚠️  Error reading {py_file}: {e}")

        # Sort files by name

        logger.info(f"✅ Found {len(files_data)} Python files across {len(categories)} categories")
        return files_data, categories

    async def extract_file_metadata(self, file_path, content):
    def extract_file_metadata(self, file_path, content): -> Any
        """Extract metadata from a Python file."""

        # Extract basic info

        # Extract docstring

        # Extract imports

        # Extract functions and classes

        # Extract first few lines for preview

        # Determine file type/purpose

        # Extract keywords

        return {
            'id': str(relative_path).replace('/', '_').replace('.', '_'), 
            'name': name, 
            'path': str(relative_path), 
            'full_path': str(file_path), 
            'size': size, 
            'lines': lines, 
            'docstring': docstring, 
            'imports': imports, 
            'functions': functions, 
            'classes': classes, 
            'preview': preview, 
            'file_type': file_type, 
            'keywords': keywords, 
            'category': self.get_category_from_path(file_path), 
            'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        }

    async def extract_docstring(self, content):
    def extract_docstring(self, content): -> Any
        """Extract docstring from Python file."""
        # Look for module docstring
        if lines and lines[0].strip().startswith('"""'):
            # Multi-line docstring
            for i, line in enumerate(lines[1:], 1):
                if '"""' in line:
                    docstring_lines.append(line.split('"""')[0])
                    break
                docstring_lines.append(line)
            return ' '.join(docstring_lines).strip()
        elif lines and lines[0].strip().startswith("'''"):
            # Multi-line docstring with single quotes
            for i, line in enumerate(lines[1:], 1):
                if "'''" in line:
                    docstring_lines.append(line.split("'''")[0])
                    break
                docstring_lines.append(line)
            return ' '.join(docstring_lines).strip()
        elif lines and lines[0].strip().startswith('#'):
            # Comment-based description
            for line in lines:
                if line.strip().startswith('#'):
                    comment_lines.append(line.strip()[1:].strip())
                else:
                    break
            return ' '.join(comment_lines).strip()

        return ""

    async def extract_imports(self, content):
    def extract_imports(self, content): -> Any
        """Extract import statements."""

        for line in lines:
            if line.startswith(('import ', 'from ')):
                imports.append(line)
                if len(imports) >= 10:  # Limit to first 10 imports
                    break

        return imports

    async def extract_functions(self, content):
    def extract_functions(self, content): -> Any
        """Extract function definitions."""

        for line in lines:
            if line.startswith('def ') and not line.startswith('def _'):
                functions.append(func_name)
                if len(functions) >= 5:  # Limit to first 5 functions
                    break

        return functions

    async def extract_classes(self, content):
    def extract_classes(self, content): -> Any
        """Extract @dataclass
class definitions."""

        for line in lines:
            if line.startswith('@dataclass
class ') and not line.startswith('@dataclass
class _'):
                classes.append(class_name)
                if len(classes) >= MAX_RETRIES:  # Limit to first MAX_RETRIES classes
                    break

        return classes

    async def determine_file_type(self, content, filename):
    def determine_file_type(self, content, filename): -> Any
        """Determine the type/purpose of the file."""

        # Check for specific patterns
        if 'transcription' in filename_lower or 'whisper' in content_lower:
            return 'transcription'
        elif 'analyze' in filename_lower or 'analysis' in filename_lower:
            return 'analysis'
        elif 'youtube' in filename_lower or 'youtube' in content_lower:
            return 'youtube'
        elif 'image' in filename_lower or 'pil' in content_lower or 'opencv' in content_lower:
            return 'image_processing'
        elif 'video' in filename_lower or 'moviepy' in content_lower:
            return 'video_processing'
        elif 'audio' in filename_lower or 'pyaudio' in content_lower:
            return 'audio_processing'
        elif 'web' in filename_lower or 'requests' in content_lower or 'scraping' in filename_lower:
            return 'web_tools'
        elif 'data' in filename_lower or 'pandas' in content_lower or 'numpy' in content_lower:
            return 'data_processing'
        elif 'test' in filename_lower or 'unittest' in content_lower:
            return 'testing'
        elif 'setup' in filename_lower or 'install' in filename_lower:
            return 'setup'
        elif 'migrate' in filename_lower or 'organize' in filename_lower:
            return 'organization'
        else:
            return 'utility'

    async def extract_keywords(self, content, filename):
    def extract_keywords(self, content, filename): -> Any
        """Extract relevant keywords from content and filename."""

        # Add filename words
        keywords.update(filename_words)

        # Add common Python/tech keywords
            'openai', 'whisper', 'gpt', 'ai', 'ml', 'transcription', 
            'youtube', 'video', 'audio', 'image', 'processing', 
            'web', 'scraping', 'requests', 'beautifulsoup', 
            'pandas', 'numpy', 'matplotlib', 'data', 
            'flask', 'django', 'fastapi', 'api', 
            'test', 'unittest', 'pytest', 'testing', 
            'migrate', 'organize', 'setup', 'install'
        ]

        for keyword in tech_keywords:
            if keyword in content_lower:
                keywords.add(keyword)

        return list(keywords)[:10]  # Limit to 10 keywords

    async def get_category_from_path(self, file_path):
    def get_category_from_path(self, file_path): -> Any
        """Get category from file path."""

        if len(path_parts) > 1:
            return path_parts[0]  # First directory is category
        else:
            return 'root'

    async def create_html(self, files_data, categories):
    def create_html(self, files_data, categories): -> Any
        """Create the main HTML file."""
        logger.info("📝 Creating HTML code browser...")

<head>
    <title>Python Code Browser</title>
</head>
<body>
        <!-- Header -->
                <h1>🐍 Python Code Browser</h1>
                <p>Explore {len(files_data)} Python scripts across {len(categories)} categories</p>
            </div>
        </header>

        <!-- Controls -->
            </div>
                    {self.generate_category_options(categories)}
                </select>
                </select>
            </div>
        </div>

        <!-- Stats -->
            </div>
            </div>
            </div>
        </div>

        <!-- Code Grid -->
            {self.generate_code_cards(files_data)}
        </div>

        <!-- Code Modal -->
                </div>
                        </div>
                        </div>
                        </div>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Pass data to JavaScript
    </script>
</body>
</html>
'''

        with open(self.html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info("✅ HTML code browser created")

    async def generate_category_options(self, categories):
    def generate_category_options(self, categories): -> Any
        """Generate category options for the filter."""
        for category, files in categories.items():
        return '\\\n'.join(options)

    async def generate_code_cards(self, files_data):
    def generate_code_cards(self, files_data): -> Any
        """Generate HTML for code cards."""

        for file_data in files_data:
            # Truncate preview
            if len(preview) > 500:

            # Get file type icon

            # Format size

            # Generate keywords HTML

                    </div>
                    </div>
                </div>

                        {file_data['docstring'][:200] if file_data['docstring'] else 'No description available'}
                    </div>

                        {keywords_html}
                    </div>

                        {', '.join(file_data['functions'][:MAX_RETRIES]) if file_data['functions'] else 'No functions'}
                    </div>
                </div>

                    </div>
                        View Full Code
                    </button>
                </div>
            </div>
            '''

            cards.append(card_html)

        return '\\\n'.join(cards)

    async def get_type_icon(self, file_type):
    def get_type_icon(self, file_type): -> Any
        """Get icon for file type."""
            'transcription': '🎤', 
            'analysis': '📊', 
            'youtube': '📺', 
            'image_processing': '🖼️', 
            'video_processing': '🎬', 
            'audio_processing': '🔊', 
            'web_tools': '🌐', 
            'data_processing': '📈', 
            'testing': '🧪', 
            'setup': '⚙️', 
            'organization': '📁', 
            'utility': '🔧'
        }
        return icons.get(file_type, '🐍')

    async def escape_html(self, text):
    def escape_html(self, text): -> Any
        """Escape HTML special characters."""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#39;'))

    async def create_css(self):
    def create_css(self): -> Any
        """Create CSS styles."""
        logger.info("🎨 Creating CSS styles...")

/* Code Browser Styles */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 DEFAULT_BATCH_SIZE%);
    min-height: 100vh;
    color: #333;
}

.app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Header */
.header {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    padding: 2rem 0;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.header-content h1 {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.header-content p {
    font-size: 1.2rem;
    color: #666;
    font-weight: 400;
}

/* Controls */
.controls {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    padding: 1.5rem 2rem;
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.search-container {
    position: relative;
    flex: 1;
    max-width: 400px;
}

#searchInput {
    width: DEFAULT_BATCH_SIZE%;
    padding: 0.75rem 1rem 0.75rem 3rem;
    border: 2px solid #e1e5e9;
    border-radius: 25px;
    font-size: 1rem;
    outline: none;
    transition: all 0.3s ease;
}

#searchInput:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #999;
    font-size: 1.2rem;
}

.filter-container {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

select, .sort-btn {
    padding: 0.75rem 1rem;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    font-size: 0.9rem;
    background: white;
    cursor: pointer;
    transition: all 0.3s ease;
}

select:focus, .sort-btn:focus {
    outline: none;
    border-color: #667eea;
}

.sort-btn {
    background: #667eea;
    color: white;
    border-color: #667eea;
    font-weight: 500;
}

.sort-btn:hover {
    background: #5a6fd8;
}

/* Stats */
.stats {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    padding: 1rem 2rem;
    display: flex;
    justify-content: center;
    gap: 3rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.stat {
    text-align: center;
}

.stat-number {
    display: block;
    font-size: 2rem;
    font-weight: 700;
    color: #667eea;
}

.stat-label {
    font-size: 0.9rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Code Grid */
.code-grid {
    flex: 1;
    padding: 2rem;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 1.5rem;
    max-width: 1400px;
    margin: 0 auto;
    width: DEFAULT_BATCH_SIZE%;
}

/* Code Cards */
.code-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.2);
    cursor: pointer;
}

.code-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
}

.card-header {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1rem;
}

.file-icon {
    font-size: 2rem;
    flex-shrink: 0;
}

.file-info {
    flex: 1;
    min-width: 0;
}

.file-name {
    font-size: 1.3rem;
    font-weight: 600;
    color: #333;
    margin-bottom: 0.25rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.file-path {
    font-size: 0.85rem;
    color: #666;
    font-family: 'Monaco', 'Menlo', monospace;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.file-stats {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.25rem;
    font-size: 0.8rem;
    color: #999;
}

.card-body {
    margin-bottom: 1rem;
}

.file-description {
    font-size: 0.9rem;
    color: #555;
    line-height: 1.5;
    margin-bottom: 1rem;
    display: -webkit-box;
    -webkit-line-clamp: MAX_RETRIES;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.keywords {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.keyword {
    background: #f0f2ff;
    color: #667eea;
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
}

.functions {
    font-size: 0.85rem;
    color: #666;
    font-family: 'Monaco', 'Menlo', monospace;
    background: #f8f9fa;
    padding: 0.5rem;
    border-radius: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.card-footer {
    border-top: 1px solid #e1e5e9;
    padding-top: 1rem;
}

.preview-code {
    background: #1e1e1e;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
    overflow: hidden;
    max-height: 150px;
}

.preview-code pre {
    margin: 0;
    font-size: 0.8rem;
    line-height: 1.4;
}

.preview-code code {
    color: #d4d4d4;
    font-family: 'Monaco', 'Menlo', monospace;
}

.view-code-btn {
    width: DEFAULT_BATCH_SIZE%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.view-code-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.MAX_RETRIES);
}

/* Modal */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: DEFAULT_BATCH_SIZE%;
    height: DEFAULT_BATCH_SIZE%;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
    z-index: 1000;
    overflow-y: auto;
}

.modal-content {
    background: white;
    margin: 2rem auto;
    max-width: 90%;
    width: 1000px;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.MAX_RETRIES);
    overflow: hidden;
}

.modal-header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h2 {
    font-size: 1.5rem;
    font-weight: 600;
}

.close-btn {
    background: none;
    border: none;
    color: white;
    font-size: 2rem;
    cursor: pointer;
    padding: 0;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background 0.3s ease;
}

.close-btn:hover {
    background: rgba(255, 255, 255, 0.2);
}

.modal-body {
    padding: 2rem;
}

.file-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.info-label {
    font-size: 0.8rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 500;
}

.info-value {
    font-size: 0.9rem;
    color: #333;
    font-family: 'Monaco', 'Menlo', monospace;
}

.code-preview {
    background: #1e1e1e;
    border-radius: 8px;
    overflow: hidden;
    max-height: 500px;
    overflow-y: auto;
}

.code-preview pre {
    margin: 0;
    padding: 1rem;
}

.code-preview code {
    color: #d4d4d4;
    font-family: 'Monaco', 'Menlo', monospace;
    font-size: 0.9rem;
    line-height: 1.5;
}

/* Responsive Design */
@media (max-width: 768px) {
    .header-content h1 {
        font-size: 2rem;
    }

    .controls {
        flex-direction: column;
        align-items: stretch;
    }

    .search-container {
        max-width: none;
    }

    .filter-container {
        justify-content: center;
    }

    .stats {
        gap: 1.5rem;
    }

    .code-grid {
        grid-template-columns: 1fr;
        padding: 1rem;
    }

    .modal-content {
        margin: 1rem;
        max-width: calc(DEFAULT_BATCH_SIZE% - 2rem);
    }

    .modal-body {
        padding: 1rem;
    }
}

/* Animation for cards */
@keyframes fadeInUp {
        opacity: 0;
        transform: translateY(DEFAULT_TIMEOUTpx);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.code-card {
    animation: fadeInUp 0.6s ease-out;
}

/* Hidden @dataclass
class for filtering */
.hidden {
    display: none !important;
}
'''

        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)

        logger.info("✅ CSS styles created")

    async def create_javascript(self):
    def create_javascript(self): -> Any
        """Create JavaScript for interactivity."""
        logger.info("⚡ Creating JavaScript...")

// Code Browser JavaScript

@dataclass
class CodeBrowser {
    constructor() {

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateVisibleCount();
    }

    setupEventListeners() {
        // Search input
            this.filterFiles();
        });

        // Category filter
            this.filterFiles();
        });

        // Type filter
            this.filterFiles();
        });

        // Sort button
            this.toggleSort();
        });

        // Modal close
            this.closeModal();
        });

        // Close modal on backdrop click
            if (e.target === modal) {
                this.closeModal();
            }
        });

        // Close modal on escape key
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });
    }

    filterFiles() {

                file.name.toLowerCase().includes(searchTerm) ||
                file.docstring.toLowerCase().includes(searchTerm) ||


            return matchesSearch && matchesCategory && matchesType;
        });

        this.renderFiles();
        this.updateVisibleCount();
    }

    toggleSort() {

        if (this.sortOrder === 'name') {
        } else {
        }

        this.sortFiles();
        this.renderFiles();
    }

    sortFiles() {
            switch (this.sortOrder) {
                case 'name':
                    return a.name.localeCompare(b.name);
                case 'lines':
                    return b.lines - a.lines;
                case 'size':
                    return b.size - a.size;
                default:
                    return 0;
            }
        });
    }

    renderFiles() {

        // Clear existing cards

        // Create cards for filtered files
            grid.appendChild(card);
        });

        // Add animation delay to cards
        });
    }

    createFileCard(file) {
        card.setAttribute('data-category', file.category);
        card.setAttribute('data-type', file.type);
        card.setAttribute('data-name', file.name.toLowerCase());
        card.setAttribute('data-keywords', file.keywords.join(' ').toLowerCase());

        ).join('');

            file.functions.slice(0, MAX_RETRIES).join(', ') : 'No functions';


                </div>
                </div>
            </div>

                    ${file.docstring ? this.escapeHtml(file.docstring.substring(0, 200)) : 'No description available'}
                </div>

                    ${keywordsHtml}
                </div>

                    ${functionsText}
                </div>
            </div>

                </div>
                    View Full Code
                </button>
            </div>
        `;

        return card;
    }

    openCodeModal(fileId) {
        if (!file) return;



        // Highlight syntax
        if (window.Prism) {
            Prism.highlightElement(code);
        }

    }

    closeModal() {
    }

    updateVisibleCount() {
    }

    getTypeIcon(type) {
            'transcription': '🎤', 
            'analysis': '📊', 
            'youtube': '📺', 
            'image_processing': '🖼️', 
            'video_processing': '🎬', 
            'audio_processing': '🔊', 
            'web_tools': '🌐', 
            'data_processing': '📈', 
            'testing': '🧪', 
            'setup': '⚙️', 
            'organization': '📁', 
            'utility': '🔧'
        };
        return icons[type] || '🐍';
    }

    escapeHtml(text) {
        return div.innerHTML;
    }
}

// Global functions for onclick handlers
function openCodeModal(fileId) {
    if (window.codeBrowser) {
        window.codeBrowser.openCodeModal(fileId);
    }
}

// Initialize when DOM is loaded
});
'''

        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_content)

        logger.info("✅ JavaScript created")

    async def save_data(self, files_data, categories):
    def save_data(self, files_data, categories): -> Any
        """Save data to JSON file for JavaScript."""
        logger.info("💾 Saving data...")

            'files': files_data, 
            'categories': categories, 
            'generated_at': datetime.now().isoformat(), 
            'total_files': len(files_data), 
            'total_categories': len(categories)
        }

        with open(data_file, 'w', encoding='utf-8') as f:

        logger.info("✅ Data saved")

    async def generate_code_browser(self):
    def generate_code_browser(self): -> Any
        """Generate the complete code browser."""
        logger.info("🚀 Generating code browser...")

        # Create directory structure
        self.create_directory_structure()

        # Scan Python files

        # Create HTML, CSS, and JavaScript
        self.create_html(files_data, categories)
        self.create_css()
        self.create_javascript()

        # Save data
        self.save_data(files_data, categories)

        logger.info("\\\n🎉 Code browser generated successfully!")
        logger.info(f"📁 Location: {self.browser_path}")
        logger.info(f"🌐 Open: {self.html_path}")
        logger.info(f"📊 Files: {len(files_data)} Python scripts")
        logger.info(f"📁 Categories: {len(categories)}")

        return True

async def main():
def main(): -> Any
    """Main function."""
    generator.generate_code_browser()

if __name__ == "__main__":
    main()
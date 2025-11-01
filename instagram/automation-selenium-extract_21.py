
# Constants
CONSTANT_100 = 100
CONSTANT_128 = 128
CONSTANT_300 = 300
CONSTANT_333 = 333
CONSTANT_500 = 500
CONSTANT_555 = 555
CONSTANT_600 = 600
CONSTANT_666 = 666
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920
CONSTANT_8000 = 8000
CONSTANT_856404 = 856404


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

import logging

# Constants



    import html
from datetime import datetime
from functools import lru_cache
from pathlib import Path
import argparse
import asyncio
import http.server
import json
import os
import re
import socketserver
import threading
import time
import webbrowser
from typing import Any, Dict, List, Optional, Union, Tuple, Callable

@dataclass
class Config:
    """Configuration @dataclass
class for global variables."""
    DPI_300 = CONSTANT_300
    DPI_72 = 72
    KB_SIZE = CONSTANT_1024
    MB_SIZE = CONSTANT_1024 * CONSTANT_1024
    GB_SIZE = CONSTANT_1024 * CONSTANT_1024 * CONSTANT_1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = CONSTANT_100
    MAX_FILE_SIZE = 9 * CONSTANT_1024 * CONSTANT_1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = CONSTANT_1920
    DEFAULT_HEIGHT = CONSTANT_1080
    logger = logging.getLogger(__name__)
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    async def __init__(self, base_path = "."):
    self._lazy_loaded = {}
    self.base_path = Path(base_path)
    self.files_data = []
    content = f.read()
    lines = content.split('\\\n')
    info = {
    first_line = content.split('\\\n')[0]
    version_match = re.search(r'#.*python\\s*(\\d+\\.?\\d*)', content, re.IGNORECASE)
    imports = []
    line = line.strip()
    module = line.replace('import ', '').split(' as ')[0].strip()
    module = line.split(' import ')[0].replace('from ', '').strip()
    functions = []
    line = line.strip()
    func_name = line.split('(')[0].replace('def ', '').strip()
    lines = content.split('\\\n')
    start = i
    docstring = '\\\n'.join(lines[start:j+1])
    docstring = re.sub(r'["\']{3}', '', docstring).strip()
    docstring = docstring[:CONSTANT_100] + '...'
    desc = line.strip()[1:].strip()
    desc = desc[:CONSTANT_100] + '...'
    deps = set()
    common_deps = [
    content_lower = content.lower()
    parts = file_path.parts
    python_files = list(self.base_path.rglob("*.py"))
    file_info = self.analyze_file(file_path)
    @lru_cache(maxsize = CONSTANT_128)
    html = f"""<!DOCTYPE html>
    <html lang = "en">
    <meta charset = "UTF-8">
    <meta name = "viewport" content
    <div @dataclass
class = "header">
    <div @dataclass
class = "controls">
    <div @dataclass
class = "search-box">
    <input type = "text" id
    <select @dataclass
class = "filter-select" id
    <option value = "">All Categories</option>
    <select @dataclass
class = "filter-select" id
    <option value = "">All Versions</option>
    <option value = "Python 3.x">Python 3.x</option>
    <option value = "Python 2.x">Python 2.x</option>
    <option value = "Unknown">Unknown</option>
    <div @dataclass
class = "stats">
    <div @dataclass
class = "stat">
    <div @dataclass
class = "stat-number" id
    <div @dataclass
class = "stat-label">Total Files</div>
    <div @dataclass
class = "stat">
    <div @dataclass
class = "stat-number" id
    <div @dataclass
class = "stat-label">Visible</div>
    <div @dataclass
class = "stat">
    <div @dataclass
class = "stat-number" id
    <div @dataclass
class = "stat-label">Categories</div>
    <div @dataclass
class = "files-grid" id
    const filesData = {json.dumps(files_data, indent
    let filteredFiles = [...filesData];
    const categories = [...new Set(filesData.map(f
    const categoryFilter = document.getElementById('categoryFilter');
    categories.forEach(cat = > {{
    const option = document.createElement('option');
    option.value = cat;
    option.textContent = cat;
    document.getElementById('categories').textContent = categories.length;
    const grid = document.getElementById('filesGrid');
    grid.innerHTML = '';
    filteredFiles.forEach(file = > {{
    const card = document.createElement('div');
    card.className = 'file-card';
    card.innerHTML = `
    <div @dataclass
class = "file-header">
    <div @dataclass
class = "file-name">${{file.name}}</div>
    <div @dataclass
class = "file-path">${{file.path}}</div>
    <div @dataclass
class = "file-meta">
    <div @dataclass
class = "python-version">${{file.python_version}}</div>
    <div @dataclass
class = "file-description">${{file.description}}</div>
    <div @dataclass
class = "functions">
    <div @dataclass
class = "function-list">
    ${{file.functions.map(f = > `<span class
    <div @dataclass
class = "dependencies">
    <div @dataclass
class = "dependency-list">
    ${{file.dependencies.map(d = > `<span class
    <div @dataclass
class = "preview">${{file.preview}}</div>
    <div @dataclass
class = "file-stats">
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const category = document.getElementById('categoryFilter').value;
    const version = document.getElementById('versionFilter').value;
    filteredFiles = filesData.filter(file
    const matchesSearch = !searchTerm ||
    file.functions.some(f = > f.toLowerCase().includes(searchTerm)) ||
    file.dependencies.some(d = > d.toLowerCase().includes(searchTerm));
    const matchesCategory = !category || file.category
    const matchesVersion = !version || file.python_version
    document.getElementById('visibleFiles').textContent = filteredFiles.length;
    @lru_cache(maxsize = CONSTANT_128)
    parser = argparse.ArgumentParser(description
    parser.add_argument("--port", type = int, default
    parser.add_argument("--host", default = "localhost", help
    parser.add_argument("--no-server", action = "store_true", help
    args = parser.parse_args()
    logger.info(" = " * 40)
    analyzer = PythonFileAnalyzer()
    files_data = analyzer.scan_files()
    html_content = generate_html(files_data)
    handler = http.server.SimpleHTTPRequestHandler
    @lru_cache(maxsize = CONSTANT_128)
    browser_thread = threading.Thread(target
    browser_thread.daemon = True



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

#!/usr/bin/env python3
"""
Simple Python File Explorer

A lightweight web interface to browse Python files with version info, 
content previews, and dependency information.

Usage:
    python simple_python_explorer.py [--port CONSTANT_8000]
"""


@dataclass
class PythonFileAnalyzer:
    def __init__(self, base_path="."): -> Any

    async def analyze_file(self, file_path):
    def analyze_file(self, file_path): -> Any
        """Analyze a Python file for basic info."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:


            # Extract basic info
                'name': file_path.name, 
                'path': str(file_path.relative_to(self.base_path)), 
                'size': file_path.stat().st_size, 
                'lines': len(lines), 
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M'), 
                'python_version': self.extract_python_version(content), 
                'imports': self.extract_imports(content), 
                'functions': self.extract_functions(content), 
                'description': self.extract_description(content), 
                'dependencies': self.extract_dependencies(content), 
                'preview': '\\\n'.join(lines[:15]), # First 15 lines
                'category': self.get_category(file_path)
            }

            return info

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            return None

    async def extract_python_version(self, content):
    def extract_python_version(self, content): -> Any
        """Extract Python version requirement."""
        # Look for shebang
        if content.startswith('#!'):
            if 'python3' in first_line:
                return 'Python 3.x'
            elif 'python2' in first_line:
                return 'Python 2.x'

        # Look for version comments
        if version_match:
            return f"Python {version_match.group(1)}"

        # Look for requirements or setup.py hints
        if 'python_requires' in content or 'python>=' in content:
            return 'Python 3.x+'

        return 'Unknown'

    async def extract_imports(self, content):
    def extract_imports(self, content): -> Any
        """Extract import statements."""
        for line in content.split('\\\n'):
            if line.startswith('import ') or line.startswith('from '):
                if line.startswith('import '):
                else:
                imports.append(module)
                if len(imports) >= 10:  # Limit to first 10
                    break
        return imports

    async def extract_functions(self, content):
    def extract_functions(self, content): -> Any
        """Extract function definitions."""
        for line in content.split('\\\n'):
            if line.startswith('def '):
                functions.append(func_name)
                if len(functions) >= 8:  # Limit to first 8
                    break
        return functions

    async def extract_description(self, content):
    def extract_description(self, content): -> Any
        """Extract description from docstring or comments."""

        # Look for docstring
        for i, line in enumerate(lines[:10]):
            if '"""' in line or "'''" in line:
                # Find the end of docstring
                for j in range(i+1, min(i+10, len(lines))):
                    if '"""' in lines[j] or "'''" in lines[j]:
                        # Clean up the docstring
                        if len(docstring) > CONSTANT_100:
                        return docstring

        # Look for description comments
        for line in lines[:5]:
            if line.strip().startswith('#') and len(line.strip()) > 10:
                if len(desc) > CONSTANT_100:
                return desc

        return 'No description available'

    async def extract_dependencies(self, content):
    def extract_dependencies(self, content): -> Any
        """Extract common dependencies."""
            'numpy', 'pandas', 'requests', 'openai', 'youtube', 'cv2', 'opencv', 
            'matplotlib', 'seaborn', 'scikit-learn', 'tensorflow', 'torch', 
            'flask', 'django', 'fastapi', 'beautifulsoup4', 'selenium'
        ]

        for dep in common_deps:
            if dep in content_lower:
                deps.add(dep)

        return list(deps)

    async def get_category(self, file_path):
    def get_category(self, file_path): -> Any
        """Get category from path."""
        for part in parts:
            if part.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
                return part
        return 'Other'

    async def scan_files(self):
    def scan_files(self): -> Any
        """Scan all Python files."""
        logger.info("🔍 Scanning Python files...")

        logger.info(f"Found {len(python_files)} Python files")

        for i, file_path in enumerate(python_files, 1):
            if i % 50 == 0:
                logger.info(f"Analyzed {i}/{len(python_files)} files...")

            # Skip certain directories
            if any(skip in str(file_path) for skip in ['__pycache__', '.git', '.venv', 'node_modules']):
                continue

            if file_info:
                self.files_data.append(file_info)

        logger.info(f"✅ Analyzed {len(self.files_data)} files")
        return self.files_data

async def generate_html(files_data):
def generate_html(files_data): -> Any
    """Generate simple HTML interface."""
<head>
    <title>Python File Explorer</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #CONSTANT_333;
            line-height: 1.6;
        }}

        .header {{
            background: #2c3e50;
            color: white;
            padding: 2rem;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}

        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .controls {{
            background: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }}

        .search-box {{
            flex: 1;
            min-width: 300px;
        }}

        .search-box input {{
            width: CONSTANT_100%;
            padding: 0.75rem;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
        }}

        .search-box input:focus {{
            outline: none;
            border-color: #3498db;
        }}

        .filter-select {{
            padding: 0.75rem;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
            background: white;
        }}

        .stats {{
            background: white;
            padding: 1rem 2rem;
            margin: 1rem 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            display: flex;
            gap: 2rem;
            justify-content: center;
        }}

        .stat {{
            text-align: center;
        }}

        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #3498db;
        }}

        .stat-label {{
            font-size: 0.9rem;
            color: #CONSTANT_666;
            text-transform: uppercase;
        }}

        .files-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 1.5rem;
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .file-card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            border-left: 4px solid #3498db;
        }}

        .file-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
        }}

        .file-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }}

        .file-name {{
            font-size: 1.2rem;
            font-weight: CONSTANT_600;
            color: #2c3e50;
            margin-bottom: 0.25rem;
        }}

        .file-path {{
            font-size: 0.9rem;
            color: #CONSTANT_666;
            font-family: monospace;
        }}

        .file-meta {{
            text-align: right;
            font-size: 0.8rem;
            color: #CONSTANT_666;
        }}

        .python-version {{
            background: #e8f5e8;
            color: #2d5a2d;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: CONSTANT_500;
        }}

        .file-description {{
            margin: 1rem 0;
            color: #CONSTANT_555;
            font-style: italic;
        }}

        .functions {{
            margin: 1rem 0;
        }}

        .functions h4 {{
            font-size: 0.9rem;
            color: #CONSTANT_666;
            margin-bottom: 0.5rem;
        }}

        .function-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}

        .function-tag {{
            background: #f0f8ff;
            color: #3498db;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-family: monospace;
        }}

        .dependencies {{
            margin: 1rem 0;
        }}

        .dependencies h4 {{
            font-size: 0.9rem;
            color: #CONSTANT_666;
            margin-bottom: 0.5rem;
        }}

        .dependency-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}

        .dependency-tag {{
            background: #fff3cd;
            color: #CONSTANT_856404;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }}

        .preview {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 1rem;
            margin: 1rem 0;
            font-family: monospace;
            font-size: 0.85rem;
            max-height: 200px;
            overflow-y: auto;
            white-space: pre-wrap;
        }}

        .file-stats {{
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: #CONSTANT_666;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
        }}

        .hidden {{
            display: none;
        }}

        @media (max-width: 768px) {{
            .files-grid {{
                grid-template-columns: 1fr;
                padding: 1rem;
            }}

            .controls {{
                flex-direction: column;
            }}

            .search-box {{
                min-width: auto;
            }}
        }}
    </style>
</head>
<body>
        <h1>🐍 Python File Explorer</h1>
        <p>Browse your Python files with version info, dependencies, and content previews</p>
    </div>

        </div>
        </select>
        </select>
    </div>

        </div>
        </div>
        </div>
    </div>

        <!-- Files will be populated here -->
    </div>

    <script>

        // Populate category filter
            categoryFilter.appendChild(option);
        }});


        function renderFiles() {{

                        <div>
                        </div>
                            <div>${{file.lines}} lines</div>
                            <div>${{(file.size / KB_SIZE).toFixed(1)}} KB</div>
                        </div>
                    </div>


                    ${{file.functions.length > 0 ? `
                        <h4>Functions:</h4>
                        </div>
                    </div>
                    ` : ''}}

                    ${{file.dependencies.length > 0 ? `
                        <h4>Dependencies:</h4>
                        </div>
                    </div>
                    ` : ''}}


                        <span>Modified: ${{file.modified}}</span>
                        <span>Category: ${{file.category}}</span>
                    </div>
                `;
                grid.appendChild(card);
            }});
        }}

        function filterFiles() {{

                    file.name.toLowerCase().includes(searchTerm) ||
                    file.description.toLowerCase().includes(searchTerm) ||


                return matchesSearch && matchesCategory && matchesVersion;
            }});

            renderFiles();
        }}

        // Event listeners
        document.getElementById('searchInput').addEventListener('input', filterFiles);
        document.getElementById('categoryFilter').addEventListener('change', filterFiles);
        document.getElementById('versionFilter').addEventListener('change', filterFiles);

        // Initial render
        renderFiles();
    </script>
</body>
</html>"""

    return html

async def main():
def main(): -> Any


    logger.info("🐍 Simple Python File Explorer")

    # Analyze files

    # Generate HTML

    # Save HTML file
    with open("python_explorer.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    logger.info(f"✅ Generated python_explorer.html")

    if not args.no_server:
        # Start web server
        os.chdir(".")

        with socketserver.TCPServer((args.host, args.port), handler) as httpd:
            logger.info(f"🚀 Server running at http://{args.host}:{args.port}")
            logger.info(f"🌐 Open: http://{args.host}:{args.port}/python_explorer.html")

            # Open browser
            async def open_browser():
            def open_browser(): -> Any
                time.sleep(1)
                webbrowser.open(f"http://{args.host}:{args.port}/python_explorer.html")

            browser_thread.start()

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                logger.info("\\\n🛑 Server stopped")

if __name__ == "__main__":
    main()
"""
Development Testing Create 4

This module provides functionality for development testing create 4.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_102 = 102
CONSTANT_126 = 126
CONSTANT_200 = 200
CONSTANT_234 = 234
CONSTANT_255 = 255
CONSTANT_300 = 300
CONSTANT_333 = 333
CONSTANT_400 = 400
CONSTANT_500 = 500
CONSTANT_555 = 555
CONSTANT_600 = 600
CONSTANT_666 = 666
CONSTANT_700 = 700
CONSTANT_999 = 999
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_2000 = 2000

#!/usr/bin/env python3
"""
Code Browser Generator
Creates a visual code browser similar to avatararts.org/dalle.html
Displays Python scripts as interactive cards with code previews
"""

import os
import json
import base64
from pathlib import Path
from datetime import datetime
import re


class CodeBrowserGenerator:
    def __init__(self, base_path=Path("/Users/steven/Documents/python")):
        """__init__ function."""

        self.base_path = Path(base_path)
        self.browser_path = self.base_path / "code_browser"
        self.html_path = self.browser_path / "index.html"

    def create_directory_structure(self):
        """Create the code browser directory structure."""
        logger.info("📁 Creating code browser structure...")

        self.browser_path.mkdir(exist_ok=True)

        # Create subdirectories
        subdirs = ["css", "js", "data", "images"]
        for subdir in subdirs:
            (self.browser_path / subdir).mkdir(exist_ok=True)

        logger.info(f"✅ Created code browser structure in {self.browser_path}")

    def scan_python_files(self):
        """Scan all Python files and extract metadata."""
        logger.info("🔍 Scanning Python files...")

        files_data = []
        categories = {}

        # Scan all Python files
        for py_file in self.base_path.rglob("*.py"):
            if py_file.is_file() and not py_file.name.startswith("."):
                try:
                    # Read file content
                    with open(py_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Extract metadata
                    file_data = self.extract_file_metadata(py_file, content)
                    files_data.append(file_data)

                    # Group by category
                    category = self.get_category_from_path(py_file)
                    if category not in categories:
                        categories[category] = []
                    categories[category].append(file_data)

                except Exception as e:
                    logger.info(f"⚠️  Error reading {py_file}: {e}")

        # Sort files by name
        files_data.sort(key=lambda x: x["name"].lower())

        logger.info(f"✅ Found {len(files_data)} Python files across {len(categories)} categories")
        return files_data, categories

    def extract_file_metadata(self, file_path, content):
        """Extract metadata from a Python file."""
        relative_path = file_path.relative_to(self.base_path)

        # Extract basic info
        name = file_path.stem
        size = file_path.stat().st_size
        lines = len(content.splitlines())

        # Extract docstring
        docstring = self.extract_docstring(content)

        # Extract imports
        imports = self.extract_imports(content)

        # Extract functions and classes
        functions = self.extract_functions(content)
        classes = self.extract_classes(content)

        # Extract first few lines for preview
        preview_lines = content.splitlines()[:20]
        preview = "\n".join(preview_lines)

        # Determine file type/purpose
        file_type = self.determine_file_type(content, name)

        # Extract keywords
        keywords = self.extract_keywords(content, name)

        return {
            "id": str(relative_path).replace("/", "_").replace(".", "_"),
            "name": name,
            "path": str(relative_path),
            "full_path": str(file_path),
            "size": size,
            "lines": lines,
            "docstring": docstring,
            "imports": imports,
            "functions": functions,
            "classes": classes,
            "preview": preview,
            "file_type": file_type,
            "keywords": keywords,
            "category": self.get_category_from_path(file_path),
            "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
        }

    def extract_docstring(self, content):
        """Extract docstring from Python file."""
        # Look for module docstring
        lines = content.splitlines()
        if lines and lines[0].strip().startswith('"""'):
            # Multi-line docstring
            docstring_lines = []
            for i, line in enumerate(lines[1:], 1):
                if '"""' in line:
                    docstring_lines.append(line.split('"""')[0])
                    break
                docstring_lines.append(line)
            return " ".join(docstring_lines).strip()
        elif lines and lines[0].strip().startswith("'''"):
            # Multi-line docstring with single quotes
            docstring_lines = []
            for i, line in enumerate(lines[1:], 1):
                if "'''" in line:
                    docstring_lines.append(line.split("'''")[0])
                    break
                docstring_lines.append(line)
            return " ".join(docstring_lines).strip()
        elif lines and lines[0].strip().startswith("#"):
            # Comment-based description
            comment_lines = []
            for line in lines:
                if line.strip().startswith("#"):
                    comment_lines.append(line.strip()[1:].strip())
                else:
                    break
            return " ".join(comment_lines).strip()

        return ""

    def extract_imports(self, content):
        """Extract import statements."""
        imports = []
        lines = content.splitlines()

        for line in lines:
            line = line.strip()
            if line.startswith(("import ", "from ")):
                imports.append(line)
                if len(imports) >= 10:  # Limit to first 10 imports
                    break

        return imports

    def extract_functions(self, content):
        """Extract function definitions."""
        functions = []
        lines = content.splitlines()

        for line in lines:
            line = line.strip()
            if line.startswith("def ") and not line.startswith("def _"):
                func_name = line.split("(")[0].replace("def ", "").strip()
                functions.append(func_name)
                if len(functions) >= 5:  # Limit to first 5 functions
                    break

        return functions

    def extract_classes(self, content):
        """Extract class definitions."""
        classes = []
        lines = content.splitlines()

        for line in lines:
            line = line.strip()
            if line.startswith("class ") and not line.startswith("class _"):
                class_name = line.split("(")[0].replace("class ", "").strip()
                classes.append(class_name)
                if len(classes) >= 3:  # Limit to first 3 classes
                    break

        return classes

    def determine_file_type(self, content, filename):
        """Determine the type/purpose of the file."""
        content_lower = content.lower()
        filename_lower = filename.lower()

        # Check for specific patterns
        if "transcription" in filename_lower or "whisper" in content_lower:
            return "transcription"
        elif "analyze" in filename_lower or "analysis" in filename_lower:
            return "analysis"
        elif "youtube" in filename_lower or "youtube" in content_lower:
            return "youtube"
        elif "image" in filename_lower or "pil" in content_lower or "opencv" in content_lower:
            return "image_processing"
        elif "video" in filename_lower or "moviepy" in content_lower:
            return "video_processing"
        elif "audio" in filename_lower or "pyaudio" in content_lower:
            return "audio_processing"
        elif "web" in filename_lower or "requests" in content_lower or "scraping" in filename_lower:
            return "web_tools"
        elif "data" in filename_lower or "pandas" in content_lower or "numpy" in content_lower:
            return "data_processing"
        elif "test" in filename_lower or "unittest" in content_lower:
            return "testing"
        elif "setup" in filename_lower or "install" in filename_lower:
            return "setup"
        elif "migrate" in filename_lower or "organize" in filename_lower:
            return "organization"
        else:
            return "utility"

    def extract_keywords(self, content, filename):
        """Extract relevant keywords from content and filename."""
        keywords = set()

        # Add filename words
        filename_words = re.findall(r"[a-zA-Z]+", filename.lower())
        keywords.update(filename_words)

        # Add common Python/tech keywords
        tech_keywords = [
            "openai",
            "whisper",
            "gpt",
            "ai",
            "ml",
            "transcription",
            "youtube",
            "video",
            "audio",
            "image",
            "processing",
            "web",
            "scraping",
            "requests",
            "beautifulsoup",
            "pandas",
            "numpy",
            "matplotlib",
            "data",
            "flask",
            "django",
            "fastapi",
            "api",
            "test",
            "unittest",
            "pytest",
            "testing",
            "migrate",
            "organize",
            "setup",
            "install",
        ]

        content_lower = content.lower()
        for keyword in tech_keywords:
            if keyword in content_lower:
                keywords.add(keyword)

        return list(keywords)[:10]  # Limit to 10 keywords

    def get_category_from_path(self, file_path):
        """Get category from file path."""
        relative_path = file_path.relative_to(self.base_path)
        path_parts = relative_path.parts

        if len(path_parts) > 1:
            return path_parts[0]  # First directory is category
        else:
            return "root"

    def create_html(self, files_data, categories):
        """Create the main HTML file."""
        logger.info("📝 Creating HTML code browser...")

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Code Browser</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/CONSTANT_2000/svg' viewBox='0 0 CONSTANT_100 100'><text y='.9em' font-size='90'>🐍</text></svg>">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@CONSTANT_300;CONSTANT_400;CONSTANT_500;CONSTANT_600;CONSTANT_700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
</head>
<body>
    <div class="app">
        <!-- Header -->
        <header class="header">
            <div class="header-content">
                <h1>🐍 Python Code Browser</h1>
                <p>Explore {len(files_data)} Python scripts across {len(categories)} categories</p>
            </div>
        </header>

        <!-- Controls -->
        <div class="controls">
            <div class="search-container">
                <input type="text" id="searchInput" placeholder="Search scripts, functions, keywords...">
                <div class="search-icon">🔍</div>
            </div>
            <div class="filter-container">
                <select id="categoryFilter">
                    <option value="">All Categories</option>
                    {self.generate_category_options(categories)}
                </select>
                <select id="typeFilter">
                    <option value="">All Types</option>
                    <option value="transcription">Transcription</option>
                    <option value="analysis">Analysis</option>
                    <option value="youtube">YouTube</option>
                    <option value="image_processing">Image Processing</option>
                    <option value="video_processing">Video Processing</option>
                    <option value="audio_processing">Audio Processing</option>
                    <option value="web_tools">Web Tools</option>
                    <option value="data_processing">Data Processing</option>
                    <option value="testing">Testing</option>
                    <option value="setup">Setup</option>
                    <option value="organization">Organization</option>
                    <option value="utility">Utility</option>
                </select>
                <button id="sortBtn" class="sort-btn">Sort A-Z</button>
            </div>
        </div>

        <!-- Stats -->
        <div class="stats">
            <div class="stat">
                <span class="stat-number">{len(files_data)}</span>
                <span class="stat-label">Scripts</span>
            </div>
            <div class="stat">
                <span class="stat-number">{len(categories)}</span>
                <span class="stat-label">Categories</span>
            </div>
            <div class="stat">
                <span class="stat-number" id="visibleCount">{len(files_data)}</span>
                <span class="stat-label">Visible</span>
            </div>
        </div>

        <!-- Code Grid -->
        <div class="code-grid" id="codeGrid">
            {self.generate_code_cards(files_data)}
        </div>

        <!-- Code Modal -->
        <div class="modal" id="codeModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 id="modalTitle">Script Name</h2>
                    <button class="close-btn" id="closeModal">×</button>
                </div>
                <div class="modal-body">
                    <div class="file-info">
                        <div class="info-item">
                            <span class="info-label">Path:</span>
                            <span class="info-value" id="modalPath">path/to/file.py</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Lines:</span>
                            <span class="info-value" id="modalLines">0</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Size:</span>
                            <span class="info-value" id="modalSize">0 KB</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Type:</span>
                            <span class="info-value" id="modalType">utility</span>
                        </div>
                    </div>
                    <div class="code-preview">
                        <pre><code id="modalCode" class="language-python"></code></pre>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
    <script src="js/script.js"></script>
    <script>
        // Pass data to JavaScript
        window.filesData = {json.dumps(files_data)};
        window.categories = {json.dumps(categories)};
    </script>
</body>
</html>
"""

        with open(self.html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info("✅ HTML code browser created")

    def generate_category_options(self, categories):
        """Generate category options for the filter."""
        options = []
        for category, files in categories.items():
            count = len(files)
            options.append(f'<option value="{category}">{category} ({count})</option>')
        return "\n".join(options)

    def generate_code_cards(self, files_data):
        """Generate HTML for code cards."""
        cards = []

        for file_data in files_data:
            # Truncate preview
            preview = file_data["preview"]
            if len(preview) > CONSTANT_500:
                preview = preview[:CONSTANT_500] + "..."

            # Get file type icon
            type_icon = self.get_type_icon(file_data["file_type"])

            # Format size
            size_kb = file_data["size"] / CONSTANT_1024

            # Generate keywords HTML
            keywords_html = "".join([f'<span class="keyword">{kw}</span>' for kw in file_data["keywords"][:5]])

            card_html = f"""
            <div class="code-card" data-category="{file_data['category']}" data-type="{file_data['file_type']}" data-name="{file_data['name'].lower()}" data-keywords="{' '.join(file_data['keywords']).lower()}">
                <div class="card-header">
                    <div class="file-icon">{type_icon}</div>
                    <div class="file-info">
                        <h3 class="file-name">{file_data['name']}</h3>
                        <p class="file-path">{file_data['path']}</p>
                    </div>
                    <div class="file-stats">
                        <span class="lines">{file_data['lines']} lines</span>
                        <span class="size">{size_kb:.1f} KB</span>
                    </div>
                </div>
                
                <div class="card-body">
                    <div class="file-description">
                        {file_data['docstring'][:CONSTANT_200] if file_data['docstring'] else 'No description available'}
                    </div>
                    
                    <div class="keywords">
                        {keywords_html}
                    </div>
                    
                    <div class="functions">
                        {', '.join(file_data['functions'][:3]) if file_data['functions'] else 'No functions'}
                    </div>
                </div>
                
                <div class="card-footer">
                    <div class="preview-code">
                        <pre><code class="language-python">{self.escape_html(preview[:CONSTANT_300])}</code></pre>
                    </div>
                    <button class="view-code-btn" onclick="openCodeModal('{file_data['id']}')">
                        View Full Code
                    </button>
                </div>
            </div>
            """

            cards.append(card_html)

        return "\n".join(cards)

    def get_type_icon(self, file_type):
        """Get icon for file type."""
        icons = {
            "transcription": "🎤",
            "analysis": "📊",
            "youtube": "📺",
            "image_processing": "🖼️",
            "video_processing": "🎬",
            "audio_processing": "🔊",
            "web_tools": "🌐",
            "data_processing": "📈",
            "testing": "🧪",
            "setup": "⚙️",
            "organization": "📁",
            "utility": "🔧",
        }
        return icons.get(file_type, "🐍")

    def escape_html(self, text):
        """Escape HTML special characters."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

    def create_css(self):
        """Create CSS styles."""
        logger.info("🎨 Creating CSS styles...")

        css_content = """
/* Code Browser Styles */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 CONSTANT_100%);
    min-height: 100vh;
    color: #CONSTANT_333;
}

.app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Header */
.header {
    background: rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.95);
    backdrop-filter: blur(10px);
    padding: 2rem 0;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.header-content h1 {
    font-size: 3rem;
    font-weight: CONSTANT_700;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.header-content p {
    font-size: 1.2rem;
    color: #CONSTANT_666;
    font-weight: CONSTANT_400;
}

/* Controls */
.controls {
    background: rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.9);
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
    width: CONSTANT_100%;
    padding: 0.75rem 1rem 0.75rem 3rem;
    border: 2px solid #e1e5e9;
    border-radius: 25px;
    font-size: 1rem;
    outline: none;
    transition: all 0.3s ease;
}

#searchInput:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(CONSTANT_102, CONSTANT_126, CONSTANT_234, 0.1);
}

.search-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #CONSTANT_999;
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
    font-weight: CONSTANT_500;
}

.sort-btn:hover {
    background: #5a6fd8;
}

/* Stats */
.stats {
    background: rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.9);
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
    font-weight: CONSTANT_700;
    color: #667eea;
}

.stat-label {
    font-size: 0.9rem;
    color: #CONSTANT_666;
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
    width: CONSTANT_100%;
}

/* Code Cards */
.code-card {
    background: rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    border: 1px solid rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.2);
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
    font-weight: CONSTANT_600;
    color: #CONSTANT_333;
    margin-bottom: 0.25rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.file-path {
    font-size: 0.85rem;
    color: #CONSTANT_666;
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
    color: #CONSTANT_999;
}

.card-body {
    margin-bottom: 1rem;
}

.file-description {
    font-size: 0.9rem;
    color: #CONSTANT_555;
    line-height: 1.5;
    margin-bottom: 1rem;
    display: -webkit-box;
    -webkit-line-clamp: 3;
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
    font-weight: CONSTANT_500;
}

.functions {
    font-size: 0.85rem;
    color: #CONSTANT_666;
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
    width: CONSTANT_100%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: CONSTANT_500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.view-code-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(CONSTANT_102, CONSTANT_126, CONSTANT_234, 0.3);
}

/* Modal */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: CONSTANT_100%;
    height: CONSTANT_100%;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
    z-index: CONSTANT_1000;
    overflow-y: auto;
}

.modal-content {
    background: white;
    margin: 2rem auto;
    max-width: 90%;
    width: 1000px;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
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
    font-weight: CONSTANT_600;
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
    background: rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.2);
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
    color: #CONSTANT_666;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: CONSTANT_500;
}

.info-value {
    font-size: 0.9rem;
    color: #CONSTANT_333;
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
        max-width: calc(CONSTANT_100% - 2rem);
    }
    
    .modal-body {
        padding: 1rem;
    }
}

/* Animation for cards */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.code-card {
    animation: fadeInUp 0.6s ease-out;
}

/* Hidden class for filtering */
.hidden {
    display: none !important;
}
"""

        css_file = self.browser_path / "css" / "style.css"
        with open(css_file, "w", encoding="utf-8") as f:
            f.write(css_content)

        logger.info("✅ CSS styles created")

    def create_javascript(self):
        """Create JavaScript for interactivity."""
        logger.info("⚡ Creating JavaScript...")

        js_content = """
// Code Browser JavaScript

class CodeBrowser {
    constructor() {
        this.files = window.filesData || [];
        this.categories = window.categories || {};
        this.filteredFiles = [...this.files];
        this.sortOrder = 'name';
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.updateVisibleCount();
    }
    
    setupEventListeners() {
        // Search input
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', (e) => {
            this.filterFiles();
        });
        
        // Category filter
        const categoryFilter = document.getElementById('categoryFilter');
        categoryFilter.addEventListener('change', (e) => {
            this.filterFiles();
        });
        
        // Type filter
        const typeFilter = document.getElementById('typeFilter');
        typeFilter.addEventListener('change', (e) => {
            this.filterFiles();
        });
        
        // Sort button
        const sortBtn = document.getElementById('sortBtn');
        sortBtn.addEventListener('click', (e) => {
            this.toggleSort();
        });
        
        // Modal close
        const closeModal = document.getElementById('closeModal');
        closeModal.addEventListener('click', (e) => {
            this.closeModal();
        });
        
        // Close modal on backdrop click
        const modal = document.getElementById('codeModal');
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeModal();
            }
        });
        
        // Close modal on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });
    }
    
    filterFiles() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const categoryFilter = document.getElementById('categoryFilter').value;
        const typeFilter = document.getElementById('typeFilter').value;
        
        this.filteredFiles = this.files.filter(file => {
            const matchesSearch = !searchTerm || 
                file.name.toLowerCase().includes(searchTerm) ||
                file.docstring.toLowerCase().includes(searchTerm) ||
                file.keywords.some(kw => kw.toLowerCase().includes(searchTerm)) ||
                file.functions.some(fn => fn.toLowerCase().includes(searchTerm));
            
            const matchesCategory = !categoryFilter || file.category === categoryFilter;
            const matchesType = !typeFilter || file.type === typeFilter;
            
            return matchesSearch && matchesCategory && matchesType;
        });
        
        this.renderFiles();
        this.updateVisibleCount();
    }
    
    toggleSort() {
        const sortBtn = document.getElementById('sortBtn');
        
        if (this.sortOrder === 'name') {
            this.sortOrder = 'lines';
            sortBtn.textContent = 'Sort by Lines';
        } else if (this.sortOrder === 'lines') {
            this.sortOrder = 'size';
            sortBtn.textContent = 'Sort by Size';
        } else {
            this.sortOrder = 'name';
            sortBtn.textContent = 'Sort A-Z';
        }
        
        this.sortFiles();
        this.renderFiles();
    }
    
    sortFiles() {
        this.filteredFiles.sort((a, b) => {
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
        const grid = document.getElementById('codeGrid');
        
        // Clear existing cards
        grid.innerHTML = '';
        
        // Create cards for filtered files
        this.filteredFiles.forEach(file => {
            const card = this.createFileCard(file);
            grid.appendChild(card);
        });
        
        // Add animation delay to cards
        const cards = grid.querySelectorAll('.code-card');
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });
    }
    
    createFileCard(file) {
        const card = document.createElement('div');
        card.className = 'code-card';
        card.setAttribute('data-category', file.category);
        card.setAttribute('data-type', file.type);
        card.setAttribute('data-name', file.name.toLowerCase());
        card.setAttribute('data-keywords', file.keywords.join(' ').toLowerCase());
        
        const typeIcon = this.getTypeIcon(file.type);
        const sizeKb = (file.size / CONSTANT_1024).toFixed(1);
        const keywordsHtml = file.keywords.slice(0, 5).map(kw => 
            `<span class="keyword">${kw}</span>`
        ).join('');
        
        const functionsText = file.functions.length > 0 ? 
            file.functions.slice(0, 3).join(', ') : 'No functions';
        
        const preview = this.escapeHtml(file.preview.substring(0, CONSTANT_300));
        
        card.innerHTML = `
            <div class="card-header">
                <div class="file-icon">${typeIcon}</div>
                <div class="file-info">
                    <h3 class="file-name">${file.name}</h3>
                    <p class="file-path">${file.path}</p>
                </div>
                <div class="file-stats">
                    <span class="lines">${file.lines} lines</span>
                    <span class="size">${sizeKb} KB</span>
                </div>
            </div>
            
            <div class="card-body">
                <div class="file-description">
                    ${file.docstring ? this.escapeHtml(file.docstring.substring(0, CONSTANT_200)) : 'No description available'}
                </div>
                
                <div class="keywords">
                    ${keywordsHtml}
                </div>
                
                <div class="functions">
                    ${functionsText}
                </div>
            </div>
            
            <div class="card-footer">
                <div class="preview-code">
                    <pre><code class="language-python">${preview}</code></pre>
                </div>
                <button class="view-code-btn" onclick="codeBrowser.openCodeModal('${file.id}')">
                    View Full Code
                </button>
            </div>
        `;
        
        return card;
    }
    
    openCodeModal(fileId) {
        const file = this.files.find(f => f.id === fileId);
        if (!file) return;
        
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
        size.textContent = `${(file.size / CONSTANT_1024).toFixed(1)} KB`;
        type.textContent = file.type;
        code.textContent = file.preview;
        
        // Highlight syntax
        if (window.Prism) {
            Prism.highlightElement(code);
        }
        
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
    
    closeModal() {
        const modal = document.getElementById('codeModal');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
    
    updateVisibleCount() {
        const visibleCount = document.getElementById('visibleCount');
        visibleCount.textContent = this.filteredFiles.length;
    }
    
    getTypeIcon(type) {
        const icons = {
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
        const div = document.createElement('div');
        div.textContent = text;
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
document.addEventListener('DOMContentLoaded', () => {
    window.codeBrowser = new CodeBrowser();
});
"""

        js_file = self.browser_path / "js" / "script.js"
        with open(js_file, "w", encoding="utf-8") as f:
            f.write(js_content)

        logger.info("✅ JavaScript created")

    def save_data(self, files_data, categories):
        """Save data to JSON file for JavaScript."""
        logger.info("💾 Saving data...")

        data = {
            "files": files_data,
            "categories": categories,
            "generated_at": datetime.now().isoformat(),
            "total_files": len(files_data),
            "total_categories": len(categories),
        }

        data_file = self.browser_path / "data" / "files_data.json"
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info("✅ Data saved")

    def generate_code_browser(self):
        """Generate the complete code browser."""
        logger.info("🚀 Generating code browser...")
        logger.info("=" * 50)

        # Create directory structure
        self.create_directory_structure()

        # Scan Python files
        files_data, categories = self.scan_python_files()

        # Create HTML, CSS, and JavaScript
        self.create_html(files_data, categories)
        self.create_css()
        self.create_javascript()

        # Save data
        self.save_data(files_data, categories)

        logger.info("\n🎉 Code browser generated successfully!")
        logger.info(f"📁 Location: {self.browser_path}")
        logger.info(f"🌐 Open: {self.html_path}")
        logger.info(f"📊 Files: {len(files_data)} Python scripts")
        logger.info(f"📁 Categories: {len(categories)}")

        return True


def main():
    """Main function."""
    generator = CodeBrowserGenerator()
    generator.generate_code_browser()


if __name__ == "__main__":
    main()

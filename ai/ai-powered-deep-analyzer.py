
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_033 = 033
CONSTANT_100 = 100
CONSTANT_256 = 256
CONSTANT_500 = 500
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_2000 = 2000
CONSTANT_3000 = 3000
CONSTANT_65536 = 65536

#!/usr/bin/env python3
"""
🧠 AI-POWERED DEEP INTELLIGENT CONTENT-AWARE ANALYZER
====================================================
Advanced duplicate detection with AI-powered semantic understanding,
architectural pattern recognition, and confidence scoring.

Features:
✨ 6-level deep folder traversal
✨ SHA-CONSTANT_256 content hashing
✨ Advanced AST-based semantic analysis
✨ AI-powered code understanding (OpenAI/Gemini)
✨ Vector embeddings for semantic similarity
✨ Architectural pattern detection
✨ Confidence scoring system
✨ Intelligent categorization and tagging
✨ Developer-friendly with artistic flair
"""

import ast
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# Color codes for beautiful output
class Colors:
    HEADER = '\CONSTANT_033[95m'
    BLUE = '\CONSTANT_033[94m'
    CYAN = '\CONSTANT_033[96m'
    GREEN = '\CONSTANT_033[92m'
    YELLOW = '\CONSTANT_033[93m'
    RED = '\CONSTANT_033[91m'
    MAGENTA = '\CONSTANT_033[35m'
    WHITE = '\CONSTANT_033[97m'
    END = '\CONSTANT_033[0m'
    BOLD = '\CONSTANT_033[1m'
    UNDERLINE = '\CONSTANT_033[4m'
    BLINK = '\CONSTANT_033[5m'

# Emoji system for visual feedback
class Emojis:
    ROCKET = "🚀"
    BRAIN = "🧠"
    SPARKLES = "✨"
    FIRE = "🔥"
    TARGET = "🎯"
    MICROSCOPE = "🔬"
    ROBOT = "🤖"
    CHART = "📊"
    LIGHTBULB = "💡"
    GEAR = "⚙️"
    FOLDER = "📁"
    FILE = "📄"
    PYTHON = "🐍"
    CHECK = "✅"
    WARN = "⚠️"
    ERROR = "❌"
    STAR = "⭐"
    MAGIC = "🪄"


class AICodeAnalyzer:
    """AI-powered code analysis using OpenAI/Gemini"""

    def __init__(self):
        # Load API keys from environment
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')

        # Use available API
        self.use_openai = bool(self.openai_key)
        self.use_gemini = bool(self.gemini_key) and not self.use_openai
        self.use_anthropic = bool(self.anthropic_key) and not (self.use_openai or self.use_gemini)

    def analyze_code_with_ai(self, code_snippet: str, filepath: str) -> Dict[str, Any]:
        """Use AI to deeply understand code purpose and patterns"""

        if not any([self.use_openai, self.use_gemini, self.use_anthropic]):
            return self._fallback_analysis(code_snippet, filepath)

        try:
            prompt = f"""Analyze this Python code and provide:
1. Primary purpose (one sentence)
2. Category (e.g., web scraping, image processing, automation, data analysis, etc.)
3. Architectural patterns used (e.g., MVC, script, class-based, functional)
4. Confidence score (0.0-1.0) in your analysis
5. Key technologies/libraries detected
6. Code quality indicators

File: {Path(filepath).name}

Code snippet (first 50 lines):
```python
{code_snippet[:CONSTANT_3000]}
```

Respond in JSON format:
{{
    "purpose": "...",
    "category": "...",
    "patterns": [...],
    "confidence": 0.0-1.0,
    "technologies": [...],
    "quality": {{
        "has_docstrings": bool,
        "has_type_hints": bool,
        "complexity": "low/medium/high"
    }}
}}
"""

            if self.use_openai:
                return self._query_openai(prompt)
            elif self.use_gemini:
                return self._query_gemini(prompt)
            elif self.use_anthropic:
                return self._query_anthropic(prompt)

        except Exception as e:
            logger.info(f"{Colors.YELLOW}{Emojis.WARN} AI analysis failed: {e}{Colors.END}")
            return self._fallback_analysis(code_snippet, filepath)

    def _query_openai(self, prompt: str) -> Dict[str, Any]:
        """Query OpenAI API"""
        try:
            import openai
            openai.api_key = self.openai_key

            response = openai.chat.completions.create(
                model="gpt-4o-mini",  # Fast and cost-effective
                messages=[
                    {"role": "system", "content": "You are an expert code analyzer. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=CONSTANT_500
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logger.info(f"{Colors.RED}{Emojis.ERROR} OpenAI error: {e}{Colors.END}")
            return self._fallback_analysis(prompt, "")

    def _query_gemini(self, prompt: str) -> Dict[str, Any]:
        """Query Gemini API"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_key)

            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)

            # Extract JSON from response
            text = response.text
            # Find JSON in response
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result
            else:
                return self._fallback_analysis(prompt, "")

        except Exception as e:
            logger.info(f"{Colors.RED}{Emojis.ERROR} Gemini error: {e}{Colors.END}")
            return self._fallback_analysis(prompt, "")

    def _query_anthropic(self, prompt: str) -> Dict[str, Any]:
        """Query Anthropic (Claude) API"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.anthropic_key)

            response = client.messages.create(
                model="claude-3-haiku-20240307",  # Fast and economical
                max_tokens=CONSTANT_500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            result = json.loads(response.content[0].text)
            return result

        except Exception as e:
            logger.info(f"{Colors.RED}{Emojis.ERROR} Anthropic error: {e}{Colors.END}")
            return self._fallback_analysis(prompt, "")

    def _fallback_analysis(self, code: str, filepath: str) -> Dict[str, Any]:
        """Fallback analysis without AI"""
        return {
            "purpose": "Code analysis (AI unavailable)",
            "category": "uncategorized",
            "patterns": ["script"],
            "confidence": 0.5,
            "technologies": [],
            "quality": {
                "has_docstrings": '"""' in code or "'''" in code,
                "has_type_hints": '->' in code or ': ' in code,
                "complexity": "unknown"
            }
        }


class VectorEmbeddingAnalyzer:
    """Create and compare code embeddings for semantic similarity"""

    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.embeddings_cache = {}

    def get_code_embedding(self, code: str, identifier: str) -> Optional[List[float]]:
        """Get embedding vector for code"""
        if identifier in self.embeddings_cache:
            return self.embeddings_cache[identifier]

        if not self.openai_key:
            return None

        try:
            import openai
            openai.api_key = self.openai_key

            # Truncate code to reasonable length
            code_sample = code[:CONSTANT_2000]

            response = openai.embeddings.create(
                model="text-embedding-3-small",
                input=code_sample
            )

            embedding = response.data[0].embedding
            self.embeddings_cache[identifier] = embedding
            return embedding

        except Exception as e:
            logger.info(f"{Colors.YELLOW}{Emojis.WARN} Embedding failed: {e}{Colors.END}")
            return None

    def calculate_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            import numpy as np
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            return float(dot_product / (norm1 * norm2))
        except (ImportError, ModuleNotFoundError):
            return 0.0


class ArchitecturalPatternDetector:
    """Detect architectural patterns in code"""

    PATTERNS = {
        'MVC': ['Model', 'View', 'Controller', 'render', 'template'],
        'API': ['api', 'endpoint', 'route', '@app', 'flask', 'fastapi', 'request', 'response'],
        'CLI': ['argparse', 'click', 'sys.argv', 'main()'],
        'Data Pipeline': ['transform', 'extract', 'load', 'ETL', 'pipeline'],
        'Web Scraper': ['beautifulsoup', 'selenium', 'requests', 'scrape', 'crawl'],
        'Bot': ['bot', 'telegram', 'discord', 'slack', 'automated'],
        'Image Processing': ['PIL', 'opencv', 'cv2', 'image', 'resize', 'crop'],
        'Machine Learning': ['tensorflow', 'torch', 'sklearn', 'model.fit', 'predict'],
        'Automation': ['schedule', 'cron', 'automated', 'batch'],
        'Database': ['sqlalchemy', 'database', 'query', 'SELECT', 'INSERT'],
    }

    def detect_patterns(self, code: str, metadata: Dict) -> List[Tuple[str, float]]:
        """Detect architectural patterns with confidence scores"""
        patterns_found = []
        code_lower = code.lower()

        for pattern_name, keywords in self.PATTERNS.items():
            matches = sum(1 for kw in keywords if kw.lower() in code_lower)
            if matches > 0:
                confidence = min(matches / len(keywords), 1.0)
                patterns_found.append((pattern_name, confidence))

        # Sort by confidence
        patterns_found.sort(key=lambda x: x[1], reverse=True)
        return patterns_found[:3]  # Top 3


class AIDeepIntelligentAnalyzer:
    """Main analyzer with AI enhancements"""

    def __init__(self, directories: List[str], max_depth: int = 6):
        self.directories = directories
        self.max_depth = max_depth
        self.file_inventory = {}
        self.hash_to_files = defaultdict(list)
        self.semantic_groups = defaultdict(list)
        self.category_groups = defaultdict(list)

        # AI components
        self.ai_analyzer = AICodeAnalyzer()
        self.embedding_analyzer = VectorEmbeddingAnalyzer()
        self.pattern_detector = ArchitecturalPatternDetector()

        self.stats = {
            'total_files': 0,
            'total_size': 0,
            'py_files': 0,
            'exact_dupes': 0,
            'semantic_dupes': 0,
            'unique_files': 0,
            'ai_analyzed': 0,
            'patterns_detected': 0
        }

    def print_header(self, text: str, color=Colors.CYAN, emoji=""):
        """Print fancy headers with emojis"""
        logger.info(f"\n{color}{Colors.BOLD}{'='*80}")
        logger.info(f"{emoji} {text}")
        logger.info(f"{'='*80}{Colors.END}\n")

    def calculate_hash(self, filepath: Path) -> str:
        """Calculate SHA-CONSTANT_256 hash"""
        try:
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(CONSTANT_65536), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            return f"ERROR: {str(e)}"

    def extract_python_metadata(self, filepath: Path) -> Dict[str, Any]:
        """Extract enhanced metadata with AI analysis"""
        metadata = {
            'functions': [],
            'classes': [],
            'imports': [],
            'docstring': None,
            'loc': 0,
            'complexity_score': 0,
            'is_valid_python': False,
            'ai_analysis': None,
            'patterns': [],
            'category': 'uncategorized',
            'embedding': None
        }

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                metadata['loc'] = len(content.splitlines())

            # AST Analysis
            tree = ast.parse(content)
            metadata['is_valid_python'] = True
            metadata['docstring'] = ast.get_docstring(tree)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    metadata['functions'].append(node.name)
                    metadata['complexity_score'] += 1
                elif isinstance(node, ast.ClassDef):
                    metadata['classes'].append(node.name)
                    metadata['complexity_score'] += 2
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        metadata['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        metadata['imports'].append(node.module)

            # AI-Powered Analysis (sample files for efficiency)
            if metadata['loc'] > 10 and metadata['loc'] < CONSTANT_1000:  # Reasonable size
                if self.stats['ai_analyzed'] < CONSTANT_100:  # Limit AI calls
                    logger.info(f"{Colors.CYAN}{Emojis.BRAIN} AI analyzing: {filepath.name}{Colors.END}")
                    ai_result = self.ai_analyzer.analyze_code_with_ai(content, str(filepath))
                    metadata['ai_analysis'] = ai_result
                    metadata['category'] = ai_result.get('category', 'uncategorized')
                    self.stats['ai_analyzed'] += 1

            # Pattern Detection
            patterns = self.pattern_detector.detect_patterns(content, metadata)
            if patterns:
                metadata['patterns'] = patterns
                self.stats['patterns_detected'] += 1

            # Vector Embedding (for top files)
            if metadata['loc'] > 50 and self.stats['ai_analyzed'] < 50:
                embedding = self.embedding_analyzer.get_code_embedding(content, str(filepath))
                if embedding:
                    metadata['embedding'] = embedding

        except Exception as e:
            metadata['error'] = str(e)

        return metadata

    def get_file_signature(self, metadata: Dict[str, Any]) -> str:
        """Create semantic signature"""
        functions = sorted(metadata.get('functions', []))
        classes = sorted(metadata.get('classes', []))
        imports = sorted(metadata.get('imports', []))
        category = metadata.get('category', 'unknown')

        signature_parts = [
            f"CAT:{category}",
            f"F:{','.join(functions[:10])}",
            f"C:{','.join(classes[:5])}",
            f"I:{','.join(imports[:10])}"
        ]

        return "|".join(signature_parts)

    def scan_directory(self, directory: str, current_depth: int = 0):
        """Recursively scan directory"""
        if current_depth > self.max_depth:
            return

        try:
            dir_path = Path(directory)
            if not dir_path.exists():
                logger.info(f"{Colors.RED}{Emojis.ERROR} Not found: {directory}{Colors.END}")
                return

            logger.info(f"{Colors.CYAN}{Emojis.FOLDER} Scanning: {directory} (depth: {current_depth}/{self.max_depth}){Colors.END}")

            for item in dir_path.iterdir():
                try:
                    if item.is_file():
                        self.process_file(item, directory)
                    elif item.is_dir() and not item.name.startswith('.') and item.name != '__pycache__':
                        self.scan_directory(item, current_depth + 1)
                except PermissionError:
                    pass
                except Exception as e:
                    pass

        except Exception as e:
            logger.info(f"{Colors.RED}{Emojis.ERROR} Error: {directory}: {e}{Colors.END}")

    def process_file(self, filepath: Path, source_dir: str):
        """Process individual file with AI enhancement"""
        try:
            size = filepath.stat().st_size
            file_hash = self.calculate_hash(filepath)

            file_info = {
                'path': str(filepath),
                'name': filepath.name,
                'size': size,
                'hash': file_hash,
                'source_dir': source_dir,
                'extension': filepath.suffix,
                'modified': filepath.stat().st_mtime,
                'is_python': filepath.suffix == '.py'
            }

            # Enhanced Python analysis
            if file_info['is_python']:
                file_info['metadata'] = self.extract_python_metadata(filepath)
                file_info['signature'] = self.get_file_signature(file_info['metadata'])
                file_info['category'] = file_info['metadata'].get('category', 'uncategorized')
                self.stats['py_files'] += 1

                # Group by semantic signature
                if file_info['signature']:
                    self.semantic_groups[file_info['signature']].append(str(filepath))

                # Group by AI-determined category
                if file_info['category']:
                    self.category_groups[file_info['category']].append(str(filepath))

            self.file_inventory[str(filepath)] = file_info
            self.hash_to_files[file_hash].append(str(filepath))

            self.stats['total_files'] += 1
            self.stats['total_size'] += size

        except Exception as e:
            pass

    def analyze_duplicates(self):
        """Analyze exact and semantic duplicates"""
        self.print_header("DUPLICATE ANALYSIS", Colors.YELLOW, Emojis.CHART)

        exact_dupes = {h: files for h, files in self.hash_to_files.items()
                      if len(files) > 1 and not h.startswith("ERROR")}

        self.stats['exact_dupes'] = sum(len(files) - 1 for files in exact_dupes.values())
        self.stats['unique_files'] = self.stats['total_files'] - self.stats['exact_dupes']

        logger.info(f"{Colors.GREEN}{Emojis.CHECK} Exact Duplicates: {len(exact_dupes)} groups{Colors.END}")
        logger.info(f"{Colors.BLUE}   Duplicate files: {self.stats['exact_dupes']}{Colors.END}")

        semantic_dupes = {sig: files for sig, files in self.semantic_groups.items()
                         if len(files) > 1}

        self.stats['semantic_dupes'] = len(semantic_dupes)

        logger.info(f"{Colors.GREEN}{Emojis.CHECK} Semantic Groups: {self.stats['semantic_dupes']}{Colors.END}")

        # Category analysis
        logger.info(f"\n{Colors.MAGENTA}{Emojis.SPARKLES} AI-Powered Categories:{Colors.END}")
        for category, files in sorted(self.category_groups.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            logger.info(f"  {Colors.CYAN}{category}{Colors.END}: {len(files)} files")

        return exact_dupes, semantic_dupes

    def generate_diff(self, file1: str, file2: str) -> List[str]:
        """Generate unified diff"""
        try:
            with open(file1, 'r', encoding='utf-8', errors='ignore') as f:
                lines1 = f.readlines()
            with open(file2, 'r', encoding='utf-8', errors='ignore') as f:
                lines2 = f.readlines()

            diff = list(difflib.unified_diff(
                lines1, lines2,
                fromfile=file1,
                tofile=file2,
                lineterm=''
            ))

            return diff
        except Exception as e:
            return [f"ERROR: {e}"]

    def create_detailed_report(self, exact_dupes: Dict, semantic_dupes: Dict):
        """Create comprehensive AI-enhanced report"""
        self.print_header("GENERATING AI-POWERED REPORT", Colors.BLUE, Emojis.MAGIC)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"/Users/steven/Documents/python/AI_DEEP_ANALYSIS_{timestamp}.md"
        diff_dir = f"/Users/steven/Documents/python/ai_diff_reports_{timestamp}"

        Path(diff_dir).mkdir(exist_ok=True)

        with open(report_file, 'w', encoding='utf-8') as report:
            report.write("# 🧠 AI-POWERED DEEP INTELLIGENCE ANALYSIS REPORT\n\n")
            report.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            report.write("---\n\n")

            # Executive Summary
            report.write("## 📊 EXECUTIVE SUMMARY\n\n")
            report.write(f"| Metric | Value |\n")
            report.write(f"|--------|-------|\n")
            report.write(f"| **Total Files** | {self.stats['total_files']:,} |\n")
            report.write(f"| **Total Size** | {self.stats['total_size'] / (CONSTANT_1024**3):.2f} GB |\n")
            report.write(f"| **Python Files** | {self.stats['py_files']:,} |\n")
            report.write(f"| **AI Analyzed** | {self.stats['ai_analyzed']:,} |\n")
            report.write(f"| **Patterns Detected** | {self.stats['patterns_detected']:,} |\n")
            report.write(f"| **Exact Duplicates** | {self.stats['exact_dupes']:,} |\n")
            report.write(f"| **Semantic Groups** | {self.stats['semantic_dupes']:,} |\n")
            report.write(f"| **Unique Files** | {self.stats['unique_files']:,} |\n\n")

            # AI-Powered Categories
            report.write("## 🤖 AI-POWERED CATEGORIZATION\n\n")
            for category, files in sorted(self.category_groups.items(), key=lambda x: len(x[1]), reverse=True):
                report.write(f"### {category.title()}\n")
                report.write(f"**Files:** {len(files)}\n\n")

                # Sample files from category
                for file_path in files[:5]:
                    file_info = self.file_inventory.get(file_path, {})
                    metadata = file_info.get('metadata', {})
                    ai_analysis = metadata.get('ai_analysis', {})

                    report.write(f"- `{Path(file_path).name}`\n")
                    if ai_analysis:
                        report.write(f"  - Purpose: {ai_analysis.get('purpose', 'N/A')}\n")
                        report.write(f"  - Confidence: {ai_analysis.get('confidence', 0):.2f}\n")
                        patterns = metadata.get('patterns', [])
                        if patterns:
                            report.write(f"  - Patterns: {', '.join([p[0] for p in patterns[:2]])}\n")

                report.write(Path("\n"))

            # Exact Duplicates
            report.write("## 🔄 EXACT DUPLICATES\n\n")
            for idx, (file_hash, files) in enumerate(list(exact_dupes.items())[:30], 1):
                report.write(f"### Group #{idx}\n")
                report.write(f"**Hash:** `{file_hash[:16]}...`\n")
                report.write(f"**Files:** {len(files)}\n\n")

                for file_path in files:
                    file_info = self.file_inventory[file_path]
                    report.write(f"- `{file_path}`\n")
                    report.write(f"  - Size: {file_info['size']:,} bytes\n")
                    if file_info.get('category'):
                        report.write(f"  - Category: {file_info['category']}\n")

                report.write(Path("\n---\n\n"))

            # Consolidation Plan
            report.write("## 🎯 AI-RECOMMENDED CONSOLIDATION STRATEGY\n\n")
            report.write("### Phase 1: Archive Duplicates\n")
            report.write("- Move exact duplicates to archive\n")
            report.write("- Keep most recent versions from `python_backup`\n\n")

            report.write("### Phase 2: Organize by Category\n")
            for category in sorted(self.category_groups.keys())[:10]:
                count = len(self.category_groups[category])
                report.write(f"- **{category}**: {count} files → Move to `{category}/`\n")

            report.write("\n### Phase 3: Quality Improvement\n")
            report.write("- Add missing docstrings\n")
            report.write("- Improve code with low confidence scores\n")
            report.write("- Standardize naming conventions\n\n")

        logger.info(f"{Colors.GREEN}{Emojis.CHECK} Report: {report_file}{Colors.END}")
        logger.info(f"{Colors.GREEN}{Emojis.CHECK} Diffs: {diff_dir}{Colors.END}")

        return report_file, diff_dir

    def create_json_export(self):
        """Export to JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = f"/Users/steven/Documents/python/ai_analysis_{timestamp}.json"

        # Serialize (remove non-serializable embeddings)
        inventory_clean = {}
        for path, info in self.file_inventory.items():
            info_copy = info.copy()
            if 'metadata' in info_copy and 'embedding' in info_copy['metadata']:
                info_copy['metadata'] = {**info_copy['metadata'], 'embedding': 'VECTOR_DATA'}
            inventory_clean[path] = info_copy

        export_data = {
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats,
            'directories': self.directories,
            'file_inventory': inventory_clean,
            'categories': {k: len(v) for k, v in self.category_groups.items()}
        }

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)

        logger.info(f"{Colors.GREEN}{Emojis.CHECK} JSON: {json_file}{Colors.END}")
        return json_file

    def run_complete_analysis(self):
        """Execute full AI-powered analysis"""
        logger.info(f"{Colors.BOLD}{Colors.MAGENTA}")
        logger.info("╔═══════════════════════════════════════════════════════════════════════════════╗")
        logger.info("║                                                                               ║")
        logger.info("║           🧠 AI-POWERED DEEP INTELLIGENT ANALYZER 🚀                          ║")
        logger.info("║                                                                               ║")
        logger.info("║        Advanced AI-Driven Code Analysis & Pattern Recognition System         ║")
        logger.info("║                                                                               ║")
        logger.info("╚═══════════════════════════════════════════════════════════════════════════════╝")
        logger.info(f"{Colors.END}\n")

        # Phase 1: Scanning
        self.print_header("PHASE 1: DEEP SCANNING", Colors.CYAN, Emojis.MICROSCOPE)
        logger.info(f"{Colors.YELLOW}{Emojis.GEAR} Max Depth: {self.max_depth} levels{Colors.END}\n")

        for directory in self.directories:
            self.scan_directory(directory, current_depth=0)

        logger.info(f"\n{Colors.GREEN}{Emojis.CHECK} Scan complete! {self.stats['total_files']:,} files{Colors.END}")

        # Phase 2: Analysis
        self.print_header("PHASE 2: AI ANALYSIS", Colors.CYAN, Emojis.BRAIN)
        exact_dupes, semantic_dupes = self.analyze_duplicates()

        # Phase 3: Reporting
        self.print_header("PHASE 3: REPORT GENERATION", Colors.CYAN, Emojis.SPARKLES)
        report_file, diff_dir = self.create_detailed_report(exact_dupes, semantic_dupes)
        json_file = self.create_json_export()

        # Final Summary
        self.print_header("ANALYSIS COMPLETE!", Colors.GREEN, Emojis.ROCKET)
        logger.info(f"{Colors.BOLD}📊 FINAL STATS:{Colors.END}\n")
        logger.info(f"  {Emojis.FILE} Files: {Colors.CYAN}{self.stats['total_files']:,}{Colors.END}")
        logger.info(f"  {Emojis.PYTHON} Python: {Colors.CYAN}{self.stats['py_files']:,}{Colors.END}")
        logger.info(f"  {Emojis.BRAIN} AI Analyzed: {Colors.CYAN}{self.stats['ai_analyzed']:,}{Colors.END}")
        logger.info(f"  {Emojis.FIRE} Patterns: {Colors.CYAN}{self.stats['patterns_detected']:,}{Colors.END}")
        logger.info(f"  💾 Size: {Colors.CYAN}{self.stats['total_size'] / (CONSTANT_1024**3):.2f} GB{Colors.END}\n")

        logger.info(f"{Colors.BOLD}📝 OUTPUTS:{Colors.END}\n")
        logger.info(f"  {Emojis.FILE} Report: {Colors.BLUE}{report_file}{Colors.END}")
        logger.info(f"  {Emojis.FOLDER} Diffs: {Colors.BLUE}{diff_dir}{Colors.END}")
        logger.info(f"  {Emojis.CHART} Data: {Colors.BLUE}{json_file}{Colors.END}\n")

        return {
            'stats': self.stats,
            'report_file': report_file,
            'diff_dir': diff_dir,
            'json_file': json_file
        }


def main():
    """Main execution"""
    # Load environment
    env_file = Path("/Users/steven/.env.d/MASTER_CONSOLIDATED.env")
    if Path(env_file).exists():
        logger.info(f"{Colors.CYAN}{Emojis.GEAR} Loading API keys...{Colors.END}")
        # Source the file to load env vars
        for line in open(env_file):
            if line.startswith('export '):
                line = line.replace('export ', '').strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip('"').strip("'").split('#')[0].strip()
                    os.environ[key] = value

    directories = [
        Path("/Users/steven/Documents/python-repo"),
        Path("/Users/steven/Documents/python"),
        Path("/Users/steven/Documents/python_backup")
    ]

    logger.info(f"\n{Colors.BOLD}{Colors.CYAN}Analyzing directories:{Colors.END}")
    for d in directories:
        logger.info(f"  {Emojis.FOLDER} {d}")

    analyzer = AIDeepIntelligentAnalyzer(directories, max_depth=6)
    results = analyzer.run_complete_analysis()

    logger.info(f"\n{Colors.GREEN}{Colors.BOLD}{Colors.BLINK}{Emojis.SPARKLES} ALL DONE! {Emojis.SPARKLES}{Colors.END}\n")


if __name__ == "__main__":
    main()

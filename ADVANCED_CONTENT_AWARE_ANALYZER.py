#!/usr/bin/env python3
"""
🧠 ADVANCED CONTENT-AWARE INTELLIGENT ANALYZER
Ultra-sophisticated file analysis with deep semantic understanding

Features:
- Deep content reading with intelligent encoding detection
- Semantic analysis with 9+ categories and weighted scoring
- AST-based code intelligence (functions, classes, patterns)
- Content quality assessment (complexity, documentation, maturity)
- Advanced relationship mapping (imports, references, dependencies)
- Intelligent categorization with priority scoring
- Pattern recognition and architectural detection
- Multi-factor decision making with confidence scoring
"""

import os
import sys
import json
import ast
import hashlib
import mimetypes
import re
import csv
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import defaultdict, Counter
try:
    import chardet  # For encoding detection
    HAS_CHARDET = True
except ImportError:
    HAS_CHARDET = False
import traceback


@dataclass
class CodeMetrics:
    """Code complexity and quality metrics"""
    functions: int = 0
    classes: int = 0
    imports: List[str] = field(default_factory=list)
    lines_of_code: int = 0
    complexity: str = "unknown"  # low, medium, high
    documentation_quality: str = "unknown"  # low, medium, high
    has_docstrings: bool = False
    has_type_hints: bool = False
    technical_debt_markers: List[str] = field(default_factory=list)


@dataclass
class SemanticAnalysis:
    """Semantic category analysis"""
    primary_category: str = ""
    secondary_categories: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    keyword_scores: Dict[str, float] = field(default_factory=dict)
    content_type: str = ""  # markdown, python, web, data, etc.
    project_context: str = ""  # As-a-Man-Thinketh, YouTube, Portfolio, etc.


@dataclass
class RelationshipMapping:
    """File relationships and dependencies"""
    imports: List[str] = field(default_factory=list)
    imports_from: List[str] = field(default_factory=list)
    referenced_files: List[str] = field(default_factory=list)
    external_urls: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    version_patterns: List[str] = field(default_factory=list)
    date_markers: List[str] = field(default_factory=list)


@dataclass
class FileIntelligence:
    """Comprehensive file intelligence"""
    filepath: Path
    content_hash: str
    file_size: int
    file_type: str
    encoding: str

    # Content analysis
    code_metrics: CodeMetrics
    semantic_analysis: SemanticAnalysis
    relationships: RelationshipMapping

    # Quality insights
    complexity_level: str
    documentation_quality: str
    project_maturity: str
    technical_debt: List[str]

    # Categorization
    recommended_category: str
    priority_score: float
    confidence: float

    # Recommendations
    destination_suggestions: List[str]
    key_phrases: List[str]
    description: str

    # Metadata
    analysis_timestamp: datetime
    analysis_errors: List[str] = field(default_factory=list)


class AdvancedContentAnalyzer:
    """Advanced content-aware intelligent analyzer"""

    # Semantic categories with weighted keywords
    SEMANTIC_CATEGORIES = {
        "AI/ML": {
            "keywords": {
                "openai": 10, "anthropic": 10, "claude": 10, "gpt": 10,
                "llm": 9, "neural": 9, "tensorflow": 9, "pytorch": 9,
                "huggingface": 8, "transformers": 8, "model": 8,
                "training": 7, "inference": 7, "embedding": 7,
                "machine learning": 8, "deep learning": 8, "ai": 7,
                "gemini": 9, "groq": 9, "perplexity": 9, "ollama": 8
            },
            "code_patterns": ["Model", "Trainer", "NeuralNetwork", "LLM", "Embedding"],
            "imports": ["openai", "anthropic", "transformers", "torch", "tensorflow"]
        },
        "Web Development": {
            "keywords": {
                "flask": 10, "django": 10, "fastapi": 9, "streamlit": 9,
                "html": 8, "css": 8, "javascript": 8, "react": 9,
                "api": 8, "endpoint": 7, "route": 7, "middleware": 7,
                "http": 7, "rest": 8, "graphql": 8, "websocket": 7,
                "frontend": 8, "backend": 8, "fullstack": 8
            },
            "code_patterns": ["Router", "View", "Controller", "Middleware", "API"],
            "imports": ["flask", "django", "fastapi", "streamlit", "requests"]
        },
        "Data Analysis": {
            "keywords": {
                "pandas": 10, "numpy": 10, "matplotlib": 9, "seaborn": 9,
                "dataframe": 10, "analysis": 8, "visualization": 8,
                "statistics": 7, "csv": 8, "excel": 7, "json": 7,
                "plot": 8, "chart": 7, "analytics": 8, "insight": 7,
                "dataset": 8, "processing": 7, "etl": 8
            },
            "code_patterns": ["DataFrame", "Analyst", "Processor", "Visualizer"],
            "imports": ["pandas", "numpy", "matplotlib", "seaborn", "scipy"]
        },
        "Portfolio Work": {
            "keywords": {
                "portfolio": 10, "showcase": 8, "project": 7, "demo": 7,
                "gallery": 8, "art": 7, "design": 7, "creative": 7,
                "personal": 6, "work": 6, "collection": 7
            },
            "code_patterns": ["Portfolio", "Gallery", "Showcase"],
            "imports": []
        },
        "Documentation": {
            "keywords": {
                "readme": 10, "docs": 10, "documentation": 10,
                "guide": 8, "tutorial": 8, "manual": 8, "wiki": 7,
                "markdown": 9, "md": 8, "sphinx": 8, "mkdocs": 7
            },
            "code_patterns": ["Documentation", "Guide", "Tutorial"],
            "imports": ["sphinx", "mkdocs"]
        },
        "Automation Scripts": {
            "keywords": {
                "automation": 10, "script": 9, "bot": 9, "automate": 9,
                "scheduler": 8, "cron": 7, "task": 8, "workflow": 8,
                "pipeline": 7, "orchestrator": 8, "handler": 7
            },
            "code_patterns": ["Bot", "Automation", "Scheduler", "Pipeline"],
            "imports": ["schedule", "celery", "apscheduler"]
        },
        "Media Content": {
            "keywords": {
                "audio": 10, "video": 10, "image": 10, "media": 10,
                "mp3": 9, "mp4": 9, "jpg": 9, "png": 9,
                "transcribe": 8, "transcription": 8, "edit": 7,
                "convert": 8, "process": 7, "generate": 7
            },
            "code_patterns": ["MediaProcessor", "Transcriber", "Converter"],
            "imports": ["moviepy", "PIL", "librosa", "pydub"]
        },
        "Configuration": {
            "keywords": {
                "config": 10, "settings": 9, "configuration": 10,
                ".env": 10, "yaml": 8, "json": 7, "toml": 8,
                "ini": 7, "properties": 7, "setup": 7
            },
            "code_patterns": ["Config", "Settings", "Configuration"],
            "imports": ["configparser", "yaml", "toml"]
        },
        "Testing": {
            "keywords": {
                "test": 10, "testing": 9, "pytest": 10, "unittest": 9,
                "fixture": 8, "mock": 8, "assert": 7, "coverage": 8
            },
            "code_patterns": ["Test", "TestCase", "Fixture"],
            "imports": ["pytest", "unittest", "mock"]
        }
    }

    # Project context patterns
    PROJECT_CONTEXTS = {
        "As-a-Man-Thinketh": {
            "keywords": ["as-a-man", "thinketh", "audiobook", "napoleon hill"],
            "patterns": ["thinketh", "man thinketh"]
        },
        "YouTube Content": {
            "keywords": ["youtube", "video", "content", "channel", "upload"],
            "patterns": ["youtube", "yt_"]
        },
        "Portfolio Projects": {
            "keywords": ["portfolio", "showcase", "gallery", "art", "design"],
            "patterns": ["portfolio", "gallery"]
        },
        "Claude Courses": {
            "keywords": ["claude", "course", "lesson", "tutorial", "education"],
            "patterns": ["course", "lesson"]
        }
    }

    # Technical debt markers
    TECH_DEBT_MARKERS = ["TODO", "FIXME", "XXX", "HACK", "BUG", "REFACTOR", "OPTIMIZE"]

    def __init__(self, max_file_size: int = 2 * 1024 * 1024):  # 2MB default
        self.max_file_size = max_file_size
        self.analyzed_files: List[FileIntelligence] = []
        self.stats = {
            "total_files": 0,
            "analyzed_files": 0,
            "errors": 0,
            "categories": Counter(),
            "content_types": Counter()
        }

    def analyze_file(self, filepath: Path) -> Optional[FileIntelligence]:
        """Perform comprehensive analysis on a single file"""
        try:
            self.stats["total_files"] += 1

            # Basic file info
            stat = filepath.stat()
            file_size = stat.st_size

            if file_size > self.max_file_size:
                # Sample large files (beginning + end)
                content = self._sample_large_file(filepath)
            else:
                content = self._read_file_with_encoding(filepath)

            if content is None:
                return None

            # Content hash
            content_hash = hashlib.sha256(content.encode('utf-8', errors='ignore')).hexdigest()

            # File type detection
            file_type = self._detect_file_type(filepath, content)
            encoding = self._detect_encoding(filepath)

            # Code metrics (for code files)
            code_metrics = self._analyze_code_metrics(filepath, content) if self._is_code_file(filepath) else CodeMetrics()

            # Semantic analysis
            semantic_analysis = self._perform_semantic_analysis(content, filepath, code_metrics)

            # Relationship mapping
            relationships = self._map_relationships(content, filepath, code_metrics)

            # Quality assessment
            complexity_level = self._assess_complexity(code_metrics)
            documentation_quality = self._assess_documentation(code_metrics, content)
            project_maturity = self._assess_maturity(code_metrics, content)
            technical_debt = self._detect_technical_debt(content)

            # Intelligent categorization
            recommended_category, priority_score, confidence = self._intelligent_categorize(
                semantic_analysis, code_metrics, filepath, content
            )

            # Generate recommendations
            destination_suggestions = self._suggest_destinations(
                recommended_category, semantic_analysis, filepath
            )

            # Extract key phrases
            key_phrases = self._extract_key_phrases(content, semantic_analysis)

            # Generate description
            description = self._generate_description(
                filepath, semantic_analysis, code_metrics, file_size
            )

            intelligence = FileIntelligence(
                filepath=filepath,
                content_hash=content_hash,
                file_size=file_size,
                file_type=file_type,
                encoding=encoding,
                code_metrics=code_metrics,
                semantic_analysis=semantic_analysis,
                relationships=relationships,
                complexity_level=complexity_level,
                documentation_quality=documentation_quality,
                project_maturity=project_maturity,
                technical_debt=technical_debt,
                recommended_category=recommended_category,
                priority_score=priority_score,
                confidence=confidence,
                destination_suggestions=destination_suggestions,
                key_phrases=key_phrases,
                description=description,
                analysis_timestamp=datetime.now()
            )

            self.stats["analyzed_files"] += 1
            self.stats["categories"][recommended_category] += 1
            self.stats["content_types"][file_type] += 1

            return intelligence

        except Exception as e:
            self.stats["errors"] += 1
            error_msg = f"Error analyzing {filepath}: {str(e)}"
            print(f"⚠️  {error_msg}")
            traceback.print_exc()
            return None

    def analyze_directory(self, directory: Path, max_files: Optional[int] = None) -> List[FileIntelligence]:
        """
        Analyze all files in a directory with UNLIMITED DEPTH traversal.

        Uses os.walk() which recursively processes all subdirectories
        at any depth level - no artificial depth limits applied.
        """
        directory = Path(directory)
        if not directory.exists():
            print(f"⚠️  Directory not found: {directory}")
            return []

        print(f"🔍 Analyzing directory: {directory}")
        print("📂 Processing all subdirectories (unlimited depth)...")
        print("=" * 70)

        files_analyzed = 0
        # os.walk() traverses ALL directory levels recursively - unlimited depth
        for root, dirs, files in os.walk(directory):
            # Skip common ignore patterns (but continue traversing subdirectories)
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]

            for filename in files:
                if filename.startswith('.'):
                    continue

                filepath = Path(root) / filename

                # Skip very large files or binaries
                try:
                    if filepath.stat().st_size > 10 * 1024 * 1024:  # Skip > 10MB
                        continue
                except:
                    continue

                intelligence = self.analyze_file(filepath)
                if intelligence:
                    self.analyzed_files.append(intelligence)
                    files_analyzed += 1

                    if files_analyzed % 10 == 0:
                        print(f"   Analyzed {files_analyzed} files...")

                    if max_files and files_analyzed >= max_files:
                        break

            if max_files and files_analyzed >= max_files:
                break

        print(f"\n✅ Analysis complete: {files_analyzed} files analyzed")
        return self.analyzed_files

    def _read_file_with_encoding(self, filepath: Path) -> Optional[str]:
        """Read file with intelligent encoding detection"""
        try:
            # Try UTF-8 first (most common)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except:
            try:
                # Detect encoding
                with open(filepath, 'rb') as f:
                    raw_data = f.read()
                    detected = chardet.detect(raw_data)
                    encoding = detected.get('encoding', 'utf-8')

                with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
                    return f.read()
            except:
                return None

    def _sample_large_file(self, filepath: Path, sample_size: int = 10000) -> str:
        """Sample beginning and end of large files"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                beginning = f.read(sample_size)
                f.seek(0, 2)  # Seek to end
                file_size = f.tell()
                if file_size > sample_size * 2:
                    f.seek(file_size - sample_size)
                    end = f.read(sample_size)
                    return beginning + "\n... [FILE TRUNCATED] ...\n" + end
                return beginning
        except:
            return ""

    def _detect_encoding(self, filepath: Path) -> str:
        """Detect file encoding"""
        if HAS_CHARDET:
            try:
                with open(filepath, 'rb') as f:
                    raw_data = f.read(10000)  # Sample first 10KB
                    detected = chardet.detect(raw_data)
                    return detected.get('encoding', 'utf-8')
            except:
                pass
        return 'utf-8'

    def _detect_file_type(self, filepath: Path, content: str) -> str:
        """Detect file type from extension and content"""
        ext = filepath.suffix.lower()

        # Content-based detection
        content_lower = content[:1000].lower()

        if ext in ['.py']:
            return 'python'
        elif ext in ['.md', '.markdown']:
            return 'markdown'
        elif ext in ['.html', '.htm']:
            return 'html'
        elif ext in ['.js', '.jsx']:
            return 'javascript'
        elif ext in ['.json']:
            return 'json'
        elif ext in ['.yaml', '.yml']:
            return 'yaml'
        elif ext in ['.csv']:
            return 'csv'
        elif ext in ['.txt']:
            if any(marker in content for marker in ['#', '```', '---']):
                return 'markdown'
            return 'text'
        else:
            return ext[1:] if ext else 'unknown'

    def _is_code_file(self, filepath: Path) -> bool:
        """Check if file is a code file"""
        code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.go', '.rs', '.rb'}
        return filepath.suffix.lower() in code_extensions

    def _analyze_code_metrics(self, filepath: Path, content: str) -> CodeMetrics:
        """Analyze code metrics using AST"""
        metrics = CodeMetrics()

        try:
            if filepath.suffix.lower() == '.py':
                tree = ast.parse(content, filename=str(filepath))

                # Count functions and classes
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        metrics.functions += 1
                        # Check for docstrings
                        if ast.get_docstring(node):
                            metrics.has_docstrings = True
                        # Check for type hints
                        if node.returns or any(arg.annotation for arg in node.args.args):
                            metrics.has_type_hints = True

                    elif isinstance(node, ast.ClassDef):
                        metrics.classes += 1
                        if ast.get_docstring(node):
                            metrics.has_docstrings = True

                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            metrics.imports.append(alias.name)

                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            metrics.imports.append(node.module)

                # Count lines of code (non-empty, non-comment)
                lines = content.split('\n')
                metrics.lines_of_code = sum(1 for line in lines
                                          if line.strip() and not line.strip().startswith('#'))

        except SyntaxError:
            pass
        except Exception:
            pass

        # Detect technical debt
        content_upper = content.upper()
        for marker in self.TECH_DEBT_MARKERS:
            if marker in content_upper:
                metrics.technical_debt_markers.append(marker)

        return metrics

    def _perform_semantic_analysis(self, content: str, filepath: Path, code_metrics: CodeMetrics) -> SemanticAnalysis:
        """Perform semantic analysis to categorize content"""
        analysis = SemanticAnalysis()
        content_lower = content.lower()
        filename_lower = filepath.name.lower()
        all_text = f"{content_lower} {filename_lower}"

        # Score each category
        category_scores = {}

        for category, config in self.SEMANTIC_CATEGORIES.items():
            score = 0.0

            # Keyword scoring
            for keyword, weight in config["keywords"].items():
                count = all_text.count(keyword.lower())
                score += count * weight

            # Code pattern scoring (from function/class names)
            if code_metrics.functions > 0 or code_metrics.classes > 0:
                all_names = ' '.join(code_metrics.imports)
                for pattern in config["code_patterns"]:
                    if pattern.lower() in all_names.lower():
                        score += 5

            # Import-based scoring
            for import_name in code_metrics.imports:
                if any(imp in import_name.lower() for imp in config["imports"]):
                    score += 10

            category_scores[category] = score

        # Determine primary and secondary categories
        if category_scores:
            sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
            analysis.primary_category = sorted_categories[0][0]
            analysis.secondary_categories = [cat for cat, score in sorted_categories[1:4] if score > 0]

            # Calculate confidence (normalized score)
            max_score = sorted_categories[0][1]
            total_score = sum(category_scores.values())
            analysis.confidence_score = max_score / total_score if total_score > 0 else 0.0
            analysis.keyword_scores = category_scores

        # Detect content type
        analysis.content_type = self._detect_file_type(filepath, content)

        # Detect project context
        for context_name, context_config in self.PROJECT_CONTEXTS.items():
            if any(keyword in all_text for keyword in context_config["keywords"]):
                analysis.project_context = context_name
                break

        return analysis

    def _map_relationships(self, content: str, filepath: Path, code_metrics: CodeMetrics) -> RelationshipMapping:
        """Map file relationships and dependencies"""
        mapping = RelationshipMapping()

        # Import relationships (already in code_metrics)
        mapping.imports = code_metrics.imports.copy()

        # Extract import_from statements
        if filepath.suffix.lower() == '.py':
            try:
                tree = ast.parse(content, filename=str(filepath))
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        if node.module:
                            mapping.imports_from.append(node.module)
            except:
                pass

        # Find file references
        file_ref_pattern = r'["\']([^"\']+\.(py|json|yaml|yml|txt|md|html|css|js))["\']'
        mapping.referenced_files = list(set(re.findall(file_ref_pattern, content)))

        # Find URLs
        url_pattern = r'https?://[^\s<>"\'{}|\\^`\[\]]+'
        mapping.external_urls = list(set(re.findall(url_pattern, content)))

        # Version patterns
        version_patterns = [
            r'version\s*[=:]\s*["\']?([\d.]+)["\']?',
            r'__version__\s*=\s*["\']([\d.]+)["\']',
            r'v?(\d+\.\d+\.\d+)'
        ]
        for pattern in version_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            mapping.version_patterns.extend(matches)

        # Date markers
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',
            r'\d{2}/\d{2}/\d{4}',
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
        ]
        for pattern in date_patterns:
            matches = re.findall(pattern, content)
            mapping.date_markers.extend(matches)

        return mapping

    def _assess_complexity(self, code_metrics: CodeMetrics) -> str:
        """Assess code complexity"""
        if code_metrics.lines_of_code == 0:
            return "unknown"

        complexity_score = (
            code_metrics.functions * 2 +
            code_metrics.classes * 5 +
            code_metrics.lines_of_code / 100
        )

        if complexity_score < 10:
            return "low"
        elif complexity_score < 50:
            return "medium"
        else:
            return "high"

    def _assess_documentation(self, code_metrics: CodeMetrics, content: str) -> str:
        """Assess documentation quality"""
        if code_metrics.functions == 0 and code_metrics.classes == 0:
            return "unknown"

        doc_ratio = 0.0
        if code_metrics.has_docstrings:
            doc_ratio += 0.5
        if code_metrics.has_type_hints:
            doc_ratio += 0.3

        # Count comment lines
        comment_lines = sum(1 for line in content.split('\n') if line.strip().startswith('#'))
        total_lines = len(content.split('\n'))
        if total_lines > 0:
            doc_ratio += (comment_lines / total_lines) * 0.2

        if doc_ratio < 0.3:
            return "low"
        elif doc_ratio < 0.6:
            return "medium"
        else:
            return "high"

    def _assess_maturity(self, code_metrics: CodeMetrics, content: str) -> str:
        """Assess project maturity"""
        if code_metrics.lines_of_code == 0:
            return "unknown"

        # Maturity indicators
        has_structure = code_metrics.classes > 0
        has_type_hints = code_metrics.has_type_hints
        has_docs = code_metrics.has_docstrings
        has_debt = len(code_metrics.technical_debt_markers) > 0

        maturity_score = 0
        if has_structure:
            maturity_score += 1
        if has_type_hints:
            maturity_score += 1
        if has_docs:
            maturity_score += 1
        if not has_debt:
            maturity_score += 1

        if maturity_score < 2:
            return "low"
        elif maturity_score < 4:
            return "medium"
        else:
            return "high"

    def _detect_technical_debt(self, content: str) -> List[str]:
        """Detect technical debt markers"""
        debt = []
        content_upper = content.upper()

        for marker in self.TECH_DEBT_MARKERS:
            if marker in content_upper:
                # Extract context
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if marker in line.upper():
                        debt.append(f"{marker}: {line.strip()[:50]}")
                        break

        return debt[:5]  # Limit to 5

    def _intelligent_categorize(
        self,
        semantic: SemanticAnalysis,
        code_metrics: CodeMetrics,
        filepath: Path,
        content: str
    ) -> Tuple[str, float, float]:
        """Intelligent categorization with priority scoring"""

        # Use semantic analysis primary category
        category = semantic.primary_category if semantic.primary_category else "Uncategorized"

        # Calculate priority score (0-100)
        priority = 0.0

        # Base priority from semantic confidence
        priority += semantic.confidence_score * 40

        # Code quality boosts priority
        if code_metrics.classes > 0:
            priority += 10
        if code_metrics.functions > 5:
            priority += 10
        if code_metrics.has_docstrings:
            priority += 10

        # File size consideration (larger files often more important)
        file_size_mb = filepath.stat().st_size / (1024 * 1024)
        priority += min(file_size_mb * 2, 20)

        # Project context boost
        if semantic.project_context:
            priority += 10

        priority = min(priority, 100.0)

        # Confidence is semantic confidence
        confidence = semantic.confidence_score

        return category, priority, confidence

    def _suggest_destinations(
        self,
        category: str,
        semantic: SemanticAnalysis,
        filepath: Path
    ) -> List[str]:
        """Suggest intelligent destination paths"""
        suggestions = []

        base_path = "~/Documents/CsV"

        # Category-based paths
        category_map = {
            "AI/ML": f"{base_path}/AI-ML",
            "Web Development": f"{base_path}/Web-Development",
            "Data Analysis": f"{base_path}/Data-Analysis",
            "Portfolio Work": f"{base_path}/Portfolio",
            "Documentation": f"{base_path}/Documentation",
            "Automation Scripts": f"{base_path}/Automation",
            "Media Content": f"{base_path}/Media",
            "Configuration": f"{base_path}/Configuration",
            "Testing": f"{base_path}/Testing"
        }

        if category in category_map:
            base = category_map[category]

            # Add project context subdirectory
            if semantic.project_context:
                context_map = {
                    "As-a-Man-Thinketh": "As-a-Man-Thinketh",
                    "YouTube Content": "YouTube-Content",
                    "Portfolio Projects": "Portfolio",
                    "Claude Courses": "Claude-Courses"
                }
                if semantic.project_context in context_map:
                    base = f"{base}/{context_map[semantic.project_context]}"

            # Add maturity/quality subdirectory
            suggestions.append(f"{base}/Production")
            suggestions.append(f"{base}/Experimental")

        return suggestions[:3]  # Limit to 3 suggestions

    def _extract_key_phrases(self, content: str, semantic: SemanticAnalysis) -> List[str]:
        """Extract key phrases from content"""
        phrases = []

        # Get top keywords from semantic analysis
        if semantic.keyword_scores:
            top_keywords = sorted(semantic.keyword_scores.items(), key=lambda x: x[1], reverse=True)[:5]
            phrases.extend([kw for kw, score in top_keywords if score > 5])

        # Extract capitalized phrases (potential proper nouns/titles)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content[:500])
        phrases.extend([p for p in capitalized[:3] if len(p) > 3])

        return list(set(phrases))[:10]

    def _generate_description(
        self,
        filepath: Path,
        semantic: SemanticAnalysis,
        code_metrics: CodeMetrics,
        file_size: int
    ) -> str:
        """Generate intelligent description"""
        parts = []

        # Size description
        if file_size < 1024:
            parts.append("Small file")
        elif file_size < 1024 * 100:
            parts.append("Medium file")
        else:
            parts.append("Large file")

        # Content type
        if semantic.content_type:
            parts.append(f"{semantic.content_type.title()} content")

        # Category
        if semantic.primary_category:
            parts.append(f"{semantic.primary_category} related")

        # Project context
        if semantic.project_context:
            parts.append(f"Part of '{semantic.project_context}' project")

        # Code characteristics
        if code_metrics.functions > 0:
            parts.append(f"{code_metrics.functions} functions")
        if code_metrics.classes > 0:
            parts.append(f"{code_metrics.classes} classes")

        return " | ".join(parts)

    def generate_report(self, output_path: Path) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Prepare report data
        report_data = {
            "timestamp": timestamp,
            "analysis_date": datetime.now().isoformat(),
            "statistics": {
                "total_files": self.stats["total_files"],
                "analyzed_files": self.stats["analyzed_files"],
                "errors": self.stats["errors"],
                "categories": dict(self.stats["categories"]),
                "content_types": dict(self.stats["content_types"])
            },
            "files": []
        }

        # Add file intelligence (simplified for JSON)
        for intelligence in self.analyzed_files:
            file_data = {
                "filepath": str(intelligence.filepath),
                "category": intelligence.recommended_category,
                "priority": intelligence.priority_score,
                "confidence": intelligence.confidence,
                "description": intelligence.description,
                "complexity": intelligence.complexity_level,
                "maturity": intelligence.project_maturity,
                "destination_suggestions": intelligence.destination_suggestions
            }
            report_data["files"].append(file_data)

        # Save JSON report
        json_file = output_path / f"advanced_content_analysis_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)

        # Generate markdown report
        md_file = output_path / f"ADVANCED_CONTENT_ANALYSIS_{timestamp}.md"
        with open(md_file, 'w') as f:
            f.write(self._generate_markdown_report(report_data))

        # Generate CSV report with improved sorting and organization
        csv_file = output_path / f"advanced_content_analysis_{timestamp}.csv"
        self._generate_csv_report(csv_file, self.analyzed_files)

        print(f"\n💾 Reports saved:")
        print(f"   - JSON: {json_file.name}")
        print(f"   - Markdown: {md_file.name}")
        print(f"   - CSV: {csv_file.name}")

        return report_data

    def _generate_csv_report(self, csv_file: Path, analyzed_files: List[FileIntelligence]):
        """Generate comprehensive CSV report with improved sorting and organization"""

        # Sort files by priority (highest first), then by category, then by confidence
        sorted_files = sorted(
            analyzed_files,
            key=lambda x: (x.priority_score, x.confidence, x.recommended_category),
            reverse=True
        )

        # Prepare CSV data with all relevant columns
        csv_rows = []

        for intelligence in sorted_files:
            # Generate improvement suggestions
            improvements = self._generate_improvements(intelligence)

            # Generate organizational suggestions
            org_suggestions = self._generate_organizational_suggestions(intelligence)

            # Prepare row data
            row = {
                # File Information
                "File Path": str(intelligence.filepath),
                "Filename": intelligence.filepath.name,
                "Directory": str(intelligence.filepath.parent),

                # Analysis Results
                "Category": intelligence.recommended_category,
                "Priority Score": f"{intelligence.priority_score:.2f}",
                "Confidence": f"{intelligence.confidence:.2%}",
                "Content Type": intelligence.file_type,
                "File Size (bytes)": intelligence.file_size,
                "File Size (human)": self._format_size(intelligence.file_size),

                # Quality Metrics
                "Complexity Level": intelligence.complexity_level,
                "Documentation Quality": intelligence.documentation_quality,
                "Project Maturity": intelligence.project_maturity,
                "Code Functions": intelligence.code_metrics.functions,
                "Code Classes": intelligence.code_metrics.classes,
                "Lines of Code": intelligence.code_metrics.lines_of_code,
                "Has Docstrings": "Yes" if intelligence.code_metrics.has_docstrings else "No",
                "Has Type Hints": "Yes" if intelligence.code_metrics.has_type_hints else "No",

                # Semantic Analysis
                "Primary Category": intelligence.semantic_analysis.primary_category,
                "Secondary Categories": "; ".join(intelligence.semantic_analysis.secondary_categories[:3]),
                "Project Context": intelligence.semantic_analysis.project_context or "General",
                "Semantic Confidence": f"{intelligence.semantic_analysis.confidence_score:.2%}",

                # Relationships
                "Import Count": len(intelligence.relationships.imports),
                "Key Imports": "; ".join(intelligence.relationships.imports[:5]),
                "External URLs": len(intelligence.relationships.external_urls),
                "Referenced Files": len(intelligence.relationships.referenced_files),

                # Technical Debt
                "Technical Debt Markers": "; ".join(intelligence.technical_debt[:3]) if intelligence.technical_debt else "None",
                "Debt Count": len(intelligence.technical_debt),

                # Recommendations
                "Primary Destination": intelligence.destination_suggestions[0] if intelligence.destination_suggestions else "",
                "All Destination Suggestions": " | ".join(intelligence.destination_suggestions),
                "Key Phrases": "; ".join(intelligence.key_phrases[:5]),
                "Description": intelligence.description,

                # Improvements & Suggestions
                "Improvements": " | ".join(improvements),
                "Organizational Suggestions": " | ".join(org_suggestions),
                "Action Items": self._generate_action_items(intelligence, improvements, org_suggestions),

                # Metadata
                "Content Hash": intelligence.content_hash[:16] + "...",  # Shortened hash
                "Encoding": intelligence.encoding,
                "Analysis Timestamp": intelligence.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }

            csv_rows.append(row)

        # Write CSV file
        if csv_rows:
            fieldnames = list(csv_rows[0].keys())
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_rows)

    def _generate_improvements(self, intelligence: FileIntelligence) -> List[str]:
        """Generate improvement suggestions for a file"""
        improvements = []

        # Documentation improvements
        if not intelligence.code_metrics.has_docstrings and intelligence.code_metrics.functions > 0:
            improvements.append("Add docstrings to functions")
        if not intelligence.code_metrics.has_type_hints and intelligence.code_metrics.functions > 0:
            improvements.append("Add type hints for better code clarity")

        # Quality improvements
        if intelligence.complexity_level == "high":
            improvements.append("Consider refactoring to reduce complexity")
        if intelligence.documentation_quality == "low" and intelligence.code_metrics.lines_of_code > 50:
            improvements.append("Improve documentation and add comments")

        # Technical debt
        if intelligence.technical_debt:
            improvements.append(f"Address {len(intelligence.technical_debt)} technical debt markers")

        # Maturity improvements
        if intelligence.project_maturity == "low" and intelligence.code_metrics.classes == 0:
            improvements.append("Consider organizing code into classes/modules")

        # Code structure
        if intelligence.code_metrics.functions > 20 and intelligence.code_metrics.classes == 0:
            improvements.append("Consider organizing functions into classes")

        return improvements[:5]  # Limit to 5 improvements

    def _generate_organizational_suggestions(self, intelligence: FileIntelligence) -> List[str]:
        """Generate organizational suggestions"""
        suggestions = []

        # Category-based organization
        if intelligence.recommended_category:
            suggestions.append(f"Organize under {intelligence.recommended_category} category")

        # Project context organization
        if intelligence.semantic_analysis.project_context:
            suggestions.append(f"Group with {intelligence.semantic_analysis.project_context} project files")

        # Quality-based organization
        if intelligence.project_maturity == "high":
            suggestions.append("Place in Production/Stable directory")
        elif intelligence.project_maturity == "low":
            suggestions.append("Place in Experimental/Development directory")

        # Size-based organization
        if intelligence.file_size > 1024 * 100:  # > 100KB
            suggestions.append("Consider if this large file should be archived")

        # Relationship-based organization
        if intelligence.relationships.imports:
            suggestions.append(f"Group with files using similar imports ({len(intelligence.relationships.imports)} imports)")

        return suggestions[:5]  # Limit to 5 suggestions

    def _generate_action_items(self, intelligence: FileIntelligence, improvements: List[str], org_suggestions: List[str]) -> str:
        """Generate actionable items"""
        actions = []

        # High priority actions
        if intelligence.priority_score > 70:
            actions.append("HIGH PRIORITY: Review and organize")

        if intelligence.technical_debt and len(intelligence.technical_debt) > 3:
            actions.append("URGENT: Address technical debt")

        if improvements:
            actions.append(f"Improve: {improvements[0]}")

        if org_suggestions:
            actions.append(f"Organize: {org_suggestions[0]}")

        # Low confidence files need review
        if intelligence.confidence < 0.5:
            actions.append("REVIEW: Low confidence categorization - verify manually")

        return " | ".join(actions[:3])  # Limit to 3 action items

    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    def _generate_markdown_report(self, report_data: Dict[str, Any]) -> str:
        """Generate comprehensive markdown report"""
        md = f"""# 🧠 ADVANCED CONTENT-AWARE INTELLIGENT ANALYSIS
## Comprehensive Intelligence Report

**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}
**Analysis ID:** {report_data['timestamp']}

---

## 📊 EXECUTIVE SUMMARY

### Analysis Statistics
- **Total Files Processed:** {report_data['statistics']['total_files']}
- **Successfully Analyzed:** {report_data['statistics']['analyzed_files']}
- **Errors:** {report_data['statistics']['errors']}

### Category Distribution
"""
        for category, count in sorted(report_data['statistics']['categories'].items(), key=lambda x: x[1], reverse=True):
            md += f"- **{category}:** {count} files\n"

        md += f"""
### Content Types
"""
        for content_type, count in sorted(report_data['statistics']['content_types'].items(), key=lambda x: x[1], reverse=True):
            md += f"- **{content_type}:** {count} files\n"

        md += f"""
---

## 📋 FILE INTELLIGENCE REPORT

"""
        # Group by category
        by_category = defaultdict(list)
        for file_data in report_data['files']:
            by_category[file_data['category']].append(file_data)

        for category, files in sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True):
            md += f"""### {category} ({len(files)} files)

"""
            # Sort by priority
            files_sorted = sorted(files, key=lambda x: x['priority'], reverse=True)

            for file_data in files_sorted[:20]:  # Top 20 per category
                md += f"""#### {Path(file_data['filepath']).name}

- **Path:** `{file_data['filepath']}`
- **Priority:** {file_data['priority']:.1f}/100
- **Confidence:** {file_data['confidence']:.2%}
- **Complexity:** {file_data['complexity']}
- **Maturity:** {file_data['maturity']}
- **Description:** {file_data['description']}
- **Suggested Destinations:**
"""
                for dest in file_data['destination_suggestions']:
                    md += f"  - `{dest}`\n"
                md += "\n"

            if len(files_sorted) > 20:
                md += f"\n*... and {len(files_sorted) - 20} more files*\n\n"

        md += f"""
---

**Analysis Complete** ✅

*This report was generated using advanced content-aware intelligence analysis.*
"""
        return md


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(
        description='🧠 Advanced Content-Aware Intelligent Analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('directory', type=Path, help='Directory to analyze')
    parser.add_argument('--output', type=Path, default='~/analysis_reports',
                       help='Output directory for reports (default: ~/analysis_reports)')
    parser.add_argument('--max-files', type=int, default=None,
                       help='Maximum number of files to analyze')
    parser.add_argument('--max-size', type=int, default=2 * 1024 * 1024,
                       help='Maximum file size to analyze (default: 2MB)')

    args = parser.parse_args()

    analyzer = AdvancedContentAnalyzer(max_file_size=args.max_size)

    print("🧠 ADVANCED CONTENT-AWARE INTELLIGENT ANALYZER")
    print("=" * 70)
    print()

    # Analyze directory
    analyzer.analyze_directory(args.directory, max_files=args.max_files)

    # Generate report
    output_dir = Path(args.output).expanduser()
    report = analyzer.generate_report(output_dir)

    # Print summary
    print("\n" + "=" * 70)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 70)
    print(f"\nFiles Analyzed: {report['statistics']['analyzed_files']}")
    print(f"Categories Found: {len(report['statistics']['categories'])}")
    print(f"Content Types: {len(report['statistics']['content_types'])}")
    print("\nTop Categories:")
    for category, count in sorted(report['statistics']['categories'].items(),
                                  key=lambda x: x[1], reverse=True)[:5]:
        print(f"  - {category}: {count} files")

    print("\n✅ Analysis complete!")


if __name__ == '__main__':
    main()


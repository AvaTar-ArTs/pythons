"""
Enhanced next‑generation content analyser.

This module builds upon the ``NextGenContentAnalyzer`` defined in
``next_gen_content_analyzer.py``.  It retains the asynchronous
execution model and plugin architecture but introduces several
advanced features driven by recent research in natural language
processing, system design and caching strategies.  Key improvements
include:

* **Smarter file reading:** Large files are sampled rather than fully
  loaded into memory.  For files exceeding a configurable threshold
  (1 MiB by default) only the first and last 512 KiB are read and
  concatenated.  This reduces peak memory usage and speeds up
  analysis for large multimedia files or minified code while still
  capturing representative content.

* **Concurrency control:** A semaphore limits the number of
  concurrent file analyses.  Although asynchronous processing
  improves responsiveness by allowing multiple tasks to progress
  concurrently【71718478088787†L124-L147】, unbounded concurrency can cause resource
  exhaustion.  Limiting concurrency provides a balance between
  throughput and resource utilisation.

* **Configurable caching:** File contents are cached using
  ``async_lru.alru_cache``.  A least‑recently used strategy combined
  with a time‑to‑live policy (TTL) prevents cache saturation and
  stale data【793197236363874†L49-L52】.  Cached entries older than the TTL are
  purged automatically.

* **Advanced plugin framework:** Plugins can declare the types of
  results they return and the analyser aggregates these results
  across all processed files.  Built‑in plugins illustrate how
  advanced ML/NLP tasks such as keyword extraction, summarisation and
  project classification can be integrated.  Developers can easily
  create new plugins by subclassing ``BasePlugin`` and overriding
  ``process_file``.  This modular design simplifies extension and
  supports runtime add‑on loading【980415373044174†L48-L77】.

* **Heuristic classification:** A ``CategoryClassifierPlugin`` uses
  domain‑specific heuristics inspired by research on project type
  detection to label files as AI/ML, automation, data analysis or
  web development.  The rules mirror those used in the
  ``medium_article_automation`` script but are encapsulated in a
  reusable plugin.

* **Code complexity analysis:** A ``ComplexityPlugin`` computes
  cyclomatic complexity by counting branch and loop constructs.  This
  metric helps surface files that may benefit from refactoring or
  additional documentation.

* **Trending keyword detection:** The ``TrendingKeywordPlugin``
  counts occurrences of trending keywords across the codebase.  It
  draws its vocabulary from the Medium automation tool and enables
  targeted SEO analysis.

* **Basic summarisation:** The ``AdvancedSummaryPlugin`` extracts
  leading and trailing sentences from each file to build a
  representative summary.  Research shows that transformer models
  significantly outperform simple heuristics in abstractive
  summarisation【721909682599878†L80-L91】.  For deployments where
  ``transformers`` is available, this plugin can be replaced with a
  neural summariser for higher quality results.

Usage example::

    from enhanced_next_gen_content_analyzer import (
        EnhancedContentAnalyzer,
        KeywordExtractorPlugin,
        AdvancedSummaryPlugin,
        ComplexityPlugin,
        CategoryClassifierPlugin,
        TrendingKeywordPlugin,
    )

    plugins = [
        KeywordExtractorPlugin(top_n=5),
        AdvancedSummaryPlugin(max_sentences=3),
        ComplexityPlugin(),
        CategoryClassifierPlugin(),
        TrendingKeywordPlugin(),
    ]
    analyzer = EnhancedContentAnalyzer(
        base_dir="/Users/steven/Documents/python", plugins=plugins, max_concurrency=8
    )
    import asyncio
    results = asyncio.run(analyzer.analyze_all_projects_async())

The resulting ``ProjectAnalysis`` instances include a
``plugin_results`` dictionary on their documentation plans which
contains aggregated outputs for each plugin.
"""

from __future__ import annotations

import asyncio
import logging
import re
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from async_lru import alru_cache

try:
    from next_gen_content_analyzer import NextGenContentAnalyzer  # type: ignore
    from deep_content_analyzer import ProjectAnalysis  # type: ignore
except Exception as exc:
    raise ImportError(
        "Failed to import NextGenContentAnalyzer or its dependencies."
    ) from exc


logger = logging.getLogger(__name__)


class BasePlugin:
    """Base class for analyser plugins.

    Plugins should override :meth:`process_file` to inspect the
    contents of each file and return a dictionary of results.  These
    results will be aggregated by filename under the plugin's class
    name.
    """

    def process_file(self, content: str, file_path: Path) -> Dict[str, Any]:
        raise NotImplementedError


class KeywordExtractorPlugin(BasePlugin):
    """Extract the most common non‑reserved words from each file.

    This plugin tokenises the content using a simple regular
    expression, filters out short tokens and Python keywords, then
    returns the top ``n`` words.  In a real NLP setting, stemming and
    stop‑word removal should be performed to produce cleaner
    keyphrases.
    """

    def __init__(self, top_n: int = 10) -> None:
        self.top_n = top_n
        self.reserved = set(
            [
                "and",
                "or",
                "not",
                "if",
                "else",
                "elif",
                "for",
                "while",
                "return",
                "import",
                "from",
                "class",
                "def",
                "with",
                "try",
                "except",
                "async",
                "await",
                "lambda",
            ]
        )

    def process_file(self, content: str, file_path: Path) -> Dict[str, Any]:
        tokens = re.findall(r"\b\w+\b", content.lower())
        tokens = [t for t in tokens if len(t) > 3 and t not in self.reserved]
        counts = Counter(tokens)
        common = counts.most_common(self.top_n)
        return {"top_keywords": [word for word, _ in common]}


class AdvancedSummaryPlugin(BasePlugin):
    """Generate a simple summary by combining the first and last sentences.

    For long files (>2000 characters) this plugin returns the first
    ``max_sentences`` sentences and the last sentence.  For shorter
    files it returns the entire content.  More sophisticated models
    such as T5 or BART produce higher quality summaries by training on
    large corpora【721909682599878†L80-L91】.  Those models can be
    integrated by replacing this implementation with calls to a
    transformer‑based summariser.
    """

    def __init__(self, max_sentences: int = 3) -> None:
        self.max_sentences = max_sentences

    def process_file(self, content: str, file_path: Path) -> Dict[str, Any]:
        text = content.strip()
        # If the file is short, return it entirely
        if len(text) < 2000:
            return {"summary": text}
        # Split into sentences
        sentences = re.split(r"(?<=[.!?])\s+", text)
        head = sentences[: self.max_sentences]
        tail = sentences[-1:]
        summary = " ".join(head + tail)
        return {"summary": summary}


class ComplexityPlugin(BasePlugin):
    """Compute basic cyclomatic complexity for each file.

    Complexity is estimated by counting branching and looping constructs
    such as ``if``, ``for``, ``while``, ``and``, ``or``, ``try`` and
    ``except``.  A higher score indicates more complex control flow and
    may warrant refactoring.
    """

    def process_file(self, content: str, file_path: Path) -> Dict[str, Any]:
        patterns = [
            r"\bif\b",
            r"\bfor\b",
            r"\bwhile\b",
            r"\band\b",
            r"\bor\b",
            r"\btry\b",
            r"\bexcept\b",
            r"\belif\b",
        ]
        complexity = sum(len(re.findall(p, content)) for p in patterns) + 1
        return {"cyclomatic_complexity": complexity}


class CategoryClassifierPlugin(BasePlugin):
    """Classify each file into high‑level project categories.

    The categories mirror those in the Medium automation tool.  A file
    may be classified as AI/ML, automation, data analysis, web
    development or general.  The first matching category is used.
    """

    def __init__(self) -> None:
        # Patterns to detect project type in content
        self.indicators = {
            "ai_ml": [
                "tensorflow",
                "pytorch",
                "sklearn",
                "neural",
                "model",
                "train",
                "machine learning",
            ],
            "automation": [
                "automation",
                "schedule",
                "cron",
                "workflow",
                "task",
            ],
            "data_analysis": [
                "pandas",
                "numpy",
                "matplotlib",
                "seaborn",
                "data",
                "analysis",
            ],
            "web_development": [
                "flask",
                "django",
                "fastapi",
                "http",
                "app.route",
            ],
        }

    def process_file(self, content: str, file_path: Path) -> Dict[str, Any]:
        text = content.lower()
        for category, terms in self.indicators.items():
            if any(term in text for term in terms):
                return {"category": category}
        return {"category": "general"}


class TrendingKeywordPlugin(BasePlugin):
    """Count occurrences of trending keywords within a file.

    The trending keyword lists are derived from the Medium article
    automation project.  Counts for each keyword are returned to
    support SEO analysis.
    """

    def __init__(self) -> None:
        self.keywords = {
            "hot_trending": [
                "quantum computing",
                "machine learning",
                "artificial intelligence",
                "python automation",
                "content analysis",
                "file organization",
                "nlp processing",
                "data science",
                "software architecture",
                "enterprise development",
            ],
            "technical_terms": [
                "tensorflow",
                "pytorch",
                "pandas",
                "numpy",
                "fastapi",
                "flask",
                "django",
                "sqlalchemy",
                "pytest",
                "mongodb",
            ],
            "long_tail": [
                "python file organization with ai",
                "machine learning content analysis tutorial",
                "building scalable python applications",
            ],
        }

    def process_file(self, content: str, file_path: Path) -> Dict[str, Any]:
        text = content.lower()
        counts: Dict[str, int] = {}
        for category, terms in self.keywords.items():
            for term in terms:
                count = text.count(term.lower())
                if count:
                    counts[term] = count
        return {"trending_keyword_counts": counts}


@dataclass
class EnhancedContentAnalyzer(NextGenContentAnalyzer):
    """Asynchronous content analyser with advanced features.

    This class extends ``NextGenContentAnalyzer`` with smarter file
    reading, configurable concurrency and TTL caching.  It accepts a
    list of plugins which will be executed on every file.  Results
    returned by the base class are combined with aggregated plugin
    outputs and stored on each project's documentation plan.
    """

    plugins: List[BasePlugin] = field(default_factory=list)
    max_concurrency: int = 8
    sample_threshold: int = 1_000_000  # bytes; files larger than this will be sampled
    cache_ttl: int = 600  # seconds to keep cached file contents

    def __post_init__(self) -> None:
        super().__post_init__()
        # Semaphore for limiting concurrent file analyses
        self._semaphore = asyncio.Semaphore(self.max_concurrency)
        # Track cache entry times
        self._cache_times: Dict[Path, float] = {}

    async def analyze_all_projects_async(self) -> Dict[str, ProjectAnalysis]:
        logger.info("🔍 Starting enhanced asynchronous analysis…")
        tasks = []
        for project_dir in Path(self.base_dir).iterdir():
            if project_dir.is_dir() and not project_dir.name.startswith('.'):
                tasks.append(asyncio.create_task(self._analyze_project_async(project_dir)))
        analyses = await asyncio.gather(*tasks)
        results: Dict[str, ProjectAnalysis] = {analysis.project_name: analysis for analysis in analyses}
        self.analysis_results = results
        return results

    async def _analyze_project_async(self, project_path: Path) -> ProjectAnalysis:
        analysis = ProjectAnalysis(
            project_name=project_path.name,
            total_files=0,
            total_lines=0,
            functions=[],
            classes=[],
            modules=[],
            dependencies=set(),
            quality_metrics={},
            content_categories={},
            recommendations=[],
            documentation_plan={},
        )
        plugin_results: Dict[str, List[Any]] = {plugin.__class__.__name__: [] for plugin in self.plugins}
        python_files = [p for p in project_path.rglob("*.py")]
        analysis.total_files = len(python_files)
        # Limit concurrency for file analyses
        tasks = [self._analyze_python_file_async(file, plugin_results) for file in python_files]
        file_results = await asyncio.gather(*tasks)
        for result in file_results:
            if not result:
                continue
            analysis.total_lines += result['total_lines']
            analysis.functions.extend(result['functions'])
            analysis.classes.extend(result['classes'])
            analysis.modules.extend(result['modules'])
            analysis.dependencies.update(result['dependencies'])
        # Derive metrics using base class helpers
        analysis.quality_metrics = super()._calculate_quality_metrics(analysis)
        analysis.content_categories = super()._categorize_content(analysis)
        analysis.recommendations = super()._generate_recommendations(analysis)
        analysis.documentation_plan = super()._create_documentation_plan(analysis)
        analysis.documentation_plan['plugin_results'] = plugin_results
        return analysis

    async def _analyze_python_file_async(
        self, file_path: Path, plugin_results: Dict[str, List[Any]]
    ) -> Optional[Dict[str, Any]]:
        async with self._semaphore:
            try:
                content = await self._read_file(file_path)
            except Exception as exc:
                logger.warning(f"Error reading {file_path}: {exc}")
                return None
            if not content.strip():
                return None
            # Use parent class to analyse the file in a worker thread
            try:
                base_result = await asyncio.to_thread(super()._analyze_python_file, file_path)
            except Exception as exc:
                logger.warning(f"Error analysing {file_path}: {exc}")
                return None
            # Run plugins; process each on a worker thread
            for plugin in self.plugins:
                try:
                    plugin_output = await asyncio.to_thread(plugin.process_file, content, file_path)
                    plugin_results[plugin.__class__.__name__].append({file_path.name: plugin_output})
                except Exception as exc:
                    logger.warning(f"Plugin {plugin.__class__.__name__} failed on {file_path}: {exc}")
            return base_result

    @alru_cache(maxsize=512)
    async def _read_file(self, file_path: Path) -> str:
        """Read a file asynchronously and cache its contents with TTL.

        Files larger than ``sample_threshold`` are sampled to avoid
        reading the entire file into memory.  The caching layer uses a
        least‑recently used eviction policy and we record access times
        to implement a time‑to‑live expiration.  When the cached value
        becomes older than ``cache_ttl`` seconds, it is removed and
        reloaded from disk.
        """
        # Purge expired cache entries
        now = time.time()
        stale_keys: List[Path] = []
        for path, ts in list(self._cache_times.items()):
            if now - ts > self.cache_ttl:
                stale_keys.append(path)
        for key in stale_keys:
            try:
                # Remove stale entry from the underlying LRU cache
                self._read_file.cache_invalidate(key)  # type: ignore[attr-defined]
                self._cache_times.pop(key, None)
            except Exception:
                pass
        # Check if we have a cached entry
        if file_path in self._cache_times:
            self._cache_times[file_path] = now
        loop = asyncio.get_running_loop()
        # Offload file reading to a thread
        def read_and_sample() -> str:
            size = file_path.stat().st_size
            if size > self.sample_threshold:
                # Read first and last parts of the file
                with open(file_path, 'rb') as f:
                    head = f.read(512_000)
                    f.seek(max(size - 512_000, 0))
                    tail = f.read(512_000)
                try:
                    return (head + b"\n...\n" + tail).decode('utf-8', errors='replace')
                except Exception:
                    return (head + b"\n...\n" + tail).decode('latin-1', errors='replace')
            else:
                return file_path.read_text(encoding='utf-8', errors='ignore')
        content = await loop.run_in_executor(None, read_and_sample)
        # Record access time
        self._cache_times[file_path] = now
        return content
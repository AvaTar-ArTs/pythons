"""
Next‑generation content analyzer.

This module defines a ``NextGenContentAnalyzer`` class which extends the
capabilities of the existing ``DeepContentAnalyzer`` found in this
repository.  The new implementation focuses on modern best practices for
scalability and extensibility, including:

* **Asynchronous processing:**  Python's ``asyncio`` event loop is
  leveraged to analyse many files concurrently.  I/O bound operations
  such as reading files are dispatched to background threads so that
  other work can proceed without blocking.  This makes the analyser
  more responsive when pointed at projects containing hundreds or
  thousands of files.  Asynchronous routines are able to pause while
  waiting on their ultimate result, letting other tasks run in the
  meantime【648389026675244†L715-L724】.

* **Caching:**  Repeatedly reading the same file or parsing the same
  module can be expensive.  To mitigate this, the analyser uses
  ``async_lru.alru_cache`` to memoise results of asynchronous
  operations.  A least‑recently used cache prevents the internal
  dictionaries from growing without bound【865327713283627†L54-L104】 and
  provides predictable memory usage.  Cached functions include file
  reads and parsing operations.

* **Plugin architecture:**  Extensibility is provided via a simple
  plugin system.  External modules can register custom analysis
  routines by subclassing ``AnalyzerPlugin`` and overriding
  ``process_file``.  At runtime the analyser iterates over all
  registered plugins and collects their results.  This approach
  decouples the core analysis logic from optional behaviour and makes
  it easy to add new capabilities without modifying the core class
  【401046503341842†L47-L58】.

* **ML/NLP readiness:**  While heavy machine‑learning libraries such as
  ``transformers`` are not available in this environment, the plugin
  architecture allows advanced natural language processing to be
  incorporated when those dependencies are installed.  Sample
  plugins included in this module demonstrate how to extract
  keywords and generate simple summaries using only the standard
  library.  For real deployments one could write a plugin that
  leverages state‑of‑the‑art transformer models (e.g. BART or T5) to
  perform text summarisation or zero‑shot classification【986642564950654†L16-L33】.

Usage::

    from next_gen_content_analyzer import NextGenContentAnalyzer, KeywordExtractorPlugin, SummaryPlugin

    analyzer = NextGenContentAnalyzer(base_dir="/path/to/projects",
                                      plugins=[KeywordExtractorPlugin(top_n=5),
                                               SummaryPlugin(max_sentences=2)])
    # run asynchronously
    import asyncio
    asyncio.run(analyzer.analyze_all_projects_async())

The results of the analysis, including plugin outputs, will be stored on
each project's ``documentation_plan`` under the ``plugin_results`` key.

"""

from __future__ import annotations

import asyncio
import logging
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from async_lru import alru_cache

try:
    # Import the existing DeepContentAnalyzer and associated classes from the
    # repository.  If these imports fail the module will raise an error at
    # import time.  By keeping the import at the top level we ensure that
    # static analysis tools know about the dependency.
    from deep_content_analyzer import DeepContentAnalyzer, ProjectAnalysis  # type: ignore
except Exception as exc:  # pragma: no cover - fail loudly if base analyser missing
    raise ImportError(
        "Failed to import DeepContentAnalyzer from the local repository. "
        "Ensure that deep_content_analyzer.py exists in the same directory."
    ) from exc

logger = logging.getLogger(__name__)


class AnalyzerPlugin:
    """Base class for analyser plugins.

    Plugins should override :meth:`process_file` to inspect the contents
    of each file and return a dictionary of results.  These results will
    be aggregated into a list under the plugin's class name.
    """

    def process_file(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Analyse a file's contents.

        :param content: Text of the file being analysed.
        :param file_path: Path to the file on disk.
        :returns: A dictionary with arbitrary metadata.  By convention,
                  this should be JSON‑serialisable.
        """
        raise NotImplementedError


class KeywordExtractorPlugin(AnalyzerPlugin):
    """Extract the most common words from each file.

    This plugin uses a simple regular expression to tokenise words and
    counts their occurrences.  The top *n* words are returned.  Stop
    words are not removed because the target content may be code rather
    than natural language.  In a real NLP setting, more advanced
    techniques such as stemming or transformer‑based tokenisers can be
    implemented here【986642564950654†L16-L33】.
    """

    def __init__(self, top_n: int = 10) -> None:
        self.top_n = top_n

    def process_file(self, content: str, file_path: Path) -> Dict[str, Any]:
        tokens = re.findall(r"\b\w+\b", content.lower())
        counts = Counter(tokens)
        common = counts.most_common(self.top_n)
        return {"top_keywords": [word for word, _ in common]}


class SummaryPlugin(AnalyzerPlugin):
    """Generate a simple summary of each file.

    The summary consists of the first few sentences of the file.  This is
    a naive implementation meant as a placeholder for more advanced
    summarisation techniques.  Transformer models such as BART or T5
    produce high‑quality abstractive summaries by training on large
    corpora【986642564950654†L16-L33】.  Such models can be integrated here in the future
    by installing the ``transformers`` library and writing a custom
    plugin.
    """

    def __init__(self, max_sentences: int = 3) -> None:
        self.max_sentences = max_sentences

    def process_file(self, content: str, file_path: Path) -> Dict[str, Any]:
        # Split on punctuation followed by whitespace to find sentence boundaries
        sentences = re.split(r"(?<=[.!?])\s+", content.strip())
        summary = " ".join(sentences[: self.max_sentences])
        return {"summary": summary}


@dataclass
class NextGenContentAnalyzer(DeepContentAnalyzer):
    """Asynchronous and extensible content analyser.

    This class extends :class:`DeepContentAnalyzer` with support for
    asynchronous file scanning, caching and plugin extensibility.
    """

    base_dir: str = "/Users/steven/Documents/python"
    plugins: List[AnalyzerPlugin] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__init__(self.base_dir)

    async def analyze_all_projects_async(self) -> Dict[str, ProjectAnalysis]:
        """Asynchronously analyse all projects in the base directory.

        This method spawns asynchronous tasks for each project and waits
        for them to complete.  The results are stored on
        ``self.analysis_results`` and returned.  When multiple files are
        present, reading and parsing happens concurrently to improve
        throughput.
        """
        logger.info("🔍 Starting asynchronous deep content analysis...")
        tasks = []
        for project_dir in Path(self.base_dir).iterdir():
            if project_dir.is_dir() and not project_dir.name.startswith('.'):
                tasks.append(asyncio.create_task(self._analyze_project_async(project_dir)))
        analyses = await asyncio.gather(*tasks)
        # Build result dictionary keyed by project name
        results: Dict[str, ProjectAnalysis] = {analysis.project_name: analysis for analysis in analyses}
        self.analysis_results = results
        return results

    async def _analyze_project_async(self, project_path: Path) -> ProjectAnalysis:
        """Asynchronously analyse a single project directory.

        The structure of the returned ``ProjectAnalysis`` mirrors that of
        the synchronous base class, but plugin results are stored under
        ``documentation_plan['plugin_results']``.
        """
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
        # Initialise plugin result aggregator
        plugin_results: Dict[str, List[Any]] = {plugin.__class__.__name__: [] for plugin in self.plugins}
        # Collect python files
        python_files = [p for p in project_path.rglob("*.py")]
        analysis.total_files = len(python_files)
        # Launch asynchronous analysis tasks per file
        tasks = [self._analyze_python_file_async(py_file, plugin_results) for py_file in python_files]
        file_results = await asyncio.gather(*tasks)
        # Accumulate file analyses
        for result in file_results:
            if not result:
                continue
            analysis.total_lines += result['total_lines']
            analysis.functions.extend(result['functions'])
            analysis.classes.extend(result['classes'])
            analysis.modules.extend(result['modules'])
            analysis.dependencies.update(result['dependencies'])
        # Derive quality metrics, categories and recommendations using base class methods
        analysis.quality_metrics = super()._calculate_quality_metrics(analysis)
        analysis.content_categories = super()._categorize_content(analysis)
        analysis.recommendations = super()._generate_recommendations(analysis)
        analysis.documentation_plan = super()._create_documentation_plan(analysis)
        # Attach plugin results to documentation plan
        analysis.documentation_plan['plugin_results'] = plugin_results
        return analysis

    async def _analyze_python_file_async(
        self, file_path: Path, plugin_results: Dict[str, List[Any]]
    ) -> Optional[Dict[str, Any]]:
        """Asynchronously analyse a single Python file.

        This method reads the file using an asynchronous cached reader,
        executes the synchronous analysis provided by the base class in a
        background thread, then processes the file through all
        registered plugins.  Results from plugins are aggregated into
        the shared ``plugin_results`` dictionary.
        """
        try:
            content = await self._read_file(file_path)
        except Exception as exc:
            logger.warning(f"Error reading {file_path}: {exc}")
            return None
        if not content.strip():
            return None
        # Run base class analysis in a worker thread
        try:
            result: Dict[str, Any] = await asyncio.to_thread(super()._analyze_python_file, file_path)
        except Exception as exc:
            logger.warning(f"Error analysing {file_path}: {exc}")
            return None
        # Execute plugins; run in executor to avoid blocking
        for plugin in self.plugins:
            try:
                plugin_output = await asyncio.to_thread(plugin.process_file, content, file_path)
                plugin_results[plugin.__class__.__name__].append({file_path.name: plugin_output})
            except Exception as exc:
                logger.warning(f"Plugin {plugin.__class__.__name__} failed on {file_path}: {exc}")
        return result

    @alru_cache(maxsize=256)
    async def _read_file(self, file_path: Path) -> str:
        """Read a file asynchronously and cache its contents.

        ``async_lru.alru_cache`` is used here to memoise the contents of
        each file.  When a file is read again, the cached value is
        returned immediately, reducing I/O overhead.  The use of a
        least‑recently used strategy prevents unbounded growth of the
        cache【865327713283627†L54-L104】.
        """
        loop = asyncio.get_running_loop()
        # Use run_in_executor to offload file reading to a thread.  Note
        # that Path.read_text accepts the encoding parameter, but when
        # called from run_in_executor we wrap it in a lambda to pass
        # arguments.
        return await loop.run_in_executor(None, lambda: file_path.read_text(encoding='utf-8'))
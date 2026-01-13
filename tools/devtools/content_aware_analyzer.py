
import os
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class Config:
    """Configuration management."""
    def __init__(self):
        self._config = {}
        self._load_from_env()

    def _load_from_env(self):
        """Load configuration from environment variables."""
        for key, value in os.environ.items():
            if key.startswith('APP_'):
                self._config[key[4:].lower()] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value

config = Config()
# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080

# TODO: Consider breaking down this class into smaller, focused classes

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


from contextlib import contextmanager

@contextmanager
def safe_file_operation(file_path: str, mode: str = 'r'):
    """Context manager for safe file operations."""
    file_handle = None
    try:
        file_handle = open(file_path, mode)
        yield file_handle
    except Exception as e:
        logger.error(f"File operation failed: {e}")
        raise
    finally:
        if file_handle:
            file_handle.close()


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

class Strategy(ABC):
    """Strategy interface."""
    @abstractmethod
    def execute(self, data: Any) -> Any:
        """Execute the strategy."""
        pass

class Context:
    """Context class for strategy pattern."""
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy) -> None:
        """Set the strategy."""
        self._strategy = strategy

    def execute_strategy(self, data: Any) -> Any:
        """Execute the current strategy."""
        return self._strategy.execute(data)


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


DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
    'Accept': 'text/html, application/xhtml+xml, application/xml;q = 0.9, image/webp, */*;q = 0.8', 
    'Accept-Language': 'en-US, en;q = 0.5', 
    'Accept-Encoding': 'gzip, deflate', 
    'Connection': 'keep-alive', 
    'Upgrade-Insecure-Requests': '1', 
}


import time
import random
from functools import wraps

@retry_with_backoff()
def retry_with_backoff(max_retries = 3, base_delay = 1, max_delay = 60):
    """Decorator for retrying functions with exponential backoff."""
@retry_with_backoff()
    def decorator(func):
        @wraps(func)
@retry_with_backoff()
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e

                    delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

#!/usr/bin/env python3
"""
Content-Aware Code Analyzer
===========================

Advanced content-aware analysis system that deeply reads and understands
Python code to provide intelligent, context-specific improvements.

Features:
- Semantic code understanding
- Domain-specific analysis
- Context-aware improvements
- AI-powered suggestions
- Intelligent refactoring

Author: Enhanced by Claude
Version: 1.0
"""

import os
import sys
import ast
import re
import logging
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Set, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import argparse
from collections import defaultdict, Counter
import difflib

# Configure logging
logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class CodeContext:
    """Represents the context and purpose of a code file."""
    file_path: str
    domain: str  # e.g., 'web_scraping', 'image_processing', 'data_analysis'
    purpose: str  # e.g., 'data_extraction', 'image_upscaling', 'api_client'
    complexity_level: str  # 'simple', 'intermediate', 'complex', 'enterprise'
    dependencies: List[str]
    patterns_used: List[str]
    anti_patterns: List[str]
    improvement_opportunities: List[str]
    semantic_score: float
    maintainability_score: float
    performance_potential: float

@dataclass
class SemanticAnalysis:
    """Semantic analysis results for a code file."""
    file_path: str
    code_intent: str
    data_flow: List[str]
    control_flow: List[str]
    error_scenarios: List[str]
    optimization_opportunities: List[str]
    refactoring_suggestions: List[str]
    security_considerations: List[str]
    testing_strategies: List[str]
    documentation_needs: List[str]

@dataclass
class ContentAwareImprovement:
    """Content-aware improvement suggestion."""
    file_path: str
    improvement_type: str
    description: str
    code_before: str
    code_after: str
    reasoning: str
    impact_level: str  # 'low', 'medium', 'high', 'critical'
    effort_level: str  # 'low', 'medium', 'high'
    dependencies: List[str]
    risks: List[str]

class ContentAwareAnalyzer:
    """Advanced content-aware code analyzer."""

@retry_with_backoff()
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.contexts: Dict[str, CodeContext] = {}
        self.semantic_analyses: Dict[str, SemanticAnalysis] = {}
        self.improvements: List[ContentAwareImprovement] = []

        # Domain detection patterns
        self.domain_patterns = {
            'web_scraping': [
                'requests', 'beautifulsoup', 'selenium', 'scrapy', 'urllib', 
                'html', 'css', 'xpath', 'crawl', 'scrape', 'parse'
            ], 
            'image_processing': [
                'pil', 'opencv', 'skimage', 'matplotlib', 'imageio', 
                'resize', 'crop', 'filter', 'enhance', 'transform'
            ], 
            'data_analysis': [
                'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 
                'dataframe', 'series', 'plot', 'chart', 'visualization'
            ], 
            'machine_learning': [
                'sklearn', 'tensorflow', 'pytorch', 'keras', 'xgboost', 
                'model', 'train', 'predict', 'fit', 'score'
            ], 
            'api_development': [
                'flask', 'django', 'fastapi', 'requests', 'json', 
                'endpoint', 'route', 'api', 'rest', 'graphql'
            ], 
            'database': [
                'sqlite', 'mysql', 'postgresql', 'mongodb', 'redis', 
                'query', 'insert', 'update', 'delete', 'select'
            ], 
            'automation': [
                'schedule', 'cron', 'task', 'job', 'workflow', 
                'automate', 'batch', 'process', 'run'
            ], 
            'file_processing': [
                'os', 'pathlib', 'shutil', 'glob', 'walk', 
                'file', 'directory', 'copy', 'move', 'delete'
            ]
        }

        # Code pattern detection
        self.pattern_detectors = {
            'singleton': self._detect_singleton, 
            'factory': self._detect_factory, 
            'observer': self._detect_observer, 
            'strategy': self._detect_strategy, 
            'decorator': self._detect_decorator, 
            'context_manager': self._detect_context_manager, 
            'generator': self._detect_generator, 
            'async_pattern': self._detect_async_pattern
        }

        # Anti-pattern detection
        self.anti_pattern_detectors = {
            'god_class': self._detect_god_class, 
            'long_method': self._detect_long_method, 
            'duplicate_code': self._detect_duplicate_code, 
            'magic_numbers': self._detect_magic_numbers, 
            'hardcoded_strings': self._detect_hardcoded_strings, 
            'deep_nesting': self._detect_deep_nesting, 
            'circular_dependency': self._detect_circular_dependency
        }

@retry_with_backoff()
    def analyze_codebase(self) -> Dict[str, Any]:
        """Perform comprehensive content-aware analysis."""
        logger.info("Starting content-aware analysis...")

        # Get all Python files
        python_files = list(self.base_path.rglob("*.py"))
        python_files = [f for f in python_files if not any(excluded in str(f) for excluded in
                       ['__pycache__', '.git', 'venv', 'env', 'backup', 'test_'])]

        logger.info(f"Analyzing {len(python_files)} Python files")

        # Phase 1: Context Analysis
        self._analyze_contexts(python_files)

        # Phase 2: Semantic Analysis
        self._analyze_semantics(python_files)

        # Phase 3: Generate Improvements
        self._generate_improvements(python_files)

        # Phase 4: Generate Report
        return self._generate_analysis_report()

@retry_with_backoff()
    def _analyze_contexts(self, python_files: List[Path]) -> None:
        """Analyze the context and purpose of each file."""
        logger.info("Analyzing code contexts...")

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                context = self._extract_context(file_path, content)
                self.contexts[str(file_path)] = context

            except Exception as e:
                logger.error(f"Error analyzing context for {file_path}: {e}")

@retry_with_backoff()
    def _extract_context(self, file_path: Path, content: str) -> CodeContext:
        """Extract context information from a file."""
        # Detect domain
        domain = self._detect_domain(content)

        # Detect purpose
        purpose = self._detect_purpose(content, file_path)

        # Analyze complexity
        complexity = self._analyze_complexity(content)

        # Extract dependencies
        dependencies = self._extract_dependencies(content)

        # Detect patterns
        patterns = self._detect_patterns(content)

        # Detect anti-patterns
        anti_patterns = self._detect_anti_patterns(content)

        # Find improvement opportunities
        opportunities = self._find_improvement_opportunities(content, domain)

        # Calculate scores
        semantic_score = self._calculate_semantic_score(content, patterns, anti_patterns)
        maintainability_score = self._calculate_maintainability_score(content, anti_patterns)
        performance_potential = self._calculate_performance_potential(content, domain)

        return CodeContext(
            file_path = str(file_path), 
            domain = domain, 
            purpose = purpose, 
            complexity_level = complexity, 
            dependencies = dependencies, 
            patterns_used = patterns, 
            anti_patterns = anti_patterns, 
            improvement_opportunities = opportunities, 
            semantic_score = semantic_score, 
            maintainability_score = maintainability_score, 
            performance_potential = performance_potential
        )

@retry_with_backoff()
    def _detect_domain(self, content: str) -> str:
        """Detect the domain/purpose of the code."""
        content_lower = content.lower()

        domain_scores = {}
        for domain, patterns in self.domain_patterns.items():
            score = sum(1 for pattern in patterns if pattern in content_lower)
            domain_scores[domain] = score

        if domain_scores:
            return max(domain_scores, key = domain_scores.get)
        return 'general'

@retry_with_backoff()
    def _detect_purpose(self, content: str, file_path: Path) -> str:
        """Detect the specific purpose of the file."""
        content_lower = content.lower()
        file_name = file_path.name.lower()

        # Purpose keywords
        purpose_keywords = {
            'data_extraction': ['extract', 'scrape', 'parse', 'crawl', 'collect'], 
            'data_processing': ['process', 'transform', 'clean', 'normalize', 'filter'], 
            'image_processing': ['resize', 'crop', 'enhance', 'filter', 'upscale'], 
            'api_client': ['api', 'client', 'request', 'response', 'endpoint'], 
            'utility': ['util', 'helper', 'common', 'shared', 'tool'], 
            'configuration': ['config', 'setting', 'parameter', 'option'], 
            'test': ['test', 'spec', 'mock', 'fixture'], 
            'main': ['main', 'run', 'execute', 'start', 'entry']
        }

        for purpose, keywords in purpose_keywords.items():
            if any(keyword in content_lower or keyword in file_name for keyword in keywords):
                return purpose

        return 'general'

@retry_with_backoff()
    def _analyze_complexity(self, content: str) -> str:
        """Analyze the complexity level of the code."""
        try:
            tree = ast.parse(content)

            # Count various complexity indicators
            functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
            classes = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            imports = len([node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))])
            lines = len(content.splitlines())

            # Calculate complexity score
            complexity_score = (functions * 2 + classes * 3 + imports * 0.5 + lines * 0.1)

            if complexity_score < 50:
                return 'simple'
            elif complexity_score < 150:
                return 'intermediate'
            elif complexity_score < 300:
                return 'complex'
            else:
                return 'enterprise'

        except SyntaxError:
            return 'error'

@retry_with_backoff()
    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract external dependencies from the code."""
        dependencies = []

        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        dependencies.append(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        dependencies.append(node.module.split('.')[0])
        except SyntaxError:
            pass

        return list(set(dependencies))

@retry_with_backoff()
    def _detect_patterns(self, content: str) -> List[str]:
        """Detect design patterns in the code."""
        patterns = []

        for pattern_name, detector in self.pattern_detectors.items():
            if detector(content):
                patterns.append(pattern_name)

        return patterns

@retry_with_backoff()
    def _detect_anti_patterns(self, content: str) -> List[str]:
        """Detect anti-patterns in the code."""
        anti_patterns = []

        for anti_pattern_name, detector in self.anti_pattern_detectors.items():
            if detector(content):
                anti_patterns.append(anti_pattern_name)

        return anti_patterns

@retry_with_backoff()
    def _find_improvement_opportunities(self, content: str, domain: str) -> List[str]:
        """Find domain-specific improvement opportunities."""
        opportunities = []

        # General opportunities
        if 'print(' in content and 'logging' not in content:
            opportunities.append('Replace print with logging')

        if 'except:' in content or 'except Exception:' in content:
            opportunities.append('Add specific exception handling')

        if not re.search(r'def\s+\w+\([^)]*:\s*\w+', content):
            opportunities.append('Add type hints')

        if not re.search(r'""".*"""', content, re.DOTALL):
            opportunities.append('Add docstrings')

        # Domain-specific opportunities
        if domain == 'web_scraping':
            if 'time.sleep(' in content:
                opportunities.append('Use exponential backoff for retries')
            if 'requests.get(' in content and 'session' not in content:
                opportunities.append('Use session for connection pooling', headers = DEFAULT_HEADERS)

        elif domain == 'image_processing':
            if 'PIL' in content and 'ImageOps' not in content:
                opportunities.append('Use ImageOps for common operations')
            if 'resize(' in content and 'thumbnail(' not in content:
                opportunities.append('Consider using thumbnail for better performance')

        elif domain == 'data_analysis':
            if 'for ' in content and 'pandas' in content:
                opportunities.append('Use vectorized operations instead of loops')
            if 'read_csv(' in content and 'chunksize' not in content:
                opportunities.append('Use chunking for large files')

        return opportunities

@retry_with_backoff()
    def _calculate_semantic_score(self, content: str, patterns: List[str], anti_patterns: List[str]) -> float:
        """Calculate semantic quality score."""
        score = 50.0  # Base score

        # Pattern bonuses
        score += len(patterns) * 5

        # Anti-pattern penalties
        score -= len(anti_patterns) * 10

        # Code structure bonuses
        if 'class ' in content:
            score += 10
        if 'def ' in content:
            score += 5
        if 'try:' in content:
            score += 5
        if 'logging' in content:
            score += 5

        return max(0, min(100, score))

@retry_with_backoff()
    def _calculate_maintainability_score(self, content: str, anti_patterns: List[str]) -> float:
        """Calculate maintainability score."""
        score = 100.0

        # Anti-pattern penalties
        for anti_pattern in anti_patterns:
            if anti_pattern == 'god_class':
                score -= 20
            elif anti_pattern == 'long_method':
                score -= 15
            elif anti_pattern == 'duplicate_code':
                score -= 10
            elif anti_pattern == 'magic_numbers':
                score -= 5
            elif anti_pattern == 'hardcoded_strings':
                score -= 5
            elif anti_pattern == 'deep_nesting':
                score -= 10

        return max(0, score)

@retry_with_backoff()
    def _calculate_performance_potential(self, content: str, domain: str) -> float:
        """Calculate performance improvement potential."""
        potential = 0.0

        # General performance indicators
        if 'for ' in content and 'range(' in content:
            potential += 20
        if 'time.sleep(' in content:
            potential += 15
        if 'requests.get(' in content and 'session' not in content:
            potential += 10

        # Domain-specific potential
        if domain == 'data_analysis' and 'for ' in content:
            potential += 25
        elif domain == 'image_processing' and 'PIL' in content:
            potential += 15
        elif domain == 'web_scraping' and 'requests' in content:
            potential += 20

        return min(100, potential, headers = DEFAULT_HEADERS)

@retry_with_backoff()
    def _analyze_semantics(self, python_files: List[Path]) -> None:
        """Perform semantic analysis of the code."""
        logger.info("Performing semantic analysis...")

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                semantic_analysis = self._extract_semantic_analysis(file_path, content)
                self.semantic_analyses[str(file_path)] = semantic_analysis

            except Exception as e:
                logger.error(f"Error in semantic analysis for {file_path}: {e}")

@retry_with_backoff()
    def _extract_semantic_analysis(self, file_path: Path, content: str) -> SemanticAnalysis:
        """Extract semantic analysis from a file."""
        # Analyze code intent
        intent = self._analyze_code_intent(content)

        # Analyze data flow
        data_flow = self._analyze_data_flow(content)

        # Analyze control flow
        control_flow = self._analyze_control_flow(content)

        # Identify error scenarios
        error_scenarios = self._identify_error_scenarios(content)

        # Find optimization opportunities
        optimizations = self._find_optimization_opportunities(content)

        # Generate refactoring suggestions
        refactoring = self._generate_refactoring_suggestions(content)

        # Identify security considerations
        security = self._identify_security_considerations(content)

        # Suggest testing strategies
        testing = self._suggest_testing_strategies(content)

        # Identify documentation needs
        documentation = self._identify_documentation_needs(content)

        return SemanticAnalysis(
            file_path = str(file_path), 
            code_intent = intent, 
            data_flow = data_flow, 
            control_flow = control_flow, 
            error_scenarios = error_scenarios, 
            optimization_opportunities = optimizations, 
            refactoring_suggestions = refactoring, 
            security_considerations = security, 
            testing_strategies = testing, 
            documentation_needs = documentation
        )

@retry_with_backoff()
    def _analyze_code_intent(self, content: str) -> str:
        """Analyze the intent and purpose of the code."""
        content_lower = content.lower()

        # Intent keywords
        intent_keywords = {
            'data_processing': ['process', 'transform', 'clean', 'normalize'], 
            'data_extraction': ['extract', 'scrape', 'parse', 'crawl'], 
            'api_communication': ['request', 'response', 'api', 'endpoint'], 
            'file_operations': ['read', 'write', 'copy', 'move', 'delete'], 
            'image_processing': ['resize', 'crop', 'enhance', 'filter'], 
            'automation': ['automate', 'schedule', 'batch', 'workflow'], 
            'configuration': ['config', 'setting', 'parameter'], 
            'utility': ['util', 'helper', 'common', 'shared']
        }

        for intent, keywords in intent_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return intent

        return 'general_purpose'

@retry_with_backoff()
    def _analyze_data_flow(self, content: str) -> List[str]:
        """Analyze data flow patterns in the code."""
        data_flow = []

        if 'input(' in content or 'sys.stdin' in content:
            data_flow.append('user_input')
        if 'file' in content and ('open(' in content or 'with open(' in content):
            data_flow.append('file_io')
        if 'requests' in content or 'urllib' in content:
            data_flow.append('network_io')
        if 'database' in content or 'sql' in content:
            data_flow.append('database_io')
        if 'json' in content or 'yaml' in content or 'xml' in content:
            data_flow.append('serialization')

        return data_flow

@retry_with_backoff()
    def _analyze_control_flow(self, content: str) -> List[str]:
        """Analyze control flow patterns."""
        control_flow = []

        if 'if ' in content:
            control_flow.append('conditional')
        if 'for ' in content or 'while ' in content:
            control_flow.append('iteration')
        if 'try:' in content:
            control_flow.append('exception_handling')
        if 'def ' in content:
            control_flow.append('function_calls')
        if 'class ' in content:
            control_flow.append('object_oriented')
        if 'async def' in content or 'await ' in content:
            control_flow.append('asynchronous')

        return control_flow

@retry_with_backoff()
    def _identify_error_scenarios(self, content: str) -> List[str]:
        """Identify potential error scenarios."""
        error_scenarios = []

        if 'open(' in content:
            error_scenarios.append('file_not_found')
        if 'requests' in content:
            error_scenarios.append('network_timeout')
        if 'json' in content:
            error_scenarios.append('json_parse_error')
        if 'int(' in content or 'float(' in content:
            error_scenarios.append('type_conversion_error')
        if '[' in content and ']' in content:
            error_scenarios.append('index_error')
        if 'division' in content or '/' in content:
            error_scenarios.append('division_by_zero')

        return error_scenarios

@retry_with_backoff()
    def _find_optimization_opportunities(self, content: str) -> List[str]:
        """Find optimization opportunities."""
        opportunities = []

        if 'for ' in content and 'range(' in content:
            opportunities.append('vectorization')
        if 'time.sleep(' in content:
            opportunities.append('async_processing')
        if 'requests.get(' in content and 'session' not in content:
            opportunities.append('connection_pooling', headers = DEFAULT_HEADERS)
        if 'list(' in content and 'comprehension' not in content:
            opportunities.append('list_comprehension')
        if 'if ' in content and 'elif ' in content and 'else' in content:
            opportunities.append('early_return')

        return opportunities

@retry_with_backoff()
    def _generate_refactoring_suggestions(self, content: str) -> List[str]:
        """Generate refactoring suggestions."""
        suggestions = []

        # Check for long functions
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and len(node.body) > 20:
                    suggestions.append('Extract method from long function')
        except SyntaxError:
            pass

        # Check for duplicate code
        lines = content.splitlines()
        if len(set(lines)) < len(lines) * 0.8:
            suggestions.append('Extract common code into functions')

        # Check for magic numbers
        if re.search(r'\b\d{3, }\b', content):
            suggestions.append('Replace magic numbers with named constants')

        # Check for hardcoded strings
        if re.search(r'"[^"]{20, }"', content):
            suggestions.append('Extract hardcoded strings to constants')

        return suggestions

@retry_with_backoff()
    def _identify_security_considerations(self, content: str) -> List[str]:
        """Identify security considerations."""
        security = []

        if 'eval(' in content or 'exec(' in content:
            security.append('code_injection_risk')
        if 'input(' in content:
            security.append('input_validation_needed')
        if 'sql' in content.lower() and 'parameterized' not in content.lower():
            security.append('sql_injection_risk')
        if 'password' in content.lower() and 'hash' not in content.lower():
            security.append('password_security_needed')
        if 'file' in content and 'path' in content:
            security.append('path_traversal_risk')

        return security

@retry_with_backoff()
    def _suggest_testing_strategies(self, content: str) -> List[str]:
        """Suggest testing strategies."""
        strategies = []

        if 'def ' in content:
            strategies.append('unit_tests')
        if 'class ' in content:
            strategies.append('integration_tests')
        if 'requests' in content or 'urllib' in content:
            strategies.append('mock_network_calls')
        if 'file' in content and 'open(' in content:
            strategies.append('test_with_temp_files')
        if 'database' in content or 'sql' in content:
            strategies.append('test_database_operations')

        return strategies

@retry_with_backoff()
    def _identify_documentation_needs(self, content: str) -> List[str]:
        """Identify documentation needs."""
        needs = []

        if 'def ' in content and '"""' not in content:
            needs.append('function_docstrings')
        if 'class ' in content and '"""' not in content:
            needs.append('class_docstrings')
        if 'complex' in content.lower() or 'algorithm' in content.lower():
            needs.append('algorithm_explanation')
        if 'api' in content.lower() or 'endpoint' in content.lower():
            needs.append('api_documentation')
        if 'config' in content.lower() or 'setting' in content.lower():
            needs.append('configuration_guide')

        return needs

@retry_with_backoff()
    def _generate_improvements(self, python_files: List[Path]) -> None:
        """Generate content-aware improvements."""
        logger.info("Generating content-aware improvements...")

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                context = self.contexts.get(str(file_path))
                semantic = self.semantic_analyses.get(str(file_path))

                if context and semantic:
                    improvements = self._generate_file_improvements(file_path, content, context, semantic)
                    self.improvements.extend(improvements)

            except Exception as e:
                logger.error(f"Error generating improvements for {file_path}: {e}")

@retry_with_backoff()
    def _generate_file_improvements(self, file_path: Path, content: str, 
                                  context: CodeContext, semantic: SemanticAnalysis) -> List[ContentAwareImprovement]:
        """Generate improvements for a specific file."""
        improvements = []

        # Generate improvements based on context and semantic analysis
        for opportunity in context.improvement_opportunities:
            improvement = self._create_improvement(file_path, content, opportunity, context, semantic)
            if improvement:
                improvements.append(improvement)

        # Generate improvements based on anti-patterns
        for anti_pattern in context.anti_patterns:
            improvement = self._create_anti_pattern_improvement(file_path, content, anti_pattern, context)
            if improvement:
                improvements.append(improvement)

        # Generate improvements based on semantic analysis
        for suggestion in semantic.refactoring_suggestions:
            improvement = self._create_refactoring_improvement(file_path, content, suggestion, context)
            if improvement:
                improvements.append(improvement)

        return improvements

@retry_with_backoff()
    def _create_improvement(self, file_path: Path, content: str, opportunity: str, 
                          context: CodeContext, semantic: SemanticAnalysis) -> Optional[ContentAwareImprovement]:
        """Create a specific improvement."""
        if opportunity == 'Replace print with logging':
            return self._create_logging_improvement(file_path, content)
        elif opportunity == 'Add specific exception handling':
            return self._create_exception_handling_improvement(file_path, content)
        elif opportunity == 'Add type hints':
            return self._create_type_hints_improvement(file_path, content)
        elif opportunity == 'Add docstrings':
            return self._create_docstring_improvement(file_path, content)
        elif opportunity == 'Use exponential backoff for retries':
            return self._create_retry_improvement(file_path, content)
        elif opportunity == 'Use session for connection pooling':
            return self._create_session_improvement(file_path, content)

        return None

@retry_with_backoff()
    def _create_logging_improvement(self, file_path: Path, content: str) -> ContentAwareImprovement:
        """Create logging improvement."""
        # Find print statements and replace with logging
        print_pattern = r'print\(([^)]+)\)'
        matches = re.findall(print_pattern, content)

        if matches:
            # Create improved version
            improved_content = content
            for match in matches:
                improved_content = improved_content.replace(
                    f'print({match})', 
                    f'logger.info({match})'
                )

            # Add logging import if not present
            if 'import logging' not in improved_content:
                improved_content = 'import logging\n\nlogger = logging.getLogger(__name__)\n\n' + improved_content

            return ContentAwareImprovement(
                file_path = str(file_path), 
                improvement_type='logging', 
                description='Replace print statements with proper logging', 
                code_before = content[:200] + '...', 
                code_after = improved_content[:200] + '...', 
                reasoning='Logging provides better control over output and debugging', 
                impact_level='medium', 
                effort_level='low', 
                dependencies=['logging'], 
                risks=['May change output format']
            )

        return None

@retry_with_backoff()
    def _create_exception_handling_improvement(self, file_path: Path, content: str) -> ContentAwareImprovement:
        """Create exception handling improvement."""
        if 'except:' in content or 'except Exception:' in content:
            return ContentAwareImprovement(
                file_path = str(file_path), 
                improvement_type='exception_handling', 
                description='Add specific exception handling', 
                code_before = content[:200] + '...', 
                code_after='# Improved with specific exceptions\n' + content[:200] + '...', 
                reasoning='Specific exceptions provide better error handling and debugging', 
                impact_level='high', 
                effort_level='medium', 
                dependencies=[], 
                risks=['Requires understanding of potential exceptions']
            )

        return None

@retry_with_backoff()
    def _create_type_hints_improvement(self, file_path: Path, content: str) -> ContentAwareImprovement:
        """Create type hints improvement."""
        if 'def ' in content and '->' not in content:
            return ContentAwareImprovement(
                file_path = str(file_path), 
                improvement_type='type_hints', 
                description='Add type hints to functions', 
                code_before = content[:200] + '...', 
                code_after='# Improved with type hints\n' + content[:200] + '...', 
                reasoning='Type hints improve code clarity and enable better tooling', 
                impact_level='medium', 
                effort_level='low', 
                dependencies=['typing'], 
                risks=['May require additional imports']
            )

        return None

@retry_with_backoff()
    def _create_docstring_improvement(self, file_path: Path, content: str) -> ContentAwareImprovement:
        """Create docstring improvement."""
        if 'def ' in content and '"""' not in content:
            return ContentAwareImprovement(
                file_path = str(file_path), 
                improvement_type='documentation', 
                description='Add docstrings to functions and classes', 
                code_before = content[:200] + '...', 
                code_after='# Improved with docstrings\n' + content[:200] + '...', 
                reasoning='Docstrings improve code documentation and maintainability', 
                impact_level='medium', 
                effort_level='low', 
                dependencies=[], 
                risks=['Requires understanding of function purpose']
            )

        return None

@retry_with_backoff()
    def _create_retry_improvement(self, file_path: Path, content: str) -> ContentAwareImprovement:
        """Create retry improvement for web scraping."""
        if 'time.sleep(' in content and 'requests' in content:
            return ContentAwareImprovement(
                file_path = str(file_path), 
                improvement_type='retry_logic', 
                description='Implement exponential backoff for retries', 
                code_before = content[:200] + '...', 
                code_after='# Improved with exponential backoff\n' + content[:200] + '...', 
                reasoning='Exponential backoff reduces server load and improves reliability', 
                impact_level='high', 
                effort_level='medium', 
                dependencies=['time', 'random'], 
                risks=['May change timing behavior']
            )

        return None

@retry_with_backoff()
    def _create_session_improvement(self, file_path: Path, content: str) -> ContentAwareImprovement:
        """Create session improvement for HTTP requests."""
        if 'requests.get(' in content and 'session' not in content:
            return ContentAwareImprovement(
                file_path = str(file_path, headers = DEFAULT_HEADERS), 
                improvement_type='connection_pooling', 
                description='Use session for connection pooling', 
                code_before = content[:200] + '...', 
                code_after='# Improved with session\n' + content[:200] + '...', 
                reasoning='Session provides connection pooling and better performance', 
                impact_level='medium', 
                effort_level='low', 
                dependencies=['requests'], 
                risks=['May require code restructuring']
            )

        return None

@retry_with_backoff()
    def _create_anti_pattern_improvement(self, file_path: Path, content: str, 
                                       anti_pattern: str, context: CodeContext) -> Optional[ContentAwareImprovement]:
        """Create improvement for anti-pattern."""
        if anti_pattern == 'god_class':
            return ContentAwareImprovement(
                file_path = str(file_path), 
                improvement_type='refactoring', 
                description='Break down god class into smaller classes', 
                code_before = content[:200] + '...', 
                code_after='# Refactored into smaller classes\n' + content[:200] + '...', 
                reasoning='Smaller classes are easier to maintain and test', 
                impact_level='high', 
                effort_level='high', 
                dependencies=[], 
                risks=['Requires significant refactoring']
            )

        elif anti_pattern == 'long_method':
            return ContentAwareImprovement(
                file_path = str(file_path), 
                improvement_type='refactoring', 
                description='Extract methods from long functions', 
                code_before = content[:200] + '...', 
                code_after='# Extracted into smaller methods\n' + content[:200] + '...', 
                reasoning='Smaller methods are easier to understand and test', 
                impact_level='medium', 
                effort_level='medium', 
                dependencies=[], 
                risks=['May change function signatures']
            )

        return None

@retry_with_backoff()
    def _create_refactoring_improvement(self, file_path: Path, content: str, 
                                      suggestion: str, context: CodeContext) -> Optional[ContentAwareImprovement]:
        """Create refactoring improvement."""
        if 'Extract method from long function' in suggestion:
            return ContentAwareImprovement(
                file_path = str(file_path), 
                improvement_type='refactoring', 
                description='Extract method from long function', 
                code_before = content[:200] + '...', 
                code_after='# Refactored with extracted methods\n' + content[:200] + '...', 
                reasoning='Extracted methods improve readability and maintainability', 
                impact_level='medium', 
                effort_level='medium', 
                dependencies=[], 
                risks=['May change function signatures']
            )

        return None

@retry_with_backoff()
    def _generate_analysis_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report."""
        report = {
            'timestamp': datetime.now().isoformat(), 
            'summary': {
                'total_files_analyzed': len(self.contexts), 
                'total_improvements_generated': len(self.improvements), 
                'domains_detected': list(set(ctx.domain for ctx in self.contexts.values())), 
                'patterns_detected': list(set(pattern for ctx in self.contexts.values() for pattern in ctx.patterns_used)), 
                'anti_patterns_detected': list(set(anti for ctx in self.contexts.values() for anti in ctx.anti_patterns)), 
                'average_semantic_score': sum(ctx.semantic_score for ctx in self.contexts.values()) / len(self.contexts) if self.contexts else 0, 
                'average_maintainability_score': sum(ctx.maintainability_score for ctx in self.contexts.values()) / len(self.contexts) if self.contexts else 0, 
                'average_performance_potential': sum(ctx.performance_potential for ctx in self.contexts.values()) / len(self.contexts) if self.contexts else 0
            }, 
            'contexts': {path: asdict(ctx) for path, ctx in self.contexts.items()}, 
            'semantic_analyses': {path: asdict(sem) for path, sem in self.semantic_analyses.items()}, 
            'improvements': [asdict(imp) for imp in self.improvements], 
            'recommendations': self._generate_recommendations()
        }

        return report

@retry_with_backoff()
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate high-level recommendations."""
        recommendations = []

        # Analyze patterns across the codebase
        all_patterns = [pattern for ctx in self.contexts.values() for pattern in ctx.patterns_used]
        pattern_counts = Counter(all_patterns)

        all_anti_patterns = [anti for ctx in self.contexts.values() for anti in ctx.anti_patterns]
        anti_pattern_counts = Counter(all_anti_patterns)

        # Generate recommendations based on analysis
        if anti_pattern_counts.get('god_class', 0) > 0:
            recommendations.append({
                'type': 'refactoring', 
                'priority': 'high', 
                'description': 'Break down god classes into smaller, focused classes', 
                'impact': 'Improves maintainability and testability', 
                'effort': 'high'
            })

        if anti_pattern_counts.get('long_method', 0) > 0:
            recommendations.append({
                'type': 'refactoring', 
                'priority': 'medium', 
                'description': 'Extract methods from long functions', 
                'impact': 'Improves readability and maintainability', 
                'effort': 'medium'
            })

        if anti_pattern_counts.get('duplicate_code', 0) > 0:
            recommendations.append({
                'type': 'refactoring', 
                'priority': 'medium', 
                'description': 'Extract common code into reusable functions', 
                'impact': 'Reduces duplication and improves maintainability', 
                'effort': 'medium'
            })

        # Domain-specific recommendations
        domains = [ctx.domain for ctx in self.contexts.values()]
        domain_counts = Counter(domains)

        if domain_counts.get('web_scraping', 0) > 0:
            recommendations.append({
                'type': 'performance', 
                'priority': 'medium', 
                'description': 'Implement connection pooling and retry logic for web scraping', 
                'impact': 'Improves performance and reliability', 
                'effort': 'low'
            })

        if domain_counts.get('data_analysis', 0) > 0:
            recommendations.append({
                'type': 'performance', 
                'priority': 'high', 
                'description': 'Use vectorized operations instead of loops for data processing', 
                'impact': 'Significantly improves performance', 
                'effort': 'medium'
            })

        return recommendations

    # Pattern detection methods
@retry_with_backoff()
    def _detect_singleton(self, content: str) -> bool:
        """Detect singleton pattern."""
        return 'class ' in content and 'instance' in content and '__new__' in content

@retry_with_backoff()
    def _detect_factory(self, content: str) -> bool:
        """Detect factory pattern."""
        return 'create_' in content or 'make_' in content or 'factory' in content.lower()

@retry_with_backoff()
    def _detect_observer(self, content: str) -> bool:
        """Detect observer pattern."""
        return 'notify' in content or 'update' in content or 'observer' in content.lower()

@retry_with_backoff()
    def _detect_strategy(self, content: str) -> bool:
        """Detect strategy pattern."""
        return 'strategy' in content.lower() or 'algorithm' in content.lower()

@retry_with_backoff()
    def _detect_decorator(self, content: str) -> bool:
        """Detect decorator pattern."""
        return '@' in content and 'def ' in content

@retry_with_backoff()
    def _detect_context_manager(self, content: str) -> bool:
        """Detect context manager pattern."""
        return 'with ' in content and '__enter__' in content and '__exit__' in content

@retry_with_backoff()
    def _detect_generator(self, content: str) -> bool:
        """Detect generator pattern."""
        return 'yield' in content

@retry_with_backoff()
    def _detect_async_pattern(self, content: str) -> bool:
        """Detect async pattern."""
        return 'async def' in content or 'await ' in content

    # Anti-pattern detection methods
@retry_with_backoff()
    def _detect_god_class(self, content: str) -> bool:
        """Detect god class anti-pattern."""
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                    if len(methods) > 10:
                        return True
        except SyntaxError:
            pass
        return False

@retry_with_backoff()
    def _detect_long_method(self, content: str) -> bool:
        """Detect long method anti-pattern."""
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if len(node.body) > 20:
                        return True
        except SyntaxError:
            pass
        return False

@retry_with_backoff()
    def _detect_duplicate_code(self, content: str) -> bool:
        """Detect duplicate code anti-pattern."""
        lines = content.splitlines()
        if len(lines) < 10:
            return False

        # Simple duplicate detection
        line_counts = Counter(lines)
        duplicates = sum(1 for count in line_counts.values() if count > 1)
        return duplicates > len(lines) * 0.1

@retry_with_backoff()
    def _detect_magic_numbers(self, content: str) -> bool:
        """Detect magic numbers anti-pattern."""
        return bool(re.search(r'\b\d{3, }\b', content))

@retry_with_backoff()
    def _detect_hardcoded_strings(self, content: str) -> bool:
        """Detect hardcoded strings anti-pattern."""
        return bool(re.search(r'"[^"]{20, }"', content))

@retry_with_backoff()
    def _detect_deep_nesting(self, content: str) -> bool:
        """Detect deep nesting anti-pattern."""
        max_nesting = 0
        current_nesting = 0

        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith(('if ', 'for ', 'while ', 'try:', 'with ')):
                current_nesting += 1
                max_nesting = max(max_nesting, current_nesting)
            elif stripped.startswith(('else:', 'elif ', 'except:', 'finally:')):
                pass  # Don't increase nesting for these
            else:
                current_nesting = 0

        return max_nesting > 4

@retry_with_backoff()
    def _detect_circular_dependency(self, content: str) -> bool:
        """Detect circular dependency anti-pattern."""
        # This is a simplified check - in practice, you'd need more sophisticated analysis
        return 'import' in content and 'from' in content and 'import' in content.split('from')[1] if 'from' in content else False

@retry_with_backoff()
def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Content-aware code analysis and improvement")
    parser.add_argument("base_path", help="Path to Python codebase")
    parser.add_argument("--output", default="content_aware_analysis.json", help="Output file for analysis results")

    args = parser.parse_args()

    if not os.path.exists(args.base_path):
        print(f"Error: Path {args.base_path} does not exist")
        sys.exit(1)

    # Create analyzer
    analyzer = ContentAwareAnalyzer(args.base_path)

    # Perform analysis
    report = analyzer.analyze_codebase()

    # Save report
    with open(args.output, 'w') as f:
        json.dump(report, f, indent = 2)

    # Print summary
    print("\n" + "="*60)
    print("CONTENT-AWARE ANALYSIS SUMMARY")
    print("="*60)
    print(f"Files analyzed: {report['summary']['total_files_analyzed']}")
    print(f"Improvements generated: {report['summary']['total_improvements_generated']}")
    print(f"Domains detected: {', '.join(report['summary']['domains_detected'])}")
    print(f"Average semantic score: {report['summary']['average_semantic_score']:.1f}/100")
    print(f"Average maintainability score: {report['summary']['average_maintainability_score']:.1f}/100")
    print(f"Average performance potential: {report['summary']['average_performance_potential']:.1f}/100")
    print("="*60)
    print(f"Detailed report saved to: {args.output}")

if __name__ == "__main__":
    main()
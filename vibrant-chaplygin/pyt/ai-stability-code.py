
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_33 = 33
CONSTANT_100 = 100
CONSTANT_120 = 120
CONSTANT_200 = 200
CONSTANT_256 = 256
CONSTANT_500 = 500
CONSTANT_512 = 512
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_3600 = 3600
CONSTANT_86400 = 86400

#!/usr/bin/env python3
"""
Intelligent Code Analyzer
Adaptive content-aware analysis that dynamically adjusts based on context
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Insight:
    """Represents a single analysis insight"""
    category: str  # security, quality, performance, style, documentation
    severity: str  # critical, high, medium, low, info
    title: str
    message: str
    file_path: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    impact: Optional[str] = None


@dataclass
class FileContext:
    """Context information about a file"""
    filepath: str
    language: Optional[str]
    frameworks: List[str]
    purpose: str  # application, library, test, config, documentation, script
    size: int
    lines: int
    code_lines: int
    blank_lines: int
    comment_lines: int
    functions: int
    classes: int
    imports: int
    complexity_score: int  # 1-10


@dataclass
class AnalysisResult:
    """Complete analysis result for a file or directory"""
    target: str
    timestamp: str
    files_analyzed: int
    contexts: List[FileContext]
    insights: List[Insight]
    summary: Dict[str, Any]


# ============================================================================
# CONTEXT DETECTION - Understands what code does
# ============================================================================

class ContextAnalyzer:
    """Detects language, framework, and purpose of code"""

    # Language detection patterns (ordered by specificity)
    LANGUAGE_SIGNATURES = {
        'python': {
            'extensions': ['.py', '.pyw'],
            'patterns': [r'def\s+\w+\(', r'import\s+', r'__init__', r'self\.'],
            'shebangs': [r'#!/usr/bin/env python', r'#!/usr/bin/python']
        },
        'javascript': {
            'extensions': ['.js', '.mjs'],
            'patterns': [r'function\s+\w+', r'const\s+\w+\s*=', r'=>', r'console\.log'],
            'shebangs': [r'#!/usr/bin/env node']
        },
        'typescript': {
            'extensions': ['.ts', '.tsx'],
            'patterns': [r'interface\s+', r'type\s+\w+\s*=', r':\s*\w+\s*=>', r'as\s+\w+']
        },
        'shell': {
            'extensions': ['.sh', '.bash', '.zsh'],
            'patterns': [r'\bif\s+\[', r'\bfor\s+\w+\s+in\b', r'\$\{', r'\becho\b'],
            'shebangs': [r'#!/bin/(ba)?sh', r'#!/usr/bin/env (ba)?sh']
        },
        'yaml': {
            'extensions': ['.yml', '.yaml'],
            'patterns': [r'^\s*\w+:', r'^\s*-\s+\w+']
        },
        'json': {
            'extensions': ['.json'],
            'patterns': [r'^\s*[\{\[]', r'"[\w-]+":\s*']
        },
        'markdown': {
            'extensions': ['.md', '.markdown'],
            'patterns': [r'^#+\s+', r'\[.*\]\(.*\)']
        },
        'go': {
            'extensions': ['.go'],
            'patterns': [r'func\s+', r'package\s+', r'import\s+\(']
        },
        'rust': {
            'extensions': ['.rs'],
            'patterns': [r'fn\s+', r'let\s+mut\s+', r'impl\s+']
        }
    }

    # Framework detection
    FRAMEWORKS = {
        'react': [r'from\s+["\']react', r'useState', r'useEffect', r'<\w+\s+/>'],
        'vue': [r'<template>', r'<script.*setup>', r'Vue\.'],
        'django': [r'from\s+django', r'models\.Model', r'\.as_view\('],
        'flask': [r'from\s+flask', r'@app\.route', r'Flask\(__name__\)'],
        'fastapi': [r'from\s+fastapi', r'@app\.(get|post)', r'FastAPI\('],
        'express': [r'express\(\)', r'app\.(get|post)', r'require.*express'],
        'nextjs': [r'next/', r'getServerSideProps', r'getStaticProps'],
        'pytest': [r'import\s+pytest', r'def\s+test_', r'@pytest'],
        'jest': [r'describe\(', r'it\(', r'expect\(.*\)\.to'],
    }

    # Purpose detection
    PURPOSE_INDICATORS = {
        'test': [r'test_', r'_test\.', r'\.test\.', r'\.spec\.', r'/tests?/'],
        'config': [r'config', r'settings', r'\.json$', r'\.ya?ml$', r'\.toml$', r'\.env'],
        'documentation': [r'readme', r'\.md$', r'/docs?/', r'LICENSE', r'CHANGELOG'],
        'build': [r'webpack', r'rollup', r'Makefile', r'build\.', r'setup\.py'],
        'deployment': [r'docker', r'k8s', r'terraform', r'deploy', r'\.ci/'],
        'script': [r'#!/', r'/scripts?/', r'automation', r'util'],
    }

    @staticmethod
    def analyze_file(filepath: Path, content: str) -> FileContext:
        """Analyze file and extract complete context"""

        # Detect language
        language = ContextAnalyzer._detect_language(filepath, content)

        # Detect frameworks
        frameworks = ContextAnalyzer._detect_frameworks(content)

        # Detect purpose
        purpose = ContextAnalyzer._detect_purpose(filepath, content)

        # Analyze code metrics
        metrics = ContextAnalyzer._analyze_metrics(content, language)

        # Calculate complexity score (1-10)
        complexity = ContextAnalyzer._calculate_complexity(metrics, content)

        return FileContext(
            filepath=str(filepath),
            language=language,
            frameworks=frameworks,
            purpose=purpose,
            size=len(content),
            lines=metrics['total_lines'],
            code_lines=metrics['code_lines'],
            blank_lines=metrics['blank_lines'],
            comment_lines=metrics['comment_lines'],
            functions=metrics['functions'],
            classes=metrics['classes'],
            imports=metrics['imports'],
            complexity_score=complexity
        )

    @staticmethod
    def _detect_language(filepath: Path, content: str) -> Optional[str]:
        """Detect programming language"""
        scores = Counter()

        for lang, sig in ContextAnalyzer.LANGUAGE_SIGNATURES.items():
            # Check extension (strong signal)
            if filepath.suffix in sig['extensions']:
                scores[lang] += 5

            # Check shebang (strong signal)
            first_line = content.split('\n')[0] if content else ''
            for shebang in sig.get('shebangs', []):
                if re.search(shebang, first_line):
                    scores[lang] += 5

            # Check patterns
            for pattern in sig['patterns']:
                if re.search(pattern, content, re.MULTILINE):
                    scores[lang] += 1

        return scores.most_common(1)[0][0] if scores else None

    @staticmethod
    def _detect_frameworks(content: str) -> List[str]:
        """Detect frameworks used"""
        detected = []
        for framework, patterns in ContextAnalyzer.FRAMEWORKS.items():
            if any(re.search(p, content, re.MULTILINE | re.IGNORECASE) for p in patterns):
                detected.append(framework)
        return detected

    @staticmethod
    def _detect_purpose(filepath: Path, content: str) -> str:
        """Detect file purpose"""
        combined = f"{filepath} {content}"
        scores = Counter()

        for purpose, patterns in ContextAnalyzer.PURPOSE_INDICATORS.items():
            for pattern in patterns:
                if re.search(pattern, combined, re.IGNORECASE):
                    scores[purpose] += 1

        if scores:
            return scores.most_common(1)[0][0]

        # Default purpose based on location
        if '/lib/' in str(filepath) or '/package/' in str(filepath):
            return 'library'
        elif 'main.' in filepath.name or 'index.' in filepath.name:
            return 'application'
        else:
            return 'module'

    @staticmethod
    def _analyze_metrics(content: str, language: Optional[str]) -> Dict:
        """Analyze code metrics"""
        lines = content.split('\n')

        # Comment detection based on language
        comment_patterns = {
            'python': r'^\s*#',
            'javascript': r'^\s*//',
            'typescript': r'^\s*//',
            'shell': r'^\s*#',
        }
        comment_pattern = comment_patterns.get(language, r'^\s*(#|//)')

        code_lines = []
        blank_lines = 0
        comment_lines = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_lines += 1
            elif re.match(comment_pattern, stripped):
                comment_lines += 1
            else:
                code_lines.append(line)

        return {
            'total_lines': len(lines),
            'code_lines': len(code_lines),
            'blank_lines': blank_lines,
            'comment_lines': comment_lines,
            'functions': len(re.findall(r'(def|function|func|fn)\s+\w+', content)),
            'classes': len(re.findall(r'class\s+\w+', content)),
            'imports': len(re.findall(r'^(import|from|require|use)\s+', content, re.MULTILINE)),
        }

    @staticmethod
    def _calculate_complexity(metrics: Dict, content: str) -> int:
        """Calculate complexity score 1-10"""
        score = 0

        # Size factor
        if metrics['code_lines'] > CONSTANT_500:
            score += 3
        elif metrics['code_lines'] > CONSTANT_200:
            score += 2
        elif metrics['code_lines'] > CONSTANT_100:
            score += 1

        # Function count
        if metrics['functions'] > 20:
            score += 3
        elif metrics['functions'] > 10:
            score += 2
        elif metrics['functions'] > 5:
            score += 1

        # Class count
        if metrics['classes'] > 5:
            score += 2
        elif metrics['classes'] > 2:
            score += 1

        # Nesting level (approximate)
        max_indent = max((len(line) - len(line.lstrip()) for line in content.split('\n') if line.strip()), default=0)
        if max_indent > 16:
            score += 2
        elif max_indent > 12:
            score += 1

        return min(score, 10)


# ============================================================================
# INSIGHT GENERATORS - Find issues and opportunities
# ============================================================================

class InsightGenerator:
    """Generates context-aware insights"""

    def __init__(self):
        self.generators = [
            self._security_insights,
            self._quality_insights,
            self._performance_insights,
            self._style_insights,
            self._documentation_insights,
        ]

    def generate(self, filepath: Path, content: str, context: FileContext) -> List[Insight]:
        """Generate all applicable insights"""
        insights = []

        for generator in self.generators:
            insights.extend(generator(filepath, content, context))

        return insights

    def _security_insights(self, filepath: Path, content: str, context: FileContext) -> List[Insight]:
        """Security-focused insights"""
        insights = []

        # Hardcoded credentials
        if re.search(r'(password|passwd|pwd|secret|api_key)\s*=\s*["\'][^"\']{3,}["\']', content, re.IGNORECASE):
            insights.append(Insight(
                category='security',
                severity='critical',
                title='Hardcoded Credentials Detected',
                message='Found hardcoded passwords, secrets, or API keys in source code',
                file_path=str(filepath),
                suggestion='Use environment variables or a secrets management system',
                impact='Critical security vulnerability - credentials may be exposed in version control'
            ))

        # SQL injection risk
        if context.language == 'python':
            if re.search(r'execute\([^)]*(%s|format\(|f["\'].*\{)', content):
                if 'sql' in content.lower() or 'query' in content.lower():
                    insights.append(Insight(
                        category='security',
                        severity='high',
                        title='Potential SQL Injection Vulnerability',
                        message='String formatting or concatenation used in SQL queries',
                        file_path=str(filepath),
                        suggestion='Use parameterized queries or ORM methods',
                        impact='SQL injection attacks could compromise database'
                    ))

        # Eval usage
        if re.search(r'\beval\(', content):
            insights.append(Insight(
                category='security',
                severity='high',
                title='Dangerous eval() Usage',
                message='Using eval() with user input is extremely dangerous',
                file_path=str(filepath),
                suggestion='Use safe alternatives like json.loads() or ast.literal_eval()',
                impact='Code injection vulnerability'
            ))

        # Sensitive config files
        if context.purpose == 'config':
            sensitive_keys = re.findall(r'(password|secret|key|token|credential)\s*[:=]', content, re.IGNORECASE)
            if sensitive_keys:
                insights.append(Insight(
                    category='security',
                    severity='medium',
                    title='Sensitive Data in Configuration',
                    message=f'Configuration contains {len(set(sensitive_keys))} sensitive fields',
                    file_path=str(filepath),
                    suggestion='Ensure this file is in .gitignore and use environment variables',
                    impact='Secrets could be accidentally committed'
                ))

        return insights

    def _quality_insights(self, filepath: Path, content: str, context: FileContext) -> List[Insight]:
        """Code quality insights"""
        insights = []

        # Python-specific
        if context.language == 'python':
            # Missing type hints
            functions_with_hints = len(re.findall(r'def\s+\w+\([^)]*:\s*\w+', content))
            total_functions = context.functions

            if total_functions > 3 and functions_with_hints < total_functions * 0.5:
                insights.append(Insight(
                    category='quality',
                    severity='medium',
                    title='Missing Type Hints',
                    message=f'Only {functions_with_hints}/{total_functions} functions have type hints',
                    file_path=str(filepath),
                    suggestion='Add type hints for better IDE support and error detection',
                    impact='Improves code maintainability and catches type errors early'
                ))

            # Missing docstrings
            docstrings = len(re.findall(r'"""[^"]*"""', content))
            if total_functions > 3 and docstrings < total_functions * 0.5:
                insights.append(Insight(
                    category='quality',
                    severity='medium',
                    title='Insufficient Documentation',
                    message=f'Only ~{docstrings} docstrings for {total_functions} functions',
                    file_path=str(filepath),
                    suggestion='Add docstrings explaining function purpose, parameters, and return values',
                    impact='Improves code understanding and IDE help'
                ))

            # No error handling
            try_blocks = len(re.findall(r'\btry:', content))
            if try_blocks == 0 and ('open(' in content or 'requests.' in content or 'urllib' in content):
                insights.append(Insight(
                    category='quality',
                    severity='high',
                    title='Missing Error Handling',
                    message='I/O or network operations without try/except blocks',
                    file_path=str(filepath),
                    suggestion='Wrap risky operations in try/except blocks',
                    impact='Application may crash unexpectedly'
                ))

        # JavaScript/TypeScript
        if context.language in ['javascript', 'typescript']:
            # var usage
            var_count = len(re.findall(r'\bvar\s+', content))
            if var_count > 0:
                insights.append(Insight(
                    category='quality',
                    severity='medium',
                    title='Outdated var Declarations',
                    message=f'Found {var_count} var declarations',
                    file_path=str(filepath),
                    suggestion='Use const or let instead of var',
                    impact='Prevents scope-related bugs and improves code clarity'
                ))

            # Promise chains vs async/await
            if '.then(' in content and content.count('.then(') > 3 and 'async ' not in content:
                insights.append(Insight(
                    category='style',
                    severity='low',
                    title='Complex Promise Chains',
                    message='Long promise chains could be simplified',
                    file_path=str(filepath),
                    suggestion='Consider using async/await for better readability',
                    impact='Improves code readability and error handling'
                ))

        # Large files (any language)
        if context.code_lines > CONSTANT_500:
            insights.append(Insight(
                category='quality',
                severity='medium',
                title='Large File',
                message=f'{context.code_lines} lines of code in single file',
                file_path=str(filepath),
                suggestion='Consider splitting into smaller, focused modules',
                impact='Improves maintainability and testability'
            ))

        # Too many functions in one file
        if context.functions > 25:
            insights.append(Insight(
                category='quality',
                severity='medium',
                title='High Function Count',
                message=f'{context.functions} functions in one file',
                file_path=str(filepath),
                suggestion='Group related functions into classes or separate modules',
                impact='Improves code organization and navigation'
            ))

        # TODO/FIXME comments
        todos = re.findall(r'(TODO|FIXME|XXX|HACK)(:|\s)', content, re.IGNORECASE)
        if len(todos) > 5:
            insights.append(Insight(
                category='quality',
                severity='low',
                title='Many Pending Tasks',
                message=f'{len(todos)} TODO/FIXME comments found',
                file_path=str(filepath),
                suggestion='Address pending tasks or create tracked issues',
                impact='Technical debt tracking'
            ))

        return insights

    def _performance_insights(self, filepath: Path, content: str, context: FileContext) -> List[Insight]:
        """Performance insights"""
        insights = []

        # Python-specific
        if context.language == 'python':
            # Inefficient list operations
            if '+=' in content and 'for ' in content:
                list_appends = content.count('+=')
                if list_appends > 3:
                    insights.append(Insight(
                        category='performance',
                        severity='low',
                        title='Potentially Inefficient List Building',
                        message='Multiple list concatenations with += in loops',
                        file_path=str(filepath),
                        suggestion='Use list.append() or list comprehensions instead',
                        impact='Better performance for list building'
                    ))

        # Nested loops
        nested_for = len(re.findall(r'for\s+\w+\s+in[^:]+:\s*.*for\s+\w+\s+in', content, re.DOTALL))
        if nested_for > 2:
            insights.append(Insight(
                category='performance',
                severity='medium',
                title='Multiple Nested Loops',
                message=f'Found {nested_for} nested loop patterns',
                file_path=str(filepath),
                suggestion='Review algorithmic complexity - consider optimization',
                impact='May cause performance issues with large datasets'
            ))

        return insights

    def _style_insights(self, filepath: Path, content: str, context: FileContext) -> List[Insight]:
        """Code style insights"""
        insights = []

        # Magic numbers
        if context.language in ['python', 'javascript', 'typescript']:
            magic_numbers = re.findall(r'\b(CONSTANT_100|CONSTANT_1000|CONSTANT_256|CONSTANT_512|CONSTANT_1024|CONSTANT_86400|CONSTANT_3600)\b', content)
            if len(magic_numbers) > 5:
                insights.append(Insight(
                    category='style',
                    severity='low',
                    title='Magic Numbers',
                    message=f'Found {len(magic_numbers)} numeric literals',
                    file_path=str(filepath),
                    suggestion='Define named constants for important numbers',
                    impact='Improves code readability and maintainability'
                ))

        # Long lines
        long_lines = [i for i, line in enumerate(content.split('\n'), 1) if len(line) > CONSTANT_120]
        if len(long_lines) > 10:
            insights.append(Insight(
                category='style',
                severity='low',
                title='Many Long Lines',
                message=f'{len(long_lines)} lines exceed CONSTANT_120 characters',
                file_path=str(filepath),
                suggestion='Break long lines for better readability',
                impact='Improves code readability'
            ))

        return insights

    def _documentation_insights(self, filepath: Path, content: str, context: FileContext) -> List[Insight]:
        """Documentation insights"""
        insights = []

        # Documentation files
        if context.purpose == 'documentation':
            # Outdated dates
            current_year = datetime.now().year
            years = re.findall(r'\b(20\d{2})\b', content)
            if years and int(min(years)) < current_year - 2:
                insights.append(Insight(
                    category='documentation',
                    severity='low',
                    title='Potentially Outdated Documentation',
                    message=f'References dates from {min(years)}',
                    file_path=str(filepath),
                    suggestion='Review and update documentation',
                    impact='Users may follow outdated instructions'
                ))

            # Broken links (simple check)
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            if len(links) > 10:
                insights.append(Insight(
                    category='documentation',
                    severity='info',
                    title='Many External Links',
                    message=f'{len(links)} links found',
                    file_path=str(filepath),
                    suggestion='Periodically validate links to prevent rot',
                    impact='Broken links hurt user experience'
                ))

        # README-specific
        if 'readme' in filepath.name.lower():
            # Check for common sections
            has_install = bool(re.search(r'##?\s+(install|installation|setup)', content, re.IGNORECASE))
            has_usage = bool(re.search(r'##?\s+usage', content, re.IGNORECASE))
            has_examples = bool(re.search(r'##?\s+(example|demo)', content, re.IGNORECASE))

            missing_sections = []
            if not has_install:
                missing_sections.append('Installation')
            if not has_usage:
                missing_sections.append('Usage')
            if not has_examples:
                missing_sections.append('Examples')

            if missing_sections and context.size > CONSTANT_500:
                insights.append(Insight(
                    category='documentation',
                    severity='low',
                    title='Incomplete README',
                    message=f'Missing common sections: {", ".join(missing_sections)}',
                    file_path=str(filepath),
                    suggestion='Add standard sections for better user experience',
                    impact='Helps users understand and use your code'
                ))

        return insights


# ============================================================================
# MAIN ANALYZER - Orchestrates everything
# ============================================================================

class CodeAnalyzer:
    """Main intelligent code analyzer"""

    def __init__(self, target_path: str, verbose: bool = False):
        self.target = Path(target_path)
        self.verbose = verbose
        self.insight_generator = InsightGenerator()

        # Skip patterns
        self.skip_patterns = [
            r'\.git/', r'\.svn/', r'\.hg/',
            r'node_modules/', r'__pycache__/', r'\.pytest_cache/',
            r'venv/', r'env/', r'\.venv/',
            r'\.egg-info/', r'dist/', r'build/',
            r'\.pyc$', r'\.pyo$', r'\.class$', r'\.o$', r'\.so$',
            r'\.DS_Store$', r'Thumbs\.db$',
        ]

    def analyze(self) -> AnalysisResult:
        """Perform complete analysis"""

        if self.target.is_file():
            return self._analyze_file(self.target)
        elif self.target.is_dir():
            return self._analyze_directory(self.target)
        else:
            raise ValueError(f"Target not found: {self.target}")

    def _analyze_file(self, filepath: Path) -> AnalysisResult:
        """Analyze single file"""

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            logger.info(f"Error reading {filepath}: {e}")
            return AnalysisResult(
                target=str(filepath),
                timestamp=datetime.now().isoformat(),
                files_analyzed=0,
                contexts=[],
                insights=[],
                summary={'error': str(e)}
            )

        # Analyze context
        context = ContextAnalyzer.analyze_file(filepath, content)

        if self.verbose:
            logger.info(f"Analyzing: {filepath}")
            logger.info(f"  Language: {context.language}")
            logger.info(f"  Purpose: {context.purpose}")
            logger.info(f"  Complexity: {context.complexity_score}/10")

        # Generate insights
        insights = self.insight_generator.generate(filepath, content, context)

        # Create result
        return AnalysisResult(
            target=str(filepath),
            timestamp=datetime.now().isoformat(),
            files_analyzed=1,
            contexts=[context],
            insights=insights,
            summary=self._create_summary([context], insights)
        )

    def _analyze_directory(self, dirpath: Path) -> AnalysisResult:
        """Analyze entire directory"""

        # Find all relevant files
        all_files = [f for f in dirpath.rglob('*') if f.is_file()]
        files_to_analyze = [f for f in all_files if not self._should_skip(f)]

        logger.info(f"Found {len(files_to_analyze)} files to analyze (out of {len(all_files)} total)")

        contexts = []
        insights = []

        # Analyze each file
        for i, filepath in enumerate(files_to_analyze[:CONSTANT_100], 1):  # Limit to CONSTANT_100 files
            if self.verbose or i % 10 == 0:
                logger.info(f"Progress: {i}/{min(len(files_to_analyze), CONSTANT_100)}")

            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                context = ContextAnalyzer.analyze_file(filepath, content)
                contexts.append(context)

                file_insights = self.insight_generator.generate(filepath, content, context)
                insights.extend(file_insights)

            except Exception as e:
                if self.verbose:
                    logger.info(f"Error analyzing {filepath}: {e}")

        return AnalysisResult(
            target=str(dirpath),
            timestamp=datetime.now().isoformat(),
            files_analyzed=len(contexts),
            contexts=contexts,
            insights=insights,
            summary=self._create_summary(contexts, insights)
        )

    def _should_skip(self, filepath: Path) -> bool:
        """Check if file should be skipped"""
        path_str = str(filepath)
        return any(re.search(pattern, path_str) for pattern in self.skip_patterns)

    def _create_summary(self, contexts: List[FileContext], insights: List[Insight]) -> Dict:
        """Create analysis summary"""

        # Count by severity
        by_severity = Counter([i.severity for i in insights])

        # Count by category
        by_category = Counter([i.category for i in insights])

        # Languages detected
        languages = Counter([c.language for c in contexts if c.language])

        # Frameworks detected
        frameworks = Counter([fw for c in contexts for fw in c.frameworks])

        # Purposes detected
        purposes = Counter([c.purpose for c in contexts])

        # Complexity distribution
        complexity_dist = {
            'low (1-3)': len([c for c in contexts if c.complexity_score <= 3]),
            'medium (4-6)': len([c for c in contexts if 4 <= c.complexity_score <= 6]),
            'high (7-10)': len([c for c in contexts if c.complexity_score >= 7]),
        }

        return {
            'total_insights': len(insights),
            'by_severity': dict(by_severity),
            'by_category': dict(by_category),
            'languages': dict(languages),
            'frameworks': dict(frameworks),
            'purposes': dict(purposes),
            'complexity_distribution': complexity_dist,
            'total_code_lines': sum(c.code_lines for c in contexts),
            'total_functions': sum(c.functions for c in contexts),
            'total_classes': sum(c.classes for c in contexts),
        }


# ============================================================================
# REPORTING - Beautiful, organized output
# ============================================================================

class AnalysisReporter:
    """Generates formatted reports"""

    # ANSI color codes
    COLORS = {
        'critical': '\CONSTANT_33[91m',  # Red
        'high': '\CONSTANT_33[93m',      # Yellow
        'medium': '\CONSTANT_33[94m',    # Blue
        'low': '\CONSTANT_33[92m',       # Green
        'info': '\CONSTANT_33[96m',      # Cyan
        'reset': '\CONSTANT_33[0m',
        'bold': '\CONSTANT_33[1m',
    }

    SEVERITY_ORDER = ['critical', 'high', 'medium', 'low', 'info']
    CATEGORY_ICONS = {
        'security': '🔒',
        'quality': '✨',
        'performance': '⚡',
        'style': '🎨',
        'documentation': '📚',
    }

    @staticmethod
    def print_report(result: AnalysisResult, show_details: bool = True):
        """Print comprehensive analysis report"""

        logger.info(Path("\n") + "="*80)
        logger.info(f"{AnalysisReporter.COLORS['bold']}📊 INTELLIGENT CODE ANALYSIS REPORT{AnalysisReporter.COLORS['reset']}")
        logger.info("="*80)

        # Overview
        logger.info(f"\n{AnalysisReporter.COLORS['bold']}📁 Target:{AnalysisReporter.COLORS['reset']} {result.target}")
        logger.info(f"{AnalysisReporter.COLORS['bold']}⏱  Timestamp:{AnalysisReporter.COLORS['reset']} {result.timestamp}")
        logger.info(f"{AnalysisReporter.COLORS['bold']}📄 Files Analyzed:{AnalysisReporter.COLORS['reset']} {result.files_analyzed}")

        summary = result.summary

        # Summary statistics
        logger.info(f"\n{AnalysisReporter.COLORS['bold']}📈 Code Metrics:{AnalysisReporter.COLORS['reset']}")
        logger.info(f"  Lines of Code: {summary.get('total_code_lines', 0):,}")
        logger.info(f"  Functions: {summary.get('total_functions', 0)}")
        logger.info(f"  Classes: {summary.get('total_classes', 0)}")

        # Languages
        if summary.get('languages'):
            logger.info(f"\n{AnalysisReporter.COLORS['bold']}💻 Languages:{AnalysisReporter.COLORS['reset']}")
            for lang, count in sorted(summary['languages'].items(), key=lambda x: x[1], reverse=True):
                logger.info(f"  {lang}: {count} files")

        # Frameworks
        if summary.get('frameworks'):
            logger.info(f"\n{AnalysisReporter.COLORS['bold']}🔧 Frameworks:{AnalysisReporter.COLORS['reset']}")
            for fw, count in sorted(summary['frameworks'].items(), key=lambda x: x[1], reverse=True):
                logger.info(f"  {fw}: {count} files")

        # Complexity distribution
        if summary.get('complexity_distribution'):
            logger.info(f"\n{AnalysisReporter.COLORS['bold']}📊 Complexity Distribution:{AnalysisReporter.COLORS['reset']}")
            for level, count in summary['complexity_distribution'].items():
                logger.info(f"  {level}: {count} files")

        # Insights summary
        logger.info(f"\n{AnalysisReporter.COLORS['bold']}💡 Insights Found: {summary.get('total_insights', 0)}{AnalysisReporter.COLORS['reset']}")

        if summary.get('by_severity'):
            logger.info(f"\n{AnalysisReporter.COLORS['bold']}⚠️  By Severity:{AnalysisReporter.COLORS['reset']}")
            for severity in AnalysisReporter.SEVERITY_ORDER:
                count = summary['by_severity'].get(severity, 0)
                if count > 0:
                    color = AnalysisReporter.COLORS.get(severity, '')
                    logger.info(f"  {color}{severity.upper()}: {count}{AnalysisReporter.COLORS['reset']}")

        if summary.get('by_category'):
            logger.info(f"\n{AnalysisReporter.COLORS['bold']}📂 By Category:{AnalysisReporter.COLORS['reset']}")
            for category, count in sorted(summary['by_category'].items(), key=lambda x: x[1], reverse=True):
                icon = AnalysisReporter.CATEGORY_ICONS.get(category, '•')
                logger.info(f"  {icon} {category.title()}: {count}")

        # Detailed insights
        if show_details and result.insights:
            logger.info(f"\n{AnalysisReporter.COLORS['bold']}{'='*80}")
            logger.info(f"DETAILED INSIGHTS")
            logger.info(f"{'='*80}{AnalysisReporter.COLORS['reset']}\n")

            # Group by severity
            for severity in AnalysisReporter.SEVERITY_ORDER:
                insights = [i for i in result.insights if i.severity == severity]
                if not insights:
                    continue

                color = AnalysisReporter.COLORS.get(severity, '')
                logger.info(f"\n{color}{AnalysisReporter.COLORS['bold']}{severity.upper()} PRIORITY ({len(insights)} issues){AnalysisReporter.COLORS['reset']}")
                logger.info("-" * 80)

                for insight in insights:
                    icon = AnalysisReporter.CATEGORY_ICONS.get(insight.category, '•')
                    logger.info(f"\n{color}{icon} {insight.title}{AnalysisReporter.COLORS['reset']}")
                    logger.info(f"   File: {insight.file_path}")
                    logger.info(f"   {insight.message}")
                    if insight.suggestion:
                        logger.info(f"   💡 Suggestion: {insight.suggestion}")
                    if insight.impact:
                        logger.info(f"   📌 Impact: {insight.impact}")

        logger.info(Path("\n") + "="*80)
        logger.info(f"{AnalysisReporter.COLORS['bold']}✅ Analysis Complete{AnalysisReporter.COLORS['reset']}")
        logger.info("="*80 + Path("\n"))

    @staticmethod
    def save_json(result: AnalysisResult, output_path: Path):
        """Save results as JSON"""
        data = {
            'target': result.target,
            'timestamp': result.timestamp,
            'files_analyzed': result.files_analyzed,
            'contexts': [asdict(c) for c in result.contexts],
            'insights': [asdict(i) for i in result.insights],
            'summary': result.summary,
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"💾 Results saved to: {output_path}")


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Intelligent Code Analyzer - Adaptive content-aware analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single file
  python code_analyzer.py script.py

  # Analyze a directory
  python code_analyzer.py /path/to/project

  # Verbose output
  python code_analyzer.py /path/to/project --verbose

  # Save results to JSON
  python code_analyzer.py /path/to/project --output results.json

  # Quick summary (no details)
  python code_analyzer.py /path/to/project --summary-only
        """
    )

    parser.add_argument('target', help='File or directory to analyze')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-o', '--output', help='Save results to JSON file')
    parser.add_argument('-s', '--summary-only', action='store_true', help='Show summary only (no detailed insights)')

    args = parser.parse_args()

    # Run analysis
    logger.info(f"🔍 Starting intelligent analysis of: {args.target}\n")

    analyzer = CodeAnalyzer(args.target, verbose=args.verbose)
    result = analyzer.analyze()

    # Print report
    AnalysisReporter.print_report(result, show_details=not args.summary_only)

    # Save JSON if requested
    if args.output:
        AnalysisReporter.save_json(result, Path(args.output))


if __name__ == '__main__':
    main()

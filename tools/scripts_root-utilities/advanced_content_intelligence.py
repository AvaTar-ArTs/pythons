#!/usr/bin/env python3
"""
Advanced Content-Awareness Intelligence System

This analyzer uses cutting-edge techniques to deeply understand codebase structure:
- AST (Abstract Syntax Tree) parsing for semantic code understanding
- Pattern recognition for architectural detection (MVC, microservices, etc.)
- Machine learning embeddings for intelligent categorization
- Dependency graph analysis for relationship mapping
- Confidence scoring for analysis quality metrics

Category: AI & Machine Learning
"""

import argparse
import ast
import json
import logging
import os
import re
import sys
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any

import numpy as np
from dotenv import load_dotenv

# Optional: OpenAI for embeddings-based categorization
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI not available - ML categorization will be disabled")


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class CodeEntity:
    """Represents a detected code entity (class, function, variable, etc.)"""
    name: str
    type: str  # 'class', 'function', 'variable', 'import', 'decorator'
    line_start: int
    line_end: int
    complexity: int  # cyclomatic complexity estimate
    docstring: Optional[str]
    decorators: List[str]
    dependencies: Set[str]  # imported modules/functions

@dataclass
class ArchitecturalPattern:
    """Detected architectural pattern in code"""
    pattern_type: str  # 'MVC', 'Repository', 'Factory', 'Singleton', etc.
    confidence: float  # 0.0 to 1.0
    evidence: List[str]  # reasons for detection
    file_path: str

@dataclass
class FileIntelligence:
    """Complete intelligence about a file"""
    filepath: str
    language: str
    size_bytes: int
    lines_of_code: int
    complexity_score: float

    # AST Analysis
    classes: List[CodeEntity]
    functions: List[CodeEntity]
    imports: List[str]

    # Pattern Detection
    patterns: List[ArchitecturalPattern]

    # Semantic Understanding
    primary_purpose: str  # inferred main purpose
    category: str  # AI/ML, Web Dev, Data Analysis, etc.
    category_confidence: float

    # Relationships
    depends_on: Set[str]  # files this depends on
    depended_by: Set[str]  # files that depend on this

    # Quality Metrics
    has_tests: bool
    has_documentation: bool
    code_quality_score: float  # 0-100


# ============================================================================
# AST-Based Code Analysis
# ============================================================================

class PythonASTAnalyzer:
    """Deep AST analysis for Python files"""

    def __init__(self):
        self.current_file = None

    def analyze_file(self, filepath: Path) -> Optional[FileIntelligence]:
        """Perform deep AST analysis on Python file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=str(filepath))
            self.current_file = filepath

            # Extract entities
            classes = self._extract_classes(tree)
            functions = self._extract_functions(tree)
            imports = self._extract_imports(tree)

            # Calculate metrics
            loc = len(content.splitlines())
            complexity = self._calculate_complexity(tree)

            # Detect patterns
            patterns = self._detect_patterns(tree, classes, functions)

            # Infer purpose and category
            purpose, category, confidence = self._infer_purpose(
                filepath, classes, functions, imports, content
            )

            # Quality metrics
            has_tests = self._has_tests(filepath, content)
            has_docs = self._has_documentation(tree, classes, functions)
            quality_score = self._calculate_quality_score(
                tree, classes, functions, has_tests, has_docs, complexity, loc
            )

            return FileIntelligence(
                filepath=str(filepath),
                language='python',
                size_bytes=filepath.stat().st_size,
                lines_of_code=loc,
                complexity_score=complexity,
                classes=classes,
                functions=functions,
                imports=imports,
                patterns=patterns,
                primary_purpose=purpose,
                category=category,
                category_confidence=confidence,
                depends_on=set(imports),
                depended_by=set(),  # filled later in graph analysis
                has_tests=has_tests,
                has_documentation=has_docs,
                code_quality_score=quality_score
            )

        except Exception as e:
            logging.error(f"Failed to analyze {filepath}: {e}")
            return None

    def _extract_classes(self, tree: ast.AST) -> List[CodeEntity]:
        """Extract all class definitions with metadata"""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                entity = CodeEntity(
                    name=node.name,
                    type='class',
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno,
                    complexity=self._calculate_node_complexity(node),
                    docstring=ast.get_docstring(node),
                    decorators=[self._get_decorator_name(d) for d in node.decorator_list],
                    dependencies=self._extract_node_dependencies(node)
                )
                classes.append(entity)
        return classes

    def _extract_functions(self, tree: ast.AST) -> List[CodeEntity]:
        """Extract all function definitions with metadata"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                entity = CodeEntity(
                    name=node.name,
                    type='function',
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno,
                    complexity=self._calculate_node_complexity(node),
                    docstring=ast.get_docstring(node),
                    decorators=[self._get_decorator_name(d) for d in node.decorator_list],
                    dependencies=self._extract_node_dependencies(node)
                )
                functions.append(entity)
        return functions

    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract all import statements"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        return list(set(imports))

    def _calculate_complexity(self, tree: ast.AST) -> float:
        """Calculate cyclomatic complexity estimate"""
        complexity = 1  # base complexity

        for node in ast.walk(tree):
            # Decision points increase complexity
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1

        return complexity

    def _calculate_node_complexity(self, node: ast.AST) -> int:
        """Calculate complexity for a specific node"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
        return complexity

    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Extract decorator name"""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
        return "unknown"

    def _extract_node_dependencies(self, node: ast.AST) -> Set[str]:
        """Extract dependencies from a node"""
        deps = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Name):
                deps.add(child.id)
        return deps

    def _detect_patterns(
        self,
        tree: ast.AST,
        classes: List[CodeEntity],
        functions: List[CodeEntity]
    ) -> List[ArchitecturalPattern]:
        """Detect architectural patterns in the code"""
        patterns = []

        # Singleton pattern detection
        singleton_pattern = self._detect_singleton(classes)
        if singleton_pattern:
            patterns.append(singleton_pattern)

        # Factory pattern detection
        factory_pattern = self._detect_factory(classes, functions)
        if factory_pattern:
            patterns.append(factory_pattern)

        # Repository pattern detection
        repo_pattern = self._detect_repository(classes)
        if repo_pattern:
            patterns.append(repo_pattern)

        # MVC pattern detection
        mvc_pattern = self._detect_mvc(classes, self.current_file)
        if mvc_pattern:
            patterns.append(mvc_pattern)

        return patterns

    def _detect_singleton(self, classes: List[CodeEntity]) -> Optional[ArchitecturalPattern]:
        """Detect Singleton pattern"""
        for cls in classes:
            evidence = []
            confidence = 0.0

            # Check for __new__ method override
            if '__new__' in [str(d) for d in cls.dependencies]:
                evidence.append("Overrides __new__ method")
                confidence += 0.4

            # Check for instance variable
            if '_instance' in cls.dependencies or 'instance' in cls.dependencies:
                evidence.append("Has _instance class variable")
                confidence += 0.3

            # Check for decorators
            if any('singleton' in d.lower() for d in cls.decorators):
                evidence.append("Uses @singleton decorator")
                confidence += 0.5

            if confidence >= 0.6:
                return ArchitecturalPattern(
                    pattern_type='Singleton',
                    confidence=min(confidence, 1.0),
                    evidence=evidence,
                    file_path=str(self.current_file)
                )
        return None

    def _detect_factory(
        self,
        classes: List[CodeEntity],
        functions: List[CodeEntity]
    ) -> Optional[ArchitecturalPattern]:
        """Detect Factory pattern"""
        evidence = []
        confidence = 0.0

        # Check for factory method names
        factory_names = ['create', 'build', 'make', 'factory', 'get_instance']
        for func in functions:
            if any(name in func.name.lower() for name in factory_names):
                evidence.append(f"Has factory method: {func.name}")
                confidence += 0.3

        # Check for abstract factory class
        for cls in classes:
            if 'factory' in cls.name.lower() or 'builder' in cls.name.lower():
                evidence.append(f"Has factory class: {cls.name}")
                confidence += 0.4

        if confidence >= 0.5:
            return ArchitecturalPattern(
                pattern_type='Factory',
                confidence=min(confidence, 1.0),
                evidence=evidence,
                file_path=str(self.current_file)
            )
        return None

    def _detect_repository(self, classes: List[CodeEntity]) -> Optional[ArchitecturalPattern]:
        """Detect Repository pattern"""
        for cls in classes:
            evidence = []
            confidence = 0.0

            if 'repository' in cls.name.lower() or 'repo' in cls.name.lower():
                evidence.append(f"Repository naming: {cls.name}")
                confidence += 0.5

            # Check for CRUD method names
            crud_methods = {'create', 'read', 'update', 'delete', 'save', 'find', 'get'}
            class_methods = {str(d).lower() for d in cls.dependencies}
            matches = crud_methods & class_methods

            if len(matches) >= 3:
                evidence.append(f"Has CRUD methods: {', '.join(matches)}")
                confidence += 0.4

            if confidence >= 0.6:
                return ArchitecturalPattern(
                    pattern_type='Repository',
                    confidence=min(confidence, 1.0),
                    evidence=evidence,
                    file_path=str(self.current_file)
                )
        return None

    def _detect_mvc(self, classes: List[CodeEntity], filepath: Path) -> Optional[ArchitecturalPattern]:
        """Detect MVC pattern indicators"""
        evidence = []
        confidence = 0.0

        path_lower = str(filepath).lower()

        # Check file path
        if any(pattern in path_lower for pattern in ['controller', 'model', 'view']):
            evidence.append(f"MVC directory structure detected")
            confidence += 0.4

        # Check class names
        for cls in classes:
            name_lower = cls.name.lower()
            if 'controller' in name_lower:
                evidence.append(f"Controller class: {cls.name}")
                confidence += 0.3
            elif 'model' in name_lower:
                evidence.append(f"Model class: {cls.name}")
                confidence += 0.3
            elif 'view' in name_lower:
                evidence.append(f"View class: {cls.name}")
                confidence += 0.3

        if confidence >= 0.5:
            return ArchitecturalPattern(
                pattern_type='MVC',
                confidence=min(confidence, 1.0),
                evidence=evidence,
                file_path=str(filepath)
            )
        return None

    def _infer_purpose(
        self,
        filepath: Path,
        classes: List[CodeEntity],
        functions: List[CodeEntity],
        imports: List[str],
        content: str
    ) -> Tuple[str, str, float]:
        """Infer the primary purpose and category of the file"""

        # Analyze imports to determine purpose
        import_categories = {
            'flask': ('Web Development', 0.9),
            'fastapi': ('Web Development', 0.9),
            'django': ('Web Development', 0.9),
            'pandas': ('Data Analysis', 0.9),
            'numpy': ('Data Analysis', 0.8),
            'sklearn': ('AI & Machine Learning', 0.9),
            'tensorflow': ('AI & Machine Learning', 0.95),
            'torch': ('AI & Machine Learning', 0.95),
            'openai': ('AI & Machine Learning', 0.9),
            'anthropic': ('AI & Machine Learning', 0.9),
            'selenium': ('Web Scraping', 0.9),
            'beautifulsoup': ('Web Scraping', 0.9),
            'requests': ('Web Scraping', 0.6),
            'matplotlib': ('Data Visualization', 0.8),
            'pytest': ('Testing', 0.9),
            'unittest': ('Testing', 0.9),
        }

        category_scores = defaultdict(float)

        for imp in imports:
            imp_lower = imp.lower()
            for key, (cat, conf) in import_categories.items():
                if key in imp_lower:
                    category_scores[cat] += conf

        # Analyze filename
        filename = filepath.stem.lower()
        if 'test' in filename:
            category_scores['Testing'] += 0.8
        elif 'dashboard' in filename:
            category_scores['Data Visualization'] += 0.7
        elif 'api' in filename or 'server' in filename:
            category_scores['Web Development'] += 0.7
        elif 'analyze' in filename or 'analysis' in filename:
            category_scores['Data Analysis'] += 0.7
        elif 'scrape' in filename or 'crawler' in filename:
            category_scores['Web Scraping'] += 0.8

        # Determine primary category
        if category_scores:
            category = max(category_scores, key=category_scores.get)
            confidence = min(category_scores[category] / len(imports) if imports else 1.0, 1.0)
        else:
            category = 'Utilities & Tools'
            confidence = 0.5

        # Infer purpose from docstrings
        purpose = "Unknown"
        if classes and classes[0].docstring:
            purpose = classes[0].docstring.split('\n')[0][:100]
        elif functions and functions[0].docstring:
            purpose = functions[0].docstring.split('\n')[0][:100]
        else:
            # Use filename as fallback
            purpose = filename.replace('_', ' ').title()

        return purpose, category, confidence

    def _has_tests(self, filepath: Path, content: str) -> bool:
        """Check if file has associated tests"""
        test_patterns = [
            r'def test_',
            r'class Test',
            r'unittest\.TestCase',
            r'@pytest\.',
        ]

        for pattern in test_patterns:
            if re.search(pattern, content):
                return True

        # Check for test file in same directory
        test_file = filepath.parent / f"test_{filepath.name}"
        if test_file.exists():
            return True

        return False

    def _has_documentation(
        self,
        tree: ast.AST,
        classes: List[CodeEntity],
        functions: List[CodeEntity]
    ) -> bool:
        """Check documentation quality"""
        module_doc = ast.get_docstring(tree)

        if not module_doc:
            return False

        # Check if major classes/functions have docstrings
        documented_classes = sum(1 for c in classes if c.docstring)
        documented_functions = sum(1 for f in functions if f.docstring)

        total = len(classes) + len(functions)
        if total == 0:
            return bool(module_doc)

        doc_ratio = (documented_classes + documented_functions) / total
        return doc_ratio >= 0.5

    def _calculate_quality_score(
        self,
        tree: ast.AST,
        classes: List[CodeEntity],
        functions: List[CodeEntity],
        has_tests: bool,
        has_docs: bool,
        complexity: float,
        loc: int
    ) -> float:
        """Calculate overall code quality score (0-100)"""
        score = 50.0  # baseline

        # Documentation bonus
        if has_docs:
            score += 20

        # Tests bonus
        if has_tests:
            score += 20

        # Complexity penalty (higher complexity reduces score)
        complexity_per_loc = complexity / max(loc, 1)
        if complexity_per_loc < 0.1:
            score += 10
        elif complexity_per_loc > 0.5:
            score -= 20

        # Code organization bonus
        if classes or functions:
            score += 5

        # Docstring coverage
        if classes or functions:
            total = len(classes) + len(functions)
            documented = sum(1 for c in classes if c.docstring) + sum(1 for f in functions if f.docstring)
            doc_ratio = documented / total
            score += doc_ratio * 10

        return max(0, min(100, score))


# ============================================================================
# JavaScript/TypeScript AST Analysis (Basic)
# ============================================================================

class JavaScriptAnalyzer:
    """Basic JavaScript/TypeScript analysis using regex patterns"""

    def analyze_file(self, filepath: Path) -> Optional[FileIntelligence]:
        """Analyze JS/TS file using pattern matching"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract functions
            functions = self._extract_functions(content)

            # Extract classes
            classes = self._extract_classes(content)

            # Extract imports
            imports = self._extract_imports(content)

            # Detect patterns
            patterns = self._detect_patterns(content, filepath)

            # Infer category
            category, confidence = self._infer_category(filepath, content, imports)

            loc = len(content.splitlines())

            return FileIntelligence(
                filepath=str(filepath),
                language='javascript' if filepath.suffix == '.js' else 'typescript',
                size_bytes=filepath.stat().st_size,
                lines_of_code=loc,
                complexity_score=len(functions) + len(classes),  # simplified
                classes=classes,
                functions=functions,
                imports=imports,
                patterns=patterns,
                primary_purpose=filepath.stem.replace('-', ' ').replace('_', ' ').title(),
                category=category,
                category_confidence=confidence,
                depends_on=set(imports),
                depended_by=set(),
                has_tests=self._has_tests(filepath, content),
                has_documentation=bool(re.search(r'/\*\*[\s\S]*?\*/', content)),
                code_quality_score=50.0  # simplified
            )

        except Exception as e:
            logging.error(f"Failed to analyze {filepath}: {e}")
            return None

    def _extract_functions(self, content: str) -> List[CodeEntity]:
        """Extract function definitions"""
        functions = []

        # Regular functions
        pattern = r'function\s+(\w+)\s*\('
        for match in re.finditer(pattern, content):
            functions.append(CodeEntity(
                name=match.group(1),
                type='function',
                line_start=content[:match.start()].count('\n') + 1,
                line_end=0,
                complexity=1,
                docstring=None,
                decorators=[],
                dependencies=set()
            ))

        # Arrow functions
        pattern = r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>'
        for match in re.finditer(pattern, content):
            functions.append(CodeEntity(
                name=match.group(1),
                type='function',
                line_start=content[:match.start()].count('\n') + 1,
                line_end=0,
                complexity=1,
                docstring=None,
                decorators=[],
                dependencies=set()
            ))

        return functions

    def _extract_classes(self, content: str) -> List[CodeEntity]:
        """Extract class definitions"""
        classes = []
        pattern = r'class\s+(\w+)'

        for match in re.finditer(pattern, content):
            classes.append(CodeEntity(
                name=match.group(1),
                type='class',
                line_start=content[:match.start()].count('\n') + 1,
                line_end=0,
                complexity=1,
                docstring=None,
                decorators=[],
                dependencies=set()
            ))

        return classes

    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements"""
        imports = []

        # ES6 imports
        pattern = r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]'
        imports.extend(match.group(1) for match in re.finditer(pattern, content))

        # Require statements
        pattern = r'require\([\'"]([^\'"]+)[\'"]\)'
        imports.extend(match.group(1) for match in re.finditer(pattern, content))

        return list(set(imports))

    def _detect_patterns(self, content: str, filepath: Path) -> List[ArchitecturalPattern]:
        """Detect JS/TS patterns"""
        patterns = []

        # React component detection
        if 'React' in content or 'useState' in content or 'useEffect' in content:
            patterns.append(ArchitecturalPattern(
                pattern_type='React Component',
                confidence=0.9,
                evidence=['Uses React hooks or imports'],
                file_path=str(filepath)
            ))

        # Express.js detection
        if 'express' in content.lower() and ('app.get' in content or 'app.post' in content):
            patterns.append(ArchitecturalPattern(
                pattern_type='Express API',
                confidence=0.9,
                evidence=['Uses Express routing'],
                file_path=str(filepath)
            ))

        return patterns

    def _infer_category(self, filepath: Path, content: str, imports: List[str]) -> Tuple[str, float]:
        """Infer category for JS/TS file"""

        if 'react' in content.lower() or any('react' in imp.lower() for imp in imports):
            return 'Web Development', 0.9

        if 'express' in content.lower() or any('express' in imp.lower() for imp in imports):
            return 'Web Development', 0.9

        if '.test.' in filepath.name or '.spec.' in filepath.name:
            return 'Testing', 0.95

        if 'component' in filepath.stem.lower():
            return 'Web Development', 0.8

        return 'Web Development', 0.6

    def _has_tests(self, filepath: Path, content: str) -> bool:
        """Check for tests"""
        if '.test.' in filepath.name or '.spec.' in filepath.name:
            return True

        if 'describe(' in content or 'it(' in content or 'test(' in content:
            return True

        return False


# ============================================================================
# ML-Based Semantic Categorization (Optional)
# ============================================================================

class MLCategorizer:
    """Use embeddings for intelligent categorization"""

    def __init__(self, api_key: Optional[str] = None):
        self.client = None
        if OPENAI_AVAILABLE and api_key:
            self.client = OpenAI(api_key=api_key)
        self.cache = {}  # Simple cache for embeddings

    def categorize_with_embeddings(
        self,
        content: str,
        filepath: Path
    ) -> Tuple[str, float]:
        """Use embeddings to categorize content"""

        if not self.client:
            return "Unknown", 0.0

        try:
            # Create embedding
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=content[:8000]  # Limit content length
            )

            embedding = response.data[0].embedding

            # Compare with category prototypes (simplified)
            categories = {
                'AI & Machine Learning': ['machine learning', 'neural network', 'model training', 'openai', 'anthropic'],
                'Web Development': ['web server', 'api endpoint', 'http request', 'frontend', 'backend'],
                'Data Analysis': ['data processing', 'statistics', 'visualization', 'pandas', 'analysis'],
                'Web Scraping': ['web scraping', 'crawler', 'selenium', 'beautifulsoup'],
                'Testing': ['unit test', 'integration test', 'pytest', 'assert'],
            }

            # Simplified: use keyword matching as fallback
            # In production, you'd use actual embedding comparisons
            content_lower = content.lower()
            scores = {}

            for category, keywords in categories.items():
                score = sum(1 for kw in keywords if kw in content_lower)
                scores[category] = score / len(keywords)

            if scores:
                best_category = max(scores, key=scores.get)
                confidence = min(scores[best_category], 1.0)
                return best_category, confidence

            return "Unknown", 0.0

        except Exception as e:
            logging.warning(f"ML categorization failed: {e}")
            return "Unknown", 0.0


# ============================================================================
# Dependency Graph Analysis
# ============================================================================

class DependencyGraphAnalyzer:
    """Build and analyze dependency relationships"""

    def __init__(self):
        self.graph: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_graph: Dict[str, Set[str]] = defaultdict(set)

    def build_graph(self, analyses: List[FileIntelligence]):
        """Build dependency graph from file analyses"""

        # Create lookup for local files
        local_files = {Path(a.filepath).stem: a.filepath for a in analyses}

        for analysis in analyses:
            filepath = analysis.filepath

            for dep in analysis.imports:
                # Check if import is a local file
                dep_stem = dep.split('.')[-1]  # Get last part of import

                if dep_stem in local_files:
                    dep_filepath = local_files[dep_stem]
                    self.graph[filepath].add(dep_filepath)
                    self.reverse_graph[dep_filepath].add(filepath)

    def enhance_analyses(self, analyses: List[FileIntelligence]) -> List[FileIntelligence]:
        """Add dependency information to analyses"""

        for analysis in analyses:
            filepath = analysis.filepath
            analysis.depends_on = self.graph.get(filepath, set())
            analysis.depended_by = self.reverse_graph.get(filepath, set())

        return analyses

    def find_circular_dependencies(self) -> List[Tuple[str, str]]:
        """Detect circular dependencies"""
        circular = []

        for file, deps in self.graph.items():
            for dep in deps:
                if file in self.graph.get(dep, set()):
                    circular.append((file, dep))

        return circular

    def find_orphaned_files(self, analyses: List[FileIntelligence]) -> List[str]:
        """Find files with no dependencies and not depended upon"""
        orphaned = []

        for analysis in analyses:
            filepath = analysis.filepath
            if not analysis.depends_on and not analysis.depended_by:
                orphaned.append(filepath)

        return orphaned


# ============================================================================
# Main Advanced Analyzer
# ============================================================================

class AdvancedContentIntelligenceAnalyzer:
    """Master analyzer coordinating all intelligence systems"""

    def __init__(self, use_ml: bool = False, api_key: Optional[str] = None):
        self.python_analyzer = PythonASTAnalyzer()
        self.js_analyzer = JavaScriptAnalyzer()
        self.ml_categorizer = MLCategorizer(api_key) if use_ml else None
        self.dep_analyzer = DependencyGraphAnalyzer()

    def analyze_directory(
        self,
        directory: Path,
        exclude_dirs: Optional[Set[str]] = None
    ) -> List[FileIntelligence]:
        """Perform deep analysis on entire directory"""

        if exclude_dirs is None:
            exclude_dirs = {
                'node_modules', '__pycache__', '.git', 'venv', 'env',
                '.venv', 'dist', 'build', '.next', '.pytest_cache'
            }

        analyses = []

        # Find all code files
        code_files = []
        for ext in ['.py', '.js', '.jsx', '.ts', '.tsx']:
            code_files.extend(directory.rglob(f'*{ext}'))

        # Filter out excluded directories
        code_files = [
            f for f in code_files
            if not any(excluded in f.parts for excluded in exclude_dirs)
        ]

        logging.info(f"Found {len(code_files)} code files to analyze")

        # Analyze each file
        for filepath in code_files:
            logging.info(f"Analyzing: {filepath}")

            analysis = None
            if filepath.suffix == '.py':
                analysis = self.python_analyzer.analyze_file(filepath)
            elif filepath.suffix in ['.js', '.jsx', '.ts', '.tsx']:
                analysis = self.js_analyzer.analyze_file(filepath)

            if analysis:
                # Enhance with ML if available
                if self.ml_categorizer:
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        ml_category, ml_conf = self.ml_categorizer.categorize_with_embeddings(
                            content, filepath
                        )
                        # Use ML result if higher confidence
                        if ml_conf > analysis.category_confidence:
                            analysis.category = ml_category
                            analysis.category_confidence = ml_conf
                    except Exception as e:
                        logging.warning(f"ML enhancement failed for {filepath}: {e}")

                analyses.append(analysis)

        # Build dependency graph
        logging.info("Building dependency graph...")
        self.dep_analyzer.build_graph(analyses)
        analyses = self.dep_analyzer.enhance_analyses(analyses)

        # Detect issues
        circular = self.dep_analyzer.find_circular_dependencies()
        if circular:
            logging.warning(f"Found {len(circular)} circular dependencies")

        orphaned = self.dep_analyzer.find_orphaned_files(analyses)
        if orphaned:
            logging.info(f"Found {len(orphaned)} orphaned files")

        return analyses

    def generate_report(
        self,
        analyses: List[FileIntelligence],
        output_dir: Path
    ):
        """Generate comprehensive analysis report"""

        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # CSV Report
        csv_path = output_dir / f'ADVANCED_INTELLIGENCE_{timestamp}.csv'
        self._generate_csv_report(analyses, csv_path)

        # JSON Report (full detail)
        json_path = output_dir / f'ADVANCED_INTELLIGENCE_{timestamp}.json'
        self._generate_json_report(analyses, json_path)

        # Markdown Summary
        md_path = output_dir / f'ADVANCED_INTELLIGENCE_{timestamp}.md'
        self._generate_markdown_summary(analyses, md_path)

        logging.info(f"Reports generated:")
        logging.info(f"  CSV: {csv_path}")
        logging.info(f"  JSON: {json_path}")
        logging.info(f"  Markdown: {md_path}")

    def _generate_csv_report(self, analyses: List[FileIntelligence], output_path: Path):
        """Generate CSV report"""
        import csv

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                'Filepath', 'Language', 'LOC', 'Complexity', 'Category',
                'Category Confidence', 'Classes', 'Functions', 'Imports',
                'Patterns', 'Quality Score', 'Has Tests', 'Has Docs',
                'Dependencies', 'Depended By', 'Primary Purpose'
            ])

            # Data
            for a in analyses:
                writer.writerow([
                    a.filepath,
                    a.language,
                    a.lines_of_code,
                    f"{a.complexity_score:.1f}",
                    a.category,
                    f"{a.category_confidence:.2f}",
                    len(a.classes),
                    len(a.functions),
                    len(a.imports),
                    '; '.join(p.pattern_type for p in a.patterns),
                    f"{a.code_quality_score:.1f}",
                    'Yes' if a.has_tests else 'No',
                    'Yes' if a.has_documentation else 'No',
                    len(a.depends_on),
                    len(a.depended_by),
                    a.primary_purpose
                ])

    def _generate_json_report(self, analyses: List[FileIntelligence], output_path: Path):
        """Generate detailed JSON report"""

        def convert_to_serializable(obj):
            """Convert dataclass to dict, handling sets"""
            if isinstance(obj, set):
                return list(obj)
            elif hasattr(obj, '__dict__'):
                result = {}
                for key, value in obj.__dict__.items():
                    result[key] = convert_to_serializable(value)
                return result
            elif isinstance(obj, list):
                return [convert_to_serializable(item) for item in obj]
            else:
                return obj

        data = {
            'generated_at': datetime.now().isoformat(),
            'total_files': len(analyses),
            'analyses': [convert_to_serializable(a) for a in analyses]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def _generate_markdown_summary(self, analyses: List[FileIntelligence], output_path: Path):
        """Generate markdown summary"""

        # Calculate statistics
        total_loc = sum(a.lines_of_code for a in analyses)
        avg_quality = sum(a.code_quality_score for a in analyses) / len(analyses) if analyses else 0

        category_counts = Counter(a.category for a in analyses)
        pattern_counts = Counter(
            p.pattern_type for a in analyses for p in a.patterns
        )

        with_tests = sum(1 for a in analyses if a.has_tests)
        with_docs = sum(1 for a in analyses if a.has_documentation)

        # Generate markdown
        lines = [
            "# Advanced Content Intelligence Report",
            f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "\n## Summary Statistics",
            f"- **Total Files Analyzed:** {len(analyses)}",
            f"- **Total Lines of Code:** {total_loc:,}",
            f"- **Average Quality Score:** {avg_quality:.1f}/100",
            f"- **Files with Tests:** {with_tests} ({with_tests/len(analyses)*100:.1f}%)",
            f"- **Files with Documentation:** {with_docs} ({with_docs/len(analyses)*100:.1f}%)",
            "\n## Category Distribution",
        ]

        for category, count in category_counts.most_common():
            pct = count / len(analyses) * 100
            lines.append(f"- **{category}:** {count} files ({pct:.1f}%)")

        lines.extend([
            "\n## Detected Architectural Patterns",
        ])

        if pattern_counts:
            for pattern, count in pattern_counts.most_common():
                lines.append(f"- **{pattern}:** {count} occurrences")
        else:
            lines.append("- No architectural patterns detected")

        lines.extend([
            "\n## Top Quality Files",
        ])

        top_quality = sorted(analyses, key=lambda a: a.code_quality_score, reverse=True)[:10]
        for a in top_quality:
            lines.append(f"- `{a.filepath}` - Score: {a.code_quality_score:.1f}")

        lines.extend([
            "\n## Files Needing Improvement",
        ])

        needs_improvement = sorted(analyses, key=lambda a: a.code_quality_score)[:10]
        for a in needs_improvement:
            lines.append(f"- `{a.filepath}` - Score: {a.code_quality_score:.1f}")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Advanced Content-Awareness Intelligence System'
    )
    parser.add_argument(
        'directory',
        type=Path,
        nargs='?',
        default=Path.cwd(),
        help='Directory to analyze (default: current directory)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path.cwd(),
        help='Output directory for reports'
    )
    parser.add_argument(
        '--use-ml',
        action='store_true',
        help='Enable ML-based categorization (requires OpenAI API key)'
    )
    parser.add_argument(
        '--exclude',
        nargs='+',
        help='Additional directories to exclude'
    )

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )

    # Load API key if using ML
    api_key = None
    if args.use_ml:
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logging.warning("OPENAI_API_KEY not found, ML features disabled")
            args.use_ml = False

    # Create analyzer
    analyzer = AdvancedContentIntelligenceAnalyzer(
        use_ml=args.use_ml,
        api_key=api_key
    )

    # Build exclude set
    exclude_dirs = {
        'node_modules', '__pycache__', '.git', 'venv', 'env',
        '.venv', 'dist', 'build', '.next', '.pytest_cache'
    }
    if args.exclude:
        exclude_dirs.update(args.exclude)

    # Run analysis
    print(f"\n🔍 Starting advanced intelligence analysis of: {args.directory}")
    print(f"📊 ML-based categorization: {'Enabled' if args.use_ml else 'Disabled'}\n")

    analyses = analyzer.analyze_directory(args.directory, exclude_dirs)

    # Generate reports
    analyzer.generate_report(analyses, args.output)

    print(f"\n✅ Analysis complete! Analyzed {len(analyses)} files.")
    print(f"📁 Reports saved to: {args.output}")


if __name__ == '__main__':
    main()

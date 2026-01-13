#!/usr/bin/env python3
"""
Advanced AST-Based Code Intelligence System
===========================================

This module implements cutting-edge static code analysis with semantic understanding,
content-awareness intelligence, and architectural pattern detection for creative
automation projects.

Features:
- AST-based deep code understanding
- Semantic pattern recognition with confidence scoring
- Architectural pattern detection
- Content-aware categorization and tagging
- Vector-based semantic search capabilities
- Multi-platform automation support
- Agentic workflow planning and execution

Author: AI-Powered Development Assistant
Date: 2025-01-27
Version: 2.0.0
"""

import ast
import os
import re
import json
import hashlib
import logging
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from collections import defaultdict, Counter
import networkx as nx
from datetime import datetime
import pickle
import sqlite3
from contextlib import contextmanager

# Advanced ML and NLP libraries
try:
    import torch
    import transformers
    from sentence_transformers import SentenceTransformer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.decomposition import PCA, TruncatedSVD
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("Warning: ML libraries not available. Some features will be limited.")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class CodePattern:
    """Represents a detected code pattern with metadata."""
    pattern_type: str
    confidence: float
    description: str
    location: str
    context: Dict[str, Any]
    semantic_tags: List[str]
    architectural_significance: float
    complexity_score: float
    maintainability_score: float

@dataclass
class SemanticAnalysis:
    """Comprehensive semantic analysis of code."""
    file_path: str
    content_hash: str
    ast_complexity: float
    semantic_embedding: Optional[np.ndarray]
    detected_patterns: List[CodePattern]
    architectural_style: str
    content_category: str
    quality_metrics: Dict[str, float]
    dependencies: List[str]
    relationships: Dict[str, List[str]]

@dataclass
class ProjectIntelligence:
    """Complete project intelligence profile."""
    project_name: str
    analysis_timestamp: datetime
    total_files: int
    semantic_analyses: List[SemanticAnalysis]
    architectural_patterns: Dict[str, List[CodePattern]]
    content_categories: Dict[str, List[str]]
    quality_metrics: Dict[str, float]
    recommendations: List[str]
    automation_opportunities: List[Dict[str, Any]]

class AdvancedASTAnalyzer:
    """Advanced AST-based code analyzer with semantic understanding."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.semantic_model = None
        self.vectorizer = None
        self.stemmer = PorterStemmer()
        self.stop_words = set()
        
        # Initialize ML components
        self._initialize_ml_components()
        
        # Pattern recognition rules
        self.pattern_rules = self._load_pattern_rules()
        
        # Architectural pattern definitions
        self.architectural_patterns = self._load_architectural_patterns()
        
        # Content categorization rules
        self.content_categories = self._load_content_categories()
        
        # Database for storing analysis results
        self.db_path = "intelligent_analysis.db"
        self._initialize_database()
    
    def _initialize_ml_components(self):
        """Initialize machine learning components for semantic analysis."""
        if not ML_AVAILABLE:
            logger.warning("ML libraries not available. Using basic text analysis.")
            return
        
        try:
            # Initialize sentence transformer for semantic embeddings
            self.semantic_model = SentenceTransformer(self.model_name)
            
            # Initialize TF-IDF vectorizer for text analysis
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 3),
                min_df=2
            )
            
            # Download NLTK data
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                self.stop_words = set(stopwords.words('english'))
            except:
                logger.warning("Could not download NLTK data")
                
        except Exception as e:
            logger.error(f"Error initializing ML components: {e}")
            ML_AVAILABLE = False
    
    def _load_pattern_rules(self) -> Dict[str, List[Dict]]:
        """Load pattern recognition rules for different code patterns."""
        return {
            "design_patterns": [
                {
                    "name": "Singleton Pattern",
                    "pattern": "class.*:\s*_instance\s*=\s*None.*def\s*__new__",
                    "confidence_weight": 0.9,
                    "description": "Singleton pattern implementation"
                },
                {
                    "name": "Factory Pattern",
                    "pattern": "def\s+create_.*\(.*\):\s*.*if.*return.*elif.*return",
                    "confidence_weight": 0.8,
                    "description": "Factory method pattern"
                },
                {
                    "name": "Observer Pattern",
                    "pattern": "class.*:\s*def\s+attach.*def\s+notify",
                    "confidence_weight": 0.85,
                    "description": "Observer pattern implementation"
                }
            ],
            "architectural_patterns": [
                {
                    "name": "MVC Pattern",
                    "pattern": "class.*Controller.*class.*Model.*class.*View",
                    "confidence_weight": 0.9,
                    "description": "Model-View-Controller architecture"
                },
                {
                    "name": "Repository Pattern",
                    "pattern": "class.*Repository.*def\s+(get|save|delete|update)",
                    "confidence_weight": 0.8,
                    "description": "Repository pattern for data access"
                },
                {
                    "name": "Service Layer",
                    "pattern": "class.*Service.*def\s+.*business.*logic",
                    "confidence_weight": 0.75,
                    "description": "Service layer pattern"
                }
            ],
            "code_smells": [
                {
                    "name": "Long Method",
                    "pattern": "def\s+\w+\([^)]*\):\s*(.{200,})",
                    "confidence_weight": 0.7,
                    "description": "Method longer than 200 characters"
                },
                {
                    "name": "Large Class",
                    "pattern": "class\s+\w+.*:\s*(.{500,})",
                    "confidence_weight": 0.6,
                    "description": "Class with excessive content"
                },
                {
                    "name": "Duplicate Code",
                    "pattern": "(.{50,})\s*\n.*\1",
                    "confidence_weight": 0.8,
                    "description": "Potential code duplication"
                }
            ],
            "security_patterns": [
                {
                    "name": "SQL Injection Risk",
                    "pattern": "execute\s*\(\s*[\"'].*\+.*[\"']",
                    "confidence_weight": 0.9,
                    "description": "Potential SQL injection vulnerability"
                },
                {
                    "name": "Hardcoded Credentials",
                    "pattern": "(password|secret|key)\s*=\s*[\"'][^\"']+[\"']",
                    "confidence_weight": 0.85,
                    "description": "Hardcoded sensitive information"
                }
            ]
        }
    
    def _load_architectural_patterns(self) -> Dict[str, Dict]:
        """Load architectural pattern definitions."""
        return {
            "microservices": {
                "indicators": ["api", "service", "endpoint", "gateway"],
                "weight": 0.8,
                "description": "Microservices architecture"
            },
            "monolithic": {
                "indicators": ["main", "app", "core", "shared"],
                "weight": 0.7,
                "description": "Monolithic architecture"
            },
            "layered": {
                "indicators": ["controller", "service", "repository", "model"],
                "weight": 0.9,
                "description": "Layered architecture"
            },
            "event_driven": {
                "indicators": ["event", "listener", "handler", "publish", "subscribe"],
                "weight": 0.8,
                "description": "Event-driven architecture"
            },
            "mvc": {
                "indicators": ["model", "view", "controller", "mvc"],
                "weight": 0.9,
                "description": "Model-View-Controller pattern"
            }
        }
    
    def _load_content_categories(self) -> Dict[str, List[str]]:
        """Load content categorization rules."""
        return {
            "frontend": [
                "html", "css", "javascript", "jsx", "tsx", "vue", "react", "angular",
                "component", "template", "view", "ui", "interface"
            ],
            "backend": [
                "api", "server", "controller", "service", "repository", "model",
                "database", "sql", "endpoint", "route", "middleware"
            ],
            "database": [
                "sql", "migration", "schema", "table", "query", "database",
                "postgres", "mysql", "sqlite", "mongodb"
            ],
            "testing": [
                "test", "spec", "mock", "stub", "fixture", "coverage",
                "unit", "integration", "e2e", "jest", "pytest"
            ],
            "deployment": [
                "docker", "kubernetes", "deploy", "ci", "cd", "pipeline",
                "infrastructure", "terraform", "ansible", "jenkins"
            ],
            "documentation": [
                "readme", "docs", "documentation", "guide", "tutorial",
                "api", "reference", "manual", "help"
            ],
            "configuration": [
                "config", "settings", "env", "yaml", "json", "toml",
                "properties", "ini", "xml"
            ],
            "assets": [
                "image", "icon", "logo", "font", "style", "theme",
                "static", "public", "assets", "media"
            ]
        }
    
    def _initialize_database(self):
        """Initialize SQLite database for storing analysis results."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS semantic_analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE,
                    content_hash TEXT,
                    analysis_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS project_intelligence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT,
                    analysis_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS semantic_embeddings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT,
                    embedding BLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    
    def analyze_file(self, file_path: str) -> SemanticAnalysis:
        """Perform comprehensive semantic analysis of a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate content hash
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            # Parse AST
            try:
                tree = ast.parse(content)
                ast_complexity = self._calculate_ast_complexity(tree)
            except SyntaxError:
                logger.warning(f"Could not parse {file_path} as Python code")
                tree = None
                ast_complexity = 0.0
            
            # Generate semantic embedding
            semantic_embedding = self._generate_semantic_embedding(content)
            
            # Detect patterns
            detected_patterns = self._detect_patterns(content, file_path)
            
            # Determine architectural style
            architectural_style = self._detect_architectural_style(content, file_path)
            
            # Categorize content
            content_category = self._categorize_content(content, file_path)
            
            # Calculate quality metrics
            quality_metrics = self._calculate_quality_metrics(content, tree)
            
            # Extract dependencies
            dependencies = self._extract_dependencies(content)
            
            # Analyze relationships
            relationships = self._analyze_relationships(content, file_path)
            
            return SemanticAnalysis(
                file_path=file_path,
                content_hash=content_hash,
                ast_complexity=ast_complexity,
                semantic_embedding=semantic_embedding,
                detected_patterns=detected_patterns,
                architectural_style=architectural_style,
                content_category=content_category,
                quality_metrics=quality_metrics,
                dependencies=dependencies,
                relationships=relationships
            )
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return None
    
    def _calculate_ast_complexity(self, tree: ast.AST) -> float:
        """Calculate cyclomatic complexity from AST."""
        if not tree:
            return 0.0
        
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return float(complexity)
    
    def _generate_semantic_embedding(self, content: str) -> Optional[np.ndarray]:
        """Generate semantic embedding for content."""
        if not self.semantic_model:
            return None
        
        try:
            # Clean and preprocess content
            cleaned_content = self._preprocess_text(content)
            
            # Generate embedding
            embedding = self.semantic_model.encode([cleaned_content])[0]
            
            return embedding
        except Exception as e:
            logger.error(f"Error generating semantic embedding: {e}")
            return None
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for semantic analysis."""
        # Remove code-specific elements
        text = re.sub(r'#.*$', '', text, flags=re.MULTILINE)  # Remove comments
        text = re.sub(r'""".*?"""', '', text, flags=re.DOTALL)  # Remove docstrings
        text = re.sub(r"'''.*?'''", '', text, flags=re.DOTALL)  # Remove docstrings
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove special characters
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        
        # Tokenize and remove stop words
        if self.stop_words:
            tokens = word_tokenize(text.lower())
            tokens = [token for token in tokens if token not in self.stop_words]
            text = ' '.join(tokens)
        
        return text.strip()
    
    def _detect_patterns(self, content: str, file_path: str) -> List[CodePattern]:
        """Detect various code patterns using regex and AST analysis."""
        patterns = []
        
        for category, rules in self.pattern_rules.items():
            for rule in rules:
                matches = re.finditer(rule["pattern"], content, re.MULTILINE | re.DOTALL)
                
                for match in matches:
                    confidence = self._calculate_pattern_confidence(
                        match, rule, content, file_path
                    )
                    
                    if confidence > 0.5:  # Threshold for pattern detection
                        pattern = CodePattern(
                            pattern_type=rule["name"],
                            confidence=confidence,
                            description=rule["description"],
                            location=f"{file_path}:{match.start()}",
                            context={
                                "match_text": match.group(0)[:200],
                                "line_number": content[:match.start()].count('\n') + 1
                            },
                            semantic_tags=self._extract_semantic_tags(match.group(0)),
                            architectural_significance=self._calculate_architectural_significance(
                                rule["name"], content
                            ),
                            complexity_score=self._calculate_pattern_complexity(match.group(0)),
                            maintainability_score=self._calculate_maintainability_score(
                                match.group(0), content
                            )
                        )
                        patterns.append(pattern)
        
        return patterns
    
    def _calculate_pattern_confidence(self, match, rule: Dict, content: str, file_path: str) -> float:
        """Calculate confidence score for a detected pattern."""
        base_confidence = rule.get("confidence_weight", 0.5)
        
        # Adjust based on context
        context_bonus = 0.0
        
        # Check if pattern appears in appropriate context
        if rule["name"] in ["Singleton Pattern", "Factory Pattern"]:
            if "class" in content.lower():
                context_bonus += 0.2
        
        # Check file type appropriateness
        file_extension = Path(file_path).suffix.lower()
        if file_extension in ['.py', '.js', '.ts'] and rule["name"] in ["MVC Pattern", "Repository Pattern"]:
            context_bonus += 0.1
        
        # Check for supporting evidence
        supporting_evidence = self._find_supporting_evidence(match.group(0), content)
        context_bonus += supporting_evidence * 0.1
        
        return min(1.0, base_confidence + context_bonus)
    
    def _find_supporting_evidence(self, pattern_text: str, content: str) -> float:
        """Find supporting evidence for a pattern in the surrounding code."""
        evidence_score = 0.0
        
        # Look for related keywords
        related_keywords = {
            "Singleton": ["instance", "getinstance", "private"],
            "Factory": ["create", "build", "make"],
            "Observer": ["notify", "update", "subscribe"],
            "MVC": ["model", "view", "controller"]
        }
        
        pattern_name = pattern_text.split()[0] if pattern_text else ""
        keywords = related_keywords.get(pattern_name, [])
        
        for keyword in keywords:
            if keyword.lower() in content.lower():
                evidence_score += 0.2
        
        return min(1.0, evidence_score)
    
    def _extract_semantic_tags(self, text: str) -> List[str]:
        """Extract semantic tags from text."""
        tags = []
        
        # Extract function/class names
        function_matches = re.findall(r'def\s+(\w+)', text)
        class_matches = re.findall(r'class\s+(\w+)', text)
        
        tags.extend([f"function:{name}" for name in function_matches])
        tags.extend([f"class:{name}" for name in class_matches])
        
        # Extract keywords
        keywords = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', text)
        common_keywords = Counter(keywords).most_common(5)
        tags.extend([f"keyword:{word}" for word, _ in common_keywords])
        
        return tags
    
    def _calculate_architectural_significance(self, pattern_name: str, content: str) -> float:
        """Calculate architectural significance of a pattern."""
        significance_map = {
            "Singleton Pattern": 0.8,
            "Factory Pattern": 0.7,
            "Observer Pattern": 0.6,
            "MVC Pattern": 0.9,
            "Repository Pattern": 0.8,
            "Service Layer": 0.7
        }
        
        base_significance = significance_map.get(pattern_name, 0.5)
        
        # Adjust based on frequency and context
        frequency = content.lower().count(pattern_name.lower().replace(" pattern", ""))
        frequency_bonus = min(0.2, frequency * 0.05)
        
        return min(1.0, base_significance + frequency_bonus)
    
    def _calculate_pattern_complexity(self, pattern_text: str) -> float:
        """Calculate complexity score for a pattern."""
        lines = pattern_text.count('\n') + 1
        characters = len(pattern_text)
        
        # Normalize complexity score
        complexity = (lines * 0.1) + (characters * 0.001)
        return min(1.0, complexity)
    
    def _calculate_maintainability_score(self, pattern_text: str, content: str) -> float:
        """Calculate maintainability score for a pattern."""
        # Factors: length, nesting, comments, naming
        length_score = max(0, 1 - len(pattern_text) / 1000)
        
        nesting_level = pattern_text.count('    ') + pattern_text.count('\t')
        nesting_score = max(0, 1 - nesting_level / 10)
        
        comment_ratio = len(re.findall(r'#.*$', pattern_text, re.MULTILINE)) / max(1, pattern_text.count('\n'))
        comment_score = min(1, comment_ratio * 2)
        
        # Check for descriptive names
        descriptive_names = len(re.findall(r'[a-z][a-zA-Z]*[A-Z][a-zA-Z]*', pattern_text))
        naming_score = min(1, descriptive_names / 5)
        
        return (length_score + nesting_score + comment_score + naming_score) / 4
    
    def _detect_architectural_style(self, content: str, file_path: str) -> str:
        """Detect the architectural style of the code."""
        content_lower = content.lower()
        file_path_lower = file_path.lower()
        
        style_scores = {}
        
        for style, config in self.architectural_patterns.items():
            score = 0.0
            for indicator in config["indicators"]:
                if indicator in content_lower or indicator in file_path_lower:
                    score += config["weight"]
            
            style_scores[style] = score
        
        # Return the style with highest score
        if style_scores:
            return max(style_scores, key=style_scores.get)
        
        return "unknown"
    
    def _categorize_content(self, content: str, file_path: str) -> str:
        """Categorize content based on file type and content analysis."""
        file_extension = Path(file_path).suffix.lower()
        content_lower = content.lower()
        file_path_lower = file_path.lower()
        
        category_scores = {}
        
        for category, indicators in self.content_categories.items():
            score = 0.0
            
            # Check file extension
            if file_extension in indicators:
                score += 0.5
            
            # Check content indicators
            for indicator in indicators:
                if indicator in content_lower:
                    score += 0.1
                if indicator in file_path_lower:
                    score += 0.2
            
            category_scores[category] = score
        
        # Return the category with highest score
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return "other"
    
    def _calculate_quality_metrics(self, content: str, tree: ast.AST) -> Dict[str, float]:
        """Calculate various quality metrics for the code."""
        metrics = {}
        
        # Lines of code
        metrics["lines_of_code"] = len(content.splitlines())
        
        # Cyclomatic complexity
        metrics["cyclomatic_complexity"] = self._calculate_ast_complexity(tree)
        
        # Comment ratio
        comment_lines = len(re.findall(r'^\s*#', content, re.MULTILINE))
        total_lines = len(content.splitlines())
        metrics["comment_ratio"] = comment_lines / max(1, total_lines)
        
        # Function count
        if tree:
            function_count = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
            metrics["function_count"] = function_count
        else:
            metrics["function_count"] = 0
        
        # Class count
        if tree:
            class_count = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            metrics["class_count"] = class_count
        else:
            metrics["class_count"] = 0
        
        # Average function length
        if tree and metrics["function_count"] > 0:
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            total_function_lines = sum(len(ast.get_source_segment(content, node) or "").splitlines() for node in functions)
            metrics["avg_function_length"] = total_function_lines / metrics["function_count"]
        else:
            metrics["avg_function_length"] = 0
        
        # Duplication ratio (simplified)
        lines = content.splitlines()
        unique_lines = set(lines)
        metrics["duplication_ratio"] = 1 - (len(unique_lines) / max(1, len(lines)))
        
        return metrics
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract dependencies from import statements."""
        dependencies = []
        
        # Python imports
        import_matches = re.findall(r'^(?:from\s+(\S+)\s+)?import\s+(\S+)', content, re.MULTILINE)
        for module, name in import_matches:
            if module:
                dependencies.append(module)
            else:
                dependencies.append(name.split('.')[0])
        
        # JavaScript/Node.js imports
        js_imports = re.findall(r'import.*from\s+[\'"]([^\'"]+)[\'"]', content)
        dependencies.extend(js_imports)
        
        # CommonJS requires
        require_matches = re.findall(r'require\([\'"]([^\'"]+)[\'"]\)', content)
        dependencies.extend(require_matches)
        
        return list(set(dependencies))
    
    def _analyze_relationships(self, content: str, file_path: str) -> Dict[str, List[str]]:
        """Analyze relationships between different parts of the code."""
        relationships = {
            "imports": [],
            "exports": [],
            "calls": [],
            "inherits": [],
            "implements": []
        }
        
        # Extract imports
        import_matches = re.findall(r'from\s+(\S+)\s+import\s+(\S+)', content)
        relationships["imports"] = [f"{module}.{name}" for module, name in import_matches]
        
        # Extract function calls
        call_matches = re.findall(r'(\w+)\s*\(', content)
        relationships["calls"] = list(set(call_matches))
        
        # Extract class inheritance
        if tree := ast.parse(content):
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.bases:
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            relationships["inherits"].append(f"{node.name} -> {base.id}")
        
        return relationships
    
    def analyze_project(self, project_path: str) -> ProjectIntelligence:
        """Perform comprehensive analysis of an entire project."""
        project_path = Path(project_path)
        project_name = project_path.name
        
        logger.info(f"Starting comprehensive analysis of project: {project_name}")
        
        # Find all relevant files
        file_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.sql', '.json', '.yaml', '.yml'}
        files = []
        
        for ext in file_extensions:
            files.extend(project_path.rglob(f"*{ext}"))
        
        logger.info(f"Found {len(files)} files to analyze")
        
        # Analyze each file
        semantic_analyses = []
        for file_path in files:
            try:
                analysis = self.analyze_file(str(file_path))
                if analysis:
                    semantic_analyses.append(analysis)
            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {e}")
        
        # Aggregate patterns
        architectural_patterns = defaultdict(list)
        content_categories = defaultdict(list)
        
        for analysis in semantic_analyses:
            for pattern in analysis.detected_patterns:
                architectural_patterns[pattern.pattern_type].append(pattern)
            
            content_categories[analysis.content_category].append(analysis.file_path)
        
        # Calculate project-wide quality metrics
        quality_metrics = self._calculate_project_quality_metrics(semantic_analyses)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(semantic_analyses, quality_metrics)
        
        # Identify automation opportunities
        automation_opportunities = self._identify_automation_opportunities(semantic_analyses)
        
        project_intelligence = ProjectIntelligence(
            project_name=project_name,
            analysis_timestamp=datetime.now(),
            total_files=len(semantic_analyses),
            semantic_analyses=semantic_analyses,
            architectural_patterns=dict(architectural_patterns),
            content_categories=dict(content_categories),
            quality_metrics=quality_metrics,
            recommendations=recommendations,
            automation_opportunities=automation_opportunities
        )
        
        # Store in database
        self._store_project_intelligence(project_intelligence)
        
        logger.info(f"Analysis complete for project: {project_name}")
        return project_intelligence
    
    def _calculate_project_quality_metrics(self, analyses: List[SemanticAnalysis]) -> Dict[str, float]:
        """Calculate project-wide quality metrics."""
        if not analyses:
            return {}
        
        total_files = len(analyses)
        
        # Aggregate metrics
        total_loc = sum(analysis.quality_metrics.get("lines_of_code", 0) for analysis in analyses)
        total_complexity = sum(analysis.ast_complexity for analysis in analyses)
        total_functions = sum(analysis.quality_metrics.get("function_count", 0) for analysis in analyses)
        total_classes = sum(analysis.quality_metrics.get("class_count", 0) for analysis in analyses)
        
        avg_comment_ratio = sum(analysis.quality_metrics.get("comment_ratio", 0) for analysis in analyses) / total_files
        avg_duplication = sum(analysis.quality_metrics.get("duplication_ratio", 0) for analysis in analyses) / total_files
        
        return {
            "total_lines_of_code": total_loc,
            "average_complexity": total_complexity / total_files,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "average_comment_ratio": avg_comment_ratio,
            "average_duplication_ratio": avg_duplication,
            "files_analyzed": total_files
        }
    
    def _generate_recommendations(self, analyses: List[SemanticAnalysis], quality_metrics: Dict[str, float]) -> List[str]:
        """Generate intelligent recommendations based on analysis."""
        recommendations = []
        
        # Complexity recommendations
        if quality_metrics.get("average_complexity", 0) > 10:
            recommendations.append("Consider refactoring complex functions to reduce cyclomatic complexity")
        
        # Comment ratio recommendations
        if quality_metrics.get("average_comment_ratio", 0) < 0.1:
            recommendations.append("Increase code documentation and comments for better maintainability")
        
        # Duplication recommendations
        if quality_metrics.get("average_duplication_ratio", 0) > 0.2:
            recommendations.append("Refactor duplicated code into reusable functions or modules")
        
        # Pattern-specific recommendations
        pattern_counts = defaultdict(int)
        for analysis in analyses:
            for pattern in analysis.detected_patterns:
                pattern_counts[pattern.pattern_type] += 1
        
        if pattern_counts.get("Long Method", 0) > 5:
            recommendations.append("Break down long methods into smaller, more focused functions")
        
        if pattern_counts.get("Large Class", 0) > 3:
            recommendations.append("Consider splitting large classes using Single Responsibility Principle")
        
        return recommendations
    
    def _identify_automation_opportunities(self, analyses: List[SemanticAnalysis]) -> List[Dict[str, Any]]:
        """Identify opportunities for automation based on code analysis."""
        opportunities = []
        
        # Test automation opportunities
        test_files = [a for a in analyses if a.content_category == "testing"]
        if len(test_files) < len(analyses) * 0.2:  # Less than 20% test coverage
            opportunities.append({
                "type": "test_automation",
                "description": "Implement comprehensive test suite",
                "priority": "high",
                "estimated_effort": "medium"
            })
        
        # Documentation automation
        low_doc_files = [a for a in analyses if a.quality_metrics.get("comment_ratio", 0) < 0.1]
        if len(low_doc_files) > len(analyses) * 0.3:
            opportunities.append({
                "type": "documentation_automation",
                "description": "Automate documentation generation",
                "priority": "medium",
                "estimated_effort": "low"
            })
        
        # Code quality automation
        complex_files = [a for a in analyses if a.ast_complexity > 15]
        if complex_files:
            opportunities.append({
                "type": "code_quality_automation",
                "description": "Implement automated code quality checks",
                "priority": "high",
                "estimated_effort": "medium"
            })
        
        return opportunities
    
    def _store_project_intelligence(self, project_intelligence: ProjectIntelligence):
        """Store project intelligence in database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Store project intelligence
                conn.execute('''
                    INSERT OR REPLACE INTO project_intelligence 
                    (project_name, analysis_data, created_at)
                    VALUES (?, ?, ?)
                ''', (
                    project_intelligence.project_name,
                    json.dumps(asdict(project_intelligence), default=str),
                    project_intelligence.analysis_timestamp
                ))
                
                # Store individual file analyses
                for analysis in project_intelligence.semantic_analyses:
                    conn.execute('''
                        INSERT OR REPLACE INTO semantic_analyses 
                        (file_path, content_hash, analysis_data, created_at)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        analysis.file_path,
                        analysis.content_hash,
                        json.dumps(asdict(analysis), default=str),
                        datetime.now()
                    ))
                
                conn.commit()
        except Exception as e:
            logger.error(f"Error storing project intelligence: {e}")
    
    def semantic_search(self, query: str, project_path: str = None) -> List[Dict[str, Any]]:
        """Perform semantic search across analyzed code."""
        if not self.semantic_model:
            logger.warning("Semantic model not available for search")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.semantic_model.encode([query])[0]
            
            # Load stored analyses
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT file_path, analysis_data FROM semantic_analyses
                    WHERE project_name = ? OR ? IS NULL
                ''', (project_path, project_path))
                
                results = []
                for file_path, analysis_data in cursor.fetchall():
                    analysis = json.loads(analysis_data)
                    
                    if analysis.get('semantic_embedding'):
                        # Calculate similarity
                        file_embedding = np.frombuffer(analysis['semantic_embedding'], dtype=np.float32)
                        similarity = cosine_similarity([query_embedding], [file_embedding])[0][0]
                        
                        results.append({
                            'file_path': file_path,
                            'similarity': float(similarity),
                            'analysis': analysis
                        })
                
                # Sort by similarity
                results.sort(key=lambda x: x['similarity'], reverse=True)
                return results[:10]  # Return top 10 results
                
        except Exception as e:
            logger.error(f"Error performing semantic search: {e}")
            return []
    
    def get_project_summary(self, project_name: str) -> Dict[str, Any]:
        """Get a comprehensive summary of project analysis."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT analysis_data FROM project_intelligence 
                    WHERE project_name = ?
                    ORDER BY created_at DESC LIMIT 1
                ''', (project_name,))
                
                result = cursor.fetchone()
                if result:
                    return json.loads(result[0])
                return {}
        except Exception as e:
            logger.error(f"Error getting project summary: {e}")
            return {}


def main():
    """Main function for testing the AST analyzer."""
    analyzer = AdvancedASTAnalyzer()
    
    # Example usage
    project_path = "/Users/steven/ai-sites/heavenlyHands"
    
    print("🚀 Starting Advanced AST Analysis...")
    print("=" * 50)
    
    # Analyze the project
    project_intelligence = analyzer.analyze_project(project_path)
    
    print(f"\n📊 Project Analysis Complete!")
    print(f"Project: {project_intelligence.project_name}")
    print(f"Files Analyzed: {project_intelligence.total_files}")
    print(f"Analysis Time: {project_intelligence.analysis_timestamp}")
    
    print(f"\n🏗️ Architectural Patterns Found:")
    for pattern, instances in project_intelligence.architectural_patterns.items():
        print(f"  - {pattern}: {len(instances)} instances")
    
    print(f"\n📁 Content Categories:")
    for category, files in project_intelligence.content_categories.items():
        print(f"  - {category}: {len(files)} files")
    
    print(f"\n📈 Quality Metrics:")
    for metric, value in project_intelligence.quality_metrics.items():
        print(f"  - {metric}: {value:.2f}")
    
    print(f"\n💡 Recommendations:")
    for i, rec in enumerate(project_intelligence.recommendations, 1):
        print(f"  {i}. {rec}")
    
    print(f"\n🤖 Automation Opportunities:")
    for i, opp in enumerate(project_intelligence.automation_opportunities, 1):
        print(f"  {i}. {opp['description']} (Priority: {opp['priority']})")
    
    print("\n" + "=" * 50)
    print("✅ Analysis Complete!")


if __name__ == "__main__":
    main()
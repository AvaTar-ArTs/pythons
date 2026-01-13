#!/usr/bin/env python3
"""
Advanced Code Intelligence System for AI Voice Agents
Implements AST-based deep code understanding, semantic pattern recognition,
and intelligent content categorization with confidence scoring.
"""

import ast
import os
import sys
import json
import hashlib
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import re
import pickle
from collections import defaultdict, Counter

# Advanced libraries for semantic analysis
try:
    import spacy
    from spacy import displacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

@dataclass
class CodePattern:
    """Represents a detected code pattern with metadata"""
    pattern_type: str
    confidence: float
    location: str
    description: str
    complexity_score: float
    dependencies: List[str]
    semantic_tags: List[str]

@dataclass
class CodeIntelligence:
    """Comprehensive code intelligence analysis"""
    file_path: str
    ast_complexity: float
    semantic_patterns: List[CodePattern]
    architectural_patterns: List[str]
    confidence_score: float
    content_category: str
    intelligence_level: str
    recommendations: List[str]
    timestamp: datetime

class ASTAnalyzer:
    """Advanced AST-based code analysis with semantic understanding"""

    def __init__(self):
        self.pattern_detectors = {
            'voice_agent_patterns': self._detect_voice_agent_patterns,
            'api_integration_patterns': self._detect_api_patterns,
            'data_processing_patterns': self._detect_data_patterns,
            'business_logic_patterns': self._detect_business_logic_patterns,
            'error_handling_patterns': self._detect_error_patterns
        }

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Perform comprehensive AST analysis on a Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            analysis = {
                'file_path': file_path,
                'ast_complexity': self._calculate_complexity(tree),
                'patterns': self._detect_patterns(tree, content),
                'functions': self._extract_functions(tree),
                'classes': self._extract_classes(tree),
                'imports': self._extract_imports(tree),
                'semantic_features': self._extract_semantic_features(tree, content),
                'confidence_score': 0.0
            }

            # Calculate overall confidence
            analysis['confidence_score'] = self._calculate_confidence(analysis)

            return analysis

        except Exception as e:
            return {
                'file_path': file_path,
                'error': str(e),
                'confidence_score': 0.0
            }

    def _calculate_complexity(self, tree: ast.AST) -> float:
        """Calculate cyclomatic complexity and cognitive complexity"""
        complexity = 0

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1

        # Add nesting penalty
        max_depth = self._get_max_depth(tree)
        complexity += max_depth * 0.5

        return complexity

    def _get_max_depth(self, tree: ast.AST, current_depth: int = 0) -> int:
        """Calculate maximum nesting depth"""
        max_depth = current_depth

        for child in ast.iter_child_nodes(tree):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.Try)):
                depth = self._get_max_depth(child, current_depth + 1)
                max_depth = max(max_depth, depth)
            else:
                depth = self._get_max_depth(child, current_depth)
                max_depth = max(max_depth, depth)

        return max_depth

    def _detect_patterns(self, tree: ast.AST, content: str) -> List[CodePattern]:
        """Detect various code patterns using AST analysis"""
        patterns = []

        for pattern_name, detector in self.pattern_detectors.items():
            detected = detector(tree, content)
            patterns.extend(detected)

        return patterns

    def _detect_voice_agent_patterns(self, tree: ast.AST, content: str) -> List[CodePattern]:
        """Detect voice agent specific patterns"""
        patterns = []

        # Look for OpenAI API usage
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if 'openai' in str(node.func.value).lower() or 'client' in str(node.func.value).lower():
                        patterns.append(CodePattern(
                            pattern_type='openai_integration',
                            confidence=0.9,
                            location=f"Line {node.lineno}",
                            description="OpenAI API integration detected",
                            complexity_score=0.7,
                            dependencies=['openai'],
                            semantic_tags=['ai', 'voice', 'api']
                        ))

        # Look for voice/speech related functions
        voice_keywords = ['speech', 'voice', 'audio', 'tts', 'stt', 'whisper', 'transcription']
        for keyword in voice_keywords:
            if keyword.lower() in content.lower():
                patterns.append(CodePattern(
                    pattern_type='voice_functionality',
                    confidence=0.8,
                    location="Multiple locations",
                    description=f"Voice/speech functionality detected: {keyword}",
                    complexity_score=0.6,
                    dependencies=['openai', 'requests'],
                    semantic_tags=['voice', 'speech', 'audio']
                ))

        return patterns

    def _detect_api_patterns(self, tree: ast.AST, content: str) -> List[CodePattern]:
        """Detect API integration patterns"""
        patterns = []

        # Look for HTTP requests
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ['get', 'post', 'put', 'delete', 'patch']:
                        patterns.append(CodePattern(
                            pattern_type='http_api',
                            confidence=0.85,
                            location=f"Line {node.lineno}",
                            description=f"HTTP {node.func.attr.upper()} request detected",
                            complexity_score=0.5,
                            dependencies=['requests'],
                            semantic_tags=['api', 'http', 'rest']
                        ))

        return patterns

    def _detect_data_patterns(self, tree: ast.AST, content: str) -> List[CodePattern]:
        """Detect data processing patterns"""
        patterns = []

        # Look for CSV/JSON processing
        data_keywords = ['csv', 'json', 'pandas', 'dataframe', 'load', 'save']
        for keyword in data_keywords:
            if keyword.lower() in content.lower():
                patterns.append(CodePattern(
                    pattern_type='data_processing',
                    confidence=0.7,
                    location="Multiple locations",
                    description=f"Data processing detected: {keyword}",
                    complexity_score=0.4,
                    dependencies=['pandas', 'json', 'csv'],
                    semantic_tags=['data', 'processing', keyword]
                ))

        return patterns

    def _detect_business_logic_patterns(self, tree: ast.AST, content: str) -> List[CodePattern]:
        """Detect business logic patterns"""
        patterns = []

        # Look for business-related functions
        business_keywords = ['lead', 'customer', 'appointment', 'booking', 'revenue', 'pricing']
        for keyword in business_keywords:
            if keyword.lower() in content.lower():
                patterns.append(CodePattern(
                    pattern_type='business_logic',
                    confidence=0.8,
                    location="Multiple locations",
                    description=f"Business logic detected: {keyword}",
                    complexity_score=0.6,
                    dependencies=[],
                    semantic_tags=['business', 'logic', keyword]
                ))

        return patterns

    def _detect_error_patterns(self, tree: ast.AST, content: str) -> List[CodePattern]:
        """Detect error handling patterns"""
        patterns = []

        # Look for try/except blocks
        try_except_count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                try_except_count += 1

        if try_except_count > 0:
            patterns.append(CodePattern(
                pattern_type='error_handling',
                confidence=0.9,
                location="Multiple locations",
                description=f"Error handling detected ({try_except_count} try/except blocks)",
                complexity_score=0.3,
                dependencies=[],
                semantic_tags=['error', 'handling', 'robustness']
            ))

        return patterns

    def _extract_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract function information from AST"""
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'line_number': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'docstring': ast.get_docstring(node),
                    'complexity': self._calculate_function_complexity(node)
                }
                functions.append(func_info)

        return functions

    def _extract_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract class information from AST"""
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'line_number': node.lineno,
                    'bases': [base.id if isinstance(base, ast.Name) else str(base) for base in node.bases],
                    'docstring': ast.get_docstring(node),
                    'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                }
                classes.append(class_info)

        return classes

    def _extract_imports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract import information from AST"""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        'module': alias.name,
                        'alias': alias.asname,
                        'type': 'import'
                    })
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append({
                        'module': node.module,
                        'name': alias.name,
                        'alias': alias.asname,
                        'type': 'from_import'
                    })

        return imports

    def _extract_semantic_features(self, tree: ast.AST, content: str) -> Dict[str, Any]:
        """Extract semantic features from code"""
        features = {
            'code_length': len(content),
            'line_count': len(content.splitlines()),
            'comment_ratio': self._calculate_comment_ratio(content),
            'naming_conventions': self._analyze_naming_conventions(tree),
            'complexity_indicators': self._get_complexity_indicators(tree)
        }

        return features

    def _calculate_comment_ratio(self, content: str) -> float:
        """Calculate ratio of comments to code"""
        lines = content.splitlines()
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        return comment_lines / len(lines) if lines else 0

    def _analyze_naming_conventions(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze naming conventions used in the code"""
        conventions = {
            'snake_case': 0,
            'camelCase': 0,
            'PascalCase': 0,
            'UPPER_CASE': 0
        }

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Name)):
                name = node.name
                if '_' in name and name.islower():
                    conventions['snake_case'] += 1
                elif name[0].isupper() and '_' not in name:
                    conventions['PascalCase'] += 1
                elif name.isupper() and '_' in name:
                    conventions['UPPER_CASE'] += 1
                elif name[0].islower() and any(c.isupper() for c in name[1:]):
                    conventions['camelCase'] += 1

        return conventions

    def _get_complexity_indicators(self, tree: ast.AST) -> Dict[str, int]:
        """Get indicators of code complexity"""
        indicators = {
            'nested_loops': 0,
            'deep_nesting': 0,
            'long_functions': 0,
            'many_parameters': 0
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                # Check for nested loops
                for child in ast.walk(node):
                    if isinstance(child, ast.For) and child != node:
                        indicators['nested_loops'] += 1

            if isinstance(node, ast.FunctionDef):
                # Check for long functions
                if len(node.body) > 20:
                    indicators['long_functions'] += 1

                # Check for many parameters
                if len(node.args.args) > 5:
                    indicators['many_parameters'] += 1

        return indicators

    def _calculate_function_complexity(self, node: ast.FunctionDef) -> float:
        """Calculate complexity of a specific function"""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _calculate_confidence(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall confidence score for the analysis"""
        confidence_factors = []

        # Pattern detection confidence
        if 'patterns' in analysis:
            pattern_confidences = [p.confidence for p in analysis['patterns']]
            if pattern_confidences:
                confidence_factors.append(np.mean(pattern_confidences))

        # Code quality indicators
        if 'semantic_features' in analysis:
            features = analysis['semantic_features']

            # Comment ratio (good documentation)
            comment_ratio = features.get('comment_ratio', 0)
            if 0.1 <= comment_ratio <= 0.3:  # Sweet spot for comments
                confidence_factors.append(0.9)
            else:
                confidence_factors.append(0.7)

            # Code length (not too short, not too long)
            code_length = features.get('code_length', 0)
            if 100 <= code_length <= 2000:  # Reasonable length
                confidence_factors.append(0.8)
            else:
                confidence_factors.append(0.6)

        # Complexity score
        complexity = analysis.get('ast_complexity', 0)
        if complexity <= 10:  # Low complexity is good
            confidence_factors.append(0.9)
        elif complexity <= 20:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.5)

        return np.mean(confidence_factors) if confidence_factors else 0.5

class SemanticAnalyzer:
    """Advanced semantic analysis using NLP and machine learning"""

    def __init__(self):
        self.nlp = None
        self.vectorizer = None
        self.semantic_patterns = {}

        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")

        if SKLEARN_AVAILABLE:
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )

    def analyze_semantic_patterns(self, code_content: str, comments: str = "") -> Dict[str, Any]:
        """Analyze semantic patterns in code and comments"""
        analysis = {
            'semantic_tags': [],
            'intent_classification': {},
            'complexity_indicators': {},
            'domain_specific_patterns': {},
            'confidence_score': 0.0
        }

        # Extract semantic tags
        analysis['semantic_tags'] = self._extract_semantic_tags(code_content, comments)

        # Classify intent
        analysis['intent_classification'] = self._classify_intent(code_content, comments)

        # Analyze complexity indicators
        analysis['complexity_indicators'] = self._analyze_complexity_indicators(code_content)

        # Detect domain-specific patterns
        analysis['domain_specific_patterns'] = self._detect_domain_patterns(code_content)

        # Calculate confidence
        analysis['confidence_score'] = self._calculate_semantic_confidence(analysis)

        return analysis

    def _extract_semantic_tags(self, code_content: str, comments: str) -> List[str]:
        """Extract semantic tags from code and comments"""
        tags = []

        # Voice agent specific tags
        voice_keywords = {
            'ai': ['openai', 'gpt', 'whisper', 'tts', 'stt', 'ai', 'artificial intelligence'],
            'voice': ['voice', 'speech', 'audio', 'sound', 'speak', 'listen'],
            'communication': ['phone', 'call', 'message', 'chat', 'conversation'],
            'business': ['lead', 'customer', 'client', 'appointment', 'booking', 'revenue'],
            'api': ['api', 'request', 'response', 'http', 'rest', 'endpoint'],
            'data': ['csv', 'json', 'database', 'storage', 'file', 'process']
        }

        combined_text = f"{code_content} {comments}".lower()

        for category, keywords in voice_keywords.items():
            for keyword in keywords:
                if keyword in combined_text:
                    tags.append(category)
                    break

        return list(set(tags))  # Remove duplicates

    def _classify_intent(self, code_content: str, comments: str) -> Dict[str, float]:
        """Classify the intent/purpose of the code"""
        intents = {
            'voice_agent': 0.0,
            'data_processing': 0.0,
            'api_integration': 0.0,
            'business_logic': 0.0,
            'utility': 0.0
        }

        combined_text = f"{code_content} {comments}".lower()

        # Voice agent indicators
        voice_indicators = ['openai', 'voice', 'speech', 'tts', 'stt', 'whisper', 'chat', 'conversation']
        voice_score = sum(1 for indicator in voice_indicators if indicator in combined_text)
        intents['voice_agent'] = min(voice_score / len(voice_indicators), 1.0)

        # Data processing indicators
        data_indicators = ['csv', 'json', 'pandas', 'dataframe', 'process', 'transform', 'filter']
        data_score = sum(1 for indicator in data_indicators if indicator in combined_text)
        intents['data_processing'] = min(data_score / len(data_indicators), 1.0)

        # API integration indicators
        api_indicators = ['requests', 'http', 'api', 'get', 'post', 'put', 'delete', 'endpoint']
        api_score = sum(1 for indicator in api_indicators if indicator in combined_text)
        intents['api_integration'] = min(api_score / len(api_indicators), 1.0)

        # Business logic indicators
        business_indicators = ['lead', 'customer', 'appointment', 'booking', 'revenue', 'pricing', 'scoring']
        business_score = sum(1 for indicator in business_indicators if indicator in combined_text)
        intents['business_logic'] = min(business_score / len(business_indicators), 1.0)

        return intents

    def _analyze_complexity_indicators(self, code_content: str) -> Dict[str, Any]:
        """Analyze complexity indicators using semantic analysis"""
        indicators = {
            'cognitive_load': 0.0,
            'maintainability': 0.0,
            'readability': 0.0,
            'testability': 0.0
        }

        # Cognitive load indicators
        complex_patterns = ['nested', 'recursive', 'callback', 'async', 'thread', 'multiprocess']
        cognitive_score = sum(1 for pattern in complex_patterns if pattern in code_content.lower())
        indicators['cognitive_load'] = min(cognitive_score / len(complex_patterns), 1.0)

        # Maintainability indicators
        maintainable_patterns = ['function', 'class', 'module', 'test', 'docstring', 'comment']
        maintainable_score = sum(1 for pattern in maintainable_patterns if pattern in code_content.lower())
        indicators['maintainability'] = min(maintainable_score / len(maintainable_patterns), 1.0)

        # Readability indicators
        readable_patterns = ['clear', 'simple', 'readable', 'documented', 'explained']
        readable_score = sum(1 for pattern in readable_patterns if pattern in code_content.lower())
        indicators['readability'] = min(readable_score / len(readable_patterns), 1.0)

        # Testability indicators
        testable_patterns = ['test', 'mock', 'assert', 'verify', 'validate']
        testable_score = sum(1 for pattern in testable_patterns if pattern in code_content.lower())
        indicators['testability'] = min(testable_score / len(testable_patterns), 1.0)

        return indicators

    def _detect_domain_patterns(self, code_content: str) -> Dict[str, Any]:
        """Detect domain-specific patterns"""
        patterns = {
            'voice_agent_architecture': False,
            'lead_generation_system': False,
            'api_integration_layer': False,
            'data_pipeline': False,
            'business_intelligence': False
        }

        content_lower = code_content.lower()

        # Voice agent architecture
        if any(keyword in content_lower for keyword in ['openai', 'voice', 'speech', 'conversation']):
            patterns['voice_agent_architecture'] = True

        # Lead generation system
        if any(keyword in content_lower for keyword in ['lead', 'google maps', 'business', 'contact']):
            patterns['lead_generation_system'] = True

        # API integration layer
        if any(keyword in content_lower for keyword in ['requests', 'api', 'http', 'endpoint']):
            patterns['api_integration_layer'] = True

        # Data pipeline
        if any(keyword in content_lower for keyword in ['csv', 'json', 'process', 'transform']):
            patterns['data_pipeline'] = True

        # Business intelligence
        if any(keyword in content_lower for keyword in ['revenue', 'scoring', 'analytics', 'metrics']):
            patterns['business_intelligence'] = True

        return patterns

    def _calculate_semantic_confidence(self, analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for semantic analysis"""
        confidence_factors = []

        # Tag diversity (more diverse tags = higher confidence)
        tags = analysis.get('semantic_tags', [])
        if len(tags) >= 3:
            confidence_factors.append(0.9)
        elif len(tags) >= 2:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.5)

        # Intent classification clarity
        intents = analysis.get('intent_classification', {})
        if intents:
            max_intent = max(intents.values())
            if max_intent >= 0.7:  # Clear intent
                confidence_factors.append(0.9)
            elif max_intent >= 0.5:
                confidence_factors.append(0.7)
            else:
                confidence_factors.append(0.5)

        # Domain pattern detection
        patterns = analysis.get('domain_specific_patterns', {})
        detected_patterns = sum(1 for detected in patterns.values() if detected)
        if detected_patterns >= 2:
            confidence_factors.append(0.8)
        elif detected_patterns >= 1:
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.4)

        return np.mean(confidence_factors) if confidence_factors else 0.5

class IntelligentCategorizer:
    """AI-powered code categorization and intelligent organization"""

    def __init__(self):
        self.categories = {
            'voice_agents': {
                'keywords': ['voice', 'speech', 'openai', 'tts', 'stt', 'whisper', 'conversation'],
                'patterns': ['VoiceAgent', 'chat', 'audio', 'speak', 'listen'],
                'priority': 'high'
            },
            'lead_generation': {
                'keywords': ['lead', 'google maps', 'business', 'contact', 'prospect'],
                'patterns': ['search_google_maps', 'generate_leads', 'score_lead'],
                'priority': 'high'
            },
            'data_processing': {
                'keywords': ['csv', 'json', 'pandas', 'dataframe', 'process', 'transform'],
                'patterns': ['export_leads', 'import_data', 'process_file'],
                'priority': 'medium'
            },
            'api_integration': {
                'keywords': ['requests', 'api', 'http', 'rest', 'endpoint', 'client'],
                'patterns': ['get', 'post', 'put', 'delete', 'api_call'],
                'priority': 'medium'
            },
            'business_logic': {
                'keywords': ['revenue', 'pricing', 'scoring', 'analytics', 'metrics'],
                'patterns': ['calculate', 'score', 'analyze', 'evaluate'],
                'priority': 'high'
            },
            'utilities': {
                'keywords': ['helper', 'util', 'common', 'shared', 'base'],
                'patterns': ['helper', 'util', 'common', 'base'],
                'priority': 'low'
            }
        }

        self.intelligence_levels = {
            'beginner': {'complexity_range': (0, 5), 'confidence_range': (0.3, 0.6)},
            'intermediate': {'complexity_range': (5, 15), 'confidence_range': (0.6, 0.8)},
            'advanced': {'complexity_range': (15, 30), 'confidence_range': (0.8, 0.95)},
            'expert': {'complexity_range': (30, float('inf')), 'confidence_range': (0.95, 1.0)}
        }

    def categorize_code(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Categorize code based on analysis results"""
        categorization = {
            'primary_category': 'unknown',
            'secondary_categories': [],
            'intelligence_level': 'beginner',
            'confidence_score': 0.0,
            'recommendations': [],
            'tags': []
        }

        # Extract content for analysis
        content = analysis.get('file_path', '')
        patterns = analysis.get('patterns', [])
        semantic_features = analysis.get('semantic_features', {})

        # Determine primary category
        category_scores = self._calculate_category_scores(content, patterns, semantic_features)
        if category_scores:
            categorization['primary_category'] = max(category_scores, key=category_scores.get)
            categorization['secondary_categories'] = sorted(
                category_scores.keys(),
                key=lambda x: category_scores[x],
                reverse=True
            )[1:3]  # Top 2 secondary categories

        # Determine intelligence level
        complexity = analysis.get('ast_complexity', 0)
        confidence = analysis.get('confidence_score', 0)
        categorization['intelligence_level'] = self._determine_intelligence_level(complexity, confidence)

        # Generate recommendations
        categorization['recommendations'] = self._generate_recommendations(analysis, categorization)

        # Generate tags
        categorization['tags'] = self._generate_tags(analysis, categorization)

        # Calculate overall confidence
        categorization['confidence_score'] = self._calculate_categorization_confidence(categorization)

        return categorization

    def _calculate_category_scores(self, content: str, patterns: List[CodePattern], semantic_features: Dict[str, Any]) -> Dict[str, float]:
        """Calculate scores for each category"""
        scores = {}

        content_lower = content.lower()

        for category, config in self.categories.items():
            score = 0.0

            # Keyword matching
            keyword_matches = sum(1 for keyword in config['keywords'] if keyword in content_lower)
            if config['keywords']:
                score += (keyword_matches / len(config['keywords'])) * 0.4

            # Pattern matching
            pattern_matches = sum(1 for pattern in config['patterns'] if pattern.lower() in content_lower)
            if config['patterns']:
                score += (pattern_matches / len(config['patterns'])) * 0.4

            # Pattern detection from AST analysis
            pattern_type_matches = sum(1 for p in patterns if category.replace('_', '') in p.pattern_type.lower())
            if patterns:
                score += (pattern_type_matches / len(patterns)) * 0.2

            # Priority weighting
            if config['priority'] == 'high':
                score *= 1.2
            elif config['priority'] == 'low':
                score *= 0.8

            scores[category] = score

        return scores

    def _determine_intelligence_level(self, complexity: float, confidence: float) -> str:
        """Determine intelligence level based on complexity and confidence"""
        for level, ranges in self.intelligence_levels.items():
            complexity_min, complexity_max = ranges['complexity_range']
            confidence_min, confidence_max = ranges['confidence_range']

            if (complexity_min <= complexity < complexity_max and
                confidence_min <= confidence <= confidence_max):
                return level

        return 'intermediate'  # Default fallback

    def _generate_recommendations(self, analysis: Dict[str, Any], categorization: Dict[str, Any]) -> List[str]:
        """Generate intelligent recommendations based on analysis"""
        recommendations = []

        complexity = analysis.get('ast_complexity', 0)
        confidence = analysis.get('confidence_score', 0)
        primary_category = categorization.get('primary_category', 'unknown')

        # Complexity-based recommendations
        if complexity > 20:
            recommendations.append("Consider breaking down complex functions into smaller, more manageable pieces")
            recommendations.append("Add comprehensive error handling for better robustness")

        if complexity < 5:
            recommendations.append("Code is well-structured with low complexity - good for maintainability")

        # Confidence-based recommendations
        if confidence < 0.6:
            recommendations.append("Add more documentation and comments to improve code clarity")
            recommendations.append("Consider adding type hints for better code understanding")

        # Category-specific recommendations
        if primary_category == 'voice_agents':
            recommendations.append("Consider implementing conversation state management")
            recommendations.append("Add voice quality metrics and monitoring")

        elif primary_category == 'lead_generation':
            recommendations.append("Implement lead scoring algorithms for better prioritization")
            recommendations.append("Add CRM integration capabilities")

        elif primary_category == 'data_processing':
            recommendations.append("Add data validation and error handling")
            recommendations.append("Consider implementing data caching for performance")

        # Intelligence level recommendations
        intelligence_level = categorization.get('intelligence_level', 'beginner')
        if intelligence_level == 'beginner':
            recommendations.append("Great foundation! Consider adding more advanced features")
        elif intelligence_level == 'expert':
            recommendations.append("Excellent code quality! Consider creating reusable components")

        return recommendations

    def _generate_tags(self, analysis: Dict[str, Any], categorization: Dict[str, Any]) -> List[str]:
        """Generate intelligent tags for the code"""
        tags = []

        # Category-based tags
        primary_category = categorization.get('primary_category', 'unknown')
        tags.append(primary_category)

        secondary_categories = categorization.get('secondary_categories', [])
        tags.extend(secondary_categories)

        # Intelligence level tag
        intelligence_level = categorization.get('intelligence_level', 'beginner')
        tags.append(f"intelligence_{intelligence_level}")

        # Pattern-based tags
        patterns = analysis.get('patterns', [])
        for pattern in patterns:
            tags.extend(pattern.semantic_tags)

        # Complexity-based tags
        complexity = analysis.get('ast_complexity', 0)
        if complexity > 15:
            tags.append('high_complexity')
        elif complexity < 5:
            tags.append('low_complexity')
        else:
            tags.append('medium_complexity')

        # Confidence-based tags
        confidence = analysis.get('confidence_score', 0)
        if confidence > 0.8:
            tags.append('high_confidence')
        elif confidence < 0.5:
            tags.append('low_confidence')
        else:
            tags.append('medium_confidence')

        return list(set(tags))  # Remove duplicates

class CodeIntelligenceEngine:
    """Main engine that orchestrates all intelligence components"""

    def __init__(self):
        self.ast_analyzer = ASTAnalyzer()
        self.semantic_analyzer = SemanticAnalyzer()
        self.categorizer = IntelligentCategorizer()
        self.cache = {}

    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """Perform comprehensive analysis of an entire project"""
        project_path = Path(project_path)

        if not project_path.exists():
            return {'error': f'Project path {project_path} does not exist'}

        analysis_results = {
            'project_path': str(project_path),
            'files_analyzed': [],
            'overall_intelligence': {},
            'architectural_patterns': [],
            'recommendations': [],
            'timestamp': datetime.now().isoformat()
        }

        # Find all Python files
        python_files = list(project_path.rglob('*.py'))

        if not python_files:
            return {'error': 'No Python files found in project'}

        file_analyses = []

        for py_file in python_files:
            print(f"Analyzing {py_file.name}...")

            # Check cache first
            file_hash = self._get_file_hash(py_file)
            if file_hash in self.cache:
                file_analysis = self.cache[file_hash]
            else:
                file_analysis = self._analyze_single_file(py_file)
                self.cache[file_hash] = file_analysis

            file_analyses.append(file_analysis)
            analysis_results['files_analyzed'].append({
                'file': str(py_file),
                'category': file_analysis.get('categorization', {}).get('primary_category', 'unknown'),
                'intelligence_level': file_analysis.get('categorization', {}).get('intelligence_level', 'beginner'),
                'confidence': file_analysis.get('categorization', {}).get('confidence_score', 0.0)
            })

        # Generate overall project intelligence
        analysis_results['overall_intelligence'] = self._generate_overall_intelligence(file_analyses)

        # Detect architectural patterns
        analysis_results['architectural_patterns'] = self._detect_architectural_patterns(file_analyses)

        # Generate project-level recommendations
        analysis_results['recommendations'] = self._generate_project_recommendations(file_analyses)

        return analysis_results

    def _analyze_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python file comprehensively"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # AST Analysis
            ast_analysis = self.ast_analyzer.analyze_file(str(file_path))

            # Semantic Analysis
            semantic_analysis = self.semantic_analyzer.analyze_semantic_patterns(content)

            # Categorization
            categorization = self.categorizer.categorize_code(ast_analysis)

            # Combine all analyses
            comprehensive_analysis = {
                'file_path': str(file_path),
                'ast_analysis': ast_analysis,
                'semantic_analysis': semantic_analysis,
                'categorization': categorization,
                'timestamp': datetime.now().isoformat()
            }

            return comprehensive_analysis

        except Exception as e:
            return {
                'file_path': str(file_path),
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _get_file_hash(self, file_path: Path) -> str:
        """Generate hash for file caching"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return str(file_path)

    def _generate_overall_intelligence(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate overall project intelligence metrics"""
        if not file_analyses:
            return {}

        # Calculate aggregate metrics
        total_complexity = sum(
            analysis.get('ast_analysis', {}).get('ast_complexity', 0)
            for analysis in file_analyses
        )

        avg_confidence = np.mean([
            analysis.get('categorization', {}).get('confidence_score', 0)
            for analysis in file_analyses
        ])

        # Category distribution
        categories = [
            analysis.get('categorization', {}).get('primary_category', 'unknown')
            for analysis in file_analyses
        ]
        category_distribution = Counter(categories)

        # Intelligence level distribution
        intelligence_levels = [
            analysis.get('categorization', {}).get('intelligence_level', 'beginner')
            for analysis in file_analyses
        ]
        intelligence_distribution = Counter(intelligence_levels)

        return {
            'total_files': len(file_analyses),
            'total_complexity': total_complexity,
            'average_complexity': total_complexity / len(file_analyses),
            'average_confidence': avg_confidence,
            'category_distribution': dict(category_distribution),
            'intelligence_distribution': dict(intelligence_distribution),
            'project_maturity': self._assess_project_maturity(file_analyses)
        }

    def _detect_architectural_patterns(self, file_analyses: List[Dict[str, Any]]) -> List[str]:
        """Detect architectural patterns across the project"""
        patterns = []

        # Check for common architectural patterns
        categories = [
            analysis.get('categorization', {}).get('primary_category', 'unknown')
            for analysis in file_analyses
        ]

        # MVC Pattern
        if 'voice_agents' in categories and 'data_processing' in categories:
            patterns.append('MVC-like separation of concerns')

        # Microservices Pattern
        if len(set(categories)) >= 3:
            patterns.append('Microservices architecture')

        # Layered Architecture
        if all(cat in ['voice_agents', 'api_integration', 'data_processing'] for cat in categories):
            patterns.append('Layered architecture')

        # Domain-Driven Design
        if 'business_logic' in categories and len(categories) >= 2:
            patterns.append('Domain-driven design elements')

        return patterns

    def _generate_project_recommendations(self, file_analyses: List[Dict[str, Any]]) -> List[str]:
        """Generate project-level recommendations"""
        recommendations = []

        # Analyze overall project health
        avg_confidence = np.mean([
            analysis.get('categorization', {}).get('confidence_score', 0)
            for analysis in file_analyses
        ])

        if avg_confidence < 0.6:
            recommendations.append("Overall project confidence is low - consider improving documentation and code clarity")

        # Check for architectural improvements
        categories = [
            analysis.get('categorization', {}).get('primary_category', 'unknown')
            for analysis in file_analyses
        ]

        if 'voice_agents' in categories and 'lead_generation' in categories:
            recommendations.append("Consider implementing a unified business logic layer")

        if 'data_processing' in categories:
            recommendations.append("Add data validation and error handling across data processing components")

        # Check for testing
        test_files = [f for f in file_analyses if 'test' in f.get('file_path', '').lower()]
        if not test_files:
            recommendations.append("Consider adding comprehensive test coverage")

        return recommendations

    def _assess_project_maturity(self, file_analyses: List[Dict[str, Any]]) -> str:
        """Assess overall project maturity level"""
        if not file_analyses:
            return 'unknown'

        # Calculate maturity indicators
        avg_confidence = np.mean([
            analysis.get('categorization', {}).get('confidence_score', 0)
            for analysis in file_analyses
        ])

        intelligence_levels = [
            analysis.get('categorization', {}).get('intelligence_level', 'beginner')
            for analysis in file_analyses
        ]

        advanced_count = sum(1 for level in intelligence_levels if level in ['advanced', 'expert'])
        advanced_ratio = advanced_count / len(intelligence_levels)

        if avg_confidence >= 0.8 and advanced_ratio >= 0.5:
            return 'mature'
        elif avg_confidence >= 0.6 and advanced_ratio >= 0.3:
            return 'developing'
        else:
            return 'early_stage'

def main():
    """Main function to demonstrate the Code Intelligence Engine"""
    print("🧠 Advanced Code Intelligence Engine for AI Voice Agents")
    print("=" * 60)

    # Initialize the engine
    engine = CodeIntelligenceEngine()

    # Analyze the current project
    project_path = Path(__file__).parent
    print(f"Analyzing project: {project_path}")

    results = engine.analyze_project(project_path)

    if 'error' in results:
        print(f"❌ Error: {results['error']}")
        return

    # Display results
    print(f"\n📊 Analysis Results:")
    print(f"Files analyzed: {len(results['files_analyzed'])}")

    if results['overall_intelligence']:
        intelligence = results['overall_intelligence']
        print(f"Average complexity: {intelligence.get('average_complexity', 0):.2f}")
        print(f"Average confidence: {intelligence.get('average_confidence', 0):.2f}")
        print(f"Project maturity: {intelligence.get('project_maturity', 'unknown')}")

        print(f"\n📈 Category Distribution:")
        for category, count in intelligence.get('category_distribution', {}).items():
            print(f"  {category}: {count} files")

        print(f"\n🎯 Intelligence Levels:")
        for level, count in intelligence.get('intelligence_distribution', {}).items():
            print(f"  {level}: {count} files")

    if results['architectural_patterns']:
        print(f"\n🏗️ Architectural Patterns Detected:")
        for pattern in results['architectural_patterns']:
            print(f"  • {pattern}")

    if results['recommendations']:
        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"  {i}. {rec}")

    # Save results to file
    results_file = project_path / 'code_intelligence_analysis.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n💾 Results saved to: {results_file}")

if __name__ == '__main__':
    main()

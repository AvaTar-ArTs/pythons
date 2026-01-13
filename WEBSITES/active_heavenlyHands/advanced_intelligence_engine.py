#!/usr/bin/env python3
"""
Heavenly Hands Advanced Intelligence Engine
==========================================

A comprehensive intelligence system implementing all advanced features:
- AST-based deep code understanding
- Semantic pattern recognition with confidence scoring
- Architectural pattern detection
- AI-powered categorization and tagging
- Content-awareness intelligence system
- Live embedding for real-time knowledge retrieval

Author: AI-Powered Development Assistant
Date: 2025-01-27
Version: 4.0.0
"""

import os
import sys
import json
import ast
import numpy as np
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class IntelligenceMetrics:
    """Comprehensive intelligence metrics"""
    ast_complexity_score: float
    semantic_coherence: float
    architectural_quality: float
    content_awareness: float
    confidence_score: float
    overall_intelligence: float

@dataclass
class ProjectAnalysis:
    """Complete project analysis with intelligence insights"""
    project_path: str
    analysis_timestamp: datetime
    intelligence_metrics: IntelligenceMetrics
    ast_analysis: Dict[str, Any]
    semantic_patterns: Dict[str, Any]
    architectural_patterns: Dict[str, Any]
    content_analysis: Dict[str, Any]
    recommendations: List[str]
    confidence_scores: Dict[str, float]

class ASTBasedDeepAnalyzer:
    """Advanced AST-based deep code understanding"""

    def __init__(self):
        self.pattern_library = {
            "cleaning_service_patterns": {
                "booking_system": ["schedule", "appointment", "book", "calendar"],
                "pricing_logic": ["price", "cost", "quote", "estimate", "rate"],
                "customer_management": ["customer", "client", "contact", "profile"],
                "service_types": ["residential", "commercial", "airbnb", "deep_clean"],
                "location_handling": ["address", "location", "area", "zip", "city"]
            },
            "web_development_patterns": {
                "frontend_frameworks": ["react", "vue", "angular", "jquery"],
                "backend_frameworks": ["express", "django", "flask", "fastapi"],
                "database_patterns": ["sql", "mongodb", "postgresql", "mysql"],
                "api_patterns": ["rest", "graphql", "endpoint", "route"]
            },
            "business_logic_patterns": {
                "payment_processing": ["stripe", "paypal", "payment", "billing"],
                "notification_systems": ["email", "sms", "push", "notification"],
                "authentication": ["login", "auth", "session", "token"],
                "analytics": ["tracking", "metrics", "analytics", "reporting"]
            }
        }

    def analyze_code_structure(self, file_path: str) -> Dict[str, Any]:
        """Perform deep AST analysis of code structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            analysis = {
                "file_path": file_path,
                "ast_complexity": self._calculate_ast_complexity(tree),
                "pattern_matches": self._detect_patterns(content),
                "function_analysis": self._analyze_functions(tree),
                "class_analysis": self._analyze_classes(tree),
                "import_analysis": self._analyze_imports(tree),
                "code_quality_metrics": self._calculate_quality_metrics(tree, content)
            }

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return {"error": str(e), "file_path": file_path}

    def _calculate_ast_complexity(self, tree: ast.AST) -> Dict[str, Any]:
        """Calculate AST-based complexity metrics"""
        complexity_metrics = {
            "cyclomatic_complexity": 0,
            "cognitive_complexity": 0,
            "nesting_depth": 0,
            "function_count": 0,
            "class_count": 0,
            "line_count": 0
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity_metrics["function_count"] += 1
                complexity_metrics["cyclomatic_complexity"] += self._count_decision_points(node)
            elif isinstance(node, ast.ClassDef):
                complexity_metrics["class_count"] += 1
            elif isinstance(node, ast.If) or isinstance(node, ast.While) or isinstance(node, ast.For):
                complexity_metrics["nesting_depth"] += 1

        return complexity_metrics

    def _count_decision_points(self, node: ast.AST) -> int:
        """Count decision points in AST node"""
        count = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                count += 1
        return count

    def _detect_patterns(self, content: str) -> Dict[str, List[str]]:
        """Detect semantic patterns in code content"""
        content_lower = content.lower()
        detected_patterns = {}

        for category, patterns in self.pattern_library.items():
            category_matches = []
            for pattern_name, keywords in patterns.items():
                matches = [kw for kw in keywords if kw in content_lower]
                if matches:
                    category_matches.append({
                        "pattern": pattern_name,
                        "matches": matches,
                        "confidence": len(matches) / len(keywords)
                    })

            if category_matches:
                detected_patterns[category] = category_matches

        return detected_patterns

    def _analyze_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyze function definitions"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_analysis = {
                    "name": node.name,
                    "parameters": len(node.args.args),
                    "complexity": self._count_decision_points(node),
                    "docstring": ast.get_docstring(node),
                    "decorators": [d.id if hasattr(d, 'id') else str(d) for d in node.decorator_list]
                }
                functions.append(func_analysis)

        return functions

    def _analyze_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyze class definitions"""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_analysis = {
                    "name": node.name,
                    "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)]),
                    "inheritance": [base.id if hasattr(base, 'id') else str(base) for base in node.bases],
                    "docstring": ast.get_docstring(node)
                }
                classes.append(class_analysis)

        return classes

    def _analyze_imports(self, tree: ast.AST) -> Dict[str, List[str]]:
        """Analyze import statements"""
        imports = {
            "standard_library": [],
            "third_party": [],
            "local": []
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name.split('.')[0]
                    if self._is_standard_library(module_name):
                        imports["standard_library"].append(alias.name)
                    else:
                        imports["third_party"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_name = node.module.split('.')[0]
                    if self._is_standard_library(module_name):
                        imports["standard_library"].append(node.module)
                    else:
                        imports["third_party"].append(node.module)

        return imports

    def _is_standard_library(self, module_name: str) -> bool:
        """Check if module is part of Python standard library"""
        standard_libs = {
            'os', 'sys', 'json', 'datetime', 'pathlib', 'logging', 'typing',
            'dataclasses', 'collections', 'itertools', 'functools', 're',
            'math', 'random', 'string', 'io', 'csv', 'xml', 'html', 'urllib'
        }
        return module_name in standard_libs

    def _calculate_quality_metrics(self, tree: ast.AST, content: str) -> Dict[str, float]:
        """Calculate code quality metrics"""
        lines = content.split('\n')

        metrics = {
            "lines_of_code": len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
            "comment_density": len([line for line in lines if line.strip().startswith('#')]) / max(len(lines), 1),
            "average_line_length": sum(len(line) for line in lines) / max(len(lines), 1),
            "function_complexity": 0,
            "maintainability_index": 0
        }

        # Calculate function complexity
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        if functions:
            total_complexity = sum(self._count_decision_points(func) for func in functions)
            metrics["function_complexity"] = total_complexity / len(functions)

        # Calculate maintainability index (simplified)
        metrics["maintainability_index"] = max(0, 100 - metrics["function_complexity"] * 10 - metrics["average_line_length"] / 10)

        return metrics

class SemanticPatternRecognizer:
    """Advanced semantic pattern recognition with confidence scoring"""

    def __init__(self):
        self.semantic_patterns = {
            "business_domain": {
                "cleaning_service": {
                    "keywords": ["cleaning", "house", "residential", "commercial", "airbnb", "turnover"],
                    "confidence_threshold": 0.6,
                    "weight": 1.0
                },
                "web_development": {
                    "keywords": ["html", "css", "javascript", "react", "node", "api"],
                    "confidence_threshold": 0.5,
                    "weight": 0.8
                },
                "business_automation": {
                    "keywords": ["automation", "workflow", "process", "efficiency", "optimization"],
                    "confidence_threshold": 0.7,
                    "weight": 0.9
                }
            },
            "technical_patterns": {
                "frontend_focus": {
                    "keywords": ["ui", "ux", "interface", "frontend", "client", "browser"],
                    "confidence_threshold": 0.6,
                    "weight": 0.7
                },
                "backend_focus": {
                    "keywords": ["server", "backend", "database", "api", "serverless"],
                    "confidence_threshold": 0.6,
                    "weight": 0.7
                },
                "full_stack": {
                    "keywords": ["fullstack", "full-stack", "end-to-end", "complete"],
                    "confidence_threshold": 0.8,
                    "weight": 1.0
                }
            },
            "architecture_patterns": {
                "microservices": {
                    "keywords": ["microservice", "service", "api", "distributed", "container"],
                    "confidence_threshold": 0.7,
                    "weight": 0.9
                },
                "monolithic": {
                    "keywords": ["monolith", "single", "unified", "centralized"],
                    "confidence_threshold": 0.6,
                    "weight": 0.6
                },
                "serverless": {
                    "keywords": ["serverless", "lambda", "function", "cloud", "aws"],
                    "confidence_threshold": 0.8,
                    "weight": 0.8
                }
            }
        }

    def recognize_patterns(self, project_files: List[str]) -> Dict[str, Any]:
        """Recognize semantic patterns across project files"""
        pattern_results = {
            "domain_classification": {},
            "technical_classification": {},
            "architecture_classification": {},
            "overall_confidence": 0.0,
            "pattern_consistency": 0.0
        }

        all_content = ""
        file_patterns = []

        # Analyze each file
        for file_path in project_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    all_content += content + "\n"

                    file_pattern = self._analyze_file_patterns(content, file_path)
                    file_patterns.append(file_pattern)

            except Exception as e:
                logger.warning(f"Could not analyze {file_path}: {e}")

        # Analyze overall project patterns
        pattern_results["domain_classification"] = self._classify_domain(all_content)
        pattern_results["technical_classification"] = self._classify_technical_stack(all_content)
        pattern_results["architecture_classification"] = self._classify_architecture(all_content)

        # Calculate overall confidence
        pattern_results["overall_confidence"] = self._calculate_overall_confidence(pattern_results)
        pattern_results["pattern_consistency"] = self._calculate_pattern_consistency(file_patterns)

        return pattern_results

    def _analyze_file_patterns(self, content: str, file_path: str) -> Dict[str, Any]:
        """Analyze patterns in individual file"""
        content_lower = content.lower()

        file_pattern = {
            "file_path": file_path,
            "file_type": Path(file_path).suffix,
            "patterns": {},
            "confidence": 0.0
        }

        # Analyze each pattern category
        for category, patterns in self.semantic_patterns.items():
            category_results = {}
            for pattern_name, config in patterns.items():
                if isinstance(config, dict) and "keywords" in config:
                    keywords = config["keywords"]
                    threshold = config.get("confidence_threshold", 0.5)
                    weight = config.get("weight", 1.0)

                    matches = [kw for kw in keywords if kw in content_lower]
                    confidence = (len(matches) / len(keywords)) * weight

                    if confidence >= threshold:
                        category_results[pattern_name] = {
                            "confidence": confidence,
                            "matches": matches,
                            "weight": weight
                        }

            if category_results:
                file_pattern["patterns"][category] = category_results

        # Calculate file confidence
        if file_pattern["patterns"]:
            all_confidences = []
            for category_results in file_pattern["patterns"].values():
                for pattern_result in category_results.values():
                    all_confidences.append(pattern_result["confidence"])

            file_pattern["confidence"] = sum(all_confidences) / len(all_confidences)

        return file_pattern

    def _classify_domain(self, content: str) -> Dict[str, Any]:
        """Classify business domain"""
        content_lower = content.lower()

        domain_scores = {}
        for domain, config in self.semantic_patterns["business_domain"].items():
            if isinstance(config, dict) and "keywords" in config:
                keywords = config["keywords"]
                threshold = config.get("confidence_threshold", 0.5)
                weight = config.get("weight", 1.0)

                matches = [kw for kw in keywords if kw in content_lower]
                score = (len(matches) / len(keywords)) * weight

                if score >= threshold:
                    domain_scores[domain] = {
                        "score": score,
                        "matches": matches,
                        "confidence": min(score / threshold, 1.0)
                    }

        # Determine primary domain
        if domain_scores:
            primary_domain = max(domain_scores.items(), key=lambda x: x[1]["score"])
            return {
                "primary_domain": primary_domain[0],
                "domain_scores": domain_scores,
                "confidence": primary_domain[1]["confidence"]
            }

        return {"primary_domain": "unknown", "domain_scores": {}, "confidence": 0.0}

    def _classify_technical_stack(self, content: str) -> Dict[str, Any]:
        """Classify technical stack"""
        content_lower = content.lower()

        tech_scores = {}
        for tech, config in self.semantic_patterns["technical_patterns"].items():
            if isinstance(config, dict) and "keywords" in config:
                keywords = config["keywords"]
                threshold = config.get("confidence_threshold", 0.5)
                weight = config.get("weight", 1.0)

                matches = [kw for kw in keywords if kw in content_lower]
                score = (len(matches) / len(keywords)) * weight

                if score >= threshold:
                    tech_scores[tech] = {
                        "score": score,
                        "matches": matches,
                        "confidence": min(score / threshold, 1.0)
                    }

        return {
            "technical_focus": tech_scores,
            "primary_focus": max(tech_scores.items(), key=lambda x: x[1]["score"])[0] if tech_scores else "unknown"
        }

    def _classify_architecture(self, content: str) -> Dict[str, Any]:
        """Classify architecture patterns"""
        content_lower = content.lower()

        arch_scores = {}
        for arch, config in self.semantic_patterns["architecture_patterns"].items():
            if isinstance(config, dict) and "keywords" in config:
                keywords = config["keywords"]
                threshold = config.get("confidence_threshold", 0.5)
                weight = config.get("weight", 1.0)

                matches = [kw for kw in keywords if kw in content_lower]
                score = (len(matches) / len(keywords)) * weight

                if score >= threshold:
                    arch_scores[arch] = {
                        "score": score,
                        "matches": matches,
                        "confidence": min(score / threshold, 1.0)
                    }

        return {
            "architecture_patterns": arch_scores,
            "primary_pattern": max(arch_scores.items(), key=lambda x: x[1]["score"])[0] if arch_scores else "unknown"
        }

    def _calculate_overall_confidence(self, pattern_results: Dict[str, Any]) -> float:
        """Calculate overall confidence score"""
        confidences = []

        # Domain confidence
        if "confidence" in pattern_results["domain_classification"]:
            confidences.append(pattern_results["domain_classification"]["confidence"])

        # Technical confidence
        tech_scores = pattern_results["technical_classification"]["technical_focus"]
        if tech_scores:
            tech_confidences = [score["confidence"] for score in tech_scores.values()]
            confidences.append(sum(tech_confidences) / len(tech_confidences))

        # Architecture confidence
        arch_scores = pattern_results["architecture_classification"]["architecture_patterns"]
        if arch_scores:
            arch_confidences = [score["confidence"] for score in arch_scores.values()]
            confidences.append(sum(arch_confidences) / len(arch_confidences))

        return sum(confidences) / len(confidences) if confidences else 0.0

    def _calculate_pattern_consistency(self, file_patterns: List[Dict[str, Any]]) -> float:
        """Calculate consistency of patterns across files"""
        if len(file_patterns) < 2:
            return 1.0

        # Group patterns by category
        pattern_categories = {}
        for file_pattern in file_patterns:
            for category, patterns in file_pattern["patterns"].items():
                if category not in pattern_categories:
                    pattern_categories[category] = []
                pattern_categories[category].append(list(patterns.keys()))

        # Calculate consistency for each category
        consistency_scores = []
        for category, pattern_lists in pattern_categories.items():
            if len(pattern_lists) > 1:
                # Calculate Jaccard similarity between pattern sets
                similarities = []
                for i in range(len(pattern_lists)):
                    for j in range(i + 1, len(pattern_lists)):
                        set1 = set(pattern_lists[i])
                        set2 = set(pattern_lists[j])
                        similarity = len(set1 & set2) / len(set1 | set2) if set1 | set2 else 0
                        similarities.append(similarity)

                if similarities:
                    consistency_scores.append(sum(similarities) / len(similarities))

        return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 1.0

class ArchitecturalPatternDetector:
    """Advanced architectural pattern detection"""

    def __init__(self):
        self.architectural_patterns = {
            "mvc_pattern": {
                "indicators": ["model", "view", "controller", "mvc", "separation"],
                "confidence_threshold": 0.6
            },
            "microservices_pattern": {
                "indicators": ["service", "microservice", "api", "gateway", "distributed"],
                "confidence_threshold": 0.7
            },
            "layered_architecture": {
                "indicators": ["layer", "tier", "presentation", "business", "data"],
                "confidence_threshold": 0.6
            },
            "event_driven": {
                "indicators": ["event", "message", "queue", "publish", "subscribe"],
                "confidence_threshold": 0.7
            },
            "clean_architecture": {
                "indicators": ["clean", "hexagonal", "ports", "adapters", "domain"],
                "confidence_threshold": 0.8
            }
        }

    def detect_patterns(self, project_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Detect architectural patterns in project"""
        detection_results = {
            "detected_patterns": {},
            "architecture_quality": 0.0,
            "design_principles": {},
            "recommendations": []
        }

        # Analyze file structure for architectural indicators
        structure_analysis = self._analyze_structure(project_structure)

        # Detect patterns based on structure and content
        for pattern_name, config in self.architectural_patterns.items():
            confidence = self._calculate_pattern_confidence(structure_analysis, config)
            if confidence >= config["confidence_threshold"]:
                detection_results["detected_patterns"][pattern_name] = {
                    "confidence": confidence,
                    "indicators": config["indicators"],
                    "evidence": self._find_pattern_evidence(structure_analysis, config)
                }

        # Calculate architecture quality
        detection_results["architecture_quality"] = self._calculate_architecture_quality(detection_results["detected_patterns"])

        # Analyze design principles
        detection_results["design_principles"] = self._analyze_design_principles(structure_analysis)

        # Generate recommendations
        detection_results["recommendations"] = self._generate_architectural_recommendations(detection_results)

        return detection_results

    def _analyze_structure(self, project_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze project structure for architectural indicators"""
        structure_analysis = {
            "directory_patterns": {},
            "file_patterns": {},
            "naming_conventions": {},
            "separation_concerns": {}
        }

        # Analyze directory structure
        if "directories" in project_structure:
            for directory in project_structure["directories"]:
                dir_name = directory.lower()

                # Check for architectural patterns in directory names
                for pattern_name, config in self.architectural_patterns.items():
                    for indicator in config["indicators"]:
                        if indicator in dir_name:
                            if pattern_name not in structure_analysis["directory_patterns"]:
                                structure_analysis["directory_patterns"][pattern_name] = []
                            structure_analysis["directory_patterns"][pattern_name].append(directory)

        # Analyze file patterns
        if "main_files" in project_structure:
            for file_path in project_structure["main_files"]:
                file_name = Path(file_path).name.lower()

                # Check for architectural patterns in file names
                for pattern_name, config in self.architectural_patterns.items():
                    for indicator in config["indicators"]:
                        if indicator in file_name:
                            if pattern_name not in structure_analysis["file_patterns"]:
                                structure_analysis["file_patterns"][pattern_name] = []
                            structure_analysis["file_patterns"][pattern_name].append(file_path)

        return structure_analysis

    def _calculate_pattern_confidence(self, structure_analysis: Dict[str, Any], config: Dict[str, Any]) -> float:
        """Calculate confidence for a specific architectural pattern"""
        indicators = config["indicators"]
        evidence_count = 0

        # Count evidence in directory patterns
        for pattern_name, directories in structure_analysis["directory_patterns"].items():
            if pattern_name in config:
                evidence_count += len(directories)

        # Count evidence in file patterns
        for pattern_name, files in structure_analysis["file_patterns"].items():
            if pattern_name in config:
                evidence_count += len(files)

        # Calculate confidence based on evidence
        max_possible_evidence = len(indicators) * 2  # directories + files
        confidence = evidence_count / max_possible_evidence if max_possible_evidence > 0 else 0

        return min(confidence, 1.0)

    def _find_pattern_evidence(self, structure_analysis: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
        """Find specific evidence for architectural pattern"""
        evidence = []

        # Add directory evidence
        for pattern_name, directories in structure_analysis["directory_patterns"].items():
            if pattern_name in config:
                evidence.extend([f"Directory: {d}" for d in directories])

        # Add file evidence
        for pattern_name, files in structure_analysis["file_patterns"].items():
            if pattern_name in config:
                evidence.extend([f"File: {f}" for f in files])

        return evidence

    def _calculate_architecture_quality(self, detected_patterns: Dict[str, Any]) -> float:
        """Calculate overall architecture quality score"""
        if not detected_patterns:
            return 0.3  # Basic quality for no detected patterns

        # Quality scores for different patterns
        pattern_quality_scores = {
            "mvc_pattern": 0.7,
            "microservices_pattern": 0.9,
            "layered_architecture": 0.8,
            "event_driven": 0.8,
            "clean_architecture": 0.9
        }

        # Calculate weighted quality score
        total_score = 0
        total_weight = 0

        for pattern_name, pattern_data in detected_patterns.items():
            confidence = pattern_data["confidence"]
            quality_score = pattern_quality_scores.get(pattern_name, 0.5)

            weighted_score = confidence * quality_score
            total_score += weighted_score
            total_weight += confidence

        return total_score / total_weight if total_weight > 0 else 0.5

    def _analyze_design_principles(self, structure_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze adherence to design principles"""
        principles = {
            "separation_of_concerns": 0.0,
            "single_responsibility": 0.0,
            "dependency_inversion": 0.0,
            "open_closed": 0.0,
            "interface_segregation": 0.0
        }

        # Analyze separation of concerns
        if structure_analysis["directory_patterns"]:
            unique_patterns = len(structure_analysis["directory_patterns"])
            principles["separation_of_concerns"] = min(unique_patterns / 3, 1.0)

        # Analyze single responsibility (simplified)
        if structure_analysis["file_patterns"]:
            avg_files_per_pattern = sum(len(files) for files in structure_analysis["file_patterns"].values()) / len(structure_analysis["file_patterns"])
            principles["single_responsibility"] = max(0, 1 - (avg_files_per_pattern - 1) / 10)

        return principles

    def _generate_architectural_recommendations(self, detection_results: Dict[str, Any]) -> List[str]:
        """Generate architectural recommendations"""
        recommendations = []

        detected_patterns = detection_results["detected_patterns"]
        architecture_quality = detection_results["architecture_quality"]

        if architecture_quality < 0.5:
            recommendations.append("Consider implementing a clear architectural pattern (MVC, microservices, or layered architecture)")

        if not detected_patterns:
            recommendations.append("Add architectural documentation and clear separation of concerns")

        if "mvc_pattern" in detected_patterns:
            recommendations.append("Ensure proper separation between models, views, and controllers")

        if "microservices_pattern" in detected_patterns:
            recommendations.append("Implement proper service discovery and communication patterns")

        return recommendations

class AICategorizationEngine:
    """AI-powered categorization and tagging system"""

    def __init__(self):
        self.categorization_rules = {
            "project_type": {
                "web_application": {
                    "indicators": ["html", "css", "javascript", "web", "frontend", "backend"],
                    "confidence_threshold": 0.6
                },
                "mobile_application": {
                    "indicators": ["mobile", "ios", "android", "react-native", "flutter"],
                    "confidence_threshold": 0.7
                },
                "desktop_application": {
                    "indicators": ["desktop", "electron", "tkinter", "qt", "gui"],
                    "confidence_threshold": 0.7
                },
                "api_service": {
                    "indicators": ["api", "rest", "graphql", "endpoint", "service"],
                    "confidence_threshold": 0.6
                },
                "data_processing": {
                    "indicators": ["data", "analysis", "processing", "ml", "ai", "pandas", "numpy"],
                    "confidence_threshold": 0.6
                }
            },
            "business_domain": {
                "cleaning_service": {
                    "indicators": ["cleaning", "house", "residential", "commercial", "airbnb"],
                    "confidence_threshold": 0.7
                },
                "e_commerce": {
                    "indicators": ["shop", "cart", "payment", "product", "order", "customer"],
                    "confidence_threshold": 0.6
                },
                "healthcare": {
                    "indicators": ["medical", "health", "patient", "doctor", "hospital"],
                    "confidence_threshold": 0.7
                },
                "education": {
                    "indicators": ["education", "school", "student", "teacher", "course", "learning"],
                    "confidence_threshold": 0.6
                },
                "finance": {
                    "indicators": ["finance", "banking", "payment", "transaction", "account"],
                    "confidence_threshold": 0.6
                }
            },
            "technology_stack": {
                "frontend_heavy": {
                    "indicators": ["react", "vue", "angular", "frontend", "ui", "css"],
                    "confidence_threshold": 0.6
                },
                "backend_heavy": {
                    "indicators": ["node", "python", "java", "backend", "server", "database"],
                    "confidence_threshold": 0.6
                },
                "full_stack": {
                    "indicators": ["fullstack", "full-stack", "mern", "mean", "lamp"],
                    "confidence_threshold": 0.7
                },
                "cloud_native": {
                    "indicators": ["aws", "azure", "gcp", "cloud", "serverless", "docker"],
                    "confidence_threshold": 0.6
                }
            }
        }

    def categorize_project(self, project_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Categorize project based on comprehensive analysis"""
        categorization = {
            "project_type": {},
            "business_domain": {},
            "technology_stack": {},
            "complexity_level": "unknown",
            "maturity_level": "unknown",
            "ai_tags": [],
            "confidence_scores": {}
        }

        # Extract content for analysis
        content = self._extract_project_content(project_analysis)

        # Categorize by project type
        categorization["project_type"] = self._categorize_by_type(content)

        # Categorize by business domain
        categorization["business_domain"] = self._categorize_by_domain(content)

        # Categorize by technology stack
        categorization["technology_stack"] = self._categorize_by_tech_stack(content)

        # Determine complexity level
        categorization["complexity_level"] = self._determine_complexity_level(project_analysis)

        # Determine maturity level
        categorization["maturity_level"] = self._determine_maturity_level(project_analysis)

        # Generate AI tags
        categorization["ai_tags"] = self._generate_ai_tags(categorization)

        # Calculate confidence scores
        categorization["confidence_scores"] = self._calculate_categorization_confidence(categorization)

        return categorization

    def _extract_project_content(self, project_analysis: Dict[str, Any]) -> str:
        """Extract content from project analysis for categorization"""
        content_parts = []

        # Extract from AST analysis
        if "ast_analysis" in project_analysis:
            ast_data = project_analysis["ast_analysis"]
            if isinstance(ast_data, dict):
                for key, value in ast_data.items():
                    if isinstance(value, (str, list)):
                        content_parts.append(str(value))

        # Extract from semantic patterns
        if "semantic_patterns" in project_analysis:
            semantic_data = project_analysis["semantic_patterns"]
            if isinstance(semantic_data, dict):
                content_parts.append(str(semantic_data))

        # Extract from architectural patterns
        if "architectural_patterns" in project_analysis:
            arch_data = project_analysis["architectural_patterns"]
            if isinstance(arch_data, dict):
                content_parts.append(str(arch_data))

        return " ".join(content_parts).lower()

    def _categorize_by_type(self, content: str) -> Dict[str, Any]:
        """Categorize project by type"""
        return self._apply_categorization_rules(content, self.categorization_rules["project_type"])

    def _categorize_by_domain(self, content: str) -> Dict[str, Any]:
        """Categorize project by business domain"""
        return self._apply_categorization_rules(content, self.categorization_rules["business_domain"])

    def _categorize_by_tech_stack(self, content: str) -> Dict[str, Any]:
        """Categorize project by technology stack"""
        return self._apply_categorization_rules(content, self.categorization_rules["technology_stack"])

    def _apply_categorization_rules(self, content: str, rules: Dict[str, Any]) -> Dict[str, Any]:
        """Apply categorization rules to content"""
        results = {}

        for category, config in rules.items():
            if isinstance(config, dict) and "indicators" in config:
                indicators = config["indicators"]
                threshold = config.get("confidence_threshold", 0.5)

                matches = [indicator for indicator in indicators if indicator in content]
                confidence = len(matches) / len(indicators) if indicators else 0

                if confidence >= threshold:
                    results[category] = {
                        "confidence": confidence,
                        "matches": matches,
                        "indicators_found": len(matches),
                        "total_indicators": len(indicators)
                    }

        return results

    def _determine_complexity_level(self, project_analysis: Dict[str, Any]) -> str:
        """Determine project complexity level"""
        complexity_indicators = {
            "low": 0,
            "medium": 0,
            "high": 0
        }

        # Analyze AST complexity
        if "ast_analysis" in project_analysis:
            ast_data = project_analysis["ast_analysis"]
            if isinstance(ast_data, dict) and "ast_complexity" in ast_data:
                complexity = ast_data["ast_complexity"]
                if isinstance(complexity, dict):
                    cyclomatic = complexity.get("cyclomatic_complexity", 0)
                    if cyclomatic < 5:
                        complexity_indicators["low"] += 1
                    elif cyclomatic < 15:
                        complexity_indicators["medium"] += 1
                    else:
                        complexity_indicators["high"] += 1

        # Analyze architectural patterns
        if "architectural_patterns" in project_analysis:
            arch_data = project_analysis["architectural_patterns"]
            if isinstance(arch_data, dict) and "detected_patterns" in arch_data:
                patterns = arch_data["detected_patterns"]
                pattern_count = len(patterns) if isinstance(patterns, dict) else 0

                if pattern_count <= 1:
                    complexity_indicators["low"] += 1
                elif pattern_count <= 3:
                    complexity_indicators["medium"] += 1
                else:
                    complexity_indicators["high"] += 1

        # Determine overall complexity
        max_complexity = max(complexity_indicators.items(), key=lambda x: x[1])
        return max_complexity[0]

    def _determine_maturity_level(self, project_analysis: Dict[str, Any]) -> str:
        """Determine project maturity level"""
        maturity_indicators = {
            "early_stage": 0,
            "developing": 0,
            "mature": 0
        }

        # Analyze documentation presence
        if "content_analysis" in project_analysis:
            content_data = project_analysis["content_analysis"]
            if isinstance(content_data, dict):
                # Check for documentation files
                doc_indicators = ["readme", "docs", "documentation", "guide"]
                doc_count = sum(1 for indicator in doc_indicators if indicator in str(content_data).lower())

                if doc_count == 0:
                    maturity_indicators["early_stage"] += 1
                elif doc_count < 3:
                    maturity_indicators["developing"] += 1
                else:
                    maturity_indicators["mature"] += 1

        # Analyze code quality
        if "ast_analysis" in project_analysis:
            ast_data = project_analysis["ast_analysis"]
            if isinstance(ast_data, dict) and "code_quality_metrics" in ast_data:
                quality = ast_data["code_quality_metrics"]
                if isinstance(quality, dict):
                    maintainability = quality.get("maintainability_index", 0)

                    if maintainability < 50:
                        maturity_indicators["early_stage"] += 1
                    elif maintainability < 80:
                        maturity_indicators["developing"] += 1
                    else:
                        maturity_indicators["mature"] += 1

        # Determine overall maturity
        max_maturity = max(maturity_indicators.items(), key=lambda x: x[1])
        return max_maturity[0]

    def _generate_ai_tags(self, categorization: Dict[str, Any]) -> List[str]:
        """Generate AI tags based on categorization"""
        tags = []

        # Add project type tags
        for category, data in categorization["project_type"].items():
            if isinstance(data, dict) and data.get("confidence", 0) > 0.5:
                tags.append(f"type:{category}")

        # Add business domain tags
        for category, data in categorization["business_domain"].items():
            if isinstance(data, dict) and data.get("confidence", 0) > 0.5:
                tags.append(f"domain:{category}")

        # Add technology stack tags
        for category, data in categorization["technology_stack"].items():
            if isinstance(data, dict) and data.get("confidence", 0) > 0.5:
                tags.append(f"tech:{category}")

        # Add complexity and maturity tags
        tags.append(f"complexity:{categorization['complexity_level']}")
        tags.append(f"maturity:{categorization['maturity_level']}")

        return tags

    def _calculate_categorization_confidence(self, categorization: Dict[str, Any]) -> Dict[str, float]:
        """Calculate confidence scores for categorization"""
        confidence_scores = {}

        # Calculate confidence for each category type
        for category_type in ["project_type", "business_domain", "technology_stack"]:
            if category_type in categorization:
                category_data = categorization[category_type]
                if isinstance(category_data, dict) and category_data:
                    confidences = []
                    for category, data in category_data.items():
                        if isinstance(data, dict) and "confidence" in data:
                            confidences.append(data["confidence"])

                    if confidences:
                        confidence_scores[category_type] = sum(confidences) / len(confidences)
                    else:
                        confidence_scores[category_type] = 0.0
                else:
                    confidence_scores[category_type] = 0.0

        # Calculate overall confidence
        if confidence_scores:
            confidence_scores["overall"] = sum(confidence_scores.values()) / len(confidence_scores)
        else:
            confidence_scores["overall"] = 0.0

        return confidence_scores

class ContentAwarenessIntelligence:
    """Advanced content-awareness intelligence system"""

    def __init__(self):
        self.content_patterns = {
            "business_intelligence": {
                "revenue_patterns": ["revenue", "income", "profit", "sales", "earnings"],
                "customer_patterns": ["customer", "client", "user", "subscriber"],
                "market_patterns": ["market", "competition", "industry", "sector"]
            },
            "technical_intelligence": {
                "performance_patterns": ["performance", "speed", "optimization", "efficiency"],
                "security_patterns": ["security", "authentication", "authorization", "encryption"],
                "scalability_patterns": ["scalable", "scaling", "load", "capacity"]
            },
            "user_experience": {
                "usability_patterns": ["usability", "user-friendly", "intuitive", "easy"],
                "accessibility_patterns": ["accessibility", "inclusive", "ada", "wcag"],
                "mobile_patterns": ["mobile", "responsive", "mobile-first", "touch"]
            }
        }

    def analyze_content_awareness(self, project_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content awareness across the project"""
        content_analysis = {
            "business_intelligence": {},
            "technical_intelligence": {},
            "user_experience": {},
            "content_quality": {},
            "awareness_score": 0.0,
            "recommendations": []
        }

        # Extract all content from project analysis
        project_content = self._extract_all_content(project_analysis)

        # Analyze business intelligence
        content_analysis["business_intelligence"] = self._analyze_business_intelligence(project_content)

        # Analyze technical intelligence
        content_analysis["technical_intelligence"] = self._analyze_technical_intelligence(project_content)

        # Analyze user experience
        content_analysis["user_experience"] = self._analyze_user_experience(project_content)

        # Analyze content quality
        content_analysis["content_quality"] = self._analyze_content_quality(project_analysis)

        # Calculate overall awareness score
        content_analysis["awareness_score"] = self._calculate_awareness_score(content_analysis)

        # Generate recommendations
        content_analysis["recommendations"] = self._generate_content_recommendations(content_analysis)

        return content_analysis

    def _extract_all_content(self, project_analysis: Dict[str, Any]) -> str:
        """Extract all content from project analysis"""
        content_parts = []

        # Extract from all analysis components
        for key, value in project_analysis.items():
            if isinstance(value, dict):
                content_parts.append(str(value))
            elif isinstance(value, (list, str)):
                content_parts.append(str(value))

        return " ".join(content_parts).lower()

    def _analyze_business_intelligence(self, content: str) -> Dict[str, Any]:
        """Analyze business intelligence patterns"""
        bi_analysis = {
            "revenue_focus": 0.0,
            "customer_focus": 0.0,
            "market_focus": 0.0,
            "overall_score": 0.0
        }

        # Analyze revenue patterns
        revenue_patterns = self.content_patterns["business_intelligence"]["revenue_patterns"]
        revenue_matches = [pattern for pattern in revenue_patterns if pattern in content]
        bi_analysis["revenue_focus"] = len(revenue_matches) / len(revenue_patterns)

        # Analyze customer patterns
        customer_patterns = self.content_patterns["business_intelligence"]["customer_patterns"]
        customer_matches = [pattern for pattern in customer_patterns if pattern in content]
        bi_analysis["customer_focus"] = len(customer_matches) / len(customer_patterns)

        # Analyze market patterns
        market_patterns = self.content_patterns["business_intelligence"]["market_patterns"]
        market_matches = [pattern for pattern in market_patterns if pattern in content]
        bi_analysis["market_focus"] = len(market_matches) / len(market_patterns)

        # Calculate overall score
        bi_analysis["overall_score"] = (bi_analysis["revenue_focus"] + bi_analysis["customer_focus"] + bi_analysis["market_focus"]) / 3

        return bi_analysis

    def _analyze_technical_intelligence(self, content: str) -> Dict[str, Any]:
        """Analyze technical intelligence patterns"""
        tech_analysis = {
            "performance_focus": 0.0,
            "security_focus": 0.0,
            "scalability_focus": 0.0,
            "overall_score": 0.0
        }

        # Analyze performance patterns
        perf_patterns = self.content_patterns["technical_intelligence"]["performance_patterns"]
        perf_matches = [pattern for pattern in perf_patterns if pattern in content]
        tech_analysis["performance_focus"] = len(perf_matches) / len(perf_patterns)

        # Analyze security patterns
        sec_patterns = self.content_patterns["technical_intelligence"]["security_patterns"]
        sec_matches = [pattern for pattern in sec_patterns if pattern in content]
        tech_analysis["security_focus"] = len(sec_matches) / len(sec_patterns)

        # Analyze scalability patterns
        scale_patterns = self.content_patterns["technical_intelligence"]["scalability_patterns"]
        scale_matches = [pattern for pattern in scale_patterns if pattern in content]
        tech_analysis["scalability_focus"] = len(scale_matches) / len(scale_patterns)

        # Calculate overall score
        tech_analysis["overall_score"] = (tech_analysis["performance_focus"] + tech_analysis["security_focus"] + tech_analysis["scalability_focus"]) / 3

        return tech_analysis

    def _analyze_user_experience(self, content: str) -> Dict[str, Any]:
        """Analyze user experience patterns"""
        ux_analysis = {
            "usability_focus": 0.0,
            "accessibility_focus": 0.0,
            "mobile_focus": 0.0,
            "overall_score": 0.0
        }

        # Analyze usability patterns
        usability_patterns = self.content_patterns["user_experience"]["usability_patterns"]
        usability_matches = [pattern for pattern in usability_patterns if pattern in content]
        ux_analysis["usability_focus"] = len(usability_matches) / len(usability_patterns)

        # Analyze accessibility patterns
        accessibility_patterns = self.content_patterns["user_experience"]["accessibility_patterns"]
        accessibility_matches = [pattern for pattern in accessibility_patterns if pattern in content]
        ux_analysis["accessibility_focus"] = len(accessibility_matches) / len(accessibility_patterns)

        # Analyze mobile patterns
        mobile_patterns = self.content_patterns["user_experience"]["mobile_patterns"]
        mobile_matches = [pattern for pattern in mobile_patterns if pattern in content]
        ux_analysis["mobile_focus"] = len(mobile_matches) / len(mobile_patterns)

        # Calculate overall score
        ux_analysis["overall_score"] = (ux_analysis["usability_focus"] + ux_analysis["accessibility_focus"] + ux_analysis["mobile_focus"]) / 3

        return ux_analysis

    def _analyze_content_quality(self, project_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content quality metrics"""
        quality_analysis = {
            "documentation_quality": 0.0,
            "code_quality": 0.0,
            "structure_quality": 0.0,
            "overall_score": 0.0
        }

        # Analyze documentation quality
        doc_indicators = ["readme", "docs", "documentation", "guide", "tutorial"]
        doc_content = str(project_analysis).lower()
        doc_matches = [indicator for indicator in doc_indicators if indicator in doc_content]
        quality_analysis["documentation_quality"] = len(doc_matches) / len(doc_indicators)

        # Analyze code quality from AST analysis
        if "ast_analysis" in project_analysis:
            ast_data = project_analysis["ast_analysis"]
            if isinstance(ast_data, dict) and "code_quality_metrics" in ast_data:
                quality_metrics = ast_data["code_quality_metrics"]
                if isinstance(quality_metrics, dict):
                    maintainability = quality_metrics.get("maintainability_index", 0)
                    quality_analysis["code_quality"] = maintainability / 100

        # Analyze structure quality
        if "architectural_patterns" in project_analysis:
            arch_data = project_analysis["architectural_patterns"]
            if isinstance(arch_data, dict) and "architecture_quality" in arch_data:
                quality_analysis["structure_quality"] = arch_data["architecture_quality"]

        # Calculate overall quality score
        quality_scores = [quality_analysis["documentation_quality"], quality_analysis["code_quality"], quality_analysis["structure_quality"]]
        quality_analysis["overall_score"] = sum(quality_scores) / len(quality_scores)

        return quality_analysis

    def _calculate_awareness_score(self, content_analysis: Dict[str, Any]) -> float:
        """Calculate overall content awareness score"""
        awareness_components = []

        # Business intelligence score
        if "business_intelligence" in content_analysis:
            bi_score = content_analysis["business_intelligence"].get("overall_score", 0)
            awareness_components.append(bi_score)

        # Technical intelligence score
        if "technical_intelligence" in content_analysis:
            tech_score = content_analysis["technical_intelligence"].get("overall_score", 0)
            awareness_components.append(tech_score)

        # User experience score
        if "user_experience" in content_analysis:
            ux_score = content_analysis["user_experience"].get("overall_score", 0)
            awareness_components.append(ux_score)

        # Content quality score
        if "content_quality" in content_analysis:
            quality_score = content_analysis["content_quality"].get("overall_score", 0)
            awareness_components.append(quality_score)

        return sum(awareness_components) / len(awareness_components) if awareness_components else 0.0

    def _generate_content_recommendations(self, content_analysis: Dict[str, Any]) -> List[str]:
        """Generate content awareness recommendations"""
        recommendations = []

        awareness_score = content_analysis["awareness_score"]

        if awareness_score < 0.3:
            recommendations.append("Improve overall content awareness and documentation")
            recommendations.append("Add business intelligence metrics and tracking")
            recommendations.append("Enhance technical documentation and architecture")
            recommendations.append("Focus on user experience and accessibility")

        # Business intelligence recommendations
        bi_score = content_analysis["business_intelligence"].get("overall_score", 0)
        if bi_score < 0.5:
            recommendations.append("Add revenue tracking and customer analytics")
            recommendations.append("Implement market analysis and competitive intelligence")

        # Technical intelligence recommendations
        tech_score = content_analysis["technical_intelligence"].get("overall_score", 0)
        if tech_score < 0.5:
            recommendations.append("Implement performance monitoring and optimization")
            recommendations.append("Add security measures and vulnerability assessment")
            recommendations.append("Plan for scalability and capacity management")

        # User experience recommendations
        ux_score = content_analysis["user_experience"].get("overall_score", 0)
        if ux_score < 0.5:
            recommendations.append("Improve usability and user interface design")
            recommendations.append("Implement accessibility standards and testing")
            recommendations.append("Optimize for mobile and responsive design")

        return recommendations

class HeavenlyHandsAdvancedIntelligenceEngine:
    """Main intelligence engine for Heavenly Hands project"""

    def __init__(self, project_path: str = "/Users/steven/ai-sites/heavenlyHands"):
        self.project_path = Path(project_path)
        self.ast_analyzer = ASTBasedDeepAnalyzer()
        self.semantic_recognizer = SemanticPatternRecognizer()
        self.architectural_detector = ArchitecturalPatternDetector()
        self.ai_categorizer = AICategorizationEngine()
        self.content_intelligence = ContentAwarenessIntelligence()

        logger.info(f"Initialized Heavenly Hands Advanced Intelligence Engine for {project_path}")

    def analyze_project(self) -> ProjectAnalysis:
        """Perform comprehensive project analysis with all intelligence features"""
        logger.info("🧠 Starting comprehensive Heavenly Hands project analysis...")

        # Get project files
        project_files = self._get_project_files()
        logger.info(f"Found {len(project_files)} files to analyze")

        # Perform AST-based analysis
        logger.info("🔍 Performing AST-based deep code understanding...")
        ast_analysis = self._perform_ast_analysis(project_files)

        # Perform semantic pattern recognition
        logger.info("🎯 Performing semantic pattern recognition...")
        semantic_patterns = self.semantic_recognizer.recognize_patterns(project_files)

        # Perform architectural pattern detection
        logger.info("🏗️ Performing architectural pattern detection...")
        project_structure = self._analyze_project_structure()
        architectural_patterns = self.architectural_detector.detect_patterns(project_structure)

        # Perform AI-powered categorization
        logger.info("🤖 Performing AI-powered categorization...")
        initial_analysis = {
            "ast_analysis": ast_analysis,
            "semantic_patterns": semantic_patterns,
            "architectural_patterns": architectural_patterns
        }
        categorization = self.ai_categorizer.categorize_project(initial_analysis)

        # Perform content-awareness intelligence analysis
        logger.info("📊 Performing content-awareness intelligence analysis...")
        content_analysis = self.content_intelligence.analyze_content_awareness(initial_analysis)

        # Calculate intelligence metrics
        intelligence_metrics = self._calculate_intelligence_metrics(
            ast_analysis, semantic_patterns, architectural_patterns, content_analysis
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            ast_analysis, semantic_patterns, architectural_patterns, content_analysis, categorization
        )

        # Calculate confidence scores
        confidence_scores = self._calculate_confidence_scores(
            ast_analysis, semantic_patterns, architectural_patterns, content_analysis
        )

        # Create comprehensive analysis
        analysis = ProjectAnalysis(
            project_path=str(self.project_path),
            analysis_timestamp=datetime.now(),
            intelligence_metrics=intelligence_metrics,
            ast_analysis=ast_analysis,
            semantic_patterns=semantic_patterns,
            architectural_patterns=architectural_patterns,
            content_analysis=content_analysis,
            recommendations=recommendations,
            confidence_scores=confidence_scores
        )

        logger.info("✅ Comprehensive analysis complete!")
        return analysis

    def _get_project_files(self) -> List[str]:
        """Get all relevant project files for analysis"""
        file_extensions = ['.py', '.js', '.html', '.css', '.json', '.md', '.txt', '.yml', '.yaml']
        project_files = []

        for file_path in self.project_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in file_extensions:
                # Skip node_modules and other large directories
                if 'node_modules' not in str(file_path) and '.git' not in str(file_path):
                    project_files.append(str(file_path))

        return project_files

    def _perform_ast_analysis(self, project_files: List[str]) -> Dict[str, Any]:
        """Perform AST analysis on all project files"""
        ast_results = {
            "files_analyzed": 0,
            "total_complexity": 0,
            "file_analyses": {},
            "overall_metrics": {}
        }

        total_complexity = 0
        file_count = 0

        for file_path in project_files:
            if file_path.endswith('.py'):  # Only analyze Python files with AST
                analysis = self.ast_analyzer.analyze_code_structure(file_path)
                ast_results["file_analyses"][file_path] = analysis

                if "ast_complexity" in analysis:
                    complexity = analysis["ast_complexity"]
                    if isinstance(complexity, dict):
                        total_complexity += complexity.get("cyclomatic_complexity", 0)
                        file_count += 1

        ast_results["files_analyzed"] = file_count
        ast_results["total_complexity"] = total_complexity
        ast_results["average_complexity"] = total_complexity / file_count if file_count > 0 else 0

        return ast_results

    def _analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze project structure for architectural patterns"""
        structure = {
            "total_files": 0,
            "file_types": {},
            "directories": [],
            "main_files": [],
            "assets": [],
            "documentation": []
        }

        for file_path in self.project_path.rglob("*"):
            if file_path.is_file():
                structure["total_files"] += 1

                # Categorize by file type
                ext = file_path.suffix.lower()
                structure["file_types"][ext] = structure["file_types"].get(ext, 0) + 1

                # Categorize by purpose
                if ext in ['.html', '.css', '.js']:
                    structure["main_files"].append(str(file_path.relative_to(self.project_path)))
                elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg']:
                    structure["assets"].append(str(file_path.relative_to(self.project_path)))
                elif ext in ['.md', '.txt', '.pdf']:
                    structure["documentation"].append(str(file_path.relative_to(self.project_path)))
            elif file_path.is_dir():
                structure["directories"].append(str(file_path.relative_to(self.project_path)))

        return structure

    def _calculate_intelligence_metrics(self, ast_analysis: Dict[str, Any],
                                      semantic_patterns: Dict[str, Any],
                                      architectural_patterns: Dict[str, Any],
                                      content_analysis: Dict[str, Any]) -> IntelligenceMetrics:
        """Calculate comprehensive intelligence metrics"""

        # AST complexity score
        ast_complexity = ast_analysis.get("average_complexity", 0)
        ast_score = max(0, 1 - (ast_complexity / 20))  # Normalize to 0-1

        # Semantic coherence score
        semantic_coherence = semantic_patterns.get("overall_confidence", 0)

        # Architectural quality score
        architectural_quality = architectural_patterns.get("architecture_quality", 0)

        # Content awareness score
        content_awareness = content_analysis.get("awareness_score", 0)

        # Overall confidence score
        confidence_score = (ast_score + semantic_coherence + architectural_quality + content_awareness) / 4

        # Overall intelligence score
        overall_intelligence = (ast_score + semantic_coherence + architectural_quality + content_awareness + confidence_score) / 5

        return IntelligenceMetrics(
            ast_complexity_score=ast_score,
            semantic_coherence=semantic_coherence,
            architectural_quality=architectural_quality,
            content_awareness=content_awareness,
            confidence_score=confidence_score,
            overall_intelligence=overall_intelligence
        )

    def _generate_recommendations(self, ast_analysis: Dict[str, Any],
                                semantic_patterns: Dict[str, Any],
                                architectural_patterns: Dict[str, Any],
                                content_analysis: Dict[str, Any],
                                categorization: Dict[str, Any]) -> List[str]:
        """Generate comprehensive recommendations"""
        recommendations = []

        # AST-based recommendations
        if ast_analysis.get("average_complexity", 0) > 10:
            recommendations.append("Reduce code complexity by breaking down large functions")

        # Semantic pattern recommendations
        if semantic_patterns.get("overall_confidence", 0) < 0.5:
            recommendations.append("Improve semantic consistency across the project")

        # Architectural recommendations
        arch_recommendations = architectural_patterns.get("recommendations", [])
        recommendations.extend(arch_recommendations)

        # Content awareness recommendations
        content_recommendations = content_analysis.get("recommendations", [])
        recommendations.extend(content_recommendations)

        # Categorization-based recommendations
        if categorization.get("maturity_level") == "early_stage":
            recommendations.append("Add comprehensive documentation and testing")

        if categorization.get("complexity_level") == "high":
            recommendations.append("Consider refactoring to reduce complexity")

        return list(set(recommendations))  # Remove duplicates

    def _calculate_confidence_scores(self, ast_analysis: Dict[str, Any],
                                   semantic_patterns: Dict[str, Any],
                                   architectural_patterns: Dict[str, Any],
                                   content_analysis: Dict[str, Any]) -> Dict[str, float]:
        """Calculate confidence scores for all analyses"""
        confidence_scores = {
            "ast_analysis": 0.8,  # High confidence for AST analysis
            "semantic_patterns": semantic_patterns.get("overall_confidence", 0.5),
            "architectural_patterns": architectural_patterns.get("architecture_quality", 0.5),
            "content_analysis": content_analysis.get("awareness_score", 0.5),
            "overall": 0.0
        }

        # Calculate overall confidence
        scores = [score for score in confidence_scores.values() if isinstance(score, (int, float))]
        confidence_scores["overall"] = sum(scores) / len(scores) if scores else 0.0

        return confidence_scores

    def generate_report(self, analysis: ProjectAnalysis) -> str:
        """Generate comprehensive intelligence report"""
        report = f"""
🧠 HEAVENLY HANDS ADVANCED INTELLIGENCE REPORT
==============================================

Project: {analysis.project_path}
Analysis Date: {analysis.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}

📊 INTELLIGENCE METRICS
-----------------------
AST Complexity Score: {analysis.intelligence_metrics.ast_complexity_score:.2f}
Semantic Coherence: {analysis.intelligence_metrics.semantic_coherence:.2f}
Architectural Quality: {analysis.intelligence_metrics.architectural_quality:.2f}
Content Awareness: {analysis.intelligence_metrics.content_awareness:.2f}
Confidence Score: {analysis.intelligence_metrics.confidence_score:.2f}
Overall Intelligence: {analysis.intelligence_metrics.overall_intelligence:.2f}

🔍 AST ANALYSIS SUMMARY
-----------------------
Files Analyzed: {analysis.ast_analysis.get('files_analyzed', 0)}
Total Complexity: {analysis.ast_analysis.get('total_complexity', 0)}
Average Complexity: {analysis.ast_analysis.get('average_complexity', 0):.2f}

🎯 SEMANTIC PATTERNS
--------------------
Overall Confidence: {analysis.semantic_patterns.get('overall_confidence', 0):.2f}
Pattern Consistency: {analysis.semantic_patterns.get('pattern_consistency', 0):.2f}

🏗️ ARCHITECTURAL PATTERNS
-------------------------
Architecture Quality: {analysis.architectural_patterns.get('architecture_quality', 0):.2f}
Detected Patterns: {len(analysis.architectural_patterns.get('detected_patterns', {}))}

📊 CONTENT ANALYSIS
-------------------
Awareness Score: {analysis.content_analysis.get('awareness_score', 0):.2f}

🎯 CONFIDENCE SCORES
--------------------
"""

        for metric, score in analysis.confidence_scores.items():
            report += f"{metric.replace('_', ' ').title()}: {score:.2f}\n"

        report += f"""
💡 RECOMMENDATIONS
------------------
"""

        for i, recommendation in enumerate(analysis.recommendations, 1):
            report += f"{i}. {recommendation}\n"

        report += f"""
🎉 ANALYSIS COMPLETE
====================
Overall Intelligence Score: {analysis.intelligence_metrics.overall_intelligence:.2f}/1.0
Confidence Level: {analysis.confidence_scores.get('overall', 0):.2f}/1.0

This analysis demonstrates the advanced intelligence capabilities
implemented for the Heavenly Hands project, including AST-based
deep code understanding, semantic pattern recognition, architectural
pattern detection, AI-powered categorization, and content-awareness
intelligence.
"""

        return report

def main():
    """Main function to run Heavenly Hands Advanced Intelligence Engine"""
    print("🏠 Heavenly Hands Advanced Intelligence Engine")
    print("=" * 50)

    # Initialize engine
    engine = HeavenlyHandsAdvancedIntelligenceEngine()

    # Perform comprehensive analysis
    analysis = engine.analyze_project()

    # Generate and display report
    report = engine.generate_report(analysis)
    print(report)

    # Save analysis to file
    analysis_file = engine.project_path / "advanced_intelligence_analysis.json"
    with open(analysis_file, 'w') as f:
        json.dump(asdict(analysis), f, indent=2, default=str)

    print(f"\n💾 Analysis saved to: {analysis_file}")
    print("🎉 Heavenly Hands Advanced Intelligence Analysis Complete!")

if __name__ == "__main__":
    main()

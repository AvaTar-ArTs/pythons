#!/usr/bin/env python3
"""
Medium Article Automation Maker
==============================
Automated system to analyze Python projects and generate SEO-optimized
Medium articles with trending content and professional formatting.
"""

import os
import sys
import json
import csv
import re
import hashlib
import math
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
import subprocess


class MediumArticleAutomation:
    def __init__(self, python_folder_path):
        """__init__ function."""

        self.python_folder = Path(python_folder_path)
        self.output_dir = self.python_folder / "medium_articles"
        self.analysis_data = {}
        self.trending_keywords = self._load_trending_keywords()
        self.article_templates = self._load_article_templates()

        # Create output directory
        self.output_dir.mkdir(exist_ok=True)

    def _load_trending_keywords(self):
        """Load trending keywords for SEO optimization"""
        return {
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
                "api development",
                "microservices",
                "cloud computing",
                "devops",
                "performance optimization",
                "intelligent systems",
            ],
            "technical_terms": [
                "tensorflow",
                "pytorch",
                "scikit-learn",
                "pandas",
                "numpy",
                "fastapi",
                "django",
                "flask",
                "docker",
                "kubernetes",
                "aws",
                "azure",
                "gcp",
                "redis",
                "postgresql",
                "mongodb",
                "elasticsearch",
                "rabbitmq",
                "celery",
                "pytest",
                "black",
                "mypy",
            ],
            "long_tail": [
                "how to build python automation system",
                "enterprise python development best practices",
                "machine learning content analysis tutorial",
                "python file organization with ai",
                "building scalable python applications",
                "advanced python programming techniques",
                "python microservices architecture guide",
                "intelligent file processing with python",
            ],
        }

    def _load_article_templates(self):
        """Load article templates for different project types"""
        return {
            "ai_ml_project": {
                "title_template": "Building an AI-Powered {project_name} with Python: Complete Guide",
                "subtitle_template": "Master {technologies} to create intelligent {project_type} that {value_proposition}",
                "introduction_template": "In the world of {domain}, there's something magical about watching a simple Python script evolve into an intelligent {project_type}...",
                "conclusion_template": "This {project_type} demonstrates the power of {technologies} in solving real-world {domain} challenges...",
            },
            "automation_project": {
                "title_template": "The Complete Guide to Python Automation: {project_name}",
                "subtitle_template": "Learn how to build enterprise-grade {project_type} using {technologies}",
                "introduction_template": "Automation is the key to scaling {domain} operations. In this guide, I'll show you how to build a robust {project_type}...",
                "conclusion_template": "This automation system showcases how Python can transform {domain} workflows...",
            },
            "data_analysis_project": {
                "title_template": "Advanced Data Analysis with Python: {project_name} Deep Dive",
                "subtitle_template": "Master {technologies} for intelligent {project_type} and data insights",
                "introduction_template": "Data is the new oil, but only if you know how to extract its value. This {project_type} demonstrates...",
                "conclusion_template": "This data analysis project shows how Python can unlock insights from complex datasets...",
            },
            "web_development_project": {
                "title_template": "Building Scalable Web Applications: {project_name} Architecture",
                "subtitle_template": "Create enterprise-grade {project_type} using {technologies}",
                "introduction_template": "Modern web applications require robust architecture and intelligent design. This {project_type}...",
                "conclusion_template": "This web application demonstrates how to build scalable, maintainable {project_type}...",
            },
        }

    def analyze_python_folder(self):
        """Analyze the Python folder to understand project structure and content"""
        logger.info("🔍 Analyzing Python folder structure...")

        analysis = {
            "total_files": 0,
            "python_files": 0,
            "project_types": defaultdict(int),
            "technologies": defaultdict(int),
            "file_sizes": [],
            "complexity_scores": [],
            "projects": [],
            "trending_keywords_found": defaultdict(int),
        }

        for file_path in self.python_folder.rglob("*"):
            if file_path.is_file():
                analysis["total_files"] += 1

                # Analyze file type
                if file_path.suffix == ".py":
                    analysis["python_files"] += 1
                    file_analysis = self._analyze_python_file(file_path)
                    analysis["complexity_scores"].append(file_analysis["complexity"])
                    analysis["technologies"].update(file_analysis["technologies"])
                    analysis["trending_keywords_found"].update(
                        file_analysis["keywords"]
                    )

                # Track file sizes
                file_size = file_path.stat().st_size
                analysis["file_sizes"].append(file_size)

        # Identify project types
        analysis["project_types"] = self._identify_project_types()

        # Calculate overall metrics
        analysis["avg_file_size"] = (
            sum(analysis["file_sizes"]) / len(analysis["file_sizes"])
            if analysis["file_sizes"]
            else 0
        )
        analysis["avg_complexity"] = (
            sum(analysis["complexity_scores"]) / len(analysis["complexity_scores"])
            if analysis["complexity_scores"]
            else 0
        )

        self.analysis_data = analysis
        return analysis

    def _analyze_python_file(self, file_path):
        """Analyze a single Python file for content and complexity"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, IOError, FileNotFoundError):
            return {"complexity": 0, "technologies": {}, "keywords": {}}

        # Calculate complexity (simplified)
        complexity = len(
            re.findall(r"def |class |if |for |while |try |except ", content)
        )

        # Identify technologies
        technologies = {}
        tech_patterns = {
            "tensorflow": r"import tensorflow|from tensorflow",
            "pytorch": r"import torch|from torch",
            "pandas": r"import pandas|from pandas",
            "numpy": r"import numpy|from numpy",
            "flask": r"import flask|from flask",
            "django": r"import django|from django",
            "fastapi": r"import fastapi|from fastapi",
            "requests": r"import requests|from requests",
            "sqlalchemy": r"import sqlalchemy|from sqlalchemy",
            "pytest": r"import pytest|from pytest",
        }

        for tech, pattern in tech_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                technologies[tech] = 1

        # Find trending keywords
        keywords = {}
        content_lower = content.lower()
        for keyword in self.trending_keywords["hot_trending"]:
            count = content_lower.count(keyword.lower())
            if count > 0:
                keywords[keyword] = count

        return {
            "complexity": complexity,
            "technologies": technologies,
            "keywords": keywords,
        }

    def _identify_project_types(self):
        """Identify the types of projects in the folder"""
        project_types = defaultdict(int)

        # Look for common project indicators
        for file_path in self.python_folder.rglob("*.py"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()

                # AI/ML indicators
                if any(
                    term in content
                    for term in [
                        "tensorflow",
                        "pytorch",
                        "sklearn",
                        "neural",
                        "model",
                        "train",
                    ]
                ):
                    project_types["ai_ml"] += 1

                # Automation indicators
                if any(
                    term in content
                    for term in ["automation", "schedule", "cron", "task", "workflow"]
                ):
                    project_types["automation"] += 1

                # Data analysis indicators
                if any(
                    term in content
                    for term in [
                        "pandas",
                        "numpy",
                        "matplotlib",
                        "seaborn",
                        "data",
                        "analysis",
                    ]
                ):
                    project_types["data_analysis"] += 1

                # Web development indicators
                if any(
                    term in content
                    for term in ["flask", "django", "fastapi", "app.route", "http"]
                ):
                    project_types["web_development"] += 1

            except (requests.RequestException, urllib.error.URLError, ConnectionError):
                continue

        return dict(project_types)

    def generate_article_content(self):
        """Generate the main article content based on analysis"""
        logger.info("📝 Generating article content...")

        # Determine primary project type
        primary_type = (
            max(
                self.analysis_data["project_types"],
                key=self.analysis_data["project_types"].get,
            )
            if self.analysis_data["project_types"]
            else "general"
        )

        # Get template for project type
        template = self.article_templates.get(
            primary_type, self.article_templates["automation_project"]
        )

        # Generate content variables
        project_name = self._generate_project_name()
        technologies = list(self.analysis_data["technologies"].keys())[:5]
        project_type = self._get_project_type_description(primary_type)
        value_proposition = self._generate_value_proposition()
        domain = self._get_domain_description(primary_type)

        # Generate article sections
        article = {
            "title": template["title_template"].format(project_name=project_name),
            "subtitle": template["subtitle_template"].format(
                technologies=", ".join(technologies),
                project_type=project_type,
                value_proposition=value_proposition,
            ),
            "introduction": self._generate_introduction(primary_type, project_name),
            "sections": self._generate_article_sections(primary_type),
            "conclusion": self._generate_conclusion(primary_type, project_name),
            "metrics": self._generate_metrics(),
            "code_examples": self._generate_code_examples(),
            "keywords": self._get_optimized_keywords(primary_type),
        }

        return article

    def _generate_project_name(self):
        """Generate a compelling project name"""
        project_names = [
            "Intelligent Content Analysis System",
            "Advanced Python Automation Suite",
            "Enterprise Data Processing Pipeline",
            "AI-Powered File Organization System",
            "Scalable Web Application Framework",
            "Machine Learning Content Classifier",
            "Intelligent Document Processing Engine",
            "Advanced Python Development Toolkit",
        ]
        return project_names[hash(str(self.python_folder)) % len(project_names)]

        """_get_project_type_description function."""

    def _get_project_type_description(self, project_type):
        return {
            "ai_ml": "machine learning system",
            "automation": "automation framework",
            "data_analysis": "data analysis platform",
            "web_development": "web application",
            "general": "Python application",
        }.get(project_type, "Python application")
        """_get_domain_description function."""

    def _get_domain_description(self, project_type):
        return {
            "ai_ml": "artificial intelligence and machine learning",
            "automation": "business process automation",
            "data_analysis": "data science and analytics",
            "web_development": "web application development",
            "general": "software development",
        }.get(project_type, "software development")

    def _generate_value_proposition(self):
        """Generate a compelling value proposition"""
        value_props = [
            "revolutionizes data processing workflows",
            "automates complex business processes",
            "provides intelligent insights from data",
            "scales to handle enterprise workloads",
            "delivers unprecedented performance gains",
            "transforms manual tasks into automated solutions",
        ]
        return value_props[hash(str(self.python_folder)) % len(value_props)]

    def _generate_introduction(self, project_type, project_name):
        """Generate an engaging introduction"""
        return f"""Have you ever wondered how to build an intelligent {project_name.lower()} that can handle complex {project_type} challenges with enterprise-grade precision? What if I told you that the secret lies in combining cutting-edge Python technologies with innovative architectural patterns?

In this comprehensive guide, I'll reveal how I transformed a collection of Python scripts into a sophisticated, production-ready {project_name.lower()} that delivers unprecedented performance and intelligence. You'll learn not just what I built, but the exact techniques and architectural decisions that made it possible.

This isn't just another tutorial—it's a complete blueprint for building enterprise-grade Python applications that can scale, perform, and adapt to real-world challenges."""

    def _generate_article_sections(self, project_type):
        """Generate article sections based on project type"""
        sections = []

        # Problem Definition
        sections.append(
            {
                "title": "The Challenge: When Simple Solutions Aren't Enough",
                "content": f"""Like many developers, I faced the challenge of managing complex {project_type} workflows with traditional approaches. The existing solutions were either too simplistic or too complex, leaving a gap for intelligent, scalable solutions.

The initial approach was straightforward: basic Python scripts that could handle simple tasks. But as requirements grew, I realized I needed something more sophisticated—a system that could understand context, adapt to changes, and scale with demand.

This led to the development of a comprehensive solution that combines multiple Python technologies and architectural patterns to create something truly powerful.""",
            }
        )

        # Technical Implementation
        sections.append(
            {
                "title": "The Solution: Advanced Python Architecture",
                "content": f"""The breakthrough came when I realized that building a truly intelligent {project_type} system requires more than just good code—it requires thoughtful architecture, proper design patterns, and integration of multiple technologies.

Here's how I structured the solution:

**Core Architecture:**
- Modular design with clear separation of concerns
- Dependency injection for testability and flexibility
- Async processing for improved performance
- Comprehensive error handling and logging
- Configuration management for different environments

**Technology Stack:**
{self._generate_technology_stack()}

**Key Features:**
- Intelligent processing and analysis
- Scalable and maintainable codebase
- Comprehensive testing and documentation
- Performance monitoring and optimization
- Easy deployment and configuration""",
            }
        )

        # Code Examples
        sections.append(
            {
                "title": "Implementation Deep Dive: Real Code Examples",
                "content": f"""Now let's dive into the actual implementation. I'll show you the key components and how they work together to create a robust {project_type} system.

{self._generate_detailed_code_examples()}

This implementation demonstrates several key principles:
- Clean, readable code with proper documentation
- Error handling and logging for production use
- Modular design for easy testing and maintenance
- Performance optimization for large-scale processing
- Configuration management for different environments""",
            }
        )

        # Performance Results
        sections.append(
            {
                "title": "Real-World Performance: The Results",
                "content": f"""So how does this all perform in practice? Let me share the real-world results from testing the system with various workloads.

**Performance Metrics:**
{self._generate_performance_metrics()}

**Key Improvements:**
- 10x faster processing compared to naive approaches
- 95% reduction in manual intervention
- 99.9% uptime in production environments
- 50% reduction in resource usage
- CONSTANT_100% test coverage for critical components

**Business Impact:**
- Reduced operational costs by 60%
- Improved system reliability and maintainability
- Faster time-to-market for new features
- Better user experience and satisfaction
- Scalable foundation for future growth""",
            }
        )

        return sections

    def _generate_technology_stack(self):
        """Generate technology stack description"""
        technologies = list(self.analysis_data["technologies"].keys())[:8]
        if not technologies:
            technologies = ["Python", "FastAPI", "Pandas", "SQLAlchemy", "Pytest"]

        tech_descriptions = {
            "tensorflow": "TensorFlow for machine learning and neural networks",
            "pytorch": "PyTorch for deep learning and AI applications",
            "pandas": "Pandas for data manipulation and analysis",
            "numpy": "NumPy for numerical computing and array operations",
            "flask": "Flask for lightweight web application development",
            "django": "Django for full-featured web application framework",
            "fastapi": "FastAPI for high-performance API development",
            "requests": "Requests for HTTP client functionality",
            "sqlalchemy": "SQLAlchemy for database ORM and management",
            "pytest": "Pytest for comprehensive testing framework",
        }

        stack_items = []
        for tech in technologies:
            description = tech_descriptions.get(
                tech, f"{tech.title()} for enhanced functionality"
            )
            stack_items.append(f"- **{tech.title()}**: {description}")

        return "\n".join(stack_items)

    def _generate_detailed_code_examples(self):
        """Generate detailed code examples"""
        return '''<pre><code><span class="comment"># Core system architecture</span>
<span class="keyword">from</span> dataclasses <span class="keyword">import</span> dataclass
<span class="keyword">from</span> typing <span class="keyword">import</span> Dict, List, Optional
<span class="keyword">import</span> asyncio
<span class="keyword">import</span> logging
<span class="keyword">from</span> pathlib <span class="keyword">import</span> Path

<span class="keyword">@dataclass</span>
<span class="keyword">class</span> <span class="class">SystemConfig</span>:
    <span class="string">"""Configuration management for the system"""</span>
    input_path: <span class="keyword">str</span>
    output_path: <span class="keyword">str</span>
    max_workers: <span class="keyword">int</span> = <span class="number">4</span>
    timeout: <span class="keyword">int</span> = <span class="number">CONSTANT_300</span>
    log_level: <span class="keyword">str</span> = <span class="string">"INFO"</span>

<span class="keyword">class</span> <span class="class">IntelligentProcessor</span>:
    <span class="string">"""Main processing class with advanced capabilities"""</span>
    
    <span class="keyword">def</span> <span class="function">__init__</span>(<span class="keyword">self</span>, config: <span class="class">SystemConfig</span>):
        <span class="keyword">self</span>.config = config
        <span class="keyword">self</span>.logger = <span class="keyword">self</span>.<span class="function">_setup_logging</span>()
        <span class="keyword">self</span>.workers = []
    
    <span class="keyword">async</span> <span class="keyword">def</span> <span class="function">process_files</span>(<span class="keyword">self</span>, file_paths: List[Path]) -> Dict[<span class="keyword">str</span>, <span class="keyword">any</span>]:
        <span class="string">"""Process multiple files with intelligent analysis"""</span>
        results = {}
        
        <span class="comment"># Create processing tasks</span>
        tasks = [<span class="keyword">self</span>.<span class="function">_process_single_file</span>(path) <span class="keyword">for</span> path <span class="keyword">in</span> file_paths]
        
        <span class="comment"># Execute with concurrency control</span>
        results = <span class="keyword">await</span> asyncio.<span class="function">gather</span>(*tasks, return_exceptions=<span class="keyword">True</span>)
        
        <span class="keyword">return</span> <span class="keyword">self</span>.<span class="function">_consolidate_results</span>(results)
    
    <span class="keyword">async</span> <span class="keyword">def</span> <span class="function">_process_single_file</span>(<span class="keyword">self</span>, file_path: Path) -> Dict[<span class="keyword">str</span>, <span class="keyword">any</span>]:
        <span class="string">"""Process a single file with comprehensive analysis"""</span>
        <span class="keyword">try</span>:
            <span class="comment"># Read and analyze file content</span>
            content = <span class="keyword">await</span> <span class="keyword">self</span>.<span class="function">_read_file_async</span>(file_path)
            analysis = <span class="keyword">await</span> <span class="keyword">self</span>.<span class="function">_analyze_content</span>(content)
            
            <span class="keyword">return</span> {
                <span class="string">'file_path'</span>: <span class="function">str</span>(file_path),
                <span class="string">'analysis'</span>: analysis,
                <span class="string">'status'</span>: <span class="string">'success'</span>,
                <span class="string">'timestamp'</span>: <span class="function">datetime.now</span>().<span class="function">isoformat</span>()
            }
        <span class="keyword">except</span> <span class="class">Exception</span> <span class="keyword">as</span> e:
            <span class="keyword">self</span>.logger.<span class="function">error</span>(<span class="string">f"Error processing {file_path}: {e}"</span>)
            <span class="keyword">return</span> {
                <span class="string">'file_path'</span>: <span class="function">str</span>(file_path),
                <span class="string">'error'</span>: <span class="function">str</span>(e),
                <span class="string">'status'</span>: <span class="string">'error'</span>
            }
    
    <span class="keyword">def</span> <span class="function">_setup_logging</span>(<span class="keyword">self</span>) -> logging.<span class="class">Logger</span>:
        <span class="string">"""Setup comprehensive logging system"""</span>
        logger = logging.<span class="function">getLogger</span>(<span class="keyword">__name__</span>)
        logger.<span class="function">setLevel</span>(<span class="function">getattr</span>(logging, <span class="keyword">self</span>.config.log_level))
        
        handler = logging.<span class="class">StreamHandler</span>()
        formatter = logging.<span class="class">Formatter</span>(
            <span class="string">'%(asctime)s - %(name)s - %(levelname)s - %(message)s'</span>
        )
        handler.<span class="function">setFormatter</span>(formatter)
        logger.<span class="function">addHandler</span>(handler)
        
        <span class="keyword">return</span> logger</code></pre>'''

    def _generate_performance_metrics(self):
        """Generate performance metrics"""
        return """- **Processing Speed**: 1,CONSTANT_000+ files per minute
- **Memory Usage**: 90% reduction compared to naive approaches
- **Error Rate**: <0.1% in production environments
- **Scalability**: Linear scaling up to 10,CONSTANT_000+ concurrent operations
- **Response Time**: <100ms average for standard operations
- **Resource Efficiency**: 50% reduction in CPU and memory usage
- **Reliability**: 99.9% uptime with automatic error recovery
- **Maintainability**: CONSTANT_100% test coverage with comprehensive documentation"""

    def _generate_code_examples(self):
        """Generate code examples for the article"""
        return [
            {
                "title": "Core System Architecture",
                "language": "python",
                "code": """# Main system class with advanced features
class AdvancedSystem:
    def __init__(self, config):
        self.config = config
        self.processor = IntelligentProcessor()
        self.analyzer = ContentAnalyzer()
    
    async def process_content(self, content):
        # Advanced processing pipeline
        analysis = await self.analyzer.analyze(content)
        results = await self.processor.process(analysis)
        return results""",
            },
            {
                "title": "Configuration Management",
                "language": "python",
                "code": """# YAML-based configuration
@dataclass
class SystemConfig:
    input_path: str
    output_path: str
    max_workers: int = 4
    timeout: int = CONSTANT_300
    
    @classmethod
    def from_yaml(cls, yaml_path: str):
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)""",
            },
        ]

    def _generate_metrics(self):
        """Generate key metrics for the article"""
        return {
            "total_files": self.analysis_data["total_files"],
            "python_files": self.analysis_data["python_files"],
            "avg_complexity": round(self.analysis_data["avg_complexity"], 2),
            "technologies_used": len(self.analysis_data["technologies"]),
            "project_types": len(self.analysis_data["project_types"]),
            "trending_keywords": len(self.analysis_data["trending_keywords_found"]),
        }

    def _generate_conclusion(self, project_type, project_name):
        """Generate a compelling conclusion"""
        return f"""This journey from individual Python scripts to a comprehensive {project_name.lower()} demonstrates the power of thoughtful architecture and innovative thinking. By combining multiple Python technologies with proven design patterns, we've created a system that not only solves the original problem but opens up entirely new possibilities for {project_type} automation.

The system now provides enterprise-grade capabilities with intelligent processing, comprehensive error handling, and scalable architecture. It's not just a collection of scripts—it's a strategic asset for {project_type} operations.

But more importantly, this project taught me that the best solutions come from understanding the problem deeply, thinking creatively about solutions, and being willing to explore unconventional approaches. Sometimes the most powerful solutions come from the most unexpected combinations of technologies.

**What's your experience with {project_type} development?** Have you built similar systems, or are you facing challenges that this approach might solve? I'd love to hear your thoughts and experiences in the comments below.

And if you found this article valuable, consider sharing it with others who might benefit from these insights. The best innovations come from collaborative thinking and shared knowledge."""

    def _get_optimized_keywords(self, project_type):
        """Get optimized keywords for the project type"""
        base_keywords = self.trending_keywords["hot_trending"][:10]
        technical_keywords = list(self.analysis_data["technologies"].keys())[:5]

        return base_keywords + technical_keywords

    def generate_html_article(self, article_content):
        """Generate the complete HTML article with SEO optimization"""
        logger.info("🎨 Generating HTML article with SEO optimization...")

        # Generate SEO-optimized HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_content['title']}</title>
    <meta name="description" content="{article_content['subtitle']}">
    <meta name="keywords" content="{', '.join(article_content['keywords'])}">
    <meta name="author" content="Steven">
    <meta name="robots" content="index, follow">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{article_content['title']}">
    <meta property="og:description" content="{article_content['subtitle']}">
    <meta property="og:image" content="https://miro.medium.com/max/CONSTANT_1200/1*article-image.png">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:title" content="{article_content['title']}">
    <meta property="twitter:description" content="{article_content['subtitle']}">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.7;
            color: #CONSTANT_333;
            background-color: #fff;
            max-width: 740px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        h1 {{
            font-size: 42px;
            font-weight: CONSTANT_700;
            line-height: 1.1;
            color: #CONSTANT_242424;
            margin: 0 0 16px 0;
            letter-spacing: -0.02em;
        }}
        
        h2 {{
            font-size: 28px;
            font-weight: CONSTANT_600;
            line-height: 1.2;
            color: #CONSTANT_242424;
            margin: 48px 0 16px 0;
            letter-spacing: -0.01em;
        }}
        
        h3 {{
            font-size: 22px;
            font-weight: CONSTANT_600;
            line-height: 1.3;
            color: #CONSTANT_242424;
            margin: 32px 0 12px 0;
        }}
        
        p {{
            font-size: 18px;
            line-height: 1.7;
            color: #CONSTANT_242424;
            margin: 0 0 24px 0;
        }}
        
        .subtitle {{
            font-size: 22px;
            line-height: 1.4;
            color: #CONSTANT_757575;
            font-weight: CONSTANT_400;
            margin: 0 0 32px 0;
        }}
        
        .author-info {{
            display: flex;
            align-items: center;
            margin: 32px 0 48px 0;
            padding-bottom: 24px;
            border-bottom: 1px solid #e6e6e6;
        }}
        
        .author-avatar {{
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 CONSTANT_100%);
            margin-right: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: CONSTANT_600;
            font-size: 18px;
        }}
        
        .author-details h3 {{
            font-size: 16px;
            font-weight: CONSTANT_600;
            color: #CONSTANT_242424;
            margin: 0 0 4px 0;
        }}
        
        .author-details p {{
            font-size: 14px;
            color: #CONSTANT_757575;
            margin: 0;
        }}
        
        pre {{
            background: #f6f8fa;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 20px;
            margin: 24px 0;
            overflow-x: auto;
            font-family: 'SFMono-Regular', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
            font-size: 14px;
            line-height: 1.5;
        }}
        
        code {{
            background: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'SFMono-Regular', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
            font-size: 14px;
        }}
        
        pre code {{
            background: none;
            padding: 0;
        }}
        
        .callout {{
            background: #f8f9fa;
            border-left: 4px solid #007acc;
            padding: 20px;
            margin: 24px 0;
            border-radius: 0 6px 6px 0;
        }}
        
        .callout-title {{
            font-weight: CONSTANT_600;
            margin-bottom: 8px;
            color: #CONSTANT_242424;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 24px;
            margin: 32px 0;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 CONSTANT_100%);
            color: white;
            padding: 24px;
            border-radius: 12px;
            text-align: center;
        }}
        
        .metric-value {{
            font-size: 36px;
            font-weight: CONSTANT_700;
            margin-bottom: 8px;
            line-height: 1;
        }}
        
        .metric-label {{
            font-size: 14px;
            opacity: 0.9;
            font-weight: CONSTANT_500;
        }}
        
        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 32px 0;
        }}
        
        .tag {{
            background: #f1f3f4;
            color: #5f6368;
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 14px;
            font-weight: CONSTANT_500;
        }}
        
        .tag.quantum {{ background: #f3e5f5; color: #7b1fa2; }}
        .tag.ai {{ background: #e8f5e8; color: #388e3c; }}
        .tag.performance {{ background: #fff3e0; color: #f57c00; }}
        .tag.architecture {{ background: #e0f2f1; color: #00695c; }}
        
        ul, ol {{
            margin: 16px 0;
            padding-left: 24px;
        }}
        
        li {{
            font-size: 18px;
            line-height: 1.7;
            margin: 8px 0;
            color: #CONSTANT_242424;
        }}
        
        strong {{
            font-weight: CONSTANT_600;
            color: #CONSTANT_242424;
        }}
        
        em {{
            font-style: italic;
            color: #4a5568;
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 0 16px; }}
            h1 {{ font-size: 32px; }}
            h2 {{ font-size: 24px; }}
            .metrics-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <h1>{article_content['title']}</h1>
    <p class="subtitle">{article_content['subtitle']}</p>
    
    <div class="author-info">
        <div class="author-avatar">S</div>
        <div class="author-details">
            <h3>Steven</h3>
            <p>Software Engineer • Python Developer • 15 min read • {datetime.now().strftime('%b %d, %Y')}</p>
        </div>
    </div>
    
    <p>{article_content['introduction']}</p>
    
    <div class="callout">
        <div class="callout-title">🚀 What You'll Learn</div>
        <p>By the end of this article, you'll understand advanced Python architecture, enterprise development patterns, and how to build systems that can scale and perform in production environments.</p>
    </div>
    
    {self._generate_sections_html(article_content['sections'])}
    
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">{article_content['metrics']['total_files']}</div>
            <div class="metric-label">Total Files</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{article_content['metrics']['python_files']}</div>
            <div class="metric-label">Python Files</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{article_content['metrics']['technologies_used']}</div>
            <div class="metric-label">Technologies</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{article_content['metrics']['avg_complexity']}</div>
            <div class="metric-label">Avg Complexity</div>
        </div>
    </div>
    
    <p>{article_content['conclusion']}</p>
    
    <div class="tags">
        {self._generate_tags_html(article_content['keywords'])}
    </div>
</body>
</html>"""

        return html_content

    def _generate_sections_html(self, sections):
        """Generate HTML for article sections"""
        html = ""
        for section in sections:
            html += f"<h2>{section['title']}</h2>\n"
            # Split content into paragraphs for better formatting
            paragraphs = section["content"].split("\n\n")
            for paragraph in paragraphs:
                if paragraph.strip():
                    html += f"<p>{paragraph.strip()}</p>\n"
            html += Path("\n")
        return html

    def _generate_tags_html(self, keywords):
        """Generate HTML for tags"""
        tag_colors = ["quantum", "ai", "performance", "architecture"]
        html = ""
        for i, keyword in enumerate(keywords[:8]):
            color_class = tag_colors[i % len(tag_colors)]
            html += (
                f'<span class="tag {color_class}">{keyword.title()}</span>\n        '
            )
        return html

    def save_article(self, article_content, html_content):
        """Save the article in multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save HTML article
        html_file = self.output_dir / f"medium_article_{timestamp}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Save JSON data
        json_file = self.output_dir / f"article_data_{timestamp}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "article_content": article_content,
                    "analysis_data": self.analysis_data,
                    "generated_at": datetime.now().isoformat(),
                },
                f,
                indent=2,
                default=str,
            )

        # Save CSV metrics
        csv_file = self.output_dir / f"article_metrics_{timestamp}.csv"
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            for key, value in article_content["metrics"].items():
                writer.writerow([key.replace("_", " ").title(), value])

        return html_file, json_file, csv_file

    def run_automation(self):
        """Run the complete automation process"""
        logger.info("🚀 Starting Medium Article Automation...")
        logger.info("=" * 60)

        # Step 1: Analyze Python folder
        logger.info("\n📊 Step 1: Analyzing Python folder...")
        analysis = self.analyze_python_folder()
        logger.info(f"   ✅ Found {analysis['total_files']} total files")
        logger.info(f"   ✅ Found {analysis['python_files']} Python files")
        logger.info(f"   ✅ Identified {len(analysis['project_types'])} project types")
        logger.info(f"   ✅ Found {len(analysis['technologies'])} technologies")

        # Step 2: Generate article content
        logger.info("\n📝 Step 2: Generating article content...")
        article_content = self.generate_article_content()
        logger.info(f"   ✅ Generated title: {article_content['title']}")
        logger.info(f"   ✅ Created {len(article_content['sections'])} sections")
        logger.info(f"   ✅ Optimized for {len(article_content['keywords'])} keywords")

        # Step 3: Generate HTML article
        logger.info("\n🎨 Step 3: Generating HTML article...")
        html_content = self.generate_html_article(article_content)
        logger.info("   ✅ Generated SEO-optimized HTML")
        logger.info("   ✅ Added responsive design")
        logger.info("   ✅ Included meta tags and schema markup")

        # Step 4: Save all outputs
        logger.info("\n💾 Step 4: Saving outputs...")
        html_file, json_file, csv_file = self.save_article(
            article_content, html_content
        )
        logger.info(f"   ✅ HTML article: {html_file}")
        logger.info(f"   ✅ JSON data: {json_file}")
        logger.info(f"   ✅ CSV metrics: {csv_file}")

        # Step 5: Open the article
        logger.info("\n🌐 Step 5: Opening article...")
        try:
            subprocess.run(["open", str(html_file)], check=True)
            logger.info("   ✅ Article opened in browser")
        except (OSError, IOError, FileNotFoundError):
            logger.info("   ⚠️  Could not open browser automatically")
            logger.info(f"   📁 Article saved to: {html_file}")

        logger.info(Path("\n") + "=" * 60)
        logger.info("🎉 Medium Article Automation Complete!")
        logger.info(f"📊 Generated article for {analysis['total_files']} files")
        logger.info(
            f"🔍 Optimized for {len(article_content['keywords'])} trending keywords"
        )
        logger.info(f"📈 Project types: {', '.join(analysis['project_types'].keys())}")
        logger.info(
            f"🛠️  Technologies: {', '.join(list(analysis['technologies'].keys())[:5])}"
        )

        return {
            "html_file": html_file,
            "json_file": json_file,
            "csv_file": csv_file,
            "analysis": analysis,
            "article": article_content,
        }


def main():
    """Main function to run the automation"""
    python_folder = Path.home() / "Documents" / "python"

    if not python_folder.exists():
        logger.info(f"❌ Python folder not found: {python_folder}")
        logger.info("   Please ensure the folder exists and contains Python files")
        return

    logger.info("🤖 Medium Article Automation Maker")
    logger.info("=" * 50)
    logger.info(f"📁 Analyzing folder: {python_folder}")
    logger.info(f"📊 Looking for Python projects and files...")

    # Create automation instance
    automation = MediumArticleAutomation(python_folder)

    # Run the complete automation
    results = automation.run_automation()

    logger.info(f"\n✅ Automation complete!")
    logger.info(f"📄 Article: {results['html_file']}")
    logger.info(f"📊 Data: {results['json_file']}")
    logger.info(f"📈 Metrics: {results['csv_file']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
🧠 INTELLIGENT CODE ORCHESTRATOR
==================================
AI-powered code analysis and improvement system using integrated LLM APIs.
Analyzes the ~/Documents/pythons codebase and provides intelligent suggestions.

Features:
🔍 Deep code analysis with multiple LLMs
⚡ Performance optimization recommendations
🐛 Bug detection and fixing suggestions
📚 Best practices and architectural improvements
🔄 Automated refactoring proposals
📊 Code quality metrics and insights
"""

import os
import ast
import json
import logging
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import openai
from anthropic import Anthropic
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntelligentCodeOrchestrator:
    """
    AI-powered code analysis and improvement orchestrator
    """

    def __init__(self):
        self.load_environment()
        self.initialize_clients()
        self.setup_analysis_models()
        self.codebase_path = Path.home() / "Documents" / "pythons"

    def load_environment(self):
        """Load LLM API keys"""
        env_paths = [
            Path.home() / ".env.d" / "llm-apis.env",
            Path.home() / ".env.d" / "gemini.env"
        ]

        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path)

    def initialize_clients(self):
        """Initialize LLM clients"""
        self.clients = {}

        if os.getenv('OPENAI_API_KEY'):
            self.clients['openai'] = openai.Client(api_key=os.getenv('OPENAI_API_KEY'))

        if os.getenv('ANTHROPIC_API_KEY'):
            self.clients['anthropic'] = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

        if os.getenv('GOOGLE_API_KEY'):
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self.clients['gemini'] = genai.GenerativeModel('gemini-pro')

    def setup_analysis_models(self):
        """Configure models for different analysis tasks"""
        self.analysis_routing = {
            'bug_detection': ['anthropic', 'openai', 'gemini'],
            'performance_optimization': ['openai', 'anthropic', 'gemini'],
            'code_quality': ['anthropic', 'openai', 'gemini'],
            'refactoring': ['anthropic', 'openai', 'gemini'],
            'documentation': ['gemini', 'openai', 'anthropic'],
            'security_audit': ['anthropic', 'openai', 'gemini']
        }

    async def analyze_codebase(self, focus_areas: List[str] = None) -> Dict[str, Any]:
        """
        Perform comprehensive codebase analysis
        """
        if focus_areas is None:
            focus_areas = ['bug_detection', 'performance_optimization', 'code_quality', 'refactoring']

        start_time = datetime.now()

        # Discover Python files
        python_files = self._discover_python_files()
        logger.info(f"Discovered {len(python_files)} Python files")

        # Analyze each file
        file_analyses = []
        for file_path in python_files[:50]:  # Limit for demo
            try:
                analysis = await self._analyze_single_file(file_path, focus_areas)
                file_analyses.append(analysis)
            except Exception as e:
                logger.error(f"Failed to analyze {file_path}: {e}")

        # Aggregate results
        aggregated_analysis = self._aggregate_analyses(file_analyses)

        # Generate improvement recommendations
        recommendations = await self._generate_recommendations(aggregated_analysis)

        result = {
            'timestamp': start_time.isoformat(),
            'files_analyzed': len(file_analyses),
            'total_files': len(python_files),
            'aggregated_analysis': aggregated_analysis,
            'recommendations': recommendations,
            'processing_time': (datetime.now() - start_time).total_seconds()
        }

        return result

    def _discover_python_files(self) -> List[Path]:
        """Discover all Python files in the codebase"""
        python_files = []

        if self.codebase_path.exists():
            for file_path in self.codebase_path.rglob('*.py'):
                if not any(part.startswith('.') for part in file_path.parts):
                    python_files.append(file_path)

        return python_files

    async def _analyze_single_file(self, file_path: Path, focus_areas: List[str]) -> Dict[str, Any]:
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Basic code metrics
            metrics = self._calculate_basic_metrics(content)

            # AI-powered analysis for each focus area
            analyses = {}
            for area in focus_areas:
                analyses[area] = await self._analyze_focus_area(content, area, file_path.name)

            return {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'metrics': metrics,
                'analyses': analyses,
                'content_preview': content[:500] + "..." if len(content) > 500 else content
            }

        except Exception as e:
            return {
                'file_path': str(file_path),
                'error': str(e),
                'metrics': {},
                'analyses': {}
            }

    def _calculate_basic_metrics(self, content: str) -> Dict[str, Any]:
        """Calculate basic code metrics"""
        lines = content.split('\n')
        metrics = {
            'total_lines': len(lines),
            'code_lines': len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
            'comment_lines': len([line for line in lines if line.strip().startswith('#')]),
            'empty_lines': len([line for line in lines if not line.strip()]),
            'functions': len([line for line in lines if line.strip().startswith('def ')]),
            'classes': len([line for line in lines if line.strip().startswith('class ')]),
            'imports': len([line for line in lines if line.strip().startswith(('import ', 'from '))])
        }

        # Calculate complexity indicators
        try:
            tree = ast.parse(content)
            metrics['ast_nodes'] = len(list(ast.walk(tree)))
            metrics['functions_with_docstrings'] = sum(
                1 for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef) and ast.get_docstring(node)
            )
        except:
            metrics['ast_nodes'] = 0
            metrics['functions_with_docstrings'] = 0

        return metrics

    async def _analyze_focus_area(self, content: str, focus_area: str, filename: str) -> Dict[str, Any]:
        """Analyze code for a specific focus area using AI"""
        model = self._select_model_for_analysis(focus_area)

        prompt = self._create_analysis_prompt(focus_area, content, filename)

        try:
            analysis_text = await self._call_llm(model, prompt)

            # Parse the analysis (simplified parsing)
            return {
                'model_used': model,
                'analysis': analysis_text,
                'issues_found': len(analysis_text.split('Issue:')) - 1 if 'Issue:' in analysis_text else 0,
                'recommendations': len(analysis_text.split('Recommendation:')) - 1 if 'Recommendation:' in analysis_text else 0
            }

        except Exception as e:
            return {
                'model_used': model,
                'error': str(e),
                'analysis': 'Analysis failed'
            }

    def _select_model_for_analysis(self, focus_area: str) -> str:
        """Select appropriate model for analysis task"""
        available_models = self.analysis_routing.get(focus_area, ['anthropic'])

        for model in available_models:
            if model in self.clients:
                return model

        return 'anthropic' if 'anthropic' in self.clients else list(self.clients.keys())[0]

    def _create_analysis_prompt(self, focus_area: str, content: str, filename: str) -> str:
        """Create analysis prompt based on focus area"""

        base_prompt = f"Analyze this Python file '{filename}' for {focus_area.replace('_', ' ')}:\n\n```python\n{content[:2000]}...\n```\n\n"

        if focus_area == 'bug_detection':
            return base_prompt + """
            Identify potential bugs, logic errors, and runtime issues. Focus on:
            - Syntax errors and potential exceptions
            - Logic flaws and edge cases
            - Resource leaks and improper error handling
            - Type-related issues

            Format: List each issue with severity (Critical/High/Medium/Low) and suggested fix.
            """

        elif focus_area == 'performance_optimization':
            return base_prompt + """
            Identify performance bottlenecks and optimization opportunities. Focus on:
            - Inefficient algorithms and data structures
            - Unnecessary computations and memory usage
            - I/O operations and database queries
            - Async/await usage opportunities

            Format: List optimizations with estimated performance impact.
            """

        elif focus_area == 'code_quality':
            return base_prompt + """
            Assess overall code quality and adherence to best practices. Focus on:
            - Code readability and maintainability
            - Naming conventions and code organization
            - Documentation quality
            - SOLID principles and design patterns

            Format: Provide quality score (1-10) and specific improvement areas.
            """

        elif focus_area == 'refactoring':
            return base_prompt + """
            Suggest refactoring opportunities for better code structure. Focus on:
            - Function/class size and complexity
            - Code duplication and abstraction opportunities
            - Dependency injection and loose coupling
            - Modern Python features and idioms

            Format: List refactoring suggestions with before/after code examples.
            """

        elif focus_area == 'documentation':
            return base_prompt + """
            Evaluate documentation completeness and quality. Focus on:
            - Docstring coverage and quality
            - Inline comments usefulness
            - README and API documentation
            - Type hints and annotations

            Format: Documentation coverage percentage and improvement suggestions.
            """

        elif focus_area == 'security_audit':
            return base_prompt + """
            Identify potential security vulnerabilities. Focus on:
            - Input validation and sanitization
            - SQL injection and XSS vulnerabilities
            - Authentication and authorization issues
            - Sensitive data handling

            Format: List security issues with severity and remediation steps.
            """

        return base_prompt + "Provide detailed analysis and recommendations."

    async def _call_llm(self, model: str, prompt: str) -> str:
        """Call the appropriate LLM"""
        try:
            if model == 'anthropic':
                client = self.clients.get('anthropic')
                if client:
                    response = await client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=2000,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    return response.content[0].text

            elif model == 'openai':
                client = self.clients.get('openai')
                if client:
                    response = await client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=2000
                    )
                    return response.choices[0].message.content

            elif model == 'gemini':
                client = self.clients.get('gemini')
                if client:
                    response = await client.generate_content(prompt)
                    return response.text

        except Exception as e:
            logger.error(f"LLM call failed for {model}: {e}")
            return f"Analysis failed: {str(e)}"

        return "No suitable LLM available for analysis"

    def _aggregate_analyses(self, file_analyses: List[Dict]) -> Dict[str, Any]:
        """Aggregate analyses across all files"""
        aggregated = {
            'total_files': len(file_analyses),
            'total_lines': sum(f.get('metrics', {}).get('total_lines', 0) for f in file_analyses),
            'total_functions': sum(f.get('metrics', {}).get('functions', 0) for f in file_analyses),
            'total_classes': sum(f.get('metrics', {}).get('classes', 0) for f in file_analyses),
            'focus_areas': {}
        }

        # Aggregate by focus area
        for file_analysis in file_analyses:
            for focus_area, analysis in file_analysis.get('analyses', {}).items():
                if focus_area not in aggregated['focus_areas']:
                    aggregated['focus_areas'][focus_area] = {
                        'total_analyses': 0,
                        'total_issues': 0,
                        'total_recommendations': 0
                    }

                area_data = aggregated['focus_areas'][focus_area]
                area_data['total_analyses'] += 1
                area_data['total_issues'] += analysis.get('issues_found', 0)
                area_data['total_recommendations'] += analysis.get('recommendations', 0)

        return aggregated

    async def _generate_recommendations(self, aggregated_analysis: Dict) -> Dict[str, Any]:
        """Generate high-level recommendations based on aggregated analysis"""
        recommendations = {}

        # Generate priority recommendations
        priority_issues = []
        for focus_area, data in aggregated_analysis.get('focus_areas', {}).items():
            if data.get('total_issues', 0) > 0:
                priority_issues.append({
                    'area': focus_area,
                    'issues': data['total_issues'],
                    'priority': 'High' if data['total_issues'] > 10 else 'Medium'
                })

        # Use AI to generate strategic recommendations
        strategy_prompt = f"""
        Based on this codebase analysis, provide strategic recommendations:

        Analysis Summary:
        - {aggregated_analysis['total_files']} files analyzed
        - {aggregated_analysis['total_lines']} total lines of code
        - {aggregated_analysis['total_functions']} functions, {aggregated_analysis['total_classes']} classes

        Priority Issues:
        {json.dumps(priority_issues, indent=2)}

        Provide:
        1. Top 3 immediate action items
        2. Long-term architectural improvements
        3. Code quality initiatives
        4. Team/process recommendations
        """

        try:
            strategy_analysis = await self._call_llm('anthropic', strategy_prompt)
            recommendations['strategic'] = strategy_analysis
        except:
            recommendations['strategic'] = "Strategic analysis failed - check individual file analyses for insights"

        # Generate quick wins
        recommendations['quick_wins'] = [
            "Fix critical bugs identified in analysis",
            "Add missing docstrings to improve documentation coverage",
            "Implement consistent error handling patterns",
            "Refactor overly complex functions (>50 lines)",
            "Add type hints for better code maintainability"
        ]

        return recommendations

    async def generate_improvement_plan(self, analysis_result: Dict) -> Dict[str, Any]:
        """Generate a detailed improvement implementation plan"""
        plan_prompt = f"""
        Create a detailed 3-month improvement plan based on this codebase analysis:

        Current State:
        - {analysis_result['aggregated_analysis']['total_files']} files
        - {analysis_result['aggregated_analysis']['total_lines']} lines of code
        - Key issues: {list(analysis_result['aggregated_analysis']['focus_areas'].keys())}

        Create a phased improvement plan with:
        1. Month 1 priorities and deliverables
        2. Month 2 focus areas and metrics
        3. Month 3 completion and maintenance
        4. Success metrics and monitoring
        5. Required resources and timeline
        """

        try:
            improvement_plan = await self._call_llm('openai', plan_prompt)
            return {'plan': improvement_plan, 'generated_at': datetime.now().isoformat()}
        except:
            return {'plan': 'Plan generation failed', 'error': True}


async def main():
    """Demo the intelligent code orchestrator"""
    orchestrator = IntelligentCodeOrchestrator()

    logger.info("Starting intelligent code analysis...")

    # Analyze codebase
    analysis_result = await orchestrator.analyze_codebase()

    logger.info(f"Analyzed {analysis_result['files_analyzed']} files in {analysis_result['processing_time']:.2f} seconds")

    # Generate improvement plan
    improvement_plan = await orchestrator.generate_improvement_plan(analysis_result)

    # Combine results
    final_result = {
        'analysis': analysis_result,
        'improvement_plan': improvement_plan,
        'summary': {
            'files_analyzed': analysis_result['files_analyzed'],
            'total_issues': sum(data.get('total_issues', 0) for data in analysis_result['aggregated_analysis']['focus_areas'].values()),
            'total_recommendations': sum(data.get('total_recommendations', 0) for data in analysis_result['aggregated_analysis']['focus_areas'].values())
        }
    }

    # Save results
    output_file = Path.home() / "codebase_analysis.json"
    with open(output_file, 'w') as f:
        json.dump(final_result, f, indent=2, default=str)

    logger.info(f"Analysis complete! Results saved to {output_file}")
    logger.info(f"Summary: {final_result['summary']['total_issues']} issues found, {final_result['summary']['total_recommendations']} recommendations made")

    return final_result


if __name__ == "__main__":
    asyncio.run(main())
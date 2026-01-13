#!/usr/bin/env python3
"""
Deep Research Tool - Core Analysis Engine
Comprehensive folder structure analysis with GitHub repo optimization and codex generation.
"""

import os
import sys
import json
import csv
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import mimetypes

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from analyzers.folder_analyzer import FolderAnalyzer
from analyzers.github_analyzer import GitHubAnalyzer
from analyzers.codex_analyzer import CodexAnalyzer
from exporters.csv_exporter import CSVExporter
from exporters.html_exporter import HTMLExporter
from exporters.json_exporter import JSONExporter
from visualizers.tree_visualizer import TreeVisualizer
from configs.codex_configs import CodexConfigGenerator

@dataclass
class AnalysisResult:
    """Container for analysis results."""
    total_files: int
    total_directories: int
    max_depth: int
    file_types: Dict[str, int]
    categories: Dict[str, int]
    size_by_category: Dict[str, int]
    depth_distribution: Dict[int, int]
    largest_files: List[Tuple[str, int]]
    duplicate_groups: Dict[str, List[str]]
    github_structure: Dict[str, Any]
    codex_configs: Dict[str, Any]
    analysis_timestamp: datetime
    root_path: str

class DeepResearcher:
    """Main deep research analysis engine."""
    
    def __init__(self, root_path: str, max_depth: int = 6, github_mode: bool = False):
        self.root_path = Path(root_path).resolve()
        self.max_depth = max_depth
        self.github_mode = github_mode
        self.analyzers = {
            'folder': FolderAnalyzer(self.root_path, max_depth),
            'github': GitHubAnalyzer(self.root_path) if github_mode else None,
            'codex': CodexAnalyzer(self.root_path)
        }
        self.exporters = {
            'csv': CSVExporter(),
            'html': HTMLExporter(),
            'json': JSONExporter()
        }
        self.visualizer = TreeVisualizer()
        self.codex_generator = CodexConfigGenerator()
        
    def analyze(self) -> AnalysisResult:
        """Perform comprehensive deep analysis."""
        print(f"🔍 Starting deep research analysis...")
        print(f"📁 Root path: {self.root_path}")
        print(f"📏 Max depth: {self.max_depth}")
        print(f"🐙 GitHub mode: {self.github_mode}")
        print("=" * 60)
        
        # Step 1: Basic folder analysis
        print("\n📊 Step 1: Analyzing folder structure...")
        folder_data = self.analyzers['folder'].analyze()
        
        # Step 2: GitHub structure analysis (if enabled)
        github_data = {}
        if self.github_mode and self.analyzers['github']:
            print("\n🐙 Step 2: Analyzing GitHub repository structure...")
            github_data = self.analyzers['github'].analyze()
        
        # Step 3: Codex configuration analysis
        print("\n🤖 Step 3: Analyzing codex configurations...")
        codex_data = self.analyzers['codex'].analyze()
        
        # Step 4: Generate codex configs
        print("\n⚙️  Step 4: Generating codex configurations...")
        codex_configs = self.codex_generator.generate_configs(folder_data, github_data, codex_data)
        
        # Compile results
        result = AnalysisResult(
            total_files=folder_data['total_files'],
            total_directories=folder_data['total_directories'],
            max_depth=folder_data['max_depth'],
            file_types=folder_data['file_types'],
            categories=folder_data['categories'],
            size_by_category=folder_data['size_by_category'],
            depth_distribution=folder_data['depth_distribution'],
            largest_files=folder_data['largest_files'],
            duplicate_groups=folder_data['duplicate_groups'],
            github_structure=github_data,
            codex_configs=codex_configs,
            analysis_timestamp=datetime.now(),
            root_path=str(self.root_path)
        )
        
        print(f"\n✅ Analysis complete!")
        print(f"   📁 Files analyzed: {result.total_files:,}")
        print(f"   📂 Directories: {result.total_directories:,}")
        print(f"   📏 Max depth reached: {result.max_depth}")
        print(f"   🔄 Duplicate groups: {len(result.duplicate_groups)}")
        
        return result
    
    def export_results(self, result: AnalysisResult, formats: List[str], output_dir: str = None):
        """Export analysis results in specified formats."""
        if output_dir is None:
            output_dir = self.root_path / "deep_research_output"
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"\n📤 Exporting results to: {output_path}")
        
        for format_type in formats:
            if format_type in self.exporters:
                print(f"   📄 Exporting {format_type.upper()}...")
                self.exporters[format_type].export(result, output_path)
            else:
                print(f"   ⚠️  Unknown format: {format_type}")
        
        # Generate HTML visualization
        if 'html' in formats:
            print("   🌐 Generating interactive visualization...")
            self.visualizer.generate_html_tree(result, output_path)
    
    def generate_github_structure(self, result: AnalysisResult, output_dir: str = None):
        """Generate optimized GitHub repository structure."""
        if output_dir is None:
            output_dir = self.root_path / "github_structure"
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"\n🐙 Generating GitHub repository structure...")
        print(f"   📁 Output directory: {output_path}")
        
        # Generate repository structure files
        self._generate_readme(result, output_path)
        self._generate_gitignore(result, output_path)
        self._generate_github_workflows(result, output_path)
        self._generate_issue_templates(result, output_path)
        self._generate_contributing_guide(result, output_path)
        
        print("   ✅ GitHub structure generated!")
    
    def _generate_readme(self, result: AnalysisResult, output_path: Path):
        """Generate README.md for the repository."""
        readme_content = f"""# {result.root_path.name}

## Project Overview

This repository contains {result.total_files:,} files across {result.total_directories:,} directories.

### File Distribution

| Category | Count | Size |
|----------|-------|------|
"""
        
        for category, count in sorted(result.categories.items(), key=lambda x: x[1], reverse=True):
            size_mb = result.size_by_category.get(category, 0) / (1024 * 1024)
            readme_content += f"| {category} | {count:,} | {size_mb:.1f} MB |\n"
        
        readme_content += f"""
### Top File Types

"""
        for ext, count in sorted(result.file_types.items(), key=lambda x: x[1], reverse=True)[:10]:
            readme_content += f"- `.{ext}`: {count:,} files\n"
        
        readme_content += f"""
### Repository Structure

```
{self._generate_tree_structure(result)}
```

## Analysis Details

- **Analysis Date**: {result.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}
- **Root Path**: `{result.root_path}`
- **Max Depth**: {result.max_depth}
- **Duplicate Groups**: {len(result.duplicate_groups)}

## Generated by Deep Research Tool

This repository structure was generated using the Deep Research Tool for intelligent folder analysis and GitHub optimization.
"""
        
        with open(output_path / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def _generate_gitignore(self, result: AnalysisResult, output_path: Path):
        """Generate .gitignore based on file analysis."""
        gitignore_content = """# Deep Research Tool Generated .gitignore

# Common temporary files
*.tmp
*.temp
*.log
*.cache

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
build/
dist/
*.egg-info/

# Data files (based on analysis)
*.csv
*.json
*.xml
*.yaml
*.yml

# Large files (based on analysis)
"""
        
        # Add specific patterns based on analysis
        large_extensions = set()
        for file_path, size in result.largest_files[:20]:
            ext = Path(file_path).suffix.lower()
            if ext and size > 10 * 1024 * 1024:  # > 10MB
                large_extensions.add(ext)
        
        for ext in large_extensions:
            gitignore_content += f"*{ext}\n"
        
        with open(output_path / ".gitignore", 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
    
    def _generate_github_workflows(self, result: AnalysisResult, output_path: Path):
        """Generate GitHub Actions workflows."""
        workflows_dir = output_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # Main CI workflow
        ci_workflow = """name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Run analysis
      run: |
        python src/core/deep_researcher.py --path . --depth 6
"""
        
        with open(workflows_dir / "ci.yml", 'w', encoding='utf-8') as f:
            f.write(ci_workflow)
    
    def _generate_issue_templates(self, result: AnalysisResult, output_path: Path):
        """Generate GitHub issue templates."""
        issue_dir = output_path / ".github" / "ISSUE_TEMPLATE"
        issue_dir.mkdir(parents=True, exist_ok=True)
        
        bug_template = """---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. macOS, Windows, Linux]
 - Python version: [e.g. 3.9.0]
 - Deep Research Tool version: [e.g. 1.0.0]

**Additional context**
Add any other context about the problem here.
"""
        
        with open(issue_dir / "bug_report.md", 'w', encoding='utf-8') as f:
            f.write(bug_template)
    
    def _generate_contributing_guide(self, result: AnalysisResult, output_path: Path):
        """Generate CONTRIBUTING.md guide."""
        contributing_content = """# Contributing to Deep Research Tool

Thank you for your interest in contributing to the Deep Research Tool!

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/deep-research-tool.git`
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests: `python -m pytest tests/`

## Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write docstrings for all public functions
- Run `black` for code formatting
- Run `flake8` for linting

## Testing

- Write tests for new features
- Ensure all tests pass: `python -m pytest`
- Aim for high test coverage

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Add tests if applicable
4. Update documentation if needed
5. Submit a pull request

## Reporting Issues

Use the GitHub issue tracker to report bugs or request features.
"""
        
        with open(output_path / "CONTRIBUTING.md", 'w', encoding='utf-8') as f:
            f.write(contributing_content)
    
    def _generate_tree_structure(self, result: AnalysisResult, max_depth: int = 3) -> str:
        """Generate ASCII tree structure."""
        # This is a simplified version - in practice, you'd want more sophisticated tree generation
        tree_lines = []
        tree_lines.append(f"{result.root_path.name}/")
        
        # Add some sample structure based on categories
        for category, count in sorted(result.categories.items(), key=lambda x: x[1], reverse=True)[:5]:
            tree_lines.append(f"├── {category}/ ({count:,} files)")
        
        if len(result.categories) > 5:
            tree_lines.append(f"└── ... ({len(result.categories) - 5} more categories)")
        
        return "\n".join(tree_lines)

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Deep Research Tool - Intelligent folder analysis")
    parser.add_argument("--path", "-p", required=True, help="Root path to analyze")
    parser.add_argument("--depth", "-d", type=int, default=6, help="Maximum depth to analyze")
    parser.add_argument("--github-mode", action="store_true", help="Enable GitHub repository analysis")
    parser.add_argument("--export", "-e", nargs="+", default=["csv", "html", "json"], 
                       choices=["csv", "html", "json", "markdown"], help="Export formats")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--generate-github", action="store_true", help="Generate GitHub repository structure")
    
    args = parser.parse_args()
    
    # Initialize researcher
    researcher = DeepResearcher(
        root_path=args.path,
        max_depth=args.depth,
        github_mode=args.github_mode
    )
    
    # Run analysis
    result = researcher.analyze()
    
    # Export results
    researcher.export_results(result, args.export, args.output)
    
    # Generate GitHub structure if requested
    if args.generate_github:
        researcher.generate_github_structure(result, args.output)
    
    print("\n🎉 Deep research analysis complete!")
    print("📊 Check the output directory for detailed results and visualizations.")

if __name__ == "__main__":
    main()
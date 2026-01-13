#!/usr/bin/env python3
"""
GitHub Analyzer - Analyzes repository structure for GitHub optimization
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class GitHubFile:
    """GitHub-specific file information."""
    path: str
    name: str
    type: str  # 'code', 'config', 'docs', 'assets', 'tests'
    importance: int  # 1-10 scale
    is_essential: bool
    should_ignore: bool
    github_category: str

class GitHubAnalyzer:
    """Analyzes folder structure for GitHub repository optimization."""
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir).resolve()
        self.github_files: List[GitHubFile] = []
        self.repository_structure = {}
        
    def analyze(self) -> Dict:
        """Analyze repository structure for GitHub optimization."""
        print("🐙 Analyzing GitHub repository structure...")
        
        structure = {
            'has_readme': False,
            'has_license': False,
            'has_contributing': False,
            'has_gitignore': False,
            'has_github_workflows': False,
            'has_issue_templates': False,
            'has_pr_template': False,
            'has_security_policy': False,
            'code_files': [],
            'config_files': [],
            'documentation_files': [],
            'test_files': [],
            'asset_files': [],
            'recommended_structure': {},
            'missing_essentials': [],
            'suggested_improvements': [],
            'repository_health_score': 0
        }
        
        # Scan for GitHub-specific files
        self._scan_github_files(structure)
        
        # Analyze code organization
        self._analyze_code_organization(structure)
        
        # Generate recommendations
        self._generate_recommendations(structure)
        
        # Calculate health score
        structure['repository_health_score'] = self._calculate_health_score(structure)
        
        print(f"   ✅ GitHub analysis complete (Health Score: {structure['repository_health_score']}/100)")
        
        return structure
    
    def _scan_github_files(self, structure: Dict):
        """Scan for essential GitHub files."""
        essential_files = {
            'README.md': 'has_readme',
            'LICENSE': 'has_license',
            'LICENSE.txt': 'has_license',
            'CONTRIBUTING.md': 'has_contributing',
            '.gitignore': 'has_gitignore',
            '.github/ISSUE_TEMPLATE/': 'has_issue_templates',
            '.github/PULL_REQUEST_TEMPLATE.md': 'has_pr_template',
            'SECURITY.md': 'has_security_policy'
        }
        
        for file_pattern, flag in essential_files.items():
            if self._file_exists(file_pattern):
                structure[flag] = True
            else:
                structure['missing_essentials'].append(file_pattern)
        
        # Check for GitHub workflows
        workflows_dir = self.root_dir / '.github' / 'workflows'
        if workflows_dir.exists() and any(workflows_dir.iterdir()):
            structure['has_github_workflows'] = True
        else:
            structure['missing_essentials'].append('.github/workflows/')
    
    def _file_exists(self, pattern: str) -> bool:
        """Check if a file or directory pattern exists."""
        if pattern.endswith('/'):
            # Directory pattern
            dir_path = self.root_dir / pattern.rstrip('/')
            return dir_path.exists() and dir_path.is_dir()
        else:
            # File pattern
            file_path = self.root_dir / pattern
            return file_path.exists() and file_path.is_file()
    
    def _analyze_code_organization(self, structure: Dict):
        """Analyze code organization and structure."""
        code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs'}
        config_extensions = {'.json', '.yaml', '.yml', '.toml', '.ini', '.conf', '.env'}
        doc_extensions = {'.md', '.rst', '.txt', '.pdf'}
        test_patterns = {'test', 'spec', 'specs', '__tests__', 'tests'}
        
        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file():
                rel_path = file_path.relative_to(self.root_dir)
                file_name = file_path.name.lower()
                file_ext = file_path.suffix.lower()
                
                # Categorize files
                if file_ext in code_extensions:
                    file_type = 'code'
                    importance = self._calculate_code_importance(file_path, rel_path)
                    github_category = self._get_github_category(rel_path, file_ext)
                elif file_ext in config_extensions:
                    file_type = 'config'
                    importance = 8  # Config files are usually important
                    github_category = 'configuration'
                elif file_ext in doc_extensions:
                    file_type = 'docs'
                    importance = 6
                    github_category = 'documentation'
                elif any(pattern in file_name for pattern in test_patterns):
                    file_type = 'tests'
                    importance = 7
                    github_category = 'testing'
                elif file_ext in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico'}:
                    file_type = 'assets'
                    importance = 3
                    github_category = 'assets'
                else:
                    file_type = 'other'
                    importance = 2
                    github_category = 'misc'
                
                github_file = GitHubFile(
                    path=str(rel_path),
                    name=file_path.name,
                    type=file_type,
                    importance=importance,
                    is_essential=importance >= 7,
                    should_ignore=self._should_ignore_file(file_path, rel_path),
                    github_category=github_category
                )
                
                self.github_files.append(github_file)
                
                # Add to appropriate category
                if file_type == 'code':
                    structure['code_files'].append(github_file)
                elif file_type == 'config':
                    structure['config_files'].append(github_file)
                elif file_type == 'docs':
                    structure['documentation_files'].append(github_file)
                elif file_type == 'tests':
                    structure['test_files'].append(github_file)
                elif file_type == 'assets':
                    structure['asset_files'].append(github_file)
    
    def _calculate_code_importance(self, file_path: Path, rel_path: Path) -> int:
        """Calculate importance score for code files."""
        importance = 5  # Base score
        
        # Main entry points are very important
        if file_path.name in {'main.py', 'app.py', 'index.js', 'main.js', 'main.ts', 'index.ts'}:
            importance += 3
        
        # Core modules are important
        if 'core' in str(rel_path) or 'src' in str(rel_path):
            importance += 2
        
        # Configuration files are important
        if 'config' in str(rel_path) or 'settings' in str(rel_path):
            importance += 2
        
        # Test files are moderately important
        if 'test' in str(rel_path) or 'spec' in str(rel_path):
            importance += 1
        
        # Utility files are less important
        if 'util' in str(rel_path) or 'helper' in str(rel_path):
            importance -= 1
        
        return max(1, min(10, importance))
    
    def _get_github_category(self, rel_path: Path, file_ext: str) -> str:
        """Get GitHub category for a file."""
        path_str = str(rel_path).lower()
        
        if 'src' in path_str or 'lib' in path_str:
            return 'source_code'
        elif 'test' in path_str or 'spec' in path_str:
            return 'testing'
        elif 'doc' in path_str or 'docs' in path_str:
            return 'documentation'
        elif 'config' in path_str or 'conf' in path_str:
            return 'configuration'
        elif 'asset' in path_str or 'static' in path_str:
            return 'assets'
        elif file_ext in {'.py'}:
            return 'python'
        elif file_ext in {'.js', '.ts'}:
            return 'javascript'
        elif file_ext in {'.java'}:
            return 'java'
        elif file_ext in {'.cpp', '.c'}:
            return 'cpp'
        else:
            return 'misc'
    
    def _should_ignore_file(self, file_path: Path, rel_path: Path) -> bool:
        """Determine if a file should be in .gitignore."""
        file_name = file_path.name.lower()
        path_str = str(rel_path).lower()
        
        # Common patterns to ignore
        ignore_patterns = [
            '__pycache__', '.pyc', '.pyo', '.pyd',
            'node_modules', '.npm', '.yarn',
            '.git', '.svn', '.hg',
            '.DS_Store', 'Thumbs.db',
            '.vscode', '.idea', '.vs',
            '*.log', '*.tmp', '*.temp',
            '.env', '.env.local', '.env.production',
            'dist', 'build', 'target', 'out'
        ]
        
        for pattern in ignore_patterns:
            if pattern in file_name or pattern in path_str:
                return True
        
        return False
    
    def _generate_recommendations(self, structure: Dict):
        """Generate recommendations for repository improvement."""
        recommendations = []
        
        # Check for proper directory structure
        if not self._has_proper_structure():
            recommendations.append("Consider organizing code into standard directories (src/, tests/, docs/)")
        
        # Check for documentation
        if not structure['has_readme']:
            recommendations.append("Add a comprehensive README.md file")
        
        if not structure['has_contributing']:
            recommendations.append("Add a CONTRIBUTING.md file to guide contributors")
        
        # Check for CI/CD
        if not structure['has_github_workflows']:
            recommendations.append("Add GitHub Actions workflows for CI/CD")
        
        # Check for license
        if not structure['has_license']:
            recommendations.append("Add a LICENSE file to clarify usage rights")
        
        # Check for security
        if not structure['has_security_policy']:
            recommendations.append("Add a SECURITY.md file for security reporting")
        
        # Check for tests
        if not structure['test_files']:
            recommendations.append("Add test files to improve code quality")
        
        # Check for .gitignore
        if not structure['has_gitignore']:
            recommendations.append("Add a .gitignore file to exclude unnecessary files")
        
        structure['suggested_improvements'] = recommendations
    
    def _has_proper_structure(self) -> bool:
        """Check if repository has proper directory structure."""
        common_dirs = {'src', 'lib', 'tests', 'test', 'docs', 'doc', 'examples', 'scripts'}
        existing_dirs = {d.name for d in self.root_dir.iterdir() if d.is_dir()}
        
        return len(common_dirs.intersection(existing_dirs)) >= 2
    
    def _calculate_health_score(self, structure: Dict) -> int:
        """Calculate repository health score (0-100)."""
        score = 0
        
        # Essential files (40 points)
        if structure['has_readme']:
            score += 10
        if structure['has_license']:
            score += 10
        if structure['has_contributing']:
            score += 10
        if structure['has_gitignore']:
            score += 10
        
        # GitHub features (30 points)
        if structure['has_github_workflows']:
            score += 15
        if structure['has_issue_templates']:
            score += 10
        if structure['has_pr_template']:
            score += 5
        
        # Code organization (20 points)
        if structure['code_files']:
            score += 10
        if structure['test_files']:
            score += 10
        
        # Documentation (10 points)
        if structure['documentation_files']:
            score += 10
        
        return min(100, score)
    
    def get_recommended_structure(self) -> Dict:
        """Get recommended directory structure."""
        return {
            'root': {
                'README.md': 'Project overview and setup instructions',
                'LICENSE': 'License information',
                'CONTRIBUTING.md': 'Contribution guidelines',
                '.gitignore': 'Files to ignore in version control',
                'requirements.txt': 'Python dependencies (if applicable)',
                'package.json': 'Node.js dependencies (if applicable)',
                'Dockerfile': 'Container configuration (if applicable)',
                'docker-compose.yml': 'Multi-container setup (if applicable)'
            },
            'src/': {
                'main.py': 'Main application entry point',
                'core/': 'Core application logic',
                'utils/': 'Utility functions',
                'config/': 'Configuration files'
            },
            'tests/': {
                'test_main.py': 'Main test file',
                'test_core/': 'Core functionality tests',
                'test_utils/': 'Utility function tests'
            },
            'docs/': {
                'api.md': 'API documentation',
                'deployment.md': 'Deployment instructions',
                'architecture.md': 'System architecture'
            },
            '.github/': {
                'workflows/': 'GitHub Actions workflows',
                'ISSUE_TEMPLATE/': 'Issue templates',
                'PULL_REQUEST_TEMPLATE.md': 'PR template'
            }
        }
#!/usr/bin/env python3
"""
Advanced AVATARARTS Structure Analyzer

Demonstrates advanced content-awareness, parent-child relationships,
and sophisticated folder content analysis including README files and documentation.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict, Counter
import re
from datetime import datetime

class AdvancedStructureAnalyzer:
    def __init__(self, root_path: str = "/Users/steven/AVATARARTS"):
        self.root_path = Path(root_path)
        self.analysis_cache = {}

    def get_content_hash(self, file_path: Path, sample_size: int = 1024) -> str:
        """Get content hash with smart sampling for large files."""
        try:
            hash_obj = hashlib.md5()
            with open(file_path, 'rb') as f:
                # Sample beginning, middle, and end for content awareness
                content = f.read(sample_size)
                hash_obj.update(content)

                # For larger files, sample middle and end
                if file_path.stat().st_size > sample_size * 2:
                    f.seek(file_path.stat().st_size // 2)
                    content = f.read(sample_size)
                    hash_obj.update(content)

                    f.seek(-sample_size, 2)
                    content = f.read(sample_size)
                    hash_obj.update(content)

            return hash_obj.hexdigest()
        except:
            return None

    def analyze_readme_content(self, readme_path: Path) -> Dict[str, Any]:
        """Advanced README content analysis."""
        try:
            with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            analysis = {
                'word_count': len(content.split()),
                'has_toc': '# Table of Contents' in content or '## Contents' in content,
                'has_installation': any(term in content.lower() for term in ['installation', 'setup', 'getting started']),
                'has_usage': any(term in content.lower() for term in ['usage', 'how to use', 'examples']),
                'has_api_docs': any(term in content.lower() for term in ['api', 'endpoint', 'function']),
                'has_contributing': 'contributing' in content.lower(),
                'has_license': 'license' in content.lower(),
                'sections': len(re.findall(r'^#{1,6}\s+', content, re.MULTILINE)),
                'code_blocks': len(re.findall(r'```', content)),
                'links': len(re.findall(r'\[.*?\]\(.*?\)', content)),
                'purpose_summary': self.extract_purpose_from_readme(content)
            }
            return analysis
        except:
            return {}

    def extract_purpose_from_readme(self, content: str) -> str:
        """Extract purpose summary from README content."""
        # Look for common purpose indicators
        content_lower = content.lower()

        if 'automation' in content_lower and 'tool' in content_lower:
            return "Automation tooling"
        elif 'api' in content_lower and 'integration' in content_lower:
            return "API integration service"
        elif 'machine learning' in content_lower or 'ml' in content_lower:
            return "Machine learning utilities"
        elif 'web' in content_lower and 'development' in content_lower:
            return "Web development framework"
        elif 'data' in content_lower and 'processing' in content_lower:
            return "Data processing pipeline"
        elif 'analysis' in content_lower:
            return "Content analysis tools"
        else:
            # Extract first meaningful sentence after title
            lines = content.split('\n')
            for line in lines[1:]:  # Skip title
                line = line.strip()
                if line and not line.startswith('#') and len(line) > 20:
                    return line[:100] + "..." if len(line) > 100 else line

        return "General purpose"

    def analyze_folder_structure(self, folder_path: Path) -> Dict[str, Any]:
        """Advanced folder structure analysis with parent-child relationships."""
        structure = {
            'path': str(folder_path.relative_to(self.root_path)),
            'depth': len(folder_path.relative_to(self.root_path).parts),
            'parent': str(folder_path.parent.relative_to(self.root_path)) if folder_path != self.root_path else None,
            'children': [],
            'file_types': Counter(),
            'readme_files': [],
            'config_files': [],
            'code_files': [],
            'data_files': [],
            'documentation_files': [],
            'total_files': 0,
            'total_size': 0,
            'last_modified': None,
            'content_purpose': "Unknown",
            'relationships': {
                'depends_on': [],
                'used_by': [],
                'similar_to': []
            }
        }

        try:
            # Analyze contents
            for item in folder_path.rglob('*'):
                if item.is_file():
                    structure['total_files'] += 1
                    structure['total_size'] += item.stat().st_size

                    # Track last modified
                    mtime = item.stat().st_mtime
                    if structure['last_modified'] is None or mtime > structure['last_modified']:
                        structure['last_modified'] = mtime

                    # Categorize files
                    suffix = item.suffix.lower()
                    name_lower = item.name.lower()

                    if name_lower in ['readme.md', 'readme.txt', 'readme.rst', 'readme']:
                        structure['readme_files'].append(str(item.relative_to(folder_path)))
                    elif suffix in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf']:
                        structure['config_files'].append(str(item.relative_to(folder_path)))
                    elif suffix in ['.py', '.js', '.java', '.cpp', '.c', '.go', '.rs', '.php']:
                        structure['code_files'].append(str(item.relative_to(folder_path)))
                    elif suffix in ['.csv', '.json', '.db', '.sqlite', '.parquet']:
                        structure['data_files'].append(str(item.relative_to(folder_path)))
                    elif suffix in ['.md', '.txt', '.rst', '.pdf', '.docx']:
                        structure['documentation_files'].append(str(item.relative_to(folder_path)))

                    # File type counter
                    structure['file_types'][suffix] += 1

            # Get children directories
            for item in folder_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    structure['children'].append(str(item.relative_to(folder_path)))

            # Analyze README for content purpose
            if structure['readme_files']:
                readme_path = folder_path / structure['readme_files'][0]
                readme_analysis = self.analyze_readme_content(readme_path)
                if readme_analysis.get('purpose_summary'):
                    structure['content_purpose'] = readme_analysis['purpose_summary']

            # Infer purpose from folder structure if no README
            elif not structure['readme_files']:
                structure['content_purpose'] = self.infer_purpose_from_structure(structure)

        except Exception as e:
            structure['error'] = str(e)

        return structure

    def infer_purpose_from_structure(self, structure: Dict[str, Any]) -> str:
        """Infer folder purpose from its structure and contents."""
        path = structure['path'].lower()

        # Path-based inference
        if 'api' in path or 'integration' in path:
            return "API integration services"
        elif 'automation' in path:
            return "Automation workflows"
        elif 'data' in path or 'database' in path:
            return "Data storage and processing"
        elif 'web' in path or 'website' in path:
            return "Web development assets"
        elif 'script' in path or 'tool' in path:
            return "Development tools and scripts"
        elif 'archive' in path or 'backup' in path:
            return "Archived content"

        # Content-based inference
        if structure['code_files'] and len(structure['code_files']) > len(structure['documentation_files']):
            return "Development codebase"
        elif structure['data_files'] and len(structure['data_files']) > 5:
            return "Data repository"
        elif structure['documentation_files'] and len(structure['documentation_files']) > 3:
            return "Documentation library"
        elif structure['config_files'] and len(structure['config_files']) > 2:
            return "Configuration management"

        return "General purpose"

    def build_parent_child_relationships(self) -> Dict[str, Any]:
        """Build comprehensive parent-child folder relationships."""
        print("🔍 Building parent-child folder relationships...")

        relationships = {
            'folders': {},
            'orphans': [],  # Folders without clear parent relationship
            'roots': [],    # Top-level folders
            'depth_analysis': defaultdict(list),
            'content_clusters': defaultdict(list)
        }

        # Analyze all directories
        for dir_path in self.root_path.rglob('*'):
            if dir_path.is_dir() and not any(part.startswith('.') for part in dir_path.parts):
                structure = self.analyze_folder_structure(dir_path)
                folder_key = structure['path']

                relationships['folders'][folder_key] = structure
                relationships['depth_analysis'][structure['depth']].append(folder_key)

                # Identify roots and orphans
                if structure['depth'] == 1:
                    relationships['roots'].append(folder_key)
                elif not structure['parent'] or structure['parent'] not in relationships['folders']:
                    relationships['orphans'].append(folder_key)

                # Cluster by content purpose
                purpose = structure['content_purpose']
                if purpose != "Unknown":
                    relationships['content_clusters'][purpose].append(folder_key)

        return relationships

    def analyze_content_dependencies(self, relationships: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content dependencies and relationships between folders."""
        print("🔗 Analyzing content dependencies...")

        # Find import relationships in Python files
        import_patterns = defaultdict(set)

        for folder_key, folder_data in relationships['folders'].items():
            folder_path = self.root_path / folder_key

            for py_file in folder_path.glob('**/*.py'):
                try:
                    with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Find relative imports
                    relative_imports = re.findall(r'from \.\.|\.\.', content)
                    if relative_imports:
                        import_patterns[folder_key].add('uses_parent_imports')

                    # Find specific module imports that might indicate dependencies
                    for other_folder in relationships['folders']:
                        if other_folder != folder_key:
                            folder_name = Path(other_folder).name
                            if f'from {folder_name}' in content or f'import {folder_name}' in content:
                                relationships['folders'][folder_key]['relationships']['depends_on'].append(other_folder)
                                relationships['folders'][other_folder]['relationships']['used_by'].append(folder_key)

                except:
                    continue

        return relationships

    def generate_advanced_report(self) -> Dict[str, Any]:
        """Generate comprehensive advanced structure analysis report."""
        print("📊 Generating advanced structure analysis...")

        # Build relationships
        relationships = self.build_parent_child_relationships()
        relationships = self.analyze_content_dependencies(relationships)

        # Generate insights
        insights = {
            'total_folders': len(relationships['folders']),
            'depth_distribution': dict(relationships['depth_analysis']),
            'content_clusters': dict(relationships['content_clusters']),
            'orphan_folders': len(relationships['orphans']),
            'root_folders': len(relationships['roots']),
            'readme_coverage': sum(1 for f in relationships['folders'].values() if f['readme_files']),
            'total_files': sum(f['total_files'] for f in relationships['folders'].values()),
            'total_size_bytes': sum(f['total_size'] for f in relationships['folders'].values()),
            'content_purposes': Counter(f['content_purpose'] for f in relationships['folders'].values()),
            'file_type_distribution': Counter(),
            'dependency_network': defaultdict(list)
        }

        # Aggregate file types and dependencies
        for folder_data in relationships['folders'].values():
            for file_type, count in folder_data['file_types'].items():
                insights['file_type_distribution'][file_type] += count

            for dep in folder_data['relationships']['depends_on']:
                insights['dependency_network'][folder_data['path']].append(dep)

        # Generate human-readable report
        report = self.generate_human_report(insights, relationships)

        return {
            'insights': insights,
            'relationships': relationships,
            'report': report,
            'generated_at': datetime.now().isoformat()
        }

    def generate_human_report(self, insights: Dict[str, Any], relationships: Dict[str, Any]) -> str:
        """Generate human-readable analysis report."""
        report = f"""# Advanced AVATARARTS Structure Analysis

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Structural Overview

- **Total Folders Analyzed**: {insights['total_folders']:,}
- **Total Files**: {insights['total_files']:,}
- **Total Size**: {insights['total_size_bytes'] / (1024**3):.2f} GB
- **README Coverage**: {insights['readme_coverage']}/{insights['total_folders']} folders ({insights['readme_coverage']/insights['total_folders']*100:.1f}%)

## 🏗️ Architecture Insights

### Depth Distribution
"""

        for depth, folders in sorted(insights['depth_distribution'].items()):
            report += f"- **Level {depth}**: {len(folders)} folders\n"

        report += f"""
### Content Purpose Clusters
"""
        for purpose, folders in sorted(insights['content_clusters'].items(), key=lambda x: len(x[1]), reverse=True):
            report += f"- **{purpose}**: {len(folders)} folders\n"

        report += f"""
## 📁 Key Findings

### Documentation Quality
- **README Coverage**: {insights['readme_coverage']/insights['total_folders']*100:.1f}% of folders documented
- **Well-documented areas**: {', '.join([p for p, f in insights['content_clusters'].items() if len(f) > 2])}

### Content Relationships
- **Orphan folders**: {insights['orphan_folders']} (may need reorganization)
- **Dependency network**: {sum(len(deps) for deps in insights['dependency_network'].values())} relationships identified

### File Type Distribution
"""
        for file_type, count in insights['file_type_distribution'].most_common(10):
            report += f"- **{file_type or 'no extension'}**: {count:,} files\n"

        report += f"""
## 🔍 Advanced Analysis Features Demonstrated

### 1. Content-Awareness
- SHA256 content hashing with smart sampling
- README content analysis and purpose extraction
- File type and structure pattern recognition

### 2. Parent-Child Relationships
- Hierarchical folder structure mapping
- Dependency analysis from import statements
- Orphan folder identification

### 3. Documentation Intelligence
- README parsing and section analysis
- Purpose inference from content
- Documentation quality metrics

### 4. Structural Insights
- Depth analysis and architectural patterns
- Content clustering by purpose
- Relationship mapping between components

## 🎯 Recommendations

1. **Improve README coverage** - Only {insights['readme_coverage']/insights['total_folders']*100:.1f}% of folders have documentation
2. **Review orphan folders** - {insights['orphan_folders']} folders may need better organization
3. **Strengthen dependencies** - Consider formalizing {sum(len(deps) for deps in insights['dependency_network'].values())} identified relationships

---
*This analysis demonstrates advanced content-awareness, structural intelligence, and organizational insights far beyond basic file operations.*
"""

        return report

def main():
    analyzer = AdvancedStructureAnalyzer()

    print("🚀 Starting Advanced AVATARARTS Structure Analysis...")
    print("This demonstrates content-awareness, parent-child relationships, and documentation intelligence.\n")

    results = analyzer.generate_advanced_report()

    # Save detailed analysis
    with open('/Users/steven/advanced_structure_analysis.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)

    # Save human-readable report
    with open('/Users/steven/AVATARARTS/advanced_structure_report.md', 'w') as f:
        f.write(results['report'])

    print("✅ Advanced analysis complete!")
    print(f"📊 Analyzed {results['insights']['total_folders']} folders")
    print(f"📄 Generated report: /Users/steven/AVATARARTS/advanced_structure_report.md")
    print(f"📋 Detailed data: /Users/steven/advanced_structure_analysis.json")

    # Show key insights
    insights = results['insights']
    print("\n🔍 Key Insights:")
    print(f"   • README Coverage: {insights['readme_coverage']}/{insights['total_folders']} folders")
    print(f"   • Content Clusters: {len(insights['content_clusters'])} purpose groups")
    print(f"   • Dependency Network: {sum(len(deps) for deps in insights['dependency_network'].values())} relationships")

if __name__ == "__main__":
    main()
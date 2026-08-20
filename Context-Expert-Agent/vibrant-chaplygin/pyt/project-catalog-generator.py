#!/usr/bin/env python3
"""
🏗️ ADVANCED SYSTEMS CATALOG
============================

Discovers and catalogs ALL advanced systems across:
- ~/pythons (Python automation scripts)
- ~/workspace (Web apps, APIs, full-stack projects)
- ~/ai-sites (AI-powered websites)
- ~/GitHub (Git repositories)
- ~/Documents (Projects and documentation)

Creates:
1. SYSTEMS_CATALOG.csv - Complete catalog with tech stack
2. SYSTEMS_INDEX.md - Markdown index with links
3. Sphinx documentation integration
4. Deployment readiness assessment
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Set, Any
from dataclasses import dataclass, field
from collections import defaultdict
import subprocess


@dataclass
class AdvancedSystem:
    """An advanced system/project"""
    name: str
    path: str
    system_type: str  # 'web_app', 'api', 'cli_tool', 'library', 'fullstack'
    technologies: List[str]
    description: str = ""
    has_frontend: bool = False
    has_backend: bool = False
    has_database: bool = False
    has_api: bool = False
    deployment_ready: bool = False
    documentation: List[str] = field(default_factory=list)
    dependencies: Dict[str, Any] = field(default_factory=dict)
    entry_points: List[str] = field(default_factory=list)
    value_score: int = 0  # 1-10


class AdvancedSystemsCatalog:
    """
    Catalog all advanced systems
    """
    
    def __init__(self):
        self.systems: List[AdvancedSystem] = []
        
        # Search locations
        self.search_paths = [
            "/Users/steven/pythons",
            "/Users/steven/workspace",
            "/Users/steven/ai-sites",
            "/Users/steven/GitHub",
            "/Users/steven/Documents",
        ]
    
    def catalog_all_systems(self):
        """Catalog all advanced systems"""
        print("🏗️ ADVANCED SYSTEMS CATALOG")
        print("="*70)
        print()
        
        for search_path in self.search_paths:
            if not Path(search_path).exists():
                continue
            
            print(f"📂 Scanning: {search_path}")
            self._scan_directory(search_path)
        
        print(f"\n✅ Found {len(self.systems)} advanced systems")
        
        # Analyze and score
        self._analyze_systems()
        
        # Generate outputs
        self._generate_catalog_csv()
        self._generate_index_md()
        self._generate_sphinx_integration()
        self._generate_deployment_plan()
    
    def _scan_directory(self, directory: Path):
        """Scan directory for advanced systems"""
        directory = Path(directory)
        
        for item in directory.iterdir():
            if not item.is_dir():
                continue
            
            # Skip common ignore directories
            if item.name in {'.git', 'node_modules', '__pycache__', 'venv', '.venv', 
                            'dist', 'build', '.next', 'Library', 'Applications'}:
                continue
            
            # Check if it's an advanced system
            system = self._identify_system(item)
            if system:
                self.systems.append(system)
                print(f"   ✨ Found: {system.name} ({system.system_type})")
    
    def _identify_system(self, path: Path) -> AdvancedSystem:
        """Identify if directory contains an advanced system"""
        # Check for indicators
        has_package_json = (path / 'package.json').exists()
        has_requirements = (path / 'requirements.txt').exists()
        has_setup_py = (path / 'setup.py').exists()
        has_docker = (path / 'Dockerfile').exists()
        has_readme = (path / 'README.md').exists()
        
        # Must have at least one indicator
        if not (has_package_json or has_requirements or has_setup_py or has_docker):
            return None
        
        system = AdvancedSystem(
            name=path.name,
            path=str(path),
            system_type='unknown',
            technologies=[]
        )
        
        # Analyze package.json
        if has_package_json:
            self._analyze_package_json(path, system)
        
        # Analyze Python project
        if has_requirements or has_setup_py:
            self._analyze_python_project(path, system)
        
        # Check for frontend/backend structure
        if (path / 'frontend').exists() or (path / 'client').exists():
            system.has_frontend = True
        if (path / 'backend').exists() or (path / 'server').exists() or (path / 'api').exists():
            system.has_backend = True
        
        # Determine system type
        system.system_type = self._determine_system_type(path, system)
        
        # Read README for description
        if has_readme:
            system.description = self._extract_description(path / 'README.md')
            system.documentation.append('README.md')
        
        # Check deployment readiness
        system.deployment_ready = self._check_deployment_ready(path, system)
        
        # Score value
        system.value_score = self._score_system(system)
        
        return system
    
    def _analyze_package_json(self, path: Path, system: AdvancedSystem):
        """Analyze package.json"""
        try:
            with open(path / 'package.json') as f:
                pkg = json.load(f)
            
            system.dependencies = pkg.get('dependencies', {})
            
            # Extract technologies
            if 'react' in system.dependencies:
                system.technologies.append('React')
            if 'next' in system.dependencies:
                system.technologies.append('Next.js')
            if 'vue' in system.dependencies:
                system.technologies.append('Vue.js')
            if 'express' in system.dependencies:
                system.technologies.append('Express.js')
                system.has_api = True
            if 'tailwindcss' in system.dependencies or 'tailwindcss' in pkg.get('devDependencies', {}):
                system.technologies.append('Tailwind CSS')
            
            # Get description
            if pkg.get('description'):
                system.description = pkg['description']
            
            # Get scripts (entry points)
            if pkg.get('scripts'):
                system.entry_points = list(pkg['scripts'].keys())
                
        except:
            pass
    
    def _analyze_python_project(self, path: Path, system: AdvancedSystem):
        """Analyze Python project"""
        # Check requirements.txt
        if (path / 'requirements.txt').exists():
            try:
                with open(path / 'requirements.txt') as f:
                    reqs = f.read().lower()
                
                # Detect frameworks
                if 'flask' in reqs:
                    system.technologies.append('Flask')
                    system.has_api = True
                if 'django' in reqs:
                    system.technologies.append('Django')
                    system.has_api = True
                if 'fastapi' in reqs:
                    system.technologies.append('FastAPI')
                    system.has_api = True
                if 'streamlit' in reqs:
                    system.technologies.append('Streamlit')
                
                # Detect databases
                if any(db in reqs for db in ['psycopg2', 'pymongo', 'sqlalchemy']):
                    system.has_database = True
                    
            except:
                pass
    
    def _determine_system_type(self, path: Path, system: AdvancedSystem) -> str:
        """Determine system type"""
        # Full-stack app
        if system.has_frontend and system.has_backend:
            return 'fullstack_app'
        
        # Web app
        if 'React' in system.technologies or 'Next.js' in system.technologies or 'Vue.js' in system.technologies:
            return 'web_app'
        
        # API/Backend
        if system.has_api or system.has_backend:
            return 'api_backend'
        
        # CLI tool
        if (path / 'cli.py').exists() or (path / 'main.py').exists():
            return 'cli_tool'
        
        # Library
        if (path / 'setup.py').exists():
            return 'library'
        
        return 'project'
    
    def _extract_description(self, readme_path: Path) -> str:
        """Extract description from README"""
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Get first paragraph after title
            description_lines = []
            skip_title = False
            
            for line in lines[:20]:
                if line.startswith('#'):
                    skip_title = True
                    continue
                if skip_title and line.strip():
                    description_lines.append(line.strip())
                    if len(description_lines) >= 3:
                        break
            
            return ' '.join(description_lines)[:200]
        except:
            return ""
    
    def _check_deployment_ready(self, path: Path, system: AdvancedSystem) -> bool:
        """Check if system is deployment ready"""
        indicators = 0
        
        # Has deployment configs
        if (path / 'Dockerfile').exists():
            indicators += 1
        if (path / 'docker-compose.yml').exists():
            indicators += 1
        if (path / 'vercel.json').exists():
            indicators += 1
        if (path / 'netlify.toml').exists():
            indicators += 1
        if (path / '.github/workflows').exists():
            indicators += 1
        
        # Has documentation
        if (path / 'README.md').exists():
            indicators += 1
        
        # Has proper structure
        if system.has_frontend or system.has_backend:
            indicators += 1
        
        return indicators >= 3
    
    def _score_system(self, system: AdvancedSystem) -> int:
        """Score system value (1-10)"""
        score = 5  # Base score
        
        # Type bonuses
        if system.system_type == 'fullstack_app':
            score += 3
        elif system.system_type in ['web_app', 'api_backend']:
            score += 2
        
        # Technology bonuses
        if len(system.technologies) >= 3:
            score += 1
        
        # Deployment ready
        if system.deployment_ready:
            score += 1
        
        # Has documentation
        if system.documentation:
            score += 1
        
        return min(10, score)
    
    def _analyze_systems(self):
        """Analyze all systems"""
        print("\n📊 Analyzing Systems...")
        
        # Group by type
        by_type = defaultdict(list)
        for system in self.systems:
            by_type[system.system_type].append(system)
        
        print(f"\nSystems by Type:")
        for sys_type, systems in sorted(by_type.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  • {sys_type}: {len(systems)}")
        
        # High-value systems
        high_value = [s for s in self.systems if s.value_score >= 7]
        print(f"\nHigh-Value Systems (7+): {len(high_value)}")
        
        # Deployment ready
        ready = [s for s in self.systems if s.deployment_ready]
        print(f"Deployment Ready: {len(ready)}")
    
    def _generate_catalog_csv(self):
        """Generate CSV catalog"""
        import csv
        
        filename = "SYSTEMS_CATALOG.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            writer.writerow([
                'Name', 'Type', 'Path', 'Technologies', 'Frontend', 'Backend',
                'API', 'Database', 'Deployment_Ready', 'Value_Score', 'Description'
            ])
            
            for system in sorted(self.systems, key=lambda s: s.value_score, reverse=True):
                writer.writerow([
                    system.name,
                    system.system_type,
                    system.path,
                    ', '.join(system.technologies),
                    'Yes' if system.has_frontend else 'No',
                    'Yes' if system.has_backend else 'No',
                    'Yes' if system.has_api else 'No',
                    'Yes' if system.has_database else 'No',
                    'Yes' if system.deployment_ready else 'No',
                    system.value_score,
                    system.description[:100]
                ])
        
        print(f"\n✅ Generated: {filename}")
    
    def _generate_index_md(self):
        """Generate markdown index"""
        lines = [
            "# 🏗️ Advanced Systems Index",
            "",
            "Complete catalog of all advanced systems across your workspace.",
            "",
            f"**Total Systems:** {len(self.systems)}",
            f"**Deployment Ready:** {sum(1 for s in self.systems if s.deployment_ready)}",
            f"**High Value (7+):** {sum(1 for s in self.systems if s.value_score >= 7)}",
            "",
            "---",
            ""
        ]
        
        # Group by type
        by_type = defaultdict(list)
        for system in self.systems:
            by_type[system.system_type].append(system)
        
        for sys_type in sorted(by_type.keys()):
            systems = sorted(by_type[sys_type], key=lambda s: s.value_score, reverse=True)
            
            lines.append(f"## {sys_type.replace('_', ' ').title()} ({len(systems)})")
            lines.append("")
            
            for system in systems:
                lines.append(f"### {system.name}")
                lines.append(f"**Path:** `{system.path}`")
                lines.append(f"**Value Score:** {system.value_score}/10")
                
                if system.technologies:
                    lines.append(f"**Technologies:** {', '.join(system.technologies)}")
                
                if system.description:
                    lines.append(f"**Description:** {system.description}")
                
                features = []
                if system.has_frontend:
                    features.append("Frontend")
                if system.has_backend:
                    features.append("Backend")
                if system.has_api:
                    features.append("API")
                if system.has_database:
                    features.append("Database")
                
                if features:
                    lines.append(f"**Features:** {', '.join(features)}")
                
                if system.deployment_ready:
                    lines.append("**Status:** ✅ Deployment Ready")
                else:
                    lines.append("**Status:** 🔧 Needs Setup")
                
                lines.append("")
            
            lines.append("---")
            lines.append("")
        
        # Top systems
        lines.append("## 🏆 Top 10 Highest Value Systems")
        lines.append("")
        
        top_systems = sorted(self.systems, key=lambda s: s.value_score, reverse=True)[:10]
        
        for i, system in enumerate(top_systems, 1):
            lines.append(f"{i}. **{system.name}** ({system.value_score}/10) - {system.system_type}")
            lines.append(f"   - Path: `{system.path}`")
            lines.append(f"   - Tech: {', '.join(system.technologies[:3])}")
            lines.append("")
        
        filename = "SYSTEMS_INDEX.md"
        Path(filename).write_text('\n'.join(lines))
        
        print(f"✅ Generated: {filename}")
    
    def _generate_sphinx_integration(self):
        """Generate Sphinx documentation integration"""
        # Create systems documentation for Sphinx
        sphinx_content = f'''
Advanced Systems Catalog
=========================

Complete catalog of {len(self.systems)} advanced systems across your workspace.

Systems Overview
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 30

   * - System Name
     - Type
     - Value Score
     - Technologies
'''
        
        for system in sorted(self.systems, key=lambda s: s.value_score, reverse=True)[:20]:
            tech = ', '.join(system.technologies[:2]) if system.technologies else 'N/A'
            sphinx_content += f'''   * - {system.name}
     - {system.system_type}
     - {system.value_score}/10
     - {tech}
'''
        
        sphinx_content += '''

Deployment Ready Systems
------------------------

These systems are ready for immediate deployment:

'''
        
        ready_systems = [s for s in self.systems if s.deployment_ready]
        for system in ready_systems[:10]:
            sphinx_content += f'''
{system.name}
{'~' * len(system.name)}

:Type: {system.system_type}
:Path: ``{system.path}``
:Technologies: {', '.join(system.technologies)}
:Value Score: {system.value_score}/10

{system.description}

'''
        
        # Save to docs if exists
        docs_path = Path('docs')
        if docs_path.exists():
            (docs_path / 'systems_catalog.rst').write_text(sphinx_content)
            print(f"✅ Generated: docs/systems_catalog.rst")
    
    def _generate_deployment_plan(self):
        """Generate deployment plan"""
        ready = [s for s in self.systems if s.deployment_ready and s.value_score >= 7]
        
        lines = [
            "# 🚀 Deployment Plan",
            "",
            f"**Systems Ready for Deployment:** {len(ready)}",
            "",
            "## Priority Deployments",
            ""
        ]
        
        for i, system in enumerate(sorted(ready, key=lambda s: s.value_score, reverse=True), 1):
            lines.append(f"### {i}. {system.name} (Value: {system.value_score}/10)")
            lines.append(f"**Type:** {system.system_type}")
            lines.append(f"**Path:** `{system.path}`")
            lines.append(f"**Tech:** {', '.join(system.technologies)}")
            lines.append("")
            lines.append("**Deployment Steps:**")
            lines.append(f"```bash")
            lines.append(f"cd {system.path}")
            
            if 'Next.js' in system.technologies:
                lines.append("npm run build")
                lines.append("# Deploy to Vercel: vercel --prod")
            elif 'React' in system.technologies:
                lines.append("npm run build")
                lines.append("# Deploy build/ directory")
            elif system.has_api:
                lines.append("# Deploy API (Docker, Railway, etc.)")
            
            lines.append("```")
            lines.append("")
        
        Path("DEPLOYMENT_PLAN.md").write_text('\n'.join(lines))
        print(f"✅ Generated: DEPLOYMENT_PLAN.md")


def main():
    """Run the catalog"""
    catalog = AdvancedSystemsCatalog()
    catalog.catalog_all_systems()
    
    print("\n" + "="*70)
    print("✅ SYSTEMS CATALOG COMPLETE")
    print("="*70)
    print()
    print("Generated Files:")
    print("  • SYSTEMS_CATALOG.csv - Complete CSV catalog")
    print("  • SYSTEMS_INDEX.md - Markdown index")
    print("  • DEPLOYMENT_PLAN.md - Deployment roadmap")
    print("  • docs/systems_catalog.rst - Sphinx integration")


if __name__ == "__main__":
    main()


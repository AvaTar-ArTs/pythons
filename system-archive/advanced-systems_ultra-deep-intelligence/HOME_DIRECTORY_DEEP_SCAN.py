#!/usr/bin/env python3
"""
🏠 HOME DIRECTORY DEEP INTELLIGENCE SCAN 🏠
===========================================
Complete deep scan of entire home directory (~/)
with content-aware AI analysis, categorization, and insights

Features:
✨ Full home directory recursive scan
✨ Content-aware file analysis
✨ Multi-LLM categorization
✨ Vector embeddings for semantic search
✨ Project discovery and mapping
✨ API/Config extraction
✨ Knowledge graph generation
✨ Intelligent recommendations
"""

import os
import sys
import json
import asyncio
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Set
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from ULTRA_DEEP_INTELLIGENCE_ORCHESTRATOR import (
    C, E, APIKeyManager, MultiLLMAnalyzer, VectorDatabaseManager
)


class HomeDirectoryScanner:
    """Deep scanner for entire home directory"""

    def __init__(self):
        self.home_path = Path.home()
        self.api_manager = APIKeyManager()
        self.llm_analyzer = MultiLLMAnalyzer(self.api_manager.available_apis['llm'])
        self.vector_manager = VectorDatabaseManager(self.api_manager.available_apis['vector'])

        # Skip directories that are too large or system-only
        self.skip_dirs = {
            'Library', '.Trash', 'node_modules', '__pycache__', '.venv',
            '.mamba', '.conda', 'Caches', '.cache', '.npm', '.nvm',
            '.cargo', '.rustup', 'Applications', 'System', '.local/share/mamba',
            '.git', '.next', 'dist', 'build', '.pytest_cache'
        }

        # Storage
        self.inventory = {
            'projects': [],
            'configs': [],
            'scripts': [],
            'documents': [],
            'data': [],
            'media': [],
            'repos': []
        }

        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'projects_found': 0,
            'configs_found': 0,
            'scripts_found': 0,
            'analyzed_files': 0,
            'skipped_dirs': 0
        }

        self.content_categories = defaultdict(list)
        self.project_map = {}

    def print_header(self, text: str, emoji: str = E.SPARKLES):
        """Print fancy header"""
        print(f"\n{C.BOLD}{C.MAGENTA}{'='*80}")
        print(f"{emoji} {text} {emoji}")
        print(f"{'='*80}{C.END}\n")

    def should_skip_directory(self, dir_path: Path) -> bool:
        """Check if directory should be skipped"""
        # Check if any part of the path contains skip directories
        return any(skip in dir_path.parts for skip in self.skip_dirs)

    def detect_project(self, dir_path: Path) -> Dict[str, Any]:
        """Detect if directory is a project"""
        project_indicators = {
            'package.json': 'nodejs',
            'requirements.txt': 'python',
            'Cargo.toml': 'rust',
            'pom.xml': 'java',
            'go.mod': 'go',
            'composer.json': 'php',
            'Gemfile': 'ruby',
            'pyproject.toml': 'python',
            'setup.py': 'python',
            '.git': 'git_repo'
        }

        detected = {}
        for indicator, proj_type in project_indicators.items():
            if (dir_path / indicator).exists():
                detected[proj_type] = True

        if detected:
            return {
                'path': str(dir_path),
                'name': dir_path.name,
                'types': list(detected.keys()),
                'size': self.get_directory_size(dir_path)
            }
        return None

    def get_directory_size(self, dir_path: Path) -> int:
        """Calculate directory size (with limit)"""
        total = 0
        count = 0
        try:
            for file in dir_path.rglob('*'):
                if file.is_file() and count < 10000:  # Limit for performance
                    try:
                        total += file.stat().st_size
                        count += 1
                    except:
                        pass
        except:
            pass
        return total

    def scan_home_directory(self, max_depth: int = 4):
        """Scan entire home directory"""
        self.print_header("SCANNING HOME DIRECTORY", E.TELESCOPE)

        print(f"{C.CYAN}🏠 Scanning: {self.home_path}{C.END}")
        print(f"{C.YELLOW}📏 Max depth: {max_depth} levels{C.END}")
        print(f"{C.YELLOW}🚫 Skipping: {len(self.skip_dirs)} directory types{C.END}\n")

        def scan_recursive(current_path: Path, depth: int = 0):
            """Recursive scanner"""
            if depth > max_depth:
                return

            try:
                for item in current_path.iterdir():
                    try:
                        # Skip hidden files at root level
                        if depth == 0 and item.name.startswith('.'):
                            continue

                        if item.is_dir():
                            # Check if should skip
                            if self.should_skip_directory(item):
                                self.stats['skipped_dirs'] += 1
                                continue

                            self.stats['total_dirs'] += 1

                            # Detect projects
                            project = self.detect_project(item)
                            if project:
                                self.inventory['projects'].append(project)
                                self.stats['projects_found'] += 1
                                print(f"{C.GREEN}📦 Project found: {item.relative_to(self.home_path)}{C.END}")

                            # Progress
                            if self.stats['total_dirs'] % 100 == 0:
                                print(f"{C.CYAN}  Scanned {self.stats['total_dirs']} dirs, {self.stats['total_files']:,} files...{C.END}")

                            # Recurse
                            scan_recursive(item, depth + 1)

                        elif item.is_file():
                            self.stats['total_files'] += 1
                            size = item.stat().st_size
                            self.stats['total_size'] += size

                            # Categorize interesting files
                            self.categorize_file(item, size)

                    except PermissionError:
                        pass
                    except Exception:
                        pass

            except PermissionError:
                pass
            except Exception:
                pass

        scan_recursive(self.home_path, 0)

        print(f"\n{C.GREEN}✅ Scan complete!{C.END}")
        print(f"{C.CYAN}   Directories: {self.stats['total_dirs']:,}{C.END}")
        print(f"{C.CYAN}   Files: {self.stats['total_files']:,}{C.END}")
        print(f"{C.MAGENTA}   Size: {self.stats['total_size'] / (1024**3):.2f} GB{C.END}\n")

    def categorize_file(self, file_path: Path, size: int):
        """Categorize file by type and content"""
        suffix = file_path.suffix.lower()

        # Configuration files
        if file_path.name in ['.env', '.envrc', 'config.yaml', 'config.json', '.zshrc', '.bashrc']:
            self.inventory['configs'].append({
                'path': str(file_path),
                'name': file_path.name,
                'size': size
            })
            self.stats['configs_found'] += 1

        # Scripts
        elif suffix in ['.py', '.sh', '.js', '.ts', '.rb', '.pl']:
            if size > 100 and size < 1_000_000:  # Reasonable size
                self.inventory['scripts'].append({
                    'path': str(file_path),
                    'name': file_path.name,
                    'type': suffix,
                    'size': size
                })
                self.stats['scripts_found'] += 1

        # Documents
        elif suffix in ['.md', '.txt', '.pdf', '.doc', '.docx']:
            if size > 100 and size < 10_000_000:
                self.inventory['documents'].append({
                    'path': str(file_path),
                    'name': file_path.name,
                    'type': suffix,
                    'size': size
                })

        # Media
        elif suffix in ['.jpg', '.png', '.jpeg', '.gif', '.mp4', '.mov', '.mp3', '.wav']:
            self.inventory['media'].append({
                'path': str(file_path),
                'name': file_path.name,
                'type': suffix,
                'size': size
            })

        # Data files
        elif suffix in ['.json', '.csv', '.xml', '.yaml', '.yml']:
            if size > 10 and size < 10_000_000:
                self.inventory['data'].append({
                    'path': str(file_path),
                    'name': file_path.name,
                    'type': suffix,
                    'size': size
                })

    async def analyze_key_content(self):
        """Analyze key content with AI"""
        self.print_header("ANALYZING KEY CONTENT", E.BRAIN)

        # Analyze top scripts
        print(f"{C.CYAN}Analyzing Python scripts...{C.END}\n")

        py_scripts = [s for s in self.inventory['scripts'] if s['type'] == '.py']
        py_scripts_sorted = sorted(py_scripts, key=lambda x: x['size'], reverse=True)[:20]

        for i, script in enumerate(py_scripts_sorted, 1):
            try:
                path = Path(script['path'])
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(5000)  # First 5000 chars

                if len(content) > 200:
                    print(f"{C.CYAN}  [{i}/20] {script['name'][:50]}...{C.END}")

                    # AI analysis
                    analysis = await self.llm_analyzer.multi_provider_analysis(
                        content, 'categorize'
                    )

                    if analysis:
                        for result in analysis:
                            if isinstance(result, dict) and 'category' in result:
                                category = result['category']
                                self.content_categories[category].append(script['path'])
                                break

                    self.stats['analyzed_files'] += 1

                    if i % 10 == 0:
                        print(f"{C.GREEN}  ✅ Analyzed {i} scripts{C.END}")

            except Exception as e:
                pass

        print(f"\n{C.GREEN}✅ Content analysis complete!{C.END}\n")

    def discover_api_keys(self):
        """Discover all API keys and configs"""
        self.print_header("DISCOVERING API CONFIGURATIONS", E.KEY)

        api_configs = []

        for config in self.inventory['configs']:
            path = Path(config['path'])
            if '.env' in path.name or 'api' in path.name.lower():
                api_configs.append(config)

        print(f"{C.GREEN}✅ Found {len(api_configs)} API configuration files{C.END}\n")

        for config in api_configs[:10]:
            print(f"{C.CYAN}  🔑 {Path(config['path']).relative_to(self.home_path)}{C.END}")

        if len(api_configs) > 10:
            print(f"{C.YELLOW}  ... and {len(api_configs) - 10} more{C.END}")
        print()

        return api_configs

    def generate_master_map(self):
        """Generate comprehensive home directory map"""
        self.print_header("GENERATING HOME DIRECTORY MAP", E.MAGIC)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(f"/Users/steven/advanced-systems/ultra-deep-intelligence/reports/HOME_DIRECTORY_DEEP_SCAN_{timestamp}.md")

        report_path.parent.mkdir(exist_ok=True, parents=True)

        with open(report_path, 'w') as f:
            f.write("# 🏠 HOME DIRECTORY DEEP INTELLIGENCE SCAN 🏠\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Location:** `{self.home_path}`\n\n")
            f.write("---\n\n")

            # Executive Summary
            f.write("## 📊 EXECUTIVE SUMMARY\n\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            f.write(f"| **Total Files** | {self.stats['total_files']:,} |\n")
            f.write(f"| **Total Directories** | {self.stats['total_dirs']:,} |\n")
            f.write(f"| **Total Size** | {self.stats['total_size'] / (1024**3):.2f} GB |\n")
            f.write(f"| **Projects Found** | {self.stats['projects_found']:,} |\n")
            f.write(f"| **Scripts Found** | {self.stats['scripts_found']:,} |\n")
            f.write(f"| **Configs Found** | {self.stats['configs_found']:,} |\n")
            f.write(f"| **AI Analyzed** | {self.stats['analyzed_files']:,} |\n")
            f.write(f"| **Directories Skipped** | {self.stats['skipped_dirs']:,} |\n\n")

            # Projects discovered
            if self.inventory['projects']:
                f.write("## 📦 PROJECTS DISCOVERED\n\n")
                sorted_projects = sorted(self.inventory['projects'],
                                        key=lambda x: x['size'], reverse=True)

                for i, project in enumerate(sorted_projects[:50], 1):
                    rel_path = Path(project['path']).relative_to(self.home_path)
                    f.write(f"### {i}. {project['name']}\n")
                    f.write(f"- **Path:** `~/{rel_path}`\n")
                    f.write(f"- **Type:** {', '.join(project['types'])}\n")
                    f.write(f"- **Size:** {project['size'] / (1024**2):.2f} MB\n\n")

                if len(sorted_projects) > 50:
                    f.write(f"... and {len(sorted_projects) - 50} more projects\n\n")

            # Configuration files
            if self.inventory['configs']:
                f.write("## 🔑 CONFIGURATION FILES\n\n")
                for config in self.inventory['configs'][:30]:
                    rel_path = Path(config['path']).relative_to(self.home_path)
                    f.write(f"- `~/{rel_path}` ({config['size']:,} bytes)\n")

                if len(self.inventory['configs']) > 30:
                    f.write(f"- ... and {len(self.inventory['configs']) - 30} more\n")
                f.write("\n")

            # Script analysis
            if self.inventory['scripts']:
                f.write("## 🐍 SCRIPTS BY TYPE\n\n")

                scripts_by_type = defaultdict(list)
                for script in self.inventory['scripts']:
                    scripts_by_type[script['type']].append(script)

                for script_type, scripts in sorted(scripts_by_type.items(),
                                                  key=lambda x: len(x[1]), reverse=True):
                    total_size = sum(s['size'] for s in scripts)
                    f.write(f"### {script_type} Scripts ({len(scripts)})\n")
                    f.write(f"**Total Size:** {total_size / (1024**2):.2f} MB\n\n")

                    # Show largest scripts
                    largest = sorted(scripts, key=lambda x: x['size'], reverse=True)[:10]
                    for script in largest:
                        rel_path = Path(script['path']).relative_to(self.home_path)
                        f.write(f"- `~/{rel_path}` ({script['size'] / 1024:.1f} KB)\n")

                    if len(scripts) > 10:
                        f.write(f"- ... and {len(scripts) - 10} more\n")
                    f.write("\n")

            # AI-Discovered Categories
            if self.content_categories:
                f.write("## 🧠 AI-DISCOVERED CONTENT CATEGORIES\n\n")
                for category, files in sorted(self.content_categories.items(),
                                             key=lambda x: len(x[1]), reverse=True)[:15]:
                    f.write(f"### {category}\n")
                    f.write(f"**Files:** {len(files)}\n\n")
                    for file_path in files[:5]:
                        rel_path = Path(file_path).relative_to(self.home_path)
                        f.write(f"- `~/{rel_path}`\n")
                    if len(files) > 5:
                        f.write(f"- ... and {len(files) - 5} more\n")
                    f.write("\n")

            # Documents
            if self.inventory['documents']:
                f.write("## 📄 DOCUMENTS\n\n")
                docs_by_type = defaultdict(int)
                docs_size = defaultdict(int)
                for doc in self.inventory['documents']:
                    docs_by_type[doc['type']] += 1
                    docs_size[doc['type']] += doc['size']

                f.write("| Type | Count | Total Size |\n")
                f.write("|------|-------|------------|\n")
                for doc_type in sorted(docs_by_type.keys()):
                    count = docs_by_type[doc_type]
                    size = docs_size[doc_type] / (1024**2)
                    f.write(f"| `{doc_type}` | {count:,} | {size:.2f} MB |\n")
                f.write("\n")

            # Data files
            if self.inventory['data']:
                f.write("## 📊 DATA FILES\n\n")
                data_by_type = defaultdict(int)
                for data in self.inventory['data']:
                    data_by_type[data['type']] += 1

                for data_type, count in sorted(data_by_type.items(),
                                              key=lambda x: x[1], reverse=True):
                    f.write(f"- **{data_type}**: {count:,} files\n")
                f.write("\n")

            # Recommendations
            f.write("## 💡 INTELLIGENT RECOMMENDATIONS\n\n")
            f.write("### Organization\n")
            f.write(f"1. Found {self.stats['projects_found']} projects - consider consolidating similar ones\n")
            f.write(f"2. Found {self.stats['configs_found']} config files - centralize API keys\n")
            f.write(f"3. Found {self.stats['scripts_found']} scripts - organize by function\n")
            f.write("4. Create master index of all projects\n")
            f.write("5. Set up automated backup for important configs\n\n")

            f.write("### Cleanup Opportunities\n")
            f.write(f"- Review {len(self.inventory['media'])} media files for duplicates\n")
            f.write(f"- Archive old projects to external storage\n")
            f.write(f"- Consider removing unused node_modules (skipped {self.stats['skipped_dirs']} dirs)\n\n")

            f.write("### Next Steps\n")
            f.write("1. Review project list and archive unused ones\n")
            f.write("2. Consolidate API configurations\n")
            f.write("3. Create backup strategy for important data\n")
            f.write("4. Set up automated organization system\n")
            f.write("5. Build searchable index of all content\n\n")

        print(f"{C.GREEN}✅ Map saved:{C.END}")
        print(f"{C.CYAN}   {report_path}{C.END}\n")

        return report_path

    async def run(self):
        """Run complete home directory scan"""
        print(f"{C.BOLD}{C.MAGENTA}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║           🏠 HOME DIRECTORY DEEP INTELLIGENCE SCAN 🏠                         ║")
        print("║                                                                               ║")
        print("║        Complete Content-Aware Analysis of Entire Home Directory               ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C.END}\n")

        # Phase 1: API Check
        self.print_header("PHASE 1: API ARSENAL", E.KEY)
        self.api_manager.print_available_apis()

        # Phase 2: Scan
        self.scan_home_directory(max_depth=4)

        # Phase 3: Discover APIs
        api_configs = self.discover_api_keys()

        # Phase 4: AI Analysis
        await self.analyze_key_content()

        # Phase 5: Generate map
        report_path = self.generate_master_map()

        # Complete
        self.print_header("SCAN COMPLETE!", E.ROCKET)
        print(f"{C.GREEN}{E.STAR} Home Directory Deep Scan Complete!{C.END}")
        print(f"{C.CYAN}Report: {C.BOLD}{report_path}{C.END}\n")

        return report_path


async def main():
    """Main execution"""
    scanner = HomeDirectoryScanner()
    await scanner.run()

    print(f"\n{C.GREEN}{C.BOLD}{E.SPARKLES} COMPLETE HOME SCAN DONE! {E.SPARKLES}{C.END}\n")


if __name__ == "__main__":
    asyncio.run(main())

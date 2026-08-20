#!/usr/bin/env python3
"""
📁 FOLDER-BY-FOLDER DEEP ANALYZER 📁
=====================================
Systematic deep-dive analysis of each folder individually
with comprehensive content awareness and AI insights
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from ULTRA_DEEP_INTELLIGENCE_ORCHESTRATOR import (
    C, E, APIKeyManager, MultiLLMAnalyzer, VectorDatabaseManager
)


class FolderDeepDive:
    """Deep dive analysis for a single folder"""

    def __init__(self, folder_path: str, api_manager: APIKeyManager):
        self.folder_path = Path(folder_path)
        self.folder_name = self.folder_path.name
        self.api_manager = api_manager
        self.llm_analyzer = MultiLLMAnalyzer(api_manager.available_apis['llm'])
        self.vector_manager = VectorDatabaseManager(api_manager.available_apis['vector'])

        self.inventory = {
            'files': [],
            'subdirs': [],
            'by_type': defaultdict(list),
            'by_size': defaultdict(list),
            'content_analyzed': []
        }

        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'text_files': 0,
            'code_files': 0,
            'data_files': 0,
            'media_files': 0,
            'analyzed': 0
        }

        self.insights = []
        self.categories = defaultdict(list)

    def print_section(self, text: str, emoji: str = "📌"):
        """Print section header"""
        print(f"\n{C.CYAN}{C.BOLD}{emoji} {text}{C.END}")
        print(f"{C.CYAN}{'─'*60}{C.END}\n")

    def scan_folder(self):
        """Scan folder contents"""
        print(f"{C.CYAN}🔍 Scanning {self.folder_name}...{C.END}\n")

        if not self.folder_path.exists():
            print(f"{C.RED}❌ Folder not found: {self.folder_path}{C.END}\n")
            return False

        for item in self.folder_path.rglob('*'):
            try:
                if item.is_file():
                    size = item.stat().st_size
                    suffix = item.suffix.lower()

                    file_info = {
                        'path': str(item),
                        'name': item.name,
                        'size': size,
                        'type': suffix,
                        'relative': str(item.relative_to(self.folder_path)),
                        'modified': item.stat().st_mtime
                    }

                    self.inventory['files'].append(file_info)
                    self.inventory['by_type'][suffix].append(file_info)
                    self.stats['total_files'] += 1
                    self.stats['total_size'] += size

                    # Categorize
                    if suffix in ['.md', '.txt', '.pdf', '.doc', '.docx']:
                        self.stats['text_files'] += 1
                    elif suffix in ['.py', '.js', '.ts', '.sh', '.rb', '.go', '.rs']:
                        self.stats['code_files'] += 1
                    elif suffix in ['.json', '.csv', '.xml', '.yaml', '.yml']:
                        self.stats['data_files'] += 1
                    elif suffix in ['.jpg', '.png', '.mp4', '.mp3', '.wav', '.mov']:
                        self.stats['media_files'] += 1

                elif item.is_dir():
                    self.stats['total_dirs'] += 1
                    if item.parent == self.folder_path:  # Direct subdirectory
                        dir_size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                        self.inventory['subdirs'].append({
                            'name': item.name,
                            'path': str(item),
                            'size': dir_size
                        })

            except Exception:
                pass

        print(f"{C.GREEN}✅ Scanned: {self.stats['total_files']:,} files in {self.stats['total_dirs']:,} directories{C.END}")
        print(f"{C.MAGENTA}   Total size: {self.stats['total_size'] / (1024**2):.2f} MB{C.END}\n")

        return True

    async def analyze_content(self, max_files: int = 20):
        """Analyze content with AI"""
        self.print_section("AI CONTENT ANALYSIS", E.BRAIN)

        # Find interesting files to analyze
        text_files = [f for f in self.inventory['files']
                     if f['type'] in ['.md', '.txt'] and f['size'] > 100 and f['size'] < 500000]

        code_files = [f for f in self.inventory['files']
                     if f['type'] in ['.py', '.js'] and f['size'] > 500 and f['size'] < 100000]

        to_analyze = (text_files[:10] + code_files[:10])[:max_files]

        if not to_analyze:
            print(f"{C.YELLOW}No suitable files for AI analysis{C.END}\n")
            return

        print(f"{C.CYAN}Analyzing {len(to_analyze)} files with multi-LLM...{C.END}\n")

        for i, file_info in enumerate(to_analyze, 1):
            try:
                path = Path(file_info['path'])
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(5000)  # First 5000 chars

                if len(content) > 100:
                    print(f"{C.CYAN}  [{i}/{len(to_analyze)}] {file_info['name'][:50]}...{C.END}")

                    # Multi-LLM analysis
                    results = await self.llm_analyzer.multi_provider_analysis(
                        content, 'categorize'
                    )

                    analysis = {
                        'file': file_info,
                        'results': results
                    }

                    self.inventory['content_analyzed'].append(analysis)
                    self.stats['analyzed'] += 1

                    # Extract categories
                    for result in results:
                        if isinstance(result, dict) and 'category' in result:
                            category = result['category']
                            self.categories[category].append(file_info['name'])
                            break

            except Exception as e:
                pass

        print(f"\n{C.GREEN}✅ Analyzed {self.stats['analyzed']} files{C.END}\n")

    def generate_insights(self):
        """Generate intelligent insights"""
        self.print_section("GENERATING INSIGHTS", E.LIGHTBULB)

        # Folder purpose
        purpose = self.detect_folder_purpose()
        self.insights.append(f"Primary purpose: {purpose}")

        # Size insights
        if self.stats['total_size'] > 1_000_000_000:
            self.insights.append(f"⚠️ Large folder ({self.stats['total_size'] / (1024**3):.2f} GB) - consider archiving")

        # File type insights
        if self.stats['code_files'] > 100:
            self.insights.append(f"💻 Code repository with {self.stats['code_files']} code files")

        if self.stats['media_files'] > 100:
            self.insights.append(f"🎨 Media collection with {self.stats['media_files']} media files")

        # Subdirectory insights
        if len(self.inventory['subdirs']) > 50:
            self.insights.append(f"📁 Complex structure with {len(self.inventory['subdirs'])} subdirectories")

        for insight in self.insights:
            print(f"{C.YELLOW}💡 {insight}{C.END}")

        print()

    def detect_folder_purpose(self) -> str:
        """Detect the purpose of the folder"""
        name_lower = self.folder_name.lower()

        if 'archive' in name_lower:
            return "Archive/Backup"
        elif 'backup' in name_lower:
            return "Backup Storage"
        elif 'python' in name_lower or self.stats['code_files'] > 50:
            return "Code/Development"
        elif 'doc' in name_lower or self.stats['text_files'] > 50:
            return "Documentation"
        elif 'media' in name_lower or self.stats['media_files'] > 50:
            return "Media Storage"
        elif 'data' in name_lower or self.stats['data_files'] > 50:
            return "Data Storage"
        else:
            return "Mixed Content"

    def generate_folder_report(self) -> str:
        """Generate detailed folder report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(f"/Users/steven/advanced-systems/ultra-deep-intelligence/reports/folders/FOLDER_{self.folder_name}_{timestamp}.md")

        report_path.parent.mkdir(exist_ok=True, parents=True)

        with open(report_path, 'w') as f:
            f.write(f"# 📁 DEEP DIVE: {self.folder_name}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Path:** `{self.folder_path}`\n\n")
            f.write("---\n\n")

            # Statistics
            f.write("## 📊 STATISTICS\n\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            f.write(f"| **Total Files** | {self.stats['total_files']:,} |\n")
            f.write(f"| **Directories** | {self.stats['total_dirs']:,} |\n")
            f.write(f"| **Total Size** | {self.stats['total_size'] / (1024**2):.2f} MB |\n")
            f.write(f"| **Text Files** | {self.stats['text_files']:,} |\n")
            f.write(f"| **Code Files** | {self.stats['code_files']:,} |\n")
            f.write(f"| **Data Files** | {self.stats['data_files']:,} |\n")
            f.write(f"| **Media Files** | {self.stats['media_files']:,} |\n")
            f.write(f"| **AI Analyzed** | {self.stats['analyzed']:,} |\n\n")

            # Direct subdirectories
            if self.inventory['subdirs']:
                f.write("## 📂 SUBDIRECTORIES\n\n")
                sorted_subdirs = sorted(self.inventory['subdirs'],
                                       key=lambda x: x['size'], reverse=True)

                f.write("| Directory | Size |\n")
                f.write("|-----------|------|\n")
                for subdir in sorted_subdirs[:30]:
                    f.write(f"| `{subdir['name']}` | {subdir['size'] / (1024**2):.2f} MB |\n")

                if len(sorted_subdirs) > 30:
                    f.write(f"\n*... and {len(sorted_subdirs) - 30} more subdirectories*\n")
                f.write("\n")

            # File types
            f.write("## 📄 FILES BY TYPE\n\n")
            sorted_types = sorted(self.inventory['by_type'].items(),
                                 key=lambda x: len(x[1]), reverse=True)

            f.write("| Extension | Count | Total Size |\n")
            f.write("|-----------|-------|------------|\n")
            for ext, files in sorted_types[:20]:
                total_size = sum(f['size'] for f in files)
                ext_display = ext if ext else '(no extension)'
                f.write(f"| `{ext_display}` | {len(files):,} | {total_size / (1024**2):.2f} MB |\n")
            f.write("\n")

            # AI-discovered categories
            if self.categories:
                f.write("## 🧠 AI-DISCOVERED CATEGORIES\n\n")
                for category, files in sorted(self.categories.items(),
                                             key=lambda x: len(x[1]), reverse=True):
                    f.write(f"### {category}\n")
                    f.write(f"**Files:** {len(files)}\n\n")
                    for filename in files[:5]:
                        f.write(f"- `{filename}`\n")
                    if len(files) > 5:
                        f.write(f"- ... and {len(files) - 5} more\n")
                    f.write("\n")

            # Content analysis results
            if self.inventory['content_analyzed']:
                f.write("## 📝 DETAILED CONTENT ANALYSIS\n\n")
                for i, analysis in enumerate(self.inventory['content_analyzed'][:10], 1):
                    file_info = analysis['file']
                    f.write(f"### {i}. {file_info['name']}\n\n")
                    f.write(f"**Path:** `{file_info['relative']}`\n")
                    f.write(f"**Size:** {file_info['size']:,} bytes\n")
                    f.write(f"**Type:** `{file_info['type']}`\n\n")

                    # AI results
                    for result in analysis['results']:
                        if isinstance(result, dict):
                            if 'category' in result:
                                f.write(f"**Category:** {result['category']}\n")
                            if 'topics' in result:
                                f.write(f"**Topics:** {', '.join(result['topics'][:5])}\n")
                            if 'purpose' in result:
                                f.write(f"**Purpose:** {result['purpose']}\n")
                            break
                    f.write("\n---\n\n")

            # Insights
            if self.insights:
                f.write("## 💡 KEY INSIGHTS\n\n")
                for insight in self.insights:
                    f.write(f"- {insight}\n")
                f.write("\n")

            # Recommendations
            f.write("## 🚀 RECOMMENDATIONS\n\n")
            purpose = self.detect_folder_purpose()

            if purpose == "Archive/Backup":
                f.write("### Archive Folder\n")
                f.write("1. Consider compressing old archives\n")
                f.write("2. Move to external storage if not frequently accessed\n")
                f.write("3. Remove duplicates within archives\n")
            elif purpose == "Code/Development":
                f.write("### Development Folder\n")
                f.write("1. Add README if missing\n")
                f.write("2. Set up proper .gitignore\n")
                f.write("3. Document main scripts\n")
            elif purpose == "Documentation":
                f.write("### Documentation Folder\n")
                f.write("1. Create master index\n")
                f.write("2. Link related documents\n")
                f.write("3. Add search functionality\n")
            else:
                f.write("### General Organization\n")
                f.write("1. Consider creating subcategories\n")
                f.write("2. Add descriptive README\n")
                f.write("3. Archive old/unused files\n")

            f.write("\n")

        return report_path

    async def analyze(self):
        """Run complete folder analysis"""
        print(f"\n{C.BOLD}{C.MAGENTA}{'='*80}")
        print(f"📁 DEEP DIVE: {self.folder_name}")
        print(f"{'='*80}{C.END}\n")

        # Scan
        if not self.scan_folder():
            return None

        # Statistics
        self.print_section("STATISTICS", E.CHART)
        print(f"{C.CYAN}Files:{C.END} {self.stats['total_files']:,}")
        print(f"{C.CYAN}Directories:{C.END} {self.stats['total_dirs']:,}")
        print(f"{C.CYAN}Size:{C.END} {self.stats['total_size'] / (1024**2):.2f} MB")
        print(f"{C.CYAN}Text files:{C.END} {self.stats['text_files']:,}")
        print(f"{C.CYAN}Code files:{C.END} {self.stats['code_files']:,}")
        print(f"{C.CYAN}Data files:{C.END} {self.stats['data_files']:,}")
        print(f"{C.CYAN}Media files:{C.END} {self.stats['media_files']:,}")

        # Subdirectories
        if self.inventory['subdirs']:
            self.print_section("TOP SUBDIRECTORIES", E.FOLDER)
            sorted_subdirs = sorted(self.inventory['subdirs'],
                                   key=lambda x: x['size'], reverse=True)[:10]
            for subdir in sorted_subdirs:
                print(f"{C.CYAN}📂 {subdir['name']:<40} {subdir['size'] / (1024**2):>8.2f} MB{C.END}")

        # File types
        self.print_section("FILE TYPES", E.FILE)
        sorted_types = sorted(self.inventory['by_type'].items(),
                             key=lambda x: len(x[1]), reverse=True)[:10]
        for ext, files in sorted_types:
            total_size = sum(f['size'] for f in files)
            ext_display = ext if ext else '(no ext)'
            print(f"{C.CYAN}{ext_display:<15} {len(files):>6,} files  {total_size / (1024**2):>8.2f} MB{C.END}")

        # AI Analysis
        await self.analyze_content()

        # Insights
        self.generate_insights()

        # Report
        report_path = self.generate_folder_report()

        print(f"\n{C.GREEN}✅ Deep dive complete!{C.END}")
        print(f"{C.CYAN}📊 Report: {report_path}{C.END}\n")

        return report_path


class FolderByFolderAnalyzer:
    """Analyzes all folders in Documents one by one"""

    def __init__(self, root_path: str = "/Users/steven/Documents"):
        self.root_path = Path(root_path)
        self.api_manager = APIKeyManager()
        self.folder_reports = []

    def get_top_level_folders(self) -> List[Path]:
        """Get all top-level folders"""
        folders = []
        for item in self.root_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                folders.append(item)

        # Sort by size
        folders_with_size = []
        for folder in folders:
            try:
                size = sum(f.stat().st_size for f in folder.rglob('*') if f.is_file())
                folders_with_size.append((folder, size))
            except:
                folders_with_size.append((folder, 0))

        # Sort by size descending
        folders_with_size.sort(key=lambda x: x[1], reverse=True)

        return [f[0] for f in folders_with_size]

    async def analyze_all(self):
        """Analyze all folders one by one"""
        print(f"{C.BOLD}{C.MAGENTA}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║           📁 FOLDER-BY-FOLDER DEEP ANALYZER 📁                               ║")
        print("║                                                                               ║")
        print("║        Systematic Deep-Dive of Each Folder in ~/Documents                     ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C.END}\n")

        folders = self.get_top_level_folders()

        print(f"{C.CYAN}Found {len(folders)} top-level folders in ~/Documents{C.END}\n")

        # Analyze each folder
        for i, folder in enumerate(folders, 1):
            print(f"{C.BOLD}{C.BLUE}{'='*80}")
            print(f"FOLDER {i}/{len(folders)}")
            print(f"{'='*80}{C.END}\n")

            analyzer = FolderDeepDive(str(folder), self.api_manager)
            report = await analyzer.analyze()

            if report:
                self.folder_reports.append({
                    'folder': folder.name,
                    'report': str(report)
                })

            print(f"{C.GREEN}{'─'*80}{C.END}\n")

        # Generate master index
        self.generate_master_index()

        print(f"\n{C.GREEN}{C.BOLD}{E.SPARKLES} ALL FOLDERS ANALYZED! {E.SPARKLES}{C.END}\n")

    def generate_master_index(self):
        """Generate master index of all folder analyses"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        index_path = Path(f"/Users/steven/advanced-systems/ultra-deep-intelligence/reports/MASTER_FOLDER_INDEX_{timestamp}.md")

        with open(index_path, 'w') as f:
            f.write("# 📚 MASTER FOLDER INDEX 📚\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Location:** `{self.root_path}`\n")
            f.write(f"**Folders Analyzed:** {len(self.folder_reports)}\n\n")
            f.write("---\n\n")

            f.write("## 📁 ANALYZED FOLDERS\n\n")
            for i, report_info in enumerate(self.folder_reports, 1):
                f.write(f"{i}. **{report_info['folder']}**\n")
                f.write(f"   - Report: `{Path(report_info['report']).name}`\n\n")

            f.write("\n## 📊 ALL REPORTS\n\n")
            f.write("Individual folder reports available in:\n")
            f.write("`~/advanced-systems/ultra-deep-intelligence/reports/folders/`\n\n")

        print(f"{C.GREEN}✅ Master index created:{C.END}")
        print(f"{C.CYAN}   {index_path}{C.END}\n")


async def main():
    """Main execution"""
    import sys

    if len(sys.argv) > 1:
        # Analyze specific folder
        folder_path = sys.argv[1]
        api_manager = APIKeyManager()
        analyzer = FolderDeepDive(folder_path, api_manager)
        await analyzer.analyze()
    else:
        # Analyze all folders
        analyzer = FolderByFolderAnalyzer()
        await analyzer.analyze_all()


if __name__ == "__main__":
    asyncio.run(main())

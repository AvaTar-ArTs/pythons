#!/usr/bin/env python3
"""
🗂️ ARCHIVES DEEP ANALYZER 🗂️
==============================
Specialized deep analysis tool for Archives directory
with archive extraction, content categorization, and deduplication
"""

import os
import sys
import json
import asyncio
import hashlib
import tarfile
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from ULTRA_DEEP_INTELLIGENCE_ORCHESTRATOR import (
    C, E, APIKeyManager, MultiLLMAnalyzer, VectorDatabaseManager
)

class ArchiveExtractor:
    """Extract and analyze compressed archives"""

    def __init__(self, temp_dir: str = "/tmp/archive_analysis"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(exist_ok=True, parents=True)
        self.extracted_files = {}

    def extract_archive(self, archive_path: Path) -> Dict[str, Any]:
        """Extract archive and return contents info"""
        result = {
            'path': str(archive_path),
            'name': archive_path.name,
            'size': 0,
            'type': archive_path.suffix,
            'extracted': False,
            'files': [],
            'error': None
        }

        try:
            if not archive_path.exists():
                result['error'] = "File not found"
                return result

            result['size'] = archive_path.stat().st_size
            extract_dir = self.temp_dir / archive_path.stem
            extract_dir.mkdir(exist_ok=True)

            if archive_path.suffix == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    result['files'] = zf.namelist()
                    # Extract only small text files for analysis
                    for filename in result['files'][:20]:  # Limit extraction
                        if filename.endswith(('.md', '.txt', '.py', '.json')):
                            try:
                                zf.extract(filename, extract_dir)
                            except:
                                pass

            elif archive_path.suffix in ['.tar', '.gz', '.tgz']:
                with tarfile.open(archive_path, 'r:*') as tf:
                    result['files'] = tf.getnames()
                    # Extract only small text files
                    for member in tf.getmembers()[:20]:
                        if member.name.endswith(('.md', '.txt', '.py', '.json')):
                            try:
                                tf.extract(member, extract_dir)
                            except:
                                pass

            result['extracted'] = True
            result['extract_dir'] = str(extract_dir)

        except Exception as e:
            result['error'] = str(e)

        return result


class ArchivesDeepAnalyzer:
    """Deep analyzer specifically for Archives directory"""

    def __init__(self, archives_path: str = "/Users/steven/Documents/Archives"):
        self.archives_path = Path(archives_path)
        self.api_manager = APIKeyManager()
        self.llm_analyzer = MultiLLMAnalyzer(self.api_manager.available_apis['llm'])
        self.vector_manager = VectorDatabaseManager(self.api_manager.available_apis['vector'])
        self.extractor = ArchiveExtractor()

        self.archives_inventory = {}
        self.markdown_files = []
        self.zip_files = []
        self.repos = []
        self.analysis_results = {}

        self.stats = {
            'total_files': 0,
            'total_size': 0,
            'archives_found': 0,
            'markdown_analyzed': 0,
            'repos_found': 0,
            'duplicates_found': 0
        }

    def print_header(self, text: str, emoji: str = E.SPARKLES):
        """Print fancy header"""
        print(f"\n{C.BOLD}{C.MAGENTA}{'='*80}")
        print(f"{emoji} {text} {emoji}")
        print(f"{'='*80}{C.END}\n")

    def scan_archives(self):
        """Scan Archives directory comprehensively"""
        self.print_header("SCANNING ARCHIVES DIRECTORY", E.MICROSCOPE)

        print(f"{C.CYAN}📁 Scanning: {self.archives_path}{C.END}\n")

        for item in self.archives_path.rglob('*'):
            if item.is_file():
                self.stats['total_files'] += 1
                size = item.stat().st_size
                self.stats['total_size'] += size

                file_info = {
                    'path': str(item),
                    'name': item.name,
                    'size': size,
                    'extension': item.suffix,
                    'relative_path': str(item.relative_to(self.archives_path))
                }

                # Categorize
                if item.suffix == '.md':
                    self.markdown_files.append(file_info)
                elif item.suffix in ['.zip', '.tar', '.gz', '.tgz']:
                    self.zip_files.append(file_info)
                    self.stats['archives_found'] += 1

                self.archives_inventory[str(item)] = file_info

        # Find repos
        repos_dir = self.archives_path / 'repos'
        if repos_dir.exists():
            for repo in repos_dir.iterdir():
                if repo.is_dir():
                    self.repos.append({
                        'name': repo.name,
                        'path': str(repo),
                        'size': sum(f.stat().st_size for f in repo.rglob('*') if f.is_file())
                    })
                    self.stats['repos_found'] += 1

        print(f"{C.GREEN}✅ Found {self.stats['total_files']:,} files{C.END}")
        print(f"{C.CYAN}   📝 Markdown: {len(self.markdown_files)}{C.END}")
        print(f"{C.CYAN}   📦 Archives: {len(self.zip_files)}{C.END}")
        print(f"{C.CYAN}   🔧 Repos: {len(self.repos)}{C.END}")
        print(f"{C.MAGENTA}   💾 Total Size: {self.stats['total_size'] / (1024**3):.2f} GB{C.END}\n")

    async def analyze_markdown_files(self):
        """Deep analyze markdown files in Archives"""
        self.print_header("ANALYZING MARKDOWN FILES", E.BRAIN)

        print(f"{C.YELLOW}Analyzing {len(self.markdown_files)} markdown files...{C.END}\n")

        for i, md_file in enumerate(self.markdown_files[:50], 1):  # Limit to 50
            try:
                path = Path(md_file['path'])
                if path.stat().st_size > 10_000_000:  # Skip files > 10MB
                    continue

                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                if len(content) < 100:
                    continue

                print(f"{C.CYAN}{E.BRAIN} Analyzing: {md_file['name'][:60]}...{C.END}")

                # Multi-provider analysis
                categorization = await self.llm_analyzer.multi_provider_analysis(
                    content, 'categorize'
                )

                knowledge = await self.llm_analyzer.multi_provider_analysis(
                    content, 'extract_knowledge'
                )

                self.analysis_results[md_file['path']] = {
                    'file_info': md_file,
                    'categorization': categorization,
                    'knowledge': knowledge,
                    'analyzed_at': datetime.now().isoformat()
                }

                self.stats['markdown_analyzed'] += 1

                if i % 10 == 0:
                    print(f"{C.GREEN}✅ Analyzed {i} files{C.END}")

            except Exception as e:
                print(f"{C.RED}❌ Error analyzing {md_file['name']}: {e}{C.END}")

        print(f"\n{C.GREEN}✅ Completed markdown analysis!{C.END}\n")

    def analyze_archive_contents(self):
        """Analyze compressed archive contents"""
        self.print_header("ANALYZING ARCHIVE CONTENTS", E.GEAR)

        print(f"{C.YELLOW}Examining {len(self.zip_files)} archives...{C.END}\n")

        archive_analysis = []

        for archive in sorted(self.zip_files, key=lambda x: x['size'], reverse=True)[:20]:
            print(f"{C.CYAN}📦 Extracting: {archive['name']}{C.END}")

            result = self.extractor.extract_archive(Path(archive['path']))

            if result['extracted']:
                print(f"{C.GREEN}   ✅ Found {len(result['files'])} files{C.END}")
                archive_analysis.append(result)
            else:
                print(f"{C.RED}   ❌ {result['error']}{C.END}")

        return archive_analysis

    def detect_duplicates(self):
        """Find duplicate files across archives"""
        self.print_header("DETECTING DUPLICATES", E.MICROSCOPE)

        file_hashes = defaultdict(list)

        print(f"{C.CYAN}Computing hashes...{C.END}\n")

        for file_path, file_info in self.archives_inventory.items():
            path = Path(file_path)
            if path.stat().st_size > 100_000_000:  # Skip files > 100MB
                continue

            try:
                hasher = hashlib.md5()
                with open(path, 'rb') as f:
                    hasher.update(f.read())
                file_hash = hasher.hexdigest()
                file_hashes[file_hash].append(file_info)
            except:
                pass

        duplicates = {h: files for h, files in file_hashes.items() if len(files) > 1}
        self.stats['duplicates_found'] = sum(len(files) - 1 for files in duplicates.values())

        print(f"{C.GREEN}✅ Found {len(duplicates)} duplicate groups{C.END}")
        print(f"{C.YELLOW}   Total duplicate files: {self.stats['duplicates_found']}{C.END}\n")

        return duplicates

    def generate_report(self, duplicates: Dict, archive_analysis: List):
        """Generate comprehensive Archives analysis report"""
        self.print_header("GENERATING REPORT", E.MAGIC)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"/Users/steven/advanced-systems/ultra-deep-intelligence/reports/ARCHIVES_DEEP_ANALYSIS_{timestamp}.md"

        # Ensure reports directory exists
        Path(report_path).parent.mkdir(exist_ok=True, parents=True)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 🗂️ ARCHIVES DEEP ANALYSIS REPORT 🗂️\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            # Executive Summary
            f.write("## 📊 EXECUTIVE SUMMARY\n\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            f.write(f"| **Total Files** | {self.stats['total_files']:,} |\n")
            f.write(f"| **Total Size** | {self.stats['total_size'] / (1024**3):.2f} GB |\n")
            f.write(f"| **Markdown Files** | {len(self.markdown_files)} |\n")
            f.write(f"| **Archives Found** | {self.stats['archives_found']} |\n")
            f.write(f"| **Repos Found** | {self.stats['repos_found']} |\n")
            f.write(f"| **Duplicates** | {self.stats['duplicates_found']} |\n")
            f.write(f"| **Analyzed** | {self.stats['markdown_analyzed']} |\n\n")

            # Repository Analysis
            if self.repos:
                f.write("## 🔧 REPOSITORIES FOUND\n\n")
                for repo in self.repos:
                    f.write(f"### {repo['name']}\n")
                    f.write(f"- **Path:** `{repo['path']}`\n")
                    f.write(f"- **Size:** {repo['size'] / (1024**2):.2f} MB\n\n")

            # Archive Contents
            if archive_analysis:
                f.write("## 📦 ARCHIVE CONTENTS ANALYSIS\n\n")
                for archive in archive_analysis[:10]:
                    f.write(f"### {archive['name']}\n")
                    f.write(f"- **Size:** {archive['size'] / (1024**2):.2f} MB\n")
                    f.write(f"- **Files:** {len(archive['files'])}\n")
                    f.write(f"- **Type:** {archive['type']}\n")
                    if archive['files']:
                        f.write("- **Sample Contents:**\n")
                        for filename in archive['files'][:10]:
                            f.write(f"  - `{filename}`\n")
                    f.write("\n")

            # Markdown Analysis Results
            if self.analysis_results:
                f.write("## 📝 MARKDOWN FILE ANALYSIS\n\n")
                for file_path, result in list(self.analysis_results.items())[:20]:
                    file_info = result['file_info']
                    f.write(f"### {file_info['name']}\n\n")
                    f.write(f"**Path:** `{file_info['relative_path']}`\n\n")

                    if result['categorization']:
                        f.write("**Categories:**\n")
                        for cat in result['categorization']:
                            if isinstance(cat, dict) and 'category' in cat:
                                f.write(f"- {cat.get('category', 'Unknown')}")
                                if 'topics' in cat:
                                    f.write(f" - Topics: {', '.join(cat['topics'][:3])}")
                                f.write("\n")

                    f.write("\n---\n\n")

            # Duplicates
            if duplicates:
                f.write("## 🔄 DUPLICATE FILES\n\n")
                for i, (file_hash, files) in enumerate(list(duplicates.items())[:20], 1):
                    f.write(f"### Duplicate Group #{i}\n")
                    f.write(f"**Hash:** `{file_hash[:16]}...`\n\n")
                    for file_info in files:
                        f.write(f"- `{file_info['relative_path']}` ({file_info['size'] / 1024:.1f} KB)\n")
                    f.write("\n")

            # Recommendations
            f.write("## 💡 RECOMMENDATIONS\n\n")
            f.write("### Cleanup Opportunities\n")
            f.write(f"1. **Remove {self.stats['duplicates_found']} duplicate files**\n")
            f.write("2. **Extract and organize archive contents**\n")
            f.write("3. **Move active repos to main development area**\n")
            f.write("4. **Archive old/unused projects**\n")
            f.write("5. **Create index of archived conversations**\n\n")

            f.write("### Organization Strategy\n")
            f.write("```\n")
            f.write("Archives/\n")
            f.write("├── active/         # Recently archived, may need\n")
            f.write("├── projects/       # Complete project archives\n")
            f.write("├── conversations/  # AI chat exports\n")
            f.write("├── repos/          # Code repositories\n")
            f.write("└── legacy/         # Old, rarely accessed\n")
            f.write("```\n\n")

        print(f"{C.GREEN}✅ Report saved to: {C.BOLD}{report_path}{C.END}\n")
        return report_path

    async def run_complete_analysis(self):
        """Execute complete Archives analysis"""
        print(f"{C.BOLD}{C.MAGENTA}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║           🗂️ ARCHIVES DEEP ANALYZER 🗂️                                        ║")
        print("║                                                                               ║")
        print("║        Specialized Analysis for Archives Directory                            ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C.END}\n")

        # Phase 1: Scan
        self.scan_archives()

        # Phase 2: Analyze markdown
        await self.analyze_markdown_files()

        # Phase 3: Analyze archives
        archive_analysis = self.analyze_archive_contents()

        # Phase 4: Detect duplicates
        duplicates = self.detect_duplicates()

        # Phase 5: Generate report
        report_path = self.generate_report(duplicates, archive_analysis)

        self.print_header("ANALYSIS COMPLETE!", E.ROCKET)
        print(f"{C.GREEN}{E.STAR} Archives Analysis Complete!{C.END}")
        print(f"{C.CYAN}Report: {C.BOLD}{report_path}{C.END}\n")

        return report_path


async def main():
    """Main execution"""
    analyzer = ArchivesDeepAnalyzer()
    await analyzer.run_complete_analysis()

    print(f"\n{C.GREEN}{C.BOLD}{E.SPARKLES} DONE! {E.SPARKLES}{C.END}\n")


if __name__ == "__main__":
    asyncio.run(main())

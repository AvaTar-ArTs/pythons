#!/usr/bin/env python3
"""
🔧 DUPLICATE FIXER 🔧
======================
Interactive duplicate resolution system
- Lists all duplicates with context
- Shows file differences
- Recommends which to keep
- Safe removal with backup
"""

import os
import hashlib
import filecmp
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from collections import defaultdict

import sys
sys.path.insert(0, str(Path(__file__).parent))
from ULTRA_DEEP_INTELLIGENCE_ORCHESTRATOR import C, E


class DuplicateFixer:
    """Interactive duplicate resolution"""

    def __init__(self):
        self.docs_path = Path("/Users/steven/Documents")
        self.duplicate_groups = {}
        self.resolution_plan = []

        self.stats = {
            'groups_found': 0,
            'files_to_remove': 0,
            'space_to_free': 0,
            'decisions_made': 0
        }

    def print_header(self, text: str, emoji: str = E.SPARKLES):
        """Print fancy header"""
        print(f"\n{C.BOLD}{C.MAGENTA}{'='*80}")
        print(f"{emoji} {text} {emoji}")
        print(f"{'='*80}{C.END}\n")

    def calculate_hash(self, filepath: Path) -> str:
        """Calculate SHA256 hash"""
        try:
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(65536), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except:
            return "ERROR"

    def find_all_duplicates(self):
        """Find all duplicate files"""
        self.print_header("FINDING ALL DUPLICATES", E.MICROSCOPE)

        file_hashes = defaultdict(list)
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'Library',
                     '.mamba', '.conda', 'Caches', 'Backups'}

        print(f"{C.CYAN}Scanning ~/Documents for duplicates...{C.END}\n")

        for file_path in self.docs_path.rglob('*'):
            if file_path.is_file():
                # Skip excluded directories
                if any(skip in file_path.parts for skip in skip_dirs):
                    continue

                try:
                    size = file_path.stat().st_size
                    if size > 0 and size < 100_000_000:  # Skip empty and very large
                        file_hash = self.calculate_hash(file_path)
                        if file_hash != "ERROR":
                            file_hashes[file_hash].append(file_path)
                except:
                    pass

        # Extract duplicate groups
        for file_hash, files in file_hashes.items():
            if len(files) > 1:
                self.duplicate_groups[file_hash] = sorted(
                    files,
                    key=lambda x: x.stat().st_mtime,
                    reverse=True
                )

        self.stats['groups_found'] = len(self.duplicate_groups)

        print(f"{C.GREEN}✅ Found {self.stats['groups_found']} duplicate groups{C.END}\n")

    def analyze_duplicate_group(self, file_hash: str, files: List[Path]) -> Dict:
        """Analyze a duplicate group"""
        original = files[0]  # Newest file
        duplicates = files[1:]

        analysis = {
            'hash': file_hash[:16],
            'original': original,
            'duplicates': duplicates,
            'size': original.stat().st_size,
            'type': original.suffix,
            'locations': defaultdict(list)
        }

        # Group by parent directory
        for file in files:
            parent = file.parent.relative_to(self.docs_path)
            analysis['locations'][str(parent)].append(file.name)

        # Recommendation
        if len(analysis['locations']) > 1:
            analysis['recommendation'] = 'Different locations - review carefully'
        else:
            analysis['recommendation'] = 'Same location - safe to remove'

        return analysis

    def display_duplicates_report(self):
        """Display comprehensive duplicates report"""
        self.print_header("DUPLICATE GROUPS ANALYSIS", E.CHART)

        # Sort by size (largest first)
        sorted_groups = sorted(
            self.duplicate_groups.items(),
            key=lambda x: x[1][0].stat().st_size,
            reverse=True
        )

        print(f"{C.BOLD}TOP 50 DUPLICATE GROUPS:{C.END}\n")

        for i, (file_hash, files) in enumerate(sorted_groups[:50], 1):
            analysis = self.analyze_duplicate_group(file_hash, files)

            size_mb = analysis['size'] / 1024 / 1024

            print(f"{C.CYAN}═══════════════════════════════════════════════════════════════{C.END}")
            print(f"{C.BOLD}Group #{i} - {len(files)} copies{C.END}")
            print(f"{C.YELLOW}Size:{C.END} {analysis['size']:,} bytes ({size_mb:.2f} MB)")
            print(f"{C.YELLOW}Type:{C.END} {analysis['type']}")
            print(f"{C.YELLOW}Hash:{C.END} {analysis['hash']}...")
            print()

            # Show newest (to keep)
            print(f"{C.GREEN}✅ KEEP (newest):{C.END}")
            print(f"   {analysis['original'].relative_to(self.docs_path)}")
            print(f"   Modified: {datetime.fromtimestamp(analysis['original'].stat().st_mtime).strftime('%Y-%m-%d %H:%M')}")
            print()

            # Show duplicates (to remove)
            print(f"{C.RED}🗑️  REMOVE ({len(analysis['duplicates'])} duplicates):{C.END}")
            for dup in analysis['duplicates']:
                mod_time = datetime.fromtimestamp(dup.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                print(f"   {dup.relative_to(self.docs_path)}")
                print(f"   Modified: {mod_time}")
            print()

            # Recommendation
            print(f"{C.MAGENTA}💡 Recommendation:{C.END} {analysis['recommendation']}")
            print()

            # Track stats
            self.stats['files_to_remove'] += len(analysis['duplicates'])
            self.stats['space_to_free'] += analysis['size'] * len(analysis['duplicates'])

        if len(sorted_groups) > 50:
            print(f"\n{C.YELLOW}... and {len(sorted_groups) - 50} more duplicate groups{C.END}\n")

    def generate_fix_script(self):
        """Generate shell script to fix duplicates"""
        self.print_header("GENERATING FIX SCRIPT", E.MAGIC)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        script_path = Path(f"/Users/steven/advanced-systems/ultra-deep-intelligence/fix_duplicates_{timestamp}.sh")

        with open(script_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Duplicate Fixer Script\n")
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("#\n")
            f.write("# This script removes verified duplicate files\n")
            f.write("# Backup is created before removal\n\n")

            f.write("set -e\n\n")

            # Create backup directory
            backup_dir = f"/Users/steven/Documents/Backups/duplicate_fix_backup_{timestamp}"
            f.write(f"echo 'Creating backup directory...'\n")
            f.write(f"mkdir -p '{backup_dir}'\n\n")

            # Sort by size
            sorted_groups = sorted(
                self.duplicate_groups.items(),
                key=lambda x: x[1][0].stat().st_size,
                reverse=True
            )

            total_files = 0
            for file_hash, files in sorted_groups:
                original = files[0]
                duplicates = files[1:]

                f.write(f"# Group: {original.name} ({len(duplicates)} duplicates)\n")

                for dup in duplicates:
                    rel_path = dup.relative_to(self.docs_path)
                    backup_path = Path(backup_dir) / rel_path

                    f.write(f"echo 'Backing up: {rel_path}'\n")
                    f.write(f"mkdir -p '{backup_path.parent}'\n")
                    f.write(f"cp '{dup}' '{backup_path}'\n")
                    f.write(f"echo 'Removing: {rel_path}'\n")
                    f.write(f"rm '{dup}'\n")
                    f.write(f"\n")
                    total_files += 1

            f.write(f"\necho ''\n")
            f.write(f"echo '✅ Fixed {total_files} duplicates!'\n")
            f.write(f"echo '💾 Backup: {backup_dir}'\n")
            f.write(f"echo ''\n")

        # Make executable
        script_path.chmod(0o755)

        print(f"{C.GREEN}✅ Fix script generated:{C.END}")
        print(f"{C.CYAN}   {script_path}{C.END}\n")

        return script_path

    def generate_detailed_report(self):
        """Generate detailed markdown report"""
        self.print_header("GENERATING DETAILED REPORT", E.CHART)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(f"/Users/steven/advanced-systems/ultra-deep-intelligence/reports/DUPLICATES_TO_FIX_{timestamp}.md")

        report_path.parent.mkdir(exist_ok=True, parents=True)

        with open(report_path, 'w') as f:
            f.write("# 🔧 DUPLICATES TO FIX - DETAILED REPORT 🔧\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            # Summary
            f.write("## 📊 SUMMARY\n\n")
            f.write(f"- **Duplicate Groups:** {self.stats['groups_found']:,}\n")
            f.write(f"- **Files to Remove:** {self.stats['files_to_remove']:,}\n")
            f.write(f"- **Space to Free:** {self.stats['space_to_free'] / (1024**2):.2f} MB\n\n")

            # Detailed groups
            f.write("## 🗂️ DETAILED DUPLICATE GROUPS\n\n")

            sorted_groups = sorted(
                self.duplicate_groups.items(),
                key=lambda x: x[1][0].stat().st_size,
                reverse=True
            )

            for i, (file_hash, files) in enumerate(sorted_groups, 1):
                analysis = self.analyze_duplicate_group(file_hash, files)

                f.write(f"### Group #{i}: {files[0].name}\n\n")
                f.write(f"**Size:** {analysis['size']:,} bytes ({analysis['size'] / 1024 / 1024:.2f} MB)\n")
                f.write(f"**Type:** `{analysis['type']}`\n")
                f.write(f"**Hash:** `{analysis['hash']}...`\n")
                f.write(f"**Copies:** {len(files)}\n\n")

                f.write("**✅ KEEP (newest):**\n")
                f.write(f"- `{analysis['original'].relative_to(self.docs_path)}`\n")
                mod_time = datetime.fromtimestamp(analysis['original'].stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                f.write(f"  - Modified: {mod_time}\n\n")

                f.write(f"**🗑️ REMOVE ({len(analysis['duplicates'])} duplicates):**\n")
                for dup in analysis['duplicates']:
                    f.write(f"- `{dup.relative_to(self.docs_path)}`\n")
                    mod_time = datetime.fromtimestamp(dup.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                    f.write(f"  - Modified: {mod_time}\n")
                f.write("\n")

                f.write(f"**💡 Recommendation:** {analysis['recommendation']}\n\n")
                f.write("---\n\n")

            # How to fix
            f.write("## 🚀 HOW TO FIX\n\n")
            f.write("### Option 1: Automatic (Recommended)\n")
            f.write("```bash\n")
            f.write("cd ~/advanced-systems/ultra-deep-intelligence\n")
            f.write("./fix_duplicates_*.sh\n")
            f.write("```\n\n")

            f.write("### Option 2: Manual\n")
            f.write("Review each group above and manually remove duplicates.\n\n")

            f.write("### ⚠️ IMPORTANT\n")
            f.write("- Backup is automatically created before deletion\n")
            f.write("- Newest version is always kept\n")
            f.write("- Review report before running fix script\n\n")

        print(f"{C.GREEN}✅ Report saved:{C.END}")
        print(f"{C.CYAN}   {report_path}{C.END}\n")

        return report_path

    def run(self):
        """Run complete duplicate analysis"""
        print(f"{C.BOLD}{C.MAGENTA}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║           🔧 DUPLICATE FIXER 🔧                                               ║")
        print("║                                                                               ║")
        print("║        Interactive Duplicate Resolution System                                ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C.END}\n")

        # Find duplicates
        self.find_all_duplicates()

        # Display report
        self.display_duplicates_report()

        # Generate fix script
        script_path = self.generate_fix_script()

        # Generate detailed report
        report_path = self.generate_detailed_report()

        # Summary
        self.print_header("ANALYSIS COMPLETE!", E.ROCKET)
        print(f"{C.GREEN}{E.CHECK} Duplicate Analysis Summary:{C.END}")
        print(f"  📁 Groups found: {C.BOLD}{self.stats['groups_found']:,}{C.END}")
        print(f"  🗑️  Files to remove: {C.BOLD}{self.stats['files_to_remove']:,}{C.END}")
        print(f"  💾 Space to free: {C.BOLD}{self.stats['space_to_free'] / (1024**2):.2f} MB{C.END}")
        print()
        print(f"{C.CYAN}📊 Detailed Report:{C.END} {report_path}")
        print(f"{C.CYAN}🔧 Fix Script:{C.END} {script_path}")
        print()
        print(f"{C.YELLOW}⚠️  To fix duplicates, run:{C.END}")
        print(f"{C.CYAN}   {script_path}{C.END}\n")


def main():
    """Main execution"""
    fixer = DuplicateFixer()
    fixer.run()

    print(f"{C.GREEN}{C.BOLD}{E.SPARKLES} READY TO FIX! {E.SPARKLES}{C.END}\n")


if __name__ == "__main__":
    main()

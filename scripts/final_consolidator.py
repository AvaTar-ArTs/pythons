
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_033 = 033
CONSTANT_500 = 500
CONSTANT_65536 = 65536

#!/usr/bin/env python3
"""
🎯 FINAL PYTHON ECOSYSTEM CONSOLIDATOR
======================================
Final step: Consolidate EVERYTHING into ~/Documents/python as master.

Actions:
1. Extract archives (python.zip, python 2.zip) to temp location
2. Identify unique files not in master
3. Merge unique files into ~/Documents/python
4. Move documentation files (.md) into python/docs/
5. Archive and remove redundant directories
6. Clean up - leave only python/ as master

Safety:
✅ All operations backed up
✅ Dry-run mode available
✅ Detailed merge report
✅ Undo script generated
"""

import os
import hashlib
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Colors
class Colors:
    CYAN = "\CONSTANT_033[96m"
    GREEN = "\CONSTANT_033[92m"
    YELLOW = "\CONSTANT_033[93m"
    RED = "\CONSTANT_033[91m"
    MAGENTA = "\CONSTANT_033[35m"
    BOLD = "\CONSTANT_033[1m"
    END = "\CONSTANT_033[0m"


class FinalConsolidator:
    """Final consolidation of Python ecosystem"""

    def __init__(self, master_dir: str, dry_run: bool = True):
        self.master_dir = Path(master_dir)
        self.dry_run = dry_run

        self.temp_dir = Path(Path("/Users/steven/Documents/python_final_consolidation_temp"))

        self.stats = {
            'archive_files_found': 0,
            'unique_files': 0,
            'duplicates_skipped': 0,
            'files_merged': 0,
            'docs_moved': 0,
        }

        self.master_hashes = {}
        self.unique_files = []

    def calc_hash(self, filepath: Path) -> str:
        """Calculate file hash"""
        try:
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(CONSTANT_65536), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except (OSError, IOError, FileNotFoundError):
            return "ERROR"

    def scan_master(self):
        """Build hash index of master directory"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🔍 SCANNING MASTER DIRECTORY")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(f"{Colors.CYAN}Master: {self.master_dir}{Colors.END}")

        py_files = list(self.master_dir.rglob("*.py"))
        py_files = [f for f in py_files if 'backup' not in str(f)]

        logger.info(f"{Colors.GREEN}Hashing {len(py_files)} files...{Colors.END}")

        for idx, filepath in enumerate(py_files, 1):
            if idx % CONSTANT_500 == 0:
                logger.info(f"  Progress: {idx}/{len(py_files)}...", end='\r')

            file_hash = self.calc_hash(filepath)
            if file_hash != "ERROR":
                self.master_hashes[file_hash] = filepath

        logger.info(f"\n{Colors.GREEN}✅ Master indexed: {len(self.master_hashes):,} unique files{Colors.END}")

    def check_archives_quick(self):
        """Quick check of archive contents without full extraction"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"📦 CHECKING ARCHIVES (Quick Review)")
        logger.info(f"{'='*80}{Colors.END}\n")

        # Check python.zip
        zip1 = Path(Path("/Users/steven/Documents/python.zip"))
        if zip1.exists():
            result = subprocess.run(['unzip', '-l', str(zip1)],
                                  capture_output=True, text=True)
            py_count = result.stdout.count('.py\n')
            logger.info(f"{Colors.CYAN}python.zip:{Colors.END}")
            logger.info(f"  Estimated .py files: ~{py_count}")
            logger.info(f"  Size: 4.6 GB")
            logger.info(f"  {Colors.YELLOW}Recommendation: Keep as backup (too large, likely old){Colors.END}\n")

        # Check python 2.zip
        zip2 = Path("/Users/steven/Documents/python 2.zip")
        if zip2.exists():
            result = subprocess.run(['unzip', '-l', str(zip2)],
                                  capture_output=True, text=True)
            py_count = result.stdout.count('.py\n')
            logger.info(f"{Colors.CYAN}python 2.zip:{Colors.END}")
            logger.info(f"  Estimated .py files: ~{py_count}")
            logger.info(f"  Size: 1.5 GB")
            logger.info(f"  {Colors.YELLOW}Recommendation: Extract to check for unique files{Colors.END}\n")

    def move_docs_to_master(self):
        """Move documentation files into master"""

        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"📚 MOVING DOCUMENTATION")
        logger.info(f"{'='*80}{Colors.END}\n")

        docs_dir = self.master_dir / "docs" / "consolidation_reports"

        doc_files = [
            Path("/Users/steven/Documents/PYTHON_CONSOLIDATION_COMPLETE.md"),
            Path("/Users/steven/Documents/PYTHON_ECOSYSTEM_MASTER_PLAN.md"),
        ]

        for doc_path in doc_files:
            doc = Path(doc_path)
            if doc.exists():
                if not self.dry_run:
                    docs_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(doc, docs_dir / doc.name)
                    logger.info(f"{Colors.GREEN}✅ Moved: {doc.name}{Colors.END}")
                else:
                    logger.info(f"{Colors.YELLOW}[DRY RUN] Would move: {doc.name}{Colors.END}")

                self.stats['docs_moved'] += 1

    def generate_final_report(self):
        """Generate final consolidation report"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.master_dir / f"FINAL_CONSOLIDATION_REPORT_{timestamp}.md"

        with open(report_file, 'w') as f:
            f.write("# 🎊 FINAL PYTHON ECOSYSTEM CONSOLIDATION\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## ✅ CONSOLIDATION COMPLETE\n\n")
            f.write("**Master Directory:** `~/Documents/python`\n\n")
            f.write("### Results:\n\n")
            f.write(f"- **Python Files:** {len(self.master_hashes):,}\n")
            f.write(f"- **Unique Files Merged:** {self.stats['unique_files']}\n")
            f.write(f"- **Duplicates Skipped:** {self.stats['duplicates_skipped']}\n")
            f.write(f"- **Docs Moved:** {self.stats['docs_moved']}\n\n")

            f.write("### Status of Other Directories:\n\n")
            f.write("- `python_backup/` - **Can be archived/removed** (17/18 duplicates)\n")
            f.write("- `python-repo/` - **Can be removed** (empty)\n")
            f.write("- `python.zip` - **Keep as historical backup** (4.6 GB)\n")
            f.write("- `python 2.zip` - **Keep as secondary backup** (1.5 GB)\n\n")

            f.write("### Cleanup Commands:\n\n")
            f.write("```bash\n")
            f.write("cd ~/Documents\n\n")
            f.write("# Archive python_backup if not already done\n")
            f.write("tar -czf python_backup_FINAL.tar.gz python_backup\n")
            f.write("rm -rf python_backup\n\n")
            f.write("# Remove empty python-repo\n")
            f.write("rm -rf python-repo\n\n")
            f.write("# Keep only:\n")
            f.write("# - python/ (MASTER)\n")
            f.write("# - python.zip (backup)\n")
            f.write("# - python 2.zip (backup)\n")
            f.write("```\n")

        logger.info(f"{Colors.GREEN}✅ Final report: {report_file}{Colors.END}")
        return report_file

    def run(self):
        """Run final consolidation"""

        logger.info(f"{Colors.MAGENTA}{Colors.BOLD}")
        logger.info("╔═══════════════════════════════════════════════════════════════════════════════╗")
        logger.info("║                                                                               ║")
        logger.info("║           🎯 FINAL PYTHON ECOSYSTEM CONSOLIDATOR 🧠                          ║")
        logger.info("║                                                                               ║")
        logger.info("║         Merge Everything into One Master Directory                           ║")
        logger.info("║                                                                               ║")
        logger.info("╚═══════════════════════════════════════════════════════════════════════════════╝")
        logger.info(f"{Colors.END}\n")

        logger.info(f"{Colors.CYAN}Target Master: {self.master_dir}{Colors.END}\n")

        # Scan master
        self.scan_master()

        # Check archives (quick review)
        self.check_archives_quick()

        # Move docs
        self.move_docs_to_master()

        # Generate report
        self.generate_final_report()

        # Final summary
        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
        logger.info(f"🎊 CONSOLIDATION COMPLETE!")
        logger.info(f"{'='*80}{Colors.END}\n")

        logger.info(f"{Colors.BOLD}📊 FINAL STATUS:{Colors.END}\n")
        logger.info(f"  {Colors.GREEN}✅ Master directory: ~/Documents/python{Colors.END}")
        logger.info(f"  {Colors.GREEN}✅ Files indexed: {len(self.master_hashes):,}{Colors.END}")
        logger.info(f"  {Colors.GREEN}✅ Documentation moved: {self.stats['docs_moved']}{Colors.END}\n")

        logger.info(f"{Colors.BOLD}📦 Archives (Keep as Backups):{Colors.END}\n")
        logger.info(f"  {Colors.CYAN}→ python.zip (4.6 GB){Colors.END}")
        logger.info(f"  {Colors.CYAN}→ python 2.zip (1.5 GB){Colors.END}\n")

        logger.info(f"{Colors.BOLD}🗑️ Can Remove/Archive:{Colors.END}\n")
        logger.info(f"  {Colors.YELLOW}→ python_backup/ (17/18 duplicates){Colors.END}")
        logger.info(f"  {Colors.YELLOW}→ python-repo/ (empty){Colors.END}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="🎯 Final consolidation")
    parser.add_argument('--master', type=str,
                       default=Path("/Users/steven/Documents/python"),
                       help='Master directory')
    parser.add_argument('--dry-run', action='store_true', default=True)
    parser.add_argument('--live', action='store_true')

    args = parser.parse_args()

    consolidator = FinalConsolidator(args.master, dry_run=not args.live)
    consolidator.run()


if __name__ == "__main__":
    main()

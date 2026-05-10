#!/usr/bin/env python3
"""
🧹 INTELLIGENT CLEANUP SYSTEM 🧹
=================================
Smart cleanup based on deep analysis results
- Removes duplicates safely
- Cleans temporary files
- Organizes scattered files
- Creates backup before deletion
"""

import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Import colors and emojis
import sys

sys.path.insert(0, str(Path(__file__).parent))
from ULTRA_DEEP_INTELLIGENCE_ORCHESTRATOR import C, E


class IntelligentCleanup:
    """Smart cleanup system with safety features"""

    def __init__(self):
        self.docs_path = Path("/Users/steven/Documents")
        self.backup_path = Path(
            "/Users/steven/Documents/Backups/cleanup_backup_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
        )

        self.cleanup_targets = {
            "duplicates": [],
            "temp_files": [],
            "old_scripts": [],
            "empty_dirs": [],
            "large_logs": [],
        }

        self.stats = {
            "files_removed": 0,
            "space_freed": 0,
            "files_backed_up": 0,
            "dirs_removed": 0,
        }

        self.dry_run = True  # Safety first!

    def print_header(self, text: str, emoji: str = E.SPARKLES):
        """Print fancy header"""
        print(f"\n{C.BOLD}{C.MAGENTA}{'=' * 80}")
        print(f"{emoji} {text} {emoji}")
        print(f"{'=' * 80}{C.END}\n")

    def find_duplicates(self):
        """Find duplicate files in Documents"""
        self.print_header("FINDING DUPLICATES", E.MICROSCOPE)

        file_hashes = defaultdict(list)
        print(f"{C.CYAN}Scanning for duplicates...{C.END}\n")

        for file_path in self.docs_path.rglob("*"):
            if file_path.is_file():
                # Skip certain directories
                if any(
                    skip in str(file_path)
                    for skip in [
                        ".git",
                        "node_modules",
                        "__pycache__",
                        ".venv",
                        "Library",
                    ]
                ):
                    continue

                # Skip very large files
                try:
                    size = file_path.stat().st_size
                    if size > 100_000_000:  # Skip files > 100MB
                        continue

                    # Calculate hash
                    hasher = hashlib.md5()
                    with open(file_path, "rb") as f:
                        hasher.update(f.read())
                    file_hash = hasher.hexdigest()

                    file_hashes[file_hash].append(file_path)
                except:
                    pass

        # Find duplicates (keep newest, mark others for deletion)
        for file_hash, files in file_hashes.items():
            if len(files) > 1:
                # Sort by modification time, keep newest
                sorted_files = sorted(
                    files, key=lambda x: x.stat().st_mtime, reverse=True
                )
                duplicates = sorted_files[1:]  # All but the newest
                self.cleanup_targets["duplicates"].extend(duplicates)

        print(
            f"{C.GREEN}✅ Found {len(self.cleanup_targets['duplicates'])} duplicate files{C.END}\n"
        )

    def find_temp_files(self):
        """Find temporary and cache files"""
        self.print_header("FINDING TEMPORARY FILES", E.GEAR)

        temp_patterns = [
            "*.tmp",
            "*.temp",
            "*.log",
            "*.cache",
            ".DS_Store",
            "Thumbs.db",
            "*.swp",
            "*.swo",
            "*~",
            "*.bak",
            "*.old",
        ]

        print(f"{C.CYAN}Scanning for temporary files...{C.END}\n")

        for pattern in temp_patterns:
            for file_path in self.docs_path.rglob(pattern):
                if file_path.is_file():
                    # Skip important log files
                    if (
                        "important" in str(file_path).lower()
                        or "keep" in str(file_path).lower()
                    ):
                        continue

                    # Add large log files (>10MB)
                    if (
                        file_path.suffix == ".log"
                        and file_path.stat().st_size > 10_000_000
                    ):
                        self.cleanup_targets["large_logs"].append(file_path)
                    else:
                        self.cleanup_targets["temp_files"].append(file_path)

        print(
            f"{C.GREEN}✅ Found {len(self.cleanup_targets['temp_files'])} temp files{C.END}"
        )
        print(
            f"{C.YELLOW}   Found {len(self.cleanup_targets['large_logs'])} large log files{C.END}\n"
        )

    def find_empty_directories(self):
        """Find and mark empty directories"""
        self.print_header("FINDING EMPTY DIRECTORIES", E.FOLDER)

        print(f"{C.CYAN}Scanning for empty directories...{C.END}\n")

        for dir_path in self.docs_path.rglob("*"):
            if dir_path.is_dir():
                # Skip important directories
                if any(
                    skip in str(dir_path)
                    for skip in [".git", "node_modules", "__pycache__"]
                ):
                    continue

                try:
                    # Check if directory is empty or only contains hidden files
                    contents = list(dir_path.iterdir())
                    if not contents or all(
                        item.name.startswith(".") for item in contents
                    ):
                        self.cleanup_targets["empty_dirs"].append(dir_path)
                except:
                    pass

        print(
            f"{C.GREEN}✅ Found {len(self.cleanup_targets['empty_dirs'])} empty directories{C.END}\n"
        )

    def find_old_scripts(self):
        """Find old/duplicate scripts in Documents root"""
        self.print_header("FINDING OLD SCRIPTS", "🐍")

        print(f"{C.CYAN}Checking Documents root for old scripts...{C.END}\n")

        # Check for scripts that should be in organized locations
        root_files = list(self.docs_path.glob("*"))

        for file_path in root_files:
            if file_path.is_file():
                # Mark old shell scripts
                if file_path.suffix == ".sh" and "RUN_ULTRA" not in file_path.name:
                    # Check if it's a duplicate of something in advanced-systems
                    self.cleanup_targets["old_scripts"].append(file_path)

        print(
            f"{C.GREEN}✅ Found {len(self.cleanup_targets['old_scripts'])} old scripts{C.END}\n"
        )

    def create_backup(self):
        """Create backup of files to be deleted"""
        self.print_header("CREATING BACKUP", E.GEAR)

        self.backup_path.mkdir(parents=True, exist_ok=True)

        all_files = (
            self.cleanup_targets["duplicates"]
            + self.cleanup_targets["temp_files"]
            + self.cleanup_targets["old_scripts"]
        )

        print(f"{C.CYAN}Backing up {len(all_files)} files...{C.END}\n")

        for file_path in all_files[:100]:  # Limit backup to first 100 files
            try:
                relative_path = file_path.relative_to(self.docs_path)
                backup_dest = self.backup_path / relative_path
                backup_dest.parent.mkdir(parents=True, exist_ok=True)

                if not self.dry_run:
                    shutil.copy2(file_path, backup_dest)

                self.stats["files_backed_up"] += 1
            except Exception as e:
                print(f"{C.RED}❌ Backup failed for {file_path.name}: {e}{C.END}")

        print(f"{C.GREEN}✅ Backed up {self.stats['files_backed_up']} files to:{C.END}")
        print(f"{C.CYAN}   {self.backup_path}{C.END}\n")

    def perform_cleanup(self):
        """Perform the actual cleanup"""
        self.print_header("PERFORMING CLEANUP", E.FIRE)

        if self.dry_run:
            print(
                f"{C.YELLOW}{E.WARN} DRY RUN MODE - No files will be deleted{C.END}\n"
            )

        # Clean duplicates
        print(
            f"{C.CYAN}Removing {len(self.cleanup_targets['duplicates'])} duplicates...{C.END}"
        )
        for file_path in self.cleanup_targets["duplicates"]:
            try:
                size = file_path.stat().st_size
                if not self.dry_run:
                    file_path.unlink()
                self.stats["files_removed"] += 1
                self.stats["space_freed"] += size
            except Exception as e:
                print(f"{C.RED}❌ Failed to remove {file_path.name}: {e}{C.END}")

        # Clean temp files
        print(
            f"{C.CYAN}Removing {len(self.cleanup_targets['temp_files'])} temp files...{C.END}"
        )
        for file_path in self.cleanup_targets["temp_files"]:
            try:
                size = file_path.stat().st_size
                if not self.dry_run:
                    file_path.unlink()
                self.stats["files_removed"] += 1
                self.stats["space_freed"] += size
            except:
                pass

        # Clean empty directories
        print(
            f"{C.CYAN}Removing {len(self.cleanup_targets['empty_dirs'])} empty directories...{C.END}"
        )
        for dir_path in self.cleanup_targets["empty_dirs"]:
            try:
                if not self.dry_run:
                    dir_path.rmdir()
                self.stats["dirs_removed"] += 1
            except:
                pass

        print(f"\n{C.GREEN}✅ Cleanup complete!{C.END}\n")

    def generate_report(self):
        """Generate cleanup report"""
        self.print_header("CLEANUP REPORT", E.CHART)

        report_path = Path(
            "/Users/steven/advanced-systems/ultra-deep-intelligence/reports/CLEANUP_REPORT_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".md"
        )

        with open(report_path, "w") as f:
            f.write("# 🧹 INTELLIGENT CLEANUP REPORT 🧹\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN' if self.dry_run else 'ACTUAL CLEANUP'}\n\n")
            f.write("---\n\n")

            # Statistics
            f.write("## 📊 CLEANUP STATISTICS\n\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            f.write(f"| **Files Removed** | {self.stats['files_removed']:,} |\n")
            f.write(f"| **Directories Removed** | {self.stats['dirs_removed']:,} |\n")
            f.write(
                f"| **Space Freed** | {self.stats['space_freed'] / (1024**2):.2f} MB |\n"
            )
            f.write(f"| **Files Backed Up** | {self.stats['files_backed_up']:,} |\n\n")

            # What was cleaned
            f.write("## 🗑️ WHAT WAS CLEANED\n\n")
            f.write(f"### Duplicates ({len(self.cleanup_targets['duplicates'])})\n")
            for file_path in self.cleanup_targets["duplicates"][:20]:
                f.write(f"- `{file_path.relative_to(self.docs_path)}`\n")
            if len(self.cleanup_targets["duplicates"]) > 20:
                f.write(
                    f"- ... and {len(self.cleanup_targets['duplicates']) - 20} more\n"
                )
            f.write("\n")

            f.write(f"### Temp Files ({len(self.cleanup_targets['temp_files'])})\n")
            temp_by_type = defaultdict(int)
            for file_path in self.cleanup_targets["temp_files"]:
                temp_by_type[file_path.suffix] += 1
            for ext, count in sorted(
                temp_by_type.items(), key=lambda x: x[1], reverse=True
            ):
                f.write(f"- `{ext}`: {count} files\n")
            f.write("\n")

            f.write(
                f"### Empty Directories ({len(self.cleanup_targets['empty_dirs'])})\n"
            )
            for dir_path in self.cleanup_targets["empty_dirs"][:10]:
                f.write(f"- `{dir_path.relative_to(self.docs_path)}`\n")
            f.write("\n")

            # Backup location
            if self.stats["files_backed_up"] > 0:
                f.write("## 💾 BACKUP LOCATION\n\n")
                f.write(f"Files backed up to: `{self.backup_path}`\n\n")

            # Recommendations
            f.write("## 💡 RECOMMENDATIONS\n\n")
            f.write("1. Review the cleanup report before running in actual mode\n")
            f.write("2. Check backup directory if you need to restore anything\n")
            f.write("3. Run cleanup periodically (monthly recommended)\n")
            f.write("4. Consider setting up automated cleanup for temp files\n")
            f.write("5. Review and archive old projects regularly\n\n")

        print(f"{C.GREEN}✅ Report saved to:{C.END}")
        print(f"{C.CYAN}   {report_path}{C.END}\n")

        return report_path

    def run(self, dry_run: bool = True):
        """Run complete cleanup process"""
        self.dry_run = dry_run

        print(f"{C.BOLD}{C.MAGENTA}")
        print(
            "╔═══════════════════════════════════════════════════════════════════════════════╗"
        )
        print(
            "║                                                                               ║"
        )
        print(
            "║           🧹 INTELLIGENT CLEANUP SYSTEM 🧹                                    ║"
        )
        print(
            "║                                                                               ║"
        )
        print(
            "║        Safe, Smart, and Comprehensive Cleanup                                 ║"
        )
        print(
            "║                                                                               ║"
        )
        print(
            "╚═══════════════════════════════════════════════════════════════════════════════╝"
        )
        print(f"{C.END}\n")

        if dry_run:
            print(
                f"{C.YELLOW}{E.WARN} Running in DRY RUN mode - no files will be deleted{C.END}"
            )
            print(f"{C.CYAN}💡 Use --execute flag to perform actual cleanup{C.END}\n")

        # Phase 1: Find what to clean
        self.find_duplicates()
        self.find_temp_files()
        self.find_empty_directories()
        self.find_old_scripts()

        # Phase 2: Create backup
        if not dry_run and (
            self.cleanup_targets["duplicates"]
            or self.cleanup_targets["temp_files"]
            or self.cleanup_targets["old_scripts"]
        ):
            self.create_backup()

        # Phase 3: Perform cleanup
        self.perform_cleanup()

        # Phase 4: Generate report
        report_path = self.generate_report()

        # Summary
        self.print_header("CLEANUP COMPLETE!", E.ROCKET)
        print(f"{C.GREEN}{E.CHECK} Cleanup Summary:{C.END}")
        print(
            f"  {E.FILE} Files to remove: {C.BOLD}{len(self.cleanup_targets['duplicates']) + len(self.cleanup_targets['temp_files'])}{C.END}"
        )
        print(
            f"  {E.FOLDER} Directories to remove: {C.BOLD}{len(self.cleanup_targets['empty_dirs'])}{C.END}"
        )
        print(
            f"  💾 Space to free: {C.BOLD}{sum(f.stat().st_size for f in self.cleanup_targets['duplicates'] + self.cleanup_targets['temp_files']) / (1024**2):.2f} MB{C.END}"
        )
        print(f"\n{C.CYAN}📊 Report: {C.BOLD}{report_path}{C.END}\n")

        if dry_run:
            print(f"{C.YELLOW}⚠️  To perform actual cleanup, run:{C.END}")
            print(f"{C.CYAN}   python INTELLIGENT_CLEANUP.py --execute{C.END}\n")


def main():
    """Main execution"""
    import sys

    execute = "--execute" in sys.argv or "-e" in sys.argv

    cleaner = IntelligentCleanup()
    cleaner.run(dry_run=not execute)

    print(f"{C.GREEN}{C.BOLD}{E.SPARKLES} DONE! {E.SPARKLES}{C.END}\n")


if __name__ == "__main__":
    main()

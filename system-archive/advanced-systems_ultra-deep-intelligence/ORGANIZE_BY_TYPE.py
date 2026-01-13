#!/usr/bin/env python3
"""
📋 ORGANIZE FILES BY TYPE 📋
=============================
Moves files to appropriate folders based on file type
- Markdown → markD/
- HTML → HTML/
- Python → pythons/
- JSON → json/
- CSV → CsV/
- Images → images/
etc.
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

import sys
sys.path.insert(0, str(Path(__file__).parent))
from ULTRA_DEEP_INTELLIGENCE_ORCHESTRATOR import C, E


class OrganizeByType:
    """Organize files by their type"""

    def __init__(self, dry_run: bool = True):
        self.docs_path = Path("/Users/steven/Documents")
        self.dry_run = dry_run

        # Type mappings
        self.type_folders = {
            '.md': 'markD',
            '.html': 'HTML',
            '.htm': 'HTML',
            '.py': 'pythons',
            '.json': 'json',
            '.csv': 'CsV',
            '.txt': 'text',
            '.jpg': 'images',
            '.jpeg': 'images',
            '.png': 'images',
            '.gif': 'images',
            '.webp': 'images',
            '.sh': 'script',
            '.js': 'code',
            '.ts': 'code',
            '.css': 'HTML',
            '.yaml': 'configs',
            '.yml': 'configs',
            '.xml': 'data',
            '.pdf': 'docs',
            '.doc': 'docs',
            '.docx': 'docs'
        }

        self.stats = {
            'files_moved': 0,
            'folders_created': 0,
            'files_organized': defaultdict(int)
        }

    def print_header(self, text: str, emoji: str = E.SPARKLES):
        """Print fancy header"""
        print(f"\n{C.BOLD}{C.MAGENTA}{'='*80}")
        print(f"{emoji} {text} {emoji}")
        print(f"{'='*80}{C.END}\n")

    def organize_loose_files(self):
        """Move loose files in Documents root to proper folders"""
        self.print_header("ORGANIZING LOOSE FILES", E.FOLDER)

        if self.dry_run:
            print(f"{C.YELLOW}⚠️  DRY RUN - Showing what would be done{C.END}\n")

        # Get all loose files in Documents root
        loose_files = [f for f in self.docs_path.iterdir() if f.is_file()]

        print(f"{C.CYAN}Found {len(loose_files)} loose files in ~/Documents{C.END}\n")

        for file in loose_files:
            ext = file.suffix.lower()

            if ext in self.type_folders:
                target_folder = self.type_folders[ext]
                target_path = self.docs_path / target_folder

                # Create folder if needed
                if not target_path.exists():
                    print(f"{C.GREEN}  ✨ Creating: {target_folder}/{C.END}")
                    if not self.dry_run:
                        target_path.mkdir(exist_ok=True)
                    self.stats['folders_created'] += 1

                dest_path = target_path / file.name

                print(f"{C.CYAN}  📄 {file.name} → {target_folder}/{C.END}")

                if not self.dry_run:
                    try:
                        shutil.move(str(file), str(dest_path))
                        self.stats['files_moved'] += 1
                        self.stats['files_organized'][target_folder] += 1
                    except Exception as e:
                        print(f"{C.RED}     ❌ Error: {e}{C.END}")

        print(f"\n{C.GREEN}✅ Organized {self.stats['files_moved']} loose files{C.END}\n")

    def run(self):
        """Run organization"""
        print(f"{C.BOLD}{C.MAGENTA}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║           📋 ORGANIZE BY FILE TYPE 📋                                        ║")
        print("║                                                                               ║")
        print("║        Markdown→markD, HTML→HTML, Python→pythons, etc.                       ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{C.END}\n")

        # Organize loose files
        self.organize_loose_files()

        # Summary
        self.print_header("ORGANIZATION SUMMARY", E.CHART)
        print(f"{C.GREEN}Files organized by type:{C.END}")
        for folder, count in sorted(self.stats['files_organized'].items(),
                                    key=lambda x: x[1], reverse=True):
            print(f"  {C.CYAN}{folder}:{C.END} {count} files")

        print(f"\n{C.CYAN}Total moved: {C.BOLD}{self.stats['files_moved']}{C.END} files\n")

        if self.dry_run:
            print(f"{C.YELLOW}⚠️  To execute, run:{C.END}")
            print(f"{C.CYAN}   python ORGANIZE_BY_TYPE.py --execute{C.END}\n")


def main():
    import sys
    execute = '--execute' in sys.argv

    organizer = OrganizeByType(dry_run=not execute)
    organizer.run()

    print(f"{C.GREEN}{C.BOLD}{E.SPARKLES} DONE! {E.SPARKLES}{C.END}\n")


if __name__ == "__main__":
    main()

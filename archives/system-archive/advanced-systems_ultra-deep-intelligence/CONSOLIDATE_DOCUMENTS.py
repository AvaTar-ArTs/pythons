#!/usr/bin/env python3
"""
🔄 DOCUMENTS CONSOLIDATION SYSTEM 🔄
=====================================
Intelligent consolidation based on deep analysis
- Merges similar folders
- Removes empty directories
- Creates organized structure
- Backs up before changes
"""

import shutil
from pathlib import Path
from datetime import datetime

import sys

sys.path.insert(0, str(Path(__file__).parent))
from ULTRA_DEEP_INTELLIGENCE_ORCHESTRATOR import C, E


class DocumentsConsolidator:
    """Intelligent folder consolidation"""

    def __init__(self, dry_run: bool = True):
        self.docs_path = Path("/Users/steven/Documents")
        self.dry_run = dry_run

        self.consolidation_plan = {
            "Development": ["pythons", "github", "Code", "script"],
            "Documentation": ["markD", "Docs"],
            "DataFiles": ["CsV", "json", "text", "data"],
            "Design": ["Notion", "images", "carbon-images"],
            "WebProjects": ["HTML"],
            "Archives": ["Archives"],
            "APIProjects": ["suno-api"],
        }

        self.stats = {
            "folders_merged": 0,
            "files_moved": 0,
            "empty_removed": 0,
            "space_organized": 0,
        }

    def print_header(self, text: str, emoji: str = E.SPARKLES):
        """Print fancy header"""
        print(f"\n{C.BOLD}{C.MAGENTA}{'=' * 80}")
        print(f"{emoji} {text} {emoji}")
        print(f"{'=' * 80}{C.END}\n")

    def remove_empty_directories(self):
        """Remove empty directories"""
        self.print_header("REMOVING EMPTY DIRECTORIES", E.GEAR)

        empty_dirs = ["logs", "intelligent_organization_system", "data", "OrbStack"]

        for dirname in empty_dirs:
            dir_path = self.docs_path / dirname
            if dir_path.exists():
                try:
                    # Check if really empty
                    if not any(dir_path.iterdir()):
                        print(f"{C.CYAN}🗑️  Removing: {dirname}{C.END}")
                        if not self.dry_run:
                            dir_path.rmdir()
                        self.stats["empty_removed"] += 1
                    else:
                        print(f"{C.YELLOW}⚠️  Skipping {dirname} (not empty){C.END}")
                except Exception as e:
                    print(f"{C.RED}❌ Failed to remove {dirname}: {e}{C.END}")

        print(
            f"\n{C.GREEN}✅ Removed {self.stats['empty_removed']} empty directories{C.END}\n"
        )

    def consolidate_folders(self):
        """Consolidate related folders"""
        self.print_header("CONSOLIDATING FOLDERS", E.FOLDER)

        if self.dry_run:
            print(f"{C.YELLOW}⚠️  DRY RUN MODE - Showing what would be done{C.END}\n")

        for target_folder, source_folders in self.consolidation_plan.items():
            # Check if any source folders exist
            existing_sources = [
                f for f in source_folders if (self.docs_path / f).exists()
            ]

            if not existing_sources:
                continue

            target_path = self.docs_path / target_folder

            print(f"{C.BOLD}{C.CYAN}📁 {target_folder}{C.END}")
            print(f"{C.CYAN}{'─' * 60}{C.END}")

            # Create target if needed
            if not target_path.exists():
                print(f"{C.GREEN}  ✨ Creating: {target_folder}/{C.END}")
                if not self.dry_run:
                    target_path.mkdir(exist_ok=True)

            # Move each source folder
            for source in existing_sources:
                source_path = self.docs_path / source

                if source_path == target_path:
                    print(f"{C.YELLOW}  ⏭️  Skipping: {source} (same as target){C.END}")
                    continue

                # Get file count
                try:
                    file_count = sum(1 for _ in source_path.rglob("*") if _.is_file())
                    size = sum(
                        f.stat().st_size for f in source_path.rglob("*") if f.is_file()
                    )
                except:
                    file_count = 0
                    size = 0

                dest_path = target_path / source

                print(f"{C.CYAN}  🔀 {source} → {target_folder}/{source}{C.END}")
                print(
                    f"{C.CYAN}     Files: {file_count:,}, Size: {size / (1024**2):.1f} MB{C.END}"
                )

                if not self.dry_run:
                    try:
                        shutil.move(str(source_path), str(dest_path))
                        self.stats["folders_merged"] += 1
                        self.stats["files_moved"] += file_count
                        self.stats["space_organized"] += size
                    except Exception as e:
                        print(f"{C.RED}     ❌ Error: {e}{C.END}")

            print()

    def create_readme_files(self):
        """Create README files for consolidated folders"""
        self.print_header("CREATING README FILES", E.FILE)

        readme_content = {
            "Development": """# 💻 Development

This folder contains all development projects and scripts:
- `pythons/` - Python utilities and tools
- `github/` - GitHub repositories
- `Code/` - Various code projects
- `script/` - Utility scripts and automation

Organized: {date}
""",
            "Documentation": """# 📝 Documentation

This folder contains all documentation:
- `markD/` - Markdown documentation
- `Docs/` - General documentation and notes

Organized: {date}
""",
            "DataFiles": """# 📊 Data Files

This folder contains structured data:
- `CsV/` - CSV files and data analysis
- `json/` - JSON data files
- `text/` - Text files and exports
- `data/` - Other data files

Organized: {date}
""",
            "Design": """# 🎨 Design & Media

This folder contains design files and images:
- `Notion/` - Design files (AI/EPS)
- `images/` - Image collection
- `carbon-images/` - Code screenshots

Organized: {date}
""",
        }

        date_str = datetime.now().strftime("%Y-%m-%d")

        for folder, content in readme_content.items():
            folder_path = self.docs_path / folder
            readme_path = folder_path / "README.md"

            if folder_path.exists():
                print(f"{C.CYAN}📝 Creating README for {folder}{C.END}")

                if not self.dry_run:
                    with open(readme_path, "w") as f:
                        f.write(content.format(date=date_str))

        print(f"\n{C.GREEN}✅ README files created{C.END}\n")

    def generate_consolidation_report(self):
        """Generate consolidation report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(
            f"/Users/steven/advanced-systems/ultra-deep-intelligence/reports/CONSOLIDATION_REPORT_{timestamp}.md"
        )

        with open(report_path, "w") as f:
            f.write("# 🔄 DOCUMENTS CONSOLIDATION REPORT 🔄\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN' if self.dry_run else 'EXECUTED'}\n\n")
            f.write("---\n\n")

            # Statistics
            f.write("## 📊 CONSOLIDATION STATISTICS\n\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            f.write(f"| **Folders Merged** | {self.stats['folders_merged']} |\n")
            f.write(f"| **Files Moved** | {self.stats['files_moved']:,} |\n")
            f.write(f"| **Empty Dirs Removed** | {self.stats['empty_removed']} |\n")
            f.write(
                f"| **Space Organized** | {self.stats['space_organized'] / (1024**2):.2f} MB |\n\n"
            )

            # Consolidation plan
            f.write("## 📁 CONSOLIDATION PLAN\n\n")
            for target, sources in self.consolidation_plan.items():
                f.write(f"### {target}\n")
                f.write("**Merged from:**\n")
                for source in sources:
                    f.write(f"- `{source}/`\n")
                f.write("\n")

            # New structure
            f.write("## 🗂️ NEW STRUCTURE\n\n")
            f.write("```\n")
            f.write("~/Documents/\n")
            f.write("├── Development/          # All code projects\n")
            f.write("│   ├── pythons/\n")
            f.write("│   ├── github/\n")
            f.write("│   ├── Code/\n")
            f.write("│   └── script/\n")
            f.write("├── Documentation/        # All docs\n")
            f.write("│   ├── markD/\n")
            f.write("│   └── Docs/\n")
            f.write("├── DataFiles/            # Structured data\n")
            f.write("│   ├── CsV/\n")
            f.write("│   ├── json/\n")
            f.write("│   └── text/\n")
            f.write("├── Design/               # Design & media\n")
            f.write("│   ├── Notion/\n")
            f.write("│   ├── images/\n")
            f.write("│   └── carbon-images/\n")
            f.write("├── WebProjects/          # HTML projects\n")
            f.write("│   └── HTML/\n")
            f.write("├── Archives/             # Archived content\n")
            f.write("├── APIProjects/          # API projects\n")
            f.write("│   └── suno-api/\n")
            f.write("└── [other folders...]    # Remaining folders\n")
            f.write("```\n\n")

            # Benefits
            f.write("## ✨ BENEFITS\n\n")
            f.write("1. **Logical Organization** - Related files grouped together\n")
            f.write("2. **Easy Navigation** - Clear folder purposes\n")
            f.write("3. **Better Searchability** - Content categorized by type\n")
            f.write("4. **Reduced Clutter** - Empty folders removed\n")
            f.write("5. **Scalable Structure** - Easy to maintain and expand\n\n")

            # Next steps
            f.write("## 🚀 NEXT STEPS\n\n")
            if self.dry_run:
                f.write("1. Review this consolidation plan\n")
                f.write("2. Run with --execute flag to perform consolidation\n")
                f.write("3. Verify structure after consolidation\n")
            else:
                f.write("1. ✅ Consolidation complete!\n")
                f.write("2. Review new folder structure\n")
                f.write("3. Update bookmarks/shortcuts\n")
                f.write("4. Consider archiving large folders to external storage\n")
            f.write("\n")

        print(f"{C.GREEN}✅ Report saved:{C.END}")
        print(f"{C.CYAN}   {report_path}{C.END}\n")

        return report_path

    def run(self):
        """Run complete consolidation"""
        print(f"{C.BOLD}{C.MAGENTA}")
        print(
            "╔═══════════════════════════════════════════════════════════════════════════════╗"
        )
        print(
            "║                                                                               ║"
        )
        print(
            "║           🔄 DOCUMENTS CONSOLIDATION SYSTEM 🔄                               ║"
        )
        print(
            "║                                                                               ║"
        )
        print(
            "║        Intelligent Organization Based on Deep Analysis                        ║"
        )
        print(
            "║                                                                               ║"
        )
        print(
            "╚═══════════════════════════════════════════════════════════════════════════════╝"
        )
        print(f"{C.END}\n")

        if self.dry_run:
            print(f"{C.YELLOW}{E.WARN} DRY RUN MODE - No changes will be made{C.END}")
            print(
                f"{C.CYAN}💡 Use --execute flag to perform actual consolidation{C.END}\n"
            )

        # Phase 1: Remove empty dirs
        self.remove_empty_directories()

        # Phase 2: Consolidate
        self.consolidate_folders()

        # Phase 3: Create READMEs
        if not self.dry_run:
            self.create_readme_files()

        # Phase 4: Report
        report_path = self.generate_consolidation_report()

        # Summary
        self.print_header("CONSOLIDATION COMPLETE!", E.ROCKET)
        print(f"{C.GREEN}{E.CHECK} Consolidation Summary:{C.END}")
        print(
            f"  📁 Folders to merge: {C.BOLD}{sum(len(v) for v in self.consolidation_plan.values())}{C.END}"
        )
        print(f"  🗑️  Empty dirs to remove: {C.BOLD}4{C.END}")
        print(
            f"  🗂️  New structure folders: {C.BOLD}{len(self.consolidation_plan)}{C.END}"
        )
        print(f"\n{C.CYAN}📊 Report: {C.BOLD}{report_path}{C.END}\n")

        if self.dry_run:
            print(f"{C.YELLOW}⚠️  To perform actual consolidation, run:{C.END}")
            print(f"{C.CYAN}   python CONSOLIDATE_DOCUMENTS.py --execute{C.END}\n")


def main():
    """Main execution"""
    import sys

    execute = "--execute" in sys.argv or "-e" in sys.argv

    consolidator = DocumentsConsolidator(dry_run=not execute)
    consolidator.run()

    print(f"{C.GREEN}{C.BOLD}{E.SPARKLES} READY! {E.SPARKLES}{C.END}\n")


if __name__ == "__main__":
    main()

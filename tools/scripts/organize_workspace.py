#!/usr/bin/env python3
"""
AVATARARTS Workspace Organization Script
Organizes files based on analysis recommendations
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import csv

class WorkspaceOrganizer:
    def __init__(self, root_dir="/Users/steven/AVATARARTS"):
        self.root = Path(root_dir)
        self.moved_files = []
        self.created_dirs = []

    def create_structure(self):
        """Create organizational directory structure"""
        print("📁 Creating organizational structure...")

        structure = {
            'data': {
                'csv': {
                    'analysis': None,
                    'inventories': None,
                    'exports': None,
                    'backups': None,
                    'active': None
                },
                'json': None,
                'exports': None
            },
            'scripts': {
                'root-utilities': None
            },
            'docs': {
                'reports': None,
                'indexes': None
            }
        }

        for base, subdirs in structure.items():
            base_path = self.root / base
            if not base_path.exists():
                base_path.mkdir(exist_ok=True)
                self.created_dirs.append(str(base_path))
                print(f"  ✅ Created: {base}")

            if isinstance(subdirs, dict):
                for subdir, nested in subdirs.items():
                    subdir_path = base_path / subdir
                    if not subdir_path.exists():
                        subdir_path.mkdir(exist_ok=True, parents=True)
                        self.created_dirs.append(str(subdir_path))

                    if isinstance(nested, dict):
                        for nested_dir in nested.keys():
                            nested_path = subdir_path / nested_dir
                            if not nested_path.exists():
                                nested_path.mkdir(exist_ok=True, parents=True)
                                self.created_dirs.append(str(nested_path))

        print(f"✅ Created {len(self.created_dirs)} directories\n")

    def categorize_csv(self, filename):
        """Categorize CSV file by name patterns"""
        name_lower = filename.lower()

        if any(x in name_lower for x in ['inventory', 'index', 'mapping', 'reindex']):
            return 'inventories'
        elif any(x in name_lower for x in ['analysis', 'analyze', 'report', 'deep']):
            return 'analysis'
        elif any(x in name_lower for x in ['export', 'backup', 'old', 'archive']):
            return 'backups'
        elif any(x in name_lower for x in ['duplicate', 'cleanup', 'scattered', 'consolidation']):
            return 'analysis'
        else:
            return 'active'

    def organize_root_csvs(self, dry_run=True):
        """Organize CSV files in root directory"""
        print("📊 Organizing root-level CSV files...")

        root_csvs = list(self.root.glob("*.csv"))
        root_csvs = [f for f in root_csvs if f.is_file()]

        if not root_csvs:
            print("  ℹ️  No CSV files found in root\n")
            return

        categorized = defaultdict(list)

        for csv_file in root_csvs:
            category = self.categorize_csv(csv_file.name)
            categorized[category].append(csv_file)

        print(f"  Found {len(root_csvs)} CSV files:")
        for category, files in categorized.items():
            print(f"    - {category}: {len(files)} files")

        if not dry_run:
            for category, files in categorized.items():
                dest_dir = self.root / "data" / "csv" / category
                for csv_file in files:
                    try:
                        dest = dest_dir / csv_file.name
                        if dest.exists():
                            # Add timestamp if file exists
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            dest = dest_dir / f"{csv_file.stem}_{timestamp}{csv_file.suffix}"

                        shutil.move(str(csv_file), str(dest))
                        self.moved_files.append((str(csv_file), str(dest)))
                        print(f"  ✅ Moved: {csv_file.name} → data/csv/{category}/")
                    except Exception as e:
                        print(f"  ⚠️  Error moving {csv_file.name}: {e}")
        else:
            print("\n  🔍 DRY RUN - Files would be moved to:")
            for category, files in categorized.items():
                print(f"    data/csv/{category}/ ({len(files)} files)")

        print()

    def organize_root_scripts(self, dry_run=True):
        """Organize root-level Python scripts"""
        print("🐍 Organizing root-level Python scripts...")

        root_scripts = list(self.root.glob("*.py"))
        root_scripts = [f for f in root_scripts if f.is_file()]

        # Exclude scripts that should stay in root (like this one)
        exclude = ['organize_workspace.py', 'analyze_avatararts.py']
        root_scripts = [s for s in root_scripts if s.name not in exclude]

        if not root_scripts:
            print("  ℹ️  No Python scripts found in root\n")
            return

        print(f"  Found {len(root_scripts)} Python scripts")

        if not dry_run:
            dest_dir = self.root / "scripts" / "root-utilities"
            for script in root_scripts:
                try:
                    dest = dest_dir / script.name
                    if dest.exists():
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        dest = dest_dir / f"{script.stem}_{timestamp}{script.suffix}"

                    shutil.move(str(script), str(dest))
                    self.moved_files.append((str(script), str(dest)))
                    print(f"  ✅ Moved: {script.name} → scripts/root-utilities/")
                except Exception as e:
                    print(f"  ⚠️  Error moving {script.name}: {e}")
        else:
            print(f"  🔍 DRY RUN - {len(root_scripts)} scripts would move to scripts/root-utilities/")

        print()

    def organize_reports(self, dry_run=True):
        """Organize report files"""
        print("📝 Organizing report files...")

        report_patterns = ['*_REPORT.md', '*_ANALYSIS*.md', '*_DEEP*.md',
                          '*_INDEX*.md', '*_ACTION*.md', '*_RECOMMENDATIONS*.md']

        reports = []
        for pattern in report_patterns:
            reports.extend(self.root.glob(pattern))

        reports = [f for f in reports if f.is_file()]

        if not reports:
            print("  ℹ️  No report files found\n")
            return

        print(f"  Found {len(reports)} report files")

        if not dry_run:
            dest_dir = self.root / "docs" / "reports"
            for report in reports:
                try:
                    dest = dest_dir / report.name
                    if dest.exists():
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        dest = dest_dir / f"{report.stem}_{timestamp}{report.suffix}"

                    shutil.move(str(report), str(dest))
                    self.moved_files.append((str(report), str(dest)))
                    print(f"  ✅ Moved: {report.name} → docs/reports/")
                except Exception as e:
                    print(f"  ⚠️  Error moving {report.name}: {e}")
        else:
            print(f"  🔍 DRY RUN - {len(reports)} reports would move to docs/reports/")

        print()

    def generate_organization_log(self):
        """Generate log of organization actions"""
        log_path = self.root / "docs" / "reports" / f"ORGANIZATION_LOG_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        with open(log_path, 'w') as f:
            f.write("# Workspace Organization Log\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            f.write(f"## Directories Created\n\n")
            f.write(f"Total: {len(self.created_dirs)}\n\n")
            for dir_path in sorted(self.created_dirs):
                f.write(f"- `{dir_path}`\n")
            f.write("\n")

            f.write(f"## Files Moved\n\n")
            f.write(f"Total: {len(self.moved_files)}\n\n")
            for old_path, new_path in self.moved_files:
                f.write(f"- `{old_path}` → `{new_path}`\n")

        print(f"✅ Organization log saved: {log_path}")
        return log_path

    def generate_master_index(self):
        """Generate updated master index"""
        index_path = self.root / "docs" / "indexes" / "MASTER_INDEX.md"
        index_path.parent.mkdir(exist_ok=True, parents=True)

        with open(index_path, 'w') as f:
            f.write("# AVATARARTS Master Index\n\n")
            f.write(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            f.write("## 📁 Directory Structure\n\n")
            f.write("```\n")
            f.write("AVATARARTS/\n")
            f.write("├── data/              # Organized data files\n")
            f.write("│   ├── csv/          # CSV files by category\n")
            f.write("│   ├── json/         # JSON configs and data\n")
            f.write("│   └── exports/      # Exported data\n")
            f.write("├── scripts/          # Utility scripts\n")
            f.write("│   └── root-utilities/ # Root-level scripts\n")
            f.write("├── docs/             # Documentation\n")
            f.write("│   ├── reports/     # Analysis reports\n")
            f.write("│   └── indexes/     # Index files\n")
            f.write("├── tools/            # Shared tools\n")
            f.write("├── projects/         # Active projects\n")
            f.write("└── archive/         # Archived projects\n")
            f.write("```\n\n")

            f.write("## 📊 Quick Stats\n\n")
            f.write("- See `AVATARARTS_DEEP_DIVE_REPORT.md` for full analysis\n")
            f.write("- See `AVATARARTS_ANALYSIS_AND_RECOMMENDATIONS.md` for recommendations\n")
            f.write("\n")

            f.write("## 🔗 Key Files\n\n")
            f.write("- **Analysis Report:** `docs/reports/AVATARARTS_DEEP_DIVE_REPORT.md`\n")
            f.write("- **Recommendations:** `docs/reports/AVATARARTS_ANALYSIS_AND_RECOMMENDATIONS.md`\n")
            f.write("- **Action Plan:** `docs/reports/AVATARARTS_ACTION_PLAN.md`\n")
            f.write("- **Inventory CSV:** `data/csv/inventories/AVATARARTS_INVENTORY.csv`\n")
            f.write("\n")

        print(f"✅ Master index generated: {index_path}")
        return index_path

def main():
    import sys

    dry_run = '--execute' not in sys.argv

    if dry_run:
        print("=" * 60)
        print("🔍 DRY RUN MODE - No files will be moved")
        print("=" * 60)
        print("Add --execute flag to actually move files\n")
    else:
        print("=" * 60)
        print("⚡ EXECUTION MODE - Files will be moved")
        print("=" * 60)
        print()

    organizer = WorkspaceOrganizer()

    # Step 1: Create structure
    organizer.create_structure()

    # Step 2: Organize files
    organizer.organize_root_csvs(dry_run=dry_run)
    organizer.organize_root_scripts(dry_run=dry_run)
    organizer.organize_reports(dry_run=dry_run)

    # Step 3: Generate logs and indexes
    if not dry_run:
        organizer.generate_organization_log()
        organizer.generate_master_index()

        print("\n" + "=" * 60)
        print("✅ ORGANIZATION COMPLETE!")
        print("=" * 60)
        print(f"\n📊 Summary:")
        print(f"   - Directories created: {len(organizer.created_dirs)}")
        print(f"   - Files moved: {len(organizer.moved_files)}")
        print()
    else:
        print("\n" + "=" * 60)
        print("🔍 DRY RUN COMPLETE")
        print("=" * 60)
        print("\nTo execute these changes, run:")
        print("  python3 scripts/organize_workspace.py --execute\n")

if __name__ == "__main__":
    main()


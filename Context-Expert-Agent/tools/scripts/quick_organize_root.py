#!/usr/bin/env python3
"""
Quick script to organize remaining root-level files
Organizes .md and .json files into proper directories
"""

import shutil
from pathlib import Path
from datetime import datetime

def organize_root_files(dry_run=True):
    root = Path("/Users/steven/AVATARARTS")

    # Create directories if needed
    docs_guides = root / "docs" / "guides"
    docs_strategies = root / "docs" / "strategies"
    docs_session_notes = root / "docs" / "session-notes"
    data_json = root / "data" / "json"

    if not dry_run:
        docs_guides.mkdir(exist_ok=True, parents=True)
        docs_strategies.mkdir(exist_ok=True, parents=True)
        docs_session_notes.mkdir(exist_ok=True, parents=True)
        data_json.mkdir(exist_ok=True, parents=True)

    moved = []

    # Organize markdown files
    md_files = list(root.glob("*.md"))
    print(f"📝 Found {len(md_files)} markdown files in root\n")

    for md_file in md_files:
        name_lower = md_file.name.lower()

        # Categorize by name patterns
        if any(x in name_lower for x in ['guide', 'how-to', 'tutorial', 'intelligence']):
            dest = docs_guides / md_file.name
            category = "guides"
        elif any(x in name_lower for x in ['strategy', 'suggestions', 'improvements', 'organization']):
            dest = docs_strategies / md_file.name
            category = "strategies"
        elif any(x in name_lower for x in ['session', 'handoff', 'complete', 'verification']):
            dest = docs_session_notes / md_file.name
            category = "session-notes"
        elif any(x in name_lower for x in ['report', 'analysis', 'deep', 'dive']):
            dest = root / "docs" / "reports" / md_file.name
            category = "reports"
        else:
            dest = docs_guides / md_file.name  # Default to guides
            category = "guides"

        if dry_run:
            print(f"  🔍 Would move: {md_file.name} → docs/{category}/")
        else:
            try:
                if dest.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    dest = dest.parent / f"{dest.stem}_{timestamp}{dest.suffix}"
                shutil.move(str(md_file), str(dest))
                moved.append((str(md_file), str(dest)))
                print(f"  ✅ Moved: {md_file.name} → docs/{category}/")
            except Exception as e:
                print(f"  ⚠️  Error: {md_file.name} - {e}")

    # Organize JSON files
    json_files = list(root.glob("*.json"))
    print(f"\n📊 Found {len(json_files)} JSON files in root\n")

    for json_file in json_files:
        name_lower = json_file.name.lower()

        # Categorize JSON files
        if any(x in name_lower for x in ['analysis', 'complete', 'reindex', 'cleanup', 'inventory']):
            dest = data_json / json_file.name
            category = "json/analysis"
        else:
            dest = data_json / json_file.name
            category = "json"

        if dry_run:
            print(f"  🔍 Would move: {json_file.name} → data/{category}/")
        else:
            try:
                if dest.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    dest = dest.parent / f"{dest.stem}_{timestamp}{dest.suffix}"
                shutil.move(str(json_file), str(dest))
                moved.append((str(json_file), str(dest)))
                print(f"  ✅ Moved: {json_file.name} → data/{category}/")
            except Exception as e:
                print(f"  ⚠️  Error: {json_file.name} - {e}")

    print(f"\n📊 Summary: {len(moved)} files would be organized")
    return moved

if __name__ == "__main__":
    import sys
    dry_run = "--execute" not in sys.argv

    if dry_run:
        print("=" * 60)
        print("🔍 DRY RUN MODE")
        print("=" * 60)
        print("Add --execute to actually move files\n")
    else:
        print("=" * 60)
        print("⚡ EXECUTING")
        print("=" * 60)
        print()

    organize_root_files(dry_run=dry_run)

    if dry_run:
        print("\n" + "=" * 60)
        print("To execute: python3 scripts/quick_organize_root.py --execute")
        print("=" * 60)


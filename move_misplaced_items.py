#!/usr/bin/env python3
"""
Move all misplaced items to their proper locations
Based on scan_misplaced_items.py findings
"""

from pathlib import Path
import shutil
import json

def move_misplaced_items(root_dir, dry_run=True):
    """Move misplaced items to proper locations"""
    root = Path(root_dir)

    # Load findings
    findings_file = Path.home() / "misplaced_items_scan.json"
    if not findings_file.exists():
        print("❌ Findings file not found. Run scan_misplaced_items.py first.")
        return

    with open(findings_file, 'r') as f:
        findings = json.load(f)

    print("🚚 MOVING MISPLACED ITEMS")
    print("=" * 70)
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    stats = {
        'moved': 0,
        'skipped': 0,
        'errors': 0
    }

    # 1. Move documentation directories
    print("📚 Documentation Directories:")
    print("-" * 70)
    for item in findings.get('documentation_dirs', []):
        source_path = root / item['path']
        parent = item['parent']

        # Skip project-specific docs (like axolotl-main/docs)
        if parent in ['axolotl-main'] and 'docs' in item['path']:
            print(f"   ⏭️  Skipped (project-specific): {item['path']}")
            stats['skipped'] += 1
            continue

        # Move to documentation/ (flatten - remove parent directory)
        target_dir = root / "documentation"
        target_path = target_dir / source_path.name

        if source_path.exists():
            try:
                if not dry_run:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    if target_path.exists():
                        # Merge
                        print(f"   📁 Merging {item['path']} → {target_path.relative_to(root)}/")
                        for file_item in source_path.rglob("*"):
                            if file_item.is_file():
                                rel = file_item.relative_to(source_path)
                                dst = target_path / rel
                                dst.parent.mkdir(parents=True, exist_ok=True)
                                if not dst.exists():
                                    shutil.copy2(file_item, dst)
                        shutil.rmtree(source_path)
                    else:
                        # Move
                        print(f"   📁 Moving {item['path']} → {target_path.relative_to(root)}/")
                        shutil.move(str(source_path), str(target_path))
                else:
                    print(f"   📁 Would move {item['path']} → {target_path.relative_to(root)}/")

                stats['moved'] += 1
            except Exception as e:
                print(f"   ❌ Error: {item['path']}: {e}")
                stats['errors'] += 1

    # 2. Move analysis/documentation files (skip README.md - project-specific)
    print("\n📄 Analysis/Documentation Files:")
    print("-" * 70)
    for item in findings.get('analysis_files', []):
        file_path = root / item['file']
        parent = item['parent']
        file_name = Path(item['file']).name

        # Skip README.md files (project-specific)
        if file_name.upper() == 'README.MD':
            print(f"   ⏭️  Skipped (project-specific): {item['file']}")
            stats['skipped'] += 1
            continue

        # Move analysis files to documentation/ (flatten)
        target_dir = root / "documentation"
        target_path = target_dir / file_name

        if file_path.exists():
            try:
                if not dry_run:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    if target_path.exists():
                        # Version it
                        base = file_path.stem
                        ext = file_path.suffix
                        versioned = target_dir / f"{base}_from_{parent}{ext}"
                        print(f"   📄 Moving (versioned) {item['file']} → {versioned.relative_to(root)}")
                        shutil.move(str(file_path), str(versioned))
                    else:
                        print(f"   📄 Moving {item['file']} → {target_path.relative_to(root)}")
                        shutil.move(str(file_path), str(target_path))
                else:
                    print(f"   📄 Would move {item['file']} → {target_path.relative_to(root)}")

                stats['moved'] += 1
            except Exception as e:
                print(f"   ❌ Error: {item['file']}: {e}")
                stats['errors'] += 1

    # 3. Move media directories
    print("\n🎬 Media Directories:")
    print("-" * 70)
    for item in findings.get('media_dirs', []):
        source_path = root / item['path']
        parent = item['parent']

        # Skip if already in media directory
        if 'simplegallery' in parent or 'MEDIA_PROCESSING' in parent:
            print(f"   ⏭️  Skipped (already in media): {item['path']}")
            stats['skipped'] += 1
            continue

        # Move to MEDIA_PROCESSING/ (flatten)
        target_dir = root / "MEDIA_PROCESSING"
        target_path = target_dir / source_path.name

        if source_path.exists():
            try:
                if not dry_run:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    if target_path.exists():
                        print(f"   📁 Merging {item['path']} → {target_path.relative_to(root)}/")
                        for file_item in source_path.rglob("*"):
                            if file_item.is_file():
                                rel = file_item.relative_to(source_path)
                                dst = target_path / rel
                                dst.parent.mkdir(parents=True, exist_ok=True)
                                if not dst.exists():
                                    shutil.copy2(file_item, dst)
                        shutil.rmtree(source_path)
                    else:
                        print(f"   📁 Moving {item['path']} → {target_path.relative_to(root)}/")
                        shutil.move(str(source_path), str(target_path))
                else:
                    print(f"   📁 Would move {item['path']} → {target_path.relative_to(root)}/")

                stats['moved'] += 1
            except Exception as e:
                print(f"   ❌ Error: {item['path']}: {e}")
                stats['errors'] += 1

    # 4. Move data directories (be careful - some might be intentional)
    print("\n💾 Data Directories:")
    print("-" * 70)
    for item in findings.get('data_dirs', []):
        source_path = root / item['path']
        parent = item['parent']

        # Skip DATA_UTILITIES in tools (might be intentional consolidation)
        if 'DATA_UTILITIES' in item['path'] and parent == 'tools':
            print(f"   ⏭️  Skipped (intentional consolidation): {item['path']}")
            stats['skipped'] += 1
            continue

        # Move to data/ (flatten)
        target_dir = root / "data"
        target_path = target_dir / source_path.name

        if source_path.exists():
            try:
                if not dry_run:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    if target_path.exists():
                        print(f"   📁 Merging {item['path']} → {target_path.relative_to(root)}/")
                        for file_item in source_path.rglob("*"):
                            if file_item.is_file():
                                rel = file_item.relative_to(source_path)
                                dst = target_path / rel
                                dst.parent.mkdir(parents=True, exist_ok=True)
                                if not dst.exists():
                                    shutil.copy2(file_item, dst)
                        shutil.rmtree(source_path)
                    else:
                        print(f"   📁 Moving {item['path']} → {target_path.relative_to(root)}/")
                        shutil.move(str(source_path), str(target_path))
                else:
                    print(f"   📁 Would move {item['path']} → {target_path.relative_to(root)}/")

                stats['moved'] += 1
            except Exception as e:
                print(f"   ❌ Error: {item['path']}: {e}")
                stats['errors'] += 1

    # 5. Move config directories
    print("\n⚙️  Config Directories:")
    print("-" * 70)
    for item in findings.get('config_dirs', []):
        source_path = root / item['path']
        parent = item['parent']

        # Move to config/ (flatten)
        target_dir = root / "config"
        target_path = target_dir / source_path.name

        if source_path.exists():
            try:
                if not dry_run:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    if target_path.exists():
                        print(f"   📁 Merging {item['path']} → {target_path.relative_to(root)}/")
                        for file_item in source_path.rglob("*"):
                            if file_item.is_file():
                                rel = file_item.relative_to(source_path)
                                dst = target_path / rel
                                dst.parent.mkdir(parents=True, exist_ok=True)
                                if not dst.exists():
                                    shutil.copy2(file_item, dst)
                        shutil.rmtree(source_path)
                    else:
                        print(f"   📁 Moving {item['path']} → {target_path.relative_to(root)}/")
                        shutil.move(str(source_path), str(target_path))
                else:
                    print(f"   📁 Would move {item['path']} → {target_path.relative_to(root)}/")

                stats['moved'] += 1
            except Exception as e:
                print(f"   ❌ Error: {item['path']}: {e}")
                stats['errors'] += 1

    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY:")
    print(f"   Items moved:      {stats['moved']}")
    print(f"   Items skipped:    {stats['skipped']}")
    print(f"   Errors:           {stats['errors']}")
    print("=" * 70)

    if dry_run:
        print("\n💡 Run with --execute to perform actual moves")

def main():
    """Main execution"""
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    dry_run = "--execute" not in sys.argv

    move_misplaced_items(root_dir, dry_run=dry_run)

if __name__ == "__main__":
    main()


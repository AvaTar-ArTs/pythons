#!/usr/bin/env python3
"""
Targeted cleanup: Fix obvious issues
1. Eliminate generic folder names (csv, json, pdf)
2. Remove timestamped duplicates
3. Flatten unnecessary nesting
"""
import shutil
from pathlib import Path
from datetime import datetime

base_dir = Path(Path(str(Path.home()) + "/Documents/python"))


def merge_directory(source: Path, target: Path):
    """Merge source directory into target"""
    if not source.exists():
        return False

    target.mkdir(parents=True, exist_ok=True)

    for item in source.rglob("*"):
        if item.is_file():
            rel = item.relative_to(source)
            dest = target / rel
            dest.parent.mkdir(parents=True, exist_ok=True)

            # Handle conflicts
            if dest.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                dest = dest.parent / f"{dest.stem}_{timestamp}{dest.suffix}"

            try:
                shutil.move(str(item), str(dest))
            except (ValueError, TypeError):
                pass

    # Remove source if empty
    try:
        if not any(source.iterdir()):
            source.rmdir()
    except Exception:
        pass

    return True


def main():
    """main function."""

    logger.info("=" * 70)
    logger.info("🧹 TARGETED CLEANUP")
    logger.info("=" * 70)
    print()

    moves = []

    # 1. Fix generic "csv" directories
    for csv_dir in base_dir.rglob("csv"):
        if csv_dir.is_dir() and csv_dir.parent.name != "csv_processing":
            # Determine parent category
            if "AUTOMATION_BOTS" in str(csv_dir):
                target = (
                    base_dir
                    / "DATA_UTILITIES"
                    / "spreadsheet_tools"
                    / csv_dir.parent.name
                )
            else:
                target = (
                    base_dir
                    / "DATA_UTILITIES"
                    / "spreadsheet_tools"
                    / csv_dir.parent.name
                )
            moves.append(("csv directory", csv_dir, target))

    # 2. Fix generic "json" directories
    for json_dir in base_dir.rglob("json"):
        if json_dir.is_dir() and json_dir.parent.name not in [
            "json_tools",
            "json_processing",
        ]:
            parent_name = json_dir.parent.name
            if "social_media" in parent_name or "automation" in parent_name:
                target = base_dir / "AUTOMATION_BOTS" / parent_name / "data_files"
            else:
                target = base_dir / "DATA_UTILITIES" / "json_tools" / parent_name
            moves.append(("json directory", json_dir, target))

    # 3. Fix generic "pdf" directories
    for pdf_dir in base_dir.rglob("pdf"):
        if pdf_dir.is_dir():
            target = (
                base_dir
                / "DATA_UTILITIES"
                / "document_processors"
                / pdf_dir.parent.name
            )
            moves.append(("pdf directory", pdf_dir, target))

    # 4. Consolidate timestamped duplicates
    timestamped = list(base_dir.rglob("*_20251026_*"))
    for ts_dir in timestamped:
        if ts_dir.is_dir():
            # Remove timestamp from name
            clean_name = ts_dir.name.rsplit("_20251026_", 1)[0]
            target = ts_dir.parent / clean_name
            moves.append(("timestamped duplicate", ts_dir, target))

    logger.info(f"Found {len(moves)} improvements to make")
    print()

    # Show plan
    by_type = {}
    for move_type, source, target in moves:
        if move_type not in by_type:
            by_type[move_type] = []
        by_type[move_type].append((source, target))

    for move_type, items in by_type.items():
        logger.info(f"📁 {move_type.upper()}: {len(items)} directories")
        for source, target in items[:3]:
            rel_s = source.relative_to(base_dir)
            rel_t = target.relative_to(base_dir)
            logger.info(f"   {rel_s}")
            logger.info(f"   → {rel_t}")
        if len(items) > 3:
            logger.info(f"   ... and {len(items)-3} more")
        print()

    # Execute
    logger.info("🚀 Executing cleanup...")
    success = 0
    for move_type, source, target in moves:
        try:
            if merge_directory(source, target):
                success += 1
        except Exception as e:
            logger.info(f"   ❌ Error: {str(e)[:50]}")

    print()
    logger.info(f"✅ Cleaned up {success}/{len(moves)} directories")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()

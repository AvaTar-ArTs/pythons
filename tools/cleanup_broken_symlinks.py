#!/usr/bin/env python3
"""
Cleanup Broken Symlinks Script
Safely removes broken symlinks from pythons/CONTENT_AWARE_CATALOG/CONTENT_ORGANIZED/
"""

import os
import csv
from pathlib import Path
from datetime import datetime


def find_broken_symlinks(directory):
    """Find all broken symlinks in directory."""
    broken_links = []
    directory = Path(directory).expanduser()

    print(f"🔍 Scanning for broken symlinks in: {directory}")

    for item in directory.rglob('*'):
        if item.is_symlink():
            try:
                # Check if the target exists
                item.resolve(strict=True)
            except (FileNotFoundError, OSError):
                # Symlink is broken
                try:
                    target = os.readlink(item)
                    broken_links.append({
                        'symlink_path': str(item),
                        'target_path': target,
                        'category': item.parent.name,
                        'filename': item.name
                    })
                except Exception as e:
                    print(f"   ⚠️  Error reading symlink {item}: {e}")

    return broken_links


def remove_broken_symlinks(broken_links, dry_run=True):
    """Remove broken symlinks."""
    removed_count = 0

    mode = "DRY RUN" if dry_run else "REMOVING"
    print(f"\n{'='*70}")
    print(f"🗑️  {mode} - Broken Symlinks")
    print(f"{'='*70}\n")

    for link in broken_links:
        symlink_path = Path(link['symlink_path'])

        if dry_run:
            print(f"   Would remove: {symlink_path.name}")
        else:
            try:
                symlink_path.unlink()
                removed_count += 1
                if removed_count % 100 == 0:
                    print(f"   Removed {removed_count}/{len(broken_links)}...")
            except Exception as e:
                print(f"   ⚠️  Error removing {symlink_path}: {e}")

    return removed_count


def generate_report(broken_links, removed_count, output_file):
    """Generate CSV report of removed symlinks."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"BROKEN_SYMLINKS_REPORT_{timestamp}.csv"

    with open(report_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['symlink_path', 'target_path', 'category', 'filename']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(broken_links)

    # Summary
    summary_file = f"CLEANUP_SUMMARY_{timestamp}.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# Broken Symlinks Cleanup Summary\n\n")
        f.write(f"**Date:** {datetime.now().isoformat()}\n\n")
        f.write(f"**Total Broken Symlinks Found:** {len(broken_links)}\n")
        f.write(f"**Symlinks Removed:** {removed_count}\n\n")

        # By category
        f.write("## Breakdown by Category\n\n")
        categories = {}
        for link in broken_links:
            cat = link['category']
            categories[cat] = categories.get(cat, 0) + 1

        f.write("| Category | Count |\n")
        f.write("|----------|-------|\n")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            f.write(f"| {cat} | {count} |\n")

        f.write(f"\n**Detailed Report:** {report_file}\n")

    return report_file, summary_file


def main():
    """Main execution."""
    print("\n" + "="*70)
    print("🧹 BROKEN SYMLINKS CLEANUP TOOL")
    print("="*70 + "\n")

    # Find broken symlinks
    directory = "~/pythons/CONTENT_AWARE_CATALOG/CONTENT_ORGANIZED"
    broken_links = find_broken_symlinks(directory)

    if not broken_links:
        print("✅ No broken symlinks found!")
        return

    print(f"\n✓ Found {len(broken_links)} broken symlinks\n")

    # Show sample
    print("Sample broken symlinks:")
    for link in broken_links[:5]:
        print(f"   {link['filename']} -> {link['target_path']}")
    if len(broken_links) > 5:
        print(f"   ... and {len(broken_links) - 5} more\n")

    # Dry run first
    print("\n--- DRY RUN (Preview) ---")
    remove_broken_symlinks(broken_links[:10], dry_run=True)
    print(f"(Showing first 10 of {len(broken_links)})\n")

    # Ask for confirmation
    response = input(f"Remove all {len(broken_links)} broken symlinks? (yes/no): ").strip().lower()

    if response == 'yes':
        removed_count = remove_broken_symlinks(broken_links, dry_run=False)

        # Generate report
        report_file, summary_file = generate_report(broken_links, removed_count, None)

        print(f"\n{'='*70}")
        print("✅ CLEANUP COMPLETE")
        print(f"{'='*70}")
        print(f"\n✓ Removed {removed_count} broken symlinks")
        print(f"✓ Detailed report: {report_file}")
        print(f"✓ Summary: {summary_file}\n")
    else:
        print("\n❌ Cleanup cancelled")

        # Still generate report for reference
        report_file, summary_file = generate_report(broken_links, 0, None)
        print(f"✓ Generated report (no files removed): {report_file}\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Analyze folder depths in ~/pythons directory.
Shows the maximum depth and all folder structures.
"""

from pathlib import Path
from collections import defaultdict


def get_folder_structure(root_dir, max_depth=None):
    """Get folder structure with depths."""
    root_path = Path(root_dir)
    folder_depths = []
    depth_to_folders = defaultdict(list)

    def scan_directory(path, current_depth=0):
        """Recursively scan directory."""
        try:
            for item in path.iterdir():
                if item.is_dir():
                    # Skip hidden directories and common ignore dirs
                    if item.name.startswith(".") or item.name in [
                        "__pycache__",
                        "node_modules",
                        ".git",
                    ]:
                        continue

                    depth = current_depth + 1
                    folder_depths.append((item, depth))
                    depth_to_folders[depth].append(item)

                    if max_depth is None or depth < max_depth:
                        scan_directory(item, depth)
        except PermissionError:
            pass
        except Exception:
            pass

    scan_directory(root_path)
    return folder_depths, depth_to_folders


def format_path(path, root_path):
    """Format path relative to root."""
    try:
        return str(path.relative_to(root_path))
    except:
        return str(path)


def analyze_depths(root_dir):
    """Analyze and display folder depths."""
    root_path = Path(root_dir)

    print("=" * 80)
    print(f"📁 FOLDER DEPTH ANALYSIS: {root_path}")
    print("=" * 80)
    print()

    folder_depths, depth_to_folders = get_folder_structure(root_path)

    if not folder_depths:
        print("✅ No subdirectories found (flat structure)")
        return

    # Get statistics
    max_depth = max(depth for _, depth in folder_depths) if folder_depths else 0
    total_folders = len(folder_depths)

    print("📊 STATISTICS:")
    print(f"   Total folders: {total_folders}")
    print(f"   Maximum depth: {max_depth} levels")
    print(
        f"   Average depth: {sum(d for _, d in folder_depths) / total_folders:.2f} levels"
    )
    print()

    # Show folders by depth
    print("=" * 80)
    print("📂 FOLDERS BY DEPTH LEVEL")
    print("=" * 80)
    print()

    for depth in sorted(depth_to_folders.keys()):
        folders = sorted(depth_to_folders[depth])
        print(f"Level {depth} ({len(folders)} folders):")
        for folder in folders:
            rel_path = format_path(folder, root_path)
            # Count subdirectories
            try:
                subdirs = sum(
                    1
                    for item in folder.iterdir()
                    if item.is_dir() and not item.name.startswith(".")
                )
                subdir_info = f" ({subdirs} subdirs)" if subdirs > 0 else ""
            except:
                subdir_info = ""
            print(f"   {'  ' * (depth - 1)}📁 {rel_path}{subdir_info}")
        print()

    # Show deepest paths
    print("=" * 80)
    print("🔽 DEEPEST FOLDER PATHS")
    print("=" * 80)
    print()

    # Sort by depth (deepest first)
    sorted_by_depth = sorted(folder_depths, key=lambda x: (-x[1], str(x[0])))

    # Show top 20 deepest
    for folder, depth in sorted_by_depth[:20]:
        rel_path = format_path(folder, root_path)
        print(f"   Depth {depth}: {rel_path}")

    if len(sorted_by_depth) > 20:
        print(f"\n   ... and {len(sorted_by_depth) - 20} more folders")

    # Show depth distribution
    print()
    print("=" * 80)
    print("📊 DEPTH DISTRIBUTION")
    print("=" * 80)
    print()

    depth_counts = defaultdict(int)
    for _, depth in folder_depths:
        depth_counts[depth] += 1

    for depth in sorted(depth_counts.keys()):
        count = depth_counts[depth]
        bar_length = int((count / total_folders) * 50)
        bar = "█" * bar_length
        print(
            f"   Level {depth}: {count:4d} folders {bar} ({count / total_folders * 100:.1f}%)"
        )


if __name__ == "__main__":
    root_directory = Path.home() / "pythons"
    analyze_depths(root_directory)

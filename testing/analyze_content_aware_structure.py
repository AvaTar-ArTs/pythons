#!/usr/bin/env python3
"""
Analyze folder structure with content and parent-folder awareness.
Understands the purpose and context of folders based on their content
and parent directory relationships.
"""

import sys
from pathlib import Path
from collections import defaultdict

# Avoid importing local files
if str(Path(__file__).parent) in sys.path:
    sys.path.remove(str(Path(__file__).parent))


def get_file_types_in_folder(folder_path):
    """Analyze file types in a folder."""
    file_types = defaultdict(int)
    file_count = 0
    total_size = 0

    try:
        for item in folder_path.iterdir():
            if item.is_file():
                file_count += 1
                suffix = item.suffix.lower() if item.suffix else "no_extension"
                file_types[suffix] += 1
                try:
                    total_size += item.stat().st_size
                except:
                    pass
    except:
        pass

    return file_types, file_count, total_size


def categorize_folder(folder_path, parent_path=None):
    """Categorize folder based on content and parent context."""
    name = folder_path.name.lower()
    file_types, file_count, total_size = get_file_types_in_folder(folder_path)

    # Determine category based on name patterns and content
    category = "unknown"
    purpose = []

    # Check for common patterns
    if any(x in name for x in ["test", "__pycache__", "tests"]):
        category = "testing"
    elif any(x in name for x in ["docs", "doc", "documentation"]):
        category = "documentation"
    elif any(x in name for x in ["src", "source", "lib", "library"]):
        category = "source_code"
    elif any(x in name for x in ["build", "_build", "dist", "output"]):
        category = "build_output"
    elif any(x in name for x in ["config", "settings", "conf"]):
        category = "configuration"
    elif any(x in name for x in ["static", "assets", "public", "media"]):
        category = "static_assets"
    elif any(x in name for x in ["examples", "samples", "demos"]):
        category = "examples"
    elif any(x in name for x in ["utils", "utilities", "tools", "scripts"]):
        category = "utilities"
    elif any(x in name for x in ["data", "dataset", "storage"]):
        category = "data"
    elif any(x in name for x in ["api", "endpoints", "routes"]):
        category = "api"
    elif any(x in name for x in ["ui", "components", "views", "templates"]):
        category = "ui"
    elif any(x in name for x in ["models", "schema", "database"]):
        category = "data_models"
    elif any(x in name for x in ["integrations", "plugins", "extensions"]):
        category = "integrations"
    elif any(x in name for x in ["core", "base", "common"]):
        category = "core"
    elif any(x in name for x in ["archive", "old", "backup", "_archives"]):
        category = "archive"
    elif any(x in name for x in ["fonts", "css", "js", "images", "img"]):
        category = "assets"
    elif file_types.get(".py", 0) > file_types.get(".md", 0) * 2:
        category = "python_code"
    elif file_types.get(".md", 0) > 0:
        category = "documentation"
    elif file_types.get(".json", 0) > 0 or file_types.get(".yaml", 0) > 0:
        category = "configuration"

    # Determine purpose based on content
    if file_types.get(".py", 0) > 0:
        purpose.append("python")
    if file_types.get(".md", 0) > 0:
        purpose.append("markdown")
    if file_types.get(".json", 0) > 0:
        purpose.append("json_data")
    if file_types.get(".html", 0) > 0:
        purpose.append("web")
    if file_types.get(".css", 0) > 0:
        purpose.append("styling")
    if file_types.get(".js", 0) > 0:
        purpose.append("javascript")
    if file_types.get(".txt", 0) > 0:
        purpose.append("text")
    if file_types.get(".png", 0) > 0 or file_types.get(".jpg", 0) > 0:
        purpose.append("images")

    return {
        "category": category,
        "purpose": purpose,
        "file_count": file_count,
        "file_types": dict(file_types),
        "total_size": total_size,
    }


def analyze_with_context(root_dir):
    """Analyze folder structure with parent-folder awareness."""
    root_path = Path(root_dir)

    print("=" * 80)
    print(f"📁 CONTENT-AWARE FOLDER ANALYSIS: {root_path}")
    print("=" * 80)
    print()

    folder_info = {}
    parent_children = defaultdict(list)

    # Collect all folders with their info
    for folder in root_path.rglob("*"):
        if folder.is_dir():
            # Skip hidden and cache dirs
            if folder.name.startswith(".") or folder.name in [
                "__pycache__",
                "node_modules",
            ]:
                continue

            try:
                parent = folder.parent
                info = categorize_folder(folder, parent)
                info["path"] = str(folder.relative_to(root_path))
                info["depth"] = len(folder.relative_to(root_path).parts) - 1
                info["parent"] = (
                    str(parent.relative_to(root_path))
                    if parent != root_path
                    else "ROOT"
                )

                folder_info[folder] = info
                parent_children[parent].append(folder)
            except:
                pass

    # Group by category
    print("=" * 80)
    print("📊 FOLDERS BY CATEGORY")
    print("=" * 80)
    print()

    category_groups = defaultdict(list)
    for folder, info in folder_info.items():
        category_groups[info["category"]].append((folder, info))

    for category in sorted(category_groups.keys()):
        folders = category_groups[category]
        print(f"📂 {category.upper().replace('_', ' ')} ({len(folders)} folders)")
        for folder, info in sorted(folders, key=lambda x: x[1]["depth"])[:10]:
            rel_path = info["path"]
            file_info = f"{info['file_count']} files"
            if info["file_types"]:
                main_type = max(info["file_types"].items(), key=lambda x: x[1])[0]
                file_info += f" (mostly {main_type})"
            print(f"   {'  ' * info['depth']}📁 {rel_path} - {file_info}")
        if len(folders) > 10:
            print(f"   ... and {len(folders) - 10} more")
        print()

    # Show parent-child relationships
    print("=" * 80)
    print("🔗 PARENT-CHILD RELATIONSHIPS (Top 20)")
    print("=" * 80)
    print()

    # Sort by number of children
    sorted_parents = sorted(parent_children.items(), key=lambda x: -len(x[1]))[:20]

    for parent, children in sorted_parents:
        if parent == root_path:
            parent_name = "ROOT"
        else:
            try:
                parent_name = str(parent.relative_to(root_path))
            except:
                parent_name = str(parent)

        print(f"📁 {parent_name}")
        for child in sorted(children)[:5]:
            try:
                child_name = child.name
                child_info = folder_info.get(child, {})
                file_count = child_info.get("file_count", 0)
                category = child_info.get("category", "unknown")
                print(f"   └─ {child_name} ({file_count} files, {category})")
            except:
                pass
        if len(children) > 5:
            print(f"   ... and {len(children) - 5} more children")
        print()

    # Show depth analysis with context
    print("=" * 80)
    print("📏 DEPTH ANALYSIS WITH CONTEXT")
    print("=" * 80)
    print()

    depth_stats = defaultdict(lambda: {"count": 0, "categories": defaultdict(int)})
    for folder, info in folder_info.items():
        depth = info["depth"]
        depth_stats[depth]["count"] += 1
        depth_stats[depth]["categories"][info["category"]] += 1

    for depth in sorted(depth_stats.keys()):
        stats = depth_stats[depth]
        print(f"Level {depth}: {stats['count']} folders")
        for cat, count in sorted(stats["categories"].items(), key=lambda x: -x[1])[:3]:
            print(f"   • {cat}: {count}")
        print()

    # Find orphaned or misplaced folders
    print("=" * 80)
    print("⚠️  POTENTIALLY MISPLACED FOLDERS")
    print("=" * 80)
    print()

    misplaced = []
    for folder, info in folder_info.items():
        # Check for mismatches
        if info["category"] == "build_output" and info["depth"] < 3:
            misplaced.append((folder, info, "Build output at shallow depth"))
        elif info["category"] == "testing" and info["depth"] == 1:
            misplaced.append((folder, info, "Test folder at root"))
        elif info["file_count"] == 0:
            misplaced.append((folder, info, "Empty folder"))

    for folder, info, reason in misplaced[:15]:
        print(f"📁 {info['path']}")
        print(f"   Reason: {reason}")
        print(f"   Category: {info['category']}, Files: {info['file_count']}")
        print()

    # Summary statistics
    print("=" * 80)
    print("📈 SUMMARY STATISTICS")
    print("=" * 80)
    print()
    print(f"Total folders analyzed: {len(folder_info)}")
    print(f"Categories found: {len(category_groups)}")
    print(
        f"Average files per folder: {sum(i['file_count'] for i in folder_info.values()) / len(folder_info):.1f}"
    )
    print(
        f"Folders with no files: {sum(1 for i in folder_info.values() if i['file_count'] == 0)}"
    )
    print(
        f"Most common category: {max(category_groups.items(), key=lambda x: len(x[1]))[0]}"
    )


if __name__ == "__main__":
    root_directory = Path.home() / "pythons"
    analyze_with_context(root_directory)

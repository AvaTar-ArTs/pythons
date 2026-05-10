#!/usr/bin/env python3
"""
Generate a parent-folder awareness report showing how folders relate
to their parents and the context they provide.
"""

import sys
from pathlib import Path
from collections import defaultdict

# Avoid importing local files
if str(Path(__file__).parent) in sys.path:
    sys.path.remove(str(Path(__file__).parent))


def analyze_parent_context(root_dir):
    """Analyze folders with parent-folder awareness."""
    root_path = Path(root_dir)

    print("=" * 80)
    print("🔗 PARENT-FOLDER AWARENESS ANALYSIS")
    print("=" * 80)
    print()

    # Collect folder information
    folders_by_parent = defaultdict(list)
    folder_info = {}

    for folder in root_path.rglob("*"):
        if folder.is_dir():
            if folder.name.startswith(".") or folder.name in [
                "__pycache__",
                "node_modules",
            ]:
                continue

            try:
                parent = folder.parent
                rel_path = folder.relative_to(root_path)
                depth = len(rel_path.parts) - 1

                # Count files
                file_count = sum(1 for item in folder.iterdir() if item.is_file())

                # Get file types
                file_types = defaultdict(int)
                for item in folder.iterdir():
                    if item.is_file():
                        suffix = item.suffix.lower() if item.suffix else "no_ext"
                        file_types[suffix] += 1

                info = {
                    "name": folder.name,
                    "path": str(rel_path),
                    "depth": depth,
                    "parent_path": str(parent.relative_to(root_path))
                    if parent != root_path
                    else "ROOT",
                    "parent_name": parent.name if parent != root_path else "ROOT",
                    "file_count": file_count,
                    "file_types": dict(file_types),
                }

                folder_info[folder] = info
                folders_by_parent[parent].append(folder)
            except:
                pass

    # 1. Show parent-child hierarchies
    print("=" * 80)
    print("📂 PARENT-CHILD HIERARCHIES (Top 15 by child count)")
    print("=" * 80)
    print()

    sorted_parents = sorted(folders_by_parent.items(), key=lambda x: -len(x[1]))[:15]

    for parent, children in sorted_parents:
        if parent == root_path:
            parent_display = "📁 ROOT"
        else:
            try:
                parent_info = folder_info.get(parent, {})
                parent_display = f"📁 {parent_info.get('path', str(parent))}"
            except:
                parent_display = f"📁 {parent.name}"

        print(parent_display)

        for child in sorted(
            children, key=lambda x: folder_info.get(x, {}).get("name", "")
        )[:8]:
            child_info = folder_info.get(child, {})
            file_count = child_info.get("file_count", 0)
            main_type = ""
            if child_info.get("file_types"):
                main_type = max(child_info["file_types"].items(), key=lambda x: x[1])[0]
                main_type = f" ({main_type})" if main_type != "no_ext" else ""

            indent = "   " * (child_info.get("depth", 0))
            print(
                f"{indent}└─ {child_info.get('name', 'unknown')} [{file_count} files{main_type}]"
            )

        if len(children) > 8:
            print(f"   ... and {len(children) - 8} more children")
        print()

    # 2. Show context patterns
    print("=" * 80)
    print("🎯 CONTEXT PATTERNS (Parent-Child Relationships)")
    print("=" * 80)
    print()

    # Find patterns like: parent has X type, children have Y type
    patterns = defaultdict(list)

    for folder, info in folder_info.items():
        parent = folder.parent
        if parent in folder_info:
            parent_info = folder_info[parent]

            # Check for patterns
            parent_py = parent_info.get("file_types", {}).get(".py", 0)
            child_py = info.get("file_types", {}).get(".py", 0)

            if parent_py > 0 and child_py > 0:
                patterns["python_inheritance"].append((parent_info, info))
            elif parent_py == 0 and child_py > 0:
                patterns["python_children"].append((parent_info, info))

            parent_md = parent_info.get("file_types", {}).get(".md", 0)
            child_md = info.get("file_types", {}).get(".md", 0)

            if parent_md > 0 and child_md > 0:
                patterns["documentation_nested"].append((parent_info, info))

    print(
        f"📊 Python code inheritance: {len(patterns['python_inheritance'])} parent-child pairs"
    )
    print(
        f"📊 Python code in non-Python parents: {len(patterns['python_children'])} cases"
    )
    print(f"📊 Nested documentation: {len(patterns['documentation_nested'])} pairs")
    print()

    # 3. Show depth distribution with parent context
    print("=" * 80)
    print("📏 DEPTH ANALYSIS WITH PARENT CONTEXT")
    print("=" * 80)
    print()

    depth_parents = defaultdict(lambda: defaultdict(int))

    for folder, info in folder_info.items():
        depth = info["depth"]
        parent_name = info["parent_name"]
        depth_parents[depth][parent_name] += 1

    for depth in sorted(depth_parents.keys()):
        print(f"Level {depth}:")
        parents = depth_parents[depth]
        for parent, count in sorted(parents.items(), key=lambda x: -x[1])[:5]:
            print(f"   • {count} folders under '{parent}'")
        print()

    # 4. Find contextually interesting relationships
    print("=" * 80)
    print("💡 INTERESTING PARENT-CHILD RELATIONSHIPS")
    print("=" * 80)
    print()

    interesting = []

    for folder, info in folder_info.items():
        parent = folder.parent
        if parent in folder_info:
            parent_info = folder_info[parent]

            # Large parent with many children
            if len(folders_by_parent[parent]) > 10:
                interesting.append(
                    (
                        f"Large parent '{parent_info['name']}' has {len(folders_by_parent[parent])} children",
                        parent_info,
                        info,
                    )
                )

            # Empty parent with non-empty child
            if parent_info["file_count"] == 0 and info["file_count"] > 0:
                interesting.append(
                    (
                        f"Empty parent '{parent_info['name']}' contains folder with {info['file_count']} files",
                        parent_info,
                        info,
                    )
                )

            # Type mismatch
            parent_types = set(parent_info.get("file_types", {}).keys())
            child_types = set(info.get("file_types", {}).keys())
            if (
                parent_types
                and child_types
                and not parent_types.intersection(child_types)
            ):
                interesting.append(
                    (
                        f"Type mismatch: parent has {list(parent_types)[:2]}, child has {list(child_types)[:2]}",
                        parent_info,
                        info,
                    )
                )

    for reason, parent_info, child_info in interesting[:15]:
        print(f"📁 {parent_info['path']} → {child_info['name']}")
        print(f"   {reason}")
        print()

    # 5. Summary
    print("=" * 80)
    print("📈 SUMMARY")
    print("=" * 80)
    print()
    print(f"Total folders: {len(folder_info)}")
    print(
        f"Folders with parent context: {sum(1 for f, i in folder_info.items() if i['parent_name'] != 'ROOT')}"
    )
    print(
        f"Average children per parent: {sum(len(c) for c in folders_by_parent.values()) / len(folders_by_parent):.1f}"
    )
    print(
        f"Parents with most children: {max(len(c) for c in folders_by_parent.values())}"
    )


if __name__ == "__main__":
    root_directory = Path.home() / "pythons"
    analyze_parent_context(root_directory)

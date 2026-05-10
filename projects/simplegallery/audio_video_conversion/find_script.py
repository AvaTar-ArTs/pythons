#!/usr/bin/env python3
"""Python Script Finder and Navigator
Helps you locate any Python script in your organized structure
"""

from pathlib import Path


class ScriptFinder:
    def __init__(self, base_path="/Users/steven/Documents/python"):
        self.base_path = Path(base_path)
        self.script_index = {}
        self.build_index()

    def build_index(self):
        """Build an index of all Python scripts for fast searching."""
        print("🔍 Building script index...")

        for py_file in self.base_path.rglob("*.py"):
            if py_file.is_file():
                # Get relative path from base
                rel_path = py_file.relative_to(self.base_path)

                # Store in index with multiple search keys
                script_info = {
                    "full_path": str(py_file),
                    "relative_path": str(rel_path),
                    "filename": py_file.name,
                    "stem": py_file.stem,
                    "parent_dir": str(rel_path.parent),
                    "size": py_file.stat().st_size,
                    "modified": py_file.stat().st_mtime,
                }

                # Index by filename
                self.script_index[py_file.name] = script_info

                # Index by stem (without extension)
                self.script_index[py_file.stem] = script_info

                # Index by partial matches
                for part in py_file.stem.split("_"):
                    if len(part) > 2:  # Only index meaningful parts
                        if part not in self.script_index:
                            self.script_index[part] = []
                        if not isinstance(self.script_index[part], list):
                            self.script_index[part] = [self.script_index[part]]
                        self.script_index[part].append(script_info)

        print(
            f"✅ Indexed {len([k for k, v in self.script_index.items() if isinstance(v, dict)])} unique scripts",
        )

    def find_script(self, search_term):
        """Find scripts matching the search term."""
        results = []
        search_lower = search_term.lower()

        for key, value in self.script_index.items():
            if isinstance(value, dict):
                # Direct filename match
                if search_lower in key.lower():
                    results.append(value)
            elif isinstance(value, list):
                # Partial match results
                for script_info in value:
                    if search_lower in script_info["filename"].lower():
                        results.append(script_info)

        return results

    def find_by_functionality(self, functionality):
        """Find scripts by functionality type."""
        functionality_map = {
            "transcription": "01_core_ai_analysis/transcription",
            "analysis": "01_core_ai_analysis",
            "ai": "01_core_ai_analysis",
            "image": "02_media_processing/image_tools",
            "video": "02_media_processing/video_tools",
            "audio": "02_media_processing/audio_tools",
            "youtube": "03_automation_platforms/youtube_automation",
            "social": "03_automation_platforms/social_media_automation",
            "web": "03_automation_platforms/web_automation",
            "scraping": "03_automation_platforms/web_automation",
            "data": "01_core_ai_analysis/data_processing",
            "convert": "02_media_processing/format_conversion",
            "organize": "05_data_management/file_organization",
            "test": "06_development_tools/testing_framework",
            "utility": "06_development_tools/development_utilities",
        }

        if functionality.lower() in functionality_map:
            target_dir = self.base_path / functionality_map[functionality.lower()]
            if target_dir.exists():
                return [
                    {
                        "full_path": str(f),
                        "relative_path": str(f.relative_to(self.base_path)),
                        "filename": f.name,
                    }
                    for f in target_dir.rglob("*.py")
                ]

        return []

    def show_script_location(self, script_name):
        """Show the exact location of a script."""
        results = self.find_script(script_name)

        if not results:
            print(f"❌ No script found matching '{script_name}'")
            return

        print(f"🔍 Found {len(results)} script(s) matching '{script_name}':")
        print("=" * 60)

        for i, script in enumerate(results, 1):
            print(f"\n{i}. {script['filename']}")
            print(f"   📁 Location: {script['relative_path']}")
            print(f"   📏 Size: {script['size']:,} bytes")
            print(f"   🔗 Full path: {script['full_path']}")

    def show_directory_structure(self, max_depth=3):
        """Show the organized directory structure."""
        print("📁 ORGANIZED DIRECTORY STRUCTURE")
        print("=" * 60)

        def print_tree(path, prefix="", depth=0, max_depth=3):
            if depth > max_depth:
                return

            items = sorted(
                [
                    item
                    for item in path.iterdir()
                    if item.is_dir() and not item.name.startswith(".")
                ],
            )

            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item.name}/")

                if depth < max_depth:
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    print_tree(item, next_prefix, depth + 1, max_depth)

        print_tree(self.base_path, max_depth=max_depth)

    def show_category_contents(self, category):
        """Show contents of a specific category."""
        category_map = {
            "1": "01_core_ai_analysis",
            "2": "02_media_processing",
            "3": "03_automation_platforms",
            "4": "04_content_creation",
            "5": "05_data_management",
            "6": "06_development_tools",
            "7": "07_experimental",
            "8": "08_archived",
        }

        if category in category_map:
            category_path = self.base_path / category_map[category]
            if category_path.exists():
                print(f"📁 Contents of {category_map[category]}:")
                print("=" * 50)

                for subdir in sorted(category_path.iterdir()):
                    if subdir.is_dir():
                        py_files = list(subdir.rglob("*.py"))
                        print(f"\n📂 {subdir.name}/ ({len(py_files)} Python files)")

                        # Show first 10 files as examples
                        for py_file in sorted(py_files)[:10]:
                            print(f"   📄 {py_file.name}")

                        if len(py_files) > 10:
                            print(f"   ... and {len(py_files) - 10} more files")
            else:
                print(f"❌ Category {category_map[category]} not found")
        else:
            print("❌ Invalid category. Use 1-8")

    def interactive_search(self):
        """Interactive search mode."""
        print("🔍 INTERACTIVE SCRIPT FINDER")
        print("=" * 40)
        print("Commands:")
        print("  search <name>     - Search for script by name")
        print("  func <type>       - Find by functionality")
        print("  tree              - Show directory structure")
        print("  category <1-8>    - Show category contents")
        print("  help              - Show this help")
        print("  quit              - Exit")
        print()

        while True:
            try:
                command = input("🔍 Enter command: ").strip().lower()

                if command == "quit":
                    print("👋 Goodbye!")
                    break
                if command == "help":
                    print("Commands: search, func, tree, category, help, quit")
                elif command == "tree":
                    self.show_directory_structure()
                elif command.startswith("search "):
                    script_name = command[7:]
                    self.show_script_location(script_name)
                elif command.startswith("func "):
                    func_type = command[5:]
                    results = self.find_by_functionality(func_type)
                    if results:
                        print(f"🔍 Found {len(results)} scripts for '{func_type}':")
                        for script in results[:10]:  # Show first 10
                            print(
                                f"  📄 {script['filename']} - {script['relative_path']}",
                            )
                        if len(results) > 10:
                            print(f"  ... and {len(results) - 10} more")
                    else:
                        print(f"❌ No scripts found for functionality '{func_type}'")
                elif command.startswith("category "):
                    cat_num = command[9:]
                    self.show_category_contents(cat_num)
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")

                print()

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Main function."""
    finder = ScriptFinder()

    print("🐍 PYTHON SCRIPT FINDER & NAVIGATOR")
    print("=" * 50)
    print("Find any Python script in your organized structure!")
    print()

    # Show quick overview
    print("📊 QUICK OVERVIEW:")
    print("-" * 20)

    categories = {
        "01_core_ai_analysis": "AI & Analysis tools",
        "02_media_processing": "Media processing tools",
        "03_automation_platforms": "Platform automation",
        "04_content_creation": "Content creation tools",
        "05_data_management": "Data management tools",
        "06_development_tools": "Development utilities",
        "07_experimental": "Experimental projects",
        "08_archived": "Archived projects",
    }

    for cat_dir, description in categories.items():
        cat_path = finder.base_path / cat_dir
        if cat_path.exists():
            py_count = len(list(cat_path.rglob("*.py")))
            print(f"  {cat_dir}: {py_count} Python files - {description}")

    print()

    # Start interactive mode
    finder.interactive_search()


if __name__ == "__main__":
    main()

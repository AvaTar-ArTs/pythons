#!/usr/bin/env python3
"""
🔍 RECURSIVE DEEP SCAN - EVERY FOLDER AT EVERY DEPTH
Comprehensive analysis of entire ~/pythons/ structure
"""

import ast
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import csv


class RecursiveDeepScanner:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.folder_data = []
        self.file_data = []
        self.stats = defaultdict(int)

    def scan_folder(self, folder_path, depth=0):
        """Recursively scan a folder and all its contents"""
        folder_info = {
            "full_path": str(folder_path),
            "relative_path": str(folder_path.relative_to(self.pythons_dir)),
            "folder_name": folder_path.name,
            "depth": depth,
            "python_files": 0,
            "total_files": 0,
            "total_dirs": 0,
            "size_bytes": 0,
            "total_lines": 0,
            "total_functions": 0,
            "total_classes": 0,
            "direct_py_files": 0,
            "subdirs": [],
            "py_files_list": [],
            "has_readme": False,
            "has_requirements": False,
            "has_init": False,
            "apis_found": set(),
            "purposes": set(),
        }

        try:
            # Check for special files
            folder_info["has_readme"] = (folder_path / "README.md").exists() or (
                folder_path / "README.txt"
            ).exists()
            folder_info["has_requirements"] = (
                folder_path / "requirements.txt"
            ).exists()
            folder_info["has_init"] = (folder_path / "__init__.py").exists()

            # Scan all items in this folder
            for item in folder_path.iterdir():
                if item.name.startswith("."):
                    continue  # Skip hidden files

                if item.is_dir():
                    folder_info["total_dirs"] += 1
                    folder_info["subdirs"].append(item.name)

                    # Recursively scan subdirectory
                    subfolder_info = self.scan_folder(item, depth + 1)
                    self.folder_data.append(subfolder_info)

                    # Aggregate stats
                    folder_info["python_files"] += subfolder_info["python_files"]
                    folder_info["total_files"] += subfolder_info["total_files"]
                    folder_info["size_bytes"] += subfolder_info["size_bytes"]
                    folder_info["total_lines"] += subfolder_info["total_lines"]
                    folder_info["total_functions"] += subfolder_info["total_functions"]
                    folder_info["total_classes"] += subfolder_info["total_classes"]
                    folder_info["apis_found"].update(subfolder_info["apis_found"])
                    folder_info["purposes"].update(subfolder_info["purposes"])

                elif item.is_file():
                    folder_info["total_files"] += 1

                    try:
                        file_size = item.stat().st_size
                        folder_info["size_bytes"] += file_size
                    except:
                        pass

                    # Analyze Python files
                    if item.suffix == ".py":
                        folder_info["python_files"] += 1
                        folder_info["direct_py_files"] += 1
                        folder_info["py_files_list"].append(item.name)

                        # Analyze Python file content
                        file_analysis = self.analyze_python_file(item, depth)
                        self.file_data.append(file_analysis)

                        # Aggregate
                        folder_info["total_lines"] += file_analysis["lines"]
                        folder_info["total_functions"] += file_analysis[
                            "function_count"
                        ]
                        folder_info["total_classes"] += file_analysis["class_count"]
                        folder_info["apis_found"].update(file_analysis["apis_used"])
                        folder_info["purposes"].update(file_analysis["purposes"])

            # Update global stats
            self.stats["total_folders"] += 1
            self.stats["total_python_files"] += folder_info["python_files"]
            self.stats["max_depth"] = max(self.stats["max_depth"], depth)

        except PermissionError:
            folder_info["error"] = "Permission denied"
        except Exception as e:
            folder_info["error"] = str(e)

        return folder_info

    def analyze_python_file(self, filepath, depth):
        """Analyze a single Python file"""
        analysis = {
            "filename": filepath.name,
            "full_path": str(filepath),
            "relative_path": str(filepath.relative_to(self.pythons_dir)),
            "parent_folder": filepath.parent.name,
            "depth": depth,
            "size_bytes": 0,
            "size_kb": 0,
            "lines": 0,
            "function_count": 0,
            "class_count": 0,
            "import_count": 0,
            "functions": [],
            "classes": [],
            "imports": [],
            "apis_used": [],
            "purposes": [],
            "complexity": 0,
            "has_main": False,
            "has_docstring": False,
            "error": None,
        }

        try:
            analysis["size_bytes"] = filepath.stat().st_size
            analysis["size_kb"] = round(analysis["size_bytes"] / 1024, 2)

            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            analysis["lines"] = len(content.splitlines())

            # Parse AST
            try:
                tree = ast.parse(content)

                # Get module docstring
                analysis["has_docstring"] = bool(ast.get_docstring(tree))

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis["imports"].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            analysis["imports"].append(node.module)
                    elif isinstance(node, ast.FunctionDef):
                        analysis["functions"].append(node.name)
                        if node.name == "main":
                            analysis["has_main"] = True
                    elif isinstance(node, ast.ClassDef):
                        analysis["classes"].append(node.name)

                analysis["function_count"] = len(analysis["functions"])
                analysis["class_count"] = len(analysis["classes"])
                analysis["import_count"] = len(set(analysis["imports"]))

            except SyntaxError:
                analysis["error"] = "Syntax error"

            # Detect APIs and purposes
            analysis["apis_used"] = self._detect_apis(content)
            analysis["purposes"] = self._detect_purposes(content, filepath.name)

            # Complexity
            analysis["complexity"] = (
                analysis["function_count"] * 2
                + analysis["class_count"] * 5
                + min(analysis["lines"] / 10, 50)
            )

        except Exception as e:
            analysis["error"] = str(e)

        return analysis

    def _detect_apis(self, content):
        """Detect API usage"""
        apis = []
        content_lower = content.lower()

        api_keywords = {
            "openai": ["openai", "gpt-", "chatgpt"],
            "anthropic": ["anthropic", "claude"],
            "youtube": ["youtube", "pytube"],
            "instagram": ["instagram", "instabot"],
            "reddit": ["reddit", "praw"],
            "suno": ["suno"],
            "leonardo": ["leonardo"],
            "whisper": ["whisper"],
            "elevenlabs": ["elevenlabs"],
            "streamlit": ["streamlit"],
            "selenium": ["selenium"],
            "pandas": ["pandas"],
            "numpy": ["numpy"],
        }

        for api, keywords in api_keywords.items():
            if any(kw in content_lower for kw in keywords):
                apis.append(api)

        return apis

    def _detect_purposes(self, content, filename):
        """Detect file purpose"""
        purposes = []
        text = (content + " " + filename).lower()

        purpose_keywords = {
            "automation": ["automat", "bot", "schedule"],
            "scraping": ["scrap", "crawl", "extract"],
            "generation": ["generat", "create", "produce"],
            "analysis": ["analyz", "scan", "report"],
            "organization": ["organiz", "sort", "clean"],
        }

        for purpose, keywords in purpose_keywords.items():
            if any(kw in text for kw in keywords):
                purposes.append(purpose)

        return purposes

    def scan_all(self):
        """Start recursive scan from root"""
        print("🔍 RECURSIVE DEEP SCAN - ANALYZING EVERY FOLDER")
        print("=" * 70)
        print(f"Scanning: {self.pythons_dir}")
        print("This will scan EVERY subdirectory at EVERY depth...\n")

        # Scan root
        root_info = self.scan_folder(self.pythons_dir, depth=0)
        self.folder_data.insert(0, root_info)

        print("\n✅ Scan complete!")
        print(f"   Folders analyzed: {self.stats['total_folders']}")
        print(f"   Python files: {self.stats['total_python_files']}")
        print(f"   Max depth: {self.stats['max_depth']}")

    def save_folder_csv(self):
        """Save folder analysis to CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = self.pythons_dir / f"RECURSIVE_FOLDER_SCAN_{timestamp}.csv"

        print("\n💾 Saving folder analysis CSV...")

        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "Folder Path",
                    "Folder Name",
                    "Depth",
                    "Python Files (Direct)",
                    "Python Files (Total)",
                    "Total Files",
                    "Subdirs Count",
                    "Size (MB)",
                    "Total Lines",
                    "Total Functions",
                    "Total Classes",
                    "Has README",
                    "Has Requirements",
                    "Has __init__",
                    "APIs Found",
                    "Purposes",
                    "Subdirectories",
                ]
            )

            for folder in sorted(self.folder_data, key=lambda x: x["relative_path"]):
                writer.writerow(
                    [
                        folder["relative_path"],
                        folder["folder_name"],
                        folder["depth"],
                        folder["direct_py_files"],
                        folder["python_files"],
                        folder["total_files"],
                        folder["total_dirs"],
                        round(folder["size_bytes"] / (1024 * 1024), 2),
                        folder["total_lines"],
                        folder["total_functions"],
                        folder["total_classes"],
                        folder["has_readme"],
                        folder["has_requirements"],
                        folder["has_init"],
                        ", ".join(sorted(folder["apis_found"])),
                        ", ".join(sorted(folder["purposes"])),
                        ", ".join(folder["subdirs"][:10]),  # First 10 subdirs
                    ]
                )

        print(f"✅ Saved: {csv_file.name}")
        return csv_file

    def save_file_csv(self):
        """Save file analysis to CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = self.pythons_dir / f"RECURSIVE_FILE_SCAN_{timestamp}.csv"

        print("💾 Saving file analysis CSV...")

        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "Filename",
                    "Relative Path",
                    "Parent Folder",
                    "Depth",
                    "Size (KB)",
                    "Lines",
                    "Functions",
                    "Classes",
                    "Imports",
                    "Has Main",
                    "Has Docstring",
                    "APIs Used",
                    "Purposes",
                    "Complexity",
                    "Error",
                ]
            )

            for file in sorted(self.file_data, key=lambda x: x["relative_path"]):
                writer.writerow(
                    [
                        file["filename"],
                        file["relative_path"],
                        file["parent_folder"],
                        file["depth"],
                        file["size_kb"],
                        file["lines"],
                        file["function_count"],
                        file["class_count"],
                        file["import_count"],
                        file["has_main"],
                        file["has_docstring"],
                        ", ".join(file["apis_used"]),
                        ", ".join(file["purposes"]),
                        round(file["complexity"], 1),
                        file["error"] or "",
                    ]
                )

        print(f"✅ Saved: {csv_file.name}")
        return csv_file

    def print_tree_summary(self):
        """Print tree-style summary"""
        print("\n" + "=" * 70)
        print("🌳 DIRECTORY TREE SUMMARY (Top 3 Levels)")
        print("=" * 70 + "\n")

        # Group by depth
        by_depth = defaultdict(list)
        for folder in self.folder_data:
            by_depth[folder["depth"]].append(folder)

        # Print depth 1 (root level)
        for folder in sorted(
            by_depth[1], key=lambda x: x["python_files"], reverse=True
        ):
            py_count = folder["python_files"]
            size_mb = folder["size_bytes"] / (1024 * 1024)
            print(
                f"📁 {folder['folder_name']:40} {py_count:5} files, {size_mb:7.1f} MB"
            )

            # Show its subdirectories (depth 2)
            subdirs_at_depth_2 = [
                f
                for f in by_depth[2]
                if f["relative_path"].startswith(folder["relative_path"])
            ]

            for subdir in sorted(
                subdirs_at_depth_2, key=lambda x: x["python_files"], reverse=True
            )[:5]:
                py_count = subdir["python_files"]
                print(f"  ├─ {subdir['folder_name']:37} {py_count:5} files")

            if len(subdirs_at_depth_2) > 5:
                print(f"  └─ ... and {len(subdirs_at_depth_2) - 5} more subdirs")

            print()

    def print_statistics(self):
        """Print overall statistics"""
        print("=" * 70)
        print("📊 RECURSIVE SCAN STATISTICS")
        print("=" * 70)
        print(f"Total folders analyzed:  {self.stats['total_folders']}")
        print(f"Total Python files:      {self.stats['total_python_files']}")
        print(f"Maximum depth:           {self.stats['max_depth']}")

        # Calculate totals
        total_size = sum(f["size_bytes"] for f in self.folder_data if f["depth"] == 0)
        total_lines = sum(f["total_lines"] for f in self.folder_data if f["depth"] == 0)
        total_funcs = sum(
            f["total_functions"] for f in self.folder_data if f["depth"] == 0
        )
        total_classes = sum(
            f["total_classes"] for f in self.folder_data if f["depth"] == 0
        )

        print(f"Total size:              {total_size / (1024 * 1024):.2f} MB")
        print(f"Total lines of code:     {total_lines:,}")
        print(f"Total functions:         {total_funcs:,}")
        print(f"Total classes:           {total_classes:,}")
        print("=" * 70)

    def find_issues(self):
        """Find potential issues in structure"""
        print("\n" + "=" * 70)
        print("⚠️  POTENTIAL ISSUES DETECTED")
        print("=" * 70 + "\n")

        issues = []

        # Find folders with very long names
        for folder in self.folder_data:
            if len(folder["folder_name"]) > 80:
                issues.append(f"❌ LONG NAME: {folder['relative_path']}")

        # Find folders with spaces
        for folder in self.folder_data:
            if " " in folder["folder_name"]:
                issues.append(f"⚠️  SPACES: {folder['relative_path']}")

        # Find deep nesting (>5 levels)
        for folder in self.folder_data:
            if folder["depth"] > 5:
                issues.append(
                    f"🔍 DEEP NESTING (depth {folder['depth']}): {folder['relative_path']}"
                )

        # Find folders with no Python files but has subdirs
        for folder in self.folder_data:
            if (
                folder["direct_py_files"] == 0
                and folder["total_dirs"] == 0
                and folder["total_files"] > 0
            ):
                issues.append(
                    f"📂 NO PY FILES: {folder['relative_path']} ({folder['total_files']} other files)"
                )

        # Find potential duplicates (similar names at same depth)
        by_depth_and_name = defaultdict(list)
        for folder in self.folder_data:
            by_depth_and_name[key].append(folder)

        for key, folders in by_depth_and_name.items():
            if len(folders) > 1:
                [f["relative_path"] for f in folders]
                issues.append(
                    f"♻️  DUPLICATE NAME: {folders[0]['folder_name']} appears in {len(folders)} locations"
                )

        # Print issues
        if issues:
            for issue in issues[:50]:  # Show first 50
                print(f"  {issue}")
            if len(issues) > 50:
                print(f"\n  ... and {len(issues) - 50} more issues")
        else:
            print("  ✅ No major issues detected!")

        return issues


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🔍 RECURSIVE DEEP SCAN - EVERY FOLDER AT EVERY DEPTH         ║
║     Complete analysis of entire ~/pythons/ structure             ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    scanner = RecursiveDeepScanner()

    # Scan everything
    scanner.scan_all()

    # Print statistics
    scanner.print_statistics()

    # Print tree
    scanner.print_tree_summary()

    # Find issues
    issues = scanner.find_issues()

    # Save CSVs
    folder_csv = scanner.save_folder_csv()
    file_csv = scanner.save_file_csv()

    print("\n" + "=" * 70)
    print("✨ RECURSIVE SCAN COMPLETE!")
    print("=" * 70)
    print(f"📄 Folder analysis: {folder_csv.name}")
    print(f"📄 File analysis:   {file_csv.name}")
    print(f"⚠️  Issues found:    {len(issues)}")
    print("=" * 70)


if __name__ == "__main__":
    main()

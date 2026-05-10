#!/usr/bin/env python3
"""
🔍 CONTENT SIMILARITY SCANNER
Find files with similar CODE/FUNCTIONALITY (not just names)
"""

import ast
import hashlib
from pathlib import Path
from collections import defaultdict
import csv
from datetime import datetime


class ContentSimilarityScanner:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.files = []

    def get_code_signature(self, filepath):
        """Extract code signature (functions, classes, imports)"""
        signature = {
            "path": filepath,
            "size": 0,
            "functions": [],
            "classes": [],
            "imports": [],
            "code_hash": None,
            "normalized_hash": None,
            "lines": 0,
        }

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            signature["size"] = len(content)
            signature["lines"] = len(content.splitlines())

            # Full content hash
            signature["code_hash"] = hashlib.md5(content.encode()).hexdigest()

            # Normalized hash (remove comments and whitespace)
            normalized = "\n".join(
                line.split("#")[0].strip()
                for line in content.splitlines()
                if line.strip() and not line.strip().startswith("#")
            )
            signature["normalized_hash"] = hashlib.md5(normalized.encode()).hexdigest()

            # Parse AST
            try:
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Get function signature
                        args = [arg.arg for arg in node.args.args]
                        signature["functions"].append(
                            {
                                "name": node.name,
                                "args": args,
                                "signature": f"{node.name}({','.join(args)})",
                            }
                        )

                    elif isinstance(node, ast.ClassDef):
                        methods = [
                            n.name for n in node.body if isinstance(n, ast.FunctionDef)
                        ]
                        signature["classes"].append(
                            {"name": node.name, "methods": methods}
                        )

                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            signature["imports"].append(alias.name)

                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            signature["imports"].append(node.module)

            except:
                pass

        except Exception as e:
            signature["error"] = str(e)

        return signature

    def scan_all_files(self):
        """Scan all files and extract signatures"""
        print("🔍 CONTENT SIMILARITY SCAN - Analyzing code structure...\n")

        files = [
            f
            for f in self.pythons_dir.rglob("*.py")
            if "_archive" not in str(f)
            and "2T-Xx-python" not in str(f)
            and ".venv" not in str(f)
            and ".history" not in str(f)
        ]

        print(f"📂 Analyzing {len(files)} files...\n")

        for i, f in enumerate(files, 1):
            sig = self.get_code_signature(f)
            self.files.append(sig)

            if i % 500 == 0:
                print(f"   ... analyzed {i} files")

        print("\n✅ Analysis complete!\n")
        return len(self.files)

    def find_identical_code(self):
        """Find files with identical code"""
        print("🔍 Finding files with identical code...\n")

        # Group by normalized hash (ignores comments/whitespace)
        by_hash = defaultdict(list)
        for file_sig in self.files:
            if file_sig["normalized_hash"]:
                by_hash[file_sig["normalized_hash"]].append(file_sig)

        # Find groups with multiple files
        identical = [group for group in by_hash.values() if len(group) > 1]
        identical.sort(key=lambda x: len(x), reverse=True)

        print(f"Found {len(identical)} sets of files with identical code\n")

        return identical

    def find_similar_structure(self):
        """Find files with very similar structure (same functions/classes)"""
        print("🔍 Finding files with similar structure...\n")

        similar_groups = []

        # Group by function signatures
        by_funcs = defaultdict(list)
        for file_sig in self.files:
            if file_sig["functions"]:
                # Create signature from function names
                func_sig = tuple(sorted([f["name"] for f in file_sig["functions"]]))
                if len(func_sig) >= 3:  # At least 3 functions
                    by_funcs[func_sig].append(file_sig)

        # Find groups with same function signatures
        for func_sig, group in by_funcs.items():
            if len(group) > 1:
                similar_groups.append(
                    {"type": "same_functions", "signature": func_sig, "files": group}
                )

        # Group by class signatures
        by_classes = defaultdict(list)
        for file_sig in self.files:
            if file_sig["classes"]:
                class_sig = tuple(sorted([c["name"] for c in file_sig["classes"]]))
                if len(class_sig) >= 2:  # At least 2 classes
                    by_classes[class_sig].append(file_sig)

        for class_sig, group in by_classes.items():
            if len(group) > 1:
                similar_groups.append(
                    {"type": "same_classes", "signature": class_sig, "files": group}
                )

        # Sort by group size
        similar_groups.sort(key=lambda x: len(x["files"]), reverse=True)

        print(f"Found {len(similar_groups)} sets of files with similar structure\n")

        return similar_groups

    def find_similar_imports(self):
        """Find files with very similar imports (likely similar purpose)"""
        print("🔍 Finding files with similar imports...\n")

        similar_imports = []

        # Group by import sets
        by_imports = defaultdict(list)
        for file_sig in self.files:
            if len(file_sig["imports"]) >= 5:  # At least 5 imports
                import_sig = tuple(sorted(set(file_sig["imports"])))
                by_imports[import_sig].append(file_sig)

        for import_sig, group in by_imports.items():
            if len(group) > 3:  # More than 3 files with exact same imports
                similar_imports.append(
                    {"imports": import_sig, "count": len(group), "files": group}
                )

        similar_imports.sort(key=lambda x: x["count"], reverse=True)

        print(f"Found {len(similar_imports)} import patterns with 4+ matching files\n")

        return similar_imports

    def save_results(self, identical, similar_structure, similar_imports):
        """Save results to CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 1. Identical code
        csv_file = self.pythons_dir / f"IDENTICAL_CODE_{timestamp}.csv"
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Group ID", "File Count", "File Paths", "Function Count", "Size (KB)"]
            )

            for i, group in enumerate(identical, 1):
                paths = " | ".join(
                    str(f["path"].relative_to(self.pythons_dir)) for f in group
                )
                func_count = len(group[0]["functions"])
                size = group[0]["size"] / 1024
                writer.writerow([i, len(group), paths, func_count, f"{size:.1f}"])

        print(f"✅ Saved: {csv_file.name}")

        # 2. Similar structure
        csv_file2 = self.pythons_dir / f"SIMILAR_STRUCTURE_{timestamp}.csv"
        with open(csv_file2, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "Signature", "File Count", "File Paths"])

            for group in similar_structure[:500]:
                paths = " | ".join(
                    str(f["path"].relative_to(self.pythons_dir)) for f in group["files"]
                )
                sig_str = ", ".join(group["signature"][:10])
                writer.writerow([group["type"], sig_str, len(group["files"]), paths])

        print(f"✅ Saved: {csv_file2.name}")

        # 3. Similar imports
        csv_file3 = self.pythons_dir / f"SIMILAR_IMPORTS_{timestamp}.csv"
        with open(csv_file3, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Import Count", "File Count", "Imports", "File Paths"])

            for group in similar_imports[:200]:
                imports_str = ", ".join(group["imports"][:15])
                paths = " | ".join(
                    str(f["path"].relative_to(self.pythons_dir))
                    for f in group["files"][:10]
                )
                writer.writerow(
                    [len(group["imports"]), group["count"], imports_str, paths]
                )

        print(f"✅ Saved: {csv_file3.name}")


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🔍 CONTENT SIMILARITY SCANNER                                 ║
║     Find files with similar CODE (not just similar names!)       ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    scanner = ContentSimilarityScanner()

    # Scan all files
    count = scanner.scan_all_files()

    # Find different types of duplicates
    identical = scanner.find_identical_code()
    similar_structure = scanner.find_similar_structure()
    similar_imports = scanner.find_similar_imports()

    # Print summary
    print("=" * 70)
    print("📊 CONTENT SIMILARITY SUMMARY")
    print("=" * 70)
    print(f"Files analyzed:           {count}")
    print(f"Identical code:           {len(identical)} sets")
    print(f"Similar structure:        {len(similar_structure)} sets")
    print(f"Similar imports:          {len(similar_imports)} sets")
    print("=" * 70)

    # Show top findings
    if identical:
        print("\n🔥 TOP 20 IDENTICAL CODE SETS:\n")
        for i, group in enumerate(identical[:20], 1):
            print(f"{i:2}. {len(group)} files with IDENTICAL code:")
            for file_sig in group[:5]:
                print(f"    • {file_sig['path'].name} ({file_sig['lines']} lines)")
            if len(group) > 5:
                print(f"    ... and {len(group) - 5} more")
            print()

    if similar_structure:
        print("🔥 TOP 15 SIMILAR STRUCTURE SETS:\n")
        for i, group in enumerate(similar_structure[:15], 1):
            print(f"{i:2}. {len(group['files'])} files with same {group['type']}:")
            if group["type"] == "same_functions":
                print(f"    Functions: {', '.join(list(group['signature'])[:5])}")
            else:
                print(f"    Classes: {', '.join(list(group['signature'])[:5])}")

            for file_sig in group["files"][:4]:
                print(f"    • {file_sig['path'].name}")
            if len(group["files"]) > 4:
                print(f"    ... and {len(group['files']) - 4} more")
            print()

    # Save results
    print("💾 Saving detailed reports...")
    scanner.save_results(identical, similar_structure, similar_imports)

    print("\n✅ Content similarity analysis complete!")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Deep dive analysis with content and function comparison.
Compares files by actual content, functions, and functionality.
"""

import sys
import hashlib
import ast
import difflib
from pathlib import Path
from collections import defaultdict
import re


class ContentAnalyzer:
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.stats = {
            "total_files": 0,
            "exact_duplicates": defaultdict(list),
            "functional_duplicates": defaultdict(list),
            "similar_content": defaultdict(list),
            "python_functions": defaultdict(list),
            "python_classes": defaultdict(list),
            "empty_files": [],
            "errors": [],
        }

    def extract_python_functions(self, file_path):
        """Extract function and class definitions from Python file."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            try:
                tree = ast.parse(content)
                functions = []
                classes = []

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name = node.name
                        # Get function signature
                        args = [arg.arg for arg in node.args.args]
                        func_sig = f"{func_name}({', '.join(args)})"
                        functions.append(func_sig)

                    elif isinstance(node, ast.ClassDef):
                        classes.append(node.name)

                return {
                    "functions": sorted(functions),
                    "classes": sorted(classes),
                    "function_count": len(functions),
                    "class_count": len(classes),
                }
            except SyntaxError:
                # Not valid Python, return empty
                return {
                    "functions": [],
                    "classes": [],
                    "function_count": 0,
                    "class_count": 0,
                }
        except Exception:
            return None

    def extract_text_features(self, file_path, max_lines=100):
        """Extract features from text files for comparison."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = [line.strip() for line in f.readlines()[:max_lines]]

            # Extract key features
            content = "\n".join(lines)

            # Count code-like patterns
            has_imports = bool(re.search(r"^(import|from)\s+", content, re.MULTILINE))
            has_functions = bool(re.search(r"def\s+\w+", content))
            has_classes = bool(re.search(r"class\s+\w+", content))
            has_urls = bool(re.search(r"https?://", content))
            has_emails = bool(re.search(r"\b[\w.-]+@[\w.-]+\.\w+\b", content))

            # Get first few non-empty lines as signature
            signature_lines = [line for line in lines[:10] if line.strip()][:5]

            return {
                "line_count": len(lines),
                "has_imports": has_imports,
                "has_functions": has_functions,
                "has_classes": has_classes,
                "has_urls": has_urls,
                "has_emails": has_emails,
                "signature": "\n".join(signature_lines),
                "content_hash": hashlib.md5(content.encode()).hexdigest()[:16],
            }
        except Exception:
            return None

    def compare_python_files(self, file1_path, file2_path):
        """Compare two Python files by their functions and classes."""
        funcs1 = self.extract_python_functions(file1_path)
        funcs2 = self.extract_python_functions(file2_path)

        if not funcs1 or not funcs2:
            return None

        # Compare functions
        funcs1_set = set(funcs1["functions"])
        funcs2_set = set(funcs2["functions"])

        common_funcs = funcs1_set & funcs2_set
        all_funcs = funcs1_set | funcs2_set

        similarity = len(common_funcs) / len(all_funcs) if all_funcs else 0

        return {
            "similarity": similarity,
            "common_functions": len(common_funcs),
            "total_functions": len(all_funcs),
            "functions1": funcs1["functions"],
            "functions2": funcs2["functions"],
            "classes1": funcs1["classes"],
            "classes2": funcs2["classes"],
        }

    def compare_text_content(self, file1_path, file2_path, threshold=0.8):
        """Compare text files by content similarity."""
        try:
            with open(file1_path, "r", encoding="utf-8", errors="ignore") as f1:
                content1 = f1.read()
            with open(file2_path, "r", encoding="utf-8", errors="ignore") as f2:
                content2 = f2.read()

            # Use SequenceMatcher for similarity
            similarity = difflib.SequenceMatcher(None, content1, content2).ratio()

            if similarity >= threshold:
                # Check if one is subset of another
                is_subset = content1 in content2 or content2 in content1

                return {
                    "similarity": similarity,
                    "is_subset": is_subset,
                    "size1": len(content1),
                    "size2": len(content2),
                }
        except Exception:
            return None

    def analyze(self):
        """Perform comprehensive content analysis."""
        print("=" * 80)
        print("DEEP DIVE CONTENT & FUNCTION ANALYSIS")
        print("=" * 80)
        print(f"\n📂 Analyzing: {self.root_path}")

        if not self.root_path.exists():
            print(f"\n❌ Error: Directory not found: {self.root_path}")
            return False

        # Collect all files
        print("\n📋 Scanning files...")
        all_files = []
        python_files = []
        text_files = []

        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                try:
                    stat = file_path.stat()
                    rel_path = str(file_path.relative_to(self.root_path))
                    ext = file_path.suffix.lower()

                    file_info = {
                        "path": file_path,
                        "rel_path": rel_path,
                        "size": stat.st_size,
                        "ext": ext,
                        "name": file_path.name,
                    }

                    all_files.append(file_info)
                    self.stats["total_files"] += 1

                    if ext == ".py":
                        python_files.append(file_info)
                    elif ext in [
                        ".txt",
                        ".md",
                        ".csv",
                        ".json",
                        ".html",
                        ".yaml",
                        ".yml",
                        ".sh",
                        ".js",
                    ]:
                        text_files.append(file_info)

                    if stat.st_size == 0:
                        self.stats["empty_files"].append(rel_path)

                except Exception as e:
                    self.stats["errors"].append(f"Error accessing {file_path}: {e}")

        print(f"   Found {len(all_files):,} files")
        print(f"   Python files: {len(python_files):,}")
        print(f"   Text files: {len(text_files):,}")

        # Hash-based exact duplicates
        print("\n🔍 Finding exact duplicates (hash-based)...")
        hash_map = defaultdict(list)

        for file_info in all_files:
            if (
                file_info["size"] > 0 and file_info["size"] < 100 * 1024 * 1024
            ):  # < 100MB
                try:
                    file_hash = hashlib.md5()
                    with open(file_info["path"], "rb") as f:
                        while chunk := f.read(8192):
                            file_hash.update(chunk)
                    hash_map[hash_key].append(file_info["rel_path"])
                except Exception:
                    pass

        for file_hash, file_list in hash_map.items():
            if len(file_list) > 1:
                self.stats["exact_duplicates"][file_hash] = file_list

        print(
            f"   Found {len(self.stats['exact_duplicates'])} groups of exact duplicates"
        )

        # Analyze Python files for functional duplicates
        print("\n🐍 Analyzing Python files for functional duplicates...")
        python_analysis = {}

        for file_info in python_files:
            rel_path = file_info["rel_path"]
            analysis = self.extract_python_functions(file_info["path"])
            if analysis:
                python_analysis[rel_path] = analysis

                # Group by function signatures
                if func_key:
                    self.stats["python_functions"][func_key].append(rel_path)

                # Group by class names
                if class_key:
                    self.stats["python_classes"][class_key].append(rel_path)

        print(f"   Analyzed {len(python_analysis)} Python files")

        # Compare Python files with similar functions (optimized)
        print("   Comparing Python files with similar functions...")
        compared = set()
        python_list = list(python_analysis.items())

        # First, group by function signatures to reduce comparisons
        func_groups = defaultdict(list)
        for path, info in python_list:
            if info["functions"]:
                func_groups[func_key].append(path)

        # Compare within groups and between similar groups
        for func_key, paths in func_groups.items():
            if len(paths) > 1:
                # Same functions - definitely duplicates
                for path in paths:
                    self.stats["functional_duplicates"][f"group_{func_key[:20]}"] = {
                        "type": "python",
                        "similarity": 1.0,
                        "common_functions": len(func_key),
                        "files": paths,
                        "functions": list(func_key),
                    }
                    break  # Only add once per group

        # Compare files with overlapping functions (limited comparisons)
        print(f"     Comparing {min(100, len(python_list))} Python files...")
        for i, (path1, info1) in enumerate(python_list[:100]):  # Limit comparisons
            if i % 20 == 0:
                print(f"       Processed {i}/{min(100, len(python_list))}...", end="\r")
            for path2, info2 in python_list[
                i + 1 : min(i + 50, len(python_list))
            ]:  # Limit to 50 comparisons per file
                if pair_key in compared:
                    continue
                compared.add(pair_key)

                # Quick check: if they share functions
                funcs1_set = set(info1["functions"])
                funcs2_set = set(info2["functions"])
                if funcs1_set & funcs2_set:  # Has common functions
                    comparison = self.compare_python_files(
                        self.root_path / path1, self.root_path / path2
                    )

                    if comparison and comparison["similarity"] >= 0.5:
                        self.stats["functional_duplicates"][func_key] = {
                            "type": "python",
                            "similarity": comparison["similarity"],
                            "common_functions": comparison["common_functions"],
                            "files": [path1, path2],
                            "details": comparison,
                        }
        print()

        # Analyze text files for similar content
        print("\n📄 Analyzing text files for similar content...")
        text_analysis = {}

        for file_info in text_files[:500]:  # Limit to first 500 for performance
            rel_path = file_info["rel_path"]
            features = self.extract_text_features(file_info["path"])
            if features:
                text_analysis[rel_path] = features

        print(f"   Analyzed {len(text_analysis)} text files")

        # Compare text files (optimized - only compare with same signature)
        print("   Comparing text files for similar content...")
        compared = set()
        text_list = list(text_analysis.items())

        # Group by signature first
        sig_groups = defaultdict(list)
        for path, features in text_list:
            if features["signature"]:
                sig_groups[features["signature"]].append((path, features))

        # Compare within signature groups
        print(f"     Comparing {len(text_list)} text files...")
        for sig, group in sig_groups.items():
            if len(group) > 1:
                for i, (path1, features1) in enumerate(group):
                    for path2, features2 in group[i + 1 :]:
                        if pair_key in compared:
                            continue
                        compared.add(pair_key)

                        comparison = self.compare_text_content(
                            self.root_path / path1, self.root_path / path2
                        )

                        if comparison and comparison["similarity"] >= 0.8:
                            self.stats["similar_content"][content_key] = {
                                "type": "text",
                                "similarity": comparison["similarity"],
                                "files": [path1, path2],
                                "details": comparison,
                            }

        # Also compare files with same content hash
        content_hash_groups = defaultdict(list)
        for path, features in text_list:
            if features.get("content_hash"):
                content_hash_groups[features["content_hash"]].append(path)

        for content_hash, paths in content_hash_groups.items():
            if len(paths) > 1:
                for path in paths:
                    self.stats["similar_content"][f"hash_{content_hash}"] = {
                        "type": "text",
                        "similarity": 1.0,
                        "files": paths,
                        "details": {"similarity": 1.0, "is_subset": False},
                    }
                    break
        print()

        return True

    def print_report(self):
        """Print comprehensive analysis report."""
        print("\n" + "=" * 80)
        print("CONTENT & FUNCTION ANALYSIS REPORT")
        print("=" * 80)

        print("\n📊 BASIC STATISTICS")
        print(f"   Total files analyzed: {self.stats['total_files']:,}")
        print(f"   Empty files: {len(self.stats['empty_files']):,}")

        # Exact duplicates
        print("\n🔍 EXACT DUPLICATES (Same Content/Hash)")
        exact_count = sum(
            len(files) for files in self.stats["exact_duplicates"].values()
        )
        print(f"   Duplicate groups: {len(self.stats['exact_duplicates'])}")
        print(f"   Total duplicate files: {exact_count}")

        if self.stats["exact_duplicates"]:
            print("\n   Top duplicate groups:")
            for hash_key, file_list in list(self.stats["exact_duplicates"].items())[
                :10
            ]:
                print(f"   Hash: {hash_key[:16]}... ({len(file_list)} copies)")
                for rel_path in file_list[:3]:
                    print(f"     - {rel_path}")
                if len(file_list) > 3:
                    print(f"     ... and {len(file_list) - 3} more")

        # Functional duplicates (Python)
        print("\n🐍 FUNCTIONAL DUPLICATES (Python Files)")
        print(
            f"   Python files with similar functions: {len(self.stats['functional_duplicates'])}"
        )

        if self.stats["functional_duplicates"]:
            print("\n   Files with similar functionality:")
            for key, info in list(self.stats["functional_duplicates"].items())[:15]:
                print(f"   {info['files'][0]}")
                print(f"   <-> {info['files'][1]}")
                print(f"      Similarity: {info['similarity'] * 100:.1f}%")
                print(f"      Common functions: {info['common_functions']}")
                if info["details"]["functions1"]:
                    print(
                        f"      Functions in file 1: {', '.join(info['details']['functions1'][:5])}"
                    )
                    if len(info["details"]["functions1"]) > 5:
                        print(
                            f"        ... and {len(info['details']['functions1']) - 5} more"
                        )
                print()

        # Python files with same functions
        print("\n📦 PYTHON FILES WITH IDENTICAL FUNCTIONS")
        func_dupes = {
            k: v for k, v in self.stats["python_functions"].items() if len(v) > 1
        }
        if func_dupes:
            print(f"   Found {len(func_dupes)} function signature groups")
            for func_sig, file_list in list(func_dupes.items())[:10]:
                print(
                    f"   Functions: {', '.join(func_sig[:3])}{'...' if len(func_sig) > 3 else ''}"
                )
                print(f"      Found in {len(file_list)} files:")
                for rel_path in file_list[:3]:
                    print(f"        - {rel_path}")
                if len(file_list) > 3:
                    print(f"        ... and {len(file_list) - 3} more")
        else:
            print("   ✅ No Python files with identical function signatures")

        # Similar content (text files)
        print("\n📄 SIMILAR CONTENT (Text Files)")
        print(
            f"   Text files with similar content: {len(self.stats['similar_content'])}"
        )

        if self.stats["similar_content"]:
            print("\n   Files with similar content (>80% similarity):")
            for key, info in list(self.stats["similar_content"].items())[:15]:
                print(f"   {info['files'][0]}")
                print(f"   <-> {info['files'][1]}")
                print(f"      Similarity: {info['similarity'] * 100:.1f}%")
                if info["details"]["is_subset"]:
                    print("      ⚠️  One file appears to be a subset of the other")
                print()

        # Empty files
        if self.stats["empty_files"]:
            print(f"\n📭 EMPTY FILES ({len(self.stats['empty_files'])} found)")
            for empty_file in self.stats["empty_files"][:20]:
                print(f"   - {empty_file}")
            if len(self.stats["empty_files"]) > 20:
                print(f"   ... and {len(self.stats['empty_files']) - 20} more")

        # Errors
        if self.stats["errors"]:
            print(f"\n⚠️  ERRORS ({len(self.stats['errors'])} found)")
            for error in self.stats["errors"][:10]:
                print(f"   - {error}")

        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deepdive_content_analysis.py <directory>")
        print("\nExample:")
        print("  python deepdive_content_analysis.py /path/to/dir")
        sys.exit(1)

    root_path = sys.argv[1]

    analyzer = ContentAnalyzer(root_path)
    if analyzer.analyze():
        analyzer.print_report()

#!/usr/bin/env python3
"""
Compare content and functions across Python files in the directory.
Identifies duplicate functions, similar code, and potential consolidation opportunities.
"""

import os
import ast
import hashlib
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from difflib import SequenceMatcher

TARGET_DIR = "/Users/steven/pythons"
OUTPUT_DIR = "/Users/steven/pythons/function_analysis"


def similar(a, b):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()


def get_function_hash(source_code):
    """Get hash of function source code (normalized)."""
    # Normalize: remove leading/trailing whitespace, normalize newlines
    normalized = source_code.strip().replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.md5(normalized.encode()).hexdigest()


class FunctionExtractor(ast.NodeVisitor):
    """Extract function and class definitions from Python AST."""

    def __init__(self):
        self.functions = []
        self.classes = []
        self.current_class = None

    def visit_FunctionDef(self, node):
        # Get function source (as string representation)
        func_info = {
            "name": node.name,
            "line": node.lineno,
            "args": [arg.arg for arg in node.args.args],
            "class": self.current_class,
            "decorators": [ast.dump(d) for d in node.decorator_list],
        }

        # Source will be extracted from file lines later
        func_info["source"] = None

        # Create a signature representation
        signature = f"{node.name}({', '.join(func_info['args'])})"
        if self.current_class:
            signature = f"{self.current_class}.{signature}"
        func_info["signature"] = signature

        self.functions.append(func_info)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        old_class = self.current_class
        self.current_class = node.name
        self.classes.append({"name": node.name, "line": node.lineno, "methods": []})
        self.generic_visit(node)
        self.current_class = old_class


def extract_functions_from_file(filepath):
    """Extract functions from a Python file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()

        try:
            tree = ast.parse(source, filename=str(filepath))
        except SyntaxError as e:
            return {
                "file": str(filepath),
                "error": f"Syntax error: {e}",
                "functions": [],
                "classes": [],
            }

        extractor = FunctionExtractor()
        extractor.visit(tree)

        # Also extract source code for each function
        lines = source.split("\n")
        for func_info in extractor.functions:
            try:
                # Get function lines (approximate)
                start_line = func_info["line"] - 1
                end_line = min(start_line + 50, len(lines))  # Limit to first 50 lines
                func_source = "\n".join(lines[start_line:end_line])
                func_info["source_preview"] = func_source[:500]  # First 500 chars

                # Calculate hash
                func_info["hash"] = get_function_hash(func_source)
            except:
                func_info["source_preview"] = None
                func_info["hash"] = None

        return {
            "file": str(filepath),
            "functions": extractor.functions,
            "classes": extractor.classes,
            "total_lines": len(lines),
        }
    except Exception as e:
        return {"file": str(filepath), "error": str(e), "functions": [], "classes": []}


def analyze_directory(directory):
    """Analyze all Python files in directory."""
    print(f"🔍 Analyzing Python files in {directory}...")

    all_files = []
    all_functions = []
    hash_to_functions = defaultdict(list)
    name_to_functions = defaultdict(list)

    # Find all Python files
    python_files = list(Path(directory).rglob("*.py"))
    print(f"   Found {len(python_files)} Python files")

    # Exclude common directories
    exclude_dirs = {"__pycache__", ".git", "venv", "env", ".venv", "node_modules"}
    python_files = [
        f for f in python_files if not any(ex in str(f) for ex in exclude_dirs)
    ]

    print(f"   Processing {len(python_files)} files (after exclusions)...\n")

    # Extract functions from each file
    for i, filepath in enumerate(python_files, 1):
        if i % 100 == 0:
            print(f"   Processed {i}/{len(python_files)} files...")

        result = extract_functions_from_file(filepath)
        all_files.append(result)

        for func_info in result["functions"]:
            func_info["file"] = result["file"]
            all_functions.append(func_info)

            # Index by hash
            if func_info.get("hash"):
                hash_to_functions[func_info["hash"]].append(func_info)

            # Index by name
            name_to_functions[func_info["signature"]].append(func_info)

    print("\n✅ Analysis complete!")
    print(f"   Total files: {len(all_files)}")
    print(f"   Total functions: {len(all_functions)}")
    print(f"   Unique function signatures: {len(name_to_functions)}")
    print(
        f"   Duplicate function hashes: {len([h for h, funcs in hash_to_functions.items() if len(funcs) > 1])}"
    )

    return {
        "files": all_files,
        "functions": all_functions,
        "hash_to_functions": hash_to_functions,
        "name_to_functions": name_to_functions,
    }


def generate_report(analysis, output_dir):
    """Generate detailed comparison report."""
    os.makedirs(output_dir, exist_ok=True)

    hash_to_functions = analysis["hash_to_functions"]
    name_to_functions = analysis["name_to_functions"]

    # 1. Duplicate functions (exact matches by hash)
    duplicate_hashes = {
        h: funcs for h, funcs in hash_to_functions.items() if len(funcs) > 1
    }

    # 2. Functions with same name/signature (potential duplicates)
    duplicate_names = {
        name: funcs for name, funcs in name_to_functions.items() if len(funcs) > 1
    }

    # 3. Generate reports
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Main report
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_files": len(analysis["files"]),
            "total_functions": len(analysis["functions"]),
            "unique_signatures": len(name_to_functions),
            "duplicate_hashes": len(duplicate_hashes),
            "duplicate_names": len(duplicate_names),
        },
        "duplicate_functions_by_hash": {},
        "duplicate_functions_by_name": {},
    }

    # Add duplicate hash details (limit to top 50)
    for hash_val, funcs in list(duplicate_hashes.items())[:50]:
        report["duplicate_functions_by_hash"][hash_val] = [
            {"signature": f["signature"], "file": f["file"], "line": f["line"]}
            for f in funcs
        ]

    # Add duplicate name details (limit to top 50)
    for name, funcs in list(duplicate_names.items())[:50]:
        report["duplicate_functions_by_name"][name] = [
            {
                "file": f["file"],
                "line": f["line"],
                "args": f["args"],
                "hash": f.get("hash", "N/A"),
            }
            for f in funcs
        ]

    # Save JSON report
    json_path = os.path.join(output_dir, f"function_analysis_{timestamp}.json")
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n📄 JSON report saved: {json_path}")

    # Generate human-readable report
    txt_path = os.path.join(output_dir, f"function_analysis_{timestamp}.txt")
    with open(txt_path, "w") as f:
        f.write("=" * 80 + "\n")
        f.write("PYTHON FUNCTION ANALYSIS REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")

        # Summary
        f.write("SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Python files analyzed: {report['summary']['total_files']}\n")
        f.write(f"Total functions found: {report['summary']['total_functions']}\n")
        f.write(
            f"Unique function signatures: {report['summary']['unique_signatures']}\n"
        )
        f.write(
            f"Exact duplicate functions (by hash): {report['summary']['duplicate_hashes']}\n"
        )
        f.write(
            f"Functions with same name (potential duplicates): {report['summary']['duplicate_names']}\n\n"
        )

        # Duplicate functions by hash
        f.write("=" * 80 + "\n")
        f.write("EXACT DUPLICATE FUNCTIONS (Same Content Hash)\n")
        f.write("=" * 80 + "\n\n")

        if duplicate_hashes:
            for i, (hash_val, funcs) in enumerate(
                list(duplicate_hashes.items())[:30], 1
            ):
                f.write(f"\nDuplicate Group {i} (Hash: {hash_val[:16]}...)\n")
                f.write("-" * 80 + "\n")
                for func in funcs:
                    f.write(f"  {func['signature']}\n")
                    f.write(f"    File: {func['file']}\n")
                    f.write(f"    Line: {func['line']}\n")
        else:
            f.write("No exact duplicates found.\n")

        # Duplicate functions by name
        f.write("\n" + "=" * 80 + "\n")
        f.write("FUNCTIONS WITH SAME NAME/SIGNATURE (Potential Duplicates)\n")
        f.write("=" * 80 + "\n\n")

        if duplicate_names:
            for i, (name, funcs) in enumerate(list(duplicate_names.items())[:50], 1):
                f.write(f"\n{i}. {name} ({len(funcs)} occurrences)\n")
                f.write("-" * 80 + "\n")
                for func in funcs:
                    f.write(f"  File: {func['file']}\n")
                    f.write(f"  Line: {func['line']}\n")
                    f.write(f"  Args: {', '.join(func['args'])}\n")
                    f.write(
                        f"  Hash: {func.get('hash', 'N/A')[:16] if func.get('hash') else 'N/A'}...\n"
                    )
                    f.write("\n")
        else:
            f.write("No duplicate names found.\n")

    print(f"📄 Text report saved: {txt_path}")

    return report


def main():
    """Main function."""
    print("🔍 Python Function & Content Comparison Tool")
    print("=" * 60 + "\n")

    # Analyze directory
    analysis = analyze_directory(TARGET_DIR)

    # Generate reports
    print("\n📊 Generating reports...")
    report = generate_report(analysis, OUTPUT_DIR)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total files analyzed: {report['summary']['total_files']}")
    print(f"Total functions: {report['summary']['total_functions']}")
    print(f"Unique signatures: {report['summary']['unique_signatures']}")
    print(f"Exact duplicates (same hash): {report['summary']['duplicate_hashes']}")
    print(f"Same name (potential duplicates): {report['summary']['duplicate_names']}")
    print(f"\n📁 Reports saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()

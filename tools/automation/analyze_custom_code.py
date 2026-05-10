#!/usr/bin/env python3
"""
Analyze custom/unique code within the codebase.
Identifies unique functions (non-duplicated) and custom implementations.
"""

import os
import ast
import hashlib
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

TARGET_DIR = "/Users/steven/pythons"
ANALYSIS_DIR = "/Users/steven/pythons/function_analysis"
OUTPUT_DIR = "/Users/steven/pythons/custom_code_analysis"


def get_function_hash(source_code):
    """Get hash of function source code (normalized)."""
    normalized = source_code.strip().replace("\r\n", "\n").replace("\r", "\n")
    normalized = "\n".join(line.rstrip() for line in normalized.split("\n"))
    return hashlib.md5(normalized.encode()).hexdigest()


def get_function_source(filepath, start_line, max_lines=200):
    """Extract function source code from file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        start_idx = max(0, start_line - 1)
        end_idx = min(len(lines), start_idx + max_lines)

        # Find function end
        if start_idx < len(lines):
            base_indent = len(lines[start_idx]) - len(lines[start_idx].lstrip())
            for i in range(start_idx + 1, len(lines)):
                line = lines[i]
                if (
                    line.strip()
                    and not line.startswith(" " * (base_indent + 1))
                    and not line.startswith("\t" * (base_indent // 4 + 1))
                ):
                    if not (
                        line.strip().startswith("@") or line.strip().startswith("#")
                    ):
                        end_idx = i
                        break

        return "".join(lines[start_idx:end_idx])
    except Exception as e:
        return f"Error: {e}"


class FunctionExtractor(ast.NodeVisitor):
    """Extract function definitions from Python AST."""

    def __init__(self):
        self.functions = []
        self.current_class = None

    def visit_FunctionDef(self, node):
        func_info = {
            "name": node.name,
            "line": node.lineno,
            "end_line": getattr(node, "end_lineno", node.lineno + 50),
            "args": [arg.arg for arg in node.args.args],
            "class": self.current_class,
            "decorators": [ast.dump(d) for d in node.decorator_list],
        }

        signature = f"{node.name}({', '.join(func_info['args'])})"
        if self.current_class:
            signature = f"{self.current_class}.{signature}"
        func_info["signature"] = signature

        self.functions.append(func_info)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class


def extract_functions_from_file(filepath):
    """Extract functions from a Python file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()

        try:
            tree = ast.parse(source, filename=str(filepath))
        except SyntaxError:
            return {"file": str(filepath), "functions": [], "error": "Syntax error"}

        extractor = FunctionExtractor()
        extractor.visit(tree)

        # Get source code for each function
        for func_info in extractor.functions:
            func_source = get_function_source(
                filepath,
                func_info["line"],
                func_info["end_line"] - func_info["line"] + 10,
            )
            func_info["source"] = func_source
            func_info["hash"] = get_function_hash(func_source)

        return {
            "file": str(filepath),
            "functions": extractor.functions,
            "total_lines": len(source.splitlines()),
        }
    except Exception as e:
        return {"file": str(filepath), "functions": [], "error": str(e)}


def analyze_custom_code():
    """Analyze unique/custom code (non-duplicated functions)."""
    print("🔍 Analyzing custom/unique code in codebase...\n")

    # Load duplicate analysis
    json_files = list(Path(ANALYSIS_DIR).glob("function_analysis_*.json"))
    if not json_files:
        print(
            "❌ No analysis found. Please run compare_content_and_functions.py first."
        )
        return

    latest_json = max(json_files, key=lambda p: p.stat().st_mtime)
    print(f"📄 Loading analysis from: {latest_json}")

    with open(latest_json, "r") as f:
        analysis = json.load(f)

    duplicate_groups = analysis.get("duplicate_functions_by_hash", {})
    duplicate_hashes = set(duplicate_groups.keys())
    print(f"   Found {len(duplicate_hashes)} duplicate hash groups\n")

    # Analyze all Python files
    print("📊 Scanning Python files for unique functions...\n")

    python_files = list(Path(TARGET_DIR).rglob("*.py"))
    exclude_dirs = {"__pycache__", ".git", "venv", "env", ".venv", "node_modules"}
    python_files = [
        f for f in python_files if not any(ex in str(f) for ex in exclude_dirs)
    ]

    print(f"   Processing {len(python_files)} files...\n")

    all_functions = []
    unique_functions = []
    hash_to_count = defaultdict(int)

    for i, filepath in enumerate(python_files, 1):
        if i % 500 == 0:
            print(f"   Processed {i}/{len(python_files)} files...")

        result = extract_functions_from_file(filepath)

        for func_info in result["functions"]:
            func_info["file"] = result["file"]
            all_functions.append(func_info)

            hash_val = func_info.get("hash")
            if hash_val:
                hash_to_count[hash_val] += 1

                # Check if this is a unique function (not in duplicate groups)
                if hash_val not in duplicate_hashes:
                    unique_functions.append(func_info)

    print("\n✅ Analysis complete!")
    print(f"   Total functions: {len(all_functions)}")
    print(
        f"   Duplicate functions: {len([f for f in all_functions if f.get('hash') in duplicate_hashes])}"
    )
    print(f"   Unique/custom functions: {len(unique_functions)}")

    # Generate report
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Organize unique functions by file
    functions_by_file = defaultdict(list)
    for func in unique_functions:
        functions_by_file[func["file"]].append(func)

    # Generate text report
    report_path = os.path.join(OUTPUT_DIR, f"custom_code_analysis_{timestamp}.txt")

    with open(report_path, "w") as f:
        f.write("=" * 80 + "\n")
        f.write("CUSTOM/UNIQUE CODE ANALYSIS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write("SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total functions analyzed: {len(all_functions)}\n")
        f.write(
            f"Duplicate functions: {len([f for f in all_functions if f.get('hash') in duplicate_hashes])}\n"
        )
        f.write(f"Unique/custom functions: {len(unique_functions)}\n")
        f.write(f"Files with unique functions: {len(functions_by_file)}\n\n")

        f.write("=" * 80 + "\n")
        f.write("FILES WITH CUSTOM/UNIQUE FUNCTIONS\n")
        f.write("=" * 80 + "\n\n")

        # Sort by number of unique functions
        sorted_files = sorted(
            functions_by_file.items(), key=lambda x: len(x[1]), reverse=True
        )

        for filepath, funcs in sorted_files[:100]:  # Top 100 files
            f.write(f"\n{filepath}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Unique functions: {len(funcs)}\n\n")

            for func in funcs[:20]:  # First 20 functions per file
                f.write(f"  • {func['signature']} (line {func['line']})\n")
                if func.get("source"):
                    source_preview = func["source"][:200].replace("\n", " ")
                    f.write(f"    Preview: {source_preview}...\n")
                f.write("\n")

    # Generate JSON report
    json_path = os.path.join(OUTPUT_DIR, f"custom_code_analysis_{timestamp}.json")

    json_report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_functions": len(all_functions),
            "duplicate_functions": len(
                [f for f in all_functions if f.get("hash") in duplicate_hashes]
            ),
            "unique_functions": len(unique_functions),
            "files_with_unique_functions": len(functions_by_file),
        },
        "files_with_unique_functions": [
            {
                "file": filepath,
                "unique_function_count": len(funcs),
                "functions": [
                    {
                        "signature": func["signature"],
                        "line": func["line"],
                        "class": func.get("class"),
                        "source_length": len(func.get("source", "")),
                    }
                    for func in funcs
                ],
            }
            for filepath, funcs in sorted_files[:200]  # Top 200 files
        ],
    }

    with open(json_path, "w") as f:
        json.dump(json_report, f, indent=2)

    print("\n📄 Reports generated:")
    print(f"   Text report: {report_path}")
    print(f"   JSON report: {json_path}")

    # Print top files with unique code
    print("\n📊 Top 10 files with most unique functions:")
    for filepath, funcs in sorted_files[:10]:
        rel_path = os.path.relpath(filepath, TARGET_DIR)
        print(f"   {rel_path}: {len(funcs)} unique functions")

    return report_path


if __name__ == "__main__":
    try:
        analyze_custom_code()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()

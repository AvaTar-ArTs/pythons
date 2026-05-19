#!/usr/bin/env python3
"""
Index Content and Functions from ~ (Home Directory)
Scans all files in home directory, extracts functions, classes, and content
for transcription and analysis purposes.
"""

import os
import csv
import json
import ast
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Output directories
OUTPUT_DIRS = {
    "index": Path("/Users/steven/pythons/content_index"),
    "transcripts": Path("/Users/steven/pythons/python_transcripts"),
    "analysis": Path("/Users/steven/pythons/python_analysis"),
}

# File extensions to process
CODE_EXTENSIONS = {
    ".py",
    ".pyw",  # Python
    ".js",
    ".jsx",
    ".ts",
    ".tsx",  # JavaScript/TypeScript
    ".java",  # Java
    ".cpp",
    ".c",
    ".h",
    ".hpp",  # C/C++
    ".go",  # Go
    ".rs",  # Rust
    ".rb",  # Ruby
    ".php",  # PHP
    ".swift",  # Swift
    ".kt",  # Kotlin
}

# Directories to skip
SKIP_DIRS = {
    ".git",
    ".svn",
    ".hg",  # Version control
    "node_modules",
    "__pycache__",
    ".pytest_cache",  # Dependencies/cache
    ".venv",
    "venv",
    "env",
    ".env",  # Virtual environments
    "Library",
    "Applications",
    "System",  # System directories
    ".Trash",
    ".cache",
    ".local/share",  # Cache/trash
    "Downloads",  # Optional: skip downloads if too large
}


def should_skip_path(path):
    """Check if path should be skipped."""
    path_str = str(path)
    parts = Path(path).parts

    # Skip hidden files/dirs (except .env files we might want)
    if any(part.startswith(".") and part not in [".env", ".env.d"] for part in parts):
        if ".git" not in path_str:  # Allow .git for some analysis
            return True

    # Skip specific directories
    for skip_dir in SKIP_DIRS:
        if skip_dir in parts:
            return True

    return False


def extract_python_functions(file_path):
    """Extract functions and classes from Python file using AST."""
    functions = []
    classes = []
    imports = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        try:
            tree = ast.parse(content, filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Get function signature
                    args = [arg.arg for arg in node.args.args]
                    decorators = [
                        ast.unparse(d)
                        if hasattr(ast, "unparse")
                        else d.id
                        if isinstance(d, ast.Name)
                        else "decorator"
                        for d in node.decorator_list
                    ]

                    # Get docstring
                    docstring = ast.get_docstring(node) or ""

                    # Get function body (first few lines)
                    body_lines = []
                    if node.body:
                        for stmt in node.body[:3]:  # First 3 statements
                            try:
                                if hasattr(ast, "unparse"):
                                    body_lines.append(ast.unparse(stmt))
                                else:
                                    body_lines.append(ast.dump(stmt))
                            except:
                                pass

                    functions.append(
                        {
                            "name": node.name,
                            "args": args,
                            "decorators": decorators,
                            "docstring": docstring[:200]
                            if docstring
                            else "",  # Limit length
                            "body_preview": " ".join(body_lines)[:300],  # Preview
                            "line_start": node.lineno if hasattr(node, "lineno") else 0,
                        }
                    )

                elif isinstance(node, ast.ClassDef):
                    # Get class methods
                    methods = [
                        n.name for n in node.body if isinstance(n, ast.FunctionDef)
                    ]
                    docstring = ast.get_docstring(node) or ""

                    classes.append(
                        {
                            "name": node.name,
                            "methods": methods,
                            "docstring": docstring[:200] if docstring else "",
                            "line_start": node.lineno if hasattr(node, "lineno") else 0,
                        }
                    )

                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    try:
                        if isinstance(node, ast.Import):
                            imports.extend([alias.name for alias in node.names])
                        else:
                            module = node.module or ""
                            imports.append(
                                f"{module}.{', '.join([a.name for a in node.names])}"
                            )
                    except:
                        pass

        except SyntaxError:
            # File has syntax errors, try regex extraction
            return extract_functions_regex(content, file_path)

    except Exception:
        return [], [], []

    return functions, classes, imports


def extract_functions_regex(content, file_path):
    """Fallback: Extract functions using regex when AST fails."""
    functions = []
    classes = []
    imports = []

    # Extract function definitions
    func_pattern = r"def\s+(\w+)\s*\([^)]*\)\s*:"
    for match in re.finditer(func_pattern, content):
        func_name = match.group(1)
        start_pos = match.start()
        line_num = content[:start_pos].count("\n") + 1

        # Try to get docstring
        docstring = ""
        doc_match = re.search(
            r'\"\'".*?'\"\'", content[start_pos : start_pos + 500], re.DOTALL
        )
        if doc_match:
            docstring = docmatch.group(0)[:200]

        functions.append(
            {
                "name": func_name,
                "args": [],
                "decorators": [],
                "docstring": docstring,
                "body_preview": content[start_pos : start_pos + 300],
                "line_start": line_num,
            }
        )

    # Extract class definitions
    class_pattern = r"class\s+(\w+)"
    for match in re.finditer(class_pattern, content):
        class_name = match.group(1)
        start_pos = match.start()
        line_num = content[:start_pos].count("\n") + 1

        classes.append(
            {
                "name": class_name,
                "methods": [],
                "docstring": "",
                "line_start": line_num,
            }
        )

    # Extract imports
    import_pattern = r"^(?:from\s+(\S+)\s+)?import\s+(.+)$"
    for match in re.finditer(import_pattern, content, re.MULTILINE):
        if match.group(1):
            imports.append(f"{match.group(1)}.{match.group(2)}")
        else:
            imports.append(match.group(2))

    return functions, classes, imports


def extract_other_language_functions(file_path):
    """Extract functions from other languages (JS, Java, etc.)."""
    functions = []
    classes = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        ext = file_path.suffix.lower()

        if ext in {".js", ".jsx", ".ts", ".tsx"}:
            # JavaScript/TypeScript function patterns
            patterns = [
                r"function\s+(\w+)\s*\([^)]*\)",
                r"const\s+(\w+)\s*=\s*\([^)]*\)\s*=>",
                r"(\w+)\s*:\s*\([^)]*\)\s*=>",
            ]
            for pattern in patterns:
                for match in re.finditer(pattern, content):
                    func_name = match.group(1)
                    start_pos = match.start()
                    line_num = content[:start_pos].count("\n") + 1

                    functions.append(
                        {
                            "name": func_name,
                            "args": [],
                            "decorators": [],
                            "docstring": "",
                            "body_preview": content[start_pos : start_pos + 300],
                            "line_start": line_num,
                        }
                    )

        elif ext in {".java"}:
            # Java method patterns
            pattern = (
                r"(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\([^)]*\)"
            )
            for match in re.finditer(pattern, content):
                func_name = match.group(1)
                start_pos = match.start()
                line_num = content[:start_pos].count("\n") + 1

                functions.append(
                    {
                        "name": func_name,
                        "args": [],
                        "decorators": [],
                        "docstring": "",
                        "body_preview": content[start_pos : start_pos + 300],
                        "line_start": line_num,
                    }
                )

        # Extract class definitions for various languages
        class_patterns = {
            ".js": r"class\s+(\w+)",
            ".jsx": r"class\s+(\w+)",
            ".ts": r"class\s+(\w+)",
            ".tsx": r"class\s+(\w+)",
            ".java": r"class\s+(\w+)",
            ".cpp": r"class\s+(\w+)",
            ".c": r"struct\s+(\w+)",
        }

        if ext in class_patterns:
            pattern = class_patterns[ext]
            for match in re.finditer(pattern, content):
                class_name = match.group(1)
                start_pos = match.start()
                line_num = content[:start_pos].count("\n") + 1

                classes.append(
                    {
                        "name": class_name,
                        "methods": [],
                        "docstring": "",
                        "line_start": line_num,
                    }
                )

    except Exception:
        pass

    return functions, classes


def get_file_content_summary(file_path, max_lines=50):
    """Get a summary of file content (first N lines)."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()[:max_lines]
            return "".join(lines)
    except:
        return ""


def scan_directory(directory):
    """Recursively scan directory for code files."""
    code_files = []

    print(f"Scanning {directory}...")

    try:
        for root, dirs, files in os.walk(directory):
            # Filter out directories to skip
            dirs[:] = [d for d in dirs if not should_skip_path(Path(root) / d)]

            for file in files:
                file_path = Path(root) / file

                # Skip if path should be skipped
                if should_skip_path(file_path):
                    continue

                # Check if it's a code file
                if file_path.suffix.lower() in CODE_EXTENSIONS:
                    try:
                        if file_path.exists() and file_path.is_file():
                            code_files.append(file_path)
                    except (OSError, PermissionError):
                        continue

    except (OSError, PermissionError) as e:
        print(f"Error scanning {directory}: {e}")

    return code_files


def main():
    print("=" * 80)
    print("INDEXING CONTENT AND FUNCTIONS FROM ~ (HOME DIRECTORY)")
    print("=" * 80)
    print()

    home_dir = Path.home()
    print(f"Scanning home directory: {home_dir}")
    print("This may take a while...\n")

    # Scan for code files
    code_files = scan_directory(home_dir)

    print(f"Found {len(code_files)} code files\n")

    if len(code_files) == 0:
        print("No code files found!")
        return

    # Create output directories
    for dir_path in OUTPUT_DIRS.values():
        dir_path.mkdir(parents=True, exist_ok=True)

    # Process files
    print("Extracting functions and content...")
    all_functions = []
    all_classes = []
    file_index = []

    for i, file_path in enumerate(code_files, 1):
        if i % 50 == 0:
            print(f"  Processed {i}/{len(code_files)} files...")

        try:
            # Get file info
            size_kb = file_path.stat().st_size / 1024
            line_count = sum(1 for _ in open(file_path, "rb"))

            # Extract functions/classes based on file type
            if file_path.suffix.lower() == ".py":
                functions, classes, imports = extract_python_functions(file_path)
            else:
                functions, classes = extract_other_language_functions(file_path)
                imports = []

            # Add file context to functions
            for func in functions:
                func["file_path"] = str(file_path)
                func["file_name"] = file_path.name
                func["relative_path"] = (
                    str(file_path.relative_to(home_dir))
                    if file_path.is_relative_to(home_dir)
                    else str(file_path)
                )
                all_functions.append(func)

            for cls in classes:
                cls["file_path"] = str(file_path)
                cls["file_name"] = file_path.name
                cls["relative_path"] = (
                    str(file_path.relative_to(home_dir))
                    if file_path.is_relative_to(home_dir)
                    else str(file_path)
                )
                all_classes.append(cls)

            # Get content summary
            content_summary = get_file_content_summary(file_path)

            file_index.append(
                {
                    "file_path": str(file_path),
                    "file_name": file_path.name,
                    "relative_path": str(file_path.relative_to(home_dir))
                    if file_path.is_relative_to(home_dir)
                    else str(file_path),
                    "directory": str(file_path.parent),
                    "size_kb": round(size_kb, 2),
                    "line_count": line_count,
                    "function_count": len(functions),
                    "class_count": len(classes),
                    "import_count": len(imports),
                    "content_preview": content_summary[:500],  # First 500 chars
                    "language": file_path.suffix.lower(),
                }
            )

        except Exception as e:
            print(f"  Error processing {file_path}: {e}")
            continue

    print("Extraction complete!\n")

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save function index
    if all_functions:
        func_csv = OUTPUT_DIRS["index"] / f"functions_index_{timestamp}.csv"
        with open(func_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "name",
                    "file_path",
                    "file_name",
                    "relative_path",
                    "args",
                    "decorators",
                    "docstring",
                    "body_preview",
                    "line_start",
                ],
            )
            writer.writeheader()
            for func in all_functions:
                # Convert lists to strings for CSV
                func_copy = func.copy()
                func_copy["args"] = ", ".join(func["args"]) if func["args"] else ""
                func_copy["decorators"] = (
                    ", ".join(func["decorators"]) if func["decorators"] else ""
                )
                writer.writerow(func_copy)

        print(f"Functions index: {func_csv} ({len(all_functions)} functions)")

    # Save class index
    if all_classes:
        class_csv = OUTPUT_DIRS["index"] / f"classes_index_{timestamp}.csv"
        with open(class_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "name",
                    "file_path",
                    "file_name",
                    "relative_path",
                    "methods",
                    "docstring",
                    "line_start",
                ],
            )
            writer.writeheader()
            for cls in all_classes:
                cls_copy = cls.copy()
                cls_copy["methods"] = (
                    ", ".join(cls["methods"]) if cls["methods"] else ""
                )
                writer.writerow(cls_copy)

        print(f"Classes index: {class_csv} ({len(all_classes)} classes)")

    # Save file index
    file_csv = OUTPUT_DIRS["index"] / f"files_index_{timestamp}.csv"
    with open(file_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "file_path",
                "file_name",
                "relative_path",
                "directory",
                "size_kb",
                "line_count",
                "function_count",
                "class_count",
                "import_count",
                "language",
                "content_preview",
            ],
        )
        writer.writeheader()
        writer.writerows(file_index)

    print(f"Files index: {file_csv} ({len(file_index)} files)")

    # Save JSON indices
    func_json = OUTPUT_DIRS["index"] / f"functions_index_{timestamp}.json"
    with open(func_json, "w", encoding="utf-8") as f:
        json.dump(all_functions, f, indent=2)

    class_json = OUTPUT_DIRS["index"] / f"classes_index_{timestamp}.json"
    with open(class_json, "w", encoding="utf-8") as f:
        json.dump(all_classes, f, indent=2)

    file_json = OUTPUT_DIRS["index"] / f"files_index_{timestamp}.json"
    with open(file_json, "w", encoding="utf-8") as f:
        json.dump(file_index, f, indent=2)

    print("\nJSON indices saved")

    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files scanned: {len(file_index)}")
    print(f"Total functions found: {len(all_functions)}")
    print(f"Total classes found: {len(all_classes)}")

    # By language
    lang_counts = defaultdict(int)
    for file_info in file_index:
        lang_counts[file_info["language"]] += 1

    print("\nFiles by language:")
    for lang, count in sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[
        :10
    ]:
        print(f"  {lang}: {count} files")

    # Top files by function count
    top_files = sorted(file_index, key=lambda x: x["function_count"], reverse=True)[:10]
    print("\nTop files by function count:")
    for file_info in top_files:
        print(
            f"  {file_info['file_name']}: {file_info['function_count']} functions, {file_info['line_count']} lines"
        )

    print(f"\nAll indices saved to: {OUTPUT_DIRS['index']}")


if __name__ == "__main__":
    main()

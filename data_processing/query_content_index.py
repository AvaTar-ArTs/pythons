#!/usr/bin/env python3
"""
Query and Search Content Index
Search functions, classes, and files from the indexed content.
"""

import json
import csv
import argparse
import re
from pathlib import Path
from collections import defaultdict

# Default index directory
INDEX_DIR = Path("/Users/steven/pythons/content_index")


def load_json_index(index_path):
    """Load JSON index file."""
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {index_path}: {e}")
        return []


def load_csv_index(index_path):
    """Load CSV index file."""
    try:
        data = []
        with open(index_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        print(f"Error loading {index_path}: {e}")
        return []


def find_latest_index(index_type, index_dir):
    """Find the most recent index file of a given type."""
    pattern = f"{index_type}_index_*.json"
    files = list(index_dir.glob(pattern))
    if not files:
        # Try CSV
        pattern = f"{index_type}_index_*.csv"
        files = list(index_dir.glob(pattern))

    if files:
        # Sort by modification time, get most recent
        return max(files, key=lambda p: p.stat().st_mtime)
    return None


def search_functions(query, functions, search_type="name"):
    """Search functions by name, file, or content."""
    results = []
    query_lower = query.lower()

    for func in functions:
        match = False

        if search_type == "name":
            if query_lower in func.get("name", "").lower():
                match = True
        elif search_type == "file":
            file_path = func.get("file_path", "") + func.get("file_name", "")
            if query_lower in file_path.lower():
                match = True
        elif search_type == "content":
            # Search in docstring, body preview, args
            search_text = " ".join(
                [
                    func.get("docstring", ""),
                    func.get("body_preview", ""),
                    ", ".join(func.get("args", [])),
                ]
            ).lower()
            if query_lower in search_text:
                match = True
        elif search_type == "regex":
            try:
                pattern = re.compile(query, re.IGNORECASE)
                if (
                    pattern.search(func.get("name", ""))
                    or pattern.search(func.get("docstring", ""))
                    or pattern.search(func.get("body_preview", ""))
                ):
                    match = True
            except re.error:
                return []

        if match:
            results.append(func)

    return results


def search_classes(query, classes, search_type="name"):
    """Search classes by name, file, or methods."""
    results = []
    query_lower = query.lower()

    for cls in classes:
        match = False

        if search_type == "name":
            if query_lower in cls.get("name", "").lower():
                match = True
        elif search_type == "file":
            file_path = cls.get("file_path", "") + cls.get("file_name", "")
            if query_lower in file_path.lower():
                match = True
        elif search_type == "methods":
            methods = ", ".join(cls.get("methods", []))
            if query_lower in methods.lower():
                match = True
        elif search_type == "content":
            search_text = " ".join(
                [
                    cls.get("name", ""),
                    cls.get("docstring", ""),
                    ", ".join(cls.get("methods", [])),
                ]
            ).lower()
            if query_lower in search_text:
                match = True
        elif search_type == "regex":
            try:
                pattern = re.compile(query, re.IGNORECASE)
                if pattern.search(cls.get("name", "")) or pattern.search(
                    cls.get("docstring", "")
                ):
                    match = True
            except re.error:
                return []

        if match:
            results.append(cls)

    return results


def search_files(query, files, search_type="name"):
    """Search files by name, path, or content."""
    results = []
    query_lower = query.lower()

    for file_info in files:
        match = False

        if search_type == "name":
            if query_lower in file_info.get("file_name", "").lower():
                match = True
        elif search_type == "path":
            path = file_info.get("file_path", "") + file_info.get("relative_path", "")
            if query_lower in path.lower():
                match = True
        elif search_type == "content":
            content = file_info.get("content_preview", "")
            if query_lower in content.lower():
                match = True
        elif search_type == "language":
            if query_lower == file_info.get("language", "").lower():
                match = True
        elif search_type == "regex":
            try:
                pattern = re.compile(query, re.IGNORECASE)
                if pattern.search(file_info.get("file_name", "")) or pattern.search(
                    file_info.get("content_preview", "")
                ):
                    match = True
            except re.error:
                return []

        if match:
            results.append(file_info)

    return results


def filter_results(results, filters):
    """Apply filters to results."""
    filtered = results

    if "min_lines" in filters:
        filtered = [
            r
            for r in filtered
            if int(r.get("line_count", 0) or 0) >= filters["min_lines"]
        ]

    if "max_lines" in filters:
        filtered = [
            r
            for r in filtered
            if int(r.get("line_count", 0) or 0) <= filters["max_lines"]
        ]

    if "min_size_kb" in filters:
        filtered = [
            r
            for r in filtered
            if float(r.get("size_kb", 0) or 0) >= filters["min_size_kb"]
        ]

    if "max_size_kb" in filters:
        filtered = [
            r
            for r in filtered
            if float(r.get("size_kb", 0) or 0) <= filters["max_size_kb"]
        ]

    if "language" in filters:
        filtered = [
            r
            for r in filtered
            if r.get("language", "").lower() == filters["language"].lower()
        ]

    if "min_functions" in filters:
        filtered = [
            r
            for r in filtered
            if int(r.get("function_count", 0) or 0) >= filters["min_functions"]
        ]

    return filtered


def print_function_results(results, limit=None, detailed=False):
    """Print function search results."""
    if limit:
        results = results[:limit]

    print(f"\nFound {len(results)} functions:\n")

    for i, func in enumerate(results, 1):
        print(f"{i}. {func.get('name', 'unknown')}")
        print(f"   File: {func.get('relative_path', func.get('file_name', 'unknown'))}")

        if func.get("args"):
            args_str = (
                ", ".join(func["args"])
                if isinstance(func["args"], list)
                else func["args"]
            )
            print(f"   Args: {args_str}")

        if func.get("docstring"):
            doc = (
                func["docstring"][:150] + "..."
                if len(func["docstring"]) > 150
                else func["docstring"]
            )
            print(f"   Doc: {doc}")

        if detailed and func.get("body_preview"):
            body = (
                func["body_preview"][:200] + "..."
                if len(func["body_preview"]) > 200
                else func["body_preview"]
            )
            print(f"   Preview: {body}")

        if func.get("line_start"):
            print(f"   Line: {func['line_start']}")

        print()


def print_class_results(results, limit=None, detailed=False):
    """Print class search results."""
    if limit:
        results = results[:limit]

    print(f"\nFound {len(results)} classes:\n")

    for i, cls in enumerate(results, 1):
        print(f"{i}. {cls.get('name', 'unknown')}")
        print(f"   File: {cls.get('relative_path', cls.get('file_name', 'unknown'))}")

        if cls.get("methods"):
            methods_str = (
                ", ".join(cls["methods"])
                if isinstance(cls["methods"], list)
                else cls["methods"]
            )
            print(f"   Methods: {methods_str}")

        if cls.get("docstring"):
            doc = (
                cls["docstring"][:150] + "..."
                if len(cls["docstring"]) > 150
                else cls["docstring"]
            )
            print(f"   Doc: {doc}")

        if cls.get("line_start"):
            print(f"   Line: {cls['line_start']}")

        print()


def print_file_results(results, limit=None, detailed=False):
    """Print file search results."""
    if limit:
        results = results[:limit]

    print(f"\nFound {len(results)} files:\n")

    for i, file_info in enumerate(results, 1):
        print(f"{i}. {file_info.get('file_name', 'unknown')}")
        print(
            f"   Path: {file_info.get('relative_path', file_info.get('file_path', 'unknown'))}"
        )
        print(f"   Language: {file_info.get('language', 'unknown')}")
        print(f"   Size: {file_info.get('size_kb', 0)} KB")
        print(f"   Lines: {file_info.get('line_count', 0)}")
        print(
            f"   Functions: {file_info.get('function_count', 0)}, Classes: {file_info.get('class_count', 0)}"
        )

        if detailed and file_info.get("content_preview"):
            content = (
                file_info["content_preview"][:200] + "..."
                if len(file_info["content_preview"]) > 200
                else file_info["content_preview"]
            )
            print(f"   Preview: {content}")

        print()


def get_statistics(functions, classes, files):
    """Get statistics about the indexed content."""
    stats = {
        "total_functions": len(functions),
        "total_classes": len(classes),
        "total_files": len(files),
    }

    # Language distribution
    lang_counts = defaultdict(int)
    for file_info in files:
        lang = file_info.get("language", "unknown")
        lang_counts[lang] += 1
    stats["languages"] = dict(lang_counts)

    # Files by function count
    files_by_funcs = sorted(
        files, key=lambda x: int(x.get("function_count", 0) or 0), reverse=True
    )
    stats["top_files_by_functions"] = [
        {
            "file": f.get("file_name"),
            "functions": f.get("function_count"),
            "lines": f.get("line_count"),
        }
        for f in files_by_funcs[:10]
    ]

    # Most common function names
    func_names = defaultdict(int)
    for func in functions:
        func_names[func.get("name", "")] += 1
    stats["common_function_names"] = dict(
        sorted(func_names.items(), key=lambda x: x[1], reverse=True)[:20]
    )

    return stats


def main():
    parser = argparse.ArgumentParser(description="Query and search content index")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument(
        "--type",
        choices=["function", "class", "file", "all"],
        default="all",
        help="Type of search (default: all)",
    )
    parser.add_argument(
        "--search-in",
        choices=["name", "file", "content", "methods", "path", "language", "regex"],
        default="name",
        help="What to search in (default: name)",
    )
    parser.add_argument(
        "--index-dir",
        default=str(INDEX_DIR),
        help="Index directory (default: /Users/steven/pythons/content_index)",
    )
    parser.add_argument("--limit", type=int, help="Limit number of results")
    parser.add_argument("--detailed", action="store_true", help="Show detailed results")
    parser.add_argument(
        "--stats", action="store_true", help="Show statistics instead of searching"
    )
    parser.add_argument("--min-lines", type=int, help="Filter: minimum lines")
    parser.add_argument("--max-lines", type=int, help="Filter: maximum lines")
    parser.add_argument("--min-size-kb", type=float, help="Filter: minimum size in KB")
    parser.add_argument("--max-size-kb", type=float, help="Filter: maximum size in KB")
    parser.add_argument("--language", help="Filter: language (e.g., .py, .js)")
    parser.add_argument(
        "--min-functions", type=int, help="Filter: minimum function count"
    )
    parser.add_argument(
        "--output",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument("--output-file", help="Output file path")

    args = parser.parse_args()

    # Use the index directory from args
    index_dir = Path(args.index_dir)

    if not index_dir.exists():
        print(f"Error: Index directory not found: {index_dir}")
        return

    # Load indices
    print("Loading indices...")
    func_index = find_latest_index("functions", index_dir)
    class_index = find_latest_index("classes", index_dir)
    file_index = find_latest_index("files", index_dir)

    functions = []
    classes = []
    files = []

    if func_index:
        print(f"Loading functions from {func_index.name}...")
        if func_index.suffix == ".json":
            functions = load_json_index(func_index)
        else:
            functions = load_csv_index(func_index)

    if class_index:
        print(f"Loading classes from {class_index.name}...")
        if class_index.suffix == ".json":
            classes = load_json_index(class_index)
        else:
            classes = load_csv_index(class_index)

    if file_index:
        print(f"Loading files from {file_index.name}...")
        if file_index.suffix == ".json":
            files = load_json_index(file_index)
        else:
            files = load_csv_index(file_index)

    print(
        f"Loaded: {len(functions)} functions, {len(classes)} classes, {len(files)} files\n"
    )

    # Show statistics
    if args.stats:
        stats = get_statistics(functions, classes, files)
        print("=" * 80)
        print("INDEX STATISTICS")
        print("=" * 80)
        print(f"Total functions: {stats['total_functions']}")
        print(f"Total classes: {stats['total_classes']}")
        print(f"Total files: {stats['total_files']}")
        print("\nFiles by language:")
        for lang, count in sorted(
            stats["languages"].items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {lang}: {count}")
        print("\nTop files by function count:")
        for f in stats["top_files_by_functions"]:
            print(f"  {f['file']}: {f['functions']} functions, {f['lines']} lines")
        print("\nMost common function names:")
        for name, count in list(stats["common_function_names"].items())[:10]:
            print(f"  {name}: {count} occurrences")
        return

    # Search
    if not args.query:
        print(
            "No query provided. Use --stats to see statistics or provide a search query."
        )
        return

    filters = {}
    if args.min_lines:
        filters["min_lines"] = args.min_lines
    if args.max_lines:
        filters["max_lines"] = args.max_lines
    if args.min_size_kb:
        filters["min_size_kb"] = args.min_size_kb
    if args.max_size_kb:
        filters["max_size_kb"] = args.max_size_kb
    if args.language:
        filters["language"] = args.language
    if args.min_functions:
        filters["min_functions"] = args.min_functions

    results = {}

    if args.type in ["function", "all"]:
        func_results = search_functions(args.query, functions, args.search_in)
        func_results = filter_results(func_results, filters)
        results["functions"] = func_results

    if args.type in ["class", "all"]:
        class_results = search_classes(args.query, classes, args.search_in)
        class_results = filter_results(class_results, filters)
        results["classes"] = class_results

    if args.type in ["file", "all"]:
        file_results = search_files(args.query, files, args.search_in)
        file_results = filter_results(file_results, filters)
        results["files"] = file_results

    # Output results
    if args.output == "json":
        output = json.dumps(results, indent=2)
        if args.output_file:
            with open(args.output_file, "w") as f:
                f.write(output)
        else:
            print(output)
    elif args.output == "csv":
        # Combine all results into CSV
        all_results = []
        for result_type, result_list in results.items():
            for item in result_list:
                item["result_type"] = result_type
                all_results.append(item)

        if all_results and args.output_file:
            with open(args.output_file, "w", newline="", encoding="utf-8") as f:
                if all_results:
                    writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
                    writer.writeheader()
                    writer.writerows(all_results)
            print(f"Results saved to {args.output_file}")
        else:
            print("No results to save")
    else:
        # Text output
        if "functions" in results:
            print_function_results(results["functions"], args.limit, args.detailed)
        if "classes" in results:
            print_class_results(results["classes"], args.limit, args.detailed)
        if "files" in results:
            print_file_results(results["files"], args.limit, args.detailed)


if __name__ == "__main__":
    main()

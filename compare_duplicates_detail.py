#!/usr/bin/env python3
"""
Detailed comparison of duplicate functions.
Shows code differences and similarities between duplicate functions.
"""

import os
import ast
import hashlib
import json
from pathlib import Path
from collections import defaultdict
from difflib import unified_diff, SequenceMatcher
from datetime import datetime

TARGET_DIR = "/Users/steven/pythons"
ANALYSIS_DIR = "/Users/steven/pythons/function_analysis"
OUTPUT_DIR = "/Users/steven/pythons/duplicate_comparison"

def get_function_source(filepath, start_line, max_lines=100):
    """Extract function source code from file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        # Get function code (start_line is 1-indexed in AST)
        start_idx = max(0, start_line - 1)
        end_idx = min(len(lines), start_idx + max_lines)

        function_lines = lines[start_idx:end_idx]

        # Try to find the end of the function (indentation-based)
        if start_idx < len(lines):
            base_indent = len(lines[start_idx]) - len(lines[start_idx].lstrip())
            for i in range(start_idx + 1, len(lines)):
                line = lines[i]
                if line.strip() and not line.startswith(' ' * (base_indent + 1)) and not line.startswith('\t' * (base_indent // 4 + 1)):
                    # Check if it's a decorator or continuation
                    if not (line.strip().startswith('@') or line.strip().startswith('#')):
                        end_idx = i
                        break

        return ''.join(lines[start_idx:end_idx])
    except Exception as e:
        return f"Error reading file: {e}"

def get_function_hash(source_code):
    """Get hash of function source code (normalized)."""
    normalized = source_code.strip().replace('\r\n', '\n').replace('\r', '\n')
    # Remove trailing whitespace from each line
    normalized = '\n'.join(line.rstrip() for line in normalized.split('\n'))
    return hashlib.md5(normalized.encode()).hexdigest()

def compare_functions(func1_source, func2_source):
    """Compare two function sources and return similarity metrics."""
    similarity = SequenceMatcher(None, func1_source, func2_source).ratio()

    # Generate unified diff
    lines1 = func1_source.splitlines(keepends=True)
    lines2 = func2_source.splitlines(keepends=True)
    diff = list(unified_diff(
        lines1, lines2,
        fromfile='Function 1',
        tofile='Function 2',
        lineterm='',
        n=3
    ))

    return {
        'similarity': similarity,
        'diff': diff,
        'lines1': len(lines1),
        'lines2': len(lines2)
    }

class FunctionExtractor(ast.NodeVisitor):
    """Extract function definitions from Python AST."""

    def __init__(self):
        self.functions = []
        self.current_class = None

    def visit_FunctionDef(self, node):
        func_info = {
            'name': node.name,
            'line': node.lineno,
            'end_line': getattr(node, 'end_lineno', node.lineno + 50),
            'args': [arg.arg for arg in node.args.args],
            'class': self.current_class,
        }

        signature = f"{node.name}({', '.join(func_info['args'])})"
        if self.current_class:
            signature = f"{self.current_class}.{signature}"
        func_info['signature'] = signature

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
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            source = f.read()

        try:
            tree = ast.parse(source, filename=str(filepath))
        except SyntaxError:
            return {'file': str(filepath), 'functions': [], 'error': 'Syntax error'}

        extractor = FunctionExtractor()
        extractor.visit(tree)

        # Get source code for each function
        for func_info in extractor.functions:
            func_source = get_function_source(
                filepath,
                func_info['line'],
                func_info['end_line'] - func_info['line'] + 10
            )
            func_info['source'] = func_source
            func_info['hash'] = get_function_hash(func_source)

        return {
            'file': str(filepath),
            'functions': extractor.functions
        }
    except Exception as e:
        return {'file': str(filepath), 'functions': [], 'error': str(e)}

def analyze_and_compare():
    """Analyze all files and compare duplicates."""
    print("🔍 Analyzing duplicates for detailed comparison...\n")

    # Load existing analysis if available
    json_files = list(Path(ANALYSIS_DIR).glob("function_analysis_*.json"))
    if json_files:
        latest_json = max(json_files, key=lambda p: p.stat().st_mtime)
        print(f"📄 Loading analysis from: {latest_json}")
        with open(latest_json, 'r') as f:
            analysis = json.load(f)

        duplicate_groups = analysis.get('duplicate_functions_by_hash', {})
        print(f"   Found {len(duplicate_groups)} duplicate groups\n")
    else:
        print("❌ No existing analysis found. Please run compare_content_and_functions.py first.")
        return

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Process top duplicate groups
    print("📊 Comparing duplicate functions...\n")

    comparison_results = []
    top_duplicates = list(duplicate_groups.items())[:50]  # Top 50 groups

    for hash_val, func_list in top_duplicates:
        if len(func_list) < 2:
            continue

        # Get source code for all functions in this group
        func_details = []
        for func_info in func_list:
            filepath = func_info['file']
            line = func_info['line']

            result = extract_functions_from_file(filepath)

            # Find the specific function
            for f in result['functions']:
                if f['line'] == line and f['signature'] == func_info['signature']:
                    func_details.append({
                        'file': filepath,
                        'line': line,
                        'signature': func_info['signature'],
                        'source': f.get('source', ''),
                        'hash': f.get('hash', '')
                    })
                    break

        if len(func_details) >= 2:
            # Compare first two functions
            if len(func_details) >= 2 and func_details[0]['source'] and func_details[1]['source']:
                comparison = compare_functions(
                    func_details[0]['source'],
                    func_details[1]['source']
                )

                comparison_results.append({
                    'hash': hash_val,
                    'signature': func_details[0]['signature'],
                    'functions': func_details,
                    'comparison': comparison
                })

    # Generate detailed comparison report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = os.path.join(OUTPUT_DIR, f'duplicate_comparison_{timestamp}.txt')

    with open(report_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("DETAILED DUPLICATE FUNCTION COMPARISON\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write(f"Total duplicate groups analyzed: {len(comparison_results)}\n\n")

        for i, comp in enumerate(comparison_results, 1):
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"DUPLICATE GROUP {i}: {comp['signature']}\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Hash: {comp['hash']}\n")
            f.write(f"Similarity: {comp['comparison']['similarity']:.2%}\n")
            f.write(f"Functions found: {len(comp['functions'])}\n\n")

            # List all occurrences
            f.write("Occurrences:\n")
            f.write("-" * 80 + "\n")
            for j, func_detail in enumerate(comp['functions'], 1):
                f.write(f"\n{j}. {func_detail['file']}\n")
                f.write(f"   Line: {func_detail['line']}\n")
                f.write(f"   Signature: {func_detail['signature']}\n")

            # Show comparison between first two
            if len(comp['functions']) >= 2:
                f.write("\n" + "-" * 80 + "\n")
                f.write("CODE COMPARISON (First 2 occurrences):\n")
                f.write("-" * 80 + "\n\n")

                func1 = comp['functions'][0]
                func2 = comp['functions'][1]

                f.write(f"Function 1: {func1['file']}:{func1['line']}\n")
                f.write("-" * 80 + "\n")
                f.write(func1['source'])
                f.write("\n\n")

                f.write(f"Function 2: {func2['file']}:{func2['line']}\n")
                f.write("-" * 80 + "\n")
                f.write(func2['source'])
                f.write("\n\n")

                # Show diff if not identical
                if comp['comparison']['similarity'] < 1.0:
                    f.write("Differences:\n")
                    f.write("-" * 80 + "\n")
                    for diff_line in comp['comparison']['diff']:
                        f.write(diff_line)
                    f.write("\n")
                else:
                    f.write("✅ Functions are IDENTICAL (100% match)\n\n")

    # Generate JSON report
    json_path = os.path.join(OUTPUT_DIR, f'duplicate_comparison_{timestamp}.json')
    json_report = {
        'timestamp': datetime.now().isoformat(),
        'total_groups': len(comparison_results),
        'comparisons': []
    }

    for comp in comparison_results:
        json_report['comparisons'].append({
            'hash': comp['hash'],
            'signature': comp['signature'],
            'similarity': comp['comparison']['similarity'],
            'num_occurrences': len(comp['functions']),
            'files': [
                {
                    'file': func['file'],
                    'line': func['line'],
                    'source_length': len(func['source'])
                }
                for func in comp['functions']
            ]
        })

    with open(json_path, 'w') as f:
        json.dump(json_report, f, indent=2)

    print(f"✅ Comparison complete!")
    print(f"   Text report: {report_path}")
    print(f"   JSON report: {json_path}")
    print(f"   Groups compared: {len(comparison_results)}")

    # Print summary
    identical = sum(1 for comp in comparison_results if comp['comparison']['similarity'] == 1.0)
    similar = sum(1 for comp in comparison_results if 0.9 <= comp['comparison']['similarity'] < 1.0)
    different = sum(1 for comp in comparison_results if comp['comparison']['similarity'] < 0.9)

    print(f"\n📊 Summary:")
    print(f"   Identical functions (100% match): {identical}")
    print(f"   Very similar (90-99%): {similar}")
    print(f"   Different (<90%): {different}")

    return report_path

if __name__ == "__main__":
    try:
        analyze_and_compare()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

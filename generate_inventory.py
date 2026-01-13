#!/usr/bin/env python3
"""
Generate Tool Inventory
Creates a comprehensive inventory of all Python scripts in the repository.

Usage:
    python generate_inventory.py [--output FORMAT] [--output-file FILE]
"""

import argparse
import ast
import json
import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime


def analyze_python_file(file_path):
    """Extract basic information from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            tree = ast.parse(content, filename=str(file_path))

        functions = [node.name for node in ast.walk(tree)
                    if isinstance(node, ast.FunctionDef)]
        classes = [node.name for node in ast.walk(tree)
                  if isinstance(node, ast.ClassDef)]

        # Check for common patterns
        has_main = any(f == 'main' for f in functions)
        has_cli = 'argparse' in content or 'click' in content
        has_dry_run = 'dry_run' in content or 'dry-run' in content

        # Count lines
        lines = content.split('\n')
        total_lines = len(lines)
        code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])

        # Check for imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return {
            'functions': functions,
            'classes': classes,
            'has_main': has_main,
            'has_cli': has_cli,
            'has_dry_run': has_dry_run,
            'total_lines': total_lines,
            'code_lines': code_lines,
            'imports': list(set(imports)),
            'function_count': len(functions),
            'class_count': len(classes),
        }
    except Exception as e:
        return {
            'error': str(e),
            'functions': [],
            'classes': [],
            'has_main': False,
            'has_cli': False,
            'has_dry_run': False,
            'total_lines': 0,
            'code_lines': 0,
            'imports': [],
            'function_count': 0,
            'class_count': 0,
        }


def generate_inventory(root_dir):
    """Generate inventory of all Python files."""
    inventory = defaultdict(list)
    stats = {
        'total_files': 0,
        'total_functions': 0,
        'total_classes': 0,
        'files_with_main': 0,
        'files_with_cli': 0,
        'files_with_dry_run': 0,
        'total_lines': 0,
        'total_code_lines': 0,
    }

    root_path = Path(root_dir)

    print("Analyzing Python files...")
    for py_file in root_path.rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue

        category = py_file.parent.name if py_file.parent != root_path else 'root'
        if category == root_path.name:
            category = 'root'

        info = analyze_python_file(py_file)
        file_info = {
            'file': py_file.name,
            'path': str(py_file.relative_to(root_path)),
            'category': category,
            'size_bytes': py_file.stat().st_size,
            **info
        }

        inventory[category].append(file_info)

        # Update stats
        stats['total_files'] += 1
        stats['total_functions'] += info['function_count']
        stats['total_classes'] += info['class_count']
        stats['total_lines'] += info['total_lines']
        stats['total_code_lines'] += info['code_lines']
        if info['has_main']:
            stats['files_with_main'] += 1
        if info['has_cli']:
            stats['files_with_cli'] += 1
        if info['has_dry_run']:
            stats['files_with_dry_run'] += 1

    return dict(inventory), stats


def export_json(inventory, stats, output_file):
    """Export inventory as JSON."""
    data = {
        'generated': datetime.now().isoformat(),
        'statistics': stats,
        'inventory': inventory
    }

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✓ Exported JSON to {output_file}")


def export_csv(inventory, stats, output_file):
    """Export inventory as CSV."""
    rows = []
    for category, files in inventory.items():
        for file_info in files:
            rows.append({
                'category': category,
                'file': file_info['file'],
                'path': file_info['path'],
                'functions': file_info['function_count'],
                'classes': file_info['class_count'],
                'has_main': file_info['has_main'],
                'has_cli': file_info['has_cli'],
                'has_dry_run': file_info['has_dry_run'],
                'total_lines': file_info['total_lines'],
                'code_lines': file_info['code_lines'],
                'size_bytes': file_info['size_bytes'],
            })

    if rows:
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"✓ Exported CSV to {output_file}")


def print_summary(inventory, stats):
    """Print summary statistics."""
    print("\n" + "=" * 60)
    print("INVENTORY SUMMARY")
    print("=" * 60)
    print(f"Total Python files: {stats['total_files']}")
    print(f"Total functions: {stats['total_functions']}")
    print(f"Total classes: {stats['total_classes']}")
    print(f"Files with main(): {stats['files_with_main']}")
    print(f"Files with CLI: {stats['files_with_cli']}")
    print(f"Files with dry-run: {stats['files_with_dry_run']}")
    print(f"Total lines: {stats['total_lines']:,}")
    print(f"Code lines: {stats['total_code_lines']:,}")

    print("\n" + "=" * 60)
    print("BY CATEGORY")
    print("=" * 60)
    for category in sorted(inventory.keys()):
        files = inventory[category]
        print(f"\n{category}: {len(files)} files")
        if len(files) <= 10:
            for f in files:
                print(f"  - {f['file']}")
        else:
            for f in files[:5]:
                print(f"  - {f['file']}")
            print(f"  ... and {len(files) - 5} more")


def main():
    parser = argparse.ArgumentParser(
        description='Generate inventory of Python scripts'
    )
    parser.add_argument(
        '--root',
        type=str,
        default='/Users/steven/pythons',
        help='Root directory to scan (default: /Users/steven/pythons)'
    )
    parser.add_argument(
        '--output',
        choices=['json', 'csv', 'both'],
        default='both',
        help='Output format'
    )
    parser.add_argument(
        '--output-file',
        type=str,
        help='Output file path (default: inventory.json/csv in root)'
    )

    args = parser.parse_args()

    root_path = Path(args.root)
    if not root_path.exists():
        print(f"Error: Root directory {root_path} does not exist")
        return 1

    # Generate inventory
    inventory, stats = generate_inventory(root_path)

    # Print summary
    print_summary(inventory, stats)

    # Export if requested
    if args.output in ['json', 'both']:
        json_file = args.output_file or str(root_path / 'inventory.json')
        export_json(inventory, stats, json_file)

    if args.output in ['csv', 'both']:
        csv_file = args.output_file or str(root_path / 'inventory.csv')
        if args.output == 'csv':
            csv_file = args.output_file or str(root_path / 'inventory.csv')
        export_csv(inventory, stats, csv_file)

    return 0


if __name__ == '__main__':
    exit(main())


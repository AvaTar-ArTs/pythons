#!/usr/bin/env python3
"""
Deep Duplicate Analysis Runner
Runs AST-based duplicate detection across all Python files
"""

import csv
import ast
import hashlib
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from difflib import SequenceMatcher


def read_file_content(filepath):
    """Read file content safely"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ""


def extract_code_signature(content):
    """Extract code signature using AST"""
    signature = {
        'imports': set(),
        'functions': set(),
        'classes': set(),
        'main_guard': False,
        'key_patterns': set(),
        'line_count': len(content.split('\n')) if content else 0,
        'content_hash': hashlib.md5(content.encode()).hexdigest() if content else ''
    }

    if not content:
        return signature

    try:
        tree = ast.parse(content)

        # Extract imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    signature['imports'].add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    signature['imports'].add(node.module.split('.')[0])

        # Extract functions and classes
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                signature['functions'].add(node.name.lower())
            elif isinstance(node, ast.ClassDef):
                signature['classes'].add(node.name.lower())

        # Check for main guard
        if 'if __name__ == ' in content:
            signature['main_guard'] = True

    except SyntaxError:
        # Fallback to regex if AST fails
        import re
        signature['imports'] = set(re.findall(r'^(?:import|from)\s+(\w+)', content, re.MULTILINE))
        signature['functions'] = set(re.findall(r'^def\s+(\w+)\s*\(', content, re.MULTILINE))
        signature['classes'] = set(re.findall(r'^class\s+(\w+)', content, re.MULTILINE))
        signature['main_guard'] = 'if __name__' in content

    # Detect key patterns
    content_lower = content.lower()
    if any(term in content_lower for term in ['openai', 'claude', 'anthropic', 'gpt']):
        signature['key_patterns'].add('ai_integration')
    if any(term in content_lower for term in ['requests', 'beautifulsoup', 'selenium']):
        signature['key_patterns'].add('web_scraping')
    if any(term in content_lower for term in ['flask', 'django', 'fastapi']):
        signature['key_patterns'].add('web_framework')
    if any(term in content_lower for term in ['pandas', 'numpy', 'csv.reader']):
        signature['key_patterns'].add('data_processing')

    return signature


def calculate_similarity(sig1, sig2):
    """Calculate similarity score between two signatures"""
    if sig1['line_count'] < 10 or sig2['line_count'] < 10:
        return 0.0

    # Exact match by content hash
    if sig1['content_hash'] == sig2['content_hash']:
        return 1.0

    similarity = 0.0

    # Import similarity (30%)
    if sig1['imports'] or sig2['imports']:
        import_sim = len(sig1['imports'] & sig2['imports']) / max(len(sig1['imports'] | sig2['imports']), 1)
        similarity += import_sim * 0.30

    # Function similarity (25%)
    if sig1['functions'] or sig2['functions']:
        func_sim = len(sig1['functions'] & sig2['functions']) / max(len(sig1['functions'] | sig2['functions']), 1)
        similarity += func_sim * 0.25

    # Class similarity (20%)
    if sig1['classes'] or sig2['classes']:
        class_sim = len(sig1['classes'] & sig2['classes']) / max(len(sig1['classes'] | sig2['classes']), 1)
        similarity += class_sim * 0.20

    # Pattern similarity (15%)
    if sig1['key_patterns'] or sig2['key_patterns']:
        pattern_sim = len(sig1['key_patterns'] & sig2['key_patterns']) / max(len(sig1['key_patterns'] | sig2['key_patterns']), 1)
        similarity += pattern_sim * 0.15

    # Main guard (5%)
    if sig1['main_guard'] == sig2['main_guard']:
        similarity += 0.05

    # Line count similarity (5%)
    line_diff = abs(sig1['line_count'] - sig2['line_count']) / max(sig1['line_count'], sig2['line_count'])
    similarity += (1 - line_diff) * 0.05

    return similarity


def find_duplicates(inventory_file, threshold=0.80):
    """Find functional duplicates in inventory"""
    print(f"\n{'='*70}")
    print("🔍 DEEP DUPLICATE ANALYSIS")
    print(f"{'='*70}\n")

    # Load inventory
    print(f"📂 Loading inventory: {inventory_file}")
    files = []
    with open(inventory_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        files = list(reader)

    print(f"✓ Loaded {len(files)} Python files\n")

    # Analyze files
    print("📖 Analyzing file contents...")
    signatures = {}

    for i, row in enumerate(files, 1):
        if i % 500 == 0:
            print(f"   Processed {i}/{len(files)}...")

        filepath = row['full_path']
        content = read_file_content(filepath)
        sig = extract_code_signature(content)

        signatures[filepath] = {
            'sig': sig,
            'location': row['location'],
            'filename': row['filename'],
            'size_kb': float(row['size_kb']),
            'code_lines': int(row['code_lines'])
        }

    print(f"✓ Analyzed {len(signatures)} files\n")

    # Find duplicates
    print(f"🔎 Finding duplicates (threshold: {threshold*100:.0f}%)...")
    duplicate_groups = []
    processed = set()

    for filepath1, data1 in signatures.items():
        if filepath1 in processed:
            continue

        # Skip small files
        if data1['sig']['line_count'] < 10:
            continue

        group = [{'path': filepath1, **data1, 'similarity': 1.0}]

        for filepath2, data2 in signatures.items():
            if filepath2 == filepath1 or filepath2 in processed:
                continue

            if data2['sig']['line_count'] < 10:
                continue

            sim = calculate_similarity(data1['sig'], data2['sig'])

            if sim >= threshold:
                group.append({'path': filepath2, **data2, 'similarity': sim})
                processed.add(filepath2)

        if len(group) > 1:
            duplicate_groups.append(group)
            for item in group:
                processed.add(item['path'])

    print(f"✓ Found {len(duplicate_groups)} duplicate groups\n")

    return duplicate_groups, signatures


def generate_reports(duplicate_groups):
    """Generate analysis reports"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Detailed CSV
    detail_file = f"FUNCTIONAL_DUPLICATES_DETAIL_{timestamp}.csv"
    with open(detail_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['group_id', 'file_count', 'similarity', 'location', 'filename',
                        'full_path', 'size_kb', 'code_lines'])

        for group_id, group in enumerate(duplicate_groups, 1):
            for item in sorted(group, key=lambda x: x['similarity'], reverse=True):
                writer.writerow([
                    group_id,
                    len(group),
                    f"{item['similarity']:.2%}",
                    item['location'],
                    item['filename'],
                    item['path'],
                    item['size_kb'],
                    item['code_lines']
                ])

    # Consolidation plan
    plan_file = f"CONSOLIDATION_PLAN_{timestamp}.md"
    with open(plan_file, 'w', encoding='utf-8') as f:
        f.write("# Functional Duplicate Consolidation Plan\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")

        # Statistics
        total_duplicates = sum(len(group) - 1 for group in duplicate_groups)
        total_size_kb = sum(
            sum(item['size_kb'] for item in group[1:])
            for group in duplicate_groups
        )
        total_lines = sum(
            sum(item['code_lines'] for item in group[1:])
            for group in duplicate_groups
        )

        f.write("## Summary\n\n")
        f.write(f"- **Duplicate Groups:** {len(duplicate_groups)}\n")
        f.write(f"- **Duplicate Files:** {total_duplicates}\n")
        f.write(f"- **Space Savings:** {total_size_kb/1024:.2f} MB\n")
        f.write(f"- **Lines of Code:** {total_lines:,}\n\n")

        # Top consolidation opportunities
        f.write("## Top Consolidation Opportunities\n\n")
        sorted_groups = sorted(duplicate_groups, key=lambda g: len(g), reverse=True)

        for i, group in enumerate(sorted_groups[:20], 1):
            avg_sim = sum(item['similarity'] for item in group) / len(group)
            f.write(f"### {i}. {group[0]['filename']} ({len(group)} copies, {avg_sim:.0%} similar)\n\n")

            # Locations
            locations = {}
            for item in group:
                loc = item['location']
                locations[loc] = locations.get(loc, 0) + 1

            f.write("**Locations:**\n")
            for loc, count in sorted(locations.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {loc}: {count} file(s)\n")

            f.write(f"\n**Keep:** `{group[0]['path']}`\n\n")
            f.write("**Remove/Replace:**\n")
            for item in group[1:]:
                f.write(f"- `{item['path']}` ({item['similarity']:.0%})\n")

            f.write("\n---\n\n")

    print(f"✓ Generated reports:")
    print(f"  - {detail_file}")
    print(f"  - {plan_file}\n")

    return detail_file, plan_file


def main():
    """Main execution"""
    # Find latest inventory
    inventory_files = sorted(Path('.').glob('PYTHON_INVENTORY_*.csv'), reverse=True)

    if not inventory_files:
        print("❌ No inventory file found. Run quick_python_inventory.py first.")
        return

    inventory_file = inventory_files[0]

    # Run analysis
    duplicate_groups, signatures = find_duplicates(str(inventory_file), threshold=0.80)

    if not duplicate_groups:
        print("✅ No functional duplicates found at 80% threshold!")
        return

    # Generate reports
    detail_file, plan_file = generate_reports(duplicate_groups)

    # Summary
    print(f"{'='*70}")
    print("📊 ANALYSIS COMPLETE")
    print(f"{'='*70}\n")

    total_files = len([item for group in duplicate_groups for item in group])
    total_unique = len(duplicate_groups)
    total_duplicates = total_files - total_unique

    print(f"Total Files Analyzed: {len(signatures):,}")
    print(f"Duplicate Groups: {len(duplicate_groups):,}")
    print(f"Files in Duplicate Groups: {total_files:,}")
    print(f"Unique Files to Keep: {total_unique:,}")
    print(f"Duplicate Files to Consolidate: {total_duplicates:,}")

    savings_kb = sum(
        sum(item['size_kb'] for item in group[1:])
        for group in duplicate_groups
    )
    print(f"\nEstimated Space Savings: {savings_kb/1024:.2f} MB")

    print(f"\n✓ See {plan_file} for consolidation recommendations\n")


if __name__ == "__main__":
    main()

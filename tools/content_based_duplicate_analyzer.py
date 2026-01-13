#!/usr/bin/env python3
"""
Content-Based Duplicate Analyzer
Analyzes actual code content, functionality, and usage patterns to find true duplicates
Ignores misleading filenames and focuses on what code actually does
"""

import csv
import ast
import re
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set
import hashlib
from difflib import SequenceMatcher

def load_csv_data(filename: str) -> List[Dict]:
    """Load data from CSV file"""
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def read_file_content(filepath: str) -> str:
    """Read file content safely"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ""

def extract_code_signature(content: str) -> Dict:
    """Extract comprehensive code signature from content"""
    signature = {
        'imports': set(),
        'functions': set(),
        'classes': set(),
        'main_guard': False,
        'docstring': '',
        'key_patterns': set(),
        'api_calls': set(),
        'complexity_score': 0,
        'line_count': len(content.split('\n')),
        'content_hash': hashlib.md5(content.encode()).hexdigest()
    }

    try:
        # Parse AST for accurate analysis
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
                if not signature['docstring'] and ast.get_docstring(node):
                    signature['docstring'] = ast.get_docstring(node)[:100]
            elif isinstance(node, ast.ClassDef):
                signature['classes'].add(node.name.lower())

        # Check for main guard
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                if (isinstance(node.test, ast.Compare) and
                    len(node.test.comparators) == 1 and
                    isinstance(node.test.comparators[0], ast.Str) and
                    node.test.comparators[0].s == '__main__' and
                    isinstance(node.test.left, ast.Name) and
                    node.test.left.id == '__name__'):
                    signature['main_guard'] = True
                    break

    except SyntaxError:
        # Fallback regex analysis
        signature['imports'] = set(re.findall(r'^(?:import|from)\s+(\w+)', content, re.MULTILINE))
        signature['functions'] = set(re.findall(r'^def\s+(\w+)\s*\(', content, re.MULTILINE))
        signature['classes'] = set(re.findall(r'^class\s+(\w+)', content, re.MULTILINE))
        signature['main_guard'] = 'if __name__ == \'__main__\'' in content

    # Extract key patterns and API calls
    content_lower = content.lower()

    # AI/ML patterns
    if any(term in content_lower for term in ['openai', 'claude', 'anthropic', 'gpt', 'llm']):
        signature['key_patterns'].add('ai_integration')

    # Web scraping
    if any(term in content_lower for term in ['requests', 'beautifulsoup', 'selenium', 'scrap']):
        signature['key_patterns'].add('web_scraping')

    # File operations
    if any(term in content_lower for term in ['open(', 'read(', 'write(', 'os.path']):
        signature['key_patterns'].add('file_operations')

    # Database
    if any(term in content_lower for term in ['sqlite', 'mongodb', 'postgres', 'mysql']):
        signature['key_patterns'].add('database')

    # GUI
    if any(term in content_lower for term in ['tkinter', 'pygame', 'flask', 'django']):
        signature['key_patterns'].add('gui_web')

    # Automation
    if any(term in content_lower for term in ['subprocess', 'automation', 'bot', 'selenium']):
        signature['key_patterns'].add('automation')

    # Calculate complexity score
    signature['complexity_score'] = (
        len(signature['functions']) * 2 +
        len(signature['classes']) * 3 +
        len(signature['imports']) +
        (10 if signature['main_guard'] else 0) +
        len(signature['key_patterns']) * 5
    )

    return signature

def calculate_content_similarity(sig1: Dict, sig2: Dict) -> float:
    """Calculate similarity between two code signatures"""
    similarity = 0.0
    total_weight = 0.0

    # Import similarity (high weight)
    import_sim = len(sig1['imports'] & sig2['imports']) / max(len(sig1['imports'] | sig2['imports']), 1)
    similarity += import_sim * 0.3
    total_weight += 0.3

    # Function similarity (high weight)
    func_sim = len(sig1['functions'] & sig2['functions']) / max(len(sig1['functions'] | sig2['functions']), 1)
    similarity += func_sim * 0.25
    total_weight += 0.25

    # Class similarity (high weight)
    class_sim = len(sig1['classes'] & sig2['classes']) / max(len(sig1['classes'] | sig2['classes']), 1)
    similarity += class_sim * 0.2
    total_weight += 0.2

    # Pattern similarity (medium weight)
    pattern_sim = len(sig1['key_patterns'] & sig2['key_patterns']) / max(len(sig1['key_patterns'] | sig2['key_patterns']), 1)
    similarity += pattern_sim * 0.15
    total_weight += 0.15

    # Main guard similarity (low weight)
    main_sim = 1.0 if sig1['main_guard'] == sig2['main_guard'] else 0.0
    similarity += main_sim * 0.05
    total_weight += 0.05

    # Docstring similarity (low weight)
    doc_sim = SequenceMatcher(None, sig1['docstring'], sig2['docstring']).ratio()
    similarity += doc_sim * 0.05
    total_weight += 0.05

    return similarity / total_weight if total_weight > 0 else 0.0

def find_functional_duplicates(data: List[Dict], similarity_threshold: float = 0.8) -> List[Dict]:
    """Find true functional duplicates based on content analysis"""
    duplicates = []

    # Read and analyze content for all files
    print("📖 Analyzing file contents...")
    file_signatures = {}

    for i, row in enumerate(data):
        if i % 10 == 0:
            print(f"   Processing {i+1}/{len(data)}: {row['filename']}")

        filepath = row['filepath']
        content = read_file_content(filepath)
        if content:
            signature = extract_code_signature(content)
            file_signatures[filepath] = {
                'signature': signature,
                'row': row,
                'content_length': len(content)
            }

    print(f"✅ Analyzed {len(file_signatures)} files with content")

    # Find duplicates based on content similarity
    processed = set()

    for filepath1, data1 in file_signatures.items():
        if filepath1 in processed:
            continue

        sig1 = data1['signature']
        row1 = data1['row']

        # Only consider files with substantial content
        if sig1['line_count'] < 10:
            continue

        candidates = []

        for filepath2, data2 in file_signatures.items():
            if filepath2 in processed or filepath2 == filepath1:
                continue

            sig2 = data2['signature']
            row2 = data2['row']

            # Skip very small files
            if sig2['line_count'] < 10:
                continue

            # Calculate similarity
            similarity = calculate_content_similarity(sig1, sig2)

            if similarity >= similarity_threshold:
                candidates.append((filepath2, row2, similarity))

        # If we found duplicates, recommend keeping the better one
        if candidates:
            # Sort candidates by similarity (highest first)
            candidates.sort(key=lambda x: x[2], reverse=True)

            # Keep the "best" version (larger, more complete, with main guard)
            all_versions = [(filepath1, row1, 1.0)] + candidates

            # Sort by quality metrics
            sorted_versions = sorted(all_versions, key=lambda x: (
                -int(x[1].get('line_count', '0')),  # Prefer more lines
                -int(x[1].get('functions_count', '0')),  # Prefer more functions
                -int(x[1].get('classes_count', '0')),  # Prefer more classes
                x[1].get('has_main', 'False') == 'True',  # Prefer main guard
                x[2]  # Then by similarity
            ), reverse=True)

            keep_file = sorted_versions[0]
            remove_candidates = sorted_versions[1:]

            # Create removal recommendations
            for remove_file, remove_row, similarity_score in remove_candidates:
                duplicates.append({
                    'file_to_remove': remove_file,
                    'filename': remove_row['filename'],
                    'reason': f'Functional duplicate of {keep_file[1]["filename"]} ({similarity_score:.2%} similar)',
                    'keep_file': keep_file[0],
                    'keep_filename': keep_file[1]['filename'],
                    'duplicate_type': 'Content Functional Duplicate',
                    'similarity_score': f'{similarity_score:.2%}',
                    'file_size': remove_row['file_size'],
                    'primary_purpose': remove_row['primary_purpose'],
                    'parent_folder': remove_row['parent_folder'],
                    'confidence': 'High' if similarity_score > 0.9 else 'Medium'
                })

            # Mark as processed
            processed.add(filepath1)
            for remove_file, _, _ in candidates:
                processed.add(remove_file)

    return duplicates

def find_identical_content(data: List[Dict]) -> List[Dict]:
    """Find files with identical content (same hash)"""
    duplicates = []

    # Group by content hash
    hash_groups = defaultdict(list)
    for row in data:
        filepath = row['filepath']
        content = read_file_content(filepath)
        if content:
            content_hash = hashlib.md5(content.encode()).hexdigest()
            hash_groups[content_hash].append((filepath, row))

    # Process groups with multiple files
    for content_hash, files in hash_groups.items():
        if len(files) > 1:
            # Sort by filepath (keep first one)
            files.sort(key=lambda x: x[0])
            keep_file = files[0]

            for remove_file, remove_row in files[1:]:
                duplicates.append({
                    'file_to_remove': remove_file,
                    'filename': remove_row['filename'],
                    'reason': 'Identical content - exact duplicate',
                    'keep_file': keep_file[0],
                    'keep_filename': keep_file[1]['filename'],
                    'duplicate_type': 'Identical Content',
                    'similarity_score': '100%',
                    'file_size': remove_row['file_size'],
                    'primary_purpose': remove_row['primary_purpose'],
                    'parent_folder': remove_row['parent_folder'],
                    'confidence': 'High'
                })

    return duplicates

def find_empty_useless_files(data: List[Dict]) -> List[Dict]:
    """Find truly empty or useless files based on content analysis"""
    useless_files = []

    for row in data:
        filepath = row['filepath']
        content = read_file_content(filepath)

        if not content:
            useless_files.append({
                'file_to_remove': filepath,
                'filename': row['filename'],
                'reason': 'Completely empty file',
                'keep_file': '',
                'keep_filename': '',
                'duplicate_type': 'Empty File',
                'similarity_score': 'N/A',
                'file_size': row['file_size'],
                'primary_purpose': row['primary_purpose'],
                'parent_folder': row['parent_folder'],
                'confidence': 'High'
            })
            continue

        # Analyze content quality
        lines = content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]

        # Check for minimal content
        if len(non_empty_lines) <= 2:
            useless_files.append({
                'file_to_remove': filepath,
                'filename': row['filename'],
                'reason': f'Near-empty file ({len(non_empty_lines)} non-empty lines)',
                'keep_file': '',
                'keep_filename': '',
                'duplicate_type': 'Minimal Content',
                'similarity_score': 'N/A',
                'file_size': row['file_size'],
                'primary_purpose': row['primary_purpose'],
                'parent_folder': row['parent_folder'],
                'confidence': 'High'
            })

        # Check for placeholder/stub content
        elif any(phrase in content.lower() for phrase in [
            'todo', 'fixme', 'placeholder', 'stub', 'not implemented',
            'coming soon', 'work in progress'
        ]):
            useless_files.append({
                'file_to_remove': filepath,
                'filename': row['filename'],
                'reason': 'Contains placeholder/stub content',
                'keep_file': '',
                'keep_filename': '',
                'duplicate_type': 'Stub File',
                'similarity_score': 'N/A',
                'file_size': row['file_size'],
                'primary_purpose': row['primary_purpose'],
                'parent_folder': row['parent_folder'],
                'confidence': 'Medium'
            })

    return useless_files

def create_content_based_csv(duplicates: List[Dict], filename: str):
    """Create CSV with content-based duplicate analysis"""
    if not duplicates:
        print(f"No duplicates found for {filename}")
        return

    fieldnames = [
        'action_type', 'file_path', 'filename', 'reason', 'target_file', 'target_filename',
        'duplicate_type', 'similarity_score', 'file_size', 'primary_purpose', 'parent_folder', 'confidence'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for dup in duplicates:
            row = {
                'action_type': 'Remove',
                'file_path': dup['file_to_remove'],
                'filename': dup['filename'],
                'reason': dup['reason'],
                'target_file': dup.get('keep_file', ''),
                'target_filename': dup.get('keep_filename', ''),
                'duplicate_type': dup['duplicate_type'],
                'similarity_score': dup.get('similarity_score', 'N/A'),
                'file_size': dup['file_size'],
                'primary_purpose': dup['primary_purpose'],
                'parent_folder': dup['parent_folder'],
                'confidence': dup['confidence']
            }
            writer.writerow(row)

    print(f"Created {filename} with {len(duplicates)} content-based recommendations")

def main():
    """Main analysis function"""
    print("🧠 Content-Based Duplicate Analysis")
    print("Ignoring misleading filenames, analyzing actual code functionality...")

    # Load data
    data = load_csv_data('home_directory_python_analysis.csv')
    print(f"Loaded {len(data)} files for content-based analysis")

    # Find different types of duplicates
    print("\n🔍 Analyzing file contents and functionality...")

    # Identical content (highest confidence)
    identical_files = find_identical_content(data)
    print(f"   • Identical content duplicates: {len(identical_files)}")

    # Functional duplicates (content-based similarity)
    functional_duplicates = find_functional_duplicates(data, similarity_threshold=0.8)
    print(f"   • Functional duplicates (80%+ similar): {len(functional_duplicates)}")

    # Empty/useless files
    useless_files = find_empty_useless_files(data)
    print(f"   • Empty/useless files: {len(useless_files)}")

    # Combine all recommendations
    all_duplicates = identical_files + functional_duplicates + useless_files

    # Create comprehensive CSV
    print("\n💾 Creating content-based duplicate analysis...")
    create_content_based_csv(all_duplicates, 'content_based_duplicates_to_remove.csv')

    # Summary
    total_removals = len(all_duplicates)
    space_saved = sum(int(d.get('file_size', 0)) for d in all_duplicates if d.get('file_size', '').isdigit())

    print("\n📊 Content-Based Analysis Summary:")
    print(f"   • Total files recommended for removal: {total_removals}")
    print(f"   • Identical content: {len(identical_files)}")
    print(f"   • Functional duplicates: {len(functional_duplicates)}")
    print(f"   • Empty/useless files: {len(useless_files)}")
    print(f"   • Estimated space savings: ~{space_saved // 1024} KB")

    # Show breakdown by confidence
    confidence_levels = Counter(d['confidence'] for d in all_duplicates)
    print("\n🎯 Confidence Levels:")
    for level, count in confidence_levels.most_common():
        print(f"   • {level}: {count} files")

    # Show duplicate types
    duplicate_types = Counter(d['duplicate_type'] for d in all_duplicates)
    print("\n📋 Duplicate Types:")
    for dup_type, count in duplicate_types.most_common():
        print(f"   • {dup_type}: {count} files")

    print("\n✅ Content-based duplicate analysis complete!")
    print("📄 Check 'content_based_duplicates_to_remove.csv' for detailed recommendations")
    print("\n🔍 Analysis focused on:")
    print("   • Actual code functionality (imports, functions, classes)")
    print("   • Usage patterns and API calls")
    print("   • Content similarity rather than filename similarity")
    print("   • True functional duplicates regardless of naming")

if __name__ == '__main__':
    main()
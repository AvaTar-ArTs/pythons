#!/usr/bin/env python3
"""
Duplicate Functionality Identifier and Consolidator
This script identifies duplicate functionality across the ~/pythons directory
and suggests consolidation opportunities.

Features:
- Identifies functionally similar scripts
- Groups scripts by functionality
- Suggests consolidation strategies
- Creates consolidation plan
"""

import os
import sys
import ast
import hashlib
import difflib
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import re


def extract_functions_from_file(file_path: Path) -> List[str]:
    """Extract function names from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
        
        return functions
    except:
        return []


def extract_imports_from_file(file_path: Path) -> List[str]:
    """Extract import statements from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
        
        return imports
    except:
        return []


def calculate_file_similarity(file1_path: Path, file2_path: Path) -> float:
    """Calculate similarity between two files based on content."""
    try:
        with open(file1_path, 'r', encoding='utf-8') as f1:
            content1 = f1.read()
        
        with open(file2_path, 'r', encoding='utf-8') as f2:
            content2 = f2.read()
        
        # Calculate similarity using difflib
        similarity = difflib.SequenceMatcher(None, content1, content2).ratio()
        return similarity
    except:
        return 0.0


def get_file_hash(file_path: Path) -> str:
    """Calculate hash of file content."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        return hashlib.md5(content).hexdigest()
    except:
        return ""


def identify_duplicate_scripts(base_path: Path) -> Dict[str, List[Path]]:
    """Identify potentially duplicate or similar scripts."""
    print("Identifying duplicate and similar scripts...")
    
    # Group files by name patterns
    name_pattern_groups = defaultdict(list)
    content_hash_groups = defaultdict(list)
    function_groups = defaultdict(list)
    
    # Get all Python files
    py_files = list(base_path.rglob("*.py"))
    py_files = [f for f in py_files if not any(d in str(f) for d in ['__pycache__', '.git', 'node_modules', '.venv', 'venv'])]
    
    print(f"Analyzing {len(py_files)} Python files...")
    
    # Group by name patterns
    for file_path in py_files:
        name = file_path.stem.lower()
        # Normalize names by removing common prefixes/suffixes
        normalized_name = re.sub(r'^(file_|social_|media_|data_|ai_|auto_)', '', name)
        normalized_name = re.sub(r'(_file|_script|_tool|_util)$', '', normalized_name)
        name_pattern_groups[normalized_name].append(file_path)
    
    # Group by content hash
    for file_path in py_files:
        file_hash = get_file_hash(file_path)
        if file_hash:
            content_hash_groups[file_hash].append(file_path)
    
    # Group by function signatures
    for file_path in py_files:
        functions = extract_functions_from_file(file_path)
        if functions:
            # Create a signature based on function names
            func_signature = tuple(sorted(functions))
            function_groups[func_signature].append(file_path)
    
    # Find similar files based on content
    similar_files = defaultdict(list)
    for i, file1 in enumerate(py_files):
        for j, file2 in enumerate(py_files[i+1:], i+1):
            similarity = calculate_file_similarity(file1, file2)
            if similarity > 0.8:  # 80% similarity threshold
                similar_files[file1].append((file2, similarity))
                similar_files[file2].append((file1, similarity))
    
    # Compile results
    duplicates = {
        'by_name_pattern': {k: v for k, v in name_pattern_groups.items() if len(v) > 1},
        'by_content_hash': {k: v for k, v in content_hash_groups.items() if len(v) > 1},
        'by_function_signature': {k: v for k, v in function_groups.items() if len(v) > 1},
        'by_content_similarity': similar_files
    }
    
    return duplicates


def identify_functional_duplicates(base_path: Path) -> Dict[str, List[Path]]:
    """Identify scripts with similar functionality."""
    print("Identifying functionally similar scripts...")
    
    # Define common functionality patterns
    functionality_indicators = {
        'file_organization': [
            'organize', 'rename', 'move', 'sort', 'group', 'categorize', 
            'file_management', 'directory', 'structure'
        ],
        'deduplication': [
            'duplicate', 'dedup', 'remove', 'unique', 'distinct', 'hash', 'md5'
        ],
        'ai_integration': [
            'openai', 'anthropic', 'claude', 'chatgpt', 'groq', 'llm', 
            'api_key', 'client', 'message'
        ],
        'social_media': [
            'instagram', 'twitter', 'facebook', 'social', 'bot', 'follow', 
            'like', 'post', 'comment'
        ],
        'media_processing': [
            'image', 'audio', 'video', 'resize', 'convert', 'process', 
            'transform', 'metadata'
        ],
        'data_processing': [
            'csv', 'json', 'data', 'process', 'analyze', 'transform', 
            'pandas', 'numpy'
        ]
    }
    
    functional_groups = defaultdict(list)
    
    # Analyze each Python file
    py_files = list(base_path.rglob("*.py"))
    py_files = [f for f in py_files if not any(d in str(f) for d in ['__pycache__', '.git', 'node_modules', '.venv', 'venv'])]
    
    for file_path in py_files:
        content_lower = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content_lower = f.read().lower()
        except:
            continue
        
        file_name_lower = file_path.stem.lower()
        
        # Check for functionality indicators
        for func_type, indicators in functionality_indicators.items():
            # Check in both filename and content
            name_matches = any(indicator in file_name_lower for indicator in indicators)
            content_matches = any(indicator in content_lower for indicator in indicators)
            
            if name_matches or content_matches:
                functional_groups[func_type].append(file_path)
    
    # Filter to only groups with multiple files
    functional_groups = {k: v for k, v in functional_groups.items() if len(v) > 1}
    
    return functional_groups


def generate_consolidation_report(duplicates: Dict, functional_groups: Dict, base_path: Path):
    """Generate a report of consolidation opportunities."""
    print("\n" + "="*80)
    print("CONSOLIDATION OPPORTUNITIES REPORT")
    print("="*80)
    
    report_path = base_path / "consolidation_opportunities_report.txt"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("CONSOLIDATION OPPORTUNITIES REPORT\n")
        f.write("="*80 + "\n\n")
        
        # Report by name patterns
        f.write("1. DUPLICATES BY NAME PATTERNS\n")
        f.write("-" * 40 + "\n")
        for pattern, files in duplicates['by_name_pattern'].items():
            if len(files) > 1:
                f.write(f"\nPattern: {pattern}\n")
                f.write(f"Files ({len(files)}):\n")
                for file in files:
                    f.write(f"  - {file}\n")
                f.write(f"Suggestion: Consolidate into a single configurable script\n\n")
        
        # Report by content hash
        f.write("\n2. EXACT DUPLICATES BY CONTENT\n")
        f.write("-" * 40 + "\n")
        for hash_val, files in duplicates['by_content_hash'].items():
            if len(files) > 1:
                f.write(f"\nHash: {hash_val[:8]}...\n")
                f.write(f"Files ({len(files)}):\n")
                for file in files:
                    f.write(f"  - {file}\n")
                f.write(f"Suggestion: Remove duplicates, keep one copy\n\n")
        
        # Report by function signature
        f.write("\n3. SIMILAR BY FUNCTION SIGNATURE\n")
        f.write("-" * 40 + "\n")
        for sig, files in duplicates['by_function_signature'].items():
            if len(files) > 1 and sig:  # Skip empty signatures
                f.write(f"\nFunctions: {', '.join(sig[:5])}{'...' if len(sig) > 5 else ''}\n")
                f.write(f"Files ({len(files)}):\n")
                for file in files:
                    f.write(f"  - {file}\n")
                f.write(f"Suggestion: Consider merging common functionality\n\n")
        
        # Report by content similarity
        f.write("\n4. SIMILAR BY CONTENT STRUCTURE\n")
        f.write("-" * 40 + "\n")
        similar_items = list(duplicates['by_content_similarity'].items())
        if similar_items:
            for file, similar_list in similar_items[:10]:  # Limit to top 10
                f.write(f"\nFile: {file}\n")
                f.write("Similar files:\n")
                for sim_file, similarity in sorted(similar_list, key=lambda x: x[1], reverse=True)[:3]:
                    f.write(f"  - {sim_file} (similarity: {similarity:.2f})\n")
                f.write(f"Suggestion: Review for potential consolidation\n\n")
        
        # Report by functionality
        f.write("\n5. FUNCTIONALLY SIMILAR SCRIPTS\n")
        f.write("-" * 40 + "\n")
        for func_type, files in functional_groups.items():
            if len(files) > 1:
                f.write(f"\nFunctionality: {func_type}\n")
                f.write(f"Files ({len(files)}):\n")
                for file in files:
                    f.write(f"  - {file}\n")
                f.write(f"Suggestion: Create unified {func_type} framework\n\n")
    
    print(f"Report saved to: {report_path}")
    return report_path


def suggest_consolidation_strategy(functional_groups: Dict) -> List[str]:
    """Suggest specific consolidation strategies."""
    strategies = []
    
    for func_type, files in functional_groups.items():
        if len(files) > 3:  # Only suggest for groups with 4+ files
            if func_type == 'file_organization':
                strategies.append(
                    f"Create unified file organization system for {len(files)} scripts"
                )
            elif func_type == 'deduplication':
                strategies.append(
                    f"Create centralized deduplication engine for {len(files)} scripts"
                )
            elif func_type == 'ai_integration':
                strategies.append(
                    f"Create unified AI client manager for {len(files)} integration scripts"
                )
            elif func_type == 'social_media':
                strategies.append(
                    f"Create social media automation framework for {len(files)} scripts"
                )
            elif func_type == 'media_processing':
                strategies.append(
                    f"Create media processing pipeline for {len(files)} processing scripts"
                )
            elif func_type == 'data_processing':
                strategies.append(
                    f"Create data processing toolkit for {len(files)} analysis scripts"
                )
    
    return strategies


def main():
    """Main function to execute the duplicate identification."""
    if len(sys.argv) != 2:
        print("Usage: python identify_duplicates.py <path_to_puthons_directory>")
        sys.exit(1)
    
    base_path = Path(sys.argv[1])
    
    if not base_path.exists():
        print(f"Error: Path {base_path} does not exist")
        sys.exit(1)
    
    print(f"Analyzing directory: {base_path}")
    
    try:
        # Identify duplicates by various criteria
        duplicates = identify_duplicate_scripts(base_path)
        
        # Identify functionally similar scripts
        functional_groups = identify_functional_duplicates(base_path)
        
        # Generate report
        report_path = generate_consolidation_report(duplicates, functional_groups, base_path)
        
        # Suggest consolidation strategies
        strategies = suggest_consolidation_strategy(functional_groups)
        
        print(f"\nTop consolidation opportunities:")
        for i, strategy in enumerate(strategies[:5], 1):
            print(f"{i}. {strategy}")
        
        print(f"\nDetailed report saved to: {report_path}")
        print(f"Found {len(functional_groups)} functional groups with potential for consolidation")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
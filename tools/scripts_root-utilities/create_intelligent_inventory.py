#!/usr/bin/env python3
"""
INTELLIGENT PYTHON INVENTORY GENERATOR
Creates comprehensive CSV with content-aware analysis
"""
import os
import csv
import ast
from pathlib import Path
from datetime import datetime
import re

def count_lines(filepath):
    """Count lines in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except:
        return 0

def extract_docstring(filepath):
    """Extract module docstring"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)
            return docstring[:200] if docstring else ""
    except:
        return ""

def extract_imports(filepath):
    """Extract import statements"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            tree = ast.parse(content)
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            return ', '.join(list(set(imports))[:10])  # First 10 unique
    except:
        return ""

def extract_classes_functions(filepath):
    """Count classes and functions"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            tree = ast.parse(content)
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            return len(classes), len(functions), ', '.join(classes[:5])
    except:
        return 0, 0, ""

def categorize_file(filepath, docstring, imports):
    """Categorize based on content"""
    path_str = str(filepath).lower()
    doc_lower = docstring.lower() if docstring else ""
    imports_lower = imports.lower() if imports else ""
    
    # Priority categories based on content analysis
    if 'seo' in doc_lower or 'seo' in path_str:
        return 'SEO_Optimization'
    elif 'youtube' in path_str or 'youtube' in imports_lower:
        return 'YouTube_Automation'
    elif 'instagram' in path_str or 'instagram' in imports_lower:
        return 'Instagram_Automation'
    elif 'medium' in doc_lower or 'article' in doc_lower:
        return 'Content_Generation'
    elif 'intelligence' in doc_lower or 'ast' in imports_lower:
        return 'AI_Analysis'
    elif 'orchestrat' in path_str or 'orchestrat' in doc_lower:
        return 'Orchestration'
    elif 'reddit' in path_str:
        return 'Reddit_Automation'
    elif 'twitch' in path_str:
        return 'Twitch_Automation'
    elif 'scrape' in path_str or 'scrape' in doc_lower:
        return 'Web_Scraping'
    elif 'audio' in path_str or 'music' in path_str:
        return 'Audio_Processing'
    elif 'video' in path_str:
        return 'Video_Processing'
    elif 'image' in path_str or 'image' in imports_lower:
        return 'Image_Processing'
    elif 'cleanup' in path_str or 'organize' in path_str:
        return 'File_Organization'
    elif 'csv' in path_str or 'pandas' in imports_lower:
        return 'Data_Processing'
    elif 'streamlit' in imports_lower or 'flask' in imports_lower:
        return 'Web_App'
    elif 'openai' in imports_lower or 'anthropic' in imports_lower:
        return 'AI_Integration'
    else:
        return 'Utilities'

def estimate_revenue_tier(category, lines, num_classes, num_functions):
    """Estimate revenue potential based on complexity"""
    complexity_score = (lines / 100) + (num_classes * 5) + (num_functions * 2)
    
    high_value_categories = ['SEO_Optimization', 'YouTube_Automation', 'Content_Generation', 
                            'AI_Analysis', 'Orchestration', 'Web_Scraping']
    medium_value_categories = ['Instagram_Automation', 'Reddit_Automation', 'Audio_Processing',
                              'Video_Processing', 'AI_Integration']
    
    if category in high_value_categories and complexity_score > 50:
        return 'Tier_1_High'
    elif category in high_value_categories or (category in medium_value_categories and complexity_score > 30):
        return 'Tier_2_Medium'
    elif complexity_score > 20:
        return 'Tier_3_Standard'
    else:
        return 'Tier_4_Utility'

print("🔍 Starting intelligent Python file analysis...")

# Find all Python files
base_paths = [
    Path('/Users/steven/pythons'),
    Path('/Users/steven/workspace/advanced_toolkit')
]

all_files = []
for base_path in base_paths:
    if base_path.exists():
        all_files.extend(base_path.rglob('*.py'))

print(f"📁 Found {len(all_files)} Python files")

# Analyze each file
results = []
for idx, filepath in enumerate(all_files, 1):
    if idx % 50 == 0:
        print(f"  Analyzed {idx}/{len(all_files)} files...")
    
    lines = count_lines(filepath)
    if lines == 0:
        continue
    
    docstring = extract_docstring(filepath)
    imports = extract_imports(filepath)
    num_classes, num_functions, class_names = extract_classes_functions(filepath)
    category = categorize_file(filepath, docstring, imports)
    revenue_tier = estimate_revenue_tier(category, lines, num_classes, num_functions)
    
    # Get relative path from home
    try:
        rel_path = filepath.relative_to(Path.home())
    except:
        rel_path = filepath
    
    results.append({
        'filepath': str(rel_path),
        'filename': filepath.name,
        'parent_folder': filepath.parent.name,
        'lines': lines,
        'num_classes': num_classes,
        'num_functions': num_functions,
        'class_names': class_names,
        'category': category,
        'revenue_tier': revenue_tier,
        'docstring': docstring.replace('\n', ' ').replace(',', ';')[:200] if docstring else '',
        'key_imports': imports[:200] if imports else '',
        'file_size_kb': filepath.stat().st_size // 1024,
        'last_modified': datetime.fromtimestamp(filepath.stat().st_mtime).strftime('%Y-%m-%d')
    })

# Sort by lines descending
results.sort(key=lambda x: x['lines'], reverse=True)

# Write CSV
output_path = '/Users/steven/csv_outputs/INTELLIGENT_PYTHON_INVENTORY.csv'
Path(output_path).parent.mkdir(exist_ok=True)

with open(output_path, 'w', newline='', encoding='utf-8') as f:
    if results:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

print(f"\n✅ Created: {output_path}")
print(f"📊 Total files analyzed: {len(results)}")

# Print summary by category
from collections import Counter
category_counts = Counter(r['category'] for r in results)
print("\n📋 Categories:")
for cat, count in category_counts.most_common():
    total_lines = sum(r['lines'] for r in results if r['category'] == cat)
    print(f"  {cat}: {count} files ({total_lines:,} lines)")

# Print top 10 by lines
print("\n🎯 Top 10 Largest Files:")
for i, r in enumerate(results[:10], 1):
    print(f"  {i}. {r['filename']} - {r['lines']:,} lines ({r['category']})")

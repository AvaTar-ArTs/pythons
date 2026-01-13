#!/usr/bin/env python3
"""
Analyze the Python files CSV catalog to identify patterns and insights
"""

import csv
import json
from pathlib import Path
from collections import Counter, defaultdict
import re
from datetime import datetime


def analyze_csv_patterns():
    """Analyze the CSV data to identify patterns and insights"""
    base_dir = Path("/Users/steven/pythons/CONTENT_AWARE_CATALOG")
    
    # Find the most recent CSV catalog
    csv_files = list(base_dir.glob("python_files_catalog_*.csv"))
    if not csv_files:
        print("❌ No catalog CSV file found")
        return None
    
    csv_file = csv_files[0]  # Get the most recent one
    print(f"📊 Analyzing catalog: {csv_file.name}")
    
    # Read the CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    print(f"📁 Analyzing {len(data)} Python files")
    
    # Initialize analysis results
    analysis = {
        'total_files': len(data),
        'total_size_mb': sum(int(row['size_bytes']) for row in data) / (1024 * 1024),
        'category_distribution': Counter(row['primary_category'] for row in data),
        'tag_distribution': Counter(),
        'size_analysis': {
            'largest_files': [],
            'smallest_files': [],
        },
        'code_metrics': {
            'avg_imports': sum(int(row['import_count']) for row in data) / len(data) if data else 0,
            'avg_functions': sum(int(row['function_count']) for row in data) / len(data) if data else 0,
            'avg_classes': sum(int(row['class_count']) for row in data) / len(data) if data else 0,
        },
        'feature_distribution': {
            'has_main_guard': sum(1 for row in data if row['has_main_guard'].lower() == 'true'),
            'ai_integration': sum(1 for row in data if row['ai_integration'].lower() == 'true'),
            'file_operations': sum(1 for row in data if row['file_operations'].lower() == 'true'),
            'data_processing': sum(1 for row in data if row['data_processing'].lower() == 'true'),
            'analysis_tools': sum(1 for row in data if row['analysis_tools'].lower() == 'true'),
            'deduplication': sum(1 for row in data if row['deduplication'].lower() == 'true'),
            'web_automation': sum(1 for row in data if row['web_automation'].lower() == 'true'),
            'media_processing': sum(1 for row in data if row['media_processing'].lower() == 'true'),
        },
        'duplicate_detection': [],
        'common_patterns': {},
        'suggestions': []
    }
    
    # Analyze tags
    all_tags = []
    for row in data:
        tags = row['tags'].split(', ')
        all_tags.extend([tag.strip() for tag in tags if tag.strip()])
        analysis['tag_distribution'].update([tag.strip() for tag in tags if tag.strip()])
    
    # Analyze file sizes
    size_data = [(int(row['size_bytes']), row['filename'], row['relative_path']) for row in data]
    size_data.sort(reverse=True)
    
    analysis['size_analysis']['largest_files'] = size_data[:10]
    analysis['size_analysis']['smallest_files'] = size_data[-10:][::-1]
    
    # Identify potential duplicates based on file hash
    hash_groups = defaultdict(list)
    for row in data:
        hash_groups[row['file_hash']].append(row)
    
    # Find actual duplicates (same content)
    actual_duplicates = {h: files for h, files in hash_groups.items() if len(files) > 1}
    analysis['duplicate_detection'] = actual_duplicates
    
    # Find files with similar names but different content (potential duplicates)
    name_groups = defaultdict(list)
    for row in data:
        # Extract just the name without extension and common suffixes
        name = row['filename'].replace('.py', '')
        # Remove version numbers and common suffixes
        clean_name = re.sub(r'_v?\d+|_\d+$|_backup|_copy|_old', '', name)
        name_groups[clean_name].append(row)
    
    # Find files with the same clean name but different paths
    name_duplicates = {name: files for name, files in name_groups.items() if len(files) > 1}
    analysis['name_variants'] = name_duplicates
    
    # Identify common patterns in code complexity
    analysis['code_metrics']['most_imports'] = max(data, key=lambda x: int(x['import_count'])) if data else None
    analysis['code_metrics']['most_functions'] = max(data, key=lambda x: int(x['function_count'])) if data else None
    analysis['code_metrics']['most_classes'] = max(data, key=lambda x: int(x['class_count'])) if data else None
    
    # Identify files with unusual characteristics for potential issues
    large_simple_files = []
    small_complex_files = []
    
    for row in data:
        size = int(row['size_bytes'])
        functions = int(row['function_count'])
        classes = int(row['class_count'])
        
        # Large files with little functionality may be data dumps
        if size > 10000 and functions == 0 and classes == 0:
            large_simple_files.append(row['filename'])
        
        # Very small files with complex functionality may be incomplete
        if size < 100 and (functions > 0 or classes > 0):
            small_complex_files.append(row['filename'])
    
    analysis['unusual_files'] = {
        'large_simple': large_simple_files,
        'small_complex': small_complex_files
    }
    
    print(f"✅ Analysis complete!")
    print(f"📊 Found {len(analysis['duplicate_detection'])} sets of exact duplicates")
    print(f"📊 Found {len(analysis['name_variants'])} sets of name variants")
    print(f"📊 Categories: {len(analysis['category_distribution'])}")
    print(f"📊 Total tags: {len(analysis['tag_distribution'])}")
    
    return analysis


def generate_suggestions(analysis):
    """Generate suggestions based on the analysis"""
    suggestions = []
    
    # Suggestion 1: Merge exact duplicates
    if analysis['duplicate_detection']:
        suggestions.append({
            'type': 'duplicate_removal',
            'priority': 'high',
            'description': f"Remove {len(analysis['duplicate_detection'])} sets of exact duplicates",
            'details': f"Found {sum(len(files) for files in analysis['duplicate_detection'].values())} duplicate files that have identical content and can be safely removed",
            'files_affected': sum(len(files) for files in analysis['duplicate_detection'].values())
        })
    
    # Suggestion 2: Consolidate similar functionality
    if analysis['name_variants']:
        suggestions.append({
            'type': 'consolidation',
            'priority': 'medium',
            'description': f"Consolidate {len(analysis['name_variants'])} sets of similar files",
            'details': f"Found {len(analysis['name_variants'])} groups of files with similar names that likely have overlapping functionality",
            'files_affected': sum(len(files) for files in analysis['name_variants'].values())
        })
    
    # Suggestion 3: Refactor highly common categories
    category_counts = analysis['category_distribution']
    if category_counts:
        most_common_category, count = category_counts.most_common(1)[0]
        if count > 100:  # If category has more than 100 files
            suggestions.append({
                'type': 'refactoring',
                'priority': 'medium',
                'description': f"Refactor {most_common_category} category ({count} files)",
                'details': f"The {most_common_category} category contains {count} files, suggesting potential for consolidating common functionality into shared modules",
                'files_affected': count
            })
    
    # Suggestion 4: Address unusual files
    unusual = analysis['unusual_files']
    if unusual['large_simple'] or unusual['small_complex']:
        suggestions.append({
            'type': 'cleanup',
            'priority': 'low',
            'description': f"Investigate {len(unusual['large_simple'] + unusual['small_complex'])} unusual files",
            'details': f"Found {len(unusual['large_simple'])} large files with minimal functionality and {len(unusual['small_complex'])} small files with complex functionality",
            'files_affected': len(unusual['large_simple'] + unusual['small_complex'])
        })
    
    # Suggestion 5: Standardize AI/ML integration
    if analysis['feature_distribution']['ai_integration'] > 50:
        suggestions.append({
            'type': 'standardization',
            'priority': 'medium',
            'description': f"Standardize AI integration across {analysis['feature_distribution']['ai_integration']} files",
            'details': f"With {analysis['feature_distribution']['ai_integration']} files using AI services, consider creating a common library for API calls",
            'files_affected': analysis['feature_distribution']['ai_integration']
        })
    
    # Suggestion 6: Create shared utility modules
    if analysis['feature_distribution']['file_operations'] > 100:
        suggestions.append({
            'type': 'modularization',
            'priority': 'high',
            'description': f"Create shared file operation utilities ({analysis['feature_distribution']['file_operations']} files)",
            'details': f"With {analysis['feature_distribution']['file_operations']} files handling file operations, consider consolidating common functions into shared modules",
            'files_affected': analysis['feature_distribution']['file_operations']
        })
    
    # Suggestion 7: Optimize for deduplication functionality
    if analysis['feature_distribution']['deduplication'] > 20:
        suggestions.append({
            'type': 'optimization',
            'priority': 'medium',
            'description': f"Create unified deduplication module ({analysis['feature_distribution']['deduplication']} files)",
            'details': f"With {analysis['feature_distribution']['deduplication']} files implementing deduplication logic, consider a centralized solution",
            'files_affected': analysis['feature_distribution']['deduplication']
        })
    
    # Suggestion 8: Documentation improvement
    runnable_count = analysis['feature_distribution']['has_main_guard']
    if runnable_count > 100:
        suggestions.append({
            'type': 'documentation',
            'priority': 'low',
            'description': f"Improve documentation for {runnable_count} executable scripts",
            'details': f"Many scripts ({runnable_count}) are executable but may lack proper documentation",
            'files_affected': runnable_count
        })
    
    return suggestions


def main():
    print("🔍 Analyzing CSV catalog for patterns and insights...")
    
    # Analyze the CSV
    analysis = analyze_csv_patterns()
    if not analysis:
        return
    
    # Generate suggestions
    suggestions = generate_suggestions(analysis)
    
    # Save analysis and suggestions
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = Path("/Users/steven/pythons/CONTENT_AWARE_CATALOG/analysis_suggestions.json")
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'analysis': analysis,
        'suggestions': suggestions
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📈 ANALYSIS SUMMARY:")
    print(f"   Total files: {analysis['total_files']:,}")
    print(f"   Total size: {analysis['total_size_mb']:.2f} MB")
    print(f"   Categories: {len(analysis['category_distribution'])}")
    print(f"   Unique tags: {len(analysis['tag_distribution'])}")
    
    print(f"\n📊 FEATURE DISTRIBUTION:")
    for feature, count in analysis['feature_distribution'].items():
        print(f"   {feature}: {count}")
    
    print(f"\n💡 SUGGESTIONS ({len(suggestions)} found):")
    for i, suggestion in enumerate(suggestions, 1):
        priority_emoji = '🔴' if suggestion['priority'] == 'high' else '🟡' if suggestion['priority'] == 'medium' else '🟢'
        print(f"   {i}. {priority_emoji} [{suggestion['priority'].upper()}] {suggestion['description']}")
        print(f"      {suggestion['details']}")
    
    print(f"\n📁 Analysis and suggestions saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    main()
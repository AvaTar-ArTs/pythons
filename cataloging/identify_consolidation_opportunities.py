#!/usr/bin/env python3
"""
Identify detailed consolidation opportunities in the Python codebase
"""

import csv
import json
from pathlib import Path
from collections import Counter, defaultdict
import re


def identify_consolidation_opportunities():
    """Identify detailed consolidation opportunities"""
    base_dir = Path("/Users/steven/pythons/CONTENT_AWARE_CATALOG")
    
    # Find the most recent CSV catalog
    csv_files = list(base_dir.glob("python_files_catalog_*.csv"))
    if not csv_files:
        print("❌ No catalog CSV file found")
        return None
    
    csv_file = csv_files[0]
    print(f"🔍 Identifying consolidation opportunities in: {csv_file.name}")
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    consolidation_opportunities = {
        'function_duplicates': find_function_duplicates(data),
        'category_consolidations': analyze_categories_for_consolidation(data),
        'common_import_patterns': analyze_common_imports(data),
        'similar_filename_patterns': analyze_similar_filenames(data),
        'repeated_functionality': identify_repeated_functionality(data)
    }
    
    return consolidation_opportunities


def find_function_duplicates(data):
    """Find files that likely have similar functions based on metadata"""
    # Look for files with similar names that might have duplicated functionality
    name_pattern_groups = defaultdict(list)
    
    for row in data:
        filename = row['filename'].replace('.py', '')
        
        # Extract base name by removing version numbers and suffixes
        base_name = re.sub(r'_v?\d+|_\d+$|_backup|_copy|_old|_new|_final|_updated|_revised', '', filename)
        name_pattern_groups[base_name].append(row)
    
    # Find groups with multiple files having the same base name
    duplications = {name: files for name, files in name_pattern_groups.items() if len(files) > 1}
    
    return duplications


def analyze_categories_for_consolidation(data):
    """Analyze categories to identify consolidation opportunities"""
    category_analysis = {}
    
    for category in set(row['primary_category'] for row in data):
        category_files = [row for row in data if row['primary_category'] == category]
        
        # Analyze common characteristics within the category
        category_analysis[category] = {
            'file_count': len(category_files),
            'avg_size': sum(int(f['size_bytes']) for f in category_files) / len(category_files) if category_files else 0,
            'avg_functions': sum(int(f['function_count']) for f in category_files) / len(category_files) if category_files else 0,
            'avg_imports': sum(int(f['import_count']) for f in category_files) / len(category_files) if category_files else 0,
            'has_main_guard_pct': sum(1 for f in category_files if f['has_main_guard'].lower() == 'true') / len(category_files) if category_files else 0,
            'common_tags': Counter(),
            'sample_files': [f['filename'] for f in category_files[:5]]  # Sample of top 5 files
        }
        
        # Count common tags within category
        all_tags = []
        for file_row in category_files:
            tags = file_row['tags'].split(', ')
            all_tags.extend([tag.strip() for tag in tags if tag.strip()])
        category_analysis[category]['common_tags'] = Counter(all_tags).most_common(5)
    
    return category_analysis


def analyze_common_imports(data):
    """Analyze common import patterns that suggest modularization opportunities"""
    # Count occurrences of each import
    import_counter = Counter()
    import_file_mapping = defaultdict(list)
    
    for row in data:
        # Count import count as a simple metric
        import_count = int(row['import_count'])
        if import_count > 0:  # Only consider files that have imports
            import_counter[row['primary_category']] += import_count
            import_file_mapping[row['primary_category']].append(row)
    
    return {
        'by_category': dict(import_counter),
        'mapping': {cat: len(files) for cat, files in import_file_mapping.items()}
    }


def analyze_similar_filenames(data):
    """Analyze files with similar naming patterns that might have duplicate functionality"""
    # Group by patterns in filenames
    pattern_groups = defaultdict(list)
    
    for row in data:
        filename = row['filename'].lower()
        
        # Identify common patterns that might indicate similar functionality
        if 'organize' in filename:
            pattern_groups['organization'].append(row)
        elif 'clean' in filename or 'cleanup' in filename or 'dedupe' in filename or 'deduplicate' in filename:
            pattern_groups['cleanup'].append(row)
        elif 'analysis' in filename or 'analyze' in filename or 'scanner' in filename:
            pattern_groups['analysis'].append(row)
        elif 'convert' in filename:
            pattern_groups['conversion'].append(row)
        elif 'download' in filename or 'fetch' in filename:
            pattern_groups['download'].append(row)
        elif 'process' in filename:
            pattern_groups['processing'].append(row)
    
    return {pattern: files for pattern, files in pattern_groups.items() if len(files) > 3}


def identify_repeated_functionality(data):
    """Identify functionality that appears repeatedly across files"""
    # Count occurrences of various features to find repeated functionality
    feature_counts = {
        'has_main_guard': 0,
        'ai_integration': 0,
        'file_operations': 0,
        'data_processing': 0,
        'analysis_tools': 0,
        'deduplication': 0,
        'web_automation': 0,
        'media_processing': 0
    }
    
    for row in data:
        for feature in feature_counts.keys():
            if row[feature].lower() == 'true':
                feature_counts[feature] += 1
    
    # Find features that appear frequently (potential for consolidation)
    frequent_features = {f: count for f, count in feature_counts.items() if count > 50}
    
    return frequent_features


def generate_consolidation_report(consolidation_opportunities):
    """Generate a detailed report of consolidation opportunities"""
    report = {
        'summary': {
            'total_opportunities': 0,
            'high_priority': 0,
            'medium_priority': 0,
            'low_priority': 0
        },
        'detailed_opportunities': []
    }
    
    # Report function duplicates (name-based)
    func_duplicates = consolidation_opportunities['function_duplicates']
    if func_duplicates:
        report['summary']['total_opportunities'] += len(func_duplicates)
        for name, files in list(func_duplicates.items())[:10]:  # Limit to top 10
            report['detailed_opportunities'].append({
                'type': 'name_duplicates',
                'priority': 'medium',
                'title': f"Similar functionality in {len(files)} files: {name}",
                'description': f"Files with similar names likely containing duplicated functionality: {', '.join([f['filename'] for f in files])}",
                'files_affected': [f['filename'] for f in files],
                'estimated_savings': len(files) - 1  # Potential files to remove/merge
            })
        report['summary']['medium_priority'] += len(func_duplicates)
    
    # Report category consolidations
    category_analysis = consolidation_opportunities['category_consolidations']
    for cat, analysis in category_analysis.items():
        if analysis['file_count'] > 50:  # Categories with many files
            report['summary']['total_opportunities'] += 1
            report['detailed_opportunities'].append({
                'type': 'category_consolidation',
                'priority': 'high' if analysis['file_count'] > 100 else 'medium',
                'title': f"Large {cat} category with {analysis['file_count']} files",
                'description': f"This category contains {analysis['file_count']} files with average size {analysis['avg_size']:.0f} bytes and {analysis['avg_functions']:.1f} functions per file. Consider consolidating common functionality.",
                'files_affected': analysis['sample_files'],
                'estimated_savings': analysis['file_count'] * 0.2  # Estimate 20% reduction potential
            })
            if analysis['file_count'] > 100:
                report['summary']['high_priority'] += 1
            else:
                report['summary']['medium_priority'] += 1
    
    # Report similar functionality patterns
    similar_patterns = consolidation_opportunities['similar_filename_patterns']
    for pattern, files in similar_patterns.items():
        report['summary']['total_opportunities'] += 1
        report['detailed_opportunities'].append({
            'type': 'pattern_duplicates',
            'priority': 'medium',
            'title': f"Similar {pattern} functionality in {len(files)} files",
            'description': f"Files that likely perform similar {pattern} operations: {', '.join([f['filename'] for f in files[:5]])}{'...' if len(files) > 5 else ''}",
            'files_affected': [f['filename'] for f in files],
            'estimated_savings': len(files) * 0.3  # Estimate 30% reduction potential
        })
        report['summary']['medium_priority'] += 1
    
    # Report repeated functionality
    repeated_functionality = consolidation_opportunities['repeated_functionality']
    for feature, count in repeated_functionality.items():
        if count > 100:  # Highly repeated functionality
            report['summary']['total_opportunities'] += 1
            priority = 'high' if count > 200 else 'medium'
            report['detailed_opportunities'].append({
                'type': 'repeated_functionality',
                'priority': priority,
                'title': f"Repeated {feature.replace('_', ' ')} functionality ({count} occurrences)",
                'description': f"The {feature} functionality appears in {count} files. This suggests a need for a shared library or module.",
                'files_affected': f"Approximately {count} files",
                'estimated_savings': f"Reduced code duplication across {count} files"
            })
            if priority == 'high':
                report['summary']['high_priority'] += 1
            else:
                report['summary']['medium_priority'] += 1
    
    return report


def main():
    print("🔍 Identifying consolidation opportunities...")
    
    # Identify consolidation opportunities
    opportunities = identify_consolidation_opportunities()
    if not opportunities:
        return
    
    # Generate detailed report
    report = generate_consolidation_report(opportunities)
    
    # Save the report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = Path("/Users/steven/pythons/CONTENT_AWARE_CATALOG/consolidation_opportunities.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📊 CONSOLIDATION OPPORTUNITIES REPORT:")
    print(f"   Total opportunities identified: {report['summary']['total_opportunities']}")
    print(f"   High priority: {report['summary']['high_priority']}")
    print(f"   Medium priority: {report['summary']['medium_priority']}")
    print(f"   Low priority: {report['summary']['low_priority']}")
    
    print(f"\n📋 DETAILED OPPORTUNITIES:")
    for i, opp in enumerate(report['detailed_opportunities'], 1):
        priority_emoji = '🔴' if opp['priority'] == 'high' else '🟡' if opp['priority'] == 'medium' else '🟢'
        print(f"   {i}. {priority_emoji} [{opp['priority'].upper()}] {opp['title']}")
        print(f"      {opp['description']}")
    
    print(f"\n📁 Consolidation report saved to: {output_file}")
    
    return report


if __name__ == "__main__":
    from datetime import datetime
    main()
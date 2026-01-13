#!/usr/bin/env python3
"""
Detect code quality issues and redundancies in the Python codebase
"""

import csv
import json
from pathlib import Path
from collections import Counter, defaultdict
import re


def detect_code_quality_issues():
    """Detect code quality issues and redundancies in the codebase"""
    base_dir = Path("/Users/steven/pythons/CONTENT_AWARE_CATALOG")
    
    # Find the most recent CSV catalog
    csv_files = list(base_dir.glob("python_files_catalog_*.csv"))
    if not csv_files:
        print("❌ No catalog CSV file found")
        return None
    
    csv_file = csv_files[0]
    print(f"🔍 Detecting code quality issues in: {csv_file.name}")
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    quality_issues = {
        'size_anomalies': detect_size_anomalies(data),
        'function_complexity': detect_function_complexity(data),
        'missing_main_guards': detect_missing_main_guards(data),
        'import_anomalies': detect_import_anomalies(data),
        'duplicated_logic': detect_duplicated_logic(data),
        'unused_patterns': detect_unused_patterns(data),
        'security_concerns': detect_security_concerns(data)
    }
    
    return quality_issues


def detect_size_anomalies(data):
    """Detect unusually large or small files"""
    size_issues = {
        'very_large_files': [],
        'very_small_files': [],
        'empty_files': []
    }
    
    for row in data:
        size = int(row['size_bytes'])
        filename = row['filename']
        
        if size == 0:
            size_issues['empty_files'].append({
                'filename': filename,
                'path': row['relative_path'],
                'size': size
            })
        elif size > 50000:  # Very large files (>50KB)
            size_issues['very_large_files'].append({
                'filename': filename,
                'path': row['relative_path'],
                'size': size
            })
        elif size < 50 and int(row['function_count']) > 0:  # Small files with functionality
            size_issues['very_small_files'].append({
                'filename': filename,
                'path': row['relative_path'],
                'size': size,
                'functions': int(row['function_count'])
            })
    
    return size_issues


def detect_function_complexity(data):
    """Detect files with high function/class counts"""
    complexity_issues = {
        'high_function_count': [],
        'high_class_count': [],
        'high_import_count': []
    }
    
    for row in data:
        func_count = int(row['function_count'])
        class_count = int(row['class_count'])
        import_count = int(row['import_count'])
        filename = row['filename']
        
        if func_count > 20:  # More than 20 functions per file
            complexity_issues['high_function_count'].append({
                'filename': filename,
                'path': row['relative_path'],
                'function_count': func_count
            })
        
        if class_count > 10:  # More than 10 classes per file
            complexity_issues['high_class_count'].append({
                'filename': filename,
                'path': row['relative_path'],
                'class_count': class_count
            })
        
        if import_count > 15:  # More than 15 imports per file
            complexity_issues['high_import_count'].append({
                'filename': filename,
                'path': row['relative_path'],
                'import_count': import_count
            })
    
    return complexity_issues


def detect_missing_main_guards(data):
    """Detect files that should have main guards but don't"""
    missing_guard_issues = []
    
    for row in data:
        has_guard = row['has_main_guard'].lower() == 'true'
        filename = row['filename']
        func_count = int(row['function_count'])
        class_count = int(row['class_count'])
        
        # Files with functions or classes but no main guard might be missing it
        if not has_guard and (func_count > 0 or class_count > 0):
            # Skip test files and special files that don't need guards
            if not any(skip in filename.lower() for skip in ['test_', 'setup', '__init__']):
                missing_guard_issues.append({
                    'filename': filename,
                    'path': row['relative_path'],
                    'function_count': func_count,
                    'class_count': class_count
                })
    
    return missing_guard_issues


def detect_import_anomalies(data):
    """Detect unusual import patterns"""
    import_issues = {
        'wildcard_imports': [],  # Potential if we could detect them from metadata
        'unusual_import_counts': []
    }
    
    # Files with unusually high import counts
    for row in data:
        import_count = int(row['import_count'])
        filename = row['filename']
        
        if import_count > 20:  # High number of imports might indicate tight coupling
            import_issues['unusual_import_counts'].append({
                'filename': filename,
                'path': row['relative_path'],
                'import_count': import_count
            })
    
    return import_issues


def detect_duplicated_logic(data):
    """Detect potential duplicated logic based on similar metadata patterns"""
    # Group files by similar characteristics that might indicate duplicated logic
    logic_patterns = defaultdict(list)
    
    for row in data:
        # Create a signature based on the features present
        signature = (
            row['ai_integration'],
            row['file_operations'], 
            row['data_processing'],
            row['analysis_tools'],
            row['deduplication'],
            row['web_automation'],
            row['media_processing'],
            row['primary_category']
        )
        logic_patterns[signature].append(row)
    
    # Find groups with more than one file that might have duplicated logic
    duplicated_logic_groups = {
        signature: files for signature, files in logic_patterns.items() 
        if len(files) > 1 and len(files) > 0.01 * len(data)  # At least 1% of files
    }
    
    return duplicated_logic_groups


def detect_unused_patterns(data):
    """Detect potentially unused or redundant patterns"""
    unused_issues = {
        'files_with_no_functionality': [],
        'duplicate_category_files': []
    }
    
    for row in data:
        func_count = int(row['function_count'])
        class_count = int(row['class_count'])
        filename = row['filename']
        
        # Files with no functions or classes might be placeholders or data files
        if func_count == 0 and class_count == 0:
            unused_issues['files_with_no_functionality'].append({
                'filename': filename,
                'path': row['relative_path'],
                'size': int(row['size_bytes'])
            })
    
    return unused_issues


def detect_security_concerns(data):
    """Detect potential security concerns"""
    security_issues = {
        'large_executable_files': [],
        'high_complexity_executables': []
    }
    
    for row in data:
        size = int(row['size_bytes'])
        func_count = int(row['function_count'])
        has_guard = row['has_main_guard'].lower() == 'true'
        filename = row['filename']
        
        # Large executable files might contain sensitive data
        if has_guard and size > 10000:
            security_issues['large_executable_files'].append({
                'filename': filename,
                'path': row['relative_path'],
                'size': size
            })
        
        # High complexity executable files might be harder to audit
        if has_guard and func_count > 15:
            security_issues['high_complexity_executables'].append({
                'filename': filename,
                'path': row['relative_path'],
                'function_count': func_count
            })
    
    return security_issues


def generate_quality_report(quality_issues):
    """Generate a detailed report of quality issues"""
    report = {
        'summary': {
            'total_issues': 0,
            'critical_issues': 0,
            'high_issues': 0,
            'medium_issues': 0,
            'low_issues': 0
        },
        'detailed_issues': []
    }
    
    # Report size anomalies
    size_issues = quality_issues['size_anomalies']
    if size_issues['empty_files']:
        report['summary']['total_issues'] += len(size_issues['empty_files'])
        report['summary']['medium_issues'] += len(size_issues['empty_files'])
        for file_info in size_issues['empty_files']:
            report['detailed_issues'].append({
                'type': 'empty_file',
                'severity': 'medium',
                'title': f"Empty file: {file_info['filename']}",
                'description': f"File {file_info['filename']} has zero bytes and no content. Consider removing if truly empty.",
                'path': file_info['path']
            })
    
    if size_issues['very_large_files']:
        report['summary']['total_issues'] += len(size_issues['very_large_files'])
        report['summary']['high_issues'] += len(size_issues['very_large_files'])
        for file_info in size_issues['very_large_files']:
            report['detailed_issues'].append({
                'type': 'large_file',
                'severity': 'high',
                'title': f"Very large file: {file_info['filename']} ({file_info['size']} bytes)",
                'description': f"File {file_info['filename']} is very large ({file_info['size']} bytes), which may impact performance and readability.",
                'path': file_info['path']
            })
    
    # Report function complexity issues
    complexity = quality_issues['function_complexity']
    if complexity['high_function_count']:
        report['summary']['total_issues'] += len(complexity['high_function_count'])
        report['summary']['high_issues'] += len(complexity['high_function_count'])
        for issue in complexity['high_function_count']:
            report['detailed_issues'].append({
                'type': 'high_function_count',
                'severity': 'high',
                'title': f"High function count: {issue['filename']} ({issue['function_count']} functions)",
                'description': f"File {issue['filename']} has {issue['function_count']} functions, which may indicate it should be broken into smaller modules.",
                'path': issue['path']
            })
    
    if complexity['high_class_count']:
        report['summary']['total_issues'] += len(complexity['high_class_count'])
        report['summary']['high_issues'] += len(complexity['high_class_count'])
        for issue in complexity['high_class_count']:
            report['detailed_issues'].append({
                'type': 'high_class_count',
                'severity': 'high',
                'title': f"High class count: {issue['filename']} ({issue['class_count']} classes)",
                'description': f"File {issue['filename']} has {issue['class_count']} classes, which may indicate it should be broken into smaller modules.",
                'path': issue['path']
            })
    
    # Report missing main guards
    missing_guards = quality_issues['missing_main_guards']
    if missing_guards:
        report['summary']['total_issues'] += len(missing_guards)
        report['summary']['medium_issues'] += len(missing_guards)
        for issue in missing_guards[:10]:  # Limit to first 10 to avoid too much output
            report['detailed_issues'].append({
                'type': 'missing_main_guard',
                'severity': 'medium',
                'title': f"Missing main guard: {issue['filename']}",
                'description': f"File {issue['filename']} has {issue['function_count']} functions and {issue['class_count']} classes but no main guard (if __name__ == '__main__':).",
                'path': issue['path']
            })
    
    # Report security concerns
    security = quality_issues['security_concerns']
    if security['large_executable_files']:
        report['summary']['total_issues'] += len(security['large_executable_files'])
        report['summary']['high_issues'] += len(security['large_executable_files'])
        for issue in security['large_executable_files']:
            report['detailed_issues'].append({
                'type': 'large_executable',
                'severity': 'high',
                'title': f"Large executable file: {issue['filename']}",
                'description': f"Executable file {issue['filename']} is very large ({issue['size']} bytes) which may contain sensitive information.",
                'path': issue['path']
            })
    
    return report


def main():
    print("🔍 Detecting code quality issues and redundancies...")
    
    # Detect quality issues
    issues = detect_code_quality_issues()
    if not issues:
        return
    
    # Generate detailed report
    report = generate_quality_report(issues)
    
    # Save the report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = Path("/Users/steven/pythons/CONTENT_AWARE_CATALOG/quality_issues_report.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📊 CODE QUALITY ISSUES REPORT:")
    print(f"   Total issues identified: {report['summary']['total_issues']}")
    print(f"   Critical: {report['summary']['critical_issues']}")
    print(f"   High: {report['summary']['high_issues']}")
    print(f"   Medium: {report['summary']['medium_issues']}")
    print(f"   Low: {report['summary']['low_issues']}")
    
    print(f"\n📋 DETAILED ISSUES:")
    for i, issue in enumerate(report['detailed_issues'][:15], 1):  # Limit output to first 15
        severity_emoji = '🔴' if issue['severity'] == 'high' else '🟡' if issue['severity'] == 'medium' else '🟢'
        print(f"   {i}. {severity_emoji} [{issue['severity'].upper()}] {issue['title']}")
    
    if len(report['detailed_issues']) > 15:
        print(f"   ... and {len(report['detailed_issues']) - 15} more issues")
    
    print(f"\n📁 Quality issues report saved to: {output_file}")
    
    return report


if __name__ == "__main__":
    from datetime import datetime
    main()
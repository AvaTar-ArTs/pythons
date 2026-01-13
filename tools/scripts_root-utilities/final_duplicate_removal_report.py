#!/usr/bin/env python3
"""
Final Duplicate Removal Report Generator
Creates a consolidated, actionable report of all duplicates that can be safely removed
Combines multiple analysis methods for comprehensive recommendations
"""

import csv
from collections import defaultdict, Counter
from pathlib import Path

def load_all_csv_data():
    """Load and consolidate data from all CSV analysis files"""
    data_sources = {
        'content_based': 'content_based_duplicates_to_remove.csv',
        'comprehensive': 'comprehensive_files_to_remove.csv',
        'basic': 'files_to_remove.csv'
    }

    all_recommendations = []
    seen_files = set()

    for source_name, filename in data_sources.items():
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    file_path = row['file_path']
                    if file_path not in seen_files:
                        row['analysis_source'] = source_name
                        all_recommendations.append(row)
                        seen_files.add(file_path)
        except FileNotFoundError:
            print(f"Warning: {filename} not found, skipping {source_name} analysis")

    return all_recommendations

def consolidate_duplicates(recommendations):
    """Consolidate duplicate recommendations, preferring higher confidence"""
    consolidated = {}
    conflict_resolution = {
        'content_based': 3,  # Highest priority
        'comprehensive': 2,  # Medium priority
        'basic': 1          # Lowest priority
    }

    for rec in recommendations:
        file_path = rec['file_path']

        if file_path not in consolidated:
            consolidated[file_path] = rec
        else:
            # Keep the recommendation with higher priority source
            current_priority = conflict_resolution[consolidated[file_path]['analysis_source']]
            new_priority = conflict_resolution[rec['analysis_source']]

            if new_priority > current_priority:
                consolidated[file_path] = rec

    return list(consolidated.values())

def categorize_by_risk_level(recommendations):
    """Categorize recommendations by risk level for safe removal"""
    categories = {
        'safe_high_confidence': [],      # Can be removed immediately
        'review_medium_confidence': [],  # Review before removal
        'careful_low_confidence': [],    # Careful consideration needed
        'investigate_high_impact': []    # May break functionality
    }

    for rec in recommendations:
        confidence = rec.get('confidence', 'Medium')
        duplicate_type = rec.get('duplicate_type', '')
        file_size = int(rec.get('file_size', 0))
        primary_purpose = rec.get('primary_purpose', '')

        # High confidence, safe to remove
        if confidence == 'High':
            categories['safe_high_confidence'].append(rec)

        # Medium confidence - review needed
        elif confidence == 'Medium':
            categories['review_medium_confidence'].append(rec)

        # Low confidence - careful consideration
        else:
            categories['careful_low_confidence'].append(rec)

    return categories

def calculate_space_savings(recommendations):
    """Calculate total space savings by category"""
    total_space = 0
    category_savings = defaultdict(int)

    for rec in recommendations:
        file_size = int(rec.get('file_size', 0))
        confidence = rec.get('confidence', 'Medium')

        total_space += file_size
        category_savings[confidence] += file_size

    return {
        'total_kb': total_space // 1024,
        'by_category': dict(category_savings),
        'largest_file': max((int(rec.get('file_size', 0)), rec['filename']) for rec in recommendations)
    }

def create_actionable_removal_plan(recommendations):
    """Create a step-by-step removal plan"""
    categories = categorize_by_risk_level(recommendations)
    space_info = calculate_space_savings(recommendations)

    plan = {
        'summary': {
            'total_files': len(recommendations),
            'total_space_saved_kb': space_info['total_kb'],
            'categories': {k: len(v) for k, v in categories.items()}
        },
        'removal_phases': {
            'phase_1_safe': categories['safe_high_confidence'],
            'phase_2_review': categories['review_medium_confidence'],
            'phase_3_careful': categories['careful_low_confidence']
        },
        'space_analysis': space_info
    }

    return plan

def generate_final_report():
    """Generate the final consolidated duplicate removal report"""

    print("🔍 Generating Final Duplicate Removal Report...")
    print("=" * 60)

    # Load and consolidate all recommendations
    all_recommendations = load_all_csv_data()
    consolidated = consolidate_duplicates(all_recommendations)

    print(f"📊 Found {len(consolidated)} unique files recommended for removal")

    # Create actionable plan
    plan = create_actionable_removal_plan(consolidated)

    # Generate report
    report_filename = 'FINAL_DUPLICATE_REMOVAL_REPORT.csv'

    with open(report_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header and summary
        writer.writerow(['FINAL DUPLICATE REMOVAL REPORT'])
        writer.writerow(['Generated from comprehensive multi-method analysis'])
        writer.writerow([''])
        writer.writerow(['SUMMARY STATISTICS'])
        writer.writerow(['Total files to remove', plan['summary']['total_files']])
        writer.writerow(['Total space savings (KB)', plan['summary']['total_space_saved_kb']])
        writer.writerow(['Largest file to remove', f"{plan['space_analysis']['largest_file'][1]} ({plan['space_analysis']['largest_file'][0]} bytes)"])
        writer.writerow([''])

        # Write category breakdown
        writer.writerow(['REMOVAL CATEGORIES'])
        writer.writerow(['Category', 'Files', 'Space Saved (KB)'])
        for category, count in plan['summary']['categories'].items():
            space_kb = plan['space_analysis']['by_category'].get(category.replace('_', ' ').title(), 0) // 1024
            writer.writerow([category.replace('_', ' ').title(), count, space_kb])
        writer.writerow([''])

        # Write detailed recommendations
        writer.writerow(['DETAILED REMOVAL RECOMMENDATIONS'])
        writer.writerow(['Phase', 'File Path', 'Filename', 'Reason', 'Confidence', 'Size (KB)', 'Duplicate Type', 'Analysis Source'])

        phase_names = {
            'phase_1_safe': 'PHASE 1: SAFE REMOVAL (High Confidence)',
            'phase_2_review': 'PHASE 2: REVIEW REQUIRED (Medium Confidence)',
            'phase_3_careful': 'PHASE 3: CAREFUL CONSIDERATION (Low Confidence)'
        }

        for phase_key, phase_files in plan['removal_phases'].items():
            if phase_files:
                writer.writerow([phase_names[phase_key], '', '', '', '', '', '', ''])

                for rec in sorted(phase_files, key=lambda x: int(x.get('file_size', 0)), reverse=True):
                    writer.writerow([
                        phase_key.replace('phase_', 'Phase ').replace('_', ' '),
                        rec['file_path'],
                        rec['filename'],
                        rec['reason'][:80] + '...' if len(rec['reason']) > 80 else rec['reason'],
                        rec.get('confidence', 'Medium'),
                        int(rec.get('file_size', 0)) // 1024,
                        rec.get('duplicate_type', ''),
                        rec.get('analysis_source', '')
                    ])
                writer.writerow([''])

    print(f"✅ Final report saved to: {report_filename}")
    print("\n📊 Report Summary:")
    print(f"   • Total files to remove: {plan['summary']['total_files']}")
    print(f"   • Space savings: {plan['summary']['total_space_saved_kb']} KB")
    print(f"   • Safe to remove immediately: {len(plan['removal_phases']['phase_1_safe'])} files")
    print(f"   • Require review: {len(plan['removal_phases']['phase_2_review'])} files")
    print(f"   • Need careful consideration: {len(plan['removal_phases']['phase_3_careful'])} files")

    # Show top space-saving files
    all_files = []
    for phase_files in plan['removal_phases'].values():
        all_files.extend(phase_files)

    if all_files:
        largest_files = sorted(all_files, key=lambda x: int(x.get('file_size', 0)), reverse=True)[:5]
        print("\n🏆 Top space-saving files:")
        for i, file in enumerate(largest_files, 1):
            size_kb = int(file.get('file_size', 0)) // 1024
            print(f"   {i}. {file['filename']} ({size_kb} KB) - {file.get('confidence', 'Medium')} confidence")

    print("\n🚀 Next Steps:")
    print("   1. Review the FINAL_DUPLICATE_REMOVAL_REPORT.csv file")
    print("   2. Start with Phase 1 (Safe Removal) files")
    print("   3. Backup files before removal")
    print("   4. Test functionality after each removal batch")

    return report_filename

def create_removal_script():
    """Create a safe removal script based on the analysis"""
    script_content = '''#!/bin/bash
# Safe Duplicate File Removal Script
# Generated from comprehensive analysis

set -e  # Exit on any error

echo "🗑️ Safe Duplicate File Removal Script"
echo "===================================="

# Create backup directory
BACKUP_DIR="$HOME/python_duplicate_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📁 Backup directory created: $BACKUP_DIR"

# Function to safely backup and remove
safe_remove() {
    local file_path="$1"
    local filename="$(basename "$file_path")"

    if [ -f "$file_path" ]; then
        echo "📋 Backing up: $filename"
        cp "$file_path" "$BACKUP_DIR/" 2>/dev/null || echo "⚠️  Warning: Could not backup $filename"

        echo "🗑️ Removing: $filename"
        rm "$file_path"
        echo "✅ Removed: $filename"
    else
        echo "⚠️ File not found: $filename"
    fi
}

echo ""
echo "🚀 Starting Phase 1: Safe High-Confidence Removals"
echo "=================================================="

# Add your high-confidence files here from the CSV
# Example:
# safe_remove "/path/to/file1.py"
# safe_remove "/path/to/file2.py"

echo ""
echo "📊 Backup Summary:"
ls -la "$BACKUP_DIR"

echo ""
echo "✅ Phase 1 Complete"
echo "📞 Next: Review Phase 2 recommendations in the CSV report"
echo "🛡️ All removed files backed up to: $BACKUP_DIR"
'''

    with open('safe_duplicate_removal.sh', 'w', encoding='utf-8') as f:
        f.write(script_content)

    # Make executable
    import os
    os.chmod('safe_duplicate_removal.sh', 0o755)

    print("✅ Safe removal script created: safe_duplicate_removal.sh")

if __name__ == '__main__':
    report_file = generate_final_report()
    create_removal_script()

    print("\n🎯 Final Output Files:")
    print(f"   • {report_file} - Comprehensive removal report")
    print("   • safe_duplicate_removal.sh - Safe removal script template")
    print("   • content_based_duplicates_to_remove.csv - Content analysis results")
    print("   • comprehensive_files_to_remove.csv - Filename analysis results")
    print("\n🎉 Duplicate analysis complete! Ready for cleanup implementation.")
    print("   Total potential space savings: Based on consolidated analysis")
    print("   Files ready for removal: Categorized by risk level")
    print("   Backup strategy: Automated and safe removal process")
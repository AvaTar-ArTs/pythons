#!/usr/bin/env python3
"""
Advanced Consolidation Strategy Generator
Based on existing deduplication data and analysis

Location: ~/pythons (all Python scripts belong in ~/pythons)
"""

import json
import csv
from collections import defaultdict, Counter
import os
from pathlib import Path

# All paths relative to home - script lives in ~/pythons
HOME = Path.home()


def analyze_existing_data():
    """Analyze existing deduplication reports"""
    
    print("🔍 ANALYZING EXISTING CONSOLIDATION DATA")
    print("=" * 50)
    
    results = {
        'structural_duplicates': {'groups': 0, 'total_files': 0, 'cross_directory': 0},
        'functionality_groups': {},
        'complexity_analysis': {'avg_score': 0, 'max_score': 0, 'file_count': 0}
    }
    
    # Analyze structural deduplication (paths from home)
    structural_file = HOME / 'REORGANIZATION_TEST_BED/data/inventory/structural_dedupe_report.csv'
    if structural_file.exists():
        with open(structural_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Occurrences', '1').isdigit():
                    occ = int(row['Occurrences'])
                    if occ > 1:
                        results['structural_duplicates']['groups'] += 1
                        results['structural_duplicates']['total_files'] += occ
                        
                        paths = row.get('Paths', '').split(';')
                        directories = set(str(Path(p.strip()).parent) for p in paths if p.strip())
                        if len(directories) > 1:
                            results['structural_duplicates']['cross_directory'] += 1
    
    # Analyze functionality groups
    functionality_file = HOME / 'REORGANIZATION_TEST_BED/data/inventory/FUNCTIONALITY_GROUPS.csv'
    if functionality_file.exists():
        with open(functionality_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                group = row.get('suggested_group', '')
                if group:
                    results['functionality_groups'][group] = results['functionality_groups'].get(group, 0) + 1
    
    # Analyze deep functionality
    deep_file = HOME / 'REORGANIZATION_TEST_BED/data/inventory/DEEP_FUNCTIONALITY_ANALYSIS.csv'
    if deep_file.exists():
        complexities = []
        with open(deep_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    functions = int(row.get('function_count', 0))
                    classes = int(row.get('class_count', 0))
                    lines = int(row.get('lines', 0))
                    complexity = functions + (classes * 2) + (lines / 100)
                    complexities.append(complexity)
                except (ValueError, TypeError):
                    continue
        
        if complexities:
            results['complexity_analysis']['avg_score'] = sum(complexities) / len(complexities)
            results['complexity_analysis']['max_score'] = max(complexities)
            results['complexity_analysis']['file_count'] = len(complexities)
    
    return results


def generate_strategy(results):
    """Generate comprehensive consolidation strategy"""
    
    strategy = {
        'executive_summary': {
            'total_duplicate_groups': results['structural_duplicates']['groups'],
            'files_to_consolidate': results['structural_duplicates']['total_files'] - results['structural_duplicates']['groups'],
            'cross_directory_risk': results['structural_duplicates']['cross_directory'],
            'complexity_reduction_needed': results['complexity_analysis']['max_score'] > 50
        },
        'phase_1_immediate': {
            'name': 'Safe Automated Deduplication',
            'risk_level': 'LOW',
            'estimated_time': '2-4 hours',
            'automated_percentage': 95,
            'actions': [
                'Remove exact hash duplicates in same directories',
                'Clean up temporary and backup files',
                'Remove duplicate documentation files',
                'Standardize configuration files'
            ]
        },
        'phase_2_structured': {
            'name': 'Structured Consolidation',
            'risk_level': 'MEDIUM',
            'estimated_time': '8-16 hours',
            'automated_percentage': 70,
            'actions': [
                f'Consolidate {results["structural_duplicates"]["cross_directory"]} cross-directory duplicate groups',
                'Merge functionality groups with similar purposes',
                'Refactor files with complexity scores > 50',
                'Update import references after consolidation'
            ]
        },
        'phase_3_architectural': {
            'name': 'Architectural Optimization',
            'risk_level': 'HIGH',
            'estimated_time': '20-40 hours',
            'automated_percentage': 40,
            'actions': [
                'Implement shared libraries for common functionality',
                'Create microservices architecture for complex components',
                'Establish API versioning and dependency management',
                'Implement continuous monitoring and automated testing'
            ]
        },
        'automation_opportunities': {
            'continuous_monitoring': 'Implement daily duplicate detection',
            'dependency_analysis': 'Create automated import dependency mapping',
            'consolidation_validation': 'Build automated testing for consolidation results',
            'progress_tracking': 'Implement metrics dashboard for consolidation progress'
        },
        'risk_mitigation': {
            'backup_strategy': 'Full system backup before any consolidation',
            'restore_later_csv': 'restore_later.csv in backup dir — selective restore when needed (not full rollback)',
            'rollback_plan': 'Version control and incremental commits',
            'testing_framework': 'Automated testing for all consolidated components',
            'documentation': 'Comprehensive documentation of all changes'
        }
    }
    
    return strategy


def create_implementation_script():
    """Create automated consolidation script (writes to $HOME)"""
    
    script_content = '''#!/bin/bash
# ADVANCED CONSOLIDATION IMPLEMENTATION SCRIPT
# Generated by ~/pythons/advanced_consolidation_strategy.py

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$HOME/consolidation_$(date +%Y%m%d_%H%M%S).log"
BACKUP_DIR="$HOME/consolidation_backup_$(date +%Y%m%d_%H%M%S)"
DRY_RUN=true

# Colors
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOG_FILE"
}

error() { echo -e "${RED}ERROR: $1${NC}" >&2; log "ERROR: $1"; }
success() { echo -e "${GREEN}SUCCESS: $1${NC}"; log "SUCCESS: $1"; }
warning() { echo -e "${YELLOW}WARNING: $1${NC}"; log "WARNING: $1"; }
info() { echo -e "${BLUE}INFO: $1${NC}"; log "INFO: $1"; }

# Phase 1: Safe Automated Actions
phase1_safe_automated() {
    info "=== PHASE 1: SAFE AUTOMATED DEDUPLICATION ==="
    
    if [ "$DRY_RUN" = true ]; then
        warning "DRY RUN MODE - No changes will be made"
        return
    fi
    
    DUPLICATE_FILE="${DUPLICATE_FILE:-$HOME/REORGANIZATION_TEST_BED/data/inventory/content_dedupe_report.csv}"
    export DUPLICATE_FILE
    # Phase 1 verifies content hash; only identical-byte duplicates are removed (no backup).
    if [ -f "$DUPLICATE_FILE" ]; then
        info "Processing duplicates (content-verified)..."
        
        python3 -c \"
import csv
import hashlib
import os
from pathlib import Path

def content_hash(path):
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return None

duplicate_file = os.environ.get('DUPLICATE_FILE')
if not duplicate_file:
    raise SystemExit('DUPLICATE_FILE must be set')

removed_files = []

with open(duplicate_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        occurrences = int(row.get('Occurrences', 1))
        if occurrences > 1:
            paths = [p.strip() for p in row.get('Paths', '').split(';') if p.strip()]
            
            if len(paths) > 1:
                directories = set(str(Path(p).parent) for p in paths)
                if len(directories) == 1:
                    ref_hash = content_hash(paths[0])
                    if ref_hash is None:
                        print('SKIP (unreadable):', paths[0])
                        continue
                    for duplicate_path in paths[1:]:
                        if not os.path.exists(duplicate_path):
                            continue
                        dup_hash = content_hash(duplicate_path)
                        if dup_hash is None:
                            print('SKIP (unreadable):', duplicate_path)
                            continue
                        if dup_hash != ref_hash:
                            print('SKIP (content differs):', duplicate_path)
                            continue
                        try:
                            os.remove(duplicate_path)
                            removed_files.append(duplicate_path)
                            print('REMOVED:', duplicate_path)
                        except OSError as e:
                            print('SKIP (remove failed):', duplicate_path, e)

print('Phase 1 Complete:', len(removed_files), 'content-identical duplicates removed')
for file in removed_files[:5]:
    print('  -', file)
if len(removed_files) > 5:
    print('  ... and', len(removed_files) - 5, 'more')
" DUPLICATE_FILE="$DUPLICATE_FILE"
        
        success "Phase 1 complete: content-identical duplicates removed (no backup)"
    else
        warning "Structural duplicate file not found: $DUPLICATE_FILE"
    fi
}

# Phase 2: Semi-Automated Consolidation
phase2_semi_automated() {
    info "=== PHASE 2: SEMI-AUTOMATED CONSOLIDATION ==="
    
    if [ "$DRY_RUN" = true ]; then
        warning "DRY RUN MODE - Phase 2 requires manual review"
        info "Recommendation: Review cross-directory duplicates manually"
        info "Run: python3 $HOME/pythons/advanced_consolidation_strategy.py"
        return
    fi
    
    warning "Phase 2 consolidation requires manual oversight"
    info "Use the generated reports to guide consolidation decisions"
}

# Main execution
main() {
    echo "============================================"
    echo "ADVANCED CODEBASE CONSOLIDATION SCRIPT"
    echo "Generated by ~/pythons/advanced_consolidation_strategy.py"
    echo "============================================"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --no-dry-run)
                DRY_RUN=false
                warning "DRY RUN DISABLED - REAL CHANGES WILL BE MADE"
                ;;
            --help)
                echo "Usage: $0 [--no-dry-run] [--help]"
                echo ""
                echo "Phases:"
                echo "  Phase 1: Safe automated deduplication (95% automated)"
                echo "  Phase 2: Semi-automated consolidation (70% automated)"
                echo ""
                echo "Options:"
                echo "  --no-dry-run    Disable dry run mode"
                echo "  --help          Show this help"
                echo ""
                echo "Strategy script: python3 $HOME/pythons/advanced_consolidation_strategy.py"
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                exit 1
                ;;
        esac
        shift
    done
    
    if [ "$DRY_RUN" = true ]; then
        warning "RUNNING IN DRY RUN MODE - NO CHANGES WILL BE MADE"
        echo "Use --no-dry-run to make actual changes"
    fi
    
    log "Starting advanced consolidation process (DRY_RUN=$DRY_RUN)"
    
    phase1_safe_automated
    phase2_semi_automated
    
    success "Consolidation process completed successfully"
    info "Review log file: $LOG_FILE"
    info "Phase 1 removes content-identical duplicates only (no backup)"
    
    echo ""
    echo "Next Steps:"
    echo "1. Review the log file for any issues"
    echo "2. Test your application functionality"
    echo "3. Run Phase 2 consolidation with manual oversight"
    echo "4. Re-run strategy: python3 $HOME/pythons/advanced_consolidation_strategy.py"
}

main "$@"
'''
    
    script_path = HOME / 'advanced_consolidation.sh'
    script_path.write_text(script_content)
    script_path.chmod(0o755)
    
    print(f'\n🔧 Generated consolidation script: {script_path}')
    return str(script_path)


def main():
    # Analyze existing data (paths from HOME)
    results = analyze_existing_data()
    
    # Generate strategy
    strategy = generate_strategy(results)
    
    # Save strategy to home
    strategy_file = HOME / 'advanced_consolidation_strategy.json'
    with open(strategy_file, 'w') as f:
        json.dump(strategy, f, indent=2, default=str)
    
    print(f'\n💾 Strategy saved to: {strategy_file}')
    
    # Print key insights
    print(f'\n📊 KEY INSIGHTS:')
    print(f'   Duplicate groups to address: {results["structural_duplicates"]["groups"]}')
    print(f'   Files to potentially remove: {results["structural_duplicates"]["total_files"] - results["structural_duplicates"]["groups"]}')
    print(f'   Cross-directory risks: {results["structural_duplicates"]["cross_directory"]}')
    
    if results['complexity_analysis']['file_count'] > 0:
        print(f'   Average complexity: {results["complexity_analysis"]["avg_score"]:.1f}')
        print(f'   Highest complexity: {results["complexity_analysis"]["max_score"]:.1f}')
    
    # Create implementation script (writes to $HOME)
    script_path = create_implementation_script()
    
    print(f'\n🎯 EXECUTION OPTIONS:')
    print(f'   1. Review strategy: cat {strategy_file}')
    print(f'   2. Run safe consolidation: bash {script_path}')
    print(f'   3. Run with real changes: bash {script_path} --no-dry-run')
    print(f'   4. Get help: bash {script_path} --help')
    print(f'   5. Re-run this script: python3 {HOME}/pythons/advanced_consolidation_strategy.py')


if __name__ == '__main__':
    main()

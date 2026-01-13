#!/usr/bin/env python3
"""
Generate optimization suggestions based on all analysis
"""

import json
from pathlib import Path
from datetime import datetime


def generate_optimization_suggestions():
    """Generate optimization suggestions based on previous analyses"""
    
    base_dir = Path("/Users/steven/pythons/CONTENT_AWARE_CATALOG")
    
    # Load all analysis results
    analysis_files = [
        base_dir / "analysis_suggestions.json",
        base_dir / "consolidation_opportunities.json", 
        base_dir / "quality_issues_report.json"
    ]
    
    analysis_data = {}
    for file_path in analysis_files:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                analysis_data[file_path.stem] = json.load(f)
        else:
            print(f"⚠️  Warning: {file_path} not found, skipping...")
    
    # Generate optimization suggestions from all data sources
    all_suggestions = []
    
    # Add suggestions from basic analysis
    if 'analysis_suggestions' in analysis_data:
        basic_suggestions = analysis_data['analysis_suggestions']['suggestions']
        for suggestion in basic_suggestions:
            all_suggestions.append({
                'category': 'general',
                'type': suggestion['type'],
                'priority': suggestion['priority'],
                'title': suggestion['description'],
                'description': suggestion['details'],
                'files_affected': suggestion.get('files_affected', 0),
                'source': 'basic_analysis'
            })
    
    # Add suggestions from consolidation opportunities
    if 'consolidation_opportunities' in analysis_data:
        consolidation_opp = analysis_data['consolidation_opportunities']
        for opportunity in consolidation_opp['detailed_opportunities']:
            all_suggestions.append({
                'category': 'consolidation',
                'type': opportunity['type'],
                'priority': opportunity['priority'],
                'title': opportunity['title'],
                'description': opportunity['description'],
                'files_affected': len(opportunity.get('files_affected', [])) if isinstance(opportunity.get('files_affected'), list) else opportunity.get('files_affected', 0),
                'source': 'consolidation_analysis'
            })
    
    # Add suggestions from quality issues
    if 'quality_issues_report' in analysis_data:
        quality_issues = analysis_data['quality_issues_report']
        for issue in quality_issues['detailed_issues']:
            all_suggestions.append({
                'category': 'quality',
                'type': issue['type'],
                'priority': issue['severity'],
                'title': issue['title'],
                'description': issue['description'],
                'files_affected': 1,  # Each issue affects one file
                'source': 'quality_analysis'
            })
    
    # Now create optimization-focused suggestions
    optimization_suggestions = create_optimization_suggestions(all_suggestions)
    
    return optimization_suggestions


def create_optimization_suggestions(all_suggestions):
    """Create optimization-focused suggestions from all data"""
    
    # Group suggestions by category and type for optimization focus
    optimization_items = []
    
    # 1. Code Duplication Reduction
    duplication_suggestions = [s for s in all_suggestions if 
                              any(keyword in s['type'] for keyword in ['duplicate', 'duplicated', 'name_duplicates', 'pattern_duplicates'])]
    
    if duplication_suggestions:
        total_dup_files = sum(s.get('files_affected', 0) for s in duplication_suggestions)
        optimization_items.append({
            'optimization_area': 'code_duplication_reduction',
            'priority': 'high',
            'title': f'Reduce code duplication across {len(duplication_suggestions)} areas',
            'description': f'Address code duplication patterns that affect approximately {total_dup_files} files',
            'impact': 'high',
            'effort': 'medium',
            'estimated_benefit': f'Minimize {total_dup_files} potentially redundant files/functionality'
        })
    
    # 2. Consolidation of Common Functionality
    consolidation_suggestions = [s for s in all_suggestions if 
                                'consolidation' in s['category'] or 'category_consolidation' in s['type']]
    
    if consolidation_suggestions:
        optimization_items.append({
            'optimization_area': 'common_functionality_consolidation',
            'priority': 'high',
            'title': f'Consolidate common functionality across {len(consolidation_suggestions)} areas',
            'description': 'Create shared libraries for common functionality instead of duplicating code across multiple files',
            'impact': 'high',
            'effort': 'high',
            'estimated_benefit': 'Improved maintainability, reduced redundancy, easier updates'
        })
    
    # 3. File Size Optimization
    size_suggestions = [s for s in all_suggestions if 
                       any(keyword in s['type'] for keyword in ['large_file', 'very_large_files', 'high_function_count', 'high_class_count'])]
    
    if size_suggestions:
        optimization_items.append({
            'optimization_area': 'file_size_optimization',
            'priority': 'medium',
            'title': f'Optimize {len(size_suggestions)} large files',
            'description': 'Break down large files into smaller, more manageable modules',
            'impact': 'medium',
            'effort': 'medium',
            'estimated_benefit': 'Improved readability, maintainability, and performance'
        })
    
    # 4. Standardization of Common Operations
    standardization_suggestions = [s for s in all_suggestions if 
                                  any(keyword in s['type'] for keyword in ['repeated_functionality', 'ai_integration', 'file_operations'])]
    
    if standardization_suggestions:
        optimization_items.append({
            'optimization_area': 'standardization',
            'priority': 'high',
            'title': 'Standardize common operations across multiple files',
            'description': 'Create standardized modules for AI integration, file operations, and other repeated functionality',
            'impact': 'high',
            'effort': 'medium',
            'estimated_benefit': 'Consistent behavior, easier maintenance, reduced bugs'
        })
    
    # 5. Pattern Optimization
    pattern_suggestions = [s for s in all_suggestions if 
                          any(keyword in s['type'] for keyword in ['analysis', 'cleanup', 'organize', 'download', 'processing'])]
    
    if pattern_suggestions:
        optimization_items.append({
            'optimization_area': 'pattern_optimization',
            'priority': 'medium',
            'title': f'Optimize {len(pattern_suggestions)} similar pattern groups',
            'description': 'Consolidate similar functionality patterns into reusable components',
            'impact': 'medium',
            'effort': 'medium',
            'estimated_benefit': 'Reduced redundancy, easier future development'
        })
    
    # 6. Quality Improvement
    quality_suggestions = [s for s in all_suggestions if s['category'] == 'quality']
    
    if quality_suggestions:
        optimization_items.append({
            'optimization_area': 'code_quality',
            'priority': 'medium',
            'title': f'Improve code quality across {len(quality_suggestions)} issues',
            'description': 'Address code quality issues to improve maintainability and reliability',
            'impact': 'medium',
            'effort': 'medium',
            'estimated_benefit': 'Better code quality, easier maintenance, reduced bugs'
        })
    
    return optimization_items


def generate_optimization_report():
    """Generate a comprehensive optimization report"""
    optimization_suggestions = generate_optimization_suggestions()
    
    # Categorize by priority
    high_priority = [s for s in optimization_suggestions if s['priority'] == 'high']
    medium_priority = [s for s in optimization_suggestions if s['priority'] == 'medium']
    low_priority = [s for s in optimization_suggestions if s['priority'] == 'low']
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_suggestions': len(optimization_suggestions),
            'high_priority': len(high_priority),
            'medium_priority': len(medium_priority),
            'low_priority': len(low_priority)
        },
        'suggestions': optimization_suggestions,
        'priority_breakdown': {
            'high': high_priority,
            'medium': medium_priority,
            'low': low_priority
        }
    }
    
    # Save the optimization report
    output_file = Path("/Users/steven/pythons/CONTENT_AWARE_CATALOG/optimization_suggestions.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)
    
    return report


def main():
    print("🔧 Generating optimization suggestions...")
    
    # Generate optimization report
    report = generate_optimization_report()
    
    print(f"\n⚙️  OPTIMIZATION SUGGESTIONS REPORT:")
    print(f"   Total suggestions: {report['summary']['total_suggestions']}")
    print(f"   High priority: {report['summary']['high_priority']}")
    print(f"   Medium priority: {report['summary']['medium_priority']}")
    print(f"   Low priority: {report['summary']['low_priority']}")
    
    print(f"\n🎯 TOP PRIORITY SUGGESTIONS:")
    high_priority = report['priority_breakdown']['high']
    for i, suggestion in enumerate(high_priority[:5], 1):  # Show top 5 high priority
        print(f"   {i}. 🔴 [HIGH] {suggestion['title']}")
        print(f"      {suggestion['description']}")
        print(f"      Impact: {suggestion['impact']}, Effort: {suggestion['effort']}")
    
    print(f"\n💡 MEDIUM PRIORITY SUGGESTIONS:")
    medium_priority = report['priority_breakdown']['medium']
    for i, suggestion in enumerate(medium_priority[:3], 1):  # Show top 3 medium priority
        print(f"   {i}. 🟡 [MEDIUM] {suggestion['title']}")
        print(f"      {suggestion['description']}")
    
    print(f"\n📁 Optimization suggestions report saved to: /Users/steven/pythons/CONTENT_AWARE_CATALOG/optimization_suggestions.json")
    
    return report


if __name__ == "__main__":
    main()
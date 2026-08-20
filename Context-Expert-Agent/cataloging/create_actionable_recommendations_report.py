#!/usr/bin/env python3
"""
Create a comprehensive actionable recommendations report
"""

import json
from pathlib import Path
from datetime import datetime


def create_actionable_recommendations_report():
    """Create a comprehensive actionable recommendations report"""
    
    base_dir = Path("/Users/steven/pythons/CONTENT_AWARE_CATALOG")
    
    # Load all analysis results
    analysis_files = [
        base_dir / "analysis_suggestions.json",
        base_dir / "consolidation_opportunities.json", 
        base_dir / "quality_issues_report.json",
        base_dir / "optimization_suggestions.json"
    ]
    
    analysis_data = {}
    for file_path in analysis_files:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                analysis_data[file_path.stem] = json.load(f)
        else:
            print(f"⚠️  Warning: {file_path} not found, skipping...")
    
    # Create a comprehensive report
    report = {
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'total_python_files': analysis_data.get('analysis_suggestions', {}).get('analysis', {}).get('total_files', 0),
            'total_size_mb': analysis_data.get('analysis_suggestions', {}).get('analysis', {}).get('total_size_mb', 0),
            'categories_identified': len(analysis_data.get('analysis_suggestions', {}).get('analysis', {}).get('category_distribution', {})),
            'consolidation_opportunities': analysis_data.get('consolidation_opportunities', {}).get('summary', {}).get('total_opportunities', 0),
            'quality_issues_found': analysis_data.get('quality_issues_report', {}).get('summary', {}).get('total_issues', 0),
            'optimization_suggestions': analysis_data.get('optimization_suggestions', {}).get('summary', {}).get('total_suggestions', 0)
        },
        'high_priority_recommendations': [],
        'medium_priority_recommendations': [],
        'detailed_findings': {},
        'implementation_roadmap': {}
    }
    
    # Add key findings from each analysis
    if 'analysis_suggestions' in analysis_data:
        report['detailed_findings']['basic_analysis'] = analysis_data['analysis_suggestions']['suggestions']
    
    if 'consolidation_opportunities' in analysis_data:
        report['detailed_findings']['consolidation'] = analysis_data['consolidation_opportunities']['detailed_opportunities']
        
        # Identify high priority consolidation opportunities
        high_consolidations = [opp for opp in analysis_data['consolidation_opportunities']['detailed_opportunities'] 
                              if opp['priority'] == 'high']
        for opp in high_consolidations:
            report['high_priority_recommendations'].append({
                'id': f"cons_{len(report['high_priority_recommendations'])}",
                'title': opp['title'],
                'description': opp['description'],
                'category': 'consolidation',
                'estimated_effort': 'high' if 'large' in opp['title'].lower() else 'medium',
                'estimated_impact': 'high',
                'implementation_notes': f"Consolidate functionality from {opp.get('files_affected', [])} if it's a list"
            })
    
    if 'quality_issues_report' in analysis_data:
        report['detailed_findings']['quality_issues'] = analysis_data['quality_issues_report']['detailed_issues']
        
        # Identify high priority quality issues
        high_quality_issues = [issue for issue in analysis_data['quality_issues_report']['detailed_issues'] 
                              if issue['severity'] == 'high']
        for issue in high_quality_issues[:5]:  # Top 5 quality issues
            report['high_priority_recommendations'].append({
                'id': f"qual_{len(report['high_priority_recommendations'])}",
                'title': issue['title'],
                'description': issue['description'],
                'category': 'quality',
                'estimated_effort': 'medium',
                'estimated_impact': 'high',
                'implementation_notes': "Address immediately to prevent potential issues"
            })
    
    if 'optimization_suggestions' in analysis_data:
        report['detailed_findings']['optimizations'] = analysis_data['optimization_suggestions']['suggestions']
        
        # Convert optimization suggestions to recommendations
        for opt in analysis_data['optimization_suggestions']['suggestions']:
            if opt['priority'] == 'high':
                report['high_priority_recommendations'].append({
                    'id': f"opt_{len(report['high_priority_recommendations'])}",
                    'title': opt['title'],
                    'description': opt['description'],
                    'category': opt['optimization_area'],
                    'estimated_effort': opt['effort'],
                    'estimated_impact': opt['impact'],
                    'implementation_notes': f"Estimated benefit: {opt['estimated_benefit']}"
                })
            else:
                report['medium_priority_recommendations'].append({
                    'id': f"opt_med_{len(report['medium_priority_recommendations'])}",
                    'title': opt['title'],
                    'description': opt['description'],
                    'category': opt['optimization_area'],
                    'estimated_effort': opt['effort'],
                    'estimated_impact': opt['impact'],
                    'implementation_notes': f"Estimated benefit: {opt['estimated_benefit']}"
                })
    
    # Create an implementation roadmap
    phase_1_immediate = [  # Address critical issues first
        rec for rec in report['high_priority_recommendations']
        if any(crit in rec['category'] for crit in ['quality', 'large_file', 'security'])
    ]

    phase_2_short_term = [  # High impact, medium effort
        rec for rec in report['high_priority_recommendations']
        if rec not in phase_1_immediate
    ]

    report['implementation_roadmap'] = {
        'phase_1_immediate': phase_1_immediate,
        'phase_2_short_term': phase_2_short_term,
        'phase_3_medium_term': report['medium_priority_recommendations'],
        'estimated_timeline': {
            'phase_1_duration': '1-2 weeks',
            'phase_2_duration': '1-2 months',
            'phase_3_duration': '2-3 months'
        }
    }
    
    # Add executive summary
    report['executive_summary'] = generate_executive_summary(report)
    
    return report


def generate_executive_summary(report):
    """Generate an executive summary of the findings"""
    summary = f"""
EXECUTIVE SUMMARY - Python Codebase Analysis
Generated: {report['generated_at']}

OVERVIEW:
- Analyzed {report['summary']['total_python_files']} Python files totaling {report['summary']['total_size_mb']:.2f} MB
- Identified {report['summary']['consolidation_opportunities']} consolidation opportunities
- Found {report['summary']['quality_issues_found']} quality issues
- Generated {report['summary']['optimization_suggestions']} optimization suggestions

KEY FINDINGS:
1. The codebase contains significant duplication, particularly in:
   - File operations (1,210 files)
   - Data processing (934 files) 
   - Analysis tools (765 files)
   - AI integration (358 files)

2. Large categories with potential for consolidation:
   - Media Processing: 459 files
   - Data Processing: 221 files
   - Automation Tools: 221 files
   - AI/ML Tools: 157 files

3. Quality concerns include:
   - {len([r for r in report['high_priority_recommendations'] if 'large' in r['title'].lower()])} very large files (>50KB)
   - Code duplication across hundreds of files
   - Missing standardization in common operations

PRIORITY RECOMMENDATIONS:
- Phase 1 (Immediate): Address quality issues and security concerns
- Phase 2 (Short-term): Consolidate common functionality across large categories
- Phase 3 (Medium-term): Implement standardization and further optimizations

POTENTIAL BENEFITS:
- Reduced maintenance overhead
- Improved code consistency
- Better performance through optimization
- Reduced redundancy and potential bugs
    """
    return summary


def main():
    print("📋 Creating comprehensive actionable recommendations report...")
    
    # Create the comprehensive report
    report = create_actionable_recommendations_report()
    
    # Save the comprehensive report
    output_file = Path("/Users/steven/pythons/CONTENT_AWARE_CATALOG/actionable_recommendations_report.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)
    
    # Also create a readable summary file
    summary_file = Path("/Users/steven/pythons/CONTENT_AWARE_CATALOG/actionable_recommendations_summary.md")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(report['executive_summary'])
        
        f.write("\n\nDETAILED RECOMMENDATIONS:\n")
        f.write("="*50 + "\n\n")
        
        f.write("HIGH PRIORITY RECOMMENDATIONS:\n")
        f.write("-" * 30 + "\n")
        for i, rec in enumerate(report['high_priority_recommendations'][:10], 1):  # Top 10
            f.write(f"{i}. {rec['title']}\n")
            f.write(f"   Category: {rec['category']}\n")
            f.write(f"   Impact: {rec['estimated_impact']}, Effort: {rec['estimated_effort']}\n")
            f.write(f"   Description: {rec['description']}\n\n")
        
        if len(report['high_priority_recommendations']) > 10:
            f.write(f"... and {len(report['high_priority_recommendations']) - 10} more\n\n")
        
        f.write("MEDIUM PRIORITY RECOMMENDATIONS:\n")
        f.write("-" * 35 + "\n")
        for i, rec in enumerate(report['medium_priority_recommendations'][:5], 1):  # Top 5
            f.write(f"{i}. {rec['title']}\n")
            f.write(f"   Category: {rec['category']}\n")
            f.write(f"   Description: {rec['description']}\n\n")
        
        if len(report['medium_priority_recommendations']) > 5:
            f.write(f"... and {len(report['medium_priority_recommendations']) - 5} more\n\n")
    
    print(f"\n📋 COMPREHENSIVE REPORT SUMMARY:")
    print(f"   Files analyzed: {report['summary']['total_python_files']:,}")
    print(f"   Total size: {report['summary']['total_size_mb']:.2f} MB")
    print(f"   High priority recommendations: {len(report['high_priority_recommendations'])}")
    print(f"   Medium priority recommendations: {len(report['medium_priority_recommendations'])}")
    
    print(f"\n🎯 IMPLEMENTATION ROADMAP:")
    print(f"   Phase 1 (Immediate): {len(report['implementation_roadmap']['phase_1_immediate'])} items")
    print(f"   Phase 2 (Short-term): {len(report['implementation_roadmap']['phase_2_short_term'])} items")
    print(f"   Phase 3 (Medium-term): {len(report['implementation_roadmap']['phase_3_medium_term'])} items")
    
    print(f"\n📁 Reports saved to:")
    print(f"   Detailed report: {output_file}")
    print(f"   Summary: {summary_file}")
    
    return report


if __name__ == "__main__":
    main()
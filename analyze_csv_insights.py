#!/usr/bin/env python3
"""
📊 CSV Analysis & Insights Generator
Analyzes the content analysis CSV and provides actionable insights
"""

import csv
import json
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Any
import re


def analyze_csv(csv_file: Path) -> Dict[str, Any]:
    """Comprehensive CSV analysis"""

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    analysis = {
        'total_files': len(rows),
        'categories': Counter(),
        'complexity_distribution': Counter(),
        'maturity_distribution': Counter(),
        'priority_stats': {},
        'high_priority_files': [],
        'organizational_opportunities': [],
        'recommendations': [],
        'patterns': {},
        'top_files_by_category': defaultdict(list)
    }

    priorities = []

    for row in rows:
        # Category distribution
        cat = row.get('Category', 'Unknown')
        analysis['categories'][cat] += 1

        # Complexity
        complexity = row.get('Complexity', 'unknown')
        analysis['complexity_distribution'][complexity] += 1

        # Maturity
        maturity = row.get('Maturity', 'unknown')
        analysis['maturity_distribution'][maturity] += 1

        # Priority
        try:
            priority = float(row.get('Priority', 0))
            priorities.append(priority)
            if priority > 50:
                analysis['high_priority_files'].append({
                    'file': row.get('File Path', ''),
                    'priority': priority,
                    'category': cat,
                    'description': row.get('Description', '')
                })
        except:
            pass

        # Top files by category
        analysis['top_files_by_category'][cat].append({
            'file': row.get('File Path', ''),
            'priority': float(row.get('Priority', 0)),
            'category': cat
        })

    # Priority statistics
    if priorities:
        analysis['priority_stats'] = {
            'average': sum(priorities) / len(priorities),
            'max': max(priorities),
            'min': min(priorities),
            'high_priority_count': sum(1 for p in priorities if p > 70),
            'medium_priority_count': sum(1 for p in priorities if 40 <= p <= 70),
            'low_priority_count': sum(1 for p in priorities if p < 40)
        }

    # Sort top files by category
    for cat in analysis['top_files_by_category']:
        analysis['top_files_by_category'][cat].sort(key=lambda x: x['priority'], reverse=True)
        analysis['top_files_by_category'][cat] = analysis['top_files_by_category'][cat][:10]

    # Generate organizational opportunities
    analysis['organizational_opportunities'] = generate_organizational_insights(analysis, rows)

    # Generate recommendations
    analysis['recommendations'] = generate_recommendations(analysis, rows)

    return analysis


def generate_organizational_insights(analysis: Dict, rows: List[Dict]) -> List[str]:
    """Generate organizational insights"""
    insights = []

    # Category-based organization
    for cat, count in analysis['categories'].most_common():
        if count > 10:
            insights.append(f"Create dedicated '{cat}' directory - {count} files need organization")

    # Priority-based organization
    high_priority = analysis['priority_stats'].get('high_priority_count', 0)
    if high_priority > 0:
        insights.append(f"Organize {high_priority} high-priority files (priority >70) first")

    # Complexity-based organization
    if analysis['complexity_distribution'].get('high', 0) > 0:
        insights.append(f"Separate {analysis['complexity_distribution']['high']} high-complexity files for review")

    # Maturity-based organization
    low_maturity = analysis['maturity_distribution'].get('low', 0)
    if low_maturity > 50:
        insights.append(f"Create 'Development/Experimental' area for {low_maturity} low-maturity files")

    high_maturity = analysis['maturity_distribution'].get('high', 0)
    if high_maturity > 0:
        insights.append(f"Promote {high_maturity} high-maturity files to 'Production' area")

    return insights


def generate_recommendations(analysis: Dict, rows: List[Dict]) -> List[str]:
    """Generate actionable recommendations"""
    recommendations = []

    total = analysis['total_files']

    # Category recommendations
    largest_category = analysis['categories'].most_common(1)[0]
    if largest_category[1] > total * 0.3:
        recommendations.append(
            f"Focus on organizing '{largest_category[0]}' category first ({largest_category[1]} files, "
            f"{largest_category[1]/total*100:.1f}% of total)"
        )

    # Priority-based recommendations
    avg_priority = analysis['priority_stats'].get('average', 0)
    if avg_priority < 30:
        recommendations.append(
            f"Average priority is {avg_priority:.1f} - consider reviewing categorization criteria"
        )

    # Complexity recommendations
    high_complexity = analysis['complexity_distribution'].get('high', 0)
    if high_complexity > 0:
        recommendations.append(
            f"Review and refactor {high_complexity} high-complexity files for maintainability"
        )

    # Maturity recommendations
    unknown_maturity = analysis['maturity_distribution'].get('unknown', 0)
    if unknown_maturity > total * 0.5:
        recommendations.append(
            f"Improve analysis for {unknown_maturity} files with unknown maturity (consider code metrics)"
        )

    return recommendations


def print_analysis_report(analysis: Dict, csv_file: Path):
    """Print comprehensive analysis report"""

    print("=" * 70)
    print("📊 CSV ANALYSIS & INSIGHTS REPORT")
    print("=" * 70)
    print(f"\n📁 Source: {csv_file.name}")
    print(f"📈 Total Files Analyzed: {analysis['total_files']}")

    # Category Distribution
    print("\n" + "=" * 70)
    print("📋 CATEGORY DISTRIBUTION")
    print("=" * 70)
    for cat, count in analysis['categories'].most_common():
        percentage = count / analysis['total_files'] * 100
        bar = "█" * int(percentage / 2)
        print(f"{cat:25} {count:4} files ({percentage:5.1f}%) {bar}")

    # Priority Statistics
    if analysis['priority_stats']:
        print("\n" + "=" * 70)
        print("📈 PRIORITY STATISTICS")
        print("=" * 70)
        stats = analysis['priority_stats']
        print(f"Average Priority:     {stats['average']:.2f}")
        print(f"Highest Priority:     {stats['max']:.2f}")
        print(f"Lowest Priority:      {stats['min']:.2f}")
        print(f"High Priority (>70):  {stats['high_priority_count']:4} files")
        print(f"Medium Priority (40-70): {stats['medium_priority_count']:4} files")
        print(f"Low Priority (<40):   {stats['low_priority_count']:4} files")

    # Quality Metrics
    print("\n" + "=" * 70)
    print("🎯 QUALITY METRICS")
    print("=" * 70)
    print("\nComplexity Distribution:")
    for complexity, count in analysis['complexity_distribution'].most_common():
        print(f"  {complexity:15} {count:4} files")

    print("\nMaturity Distribution:")
    for maturity, count in analysis['maturity_distribution'].most_common():
        print(f"  {maturity:15} {count:4} files")

    # Top Priority Files
    if analysis['high_priority_files']:
        print("\n" + "=" * 70)
        print("🏆 HIGH PRIORITY FILES (Top 20)")
        print("=" * 70)
        sorted_high = sorted(analysis['high_priority_files'], key=lambda x: x['priority'], reverse=True)
        for i, file_info in enumerate(sorted_high[:20], 1):
            filename = Path(file_info['file']).name
            print(f"{i:2}. [{file_info['priority']:6.2f}] {filename[:55]}")
            print(f"    Category: {file_info['category']} | {file_info['description'][:60]}")

    # Top Files by Category
    print("\n" + "=" * 70)
    print("📂 TOP FILES BY CATEGORY")
    print("=" * 70)
    for cat, files in sorted(analysis['top_files_by_category'].items(),
                            key=lambda x: len(x[1]), reverse=True):
        if files:
            print(f"\n{cat} ({len(files)} top files):")
            for i, file_info in enumerate(files[:5], 1):
                filename = Path(file_info['file']).name
                print(f"  {i}. [{file_info['priority']:6.2f}] {filename[:50]}")

    # Organizational Opportunities
    if analysis['organizational_opportunities']:
        print("\n" + "=" * 70)
        print("💡 ORGANIZATIONAL OPPORTUNITIES")
        print("=" * 70)
        for i, insight in enumerate(analysis['organizational_opportunities'], 1):
            print(f"{i}. {insight}")

    # Recommendations
    if analysis['recommendations']:
        print("\n" + "=" * 70)
        print("✅ RECOMMENDATIONS")
        print("=" * 70)
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"{i}. {rec}")

    print("\n" + "=" * 70)
    print("✅ Analysis Complete!")
    print("=" * 70)


def export_insights_json(analysis: Dict, output_file: Path):
    """Export insights as JSON"""
    # Convert Counter objects to dicts for JSON serialization
    export_data = {
        'total_files': analysis['total_files'],
        'categories': dict(analysis['categories']),
        'complexity_distribution': dict(analysis['complexity_distribution']),
        'maturity_distribution': dict(analysis['maturity_distribution']),
        'priority_stats': analysis['priority_stats'],
        'high_priority_files': analysis['high_priority_files'][:50],  # Limit to 50
        'organizational_opportunities': analysis['organizational_opportunities'],
        'recommendations': analysis['recommendations'],
        'top_files_by_category': {
            cat: files[:10] for cat, files in analysis['top_files_by_category'].items()
        }
    }

    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2, default=str)

    print(f"\n💾 Insights exported to: {output_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Analyze CSV and generate insights')
    parser.add_argument('csv_file', type=Path, help='CSV file to analyze')
    parser.add_argument('--output', type=Path, help='Output JSON file for insights')

    args = parser.parse_args()

    if not args.csv_file.exists():
        print(f"❌ CSV file not found: {args.csv_file}")
        return

    # Analyze CSV
    print("🔍 Analyzing CSV...")
    analysis = analyze_csv(args.csv_file)

    # Print report
    print_analysis_report(analysis, args.csv_file)

    # Export insights
    if args.output:
        export_insights_json(analysis, args.output)
    else:
        # Auto-generate output filename
        output_file = args.csv_file.parent / f"{args.csv_file.stem}_insights.json"
        export_insights_json(analysis, output_file)


if __name__ == '__main__':
    main()


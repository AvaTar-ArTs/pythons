#!/usr/bin/env python3
"""
🚀 Continue Analysis from CSV Insights
Uses CSV analysis to generate action plans and continue the analysis process
"""

import json
import csv
from pathlib import Path
from typing import Dict, List
from collections import defaultdict


def load_insights(insights_file: Path) -> Dict:
    """Load insights JSON"""
    with open(insights_file, 'r') as f:
        return json.load(f)


def generate_action_plan(insights: Dict) -> List[Dict]:
    """Generate actionable plan from insights"""
    actions = []

    total_files = insights['total_files']
    categories = insights['categories']

    # Action 1: Organize by category (largest first)
    largest_cat = max(categories.items(), key=lambda x: x[1])
    if largest_cat[1] > 50:
        actions.append({
            'priority': 'HIGH',
            'action': f"Organize {largest_cat[1]} '{largest_cat[0]}' files",
            'description': f"Create dedicated directory structure for {largest_cat[0]} category ({largest_cat[1]/total_files*100:.1f}% of files)",
            'steps': [
                f"Create base directory: ~/Documents/CsV/{largest_cat[0].replace('/', '-')}",
                "Subdivide by priority (High/Medium/Low)",
                "Further organize by project context if available",
                "Move files using the enhanced merge script"
            ]
        })

    # Action 2: Address high priority files
    high_priority = insights.get('high_priority_files', [])
    if high_priority:
        actions.append({
            'priority': 'HIGH',
            'action': f"Process {len(high_priority)} high-priority files",
            'description': "Focus on files with priority >50 first",
            'steps': [
                "Review each high-priority file",
                "Verify categorization is correct",
                "Apply improvement suggestions",
                "Move to appropriate organized location"
            ]
        })

    # Action 3: Improve analysis for unknown metrics
    if insights.get('maturity_distribution', {}).get('unknown', 0) > total_files * 0.5:
        actions.append({
            'priority': 'MEDIUM',
            'action': "Improve code analysis for unknown metrics",
            'description': f"{insights['maturity_distribution'].get('unknown', 0)} files have unknown maturity/complexity",
            'steps': [
                "Re-run analysis with enhanced code metrics",
                "Focus on Python files for AST analysis",
                "Improve file type detection",
                "Generate better quality assessments"
            ]
        })

    # Action 4: Create directory structure
    actions.append({
        'priority': 'HIGH',
        'action': "Create organized directory structure",
        'description': "Set up base structure based on category distribution",
        'steps': [
            "Create base: ~/Documents/CsV/",
            "Create category directories for top 5 categories",
            "Add Production/Experimental subdirectories",
            "Add project context subdirectories where applicable"
        ]
    })

    # Action 5: Process by priority tiers
    priority_stats = insights.get('priority_stats', {})
    if priority_stats:
        actions.append({
            'priority': 'MEDIUM',
            'action': "Process files in priority tiers",
            'description': "Organize files by priority level for efficient processing",
            'steps': [
                f"Process {priority_stats.get('high_priority_count', 0)} high-priority files first",
                f"Then {priority_stats.get('medium_priority_count', 0)} medium-priority files",
                f"Finally {priority_stats.get('low_priority_count', 0)} low-priority files"
            ]
        })

    return actions


def generate_directory_structure(insights: Dict, output_file: Path):
    """Generate recommended directory structure"""

    structure = {}
    base = "~/Documents/CsV"

    # Get top categories
    categories = sorted(insights['categories'].items(), key=lambda x: x[1], reverse=True)[:8]

    for cat, count in categories:
        if count > 5:  # Only create directories for categories with >5 files
            cat_dir = cat.replace('/', '-').replace(' ', '-')
            structure[cat_dir] = {
                'base_path': f"{base}/{cat_dir}",
                'file_count': count,
                'subdirectories': [
                    'Production',
                    'Experimental',
                    'Archive'
                ]
            }

    # Save structure
    with open(output_file, 'w') as f:
        json.dump(structure, f, indent=2)

    return structure


def print_action_plan(actions: List[Dict]):
    """Print formatted action plan"""
    print("\n" + "=" * 70)
    print("📋 ACTION PLAN")
    print("=" * 70)

    for i, action in enumerate(actions, 1):
        priority_icon = "🔴" if action['priority'] == 'HIGH' else "🟡" if action['priority'] == 'MEDIUM' else "🟢"
        print(f"\n{priority_icon} ACTION {i}: {action['action']} ({action['priority']} PRIORITY)")
        print(f"   {action['description']}")
        print("   Steps:")
        for step_num, step in enumerate(action['steps'], 1):
            print(f"     {step_num}. {step}")

    print("\n" + "=" * 70)


def generate_next_steps_summary(insights: Dict, actions: List[Dict]) -> str:
    """Generate summary of next steps"""
    summary = []

    summary.append("🎯 NEXT STEPS SUMMARY")
    summary.append("=" * 70)
    summary.append(f"\nTotal Files to Organize: {insights['total_files']}")
    summary.append(f"Categories Identified: {len(insights['categories'])}")
    summary.append(f"High Priority Actions: {sum(1 for a in actions if a['priority'] == 'HIGH')}")

    summary.append("\n📊 Key Statistics:")
    for cat, count in list(insights['categories'].items())[:5]:
        summary.append(f"  - {cat}: {count} files")

    summary.append("\n✅ Recommended Approach:")
    summary.append("  1. Review the action plan above")
    summary.append("  2. Create directory structure")
    summary.append("  3. Start with HIGH priority actions")
    summary.append("  4. Process files category by category")
    summary.append("  5. Use the enhanced merge script for automation")

    summary.append("\n🔄 To Continue Analysis:")
    summary.append("  - Run deep dive analysis on specific directories")
    summary.append("  - Re-analyze with enhanced code metrics")
    summary.append("  - Generate improved CSV with all features")

    return "\n".join(summary)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Continue analysis from CSV insights')
    parser.add_argument('insights_file', type=Path, help='Insights JSON file')
    parser.add_argument('--output-dir', type=Path, default=Path('~/analysis_reports').expanduser(),
                       help='Output directory for generated files')

    args = parser.parse_args()

    if not args.insights_file.exists():
        print(f"❌ Insights file not found: {args.insights_file}")
        return

    # Load insights
    print("📊 Loading insights...")
    insights = load_insights(args.insights_file)

    # Generate action plan
    print("📋 Generating action plan...")
    actions = generate_action_plan(insights)

    # Print action plan
    print_action_plan(actions)

    # Generate directory structure
    args.output_dir.mkdir(parents=True, exist_ok=True)
    structure_file = args.output_dir / "recommended_directory_structure.json"
    print(f"\n🏗️  Generating directory structure...")
    structure = generate_directory_structure(insights, structure_file)
    print(f"✅ Directory structure saved to: {structure_file}")

    # Print summary
    print("\n" + generate_next_steps_summary(insights, actions))

    # Save action plan
    action_plan_file = args.output_dir / "action_plan.json"
    with open(action_plan_file, 'w') as f:
        json.dump({
            'actions': actions,
            'insights_summary': {
                'total_files': insights['total_files'],
                'categories': insights['categories'],
                'priority_stats': insights.get('priority_stats', {})
            }
        }, f, indent=2)
    print(f"\n💾 Action plan saved to: {action_plan_file}")


if __name__ == '__main__':
    main()


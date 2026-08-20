#!/usr/bin/env python3
"""
Batch CSV Conversation Analyzer
Analyzes all CSV conversation files in a directory and generates comprehensive reports.
"""

import csv
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Tuple
import statistics


def extract_topics(content: str) -> List[str]:
    """Extract key topics from content."""
    topics = []
    content_lower = content.lower()

    # Common topic patterns
    topic_keywords = {
        'python': ['python', 'script', 'code', 'programming', 'function'],
        'ai': ['ai', 'artificial intelligence', 'model', 'claude', 'gpt'],
        'automation': ['automation', 'workflow', 'process', 'efficient'],
        'design': ['design', 'ui', 'ux', 'interface', 'layout', 'css'],
        'data': ['data', 'csv', 'json', 'database', 'organize', 'sort'],
        'web': ['web', 'html', 'website', 'browser', 'http'],
        'creative': ['creative', 'art', 'image', 'gallery', 'visual'],
        'social': ['social media', 'linkedin', 'instagram', 'twitter', 'youtube'],
        'business': ['business', 'strategy', 'growth', 'marketing', 'portfolio'],
        'technical': ['technical', 'api', 'server', 'terminal', 'command'],
    }

    for topic, keywords in topic_keywords.items():
        if any(keyword in content_lower for keyword in keywords):
            topics.append(topic)

    return topics[:5]  # Limit to 5 topics


def extract_action_items(content: str) -> List[str]:
    """Extract action items from content."""
    actions = []
    content_lower = content.lower()

    action_patterns = [
        ('created', r'created|built|generated|made'),
        ('organized', r'organized|sorted|structured|arranged'),
        ('analyzed', r'analyzed|examined|reviewed|studied'),
        ('improved', r'improved|enhanced|optimized|refined'),
        ('fixed', r'fixed|resolved|corrected|repaired'),
        ('converted', r'converted|transformed|changed|modified'),
    ]

    for action_name, pattern in action_patterns:
        if re.search(pattern, content_lower):
            actions.append(action_name)

    return actions[:3]


def classify_content_type(content: str, role: str) -> str:
    """Classify the type of content."""
    if role == 'Human':
        if len(content) < 50:
            return 'Request'
        elif '?' in content:
            return 'Question'
        return 'Query'

    content_lower = content.lower()

    if any(word in content_lower for word in ['analysis', 'analyze', 'analyzing', 'examined']):
        return 'Analysis'
    elif any(word in content_lower for word in ['created', 'generated', 'built', 'made']):
        return 'Creation'
    elif any(word in content_lower for word in ['explain', 'describe', 'summary', 'overview']):
        return 'Explanation'
    elif any(word in content_lower for word in ['fix', 'error', 'issue', 'problem']):
        return 'Troubleshooting'
    elif any(word in content_lower for word in ['improve', 'enhance', 'optimize', 'better']):
        return 'Improvement'
    else:
        return 'Response'


def analyze_single_csv(file_path: Path) -> Dict:
    """Analyze a single CSV file."""
    stats = {
        'filename': file_path.name,
        'filepath': str(file_path),
        'total_rows': 0,
        'human_messages': 0,
        'assistant_messages': 0,
        'total_content_length': 0,
        'max_content_length': 0,
        'min_content_length': float('inf'),
        'content_types': Counter(),
        'topics': Counter(),
        'actions': Counter(),
        'dates': [],
        'has_long_content': False,
        'conversation_turns': set(),
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                stats['total_rows'] += 1

                role = row.get('Role', '')
                content = row.get('Content', '')
                content_length = len(content)

                if role == 'Human':
                    stats['human_messages'] += 1
                elif role == 'Assistant':
                    stats['assistant_messages'] += 1
                    content_type = classify_content_type(content, role)
                    stats['content_types'][content_type] += 1

                    topics = extract_topics(content)
                    for topic in topics:
                        stats['topics'][topic] += 1

                    actions = extract_action_items(content)
                    for action in actions:
                        stats['actions'][action] += 1

                stats['total_content_length'] += content_length
                stats['max_content_length'] = max(stats['max_content_length'], content_length)
                if content_length > 0:
                    stats['min_content_length'] = min(stats['min_content_length'], content_length)

                if content_length > 1000:
                    stats['has_long_content'] = True

                turn = row.get('Turn', '')
                if turn:
                    stats['conversation_turns'].add(turn)

                timestamp = row.get('Timestamp', '')
                if timestamp:
                    try:
                        date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        stats['dates'].append(date)
                    except:
                        pass

        if stats['total_rows'] > 0:
            stats['avg_content_length'] = stats['total_content_length'] // stats['total_rows']
        else:
            stats['avg_content_length'] = 0

        if stats['min_content_length'] == float('inf'):
            stats['min_content_length'] = 0

        stats['conversation_turns'] = len(stats['conversation_turns'])

        if stats['dates']:
            stats['first_date'] = min(stats['dates']).isoformat()
            stats['last_date'] = max(stats['dates']).isoformat()
        else:
            stats['first_date'] = None
            stats['last_date'] = None

    except Exception as e:
        stats['error'] = str(e)

    return stats


def analyze_directory(directory_path: str) -> Dict:
    """Analyze all CSV files in a directory."""
    directory = Path(directory_path)
    csv_files = list(directory.glob('*.csv'))

    # Exclude already improved files
    csv_files = [f for f in csv_files if '_IMPROVED' not in f.name]

    print(f"📊 Found {len(csv_files)} CSV files to analyze...")

    all_stats = []
    overall_stats = {
        'total_files': len(csv_files),
        'total_rows': 0,
        'total_human_messages': 0,
        'total_assistant_messages': 0,
        'total_content_length': 0,
        'content_types': Counter(),
        'topics': Counter(),
        'actions': Counter(),
        'files_with_long_content': 0,
        'date_range': {'earliest': None, 'latest': None},
        'conversation_lengths': [],
    }

    for i, csv_file in enumerate(csv_files, 1):
        print(f"  Analyzing {i}/{len(csv_files)}: {csv_file.name}")
        stats = analyze_single_csv(csv_file)
        all_stats.append(stats)

        # Aggregate statistics
        overall_stats['total_rows'] += stats['total_rows']
        overall_stats['total_human_messages'] += stats['human_messages']
        overall_stats['total_assistant_messages'] += stats['assistant_messages']
        overall_stats['total_content_length'] += stats['total_content_length']

        for content_type, count in stats['content_types'].items():
            overall_stats['content_types'][content_type] += count

        for topic, count in stats['topics'].items():
            overall_stats['topics'][topic] += count

        for action, count in stats['actions'].items():
            overall_stats['actions'][action] += count

        if stats['has_long_content']:
            overall_stats['files_with_long_content'] += 1

        if stats.get('first_date'):
            if not overall_stats['date_range']['earliest'] or stats['first_date'] < overall_stats['date_range']['earliest']:
                overall_stats['date_range']['earliest'] = stats['first_date']

        if stats.get('last_date'):
            if not overall_stats['date_range']['latest'] or stats['last_date'] > overall_stats['date_range']['latest']:
                overall_stats['date_range']['latest'] = stats['last_date']

        overall_stats['conversation_lengths'].append(stats['conversation_turns'])

    overall_stats['avg_rows_per_file'] = overall_stats['total_rows'] / len(csv_files) if csv_files else 0
    overall_stats['avg_content_length'] = overall_stats['total_content_length'] / overall_stats['total_rows'] if overall_stats['total_rows'] > 0 else 0
    overall_stats['avg_conversation_length'] = statistics.mean(overall_stats['conversation_lengths']) if overall_stats['conversation_lengths'] else 0

    return {
        'individual_stats': all_stats,
        'overall_stats': overall_stats,
    }


def generate_report(analysis_results: Dict, output_dir: Path):
    """Generate comprehensive analysis reports."""
    output_dir.mkdir(exist_ok=True)

    # Overall statistics report
    overall = analysis_results['overall_stats']

    report = f"""# 📊 Conversations Directory - Comprehensive Analysis Report

## 📋 Overview

**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Directory:** `/Users/steven/claude/conversations`
**Total CSV Files Analyzed:** {overall['total_files']}

---

## 📈 Overall Statistics

### File Statistics
- **Total Files:** {overall['total_files']}
- **Total Rows:** {overall['total_rows']:,}
- **Average Rows per File:** {overall['avg_rows_per_file']:.1f}
- **Files with Long Content (>1000 chars):** {overall['files_with_long_content']}

### Message Statistics
- **Total Human Messages:** {overall['total_human_messages']:,}
- **Total Assistant Messages:** {overall['total_assistant_messages']:,}
- **Total Content Length:** {overall['total_content_length']:,} characters
- **Average Content Length:** {overall['avg_content_length']:.0f} characters
- **Average Conversation Length:** {overall['avg_conversation_length']:.1f} turns

### Date Range
- **Earliest Conversation:** {overall['date_range']['earliest'] or 'N/A'}
- **Latest Conversation:** {overall['date_range']['latest'] or 'N/A'}

---

## 🎯 Content Type Distribution

"""

    for content_type, count in overall['content_types'].most_common(10):
        percentage = (count / overall['total_assistant_messages'] * 100) if overall['total_assistant_messages'] > 0 else 0
        report += f"- **{content_type}:** {count} ({percentage:.1f}%)\n"

    report += f"""
---

## 🏷️ Topic Distribution (Top 15)

"""

    for topic, count in overall['topics'].most_common(15):
        report += f"- **{topic}:** {count} occurrences\n"

    report += f"""
---

## ⚡ Action Distribution (Top 10)

"""

    for action, count in overall['actions'].most_common(10):
        report += f"- **{action}:** {count} occurrences\n"

    report += f"""
---

## 📊 File-Level Insights

### Files Needing Improvement
"""

    # Find files with long content
    long_content_files = [
        s for s in analysis_results['individual_stats']
        if s.get('has_long_content', False)
    ]

    report += f"- **Files with Long Content:** {len(long_content_files)}\n"
    for stats in sorted(long_content_files, key=lambda x: x.get('max_content_length', 0), reverse=True)[:10]:
        report += f"  - `{stats['filename']}` (max: {stats.get('max_content_length', 0):,} chars)\n"

    report += f"""
### Largest Conversations
"""

    large_conversations = sorted(
        analysis_results['individual_stats'],
        key=lambda x: x.get('total_rows', 0),
        reverse=True
    )[:10]

    for stats in large_conversations:
        report += f"- `{stats['filename']}`: {stats.get('total_rows', 0)} rows, {stats.get('conversation_turns', 0)} turns\n"

    report += f"""
---

## 💡 Recommendations

### 1. Content Optimization
- {len(long_content_files)} files contain very long content fields (>1000 characters)
- Consider condensing these for better readability
- Use the `csv_analyzer.py` script to improve these files

### 2. Metadata Enhancement
- Add metadata columns (Content_Length, Content_Type, Key_Topics, Action_Items)
- This will improve searchability and analysis capabilities

### 3. Organization
- Consider grouping conversations by topic
- Create topic-based indexes for easier navigation
- Build a master conversation index

### 4. Automation
- Use batch processing for consistent formatting
- Automate metadata extraction
- Create standardized templates

---

## 🔧 Tools Available

1. **`csv_analyzer.py`** - Analyze and improve individual CSV files
2. **`batch_csv_analyzer.py`** - Batch process all files (this script)
3. **Improved CSV format** - Enhanced structure with metadata columns

---

*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    # Write report
    report_path = output_dir / 'CONVERSATIONS_ANALYSIS_REPORT.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    # Write JSON data
    json_path = output_dir / 'conversations_analysis_data.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2, default=str)

    # Write detailed file list
    details_path = output_dir / 'CONVERSATIONS_DETAILED_LIST.md'
    details = "# 📋 Detailed File Analysis\n\n"
    details += "## All Files Analyzed\n\n"
    details += "| Filename | Rows | Human | Assistant | Avg Length | Topics | Actions |\n"
    details += "|----------|------|-------|-----------|------------|--------|---------|\n"

    for stats in sorted(analysis_results['individual_stats'], key=lambda x: x.get('filename', '')):
        topics_str = ', '.join([t for t, _ in stats['topics'].most_common(3)])
        actions_str = ', '.join([a for a, _ in stats['actions'].most_common(2)])
        details += f"| {stats['filename']} | {stats.get('total_rows', 0)} | {stats.get('human_messages', 0)} | {stats.get('assistant_messages', 0)} | {stats.get('avg_content_length', 0)} | {topics_str[:30]} | {actions_str[:20]} |\n"

    with open(details_path, 'w', encoding='utf-8') as f:
        f.write(details)

    print(f"\n✅ Reports generated:")
    print(f"   - {report_path}")
    print(f"   - {json_path}")
    print(f"   - {details_path}")

    return report_path, json_path, details_path


def main():
    """Main function."""
    import sys

    directory = sys.argv[1] if len(sys.argv) > 1 else '/Users/steven/claude/conversations'
    output_dir = Path(directory) / 'analysis_reports'

    print(f"🚀 Starting batch analysis of: {directory}")
    print("=" * 60)

    results = analyze_directory(directory)

    print("\n" + "=" * 60)
    print("📊 Generating reports...")

    report_path, json_path, details_path = generate_report(results, output_dir)

    print("\n" + "=" * 60)
    print("✅ Analysis Complete!")
    print(f"\n📁 Reports saved to: {output_dir}")
    print(f"\n📈 Summary:")
    print(f"   - Total files: {results['overall_stats']['total_files']}")
    print(f"   - Total rows: {results['overall_stats']['total_rows']:,}")
    print(f"   - Total messages: {results['overall_stats']['total_human_messages'] + results['overall_stats']['total_assistant_messages']:,}")


if __name__ == '__main__':
    main()


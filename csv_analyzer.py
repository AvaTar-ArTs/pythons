#!/usr/bin/env python3
"""
CSV Conversation Analyzer & Improver
Analyzes and improves CSV conversation files with better structure and metadata.
"""

import csv
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


def extract_topics(content: str) -> str:
    """Extract key topics from content."""
    topics = []

    # Common topic patterns
    topic_patterns = [
        r'(?:WhisperText|prompts?|content)',
        r'(?:organiz(?:ation|e|ing))',
        r'(?:social media|LinkedIn|Instagram|Twitter|X)',
        r'(?:YouTube|SEO)',
        r'(?:typography|design)',
        r'(?:automation|workflow)',
    ]

    content_lower = content.lower()
    for pattern in topic_patterns:
        if re.search(pattern, content_lower, re.IGNORECASE):
            topic = pattern.replace('(?:', '').replace(')', '').replace('|', ', ')
            topics.append(topic)

    return ', '.join(topics[:5]) if topics else 'General'


def extract_action_items(content: str) -> str:
    """Extract action items from content."""
    actions = []

    # Look for action verbs
    action_patterns = [
        r'created (\d+) (?:file|version|document)',
        r'organized (?:by|into)',
        r'sorted (?:by|into)',
        r'added (?:reference|table|matrix)',
        r'generated',
        r'extracted',
    ]

    for pattern in action_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            actions.append(pattern.replace('(?:', '').replace(')', '').replace('|', ', '))

    return ', '.join(actions[:3]) if actions else 'Analysis completed'


def classify_content_type(content: str, role: str) -> str:
    """Classify the type of content."""
    if role == 'Human':
        if len(content) < 50:
            return 'Request'
        return 'Query'

    content_lower = content.lower()

    if any(word in content_lower for word in ['analysis', 'analyze', 'analyzing']):
        return 'Analysis & Organization'
    elif any(word in content_lower for word in ['created', 'generated', 'built']):
        return 'Creation & Generation'
    elif any(word in content_lower for word in ['explain', 'describe', 'summary']):
        return 'Explanation'
    else:
        return 'Response'


def condense_content(content: str, max_length: int = 800) -> str:
    """Condense content while preserving key information."""
    if len(content) <= max_length:
        return content

    # Remove code blocks with "not supported" messages
    content = re.sub(r'```[^`]*This block is not supported[^`]*```', '', content, flags=re.DOTALL)

    # Remove excessive markdown formatting
    content = re.sub(r'#{4,}', '##', content)  # Limit heading depth

    # Extract key sections
    sections = []

    # Look for structured sections
    if '##' in content:
        parts = re.split(r'##+', content)
        for part in parts[:5]:  # Keep first 5 sections
            if part.strip():
                sections.append(part.strip()[:200])  # Limit section length

    if sections:
        condensed = '\n\n'.join(sections)
        if len(condensed) <= max_length:
            return condensed

    # Fallback: truncate with ellipsis
    return content[:max_length-3] + '...'


def analyze_csv(input_path: str, output_path: str = None) -> Dict:
    """Analyze and improve a CSV conversation file."""
    if output_path is None:
        output_path = input_path.replace('.csv', '_IMPROVED.csv')

    rows = []
    stats = {
        'total_rows': 0,
        'human_messages': 0,
        'assistant_messages': 0,
        'total_content_length': 0,
        'average_content_length': 0,
    }

    # Read original CSV
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            stats['total_rows'] += 1

            if row['Role'] == 'Human':
                stats['human_messages'] += 1
            elif row['Role'] == 'Assistant':
                stats['assistant_messages'] += 1

            content_length = len(row.get('Content', ''))
            stats['total_content_length'] += content_length

    if stats['total_rows'] > 0:
        stats['average_content_length'] = stats['total_content_length'] // stats['total_rows']

    # Create improved rows
    improved_rows = []
    fieldnames = ['Turn', 'Role', 'Content', 'Timestamp', 'Platform',
                  'Content_Length', 'Content_Type', 'Key_Topics', 'Action_Items']

    for row in rows:
        content = row.get('Content', '')
        role = row.get('Role', '')

        # Extract metadata
        content_length = len(content)
        content_type = classify_content_type(content, role)
        key_topics = extract_topics(content) if role == 'Assistant' else ''
        action_items = extract_action_items(content) if role == 'Assistant' else ''

        # Condense long assistant responses
        if role == 'Assistant' and content_length > 800:
            content = condense_content(content)
            content_length = len(content)

        improved_row = {
            'Turn': row.get('Turn', ''),
            'Role': role,
            'Content': content,
            'Timestamp': row.get('Timestamp', ''),
            'Platform': row.get('Platform', ''),
            'Content_Length': str(content_length),
            'Content_Type': content_type,
            'Key_Topics': key_topics,
            'Action_Items': action_items,
        }

        improved_rows.append(improved_row)

    # Write improved CSV
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(improved_rows)

    stats['output_file'] = output_path
    return stats


def main():
    """Main function to run the analyzer."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python csv_analyzer.py <input_csv_file> [output_csv_file]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not Path(input_file).exists():
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    print(f"📊 Analyzing: {input_file}")
    stats = analyze_csv(input_file, output_file)

    print("\n✅ Analysis Complete!")
    print(f"📁 Output file: {stats['output_file']}")
    print(f"📈 Statistics:")
    print(f"   - Total rows: {stats['total_rows']}")
    print(f"   - Human messages: {stats['human_messages']}")
    print(f"   - Assistant messages: {stats['assistant_messages']}")
    print(f"   - Average content length: {stats['average_content_length']} characters")


if __name__ == '__main__':
    main()


#!/usr/bin/env python3
"""
Create Notion pages/databases from CSV migration files
"""

import csv
import json
from pathlib import Path

def format_csv_for_notion(csv_file: Path):
    """Read CSV and format content for Notion"""
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Create formatted markdown table
    if not rows:
        return "No data found"
    
    # Get headers
    headers = list(rows[0].keys())
    
    # Create markdown table
    md_lines = []
    md_lines.append("| " + " | ".join(headers) + " |")
    md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    
    for row in rows[:100]:  # Limit to 100 rows for display
        values = [str(row.get(h, ''))[:100] for h in headers]  # Truncate long values
        md_lines.append("| " + " | ".join(values) + " |")
    
    if len(rows) > 100:
        md_lines.append(f"\n*... and {len(rows) - 100} more rows*")
    
    return "\n".join(md_lines)

def create_summary_page_content():
    """Create content for migration summary page"""
    
    csv_file = Path.home() / 'analysis_reports' / 'migration_summary.csv'
    if not csv_file.exists():
        return "# Migration Summary\n\nCSV file not found."
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    content = "# 📋 Migration Summary\n\n"
    content += "File migration overview based on analysis of 500 files.\n\n"
    content += "## Categories\n\n"
    content += "| Category | File Count | CSV File |\n"
    content += "| --- | --- | --- |\n"
    
    for row in rows:
        content += f"| {row['Category']} | {row['File Count']} | `{row['CSV File']}` |\n"
    
    content += f"\n\n**Total Files:** {sum(int(r['File Count']) for r in rows)}\n"
    content += f"**Total Categories:** {len(rows)}\n"
    
    return content

if __name__ == '__main__':
    summary_content = create_summary_page_content()
    print(summary_content)


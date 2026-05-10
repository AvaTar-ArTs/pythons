"""
Summary of generate_migration_csv.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import re
import csv
import os

report_path = './advanced_analysis_report/ADVANCED_CONTENT_ANALYSIS_20260117_073313.md'
if not os.path.exists(report_path):
    print(f"Error: {report_path} not found")
    exit(1)

with open(report_path, 'r') as f:
    content = f.read()

# Split by sections to handle categories
sections = re.split(r'### (.*?)\s\(.*?\)', content)
migration_data = []

# sections[0] is header, then pairs of (Category, Content)
for i in range(1, len(sections), 2):
    category = sections[i]
    body = sections[i+1]
    
    # Find all file blocks in this section
    # Matches #### filename and then the first suggested destination
    files = re.findall(r'#### (.*?)\n.*?Path:\*\* `(.*?)`.*?\n- \*\*Suggested Destinations:\*\*\n\s+-\s+`(.*?)`', body, re.DOTALL)
    for name, path, dest in files:
        migration_data.append({
            'Filename': name,
            'CurrentPath': path,
            'Category': category,
            'SuggestedDestination': dest
        })

with open('migration_mapping.csv', 'w', newline='') as csvfile:
    fieldnames = ['Filename', 'CurrentPath', 'Category', 'SuggestedDestination']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow({f: f for f in fieldnames}) # Manual header to avoid issues
    for data in migration_data:
        writer.writerow(data)

print(f"Successfully created migration_mapping.csv with {len(migration_data)} entries.")

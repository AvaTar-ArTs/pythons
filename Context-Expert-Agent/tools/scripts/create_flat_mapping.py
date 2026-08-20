#!/usr/bin/env python3
"""
Create flat reorganization mapping - NO nested folders
"""

import json
import csv
from collections import defaultdict

# Load analysis
with open('directory_analysis.json') as f:
    data = json.load(f)

# Create mapping - FLAT structure only
mapping = []

# Root level directories and files
root_dirs = [
    'heavenlyHands', 'BUSINESS', 'BUSINESS_PROJECTS', 'DEVELOPMENT',
    'CODE_PROJECTS', 'AI_TOOLS', 'UTILITIES_TOOLS', 'automation',
    'CLIENT_PROJECTS', 'AvaTar-ArTs.github.io', 'ai-sites',
    'SEO_MARKETING', 'CONTENT_ASSETS', 'DOCUMENTATION', 'docs',
    'docs-demos', 'docs-sphinx', 'Master_Documentation_Index',
    'ARCHIVES_BACKUPS', 'DATA_ANALYTICS', 'other', 'OTHER_MISC'
]

# Root level files
root_files = [
    'analyze_income_opportunities.py', 'deepdive_analysis.py',
    'generate_sorted_exports.py', 'master_revenue_dashboard.py',
    'organize_files.sh', 'INCOME_OPPORTUNITIES.csv',
    'ADDITIONAL_OPPORTUNITIES.csv', 'SORTED_QUICK_WINS.csv',
    'SORTED_BY_ROI.csv', 'SORTED_BY_REVENUE.csv',
    'SORTED_BY_READINESS.csv', 'READY_TO_IMPLEMENT.csv',
    'SUMMARY_BY_CATEGORY.csv', 'SUMMARY_BY_STATUS.csv',
    'reanalysis_output.txt', 'README.md',
    # All .md files
    'ORGANIZATION_ANALYSIS_AND_PLAN.md', 'REORGANIZATION_PLAN.md',
    'FINAL_ORGANIZATION_SUMMARY.md', 'ORGANIZATION_COMPLETE.md',
    'ORGANIZATION_FINAL_SUMMARY.txt', 'INCOME_OPPORTUNITIES_INDEX.md',
    'HTML_PDF_INCOME_OPPORTUNITIES.md', 'QUICK_ACTION_PLAN.md',
    'TOP_OPPORTUNITIES_IMPLEMENTATION_GUIDE.md', 'SEO_CONSOLIDATION_PLAN.md',
    'DOCUMENTATION_STYLES_COMPLETE_2026-01-02.md',
    'SPHINX_DOCS_COMPLETE_2026-01-02.md', 'QWEN.md',
    'analysis_and_suggestions.md', 'comprehensive_improvements_suggestions.html',
    'deepdive_index.md', 'directory_index.csv',
    'home_vs_external_comparison.md', 'WORKSPACE_CONSOLIDATION_HANDOFF.md',
    'EXPORT_SUMMARY.txt'
]

# Map directories - FLAT (directly into main folder, no nesting)
for dir_name in root_dirs:
    # Determine category based on name
    name_lower = dir_name.lower()
    if any(x in name_lower for x in ['business', 'client', 'seo', 'heavenly']):
        new_path = f'active/{dir_name}'
        category = 'active'
    elif any(x in name_lower for x in ['dev', 'code', 'ai_tools', 'utilities', 'automation']):
        new_path = f'code/{dir_name}'
        category = 'code'
    elif any(x in name_lower for x in ['content', 'asset']):
        new_path = f'content/{dir_name}'
        category = 'content'
    elif any(x in name_lower for x in ['doc', 'sphinx', 'master_documentation']):
        new_path = f'docs/{dir_name}'
        category = 'docs'
    elif any(x in name_lower for x in ['data', 'analytics']):
        new_path = f'data/{dir_name}'
        category = 'data'
    elif any(x in name_lower for x in ['archive', 'backup', 'other', 'misc']):
        new_path = f'archive/{dir_name}'
        category = 'archive'
    elif 'github.io' in name_lower or 'ai-sites' in name_lower:
        new_path = f'active/{dir_name}'
        category = 'active'
    else:
        new_path = f'active/{dir_name}'
        category = 'active'

    mapping.append({
        'old_path': dir_name + '/',
        'new_path': new_path + '/',
        'category': category,
        'size_mb': 0,
        'file_count': 0,
        'notes': 'Root level directory'
    })

# Map files - FLAT (directly into main folder)
for file_name in root_files:
    name_lower = file_name.lower()
    if any(x in name_lower for x in ['income', 'revenue', 'opportunities', 'sorted', 'ready', 'summary']):
        new_path = f'active/{file_name}'
        category = 'active'
    elif any(x in name_lower for x in ['.py', '.sh']) and 'analyze' in name_lower:
        new_path = f'active/{file_name}'
        category = 'active'
    elif any(x in name_lower for x in ['.md', '.html', '.txt']) or 'index' in name_lower:
        new_path = f'docs/{file_name}'
        category = 'docs'
    else:
        new_path = f'active/{file_name}'
        category = 'active'

    mapping.append({
        'old_path': file_name,
        'new_path': new_path,
        'category': category,
        'size_mb': 0,
        'file_count': 1,
        'notes': 'Root level file'
    })

# Write CSV
with open('reorganization_mapping.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['old_path', 'new_path', 'category', 'size_mb', 'file_count', 'notes'])
    writer.writeheader()
    writer.writerows(mapping)

print(f'✅ Created FLAT mapping CSV with {len(mapping)} entries')
print('Structure: Only 4 main folders (active, code, content, docs, data, archive)')
print('No nested subfolders!')


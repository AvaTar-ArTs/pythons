#!/usr/bin/env python3
"""
SEO-DRIVEN MULTI-CSV GENERATOR
Creates multiple CSVs organized by TOP RISING SEO TRENDS (2025)

Based on Top 1-5% Rising Keywords:
- AI Workflow Automation (+460%)
- Generative Automation (+470%)
- AI Art Workflow (+440%)
- Image Prompt Generator (+420%)
- Creative Automation (+380%)
- AI Content Pipeline (+350%)
- Automated SEO Optimization (+320%)
"""
import csv
import ast
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import re

# SEO TREND DEFINITIONS (Top 1-5% Rising 2025)
SEO_TRENDS = {
    'AI_Workflow_Automation': {
        'keywords': ['workflow', 'automation', 'pipeline', 'orchestrator', 'scheduler', 'n8n', 'zapier'],
        'growth': '+460%',
        'monthly_searches': '12,000-18,000',
        'priority': 1
    },
    'Generative_Automation': {
        'keywords': ['generative', 'ai', 'openai', 'claude', 'gemini', 'gpt', 'llm', 'generate'],
        'growth': '+470%',
        'monthly_searches': '15,000-22,000',
        'priority': 1
    },
    'AI_Art_Workflow': {
        'keywords': ['image', 'art', 'dalle', 'midjourney', 'stable', 'diffusion', 'leonardo', 'ideogram'],
        'growth': '+440%',
        'monthly_searches': '10,000-15,000',
        'priority': 2
    },
    'Image_Prompt_Generator': {
        'keywords': ['prompt', 'prompt_engineering', 'image_generation', 'text_to_image'],
        'growth': '+420%',
        'monthly_searches': '8,000-12,000',
        'priority': 2
    },
    'Creative_Automation': {
        'keywords': ['creative', 'content', 'media', 'social', 'instagram', 'youtube', 'music'],
        'growth': '+380%',
        'monthly_searches': '14,000-20,000',
        'priority': 2
    },
    'AI_Content_Pipeline': {
        'keywords': ['content', 'article', 'blog', 'medium', 'writing', 'transcription', 'voice'],
        'growth': '+350%',
        'monthly_searches': '9,000-14,000',
        'priority': 3
    },
    'Automated_SEO': {
        'keywords': ['seo', 'optimization', 'keyword', 'metadata', 'schema', 'rank'],
        'growth': '+320%',
        'monthly_searches': '11,000-16,000',
        'priority': 1
    }
}

def count_lines(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except:
        return 0

def extract_content_features(filepath):
    """Extract docstring, imports, classes, functions"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            tree = ast.parse(content)
            
        docstring = ast.get_docstring(tree) or ""
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        
        return docstring, imports, classes, functions, content.lower()
    except:
        return "", [], [], [], ""

def match_seo_trends(filepath, docstring, imports, content):
    """Match file to SEO trends based on content"""
    matches = []
    
    path_str = str(filepath).lower()
    doc_lower = docstring.lower()
    imports_str = ' '.join(imports).lower()
    
    combined_text = f"{path_str} {doc_lower} {imports_str} {content[:1000]}"
    
    for trend_name, trend_data in SEO_TRENDS.items():
        keyword_matches = sum(1 for kw in trend_data['keywords'] if kw in combined_text)
        
        if keyword_matches >= 2:  # Need at least 2 keyword matches
            matches.append({
                'trend': trend_name,
                'keyword_matches': keyword_matches,
                'growth': trend_data['growth'],
                'monthly_searches': trend_data['monthly_searches'],
                'priority': trend_data['priority']
            })
    
    # Sort by keyword matches and priority
    matches.sort(key=lambda x: (x['keyword_matches'], -x['priority']), reverse=True)
    return matches

def calculate_seo_score(matches, lines, num_classes, num_functions):
    """Calculate SEO marketability score (0-100)"""
    if not matches:
        return 0
    
    # Base score from best trend match
    best_match = matches[0]
    base_score = best_match['keyword_matches'] * 10
    
    # Priority bonus
    priority_bonus = (4 - best_match['priority']) * 5
    
    # Complexity bonus
    complexity_score = min(30, (lines / 100) + (num_classes * 2) + (num_functions))
    
    # Multi-trend bonus
    multi_trend_bonus = min(15, (len(matches) - 1) * 5)
    
    total_score = min(100, base_score + priority_bonus + complexity_score + multi_trend_bonus)
    return round(total_score, 1)

def estimate_market_value(seo_score, matches):
    """Estimate monthly market value based on SEO score and trends"""
    if seo_score >= 80:
        return "$2,000-$5,000/month"
    elif seo_score >= 60:
        return "$1,000-$2,500/month"
    elif seo_score >= 40:
        return "$500-$1,500/month"
    elif seo_score >= 20:
        return "$200-$800/month"
    else:
        return "$50-$300/month"

print("🔍 SEO-DRIVEN ANALYSIS: Scanning Python files...")

# Find all Python files
base_paths = [
    Path('/Users/steven/pythons'),
    Path('/Users/steven/workspace/advanced_toolkit')
]

all_files = []
for base_path in base_paths:
    if base_path.exists():
        all_files.extend(base_path.rglob('*.py'))

print(f"📁 Found {len(all_files)} Python files")

# Analyze each file
results = []
trend_buckets = defaultdict(list)

for idx, filepath in enumerate(all_files, 1):
    if idx % 100 == 0:
        print(f"  Analyzed {idx}/{len(all_files)} files...")
    
    lines = count_lines(filepath)
    if lines == 0:
        continue
    
    docstring, imports, classes, functions, content = extract_content_features(filepath)
    seo_matches = match_seo_trends(filepath, docstring, imports, content)
    
    if not seo_matches:
        continue  # Skip files with no SEO trend matches
    
    seo_score = calculate_seo_score(seo_matches, lines, len(classes), len(functions))
    market_value = estimate_market_value(seo_score, seo_matches)
    
    # Get relative path
    try:
        rel_path = filepath.relative_to(Path.home())
    except:
        rel_path = filepath
    
    result = {
        'filepath': str(rel_path),
        'filename': filepath.name,
        'parent_folder': filepath.parent.name,
        'lines': lines,
        'num_classes': len(classes),
        'num_functions': len(functions),
        'primary_trend': seo_matches[0]['trend'],
        'trend_growth': seo_matches[0]['growth'],
        'monthly_searches': seo_matches[0]['monthly_searches'],
        'keyword_matches': seo_matches[0]['keyword_matches'],
        'all_trends': '; '.join([m['trend'] for m in seo_matches]),
        'seo_score': seo_score,
        'market_value_estimate': market_value,
        'priority': seo_matches[0]['priority'],
        'docstring': docstring.replace('\n', ' ').replace(',', ';')[:150] if docstring else '',
        'key_classes': ', '.join(classes[:3]),
        'file_size_kb': filepath.stat().st_size // 1024,
        'last_modified': datetime.fromtimestamp(filepath.stat().st_mtime).strftime('%Y-%m-%d')
    }
    
    results.append(result)
    
    # Add to trend-specific buckets
    for match in seo_matches:
        trend_buckets[match['trend']].append(result)

print(f"\n📊 Total files with SEO trend matches: {len(results)}")

# Sort by SEO score descending
results.sort(key=lambda x: x['seo_score'], reverse=True)

# OUTPUT 1: MASTER SEO-DRIVEN INVENTORY
output_dir = Path('/Users/steven/csv_outputs')
output_dir.mkdir(exist_ok=True)

master_path = output_dir / 'SEO_MASTER_INVENTORY.csv'
with open(master_path, 'w', newline='', encoding='utf-8') as f:
    if results:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

print(f"✅ Created: {master_path}")

# OUTPUT 2-8: INDIVIDUAL TREND CSVs
for trend_name, trend_files in trend_buckets.items():
    trend_files.sort(key=lambda x: x['seo_score'], reverse=True)
    
    trend_path = output_dir / f'{trend_name}_ASSETS.csv'
    with open(trend_path, 'w', newline='', encoding='utf-8') as f:
        if trend_files:
            writer = csv.DictWriter(f, fieldnames=trend_files[0].keys())
            writer.writeheader()
            writer.writerows(trend_files)
    
    print(f"✅ Created: {trend_name}_ASSETS.csv ({len(trend_files)} files)")

# OUTPUT 9: HIGH-VALUE OPPORTUNITIES (SEO Score >= 60)
high_value = [r for r in results if r['seo_score'] >= 60]
if high_value:
    hv_path = output_dir / 'HIGH_VALUE_SEO_OPPORTUNITIES.csv'
    with open(hv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=high_value[0].keys())
        writer.writeheader()
        writer.writerows(high_value)
    print(f"✅ Created: HIGH_VALUE_SEO_OPPORTUNITIES.csv ({len(high_value)} files)")

# SUMMARY REPORT
print("\n" + "="*70)
print("📊 SEO-DRIVEN ANALYSIS SUMMARY")
print("="*70)

for trend_name, trend_data in sorted(SEO_TRENDS.items(), key=lambda x: x[1]['priority']):
    count = len(trend_buckets.get(trend_name, []))
    total_lines = sum(f['lines'] for f in trend_buckets.get(trend_name, []))
    avg_score = sum(f['seo_score'] for f in trend_buckets.get(trend_name, [])) / count if count > 0 else 0
    
    print(f"\n🔥 {trend_name}")
    print(f"   Growth: {trend_data['growth']} | Searches: {trend_data['monthly_searches']}/month")
    print(f"   Matched Files: {count} | Total Lines: {total_lines:,} | Avg SEO Score: {avg_score:.1f}")

print(f"\n💰 High-Value Opportunities (SEO Score >= 60): {len(high_value)} files")

# Top 10 by SEO Score
print("\n🎯 TOP 10 SEO-OPTIMIZED ASSETS:")
for i, r in enumerate(results[:10], 1):
    print(f"  {i}. {r['filename'][:50]}")
    print(f"     Score: {r['seo_score']} | Trend: {r['primary_trend']} | Value: {r['market_value_estimate']}")

print("\n✅ SEO-DRIVEN CSV GENERATION COMPLETE!")

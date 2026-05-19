#!/usr/bin/env python3
"""
AVATARARTS Advanced Parent-Child Content Analyzer
Creates comprehensive CSV mapping with content-aware intelligence and functional categorization
"""

import csv
import os
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import hashlib
import pandas as pd


def get_file_hash(filepath: str) -> str:
    """Generate a hash for file content to identify duplicates"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return "unknown"


def analyze_file_content(filepath: str) -> dict:
    """Analyze file content to determine function and business value"""
    analysis = {
        'function_classification': 'MISCELLANEOUS',
        'business_value': 0,
        'integration_potential': False,
        'content_keywords': [],
        'primary_purpose': 'unknown',
        'ai_tool_type': None,
        'revenue_potential': False,
        'automation_potential': False
    }
    
    try:
        # Get file extension
        ext = Path(filepath).suffix.lower()
        
        # For text-based files, analyze content
        if ext in ['.py', '.sh', '.js', '.ts', '.md', '.txt', '.json', '.csv', '.html', '.css']:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2000).lower()  # Read first 2000 chars for analysis
                
            # Function classification based on content
            if any(keyword in content for keyword in ['automation', 'automate', 'workflow', 'orchestrate', 'bot', 'agent']):
                analysis['function_classification'] = 'AUTOMATION'
                analysis['automation_potential'] = True
                analysis['business_value'] = 8
            elif any(keyword in content for keyword in ['revenue', 'income', 'profit', 'monetiz', 'launch', 'sales']):
                analysis['function_classification'] = 'REVENUE'
                analysis['revenue_potential'] = True
                analysis['business_value'] = 10
            elif any(keyword in content for keyword in ['dashboard', 'analytics', 'intelligence', 'report', 'metric', 'kpi']):
                analysis['function_classification'] = 'BUSINESS_INTELLIGENCE'
                analysis['business_value'] = 7
            elif any(keyword in content for keyword in ['ai', 'ml', 'model', 'neural', 'tensor', 'torch', 'openai', 'claude', 'gemini', 'grok', 'ollama']):
                analysis['function_classification'] = 'AI_ML'
                analysis['ai_tool_type'] = 'ai_ml'
                analysis['business_value'] = 9
            elif any(keyword in content for keyword in ['data', 'process', 'csv', 'pandas', 'json', 'xml', 'transform', 'analyze']):
                analysis['function_classification'] = 'DATA_PROCESSING'
                analysis['business_value'] = 6
            elif any(keyword in content for keyword in ['api', 'endpoint', 'client', 'integration', 'request', 'auth']):
                analysis['function_classification'] = 'API_INTEGRATION'
                analysis['integration_potential'] = True
                analysis['business_value'] = 6
            elif any(keyword in content for keyword in ['dev', 'tool', 'util', 'script', 'build', 'test', 'debug']):
                analysis['function_classification'] = 'DEVELOPMENT_TOOLS'
                analysis['business_value'] = 4
            elif ext in ['.md', '.txt'] or any(keyword in content for keyword in ['doc', 'manual', 'guide', 'tutorial']):
                analysis['function_classification'] = 'DOCUMENTATION'
                analysis['business_value'] = 5
            elif any(keyword in content for keyword in ['media', 'audio', 'video', 'image', 'mp3', 'mp4', 'jpg', 'png']):
                analysis['function_classification'] = 'MEDIA_PROCESSING'
                analysis['business_value'] = 5
            elif any(keyword in content for keyword in ['portfolio', 'invest', 'finance', 'stock', 'trade', 'asset']):
                analysis['function_classification'] = 'PORTFOLIO_MANAGEMENT'
                analysis['business_value'] = 7
            elif any(keyword in content for keyword in ['content', 'create', 'design', 'write', 'copy']):
                analysis['function_classification'] = 'CONTENT_CREATION'
                analysis['business_value'] = 5
            elif any(keyword in content for keyword in ['seo', 'marketing', 'campaign', 'keyword', 'rank', 'traffic']):
                analysis['function_classification'] = 'SEO_MARKETING'
                analysis['business_value'] = 6
            elif any(keyword in content for keyword in ['archiv', 'backup', 'old', 'historical', 'deprecated']):
                analysis['function_classification'] = 'ARCHIVES'
                analysis['business_value'] = 3
            elif any(keyword in content for keyword in ['config', 'setting', 'env', 'environment']):
                analysis['function_classification'] = 'CONFIGURATIONS'
                analysis['business_value'] = 4
            else:
                analysis['function_classification'] = 'UTILITIES'
                analysis['business_value'] = 4
        
        # Extract content keywords
        keywords = []
        if ext == '.py':
            # Python-specific analysis
            keywords.extend(re.findall(r'def (\w+)', content))
            keywords.extend(re.findall(r'class (\w+)', content))
            keywords.extend(re.findall(r'import (\w+)', content))
            keywords.extend(re.findall(r'from (\w+)', content))
        elif ext == '.md':
            # Markdown-specific analysis
            keywords.extend(re.findall(r'# (.+)', content))
            keywords.extend(re.findall(r'\*\*(.+?)\*\*', content))
            keywords.extend(re.findall(r'## (.+)', content))
        
        analysis['content_keywords'] = list(set(keywords))[:10]  # Top 10 unique keywords
        
        # Determine primary purpose
        if 'automation' in content:
            analysis['primary_purpose'] = 'automation'
        elif 'revenue' in content or 'income' in content:
            analysis['primary_purpose'] = 'revenue_generation'
        elif 'ai' in content or 'ml' in content:
            analysis['primary_purpose'] = 'ai_ml'
        elif 'data' in content or 'process' in content:
            analysis['primary_purpose'] = 'data_processing'
        elif 'api' in content:
            analysis['primary_purpose'] = 'api_integration'
        elif 'doc' in content or ext in ['.md', '.txt']:
            analysis['primary_purpose'] = 'documentation'
        else:
            analysis['primary_purpose'] = 'utility'
            
    except Exception as e:
        print(f"Error analyzing {filepath}: {e}")
        analysis['function_classification'] = 'MISCELLANEOUS'
        analysis['business_value'] = 1
    
    return analysis


def analyze_directory_structure(base_path: str) -> list:
    """Analyze directory structure with parent-child awareness"""
    file_records = []
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            filepath = Path(root) / file
            if filepath.is_file():
                # Get file metadata
                stat = filepath.stat()
                
                # Analyze content
                content_analysis = analyze_file_content(str(filepath))
                
                # Create record with parent-child awareness
                parent_dirs = str(filepath.parent).replace(base_path, '').strip('/')
                grandparent_dir = str(filepath.parent.parent).replace(base_path, '').strip('/') if filepath.parent.parent != Path(base_path) else ''
                
                record = {
                    'original_path': str(filepath),
                    'filename': file,
                    'extension': Path(file).suffix.lower(),
                    'parent_directory': parent_dirs.split('/')[-1] if parent_dirs else 'root',
                    'grandparent_directory': grandparent_dir.split('/')[-1] if grandparent_dir else '',
                    'relative_path': str(filepath.relative_to(base_path)),
                    'size_bytes': stat.st_size,
                    'size_mb': round(stat.st_size / (1024*1024), 2),
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'function_classification': content_analysis['function_classification'],
                    'business_value': content_analysis['business_value'],
                    'primary_purpose': content_analysis['primary_purpose'],
                    'content_keywords': '|'.join(content_analysis['content_keywords']),
                    'revenue_potential': content_analysis['revenue_potential'],
                    'automation_potential': content_analysis['automation_potential'],
                    'integration_potential': content_analysis['integration_potential'],
                    'ai_tool_type': content_analysis['ai_tool_type'] or '',
                    'file_hash': get_file_hash(str(filepath)),
                    'suggested_new_path': f"{content_analysis['function_classification']}/{file}"
                }
                
                file_records.append(record)
    
    return file_records


def create_parent_child_analysis(file_records: list) -> dict:
    """Create parent-child relationship analysis"""
    parent_child_analysis = {
        'parent_directory_analysis': defaultdict(lambda: {'count': 0, 'total_size': 0, 'functions': Counter(), 'business_value_total': 0}),
        'grandparent_analysis': defaultdict(lambda: {'count': 0, 'total_size': 0, 'functions': Counter(), 'business_value_total': 0}),
        'function_distribution': defaultdict(lambda: {'count': 0, 'total_size': 0, 'avg_business_value': 0}),
        'content_patterns': defaultdict(list)
    }
    
    for record in file_records:
        # Parent directory analysis
        parent = record['parent_directory']
        parent_child_analysis['parent_directory_analysis'][parent]['count'] += 1
        parent_child_analysis['parent_directory_analysis'][parent]['total_size'] += record['size_mb']
        parent_child_analysis['parent_directory_analysis'][parent]['functions'][record['function_classification']] += 1
        parent_child_analysis['parent_directory_analysis'][parent]['business_value_total'] += record['business_value']
        
        # Grandparent directory analysis
        grandparent = record['grandparent_directory']
        if grandparent:
            parent_child_analysis['grandparent_analysis'][grandparent]['count'] += 1
            parent_child_analysis['grandparent_analysis'][grandparent]['total_size'] += record['size_mb']
            parent_child_analysis['grandparent_analysis'][grandparent]['functions'][record['function_classification']] += 1
            parent_child_analysis['grandparent_analysis'][grandparent]['business_value_total'] += record['business_value']
        
        # Function distribution analysis
        func = record['function_classification']
        parent_child_analysis['function_distribution'][func]['count'] += 1
        parent_child_analysis['function_distribution'][func]['total_size'] += record['size_mb']
        parent_child_analysis['function_distribution'][func]['avg_business_value'] += record['business_value']
        
        # Content patterns
        if record['content_keywords']:
            keywords = record['content_keywords'].split('|')
            for keyword in keywords:
                if keyword.strip():
                    parent_child_analysis['content_patterns'][keyword.strip()].append(record['filename'])
    
    # Calculate averages
    for func, data in parent_child_analysis['function_distribution'].items():
        if data['count'] > 0:
            data['avg_business_value'] = round(data['avg_business_value'] / data['count'], 2)
    
    return parent_child_analysis


def save_analysis_to_csv(file_records: list, output_path: str):
    """Save the analysis to a CSV file"""
    fieldnames = [
        'original_path', 'filename', 'extension', 'parent_directory', 
        'grandparent_directory', 'relative_path', 'size_bytes', 'size_mb',
        'created', 'modified', 'function_classification', 'business_value',
        'primary_purpose', 'content_keywords', 'revenue_potential',
        'automation_potential', 'integration_potential', 'ai_tool_type',
        'file_hash', 'suggested_new_path'
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in file_records:
            writer.writerow(record)
    
    print(f"✅ Analysis saved to: {output_path}")


def save_parent_child_summary(analysis: dict, output_path: str):
    """Save parent-child analysis summary to CSV"""
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['directory', 'type', 'count', 'total_size_mb', 'dominant_function', 'avg_business_value', 'function_breakdown']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Write parent directory analysis
        for parent_dir, data in analysis['parent_directory_analysis'].items():
            dominant_func = data['functions'].most_common(1)[0][0] if data['functions'] else 'unknown'
            avg_business_value = round(data['business_value_total'] / data['count'], 2) if data['count'] > 0 else 0
            func_breakdown = ', '.join([f"{func}:{count}" for func, count in data['functions'].most_common(3)])
            
            writer.writerow({
                'directory': parent_dir,
                'type': 'parent',
                'count': data['count'],
                'total_size_mb': round(data['total_size'], 2),
                'dominant_function': dominant_func,
                'avg_business_value': avg_business_value,
                'function_breakdown': func_breakdown
            })
        
        # Write grandparent directory analysis
        for grandparent_dir, data in analysis['grandparent_analysis'].items():
            dominant_func = data['functions'].most_common(1)[0][0] if data['functions'] else 'unknown'
            avg_business_value = round(data['business_value_total'] / data['count'], 2) if data['count'] > 0 else 0
            func_breakdown = ', '.join([f"{func}:{count}" for func, count in data['functions'].most_common(3)])
            
            writer.writerow({
                'directory': grandparent_dir,
                'type': 'grandparent',
                'count': data['count'],
                'total_size_mb': round(data['total_size'], 2),
                'dominant_function': dominant_func,
                'avg_business_value': avg_business_value,
                'function_breakdown': func_breakdown
            })
    
    print(f"✅ Parent-child analysis summary saved to: {output_path}")


def main():
    print("🚀 AVATARARTS Advanced Parent-Child Content Analyzer")
    print("=" * 60)
    
    # Analyze the AVATARARTS directory
    base_path = "/Users/steven/AVATARARTS"
    print(f"Analyzing directory: {base_path}")
    
    # Get all file records with content analysis
    file_records = analyze_directory_structure(base_path)
    print(f"Analyzed {len(file_records)} files")
    
    # Create parent-child analysis
    parent_child_analysis = create_parent_child_analysis(file_records)
    
    # Create output directory
    output_dir = Path.home() / "avatararts_analysis_output"
    output_dir.mkdir(exist_ok=True)
    
    # Save main analysis to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    main_csv_path = output_dir / f"avatararts_content_analysis_{timestamp}.csv"
    save_analysis_to_csv(file_records, main_csv_path)
    
    # Save parent-child summary to CSV
    summary_csv_path = output_dir / f"avatararts_parent_child_summary_{timestamp}.csv"
    save_parent_child_summary(parent_child_analysis, summary_csv_path)
    
    # Create summary report
    summary_path = output_dir / f"avatararts_analysis_summary_{timestamp}.md"
    with open(summary_path, 'w') as f:
        f.write("# AVATARARTS Content Analysis Summary\n\n")
        f.write(f"Analysis Date: {datetime.now().isoformat()}\n\n")
        f.write(f"Total Files Analyzed: {len(file_records)}\n\n")
        
        f.write("## Function Distribution:\n")
        for func, data in parent_child_analysis['function_distribution'].items():
            f.write(f"- {func}: {data['count']} files ({data['total_size']:.2f} MB, avg business value: {data['avg_business_value']})\n")
        
        f.write("\n## Top Parent Directories by File Count:\n")
        sorted_parents = sorted(parent_child_analysis['parent_directory_analysis'].items(), 
                               key=lambda x: x[1]['count'], reverse=True)
        for parent, data in sorted_parents[:10]:
            f.write(f"- {parent}: {data['count']} files ({data['total_size']:.2f} MB)\n")
    
    print(f"✅ Analysis summary saved to: {summary_path}")
    
    print("\n📊 Analysis Complete!")
    print(f"   - Main analysis: {main_csv_path}")
    print(f"   - Parent-child summary: {summary_csv_path}")
    print(f"   - Summary report: {summary_path}")
    print(f"   - Total files analyzed: {len(file_records)}")


if __name__ == "__main__":
    main()
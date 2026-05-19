#!/usr/bin/env python3
"""
Enhanced Content-Aware Categorization System for AVATARARTS
Based on the existing AutoTag system but with improved functional categories
"""

import json
import os
import re
from datetime import datetime
import argparse
import sqlite3
from collections import Counter

def analyze_content_for_enhanced_category(description, filename=""):
    """Analyze content to determine the most appropriate functional category"""
    if not description and not filename:
        return 'MISCELLANEOUS', 0

    content_lower = (description + " " + filename).lower()

    # Define enhanced category keywords with more specific business functions
    categories = {
        'AUTOMATION': {
            'keywords': ['automation', 'automate', 'workflow', 'orchestrate', 'bot', 'agent', 'script', 'suite', 'routine', 'task'],
            'weight': 0
        },
        'REVENUE': {
            'keywords': ['revenue', 'income', 'profit', 'monetiz', 'launch', 'sales', 'earn', 'money', 'pricing', 'pricing', 'revenue'],
            'weight': 0
        },
        'BUSINESS_INTELLIGENCE': {
            'keywords': ['dashboard', 'analytics', 'intelligence', 'report', 'metric', 'kpi', 'insight', 'visualization', 'business', 'analysis'],
            'weight': 0
        },
        'AI_ML': {
            'keywords': ['ai', 'ml', 'model', 'neural', 'tensor', 'torch', 'openai', 'claude', 'gemini', 'grok', 'ollama', 'chatgpt', 'gpt'],
            'weight': 0
        },
        'DATA_PROCESSING': {
            'keywords': ['data', 'process', 'csv', 'pandas', 'json', 'xml', 'excel', 'transform', 'analyze', 'parsing', 'manipulation'],
            'weight': 0
        },
        'API_INTEGRATION': {
            'keywords': ['api', 'endpoint', 'client', 'integration', 'request', 'auth', 'oauth', 'endpoint', 'service', 'connect'],
            'weight': 0
        },
        'DEVELOPMENT_TOOLS': {
            'keywords': ['dev', 'tool', 'util', 'script', 'build', 'test', 'debug', 'development', 'coding', 'programming'],
            'weight': 0
        },
        'DOCUMENTATION': {
            'keywords': ['doc', 'manual', 'guide', 'tutorial', 'readme', 'howto', 'instruction', 'documentation', 'explanation'],
            'weight': 0
        },
        'MEDIA_PROCESSING': {
            'keywords': ['media', 'audio', 'video', 'image', 'mp3', 'mp4', 'jpg', 'png', 'process', 'convert', 'ffmpeg', 'media'],
            'weight': 0
        },
        'PORTFOLIO_MANAGEMENT': {
            'keywords': ['portfolio', 'invest', 'finance', 'stock', 'trade', 'asset', 'management', 'portfolio', 'financial'],
            'weight': 0
        },
        'CONTENT_CREATION': {
            'keywords': ['content', 'create', 'design', 'write', 'copy', 'text', 'generate', 'content', 'creative', 'media'],
            'weight': 0
        },
        'SEO_MARKETING': {
            'keywords': ['seo', 'marketing', 'campaign', 'keyword', 'rank', 'traffic', 'optimization', 'search', 'advertising'],
            'weight': 0
        },
        'ARCHIVES': {
            'keywords': ['archive', 'backup', 'old', 'historical', 'deprecated', 'legacy', 'past', 'archived', 'restore'],
            'weight': 0
        },
        'UTILITIES': {
            'keywords': ['util', 'helper', 'common', 'sync', 'clean', 'organize', 'utility', 'helper', 'common'],
            'weight': 0
        },
        'CONFIGURATIONS': {
            'keywords': ['config', 'setting', 'env', 'environment', 'ini', 'yaml', 'yml', 'json', 'configuration', 'setup'],
            'weight': 0
        },
        'MISCELLANEOUS': {
            'keywords': [],
            'weight': 0
        }
    }

    # Calculate weight for each category based on keyword matches
    for category, data in categories.items():
        weight = 0
        for keyword in data['keywords']:
            # Count occurrences of keyword in content
            matches = len(content_lower.split(keyword)) - 1
            weight += matches * 2  # Double weight for direct matches

        # Additional scoring based on context
        if 'automation' in content_lower and ('revenue' in content_lower or 'income' in content_lower or 'monetiz' in content_lower):
            weight += 5  # High value for revenue automation
        if 'ai' in content_lower and ('automation' in content_lower or 'agent' in content_lower):
            weight += 4  # High value for AI automation
        if 'api' in content_lower and ('integration' in content_lower or 'connect' in content_lower):
            weight += 3  # High value for API integration
        if 'business' in content_lower and ('intelligence' in content_lower or 'analytics' in content_lower or 'dashboard' in content_lower):
            weight += 4  # High value for business intelligence

        categories[category]['weight'] = weight

    # Find category with highest weight
    best_category = max(categories.keys(), key=lambda k: categories[k]['weight'])

    # If no significant matches found, default to Utilities or Documentation based on file extension
    if categories[best_category]['weight'] == 0:
        if filename.endswith(('.md', '.txt', '.rst')):
            best_category = 'DOCUMENTATION'
        elif filename.endswith(('.py', '.sh', '.js', '.ts')):
            best_category = 'UTILITIES'
        else:
            best_category = 'MISCELLANEOUS'

    return best_category, categories[best_category]['weight']

def analyze_file_content_for_function(file_path):
    """Analyze actual file content to determine its primary function"""
    try:
        # Get file extension first
        ext = os.path.splitext(file_path)[1].lower()
        
        # For Python files, analyze the content
        if ext == '.py':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2000)  # Read first 2000 characters for analysis
            return analyze_content_for_enhanced_category(content, os.path.basename(file_path))
        
        # For shell scripts
        elif ext in ['.sh', '.bash', '.zsh']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2000)
            return analyze_content_for_enhanced_category(content, os.path.basename(file_path))
        
        # For documentation files
        elif ext in ['.md', '.txt', '.rst']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(2000)
            return analyze_content_for_enhanced_category(content, os.path.basename(file_path))
        
        # For other files, use filename and path
        else:
            return analyze_content_for_enhanced_category("", os.path.basename(file_path))
    
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        # If we can't read the file, use filename and path for categorization
        return analyze_content_for_enhanced_category("", os.path.basename(file_path))

def get_file_metadata(file_path):
    """Extract metadata from file path and name"""
    stat = os.stat(file_path)
    return {
        'name': os.path.basename(file_path),
        'path': file_path,
        'size_mb': round(stat.st_size / (1024*1024), 2),
        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'extension': os.path.splitext(file_path)[1].lower()
    }

def create_enhanced_index(target_dir):
    """Create an enhanced index with functional categorization"""
    print(f"Creating enhanced index for: {target_dir}")
    
    automation_tools = []
    
    # Walk through all files in target directory
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip certain file types that are not automation tools
            if file.startswith('.') or file.endswith(('.log', '.tmp', '__pycache__', '.pyc')):
                continue
                
            # Get file metadata
            metadata = get_file_metadata(file_path)
            
            # Analyze content for functional category
            category, confidence = analyze_file_content_for_function(file_path)
            
            # Add to automation tools list
            tool_info = {
                'name': metadata['name'],
                'path': metadata['path'],
                'size_mb': metadata['size_mb'],
                'created': metadata['created'],
                'modified': metadata['modified'],
                'extension': metadata['extension'],
                'primary_type': 'script' if metadata['extension'] in ['.py', '.sh', '.js', '.ts'] else 'document' if metadata['extension'] in ['.md', '.txt', '.csv'] else 'other',
                'description': f"File: {metadata['name']}, Size: {metadata['size_mb']}MB, Type: {metadata['extension']}",
                'intelligent_category': category,
                'confidence_score': min(confidence / 10.0, 1.0),  # Normalize confidence
                'predicted_business_value': predict_business_value_from_path(metadata['path'], category),
                'integration_potential': identify_integration_potential_simple(metadata['name'], metadata['extension'])
            }
            
            automation_tools.append(tool_info)
    
    index_data = {
        'scan_start_time': datetime.now().isoformat(),
        'target_directory': target_dir,
        'automation_tools': automation_tools,
        'total_files': len(automation_tools),
        'total_directories': len(next(os.walk(target_dir))[1]),
        'scan_end_time': datetime.now().isoformat()
    }
    
    return index_data

def predict_business_value_from_path(file_path, category):
    """Predict business value based on path and category"""
    path_lower = file_path.lower()
    
    # High business value categories
    if category in ['REVENUE', 'AUTOMATION', 'AI_ML', 'BUSINESS_INTELLIGENCE']:
        base_value = 8.0
    elif category in ['API_INTEGRATION', 'DATA_PROCESSING', 'SEO_MARKETING']:
        base_value = 6.0
    elif category in ['DEVELOPMENT_TOOLS', 'PORTFOLIO_MANAGEMENT', 'CONTENT_CREATION']:
        base_value = 5.0
    else:
        base_value = 3.0
    
    # Additional factors
    if 'revenue' in path_lower or 'income' in path_lower or 'monetiz' in path_lower:
        base_value += 2.0
    if 'api' in path_lower and 'integration' in path_lower:
        base_value += 1.5
    if 'automation' in path_lower or 'automate' in path_lower:
        base_value += 1.5
    if 'ai' in path_lower or 'ml' in path_lower:
        base_value += 1.5
    
    return min(base_value, 10.0)

def identify_integration_potential_simple(filename, extension):
    """Simple integration potential identification"""
    name_lower = filename.lower()
    
    has_potential = any([
        'api' in name_lower,
        'integration' in name_lower,
        'connect' in name_lower,
        'sync' in name_lower,
        'webhook' in name_lower,
        extension in ['.py', '.js', '.ts']  # Programming files often have integration potential
    ])
    
    return {
        'has_potential': has_potential,
        'potential_type': 'high' if has_potential else 'low'
    }

def save_enhanced_index_to_csv(index_data, csv_path):
    """Save the enhanced index to CSV format"""
    import csv
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'name', 'path', 'size_mb', 'created', 'modified', 'extension', 
            'primary_type', 'description', 'intelligent_category', 
            'confidence_score', 'predicted_business_value', 'integration_potential_has_potential'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for tool in index_data['automation_tools']:
            row = {
                'name': tool.get('name', ''),
                'path': tool.get('path', ''),
                'size_mb': tool.get('size_mb', 0),
                'created': tool.get('created', ''),
                'modified': tool.get('modified', ''),
                'extension': tool.get('extension', ''),
                'primary_type': tool.get('primary_type', ''),
                'description': tool.get('description', '')[:200],  # Limit description length
                'intelligent_category': tool.get('intelligent_category', ''),
                'confidence_score': tool.get('confidence_score', 0),
                'predicted_business_value': tool.get('predicted_business_value', 0),
                'integration_potential_has_potential': tool.get('integration_potential', {}).get('has_potential', False)
            }
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description='Create enhanced functional index of AVATARARTS directory')
    parser.add_argument('--target', required=True, help='Target directory to index')
    parser.add_argument('--output', default='./enhanced_functional_index.csv', help='Output CSV file path')
    
    args = parser.parse_args()
    
    print("🚀 Creating Enhanced Functional Index of AVATARARTS Directory")
    print(f"Target: {args.target}")
    print(f"Output: {args.output}")
    print("="*60)
    
    # Create enhanced index
    index_data = create_enhanced_index(args.target)
    
    # Save to CSV
    save_enhanced_index_to_csv(index_data, args.output)
    
    print(f"✅ Enhanced index created with {len(index_data['automation_tools'])} tools")
    print(f"📊 Results saved to: {args.output}")
    
    # Print summary by category
    print("\n📋 Summary by Category:")
    category_counts = {}
    for tool in index_data['automation_tools']:
        cat = tool.get('intelligent_category', 'MISCELLANEOUS')
        if cat not in category_counts:
            category_counts[cat] = 0
        category_counts[cat] += 1
    
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} files")

if __name__ == "__main__":
    main()
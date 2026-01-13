#!/usr/bin/env python3
"""
Content-Aware Python File Cataloger
Scans and categorizes all Python files in /Users/steven/pythons with metadata
"""

import os
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from collections import Counter
import hashlib


class ContentAwareCataloger:
    def __init__(self, base_dir: str = "/Users/steven/pythons"):
        self.base_dir = Path(base_dir)
        self.py_files = []
        self.catalog_data = []
        
    def scan_python_files(self):
        """Scan for all Python files in the directory"""
        print("🔍 Scanning for Python files...")
        
        for py_file in self.base_dir.rglob("*.py"):
            if not any(part.startswith('.') for part in py_file.parts):
                self.py_files.append(py_file)
        
        print(f"✅ Found {len(self.py_files)} Python files")
        return self.py_files
    
    def analyze_file_content(self, file_path: Path) -> Dict[str, Any]:
        """Analyze content of a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Basic file stats
            stat = file_path.stat()
            file_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            
            # Analyze content
            lines = content.splitlines()
            non_empty_lines = [line for line in lines if line.strip()]
            code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
            
            # Identify content patterns
            patterns = self.identify_patterns(content)
            
            # Determine primary category
            category = self.determine_category(file_path, content, patterns)
            
            # Determine secondary tags
            tags = self.generate_tags(content, patterns)
            
            file_info = {
                'filename': file_path.name,
                'relative_path': str(file_path.relative_to(self.base_dir)),
                'absolute_path': str(file_path),
                'size_bytes': len(content),
                'line_count': len(lines),
                'non_empty_line_count': len(non_empty_lines),
                'code_line_count': len(code_lines),
                'word_count': len(content.split()),
                'creation_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modification_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'file_hash': file_hash,
                'primary_category': category,
                'tags': ', '.join(tags),
                'import_count': patterns['import_count'],
                'function_count': patterns['function_count'],
                'class_count': patterns['class_count'],
                'has_main_guard': patterns['has_main_guard'],
                'ai_integration': patterns['ai_integration'],
                'file_operations': patterns['file_operations'],
                'data_processing': patterns['data_processing'],
                'analysis_tools': patterns['analysis_tools'],
                'deduplication': patterns['deduplication'],
                'web_automation': patterns['web_automation'],
                'media_processing': patterns['media_processing']
            }
            
            return file_info
            
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
            return None
    
    def identify_patterns(self, content: str) -> Dict[str, Any]:
        """Identify content patterns in the file"""
        # Count imports
        import_count = len(re.findall(r'^(import|from)\s', content, re.MULTILINE))
        
        # Count functions
        function_count = len(re.findall(r'^def\s+\w+', content, re.MULTILINE))
        
        # Count classes
        class_count = len(re.findall(r'^class\s+\w+', content, re.MULTILINE))
        
        # Check for main guard
        has_main_guard = bool(re.search(r'if __name__ == [\'"]__main__[\'"]:', content))
        
        # Identify specific technology usage
        ai_integration = bool(re.search(r'openai|anthropic|gemini|groq|claude', content, re.IGNORECASE))
        file_operations = bool(re.search(r'os\.path|pathlib|shutil|open\(|\.read|\.write', content, re.IGNORECASE))
        data_processing = bool(re.search(r'pandas|DataFrame|csv|json', content, re.IGNORECASE))
        analysis_tools = bool(re.search(r'analyze|analysis|report|metrics|summary', content, re.IGNORECASE))
        deduplication = bool(re.search(r'duplicate|hashlib|md5|similarity|compare', content, re.IGNORECASE))
        web_automation = bool(re.search(r'requests|selenium|beautifulsoup|flask|django|web', content, re.IGNORECASE))
        media_processing = bool(re.search(r'PIL|Pillow|cv2|moviepy|pydub|image|audio|video', content, re.IGNORECASE))
        
        return {
            'import_count': import_count,
            'function_count': function_count,
            'class_count': class_count,
            'has_main_guard': has_main_guard,
            'ai_integration': ai_integration,
            'file_operations': file_operations,
            'data_processing': data_processing,
            'analysis_tools': analysis_tools,
            'deduplication': deduplication,
            'web_automation': web_automation,
            'media_processing': media_processing
        }
    
    def determine_category(self, file_path: Path, content: str, patterns: Dict[str, Any]) -> str:
        """Determine primary category based on content and path"""
        # Check parent directory name first
        parent_dir = file_path.parent.name.lower()
        
        # Directory-based categories
        if 'ai_content' in parent_dir:
            return 'AI/ML Tools'
        elif 'automation' in parent_dir or 'bot' in parent_dir:
            return 'Automation Tools'
        elif 'media' in parent_dir or 'audio' in parent_dir or 'video' in parent_dir or 'image' in parent_dir:
            return 'Media Processing'
        elif 'data' in parent_dir:
            return 'Data Processing'
        elif 'file' in parent_dir or 'organiz' in parent_dir:
            return 'File Organization'
        elif 'util' in parent_dir:
            return 'Utilities'
        elif 'analysis' in parent_dir:
            return 'Analysis Tools'
        elif 'content' in parent_dir:
            return 'Content Creation'
        
        # Content-based categories
        if patterns['ai_integration'] and patterns['data_processing']:
            return 'AI/ML Tools'
        elif patterns['web_automation']:
            return 'Automation Tools' 
        elif patterns['media_processing']:
            return 'Media Processing'
        elif patterns['data_processing']:
            return 'Data Processing'
        elif patterns['analysis_tools']:
            return 'Analysis Tools'
        elif patterns['deduplication']:
            return 'File Organization'
        elif patterns['file_operations']:
            return 'Utilities'
        else:
            return 'General Python'
    
    def generate_tags(self, content: str, patterns: Dict[str, Any]) -> List[str]:
        """Generate tags based on content patterns"""
        tags = []
        
        if patterns['ai_integration']:
            tags.append('AI/ML')
        if patterns['web_automation']:
            tags.append('Web')
        if patterns['media_processing']:
            tags.append('Media')
        if patterns['data_processing']:
            tags.append('Data')
        if patterns['analysis_tools']:
            tags.append('Analysis')
        if patterns['deduplication']:
            tags.append('Deduplication')
        if patterns['file_operations']:
            tags.append('FileOps')
        if patterns['has_main_guard']:
            tags.append('Runnable')
        
        # Add common tech tags
        if 'openai' in content.lower():
            tags.append('OpenAI')
        if 'anthropic' in content.lower() or 'claude' in content.lower():
            tags.append('Anthropic')
        if 'gemini' in content.lower() or 'google' in content.lower():
            tags.append('Google')
        if 'pandas' in content:
            tags.append('Pandas')
        if 'requests' in content:
            tags.append('Requests')
        
        return list(set(tags))  # Remove duplicates
    
    def build_catalog(self):
        """Build the complete catalog of Python files"""
        print("📊 Building content-aware catalog...")
        
        for i, file_path in enumerate(self.py_files, 1):
            if i % 100 == 0:
                print(f"   Processed {i}/{len(self.py_files)} files...")
                
            file_info = self.analyze_file_content(file_path)
            if file_info:
                self.catalog_data.append(file_info)
        
        print(f"✅ Catalog built with {len(self.catalog_data)} entries")
        return self.catalog_data
    
    def save_csv(self, output_path: str = None):
        """Save catalog to CSV file"""
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.base_dir / f"CONTENT_AWARE_CATALOG/python_files_catalog_{timestamp}.csv"
        
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        fieldnames = [
            'filename', 'relative_path', 'absolute_path', 'size_bytes', 
            'line_count', 'non_empty_line_count', 'code_line_count', 'word_count',
            'creation_time', 'modification_time', 'file_hash', 
            'primary_category', 'tags', 'import_count', 'function_count', 
            'class_count', 'has_main_guard', 'ai_integration', 'file_operations',
            'data_processing', 'analysis_tools', 'deduplication', 
            'web_automation', 'media_processing'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.catalog_data:
                writer.writerow(row)
        
        print(f"✅ Catalog saved to: {output_path}")
        return output_path
    
    def save_json(self, output_path: str = None):
        """Save catalog to JSON file for more detailed analysis"""
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.base_dir / f"CONTENT_AWARE_CATALOG/python_files_catalog_{timestamp}.json"
        
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.catalog_data, jsonfile, indent=2, default=str)
        
        print(f"✅ JSON catalog saved to: {output_path}")
        return output_path
    
    def generate_summary(self):
        """Generate summary statistics"""
        if not self.catalog_data:
            return {}
        
        categories = Counter(item['primary_category'] for item in self.catalog_data)
        tags_all = []
        for item in self.catalog_data:
            tags_all.extend(item['tags'].split(', '))
        tags = Counter(tag for tag in tags_all if tag.strip())
        
        ai_integration_count = sum(1 for item in self.catalog_data if item['ai_integration'])
        file_operations_count = sum(1 for item in self.catalog_data if item['file_operations'])
        data_processing_count = sum(1 for item in self.catalog_data if item['data_processing'])
        analysis_tools_count = sum(1 for item in self.catalog_data if item['analysis_tools'])
        deduplication_count = sum(1 for item in self.catalog_data if item['deduplication'])
        
        summary = {
            'total_files': len(self.catalog_data),
            'total_size_mb': round(sum(item['size_bytes'] for item in self.catalog_data) / (1024*1024), 2),
            'total_lines': sum(item['line_count'] for item in self.catalog_data),
            'categories': dict(categories),
            'top_tags': dict(tags.most_common(20)),
            'ai_integration_files': ai_integration_count,
            'file_operations_files': file_operations_count,
            'data_processing_files': data_processing_count,
            'analysis_tools_files': analysis_tools_count,
            'deduplication_files': deduplication_count,
        }
        
        return summary
    
    def save_summary(self, output_path: str = None):
        """Save summary statistics to a text file"""
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.base_dir / f"CONTENT_AWARE_CATALOG/catalog_summary_{timestamp}.txt"
        
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        summary = self.generate_summary()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("Content-Aware Python Files Catalog Summary\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("Overall Statistics:\n")
            f.write(f"  Total Files: {summary['total_files']}\n")
            f.write(f"  Total Size: {summary['total_size_mb']} MB\n")
            f.write(f"  Total Lines: {summary['total_lines']:,}\n\n")
            
            f.write("Files by Category:\n")
            for category, count in sorted(summary['categories'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"  {category}: {count}\n")
            f.write("\n")
            
            f.write("Top Tags:\n")
            for tag, count in summary['top_tags'].items():
                if tag:  # Skip empty tags
                    f.write(f"  {tag}: {count}\n")
            f.write("\n")
            
            f.write("Feature Distribution:\n")
            f.write(f"  AI Integration: {summary['ai_integration_files']}\n")
            f.write(f"  File Operations: {summary['file_operations_files']}\n")
            f.write(f"  Data Processing: {summary['data_processing_files']}\n")
            f.write(f"  Analysis Tools: {summary['analysis_tools_files']}\n")
            f.write(f"  Deduplication: {summary['deduplication_files']}\n")
        
        print(f"✅ Summary saved to: {output_path}")
        return output_path
    
    def run_full_catalog(self):
        """Run the complete cataloging process"""
        print("🚀 Starting Content-Aware Python Files Cataloger")
        print(f"📁 Scanning directory: {self.base_dir}")
        
        # Scan files
        self.scan_python_files()
        
        # Build catalog
        self.build_catalog()
        
        # Save outputs
        csv_path = self.save_csv()
        json_path = self.save_json()
        summary_path = self.save_summary()
        
        # Print summary
        summary = self.generate_summary()
        print("\n📈 CATALOG SUMMARY:")
        print(f"   Total files cataloged: {summary['total_files']}")
        print(f"   Total size: {summary['total_size_mb']} MB")
        print(f"   Total lines: {summary['total_lines']:,}")
        print(f"   Primary categories: {len(summary['categories'])}")
        print(f"   Top category: {max(summary['categories'], key=summary['categories'].get)}")
        print(f"   Files with AI integration: {summary['ai_integration_files']}")
        
        print(f"\n📁 Outputs:")
        print(f"   CSV: {csv_path}")
        print(f"   JSON: {json_path}")
        print(f"   Summary: {summary_path}")
        
        return csv_path, json_path, summary_path


def main():
    cataloger = ContentAwareCataloger()
    cataloger.run_full_catalog()


if __name__ == "__main__":
    main()
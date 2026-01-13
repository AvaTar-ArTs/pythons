#!/usr/bin/env python3
"""
Deep Multi-Folder Content Search Tool
Searches across multiple directories for common content patterns, functions, and functionality
"""

import os
import re
from pathlib import Path
from collections import defaultdict, Counter
import json
from datetime import datetime


class MultiFolderContentSearch:
    def __init__(self, base_dir="/Users/steven/pythons"):
        self.base_dir = Path(base_dir)
        self.content_patterns = {}
        self.function_patterns = {}
        self.common_imports = Counter()
        self.file_extensions = Counter()
        self.folder_contents = {}

    def search_patterns(self):
        """Search for common content patterns across directories"""
        print("🔍 Starting deep multi-folder content search...")
        
        # Define patterns to search for
        patterns = {
            'load_env_d': r'load_env_d|\.env\.d|load_dotenv',
            'api_key_usage': r'OPENAI_API_KEY|ANTHROPIC_API_KEY|GEMINI_API_KEY|api_key',
            'file_operations': r'os\.path|pathlib|shutil|open\(|\.read\(|\.write\(',
            'pandas_usage': r'import pandas as pd|pd\.',
            'dedup_patterns': r'duplicate|hashlib|md5|duplicate|similarity|compare',
            'analysis_patterns': r'analyze|analysis|report|metrics|summary'
        }
        
        # Scan Python files for patterns
        for py_file in self.base_dir.rglob("*.py"):
            if any(part.startswith('.') for part in py_file.parts):
                continue  # Skip hidden directories
                
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check for each pattern
                for pattern_name, pattern_regex in patterns.items():
                    if re.search(pattern_regex, content, re.IGNORECASE):
                        if pattern_name not in self.content_patterns:
                            self.content_patterns[pattern_name] = []
                        self.content_patterns[pattern_name].append(str(py_file))
                        
                # Extract common imports
                import_matches = re.findall(r'import (\w+)|from (\w+) import', content)
                for match in import_matches:
                    imp = match[0] or match[1]
                    if imp:
                        self.common_imports[imp] += 1
                        
                # Count file extensions
                self.file_extensions[py_file.suffix] += 1
                
            except Exception as e:
                print(f"Error reading {py_file}: {e}")
        
        print(f"✅ Found content patterns in {len(list(self.base_dir.rglob('*.py')))} Python files")
        return self.content_patterns

    def search_functions(self):
        """Search for common function definitions across directories"""
        function_counts = Counter()
        
        for py_file in self.base_dir.rglob("*.py"):
            if any(part.startswith('.') for part in py_file.parts):
                continue  # Skip hidden directories
                
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Find function definitions
                func_matches = re.findall(r'def (\w+)\s*\(', content)
                for func_name in func_matches:
                    function_counts[func_name] += 1
                    
                    # Store which files have this function
                    if func_name not in self.function_patterns:
                        self.function_patterns[func_name] = []
                    self.function_patterns[func_name].append(str(py_file))
            
            except Exception as e:
                print(f"Error reading {py_file} for functions: {e}")
        
        # Find functions that appear in multiple files
        common_functions = {name: files for name, files in self.function_patterns.items() 
                           if len(files) > 1}
        
        print(f"✅ Found {len(common_functions)} functions that appear in multiple files")
        return common_functions

    def analyze_folder_contents(self):
        """Analyze content of each major folder"""
        for item in self.base_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                py_files = list(item.rglob("*.py"))
                if py_files:
                    print(f"📁 Analyzing {item.name}: {len(py_files)} Python files")
                    
                    folder_content = {
                        'directory': item.name,
                        'python_files_count': len(py_files),
                        'files': [str(f.relative_to(self.base_dir)) for f in py_files[:10]],  # First 10 files
                        'pattern_counts': defaultdict(int)
                    }
                    
                    # Analyze content patterns in this folder
                    for py_file in py_files:
                        try:
                            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                
                            # Count occurrence of key patterns
                            if re.search(r'load_env_d|\.env\.d|load_dotenv', content, re.IGNORECASE):
                                folder_content['pattern_counts']['env_loading'] += 1
                            if re.search(r'duplicate|hashlib|md5|similarity', content, re.IGNORECASE):
                                folder_content['pattern_counts']['deduplication'] += 1
                            if re.search(r'analyze|analysis|report', content, re.IGNORECASE):
                                folder_content['pattern_counts']['analysis'] += 1
                            if re.search(r'pandas|DataFrame|csv', content, re.IGNORECASE):
                                folder_content['pattern_counts']['data_processing'] += 1
                            if re.search(r'openai|anthropic|gemini|api_key', content, re.IGNORECASE):
                                folder_content['pattern_counts']['ai_integration'] += 1
                                
                        except Exception as e:
                            print(f"Error analyzing {py_file}: {e}")
                    
                    self.folder_contents[item.name] = folder_content
                    
        return self.folder_contents

    def find_cross_directory_functionality(self):
        """Find similar functionality across different directories"""
        cross_dir_patterns = {
            'deduplication': [],
            'analysis': [],
            'file_operations': [],
            'api_integration': []
        }
        
        # Look for files that have specific functionality
        all_py_files = list(self.base_dir.rglob("*.py"))
        
        for py_file in all_py_files:
            if any(part.startswith('.') for part in py_file.parts):
                continue  # Skip hidden directories
                
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                file_path = str(py_file.relative_to(self.base_dir))
                
                # Classify functionality
                if re.search(r'hashlib|md5|duplicate|similarity|compare', content, re.IGNORECASE):
                    cross_dir_patterns['deduplication'].append(file_path)
                if re.search(r'analyze|analysis|report|metrics|summary', content, re.IGNORECASE):
                    cross_dir_patterns['analysis'].append(file_path)
                if re.search(r'os\.path|pathlib|shutil|open\(|\.read\(|\.write\(', content, re.IGNORECASE):
                    cross_dir_patterns['file_operations'].append(file_path)
                if re.search(r'openai|anthropic|gemini|api_key|load_env_d', content, re.IGNORECASE):
                    cross_dir_patterns['api_integration'].append(file_path)
                    
            except Exception as e:
                print(f"Error analyzing {py_file}: {e}")
                
        print(f"✅ Cross-directory functionality mapping complete")
        for func_type, files in cross_dir_patterns.items():
            print(f"  {func_type}: {len(files)} files")
            
        return cross_dir_patterns

    def generate_report(self):
        """Generate comprehensive report of multi-folder content analysis"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.base_dir / f"MULTI_FOLDER_CONTENT_REPORT_{timestamp}.md"
        
        with open(report_file, 'w') as f:
            f.write(f"# Multi-Folder Content Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Content Patterns Found\n\n")
            for pattern, files in self.content_patterns.items():
                f.write(f"### {pattern}\n")
                f.write(f"- Found in {len(files)} files\n")
                for file in files[:5]:  # Show first 5
                    f.write(f"  - {Path(file).name}\n")
                if len(files) > 5:
                    f.write(f"  - ... and {len(files) - 5} more\n")
                f.write("\n")
            
            f.write("\n## Common Functions\n\n")
            common_functions = {name: files for name, files in self.function_patterns.items() 
                               if len(files) > 5}  # Only show functions in more than 5 files
            for func_name, files in common_functions.items():
                f.write(f"### {func_name}\n")
                f.write(f"- Found in {len(files)} files\n")
                for file in files[:5]:
                    f.write(f"  - {Path(file).name}\n")
                if len(files) > 5:
                    f.write(f"  - ... and {len(files) - 5} more\n")
                f.write("\n")
            
            f.write("\n## Folder Analysis\n\n")
            for folder_name, data in self.folder_contents.items():
                f.write(f"### {folder_name}\n")
                f.write(f"- {data['python_files_count']} Python files\n")
                for pattern, count in data['pattern_counts'].items():
                    if count > 0:
                        f.write(f"  - {pattern}: {count} occurrences\n")
                f.write("\n")
            
            f.write("\n## Top Common Imports\n\n")
            for imp, count in self.common_imports.most_common(20):
                f.write(f"- {imp}: {count} occurrences\n")
            
            f.write("\n## File Extensions Distribution\n\n")
            for ext, count in self.file_extensions.most_common(10):
                f.write(f"- {ext}: {count} files\n")
        
        print(f"📊 Report saved to {report_file}")
        return report_file

    def save_detailed_results(self):
        """Save detailed results to JSON file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = self.base_dir / f"MULTI_FOLDER_CONTENT_DATA_{timestamp}.json"
        
        results = {
            'scan_date': datetime.now().isoformat(),
            'base_directory': str(self.base_dir),
            'content_patterns': self.content_patterns,
            'function_patterns': self.function_patterns,
            'folder_contents': self.folder_contents,
            'common_imports': dict(self.common_imports),
            'file_extensions': dict(self.file_extensions)
        }
        
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"💾 Detailed results saved to {json_file}")
        return json_file


def main():
    searcher = MultiFolderContentSearch()
    
    print("=" * 60)
    print("🔍 DEEP MULTI-FOLDER CONTENT SEARCH")
    print("=" * 60)
    
    # Search for content patterns
    print("\n1. Searching for content patterns...")
    patterns = searcher.search_patterns()
    
    # Search for common functions
    print("\n2. Searching for common functions...")
    functions = searcher.search_functions()
    
    # Analyze folder contents
    print("\n3. Analyzing folder contents...")
    folders = searcher.analyze_folder_contents()
    
    # Find cross-directory functionality
    print("\n4. Finding cross-directory functionality...")
    cross_func = searcher.find_cross_directory_functionality()
    
    # Generate report
    print("\n5. Generating comprehensive report...")
    report_file = searcher.generate_report()
    
    # Save detailed results
    json_file = searcher.save_detailed_results()
    
    print(f"\n✅ Deep multi-folder content search complete!")
    print(f"📄 Report: {report_file}")
    print(f"💾 JSON Data: {json_file}")
    
    # Summary
    print(f"\n📈 SUMMARY:")
    print(f"- Directories analyzed: {len(searcher.folder_contents)}")
    print(f"- Content patterns found: {len(searcher.content_patterns)}")
    print(f"- Functions analyzed: {len(searcher.function_patterns)}")
    print(f"- Common imports identified: {len(searcher.common_imports)}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Comprehensive Home Directory Python Scanner
Scans all Python files in ~/ with parent-folder content-awareness
Analyzes for duplicates, merge opportunities, and usage patterns
"""

import os
import csv
import ast
import re
import hashlib
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set
from difflib import SequenceMatcher

def safe_find_python_files() -> List[str]:
    """Safely find all Python files in home directory, excluding system areas"""
    home_dir = Path.home()
    python_files = []

    # Common directories to exclude
    exclude_patterns = {
        'Library', 'Applications', 'System', 'Volumes', '.Trash',
        '.git', '__pycache__', 'node_modules', '.venv', 'venv',
        '.cache', '.local', '.npm', '.yarn', '.DS_Store'
    }

    def should_exclude(path_parts: List[str]) -> bool:
        """Check if path contains excluded patterns"""
        for part in path_parts:
            if part in exclude_patterns:
                return True
        return False

    try:
        for root, dirs, files in os.walk(home_dir):
            # Filter directories
            dirs[:] = [d for d in dirs if not should_exclude([d])]

            # Check if current path should be excluded
            root_parts = Path(root).parts
            if should_exclude(root_parts):
                continue

            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    # Final check on full path
                    if not should_exclude(Path(filepath).parts):
                        python_files.append(filepath)

    except Exception as e:
        print(f"Warning during file scanning: {e}")

    return python_files

def extract_file_metadata(filepath: str) -> Dict:
    """Extract comprehensive metadata from a Python file"""
    metadata = {
        'filepath': filepath,
        'filename': os.path.basename(filepath),
        'directory': os.path.dirname(filepath),
        'parent_folder': Path(filepath).parent.name,
        'grandparent_folder': Path(filepath).parent.parent.name if Path(filepath).parent.parent != Path(filepath).parent else '',
        'file_size': 0,
        'line_count': 0,
        'file_hash': '',
        'last_modified': 0,
        'imports': [],
        'functions': [],
        'classes': [],
        'has_main': False,
        'docstring': '',
        'complexity_score': 0,
        'ai_related': False,
        'automation_related': False,
        'web_related': False,
        'data_related': False,
        'duplicate_potential': 'LOW',
        'merge_candidates': [],
        'content_summary': '',
        'error': None
    }

    try:
        # Basic file stats
        stat = os.stat(filepath)
        metadata['file_size'] = stat.st_size
        metadata['last_modified'] = stat.st_mtime

        # Read content
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        metadata['line_count'] = len(content.split('\n'))
        metadata['file_hash'] = hashlib.md5(content.encode()).hexdigest()

        # Parse content
        try:
            tree = ast.parse(content, filename=filepath)
            analyzer = ContentAnalyzer()
            analyzer.visit(tree)

            metadata.update(analyzer.get_metadata())

        except SyntaxError:
            # Fallback for files with syntax errors
            metadata.update(parse_with_regex(content))

        # Analyze content patterns
        content_lower = content.lower()

        # AI/ML patterns
        ai_keywords = ['openai', 'claude', 'anthropic', 'gpt', 'llm', 'ai', 'machine learning', 'neural']
        metadata['ai_related'] = any(keyword in content_lower for keyword in ai_keywords)

        # Automation patterns
        automation_keywords = ['automation', 'bot', 'scraper', 'selenium', 'automation']
        metadata['automation_related'] = any(keyword in content_lower for keyword in automation_keywords)

        # Web patterns
        web_keywords = ['flask', 'django', 'fastapi', 'requests', 'beautifulsoup', 'scrapy']
        metadata['web_related'] = any(keyword in content_lower for keyword in web_keywords)

        # Data patterns
        data_keywords = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'sklearn', 'tensorflow', 'pytorch']
        metadata['data_related'] = any(keyword in content_lower for keyword in data_keywords)

        # Generate content summary
        metadata['content_summary'] = generate_content_summary(metadata, content)

        # Assess duplicate potential
        metadata['duplicate_potential'] = assess_duplicate_potential(metadata, content)

    except Exception as e:
        metadata['error'] = str(e)

    return metadata

def parse_with_regex(content: str) -> Dict:
    """Fallback parsing for files with syntax errors"""
    return {
        'imports': list(set(re.findall(r'^(?:import|from)\s+(\w+)', content, re.MULTILINE))),
        'functions': list(set(re.findall(r'^def\s+(\w+)\s*\(', content, re.MULTILINE))),
        'classes': list(set(re.findall(r'^class\s+(\w+)', content, re.MULTILINE))),
        'has_main': 'if __name__ == \'__main__\'' in content,
        'docstring': extract_docstring_regex(content)
    }

def extract_docstring_regex(content: str) -> str:
    """Extract docstring using regex"""
    # Look for triple-quoted strings at the beginning
    docstring_match = re.search(r'^\s*"""(.*?)"""', content, re.DOTALL)
    if docstring_match:
        return docstring_match.group(1).strip()[:200]
    return ''

class ContentAnalyzer(ast.NodeVisitor):
    """AST-based content analyzer"""

    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []
        self.has_main = False
        self.docstring = ''
        self.assignments = []
        self.function_calls = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name.split('.')[0])

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.append(node.module.split('.')[0])

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        if ast.get_docstring(node) and not self.docstring:
            self.docstring = ast.get_docstring(node)[:200]

    def visit_ClassDef(self, node):
        self.classes.append(node.name)

    def visit_Assign(self, node):
        # Track variable assignments
        if hasattr(node, 'targets') and node.targets:
            target = node.targets[0]
            if hasattr(target, 'id'):
                self.assignments.append(target.id)

    def visit_Call(self, node):
        # Track function calls
        if hasattr(node.func, 'id'):
            self.function_calls.append(node.func.id)
        elif hasattr(node.func, 'attr'):
            self.function_calls.append(node.func.attr)

    def visit_If(self, node):
        # Check for main guard
        if (isinstance(node.test, ast.Compare) and
            len(node.test.comparators) == 1 and
            isinstance(node.test.comparators[0], ast.Str) and
            node.test.comparators[0].s == '__main__'):
            self.has_main = True

    def get_metadata(self):
        return {
            'imports': list(set(self.imports)),
            'functions': self.functions,
            'classes': self.classes,
            'has_main': self.has_main,
            'docstring': self.docstring,
            'assignments': list(set(self.assignments)),
            'function_calls': list(set(self.function_calls))
        }

def generate_content_summary(metadata: Dict, content: str) -> str:
    """Generate a concise summary of file content and purpose"""
    summary_parts = []

    # Primary purpose based on patterns
    if metadata['ai_related']:
        summary_parts.append("AI/ML integration")
    if metadata['automation_related']:
        summary_parts.append("automation tools")
    if metadata['web_related']:
        summary_parts.append("web development")
    if metadata['data_related']:
        summary_parts.append("data processing")

    # Structure info
    if metadata['classes']:
        summary_parts.append(f"{len(metadata['classes'])} classes")
    if metadata['functions']:
        summary_parts.append(f"{len(metadata['functions'])} functions")
    if metadata['imports']:
        summary_parts.append(f"{len(metadata['imports'])} imports")

    # Main guard
    if metadata['has_main']:
        summary_parts.append("executable")

    # Docstring preview
    if metadata['docstring']:
        doc_preview = metadata['docstring'][:50].replace('\n', ' ')
        summary_parts.append(f"docs: {doc_preview}")

    return " | ".join(summary_parts) if summary_parts else "utility script"

def assess_duplicate_potential(metadata: Dict, content: str) -> str:
    """Assess the potential for this file to be a duplicate"""
    filename = metadata['filename'].lower()

    # High potential indicators
    if re.search(r'[_\-\s][v]?(\d+)$', filename):  # versioned files
        return 'HIGH - Versioned file'

    if any(term in filename for term in ['copy', 'bak', 'old', 'new']):
        return 'HIGH - Backup file'

    if 'duplicate' in content.lower() or 'copy' in content.lower():
        return 'HIGH - Explicitly marked as duplicate'

    # Medium potential indicators
    if len(metadata['functions']) <= 2 and metadata['line_count'] < 50:
        return 'MEDIUM - Very simple file'

    if metadata['functions'] and len(set(metadata['functions'])) < len(metadata['functions']):
        return 'MEDIUM - Function name conflicts'

    # Parent folder context
    parent = metadata['parent_folder'].lower()
    if any(term in parent for term in ['backup', 'old', 'archive', 'temp']):
        return 'MEDIUM - In backup/archive folder'

    # Content similarity checks would be done later in batch processing
    return 'LOW - Standard file'

def analyze_parent_folder_context(all_metadata: List[Dict]) -> Dict[str, Dict]:
    """Analyze parent folder patterns and relationships"""
    folder_analysis = defaultdict(lambda: {
        'file_count': 0,
        'total_size': 0,
        'purposes': Counter(),
        'ai_files': 0,
        'automation_files': 0,
        'common_imports': Counter(),
        'duplicate_risk': 'LOW'
    })

    for metadata in all_metadata:
        folder = metadata['parent_folder']
        folder_data = folder_analysis[folder]

        folder_data['file_count'] += 1
        folder_data['total_size'] += metadata['file_size']
        folder_data['purposes'][metadata.get('primary_purpose', 'unknown')] += 1

        if metadata['ai_related']:
            folder_data['ai_files'] += 1
        if metadata['automation_related']:
            folder_data['automation_files'] += 1

        for imp in metadata['imports']:
            folder_data['common_imports'][imp] += 1

    # Assess folder duplicate risk
    for folder, data in folder_analysis.items():
        if data['file_count'] > 10:
            data['duplicate_risk'] = 'HIGH - Many similar files'
        elif data['file_count'] > 5 and len(data['purposes']) == 1:
            data['duplicate_risk'] = 'MEDIUM - Similar purpose files'
        elif data['ai_files'] > data['file_count'] * 0.8:
            data['duplicate_risk'] = 'MEDIUM - Highly specialized folder'

    return dict(folder_analysis)

def find_content_duplicates(all_metadata: List[Dict]) -> List[Dict]:
    """Find files with similar or identical content"""
    duplicates = []

    # Group by hash for identical files
    hash_groups = defaultdict(list)
    for metadata in all_metadata:
        if metadata['file_hash']:
            hash_groups[metadata['file_hash']].append(metadata)

    # Process identical files
    for file_hash, files in hash_groups.items():
        if len(files) > 1:
            # Sort by path to keep first one
            files.sort(key=lambda x: x['filepath'])
            keep_file = files[0]

            for duplicate_file in files[1:]:
                duplicates.append({
                    'file_to_remove': duplicate_file['filepath'],
                    'filename': duplicate_file['filename'],
                    'reason': 'Identical content - exact duplicate',
                    'keep_file': keep_file['filepath'],
                    'similarity': '100%',
                    'duplicate_type': 'Identical Content',
                    'confidence': 'High',
                    'size_saved': duplicate_file['file_size']
                })

    # Find functionally similar files (same imports + functions)
    import_func_groups = defaultdict(list)
    for metadata in all_metadata:
        # Create signature based on imports and functions
        signature = (
            tuple(sorted(metadata['imports'])),
            tuple(sorted(metadata['functions']))
        )
        if signature[0] or signature[1]:  # Only if has content
            import_func_groups[signature].append(metadata)

    # Process similar files
    for signature, files in import_func_groups.items():
        if len(files) > 1 and len(signature[0]) > 2:  # At least 3 imports, 2+ files
            # Sort by file size (keep largest)
            files.sort(key=lambda x: x['file_size'], reverse=True)
            keep_file = files[0]

            for similar_file in files[1:]:
                duplicates.append({
                    'file_to_remove': similar_file['filepath'],
                    'filename': similar_file['filename'],
                    'reason': f'Similar functionality (imports: {len(signature[0])}, functions: {len(signature[1])})',
                    'keep_file': keep_file['filepath'],
                    'similarity': '85%',
                    'duplicate_type': 'Functional Duplicate',
                    'confidence': 'Medium',
                    'size_saved': similar_file['file_size']
                })

    return duplicates

def identify_merge_opportunities(all_metadata: List[Dict], folder_analysis: Dict) -> List[Dict]:
    """Identify files that could be merged or consolidated"""
    merge_opportunities = []

    # Find folders with many similar files
    for folder, data in folder_analysis.items():
        if data['file_count'] > 8:
            # Get files in this folder
            folder_files = [m for m in all_metadata if m['parent_folder'] == folder]

            # Group by primary purpose
            purpose_groups = defaultdict(list)
            for file_meta in folder_files:
                purpose = file_meta.get('primary_purpose', 'utility')
                purpose_groups[purpose].append(file_meta)

            # Look for merge opportunities
            for purpose, files in purpose_groups.items():
                if len(files) >= 5:  # 5+ files of same purpose
                    # Calculate potential consolidation
                    total_size = sum(f['file_size'] for f in files)
                    avg_size = total_size // len(files)

                    merge_opportunities.append({
                        'merge_type': 'Consolidate Similar Files',
                        'folder': folder,
                        'purpose': purpose,
                        'file_count': len(files),
                        'total_size_kb': total_size // 1024,
                        'avg_size_kb': avg_size // 1024,
                        'recommendation': f'Merge {len(files)} {purpose} files into unified module',
                        'complexity': 'High' if len(files) > 10 else 'Medium'
                    })

    # Find scattered utilities that could be centralized
    utility_functions = defaultdict(list)
    for metadata in all_metadata:
        if 'util' in metadata['filename'].lower():
            for func in metadata['functions']:
                utility_functions[func].append(metadata['filepath'])

    # Find commonly duplicated utility functions
    common_utils = {func: files for func, files in utility_functions.items() if len(files) >= 3}
    if common_utils:
        merge_opportunities.append({
            'merge_type': 'Centralize Utility Functions',
            'functions': list(common_utils.keys()),
            'occurrences': {func: len(files) for func, files in common_utils.items()},
            'recommendation': f'Create shared utility module for {len(common_utils)} common functions',
            'complexity': 'Medium'
        })

    return merge_opportunities

def create_comprehensive_csv(all_metadata: List[Dict], duplicates: List[Dict], merges: List[Dict], folder_analysis: Dict):
    """Create comprehensive CSV with all analysis data"""

    # Main file analysis CSV
    with open('home_python_comprehensive_analysis.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'filepath', 'filename', 'parent_folder', 'grandparent_folder',
            'file_size', 'line_count', 'file_hash', 'content_summary',
            'imports_count', 'functions_count', 'classes_count', 'has_main',
            'ai_related', 'automation_related', 'web_related', 'data_related',
            'duplicate_potential', 'primary_purpose', 'last_modified', 'error'
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for metadata in all_metadata:
            row = {
                'filepath': metadata['filepath'],
                'filename': metadata['filename'],
                'parent_folder': metadata['parent_folder'],
                'grandparent_folder': metadata['grandparent_folder'],
                'file_size': metadata['file_size'],
                'line_count': metadata['line_count'],
                'file_hash': metadata['file_hash'],
                'content_summary': metadata['content_summary'],
                'imports_count': len(metadata.get('imports', [])),
                'functions_count': len(metadata.get('functions', [])),
                'classes_count': len(metadata.get('classes', [])),
                'has_main': metadata['has_main'],
                'ai_related': metadata['ai_related'],
                'automation_related': metadata['automation_related'],
                'web_related': metadata['web_related'],
                'data_related': metadata['data_related'],
                'duplicate_potential': metadata['duplicate_potential'],
                'primary_purpose': metadata.get('primary_purpose', 'unknown'),
                'last_modified': metadata['last_modified'],
                'error': metadata['error']
            }
            writer.writerow(row)

    # Duplicates CSV
    if duplicates:
        with open('home_python_duplicates.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'file_to_remove', 'filename', 'reason', 'keep_file',
                'similarity', 'duplicate_type', 'confidence', 'size_saved'
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(duplicates)

    # Merge opportunities CSV
    if merges:
        with open('home_python_merge_opportunities.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['merge_type', 'folder', 'purpose', 'file_count', 'total_size_kb', 'avg_size_kb', 'recommendation', 'complexity'])

            for merge in merges:
                writer.writerow([
                    merge['merge_type'],
                    merge.get('folder', ''),
                    merge.get('purpose', ''),
                    merge.get('file_count', ''),
                    merge.get('total_size_kb', ''),
                    merge.get('avg_size_kb', ''),
                    merge['recommendation'],
                    merge['complexity']
                ])

    # Folder analysis CSV
    with open('home_python_folder_analysis.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'folder', 'file_count', 'total_size_kb', 'primary_purposes',
            'ai_files', 'automation_files', 'top_imports', 'duplicate_risk'
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for folder, data in folder_analysis.items():
            row = {
                'folder': folder,
                'file_count': data['file_count'],
                'total_size_kb': data['total_size'] // 1024,
                'primary_purposes': ', '.join(f"{k}({v})" for k, v in data['purposes'].most_common(3)),
                'ai_files': data['ai_files'],
                'automation_files': data['automation_files'],
                'top_imports': ', '.join(f"{k}({v})" for k, v in data['common_imports'].most_common(3)),
                'duplicate_risk': data['duplicate_risk']
            }
            writer.writerow(row)

def main():
    """Main analysis function"""
    print("🔍 Starting comprehensive home directory Python analysis...")
    print("📂 Scanning with parent-folder content-awareness...")

    # Find all Python files
    python_files = safe_find_python_files()
    print(f"📊 Found {len(python_files)} Python files to analyze")

    # Limit for performance (can be adjusted)
    analysis_limit = min(500, len(python_files))
    python_files = python_files[:analysis_limit]

    print(f"🎯 Analyzing first {analysis_limit} files...")

    # Analyze each file
    all_metadata = []
    for i, filepath in enumerate(python_files):
        if i % 50 == 0:
            print(f"   Progress: {i+1}/{len(python_files)} files analyzed")

        metadata = extract_file_metadata(filepath)
        all_metadata.append(metadata)

    print(f"✅ Completed content analysis of {len(all_metadata)} files")

    # Analyze parent folder context
    print("📁 Analyzing parent folder relationships...")
    folder_analysis = analyze_parent_folder_context(all_metadata)

    # Find duplicates
    print("🔍 Identifying content-based duplicates...")
    duplicates = find_content_duplicates(all_metadata)

    # Identify merge opportunities
    print("🔗 Finding merge opportunities...")
    merges = identify_merge_opportunities(all_metadata, folder_analysis)

    # Create comprehensive CSV files
    print("💾 Generating comprehensive CSV reports...")
    create_comprehensive_csv(all_metadata, duplicates, merges, folder_analysis)

    # Summary statistics
    print("\n📊 Analysis Summary:")
    print(f"   • Files analyzed: {len(all_metadata)}")
    print(f"   • Duplicates found: {len(duplicates)}")
    print(f"   • Merge opportunities: {len(merges)}")
    print(f"   • Folders analyzed: {len(folder_analysis)}")

    # Calculate space savings
    if duplicates:
        space_saved = sum(int(d.get('size_saved', 0)) for d in duplicates)
        print(f"   • Potential space savings: ~{space_saved // 1024} KB")

    # Show top purposes
    purposes = Counter(m.get('primary_purpose', 'unknown') for m in all_metadata if m.get('primary_purpose'))
    print("\n🎯 Top file purposes:")
    for purpose, count in purposes.most_common(5):
        print(f"   • {purpose}: {count} files")

    # Show duplicate types
    if duplicates:
        dup_types = Counter(d['duplicate_type'] for d in duplicates)
        print("\n📋 Duplicate types found:")
        for dup_type, count in dup_types.most_common():
            print(f"   • {dup_type}: {count} files")

    print("\n✅ Analysis complete!")
    print("📄 Generated CSV files:")
    print("   • home_python_comprehensive_analysis.csv - Detailed file analysis")
    print("   • home_python_duplicates.csv - Files to remove")
    print("   • home_python_merge_opportunities.csv - Consolidation opportunities")
    print("   • home_python_folder_analysis.csv - Folder-level insights")

if __name__ == '__main__':
    main()
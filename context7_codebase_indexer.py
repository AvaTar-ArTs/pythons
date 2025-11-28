#!/usr/bin/env python3
"""
Context7 Codebase Indexer
Analyzes your entire codebase and generates Context7-compatible documentation index
Leverages your 758+ Python scripts, MD files, HTML, CSV, and existing documentation
"""

import os
import sys
import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict, Counter
from datetime import datetime
import hashlib

# Load environment from ~/.env.d/
env_dir = Path.home() / '.env.d'
if env_dir.exists():
    from dotenv import load_dotenv
    for env_file in env_dir.glob('*.env'):
        load_dotenv(env_file, override=False)

class Context7CodebaseIndexer:
    """Index your codebase for Context7 integration"""
    
    def __init__(self):
        self.pythons_dir = Path.home() / 'pythons'
        self.documents_dir = Path.home() / 'Documents'
        self.pictures_dir = Path.home() / 'Pictures'
        self.context7_dir = self.pythons_dir / '.context7'
        self.context7_dir.mkdir(exist_ok=True)
        
        self.libraries = defaultdict(list)  # library -> [files using it]
        self.functions = []  # All function definitions
        self.classes = []  # All class definitions
        self.imports = Counter()  # Import frequency
        self.code_patterns = defaultdict(list)  # Pattern type -> examples
        self.documentation = []  # Extracted documentation
        
    def analyze_codebase(self):
        """Main analysis function"""
        print("🔍 Context7 Codebase Indexer")
        print("=" * 80)
        print(f"📁 Analyzing: {self.pythons_dir}")
        print()
        
        # Analyze Python files
        print("📄 Analyzing Python scripts...")
        self.analyze_python_files()
        
        # Analyze documentation
        print("\n📚 Analyzing documentation files...")
        self.analyze_documentation()
        
        # Analyze other content
        print("\n📊 Analyzing other content (HTML, CSV)...")
        self.analyze_other_content()
        
        # Generate index
        print("\n📝 Generating Context7 index...")
        self.generate_index()
        
        # Generate library usage report
        print("\n📊 Generating library usage report...")
        self.generate_library_report()
        
        print("\n✅ Analysis complete!")
        print(f"📁 Results saved to: {self.context7_dir}")
        
    def analyze_python_files(self):
        """Analyze all Python files"""
        py_files = list(self.pythons_dir.rglob('*.py'))
        total = len(py_files)
        
        for i, py_file in enumerate(py_files, 1):
            # Skip venv and hidden directories
            if '.venv' in str(py_file) or '.git' in str(py_file):
                continue
                
            if i % 50 == 0:
                print(f"  Progress: {i}/{total} files...", end='\r')
            
            try:
                self.analyze_python_file(py_file)
            except Exception as e:
                pass  # Skip files that can't be parsed
        
        print(f"\n  ✅ Analyzed {total} Python files")
    
    def analyze_python_file(self, file_path: Path):
        """Analyze a single Python file"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            rel_path = str(file_path.relative_to(self.pythons_dir))
            
            # Parse AST
            try:
                tree = ast.parse(content)
                self.extract_from_ast(tree, rel_path)
            except SyntaxError:
                # If AST parsing fails, use regex fallback
                self.extract_from_regex(content, rel_path)
            
            # Extract imports (regex for reliability)
            imports = self.extract_imports_regex(content)
            for imp in imports:
                self.imports[imp] += 1
                self.libraries[imp].append(rel_path)
            
            # Extract code patterns
            self.extract_patterns(content, rel_path)
            
        except Exception:
            pass
    
    def extract_from_ast(self, tree: ast.AST, file_path: str):
        """Extract functions and classes from AST"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.functions.append({
                    'name': node.name,
                    'file': file_path,
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'docstring': ast.get_docstring(node) or ''
                })
            elif isinstance(node, ast.ClassDef):
                self.classes.append({
                    'name': node.name,
                    'file': file_path,
                    'line': node.lineno,
                    'docstring': ast.get_docstring(node) or ''
                })
    
    def extract_from_regex(self, content: str, file_path: str):
        """Fallback: extract functions using regex"""
        # Function definitions
        func_pattern = r'^def\s+(\w+)\s*\([^)]*\)\s*:'
        for match in re.finditer(func_pattern, content, re.MULTILINE):
            self.functions.append({
                'name': match.group(1),
                'file': file_path,
                'line': content[:match.start()].count('\n') + 1,
                'args': [],
                'docstring': ''
            })
    
    def extract_imports_regex(self, content: str) -> Set[str]:
        """Extract import statements using regex"""
        imports = set()
        
        # Standard imports: import library
        import_pattern = r'^import\s+(\w+)'
        for match in re.finditer(import_pattern, content, re.MULTILINE):
            imports.add(match.group(1))
        
        # From imports: from library import ...
        from_pattern = r'^from\s+(\w+)'
        for match in re.finditer(from_pattern, content, re.MULTILINE):
            imports.add(match.group(1))
        
        return imports
    
    def extract_patterns(self, content: str, file_path: str):
        """Extract common code patterns"""
        # API calls
        if re.search(r'(openai|anthropic|gemini)\.', content, re.IGNORECASE):
            self.code_patterns['llm_api_calls'].append({
                'file': file_path,
                'pattern': 'LLM API usage'
            })
        
        # Image processing
        if re.search(r'PIL|Image|Pillow', content):
            self.code_patterns['image_processing'].append({
                'file': file_path,
                'pattern': 'Image processing'
            })
        
        # File operations
        if re.search(r'Path\(|pathlib', content):
            self.code_patterns['pathlib_usage'].append({
                'file': file_path,
                'pattern': 'Pathlib usage'
            })
        
        # Environment loading
        if re.search(r'\.env\.d|load_dotenv|loader\.sh', content):
            self.code_patterns['env_loading'].append({
                'file': file_path,
                'pattern': 'Environment loading'
            })
    
    def analyze_documentation(self):
        """Analyze markdown and documentation files"""
        # Analyze pythons WARP.md
        warp_file = self.pythons_dir / 'WARP.md'
        if warp_file.exists():
            self.documentation.append({
                'file': 'WARP.md',
                'type': 'project_context',
                'content': warp_file.read_text()[:1000]  # First 1000 chars
            })
        
        # Analyze Documents markdown files
        for md_file in self.documents_dir.rglob('*.md'):
            if md_file.is_file() and md_file.stat().st_size < 1_000_000:  # < 1MB
                try:
                    content = md_file.read_text(encoding='utf-8', errors='ignore')
                    # Extract code blocks
                    code_blocks = re.findall(r'```(?:python|bash|sh)?\n(.*?)```', content, re.DOTALL)
                    if code_blocks:
                        self.documentation.append({
                            'file': str(md_file.relative_to(self.documents_dir)),
                            'type': 'markdown',
                            'code_examples': code_blocks[:5]  # First 5 examples
                        })
                except Exception:
                    pass
    
    def analyze_other_content(self):
        """Analyze HTML, CSV, and other content"""
        # HTML files - extract code snippets
        for html_file in self.documents_dir.rglob('*.html'):
            if html_file.is_file():
                try:
                    content = html_file.read_text(encoding='utf-8', errors='ignore')
                    # Extract script tags
                    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
                    if scripts:
                        self.code_patterns['html_scripts'].append({
                            'file': str(html_file.relative_to(self.documents_dir)),
                            'count': len(scripts)
                        })
                except Exception:
                    pass
    
    def generate_index(self):
        """Generate Context7-compatible index"""
        index = {
            'generated_at': datetime.now().isoformat(),
            'codebase_stats': {
                'total_python_files': len(list(self.pythons_dir.rglob('*.py'))),
                'total_functions': len(self.functions),
                'total_classes': len(self.classes),
                'unique_libraries': len(self.libraries),
                'total_imports': sum(self.imports.values())
            },
            'libraries': {
                lib: {
                    'usage_count': len(files),
                    'files': files[:10]  # Top 10 files
                }
                for lib, files in sorted(self.libraries.items(), key=lambda x: len(x[1]), reverse=True)[:50]
            },
            'top_imports': dict(self.imports.most_common(30)),
            'code_patterns': {
                pattern: len(examples) for pattern, examples in self.code_patterns.items()
            },
            'documentation_files': len(self.documentation),
            'context7_integration': {
                'api_key_configured': bool(os.getenv('CONTEXT7_API_KEY')),
                'ready_for_queries': True,
                'recommended_libraries': self.get_recommended_libraries()
            }
        }
        
        index_file = self.context7_dir / 'codebase_index.json'
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
        
        print(f"  ✅ Index saved: {index_file}")
    
    def get_recommended_libraries(self) -> List[str]:
        """Get libraries that would benefit from Context7 docs"""
        # Libraries you use that Context7 likely supports
        context7_candidates = [
            'openai', 'anthropic', 'requests', 'pandas', 'numpy',
            'PIL', 'Pillow', 'pathlib', 'json', 'csv',
            'jinja2', 'flask', 'fastapi', 'django'
        ]
        
        return [lib for lib in self.libraries.keys() 
                if any(candidate in lib.lower() for candidate in context7_candidates)]
    
    def generate_library_report(self):
        """Generate detailed library usage report"""
        report = {
            'most_used_libraries': [
                {
                    'library': lib,
                    'usage_count': len(files),
                    'files': files[:5]
                }
                for lib, files in sorted(self.libraries.items(), 
                                        key=lambda x: len(x[1]), 
                                        reverse=True)[:20]
            ],
            'library_categories': self.categorize_libraries(),
            'context7_ready_libraries': self.get_recommended_libraries()
        }
        
        report_file = self.context7_dir / 'library_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"  ✅ Report saved: {report_file}")
        
        # Also generate markdown summary
        self.generate_markdown_summary(report)
    
    def categorize_libraries(self) -> Dict[str, List[str]]:
        """Categorize libraries by type"""
        categories = {
            'ai_ml': ['openai', 'anthropic', 'gemini', 'groq', 'mistral'],
            'data': ['pandas', 'numpy', 'csv', 'json'],
            'image': ['PIL', 'Pillow', 'Image'],
            'web': ['requests', 'flask', 'fastapi', 'django'],
            'utils': ['pathlib', 'os', 'sys', 'datetime']
        }
        
        categorized = defaultdict(list)
        for lib in self.libraries.keys():
            lib_lower = lib.lower()
            for category, keywords in categories.items():
                if any(keyword in lib_lower for keyword in keywords):
                    categorized[category].append(lib)
                    break
            else:
                categorized['other'].append(lib)
        
        return dict(categorized)
    
    def generate_markdown_summary(self, report: Dict):
        """Generate markdown summary for easy reading"""
        md_file = self.context7_dir / 'CONTEXT7_INTEGRATION_SUMMARY.md'
        
        with open(md_file, 'w') as f:
            f.write("# Context7 Integration Summary\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 📊 Codebase Statistics\n\n")
            f.write(f"- **Total Python Files:** {len(list(self.pythons_dir.rglob('*.py')))}\n")
            f.write(f"- **Total Functions:** {len(self.functions)}\n")
            f.write(f"- **Total Classes:** {len(self.classes)}\n")
            f.write(f"- **Unique Libraries:** {len(self.libraries)}\n")
            f.write(f"- **Total Imports:** {sum(self.imports.values())}\n\n")
            
            f.write("## 🔝 Top 20 Most Used Libraries\n\n")
            f.write("| Library | Usage Count | Sample Files |\n")
            f.write("|---------|-------------|--------------|\n")
            for item in report['most_used_libraries'][:20]:
                files_str = ', '.join([f"`{f}`" for f in item['files'][:3]])
                f.write(f"| `{item['library']}` | {item['usage_count']} | {files_str} |\n")
            f.write("\n")
            
            f.write("## 📚 Library Categories\n\n")
            for category, libs in report['library_categories'].items():
                f.write(f"### {category.title()}\n")
                f.write(f"- {', '.join([f'`{lib}`' for lib in libs[:10]])}\n")
                if len(libs) > 10:
                    f.write(f"- ... and {len(libs) - 10} more\n")
                f.write("\n")
            
            f.write("## 🚀 Context7 Ready Libraries\n\n")
            f.write("These libraries are good candidates for Context7 documentation:\n\n")
            for lib in report['context7_ready_libraries']:
                f.write(f"- `{lib}` - Used in {len(self.libraries.get(lib, []))} files\n")
            f.write("\n")
            
            f.write("## 💡 Next Steps\n\n")
            f.write("1. Use Context7 MCP server to fetch latest docs for these libraries\n")
            f.write("2. Compare Context7 docs with your existing code patterns\n")
            f.write("3. Generate updated code examples combining both\n")
            f.write("4. Create auto-documentation for your custom functions\n")
        
        print(f"  ✅ Summary saved: {md_file}")


def main():
    """Main entry point"""
    indexer = Context7CodebaseIndexer()
    indexer.analyze_codebase()
    
    print("\n" + "=" * 80)
    print("📋 Next Steps:")
    print("  1. Review: ~/pythons/.context7/CONTEXT7_INTEGRATION_SUMMARY.md")
    print("  2. Check: ~/pythons/.context7/codebase_index.json")
    print("  3. Use Context7 MCP server with your codebase knowledge")
    print("  4. Set up auto-invoke rules in Cursor/Warp")
    print("=" * 80)


if __name__ == '__main__':
    main()

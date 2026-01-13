#!/usr/bin/env python3
"""
Create master documentation index
Scans home directory for all documentation files
"""

import os
from pathlib import Path
from collections import defaultdict
import json
from datetime import datetime

HOME = Path.home()
DOCS_DIR = HOME / 'docs'

# Documentation extensions
DOC_EXTENSIONS = {'.md', '.markdown', '.txt', '.rst', '.mdx'}

# Categories
CATEGORIES = {
    'projects': ['workspace', 'github', 'pythons'],
    'guides': ['tutorial', 'guide', 'how-to', 'howto'],
    'references': ['reference', 'api', 'cheatsheet', 'cheat'],
    'config': ['.env.d', '.config', 'config'],
    'sites': ['sites-navigator', 'docs_', 'sphinx']
}

def categorize_doc(filepath):
    """Categorize documentation file"""
    path_str = str(filepath).lower()
    name = filepath.name.lower()
    
    # Check categories
    for category, keywords in CATEGORIES.items():
        if any(keyword in path_str for keyword in keywords):
            return category
    
    # Default
    if 'readme' in name:
        return 'projects'
    
    return 'other'

def scan_documentation():
    """Scan for all documentation files"""
    docs = defaultdict(list)
    
    print("=" * 70)
    print("📚 Scanning Documentation Files")
    print("=" * 70)
    print(f"\n🔍 Scanning: {HOME}\n")
    
    # Priority directories
    priority_dirs = [
        HOME / 'workspace',
        HOME / 'GitHub',
        HOME / 'pythons',
        HOME / 'Documents',
        HOME / '.env.d',
        HOME / 'docs_docsify',
        HOME / 'docs_mkdocs',
        HOME / 'docs_seo',
        HOME / 'sphinx-docs'
    ]
    
    for dir_path in priority_dirs:
        if not dir_path.exists():
            continue
        
        print(f"  📂 {dir_path.name}/")
        count = 0
        
        for filepath in dir_path.rglob('*'):
            if not filepath.is_file():
                continue
            
            if filepath.suffix.lower() not in DOC_EXTENSIONS:
                continue
            
            # Skip certain directories
            if any(skip in str(filepath) for skip in ['node_modules', '.git', 'Library', '__pycache__']):
                continue
            
            try:
                stat = filepath.stat()
                category = categorize_doc(filepath)
                
                doc_info = {
                    'path': str(filepath),
                    'name': filepath.name,
                    'category': category,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'relative': str(filepath.relative_to(HOME))
                }
                
                docs[category].append(doc_info)
                count += 1
            except:
                continue
        
        if count > 0:
            print(f"     ✓ Found {count} docs")
    
    return docs

def generate_index(docs):
    """Generate master index"""
    index_content = f"""# Master Documentation Index

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📚 Documentation Catalog

Total files: {sum(len(v) for v in docs.values())}

"""
    
    for category, files in sorted(docs.items()):
        index_content += f"\n### {category.title()} ({len(files)} files)\n\n"
        
        for doc in sorted(files, key=lambda x: x['name'])[:20]:
            index_content += f"- [{doc['name']}]({doc['relative']})\n"
            index_content += f"  - Path: `{doc['relative']}`\n"
            index_content += f"  - Modified: {doc['modified'][:10]}\n\n"
    
    return index_content

def main():
    # Create docs directory
    DOCS_DIR.mkdir(exist_ok=True)
    
    # Scan documentation
    docs = scan_documentation()
    
    # Generate index
    index_content = generate_index(docs)
    
    # Save index
    index_file = DOCS_DIR / 'index.md'
    index_file.write_text(index_content, encoding='utf-8')
    
    # Save JSON catalog
    catalog = {
        'timestamp': datetime.now().isoformat(),
        'total_files': sum(len(v) for v in docs.values()),
        'categories': {k: len(v) for k, v in docs.items()},
        'files': {k: v[:50] for k, v in docs.items()}
    }
    
    catalog_file = DOCS_DIR / 'catalog.json'
    with open(catalog_file, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Index created: {index_file}")
    print(f"✅ Catalog saved: {catalog_file}")
    print(f"\n📊 Summary:")
    for category, files in sorted(docs.items()):
        print(f"   {category:15} {len(files):>4} files")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Enhanced Script Categorization
Use your provided categories and code patterns to better organize scripts
"""

import csv
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class EnhancedCategorizer:
    """Categorize scripts using refined category structure"""
    
    def __init__(self):
        self.base_dir = Path.home() / 'Documents' / 'pythons'
        self.analysis_dir = self.base_dir / '_analysis'
        
        # Your refined categories
        self.categories = {
            'Code Analysis & Refactoring': {
                'keywords': ['analyze-code', 'lint', 'complexity', 'refactor', 'review', 'quality'],
                'scripts': []
            },
            'Data Processing & Conversion': {
                'keywords': ['csv', 'json', 'convert', 'parse', 'extract', 'process-'],
                'scripts': []
            },
            'File & Folder Organization': {
                'keywords': ['organize', 'clean', 'rename', 'sort', 'flatten', 'consolidate'],
                'scripts': []
            },
            'Content Generation & Creation': {
                'keywords': ['generate', 'create', 'content-', 'builder', 'producer'],
                'scripts': []
            },
            'Automation & Bot Frameworks': {
                'keywords': ['bot-', 'automation', 'instagram-', 'youtube-', 'schedule'],
                'scripts': []
            },
            'Media Processing (Images)': {
                'keywords': ['image-', 'leonardo', 'dalle', 'stability', 'upscale', 'resize'],
                'scripts': []
            },
            'Media Processing (Audio/Video)': {
                'keywords': ['audio', 'video', 'transcribe', 'suno', 'elevenlabs', 'whisper', 'ffmpeg'],
                'scripts': []
            },
            'Web Scraping & Downloading': {
                'keywords': ['scrape', 'download', 'fetch', 'crawler', 'spider'],
                'scripts': []
            },
            'API Integration Utilities': {
                'keywords': ['openai', 'claude', 'anthropic', 'api-', '-api'],
                'scripts': []
            },
            'HTML & Gallery Generation': {
                'keywords': ['html', 'gallery', 'discography', 'photo-', 'webpage'],
                'scripts': []
            },
            'Testing & Quality Assurance': {
                'keywords': ['test', 'check-', 'validate', 'verify', 'diagnose'],
                'scripts': []
            },
            'Database & Cache Operations': {
                'keywords': ['database', 'sqlite', 'cache', 'db-', 'postgres'],
                'scripts': []
            },
            'Config & Setup Utilities': {
                'keywords': ['config', 'setup', 'install', 'env-', 'loader'],
                'scripts': []
            },
            'Experimental/Development': {
                'keywords': ['test-', 'dev-', 'experimental', 'prototype', 'draft'],
                'scripts': []
            },
        }
    
    def categorize_scripts(self):
        """Categorize all scripts using refined categories"""
        print("???  Enhanced Script Categorization")
        print("=" * 80)
        
        py_files = [f for f in self.base_dir.glob('*.py') if not f.name.startswith('_')]
        print(f"\nCategorizing {len(py_files)} scripts...")
        
        uncategorized = []
        
        for filepath in py_files:
            filename_lower = filepath.name.lower()
            categorized = False
            
            for category, info in self.categories.items():
                if categorized:
                    break
                    
                for keyword in info['keywords']:
                    if keyword in filename_lower:
                        info['scripts'].append({
                            'filename': filepath.name,
                            'path': str(filepath),
                            'size_kb': filepath.stat().st_size / 1024
                        })
                        categorized = True
                        break
            
            if not categorized:
                uncategorized.append(filepath.name)
        
        print(f"? Categorization complete")
        print(f"  ? Categorized: {len(py_files) - len(uncategorized)}")
        print(f"  ? Uncategorized: {len(uncategorized)}")
        
        return uncategorized
    
    def generate_enhanced_docs(self):
        """Generate documentation with enhanced categories"""
        doc = f"""# ?? Python Automation Arsenal - Enhanced Organization

> **Reorganized**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> **Total Scripts**: {sum(len(cat['scripts']) for cat in self.categories.values())}
> **Categories**: {len([c for c in self.categories.values() if c['scripts']])}

---

## ?? Scripts by Category

"""
        
        for category, info in sorted(self.categories.items()):
            if not info['scripts']:
                continue
            
            scripts = info['scripts']
            total_size = sum(s['size_kb'] for s in scripts)
            
            doc += f"\n### {category} ({len(scripts)} scripts)\n\n"
            
            # List scripts
            for script in sorted(scripts, key=lambda x: x['filename']):
                doc += f"- **{script['filename']}** ({script['size_kb']:.1f} KB)\n"
            
            doc += f"\n_Total: {total_size:.1f} KB_\n\n"
            doc += "---\n"
        
        # Save
        doc_path = self.base_dir / 'SCRIPTS_BY_CATEGORY.md'
        with open(doc_path, 'w') as f:
            f.write(doc)
        
        print(f"\n? Documentation: {doc_path}")
        return doc_path
    
    def generate_category_csv(self):
        """Generate CSV with category assignments"""
        csv_path = self.analysis_dir / 'SCRIPTS_CATEGORIZED.csv'
        
        rows = []
        for category, info in self.categories.items():
            for script in info['scripts']:
                rows.append({
                    'category': category,
                    'filename': script['filename'],
                    'path': script['path'],
                    'size_kb': f"{script['size_kb']:.1f}"
                })
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['category', 'filename', 'path', 'size_kb'])
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"? CSV: {csv_path}")
        return csv_path
    
    def print_summary(self, uncategorized):
        """Print categorization summary"""
        print("\n" + "=" * 80)
        print("?? CATEGORIZATION SUMMARY")
        print("=" * 80)
        
        for category, info in sorted(self.categories.items(), key=lambda x: -len(x[1]['scripts'])):
            if info['scripts']:
                print(f"\n{category}: {len(info['scripts'])} scripts")
        
        if uncategorized:
            print(f"\n??  Uncategorized: {len(uncategorized)} scripts")
            print("  (First 10):")
            for name in uncategorized[:10]:
                print(f"    ? {name}")

def main():
    from datetime import datetime
    
    categorizer = EnhancedCategorizer()
    
    # Categorize
    uncategorized = categorizer.categorize_scripts()
    
    # Generate docs
    doc_path = categorizer.generate_enhanced_docs()
    
    # Generate CSV
    csv_path = categorizer.generate_category_csv()
    
    # Summary
    categorizer.print_summary(uncategorized)
    
    print("\n" + "=" * 80)
    print("? ENHANCED CATEGORIZATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Filter Bad Names - Identify only files that truly need renaming
Focuses on vague, misleading, or unclear names
"""

import csv
from pathlib import Path
from datetime import datetime

class BadNameFilter:
    """Filter for files with genuinely bad names"""
    
    def __init__(self, csv_path):
        self.csv_path = Path(csv_path)
        self.scripts = []
        self.bad_names = []
        
    def load_csv(self):
        """Load CSV data"""
        with open(self.csv_path, 'r') as f:
            reader = csv.DictReader(f)
            self.scripts = list(reader)
        print(f"✅ Loaded {len(self.scripts)} scripts")
    
    def is_bad_name(self, script):
        """Determine if filename is bad/vague"""
        current = script['current_name']
        desc = script['description'].lower()
        
        # Patterns that indicate BAD names
        bad_patterns = [
            # Too generic
            (r'^analyze-', "Generic 'analyze-' prefix doesn't say what it analyzes"),
            (r'^process-', "Generic 'process-' prefix doesn't describe processing"),
            (r'^test\.py$', "Too generic - what does it test?"),
            (r'^build\.py$', "Too generic - what does it build?"),
            (r'^main\.py$', "Too generic - main for what?"),
            (r'^script\.py$', "Literally just 'script'"),
            (r'^tool\.py$', "Too generic"),
            (r'^utils?\.py$', "Too generic"),
            (r'^helpers?\.py$', "Too generic"),
            
            # ALL_CAPS or SHOUTING
            (r'^[A-Z_]+\.py$', "ALL_CAPS naming - should use lowercase"),
            
            # Version numbers/copies
            (r'-v?\d+\.py$', "Has version number - consolidate versions"),
            (r'-copy\.py$', "Is a copy - remove or consolidate"),
            (r'\s+\(\d+\)\.py$', "Has (1), (2) - duplicate file"),
            
            # Single generic words
            (r'^(check|run|make|do|get|set|update|create)\.py$', "Single generic verb"),
            
            # Project-specific that should be descriptive
            (r'^(claude|anthropic|openai|gemini)-(?!.*-(analyzer|generator|downloader|uploader|scraper))', 
             "API name prefix but unclear what it does"),
        ]
        
        # Check each pattern
        import re
        for pattern, reason in bad_patterns:
            if re.search(pattern, current, re.IGNORECASE):
                return True, reason
        
        # Check for mismatched name vs description
        # If name says one thing but description says another
        name_lower = current.lower()
        
        if 'download' in name_lower and 'download' not in desc and 'scrap' not in desc:
            return True, "Name says 'download' but description doesn't match"
        
        if 'upload' in name_lower and 'upload' not in desc and 'post' not in desc:
            return True, "Name says 'upload' but description doesn't match"
        
        if 'analyzer' in name_lower and 'analyz' not in desc:
            return True, "Name says 'analyzer' but description doesn't match"
        
        # No description found
        if 'no description found' in desc:
            return True, "Missing documentation - unclear purpose"
        
        return False, ""
    
    def filter_bad_names(self):
        """Filter for only bad names"""
        print("\n🔍 Filtering for bad/vague names...")
        
        for script in self.scripts:
            is_bad, reason = self.is_bad_name(script)
            
            if is_bad:
                script['bad_name_reason'] = reason
                self.bad_names.append(script)
        
        print(f"✅ Found {len(self.bad_names)} files with bad/vague names")
        print(f"✅ {len(self.scripts) - len(self.bad_names)} files have good names")
    
    def save_bad_names_csv(self):
        """Save filtered bad names CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = self.csv_path.parent / f'_needs_renaming_{timestamp}.csv'
        
        fieldnames = [
            'current_name',
            'description',
            'category',
            'apis_used',
            'lines',
            'size_kb',
            'bad_name_reason',
            'suggested_name',
            'action',
            'reason'
        ]
        
        # Sort by category
        sorted_bad = sorted(self.bad_names, key=lambda x: (x['category'], x['current_name']))
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_bad)
        
        return output_path
    
    def print_summary(self):
        """Print summary by category"""
        by_category = {}
        for script in self.bad_names:
            cat = script['category']
            by_category.setdefault(cat, []).append(script)
        
        print("\n" + "="*80)
        print("📊 BAD NAMES BY CATEGORY")
        print("="*80)
        
        for category in sorted(by_category.keys(), key=lambda x: len(by_category[x]), reverse=True):
            scripts = by_category[category]
            print(f"\n📂 {category}: {len(scripts)} files need renaming")
            
            # Show top 5 examples
            for i, script in enumerate(scripts[:5], 1):
                print(f"   {i}. {script['current_name']}")
                print(f"      Issue: {script['bad_name_reason']}")
                print(f"      Does: {script['description'][:80]}")


def main():
    csv_path = Path.home() / 'pythons' / '_all_scripts_analysis_20251106_132427.csv'
    
    filter = BadNameFilter(csv_path)
    filter.load_csv()
    filter.filter_bad_names()
    filter.print_summary()
    
    output_csv = filter.save_bad_names_csv()
    
    print(f"\n{'='*80}")
    print("💾 Files needing rename saved to:")
    print(f"   {output_csv}")
    print(f"\n💡 These {len(filter.bad_names)} files need your attention!")
    print(f"   {len(filter.scripts) - len(filter.bad_names)} files already have good names ✅")


if __name__ == '__main__':
    main()

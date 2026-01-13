#!/usr/bin/env python3
"""
As-a-Man-Thinketh Content-Aware Renamer
Specialized renaming for the As-a-man-thinketh directory with massive duplicate cleanup
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
import hashlib

class ThinkethContentRenamer:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir)
        self.rename_log = []
        self.files_renamed = 0
        self.duplicates_removed = 0
        self.space_saved = 0
        
    def clean_filename(self, filename):
        """Clean filename by removing problematic characters and patterns"""
        # Remove common problematic patterns
        patterns_to_remove = [
            r'_truncated_',
            r'x27;',  # HTML entity for apostrophe
            r'ud83d_udcc1',  # Unicode emoji encoding
            r'ud83c_udfa8',  # Unicode emoji encoding
            r'ud83c_udf0d',  # Unicode emoji encoding
            r'&#x2[0-9a-fA-F]+;',  # HTML entities
            r'&quot;',  # HTML entities
            r'&amp;',  # HTML entities
            r'&lt;',  # HTML entities
            r'&gt;',  # HTML entities
            r'[^\w\s\-\.]',  # Remove special characters except word chars, spaces, hyphens, dots
        ]
        
        cleaned = filename
        for pattern in patterns_to_remove:
            cleaned = re.sub(pattern, '', cleaned)
        
        # Clean up multiple spaces and underscores
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = re.sub(r'_+', '_', cleaned)
        cleaned = re.sub(r'-+', '-', cleaned)
        
        # Remove leading/trailing spaces and underscores
        cleaned = cleaned.strip(' _-')
        
        return cleaned
    
    def extract_content_theme(self, content):
        """Extract main theme/topic from file content"""
        content_lower = content.lower()
        
        # Define theme patterns specific to As-a-Man-Thinketh
        themes = {
            'book_analysis': ['as a man thinketh', 'james allen', 'project gutenberg', 'book analysis', 'thought and character'],
            'project_analysis': ['project analysis', 'generated:', 'files:', 'total size:', 'chat id:'],
            'seo_optimization': ['seo', 'optimization', 'search engine', 'ranking', 'keywords', 'meta'],
            'content_creation': ['content', 'creation', 'creative', 'assets', 'media', 'writing'],
            'web_development': ['web', 'development', 'html', 'css', 'javascript', 'react'],
            'automation': ['automation', 'script', 'automated', 'workflow', 'process'],
            'business_analysis': ['business', 'analysis', 'roi', 'revenue', 'profit', 'value'],
            'technical_guide': ['technical', 'guide', 'implementation', 'setup', 'configuration'],
            'chat_analysis': ['chat', 'conversation', 'discussion', 'chat id', 'analysis'],
            'file_management': ['file', 'management', 'organize', 'structure', 'directory'],
            'data_analysis': ['data', 'analysis', 'metrics', 'statistics', 'performance'],
            'philosophy': ['philosophy', 'wisdom', 'thought', 'mind', 'character', 'purpose'],
            'self_development': ['self', 'development', 'growth', 'improvement', 'personal'],
            'spiritual': ['spiritual', 'soul', 'divine', 'heaven', 'blessed', 'holy']
        }
        
        # Find matching themes
        matched_themes = []
        for theme, patterns in themes.items():
            if any(pattern in content_lower for pattern in patterns):
                matched_themes.append(theme)
        
        return matched_themes
    
    def extract_key_terms(self, content):
        """Extract key terms from content for better naming"""
        # Extract words from headers and important sections
        lines = content.split('\n')
        key_terms = []
        
        for line in lines[:100]:  # Look at first 100 lines
            line = line.strip()
            if line.startswith('#') or line.startswith('**') or line.startswith('-'):
                # Extract meaningful words
                words = re.findall(r'\b[A-Za-z]{3,}\b', line)
                key_terms.extend(words[:3])  # Take first 3 words
        
        # Remove common words
        common_words = {'the', 'and', 'for', 'with', 'this', 'that', 'from', 'into', 'your', 'are', 'has', 'have', 'will', 'can', 'should', 'project', 'analysis', 'generated', 'files', 'total', 'size', 'words', 'chat', 'id', 'categories', 'code', 'blocks', 'tool', 'calls', 'modified', 'man', 'thinketh', 'james', 'allen'}
        key_terms = [word.lower() for word in key_terms if word.lower() not in common_words]
        
        return key_terms[:5]  # Return top 5 key terms
    
    def generate_new_name(self, original_name, content, themes, key_terms):
        """Generate a new descriptive name based on content analysis"""
        # Start with cleaned original name
        base_name = self.clean_filename(original_name)
        
        # Remove extensions temporarily
        if base_name.endswith('.md'):
            base_name = base_name[:-3]
        if base_name.endswith('.seo_backup'):
            base_name = base_name[:-11]
        
        # Special handling for different file types
        if 'seo_backup' in original_name:
            if themes:
                primary_theme = themes[0].replace('_', ' ').title()
                if key_terms:
                    key_term = key_terms[0].title()
                    new_name = f"{primary_theme}_{key_term}_SEO_Backup"
                else:
                    new_name = f"{primary_theme}_SEO_Backup"
            else:
                new_name = "As_Man_Thinketh_SEO_Backup"
        elif 'analysis' in base_name.lower() or 'ANALYSIS' in base_name:
            if themes:
                primary_theme = themes[0].replace('_', ' ').title()
                if key_terms:
                    key_term = key_terms[0].title()
                    new_name = f"{primary_theme}_{key_term}_Analysis"
                else:
                    new_name = f"{primary_theme}_Analysis"
            else:
                new_name = "As_Man_Thinketh_Analysis"
        elif 'as a man thinketh' in base_name.lower() or 'as a ma' in base_name.lower():
            if themes:
                primary_theme = themes[0].replace('_', ' ').title()
                new_name = f"As_Man_Thinketh_{primary_theme}"
            else:
                new_name = "As_Man_Thinketh_Book"
        else:
            # Try to create a meaningful name from themes and key terms
            if themes and key_terms:
                theme = themes[0].replace('_', ' ').title()
                key_term = key_terms[0].title()
                new_name = f"{theme}_{key_term}"
            elif themes:
                new_name = themes[0].replace('_', ' ').title()
            elif key_terms:
                new_name = key_terms[0].title()
            else:
                new_name = base_name
        
        # Clean up the new name
        new_name = re.sub(r'[^\w\s\-]', '', new_name)
        new_name = re.sub(r'\s+', '_', new_name)
        new_name = re.sub(r'_+', '_', new_name)
        new_name = new_name.strip('_')
        
        # Add appropriate extension back
        if 'seo_backup' in original_name:
            new_name += '.seo_backup'
        else:
            new_name += '.md'
        
        return new_name
    
    def is_duplicate_name(self, new_name, existing_files):
        """Check if the new name already exists"""
        return new_name in existing_files
    
    def get_unique_name(self, base_name, existing_files):
        """Get a unique name by adding a number if needed"""
        if base_name not in existing_files:
            return base_name
        
        counter = 1
        name_parts = base_name.rsplit('.', 1)
        if len(name_parts) == 2:
            base, ext = name_parts
            while f"{base}_{counter}.{ext}" in existing_files:
                counter += 1
            return f"{base}_{counter}.{ext}"
        else:
            while f"{base_name}_{counter}" in existing_files:
                counter += 1
            return f"{base_name}_{counter}"
    
    def analyze_and_rename_file(self, file_path, existing_files):
        """Analyze a single file and rename it"""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract themes and key terms
            themes = self.extract_content_theme(content)
            key_terms = self.extract_key_terms(content)
            
            # Generate new name
            new_name = self.generate_new_name(file_path.name, content, themes, key_terms)
            
            # Ensure unique name
            new_name = self.get_unique_name(new_name, existing_files)
            
            # Only rename if the name actually changed
            if new_name != file_path.name:
                new_path = file_path.parent / new_name
                
                # Log the rename
                self.rename_log.append({
                    'original': str(file_path),
                    'new': str(new_path),
                    'themes': themes,
                    'key_terms': key_terms,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Rename the file
                file_path.rename(new_path)
                self.files_renamed += 1
                
                print(f"✅ Renamed: {file_path.name} → {new_name}")
                print(f"   Themes: {', '.join(themes) if themes else 'None'}")
                print(f"   Key terms: {', '.join(key_terms[:3]) if key_terms else 'None'}")
                print()
                
                return new_name
            else:
                print(f"⏭️  Skipped: {file_path.name} (no change needed)")
                return file_path.name
                
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {str(e)}")
            return file_path.name
    
    def process_directory(self):
        """Process all files in the target directory"""
        print(f"🔍 Analyzing files in: {self.target_dir}")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Get all files (md and seo_backup)
        all_files = list(self.target_dir.glob("*"))
        md_files = [f for f in all_files if f.suffix == '.md']
        seo_files = [f for f in all_files if f.suffix == '.seo_backup']
        
        print(f"📄 Found {len(md_files)} markdown files")
        print(f"📄 Found {len(seo_files)} SEO backup files")
        print(f"📄 Total files to process: {len(all_files)}")
        print()
        
        # Track existing filenames to avoid duplicates
        existing_files = set()
        
        # Process each file
        for file_path in all_files:
            new_name = self.analyze_and_rename_file(file_path, existing_files)
            existing_files.add(new_name)
        
        # Save rename log
        log_file = self.target_dir.parent / "cleanup_logs" / f"thinketh_renaming_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_file.parent.mkdir(exist_ok=True)
        
        log_data = {
            'rename_date': datetime.now().isoformat(),
            'target_directory': str(self.target_dir),
            'files_renamed': self.files_renamed,
            'total_files_processed': len(all_files),
            'md_files': len(md_files),
            'seo_files': len(seo_files),
            'rename_actions': self.rename_log
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print("=" * 80)
        print("🎉 AS-A-MAN-THINKETH RENAMING COMPLETE!")
        print(f"📊 Files renamed: {self.files_renamed}")
        print(f"📄 Total files processed: {len(all_files)}")
        print(f"📝 Log saved to: {log_file}")
        print("=" * 80)

def main():
    # Target the As-a-man-thinketh directory
    thinketh_dir = Path.home() / "Documents" / "As-a-man-thinketh"
    
    if not thinketh_dir.exists():
        print(f"❌ Error: Directory {thinketh_dir} does not exist")
        return
    
    print("🧠 As-a-Man-Thinketh Content-Aware Renamer")
    print("📂 Target directory: ~/Documents/As-a-man-thinketh")
    print("🎯 Will analyze content and create descriptive filenames")
    print("📚 Specialized for book analysis and philosophy content")
    print()
    
    # Run the renamer
    renamer = ThinkethContentRenamer(thinketh_dir)
    renamer.process_directory()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Directory consolidation script for AVATARARTS project
Groups related directories into broader categories to reduce the number of top-level directories
"""
import os
import shutil
from pathlib import Path

def create_consolidated_structure():
    """Create a consolidated directory structure"""
    print("🏗️  CREATING CONSOLIDATED DIRECTORY STRUCTURE")
    print("="*60)
    
    # Define the new consolidated structure
    consolidated_dirs = {
        'AI_TOOLS': [
            'Ai-Empire',
            'ai-voice-agents', 
            'intelligencTtools',
            'oLLaMa'
        ],
        'CODE_PROJECTS': [
            'avatararts',
            'avatararts-deployment',
            'code-repos',
            'advanced_toolkit'
        ],
        'CONTENT_ASSETS': [
            'ai-ml-notes',
            'ai-sites',
            'content',
            'html-assets',
            'images',
            'audio-analysis',
            'music-analysis',
            'music-empire'
        ],
        'BUSINESS_PROJECTS': [
            'passive-income-empire',
            'retention-suite-complete',
            'cleanconnect-complete',
            'quantumforge-complete',
            'marketplace',
            'education'
        ],
        'SEO_MARKETING': [
            'SEO Content Optimization Suite',
            'SEO Content Optimization Suite',
            'SEO_CONTENT_STRATEGY',
            'SEO_YouTube_2025_Dataset',
            'seo-domination-engine',
            'MASTER_SEO_PACKAGE_2024'
        ],
        'CLIENT_PROJECTS': [
            'josephrosadomd',
            'Dr_Adu_GainesvillePFS_SEO_Project',
            'steven-chaplinski-website'
        ],
        'DATA_ANALYTICS': [
            'data',
            'Data-Analysis',
            'csvs-consolidated',
            'analysis',
            'reports',
            'json'
        ],
        'UTILITIES_TOOLS': [
            'tools',
            'scripts',
            'configs',
            'organization-tools',
            'n8n-local'
        ],
        'ARCHIVES_BACKUPS': [
            'archive',
            'archives',
            'exports',
            'documents'
        ],
        'OTHER_MISC': [
            'assets',
            'guides',
            'strategies',
            'templates',
            'Portfolio',
            'JOB_SEARCH_2025',
            'TOP_TRENDS_AVATARARTS_QUANTUMFORGE'
        ]
    }
    
    # Create the new consolidated directories
    for category, dirs in consolidated_dirs.items():
        Path(category).mkdir(exist_ok=True)
        print(f"Created directory: {category}/")
    
    # Move directories into their consolidated categories
    moved_count = 0
    for category, dirs in consolidated_dirs.items():
        for dir_name in dirs:
            source_path = Path(dir_name)
            dest_path = Path(category) / dir_name
            
            if source_path.exists() and source_path.is_dir():
                if not dest_path.exists():
                    try:
                        shutil.move(str(source_path), str(dest_path))
                        print(f"  Moved {dir_name}/ -> {category}/{dir_name}/")
                        moved_count += 1
                    except Exception as e:
                        print(f"  Error moving {dir_name}: {e}")
                else:
                    print(f"  Warning: {dest_path} already exists, skipping {dir_name}")
    
    print(f"\n✅ Consolidation complete!")
    print(f"  - Created {len(consolidated_dirs)} consolidated directories")
    print(f"  - Moved {moved_count} directories into consolidated structure")
    print(f"  - Reduced top-level directories from many to {len(consolidated_dirs)} main categories")
    
    return consolidated_dirs

def show_before_after(consolidated_dirs):
    """Show the before and after directory structure"""
    print(f"\n📊 DIRECTORY CONSOLIDATION SUMMARY")
    print("="*60)
    
    print(f"BEFORE: Many scattered directories")
    print(f"AFTER: Consolidated into {len(consolidated_dirs)} main categories:")
    print()
    
    for category, dirs in consolidated_dirs.items():
        print(f"📁 {category}/")
        for dir_name in dirs:
            print(f"   └── {dir_name}/")
        print()

def main():
    print("AVATARARTS DIRECTORY CONSOLIDATION")
    print("Reducing number of top-level directories by grouping related content")
    print("="*70)
    
    consolidated_dirs = create_consolidated_structure()
    show_before_after(consolidated_dirs)
    
    print(f"\n🎯 BENEFITS OF CONSOLIDATION:")
    print(f"  • Reduced cognitive load from many scattered directories")
    print(f"  • Logical grouping of related projects and tools")
    print(f"  • Easier navigation and maintenance")
    print(f"  • Better organization by function/domain")
    
    print(f"\n💡 NOTE: Some directories may have been skipped if they already existed in target location")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Content-Aware Organization System
Creates subdirectories based on content categories and symbolic links to original files
"""

import csv
import json
from pathlib import Path
from datetime import datetime
import os


def create_content_aware_organization():
    """Create content-aware folder organization based on the catalog"""
    base_dir = Path("/Users/steven/pythons")
    catalog_dir = base_dir / "CONTENT_AWARE_CATALOG"
    
    # Read the CSV catalog
    csv_files = list(catalog_dir.glob("python_files_catalog_*.csv"))
    if not csv_files:
        print("❌ No catalog CSV file found")
        return
    
    csv_file = csv_files[0]  # Get the most recent one
    print(f"📁 Reading catalog: {csv_file.name}")
    
    # Create content-aware directories
    content_org_dir = catalog_dir / "CONTENT_ORGANIZED"
    content_org_dir.mkdir(exist_ok=True)
    
    # Read the catalog
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        catalog_data = list(reader)
    
    # Create category directories and organize files
    category_dirs = {}
    for row in catalog_data:
        category = row['primary_category']
        
        # Create category directory if it doesn't exist
        if category not in category_dirs:
            clean_category = category.replace('/', '_').replace(' ', '_')
            cat_dir = content_org_dir / clean_category
            cat_dir.mkdir(exist_ok=True)
            category_dirs[category] = cat_dir
        
        # Create symbolic link to original file in category directory
        original_file = Path(row['absolute_path'])
        link_name = category_dirs[category] / original_file.name
        
        # Handle duplicate filenames by adding unique suffixes
        counter = 1
        original_link_name = link_name
        while link_name.exists():
            stem = original_link_name.stem
            suffix = original_link_name.suffix
            link_name = category_dirs[category] / f"{stem}_{counter}{suffix}"
            counter += 1
        
        # Create symbolic link
        try:
            link_name.symlink_to(original_file)
        except OSError as e:
            # Fallback: copy the file if symbolic link fails
            import shutil
            shutil.copy2(original_file, link_name)
    
    # Create tag-based directories as well
    tag_based_dir = content_org_dir / "TAG_BASED"
    tag_based_dir.mkdir(exist_ok=True)
    
    # Extract all unique tags
    all_tags = set()
    for row in catalog_data:
        tags = row['tags'].split(', ')
        all_tags.update(tags)
    
    # Create a directory for each tag and link files that have that tag
    for tag in all_tags:
        if tag.strip():  # Skip empty tags
            # Replace problematic characters in tag names
            clean_tag = tag.strip().replace(' ', '_').replace('/', '_').replace('\\', '_')
            tag_dir = tag_based_dir / clean_tag
            tag_dir.mkdir(exist_ok=True)
            
            # Find all files with this tag and create links
            for row in catalog_data:
                file_tags = row['tags'].split(', ')
                if tag in file_tags:
                    original_file = Path(row['absolute_path'])
                    link_file = tag_dir / original_file.name
                    
                    # Handle duplicates
                    counter = 1
                    original_link_file = link_file
                    while link_file.exists():
                        stem = original_link_file.stem
                        suffix = original_link_file.suffix
                        link_file = tag_dir / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    try:
                        link_file.symlink_to(original_file)
                    except OSError:
                        # Fallback: copy the file
                        import shutil
                        shutil.copy2(original_file, link_file)
    
    # Create a summary of the organization
    summary_path = content_org_dir / "ORGANIZATION_SUMMARY.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# Content-Aware Organization Summary\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Categories\n\n")
        for category, cat_dir in category_dirs.items():
            file_count = len([f for f in cat_dir.iterdir() if f.is_file()])
            f.write(f"- **{category}**: {file_count} files\n")
        
        f.write(f"\n## Tag-Based Organization\n")
        f.write(f"- Tag directories created: {len([d for d in tag_based_dir.iterdir() if d.is_dir()])}\n")
        f.write(f"- Unique tags identified: {len(all_tags)}\n\n")
        
        f.write("### Top Tags:\n")
        tag_counts = {}
        for row in catalog_data:
            for tag in row['tags'].split(', '):
                if tag.strip():
                    tag_counts[tag.strip()] = tag_counts.get(tag.strip(), 0) + 1
        
        # Sort tags by count
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        for tag, count in sorted_tags[:15]:  # Top 15 tags
            f.write(f"- **{tag}**: {count} files\n")
    
    print(f"✅ Content-aware organization created in: {content_org_dir}")
    print(f"📊 Summary saved to: {summary_path}")
    
    # Also create a JSON representation of the organization
    org_json = {
        "generated": datetime.now().isoformat(),
        "base_directory": str(base_dir),
        "organization_path": str(content_org_dir),
        "category_counts": {cat: len([f for f in cat_dir.iterdir() if f.is_file()]) 
                           for cat, cat_dir in category_dirs.items()},
        "tag_counts": tag_counts,
        "total_categories": len(category_dirs),
        "total_tags": len(all_tags)
    }
    
    json_path = content_org_dir / "organization_structure.json"
    with open(json_path, 'w') as f:
        json.dump(org_json, f, indent=2)
    
    print(f"📄 JSON structure saved to: {json_path}")
    return content_org_dir, summary_path


def main():
    print("🚀 Creating Content-Aware Organization System")
    org_dir, summary_path = create_content_aware_organization()
    print(f"✅ Content-aware organization system complete!")
    print(f"📁 Organization path: {org_dir}")
    print(f"📊 Summary: {summary_path}")


if __name__ == "__main__":
    main()
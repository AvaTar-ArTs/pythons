import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
AVATARARTS Consolidation and Merging Tool
Uses the indexes to identify consolidation opportunities and merge similar content
"""

import pandas as pd
import os
from pathlib import Path
import shutil
from collections import defaultdict
import csv

def load_indexes():
    """Load the created indexes"""
    print("Loading indexes...")
    
    main_index = pd.read_csv("/Users/steven/AVATARARTS_MAIN_INDEX.csv")
    function_index = pd.read_csv("/Users/steven/AVATARARTS_FUNCTION_INDEX.csv")
    duplicates_index = pd.read_csv("/Users/steven/AVATARARTS_DUPLICATES_INDEX.csv")
    directory_analysis = pd.read_csv("/Users/steven/AVATARARTS_DIRECTORY_ANALYSIS.csv")
    
    return main_index, function_index, duplicates_index, directory_analysis

def identify_consolidation_opportunities(main_index, directory_analysis):
    """Identify directories that could be consolidated"""
    print("\nIdentifying consolidation opportunities...")
    
    # Find directories with similar content types
    content_similarities = directory_analysis.groupby('extensions')['directory'].apply(list).reset_index()
    
    # Find directories with low file counts that could be merged
    sparse_directories = directory_analysis[
        (directory_analysis['file_count'] < 5) & 
        (directory_analysis['path_depth'] > 3)
    ]
    
    # Find directories with similar function classifications
    function_groups = main_index.groupby('function_classification')['directory'].apply(list).reset_index()
    function_groups['unique_dirs'] = function_groups['directory'].apply(lambda x: list(set(x)))
    
    return content_similarities, sparse_directories, function_groups

def create_consolidation_plan(main_index, duplicates_index, sparse_directories):
    """Create a plan for consolidation"""
    print("\nCreating consolidation plan...")
    
    consolidation_plan = []
    
    # Plan for duplicate removal
    for _, row in duplicates_index.iterrows():
        if row['duplicate_count'] > 1:
            paths = row['duplicate_paths'].split('; ')
            keep_path = paths[0]  # Keep the first one
            remove_paths = paths[1:]  # Remove the rest
            
            consolidation_plan.append({
                'action': 'remove_duplicate',
                'keep_path': keep_path,
                'remove_paths': remove_paths,
                'potential_savings_mb': row['total_size_saved_mb']
            })
    
    # Plan for sparse directory consolidation
    for _, row in sparse_directories.iterrows():
        directory = row['directory']
        file_count = row['file_count']
        
        # Find similar directories based on content
        similar_dirs = main_index[
            (main_index['directory'] == directory) &
            (main_index['function_classification'] != 'Unknown')
        ]['function_classification'].value_counts().head(1)
        
        if not similar_dirs.empty:
            primary_function = similar_dirs.index[0]
            
            consolidation_plan.append({
                'action': 'merge_sparse_directory',
                'directory': directory,
                'primary_function': primary_function,
                'file_count': file_count
            })
    
    return consolidation_plan

def generate_merge_recommendations(main_index):
    """Generate recommendations for merging similar content"""
    print("\nGenerating merge recommendations...")
    
    # Group files by function classification
    function_groups = main_index.groupby('function_classification')
    
    merge_recommendations = []
    
    for func_class, group in function_groups:
        if len(group) > 1:  # Only consider classes with multiple files
            extensions = group['extension'].value_counts()
            directories = group['directory'].value_counts()
            
            # Recommend merging if multiple directories have same function
            if len(directories) > 1:
                merge_recommendations.append({
                    'function_classification': func_class,
                    'file_count': len(group),
                    'directory_count': len(directories),
                    'extensions': ', '.join(extensions.head(3).index.tolist()),
                    'directories': directories.head(5).index.tolist(),
                    'recommendation': f'Merge {func_class} files into single directory'
                })
    
    return merge_recommendations

def save_consolidation_report(consolidation_plan, merge_recommendations):
    """Save the consolidation report"""
    print("\nSaving consolidation report...")
    
    report_path = "/Users/steven/AVATARARTS_CONSOLIDATION_PLAN.csv"
    
    with open(report_path, 'w', newline='') as csvfile:
        fieldnames = [
            'action', 'details', 'estimated_savings_mb', 
            'priority', 'status', 'notes'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        # Write duplicate removal recommendations
        for item in consolidation_plan:
            if item['action'] == 'remove_duplicate':
                writer.writerow({
                    'action': 'Remove duplicate files',
                    'details': f"Keep: {item['keep_path'][:100]}..., Remove: {len(item['remove_paths'])} files",
                    'estimated_savings_mb': item['potential_savings_mb'],
                    'priority': 'High',
                    'status': 'Pending',
                    'notes': 'Duplicate files identified by hash'
                })
            elif item['action'] == 'merge_sparse_directory':
                writer.writerow({
                    'action': 'Merge sparse directory',
                    'details': f"Directory: {item['directory']}, Files: {item['file_count']}",
                    'estimated_savings_mb': 0,
                    'priority': 'Medium',
                    'status': 'Pending',
                    'notes': f"Merging based on function: {item['primary_function']}"
                })
        
        # Write merge recommendations
        for rec in merge_recommendations:
            writer.writerow({
                'action': 'Merge functionally similar directories',
                'details': f"Function: {rec['function_classification']}, Files: {rec['file_count']}, Dirs: {rec['directory_count']}",
                'estimated_savings_mb': 0,
                'priority': 'Medium',
                'status': 'Pending',
                'notes': f"Extensions: {rec['extensions']}, Directories: {len(rec['directories'])} affected"
            })
    
    print(f"Consolidation report saved to: {report_path}")

def create_smart_symlinks():
    """Create smart symlinks to maintain backward compatibility during consolidation"""
    print("\nCreating smart symlink strategy...")
    
    # This would create a strategy for maintaining backward compatibility
    # during the consolidation process
    symlink_strategy = """
    SMART SYMLINK STRATEGY FOR CONSOLIDATION:

    1. BEFORE moving any files:
       - Create symbolic links from old locations to new locations
       - Test all scripts to ensure they still work
       - Verify all functionality remains intact

    2. DURING consolidation:
       - Keep symlinks in place for 30 days minimum
       - Monitor for any broken references
       - Update internal references to use new paths

    3. AFTER consolidation:
       - Remove symlinks only after confirming no references
       - Update documentation to reflect new structure
       - Notify all stakeholders of path changes
    """
    
    with open("/Users/steven/SMART_SYMLINK_STRATEGY.md", "w") as f:
        f.write(symlink_strategy)
    
    print("Smart symlink strategy saved to: /Users/steven/SMART_SYMLINK_STRATEGY.md")

def main():
    """Main function to run the consolidation tool"""
    print("AVATARARTS Consolidation and Merging Tool")
    print("=" * 50)
    
    # Load indexes
    main_index, function_index, duplicates_index, directory_analysis = load_indexes()
    
    # Identify consolidation opportunities
    content_similarities, sparse_directories, function_groups = identify_consolidation_opportunities(
        main_index, directory_analysis
    )
    
    # Create consolidation plan
    consolidation_plan = create_consolidation_plan(
        main_index, duplicates_index, sparse_directories
    )
    
    # Generate merge recommendations
    merge_recommendations = generate_merge_recommendations(main_index)
    
    # Save consolidation report
    save_consolidation_report(consolidation_plan, merge_recommendations)
    
    # Create symlink strategy
    create_smart_symlinks()
    
    # Print summary
    print(f"\nSUMMARY:")
    print(f"- {len(consolidation_plan)} consolidation items identified")
    print(f"- {len(merge_recommendations)} merge recommendations generated")
    print(f"- Consolidation report saved to AVATARARTS_CONSOLIDATION_PLAN.csv")
    print(f"- Smart symlink strategy saved to SMART_SYMLINK_STRATEGY.md")
    
    print("\nNext steps:")
    print("1. Review AVATARARTS_CONSOLIDATION_PLAN.csv for prioritization")
    print("2. Follow SMART_SYMLINK_STRATEGY.md for backward compatibility")
    print("3. Begin consolidation with highest priority items first")
    print("4. Test thoroughly after each consolidation step")

try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)
#!/usr/bin/env python3
"""
Advanced file organizer with parent-folder content awareness for AVATARARTS project
"""
import os
import shutil
from pathlib import Path
import re

def analyze_parent_folder_context(directory):
    """Analyze the parent folder to understand the project context"""
    directory = Path(directory)
    
    # Look for project-specific patterns and keywords
    context_indicators = {
        'ai_ml': ['ai', 'ml', 'machine', 'learning', 'neural', 'model', 'algorithm'],
        'seo_marketing': ['seo', 'marketing', 'campaign', 'keyword', 'traffic', 'conversion'],
        'automation': ['automation', 'workflow', 'script', 'bot', 'auto', 'automate'],
        'music_audio': ['music', 'audio', 'suno', 'track', 'song', 'mp3', 'wav'],
        'content_creation': ['content', 'creation', 'video', 'image', 'design', 'creative'],
        'development': ['code', 'dev', 'develop', 'programming', 'script', 'function'],
        'analysis': ['analysis', 'data', 'report', 'statistic', 'metric', 'analytics']
    }
    
    # Analyze directory name and subdirectories
    dir_name = directory.name.lower()
    subdirs = [d.name.lower() for d in directory.iterdir() if d.is_dir()]
    
    # Score each context type
    context_scores = {}
    for context_type, keywords in context_indicators.items():
        score = 0
        # Check directory name
        for keyword in keywords:
            if keyword in dir_name:
                score += 2
        # Check subdirectory names
        for subdir in subdirs:
            for keyword in keywords:
                if keyword in subdir:
                    score += 1
        context_scores[context_type] = score
    
    # Return the context with highest score
    dominant_context = max(context_scores, key=context_scores.get)
    return dominant_context, context_scores

def get_advanced_file_categories(project_context):
    """Get file categories based on project context"""
    # Base categories
    base_categories = {
        'documents': {'.txt', '.pdf', '.doc', '.docx', '.rtf', '.odt', '.md'},
        'images': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'},
        'videos': {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'},
        'audio': {'.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg', '.wma'},
        'data': {'.csv', '.json', '.xml', '.yaml', '.yml', '.sql', '.db'},
        'scripts': {'.py', '.js', '.sh', '.bash', '.pl', '.rb', '.php', '.html', '.css'},
        'archives': {'.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.xz'},
        'configs': {'.env', '.ini', '.cfg', '.conf', '.toml', '.gitignore', '.dockerignore'}
    }
    
    # Context-specific categories
    context_categories = {
        'ai_ml': {
            'ai_models': {'.pkl', '.joblib', '.h5', '.pt', '.pth', '.onnx', '.model'},
            'ai_datasets': {'.parquet', '.pkl', '.npy', '.npz'},
            'ai_notebooks': {'.ipynb'}
        },
        'seo_marketing': {
            'seo_reports': {'.csv', '.xlsx', '.xls'},
            'marketing_assets': {'.psd', '.ai', '.xd'}
        },
        'automation': {
            'workflow_scripts': {'.py', '.js', '.sh', '.rb'},
            'automation_configs': {'.yaml', '.yml', '.json', '.env'}
        },
        'music_audio': {
            'music_tracks': {'.mp3', '.wav', '.flac', '.m4a'},
            'music_metadata': {'.json', '.txt', '.lrc'}
        },
        'content_creation': {
            'creative_assets': {'.psd', '.ai', '.xd', '.fig', '.sketch'},
            'content_templates': {'.html', '.css', '.jsx', '.tsx'}
        },
        'development': {
            'source_code': {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.go', '.rs'},
            'tests': {'.test.py', '.spec.js', '.test.js'}
        },
        'analysis': {
            'analytics_data': {'.csv', '.xlsx', '.parquet', '.json'},
            'reports': {'.pdf', '.html', '.md', '.ipynb'}
        }
    }
    
    # Merge base and context-specific categories
    categories = base_categories.copy()
    if project_context in context_categories:
        for cat_name, extensions in context_categories[project_context].items():
            if cat_name in categories:
                categories[cat_name].update(extensions)
            else:
                categories[cat_name] = extensions
    
    return categories

def get_target_directory(file_path, categories, project_context):
    """Determine the target directory based on file type and project context"""
    file_ext = file_path.suffix.lower()
    file_name = file_path.name.lower()
    
    # Special handling based on project context and file name patterns
    if project_context == 'ai_ml':
        if any(keyword in file_name for keyword in ['model', 'train', 'predict']):
            return 'ai_models'
        elif any(keyword in file_name for keyword in ['data', 'dataset', 'feature']):
            return 'ai_datasets'
    
    elif project_context == 'music_audio':
        if any(keyword in file_name for keyword in ['suno', 'track', 'song']):
            return 'music_tracks'
        elif any(keyword in file_name for keyword in ['lyrics', 'metadata']):
            return 'music_metadata'
    
    elif project_context == 'automation':
        if any(keyword in file_name for keyword in ['workflow', 'n8n', 'script']):
            return 'workflow_scripts'
    
    # General category matching
    for cat_name, extensions in categories.items():
        if file_ext in extensions:
            return cat_name
    
    # Default category
    return 'other'

def organize_files_with_context_awareness(directory):
    """Organize files with advanced parent-folder content awareness"""
    directory = Path(directory)
    
    # Analyze project context
    project_context, context_scores = analyze_parent_folder_context(directory)
    print(f"Project Context: {project_context}")
    print(f"Context Scores: {context_scores}")
    print("="*60)
    
    # Get categories based on context
    categories = get_advanced_file_categories(project_context)
    
    # Counters
    organized_count = 0
    skipped_count = 0
    
    print(f"Organizing files in: {directory}")
    print(f"Using context-aware categories for: {project_context}")
    print("-"*60)
    
    # Get all files in the current directory (not subdirectories)
    files = [f for f in directory.iterdir() if f.is_file()]
    
    for file_path in files:
        # Skip this script and important project files
        if file_path.name in [os.path.basename(__file__), 'QWEN.md', '.gitignore']:
            continue
            
        # Determine target directory based on context
        target_dir_name = get_target_directory(file_path, categories, project_context)
        target_dir = directory / target_dir_name
        target_dir.mkdir(exist_ok=True)
        
        # Move the file to its target directory
        target_path = target_dir / file_path.name
        
        # Handle potential name conflicts
        counter = 1
        original_target = target_path
        while target_path.exists():
            stem = original_target.stem
            suffix = original_target.suffix
            target_path = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1
        
        try:
            shutil.move(str(file_path), str(target_path))
            print(f"Moved: {file_path.name} -> {target_dir_name}/")
            organized_count += 1
        except Exception as e:
            print(f"Skipped: {file_path.name} (reason: {e})")
            skipped_count += 1
    
    print("="*60)
    print(f"Context-aware organization complete!")
    print(f"Project context: {project_context}")
    print(f"Files organized: {organized_count}")
    print(f"Files skipped: {skipped_count}")
    
    # Show context analysis summary
    print(f"\nContext Analysis Summary:")
    for context_type, score in sorted(context_scores.items(), key=lambda x: x[1], reverse=True):
        if score > 0:
            print(f"  {context_type}: {score}")

def main():
    directory = Path.cwd()  # Current directory
    organize_files_with_context_awareness(directory)

if __name__ == "__main__":
    print("Advanced Parent-Folder Content Awareness File Organizer")
    print("Analyzes project context and organizes files accordingly")
    print("="*60)
    print("Running organization with parent-folder content awareness...")
    main()
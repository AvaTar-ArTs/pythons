#!/usr/bin/env python3
"""
Reorganization Helper Script
This script helps implement the reorganization strategy for the ~/pythons directory.

Features:
- Analyzes current directory structure
- Identifies files for consolidation
- Creates new directory structure
- Moves files according to the new organization
- Generates migration reports
"""

import os
import sys
import shutil
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Set
from datetime import datetime
import re


def setup_logging():
    """Set up logging for the reorganization process."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"reorganization_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def analyze_current_structure(base_path: Path) -> Dict:
    """Analyze the current directory structure."""
    logger = setup_logging()
    logger.info(f"Analyzing directory structure: {base_path}")
    
    analysis = {
        'total_files': 0,
        'total_dirs': 0,
        'file_extensions': {},
        'directory_sizes': {},
        'potential_duplicates': [],
        'categories': {}
    }
    
    for root, dirs, files in os.walk(base_path):
        # Count directories
        analysis['total_dirs'] += len(dirs)
        
        # Process files
        for file in files:
            file_path = Path(root) / file
            if file_path.is_file():
                analysis['total_files'] += 1
                
                # Track file extensions
                ext = file_path.suffix.lower()
                analysis['file_extensions'][ext] = analysis['file_extensions'].get(ext, 0) + 1
                
                # Track directory sizes
                dir_path = file_path.parent
                dir_size = analysis['directory_sizes'].get(str(dir_path), 0)
                try:
                    dir_size += file_path.stat().st_size
                    analysis['directory_sizes'][str(dir_path)] = dir_size
                except:
                    pass  # Skip if file is inaccessible
    
    # Categorize directories by content
    for root, dirs, files in os.walk(base_path):
        dir_path = Path(root)
        dir_name = dir_path.name.lower()
        
        # Determine category based on directory name and content
        category = categorize_directory(dir_name, files)
        if category:
            if category not in analysis['categories']:
                analysis['categories'][category] = []
            analysis['categories'][category].append(str(dir_path))
    
    logger.info(f"Analysis complete: {analysis['total_files']} files, {analysis['total_dirs']} directories")
    return analysis


def categorize_directory(dir_name: str, files: List[str]) -> str:
    """Categorize a directory based on its name and content."""
    # AI/ML related directories
    ai_keywords = ['ai', 'llm', 'openai', 'anthropic', 'grok', 'claude', 'chatgpt', 'langchain']
    if any(keyword in dir_name for keyword in ai_keywords):
        return 'ai'
    
    # Social media related directories
    social_keywords = ['instagram', 'social', 'automation', 'bot', 'twitter', 'facebook', 'tiktok']
    if any(keyword in dir_name for keyword in social_keywords):
        return 'social'
    
    # Media processing directories
    media_keywords = ['media', 'audio', 'video', 'image', 'processing', 'resize', 'convert']
    if any(keyword in dir_name for keyword in media_keywords):
        return 'media'
    
    # Data processing directories
    data_keywords = ['data', 'csv', 'json', 'analysis', 'process', 'transform']
    if any(keyword in dir_name for keyword in data_keywords):
        return 'data'
    
    # File operations directories
    file_keywords = ['file', 'organize', 'rename', 'move', 'copy', 'duplicate']
    if any(keyword in dir_name for keyword in file_keywords):
        return 'file_operations'
    
    # Testing directories
    test_keywords = ['test', 'testing', 'mock', 'unit']
    if any(keyword in dir_name for keyword in test_keywords):
        return 'testing'
    
    # Documentation directories
    doc_keywords = ['doc', 'documentation', 'readme', 'guide']
    if any(keyword in dir_name for keyword in doc_keywords):
        return 'documentation'
    
    # Default to utilities if no specific category found
    return 'utilities'


def create_new_structure(base_path: Path) -> Dict[str, Path]:
    """Create the new directory structure."""
    logger = setup_logging()
    logger.info("Creating new directory structure...")
    
    new_dirs = {
        'core': base_path / 'core',
        'ai': base_path / 'ai',
        'automation': base_path / 'automation',
        'media': base_path / 'media',
        'social': base_path / 'social',
        'data': base_path / 'data',
        'projects': base_path / 'projects',
        'legacy': base_path / 'legacy'
    }
    
    # Subdirectories
    subdirs = {
        'core_config': base_path / 'core' / 'config',
        'core_logging': base_path / 'core' / 'logging',
        'core_security': base_path / 'core' / 'security',
        'core_utils': base_path / 'core' / 'utils',
        'ai_clients': base_path / 'ai' / 'clients',
        'ai_agents': base_path / 'ai' / 'agents',
        'ai_interfaces': base_path / 'ai' / 'interfaces',
        'automation_scheduling': base_path / 'automation' / 'scheduling',
        'automation_monitoring': base_path / 'automation' / 'monitoring',
        'automation_orchestration': base_path / 'automation' / 'orchestration',
        'media_audio': base_path / 'media' / 'audio',
        'media_video': base_path / 'media' / 'video',
        'media_image': base_path / 'media' / 'image',
        'social_adapters': base_path / 'social' / 'adapters',
        'social_strategies': base_path / 'social' / 'strategies',
        'social_analytics': base_path / 'social' / 'analytics',
        'data_analysis': base_path / 'data' / 'analysis',
        'data_transformation': base_path / 'data' / 'transformation',
        'data_validation': base_path / 'data' / 'validation',
        'projects_content_auto': base_path / 'projects' / 'content_automation',
        'projects_revenue_dash': base_path / 'projects' / 'revenue_dashboard',
        'projects_ai_recipe': base_path / 'projects' / 'ai_recipe_gen'
    }
    
    # Combine all directories
    all_dirs = {**new_dirs, **subdirs}
    
    # Create directories
    for name, path in all_dirs.items():
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {path}")
    
    logger.info("New directory structure created successfully")
    return all_dirs


def identify_files_for_moving(base_path: Path) -> Dict[str, List[Path]]:
    """Identify files that should be moved to new locations."""
    logger = setup_logging()
    logger.info("Identifying files for movement...")
    
    files_to_move = {
        'ai_scripts': [],
        'social_scripts': [],
        'media_scripts': [],
        'data_scripts': [],
        'file_scripts': [],
        'utility_scripts': [],
        'project_scripts': []
    }
    
    # Define patterns for different categories
    ai_patterns = [r'.*ai.*\.py$', r'.*llm.*\.py$', r'.*chat.*\.py$', r'.*claude.*\.py$', r'.*groq.*\.py$']
    social_patterns = [r'.*instagram.*\.py$', r'.*social.*\.py$', r'.*bot.*\.py$']
    media_patterns = [r'.*audio.*\.py$', r'.*video.*\.py$', r'.*image.*\.py$', r'.*resize.*\.py$']
    data_patterns = [r'.*data.*\.py$', r'.*process.*\.py$', r'.*csv.*\.py$', r'.*json.*\.py$']
    file_patterns = [r'.*organize.*\.py$', r'.*rename.*\.py$', r'.*duplicate.*\.py$']
    
    for root, dirs, files in os.walk(base_path):
        # Skip newly created directories
        if any(new_dir in str(root) for new_dir in ['core', 'ai', 'automation', 'media', 'social', 'data', 'projects', 'legacy']):
            continue
            
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                
                # Skip if it's in the new structure directories
                if any(str(file_path).startswith(str(base_path / new_dir)) for new_dir in ['core', 'ai', 'automation', 'media', 'social', 'data', 'projects', 'legacy']):
                    continue
                
                # Match patterns
                if any(re.search(pattern, file, re.IGNORECASE) for pattern in ai_patterns):
                    files_to_move['ai_scripts'].append(file_path)
                elif any(re.search(pattern, file, re.IGNORECASE) for pattern in social_patterns):
                    files_to_move['social_scripts'].append(file_path)
                elif any(re.search(pattern, file, re.IGNORECASE) for pattern in media_patterns):
                    files_to_move['media_scripts'].append(file_path)
                elif any(re.search(pattern, file, re.IGNORECASE) for pattern in data_patterns):
                    files_to_move['data_scripts'].append(file_path)
                elif any(re.search(pattern, file, re.IGNORECASE) for pattern in file_patterns):
                    files_to_move['file_scripts'].append(file_path)
                elif 'project' in str(file_path).lower() or 'recipe' in str(file_path).lower():
                    files_to_move['project_scripts'].append(file_path)
                else:
                    files_to_move['utility_scripts'].append(file_path)
    
    # Log summary
    for category, files in files_to_move.items():
        logger.info(f"{category}: {len(files)} files identified")
    
    return files_to_move


def move_files(files_to_move: Dict[str, List[Path]], new_structure: Dict[str, Path], base_path: Path):
    """Move files to their new locations."""
    logger = setup_logging()
    logger.info("Moving files to new locations...")
    
    moved_count = 0
    failed_moves = []
    
    for category, files in files_to_move.items():
        if not files:
            continue
            
        # Determine destination based on category
        if 'ai' in category:
            dest_dir = new_structure.get('ai_clients', new_structure.get('ai'))
        elif 'social' in category:
            dest_dir = new_structure.get('social_adapters', new_structure.get('social'))
        elif 'media' in category:
            if 'audio' in category:
                dest_dir = new_structure.get('media_audio', new_structure.get('media'))
            elif 'video' in category:
                dest_dir = new_structure.get('media_video', new_structure.get('media'))
            elif 'image' in category:
                dest_dir = new_structure.get('media_image', new_structure.get('media'))
            else:
                dest_dir = new_structure.get('media')
        elif 'data' in category:
            dest_dir = new_structure.get('data_analysis', new_structure.get('data'))
        elif 'project' in category:
            dest_dir = new_structure.get('projects_content_auto', new_structure.get('projects'))
        else:
            dest_dir = new_structure.get('core_utils', new_structure.get('core'))
        
        if not dest_dir:
            logger.warning(f"No destination directory found for category: {category}")
            continue
        
        for file_path in files:
            try:
                # Skip if file is already in the destination or new structure
                if str(file_path).startswith(str(base_path)):
                    relative_path = file_path.relative_to(base_path)
                    new_file_path = dest_dir / relative_path.name
                    
                    # Handle name conflicts
                    counter = 1
                    original_new_path = new_file_path
                    while new_file_path.exists():
                        stem = original_new_path.stem
                        suffix = original_new_path.suffix
                        new_file_path = original_new_path.parent / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    # Move the file
                    shutil.move(str(file_path), str(new_file_path))
                    logger.info(f"Moved: {file_path.name} -> {new_file_path}")
                    moved_count += 1
            except Exception as e:
                logger.error(f"Failed to move {file_path}: {e}")
                failed_moves.append((file_path, str(e)))
    
    logger.info(f"File movement completed: {moved_count} moved, {len(failed_moves)} failed")
    return moved_count, failed_moves


def generate_migration_report(analysis: Dict, moved_count: int, failed_moves: List[Tuple], base_path: Path):
    """Generate a comprehensive migration report."""
    logger = setup_logging()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = base_path / f"migration_report_{timestamp}.json"
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'base_path': str(base_path),
        'analysis': analysis,
        'moved_files_count': moved_count,
        'failed_moves_count': len(failed_moves),
        'failed_moves': [(str(path), error) for path, error in failed_moves],
        'recommendations': [
            "Review failed moves and handle manually",
            "Update import paths in moved files",
            "Test functionality of moved components",
            "Remove empty old directories after verification"
        ]
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)
    
    logger.info(f"Migration report saved to: {report_path}")
    return report_path


def main():
    """Main function to execute the reorganization."""
    if len(sys.argv) != 2:
        print("Usage: python reorganize_helper.py <path_to_puthons_directory>")
        sys.exit(1)
    
    base_path = Path(sys.argv[1])
    
    if not base_path.exists():
        print(f"Error: Path {base_path} does not exist")
        sys.exit(1)
    
    logger = setup_logging()
    logger.info(f"Starting reorganization of: {base_path}")
    
    try:
        # Step 1: Analyze current structure
        analysis = analyze_current_structure(base_path)
        
        # Step 2: Create new directory structure
        new_structure = create_new_structure(base_path)
        
        # Step 3: Identify files for movement
        files_to_move = identify_files_for_moving(base_path)
        
        # Step 4: Move files
        moved_count, failed_moves = move_files(files_to_move, new_structure, base_path)
        
        # Step 5: Generate report
        report_path = generate_migration_report(analysis, moved_count, failed_moves, base_path)
        
        logger.info("Reorganization completed successfully!")
        logger.info(f"Files moved: {moved_count}")
        logger.info(f"Files failed to move: {len(failed_moves)}")
        logger.info(f"Report saved to: {report_path}")
        
        if failed_moves:
            logger.warning("Some files failed to move. Check the report for details.")
        
    except Exception as e:
        logger.error(f"Reorganization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
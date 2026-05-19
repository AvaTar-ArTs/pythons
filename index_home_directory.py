#!/usr/bin/env python3
# home-search-index/index_home_directory.py

"""
Home Directory Indexing System
This script creates a comprehensive search index for the entire /Users/steven/ directory
with content-aware analysis, business value assessment, and macOS tag integration.
"""

import os
import sys
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, KEYWORD, NUMERIC, DATETIME
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import writing
import json
import csv
from datetime import datetime
from pathlib import Path
import mimetypes
import logging
from logging.handlers import RotatingFileHandler
import hashlib
from tqdm import tqdm
import xattr  # For reading macOS extended attributes (tags)
import plistlib  # For parsing macOS tag plists
from typing import List

# Configure logging
logger = logging.getLogger('home_directory_indexer')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('index_home_directory.log', maxBytes=10*1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)

# Define schema for the index with macOS tags
schema = Schema(
    title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    content=TEXT(analyzer=StemmingAnalyzer()),
    path=KEYWORD(stored=True),
    filename=TEXT(stored=True),
    category=KEYWORD(stored=True),
    file_type=KEYWORD(stored=True),
    size_bytes=NUMERIC(stored=True),
    modified_date=DATETIME(stored=True),
    created_date=DATETIME(stored=True),
    business_value=NUMERIC(stored=True),
    complexity=KEYWORD(stored=True),
    semantic_tags=KEYWORD(stored=True),
    macos_tags=KEYWORD(stored=True)  # Added macOS tags field
)

def get_file_category(file_path):
    """Determine file category based on path and content"""
    path_lower = file_path.lower()
    
    if 'ai' in path_lower or 'automation' in path_lower or 'llm' in path_lower:
        return 'AI_Automation'
    elif 'web' in path_lower or 'html' in path_lower or 'css' in path_lower:
        return 'Web_Development'
    elif 'strategy' in path_lower or 'plan' in path_lower:
        return 'Strategic_Planning'
    elif 'knowledge' in path_lower or 'research' in path_lower:
        return 'Knowledge_Research'
    elif 'literature' in path_lower or 'thinketh' in path_lower:
        return 'Literature'
    elif 'data' in path_lower or 'csv' in path_lower or 'json' in path_lower:
        return 'Data_Analysis'
    elif 'audio' in path_lower or 'music' in path_lower or 'mp3' in path_lower:
        return 'Audio_Media'
    elif 'video' in path_lower or 'mp4' in path_lower:
        return 'Video_Media'
    elif 'image' in path_lower or 'jpg' in path_lower or 'png' in path_lower:
        return 'Image_Media'
    elif 'avatararts' in path_lower:
        return 'AvatarArts_Project'
    elif 'autotagger' in path_lower:
        return 'AutoTagger_System'
    elif 'harbor' in path_lower:
        return 'Harbor_Projects'
    elif 'claude' in path_lower:
        return 'Claude_Conversations'
    elif 'grok' in path_lower:
        return 'Grok_Conversations'
    elif 'qwen' in path_lower:
        return 'Qwen_Conversations'
    elif 'scripts' in path_lower:
        return 'Scripts'
    elif 'documents' in path_lower:
        return 'Documents'
    elif 'downloads' in path_lower:
        return 'Downloads'
    elif 'desktop' in path_lower:
        return 'Desktop'
    elif 'library' in path_lower:
        return 'Library'
    elif 'movies' in path_lower:
        return 'Movies'
    elif 'music' in path_lower:
        return 'Music'
    elif 'pictures' in path_lower:
        return 'Pictures'
    else:
        return 'General'

def get_business_value(file_path, content=""):
    """Calculate business value based on keywords and file importance"""
    path_lower = file_path.lower()
    content_lower = content.lower()
    
    # Keywords that indicate high business value
    high_value_keywords = [
        'business', 'revenue', 'profit', 'strategy', 'plan', 'implementation',
        'automation', 'ai', 'marketing', 'seo', 'client', 'customer',
        'financial', 'investment', 'growth', 'scaling', 'enterprise',
        'monetization', 'opportunity', 'analysis', 'report', 'dashboard'
    ]
    
    value = 0.5  # Base value
    
    # Check path for high-value keywords
    for keyword in high_value_keywords:
        if keyword in path_lower:
            value += 0.5
    
    # Check content for high-value keywords
    for keyword in high_value_keywords:
        if keyword in content_lower:
            value += 0.2
    
    # Cap at 10.0
    return min(value, 10.0)

def get_macos_tags(file_path: str) -> List[str]:
    """Extract macOS tags from a file using extended attributes"""
    try:
        # Get the extended attributes
        attrs = xattr.listxattr(file_path)
        if 'com.apple.metadata:_kMDItemUserTags' in attrs:
            # Read the tag data
            tag_data = xattr.getxattr(file_path, 'com.apple.metadata:_kMDItemUserTags')
            # This is a binary plist, need to parse it
            tags = plistlib.loads(tag_data)
            return tags if isinstance(tags, list) else []
        else:
            return []
    except Exception as e:
        logger.warning(f"Could not read tags for {file_path}: {e}")
        return []

def read_file_content(file_path, max_size=1000000):
    """Read file content with error handling and size limits"""
    try:
        # Skip large files to avoid memory issues
        if os.path.getsize(file_path) > max_size:
            logger.warning(f"Skipping large file: {file_path}")
            return ""
        
        # Only read text-based files
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and not mime_type.startswith('text/'):
            # For specific text-based extensions
            ext = Path(file_path).suffix.lower()
            if ext not in ['.py', '.js', '.ts', '.html', '.css', '.md', '.txt', '.json', '.csv', '.xml', '.yaml', '.yml']:
                logger.debug(f"Skipping non-text file: {file_path}")
                return ""
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Truncate if too long
        if len(content) > 50000:
            content = content[:50000]
        
        return content
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return ""

def index_home_directory(home_dir="/Users/steven", index_writer=None):
    """Index the entire home directory with macOS tag integration"""
    indexed_count = 0
    skipped_count = 0
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(home_dir):
        # Skip certain directories to avoid indexing system files
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['Library', 'System', 'Network']]
        
        for file in tqdm(files, desc=f"Indexing {root}"):
            if file.startswith('.'):  # Skip hidden files
                continue
            
            file_path = os.path.join(root, file)
            
            try:
                # Get file stats
                stat = os.stat(file_path)
                size_bytes = stat.st_size
                modified_time = datetime.fromtimestamp(stat.st_mtime)
                created_time = datetime.fromtimestamp(stat.st_ctime)
                
                # Read content
                content = read_file_content(file_path)
                
                # Determine category
                category = get_file_category(file_path)
                
                # Determine file type
                file_ext = Path(file_path).suffix.lower().strip('.') or 'no_ext'

                # Calculate business value
                business_value = get_business_value(file_path, content)

                # Create semantic tags based on path and content
                semantic_tags = [category.lower().replace('_', '-')]
                if business_value > 2.0:
                    semantic_tags.append('high-value')
                if 'ai' in content.lower():
                    semantic_tags.append('ai')
                if 'automation' in content.lower():
                    semantic_tags.append('automation')
                if 'strategy' in content.lower():
                    semantic_tags.append('strategy')

                # Get macOS tags
                macos_tags = get_macos_tags(file_path)

                # Determine complexity for code files
                complexity = 'unknown'
                if file_ext == 'py':
                    complexity = 'high' if len(content) > 5000 else 'medium' if len(content) > 1000 else 'low'
                elif file_ext in ['js', 'ts', 'html', 'css']:
                    complexity = 'high' if len(content) > 3000 else 'medium' if len(content) > 500 else 'low'

                # Add document to index
                index_writer.add_document(
                    title=file,
                    content=content,
                    path=file_path,
                    filename=file,
                    category=category,
                    file_type=file_ext,
                    size_bytes=size_bytes,
                    modified_date=modified_time,
                    created_date=created_time,
                    business_value=business_value,
                    complexity=complexity,
                    semantic_tags=','.join(semantic_tags),
                    macos_tags=','.join(macos_tags)  # Add macOS tags to index
                )
                
                indexed_count += 1
                if indexed_count % 100 == 0:
                    logger.info(f"Indexed {indexed_count} documents so far...")
                
            except Exception as e:
                logger.error(f"Error indexing {file_path}: {e}")
                skipped_count += 1
    
    return indexed_count, skipped_count

def main():
    logger.info("Starting home directory indexing process with macOS tag integration...")
    
    # Create index directory if it doesn't exist
    index_dir = Path('/Users/steven/home-search-index/index')
    index_dir.mkdir(exist_ok=True)
    
    # Check if index already exists
    if index_dir.exists() and any(index_dir.iterdir()):
        logger.info("Opening existing index...")
        ix = open_dir(str(index_dir))
        index_writer = ix.writer()
    else:
        logger.info("Creating new index with macOS tag support...")
        ix = create_in(str(index_dir), schema)
        index_writer = ix.writer()
    
    # Index the home directory
    home_dir = "/Users/steven"
    indexed_count, skipped_count = index_home_directory(home_dir, index_writer)
    
    # Commit the changes
    logger.info("Committing index changes...")
    index_writer.commit()
    
    logger.info(f"Indexing complete! Indexed: {indexed_count}, Skipped: {skipped_count}")
    
    # Save index statistics
    stats = {
        "indexed_count": indexed_count,
        "skipped_count": skipped_count,
        "index_path": str(index_dir),
        "timestamp": datetime.now().isoformat(),
        "features": ["semantic_analysis", "macos_tags", "business_value", "complexity"]
    }
    
    with open("index_statistics.json", "w") as f:
        json.dump(stats, f, indent=2, default=str)
    
    print(f"Indexing complete! Indexed: {indexed_count}, Skipped: {skipped_count}")
    print(f"Index location: {index_dir}")
    print(f"Statistics saved to: index_statistics.json")
    print("The index now includes both semantic tags and macOS tags for enhanced searchability!")

if __name__ == "__main__":
    # Install xattr if not available
    try:
        import xattr
    except ImportError:
        print("Installing xattr library for macOS tag support...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "xattr"])
        import xattr
    
    main()
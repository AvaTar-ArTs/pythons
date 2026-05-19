"""
Incremental Indexing System for AVATARARTS Ecosystem
Processes files progressively and integrates with AutoTag analysis
"""

import os
import sqlite3
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
import json
import time
from avatararts_db_schema import connect_to_avatararts_db, add_file_entry, update_autotag_analysis


class IncrementalIndexer:
    def __init__(self, db_path="avatararts.db", root_path="/Users/steven"):
        self.db_path = db_path
        self.root_path = root_path
        self.conn = connect_to_avatararts_db(db_path)
        
        # Create a table to track processed files and their hashes
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_tracking (
                path TEXT PRIMARY KEY,
                hash TEXT NOT NULL,
                indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                file_size INTEGER,
                last_modified REAL
            )
        ''')
        self.conn.commit()
    
    def calculate_file_hash(self, file_path):
        """Calculate SHA-256 hash of a file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def is_file_processed(self, file_path):
        """Check if a file has already been processed and hasn't changed"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT hash, file_size, last_modified FROM file_tracking WHERE path = ?", (file_path,))
        result = cursor.fetchone()
        
        if not result:
            return False  # File not in tracking table
        
        stored_hash, stored_size, stored_mod_time = result
        
        # Check if file still exists and get current stats
        try:
            stat_info = os.stat(file_path)
            current_size = stat_info.st_size
            current_mod_time = stat_info.st_mtime
            
            # If sizes differ, file has definitely changed
            if current_size != stored_size:
                return False
            
            # If modification times differ significantly, file has changed
            if abs(current_mod_time - stored_mod_time) > 1:  # 1 second tolerance
                return False
                
            # If sizes and mod times match, double-check with hash
            current_hash = self.calculate_file_hash(file_path)
            if current_hash != stored_hash:
                return False
                
            return True  # File is unchanged and already processed
        except OSError:
            # File no longer exists
            return False
    
    def mark_file_as_processed(self, file_path):
        """Mark a file as processed in the tracking table"""
        cursor = self.conn.cursor()
        stat_info = os.stat(file_path)
        
        cursor.execute('''
            INSERT OR REPLACE INTO file_tracking 
            (path, hash, file_size, last_modified) 
            VALUES (?, ?, ?, ?)
        ''', (
            file_path,
            self.calculate_file_hash(file_path),
            stat_info.st_size,
            stat_info.st_mtime
        ))
        self.conn.commit()
    
    def determine_business_vertical(self, file_path):
        """Determine which business vertical a file belongs to based on path"""
        path_lower = file_path.lower()
        
        # Map file paths to business verticals based on directory structure
        if 'ai-automation' in path_lower or 'automation' in path_lower:
            return 'AI Automation Tools'
        elif 'business-ops' in path_lower or 'operations' in path_lower:
            return 'Business Operations'
        elif 'content' in path_lower or 'creation' in path_lower:
            return 'Content Creation Pipeline'
        elif 'seo' in path_lower or 'marketing' in path_lower:
            return 'SEO Optimization Suite'
        elif 'notebooklm' in path_lower or 'google-ai' in path_lower:
            return 'NotebookLM Integration'
        elif 'dr-adu' in path_lower or 'adu' in path_lower:
            return 'Dr. Adu Project'
        elif 'heavenly-hands' in path_lower or 'hands' in path_lower:
            return 'Heavenly Hands'
        else:
            # Default to most common category or try to infer from content
            return None
    
    def process_single_file(self, file_path):
        """Process a single file and add it to the database"""
        try:
            # Add file to the main files table
            business_vertical = self.determine_business_vertical(file_path)
            file_id = add_file_entry(self.conn, file_path, business_vertical)
            
            # Create a basic AutoTag analysis entry (this would later be enhanced by the actual AutoTag system)
            analysis_data = {
                'rapid_scan_result': {
                    'file_type': os.path.splitext(file_path)[1],
                    'size_category': self.categorize_file_size(os.path.getsize(file_path))
                },
                'intelligent_org_result': {},
                'advanced_intel_result': {},
                'business_value_score': 0.0,  # Will be updated by AutoTag analysis
                'business_value_reason': 'Initial indexing',
                'semantic_tags': self.extract_basic_tags(file_path),
                'content_summary': f'File in {os.path.dirname(file_path)}'
            }
            
            update_autotag_analysis(self.conn, file_id, analysis_data)
            
            # Mark as processed
            self.mark_file_as_processed(file_path)
            
            return True
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return False
    
    def categorize_file_size(self, size_bytes):
        """Categorize file size for rapid scanning"""
        if size_bytes < 1024:  # < 1KB
            return 'tiny'
        elif size_bytes < 1024 * 100:  # < 100KB
            return 'small'
        elif size_bytes < 1024 * 1024:  # < 1MB
            return 'medium'
        elif size_bytes < 1024 * 1024 * 10:  # < 10MB
            return 'large'
        else:
            return 'huge'
    
    def extract_basic_tags(self, file_path):
        """Extract basic tags from file path and name"""
        path_parts = Path(file_path).parts
        filename = Path(file_path).stem.lower()
        
        tags = []
        
        # Add extension as tag
        ext = os.path.splitext(file_path)[1][1:]  # Remove the dot
        if ext:
            tags.append(ext)
        
        # Add directory names as tags
        for part in path_parts[-4:]:  # Last 4 directory levels
            clean_part = part.lower().replace('_', ' ').replace('-', ' ')
            if len(clean_part) > 2:  # Skip short parts like '.'
                tags.append(clean_part)
        
        # Add filename words as tags
        for word in filename.replace('_', ' ').replace('-', ' ').split():
            if len(word) > 2:  # Skip short words
                tags.append(word)
        
        return list(set(tags))  # Remove duplicates
    
    def scan_directory_incrementally(self, directory_path, max_files=None, callback=None):
        """Scan a directory incrementally, processing only new or changed files"""
        processed_count = 0
        skipped_count = 0
        
        print(f"Starting incremental scan of: {directory_path}")
        
        for root, dirs, files in os.walk(directory_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip hidden files
                if file.startswith('.'):
                    continue
                
                # Determine MIME type to focus on relevant files
                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type is None:
                    # If we can't determine MIME type, check file extension
                    ext = os.path.splitext(file_path)[1].lower()
                    if ext in ['.tmp', '.log', '.cache', '.swp', '.pyc']:
                        continue  # Skip temporary/cache files
                
                # Check if file needs processing
                if self.is_file_processed(file_path):
                    skipped_count += 1
                    continue
                
                # Process the file
                success = self.process_single_file(file_path)
                if success:
                    processed_count += 1
                    if callback:
                        callback(file_path, processed_count)
                
                # Check if we've reached the max files limit
                if max_files and processed_count >= max_files:
                    print(f"Reached maximum file limit of {max_files}")
                    break
            
            if max_files and processed_count >= max_files:
                break
        
        print(f"Scan completed. Processed: {processed_count}, Skipped: {skipped_count}")
        return processed_count, skipped_count
    
    def get_unprocessed_files(self, directory_path):
        """Get a list of files that haven't been processed yet"""
        unprocessed = []
        
        for root, dirs, files in os.walk(directory_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip hidden files
                if file.startswith('.'):
                    continue
                
                # Check if file needs processing
                if not self.is_file_processed(file_path):
                    unprocessed.append(file_path)
        
        return unprocessed
    
    def close(self):
        """Close the database connection"""
        self.conn.close()


def indexing_callback(file_path, processed_count):
    """Callback function to report progress during indexing"""
    if processed_count % 100 == 0:  # Report every 100 files
        print(f"Processed {processed_count} files... Current: {os.path.basename(file_path)}")


def main():
    """Main function to demonstrate the incremental indexer"""
    print("Initializing AVATARARTS Incremental Indexer...")
    
    # Initialize the indexer
    indexer = IncrementalIndexer()
    
    # Example: Index a specific directory (you can change this to any directory)
    directory_to_index = "/Users/steven"  # Root directory
    
    print(f"Scanning directory: {directory_to_index}")
    
    # Get count of unprocessed files first
    unprocessed_files = indexer.get_unprocessed_files(directory_to_index)
    print(f"Found {len(unprocessed_files)} unprocessed files")
    
    # For demonstration purposes, let's process a limited number of files
    # In a real scenario, you might want to process all files or process in batches
    processed, skipped = indexer.scan_directory_incrementally(
        directory_to_index, 
        max_files=100,  # Limit for demonstration
        callback=indexing_callback
    )
    
    print(f"\nIndexing Summary:")
    print(f"- Files processed: {processed}")
    print(f"- Files skipped (already processed): {skipped}")
    
    # Close the indexer
    indexer.close()
    
    print("\nIncremental indexing completed!")


if __name__ == "__main__":
    main()
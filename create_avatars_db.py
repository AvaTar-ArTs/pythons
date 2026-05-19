#!/usr/bin/env python3
"""
AVATARARTS File Metadata Database Generator
Creates a SQLite database with metadata for files in the AVATARARTS directory
"""

import sqlite3
import os
import hashlib
from datetime import datetime
import mimetypes
from pathlib import Path

def create_database(db_path):
    """Create the SQLite database with appropriate tables"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create files table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            name TEXT NOT NULL,
            extension TEXT,
            size_bytes INTEGER,
            created_time TEXT,
            modified_time TEXT,
            accessed_time TEXT,
            mime_type TEXT,
            md5_hash TEXT,
            directory TEXT,
            depth INTEGER,
            is_file BOOLEAN,
            is_directory BOOLEAN
        )
    ''')
    
    # Create directories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS directories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            file_count INTEGER DEFAULT 0,
            total_size INTEGER DEFAULT 0,
            created_time TEXT,
            modified_time TEXT
        )
    ''')
    
    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_path ON files(path)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_extension ON files(extension)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_directory ON files(directory)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_mime_type ON files(mime_type)')
    
    conn.commit()
    return conn

def get_file_metadata(file_path):
    """Get metadata for a file"""
    stat = os.stat(file_path)
    
    # Calculate MD5 hash (for smaller files only to save time)
    md5_hash = None
    if stat.st_size < 10 * 1024 * 1024:  # Only for files smaller than 10MB
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
                md5_hash = hashlib.md5(file_content).hexdigest()
        except:
            md5_hash = None
    
    # Get MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    
    # Calculate directory depth
    depth = len(Path(file_path).parts) - len(Path('/Users/steven/AVATARARTS').parts)
    
    return {
        'path': file_path,
        'name': os.path.basename(file_path),
        'extension': os.path.splitext(file_path)[1],
        'size_bytes': stat.st_size,
        'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'accessed_time': datetime.fromtimestamp(stat.st_atime).isoformat(),
        'mime_type': mime_type,
        'md5_hash': md5_hash,
        'directory': os.path.dirname(file_path),
        'depth': depth,
        'is_file': os.path.isfile(file_path),
        'is_directory': os.path.isdir(file_path)
    }

def populate_database(conn, avatars_path):
    """Populate the database with file metadata"""
    cursor = conn.cursor()
    
    # Walk through the directory structure
    count = 0
    for root, dirs, files in os.walk(avatars_path):
        # Process directories
        for d in dirs:
            dir_path = os.path.join(root, d)
            try:
                stat = os.stat(dir_path)
                
                # Count files and total size in this directory
                dir_file_count = 0
                dir_total_size = 0
                
                for dir_root, _, dir_files in os.walk(dir_path):
                    for f in dir_files:
                        try:
                            file_stat = os.stat(os.path.join(dir_root, f))
                            dir_file_count += 1
                            dir_total_size += file_stat.st_size
                        except:
                            continue
                
                cursor.execute('''
                    INSERT OR REPLACE INTO directories 
                    (path, name, file_count, total_size, created_time, modified_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    dir_path,
                    d,
                    dir_file_count,
                    dir_total_size,
                    datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    datetime.fromtimestamp(stat.st_mtime).isoformat()
                ))
            except:
                continue
        
        # Process files (limit to first 10000 files to avoid timeout)
        for f in files:
            if count >= 10000:  # Limit to prevent timeout
                break
                
            file_path = os.path.join(root, f)
            try:
                metadata = get_file_metadata(file_path)
                
                cursor.execute('''
                    INSERT INTO files 
                    (path, name, extension, size_bytes, created_time, modified_time, 
                     accessed_time, mime_type, md5_hash, directory, depth, is_file, is_directory)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    metadata['path'],
                    metadata['name'],
                    metadata['extension'],
                    metadata['size_bytes'],
                    metadata['created_time'],
                    metadata['modified_time'],
                    metadata['accessed_time'],
                    metadata['mime_type'],
                    metadata['md5_hash'],
                    metadata['directory'],
                    metadata['depth'],
                    metadata['is_file'],
                    metadata['is_directory']
                ))
                
                count += 1
                if count % 1000 == 0:
                    print(f"Processed {count} files...")
                    conn.commit()
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
    
    conn.commit()
    print(f"Database populated with {count} files")

def create_summary_tables(conn):
    """Create summary tables for analysis"""
    cursor = conn.cursor()
    
    # File type summary
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS file_types_summary AS
        SELECT 
            extension,
            COUNT(*) as file_count,
            SUM(size_bytes) as total_size,
            AVG(size_bytes) as avg_size
        FROM files
        WHERE extension IS NOT NULL AND extension != ''
        GROUP BY extension
        ORDER BY file_count DESC
    ''')
    
    # Directory summary
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS directory_summary AS
        SELECT 
            CASE 
                WHEN depth = 1 THEN 'Root Level'
                WHEN depth = 2 THEN 'Level 1 Subdirectories'
                WHEN depth = 3 THEN 'Level 2 Subdirectories'
                ELSE 'Deeper Levels (' || depth || ')'
            END as level_category,
            COUNT(*) as directory_count,
            SUM(file_count) as total_files,
            SUM(total_size) as total_size
        FROM directories
        GROUP BY level_category
        ORDER BY depth
    ''')
    
    # Largest files
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS largest_files AS
        SELECT 
            path,
            name,
            size_bytes,
            extension,
            mime_type
        FROM files
        ORDER BY size_bytes DESC
        LIMIT 50
    ''')
    
    # Most common file types
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS common_file_types AS
        SELECT 
            extension,
            COUNT(*) as count,
            SUM(size_bytes) as total_size
        FROM files
        WHERE extension IS NOT NULL
        GROUP BY extension
        ORDER BY count DESC
        LIMIT 20
    ''')
    
    conn.commit()

def main():
    # Define paths
    avatars_path = "/Users/steven/AVATARARTS"
    db_path = "/Users/steven/AVATARARTS_METADATA.db"
    
    print("Creating AVATARARTS metadata database...")
    
    # Create database
    conn = create_database(db_path)
    
    print("Populating database with file metadata...")
    populate_database(conn, avatars_path)
    
    print("Creating summary tables...")
    create_summary_tables(conn)
    
    # Print some statistics
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM files")
    file_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM directories")
    dir_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(size_bytes) FROM files")
    total_size = cursor.fetchone()[0] or 0
    
    print(f"\nDatabase Statistics:")
    print(f"Files indexed: {file_count:,}")
    print(f"Directories indexed: {dir_count:,}")
    print(f"Total size: {total_size / (1024**3):.2f} GB")
    
    conn.close()
    print(f"\nDatabase created: {db_path}")
    print("You can now query the database using standard SQL commands.")

if __name__ == "__main__":
    main()
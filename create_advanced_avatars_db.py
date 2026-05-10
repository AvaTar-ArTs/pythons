#!/usr/bin/env python3
"""
Advanced AVATARARTS File Metadata Database Generator
Creates a comprehensive SQLite database with better organization and structure
"""

import sqlite3
import os
import hashlib
from datetime import datetime
import mimetypes
from pathlib import Path
import json

def create_advanced_database(db_path):
    """Create the SQLite database with advanced tables and relationships"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute('PRAGMA foreign_keys = ON')
    
    # Create file categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            color_code TEXT DEFAULT '#CCCCCC'
        )
    ''')
    
    # Insert standard categories
    categories = [
        ('Python Scripts', 'Python automation and utility scripts', '#FFD700'),
        ('Documentation', 'Markdown and text documentation', '#87CEEB'),
        ('Images', 'Image files (PNG, JPG, etc.)', '#32CD32'),
        ('Web Files', 'HTML, CSS, JavaScript files', '#FF6347'),
        ('Data Files', 'JSON, CSV, XML data files', '#9370DB'),
        ('Configuration', 'Configuration and settings files', '#FFA500'),
        ('Archives', 'ZIP and compressed files', '#20B2AA'),
        ('Videos', 'Video files', '#FF4500'),
        ('Audio', 'Audio files', '#BA55D3'),
        ('Other', 'Miscellaneous file types', '#CCCCCC')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO file_categories (name, description, color_code) VALUES (?, ?, ?)', categories)
    
    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            start_date TEXT,
            status TEXT DEFAULT 'active',
            revenue_potential REAL DEFAULT 0.0
        )
    ''')
    
    # Insert known projects
    projects = [
        ('AI Automation Tools', '755+ Python scripts for automation', '2024-01-01', 'active', 150000),
        ('SEO Optimization Suite', 'Complete SEO Content Optimization Suite', '2024-01-01', 'active', 45000),
        ('Content Creation Pipeline', 'AI-powered content generation tools', '2024-01-01', 'active', 35000),
        ('Business Operations', 'SaaS products and automation tools', '2024-01-01', 'active', 125000),
        ('Heavenly Hands', 'Client project - call tracking and cleaning site', '2024-01-01', 'active', 0),
        ('Dr. Adu Project', 'Client project - medical practice SEO', '2024-01-01', 'active', 0),
        ('NotebookLM Integration', 'Google NotebookLM integration tools', '2024-01-01', 'active', 0)
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO projects (name, description, start_date, status, revenue_potential) VALUES (?, ?, ?, ?, ?)', projects)
    
    # Create directories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS directories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            parent_path TEXT,
            depth INTEGER,
            project_id INTEGER,
            file_count INTEGER DEFAULT 0,
            total_size INTEGER DEFAULT 0,
            created_time TEXT,
            modified_time TEXT,
            description TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    ''')
    
    # Create files table with better organization
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
            directory_id INTEGER,
            category_id INTEGER,
            project_id INTEGER,
            is_important BOOLEAN DEFAULT 0,
            tags TEXT,
            description TEXT,
            FOREIGN KEY (directory_id) REFERENCES directories(id),
            FOREIGN KEY (category_id) REFERENCES file_categories(id),
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    ''')
    
    # Create file relationships table for dependencies
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id_from INTEGER,
            file_id_to INTEGER,
            relationship_type TEXT, -- 'includes', 'calls', 'depends_on', 'similar_to'
            strength REAL DEFAULT 1.0, -- 0.0 to 1.0
            FOREIGN KEY (file_id_from) REFERENCES files(id),
            FOREIGN KEY (file_id_to) REFERENCES files(id)
        )
    ''')
    
    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_files_path ON files(path)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_files_extension ON files(extension)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_files_directory ON files(directory_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_files_category ON files(category_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_files_project ON files(project_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_files_important ON files(is_important)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_directories_path ON directories(path)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_directories_project ON directories(project_id)')
    
    conn.commit()
    return conn

def get_file_category(extension):
    """Determine file category based on extension"""
    ext = extension.lower() if extension else ''
    
    if ext in ['.py']:
        return 'Python Scripts'
    elif ext in ['.md', '.txt', '.rst']:
        return 'Documentation'
    elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']:
        return 'Images'
    elif ext in ['.html', '.css', '.js', '.jsx', '.ts', '.tsx']:
        return 'Web Files'
    elif ext in ['.json', '.csv', '.xml', '.yaml', '.yml']:
        return 'Data Files'
    elif ext in ['.conf', '.config', '.ini', '.env', '.toml']:
        return 'Configuration'
    elif ext in ['.zip', '.tar', '.gz', '.rar']:
        return 'Archives'
    elif ext in ['.mp4', '.avi', '.mov', '.wmv']:
        return 'Videos'
    elif ext in ['.mp3', '.wav', '.flac', '.aac']:
        return 'Audio'
    else:
        return 'Other'

def get_project_for_path(file_path):
    """Determine which project a file belongs to based on its path"""
    path_str = file_path.lower()
    
    if 'heavenlyhands' in path_str or 'heavenly_hands' in path_str:
        return 'Heavenly Hands'
    elif 'dr_' in path_str and 'adu' in path_str:
        return 'Dr. Adu Project'
    elif 'notebooklm' in path_str or 'notebook' in path_str:
        return 'NotebookLM Integration'
    elif 'pythons' in path_str or any(keyword in path_str for keyword in ['automation', 'script', 'utility']):
        return 'AI Automation Tools'
    elif 'seo' in path_str or 'optimization' in path_str:
        return 'SEO Optimization Suite'
    elif 'content' in path_str:
        return 'Content Creation Pipeline'
    elif any(keyword in path_str for keyword in ['business', 'operation', 'saas']):
        return 'Business Operations'
    else:
        return None

def get_file_metadata(file_path):
    """Get metadata for a file"""
    try:
        stat = os.stat(file_path)
        
        # Calculate MD5 hash (for smaller files only to save time)
        md5_hash = None
        if stat.st_size < 5 * 1024 * 1024:  # Only for files smaller than 5MB
            try:
                with open(file_path, 'rb') as f:
                    file_content = f.read()
                    md5_hash = hashlib.md5(file_content).hexdigest()
            except:
                md5_hash = None
        
        # Get MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        
        return {
            'path': file_path,
            'name': os.path.basename(file_path),
            'extension': os.path.splitext(file_path)[1],
            'size_bytes': stat.st_size,
            'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'accessed_time': datetime.fromtimestamp(stat.st_atime).isoformat(),
            'mime_type': mime_type,
            'md5_hash': md5_hash
        }
    except:
        return None

def populate_advanced_database(conn, avatars_path):
    """Populate the database with file metadata and relationships"""
    cursor = conn.cursor()
    
    # Define key directories to index with their associated projects
    key_directories = [
        ("/Users/steven/AVATARARTS/00_ACTIVE", "Business Operations"),
        ("/Users/steven/AVATARARTS/01_TOOLS", "AI Automation Tools"), 
        ("/Users/steven/AVATARARTS/02_DOCUMENTATION", "Documentation"),
        ("/Users/steven/AVATARARTS/pythons", "AI Automation Tools"),
        ("/Users/steven/AVATARARTS/notebookLM", "NotebookLM Integration"),
        ("/Users/steven/AVATARARTS/seo", "SEO Optimization Suite"),
        ("/Users/steven/AVATARARTS/scripts", "AI Automation Tools"),
        ("/Users/steven/AVATARARTS/heavenlyHands", "Heavenly Hands"),
        ("/Users/steven/AVATARARTS/REVENUE_LAUNCH_2026", "Business Operations"),
        ("/Users/steven/AVATARARTS/research_and_architecture", "Business Operations")
    ]
    
    file_id_map = {}  # Map file paths to IDs for relationship tracking
    count = 0
    
    for directory_path, project_name in key_directories:
        if os.path.exists(directory_path):
            print(f"Processing directory: {directory_path} (Project: {project_name})")
            
            # Get project ID
            cursor.execute("SELECT id FROM projects WHERE name = ?", (project_name,))
            project_result = cursor.fetchone()
            project_id = project_result[0] if project_result else None
            
            for root, dirs, files in os.walk(directory_path):
                # Calculate directory depth
                root_path = Path(root)
                avatars_root = Path(avatars_path)
                depth = len(root_path.relative_to(avatars_root).parts) if root_path != avatars_root else 0
                
                # Process directories
                parent_path = str(Path(root).parent)
                if parent_path == str(avatars_root.parent):  # Handle root case
                    parent_path = None
                
                dir_name = os.path.basename(root)
                
                # Insert directory
                cursor.execute('''
                    INSERT OR IGNORE INTO directories 
                    (path, name, parent_path, depth, project_id, created_time, modified_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    root,
                    dir_name,
                    parent_path,
                    depth,
                    project_id,
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
                
                # Get directory ID
                cursor.execute("SELECT id FROM directories WHERE path = ?", (root,))
                dir_result = cursor.fetchone()
                directory_id = dir_result[0] if dir_result else None
                
                # Process files in this directory
                for f in files:
                    file_path = os.path.join(root, f)
                    metadata = get_file_metadata(file_path)
                    
                    if metadata:
                        # Determine category
                        category_name = get_file_category(metadata['extension'])
                        cursor.execute("SELECT id FROM file_categories WHERE name = ?", (category_name,))
                        category_result = cursor.fetchone()
                        category_id = category_result[0] if category_result else None
                        
                        # Determine project
                        assigned_project_name = get_project_for_path(file_path)
                        if assigned_project_name:
                            cursor.execute("SELECT id FROM projects WHERE name = ?", (assigned_project_name,))
                            proj_result = cursor.fetchone()
                            assigned_project_id = proj_result[0] if proj_result else project_id
                        else:
                            assigned_project_id = project_id
                        
                        # Determine if file is important based on name
                        is_important = any(keyword in metadata['name'].lower() for keyword in 
                                         ['readme', 'summary', 'plan', 'guide', 'analysis', 'strategy'])
                        
                        # Insert file
                        cursor.execute('''
                            INSERT INTO files 
                            (path, name, extension, size_bytes, created_time, modified_time, 
                             accessed_time, mime_type, md5_hash, directory_id, category_id, 
                             project_id, is_important)
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
                            directory_id,
                            category_id,
                            assigned_project_id,
                            is_important
                        ))
                        
                        # Store file ID for potential relationships
                        file_id = cursor.lastrowid
                        file_id_map[file_path] = file_id
                        
                        count += 1
                        if count % 500 == 0:
                            print(f"Processed {count} files...")
                            conn.commit()
                
                # Update directory file count and total size
                if directory_id:
                    cursor.execute('''
                        UPDATE directories 
                        SET file_count = (SELECT COUNT(*) FROM files WHERE directory_id = ?),
                            total_size = (SELECT COALESCE(SUM(size_bytes), 0) FROM files WHERE directory_id = ?)
                        WHERE id = ?
                    ''', (directory_id, directory_id, directory_id))
                
                # Limit total files to prevent timeout
                if count >= 8000:  # Increased limit for better coverage
                    print(f"Reached limit of {count} files")
                    break
            
            if count >= 8000:
                break
    
    conn.commit()
    print(f"Database populated with {count} files")

def create_advanced_summary_views(conn):
    """Create advanced summary views for analysis"""
    cursor = conn.cursor()
    
    # Project summary view
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS project_summary AS
        SELECT 
            p.name as project_name,
            p.description,
            p.status,
            p.revenue_potential,
            COUNT(f.id) as file_count,
            SUM(f.size_bytes) as total_size,
            COUNT(DISTINCT d.id) as directory_count
        FROM projects p
        LEFT JOIN files f ON p.id = f.project_id
        LEFT JOIN directories d ON p.id = d.project_id
        GROUP BY p.id, p.name, p.description, p.status, p.revenue_potential
        ORDER BY p.revenue_potential DESC
    ''')
    
    # File category distribution
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS category_distribution AS
        SELECT 
            fc.name as category_name,
            fc.description,
            fc.color_code,
            COUNT(f.id) as file_count,
            SUM(f.size_bytes) as total_size,
            AVG(f.size_bytes) as avg_size
        FROM file_categories fc
        LEFT JOIN files f ON fc.id = f.category_id
        GROUP BY fc.id, fc.name, fc.description, fc.color_code
        ORDER BY file_count DESC
    ''')
    
    # Directory structure view
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS directory_structure AS
        SELECT 
            d.name as directory_name,
            d.path,
            d.depth,
            p.name as project_name,
            d.file_count,
            d.total_size,
            d.created_time
        FROM directories d
        LEFT JOIN projects p ON d.project_id = p.id
        ORDER BY d.depth, d.path
    ''')
    
    # Important files view
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS important_files AS
        SELECT 
            f.name,
            f.path,
            f.extension,
            f.size_bytes,
            f.modified_time,
            fc.name as category,
            p.name as project
        FROM files f
        JOIN file_categories fc ON f.category_id = fc.id
        LEFT JOIN projects p ON f.project_id = p.id
        WHERE f.is_important = 1
        ORDER BY f.size_bytes DESC
    ''')
    
    # File size distribution
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS file_size_analysis AS
        SELECT 
            CASE 
                WHEN size_bytes < 1024 THEN 'Tiny (< 1KB)'
                WHEN size_bytes < 10240 THEN 'Small (1-10KB)'
                WHEN size_bytes < 102400 THEN 'Medium (10-100KB)'
                WHEN size_bytes < 1048576 THEN 'Large (100KB-1MB)'
                ELSE 'Huge (> 1MB)'
            END as size_category,
            COUNT(*) as file_count,
            SUM(size_bytes) as total_size,
            AVG(size_bytes) as avg_size
        FROM files
        GROUP BY size_category
        ORDER BY avg_size
    ''')
    
    conn.commit()

def main():
    # Define paths
    avatars_path = "/Users/steven/AVATARARTS"
    db_path = "/Users/steven/AVATARARTS_ADVANCED_METADATA.db"
    
    print("Creating advanced AVATARARTS metadata database with better organization...")
    
    # Create database
    conn = create_advanced_database(db_path)
    
    print("Populating database with file metadata and relationships...")
    populate_advanced_database(conn, avatars_path)
    
    print("Creating advanced summary views...")
    create_advanced_summary_views(conn)
    
    # Print some statistics
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM files")
    file_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM directories")
    dir_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM projects")
    project_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(size_bytes) FROM files")
    total_size = cursor.fetchone()[0] or 0
    
    print(f"\nAdvanced Database Statistics:")
    print(f"Files indexed: {file_count:,}")
    print(f"Directories indexed: {dir_count:,}")
    print(f"Projects identified: {project_count:,}")
    print(f"Total size: {total_size / (1024**3):.2f} GB")
    
    # Show project summary
    print(f"\nProject Summary:")
    cursor.execute("""
        SELECT project_name, file_count, total_size, revenue_potential 
        FROM project_summary 
        ORDER BY revenue_potential DESC
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]:,} files, {row[2] / (1024*1024):.2f} MB, ${row[3]:,.0f} potential")
    
    # Show category distribution
    print(f"\nCategory Distribution:")
    cursor.execute("""
        SELECT category_name, file_count, total_size 
        FROM category_distribution 
        ORDER BY file_count DESC
    """)
    for row in cursor.fetchall()[:10]:  # Top 10
        print(f"  {row[0]}: {row[1]:,} files, {row[2] / (1024*1024):.2f} MB")
    
    conn.close()
    print(f"\nAdvanced database created: {db_path}")
    print("The database includes projects, categories, relationships, and advanced analytics.")
    print("\nKey tables:")
    print("  - files: Detailed file metadata with project associations")
    print("  - directories: Directory structure with project mappings")
    print("  - projects: Business projects with revenue potential")
    print("  - file_categories: Organized file types")
    print("  - file_relationships: Dependencies between files")
    print("\nKey views:")
    print("  - project_summary: Files and sizes by project")
    print("  - category_distribution: File types breakdown")
    print("  - directory_structure: Organized directory view")
    print("  - important_files: Key files marked as important")
    print("  - file_size_analysis: Size distribution analysis")

if __name__ == "__main__":
    main()
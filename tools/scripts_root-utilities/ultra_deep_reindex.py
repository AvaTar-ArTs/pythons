#!/usr/bin/env python3
"""
Ultra Deep Reindexing System - Unlimited Depth
Completely reindexes everything in /Users/steven/AVATARARTS with UNLIMITED depth scanning.
Ensures no directory is missed regardless of nesting level.
"""

import hashlib
import json
import csv
import sqlite3
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import mimetypes

class UltraDeepReindexer:
    """Complete reindexing system with unlimited depth scanning."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root).resolve()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'max_depth': 0,
            'by_extension': Counter(),
            'by_directory': {},
            'by_type': Counter(),
            'large_files': [],
            'recent_files': [],
            'old_files': [],
            'depth_distribution': Counter()
        }
        
        # Index data
        self.file_index = []
        self.dir_index = []
        
        # Exclude patterns (but still scan to verify depth)
        self.exclude_patterns = [
            'node_modules', '.git', '__pycache__', '.venv', 'venv',
            '.next', 'dist', 'build', '.cache', '.DS_Store',
            '.pytest_cache', '.mypy_cache', '.tox'
        ]
    
    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded from indexing."""
        path_str = str(path)
        return any(pattern in path_str for pattern in self.exclude_patterns)
    
    def calculate_file_hash(self, file_path: Path, max_size: int = 100 * 1024 * 1024) -> str:
        """Calculate content hash with chunking for large files."""
        try:
            size = file_path.stat().st_size
            if size > max_size:
                # For large files, hash first+middle+last chunks
                md5 = hashlib.md5()
                with open(file_path, 'rb') as f:
                    md5.update(f.read(8192))
                    f.seek(size // 2)
                    md5.update(f.read(8192))
                    f.seek(max(0, size - 8192))
                    md5.update(f.read(8192))
                    md5.update(str(size).encode())
                return md5.hexdigest()
            
            # Full hash for smaller files
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            return None
    
    def get_file_type(self, file_path: Path) -> str:
        """Determine file type category."""
        ext = file_path.suffix.lower()
        
        type_map = {
            # Code
            '.py': 'code_python',
            '.js': 'code_javascript',
            '.ts': 'code_typescript',
            '.jsx': 'code_javascript',
            '.tsx': 'code_typescript',
            '.html': 'code_html',
            '.css': 'code_css',
            '.sh': 'code_shell',
            '.json': 'code_json',
            '.yaml': 'code_yaml',
            '.yml': 'code_yaml',
            '.xml': 'code_xml',
            
            # Documents
            '.md': 'document_markdown',
            '.txt': 'document_text',
            '.pdf': 'document_pdf',
            '.doc': 'document_word',
            '.docx': 'document_word',
            '.xls': 'document_excel',
            '.xlsx': 'document_excel',
            '.ppt': 'document_powerpoint',
            '.pptx': 'document_powerpoint',
            
            # Images
            '.jpg': 'image',
            '.jpeg': 'image',
            '.png': 'image',
            '.gif': 'image',
            '.svg': 'image',
            '.webp': 'image',
            '.ico': 'image',
            '.bmp': 'image',
            '.tiff': 'image',
            '.tif': 'image',
            
            # Audio
            '.mp3': 'audio',
            '.wav': 'audio',
            '.flac': 'audio',
            '.aac': 'audio',
            '.ogg': 'audio',
            '.m4a': 'audio',
            '.wma': 'audio',
            
            # Video
            '.mp4': 'video',
            '.avi': 'video',
            '.mov': 'video',
            '.mkv': 'video',
            '.wmv': 'video',
            '.flv': 'video',
            '.webm': 'video',
            
            # Archives
            '.zip': 'archive',
            '.tar': 'archive',
            '.gz': 'archive',
            '.rar': 'archive',
            '.7z': 'archive',
            
            # Data
            '.csv': 'data',
            '.db': 'data',
            '.sqlite': 'data',
            '.sqlite3': 'data',
            
            # Fonts
            '.ttf': 'font',
            '.otf': 'font',
            '.woff': 'font',
            '.woff2': 'font',
            '.eot': 'font',
        }
        
        return type_map.get(ext, 'other')
    
    def index_file(self, file_path: Path):
        """Index a single file with comprehensive metadata."""
        try:
            stat = file_path.stat()
            rel_path = str(file_path.relative_to(self.workspace_root))
            parts = Path(rel_path).parts
            
            # Basic info
            size = stat.st_size
            ext = file_path.suffix.lower()
            file_type = self.get_file_type(file_path)
            
            # Calculate hash
            content_hash = self.calculate_file_hash(file_path)
            
            # MIME type
            mime_type, _ = mimetypes.guess_type(str(file_path))
            
            # Directory info
            parent_dir = str(file_path.parent.relative_to(self.workspace_root))
            depth = len(parts)
            
            # Update max depth
            if depth > self.stats['max_depth']:
                self.stats['max_depth'] = depth
            
            # Track depth distribution
            self.stats['depth_distribution'][depth] += 1
            
            # Check if nested (repeated folder names)
            is_nested = depth > 3 and any(parts[i] == parts[i+1] for i in range(len(parts)-1))
            
            file_data = {
                'path': rel_path,
                'full_path': str(file_path),
                'filename': file_path.name,
                'parent_directory': parent_dir,
                'extension': ext or '(no extension)',
                'file_type': file_type,
                'mime_type': mime_type or 'unknown',
                'size': size,
                'size_mb': size / (1024 * 1024),
                'size_gb': size / (1024 * 1024 * 1024),
                'content_hash': content_hash,
                'depth': depth,
                'is_nested': is_nested,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'accessed': datetime.fromtimestamp(stat.st_atime).isoformat(),
            }
            
            self.file_index.append(file_data)
            
            # Update statistics
            self.stats['total_files'] += 1
            self.stats['total_size'] += size
            self.stats['by_extension'][ext or '(no extension)'] += 1
            self.stats['by_type'][file_type] += 1
            # Initialize directory stats if needed
            if parent_dir not in self.stats['by_directory']:
                self.stats['by_directory'][parent_dir] = {'count': 0, 'size': 0}
            # Update directory stats
            dir_stats = self.stats['by_directory'][parent_dir]
            dir_stats['count'] = dir_stats.get('count', 0) + 1
            dir_stats['size'] = dir_stats.get('size', 0) + size
            
            # Track large files (>100MB)
            if size > 100 * 1024 * 1024:
                self.stats['large_files'].append({
                    'path': rel_path,
                    'size_mb': size / (1024 * 1024)
                })
            
            # Track recent files (last 30 days)
            days_old = (datetime.now().timestamp() - stat.st_mtime) / 86400
            if days_old < 30:
                self.stats['recent_files'].append({
                    'path': rel_path,
                    'days_old': days_old
                })
            elif days_old > 365:
                self.stats['old_files'].append({
                    'path': rel_path,
                    'days_old': days_old
                })
            
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")
    
    def index_directory(self, dir_path: Path):
        """Index a directory with metadata."""
        try:
            rel_path = str(dir_path.relative_to(self.workspace_root))
            parts = Path(rel_path).parts
            depth = len(parts)
            
            # Count files in directory
            file_count = sum(1 for _ in dir_path.iterdir() if _.is_file())
            
            dir_data = {
                'path': rel_path,
                'full_path': str(dir_path),
                'name': dir_path.name,
                'parent_directory': str(dir_path.parent.relative_to(self.workspace_root)) if dir_path != self.workspace_root else '',
                'depth': depth,
                'file_count': file_count
            }
            
            self.dir_index.append(dir_data)
            self.stats['total_dirs'] += 1
            
        except Exception as e:
            print(f"Error indexing directory {dir_path}: {e}")
    
    def scan_unlimited_depth(self):
        """Scan with unlimited depth using os.walk for maximum reliability."""
        print(f"🔍 Starting unlimited depth scan of {self.workspace_root}")
        print("   This will scan ALL directories regardless of nesting level...")
        
        files_scanned = 0
        dirs_scanned = 0
        excluded_files = 0
        excluded_dirs = 0
        
        # Use os.walk for unlimited depth traversal
        for root, dirs, files in os.walk(self.workspace_root, topdown=True):
            root_path = Path(root)
            
            # Filter out excluded directories from further traversal
            dirs[:] = [d for d in dirs if not self.should_exclude(root_path / d)]
            
            # Index directory
            if not self.should_exclude(root_path):
                self.index_directory(root_path)
                dirs_scanned += 1
            else:
                excluded_dirs += 1
            
            # Index files
            for file in files:
                file_path = root_path / file
                if not self.should_exclude(file_path):
                    self.index_file(file_path)
                    files_scanned += 1
                else:
                    excluded_files += 1
                
                # Progress indicator
                if files_scanned % 1000 == 0:
                    print(f"   Scanned {files_scanned:,} files, {dirs_scanned:,} directories... (max depth: {self.stats['max_depth']})")
        
        print(f"\n✅ Scan complete!")
        print(f"   Files indexed: {files_scanned:,}")
        print(f"   Directories indexed: {dirs_scanned:,}")
        print(f"   Excluded files: {excluded_files:,}")
        print(f"   Excluded directories: {excluded_dirs:,}")
        print(f"   Maximum depth found: {self.stats['max_depth']}")
        print(f"   Total size: {self.stats['total_size'] / (1024**3):.2f} GB")
    
    def save_to_csv(self):
        """Save indexes to CSV files."""
        base_name = f"ULTRA_DEEP_REINDEX_{self.timestamp}"
        
        # Files CSV
        files_csv = f"{base_name}_FILES.csv"
        if self.file_index:
            with open(files_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.file_index[0].keys())
                writer.writeheader()
                writer.writerows(self.file_index)
            print(f"✅ Saved {len(self.file_index):,} files to {files_csv}")
        
        # Directories CSV
        dirs_csv = f"{base_name}_DIRECTORIES.csv"
        if self.dir_index:
            with open(dirs_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.dir_index[0].keys())
                writer.writeheader()
                writer.writerows(self.dir_index)
            print(f"✅ Saved {len(self.dir_index):,} directories to {dirs_csv}")
        
        # Statistics CSV
        stats_csv = f"{base_name}_STATISTICS.csv"
        stats_data = [{
            'metric': 'total_files',
            'value': self.stats['total_files']
        }, {
            'metric': 'total_dirs',
            'value': self.stats['total_dirs']
        }, {
            'metric': 'total_size_gb',
            'value': self.stats['total_size'] / (1024**3)
        }, {
            'metric': 'max_depth',
            'value': self.stats['max_depth']
        }]
        
        with open(stats_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['metric', 'value'])
            writer.writeheader()
            writer.writerows(stats_data)
        print(f"✅ Saved statistics to {stats_csv}")
    
    def save_to_json(self):
        """Save complete index to JSON."""
        base_name = f"ULTRA_DEEP_REINDEX_{self.timestamp}_COMPLETE.json"
        
        data = {
            'timestamp': self.timestamp,
            'workspace_root': str(self.workspace_root),
            'statistics': {
                'total_files': self.stats['total_files'],
                'total_dirs': self.stats['total_dirs'],
                'total_size': self.stats['total_size'],
                'total_size_gb': self.stats['total_size'] / (1024**3),
                'max_depth': self.stats['max_depth'],
                'depth_distribution': dict(self.stats['depth_distribution']),
                'by_type': dict(self.stats['by_type']),
                'by_extension': dict(self.stats['by_extension']),
            },
            'files': self.file_index,
            'directories': self.dir_index
        }
        
        with open(base_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved complete index to {base_name}")
    
    def save_to_sqlite(self):
        """Save to SQLite database for fast querying."""
        db_name = f"ULTRA_DEEP_REINDEX_{self.timestamp}.db"
        
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Create files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE,
                full_path TEXT,
                filename TEXT,
                parent_directory TEXT,
                extension TEXT,
                file_type TEXT,
                mime_type TEXT,
                size INTEGER,
                size_mb REAL,
                size_gb REAL,
                content_hash TEXT,
                depth INTEGER,
                is_nested INTEGER,
                created TEXT,
                modified TEXT,
                accessed TEXT
            )
        ''')
        
        # Create directories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS directories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE,
                full_path TEXT,
                name TEXT,
                parent_directory TEXT,
                depth INTEGER,
                file_count INTEGER
            )
        ''')
        
        # Create indexes for fast queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_files_path ON files(path)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_files_type ON files(file_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_files_depth ON files(depth)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_files_hash ON files(content_hash)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_dirs_path ON directories(path)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_dirs_depth ON directories(depth)')
        
        # Insert files
        print("💾 Saving files to database...")
        for file_data in self.file_index:
            cursor.execute('''
                INSERT OR REPLACE INTO files 
                (path, full_path, filename, parent_directory, extension, file_type, mime_type,
                 size, size_mb, size_gb, content_hash, depth, is_nested, created, modified, accessed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                file_data['path'], file_data['full_path'], file_data['filename'],
                file_data['parent_directory'], file_data['extension'], file_data['file_type'],
                file_data['mime_type'], file_data['size'], file_data['size_mb'],
                file_data['size_gb'], file_data['content_hash'], file_data['depth'],
                int(file_data['is_nested']), file_data['created'], file_data['modified'],
                file_data['accessed']
            ))
        
        # Insert directories
        print("💾 Saving directories to database...")
        for dir_data in self.dir_index:
            cursor.execute('''
                INSERT OR REPLACE INTO directories 
                (path, full_path, name, parent_directory, depth, file_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                dir_data['path'], dir_data['full_path'], dir_data['name'],
                dir_data['parent_directory'], dir_data['depth'], dir_data['file_count']
            ))
        
        conn.commit()
        conn.close()
        print(f"✅ Saved to SQLite database: {db_name}")
    
    def generate_report(self):
        """Generate markdown report."""
        report_name = f"ULTRA_DEEP_REINDEX_REPORT_{self.timestamp}.md"
        
        with open(report_name, 'w', encoding='utf-8') as f:
            f.write(f"# Ultra Deep Reindex Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Workspace:** {self.workspace_root}\n")
            f.write(f"**Method:** Unlimited depth scanning (os.walk)\n\n")
            f.write("---\n\n")
            
            f.write("## 📊 Summary Statistics\n\n")
            f.write(f"- **Total Files:** {self.stats['total_files']:,}\n")
            f.write(f"- **Total Directories:** {self.stats['total_dirs']:,}\n")
            f.write(f"- **Total Size:** {self.stats['total_size'] / (1024**3):.2f} GB\n")
            f.write(f"- **Maximum Depth:** {self.stats['max_depth']} levels\n\n")
            
            f.write("## 📈 Depth Distribution\n\n")
            f.write("| Depth | Files |\n")
            f.write("|-------|-------|\n")
            for depth in sorted(self.stats['depth_distribution'].keys()):
                count = self.stats['depth_distribution'][depth]
                f.write(f"| {depth} | {count:,} |\n")
            f.write("\n")
            
            f.write("## 📁 File Types\n\n")
            f.write("| Type | Count | Size (GB) |\n")
            f.write("|------|-------|-----------|\n")
            for file_type, count in self.stats['by_type'].most_common(20):
                size = sum(f['size'] for f in self.file_index if f['file_type'] == file_type)
                f.write(f"| {file_type} | {count:,} | {size / (1024**3):.2f} |\n")
            f.write("\n")
            
            if self.stats['large_files']:
                f.write("## 📦 Largest Files (>100MB)\n\n")
                f.write("| File | Size (MB) |\n")
                f.write("|------|-----------|\n")
                for large_file in sorted(self.stats['large_files'], key=lambda x: x['size_mb'], reverse=True)[:20]:
                    f.write(f"| {large_file['path']} | {large_file['size_mb']:.1f} |\n")
                f.write("\n")
        
        print(f"✅ Generated report: {report_name}")


def main():
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    print("=" * 70)
    print("ULTRA DEEP REINDEX - UNLIMITED DEPTH SCANNING")
    print("=" * 70)
    print()
    
    reindexer = UltraDeepReindexer(workspace_root)
    
    # Scan with unlimited depth
    reindexer.scan_unlimited_depth()
    
    # Save outputs
    print("\n💾 Saving indexes...")
    reindexer.save_to_csv()
    reindexer.save_to_json()
    reindexer.save_to_sqlite()
    reindexer.generate_report()
    
    print("\n" + "=" * 70)
    print("✅ ULTRA DEEP REINDEX COMPLETE")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"   Files: {reindexer.stats['total_files']:,}")
    print(f"   Directories: {reindexer.stats['total_dirs']:,}")
    print(f"   Max Depth: {reindexer.stats['max_depth']} levels")
    print(f"   Total Size: {reindexer.stats['total_size'] / (1024**3):.2f} GB")
    print(f"\n📁 Database: ULTRA_DEEP_REINDEX_{reindexer.timestamp}.db")
    print(f"📄 CSV Files: ULTRA_DEEP_REINDEX_{reindexer.timestamp}_*.csv")
    print(f"📋 Report: ULTRA_DEEP_REINDEX_REPORT_{reindexer.timestamp}.md")


if __name__ == "__main__":
    main()

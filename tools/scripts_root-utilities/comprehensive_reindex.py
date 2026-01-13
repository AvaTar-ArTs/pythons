#!/usr/bin/env python3
"""
Comprehensive Reindexing System
Completely reindexes everything in /Users/steven/AVATARARTS with full metadata.
Creates searchable indexes, CSVs, and JSON database.
"""

import hashlib
import json
import csv
import sqlite3
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import mimetypes

class ComprehensiveReindexer:
    """Complete reindexing system for workspace."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Statistics
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'by_extension': Counter(),
            'by_directory': defaultdict(lambda: {'count': 0, 'size': 0}),
            'by_type': defaultdict(lambda: {'count': 0, 'size': 0}),
            'large_files': [],
            'recent_files': [],
            'old_files': []
        }
        
        # Index data
        self.file_index = []
        self.dir_index = []
        
        # Exclude patterns
        self.exclude_patterns = [
            'node_modules', '.git', '__pycache__', '.venv', 'venv',
            '.next', 'dist', 'build', '.cache', '.DS_Store',
            '.pytest_cache', '.mypy_cache', '.tox'
        ]
    
    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        path_str = str(path)
        return any(pattern in path_str for pattern in self.exclude_patterns)
    
    def calculate_file_hash(self, file_path: Path, max_size: int = 100 * 1024 * 1024) -> str:
        """Calculate content hash."""
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
        except:
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
            
            # Images
            '.jpg': 'image',
            '.jpeg': 'image',
            '.png': 'image',
            '.gif': 'image',
            '.webp': 'image',
            '.svg': 'image',
            '.bmp': 'image',
            
            # Audio
            '.mp3': 'audio',
            '.wav': 'audio',
            '.m4a': 'audio',
            '.flac': 'audio',
            
            # Video
            '.mp4': 'video',
            '.mov': 'video',
            '.avi': 'video',
            '.mkv': 'video',
            
            # Data
            '.csv': 'data',
            '.tsv': 'data',
            '.db': 'data_database',
            '.sqlite': 'data_database',
            
            # Archives
            '.zip': 'archive',
            '.tar': 'archive',
            '.gz': 'archive',
            '.rar': 'archive',
            
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
            
            # Check if nested
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
            self.stats['by_directory'][parent_dir]['count'] += 1
            self.stats['by_directory'][parent_dir]['size'] += size
            self.stats['by_type'][file_type]['count'] += 1
            self.stats['by_type'][file_type]['size'] += size
            
            # Track large files
            if size > 100 * 1024 * 1024:  # > 100MB
                self.stats['large_files'].append({
                    'path': rel_path,
                    'size_mb': size / (1024 * 1024)
                })
            
            # Track recent files (modified in last 30 days)
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
            pass
    
    def index_directory(self, dir_path: Path):
        """Index a directory."""
        try:
            rel_path = str(dir_path.relative_to(self.workspace_root))
            parts = Path(rel_path).parts
            
            # Count files in directory
            file_count = sum(1 for _ in dir_path.iterdir() if _.is_file())
            dir_count = sum(1 for _ in dir_path.iterdir() if _.is_dir())
            
            dir_data = {
                'path': rel_path,
                'full_path': str(dir_path),
                'name': dir_path.name,
                'parent_directory': str(dir_path.parent.relative_to(self.workspace_root)) if dir_path != self.workspace_root else '',
                'depth': len(parts),
                'file_count': file_count,
                'subdirectory_count': dir_count,
                'is_empty': file_count == 0 and dir_count == 0,
                'is_nested': len(parts) > 3 and any(parts[i] == parts[i+1] for i in range(len(parts)-1))
            }
            
            self.dir_index.append(dir_data)
            self.stats['total_dirs'] += 1
        
        except Exception:
            pass
    
    def scan_workspace(self):
        """Scan entire workspace."""
        print("=" * 80)
        print("COMPREHENSIVE REINDEXING")
        print("=" * 80)
        print(f"Workspace: {self.workspace_root}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print("🔍 Scanning workspace...")
        
        # Scan directories first
        print("   Indexing directories...")
        for dir_path in self.workspace_root.rglob('*'):
            if dir_path.is_dir() and not self.should_exclude(dir_path):
                self.index_directory(dir_path)
        
        # Scan files
        print("   Indexing files...")
        file_count = 0
        for file_path in self.workspace_root.rglob('*'):
            if file_path.is_file() and not self.should_exclude(file_path):
                self.index_file(file_path)
                file_count += 1
                
                if file_count % 1000 == 0:
                    print(f"      Processed {file_count:,} files...")
        
        print(f"\n✅ Scan complete!")
        print(f"   Files indexed: {len(self.file_index):,}")
        print(f"   Directories indexed: {len(self.dir_index):,}")
        print(f"   Total size: {self.stats['total_size'] / (1024**3):.2f} GB")
    
    def generate_csv_indexes(self):
        """Generate CSV index files."""
        print("\n💾 Generating CSV indexes...")
        
        base_name = f"REINDEX_{self.timestamp}"
        
        # 1. Complete file index
        files_csv = self.workspace_root / f"{base_name}_FILES.csv"
        print(f"   Creating: {files_csv.name}")
        with open(files_csv, 'w', newline='', encoding='utf-8') as f:
            if self.file_index:
                fieldnames = list(self.file_index[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.file_index)
        
        # 2. Directory index
        dirs_csv = self.workspace_root / f"{base_name}_DIRECTORIES.csv"
        print(f"   Creating: {dirs_csv.name}")
        with open(dirs_csv, 'w', newline='', encoding='utf-8') as f:
            if self.dir_index:
                fieldnames = list(self.dir_index[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.dir_index)
        
        # 3. Statistics summary
        stats_csv = self.workspace_root / f"{base_name}_STATISTICS.csv"
        print(f"   Creating: {stats_csv.name}")
        with open(stats_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Category', 'Metric', 'Value'])
            writer.writerow(['General', 'Total Files', self.stats['total_files']])
            writer.writerow(['General', 'Total Directories', self.stats['total_dirs']])
            writer.writerow(['General', 'Total Size (GB)', f"{self.stats['total_size'] / (1024**3):.2f}"])
            writer.writerow(['General', 'Large Files (>100MB)', len(self.stats['large_files'])])
            writer.writerow(['General', 'Recent Files (<30 days)', len(self.stats['recent_files'])])
            writer.writerow(['General', 'Old Files (>1 year)', len(self.stats['old_files'])])
            
            # By extension
            for ext, count in self.stats['by_extension'].most_common(50):
                writer.writerow(['By Extension', ext, count])
            
            # By type
            for file_type, data in sorted(self.stats['by_type'].items(), key=lambda x: x[1]['count'], reverse=True):
                writer.writerow(['By Type', file_type, f"{data['count']} files, {data['size']/(1024**3):.2f} GB"])
        
        return files_csv, dirs_csv, stats_csv
    
    def generate_json_index(self):
        """Generate JSON index for fast searching."""
        print("\n💾 Generating JSON index...")
        
        json_file = self.workspace_root / f"REINDEX_{self.timestamp}_COMPLETE.json"
        
        index_data = {
            'metadata': {
                'workspace': str(self.workspace_root),
                'indexed_at': datetime.now().isoformat(),
                'total_files': len(self.file_index),
                'total_directories': len(self.dir_index),
                'total_size_gb': self.stats['total_size'] / (1024**3)
            },
            'statistics': {
                'by_extension': dict(self.stats['by_extension'].most_common(100)),
                'by_type': {k: {'count': v['count'], 'size_gb': v['size']/(1024**3)} 
                           for k, v in self.stats['by_type'].items()},
                'large_files': self.stats['large_files'][:100],
                'recent_files': self.stats['recent_files'][:100],
                'old_files': self.stats['old_files'][:100]
            },
            'files': self.file_index,
            'directories': self.dir_index
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ JSON index created: {json_file.name}")
        return json_file
    
    def generate_sqlite_index(self):
        """Generate SQLite database for fast querying."""
        print("\n💾 Generating SQLite database...")
        
        db_file = self.workspace_root / f"REINDEX_{self.timestamp}.db"
        
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Create files table
        cursor.execute('''
            CREATE TABLE files (
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
            CREATE TABLE directories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE,
                full_path TEXT,
                name TEXT,
                parent_directory TEXT,
                depth INTEGER,
                file_count INTEGER,
                subdirectory_count INTEGER,
                is_empty INTEGER,
                is_nested INTEGER
            )
        ''')
        
        # Insert files
        print("   Inserting files into database...")
        for file_data in self.file_index:
            cursor.execute('''
                INSERT OR REPLACE INTO files 
                (path, full_path, filename, parent_directory, extension, file_type, mime_type,
                 size, size_mb, content_hash, depth, is_nested, created, modified, accessed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                file_data['path'], file_data['full_path'], file_data['filename'],
                file_data['parent_directory'], file_data['extension'], file_data['file_type'],
                file_data['mime_type'], file_data['size'], file_data['size_mb'],
                file_data['content_hash'], file_data['depth'], int(file_data['is_nested']),
                file_data['created'], file_data['modified'], file_data['accessed']
            ))
        
        # Insert directories
        print("   Inserting directories into database...")
        for dir_data in self.dir_index:
            cursor.execute('''
                INSERT OR REPLACE INTO directories
                (path, full_path, name, parent_directory, depth, file_count, 
                 subdirectory_count, is_empty, is_nested)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                dir_data['path'], dir_data['full_path'], dir_data['name'],
                dir_data['parent_directory'], dir_data['depth'], dir_data['file_count'],
                dir_data['subdirectory_count'], int(dir_data['is_empty']), int(dir_data['is_nested'])
            ))
        
        # Create indexes for fast searching
        print("   Creating search indexes...")
        cursor.execute('CREATE INDEX idx_files_path ON files(path)')
        cursor.execute('CREATE INDEX idx_files_extension ON files(extension)')
        cursor.execute('CREATE INDEX idx_files_type ON files(file_type)')
        cursor.execute('CREATE INDEX idx_files_hash ON files(content_hash)')
        cursor.execute('CREATE INDEX idx_dirs_path ON directories(path)')
        
        conn.commit()
        conn.close()
        
        print(f"   ✅ SQLite database created: {db_file.name}")
        return db_file
    
    def generate_report(self):
        """Generate markdown report."""
        report_file = self.workspace_root / f"REINDEX_REPORT_{self.timestamp}.md"
        
        print("\n📝 Generating markdown report...")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive Reindexing Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Workspace:** `{self.workspace_root}`\n\n")
            f.write("---\n\n")
            
            f.write("## 📊 Executive Summary\n\n")
            f.write(f"- **Total Files:** {self.stats['total_files']:,}\n")
            f.write(f"- **Total Directories:** {self.stats['total_dirs']:,}\n")
            f.write(f"- **Total Size:** {self.stats['total_size'] / (1024**3):.2f} GB\n")
            f.write(f"- **Large Files (>100MB):** {len(self.stats['large_files'])}\n")
            f.write(f"- **Recent Files (<30 days):** {len(self.stats['recent_files'])}\n")
            f.write(f"- **Old Files (>1 year):** {len(self.stats['old_files'])}\n\n")
            
            f.write("## 📁 Top File Extensions\n\n")
            f.write("| Extension | Count | Percentage |\n")
            f.write("|-----------|------:|----------:|\n")
            total = self.stats['total_files']
            for ext, count in self.stats['by_extension'].most_common(30):
                pct = (count / total) * 100 if total > 0 else 0
                f.write(f"| `{ext}` | {count:,} | {pct:.1f}% |\n")
            f.write("\n")
            
            f.write("## 📂 File Types\n\n")
            f.write("| Type | Count | Size (GB) |\n")
            f.write("|------|------:|----------:|\n")
            for file_type, data in sorted(self.stats['by_type'].items(), key=lambda x: x[1]['count'], reverse=True):
                f.write(f"| `{file_type}` | {data['count']:,} | {data['size']/(1024**3):.2f} |\n")
            f.write("\n")
            
            if self.stats['large_files']:
                f.write("## 💾 Largest Files\n\n")
                f.write("| File | Size (MB) |\n")
                f.write("|------|----------:|\n")
                for file_info in sorted(self.stats['large_files'], key=lambda x: x['size_mb'], reverse=True)[:50]:
                    f.write(f"| `{file_info['path']}` | {file_info['size_mb']:.1f} |\n")
                f.write("\n")
        
        print(f"   ✅ Report created: {report_file.name}")
        return report_file

def main():
    """Main execution."""
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    reindexer = ComprehensiveReindexer(workspace_root)
    
    # Scan workspace
    reindexer.scan_workspace()
    
    # Generate indexes
    files_csv, dirs_csv, stats_csv = reindexer.generate_csv_indexes()
    json_index = reindexer.generate_json_index()
    sqlite_db = reindexer.generate_sqlite_index()
    report = reindexer.generate_report()
    
    print("\n" + "=" * 80)
    print("✅ REINDEXING COMPLETE")
    print("=" * 80)
    print(f"\n📄 Generated Files:")
    print(f"   - Files CSV: {files_csv.name}")
    print(f"   - Directories CSV: {dirs_csv.name}")
    print(f"   - Statistics CSV: {stats_csv.name}")
    print(f"   - JSON Index: {json_index.name}")
    print(f"   - SQLite Database: {sqlite_db.name}")
    print(f"   - Markdown Report: {report.name}")
    print(f"\n💡 Use the SQLite database for fast queries:")
    print(f"   sqlite3 {sqlite_db.name} \"SELECT * FROM files WHERE extension='.py'\"")
    print()

if __name__ == "__main__":
    main()

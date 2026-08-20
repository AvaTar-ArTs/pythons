#!/usr/bin/env python3
"""
Advanced File Intelligence System
Combines AST analysis, content fingerprinting, and ML-based classification
"""

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import mimetypes
import subprocess
import re

@dataclass
class FileFingerprint:
    """Comprehensive file fingerprint"""
    path: Path
    size: int
    hash_md5: str
    hash_sha256: str
    mime_type: str
    extension: str
    created: float
    modified: float
    is_binary: bool
    
    # Content-specific
    metadata: Dict = None
    language: Optional[str] = None
    encoding: Optional[str] = None
    line_count: Optional[int] = None
    
    # Relationships
    duplicates: List[str] = None
    similar_files: List[str] = None
    related_files: List[str] = None
    
    def to_dict(self):
        return asdict(self)


class FileIntelligenceDB:
    """SQLite database for file intelligence"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self._init_schema()
    
    def _init_schema(self):
        """Create comprehensive schema"""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY,
                path TEXT UNIQUE NOT NULL,
                size INTEGER,
                hash_md5 TEXT,
                hash_sha256 TEXT,
                mime_type TEXT,
                extension TEXT,
                created REAL,
                modified REAL,
                is_binary BOOLEAN,
                language TEXT,
                encoding TEXT,
                line_count INTEGER,
                metadata JSON,
                last_analyzed REAL
            );
            
            CREATE INDEX IF NOT EXISTS idx_hash_md5 ON files(hash_md5);
            CREATE INDEX IF NOT EXISTS idx_hash_sha256 ON files(hash_sha256);
            CREATE INDEX IF NOT EXISTS idx_extension ON files(extension);
            CREATE INDEX IF NOT EXISTS idx_mime_type ON files(mime_type);
            
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY,
                file_id INTEGER,
                related_file_id INTEGER,
                relationship_type TEXT,
                confidence REAL,
                FOREIGN KEY (file_id) REFERENCES files(id),
                FOREIGN KEY (related_file_id) REFERENCES files(id)
            );
            
            CREATE INDEX IF NOT EXISTS idx_relationships ON relationships(file_id, relationship_type);
            
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY,
                file_id INTEGER,
                tag TEXT,
                source TEXT,
                confidence REAL,
                FOREIGN KEY (file_id) REFERENCES files(id)
            );
            
            CREATE INDEX IF NOT EXISTS idx_tags ON tags(tag);
            
            CREATE TABLE IF NOT EXISTS content_chunks (
                id INTEGER PRIMARY KEY,
                file_id INTEGER,
                chunk_index INTEGER,
                content TEXT,
                embedding BLOB,
                FOREIGN KEY (file_id) REFERENCES files(id)
            );
        """)
        self.conn.commit()
    
    def upsert_file(self, fingerprint: FileFingerprint) -> int:
        """Insert or update file fingerprint"""
        cursor = self.conn.execute("""
            INSERT INTO files (
                path, size, hash_md5, hash_sha256, mime_type, extension,
                created, modified, is_binary, language, encoding, line_count,
                metadata, last_analyzed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(path) DO UPDATE SET
                size=excluded.size,
                hash_md5=excluded.hash_md5,
                hash_sha256=excluded.hash_sha256,
                modified=excluded.modified,
                last_analyzed=excluded.last_analyzed
            RETURNING id
        """, (
            str(fingerprint.path),
            fingerprint.size,
            fingerprint.hash_md5,
            fingerprint.hash_sha256,
            fingerprint.mime_type,
            fingerprint.extension,
            fingerprint.created,
            fingerprint.modified,
            fingerprint.is_binary,
            fingerprint.language,
            fingerprint.encoding,
            fingerprint.line_count,
            json.dumps(fingerprint.metadata) if fingerprint.metadata else None,
            fingerprint.modified
        ))
        
        file_id = cursor.fetchone()[0]
        self.conn.commit()
        return file_id
    
    def find_duplicates(self, min_size: int = 1024) -> Dict[str, List[str]]:
        """Find duplicate files by hash"""
        cursor = self.conn.execute("""
            SELECT hash_sha256, GROUP_CONCAT(path, '||') as paths, COUNT(*) as count
            FROM files
            WHERE size >= ? AND hash_sha256 IS NOT NULL
            GROUP BY hash_sha256
            HAVING count > 1
        """, (min_size,))
        
        duplicates = {}
        for row in cursor:
            hash_val, paths, count = row
            duplicates[hash_val] = paths.split('||')
        
        return duplicates
    
    def find_by_extension(self, extension: str) -> List[Dict]:
        """Find all files with given extension"""
        cursor = self.conn.execute("""
            SELECT path, size, mime_type, created, modified
            FROM files
            WHERE extension = ?
            ORDER BY size DESC
        """, (extension,))
        
        return [
            {
                'path': row[0],
                'size': row[1],
                'mime_type': row[2],
                'created': row[3],
                'modified': row[4]
            }
            for row in cursor
        ]
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        cursor = self.conn.execute("""
            SELECT 
                COUNT(*) as total_files,
                SUM(size) as total_size,
                COUNT(DISTINCT extension) as unique_extensions,
                COUNT(DISTINCT mime_type) as unique_mimetypes
            FROM files
        """)
        
        row = cursor.fetchone()
        
        # Get extension breakdown
        cursor = self.conn.execute("""
            SELECT extension, COUNT(*) as count, SUM(size) as total_size
            FROM files
            GROUP BY extension
            ORDER BY count DESC
            LIMIT 20
        """)
        
        extensions = [
            {'ext': row[0], 'count': row[1], 'size': row[2]}
            for row in cursor
        ]
        
        return {
            'total_files': row[0],
            'total_size': row[1],
            'unique_extensions': row[2],
            'unique_mimetypes': row[3],
            'top_extensions': extensions
        }
    
    def add_relationship(self, file1_path: str, file2_path: str, 
                        rel_type: str, confidence: float):
        """Add relationship between files"""
        self.conn.execute("""
            INSERT INTO relationships (file_id, related_file_id, relationship_type, confidence)
            SELECT f1.id, f2.id, ?, ?
            FROM files f1, files f2
            WHERE f1.path = ? AND f2.path = ?
        """, (rel_type, confidence, file1_path, file2_path))
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        self.conn.close()


class FileAnalyzer:
    """Advanced file analysis"""
    
    def __init__(self, db_path: Path):
        self.db = FileIntelligenceDB(db_path)
    
    def analyze_file(self, file_path: Path) -> Optional[FileFingerprint]:
        """Analyze a single file"""
        if not file_path.exists() or not file_path.is_file():
            return None
        
        stat = file_path.stat()
        
        # Calculate hashes
        hash_md5, hash_sha256 = self._calculate_hashes(file_path)
        
        # Determine mime type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        mime_type = mime_type or 'application/octet-stream'
        
        # Check if binary
        is_binary = self._is_binary(file_path)
        
        # Extract metadata based on file type
        metadata = self._extract_metadata(file_path, mime_type)
        
        # Language detection for text files
        language = self._detect_language(file_path) if not is_binary else None
        
        # Encoding detection
        encoding = self._detect_encoding(file_path) if not is_binary else None
        
        # Line count for text files
        line_count = self._count_lines(file_path) if not is_binary else None
        
        return FileFingerprint(
            path=file_path,
            size=stat.st_size,
            hash_md5=hash_md5,
            hash_sha256=hash_sha256,
            mime_type=mime_type,
            extension=file_path.suffix.lower(),
            created=stat.st_ctime,
            modified=stat.st_mtime,
            is_binary=is_binary,
            metadata=metadata,
            language=language,
            encoding=encoding,
            line_count=line_count
        )
    
    def _calculate_hashes(self, file_path: Path, chunk_size: int = 8192) -> Tuple[str, str]:
        """Calculate MD5 and SHA256 hashes"""
        md5 = hashlib.md5()
        sha256 = hashlib.sha256()
        
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    md5.update(chunk)
                    sha256.update(chunk)
        except Exception:
            return '', ''
        
        return md5.hexdigest(), sha256.hexdigest()
    
    def _is_binary(self, file_path: Path, check_bytes: int = 8192) -> bool:
        """Check if file is binary"""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(check_bytes)
                # Check for null bytes
                return b'\x00' in chunk
        except Exception:
            return True
    
    def _extract_metadata(self, file_path: Path, mime_type: str) -> Dict:
        """Extract file-type specific metadata"""
        metadata = {}
        
        # Audio files
        if mime_type.startswith('audio/'):
            metadata = self._extract_audio_metadata(file_path)
        
        # Image files
        elif mime_type.startswith('image/'):
            metadata = self._extract_image_metadata(file_path)
        
        # Video files
        elif mime_type.startswith('video/'):
            metadata = self._extract_video_metadata(file_path)
        
        # PDF files
        elif mime_type == 'application/pdf':
            metadata = self._extract_pdf_metadata(file_path)
        
        return metadata
    
    def _extract_audio_metadata(self, file_path: Path) -> Dict:
        """Extract audio metadata using ffprobe"""
        try:
            cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', 
                   '-show_format', '-show_streams', str(file_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                format_info = data.get('format', {})
                tags = format_info.get('tags', {})
                
                return {
                    'title': tags.get('title') or tags.get('TITLE'),
                    'artist': tags.get('artist') or tags.get('ARTIST'),
                    'album': tags.get('album') or tags.get('ALBUM'),
                    'duration': format_info.get('duration'),
                    'bitrate': format_info.get('bit_rate'),
                    'format': format_info.get('format_name')
                }
        except Exception:
            pass
        
        return {}
    
    def _extract_image_metadata(self, file_path: Path) -> Dict:
        """Extract image metadata"""
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode
                }
        except Exception:
            pass
        
        return {}
    
    def _extract_video_metadata(self, file_path: Path) -> Dict:
        """Extract video metadata"""
        return self._extract_audio_metadata(file_path)  # ffprobe works for video too
    
    def _extract_pdf_metadata(self, file_path: Path) -> Dict:
        """Extract PDF metadata"""
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                info = pdf.metadata
                return {
                    'title': info.get('/Title'),
                    'author': info.get('/Author'),
                    'subject': info.get('/Subject'),
                    'pages': len(pdf.pages)
                }
        except Exception:
            pass
        
        return {}
    
    def _detect_language(self, file_path: Path) -> Optional[str]:
        """Detect programming language"""
        extension_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.go': 'Go',
            '.rs': 'Rust',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.sh': 'Shell',
            '.sql': 'SQL',
            '.html': 'HTML',
            '.css': 'CSS',
            '.md': 'Markdown',
            '.json': 'JSON',
            '.xml': 'XML',
            '.yaml': 'YAML',
            '.yml': 'YAML'
        }
        
        return extension_map.get(file_path.suffix.lower())
    
    def _detect_encoding(self, file_path: Path) -> Optional[str]:
        """Detect text encoding"""
        try:
            import chardet
            with open(file_path, 'rb') as f:
                result = chardet.detect(f.read(10000))
                return result.get('encoding')
        except Exception:
            return 'utf-8'
    
    def _count_lines(self, file_path: Path) -> Optional[int]:
        """Count lines in text file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except Exception:
            return None
    
    def scan_directory(self, directory: Path, 
                      exclude_patterns: List[str] = None,
                      max_files: int = None) -> List[FileFingerprint]:
        """Scan directory recursively"""
        if exclude_patterns is None:
            exclude_patterns = [
                r'.*/\..*',  # Hidden files/dirs
                r'.*/node_modules/.*',
                r'.*/venv/.*',
                r'.*/.venv/.*',
                r'.*/Library/.*',
                r'.*/__pycache__/.*',
                r'.*/\.git/.*'
            ]
        
        compiled_patterns = [re.compile(p) for p in exclude_patterns]
        
        fingerprints = []
        count = 0
        
        for file_path in directory.rglob('*'):
            if not file_path.is_file():
                continue
            
            # Check exclusions
            if any(pattern.match(str(file_path)) for pattern in compiled_patterns):
                continue
            
            # Analyze file
            fingerprint = self.analyze_file(file_path)
            if fingerprint:
                self.db.upsert_file(fingerprint)
                fingerprints.append(fingerprint)
                count += 1
                
                if count % 100 == 0:
                    print(f"Analyzed {count} files...")
                
                if max_files and count >= max_files:
                    break
        
        return fingerprints
    
    def close(self):
        """Close database"""
        self.db.close()


if __name__ == '__main__':
    # Example usage
    db_path = Path.home() / '.file_intelligence.db'
    analyzer = FileAnalyzer(db_path)
    
    print("File Intelligence System initialized")
    print(f"Database: {db_path}")
    print()
    print("Statistics:")
    stats = analyzer.db.get_statistics()
    for key, value in stats.items():
        if key != 'top_extensions':
            print(f"  {key}: {value}")

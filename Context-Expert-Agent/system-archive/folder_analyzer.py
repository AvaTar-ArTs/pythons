#!/usr/bin/env python3
"""
Folder Analyzer - Deep folder structure analysis with depth tracking
"""

import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass
from collections import defaultdict
import mimetypes

@dataclass
class FileInfo:
    """Detailed file information."""
    path: str
    name: str
    extension: str
    size: int
    modified_time: datetime
    mime_type: str
    content_hash: str
    depth: int
    is_duplicate: bool = False
    duplicate_group: Optional[int] = None
    category: str = "unknown"
    priority: int = 0

class FolderAnalyzer:
    """Analyzes folder structures with depth tracking and intelligent categorization."""
    
    def __init__(self, root_dir: str, max_depth: int = 6):
        self.root_dir = Path(root_dir).resolve()
        self.max_depth = max_depth
        self.files: List[FileInfo] = []
        self.duplicate_groups: Dict[str, List[FileInfo]] = defaultdict(list)
        self.category_mapping = self._create_category_mapping()
        
    def _create_category_mapping(self) -> Dict[str, str]:
        """Create intelligent mapping of file extensions to categories."""
        return {
            # Programming Languages
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'jsx': 'react',
            'tsx': 'react',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c',
            'h': 'c',
            'hpp': 'cpp',
            'cs': 'csharp',
            'php': 'php',
            'rb': 'ruby',
            'go': 'go',
            'rs': 'rust',
            'swift': 'swift',
            'kt': 'kotlin',
            'scala': 'scala',
            'r': 'r',
            'm': 'objective-c',
            'mm': 'objective-cpp',
            
            # Web Technologies
            'html': 'html',
            'htm': 'html',
            'css': 'css',
            'scss': 'scss',
            'sass': 'sass',
            'less': 'less',
            'vue': 'vue',
            'svelte': 'svelte',
            
            # Data Formats
            'json': 'json',
            'xml': 'xml',
            'yaml': 'yaml',
            'yml': 'yaml',
            'toml': 'toml',
            'ini': 'config',
            'conf': 'config',
            'cfg': 'config',
            'env': 'config',
            'properties': 'config',
            
            # Documents
            'md': 'markdown',
            'rst': 'documentation',
            'txt': 'text',
            'rtf': 'text',
            'doc': 'documents',
            'docx': 'documents',
            'pdf': 'documents',
            'odt': 'documents',
            'pages': 'documents',
            
            # Spreadsheets
            'csv': 'csv',
            'xlsx': 'excel',
            'xls': 'excel',
            'ods': 'excel',
            'numbers': 'excel',
            
            # Images
            'jpg': 'images',
            'jpeg': 'images',
            'png': 'images',
            'gif': 'images',
            'svg': 'images',
            'webp': 'images',
            'bmp': 'images',
            'tiff': 'images',
            'ico': 'images',
            'psd': 'images',
            'ai': 'images',
            'sketch': 'images',
            
            # Audio
            'mp3': 'audio',
            'wav': 'audio',
            'flac': 'audio',
            'aac': 'audio',
            'ogg': 'audio',
            'm4a': 'audio',
            'wma': 'audio',
            
            # Video
            'mp4': 'video',
            'avi': 'video',
            'mov': 'video',
            'wmv': 'video',
            'flv': 'video',
            'webm': 'video',
            'mkv': 'video',
            'm4v': 'video',
            
            # Archives
            'zip': 'archives',
            'rar': 'archives',
            '7z': 'archives',
            'tar': 'archives',
            'gz': 'archives',
            'bz2': 'archives',
            'xz': 'archives',
            
            # Fonts
            'ttf': 'fonts',
            'otf': 'fonts',
            'woff': 'fonts',
            'woff2': 'fonts',
            'eot': 'fonts',
            
            # Database
            'sql': 'sql',
            'db': 'database',
            'sqlite': 'database',
            'sqlite3': 'database',
            
            # Logs
            'log': 'logs',
            'out': 'logs',
            'err': 'logs',
            
            # Temporary
            'tmp': 'temp',
            'temp': 'temp',
            'bak': 'backup',
            'backup': 'backup',
            'old': 'backup',
            
            # Executables
            'exe': 'executable',
            'app': 'executable',
            'dmg': 'executable',
            'pkg': 'executable',
            'deb': 'executable',
            'rpm': 'executable',
        }
    
    def analyze(self) -> Dict:
        """Perform comprehensive folder analysis."""
        print("🔍 Analyzing folder structure...")
        
        structure = {
            'total_files': 0,
            'total_directories': 0,
            'file_types': defaultdict(int),
            'categories': defaultdict(int),
            'size_by_category': defaultdict(int),
            'depth_distribution': defaultdict(int),
            'largest_files': [],
            'oldest_files': [],
            'newest_files': [],
            'duplicate_groups': {},
            'max_depth': 0,
            'directory_structure': {},
            'file_size_distribution': defaultdict(int),
            'extension_frequency': defaultdict(int)
        }
        
        file_count = 0
        processed_dirs = 0
        
        for root, dirs, files in os.walk(self.root_dir):
            # Calculate current depth
            depth = len(Path(root).relative_to(self.root_dir).parts)
            
            # Skip if exceeding max depth
            if depth >= self.max_depth:
                dirs[:] = []  # Don't go deeper
                continue
            
            structure['total_directories'] += 1
            structure['depth_distribution'][depth] += 1
            structure['max_depth'] = max(structure['max_depth'], depth)
            processed_dirs += 1
            
            # Track directory structure
            rel_path = Path(root).relative_to(self.root_dir)
            structure['directory_structure'][str(rel_path)] = {
                'file_count': len(files),
                'depth': depth,
                'files': files[:10]  # Store first 10 files as sample
            }
            
            for file in files:
                file_path = Path(root) / file
                try:
                    if file_path.is_file():
                        file_info = self._analyze_file(file_path, depth)
                        if file_info:
                            self.files.append(file_info)
                            structure['total_files'] += 1
                            
                            # Update statistics
                            ext = file_info.extension.lower()
                            structure['file_types'][ext] += 1
                            structure['categories'][file_info.category] += 1
                            structure['size_by_category'][file_info.category] += file_info.size
                            structure['extension_frequency'][ext] += 1
                            
                            # Track file size distribution
                            size_mb = file_info.size / (1024 * 1024)
                            if size_mb < 1:
                                structure['file_size_distribution']['<1MB'] += 1
                            elif size_mb < 10:
                                structure['file_size_distribution']['1-10MB'] += 1
                            elif size_mb < 100:
                                structure['file_size_distribution']['10-100MB'] += 1
                            else:
                                structure['file_size_distribution']['>100MB'] += 1
                            
                            # Track largest files
                            structure['largest_files'].append((str(file_path), file_info.size))
                            structure['oldest_files'].append((str(file_path), file_info.modified_time))
                            structure['newest_files'].append((str(file_path), file_info.modified_time))
                            
                            file_count += 1
                            if file_count % 1000 == 0:
                                print(f"   Processed {file_count:,} files...")
                                
                except (OSError, PermissionError) as e:
                    continue
            
            if processed_dirs % 100 == 0:
                print(f"   Processed {processed_dirs:,} directories...")
        
        # Sort and limit lists
        structure['largest_files'] = sorted(structure['largest_files'], key=lambda x: x[1], reverse=True)[:100]
        structure['oldest_files'] = sorted(structure['oldest_files'], key=lambda x: x[1])[:100]
        structure['newest_files'] = sorted(structure['newest_files'], key=lambda x: x[1], reverse=True)[:100]
        
        # Detect duplicates
        print("🔍 Detecting duplicate files...")
        structure['duplicate_groups'] = self._detect_duplicates()
        
        print(f"   ✅ Analysis complete: {structure['total_files']:,} files in {structure['total_directories']:,} directories")
        
        return structure
    
    def _analyze_file(self, file_path: Path, depth: int) -> Optional[FileInfo]:
        """Analyze a single file and extract detailed information."""
        try:
            stat = file_path.stat()
            extension = file_path.suffix.lower().lstrip('.')
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(file_path))
            mime_type = mime_type or 'unknown'
            
            # Calculate content hash for duplicate detection (only for smaller files)
            content_hash = ""
            if stat.st_size < 50 * 1024 * 1024:  # Only hash files < 50MB
                try:
                    with open(file_path, 'rb') as f:
                        content_hash = hashlib.md5(f.read()).hexdigest()
                except (OSError, PermissionError):
                    pass
            
            # Determine category
            category = self.category_mapping.get(extension, 'unknown')
            
            # Determine priority based on file type and size
            priority = self._calculate_priority(extension, stat.st_size, category)
            
            return FileInfo(
                path=str(file_path),
                name=file_path.name,
                extension=extension,
                size=stat.st_size,
                modified_time=datetime.fromtimestamp(stat.st_mtime),
                mime_type=mime_type,
                content_hash=content_hash,
                depth=depth,
                category=category,
                priority=priority
            )
        except (OSError, PermissionError):
            return None
    
    def _calculate_priority(self, extension: str, size: int, category: str) -> int:
        """Calculate file priority for organization."""
        priority = 0
        
        # High priority for code files
        if category in ['python', 'javascript', 'typescript', 'html', 'css']:
            priority += 100
        
        # Medium priority for config files
        elif category in ['config', 'json', 'yaml']:
            priority += 50
        
        # Lower priority for large files
        size_mb = size / (1024 * 1024)
        if size_mb > 100:
            priority -= 50
        elif size_mb > 10:
            priority -= 20
        
        # Lower priority for temporary files
        if category in ['temp', 'backup', 'logs']:
            priority -= 30
        
        return max(priority, 0)
    
    def _detect_duplicates(self) -> Dict[str, List[str]]:
        """Detect duplicate files based on content hash."""
        hash_groups = defaultdict(list)
        
        for file_info in self.files:
            if file_info.content_hash:
                hash_groups[file_info.content_hash].append(file_info.path)
        
        # Return only groups with duplicates
        duplicates = {}
        for content_hash, file_paths in hash_groups.items():
            if len(file_paths) > 1:
                duplicates[content_hash] = file_paths
        
        return duplicates
    
    def get_files_by_category(self, category: str) -> List[FileInfo]:
        """Get all files in a specific category."""
        return [f for f in self.files if f.category == category]
    
    def get_files_by_depth(self, depth: int) -> List[FileInfo]:
        """Get all files at a specific depth."""
        return [f for f in self.files if f.depth == depth]
    
    def get_largest_files(self, limit: int = 10) -> List[FileInfo]:
        """Get the largest files."""
        return sorted(self.files, key=lambda x: x.size, reverse=True)[:limit]
    
    def get_oldest_files(self, limit: int = 10) -> List[FileInfo]:
        """Get the oldest files."""
        return sorted(self.files, key=lambda x: x.modified_time)[:limit]
    
    def get_newest_files(self, limit: int = 10) -> List[FileInfo]:
        """Get the newest files."""
        return sorted(self.files, key=lambda x: x.modified_time, reverse=True)[:limit]
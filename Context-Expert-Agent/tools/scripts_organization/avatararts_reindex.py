#!/usr/bin/env python3
"""
AVATARARTS Intelligent Reindexing System
=========================================

A lightweight, efficient workspace indexing and search system that:
- Indexes all files in your workspace (code, docs, data, content)
- Creates searchable metadata database
- Enables fast content search without heavy vector libraries
- Supports semantic tagging and categorization
- Provides instant file discovery

Version: 2.0.0
Date: 2026-01-02
"""

import os
import sys
import json
import sqlite3
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict, Counter
import re


class Colors:
    """Terminal colors"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class WorkspaceIndexer:
    """Intelligent workspace indexing system"""

    def __init__(self, workspace_root: Path, db_path: Path = None):
        self.workspace_root = workspace_root
        self.db_path = db_path or (workspace_root / 'UTILITIES_TOOLS' / 'workspace_index.db')
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Directories to skip
        self.skip_dirs = {
            '.git', '.github', '.history', '__pycache__',
            'node_modules', '.DS_Store', '.venv', 'venv',
            'ARCHIVES_BACKUPS'  # Don't index archives
        }

        # File patterns to index
        self.indexable_extensions = {
            # Code
            '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c', '.h',
            '.go', '.rs', '.rb', '.php', '.sh', '.bash',
            # Documentation
            '.md', '.txt', '.rst', '.adoc',
            # Data
            '.json', '.yaml', '.yml', '.csv', '.xml',
            # Web
            '.html', '.css', '.scss', '.sass',
            # Config
            '.toml', '.ini', '.cfg', '.conf', '.env.example'
        }

        # Context keywords for smart categorization
        self.context_patterns = {
            'ai_ml': r'\b(ai|ml|machine learning|neural|model|train|predict|algorithm)\b',
            'automation': r'\b(automation|workflow|script|bot|schedule|cron)\b',
            'seo': r'\b(seo|keyword|ranking|search engine|optimization|backlink)\b',
            'web_dev': r'\b(react|vue|angular|frontend|backend|api|endpoint)\b',
            'database': r'\b(sql|database|query|schema|migration|orm)\b',
            'business': r'\b(business|client|customer|revenue|sales|marketing)\b',
            'content': r'\b(content|article|blog|post|video|image|media)\b'
        }

        self.init_database()

    def init_database(self):
        """Initialize SQLite database with optimized schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE NOT NULL,
                relative_path TEXT NOT NULL,
                file_name TEXT NOT NULL,
                file_ext TEXT,
                file_size INTEGER,
                file_hash TEXT,
                mime_type TEXT,
                category TEXT,
                project_context TEXT,
                last_modified TIMESTAMP,
                indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                content_preview TEXT,
                line_count INTEGER,
                word_count INTEGER
            )
        ''')

        # Keywords/tags table for search
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id INTEGER,
                keyword TEXT NOT NULL,
                frequency INTEGER DEFAULT 1,
                FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
            )
        ''')

        # Create indexes for fast search
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_file_path ON files(file_path)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_file_ext ON files(file_ext)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON files(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_keyword ON keywords(keyword)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_relative_path ON files(relative_path)')

        # Index statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS index_metadata (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def categorize_file(self, filepath: Path, content_preview: str) -> Tuple[str, str]:
        """Categorize file based on location and content"""
        relative = filepath.relative_to(self.workspace_root)
        path_str = str(relative).lower()
        content_lower = content_preview.lower()

        # Check directory-based categorization
        if 'ai_tools' in path_str or 'ai-' in path_str:
            category = 'AI/ML'
        elif 'business' in path_str or 'client' in path_str:
            category = 'Business'
        elif 'seo' in path_str or 'marketing' in path_str:
            category = 'Marketing/SEO'
        elif 'data' in path_str or 'analytics' in path_str:
            category = 'Data/Analytics'
        elif 'content' in path_str or 'assets' in path_str:
            category = 'Content/Assets'
        elif 'utilities' in path_str or 'tools' in path_str or 'scripts' in path_str:
            category = 'Utilities/Tools'
        elif 'docs' in path_str or 'documentation' in path_str:
            category = 'Documentation'
        else:
            category = 'Other'

        # Detect project context from content
        context_scores = {}
        for context_name, pattern in self.context_patterns.items():
            matches = len(re.findall(pattern, content_lower, re.IGNORECASE))
            if matches > 0:
                context_scores[context_name] = matches

        project_context = max(context_scores, key=context_scores.get) if context_scores else 'general'

        return category, project_context

    def extract_keywords(self, content: str, max_keywords: int = 20) -> List[Tuple[str, int]]:
        """Extract important keywords from content"""
        # Common stop words to skip
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
            'those', 'it', 'its', 'if', 'then', 'else', 'when', 'where', 'what',
            'which', 'who', 'how', 'not', 'no', 'yes'
        }

        # Extract words (alphanumeric, 3+ chars)
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]{2,}\b', content.lower())

        # Count frequencies
        word_freq = Counter(w for w in words if w not in stop_words)

        # Return top keywords
        return word_freq.most_common(max_keywords)

    def index_file(self, filepath: Path) -> Optional[Dict]:
        """Index a single file"""
        try:
            # Get file stats
            stat = filepath.stat()
            file_size = stat.st_size
            last_modified = datetime.fromtimestamp(stat.st_mtime)

            # Skip very large files (>10MB)
            if file_size > 10 * 1024 * 1024:
                return None

            # Read file content (first 50KB for preview)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(50000)
                    lines = content.split('\n')
                    line_count = len(lines)
                    word_count = len(content.split())
                    content_preview = content[:500]  # First 500 chars
            except:
                # Binary file or unreadable
                content_preview = ""
                line_count = 0
                word_count = 0

            # Calculate file hash
            file_hash = hashlib.md5(filepath.read_bytes()).hexdigest()

            # Get mime type
            mime_type, _ = mimetypes.guess_type(str(filepath))

            # Categorize
            category, project_context = self.categorize_file(filepath, content_preview)

            # Extract keywords
            keywords = self.extract_keywords(content_preview)

            return {
                'file_path': str(filepath.absolute()),
                'relative_path': str(filepath.relative_to(self.workspace_root)),
                'file_name': filepath.name,
                'file_ext': filepath.suffix.lower(),
                'file_size': file_size,
                'file_hash': file_hash,
                'mime_type': mime_type or 'unknown',
                'category': category,
                'project_context': project_context,
                'last_modified': last_modified,
                'content_preview': content_preview,
                'line_count': line_count,
                'word_count': word_count,
                'keywords': keywords
            }
        except Exception as e:
            print(f"Error indexing {filepath}: {e}")
            return None

    def reindex(self, verbose: bool = True):
        """Reindex entire workspace"""
        if verbose:
            print(f"{Colors.HEADER}{'='*70}{Colors.ENDC}")
            print(f"{Colors.BOLD}AVATARARTS Workspace Reindexing{Colors.ENDC}")
            print(f"{Colors.HEADER}{'='*70}{Colors.ENDC}\n")
            print(f"Workspace: {self.workspace_root}")
            print(f"Database: {self.db_path}\n")

        # Clear existing index
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM files')
        cursor.execute('DELETE FROM keywords')
        conn.commit()

        # Stats
        stats = {
            'total_files': 0,
            'indexed_files': 0,
            'skipped_files': 0,
            'categories': defaultdict(int),
            'extensions': defaultdict(int),
            'total_size': 0
        }

        # Find all indexable files
        if verbose:
            print(f"{Colors.CYAN}🔍 Scanning workspace...{Colors.ENDC}\n")

        for root, dirs, files in os.walk(self.workspace_root):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.skip_dirs and not d.startswith('.')]

            for filename in files:
                filepath = Path(root) / filename

                # Skip hidden files
                if filename.startswith('.'):
                    continue

                stats['total_files'] += 1

                # Check if file should be indexed
                if filepath.suffix.lower() not in self.indexable_extensions:
                    stats['skipped_files'] += 1
                    continue

                # Index file
                file_data = self.index_file(filepath)
                if file_data:
                    # Insert file record
                    cursor.execute('''
                        INSERT INTO files (
                            file_path, relative_path, file_name, file_ext,
                            file_size, file_hash, mime_type, category,
                            project_context, last_modified, content_preview,
                            line_count, word_count
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        file_data['file_path'], file_data['relative_path'],
                        file_data['file_name'], file_data['file_ext'],
                        file_data['file_size'], file_data['file_hash'],
                        file_data['mime_type'], file_data['category'],
                        file_data['project_context'], file_data['last_modified'],
                        file_data['content_preview'], file_data['line_count'],
                        file_data['word_count']
                    ))

                    file_id = cursor.lastrowid

                    # Insert keywords
                    for keyword, freq in file_data['keywords']:
                        cursor.execute('''
                            INSERT INTO keywords (file_id, keyword, frequency)
                            VALUES (?, ?, ?)
                        ''', (file_id, keyword, freq))

                    # Update stats
                    stats['indexed_files'] += 1
                    stats['categories'][file_data['category']] += 1
                    stats['extensions'][file_data['file_ext']] += 1
                    stats['total_size'] += file_data['file_size']

                    if verbose and stats['indexed_files'] % 100 == 0:
                        print(f"   Indexed {stats['indexed_files']} files...", end='\r')

        # Save metadata
        cursor.execute('''
            INSERT OR REPLACE INTO index_metadata (key, value, updated_at)
            VALUES ('last_reindex', ?, CURRENT_TIMESTAMP)
        ''', (datetime.now().isoformat(),))

        cursor.execute('''
            INSERT OR REPLACE INTO index_metadata (key, value, updated_at)
            VALUES ('total_indexed', ?, CURRENT_TIMESTAMP)
        ''', (str(stats['indexed_files']),))

        conn.commit()
        conn.close()

        # Print results
        if verbose:
            print(f"\n{Colors.GREEN}✓ Reindexing complete!{Colors.ENDC}\n")
            self._print_stats(stats)

        return stats

    def _print_stats(self, stats: Dict):
        """Print indexing statistics"""
        print(f"{Colors.CYAN}📊 Indexing Statistics{Colors.ENDC}")
        print(f"   Total files scanned: {Colors.BOLD}{stats['total_files']:,}{Colors.ENDC}")
        print(f"   Files indexed: {Colors.BOLD}{Colors.GREEN}{stats['indexed_files']:,}{Colors.ENDC}")
        print(f"   Files skipped: {stats['skipped_files']:,}")
        print(f"   Total indexed size: {self._format_size(stats['total_size'])}\n")

        print(f"{Colors.CYAN}📁 Categories{Colors.ENDC}")
        for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
            print(f"   {category:25s} {count:>6,} files")

        print(f"\n{Colors.CYAN}📝 File Types (Top 10){Colors.ENDC}")
        sorted_exts = sorted(stats['extensions'].items(), key=lambda x: x[1], reverse=True)[:10]
        for ext, count in sorted_exts:
            ext_display = ext if ext else '[no extension]'
            print(f"   {ext_display:15s} {count:>6,} files")

    def _format_size(self, size_bytes: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def search(self, query: str, limit: int = 20) -> List[Dict]:
        """Search indexed files"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Search in keywords, file names, and paths
        results = cursor.execute('''
            SELECT DISTINCT f.relative_path, f.file_name, f.category,
                   f.project_context, f.file_size, f.last_modified,
                   f.content_preview
            FROM files f
            LEFT JOIN keywords k ON f.id = k.file_id
            WHERE k.keyword LIKE ?
               OR f.file_name LIKE ?
               OR f.relative_path LIKE ?
               OR f.content_preview LIKE ?
            ORDER BY f.last_modified DESC
            LIMIT ?
        ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', limit)).fetchall()

        conn.close()

        return [
            {
                'path': r[0],
                'name': r[1],
                'category': r[2],
                'context': r[3],
                'size': self._format_size(r[4]),
                'modified': r[5],
                'preview': r[6][:200] if r[6] else ''
            }
            for r in results
        ]

    def get_stats(self) -> Dict:
        """Get index statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        total_files = cursor.execute('SELECT COUNT(*) FROM files').fetchone()[0]
        total_keywords = cursor.execute('SELECT COUNT(DISTINCT keyword) FROM keywords').fetchone()[0]
        last_reindex = cursor.execute(
            'SELECT value FROM index_metadata WHERE key = "last_reindex"'
        ).fetchone()

        categories = cursor.execute('''
            SELECT category, COUNT(*) FROM files GROUP BY category ORDER BY COUNT(*) DESC
        ''').fetchall()

        conn.close()

        return {
            'total_files': total_files,
            'total_keywords': total_keywords,
            'last_reindex': last_reindex[0] if last_reindex else 'Never',
            'categories': dict(categories)
        }


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description='AVATARARTS Workspace Reindexing System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s reindex           # Reindex entire workspace
  %(prog)s search "react"    # Search for files related to "react"
  %(prog)s stats             # Show index statistics
        """
    )

    parser.add_argument('command', choices=['reindex', 'search', 'stats'],
                       help='Command to execute')
    parser.add_argument('query', nargs='?', help='Search query (for search command)')
    parser.add_argument('--limit', type=int, default=20, help='Max search results')

    args = parser.parse_args()

    # Initialize indexer
    workspace = Path.cwd()
    indexer = WorkspaceIndexer(workspace)

    if args.command == 'reindex':
        indexer.reindex()

    elif args.command == 'search':
        if not args.query:
            print(f"{Colors.RED}Error: Search query required{Colors.ENDC}")
            sys.exit(1)

        print(f"{Colors.CYAN}🔍 Searching for: {Colors.BOLD}{args.query}{Colors.ENDC}\n")
        results = indexer.search(args.query, args.limit)

        if not results:
            print(f"{Colors.YELLOW}No results found{Colors.ENDC}")
        else:
            print(f"Found {len(results)} results:\n")
            for i, r in enumerate(results, 1):
                print(f"{Colors.BOLD}{i}. {r['name']}{Colors.ENDC}")
                print(f"   Path: {r['path']}")
                print(f"   Category: {r['category']} | Context: {r['context']}")
                print(f"   Size: {r['size']} | Modified: {r['modified']}")
                if r['preview']:
                    print(f"   Preview: {r['preview'][:100]}...")
                print()

    elif args.command == 'stats':
        stats = indexer.get_stats()
        print(f"{Colors.CYAN}📊 Index Statistics{Colors.ENDC}\n")
        print(f"   Total files indexed: {Colors.BOLD}{stats['total_files']:,}{Colors.ENDC}")
        print(f"   Unique keywords: {stats['total_keywords']:,}")
        print(f"   Last reindexed: {stats['last_reindex']}\n")
        print(f"{Colors.CYAN}Categories:{Colors.ENDC}")
        for cat, count in stats['categories'].items():
            print(f"   {cat:25s} {count:>6,} files")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Advanced Parent-Folder Content-Aware Organization
Analyzes files with full context awareness of parent folders, project structure,
and file relationships to make intelligent organization decisions.
"""

import sqlite3
import csv
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import re

class AdvancedParentFolderOrganizer:
    """Advanced organization with parent-folder content awareness."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Project detection patterns
        self.project_patterns = {
            'quantumforge-complete': {
                'type': 'active_project',
                'priority': 100,
                'should_stay': True,
                'file_patterns': ['.py', '.html', '.css', '.js', 'requirements.txt', 'package.json']
            },
            'retention-suite-complete': {
                'type': 'active_project',
                'priority': 95,
                'should_stay': True
            },
            'heavenlyhands-complete': {
                'type': 'active_project',
                'priority': 90,
                'should_stay': True
            },
            'josephrosadomd': {
                'type': 'website_project',
                'priority': 85,
                'should_stay': True,
                'note': 'WordPress website - keep structure intact'
            },
            'Dr_Adu_GainesvillePFS_SEO_Project': {
                'type': 'client_project',
                'priority': 80,
                'should_stay': True
            }
        }
        
        # Directory purpose detection
        self.directory_purposes = {
            'tools': 'python_utilities',
            'scripts': 'python_utilities',
            'html-assets': 'html_assets',
            'ai-sites': 'html_assets',
            'organized_intelligent': 'archive_content',
            'archive': 'archived_files',
            'analysis': 'data_analysis',
            'ai-ml-notes': 'documentation',
            'intelligencTtools': 'python_utilities'
        }
    
    def find_latest_index(self):
        """Find latest reindex database (preferring ultra-deep reindex)."""
        # First try ultra-deep reindex (unlimited depth)
        ultra_deep_files = sorted(
            self.workspace_root.glob("ULTRA_DEEP_REINDEX_*.db"),
            reverse=True
        )
        if ultra_deep_files:
            print(f"✅ Using ultra-deep reindex: {ultra_deep_files[0].name}")
            return ultra_deep_files[0]
        
        # Fall back to regular reindex
        db_files = sorted(
            self.workspace_root.glob("REINDEX_*.db"),
            reverse=True
        )
        if db_files:
            print(f"⚠️  Using regular reindex: {db_files[0].name}")
            return db_files[0]
        
        return None
    
    def analyze_parent_folder_context(self, db_path: Path):
        """Analyze parent folder context for intelligent decisions."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🧠 Advanced Parent-Folder Content Analysis")
        print("=" * 80)
        print()
        
        print("1️⃣  Analyzing directory purposes and contexts...")
        
        # Get directory analysis
        cursor.execute('''
            SELECT 
                parent_directory,
                COUNT(*) as file_count,
                ROUND(SUM(size_mb), 1) as total_mb,
                GROUP_CONCAT(DISTINCT file_type) as types,
                GROUP_CONCAT(DISTINCT extension) as extensions,
                AVG(depth) as avg_depth,
                MIN(modified) as oldest,
                MAX(modified) as newest
            FROM files
            WHERE parent_directory != '.'
            GROUP BY parent_directory
            ORDER BY file_count DESC
        ''')
        
        directory_analysis = {}
        for row in cursor.fetchall():
            parent_dir, file_count, total_mb, types, extensions, avg_depth, oldest, newest = row
            directory_analysis[parent_dir] = {
                'file_count': file_count,
                'total_mb': total_mb,
                'types': types.split(',') if types else [],
                'extensions': extensions.split(',') if extensions else [],
                'avg_depth': avg_depth,
                'oldest': oldest,
                'newest': newest,
                'purpose': self._detect_directory_purpose(parent_dir, types, file_count),
                'project': self._detect_project(parent_dir),
                'should_move': self._should_move_directory(parent_dir, file_count, total_mb)
            }
        
        print(f"   Analyzed {len(directory_analysis)} directories\n")
        
        # Analyze file relationships
        print("2️⃣  Analyzing file relationships and context...")
        
        # Group files by parent and analyze patterns
        cursor.execute('''
            SELECT 
                parent_directory,
                filename,
                file_type,
                extension,
                size_mb,
                path
            FROM files
            ORDER BY parent_directory, filename
        ''')
        
        file_relationships = defaultdict(list)
        for row in cursor.fetchall():
            parent_dir, filename, file_type, ext, size_mb, path = row
            file_relationships[parent_dir].append({
                'filename': filename,
                'file_type': file_type,
                'extension': ext,
                'size_mb': size_mb,
                'path': path
            })
        
        conn.close()
        
        print(f"   Analyzed file relationships in {len(file_relationships)} directories\n")
        
        return directory_analysis, file_relationships
    
    def _detect_directory_purpose(self, parent_dir: str, types: list, file_count: int) -> str:
        """Detect directory purpose from context."""
        parent_lower = parent_dir.lower()
        
        # Check known patterns
        for pattern, purpose in self.directory_purposes.items():
            if pattern in parent_lower:
                return purpose
        
        # Analyze by file types
        if types:
            if 'code_python' in types and file_count > 5:
                return 'python_utilities'
            if 'code_html' in types and file_count > 10:
                return 'html_assets'
            if 'data' in types or 'data_database' in types:
                return 'data_files'
            if 'document_markdown' in types:
                return 'documentation'
            if 'image' in types and file_count > 20:
                return 'image_assets'
        
        # Check for project indicators
        if any(proj in parent_dir for proj in ['complete', 'project', 'suite']):
            return 'active_project'
        
        if 'archive' in parent_lower or 'backup' in parent_lower:
            return 'archived_files'
        
        return 'general'
    
    def _detect_project(self, parent_dir: str) -> str:
        """Detect which project a directory belongs to."""
        for project, info in self.project_patterns.items():
            if project in parent_dir:
                return project
        return None
    
    def _should_move_directory(self, parent_dir: str, file_count: int, total_mb: float) -> bool:
        """Determine if directory should be moved."""
        # Don't move project directories
        if any(proj in parent_dir for proj in self.project_patterns.keys()):
            return False
        
        # Don't move if it's already in the right place
        if parent_dir.startswith(('projects/', 'tools/', 'assets/', 'docs/', 'data/')):
            return False
        
        # Move if it's a utility directory with Python files
        if 'tools' in parent_dir.lower() or 'scripts' in parent_dir.lower():
            return True
        
        # Move if it's HTML assets not in a project
        if 'html' in parent_dir.lower() and 'josephrosadomd' not in parent_dir:
            return True
        
        return False
    
    def generate_intelligent_moves(self, directory_analysis: dict, file_relationships: dict):
        """Generate intelligent file moves based on parent-folder context."""
        print("3️⃣  Generating intelligent organization moves...")
        
        moves = []
        
        # Analyze each directory
        for parent_dir, dir_info in directory_analysis.items():
            purpose = dir_info['purpose']
            project = dir_info['project']
            files = file_relationships.get(parent_dir, [])
            
            # Skip if it's a project directory (keep intact)
            if project or purpose == 'active_project':
                continue
            
            # Generate moves based on purpose
            if purpose == 'python_utilities':
                # Move Python files to tools/ with subcategorization
                for file_info in files:
                    if file_info['file_type'] == 'code_python':
                        new_path = self._determine_tools_location(
                            file_info['filename'],
                            file_info['path'],
                            parent_dir
                        )
                        moves.append({
                            'original_path': file_info['path'],
                            'new_path': new_path,
                            'category': 'python_script',
                            'parent_context': parent_dir,
                            'purpose': purpose,
                            'reason': f'Python utility from {parent_dir} - context-aware placement'
                        })
            
            elif purpose == 'html_assets':
                # Move HTML files to assets/html/ (unless in a project)
                for file_info in files:
                    if file_info['file_type'] == 'code_html':
                        # Check if it's part of a website project
                        if 'josephrosadomd' in file_info['path']:
                            continue  # Keep website files in place
                        
                        new_path = f"assets/html/{file_info['filename']}"
                        moves.append({
                            'original_path': file_info['path'],
                            'new_path': new_path,
                            'category': 'html_asset',
                            'parent_context': parent_dir,
                            'purpose': purpose,
                            'reason': f'HTML asset from {parent_dir} - consolidate to assets/html/'
                        })
            
            elif purpose == 'data_files':
                # Organize data files intelligently
                for file_info in files:
                    if file_info['file_type'] in ['data', 'data_database']:
                        new_path = self._determine_data_location(
                            file_info['filename'],
                            file_info['path'],
                            parent_dir
                        )
                        moves.append({
                            'original_path': file_info['path'],
                            'new_path': new_path,
                            'category': 'data_file',
                            'parent_context': parent_dir,
                            'purpose': purpose,
                            'reason': f'Data file from {parent_dir} - context-aware placement'
                        })
            
            elif purpose == 'documentation':
                # Organize documentation
                for file_info in files:
                    if file_info['file_type'] == 'document_markdown':
                        new_path = self._determine_docs_location(
                            file_info['filename'],
                            file_info['path'],
                            parent_dir
                        )
                        moves.append({
                            'original_path': file_info['path'],
                            'new_path': new_path,
                            'category': 'documentation',
                            'parent_context': parent_dir,
                            'purpose': purpose,
                            'reason': f'Documentation from {parent_dir} - context-aware placement'
                        })
        
        print(f"   Generated {len(moves)} intelligent moves\n")
        return moves
    
    def _determine_tools_location(self, filename: str, path: str, parent_dir: str) -> str:
        """Determine where Python script should go in tools/ based on context."""
        filename_lower = filename.lower()
        path_lower = path.lower()
        parent_lower = parent_dir.lower()
        
        # Check filename patterns
        if any(term in filename_lower for term in ['analyze', 'analysis', 'scan', 'inventory', 'report']):
            return f"tools/analysis/{filename}"
        
        if any(term in filename_lower for term in ['automate', 'automation', 'bot', 'scraper']):
            return f"tools/automation/{filename}"
        
        if any(term in filename_lower for term in ['util', 'utility', 'helper', 'helper']):
            return f"tools/utilities/{filename}"
        
        # Check parent directory context
        if 'analysis' in parent_lower or 'analyze' in parent_lower:
            return f"tools/analysis/{filename}"
        
        if 'automation' in parent_lower or 'automate' in parent_lower:
            return f"tools/automation/{filename}"
        
        if 'utility' in parent_lower or 'utilities' in parent_lower:
            return f"tools/utilities/{filename}"
        
        # Check path context
        if 'analysis' in path_lower:
            return f"tools/analysis/{filename}"
        if 'automation' in path_lower:
            return f"tools/automation/{filename}"
        
        # Default to tools root for main scripts
        return f"tools/{filename}"
    
    def _determine_data_location(self, filename: str, path: str, parent_dir: str) -> str:
        """Determine where data file should go based on context."""
        filename_lower = filename.lower()
        parent_lower = parent_dir.lower()
        
        # Reindex files go to index/
        if 'REINDEX' in filename or 'reindex' in filename_lower:
            return f"index/{filename}"
        
        # Analysis outputs
        if 'ANALYSIS' in filename or 'analysis' in filename_lower or 'analysis' in parent_lower:
            return f"data/analysis/{filename}"
        
        # Database files
        if filename.endswith('.db') or filename.endswith('.sqlite'):
            return f"data/databases/{filename}"
        
        # Exports
        if 'export' in filename_lower or 'export' in parent_lower:
            return f"data/exports/{filename}"
        
        # Old/archive data
        if 'archive' in parent_lower or 'backup' in parent_lower:
            return f"data/archives/{filename}"
        
        # Default to data root
        return f"data/{filename}"
    
    def _determine_docs_location(self, filename: str, path: str, parent_dir: str) -> str:
        """Determine where documentation should go."""
        filename_lower = filename.lower()
        parent_lower = parent_dir.lower()
        
        # API docs
        if 'api' in filename_lower or 'api' in parent_lower:
            return f"docs/api/{filename}"
        
        # Guides
        if any(term in filename_lower for term in ['guide', 'tutorial', 'howto', 'how-to']):
            return f"docs/guides/{filename}"
        
        # Reference
        if any(term in filename_lower for term in ['reference', 'ref', 'manual']):
            return f"docs/reference/{filename}"
        
        # Project-specific docs stay with project
        if any(proj in parent_dir for proj in self.project_patterns.keys()):
            return path  # Keep in project
        
        # Default to docs root
        return f"docs/{filename}"
    
    def generate_directory_moves(self, directory_analysis: dict):
        """Generate directory-level moves for entire directories."""
        print("4️⃣  Generating directory-level moves...")
        
        directory_moves = []
        
        # Identify directories that should be moved as units
        for parent_dir, dir_info in directory_analysis.items():
            purpose = dir_info['purpose']
            project = dir_info['project']
            
            # Skip project directories
            if project:
                continue
            
            # Move entire directories when appropriate
            if purpose == 'python_utilities' and dir_info['file_count'] < 50:
                # Small utility directories can move as units
                new_dir = self._determine_directory_location(parent_dir, purpose)
                if new_dir and new_dir != parent_dir:
                    directory_moves.append({
                        'original_directory': parent_dir,
                        'new_directory': new_dir,
                        'file_count': dir_info['file_count'],
                        'total_mb': dir_info['total_mb'],
                        'purpose': purpose,
                        'reason': f'Move {purpose} directory as unit'
                    })
        
        print(f"   Generated {len(directory_moves)} directory moves\n")
        return directory_moves
    
    def _determine_directory_location(self, parent_dir: str, purpose: str) -> str:
        """Determine where entire directory should move."""
        if purpose == 'python_utilities':
            # Check if it's analysis, automation, or utilities
            if 'analysis' in parent_dir.lower():
                return parent_dir.replace('tools/', 'tools/analysis/').replace('scripts/', 'tools/analysis/')
            elif 'automation' in parent_dir.lower():
                return parent_dir.replace('tools/', 'tools/automation/').replace('scripts/', 'tools/automation/')
            else:
                return parent_dir.replace('tools/', 'tools/utilities/').replace('scripts/', 'tools/utilities/')
        
        return None
    
    def generate_report(self, directory_analysis: dict, file_moves: list, directory_moves: list):
        """Generate comprehensive organization report."""
        report_file = self.workspace_root / f"ADVANCED_ORGANIZATION_PLAN_{self.timestamp}.md"
        
        print("📝 Generating advanced organization report...")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Advanced Parent-Folder Content-Aware Organization Plan\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Method:** Parent-folder content awareness with context analysis\n\n")
            f.write("---\n\n")
            
            # Directory analysis
            f.write("## 📊 Directory Context Analysis\n\n")
            f.write("### Directory Purposes Detected\n\n")
            
            purpose_summary = defaultdict(lambda: {'count': 0, 'files': 0, 'size_mb': 0})
            for parent_dir, dir_info in directory_analysis.items():
                purpose = dir_info['purpose']
                purpose_summary[purpose]['count'] += 1
                purpose_summary[purpose]['files'] += dir_info['file_count']
                purpose_summary[purpose]['size_mb'] += dir_info['total_mb']
            
            f.write("| Purpose | Directories | Files | Size (MB) |\n")
            f.write("|---------|-----------:|------:|----------:|\n")
            for purpose, stats in sorted(purpose_summary.items(), key=lambda x: x[1]['files'], reverse=True):
                f.write(f"| `{purpose}` | {stats['count']} | {stats['files']:,} | {stats['size_mb']:.1f} |\n")
            f.write("\n")
            
            # Project detection
            f.write("### Projects Detected\n\n")
            projects_found = {}
            for parent_dir, dir_info in directory_analysis.items():
                if dir_info['project']:
                    proj = dir_info['project']
                    if proj not in projects_found:
                        projects_found[proj] = {
                            'directories': [],
                            'file_count': 0,
                            'total_mb': 0
                        }
                    projects_found[proj]['directories'].append(parent_dir)
                    projects_found[proj]['file_count'] += dir_info['file_count']
                    projects_found[proj]['total_mb'] += dir_info['total_mb']
            
            f.write("| Project | Directories | Files | Size (MB) | Action |\n")
            f.write("|---------|-----------:|------:|----------:|--------|\n")
            for project, info in sorted(projects_found.items(), key=lambda x: x[1]['file_count'], reverse=True):
                action = "Keep in place (project structure)" if self.project_patterns.get(project, {}).get('should_stay') else "Review"
                f.write(f"| `{project}` | {len(info['directories'])} | {info['file_count']:,} | {info['total_mb']:.1f} | {action} |\n")
            f.write("\n")
            
            # File moves
            f.write("## 📦 Intelligent File Moves\n\n")
            f.write(f"**Total files to move:** {len(file_moves)}\n\n")
            
            # Group by category
            by_category = defaultdict(list)
            for move in file_moves:
                by_category[move['category']].append(move)
            
            for category, moves in by_category.items():
                f.write(f"### {category.replace('_', ' ').title()} ({len(moves)} files)\n\n")
                f.write("| Original Path | New Path | Parent Context | Reason |\n")
                f.write("|---------------|----------|---------------|--------|\n")
                for move in moves[:30]:
                    f.write(f"| `{move['original_path']}` | `{move['new_path']}` | `{move['parent_context']}` | {move['reason']} |\n")
                if len(moves) > 30:
                    f.write(f"| ... | ... | ... | ... ({len(moves) - 30} more) |\n")
                f.write("\n")
            
            # Directory moves
            if directory_moves:
                f.write("## 📁 Directory-Level Moves\n\n")
                f.write("| Original Directory | New Directory | Files | Size (MB) | Reason |\n")
                f.write("|-------------------|---------------|------:|----------:|--------|\n")
                for move in directory_moves:
                    f.write(f"| `{move['original_directory']}` | `{move['new_directory']}` | {move['file_count']} | {move['total_mb']:.1f} | {move['reason']} |\n")
                f.write("\n")
            
            # Recommendations
            f.write("## 🎯 Recommendations\n\n")
            f.write("### High Priority\n\n")
            f.write("1. **Respect Project Structure** - Keep project directories intact\n")
            f.write("2. **Context-Aware Placement** - Files moved based on parent folder context\n")
            f.write("3. **Preserve Relationships** - Related files kept together\n\n")
            
            f.write("### Implementation\n\n")
            f.write("1. Review the migration CSV\n")
            f.write("2. Verify project directories are preserved\n")
            f.write("3. Execute moves in phases\n")
            f.write("4. Test after each phase\n\n")
        
        print(f"   ✅ Report created: {report_file.name}\n")
        return report_file
    
    def generate_migration_csv(self, file_moves: list, directory_moves: list):
        """Generate migration CSV."""
        csv_file = self.workspace_root / f"ADVANCED_ORGANIZATION_MIGRATION_{self.timestamp}.csv"
        
        print("💾 Generating migration CSV...")
        
        all_moves = []
        
        # Add file moves
        for move in file_moves:
            all_moves.append({
                'original_path': move['original_path'],
                'new_path': move['new_path'],
                'category': move['category'],
                'parent_context': move['parent_context'],
                'purpose': move['purpose'],
                'reason': move['reason'],
                'move_type': 'file'
            })
        
        # Add directory moves (as file moves for each file in directory)
        # Note: Directory moves would need to be handled separately
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['original_path', 'new_path', 'category', 'parent_context', 'purpose', 'reason', 'move_type']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_moves)
        
        print(f"   ✅ CSV created: {csv_file.name}")
        print(f"   Total moves: {len(all_moves)}\n")
        
        return csv_file

def main():
    """Main execution."""
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    organizer = AdvancedParentFolderOrganizer(workspace_root)
    
    db_path = organizer.find_latest_index()
    if not db_path:
        print("❌ No reindex database found!")
        return
    
    print(f"📄 Using index: {db_path.name}\n")
    
    # Analyze parent folder context
    directory_analysis, file_relationships = organizer.analyze_parent_folder_context(db_path)
    
    # Generate intelligent moves
    file_moves = organizer.generate_intelligent_moves(directory_analysis, file_relationships)
    
    # Generate directory moves
    directory_moves = organizer.generate_directory_moves(directory_analysis)
    
    # Generate reports
    report = organizer.generate_report(directory_analysis, file_moves, directory_moves)
    migration_csv = organizer.generate_migration_csv(file_moves, directory_moves)
    
    print("=" * 80)
    print("✅ ADVANCED ORGANIZATION PLAN COMPLETE")
    print("=" * 80)
    print(f"\n📊 Results:")
    print(f"   Directories analyzed: {len(directory_analysis)}")
    print(f"   File moves generated: {len(file_moves)}")
    print(f"   Directory moves: {len(directory_moves)}")
    print(f"\n📄 Files generated:")
    print(f"   - Report: {report.name}")
    print(f"   - Migration CSV: {migration_csv.name}")
    print(f"\n💡 This plan uses parent-folder content awareness:")
    print(f"   - Respects project structures")
    print(f"   - Context-aware file placement")
    print(f"   - Preserves file relationships")
    print()

if __name__ == "__main__":
    main()

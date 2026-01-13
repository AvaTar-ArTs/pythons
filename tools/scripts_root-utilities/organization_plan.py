#!/usr/bin/env python3
"""
Intelligent Organization Plan Generator
Analyzes current structure and generates comprehensive organization recommendations.
"""

import sqlite3
import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

class OrganizationPlanner:
    """Generate intelligent organization plan."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Project categories
        self.project_categories = {
            'quantumforge-complete': 'active_project',
            'retention-suite-complete': 'active_project',
            'heavenlyhands-complete': 'active_project',
            'cleanconnect-complete': 'active_project',
            'avatararts-complete': 'active_project',
            'passive-income-empire': 'active_project',
            'education': 'active_project',
            'marketplace': 'active_project',
        }
        
        # File type organization rules
        self.file_organization = {
            'code_python': 'tools/',
            'code_javascript': 'projects/',
            'code_html': 'assets/html/',
            'code_css': 'assets/css/',
            'image': 'assets/images/',
            'document_markdown': 'docs/',
            'data': 'data/',
            'archive': 'archive/',
        }
    
    def find_latest_index(self):
        """Find latest reindex database."""
        db_files = sorted(
            self.workspace_root.glob("REINDEX_*.db"),
            reverse=True
        )
        return db_files[0] if db_files else None
    
    def analyze_current_structure(self, db_path: Path):
        """Analyze current directory structure."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("📊 Analyzing Current Structure")
        print("=" * 80)
        print()
        
        # Get top-level directories
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN parent_directory = '.' THEN filename
                    ELSE substr(parent_directory, 1, instr(parent_directory || '/', '/') - 1)
                END as top_level,
                COUNT(*) as file_count,
                ROUND(SUM(size_mb), 1) as total_mb,
                GROUP_CONCAT(DISTINCT file_type) as types
            FROM files
            GROUP BY top_level
            ORDER BY total_mb DESC
        ''')
        
        top_level_dirs = cursor.fetchall()
        
        # Analyze file distribution
        cursor.execute('''
            SELECT file_type, COUNT(*) as count, ROUND(SUM(size_mb), 1) as mb
            FROM files
            GROUP BY file_type
            ORDER BY mb DESC
        ''')
        
        file_distribution = cursor.fetchall()
        
        # Analyze depth distribution
        cursor.execute('''
            SELECT depth, COUNT(*) as count
            FROM files
            GROUP BY depth
            ORDER BY depth
        ''')
        
        depth_distribution = cursor.fetchall()
        
        conn.close()
        
        return {
            'top_level_dirs': top_level_dirs,
            'file_distribution': file_distribution,
            'depth_distribution': depth_distribution
        }
    
    def generate_organization_plan(self, analysis: dict):
        """Generate comprehensive organization plan."""
        
        print("🎯 Generating Organization Plan")
        print("=" * 80)
        print()
        
        plan = {
            'recommended_structure': {},
            'moves': [],
            'consolidations': [],
            'new_directories': [],
            'rationale': {}
        }
        
        # Recommended structure
        recommended = {
            'projects/': {
                'description': 'Active development projects',
                'should_contain': ['quantumforge-complete', 'retention-suite-complete', 
                                  'heavenlyhands-complete', 'cleanconnect-complete',
                                  'avatararts-complete', 'passive-income-empire',
                                  'education', 'marketplace'],
                'priority': 'HIGH'
            },
            'tools/': {
                'description': 'All Python scripts and utilities',
                'should_contain': ['tools/', 'scripts/', '*.py files'],
                'priority': 'HIGH'
            },
            'assets/': {
                'description': 'Static assets (HTML, CSS, images, fonts)',
                'subdirs': {
                    'html/': 'HTML files and templates',
                    'css/': 'Stylesheets',
                    'images/': 'Images (JPG, PNG, WebP, etc.)',
                    'fonts/': 'Font files',
                    'media/': 'Large media files (videos, audio)'
                },
                'priority': 'HIGH'
            },
            'docs/': {
                'description': 'Documentation and markdown files',
                'should_contain': ['*.md files', 'documentation'],
                'priority': 'MEDIUM'
            },
            'data/': {
                'description': 'Data files (CSV, JSON, databases)',
                'subdirs': {
                    'analysis/': 'Analysis outputs',
                    'exports/': 'Export files',
                    'databases/': 'SQLite databases',
                    'archives/': 'Old data files'
                },
                'priority': 'MEDIUM'
            },
            'archive/': {
                'description': 'Archived and backup files',
                'should_contain': ['backups', 'old files', 'reference files'],
                'priority': 'LOW'
            },
            'index/': {
                'description': 'Reindex files and search indexes',
                'should_contain': ['REINDEX_*.db', 'REINDEX_*.json', 'REINDEX_*.csv'],
                'priority': 'LOW'
            }
        }
        
        plan['recommended_structure'] = recommended
        
        # Generate specific moves based on analysis
        top_dirs = analysis['top_level_dirs']
        
        moves = []
        consolidations = []
        
        # Organize by file type
        for dir_info in top_dirs[:20]:
            top_level, file_count, total_mb, types = dir_info
            
            if top_level in ['tools', 'scripts']:
                moves.append({
                    'from': top_level,
                    'to': 'tools/',
                    'reason': 'Consolidate all Python tools',
                    'priority': 'HIGH'
                })
            elif top_level in ['html-assets', 'ai-sites']:
                moves.append({
                    'from': top_level,
                    'to': 'assets/html/',
                    'reason': 'Consolidate HTML assets',
                    'priority': 'MEDIUM'
                })
            elif 'organized_intelligent' in str(top_level):
                moves.append({
                    'from': top_level,
                    'to': 'archive/organized_intelligent/',
                    'reason': 'Large organized directory - review and archive',
                    'priority': 'LOW'
                })
        
        plan['moves'] = moves
        plan['consolidations'] = consolidations
        
        return plan
    
    def generate_migration_plan(self, plan: dict, db_path: Path):
        """Generate detailed migration plan with file mappings."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("📋 Generating Migration Plan")
        print("=" * 80)
        print()
        
        migrations = []
        
        # Python scripts consolidation
        cursor.execute('''
            SELECT path, parent_directory, filename
            FROM files
            WHERE file_type = 'code_python'
              AND parent_directory NOT LIKE 'tools/%'
              AND parent_directory NOT LIKE 'projects/%'
              AND parent_directory != 'tools'
            LIMIT 100
        ''')
        
        python_files = cursor.fetchall()
        
        for path, parent_dir, filename in python_files:
            # Determine new location
            if 'analysis' in parent_dir.lower() or 'analyze' in filename.lower():
                new_path = f"tools/analysis/{filename}"
            elif 'automation' in parent_dir.lower() or 'automate' in filename.lower():
                new_path = f"tools/automation/{filename}"
            elif 'utility' in parent_dir.lower() or 'util' in filename.lower():
                new_path = f"tools/utilities/{filename}"
            else:
                new_path = f"tools/{filename}"
            
            migrations.append({
                'original_path': path,
                'new_path': new_path,
                'category': 'python_script',
                'reason': 'Consolidate Python scripts into tools/'
            })
        
        # HTML files consolidation
        cursor.execute('''
            SELECT path, parent_directory, filename
            FROM files
            WHERE file_type = 'code_html'
              AND parent_directory NOT LIKE 'assets/%'
              AND parent_directory NOT LIKE 'projects/%'
              AND (parent_directory LIKE '%html%' OR parent_directory LIKE '%ai-sites%')
            LIMIT 50
        ''')
        
        html_files = cursor.fetchall()
        
        for path, parent_dir, filename in html_files:
            # Keep josephrosadomd HTML files in place (they're part of the site)
            if 'josephrosadomd' in path:
                continue
            
            new_path = f"assets/html/{filename}"
            migrations.append({
                'original_path': path,
                'new_path': new_path,
                'category': 'html_file',
                'reason': 'Consolidate HTML files into assets/html/'
            })
        
        # Data files organization
        cursor.execute('''
            SELECT path, parent_directory, filename
            FROM files
            WHERE file_type IN ('data', 'data_database')
              AND (filename LIKE '%.csv' OR filename LIKE '%.json' OR filename LIKE '%.db')
              AND parent_directory NOT LIKE 'data/%'
            LIMIT 50
        ''')
        
        data_files = cursor.fetchall()
        
        for path, parent_dir, filename in data_files:
            if 'REINDEX' in filename or 'ANALYSIS' in filename:
                new_path = f"index/{filename}"
            elif 'analysis' in parent_dir.lower():
                new_path = f"data/analysis/{filename}"
            else:
                new_path = f"data/{filename}"
            
            migrations.append({
                'original_path': path,
                'new_path': new_path,
                'category': 'data_file',
                'reason': 'Organize data files into data/ directory'
            })
        
        conn.close()
        
        return migrations
    
    def generate_report(self, plan: dict, migrations: list, analysis: dict):
        """Generate comprehensive organization report."""
        report_file = self.workspace_root / f"ORGANIZATION_PLAN_{self.timestamp}.md"
        
        print("📝 Generating Organization Plan Report...")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Intelligent Organization Plan\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Workspace:** `/Users/steven/AVATARARTS`\n\n")
            f.write("---\n\n")
            
            # Current state
            f.write("## 📊 Current State Analysis\n\n")
            f.write("### Top-Level Directories\n\n")
            f.write("| Directory | Files | Size (MB) | Types |\n")
            f.write("|-----------|------:|----------:|-------|\n")
            for dir_info in analysis['top_level_dirs'][:20]:
                top_level, file_count, total_mb, types = dir_info
                types_preview = types[:50] + '...' if len(types) > 50 else types
                f.write(f"| `{top_level}` | {file_count:,} | {total_mb} | {types_preview} |\n")
            f.write("\n")
            
            # Recommended structure
            f.write("## 🎯 Recommended Directory Structure\n\n")
            for dir_name, dir_info in plan['recommended_structure'].items():
                f.write(f"### {dir_name}\n\n")
                f.write(f"**Description:** {dir_info['description']}\n")
                f.write(f"**Priority:** {dir_info['priority']}\n\n")
                
                if 'subdirs' in dir_info:
                    f.write("**Subdirectories:**\n")
                    for subdir, desc in dir_info['subdirs'].items():
                        f.write(f"- `{subdir}` - {desc}\n")
                    f.write("\n")
                
                if 'should_contain' in dir_info:
                    f.write("**Should contain:**\n")
                    for item in dir_info['should_contain'][:5]:
                        f.write(f"- {item}\n")
                    if len(dir_info['should_contain']) > 5:
                        f.write(f"- ... and {len(dir_info['should_contain']) - 5} more\n")
                    f.write("\n")
            
            # Migration plan
            f.write("## 📦 Migration Plan\n\n")
            f.write(f"**Total files to reorganize:** {len(migrations)}\n\n")
            
            # Group by category
            by_category = defaultdict(list)
            for mig in migrations:
                by_category[mig['category']].append(mig)
            
            for category, migs in by_category.items():
                f.write(f"### {category.replace('_', ' ').title()} ({len(migs)} files)\n\n")
                f.write("| Original Path | New Path | Reason |\n")
                f.write("|---------------|----------|--------|\n")
                for mig in migs[:20]:
                    f.write(f"| `{mig['original_path']}` | `{mig['new_path']}` | {mig['reason']} |\n")
                if len(migs) > 20:
                    f.write(f"| ... | ... | ... ({len(migs) - 20} more) |\n")
                f.write("\n")
            
            # Implementation steps
            f.write("## 🚀 Implementation Steps\n\n")
            f.write("### Phase 1: Create New Structure (5 min)\n\n")
            f.write("```bash\n")
            f.write("mkdir -p projects tools assets/{html,css,images,fonts,media}\n")
            f.write("mkdir -p docs data/{analysis,exports,databases,archives}\n")
            f.write("mkdir -p archive index\n")
            f.write("```\n\n")
            
            f.write("### Phase 2: Move Active Projects (10 min)\n\n")
            f.write("Move completed projects to `projects/` directory.\n\n")
            
            f.write("### Phase 3: Consolidate Tools (15 min)\n\n")
            f.write("Move all Python scripts to `tools/` with subdirectories:\n")
            f.write("- `tools/analysis/` - Analysis scripts\n")
            f.write("- `tools/automation/` - Automation scripts\n")
            f.write("- `tools/utilities/` - Utility scripts\n\n")
            
            f.write("### Phase 4: Organize Assets (20 min)\n\n")
            f.write("Move HTML, CSS, images to `assets/` subdirectories.\n\n")
            
            f.write("### Phase 5: Organize Data (10 min)\n\n")
            f.write("Move CSV, JSON, database files to `data/` directory.\n\n")
            
            # Benefits
            f.write("## ✅ Benefits\n\n")
            f.write("- **Clear structure** - Easy to find files\n")
            f.write("- **Better organization** - Files grouped by purpose\n")
            f.write("- **Easier maintenance** - Clear separation of concerns\n")
            f.write("- **Scalability** - Structure supports growth\n")
            f.write("- **Professional** - Industry-standard organization\n\n")
        
        print(f"   ✅ Report created: {report_file.name}\n")
        return report_file
    
    def generate_migration_csv(self, migrations: list):
        """Generate CSV for migration."""
        csv_file = self.workspace_root / f"ORGANIZATION_MIGRATION_{self.timestamp}.csv"
        
        print("💾 Generating Migration CSV...")
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['original_path', 'new_path', 'category', 'reason']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(migrations)
        
        print(f"   ✅ CSV created: {csv_file.name}")
        print(f"   Total migrations: {len(migrations)}\n")
        
        return csv_file

def main():
    """Main execution."""
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    planner = OrganizationPlanner(workspace_root)
    
    db_path = planner.find_latest_index()
    if not db_path:
        print("❌ No reindex database found!")
        return
    
    print(f"📄 Using index: {db_path.name}\n")
    
    # Analyze current structure
    analysis = planner.analyze_current_structure(db_path)
    
    # Generate organization plan
    plan = planner.generate_organization_plan(analysis)
    
    # Generate migration plan
    migrations = planner.generate_migration_plan(plan, db_path)
    
    # Generate reports
    report = planner.generate_report(plan, migrations, analysis)
    migration_csv = planner.generate_migration_csv(migrations)
    
    print("=" * 80)
    print("✅ ORGANIZATION PLAN COMPLETE")
    print("=" * 80)
    print(f"\n📄 Files generated:")
    print(f"   - Organization Plan: {report.name}")
    print(f"   - Migration CSV: {migration_csv.name}")
    print(f"\n💡 Review the plan and CSV, then implement organization")
    print()

if __name__ == "__main__":
    main()

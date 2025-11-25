#!/usr/bin/env python3
"""
Project Consolidator - Organize and consolidate Python/JS projects
Identifies duplicate/similar projects and suggests consolidation
"""

import os
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import difflib

class ProjectConsolidator:
    def __init__(self, home_path="~/"):
        self.home = Path(home_path).expanduser().resolve()
        self.python_projects = []
        self.js_projects = []
        self.duplicates = []
        
    def load_workspace_report(self):
        """Load workspace optimization report"""
        json_files = sorted(Path.cwd().glob('workspace_optimization_*.json'), reverse=True)
        if not json_files:
            print("❌ No workspace optimization report found.")
            print("Run workspace_optimizer.py first!")
            return False
        
        with open(json_files[0]) as f:
            report = json.load(f)
        
        self.python_projects = report.get('python_projects', [])
        self.js_projects = report.get('js_projects', [])
        
        print(f"✅ Loaded {len(self.python_projects)} Python projects")
        print(f"✅ Loaded {len(self.js_projects)} JavaScript projects")
        return True
    
    def find_similar_projects(self, projects, name_key='path'):
        """Find projects with similar names"""
        similar_groups = defaultdict(list)
        
        for proj in projects:
            name = Path(proj[name_key]).name.lower()
            # Remove common suffixes
            clean_name = name.replace('-complete', '').replace('-archived', '')
            clean_name = clean_name.replace('-enhanced', '').replace('-pro', '')
            clean_name = clean_name.replace('_', '-')
            
            similar_groups[clean_name].append(proj)
        
        # Filter to only groups with multiple projects
        return {k: v for k, v in similar_groups.items() if len(v) > 1}
    
    def analyze_project_relationships(self):
        """Analyze relationships between projects"""
        print("\n🔍 Analyzing project relationships...\n")
        
        # Find similar Python projects
        similar_py = self.find_similar_projects(self.python_projects)
        
        if similar_py:
            print("🐍 Similar Python Projects Found:")
            print("-" * 80)
            for group_name, projects in similar_py.items():
                print(f"\n📦 Group: {group_name}")
                print(f"   {len(projects)} similar projects:\n")
                for proj in projects:
                    print(f"   • {proj['path']}")
                    print(f"     Files: {proj['py_files_count']} .py files")
                    deps = []
                    if proj.get('has_requirements'): deps.append("requirements.txt")
                    if proj.get('has_pyproject'): deps.append("pyproject.toml")
                    print(f"     Dependencies: {', '.join(deps) if deps else 'None'}")
                print()
        
        # Find similar JS projects
        similar_js = self.find_similar_projects(self.js_projects)
        
        if similar_js:
            print("\n📦 Similar JavaScript Projects Found:")
            print("-" * 80)
            for group_name, projects in similar_js.items():
                print(f"\n📦 Group: {group_name}")
                print(f"   {len(projects)} similar projects:\n")
                for proj in projects:
                    print(f"   • {proj['path']}")
                    print(f"     Files: {proj['total_files']} total files")
                    print(f"     node_modules: {'✓' if proj.get('has_node_modules') else '✗'}")
                print()
        
        return similar_py, similar_js
    
    def generate_consolidation_plan(self, similar_py, similar_js):
        """Generate consolidation recommendations"""
        print("\n" + "="*80)
        print("📋 CONSOLIDATION RECOMMENDATIONS")
        print("="*80)
        
        recommendations = []
        
        # Python project recommendations
        for group_name, projects in similar_py.items():
            # Find the "best" version (most files, in workspace, not archived)
            best = None
            archived = []
            
            for proj in projects:
                path = proj['path']
                if 'archive' in path.lower():
                    archived.append(proj)
                elif best is None or proj['py_files_count'] > best['py_files_count']:
                    best = proj
            
            if best and archived:
                recommendations.append({
                    'type': 'python',
                    'group': group_name,
                    'keep': best,
                    'archive': archived
                })
        
        # JavaScript project recommendations
        for group_name, projects in similar_js.items():
            best = None
            archived = []
            
            for proj in projects:
                path = proj['path']
                if 'archive' in path.lower():
                    archived.append(proj)
                elif best is None or proj['total_files'] > best['total_files']:
                    best = proj
            
            if best and archived:
                recommendations.append({
                    'type': 'javascript',
                    'group': group_name,
                    'keep': best,
                    'archive': archived
                })
        
        # Print recommendations
        if recommendations:
            print("\n💡 Recommended Consolidations:\n")
            
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec['group']} ({rec['type'].upper()})")
                print(f"   ✓ KEEP: {rec['keep']['path']}")
                print(f"   ✗ ARCHIVE/DELETE:")
                for arch in rec['archive']:
                    print(f"      • {arch['path']}")
                print()
        else:
            print("\n✅ No obvious duplicates found!")
        
        return recommendations
    
    def generate_consolidation_script(self, recommendations, output_path):
        """Generate script to consolidate projects"""
        script_lines = [
            "#!/bin/bash",
            "# Project Consolidation Script",
            f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "set -e",
            "",
            "echo '📦 Starting project consolidation...'",
            "echo ''",
            "",
            "# Create backup",
            "BACKUP_DIR=~/project_consolidation_backup_$(date +%Y%m%d_%H%M%S)",
            "mkdir -p $BACKUP_DIR",
            "echo '💾 Backup directory: $BACKUP_DIR'",
            "echo ''",
            "",
            "# Archive duplicate projects",
        ]
        
        archive_base = "~/consolidated_archives_$(date +%Y%m%d)"
        script_lines.append(f"ARCHIVE_DIR={archive_base}")
        script_lines.append("mkdir -p $ARCHIVE_DIR")
        script_lines.append("")
        
        for i, rec in enumerate(recommendations, 1):
            script_lines.append(f"# Consolidation {i}: {rec['group']}")
            script_lines.append(f"echo 'Processing: {rec['group']}'")
            script_lines.append(f"echo '  Keeping: {rec['keep']['path']}'")
            script_lines.append("")
            
            for arch in rec['archive']:
                path = arch['path']
                full_path = f"~/{path}"
                script_lines.append(f"# Archive: {path}")
                script_lines.append(f"if [ -d \"{full_path}\" ]; then")
                script_lines.append(f"    echo '  Archiving: {path}'")
                script_lines.append(f"    tar -czf \"$ARCHIVE_DIR/{Path(path).name}.tar.gz\" -C \"$(dirname \"{full_path}\")\" \"$(basename \"{full_path}\")\"")
                script_lines.append(f"    # Uncomment to delete after archiving:")
                script_lines.append(f"    # rm -rf \"{full_path}\"")
                script_lines.append(f"fi")
                script_lines.append("")
        
        script_lines.extend([
            "echo ''",
            "echo '✅ Consolidation complete!'",
            "echo 'Archives saved to: $ARCHIVE_DIR'",
            "echo ''",
            "echo '💡 Review the archives, then uncomment the rm -rf lines to delete originals'",
        ])
        
        with open(output_path, 'w') as f:
            f.write('\n'.join(script_lines))
        
        os.chmod(output_path, 0o755)
        print(f"\n✅ Consolidation script saved: {output_path}")
    
    def print_summary(self):
        """Print summary of projects"""
        print("\n" + "="*80)
        print("📊 PROJECT SUMMARY")
        print("="*80)
        
        # Categorize projects
        py_active = [p for p in self.python_projects if 'archive' not in p['path'].lower()]
        py_archived = [p for p in self.python_projects if 'archive' in p['path'].lower()]
        
        js_active = [p for p in self.js_projects if 'archive' not in p['path'].lower()]
        js_archived = [p for p in self.js_projects if 'archive' in p['path'].lower()]
        
        print(f"\n🐍 Python Projects:")
        print(f"   Active: {len(py_active)}")
        print(f"   Archived: {len(py_archived)}")
        print(f"   Total: {len(self.python_projects)}")
        
        print(f"\n📦 JavaScript Projects:")
        print(f"   Active: {len(js_active)}")
        print(f"   Archived: {len(js_archived)}")
        print(f"   Total: {len(self.js_projects)}")
        
        print("\n" + "="*80)


def main():
    consolidator = ProjectConsolidator()
    
    if not consolidator.load_workspace_report():
        return
    
    consolidator.print_summary()
    
    similar_py, similar_js = consolidator.analyze_project_relationships()
    recommendations = consolidator.generate_consolidation_plan(similar_py, similar_js)
    
    if recommendations:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        script_path = f"consolidate_projects_{timestamp}.sh"
        consolidator.generate_consolidation_script(recommendations, script_path)
        
        print("\n📋 Next Steps:")
        print(f"1. Review recommendations above")
        print(f"2. Review the script: {script_path}")
        print(f"3. Run consolidation: ./{script_path}")
        print("\n⚠️  IMPORTANT: This will create archives but NOT delete originals by default")
        print("   Review the archives first, then uncomment the delete commands in the script")


if __name__ == '__main__':
    main()

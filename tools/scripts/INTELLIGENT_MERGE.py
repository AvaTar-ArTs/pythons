#!/usr/bin/env python3
"""
Intelligent Project Merger
Deduplicates, diffs, and merges multiple versions of the same project
"""
import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import json

class IntelligentMerger:
    def __init__(self, workspace_root):
        self.workspace = Path(workspace_root)
        self.report = {
            'timestamp': datetime.now().isoformat(),
            'merges': [],
            'duplicates_removed': [],
            'files_kept': [],
            'conflicts': []
        }
    
    def get_file_hash(self, filepath):
        """Get MD5 hash of file"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def get_newest_file(self, files):
        """Get most recently modified file"""
        return max(files, key=lambda f: f.stat().st_mtime)
    
    def merge_directories(self, source_dirs, target_dir, project_name):
        """Intelligently merge multiple versions of same project"""
        print(f"\n?? Merging {project_name}...")
        print(f"   Sources: {len(source_dirs)} versions")
        
        target = Path(target_dir)
        target.mkdir(parents=True, exist_ok=True)
        
        # Track all files across versions
        all_files = {}
        
        for source in source_dirs:
            source_path = Path(source)
            if not source_path.exists():
                continue
                
            print(f"   Scanning: {source_path.name}")
            
            for file in source_path.rglob('*'):
                if file.is_file() and not any(skip in str(file) for skip in ['.git', 'node_modules', '__pycache__', '.DS_Store']):
                    relative = file.relative_to(source_path)
                    
                    if str(relative) not in all_files:
                        all_files[str(relative)] = []
                    
                    all_files[str(relative)].append(file)
        
        # Merge intelligently
        kept = 0
        duplicates = 0
        conflicts = 0
        
        for rel_path, versions in all_files.items():
            target_file = target / rel_path
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            if len(versions) == 1:
                # Only one version - just copy
                shutil.copy2(versions[0], target_file)
                kept += 1
            else:
                # Multiple versions - choose best
                hashes = {self.get_file_hash(v): v for v in versions}
                
                if len(hashes) == 1:
                    # All versions identical - use newest
                    newest = self.get_newest_file(versions)
                    shutil.copy2(newest, target_file)
                    duplicates += len(versions) - 1
                else:
                    # Different versions - use newest
                    newest = self.get_newest_file(versions)
                    shutil.copy2(newest, target_file)
                    conflicts += 1
                    
                    self.report['conflicts'].append({
                        'file': str(rel_path),
                        'versions': len(versions),
                        'kept': str(newest),
                        'note': 'Kept newest version'
                    })
                
                kept += 1
        
        print(f"   ? Merged {kept} files")
        print(f"   ???  Removed {duplicates} duplicates")
        if conflicts > 0:
            print(f"   ??  {conflicts} conflicts (kept newest)")
        
        self.report['merges'].append({
            'project': project_name,
            'sources': [str(s) for s in source_dirs],
            'target': str(target_dir),
            'files_kept': kept,
            'duplicates': duplicates,
            'conflicts': conflicts
        })
        
        return target_dir

def main():
    workspace = Path.home() / 'workspace'
    merger = IntelligentMerger(workspace)
    
    print("=" * 70)
    print("              ?? INTELLIGENT PROJECT MERGER")
    print("=" * 70)
    print()
    
    # Define merges
    merges = [
        {
            'name': 'HeavenlyHands',
            'sources': [
                workspace / 'revenue-projects/heavenlyhands/heavenlyHands',
                workspace / 'revenue-projects/heavenlyhands-v2',
                workspace / 'revenue-projects/heavenlyhands-archived',
                workspace / 'LIVE-DEPLOYMENT/heavenlyhands'
            ],
            'target': workspace / 'FINAL/heavenlyhands-complete'
        },
        {
            'name': 'AvatarArts',
            'sources': [
                workspace / 'creative-platforms/avatararts/AvaTarArTs',
                workspace / 'avatararts-projects',
                workspace / 'avatararts-steven-docs'
            ],
            'target': workspace / 'FINAL/avatararts-complete'
        },
        {
            'name': 'QuantumForge',
            'sources': [
                workspace / 'websites/quantumforge-v1',
                workspace / 'websites/quantumforge-v2',
                workspace / 'websites/quantumforge-docs',
                workspace / 'websites/quantumforge-landings'
            ],
            'target': workspace / 'FINAL/quantumforge-complete'
        },
        {
            'name': 'CleanConnect Pro',
            'sources': [
                workspace / 'revenue-projects/cleanconnect/cleanconnect-pro',
                workspace / 'LIVE-DEPLOYMENT/ai-voice-agents' # Has AI voice code
            ],
            'target': workspace / 'FINAL/cleanconnect-complete'
        }
    ]
    
    # Execute merges
    for merge in merges:
        existing_sources = [s for s in merge['sources'] if Path(s).exists()]
        if existing_sources:
            merger.merge_directories(
                existing_sources,
                merge['target'],
                merge['name']
            )
    
    # Copy single-version projects as-is
    print("\n?? Copying single-version projects...")
    
    single_projects = {
        'Retention Suite': workspace / 'revenue-projects/retention-suite-complete',
        'Passive Income Empire': workspace / 'revenue-projects/passive-income/passive-income-empire',
        'Creative Marketplace': workspace / 'creative-platforms/marketplace',
        'Creative Education': workspace / 'creative-platforms/education'
    }
    
    for name, source in single_projects.items():
        if source.exists():
            target = workspace / 'FINAL' / source.name
            print(f"   Copying: {name}")
            shutil.copytree(source, target, dirs_exist_ok=True)
    
    # Save report
    print("\n?? Generating merge report...")
    report_path = workspace / 'MERGE_REPORT.json'
    with open(report_path, 'w') as f:
        json.dump(merger.report, f, indent=2)
    
    # Create human-readable report
    report_md = workspace / 'MERGE_REPORT.md'
    with open(report_md, 'w') as f:
        f.write(f"# ?? Intelligent Merge Report\n\n")
        f.write(f"**Generated:** {merger.report['timestamp']}\n\n")
        f.write(f"---\n\n")
        f.write(f"## Projects Merged\n\n")
        
        for merge in merger.report['merges']:
            f.write(f"### {merge['project']}\n")
            f.write(f"- **Sources:** {len(merge['sources'])} versions\n")
            f.write(f"- **Files kept:** {merge['files_kept']}\n")
            f.write(f"- **Duplicates removed:** {merge['duplicates']}\n")
            f.write(f"- **Conflicts resolved:** {merge['conflicts']}\n")
            f.write(f"- **Target:** `{merge['target']}`\n\n")
        
        if merger.report['conflicts']:
            f.write(f"## ?? Conflicts Resolved\n\n")
            for conflict in merger.report['conflicts'][:20]:
                f.write(f"- `{conflict['file']}`: Kept newest ({conflict['kept']})\n")
            if len(merger.report['conflicts']) > 20:
                f.write(f"\n... and {len(merger.report['conflicts']) - 20} more\n")
    
    print(f"   ? Report saved: MERGE_REPORT.md")
    
    print("\n" + "=" * 70)
    print("              ?? INTELLIGENT MERGE COMPLETE!")
    print("=" * 70)
    print()
    print("?? Final consolidated projects in:")
    print("   ~/workspace/FINAL/")
    print()
    print("?? Read merge report:")
    print("   cat ~/workspace/MERGE_REPORT.md")
    print()
    print("?? Next step:")
    print("   cd ~/workspace/FINAL/")
    print("   ls -la")
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()

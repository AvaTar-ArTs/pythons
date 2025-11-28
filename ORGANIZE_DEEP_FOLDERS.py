#!/usr/bin/env python3
"""
Organize and flatten deep folder structures
Identifies user-created folders (not git repos/archives) and suggests flattening
"""

from pathlib import Path
import json
import shutil
from datetime import datetime

documents_dir = Path.home() / "Documents"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Folders to exclude (system/dependency/archive folders)
EXCLUDE_PATTERNS = [
    'node_modules',
    '.git',
    '__pycache__',
    '.next',
    'dist',
    'build',
    '.venv',
    'venv',
    '.env',
    '.idea',
    '.vscode',
    'target',
    'bin',
    'obj',
    'Archives/repos',  # Archived code repos
    'github/',  # Cloned repos
    'Code/openai-cookbook',  # Code repository
]

def should_exclude(path):
    """Check if path should be excluded"""
    path_str = str(path.relative_to(documents_dir))
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    return False

def is_git_repo(path):
    """Check if path is a git repository"""
    return (path / '.git').exists()

def analyze_folder_structure():
    """Analyze folder structure and identify organization candidates"""
    candidates = []
    
    def analyze_path(path, parent_depth=0):
        try:
            if not path.exists() or not path.is_dir():
                return
            
            # Skip excluded paths
            if should_exclude(path):
                return
            
            # Skip if it's a git repo (unless it's in a specific location we want to organize)
            if is_git_repo(path) and 'Archives' not in str(path):
                return
            
            depth = len(path.relative_to(documents_dir).parts)
            
            # Count files and subfolders
            items = list(path.iterdir())
            files = [f for f in items if f.is_file()]
            folders = [f for f in items if f.is_dir()]
            
            file_count = len(files)
            folder_count = len(folders)
            
            # Calculate size
            total_size = sum(f.stat().st_size for f in files)
            
            # If depth > 3 and has files, it's a candidate
            if depth > 3 and file_count > 0:
                # Check if all subfolders are empty or have minimal content
                total_sub_files = 0
                for subfolder in folders:
                    try:
                        sub_files = list(subfolder.rglob('*'))
                        total_sub_files += sum(1 for f in sub_files if f.is_file())
                    except:
                        pass
                
                candidates.append({
                    'path': str(path.relative_to(documents_dir)),
                    'depth': depth,
                    'files': file_count,
                    'subfolders': folder_count,
                    'sub_files': total_sub_files,
                    'size_mb': round(total_size / (1024 * 1024), 2),
                    'severity': file_count * depth,
                    'can_flatten': total_sub_files < file_count * 2  # If subfolders don't have many more files
                })
            
            # Recurse
            for folder in folders:
                if not should_exclude(folder):
                    analyze_path(folder, depth)
        
        except (PermissionError, OSError):
            pass
    
    print("Analyzing folder structure...")
    analyze_path(documents_dir)
    
    return candidates

def create_organization_plan(candidates):
    """Create an organization plan"""
    # Sort by severity
    candidates.sort(key=lambda x: x['severity'], reverse=True)
    
    plan = {
        'high_priority': [],
        'medium_priority': [],
        'low_priority': [],
        'skip': []
    }
    
    for candidate in candidates:
        # High priority: depth > 4, severity > 500, can flatten
        if candidate['depth'] > 4 and candidate['severity'] > 500 and candidate['can_flatten']:
            plan['high_priority'].append(candidate)
        # Medium priority: depth > 3, severity > 200
        elif candidate['depth'] > 3 and candidate['severity'] > 200:
            plan['medium_priority'].append(candidate)
        # Low priority: depth > 3, lower severity
        elif candidate['depth'] > 3:
            plan['low_priority'].append(candidate)
        else:
            plan['skip'].append(candidate)
    
    return plan

def flatten_folder(source_path, target_depth=2):
    """Flatten a folder to target depth"""
    source = documents_dir / source_path
    if not source.exists():
        return False, f"Path does not exist: {source_path}"
    
    try:
        # Calculate how many levels to go up
        current_depth = len(source.relative_to(documents_dir).parts)
        levels_to_go_up = current_depth - target_depth
        
        if levels_to_go_up <= 0:
            return False, "Already at or below target depth"
        
        # Create new path at target depth
        parts = source.relative_to(documents_dir).parts
        new_parent = documents_dir / '/'.join(parts[:target_depth])
        new_name = '_'.join(parts[target_depth:])  # Combine deeper parts with underscore
        new_path = new_parent / new_name
        
        # Create backup log entry
        backup_log = documents_dir / f"FLATTEN_BACKUP_LOG_{timestamp}.csv"
        with open(backup_log, 'a') as log:
            log.write(f"{source_path},{new_path.relative_to(documents_dir)},{current_depth},{target_depth}\n")
        
        # Move folder
        if new_path.exists():
            # Handle name conflicts
            counter = 1
            while new_path.exists():
                new_path = new_parent / f"{new_name}_{counter}"
                counter += 1
        
        shutil.move(str(source), str(new_path))
        return True, f"Moved to: {new_path.relative_to(documents_dir)}"
    
    except Exception as e:
        return False, f"Error: {str(e)}"

print("=" * 100)
print("🔍 DEEP FOLDER ORGANIZATION ANALYSIS")
print("=" * 100)
print()

# Analyze structure
candidates = analyze_folder_structure()

print(f"Found {len(candidates)} candidate folders with depth > 3")
print()

# Create organization plan
plan = create_organization_plan(candidates)

print("=" * 100)
print("📊 ORGANIZATION PLAN")
print("=" * 100)
print()

print(f"🔴 HIGH PRIORITY: {len(plan['high_priority'])} folders")
print("-" * 100)
for i, folder in enumerate(plan['high_priority'][:20], 1):
    print(f"{i:2d}. Depth: {folder['depth']} | Files: {folder['files']:,} | "
          f"Severity: {folder['severity']:,} | {folder['path']}")

print()
print(f"🟡 MEDIUM PRIORITY: {len(plan['medium_priority'])} folders")
print("-" * 100)
for i, folder in enumerate(plan['medium_priority'][:20], 1):
    print(f"{i:2d}. Depth: {folder['depth']} | Files: {folder['files']:,} | "
          f"Severity: {folder['severity']:,} | {folder['path']}")

print()
print(f"🟢 LOW PRIORITY: {len(plan['low_priority'])} folders")
print("-" * 100)
for i, folder in enumerate(plan['low_priority'][:10], 1):
    print(f"{i:2d}. Depth: {folder['depth']} | Files: {folder['files']:,} | "
          f"Severity: {folder['severity']:,} | {folder['path']}")

# Save plan
plan_file = documents_dir / f"ORGANIZATION_PLAN_{timestamp}.json"
with open(plan_file, 'w') as f:
    json.dump({
        'timestamp': timestamp,
        'summary': {
            'high_priority': len(plan['high_priority']),
            'medium_priority': len(plan['medium_priority']),
            'low_priority': len(plan['low_priority']),
            'total_candidates': len(candidates)
        },
        'plan': plan
    }, f, indent=2)

print()
print(f"📄 Organization plan saved: {plan_file.name}")
print()
print("=" * 100)
print("💡 NEXT STEPS")
print("=" * 100)
print()
print("To flatten high-priority folders, run:")
print("  python3 ORGANIZE_DEEP_FOLDERS.py --flatten-high-priority")
print()
print("To flatten a specific folder:")
print("  python3 ORGANIZE_DEEP_FOLDERS.py --flatten <folder_path>")
print()
print("=" * 100)
print("✅ ANALYSIS COMPLETE")
print("=" * 100)


#!/usr/bin/env python3
"""
COMPREHENSIVE PYTHON SCAN - FIND MISSED SCRIPTS
=================================================
Scans ALL directories for Python files we may have missed.
"""

import os
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ============================================================
# Configuration
# ============================================================

HOME = Path("/Users/steven")
OUTPUT_CSV = "/Users/steven/python-marketplace-inventory/COMPREHENSIVE_SCAN_RESULTS.csv"
MISSED_SCRIPTS_CSV = "/Users/steven/python-marketplace-inventory/MISSED_SCRIPTS.csv"

# All directories to scan (from user's list)
SCAN_DIRS = [
    # Dot directories (hidden)
    ".actor", ".agent_events", ".agent_ops", ".agents", ".aider", ".aitk", ".apify",
    ".archives", ".autotagger-lite", ".boltai", ".book_of_memory", ".cagent", ".chatgpt",
    ".cline", ".codeium", ".copilot", ".crewai", ".cursor", ".domain-catalog", ".dotfiles",
    ".eigent", ".env.d", ".file-tracker", ".gemini", ".git-ai", ".github", ".grok", ".groq",
    ".harbor", ".iterm2", ".kimi", ".logseq", ".mcp-auth", ".mcp-central", ".mcphooker",
    ".ollama", ".opencode", ".pdf-filler-profiles", ".postman", ".qodo", ".qwen", ".raycast",
    ".scan_temp", ".secrets", ".serena", ".services", ".sonarlint", ".spicetify", ".spotdl",
    ".streamlit", ".supremepower", ".tooluniverse", ".u2net", ".update_logs", ".vscode",
    ".zsh", ".zshrc.d", ".claude", ".codex", ".tagger",
    
    # Regular directories
    "agent_forge", "agent-transcripts", "AI_Chats", "ai_merge_auto", "aider-env",
    "AutoTagger", "autotagger-lite", "backups", "bin", "book_of_memory", "chromium",
    "claudemarketplaces.com", "clean", "codex-upgrades", "Development", "DOC-sorted",
    "Documents", "Downloads", "Epstein", "Fancy-Advanced-Med-journals", "file-tracker",
    "Fixes", "fuzzy-finder", "git-ai", "github", "grok", "ice-tracker", "iterm2",
    "iterm2_prompt-engineering-exploration", "kimi", "logs", "MarketMaster",
    "Master CodeSnip dev", "MasterxEo", "mcPHooker", "mcphooker-lite",
    "Miniforge_Mamba_Analysis", "my_crew", "my-simple", "nocTurneMeLoDieS",
    "nocTurneMeLoDieS_HTML_Archive", "python_syntax_fix_report", "python-inventory",
    "python-marketplace-inventory", "python-portfolio-inventory", "pythons", "Raycast",
    "reports", "scripts", "simplegallery", "Sora", "sora-remover", "test", "tester",
    "tools", "upWork", "userscripts", "uv-demo", "zombot-simple-gallery", "AutoTag",
    "iCloud",
]

# Directories to EXCLUDE (system/dependency files)
EXCLUDE_PATTERNS = {
    # Virtual environments
    ".venv", ".venv_dev", "site-packages", "dist-packages",
    
    # Node.js
    "node_modules",
    
    # Cache/Build
    ".cache", "build", "dist", ".eggs", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".tox", ".nox",
    
    # System
    "Library", "Applications", "Public", "Movies", "Music", "Pictures",
    "google-cloud-sdk", ".nvm", ".npm", ".npm-global", ".cargo", ".rustup",
    ".rbenv", ".bun", ".bundle", ".gem", ".mamba", ".pixi", ".conda",
    ".oh-my-zsh", ".zsh_sessions", ".zshrc_archive", "zsh-autocomplete",
    "zsh-completions",
    
    # IDE/Editor extensions
    ".vscode/extensions", ".cursor/extensions",
    
    # Package managers
    ".local/share/uv",
    
    # Docker/Containers
    ".docker",
    
    # SSH/Security
    ".ssh", ".gnupg", ".secrets",
    
    # Logs/Backups
    "backups", "logs", ".update_logs",
}

# ============================================================
# Scanning Functions
# ============================================================

def should_exclude_dir(dir_name: str, dir_path: Path) -> bool:
    """Check if directory should be excluded."""
    # Check exact matches
    if dir_name in EXCLUDE_PATTERNS:
        return True
    
    # Check path contains
    path_str = str(dir_path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    
    return False


def scan_directory(scan_dir: Path) -> list:
    """Scan a directory for Python files."""
    py_files = []
    
    if not scan_dir.exists():
        return py_files
    
    try:
        for root, dirs, files in os.walk(scan_dir, topdown=True):
            root_path = Path(root)
            
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not should_exclude_dir(d, root_path / d)]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = root_path / file
                    try:
                        stat = file_path.stat()
                        py_files.append({
                            'file_name': file,
                            'full_path': str(file_path),
                            'file_size_kb': round(stat.st_size / 1024, 1),
                            'last_modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                            'parent_dir': scan_dir.name,
                        })
                    except OSError:
                        pass
    except PermissionError:
        pass
    except Exception as e:
        print(f"   ⚠️  Error scanning {scan_dir}: {e}")
    
    return py_files


def main():
    """Run comprehensive scan."""
    
    print("="*70)
    print("🔍 COMPREHENSIVE PYTHON SCAN - FINDING MISSED SCRIPTS")
    print("="*70)
    
    all_files = []
    dirs_scanned = 0
    dirs_not_found = 0
    
    for dir_name in SCAN_DIRS:
        scan_dir = HOME / dir_name
        
        if not scan_dir.exists():
            dirs_not_found += 1
            continue
        
        dirs_scanned += 1
        
        if dirs_scanned % 10 == 0:
            print(f"   Scanned {dirs_scanned} directories...")
        
        files = scan_directory(scan_dir)
        all_files.extend(files)
    
    print("\n✅ Scan complete!")
    print(f"   Directories scanned: {dirs_scanned}")
    print(f"   Directories not found: {dirs_not_found}")
    print(f"   Total Python files found: {len(all_files):,}")
    
    # Compare with existing inventory
    existing_files = load_existing_inventory()
    
    # Find new files (not in existing inventory)
    existing_paths = set(f['full_path'] for f in existing_files)
    new_files = [f for f in all_files if f['full_path'] not in existing_paths]
    
    print("\n📊 Comparison Results:")
    print(f"   Existing inventory: {len(existing_files):,} files")
    print(f"   Newly found: {len(new_files):,} files")
    print(f"   Already tracked: {len(all_files) - len(new_files):,} files")
    
    # Save results
    print("\n💾 Saving results...")
    
    # Save all found files
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        if all_files:
            fieldnames = list(all_files[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_files)
    
    # Save only new/missed files
    with open(MISSED_SCRIPTS_CSV, 'w', newline='', encoding='utf-8') as f:
        if new_files:
            fieldnames = list(new_files[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(new_files)
    
    print(f"   ✅ All files: {OUTPUT_CSV}")
    print(f"   ✅ New files: {MISSED_SCRIPTS_CSV}")
    
    # Show top directories with new files
    if new_files:
        dir_counts = defaultdict(int)
        for f in new_files:
            dir_counts[f['parent_dir']] += 1
        
        print("\n📁 Top Directories with New Files:")
        for dir_name, count in sorted(dir_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
            print(f"   {dir_name:40s} {count:,} files")
    
    print("\n" + "="*70)


def load_existing_inventory() -> list:
    """Load existing inventory to compare."""
    existing = []
    inventory_path = HOME / "python-marketplace-inventory" / "YOUR_PYTHON_SCRIPTS.csv"
    
    if inventory_path.exists():
        with open(inventory_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing.append(row)
    
    return existing


if __name__ == "__main__":
    main()

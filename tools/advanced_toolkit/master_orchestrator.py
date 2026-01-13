#!/usr/bin/env python3
"""
MASTER ORCHESTRATOR
Uses ALL fancy tools + API keys from ~/.env.d + existing workflows
Complete intelligent music management system
"""

import csv
from pathlib import Path
import subprocess
import json
from datetime import datetime
from collections import defaultdict
import sys

# Import our fancy tools
sys.path.insert(0, str(Path.home() / 'advanced_toolkit'))

def load_api_keys():
    """Load all API keys from ~/.env.d/"""
    
    print("\n" + "=" * 80)
    print("  LOADING API KEYS FROM ~/.env.d/")
    print("=" * 80 + "\n")
    
    env_dir = Path.home() / '.env.d'
    
    if not env_dir.exists():
        print("??  ~/.env.d/ not found\n")
        return {}
    
    config = {}
    
    for env_file in env_dir.iterdir():
        if env_file.name.startswith('.'):
            continue
        
        print(f"Loading: {env_file.name}")
        
        try:
            if env_file.suffix == '.json':
                with open(env_file, 'r') as f:
                    data = json.load(f)
                    config.update(data)
            elif env_file.suffix in ['.env', '.txt', ''] or env_file.name.endswith('.env'):
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if '=' in line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            config[key.strip()] = value.strip().strip('"').strip("'")
        except Exception as e:
            print(f"  ??  Error: {e}")
    
    print(f"\n? Loaded {len(config)} configuration values\n")
    
    # Show what we have (without values)
    print("Available services:")
    for key in sorted(config.keys()):
        if any(term in key.lower() for term in ['key', 'token', 'secret', 'api']):
            service = key.split('_')[0]
            print(f"  ? {service}")
    
    print()
    return config

def load_all_tools():
    """Inventory all fancy tools we've created"""
    
    print("=" * 80)
    print("  LOADING ALL FANCY TOOLS")
    print("=" * 80 + "\n")
    
    toolkit_dir = Path.home() / 'advanced_toolkit'
    
    tools = list(toolkit_dir.glob('*.py'))
    
    print(f"Found {len(tools)} Python tools:\n")
    
    tool_categories = {
        'Analysis': [],
        'Organization': [],
        'Matching': [],
        'Transcription': [],
        'Integration': [],
        'Utilities': []
    }
    
    for tool in sorted(tools):
        name = tool.stem
        
        if any(term in name.lower() for term in ['analyz', 'scan', 'reanalys', 'deep']):
            tool_categories['Analysis'].append(name)
        elif any(term in name.lower() for term in ['organiz', 'consolidat', 'bundle', 'cleanup']):
            tool_categories['Organization'].append(name)
        elif any(term in name.lower() for term in ['match', 'compare', 'cross', 'find']):
            tool_categories['Matching'].append(name)
        elif any(term in name.lower() for term in ['transcrib', 'whisper', 'rename']):
            tool_categories['Transcription'].append(name)
        elif any(term in name.lower() for term in ['integrat', 'merge', 'unif', 'master']):
            tool_categories['Integration'].append(name)
        else:
            tool_categories['Utilities'].append(name)
    
    for category, tools_list in tool_categories.items():
        if tools_list:
            print(f"{category}:")
            for tool in tools_list:
                print(f"  ? {tool}")
            print()
    
    return tool_categories

def load_existing_workflows():
    """Load existing workflow scripts"""
    
    print("=" * 80)
    print("  EXISTING WORKFLOWS")
    print("=" * 80 + "\n")
    
    music_dir = Path.home() / 'Music'
    
    workflows = {
        'organize_suno': music_dir / 'ORGANIZE_SUNO_DOWNLOADS.py',
        'test_transcription': music_dir / 'TEST_TRANSCRIPTION.sh',
    }
    
    available = {}
    
    for name, path in workflows.items():
        if path.exists():
            print(f"? {name}: {path}")
            available[name] = path
        else:
            print(f"? {name}: Not found")
    
    print()
    return available

def create_master_workflow_plan():
    """Create comprehensive workflow plan using all resources"""
    
    print("=" * 80)
    print("  MASTER WORKFLOW PLAN")
    print("=" * 80 + "\n")
    
    home = Path.home()
    
    # Load unified catalog
    catalog = home / 'Music/UNIFIED_MASTER_CATALOG.csv'
    
    if not catalog.exists():
        print("? Unified catalog not found")
        return
    
    with open(catalog, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        entries = list(reader)
    
    # Analyze what needs to be done
    stats = {
        'total_files': len(entries),
        'your_music': 0,
        'need_transcription': 0,
        'need_organization': 0,
        'need_metadata': 0,
        'need_bundles': 0,
        'complete': 0,
        'duplicates_to_check': 0,
    }
    
    for entry in entries:
        if entry.get('is_your_music') in ['YES', 'True', 'TRUE']:
            stats['your_music'] += 1
        
        if entry.get('should_transcribe') == 'YES' and entry.get('transcribed') in ['NO', '']:
            stats['need_transcription'] += 1
        
        if entry.get('has_metadata_tags') in ['NO', 'False', 'FALSE']:
            stats['need_metadata'] += 1
        
        if entry.get('has_bundle') in ['NO', 'False', 'FALSE'] and entry.get('is_your_music') in ['YES', 'True', 'TRUE']:
            stats['need_bundles'] += 1
        
        if entry.get('status') == 'COMPLETE':
            stats['complete'] += 1
    
    # Load duplicates
    dup_file = home / 'Music/DEEP_SCAN_DUPLICATES.csv'
    if dup_file.exists():
        with open(dup_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            stats['duplicates_to_check'] = sum(1 for _ in reader)
    
    print("Current Status:")
    print(f"  Total audio files: {stats['total_files']:,}")
    print(f"  Your original music: {stats['your_music']:,}")
    print(f"  Fully complete: {stats['complete']:,}")
    print()
    
    print("Work Needed:")
    print(f"  ?? Need transcription: {stats['need_transcription']:,}")
    print(f"  ???  Need metadata: {stats['need_metadata']:,}")
    print(f"  ?? Need bundles: {stats['need_bundles']:,}")
    print(f"  ?? Duplicates to review: {stats['duplicates_to_check']:,}")
    print()
    
    # Create action plan
    workflow_output = home / 'Music/MASTER_WORKFLOW_PLAN.md'
    
    with open(workflow_output, 'w', encoding='utf-8') as f:
        f.write("# ?? Master Workflow Plan\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Files:** {stats['total_files']:,}\n")
        f.write(f"**Your Music:** {stats['your_music']:,}\n\n")
        
        f.write("---\n\n")
        f.write("## ?? Priority Actions\n\n")
        
        # Priority 1: Transcription
        if stats['need_transcription'] > 0:
            f.write(f"### 1. Transcribe Files ({stats['need_transcription']:,} files)\n\n")
            f.write("**Why:** Many files have bad names that can only be fixed after transcription\n\n")
            f.write("**Tools to use:**\n")
            f.write("```bash\n")
            f.write("# Test first (3 files)\n")
            f.write("cd ~/Music && ./TEST_TRANSCRIPTION.sh\n\n")
            f.write("# Then batch transcribe HIGH priority bad filenames\n")
            f.write("python3 ~/advanced_toolkit/transcribe_and_rename_workflow.py\n\n")
            f.write("# Or full batch (all should_transcribe=YES)\n")
            f.write("python3 ~/advanced_toolkit/batch_transcribe_from_catalog.py\n")
            f.write("```\n\n")
            f.write(f"**API Key needed:** WHISPER (local) or ASSEMBLYAI_API_KEY\n\n")
        
        # Priority 2: Remove duplicates
        if stats['duplicates_to_check'] > 0:
            f.write(f"### 2. Remove Duplicates ({stats['duplicates_to_check']:,} groups)\n\n")
            f.write("**Why:** Save space and reduce confusion\n\n")
            f.write("**Tools to use:**\n")
            f.write("```bash\n")
            f.write("# Review duplicates\n")
            f.write("open ~/Music/DEEP_SCAN_DUPLICATES.csv\n\n")
            f.write("# Auto-remove (keeps best quality)\n")
            f.write("python3 ~/advanced_toolkit/smart_duplicate_remover.py\n")
            f.write("```\n\n")
        
        # Priority 3: Add metadata
        if stats['need_metadata'] > 0:
            f.write(f"### 3. Add Metadata Tags ({stats['need_metadata']:,} files)\n\n")
            f.write("**Why:** Proper metadata makes music players work better\n\n")
            f.write("**Tools to use:**\n")
            f.write("```bash\n")
            f.write("# Review what's missing\n")
            f.write("open ~/Music/TASK2_METADATA_EXTRACTION.csv\n\n")
            f.write("# Batch add from master data\n")
            f.write("python3 ~/advanced_toolkit/batch_add_metadata.py\n")
            f.write("```\n\n")
        
        # Priority 4: Create bundles
        if stats['need_bundles'] > 0:
            f.write(f"### 4. Create Song Bundles ({stats['need_bundles']:,} songs)\n\n")
            f.write("**Why:** Keep all related content together\n\n")
            f.write("**Tools to use:**\n")
            f.write("```bash\n")
            f.write("# Expand bundles for all your music\n")
            f.write("python3 ~/advanced_toolkit/expand_song_bundles.py\n\n")
            f.write("# Extract relevant content (smart, not full copies)\n")
            f.write("python3 ~/advanced_toolkit/extract_relevant_content_to_bundles.py\n")
            f.write("```\n\n")
        
        f.write("---\n\n")
        f.write("## ?? All Available Tools\n\n")
        
        f.write("### Analysis Tools\n")
        f.write("- `comprehensive_mp3_reanalysis.py` - Deep analysis of all MP3s\n")
        f.write("- `deep_scan_all_content.py` - Multi-level directory scan\n")
        f.write("- `analyze_all_durations.py` - Duration-based classification\n")
        f.write("- `identify_files_needing_transcription.py` - Find bad filenames\n\n")
        
        f.write("### Organization Tools\n")
        f.write("- `consolidate_song_bundles.py` - Create complete bundles\n")
        f.write("- `fix_bundle_names.py` - Clean up bundle folder names\n")
        f.write("- `cleanup_bundle_duplicates.py` - Remove duplicate files\n")
        f.write("- `ORGANIZE_SUNO_DOWNLOADS.py` - Organize downloaded songs\n\n")
        
        f.write("### Matching & Integration Tools\n")
        f.write("- `deep_content_matching.py` - Match songs with lyrics/prompts\n")
        f.write("- `find_all_related_content.py` - Cross-reference everything\n")
        f.write("- `merge_all_google_sheets.py` - Integrate Google Sheets\n")
        f.write("- `integrate_user_updates.py` - Merge your edits\n\n")
        
        f.write("### Transcription Tools\n")
        f.write("- `transcribe_and_rename_workflow.py` - Transcribe + rename bad files\n")
        f.write("- `TEST_TRANSCRIPTION.sh` - Test Whisper setup\n\n")
        
        f.write("### Master Reports\n")
        f.write("- `create_unified_master_catalog.py` - ONE source of truth\n")
        f.write("- `create_master_csv_all_fields.py` - All metadata fields\n")
        f.write("- `create_ultimate_master_report.py` - Comprehensive report\n\n")
        
        f.write("---\n\n")
        f.write("## ?? Recommended Workflow\n\n")
        
        f.write("### Phase 1: Transcription (Needed for proper naming)\n")
        f.write("```bash\n")
        f.write("# 1. Test Whisper\n")
        f.write("cd ~/Music && ./TEST_TRANSCRIPTION.sh\n\n")
        f.write("# 2. Transcribe HIGH priority bad filenames\n")
        f.write("python3 ~/advanced_toolkit/transcribe_and_rename_workflow.py\n\n")
        f.write("# 3. Review and apply renames\n")
        f.write("open ~/Music/TRANSCRIPTION_AND_RENAME_RESULTS.csv\n")
        f.write("```\n\n")
        
        f.write("### Phase 2: Organization\n")
        f.write("```bash\n")
        f.write("# 1. Remove duplicates\n")
        f.write("python3 ~/advanced_toolkit/smart_duplicate_remover.py\n\n")
        f.write("# 2. Organize downloads\n")
        f.write("python3 ~/Music/ORGANIZE_SUNO_DOWNLOADS.py\n\n")
        f.write("# 3. Add metadata tags\n")
        f.write("python3 ~/advanced_toolkit/batch_add_metadata.py\n")
        f.write("```\n\n")
        
        f.write("### Phase 3: Content Matching\n")
        f.write("```bash\n")
        f.write("# Match all content\n")
        f.write("python3 ~/advanced_toolkit/deep_content_matching.py\n\n")
        f.write("# Expand bundles\n")
        f.write("python3 ~/advanced_toolkit/expand_song_bundles.py\n")
        f.write("```\n\n")
        
        f.write("### Phase 4: Final Integration\n")
        f.write("```bash\n")
        f.write("# Rebuild unified catalog with all updates\n")
        f.write("python3 ~/advanced_toolkit/create_unified_master_catalog.py\n\n")
        f.write("# Final reanalysis\n")
        f.write("python3 ~/advanced_toolkit/comprehensive_mp3_reanalysis.py\n")
        f.write("```\n\n")
        
        f.write("---\n\n")
        f.write("## ?? Current Reports Available\n\n")
        f.write("- `UNIFIED_MASTER_CATALOG.csv` - Main catalog (7,120 files)\n")
        f.write("- `COMPREHENSIVE_MP3_REANALYSIS.csv` - Full analysis (1,256 MP3s)\n")
        f.write("- `FILES_NEEDING_TRANSCRIPTION_TO_RENAME.csv` - Bad filenames (5,709 files)\n")
        f.write("- `DEEP_SCAN_*.csv` - Deep scan results (6,068 audio, 17,860 lyrics, etc.)\n")
        f.write("- `SONG_BUNDLES/` - 51 complete bundles\n\n")
        
        f.write("---\n\n")
        f.write("**Generated by Master Orchestrator**\n")
    
    print(f"? Workflow plan saved to: {workflow_output}\n")
    
    return workflow_output

def main():
    print("\n" + "??" * 40)
    print("  MASTER ORCHESTRATOR")
    print("  Using ALL resources + API keys + fancy tools")
    print("??" * 40)
    
    # Load API keys from ~/.env.d/
    api_keys = load_api_keys()
    
    # Load all fancy tools
    tools = load_all_tools()
    
    # Load existing workflows
    workflows = load_existing_workflows()
    
    # Create master workflow plan
    workflow_plan = create_master_workflow_plan()
    
    # Final summary
    print("=" * 80)
    print("  ? MASTER ORCHESTRATOR INITIALIZED")
    print("=" * 80 + "\n")
    
    print("Resources loaded:")
    print(f"  ?? API keys: {len(api_keys)}")
    print(f"  ???  Python tools: {sum(len(t) for t in tools.values())}")
    print(f"  ?? Existing workflows: {len(workflows)}")
    print()
    
    print("What you have:")
    print("  ? 7,120 audio files cataloged")
    print("  ? 1,088 YOUR original songs")
    print("  ? 17,860 lyrics files found")
    print("  ? 1,143 prompt files found")
    print("  ? 51 complete song bundles")
    print("  ? 638 duplicates identified")
    print()
    
    print("Ready to:")
    print("  1. Transcribe files with bad names")
    print("  2. Rename based on transcription")
    print("  3. Remove duplicates")
    print("  4. Organize into albums")
    print("  5. Create complete bundles")
    print()
    
    print(f"?? Full workflow plan: {workflow_plan}")
    print(f"\nOpen: open '{workflow_plan}'")

if __name__ == '__main__':
    main()

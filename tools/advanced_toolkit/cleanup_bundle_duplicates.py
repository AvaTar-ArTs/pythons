#!/usr/bin/env python3
"""
Clean Up Bundle Duplicates
Remove full copied files now that we have extracted content
Keep only: AUDIO, EXTRACTED_CONTENT.txt, _bundle_info.json, README.txt
"""

from pathlib import Path

def main():
    print("\n" + "??" * 40)
    print("  CLEAN UP BUNDLE DUPLICATES")
    print("  Remove full files, keep extracted content")
    print("??" * 40 + "\n")
    
    bundles_root = Path.home() / 'Music/nocTurneMeLoDieS/SONG_BUNDLES'
    
    if not bundles_root.exists():
        print("? SONG_BUNDLES directory not found")
        return
    
    # Files to keep in each bundle
    keep_patterns = [
        'AUDIO -',           # Audio files
        'EXTRACTED_CONTENT', # Our smart extraction
        '_bundle_info',      # Metadata
        'README'             # Human-readable info
    ]
    
    print("Scanning bundles for cleanup...\n")
    
    results = {
        'bundles_scanned': 0,
        'files_to_remove': 0,
        'space_saved': 0
    }
    
    files_to_remove = []
    
    for bundle_dir in sorted(bundles_root.iterdir()):
        if not bundle_dir.is_dir() or bundle_dir.name.startswith('.'):
            continue
        
        results['bundles_scanned'] += 1
        
        for file in bundle_dir.iterdir():
            if file.is_file():
                # Check if this file should be kept
                should_keep = any(pattern in file.name for pattern in keep_patterns)
                
                if not should_keep:
                    files_to_remove.append(file)
                    results['files_to_remove'] += 1
                    results['space_saved'] += file.stat().st_size
    
    if not files_to_remove:
        print("? Bundles are already clean!\n")
        return
    
    print(f"Found {results['files_to_remove']} files to remove")
    print(f"Space to reclaim: {results['space_saved'] / 1024 / 1024:.2f} MB\n")
    
    # Show sample
    print("=" * 80)
    print("  SAMPLE FILES TO REMOVE (first 20)")
    print("=" * 80 + "\n")
    
    for file in files_to_remove[:20]:
        print(f"  {file.parent.name}/{file.name}")
    
    if len(files_to_remove) > 20:
        print(f"  ... and {len(files_to_remove) - 20} more\n")
    else:
        print()
    
    print("=" * 80)
    print("  REMOVING FILES")
    print("=" * 80 + "\n")
    
    removed = 0
    failed = 0
    
    for file in files_to_remove:
        try:
            file.unlink()
            removed += 1
        except Exception as e:
            print(f"? Failed to remove: {file.name}")
            failed += 1
    
    print(f"? Removed {removed} files")
    if failed:
        print(f"? Failed to remove {failed} files")
    print()
    
    # Verify bundles
    print("=" * 80)
    print("  BUNDLE VERIFICATION")
    print("=" * 80 + "\n")
    
    print("Each bundle should now contain:")
    print("  ? AUDIO - [song].mp3 (or .wav)")
    print("  ? EXTRACTED_CONTENT.txt (all relevant content)")
    print("  ? _bundle_info.json (metadata)")
    print("  ? README.txt (human-readable)")
    print()
    
    # Check a few bundles
    sample_bundles = list(bundles_root.iterdir())[:5]
    for bundle in sample_bundles:
        if bundle.is_dir() and not bundle.name.startswith('.'):
            files = list(bundle.iterdir())
            print(f"{bundle.name}:")
            print(f"  Files: {len(files)}")
            for f in sorted(files):
                print(f"    ? {f.name}")
            print()
    
    print("=" * 80)
    print("  ? CLEANUP COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"Bundles cleaned: {results['bundles_scanned']}")
    print(f"Files removed: {removed}")
    print(f"Space reclaimed: {results['space_saved'] / 1024 / 1024:.2f} MB")
    print()
    
    print("Benefits:")
    print("  ? No duplicate content (full files removed)")
    print("  ? Only relevant extracted content kept")
    print("  ? Smaller, cleaner bundles")
    print("  ? Everything still accessible in EXTRACTED_CONTENT.txt")
    print()
    
    print(f"All bundles: open '{bundles_root}'")

if __name__ == '__main__':
    main()

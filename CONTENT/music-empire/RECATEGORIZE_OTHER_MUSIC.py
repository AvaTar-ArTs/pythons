#!/usr/bin/env python3
"""
?? Recategorize OTHER_MUSIC
============================

Finds YOUR files that were misclassified as "other":
- InVideo AI content (YOURS!)
- AvatarArts content (YOURS!)
- nocTurneMeLoDieS content (YOURS!)
- Moves them to YOUR_SUNO_SONGS

Leaves only truly other people's music in OTHER_MUSIC.

Author: Steven Chaplinski
Date: November 4, 2025
"""

import shutil
from pathlib import Path
from datetime import datetime

class MusicRecategorizer:
    """Recategorize misclassified music"""
    
    def __init__(self):
        self.other_dir = Path.home() / 'Music' / 'nocTurneMeLoDieS' / 'FINAL_ORGANIZED' / 'OTHER_MUSIC'
        self.suno_dir = Path.home() / 'Music' / 'nocTurneMeLoDieS' / 'FINAL_ORGANIZED' / 'YOUR_SUNO_SONGS'
        
        self.stats = {
            'total_checked': 0,
            'moved_to_suno': 0,
            'stayed_other': 0
        }
        
        # Indicators that file is YOURS
        self.your_indicators = [
            'invideo',  # InVideo AI content
            'avatararts',
            'nocturne',
            'trashcat',
            'suno',
            'moonlit',
            'junkyard',
            'alley',
            'feather fang',
            'petals fall',
            'as a man thinketh',  # Your content
        ]
        
        # Indicators that file is NOT yours
        self.not_yours_indicators = [
            'jay brannan',
            'murray kyle',
            'dispatch',
            'netflix',
            'official music video',
            'official audio',
            'podcast',
            '[',  # YouTube video IDs
            'towa tei',
            'dr. joseph',
        ]
    
    def is_yours(self, filename: str) -> tuple:
        """Check if file is yours"""
        
        filename_lower = filename.lower()
        
        # First check if definitely NOT yours
        for indicator in self.not_yours_indicators:
            if indicator in filename_lower:
                return False, f"Not yours: {indicator}"
        
        # Then check if it's yours
        for indicator in self.your_indicators:
            if indicator in filename_lower:
                return True, f"Yours: {indicator}"
        
        # If unsure, keep in OTHER
        return False, "Unknown"
    
    def recategorize(self):
        """Recategorize files"""
        
        print("?? RECATEGORIZING OTHER_MUSIC")
        print("=" * 70)
        print()
        
        if not self.other_dir.exists():
            print("? OTHER_MUSIC folder not found")
            return
        
        print(f"?? Scanning: {self.other_dir.name}\n")
        
        # Get all audio files
        audio_files = []
        for ext in ['.mp3', '.wav', '.m4a', '.flac', '.aac']:
            audio_files.extend(self.other_dir.glob(f'*{ext}'))
        
        print(f"   Found {len(audio_files)} files to check\n")
        
        self.stats['total_checked'] = len(audio_files)
        
        # Check each file
        yours = []
        not_yours = []
        
        for i, filepath in enumerate(audio_files):
            is_your_file, reason = self.is_yours(filepath.name)
            
            if is_your_file:
                yours.append({'path': filepath, 'reason': reason})
            else:
                not_yours.append({'path': filepath, 'reason': reason})
            
            if (i + 1) % 100 == 0:
                print(f"   Checked {i + 1}/{len(audio_files)}...", end='\r')
        
        print(f"   ? Checked all {len(audio_files)} files" + " " * 20)
        
        print(f"\n?? Results:")
        print(f"   ? YOURS: {len(yours)}")
        print(f"   ?? Other: {len(not_yours)}")
        
        # Show samples
        print(f"\n?? Sample YOUR files found in OTHER_MUSIC:")
        for i, item in enumerate(yours[:20], 1):
            print(f"   {i:2d}. {item['path'].name}")
            print(f"       ? {item['reason']}")
        
        if len(yours) > 20:
            print(f"\n   ... and {len(yours) - 20} more!")
        
        # Move YOUR files
        if yours:
            print(f"\n?? Moving YOUR files to YOUR_SUNO_SONGS...")
            
            for item in yours:
                try:
                    source = item['path']
                    target = self.suno_dir / source.name
                    
                    # Handle conflicts
                    if target.exists():
                        stem = source.stem
                        ext = source.suffix
                        counter = 1
                        while target.exists():
                            target = self.suno_dir / f"{stem}_{counter}{ext}"
                            counter += 1
                    
                    shutil.move(str(source), str(target))
                    self.stats['moved_to_suno'] += 1
                    
                    if self.stats['moved_to_suno'] % 50 == 0:
                        print(f"      Moved {self.stats['moved_to_suno']}/{len(yours)}...", end='\r')
                
                except Exception as e:
                    pass
            
            print(f"      ? Moved {self.stats['moved_to_suno']} files" + " " * 20)
        
        self.stats['stayed_other'] = len(not_yours)
        
        # Summary
        print(f"\n{'=' * 70}")
        print("?? RECATEGORIZATION COMPLETE!")
        print("=" * 70)
        
        print(f"\n?? Final counts:")
        print(f"   ? YOUR SUNO SONGS: {self.stats['moved_to_suno']} files moved")
        print(f"   ?? OTHER MUSIC: {self.stats['stayed_other']} files remain")
        
        # New totals
        suno_count = len(list(self.suno_dir.glob('*.mp3'))) + len(list(self.suno_dir.glob('*.wav'))) + len(list(self.suno_dir.glob('*.m4a')))
        other_count = len(list(self.other_dir.glob('*.mp3'))) + len(list(self.other_dir.glob('*.wav'))) + len(list(self.other_dir.glob('*.m4a')))
        
        print(f"\n?? New totals:")
        print(f"   YOUR_SUNO_SONGS: {suno_count} files")
        print(f"   OTHER_MUSIC: {other_count} files")
        
        print(f"\n?? You now have {suno_count} Suno songs!")
        print(f"   Can create ~{suno_count // 24} albums!")
        
        # Create log
        log_file = Path.home() / 'workspace' / 'music-empire' / f'RECATEGORIZATION_LOG_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        
        with open(log_file, 'w') as f:
            f.write("?? RECATEGORIZATION LOG\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Moved to YOUR_SUNO_SONGS ({len(yours)}):\n\n")
            for item in yours:
                f.write(f"  ? {item['path'].name}\n")
                f.write(f"    {item['reason']}\n\n")
        
        print(f"\n?? Log saved: {log_file.name}")


def main():
    recategorizer = MusicRecategorizer()
    recategorizer.recategorize()


if __name__ == '__main__':
    main()

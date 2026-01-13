#!/usr/bin/env python3
"""
📦 FIX MISPLACED FILES
Move audio/video/image files to correct categories
"""

import shutil
from pathlib import Path

class MisplacedFixer:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)

    def fix_misplaced_files(self):
        """Find and fix misplaced files"""
        print("🔍 Finding misplaced files...\n")

        files = [f for f in self.pythons_dir.rglob('*.py')
                 if '_archive' not in str(f) and '2T-Xx-python' not in str(f)
                 and '.venv' not in str(f) and '.history' not in str(f)]

        moves = []

        for f in files:
            name = f.name.lower()
            current_path = str(f.parent).lower()

            # Determine correct location
            target = None

            # Audio files
            if any(x in name for x in ['audio', 'mp3', 'wav', 'sound', 'music', 'tts', 'speech']):
                if 'audio' not in current_path:
                    if 'transcribe' in name or 'transcript' in name or 'speech-to-text' in name or 'whisper' in name:
                        target = self.pythons_dir / 'audio_transcription'
                    else:
                        target = self.pythons_dir / 'audio_generation'

            # Video files
            elif any(x in name for x in ['video', 'mp4', 'movie', 'clip']):
                if 'video' not in current_path and 'media' not in current_path:
                    target = self.pythons_dir / 'MEDIA_PROCESSING/video_tools'

            # Image files
            elif any(x in name for x in ['image', 'img', 'photo', 'picture']):
                if 'image' not in current_path and 'media' not in current_path:
                    target = self.pythons_dir / 'MEDIA_PROCESSING/image_tools'

            if target:
                moves.append((f, target))

        print(f"Found {len(moves)} files to move\n")

        # Execute moves
        moved = 0
        skipped = 0

        for src, target_dir in moves:
            target_dir.mkdir(parents=True, exist_ok=True)
            target_file = target_dir / src.name

            if target_file.exists():
                skipped += 1
                continue

            try:
                shutil.move(str(src), str(target_file))
                moved += 1

                if moved % 20 == 0:
                    print(f"   ... moved {moved} files")
            except Exception as e:
                pass

        print(f"\n✅ Moved {moved} files to correct locations")
        print(f"⚠️  Skipped {skipped} files (already exist)\n")

        return moved

    def remove_empty_folders(self):
        """Remove empty folders"""
        print("🗑️  Removing empty folders...\n")

        # Find empty folders (bottom-up)
        removed = 0

        for depth in range(10, 0, -1):  # Start from deepest
            for folder in self.pythons_dir.rglob('*'):
                if not folder.is_dir():
                    continue

                if '_archive' in str(folder) or '2T-Xx-python' in str(folder):
                    continue

                # Check if empty
                try:
                    contents = list(folder.iterdir())
                    if not contents:
                        folder.rmdir()
                        removed += 1

                        if removed % 10 == 0:
                            print(f"   ... removed {removed} folders")
                except:
                    pass

        print(f"✅ Removed {removed} empty folders\n")
        return removed


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     📦 FIX MISPLACED FILES                                        ║
║     Move files to correct categories + remove empty folders      ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    fixer = MisplacedFixer()

    print("This will:")
    print("  • Move audio files → audio_generation/ or audio_transcription/")
    print("  • Move video files → MEDIA_PROCESSING/video_tools/")
    print("  • Move image files → MEDIA_PROCESSING/image_tools/")
    print("  • Remove all empty folders")
    print()

    confirm = input("Type 'RELOCATE' to fix: ")

    if confirm == 'RELOCATE':
        moved = fixer.fix_misplaced_files()
        removed = fixer.remove_empty_folders()
        print(f"🎉 Cleanup complete! Moved {moved} files, removed {removed} empty folders!")
    else:
        print("\n❌ Cancelled")


if __name__ == "__main__":
    main()


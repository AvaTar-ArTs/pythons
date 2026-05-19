#!/usr/bin/env python3
"""
Script to move music content from external volumes to the appropriate album directories
in the nocTurneMeLoDieS album organization system.
This version focuses on specific known directories for efficiency.
"""

import logging
import shutil
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class MusicVolumeOrganizer:
    def __init__(self):
        self.source_directories = {
            "/Volumes/DeVonDaTa/gDrive/MyMusic": [
                "HeartBreak Alley.mp3",
                "Junkyard Kings.mp3",
                "Heroes RiSe.mp3",
                "Echoes of Moonlight.mp3",
                "in This aLLey Where i HiDe.mp3",
                "Moonlight Night.mp3",
                "Moonlight's Pomise.mp3",
                "Broken Dreams.mp3",
                "Cannon Blastin.mp3",
                "Dumpster Brew.mp3",
                "Grabage Grove.mp3",
                "Urban Raccoon Party.mp3",
                "Concrete Jungle Rumble.mp3",
                "Bite in the Night.mp3",
                "Virtual Pulse.mp3",
                "No more love songs.mp3",
                "Sammy's SereNade.mp3",
            ],
            "/Volumes/DeVonDaTa/gDrive/TrashCaTs-and_BeYond/mp3": [
                "Beautiful Mess.mp3",
                "Beautiful-Mess.mp3",
                "Blues in the Alley Haunted Strings Nocturnal Notes.mp3",
                "blues-in-the-alley-haunted-strings-nocturnal-notes.mp3",
                "Blues-in-the-Alley-Haunted-Strings-Nocturnal-Notes2.mp3",
                "Blues-in-the-Moonlit-Nights.mp3",
                "Dance-Like-Nobody's-Watching.mp3",
                "Echoes of Yesterday.mp3",
                "enchanted-woods.mp3",
                "Enchanted-Woods2.mp3",
                "Heartbeats-in-the-Dark.mp3",
                "Howligritty-Nights.mp3",
                "Howling-Cat's-Song.mp3",
                "in-This-aLLey-Where-i-HiDe.mp3",
                "in-This-aLLey-Where-i-HiDe2.mp3",
                "Junky-Symphony.mp3",
                "Junky-Symphony2.mp3",
                "Junkyard-Dream-Symphony5.mp3",
                "Junkyard-Moon-Symphony4.mp3",
                "junkyard-symphony-scraps.mp3",
                "Kings and Queens of Litter.mp3",
                "Love in Imperfection.mp3",
                "Love-in-Imperfection.mp3",
                "Love-is-Rubbish,-and-Rubbish-is-Love.mp3",
                "Marching-ever-forward-neath-the-wooded-s.mp3",
                "Marching-ever-forward-neath-the-wooded-s2.mp3",
                "Marching-Shadows-(Cover).mp3",
                "Marching-Shadows.mp3",
                "Moonly Alley3.mp3",
                "Moonly-Alley-(1).mp3",
                "Moonly-Alley-by-_avatararts-_-Suno.mp3",
                "Moonly-Alley-Serenade.mp3",
                "Moonly-Alley2.mp3",
                "Moonly-Alley4.mp3",
                "Neon Whisper.mp3",
                "Neon Whisper (1).mp3",
                "Neon Whisper (2).mp3",
                "No-More-Love-Songs.mp3",
                "Recycled-Symphony2.mp3",
                "Royalty-of-Refuse.mp3",
                "Rubbish-Love.mp3",
                "Shadow-Messages.mp3",
                "The-Alley-King.mp3",
                "The-Raccoon's-Revelry.mp3",
                "The-Sound-of-Ancestors.mp3",
                "The-Sound-of-Ancestors2.mp3",
                "Whisper of the Willow.mp3",
                "Whisper-of-the-Willow.mp3",
            ],
        }

        self.target_base = "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/ALBUMS"

        # Define album mappings for known themes
        self.album_mappings = {
            # Alley-related
            "In_This_Alley_Where_I_Hide": [
                "in This aLLey Where i HiDe.mp3",
                "in-This-aLLey-Where-i-HiDe.mp3",
                "in-This-aLLey-Where-i-HiDe2.mp3",
            ],
            # Beautiful-related
            "Beautiful_Mess": ["Beautiful Mess.mp3", "Beautiful-Mess.mp3"],
            # Echoes-related
            "Echoes_of_Moonlight": ["Echoes of Moonlight.mp3"],
            "Echoes_of_Yesterday": ["Echoes of Yesterday.mp3"],
            # Heartbeat-related
            "Heartbeats_in_the_Dark": ["Heartbeats-in-the-Dark.mp3"],
            # Junkyard-related
            "Junkyard_Symphony": [
                "Junky-Symphony.mp3",
                "Junky-Symphony2.mp3",
                "Junkyard-Dream-Symphony5.mp3",
                "Junkyard-Moon-Symphony4.mp3",
                "junkyard-symphony-scraps.mp3",
            ],
            "Junkyard_Kings": ["Junkyard Kings.mp3"],
            # Hero-related
            "Heroes_Rise_Villains_Overthrow": ["Heroes RiSe.mp3"],
            # Kings and Queens of Litter
            "Kings_And_Queens_Of_Litter": ["Kings and Queens of Litter.mp3"],
            # Moon-related
            "Moonlight_Night": ["Moonlight Night.mp3"],
            "Moonlights_Pomise": ["Moonlight's Pomise.mp3"],
            # Sound of ancestors
            "The_Sound_Of_Ancestors": [
                "The-Sound-of-Ancestors.mp3",
                "The-Sound-of-Ancestors2.mp3",
            ],
            # Willow-related
            "Whisper_of_the_Willow": [
                "Whisper of the Willow.mp3",
                "Whisper-of-the-Willow.mp3",
            ],
            # Alley/Hide-related
            "Blues_in_the_Alley_Haunted_Strings_Nocturnal_Notes": [
                "Blues in the Alley Haunted Strings Nocturnal Notes.mp3",
                "blues-in-the-alley-haunted-strings-nocturnal-notes.mp3",
                "Blues-in-the-Alley-Haunted-Strings-Nocturnal-Notes2.mp3",
            ],
            # Enchanted Woods
            "Enchanted_Woods_(1)": ["Enchanted-Woods2.mp3", "enchanted-woods.mp3"],
            # Raccoon-related
            "Urban_Raccoon_Party": [
                "Urban Raccoon Party.mp3",
                "The-Raccoon's-Revelry.mp3",
            ],
            # Love/imperfection
            "Love_in_Imperfection": [
                "Love in Imperfection.mp3",
                "Love-in-Imperfection.mp3",
            ],
            # Rubbish/Trash
            "Rubbish_Love": [
                "Rubbish-Love.mp3",
                "Love-is-Rubbish,-and-Rubbish-is-Love.mp3",
            ],
            # Royalty of refuse
            "Royalty_Of_Refuse": ["Royalty-of-Refuse.mp3"],
            # Dance
            "Dance_Like_Nobodys_Watching": ["Dance-Like-Nobody's-Watching.mp3"],
            # Blues in moonlit nights
            "Blues_in_the_Moonlit_Nights": ["Blues-in-the-Moonlit-Nights.mp3"],
            # No more love songs
            "No_More_Love_Songs": ["No-More-Love-Songs.mp3", "No more love songs.mp3"],
            # Recycled symphony
            "Recycled_Symphony": ["Recycled-Symphony2.mp3"],
            # Shadow messages
            "Shadow_Messages226": ["Shadow-Messages.mp3"],  # Using an existing album name pattern
            # Alley king
            "The_Alley_King": ["The-Alley-King.mp3"],
            # Marching
            "Marching_Ever_Forward": [
                "Marching-ever-forward-neath-the-wooded-s.mp3",
                "Marching-ever-forward-neath-the-wooded-s2.mp3",
                "Marching-Shadows.mp3",
                "Marching-Shadows-(Cover).mp3",
            ],
            # Cat-related
            "Howligritty_Nights": ["Howligritty-Nights.mp3", "Howling-Cat's-Song.mp3"],
            # Broken dreams
            "Broken_Dreams": ["Broken Dreams.mp3"],
            # Concrete jungle
            "Concrete_Jungle_Rumble": ["Concrete Jungle Rumble.mp3"],
            # Dumpster
            "Dumpster_Brew": ["Dumpster Brew.mp3"],
            # Garbage
            "Grabage_Grove": ["Grabage Grove.mp3"],
            # Cannon blastin'
            "Cannon_Blastin": ["Cannon Blastin.mp3"],
            # Bite in the night
            "Bite_In_The_Night_Collection": ["Bite in the Night.mp3"],
            # Virtual pulse
            "Virtual_Pulse": ["Virtual Pulse.mp3"],  # Creating new album if doesn't exist
            # Neon whisper
            "Neon_Whisper": [  # Creating new album if doesn't exist
                "Neon Whisper.mp3",
                "Neon Whisper (1).mp3",
                "Neon Whisper (2).mp3",
            ],
            # Sammy-related (Moonly Alley tracks) - mapping to Sammys_Serenade
            "Sammys_Serenade": [
                "Moonly Alley3.mp3",
                "Moonly-Alley-(1).mp3",
                "Moonly-Alley-by-_avatararts-_-Suno.mp3",
                "Moonly-Alley-Serenade.mp3",
                "Moonly-Alley2.mp3",
                "Moonly-Alley4.mp3",
                "Sammy's SereNade.mp3",
            ],
        }

    def find_existing_album_dirs(self) -> dict:
        """Find all existing album directories in the target base."""
        album_dirs = {}

        for item in Path(self.target_base).iterdir():
            if item.is_dir():
                dir_name = item.name

                # Look for exact matches with our album mappings
                for album_key in self.album_mappings.keys():
                    if album_key == dir_name or album_key.replace("_", " ") in dir_name:
                        album_dirs[album_key] = item

        return album_dirs

    def run(self, dry_run: bool = True):
        """Execute the organization process."""
        logger.info("Starting music volume organization process...")

        # Find existing album directories
        logger.info("Finding existing album directories...")
        album_dirs = self.find_existing_album_dirs()
        logger.info(f"Found {len(album_dirs)} matching album directories")

        # Track planned moves
        planned_moves = []

        # Process each source directory
        for source_dir, expected_files in self.source_directories.items():
            source_path = Path(source_dir)
            if not source_path.exists():
                logger.warning(f"Source directory does not exist: {source_path}")
                continue

            logger.info(f"Processing source directory: {source_path}")

            # For each expected file, find it and determine where to move it
            for expected_file in expected_files:
                source_file = source_path / expected_file

                if not source_file.exists():
                    # Try to find a file with similar name (case-insensitive)
                    found_file = None
                    for file_in_dir in source_path.iterdir():
                        if file_in_dir.is_file() and expected_file.lower() in file_in_dir.name.lower():
                            found_file = file_in_dir
                            break

                    if not found_file:
                        logger.warning(f"Expected file not found: {source_file}")
                        continue
                    else:
                        source_file = found_file
                        logger.info(f"Found similar file: {source_file}")

                # Determine target album directory
                target_album = None
                for album_key, file_list in self.album_mappings.items():
                    if expected_file in file_list:
                        target_album = album_key
                        break

                if not target_album:
                    logger.warning(f"No album mapping found for: {expected_file}")
                    continue

                # Determine target directory
                if target_album in album_dirs:
                    target_dir = album_dirs[target_album]
                else:
                    # Create new album directory
                    target_dir = Path(self.target_base) / target_album
                    if not dry_run:
                        target_dir.mkdir(exist_ok=True)
                    logger.info(f"Created/using new album directory: {target_dir}")

                target_file = target_dir / source_file.name

                # Plan the move
                planned_moves.append((source_file, target_file))
                logger.info(f"Planned move: {source_file} -> {target_file}")

        if dry_run:
            logger.info(f"\nDRY RUN MODE - Would perform {len(planned_moves)} moves:")
            for src, dst in planned_moves:
                print(f"  {src} -> {dst}")

            # Show summary by album
            album_summary = {}
            for src, dst in planned_moves:
                album_name = dst.parent.name
                if album_name not in album_summary:
                    album_summary[album_name] = 0
                album_summary[album_name] += 1

            print("\nSummary by album:")
            for album, count in album_summary.items():
                print(f"  {album}: {count} files")

        else:
            logger.info(f"Performing {len(planned_moves)} actual moves...")

            successful_moves = 0
            failed_moves = 0

            for src, dst in planned_moves:
                try:
                    # Make sure target directory exists
                    dst.parent.mkdir(parents=True, exist_ok=True)

                    # Copy file to destination
                    shutil.copy2(src, dst)
                    logger.info(f"Moved: {src} -> {dst}")
                    successful_moves += 1
                except Exception as e:
                    logger.error(f"Failed to move {src} to {dst}: {str(e)}")
                    failed_moves += 1

            logger.info(f"Move operation completed: {successful_moves} successful, {failed_moves} failed")

    def get_statistics(self):
        """Get statistics about the source files."""
        stats = {}

        for source_dir, expected_files in self.source_directories.items():
            source_path = Path(source_dir)
            if source_path.exists():
                actual_files = list(source_path.iterdir())
                stats[source_dir] = {
                    "expected_count": len(expected_files),
                    "actual_count": len(actual_files),
                    "expected_files": expected_files,
                    "actual_files": [f.name for f in actual_files if f.is_file()],
                }

        return stats


def main():
    organizer = MusicVolumeOrganizer()

    # Show statistics first
    stats = organizer.get_statistics()
    print("Source Directory Statistics:")
    for dir_path, dir_stats in stats.items():
        print(f"  {dir_path}: {dir_stats['expected_count']} expected, {dir_stats['actual_count']} actual files")

    print("\nRunning in DRY RUN mode to show planned operations...")
    organizer.run(dry_run=True)

    print("\nRunning in ACTUAL mode to perform the operations...")
    organizer.run(dry_run=False)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script to move music content from external volumes to the appropriate album directories
in the nocTurneMeLoDieS album organization system.
"""

import logging
import shutil
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class MusicVolumeOrganizer:
    def __init__(self):
        self.source_volumes = ["/Volumes/DeVonDaTa", "/Volumes/2T-Xx"]

        self.target_base = "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/ALBUMS"
        self.cover_art_base = "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/COVER_ART"

        # Define album mappings for known themes
        self.album_mappings = {
            # Alley-related
            "alley": [
                "HeartBreak Alley.mp3",
                "in This aLLey Where i HiDe.mp3",
                "in-This-aLLey-Where-i-HiDe.mp3",
                "in-This-aLLey-Where-i-HiDe2.mp3",
                "Moonly-Alley-by-_avatararts-_-Suno.mp3",
                "Moonly Alley3.mp3",
                "Moonly-Alley-(1).mp3",
                "Moonly-Alley-Serenade.mp3",
                "Moonly-Alley2.mp3",
                "Moonly-Alley4.mp3",
            ],
            # Beautiful-related
            "beautiful_mess": ["Beautiful Mess.mp3", "Beautiful-Mess.mp3"],
            # Echoes-related
            "echoes_of_moonlight": ["Echoes of Moonlight.mp3"],
            "echoes_of_yesterday": ["Echoes of Yesterday.mp3"],
            # Heartbeat-related
            "heartbeats_in_the_dark": ["Heartbeats-in-the-Dark.mp3"],
            # Junkyard-related
            "junkyard_symphony": [
                "Junky-Symphony.mp3",
                "Junky-Symphony2.mp3",
                "Junkyard-Dream-Symphony5.mp3",
                "Junkyard-Moon-Symphony4.mp3",
                "junkyard-symphony-scraps.mp3",
            ],
            "junkyard_kings": ["Junkyard Kings.mp3"],
            # Hero-related
            "heroes_rise": ["Heroes RiSe.mp3"],
            # Kings and Queens of Litter
            "kings_and_queens_of_litter": ["Kings and Queens of Litter.mp3"],
            # Moon-related
            "moonlight": ["Moonlight Night.mp3", "Moonlight's Pomise.mp3"],
            # Sound of ancestors
            "the_sound_of_ancestors": [
                "The-Sound-of-Ancestors.mp3",
                "The-Sound-of-Ancestors2.mp3",
            ],
            # Willow-related
            "whisper_of_the_willow": [
                "Whisper of the Willow.mp3",
                "Whisper-of-the-Willow.mp3",
            ],
            # Alley/Hide-related
            "blues_in_the_alley": [
                "Blues in the Alley Haunted Strings Nocturnal Notes.mp3",
                "blues-in-the-alley-haunted-strings-nocturnal-notes.mp3",
                "Blues-in-the-Alley-Haunted-Strings-Nocturnal-Notes2.mp3",
            ],
            # Enchanted Woods
            "enchanted_woods": ["Enchanted-Woods2.mp3", "enchanted-woods.mp3"],
            # Raccoon-related
            "raccoon": ["Urban Raccoon Party.mp3", "The-Raccoon's-Revelry.mp3"],
            # Love/imperfection
            "love_in_imperfection": [
                "Love in Imperfection.mp3",
                "Love-in-Imperfection.mp3",
            ],
            # Rubbish/Trash
            "rubbish_love": [
                "Rubbish-Love.mp3",
                "Love-is-Rubbish,-and-Rubbish-is-Love.mp3",
            ],
            # Royalty of refuse
            "royalty_of_refuse": ["Royalty-of-Refuse.mp3"],
            # Dance
            "dance_like_nobody": ["Dance-Like-Nobody's-Watching.mp3"],
            # Blues in moonlit nights
            "blues_in_moonlit_nights": ["Blues-in-the-Moonlit-Nights.mp3"],
            # No more love songs
            "no_more_love_songs": ["No-More-Love-Songs.mp3"],
            # Recycled symphony
            "recycled_symphony": ["Recycled-Symphony2.mp3"],
            # Shadow messages
            "shadow_messages": ["Shadow-Messages.mp3"],
            # Alley king
            "the_alley_king": ["The-Alley-King.mp3"],
            # Marching
            "marching": [
                "Marching-ever-forward-neath-the-wooded-s.mp3",
                "Marching-ever-forward-neath-the-wooded-s2.mp3",
                "Marching-Shadows.mp3",
                "Marching-Shadows-(Cover).mp3",
            ],
            # Cat-related
            "howling_cats": ["Howligritty-Nights.mp3", "Howling-Cat's-Song.mp3"],
            # Broken dreams
            "broken_dreams": ["Broken Dreams.mp3"],
            # Concrete jungle
            "concrete_jungle": ["Concrete Jungle Rumble.mp3"],
            # Dumpster
            "dumpster": ["Dumpster Brew.mp3"],
            # Garbage
            "garbage_grove": ["Grabage Grove.mp3"],
            # Cannon blastin'
            "cannon_blastin": ["Cannon Blastin.mp3"],
            # Bite in the night
            "bite_in_the_night": ["Bite in the Night.mp3"],
            # Virtual pulse
            "virtual_pulse": ["Virtual Pulse.mp3"],
            # Neon whisper
            "neon_whisper": [
                "Neon Whisper.mp3",
                "Neon Whisper (1).mp3",
                "Neon Whisper (2).mp3",
            ],
            # Sammy-related (Moonly Alley tracks)
            "sammys_serenade": [
                "Moonly Alley3.mp3",
                "Moonly-Alley-(1).mp3",
                "Moonly-Alley-by-_avatararts-_-Suno.mp3",
                "Moonly-Alley-Serenade.mp3",
                "Moonly-Alley2.mp3",
                "Moonly-Alley4.mp3",
            ],
        }

    def find_existing_album_dirs(self) -> dict[str, list[Path]]:
        """Find all existing album directories in the target base."""
        album_dirs = {}

        for item in Path(self.target_base).iterdir():
            if item.is_dir():
                dir_name = item.name.lower()

                # Look for matches with our album mappings
                for album_key in self.album_mappings.keys():
                    if album_key.replace("_", " ") in dir_name or album_key in dir_name:
                        if album_key not in album_dirs:
                            album_dirs[album_key] = []
                        album_dirs[album_key].append(item)

        return album_dirs

    def find_source_files(self) -> dict[str, list[Path]]:
        """Find all source files that match our album mappings."""
        source_files = {}

        for volume in self.source_volumes:
            volume_path = Path(volume)
            if not volume_path.exists():
                logger.warning(f"Volume {volume} does not exist, skipping...")
                continue

            # Search for music files in common locations
            search_paths = [
                volume_path / "gDrive" / "MyMusic",
                volume_path / "gDrive" / "TrashCaTs-and_BeYond" / "mp3",
                volume_path / "mp3",
                volume_path / "steven" / "Music" / "NocTurnE-meLoDieS",
                volume_path / "steven" / "Music" / "TrashyArTs" / "mp3",
                volume_path / "steven" / "Music" / "Suno-Music",
            ]

            for search_path in search_paths:
                if search_path.exists():
                    for file_path in search_path.rglob("*"):
                        if file_path.is_file() and file_path.suffix.lower() in [
                            ".mp3",
                            ".wav",
                            ".flac",
                            ".m4a",
                        ]:
                            # Check if this file matches any of our mappings
                            for album_key, file_names in self.album_mappings.items():
                                for expected_file in file_names:
                                    if expected_file.lower() in file_path.name.lower():
                                        if album_key not in source_files:
                                            source_files[album_key] = []
                                        source_files[album_key].append(file_path)

        return source_files

    def move_files_to_albums(
        self, source_files: dict[str, list[Path]], album_dirs: dict[str, list[Path]]
    ) -> list[tuple[Path, Path, str]]:
        """Move source files to appropriate album directories."""
        moves_performed = []

        for album_key, files in source_files.items():
            if album_key in album_dirs and album_dirs[album_key]:
                # Use the first matching album directory
                target_dir = album_dirs[album_key][0]

                for source_file in files:
                    target_file = target_dir / source_file.name

                    # Skip if file already exists at destination
                    if target_file.exists():
                        logger.info(f"File already exists at destination: {target_file}")
                        continue

                    try:
                        # Perform the copy operation
                        shutil.copy2(source_file, target_file)
                        logger.info(f"Moved {source_file} to {target_file}")
                        moves_performed.append((source_file, target_file, "COPIED"))
                    except Exception as e:
                        logger.error(f"Failed to move {source_file} to {target_file}: {str(e)}")
                        moves_performed.append((source_file, target_file, f"ERROR: {str(e)}"))
            else:
                logger.warning(f"No existing album directory found for {album_key}, creating new one...")

                # Create a new album directory
                new_album_dir = Path(self.target_base) / album_key.replace("_", " ").title().replace(" ", "_")
                new_album_dir.mkdir(exist_ok=True)

                for source_file in files:
                    target_file = new_album_dir / source_file.name

                    # Skip if file already exists at destination
                    if target_file.exists():
                        logger.info(f"File already exists at destination: {target_file}")
                        continue

                    try:
                        # Perform the copy operation
                        shutil.copy2(source_file, target_file)
                        logger.info(f"Moved {source_file} to {target_file} (new album)")
                        moves_performed.append((source_file, target_file, "COPIED_NEW_ALBUM"))
                    except Exception as e:
                        logger.error(f"Failed to move {source_file} to {target_file}: {str(e)}")
                        moves_performed.append((source_file, target_file, f"ERROR: {str(e)}"))

        return moves_performed

    def find_image_files(self) -> list[Path]:
        """Find all image files that could serve as cover art."""
        image_files = []

        for volume in self.source_volumes:
            volume_path = Path(volume)
            if not volume_path.exists():
                continue

            # Search for image files in common locations
            search_paths = [
                volume_path,
                volume_path / "gDrive",
                volume_path / "steven" / "Music",
                volume_path / "steven" / "Music" / "NocTurnE-meLoDieS",
                volume_path / "steven" / "Music" / "TrashyArTs" / "covers",
                volume_path / "steven" / "Music" / "Suno-Music",
            ]

            for search_path in search_paths:
                if search_path.exists():
                    for file_path in search_path.rglob("*"):
                        if file_path.is_file() and file_path.suffix.lower() in [
                            ".jpg",
                            ".jpeg",
                            ".png",
                        ]:
                            # Skip hidden files and system files
                            if not file_path.name.startswith("."):
                                image_files.append(file_path)

        return image_files

    def organize_cover_art(self, image_files: list[Path]) -> list[tuple[Path, Path, str]]:
        """Organize image files as cover art."""
        moves_performed = []

        for image_file in image_files:
            # Create a destination filename based on the image name
            dest_filename = image_file.name
            target_file = Path(self.cover_art_base) / dest_filename

            # If file exists, create a unique name
            counter = 1
            original_target = target_file
            while target_file.exists():
                stem = original_target.stem
                suffix = original_target.suffix
                target_file = Path(self.cover_art_base) / f"{stem}_{counter}{suffix}"
                counter += 1

            try:
                shutil.copy2(image_file, target_file)
                logger.info(f"Copied cover art {image_file} to {target_file}")
                moves_performed.append((image_file, target_file, "COVER_ART_COPIED"))
            except Exception as e:
                logger.error(f"Failed to copy cover art {image_file} to {target_file}: {str(e)}")
                moves_performed.append((image_file, target_file, f"COVER_ART_ERROR: {str(e)}"))

        return moves_performed

    def run(self, dry_run: bool = True):
        """Execute the organization process."""
        logger.info("Starting music volume organization process...")

        # Find existing album directories
        logger.info("Finding existing album directories...")
        album_dirs = self.find_existing_album_dirs()
        logger.info(f"Found {len(album_dirs)} matching album directories")

        # Find source files
        logger.info("Finding source files...")
        source_files = self.find_source_files()
        logger.info(f"Found {sum(len(files) for files in source_files.values())} source files to organize")

        # Find image files
        logger.info("Finding image files for cover art...")
        image_files = self.find_image_files()
        logger.info(f"Found {len(image_files)} image files for cover art")

        if dry_run:
            logger.info("DRY RUN MODE - No files will be moved")
            logger.info("Summary of planned operations:")

            for album_key, files in source_files.items():
                if album_key in album_dirs and album_dirs[album_key]:
                    target_dir = album_dirs[album_key][0]
                    logger.info(f"Would move {len(files)} files to {target_dir} for {album_key}")
                else:
                    new_album_name = album_key.replace("_", " ").title().replace(" ", "_")
                    logger.info(f"Would create new album '{new_album_name}' and move {len(files)} files")

            logger.info(f"Would copy {len(image_files)} image files to cover art directory")
            return

        # Perform the actual moves
        logger.info("Performing file moves...")
        music_moves = self.move_files_to_albums(source_files, album_dirs)

        logger.info("Organizing cover art...")
        cover_art_moves = self.organize_cover_art(image_files)

        # Log summary
        logger.info("Organization complete!")
        logger.info(f"Music files moved: {len(music_moves)}")
        logger.info(f"Cover art files moved: {len(cover_art_moves)}")

        # Save detailed log
        self.save_operation_log(music_moves + cover_art_moves)

    def save_operation_log(self, moves: list[tuple[Path, Path, str]]):
        """Save a detailed log of all operations performed."""
        log_path = Path("/Users/steven/Music/nocTurneMeLoDieS") / "external_volume_organization_log.txt"

        with open(log_path, "w") as f:
            f.write("External Volume Music Organization Log\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Date: {Path.cwd().stat().st_mtime}\n\n")

            for src, dst, status in moves:
                f.write(f"{status}: {src} -> {dst}\n")

        logger.info(f"Detailed log saved to {log_path}")


def main():
    organizer = MusicVolumeOrganizer()

    # First run in dry-run mode to show what would happen
    print("Running in DRY RUN mode to show planned operations...")
    organizer.run(dry_run=True)

    # Uncomment the next line to actually perform the operations
    # print("\nRunning in ACTUAL mode to perform the operations...")
    # organizer.run(dry_run=False)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""from pathlib import Path
import csv
import os
import re
import sys

from difflib import SequenceMatcher
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
MASTER METADATA APPLIER
=======================
Sources:
1. LOCAL INVENTORY: /Users/steven/clean/audio-11-28-21:09.csv
   - Contains: Filename, Duration (clean), File Size, Original Path
   - This is the SOURCE OF TRUTH for what files we actually have.

2. METADATA VAULTS:
   - suno_ultimate_master_combined.csv (Technical: UUID, Exact Duration, Genres, Date)
   - Discography ALL.csv (Creative: Analysis, Witty Comments, Info)

Process:
1. Load Local Inventory.
2. Load Metadata Vaults.
3. For each local file:
   - Find best match in Vaults (Title + Duration).
   - Merge metadata (Genre, Date, Comment).
   - Apply ID3 tags using Mutagen.
"""

# Paths
LOCAL_CSV = Path("/Users/steven/clean/audio-11-28-21:09.csv")
SUNO_CSV = Path(
    "/Users/steven/Music/nocTurneMeLoDieS/suno_ultimate_master_combined.csv",
)
DISCO_CSV = Path("/Users/steven/Music/nocTurneMeLoDieS/Discography ALL.csv")


class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


class MasterMetadataApplier:
    def __init__(self, live_run=False):
        self.live_run = live_run
        self.local_files = []
        self.metadata_vault = {}  # Key: Normalized Title
        self.uuid_map = {}  # Key: UUID

    def normalize_title(self, title):
        if not title:
            return ""
        # Remove extension
        title = re.sub(r"\.(mp3|wav)$", "", title, flags=re.I)
        # Remove duration suffixes like "345" or "0345" at end
        title = re.sub(r"\d{3,4}$", "", title)
        # Standardize
        title = re.sub(r"[^\w\s]", " ", title)
        return re.sub(r"\s+", " ", title).strip().lower()

    def parse_duration(self, dur_str):
        '\''Convert 'M:SS' to total seconds"""
        try:
            parts = dur_str.split(":")
            return int(parts[0]) * 60 + int(parts[1])
        except:
            return 0

    def load_data(self):
        print(f"{Colors.CYAN}Loading Data...{Colors.END}")

        # 1. Load Metadata Vaults first
        # Suno Master
        if SUNO_CSV.exists():
            with open(SUNO_CSV, encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row = {k.lstrip("\ufeff"): v for k, v in row.items()}
                    title = row.get("Song Name") or row.get("title")
                    uuid = row.get("idNumber") or row.get("id")

                    if not title:
                        continue

                    norm_title = self.normalize_title(title)
                    entry = {
                        "title": title,
                        "artist": row.get("Artist", "Avatar Arts"),
                        "genre": row.get("genres", ""),
                        "date": row.get("originDaTe", ""),
                        "duration_str": row.get("duration", ""),
                        "source": "suno",
                    }

                    if norm_title not in self.metadata_vault:
                        self.metadata_vault[norm_title] = entry

                    if uuid:
                        self.uuid_map[uuid] = entry

        # Discography
        if DISCO_CSV.exists():
            with open(DISCO_CSV, encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = row.get("Song Title")
                    if not title:
                        continue

                    norm_title = self.normalize_title(title)

                    # Update existing or create new
                    if norm_title in self.metadata_vault:
                        self.metadata_vault[norm_title]["comment"] = (
                            row.get("witty") or row.get("inFo") or ""
                        )[:200]
                    else:
                        self.metadata_vault[norm_title] = {
                            "title": title,
                            "artist": "Avatar Arts",
                            "comment": (row.get("witty") or row.get("inFo") or "")[
                                :200
                            ],
                            "source": "disco",
                        }

        print(
            f"Vault loaded: {len(self.metadata_vault)} titles, {len(self.uuid_map)} UUIDs",
        )

        # 2. Load Local Inventory
        if LOCAL_CSV.exists():
            with open(LOCAL_CSV, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.local_files.append(row)
            print(f"Local files loaded: {len(self.local_files)}")
        else:
            print(f"{Colors.RED}Error: Local inventory not found!{Colors.END}")
            sys.exit(1)

    def apply(self):
        print(f"\n{Colors.CYAN}Matching and Applying Metadata...{Colors.END}")

        matched_count = 0

        for file_data in self.local_files:
            original_path = Path(file_data["Original Path"])
            if not original_path.exists():
                continue

            filename = file_data["Filename"]
            local_norm_title = self.normalize_title(filename)
            local_dur_str = file_data["Duration"]  # "3:45"
            local_dur_sec = self.parse_duration(local_dur_str)

            best_match = None
            match_type = None

            # Strategy A: UUID in filename
            for uuid, meta in self.uuid_map.items():
                if uuid in filename:
                    best_match = meta
                    match_type = "UUID"
                    break

            # Strategy B: Exact Title
            if not best_match:
                if local_norm_title in self.metadata_vault:
                    best_match = self.metadata_vault[local_norm_title]
                    match_type = "Exact Title"

            # Strategy C: Fuzzy Title + Duration Check
            if not best_match:
                best_score = 0
                for key, meta in self.metadata_vault.items():
                    if len(key) < 4:
                        continue

                    # Title Sim
                    score = SequenceMatcher(None, local_norm_title, key).ratio()

                    # Duration Check (if available in vault)
                    vault_dur = self.parse_duration(meta.get("duration_str", ""))
                    dur_match = True
                    if vault_dur > 0 and abs(vault_dur - local_dur_sec) > 5:
                        dur_match = False  # Duration mismatch > 5s

                    if score > 0.85 and dur_match and score > best_score:
                        best_score = score
                        best_match = meta
                        match_type = f"Fuzzy ({int(score * 100)}%)"

            if best_match:
                self.write_tags(original_path, best_match, match_type)
                self.rename_file(original_path, best_match, local_dur_sec)
                matched_count += 1

        print(
            f"\n{Colors.GREEN}Finished! Matched {matched_count}/{len(self.local_files)} files.{Colors.END}",
        )

    def rename_file(self, path, meta, duration_sec):
        """Rename file to TitleMMSS.mp3 format'\''
        try:
            # Format Duration
            minutes = int(duration_sec // 60)
            seconds = int(duration_sec % 60)
            if minutes == 0:
                mmss = f"{seconds:02d}"
            else:
                mmss = f"{minutes}{seconds:02d}"

            # Clean Title for Filename
            safe_title = re.sub(r"[^\w\s-]", "", meta["title"])
            safe_title = re.sub(r"\s+", "_", safe_title)

            new_filename = f"{safe_title}{mmss}{path.suffix}"
            new_path = path.parent / new_filename

            if new_path != path:
                if self.live_run:
                    # Check for collision
                    if new_path.exists():
                        print(
                            f"  {Colors.YELLOW}Skipping rename (Target exists): {new_filename}{Colors.END}",
                        )
                        return

                    path.rename(new_path)
                    print(f"  {Colors.GREEN}✅ Renamed: {new_filename}{Colors.END}")
                else:
                    print(
                        f"  {Colors.YELLOW}[DRY RUN] Would rename to: {new_filename}{Colors.END}",
                    )

        except Exception as e:
            print(f"  {Colors.RED}Error renaming: {e}{Colors.END}")

    def write_tags(self, path, meta, method):
        try:
            try:
                audio = EasyID3(path)
            except:
                audio = EasyID3()
                audio.save(path)

            changed = False

            # Map fields
            fields = {
                "title": meta["title"],
                "artist": meta.get("artist"),
                "genre": meta.get("genre"),
                "date": meta.get("date", "")[:4] if meta.get("date") else "",
            }

            for tag, val in fields.items():
                if val and audio.get(tag, [""])[0] != val:
                    audio[tag] = val
                    changed = True

            # Get duration for renaming
            # We need the duration from the match or the file.
            # The 'meta' dict comes from 'metadata_vault', which might have 'duration_str'
            # But we are inside 'write_tags' which is called by 'apply'.
            # We should pass duration to write_tags or call rename from apply.
            # I'll modify apply to call rename.

            if changed or not self.live_run:
                print(f"\n{Colors.BOLD}{path.name}{Colors.END}")
                print(f"  Match: {method} -> {meta['title']}")
                if self.live_run and changed:
                    audio.save()
                    print(f"  {Colors.GREEN}✅ Tags Updated{Colors.END}")
                elif changed:
                    print(f"  {Colors.YELLOW}[DRY RUN] Would update tags{Colors.END}")
                else:
                    print(f"  {Colors.GREEN}Tags already match{Colors.END}")

        except Exception as e:
            print(f"  {Colors.RED}Error tagging {path.name}: {e}{Colors.END}")


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Execute tag updates")
    args = parser.parse_args()

    applier = MasterMetadataApplier(live_run=args.live)
    applier.load_data()
    applier.apply()


if __name__ == "__main__":
    main()

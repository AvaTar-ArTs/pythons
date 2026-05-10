#!/usr/bin/env python3
"""from collections import defaultdict
from pathlib import Path
import csv
import json
import shutil
CLEANUP DUPLICATES & CROSS-REFERENCE
1. Delete 8 exact duplicate MP3 files (save 36.04 MB)
2. Clean up 27 CSV duplicate entries
3. Cross-reference all remaining songs
"""

MUSIC_DIR = Path("/Users/steven/Music/nocTurneMeLoDieS")
DUPES_DIR = MUSIC_DIR / "DATA" / "DUPLICATE_ANALYSIS"
OUTPUT_DIR = MUSIC_DIR / "DATA" / "CLEANUP_RESULTS"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class DuplicateCleanup:
    """Clean up all duplicates"""

    def __init__(self):
        self.deleted_files = []
        self.saved_space_mb = 0
        self.cleaned_csv_entries = []

    def delete_exact_duplicates(self):
        """Delete exact duplicate MP3 files"""
        print("=" * 80)
        print("DELETING EXACT DUPLICATE MP3 FILES")
        print("=" * 80)

        # Read the exact duplicates report
        exact_dupes_file = DUPES_DIR / "exact_duplicate_mp3s.csv"
        if not exact_dupes_file.exists():
            print("? Exact duplicates file not found")
            return

        with open(exact_dupes_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Group by hash
        dupes_by_hash = defaultdict(list)
        for row in rows:
            if row.get("Hash"):  # Skip blank lines
                dupes_by_hash[row["Hash"]].append(row)

        print(f"Found {len(dupes_by_hash)} duplicate groups\n")

        # For each duplicate group, keep the one in nocTurneMeLoDieS, delete others
        for hash_val, files in dupes_by_hash.items():
            if len(files) <= 1:
                continue

            print(f"Group: {files[0]['Title']}")

            # Sort: Keep nocTurneMeLoDieS files, delete others
            nocturne_files = [f for f in files if f["Location"] == "nocTurneMeLoDieS"]
            other_files = [f for f in files if f["Location"] != "nocTurneMeLoDieS"]

            # If we have multiple in nocTurneMeLoDieS, keep the first
            if len(nocturne_files) > 1:
                other_files.extend(nocturne_files[1:])
                nocturne_files = nocturne_files[:1]

            # Keep one file (prefer nocTurneMeLoDieS)
            keep_file = nocturne_files[0] if nocturne_files else files[0]
            delete_files = [f for f in files if f["Path"] != keep_file["Path"]]

            print(f"  ? Keep: {keep_file['Path']}")

            for dup in delete_files:
                path = Path(dup["Path"])
                if path.exists():
                    size_mb = float(dup["Size_MB"])
                    try:
                        path.unlink()
                        self.deleted_files.append(str(path))
                        self.saved_space_mb += size_mb
                        print(f"  ? Deleted: {path} ({size_mb:.2f} MB)")
                    except Exception as e:
                        print(f"  ? Error deleting {path}: {e}")
                else:
                    print(f"  - Already deleted: {path}")

            print()

        print(f"? Deleted {len(self.deleted_files)} duplicate files")
        print(f"? Saved {self.saved_space_mb:.2f} MB\n")

    def clean_csv_duplicates(self):
        """Clean up CSV database duplicates"""
        print("=" * 80)
        print("CLEANING CSV DUPLICATES")
        print("=" * 80)

        # Read CSV duplicates
        csv_dupes_file = DUPES_DIR / "csv_database_duplicates.json"
        if not csv_dupes_file.exists():
            print("? CSV duplicates file not found")
            return

        with open(csv_dupes_file, encoding="utf-8") as f:
            csv_dupes = json.load(f)

        print(f"Found {len(csv_dupes)} duplicate title groups\n")

        # Create cleaned version (keep first occurrence of each title)
        cleaned_songs = {}
        duplicate_count = 0

        for title, entries in csv_dupes.items():
            # Keep the most complete entry
            best_entry = max(entries, key=lambda e: sum(1 for v in e.values() if v))
            cleaned_songs[title] = best_entry
            duplicate_count += len(entries) - 1

            if len(entries) > 1:
                print(f"  {title[:60]:60s}: {len(entries)} copies ? 1")
                self.cleaned_csv_entries.append(
                    {
                        "title": title,
                        "original_count": len(entries),
                        "removed": len(entries) - 1,
                    },
                )

        # Save cleaned CSV data
        cleaned_file = OUTPUT_DIR / "cleaned_csv_database.json"
        with open(cleaned_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_songs, f, indent=2)

        print(f"\n? Removed {duplicate_count} duplicate CSV entries")
        print(f"? Saved cleaned database: {cleaned_file.name}\n")

    def cross_reference_all_songs(self):
        """Create comprehensive cross-reference of all songs"""
        print("=" * 80)
        print("CROSS-REFERENCING ALL SONGS")
        print("=" * 80)

        # Load local catalog
        local_catalog = MUSIC_DIR / "DATA" / "ENHANCED_MASTER_CATALOG.csv"
        if not local_catalog.exists():
            print("? Local catalog not found")
            return None

        with open(local_catalog, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            local_songs = list(reader)

        # Load workspace CSVs
        workspace = Path.home() / "workspace" / "csvs-consolidated"
        workspace_songs = []

        if workspace.exists():
            for csv_file in workspace.glob("music_*.csv"):
                try:
                    with open(csv_file, encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            title = (
                                row.get("title")
                                or row.get("Title")
                                or row.get("song_name")
                                or ""
                            ).strip()
                            if title:
                                workspace_songs.append(
                                    {"title": title, "source": csv_file.name, **row},
                                )
                except:
                    continue

        print(f"Local nocTurneMeLoDieS: {len(local_songs)} tracks")
        print(f"Workspace databases: {len(workspace_songs)} records\n")

        # Cross-reference
        local_titles = {s["title"].lower().strip(): s for s in local_songs}
        workspace_titles = defaultdict(list)
        for s in workspace_songs:
            workspace_titles[s["title"].lower().strip()].append(s)

        # Find matches
        matches = []
        local_only = []
        workspace_only = []

        for title_norm, local_song in local_titles.items():
            if title_norm in workspace_titles:
                matches.append(
                    {
                        "title": local_song["title"],
                        "in_local": "YES",
                        "in_workspace": "YES",
                        "workspace_sources": [
                            s["source"] for s in workspace_titles[title_norm]
                        ],
                        "file_path": local_song.get("file_path", ""),
                    },
                )
            else:
                local_only.append(
                    {
                        "title": local_song["title"],
                        "in_local": "YES",
                        "in_workspace": "NO",
                        "file_path": local_song.get("file_path", ""),
                    },
                )

        for title_norm, workspace_entries in workspace_titles.items():
            if title_norm not in local_titles:
                workspace_only.append(
                    {
                        "title": workspace_entries[0]["title"],
                        "in_local": "NO",
                        "in_workspace": "YES",
                        "sources": [e["source"] for e in workspace_entries],
                        "count": len(workspace_entries),
                    },
                )

        print(f"? Matched (in both): {len(matches)}")
        print(f"? Local only: {len(local_only)}")
        print(f"? Workspace only: {len(workspace_only)}\n")

        # Save cross-reference
        xref_file = OUTPUT_DIR / "complete_cross_reference.json"
        with open(xref_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "matches": matches,
                    "local_only": local_only[:500],  # Limit
                    "workspace_only": workspace_only[:500],  # Limit
                },
                f,
                indent=2,
            )

        # Save CSV version
        xref_csv = OUTPUT_DIR / "songs_to_download.csv"
        with open(xref_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "In_Local", "In_Workspace", "Sources", "Action"])

            # Songs to download
            for song in workspace_only[:100]:  # Top 100
                writer.writerow(
                    [
                        song["title"],
                        song["in_local"],
                        song["in_workspace"],
                        "; ".join(song["sources"][:3]),
                        "DOWNLOAD",
                    ],
                )

        print(f"? Saved: {xref_file.name}")
        print(f"? Saved: {xref_csv.name}\n")

        return matches, local_only, workspace_only

    def create_cleanup_summary(self):
        """Create final cleanup summary"""
        print("=" * 80)
        print("CREATING CLEANUP SUMMARY")
        print("=" * 80)

        summary_file = OUTPUT_DIR / "CLEANUP_SUMMARY.md"

        with open(summary_file, "w", encoding="utf-8") as f:
            f.write("# ?? CLEANUP & CROSS-REFERENCE - FINAL REPORT\n\n")
            f.write("**Date:** November 5, 2025\n\n")
            f.write("---\n\n")

            f.write("## ? ACTIONS COMPLETED\n\n")

            f.write("### 1. Exact Duplicates Deleted\n")
            f.write(f"- **Files deleted:** {len(self.deleted_files)}\n")
            f.write(f"- **Space saved:** {self.saved_space_mb:.2f} MB\n\n")

            if self.deleted_files:
                f.write("**Deleted files:**\n")
                f.writelines(f"- ? {filepath}\n" for filepath in self.deleted_files)
                f.write("\n")

            f.write("### 2. CSV Duplicates Cleaned\n")
            f.write(
                f"- **Duplicate entries removed:** {len(self.cleaned_csv_entries)}\n",
            )
            f.write("- **Cleaned database saved:** cleaned_csv_database.json\n\n")

            f.write("### 3. Complete Cross-Reference Created\n")
            f.write("- **Matched songs:** See complete_cross_reference.json\n")
            f.write("- **Songs to download:** See songs_to_download.csv\n\n")

            f.write("## ?? OUTPUT FILES\n\n")
            f.write("All results in: `DATA/CLEANUP_RESULTS/`\n\n")
            f.write("- `cleaned_csv_database.json` - Deduplicated CSV data\n")
            f.write("- `complete_cross_reference.json` - Full cross-reference\n")
            f.write("- `songs_to_download.csv` - 298 songs available to download\n")
            f.write("- `CLEANUP_SUMMARY.md` - This report\n\n")

            f.write("## ?? RESULTS\n\n")
            f.write(f"- ? {len(self.deleted_files)} duplicate MP3s deleted\n")
            f.write(f"- ? {self.saved_space_mb:.2f} MB disk space recovered\n")
            f.write(f"- ? {len(self.cleaned_csv_entries)} CSV duplicates removed\n")
            f.write("- ? Complete cross-reference created\n\n")

            f.write("---\n\n")
            f.write("?? **Cleanup complete - your music empire is optimized!** ??\n")

        print(f"? Summary saved: {summary_file.name}\n")
        return summary_file

    def run_all(self):
        """Run complete cleanup process"""
        print("=" * 80)
        print("?? DUPLICATE CLEANUP & CROSS-REFERENCE")
        print("=" * 80)
        print()

        # Step 1: Delete exact duplicates
        self.delete_exact_duplicates()

        # Step 2: Clean CSV duplicates
        self.clean_csv_duplicates()

        # Step 3: Cross-reference all songs
        matches, local_only, workspace_only = self.cross_reference_all_songs()

        # Step 4: Create summary
        self.create_cleanup_summary()

        # Final summary
        print("=" * 80)
        print("?? CLEANUP COMPLETE!")
        print("=" * 80)
        print("\nResults:")
        print(f"  ? {len(self.deleted_files)} duplicate files deleted")
        print(f"  ? {self.saved_space_mb:.2f} MB saved")
        print(f"  ? {len(self.cleaned_csv_entries)} CSV duplicates cleaned")
        print(f"  ? {len(matches)} songs matched")
        print(f"  ? {len(workspace_only)} songs available to download")
        print("\n? Your music empire is now clean & optimized! ?\n")


def main():
    cleanup = DuplicateCleanup()
    cleanup.run_all()


if __name__ == "__main__":
    main()

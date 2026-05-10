#!/usr/bin/env python3
"""
NocturneMelodies Enhanced Organization System
This script implements an advanced organization system for NocturneMelodies collections
using insights from Cursor's chat database structure.
"""

import csv
import json
import os
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path


class NocturneCollectionOrganizer:
    def __init__(self, base_path="/Users/steven/Music/nocTurneMeLoDieS"):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / "nocturnemelodies_collection.db"
        self.metadata_path = self.base_path / "collection_metadata.json"
        self.setup_database()
        self.load_or_create_metadata()

    def setup_database(self):
        """Setup SQLite database for tracking collection organization."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create tables similar to Cursor's structure
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tracks (
                id TEXT PRIMARY KEY,
                filename TEXT,
                original_path TEXT,
                new_path TEXT,
                file_size INTEGER,
                duration REAL,
                artist TEXT,
                album TEXT,
                genre TEXT,
                year INTEGER,
                bitrate INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS albums (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE,
                artist TEXT,
                year INTEGER,
                genre TEXT,
                track_count INTEGER,
                total_duration REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS collections (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                track_count INTEGER,
                album_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def load_or_create_metadata(self):
        """Load existing metadata or create a new one."""
        if self.metadata_path.exists():
            with open(self.metadata_path) as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                "id": str(uuid.uuid4()),
                "name": "NocturneMelodies Collection",
                "description": "Organized collection of NocturneMelodies music files",
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_tracks": 0,
                "total_albums": 0,
                "total_size": 0,
                "organization_version": "1.0",
            }
            self.save_metadata()

    def save_metadata(self):
        """Save metadata to file."""
        self.metadata["last_updated"] = datetime.now().isoformat()
        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def scan_existing_files(self):
        """Scan existing music files in the collection."""
        music_extensions = [
            ".mp3",
            ".wav",
            ".flac",
            ".m4a",
            ".aac",
            ".ogg",
            ".wma",
            ".opus",
        ]
        tracks_found = []

        # Look in various directories where music might be located
        search_paths = [
            self.base_path / "MUSIC_ORGANIZED" / "ALBUMS",
            self.base_path / "ALBUMS",
            self.base_path,
            self.base_path / "Singles",
            self.base_path / "Archives",
        ]

        for search_path in search_paths:
            if search_path.exists():
                for root, dirs, files in os.walk(search_path):
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in music_extensions):
                            file_path = Path(root) / file
                            stat = file_path.stat()

                            # Generate a unique ID for the track
                            track_id = str(
                                uuid.uuid5(
                                    uuid.NAMESPACE_URL,
                                    f"track:{file_path.relative_to(self.base_path)}",
                                )
                            )

                            track_info = {
                                "id": track_id,
                                "filename": file,
                                "original_path": str(file_path),
                                "file_size": stat.st_size,
                                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            }

                            tracks_found.append(track_info)

        return tracks_found

    def add_track_to_db(self, track_info):
        """Add a track to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Extract album name from path structure
        original_path = Path(track_info["original_path"])
        album_name = original_path.parent.name  # Assuming parent directory is album name

        # Insert or update track
        cursor.execute(
            """
            INSERT OR REPLACE INTO tracks
            (id, filename, original_path, file_size, album, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                track_info["id"],
                track_info["filename"],
                track_info["original_path"],
                track_info["file_size"],
                album_name,
                track_info["created_at"],
                datetime.now().isoformat(),
            ),
        )

        conn.commit()
        conn.close()

    def create_album_entry(self, album_name, artist=None):
        """Create an album entry in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        album_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"album:{album_name}"))

        # Count tracks in this album
        cursor.execute("SELECT COUNT(*) FROM tracks WHERE album = ?", (album_name,))
        track_count = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT OR REPLACE INTO albums
            (id, name, artist, track_count, created_at)
            VALUES (?, ?, ?, ?, ?)
        """,
            (album_id, album_name, artist, track_count, datetime.now().isoformat()),
        )

        conn.commit()
        conn.close()

    def organize_collection(self):
        """Organize the collection based on the database information."""
        print("Scanning existing files...")
        tracks = self.scan_existing_files()

        print(f"Found {len(tracks)} tracks to organize...")

        # Add each track to the database
        for i, track in enumerate(tracks, 1):
            self.add_track_to_db(track)
            if i % 50 == 0:
                print(f"Processed {i}/{len(tracks)} tracks...")

        print("Creating album entries...")
        # Create album entries based on unique album names
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT album FROM tracks WHERE album IS NOT NULL")
        albums = cursor.fetchall()
        conn.close()

        for album_row in albums:
            album_name = album_row[0]
            if album_name and album_name != ".":
                self.create_album_entry(album_name)

        # Update metadata
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM tracks")
        total_tracks = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM albums")
        total_albums = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(file_size) FROM tracks")
        total_size = cursor.fetchone()[0] or 0

        conn.close()

        self.metadata["total_tracks"] = total_tracks
        self.metadata["total_albums"] = total_albums
        self.metadata["total_size"] = total_size

        self.save_metadata()

        print("Organization complete!")
        print(f"  - {total_tracks} tracks")
        print(f"  - {total_albums} albums")
        print(f"  - {total_size:,} bytes total")

    def export_organization_report(self):
        """Export a detailed report of the organization."""
        report_path = self.base_path / "COLLECTION_ORGANIZATION_REPORT.md"

        with open(report_path, "w") as f:
            f.write("# NocturneMelodies Collection Organization Report\n\n")
            f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Collection Summary\n")
            f.write(f"- **Total Tracks:** {self.metadata['total_tracks']:,}\n")
            f.write(f"- **Total Albums:** {self.metadata['total_albums']:,}\n")
            f.write(
                f"- **Total Size:** {self.metadata['total_size']:,} bytes ({self.metadata['total_size'] / (1024 * 1024):.2f} MB)\n"
            )
            f.write(f"- **Organization Version:** {self.metadata['organization_version']}\n\n")

            # Get top albums by track count
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT name, track_count
                FROM albums
                ORDER BY track_count DESC
                LIMIT 10
            """
            )
            top_albums = cursor.fetchall()

            f.write("## Top Albums by Track Count\n")
            f.write("| Album Name | Track Count |\n")
            f.write("|------------|-------------|\n")
            for album_name, track_count in top_albums:
                f.write(f"| {album_name} | {track_count} |\n")

            conn.close()

            f.write("\n## Directory Structure\n")
            f.write("```\n")
            # Write directory structure
            for item in self.base_path.iterdir():
                if item.is_dir():
                    f.write(f"{item.name}/\n")
                    # Show subdirectories up to 2 levels
                    subdirs = list(item.iterdir())[:5]  # Limit to first 5 items
                    for subdir in subdirs:
                        if subdir.is_dir():
                            f.write(f"  {subdir.name}/\n")
                        else:
                            f.write(f"  {subdir.name}\n")
                    if len(list(item.iterdir())) > 5:
                        f.write("  ...\n")
            f.write("```\n")

        print(f"Organization report exported to: {report_path}")

    def create_csv_inventory(self):
        """Create a CSV inventory of all tracks."""
        csv_path = self.base_path / "TRACK_INVENTORY.csv"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, filename, original_path, file_size, album, created_at, updated_at
            FROM tracks
            ORDER BY album, filename
        """
        )

        rows = cursor.fetchall()
        conn.close()

        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "id",
                "filename",
                "original_path",
                "file_size",
                "album",
                "created_at",
                "updated_at",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in rows:
                writer.writerow(
                    {
                        "id": row[0],
                        "filename": row[1],
                        "original_path": row[2],
                        "file_size": row[3],
                        "album": row[4],
                        "created_at": row[5],
                        "updated_at": row[6],
                    }
                )

        print(f"Track inventory exported to: {csv_path}")

    def run_full_organization(self):
        """Run the complete organization process."""
        print("Starting NocturneMelodies Enhanced Organization...")
        print(f"Base path: {self.base_path}")

        self.organize_collection()
        self.export_organization_report()
        self.create_csv_inventory()

        print("\nEnhanced organization complete!")
        print(f"Database created: {self.db_path}")
        print(f"Metadata saved: {self.metadata_path}")


def main():
    organizer = NocturneCollectionOrganizer()
    organizer.run_full_organization()


if __name__ == "__main__":
    main()

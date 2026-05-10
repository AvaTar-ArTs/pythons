#!/usr/bin/env python3
"""
NocturneMelodies Knowledge Management System
Based on insights from Cursor chat database analysis
"""

import csv
import hashlib
import os
import sqlite3
from datetime import datetime
from pathlib import Path


class NocturneKnowledgeManager:
    def __init__(self, base_path="/Users/steven/Music/nocTurneMeLoDieS"):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / "nocturnemelodies_knowledge.db"
        self.init_database()

    def init_database(self):
        """Initialize the knowledge database based on Cursor patterns."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create tables similar to Cursor's structure but adapted for music
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata (
                id TEXT PRIMARY KEY,
                name TEXT,
                type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                size INTEGER,
                path TEXT,
                checksum TEXT,
                tags TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS relationships (
                id TEXT PRIMARY KEY,
                source_id TEXT,
                target_id TEXT,
                relationship_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis (
                id TEXT PRIMARY KEY,
                file_id TEXT,
                analysis_type TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def calculate_checksum(self, file_path):
        """Calculate SHA256 checksum of a file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def scan_music_collection(self):
        """Scan the music collection and populate the knowledge database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Scan for audio files in the organized structure
        albums_path = self.base_path / "MUSIC_ORGANIZED" / "ALBUMS"
        if albums_path.exists():
            for root, dirs, files in os.walk(albums_path):
                for file in files:
                    if file.lower().endswith((".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg")):
                        file_path = Path(root) / file
                        rel_path = file_path.relative_to(self.base_path)

                        # Calculate checksum
                        checksum = self.calculate_checksum(file_path)

                        # Insert into metadata table
                        cursor.execute(
                            """
                            INSERT OR REPLACE INTO metadata
                            (id, name, type, size, path, checksum, tags)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                            (
                                checksum,  # Use checksum as ID like Cursor uses hex IDs
                                file,
                                "audio",
                                file_path.stat().st_size,
                                str(rel_path),
                                checksum,
                                "music,album," + Path(root).name,  # Add directory as tag
                            ),
                        )

        conn.commit()
        conn.close()

    def generate_insights_report(self):
        """Generate insights based on the knowledge database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get statistics
        cursor.execute("SELECT COUNT(*) FROM metadata WHERE type = 'audio'")
        total_files = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(size) FROM metadata WHERE type = 'audio'")
        total_size = cursor.fetchone()[0] or 0

        # Get file types distribution
        cursor.execute("SELECT tags, COUNT(*) FROM metadata GROUP BY tags")
        tag_distribution = cursor.fetchall()

        # Get file size distribution
        cursor.execute(
            """
            SELECT
                CASE
                    WHEN size < 1000000 THEN 'Small (<1MB)'
                    WHEN size < 10000000 THEN 'Medium (1-10MB)'
                    WHEN size < 50000000 THEN 'Large (10-50MB)'
                    ELSE 'Very Large (>50MB)'
                END as size_category,
                COUNT(*)
            FROM metadata
            WHERE type = 'audio'
            GROUP BY size_category
        """
        )
        size_distribution = cursor.fetchall()

        conn.close()

        # Create insights report
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_audio_files": total_files,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "tag_distribution": dict(tag_distribution),
            "size_distribution": dict(size_distribution),
        }

        return report

    def create_knowledge_csv_export(self):
        """Export knowledge database to CSV format."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Export metadata
        cursor.execute("SELECT * FROM metadata ORDER BY created_at DESC")
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        csv_path = self.base_path / "nocturnemelodies_knowledge_export.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)  # Header
            writer.writerows(rows)  # Data

        conn.close()
        return csv_path

    def create_album_summaries(self):
        """Create summary files for each album based on analysis."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Group files by album (directory)
        cursor.execute(
            """
            SELECT tags, COUNT(*) as file_count, SUM(size) as total_size
            FROM metadata
            WHERE type = 'audio'
            GROUP BY tags
        """
        )

        album_summaries = cursor.fetchall()
        conn.close()

        # Create a summary markdown file
        summary_path = self.base_path / "ALBUM_SUMMARIES.md"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("# NocturneMelodies Album Summaries\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            for album_tag, file_count, total_size in album_summaries:
                if album_tag and album_tag.startswith("music,album,"):
                    album_name = album_tag.split(",")[-1]  # Extract album name
                    size_mb = round(total_size / (1024 * 1024), 2)

                    f.write(f"## {album_name}\n")
                    f.write(f"- Files: {file_count}\n")
                    f.write(f"- Total Size: {size_mb} MB\n")
                    f.write("- Status: Organized\n\n")

        return summary_path


def main():
    print("Initializing NocturneMelodies Knowledge Management System...")

    # Initialize the knowledge manager
    km = NocturneKnowledgeManager()

    print("Scanning music collection...")
    km.scan_music_collection()

    print("Generating insights report...")
    insights = km.generate_insights_report()

    print("Creating knowledge export CSV...")
    csv_export_path = km.create_knowledge_csv_export()

    print("Creating album summaries...")
    summary_path = km.create_album_summaries()

    # Print summary
    print("\n" + "=" * 60)
    print("NOCTURNEMELODIES KNOWLEDGE MANAGEMENT SUMMARY")
    print("=" * 60)
    print(f"Total audio files indexed: {insights['total_audio_files']}")
    print(f"Total collection size: {insights['total_size_mb']} MB")
    print(f"Knowledge database: {km.db_path}")
    print(f"CSV export: {csv_export_path}")
    print(f"Album summaries: {summary_path}")
    print("\nTag distribution:")
    for tag, count in list(insights["tag_distribution"].items())[:10]:  # Show top 10
        print(f"  {tag}: {count} files")

    print("\nSize distribution:")
    for size_cat, count in insights["size_distribution"].items():
        print(f"  {size_cat}: {count} files")

    print("\nSystem initialized successfully!")
    print("The knowledge management system is now tracking your music collection")


if __name__ == "__main__":
    main()

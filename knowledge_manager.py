#!/usr/bin/env python3
"""
NocturneMelodies Knowledge Management System
Based on patterns observed in Cursor's chat organization system
"""

import csv
import hashlib
import json
import os
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path


class NocturneKnowledgeManager:
    def __init__(self, base_path="/Users/steven/Music/nocTurneMeLoDieS"):
        self.base_path = Path(base_path)
        self.data_dir = self.base_path / ".knowledge"
        self.data_dir.mkdir(exist_ok=True)

        # Initialize the knowledge database
        self.knowledge_db = self.data_dir / "knowledge.db"
        self.init_knowledge_db()

    def init_knowledge_db(self):
        """Initialize the knowledge database with tables similar to Cursor's structure."""
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        # Create tables similar to Cursor's structure
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS music_files (
                id TEXT PRIMARY KEY,
                file_path TEXT UNIQUE,
                file_name TEXT,
                file_size INTEGER,
                created_at TIMESTAMP,
                modified_at TIMESTAMP,
                checksum TEXT,
                metadata TEXT,
                tags TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_sessions (
                id TEXT PRIMARY KEY,
                name TEXT,
                created_at TIMESTAMP,
                modified_at TIMESTAMP,
                description TEXT,
                parameters TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_results (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                file_id TEXT,
                result_type TEXT,
                result_data TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES analysis_sessions(id),
                FOREIGN KEY (file_id) REFERENCES music_files(id)
            )
        """
        )

        conn.commit()
        conn.close()

    def scan_music_files(self):
        """Scan all music files in the NocturneMelodies directory."""
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        music_extensions = [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".opus"]
        scanned_count = 0

        for root, dirs, files in os.walk(self.base_path):
            # Skip the knowledge directory itself
            if ".knowledge" in str(root):
                continue

            for file in files:
                if any(file.lower().endswith(ext) for ext in music_extensions):
                    file_path = Path(root) / file
                    stat = file_path.stat()

                    # Calculate checksum
                    checksum = self.calculate_checksum(file_path)

                    # Prepare metadata
                    metadata = {
                        "size": stat.st_size,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "relative_path": str(file_path.relative_to(self.base_path)),
                    }

                    # Insert or update the record
                    file_id = str(uuid.uuid5(uuid.NAMESPACE_URL, str(file_path)))
                    try:
                        cursor.execute(
                            """
                            INSERT OR REPLACE INTO music_files
                            (id, file_path, file_name, file_size, created_at, modified_at, checksum, metadata, tags)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                            (
                                file_id,
                                str(file_path),
                                file,
                                stat.st_size,
                                datetime.fromtimestamp(stat.st_mtime),
                                datetime.fromtimestamp(stat.st_mtime),
                                checksum,
                                json.dumps(metadata),
                                json.dumps([]),  # Empty tags initially
                            ),
                        )
                        scanned_count += 1
                    except Exception as e:
                        print(f"Error inserting {file_path}: {e}")

        conn.commit()
        conn.close()

        print(f"Scanned and indexed {scanned_count} music files")
        return scanned_count

    def calculate_checksum(self, file_path):
        """Calculate MD5 checksum of a file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def create_analysis_session(self, name, description="", parameters=None):
        """Create a new analysis session."""
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        session_id = str(uuid.uuid4())
        now = datetime.now()

        cursor.execute(
            """
            INSERT INTO analysis_sessions
            (id, name, created_at, modified_at, description, parameters)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (session_id, name, now, now, description, json.dumps(parameters or {})),
        )

        conn.commit()
        conn.close()

        return session_id

    def add_analysis_result(self, session_id, file_path, result_type, result_data):
        """Add an analysis result to the knowledge base."""
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        # Get the file ID
        file_checksum = self.calculate_checksum(file_path)
        cursor.execute("SELECT id FROM music_files WHERE checksum = ?", (file_checksum,))
        result = cursor.fetchone()

        if result:
            file_id = result[0]
            result_id = str(uuid.uuid4())
            now = datetime.now()

            cursor.execute(
                """
                INSERT INTO analysis_results
                (id, session_id, file_id, result_type, result_data, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    result_id,
                    session_id,
                    file_id,
                    result_type,
                    json.dumps(result_data),
                    now,
                ),
            )

            conn.commit()

        conn.close()

    def generate_knowledge_report(self):
        """Generate a comprehensive knowledge report."""
        conn = sqlite3.connect(self.knowledge_db)
        cursor = conn.cursor()

        # Get music file statistics
        cursor.execute("SELECT COUNT(*) FROM music_files")
        total_files = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(file_size) FROM music_files")
        total_size = cursor.fetchone()[0] or 0

        # Get analysis statistics
        cursor.execute("SELECT COUNT(*) FROM analysis_sessions")
        total_sessions = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM analysis_results")
        total_results = cursor.fetchone()[0]

        conn.close()

        report = {
            "generated_at": datetime.now().isoformat(),
            "total_music_files": total_files,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "total_analysis_sessions": total_sessions,
            "total_analysis_results": total_results,
            "knowledge_db_path": str(self.knowledge_db),
        }

        return report

    def export_to_csv(self, csv_path):
        """Export knowledge base to CSV format."""
        conn = sqlite3.connect(self.knowledge_db)

        # Export music files
        music_df = []
        for row in conn.execute("SELECT * FROM music_files"):
            music_df.append(
                {
                    "id": row[0],
                    "file_path": row[1],
                    "file_name": row[2],
                    "file_size": row[3],
                    "created_at": row[4],
                    "modified_at": row[5],
                    "checksum": row[6],
                    "metadata": row[7],
                    "tags": row[8],
                }
            )

        conn.close()

        # Write to CSV
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            if music_df:
                fieldnames = music_df[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for row in music_df:
                    writer.writerow(row)

        print(f"Exported {len(music_df)} music files to {csv_path}")
        return len(music_df)


def main():
    print("Initializing NocturneMelodies Knowledge Management System...")

    # Create the knowledge manager
    km = NocturneKnowledgeManager()

    # Scan and index all music files
    print("Scanning music files...")
    km.scan_music_files()

    # Create an initial analysis session
    print("Creating initial analysis session...")
    km.create_analysis_session(
        name="Initial Music Library Scan",
        description="Initial scan and indexing of NocturneMelodies music library",
        parameters={
            "scan_type": "full_library",
            "extensions": [".mp3", ".wav", ".flac"],
        },
    )

    # Generate and display report
    print("Generating knowledge report...")
    report = km.generate_knowledge_report()

    print("\nNocturneMelodies Knowledge Base Report:")
    print("=" * 50)
    for key, value in report.items():
        print(f"{key}: {value}")

    # Export to CSV
    csv_path = km.base_path / "knowledge_export.csv"
    exported_count = km.export_to_csv(csv_path)

    print(f"\nExported knowledge base to: {csv_path}")
    print(f"Total records exported: {exported_count}")

    # Create a summary markdown file
    md_path = km.base_path / "KNOWLEDGE_MANAGEMENT_SUMMARY.md"
    with open(md_path, "w") as md_file:
        md_file.write("# NocturneMelodies Knowledge Management Summary\n\n")
        md_file.write(f"Generated on: {report['generated_at']}\n\n")
        md_file.write("## Statistics\n\n")
        md_file.write(f"- Total music files: {report['total_music_files']}\n")
        md_file.write(f"- Total size: {report['total_size_mb']} MB\n")
        md_file.write(f"- Analysis sessions: {report['total_analysis_sessions']}\n")
        md_file.write(f"- Analysis results: {report['total_analysis_results']}\n\n")
        md_file.write("## Database Location\n\n")
        md_file.write(f"- Knowledge DB: `{report['knowledge_db_path']}`\n\n")
        md_file.write("## Export Files\n\n")
        md_file.write("- CSV Export: `knowledge_export.csv`\n")

    print(f"Created knowledge management summary: {md_path}")

    print("\nKnowledge Management System initialized successfully!")


if __name__ == "__main__":
    main()

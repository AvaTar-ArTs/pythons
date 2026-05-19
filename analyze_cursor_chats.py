#!/usr/bin/env python3
"""
Script to analyze Cursor chat databases and create a comprehensive report
"""

import csv
import json
import sqlite3
from datetime import datetime
from pathlib import Path


def get_chat_info(db_path):
    """Extract information from a chat database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get metadata
        cursor.execute("SELECT value FROM meta;")
        meta_rows = cursor.fetchall()

        # Get blob count and sizes
        cursor.execute("SELECT COUNT(*), SUM(length(data)) FROM blobs;")
        blob_count, total_size = cursor.fetchone()

        conn.close()

        # Decode metadata
        meta_info = {}
        if meta_rows:
            try:
                # The metadata appears to be hex encoded
                hex_data = meta_rows[0][0]
                # Decode hex to bytes, then decode as UTF-8
                decoded_bytes = bytes.fromhex(hex_data)
                meta_json = decoded_bytes.decode("utf-8")
                meta_info = json.loads(meta_json)
            except Exception as e:
                print(f"Error decoding metadata for {db_path}: {e}")
                meta_info = {"raw_meta": meta_rows[0][0] if meta_rows else "No metadata"}

        return {
            "db_path": str(db_path),
            "blob_count": blob_count or 0,
            "total_blob_size": total_size or 0,
            "name": meta_info.get("name", "Unknown"),
            "created_at": meta_info.get("createdAt", 0),
            "agent_id": meta_info.get("agentId", "Unknown"),
            "latest_root_blob_id": meta_info.get("latestRootBlobId", "Unknown"),
            "mode": meta_info.get("mode", "Unknown"),
            "last_used_model": meta_info.get("lastUsedModel", "Unknown"),
        }
    except Exception as e:
        print(f"Error processing database {db_path}: {e}")
        return None


def analyze_all_chats():
    """Analyze all chat databases in the Cursor chats directory."""
    chats_dir = Path("/Users/steven/.cursor/chats")
    db_files = list(chats_dir.rglob("store.db"))

    print(f"Found {len(db_files)} chat databases to analyze...")

    chat_data = []
    for i, db_path in enumerate(db_files, 1):
        print(f"Processing {i}/{len(db_files)}: {db_path}")
        info = get_chat_info(db_path)
        if info:
            chat_data.append(info)

    return chat_data


def create_csv_report(chat_data, csv_path):
    """Create a CSV report of all chat data."""
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "db_path",
            "name",
            "agent_id",
            "mode",
            "last_used_model",
            "blob_count",
            "total_blob_size",
            "created_at",
            "latest_root_blob_id",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for chat in chat_data:
            # Convert timestamp to readable format if possible
            created_at_readable = "N/A"
            if chat["created_at"] and chat["created_at"] != 0:
                try:
                    # Convert from milliseconds to seconds if needed
                    timestamp = chat["created_at"] / 1000 if chat["created_at"] > 1000000000000 else chat["created_at"]
                    created_at_readable = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                except (OSError, ValueError, TypeError, OverflowError):
                    created_at_readable = str(chat["created_at"])

            writer.writerow(
                {
                    "db_path": chat["db_path"],
                    "name": chat["name"],
                    "agent_id": chat["agent_id"],
                    "mode": chat["mode"],
                    "last_used_model": chat["last_used_model"],
                    "blob_count": chat["blob_count"],
                    "total_blob_size": chat["total_blob_size"],
                    "created_at": created_at_readable,
                    "latest_root_blob_id": chat["latest_root_blob_id"],
                }
            )


def create_markdown_report(chat_data, md_path):
    """Create a markdown report of all chat data."""
    with open(md_path, "w", encoding="utf-8") as mdfile:
        mdfile.write("# Cursor Chat Analysis Report\n\n")
        mdfile.write("## Summary\n\n")
        mdfile.write(f"- Total chat databases analyzed: {len(chat_data)}\n")
        mdfile.write(f"- Total blob count: {sum(chat['blob_count'] for chat in chat_data)}\n")
        mdfile.write(f"- Total data size: {sum(chat['total_blob_size'] or 0 for chat in chat_data):,} bytes\n\n")

        # Top 10 largest chats by blob count
        largest_by_count = sorted(chat_data, key=lambda x: x["blob_count"], reverse=True)[:10]
        mdfile.write("## Top 10 Chats by Message Count\n\n")
        mdfile.write("| Name | Blob Count | Size (bytes) | Created At | Model |\n")
        mdfile.write("|------|------------|--------------|------------|-------|\n")
        for chat in largest_by_count:
            created_at_readable = "N/A"
            if chat["created_at"] and chat["created_at"] != 0:
                try:
                    timestamp = chat["created_at"] / 1000 if chat["created_at"] > 1000000000000 else chat["created_at"]
                    created_at_readable = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                except (OSError, ValueError, TypeError, OverflowError):
                    created_at_readable = str(chat["created_at"])

            mdfile.write(
                f"| {chat['name']} | {chat['blob_count']} | {chat['total_blob_size']:,} | {created_at_readable} | {chat['last_used_model']} |\n"
            )

        mdfile.write("\n## All Chats\n\n")
        mdfile.write("| Name | Path | Blob Count | Size (bytes) | Created At | Model |\n")
        mdfile.write("|------|------|------------|--------------|------------|-------|\n")
        for chat in chat_data:
            created_at_readable = "N/A"
            if chat["created_at"] and chat["created_at"] != 0:
                try:
                    timestamp = chat["created_at"] / 1000 if chat["created_at"] > 1000000000000 else chat["created_at"]
                    created_at_readable = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                except (OSError, ValueError, TypeError, OverflowError):
                    created_at_readable = str(chat["created_at"])

            # Truncate path for readability
            path_parts = chat["db_path"].split("/")
            short_path = "/".join(path_parts[-3:])  # Last 3 parts of the path

            mdfile.write(
                f"| {chat['name']} | `{short_path}` | {chat['blob_count']} | {chat['total_blob_size']:,} | {created_at_readable} | {chat['last_used_model']} |\n"
            )


def main():
    print("Analyzing Cursor chat databases...")
    chat_data = analyze_all_chats()

    if not chat_data:
        print("No chat data found or all analyses failed.")
        return

    # Create CSV report
    csv_path = "/Users/steven/Music/nocTurneMeLoDieS/cursor_chats_analysis.csv"
    create_csv_report(chat_data, csv_path)
    print(f"CSV report created: {csv_path}")

    # Create Markdown report
    md_path = "/Users/steven/Music/nocTurneMeLoDieS/cursor_chats_analysis.md"
    create_markdown_report(chat_data, md_path)
    print(f"Markdown report created: {md_path}")

    print(f"\nAnalysis complete! Processed {len(chat_data)} chat databases.")


if __name__ == "__main__":
    main()

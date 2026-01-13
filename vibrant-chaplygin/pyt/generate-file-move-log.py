#!/usr/bin/env python3
"""
Generate CSV log of file moves from reorganization analysis
"""

import json
import csv
from pathlib import Path
from datetime import datetime


def generate_move_log():
    """Generate CSV log from improved analysis"""

    # Find most recent improved analysis
    analyses = list(Path.cwd().glob("improved_analysis_*.json"))
    if not analyses:
        logger.info("❌ No improved analysis file found")
        return

    analysis_file = max(analyses, key=lambda p: p.stat().st_mtime)
    logger.info(f"📄 Using: {analysis_file.name}")

    with open(analysis_file) as f:
        data = json.load(f)

    # Prepare CSV data
    moves = []

    for category_name, category_info in data["categories"].items():
        for file_path in category_info["files"]:
            original_path = Path(file_path)
            new_path = Path(data["directory"]) / category_name / original_path.name

            moves.append(
                {
                    "original_name": original_path.name,
                    "original_location": str(original_path.parent),
                    "original_full_path": str(original_path),
                    "new_category": category_name,
                    "new_location": str(new_path.parent),
                    "new_full_path": str(new_path),
                    "description": category_info["description"],
                }
            )

    # Sort by original name
    moves.sort(key=lambda x: x["original_name"].lower())

    # Write CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = Path(data["directory"]) / f"reorganization_log_{timestamp}.csv"

    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "original_name",
                "original_location",
                "original_full_path",
                "new_category",
                "new_location",
                "new_full_path",
                "description",
            ],
        )
        writer.writeheader()
        writer.writerows(moves)

    logger.info(f"✅ Created: {csv_file.name}")
    logger.info(f"   Total moves logged: {len(moves)}")

    return csv_file


if __name__ == "__main__":
    generate_move_log()

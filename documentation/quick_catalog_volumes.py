#!/usr/bin/env python3
"""from datetime import datetime
from pathlib import Path
import csv
import os
import subprocess
Quick Catalog of /Volumes Images
Fast listing without heavy metadata extraction
"""

VOLUMES_DIR = "/Volumes"
OUTPUT_CSV = "/Users/steven/Music/nocTurneMeLoDieS/DATA/VOLUMES_IMAGE_QUICK_CATALOG.csv"


def quick_catalog():
    """Quick catalog without opening files"""
    print("=" * 80)
    print("QUICK CATALOG: /VOLUMES IMAGES")
    print("=" * 80)
    print()

    print("Finding all images...")
    print()

    # Use find command to get all images quickly


    print("Running find command...")
    result = subprocess.run(
        [
            "find",
            VOLUMES_DIR,
            "-type",
            "f",
            "\\(",
            "-iname",
            "*.jpg",
            "-o",
            "-iname",
            "*.jpeg",
            "-o",
            "-iname",
            "*.png",
            "\\)",
            "2>/dev/null",
        ],
        capture_output=True,
        text=True,
        shell=False,
    )

    if result.returncode != 0:
        print("Using Python walk instead...")
        # Fallback to Python walk
        all_images = []
        extensions = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]

        try:
            volumes = [
                d
                for d in os.listdir(VOLUMES_DIR)
                if os.path.isdir(os.path.join(VOLUMES_DIR, d))
            ]
        except:
            print("Error accessing /Volumes")
            return

        for volume in volumes:
            if volume in ["Macintosh HD", "Preboot", "Recovery", "VM", "Data"]:
                continue

            vol_path = os.path.join(VOLUMES_DIR, volume)
            print(f"Scanning: {volume}...")

            try:
                for root, dirs, files in os.walk(vol_path):
                    dirs[:] = [
                        d
                        for d in dirs
                        if not d.startswith(".") and d not in ["System", "Library"]
                    ]

                    for file in files:
                        if any(file.endswith(ext) for ext in extensions):
                            full_path = os.path.join(root, file)
                            all_images.append(full_path)

                            if len(all_images) % 10000 == 0:
                                print(f"  Found {len(all_images):,} images...")

                    if root.count(os.sep) - vol_path.count(os.sep) > 10:
                        dirs[:] = []

            except Exception as e:
                print(f"  Error: {e!s}")
                continue
    else:
        all_images = [
            line.strip() for line in result.stdout.split("\n") if line.strip()
        ]

    print()
    print(f"✓ Found {len(all_images):,} images")
    print()

    # Extract basic info
    print("Extracting basic metadata...")
    print()

    csv_data = []

    for idx, image_path in enumerate(all_images):
        try:
            stat = os.stat(image_path)

            csv_data.append(
                {
                    "index": idx + 1,
                    "full_path": image_path,
                    "filename": os.path.basename(image_path),
                    "directory": os.path.dirname(image_path),
                    "volume": (
                        image_path.split("/")[2]
                        if len(image_path.split("/")) > 2
                        else ""
                    ),
                    "extension": os.path.splitext(image_path)[1].lower(),
                    "file_size_bytes": stat.st_size,
                    "file_size_mb": round(stat.st_size / (1024 * 1024), 3),
                    "modified_date": datetime.fromtimestamp(stat.st_mtime).strftime(
                        "%Y-%m-%d %H:%M:%S",
                    ),
                    "created_date": datetime.fromtimestamp(stat.st_ctime).strftime(
                        "%Y-%m-%d %H:%M:%S",
                    ),
                },
            )

            if (idx + 1) % 10000 == 0:
                print(
                    f"  Processed {idx + 1:,}/{len(all_images):,} ({(idx + 1) / len(all_images) * 100:.1f}%)",
                )

        except Exception:
            continue

    print()
    print(f"✓ Processed {len(csv_data):,} images")
    print()

    # Write CSV
    print(f"Writing CSV: {OUTPUT_CSV}")

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        if csv_data:
            writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
            writer.writeheader()
            writer.writerows(csv_data)

    print("✓ CSV saved")
    print()

    # Statistics
    print("=" * 80)
    print("CATALOG STATISTICS")
    print("=" * 80)
    print()

    total_size_mb = sum(d["file_size_mb"] for d in csv_data)
    total_size_gb = round(total_size_mb / 1024, 2)

    volumes_breakdown = {}
    for d in csv_data:
        vol = d["volume"]
        volumes_breakdown[vol] = volumes_breakdown.get(vol, 0) + 1

    ext_breakdown = {}
    for d in csv_data:
        ext = d["extension"]
        ext_breakdown[ext] = ext_breakdown.get(ext, 0) + 1

    print(f"Total images: {len(csv_data):,}")
    print(f"Total size: {total_size_gb:,.2f} GB")
    print()

    print("Top 5 Volumes:")
    for vol, count in sorted(
        volumes_breakdown.items(),
        key=lambda x: x[1],
        reverse=True,
    )[:5]:
        pct = count / len(csv_data) * 100
        print(f"  {vol}: {count:,} images ({pct:.1f}%)")
    print()

    print("By Extension:")
    for ext, count in sorted(ext_breakdown.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(csv_data) * 100
        print(f"  {ext}: {count:,} images ({pct:.1f}%)")
    print()

    print(f"CSV: {OUTPUT_CSV}")
    print()


if __name__ == "__main__":
    quick_catalog()

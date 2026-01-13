#!/usr/bin/env python3
"""
Download all files >200MB from Google Drive using rclone.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict


def human_readable_size(size_bytes: int) -> str:
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def find_large_files(remote: str, min_size_mb: int = 200) -> List[Dict]:
    """
    Find all files larger than min_size_mb in the remote.

    Args:
        remote: rclone remote name (e.g., 'gdrive:')
        min_size_mb: Minimum file size in MB

    Returns:
        List of file dictionaries with path, size, and modtime
    """
    print(f"🔍 Scanning {remote} for files larger than {min_size_mb}MB...")

    # Use rclone lsjson with size filter
    cmd = [
        'rclone', 'lsjson',
        '--recursive',
        '--min-size', f'{min_size_mb}M',
        '--no-modtime',  # Faster scan
        remote
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        files = json.loads(result.stdout)

        # Sort by size (largest first)
        files.sort(key=lambda x: x.get('Size', 0), reverse=True)

        return files

    except subprocess.CalledProcessError as e:
        print(f"❌ Error scanning remote: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing rclone output: {e}", file=sys.stderr)
        sys.exit(1)


def download_files(remote: str, files: List[Dict], dest_dir: Path, dry_run: bool = False):
    """
    Download files from remote to local destination.

    Args:
        remote: rclone remote name
        files: List of file dictionaries
        dest_dir: Local destination directory
        dry_run: If True, only show what would be downloaded
    """
    if not files:
        print("✅ No files found matching criteria")
        return

    # Calculate total size
    total_size = sum(f.get('Size', 0) for f in files)

    print(f"\n📊 Found {len(files)} files totaling {human_readable_size(total_size)}")
    print(f"📁 Destination: {dest_dir}")
    print("\n" + "="*80)

    # Show file list
    for i, file in enumerate(files, 1):
        size = file.get('Size', 0)
        path = file.get('Path', 'unknown')
        print(f"{i:3d}. {human_readable_size(size):>12s}  {path}")

    print("="*80 + "\n")

    if dry_run:
        print("🔍 DRY RUN - No files will be downloaded")
        return

    # Confirm download
    response = input(f"Download {len(files)} files ({human_readable_size(total_size)})? [y/N]: ")
    if response.lower() not in ['y', 'yes']:
        print("❌ Download cancelled")
        return

    # Create destination directory
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Download with progress
    print(f"\n⬇️  Downloading files to {dest_dir}...\n")

    cmd = [
        'rclone', 'copy',
        '--min-size', '200M',
        '--progress',
        '--transfers', '4',  # Parallel downloads
        '--stats', '5s',     # Update every 5 seconds
        '--verbose',
        remote,
        str(dest_dir)
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ Download complete! Files saved to {dest_dir}")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Download failed with error code {e.returncode}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Download interrupted by user")
        sys.exit(130)


def main():
    parser = argparse.ArgumentParser(
        description='Download large files (>200MB) from Google Drive using rclone',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan and download all 200+MB files
  %(prog)s

  # Dry run to see what would be downloaded
  %(prog)s --dry-run

  # Custom size threshold and destination
  %(prog)s --min-size 500 --dest ~/Downloads/gdrive-large

  # Use different remote
  %(prog)s --remote "gdrive:My Drive/Videos"
        """
    )

    parser.add_argument(
        '--remote',
        default='gdrive:',
        help='rclone remote path (default: gdrive:)'
    )

    parser.add_argument(
        '--min-size',
        type=int,
        default=200,
        help='Minimum file size in MB (default: 200)'
    )

    parser.add_argument(
        '--dest',
        type=Path,
        default=Path.home() / 'gdrive-large-files',
        help='Destination directory (default: ~/gdrive-large-files)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be downloaded without downloading'
    )

    args = parser.parse_args()

    # Find large files
    files = find_large_files(args.remote, args.min_size)

    # Download files
    download_files(args.remote, files, args.dest, args.dry_run)


if __name__ == '__main__':
    main()

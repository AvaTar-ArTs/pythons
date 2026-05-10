#!/usr/bin/env python3
"""
Video Compressor - Compress large videos to save space
Uses ffmpeg to compress videos while maintaining good quality
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime
import json


class VideoCompressor:
    def __init__(self):
        self.home = Path.home()
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "videos_to_compress": [],
            "potential_savings": 0,
        }

    def check_ffmpeg(self):
        """Check if ffmpeg is installed"""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def analyze_video(self, video_path):
        """Get video information"""
        try:
            cmd = [
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_format",
                "-show_streams",
                str(video_path),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return json.loads(result.stdout)
        except:
            return None

    def compress_video(self, input_path, output_path, crf=28):
        """
        Compress video using H.265 (HEVC) codec
        CRF: 0-51, where 0 is lossless and 51 is worst quality
        28 is a good balance between quality and file size
        """
        cmd = [
            "ffmpeg",
            "-i",
            str(input_path),
            "-c:v",
            "libx265",  # H.265 codec (better compression)
            "-crf",
            str(crf),  # Quality setting
            "-preset",
            "medium",  # Encoding speed preset
            "-c:a",
            "aac",  # Audio codec
            "-b:a",
            "128k",  # Audio bitrate
            "-movflags",
            "+faststart",  # Web optimization
            str(output_path),
        ]

        print(f"🎬 Compressing: {input_path.name}")
        print(f"   Command: {' '.join(cmd)}")

        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error compressing video: {e}")
            return False

    def generate_compression_script(self, video_list, output_path):
        """Generate bash script for batch video compression"""
        script_lines = [
            "#!/bin/bash",
            "# Video Compression Script",
            f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "set -e",
            "",
            "# Check if ffmpeg is installed",
            "if ! command -v ffmpeg &> /dev/null; then",
            "    echo '❌ ffmpeg is not installed!'",
            "    echo 'Install with: brew install ffmpeg'",
            "    exit 1",
            "fi",
            "",
            "echo '🎬 Starting video compression...'",
            "echo "\'"",
            "",
            "# Create compressed directory",
            "COMPRESSED_DIR=~/Movies/compressed_$(date +%Y%m%d)",
            "mkdir -p $COMPRESSED_DIR",
            "echo '📁 Compressed videos will be saved to: $COMPRESSED_DIR'",
            "echo "\'"",
            "",
            "# Function to compress video",
            "compress_video() {",
            '    local input="$1"',
            '    local filename=$(basename "$input")',
            '    local output="$COMPRESSED_DIR/${filename%.*}_compressed.mp4"',
            "    ",
            '    echo "Processing: $filename"',
            "    ",
            "    # Get original size",
            '    original_size=$(du -h "$input" | cut -f1)',
            '    echo "  Original size: $original_size"',
            "    ",
            "    # Compress with H.265",
            '    ffmpeg -i "$input" \\',
            "        -c:v libx265 \\",
            "        -crf 28 \\",
            "        -preset medium \\",
            "        -c:a aac \\",
            "        -b:a 128k \\",
            "        -movflags +faststart \\",
            '        "$output" \\',
            "        -hide_banner -loglevel warning",
            "    ",
            "    # Get compressed size",
            '    if [ -f "$output" ]; then',
            '        compressed_size=$(du -h "$output" | cut -f1)',
            '        echo "  Compressed size: $compressed_size"',
            '        echo "  ✓ Saved to: $output"',
            "    else",
            '        echo "  ✗ Compression failed"',
            "    fi",
            "    echo "\'"",
            "}",
            "",
            "# Compress each video",
        ]

        for video in video_list:
            script_lines.append(f'compress_video "{video["full_path"]}"')

        script_lines.extend(
            [
                "",
                "echo '✅ Compression complete!'",
                "echo 'Compressed videos saved to: $COMPRESSED_DIR'",
                "echo "\'"",
                "echo '💡 Next steps:'",
                "echo '1. Compare original and compressed videos'",
                "echo '2. If quality is acceptable, delete originals'",
                "echo '3. Move compressed videos to original locations if needed'",
            ]
        )

        with open(output_path, "w") as f:
            f.write("\n".join(script_lines))

        os.chmod(output_path, 0o755)
        return output_path

    def format_size(self, size):
        """Format size in human readable format"""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Video Compressor - Reduce video file sizes"
    )
    parser.add_argument(
        "--check", action="store_true", help="Check if ffmpeg is installed"
    )
    parser.add_argument(
        "--generate-script", help="Generate compression script for large videos"
    )

    args = parser.parse_args()

    compressor = VideoCompressor()

    if args.check:
        if compressor.check_ffmpeg():
            print("✅ ffmpeg is installed and ready to use")
        else:
            print("❌ ffmpeg is not installed")
            print("Install with: brew install ffmpeg")
        return

    # Load the workspace optimization report
    print("📊 Looking for workspace optimization report...")

    json_files = sorted(Path.cwd().glob("workspace_optimization_*.json"), reverse=True)
    if not json_files:
        print("❌ No workspace optimization report found.")
        print("Run workspace_optimizer.py first!")
        return

    with open(json_files[0]) as f:
        report = json.load(f)

    large_videos = report.get("large_videos", [])

    if not large_videos:
        print("✅ No large videos found!")
        return

    print(f"Found {len(large_videos)} large videos")
    total_size = sum(v["size"] for v in large_videos)
    print(f"Total size: {compressor.format_size(total_size)}")
    print(
        f"Estimated compression (50-70%): {compressor.format_size(total_size * 0.5)} - {compressor.format_size(total_size * 0.7)} savings"
    )
    print()

    # Generate compression script
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    script_path = args.generate_script or f"compress_videos_{timestamp}.sh"

    compressor.generate_compression_script(large_videos, script_path)

    print(f"✅ Compression script generated: {script_path}")
    print()
    print("📋 Next steps:")
    print("1. Install ffmpeg if needed: brew install ffmpeg")
    print(f"2. Review the script: cat {script_path}")
    print(f"3. Run compression: ./{script_path}")
    print()
    print("⚠️  Note: Video compression can take a long time!")
    print("   Estimated time: 5-10 minutes per GB of video")


if __name__ == "__main__":
    main()

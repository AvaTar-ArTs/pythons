from __future__ import annotations

import subprocess

# Constants
CONSTANT_1080 = 1080


def export_thumbnail(video_path: str, out_png: str, ss: float = 0.25):
    """export_thumbnail function."""

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-vf",
        "thumbnail,scale=CONSTANT_1080:-2",
        "-frames:v",
        "1",
        out_png,
    ]
    subprocess.check_call(cmd)

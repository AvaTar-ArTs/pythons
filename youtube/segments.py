from __future__ import annotations

import json
import math
import os
import re
import subprocess
from typing import Any, Dict, List, Tuple

from pydub import AudioSegment, silence
from scenedetect import SceneManager, VideoManager
from scenedetect.detectors import ContentDetector

# Constants
CONSTANT_600 = 600
CONSTANT_1000 = 1000



def detect_scenes(video_path: str, threshold: float = 27.0) -> List[Tuple[float, float]]:
    """Return list of (start_sec, end_sec) scene ranges using PySceneDetect."""
    vm = VideoManager([video_path])
    vm.set_downscale_factor()
    sm = SceneManager()
    sm.add_detector(ContentDetector(threshold=threshold))
    vm.start()
    scene_list = []
    sm.detect_scenes(vm)
    for s in sm.get_scene_list():
        start = s[0].get_seconds()
        end = s[1].get_seconds()
        scene_list.append((start, end))
    vm.release()
    return scene_list


def detect_silence_segments(
    audio_path: str, min_silence_len_ms: int = CONSTANT_600, silence_thresh_db: int = -35
):
    audio = AudioSegment.from_file(audio_path)
    chunks = silence.detect_nonsilent(
        audio, min_silence_len=min_silence_len_ms, silence_thresh=silence_thresh_db
    )
    # convert to seconds
    return [(s / CONSTANT_1000.0, e / CONSTANT_1000.0) for s, e in chunks]


def ffprobe_duration(video_path: str) -> float:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        video_path,
    ]
    out = subprocess.check_output(cmd).decode().strip()
    try:
        return float(out)
    except (ValueError, TypeError):
        return 0.0


def merge_overlaps(
    spans: List[Tuple[float, float]], pad: float = 0.15
) -> List[Tuple[float, float]]:
    if not spans:
        return []
    spans = sorted([(max(0.0, a - pad), b + pad) for a, b in spans])
    merged = [spans[0]]
    for a, b in spans[1:]:
        la, lb = merged[-1]
        if a <= lb:
            merged[-1] = (la, max(lb, b))
        else:
            merged.append((a, b))
    return merged

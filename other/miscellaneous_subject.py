"""
Subject-aware reframing using face/pose detection for intelligent cropping
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np


class SubjectTracker:
    def __init__(self):
        # Initialize face detection
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            self.profile_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_profileface.xml"
            )
        except (OSError, IOError, FileNotFoundError):
            self.face_cascade = None
            self.profile_cascade = None

    def track_segment(
        self,
        video_path: str,
        start_time: float,
        end_time: float,
        sample_rate: float = 0.5,
    ) -> List[Dict[str, Any]]:
        """Track subjects (faces, poses) in a video segment"""
        if not self.face_cascade:
            return []

        subjects = []
        duration = end_time - start_time

        # Sample frames at specified rate
        sample_times = np.arange(start_time, end_time, sample_rate)

        for t in sample_times:
            frame = self._extract_frame(video_path, t)
            if frame is not None:
                faces = self._detect_faces(frame)
                if faces:
                    subjects.append({"time": t, "faces": faces, "frame_shape": frame.shape})

        return subjects

    def _extract_frame(self, video_path: str, timestamp: float) -> Optional[np.ndarray]:
        """Extract a single frame at timestamp using ffmpeg"""
        try:
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                cmd = [
                    "ffmpeg",
                    "-y",
                    "-ss",
                    str(timestamp),
                    "-i",
                    video_path,
                    "-vframes",
                    "1",
                    "-q:v",
                    "2",
                    tmp.name,
                ]
                subprocess.run(cmd, capture_output=True, check=True)
                frame = cv2.imread(tmp.name)
                os.unlink(tmp.name)
                return frame
        except (OSError, IOError, FileNotFoundError):
            return None

    def _detect_faces(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Detect faces in frame"""
        if frame is None or self.face_cascade is None:
            return []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = frame.shape[:2]

        faces = []

        # Detect frontal faces
        frontal_faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        for x, y, w_face, h_face in frontal_faces:
            # Calculate center and confidence (size-based)
            center_x = x + w_face // 2
            center_y = y + h_face // 2
            confidence = min(
                1.0, (w_face * h_face) / (w * h) * CONSTANT_100
            )  # Larger faces = higher confidence

            faces.append(
                {
                    "type": "face",
                    "bbox": [x, y, w_face, h_face],
                    "center": [center_x / w, center_y / h],  # Normalized coordinates
                    "size": (w_face * h_face) / (w * h),  # Normalized size
                    "confidence": confidence,
                }
            )

        # If no frontal faces, try profile detection
        if not faces and self.profile_cascade:
            profile_faces = self.profile_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )

            for x, y, w_face, h_face in profile_faces:
                center_x = x + w_face // 2
                center_y = y + h_face // 2
                confidence = min(
                    1.0, (w_face * h_face) / (w * h) * 50
                )  # Lower confidence for profile

                faces.append(
                    {
                        "type": "profile",
                        "bbox": [x, y, w_face, h_face],
                        "center": [center_x / w, center_y / h],
                        "size": (w_face * h_face) / (w * h),
                        "confidence": confidence,
                    }
                )

        return faces


def generate_smooth_path(
    subjects: List[Dict[str, Any]],
    target_ar: float,
    duration: float,
    smoothing: float = 0.3,
) -> str:
    """Generate smooth camera path for subject-aware reframing"""
    if not subjects:
        # Fallback to center crop
        return f"crop='if(gte(iw/ih,{target_ar}),ih*{target_ar},iw)':'if(gte(iw/ih,{target_ar}),ih,iw/{target_ar})'"

    # Find the most prominent subject (largest, most confident)
    primary_subject = None
    max_score = 0

    for subject_frame in subjects:
        for face in subject_frame.get("faces", []):
            score = face["size"] * face["confidence"]
            if score > max_score:
                max_score = score
                primary_subject = {
                    "center": face["center"],
                    "size": face["size"],
                    "time": subject_frame["time"],
                }

    if not primary_subject:
        # No good subject found, center crop
        return f"crop='if(gte(iw/ih,{target_ar}),ih*{target_ar},iw)':'if(gte(iw/ih,{target_ar}),ih,iw/{target_ar})'"

    # Calculate crop parameters to keep subject in frame
    subject_x, subject_y = primary_subject["center"]
    subject_size = primary_subject["size"]

    # Ensure subject stays in frame with some padding
    padding = 0.1  # 10% padding around subject

    # For vertical crops (9:16), focus more on keeping face in upper third
    if target_ar < 1:  # Portrait
        crop_y = max(0.0, min(0.3, subject_y - 0.2))  # Keep in upper portion
        crop_x = max(0.0, min(1 - target_ar, subject_x - target_ar / 2))
    else:  # Landscape or square
        crop_x = max(0.0, min(1 - target_ar, subject_x - target_ar / 2))
        crop_y = max(0.0, min(1 - 1 / target_ar, subject_y - 1 / (2 * target_ar)))

    # For now, return static crop (smooth animation would need more complex FFmpeg filters)
    return f"crop='iw*{target_ar}:ih:iw*{crop_x}:ih*{crop_y}'"


class MotionTracker:
    """Advanced motion tracking for more sophisticated reframing"""
    def __init__(self):
        self.tracker = None

    def init_tracker(self, frame: np.ndarray, bbox: Tuple[int, int, int, int]) -> bool:
        """Initialize tracker with first detection"""
        try:
            self.tracker = cv2.TrackerCSRT_create()
            return self.tracker.init(frame, bbox)
        except (IndexError, KeyError):
            return False

    def update(self, frame: np.ndarray) -> Tuple[bool, Tuple[int, int, int, int]]:
        """Update tracker with new frame"""
        if self.tracker is None:
            return False, (0, 0, 0, 0)

        success, bbox = self.tracker.update(frame)
        return success, tuple(map(int, bbox)) if success else (0, 0, 0, 0)

"""
Summary of audio-normalize.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import logging
import random

from pydub import AudioSegment, effects

logger = logging.getLogger(__name__)


AMBIENT_DIR = "ambient"


def normalize_audio(seg: AudioSegment, target_dbfs: float = -14.0) -> AudioSegment:
    """🎚️ Normalize audio segment to a target dBFS level."""
    normalized_seg = effects.normalize(seg)
    gain_change = target_dbfs - normalized_seg.dBFS
    return normalized_seg.apply_gain(gain_change)


def random_voice() -> str:
    """🎤 Select a random voice from the available options."""
    voices = ["verse", "alloy", "cove"]
    selected_voice = random.choice(voices)
    logger.info(f"🔊 Selected voice: {selected_voice}")
    return selected_voice

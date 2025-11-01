"""
Utilities Misc Ptt 1

This module provides functionality for utilities misc ptt 1.

Author: Auto-generated
Date: 2025-11-01
"""

import pyttsx3

import logging

logger = logging.getLogger(__name__)


engine = pyttsx3.init()
voices = engine.getProperty("voices")
for voice in voices:
    logger.info(voice, voice.id)
    engine.setProperty("voice", voice.id)
    engine.say("Hello World!")
    engine.runAndWait()
    engine.stop()

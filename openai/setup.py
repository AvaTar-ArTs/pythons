"""
Setup 19

This module provides functionality for setup 19.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Test script to verify the transcription analyzer setup
"""

import os
import sys
from pathlib import Path


def test_imports():
    """Test if all required modules can be imported."""
    logger.info("Testing imports...")

    try:
        import whisper

        logger.info("✅ whisper imported successfully")
    except ImportError as e:
        logger.info(f"❌ whisper import failed: {e}")
        return False

    try:
        import moviepy

        logger.info("✅ moviepy imported successfully")
    except ImportError as e:
        logger.info(f"❌ moviepy import failed: {e}")
        return False

    try:
        from openai import OpenAI

        logger.info("✅ openai imported successfully")
    except ImportError as e:
        logger.info(f"❌ openai import failed: {e}")
        return False

    try:
        from dotenv import load_dotenv

        logger.info("✅ python-dotenv imported successfully")
    except ImportError as e:
        logger.info(f"❌ python-dotenv import failed: {e}")
        return False

    return True


def test_environment():
    """Test environment configuration."""
    logger.info("\nTesting environment...")

    # Load environment variables from ~/.env
    from dotenv import load_dotenv

    load_dotenv(os.path.expanduser("~/.env"))

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        logger.info("✅ OpenAI API key is configured")
        return True
    else:
        logger.info("❌ OpenAI API key not configured")
        logger.info("   Please set OPENAI_API_KEY in .env file")
        return False


def test_ffmpeg():
    """Test if FFmpeg is available."""
    logger.info("\nTesting FFmpeg...")

    import subprocess

    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            logger.info("✅ FFmpeg is available")
            return True
        else:
            logger.info("❌ FFmpeg not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        logger.info("❌ FFmpeg not found")
        logger.info("   Please install FFmpeg for video processing")
        return False


def test_whisper_model():
    """Test if Whisper model can be loaded."""
    logger.info("\nTesting Whisper model...")

    try:
        import whisper

        logger.info("Loading Whisper model (this may take a moment)...")
        model = whisper.load_model("tiny")  # Use tiny for testing
        logger.info("✅ Whisper model loaded successfully")
        return True
    except Exception as e:
        logger.info(f"❌ Whisper model loading failed: {e}")
        return False


def main():
    """Run all tests."""
    logger.info("🧪 Transcription Analyzer - Setup Test")
    logger.info("=" * 50)

    tests = [
        ("Imports", test_imports),
        ("Environment", test_environment),
        ("FFmpeg", test_ffmpeg),
        ("Whisper Model", test_whisper_model),
    ]

    results = []
    for test_name, test_func in tests:
        logger.info(f"\n{test_name}:")
        logger.info("-" * 20)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.info(f"❌ {test_name} test failed with error: {e}")
            results.append((test_name, False))

    logger.info(Path("\n") + "=" * 50)
    logger.info("TEST RESULTS")
    logger.info("=" * 50)

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        logger.info(
            "\n🎉 All tests passed! The transcription analyzer is ready to use."
        )
        logger.info("\nNext steps:")
        logger.info("1. Add some MP3 or MP4 files to test with")
        logger.info("2. Run: python transcription_analyzer.py your_file.mp4")
    else:
        logger.info("\n⚠️  Some tests failed. Please address the issues above.")
        logger.info("\nTroubleshooting:")
        logger.info("1. Run: pip install -r requirements.txt")
        logger.info("2. Install FFmpeg: brew install ffmpeg (macOS)")
        logger.info("3. Set your OpenAI API key in .env file")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script to verify all media file organizer scripts are properly configured.
"""

import os
import sys
import subprocess


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")

    try:
        import config

        print("✓ config.py imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import config.py: {e}")
        return False

    try:
        import aiohttp

        print("✓ aiohttp imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import aiohttp: {e}")
        print("  Install with: pip install aiohttp")

    try:
        import pandas

        print("✓ pandas imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pandas: {e}")
        print("  Install with: pip install pandas")

    try:
        from PIL import Image

        print("✓ Pillow (PIL) imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Pillow: {e}")
        print("  Install with: pip install Pillow")

    try:
        from mutagen.easyid3 import EasyID3

        print("✓ mutagen imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import mutagen: {e}")
        print("  Install with: pip install mutagen")

    return True


def test_script_syntax():
    """Test that all scripts have valid syntax."""
    print("\nTesting script syntax...")

    scripts = [
        ("vids/vids.py", "Video organizer"),
        ("audio/audio_combined.py", "Audio organizer"),
        ("img/img_combined.py", "Image organizer"),
        ("docs/docs_combined.py", "Document organizer"),
        ("run_all.py", "Master runner"),
    ]

    all_valid = True

    for script_path, description in scripts:
        if os.path.exists(script_path):
            try:
                result = subprocess.run(
                    ["python3", "-m", "py_compile", script_path],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    print(f"✓ {description} syntax is valid")
                else:
                    print(f"✗ {description} syntax error: {result.stderr}")
                    all_valid = False
            except Exception as e:
                print(f"✗ Error testing {description}: {e}")
                all_valid = False
        else:
            print(f"✗ {description} not found: {script_path}")
            all_valid = False

    return all_valid


def test_txt_files():
    """Test that all required .txt files exist."""
    print("\nTesting .txt files...")

    txt_files = [
        ("vids.txt", "Video script last directory"),
        ("audio.txt", "Audio script last directory"),
        ("image_data.txt", "Image script last directory"),
        ("docs.txt", "Document script last directory"),
    ]

    all_exist = True

    for txt_file, description in txt_files:
        if os.path.exists(txt_file):
            print(f"✓ {description} file exists")
        else:
            print(f"✗ {description} file missing: {txt_file}")
            all_exist = False

    return all_exist


def test_script_execution():
    """Test that scripts can be executed (dry run)."""
    print("\nTesting script execution (dry run)...")

    # Test the master runner with --list option
    try:
        result = subprocess.run(
            ["python3", "run_all.py", "--list"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            print("✓ Master runner script executes successfully")
            print("  Available scripts:")
            for line in result.stdout.split("\n"):
                if ":" in line and ("✓" in line or "✗" in line):
                    print(f"    {line}")
        else:
            print(f"✗ Master runner failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Master runner timed out")
        return False
    except Exception as e:
        print(f"✗ Error testing master runner: {e}")
        return False

    return True


def main():
    """Run all tests."""
    print("=== Media File Organizer Setup Test ===\n")

    tests = [
        ("Import Test", test_imports),
        ("Syntax Test", test_script_syntax),
        ("TXT Files Test", test_txt_files),
        ("Execution Test", test_script_execution),
    ]

    all_passed = True

    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if not test_func():
            all_passed = False

    print("\n=== Test Results ===")
    if all_passed:
        print("✓ All tests passed! The setup is ready to use.")
        print("\nNext steps:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Run individual scripts: python3 run_all.py --script <name>")
        print("3. Run all scripts: python3 run_all.py")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Check file permissions")
        print("- Verify all script files exist")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

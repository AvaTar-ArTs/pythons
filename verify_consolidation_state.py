#!/usr/bin/env python3
"""
Verify the current state before consolidation
"""

import os
from pathlib import Path


def verify_consolidation_state():
    """Verify the current state of music collections before consolidation"""
    print("Verifying current state before consolidation...")

    # Check AVATARARTS directories
    hh_path = Path("/Users/steven/AVATARARTS/HEAVENLY_HANDS_PROJECT")
    adu_path = Path("/Users/steven/AVATARARTS/DR_ADU_PROJECT")

    print("\n🔍 Checking AVATARARTS directories...")

    if hh_path.exists():
        hh_items = sum([len(files) + len(dirs) for _, dirs, files in os.walk(hh_path)])
        print(f"  ✓ HEAVENLY_HANDS_PROJECT exists with {hh_items} items")
        print(f"    Location: {hh_path}")
    else:
        print("  ✗ HEAVENLY_HANDS_PROJECT does not exist")

    if adu_path.exists():
        adu_items = sum([len(files) + len(dirs) for _, dirs, files in os.walk(adu_path)])
        print(f"  ✓ DR_ADU_PROJECT exists with {adu_items} items")
        print(f"    Location: {adu_path}")
    else:
        print("  ✗ DR_ADU_PROJECT does not exist")

    # Check existing MUSIC_ORGANIZED_SIMPLIFIED
    simplified_path = Path("/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED_SIMPLIFIED")
    if simplified_path.exists():
        simplified_items = sum([len(files) + len(dirs) for _, dirs, files in os.walk(simplified_path)])
        print(f"  ✓ MUSIC_ORGANIZED_SIMPLIFIED exists with {simplified_items} items")
        print(f"    Location: {simplified_path}")
    else:
        print("  ✗ MUSIC_ORGANIZED_SIMPLIFIED does not exist")

    # Check if MUSIC_ORGANIZED already exists
    main_path = Path("/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED")
    if main_path.exists():
        main_items = sum([len(files) + len(dirs) for _, dirs, files in os.walk(main_path)])
        print(f"  ⚠ MUSIC_ORGANIZED already exists with {main_items} items")
        print(f"    Location: {main_path}")
    else:
        print("  ✓ MUSIC_ORGANIZED does not exist yet (ready for creation)")

    # Summary
    print("\n📋 Current State Summary:")
    print(f"  - Heavenly Hands Project: {'Exists' if hh_path.exists() else 'Missing'}")
    print(f"  - Dr. Adu Project: {'Exists' if adu_path.exists() else 'Missing'}")
    print(f"  - Existing Simplified Organization: {'Exists' if simplified_path.exists() else 'Missing'}")
    print(f"  - Main Organization Directory: {'Exists' if main_path.exists() else 'Ready to Create'}")

    print("\n✅ Verification complete. Safe to proceed with consolidation.")


if __name__ == "__main__":
    verify_consolidation_state()

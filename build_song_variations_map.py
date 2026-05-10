#!/usr/bin/env python3
"""
Build song -> variations mapping (JSON) for browse/display.

Uses CSV sources (albums-metadata, COMPLETE_MUSIC_COLLECTION_INVENTORY, Suno exports)
plus folder scan. Output: AI_ENHANCED_ORGANIZATION/DATA/song_variations_map.json

Usage:
  python3 build_song_variations_map.py
"""

from csv_song_mapping import build_and_save

if __name__ == "__main__":
    build_and_save()

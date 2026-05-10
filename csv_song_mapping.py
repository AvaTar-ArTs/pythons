#!/usr/bin/env python3
"""
Build song -> variations mapping from CSV sources and song titles.

Sources:
  - albums-metadata.csv: Album Name + Related Tracks
  - COMPLETE_MUSIC_COLLECTION_INVENTORY.csv: Album Series + Directory
  - suno-export-*.csv: title (song names)

Output: song_variations_map.json (canonical song -> variations for browse/display)
"""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

PROJECT = Path(__file__).parent
DATA_DIR = PROJECT / "AI_ENHANCED_ORGANIZATION" / "DATA"
ALBUMS_DIR = PROJECT / "ALBUMS"
OUTPUT_PATH = DATA_DIR / "song_variations_map.json"


def normalize(s: str) -> str:
    """Lowercase, collapse spaces/underscores/dashes for comparison."""
    s = re.sub(r"[_\-\s]+", " ", s.lower().strip())
    s = re.sub(r"[^\w\s]", "", s)
    return re.sub(r"\s+", "_", s.strip("_"))


def title_to_folder(title: str) -> str:
    """'Petals Fall' -> 'Petals_Fall'"""
    s = re.sub(r'[<>:"/\\|?*]', "", title)
    s = re.sub(r"\s+", "_", s.strip())
    return s or "Untitled"


def load_albums_metadata() -> dict[str, list[str]]:
    """Album Name -> [variation folder names]. Source: albums-metadata.csv"""
    path = DATA_DIR / "albums-metadata.csv"
    if not path.exists():
        return {}
    out = defaultdict(set)
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            album = (row.get("Album Name") or "").strip()
            related = (row.get("Related Tracks") or "").strip()
            if not album:
                continue
            canonical = title_to_folder(album)
            out[normalize(album)].add(canonical)
            for part in re.split(r"[,;]+", related):
                part = part.strip().strip("_")
                if part:
                    out[normalize(album)].add(part)
    return {k: list(v) for k, v in out.items()}


def load_inventory() -> dict[str, list[str]]:
    """Album Series (song title) -> [folder names]. Source: COMPLETE_MUSIC_COLLECTION_INVENTORY.csv"""
    path = DATA_DIR / "COMPLETE_MUSIC_COLLECTION_INVENTORY.csv"
    if not path.exists():
        return {}
    out = defaultdict(set)
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            series = (row.get("Album Series") or "").strip()
            directory = (row.get("Directory") or "").strip()
            if not series or not directory:
                continue
            folder = Path(directory).name
            out[normalize(series)].add(folder)
    return {k: list(v) for k, v in out.items()}


def load_suno_titles() -> set[str]:
    """Unique song titles from Suno exports."""
    titles = set()
    for p in DATA_DIR.glob("suno-export-*.csv"):
        try:
            with open(p, encoding="utf-8") as f:
                r = csv.DictReader(f)
                for row in r:
                    t = (row.get("title") or "").strip()
                    t = re.sub(r"^#+\s*", "", t)
                    t = re.sub(r"\*\*|🌀|" "", "", t)
                    t = t.strip()
                    if t and t.lower() != "untitled":
                        titles.add(t)
        except Exception:
            pass
    return titles


def scan_albums_folders() -> dict[str, list[Path]]:
    """From ALBUMS dir: infer groups by folder name prefix matching."""
    if not ALBUMS_DIR.exists():
        return {}
    folders = [
        p
        for p in ALBUMS_DIR.iterdir()
        if p.is_dir()
        and not p.name.startswith(".")
        and p.name not in ("consolidate_nested_albums.py",)
        and p.suffix != ".json"
    ]
    # Group by normalized prefix (first 2 segments): Petals_Fall_X -> petals_fall
    groups = defaultdict(list)
    for p in folders:
        parts = re.split(r"[_\-\d]+", p.name, maxsplit=2)
        base = "_".join(p for p in parts[:2] if p).lower() or normalize(p.name)
        groups[base].append(p)
    return {k: v for k, v in groups.items() if len(v) >= 2}


def merge_mappings(albums: dict, inventory: dict, suno_titles: set[str], folder_scan: dict) -> dict:
    """
    Merge CSV + scan into one mapping.
    Key = normalized song title. Value = { display_name, canonical_folder, variations }.
    """
    merged = {}

    # 1. albums-metadata (authoritative when present)
    for key, folders in albums.items():
        display = re.sub(r"_", " ", key).title()
        canonical = title_to_folder(display)
        if folders:
            prefer = [f for f in folders if normalize(f) == key or f == canonical]
            canonical = min(prefer, key=len) if prefer else min(folders, key=lambda x: (len(x), x))
        else:
            canonical = title_to_folder(display)
        merged[key] = {
            "display_name": display,
            "canonical_folder": canonical,
            "variations": sorted(set(folders)) if folders else [canonical],
            "source": "albums-metadata",
        }

    # 2. inventory (Album Series -> folders)
    for key, folders in inventory.items():
        display = re.sub(r"_", " ", key).title()
        canonical = title_to_folder(display)
        if canonical not in folders and folders:
            canonical = min(folders, key=lambda x: (len(x), x))
        if key in merged:
            merged[key]["variations"] = sorted(set(merged[key]["variations"]) | set(folders))
            merged[key]["source"] = "albums-metadata+inventory"
        else:
            merged[key] = {
                "display_name": display,
                "canonical_folder": canonical,
                "variations": sorted(folders),
                "source": "inventory",
            }

    # 3. Suno titles (add as single-folder entries if not present)
    for title in suno_titles:
        key = normalize(title)
        if key and key not in merged:
            folder = title_to_folder(title)
            merged[key] = {
                "display_name": title,
                "canonical_folder": folder,
                "variations": [folder],
                "source": "suno",
            }

    # 4. folder scan: add groups not in CSV
    for key, paths in folder_scan.items():
        if key not in merged:
            names = [p.name for p in paths]
            canonical = min(names, key=lambda x: (len(x), x))
            display = re.sub(r"_", " ", key).title()
            merged[key] = {
                "display_name": display,
                "canonical_folder": canonical,
                "variations": sorted(names),
                "source": "folder_scan",
            }

    return merged


def build_and_save() -> dict:
    albums = load_albums_metadata()
    inventory = load_inventory()
    suno = load_suno_titles()
    scan = scan_albums_folders()
    merged = merge_mappings(albums, inventory, suno, scan)

    # Enrich with file counts (from ALBUMS)
    result = {}
    for key, v in merged.items():
        variations = v["variations"]
        file_count = 0
        for fname in variations:
            p = ALBUMS_DIR / fname
            if p.exists() and p.is_dir():
                file_count += sum(1 for x in p.rglob("*") if x.is_file())
        result[v["canonical_folder"]] = {
            "display_name": v["display_name"],
            "canonical_folder": v["canonical_folder"],
            "variations": variations,
            "variation_count": len(variations),
            "file_count": file_count,
            "source": v.get("source", "merged"),
        }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Wrote {len(result)} song entries to {OUTPUT_PATH}")
    print(
        f"  Sources: albums-metadata={len(albums)}, inventory={len(inventory)}, suno_titles={len(suno)}, folder_scan={len(scan)}"
    )
    return result


if __name__ == "__main__":
    build_and_save()

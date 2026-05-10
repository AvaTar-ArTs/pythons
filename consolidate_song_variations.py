#!/usr/bin/env python3
"""
Consolidate song variation folders into single album folders.

E.g. Petals_Fall, Petals_Fall_(duo_344), Petals_Fall_Banjo, etc. -> one Petals_Fall/

Uses CSV/song-title mapping when --csv: albums-metadata, inventory, Suno exports.
Otherwise uses heuristic folder-name grouping.

Usage:
  python3 consolidate_song_variations.py          # dry run (heuristic)
  python3 consolidate_song_variations.py --apply  # perform consolidation
  python3 consolidate_song_variations.py --csv    # use CSV-based mapping
  python3 consolidate_song_variations.py --csv --apply
"""

import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

ALBUMS_DIR = Path(__file__).parent / "ALBUMS"

# Typo/abbreviation overrides: variant_key -> canonical_key
OVERRIDES = {
    "petals": "petals_fall",
    "petasls": "petals_fall",
}


def normalize(s: str) -> str:
    """Lowercase, collapse underscores."""
    return re.sub(r"[_\-]+", "_", s.lower()).strip("_")


def base_key(folder_name: str) -> str:
    """
    Extract base song key from folder name.
    Petals_Fall_(duo_344) -> petals_fall
    Petals_Fall_Remastered0326 -> petals_fall
    PETALS_FALL_ROOTS_REMAIN -> petals_fall
    Petals0308, Petals_Fall0000, Petasls0249 -> petals_fall (via overrides)
    """
    s = folder_name
    # Remove parenthetical suffix
    s = re.sub(r"_[(_][^)]*\).*$", "", s)
    s = re.sub(r"_\([^)]*\)$", "", s)
    # Remove trailing version numbers (with or without leading _)
    s = re.sub(r"_\d{3,}.*$", "", s)
    s = re.sub(r"_\d+$", "", s)
    s = re.sub(r"\d{4,}$", "", s)  # Petals_Fall0000 -> Petals_Fall, Petals0308 -> Petals
    # Remove common variation suffixes (keep base)
    for suffix in [
        r"_Remastered\d*.*",
        r"_Remix.*",
        r"_Anime.*",
        r"_Banjo.*",
        r"_Yah_Yah.*",
        r"_Roots_Remain.*",
        r"_Yet_Roots_Remain.*",
        r"_flutr\d*.*",
        r"_duo_\d+.*",
        r"_indie_Folk.*",
        r"_Ballad.*",
        r"_Ed\).*",
    ]:
        s = re.sub(suffix, "", s, flags=re.I)
    s = s.strip("_")
    key = normalize(s)
    return OVERRIDES.get(key, key) if key else normalize(folder_name)


def get_families() -> dict[str, list[Path]]:
    """Group album folders by base key."""
    families = defaultdict(list)
    for item in ALBUMS_DIR.iterdir():
        if not item.is_dir() or item.name.startswith("."):
            continue
        if item.name in ("consolidate_nested_albums.py",) or item.suffix == ".json":
            continue
        key = base_key(item.name)
        families[key].append(item)

    # Keep only families with 2+ folders. Sort: prefer folder name that matches base key, then shortest.
    def canonical_rank(p: Path, key: str) -> tuple:
        return (0 if normalize(p.name) == key else 1, len(p.name), p.name)

    return {k: sorted(v, key=lambda p: canonical_rank(p, k)) for k, v in families.items() if len(v) >= 2}


def get_families_from_csv() -> dict[str, list[Path]]:
    """Group folders using CSV-based song mapping."""
    from csv_song_mapping import build_and_save

    data = build_and_save()
    families = {}
    for canonical_name, entry in data.items():
        variations = entry.get("variations", [])
        if len(variations) < 2:
            continue
        paths = []
        seen = set()
        for v in variations:
            p = ALBUMS_DIR / v
            if p.exists() and p.is_dir():
                rp = p.resolve()
                if rp not in seen:
                    seen.add(rp)
                    paths.append(p)
        if len(paths) >= 2:
            canonical_path = ALBUMS_DIR / canonical_name
            if canonical_path in paths:
                sorted_paths = [canonical_path] + [x for x in paths if x != canonical_path]
            else:
                sorted_paths = sorted(paths, key=lambda x: (len(x.name), x.name))
            families[canonical_name] = sorted_paths
    return families


def consolidate(families: dict[str, list[Path]], dry_run: bool) -> dict:
    """Merge variation folders into canonical (shortest) folder."""
    stats = {
        "merged": 0,
        "files_moved": 0,
        "folders_removed": 0,
        "conflicts": 0,
        "errors": [],
    }
    mode = "DRY RUN - " if dry_run else ""

    for key, folders in sorted(families.items()):
        canonical = folders[0]
        variants = folders[1:]
        if canonical.name == variants[0].name:
            continue
        print(f"\n{mode}[{key}] canonical: {canonical.name}/")
        for var in variants:
            print(f"  <- {var.name}/")
            if dry_run:
                count = sum(1 for _ in var.rglob("*") if _.is_file())
                stats["files_moved"] += count
                stats["merged"] += 1
                continue
            try:
                for f in var.rglob("*"):
                    if not f.is_file():
                        continue
                    rel = f.relative_to(var)
                    dest = canonical / rel
                    if dest.exists():
                        stem, ext = dest.stem, dest.suffix
                        i = 1
                        while dest.exists():
                            dest = dest.parent / f"{stem}_{i}{ext}"
                            i += 1
                        stats["conflicts"] += 1
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(f), str(dest))
                    stats["files_moved"] += 1
                # Remove empty dirs in variant
                for d in sorted(var.rglob("*"), key=lambda x: -len(x.parts)):
                    if d.is_dir() and not any(d.iterdir()):
                        d.rmdir()
                if not any(var.iterdir()):
                    var.rmdir()
                    stats["folders_removed"] += 1
                stats["merged"] += 1
            except Exception as e:
                stats["errors"].append(f"{var}: {e}")
                print(f"    ERROR: {e}")

    return stats


def main():
    dry_run = "--apply" not in sys.argv
    use_csv = "--csv" in sys.argv
    families = get_families_from_csv() if use_csv else get_families()
    mode = " (CSV-based)" if use_csv else ""
    print(f"Found {len(families)} song families with 2+ variation folders{mode}")
    for key, folders in list(families.items())[:15]:
        print(f"  {key}: {len(folders)} folders")
    stats = consolidate(families, dry_run)
    print("\n--- Summary ---")
    print(f"  Families merged: {stats['merged']}")
    print(f"  Files moved: {stats['files_moved']}")
    print(f"  Folders removed: {stats['folders_removed']}")
    print(f"  Conflicts (renamed): {stats['conflicts']}")
    if stats["errors"]:
        print(f"  Errors: {len(stats['errors'])}")
        for e in stats["errors"][:5]:
            print(f"    {e}")
    if dry_run:
        print("\nRun with --apply to perform consolidation.")


if __name__ == "__main__":
    main()

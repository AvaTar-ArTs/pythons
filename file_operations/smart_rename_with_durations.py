import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""from collections import defaultdict
from pathlib import Path
import csv
import re
?? SMART RENAMER WITH DURATION PRESERVATION
Preserves duration codes (234 = 2:34) and version numbers
"""


def extract_duration_from_number(num_str: str) -> str:
    """Convert 234 -> 2:34, 359 -> 3:59"""
    if len(num_str) == 3 and num_str.isdigit():
        minutes = num_str[0]
        seconds = num_str[1:3]
        if int(seconds) < 60:  # Valid seconds
            return f"{minutes}:{seconds}"
    return None


def parse_filename_components(filename: str) -> dict:
    """Extract: base name, duration, version, tags"""
    # Extract duration from (2:34) or (3:59) format
    duration_match = re.search(r"\((\d+:\d+)\)", filename)
    duration_from_parens = duration_match.group(1) if duration_match else None

    # Extract duration from _234 or _359 format
    number_match = re.search(r"_(\d{3})(?:$|[^0-9])", filename)
    duration_from_code = None
    if number_match:
        code = number_match.group(1)
        duration_from_code = extract_duration_from_number(code)

    # Extract version (_1, _2, (1), (2))
    version_match = re.search(r"[_\(](\d)[_\)]", filename)
    version = version_match.group(1) if version_match else None

    # Extract tags (Edit, Remix, Remastered, etc)
    tags = []
    tag_patterns = [
        r"\[?(Edit)\]?",
        r"\[?(Remix)\]?",
        r"\[?(Remastered)\]?",
        r"\[?(Cover)\]?",
        r"\[?(Live)\]?",
    ]
    for pattern in tag_patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            tags.append(match.group(1).capitalize())

    # Get base name (remove all the extras)
    base = filename
    base = re.sub(r"\(\d+:\d+\)", "", base)  # Remove (2:34)
    base = re.sub(r"_\d{3}(?:$|[^0-9])", "", base)  # Remove _234
    base = re.sub(r"[_\(]\d[_\)]", "", base)  # Remove _1 or (1)
    base = re.sub(
        r"\s*-\s*\[?(Edit|Remix|Remastered|Cover|Live)\]?",
        "",
        base,
        flags=re.IGNORECASE,
    )
    base = base.replace("_", " ").replace("-", " ")
    base = " ".join(base.split()).strip()
    base = base.title()

    return {
        "base": base,
        "duration": duration_from_code or duration_from_parens,
        "version": version,
        "tags": tags,
    }


def create_smart_name(components: dict, avoid_duplicates: set) -> str:
    """Create clean name with duration preserved"""
    parts = [components["base"]]

    # Add duration if present
    if components["duration"]:
        parts.append(f"({components['duration']})")

    # Add tags
    if components["tags"]:
        parts.extend(f"[{tag}]" for tag in components["tags"])

    # Create name
    name = " ".join(parts)

    # Handle duplicates by adding version
    original_name = name
    counter = 1
    while name in avoid_duplicates:
        counter += 1
        name = f"{original_name} v{counter}"

    return name


def smart_rename():
    """Smart rename preserving durations"""
    print("\n" + "=" * 80)
    print("  ?? SMART RENAMER WITH DURATION PRESERVATION")
    print("  Preserves: 234 ? (2:34), 359 ? (3:59)")
    print("=" * 80 + "\n")

    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
    fuzzy_csv = base_dir / "TRANSCRIPT_MATCHING" / "FUZZY_MATCHES.csv"

    if not fuzzy_csv.exists():
        print("? Run match_transcripts.py first!")
        return

    # Load fuzzy matches
    with open(fuzzy_csv) as f:
        reader = csv.DictReader(f)
        fuzzy_matches = list(reader)

    print(f"?? Loaded {len(fuzzy_matches)} fuzzy-matched pairs\n")

    # Process each folder
    folders = [d for d in base_dir.iterdir() if d.is_dir() and d.name[0].isupper()]

    all_renames = []

    for folder in sorted(folders):
        mp3_files = {f.stem: f for f in folder.glob("*.mp3")}
        txt_files = {f.stem: f for f in folder.glob("*.txt")}

        if not mp3_files:
            continue

        print(f"?? {folder.name}")
        print(f"   MP3s: {len(mp3_files)} | TXTs: {len(txt_files)}")

        # Get matches for this folder
        folder_matches = [m for m in fuzzy_matches if m["folder"] == folder.name]

        used_names = set()
        folder_renames = []

        for match in folder_matches:
            mp3_stem = match["mp3"]
            txt_stem = match["txt"]

            # Parse MP3 filename
            mp3_components = parse_filename_components(mp3_stem)

            # Create smart name
            smart_name = create_smart_name(mp3_components, used_names)
            used_names.add(smart_name)

            # Create rename entries
            mp3_old = folder / f"{mp3_stem}.mp3"
            txt_old = folder / f"{txt_stem}.txt"
            mp3_new = folder / f"{smart_name}.mp3"
            txt_new = folder / f"{smart_name}.txt"

            if mp3_old.exists() and mp3_old.name != mp3_new.name:
                folder_renames.append(
                    {
                        "type": "mp3",
                        "folder": folder.name,
                        "old_path": str(mp3_old),
                        "new_path": str(mp3_new),
                        "old_name": mp3_stem,
                        "new_name": smart_name,
                        "duration": mp3_components["duration"] or "N/A",
                    },
                )

            if txt_old.exists() and txt_old.name != txt_new.name:
                folder_renames.append(
                    {
                        "type": "txt",
                        "folder": folder.name,
                        "old_path": str(txt_old),
                        "new_path": str(txt_new),
                        "old_name": txt_stem,
                        "new_name": smart_name,
                        "duration": mp3_components["duration"] or "N/A",
                    },
                )

        if folder_renames:
            print(f"   ?? Proposing {len(folder_renames)} renames")

            # Show examples with durations
            for rename in folder_renames[:4]:
                duration_str = (
                    f" [{rename['duration']}]" if rename["duration"] != "N/A" else ""
                )
                print(
                    f"      {rename['type'].upper()}: {rename['old_name'][:40]}{duration_str}",
                )
                print(f"           ? {rename['new_name'][:50]}")

            if len(folder_renames) > 4:
                print(f"      ... and {len(folder_renames) - 4} more")

            all_renames.extend(folder_renames)

        print()

    if all_renames:
        # Save plan
        plan_csv = base_dir / "SMART_RENAME_PLAN.csv"

        with open(plan_csv, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "type",
                    "folder",
                    "old_path",
                    "new_path",
                    "old_name",
                    "new_name",
                    "duration",
                ],
            )
            writer.writeheader()
            writer.writerows(all_renames)

        print("=" * 80)
        print("  ?? SMART RENAME SUMMARY")
        print("=" * 80 + "\n")

        mp3_renames = [r for r in all_renames if r["type"] == "mp3"]
        txt_renames = [r for r in all_renames if r["type"] == "txt"]

        with_duration = [r for r in all_renames if r["duration"] != "N/A"]

        print(f"Total renames proposed: {len(all_renames)}")
        print(f"  ? MP3 files: {len(mp3_renames)}")
        print(f"  ? TXT files: {len(txt_renames)}")
        print(f"  ? With duration preserved: {len(with_duration)}")
        print()

        # Check for duplicates in new names
        new_names = [r["new_name"] for r in all_renames]
        duplicates = {
            name: new_names.count(name)
            for name in set(new_names)
            if new_names.count(name) > 1
        }

        if duplicates:
            print(f"??  Duplicate target names found: {len(duplicates)}")
            print("   (These will be handled by adding version numbers)")
            print()

        print("?? Smart rename plan saved: SMART_RENAME_PLAN.csv")
        print()
        print("? Duration codes preserved:")
        print("   ? _234 ? (2:34)")
        print("   ? _359 ? (3:59)")
        print("   ? etc.")
        print()
    else:
        print("? All files already properly named!")


try:
        smart_rename()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)
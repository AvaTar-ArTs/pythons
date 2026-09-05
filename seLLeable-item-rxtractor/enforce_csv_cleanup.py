#!/usr/bin/env python3
"""
nocturneMelodies — CSV-Enforced Cleanup
CSV rows = EXACT number of tracks allowed in DISCO.
Move all extras to DISCO/_EXTRAS/. Keep only CSV-matched MP3s.
"""

import csv
import os
import json
import re
import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path

SUNO_CSV = "/Users/steven/Music/nocturneMelodies/suno-937.csv"
DISCO_DIR = Path("/Users/steven/Music/nocturneMelodies/DISCO")
EXTRAS_DIR = DISCO_DIR / "_EXTRAS"
REPORT_DIR = Path("/Users/steven/Music/nocturneMelodies")


def normalize(s):
    s = s.lower().strip()
    s = re.sub(r'[##*"\']', '', s)
    s = re.sub(r'[\s_\-]+', ' ', s)
    s = re.sub(r'[^a-z0-9 ]', '', s)
    return s


def load_csv():
    """Load THE authoritative catalog."""
    tracks = {}
    with open(SUNO_CSV, "r", encoding="utf-8", errors="ignore") as f:
        for row in csv.DictReader(f):
            uid = row.get("ID", "").strip()
            if not uid:
                continue
            title = row.get("Title", "").strip().strip('"').strip("'")
            title = title.replace("## ", "").replace("### ", "").replace("**", "").strip()
            album = title.split(",")[0].strip() if "," in title else title
            if not album:
                album = "Misc"
            safe_album = re.sub(r'[^a-zA-Z0-9 _-]', '', album)[:80]
            tracks[uid] = {
                "title": title,
                "album": album,
                "safe_album": safe_album,
                "norm_title": normalize(title),
                "norm_album": normalize(album),
                "duration": row.get("Duration", "0:00"),
            }
    print(f"📖 CSV loaded: {len(tracks)} authoritative tracks")
    return tracks


def scan_all_mp3s(base_dir):
    """Scan all MP3s, return list of {path, filename, parent_album_dir}."""
    files = []
    for root, dirs, fnames in os.walk(base_dir):
        if "_EXTRAS" in root:
            continue
        for f in fnames:
            if f.endswith(".mp3") and not os.path.islink(os.path.join(root, f)):
                files.append({
                    "path": os.path.join(root, f),
                    "filename": f,
                    "norm": normalize(f),
                    "parent": os.path.basename(root),
                })
    print(f"🔍 Found {len(files)} MP3s in DISCO")
    return files


def match_mp3_to_csv(mp3, csv_tracks):
    """Try to match an MP3 file to a CSV track."""
    fn_norm = mp3["norm"]
    parent_norm = normalize(mp3["parent"])

    # Strategy 1: Extract potential UUID from filename
    uuid_match = re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', mp3["filename"])
    if uuid_match:
        for uid in uuid_match:
            if uid in csv_tracks:
                return uid

    # Strategy 2: Match by album + title words
    for uid, track in csv_tracks.items():
        # Check if track's title words appear in the filename
        title_words = track["norm_title"].split()
        if len(title_words) >= 2:
            # Check if first 2-3 meaningful words of title are in the filename
            match_count = sum(1 for w in title_words[:4] if len(w) > 3 and w in fn_norm)
            if match_count >= 2:
                # Also check album match
                if track["norm_album"] in parent_norm or parent_norm in track["norm_album"]:
                    return uid

    return None


def _file_identity(path):
    stat = os.lstat(path)
    if not stat or os.path.islink(path):
        raise ValueError(f"refusing symlink source: {path}")
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return {"sha256": digest.hexdigest(), "device": stat.st_dev, "inode": stat.st_ino}


def _write_changeset(path, entries):
    changeset = {
        "schema_version": "1.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "operation": "move-unmatched-mp3s",
        "status": "planned",
        "entries": entries,
    }
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(changeset, indent=2) + "\n", encoding="utf-8")
    return output


def _read_changeset(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0" or not isinstance(data.get("entries"), list):
        raise ValueError("invalid cleanup changeset")
    return data


def apply_changeset(path):
    """Apply a previously written plan without recomputing destinations."""
    changeset = _read_changeset(path)
    if changeset.get("status") not in {"planned", "partial"}:
        raise ValueError(f"changeset is not applicable: {changeset.get('status')}")
    applied = 0
    for entry in changeset["entries"]:
        source = Path(entry["source"])
        target = Path(entry["target"])
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"source changed or is unavailable: {source}")
        identity = _file_identity(source)
        if identity != entry["identity"]:
            raise ValueError(f"source identity changed: {source}")
        if target.exists() or target.is_symlink():
            raise ValueError(f"destination already exists: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(source, target)
        except FileExistsError:
            raise ValueError(f"destination appeared during apply: {target}")
        except OSError as error:
            if error.errno == 18:
                raise ValueError("cleanup requires source and destination on one filesystem") from error
            raise
        if _file_identity(target)["sha256"] != entry["identity"]["sha256"]:
            target.unlink(missing_ok=True)
            raise ValueError(f"destination verification failed: {target}")
        source.unlink()
        entry["status"] = "applied"
        entry["rollback"] = {"source": str(target), "destination": str(source)}
        applied += 1
        changeset["status"] = "partial"
        Path(path).write_text(json.dumps(changeset, indent=2) + "\n", encoding="utf-8")
    changeset["status"] = "applied" if applied == len(changeset["entries"]) else "partial"
    Path(path).write_text(json.dumps(changeset, indent=2) + "\n", encoding="utf-8")
    return changeset


def rollback_changeset(path):
    """Restore applied moves after revalidating destination identity."""
    changeset = _read_changeset(path)
    restored = 0
    for entry in reversed(changeset["entries"]):
        if entry.get("status") != "applied":
            continue
        source = Path(entry["rollback"]["source"])
        target = Path(entry["rollback"]["destination"])
        if source.is_symlink() or not source.is_file() or target.exists() or target.is_symlink():
            raise ValueError(f"rollback boundary changed: {source} -> {target}")
        if _file_identity(source)["sha256"] != entry["identity"]["sha256"]:
            raise ValueError(f"rollback identity changed: {source}")
        os.link(source, target)
        source.unlink()
        entry["status"] = "rolled_back"
        restored += 1
    changeset["status"] = "rolled_back" if restored == len(changeset["entries"]) else "partial"
    Path(path).write_text(json.dumps(changeset, indent=2) + "\n", encoding="utf-8")
    return changeset


def enforce_csv(csv_tracks, all_mp3s, *, apply=False, extras_dir=None):
    """Plan or apply CSV enforcement.

    The default creates a read-only plan. Applying requires a persisted
    changeset and ``apply_changeset()``.
    """
    target_dir = Path(extras_dir) if extras_dir else EXTRAS_DIR
    if apply:
        raise ValueError("apply must use apply_changeset() with a persisted plan")
    stats = {
        "total_mp3s": len(all_mp3s),
        "csv_matched": 0,
        "moved_to_extras": 0,
        "missing_from_csv": 0,
        "matched_details": [],
        "moved_files": [],
        "planned_files": [],
        "apply": apply,
    }

    # Match all MP3s
    matched_mp3s = set()
    for mp3 in all_mp3s:
        uid = match_mp3_to_csv(mp3, csv_tracks)
        if uid:
            stats["csv_matched"] += 1
            matched_mp3s.add(mp3["path"])
            stats["matched_details"].append({
                "mp3": mp3["filename"],
                "csv_track": csv_tracks[uid]["title"][:50],
                "album": csv_tracks[uid]["safe_album"],
            })

    # Move unmatched to _EXTRAS
    if apply:
        target_dir.mkdir(parents=True, exist_ok=True)
    reserved_targets = set()
    for mp3 in all_mp3s:
        if mp3["path"] not in matched_mp3s:
            target = target_dir / mp3["filename"]
            # Handle filename conflicts
            counter = 1
            while target.exists() or str(target) in reserved_targets:
                stem = Path(mp3["filename"]).stem
                ext = Path(mp3["filename"]).suffix
                target = target_dir / f"{stem}_{counter}{ext}"
                counter += 1
            detail = {
                "source": mp3["path"],
                "target": str(target),
                "filename": mp3["filename"],
                "status": "planned",
                "rollback": {
                    "source": str(target),
                    "destination": mp3["path"],
                },
            }
            if not apply:
                detail["identity"] = _file_identity(mp3["path"])
            stats["planned_files"].append(detail)
            reserved_targets.add(str(target))

    # Check which CSV tracks are missing MP3s
    matched_csv_uids = set()
    for detail in stats["matched_details"]:
        for uid, track in csv_tracks.items():
            if detail["csv_track"].startswith(track["title"][:30]):
                matched_csv_uids.add(uid)

    stats["missing_from_csv"] = len(csv_tracks) - len(matched_csv_uids)

    return stats


def print_report(stats):
    print(f"\n{'='*60}")
    print("📊 CSV-Enforced Cleanup Report")
    print(f"{'='*60}\n")
    print(f"  Total MP3s in DISCO:           {stats['total_mp3s']:>6}")
    print(f"  Matched to CSV (kept):          {stats['csv_matched']:>6}")
    print(f"  Moved to _EXTRAS/:              {stats['moved_to_extras']:>6}")
    print(f"  CSV tracks missing MP3s:        {stats['missing_from_csv']:>6}")
    print(f"\n  DISCO now contains exactly:     {stats['csv_matched']} / {stats['total_mp3s']} original MP3s")
    print(f"  _EXTRAS/ contains:               {stats['moved_to_extras']} files\n")

    if stats['moved_files']:
        print(f"📦 Moved to _EXTRAS/ (first 10):")
        for f in stats['moved_files'][:10]:
            print(f"  → {f}")
        if len(stats['moved_files']) > 10:
            print(f"  ... and {len(stats['moved_files']) - 10} more")


def save_report(stats):
    report = {
        "summary": {
            "total_mp3s": stats["total_mp3s"],
            "csv_matched": stats["csv_matched"],
            "moved_to_extras": stats["moved_to_extras"],
            "missing_from_csv": stats["missing_from_csv"],
            "apply": stats.get("apply", False),
            "planned_files": len(stats.get("planned_files", [])),
        },
        "moved_files": stats["moved_files"][:100],
        "planned_files": stats.get("planned_files", [])[:100],
        "matched_sample": stats["matched_details"][:50],
    }
    path = REPORT_DIR / "csv_enforced_report.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2))
    print(f"📋 Full report: {path}")


def main():
    global SUNO_CSV, DISCO_DIR, EXTRAS_DIR, REPORT_DIR

    parser = argparse.ArgumentParser(description="Plan or apply CSV-enforced music cleanup")
    parser.add_argument("--csv", default=SUNO_CSV, help="Authoritative catalog CSV")
    parser.add_argument("--disco", default=str(DISCO_DIR), help="Directory containing MP3s")
    parser.add_argument("--report-dir", default=str(REPORT_DIR), help="Report output directory")
    parser.add_argument("--apply", action="store_true", help="Move unmatched MP3s to _EXTRAS")
    parser.add_argument(
        "--changeset",
        help="Changeset JSON path (default: <report-dir>/cleanup-changeset.json)",
    )
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Rollback an applied changeset instead of planning cleanup",
    )
    args = parser.parse_args()

    SUNO_CSV = args.csv
    DISCO_DIR = Path(args.disco).expanduser()
    EXTRAS_DIR = DISCO_DIR / "_EXTRAS"
    REPORT_DIR = Path(args.report_dir).expanduser()
    changeset_path = Path(args.changeset).expanduser() if args.changeset else REPORT_DIR / "cleanup-changeset.json"
    if args.rollback:
        rollback_changeset(changeset_path)
        print(f"↩️ Rolled back changeset: {changeset_path}")
        return
    if args.apply:
        applied = apply_changeset(changeset_path)
        stats = {
            "total_mp3s": len(applied["entries"]),
            "csv_matched": 0,
            "moved_to_extras": sum(
                entry.get("status") == "applied" for entry in applied["entries"]
            ),
            "missing_from_csv": 0,
            "matched_details": [],
            "moved_files": [entry["filename"] for entry in applied["entries"]],
            "planned_files": applied["entries"],
            "apply": True,
        }
        print_report(stats)
        save_report(stats)
        return
    print("=== nocturneMelodies — CSV-Enforced Cleanup ===\n")
    print("📖 suno-937.csv = AUTHORITY (exact row count = exact tracks allowed)")
    print("📂 DISCO/ = keep only CSV-matched MP3s\n")

    csv_tracks = load_csv()
    all_mp3s = scan_all_mp3s(DISCO_DIR)

    stats = enforce_csv(csv_tracks, all_mp3s)
    _write_changeset(changeset_path, stats["planned_files"])
    print(f"📝 Changeset written: {changeset_path}")
    print_report(stats)
    save_report(stats)


if __name__ == "__main__":
    main()

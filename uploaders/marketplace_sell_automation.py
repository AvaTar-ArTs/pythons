#!/usr/bin/env python3
"""
Generate sell-ready listing text (JSON + Markdown) from marketplace CSVs and
optionally create draft products on Gumroad.

  • "Info to sell": titles, descriptions, tags, suggested price — written to disk.
  • "Uploads": optional Gumroad API (draft products). No file binary upload via
    API in v1 — attach deliverables in Gumroad UI or zip locally first.

Usage:
  python marketplace_sell_automation.py --dry-run
  python marketplace_sell_automation.py --out ./listings_export --limit 20
  python marketplace_sell_automation.py --upload gumroad --limit 5

Env:
  GUMROAD_ACCESS_TOKEN  Required for --upload gumroad (https://gumroad.com/settings/advanced#application-form)

Requires: requests (only for Gumroad upload)
  pip install requests
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any
DEFAULT_CSV = Path(__file__).resolve().parent / "TOP_MARKETABLE_SCRIPTS.csv"


def slugify(name: str) -> str:
    base = Path(name).stem
    s = re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower()
    return s[:80] or "listing"


def parse_price_hint(value_range: str) -> tuple[int | None, str]:
    """Return (price_cents, note). Gumroad uses cents; we take midpoint of $a-$b."""
    if not value_range or value_range in ("$0-$0", "Unknown", ""):
        return None, "set_price_manually"
    m = re.findall(r"\$(\d+(?:,\d{3})*|\d+)", value_range.replace(",", ""))
    if len(m) >= 2:
        lo = int(m[0])
        hi = int(m[1])
        mid_dollars = max(5, min((lo + hi) // 2, 9999))  # cap $9999 for API sanity
        cents = mid_dollars * 100
        return cents, f"mid_of_range_{lo}_{hi}_usd"
    if len(m) == 1:
        d = int(m[0])
        return max(500, d * 100), "single_value_usd"
    return None, "unparsed"


def build_listing(row: dict[str, str], index: int) -> dict[str, Any]:
    fn = row.get("file_name") or Path(row.get("full_path", "")).name
    path = row.get("full_path", "")
    cat = row.get("category", "general")
    sub = row.get("subcategory", "")
    desc = (row.get("description") or "").strip() or "Python utility script."
    est = row.get("estimated_value_range", "")
    score = row.get("marketability_score", "")
    reasons = row.get("score_reasons", "")

    slug = slugify(fn)
    title = Path(fn).stem.replace("_", " ").replace("-", " ").strip()[:100]
    if not title:
        title = f"Script {index}"

    price_cents, price_note = parse_price_hint(est)
    if price_cents is None:
        price_cents = 2900  # $29 default placeholder
        price_note = "default_29_usd"

    tags = [cat, sub] if sub else [cat]
    tags = [t for t in tags if t][:10]

    short = desc[:280] + ("…" if len(desc) > 280 else "")

    long_md = f"""# {title}

**Category:** {cat} / {sub}
**Source file:** `{fn}`
**Inventory path:** `{path}`

## Summary
{desc}

## Details
- Estimated band (from inventory): {est or "n/a"}
- Marketability score: {score}
- Score signals: {reasons or "n/a"}

## What you get
- The described Python script (verify license and originality before sale).
- Add your own README, requirements.txt excerpt, and run instructions for buyers.

## Suggested tags
{", ".join(tags)}
"""

    return {
        "slug": slug,
        "index": index,
        "title": title,
        "short_description": short,
        "long_description_markdown": long_md,
        "tags": tags,
        "price_cents": price_cents,
        "price_note": price_note,
        "estimated_value_range_csv": est,
        "source_full_path": path,
        "gumroad_payload": {
            "name": title[:200],
            "description": long_md[:5000],
            "price": price_cents,
            "currency": "usd",
        },
    }


def write_listing_files(out_dir: Path, listing: dict[str, Any]) -> None:
    slug = listing["slug"]
    d = out_dir / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "listing.json").write_text(
        json.dumps(listing, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (d / "README_FOR_MARKETPLACE.md").write_text(
        listing["long_description_markdown"],
        encoding="utf-8",
    )


def write_manifest(out_dir: Path, listings: list[dict[str, Any]]) -> None:
    path = out_dir / "manifest.csv"
    fields = [
        "slug",
        "title",
        "price_cents",
        "price_note",
        "estimated_value_range_csv",
        "tags",
        "source_full_path",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for L in listings:
            row = {k: L.get(k, "") for k in fields}
            row["tags"] = ";".join(L.get("tags") or [])
            w.writerow(row)


def gumroad_create_product(
    access_token: str,
    payload: dict[str, Any],
    *,
    timeout: float = 60.0,
) -> dict[str, Any]:
    try:
        import requests
    except ImportError as e:
        raise SystemExit("Install requests: pip install requests") from e

    url = "https://api.gumroad.com/v2/products"
    data = {
        "access_token": access_token,
        "name": payload["name"],
        "description": payload["description"][:5000],
        "price": payload["price"],
        "currency": payload.get("currency", "usd"),
    }
    r = requests.post(url, data=data, timeout=timeout)
    try:
        body = r.json()
    except Exception:
        body = {"raw": r.text[:2000]}
    if r.status_code >= 400:
        raise RuntimeError(f"Gumroad API {r.status_code}: {body}")
    return body


def load_rows(csv_path: Path, limit: int | None) -> list[dict[str, str]]:
    rows = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for i, row in enumerate(r):
            if limit is not None and i >= limit:
                break
            rows.append(dict(row))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build listing files + optional Gumroad product drafts from TOP_MARKETABLE_SCRIPTS.csv"
    )
    ap.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help=f"Input CSV (default: {DEFAULT_CSV})",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent / "listings_export",
        help="Output directory for JSON/Markdown per listing",
    )
    ap.add_argument("--limit", type=int, default=None, help="Max rows to process")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print first listing summary only; no files written",
    )
    ap.add_argument(
        "--upload",
        choices=("none", "gumroad"),
        default="none",
        help="Create Gumroad draft products (requires GUMROAD_ACCESS_TOKEN)",
    )
    ap.add_argument(
        "--sleep",
        type=float,
        default=1.5,
        help="Seconds between Gumroad API calls",
    )
    args = ap.parse_args()

    if not args.csv.is_file():
        print(f"CSV not found: {args.csv}", file=sys.stderr)
        return 1

    rows = load_rows(args.csv, args.limit)
    if not rows:
        print("No rows in CSV.", file=sys.stderr)
        return 1

    listings = [build_listing(row, i + 1) for i, row in enumerate(rows)]

    if args.dry_run:
        L = listings[0]
        print(json.dumps(L, indent=2, ensure_ascii=False)[:4000])
        print(f"\n... {len(listings)} listing(s) would be written to {args.out}")
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    for L in listings:
        write_listing_files(args.out, L)
    write_manifest(args.out, listings)
    print(f"Wrote {len(listings)} listings under {args.out}")
    print(f"Manifest: {args.out / 'manifest.csv'}")

    if args.upload == "gumroad":
        token = os.environ.get("GUMROAD_ACCESS_TOKEN", "").strip()
        if not token:
            print(
                "Set GUMROAD_ACCESS_TOKEN in the environment to create products.",
                file=sys.stderr,
            )
            return 1
        results = []
        for L in listings:
            gp = L["gumroad_payload"]
            print(f"Creating Gumroad product: {gp['name'][:60]}...")
            try:
                resp = gumroad_create_product(token, gp)
                results.append({"slug": L["slug"], "ok": True, "response": resp})
            except Exception as e:
                results.append({"slug": L["slug"], "ok": False, "error": str(e)})
            time.sleep(args.sleep)
        (args.out / "gumroad_upload_results.json").write_text(
            json.dumps(results, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Gumroad results: {args.out / 'gumroad_upload_results.json'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

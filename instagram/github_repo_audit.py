"""
Github Repo Audit

This module provides functionality for github repo audit.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_200 = 200
CONSTANT_202 = 202
CONSTANT_204 = 204
CONSTANT_275 = 275
CONSTANT_300 = 300
CONSTANT_365 = 365
CONSTANT_403 = 403
CONSTANT_1000 = 1000
CONSTANT_10000 = 10000
CONSTANT_99999 = 99999

#!/usr/bin/env python3
"""
github_repo_audit.py
--------------------
Scan all GitHub repos for a user, score usefulness, and output CSV/JSON/HTML.
- Loads token from ~/.env.d/github.env (GITHUB_TOKEN=...)
- Uses /user/repos (if authorized) else falls back to /users/<username>/repos
- Scores each repo on Recency, Originality, Engagement, Substance
- Labels: KEEP (>=70), REVIEW (40–69), DELETE (<40)
- Optional: create ZIP archives for REVIEW category (--zip-review)
- Optional: delete DELETE repos via API (--delete --confirm 'I UNDERSTAND')

Usage examples:
  python3 github_repo_audit.py --username ichoake
  python3 github_repo_audit.py --username ichoake --zip-review --out-dir ~/GitHub/audit_out
  python3 github_repo_audit.py --username ichoake --delete --confirm "I UNDERSTAND"
"""

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
    from dotenv import load_dotenv
except Exception as e:
    logger.info("❌ Missing dependencies. Install with:")
    logger.info("   mamba install -c conda-forge python-dotenv requests")
    sys.exit(1)

DEFAULT_OUT_DIR = os.path.expanduser("~/GitHub/audit_out")
ENV_PATH = os.path.expanduser("~/.env.d/github.env")


def load_token():
    load_dotenv(ENV_PATH)
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logger.info("❌ Missing GITHUB_TOKEN in ~/.env.d/github")
        sys.exit(1)
    return token
def gh_get(url, headers, params=None, max_retries=5):
    for attempt in range(max_retries):
        r = requests.get(url, headers=headers, params=params, timeout=30)
        # Rate limit or abuse-detection handling
        if r.status_code == CONSTANT_403 and (
            "rate limit" in r.text.lower() or "abuse" in r.text.lower()
        ):
            wait_s = 10 * (attempt + 1)
            logger.info(f"⏳ Hit GitHub limits; backing off {wait_s}s...")
            time.sleep(wait_s)
            continue
        return r
    return r

def get_authenticated_login(headers):
    r = gh_get("https://api.github.com/user", headers)
    if r.status_code == CONSTANT_200:
        return r.json().get("login")
    return None


def paginate(url, headers, params=None):
    """Yield list pages following Link: rel=next"""
    while url:
        r = gh_get(url, headers, params=params)
        if r.status_code != CONSTANT_200:
            raise SystemExit(f"❌ GitHub API error {r.status_code}: {r.text[:CONSTANT_300]}")
        yield r.json()
        link = r.headers.get("Link", "")
        next_url = None
        if link:
            for part in link.split(","):
                seg = part.strip().split(";")
                if len(seg) == 2 and 'rel="next"' in seg[1]:
                    next_url = seg[0].strip()[1:-1]
        url = next_url
        params = None


def fetch_repos(username, token):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "ichoake-repo-audit",
    }
    login = get_authenticated_login(headers)
    if login and login.lower() == username.lower():
        base = "https://api.github.com/user/repos"
        params = {
            "per_page": CONSTANT_100,
            "type": "all",
            "sort": "full_name",
            "direction": "asc",
        }
        logger.info("🔐 Authenticated as target user → using /user/repos (includes private).")
    else:
        base = f"https://api.github.com/users/{username}/repos"
        params = {
            "per_page": CONSTANT_100,
            "type": "all",
            "sort": "full_name",
            "direction": "asc",
        }
        logger.info("🌐 Public export → using /users/<username>/repos.")

    repos = []
    for page in paginate(base, headers, params=params):
        if not isinstance(page, list):
            raise SystemExit("❌ Unexpected API response (expected list).")
        repos.extend(page)
    logger.info(f"✅ Retrieved {len(repos)} repositories.")
    return repos, headers


def days_since(ts_iso):
    if not ts_iso:
        return CONSTANT_99999
    try:
        dt = datetime.fromisoformat(ts_iso.replace("Z", "+00:00"))
    except Exception:
        return CONSTANT_99999
    now = datetime.now(timezone.utc)
    return (now - dt).days


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def score_repo(r):
    """Return (score, breakdown_dict) for a repo r"""
    # Signals
    dpush = days_since(r.get("pushed_at"))
    stars = r.get("stargazers_count") or 0
    watchers = r.get("watchers_count") or 0
    size = r.get("size") or 0  # KB
    is_fork = bool(r.get("fork"))
    archived = bool(r.get("archived"))
    disabled = bool(r.get("disabled"))

    # Early penalties
    if archived or disabled:
        return 0, {"recency": 0, "originality": 0, "engagement": 0, "substance": 0}

    # Recency (35): 0–90 days → up to 35, CONSTANT_365+ → near 0
    if dpush <= 0:
        recency = 35
    elif dpush <= 90:
        recency = 35 * (1 - dpush / 90)
    elif dpush <= CONSTANT_365:
        recency = 35 * (1 - (dpush - 90) / CONSTANT_275) * 0.5
    else:
        recency = 0
    recency = clamp(recency, 0, 35)

    # Originality (25): fork gets 0–8, original gets up to 25
    originality = 8 if is_fork else 25

    # Engagement (20): stars+watchers scaled (log-like)
    eng_raw = stars + watchers
    if eng_raw == 0:
        engagement = 0
    elif eng_raw < 5:
        engagement = 6
    elif eng_raw < 25:
        engagement = 12
    else:
        engagement = 20
    engagement = clamp(engagement, 0, 20)

    # Substance (20): size bands (KB) as proxy for “meaty-ness”
    if size < CONSTANT_100:
        substance = 2
    elif size < CONSTANT_1000:
        substance = 8
    elif size < CONSTANT_10000:
        substance = 14
    else:
        substance = 20
    substance = clamp(substance, 0, 20)

    score = round(recency + originality + engagement + substance, 2)
    return score, {
        "recency": round(recency, 2),
        "originality": originality,
        "engagement": engagement,
        "substance": substance,
    }


def label_from_score(score):
    if score >= 70:
        return "KEEP"
    if score >= 40:
        return "REVIEW"
    return "DELETE"


def ensure_dir(p):
    Path(p).expanduser().mkdir(parents=True, exist_ok=True)


def write_csv_json_html(repos, out_dir, html_template_path):
    csv_path = Path(out_dir) / "ichoake_repo_audit.csv"
    json_path = Path(out_dir) / "ichoake_repo_audit.json"
    html_path = Path(out_dir) / "index.html"

    # Prepare rows and stats
    rows = []
    stats = {"KEEP": 0, "REVIEW": 0, "DELETE": 0, "TOTAL": len(repos)}
    for r in repos:
        score, bd = score_repo(r)
        label = label_from_score(score)
        stats[label] += 1
        row = {
            "name": r.get("name", ""),
            "full_name": r.get("full_name", ""),
            "html_url": r.get("html_url", ""),
            "fork": r.get("fork", False),
            "language": r.get("language", ""),
            "created_at": r.get("created_at", ""),
            "updated_at": r.get("updated_at", ""),
            "pushed_at": r.get("pushed_at", ""),
            "size_kb": r.get("size", 0),
            "stargazers": r.get("stargazers_count", 0),
            "watchers": r.get("watchers_count", 0),
            "forks": r.get("forks_count", 0),
            "archived": r.get("archived", False),
            "disabled": r.get("disabled", False),
            "score": score,
            "label": label,
            "recency_score": bd["recency"],
            "originality_score": bd["originality"],
            "engagement_score": bd["engagement"],
            "substance_score": bd["substance"],
        }
        rows.append(row)

    # CSV
    cols = [
        "name",
        "full_name",
        "html_url",
        "fork",
        "language",
        "created_at",
        "updated_at",
        "pushed_at",
        "size_kb",
        "stargazers",
        "watchers",
        "forks",
        "archived",
        "disabled",
        "score",
        "label",
        "recency_score",
        "originality_score",
        "engagement_score",
        "substance_score",
    ]
    ensure_dir(out_dir)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for row in rows:
            w.writerow(row)

    # JSON
    audit = {
        "generated_at": datetime.now(timezone.utc).isoformat() + "Z",
        "stats": stats,
        "repos": rows,
    }
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(audit, jf, indent=2)

    # HTML
    try:
        with open(html_template_path, "r", encoding="utf-8") as tf:
            template = tf.read()
        # Simple injection: we’ll embed JSON and let the template render it client-side.
        html = template.replace("/*__AUDIT_JSON__*/", json.dumps(audit))
        with open(html_path, "w", encoding="utf-8") as hf:
            hf.write(html)
    except Exception as e:
        logger.info(f"⚠️ HTML template failed: {e}")

    logger.info(f"📄 CSV:   {csv_path}")
    logger.info(f"🧾 JSON:  {json_path}")
    logger.info(f"🖥️  HTML:  {html_path}")
    return csv_path, json_path, html_path, rows


def shallow_clone_and_zip(repo_html_url, out_zip_dir):
    """Shallow clone default branch and zip it. Requires git & zip available."""
    ensure_dir(out_zip_dir)
    name = repo_html_url.rstrip("/").split("/")[-1]
    tmp_dir = Path(out_zip_dir) / f".tmp_{name}"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    # Shallow clone
    rc = subprocess.call(
        ["git", "clone", "--depth", "1", repo_html_url, str(tmp_dir)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if rc != 0:
        return None
    zip_path = Path(out_zip_dir) / f"{name}.zip"
    rc = subprocess.call(["zip", "-rq", str(zip_path), "."], cwd=str(tmp_dir))
    shutil.rmtree(tmp_dir, ignore_errors=True)
    if rc != 0:
        return None
    return str(zip_path)


def delete_repo(full_name, headers):
    url = f"https://api.github.com/repos/{full_name}"
    r = requests.delete(url, headers=headers, timeout=30)
    return r.status_code in (CONSTANT_204, CONSTANT_202)


def main():
    ap = argparse.ArgumentParser(
        description="Audit GitHub repos and generate keep/review/delete recommendations."
    )
    ap.add_argument(
        "--username", required=True, help="GitHub username to audit (e.g., ichoake)"
    )
    ap.add_argument(
        "--out-dir", default=DEFAULT_OUT_DIR, help="Output directory for CSV/JSON/HTML"
    )
    ap.add_argument(
        "--zip-review", action="store_true", help="Zip REVIEW repos (local backup)"
    )
    ap.add_argument(
        "--delete",
        action="store_true",
        help="Delete repos labeled DELETE (requires token scope: delete_repo)",
    )
    ap.add_argument(
        "--confirm",
        default="",
        help="Required confirmation string for --delete. Must be: I UNDERSTAND",
    )
    args = ap.parse_args()

    token = load_token()
    repos, headers = fetch_repos(args.username, token)

    # Write CSV/JSON/HTML
    template_path = os.path.join(os.path.dirname(__file__), "audit_template.html")
    csv_path, json_path, html_path, rows = write_csv_json_html(
        repos, args.out_dir, template_path
    )

    # Optional zip REVIEW
    if args.zip_review:
        backup_dir = os.path.join(args.out_dir, "review_backups")
        logger.info("🗜️  Zipping REVIEW repos…")
        for row in rows:
            if row["label"] == "REVIEW":
                zp = shallow_clone_and_zip(row["html_url"], backup_dir)
                if zp:
                    logger.info(f"  • {row['name']} → {zp}")
                else:
                    logger.info(f"  • {row['name']} → zip failed (git/zip?)")

    # Optional deletion for DELETE
    if args.delete:
        if args.confirm != "I UNDERSTAND":
            logger.info('❌ Refusing to delete; pass --confirm "I UNDERSTAND" to proceed.')
            sys.exit(1)
        logger.info("🧨 Deleting repos labeled DELETE…")
        fail = 0
        ok = 0
        for row in rows:
            if row["label"] == "DELETE":
                ok_flag = delete_repo(row["full_name"], headers)
                if ok_flag:
                    ok += 1
                    logger.info(f"  ✓ Deleted {row['full_name']}")
                else:
                    fail += 1
                    logger.info(f"  ✗ Failed  {row['full_name']}")
        logger.info(f"Done. Deleted {ok}, failed {fail}.")

    logger.info("✅ Audit complete.")
    logger.info(f"Open the HTML dashboard:\n  file://{html_path}")


if __name__ == "__main__":
    main()

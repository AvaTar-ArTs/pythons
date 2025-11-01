"""
Upwork

This module provides functionality for upwork.

Author: Auto-generated
Date: 2025-11-01
"""

#!/usr/bin/env python3
import asyncio
import pandas as pd
import argparse
import os
import json
import re
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_800 = 800
CONSTANT_8000 = 8000


DEFAULT_FEEDS = [
    "https://www.upwork.com/nx/find-work/most-recent",
    "https://www.upwork.com/nx/find-work/domestic",
    "https://www.upwork.com/nx/find-work/best-matches?cf_lbyyhhwhyjj5l3rs65cb3w=974o4kqriphk7600xo23xf",
]

JOB_TILE_SELECTOR = 'section[data-test="job-tile"], div.up-card-section'
SCROLL_PAUSE = 1.0


def extract_job_id_from_url(url: str):
    """extract_job_id_from_url function."""

    if not url:
        return ""
    m = re.search(r"/jobs/~([0-9a-fA-F]+)", url)
    if m:
        return m.group(1)
    return ""


async def scrape_feed(page, feed_url, max_scrolls, max_pages=3):
    await page.goto(feed_url, wait_until="networkidle")
    if (
        "Log In" in await page.title()
        or "Sign In" in await page.content()[:CONSTANT_800]
    ):
        logger.info(
            f"[{feed_url}] If you're not logged in, please log in manually and then press Enter here."
        )
        input()

    collected = []
    seen_keys = set()

    for page_num in range(1, max_pages + 1):
        for _ in range(max_scrolls):
            await page.evaluate("window.scrollBy(0, window.innerHeight);")
            await asyncio.sleep(SCROLL_PAUSE)

        try:
            await page.wait_for_selector(JOB_TILE_SELECTOR, timeout=CONSTANT_8000)
        except Exception:
            logger.info(
                f"[{feed_url}] Warning: job tiles might not have appeared on page {page_num}."
            )

        cards = await page.query_selector_all(JOB_TILE_SELECTOR)
        logger.info(
            f"[{feed_url}] [page {page_num}] Found {len(cards)} potential job cards."
        )

        for card in cards:
            try:
                title_el = await card.query_selector("h4") or await card.query_selector(
                    'a[data-test="job-title-link"]'
                )
                title = (await title_el.inner_text()) if title_el else ""

                link_el = await card.query_selector("a")
                url = await link_el.get_attribute("href") if link_el else ""
                if url and url.startswith("/"):
                    url = "https://www.upwork.com" + url

                job_id = extract_job_id_from_url(url)
                uniq_key = (job_id or "") + "|" + (url or "") + "|" + title.strip()
                if uniq_key in seen_keys:
                    continue
                seen_keys.add(uniq_key)

                budget_el = await card.query_selector(
                    '[data-test="budget"]'
                ) or await card.query_selector(".up-budget")
                budget = (await budget_el.inner_text()) if budget_el else ""

                skill_tags = []
                skill_els = await card.query_selector_all(
                    '[data-test="skill"], .up-skill-tag'
                )
                for s in skill_els:
                    txt = await s.inner_text()
                    skill_tags.append(txt.strip())

                level = ""
                for lvl in ["Entry Level", "Intermediate", "Expert"]:
                    lvl_el = await card.query_selector(f'text="{lvl}"')
                    if lvl_el:
                        level = lvl
                        break

                location = ""
                loc_el = await card.query_selector(
                    '[data-test="client-location"]'
                ) or await card.query_selector(".up-client-info")
                if loc_el:
                    location = (await loc_el.inner_text()).strip()

                desc_el = await card.query_selector(
                    '[data-test="job-description"]'
                ) or await card.query_selector(".up-line-clamp")
                description = (await desc_el.inner_text()).strip() if desc_el else ""

                result = {
                    "Title": title.strip(),
                    "URL": url or "",
                    "Job ID": job_id or "",
                    "Budget": budget.strip(),
                    "Primary Skill": skill_tags[0] if skill_tags else "",
                    "All Skills": ", ".join(skill_tags),
                    "Skill Level": level,
                    "Location": location,
                    "Description": description.replace(Path("\n"), " ")[:CONSTANT_800],
                    "Date Scraped": datetime.utcnow().isoformat(),
                    "Feed Source": feed_url,
                    "Page": page_num,
                }
                if result["Title"] or result["Job ID"]:
                    collected.append(result)
            except Exception as e:
                logger.info(f"[{feed_url}] Error parsing card on page {page_num}: {e}")

        next_clicked = False
        selectors_to_try = [
            'button:has-text("Next")',
            'a:has-text("Next")',
            'button:has-text("Load more")',
            'button[aria-label="Next"]',
            'div[role="button"]:has-text("More")',
        ]
        for sel in selectors_to_try:
            try:
                nxt = await page.query_selector(sel)
                if nxt:
                    await nxt.click()
                    await asyncio.sleep(1.5)
                    next_clicked = True
                    logger.info(
                        f"[{feed_url}] Clicked pagination control '{sel}' on page {page_num}."
                    )
                    break
            except Exception:
                continue

        if not next_clicked:
            logger.info(
                f"[{feed_url}] No further pagination control found after page {page_num}; stopping pagination loop."
            )
            break

    return collected


async def main(args):
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cookie_path = Path(args.cookies_file)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        if cookie_path.exists():
            try:
                cookies = json.loads(cookie_path.read_text())
                await context.add_cookies(cookies)
                logger.info(f"Loaded {len(cookies)} cookies from {cookie_path}")
            except Exception as e:
                logger.info("Failed to load cookies:", e)

        page = await context.new_page()
        all_jobs = []
        for feed in args.feeds:
            jobs = await scrape_feed(page, feed, args.max_scrolls, args.max_pages)
            all_jobs.extend(jobs)
        try:
            saved = await context.cookies()
            cookie_path.write_text(json.dumps(saved, indent=2))
            logger.info(f"Saved {len(saved)} cookies to {cookie_path}")
        except Exception as e:
            logger.info("Failed to save cookies:", e)

        await browser.close()

    if not all_jobs:
        logger.info("No jobs collected from any feed.")
        return

    df = pd.DataFrame(all_jobs)
    df["uniq_key"] = df["Job ID"].fillna("") + "|" + df["URL"].fillna("")
    df = df.drop_duplicates(subset=["uniq_key"]).drop(columns=["uniq_key"])

    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"dataset_upwork-job-scraper_multi-feed_{timestamp}.csv"
    out_path = out_dir / filename
    df.to_csv(out_path, index=False)
    logger.info(f"Saved combined multi-feed scrape ({len(df)} jobs) to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Multi-feed Upwork job scraper with pagination"
    )
    parser.add_argument(
        "--output-dir",
        default=Path("/Users/steven/upwork"),
        help="Output directory for CSVs",
    )
    parser.add_argument(
        "--feeds", nargs="+", default=DEFAULT_FEEDS, help="List of Upwork feed URLs"
    )
    parser.add_argument(
        "--max-scrolls", type=int, default=6, help="Number of scrolls per page"
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=3,
        help="Maximum pagination pages to click through per feed",
    )
    parser.add_argument(
        "--cookies-file",
        default=".upwork_cookies.json",
        help="File to persist login cookies",
    )
    args = parser.parse_args()
    asyncio.run(main(args))

"""
Build

This module provides functionality for build.

Author: Auto-generated
Date: 2025-11-01
"""

#!/usr/bin/env python3
import os, sys, csv
from pathlib import Path

CATEGORIES = [
  ("Audio & Transcription", ["transcribe","lyrics","audio","spotifymp3","savify"]),
  ("YouTube/Twitch Automation", ["youtube","yt-","twitch","shorts","clip"]),
  ("Social Media Bots & Scrapers", ["reddit","instagram","tiktok","fb-","twitter","scraper"]),
  ("AI Art & POD Pipelines", ["redbubble","pod","photoshop","mockup","leonardo","dalle","ai-comic","remove-bg","upscale"]),
  ("File Utilities & Organizers", ["organize","sort","clean","convertor","tablecontentspython","download-all-the-gifs","simplegallery"]),
  ("LLM / Generative AI", ["llm","openai","ygpt","sora","gpt"]),
  ("Interactive / Games", ["quiz","game"]),
  ("Analytics & Dashboards", ["analytics","dashboard"]),
  ("Tools & Misc", ["spicetify","fdupes","html","colab"]),
]

def categorize(name: str) -> str:
    n=name.lower()
    for label,keys in CATEGORIES:
        if any(k in n for k in keys):
            return label
    return "Uncategorized"
def one_liner(cat:str)->str:
    return {
        "Audio & Transcription":"Batch audio tools and Whisper-powered transcription for creators.",
        "YouTube/Twitch Automation":"Hands-free channel ops: uploaders, viewers, shorts-maker, playlist tools.",
        "Social Media Bots & Scrapers":"Data collection and automation for growth workflows.",
        "AI Art & POD Pipelines":"Generate, upscale, remove BG, and prep mockups for POD storefronts.",
        "File Utilities & Organizers":"Bulk organize, sort, clean, and convert media libraries.",
        "LLM / Generative AI":"Prompt engines, OpenAI integrations, and storyboard/video generators.",
        "Interactive / Games":"Playable scripts for engagement and learning.",
        "Analytics & Dashboards":"Dashboards and reporting for content performance.",
        "Tools & Misc":"Handy utilities and wrappers for daily use.",
        "Uncategorized":"Prototype or mixed-utility scripts.",
    }.get(cat,"Python automation for creative workflows.")

def tags_for(cat:str)->str:
    return {
        "AI Art & POD Pipelines":"AI art, POD, DALL·E, Leonardo, upscaling, Photoshop",
        "YouTube/Twitch Automation":"YouTube API, Twitch, automation, FFmpeg, shorts",
        "Audio & Transcription":"Whisper, audio, transcription, TTS, mp3, m4a",
        "File Utilities & Organizers":"batch, file rename, metadata, sorting, PIL, OpenCV",
        "Social Media Bots & Scrapers":"Instagram, Reddit, TikTok, scraper, growth",
        "LLM / Generative AI":"OpenAI, GPT, LLM, storyboard, video",
        "Analytics & Dashboards":"analytics, SEO, YouTube Studio, pandas, dash",
        "Interactive / Games":"game, CLI, education",
        "Tools & Misc":"python, automation",
        "Uncategorized":"python, automation",
    }.get(cat,"python, automation")
def gh_url(folder:str)->str:
    return f"https://github.com/ichoake/python/tree/main/{folder.replace(' ', '%20')}"

def main(repo_root=".", out_csv="portfolio/portfolio_descriptions.csv", out_py_md="content/python_portfolio.md", out_al_md="content/alchemy_index.md"):
    root = Path(repo_root)
    skip = {".git",".github","scripts","content","portfolio","__pycache__"}
    folders = [p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith('.') and p.name not in skip]
    rows = []
    for name in folders:
        cat = categorize(name)
        rows.append({
            "name": name,
            "category": cat,
            "seo_title": f"{name} — {cat}",
            "summary": one_liner(cat),
            "suggested_tags": tags_for(cat)
        })
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv,"w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f, fieldnames=["name","category","seo_title","summary","suggested_tags"])
        writer.writeheader(); writer.writerows(rows)

    def md_section(r):
        return """### {name}
**Category:** {category}  
**What it does:** {summary}  
**Tags:** {tags}

**Repo:** {repo}
""".format(name=r['name'], category=r['category'], summary=r['summary'], tags=r['suggested_tags'], repo=gh_url(r['name']))

    rows_sorted = sorted(rows, key=lambda r: (r["category"], r["name"].lower()))
    Path(out_py_md).parent.mkdir(parents=True, exist_ok=True)
    Path(out_py_md).write_text("# AvatarArts · Python Portfolio\n\n" + Path("\n").join(md_section(r) for r in rows_sorted), encoding="utf-8")

    al_lines = ["- **{name}** — *{category}*: {summary} · *Tags:* {tags}".format(
        name=r['name'], category=r['category'], summary=r['summary'], tags=r['suggested_tags']) for r in rows_sorted]
    Path(out_al_md).write_text("# Alchemy · Creative Automation Index\n\n> Tools and rituals behind the art.\n\n" + Path("\n").join(al_lines), encoding="utf-8")

if __name__ == "__main__":
    repo_root = sys.argv[1] if len(sys.argv)>1 else "."
    main(repo_root)

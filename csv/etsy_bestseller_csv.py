#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import argparse, os, math, json, re, csv, statistics
from collections import Counter, defaultdict
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100


try:
    import pandas as pd
    import numpy as np
except Exception as e:
    raise SystemExit("Please `pip install pandas numpy` first.")

IP_TERMS = [
    # Common IP/brand words to flag (extend as needed)
    "harry potter","hogwarts","disney","pixar","star wars","marvel","dc",
    "pokemon","nintendo","zelda","taylor swift","swiftie","barbie","hello kitty",
    "ravenclaw","hufflepuff","slytherin","gryffindor","mickey","minnie","yoda",
]
# Map frequent typos to generic, *non-IP* terms
TYPO_MAP = {
    "ravenclawe":"raven", "gryfindor":"wizard", "pokeman":"pocket monster", "disny":"magic",
}

GENERIC_THEMES = [
    "wizard school","magic academy","enchanted forest","castlecore","chateaucore","cottagecore",
    "national parks","retro travel","space adventure","galactic","neon","primary play",
    "cherry coded","dill green","aura indigo","butter yellow",
]

TITLE_SHELLS = [
    "{NOUN} {AESTHETIC} for {AUDIENCE} | {COLOR} {USP}",
    "{AESTHETIC} {NOUN} — {OCCASION} | {COLOR} {USP}",
]

def std_col(df, names):
    for n in names:
        for c in df.columns:
            if c.strip().lower() == n:
                return c
    return None

def parse_args():
    ap = argparse.ArgumentParser(description="Analyze Etsy bestseller CSV and output recommendations.")
    ap.add_argument("--input", required=True, help="Path to CSV")
    ap.add_argument("--outdir", default="./outputs", help="Directory for outputs")
    ap.add_argument("--sep", default=None, help="CSV delimiter (auto if omitted)")
    return ap.parse_args()

def normalize_df(df):
    # Standardize column names
    cols = {c:c for c in df.columns}
    def col(*alts): return std_col(df, [a.lower() for a in alts])
    title = col("title","product_name","name"); 
    price = col("price")
    views = col("views","view")
    favs  = col("favorites","favourites","fav")
    reviews = col("reviews","review_count")
    mo_rev = col("est_mo_revenue","estimated_monthly_revenue")
    tot_sales = col("est_total_sales","total_sales")
    conv = col("conversion_rate","conversion")
    url  = col("url","link")
    tags = col("tags","tag_list")
    # Create a normalized frame
    out = pd.DataFrame()
    out["title"] = df[title] if title else ""
    out["price"] = pd.to_numeric(df[price], errors="coerce") if price else np.nan
    out["views"] = pd.to_numeric(df[views], errors="coerce") if views else np.nan
    out["favorites"] = pd.to_numeric(df[favs], errors="coerce") if favs else np.nan
    out["reviews"] = pd.to_numeric(df[reviews], errors="coerce") if reviews else np.nan
    out["est_mo_revenue"] = pd.to_numeric(df[mo_rev], errors="coerce") if mo_rev else np.nan
    out["est_total_sales"] = pd.to_numeric(df[tot_sales], errors="coerce") if tot_sales else np.nan
    out["conversion_rate"] = pd.to_numeric(df[conv], errors="coerce") if conv else np.nan
    out["url"] = df[url] if url else ""
    out["raw_tags"] = df[tags] if tags else ""
    return out

def tokenize_tags(s):
    if pd.isna(s): return []
    s = str(s)
    if "|" in s: parts = [p.strip() for p in s.split("|")]
    else: parts = [p.strip() for p in s.split(",")]
    return [p for p in parts if p]

def tag_cleanup(tags):
    cleaned = []
    warnings = []
    for t in tags:
        t0 = t
        t = t.lower().strip()
        if not t: continue
        t = TYPO_MAP.get(t, t)
        # IP flag -> soften to generic
        for ip in IP_TERMS:
            if ip in t:
                warnings.append(f"IP risk: '{t0}' contains '{ip}'")
                # replace with generic if possible
                t = re.sub(ip, "magic academy", t)
        t = re.sub(r"\s+", " ", t)
        if t not in cleaned:
            cleaned.append(t)
    return cleaned[:20], warnings

def top_tag_stats(df):
    all_tags = []
    for row in df["raw_tags"].fillna(""):
        all_tags.extend(tokenize_tags(row))
    ctr = Counter([t.lower().strip() for t in all_tags if t])
    return ctr.most_common(CONSTANT_100)

def derive_conversion(df):
    cr = df["conversion_rate"].copy()
    # If missing or mostly NaN, attempt compute: sales / views
    if cr.isna().mean() > 0.5:
        if ("est_total_sales" in df) and ("views" in df):
            with np.errstate(divide='ignore', invalid='ignore'):
                alt = df["est_total_sales"] / df["views"]
                alt = alt.replace([np.inf, -np.inf], np.nan)
                cr = alt.fillna(cr)
    # coerce to [0,1]
    cr = cr.apply(lambda x: x/CONSTANT_100.0 if (pd.notna(x) and x>1.5) else x)
    return cr.clip(lower=0, upper=1)

def make_title_variants(base_title, tags):
    # Extract primary noun + aesthetic + audience + color + USP from tags
    noun = next((t for t in tags if any(k in t for k in ["shirt","sweatshirt","mug","poster","print","svg","stl","tumbler","template","invite","label","sticker","wallpaper"])), "poster")
    aesthetic = next((t for t in tags if any(k in t for k in ["castlecore","chateaucore","coquette","primary play","cherry","aura indigo","butter yellow","dill green","galactic","neon"])), "modern")
    audience = next((t for t in tags if any(k in t for k in ["teacher","parents","kids","men","women","gifts","family","couple"])), "gifts")
    color = next((t for t in tags if any(k in t for k in ["butter yellow","alpine oat","aura indigo","cherry red","primary colors","bold red"])), "neutral")
    usp = next((t for t in tags if any(k in t for k in ["printable","svg","stl","digital download","seamless","vector","instant download"])), "instant download")
    shells = TITLE_SHELLS[:]
    outs = []
    for sh in shells:
        t = sh.format(NOUN=noun.title(), AESTHETIC=aesthetic.title(), AUDIENCE=audience.title(), COLOR=color.title(), USP=usp.title())
        outs.append((t[:60]).strip())
    return outs

def main():
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    # Read CSV (let pandas auto-detect sep if not specified)
    df = pd.read_csv(args.input, sep=args.sep)
    df0 = normalize_df(df)
    df0["conversion_est"] = derive_conversion(df0)
    # Tag processing
    cleaned_tags = []
    tag_warnings = []
    for tags in df0["raw_tags"].fillna("").tolist():
        c, w = tag_cleanup(tokenize_tags(tags))
        cleaned_tags.append(", ".join(c))
        tag_warnings.append("; ".join(w))
    df0["tags_cleaned"] = cleaned_tags
    df0["tag_warnings"] = tag_warnings
    # Scores
    # revenue score (normalize 0..1)
    rev = df0["est_mo_revenue"].fillna(0).astype(float)
    rev_score = (rev - rev.min()) / (rev.max() - rev.min() + 1e-9)
    conv = df0["conversion_est"].fillna(0.0)
    # price position by IQR
    price = df0["price"].fillna(np.nan)
    q1, q3 = np.nanpercentile(price, 25), np.nanpercentile(price, 75)
    iqr = q3 - q1 if not math.isnan(q3) and not math.isnan(q1) else 0
    def price_flag(p, cr):
        if math.isnan(p): return ""
        if iqr <= 0: return ""
        if p > q3 and cr < np.nanmedian(conv):
            return "Consider -5% to -10% price test (high price, low conv)."
        if p < q1 and rev_score.mean() > 0.5:
            return "Test +5% anchor bundle (low price; try higher)."
        return ""
    # Build recommendations
    rec_rows = []
    rewrite_rows = []
    price_rows = []
    thumb_prompts = []
    for idx, row in df0.iterrows():
        title = (row["title"] or "").strip()
        tags = [t.strip() for t in (row["tags_cleaned"] or "").split(",") if t.strip()]
        v1, v2 = make_title_variants(title, tags)
        # recommendations
        rec = {
            "title": title,
            "url": row["url"],
            "price": row["price"],
            "est_mo_revenue": row["est_mo_revenue"],
            "est_total_sales": row["est_total_sales"],
            "views": row["views"],
            "conversion_est": round(float(row["conversion_est"] or 0), 4),
            "favorites": row["favorites"],
            "reviews": row["reviews"],
            "ip_warnings": row["tag_warnings"],
            "actions": "; ".join([
                "Fix tags typos/IP to generic" if row["tag_warnings"] else "",
                "A/B title using variants below",
                price_flag(row["price"], row["conversion_est"]),
            ]).strip("; ").strip()
        }
        rec_rows.append(rec)
        # rewrite variants
        rewrite_rows.append({
            "original_title": title,
            "variant_a": v1,
            "variant_b": v2,
            "tags_suggested": row["tags_cleaned"]
        })
        # price guidance
        pf = price_flag(row["price"], row["conversion_est"])
        price_rows.append({
            "title": title, "price": row["price"], "guidance": pf
        })
        # thumbnail prompt
        if v1:
            thumb_prompts.append(f"- Mockup: {v1} — flat-lay on textured paper, soft daylight, shadow play.")
    # Save outputs
    import pandas as pd
    pd.DataFrame(rec_rows).to_csv(os.path.join(args.outdir, "recommendations.csv"), index=False)
    pd.DataFrame(rewrite_rows).to_csv(os.path.join(args.outdir, "title_rewrites.csv"), index=False)
    pd.DataFrame(price_rows).to_csv(os.path.join(args.outdir, "price_guidance.csv"), index=False)
    open(os.path.join(args.outdir, "tags_cleaned.csv"), "w", encoding="utf-8", newline="").write(Path("\n").join(df0["tags_cleaned"].fillna("").tolist()))
    open(os.path.join(args.outdir, "thumbnail_prompts.txt"), "w", encoding="utf-8").write(Path("\n").join(thumb_prompts))
    # Pack folder for Gumroad (example)
    packdir = os.path.join(args.outdir, "pack")
    os.makedirs(packdir, exist_ok=True)
    open(os.path.join(packdir, "README.md"), "w", encoding="utf-8").write("# Cleaned SEO Pack\n\nIncludes: recommendations.csv, title_rewrites.csv, tags_cleaned.csv, price_guidance.csv.\n")
    open(os.path.join(packdir, "LICENSE.txt"), "w", encoding="utf-8").write("Single-store license. No redistribution of datasets.\n")
    # copy files
    for fn in ["recommendations.csv", "title_rewrites.csv", "price_guidance.csv", "tags_cleaned.csv"]:
        import shutil
        shutil.copy(os.path.join(args.outdir, fn), os.path.join(packdir, fn))
    logger.info("Done. Outputs in", args.outdir)

if __name__ == "__main__":
    main()

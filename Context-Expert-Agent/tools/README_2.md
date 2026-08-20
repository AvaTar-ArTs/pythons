# Page Maker v3

A small static generator with clean defaults and sensible features.

## Install
```bash
pip install jinja2 markdown pyyaml
```

## Build
```bash
python page_maker.py \
  --input ./content \
  --output ./output \
  --site-title "Quantum Forge Labs" \
  --site-description "AI, automation, and creative intelligence from the edge of innovation." \
  --site-url "https://QuantumForgelabs.org" \
  --author "Quantum Forge Labs Team" \
  --format both
```

## Import Deepseek export
```bash
python deepseek_to_pages.py \
  --user "/path/to/user.json" \
  --conversations "/path/to/conversations.json" \
  --out "./content"
```

Features: sticky TOC, tag pages, archives, search, RSS, sitemap with lastmod, robots.txt, 404.html, copy buttons on code, RFC-compliant dates, canonical only when site_url is set.

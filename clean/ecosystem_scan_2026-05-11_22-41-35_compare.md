# Ecosystem scan vs metadata (2026-05-11_22-41-35)

## Method
- **Document-class files**: same extensions as `~/clean/docs.py` dry-run, with ecosystem exclusions (see script header).
- **`du -sk`**: total disk use per directory (includes skipped trees like `.git`).
- **Master index**: keys from `filesystem_master_index_20260208_064111.txt` where a `📁 ... (/Users/steven/...)` block exists. Index **file counts are total files**, not document-class only — use for spot-check, not equality.

## 2T-Xx report (excerpt)
```

```

## Per-target

| Path | du | doc files | doc MiB | master index files | master size |
|------|-----|-----------|---------|-------------------|-------------|
| `Applications` | 552K | 0 | 0 |  |  |
| `AutoTagger` | 727.8M | 772 | 77.4 |  |  |
| `claudemarketplaces.com` | 3.1M | 25 | 1.2 |  |  |
| `clean` | 31.3M | 502 | 29.2 |  |  |
| `Development` | 206.2M | 282 | 6.5 |  |  |
| `Documents` | 2.9G | 7310 | 2548.0 |  |  |
| `Downloads` | 22.1G | 31257 | 1071.9 |  |  |
| `Fixes` | 40K | 4 | 0.0 |  |  |
| `github` | 2.5G | 6349 | 245.0 |  |  |
| `grok` | 18.8M | 58 | 16.3 |  |  |
| `iterm2` | 3.5G | 9455 | 1076.4 |  |  |
| `Miniforge_Mamba_Analysis` | 44K | 3 | 0.0 |  |  |
| `my-simple` | 56K | 8 | 0.0 |  |  |
| `Pictures` | 19.7G | 7466 | 1088.6 |  |  |
| `PYTHON_MARKETPLACE_MASTER` | 3.4G | 16920 | 1077.7 |  |  |
| `pythons` | 1.2G | 10173 | 364.6 |  |  |
| `reports` | 0K | 0 | 0 |  |  |
| `scripts` | 47.8M | 1177 | 24.3 |  |  |
| `userscripts` | 42.2M | 42 | 9.0 |  |  |
| `zombot-simple-gallery` | 140K | 14 | 0.1 |  |  |
| `Zotero` | 18.1M | 738 | 10.8 |  |  |

Full CSV: `/Users/steven/clean/ecosystem_scan_2026-05-11_22-41-35.csv`
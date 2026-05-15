# CSV schema diff

**Why it’s unique:** Merge tools are common; **“did my nightly export change shape?”** is a different job—column drift, dtype drift, row counts, optional key overlap.

## Usage

```bash
pip install -r requirements.txt
python3 csv_schema_diff.py yesterday.csv today.csv
python3 csv_schema_diff.py a.csv b.csv --key order_id -o report.md
```

**Listing angle:** “Stop silent CSV breakage—diff schemas before pipelines fail.”

# CSV Safe Merge (CLI)

**Gap filled:** High search volume for “merge CSV files python / dedupe” with few **boxed** CLIs—most results are notebook cells.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Concatenate two exports
python3 csv_safe_merge.py shop_a.csv shop_b.csv -o merged.csv

# Merge and dedupe on an ID column
python3 csv_safe_merge.py a.csv b.csv c.csv -o out.csv --dedupe-column customer_id
```

## Notes

- Column names must align for meaningful merges (pandas concat).
- For production, add schema validation—this is a focused utility SKU.

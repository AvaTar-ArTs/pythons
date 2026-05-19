# Import vs requirements audit

**Why it’s unique:** Code marketplaces fail when **`pip install -r requirements.txt` misses a dep**. This walks `*.py`, collects top-level imports, and flags **likely** gaps (stdlib excluded; common import→PyPI aliases included).

## Usage

```bash
python3 audit_imports.py /path/to/your/product/folder
python3 audit_imports.py . -r ./requirements.txt
```

**Listing angle:** “Ship Python zips that actually install—audit imports vs requirements before buyers one-star you.”

**Limit:** Heuristic; always confirm in a **clean venv**.

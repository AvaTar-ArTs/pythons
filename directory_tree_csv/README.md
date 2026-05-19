# Directory tree → CSV

**Gap filled:** “Export folder structure csv” / “directory listing spreadsheet” — lots of search volume; answers are often **PowerShell one-liners** or heavy tools, not a **small Python SKU**.

## Usage

```bash
python3 tree_to_csv.py /path/to/project -o audit.csv
```

Limit depth:

```bash
python3 tree_to_csv.py /path/to/project -o shallow.csv --max-depth 3
```

## Columns

`path`, `depth`, `name`, `is_file`, `size_bytes`

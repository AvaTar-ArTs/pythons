# Paste.app History Export Review

Date: 2026-08-09
Reviewed source database:

`/Users/steven/Library/Application Support/com.wiheads.paste-setapp/db.sqlite`

Reviewed scripts:

- `/Users/steven/pythons/export_paste_history.py`
- `/Users/steven/pythons/improve_paste_export.py`
- `/Users/steven/pythons/tools/legacy_scripts/create_search_interface.py`
- `/Users/steven/pythons/tools/legacy/legacy_scripts/create_search_interface.py`

Privacy note: no clipboard text/content is included in this report.

## What is actually present

The Paste app database is healthy according to SQLite `PRAGMA quick_check`.

Observed database facts:

- Main database: approximately 569 MB.
- Search index database: approximately 709 MB.
- Clipboard item rows: 13,234 in `ZITEMENTITY`.
- Item-data rows: 21,524 in `ZITEMDATAENTITY`.
- All clipboard items have a data link.
- The app uses SQLite WAL files, so this is an active application database.

Relevant data model:

- `ZITEMENTITY`: item metadata, timestamp, title, raw preview blob.
- `ZITEMDATAENTITY`: item payload blobs (`ZRAWPASTEBOARDITEMS`).
- `ZAPPLICATIONENTITY`: source application metadata.
- `ZLISTENTITY`: Paste lists/collections.

## Current script verdicts

### `export_paste_history.py`

Status: metadata-only exporter; not a full clipboard-content exporter.

What it does:

- Reads `ZITEMENTITY`.
- Groups item metadata by date.
- Exports title, time, raw type, and preview size.
- Writes to `~/Documents/paste-clipboard-export`.

Problems:

1. It does not export actual clipboard text.
2. It runs immediately on import because the call is not under `if __name__ == "__main__":`.
3. The exception handler uses `sys.exit()` but the script does not import `sys`.
4. It opens the active database directly and makes no explicit read-only snapshot.
5. It can create many files and an index without a dry-run or destination confirmation.

Syntax: compiles successfully.

### `improve_paste_export.py`

Status: intended full exporter, but its extraction strategy is currently pointed at the wrong field/format.

What it intends to do:

- Joins `ZITEMENTITY` to `ZITEMDATAENTITY`.
- Reads `ZRAWPASTEBOARDITEMS`.
- Attempts to decode it as a plist and find text in common pasteboard keys.
- Writes daily markdown exports to `~/Documents/paste-clipboard-FULL-export`.

Validated issue:

- A non-content sample of 250 `ZRAWPASTEBOARDITEMS` blobs yielded zero text values through the current `plistlib` extractor.
- The sampled blob prefixes do not resemble ordinary `bplist` data.
- Therefore the current extractor should not be trusted to export actual text.

Additional bug:

- At index generation, line 241 uses the last `filename` value from the earlier loop instead of rebuilding `clipboard_<date>.md` for each date. The index would link every date to the same final file.

Other concerns:

- No safe dry-run.
- No redact/exclude policy for secrets, passwords, tokens, recovery codes, or private conversation data.
- No provenance record tying exported rows to source IDs without exposing body text.
- Directly opens an active WAL database.

Syntax: compiles successfully.

### Search interface scripts

`/Users/steven/pythons/tools/legacy_scripts/create_search_interface.py`

- Syntax-valid version.
- Generates a browser file index across Cursor and Paste Markdown exports.
- Its “search” filters filenames only. It does not search clipboard or chat body text.
- It emits JavaScript from Python string representations instead of JSON, which is brittle.
- It assumes export folders exist but they do not currently exist.

`/Users/steven/pythons/tools/legacy/legacy_scripts/create_search_interface.py`

- Broken: `py_compile` fails with a syntax error at line 46 due to malformed string quoting.
- It should be treated as obsolete duplicate history, not a current runnable path.

## Key discovery: the viable text source is likely `ZRAWPREVIEW`

A sampled metadata-only check of `ZRAWPREVIEW` found:

- 496 of 500 sampled preview blobs parsed as JSON.
- The common JSON keys were `type`, `textLength`, and `text`.
- This means `ZRAWPREVIEW` is likely the reliable first-pass source for text previews.

This is materially different from the current full-export script, which tries to parse the opaque `ZRAWPASTEBOARDITEMS` blobs as plists.

## Recommended design: safe two-stage exporter

Do not run either existing exporter against the full live history yet.

Build a replacement with these properties:

### Stage 1 — audit / dry run

- Read the database in read-only mode.
- Use `ZRAWPREVIEW` JSON for a count-only inventory.
- Report item counts, source app counts, date range, text/non-text counts, and estimated output size.
- Do not emit clipboard body text.
- Do not write anything without explicit destination approval.

### Stage 2 — approved export

- Export only after Steven chooses a destination and retention rule.
- Preserve source ID, timestamps, item type, source app, and content hash.
- Extract the JSON `text` preview first.
- Keep opaque raw blobs only as optional, non-default forensic attachments.
- Create a manifest and a redaction report.
- Exclude obvious secrets and credentials by default, with a review queue rather than automatic disclosure.
- Keep the output local and explicitly mark it private.

Recommended output formats:

- `manifest.jsonl`: one metadata/provenance record per item.
- date- or source-app-scoped Markdown only for approved readable records.
- `redaction_review.jsonl`: excluded/suspected-secret items with hashes and reason, not plaintext.
- one SQLite/FTS index for local search rather than hundreds of Markdown files.

## Why this matters for Claude / knowledge-system work

Paste history is a valuable local evidence source, but it is not clean product inventory and should never be included in marketplace bundles or public portfolio material.

Potential private use:

- Recover project context.
- Find past commands, URLs, research notes, and snippets.
- Build a private, searchable local timeline.

Do not treat it as:

- public content,
- redistributable prompts,
- client evidence,
- an automatic source for agent memory,
- a data source to send to third-party models without explicit filtering and approval.

## Recommendation

Retire the malformed legacy search script. Do not run either current exporter on the full database. Replace them with one read-only, JSON-preview-first, dry-run-first exporter and a local SQLite/FTS search index.

Implementation should begin only after Steven decides:

1. whether the output may contain full text or metadata/preview text only;
2. the approved local destination;
3. whether to redact secrets automatically;
4. whether the result is for private local search only or selective Claude-ready research.

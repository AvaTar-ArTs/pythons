# Enriched scanner v2

This is a separate normalized report entry point. It leaves doc-source-enriched.py and existing inventories untouched. It reuses the sibling scanner's enrichment functions; distribute it with that file, scanner_utils.py and exclude_patterns.py, not as a standalone copied script.

## Usage

```sh
python3 scan-to-csv/doc-source-enriched-v2.py /path/to/input -o /path/outside/input/new-report
```

Output is a **new directory**, not a CSV filename. Existing destinations and outputs inside scan roots are rejected. No cleanup runs. Do not point at the entire home directory casually: the inherited scanner reads content.

The report contains:

- inventory.csv: one row per scanned file; enrichment fields plus schema_version, root_id, relative_path, content_hash and duplicate_group_id. No repeated duplicate_paths field.
- duplicate-members.csv: one row per duplicate-group member; full SHA-256 group ID, root ID and relative path. Membership is stored once rather than every member listing every other member.
- summary.json: counts, root IDs, encoding and limitations.

A root ID plus relative path is the path identity. Root IDs are deterministic for the same normalized root set, not permanent identities across different root selections. Default report root records omit absolute paths; --absolute-paths adds private root mappings and per-file absolute paths. Relative filenames and enrichment can still reveal sensitive information: this is not a full secret-redaction system. Formula-leading CSV strings are prefixed with an apostrophe; consumers must account for this documented encoding.

## Why size is controlled

The old duplicate annotation stores an entire group's path list on every member: quadratic serialized output in large groups. V2 never calls that annotation function. It counts hashes and emits membership rows once. It preserves every file row without selecting a copy to delete. Group IDs use the full digest.

## Publication

Files are written and fsynced in a unique sibling staging directory. Only after all files succeed is the directory renamed to the requested report path. Ordinary failures remove staging output; forced termination may leave a clearly named .enriched-v2-* staging directory, not a completed report. This is not a hostile-concurrent-writer or power-loss durability guarantee. Use a private output parent and unique destination; do not concurrently publish to the same name.

## Explicit limitations

This fixes the duplicate serialization and path presentation defects; it is not a complete new traversal engine. The inherited scanner still uses full hashing, stores rows in memory, performs heuristic classification and applies existing exclusions and sensitive-name policy. It is not metadata-only, does not bound all I/O, and does not make a live tree race-free. Missing/excluded content is not a complete filesystem coverage ledger. The v2 report is a schema change: consumers must not expect the old duplicate_paths, original_path or full_path columns. Existing large CSVs are not converted or overwritten.

## Verification

Tests cover nested same-name path preservation, normalized full-hash membership, near-linear size growth, existing/in-tree output rejection, symlink-root rejection, empty reports, absolute-path opt-in and failure before publication. Only synthetic temporary fixtures are scanned by the tests.

```sh
python3 -B -m pytest -p no:cacheprovider scan-to-csv/test_doc_source_enriched_v2.py -q
```

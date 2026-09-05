# Repository launcher

`pythons_sort.py` is the canonical launcher. The older
`file_operations/pythons_sort.py` path delegates to it. Both installed command
names, `pythons-sort` and `pythons_sort`, use the same implementation.

## Install and discover

Use Python 3.9–3.12 and install from the checkout:

```bash
python -m pip install -e '.[dev]'
pythons-sort info --all
pythons-sort info --category scanners
```

The installed wheel contains the launcher, not the entire script collection or
its datasets. With a wheel installation, select a checkout explicitly:

```bash
pythons-sort --repository /path/to/pythons info --all
```

`PYTHONS_REPOSITORY` provides the same default. Category listings show direct
Python files in the mapped directories; they are not an exhaustive recursive
inventory. `run` can select an exact nested path even if it is not listed.

## Execute a selected script

```bash
pythons-sort run --dry-run path/to/script.py -- argument --option value
pythons-sort run path/to/script.py -- argument --option value
```

Replace the example path with a real repository-relative script. Read that
script's interface first: these utilities do not share an argument convention,
and some use fixed directories. The launcher forwards arguments unchanged,
preserves the caller's working directory, runs the script in a child Python
process, and returns its exit status. It does not load `.env` or install tool
dependencies.

Put the launcher's `--dry-run` before the script path. It only prints a command;
it does not inspect the script's intended filesystem changes. Flags after the
script path belong to that script. Paths resolving outside the selected
repository, including external symlinks, are rejected.

## Migration from implicit dispatch

The previous `analyze`, `cleanup`, `dedup`, `organize`, `scan`, `rename`, and `pdf`
commands referenced missing `src/tools` directories or imported scripts without
running their `__main__` blocks. Their positional-path and dry-run mappings were
not supported consistently by the target scripts. They now exit with a migration
message instead of reporting misleading success or guessing another script by
filename prefix.

Choose a script explicitly with `run`, and supply the arguments its source
actually supports. This is a CLI compatibility change, not a repair of every
standalone script in the repository.

## Validation

```bash
python -m pytest tests
```

Tests execute small temporary fixture scripts to verify argument forwarding,
exit codes, non-executing previews, and both entry points. They do not run the
repository's cleanup or renaming utilities. Optional coverage can be requested
with `--cov=pythons_sort` when pytest-cov is installed.

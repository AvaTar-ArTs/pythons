"""
Exclusion patterns for file/directory scanning.

Patterns are regular expressions tested against the **full path**
(``os.path.join(root, name)``) so they must match the entire path
segment they target.

Usage::

    from exclude_patterns import DIR_EXCLUDES, FILE_EXCLUDES
    from scanner_utils import is_path_excluded, filter_excluded_dirs

    for root, dirs, files in os.walk(top):
        filter_excluded_dirs(root, dirs, dir_patterns=DIR_EXCLUDES)
        for fname in files:
            fpath = os.path.join(root, fname)
            if is_path_excluded(fpath, file_patterns=FILE_EXCLUDES):
                continue
            # ... process fpath ...

Backward-compatible ``FULL_EXCLUDED_PATTERNS`` is kept so existing
scripts continue to work unchanged.
"""

# ── Directory patterns ────────────────────────────────────────────
# These are checked against os.walk *dirnames*.  The pattern is
# tested on the joined ``os.path.join(root, d)`` path.

DIR_EXCLUDES: list[str] = [
    # Version control
    r"/\.git$",             # .git directory (matches .../dirname/.git)
    r"/\.svn$",
    r"/\.hg$",

    # Package managers & build
    r"/node_modules$",
    r"/\.next$",
    r"/\.nuxt$",
    r"/\.turbo$",
    r"/dist$",
    r"/build$",
    r"/out$",
    r"/target$",            # Rust

    # Python
    r"/__pycache__$",
    r"/\.venv$",
    r"/venv$",
    r"/\.eggs$",
    r"/\.tox$",
    r"/\.mypy_cache$",
    r"/\.ruff_cache$",
    r"/\.pytest_cache$",
    r"/site-packages$",

    # IDE / editor
    r"/\.vscode$",
    r"/\.idea$",
    r"/\.sublime-text$",

    # Cache
    r"/\.cache$",
    r"/\.aider$",
    r"/logs$",

    # Virtual environments / tools
    r"/\.conda$",
    r"/\.poetry$",
    r"/\.pnpm-store$",
]


# ── File patterns ─────────────────────────────────────────────────
# Tested against the full file path.  Use $ anchor wherever possible
# so "build.py" is NOT caught by a pattern meant for "build/".

FILE_EXCLUDES: list[str] = [
    # Python bytecode & artifacts
    r"\.pyc$",
    r"\.pyo$",
    r"\.egg-info/",         # directory-like but often appears in paths

    # OS metadata
    r"/\.DS_Store$",
    r"/Thumbs\.db$",

    # Temporary / backup / swap
    r"\.tmp$",
    r"\.temp$",
    r"\.bak$",
    r"\.swp$",
    r"\.swo$",
    r"~$",
    r"/\.[^/]*\.sw[nop]$",  # vim swap files (.swp, .swo, .swn)

    # Lock files (keep package.json, exclude lock)
    r"/package-lock\.json$",
    r"/yarn\.lock$",
    r"/Pipfile\.lock$",
    r"/poetry\.lock$",
    r"/pnpm-lock\.yaml$",

    # Logs
    r"\.log$",

    # Coverage / test artifacts
    r"/\.nyc_output/",
    r"/jest-coverage",
    r"/\.coverage",
    r"/coverage/",

    # Archives (don't scan inside zips/tars)
    r"\.zip$",
    r"\.tar(\.\w+)?$",
    r"\.gz$",
    r"\.7z$",
    r"\.rar$",
    r"\.bz2$",
    r"\.xz$",

    # Media (skip large binary media in doc scans)
    r"\.mp3$",
    r"\.mp4$",
    r"\.mov$",
    r"\.avi$",
    r"\.mkv$",
    r"\.flac$",
    r"\.wav$",
    r"\.ogg$",
    r"\.jpg$",
    r"\.jpeg$",
    r"\.png$",
    r"\.gif$",
    r"\.bmp$",
    r"\.webp$",
    r"\.tiff$",
    r"\.ico$",
    r"\.woff2?$",
    r"\.ttf$",
    r"\.otf$",
    r"\.eot$",

    # Large data
    r"\.sqlite$",
    r"\.db$",
    r"\.sqlite3$",
]


# ── Backward-compatible flat list ─────────────────────────────────
# Used by doc-source.py, doc-source-evolved.py, ecosystem_scan_compare.py
# which check against the full path with re.match.

FULL_EXCLUDED_PATTERNS: list[str] = [
    # Version control
    r".*\.git.*",
    r".*\.gitignore.*",
    r".*\.svn.*",

    # Package managers
    r".*node_modules.*",
    r".*\.next.*",
    r".*\.nuxt.*",
    r".*dist.*",
    r".*build.*",
    r".*out.*",
    r".*target.*",

    # Python
    r".*__pycache__.*",
    r".*\.pyc.*",
    r".*\.pyo.*",
    r".*\.egg-info.*",
    r".*\.venv.*",
    r".*venv.*",
    r".*\.eggs.*",
    r".*\.mypy_cache.*",
    r".*\.ruff_cache.*",
    r".*\.pytest_cache.*",
    r".*site-packages.*",

    # OS
    r".*\.DS_Store.*",
    r".*Thumbs\.db.*",

    # IDE
    r".*\.vscode.*",
    r".*\.idea.*",
    r".*\.sublime.*",

    # Cache
    r".*\.cache.*",

    # Temp / backup
    r".*\.tmp.*",
    r".*\.temp.*",
    r".*\.bak.*",
    r".*\.swp.*",
    r".*\.swo.*",
    r".*~.*",

    # Locks
    r".*package-lock\.json.*",
    r".*yarn\.lock.*",
    r".*Pipfile\.lock.*",
    r".*poetry\.lock.*",

    # Logs
    r".*\.log.*",
    r".*logs.*",

    # Coverage
    r".*coverage.*",
    r".*\.nyc_output.*",

    # Archives
    r".*\.zip.*",
    r".*\.tar.*",
    r".*\.gz.*",
    r".*\.7z.*",
    r".*\.rar.*",
]


# Ecosystem-level alias (identical to full — kept for compatibility)
ECOSYSTEM_EXCLUDED_PATTERNS = FULL_EXCLUDED_PATTERNS


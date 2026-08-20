"""
Exclusion patterns for document scanning in doc-source.py
Defines regex patterns for directories and files to skip during scans.
"""

# Full list of excluded patterns (regex)
FULL_EXCLUDED_PATTERNS = [
    # Version control and build artifacts
    r'.*\.git.*',
    r'.*\.gitignore.*',
    r'.*node_modules.*',
    r'.*\.next.*',
    r'.*\.nuxt.*',
    r'.*dist.*',
    r'.*build.*',
    r'.*out.*',

    # Python artifacts
    r'.*__pycache__.*',
    r'.*\.pyc.*',
    r'.*\.pyo.*',
    r'.*\.egg-info.*',
    r'.*\.venv.*',
    r'.*venv.*',
    r'.*\.eggs.*',

    # OS and editor artifacts
    r'.*\.DS_Store.*',
    r'.*Thumbs\.db.*',
    r'.*\.vscode.*',
    r'.*\.idea.*',
    r'.*\.sublime.*',
    r'.*\.cache.*',
    
    # Tool-specific artifacts
    r'.*us\.sitesucker\.mac.*', # Added to ignore Sitesucker files

    # Temporary and backup files
    r'.*\.tmp.*',
    r'.*\.temp.*',
    r'.*\.bak.*',
    r'.*\.swp.*',
    r'.*\.swo.*',
    r'.*~.*',
    r'.*\#.*\#.*',

    # Dependency and lockfiles (but not the files themselves for analysis)
    r'.*package-lock\.json.*',
    r'.*yarn\.lock.*',
    r'.*Pipfile\.lock.*',

    # Log files
    r'.*\.log.*',
    r'.*logs.*',

    # Test artifacts
    r'.*coverage.*',
    r'.*\.nyc_output.*',
    r'.*jest-coverage.*',

    # Archive files (keep these from being scanned as documents)
    r'.*\.zip.*',
    r'.*\.tar.*',
    r'.*\.gz.*',
    r'.*\.7z.*',
    r'.*\.rar.*',
]

# Ecosystem-level scan patterns (same as full, but omits project-specific media/directory skips)
# Used by ecosystem_scan_compare.py for cross-project filesystem analysis
ECOSYSTEM_EXCLUDED_PATTERNS = FULL_EXCLUDED_PATTERNS

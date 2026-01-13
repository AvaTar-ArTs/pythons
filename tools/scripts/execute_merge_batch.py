#!/usr/bin/env python3
"""
Execute merge batch - non-interactive
"""

import subprocess
import sys

# Execute merge with --execute flag
result = subprocess.run([
    sys.executable,
    'merge_and_combine.py',
    'execute',
    '--execute',
    '--limit', '10',
    '--strategy', 'copy_unique'
], capture_output=True, text=True)

print(result.stdout)
if result.stderr:
    print("Errors:", result.stderr, file=sys.stderr)

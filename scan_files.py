import os
import sys

files = []
base_path = "/Users/steven/Music/nocturneMelodies"

# Get all Python files
for root, dirs, filenames in os.walk(base_path):
    # Skip venv directories
    dirs[:] = [d for d in dirs if d not in ('venv', '.venv', 'venv313')]
    
    for fname in filenames:
        if fname.endswith('.py'):
            full_path = os.path.join(root, fname)
            files.append(full_path)

# Sort and print
for f in sorted(files):
    print(f)

print(f"\nTotal: {len(files)}", file=sys.stderr)

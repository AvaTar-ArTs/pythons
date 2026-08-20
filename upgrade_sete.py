import re, sys

files = open('/tmp/needs_upgrade.txt').read().splitlines()
changed = []
failed = []

for fname in files:
    try:
        with open(fname, 'r') as f:
            content = f.read()
        # Match first line starting with "set -e" (any variant, optional trailing comment)
        pattern = re.compile(r'^set -e[a-zA-Z]*(\s+pipefail)?(\s*#.*)?$', re.MULTILINE)
        m = pattern.search(content)
        if not m:
            failed.append((fname, "no match"))
            continue
        new_content = content[:m.start()] + "set -euo pipefail" + content[m.end():]
        with open(fname, 'w') as f:
            f.write(new_content)
        changed.append(fname)
    except Exception as e:
        failed.append((fname, str(e)))

print(f"Changed: {len(changed)}")
print(f"Failed: {len(failed)}")
for f, r in failed:
    print(f"  FAILED {f}: {r}")

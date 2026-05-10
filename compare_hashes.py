import sys

local_data = {}
try:
    with open('local_hashes.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(' ', 1)
            if len(parts) == 2:
                h, n = parts
                if h not in local_data: local_data[h] = set()
                local_data[h].add(n)
except FileNotFoundError:
    print("Error: local_hashes.txt not found")
    sys.exit(1)

icloud_data = {}
try:
    with open('icloud_hashes.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(' ', 1)
            if len(parts) == 2:
                h, n = parts
                if h not in icloud_data: icloud_data[h] = set()
                icloud_data[h].add(n)
except FileNotFoundError:
    print("Error: icloud_hashes.txt not found")
    sys.exit(1)

print('=== MISNAMED DUPLICATES (Same Content, Different Name) ===')
for h, names in icloud_data.items():
    if h in local_data:
        local_names = local_data[h]
        if not (names & local_names):
            print("Hash %s: Local '%s' <--> iCloud '%s'" % (h[:8], list(local_names)[0], list(names)[0]))

print('\n=== TRULY UNIQUE CONTENT IN iCLOUD ===')
unique_count = 0
for h, names in icloud_data.items():
    if h not in local_data:
        unique_count += 1
        if unique_count <= 15:
            print("Unique: %s" % list(names)[0])
print("\nTotal Truly Unique iCloud Files: %d" % unique_count)

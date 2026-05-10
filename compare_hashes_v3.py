import os

def parse_md5(filename):
    data = {}
    if not os.path.exists(filename): return data
    with open(filename, 'r') as f:
        for line in f:
            # Format: MD5 (path) = hash
            if ' = ' in line:
                path_part, h = line.strip().split(' = ')
                path = path_part.replace('MD5 (', '').rstrip(')')
                name = os.path.basename(path)
                if h not in data: data[h] = set()
                data[h].add(name)
    return data

local = parse_md5('local_raw.txt')
icloud = parse_md5('icloud_raw.txt')

print('=== MISNAMED DUPLICATES (Same Content, Different Name) ===')
for h, i_names in icloud.items():
    if h in local:
        l_names = local[h]
        if not (i_names & l_names):
            print("Hash %s: Local '%s' <--> iCloud '%s'" % (h[:8], list(l_names)[0], list(i_names)[0]))

print('\n=== TRULY UNIQUE CONTENT IN iCLOUD ===')
unique = [list(names)[0] for h, names in icloud.items() if h not in local]
for item in unique[:15]:
    print("Unique: %s" % item)
print("\nTotal Truly Unique iCloud Files: %d" % len(unique))

import csv
import os

def parse_md_to_list(file_path):
    """Parses pythons-md.txt which seems to be a space-separated list of paths."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The file content appears to be space-separated paths, 
    # but some paths might be quoted if they contain spaces.
    # A simple split might break on spaces within paths.
    # Let's try to handle paths assuming they are separated by spaces,
    # but respecting quotes.
    
    # This is a naive implementation; assuming paths don't contain spaces *unless* quoted.
    import shlex
    return shlex.split(content)

def create_enriched_csv(input_txt, output_csv):
    """Creates a CSV enriched with basic metadata."""
    paths = parse_md_to_list(input_txt)
    
    # Inspired by doc-source-enriched.py
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "filename", "original_path", "full_path", 
            "file_size", "extension", "type"
        ])
        
        for path in paths:
            if not os.path.exists(path):
                continue
            
            try:
                stats = os.stat(path)
                filename = os.path.basename(path)
                ext = os.path.splitext(filename)[1]
                
                writer.writerow([
                    filename,
                    os.path.dirname(path),
                    path,
                    stats.st_size,
                    ext,
                    "file" if os.path.isfile(path) else "directory"
                ])
            except Exception as e:
                print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    create_enriched_csv("/Users/steven/pythons/pythons-md.txt", "/Users/steven/pythons/enriched_files.csv")

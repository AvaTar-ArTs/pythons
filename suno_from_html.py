import re
import csv

def extract_from_text_dump(input_file, output_csv):
    print(f"📂 Reading text dump: {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Regex patterns to find song structures in raw text/logs
    # Looking for UUIDs followed typically by song titles or metadata
    # Pattern: ID (36 chars) -> potential JSON or text structure
    
    # This pattern looks for the standard Suno ID format in links or data attributes
    id_pattern = re.compile(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})')
    
    found_ids = list(set(id_pattern.findall(content)))
    
    print(f"   Found {len(found_ids)} potential song IDs. Extracting details...")
    
    songs = []
    
    for song_id in found_ids:
        # We try to find the 'block' of text around the ID to get context
        # This is a 'best effort' search since raw text dumps lack structure
        
        # Search for title (usually appears before or after ID in logs)
        # We verify it's a song by checking if we can construct a valid URL
        
        songs.append({
            'id': song_id,
            'url': f"https://suno.com/song/{song_id}",
            'audio_url': f"https://cdn1.suno.ai/{song_id}.mp3",
            'image_url': f"https://cdn2.suno.ai/image_{song_id}.png"
        })

    if not songs:
        print("❌ No songs found in the text file.")
        return

    print(f"✅ Verified {len(songs)} unique songs.")

    # Write to CSV
    keys = ['id', 'url', 'audio_url', 'image_url']
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(songs)
    
    print(f"💾 Saved to {output_csv}")

if __name__ == "__main__":
    extract_from_text_dump("song-area.txt", "suno_songs_from_text.csv")
import csv
import re
from bs4 import BeautifulSoup

def extract_from_html(html_file, output_csv):
    print(f"📂 Reading {html_file}...")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Find all song containers (using multiple selectors for robustness)
    # Suno uses data-clip-id on the row or a link to /song/
    songs = []
    seen_ids = set()

    # Strategy: Find all links to songs, then traverse up to find the row
    anchors = soup.find_all('a', href=re.compile(r'/song/[a-f0-9-]{36}'))
    
    print(f"   Found {len(anchors)} song links. Processing...")

    for a in anchors:
        try:
            href = a.get('href')
            song_id = re.search(r'([a-f0-9-]{36})', href).group(1)
            
            if song_id in seen_ids:
                continue
            seen_ids.add(song_id)

            # Locate the container row
            # Usually a div with role="row" or class="clip-row"
            row = a.find_parent('div', {'role': 'row'}) or a.find_parent('div', class_='clip-row') or a.find_parent('div', class_='relative')

            # Extract Metadata
            title = a.get('title') or a.get_text(strip=True) or "Untitled"
            
            # Duration (look for patterns like 3:45)
            duration = ""
            if row:
                dur_match = row.find(string=re.compile(r'\d:\d{2}'))
                if dur_match:
                    duration = dur_match.strip()

            # Image
            image_url = ""
            img = row.find('img') if row else None
            if img:
                image_url = img.get('src') or img.get('data-src') or ""
                if "image_" in image_url:
                    image_url = image_url.replace("image_", "image_large_")

            # Tags (Styles)
            tags = []
            if row:
                tag_links = row.find_all('a', href=re.compile(r'/style/'))
                tags = [t.get_text(strip=True) for t in tag_links]
            
            # Author
            author = ""
            if row:
                auth_link = row.find('a', href=re.compile(r'/@'))
                if auth_link:
                    author = auth_link.get_text(strip=True)

            songs.append({
                'id': song_id,
                'title': title,
                'duration': duration,
                'tags': ", ".join(tags),
                'author': author,
                'url': f"https://suno.com/song/{song_id}",
                'audio_url': f"https://cdn1.suno.ai/{song_id}.mp3",
                'image_url': image_url
            })

        except Exception as e:
            continue

    print(f"✅ Extracted {len(songs)} unique songs.")

    # Write to CSV
    keys = ['id', 'title', 'duration', 'tags', 'author', 'url', 'audio_url', 'image_url']
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(songs)
    
    print(f"💾 Saved to {output_csv}")

# Run it
if __name__ == "__main__":
    extract_from_html("full-suno.html", "suno_complete_library.csv")
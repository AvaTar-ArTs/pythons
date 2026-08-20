import csv
import json
import os
from pathlib import Path

# Paths
CSV_PATH = "/Users/steven/Music/nocturneMelodies/Suno-1366-CoverMP4-path.csv"
OUTPUT_HTML = "/Users/steven/Music/nocturneMelodies/mobile_music_gallery.html"
BASE_DIR = "/Users/steven/Music/nocturneMelodies"

def generate_html():
    songs = []
    
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV not found at {CSV_PATH}")
        return

    print(f"Reading CSV: {CSV_PATH}")
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Fix path: June-Sunos -> June-Suno
            local_path = row.get('path', '')
            if local_path:
                local_path = local_path.replace('June-Sunos', 'June-Suno')
            
            song = {
                "id": row.get('ID', ''),
                "title": row.get('Title', 'Untitled'),
                "audio_url": row.get('Audio URL', ''),
                "local_path": local_path,
                "cover_url": row.get('Cover URL', ''),
                "mp4_url": row.get('Cover MP4 URL', ''),
                "genres": row.get('genres', ''),
                "lyrics": row.get('Lyrics', ''),
                "description": row.get('Description', row.get('inFo', '')),
                "duration": row.get('Duration', '')
            }
            songs.append(song)

    print(f"Loaded {len(songs)} songs.")

    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nocturne Melodies - Mobile First Gallery</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
        }
        .glass {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .song-card {
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .song-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }
        .line-clamp-2 {
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        audio::-webkit-media-controls-panel {
            background-color: #1e293b;
        }
        audio::-webkit-media-controls-current-time-display,
        audio::-webkit-media-controls-time-remaining-display {
            color: #f8fafc;
        }
    </style>
</head>
<body class="min-h-screen pb-20">

    <!-- Header -->
    <header class="sticky top-0 z-50 glass px-4 py-4 shadow-xl">
        <div class="max-w-6xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
            <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                Nocturne Melodies
            </h1>
            <div class="relative flex-1 max-w-md">
                <input type="text" id="searchInput" placeholder="Search songs, genres, lyrics..." 
                    class="w-full bg-slate-800 border border-slate-700 rounded-full py-2 px-5 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-200">
                <span class="absolute right-4 top-2.5 text-slate-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                </span>
            </div>
            <div id="stats" class="text-sm text-slate-400 font-medium">
                Loading...
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-6xl mx-auto p-4 md:p-6">
        <div id="gallery" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <!-- Songs will be injected here -->
        </div>
        <div id="noResults" class="hidden text-center py-20 text-slate-500">
            <p class="text-xl">No songs found matching your search.</p>
        </div>
    </main>
    
    <script>
        const songs = {songs_json};
        const gallery = document.getElementById('gallery');
        const searchInput = document.getElementById('searchInput');
        const stats = document.getElementById('stats');
        const noResults = document.getElementById('noResults');

        function renderSongs(filter = '') {
            const filtered = songs.filter(s => 
                s.title.toLowerCase().includes(filter.toLowerCase()) ||
                s.genres.toLowerCase().includes(filter.toLowerCase()) ||
                s.lyrics.toLowerCase().includes(filter.toLowerCase())
            );

            gallery.innerHTML = '';
            stats.textContent = `Showing ${filtered.length} of ${songs.length} songs`;

            if (filtered.length === 0) {
                noResults.classList.remove('hidden');
            } else {
                noResults.classList.add('hidden');
                filtered.slice(0, 100).forEach(song => { 
                    const card = createSongCard(song);
                    gallery.appendChild(card);
                });
                
                if (filtered.length > 100) {
                    const loadMoreBtn = document.createElement('button');
                    loadMoreBtn.className = "col-span-full py-4 text-blue-400 hover:text-blue-300 font-semibold";
                    loadMoreBtn.textContent = "Load More...";
                    loadMoreBtn.onclick = () => {
                        loadMoreBtn.remove();
                        filtered.slice(100).forEach(song => {
                            gallery.appendChild(createSongCard(song));
                        });
                    };
                    gallery.appendChild(loadMoreBtn);
                }
            }
        }

        function createSongCard(song) {
            const div = document.createElement('div');
            div.className = "glass song-card rounded-2xl overflow-hidden flex flex-col";
            
            const coverSrc = song.cover_url || 'https://via.placeholder.com/400?text=No+Cover';
            
            div.innerHTML = `
                <div class="relative aspect-square overflow-hidden group">
                    <img src="${coverSrc}" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" loading="lazy">
                    <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                        <button class="bg-blue-500 p-4 rounded-full text-white shadow-lg transform scale-75 group-hover:scale-100 transition-transform">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </button>
                    </div>
                    <div class="absolute bottom-2 right-2 bg-black/60 px-2 py-1 rounded text-xs text-white">
                        ${song.duration}
                    </div>
                </div>
                <div class="p-4 flex-1 flex flex-col">
                    <h3 class="font-bold text-lg mb-1 truncate" title="${song.title}">${song.title}</h3>
                    <p class="text-xs text-slate-400 mb-3 line-clamp-2">${song.genres}</p>
                    
                    <audio controls class="w-full h-8 mb-4">
                        <source src="${song.local_path}" type="audio/mpeg">
                        <source src="${song.audio_url}" type="audio/mpeg">
                    </audio>

                    <div class="mt-auto flex gap-2">
                        <button onclick="toggleSection(this, 'lyrics-${song.id}')" class="text-[10px] uppercase tracking-wider font-bold text-slate-400 hover:text-white transition-colors">Lyrics</button>
                        <button onclick="toggleSection(this, 'info-${song.id}')" class="text-[10px] uppercase tracking-wider font-bold text-slate-400 hover:text-white transition-colors">Details</button>
                    </div>
                    
                    <div id="lyrics-${song.id}" class="hidden mt-4 text-xs text-slate-300 bg-slate-800/50 p-3 rounded-lg max-h-40 overflow-y-auto whitespace-pre-wrap font-serif leading-relaxed">
                        ${song.lyrics || 'No lyrics available.'}
                    </div>
                    <div id="info-${song.id}" class="hidden mt-4 text-xs text-slate-300 bg-slate-800/50 p-3 rounded-lg">
                        ${song.description || 'No description available.'}
                    </div>
                </div>
            `;
            return div;
        }

        function toggleSection(btn, id) {
            const el = document.getElementById(id);
            const isHidden = el.classList.contains('hidden');
            
            if (isHidden) {
                el.classList.remove('hidden');
                btn.classList.add('text-blue-400');
            } else {
                el.classList.add('hidden');
                btn.classList.remove('text-blue-400');
            }
        }

        searchInput.addEventListener('input', (e) => {
            renderSongs(e.target.value);
        });

        // Initial render
        renderSongs();
    </script>
</body>
</html>
    """

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_template.replace('{songs_json}', json.dumps(songs)))
    
    print(f"Successfully generated: {OUTPUT_HTML}")

if __name__ == "__main__":
    generate_html()

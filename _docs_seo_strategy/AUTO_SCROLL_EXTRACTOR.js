// ?? AUTO-SCROLL SUNO EXTRACTOR - Paste into Dev Console
// =========================================================
// This will auto-scroll to load ALL songs, then extract them!

console.log('?? Starting AUTO-SCROLL Extractor...');
console.log('? This will scroll through the page to load all songs...');

// Configuration
const SCROLL_DELAY = 1500; // Wait 1.5 seconds between scrolls
const MAX_SCROLLS = 200;   // Maximum number of scrolls (safety limit)

let scrollCount = 0;
let lastHeight = 0;
let noChangeCount = 0;

// Auto-scroll function
function autoScroll() {
    return new Promise((resolve) => {
        const scrollInterval = setInterval(() => {
            // Scroll to bottom
            window.scrollTo(0, document.body.scrollHeight);
            
            const currentHeight = document.body.scrollHeight;
            
            // Check if page height changed
            if (currentHeight === lastHeight) {
                noChangeCount++;
                console.log(`   No new content loaded... (${noChangeCount}/3)`);
                
                // If no change for 3 scrolls, we're done
                if (noChangeCount >= 3) {
                    clearInterval(scrollInterval);
                    console.log('? Finished scrolling!');
                    resolve();
                }
            } else {
                noChangeCount = 0;
                lastHeight = currentHeight;
                scrollCount++;
                
                // Count current songs
                const currentSongCount = document.querySelectorAll('[data-clip-id]').length;
                console.log(`   Scroll ${scrollCount}: Found ${currentSongCount} songs...`);
            }
            
            // Safety limit
            if (scrollCount >= MAX_SCROLLS) {
                clearInterval(scrollInterval);
                console.log('??  Reached max scrolls, stopping...');
                resolve();
            }
            
        }, SCROLL_DELAY);
    });
}

// Extract function
async function extractAllSongs() {
    // Step 1: Auto-scroll to load everything
    console.log('\n?? Step 1: Auto-scrolling to load all songs...');
    await autoScroll();
    
    // Step 2: Extract all songs
    console.log('\n?? Step 2: Extracting song data...');
    
    const songs = [];
    const songElements = document.querySelectorAll('[data-clip-id]');
    
    console.log(`   Found ${songElements.length} total songs!`);
    
    songElements.forEach((el, index) => {
        try {
            const song = {
                id: el.getAttribute('data-clip-id'),
                title: el.querySelector('[title]')?.getAttribute('title') || '',
                duration: el.querySelector('.font-mono')?.textContent?.trim() || '',
                url: 'https://suno.com/song/' + el.getAttribute('data-clip-id'),
                audio_url: 'https://cdn1.suno.ai/' + el.getAttribute('data-clip-id') + '.mp3',
                image_url: el.querySelector('img[src*="suno.ai"]')?.getAttribute('src') || '',
            };
            
            // Extract tags
            const tagElements = el.querySelectorAll('[href*="/style/"]');
            if (tagElements.length > 0) {
                song.tags = Array.from(tagElements).map(t => t.textContent.trim()).join(', ');
            }
            
            // Extract version
            const versionEl = el.querySelector('[style*="FD429C"]');
            if (versionEl) {
                song.version = versionEl.textContent.trim();
            }
            
            // Extract stats (plays, likes, comments)
            const statsElements = el.querySelectorAll('.text-\\[12px\\] .font-medium');
            if (statsElements.length >= 3) {
                song.plays = statsElements[0]?.textContent.trim() || '0';
                song.likes = statsElements[1]?.textContent.trim() || '0';
                song.comments = statsElements[2]?.textContent.trim() || '0';
            }
            
            if (song.title) {
                songs.push(song);
            }
        } catch (e) {
            console.error(`Error on song ${index}:`, e);
        }
    });
    
    console.log(`? Extracted ${songs.length} songs!`);
    
    // Step 3: Create CSV
    console.log('\n?? Step 3: Creating CSV...');
    
    const csv = [
        'id,title,duration,tags,version,plays,likes,comments,url,audio_url,image_url',
        ...songs.map(s => {
            const title = (s.title || '').replace(/"/g, '""');
            const tags = (s.tags || '').replace(/"/g, '""');
            return `${s.id},"${title}",${s.duration},"${tags}",${s.version || ''},${s.plays || '0'},${s.likes || '0'},${s.comments || '0'},${s.url},${s.audio_url},${s.image_url}`;
        })
    ].join('\n');
    
    // Step 4: Download CSV
    console.log('\n?? Step 4: Downloading CSV...');
    
    const blob = new Blob([csv], {type: 'text/csv'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    
    const timestamp = new Date().toISOString().slice(0,19).replace(/:/g,'-');
    const filename = `suno-songs-${timestamp}.csv`;
    
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    console.log(`? Downloaded: ${filename}`);
    console.log('?? Check your Downloads folder!');
    
    // Step 5: Copy to clipboard
    console.log('\n?? Step 5: Copying JSON to clipboard...');
    
    const jsonData = JSON.stringify(songs, null, 2);
    navigator.clipboard.writeText(jsonData).then(() => {
        console.log('? JSON copied to clipboard!');
    }).catch(() => {
        console.log('??  Could not copy to clipboard');
    });
    
    // Summary
    console.log('\n' + '='.repeat(70));
    console.log('?? EXTRACTION COMPLETE!');
    console.log('='.repeat(70));
    console.log(`\n   Total songs: ${songs.length}`);
    console.log(`   CSV file: ${filename}`);
    console.log(`   Location: ~/Downloads/`);
    
    // Show samples
    console.log('\n?? First 10 songs:');
    songs.slice(0, 10).forEach((s, i) => {
        console.log(`   ${i + 1}. ${s.title} (${s.duration}) - ${s.version}`);
    });
    
    if (songs.length > 10) {
        console.log(`   ... and ${songs.length - 10} more!`);
    }
    
    console.log('\n?? To view all data in console, type: extractedSongs');
    
    // Return for inspection
    window.extractedSongs = songs;
    return songs;
}

// Run the extraction
extractAllSongs();

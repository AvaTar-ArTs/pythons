// ?? SAVED HTML EXTRACTOR - For main.html & evolves.html
// ========================================================
// Paste this into dev console when viewing saved HTML files

console.log('?? Saved HTML Extractor Starting...');

const songs = [];
const extractedIds = new Set();

// Method 1: Extract from href links
console.log('?? Looking for song links...');
const songLinks = document.querySelectorAll('a[href*="/song/"]');
console.log(`   Found ${songLinks.length} song links`);

songLinks.forEach((link, index) => {
    try {
        // Extract song ID from href
        const href = link.getAttribute('href');
        const match = href.match(/\/song\/([a-f0-9-]{36})/);
        
        if (match) {
            const songId = match[1];
            
            if (extractedIds.has(songId)) return; // Skip duplicates
            extractedIds.add(songId);
            
            // Get title
            const title = link.getAttribute('title') || 
                         link.textContent.trim() ||
                         link.querySelector('span')?.textContent.trim() || '';
            
            // Find parent container to get more data
            const container = link.closest('[class*="flex"]')?.parentElement?.parentElement;
            
            let duration = '';
            let imageUrl = '';
            let tags = '';
            
            if (container) {
                // Extract duration
                const durationEl = container.querySelector('.font-mono') ||
                                  container.querySelector('div:has(>*)');
                if (durationEl) {
                    const text = durationEl.textContent;
                    const timeMatch = text.match(/\d+:\d+/);
                    if (timeMatch) duration = timeMatch[0];
                }
                
                // Extract image
                const imgEl = container.querySelector('img[src*="suno"]');
                if (imgEl) {
                    imageUrl = imgEl.getAttribute('src') || imgEl.getAttribute('data-src') || '';
                }
                
                // Extract tags
                const tagLinks = container.querySelectorAll('a[href*="/style/"]');
                if (tagLinks.length > 0) {
                    tags = Array.from(tagLinks).map(t => t.textContent.trim()).join(', ');
                }
            }
            
            songs.push({
                id: songId,
                title: title,
                duration: duration,
                tags: tags,
                url: `https://suno.com/song/${songId}`,
                audio_url: `https://cdn1.suno.ai/${songId}.mp3`,
                image_url: imageUrl
            });
        }
    } catch (e) {
        console.error(`Error on link ${index}:`, e);
    }
});

console.log(`? Extracted ${songs.length} songs!`);

if (songs.length === 0) {
    console.error('? No songs extracted!');
    console.error('Debugging info:');
    console.error(`   Song links found: ${songLinks.length}`);
    console.error(`   Page title: ${document.title}`);
    console.error('\nTry:');
    console.error('   1. Make sure main.html or evolves.html is open');
    console.error('   2. Wait for page to fully render');
    console.error('   3. Paste script again');
} else {
    // Show preview
    console.log('\n?? First 10 songs:');
    songs.slice(0, 10).forEach((s, i) => {
        console.log(`   ${i + 1}. ${s.title} ${s.duration ? '(' + s.duration + ')' : ''}`);
    });
    
    if (songs.length > 10) {
        console.log(`   ... and ${songs.length - 10} more!`);
    }
    
    // Create CSV
    console.log('\n?? Creating CSV...');
    
    const csv = [
        'id,title,duration,tags,url,audio_url,image_url',
        ...songs.map(s => {
            const title = (s.title || '').replace(/"/g, '""');
            const tags = (s.tags || '').replace(/"/g, '""');
            return `${s.id},"${title}",${s.duration || ''},"${tags}",${s.url},${s.audio_url},${s.image_url || ''}`;
        })
    ].join('\n');
    
    // Download CSV
    console.log('?? Downloading CSV...');
    
    const blob = new Blob([csv], {type: 'text/csv;charset=utf-8'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    
    const timestamp = new Date().toISOString().slice(0,19).replace(/:/g,'-');
    const filename = `suno-saved-html-${timestamp}.csv`;
    
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    console.log('\n' + '='.repeat(70));
    console.log('?? EXTRACTION COMPLETE!');
    console.log('='.repeat(70));
    console.log(`\n   ?? Total songs: ${songs.length}`);
    console.log(`   ?? CSV file: ${filename}`);
    console.log(`   ?? Location: ~/Downloads/`);
    console.log('\n?? Type "extractedSongs" to view data');
    
    // Store globally
    window.extractedSongs = songs;
}

songs;

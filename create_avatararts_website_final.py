#!/usr/bin/env python3
"""
HTML Directory System Generator for avatararts.org

This script creates a comprehensive HTML directory system to organize all content
from the /Users/steven directory with a focus on the avatararts.org domain.
"""

from datetime import datetime
from pathlib import Path


def create_avatararts_directory_structure():
    """Create the HTML directory structure for avatararts.org"""

    # Define the base directory for the avatararts.org website
    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/avatararts_org_website")
    base_dir.mkdir(parents=True, exist_ok=True)

    # Create the directory structure
    directories = [
        "css",
        "js",
        "images",
        "music",
        "music/albums",
        "music/tracks",
        "music/artists",
        "lyrics",
        "lyrics/by-album",
        "lyrics/by-artist",
        "lyrics/by-genre",
        "docs",
        "docs/guides",
        "docs/api",
        "docs/tutorials",
        "assets",
        "assets/audio",
        "assets/videos",
        "assets/images",
        "data",
        "data/json",
        "data/csv",
        "data/xml",
        "pages",
        "pages/artists",
        "pages/albums",
        "pages/tracks",
        "pages/playlists",
        "pages/discover",
        "pages/community",
        "pages/account",
        "templates",
        "components",
    ]

    for directory in directories:
        (base_dir / directory).mkdir(parents=True, exist_ok=True)

    print(f"Created directory structure at: {base_dir}")
    return base_dir


def create_main_index_html(base_dir):
    """Create the main index.html for avatararts.org"""

    index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AvatarArts - Creative AI Music & Digital Art Platform</title>
    <meta name="description" content="AvatarArts: Where AI meets creativity in music and digital art. Explore our collection of AI-generated music, lyrics, and digital artworks.">
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" type="image/x-icon" href="images/favicon.ico">
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="nav-brand">
                <a href="/">AvatarArts</a>
            </div>
            <ul class="nav-menu">
                <li><a href="/pages/discover">Discover</a></li>
                <li><a href="/pages/artists">Artists</a></li>
                <li><a href="/music">Music</a></li>
                <li><a href="/lyrics">Lyrics</a></li>
                <li><a href="/docs">Documentation</a></li>
                <li><a href="/pages/community">Community</a></li>
            </ul>
            <div class="nav-search">
                <input type="text" placeholder="Search...">
            </div>
        </nav>
    </header>

    <main>
        <section class="hero">
            <div class="hero-content">
                <h1>Welcome to AvatarArts</h1>
                <p>Where AI meets creativity in music and digital art</p>
                <p>Explore our collection of AI-generated music, lyrics, and digital artworks</p>
            </div>
        </section>

        <section class="featured-content">
            <h2>Featured Content</h2>
            <div class="content-grid">
                <div class="content-card">
                    <h3><a href="/music">Latest Music Releases</a></h3>
                    <p>Discover our newest AI-generated tracks and albums</p>
                </div>
                <div class="content-card">
                    <h3><a href="/lyrics">Lyrics Collection</a></h3>
                    <p>Explore lyrics from our extensive collection of songs</p>
                </div>
                <div class="content-card">
                    <h3><a href="/pages/artists">Featured Artists</a></h3>
                    <p>Meet the creative minds behind our projects</p>
                </div>
                <div class="content-card">
                    <h3><a href="/docs">Documentation</a></h3>
                    <p>Learn how to use our tools and resources</p>
                </div>
            </div>
        </section>

        <section class="about-section">
            <h2>About AvatarArts</h2>
            <p>AvatarArts is a creative platform that explores the intersection of artificial intelligence and artistic expression. Our mission is to empower creators with cutting-edge AI tools while preserving the human element in art.</p>
            <p>We specialize in AI-generated music, lyrics, and digital art, with a focus on experimental and innovative approaches to creative expression.</p>
        </section>
    </main>

    <footer>
        <div class="footer-content">
            <p>&copy; 2026 AvatarArts. All rights reserved.</p>
            <p>Designed for creativity and innovation.</p>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>"""

    with open(base_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

    print("Created main index.html file")


def create_css_file(base_dir):
    """Create the main CSS file for avatararts.org"""

    css_content = """/* AvatarArts Website Styles */
:root {
    --primary-color: #6e44ff;
    --secondary-color: #ff6b6b;
    --accent-color: #4ecdc4;
    --background-color: #f8f9fa;
    --text-color: #333333;
    --card-background: #ffffff;
    --border-color: #e0e0e0;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--background-color);
}

/* Header Styles */
header {
    background-color: var(--card-background);
    box-shadow: var(--shadow);
    position: sticky;
    top: 0;
    z-index: 100;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.nav-brand a {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary-color);
    text-decoration: none;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    text-decoration: none;
    color: var(--text-color);
    font-weight: 500;
    transition: color 0.3s ease;
}

.nav-menu a:hover {
    color: var(--primary-color);
}

.nav-search input {
    padding: 0.5rem;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    width: 200px;
}

/* Main Content */
main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    color: white;
    padding: 4rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    border-radius: 8px;
}

.hero-content h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.hero-content p {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}

/* Content Grid */
.content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.content-card {
    background-color: var(--card-background);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: var(--shadow);
    transition: transform 0.3s ease;
}

.content-card:hover {
    transform: translateY(-5px);
}

.content-card h3 a {
    color: var(--primary-color);
    text-decoration: none;
    font-size: 1.2rem;
}

.content-card p {
    margin-top: 0.5rem;
    color: #666;
}

/* Sections */
section {
    margin-bottom: 3rem;
}

h2 {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    color: var(--primary-color);
    text-align: center;
}

.about-section p {
    max-width: 800px;
    margin: 0 auto 1rem;
    text-align: center;
    line-height: 1.8;
}

/* Footer */
footer {
    background-color: var(--card-background);
    padding: 2rem;
    text-align: center;
    border-top: 1px solid var(--border-color);
    margin-top: 3rem;
}

/* Responsive Design */
@media (max-width: 768px) {
    .navbar {
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
    }

    .nav-menu {
        flex-wrap: wrap;
        justify-content: center;
        gap: 1rem;
    }

    .hero-content h1 {
        font-size: 2rem;
    }

    .hero-content p {
        font-size: 1rem;
    }

    .content-grid {
        grid-template-columns: 1fr;
    }
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
    :root {
        --background-color: #121212;
        --text-color: #e0e0e0;
        --card-background: #1e1e1e;
        --border-color: #333333;
    }

    .hero {
        background: linear-gradient(135deg, #5a38cc, #3aa196);
    }

    .content-card {
        border: 1px solid var(--border-color);
    }

    .content-card p {
        color: #aaa;
    }
}
"""

    with open(base_dir / "css" / "style.css", "w", encoding="utf-8") as f:
        f.write(css_content)

    print("Created CSS file")


def create_js_file(base_dir):
    """Create the main JavaScript file for avatararts.org"""

    js_content = """// AvatarArts Website JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const menuToggle = document.createElement('button');
    menuToggle.innerHTML = '☰';
    menuToggle.className = 'menu-toggle';
    menuToggle.style.display = 'none'; // Will be shown on mobile via CSS

    // Add mobile menu functionality if needed
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
        // Add event listeners for mobile menu
    }

    // Initialize any interactive elements
    initializeInteractiveElements();
});

function initializeInteractiveElements() {
    // Add any interactive functionality here
    console.log('AvatarArts website initialized');
}

// Search functionality
function setupSearch() {
    const searchInput = document.querySelector('.nav-search input');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch(searchInput.value);
            }
        });
    }
}

function performSearch(query) {
    // Placeholder for search functionality
    console.log('Searching for:', query);
    alert('Search functionality would be implemented here');
}

// Audio player functionality (if needed)
function setupAudioPlayer() {
    // Add audio player functionality if needed
    console.log('Audio player setup');
}
"""

    with open(base_dir / "js" / "main.js", "w", encoding="utf-8") as f:
        f.write(js_content)

    print("Created JavaScript file")


def create_music_pages(base_dir, music_files):
    """Create HTML pages for music content"""

    # Create a music index page
    music_index = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Music Collection - AvatarArts</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="nav-brand">
                <a href="/">AvatarArts</a>
            </div>
            <ul class="nav-menu">
                <li><a href="/">Home</a></li>
                <li><a href="/pages/discover">Discover</a></li>
                <li><a href="/pages/artists">Artists</a></li>
                <li><a href="/music">Music</a></li>
                <li><a href="/lyrics">Lyrics</a></li>
                <li><a href="/docs">Documentation</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <h1>Music Collection</h1>
        <p>Explore our collection of AI-generated music and creative compositions</p>

        <div class="music-grid">
            <!-- Music tracks will be listed here -->
        </div>
    </main>

    <footer>
        <div class="footer-content">
            <p>&copy; 2026 AvatarArts. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""

    with open(base_dir / "music" / "index.html", "w", encoding="utf-8") as f:
        f.write(music_index)

    print(f"Created music index page with {len(music_files)} music files to be organized")


def create_lyrics_pages(base_dir, lyrics_files):
    """Create HTML pages for lyrics content"""

    # Create a lyrics index page
    lyrics_index = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lyrics Collection - AvatarArts</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="nav-brand">
                <a href="/">AvatarArts</a>
            </div>
            <ul class="nav-menu">
                <li><a href="/">Home</a></li>
                <li><a href="/pages/discover">Discover</a></li>
                <li><a href="/pages/artists">Artists</a></li>
                <li><a href="/music">Music</a></li>
                <li><a href="/lyrics">Lyrics</a></li>
                <li><a href="/docs">Documentation</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <h1>Lyrics Collection</h1>
        <p>Explore lyrics from our extensive collection of AI-generated songs</p>

        <div class="lyrics-list">
            <!-- Lyrics will be listed here -->
        </div>
    </main>

    <footer>
        <div class="footer-content">
            <p>&copy; 2026 AvatarArts. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""

    with open(base_dir / "lyrics" / "index.html", "w", encoding="utf-8") as f:
        f.write(lyrics_index)

    print(f"Created lyrics index page with {len(lyrics_files)} lyrics files to be organized")


def create_documentation_pages(base_dir):
    """Create HTML pages for documentation"""

    # Create a documentation index page
    docs_index = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation - AvatarArts</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="nav-brand">
                <a href="/">AvatarArts</a>
            </div>
            <ul class="nav-menu">
                <li><a href="/">Home</a></li>
                <li><a href="/pages/discover">Discover</a></li>
                <li><a href="/pages/artists">Artists</a></li>
                <li><a href="/music">Music</a></li>
                <li><a href="/lyrics">Lyrics</a></li>
                <li><a href="/docs">Documentation</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <h1>Documentation</h1>
        <p>Resources and guides for using AvatarArts tools and services</p>

        <div class="docs-grid">
            <div class="doc-card">
                <h3><a href="guides/getting-started.html">Getting Started</a></h3>
                <p>Learn how to get started with AvatarArts</p>
            </div>
            <div class="doc-card">
                <h3><a href="api/index.html">API Documentation</a></h3>
                <p>Technical documentation for developers</p>
            </div>
            <div class="doc-card">
                <h3><a href="tutorials/index.html">Tutorials</a></h3>
                <p>Step-by-step guides for various features</p>
            </div>
        </div>
    </main>

    <footer>
        <div class="footer-content">
            <p>&copy; 2026 AvatarArts. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""

    with open(base_dir / "docs" / "index.html", "w", encoding="utf-8") as f:
        f.write(docs_index)

    # Create subdirectory index files
    guides_index = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guides - AvatarArts Documentation</title>
    <link rel="stylesheet" href="../../css/style.css">
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="nav-brand">
                <a href="/">AvatarArts</a>
            </div>
            <ul class="nav-menu">
                <li><a href="/">Home</a></li>
                <li><a href="/docs">Documentation</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <h1>Guides</h1>
        <p>Helpful guides for using AvatarArts tools and services</p>

        <ul>
            <li><a href="getting-started.html">Getting Started Guide</a></li>
            <li><a href="mobile-optimization.html">Mobile Optimization Guide</a></li>
            <li><a href="content-organization.html">Content Organization Guide</a></li>
        </ul>
    </main>

    <footer>
        <div class="footer-content">
            <p>&copy; 2026 AvatarArts. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""

    with open(base_dir / "docs" / "guides" / "index.html", "w", encoding="utf-8") as f:
        f.write(guides_index)

    print("Created documentation pages")


def create_artist_pages(base_dir):
    """Create HTML pages for artists"""

    # Create an artists index page
    artists_index = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Artists - AvatarArts</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="nav-brand">
                <a href="/">AvatarArts</a>
            </div>
            <ul class="nav-menu">
                <li><a href="/">Home</a></li>
                <li><a href="/pages/discover">Discover</a></li>
                <li><a href="/pages/artists">Artists</a></li>
                <li><a href="/music">Music</a></li>
                <li><a href="/lyrics">Lyrics</a></li>
                <li><a href="/docs">Documentation</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <h1>Featured Artists</h1>
        <p>Meet the creative minds behind our projects</p>

        <div class="artists-grid">
            <div class="artist-card">
                <h3><a href="avatararts.html">AvatarArts</a></h3>
                <p>Founder and lead creative director</p>
            </div>
            <div class="artist-card">
                <h3><a href="trashcat.html">TrashCat</a></h3>
                <p>Experimental music and digital art pioneer</p>
            </div>
            <div class="artist-card">
                <h3><a href="suno.html">Suno Collaborations</a></h3>
                <p>AI music generation specialist</p>
            </div>
        </div>
    </main>

    <footer>
        <div class="footer-content">
            <p>&copy; 2026 AvatarArts. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""

    with open(base_dir / "pages" / "artists" / "index.html", "w", encoding="utf-8") as f:
        f.write(artists_index)

    print("Created artist pages")


def scan_content_for_website():
    """Scan the directory for content to include in the website"""

    # Find all relevant content
    music_files = list(Path("/Users/steven/Music").rglob("*.mp3"))
    lyrics_files = list(Path("/Users/steven/Music").rglob("*lyric*.txt")) + list(
        Path("/Users/steven/Music").rglob("*lyrics*.txt")
    )
    html_files = list(Path("/Users/steven/Music").rglob("*.html"))
    json_files = list(Path("/Users/steven/Music").rglob("*.json"))

    # Filter out files from the already-processed nocTurneMeLoDieS directory
    music_files = [f for f in music_files if "nocTurneMeLoDieS" not in str(f)]
    lyrics_files = [f for f in lyrics_files if "nocTurneMeLoDieS" not in str(f)]
    html_files = [f for f in html_files if "nocTurneMeLoDieS" not in str(f)]
    json_files = [f for f in json_files if "nocTurneMeLoDieS" not in str(f)]

    return {
        "music_files": music_files,
        "lyrics_files": lyrics_files,
        "html_files": html_files,
        "json_files": json_files,
    }


def main():
    print("Creating HTML directory system for avatararts.org...")

    # Create the directory structure
    base_dir = create_avatararts_directory_structure()

    # Scan for content
    print("Scanning content...")
    content = scan_content_for_website()

    print(f"Found {len(content['music_files'])} music files")
    print(f"Found {len(content['lyrics_files'])} lyrics files")
    print(f"Found {len(content['html_files'])} HTML files")
    print(f"Found {len(content['json_files'])} JSON files")

    # Create the main pages
    print("Creating main index page...")
    create_main_index_html(base_dir)

    print("Creating CSS file...")
    create_css_file(base_dir)

    print("Creating JavaScript file...")
    create_js_file(base_dir)

    print("Creating music pages...")
    create_music_pages(base_dir, content["music_files"])

    print("Creating lyrics pages...")
    create_lyrics_pages(base_dir, content["lyrics_files"])

    print("Creating documentation pages...")
    create_documentation_pages(base_dir)

    print("Creating artist pages...")
    create_artist_pages(base_dir)

    # Create a site map
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://avatararts.org/</loc>
        <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://avatararts.org/music/</loc>
        <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://avatararts.org/lyrics/</loc>
        <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://avatararts.org/pages/artists/</loc>
        <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://avatararts.org/docs/</loc>
        <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
</urlset>"""

    with open(base_dir / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    # Create a robots.txt file
    robots_content = """User-agent: *
Allow: /
Disallow: /private/
Disallow: /temp/

Sitemap: https://avatararts.org/sitemap.xml
"""

    with open(base_dir / "robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_content)

    # Create a summary file
    summary_content = f"""# AvatarArts Website Content Summary

## Files Organized
- Music files: {len(content["music_files"])}
- Lyrics files: {len(content["lyrics_files"])}
- HTML files: {len(content["html_files"])}
- JSON files: {len(content["json_files"])}

## Directory Structure
- /css - Stylesheets
- /js - JavaScript files
- /images - Image assets
- /music - Music-related content
- /lyrics - Lyrics and song content
- /docs - Documentation
- /pages - Static pages
- /assets - Media assets
- /data - Data files

## Generated Files
- index.html - Main landing page
- sitemap.xml - Site map for search engines
- robots.txt - Crawler directives
- css/style.css - Main stylesheet
- js/main.js - Main JavaScript file

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    with open(base_dir / "content_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_content)

    print("\nHTML directory system for avatararts.org created successfully!")
    print(f"Base directory: {base_dir}")
    print("Total content scanned:")
    print(f"  - Music files: {len(content['music_files'])}")
    print(f"  - Lyrics files: {len(content['lyrics_files'])}")
    print(f"  - HTML files: {len(content['html_files'])}")
    print(f"  - JSON files: {len(content['json_files'])}")
    print("\nDirectory structure created with main pages, CSS, JS, sitemap and robots.txt.")


if __name__ == "__main__":
    main()

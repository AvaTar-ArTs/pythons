#!/usr/bin/env python3
"""
NocturneMelodies Content Consolidation Script - VERSION 2
Enhanced with better content analysis and categorization

This script creates an improved HTML directory system for NocturneMelodies content
with enhanced categorization based on content analysis.
"""

from datetime import datetime
from pathlib import Path


def create_enhanced_nocturnemelodies_structure():
    """Create an enhanced NocturneMelodies directory structure with better categorization"""

    # Define the base directory for the enhanced NocturneMelodies content
    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/NOCTURNEMELODIES_WEB_STRUCTURE_V2")
    base_dir.mkdir(parents=True, exist_ok=True)

    # Create a more detailed directory structure
    directories = [
        "css",
        "js",
        "images",
        "music",
        "music/albums",
        "music/tracks",
        "music/artists",
        "music/genres",
        "music/analysis",
        "lyrics",
        "lyrics/by-album",
        "lyrics/by-artist",
        "lyrics/by-genre",
        "lyrics/by-theme",
        "docs",
        "docs/guides",
        "docs/api",
        "docs/tutorials",
        "docs/reference",
        "assets",
        "assets/audio",
        "assets/videos",
        "assets/images",
        "data",
        "data/json",
        "data/csv",
        "data/xml",
        "data/backup",
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
        "gallery",
        "seo",
        "automation",
        "scripts",
        "logs",
        "backup",
    ]

    for directory in directories:
        (base_dir / directory).mkdir(parents=True, exist_ok=True)

    print(f"Created enhanced NocturneMelodies directory structure at: {base_dir}")
    return base_dir


def analyze_file_content_for_category(filepath):
    """Analyze file content to determine the most appropriate category"""
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            content = f.read().lower()[:2000]  # Read first 2000 chars for analysis

        # Content-based classification
        content_indicators = {
            "lyrics": [
                "verse",
                "chorus",
                "lyric",
                "song",
                "sung",
                "sing",
                "vocal",
                "music",
            ],
            "music_analysis": [
                "analysis",
                "composition",
                "structure",
                "chord",
                "tempo",
                "beat",
                "bpm",
                "key",
            ],
            "documentation": [
                "documentation",
                "guide",
                "tutorial",
                "reference",
                "how to",
                "instructions",
            ],
            "conversation": [
                "user:",
                "assistant:",
                "chat",
                "conversation",
                "dialogue",
                "response",
            ],
            "code": [
                "import",
                "def ",
                "function",
                "class ",
                "var ",
                "const ",
                "console.log",
                "function(",
                "script",
            ],
            "seo": [
                "seo",
                "keywords",
                "meta",
                "title",
                "description",
                "tags",
                "optimize",
            ],
            "automation": [
                "automat",
                "script",
                "workflow",
                "process",
                "routine",
                "task",
            ],
            "gallery": [
                "gallery",
                "image",
                "photo",
                "picture",
                "visual",
                "artwork",
                "cover",
            ],
        }

        scores = {}
        for category, keywords in content_indicators.items():
            score = sum(1 for keyword in keywords if keyword in content)
            scores[category] = score

        # Return the category with highest score, or 'misc' if no strong indicators
        best_category = max(scores, key=scores.get)
        if scores[best_category] == 0:
            return "misc"

        return best_category
    except (OSError, ValueError):
        return "misc"


def get_enhanced_content_category(filepath):
    """Determine the category for a file based on name and content analysis"""
    filename = filepath.name.lower()
    filepath_str = str(filepath).lower()

    # Filename-based classification with priority
    if "lyric" in filename or "song" in filename:
        return "lyrics"
    elif "analysis" in filename:
        return "music_analysis"
    elif "doc" in filename or "readme" in filename or "guide" in filename:
        return "documentation"
    elif "conversation" in filepath_str or "chat" in filepath_str:
        return "conversation"
    elif filepath.suffix.lower() in [".py", ".js", ".ts", ".jsx", ".tsx", ".html"]:
        return "code"
    elif "seo" in filename or "keyword" in filename:
        return "seo"
    elif "auto" in filename or "script" in filename or "workflow" in filename:
        return "automation"
    elif "gallery" in filename or "image" in filename or "cover" in filename:
        return "gallery"
    elif "album" in filename:
        return "music/albums"
    elif "artist" in filename:
        return "pages/artists"

    # Content-based classification as fallback
    return analyze_file_content_for_category(filepath)


def create_enhanced_main_index_html(base_dir):
    """Create an enhanced main index.html for NocturneMelodies V2"""

    index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NocturneMelodies V2 - Enhanced Creative AI Music Platform</title>
    <meta name="description" content="NocturneMelodies V2: Enhanced platform for AI-generated music, lyrics, and digital art. Improved organization and mobile optimization.">
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" type="image/x-icon" href="images/favicon.ico">
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="nav-brand">
                <a href="/">NocturneMelodies V2</a>
            </div>
            <ul class="nav-menu">
                <li><a href="/pages/discover">Discover</a></li>
                <li><a href="/pages/artists">Artists</a></li>
                <li><a href="/music">Music</a></li>
                <li><a href="/lyrics">Lyrics</a></li>
                <li><a href="/docs">Documentation</a></li>
                <li><a href="/gallery">Gallery</a></li>
            </ul>
            <div class="nav-search">
                <input type="text" placeholder="Search NocturneMelodies...">
            </div>
        </nav>
    </header>

    <main>
        <section class="hero">
            <div class="hero-content">
                <h1>Welcome to NocturneMelodies V2</h1>
                <p>Enhanced platform for AI-generated music and digital art</p>
                <p>Better organization, improved mobile experience, and expanded content</p>
            </div>
        </section>

        <section class="featured-content">
            <h2>Enhanced Features</h2>
            <div class="content-grid">
                <div class="content-card">
                    <h3><a href="/music">Improved Music Organization</a></h3>
                    <p>Better categorization and discovery of AI-generated tracks</p>
                </div>
                <div class="content-card">
                    <h3><a href="/lyrics">Advanced Lyrics Indexing</a></h3>
                    <p>Organized by album, artist, genre, and theme</p>
                </div>
                <div class="content-card">
                    <h3><a href="/gallery">Visual Content Gallery</a></h3>
                    <p>Showcase of associated artwork and visual elements</p>
                </div>
                <div class="content-card">
                    <h3><a href="/docs">Comprehensive Documentation</a></h3>
                    <p>Enhanced guides and reference materials</p>
                </div>
            </div>
        </section>

        <section class="about-section">
            <h2>About NocturneMelodies V2</h2>
            <p>This enhanced version builds upon the original NocturneMelodies platform with improved content organization, better mobile optimization, and expanded functionality. The system now includes advanced categorization based on content analysis and improved accessibility across all devices.</p>
            <p>We continue to focus on the intersection of artificial intelligence and musical expression, providing creators with cutting-edge tools while preserving the human element in art.</p>
        </section>
    </main>

    <footer>
        <div class="footer-content">
            <p>&copy; 2026 NocturneMelodies V2. All rights reserved.</p>
            <p>Enhanced for creativity and innovation.</p>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>"""

    with open(base_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

    print("Created enhanced NocturneMelodies V2 index.html file")


def create_enhanced_css_file(base_dir):
    """Create an enhanced CSS file for NocturneMelodies V2"""

    css_content = """/* Enhanced NocturneMelodies V2 Website Styles */
:root {
    --primary-color: #6e44ff;
    --secondary-color: #ff6b6b;
    --accent-color: #4ecdc4;
    --background-color: #f8f9fa;
    --text-color: #333333;
    --card-background: #ffffff;
    --border-color: #e0e0e0;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    --transition-speed: 0.3s;
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
    transition: color var(--transition-speed) ease;
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
    transition: transform var(--transition-speed) ease;
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

/* Enhanced UI Elements */
.button-primary {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background-color: var(--primary-color);
    color: white;
    text-decoration: none;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color var(--transition-speed) ease;
}

.button-primary:hover {
    background-color: #5a38cc;
}

.card-enhanced {
    background-color: var(--card-background);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: var(--shadow);
    transition: all var(--transition-speed) ease;
    margin-bottom: 1.5rem;
}

.card-enhanced:hover {
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    transform: translateY(-3px);
}

.grid-responsive {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
}
"""

    with open(base_dir / "css" / "style.css", "w", encoding="utf-8") as f:
        f.write(css_content)

    print("Created enhanced NocturneMelodies V2 CSS file")


def main_v2():
    print("Creating enhanced NocturneMelodies V2 HTML directory system...")

    # Create the enhanced directory structure
    base_dir = create_enhanced_nocturnemelodies_structure()

    # Create the enhanced pages
    print("Creating enhanced main index page...")
    create_enhanced_main_index_html(base_dir)

    print("Creating enhanced CSS file...")
    create_enhanced_css_file(base_dir)

    # Create enhanced JavaScript file
    js_content = """// Enhanced NocturneMelodies V2 JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Enhanced mobile menu functionality
    const menuToggle = document.createElement('button');
    menuToggle.innerHTML = '☰';
    menuToggle.className = 'menu-toggle';
    menuToggle.style.display = 'none'; // Will be shown on mobile via CSS

    // Enhanced search functionality
    setupEnhancedSearch();

    // Initialize enhanced interactive elements
    initializeEnhancedInteractiveElements();
});

function setupEnhancedSearch() {
    const searchInput = document.querySelector('.nav-search input');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performEnhancedSearch(searchInput.value);
            }
        });

        // Add search suggestions if available
        searchInput.addEventListener('input', function(e) {
            showSearchSuggestions(e.target.value);
        });
    }
}

function performEnhancedSearch(query) {
    // Placeholder for enhanced search functionality
    console.log('Enhanced search for:', query);
    alert('Enhanced search functionality would be implemented here');
}

function showSearchSuggestions(query) {
    // Placeholder for search suggestions
    console.log('Showing suggestions for:', query);
}

function initializeEnhancedInteractiveElements() {
    // Add enhanced interactive functionality
    console.log('Enhanced NocturneMelodies V2 website initialized');

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
}

// Enhanced audio player functionality (if needed)
function setupEnhancedAudioPlayer() {
    // Add enhanced audio player functionality if needed
    console.log('Enhanced audio player setup');
}
"""

    with open(base_dir / "js" / "main.js", "w", encoding="utf-8") as f:
        f.write(js_content)

    print("Created enhanced NocturneMelodies V2 JavaScript file")

    # Create a site map for V2
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://nocturnemelodies-v2.avatararts.org/</loc>
        <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://nocturnemelodies-v2.avatararts.org/music/</loc>
        <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://nocturnemelodies-v2.avatararts.org/lyrics/</loc>
        <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://nocturnemelodies-v2.avatararts.org/pages/artists/</loc>
        <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://nocturnemelodies-v2.avatararts.org/docs/</loc>
        <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>https://nocturnemelodies-v2.avatararts.org/gallery/</loc>
        <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
</urlset>"""

    with open(base_dir / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    # Create a robots.txt file for V2
    robots_content = """User-agent: *
Allow: /
Disallow: /private/
Disallow: /temp/
Disallow: /backup/

Sitemap: https://nocturnemelodies-v2.avatararts.org/sitemap.xml
"""

    with open(base_dir / "robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_content)

    # Create a summary file for V2
    summary_content = f"""# NocturneMelodies V2 Website Content Summary

## Enhanced Features
- Improved content categorization based on content analysis
- Enhanced UI with better responsive design
- Improved navigation and search capabilities
- More detailed organization structure

## Directory Structure
- /css - Enhanced stylesheets
- /js - Enhanced JavaScript files
- /images - Image assets
- /music - Music-related content (with subcategories)
- /lyrics - Lyrics and song content (organized by multiple criteria)
- /docs - Comprehensive documentation
- /pages - Static pages
- /assets - Media assets
- /data - Data files
- /gallery - Visual content gallery
- /seo - SEO optimization tools
- /automation - Automation tools and scripts
- /scripts - Utility scripts
- /logs - System logs
- /backup - Backup files

## Generated Files
- index.html - Enhanced landing page
- sitemap.xml - Site map for search engines
- robots.txt - Crawler directives
- css/style.css - Enhanced stylesheet
- js/main.js - Enhanced JavaScript file

## Improvements in V2
- Better content analysis for categorization
- Enhanced UI/UX design
- More granular organization structure
- Improved mobile responsiveness
- Enhanced search and navigation

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    with open(base_dir / "content_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_content)

    print("\nNocturneMelodies V2 HTML directory system created successfully!")
    print(f"Base directory: {base_dir}")
    print("Enhanced directory structure created with improved pages, CSS, JS, sitemap and robots.txt.")


if __name__ == "__main__":
    main_v2()

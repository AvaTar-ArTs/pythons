#!/usr/bin/env python3
"""
Simple File Organization Script
Migrates files to new structure without external dependencies
"""

import re
import shutil
from pathlib import Path


class SimpleFileOrganizer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.stats = {"files_moved": 0, "files_organized": 0, "errors": 0}

    def create_directories(self):
        """Create the new directory structure"""
        directories = [
            "music/final_versions",
            "music/demos",
            "music/remixes",
            "visuals/album_covers",
            "visuals/promotional",
            "visuals/raw_assets",
            "web/pages",
            "web/css",
            "web/js",
            "data/metadata",
            "data/analysis",
            "documentation",
            "scripts",
            "archive",
        ]

        for directory in directories:
            dir_path = self.base_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created directory: {directory}")

    def organize_audio_files(self):
        """Organize MP3 files by quality and version"""
        print("\n🎵 Organizing audio files...")

        # Find all MP3 files
        mp3_files = list(self.base_path.rglob("*.mp3"))
        print(f"Found {len(mp3_files)} MP3 files")

        for mp3_file in mp3_files:
            # Skip if already in organized structure
            if "music/" in str(mp3_file):
                continue

            filename = mp3_file.name.lower()

            # Determine category based on filename patterns
            if any(
                keyword in filename
                for keyword in ["remastered", "final", "master", "v4", "v5", "best"]
            ):
                target_dir = "music/final_versions"
            elif any(
                keyword in filename
                for keyword in ["demo", "draft", "test", "rough", "unfinished"]
            ):
                target_dir = "music/demos"
            elif any(
                keyword in filename
                for keyword in ["remix", "edit", "version", "alt", "mix"]
            ):
                target_dir = "music/remixes"
            else:
                target_dir = "music/final_versions"  # Default to final versions

            # Create clean filename
            clean_name = self.clean_filename(mp3_file.name)
            target_path = self.base_path / target_dir / clean_name

            try:
                shutil.move(str(mp3_file), str(target_path))
                self.stats["files_moved"] += 1
                print(f"  ✓ Moved: {mp3_file.name} -> {target_dir}")
            except Exception as e:
                print(f"  ✗ Error moving {mp3_file.name}: {e}")
                self.stats["errors"] += 1

    def organize_image_files(self):
        """Organize PNG files by category"""
        print("\n🖼️ Organizing image files...")

        # Find all PNG files
        png_files = list(self.base_path.rglob("*.png"))
        print(f"Found {len(png_files)} PNG files")

        for png_file in png_files:
            # Skip if already in organized structure
            if "visuals/" in str(png_file):
                continue

            filename = png_file.name.lower()

            # Determine category based on filename patterns
            if any(
                keyword in filename
                for keyword in ["cover", "album", "artwork", "poster", "main"]
            ):
                target_dir = "visuals/album_covers"
            elif any(
                keyword in filename
                for keyword in ["promo", "marketing", "social", "banner", "ad"]
            ):
                target_dir = "visuals/promotional"
            else:
                target_dir = "visuals/raw_assets"

            # Create clean filename
            clean_name = self.clean_filename(png_file.name)
            target_path = self.base_path / target_dir / clean_name

            try:
                shutil.move(str(png_file), str(target_path))
                self.stats["files_moved"] += 1
                print(f"  ✓ Moved: {png_file.name} -> {target_dir}")
            except Exception as e:
                print(f"  ✗ Error moving {png_file.name}: {e}")
                self.stats["errors"] += 1

    def organize_html_files(self):
        """Organize HTML files and identify essential ones"""
        print("\n🌐 Organizing HTML files...")

        # Find all HTML files
        html_files = list(self.base_path.rglob("*.html"))
        print(f"Found {len(html_files)} HTML files")

        # Essential HTML files to keep in main pages
        essential_files = [
            "index.html",
            "disco.html",
            "gindex.html",
            "preview.html",
            "main.html",
        ]

        for html_file in html_files:
            # Skip if already in organized structure
            if "web/" in str(html_file):
                continue

            filename = html_file.name.lower()

            # Check if it's an essential file
            if any(essential in filename for essential in essential_files):
                target_dir = "web/pages"
            else:
                # Move to archive for review
                target_dir = "web/pages/archive"

            # Create clean filename
            clean_name = self.clean_filename(html_file.name)
            target_path = self.base_path / target_dir / clean_name

            try:
                shutil.move(str(html_file), str(target_path))
                self.stats["files_moved"] += 1
                print(f"  ✓ Moved: {html_file.name} -> {target_dir}")
            except Exception as e:
                print(f"  ✗ Error moving {html_file.name}: {e}")
                self.stats["errors"] += 1

    def organize_data_files(self):
        """Organize CSV, JSON, and analysis files"""
        print("\n📊 Organizing data files...")

        # Move CSV files
        csv_files = list(self.base_path.rglob("*.csv"))
        print(f"Found {len(csv_files)} CSV files")
        for csv_file in csv_files:
            if "data/" not in str(csv_file):
                target_path = self.base_path / "data/metadata" / csv_file.name
                try:
                    shutil.move(str(csv_file), str(target_path))
                    self.stats["files_moved"] += 1
                    print(f"  ✓ Moved: {csv_file.name} -> data/metadata")
                except Exception as e:
                    print(f"  ✗ Error moving {csv_file.name}: {e}")
                    self.stats["errors"] += 1

        # Move JSON files
        json_files = list(self.base_path.rglob("*.json"))
        print(f"Found {len(json_files)} JSON files")
        for json_file in json_files:
            if "data/" not in str(json_file):
                target_path = self.base_path / "data/metadata" / json_file.name
                try:
                    shutil.move(str(json_file), str(target_path))
                    self.stats["files_moved"] += 1
                    print(f"  ✓ Moved: {json_file.name} -> data/metadata")
                except Exception as e:
                    print(f"  ✗ Error moving {json_file.name}: {e}")
                    self.stats["errors"] += 1

        # Move analysis files
        analysis_files = list(self.base_path.rglob("*analysis*"))
        print(f"Found {len(analysis_files)} analysis files")
        for analysis_file in analysis_files:
            if "data/" not in str(analysis_file):
                target_path = self.base_path / "data/analysis" / analysis_file.name
                try:
                    shutil.move(str(analysis_file), str(target_path))
                    self.stats["files_moved"] += 1
                    print(f"  ✓ Moved: {analysis_file.name} -> data/analysis")
                except Exception as e:
                    print(f"  ✗ Error moving {analysis_file.name}: {e}")
                    self.stats["errors"] += 1

    def organize_other_files(self):
        """Organize remaining files"""
        print("\n📁 Organizing other files...")

        # Move markdown files to documentation
        md_files = list(self.base_path.rglob("*.md"))
        for md_file in md_files:
            if "documentation/" not in str(md_file):
                target_path = self.base_path / "documentation" / md_file.name
                try:
                    shutil.move(str(md_file), str(target_path))
                    self.stats["files_moved"] += 1
                    print(f"  ✓ Moved: {md_file.name} -> documentation")
                except Exception as e:
                    print(f"  ✗ Error moving {md_file.name}: {e}")
                    self.stats["errors"] += 1

        # Move video files to archive
        video_files = list(self.base_path.rglob("*.mp4"))
        for video_file in video_files:
            target_path = self.base_path / "archive" / video_file.name
            try:
                shutil.move(str(video_file), str(target_path))
                self.stats["files_moved"] += 1
                print(f"  ✓ Moved: {video_file.name} -> archive")
            except Exception as e:
                print(f"  ✗ Error moving {video_file.name}: {e}")
                self.stats["errors"] += 1

    def clean_filename(self, filename):
        """Clean filename for better organization"""
        # Remove special characters and normalize
        clean = re.sub(r"[^\w\s-]", "", filename)
        clean = re.sub(r"[-\s]+", "-", clean)
        return clean.strip("-")

    def create_unified_web_interface(self):
        """Create a unified web interface"""
        print("\n🌐 Creating unified web interface...")

        # Main index page
        index_content = '\''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>nocTurneMeLoDieS - Indie Folk Visual Music Project</title>
    <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@200;300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/main.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-brand">
            <h1>🌙 nocTurneMeLoDieS</h1>
            <p>Indie Folk Visual Music Project</p>
        </div>
        <div class="nav-links">
            <a href="#music">Music</a>
            <a href="#visuals">Visuals</a>
            <a href="#stories">Stories</a>
            <a href="#about">About</a>
        </div>
    </nav>

    <main class="main-content">
        <section id="hero" class="hero-section">
            <div class="hero-content">
                <h2>Where Typography Dances with Shadows</h2>
                <p>Experience the journey from heartbreak to healing through indie-folk music and cinematic visual storytelling</p>
                <div class="hero-buttons">
                    <a href="#music" class="btn btn-primary">Explore Music</a>
                    <a href="#visuals" class="btn btn-secondary">View Visuals</a>
                </div>
            </div>
        </section>

        <section id="music" class="music-section">
            <h2>Musical Journey</h2>
            <div class="music-grid">
                <div class="music-card">
                    <h3>Willow Whispers</h3>
                    <p>Ethereal folk journey through moonlit healing</p>
                    <a href="pages/willow-whispers.html" class="btn">Listen</a>
                </div>
                <div class="music-card">
                    <h3>Love is Rubbish</h3>
                    <p>Punk raccoon's anti-valentine rebellion</p>
                    <a href="pages/love-is-rubbish.html" class="btn">Listen</a>
                </div>
                <div class="music-card">
                    <h3>Dark Traveler</h3>
                    <p>Mystical folk journey through midnight crossroads</p>
                    <a href="pages/dark-traveler.html" class="btn">Listen</a>
                </div>
            </div>
        </section>

        <section id="visuals" class="visuals-section">
            <h2>Visual Storytelling</h2>
            <div class="visuals-grid">
                <div class="visual-card">
                    <h3>Nature Series</h3>
                    <p>Ethereal moonlight and mystical willow imagery</p>
                </div>
                <div class="visual-card">
                    <h3>Urban Series</h3>
                    <p>Neon graffiti and punk rebellion aesthetics</p>
                </div>
                <div class="visual-card">
                    <h3>Blues Series</h3>
                    <p>Intimate moonlit scenes and emotional depth</p>
                </div>
            </div>
        </section>

        <section id="stories" class="stories-section">
            <h2>Narrative Themes</h2>
            <div class="themes-grid">
                <div class="theme-card">
                    <h3>Nature Sanctuary</h3>
                    <p>Healing through ancient willow wisdom</p>
                </div>
                <div class="theme-card">
                    <h3>Urban Rebellion</h3>
                    <p>Anti-establishment punk authenticity</p>
                </div>
                <div class="theme-card">
                    <h3>Mystical Journey</h3>
                    <p>Self-discovery through wandering</p>
                </div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <p>&copy; 2025 nocTurneMeLoDieS. All rights reserved.</p>
        <p>Where typography dances with shadows, and music heals the broken heart.</p>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>"""

        # Write main index
        with open(self.base_path / "web/pages/index.html", "w") as f:
            f.write(index_content)

        # Create CSS file
        css_content = """/* Main CSS for nocTurneMeLoDieS */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Oswald', sans-serif;
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    color: #ffffff;
    line-height: 1.6;
}

.navbar {
    background: rgba(0, 0, 0, 0.9);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
}

.nav-brand h1 {
    font-size: 1.8rem;
    color: #ff6b6b;
}

.nav-brand p {
    font-size: 0.9rem;
    color: #cccccc;
}

.nav-links {
    display: flex;
    gap: 2rem;
}

.nav-links a {
    color: #ffffff;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: #ff6b6b;
}

.main-content {
    margin-top: 80px;
}

.hero-section {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5));
    background-size: cover;
    background-position: center;
}

.hero-content h2 {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: #ff6b6b;
}

.hero-content p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    color: #cccccc;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
}

.btn {
    padding: 12px 24px;
    border: none;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s;
    display: inline-block;
}

.btn-primary {
    background: #ff6b6b;
    color: white;
}

.btn-primary:hover {
    background: #ff5252;
    transform: translateY(-2px);
}

.btn-secondary {
    background: transparent;
    color: #ff6b6b;
    border: 2px solid #ff6b6b;
}

.btn-secondary:hover {
    background: #ff6b6b;
    color: white;
}

.music-section, .visuals-section, .stories-section {
    padding: 4rem 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.music-section h2, .visuals-section h2, .stories-section h2 {
    font-size: 2.5rem;
    text-align: center;
    margin-bottom: 3rem;
    color: #ff6b6b;
}

.music-grid, .visuals-grid, .themes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.music-card, .visual-card, .theme-card {
    background: rgba(255, 255, 255, 0.1);
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    transition: transform 0.3s;
}

.music-card:hover, .visual-card:hover, .theme-card:hover {
    transform: translateY(-5px);
}

.music-card h3, .visual-card h3, .theme-card h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #ff6b6b;
}

.footer {
    background: #000000;
    padding: 2rem;
    text-align: center;
    color: #cccccc;
}

    .hero-content h2 {
        font-size: 2rem;
    }
    
    .nav-links {
        display: none;
    }
    
    .music-grid, .visuals-grid, .themes-grid {
        grid-template-columns: 1fr;
    }
}"""

        # Write CSS
        with open(self.base_path / "web/css/main.css", "w") as f:
            f.write(css_content)

        # Create JavaScript file
        js_content = """// Main JavaScript for nocTurneMeLoDieS
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add scroll effect to navbar
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(0, 0, 0, 0.95)';
        } else {
            navbar.style.background = 'rgba(0, 0, 0, 0.9)';
        }
    });
    
    // Add animation to cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    const cards = document.querySelectorAll('.music-card, .visual-card, .theme-card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s, transform 0.6s';
        observer.observe(card);
    });
});"""

        # Write JavaScript
        with open(self.base_path / "web/js/main.js", "w") as f:
            f.write(js_content)

        print("  ✓ Created unified web interface")

    def run_optimization(self):
        """Run the complete optimization process'\''
        print("🚀 Starting comprehensive file organization and optimization...")
        print("=" * 60)

        # Create directories
        self.create_directories()

        # Organize files
        self.organize_audio_files()
        self.organize_image_files()
        self.organize_html_files()
        self.organize_data_files()
        self.organize_other_files()

        # Create web interface
        self.create_unified_web_interface()

        # Print statistics
        print("\n" + "=" * 60)
        print("🎉 OPTIMIZATION COMPLETE!")
        print("=" * 60)
        print(f"📁 Files moved: {self.stats['files_moved']}")
        print(f"📊 Files organized: {self.stats['files_organized']}")
        print(f"❌ Errors: {self.stats['errors']}")
        print("=" * 60)
        print("✅ Project structure optimized!")
        print("✅ Web interface created!")
        print("✅ Files organized by category!")
        print("✅ Ready for production!")


def main():
    base_path = "/Users/steven/Music/nocTurneMeLoDieS"
    organizer = SimpleFileOrganizer(base_path)
    organizer.run_optimization()


if __name__ == "__main__":
    main()

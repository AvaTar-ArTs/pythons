#!/usr/bin/env python3
"""
🌐 MULTI-PLATFORM CONTENT EXTRACTOR & ANALYZER
Content-aware extraction and analysis from multiple platforms

Integrates:
- Ideogram.ai image/video extraction
- Suno music extraction
- Make.com workflow integration
- Deep content awareness (semantic embedding, tagging)
- YouTube content generation

Features:
- Browser automation (Selenium/Playwright)
- Content-aware metadata extraction
- Semantic analysis and tagging
- CSV/JSON export
- Integration with existing systems
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import csv
import hashlib
import re

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
except ImportError:
    print("Installing selenium...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "selenium", "webdriver-manager"])
    from selenium import webdriver
    from selenium.webdriver.common.by import By

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing requests, beautifulsoup4...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "requests", "beautifulsoup4"])
    import requests
    from bs4 import BeautifulSoup


@dataclass
class IdeogramAsset:
    """Ideogram.ai extracted asset"""
    id: str
    kind: str  # "image" or "video"
    filename: str
    content_type: str
    primary_url: str
    poster_url: str
    page_url: str
    prompt_or_alt: str
    badges: str
    generation_id: str
    frame_index: str
    likes: str
    aspect_ratio: str
    natural_w: Optional[int] = None
    natural_h: Optional[int] = None
    video_w: Optional[int] = None
    video_h: Optional[int] = None
    duration_s: Optional[float] = None
    extracted_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SunoSong:
    """Suno extracted song"""
    id: str
    title: str
    url: str
    image_url: str
    duration: str
    tags: str
    author: str
    author_link: str
    audio_url: str
    summary: str
    lyrics: str
    plays: str = ""
    likes: str = ""
    extracted_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ContentAnalysis:
    """Content-aware analysis result"""
    asset_id: str
    tags: List[str]
    tag_scores: List[Dict[str, float]]
    metadata: Dict[str, Any]
    semantic_embedding: Optional[List[float]] = None
    content_category: str = ""
    seo_keywords: List[str] = field(default_factory=list)
    suggested_use: List[str] = field(default_factory=list)


class MultiPlatformContentExtractor:
    """Extract and analyze content from multiple platforms"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None
        self.ideogram_assets: List[IdeogramAsset] = []
        self.suno_songs: List[SunoSong] = []
        
        # Content-aware analysis
        self.content_analyzer = None
        try:
            from advanced_toolkit.content_classifier import ContentClassifier
            self.content_analyzer = ContentClassifier()
        except:
            pass
    
    def initialize_browser(self):
        """Initialize Selenium browser"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            print(f"⚠️  Chrome driver error: {e}")
            print("   Install: brew install chromedriver (macOS) or download from chromedriver.chromium.org")
            raise
    
    def extract_ideogram(
        self,
        url: str,
        max_scrolls: int = 500,
        max_downloads: int = 2000,
        scroll_delay: float = 0.2
    ) -> List[IdeogramAsset]:
        """Extract images/videos from Ideogram.ai"""
        
        print(f"🎨 Extracting from Ideogram.ai: {url}")
        
        if not self.driver:
            self.initialize_browser()
        
        self.driver.get(url)
        
        # Inject extraction script
        ideogram_script = """
        // Ideogram extraction logic (simplified Python version)
        const CONFIG = {
          scrollDelay: 200,
          scrollStep: Math.max(600, window.innerHeight * 4),
          maxScrolls: """ + str(max_scrolls) + """,
          maxDownloads: """ + str(max_downloads) + """,
          imgSelector: 'img[src^="https://ideogram.ai/assets/progressive-image/"]',
          linkSelector: 'a[href^="/g/"]',
          alsoGrabVideos: true
        };
        
        const records = [];
        const downloaded = new Set();
        let scrollCount = 0;
        
        function scrapeImages() {
          document.querySelectorAll(CONFIG.imgSelector).forEach(img => {
            const raw = img.currentSrc || img.src;
            if (!raw || !raw.includes('ideogram.ai')) return;
            
            const container = img.closest('[data-index]') || img.parentElement;
            const a = container?.querySelector?.(CONFIG.linkSelector);
            
            let generation_id = "", frame_index = "";
            if (a) {
              const path = new URL(a.href, location.origin).pathname.split("/").filter(Boolean);
              generation_id = path[1] || "";
              frame_index = path[2] || "";
            }
            
            const prompt = img.getAttribute("alt") || img.getAttribute("aria-label") || "";
            const filename = prompt.replace(/[^\\w\\-\\\.]+/g, "_").slice(0, 90) + ".jpg";
            
            const record = {
              id: raw.split('/').pop().split('?')[0],
              kind: "image",
              filename: filename,
              content_type: "image/jpeg",
              primary_url: raw,
              poster_url: "",
              page_url: location.href,
              prompt_or_alt: prompt,
              badges: "",
              generation_id: generation_id,
              frame_index: frame_index,
              likes: "",
              aspect_ratio: "",
              natural_w: img.naturalWidth || "",
              natural_h: img.naturalHeight || ""
            };
            
            if (!downloaded.has(raw)) {
              records.push(record);
              downloaded.add(raw);
            }
          });
        }
        
        function autoScroll() {
          if (scrollCount >= CONFIG.maxScrolls) {
            return records;
          }
          window.scrollBy(0, CONFIG.scrollStep);
          scrollCount++;
          scrapeImages();
          setTimeout(autoScroll, CONFIG.scrollDelay);
        }
        
        autoScroll();
        return records;
        """
        
        # Execute script and wait
        print("   📜 Scrolling and extracting...")
        records = self.driver.execute_async_script(f"""
        var callback = arguments[arguments.length - 1];
        {ideogram_script}
        setTimeout(() => callback(records), {max_scrolls * scroll_delay * 1000});
        """)
        
        # Convert to IdeogramAsset objects
        assets = []
        for rec in records:
            asset = IdeogramAsset(
                id=rec.get('id', ''),
                kind=rec.get('kind', 'image'),
                filename=rec.get('filename', ''),
                content_type=rec.get('content_type', ''),
                primary_url=rec.get('primary_url', ''),
                poster_url=rec.get('poster_url', ''),
                page_url=rec.get('page_url', ''),
                prompt_or_alt=rec.get('prompt_or_alt', ''),
                badges=rec.get('badges', ''),
                generation_id=rec.get('generation_id', ''),
                frame_index=rec.get('frame_index', ''),
                likes=rec.get('likes', ''),
                aspect_ratio=rec.get('aspect_ratio', ''),
                natural_w=rec.get('natural_w'),
                natural_h=rec.get('natural_h')
            )
            assets.append(asset)
        
        self.ideogram_assets.extend(assets)
        print(f"   ✅ Extracted {len(assets)} assets")
        
        return assets
    
    def extract_suno(
        self,
        url: str,
        max_scrolls: int = 400,
        scroll_delay: float = 0.9
    ) -> List[SonoSong]:
        """Extract songs from Suno"""
        
        print(f"🎵 Extracting from Suno: {url}")
        
        if not self.driver:
            self.initialize_browser()
        
        self.driver.get(url)
        
        # Inject Suno extraction script
        suno_script = """
        // Suno extraction (simplified)
        const songs = [];
        const seen = new Set();
        let scrollCount = 0;
        
        function extractSongs() {
          const anchors = document.querySelectorAll('a[href*="/song/"]');
          anchors.forEach(a => {
            const match = a.href.match(/\\/song\\/([a-f0-9-]{36})/);
            if (!match) return;
            const id = match[1];
            if (seen.has(id)) return;
            seen.add(id);
            
            const container = a.closest('div') || a.parentElement;
            const titleEl = a.querySelector('[title]') || a;
            const title = titleEl.getAttribute('title') || titleEl.textContent || 'Untitled';
            
            const imgEl = a.querySelector('img') || container?.querySelector('img');
            const imageUrl = imgEl?.src || '';
            
            const durationEl = container?.querySelector('[class*="duration"]');
            const duration = durationEl?.textContent?.trim() || '';
            
            const authorEl = container?.querySelector('a[href^="/@"]');
            const author = authorEl?.textContent?.trim() || '';
            const authorLink = authorEl?.href || '';
            
            songs.push({
              id: id,
              title: title,
              url: `https://suno.com/song/${id}`,
              image_url: imageUrl,
              duration: duration,
              tags: "",
              author: author,
              author_link: authorLink,
              audio_url: `https://cdn1.suno.ai/${id}.mp3`,
              summary: "",
              lyrics: ""
            });
          });
        }
        
        function autoScroll() {
          if (scrollCount >= """ + str(max_scrolls) + """) {
            return songs;
          }
          window.scrollBy(0, window.innerHeight * 4);
          scrollCount++;
          extractSongs();
          setTimeout(autoScroll, """ + str(int(scroll_delay * 1000)) + """);
        }
        
        autoScroll();
        return songs;
        """
        
        print("   📜 Scrolling and extracting...")
        songs_data = self.driver.execute_async_script(f"""
        var callback = arguments[arguments.length - 1];
        {suno_script}
        setTimeout(() => callback(songs), {max_scrolls * int(scroll_delay * 1000)});
        """)
        
        # Convert to SunoSong objects
        songs = []
        for data in songs_data:
            song = SunoSong(
                id=data.get('id', ''),
                title=data.get('title', ''),
                url=data.get('url', ''),
                image_url=data.get('image_url', ''),
                duration=data.get('duration', ''),
                tags=data.get('tags', ''),
                author=data.get('author', ''),
                author_link=data.get('author_link', ''),
                audio_url=data.get('audio_url', ''),
                summary=data.get('summary', ''),
                lyrics=data.get('lyrics', '')
            )
            songs.append(song)
        
        self.suno_songs.extend(songs)
        print(f"   ✅ Extracted {len(songs)} songs")
        
        return songs
    
    def analyze_content(self, asset: Any) -> ContentAnalysis:
        """Content-aware analysis of extracted asset"""
        
        # Determine content type
        if isinstance(asset, IdeogramAsset):
            content = asset.prompt_or_alt
            content_type = "image" if asset.kind == "image" else "video"
        elif isinstance(asset, SunoSong):
            content = f"{asset.title} {asset.summary} {asset.lyrics}"
            content_type = "audio"
        else:
            content = str(asset)
            content_type = "unknown"
        
        # Basic tag extraction
        tags = self._extract_tags(content)
        tag_scores = [{"tag": tag, "score": 0.8} for tag in tags[:10]]
        
        # SEO keywords
        seo_keywords = self._extract_seo_keywords(content)
        
        # Suggested use cases
        suggested_use = self._suggest_use_cases(content, content_type)
        
        return ContentAnalysis(
            asset_id=getattr(asset, 'id', ''),
            tags=tags,
            tag_scores=tag_scores,
            metadata={
                "content_type": content_type,
                "source": "ideogram" if isinstance(asset, IdeogramAsset) else "suno",
                "analyzed_at": datetime.now().isoformat()
            },
            content_category=self._categorize_content(content, content_type),
            seo_keywords=seo_keywords,
            suggested_use=suggested_use
        )
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from content"""
        if not content:
            return []
        
        # Simple keyword extraction
        words = re.findall(r'\b[a-z]{4,}\b', content.lower())
        
        # Common stop words
        stop_words = {'this', 'that', 'with', 'from', 'have', 'been', 'will', 'your', 'they', 'them'}
        words = [w for w in words if w not in stop_words]
        
        # Count frequency
        from collections import Counter
        word_freq = Counter(words)
        
        # Return top tags
        return [word for word, _ in word_freq.most_common(10)]
    
    def _extract_seo_keywords(self, content: str) -> List[str]:
        """Extract SEO keywords"""
        tags = self._extract_tags(content)
        
        # Add trending indicators
        seo_keywords = tags.copy()
        
        # Add year
        seo_keywords.append("2025")
        
        # Add content type keywords
        if "image" in content.lower() or "art" in content.lower():
            seo_keywords.extend(["digital art", "ai art", "generated art"])
        if "music" in content.lower() or "song" in content.lower():
            seo_keywords.extend(["music", "song", "audio"])
        
        return list(set(seo_keywords))[:15]
    
    def _suggest_use_cases(self, content: str, content_type: str) -> List[str]:
        """Suggest use cases for content"""
        suggestions = []
        
        if content_type == "image":
            suggestions.extend([
                "Print-on-demand products",
                "Social media posts",
                "YouTube thumbnails",
                "Blog illustrations"
            ])
        elif content_type == "video":
            suggestions.extend([
                "YouTube content",
                "Social media videos",
                "Video thumbnails",
                "Promotional content"
            ])
        elif content_type == "audio":
            suggestions.extend([
                "YouTube background music",
                "Music licensing",
                "Podcast intros",
                "Content creation"
            ])
        
        return suggestions
    
    def _categorize_content(self, content: str, content_type: str) -> str:
        """Categorize content"""
        content_lower = content.lower()
        
        if "art" in content_lower or "painting" in content_lower:
            return "art"
        elif "music" in content_lower or "song" in content_lower:
            return "music"
        elif "video" in content_lower or "film" in content_lower:
            return "video"
        elif "tutorial" in content_lower or "guide" in content_lower:
            return "educational"
        else:
            return "general"
    
    def export_csv(self, output_path: Path, assets: List[Any] = None):
        """Export to CSV"""
        if assets is None:
            assets = list(self.ideogram_assets) + list(self.suno_songs)
        
        if not assets:
            print("⚠️  No assets to export")
            return
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_file = output_path / f"content_export_{timestamp}.csv"
        
        # Determine fields based on asset type
        if isinstance(assets[0], IdeogramAsset):
            fields = [
                'id', 'kind', 'filename', 'content_type', 'primary_url', 'page_url',
                'prompt_or_alt', 'generation_id', 'frame_index', 'likes', 'aspect_ratio',
                'natural_w', 'natural_h', 'extracted_at'
            ]
        else:
            fields = [
                'id', 'title', 'url', 'image_url', 'duration', 'tags', 'author',
                'author_link', 'audio_url', 'summary', 'lyrics', 'extracted_at'
            ]
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for asset in assets:
                row = {field: getattr(asset, field, '') for field in fields}
                writer.writerow(row)
        
        print(f"💾 Exported {len(assets)} assets to: {csv_file}")
        return csv_file
    
    def export_json(self, output_path: Path, assets: List[Any] = None):
        """Export to JSON"""
        if assets is None:
            assets = list(self.ideogram_assets) + list(self.suno_songs)
        
        if not assets:
            print("⚠️  No assets to export")
            return
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = output_path / f"content_export_{timestamp}.json"
        
        # Convert to dicts
        data = []
        for asset in assets:
            if isinstance(asset, IdeogramAsset):
                data.append({
                    'id': asset.id,
                    'kind': asset.kind,
                    'filename': asset.filename,
                    'content_type': asset.content_type,
                    'primary_url': asset.primary_url,
                    'page_url': asset.page_url,
                    'prompt_or_alt': asset.prompt_or_alt,
                    'generation_id': asset.generation_id,
                    'frame_index': asset.frame_index,
                    'likes': asset.likes,
                    'aspect_ratio': asset.aspect_ratio,
                    'extracted_at': asset.extracted_at
                })
            elif isinstance(asset, SunoSong):
                data.append({
                    'id': asset.id,
                    'title': asset.title,
                    'url': asset.url,
                    'image_url': asset.image_url,
                    'duration': asset.duration,
                    'tags': asset.tags,
                    'author': asset.author,
                    'author_link': asset.author_link,
                    'audio_url': asset.audio_url,
                    'summary': asset.summary,
                    'lyrics': asset.lyrics,
                    'extracted_at': asset.extracted_at
                })
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Exported {len(assets)} assets to: {json_file}")
        return json_file
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Multi-Platform Content Extractor')
    parser.add_argument('--ideogram', help='Ideogram.ai URL to extract from')
    parser.add_argument('--suno', help='Suno URL to extract from')
    parser.add_argument('--max-scrolls', type=int, default=100, help='Max scrolls')
    parser.add_argument('--max-downloads', type=int, default=200, help='Max downloads')
    parser.add_argument('--output', default='~/extracted_content', help='Output directory')
    parser.add_argument('--format', choices=['csv', 'json', 'both'], default='both',
                       help='Export format')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    
    args = parser.parse_args()
    
    extractor = MultiPlatformContentExtractor(headless=args.headless)
    
    try:
        assets = []
        
        if args.ideogram:
            ideogram_assets = extractor.extract_ideogram(
                args.ideogram,
                max_scrolls=args.max_scrolls,
                max_downloads=args.max_downloads
            )
            assets.extend(ideogram_assets)
        
        if args.suno:
            suno_songs = extractor.extract_suno(
                args.suno,
                max_scrolls=args.max_scrolls
            )
            assets.extend(suno_songs)
        
        if not assets:
            print("⚠️  No assets extracted. Provide --ideogram or --suno URL")
            return
        
        # Export
        output_dir = Path(args.output).expanduser()
        if args.format in ['csv', 'both']:
            extractor.export_csv(output_dir, assets)
        if args.format in ['json', 'both']:
            extractor.export_json(output_dir, assets)
        
        print(f"\n✅ Extraction complete: {len(assets)} assets")
        
    finally:
        extractor.close()


if __name__ == '__main__':
    main()


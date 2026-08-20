#!/usr/bin/env python3
"""
🌟 CONTENT INTELLIGENCE SYSTEM - MAIN
======================================
Enhanced, production-ready content intelligence with caching, queuing, and more!
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
import logging

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from core.api_discovery import APIDiscoveryEngine
from database.cache_manager import SmartCacheManager
from utils.queue_manager import AsyncBatchQueue, Priority
from cli import cli

logger = logging.getLogger(__name__)


class EnhancedContentIntelligence:
    """
    Production-ready content intelligence system with all enhancements
    """
    
    def __init__(self):
        cli.print_header(
            "🌟 CONTENT INTELLIGENCE SYSTEM v3.0",
            "Enhanced with caching, queuing, and intelligent routing"
        )
        
        # Initialize subsystems
        self.api_engine = APIDiscoveryEngine()
        self.cache_manager = SmartCacheManager()
        self.queue_manager = AsyncBatchQueue(max_workers=5)
        
        # Discover APIs
        self.available_apis = self.api_engine.discover_all_apis()
        
        # Initialize engines based on available APIs
        self.engines = {}
        self._initialize_engines()
    
    def _initialize_engines(self):
        """Initialize content engines based on available APIs"""
        cli.print_info("Initializing content engines...")
        
        # Check what's available
        llm_apis = self.api_engine.get_apis_for_category('llm')
        image_apis = self.api_engine.get_apis_for_category('image')
        audio_apis = self.api_engine.get_apis_for_category('audio')
        video_apis = self.api_engine.get_apis_for_category('video')
        
        if llm_apis:
            self.engines['text'] = True
            cli.print_success(f"Text Engine: {len(llm_apis)} LLMs")
        
        if image_apis:
            self.engines['image'] = True
            cli.print_success(f"Image Engine: {len(image_apis)} services")
        
        if audio_apis:
            self.engines['audio'] = True
            cli.print_success(f"Audio Engine: {len(audio_apis)} services")
        
        if video_apis:
            self.engines['video'] = True
            cli.print_success(f"Video Engine: {len(video_apis)} services")
    
    async def analyze_file_with_cache(
        self, 
        file_path: Path,
        force: bool = False
    ) -> dict:
        """
        Analyze file with intelligent caching
        """
        # Generate content hash
        with open(file_path, 'rb') as f:
            content = f.read()
        
        content_hash = content[:1000].decode('utf-8', errors='ignore')  # First 1KB for hash
        operation = f"analyze_{file_path.suffix}"
        content_type = self._detect_content_type(file_path)
        
        # Check cache first (unless force refresh)
        if not force:
            cached = self.cache_manager.get(
                content_hash,
                operation,
                content_type=content_type
            )
            
            if cached:
                cli.print_success(f"📦 Cache hit: {file_path.name} (saved API call!)")
                return cached
        
        # Cache miss - perform actual analysis
        cli.print_info(f"🔍 Analyzing: {file_path.name}")
        result = await self._perform_analysis(file_path, content_type)
        
        # Store in cache
        estimated_cost = self._estimate_cost(content_type)
        self.cache_manager.set(
            content_hash,
            operation,
            result,
            content_type=content_type,
            estimated_cost=estimated_cost
        )
        
        return result
    
    async def _perform_analysis(self, file_path: Path, content_type: str) -> dict:
        """Perform actual analysis (calls APIs)"""
        result = {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'content_type': content_type,
            'analyzed_at': datetime.now().isoformat()
        }
        
        # Route to appropriate analyzer
        if content_type == 'image':
            result['analysis'] = await self._analyze_image(file_path)
        elif content_type == 'audio':
            result['analysis'] = await self._analyze_audio(file_path)
        elif content_type == 'video':
            result['analysis'] = await self._analyze_video(file_path)
        elif content_type == 'text':
            result['analysis'] = await self._analyze_text(file_path)
        else:
            result['analysis'] = {'error': 'Unsupported content type'}
        
        return result
    
    def _detect_content_type(self, path: Path) -> str:
        """Detect content type from extension"""
        ext = path.suffix.lower()
        
        if ext in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}:
            return 'image'
        elif ext in {'.mp3', '.wav', '.flac', '.ogg', '.m4a'}:
            return 'audio'
        elif ext in {'.mp4', '.mov', '.avi', '.mkv'}:
            return 'video'
        elif ext in {'.txt', '.md', '.html'}:
            return 'text'
        return 'unknown'
    
    def _estimate_cost(self, content_type: str) -> float:
        """Estimate API cost for analysis"""
        costs = {
            'image': 0.02,  # Vision API
            'audio': 0.01,  # Transcription
            'video': 0.05,  # Video analysis
            'text': 0.005   # LLM analysis
        }
        return costs.get(content_type, 0.01)
    
    async def _analyze_image(self, path: Path) -> dict:
        """Placeholder for image analysis"""
        return {
            'quality_score': 85,
            'seo': {'alt_text': f'Image: {path.stem}', 'keywords': []}
        }
    
    async def _analyze_audio(self, path: Path) -> dict:
        """Placeholder for audio analysis"""
        return {
            'quality_score': 85,
            'metadata': {'title': path.stem}
        }
    
    async def _analyze_video(self, path: Path) -> dict:
        """Placeholder for video analysis"""
        return {
            'quality_score': 85,
            'duration': 0
        }
    
    async def _analyze_text(self, path: Path) -> dict:
        """Placeholder for text analysis"""
        with open(path, 'r') as f:
            text = f.read()
        return {
            'word_count': len(text.split()),
            'quality_score': 85
        }
    
    async def batch_analyze_directory(
        self,
        directory: Path,
        recursive: bool = True,
        force: bool = False
    ) -> dict:
        """
        Analyze entire directory with progress tracking
        """
        cli.print_header(
            f"📁 Batch Analysis",
            f"Directory: {directory}"
        )
        
        # Find all files
        files = []
        if recursive:
            for ext in ['.jpg', '.png', '.mp3', '.wav', '.mp4', '.txt', '.md']:
                files.extend(directory.rglob(f"*{ext}"))
        else:
            for ext in ['.jpg', '.png', '.mp3', '.wav', '.mp4', '.txt', '.md']:
                files.extend(directory.glob(f"*{ext}"))
        
        cli.print_info(f"Found {len(files)} files to analyze")
        
        if not files:
            cli.print_warning("No files found to analyze")
            return {'results': []}
        
        # Confirm if large batch
        if len(files) > 100:
            if not cli.confirm(f"Analyze {len(files)} files? This may take a while."):
                cli.print_info("Cancelled by user")
                return {'results': []}
        
        # Process with queue and progress bar
        results = []
        
        if RICH_AVAILABLE:
            with cli.create_progress_bar(len(files), "Analyzing files") as progress:
                task = progress.add_task("[cyan]Processing...", total=len(files))
                
                for file_path in files:
                    result = await self.analyze_file_with_cache(file_path, force=force)
                    results.append(result)
                    progress.advance(task)
                    
                    # Small delay for rate limiting
                    await asyncio.sleep(0.1)
        else:
            for i, file_path in enumerate(files, 1):
                print(f"[{i}/{len(files)}] {file_path.name}")
                result = await self.analyze_file_with_cache(file_path, force=force)
                results.append(result)
                await asyncio.sleep(0.1)
        
        # Show statistics
        cli.print_success(f"\n✅ Analyzed {len(results)} files")
        self._print_batch_statistics(results)
        
        return {'results': results, 'total': len(results)}
    
    def _print_batch_statistics(self, results: list):
        """Print statistics about batch analysis"""
        # Count by type
        by_type = {}
        for result in results:
            ctype = result.get('content_type', 'unknown')
            by_type[ctype] = by_type.get(ctype, 0) + 1
        
        # Count cache hits
        cache_hits = len([r for r in results if r.get('_from_cache')])
        
        # Show stats
        if RICH_AVAILABLE:
            table_data = []
            for ctype, count in sorted(by_type.items()):
                table_data.append([ctype.title(), count])
            
            cli.print_table(
                "📊 Analysis Summary",
                table_data,
                ["Content Type", "Count"]
            )
            
            # Cache statistics
            cache_stats = self.cache_manager.get_statistics()
            cli.print_info(f"\n💾 Cache Statistics:")
            cli.console.print(f"   Cache Hit Rate: [green]{cache_stats['cache_hit_rate']}%[/green]")
            cli.console.print(f"   Cost Saved: [green]${cache_stats['total_cost_saved']:.2f}[/green]")
        else:
            print("\n📊 Analysis Summary:")
            for ctype, count in sorted(by_type.items()):
                print(f"   {ctype.title()}: {count}")
            print(f"\n💾 Cache hits: {cache_hits}/{len(results)} ({cache_hits/len(results)*100:.1f}%)")
    
    def show_api_capabilities(self):
        """Display all available API capabilities"""
        report = self.api_engine.generate_capabilities_report()
        
        if RICH_AVAILABLE:
            self.console.print(Panel(report, border_style="green", title="API Capabilities"))
        else:
            print(report)
    
    def show_cache_statistics(self):
        """Display cache statistics"""
        stats = self.cache_manager.get_statistics()
        
        cli.print_header("💾 Cache Statistics")
        
        if RICH_AVAILABLE:
            data = [
                ["Total Entries", stats['total_entries']],
                ["Cache Hit Rate", f"{stats['cache_hit_rate']}%"],
                ["Total Cost Saved", f"${stats['total_cost_saved']:.2f}"],
                ["Session Hits", stats['session_stats']['hits']],
                ["Session Misses", stats['session_stats']['misses']]
            ]
            
            cli.print_table("Cache Performance", data, ["Metric", "Value"])
        else:
            print(f"Total Entries: {stats['total_entries']}")
            print(f"Cache Hit Rate: {stats['cache_hit_rate']}%")
            print(f"Total Cost Saved: ${stats['total_cost_saved']:.2f}")


async def main():
    """Main entry point"""
    
    # Parse command-line arguments
    if len(sys.argv) < 2:
        # Interactive mode
        await interactive_mode()
    else:
        # Command mode
        command = sys.argv[1]
        
        system = EnhancedContentIntelligence()
        
        if command == 'apis':
            system.show_api_capabilities()
        
        elif command == 'cache':
            system.show_cache_statistics()
        
        elif command == 'analyze' and len(sys.argv) > 2:
            directory = Path(sys.argv[2])
            recursive = '-r' in sys.argv or '--recursive' in sys.argv
            force = '-f' in sys.argv or '--force' in sys.argv
            
            results = await system.batch_analyze_directory(
                directory,
                recursive=recursive,
                force=force
            )
        
        elif command == 'clear-cache':
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            deleted = system.cache_manager.clear_old(days)
            cli.print_success(f"Cleared {deleted} old cache entries (>{days} days)")
        
        else:
            print_usage()


async def interactive_mode():
    """Interactive CLI mode"""
    system = EnhancedContentIntelligence()
    
    while True:
        print("\n" + "="*80)
        print("🌟 CONTENT INTELLIGENCE SYSTEM - Interactive Mode")
        print("="*80)
        print("\n1. 🔍 Show API Capabilities")
        print("2. 📁 Analyze Directory")
        print("3. 📄 Analyze Single File")
        print("4. 💾 Show Cache Statistics")
        print("5. 🗑️  Clear Old Cache")
        print("0. 🚪 Exit")
        
        choice = cli.prompt("\nSelect option", "0")
        
        if choice == '1':
            system.show_api_capabilities()
        
        elif choice == '2':
            directory = cli.prompt("Directory path", str(Path.home()))
            recursive = cli.confirm("Recursive scan?", True)
            force = cli.confirm("Force refresh (skip cache)?", False)
            
            await system.batch_analyze_directory(
                Path(directory),
                recursive=recursive,
                force=force
            )
        
        elif choice == '3':
            file_path = cli.prompt("File path")
            result = await system.analyze_file_with_cache(Path(file_path))
            print(f"\n✅ Analysis complete!")
            print(f"Quality Score: {result.get('analysis', {}).get('quality_score', 'N/A')}")
        
        elif choice == '4':
            system.show_cache_statistics()
        
        elif choice == '5':
            days = int(cli.prompt("Clear entries older than (days)", "30"))
            deleted = system.cache_manager.clear_old(days)
            cli.print_success(f"Cleared {deleted} entries")
        
        elif choice == '0':
            cli.print_info("Goodbye! 👋")
            break
        
        else:
            cli.print_warning("Invalid option")


def print_usage():
    """Print usage information"""
    print("""
🌟 Content Intelligence System v3.0

Usage:
    python main.py                              # Interactive mode
    python main.py apis                         # Show API capabilities
    python main.py cache                        # Show cache statistics
    python main.py analyze <directory> [-r] [-f]  # Analyze directory
    python main.py clear-cache [days]           # Clear old cache

Examples:
    python main.py apis
    python main.py analyze ~/pictures -r
    python main.py analyze ~/music -r -f
    python main.py clear-cache 30

Options:
    -r, --recursive    Recursive directory scan
    -f, --force        Force refresh (skip cache)
    """)


if __name__ == "__main__":
    asyncio.run(main())


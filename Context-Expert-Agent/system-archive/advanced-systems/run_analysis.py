#!/usr/bin/env python3
"""
Deep Research Tool - Main Analysis Script
Run comprehensive folder analysis with GitHub and codex optimization
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.deep_researcher import DeepResearcher

def main():
    """Main entry point for the deep research tool."""
    parser = argparse.ArgumentParser(
        description="Deep Research Tool - Intelligent folder analysis with GitHub and codex optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python scripts/run_analysis.py --path ~/Documents --depth 6

  # GitHub repository analysis
  python scripts/run_analysis.py --path ~/Documents --github-mode --generate-github

  # Export to multiple formats
  python scripts/run_analysis.py --path ~/Documents --export csv,html,json --output ./results

  # Deep analysis with codex generation
  python scripts/run_analysis.py --path ~/Documents --depth 8 --github-mode --export all
        """
    )
    
    parser.add_argument(
        "--path", "-p", 
        required=True, 
        help="Root path to analyze"
    )
    
    parser.add_argument(
        "--depth", "-d", 
        type=int, 
        default=6, 
        help="Maximum depth to analyze (default: 6)"
    )
    
    parser.add_argument(
        "--github-mode", 
        action="store_true", 
        help="Enable GitHub repository analysis and optimization"
    )
    
    parser.add_argument(
        "--export", "-e", 
        nargs="+", 
        default=["csv", "html", "json"], 
        choices=["csv", "html", "json", "markdown", "all"],
        help="Export formats (default: csv,html,json)"
    )
    
    parser.add_argument(
        "--output", "-o", 
        help="Output directory (default: ./deep_research_output)"
    )
    
    parser.add_argument(
        "--generate-github", 
        action="store_true", 
        help="Generate GitHub repository structure files"
    )
    
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--quiet", "-q", 
        action="store_true", 
        help="Suppress non-essential output"
    )
    
    args = parser.parse_args()
    
    # Handle 'all' export option
    if 'all' in args.export:
        args.export = ['csv', 'html', 'json', 'markdown']
    
    # Validate path
    if not Path(args.path).exists():
        print(f"❌ Error: Path '{args.path}' does not exist")
        sys.exit(1)
    
    if not Path(args.path).is_dir():
        print(f"❌ Error: Path '{args.path}' is not a directory")
        sys.exit(1)
    
    # Set output directory
    if args.output is None:
        args.output = Path(args.path) / "deep_research_output"
    
    # Initialize researcher
    try:
        researcher = DeepResearcher(
            root_path=args.path,
            max_depth=args.depth,
            github_mode=args.github_mode
        )
    except Exception as e:
        print(f"❌ Error initializing researcher: {e}")
        sys.exit(1)
    
    # Run analysis
    try:
        print("🔍 Deep Research Tool")
        print("=" * 50)
        print(f"📁 Analyzing: {args.path}")
        print(f"📏 Max depth: {args.depth}")
        print(f"🐙 GitHub mode: {args.github_mode}")
        print(f"📤 Export formats: {', '.join(args.export)}")
        print(f"📂 Output directory: {args.output}")
        print()
        
        # Perform analysis
        result = researcher.analyze()
        
        # Export results
        if not args.quiet:
            print("\n📤 Exporting results...")
        researcher.export_results(result, args.export, args.output)
        
        # Generate GitHub structure if requested
        if args.generate_github:
            if not args.quiet:
                print("\n🐙 Generating GitHub repository structure...")
            researcher.generate_github_structure(result, args.output)
        
        # Print summary
        if not args.quiet:
            print("\n🎉 Analysis complete!")
            print("=" * 50)
            print(f"📊 Summary:")
            print(f"   📁 Files analyzed: {result.total_files:,}")
            print(f"   📂 Directories: {result.total_directories:,}")
            print(f"   📏 Max depth reached: {result.max_depth}")
            print(f"   🔄 Duplicate groups: {len(result.duplicate_groups)}")
            print(f"   📂 Unique categories: {len(result.categories)}")
            print(f"   📄 File types: {len(result.file_types)}")
            
            if args.github_mode and hasattr(result, 'github_structure'):
                health_score = result.github_structure.get('repository_health_score', 0)
                print(f"   🐙 GitHub health score: {health_score}/100")
            
            print(f"\n📁 Results saved to: {args.output}")
            print(f"🌐 Open {args.output}/dashboard.html in your browser to explore the results")
        
    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
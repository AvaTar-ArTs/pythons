#!/usr/bin/env python3
"""
Example usage of Deep Research Tool
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.deep_researcher import DeepResearcher


def example_basic_analysis():
    """Example of basic folder analysis."""
    print("🔍 Example: Basic Folder Analysis")
    print("=" * 40)

    # Initialize researcher
    researcher = DeepResearcher(
        root_path="~/Documents",  # Change to your path
        max_depth=4,
    )

    # Run analysis
    result = researcher.analyze()

    # Export results
    researcher.export_results(result, ["csv", "html", "json"])

    print("✅ Analysis complete!")
    print(f"   Files: {result.total_files:,}")
    print(f"   Directories: {result.total_directories:,}")
    print(f"   Categories: {len(result.categories)}")


def example_github_analysis():
    """Example of GitHub repository analysis."""
    print("\n🐙 Example: GitHub Repository Analysis")
    print("=" * 40)

    # Initialize researcher with GitHub mode
    researcher = DeepResearcher(
        root_path="~/Documents",  # Change to your path
        max_depth=6,
        github_mode=True,
    )

    # Run analysis
    result = researcher.analyze()

    # Export results
    researcher.export_results(result, ["html", "json"])

    # Generate GitHub structure
    researcher.generate_github_structure(result)

    print("✅ GitHub analysis complete!")
    if hasattr(result, "github_structure"):
        health_score = result.github_structure.get("repository_health_score", 0)
        print(f"   Health score: {health_score}/100")


def example_custom_analysis():
    """Example of custom analysis with specific parameters."""
    print("\n⚙️  Example: Custom Analysis")
    print("=" * 40)

    # Initialize researcher with custom parameters
    researcher = DeepResearcher(
        root_path="~/Documents",  # Change to your path
        max_depth=8,
    )

    # Run analysis
    result = researcher.analyze()

    # Export to specific formats
    researcher.export_results(result, ["csv", "html"], "./custom_output")

    # Generate GitHub structure
    researcher.generate_github_structure(result, "./custom_output")

    print("✅ Custom analysis complete!")
    print("   Output saved to: ./custom_output")


def main():
    """Run all examples."""
    print("🚀 Deep Research Tool - Examples")
    print("=" * 50)

    try:
        # Run examples
        example_basic_analysis()
        example_github_analysis()
        example_custom_analysis()

        print("\n🎉 All examples completed successfully!")
        print("\n📚 Next steps:")
        print("   1. Check the generated HTML files in your browser")
        print("   2. Review the CSV files for detailed data")
        print("   3. Use the generated GitHub structure files")
        print("   4. Explore the codex configurations")

    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print(
            "   Make sure to update the paths in the examples to point to existing directories"
        )


if __name__ == "__main__":
    main()

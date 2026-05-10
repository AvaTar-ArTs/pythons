#!/usr/bin/env python3
"""
Example script demonstrating the usage of the Content Organizer Agent.

This script shows how to use the agent programmatically and customize its behavior
for specific organizational needs.
"""

import os
import json
from datetime import datetime
from content_organizer_agent import ContentOrganizerAgent, ContentAnalyzer


def example_basic_usage():
    """Demonstrate basic usage of the Content Organizer Agent."""
    print("=== Basic Usage Example ===")
    
    # Initialize the agent
    agent = ContentOrganizerAgent()
    
    # For this example, we'll use a mock directory path
    # In practice, replace this with your actual directory
    test_directory = "./sample_documents"  # This would be your target directory
    
    # Create sample directory structure for demonstration
    os.makedirs(test_directory, exist_ok=True)
    os.makedirs(os.path.join(test_directory, "subfolder1"), exist_ok=True)
    os.makedirs(os.path.join(test_directory, "subfolder2"), exist_ok=True)
    
    # Create sample files for demonstration
    sample_files = [
        ("strategy_document.txt", "This contains strategic planning information"),
        ("ml_research_paper.pdf", "Machine learning research paper content"),
        ("web_dev_guide.md", "Guide for web development best practices"),
        ("automation_script.py", "# Python automation script"),
        ("financial_report.xlsx", "Financial data and analysis"),
        ("subfolder1/meeting_notes.txt", "Notes from strategic meeting"),
        ("subfolder2/data_analysis.R", "# R script for data analysis"),
    ]
    
    for file_path, content in sample_files:
        full_path = os.path.join(test_directory, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
    
    print(f"Created sample directory structure in: {test_directory}")
    
    try:
        # Perform analysis with default settings
        result = agent.analyze_directory(test_directory, max_depth=3)
        
        # Print summary report
        report = agent.generate_summary_report(result)
        print(report)
        
        # Show first few CSV mappings
        print("\nFirst 3 CSV Mappings:")
        for i, mapping in enumerate(result['csv_mappings'][:3]):
            print(f"{i+1}. {mapping['original_name']} -> {mapping['semantic_category']}")
        
        # Export CSV mapping
        csv_output_path = f"example_mapping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        agent.export_csv_mapping(result['csv_mappings'], csv_output_path)
        print(f"\nCSV mapping exported to: {csv_output_path}")
        
    except Exception as e:
        print(f"Error in basic usage example: {str(e)}")


def example_custom_categories():
    """Demonstrate how to customize semantic categories."""
    print("\n=== Custom Categories Example ===")
    
    # Initialize analyzer
    analyzer = ContentAnalyzer()
    
    # Add custom categories specific to your domain
    custom_categories = {
        'Project Management': ['project', 'task', 'schedule', 'timeline', 'milestone', 'gantt', 'kanban'],
        'Marketing Materials': ['marketing', 'campaign', 'advertising', 'promotion', 'brand', 'outreach'],
        'Customer Service': ['customer', 'support', 'ticket', 'feedback', 'complaint', 'satisfaction'],
        'HR Documents': ['employee', 'hr', 'personnel', 'benefits', 'onboarding', 'evaluation'],
        'R&D': ['research', 'development', 'experiment', 'prototype', 'innovation', 'lab'],
        'Compliance': ['compliance', 'regulatory', 'audit', 'certification', 'policy', 'procedure']
    }
    
    # Extend the default categories
    analyzer.semantic_categories.update(custom_categories)
    
    # Create a test file with custom category keywords
    test_file = "marketing_campaign_strategy.docx"
    content_preview = "This document outlines our new marketing campaign strategy for Q1 2025"
    
    # Categorize using extended categories
    category, tags, business_value = analyzer.categorize_semantically(test_file, content_preview)
    
    print(f"File: {test_file}")
    print(f"Content: {content_preview}")
    print(f"Suggested Category: {category}")
    print(f"Tags: {', '.join(tags)}")
    print(f"Business Value: {business_value}")


def example_advanced_usage():
    """Demonstrate advanced usage with custom configurations."""
    print("\n=== Advanced Usage Example ===")
    
    # Initialize the agent
    agent = ContentOrganizerAgent()
    
    # Example of how you might customize the analysis
    directory_to_analyze = "./sample_documents"  # Replace with your directory
    
    print(f"Performing advanced analysis on: {directory_to_analyze}")
    
    # Perform analysis with specific parameters
    result = agent.analyze_directory(directory_to_analyze, max_depth=4)
    
    # Access detailed analysis results
    improvements = result['improvements']
    
    print(f"Total files analyzed: {improvements['total_files']}")
    print(f"Total size: {improvements['total_size_bytes']:,} bytes")
    print(f"Top 5 extensions: {improvements['top_extensions'][:5]}")
    print(f"Top 5 categories: {improvements['top_categories'][:5]}")
    
    # Show improvement suggestions
    print("\nImprovement Suggestions:")
    for suggestion in improvements['improvement_suggestions']:
        print(f"  - {suggestion}")
    
    # Example of filtering results by category
    csv_mappings = result['csv_mappings']
    strategy_files = [m for m in csv_mappings if 'strategy' in m['semantic_category'].lower()]
    
    print(f"\nFound {len(strategy_files)} strategy-related files:")
    for file_info in strategy_files[:3]:  # Show first 3
        print(f"  - {file_info['original_name']} (Business Value: {file_info['business_value']})")


def example_integration():
    """Demonstrate how to integrate the agent into a larger workflow."""
    print("\n=== Integration Example ===")
    
    # Initialize the agent
    agent = ContentOrganizerAgent()
    
    # Simulate a workflow where we analyze multiple directories
    directories_to_analyze = [
        "./documents",
        "./projects",
        "./reports"
    ]
    
    # Create sample directories
    for dir_path in directories_to_analyze:
        os.makedirs(dir_path, exist_ok=True)
        # Create a sample file in each
        sample_file = os.path.join(dir_path, f"sample_{os.path.basename(dir_path)}.txt")
        with open(sample_file, 'w') as f:
            f.write(f"Sample content for {dir_path}")
    
    all_results = {}
    
    for directory in directories_to_analyze:
        if os.path.exists(directory):
            print(f"Analyzing: {directory}")
            try:
                result = agent.analyze_directory(directory, max_depth=3)
                all_results[directory] = {
                    'file_count': result['improvements']['total_files'],
                    'total_size': result['improvements']['total_size_bytes'],
                    'categories': result['improvements']['top_categories'][:3],
                    'suggestions': result['improvements']['improvement_suggestions']
                }
            except Exception as e:
                print(f"  Error analyzing {directory}: {str(e)}")
        else:
            print(f"  Directory does not exist: {directory}")
    
    # Summarize findings across all directories
    print("\nSummary Across All Directories:")
    total_files = sum(data['file_count'] for data in all_results.values())
    total_size = sum(data['total_size'] for data in all_results.values())
    
    print(f"Total files across all directories: {total_files}")
    print(f"Total size across all directories: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
    
    # Show top categories across all directories
    all_categories = {}
    for data in all_results.values():
        for category, count in data['categories']:
            all_categories[category] = all_categories.get(category, 0) + count
    
    print(f"\nTop categories across all directories:")
    for category, count in sorted(all_categories.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  - {category}: {count} files")


def cleanup_example_files():
    """Clean up example files created during demonstration."""
    import shutil
    
    print("\n=== Cleaning Up Example Files ===")
    
    example_dirs = ["./sample_documents", "./documents", "./projects", "./reports"]
    
    for directory in example_dirs:
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
                print(f"Removed: {directory}")
            except Exception as e:
                print(f"Could not remove {directory}: {str(e)}")


if __name__ == "__main__":
    print("Content Organizer Agent - Usage Examples")
    print("=" * 50)
    
    # Run examples
    example_basic_usage()
    example_custom_categories()
    example_advanced_usage()
    example_integration()
    
    # Clean up
    cleanup_example_files()
    
    print("\nExamples completed successfully!")
    print("\nTo use the Content Organizer Agent with your own files:")
    print("1. Run: python content_organizer_agent.py <your_directory_path>")
    print("2. Or import and use programmatically as shown in these examples")
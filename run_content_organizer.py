#!/usr/bin/env python3
"""
Utility script to run the Content Organizer Agent on your Documents folder.
This script implements the same content-aware organization approaches 
demonstrated in fancy-qwen.txt.
"""

import os
import sys
from pathlib import Path
from content_organizer_agent import ContentOrganizerAgent


def run_on_documents_folder():
    """Run the Content Organizer Agent on the Documents folder."""
    # Get the user's Documents directory
    home_dir = Path.home()
    documents_dir = home_dir / "Documents"
    
    if not documents_dir.exists():
        print(f"Documents directory does not exist: {documents_dir}")
        return False
    
    print(f"Analyzing Documents folder: {documents_dir}")
    print(f"Folder exists: {documents_dir.exists()}")
    print(f"Is directory: {documents_dir.is_dir()}")
    
    # Initialize the agent
    agent = ContentOrganizerAgent()
    
    try:
        # Perform analysis with reasonable depth
        print("\nStarting content-aware analysis...")
        result = agent.analyze_directory(str(documents_dir), max_depth=5)
        
        # Generate and display summary report
        report = agent.generate_summary_report(result)
        print(report)
        
        # Export CSV mapping
        csv_output_path = f"documents_organizational_mapping_{result['analysis_timestamp'].replace(':', '-')}.csv"
        agent.export_csv_mapping(result['csv_mappings'], csv_output_path)
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"📁 CSV mapping saved to: {csv_output_path}")
        print(f"📊 Total mappings created: {len(result['csv_mappings'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_on_specified_directory(directory_path):
    """Run the Content Organizer Agent on a specified directory."""
    if not os.path.exists(directory_path):
        print(f"Directory does not exist: {directory_path}")
        return False
    
    if not os.path.isdir(directory_path):
        print(f"Path is not a directory: {directory_path}")
        return False
    
    print(f"Analyzing specified directory: {directory_path}")
    
    # Initialize the agent
    agent = ContentOrganizerAgent()
    
    try:
        # Perform analysis
        print("\nStarting content-aware analysis...")
        result = agent.analyze_directory(directory_path, max_depth=5)
        
        # Generate and display summary report
        report = agent.generate_summary_report(result)
        print(report)
        
        # Export CSV mapping
        timestamp = result['analysis_timestamp'].replace(':', '-')
        csv_output_path = f"organizational_mapping_{os.path.basename(directory_path)}_{timestamp}.csv"
        agent.export_csv_mapping(result['csv_mappings'], csv_output_path)
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"📁 CSV mapping saved to: {csv_output_path}")
        print(f"📊 Total mappings created: {len(result['csv_mappings'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function to run the Content Organizer Agent."""
    print("🚀 Content Organizer Agent")
    print("=" * 50)
    print("Implementing content-aware file organization approaches")
    print("based on methodologies from fancy-qwen.txt")
    print()
    
    if len(sys.argv) > 1:
        # Use specified directory
        directory_path = sys.argv[1]
        success = run_on_specified_directory(directory_path)
    else:
        # Use Documents folder by default
        success = run_on_documents_folder()
    
    if success:
        print("\n💡 Next steps:")
        print("   - Review the generated CSV mapping file")
        print("   - Consider the improvement suggestions")
        print("   - Use the mapping to reorganize your files")
        print("   - Customize categories in the ContentAnalyzer if needed")
    else:
        print("\n❌ Analysis failed. Please check the error messages above.")


if __name__ == "__main__":
    main()
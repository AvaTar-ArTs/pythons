#!/usr/bin/env python3
"""
Main entry point for the Python Automation Framework

This CLI provides access to the comprehensive suite of automation tools
for file management, code analysis, and system maintenance tasks.
"""

import argparse
import sys
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Python Automation Framework - Comprehensive automation tools",
        prog="pythons_sort"
    )
    
    # Define subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analysis command
    analyze_parser = subparsers.add_parser('analyze', help='Run analysis tools')
    analyze_parser.add_argument('path', help='Path to analyze')
    analyze_parser.add_argument('--tool', default='python_complexity_analyzer', 
                              help='Specific analysis tool to run (default: python_complexity_analyzer)')
    analyze_parser.add_argument('--output', help='Output directory for results')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Run cleanup tools')
    cleanup_parser.add_argument('path', help='Path to cleanup')
    cleanup_parser.add_argument('--tool', default='organize_files', 
                              help='Specific cleanup tool to run (default: organize_files)')
    cleanup_parser.add_argument('--dry-run', action='store_true', 
                               help='Preview changes without making them')
    
    # Deduplication command
    dedup_parser = subparsers.add_parser('dedup', help='Run deduplication tools')
    dedup_parser.add_argument('path', help='Path to check for duplicates')
    dedup_parser.add_argument('--tool', default='duplicate_cleaner', 
                             help='Specific dedup tool to run (default: duplicate_cleaner)')
    dedup_parser.add_argument('--dry-run', action='store_true', 
                             help='Preview changes without making them')
    
    # Organize command
    organize_parser = subparsers.add_parser('organize', help='Run organization tools')
    organize_parser.add_argument('path', help='Path to organize')
    organize_parser.add_argument('--tool', default='organize_files', 
                               help='Specific organization tool to run (default: organize_files)')
    organize_parser.add_argument('--dry-run', action='store_true', 
                               help='Preview changes without making them')
    
    # Scanner command
    scan_parser = subparsers.add_parser('scan', help='Run scanning tools')
    scan_parser.add_argument('path', help='Path to scan')
    scan_parser.add_argument('--tool', default='function_scanner', 
                           help='Specific scanner tool to run (default: function_scanner)')
    
    # Rename command
    rename_parser = subparsers.add_parser('rename', help='Run renaming tools')
    rename_parser.add_argument('path', help='Path for renaming operations')
    rename_parser.add_argument('--tool', default='execute_renames', 
                             help='Specific rename tool to run (default: execute_renames)')
    rename_parser.add_argument('--dry-run', action='store_true', 
                             help='Preview changes without making them')
    
    # PDF analysis command
    pdf_parser = subparsers.add_parser('pdf', help='Run PDF analysis tools')
    pdf_parser.add_argument('--analyze', help='Analyze PDF collection from file paths')
    pdf_parser.add_argument('--path', help='Path to PDF analysis results')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get information about tools')
    info_parser.add_argument('--category', choices=['analysis', 'cleanup', 'dedup', 'rename', 'scanners'],
                            help='Show tools in specific category')
    info_parser.add_argument('--all', action='store_true', help='Show all available tools')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Get the tools directory
    tools_dir = Path(__file__).parent / 'src' / 'tools'
    
    # Based on the command, execute the appropriate tool
    if args.command == 'analyze':
        execute_tool(tools_dir / 'analysis', args.tool, args.path, dry_run=getattr(args, 'dry_run', False))
    elif args.command == 'cleanup':
        execute_tool(tools_dir / 'cleanup', args.tool, args.path, dry_run=getattr(args, 'dry_run', False))
    elif args.command == 'dedup':
        execute_tool(tools_dir / 'dedup', args.tool, args.path, dry_run=getattr(args, 'dry_run', False))
    elif args.command == 'organize':
        execute_tool(tools_dir / 'cleanup', args.tool, args.path, dry_run=getattr(args, 'dry_run', False))
    elif args.command == 'scan':
        execute_tool(tools_dir / 'scanners', args.tool, args.path)
    elif args.command == 'rename':
        execute_tool(tools_dir / 'rename', args.tool, args.path, dry_run=getattr(args, 'dry_run', False))
    elif args.command == 'pdf':
        if args.analyze:
            execute_pdf_analysis(args.analyze)
        else:
            pdf_parser.print_help()
    elif args.command == 'info':
        if args.all:
            show_all_tools(tools_dir)
        elif args.category:
            show_category_tools(tools_dir, args.category)
        else:
            info_parser.print_help()
    else:
        parser.print_help()
        return 1
    
    return 0


def execute_tool(tool_category_dir, tool_name, path, dry_run=False):
    """Execute a specific tool from a category."""
    # Convert tool name to module format (replace hyphens with underscores)
    tool_module = tool_name.replace('-', '_')
    
    # Look for the tool in the category directory
    tool_path = tool_category_dir / f"{tool_module}.py"
    
    if not tool_path.exists():
        # Try to find a matching tool (with version numbers like tool_name_1.py)
        import glob
        matching_files = list(tool_category_dir.glob(f"{tool_module}*.py"))
        if matching_files:
            tool_path = matching_files[0]  # Use the first match
        else:
            print(f"Error: Tool '{tool_name}' not found in {tool_category_dir}")
            sys.exit(1)
    
    # Add the directory to Python path
    sys.path.insert(0, str(tool_category_dir))
    
    # Import and execute the tool if it has a main function
    try:
        # Import the module dynamically
        import importlib.util
        spec = importlib.util.spec_from_file_location(tool_module, tool_path)
        module = importlib.util.module_from_spec(spec)
        
        # Set up command line arguments for the tool
        original_argv = sys.argv
        sys.argv = [str(tool_path), str(path)]
        if dry_run:
            sys.argv.append('--dry-run')
        
        # Execute the module
        spec.loader.exec_module(module)
        
        # Restore original argv
        sys.argv = original_argv
        
    except Exception as e:
        print(f"Error executing tool {tool_name}: {e}")
        sys.exit(1)


def execute_pdf_analysis(file_path):
    """Execute the PDF analysis."""
    analyzer_path = Path(__file__).parent / 'pdf_analyzer.py'
    if analyzer_path.exists():
        sys.path.insert(0, str(Path(__file__).parent))
        import importlib.util
        spec = importlib.util.spec_from_file_location('pdf_analyzer', analyzer_path)
        module = importlib.util.module_from_spec(spec)
        
        # Set up arguments for the PDF analyzer
        original_argv = sys.argv
        sys.argv = [str(analyzer_path), '--file', str(file_path)]
        
        spec.loader.exec_module(module)
        sys.argv = original_argv
    else:
        print(f"PDF analyzer not found at {analyzer_path}")
        sys.exit(1)


def show_all_tools(tools_dir):
    """Show all available tools."""
    categories = ['analysis', 'cleanup', 'dedup', 'rename', 'scanners']
    
    for category in categories:
        print(f"\n{category.upper()} TOOLS:")
        category_dir = tools_dir / category
        if category_dir.exists():
            tools = [f.name.replace('.py', '') for f in category_dir.glob('*.py') 
                    if not f.name.startswith('__') and f.name != 'README.md']
            tools = sorted(set([t.split('_')[0] for t in tools]))  # Get base names
            for tool in tools[:10]:  # Show first 10 tools in each category
                print(f"  - {tool}")
            if len(tools) > 10:
                print(f"  ... and {len(tools) - 10} more tools")


def show_category_tools(tools_dir, category):
    """Show tools in a specific category."""
    category_dir = tools_dir / category
    if category_dir.exists():
        print(f"\n{category.upper().replace('_', ' ')} TOOLS:")
        tools = [f.name.replace('.py', '') for f in category_dir.glob('*.py') 
                if not f.name.startswith('__') and f.name != 'README.md']
        tools = sorted(set([t.split('_')[0] for t in tools]))  # Get base names
        for tool in tools:
            print(f"  - {tool}")
        print(f"\nTotal: {len(tools)} tools")
    else:
        print(f"Category '{category}' not found")


if __name__ == "__main__":
    sys.exit(main())
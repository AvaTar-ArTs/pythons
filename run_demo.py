#!/usr/bin/env python3
"""
Demonstration script for the Automation Ecosystem Consolidation System
This script runs a limited analysis to showcase the system's capabilities
"""

import os
import json
from pathlib import Path
from automation_consolidation_system import AutomationConsolidationSystem

def demonstrate_system():
    print("🔧 AUTOMATION ECOSYSTEM CONSOLIDATION SYSTEM")
    print("="*60)
    print("Demonstrating system capabilities with a focused analysis...\n")
    
    # Initialize the system
    system = AutomationConsolidationSystem(root_path="/Users/steven")
    
    print("1. 📁 SCANNING DIRECTORY STRUCTURE")
    print("-"*40)
    
    # Show some example directory structures
    avatararts_path = Path("/Users/steven/AVATARARTS")
    if avatararts_path.exists():
        print(f"   Found AVATARARTS directory with {len(list(avatararts_path.glob('*'))) if avatararts_path.exists() else 0} items")

    pythons_path = Path("/Users/steven/pythons")
    if pythons_path.exists():
        # Count Python files using os.walk since Path.glob doesn't support recursive in older Python versions
        py_count = 0
        for root, dirs, files in os.walk(pythons_path):
            py_count += len([f for f in files if f.endswith('.py')])
        print(f"   Found pythons directory with {py_count} Python files")
    
    print("\n2. 🏢 IDENTIFYING BUSINESS VERTICALS")
    print("-"*40)
    
    # Show the business verticals defined in the system
    for i, vertical in enumerate(system.business_verticals, 1):
        print(f"   {i}. {vertical}")
    
    print("\n3. 🔍 CONFIGURATION LOADED")
    print("-"*40)
    print(f"   - Exclusion patterns: {len(system.exclusion_patterns)}")
    print(f"   - Max workers: {system.max_workers}")
    print(f"   - Chunk size: {system.chunk_size}")
    
    print("\n4. 📊 SAMPLE ASSET ANALYSIS")
    print("-"*40)
    
    # Perform a limited scan to demonstrate functionality
    sample_path = Path("/Users/steven")
    sample_assets = []
    
    # Scan just a few files to demonstrate
    py_files = list(sample_path.glob("**/*.py"))[:10]  # Take first 10 Python files
    
    for py_file in py_files:
        try:
            stat = py_file.stat()
            business_vertical = system.determine_business_vertical(str(py_file))
            business_value = system.calculate_business_value_score(str(py_file))
            
            print(f"   File: {py_file.name}")
            print(f"     Size: {stat.st_size:,} bytes")
            print(f"     Modified: {stat.st_mtime}")
            print(f"     Business Vertical: {business_vertical}")
            print(f"     Business Value: {business_value:.1f}")
            print()
        except:
            continue
    
    print("\n5. 🎯 SYSTEM CAPABILITIES OVERVIEW")
    print("-"*40)
    print("   • Duplicate detection using checksums")
    print("   • Business vertical classification")
    print("   • Business value scoring")
    print("   • Risk assessment for consolidations")
    print("   • Priority-ranked recommendations")
    print("   • Comprehensive reporting")
    print("   • Implementation planning")
    
    print("\n6. 📈 EXPECTED OUTPUT FILES")
    print("-"*40)
    print("   • master_inventory.json - Complete asset inventory")
    print("   • vertical_summaries.json - Business vertical summaries")
    print("   • consolidation_recommendations.json - Detailed recommendations")
    print("   • top_priority_consolidations.csv - CSV with top priorities")
    print("   • vertical_*_assets.json - Detailed reports per vertical")
    print("   • consolidation_implementation_plan.md - Step-by-step plan")
    
    print("\n7. 🚀 TO RUN FULL ANALYSIS:")
    print("-"*40)
    print("   python automation_consolidation_system.py")
    print("\n   This will:")
    print("   • Scan all directories in /Users/steven")
    print("   • Identify duplicates and similar files")
    print("   • Generate business value scores")
    print("   • Create consolidation recommendations")
    print("   • Export comprehensive reports")
    print("   • Generate implementation plan")
    
    print("\n" + "="*60)
    print("✅ DEMONSTRATION COMPLETE")
    print("The system is ready for full analysis!")
    print("="*60)

if __name__ == "__main__":
    demonstrate_system()
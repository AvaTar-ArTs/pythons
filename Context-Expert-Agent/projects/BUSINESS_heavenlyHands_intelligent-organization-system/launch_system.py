#!/usr/bin/env python3
"""
Intelligent Organization System Launcher
=======================================

This script launches the intelligent organization system for the Heavenly Hands project.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from integration_system import IntelligentOrganizationSystem

def main():
    """Main launcher function."""
    print("🚀 Starting Intelligent Organization System...")
    print("=" * 60)
    
    # Initialize system
    system = IntelligentOrganizationSystem()
    
    # Get system status
    status = system.get_system_status()
    print(f"📊 System Status:")
    print(f"  Running: {status.is_running}")
    print(f"  Components: {status.components_status}")
    print(f"  System Load: {status.system_load:.2f}")
    
    # Analyze Heavenly Hands project
    print("\n🔍 Analyzing Heavenly Hands project...")
    analysis = system.analyze_project()
    
    print(f"\n📈 Analysis Results:")
    print(f"  Content Awareness Score: {analysis.content_awareness_score:.2f}")
    print(f"  Overall Health Score: {analysis.overall_health_score:.2f}")
    print(f"  Automation Opportunities: {len(analysis.automation_opportunities)}")
    print(f"  Optimization Recommendations: {len(analysis.optimization_recommendations)}")
    
    # Show recommendations
    print(f"\n💡 Top Recommendations:")
    for i, rec in enumerate(analysis.optimization_recommendations[:5], 1):
        print(f"  {i}. {rec}")
    
    # Perform optimization
    print(f"\n⚡ Starting optimization...")
    optimization_result = system.optimize_heavenly_hands_project()
    
    print(f"✅ Optimization initiated:")
    print(f"  Automation Workflow: {optimization_result['automation_workflow_id']}")
    print(f"  Agentic Plan: {optimization_result['agentic_plan_id']}")
    
    print("\n" + "=" * 60)
    print("✅ Intelligent Organization System Ready!")
    print("\nPress Ctrl+C to stop the system...")
    
    try:
        # Keep system running
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down system...")
        system.shutdown()
        print("✅ System shutdown complete")

if __name__ == "__main__":
    main()

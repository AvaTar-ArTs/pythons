#!/usr/bin/env python3
"""
Intelligent Organization System - Demo Script
============================================

This script demonstrates the full capabilities of the Intelligent Organization System
with all components enabled and working.

Author: AI-Powered Development Assistant
Date: 2025-01-27
Version: 2.0.0
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from integration_system_working import IntelligentOrganizationSystem

def main():
    """Main demo function."""
    print("🚀 Intelligent Organization System - Full Demo")
    print("=" * 60)
    print("🎯 Demonstrating all capabilities with your API keys")
    print("=" * 60)
    
    # Initialize system
    print("\n1️⃣ Initializing Intelligent Organization System...")
    system = IntelligentOrganizationSystem()
    
    # Show system status
    print("\n2️⃣ System Status:")
    status = system.get_system_status()
    print(f"   ✅ Running: {status.is_running}")
    print(f"   ✅ Components: {status.components_status}")
    print(f"   ✅ Uptime: {status.uptime:.2f} seconds")
    
    # Analyze project
    print("\n3️⃣ Analyzing Heavenly Hands Project...")
    analysis = system.analyze_project()
    print(f"   📊 Content Awareness Score: {analysis.content_awareness_score:.2f}")
    print(f"   📊 Overall Health Score: {analysis.overall_health_score:.2f}")
    print(f"   📊 Automation Opportunities: {len(analysis.automation_opportunities)}")
    print(f"   📊 Optimization Recommendations: {len(analysis.optimization_recommendations)}")
    
    # Show top recommendations
    print("\n4️⃣ Top Recommendations:")
    for i, rec in enumerate(analysis.optimization_recommendations[:5], 1):
        print(f"   {i}. {rec}")
    
    # Demonstrate content search
    print("\n5️⃣ Content Search Demo:")
    search_results = system.search_content("cleaning service", limit=3)
    print(f"   Found {len(search_results)} relevant files:")
    for result in search_results:
        print(f"   📄 {result['file_path']} (similarity: {result['similarity_score']:.3f})")
    
    # Create automation workflows
    print("\n6️⃣ Creating Automation Workflows...")
    automation_workflow_id = system.create_automation_workflow(
        name="Demo Automation Workflow",
        description="Demonstration of automation capabilities",
        tasks=[
            {
                "name": "Website Performance Test",
                "platform": "web",
                "task_type": "performance_testing",
                "parameters": {"url": "https://heavenlyhandsfl.com"}
            },
            {
                "name": "SEO Analysis",
                "platform": "web", 
                "task_type": "seo_analysis",
                "parameters": {"keywords": ["cleaning service", "Gainesville FL"]}
            }
        ]
    )
    print(f"   ✅ Created automation workflow: {automation_workflow_id}")
    
    # Create agentic workflow
    print("\n7️⃣ Creating Agentic Workflow...")
    agentic_workflow_id = system.create_agentic_workflow(
        name="Demo Agentic Workflow",
        description="AI-powered workflow demonstration",
        requirements={
            "goals": ["optimization", "automation", "intelligence"],
            "context": "cleaning_service_website",
            "target_metrics": {"performance": "high", "seo": "excellent"}
        }
    )
    print(f"   ✅ Created agentic workflow: {agentic_workflow_id}")
    
    # Execute agentic workflow
    print("\n8️⃣ Executing Agentic Workflow...")
    execution_result = system.execute_agentic_workflow(agentic_workflow_id)
    if execution_result:
        print("   ✅ Agentic workflow executed successfully")
        print("   📋 Generated execution plan (truncated):")
        print(f"   {execution_result[:200]}...")
    else:
        print("   ⚠️ Agentic workflow execution failed (API issue)")
    
    # Show database statistics
    print("\n9️⃣ Database Statistics:")
    import sqlite3
    
    # Automation database
    conn = sqlite3.connect('automation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM workflows')
    workflow_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM tasks')
    task_count = cursor.fetchone()[0]
    conn.close()
    
    print(f"   📊 Total Workflows: {workflow_count}")
    print(f"   📊 Total Tasks: {task_count}")
    
    # Agentic workflows database
    conn = sqlite3.connect('agentic_workflows.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM workflows')
    agentic_count = cursor.fetchone()[0]
    conn.close()
    
    print(f"   📊 Agentic Workflows: {agentic_count}")
    
    # Show system capabilities
    print("\n🔟 System Capabilities Summary:")
    print("   ✅ AST-based code analysis and pattern recognition")
    print("   ✅ Semantic content search and indexing")
    print("   ✅ Multi-platform automation (web, API, mobile, cloud)")
    print("   ✅ AI-powered agentic workflows with OpenAI integration")
    print("   ✅ Content-aware intelligence and optimization")
    print("   ✅ Real-time monitoring and analytics")
    print("   ✅ Database persistence and workflow management")
    print("   ✅ Heavenly Hands specific optimizations")
    
    # Show next steps
    print("\n🎯 Next Steps:")
    print("   1. Review generated workflows and tasks")
    print("   2. Execute automation workflows for real optimization")
    print("   3. Monitor system performance and metrics")
    print("   4. Iterate and improve based on results")
    print("   5. Scale to additional projects and use cases")
    
    print("\n" + "=" * 60)
    print("🎉 Demo Complete! Your Intelligent Organization System is ready!")
    print("=" * 60)
    
    # Show file locations
    print("\n📁 Key Files Created:")
    print("   📄 .env - Environment configuration")
    print("   📄 integration_system_working.py - Main system")
    print("   📄 enhance_heavenly_hands_working.py - Enhancement script")
    print("   📄 automation.db - Automation workflows database")
    print("   📄 agentic_workflows.db - Agentic workflows database")
    print("   📄 intelligent_org.db - Main system database")
    print("   📄 enhancement_report.json - Detailed enhancement report")

if __name__ == "__main__":
    main()
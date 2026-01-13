#!/usr/bin/env python3
"""
Enhanced Creative Automation System - Full Demo
===============================================

Comprehensive demonstration of all enhanced capabilities
"""

import os
import json
from enhanced_creative_automation import EnhancedIntelligentOrganizationSystem
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main demo function"""
    print("🚀 Enhanced Creative Automation System - Full Demo")
    print("=" * 60)
    
    # Initialize system
    system = EnhancedIntelligentOrganizationSystem()
    
    # 1. System Status
    print("\n1️⃣ System Status:")
    status = system.get_system_status()
    print(f"   📊 System: {status['system_name']} v{status['version']}")
    print(f"   🔧 Components: {status['components']}")
    print(f"   🎯 Capabilities: {len(status['capabilities'])} features enabled")
    
    # 2. Content Indexing
    print("\n2️⃣ Enhanced Content Indexing:")
    print("   🔍 Indexing project with enhanced semantic analysis...")
    system.index_project_content()
    print("   ✅ Content indexed with advanced vector search")
    
    # 3. Semantic Search Demo
    print("\n3️⃣ Enhanced Semantic Search:")
    queries = [
        "cleaning services pricing",
        "contact information",
        "customer testimonials",
        "service areas"
    ]
    
    for query in queries:
        results = system.search_content(query, categories=['cleaning_services'])
        print(f"   🔍 '{query}': {len(results)} results")
    
    # 4. Creative Automation
    print("\n4️⃣ Creative Automation Platform:")
    phone_system = system.create_heavenly_hands_phone_system()
    print(f"   📞 Phone campaign: {phone_system.get('phone_campaign_id', 'Not created')}")
    print(f"   🤖 Agentic workflow: {phone_system.get('agentic_workflow_id', 'Not created')}")
    
    # 5. Agentic Workflows
    print("\n5️⃣ Agentic Workflows:")
    workflow_id = system.agentic_workflows.create_creative_workflow(
        "Comprehensive Marketing Automation",
        {
            'business_type': 'cleaning_service',
            'goals': ['lead_generation', 'customer_retention', 'brand_awareness'],
            'channels': ['phone', 'email', 'social_media', 'website']
        }
    )
    print(f"   ✅ Created workflow: {workflow_id}")
    
    # 6. Database Statistics
    print("\n6️⃣ Database Statistics:")
    try:
        import sqlite3
        
        # Creative automation stats
        conn = sqlite3.connect('creative_automation.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM creative_tasks")
        tasks = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM automation_workflows")
        workflows = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM leads")
        leads = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"   📊 Creative Tasks: {tasks}")
        print(f"   📊 Automation Workflows: {workflows}")
        print(f"   📊 Leads: {leads}")
        
    except Exception as e:
        print(f"   ⚠️  Could not retrieve database stats: {e}")
    
    # 7. Next Steps
    print("\n7️⃣ Next Steps:")
    print("   🎯 Configure Twilio credentials for phone automation")
    print("   🎯 Set up webhook server for TwiML handling")
    print("   🎯 Execute phone campaigns for lead generation")
    print("   🎯 Monitor and optimize based on results")
    print("   🎯 Scale to additional creative projects")
    
    print("\n" + "=" * 60)
    print("🎉 Enhanced Creative Automation System Ready!")
    print("=" * 60)

if __name__ == "__main__":
    main()

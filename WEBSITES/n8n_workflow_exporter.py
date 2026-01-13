#!/usr/bin/env python3
"""
n8n Workflow Exporter
====================

Exports n8n workflow templates and creates individual JSON files
for easy import into n8n instances.

Usage:
    python n8n_workflow_exporter.py
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

def export_n8n_workflows():
    """Export n8n workflows to individual JSON files"""
    
    # Load the main template file
    template_file = Path("/Users/steven/n8n_ai_agent_templates.json")
    
    if not template_file.exists():
        print("❌ Template file not found: n8n_ai_agent_templates.json")
        return
    
    with open(template_file, 'r') as f:
        templates = json.load(f)
    
    # Create output directory
    output_dir = Path("/Users/steven/n8n_workflows")
    output_dir.mkdir(exist_ok=True)
    
    print("🚀 Exporting n8n workflows...")
    print("=" * 50)
    
    # Export individual workflows
    workflows = templates.get("n8n_workflows", {})
    
    for workflow_name, workflow_data in workflows.items():
        # Create individual workflow file
        workflow_file = output_dir / f"{workflow_name}.json"
        
        # Format for n8n import
        n8n_workflow = {
            "name": workflow_data["name"],
            "nodes": workflow_data["nodes"],
            "connections": workflow_data["connections"],
            "active": False,
            "settings": {
                "executionOrder": "v1"
            },
            "staticData": None,
            "meta": {
                "templateCredsSetupCompleted": True
            },
            "pinData": None,
            "versionId": "1"
        }
        
        with open(workflow_file, 'w') as f:
            json.dump(n8n_workflow, f, indent=2)
        
        print(f"✅ Exported: {workflow_name}.json")
    
    # Export credentials template
    credentials_file = output_dir / "credentials_template.json"
    credentials_data = {
        "credentials": templates.get("n8n_credentials", {}),
        "setup_instructions": {
            "openai": "1. Go to Settings → Credentials\n2. Add new credential\n3. Select 'OpenAI API'\n4. Enter your API key",
            "serp_api": "1. Go to Settings → Credentials\n2. Add new credential\n3. Select 'HTTP Request Auth'\n4. Enter your SERP API key",
            "news_api": "1. Go to Settings → Credentials\n2. Add new credential\n3. Select 'HTTP Request Auth'\n4. Enter your News API key"
        }
    }
    
    with open(credentials_file, 'w') as f:
        json.dump(credentials_data, f, indent=2)
    
    print(f"✅ Exported: credentials_template.json")
    
    # Export setup script
    setup_script_file = output_dir / "setup_n8n_workflows.sh"
    setup_script = """#!/bin/bash
# n8n Workflow Setup Script
# =========================

echo "🚀 Setting up n8n AI Agent Workflows"
echo "====================================="

# Check if n8n is running
if ! curl -s http://localhost:5678 > /dev/null; then
    echo "❌ n8n is not running. Please start n8n first:"
    echo "   n8n start"
    exit 1
fi

echo "✅ n8n is running"

# Create workflows directory
mkdir -p ~/.n8n/workflows

# Copy workflow files
echo "📁 Copying workflow files..."
cp *.json ~/.n8n/workflows/

echo "✅ Workflows copied to n8n directory"
echo ""
echo "Next steps:"
echo "1. Open n8n at http://localhost:5678"
echo "2. Go to Settings → Credentials"
echo "3. Add your API credentials"
echo "4. Import the workflows"
echo "5. Configure webhook URLs"
echo ""
echo "🎉 Setup complete!"
"""
    
    with open(setup_script_file, 'w') as f:
        f.write(setup_script)
    
    # Make script executable
    os.chmod(setup_script_file, 0o755)
    
    print(f"✅ Exported: setup_n8n_workflows.sh")
    
    # Create README
    readme_file = output_dir / "README.md"
    readme_content = """# n8n AI Agent Workflows

This directory contains n8n workflow templates for AI content generation automation.

## Files

- `ai_content_agent.json` - Main content generation orchestrator
- `content_research_agent.json` - Document analysis and pattern extraction
- `ai_optimization_agent.json` - Performance monitoring and optimization
- `credentials_template.json` - API credentials configuration
- `setup_n8n_workflows.sh` - Automated setup script

## Quick Start

1. **Start n8n:**
   ```bash
   n8n start
   ```

2. **Run setup script:**
   ```bash
   ./setup_n8n_workflows.sh
   ```

3. **Configure credentials:**
   - OpenAI API Key
   - SERP API Key
   - News API Key

4. **Import workflows:**
   - Go to n8n web interface
   - Import each JSON file
   - Configure webhook URLs

## Configuration

Update these URLs in each workflow:

- `webhook_url`: Your AI agent server URL
- `airtable_webhook_url`: Your Airtable webhook URL
- `notification_webhook`: Your notification webhook URL

## Support

For issues and questions, check the main setup guide:
`/Users/steven/n8n_setup_guide.md`
"""
    
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Exported: README.md")
    
    print("\n🎉 Export complete!")
    print(f"📁 Workflows exported to: {output_dir}")
    print("\nNext steps:")
    print("1. Start n8n: n8n start")
    print("2. Run setup script: ./n8n_workflows/setup_n8n_workflows.sh")
    print("3. Configure credentials in n8n")
    print("4. Import workflows")

def create_n8n_docker_compose():
    """Create Docker Compose file for n8n with AI agent"""
    
    docker_compose_content = """version: '3.8'

services:
  n8n:
    image: n8nio/n8n
    container_name: n8n-ai-agent
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin123
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://localhost:5678
    volumes:
      - n8n_data:/home/node/.n8n
      - ./n8n_workflows:/home/node/.n8n/workflows
    restart: unless-stopped

  ai-agent:
    build: .
    container_name: ai-agent-server
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SERPAPI_KEY=${SERPAPI_KEY}
      - NEWSAPI_KEY=${NEWSAPI_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./:/app
    working_dir: /app
    command: python ai_agent_server.py
    restart: unless-stopped
    depends_on:
      - n8n

  ngrok:
    image: ngrok/ngrok:latest
    container_name: ngrok-tunnel
    command:
      - "tunnel"
      - "--label"
      - "edge=edghts_1234567890"
      - "ai-agent:5000"
    environment:
      - NGROK_AUTHTOKEN=${NGROK_AUTHTOKEN}
    depends_on:
      - ai-agent

volumes:
  n8n_data:

networks:
  default:
    name: ai-agent-network
"""
    
    docker_compose_file = Path("/Users/steven/docker-compose.yml")
    with open(docker_compose_file, 'w') as f:
        f.write(docker_compose_content)
    
    print(f"✅ Created: docker-compose.yml")
    
    # Create .env file
    env_file = Path("/Users/steven/.env.docker")
    env_content = """# Docker Environment Variables
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_KEY=your_serp_api_key_here
NEWSAPI_KEY=your_news_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GROQ_API_KEY=your_groq_api_key_here
NGROK_AUTHTOKEN=your_ngrok_authtoken_here
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Created: .env.docker")

def main():
    """Main function"""
    print("🤖 n8n Workflow Exporter")
    print("=" * 30)
    
    # Export workflows
    export_n8n_workflows()
    
    # Create Docker setup
    print("\n🐳 Creating Docker setup...")
    create_n8n_docker_compose()
    
    print("\n🎉 All done!")
    print("\nYou now have:")
    print("📁 Individual n8n workflow files")
    print("🐳 Docker Compose setup")
    print("📋 Setup scripts and documentation")
    print("\nReady to deploy your AI agent! 🚀")

if __name__ == "__main__":
    main()
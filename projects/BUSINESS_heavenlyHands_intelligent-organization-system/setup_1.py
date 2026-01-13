#!/usr/bin/env python3
"""
Setup script for Intelligent Organization System
===============================================

This script sets up the intelligent organization system for the Heavenly Hands project
with all necessary dependencies and configurations.

Author: AI-Powered Development Assistant
Date: 2025-01-27
Version: 2.0.0
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import json
import yaml

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3.8, 0):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version}")

def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        sys.exit(1)

def setup_directories():
    """Create necessary directories."""
    print("📁 Setting up directories...")
    
    directories = [
        "vector_indices",
        "logs",
        "screenshots",
        "backups",
        "temp",
        "data"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  ✅ Created directory: {directory}")

def setup_database():
    """Initialize the database."""
    print("🗄️ Setting up database...")
    
    try:
        import sqlite3
        
        db_path = "intelligent_org_system.db"
        with sqlite3.connect(db_path) as conn:
            # Create tables
            conn.execute('''
                CREATE TABLE IF NOT EXISTS system_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status_data TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS project_analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT,
                    analysis_data TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS automation_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT UNIQUE,
                    task_data TEXT,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        sys.exit(1)

def download_nltk_data():
    """Download required NLTK data."""
    print("📚 Downloading NLTK data...")
    
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        print("✅ NLTK data downloaded successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not download NLTK data: {e}")

def create_sample_config():
    """Create sample configuration files."""
    print("⚙️ Creating configuration files...")
    
    # Create sample automation config
    automation_config = {
        "general": {
            "max_concurrent_tasks": 10,
            "task_timeout": 300,
            "retry_delay": 5,
            "log_level": "INFO"
        },
        "platforms": {
            "web": {
                "enabled": True,
                "browser": "chrome",
                "headless": True,
                "window_size": [1920, 1080]
            },
            "api": {
                "enabled": True,
                "base_url": "https://api.example.com",
                "timeout": 30,
                "retry_count": 3
            }
        }
    }
    
    with open("automation_config.yaml", "w") as f:
        yaml.dump(automation_config, f, default_flow_style=False)
    
    # Create sample agentic config
    agentic_config = {
        "system": {
            "max_concurrent_agents": 10,
            "max_workflow_executions": 5,
            "learning_enabled": True,
            "optimization_enabled": True
        },
        "ai": {
            "openai_api_key": "",
            "model_name": "gpt-4",
            "max_tokens": 2000,
            "temperature": 0.7
        }
    }
    
    with open("agentic_config.yaml", "w") as f:
        yaml.dump(agentic_config, f, default_flow_style=False)
    
    print("✅ Configuration files created")

def create_launcher_script():
    """Create launcher script."""
    print("🚀 Creating launcher script...")
    
    launcher_content = '''#!/usr/bin/env python3
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
    print("\\n🔍 Analyzing Heavenly Hands project...")
    analysis = system.analyze_project()
    
    print(f"\\n📈 Analysis Results:")
    print(f"  Content Awareness Score: {analysis.content_awareness_score:.2f}")
    print(f"  Overall Health Score: {analysis.overall_health_score:.2f}")
    print(f"  Automation Opportunities: {len(analysis.automation_opportunities)}")
    print(f"  Optimization Recommendations: {len(analysis.optimization_recommendations)}")
    
    # Show recommendations
    print(f"\\n💡 Top Recommendations:")
    for i, rec in enumerate(analysis.optimization_recommendations[:5], 1):
        print(f"  {i}. {rec}")
    
    # Perform optimization
    print(f"\\n⚡ Starting optimization...")
    optimization_result = system.optimize_heavenly_hands_project()
    
    print(f"✅ Optimization initiated:")
    print(f"  Automation Workflow: {optimization_result['automation_workflow_id']}")
    print(f"  Agentic Plan: {optimization_result['agentic_plan_id']}")
    
    print("\\n" + "=" * 60)
    print("✅ Intelligent Organization System Ready!")
    print("\\nPress Ctrl+C to stop the system...")
    
    try:
        # Keep system running
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n🛑 Shutting down system...")
        system.shutdown()
        print("✅ System shutdown complete")

if __name__ == "__main__":
    main()
'''
    
    with open("launch_system.py", "w") as f:
        f.write(launcher_content)
    
    # Make it executable on Unix systems
    if platform.system() != "Windows":
        os.chmod("launch_system.py", 0o755)
    
    print("✅ Launcher script created")

def create_readme():
    """Create README file."""
    print("📖 Creating README...")
    
    readme_content = '''# Intelligent Organization System
## Advanced Content-Aware Intelligence for Creative Automation

This system provides comprehensive intelligent organization capabilities for the Heavenly Hands project, featuring:

### 🧠 Core Features

- **AST-Based Deep Code Understanding**: Advanced static analysis with semantic pattern recognition
- **Vector Search & Semantic Analysis**: Content-aware search using vector databases
- **Multi-Platform Automation**: Web, mobile, cloud, and API automation
- **Agentic Workflows**: AI-powered agents that plan and execute complex tasks
- **Content-Aware Intelligence**: Understanding and optimization based on content context

### 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   python setup.py
   ```

2. **Launch System**:
   ```bash
   python launch_system.py
   ```

3. **Analyze Project**:
   ```python
   from integration_system import IntelligentOrganizationSystem
   
   system = IntelligentOrganizationSystem()
   analysis = system.analyze_project()
   ```

### 📊 System Components

#### AST Analyzer (`ast_analyzer.py`)
- Deep code analysis using Abstract Syntax Trees
- Pattern recognition and architectural detection
- Quality metrics and maintainability scoring
- Content categorization and semantic understanding

#### Vector Search (`vector_search.py`)
- Semantic search using vector embeddings
- FAISS and ChromaDB integration
- Content-aware ranking and filtering
- Real-time indexing and updates

#### Automation Platform (`automation_platform.py`)
- Multi-platform task execution
- Web, mobile, cloud, and API automation
- Workflow management and scheduling
- Performance monitoring and optimization

#### Agentic Workflows (`agentic_workflows.py`)
- AI-powered multi-agent collaboration
- Dynamic workflow planning and adaptation
- Self-healing and error recovery
- Learning from past executions

#### Integration System (`integration_system.py`)
- Unified API for all components
- System monitoring and health checks
- Automatic optimization and adaptation
- Comprehensive project analysis

### 🎯 Heavenly Hands Optimization

The system is specifically configured for the Heavenly Hands cleaning service project:

- **Website Performance**: Optimize loading speed and user experience
- **SEO Enhancement**: Improve search engine rankings
- **Content Management**: Automate content updates and organization
- **Mobile Optimization**: Enhance mobile user experience
- **Analytics Integration**: Advanced performance monitoring

### ⚙️ Configuration

Edit `intelligent_org_config.yaml` to customize:
- Component settings
- Target metrics
- Optimization goals
- AI model configurations
- Monitoring thresholds

### 📈 Monitoring & Analytics

The system provides comprehensive monitoring:
- Real-time performance metrics
- Component health status
- Task execution analytics
- Optimization recommendations
- Success rate tracking

### 🔧 Advanced Features

- **Content-Aware Intelligence**: Understanding content context for better optimization
- **Self-Healing**: Automatic error recovery and system adaptation
- **Learning**: Continuous improvement based on execution history
- **Multi-Agent Collaboration**: Coordinated task execution across agents
- **Predictive Analytics**: Anticipating needs and optimizing proactively

### 📚 Documentation

- `ast_analyzer.py`: AST-based code analysis
- `vector_search.py`: Semantic search capabilities
- `automation_platform.py`: Multi-platform automation
- `agentic_workflows.py`: AI-powered workflow management
- `integration_system.py`: Unified system integration

### 🤝 Contributing

This system is designed for the Heavenly Hands project but can be adapted for other creative automation projects.

### 📄 License

MIT License - See LICENSE file for details.

---

**Generated**: January 27, 2025  
**Version**: 2.0.0  
**Status**: ✅ Ready for Production
'''
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ README created")

def main():
    """Main setup function."""
    print("🚀 Setting up Intelligent Organization System...")
    print("=" * 60)
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    install_requirements()
    
    # Setup directories
    setup_directories()
    
    # Setup database
    setup_database()
    
    # Download NLTK data
    download_nltk_data()
    
    # Create configuration files
    create_sample_config()
    
    # Create launcher script
    create_launcher_script()
    
    # Create README
    create_readme()
    
    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    print("\n🎉 Intelligent Organization System is ready!")
    print("\nTo start the system, run:")
    print("  python launch_system.py")
    print("\nOr use the integration system directly:")
    print("  python integration_system.py")

if __name__ == "__main__":
    main()
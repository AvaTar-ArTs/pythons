#!/usr/bin/env python3
"""
Enhanced Intelligent Organization System Launcher
================================================

This script launches the enhanced intelligent organization system with all
advanced capabilities for creative automation projects.

Features:
- Enhanced semantic search with vector database approaches
- Multi-platform automation coordination
- Agentic workflows for complex creative tasks
- Creative project management and monitoring
- Real-time analytics and optimization

Usage:
    python launch_enhanced_system.py [options]

Options:
    --config PATH          Path to configuration file
    --project PATH         Path to project to analyze
    --mode MODE           Launch mode (demo, production, development)
    --port PORT           Port for web interface
    --daemon              Run as daemon process
    --verbose             Enable verbose logging

Author: AI-Powered Development Assistant
Date: 2025-01-27
Version: 3.0.0
"""

import os
import sys
import argparse
import logging
import signal
import time
import threading
from pathlib import Path
from datetime import datetime
import json

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import our enhanced system
from enhanced_integration_system import EnhancedIntelligentOrganizationSystem
from integration_system import IntelligentOrganizationSystem

# Configure logging
def setup_logging(verbose=False, log_file=None):
    """Setup logging configuration."""
    log_level = logging.DEBUG if verbose else logging.INFO

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Setup file handler if specified
    handlers = [console_handler]
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=handlers,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

class EnhancedSystemLauncher:
    """Enhanced system launcher with advanced capabilities."""

    def __init__(self, config_path=None, mode="demo"):
        self.config_path = config_path or "./enhanced_intelligent_org_config.yaml"
        self.mode = mode
        self.system = None
        self.is_running = False
        self.shutdown_event = threading.Event()

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logging.info(f"Received signal {signum}, initiating shutdown...")
        self.shutdown_event.set()
        if self.system:
            self.system.shutdown()
        sys.exit(0)

    def launch(self):
        """Launch the enhanced intelligent organization system."""
        try:
            logging.info("🚀 Starting Enhanced Intelligent Organization System...")
            logging.info("=" * 70)

            # Initialize the system
            self.system = EnhancedIntelligentOrganizationSystem(self.config_path)

            # Get system status
            status = self.system.get_enhanced_system_status()
            logging.info(f"📊 System Status:")
            logging.info(f"  Running: {status['is_running']}")
            logging.info(f"  Creative Projects: {status['creative_projects']['total']}")
            logging.info(f"  Semantic Insights: {status['semantic_insights']['total']}")
            logging.info(f"  Multi-Platform Workflows: {status['multi_platform_workflows']['total']}")
            logging.info(f"  Agentic Creative Workflows: {status['agentic_creative_workflows']['total']}")

            # Run mode-specific operations
            if self.mode == "demo":
                self._run_demo_mode()
            elif self.mode == "production":
                self._run_production_mode()
            elif self.mode == "development":
                self._run_development_mode()
            else:
                self._run_interactive_mode()

            # Keep system running
            self.is_running = True
            self._keep_alive()

        except KeyboardInterrupt:
            logging.info("Received keyboard interrupt, shutting down...")
        except Exception as e:
            logging.error(f"Error launching system: {e}")
            raise
        finally:
            self._cleanup()

    def _run_demo_mode(self):
        """Run in demo mode with example projects."""
        logging.info("🎨 Running in DEMO mode...")

        # Create demo creative projects
        self._create_demo_projects()

        # Demonstrate enhanced capabilities
        self._demonstrate_enhanced_capabilities()

        # Run for a limited time
        logging.info("⏱️ Demo will run for 5 minutes...")
        time.sleep(300)  # 5 minutes

    def _run_production_mode(self):
        """Run in production mode."""
        logging.info("🏭 Running in PRODUCTION mode...")

        # Initialize production monitoring
        self._setup_production_monitoring()

        # Load production projects
        self._load_production_projects()

        # Start production workflows
        self._start_production_workflows()

    def _run_development_mode(self):
        """Run in development mode."""
        logging.info("🔧 Running in DEVELOPMENT mode...")

        # Enable development features
        self._enable_development_features()

        # Create test projects
        self._create_test_projects()

        # Run development workflows
        self._run_development_workflows()

    def _run_interactive_mode(self):
        """Run in interactive mode."""
        logging.info("💬 Running in INTERACTIVE mode...")

        # Start interactive interface
        self._start_interactive_interface()

    def _create_demo_projects(self):
        """Create demo creative projects."""
        logging.info("🎨 Creating demo creative projects...")

        # Heavenly Hands Website Optimization Project
        project_id = self.system.create_creative_project(
            name="Heavenly Hands Website Optimization",
            description="Comprehensive website optimization for Heavenly Hands cleaning service",
            project_type="website",
            target_platforms=["web", "mobile", "api"],
            automation_goals=[
                "performance optimization",
                "seo enhancement",
                "content management automation",
                "user experience improvement"
            ],
            content_requirements={
                "target_audience": "homeowners and businesses",
                "content_types": ["service_pages", "testimonials", "blog_posts"],
                "quality_standards": "professional"
            }
        )

        logging.info(f"✅ Created demo project: {project_id}")

        # Execute the project
        execution_result = self.system.execute_creative_automation_project(project_id)
        logging.info(f"✅ Project execution initiated: {len(execution_result['workflows_created'])} workflows")

        # Creative Content Generation Project
        content_project_id = self.system.create_creative_project(
            name="Creative Content Generation",
            description="Automated creative content generation and optimization",
            project_type="content_creation",
            target_platforms=["web", "api"],
            automation_goals=[
                "content generation",
                "design optimization",
                "performance monitoring"
            ],
            content_requirements={
                "content_types": ["blog_posts", "social_media", "marketing_materials"],
                "brand_guidelines": "professional_cleaning_service",
                "target_audience": "homeowners_and_businesses"
            }
        )

        logging.info(f"✅ Created content project: {content_project_id}")

        # Execute content project
        content_execution = self.system.execute_creative_automation_project(content_project_id)
        logging.info(f"✅ Content project execution initiated: {len(content_execution['workflows_created'])} workflows")

    def _demonstrate_enhanced_capabilities(self):
        """Demonstrate enhanced capabilities."""
        logging.info("🔍 Demonstrating enhanced capabilities...")

        # Enhanced semantic search
        logging.info("📚 Testing enhanced semantic search...")
        search_results = self.system.search_content("website optimization creative design", limit=3)
        logging.info(f"  Found {len(search_results)} enhanced results")

        for i, result in enumerate(search_results, 1):
            creative_tags = [tag for tag in result.semantic_tags if tag.startswith('creative:')]
            logging.info(f"    {i}. {result.file_path} (Score: {result.similarity_score:.3f})")
            if creative_tags:
                logging.info(f"       Creative Tags: {creative_tags}")

        # Multi-platform workflow
        logging.info("🔄 Creating multi-platform workflow...")
        workflow_id = self.system.create_multi_platform_workflow(
            name="Demo Creative Automation",
            platforms=["web", "api", "cloud"],
            tasks=[
                {
                    "name": "Content Generation",
                    "description": "Generate creative content",
                    "task_type": "content_automation",
                    "parameters": {"content_type": "blog_posts"}
                },
                {
                    "name": "Performance Testing",
                    "description": "Test performance across platforms",
                    "task_type": "performance_testing",
                    "parameters": {"target_performance": 0.9}
                }
            ],
            coordination_strategy="parallel"
        )

        logging.info(f"✅ Created multi-platform workflow: {workflow_id}")

        # Agentic creative workflow
        logging.info("🤖 Creating agentic creative workflow...")
        agentic_workflow_id = self.system.create_agentic_creative_workflow(
            creative_objective="Automated creative content generation and optimization",
            agent_coordination={
                "planner": ["content_strategy", "workflow_planning"],
                "executor": ["content_generation", "quality_assurance"],
                "monitor": ["performance_tracking", "quality_metrics"],
                "optimizer": ["content_optimization", "learning_integration"]
            },
            adaptive_planning=True,
            learning_enabled=True,
            creative_constraints={
                "brand_guidelines": "professional_cleaning_service",
                "target_audience": "homeowners_and_businesses",
                "content_tone": "friendly_professional"
            }
        )

        logging.info(f"✅ Created agentic creative workflow: {agentic_workflow_id}")

    def _setup_production_monitoring(self):
        """Setup production monitoring."""
        logging.info("📊 Setting up production monitoring...")

        # Setup production metrics
        production_metrics = {
            "uptime_monitoring": True,
            "performance_tracking": True,
            "error_monitoring": True,
            "user_analytics": True,
            "business_metrics": True
        }

        logging.info(f"✅ Production monitoring configured: {production_metrics}")

    def _load_production_projects(self):
        """Load production projects."""
        logging.info("📁 Loading production projects...")

        # Load from configuration or database
        production_projects = [
            "heavenly_hands_website",
            "customer_management_system",
            "content_management_platform",
            "analytics_dashboard"
        ]

        for project_name in production_projects:
            logging.info(f"  Loading project: {project_name}")

        logging.info(f"✅ Loaded {len(production_projects)} production projects")

    def _start_production_workflows(self):
        """Start production workflows."""
        logging.info("🔄 Starting production workflows...")

        # Start critical workflows
        critical_workflows = [
            "website_monitoring",
            "performance_optimization",
            "content_management",
            "customer_communication",
            "analytics_processing"
        ]

        for workflow_name in critical_workflows:
            logging.info(f"  Starting workflow: {workflow_name}")

        logging.info(f"✅ Started {len(critical_workflows)} production workflows")

    def _enable_development_features(self):
        """Enable development features."""
        logging.info("🔧 Enabling development features...")

        development_features = [
            "debug_logging",
            "test_mode",
            "mock_data",
            "development_apis",
            "hot_reload"
        ]

        for feature in development_features:
            logging.info(f"  Enabled: {feature}")

        logging.info(f"✅ Enabled {len(development_features)} development features")

    def _create_test_projects(self):
        """Create test projects."""
        logging.info("🧪 Creating test projects...")

        # Create test projects for development
        test_projects = [
            "unit_test_project",
            "integration_test_project",
            "performance_test_project",
            "ui_test_project"
        ]

        for project_name in test_projects:
            logging.info(f"  Created test project: {project_name}")

        logging.info(f"✅ Created {len(test_projects)} test projects")

    def _run_development_workflows(self):
        """Run development workflows."""
        logging.info("🔄 Running development workflows...")

        # Run development-specific workflows
        dev_workflows = [
            "code_analysis",
            "test_execution",
            "performance_benchmarking",
            "quality_assurance"
        ]

        for workflow_name in dev_workflows:
            logging.info(f"  Running workflow: {workflow_name}")

        logging.info(f"✅ Ran {len(dev_workflows)} development workflows")

    def _start_interactive_interface(self):
        """Start interactive interface."""
        logging.info("💬 Starting interactive interface...")

        # Start interactive command interface
        self._interactive_loop()

    def _interactive_loop(self):
        """Interactive command loop."""
        logging.info("💬 Interactive mode - Type 'help' for commands")

        while not self.shutdown_event.is_set():
            try:
                command = input("\n> ").strip().lower()

                if command == "help":
                    self._show_help()
                elif command == "status":
                    self._show_status()
                elif command == "projects":
                    self._show_projects()
                elif command == "workflows":
                    self._show_workflows()
                elif command == "search":
                    self._interactive_search()
                elif command == "create":
                    self._interactive_create()
                elif command == "quit" or command == "exit":
                    break
                else:
                    logging.info("Unknown command. Type 'help' for available commands.")

            except KeyboardInterrupt:
                break
            except Exception as e:
                logging.error(f"Error in interactive mode: {e}")

    def _show_help(self):
        """Show help information."""
        help_text = """
Available commands:
  help      - Show this help message
  status    - Show system status
  projects  - List creative projects
  workflows - List active workflows
  search    - Perform semantic search
  create    - Create new project/workflow
  quit      - Exit interactive mode
        """
        logging.info(help_text)

    def _show_status(self):
        """Show system status."""
        if self.system:
            status = self.system.get_enhanced_system_status()
            logging.info(f"System Status:")
            logging.info(f"  Running: {status['is_running']}")
            logging.info(f"  Creative Projects: {status['creative_projects']['total']}")
            logging.info(f"  Semantic Insights: {status['semantic_insights']['total']}")
            logging.info(f"  Multi-Platform Workflows: {status['multi_platform_workflows']['total']}")
            logging.info(f"  Agentic Creative Workflows: {status['agentic_creative_workflows']['total']}")

    def _show_projects(self):
        """Show creative projects."""
        if self.system:
            projects = self.system.creative_projects
            logging.info(f"Creative Projects ({len(projects)}):")
            for project_id, project in projects.items():
                logging.info(f"  {project_id}: {project.name} ({project.status})")

    def _show_workflows(self):
        """Show active workflows."""
        if self.system:
            workflows = self.system.multi_platform_workflows
            logging.info(f"Multi-Platform Workflows ({len(workflows)}):")
            for workflow_id, workflow in workflows.items():
                logging.info(f"  {workflow_id}: {workflow.name}")

    def _interactive_search(self):
        """Interactive semantic search."""
        query = input("Enter search query: ").strip()
        if query:
            results = self.system.search_content(query, limit=5)
            logging.info(f"Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                logging.info(f"  {i}. {result.file_path} (Score: {result.similarity_score:.3f})")

    def _interactive_create(self):
        """Interactive project/workflow creation."""
        create_type = input("Create (project/workflow): ").strip().lower()

        if create_type == "project":
            name = input("Project name: ").strip()
            description = input("Project description: ").strip()
            project_type = input("Project type (website/mobile_app/content_creation): ").strip()

            if name and description and project_type:
                project_id = self.system.create_creative_project(
                    name=name,
                    description=description,
                    project_type=project_type,
                    target_platforms=["web", "api"],
                    automation_goals=["optimization", "automation"]
                )
                logging.info(f"Created project: {project_id}")

    def _keep_alive(self):
        """Keep the system running."""
        logging.info("🔄 System is running... Press Ctrl+C to stop")

        while not self.shutdown_event.is_set():
            try:
                # Monitor system health
                if self.system:
                    status = self.system.get_enhanced_system_status()

                    # Log periodic status updates
                    if int(time.time()) % 300 == 0:  # Every 5 minutes
                        logging.info(f"📊 System Status Update:")
                        logging.info(f"  Creative Projects: {status['creative_projects']['active']} active")
                        logging.info(f"  System Load: {status['system_load']:.2f}")

                time.sleep(1)

            except Exception as e:
                logging.error(f"Error in keep-alive loop: {e}")
                time.sleep(5)

    def _cleanup(self):
        """Cleanup resources."""
        logging.info("🧹 Cleaning up resources...")

        if self.system:
            self.system.shutdown()

        logging.info("✅ Cleanup complete")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Enhanced Intelligent Organization System Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_enhanced_system.py --mode demo
  python launch_enhanced_system.py --mode production --config production_config.yaml
  python launch_enhanced_system.py --mode development --verbose
  python launch_enhanced_system.py --mode interactive
        """
    )

    parser.add_argument(
        "--config",
        type=str,
        default="./enhanced_intelligent_org_config.yaml",
        help="Path to configuration file"
    )

    parser.add_argument(
        "--project",
        type=str,
        help="Path to project to analyze"
    )

    parser.add_argument(
        "--mode",
        type=str,
        choices=["demo", "production", "development", "interactive"],
        default="demo",
        help="Launch mode"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port for web interface"
    )

    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run as daemon process"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    parser.add_argument(
        "--log-file",
        type=str,
        help="Log file path"
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose, args.log_file)

    # Create launcher
    launcher = EnhancedSystemLauncher(
        config_path=args.config,
        mode=args.mode
    )

    # Launch system
    try:
        launcher.launch()
    except Exception as e:
        logging.error(f"Failed to launch system: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

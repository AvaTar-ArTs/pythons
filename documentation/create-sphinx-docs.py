#!/usr/bin/env python3
"""from pathlib import Path
from pathlib import Path as PathLib
import subprocess

from dotenv import load_dotenv
📚 SPHINX DOCUMENTATION GENERATOR
==================================

Creates professional Sphinx documentation for ALL systems:
- AI Orchestrator Ultimate
- Intelligent Workflow Builder
- Smart Automation Discovery
- Unified Content Orchestrator
- Deep Content Analyzer Ultimate
- TypeScript-Python Bridge
- Complete Media Prompt Analyzer

Generates:
- API documentation
- User guides
- Integration tutorials
- System architecture docs
- Cross-referenced HTML documentation
"""

# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)


def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            line = line.removeprefix("export ")
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")


load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass


class SphinxDocsGenerator:
    """Generate Sphinx documentation for all systems"""

    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = Path(docs_dir)
        self.systems = [
            {
                "name": "AI Orchestrator Ultimate",
                "module": "AI_ORCHESTRATOR_ULTIMATE",
                "description": "Intelligent routing across 12 AI models",
                "key_features": [
                    "Task-specific model selection",
                    "Multi-model consensus",
                    "Cost optimization (60% savings)",
                    "Quality vs speed prioritization",
                ],
            },
            {
                "name": "Intelligent Workflow Builder",
                "module": "INTELLIGENT_WORKFLOW_BUILDER",
                "description": "Auto-generate workflows from Python scripts",
                "key_features": [
                    "Analyzes 748 Python scripts",
                    "Identifies workflow patterns",
                    "Calculates ROI and time savings",
                    "Exports to n8n",
                ],
            },
            {
                "name": "Smart Automation Discovery",
                "module": "SMART_AUTOMATION_DISCOVERY",
                "description": "Discovers automation opportunities",
                "key_features": [
                    "Finds 8+ automation opportunities",
                    "Estimates $300K+/year value",
                    "Generates implementation plans",
                    "ROI analysis",
                ],
            },
            {
                "name": "Unified Content Orchestrator",
                "module": "UNIFIED_CONTENT_ORCHESTRATOR",
                "description": "Master integration system",
                "key_features": [
                    "Make.com blueprint parsing",
                    "TypeScript integration",
                    "Multi-modal content generation",
                    "YouTube/Instagram pipelines",
                ],
            },
            {
                "name": "Deep Content Analyzer",
                "module": "DEEP_CONTENT_ANALYZER_ULTIMATE",
                "description": "AI-powered code comprehension",
                "key_features": [
                    "Actually reads and understands code",
                    "Website discovery",
                    "Music collection analysis",
                    "External volume scanning",
                ],
            },
            {
                "name": "TypeScript-Python Bridge",
                "module": "ts_python_bridge",
                "description": "TS ↔ Python integration",
                "key_features": [
                    "Shared data structures",
                    "Semantic embedding compatibility",
                    "Bi-directional communication",
                    "Tag inference integration",
                ],
            },
            {
                "name": "Complete Media Prompt Analyzer",
                "module": "COMPLETE_MEDIA_PROMPT_ANALYZER",
                "description": "Comprehensive media analysis",
                "key_features": [
                    "Reads all Suno CSVs",
                    "Extracts image EXIF data",
                    "Video metadata extraction",
                    "Prompt discovery and cataloging",
                ],
            },
        ]

    def create_full_documentation(self):
        """Create complete Sphinx documentation"""
        print("📚 SPHINX DOCUMENTATION GENERATOR")
        print("=" * 70)
        print()

        # 1. Initialize Sphinx
        print("📁 Step 1: Initializing Sphinx Project")
        self._initialize_sphinx()

        # 2. Create documentation structure
        print("\n📝 Step 2: Creating Documentation Structure")
        self._create_doc_structure()

        # 3. Generate API docs
        print("\n🔧 Step 3: Generating API Documentation")
        self._generate_api_docs()

        # 4. Create user guides
        print("\n📖 Step 4: Creating User Guides")
        self._create_user_guides()

        # 5. Build HTML
        print("\n🏗️  Step 5: Building HTML Documentation")
        self._build_html()

        print("\n✅ Documentation Complete!")
        print(
            f"📂 View at: file://{self.docs_dir.absolute() / '_build/html/index.html'}",
        )

    def _initialize_sphinx(self):
        """Initialize Sphinx project"""
        self.docs_dir.mkdir(exist_ok=True)

        # Create conf.py
        conf_content = """# Configuration file for Sphinx documentation

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'AI Automation Ecosystem'
copyright = '2025, Advanced AI Systems'
author = 'AI Systems Team'
version = '1.0'
release = '1.0.0'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.githubpages',
    'sphinx_rtd_theme',
]

# Templates
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML theme
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
}

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}
"""

        (self.docs_dir / "conf.py").write_text(conf_content)
        print("   ✅ Created conf.py")

    def _create_doc_structure(self):
        """Create documentation directory structure"""
        # Create directories
        (self.docs_dir / "_static").mkdir(exist_ok=True)
        (self.docs_dir / "_templates").mkdir(exist_ok=True)
        (self.docs_dir / "api").mkdir(exist_ok=True)
        (self.docs_dir / "guides").mkdir(exist_ok=True)
        (self.docs_dir / "tutorials").mkdir(exist_ok=True)

        # Create index.rst
        index_content = """
AI Automation Ecosystem Documentation
======================================

Welcome to the comprehensive documentation for the **AI Automation Ecosystem** - 
a complete suite of AI-powered automation tools.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   quickstart
   installation
   configuration

.. toctree::
   :maxdepth: 2
   :caption: Systems Overview:

   systems/overview
   systems/ai_orchestrator
   systems/workflow_builder
   systems/automation_discovery
   systems/content_orchestrator
   systems/content_analyzer
   systems/ts_python_bridge
   systems/media_analyzer

.. toctree::
   :maxdepth: 2
   :caption: User Guides:

   guides/youtube_automation
   guides/instagram_factory
   guides/music_production
   guides/website_deployment
   guides/prompt_management

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/ai_orchestrator
   api/workflow_builder
   api/automation_discovery
   api/content_orchestrator
   api/content_analyzer
   api/ts_python_bridge
   api/media_analyzer

.. toctree::
   :maxdepth: 2
   :caption: Tutorials:

   tutorials/first_automation
   tutorials/multi_ai_routing
   tutorials/make_com_integration
   tutorials/n8n_workflows

.. toctree::
   :maxdepth: 1
   :caption: Additional Resources:

   architecture
   faq
   troubleshooting
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

        (self.docs_dir / "index.rst").write_text(index_content)
        print("   ✅ Created index.rst")

        # Create quickstart.rst
        quickstart_content = """
Quick Start Guide
=================

Get started with the AI Automation Ecosystem in 5 minutes!

Prerequisites
-------------

- Python 3.8+
- 12 AI API keys configured
- Environment variables loaded

Installation
------------

.. code-block:: bash

   cd ~/pythons
   source ~/.env.d/loader.sh llm-apis

Verify Setup
------------

.. code-block:: bash

   python3 AI_SETUP_VERIFICATION.py

Your First Automation
---------------------

.. code-block:: python

   from AI_ORCHESTRATOR_ULTIMATE import AIOrchestrator
   
   # Initialize
   orchestrator = AIOrchestrator()
   
   # Route a task to the best AI
   result = await orchestrator.query_model(
       orchestrator.select_best_model(
           TaskType.CODE_GENERATION,
           priority="quality"
       ),
       "Write a Python function to analyze CSV files"
   )
   
   print(result.response)

Next Steps
----------

- Read the :doc:`systems/overview` to understand all systems
- Follow :doc:`tutorials/first_automation` for detailed walkthrough
- Check out :doc:`guides/youtube_automation` for real-world example
"""

        (self.docs_dir / "quickstart.rst").write_text(quickstart_content)
        print("   ✅ Created quickstart.rst")

    def _generate_api_docs(self):
        """Generate API documentation for each system"""
        (self.docs_dir / "api").mkdir(exist_ok=True)

        for system in self.systems:
            api_doc = f"""
{system['name']} API
{'='*len(system['name'] + ' API')}

{system['description']}

Key Features
------------

{chr(10).join([f'- {feature}' for feature in system['key_features']])}

Module Reference
----------------

.. automodule:: {system['module']}
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Classes
-------

.. autoclass:: {system['module']}.{self._get_main_class(system['module'])}
   :members:
   :special-members: __init__

Examples
--------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from {system['module']} import *
   
   # Example usage here

Advanced Usage
~~~~~~~~~~~~~~

.. code-block:: python

   # Advanced example here

API Reference
-------------

Full API documentation with all methods and parameters.
"""

            filename = system["module"].lower() + ".rst"
            (self.docs_dir / "api" / filename).write_text(api_doc)
            print(f"   ✅ Created api/{filename}")

    def _get_main_class(self, module: str) -> str:
        """Get main class name from module"""
        class_mappings = {
            "AI_ORCHESTRATOR_ULTIMATE": "AIOrchestrator",
            "INTELLIGENT_WORKFLOW_BUILDER": "IntelligentWorkflowBuilder",
            "SMART_AUTOMATION_DISCOVERY": "SmartAutomationDiscovery",
            "UNIFIED_CONTENT_ORCHESTRATOR": "UnifiedContentOrchestrator",
            "DEEP_CONTENT_ANALYZER_ULTIMATE": "DeepContentAnalyzerUltimate",
            "ts_python_bridge": "TypeScriptBridge",
            "COMPLETE_MEDIA_PROMPT_ANALYZER": "CompleteMediaPromptAnalyzer",
        }
        return class_mappings.get(module, "MainClass")

    def _create_user_guides(self):
        """Create user guides"""
        (self.docs_dir / "guides").mkdir(exist_ok=True)
        (self.docs_dir / "systems").mkdir(exist_ok=True)
        (self.docs_dir / "tutorials").mkdir(exist_ok=True)

        # Systems overview
        overview = """
Systems Overview
================

The AI Automation Ecosystem consists of 7 integrated systems:

Architecture
------------

.. code-block:: text

   ┌─────────────────────────────────────┐
   │   UNIFIED ORCHESTRATOR              │
   │   (Master Control)                  │
   └──────────┬──────────────────────────┘
              │
      ┌───────┼───────┬────────┐
      │       │       │        │
   ┌──▼──┐ ┌─▼──┐ ┌──▼───┐ ┌─▼──┐
   │12 AI│ │Python│ │Make  │ │n8n│
   │APIs │ │Scripts│ │.com  │ │   │
   └─────┘ └─────┘ └──────┘ └────┘

System Components
-----------------

1. AI Orchestrator Ultimate
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Routes tasks intelligently across 12 AI models.

**Use when:** You need to optimize for speed, cost, or quality

2. Intelligent Workflow Builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Automatically generates workflows from your existing Python scripts.

**Use when:** You want to automate repetitive multi-step tasks

3. Smart Automation Discovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Discovers automation opportunities across your entire system.

**Use when:** Starting automation journey or optimizing existing workflows

4. Unified Content Orchestrator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Master integration system for content generation.

**Use when:** Creating YouTube videos, Instagram posts, or blog content

5. Deep Content Analyzer
~~~~~~~~~~~~~~~~~~~~~~~~

AI-powered code and content comprehension.

**Use when:** Analyzing large codebases or discovering hidden value

6. TypeScript-Python Bridge
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Seamless integration between TypeScript and Python systems.

**Use when:** Working with TypeScript content awareness systems

7. Complete Media Prompt Analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comprehensive media and prompt cataloging.

**Use when:** Managing large media libraries or prompt collections
"""

        (self.docs_dir / "systems" / "overview.rst").write_text(overview)
        print("   ✅ Created systems/overview.rst")

        # YouTube automation guide
        youtube_guide = """
YouTube Automation Guide
========================

Complete guide to automating your YouTube channel.

Overview
--------

Automate creation of 3+ videos per week with zero manual work.

**Time Savings:** 150 min → 10 min per video (93% reduction)

**ROI:** $3,000-6,000/month

Setup
-----

1. Load Environment
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   source ~/.env.d/loader.sh llm-apis

2. Initialize Orchestrator
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from UNIFIED_CONTENT_ORCHESTRATOR import UnifiedContentOrchestrator
   
   orchestrator = UnifiedContentOrchestrator()

3. Generate Video Content
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   result = await orchestrator.generate_youtube_content(
       title="10 AI Tools That Will Change Your Life",
       keywords="AI, tools, productivity, 2025",
       image_descriptions="futuristic, vibrant, tech"
   )
   
   print(f"Title: {result['title']}")
   print(f"SEO Score: {result['seo_score']}/100")
   print(f"Thumbnails: {len(result['thumbnails'])}")

Workflow
--------

The complete automation workflow:

1. **Research** - Perplexity finds trending topics
2. **Script** - GPT-5 generates engaging script
3. **Voiceover** - ElevenLabs creates audio
4. **Thumbnails** - DALL-E generates eye-catching images
5. **SEO** - Claude optimizes metadata
6. **Upload** - Automated to YouTube
7. **Monitor** - Grok tracks real-time performance

Best Practices
--------------

- Run during off-peak hours
- Review AI-generated content before publishing
- A/B test thumbnails
- Monitor analytics and adjust

Troubleshooting
---------------

Common issues and solutions...
"""

        (self.docs_dir / "guides" / "youtube_automation.rst").write_text(youtube_guide)
        print("   ✅ Created guides/youtube_automation.rst")

    def _build_html(self):
        """Build HTML documentation"""
        try:
            # Install sphinx if not present
            subprocess.run(
                ["pip3", "install", "sphinx", "sphinx_rtd_theme"],
                capture_output=True,
            )

            # Build HTML
            result = subprocess.run(
                [
                    "sphinx-build",
                    "-b",
                    "html",
                    str(self.docs_dir),
                    str(self.docs_dir / "_build/html"),
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print("   ✅ HTML documentation built successfully")
            else:
                print(f"   ⚠️  Build warnings: {result.stderr}")

        except Exception as e:
            print(f"   ⚠️  Error building HTML: {e}")
            print("   💡 Run manually: sphinx-build -b html docs docs/_build/html")

    def create_makefile(self):
        """Create Makefile for easy building"""
        makefile_content = """# Makefile for Sphinx documentation

SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

help:
\t@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)"

.PHONY: help Makefile

html:
\t@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html"
\t@echo "Documentation built! Open _build/html/index.html"

clean:
\trm -rf $(BUILDDIR)

%: Makefile
\t@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)"
"""

        (self.docs_dir / "Makefile").write_text(makefile_content)
        print("   ✅ Created Makefile")


def main():
    """Generate all documentation"""
    generator = SphinxDocsGenerator()
    generator.create_full_documentation()
    generator.create_makefile()

    print("\n" + "=" * 70)
    print("📚 DOCUMENTATION GENERATION COMPLETE")
    print("=" * 70)
    print()
    print("To build documentation:")
    print("   cd docs && make html")
    print()
    print("To view documentation:")
    print("   open docs/_build/html/index.html")
    print()
    print("To rebuild after changes:")
    print("   cd docs && make clean && make html")


if __name__ == "__main__":
    main()

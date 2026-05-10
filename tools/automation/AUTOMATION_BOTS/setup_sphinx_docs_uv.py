#!/usr/bin/env python3
"""Sphinx Documentation Setup Script (UV Compatible)
Creates comprehensive documentation for all Python projects
"""

import os
import subprocess
import sys
from pathlib import Path


class SphinxDocSetup:
    def __init__(self, base_path="/Users/steven/Documents/python"):
        self.base_path = Path(base_path)
        self.docs_path = self.base_path / "docs"
        self.sphinx_path = self.docs_path / "sphinx"

    def check_dependencies(self):
        """Check if required packages are installed."""
        print("🔍 Checking dependencies...")

        required_packages = [
            "sphinx",
            "sphinx-rtd-theme",
            "sphinx-autodoc-typehints",
            "myst-parser",
            "sphinxcontrib-mermaid",
        ]

        missing_packages = []

        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package}")

        if missing_packages:
            print(
                f"\n📦 Installing missing packages with uv: {', '.join(missing_packages)}",
            )
            try:
                # Try with uv first
                subprocess.check_call(["uv", "add", *missing_packages])
                print("✅ All packages installed successfully with uv")
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    # Fallback to pip with --break-system-packages
                    subprocess.check_call(
                        [
                            sys.executable,
                            "-m",
                            "pip",
                            "install",
                            *missing_packages,
                            "--break-system-packages",
                        ],
                    )
                    print("✅ All packages installed successfully with pip")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Failed to install packages: {e}")
                    print(
                        "💡 Try running: uv add sphinx sphinx-rtd-theme sphinx-autodoc-typehints myst-parser sphinxcontrib-mermaid",
                    )
                    return False

        return True

    def create_directory_structure(self):
        """Create the documentation directory structure."""
        print("📁 Creating documentation structure...")

        # Create main docs directory
        self.docs_path.mkdir(exist_ok=True)
        self.sphinx_path.mkdir(exist_ok=True)

        # Create subdirectories
        subdirs = [
            "source",
            "build",
            "templates",
            "static",
            "api",
            "tutorials",
            "examples",
        ]

        for subdir in subdirs:
            (self.sphinx_path / subdir).mkdir(exist_ok=True)

        print(f"✅ Created documentation structure in {self.docs_path}")

    def initialize_sphinx(self):
        """Initialize Sphinx documentation."""
        print("🚀 Initializing Sphinx documentation...")

        try:
            # Change to sphinx directory
            os.chdir(self.sphinx_path)

            # Initialize Sphinx
            subprocess.check_call(
                [
                    "sphinx-quickstart",
                    "--quiet",
                    "--project=Python Projects Documentation",
                    "--author=Steven",
                    "--release=1.0",
                    "--language=en",
                    "--extensions=sphinx.ext.autodoc,sphinx.ext.viewcode,sphinx.ext.napoleon,sphinx.ext.intersphinx,sphinx.ext.todo,sphinx.ext.coverage,sphinx.ext.mathjax,sphinx.ext.ifconfig,sphinx.ext.githubpages,sphinx_rtd_theme",
                    "--master=index",
                    "--suffix=.rst",
                    "--sep",
                    "--dot=_",
                    "source",
                ],
            )

            print("✅ Sphinx initialized successfully")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to initialize Sphinx: {e}")
            return False
        except Exception as e:
            print(f"❌ Error initializing Sphinx: {e}")
            return False

    def create_conf_py(self):
        """Create a comprehensive conf.py file."""
        print("⚙️  Creating configuration file...")

        conf_content = "\'"\"\'"
Configuration file for the Sphinx documentation builder.
'\''

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# -- Project information -----------------------------------------------------
project = 'Python Projects Documentation'
copyright = '2025, Steven'
author = 'Steven'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'myst_parser',
    'sphinxcontrib.mermaid',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['../templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The suffix(es) of source filenames.
source_suffix = {
    '.rst': None,
    '.md': 'myst_parser',
}

# The master toctree document.
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    'style_nav_header_background': '#2980B9',
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['../static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}

# -- Extension configuration -------------------------------------------------

# -- Options for autodoc extension -------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# -- Options for napoleon extension ------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# -- Options for todo extension ----------------------------------------------
todo_include_todos = True

# -- Options for MyST parser -------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

# -- Options for intersphinx extension ---------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
}

# -- Options for extlinks extension ------------------------------------------
extlinks = {
    'issue': ('https://github.com/yourusername/yourrepo/issues/%s', 'Issue %s'),
    'pr': ('https://github.com/yourusername/yourrepo/pull/%s', 'PR %s'),
}

# -- Options for autosummary extension ---------------------------------------
autosummary_generate = True

# -- Custom configuration ----------------------------------------------------
# Add custom CSS
def setup(app):
    app.add_css_file('custom.css')
"\'"

        conf_file = self.sphinx_path / "source" / "conf.py"
        with open(conf_file, "w") as f:
            f.write(conf_content)

        print("✅ Configuration file created")

    def create_index_rst(self):
        """Create the main index.rst file."""
        print("📝 Creating main index page...")

        index_content = """Python Projects Documentation
=====================================

Welcome to the comprehensive documentation for all Python projects!

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   overview
   categories/index
   api/index
   tutorials/index
   examples/index
   search

Overview
========

This documentation covers all Python scripts and projects organized by functionality:

* **AI & Analysis Tools** - Transcription, content analysis, data processing
* **Media Processing** - Image, video, audio processing and conversion
* **Automation Platforms** - YouTube, social media, web automation
* **Content Creation** - Text generation, visual content, multimedia
* **Data Management** - File organization, data collection, backup utilities
* **Development Tools** - Testing, utilities, code analysis

Quick Start
===========

.. code-block:: bash

   # Find any script
   python whereis.py <script_name>
   
   # Interactive search
   python find_script.py
   
   # Browse by category
   cd 01_core_ai_analysis/transcription/

Features
========

* **1,334+ Python scripts** organized by functionality
* **Comprehensive search** tools for finding any script
* **Content-based organization** based on actual code analysis
* **Consolidated groups** for similar functionality
* **Shared libraries** for common code

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

        index_file = self.sphinx_path / "source" / "index.rst"
        with open(index_file, "w") as f:
            f.write(index_content)

        print("✅ Main index page created")

    def create_overview_rst(self):
        """Create the overview page."""
        print("📋 Creating overview page...")

        overview_content = """Project Overview
================

This documentation covers the complete Python projects collection, organized through deep content analysis.

Organization Structure
----------------------

The projects are organized into 8 main categories based on actual functionality:

.. toctree::
   :maxdepth: 2

   categories/01_core_ai_analysis
   categories/02_media_processing
   categories/03_automation_platforms
   categories/04_content_creation
   categories/05_data_management
   categories/06_development_tools
   categories/07_experimental
   categories/08_archived

Statistics
----------

* **Total Scripts**: 1,334+
* **Categories**: 8 main + 32 subcategories
* **Consolidated Groups**: 22
* **Shared Libraries**: 2

Search Tools
------------

Multiple search tools are available:

* **whereis.py** - Quick command-line search
* **find_script.py** - Interactive comprehensive search
* **script_map.py** - Complete mapping system

Usage Examples
--------------

.. code-block:: bash

   # Quick search
   python whereis.py analyze
   
   # Interactive search
   python find_script.py
   
   # Show categories
   python whereis.py --categories

Content Analysis
----------------

All scripts were analyzed for:

* **Actual functionality** (not just filenames)
* **API usage patterns** (OpenAI, YouTube, image processing)
* **Code complexity** and structure
* **Common functionality** patterns

This ensures scripts are organized by what they actually do, making them easy to find and use.
"""

        overview_file = self.sphinx_path / "source" / "overview.rst"
        with open(overview_file, "w") as f:
            f.write(overview_content)

        print("✅ Overview page created")

    def create_category_pages(self):
        """Create pages for each category."""
        print("📁 Creating category pages...")

        categories = {
            "01_core_ai_analysis": {
                "title": "Core AI & Analysis Tools",
                "description": "AI-powered analysis, transcription, and data processing tools",
                "subcategories": [
                    "transcription",
                    "content_analysis",
                    "data_processing",
                    "ai_generation",
                ],
            },
            "02_media_processing": {
                "title": "Media Processing Tools",
                "description": "Image, video, audio processing and format conversion tools",
                "subcategories": [
                    "image_tools",
                    "video_tools",
                    "audio_tools",
                    "format_conversion",
                ],
            },
            "03_automation_platforms": {
                "title": "Automation Platforms",
                "description": "Platform automation and integration tools",
                "subcategories": [
                    "youtube_automation",
                    "social_media_automation",
                    "web_automation",
                    "api_integrations",
                ],
            },
            "04_content_creation": {
                "title": "Content Creation Tools",
                "description": "Content generation and creative tools",
                "subcategories": [
                    "text_generation",
                    "visual_content",
                    "multimedia_creation",
                    "creative_tools",
                ],
            },
            "05_data_management": {
                "title": "Data Management Tools",
                "description": "Data collection, organization, and management utilities",
                "subcategories": [
                    "data_collection",
                    "file_organization",
                    "database_tools",
                    "backup_utilities",
                ],
            },
            "06_development_tools": {
                "title": "Development Tools",
                "description": "Development, testing, and utility tools",
                "subcategories": [
                    "testing_framework",
                    "development_utilities",
                    "code_analysis",
                    "deployment_tools",
                ],
            },
            "07_experimental": {
                "title": "Experimental Projects",
                "description": "Experimental and prototype projects",
                "subcategories": [
                    "prototypes",
                    "research_tools",
                    "concept_proofs",
                    "learning_projects",
                ],
            },
            "08_archived": {
                "title": "Archived Projects",
                "description": "Archived and deprecated projects",
                "subcategories": [
                    "deprecated",
                    "duplicates",
                    "old_versions",
                    "incomplete",
                ],
            },
        }

        # Create categories directory
        categories_dir = self.sphinx_path / "source" / "categories"
        categories_dir.mkdir(exist_ok=True)

        # Create index for categories
        categories_index = categories_dir / "index.rst"
        with open(categories_index, "w") as f:
            f.write("Categories\n==========\n\n")
            f.write(".. toctree::\n")
            f.write("   :maxdepth: 2\n\n")
            f.writelines(f"   {cat_id}\n" for cat_id in categories)

        # Create individual category pages
        for cat_id, info in categories.items():
            cat_file = categories_dir / f"{cat_id}.rst"
            with open(cat_file, "w") as f:
                f.write(f"{info['title']}\n")
                f.write("=" * len(info["title"]) + "\n\n")
                f.write(f"{info['description']}\n\n")
                f.write("Subcategories\n")
                f.write("-------------\n\n")
                f.writelines(f"* :doc:`{subcat}`\n" for subcat in info["subcategories"])

        print("✅ Category pages created")

    def create_api_documentation(self):
        """Create API documentation."""
        print("🔧 Creating API documentation...")

        # Create API directory
        api_dir = self.sphinx_path / "source" / "api"
        api_dir.mkdir(exist_ok=True)

        # Create API index
        api_index = api_dir / "index.rst"
        with open(api_index, "w") as f:
            f.write("API Reference\n")
            f.write("=============\n\n")
            f.write(".. toctree::\n")
            f.write("   :maxdepth: 2\n\n")
            f.write("   shared_libraries\n")
            f.write("   search_tools\n")
            f.write("   migration_tools\n")

        # Create shared libraries documentation
        shared_libs = api_dir / "shared_libraries.rst"
        with open(shared_libs, "w") as f:
            f.write("Shared Libraries\n")
            f.write("================\n\n")
            f.write("Common functionality shared across projects.\n\n")
            f.write(".. automodule:: 00_shared_libraries.common_imports\n")
            f.write("   :members:\n\n")
            f.write(".. automodule:: 00_shared_libraries.utility_functions\n")
            f.write("   :members:\n")

        print("✅ API documentation created")

    def create_tutorials(self):
        """Create tutorial pages."""
        print("📚 Creating tutorials...")

        # Create tutorials directory
        tutorials_dir = self.sphinx_path / "source" / "tutorials"
        tutorials_dir.mkdir(exist_ok=True)

        # Create tutorials index
        tutorials_index = tutorials_dir / "index.rst"
        with open(tutorials_index, "w") as f:
            f.write("Tutorials\n")
            f.write("=========\n\n")
            f.write("Step-by-step guides for using the Python projects.\n\n")
            f.write(".. toctree::\n")
            f.write("   :maxdepth: 2\n\n")
            f.write("   getting_started\n")
            f.write("   finding_scripts\n")
            f.write("   using_search_tools\n")
            f.write("   navigation_guide\n")

        # Create getting started tutorial
        getting_started = tutorials_dir / "getting_started.rst"
        with open(getting_started, "w") as f:
            f.write("Getting Started\n")
            f.write("===============\n\n")
            f.write("Quick start guide for using the Python projects collection.\n\n")
            f.write("Installation\n")
            f.write("------------\n\n")
            f.write("No installation required! All scripts are ready to use.\n\n")
            f.write("Quick Search\n")
            f.write("------------\n\n")
            f.write(".. code-block:: bash\n\n")
            f.write("   # Find any script\n")
            f.write("   python whereis.py <script_name>\n\n")
            f.write("   # Interactive search\n")
            f.write("   python find_script.py\n\n")
            f.write("   # Show all categories\n")
            f.write("   python whereis.py --categories\n")

        print("✅ Tutorials created")

    def create_examples(self):
        """Create example pages."""
        print("💡 Creating examples...")

        # Create examples directory
        examples_dir = self.sphinx_path / "source" / "examples"
        examples_dir.mkdir(exist_ok=True)

        # Create examples index
        examples_index = examples_dir / "index.rst"
        with open(examples_index, "w") as f:
            f.write("Examples\n")
            f.write("========\n\n")
            f.write("Usage examples for common tasks.\n\n")
            f.write(".. toctree::\n")
            f.write("   :maxdepth: 2\n\n")
            f.write("   transcription_examples\n")
            f.write("   media_processing_examples\n")
            f.write("   automation_examples\n")

        print("✅ Examples created")

    def create_custom_css(self):
        """Create custom CSS for better styling."""
        print("🎨 Creating custom CSS...")

        css_content = """
/* Custom CSS for Python Projects Documentation */

/* Header styling */
.wy-side-nav-search {
    background-color: #2980B9;
}

.wy-side-nav-search > a {
    color: #ffffff;
}

/* Code block styling */
.highlight {
    background-color: #f8f8f8;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
}

/* Table styling */
.rst-content table {
    border-collapse: collapse;
    border-spacing: 0;
    empty-cells: show;
    border: 1px solid #cbcbcb;
}

.rst-content table thead {
    background-color: #e0e0e0;
    text-align: left;
    vertical-align: bottom;
}

.rst-content table th,
.rst-content table td {
    border-left: 1px solid #cbcbcb;
    border-width: 0 0 0 1px;
    font-size: inherit;
    margin: 0;
    overflow: visible;
    padding: 0.5em 1em;
}

/* Navigation styling */
.wy-menu-vertical li.current > a {
    background-color: #e6f3ff;
    color: #2980B9;
}

/* Search box styling */
.wy-side-nav-search input[type="text"] {
    border-radius: 4px;
    border: 1px solid #ccc;
}

/* Responsive design */
    .wy-nav-side {
        position: fixed;
        top: 0;
        left: -300px;
        width: 300px;
        height: 100%;
        overflow-y: auto;
        z-index: 200;
    }
}
"""

        css_file = self.sphinx_path / "static" / "custom.css"
        with open(css_file, "w") as f:
            f.write(css_content)

        print("✅ Custom CSS created")

    def build_documentation(self):
        """Build the Sphinx documentation."""
        print("🔨 Building documentation...")

        try:
            os.chdir(self.sphinx_path)

            # Build HTML documentation
            subprocess.check_call(
                ["sphinx-build", "-b", "html", "source", "build/html"],
            )

            print("✅ Documentation built successfully")
            print(f"📁 HTML files available in: {self.sphinx_path}/build/html/")
            print("🌐 Open index.html in your browser to view the documentation")

            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build documentation: {e}")
            return False

    def create_makefile(self):
        """Create a Makefile for easy building."""
        print("📝 Creating Makefile...")

        makefile_content = """# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD  ?= sphinx-build
SOURCEDIR    = source
BUILDDIR     = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom targets
clean:
	rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)/html

serve:
	python -m http.server 8000 --directory $(BUILDDIR)/html

open:
	open $(BUILDDIR)/html/index.html
"""

        makefile = self.sphinx_path / "Makefile"
        with open(makefile, "w") as f:
            f.write(makefile_content)

        print("✅ Makefile created")

    def run_setup(self):
        """Run the complete Sphinx setup."""
        print("🚀 Setting up Sphinx documentation...")
        print("=" * 50)

        # Check dependencies
        if not self.check_dependencies():
            print("\n💡 Manual installation required:")
            print(
                "Run: uv add sphinx sphinx-rtd-theme sphinx-autodoc-typehints myst-parser sphinxcontrib-mermaid",
            )
            print("Then run this script again.")
            return False

        # Create directory structure
        self.create_directory_structure()

        # Initialize Sphinx
        if not self.initialize_sphinx():
            return False

        # Create configuration
        self.create_conf_py()

        # Create documentation pages
        self.create_index_rst()
        self.create_overview_rst()
        self.create_category_pages()
        self.create_api_documentation()
        self.create_tutorials()
        self.create_examples()
        self.create_custom_css()
        self.create_makefile()

        # Build documentation
        if self.build_documentation():
            print("\n🎉 Sphinx documentation setup complete!")
            print(f"📁 Documentation location: {self.sphinx_path}")
            print(f"🌐 Open: {self.sphinx_path}/build/html/index.html")
            print("\n💡 Useful commands:")
            print(f"  cd {self.sphinx_path}")
            print("  make html          # Build HTML documentation")
            print("  make serve         # Serve documentation locally")
            print("  make open          # Open in browser")
            print("  make clean         # Clean build files")
            return True
        print("❌ Documentation setup failed")
        return False


def main():
    """Main function."""
    setup = SphinxDocSetup()
    setup.run_setup()


if __name__ == "__main__":
    main()

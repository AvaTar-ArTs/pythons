# Configuration file for the Sphinx documentation builder.
#
# Documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

# --- Path setup: Add parent dirs for imports ---
docs_root = Path(__file__).parent
sys.path.insert(0, str(docs_root.parent / 'pythons'))
sys.path.insert(0, str(docs_root.parent))

# -- Project information -----------------------------------------------------
project = 'SEO Content Optimization Suite'
copyright = '2025, Steven'
author = 'Steven'
version = '1.0.0'
release = version

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.autosummary',
    'sphinx_autodoc_typehints',
]

# Add myst_parser if you want Markdown support in docs
# extensions.append('myst_parser')

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- HTML output options -----------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
}

# -- Extension configuration -------------------------------------------------

# Napoleon: Google/NumPy docstring support
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

# Autodoc default options
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
autodoc_member_order = 'bysource'  # Explicit member order

# Type hint rendering
typehints_fully_qualified = False
always_document_param_types = True
typehints_document_rtype = True

# Intersphinx for cross-project references
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    # Add more mappings if referencing external APIs
}

# -- Additional suggestions --------------------------------------------------
# Uncomment below lines for additional nice-to-haves:

# import sphinx_rtd_theme
# html_style = None  # Use theme's default CSS

# def setup(app):
#     app.add_css_file('custom.css')  # If you have custom Sphinx CSS


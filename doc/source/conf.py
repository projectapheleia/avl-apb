# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
from unittest import mock

MOCK_MODULES = [
    "cocotb", "cocotb.utils", "cocotb.simulator", "cocotb.triggers", "cocotb.clock",
    "cocotb.handle", "cocotb.binary", "cocotb.decorators", "cocotb.result"
]
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.MagicMock()

sys.path.insert(0, os.path.abspath('../../avl_apb'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'avl-apb'
copyright = '2025, apheleia'
author = 'apheleia'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.graphviz',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx'
]

templates_path = ['_templates']
exclude_patterns = []

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'private-members': True,
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

autodoc_typehints = "description"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

graphviz_output_format = 'svg'
html_theme = 'sphinx_rtd_theme'

# -- Options for LaTeX (PDF) output -------------------------------------------
latex_elements = {
    # Paper size
    'papersize': 'a4paper',

    # Font size
    'pointsize': '11pt',

    # Additional LaTeX preamble
    'preamble': r'''
\usepackage{amsmath}
\usepackage{amssymb}
''',

    # Figure alignment
    'figure_align': 'H',
}

# Name of the master document
master_doc = 'index'

intersphinx_mapping = {
    'avl-core': ('https://avl-core.readthedocs.io/en/latest/', None),
}

def skip_private_members(app, what, name, obj, skip, options):
    # Skip all members that start with a single underscore, but not dunder methods
    if name.startswith('_') and not name.startswith('__'):
        return True
    return skip

def setup(app):
    app.connect("autodoc-skip-member", skip_private_members)

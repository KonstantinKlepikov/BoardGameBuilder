# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sys, os

# Insert Requests' path into the system.
sys.path.insert(0, os.path.abspath("..."))
sys.path.insert(0, os.path.abspath('.../bgameb'))

import bgameb

project = 'BoardGameBuild'
copyright = '2022, Konstantin Klepikov'
author = 'Konstantin Klepikov'
version = bgameb.PUB_VERSION
release = bgameb.PUB_VERSION


# The master toctree document.
master_doc = "index"

# Extentiomns
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    ]

# Templates
templates_path = ['_templates']
exclude_patterns = ['_build']

# Outputs
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# The suffix(es) of source filenames.
source_suffix = ['.rst', '.md']

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = False

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

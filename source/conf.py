# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from pathlib import Path

from importlib.metadata import version as get_version

# Used when building API docs, put the dependencies
# of any class you are documenting here
autodoc_mock_imports = []

# When building locally next to a PyNutil checkout, prefer that source tree.
# In CI, requirements.txt installs PyNutil from GitHub instead.
default_source_checkout = Path(__file__).resolve().parents[2] / "PyNutil"
source_checkout = Path(os.environ.get("PYNUTIL_SOURCE_PATH", default_source_checkout)).resolve()
if source_checkout.exists():
    sys.path.insert(0, str(source_checkout))

project = "pynutil"
copyright = "2022, BrainGlobe & Nesys"
author = "BrainGlobe & Nesys"
try:
    full_version = get_version(project)
    # Splitting the release on '+' to remove the commit hash
    release = full_version.split('+', 1)[0]
except LookupError:
    # if git is not initialised, still allow local build
    # with a dummy version
    release = "0.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.githubpages",
    "sphinx_autodoc_typehints",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_sitemap",
    "myst_parser",
    "nbsphinx",
    "sphinx_design",
]

# Configure the myst parser to enable cool markdown features
# See https://sphinx-design.readthedocs.io
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
# Automatically add anchors to markdown headings
myst_heading_anchors = 3

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Automatically generate stub pages for API
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "inherited-members": True,
}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "**.ipynb_checkpoints",
    # to ensure that include files (partial pages) aren't built, exclude them
    # https://github.com/sphinx-doc/sphinx/issues/1965#issuecomment-124732907
    "**/includes/**",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "pydata_sphinx_theme"
html_title = "pynutil"
html_logo = "_static/pynutil_mark.svg"
html_favicon = "_static/pynutil_mark.svg"

# Customize the theme
html_theme_options = {
    "navbar_align": "left",
    "show_nav_level": 2,
    "icon_links": [
        {
            # Label for this link
            "name": "GitHub",
            # URL where the link will redirect
            "url": "https://github.com/Neural-Systems-at-UIO/PyNutil",
            # Icon class (if "type": "fontawesome"),
            # or path to local image (if "type": "local")
            "icon": "fa-brands fa-github",
            # The type of image to be used (see below for details)
            "type": "fontawesome",
        }
    ],
    "logo": {
        "text": f"{project} v{release}",
    },
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "footer_start": ["footer_start"],
    "footer_end": ["footer_end"],
}

# Redirect the webpage to another URL
# Sphinx will create the appropriate CNAME file in the build directory
# The default is the URL of the GitHub pages
# https://www.sphinx-doc.org/en/master/usage/extensions/githubpages.html
github_user = "brainglobe"
html_baseurl = "https://pynutil.brainglobe.info/"
sitemap_url_scheme = "{link}"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]


def _fix_read_alignment_docstring(app, what, name, obj, options, lines):
    """Replace the malformed v0.6.1 docstring with equivalent valid markup."""
    if not name.endswith(".read_alignment"):
        return

    lines[:] = [
        "Load registration data using the appropriate registered loader.",
        "",
        "Parameters",
        "----------",
        "path : str",
        "    Path to the registration file.",
        "loader_name : str, optional",
        "    Explicit loader name. By default, PyNutil detects the format.",
        "apply_deformation : bool",
        "    Apply deformation data when available.",
        "apply_damage : bool",
        "    Apply damage masks when available.",
        "deformation_provider : DeformationProvider, optional",
        "    Custom deformation provider.",
        "damage_provider : DamageProvider, optional",
        "    Custom damage provider.",
        "",
        "Returns",
        "-------",
        "RegistrationData",
        "    Registration data with the requested components applied.",
    ]


def setup(app):
    app.connect("autodoc-process-docstring", _fix_read_alignment_docstring)

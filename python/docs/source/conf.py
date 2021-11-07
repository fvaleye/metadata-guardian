# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

import toml

sys.path.insert(0, os.path.abspath("../metadata_guardian/"))
sys.path.insert(0, os.path.abspath("./_ext"))


def get_release_version() -> str:
    """
    Get the release version from the Cargo.toml file

    :return:
    """
    cargo_content = toml.load("../../Cargo.toml")
    return cargo_content["package"]["version"]


# -- Project information -----------------------------------------------------

project = "metadata-guardian"
copyright = "2021 Metadata Guardian contributors"
author = "Florian Valeye"
version = get_release_version()

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc", "edit_on_github"]
autodoc_typehints = "description"
nitpicky = True
nitpick_ignore = [
    ("py:class", "RawDataRules"),
    ("py:class", "pyarrow._fs.FileSystem"),
    ("py:class", "pyarrow._dataset.Dataset"),
    ("py:class", "pyarrow.lib.Schema"),
    ("py:class", "avro.datafile.DataFileReader"),
    ("py:class", "mypy_boto3_athena.client.AthenaClient"),
    ("py:class", "mypy_boto3_glue.client.GlueClient"),
    ("py:class", "snowflake.connector.connection.SnowflakeConnection"),
    ("py:class", "deltalake.data_catalog.DataCatalog"),
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"
html_logo = "../../../logo.png"
html_favicon = "../../../logo.png"
html_theme_options = {
    "external_links": [],
    "github_url": "https://github.com/fvaleye/MetadataGuardian",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

edit_on_github_project = "fvaleye/MetadataGuardian"
edit_on_github_branch = "main"
page_source_prefix = "python/docs/source"

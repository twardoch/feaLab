#!/usr/bin/env python
import os
import warnings

try:
    from sh import pdoc

    isPdoc = True
except ImportError:
    warnings.warn("Run: pip install --user pdoc")
    isPdoc = False

pydocs = os.path.join(os.path.realpath(os.path.dirname(__file__)), "pydocs")
if not os.path.isdir(pydocs):
    os.makedirs(pydocs)
pdoc(
    "feaLab",
    _cwd=pydocs,
    html=False,
    all_submodules=True,
    external_links=True,
    overwrite=True,
)

pydocs = os.path.join(os.path.realpath(os.path.dirname(__file__)), "docs", "pydocs")
if not os.path.isdir(pydocs):
    os.makedirs(pydocs)
pdoc(
    "feaLab",
    _cwd=pydocs,
    html=True,
    all_submodules=True,
    external_links=True,
    overwrite=True,
)

try:
    from sh import pandoc

    isPandoc = True
except ImportError:
    warnings.warn("Run: brew install pandoc")
    isPandoc = False

if isPandoc:
    readmepath = os.path.join(os.path.realpath(os.path.dirname(__file__)), "README.md")
    if os.path.exists(readmepath):
        long_description = pandoc(
            readmepath, read="markdown", write="html", output="docs/index.html"
        )
